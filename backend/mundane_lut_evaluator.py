"""
Mundane LUT Evaluator -- queries V22 Mundane Engine Specs (mundane_engine_specs collection).
Zero API calls. All interpretation is from pre-seeded LUTs in the DB.
"""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

SIGN_ELEMENTS = {
    "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
    "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
    "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
    "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water",
}

# Routing table: (planet, domain) → list of spec_ids to query (in priority order)
_LUT_ROUTING: dict[tuple[str, str], list[str]] = {
    # Economy / price matrices
    ("Saturn",  "economy"):      ["gaur-ch10-saturn-transit-price-matrix", "mehta-ch10-macro-conjunction-engine"],
    ("Jupiter", "economy"):      ["gaur-ch10-jupiter-transit-price-matrix"],
    ("Mars",    "economy"):      ["gaur-ch10-mars-transit-price-matrix"],
    ("Mercury", "economy"):      ["gaur-ch10-mercury-transit-price-matrix"],
    ("Venus",   "economy"):      ["gaur-ch10-venus-rahu-transit-price-matrix"],
    ("Rahu",    "economy"):      ["gaur-ch10-venus-rahu-transit-price-matrix"],
    ("Sun",     "agriculture"):  ["gaur-ch10-sun-transit-signs", "gaur-ch10-sun-transit-nakshatras"],
    # Governance
    ("Saturn",  "governance"):   ["gopal-ch13-saturn-house-transit-govt-change", "mehta-ch22-lord-of-year-engine"],
    ("Jupiter", "governance"):   ["mehta-ch22-yearly-cabinet-portfolios"],
    ("Rahu",    "governance"):   ["mehta-ch22-lord-of-year-engine"],
    # Eclipse / calamity
    ("eclipse", "calamity"):     [
        "raphael-ch22-eclipse-sign-element-timing-rules",
        "raphael-ch23-solar-eclipse-decanate-effects",
        "raphael-ch24-lunar-eclipse-decanate-effects",
        "gaur-ch11-eclipse-monthly-zodiac-engine",
        "mehta-seismic-16factors",
        "raphael-ch26-earthquake-9-rules",
    ],
    ("eclipse", "governance"):   ["mehta-assassination-engine"],
    # Industrial / finance
    ("Saturn",  "finance"):      ["gopal-industrial-sector"],
    ("Jupiter", "finance"):      ["gopal-industrial-sector"],
    ("Mars",    "finance"):      ["gopal-industrial-sector"],
    # Macro / ingress
    ("Sun",     "macro"):        ["gaur-ch10-sun-ingress-weekday", "gaur-ch3-universal-horoscope-aries-ingress"],
    ("Jupiter", "macro"):        ["mehta-ch10-macro-conjunction-engine"],
    ("Saturn",  "macro"):        ["mehta-ch10-macro-conjunction-engine"],
    # Conflict
    ("Mars",    "conflict"):     ["raphael-ch22-eclipse-sign-element-timing-rules"],
    ("Rahu",    "conflict"):     ["mehta-ch10-macro-conjunction-engine"],
}


