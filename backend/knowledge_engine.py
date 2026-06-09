from __future__ import annotations

import asyncio
import json
import logging
import os
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from typing import Any

try:
    from motor.motor_asyncio import AsyncIOMotorDatabase
except Exception:  # pragma: no cover - local lightweight validation path
    AsyncIOMotorDatabase = Any  # type: ignore[misc, assignment]

from tranche_filter import apply_tranche_filter
from knowledge_schema import (
    COLLECTION_AUTHOR_VOICES,
    COLLECTION_INTERPRETATION_RULES,
    COLLECTION_NARRATIVE_BRIDGES,
    COLLECTION_SCIENCE_REGISTRY,
    InterpretationRuleDocument,
    KnowledgeNarrativeDomain,
    KnowledgeNarrativeResponse,
    KnowledgeRequestContext,
    TensionBlock,
)


logger = logging.getLogger(__name__)

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
SCIENCE_WEIGHTS = {
    "vedic_astrology": 0.40,
    "palmistry": 0.25,
    "numerology": 0.20,
    "tarot": 0.15,
    "kp": 0.20,
}
STRENGTH_MULTIPLIERS = {"low": 0.70, "medium": 0.85, "high": 1.00, "extreme": 1.15}
CONTEXT_WEIGHTS = {
    "alpha": 0.15,
    "beta": 0.10,
    "gamma": 0.10,
}
NEUTRAL_CONTEXT_SCORE = 1.0
MIN_CONTEXTUAL_ADJUSTMENT = 0.78
MAX_CONTEXTUAL_ADJUSTMENT = 1.22
MODIFIER_FACTORS = {
    "amplify_positive": 1.15,
    "amplify_negative": 1.15,
    "intensify": 1.10,
    "diminish": 0.85,
    "suppress": 0.75,
}
APPROVED_RULE_FILTER = {"active": True, "approval_status": "approved"}
DEFAULT_BACKBONE = "vedic_astrology"
DEFAULT_AUTHOR_VOICE = "classical"
DEFAULT_NARRATIVE_MODEL = os.getenv("KNOWLEDGE_ENGINE_CLAUDE_MODEL", "claude-sonnet-4-5")
CONTRADICTION_THRESHOLD = 0.55
LOW_CONFIDENCE_THRESHOLD = 0.20
PLANET_VARIANTS = {
    "Sun (Surya)": "Sun",
    "Moon (Chandra)": "Moon",
    "Mars (Mangal)": "Mars",
    "Mercury (Budha)": "Mercury",
    "Jupiter (Brihaspati)": "Jupiter",
    "Venus (Shukra)": "Venus",
    "Saturn (Shani)": "Saturn",
    "Sun": "Sun",
    "Moon": "Moon",
    "Mars": "Mars",
    "Mercury": "Mercury",
    "Jupiter": "Jupiter",
    "Venus": "Venus",
    "Saturn": "Saturn",
    "Rahu": "Rahu",
    "Ketu": "Ketu",
    "Lagna": "Lagna",
}
ARC_ANGEL_DOMAIN_MAP = {
    "health": "Health & Fitness",
    "career": "Career & Work",
    "wealth": "Finances",
    "education": "Intellectual Life & Learning",
    "relationships": "Love Relationships",
    "spirituality": "Spirituality",
    "longevity": "Health & Fitness",
    "general": "Emotional Life",
    # Phase 1 additions -- complete the 12-domain coverage
    "family": "Family Life",
    "social": "Social Life & Friendship",
    "travel": "Adventure & Travel",
    "environment": "Environment",
    "creativity": "Creativity & Hobbies",
}
DOMAIN_PRIORITY = [
    "Health & Fitness",
    "Career & Work",
    "Finances",
    "Intellectual Life & Learning",
    "Emotional Life",
    "Spirituality",
    "Love Relationships",
    "Family Life",
    "Social Life & Friendship",
    "Adventure & Travel",
    "Environment",
    "Creativity & Hobbies",
]
DEFAULT_SUPERSESSION_MAP = {
    "career": {"career_growth": ["vedic_astrology", "numerology", "palmistry", "tarot"]},
    "wealth": {"financial_security": ["vedic_astrology", "numerology", "tarot", "palmistry"]},
    "relationships": {
        "partnership_stability": ["vedic_astrology", "numerology", "tarot", "palmistry"],
        "marriage_timing": ["vedic_astrology", "numerology", "tarot", "palmistry"],
    },
    "health": {"health_vitality": ["vedic_astrology", "palmistry", "numerology", "tarot"]},
    "general": {"*": ["vedic_astrology", "numerology", "palmistry", "tarot"]},
}
POLARITY_DISTANCE_MAP = {
    ("positive", "negative"): 1.0,
    ("negative", "positive"): 1.0,
    ("mixed", "positive"): 0.5,
    ("positive", "mixed"): 0.5,
    ("mixed", "negative"): 0.5,
    ("negative", "mixed"): 0.5,
    ("mixed", "neutral"): 0.5,
    ("neutral", "mixed"): 0.5,
    ("neutral", "positive"): 0.25,
    ("positive", "neutral"): 0.25,
    ("neutral", "negative"): 0.25,
    ("negative", "neutral"): 0.25,
}
TIMING_DISTANCE_MAP = {
    ("early", "late"): 1.0,
    ("late", "early"): 1.0,
    ("early", "on_time"): 0.5,
    ("on_time", "early"): 0.5,
    ("late", "on_time"): 0.5,
    ("on_time", "late"): 0.5,
    ("cyclical", "early"): 0.75,
    ("early", "cyclical"): 0.75,
    ("cyclical", "late"): 0.75,
    ("late", "cyclical"): 0.75,
    ("cyclical", "on_time"): 0.5,
    ("on_time", "cyclical"): 0.5,
    ("none", "early"): 0.25,
    ("early", "none"): 0.25,
    ("none", "late"): 0.25,
    ("late", "none"): 0.25,
    ("none", "cyclical"): 0.15,
    ("cyclical", "none"): 0.15,
    ("none", "on_time"): 0.10,
    ("on_time", "none"): 0.10,
}
STRENGTH_BAND_VALUES = {"low": 0, "medium": 1, "high": 2, "extreme": 3}
MODE_SEVERITY = {"synthesis": 0, "tension": 1, "honest_uncertainty": 2}
ARC_ANGEL_DOMAIN_SLUGS = [
    "health",
    "career",
    "finances",
    "learning",
    "emotional",
    "spirituality",
    "relationships",
    "family",
    "social",
    "adventure",
    "environment",
    "creativity",
]
ARC_ANGEL_DOMAIN_LABELS = {
    "health": "Health & Fitness",
    "career": "Career & Work",
    "finances": "Finances",
    "learning": "Intellectual Life & Learning",
    "emotional": "Emotional Life",
    "spirituality": "Spirituality",
    "relationships": "Love Relationships",
    "family": "Family Life",
    "social": "Social Life & Friendship",
    "adventure": "Adventure & Travel",
    "environment": "Environment",
    "creativity": "Creativity & Hobbies",
}
# TD-29: Natural benefic/malefic baseline -- fallback when no approved KE rules match.
# Source: Legacy Model (vedic_calculator.py) planetary classification.
NATURAL_BENEFICS: frozenset[str] = frozenset({"Jupiter", "Venus", "Mercury", "Moon"})
NATURAL_MALEFICS: frozenset[str] = frozenset({"Saturn", "Mars", "Rahu", "Ketu", "Sun"})

MOOLATRIKONA_SIGNS = {
    "Sun": "Leo",
    "Moon": "Taurus",
    "Mars": "Aries",
    "Mercury": "Virgo",
    "Jupiter": "Sagittarius",
    "Venus": "Libra",
    "Saturn": "Aquarius",
}
DASA_VARGA = ["D1", "D2", "D3", "D7", "D9", "D10", "D12", "D16", "D30", "D60"]
VIMSHOPAKA_TIERS = {
    2: "Parijatamsa",
    3: "Uttamamsa",
    4: "Gopuramsa",
    5: "Simhasanamsa",
    6: "Paravatamsa",
    7: "Devalokamsa",
    8: "Suralokamsa",
    9: "Iravatamsa",
    10: "Iravatamsa",
}

ARC_ANGEL_ENGINE_LABEL = "Vedic Astrology Engine Activated"
CONFIDENCE_BASE = 40
PILLAR_1_PER_AREA = 2
PILLAR_2_PER_IR = 1
PILLAR_3_MAX = 10
CONFIDENCE_CAP = 86
ARC_ANGEL_SOCIAL_SPHERE_AREAS = {"family", "social", "environment", "relationships", "adventure", "spirituality"}

ARC_ANGEL_REPORT_SLUGS = {
    "brihat_kundali",
    "numerology",
    "longevity",
    "kp_oracle",
    "tarot_spread",
    "palmistry",
    "lal_kitab",
    "love_compatibility",
    "lunar_cycle",
    "solar_return",
    "karmic_debt",
    "individual_natal",
    "soul_connection",
}

ARC_ANGEL_DOMAIN_IR_MAP = {
    "health": {"longevity", "individual_natal"},
    "career": {"brihat_kundali", "numerology", "individual_natal"},
    "finances": {"brihat_kundali", "lal_kitab", "numerology"},
    "learning": {"brihat_kundali", "kp_oracle"},
    "emotional": {"love_compatibility", "lunar_cycle"},
    "spirituality": {"kp_oracle", "individual_natal"},
    "relationships": {"love_compatibility", "soul_connection"},
    "family": {"brihat_kundali", "individual_natal"},
    "social": {"numerology", "individual_natal"},
    "adventure": {"individual_natal", "solar_return"},
    "environment": {"lal_kitab", "individual_natal"},
    "creativity": {"numerology", "tarot_spread"},
}

ARC_ANGEL_REPORT_ALIASES = {
    "brihat_kundali": "brihat_kundali",
    "brihat-kundli": "brihat_kundali",
    "brihat_kundli": "brihat_kundali",
    "numerology": "numerology",
    "numerology_core_profile": "numerology",
    "numerology_name_correction": "numerology",
    "numerology_annual_forecast": "numerology",
    "numerology_premium_ankjyotish": "numerology",
    "longevity": "longevity",
    "longevity_report": "longevity",
    "kp_oracle": "kp_oracle",
    "krishna_oracle": "kp_oracle",
    "tarot_spread": "tarot_spread",
    "daily-draw": "tarot_spread",
    "daily_draw": "tarot_spread",
    "spread": "tarot_spread",
    "palmistry": "palmistry",
    "hasta_rekha": "palmistry",
    "lal_kitab": "lal_kitab",
    "lk_remedies": "lal_kitab",
    "love_compatibility": "love_compatibility",
    "soul_connection": "soul_connection",
    "deep_synastry_soul_connection": "soul_connection",
    "lunar_cycle": "lunar_cycle",
    "lunar_cycle_wellness": "lunar_cycle",
    "solar_return": "solar_return",
    "karmic_debt": "karmic_debt",
    "individual_natal": "individual_natal",
}

ARC_ANGEL_RUNTIME_SECTION_MAP = {
    "personal": {"career", "finances", "learning"},
    "life": {"health", "emotional", "adventure", "environment"},
    "relationships": {"relationships", "social", "spirituality"},
    "family": {"family", "creativity"},
}

# Phase 1 baseline confidence (birth data only, no questionnaire, no module runs).
ARC_ANGEL_BASELINE_CONFIDENCE_PCT: int = CONFIDENCE_BASE


def _natural_quality(planet: str | None) -> str:
    """TD-29 -- Legacy Model fallback: natural benefic/malefic classification.
    Used when zero approved KE rules exist for the active antardasha planet.
    Jupiter/Venus/Mercury/Moon → auspicious.
    Saturn/Mars/Rahu/Ketu/Sun → inauspicious.
    """
    if not planet:
        return "neutral"
    p = planet.strip().title()
    if p in NATURAL_BENEFICS:
        return "auspicious"
    if p in NATURAL_MALEFICS:
        return "inauspicious"
    return "neutral"


CATEGORY_TO_DOMAIN_SLUG = {
    "health": "health",
    "longevity": "health",
    "career": "career",
    "wealth": "finances",
    "finances": "finances",
    "education": "learning",
    "learning": "learning",
    "general": "emotional",
    "emotional": "emotional",
    "spirituality": "spirituality",
    "relationships": "relationships",
    "family": "family",
    "social": "social",
    "travel": "adventure",
    "adventure": "adventure",
    "environment": "environment",
    "creativity": "creativity",
}
PERIOD_QUALITY_ORDER = {"auspicious": 2, "neutral": 1, "inauspicious": 0}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def normalize_planet_name(value: str | None) -> str | None:
    if not value:
        return None
    cleaned = str(value).strip()
    return PLANET_VARIANTS.get(cleaned, cleaned.split("(", 1)[0].strip())


def normalize_sign_name(value: str | None) -> str | None:
    if not value:
        return None
    cleaned = str(value).strip()
    return cleaned[:1].upper() + cleaned[1:].lower() if cleaned else None


def normalize_nakshatra_name(value: str | None) -> str | None:
    if not value:
        return None
    return " ".join(part.capitalize() for part in str(value).strip().split())


def normalize_dignity(value: str | None) -> str | None:
    if not value:
        return None
    return str(value).strip().lower()


def canonical_key(condition_type: str, *parts: Any) -> str:
    normalized_parts: list[str] = [condition_type]
    for part in parts:
        if part is None:
            continue
        normalized_parts.append(str(part))
    return "|".join(normalized_parts)


def sorted_planet_list(planets: list[str]) -> list[str]:
    return sorted(filter(None, (normalize_planet_name(planet) for planet in planets)))


@dataclass
class ChartFacts:
    keys: set[str] = field(default_factory=set)
    planet_positions: dict[str, dict[str, Any]] = field(default_factory=dict)
    house_planets: dict[int, list[str]] = field(default_factory=lambda: defaultdict(list))
    house_lords: dict[int, str] = field(default_factory=dict)
    yogas: set[str] = field(default_factory=set)
    dasha_levels: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    aspect_targets: dict[str, set[int]] = field(default_factory=lambda: defaultdict(set))
    aspected_by: dict[int, set[str]] = field(default_factory=lambda: defaultdict(set))
    varga_dignities: dict[str, dict[str, Any]] = field(default_factory=dict)
    kp_chains: dict[str, dict[str, str]] = field(default_factory=dict)
    kp_significations: dict[str, list[int]] = field(default_factory=dict)
    cuspal_sub_lords: dict[int, str] = field(default_factory=dict)


