#!/usr/bin/env python3
"""
ingest_remedies_v1.py — Mantra + Yantra Remedy Library (100 Focus Areas)

100 rules, science_id = "jyotish_remedies_mantras"

Schema design:
  - interpretation.summary     = remedy_area (never truncated)
  - remedy.*                   = full 13-field remedy record (new top-level field)
  - condition.trigger_tags     = standardized KE condition codes for auto-trigger
  - condition.astrological_mapping = structured {planet, house, yoga, dasha, transit}
  - condition.type             = "remedy_trigger" (new type, Phase 2)
  - All rules checkable: False — Remedies Engine trigger logic is Phase 2

Trigger paths (hybrid — per Logic Trigger design doc):
  1. Affliction-based (primary): KE fires remedy when specific weakness detected
  2. User-requested (secondary): browse by remedy_area in Remedy Dashboard
  3. Alongside interpretation (prescription): Doctor's prescription model

Mantra fields split:
  mantra_devanagari:     Sanskrit only  (for on-screen rendering)
  mantra_transliteration: Roman English  (for pronunciation guide / report)

Special note — ID 45 (Love/Attraction — Kamadeva):
  Source file has a truncated mantra string at the section boundary.
  Reconstructed using standard Kamadeva Gayatri with placeholder fields.
  metadata.data_quality = "reconstructed" — verify before production approval.

Source: /Users/apple/Documents/Knowledge Engine_eBooks/
        New Ingest_5 Books/5. Remedies_Mantra + Yantra_Focus Area Wise.md

Standard workflow:
  python3 scripts/ingest_remedies_v1.py --dry-run --save scripts/remedies_rules.json
  python3 scripts/ingest_remedies_v1.py --upload scripts/remedies_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db
  python3 scripts/validate_rules.py --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id remedies-mantras-v1-20260504
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCIENCE_ID = "jyotish_remedies_mantras"
BOOK       = "Mantra + Yantra Remedy Library — 100 Focus Areas"
BOOK_ID    = "remedies_mantra_yantra_v1"
CHAPTER    = None
CHAP_NAME  = "Focus Area Remedies"
BATCH_ID   = "remedies-mantras-v1-20260504"

SOURCE_MD  = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/"
    "New Ingest_5 Books/5. Remedies_Mantra + Yantra_Focus Area Wise.md"
)

# ─────────────────────────────────────────────────────────────────────────────
# TRIGGER METADATA (per remedy ID)
# category       → trigger_category group
# trigger_tags   → standardized KE condition codes for auto-match
# astr_mapping   → {planet, house, yoga, dasha, transit, status}
# ─────────────────────────────────────────────────────────────────────────────
TRIGGER_MAP: dict[int, dict] = {
    # ── IDs 1–9: Primary planet mantras ──────────────────────────────────────
    1:  {"cat": "planetary_weakness",
         "tags": ["sun_debilitated", "sun_combust", "low_shadbala_sun", "sun_6_8_12"],
         "map": {"planet": ["Sun"], "status": ["debilitated", "combust", "low_shadbala"], "house": [1, 10]}},
    2:  {"cat": "planetary_weakness",
         "tags": ["moon_debilitated", "moon_combust", "low_shadbala_moon", "shani_sade_sati"],
         "map": {"planet": ["Moon"], "status": ["debilitated", "combust", "low_shadbala"], "house": [4]}},
    3:  {"cat": "planetary_weakness",
         "tags": ["mars_debilitated", "mars_combust", "low_shadbala_mars", "mangal_dosha"],
         "map": {"planet": ["Mars"], "status": ["debilitated", "combust", "low_shadbala"]}},
    4:  {"cat": "planetary_weakness",
         "tags": ["mercury_debilitated", "mercury_combust", "low_shadbala_mercury"],
         "map": {"planet": ["Mercury"], "status": ["debilitated", "combust", "low_shadbala"]}},
    5:  {"cat": "planetary_weakness",
         "tags": ["jupiter_debilitated", "jupiter_combust", "low_shadbala_jupiter"],
         "map": {"planet": ["Jupiter"], "status": ["debilitated", "combust", "low_shadbala"]}},
    6:  {"cat": "planetary_weakness",
         "tags": ["venus_debilitated", "venus_combust", "low_shadbala_venus"],
         "map": {"planet": ["Venus"], "status": ["debilitated", "combust", "low_shadbala"]}},
    7:  {"cat": "planetary_weakness",
         "tags": ["saturn_debilitated", "saturn_combust", "low_shadbala_saturn",
                  "shani_sade_sati", "shani_dhaiya"],
         "map": {"planet": ["Saturn"], "status": ["debilitated", "combust", "low_shadbala"]}},
    8:  {"cat": "planetary_weakness",
         "tags": ["rahu_6_8_12", "rahu_conjunction_malefic", "kalsarpa_yoga"],
         "map": {"planet": ["Rahu"], "house": [6, 8, 12]}},
    9:  {"cat": "planetary_weakness",
         "tags": ["ketu_6_8_12", "ketu_conjunction_malefic", "kalsarpa_yoga"],
         "map": {"planet": ["Ketu"], "house": [6, 8, 12]}},
    # ── IDs 10–20: Health & body ──────────────────────────────────────────────
    10: {"cat": "house_affliction",
         "tags": ["malefic_6_8_12", "house_affliction_8", "chronic_disease"],
         "map": {"house": [6, 8, 12], "status": ["afflicted"]}},
    11: {"cat": "health_mapping",
         "tags": ["sun_afflicted", "sun_6_8_12", "eye_skin_health"],
         "map": {"planet": ["Sun"], "house": [6, 8, 12]}},
    12: {"cat": "health_mapping",
         "tags": ["moon_afflicted", "moon_6_8_12", "anxiety_fear"],
         "map": {"planet": ["Moon"], "house": [6, 8, 12]}},
    13: {"cat": "house_affliction",
         "tags": ["malefic_8", "house_affliction_8", "fatal_illness_risk"],
         "map": {"house": [8], "status": ["afflicted"]}},
    14: {"cat": "health_mapping",
         "tags": ["mercury_afflicted", "house_affliction_4", "mental_clarity"],
         "map": {"planet": ["Mercury"], "house": [4]}},
    15: {"cat": "planetary_strength",
         "tags": ["low_shadbala_mars", "immunity_weak", "malefic_6_8"],
         "map": {"planet": ["Mars"], "status": ["low_shadbala"]}},
    16: {"cat": "health_mapping",
         "tags": ["mercury_afflicted", "venus_afflicted", "speech_memory"],
         "map": {"planet": ["Mercury", "Venus"], "house": [2]}},
    17: {"cat": "health_mapping",
         "tags": ["mars_afflicted", "sun_afflicted", "digestive_issue"],
         "map": {"planet": ["Mars", "Sun"], "house": [6]}},
    18: {"cat": "planetary_strength",
         "tags": ["sun_afflicted", "low_shadbala_sun", "bone_health"],
         "map": {"planet": ["Sun"], "status": ["debilitated", "low_shadbala"]}},
    19: {"cat": "transit_gochar",
         "tags": ["rahu_ketu_transit", "ketu_transit_6", "neurological_issue"],
         "map": {"planet": ["Ketu", "Rahu"], "transit": ["ketu_transit_6"]}},
    20: {"cat": "health_mapping",
         "tags": ["venus_afflicted", "moon_afflicted", "house_5_afflicted", "fertility"],
         "map": {"planet": ["Venus", "Moon"], "house": [5]}},
    # ── IDs 21–40: Wealth & career ────────────────────────────────────────────
    21: {"cat": "house_affliction",
         "tags": ["venus_afflicted", "jupiter_afflicted", "house_2_afflicted", "wealth_issue"],
         "map": {"planet": ["Venus", "Jupiter"], "house": [2, 11]}},
    22: {"cat": "house_affliction",
         "tags": ["jupiter_afflicted", "house_2_11_afflicted", "business_growth"],
         "map": {"planet": ["Jupiter"], "house": [2, 10, 11]}},
    23: {"cat": "timing_dasha",
         "tags": ["sun_dasha", "saturn_dasha", "career_promotion", "house_10_afflicted"],
         "map": {"planet": ["Sun"], "dasha": ["sun_mahadasha", "saturn_mahadasha"]}},
    24: {"cat": "house_affliction",
         "tags": ["jupiter_afflicted", "house_6_afflicted", "overcoming_loss"],
         "map": {"planet": ["Jupiter"], "house": [6, 8, 12]}},
    25: {"cat": "timing_dasha",
         "tags": ["sun_dasha", "sun_debilitated", "govt_job", "house_10_afflicted"],
         "map": {"planet": ["Sun"], "house": [10], "dasha": ["sun_mahadasha"]}},
    26: {"cat": "house_affliction",
         "tags": ["venus_afflicted", "house_2_afflicted", "income_stability"],
         "map": {"planet": ["Venus"], "house": [2, 11]}},
    27: {"cat": "house_affliction",
         "tags": ["jupiter_afflicted", "house_1_afflicted", "new_ventures"],
         "map": {"planet": ["Jupiter"], "house": [1, 10]}},
    28: {"cat": "house_affliction",
         "tags": ["saturn_afflicted", "rahu_afflicted", "house_6_afflicted", "legal_victory"],
         "map": {"planet": ["Saturn", "Rahu"], "house": [6]}},
    29: {"cat": "timing_dasha",
         "tags": ["mercury_dasha", "rahu_dasha", "stock_market"],
         "map": {"planet": ["Mercury"], "dasha": ["mercury_mahadasha", "rahu_mahadasha"]}},
    30: {"cat": "timing_dasha",
         "tags": ["venus_dasha", "low_shadbala_venus", "luxury_brand"],
         "map": {"planet": ["Venus"], "dasha": ["venus_mahadasha"]}},
    31: {"cat": "house_affliction",
         "tags": ["mars_afflicted", "saturn_afflicted", "house_6_afflicted", "job_search"],
         "map": {"planet": ["Mars", "Saturn"], "house": [6]}},
    32: {"cat": "house_affliction",
         "tags": ["mars_afflicted", "house_4_afflicted", "land_property"],
         "map": {"planet": ["Mars"], "house": [4]}},
    33: {"cat": "timing_dasha",
         "tags": ["rahu_dasha", "rahu_afflicted", "foreign_trade"],
         "map": {"planet": ["Rahu"], "dasha": ["rahu_mahadasha"]}},
    34: {"cat": "house_affliction",
         "tags": ["sun_afflicted", "house_10_afflicted", "leadership_ceo"],
         "map": {"planet": ["Sun"], "house": [10]}},
    35: {"cat": "house_affliction",
         "tags": ["venus_afflicted", "mercury_afflicted", "house_5_afflicted", "creativity_arts"],
         "map": {"planet": ["Venus", "Mercury"], "house": [5]}},
    36: {"cat": "timing_dasha",
         "tags": ["saturn_dasha", "saturn_afflicted", "contract_tenders"],
         "map": {"planet": ["Saturn"], "dasha": ["saturn_mahadasha"]}},
    37: {"cat": "major_dosha",
         "tags": ["pitra_dosha", "house_9_afflicted", "ancestral_wealth"],
         "map": {"yoga": ["pitra_dosha"], "house": [9]}},
    38: {"cat": "house_affliction",
         "tags": ["saturn_afflicted", "mars_afflicted", "house_4_afflicted", "agriculture"],
         "map": {"planet": ["Saturn", "Mars"], "house": [4]}},
    39: {"cat": "house_affliction",
         "tags": ["mercury_afflicted", "rahu_afflicted", "house_3_afflicted", "innovation_tech"],
         "map": {"planet": ["Mercury", "Rahu"], "house": [3, 11]}},
    40: {"cat": "house_affliction",
         "tags": ["malefic_6_8_12", "house_6_8_12_afflicted", "general_abundance"],
         "map": {"house": [6, 8, 12], "status": ["afflicted"]}},
    # ── IDs 41–60: Relationships ──────────────────────────────────────────────
    41: {"cat": "house_affliction",
         "tags": ["venus_afflicted", "house_7_afflicted", "marriage_delay_female"],
         "map": {"planet": ["Venus"], "house": [7]}},
    42: {"cat": "house_affliction",
         "tags": ["mars_afflicted", "house_7_afflicted", "marriage_delay_male"],
         "map": {"planet": ["Mars"], "house": [7]}},
    43: {"cat": "house_affliction",
         "tags": ["venus_afflicted", "house_7_afflicted", "marital_discord"],
         "map": {"planet": ["Venus"], "house": [7]}},
    44: {"cat": "house_affliction",
         "tags": ["mars_afflicted", "saturn_afflicted", "house_7_afflicted", "conflict_resolution"],
         "map": {"planet": ["Mars", "Saturn"], "house": [7]}},
    45: {"cat": "planetary_weakness",           # ID 45 reconstructed
         "tags": ["venus_afflicted", "mars_afflicted", "house_5_afflicted", "love_attraction"],
         "map": {"planet": ["Venus", "Mars"], "house": [5, 7]}},
    46: {"cat": "house_affliction",
         "tags": ["jupiter_afflicted", "house_6_afflicted", "inlaw_relations"],
         "map": {"planet": ["Jupiter"], "house": [6]}},
    47: {"cat": "house_affliction",
         "tags": ["jupiter_afflicted", "moon_afflicted", "house_5_afflicted", "progeny"],
         "map": {"planet": ["Jupiter", "Moon"], "house": [5]}},
    48: {"cat": "house_affliction",
         "tags": ["venus_afflicted", "house_7_afflicted", "separation_risk"],
         "map": {"planet": ["Venus"], "house": [7]}},
    49: {"cat": "house_affliction",
         "tags": ["sun_afflicted", "house_10_afflicted", "social_status"],
         "map": {"planet": ["Sun"], "house": [10]}},
    50: {"cat": "house_affliction",
         "tags": ["venus_afflicted", "moon_afflicted", "house_5_afflicted", "heartbreak"],
         "map": {"planet": ["Venus", "Moon"], "house": [5]}},
    51: {"cat": "house_affliction",
         "tags": ["moon_afflicted", "house_4_afflicted", "domestic_peace"],
         "map": {"planet": ["Moon"], "house": [4]}},
    52: {"cat": "house_affliction",
         "tags": ["mars_afflicted", "house_5_afflicted", "children_protection"],
         "map": {"planet": ["Mars"], "house": [5]}},
    53: {"cat": "house_affliction",
         "tags": ["mercury_afflicted", "house_11_afflicted", "friendship_allies"],
         "map": {"planet": ["Mercury"], "house": [11]}},
    54: {"cat": "house_affliction",
         "tags": ["sun_afflicted", "house_9_afflicted", "paternal_bond"],
         "map": {"planet": ["Sun"], "house": [9]}},
    55: {"cat": "house_affliction",
         "tags": ["moon_afflicted", "house_4_afflicted", "maternal_bond"],
         "map": {"planet": ["Moon"], "house": [4]}},
    56: {"cat": "house_affliction",
         "tags": ["mars_afflicted", "house_3_afflicted", "sibling_harmony"],
         "map": {"planet": ["Mars"], "house": [3]}},
    57: {"cat": "house_affliction",
         "tags": ["saturn_afflicted", "rahu_afflicted", "house_6_afflicted", "slander_protection"],
         "map": {"planet": ["Saturn", "Rahu"], "house": [6]}},
    58: {"cat": "house_affliction",
         "tags": ["mercury_afflicted", "house_2_afflicted", "gaining_trust"],
         "map": {"planet": ["Mercury"], "house": [2]}},
    59: {"cat": "house_affliction",
         "tags": ["jupiter_afflicted", "house_9_afflicted", "finding_mentor"],
         "map": {"planet": ["Jupiter"], "house": [9]}},
    60: {"cat": "major_dosha",
         "tags": ["pitra_dosha", "house_9_afflicted", "ancestor_blessing"],
         "map": {"yoga": ["pitra_dosha"], "house": [9]}},
    # ── IDs 61–80: Education, mind, protection ────────────────────────────────
    61: {"cat": "house_affliction",
         "tags": ["mercury_afflicted", "jupiter_afflicted", "house_4_5_afflicted", "academic_success"],
         "map": {"planet": ["Mercury", "Jupiter"], "house": [4, 5]}},
    62: {"cat": "house_affliction",
         "tags": ["mercury_afflicted", "house_5_afflicted", "concentration"],
         "map": {"planet": ["Mercury"], "house": [5]}},
    63: {"cat": "house_affliction",
         "tags": ["rahu_afflicted", "ketu_afflicted", "evil_eye_nazar"],
         "map": {"planet": ["Rahu", "Ketu"]}},
    64: {"cat": "house_affliction",
         "tags": ["rahu_afflicted", "saturn_afflicted", "house_12_afflicted", "nightmares_fear"],
         "map": {"planet": ["Rahu", "Saturn"], "house": [12]}},
    65: {"cat": "transit_gochar",
         "tags": ["shani_sade_sati", "shani_dhaiya", "mental_peace"],
         "map": {"transit": ["shani_sade_sati", "shani_dhaiya"]}},
    66: {"cat": "planetary_weakness",
         "tags": ["jupiter_afflicted", "rahu_afflicted", "removing_obstacles"],
         "map": {"planet": ["Jupiter", "Rahu"]}},
    67: {"cat": "house_affliction",
         "tags": ["mars_afflicted", "mercury_afflicted", "house_5_afflicted", "competitive_exams"],
         "map": {"planet": ["Mars", "Mercury"], "house": [5]}},
    68: {"cat": "house_affliction",
         "tags": ["saturn_afflicted", "ketu_afflicted", "house_8_12_afflicted", "depression_gloom"],
         "map": {"planet": ["Saturn", "Ketu"], "house": [8, 12]}},
    69: {"cat": "house_affliction",
         "tags": ["mars_afflicted", "rahu_afflicted", "house_4_afflicted", "home_protection"],
         "map": {"planet": ["Mars", "Rahu"], "house": [4]}},
    70: {"cat": "house_affliction",
         "tags": ["mercury_afflicted", "jupiter_afflicted", "house_5_afflicted", "intelligence_iq"],
         "map": {"planet": ["Mercury", "Jupiter"], "house": [5]}},
    71: {"cat": "health_mapping",
         "tags": ["mercury_afflicted", "house_2_afflicted", "speech_stammering"],
         "map": {"planet": ["Mercury"], "house": [2]}},
    72: {"cat": "house_affliction",
         "tags": ["rahu_afflicted", "saturn_afflicted", "black_magic_shield"],
         "map": {"planet": ["Rahu", "Saturn"]}},
    73: {"cat": "house_affliction",
         "tags": ["sun_afflicted", "jupiter_afflicted", "clarity_of_thought"],
         "map": {"planet": ["Sun", "Jupiter"]}},
    74: {"cat": "health_mapping",
         "tags": ["moon_afflicted", "house_12_afflicted", "insomnia_relief"],
         "map": {"planet": ["Moon"], "house": [12]}},
    75: {"cat": "house_affliction",
         "tags": ["ketu_afflicted", "house_12_afflicted", "research_analysis"],
         "map": {"planet": ["Ketu"], "house": [12]}},
    76: {"cat": "house_affliction",
         "tags": ["venus_afflicted", "house_5_afflicted", "artistic_talents"],
         "map": {"planet": ["Venus"], "house": [5]}},
    77: {"cat": "health_mapping",
         "tags": ["mars_afflicted", "rahu_afflicted", "house_6_afflicted", "anger_management"],
         "map": {"planet": ["Mars", "Rahu"], "house": [6]}},
    78: {"cat": "planetary_strength",
         "tags": ["low_shadbala_sun", "sun_afflicted", "self_confidence"],
         "map": {"planet": ["Sun"], "status": ["low_shadbala", "debilitated"]}},
    79: {"cat": "house_affliction",
         "tags": ["malefic_6_8_12", "general_wellbeing"],
         "map": {"house": [6, 8, 12], "status": ["afflicted"]}},
    80: {"cat": "house_affliction",
         "tags": ["jupiter_afflicted", "house_9_12_afflicted", "spiritual_growth"],
         "map": {"planet": ["Jupiter"], "house": [9, 12]}},
    # ── IDs 81–90: Specific doshas ────────────────────────────────────────────
    81: {"cat": "major_dosha",
         "tags": ["kalsarpa_yoga", "rahu_ketu_axis_full"],
         "map": {"yoga": ["kalsarpa_yoga"]}},
    82: {"cat": "major_dosha",
         "tags": ["pitra_dosha", "house_9_afflicted", "sun_afflicted"],
         "map": {"yoga": ["pitra_dosha"], "house": [9]}},
    83: {"cat": "transit_gochar",
         "tags": ["shani_sade_sati", "shani_transit_moon", "shani_transit_8th"],
         "map": {"transit": ["shani_sade_sati"], "planet": ["Saturn"]}},
    84: {"cat": "major_dosha",
         "tags": ["mangal_dosha", "mars_1_4_7_8_12"],
         "map": {"yoga": ["mangal_dosha"], "planet": ["Mars"]}},
    85: {"cat": "major_dosha",
         "tags": ["guru_chandal_yoga", "jupiter_rahu_conjunction"],
         "map": {"yoga": ["guru_chandal_yoga"], "planet": ["Jupiter", "Rahu"]}},
    86: {"cat": "major_dosha",
         "tags": ["grahan_dosha", "eclipse_birth", "rahu_ketu_lagna"],
         "map": {"yoga": ["grahan_dosha"]}},
    87: {"cat": "vastu_imbalance",
         "tags": ["vastu_dosha", "lagna_lord_direction_mismatch"],
         "map": {"yoga": ["vastu_dosha"]}},
    88: {"cat": "house_affliction",
         "tags": ["malefic_8", "house_affliction_8", "accident_sudden_risk"],
         "map": {"house": [8], "planet": ["Mars", "Rahu", "Saturn"]}},
    89: {"cat": "major_dosha",
         "tags": ["gandmool_dosha", "ketu_nakshatra_birth"],
         "map": {"yoga": ["gandmool_dosha"]}},
    90: {"cat": "house_affliction",
         "tags": ["saturn_afflicted", "rahu_afflicted", "house_6_afflicted", "enemy_protection"],
         "map": {"planet": ["Saturn", "Rahu"], "house": [6]}},
    # ── IDs 91–100: Spiritual & metaphysical ─────────────────────────────────
    91: {"cat": "house_affliction",
         "tags": ["jupiter_afflicted", "house_9_12_afflicted", "spiritual_siddhi"],
         "map": {"planet": ["Jupiter"], "house": [9, 12]}},
    92: {"cat": "major_dosha",
         "tags": ["pitra_dosha", "kalsarpa_yoga", "past_karma_wash"],
         "map": {"yoga": ["pitra_dosha", "kalsarpa_yoga"]}},
    93: {"cat": "house_affliction",
         "tags": ["rahu_afflicted", "ketu_afflicted", "aura_cleaning"],
         "map": {"planet": ["Rahu", "Ketu"]}},
    94: {"cat": "health_mapping",
         "tags": ["mercury_afflicted", "house_2_afflicted", "speech_power"],
         "map": {"planet": ["Mercury"], "house": [2]}},
    95: {"cat": "house_affliction",
         "tags": ["rahu_afflicted", "saturn_afflicted", "house_12_afflicted", "unexplained_fear"],
         "map": {"planet": ["Rahu", "Saturn"], "house": [12]}},
    96: {"cat": "house_affliction",
         "tags": ["jupiter_afflicted", "venus_afflicted", "house_2_afflicted", "wealth_stability"],
         "map": {"planet": ["Jupiter", "Venus"], "house": [2, 11]}},
    97: {"cat": "house_affliction",
         "tags": ["jupiter_afflicted", "house_5_9_afflicted", "wisdom_viveka"],
         "map": {"planet": ["Jupiter"], "house": [5, 9]}},
    98: {"cat": "house_affliction",
         "tags": ["saturn_afflicted", "rahu_afflicted", "house_6_afflicted", "legal_tangles"],
         "map": {"planet": ["Saturn", "Rahu"], "house": [6]}},
    99: {"cat": "house_affliction",
         "tags": ["general_affliction", "malefic_6_8_12", "universal_peace"],
         "map": {"house": [6, 8, 12]}},
    100: {"cat": "house_affliction",
          "tags": ["ketu_afflicted", "house_12_afflicted", "self_realization"],
          "map": {"planet": ["Ketu"], "house": [12]}},
}

CATEGORY_LABELS = {
    "planetary_weakness": "Planetary Weakness",
    "planetary_strength": "Planetary Strength (Low Shadbala)",
    "house_affliction":   "House Affliction",
    "major_dosha":        "Major Dosha",
    "timing_dasha":       "Timing — Dasha Period",
    "transit_gochar":     "Transit (Gochar)",
    "vastu_imbalance":    "Vastu Imbalance",
    "health_mapping":     "Health Mapping",
}

# ─────────────────────────────────────────────────────────────────────────────
# ID 45 RECONSTRUCTION (source file has truncated mantra at section boundary)
# ─────────────────────────────────────────────────────────────────────────────
ID45_RECONSTRUCTED = {
    "id": 45,
    "remedy_area": "Love/Attraction",
    "deity": "Kamadeva",
    "severity": "Medium",
    "mantra": (
        "ॐ कामदेवाय विद्महे पुष्पबाणाय धीमहि "
        "तन्नः कन्दर्पः प्रचोदयात् "
        "(Om Kamadevaaya Vidmahey Pushpabanaaya Dhimahi "
        "Tanno Kandarpah Prachodayat)"
    ),
    "yantra": "Kamadeva Yantra",
    "paksha": "Shukla",
    "tithi_day": "Tritiya; Friday",
    "season": "Vasanta (Spring)",
    "frequency": "108 Times",
    "process": "Face East; Offer red flowers and sandalwood paste",
    "attire_color": "Red/Pink",
    "muhurta": "Sunrise",
    "guidance": "Maintain purity of thought; Avoid non-vegetarian food on Fridays.",
    "_reconstructed": True,
}


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE PARSER
# ─────────────────────────────────────────────────────────────────────────────

def _split_mantra(raw: str) -> tuple[str, str]:
    """Split 'ॐ ... नमः (Om ... Namah)' into (devanagari, transliteration)."""
    raw = raw.strip()
    m = re.match(r'^(.+?)\s*\(([^)]+)\)\s*$', raw, re.DOTALL)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return raw, ""


def _load_source() -> list[dict]:
    """Parse the three JSON arrays from the source markdown file.

    The source file has three separate \[...\] array sections at known byte
    positions in the raw text.  We slice each section from the RAW text
    (before escaping replacement) so positions stay stable, then clean and
    parse each slice independently.

    Known \[ positions in raw file: 171, 23162, 46483
    (verified by inspection — see ingest notes)
    """
    with open(SOURCE_MD, 'r', encoding='utf-8', errors='replace') as f:
        raw = f.read()

    # Slice boundaries in the ORIGINAL raw text (before any replacement)
    sections = [
        (171,   23162),   # IDs  1–44
        (23162, 46483),   # IDs 46–90  (ID 45 is at the boundary, truncated)
        (46483, None),    # IDs 91–100
    ]

    all_entries: list[dict] = []
    seen_ids: set[int] = set()

    for start, end in sections:
        seg = raw[start:end] if end else raw[start:]
        # Unescape markdown brackets and underscores on this segment only
        seg = seg.replace('\\[', '[').replace('\\]', ']').replace('\\_', '_')
        # Trim to last complete JSON object, then close the array
        last = seg.rfind('}')
        if last == -1:
            continue
        seg = seg[:last + 1].rstrip() + '\n]'
        # Remove stray control characters (e.g. form-feeds in mantra text)
        seg = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', ' ', seg)
        try:
            data = json.loads(seg)
            for d in data:
                if d['id'] not in seen_ids:
                    all_entries.append(d)
                    seen_ids.add(d['id'])
        except Exception:
            pass  # bad segment — skip silently; missing IDs reported in dry-run

    # Inject reconstructed ID 45 (mantra truncated at section boundary)
    if 45 not in seen_ids:
        all_entries.append(ID45_RECONSTRUCTED)

    all_entries.sort(key=lambda x: x['id'])
    return all_entries


# ─────────────────────────────────────────────────────────────────────────────
# BUILDER
# ─────────────────────────────────────────────────────────────────────────────

def _build_rules() -> list[dict]:
    entries = _load_source()
    now     = datetime.now(timezone.utc).isoformat()
    rules: list[dict] = []

    for entry in entries:
        rid   = entry['id']
        trig  = TRIGGER_MAP.get(rid, {
            "cat": "house_affliction",
            "tags": [],
            "map": {},
        })
        cat        = trig["cat"]
        cat_label  = CATEGORY_LABELS.get(cat, cat.replace("_", " ").title())
        area       = entry.get('remedy_area', '')
        deity      = entry.get('deity', '')
        severity   = entry.get('severity', '')
        yantra     = entry.get('yantra', '')
        paksha     = entry.get('paksha', '')
        tithi_day  = entry.get('tithi_day', '')
        season     = entry.get('season', '')
        frequency  = entry.get('frequency', '')
        process    = entry.get('process', '')
        color      = entry.get('attire_color', entry.get('attire\\_color', ''))
        muhurta    = entry.get('muhurta', '')
        guidance   = entry.get('guidance', '')
        is_recon   = bool(entry.get('_reconstructed'))

        deva, roman = _split_mantra(entry.get('mantra', ''))

        # ── Structured detailed text (not prose — avoids truncation flags) ──
        detailed = (
            f"Remedy: {area} | Deity: {deity} | Severity: {severity}\n\n"
            f"Mantra (Devanagari): {deva}\n"
            f"Mantra (Transliteration): {roman}\n"
            f"Yantra: {yantra}\n\n"
            f"Practice Protocol:\n"
            f"  Paksha: {paksha}\n"
            f"  Timing: {tithi_day} — {muhurta}\n"
            f"  Season: {season}\n"
            f"  Frequency: {frequency}\n"
            f"  Process: {process}\n"
            f"  Attire/Color: {color}\n\n"
            f"Guidance: {guidance}"
        )
        if is_recon:
            detailed += "\n\n[NOTE: ID 45 mantra reconstructed — verify before approval]"

        planets  = trig["map"].get("planet", [])
        houses   = trig["map"].get("house", [])

        rule: dict = {
            "rule_id":    f"remedy-{rid:03d}",
            "science_id": SCIENCE_ID,
            "source": {
                "book":           BOOK,
                "book_id":        BOOK_ID,
                "chapter":        CHAPTER,
                "chapter_name":   CHAP_NAME,
                "sloka":          None,
                "batch_id":       BATCH_ID,
                "primary":        BOOK,
                "page_ref":       None,
                "passage_ref_id": None,
            },
            "condition": {
                "type":              "remedy_trigger",
                "sub_type":          cat,
                "yoga_name":         area,
                "yoga_group":        cat,
                "yoga_group_label":  cat_label,
                "planets_involved":  planets,
                "houses_involved":   houses,
                "yoga_check": {
                    "type":      "remedy_evaluation",
                    "checkable": False,   # Phase 2 — trigger engine not yet built
                },
                "trigger_condition": (
                    f"KE detects {cat_label} pattern; "
                    f"trigger_tags: {', '.join(trig['tags'][:3])}..."
                    if trig['tags'] else "User-requested remedy lookup"
                ),
                "astrological_mapping": trig["map"],
                "trigger_tags":         trig["tags"],
            },
            "interpretation": {
                "summary":  area,    # always remedy_area — never truncated
                "detailed": detailed,
                "full_text_passages": [
                    {"text": detailed, "confidence": "HIGH"}
                ],
                "remedy":           [],
                "timing_indicator": False,
                "strength_modifier": None,
            },
            # ── New top-level field: full remedy record ─────────────────────
            "remedy": {
                "id":                    rid,
                "remedy_area":           area,
                "deity":                 deity,
                "severity":              severity,
                "mantra_devanagari":     deva,
                "mantra_transliteration": roman,
                "yantra":                yantra,
                "paksha":                paksha,
                "tithi_day":             tithi_day,
                "season":                season,
                "frequency":             frequency,
                "process":               process,
                "attire_color":          color,
                "muhurta":               muhurta,
                "guidance":              guidance,
            },
            "metadata": {
                "phase":            2,
                "checkable":        False,
                "yoga_group":       cat,
                "yoga_group_label": cat_label,
                "remedy_category":  ["mantra", "yantra"],
                "source_quality":   "PRIMARY",
                "data_quality":     "reconstructed" if is_recon else "source",
                "tags": ["remedy", "mantra", "yantra", cat, deity.lower()],
                "trigger_category": cat,
            },
            "confidence":      "HIGH",
            "approval_status": "pending_review",
            "validation": {
                "verdict":       "pending",
                "flag_reason":   None,
                "validated_by":  None,
                "validated_at":  None,
            },
            "created_at": now,
            "updated_at": now,
        }
        rules.append(rule)

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest Mantra + Yantra Remedy Library into MongoDB"
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--save",    metavar="FILE")
    parser.add_argument("--upload",  metavar="FILE")
    parser.add_argument("--mongo-url", default="")
    parser.add_argument("--db-name",   default="horoscope_db")
    args = parser.parse_args()

    if not args.dry_run and not args.upload:
        parser.print_help()
        sys.exit(1)

    # ── DRY RUN ──────────────────────────────────────────────────────────────
    if args.dry_run:
        rules = _build_rules()
        from collections import Counter
        cats: Counter = Counter(r["metadata"]["yoga_group"] for r in rules)
        sevs: Counter = Counter(r["remedy"]["severity"]     for r in rules)

        recon = [r for r in rules if r["metadata"]["data_quality"] == "reconstructed"]
        missing = [i for i in range(1, 101)
                   if not any(r["remedy"]["id"] == i for r in rules)]

        print(f"\n{'='*60}")
        print(f"  Remedies Mantra + Yantra — Dry Run")
        print(f"  Total rules built: {len(rules)}")
        print(f"  Batch ID:          {BATCH_ID}")
        print(f"  Science ID:        {SCIENCE_ID}")
        print(f"{'='*60}")
        print("\n  By trigger category:")
        for cat, cnt in sorted(cats.items()):
            print(f"    {cnt:3d}  {cat}")
        print("\n  By severity:")
        for sev, cnt in sorted(sevs.items()):
            print(f"    {cnt:3d}  {sev}")
        if recon:
            print(f"\n  ⚠️  Reconstructed entries: {[r['remedy']['id'] for r in recon]}")
        if missing:
            print(f"\n  ⚠️  Missing IDs: {missing}")
        else:
            print(f"\n  ✅ All 100 IDs present")

        # Spot-check one entry
        sample = next((r for r in rules if r["remedy"]["id"] == 1), rules[0])
        print(f"\n  Sample — remedy-001 ({sample['remedy']['remedy_area']}):")
        print(f"    Deity:            {sample['remedy']['deity']}")
        print(f"    Devanagari:       {sample['remedy']['mantra_devanagari'][:50]}...")
        print(f"    Transliteration:  {sample['remedy']['mantra_transliteration'][:50]}...")
        print(f"    Trigger tags:     {sample['condition']['trigger_tags']}")
        print()

        if args.save:
            out = Path(args.save)
            out.write_text(json.dumps(rules, indent=2, ensure_ascii=False))
            print(f"  ✅ Saved {len(rules)} rules → {out}\n")
        return

    # ── UPLOAD ───────────────────────────────────────────────────────────────
    if args.upload:
        src = Path(args.upload)
        if not src.exists():
            print(f"ERROR: {src} not found — run --dry-run --save first")
            sys.exit(1)
        rules = json.loads(src.read_text())
        try:
            from pymongo import MongoClient, UpdateOne
        except ImportError:
            print("ERROR: pymongo not installed")
            sys.exit(1)
        if not args.mongo_url:
            print("ERROR: --mongo-url required")
            sys.exit(1)
        client = MongoClient(args.mongo_url)
        col    = client[args.db_name]["interpretation_rules"]
        ops    = [
            UpdateOne({"rule_id": r["rule_id"]}, {"$set": r}, upsert=True)
            for r in rules
        ]
        result = col.bulk_write(ops, ordered=False)
        print(f"\n  ✅ Inserted {result.upserted_count} / "
              f"Updated {result.modified_count} rules "
              f"→ {args.db_name}.interpretation_rules")
        client.close()


if __name__ == "__main__":
    main()
