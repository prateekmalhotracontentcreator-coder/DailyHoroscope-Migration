#!/usr/bin/env python3
"""
ingest_bphs_ch27_v1.py — BPHS Chapter 27: Evaluation of Strengths (Shadbala)

29 rules total across 3 groups:
  17  Shadbala Engine Specification  (Logic Units 27.1–27.16, 27.22–27.24, 27.26–27.27)
   3  Bhava Bala Specification       (Logic Units 27.16, 27.17, 27.25)
   9  Strength Interpretation        (Logic Units 27.18–27.21, plus minimum thresholds)

Source:
  PDF:      BPHS_Ch27_Vol1 _Strengths.pdf
  Decode:   BPHS_Ch27_Vol1_JSON Ready_LM.docx
  Diag:     BPHS_Ch27_Vol1_Diagnostic_LM.docx

Architecture note:
  The Shadbala engine itself is implemented in backend/vedic_calculator.py
  (calculate_shadbala(), committed c0de967 + Tribhaga fix committed after).
  Ch 27 rules in this batch serve two purposes:
    1. Engine Specification (condition_type = "engine_specification"):
       Canonical reference for the implemented formulae — 0 checkable.
       These are auto-candidated for approval since they ARE the standard.
    2. Strength Interpretation (condition_type = "planet_shadbala_strong"
       or "constituent_shadbala_minimum"):
       Diagnostic rules fired against Shadbala output — Phase 2 promotion
       once KE evaluator is wired to the 'shadbala' payload in chart data.

Tribhaga bug fixed in vedic_calculator.py (same commit as this script):
  WRONG: Mercury always 60, day lords = Jupiter/Sun/Saturn
  FIXED: Jupiter always 60, day lords = Mercury/Sun/Saturn   (BPHS Ch27.9)

Standard --save / --upload workflow:
  Step 1 — Dry run:
    python3 scripts/ingest_bphs_ch27_v1.py --dry-run --save scripts/bphs_ch27_rules.json

  Step 2 — Review bphs_ch27_rules.json; amend as needed.

  Step 3 — Upload:
    python3 scripts/ingest_bphs_ch27_v1.py \\
      --upload scripts/bphs_ch27_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 4 — Validate:
    python3 scripts/validate_rules.py \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id bphs-ch27-v1-20260504
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Constants ─────────────────────────────────────────────────────────────────

SCIENCE   = "jyotish"
BOOK      = "Brihat Parashara Hora Shastra"
BOOK_ID   = "bphs"
CHAPTER   = 27
CHAP_NAME = "Evaluation of Strengths (Shadbala)"
BATCH_ID  = "bphs-ch27-v1-20260504"

# ── Rule data ─────────────────────────────────────────────────────────────────

YOGA_DATA: list[dict] = [

    # ═══════════════════════════════════════════════════════════════════════════
    # GROUP 1: SHADBALA ENGINE SPECIFICATION
    # All 6 strength components + sub-components.
    # condition_type = "engine_specification"
    # Implemented in: backend/vedic_calculator.py → calculate_shadbala()
    # ═══════════════════════════════════════════════════════════════════════════

    # ── Sthana Bala (Positional Strength) ────────────────────────────────────

    {
        "yoga_name":      "Uchcha Bala — Exaltation Strength Formula",
        "sloka":          "ch27-sloka-01-03",
        "group":          "shadbala_engine_spec",
        "condition_type": "engine_specification",
        "formation": (
            "Component of Sthana Bala. Procedure: deduct the deep debilitation "
            "longitude from the planet's actual longitude. If the result is < 180°, "
            "use as-is; if > 180°, deduct from 360°. Divide final value by 3 to "
            "obtain Uchcha Bala in Virupas. Maximum = 60 Virupas (1 Rupa). "
            "Deep debilitation point = exaltation longitude + 180°."
        ),
        "effect": (
            "Measures how close a planet is to its exaltation peak. A planet at "
            "exact exaltation scores maximum Uchcha Bala (60); at exact debilitation "
            "it scores 0. Contributes to Sthana Bala total."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    [],
            "description": (
                "Implemented in vedic_calculator._uchcha_bala(). "
                "Engine spec reference only — not a KE evaluator rule."
            ),
        },
    },

    {
        "yoga_name":      "Saptavargaja Bala — Divisional Dignity Strength",
        "sloka":          "ch27-sloka-04-06",
        "group":          "shadbala_engine_spec",
        "condition_type": "engine_specification",
        "formation": (
            "Component of Sthana Bala. Compute the dignity of a planet in each of "
            "the 7 divisional charts (D1 Rasi, D2 Hora, D3 Drekkana, D7 Saptamamsa, "
            "D9 Navamsa, D12 Dvadasamsa, D30 Trimsamsa) and award Virupas per "
            "dignity: Moolatrikona=45, Own Sign=30, Extreme Friend=20, Friend=15, "
            "Neutral=10, Enemy=4, Extreme Enemy=2. Sum all 7 divisions."
        ),
        "effect": (
            "Measures how well-placed a planet is across all 7 divisional charts. "
            "A planet in Moolatrikona in all 7 divisions scores 315 Virupas maximum. "
            "Contributes to Sthana Bala total."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    ["V"],
            "description": (
                "Requires all 7 divisional chart positions. Current engine "
                "computes D1 dignity only (own_sign/friendly/enemy etc.) via "
                "get_planet_dignity(). Full Saptavargaja requires D1–D30 "
                "positions — Phase 2 once varga engine expands beyond D9."
            ),
        },
    },

    {
        "yoga_name":      "Ojhayugmarasiamsa Bala — Odd/Even Sign Strength",
        "sloka":          "ch27-sloka-07-09",
        "group":          "shadbala_engine_spec",
        "condition_type": "engine_specification",
        "formation": (
            "Component of Sthana Bala. Male/neutral planets (Sun, Mars, Jupiter, "
            "Mercury, Saturn) in an odd Rasi → 15 Virupas; same planets in an odd "
            "Navamsa → another 15 Virupas. Female planets (Moon, Venus) in an even "
            "Rasi → 15 Virupas; in an even Navamsa → 15 Virupas. Maximum = 30 per "
            "planet (15 Rasi + 15 Navamsa). Mercury and Saturn always score 30 "
            "(neutral, benefit from both)."
        ),
        "effect": (
            "Rewards planets placed in signs aligned with their gender polarity. "
            "Contributes to Sthana Bala total."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    [],
            "description": (
                "Implemented in vedic_calculator._ojayugma_bala(). "
                "Engine spec reference only — not a KE evaluator rule."
            ),
        },
    },

    {
        "yoga_name":      "Kendradi Bala — House Quality Strength",
        "sloka":          "ch27-sloka-10-11",
        "group":          "shadbala_engine_spec",
        "condition_type": "engine_specification",
        "formation": (
            "Component of Sthana Bala. Planet in an angular house (1, 4, 7, 10) "
            "→ 60 Virupas. Planet in a succedent house (2, 5, 8, 11) → 30 Virupas. "
            "Planet in a cadent house (3, 6, 9, 12) → 15 Virupas."
        ),
        "effect": (
            "Measures the strength of house placement. Angular placement confers "
            "maximum Kendradi Bala (1 Rupa). Contributes to Sthana Bala total."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    [],
            "description": (
                "Implemented in vedic_calculator._kendradi_bala(). "
                "Engine spec reference only — not a KE evaluator rule."
            ),
        },
    },

    {
        "yoga_name":      "Drekkana Bala — Gender-Decanate Positional Strength",
        "sloka":          "ch27-sloka-12",
        "group":          "shadbala_engine_spec",
        "condition_type": "engine_specification",
        "formation": (
            "Component of Sthana Bala. 15 Virupas granted based on planetary gender "
            "and decanate (Drekkana) within a sign: Male planets (Sun, Mars, Jupiter) "
            "in the 1st Decanate (0°–10°) of any sign. Female planets (Moon, Venus) "
            "in the 2nd Decanate (10°–20°). Eunuch/neutral planets (Mercury, Saturn) "
            "in the 3rd Decanate (20°–30°). Otherwise 0."
        ),
        "effect": (
            "Small positional bonus aligned with planetary gender and the "
            "masculine/feminine/neutral thirds of a sign. Contributes to Sthana "
            "Bala total."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    [],
            "description": (
                "Not separately implemented in current Shadbala engine — "
                "absorbed into Sthana Bala approximation. "
                "Phase 2 enhancement to add Drekkana sub-component."
            ),
        },
    },

    # ── Dig Bala (Directional Strength) ─────────────────────────────────────

    {
        "yoga_name":      "Dig Bala — Directional Strength",
        "sloka":          "ch27-sloka-13-14",
        "group":          "shadbala_engine_spec",
        "condition_type": "engine_specification",
        "formation": (
            "Full strength direction (point of nil strength is the opposite): "
            "Jupiter and Mercury → Ascendant (1st house, East). "
            "Sun and Mars → 10th house (South/Meridian). "
            "Saturn → 7th house (West/Descendant). "
            "Moon and Venus → 4th house (North/Nadir). "
            "Formula: deduct longitude of nil-strength house from planet longitude, "
            "divide by 3. If result > 180°, deduct from 360°. Max = 60 Virupas."
        ),
        "effect": (
            "Rewards planets placed in their naturally strong direction. Jupiter "
            "and Mercury flourish near the Ascendant; Sun and Mars near the "
            "Midheaven; Saturn near the Descendant; Moon and Venus near the IC."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    [],
            "description": (
                "Implemented in vedic_calculator._dig_bala() using whole-sign "
                "house approximation. Engine spec reference only."
            ),
        },
    },

    # ── Kala Bala (Temporal Strength) ────────────────────────────────────────

    {
        "yoga_name":      "Nathonnatha Bala — Day/Night Temporal Strength",
        "sloka":          "ch27-sloka-15",
        "group":          "shadbala_engine_spec",
        "condition_type": "engine_specification",
        "formation": (
            "Based on proximity to midnight (Nata) or noon (Unnata). "
            "Day group (Sun, Jupiter, Venus): full 60 Virupas during daytime. "
            "Night group (Moon, Mars, Saturn): full 60 Virupas during night. "
            "Mercury: always 60 Virupas (neutral — neither day nor night planet). "
            "Formula: Natha Ghatis × 2 for night-group; 60 minus night-group value "
            "for day-group. Mercury constant = 60."
        ),
        "effect": (
            "Temporal strength from diurnal or nocturnal dominance. A daytime "
            "birth empowers Sun, Jupiter, and Venus; a night birth empowers Moon, "
            "Mars, and Saturn. Mercury is always temporally favoured."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    [],
            "description": (
                "Implemented in vedic_calculator.calculate_shadbala() as binary "
                "60/0 day-night check (simplified). Full proximity-to-noon/midnight "
                "formula is a Phase 2 enhancement. Engine spec reference only."
            ),
        },
    },

    {
        "yoga_name":      "Paksha Bala — Lunar Fortnight Strength",
        "sloka":          "ch27-sloka-16",
        "group":          "shadbala_engine_spec",
        "condition_type": "engine_specification",
        "formation": (
            "Formula: (Moon Longitude − Sun Longitude) / 3 = elongation-based "
            "Virupas. Benefics (Moon, Mercury, Jupiter, Venus) receive higher "
            "strength in Sukla Paksha (Bright Half, 0°–180° elongation). Malefics "
            "(Sun, Mars, Saturn) receive higher strength in Krishna Paksha (Dark "
            "Half, 180°–360° elongation). Maximum = 60 Virupas."
        ),
        "effect": (
            "Measures how well the Moon's phase aligns with the planet's natural "
            "benefic/malefic character. Moon's own Cheshta Bala is identically equal "
            "to its Paksha Bala (see Logic Unit 27.22)."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    [],
            "description": (
                "Implemented in vedic_calculator._paksha_bala(). "
                "Engine spec reference only."
            ),
        },
    },

    {
        "yoga_name":      "Tribhaga Bala — Diurnal/Nocturnal Division Strength",
        "sloka":          "ch27-sloka-17",
        "group":          "shadbala_engine_spec",
        "condition_type": "engine_specification",
        "formation": (
            "Day and night are each divided into three equal thirds. 60 Virupas "
            "granted to the lord of the third in which birth occurs. "
            "Day thirds: 1st = Mercury, 2nd = Sun, 3rd = Saturn. "
            "Night thirds: 1st = Moon, 2nd = Venus, 3rd = Mars. "
            "Jupiter: receives 60 Virupas at all times (constant). "
            "Note: Mercury's 'always 60' applies to Nathonnatha, NOT Tribhaga."
        ),
        "effect": (
            "A temporal bonus awarded to the planet that 'rules' the current "
            "third of the day or night. Only one planet (plus Jupiter always) "
            "receives this bonus per chart."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    [],
            "description": (
                "Implemented in vedic_calculator._tribhaga_bala(). "
                "Codex bug fixed: Jupiter constant (not Mercury); day lords = "
                "Mercury/Sun/Saturn (not Jupiter/Sun/Saturn). "
                "Engine spec reference only."
            ),
        },
    },

    {
        "yoga_name":      "Varsha-Maasa-Dina-Hora Bala — Temporal Lordship Multipliers",
        "sloka":          "ch27-sloka-18",
        "group":          "shadbala_engine_spec",
        "condition_type": "engine_specification",
        "formation": (
            "Fixed Virupa awards for the planet that holds each temporal lordship "
            "at birth: Hora Lord (current planetary hour) = 60 Virupas. "
            "Dina Lord (weekday lord) = 45 Virupas. "
            "Maasa Lord (lunar month lord, from new moon) = 30 Virupas. "
            "Varsha Lord (year lord, from Mesha Sankranti) = 15 Virupas. "
            "A planet may hold multiple lordships simultaneously."
        ),
        "effect": (
            "Cumulative temporal bonus. A planet that is Hora, Dina, Maasa, and "
            "Varsha Lord simultaneously can score 150 additional Virupas within "
            "Kala Bala — a rare maximum condition."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    [],
            "description": (
                "Implemented in vedic_calculator.calculate_shadbala(). "
                "Hora lord via _hora_lord(); Dina lord via _weekday_lord_from_jd(jd); "
                "Maasa lord via _find_previous_new_moon_jd(); Varsha lord via "
                "_find_previous_mesha_sankranti_jd(). Engine spec reference only."
            ),
        },
    },

    {
        "yoga_name":      "Ayana Bala — Equinoctial/Solstitial Strength",
        "sloka":          "ch27-sloka-19-21",
        "group":          "shadbala_engine_spec",
        "condition_type": "engine_specification",
        "formation": (
            "Based on a planet's declination (Kranti) from the celestial equator. "
            "Planets gain strength when their declination aligns with their natural "
            "hemisphere: Sun, Mars, Jupiter, Venus → gain from Northern declination "
            "(Uttara Kranti). Moon, Saturn → gain from Southern declination (Dakshina "
            "Kranti). Mercury → always gains regardless of direction. "
            "Sun's final Ayana Bala is multiplied by 2. "
            "Formula: 30 + (declination / 24° × 30) for direct cases; "
            "reverse for Moon/Saturn. Clamped to 0–60 Virupas."
        ),
        "effect": (
            "Temporal-directional strength from a planet's position relative to "
            "the equinoxes. A planet near its favoured solstice gains up to 60 "
            "Virupas. Part of Kala Bala total."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    [],
            "description": (
                "Implemented in vedic_calculator._ayana_bala(). "
                "Engine spec reference only."
            ),
        },
    },

    # ── Naisargika Bala (Natural Strength) ────────────────────────────────────

    {
        "yoga_name":      "Naisargika Bala — Natural Luminosity Strength",
        "sloka":          "ch27-sloka-22",
        "group":          "shadbala_engine_spec",
        "condition_type": "engine_specification",
        "formation": (
            "Fixed natural strength by luminosity (Virupas): "
            "Sun=60.0, Moon=51.43, Venus=42.86, Jupiter=34.29, "
            "Mercury=25.71, Mars=17.14, Saturn=8.57. "
            "These values are permanent constants — never change per chart. "
            "Tie-breaker rule: when two planets have equal total Shadbala, "
            "the planet with higher Naisargika Bala prevails in effects."
        ),
        "effect": (
            "The Sun is always the most naturally powerful graha; Saturn the "
            "weakest in inherent luminosity. Used as the final arbiter when "
            "other strengths are equal."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    [],
            "description": (
                "Implemented as NAISARGIKA_BALA constant dict in vedic_calculator.py. "
                "Engine spec reference only."
            ),
        },
    },

    # ── Cheshta Bala (Motional Strength) ─────────────────────────────────────

    {
        "yoga_name":      "Cheshta Bala — Motional Strength (Sun and Moon Equivalency)",
        "sloka":          "ch27-sloka-23",
        "group":          "shadbala_engine_spec",
        "condition_type": "engine_specification",
        "formation": (
            "Sun: Cheshta Bala is identical to Ayana Bala — no separate motional "
            "calculation required. Moon: Cheshta Bala is identical to Paksha Bala. "
            "For starry planets (Mars through Saturn), Cheshta Bala is computed "
            "separately via the Cheshta Kendra formula (see Logic Unit 27.24)."
        ),
        "effect": (
            "The Sun and Moon's motional strength is absorbed into their temporal "
            "and phase strengths. Only the five starry planets have an independent "
            "Cheshta Bala component."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    [],
            "description": (
                "Implemented in vedic_calculator._chesta_bala() using actual speed "
                "vs mean daily motion ratio (simplified). Full Seeghrocha-based "
                "formula is a Phase 2 enhancement. Engine spec reference only."
            ),
        },
    },

    {
        "yoga_name":      "Cheshta Bala — Eight Kinds of Planetary Motion",
        "sloka":          "ch27-sloka-24-26",
        "group":          "shadbala_engine_spec",
        "condition_type": "engine_specification",
        "formation": (
            "Applies to starry planets (Mars, Mercury, Jupiter, Venus, Saturn). "
            "Eight motion types with Virupa awards: "
            "Vakra (Retrogression) = 60. "
            "Anuvakra (Entering previous sign in retrograde) = 30. "
            "Vikala (Stationary/devoid of motion) = 15. "
            "Manda (Slower than normal) = 30. "
            "Mandatara (Slower than Manda) = 15. "
            "Sama (Somewhat increasing in motion) = 7.5. "
            "Chara (Faster than mean) = 45. "
            "Atichara (Entering next sign in accelerated motion) = 30."
        ),
        "effect": (
            "Retrograde motion confers maximum Cheshta Bala (60). A stationary "
            "planet paradoxically scores low (15). Fast-moving planets near their "
            "mean speed score moderately. This table is the canonical lookup for "
            "precise Cheshta Bala — more granular than the simplified speed-ratio."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    [],
            "description": (
                "Current engine uses simplified speed-ratio approach. Phase 2 "
                "enhancement: detect motion type from speed and sign-crossing "
                "flags, then apply this 8-tier lookup table. "
                "Engine spec reference only."
            ),
        },
    },

    {
        "yoga_name":      "Cheshta Kendra — Mathematical Derivation of Motional Angle",
        "sloka":          "ch27-sloka-27-29",
        "group":          "shadbala_engine_spec",
        "condition_type": "engine_specification",
        "formation": (
            "For starry planets. Procedure: "
            "1. Average the planet's Mean Longitude and True Longitude. "
            "2. Deduct this average from the planet's Seeghrocha (Apogee). "
            "   Result = Cheshta Kendra. "
            "3. If Cheshta Kendra > 180°, deduct from 360°. "
            "4. Divide final value in degrees by 3 = Cheshta Bala Virupas. "
            "Applicable planets: Mars, Mercury, Jupiter, Venus, Saturn."
        ),
        "effect": (
            "The precise BPHS formula for deriving motional strength from a "
            "planet's relationship to its apogee. A planet at Cheshta Kendra = 0° "
            "or 360° scores 0; at 180° from apogee scores maximum 60 Virupas."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    ["S"],
            "description": (
                "Requires Seeghrocha (planetary apogee) data from Swiss Ephemeris. "
                "Phase 2: access swe.calc_ut with additional flags for apogee "
                "longitude per planet. Engine spec reference only."
            ),
        },
    },

    # ── Drig Bala (Aspectual Strength) ────────────────────────────────────────

    {
        "yoga_name":      "Drig Bala — Aspectual Strength",
        "sloka":          "ch27-sloka-30-32",
        "group":          "shadbala_engine_spec",
        "condition_type": "engine_specification",
        "formation": (
            "Sum of all aspectual influences received by a planet. "
            "For each aspecting planet: deduct 1/4 of the Drishti Pinda "
            "(aspect value) for malefic aspects; add 1/4 for benefic aspects. "
            "Super-addition: add the FULL aspect value of Mercury and Jupiter's "
            "aspects (not just 1/4). Net sum = Drig Bala in Virupas. "
            "Can be negative (net malefic pressure)."
        ),
        "effect": (
            "Measures the net quality of planetary influences received. A planet "
            "heavily aspected by benefics gains positive Drig Bala; malefic "
            "aspects reduce it. Jupiter and Mercury aspects are "
            "doubly weighted in this calculation."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    [],
            "description": (
                "Implemented in vedic_calculator._drik_bala() using simplified "
                "Parashari aspect model. Full Drishti Pinda with partial aspect "
                "values per degree is a Phase 2 enhancement. Engine spec reference."
            ),
        },
    },

    # ── Yuddha Bala (Planetary War Strength) ─────────────────────────────────

    {
        "yoga_name":      "Yuddha Bala — Planetary War Strength Redistribution",
        "sloka":          "ch27-sloka-33-35",
        "group":          "shadbala_engine_spec",
        "condition_type": "engine_specification",
        "formation": (
            "Applies when two starry planets (Mars through Saturn) are within 1° "
            "of each other (Yuddha / Planetary War). The victor is determined by "
            "the planet with greater total Shadbala at that moment. "
            "Rule: the difference between the two planets' total Shadbalas is "
            "added to the victor's score and deducted from the vanquished planet's "
            "score. Sun, Moon, Rahu, and Ketu are exempt from Yuddha."
        ),
        "effect": (
            "Planetary war amplifies the strong planet and further weakens the "
            "defeated planet. A planet vanquished in war loses Shadbala and "
            "correspondingly weakens its significations during its dashas."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    ["Y"],
            "description": (
                "Implemented as _yuddha_bala() stub returning 0 for all planets. "
                "Full implementation: detect pairs within 1° longitude, compare "
                "preliminary Shadbalas, redistribute difference. "
                "Staged simplification per commission brief. Phase 2 enhancement."
            ),
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # GROUP 2: BHAVA BALA SPECIFICATION
    # House strength rules — separate from planetary Shadbala.
    # ═══════════════════════════════════════════════════════════════════════════

    {
        "yoga_name":      "Bhava Bala — House Strength Composite Engine",
        "sloka":          "ch27-sloka-36-38",
        "group":          "bhava_bala_spec",
        "condition_type": "engine_specification",
        "formation": (
            "Bhava Bala has four components: "
            "1. Bhava Cusp Strength: degrees from nil-strength point / 3 = Virupas. "
            "2. Occupancy Modifier: Jupiter/Mercury occupant +60 Virupas; "
            "   Sun/Mars/Saturn occupant −60 Virupas. "
            "3. Aspect Modifier: +1/4 of Drishti Pinda for benefic aspects; "
            "   −1/4 for malefic aspects. "
            "4. Time/Sign Modifier: +15 Virupas for Seershodaya signs at day birth, "
            "   Dual/Common signs at twilight birth, Prishtodaya signs at night birth."
        ),
        "effect": (
            "The composite house strength. Higher Bhava Bala means the house and "
            "its significations are more potent and more likely to manifest clearly "
            "in the native's life."
        ),
        "is_benefic":   None,
        "life_domains": ["house_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    ["B"],
            "description": (
                "Bhava Bala engine not yet implemented. Phase 2: build "
                "calculate_bhava_bala() alongside Shadbala in vedic_calculator.py."
            ),
        },
    },

    {
        "yoga_name":      "Bhava Occupancy & Sign Modifiers — Detailed Rules",
        "sloka":          "ch27-sloka-39-40",
        "group":          "bhava_bala_spec",
        "condition_type": "engine_specification",
        "formation": (
            "Bhava occupied by Jupiter or Mercury → +60 Virupas (house gains strength). "
            "Bhava occupied by Saturn, Mars, or Sun → −60 Virupas (house loses strength). "
            "Birth in Day AND bhava in Seershodaya Rasi (Gemini, Leo, Virgo, Libra, "
            "Scorpio, Aquarius) → +15 Virupas. "
            "Birth at Twilight AND bhava in Dual/Common Rasi (Gemini, Virgo, Sagittarius, "
            "Pisces) → +15 Virupas. "
            "Birth at Night AND bhava in Prishtodaya Rasi (Aries, Taurus, Cancer, "
            "Sagittarius, Capricorn) → +15 Virupas."
        ),
        "effect": (
            "Beneficial natural planets (Jupiter, Mercury) elevate house strength; "
            "natural malefics (Saturn, Mars, Sun) depress it. The sign-type modifier "
            "aligns house strength with the day/night quality of the birth."
        ),
        "is_benefic":   None,
        "life_domains": ["house_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    ["B"],
            "description": (
                "Bhava Bala engine not yet implemented. These are sub-rules of the "
                "Bhava Bala calculation, not standalone KE evaluator rules. "
                "Phase 2 Bhava Bala engine."
            ),
        },
    },

    {
        "yoga_name":      "Sign-Specific Bhava Cusp Strength Calculation",
        "sloka":          "ch27-sloka-41-44",
        "group":          "bhava_bala_spec",
        "condition_type": "engine_specification",
        "formation": (
            "The nil-strength reference point for Bhava Cusp Strength varies by "
            "sign occupied by the bhava: "
            "Virgo, Gemini, Libra, Aquarius, 1st half Sagittarius → use 7th house "
            "(Descendant) longitude as nil-strength point. "
            "Aries, Taurus, Leo, 1st half Capricorn, 2nd half Sagittarius → use "
            "4th house (Nadir) longitude. "
            "Cancer, Scorpio → use Ascendant longitude. "
            "2nd half Capricorn, Pisces → use 10th house (Meridian) longitude. "
            "Rectification: if deduction result > 6 signs (180°), deduct again from "
            "12 signs (360°) before dividing by 3 for Virupas."
        ),
        "effect": (
            "The point of minimum house strength varies by sign, reflecting the "
            "compass-direction alignment of sign groups. This rule makes Bhava Bala "
            "sensitive to both time and geography."
        ),
        "is_benefic":   None,
        "life_domains": ["house_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    ["B"],
            "description": (
                "Bhava Bala engine not yet implemented. Phase 2. "
                "Engine spec reference only."
            ),
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # GROUP 3: STRENGTH INTERPRETATION
    # Diagnostic rules fired against Shadbala output.
    # Checkable: False for now (Phase 2 — KE needs 'shadbala' payload wired).
    # ═══════════════════════════════════════════════════════════════════════════

    {
        "yoga_name":      "Shadbala Minimum Threshold — Planet Deemed Strong",
        "sloka":          "ch27-sloka-45-47",
        "group":          "strength_interpretation",
        "condition_type": "planet_shadbala_strong",
        "formation": (
            "A planet is deemed Strong (Bali) when its total Shadbala meets or "
            "exceeds the minimum Rupa threshold: Sun ≥ 6.5 Rupas, Moon ≥ 6.0, "
            "Mars ≥ 5.0, Mercury ≥ 7.0, Jupiter ≥ 6.5, Venus ≥ 5.5, Saturn ≥ 5.0. "
            "These thresholds are now encoded as MINIMUM_RUPAS constants in the "
            "Shadbala engine (vedic_calculator.py) and returned as 'is_strong' per "
            "planet in the chart payload."
        ),
        "effect": (
            "A planet meeting its Rupa minimum is classed as Strong (Bali). It "
            "delivers its significations fully and positively during its Mahadasha "
            "and Antardasha periods. A planet below threshold is weak — its "
            "dasha effects are diminished, delayed, or obstructed."
        ),
        "is_benefic":   True,
        "life_domains": ["planetary_strength", "dasha_prediction"],
        "yoga_check": {
            "type":        "planet_shadbala_strong",
            "checkable":   False,
            "blockers":    ["KE"],
            "description": (
                "Condition type 'planet_shadbala_strong' not yet wired in KE "
                "evaluator. Phase 2: add evaluator branch that reads "
                "planets[planet]['shadbala']['is_strong'] from chart payload. "
                "MINIMUM_RUPAS already enforced in calculate_shadbala()."
            ),
        },
    },

    {
        "yoga_name":      "Saturn Strength Paradox — Long Life with Miseries",
        "sloka":          "ch27-sloka-48-49",
        "group":          "strength_interpretation",
        "condition_type": "planet_shadbala_strong",
        "formation": (
            "When Saturn possesses the required or extreme Shadbala (is_strong = True, "
            "total Rupas ≥ 5.0), it simultaneously confers two contradictory outcomes: "
            "long life (Dirghayu) AND persistent miseries or suffering. "
            "This paradox is specific to Saturn — strength does not guarantee "
            "enjoyment, only endurance."
        ),
        "effect": (
            "A strong Saturn in the chart grants the native longevity but does not "
            "protect against hardship. Saturn's dasha periods, even when the planet "
            "is fully Bali (strong), will involve discipline, delay, loss, and "
            "karmic reckoning alongside stability and persistence."
        ),
        "is_benefic":   False,
        "life_domains": ["longevity", "suffering", "karma", "dasha_prediction"],
        "yoga_check": {
            "type":        "planet_shadbala_strong",
            "checkable":   False,
            "blockers":    ["KE"],
            "planet":      "Saturn",
            "description": (
                "Phase 2: evaluator checks planets['Saturn (Shani)']['shadbala']['is_strong']. "
                "If True, tag chart with 'saturn_strength_paradox' marker. "
                "Not yet wired to KE evaluator."
            ),
        },
    },

    {
        "yoga_name":      "Constituent Strength Minimum — Group A (Jupiter, Mercury, Sun)",
        "sloka":          "ch27-sloka-50-52",
        "group":          "strength_interpretation",
        "condition_type": "constituent_shadbala_minimum",
        "formation": (
            "Even if total Shadbala falls short of the minimum Rupas, a planet is "
            "still 'Considerably Favourable' if it meets these constituent minimums "
            "in Virupas. Group A applies to Jupiter, Mercury, and Sun: "
            "Sthana Bala ≥ 165, Dig Bala ≥ 35, Kala Bala ≥ 50, "
            "Cheshta Bala ≥ 112, Ayana Bala ≥ 30."
        ),
        "effect": (
            "Jupiter, Mercury, or Sun meeting Group A minimums is classified as "
            "Considerably Favourable even without full Shadbala. This is a "
            "diagnostic fallback that prevents over-penalising a planet that is "
            "strong in specific dimensions while weak overall."
        ),
        "is_benefic":   True,
        "life_domains": ["planetary_strength", "dasha_prediction"],
        "yoga_check": {
            "type":        "constituent_shadbala_minimum",
            "checkable":   False,
            "blockers":    ["KE"],
            "planets":     ["Jupiter", "Mercury", "Sun"],
            "group":       "A",
            "minimums_virupas": {
                "sthana_bala": 165, "dig_bala": 35, "kala_bala": 50,
                "chesta_bala": 112, "ayana_bala": 30,
            },
            "description": (
                "Phase 2: evaluator reads individual component scores from "
                "planets[planet]['shadbala'] and compares against these thresholds. "
                "Not yet wired to KE evaluator."
            ),
        },
    },

    {
        "yoga_name":      "Constituent Strength Minimum — Group B (Moon, Venus)",
        "sloka":          "ch27-sloka-53-55",
        "group":          "strength_interpretation",
        "condition_type": "constituent_shadbala_minimum",
        "formation": (
            "Diagnostic fallback for Moon and Venus. Even if total Shadbala falls "
            "short of minimum Rupas, the planet is 'Considerably Favourable' if: "
            "Sthana Bala ≥ 133, Dig Bala ≥ 50, Kala Bala ≥ 30, "
            "Cheshta Bala ≥ 100, Ayana Bala ≥ 40."
        ),
        "effect": (
            "Moon or Venus meeting Group B minimums is classified as Considerably "
            "Favourable. Moon and Venus require higher Dig Bala and Ayana Bala "
            "than the Sun group, reflecting their fundamentally receptive and "
            "relational nature."
        ),
        "is_benefic":   True,
        "life_domains": ["planetary_strength", "dasha_prediction"],
        "yoga_check": {
            "type":        "constituent_shadbala_minimum",
            "checkable":   False,
            "blockers":    ["KE"],
            "planets":     ["Moon", "Venus"],
            "group":       "B",
            "minimums_virupas": {
                "sthana_bala": 133, "dig_bala": 50, "kala_bala": 30,
                "chesta_bala": 100, "ayana_bala": 40,
            },
            "description": (
                "Phase 2: evaluator reads individual component scores from "
                "planets[planet]['shadbala'] and compares against these thresholds. "
                "Not yet wired to KE evaluator."
            ),
        },
    },

    {
        "yoga_name":      "Constituent Strength Minimum — Group C (Mars, Saturn)",
        "sloka":          "ch27-sloka-56-58",
        "group":          "strength_interpretation",
        "condition_type": "constituent_shadbala_minimum",
        "formation": (
            "Diagnostic fallback for Mars and Saturn. Even if total Shadbala falls "
            "short of minimum Rupas, the planet is 'Considerably Favourable' if: "
            "Sthana Bala ≥ 96, Dig Bala ≥ 30, Kala Bala ≥ 40, "
            "Cheshta Bala ≥ 67, Ayana Bala ≥ 20. "
            "Note: Saturn paradox (rule 27.18) still applies even when Group C "
            "minimums are met."
        ),
        "effect": (
            "Mars or Saturn meeting Group C minimums is Considerably Favourable. "
            "The thresholds are lower than Groups A and B, reflecting the natural "
            "malefic character of these planets — they need less to achieve "
            "functional strength."
        ),
        "is_benefic":   True,
        "life_domains": ["planetary_strength", "dasha_prediction"],
        "yoga_check": {
            "type":        "constituent_shadbala_minimum",
            "checkable":   False,
            "blockers":    ["KE"],
            "planets":     ["Mars", "Saturn"],
            "group":       "C",
            "minimums_virupas": {
                "sthana_bala": 96, "dig_bala": 30, "kala_bala": 40,
                "chesta_bala": 67, "ayana_bala": 20,
            },
            "description": (
                "Phase 2: evaluator reads individual component scores from "
                "planets[planet]['shadbala'] and compares against these thresholds. "
                "Not yet wired to KE evaluator."
            ),
        },
    },

    {
        "yoga_name":      "Bhava Manifestation Protocol — Strongest Planet Governs",
        "sloka":          "ch27-sloka-59-61",
        "group":          "strength_interpretation",
        "condition_type": "general_principle",
        "formation": (
            "Whatever yogas or effects are declared for a house (bhava), they shall "
            "manifest ONLY through the planet with the highest Shadbala associated "
            "with that bhava — either as its lord or as an occupant. "
            "If the strongest associated planet has insufficient Shadbala, the "
            "house effects are diminished regardless of the yoga's inherent strength."
        ),
        "effect": (
            "No house acts independently. Its effects are funnelled through and "
            "amplified by its strongest planet. A house with a strong lord but "
            "malefic occupants will express through the lord; a house with a weak "
            "lord but a powerful occupant will express through the occupant."
        ),
        "is_benefic":   None,
        "life_domains": ["house_strength", "yoga_manifestation"],
        "yoga_check": {
            "type":        "general_principle",
            "checkable":   False,
            "blockers":    ["KE", "B"],
            "description": (
                "Requires both Shadbala (for ranking planets) and Bhava Bala engine. "
                "This is an architectural principle for the interpretation layer, "
                "not a standalone condition. Phase 2 after both engines are wired."
            ),
        },
    },

    {
        "yoga_name":      "Ahargana Derivation — Varsha and Maasa Lord Calculation",
        "sloka":          "ch27-sloka-18",
        "group":          "strength_interpretation",
        "condition_type": "engine_specification",
        "formation": (
            "Determines which planet receives the Varsha (Year) and Maasa (Month) "
            "temporal multipliers using day-count from creation (Ahargana). "
            "Varsha Lord: divide Ahargana by 360; multiply completed years by 3, "
            "add 1, divide by 7 — remainder is weekday index for Varsha lord. "
            "Maasa Lord: divide Ahargana by 30; multiply completed months by 2, "
            "add 1, divide by 7 — remainder is weekday index for Maasa lord. "
            "Dina Lord: Ahargana mod 7 = weekday index (Sunday=0, Saturday=6). "
            "Weekday sequence: Sun/Moon/Mars/Mercury/Jupiter/Venus/Saturn."
        ),
        "effect": (
            "Provides the exact mathematical derivation for the temporal lordship "
            "multipliers. The current engine approximates Varsha lord from Mesha "
            "Sankranti (Sun's Aries ingress) and Maasa lord from the preceding new "
            "moon, which is equivalent in effect."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    [],
            "description": (
                "Current engine uses _find_previous_mesha_sankranti_jd() and "
                "_find_previous_new_moon_jd() for Varsha and Maasa lords — "
                "equivalent to Ahargana approach. Engine spec reference only."
            ),
        },
    },

    {
        "yoga_name":      "Ayana Bala Kranti Precision — Declination Direction Rules",
        "sloka":          "ch27-sloka-20-22",
        "group":          "strength_interpretation",
        "condition_type": "engine_specification",
        "formation": (
            "Precise directional gate for Ayana Bala declination (Kranti): "
            "Sun, Mars, Jupiter, Venus → Northern declination (Uttara Kranti) = PLUS. "
            "Moon, Saturn → Southern declination (Dakshina Kranti) = PLUS. "
            "Mercury → any direction = always PLUS. "
            "Opposite conditions = MINUS for all except Mercury. "
            "Super-modifier: Sun's final Ayana Bala product is always multiplied by 2. "
            "Mercury exception: gains strength from any declination (always PLUS)."
        ),
        "effect": (
            "The directional gate determines whether a planet's distance from the "
            "equinox adds to or subtracts from Ayana Bala. Sun in Northern declination "
            "is doubly empowered (standard gain × 2). Mercury ignores direction entirely."
        ),
        "is_benefic":   None,
        "life_domains": ["planetary_strength"],
        "yoga_check": {
            "type":        "engine_specification",
            "checkable":   False,
            "blockers":    [],
            "description": (
                "Implemented in vedic_calculator._ayana_bala() using "
                "_planet_declination() and the Moon/Saturn reversal logic. "
                "Sun × 2 modifier and Mercury always-PLUS both present. "
                "Engine spec reference only."
            ),
        },
    },
]

# ── Build function ────────────────────────────────────────────────────────────

def _build_rules() -> list[dict]:
    now = datetime.now(timezone.utc)
    rules: list[dict] = []
    for i, entry in enumerate(YOGA_DATA, start=1):
        rid = f"{BOOK_ID}-ch{CHAPTER:02d}-{i:03d}"
        rule = {
            "batch_id":        BATCH_ID,
            "rule_id":         rid,
            "science":         SCIENCE,
            "source_book":     BOOK,
            "source_book_id":  BOOK_ID,
            "source_chapter":  CHAPTER,
            "source_chapter_name": CHAP_NAME,
            "source_sloka":    entry.get("sloka", ""),
            "rule_group":      entry["group"],
            "yoga_name":       entry["yoga_name"],
            "condition_type":  entry["condition_type"],
            "formation":       entry["formation"],
            "effect":          entry["effect"],
            "is_benefic":      entry.get("is_benefic"),
            "life_domains":    entry.get("life_domains", []),
            "yoga_check":      entry["yoga_check"],
            "approval_status": "pending_review",
            "validation": {
                "status":         "pending_review",
                "validator_notes": [],
                "last_validated": None,
            },
            "created_at":      now.isoformat(),
            "updated_at":      now.isoformat(),
        }
        rules.append(rule)
    return rules


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description=f"Ingest BPHS Ch {CHAPTER} — {CHAP_NAME}"
    )
    parser.add_argument("--dry-run",   action="store_true",
                        help="Build rules without writing anywhere")
    parser.add_argument("--save",      metavar="PATH",
                        help="Save rules JSON to this path (use with --dry-run)")
    parser.add_argument("--upload",    metavar="PATH",
                        help="Upload from this JSON file to MongoDB")
    parser.add_argument("--mongo-url", metavar="URL",  default="")
    parser.add_argument("--db-name",   metavar="NAME", default="horoscope_db")
    args = parser.parse_args()

    rules = _build_rules()

    # ── Summary ───────────────────────────────────────────────────────────────
    from collections import Counter
    groups  = Counter(r["rule_group"]      for r in rules)
    ctypes  = Counter(r["condition_type"]  for r in rules)
    checkable_count = sum(1 for r in rules if r["yoga_check"].get("checkable"))
    print(f"\nBPHS Ch {CHAPTER} — {CHAP_NAME}")
    print(f"  Batch:      {BATCH_ID}")
    print(f"  Rules:      {len(rules)}")
    print(f"  Checkable:  {checkable_count} / {len(rules)}")
    print(f"\n  Groups:")
    for g, n in sorted(groups.items()):
        print(f"    {g:<35} {n:>3}")
    print(f"\n  Condition types:")
    for ct, n in sorted(ctypes.items()):
        print(f"    {ct:<35} {n:>3}")

    # ── Dry run ───────────────────────────────────────────────────────────────
    if args.dry_run or (not args.upload):
        print("\n[DRY RUN — no data written]")
        if args.save:
            out = Path(args.save)
            out.write_text(json.dumps(rules, indent=2, default=str), encoding="utf-8")
            print(f"  Saved → {out}")
        return

    # ── Upload ────────────────────────────────────────────────────────────────
    if args.upload:
        src = Path(args.upload)
        if not src.exists():
            print(f"ERROR: file not found — {src}", file=sys.stderr)
            sys.exit(1)
        rules = json.loads(src.read_text(encoding="utf-8"))

    if not args.mongo_url:
        print("ERROR: --mongo-url required for upload", file=sys.stderr)
        sys.exit(1)

    try:
        from motor.frameworks.asyncio import AsyncIOMotorClient  # type: ignore
    except ImportError:
        from pymongo import MongoClient  # type: ignore
        client = MongoClient(args.mongo_url)
        db     = client[args.db_name]
        col    = db["yoga_rules"]
        result = col.insert_many(rules)
        print(f"\n✅ Inserted {len(result.inserted_ids)} rules → {args.db_name}.yoga_rules")
        client.close()
        return

    import asyncio

    async def _upload() -> None:
        from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
        client = AsyncIOMotorClient(args.mongo_url)
        db     = client[args.db_name]
        col    = db["yoga_rules"]
        result = await col.insert_many(rules)
        print(f"\n✅ Inserted {len(result.inserted_ids)} rules → {args.db_name}.yoga_rules")
        client.close()

    asyncio.run(_upload())


if __name__ == "__main__":
    main()