@dataclass
class IndexedRule:
    document: InterpretationRuleDocument
    anchor_keys: set[str]


@dataclass
class KnowledgeIndexSnapshot:
    built_at: datetime
    rule_count: int
    key_to_rule_ids: dict[str, set[str]]
    rules_by_id: dict[str, IndexedRule]


def extract_chart_facts(chart: dict[str, Any]) -> ChartFacts:
    facts = ChartFacts()
    planet_positions = _extract_planet_positions(chart)
    facts.planet_positions = planet_positions

    for planet, payload in planet_positions.items():
        house = payload.get("house")
        sign = payload.get("sign")
        nakshatra = payload.get("nakshatra")
        dignity = payload.get("dignity")
        retrograde = bool(payload.get("retrograde"))

        if house is not None:
            facts.keys.add(canonical_key("planet_in_house", planet, house))
            facts.house_planets[int(house)].append(planet)
        if sign:
            facts.keys.add(canonical_key("planet_in_sign", planet, sign))
        if nakshatra:
            facts.keys.add(canonical_key("planet_in_nakshatra", planet, nakshatra))
        if dignity:
            facts.keys.add(canonical_key("planet_dignity", planet, dignity))
        if retrograde:
            facts.keys.add(canonical_key("planet_retrograde", planet, True))
        if bool(payload.get("combust")):
            facts.keys.add(canonical_key("planet_combust", planet, True))

    _populate_conjunction_facts(facts)
    _populate_house_lord_facts(chart, facts)
    _populate_yoga_facts(chart, facts)
    _populate_dasha_facts(chart, facts)
    _populate_aspect_facts(facts)
    _populate_varga_dignity_facts(chart, facts)
    _populate_kp_facts(chart, facts)
    return facts


def _extract_planet_positions(chart: dict[str, Any]) -> dict[str, dict[str, Any]]:
    positions: dict[str, dict[str, Any]] = {}

    if isinstance(chart.get("planets"), dict):
        for raw_name, payload in chart["planets"].items():
            name = normalize_planet_name(raw_name)
            if not name:
                continue
            positions[name] = {
                "house": payload.get("house"),
                "sign": normalize_sign_name(payload.get("sign")),
                "nakshatra": normalize_nakshatra_name(payload.get("nakshatra") if isinstance(payload.get("nakshatra"), str) else (payload.get("nakshatra") or {}).get("name")),
                "retrograde": bool(payload.get("retrograde")),
                "dignity": normalize_dignity(payload.get("dignity")),
                "combust": bool(payload.get("combust")),
                "longitude": float(payload["longitude"]) if isinstance(payload.get("longitude"), (int, float)) else None,
            }

    d1_chart = ((chart.get("charts") or {}).get("D1") or {})
    for graha in d1_chart.get("grahas", []):
        raw_name = graha.get("name") or graha.get("code")
        name = normalize_planet_name(raw_name)
        if not name or name == "Lagna":
            continue
        positions[name] = {
            "house": graha.get("house_whole_sign"),
            "sign": normalize_sign_name(graha.get("sign")),
            "nakshatra": normalize_nakshatra_name(graha.get("nakshatra")),
            "retrograde": bool(graha.get("retrograde")),
            "dignity": normalize_dignity(graha.get("dignity")),
            "combust": bool(graha.get("combust")),
            "longitude": float(graha["longitude"]) if isinstance(graha.get("longitude"), (int, float)) else None,
        }
    return positions


def _populate_conjunction_facts(facts: ChartFacts) -> None:
    for house, planets in facts.house_planets.items():
        normalized = sorted_planet_list(planets)
        if len(normalized) < 2:
            continue
        facts.keys.add(canonical_key("planet_conjunction", *normalized, house))
        for index, first in enumerate(normalized):
            for second in normalized[index + 1 :]:
                facts.keys.add(canonical_key("planet_conjunction", first, second, house))


def _populate_house_lord_facts(chart: dict[str, Any], facts: ChartFacts) -> None:
    if isinstance(chart.get("houses"), dict):
        for house_num, payload in chart["houses"].items():
            try:
                facts.house_lords[int(house_num)] = normalize_planet_name(payload.get("lord")) or str(payload.get("lord"))
            except Exception:
                continue
    d1_chart = ((chart.get("charts") or {}).get("D1") or {})
    for payload in d1_chart.get("houses", []):
        house_num = payload.get("house_num")
        if house_num is None:
            continue
        lord = normalize_planet_name(payload.get("lord"))
        if lord:
            facts.house_lords[int(house_num)] = lord

    for source_house, lord in facts.house_lords.items():
        target_house = (facts.planet_positions.get(lord) or {}).get("house")
        if target_house is None:
            continue
        facts.keys.add(canonical_key("house_lord_in_house", source_house, target_house))


def _populate_yoga_facts(chart: dict[str, Any], facts: ChartFacts) -> None:
    yoga_layer = ((chart.get("layers") or {}).get("yoga") or {})
    for item in yoga_layer.get("items", []):
        if not item.get("matched"):
            continue
        name = item.get("name")
        code = item.get("code")
        if name:
            facts.yogas.add(str(name))
            facts.keys.add(canonical_key("yoga", name))
        if code:
            facts.yogas.add(str(code))
            facts.keys.add(canonical_key("yoga", code))


def _populate_dasha_facts(chart: dict[str, Any], facts: ChartFacts) -> None:
    current = chart.get("current_dasha") or {}
    if isinstance(current, dict) and current.get("planet"):
        planet = normalize_planet_name(current.get("planet"))
        if planet:
            facts.dasha_levels[planet].add("Maha")
            facts.keys.add(canonical_key("dasha_period", planet, "Maha"))

    overview = chart.get("overview") or {}
    for level_name, level in (("Maha", overview.get("current_maha_dasha")), ("Antar", overview.get("current_antar_dasha"))):
        planet = normalize_planet_name(level)
        if planet:
            facts.dasha_levels[planet].add(level_name)
            facts.keys.add(canonical_key("dasha_period", planet, level_name))

    dasha_layer = ((chart.get("layers") or {}).get("vimshottari_dasha") or {})
    for key, level_name in (("current_maha", "Maha"), ("current_antar", "Antar"), ("current_pratyantar", "Pratyantar")):
        payload = dasha_layer.get(key) or {}
        planet = normalize_planet_name(payload.get("planet"))
        if planet:
            facts.dasha_levels[planet].add(level_name)
            facts.keys.add(canonical_key("dasha_period", planet, level_name))


def _planet_longitude(chart: dict[str, Any], planet: str) -> float | None:
    payload = (chart.get("planets") or {}).get(planet) or {}
    longitude = payload.get("longitude")
    if isinstance(longitude, (int, float)):
        return float(longitude)
    d1_chart = ((chart.get("charts") or {}).get("D1") or {})
    d1_planet = d1_chart.get(planet) or {}
    longitude = d1_planet.get("longitude")
    if isinstance(longitude, (int, float)):
        return float(longitude)
    for graha in d1_chart.get("grahas", []):
        name = normalize_planet_name(graha.get("name") or graha.get("code"))
        if name == planet and isinstance(graha.get("longitude"), (int, float)):
            return float(graha["longitude"])
    return None


def _populate_varga_dignity_facts(chart: dict[str, Any], facts: ChartFacts) -> None:
    from kundali_router import EXALTATION_SIGNS, _divisional_sign
    from vedic_calculator import SIGN_LORDS

    for planet in PLANETS[:7]:
        longitude = _planet_longitude(chart, planet)
        if longitude is None:
            facts.varga_dignities[planet] = {"count": 0, "tier": None}
            continue
        count = 0
        for chart_code in DASA_VARGA:
            div_sign = _divisional_sign(longitude, chart_code)
            if div_sign == EXALTATION_SIGNS.get(planet):
                count += 1
                continue
            if SIGN_LORDS.get(div_sign) == planet:
                count += 1
                continue
            if div_sign == MOOLATRIKONA_SIGNS.get(planet):
                count += 1
        facts.varga_dignities[planet] = {"count": count, "tier": VIMSHOPAKA_TIERS.get(count)}


def _normalize_house_numbers(value: Any) -> list[int]:
    if value is None:
        return []
    items = value if isinstance(value, (list, tuple, set)) else [value]
    houses: set[int] = set()
    for item in items:
        try:
            house = int(item)
        except Exception:
            continue
        if 1 <= house <= 12:
            houses.add(house)
    return sorted(houses)


def _extract_cusp_longitudes(chart: dict[str, Any]) -> dict[int, float]:
    cusp_longitudes: dict[int, float] = {}

    def _read_cusp_items(items: Any) -> None:
        if isinstance(items, dict):
            for raw_house, raw_value in items.items():
                try:
                    house = int(raw_house)
                except Exception:
                    continue
                value = raw_value
                if isinstance(raw_value, dict):
                    value = raw_value.get("longitude", raw_value.get("degree", raw_value.get("lon")))
                if isinstance(value, (int, float)) and 1 <= house <= 12:
                    cusp_longitudes[house] = float(value)
            return
        if not isinstance(items, list):
            return
        for index, raw_value in enumerate(items, start=1):
            value = raw_value
            if isinstance(raw_value, dict):
                value = raw_value.get("longitude", raw_value.get("degree", raw_value.get("lon")))
            if isinstance(value, (int, float)):
                cusp_longitudes[index] = float(value)

    _read_cusp_items(chart.get("cusps"))
    _read_cusp_items(chart.get("kp_cusps"))
    _read_cusp_items((chart.get("kp_chart") or {}).get("cusps"))
    return cusp_longitudes


def _populate_kp_facts(chart: dict[str, Any], facts: ChartFacts) -> None:
    from kp_engine import kp_chain

    reverse_house_lords: dict[str, list[int]] = defaultdict(list)
    for house, lord in facts.house_lords.items():
        normalized_lord = normalize_planet_name(lord)
        if normalized_lord:
            reverse_house_lords[normalized_lord].append(int(house))
    for houses in reverse_house_lords.values():
        houses.sort()

    for planet, payload in facts.planet_positions.items():
        longitude = payload.get("longitude")
        if isinstance(longitude, (int, float)):
            chain = kp_chain(float(longitude))
            facts.kp_chains[planet] = {
                "star_lord": str(chain["star_lord"]),
                "sub_lord": str(chain["sub_lord"]),
                "sub_sub_lord": str(chain["sub_sub_lord"]),
            }

    for planet, payload in facts.planet_positions.items():
        score_by_house: dict[int, int] = defaultdict(int)
        house = payload.get("house")
        if house is not None:
            try:
                score_by_house[int(house)] += 3
            except Exception:
                pass

        if planet not in {"Rahu", "Ketu"}:
            for house_num in reverse_house_lords.get(planet, []):
                score_by_house[house_num] += 2

        chain = facts.kp_chains.get(planet)
        if chain:
            for linked_planet in (chain["star_lord"], chain["sub_lord"], chain["sub_sub_lord"]):
                linked_payload = facts.planet_positions.get(linked_planet)
                if linked_payload and linked_payload.get("house") is not None:
                    try:
                        score_by_house[int(linked_payload["house"])] += 1
                    except Exception:
                        pass
                if linked_planet not in {"Rahu", "Ketu"}:
                    for house_num in reverse_house_lords.get(linked_planet, []):
                        score_by_house[house_num] += 1

        facts.kp_significations[planet] = sorted(house_num for house_num, score in score_by_house.items() if score > 0)

    cusp_longitudes = _extract_cusp_longitudes(chart)
    for house_num, longitude in cusp_longitudes.items():
        facts.cuspal_sub_lords[int(house_num)] = str(kp_chain(float(longitude))["sub_lord"])


def get_t05_enrichment(planet: str, facts: ChartFacts) -> dict[str, Any] | None:
    from kp_sublord_table import get_sub_entry_for_sign

    planet_name = normalize_planet_name(planet)
    if not planet_name:
        return None
    payload = facts.planet_positions.get(planet_name)
    chain = facts.kp_chains.get(planet_name)
    if not payload or not chain:
        return None
    sign = payload.get("sign")
    if not sign:
        return None
    return get_sub_entry_for_sign(chain["star_lord"], chain["sub_lord"], str(sign))


def _populate_aspect_facts(facts: ChartFacts) -> None:
    for planet, payload in facts.planet_positions.items():
        house = payload.get("house")
        if house is None:
            continue
        for target_house in _vedic_aspect_targets(planet, int(house)):
            facts.aspect_targets[planet].add(target_house)
            facts.aspected_by[target_house].add(planet)
            facts.keys.add(canonical_key("planet_aspect", planet, target_house))


def _vedic_aspect_targets(planet: str, house: int) -> set[int]:
    offsets = {7}
    if planet == "Mars":
        offsets.update({4, 8})
    elif planet == "Jupiter":
        offsets.update({5, 9})
    elif planet == "Saturn":
        offsets.update({3, 10})
    elif planet in {"Rahu", "Ketu"}:
        offsets.update({5, 9})
    return {((house - 1 + offset - 1) % 12) + 1 for offset in offsets}


