"""
Mundane Engine -- Core computation layer for Mundane Astrology.
Provides: foundation chart transits, eclipse/lunation checks,
          ingress checks, condition string pattern matcher, mundane_scan().

All live astronomical computation via pyswisseph ONLY.
All LUT interpretation via mundane_lut_evaluator.py (zero API calls).
"""
from __future__ import annotations

import logging
import re
from datetime import datetime, timedelta, timezone
from typing import Any

import swisseph as swe

from mundane_lut_evaluator import evaluate_mundane_lut

logger = logging.getLogger(__name__)

# ── Swiss Ephemeris Setup ────────────────────────────────────────────────────

swe.set_sid_mode(swe.SIDM_LAHIRI)
_SWE_FLAGS = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
_SWE_FLAGS_FALLBACK = swe.FLG_MOSEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

# ── Constants ────────────────────────────────────────────────────────────────

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
    "Dhanishtha", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada",
    "Revati",
]

PLANET_SWE_IDS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,
}

# Claim axis mapping for Mundane domains
_CLAIM_AXIS_MAP = {
    "economy":    "finance",
    "finance":    "finance",
    "governance": "career",
    "calamity":   "health",
    "agriculture":"career",
    "conflict":   "career",
    "macro":      "career",
}

# ── Helpers ──────────────────────────────────────────────────────────────────

def _calc_planet(jd: float, swe_id: int) -> tuple[float, float]:
    """Return (sidereal_longitude, speed_lon). Falls back to MOSEPH if SWIEPH unavailable."""
    try:
        result = swe.calc_ut(jd, swe_id, _SWE_FLAGS)
    except Exception:
        result = swe.calc_ut(jd, swe_id, _SWE_FLAGS_FALLBACK)
    return result[0][0], result[0][3]


