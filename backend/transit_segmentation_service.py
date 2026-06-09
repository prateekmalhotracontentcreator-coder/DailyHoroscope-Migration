from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
import logging
from typing import Any, Dict, Optional

import vedic_calculator as vedic_calculator_module
from vedic_calculator import (
    SWE_FLAGS,
    _calc_planet,
    calculate_vimshottari_dasha,
    get_current_dasha,
    get_nakshatra,
)


SEGMENT_DEFINITIONS: dict[str, dict[str, str]] = {
    "sade_sati": {
        "label": "Sade Sati",
        "description": "Saturn transiting 12th/1st/2nd from natal Moon",
    },
    "kantaka_shani": {
        "label": "Kantaka Shani",
        "description": "Saturn in 4th from natal Moon",
    },
    "ashtama_shani": {
        "label": "Ashtama Shani",
        "description": "Saturn in 8th from natal Moon",
    },
    "rahu_moon": {
        "label": "Rahu-Ketu Over Moon",
        "description": "Rahu or Ketu transiting natal Moon sign",
    },
    "saturn_mahadasha": {
        "label": "Saturn/Rahu/Ketu Dasha",
        "description": "Currently in Saturn, Rahu, or Ketu Mahadasha",
    },
    "jupiter_transit_new": {
        "label": "Jupiter Ingress Window",
        "description": "Jupiter changed signs in the last 30 days",
    },
}

SIGN_NAMES = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

_TRANSIT_CACHE: dict[str, dict[str, Any]] = {}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _to_sign_index(longitude: float) -> int:
    return int(float(longitude) / 30) % 12


def _sign_name(index: int | None) -> str:
    if index is None:
        return ""
    return SIGN_NAMES[index % 12]


def _sign_index_from_value(value: Any) -> Optional[int]:
    if isinstance(value, (int, float)):
        number = int(value)
        if 0 <= number <= 11:
            return number
        return number % 12
    if isinstance(value, str):
        normalized = value.strip().lower()
        for idx, sign_name in enumerate(SIGN_NAMES):
            if normalized == sign_name.lower():
                return idx
    return None


def _build_julian_day(target_dt: datetime) -> float:
    swe = vedic_calculator_module.swe
    hour_fraction = (
        target_dt.hour
        + (target_dt.minute / 60)
        + (target_dt.second / 3600)
    )
    return swe.julday(target_dt.year, target_dt.month, target_dt.day, hour_fraction)


def _calc_longitude_for_day(target_dt: datetime, swe_id: int) -> float:
    jd = _build_julian_day(target_dt)
    longitude, _ = _calc_planet(jd, swe_id)
    return float(longitude)


def get_today_transit_planets() -> dict[str, Any]:
    today_key = date.today().isoformat()
    cached = _TRANSIT_CACHE.get(today_key)
    if cached:
        return cached

    swe = vedic_calculator_module.swe
    now_utc = _utc_now()
    jupiter_past_dt = now_utc - timedelta(days=30)

    saturn_longitude = _calc_longitude_for_day(now_utc, int(swe.SATURN))
    rahu_longitude = _calc_longitude_for_day(now_utc, int(swe.TRUE_NODE))
    jupiter_longitude = _calc_longitude_for_day(now_utc, int(swe.JUPITER))
    jupiter_longitude_30d_ago = _calc_longitude_for_day(jupiter_past_dt, int(swe.JUPITER))
    ketu_longitude = (rahu_longitude + 180.0) % 360.0

    payload = {
        "saturn_sign": _to_sign_index(saturn_longitude),
        "saturn_longitude": saturn_longitude,
        "rahu_sign": _to_sign_index(rahu_longitude),
        "rahu_longitude": rahu_longitude,
        "ketu_sign": _to_sign_index(ketu_longitude),
        "ketu_longitude": ketu_longitude,
        "jupiter_sign": _to_sign_index(jupiter_longitude),
        "jupiter_longitude": jupiter_longitude,
        "jupiter_sign_30d_ago": _to_sign_index(jupiter_longitude_30d_ago),
        "jupiter_longitude_30d_ago": jupiter_longitude_30d_ago,
        "computation_date": today_key,
        "cache_created_at": _utc_now().isoformat(),
        "swe_flags": int(SWE_FLAGS),
    }
    _TRANSIT_CACHE.clear()
    _TRANSIT_CACHE[today_key] = payload
    return payload