def _condition_anchor_keys(condition: dict[str, Any]) -> set[str]:
    condition_type = condition.get("type")
    if condition_type == "planet_in_house":
        return {canonical_key(condition_type, normalize_planet_name(condition.get("planet")), condition.get("house"))}
    if condition_type == "planet_in_sign":
        return {canonical_key(condition_type, normalize_planet_name(condition.get("planet")), normalize_sign_name(condition.get("sign")))}
    if condition_type == "planet_in_nakshatra":
        return {canonical_key(condition_type, normalize_planet_name(condition.get("planet")), normalize_nakshatra_name(condition.get("nakshatra")))}
    if condition_type == "planet_aspect":
        return {canonical_key(condition_type, normalize_planet_name(condition.get("planet")), condition.get("aspecting_house"))}
    if condition_type == "planet_conjunction":
        planets = sorted_planet_list(condition.get("planets") or [])
        return {canonical_key(condition_type, *planets, condition.get("house"))}
    if condition_type == "planet_dignity":
        return {canonical_key(condition_type, normalize_planet_name(condition.get("planet")), normalize_dignity(condition.get("dignity")))}
    if condition_type == "planet_retrograde":
        return {canonical_key(condition_type, normalize_planet_name(condition.get("planet")), True)}
    if condition_type == "planet_combust":
        return {canonical_key(condition_type, normalize_planet_name(condition.get("planet")), True)}
    if condition_type == "house_lord_in_house":
        return {canonical_key(condition_type, condition.get("source_house"), condition.get("target_house"))}
    if condition_type == "yoga":
        return {canonical_key(condition_type, condition.get("yoga_name"))}
    if condition_type == "dasha_period":
        return {canonical_key(condition_type, normalize_planet_name(condition.get("dasha_lord")), condition.get("level"))}
    if condition_type == "kp_sublord":
        keys: set[str] = set()
        planet = normalize_planet_name(condition.get("planet"))
        house = condition.get("house")
        star_lord = normalize_planet_name(condition.get("star_lord") or condition.get("lord"))
        if planet and house is not None and star_lord:
            keys.add(canonical_key(condition_type, planet, house, star_lord))
        if house is not None and star_lord:
            keys.add(canonical_key(condition_type, house, star_lord))
        cusp_num = condition.get("cusp_num")
        sub_lord = normalize_planet_name(condition.get("sub_lord"))
        if cusp_num is not None and sub_lord:
            keys.add(canonical_key(condition_type, cusp_num, sub_lord))
        return keys
    if condition_type == "kp_planet_signification":
        planet = normalize_planet_name(condition.get("planet"))
        houses = _normalize_house_numbers(condition.get("houses") or condition.get("house") or condition.get("target_house"))
        if not houses:
            return {canonical_key(condition_type, planet)}
        return {canonical_key(condition_type, planet, *houses)}
    if condition_type == "kp_star_lord":
        planet = normalize_planet_name(condition.get("planet"))
        star_lord = normalize_planet_name(condition.get("star_lord") or condition.get("lord"))
        return {canonical_key(condition_type, planet, star_lord)}
    if condition_type == "kp_csl":
        house = condition.get("house") or condition.get("cusp_num")
        sub_lord = normalize_planet_name(condition.get("sub_lord") or condition.get("lord"))
        return {canonical_key(condition_type, house, sub_lord)}
    if condition_type == "kp_signification_chain":
        planet = normalize_planet_name(condition.get("planet"))
        houses = _normalize_house_numbers(condition.get("houses") or condition.get("house") or condition.get("target_houses"))
        return {canonical_key(condition_type, planet, *houses)}
    if condition_type == "kp_profession_ruler":
        profession = condition.get("profession")
        return {canonical_key(condition_type, profession)}
    if condition_type == "transit":
        return {canonical_key(condition_type, normalize_planet_name(condition.get("planet")), condition.get("transit_house"))}
    if condition_type == "composite":
        keys: set[str] = set()
        for sub in condition.get("sub_conditions") or []:
            keys.update(_condition_anchor_keys(sub))
        return keys
    return set()


def _condition_matches(condition: dict[str, Any], facts: ChartFacts) -> bool:
    condition_type = condition.get("type")
    if condition_type == "planet_in_house":
        planet = normalize_planet_name(condition.get("planet"))
        payload = facts.planet_positions.get(planet or "")
        if not payload or payload.get("house") != condition.get("house"):
            return False
        if condition.get("sign") and payload.get("sign") != normalize_sign_name(condition.get("sign")):
            return False
        if condition.get("dignity") and payload.get("dignity") != normalize_dignity(condition.get("dignity")):
            return False
        if condition.get("retrograde") is not None and bool(payload.get("retrograde")) != bool(condition.get("retrograde")):
            return False
        if condition.get("nakshatra") and payload.get("nakshatra") != normalize_nakshatra_name(condition.get("nakshatra")):
            return False
        if condition.get("conjunct_with"):
            partner = normalize_planet_name(condition.get("conjunct_with"))
            house_planets = facts.house_planets.get(int(condition.get("house") or 0), [])
            if partner not in house_planets:
                return False
        if condition.get("aspected_by"):
            aspected_by = normalize_planet_name(condition.get("aspected_by"))
            if aspected_by not in facts.aspected_by.get(int(condition.get("house") or 0), set()):
                return False
        if condition.get("dasha_active"):
            active = normalize_planet_name(condition.get("dasha_active"))
            if active not in facts.dasha_levels:
                return False
        return True
    if condition_type == "planet_in_sign":
        planet = normalize_planet_name(condition.get("planet"))
        return (facts.planet_positions.get(planet or "") or {}).get("sign") == normalize_sign_name(condition.get("sign"))
    if condition_type == "planet_in_nakshatra":
        planet = normalize_planet_name(condition.get("planet"))
        return (facts.planet_positions.get(planet or "") or {}).get("nakshatra") == normalize_nakshatra_name(condition.get("nakshatra"))
    if condition_type == "planet_aspect":
        planet = normalize_planet_name(condition.get("planet"))
        return int(condition.get("aspecting_house") or 0) in facts.aspect_targets.get(planet or "", set())
    if condition_type == "planet_conjunction":
        house = int(condition.get("house") or 0)
        expected = set(sorted_planet_list(condition.get("planets") or []))
        actual = set(facts.house_planets.get(house, []))
        return expected.issubset(actual)
    if condition_type == "planet_dignity":
        planet = normalize_planet_name(condition.get("planet"))
        return (facts.planet_positions.get(planet or "") or {}).get("dignity") == normalize_dignity(condition.get("dignity"))
    if condition_type == "planet_retrograde":
        planet = normalize_planet_name(condition.get("planet"))
        return bool((facts.planet_positions.get(planet or "") or {}).get("retrograde"))
    if condition_type == "planet_combust":
        planet = normalize_planet_name(condition.get("planet"))
        return bool((facts.planet_positions.get(planet or "") or {}).get("combust"))
    if condition_type == "house_lord_in_house":
        lord = facts.house_lords.get(int(condition.get("source_house") or 0))
        if not lord:
            return False
        return (facts.planet_positions.get(lord) or {}).get("house") == int(condition.get("target_house") or 0)
    if condition_type == "yoga":
        return str(condition.get("yoga_name")) in facts.yogas
    if condition_type == "dasha_period":
        planet = normalize_planet_name(condition.get("dasha_lord"))
        return str(condition.get("level")) in facts.dasha_levels.get(planet or "", set())
    if condition_type == "yoga_combination":
        from ke_yoga_evaluator import evaluate_yoga_check
        return evaluate_yoga_check(condition, facts).matched
    if condition_type == "kp_sublord":
        planet = normalize_planet_name(condition.get("planet"))
        house = condition.get("house")
        star_lord = normalize_planet_name(condition.get("star_lord") or condition.get("lord"))
        if planet and house is not None:
            try:
                house_num = int(house)
            except Exception:
                return False
            payload = facts.planet_positions.get(planet)
            if not payload or payload.get("house") != house_num:
                return False
        if star_lord and planet:
            chain = facts.kp_chains.get(planet)
            if not chain or chain.get("star_lord") != star_lord:
                return False
        cusp_num = condition.get("cusp_num")
        sub_lord = normalize_planet_name(condition.get("sub_lord"))
        if cusp_num is not None and sub_lord:
            if facts.cuspal_sub_lords.get(int(cusp_num)) != sub_lord:
                return False
        return True
    if condition_type == "kp_planet_signification":
        planet = normalize_planet_name(condition.get("planet"))
        if not planet:
            return False
        target_houses = _normalize_house_numbers(condition.get("houses") or condition.get("house") or condition.get("target_house"))
        if not target_houses:
            return bool(facts.kp_significations.get(planet))
        actual_houses = set(facts.kp_significations.get(planet, []))
        return set(target_houses).issubset(actual_houses)
    if condition_type == "kp_star_lord":
        planet = normalize_planet_name(condition.get("planet"))
        if not planet:
            return False
        target = normalize_planet_name(condition.get("star_lord") or condition.get("lord"))
        if not target:
            return False
        return (facts.kp_chains.get(planet) or {}).get("star_lord") == target
    if condition_type == "kp_csl":
        house = condition.get("house") or condition.get("cusp_num")
        target = normalize_planet_name(condition.get("sub_lord") or condition.get("lord") or condition.get("star_lord"))
        if house is None or not target:
            return False
        try:
            house_num = int(house)
        except Exception:
            return False
        return facts.cuspal_sub_lords.get(house_num) == target
    if condition_type == "kp_signification_chain":
        planet = normalize_planet_name(condition.get("planet"))
        if not planet:
            return False
        target_houses = _normalize_house_numbers(condition.get("houses") or condition.get("house") or condition.get("target_houses"))
        if not target_houses:
            return False
        actual_houses = set(facts.kp_significations.get(planet, []))
        return set(target_houses).issubset(actual_houses)
    if condition_type == "kp_profession_ruler":
        from kp_sublord_table import get_profession_entry

        profession = condition.get("profession")
        if not profession:
            return False
        return get_profession_entry(str(profession)) is not None
    if condition_type == "composite":
        sub_conditions = condition.get("sub_conditions") or []
        operator = str(condition.get("operator") or "and").lower()
        results = [_condition_matches(sub, facts) for sub in sub_conditions]
        if operator == "and":
            return all(results)
        if operator == "or":
            return any(results)
        return False
    return False


def _modifier_factor(modifiers: list[Any], facts: ChartFacts) -> tuple[float, list[str]]:
    factor = 1.0
    applied: list[str] = []
    for modifier in modifiers:
        condition = getattr(modifier, "condition", None) or modifier.get("condition") or {}
        if not _condition_matches(condition, facts):
            continue
        effect = getattr(modifier, "effect", None) or modifier.get("effect") or ""
        applied.append(effect)
        factor *= MODIFIER_FACTORS.get(str(effect), 1.0)
    return factor, applied


def _backbone_adjusted_weight(science_id: str, backbone_science_id: str | None) -> float:
    base = SCIENCE_WEIGHTS.get(science_id, 0.10)
    if backbone_science_id and backbone_science_id != DEFAULT_BACKBONE and science_id == backbone_science_id:
        return base + 0.10
    return base


def _contextual_adjustment(context: KnowledgeRequestContext) -> float:
    alpha_score = _context_score(context.alpha)
    beta_score = _context_score(context.beta)
    gamma_score = _context_score(context.gamma)
    adjustment = 1.0 + (
        CONTEXT_WEIGHTS["alpha"] * (alpha_score - NEUTRAL_CONTEXT_SCORE)
        + CONTEXT_WEIGHTS["beta"] * (beta_score - NEUTRAL_CONTEXT_SCORE)
        + CONTEXT_WEIGHTS["gamma"] * (gamma_score - NEUTRAL_CONTEXT_SCORE)
    )
    return round(max(MIN_CONTEXTUAL_ADJUSTMENT, min(MAX_CONTEXTUAL_ADJUSTMENT, adjustment)), 4)


def _score_rule(
    rule: InterpretationRuleDocument,
    facts: ChartFacts,
    context: KnowledgeRequestContext,
) -> tuple[float, float, list[str], float]:
    priority_factor = 0.50 + (rule.priority / 10.0)
    intensity = rule.intensity_score if rule.intensity_score > 0 else 1.0
    strength = STRENGTH_MULTIPLIERS.get(rule.strength_band, 0.85)
    science_weight = _backbone_adjusted_weight(rule.science_id, context.backbone_science_id)
    modifier_factor, applied_modifiers = _modifier_factor(rule.modifiers, facts)
    contextual_adjustment = _contextual_adjustment(context)
    score = round(
        rule.weight
        * priority_factor
        * intensity
        * (1.0 + science_weight)
        * strength
        * modifier_factor
        * contextual_adjustment,
        6,
    )
    effective_confidence = round(min(1.15, science_weight * strength), 4)
    return score, effective_confidence, applied_modifiers, contextual_adjustment


def _context_score(value: float | dict[str, Any] | Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, dict):
        return float(value.get("score", 1.0))
    score = getattr(value, "score", None)
    if isinstance(score, (int, float)):
        return float(score)
    return 1.0


def _confidence_band(value: float) -> str:
    if value >= 1.0:
        return "VERIFIED"
    if value >= 0.80:
        return "HIGH"
    if value >= 0.60:
        return "MEDIUM"
    return "LOW"


def _category_to_domain(category: str) -> str:
    return ARC_ANGEL_DOMAIN_MAP.get(category, category.replace("_", " ").title())


def _category_to_domain_slug(category: str) -> str:
    key = str(category or "").strip().lower()
    return CATEGORY_TO_DOMAIN_SLUG.get(key, "emotional")


def _normalize_domain_name(value: str) -> str:
    if value in DOMAIN_PRIORITY:
        return value
    for category, label in ARC_ANGEL_DOMAIN_MAP.items():
        if value == category:
            return label
    return value


def _normalize_domain_slug(value: str) -> str:
    key = str(value or "").strip()
    if key in ARC_ANGEL_DOMAIN_SLUGS:
        return key
    if key in ARC_ANGEL_DOMAIN_LABELS.values():
        for slug, label in ARC_ANGEL_DOMAIN_LABELS.items():
            if key == label:
                return slug
    return _category_to_domain_slug(key)


def _empty_domain_rule_map() -> dict[str, list[dict[str, Any]]]:
    return {domain: [] for domain in ARC_ANGEL_DOMAIN_SLUGS}


def build_domain_rule_map(matched_rules: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped = _empty_domain_rule_map()
    for rule in matched_rules:
        categories = rule.get("categories") or []
        slugs = {_category_to_domain_slug(category) for category in categories if category}
        if not slugs:
            slugs = {_normalize_domain_slug(str(rule.get("life_domain") or "emotional"))}
        for slug in slugs:
            grouped.setdefault(slug, []).append(rule)
    return grouped


def _coerce_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time(), tzinfo=timezone.utc)
    text = str(value).strip()
    if not text:
        return None
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        try:
            dt = datetime.fromisoformat(f"{text}T00:00:00+00:00")
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _coerce_date(value: Any) -> date | None:
    dt = _coerce_datetime(value)
    return dt.date() if dt else None


def compute_dasha_timeline(chart: dict[str, Any]) -> list[dict[str, Any]]:
    from vedic_calculator import build_dasha_timeline

    birth_details = chart.get("birth_details") or {}
    birth_date = str(birth_details.get("date") or "").strip()
    moon_longitude = chart.get("moon_longitude")
    if not birth_date or not isinstance(moon_longitude, (int, float)):
        return []
    # Removed: TD-28 -- moved to vedic_calculator.build_dasha_timeline()
    return build_dasha_timeline(birth_date, float(moon_longitude))