def _extract_effect(spec: dict, planet: str, sign: str | None, house: int | None, domain: str) -> str | None:
    """
    Flexible extractor: tries common field naming conventions across spec types.
    Returns a human-readable effect string or None.
    """
    spec_id: str = spec.get("spec_id", "")

    # ----- Price matrix pattern: data.{sign} or data.rows[].sign -----
    if "transit-price-matrix" in spec_id or "sun-transit" in spec_id:
        data = spec.get("data", spec.get("matrix", spec.get("rows", {})))
        if isinstance(data, dict) and sign:
            row = data.get(sign)
            if row:
                if isinstance(row, str):
                    return row
                if isinstance(row, dict):
                    return row.get("effect") or row.get("interpretation") or row.get("price_effect") or str(row)
        if isinstance(data, list) and sign:
            for row in data:
                if isinstance(row, dict) and row.get("sign") == sign:
                    return row.get("effect") or row.get("interpretation") or row.get("price_effect")

    # ----- House transit pattern (governance) -----
    if "house-transit" in spec_id or "saturn-house" in spec_id:
        data = spec.get("data", spec.get("houses", spec.get("rows", {})))
        if house is not None:
            if isinstance(data, dict):
                row = data.get(str(house)) or data.get(house)
                if row:
                    if isinstance(row, str):
                        return row
                    if isinstance(row, dict):
                        return row.get("effect") or row.get("interpretation") or str(row)
            if isinstance(data, list):
                for row in data:
                    if isinstance(row, dict) and (row.get("house") == house or row.get("house_number") == house):
                        return row.get("effect") or row.get("interpretation")

    # ----- Eclipse sign/element pattern -----
    if "eclipse" in spec_id or "raphael-ch2" in spec_id:
        data = spec.get("data", spec.get("rules", spec.get("rows", {})))
        element = SIGN_ELEMENTS.get(sign, "") if sign else ""
        if isinstance(data, dict):
            row = (sign and data.get(sign)) or (element and data.get(element))
            if row:
                return row if isinstance(row, str) else row.get("effect") or row.get("interpretation") or str(row)
        if isinstance(data, list):
            for row in data:
                if isinstance(row, dict):
                    if sign and row.get("sign") == sign:
                        return row.get("effect") or row.get("interpretation")
                    if element and row.get("element") == element:
                        return row.get("effect") or row.get("interpretation")

    # ----- Industrial sector pattern -----
    if "industrial-sector" in spec_id or "sector" in spec_id:
        data = spec.get("data", spec.get("sectors", spec.get("rows", {})))
        if isinstance(data, dict) and sign:
            row = data.get(sign)
            if row:
                return row if isinstance(row, str) else row.get("sector") or row.get("effect") or str(row)
        if isinstance(data, list) and sign:
            for row in data:
                if isinstance(row, dict) and row.get("sign") == sign:
                    return row.get("sector") or row.get("effect") or row.get("industries")

    # ----- Generic fallback: try any 'interpretation' or 'effect' at top-level -----
    for key in ("interpretation", "effect", "summary", "description", "content"):
        val = spec.get(key)
        if val and isinstance(val, str):
            return val

    # ----- Last resort: return spec title/name if present -----
    return spec.get("title") or spec.get("name") or f"[{spec_id}]"


async def evaluate_mundane_lut(
    planet: str,
    sign: str | None,
    domain: str,
    db: Any,
    house: int | None = None,
) -> dict:
    """
    Query V22 engine specs for planet × sign/house × domain interpretation.
    Returns:
    {
        "matched": bool,
        "spec_ids_queried": list[str],
        "spec_id_hit": str | None,
        "effect": str | None,
        "claim_axis": str,
        "polarity": str | None,
    }
    """
    spec_ids = _LUT_ROUTING.get((planet, domain), [])
    if not spec_ids:
        # Try wildcard match on planet only (any domain)
        for (p, d), ids in _LUT_ROUTING.items():
            if p == planet:
                spec_ids = ids
                break
    if not spec_ids:
        return {
            "matched": False,
            "spec_ids_queried": [],
            "spec_id_hit": None,
            "effect": None,
            "claim_axis": domain,
            "polarity": None,
        }

    spec_ids_queried = []
    for spec_id in spec_ids:
        spec = await db["mundane_engine_specs"].find_one({"spec_id": spec_id})
        if spec is None:
            continue
        spec_ids_queried.append(spec_id)
        effect = _extract_effect(spec, planet, sign, house, domain)
        if effect:
            polarity = _infer_polarity(effect)
            return {
                "matched": True,
                "spec_ids_queried": spec_ids_queried,
                "spec_id_hit": spec_id,
                "effect": effect,
                "claim_axis": domain,
                "polarity": polarity,
            }

    return {
        "matched": False,
        "spec_ids_queried": spec_ids_queried,
        "spec_id_hit": None,
        "effect": None,
        "claim_axis": domain,
        "polarity": None,
    }


def _infer_polarity(effect_text: str) -> str | None:
    """Infer polarity from effect text keywords."""
    if not effect_text:
        return None
    lower = effect_text.lower()
    positive_words = {"benefit", "good", "prosper", "growth", "rise", "gain", "profit",
                      "auspicious", "fortune", "success", "increase", "favorable"}
    negative_words = {"loss", "decline", "fall", "danger", "conflict", "crisis", "disaster",
                      "calamity", "suffering", "harm", "difficult", "adversity", "unfavorable",
                      "famine", "drought", "earthquake", "assassination", "war", "disease"}
    pos = sum(1 for w in positive_words if w in lower)
    neg = sum(1 for w in negative_words if w in lower)
    if pos > neg:
        return "positive"
    if neg > pos:
        return "negative"
    if pos == neg and pos > 0:
        return "mixed"
    return None


def get_lut_routing_keys() -> list[tuple[str, str]]:
    """Return all (planet, domain) keys in the routing table."""
    return list(_LUT_ROUTING.keys())
