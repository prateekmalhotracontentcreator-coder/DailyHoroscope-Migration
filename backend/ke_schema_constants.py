from __future__ import annotations

"""Single source of truth for Knowledge Engine schema enumerations."""

VALID_CONDITION_TYPES = [
    "planet_in_house",
    "planet_in_sign",
    "planet_in_nakshatra",
    "planet_aspect",
    "planet_conjunction",
    "planet_dignity",
    "planet_retrograde",
    "house_lord_in_house",
    "yoga",
    "dasha_period",
    "dasha_planet",
    "dasha_of_house_lord",
    "transit",
    "kp_sublord",
    "composite",
    "engine_specification",
    "planet_in_house_and_sign",
    "yoga_combination",
    "transit_position",
    "aspect_rule",
    "neechabhanga_rule",
    "lagna_sign",
    "ashtakavarga_threshold",
]

VALID_SCOPES = [
    "natal",
    "transit",
    "dasha",
    "engine_specification",
    "natal_lagna",
]

LEGACY_CLAIM_SCOPES = [
    "tendency",
    "event_timing",
    "window",
    "trait",
]

VALID_CLAIM_AXES = [
    "general",
    "general_trend",
    "career_growth",
    "career_timing",
    "career_trend",
    "wealth",
    "wealth_trend",
    "financial_security",
    "marriage_timing",
    "relationship_quality",
    "relationships_trend",
    "partnership_stability",
    "children",
    "education_trend",
    "health_vitality",
    "health_trend",
    "spiritual_growth",
    "spirituality_trend",
    "enemies_adversaries",
    "past_lives",
    "travel_pattern",
    "learning_outcome",
    "longevity",
    "longevity_trend",
]

STANDARD_PLANETS = [
    "sun",
    "moon",
    "mars",
    "mercury",
    "jupiter",
    "venus",
    "saturn",
    "rahu",
    "ketu",
]

UPAGRAHA_PLANETS = [
    "mandi",
    "dhuma",
    "vyatipata",
    "paridhi",
    "indra_dhanus",
    "upaketu",
]

ALL_PLANETS = STANDARD_PLANETS + UPAGRAHA_PLANETS

VALID_DASHA_SYSTEMS = ["vimshottari", "kalachakra", "yogini", "jaimini"]
VALID_PLANET_CATEGORIES = ["physical", "upagraha"]
VALID_CANCELLATION_TRIGGERS = [
    "sign_lord_in_kendra",
    "exaltation_lord_in_kendra",
    "sign_lord_aspects_debilitated",
    "mutual_reception",
    "exaltation_lord_aspects_debilitated",
]
VALID_REFERENCE_POINTS = ["lagna", "moon", "either"]
VALID_SIGNS = [
    "aries",
    "taurus",
    "gemini",
    "cancer",
    "leo",
    "virgo",
    "libra",
    "scorpio",
    "sagittarius",
    "capricorn",
    "aquarius",
    "pisces",
]
VALID_ASHTAKAVARGA_SYSTEMS = ["sarvashtakavarga", "bhinnashtakavarga"]
VALID_NULLIFICATION_TYPES = [
    "positive_result_cancelled",
    "result_reversed",
    "result_delayed",
]
VALID_CROSS_TEXT_RELATIONSHIPS = [
    "identical_claim",
    "near_identical",
    "same_principle_different_phrasing",
    "partial_overlap",
]

ENGINE_DEPENDENCY_IDENTIFIERS = [
    "kalachakra_dasa_calculator",
    "ashtakavarga_calculator",
    "upagraha_calculator",
    "longevity_calculator",
]

KALACHAKRA_DASHA_YEARS = {
    "sun": 5,
    "moon": 21,
    "mars": 7,
    "mercury": 9,
    "jupiter": 10,
    "venus": 16,
    "saturn": 4,
}