def _active_dasha_pair(
    dasha_timeline: list[dict[str, Any]],
    as_of: date | None = None,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    if not dasha_timeline:
        return None, None
    target = as_of or date.today()
    active_maha: dict[str, Any] | None = None
    for maha in dasha_timeline:
        start_date = _coerce_date(maha.get("start"))
        end_date = _coerce_date(maha.get("end"))
        if start_date and end_date and start_date <= target <= end_date:
            active_maha = maha
            break
    if active_maha is None:
        active_maha = dasha_timeline[-1]

    active_antar: dict[str, Any] | None = None
    for antar in active_maha.get("antardashas") or []:
        start_date = _coerce_date(antar.get("start"))
        end_date = _coerce_date(antar.get("end"))
        if start_date and end_date and start_date <= target <= end_date:
            active_antar = antar
            break
    if active_antar is None:
        antardashas = active_maha.get("antardashas") or []
        active_antar = antardashas[-1] if antardashas else None
    return active_maha, active_antar


def _rule_condition(rule: dict[str, Any]) -> dict[str, Any]:
    condition = rule.get("condition") or {}
    return condition if isinstance(condition, dict) else {}


def _period_quality_reason(rule: dict[str, Any]) -> str:
    interpretation = rule.get("interpretation") or {}
    text = str(interpretation.get("summary") or interpretation.get("detailed") or "").strip()
    if not text:
        return ""
    sentence = text.split(".", 1)[0].strip()
    if not sentence:
        return ""
    return sentence[0].lower() + sentence[1:] if len(sentence) > 1 else sentence.lower()


def _matching_dasha_rules(
    domain_rules: list[dict[str, Any]],
    mahadasha_lord: str | None,
    antardasha_planet: str | None,
) -> list[dict[str, Any]]:
    if not mahadasha_lord or not antardasha_planet:
        return []
    normalized_maha = normalize_planet_name(mahadasha_lord)
    normalized_antar = normalize_planet_name(antardasha_planet)
    matches: list[dict[str, Any]] = []
    for rule in domain_rules:
        condition = _rule_condition(rule)
        rule_maha = normalize_planet_name(condition.get("dasha_lord"))
        rule_antar = normalize_planet_name(
            condition.get("antardasha_planet") or condition.get("antardasha_lord")
        )
        if rule_maha and rule_antar and rule_maha == normalized_maha and rule_antar == normalized_antar:
            matches.append(rule)
    return matches


def _quality_from_rules(
    domain_rules: list[dict[str, Any]],
    mahadasha_lord: str | None,
    antardasha_planet: str | None,
) -> tuple[str, list[dict[str, Any]]]:
    matching_rules = _matching_dasha_rules(domain_rules, mahadasha_lord, antardasha_planet)
    favourable = [
        rule for rule in matching_rules if str(_rule_condition(rule).get("sub_type") or "") == "dasha_favourable"
    ]
    unfavourable = [
        rule for rule in matching_rules if str(_rule_condition(rule).get("sub_type") or "") == "dasha_unfavourable"
    ]
    if len(favourable) > len(unfavourable):
        return "auspicious", favourable
    if len(unfavourable) > len(favourable):
        return "inauspicious", unfavourable
    # TD-29: No approved KE rules matched -- fall back to Legacy Model natural
    # benefic/malefic classification for the active antardasha planet.
    return _natural_quality(antardasha_planet), []


def assign_period_quality(
    rule: dict[str, Any],
    dasha_timeline: list[dict[str, Any]],
    as_of: date | None = None,
) -> str:
    active_maha, active_antar = _active_dasha_pair(dasha_timeline, as_of=as_of)
    active_maha_lord = normalize_planet_name((active_maha or {}).get("planet"))
    active_antar_planet = normalize_planet_name((active_antar or {}).get("planet"))
    condition = _rule_condition(rule)
    rule_lord = normalize_planet_name(condition.get("dasha_lord"))
    rule_antar = normalize_planet_name(condition.get("antardasha_planet") or condition.get("antardasha_lord"))
    sub_type = str(condition.get("sub_type") or "")
    if (
        rule_lord
        and rule_antar
        and active_maha_lord
        and active_antar_planet
        and rule_lord == active_maha_lord
        and rule_antar == active_antar_planet
    ):
        if sub_type == "dasha_favourable":
            return "auspicious"
        if sub_type == "dasha_unfavourable":
            return "inauspicious"
    return "neutral"


def compute_period_quality_now(
    dasha_timeline: list[dict[str, Any]],
    domain_matched_rules: dict[str, list[dict[str, Any]]],
    as_of: date | None = None,
) -> dict[str, str]:
    active_maha, active_antar = _active_dasha_pair(dasha_timeline, as_of=as_of)
    active_maha_planet = normalize_planet_name((active_maha or {}).get("planet"))
    active_antar_planet = normalize_planet_name((active_antar or {}).get("planet"))
    result = {domain: "neutral" for domain in ARC_ANGEL_DOMAIN_SLUGS}
    for domain in ARC_ANGEL_DOMAIN_SLUGS:
        quality, _ = _quality_from_rules(
            domain_matched_rules.get(domain, []),
            active_maha_planet,
            active_antar_planet,
        )
        result[domain] = quality
    return result


def _flatten_antardasha_periods(
    dasha_timeline: list[dict[str, Any]],
    as_of: date,
    horizon_years: int,
) -> list[dict[str, Any]]:
    horizon_end = as_of + timedelta(days=365 * horizon_years)
    periods: list[dict[str, Any]] = []
    for maha in dasha_timeline:
        maha_planet = normalize_planet_name(maha.get("planet"))
        for antar in maha.get("antardashas") or []:
            start_date = _coerce_date(antar.get("start"))
            end_date = _coerce_date(antar.get("end"))
            antar_planet = normalize_planet_name(antar.get("planet"))
            if not start_date or not end_date or not antar_planet or end_date < as_of or start_date > horizon_end:
                continue
            periods.append(
                {
                    "maha_planet": maha_planet,
                    "antar_planet": antar_planet,
                    "start": max(start_date, as_of),
                    "end": min(end_date, horizon_end),
                }
            )
    periods.sort(key=lambda item: item["start"])
    return periods


def _make_window_entry(
    quality: str,
    start: date,
    end: date,
    maha_planet: str | None,
    antar_planet: str | None,
    domain: str,
    dominant_rule: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "quality": quality,
        "start": start,
        "end": end,
        "segments": [
            {
                "start": start,
                "end": end,
                "maha_planet": maha_planet,
                "antar_planet": antar_planet,
                "dominant_rule": dominant_rule,
                "domain": domain,
            }
        ],
    }


def _window_duration_days(window: dict[str, Any]) -> int:
    return max(1, int((window["end"] - window["start"]).days) + 1)


def _merge_window_group(windows: list[dict[str, Any]], quality: str) -> dict[str, Any]:
    merged_segments: list[dict[str, Any]] = []
    for window in windows:
        merged_segments.extend(window.get("segments", []))
    return {
        "quality": quality,
        "start": min(window["start"] for window in windows),
        "end": max(window["end"] for window in windows),
        "segments": merged_segments,
    }


def _merge_consecutive_quality_windows(windows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not windows:
        return []
    merged: list[dict[str, Any]] = [windows[0]]
    for window in windows[1:]:
        previous = merged[-1]
        contiguous = previous["end"] + timedelta(days=1) >= window["start"]
        if window["quality"] == previous["quality"] and contiguous:
            merged[-1] = _merge_window_group([previous, window], previous["quality"])
        else:
            merged.append(window)
    return merged


def _collapse_short_windows(windows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    collapsed = list(windows)
    index = 0
    while index < len(collapsed):
        window = collapsed[index]
        if _window_duration_days(window) >= 90 or len(collapsed) == 1:
            index += 1
            continue
        previous = collapsed[index - 1] if index > 0 else None
        following = collapsed[index + 1] if index + 1 < len(collapsed) else None
        if previous and following and previous["quality"] == following["quality"]:
            collapsed[index - 1 : index + 2] = [_merge_window_group([previous, window, following], previous["quality"])]
            index = max(index - 1, 0)
            continue
        if previous is None and following is not None:
            collapsed[index : index + 2] = [_merge_window_group([window, following], following["quality"])]
            continue
        if following is None and previous is not None:
            collapsed[index - 1 : index + 1] = [_merge_window_group([previous, window], previous["quality"])]
            index = max(index - 1, 0)
            continue
        if previous and following:
            previous_days = _window_duration_days(previous)
            following_days = _window_duration_days(following)
            if previous_days >= following_days:
                collapsed[index - 1 : index + 1] = [_merge_window_group([previous, window], previous["quality"])]
                index = max(index - 1, 0)
            else:
                collapsed[index : index + 2] = [_merge_window_group([window, following], following["quality"])]
            continue
        index += 1
    return collapsed


def _dominant_rule_for_window(window: dict[str, Any], quality: str) -> tuple[str | None, str | None, dict[str, Any] | None]:
    candidates: list[tuple[float, float, dict[str, Any], dict[str, Any]]] = []
    for segment in window.get("segments", []):
        rule = segment.get("dominant_rule")
        if rule:
            candidates.append(
                (
                    _rule_effective_confidence(rule),
                    _rule_score_value(rule),
                    segment,
                    rule,
                )
            )
    if not candidates:
        first = (window.get("segments") or [{}])[0]
        return first.get("maha_planet"), first.get("antar_planet"), None
    candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
    best_segment = candidates[0][2]
    return best_segment.get("maha_planet"), best_segment.get("antar_planet"), candidates[0][3]


def _window_driver(domain: str, quality: str, window: dict[str, Any]) -> str:
    maha_planet, antar_planet, dominant_rule = _dominant_rule_for_window(window, quality)
    domain_phrase = domain.replace("_", " ")
    reason = _period_quality_reason(dominant_rule or {})
    if reason:
        return f"{antar_planet} AD in {maha_planet} MD -- {domain_phrase} {reason}"
    if antar_planet and maha_planet:
        return f"{antar_planet} AD in {maha_planet} MD -- {domain_phrase} {quality} period"
    return f"{domain_phrase} {quality} window"


def compute_arc_angel_windows(
    dasha_timeline: list[dict[str, Any]],
    domain_matched_rules: dict[str, list[dict[str, Any]]],
    horizon_years: int = 10,
    as_of: date | None = None,
) -> dict[str, dict[str, Any]]:
    base_date = as_of or date.today()
    periods = _flatten_antardasha_periods(dasha_timeline, base_date, horizon_years)
    result: dict[str, dict[str, Any]] = {
        domain: {"auspicious_periods": [], "inauspicious_periods": []} for domain in ARC_ANGEL_DOMAIN_SLUGS
    }
    for domain in ARC_ANGEL_DOMAIN_SLUGS:
        domain_windows: list[dict[str, Any]] = []
        for period in periods:
            quality, dominant_pool = _quality_from_rules(
                domain_matched_rules.get(domain, []),
                period["maha_planet"],
                period["antar_planet"],
            )
            dominant_rule = None
            if dominant_pool:
                dominant_rule = sorted(
                    dominant_pool,
                    key=lambda rule: (_rule_effective_confidence(rule), _rule_score_value(rule)),
                    reverse=True,
                )[0]
            domain_windows.append(
                _make_window_entry(
                    quality=quality,
                    start=period["start"],
                    end=period["end"],
                    maha_planet=period["maha_planet"],
                    antar_planet=period["antar_planet"],
                    domain=domain,
                    dominant_rule=dominant_rule,
                )
            )
        collapsed = _collapse_short_windows(domain_windows)
        for window in collapsed:
            if window["quality"] not in {"auspicious", "inauspicious"}:
                continue
            if _window_duration_days(window) < 90:
                continue
            result[domain][f"{window['quality']}_periods"].append(
                {
                    "start": window["start"].strftime("%Y-%m"),
                    "end": window["end"].strftime("%Y-%m"),
                    "driver": _window_driver(domain, window["quality"], window),
                }
            )
    return result


def _normalize_modules_run(values: list[Any] | None) -> list[str]:
    seen: set[str] = set()
    modules: list[str] = []
    for value in values or []:
        slug = canonicalize_arc_angel_report_slug(value) or str(value or "").strip()
        if slug and slug not in seen:
            seen.add(slug)
            modules.append(slug)
    return modules


def canonicalize_arc_angel_report_slug(value: Any) -> str | None:
    if value is None:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    candidates = [
        raw,
        raw.lower(),
        raw.lower().replace("-", "_"),
        raw.lower().replace(" ", "_"),
        raw.lower().replace("-", "_").replace(" ", "_"),
    ]
    for candidate in candidates:
        mapped = ARC_ANGEL_REPORT_ALIASES.get(candidate)
        if mapped:
            return mapped
    return None


def domain_has_quality_badge(domain_id: str, reports_run: list[Any] | None) -> bool:
    modules = set(_normalize_modules_run(reports_run))
    return bool(modules & ARC_ANGEL_DOMAIN_IR_MAP.get(domain_id, set()))


def _compute_domain_confidence(domain_id: str, profile: dict[str, Any]) -> int:
    areas_completed = {
        str(area)
        for area in ((profile.get("pillar_1") or {}).get("areas_completed") or [])
        if str(area or "").strip()
    }
    score = CONFIDENCE_BASE
    if domain_id in areas_completed:
        score += PILLAR_1_PER_AREA
    return score


def _context_path_complete(payload: dict[str, Any], path: str) -> bool:
    current: Any = payload
    for part in path.split("."):
        if not isinstance(current, dict):
            return False
        current = current.get(part)
    if isinstance(current, str):
        return bool(current.strip())
    return current is not None


def _context_parent_complete(payload: dict[str, Any], parent_key: str) -> bool:
    return _context_path_complete(payload, f"parents_data.{parent_key}.dob") and _context_path_complete(
        payload, f"parents_data.{parent_key}.place"
    )


def build_arc_angel_questionnaire_state(context_profile: dict[str, Any] | None) -> dict[str, Any]:
    payload = context_profile or {}
    section_complete = {
        "personal": all(
            _context_path_complete(payload, field_name)
            for field_name in ("salary_bracket", "family_wealth_tier", "siblings_count")
        ),
        "life": all(
            _context_path_complete(payload, field_name)
            for field_name in ("current_city", "travel_frequency")
        ),
        "relationships": _context_path_complete(payload, "relationship_status"),
        "family": _context_parent_complete(payload, "father") and _context_parent_complete(payload, "mother"),
    }

    areas_completed: set[str] = set()
    for section_id, areas in ARC_ANGEL_RUNTIME_SECTION_MAP.items():
        if section_complete.get(section_id):
            areas_completed.update(areas)

    current_city_bonus = 0.5 if _context_path_complete(payload, "current_city") else 0.0
    father_bonus = 0.5 if _context_parent_complete(payload, "father") else 0.0
    mother_bonus = 0.5 if _context_parent_complete(payload, "mother") else 0.0
    partial_points = current_city_bonus + father_bonus + mother_bonus
    score = min((len(areas_completed) * PILLAR_1_PER_AREA) + partial_points, 24)

    return {
        "areas_completed": sorted(areas_completed),
        "social_sphere_areas_completed": sorted(area for area in areas_completed if area in ARC_ANGEL_SOCIAL_SPHERE_AREAS),
        "current_city_bonus": current_city_bonus,
        "parents_bonus": father_bonus + mother_bonus,
        "partial_points": partial_points,
        "score": score,
        "max_score": 24,
    }


def _normalized_data_completeness(value: dict[str, Any] | None) -> dict[str, Any]:
    payload = value or {}
    return {
        "birth_data": bool(payload.get("birth_data")),
        "questionnaire": bool(payload.get("questionnaire")),
        "modules_run": sorted(_normalize_modules_run(payload.get("modules_run"))),
        "parents_data": bool(payload.get("parents_data")),
    }


def arc_angel_profile_is_fresh(
    profile: dict[str, Any] | None,
    data_completeness: dict[str, Any],
    *,
    now: datetime | None = None,
    freshness_hours: int = 6,
) -> bool:
    payload = profile or {}
    computed_at = _coerce_datetime(payload.get("computed_at"))
    if computed_at is None:
        return False
    reference = now or utc_now()
    if computed_at + timedelta(hours=freshness_hours) <= reference:
        return False
    return _normalized_data_completeness(payload.get("data_completeness")) == _normalized_data_completeness(data_completeness)


def _coerce_pillar_1(existing: dict[str, Any] | None) -> dict[str, Any]:
    payload = existing or {}
    areas_completed = [str(area) for area in payload.get("areas_completed") or [] if str(area or "").strip()]
    social_sphere = [str(area) for area in payload.get("social_sphere_areas_completed") or [] if str(area or "").strip()]
    if not social_sphere:
        social_sphere = [area for area in areas_completed if area in ARC_ANGEL_SOCIAL_SPHERE_AREAS]
    current_city_bonus = float(payload.get("current_city_bonus") or 0.0)
    parents_bonus = float(payload.get("parents_bonus") or 0.0)
    partial_points = float(payload.get("partial_points") or (current_city_bonus + parents_bonus))
    score = min((len(areas_completed) * PILLAR_1_PER_AREA) + partial_points, 24)
    return {
        "areas_completed": areas_completed,
        "social_sphere_areas_completed": social_sphere,
        "current_city_bonus": current_city_bonus,
        "parents_bonus": parents_bonus,
        "partial_points": partial_points,
        "score": score,
        "max_score": 24,
    }


def _coerce_pillar_2(existing: dict[str, Any] | None, data_completeness: dict[str, Any]) -> dict[str, Any]:
    payload = existing or {}
    reports_run = _normalize_modules_run(payload.get("reports_run") or data_completeness.get("modules_run"))
    score = min(len(reports_run), 12) * PILLAR_2_PER_IR
    return {
        "reports_run": reports_run,
        "score": score,
        "max_score": 12,
    }


def _coerce_pillar_3(existing: dict[str, Any] | None) -> dict[str, Any]:
    payload = existing or {}
    tarot_love_score = max(0, min(int(payload.get("tarot_love_score", 0) or 0), 5))
    strategist_score = max(0, min(int(payload.get("strategist_score", 0) or 0), 5))
    pillar_3_score = payload.get("pillar_3_score")
    if pillar_3_score is None:
        pillar_3_score = tarot_love_score + strategist_score
    pillar_3_score = max(0, min(int(pillar_3_score or 0), PILLAR_3_MAX))
    return {
        "tarot_love_score": tarot_love_score,
        "strategist_score": strategist_score,
        "pillar_3_score": pillar_3_score,
        "last_ritual_date": _coerce_datetime(payload.get("last_ritual_date")),
        "decay_started_at": _coerce_datetime(payload.get("decay_started_at")),
        "tarot_love_last_ritual_date": _coerce_datetime(payload.get("tarot_love_last_ritual_date")),
        "strategist_last_ritual_date": _coerce_datetime(payload.get("strategist_last_ritual_date")),
        "tarot_love_decay_started_at": _coerce_datetime(payload.get("tarot_love_decay_started_at")),
        "strategist_decay_started_at": _coerce_datetime(payload.get("strategist_decay_started_at")),
        "tarot_love_last_notification_at": _coerce_datetime(payload.get("tarot_love_last_notification_at")),
        "strategist_last_notification_at": _coerce_datetime(payload.get("strategist_last_notification_at")),
        "notification_pending": payload.get("notification_pending") or [],
        "max_score": 10,
        "note": "Decay engine wired in ARC-2. Sprint 3 reads stored pillar_3_score only.",
    }


def _compute_confidence(profile: dict[str, Any]) -> int:
    p1 = profile.get("pillar_1") or {}
    areas_completed = p1.get("areas_completed")
    if areas_completed is not None:
        pillar_1_score = float(min(len(areas_completed), 12) * PILLAR_1_PER_AREA)
    else:
        pillar_1_score = min(float(p1.get("score") or 0.0), 24.0)

    p2 = profile.get("pillar_2") or {}
    reports_run = p2.get("reports_run")
    if reports_run is not None:
        pillar_2_score = int(min(len(reports_run), 12) * PILLAR_2_PER_IR)
    else:
        pillar_2_score = min(int(p2.get("score") or 0), 12)

    pillar_3_score = min(int((profile.get("pillar_3") or {}).get("pillar_3_score") or 0), PILLAR_3_MAX)
    return min(int(round(CONFIDENCE_BASE + pillar_1_score + pillar_2_score + pillar_3_score)), CONFIDENCE_CAP)


def _period_indicator_for_domain(domain: str, quality: str, windows: dict[str, Any]) -> str:
    if quality == "auspicious":
        period = ((windows.get("auspicious_periods") or [{}])[0]) if windows.get("auspicious_periods") else {}
    elif quality == "inauspicious":
        period = ((windows.get("inauspicious_periods") or [{}])[0]) if windows.get("inauspicious_periods") else {}
    else:
        period = {}
    driver = str(period.get("driver") or "").strip()
    if driver:
        return driver
    return f"{ARC_ANGEL_DOMAIN_LABELS.get(domain, domain)} is currently {quality}"


def build_arc_angel_data_completeness(
    *,
    birth_data: bool = True,
    questionnaire_areas: list[str] | None = None,
    modules_run: list[str] | None = None,
    parents_data: bool = False,
) -> dict[str, Any]:
    return {
        "birth_data": bool(birth_data),
        "questionnaire": bool(questionnaire_areas),
        "modules_run": _normalize_modules_run(modules_run),
        "parents_data": bool(parents_data),
    }


def _default_arc_angel_domain(domain_id: str, computed_at: datetime) -> dict[str, Any]:
    return {
        "domain_id": domain_id,
        "domain_label": ARC_ANGEL_DOMAIN_LABELS.get(domain_id, domain_id),
        "period_quality": "neutral",
        "confidence_pct": ARC_ANGEL_BASELINE_CONFIDENCE_PCT,
        "domain_confidence_pct": ARC_ANGEL_BASELINE_CONFIDENCE_PCT,
        "has_quality_badge": False,
        "period_indicator": _period_indicator_for_domain(domain_id, "neutral", {}),
        "auspicious_periods": [],
        "inauspicious_periods": [],
        "last_updated": computed_at,
    }


def refresh_arc_angel_profile(profile: dict[str, Any]) -> dict[str, Any]:
    computed_at = _coerce_datetime(profile.get("computed_at")) or utc_now()
    profile["computed_at"] = computed_at
    profile["engine_label"] = profile.get("engine_label") or ARC_ANGEL_ENGINE_LABEL
    profile["data_completeness"] = _normalized_data_completeness(profile.get("data_completeness"))
    profile["pillar_1"] = _coerce_pillar_1(profile.get("pillar_1"))
    profile["pillar_2"] = _coerce_pillar_2(profile.get("pillar_2"), profile["data_completeness"])
    profile["pillar_3"] = _coerce_pillar_3(profile.get("pillar_3"))

    pillar_3 = profile["pillar_3"]
    sub_last_dates = [
        value
        for value in (
            pillar_3.get("tarot_love_last_ritual_date"),
            pillar_3.get("strategist_last_ritual_date"),
            pillar_3.get("last_ritual_date"),
        )
        if isinstance(value, datetime)
    ]
    pillar_3["last_ritual_date"] = max(sub_last_dates) if sub_last_dates else pillar_3.get("last_ritual_date")
    active_decays = [
        value
        for value in (
            pillar_3.get("tarot_love_decay_started_at"),
            pillar_3.get("strategist_decay_started_at"),
        )
        if isinstance(value, datetime)
    ]
    pillar_3["decay_started_at"] = min(active_decays) if active_decays else None
    pillar_3["pillar_3_score"] = min(
        int(pillar_3.get("tarot_love_score", 0) or 0) + int(pillar_3.get("strategist_score", 0) or 0),
        PILLAR_3_MAX,
    )

    profile["overall_confidence_pct"] = _compute_confidence(profile)
    existing_domains = {
        str(domain.get("domain_id")): domain
        for domain in (profile.get("domains") or [])
        if isinstance(domain, dict) and domain.get("domain_id")
    }
    reports_run = (profile.get("pillar_2") or {}).get("reports_run") or []
    refreshed_domains: list[dict[str, Any]] = []
    for domain_id in ARC_ANGEL_DOMAIN_SLUGS:
        current = {**_default_arc_angel_domain(domain_id, computed_at), **(existing_domains.get(domain_id) or {})}
        current["domain_label"] = ARC_ANGEL_DOMAIN_LABELS.get(domain_id, domain_id)
        current["confidence_pct"] = profile["overall_confidence_pct"]
        current["domain_confidence_pct"] = _compute_domain_confidence(domain_id, profile)
        current["has_quality_badge"] = domain_has_quality_badge(domain_id, reports_run)
        current["last_updated"] = computed_at
        refreshed_domains.append(current)
    profile["domains"] = refreshed_domains
    return profile


def build_arc_angel_profile_doc(
    *,
    user_id: str,
    birth_date: str,
    birth_time: str,
    birth_place: str,
    domain_quality_now: dict[str, str],
    raw_windows: dict[str, dict[str, Any]],
    data_completeness: dict[str, Any] | None = None,
    existing_profile: dict[str, Any] | None = None,
    computed_at: datetime | None = None,
) -> dict[str, Any]:
    existing = existing_profile or {}
    completeness = _normalized_data_completeness(data_completeness)
    profile: dict[str, Any] = {
        "user_id": user_id,
        "birth_date": birth_date,
        "birth_time": birth_time,
        "birth_place": birth_place,
        "computed_at": computed_at or utc_now(),
        "engine_label": ARC_ANGEL_ENGINE_LABEL,
        "data_completeness": completeness,
        "pillar_1": _coerce_pillar_1(existing.get("pillar_1")),
        "pillar_2": _coerce_pillar_2(existing.get("pillar_2"), completeness),
        "pillar_3": _coerce_pillar_3(existing.get("pillar_3")),
    }
    profile["domains"] = [
        {
            "domain_id": domain_id,
            "domain_label": ARC_ANGEL_DOMAIN_LABELS.get(domain_id, domain_id),
            "period_quality": domain_quality_now.get(domain_id, "neutral"),
            "confidence_pct": ARC_ANGEL_BASELINE_CONFIDENCE_PCT,
            "period_indicator": _period_indicator_for_domain(
                domain_id,
                domain_quality_now.get(domain_id, "neutral"),
                raw_windows.get(domain_id, {}),
            ),
            "auspicious_periods": raw_windows.get(domain_id, {}).get("auspicious_periods", []),
            "inauspicious_periods": raw_windows.get(domain_id, {}).get("inauspicious_periods", []),
            "last_updated": profile["computed_at"],
        }
        for domain_id in ARC_ANGEL_DOMAIN_SLUGS
    ]
    return refresh_arc_angel_profile(profile)


async def load_arc_angel_profile(db: AsyncIOMotorDatabase, user_id: str) -> dict[str, Any]:
    existing = await db.user_arc_angel_profile.find_one({"user_id": user_id}, {"_id": 0})
    if existing:
        return refresh_arc_angel_profile(existing)
    return refresh_arc_angel_profile(
        {
            "user_id": user_id,
            "birth_date": "",
            "birth_time": "",
            "birth_place": "",
            "computed_at": utc_now(),
            "engine_label": ARC_ANGEL_ENGINE_LABEL,
            "data_completeness": build_arc_angel_data_completeness(birth_data=False),
            "pillar_1": {},
            "pillar_2": {},
            "pillar_3": {},
            "domains": [],
        }
    )


async def _upsert_arc_angel_profile_doc(db: AsyncIOMotorDatabase, user_id: str, profile_data: dict[str, Any]) -> None:
    """Persist an Arc Angel profile document. Defined here so knowledge_engine functions
    can call it without creating a circular import with server.py."""
    await db.user_arc_angel_profile.update_one(
        {"user_id": user_id},
        {"$set": profile_data},
        upsert=True,
    )


async def sync_arc_angel_questionnaire_state(
    db: AsyncIOMotorDatabase,
    user_id: str,
    context_profile: dict[str, Any] | None,
) -> dict[str, Any]:
    profile = await load_arc_angel_profile(db, user_id)
    questionnaire_state = build_arc_angel_questionnaire_state(context_profile)
    profile["pillar_1"] = questionnaire_state
    profile["data_completeness"] = build_arc_angel_data_completeness(
        birth_data=bool(profile.get("birth_date") and profile.get("birth_time") and profile.get("birth_place")),
        questionnaire_areas=questionnaire_state.get("areas_completed") or [],
        modules_run=((profile.get("pillar_2") or {}).get("reports_run") or []),
        parents_data=bool(questionnaire_state.get("parents_bonus")),
    )
    refreshed = refresh_arc_angel_profile(profile)
    await _upsert_arc_angel_profile_doc(db, user_id, refreshed)
    return refreshed


async def register_arc_angel_report_run(
    db: AsyncIOMotorDatabase,
    user_id: str,
    report_slug: Any,
) -> dict[str, Any] | None:
    canonical_slug = canonicalize_arc_angel_report_slug(report_slug)
    if not canonical_slug:
        return None
    profile = await load_arc_angel_profile(db, user_id)
    reports_run = _normalize_modules_run(((profile.get("pillar_2") or {}).get("reports_run") or []) + [canonical_slug])
    profile["pillar_2"] = {
        **(profile.get("pillar_2") or {}),
        "reports_run": reports_run,
        "score": min(len(reports_run), 12) * PILLAR_2_PER_IR,
        "max_score": 12,
    }
    profile["data_completeness"] = build_arc_angel_data_completeness(
        birth_data=bool(profile.get("birth_date") and profile.get("birth_time") and profile.get("birth_place")),
        questionnaire_areas=((profile.get("pillar_1") or {}).get("areas_completed") or []),
        modules_run=reports_run,
        parents_data=bool(((profile.get("pillar_1") or {}).get("parents_bonus"))),
    )
    refreshed = refresh_arc_angel_profile(profile)
    await _upsert_arc_angel_profile_doc(db, user_id, refreshed)
    return refreshed


def tiered_recovery_points(days_since_decay_start: int | None) -> int:
    if not days_since_decay_start or days_since_decay_start <= 1:
        return 1
    return 2


async def log_ritual_event(
    db: AsyncIOMotorDatabase,
    user_id: str,
    ritual_type: str,
    *,
    occurred_at: datetime | None = None,
) -> dict[str, Any]:
    if ritual_type not in {"tarot_love", "strategist"}:
        raise ValueError(f"Unsupported ritual_type: {ritual_type}")
    now = occurred_at or utc_now()
    profile = await load_arc_angel_profile(db, user_id)
    pillar_3 = dict(profile.get("pillar_3") or {})
    score_key = "tarot_love_score" if ritual_type == "tarot_love" else "strategist_score"
    last_key = "tarot_love_last_ritual_date" if ritual_type == "tarot_love" else "strategist_last_ritual_date"
    decay_key = "tarot_love_decay_started_at" if ritual_type == "tarot_love" else "strategist_decay_started_at"
    max_score = 5
    existing_score = max(0, min(int(pillar_3.get(score_key, 0) or 0), max_score))
    decay_started_at = _coerce_datetime(pillar_3.get(decay_key))
    recovery = tiered_recovery_points(
        max((now.date() - decay_started_at.date()).days, 1) if decay_started_at else None
    )
    pillar_3[score_key] = min(existing_score + recovery, max_score)
    pillar_3[last_key] = now
    pillar_3[decay_key] = None
    pillar_3["notification_pending"] = [
        item for item in (pillar_3.get("notification_pending") or []) if item.get("ritual_type") != ritual_type
    ]
    profile["pillar_3"] = pillar_3
    refreshed = refresh_arc_angel_profile(profile)
    await _upsert_arc_angel_profile_doc(db, user_id, refreshed)
    return refreshed


async def run_arc_angel_pillar3_decay_job(
    db: AsyncIOMotorDatabase,
    *,
    now: datetime | None = None,
) -> int:
    reference = now or utc_now()
    updated = 0
    cursor = db.user_arc_angel_profile.find({}, {"_id": 0})
    async for raw_profile in cursor:
        profile = refresh_arc_angel_profile(raw_profile)
        pillar_3 = dict(profile.get("pillar_3") or {})
        changed = False
        pending = [item for item in (pillar_3.get("notification_pending") or []) if isinstance(item, dict)]

        for ritual_type, score_key, last_key, decay_key, notif_key in (
            ("tarot_love", "tarot_love_score", "tarot_love_last_ritual_date", "tarot_love_decay_started_at", "tarot_love_last_notification_at"),
            ("strategist", "strategist_score", "strategist_last_ritual_date", "strategist_decay_started_at", "strategist_last_notification_at"),
        ):
            last_ritual_at = _coerce_datetime(pillar_3.get(last_key))
            decay_started_at = _coerce_datetime(pillar_3.get(decay_key))
            last_notification_at = _coerce_datetime(pillar_3.get(notif_key))
            score_value = max(0, min(int(pillar_3.get(score_key, 0) or 0), 5))
            days_since = 999999 if last_ritual_at is None else (reference.date() - last_ritual_at.date()).days

            if days_since == 2:
                should_notify = not last_notification_at or (reference.date() - last_notification_at.date()).days >= 2
                if should_notify:
                    pending.append(
                        {
                            "type": "motivational",
                            "ritual_type": ritual_type,
                            "score": score_value,
                            "queued_at": reference,
                        }
                    )
                    pillar_3[notif_key] = reference
                    changed = True
                continue

            if days_since >= 3 and score_value > 0:
                pillar_3[decay_key] = decay_started_at or reference
                pillar_3[score_key] = max(score_value - 1, 0)
                should_notify = not last_notification_at or (reference.date() - last_notification_at.date()).days >= 2
                if should_notify:
                    pending.append(
                        {
                            "type": "score_dip_risk",
                            "ritual_type": ritual_type,
                            "score": pillar_3[score_key],
                            "queued_at": reference,
                        }
                    )
                    pillar_3[notif_key] = reference
                changed = True

        if not changed:
            continue

        pillar_3["notification_pending"] = pending
        profile["pillar_3"] = pillar_3
        refreshed = refresh_arc_angel_profile(profile)
        await _upsert_arc_angel_profile_doc(db, str(refreshed.get("user_id") or ""), refreshed)
        updated += 1
    return updated


def _rule_payload(rule: dict[str, Any] | Any) -> dict[str, Any]:
    if isinstance(rule, dict):
        return rule
    model_dump = getattr(rule, "model_dump", None)
    if callable(model_dump):
        return model_dump(mode="json", by_alias=True, exclude_none=True)
    return {}


def _rule_effective_confidence(rule: dict[str, Any] | Any) -> float:
    payload = _rule_payload(rule)
    value = payload.get("effective_confidence")
    try:
        if value is not None:
            return float(value)
    except (TypeError, ValueError):
        pass
    return 1.0


def _rule_score_value(rule: dict[str, Any] | Any) -> float:
    payload = _rule_payload(rule)
    value = payload.get("score")
    try:
        if value is not None:
            return float(value)
    except (TypeError, ValueError):
        pass
    return 0.0


def _primary_category(rule: dict[str, Any]) -> str:
    rule = _rule_payload(rule)
    categories = rule.get("categories") or []
    for category in categories:
        if category in DEFAULT_SUPERSESSION_MAP:
            return str(category)
    if categories:
        return str(categories[0])
    life_domain = str(rule.get("life_domain") or "general")
    return life_domain if life_domain in DEFAULT_SUPERSESSION_MAP else "general"


def _domain_names_for_rule(rule: dict[str, Any]) -> list[str]:
    rule = _rule_payload(rule)
    categories = rule.get("categories") or []
    mapped = sorted({_category_to_domain(category) for category in categories})
    if mapped:
        return mapped
    return [_category_to_domain(str(rule.get("life_domain") or "general"))]


def _strength_distance(band_a: str | None, band_b: str | None) -> float:
    value_a = STRENGTH_BAND_VALUES.get(str(band_a or "").lower(), 1)
    value_b = STRENGTH_BAND_VALUES.get(str(band_b or "").lower(), 1)
    return round(abs(value_a - value_b) / 3.0, 4)


def _polarity_distance(polarity_a: str | None, polarity_b: str | None) -> float:
    key = (str(polarity_a or "neutral").lower(), str(polarity_b or "neutral").lower())
    if key[0] == key[1]:
        return 0.0
    return POLARITY_DISTANCE_MAP.get(key, 0.25)


def _timing_distance(timing_a: str | None, timing_b: str | None) -> float:
    key = (str(timing_a or "none").lower(), str(timing_b or "none").lower())
    if key[0] == key[1]:
        return 0.0
    return TIMING_DISTANCE_MAP.get(key, 0.25)


def _authority_distance(
    rule_a: dict[str, Any],
    rule_b: dict[str, Any],
    science_registry: dict[str, dict[str, Any]] | None = None,
) -> float:
    rule_a = _rule_payload(rule_a)
    rule_b = _rule_payload(rule_b)
    science_a = str(rule_a.get("science_id") or "")
    science_b = str(rule_b.get("science_id") or "")
    if not science_a or not science_b or science_a == science_b:
        return 0.0
    registry = science_registry or {}
    rank_a = int((registry.get(science_a) or {}).get("hierarchy_rank", 99))
    rank_b = int((registry.get(science_b) or {}).get("hierarchy_rank", 99))
    known_ranks = [int(doc.get("hierarchy_rank", 0)) for doc in registry.values() if isinstance(doc.get("hierarchy_rank"), int)]
    max_rank_delta = max(1, (max(known_ranks) - min(known_ranks)) if len(known_ranks) >= 2 else 3)
    return round(min(1.0, abs(rank_a - rank_b) / max_rank_delta), 4)


def _contradiction_components(
    rule_a: dict[str, Any],
    rule_b: dict[str, Any],
    science_registry: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    rule_a = _rule_payload(rule_a)
    rule_b = _rule_payload(rule_b)
    if str(rule_a.get("life_domain") or "") != str(rule_b.get("life_domain") or ""):
        return {
            "candidate": False,
            "polarity_delta": 0.0,
            "timing_delta": 0.0,
            "strength_delta": 0.0,
            "authority_delta": 0.0,
            "contradiction_types": [],
        }
    if str(rule_a.get("claim_axis") or "") != str(rule_b.get("claim_axis") or ""):
        return {
            "candidate": False,
            "polarity_delta": 0.0,
            "timing_delta": 0.0,
            "strength_delta": 0.0,
            "authority_delta": 0.0,
            "contradiction_types": [],
        }
    if str(rule_a.get("claim_scope") or "") != str(rule_b.get("claim_scope") or ""):
        return {
            "candidate": False,
            "polarity_delta": 0.0,
            "timing_delta": 0.0,
            "strength_delta": 0.0,
            "authority_delta": 0.0,
            "contradiction_types": [],
        }

    polarity_delta = _polarity_distance(rule_a.get("claim_polarity"), rule_b.get("claim_polarity"))
    timing_delta = _timing_distance(rule_a.get("timing_bias"), rule_b.get("timing_bias"))
    strength_delta = _strength_distance(rule_a.get("strength_band"), rule_b.get("strength_band"))
    authority_delta = _authority_distance(rule_a, rule_b, science_registry)

    contradiction_types: list[str] = []
    if polarity_delta >= 0.5:
        contradiction_types.append("directional")
    if timing_delta >= 0.5:
        contradiction_types.append("temporal")
    if strength_delta >= 0.34:
        contradiction_types.append("strength")
    if authority_delta > 0:
        contradiction_types.append("authority_overlap")

    return {
        "candidate": True,
        "polarity_delta": polarity_delta,
        "timing_delta": timing_delta,
        "strength_delta": strength_delta,
        "authority_delta": authority_delta,
        "contradiction_types": contradiction_types,
    }


def _contradiction_score(
    rule_a: dict[str, Any],
    rule_b: dict[str, Any],
    science_registry: dict[str, dict[str, Any]] | None = None,
) -> tuple[float, bool]:
    rule_a = _rule_payload(rule_a)
    rule_b = _rule_payload(rule_b)
    components = _contradiction_components(rule_a, rule_b, science_registry)
    if not components["candidate"]:
        return 0.0, False
    c_score = round(
        0.40 * float(components["polarity_delta"])
        + 0.35 * float(components["timing_delta"])
        + 0.15 * float(components["strength_delta"])
        + 0.10 * float(components["authority_delta"]),
        4,
    )
    is_contradiction = (
        c_score >= CONTRADICTION_THRESHOLD
        and _rule_effective_confidence(rule_a) >= 0.18
        and _rule_effective_confidence(rule_b) >= 0.18
    )
    return c_score, is_contradiction


def _resolve_supersession_order(
    category: str,
    claim_axis: str,
    science_registry: dict[str, dict[str, Any]] | None = None,
) -> list[str]:
    category_map = DEFAULT_SUPERSESSION_MAP.get(category) or DEFAULT_SUPERSESSION_MAP.get("general", {})
    fallback_order = category_map.get(claim_axis) or category_map.get("*") or []
    registry = science_registry or {}
    if not registry:
        return list(fallback_order)

    def _priority(science_id: str) -> tuple[int, int]:
        document = registry.get(science_id) or {}
        domains = {str(item) for item in document.get("authority_domain", [])}
        domain_match = 0 if claim_axis in domains or category in domains else 1
        rank = int(document.get("hierarchy_rank", 99))
        fallback_rank = fallback_order.index(science_id) if science_id in fallback_order else len(fallback_order) + rank
        return (domain_match, fallback_rank)

    ordered = sorted(registry.keys(), key=_priority)
    if fallback_order:
        ordered = [science_id for science_id in fallback_order if science_id in registry] + [
            science_id for science_id in ordered if science_id not in fallback_order
        ]
    return ordered or list(fallback_order)


def _science_authority_rank(science_id: str, science_registry: dict[str, dict[str, Any]] | None = None) -> int:
    registry = science_registry or {}
    return int((registry.get(science_id) or {}).get("hierarchy_rank", 99))


def _dominant_science_for_pair(
    rule_a: dict[str, Any],
    rule_b: dict[str, Any],
    backbone_science_id: str,
    science_registry: dict[str, dict[str, Any]] | None = None,
) -> str:
    rule_a = _rule_payload(rule_a)
    rule_b = _rule_payload(rule_b)
    science_a = str(rule_a.get("science_id") or "")
    science_b = str(rule_b.get("science_id") or "")
    if science_a == backbone_science_id:
        return science_a
    if science_b == backbone_science_id:
        return science_b

    category = _primary_category(rule_a)
    claim_axis = str(rule_a.get("claim_axis") or "")
    order = _resolve_supersession_order(category, claim_axis, science_registry)
    for science_id in order:
        if science_id in {science_a, science_b}:
            return science_id

    score_a = _rule_effective_confidence(rule_a) + _rule_score_value(rule_a)
    score_b = _rule_effective_confidence(rule_b) + _rule_score_value(rule_b)
    if score_a == score_b:
        return science_a if _science_authority_rank(science_a, science_registry) <= _science_authority_rank(science_b, science_registry) else science_b
    return science_a if score_a > score_b else science_b


def _representation_mode(
    c_scores: list[float],
    top_effective_confidence: float | None = None,
    same_directional_polarity: bool = False,
    confidence_delta: float = 0.0,
) -> str:
    if top_effective_confidence is not None and top_effective_confidence < LOW_CONFIDENCE_THRESHOLD:
        return "honest_uncertainty"
    if not c_scores:
        return "synthesis"
    max_c_score = max(c_scores)
    if max_c_score > 0.75:
        return "honest_uncertainty"
    if same_directional_polarity and confidence_delta >= 0.05:
        return "synthesis"
    if confidence_delta > 0.15:
        return "synthesis"
    if max_c_score < 0.30:
        return "synthesis"
    if 0.30 <= max_c_score <= 0.75:
        return "tension"
    return "honest_uncertainty"


def _compact_tension_summary(rule: dict[str, Any]) -> str:
    rule = _rule_payload(rule)
    interpretation = rule.get("interpretation") or {}
    return str(interpretation.get("summary") or interpretation.get("detailed") or "").strip()


def _build_tension_block(
    rule_a: dict[str, Any],
    rule_b: dict[str, Any],
    c_score: float,
    domain: str,
    backbone_science_id: str | None = None,
    science_registry: dict[str, dict[str, Any]] | None = None,
    representation_mode: str | None = None,
) -> dict[str, Any]:
    rule_a = _rule_payload(rule_a)
    rule_b = _rule_payload(rule_b)
    components = _contradiction_components(rule_a, rule_b, science_registry)
    dominant_science = _dominant_science_for_pair(
        rule_a,
        rule_b,
        backbone_science_id or str(rule_a.get("backbone_science_id") or DEFAULT_BACKBONE),
        science_registry,
    )
    claims = sorted(
        [rule_a, rule_b],
        key=lambda rule: (
            0 if str(rule.get("science_id") or "") == dominant_science else 1,
            -_rule_effective_confidence(rule),
            -_rule_score_value(rule),
            _science_authority_rank(str(rule.get("science_id") or ""), science_registry),
        ),
    )
    confidence_values = [_rule_effective_confidence(rule) for rule in claims]
    confidence_delta = round(abs(confidence_values[0] - confidence_values[1]), 4) if len(confidence_values) >= 2 else 0.0
    same_direction = components["polarity_delta"] == 0.0
    mode = representation_mode or _representation_mode(
        [c_score],
        top_effective_confidence=max(confidence_values) if confidence_values else 0.0,
        same_directional_polarity=same_direction,
        confidence_delta=confidence_delta,
    )
    return TensionBlock(
        life_domain=domain,
        claim_axis=str(rule_a.get("claim_axis") or rule_b.get("claim_axis") or ""),
        representation_mode=mode,
        dominant_science=dominant_science,
        backbone_science_id=backbone_science_id or str(rule_a.get("backbone_science_id") or DEFAULT_BACKBONE),
        confidence_delta=confidence_delta,
        contradiction_score=c_score,
        contradiction_types=list(components["contradiction_types"]),
        tranche_adjustments_applied=bool(rule_a.get("_tranche_adjusted") or rule_b.get("_tranche_adjusted")),
        low_confidence=max(confidence_values) < LOW_CONFIDENCE_THRESHOLD if confidence_values else True,
        claims=[
            {
                "science_id": str(rule.get("science_id") or ""),
                "summary": _compact_tension_summary(rule),
                "effective_confidence": _rule_effective_confidence(rule),
                "authority_rank": _science_authority_rank(str(rule.get("science_id") or ""), science_registry),
            }
            for rule in claims[:2]
        ],
    ).model_dump(mode="json", by_alias=True, exclude_none=True)


def _dominant_representation_mode(modes: list[str]) -> str:
    if not modes:
        return "synthesis"
    return max(modes, key=lambda mode: MODE_SEVERITY.get(mode, 0))


def _arbitration_summary(
    matched_rules: list[dict[str, Any]],
    backbone_science_id: str,
    science_registry: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for rule in matched_rules:
        for domain in _domain_names_for_rule(rule):
            grouped[domain][str(rule.get("claim_axis") or "")].append(rule)

    domain_modes: dict[str, str] = {}
    domain_tension_blocks: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for domain, axis_groups in grouped.items():
        domain_c_scores: list[float] = []
        domain_modes_for_axis: list[str] = []
        for axis, rules in axis_groups.items():
            if not axis:
                continue
            leaders_by_science: dict[str, dict[str, Any]] = {}
            for rule in sorted(rules, key=lambda item: (_rule_effective_confidence(item), _rule_score_value(item)), reverse=True):
                science_id = str(rule.get("science_id") or "")
                if science_id and science_id not in leaders_by_science:
                    leaders_by_science[science_id] = rule
            selected = list(leaders_by_science.values())
            if len(selected) < 2:
                top_confidence = max((_rule_effective_confidence(rule) for rule in selected), default=0.0)
                mode = _representation_mode([], top_effective_confidence=top_confidence)
                domain_modes_for_axis.append(mode)
                continue

            best_pair: tuple[dict[str, Any], dict[str, Any], float] | None = None
            for index, first in enumerate(selected):
                for second in selected[index + 1 :]:
                    c_score, is_contradiction = _contradiction_score(first, second, science_registry)
                    if not is_contradiction:
                        continue
                    if best_pair is None or c_score > best_pair[2]:
                        best_pair = (first, second, c_score)

            top_confidence = max(_rule_effective_confidence(rule) for rule in selected)
            if best_pair is None:
                mode = _representation_mode([], top_effective_confidence=top_confidence)
                domain_modes_for_axis.append(mode)
                continue

            first, second, c_score = best_pair
            domain_c_scores.append(c_score)
            confidence_delta = round(
                abs(
                    _rule_effective_confidence(first)
                    - _rule_effective_confidence(second)
                ),
                4,
            )
            mode = _representation_mode(
                [c_score],
                top_effective_confidence=top_confidence,
                same_directional_polarity=_contradiction_components(first, second, science_registry)["polarity_delta"] == 0.0,
                confidence_delta=confidence_delta,
            )
            domain_modes_for_axis.append(mode)
            if mode != "synthesis":
                block = _build_tension_block(
                    first,
                    second,
                    c_score,
                    domain,
                    backbone_science_id=backbone_science_id,
                    science_registry=science_registry,
                    representation_mode=mode,
                )
                domain_tension_blocks[domain].append(block)

        domain_modes[domain] = _dominant_representation_mode(domain_modes_for_axis)

    return {
        "domain_modes": domain_modes,
        "domain_tension_blocks": dict(domain_tension_blocks),
        "tension_blocks": [block for blocks in domain_tension_blocks.values() for block in blocks],
    }


def _extract_lucky_elements(rules: list[dict[str, Any]], chart: dict[str, Any]) -> dict[str, Any]:
    planets = []
    signs = []
    for rule in rules[:5]:
        condition = rule.get("condition") or {}
        planet = normalize_planet_name(condition.get("planet") if isinstance(condition, dict) else None)
        if planet:
            planets.append(planet)
        sign = normalize_sign_name(condition.get("sign") if isinstance(condition, dict) else None)
        if sign:
            signs.append(sign)
    current_dasha = ((chart.get("overview") or {}).get("current_maha_dasha")) or ((chart.get("current_dasha") or {}).get("planet"))
    return {
        "dominant_planets": sorted({planet for planet in planets})[:3],
        "supporting_signs": sorted({sign for sign in signs})[:3],
        "current_dasha": normalize_planet_name(current_dasha),
    }


def _extract_timing_window(chart: dict[str, Any]) -> str:
    overview = chart.get("overview") or {}
    maha = overview.get("current_maha_dasha")
    antar = overview.get("current_antar_dasha")
    if maha and antar:
        return f"Current Maha/Antar window: {maha} / {antar}"
    current = chart.get("current_dasha") or {}
    if current.get("planet"):
        return f"Current dasha emphasis: {current['planet']}"
    return "Timing remains open and should be refined with dasha and transit review."


def _select_bridge_phrases(bridges: list[dict[str, Any]], tension_blocks: list[TensionBlock]) -> dict[str, list[str]]:
    selected: dict[str, list[str]] = defaultdict(list)
    for document in bridges:
        bridge_type = str(document.get("bridge_type") or "")
        phrases = document.get("phrases") or []
        if phrases:
            selected[bridge_type].extend(phrases[:2])
    if tension_blocks and "contrast" not in selected:
        selected["contrast"] = [
            "Your chart carries one dominant rhythm, while another layer introduces a meaningful counter-current.",
        ]
    return dict(selected)


def _build_domain_plan(
    matched_rules: list[dict[str, Any]],
    chart: dict[str, Any],
    context: KnowledgeRequestContext,
    tension_blocks: list[TensionBlock],
    user_context: dict[str, Any],
) -> tuple[list[str], list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for rule in matched_rules:
        categories = rule.get("categories") or []
        mapped = {_category_to_domain(category) for category in categories} or {"Emotional Life"}
        for domain in mapped:
            grouped[domain].append(rule)

    ordered_domains = [domain for domain in DOMAIN_PRIORITY if domain in grouped] + [domain for domain in grouped if domain not in DOMAIN_PRIORITY]
    tension_by_domain: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for block in tension_blocks:
        tension_by_domain[_normalize_domain_name(block.life_domain)].append(block.model_dump(mode="json", by_alias=True, exclude_none=True))
    domain_representation_modes: dict[str, str] = {}
    for domain, blocks in tension_by_domain.items():
        modes = [str(block.get("representation_mode") or "synthesis") for block in blocks]
        domain_representation_modes[domain] = _dominant_representation_mode(modes)

    planner_domains: list[dict[str, Any]] = []
    for domain in ordered_domains:
        domain_rules = sorted(grouped[domain], key=lambda item: item.get("score", 0), reverse=True)
        backbone_rules = [rule for rule in domain_rules if rule.get("science_id") == context.backbone_science_id]
        support_rules = [rule for rule in domain_rules if rule.get("science_id") != context.backbone_science_id]
        top_rules = domain_rules[:6]
        average_confidence = sum(float(rule.get("effective_confidence", 0.0)) for rule in top_rules) / max(1, len(top_rules))
        planner_domains.append(
            {
                "domain": domain,
                "confidence_tier_hint": _confidence_band(average_confidence),
                "timing_window_hint": _extract_timing_window(chart),
                "lucky_elements_hint": _extract_lucky_elements(top_rules, chart),
                "backbone_rules": [_compact_rule_payload(rule) for rule in backbone_rules[:4]],
                "support_rules": [_compact_rule_payload(rule) for rule in support_rules[:3]],
                "representation_mode": domain_representation_modes.get(domain, "synthesis"),
                "tension_blocks": tension_by_domain.get(domain, []),
                "user_context": user_context,
            }
        )
    return ordered_domains, planner_domains


def _compact_rule_payload(rule: dict[str, Any]) -> dict[str, Any]:
    passages = (((rule.get("interpretation") or {}).get("full_text_passages")) or [])
    return {
        "rule_id": rule.get("rule_id"),
        "science_id": rule.get("science_id"),
        "summary": (rule.get("interpretation") or {}).get("summary"),
        "detailed": (rule.get("interpretation") or {}).get("detailed"),
        "score": rule.get("score"),
        "effective_confidence": rule.get("effective_confidence"),
        "claim_axis": rule.get("claim_axis"),
        "claim_scope": rule.get("claim_scope"),
        "claim_polarity": rule.get("claim_polarity"),
        "timing_bias": rule.get("timing_bias"),
        "strength_band": rule.get("strength_band"),
        "categories": rule.get("categories"),
        "passages": passages[:2],
    }


def _extract_text_from_claude_response(response: Any) -> str | None:
    content = getattr(response, "content", None)
    if not content:
        return None
    text_parts: list[str] = []
    for item in content:
        text_value = getattr(item, "text", None)
        if text_value:
            text_parts.append(text_value)
    return "\n".join(text_parts).strip() if text_parts else None


def _parse_json_payload(raw_text: str) -> dict[str, Any] | None:
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        cleaned = cleaned.rsplit("```", 1)[0].strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return None


def _build_narrative_system_prompt(voice_instruction: str, bridge_phrases: dict[str, list[str]]) -> str:
    bridge_json = json.dumps(bridge_phrases, ensure_ascii=True)
    return f"""
You are the Narrative Planner for EverydayHoroscope's Knowledge Engine.

Follow these rules exactly:
- Write only from the supplied rule evidence. Do not introduce unsupported astrological claims.
- Use original prose only. Do not reproduce book-like or copyright-adjacent phrasing.
- Technical astrological vocabulary is allowed.
- The default tonal blend is classical plus modern analytical.
- Keep each body entry as a full prose paragraph, not a bullet fragment.
- Backbone science rules lead each domain section. Supporting sciences may refine or qualify them.
- If tension blocks are present, acknowledge them honestly without making the section collapse into uncertainty.
- Return valid JSON only in the form: {{"narratives": [{{"domain": str, "headline": str, "body": [str, ...], "lucky_elements": dict, "timing_window": str, "confidence_tier": "LOW|MEDIUM|HIGH|VERIFIED"}}]}}

Author voice instruction:
{voice_instruction}

Available bridge phrases:
{bridge_json}
""".strip()


def _build_narrative_user_prompt(
    planner_domains: list[dict[str, Any]],
    matched_rules: list[dict[str, Any]],
    context: KnowledgeRequestContext,
    author_voice_id: str,
) -> str:
    payload = {
        "backbone_science_id": context.backbone_science_id,
        "alpha": _context_score(context.alpha),
        "beta": _context_score(context.beta),
        "gamma": _context_score(context.gamma),
        "author_voice_id": author_voice_id,
        "rule_count": len(matched_rules),
        "domains": planner_domains,
    }
    return json.dumps(payload, ensure_ascii=True)


def _coerce_narratives(payload: dict[str, Any], matched_domains: list[str]) -> list[KnowledgeNarrativeDomain]:
    raw_narratives = payload.get("narratives")
    if not isinstance(raw_narratives, list):
        raise ValueError("Claude response missing 'narratives' list")
    narratives: list[KnowledgeNarrativeDomain] = []
    for item in raw_narratives:
        if not isinstance(item, dict):
            continue
        if "domain" not in item:
            continue
        item.setdefault("headline", item["domain"])
        item.setdefault("body", [])
        item.setdefault("lucky_elements", {})
        item.setdefault("timing_window", "Timing window not specified.")
        item.setdefault("confidence_tier", "MEDIUM")
        item.setdefault("tranche_adjusted", False)
        narratives.append(KnowledgeNarrativeDomain(**item))
    if not narratives and matched_domains:
        raise ValueError("Claude response did not contain valid narrative items")
    return narratives


class KnowledgeIndexStore:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self._snapshot = KnowledgeIndexSnapshot(
            built_at=utc_now(),
            rule_count=0,
            key_to_rule_ids={},
            rules_by_id={},
        )
        self._refresh_task: asyncio.Task[KnowledgeIndexSnapshot] | None = None

    @property
    def snapshot(self) -> KnowledgeIndexSnapshot:
        return self._snapshot

    @property
    def refresh_in_progress(self) -> bool:
        return self._refresh_task is not None and not self._refresh_task.done()

    async def refresh(self) -> KnowledgeIndexSnapshot:
        cursor = self.db[COLLECTION_INTERPRETATION_RULES].find(APPROVED_RULE_FILTER, {"_id": 0})
        raw_rules = await cursor.to_list(length=None)
        key_to_rule_ids: dict[str, set[str]] = defaultdict(set)
        rules_by_id: dict[str, IndexedRule] = {}

        for payload in raw_rules:
            try:
                rule = InterpretationRuleDocument(**payload)
            except Exception as exc:
                logger.warning("Skipping invalid knowledge rule during index refresh: %s", exc)
                continue
            anchor_keys = _condition_anchor_keys(rule.condition.model_dump(mode="python", exclude_none=True))
            indexed = IndexedRule(document=rule, anchor_keys=anchor_keys)
            rules_by_id[rule.rule_id] = indexed
            for key in anchor_keys:
                key_to_rule_ids[key].add(rule.rule_id)

        snapshot = KnowledgeIndexSnapshot(
            built_at=utc_now(),
            rule_count=len(rules_by_id),
            key_to_rule_ids=dict(key_to_rule_ids),
            rules_by_id=rules_by_id,
        )
        self._snapshot = snapshot
        logger.info("Knowledge index refreshed with %d approved active rules", snapshot.rule_count)
        return snapshot

    def schedule_refresh(self) -> asyncio.Task[KnowledgeIndexSnapshot]:
        if self.refresh_in_progress:
            return self._refresh_task  # type: ignore[return-value]
        self._refresh_task = asyncio.create_task(self.refresh())

        def _clear(task: asyncio.Task[KnowledgeIndexSnapshot]) -> None:
            if task.cancelled():
                logger.warning("Knowledge index refresh task cancelled")
            elif task.exception():
                logger.exception("Knowledge index refresh failed", exc_info=task.exception())
            self._refresh_task = None

        self._refresh_task.add_done_callback(_clear)
        return self._refresh_task

    def refresh_status(self) -> dict[str, Any]:
        return {
            "index_refreshed": not self.refresh_in_progress,
            "rule_count": self._snapshot.rule_count,
            "built_at": self._snapshot.built_at.isoformat(),
        }


class KnowledgeEngine:
    def __init__(self, db: AsyncIOMotorDatabase, index_store: KnowledgeIndexStore | None = None):
        self.db = db
        self.index_store = index_store or KnowledgeIndexStore(db)

    async def refresh_index(self) -> KnowledgeIndexSnapshot:
        return await self.index_store.refresh()

    def schedule_index_refresh(self) -> asyncio.Task[KnowledgeIndexSnapshot]:
        return self.index_store.schedule_refresh()

    def index_refresh_status(self) -> dict[str, Any]:
        return self.index_store.refresh_status()

    async def scan_chart(
        self,
        chart: dict[str, Any],
        categories: list[str] | None = None,
        max_rules: int = 50,
        context: dict[str, Any] | KnowledgeRequestContext | None = None,
        dasha_timeline: list[dict[str, Any]] | None = None,
    ) -> list[dict[str, Any]]:
        snapshot = self.index_store.snapshot
        facts = extract_chart_facts(chart)
        request_context = context if isinstance(context, KnowledgeRequestContext) else KnowledgeRequestContext(**(context or {}))
        science_registry = await self._load_science_registry()

        candidate_rule_ids: set[str] = set()
        for key in facts.keys:
            candidate_rule_ids.update(snapshot.key_to_rule_ids.get(key, set()))

        requested_categories = set(categories or [])
        matches: list[dict[str, Any]] = []
        for rule_id in candidate_rule_ids:
            indexed_rule = snapshot.rules_by_id.get(rule_id)
            if indexed_rule is None:
                continue
            rule = indexed_rule.document
            if requested_categories and not requested_categories.intersection(rule.categories):
                continue
            if not _condition_matches(rule.condition.model_dump(mode="python", exclude_none=True), facts):
                continue
            score, effective_confidence, applied_modifiers, contextual_adjustment = _score_rule(rule, facts, request_context)
            payload = rule.model_dump(mode="json", by_alias=True, exclude_none=True)
            payload.update(
                {
                    "score": score,
                    "effective_confidence": effective_confidence,
                    "contextual_adjustment": contextual_adjustment,
                    "period_quality": assign_period_quality(payload, dasha_timeline or []),
                    "backbone_science_id": request_context.backbone_science_id,
                    "applied_modifiers": applied_modifiers,
                    "matched_anchor_keys": sorted(indexed_rule.anchor_keys.intersection(facts.keys)),
                }
            )
            matches.append(payload)

        arbitration = _arbitration_summary(
            matched_rules=matches,
            backbone_science_id=request_context.backbone_science_id,
            science_registry=science_registry,
        )
        for payload in matches:
            domains = _domain_names_for_rule(payload)
            relevant_blocks = [block for block in arbitration["tension_blocks"] if block.get("life_domain") in domains]
            payload["tension_blocks"] = relevant_blocks
            payload["representation_mode"] = _dominant_representation_mode(
                [arbitration["domain_modes"].get(domain, "synthesis") for domain in domains]
            )

        matches.sort(key=lambda item: (item["score"], item.get("priority", 0), item.get("effective_confidence", 0)), reverse=True)
        return matches[: max_rules]

    async def generate_narrative(
        self,
        matched_rules: list[dict[str, Any]],
        chart: dict[str, Any],
        context: dict[str, Any] | KnowledgeRequestContext | None = None,
        user_context: dict[str, Any] | None = None,
        author_voice_id: str | None = None,
        tension_blocks: list[dict[str, Any] | TensionBlock] | None = None,
        model: str | None = None,
    ) -> KnowledgeNarrativeResponse:
        request_context = context if isinstance(context, KnowledgeRequestContext) else KnowledgeRequestContext(**(context or {}))
        science_registry = await self._load_science_registry()
        all_tension_blocks: list[TensionBlock] = []
        for block in request_context.tension_blocks:
            all_tension_blocks.append(block if isinstance(block, TensionBlock) else TensionBlock(**block))
        for block in tension_blocks or []:
            all_tension_blocks.append(block if isinstance(block, TensionBlock) else TensionBlock(**block))

        matched_rules = apply_tranche_filter(matched_rules, user_context or {})
        arbitration = _arbitration_summary(
            matched_rules=matched_rules,
            backbone_science_id=request_context.backbone_science_id,
            science_registry=science_registry,
        )
        for block in arbitration["tension_blocks"]:
            all_tension_blocks.append(block if isinstance(block, TensionBlock) else TensionBlock(**block))
        tranche_adjusted_domains: set[str] = set()
        for _rule in matched_rules:
            if _rule.get("_tranche_adjusted"):
                for _cat in (_rule.get("categories") or []):
                    tranche_adjusted_domains.add(_category_to_domain(_cat))
        matched_domains, planner_domains = _build_domain_plan(
            matched_rules=matched_rules,
            chart=chart,
            context=request_context,
            tension_blocks=all_tension_blocks,
            user_context=user_context or {},
        )
        if not matched_rules:
            return KnowledgeNarrativeResponse(
                rule_count=0,
                matched_domains=matched_domains,
                narratives=[],
                author_voice_id=author_voice_id or DEFAULT_AUTHOR_VOICE,
                model=model or DEFAULT_NARRATIVE_MODEL,
                error=None,
            )
        selected_voice_id = author_voice_id or DEFAULT_AUTHOR_VOICE
        voice_instruction = await self._load_author_voice_instruction(selected_voice_id)
        bridge_phrases = await self._load_bridge_phrases(all_tension_blocks)
        system_prompt = _build_narrative_system_prompt(voice_instruction, bridge_phrases)
        user_prompt = _build_narrative_user_prompt(planner_domains, matched_rules, request_context, selected_voice_id)
        selected_model = model or DEFAULT_NARRATIVE_MODEL

        client = await self._anthropic_client()
        if client is None:
            return KnowledgeNarrativeResponse(
                rule_count=len(matched_rules),
                matched_domains=matched_domains,
                narratives=[],
                author_voice_id=selected_voice_id,
                model=selected_model,
                error="Claude API is unavailable. Check ANTHROPIC_API_KEY and anthropic dependency.",
            )
        try:
            response = await client.messages.create(
                model=selected_model,
                max_tokens=2400,
                temperature=0.35,
                system=system_prompt,
                messages=[{"role": "user", "content": [{"type": "text", "text": user_prompt}]}],
            )
        except Exception as exc:
            logger.error("Knowledge narrative generation failed: %s", exc)
            return KnowledgeNarrativeResponse(
                rule_count=len(matched_rules),
                matched_domains=matched_domains,
                narratives=[],
                author_voice_id=selected_voice_id,
                model=selected_model,
                error=f"Claude API call failed: {exc}",
            )

        response_text = _extract_text_from_claude_response(response)
        if not response_text:
            return KnowledgeNarrativeResponse(
                rule_count=len(matched_rules),
                matched_domains=matched_domains,
                narratives=[],
                author_voice_id=selected_voice_id,
                model=selected_model,
                error="Claude returned an empty response.",
            )

        payload = _parse_json_payload(response_text)
        if payload is None:
            logger.error("Knowledge narrative response was not valid JSON: %.200s", response_text)
            return KnowledgeNarrativeResponse(
                rule_count=len(matched_rules),
                matched_domains=matched_domains,
                narratives=[],
                author_voice_id=selected_voice_id,
                model=selected_model,
                error="Claude returned invalid JSON.",
            )

        try:
            narratives = _coerce_narratives(payload, matched_domains)
        except Exception as exc:
            logger.error("Knowledge narrative coercion failed: %s", exc)
            return KnowledgeNarrativeResponse(
                rule_count=len(matched_rules),
                matched_domains=matched_domains,
                narratives=[],
                author_voice_id=selected_voice_id,
                model=selected_model,
                error=f"Narrative payload validation failed: {exc}",
            )

        if tranche_adjusted_domains:
            narratives = [
                narrative.model_copy(update={"tranche_adjusted": True})
                if narrative.domain in tranche_adjusted_domains
                else narrative
                for narrative in narratives
            ]

        return KnowledgeNarrativeResponse(
            rule_count=len(matched_rules),
            matched_domains=matched_domains,
            narratives=narratives,
            author_voice_id=selected_voice_id,
            model=selected_model,
            error=None,
        )

    async def _load_author_voice_instruction(self, voice_id: str) -> str:
        collection = self.db[COLLECTION_AUTHOR_VOICES]
        document = await collection.find_one({"voice_id": voice_id, "active": True}, {"_id": 0})
        if document and document.get("llm_instruction"):
            return str(document["llm_instruction"])
        if voice_id != DEFAULT_AUTHOR_VOICE:
            default_document = await collection.find_one({"voice_id": DEFAULT_AUTHOR_VOICE, "active": True}, {"_id": 0})
            if default_document and default_document.get("llm_instruction"):
                return str(default_document["llm_instruction"])
        return "Write with a classical Vedic tone blended with modern analytical clarity."

    async def _load_bridge_phrases(self, tension_blocks: list[TensionBlock] | None = None) -> dict[str, list[str]]:
        collection = self.db[COLLECTION_NARRATIVE_BRIDGES]
        documents = await collection.find({"active": True}, {"_id": 0}).to_list(length=50)
        return _select_bridge_phrases(documents, tension_blocks or [])

    async def _load_science_registry(self) -> dict[str, dict[str, Any]]:
        collection = self.db[COLLECTION_SCIENCE_REGISTRY]
        try:
            documents = await collection.find({"active": True}, {"_id": 0}).to_list(length=50)
        except Exception as exc:
            logger.warning("Knowledge engine could not load science_registry, using fallback order: %s", exc)
            return {}
        result: dict[str, dict[str, Any]] = {}
        for document in documents:
            science_id = str(document.get("science_id") or "")
            if science_id:
                result[science_id] = document
        return result

    async def _anthropic_client(self) -> Any | None:
        try:
            from anthropic import AsyncAnthropic  # type: ignore
        except Exception:
            return None
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return None
        return AsyncAnthropic(api_key=api_key)


_default_engine: KnowledgeEngine | None = None


async def configure_default_knowledge_engine(db: AsyncIOMotorDatabase) -> KnowledgeEngine:
    global _default_engine
    if _default_engine is None or _default_engine.db is not db:
        _default_engine = KnowledgeEngine(db)
    await _default_engine.refresh_index()
    return _default_engine


def get_default_knowledge_engine(db: AsyncIOMotorDatabase | None = None) -> KnowledgeEngine:
    global _default_engine
    if _default_engine is None:
        if db is None:
            raise RuntimeError("Knowledge engine is not configured")
        _default_engine = KnowledgeEngine(db)
    return _default_engine


async def scan_chart(
    chart: dict[str, Any],
    categories: list[str] | None = None,
    max_rules: int = 50,
    context: dict[str, Any] | KnowledgeRequestContext | None = None,
    dasha_timeline: list[dict[str, Any]] | None = None,
    db: AsyncIOMotorDatabase | None = None,
) -> list[dict[str, Any]]:
    engine = get_default_knowledge_engine(db)
    return await engine.scan_chart(
        chart=chart,
        categories=categories,
        max_rules=max_rules,
        context=context,
        dasha_timeline=dasha_timeline,
    )
