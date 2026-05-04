#!/usr/bin/env python3
"""
ingest_bphs_ch43_v1.py — BPHS Chapter 43: Longevity (Ayurdaya)

38 rules across 7 groups:
  10  pindayu_engine       — Pindayu constants, formulas, and 4 rectifications
   3  ascendant_engine     — Lagna contribution (Rasi/Navamsa), exemption rule
   5  alternative_systems  — Nisargayu, Amsayu, animal spans, calendar conversion
   2  system_selection     — System choice protocol + doubtful averaging
   5  pair_span_logic      — Three pairs, sign-placement, conflict resolution, quantum
   3  class_modifiers      — Degreewise rectification, Saturn/Jupiter class shifts
  10  longevity_yogas      — Seven-fold classification, supernatural spans, Full/Long/Short
                             life yoga groups, strength-placement, weakness-to-help

Source:
  PDF:    BPHS_Vol 1_Longevity_Ch 43.pdf
  Decode: BPHS_Ch43_JSON ready_LM.md (V1 + V4 Master — de-duplicated)
  Ref:    Summary Logic of Ch43 and Ch44.md

Checkable: 10 / 38
  planet_combust (Astangata)
  planetary_combination (Satru Kshetra, Vyayadi, Kroorodaya,
                         Saturn modifier, Jupiter modifier,
                         Amitayu, Divya, Full/Long/Short life yogas)

Standard workflow:
  python3 scripts/ingest_bphs_ch43_v1.py --dry-run --save scripts/bphs_ch43_rules.json
  python3 scripts/ingest_bphs_ch43_v1.py --upload scripts/bphs_ch43_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db
  python3 scripts/validate_rules.py --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id bphs-ch43-v1-20260504
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCIENCE   = "jyotish"
BOOK      = "Brihat Parashara Hora Shastra"
BOOK_ID   = "bphs"
CHAPTER   = 43
CHAP_NAME = "Longevity (Ayurdaya)"
BATCH_ID  = "bphs-ch43-v1-20260504"

YOGA_DATA: list[dict] = [

    # ═══════════════════════════════════════════════════════════════════════════
    # GROUP 1: PINDAYU ENGINE
    # ═══════════════════════════════════════════════════════════════════════════

    {
        "yoga_name":      "Pindayu — Deep Exaltation Longevity Constants",
        "sloka":          "ch43-sloka-04-05",
        "group":          "pindayu_engine",
        "condition_type": "general_principle",
        "formation": (
            "Each of the seven classical planets is allotted a fixed number of years "
            "at its deep exaltation point (Paramochcha). These are the Pindayu constants: "
            "Sun=19, Moon=25, Mars=15, Mercury=12, Jupiter=15, Venus=21, Saturn=20 years. "
            "At deep debilitation, the allotment is halved. Intermediate positions use the "
            "proportional formula (Logic Unit 43.2)."
        ),
        "effect": (
            "The foundation of the Pindayu longevity system. Sum all seven planetary "
            "contributions (after rectifications) plus the Ascendant contribution to "
            "obtain the total Pindayu lifespan."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "blockers":    ["L"],
            "description": "Engine spec — Pindayu system not yet implemented in vedic_calculator.py.",
        },
    },

    {
        "yoga_name":      "Pindayu — Basic Contribution Formula (Distance d)",
        "sloka":          "ch43-sloka-06-07",
        "group":          "pindayu_engine",
        "condition_type": "general_principle",
        "formation": (
            "Compute d = angular distance between the planet's deep exaltation longitude "
            "and its actual natal longitude. "
            "Rule A — if d < 180°: contribution c = f − (d × f / 360), where f = full "
            "exaltation allotment. "
            "Rule B — if d > 180°: c = (d × f) / 360. "
            "Result is in years. Apply rectifications (LU 43.3–43.8) before summing."
        ),
        "effect": (
            "Produces the planet's individual longevity contribution in years. "
            "Planets near exaltation contribute more; near debilitation, less. "
            "The formula is continuous — no binary strong/weak split."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "blockers":    ["L"],
            "description": "Engine spec — Pindayu calculation formula.",
        },
    },

    {
        "yoga_name":      "Astangata Harana — Combustion Longevity Reduction",
        "sloka":          "ch43-sloka-08",
        "group":          "pindayu_engine",
        "condition_type": "planet_combust",
        "formation": (
            "When a classical planet is combust (within Sun's combustion orb), its "
            "Pindayu contribution is reduced by half (×0.5). "
            "Exception: Venus and Saturn are EXEMPT — combustion does not reduce "
            "their longevity contributions. "
            "If a planet attracts both this and another reduction simultaneously, "
            "apply only the highest reduction (see Highest Reduction Priority rule)."
        ),
        "effect": (
            "A combust planet contributes only half its calculated Pindayu years. "
            "For example, if Mercury's calculated contribution is 8 years and it is "
            "combust, only 4 years are counted. Venus and Saturn retain full "
            "contributions despite combustion."
        ),
        "is_benefic":   False,
        "life_domains": ["longevity", "combustion"],
        "yoga_check": {
            "type":        "planet_combust",
            "checkable":   True,
            "excluded_planets": ["Venus", "Saturn"],
            "description": (
                "Check planets[p]['combust'] == True for each planet except "
                "Venus and Saturn. Fire when any non-exempt planet is combust."
            ),
        },
    },

    {
        "yoga_name":      "Satru Kshetra Harana — Inimical Sign Longevity Reduction",
        "sloka":          "ch43-sloka-09",
        "group":          "pindayu_engine",
        "condition_type": "planetary_combination",
        "formation": (
            "When a planet occupies an enemy sign (Satru Kshetra — where dignity = 'enemy'), "
            "its Pindayu contribution is reduced by one-third (×0.667). "
            "Exception: a planet in retrograde motion (Vakrachara) is EXEMPT — retrograde "
            "planets are not penalised even if in enemy sign. "
            "Use Highest Reduction Priority if multiple reductions apply."
        ),
        "effect": (
            "A planet in enemy sign loses one-third of its calculated Pindayu years. "
            "Retrograde planets are protected from this reduction regardless of sign "
            "placement, reflecting their increased Cheshta Bala."
        ),
        "is_benefic":   False,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Check planets[p]['dignity'] == 'enemy' AND planets[p]['retrograde'] == False. "
                "Fire when any planet is in enemy sign and direct."
            ),
        },
    },

    {
        "yoga_name":      "Vyayadi Harana — Visible-Half Harmonic Reduction",
        "sloka":          "ch43-sloka-10-11",
        "group":          "pindayu_engine",
        "condition_type": "planetary_combination",
        "formation": (
            "Planets in houses 7 through 12 (the visible half) suffer a progressive "
            "harmonic reduction using the formula: loss = c / ((14 − house) − (DP / BL)), "
            "where DP = degrees from bhava cusp, BL = bhava span. "
            "Simplified scale: H12=Full, H11=1/2, H10=1/3, H9=1/4, H8=1/5, H7=1/6. "
            "For benefics (Jupiter, Venus, Mercury, Moon, Waning Moon treated as benefic): "
            "apply only HALF of the above reduction scale. "
            "Only the STRONGEST planet in a house suffers the reduction; others are exempt "
            "(Strongest Planet Over-rule — LU 43.6). "
            "Highest Reduction Priority applies if multiple rectifications conflict."
        ),
        "effect": (
            "Planets above the horizon (houses 7–12) lose longevity contribution proportional "
            "to their distance from the 12th house cusp. The 12th house planet loses the most; "
            "the 7th house planet loses the least (1/6). Benefics lose half as much as malefics."
        ),
        "is_benefic":   False,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "houses":      [7, 8, 9, 10, 11, 12],
            "description": (
                "Check planets[p]['house'] in [7,8,9,10,11,12]. "
                "Fire when any planet is in the visible half. "
                "Benefic/malefic status and Shadbala comparison for strongest-planet "
                "override are Phase 2 refinements."
            ),
        },
    },

    {
        "yoga_name":      "Vyayadi Strongest Planet Override",
        "sloka":          "ch43-sloka-11",
        "group":          "pindayu_engine",
        "condition_type": "planetary_combination",
        "formation": (
            "When multiple planets occupy the same house in the visible half (houses 7–12), "
            "ONLY the planet with the highest Shadbala in that house suffers the Vyayadi "
            "reduction. The contributions of all other co-occupants in that house are "
            "exempt from Vyayadi Harana on that account."
        ),
        "effect": (
            "Protects weaker planets in crowded houses from double-penalisation. "
            "Only the strongest planet bears the full weight of visible-half reduction "
            "for its house group."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   False,
            "blockers":    ["KE"],
            "description": (
                "Requires Shadbala comparison between co-occupants of the same house. "
                "Phase 2 after 'planet_shadbala_strong' condition type is wired."
            ),
        },
    },

    {
        "yoga_name":      "Benefic Planetary Class — Always Treated as Benefics",
        "sloka":          "ch43-sloka-11",
        "group":          "pindayu_engine",
        "condition_type": "general_principle",
        "formation": (
            "For all Pindayu longevity calculations and Vyayadi reductions, the Moon "
            "and Mercury are always treated as natural benefics regardless of their "
            "conjunctions. A Waning Moon is specifically classified as a benefic for "
            "these purposes. This means: (a) they lose only half of the malefic Vyayadi "
            "scale, and (b) neither Moon nor Mercury is ever liable for Kroorodaya Harana "
            "(the malefic-ascendant reduction)."
        ),
        "effect": (
            "Moon and Mercury receive preferential treatment in longevity calculations — "
            "their contributions are better protected from reduction than those of the "
            "classical malefics (Sun, Mars, Saturn)."
        ),
        "is_benefic":   True,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "description": "Classification rule for Pindayu engine. Engine spec reference.",
        },
    },

    {
        "yoga_name":      "Kroorodaya Harana — Malefic Ascendant Reduction",
        "sloka":          "ch43-sloka-12-13",
        "group":          "pindayu_engine",
        "condition_type": "planetary_combination",
        "formation": (
            "When a natural malefic (Sun, Mars, or Saturn) occupies the Ascendant, "
            "its Pindayu contribution is reduced by: "
            "(Ascendant cusp in arc-minutes × malefic's basic years) / 21600. "
            "Modifier: if a benefic aspects the malefic in the Ascendant, reduce only "
            "HALF of the calculated figure. "
            "Exception: Mercury is totally exempt from Kroorodaya even when joined with "
            "a natural malefic. Moon and Mercury never attract this reduction."
        ),
        "effect": (
            "A malefic planet in the Ascendant has its longevity contribution progressively "
            "reduced based on the exact cusp degree. The later the Ascendant degree, the "
            "larger the reduction. Benefic aspect partially shields the malefic."
        ),
        "is_benefic":   False,
        "life_domains": ["longevity", "ascendant"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "planets":     ["Sun", "Mars", "Saturn"],
            "houses":      [1],
            "description": (
                "Check planets[p]['house'] == 1 AND planet in ['Sun','Mars','Saturn']. "
                "Fire when a natural malefic is in the Ascendant. "
                "Exact cusp-degree formula is Phase 2."
            ),
        },
    },

    {
        "yoga_name":      "Highest Reduction Priority — One Reduction Per Planet",
        "sloka":          "ch43-sloka-14",
        "group":          "pindayu_engine",
        "condition_type": "general_principle",
        "formation": (
            "If a single planet attracts more than one type of Pindayu rectification "
            "(e.g., both Astangata combustion reduction AND Satru Kshetra enemy-sign "
            "reduction), ONLY the highest single reduction figure is applied. "
            "All other lesser reductions for that planet are ignored entirely. "
            "This prevents compounded reductions from eliminating a planet's "
            "contribution below a reasonable floor."
        ),
        "effect": (
            "Conflict-resolution rule for the rectification layer. When multiple "
            "penalties apply to one planet, the engine picks the maximum penalty only. "
            "This sets an upper bound on how severely any single planet can be reduced."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "description": "Engine logic rule. Reference only.",
        },
    },

    {
        "yoga_name":      "Calendar Conversion — Savanamana to Sauramana",
        "sloka":          "ch43-sloka-15",
        "group":          "pindayu_engine",
        "condition_type": "general_principle",
        "formation": (
            "The Pindayu calculation uses a 360-day zodiacal year (Savanamana) because "
            "it operates over 360° of the zodiac. The final longevity total must be "
            "converted to the solar (Sauramana / Gregorian) calendar by multiplying "
            "the Savanamana total by the constant 0.9856034. "
            "This is always the final step — applied after all rectifications."
        ),
        "effect": (
            "Converts the zodiacal longevity total to a real-world calendar year figure. "
            "For example, 120 Savanamana years = 120 × 0.9856034 ≈ 118.3 Gregorian years."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "description": "Engine spec — final conversion step for Pindayu.",
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # GROUP 2: ASCENDANT ENGINE
    # ═══════════════════════════════════════════════════════════════════════════

    {
        "yoga_name":      "Ascendant Contribution — Rasi Method (Lagnavayu)",
        "sloka":          "ch43-sloka-16-17",
        "group":          "ascendant_engine",
        "condition_type": "general_principle",
        "formation": (
            "Used when the Rasi Ascendant Lord is stronger in Shadbala than the "
            "Navamsa Ascendant Lord. "
            "Calculation A (Signs): Count completed signs from Aries up to (but not "
            "including) the Ascendant sign — each completed sign = 1 year. "
            "Calculation B (Degrees): Convert degrees gained within the current "
            "Ascendant sign to years — 30° = 1 year, 2.5° = 1 month. "
            "Sum A + B = Rasi Lagnavayu contribution."
        ),
        "effect": (
            "The Ascendant itself contributes longevity years based on how far "
            "Aries-to-Ascendant has advanced through the zodiac. A Sagittarius "
            "Ascendant at 0° contributes 8 years from sign count (8 completed signs) "
            "plus proportionate degrees."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity", "ascendant"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "blockers":    ["KE"],
            "description": "Requires Shadbala comparison of Rasi vs Navamsa ASC lord. Phase 2.",
        },
    },

    {
        "yoga_name":      "Ascendant Contribution — Navamsa Method (Lagnavayu)",
        "sloka":          "ch43-sloka-18-19",
        "group":          "ascendant_engine",
        "condition_type": "general_principle",
        "formation": (
            "Used when the Navamsa Ascendant Lord is stronger in Shadbala than the "
            "Rasi Ascendant Lord. "
            "Calculation: Count completed Navamsas from the start of Aries up to "
            "the Navamsa Lagna. Each completed Navamsa (3° 20' arc) = 1 full year. "
            "Proportionately convert remaining minutes of arc within the current "
            "Navamsa using the 3°20' = 1 year ratio."
        ),
        "effect": (
            "The high-density Navamsa conversion makes each small arc unit (3°20') "
            "equal to one full year — more granular than the Rasi method. "
            "Provides an alternative longevity anchor when the Navamsa Ascendant "
            "lord is the dominant factor."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity", "ascendant"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "blockers":    ["KE", "V"],
            "description": "Requires Shadbala comparison and Navamsa Lagna position. Phase 2.",
        },
    },

    {
        "yoga_name":      "Ascendant Exemption — No Rectification Applies to Lagnavayu",
        "sloka":          "ch43-sloka-20",
        "group":          "ascendant_engine",
        "condition_type": "general_principle",
        "formation": (
            "Unlike the contributions of the seven planets, the Ascendant's longevity "
            "contribution (Lagnavayu) is FIXED once calculated. It undergoes NO "
            "rectification checks — it is not reduced for combustion, enemy sign "
            "placement, visible-half position, or malefic-ascendant penalties. "
            "Lagnavayu acts as the stable anchor of the Pindayu total."
        ),
        "effect": (
            "The Ascendant contribution is immune to all four Harana (rectification) "
            "rules. Once computed, it is added to the planetary sum without reduction. "
            "This provides a floor of stability in the longevity calculation."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity", "ascendant"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "description": "Engine rule — Ascendant exemption from rectification.",
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # GROUP 3: ALTERNATIVE SYSTEMS
    # ═══════════════════════════════════════════════════════════════════════════

    {
        "yoga_name":      "Nisargayu — Natural Longevity System Constants",
        "sloka":          "ch43-sloka-22-23",
        "group":          "alternative_systems",
        "condition_type": "general_principle",
        "formation": (
            "The Nisargayu system uses fixed natural-year allotments per planet: "
            "Moon=1, Mars=2, Mercury=9, Venus=20, Jupiter=18, Sun=20, Saturn=50 years. "
            "Used when the Moon is the strongest of Sun/Moon/Ascendant in Shadbala. "
            "Sum all seven allotments for the base total, then apply same rectifications "
            "(Astangata, Satru Kshetra, Vyayadi, Kroorodaya) as in Pindayu."
        ),
        "effect": (
            "Saturn dominates in Nisargayu (50 years) and Moon contributes least (1 year). "
            "This system tends to produce shorter calculated spans than Pindayu for "
            "charts where Sun/Jupiter are well-placed."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "blockers":    ["L"],
            "description": "Engine spec — Nisargayu system not yet implemented.",
        },
    },

    {
        "yoga_name":      "Amsayu — Divisional Longevity System (Treble/Double Rule)",
        "sloka":          "ch43-sloka-24-25",
        "group":          "alternative_systems",
        "condition_type": "general_principle",
        "formation": (
            "Used when the Ascendant is the strongest of Sun/Moon/Ascendant. "
            "Amsayu multipliers apply to each planet's Navamsa position: "
            "Treble (×3): planet in exaltation or own sign in Navamsa. "
            "Double (×2): planet in own Navamsa decanate. "
            "Override: if BOTH treble and double conditions apply simultaneously, "
            "use TREBLE only — do not compound. "
            "Sum all seven multiplied contributions for the Amsayu total."
        ),
        "effect": (
            "Strongly rewards exalted or own-sign Navamsa placements. A planet "
            "in exaltation in the Navamsa triples its Pindayu base contribution. "
            "Produces the longest calculated spans when many planets are well-placed "
            "in divisional charts."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "blockers":    ["L", "V"],
            "description": "Engine spec — requires Navamsa position per planet. Phase 2.",
        },
    },

    {
        "yoga_name":      "Animal Longevity Formula",
        "sloka":          "ch43-sloka-26",
        "group":          "alternative_systems",
        "condition_type": "general_principle",
        "formation": (
            "To calculate the longevity of a non-human being: "
            "Formula: (Human_Calculation × Animal_Full_Span) / 120. "
            "Where Human_Calculation = the Pindayu/Nisargayu/Amsayu result as if "
            "the animal were human, and Animal_Full_Span = the maximum natural "
            "lifespan for that species from the full span catalog."
        ),
        "effect": (
            "Scales the human longevity calculation proportionally to the natural "
            "lifespan of the species. Allows the same Pindayu engine to generate "
            "species-appropriate longevity figures."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "description": "Engine spec — animal longevity formula.",
        },
    },

    {
        "yoga_name":      "Full Lifespan Catalog — Beings and Their Natural Spans",
        "sloka":          "ch43-sloka-27-29",
        "group":          "alternative_systems",
        "condition_type": "general_principle",
        "formation": (
            "Maximum natural lifespan by being type: Gods/Sages=Endless, "
            "Eagles/Owls/Parrots/Crows/Snakes=1000, Falcons/Monkeys/Bears/Frogs=300, "
            "Demons=150, Humans=120, Horses=32, Donkeys/Camels=25, Oxen/Buffaloes=24, "
            "Peacocks=20, Goats/Rams=16, Swans=14, Dogs=12, Hens=8, Birds=7 years."
        ),
        "effect": (
            "Reference table used in the animal longevity formula. Establishes the "
            "maximum span denominator for each species. Humans have a maximum of "
            "120 years — this is the baseline for Full Life (Poorna Ayu)."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "description": "Reference table — not a KE evaluator rule.",
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # GROUP 4: SYSTEM SELECTION
    # ═══════════════════════════════════════════════════════════════════════════

    {
        "yoga_name":      "Longevity System Selection — Strongest Pivot (Sun/Moon/Ascendant)",
        "sloka":          "ch43-sloka-30-32",
        "group":          "system_selection",
        "condition_type": "general_principle",
        "formation": (
            "A Shadbala comparison of Sun, Moon, and Ascendant Lord determines which "
            "longevity system to use: "
            "If Ascendant Lord is strongest → use Amsayu. "
            "If Sun is strongest → use Pindayu. "
            "If Moon is strongest → use Nisargayu. "
            "This comparison is non-negotiable — calculating longevity without "
            "identifying the dominant pivot is logically invalid per BPHS."
        ),
        "effect": (
            "The system selection gate determines the entire longevity calculation "
            "path. Charts with a strong Sun will use Pindayu (the most commonly "
            "referenced system); strong Moon charts use Nisargayu; strong Ascendant "
            "charts use Amsayu."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "blockers":    ["KE"],
            "description": "Requires three-way Shadbala comparison. Phase 2.",
        },
    },

    {
        "yoga_name":      "Doubtful Case Averaging — Equal Strength Resolution",
        "sloka":          "ch43-sloka-32",
        "group":          "system_selection",
        "condition_type": "general_principle",
        "formation": (
            "When two of the three pivots (Sun, Moon, Ascendant) have equal Shadbala: "
            "calculate longevity using both applicable systems and take the average "
            "of the two results. "
            "When all three have equal Shadbala: calculate all three systems and "
            "take the average of all three results. "
            "This prevents bias toward any single calculation path."
        ),
        "effect": (
            "Produces a balanced longevity estimate when no single pivot clearly "
            "dominates. The averaging approach captures contributions from multiple "
            "calculation perspectives."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "blockers":    ["KE"],
            "description": "Requires Shadbala equality detection across three pivots. Phase 2.",
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # GROUP 5: PAIR SPAN LOGIC
    # ═══════════════════════════════════════════════════════════════════════════

    {
        "yoga_name":      "Three Diagnostic Pairs for Lifespan Class",
        "sloka":          "ch43-sloka-33-34",
        "group":          "pair_span_logic",
        "condition_type": "general_principle",
        "formation": (
            "Three planetary pairs are used to diagnose the class of longevity "
            "(Long / Medium / Short): "
            "Pair 1: Lord of Ascendant + Lord of 8th House. "
            "Pair 2: Saturn + Moon. "
            "Pair 3: Natal Ascendant + Hora Ascendant (Hora Lagna). "
            "Each pair is evaluated independently for sign-placement category "
            "(see Sign-Placement Longevity rule). A consensus of two out of three "
            "pairs establishes the baseline class."
        ),
        "effect": (
            "The three-pair system provides a redundant diagnostic with built-in "
            "conflict resolution. When all three agree, the lifespan class is certain; "
            "when they diverge, the conflict resolution hierarchy (LU 43.34) applies."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "blockers":    ["L", "KE"],
            "description": "Requires lord identification + Hora Lagna. Phase 2.",
        },
    },

    {
        "yoga_name":      "Sign-Placement Longevity — Movable/Fixed/Dual Classification",
        "sloka":          "ch43-sloka-35-37",
        "group":          "pair_span_logic",
        "condition_type": "general_principle",
        "formation": (
            "For each of the three diagnostic pairs, classify the longevity span "
            "based on the modality of the signs occupied by both members of the pair: "
            "Long Life: both in Movable signs (Aries/Cancer/Libra/Capricorn) "
            "OR one in Fixed + one in Dual. "
            "Medium Life: both in Dual signs (Gemini/Virgo/Sagittarius/Pisces) "
            "OR one in Movable + one in Fixed. "
            "Short Life: both in Fixed signs (Taurus/Leo/Scorpio/Aquarius) "
            "OR one in Movable + one in Dual."
        ),
        "effect": (
            "Movable-sign dominance indicates a mobile, adaptive life energy and "
            "tends toward longer spans. Fixed-sign dominance indicates rigidity and "
            "tends toward shorter spans. Dual signs indicate medium spans."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "blockers":    ["L"],
            "description": "Requires lord identification for Pairs 1 and 2. Phase 2.",
        },
    },

    {
        "yoga_name":      "Conflict Resolution — Pair 3 Prevails, Moon Override",
        "sloka":          "ch43-sloka-38-40",
        "group":          "pair_span_logic",
        "condition_type": "general_principle",
        "formation": (
            "When the three diagnostic pairs indicate different spans (e.g., Long, "
            "Medium, Short — all different): "
            "Primary rule: the indication of Pair 3 (Natal Ascendant + Hora Ascendant) "
            "prevails as the baseline span. "
            "Moon Override (Exception): if the Moon occupies the Ascendant (H1) or "
            "the 7th house, the indication of Pair 2 (Saturn + Moon) VETOES the "
            "above and becomes the master diagnostic, regardless of Pair 3."
        ),
        "effect": (
            "Establishes a clear hierarchy when all three pairs disagree. Pair 3 is "
            "the default arbiter; but the Moon's position in H1 or H7 triggers an "
            "override that gives Pair 2 (Saturn-Moon axis) the final word."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "blockers":    ["L", "KE"],
            "description": "Requires all three pair evaluations. Phase 2.",
        },
    },

    {
        "yoga_name":      "Quantum of Years — Harmonic Scale per Lifespan Class",
        "sloka":          "ch43-sloka-41-44",
        "group":          "pair_span_logic",
        "condition_type": "general_principle",
        "formation": (
            "The number of pairs indicating a given class determines the exact quantum: "
            "Long Life: 3 pairs = 120 years, 2 pairs = 108 years, 1 pair = 96 years. "
            "Medium Life: 3 pairs = 80 years, 2 pairs = 72 years, 1 pair = 64 years. "
            "Short Life: 3 pairs = 32 years, 2 pairs = 36 years, 1 pair = 40 years. "
            "Note: Short Life increases with fewer pairs (32→36→40) — a counter-intuitive "
            "harmonic that reflects stronger confidence in a short span when all three "
            "pairs agree."
        ),
        "effect": (
            "Produces the specific longevity quantum in years. Strong consensus among "
            "all three pairs (120, 80, or 32 years) gives maximum/minimum values. "
            "Mixed signals produce intermediate quanta."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "blockers":    ["L", "KE"],
            "description": "Requires all three pair evaluations and counts. Phase 2.",
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # GROUP 6: CLASS MODIFIERS
    # ═══════════════════════════════════════════════════════════════════════════

    {
        "yoga_name":      "Degreewise Pair Rectification — Proportional Precision",
        "sloka":          "ch43-sloka-45-46",
        "group":          "class_modifiers",
        "condition_type": "general_principle",
        "formation": (
            "Longevity contribution is maximised at 0° of a sign and reduced to zero "
            "at 30°. For intermediate placements, use the Rule of Three: "
            "Sum the longitudes of contributing planets (devoid of sign multiples), "
            "divide by the number of contributors, multiply by the basic years of "
            "the class, and divide by 30. "
            "Formula: (Sum_of_degrees / count) × basic_years / 30."
        ),
        "effect": (
            "Fine-tunes the quantum calculation with degree-level precision. A planet "
            "at 0° of its sign contributes maximum years; one at 29° contributes "
            "almost nothing on a per-degree basis."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "description": "Degree-precision rectification for pair engine. Phase 2.",
        },
    },

    {
        "yoga_name":      "Saturn Class Decline — Longevity Class Downgrade",
        "sloka":          "ch43-sloka-47",
        "group":          "class_modifiers",
        "condition_type": "planetary_combination",
        "formation": (
            "When Saturn is one of the contributing factors in the longevity calculation, "
            "the CLASS of longevity declines by one step (e.g., Long → Medium, "
            "Medium → Short). "
            "Exception: no decline occurs if Saturn is in its own sign (Capricorn or "
            "Aquarius) or in exaltation (Libra), even if aspected by malefics."
        ),
        "effect": (
            "Saturn's natural constricting influence 'pulls down' the longevity class "
            "by one grade unless it holds essential dignity. A chart that would otherwise "
            "indicate Long Life becomes Medium Life when Saturn is a contributor without "
            "dignity."
        ),
        "is_benefic":   False,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "planet":      "Saturn",
            "description": (
                "Check planets['Saturn (Shani)']['dignity'] not in ['own_sign','exalted','moolatrikona']. "
                "If Saturn lacks dignity, flag as class-decline trigger."
            ),
        },
    },

    {
        "yoga_name":      "Jupiter Class Rise — Longevity Class Upgrade",
        "sloka":          "ch43-sloka-48",
        "group":          "class_modifiers",
        "condition_type": "planetary_combination",
        "formation": (
            "When Jupiter occupies the Ascendant (H1) or the 7th house AND is aspected "
            "by or conjunct ONLY benefics (no malefic aspect or conjunction), "
            "the CLASS of longevity increases by one step (Short → Medium, Medium → Long)."
        ),
        "effect": (
            "Jupiter in an angular position with pure benefic company upgrades the "
            "longevity class. A chart indicating Short Life can be promoted to Medium "
            "Life through this single condition — Jupiter's protective grace must be "
            "uncontaminated by malefic influence."
        ),
        "is_benefic":   True,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "planet":      "Jupiter",
            "houses":      [1, 7],
            "description": (
                "Check planets['Jupiter (Brihaspati)']['house'] in [1,7]. "
                "Malefic-only-aspect check is Phase 2 (requires aspect evaluation)."
            ),
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # GROUP 7: LONGEVITY YOGAS
    # ═══════════════════════════════════════════════════════════════════════════

    {
        "yoga_name":      "Seven-Fold Longevity Classification",
        "sloka":          "ch43-sloka-52-54",
        "group":          "longevity_yogas",
        "condition_type": "general_principle",
        "formation": (
            "BPHS recognises seven classes of lifespan: "
            "Balarishta (childhood death) < 8 years. "
            "Yogarishta (youth death) < 20 years. "
            "Short (Alpayu) up to 32 years. "
            "Medium (Madhyamayu) up to 64 years. "
            "Long (Purnayu) up to 120 years. "
            "Supernatural (Divya) = 1000 years. "
            "Illimitable (Amitayu) = acquired by extraordinary merits."
        ),
        "effect": (
            "Provides the complete classification hierarchy for longevity assessment. "
            "Most human charts fall in the Short/Medium/Long range (0–120 years). "
            "Divya and Amitayu are yogic/exceptional spans beyond normal human capacity."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "description": "Classification reference table.",
        },
    },

    {
        "yoga_name":      "Amitayu Yoga — Limitless Longevity",
        "sloka":          "ch43-sloka-55-56",
        "group":          "longevity_yogas",
        "condition_type": "planetary_combination",
        "formation": (
            "Conditions for Amitayu (limitless/illimitable longevity): "
            "Cancer Ascendant AND Jupiter + Moon both in the 1st house AND "
            "Venus and Mercury in angular houses (H1, H4, H7, or H10) AND "
            "other planets in 3rd, 6th, and 11th houses (Upachaya positions)."
        ),
        "effect": (
            "When fully satisfied, this yoga confers a lifespan beyond normal human "
            "reckoning — the 'Amitayu' or illimitable span, acquired through "
            "extraordinary spiritual merit. Extremely rare in natal charts."
        ),
        "is_benefic":   True,
        "life_domains": ["longevity", "supernatural"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Check: lagna sign == 'Cancer' AND "
                "planets['Jupiter (Brihaspati)']['house'] == 1 AND "
                "planets['Moon (Chandra)']['house'] == 1 AND "
                "planets['Venus (Shukra)']['house'] in [1,4,7,10] AND "
                "planets['Mercury (Budha)']['house'] in [1,4,7,10]."
            ),
        },
    },

    {
        "yoga_name":      "Divya Yoga — Supernatural 1000-Year Span",
        "sloka":          "ch43-sloka-57",
        "group":          "longevity_yogas",
        "condition_type": "planetary_combination",
        "formation": (
            "Conditions for Divya (supernatural longevity of 1000 years): "
            "Benefics (Jupiter, Venus, Mercury, waxing Moon) occupy angular (H1, H4, H7, H10) "
            "and trinal (H1, H5, H9) houses AND malefics (Sun, Mars, Saturn, Rahu, Ketu) "
            "occupy the 3rd, 6th, and 11th houses (Upachaya) AND the 8th house is "
            "occupied by or receives the sign of a benefic planet."
        ),
        "effect": (
            "The ideal distribution of benefics in benefic houses and malefics in "
            "Upachaya houses — the classic 'Raj Yoga' pattern — when combined with "
            "a protected 8th house, confers a supernatural lifespan."
        ),
        "is_benefic":   True,
        "life_domains": ["longevity", "supernatural"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Check benefics in angles/trines AND malefics in [3,6,11] AND "
                "8th house sign lord is a benefic. Complex multi-condition check."
            ),
        },
    },

    {
        "yoga_name":      "End of Yuga Yoga — Jupiter + Venus Varga Conditions",
        "sloka":          "ch43-sloka-58",
        "group":          "longevity_yogas",
        "condition_type": "planetary_combination",
        "formation": (
            "Conditions: Cancer Ascendant AND Jupiter in an angular house at Gopuramsa "
            "varga dignity (4th tier in the Vimshopaka system) AND Venus in a trinal "
            "house at Paaravatamsa varga dignity (5th tier). "
            "Outcome: 'End of Yuga' span — an astronomically long lifespan exceeding "
            "normal human bounds."
        ),
        "effect": (
            "A varga-triggered supernatural lifespan requiring both specific house "
            "placement AND advanced divisional dignity from Jupiter and Venus. "
            "The standard house-placement logic is overridden by Varga status."
        ),
        "is_benefic":   True,
        "life_domains": ["longevity", "supernatural"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   False,
            "blockers":    ["V"],
            "description": "Requires Gopuramsa and Paaravatamsa varga tier computation. Phase 2.",
        },
    },

    {
        "yoga_name":      "Sage Longevity Yoga — Varga Triad (Jupiter + Saturn + Mars)",
        "sloka":          "ch43-sloka-58",
        "group":          "longevity_yogas",
        "condition_type": "planetary_combination",
        "formation": (
            "Conditions: Jupiter in the 1st house at Simhasanamsa varga dignity (4th tier) "
            "AND Saturn at Devalokamsa (6th tier) AND Mars at Paaravatamsa (5th tier). "
            "Outcome: 'Span of a Sage' — extraordinary longevity consistent with a "
            "spiritually elevated being."
        ),
        "effect": (
            "This yoga requires three planets to simultaneously achieve high varga "
            "dignity — an extremely rare condition. When met, it confers the lifespan "
            "associated with ancient sages and spiritually advanced beings."
        ),
        "is_benefic":   True,
        "life_domains": ["longevity", "supernatural"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   False,
            "blockers":    ["V"],
            "description": "Requires Simhasanamsa, Devalokamsa, Paaravatamsa varga tiers. Phase 2.",
        },
    },

    {
        "yoga_name":      "Full Life Span Yogas — 120 Years (Purnayu)",
        "sloka":          "ch43-sloka-60-64",
        "group":          "longevity_yogas",
        "condition_type": "planetary_combination",
        "formation": (
            "Four formations conferring full lifespan (Purnayu ~120 years): "
            "Yoga A: Benefics in angular houses AND Ascendant lord conjunct or aspected "
            "by a benefic or Jupiter. "
            "Yoga B: Ascendant lord in an angular house AND conjunct or aspected by "
            "both Jupiter and Venus. "
            "Yoga C: Three or more planets in exaltation (including lords of H1 and H8) "
            "AND 8th house empty AND 8th house not aspected by malefics. "
            "Yoga D: Benefics in H6, H7, H8 AND malefics in H3 and H11."
        ),
        "effect": (
            "Any of these four formations indicates a full human lifespan of approximately "
            "120 years. Yoga D follows the Malefic Displacement Principle — malefics "
            "thrive in Upachaya houses (3, 11) while benefics protect the sensitive "
            "death/longevity axis (6, 7, 8)."
        ),
        "is_benefic":   True,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Yoga A: check benefics in [1,4,7,10] + ASC lord aspected by benefic. "
                "Yoga D: check benefics in [6,7,8] AND malefics in [3,11]. "
                "Yogas B and C require aspect evaluation (Phase 2)."
            ),
        },
    },

    {
        "yoga_name":      "Long Life Yogas — Dirghaayu",
        "sloka":          "ch43-sloka-65-70",
        "group":          "longevity_yogas",
        "condition_type": "planetary_combination",
        "formation": (
            "Five formations conferring long life (64–120 years): "
            "Yoga A: Three or more planets in H8 in exaltation/own/friendly signs "
            "AND Ascendant lord is strong. "
            "Yoga B: Saturn or Ascendant lord conjunct any exalted planet. "
            "Yoga C: Malefics in H3, H6, H11 AND benefics in angular houses. "
            "Yoga D: A malefic in H8 AND the 10th lord is exalted. "
            "Yoga E: Dual/common sign Ascendant AND Ascendant lord in angle, "
            "exaltation, or trine."
        ),
        "effect": (
            "These combinations indicate a lifespan exceeding 64 years. Yoga C "
            "is the 'classical Raj Yoga longevity pattern' — malefics displaced to "
            "Upachaya houses, benefics holding the angular framework."
        ),
        "is_benefic":   True,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Yoga C: check malefics in [3,6,11] AND benefics in [1,4,7,10]. "
                "Yoga E: check ASC sign is dual (Gemini/Virgo/Sagittarius/Pisces). "
                "Other yogas require aspect/strength evaluation (Phase 2)."
            ),
        },
    },

    {
        "yoga_name":      "Short Life Yogas — Alpayu",
        "sloka":          "ch43-sloka-71-74",
        "group":          "longevity_yogas",
        "condition_type": "planetary_combination",
        "formation": (
            "Four formations indicating short life (< 32 years): "
            "Yoga A: Mars or 3rd lord combust OR 8th lord or Saturn combust AND "
            "additionally aspected/conjunct by malefics. "
            "Yoga B: Ascendant lord in a house with malefics AND no benefic aspect. "
            "Yoga C: Malefics in angular houses AND no benefic aspect AND Ascendant "
            "lord is weak. "
            "Yoga D: Malefics in H12 and H2 AND no benefic aspect. "
            "Upgrade: if lords of H1 and H8 are weak but receive aspect/help from "
            "other planets → diagnose Medium Life instead."
        ),
        "effect": (
            "These are warning indicators for significantly shortened lifespan. "
            "The 'Weakness-to-Help' modifier provides a diagnostic upgrade — "
            "if weak lords receive planetary support, Short Life is upgraded to Medium."
        ),
        "is_benefic":   False,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Yoga B: check ASC lord's house contains malefics (no benefic aspect — Phase 2). "
                "Yoga D: check malefics in [12,2] (no benefic aspect check — Phase 2). "
                "Full evaluation of all four requires aspect data."
            ),
        },
    },

    {
        "yoga_name":      "Strength-Placement Longevity — Stronger of H1/H8 Lords",
        "sloka":          "ch43-sloka-71-73",
        "group":          "longevity_yogas",
        "condition_type": "general_principle",
        "formation": (
            "Compare the Shadbala strength of the Ascendant Lord and the 8th House Lord. "
            "Whichever is stronger determines the longevity class based on its house: "
            "Stronger lord in Angular house (H1, H4, H7, H10) → Long Life. "
            "Stronger lord in Panaphara house (H2, H5, H8, H11) → Medium Life. "
            "Stronger lord in Apoklima house (H3, H6, H9, H12) → Short Life. "
            "Final refinement: the classification is further adjusted by the lord's "
            "friendship relationship to the Sun (friendly/neutral/inimical)."
        ),
        "effect": (
            "A strength-based longevity gate that integrates both Shadbala "
            "and house placement. The dominant lord's angular/panaphara/apoklima "
            "position sets the baseline class, then solar friendship refines it."
        ),
        "is_benefic":   None,
        "life_domains": ["longevity"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "blockers":    ["L", "KE"],
            "description": "Requires lord identification + Shadbala comparison. Phase 2.",
        },
    },
]


# ── Build function (Ch 40 schema) ─────────────────────────────────────────────

def _build_rules() -> list[dict]:
    now = datetime.now(timezone.utc)
    rules: list[dict] = []
    for i, entry in enumerate(YOGA_DATA, start=1):
        rid        = f"{BOOK_ID}-ch{CHAPTER:02d}-{i:03d}"
        group      = entry["group"]
        ctype      = entry["condition_type"]
        yoga_name  = entry["yoga_name"]
        formation  = entry["formation"]
        effect     = entry.get("effect", "")
        domains    = entry.get("life_domains", [])
        is_benefic = entry.get("is_benefic")
        ycheck     = entry["yoga_check"]
        checkable  = bool(ycheck.get("checkable"))
        detailed   = formation + (" Effect: " + effect if effect else "")
        tags       = [group, ctype]
        if checkable:
            tags.append("yoga_checkable")

        planets_involved = (
            ycheck.get("planets", [])
            or ([ycheck["planet"]] if ycheck.get("planet") else [])
        )

        rule = {
            "rule_id":    rid,
            "science_id": SCIENCE,
            "source": {
                "book":           BOOK,
                "book_id":        BOOK_ID,
                "chapter":        CHAPTER,
                "chapter_name":   CHAP_NAME,
                "sloka":          entry.get("sloka", ""),
                "batch_id":       BATCH_ID,
                "primary":        BOOK,
                "page_ref":       None,
                "passage_ref_id": None,
            },
            "condition": {
                "type":               ctype,
                "sub_type":           "longevity_calculation",
                "yoga_name":          yoga_name,
                "yoga_group":         group,
                "yoga_group_label":   group.replace("_", " ").title(),
                "planets_involved":   planets_involved,
                "houses_involved":    ycheck.get("houses", []),
                "sub_conditions":     [],
                "operator":           "and",
                "gender_context":     "neutral",
                "condition_group_id": f"bphs-ch{CHAPTER:02d}-{group}",
                "is_group_summary":   False,
                "is_benefic":         is_benefic,
                "yoga_check":         ycheck,
            },
            "interpretation": {
                "summary":            yoga_name,
                "detailed":           detailed,
                "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
                "remedies":           [],
                "life_domain":        domains[0] if domains else "longevity",
                "life_domains":       domains,
                "tags":               tags,
                "physical_markers":   [],
            },
            "metadata": {
                "planets_involved":     planets_involved,
                "houses_involved":      ycheck.get("houses", []),
                "signs_involved":       [],
                "condition_count":      1,
                "gender_context":       "neutral",
                "condition_group_id":   f"bphs-ch{CHAPTER:02d}-{group}",
                "is_group_summary":     False,
                "has_physical_markers": False,
                "physical_categories":  [],
                "yoga_checkable":       checkable,
            },
            "confidence": {
                "source_confidence":  "HIGH",
                "extraction_method":  "hard_coded",
                "validated":          False,
            },
            "approval_status": "pending_review",
            "created_at":      now.isoformat(),
        }
        rules.append(rule)
    return rules


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description=f"Ingest BPHS Ch {CHAPTER} — {CHAP_NAME}"
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--save",    metavar="PATH")
    parser.add_argument("--upload",  metavar="PATH")
    parser.add_argument("--mongo-url", metavar="URL",  default="")
    parser.add_argument("--db-name",   metavar="NAME", default="horoscope_db")
    args = parser.parse_args()

    rules = _build_rules()

    from collections import Counter
    groups    = Counter(r["condition"]["yoga_group"] for r in rules)
    ctypes    = Counter(r["condition"]["type"]       for r in rules)
    checkable = sum(1 for r in rules if r["condition"]["yoga_check"].get("checkable"))
    print(f"\nBPHS Ch {CHAPTER} — {CHAP_NAME}")
    print(f"  Batch:      {BATCH_ID}")
    print(f"  Rules:      {len(rules)}")
    print(f"  Checkable:  {checkable} / {len(rules)}")
    print(f"\n  Groups:")
    for g, n in sorted(groups.items()):
        print(f"    {g:<35} {n:>3}")
    print(f"\n  Condition types:")
    for ct, n in sorted(ctypes.items()):
        print(f"    {ct:<35} {n:>3}")

    if args.dry_run or not args.upload:
        print("\n[DRY RUN — no data written]")
        if args.save:
            out = Path(args.save)
            out.write_text(json.dumps(rules, indent=2, default=str), encoding="utf-8")
            print(f"  Saved → {out}")
        return

    if args.upload:
        src = Path(args.upload)
        if not src.exists():
            print(f"ERROR: file not found — {src}", file=sys.stderr)
            sys.exit(1)
        rules = json.loads(src.read_text(encoding="utf-8"))

    if not args.mongo_url:
        print("ERROR: --mongo-url required for upload", file=sys.stderr)
        sys.exit(1)

    from pymongo import MongoClient
    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]
    result = col.insert_many(rules)
    print(f"\n✅ Inserted {len(result.inserted_ids)} rules → {args.db_name}.interpretation_rules")
    client.close()


if __name__ == "__main__":
    main()