def _lon_to_sign(lon: float) -> str:
    return SIGNS[int(lon // 30) % 12]


def _lon_to_sign_degree(lon: float) -> tuple[str, float]:
    sign = SIGNS[int(lon // 30) % 12]
    degree_in_sign = lon % 30
    return sign, degree_in_sign


def _lon_to_nakshatra(lon: float) -> tuple[str, int]:
    nak_width = 360.0 / 27
    nak_index = int(lon / nak_width) % 27
    nak_name = NAKSHATRAS[nak_index]
    pada = int((lon % nak_width) / (nak_width / 4)) + 1
    return nak_name, pada


def _jd_to_utc_iso(jd: float) -> str:
    """Convert Julian Day to ISO UTC string (hr:min:sec precision)."""
    y, mo, d, h = swe.revjul(jd)
    total_secs = h * 3600
    hh = int(total_secs // 3600)
    mm = int((total_secs % 3600) // 60)
    ss = int(total_secs % 60)
    return f"{y:04d}-{mo:02d}-{d:02d}T{hh:02d}:{mm:02d}:{ss:02d}Z"


def _ist_from_utc_iso(utc_iso: str) -> str:
    """Add 5h30m to UTC ISO string for IST."""
    dt = datetime.strptime(utc_iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    ist = dt + timedelta(hours=5, minutes=30)
    return ist.strftime("%Y-%m-%dT%H:%M:%SZ").replace("+00:00", "")


def _date_to_jd(date_str: str) -> float:
    """Convert 'YYYY-MM-DD' to Julian Day at noon UT."""
    y, mo, d = map(int, date_str.split("-"))
    return swe.julday(y, mo, d, 12.0)


def _parse_query_date(query_date: str) -> float:
    """Parse 'YYYY-MM-DD' to JD at noon."""
    return _date_to_jd(query_date)


def _whole_sign_house(planet_sign: str, lagna_sign: str) -> int:
    """Whole Sign house number (1-indexed)."""
    lagna_idx = SIGNS.index(lagna_sign)
    planet_idx = SIGNS.index(planet_sign)
    return (planet_idx - lagna_idx) % 12 + 1


# ── Foundation Chart Transits (Tool D) ───────────────────────────────────────

async def get_foundation_chart_transits(
    country_code: str,
    query_date: str,
    db: Any,
) -> dict:
    """
    Returns current planetary transits over a country's foundation chart,
    cross-referenced against V22 LUTs.
    """
    fc = await db["mundane_foundation_charts"].find_one(
        {"country_code": country_code, "active": True},
        {"_id": 0},
    )
    if fc is None:
        return {"error": f"Foundation chart not found for {country_code}"}

    lagna_sign: str = fc["chart"]["lagna_sign"]
    jd = _parse_query_date(query_date)

    active_transits = []
    for planet_name, swe_id in PLANET_SWE_IDS.items():
        try:
            lon, speed = _calc_planet(jd, swe_id)
            # Ketu = Rahu + 180
            if planet_name == "Rahu":
                ketu_lon = (lon + 180.0) % 360.0
                ketu_sign, ketu_deg = _lon_to_sign_degree(ketu_lon)
                ketu_house = _whole_sign_house(ketu_sign, lagna_sign)
                lut_result = await evaluate_mundane_lut("Ketu", ketu_sign, "governance", db, house=ketu_house)
                active_transits.append({
                    "planet": "Ketu",
                    "current_sign": ketu_sign,
                    "current_degree": round(ketu_deg, 4),
                    "foundation_house": ketu_house,
                    "transit_effect": lut_result.get("effect"),
                    "lut_source": lut_result.get("spec_id_hit"),
                    "claim_axis": "governance",
                    "retrograde": True,
                })
        except Exception as exc:
            logger.warning("Ketu compute error: %s", exc)

        try:
            lon, speed = _calc_planet(jd, swe_id)
        except Exception as exc:
            logger.warning("Planet %s compute error: %s", planet_name, exc)
            continue

        sign, degree_in_sign = _lon_to_sign_degree(lon)
        house = _whole_sign_house(sign, lagna_sign)
        retrograde = speed < 0

        # Primary domain based on planet
        primary_domain = "governance" if planet_name in ("Saturn", "Jupiter", "Rahu") else "economy"
        lut_result = await evaluate_mundane_lut(planet_name, sign, primary_domain, db, house=house)

        active_transits.append({
            "planet": planet_name,
            "current_sign": sign,
            "current_degree": round(degree_in_sign, 4),
            "foundation_house": house,
            "transit_effect": lut_result.get("effect"),
            "lut_source": lut_result.get("spec_id_hit"),
            "claim_axis": _CLAIM_AXIS_MAP.get(primary_domain, "career"),
            "retrograde": retrograde,
        })

    # Eclipses within ±12 months
    date_from = _shift_months(query_date, -12)
    date_to = _shift_months(query_date, 12)
    eclipse_cursor = db["mundane_eclipse_events"].find(
        {
            "event_type": {"$in": ["solar_eclipse", "lunar_eclipse"]},
            "event_date_utc": {"$gte": date_from, "$lte": date_to},
            "active": True,
        },
        {"_id": 0},
        sort=[("event_date_utc", 1)],
    )
    active_eclipses = []
    async for doc in eclipse_cursor:
        active_eclipses.append({
            "event_type": doc["event_type"],
            "event_date_utc": doc["event_date_utc"],
            "sign": doc["sign"],
            "degree_in_sign": doc["degree_in_sign"],
            "eclipse_type": doc.get("eclipse_type"),
        })

    # Ingresses within ±6 months for slow planets
    ingress_from = _shift_months(query_date, -6)
    ingress_to = _shift_months(query_date, 6)
    ingress_cursor = db["mundane_ingress_events"].find(
        {
            "planet": {"$in": ["Saturn", "Jupiter", "Rahu", "Ketu"]},
            "ingress_date_utc": {"$gte": ingress_from, "$lte": ingress_to},
            "active": True,
        },
        {"_id": 0},
        sort=[("ingress_date_utc", 1)],
    )
    active_ingresses = []
    async for doc in ingress_cursor:
        active_ingresses.append({
            "planet": doc["planet"],
            "from_sign": doc["from_sign"],
            "to_sign": doc["to_sign"],
            "ingress_date_utc": doc["ingress_date_utc"],
        })

    return {
        "country_code": country_code,
        "country_name": fc.get("country_name", ""),
        "query_date": query_date,
        "foundation_chart_lagna": lagna_sign,
        "chart_type": fc.get("chart_type", ""),
        "event_date": fc.get("event_date", ""),
        "active_transits": active_transits,
        "active_eclipses_in_range": active_eclipses,
        "active_ingresses_in_range": active_ingresses,
    }


# ── Mundane Condition String Pattern Matcher ──────────────────────────────────

_PLANET_PATTERN = r"(?:Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)"
_SIGN_PATTERN = (
    r"(?:Aries|Taurus|Gemini|Cancer|Leo|Virgo|Libra|Scorpio|"
    r"Sagittarius|Capricorn|Aquarius|Pisces)"
)
_HOUSE_ORDINAL = (
    r"(?:1st|2nd|3rd|4th|5th|6th|7th|8th|9th|10th|11th|12th|"
    r"first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth)"
)

_ORDINAL_MAP = {
    "1st": 1, "first": 1, "2nd": 2, "second": 2, "3rd": 3, "third": 3,
    "4th": 4, "fourth": 4, "5th": 5, "fifth": 5, "6th": 6, "sixth": 6,
    "7th": 7, "seventh": 7, "8th": 8, "eighth": 8, "9th": 9, "ninth": 9,
    "10th": 10, "tenth": 10, "11th": 11, "eleventh": 11, "12th": 12, "twelfth": 12,
}


def extract_mundane_signals(condition_string: str) -> list[dict]:
    """
    Parses a mundane rule condition string and returns checkable signals.
    Each signal maps to one Core Tool query.
    """
    signals = []
    cs = condition_string.lower()

    # Planet in sign / transiting sign
    for m in re.finditer(
        rf"({_PLANET_PATTERN.lower()})\s+(?:in|transiting)\s+({_SIGN_PATTERN.lower()})",
        cs,
    ):
        planet = m.group(1).title()
        sign = m.group(2).title()
        signals.append({"signal_type": "planet_in_sign", "planet": planet, "sign": sign})

    # Eclipse in sign / sign eclipse
    for m in re.finditer(rf"eclipse\s+in\s+({_SIGN_PATTERN.lower()})", cs):
        sign = m.group(1).title()
        signals.append({"signal_type": "eclipse_in_sign", "sign": sign, "window_months": 6})
    for m in re.finditer(rf"({_SIGN_PATTERN.lower()})\s+eclipse", cs):
        sign = m.group(1).title()
        signals.append({"signal_type": "eclipse_in_sign", "sign": sign, "window_months": 6})

    # Planet in Nth house (foundation transit)
    for m in re.finditer(
        rf"({_PLANET_PATTERN.lower()})\s+in\s+(?:the\s+)?({_HOUSE_ORDINAL.lower()})\s+house",
        cs,
    ):
        planet = m.group(1).title()
        house_str = m.group(2).lower()
        house_num = _ORDINAL_MAP.get(house_str)
        if house_num:
            signals.append({
                "signal_type": "planet_in_house",
                "planet": planet,
                "house": house_num,
                "country": "IN",
            })

    # New moon / full moon
    if "new moon" in cs:
        signals.append({"signal_type": "lunation", "lunation_type": "new_moon", "window_months": 1})
    if "full moon" in cs:
        signals.append({"signal_type": "lunation", "lunation_type": "full_moon", "window_months": 1})

    # Conjunction pattern
    for m in re.finditer(
        rf"({_PLANET_PATTERN.lower()})[-\----]\s*({_PLANET_PATTERN.lower()})\s+conjunction",
        cs,
    ):
        p1, p2 = m.group(1).title(), m.group(2).title()
        signals.append({"signal_type": "conjunction", "planet1": p1, "planet2": p2})

    return signals


# ── Core Mundane Scan ─────────────────────────────────────────────────────────

async def mundane_scan(
    claim_axis: str,
    query_date: str,
    country_code: str,
    db: Any,
) -> dict:
    """
    Evaluate mundane signals for a given claim_axis on query_date.
    Returns fired_rules, top_mundane_factor, mundane_polarity, triple_confirmation.
    """
    # Fetch active mundane_macro rules for this claim_axis (or all)
    cursor = db["interpretation_rules"].find(
        {
            "active": True,
            "metadata.precision_tier": "mundane_macro",
            "approval_status": "approved",
        },
        {"_id": 0, "rule_id": 1, "claim_axis": 1, "condition": 1, "interpretation": 1, "claim_polarity": 1},
        limit=50,
    )

    fired_rules: list[dict] = []
    jd = _parse_query_date(query_date)
    axis_filter = _CLAIM_AXIS_MAP.get(claim_axis, claim_axis)

    async for rule in cursor:
        rule_axis = rule.get("claim_axis", "")
        if rule_axis and rule_axis != claim_axis and rule_axis != axis_filter:
            continue

        condition = rule.get("condition", "")
        if not isinstance(condition, str):
            continue

        signals = extract_mundane_signals(condition)
        matched = False
        match_detail = None

        for signal in signals:
            stype = signal.get("signal_type")

            if stype == "planet_in_sign":
                planet = signal["planet"]
                expected_sign = signal["sign"]
                swe_id = PLANET_SWE_IDS.get(planet)
                if swe_id is not None:
                    try:
                        lon, _ = _calc_planet(jd, swe_id)
                        actual_sign = _lon_to_sign(lon)
                        if actual_sign == expected_sign:
                            matched = True
                            match_detail = f"{planet} in {expected_sign}"
                    except Exception:
                        pass

            elif stype == "eclipse_in_sign":
                result = await _check_eclipse_in_sign(signal["sign"], signal.get("window_months", 6), query_date, db)
                if result["matched"]:
                    matched = True
                    match_detail = f"Eclipse in {signal['sign']}"

            elif stype == "planet_in_house":
                fc = await db["mundane_foundation_charts"].find_one(
                    {"country_code": signal.get("country", country_code), "active": True},
                    {"chart.lagna_sign": 1},
                )
                if fc:
                    lagna = fc["chart"]["lagna_sign"]
                    planet = signal["planet"]
                    swe_id = PLANET_SWE_IDS.get(planet)
                    if swe_id is not None:
                        try:
                            lon, _ = _calc_planet(jd, swe_id)
                            p_sign = _lon_to_sign(lon)
                            house = _whole_sign_house(p_sign, lagna)
                            if house == signal["house"]:
                                matched = True
                                match_detail = f"{planet} in H{house} of {signal.get('country', country_code)} chart"
                        except Exception:
                            pass

            elif stype == "lunation":
                result = await _check_recent_lunation(signal["lunation_type"], query_date, db)
                if result["matched"]:
                    matched = True
                    match_detail = signal["lunation_type"]

            if matched:
                break

        if matched:
            fired_rules.append({
                "rule_id": rule.get("rule_id"),
                "claim_axis": rule.get("claim_axis", claim_axis),
                "claim_polarity": rule.get("claim_polarity"),
                "match_detail": match_detail,
                "interpretation": rule.get("interpretation", "")[:200],
            })

    # Determine overall mundane polarity
    polarities = [r.get("claim_polarity") for r in fired_rules if r.get("claim_polarity")]
    mundane_polarity: str | None = None
    if polarities:
        pos = polarities.count("positive")
        neg = polarities.count("negative")
        if pos > neg:
            mundane_polarity = "positive"
        elif neg > pos:
            mundane_polarity = "negative"
        else:
            mundane_polarity = "mixed"

    top_mundane_factor: str | None = None
    if fired_rules:
        top_mundane_factor = fired_rules[0].get("match_detail")

    # Triple confirmation = natal rule already fired (tracked by caller) +
    # mundane_macro rule fired (len(fired_rules) > 0) + at least 1 Core Tool event matched
    core_tool_matched = await _core_tool_event_check(claim_axis, query_date, country_code, db)
    triple_confirmation = len(fired_rules) > 0 and core_tool_matched

    return {
        "fired_rules": fired_rules,
        "top_mundane_factor": top_mundane_factor,
        "mundane_polarity": mundane_polarity,
        "triple_confirmation": triple_confirmation,
        "core_tool_matched": core_tool_matched,
        "claim_axis": claim_axis,
    }


async def _check_eclipse_in_sign(sign: str, window_months: int, query_date: str, db: Any) -> dict:
    """Check if any eclipse occurred in the given sign within the window."""
    date_from = _shift_months(query_date, -window_months)
    date_to = _shift_months(query_date, window_months)
    doc = await db["mundane_eclipse_events"].find_one({
        "event_type": {"$in": ["solar_eclipse", "lunar_eclipse"]},
        "sign": sign,
        "event_date_utc": {"$gte": date_from, "$lte": date_to},
        "active": True,
    })
    return {"matched": doc is not None, "event": doc}


async def _check_recent_lunation(lunation_type: str, query_date: str, db: Any) -> dict:
    """Check if a new/full moon occurred in the last month."""
    date_from = _shift_months(query_date, -1)
    doc = await db["mundane_eclipse_events"].find_one({
        "event_type": lunation_type,
        "event_date_utc": {"$gte": date_from, "$lte": query_date + "T23:59:59Z"},
        "active": True,
    })
    return {"matched": doc is not None}


async def _core_tool_event_check(claim_axis: str, query_date: str, country_code: str, db: Any) -> bool:
    """Check if any Core Tool (eclipse/ingress/transit) event is active for the claim_axis."""
    # Check for eclipse in last 12 months
    date_from = _shift_months(query_date, -12)
    eclipse = await db["mundane_eclipse_events"].find_one({
        "event_type": {"$in": ["solar_eclipse", "lunar_eclipse"]},
        "event_date_utc": {"$gte": date_from, "$lte": query_date + "T23:59:59Z"},
        "active": True,
    })
    if eclipse:
        return True

    # Check for slow-planet ingress in last 6 months
    ingress_from = _shift_months(query_date, -6)
    ingress = await db["mundane_ingress_events"].find_one({
        "planet": {"$in": ["Saturn", "Jupiter", "Rahu", "Ketu"]},
        "ingress_date_utc": {"$gte": ingress_from, "$lte": query_date + "T23:59:59Z"},
        "active": True,
    })
    if ingress:
        return True

    # Check foundation chart exists (always true if seeded)
    fc = await db["mundane_foundation_charts"].find_one(
        {"country_code": country_code, "active": True}, {"_id": 1}
    )
    return fc is not None


def _shift_months(date_str: str, months: int) -> str:
    """Shift a YYYY-MM-DD date by N months (approximate: 30 days per month)."""
    d = datetime.strptime(date_str, "%Y-%m-%d")
    d = d + timedelta(days=months * 30)
    return d.strftime("%Y-%m-%d")