def classify_user_segments(birth_profile: dict[str, Any], today_transits: dict[str, Any]) -> list[str]:
    natal_moon_sign = birth_profile.get("_derived_moon_sign_index")
    moon_longitude = birth_profile.get("_derived_moon_longitude")
    current_dasha = birth_profile.get("_derived_current_dasha") or {}

    if natal_moon_sign is None and isinstance(moon_longitude, (int, float)):
        natal_moon_sign = _to_sign_index(float(moon_longitude))

    if natal_moon_sign is None:
        return []

    segments: list[str] = []

    sade_sati_signs = [
        (natal_moon_sign - 1) % 12,
        natal_moon_sign,
        (natal_moon_sign + 1) % 12,
    ]
    if today_transits["saturn_sign"] in sade_sati_signs:
        segments.append("sade_sati")

    if today_transits["saturn_sign"] == (natal_moon_sign + 3) % 12:
        segments.append("kantaka_shani")

    if today_transits["saturn_sign"] == (natal_moon_sign + 7) % 12:
        segments.append("ashtama_shani")

    if (
        today_transits["rahu_sign"] == natal_moon_sign
        or today_transits["ketu_sign"] == natal_moon_sign
    ):
        segments.append("rahu_moon")

    maha_lord = current_dasha.get("maha_lord") or current_dasha.get("planet")
    if not maha_lord and isinstance(moon_longitude, (int, float)):
        try:
            dashas = calculate_vimshottari_dasha(
                birth_profile["date_of_birth"],
                float(moon_longitude),
            )
            maha_lord = (get_current_dasha(dashas) or {}).get("planet")
        except Exception as exc:
            logging.warning("Transit dasha lookup failed for %s: %s", birth_profile.get("id"), exc)
    if maha_lord in {"Saturn", "Rahu", "Ketu"}:
        segments.append("saturn_mahadasha")

    if today_transits.get("jupiter_sign") != today_transits.get("jupiter_sign_30d_ago"):
        segments.append("jupiter_transit_new")

    return segments


async def _derive_birth_profile_context(
    db,
    birth_profile: dict[str, Any],
) -> tuple[dict[str, Any], bool]:
    profile = dict(birth_profile)
    moon_longitude = profile.get("moon_longitude")
    moon_sign_index = None
    current_dasha = profile.get("current_dasha") or {}

    if isinstance(moon_longitude, (int, float)):
        moon_sign_index = _to_sign_index(float(moon_longitude))
    elif isinstance(moon_longitude, str):
        try:
            moon_longitude = float(moon_longitude)
            moon_sign_index = _to_sign_index(moon_longitude)
        except Exception:
            moon_longitude = None

    if moon_sign_index is None:
        report = await db.birth_chart_reports.find_one(
            {"profile_id": profile.get("id")},
            {"_id": 0, "moon_sign": 1, "current_dasha": 1},
            sort=[("generated_at", -1)],
        )
        if not report:
            return profile, True
        moon_sign = report.get("moon_sign") or {}
        moon_sign_index = _sign_index_from_value(moon_sign.get("index"))
        if moon_sign_index is None:
            moon_sign_index = _sign_index_from_value(moon_sign.get("sign"))
        current_dasha = current_dasha or report.get("current_dasha") or {}

    profile["_derived_moon_longitude"] = moon_longitude
    profile["_derived_moon_sign_index"] = moon_sign_index
    profile["_derived_current_dasha"] = current_dasha or {}
    return profile, moon_sign_index is None


async def get_segment_summary(db) -> dict[str, Any]:
    today_transits = get_today_transit_planets()
    rows = await db.birth_profiles.find(
        {"transit_alerts_consent": True},
        {"_id": 0},
    ).limit(5000).to_list(5000)

    counts = {segment_id: 0 for segment_id in SEGMENT_DEFINITIONS}
    skipped_profiles = 0

    for birth_profile in rows:
        enriched, should_skip = await _derive_birth_profile_context(db, birth_profile)
        if should_skip:
            skipped_profiles += 1
            continue
        for segment_id in classify_user_segments(enriched, today_transits):
            counts[segment_id] += 1

    return {
        "computed_at": _utc_now().isoformat(),
        "total_profiles_scanned": len(rows),
        "skipped_profiles": skipped_profiles,
        "segments": {
            segment_id: {
                "count": count,
                "label": SEGMENT_DEFINITIONS[segment_id]["label"],
                "description": SEGMENT_DEFINITIONS[segment_id]["description"],
            }
            for segment_id, count in counts.items()
        },
    }


async def get_segment_user_emails(
    db,
    segment_id: str,
    limit: int = 500,
) -> list[dict[str, Any]]:
    if segment_id not in SEGMENT_DEFINITIONS:
        raise ValueError(f"Unknown segment_id: {segment_id}")

    today_transits = get_today_transit_planets()
    users: list[dict[str, Any]] = []
    cursor = db.birth_profiles.find({"transit_alerts_consent": True}, {"_id": 0}).limit(5000)
    async for birth_profile in cursor:
        enriched, should_skip = await _derive_birth_profile_context(db, birth_profile)
        if should_skip:
            continue
        segments = classify_user_segments(enriched, today_transits)
        if segment_id not in segments:
            continue
        email = str(enriched.get("user_email") or "").strip().lower()
        if not email:
            continue
        users.append(
            {
                "email": email,
                "name": enriched.get("name") or "Seeker",
                "moon_sign": _sign_name(enriched.get("_derived_moon_sign_index")),
                "segment": segment_id,
                "profile_id": enriched.get("id"),
            }
        )
        if len(users) >= limit:
            break
    return users
