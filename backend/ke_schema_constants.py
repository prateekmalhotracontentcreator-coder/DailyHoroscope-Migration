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
    "kp_planet_signification",
    "kp_star_lord",
    "kp_csl",
    "kp_signification_chain",
    "kp_profession_ruler",
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
    "career",
    "career_growth",
    "career_timing",
    "career_trend",
    "health",
    "wealth",
    "wealth_trend",
    "financial_security",
    "marriage",
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
    "timing",
    "death_timing",
    "death_mode",
    "spouse_longevity",
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
    # Agreement relationships (dedup candidates)
    "identical_claim",
    "near_identical",
    "same_principle_different_phrasing",
    "partial_overlap",
    # Contradiction relationships
    "contradicts",           # Same condition, directly opposite outcome polarity
    "partial_contradiction", # Same condition, overlapping but incompatible outcome (e.g. one says wealth, one says loss of wealth under a modifier)
]

# Contradiction type distinguishes where the contradiction was detected
VALID_CONTRADICTION_TYPES = [
    "within_text",   # Two rules in the same source text conflict
    "cross_text",    # Rules from two different source texts conflict
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

# ---------------------------------------------------------------------------
# Longevity (KP Aayu) Bucket Configuration
# Approved by co-founder Prateek Malhotra on 2026-06-02.
# Architecture decision: rules carry LABELS only (e.g. "madhya_aayu").
# Year ranges are resolved from this config at engine runtime -- never
# hardcoded inside individual rule documents.
# ---------------------------------------------------------------------------

# Option B: wider Madhya range, validated against 38 benchmark case studies.
LONGEVITY_AAYU_CONFIG = {
    "balarishta":     {"min": 0,   "max": 8,    "label": "Balarishta",   "description": "Infant mortality / very early death"},
    "alpa_aayu":      {"min": 8,   "max": 33,   "label": "Alpa Aayu",    "description": "Short longevity"},
    "madhya_aayu":    {"min": 33,  "max": 75,   "label": "Madhya Aayu",  "description": "Middle longevity"},
    "purna_aayu":     {"min": 75,  "max": 100,  "label": "Purna Aayu",   "description": "Full longevity"},
    "aparimita_aayu": {"min": 100, "max": None, "label": "Aparimita Aayu","description": "Super-centenarian / unlimited"},
}

# Edge-case zone where the Madhya/Purna boundary is ambiguous.
# Rules whose natural outcome falls in this window must carry
# edge_case_zone: true and edge_case_gates in their result block.
# The engine applies additional gate checks before assigning final bucket.
LONGEVITY_EDGE_CASE_ZONE = {
    "min": 66,
    "max": 75,
    "classical_reference_point": 72,   # Shashtyamsa/Ashtakavarga classical boundary per GAI review
    "gates": [
        "dasha_activity",       # Is a Maraka/Badhaka Dasha active in the 66-75 window?
        "maraka_strength",      # Are Maraka lords strong enough to terminate life?
        "ayushkaraka_strength", # Is Saturn (Ayushkaraka) protective in this period?
    ],
    "default_on_tie": "purna_aayu",  # When gates are inconclusive, assign higher bucket (Purna)
}

# Valid aayu_bucket label values for rule result.aayu_bucket field
VALID_AAYU_BUCKET_LABELS = list(LONGEVITY_AAYU_CONFIG.keys())
