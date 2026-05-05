#!/usr/bin/env python3
"""
ingest_lalkitab_ch29_v1.py

Lal Kitab Ch 29 — Forecasting on the Basis of Bodily Traits (Physiognomy)
BATCH_ID: lalkitab-ch29-v1-20260505
22 rules:
  18 body_trait rules  (one per body part section / logical group)
   3 archetype rules   (ARCH_THIEF, ARCH_SHAMELESS, ARCH_LION)
   1 family_wealth     (generational wealth continuity)

Sources reconciled:
  Lal Kitab_Ch29_JSON_AI Mode_Final.md — primary trait-outcome data
  Lal Kitab_Ch 29_Diagnostic_LM.md    — cross-cutting character & archetype patterns
  Lal Kitab_Ch 29_Queries Answers_AI Mode.md — schema guidance

Key design decisions:
  1. GROUPED RULES (Option A): One rule per body part section. All trait-outcome
     pairs embedded as diagnostic_array in condition.extra_cond. The KE retrieves
     one rule per body region and searches within the array — avoids 98-rule overhead.

  2. SNAKE_CASE TRAIT KEYS: Trait descriptions normalised to snake_case slugs for
     instantaneous KE matching (e.g., "Raised and big" → "raised_and_big").
     Original text preserved in the "label" field for human readability.

  3. CROSS_REF LINKS: Body-part traits that are archetype triggers carry a
     "cross_ref" field pointing to the archetype rule_id so the KE can run
     Archetype Matching in a second pass.

  4. ARCHETYPE ENGINE (3 standalone rules):
     - ARCH_THIEF:    fused eyebrows OR excessively thick neck (logic_gate: OR)
     - ARCH_SHAMELESS: rooster eyes OR large nostrils (logic_gate: OR)
     - ARCH_LION:     fleshy elbows + strong fleshy thighs + fierce eyes
                      (logic_gate: AND_OR_WEIGHTED — weighted scores, sum ≥ 1.0)

  5. GENERATIONAL WEALTH RULE: Black+soft hair is a HIGH PRIORITY flag for
     triple-generational wealth (Father, Native, Son) — separate rule to surface
     the family continuity logic explicitly.

  6. LINE-COUNT FORMULA SEPARATION (per AI structural note):
     - Forehead lines: NON-LINEAR / inverted U-curve
         0 lines = sage/detached; 1 = prosperous; 2 = high position + long life;
         4-5 = poor/struggling. Never collapse with neck logic.
     - Neck lines: STRICTLY LINEAR / positive
         1 = longevity; 2 = intelligence; 3 = affluence; 4 = impatient/worried.
     Both are separate rules (ch29-forehead-temple and ch29-neck-lines).

  7. NO REMEDIES: Ch 29 is pure physiognomy — no planetary conditions, no remedies.
     All rules: remedies = [], checkable = False.

  8. LU NAMING: Descriptive slug references (LU_29.<body_part>) — semantic anchors
     for LLM context and cross-chapter linking.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pymongo import MongoClient

SCIENCE  = "jyotish"
BOOK     = "Lal Kitab"
BATCH_ID = "lalkitab-ch29-v1-20260505"

# ── Body part group data ──────────────────────────────────────────────────────
# Each entry → one rule. diagnostic_array uses snake_case trait slugs + label.

BODY_PART_DATA = [
    {
        "rule_id":    "lalkitab-ch29-head-formation",
        "lu":         "LU_29.head_formation",
        "body_part":  "head_formation",
        "body_region": "head",
        "summary":    "ch29-head-formation",
        "detailed":   "Lal Kitab physiognomy: head shape and size as indicators of life quality and fortune.",
        "diagnostic_array": [
            {"trait": "longer_than_wide",     "label": "Longer than wide",          "outcome": "Enjoys affluence; life of pomp and show"},
            {"trait": "medium_size",           "label": "Medium size",               "outcome": "Rich and wealthy"},
            {"trait": "big_and_wide",          "label": "Big and wide (stands out)", "outcome": "Always lives in trouble"},
        ],
    },
    {
        "rule_id":    "lalkitab-ch29-hair-traits",
        "lu":         "LU_29.hair_traits",
        "body_part":  "hair_on_head",
        "body_region": "head",
        "summary":    "ch29-hair-traits",
        "detailed":   (
            "Lal Kitab physiognomy: hair texture and colour as indicators of wealth, "
            "character, and generational prosperity. Black and soft hair is a HIGH PRIORITY "
            "flag for multi-generational wealth — see ch29-generational-wealth."
        ),
        "formula_note": (
            "BLACK AND SOFT HAIR is a High Priority flag for multi-generational wealth "
            "(Father, Native, Son). Triggers ch29-generational-wealth archetype check."
        ),
        "diagnostic_array": [
            {"trait": "black_and_soft",  "label": "Black and soft",  "outcome": "Wealthy; father and son will also be wealthy",
             "priority": "HIGH", "cross_ref": "ch29-generational-wealth"},
            {"trait": "thin",            "label": "Thin",             "outcome": "Fair-hearted and handsome"},
            {"trait": "dry_and_hard",    "label": "Dry and hard",     "outcome": "Brave and uncaring"},
            {"trait": "dark_coloured",   "label": "Dark-coloured",    "outcome": "Poor and worrisome"},
            {"trait": "golden",          "label": "Golden",           "outcome": "Medium type"},
        ],
    },
    {
        "rule_id":    "lalkitab-ch29-forehead-temple",
        "lu":         "LU_29.forehead_temple",
        "body_part":  "forehead_and_temple",
        "body_region": "head",
        "summary":    "ch29-forehead-temple",
        "detailed":   (
            "Lal Kitab physiognomy: forehead shape, moles, and line-count as indicators of "
            "luck, intelligence, prosperity, and longevity. Line-count follows a NON-LINEAR "
            "inverted U-curve: 0 = sage, 1 = prosperous, 2 = high position/long life, "
            "4-5 = poor/struggling. Do NOT conflate with neck-line logic (which is linear)."
        ),
        "formula_note": (
            "FOREHEAD LINE-COUNT: Inverted U-curve / non-linear. "
            "0 lines = sage-like and detached; 1 line = prosperous; "
            "2 lines = high position and long life (peak); "
            "4-5 lines = poor, life of struggle. "
            "NEVER merge with neck-line formula (neck lines are strictly linear-positive)."
        ),
        "diagnostic_array": [
            {"trait": "raised_forehead",               "label": "Raised forehead",                          "outcome": "Lucky and rich"},
            {"trait": "wide_forehead",                 "label": "Wide forehead",                            "outcome": "Intelligent"},
            {"trait": "small_forehead",                "label": "Small forehead",                           "outcome": "Short-lived and rough behaviour"},
            {"trait": "plain_and_raised_forehead",     "label": "Plain and raised forehead",                "outcome": "Life in grief and trouble"},
            {"trait": "mole_on_forehead",              "label": "Mole on forehead",                         "outcome": "Lucky"},
            {"trait": "single_line_side_to_side",      "label": "Single line stretched side-to-side",       "outcome": "Prosperous",               "line_count": 1},
            {"trait": "two_lines",                     "label": "Two lines on forehead",                    "outcome": "High position and long life","line_count": 2},
            {"trait": "four_or_five_lines",            "label": "Four or five lines on forehead",           "outcome": "Poor; lives life struggling with difficulties", "line_count": "4-5"},
            {"trait": "no_lines",                      "label": "No lines on forehead",                     "outcome": "Sage-like and detached",    "line_count": 0},
        ],
    },
    {
        "rule_id":    "lalkitab-ch29-eyebrows",
        "lu":         "LU_29.eyebrows",
        "body_part":  "eyebrows",
        "body_region": "head",
        "summary":    "ch29-eyebrows",
        "detailed":   (
            "Lal Kitab physiognomy: eyebrow form and texture as indicators of status, "
            "character, and prosperity. Fused eyebrows are a trigger for ARCH_THIEF."
        ),
        "diagnostic_array": [
            {"trait": "beautiful_and_delicate", "label": "Beautiful and delicate",      "outcome": "Financially accomplished"},
            {"trait": "fused_together",          "label": "Fused together",              "outcome": "Thief or dacoit",
             "cross_ref": "lalkitab-ch29-arch-thief"},
            {"trait": "dry_and_hard_hairs",      "label": "Dry and hard hairs",          "outcome": "Dry-natured and strict"},
            {"trait": "wide_and_dense",          "label": "Wide and dense (not fused)",  "outcome": "Like a king and emperor"},
        ],
    },
    {
        "rule_id":    "lalkitab-ch29-eyes",
        "lu":         "LU_29.eyes",
        "body_part":  "eyes",
        "body_region": "head",
        "summary":    "ch29-eyes",
        "detailed":   (
            "Lal Kitab physiognomy: eye shape and colour as indicators of intelligence, "
            "character, courage, and moral standing. Rooster-like eyes → ARCH_SHAMELESS; "
            "fierce lion-like eyes → ARCH_LION."
        ),
        "diagnostic_array": [
            {"trait": "like_chakor",                       "label": "Like chakor (partridge)",        "outcome": "Clever, uncanny, and charlatan"},
            {"trait": "like_cat_blue_or_green",            "label": "Like a cat (blue or green)",     "outcome": "Wicked, bad character, and ungrateful"},
            {"trait": "black_white_bright_red_threads",    "label": "Black and white with bright red threads", "outcome": "Affluence, status, comfort; meets women frequently"},
            {"trait": "fierce_lion_like",                  "label": "Dangerous and fierce (like a lion)", "outcome": "Courageous and brave",
             "cross_ref": "lalkitab-ch29-arch-lion"},
            {"trait": "rooster_like_oblique_glances",      "label": "Like a rooster / oblique glances", "outcome": "Shameless and brazen",
             "cross_ref": "lalkitab-ch29-arch-shameless"},
        ],
    },
    {
        "rule_id":    "lalkitab-ch29-eyelids",
        "lu":         "LU_29.eyelids",
        "body_part":  "eyelids",
        "body_region": "head",
        "summary":    "ch29-eyelids",
        "detailed":   "Lal Kitab physiognomy: eyelid hair density as indicator of lifestyle quality.",
        "diagnostic_array": [
            {"trait": "less_hair",          "label": "Less hair on eyelids",          "outcome": "Life of rejoicing hobbies and pleasure-seeking"},
            {"trait": "hard_or_excess_hair","label": "Hard or excessive hair",         "outcome": "Poor and strict"},
        ],
    },
    {
        "rule_id":    "lalkitab-ch29-nose",
        "lu":         "LU_29.nose",
        "body_part":  "nose",
        "body_region": "head",
        "summary":    "ch29-nose",
        "detailed":   (
            "Lal Kitab physiognomy: nose shape and nostril size as indicators of prosperity, "
            "intelligence, and character. Large nostrils → ARCH_SHAMELESS."
        ),
        "diagnostic_array": [
            {"trait": "raised_and_big",          "label": "Raised and big",                       "outcome": "Prosperous"},
            {"trait": "pointed_parrot_like",      "label": "Beautiful and pointed (parrot-like)",  "outcome": "Intelligent, gentle, seated on high position"},
            {"trait": "small_and_least_raised",   "label": "Small and least raised",               "outcome": "Beneficent and gentle"},
            {"trait": "small_and_thick",          "label": "Small and thick",                      "outcome": "Imprudent, bereft of money, always searching for a job"},
            {"trait": "little_nostrils",          "label": "Little nostrils",                      "outcome": "Intelligent and modest"},
            {"trait": "large_nostrils",           "label": "Large nostrils",                       "outcome": "Shameless and brazen",
             "cross_ref": "lalkitab-ch29-arch-shameless"},
        ],
    },
    {
        "rule_id":    "lalkitab-ch29-ears",
        "lu":         "LU_29.ears",
        "body_part":  "ears",
        "body_region": "head",
        "summary":    "ch29-ears",
        "detailed":   "Lal Kitab physiognomy: ear shape, length, and lobe attachment as indicators of wealth, temperament, and longevity.",
        "diagnostic_array": [
            {"trait": "long_ears",                   "label": "Long ears",                         "outcome": "Wealthy, gentle, and long-living"},
            {"trait": "long_and_thin",               "label": "Long and thin",                     "outcome": "Good thoughts, talks nobly"},
            {"trait": "earlobe_separated_from_back", "label": "Earlobe separated from back of ear","outcome": "Happy"},
            {"trait": "earlobe_slightly_attached",   "label": "Earlobe slightly attached to back", "outcome": "Happy"},
            {"trait": "excess_hair_on_ears",         "label": "Excess of hair on ears",            "outcome": "Miserable and laborious"},
        ],
    },
    {
        "rule_id":    "lalkitab-ch29-face",
        "lu":         "LU_29.face",
        "body_part":  "face",
        "body_region": "head",
        "summary":    "ch29-face",
        "detailed":   (
            "Lal Kitab physiognomy: overall face shape as an indicator of social standing and "
            "prosperity. Animal archetypes: tiger face = respected; mouse face = beggar."
        ),
        "diagnostic_array": [
            {"trait": "like_mouse_narrow_front",  "label": "Like a mouse (narrow front, wide back)", "outcome": "Very poor, beggar or mendicant",
             "archetype": "ARCH_MOUSE"},
            {"trait": "like_deer",                "label": "Like a deer",                           "outcome": "Bad habits"},
            {"trait": "like_tiger",               "label": "Like a tiger",                          "outcome": "Respected",
             "archetype": "ARCH_TIGER"},
            {"trait": "moderate_face",            "label": "Moderate face",                         "outcome": "Lucky; leads life with glory"},
            {"trait": "beautiful_and_full",       "label": "Beautiful and full face",               "outcome": "Gentle and financially prosperous"},
        ],
    },
    {
        "rule_id":    "lalkitab-ch29-tongue-lips-teeth",
        "lu":         "LU_29.tongue_lips_teeth",
        "body_part":  "tongue_lips_teeth",
        "body_region": "mouth",
        "summary":    "ch29-tongue-lips-teeth",
        "detailed":   (
            "Lal Kitab physiognomy: tongue colour, lip colour, and tooth quality as indicators "
            "of prosperity, character, and moral standing. Yellow/dirty teeth → fraudulent character."
        ),
        "diagnostic_array": [
            {"trait": "tongue_red",               "sub_part": "tongue", "label": "Tongue: Red",              "outcome": "Prosperity"},
            {"trait": "tongue_white",             "sub_part": "tongue", "label": "Tongue: White",            "outcome": "Poverty and penury"},
            {"trait": "tongue_black",             "sub_part": "tongue", "label": "Tongue: Black",            "outcome": "Prosperity and illness"},
            {"trait": "lips_bright",              "sub_part": "lips",   "label": "Lips: Bright",             "outcome": "Prosperity"},
            {"trait": "lips_black",               "sub_part": "lips",   "label": "Lips: Black",              "outcome": "Poverty"},
            {"trait": "teeth_delicate",           "sub_part": "teeth",  "label": "Teeth: Delicate",          "outcome": "Prosperity"},
            {"trait": "teeth_yellow_ugly_dirty",  "sub_part": "teeth",  "label": "Teeth: Yellow, ugly, dirty, and uneven", "outcome": "Fraudulent man",
             "character_flag": "FRAUDULENT"},
            {"trait": "teeth_white_pearl_like",   "sub_part": "teeth",  "label": "Teeth: White, bright, pearl-like", "outcome": "Superior person and prosperity"},
        ],
    },
    {
        "rule_id":    "lalkitab-ch29-voice-beard",
        "lu":         "LU_29.voice_beard",
        "body_part":  "voice_and_beard",
        "body_region": "head_neck",
        "summary":    "ch29-voice-beard",
        "detailed":   "Lal Kitab physiognomy: voice quality and beard texture as indicators of character, status, and prosperity.",
        "diagnostic_array": [
            {"trait": "voice_cloud_like_thunder",  "sub_part": "voice", "label": "Voice: Cloud-like thunder",      "outcome": "Fair-hearted man"},
            {"trait": "voice_raised",              "sub_part": "voice", "label": "Voice: Raised",                  "outcome": "Position and respect"},
            {"trait": "voice_metallic_resonance",  "sub_part": "voice", "label": "Voice: Metallic resonance",      "outcome": "Beauty"},
            {"trait": "voice_like_peacock",        "sub_part": "voice", "label": "Voice: Like a peacock",          "outcome": "Prosperity and popularity"},
            {"trait": "beard_dark_and_soft",       "sub_part": "beard", "label": "Beard: Dark and soft",           "outcome": "Rich and famous man"},
            {"trait": "beard_hard",                "sub_part": "beard", "label": "Beard: Hard",                    "outcome": "Cruel and furious"},
        ],
    },
    {
        "rule_id":    "lalkitab-ch29-mouth",
        "lu":         "LU_29.mouth",
        "body_part":  "mouth",
        "body_region": "head",
        "summary":    "ch29-mouth",
        "detailed":   "Lal Kitab physiognomy: mouth width as indicator of wisdom and materialistic orientation.",
        "diagnostic_array": [
            {"trait": "wide_mouthed",    "label": "Wide-mouthed",   "outcome": "Unwise and aggrieved"},
            {"trait": "medium_sized",    "label": "Medium-sized",   "outcome": "Normal standard"},
            {"trait": "narrow_mouthed",  "label": "Narrow-mouthed", "outcome": "Enjoys materialistic pleasure"},
        ],
    },
    {
        "rule_id":    "lalkitab-ch29-chin",
        "lu":         "LU_29.chin",
        "body_part":  "chin",
        "body_region": "head",
        "summary":    "ch29-chin",
        "detailed":   "Lal Kitab physiognomy: chin shape as indicator of intelligence, character, and prosperity.",
        "diagnostic_array": [
            {"trait": "round",         "label": "Round chin",      "outcome": "Intelligent and artistic"},
            {"trait": "long",          "label": "Long chin",       "outcome": "Imperfect person"},
            {"trait": "dimple_in_chin","label": "Dimple in chin",  "outcome": "Victim of bad habits"},
            {"trait": "raised_chin",   "label": "Raised chin",     "outcome": "Prosperous"},
        ],
    },
    {
        "rule_id":    "lalkitab-ch29-neck-formation",
        "lu":         "LU_29.neck_formation",
        "body_part":  "neck_formation",
        "body_region": "neck",
        "summary":    "ch29-neck-formation",
        "detailed":   (
            "Lal Kitab physiognomy: neck shape and thickness as indicators of character and social standing. "
            "Excessively thick neck → ARCH_THIEF. Straight and long neck → unworthy/duffer."
        ),
        "diagnostic_array": [
            {"trait": "long_and_thin",        "label": "Long and thin",         "outcome": "Very attractive"},
            {"trait": "excessively_thick",    "label": "Excessively thick",     "outcome": "Habit of stealing",
             "cross_ref": "lalkitab-ch29-arch-thief"},
            {"trait": "straight_and_long",    "label": "Straight and long",     "outcome": "Unworthy and duffer"},
            {"trait": "long",                 "label": "Long",                  "outcome": "Earns disrepute"},
            {"trait": "medium_sized",         "label": "Medium-sized",          "outcome": "Normal life"},
        ],
    },
    {
        "rule_id":    "lalkitab-ch29-neck-lines",
        "lu":         "LU_29.neck_lines",
        "body_part":  "lines_on_neck",
        "body_region": "neck",
        "summary":    "ch29-neck-lines",
        "detailed":   (
            "Lal Kitab physiognomy: number of lines on the neck as indicators of longevity, "
            "intelligence, and prosperity. Neck lines follow a STRICTLY LINEAR positive pattern "
            "(1-3 lines); 4 lines breaks the trend. "
            "Do NOT conflate with forehead-line logic (forehead is non-linear / inverted U-curve)."
        ),
        "formula_note": (
            "NECK LINE-COUNT: Strictly linear-positive for 1-3 lines. "
            "1 line = longevity; 2 lines = intelligence; 3 lines = affluence. "
            "4 lines reverses trend: always impatient and worried. "
            "NEVER merge with forehead-line formula (forehead lines are non-linear)."
        ),
        "diagnostic_array": [
            {"trait": "one_line",   "label": "1 line on neck",  "line_count": 1, "outcome": "Long life"},
            {"trait": "two_lines",  "label": "2 lines on neck", "line_count": 2, "outcome": "Intelligent"},
            {"trait": "three_lines","label": "3 lines on neck", "line_count": 3, "outcome": "Affluent"},
            {"trait": "four_lines", "label": "4 lines on neck", "line_count": 4, "outcome": "Always impatient and worried"},
        ],
    },
    {
        "rule_id":    "lalkitab-ch29-upper-body",
        "lu":         "LU_29.upper_body",
        "body_part":  "upper_body",
        "body_region": "torso_arms",
        "summary":    "ch29-upper-body",
        "detailed":   "Lal Kitab physiognomy: back width, arm length, and hand symmetry as indicators of wealth, courage, and mental state.",
        "diagnostic_array": [
            {"trait": "back_wide",              "sub_part": "back",  "label": "Back: Wide",                          "outcome": "Wealth and position"},
            {"trait": "back_excessively_long",  "sub_part": "back",  "label": "Back: Excessively long",              "outcome": "Penury and poverty"},
            {"trait": "arms_medium_sized",      "sub_part": "arms",  "label": "Arms: Medium sized",                  "outcome": "Prosperous"},
            {"trait": "arms_long",              "sub_part": "arms",  "label": "Arms: Long",                          "outcome": "Compassionate and intelligent"},
            {"trait": "right_hand_longer",      "sub_part": "hands", "label": "Right hand longer than left",         "outcome": "Courageous",
             "diagnostic_logic": "Right-side dominance → courage (symmetry rule)"},
            {"trait": "left_hand_longer",       "sub_part": "hands", "label": "Left hand longer than right",         "outcome": "Worried and restless",
             "diagnostic_logic": "Left-side dominance → worried/restless mental state"},
        ],
    },
    {
        "rule_id":    "lalkitab-ch29-extremities",
        "lu":         "LU_29.extremities",
        "body_part":  "extremities_and_torso",
        "body_region": "torso_extremities",
        "summary":    "ch29-extremities",
        "detailed":   (
            "Lal Kitab physiognomy: elbow fleshiness, finger symmetry, abdomen size, and navel "
            "depth as indicators of prosperity. Fleshy elbow → ARCH_LION."
        ),
        "diagnostic_array": [
            {"trait": "elbow_fleshy_lion_like",          "sub_part": "elbow",   "label": "Elbow: Fleshy (like a lion)", "outcome": "Prosperity",
             "cross_ref": "lalkitab-ch29-arch-lion"},
            {"trait": "elbow_dry_and_thin",              "sub_part": "elbow",   "label": "Elbow: Dry and thin",         "outcome": "Penury"},
            {"trait": "little_finger_equals_ring_finger","sub_part": "fingers", "label": "Little finger = ring finger length", "outcome": "More respect and honour than father",
             "diagnostic_logic": "Finger symmetry rule: equal little and ring fingers = status exceeds father's"},
            {"trait": "abdomen_large",                   "sub_part": "abdomen", "label": "Abdomen: Large (belly)",      "outcome": "Prosperity and luck"},
            {"trait": "abdomen_large_but_sagging",       "sub_part": "abdomen", "label": "Abdomen: Large but sagging", "outcome": "Poor"},
            {"trait": "navel_deep_and_fleshy",           "sub_part": "navel",   "label": "Navel: Deep and fleshy",     "outcome": "Prosperity"},
        ],
    },
    {
        "rule_id":    "lalkitab-ch29-lower-body",
        "lu":         "LU_29.lower_body",
        "body_part":  "lower_body",
        "body_region": "legs_feet",
        "summary":    "ch29-lower-body",
        "detailed":   (
            "Lal Kitab physiognomy: thigh fleshiness, calf muscle strength, and sole texture "
            "as indicators of prosperity and personal relationships. "
            "Strong and fleshy thighs → ARCH_LION."
        ),
        "diagnostic_array": [
            {"trait": "thighs_fleshy",               "sub_part": "thighs",      "label": "Thighs: Fleshy",                       "outcome": "Prosperous"},
            {"trait": "thighs_thin_and_strong",      "sub_part": "thighs",      "label": "Thighs: Thin and strong (horse-like)",  "outcome": "Rise in income"},
            {"trait": "thighs_strong_and_fleshy",    "sub_part": "thighs",      "label": "Thighs: Strong and fleshy (lion-like)", "outcome": "Financially very prosperous",
             "cross_ref": "lalkitab-ch29-arch-lion"},
            {"trait": "thighs_very_thick_and_sagging","sub_part": "thighs",     "label": "Thighs: Very thick and sagging",        "outcome": "Timid"},
            {"trait": "calf_fleshy",                 "sub_part": "calf_muscle", "label": "Calf: Fleshy",                         "outcome": "More prosperous"},
            {"trait": "calf_strong",                 "sub_part": "calf_muscle", "label": "Calf: Strong",                         "outcome": "Good-looking wife / husband"},
            {"trait": "sole_thick_and_fleshy",       "sub_part": "sole",        "label": "Sole: Thick and fleshy",               "outcome": "Prosperous"},
            {"trait": "sole_thin_and_deep",          "sub_part": "sole",        "label": "Sole: Thin and deep",                  "outcome": "Prosperity and respect"},
        ],
    },
]

# ── Archetype data (3 standalone rules) ──────────────────────────────────────

ARCHETYPE_DATA = [
    {
        "rule_id":     "lalkitab-ch29-arch-thief",
        "lu":          "LU_29.arch_thief",
        "archetype_id":"ARCH_THIEF",
        "label":       "Thief / Dacoit Indicator",
        "summary":     "ch29-arch-thief",
        "detailed":    (
            "Archetype rule: native is diagnosed as a thief or dacoit if either of two "
            "body-part triggers is present. Logic gate is OR — either trigger alone is sufficient. "
            "Trigger 1: eyebrows are fused together (ch29-eyebrows). "
            "Trigger 2: neck is excessively thick (ch29-neck-formation). "
            "Cumulative weight increases if both triggers are present simultaneously."
        ),
        "logic_gate":  "OR",
        "triggers": [
            {"body_part": "eyebrows",       "trait": "fused_together",    "rule_ref": "lalkitab-ch29-eyebrows"},
            {"body_part": "neck_formation", "trait": "excessively_thick", "rule_ref": "lalkitab-ch29-neck-formation"},
        ],
        "result":      "Thief or Dacoit",
        "result_quality": "inauspicious",
    },
    {
        "rule_id":     "lalkitab-ch29-arch-shameless",
        "lu":          "LU_29.arch_shameless",
        "archetype_id":"ARCH_SHAMELESS",
        "label":       "Shameless / Brazen Personality",
        "summary":     "ch29-arch-shameless",
        "detailed":    (
            "Archetype rule: native is diagnosed as shameless and brazen if either of two "
            "body-part triggers is present. Logic gate is OR — either trigger alone is sufficient. "
            "Trigger 1: eyes are rooster-like or have oblique glances (ch29-eyes). "
            "Trigger 2: nostrils are large (ch29-nose). "
            "Cumulative weight increases if both triggers are present simultaneously."
        ),
        "logic_gate":  "OR",
        "triggers": [
            {"body_part": "eyes", "trait": "rooster_like_oblique_glances", "rule_ref": "lalkitab-ch29-eyes"},
            {"body_part": "nose", "trait": "large_nostrils",               "rule_ref": "lalkitab-ch29-nose"},
        ],
        "result":      "Shameless and Brazen",
        "result_quality": "inauspicious",
    },
    {
        "rule_id":     "lalkitab-ch29-arch-lion",
        "lu":          "LU_29.arch_lion",
        "archetype_id":"ARCH_LION",
        "label":       "Lion Archetype — Maximum Financial Prosperity and Courage",
        "summary":     "ch29-arch-lion",
        "detailed":    (
            "Archetype rule: Lion Archetype spans three body parts with weighted scoring. "
            "Logic gate is AND_OR_WEIGHTED — individual triggers contribute a weight of 0.5; "
            "combined score ≥ 1.0 confirms maximum prosperity and courage. "
            "Trigger 1 (weight 0.5): elbows are fleshy lion-like (ch29-extremities). "
            "Trigger 2 (weight 0.5): thighs are strong and fleshy lion-like (ch29-lower-body). "
            "Trigger 3 (weight 0.5): eyes are fierce and lion-like (ch29-eyes). "
            "Any two triggers present = score 1.0 = Lion Archetype confirmed."
        ),
        "logic_gate":  "AND_OR_WEIGHTED",
        "triggers": [
            {"body_part": "extremities",  "trait": "elbow_fleshy_lion_like",     "rule_ref": "lalkitab-ch29-extremities", "weight": 0.5},
            {"body_part": "lower_body",   "trait": "thighs_strong_and_fleshy",   "rule_ref": "lalkitab-ch29-lower-body",  "weight": 0.5},
            {"body_part": "eyes",         "trait": "fierce_lion_like",            "rule_ref": "lalkitab-ch29-eyes",        "weight": 0.5},
        ],
        "score_threshold": 1.0,
        "result":      "Maximum Financial Prosperity and Courage",
        "result_quality": "auspicious",
    },
]


# ── Base document builder ─────────────────────────────────────────────────────

def _base(rule_id: str, logic_unit: str, rule_type: str, sub_type: str,
          summary: str, detailed: str, now: str) -> dict:
    return {
        "rule_id":         rule_id,
        "approval_status": "pending_review",
        "source": {
            "science":    SCIENCE,
            "book":       BOOK,
            "chapter":    29,
            "logic_unit": logic_unit,
            "batch_id":   BATCH_ID,
        },
        "metadata": {
            "rule_type": rule_type,
            "sub_type":  sub_type,
        },
        "interpretation": {
            "summary": summary,
            "detailed": detailed,
            "remedies": [],
        },
        "validation": {
            "checkable":    False,
            "yoga_check":   {"type": "manual", "checkable": False},
            "validated_by": None,
            "validated_at": None,
        },
        "created_at": now,
        "updated_at": now,
    }


# ── Builder: Body trait group rules (18 rules) ───────────────────────────────

def build_body_traits(now: str) -> list[dict]:
    rules = []
    for data in BODY_PART_DATA:
        r = _base(
            rule_id    = data["rule_id"],
            logic_unit = data["lu"],
            rule_type  = "physiognomy",
            sub_type   = "body_trait",
            summary    = data["summary"],
            detailed   = data["detailed"],
            now        = now,
        )
        r["condition"] = {
            "body_part":   data["body_part"],
            "body_region": data["body_region"],
        }
        extra: dict = {
            "diagnostic_array": data["diagnostic_array"],
        }
        if "formula_note" in data:
            extra["formula_note"] = data["formula_note"]
        r["condition"]["extra_cond"] = extra
        rules.append(r)
    return rules


# ── Builder: Archetype rules (3 rules) ───────────────────────────────────────

def build_archetypes(now: str) -> list[dict]:
    rules = []
    for data in ARCHETYPE_DATA:
        r = _base(
            rule_id    = data["rule_id"],
            logic_unit = data["lu"],
            rule_type  = "physiognomy",
            sub_type   = "archetype",
            summary    = data["summary"],
            detailed   = data["detailed"],
            now        = now,
        )
        r["condition"] = {
            "archetype_id": data["archetype_id"],
            "label":        data["label"],
            "logic_gate":   data["logic_gate"],
            "triggers":     data["triggers"],
        }
        if "score_threshold" in data:
            r["condition"]["score_threshold"] = data["score_threshold"]
        r["interpretation"]["result"]         = data["result"]
        r["interpretation"]["result_quality"] = data["result_quality"]
        rules.append(r)
    return rules


# ── Builder: Generational wealth rule (1 rule) ───────────────────────────────

def build_generational_wealth(now: str) -> list[dict]:
    r = _base(
        rule_id    = "lalkitab-ch29-generational-wealth",
        logic_unit = "LU_29.generational_wealth",
        rule_type  = "physiognomy",
        sub_type   = "family_wealth",
        summary    = "ch29-generational-wealth",
        detailed   = (
            "Lal Kitab Family Prosperity Continuity Logic: black and soft hair on the native's "
            "head is a HIGH PRIORITY physiognomy flag for triple-generational wealth. "
            "Diagnosis: Father, Native, and Son will all be wealthy. "
            "This rule surfaces the family continuity dimension of the hair-traits rule "
            "(ch29-hair-traits: black_and_soft trait) as a standalone diagnostic so the KE "
            "can perform multi-generational wealth checks explicitly."
        ),
        now        = now,
    )
    r["condition"] = {
        "body_part":    "hair_on_head",
        "body_region":  "head",
        "trigger_trait": "black_and_soft",
        "rule_ref":      "lalkitab-ch29-hair-traits",
        "priority":      "HIGH",
    }
    r["interpretation"]["outcome"]            = "Triple-generational wealth: Father, Native, and Son are all wealthy"
    r["interpretation"]["generational_scope"] = ["father", "native", "son"]
    return [r]


# ── Aggregate ─────────────────────────────────────────────────────────────────

def build_all(now: str) -> list[dict]:
    rules = []
    rules.extend(build_body_traits(now))
    rules.extend(build_archetypes(now))
    rules.extend(build_generational_wealth(now))
    return rules


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run",  action="store_true")
    parser.add_argument("--save",     help="Path to write JSON")
    parser.add_argument("--upload",   help="Path to JSON for upload")
    parser.add_argument("--mongo-url")
    parser.add_argument("--db-name",  default="horoscope_db")
    args = parser.parse_args()

    now   = datetime.now(timezone.utc).isoformat()
    rules = build_all(now)

    if args.dry_run or args.save:
        by_sub: dict[str, int] = {}
        for r in rules:
            st = r["metadata"]["sub_type"]
            by_sub[st] = by_sub.get(st, 0) + 1

        print(f"Built {len(rules)} rules for batch {BATCH_ID}\n")
        print("Breakdown by sub_type:")
        for st, count in sorted(by_sub.items()):
            print(f"  {st:<30}: {count}")
        print("\nRule IDs:")
        for r in rules:
            print(f"  {r['rule_id']}")

        if args.save:
            with open(args.save, "w") as f:
                json.dump(rules, f, indent=2, default=str)
            print(f"\nSaved → {args.save}")
        print("\nDry run complete.")
        return

    if args.upload:
        if not args.mongo_url:
            raise SystemExit("ERROR: --mongo-url is required with --upload")
        with open(args.upload) as f:
            rules = json.load(f)

        client   = MongoClient(args.mongo_url)
        col      = client[args.db_name]["interpretation_rules"]
        inserted = updated = 0
        for rule in rules:
            result = col.update_one(
                {"rule_id": rule["rule_id"]},
                {"$set":    rule},
                upsert=True,
            )
            if result.upserted_id:
                inserted += 1
            elif result.modified_count:
                updated += 1
        print(f"Loaded {len(rules)} rules from {args.upload}")
        print(f"Inserted {inserted} / Updated {updated} rules → {args.db_name}.interpretation_rules")
        client.close()


if __name__ == "__main__":
    main()
