"""
ke_jaimini.py — Jaimini astrological context builder.

Computes Chara Karakas (AK/AMK/BK/MK/PK/GK/DK) and Arudha Padas for all 12
houses from a raw chart dict. Called by ke_yoga_evaluator when evaluating
Jaimini-tagged rules.

Does NOT import from knowledge_engine.py to avoid circular imports.
"""
from __future__ import annotations

CHARA_KARAKA_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
CHARA_KARAKA_TITLES  = ["AK", "AMK", "BK", "MK", "PK", "GK", "DK"]

SIGN_ORDER = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

SIGN_LORDS = {
    "Aries": "Mars",   "Taurus": "Venus",  "Gemini": "Mercury",
    "Cancer": "Moon",  "Leo": "Sun",       "Virgo": "Mercury",
    "Libra": "Venus",  "Scorpio": "Mars",  "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

# Maps raw planet name variants to canonical names used by normalize_planet_name()
_RAW_NAME_MAP = {
    "Sun (Surya)": "Sun",       "Moon (Chandra)": "Moon",
    "Mars (Mangal)": "Mars",    "Mercury (Budha)": "Mercury",
    "Jupiter (Brihaspati)": "Jupiter", "Venus (Shukra)": "Venus",
    "Saturn (Shani)": "Saturn", "Rahu": "Rahu", "Ketu": "Ketu",
    "Lagna": "Lagna",
}


def _canon(raw: str) -> str:
    return _RAW_NAME_MAP.get(raw, raw)


def _planet_payloads(chart: dict) -> dict[str, dict]:
    """
    Extract planet payload dicts keyed by canonical planet name.
    Tries chart["planets"] first; falls back to chart["charts"]["D1"]["grahas"].
    degree_in_sign is only available via chart["planets"].
    """
    payloads: dict[str, dict] = {}

    direct = chart.get("planets") or {}
    if isinstance(direct, dict):
        for raw, payload in direct.items():
            name = _canon(raw)
            if isinstance(payload, dict):
                payloads[name] = payload

    if not payloads:
        d1_grahas = ((chart.get("charts") or {}).get("D1") or {}).get("grahas") or []
        for graha in d1_grahas:
            if not isinstance(graha, dict):
                continue
            raw = graha.get("name") or graha.get("code") or ""
            name = _canon(raw)
            if name:
                payloads[name] = graha

    return payloads


# ---------------------------------------------------------------------------
# Chara Karakas
# ---------------------------------------------------------------------------

def calculate_chara_karakas(chart: dict) -> dict[str, str]:
    """
    Assign Chara Karaka titles to the 7 classical planets.

    Planets are sorted by degree_in_sign descending.
    AK (Atmakaraka) = highest degree, AMK = second, ..., DK = lowest.
    Rahu and Ketu are excluded (7-karaka system, standard Parashari Jaimini).
    """
    payloads = _planet_payloads(chart)
    scored: list[tuple[str, float]] = []
    for planet in CHARA_KARAKA_PLANETS:
        payload = payloads.get(planet, {})
        raw_deg = payload.get("degree_in_sign")
        degree = float(raw_deg) if raw_deg is not None else 0.0
        scored.append((planet, degree))

    scored.sort(key=lambda x: x[1], reverse=True)
    return {title: planet for title, (planet, _) in zip(CHARA_KARAKA_TITLES, scored)}


# ---------------------------------------------------------------------------
# Arudha Padas
# ---------------------------------------------------------------------------

def calculate_arudha(house_num: int, lord_house: int) -> int:
    """
    Calculate the Arudha Pada house for a given house and its lord's placement.

    Formula:
      N       = distance from house to its lord (inclusive, 1-indexed)
      raw_al  = N houses from lord

    Edge cases (Parashari Jaimini standard):
      If raw_al falls on the house itself  -> shift to the 10th from that house.
      If raw_al falls on the 7th from house -> shift to the 4th from that house.
    """
    n = ((lord_house - house_num + 12) % 12) + 1
    raw_al = ((lord_house + n - 2) % 12) + 1
    seventh_from_house = ((house_num + 5) % 12) + 1

    if raw_al == house_num:
        return ((house_num + 8) % 12) + 1   # 10th from house (n-1 offset)
    if raw_al == seventh_from_house:
        return ((house_num + 2) % 12) + 1   # 4th from house (n-1 offset)
    return raw_al


def _resolve_house_lords(chart: dict, facts=None) -> dict[int, str]:
    """
    Return house_lords dict (house_num -> lord planet).
    Prefers facts.house_lords if available (already computed by KE).
    Falls back to deriving from lagna sign in chart["houses"].
    """
    if facts is not None and hasattr(facts, "house_lords") and facts.house_lords:
        return dict(facts.house_lords)

    # Try chart["houses"] dict
    houses = chart.get("houses") or {}
    if isinstance(houses, dict) and houses:
        result: dict[int, str] = {}
        for k, v in houses.items():
            try:
                lord = v.get("lord") if isinstance(v, dict) else None
                if lord:
                    result[int(k)] = _canon(str(lord))
            except (ValueError, TypeError):
                continue
        if result:
            return result

    # Derive from lagna sign
    payloads = _planet_payloads(chart)
    lagna_sign = (payloads.get("Lagna") or {}).get("sign")
    if not lagna_sign or lagna_sign not in SIGN_ORDER:
        return {}

    lagna_idx = SIGN_ORDER.index(lagna_sign)
    return {
        h: SIGN_LORDS[SIGN_ORDER[(lagna_idx + h - 1) % 12]]
        for h in range(1, 13)
    }


def _resolve_planet_houses(chart: dict, facts=None) -> dict[str, int]:
    """Return planet -> house mapping, preferring facts over raw chart."""
    planet_houses: dict[str, int] = {}

    if facts is not None and hasattr(facts, "planet_positions"):
        for planet, pos in facts.planet_positions.items():
            h = pos.get("house")
            if h is not None:
                planet_houses[planet] = int(h)

    # Fill gaps from raw chart
    payloads = _planet_payloads(chart)
    for planet, payload in payloads.items():
        if planet not in planet_houses:
            h = payload.get("house")
            if h is not None:
                planet_houses[planet] = int(h)

    return planet_houses


def calculate_all_arudhas(chart: dict, facts=None) -> dict[int, int]:
    """
    Calculate Arudha Pada for all 12 houses.
    Returns {house_num: arudha_house_num}.
    Houses where the lord position is unknown are omitted.
    """
    house_lords   = _resolve_house_lords(chart, facts)
    planet_houses = _resolve_planet_houses(chart, facts)

    arudhas: dict[int, int] = {}
    for house_num in range(1, 13):
        lord = house_lords.get(house_num)
        if not lord:
            continue
        lord_house = planet_houses.get(lord)
        if lord_house is None:
            continue
        arudhas[house_num] = calculate_arudha(house_num, lord_house)

    return arudhas


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def build_jaimini_context(chart: dict, facts=None) -> dict:
    """
    Build the full Jaimini evaluation context for use in ke_yoga_evaluator.

    Args:
        chart: Raw chart dict from vedic_calculator / kundali_router.
               Must contain chart["planets"] with degree_in_sign for Karaka
               calculation to be accurate.
        facts: Optional ChartFacts from knowledge_engine.extract_chart_facts().
               Used for house_lords and planet house positions if chart is sparse.

    Returns:
        {
            "karakas":       {"AK": "Sun", "AMK": "Jupiter", ...},
            "karaka_signs":  {"AK": "Leo", "AMK": "Sagittarius", ...},
            "karaka_houses": {"AK": 1, "AMK": 9, ...},
            "arudhas":       {1: 4, 2: 7, 3: 11, ...},  # house -> arudha house
            "arudha_lagna":  4,                           # Arudha of 1st house
        }
    """
    karakas = calculate_chara_karakas(chart)
    arudhas  = calculate_all_arudhas(chart, facts)

    payloads      = _planet_payloads(chart)
    planet_houses = _resolve_planet_houses(chart, facts)

    karaka_signs:  dict[str, str | None] = {}
    karaka_houses: dict[str, int | None] = {}
    for title, planet in karakas.items():
        payload = payloads.get(planet, {})
        karaka_signs[title]  = payload.get("sign")
        karaka_houses[title] = planet_houses.get(planet)

    return {
        "karakas":       karakas,
        "karaka_signs":  karaka_signs,
        "karaka_houses": karaka_houses,
        "arudhas":       arudhas,
        "arudha_lagna":  arudhas.get(1),
    }
