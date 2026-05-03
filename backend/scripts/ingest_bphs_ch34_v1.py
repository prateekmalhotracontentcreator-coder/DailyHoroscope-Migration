#!/usr/bin/env python3
"""
ingest_bphs_ch34_v1.py — BPHS Chapter 34: Nature of Planets Due to Lordship

82 rules total across 4 groups:
   6  Lordship Principle    (LU 34.1–34.6)   — core engine rules (checkable: False)
   4  General Principle     (LU 34.7–34.10)  — graduation/stalling/adversity (checkable: False)
   5  Rajayoga Definition   (LU 34.11–34.15) — 4 checkable, 1 not
  67  Lagna Planet Quality  (12 lagnas × planets) — all checkable: False (lagna evaluator needed)

Hard-coded from docx decode — zero AI extraction cost.
Checkable: 4 / 82 (5%) — LU 34.11, 34.12, 34.14, 34.15 are planetary_combination checks.

Standard --save / --upload workflow:
  Step 1 — Dry run:
    python3 scripts/ingest_bphs_ch34_v1.py --dry-run --save scripts/bphs_ch34_rules.json

  Step 2 — Review bphs_ch34_rules.json; amend as needed.

  Step 3 — Upload:
    python3 scripts/ingest_bphs_ch34_v1.py \\
      --upload scripts/bphs_ch34_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 4 — Validate:
    python3 scripts/validate_rules.py \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id bphs-ch34-v1-20260503
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
CHAPTER   = 34
CHAP_NAME = "Nature of Planets Due to Lordship"
BATCH_ID  = "bphs-ch34-v1-20260503"

# ── Lagna quality table ───────────────────────────────────────────────────────
# Compact source: docx decode + Diagnostics file
# Keys: lagna → planet → {quality, houses, note, extra_label}
# quality: "auspicious" | "malefic" | "yogakaraka" | "neutral" | "killer"
# extra_label: optional second label (e.g. Venus for Virgo = auspicious + killer)

LAGNA_QUALITY_TABLE: dict[str, dict[str, dict]] = {
    "Aries": {
        "Jupiter": {
            "quality": "auspicious",
            "houses": [9, 12],
            "note": "Pure 9th lord (best trine); Moolatrikona Sagittarius in 9th dominates over 12th.",
        },
        "Sun": {
            "quality": "auspicious",
            "houses": [5],
            "note": "Pure 5th lord (trine); single lordship, no evil house contamination.",
        },
        "Saturn": {
            "quality": "malefic",
            "houses": [10, 11],
            "note": "Moolatrikona Aquarius = 11th (most evil house) predominates over 10th angular lordship.",
        },
        "Mercury": {
            "quality": "malefic",
            "houses": [3, 6],
            "note": "Lords both evil houses — 3rd and 6th; doubly malefic.",
        },
        "Venus": {
            "quality": "killer",
            "houses": [2, 7],
            "note": "Marak (death-inflicting) planet: lords both 2nd and 7th (Marak houses).",
        },
        "Mars": {
            "quality": "neutral",
            "houses": [1, 8],
            "note": "Lagna lord (1st = Moolatrikona Aries) counterbalanced by 8th lordship; neither clearly auspicious nor evil.",
        },
    },
    "Taurus": {
        "Saturn": {
            "quality": "yogakaraka",
            "houses": [9, 10],
            "note": "Single planet lords both 9th (trine/Capricorn) and 10th (angle/Aquarius); the Yogakaraka for Taurus.",
        },
        "Sun": {
            "quality": "auspicious",
            "houses": [4],
            "note": "4th lord (angular); as a natural malefic, angular lordship does not produce Kendradhipatya dosha.",
        },
        "Jupiter": {
            "quality": "malefic",
            "houses": [8, 11],
            "note": "Lords 8th (evil) and 11th (most evil); Moolatrikona Sagittarius = 8th; doubly malefic.",
        },
        "Venus": {
            "quality": "malefic",
            "houses": [1, 6],
            "note": "Lagna lord (1st) but also 6th lord (evil house); Kendradhipatya dosha (natural benefic owning angle) plus evil 6th lordship.",
        },
        "Moon": {
            "quality": "malefic",
            "houses": [3],
            "note": "Pure 3rd lord (evil house); no redeeming lordship.",
        },
    },
    "Gemini": {
        "Venus": {
            "quality": "auspicious",
            "houses": [5, 12],
            "note": "5th lord (trine); Moolatrikona Taurus = 5th dominates over 12th; pure trinal lord.",
        },
        "Mars": {
            "quality": "malefic",
            "houses": [6, 11],
            "note": "Lords 6th and 11th — both evil houses; doubly malefic.",
        },
        "Jupiter": {
            "quality": "malefic",
            "houses": [7, 10],
            "note": "Kendradhipatya dosha: natural benefic owning two angular houses (7th and 10th) loses benefic nature.",
        },
        "Sun": {
            "quality": "malefic",
            "houses": [3],
            "note": "Pure 3rd lord (evil house).",
        },
        "Moon": {
            "quality": "killer",
            "houses": [2],
            "note": "2nd lord = Marak (death-inflicting); single Marak lordship.",
        },
    },
    "Cancer": {
        "Mars": {
            "quality": "yogakaraka",
            "houses": [5, 10],
            "note": "Single planet lords 5th (trine/Scorpio) and 10th (angle/Aries); Moolatrikona Aries = 10th; Yogakaraka for Cancer.",
        },
        "Jupiter": {
            "quality": "auspicious",
            "houses": [6, 9],
            "note": "9th lord (best trine/Pisces); despite Moolatrikona Sagittarius being in 6th, BPHS classifies Jupiter as auspicious — 9th lord quality dominates per text.",
        },
        "Moon": {
            "quality": "auspicious",
            "houses": [1],
            "note": "Lagna lord (Cancer = 1st); 1st house is both angle and trine; natural lord of its sign.",
        },
        "Venus": {
            "quality": "malefic",
            "houses": [4, 11],
            "note": "Moolatrikona Taurus = 4th (angle); Kendradhipatya dosha (natural benefic in angle) plus 11th evil lordship.",
        },
        "Mercury": {
            "quality": "malefic",
            "houses": [3, 12],
            "note": "3rd lord (evil house); Moolatrikona Virgo = 12th; predominantly malefic.",
        },
    },
    "Leo": {
        "Mars": {
            "quality": "auspicious",
            "houses": [4, 9],
            "note": "9th lord (trine/Aries); Moolatrikona Aries = 9th dominates; natural malefic so no Kendradhipatya for angular 4th lordship.",
        },
        "Jupiter": {
            "quality": "auspicious",
            "houses": [5, 8],
            "note": "5th lord (trine/Sagittarius); Moolatrikona Sagittarius = 5th dominates over evil 8th lordship.",
        },
        "Sun": {
            "quality": "auspicious",
            "houses": [1],
            "note": "Lagna lord (Leo = 1st); 1st is both angle and trine; natural malefic so no Kendradhipatya.",
        },
        "Mercury": {
            "quality": "malefic",
            "houses": [2, 11],
            "note": "2nd lord (Marak/Virgo) and 11th lord (evil); Moolatrikona Virgo = 2nd; double blemish.",
        },
        "Venus": {
            "quality": "malefic",
            "houses": [3, 10],
            "note": "3rd lord (evil) and 10th lord (angle); Kendradhipatya (natural benefic in angle) plus evil 3rd lordship.",
        },
        "Saturn": {
            "quality": "malefic",
            "houses": [6, 7],
            "note": "6th lord (evil) and 7th lord (Marak); Moolatrikona Aquarius = 7th Marak; doubly malefic.",
        },
        "Moon": {
            "quality": "killer",
            "houses": [12],
            "note": "12th lord; described in BPHS as a killer/maraka planet for Leo — brings loss and dissolution themes.",
        },
    },
    "Virgo": {
        "Mercury": {
            "quality": "auspicious",
            "houses": [1, 10],
            "note": "Lagna lord (Virgo = 1st) and 10th lord; Moolatrikona Virgo = 1st; 1st is both angle and trine.",
        },
        "Venus": {
            "quality": "auspicious",
            "houses": [2, 9],
            "extra_label": "killer",
            "note": "9th lord (trine/Taurus) makes Venus auspicious; also 2nd lord (Marak) making it simultaneously a killer/Marak. Dual classification: auspicious AND Marak.",
        },
        "Mars": {
            "quality": "malefic",
            "houses": [3, 8],
            "note": "3rd lord (evil) and 8th lord (evil); doubly malefic.",
        },
        "Jupiter": {
            "quality": "malefic",
            "houses": [4, 7],
            "note": "Kendradhipatya dosha: natural benefic owning two angular houses (4th and 7th); both angular blemishes compound.",
        },
        "Moon": {
            "quality": "malefic",
            "houses": [11],
            "note": "Pure 11th lord (most evil house); no redeeming lordship.",
        },
    },
    "Libra": {
        "Saturn": {
            "quality": "auspicious",
            "houses": [4, 5],
            "note": "5th lord (trine/Aquarius); Moolatrikona Aquarius = 5th dominates; natural malefic so no Kendradhipatya for 4th angular lordship.",
        },
        "Mercury": {
            "quality": "auspicious",
            "houses": [9, 12],
            "note": "9th lord (trine/Gemini); BPHS classifies as auspicious — 9th lord quality dominates despite Moolatrikona Virgo in 12th.",
        },
        "Jupiter": {
            "quality": "malefic",
            "houses": [3, 6],
            "note": "3rd lord (evil) and 6th lord (evil); doubly malefic.",
        },
        "Sun": {
            "quality": "malefic",
            "houses": [11],
            "note": "Pure 11th lord (most evil house).",
        },
        "Mars": {
            "quality": "malefic",
            "houses": [2, 7],
            "note": "2nd lord (Marak) and 7th lord (Marak); double Marak planet; Moolatrikona Aries = 2nd.",
        },
        "Venus": {
            "quality": "neutral",
            "houses": [1, 8],
            "note": "Lagna lord (Libra = 1st) and 8th lord; Kendradhipatya (natural benefic as lagna lord/angle) plus 8th evil; net result is neutral per BPHS.",
        },
    },
    "Scorpio": {
        "Jupiter": {
            "quality": "auspicious",
            "houses": [2, 5],
            "note": "5th lord (trine/Pisces) makes Jupiter auspicious; Moolatrikona Sagittarius = 2nd Marak, but 5th trine quality dominates per BPHS.",
        },
        "Moon": {
            "quality": "yogakaraka",
            "houses": [9],
            "note": "Pure 9th lord (Cancer = 9th); described in BPHS as Yogakaraka for Scorpio — best-result planet during its Dasha.",
        },
        "Sun": {
            "quality": "yogakaraka",
            "houses": [10],
            "note": "10th lord (Leo = 10th); described in BPHS as Yogakaraka for Scorpio alongside Moon — gives the best status and authority results.",
        },
        "Venus": {
            "quality": "malefic",
            "houses": [7, 12],
            "note": "7th lord (Marak/Taurus) and 12th lord; Moolatrikona Taurus = 7th Marak.",
        },
        "Mercury": {
            "quality": "malefic",
            "houses": [8, 11],
            "note": "8th lord (evil) and 11th lord (most evil); doubly malefic.",
        },
        "Saturn": {
            "quality": "malefic",
            "houses": [3, 4],
            "note": "3rd lord (evil) and 4th lord (angle); 3rd evil lordship makes Saturn malefic despite angular 4th lordship.",
        },
        "Mars": {
            "quality": "neutral",
            "houses": [1, 6],
            "note": "Lagna lord (Scorpio = 1st) and 6th lord (evil); Moolatrikona Aries = 6th for Scorpio → evil house predominates; net result neutral as lagna lord counterbalances.",
        },
    },
    "Sagittarius": {
        "Mars": {
            "quality": "auspicious",
            "houses": [5, 12],
            "note": "5th lord (trine/Aries); Moolatrikona Aries = 5th dominates over 12th; pure trinal lord.",
        },
        "Sun": {
            "quality": "auspicious",
            "houses": [9],
            "note": "Pure 9th lord (Leo = 9th); single lordship of best trine house.",
        },
        "Venus": {
            "quality": "malefic",
            "houses": [6, 11],
            "note": "6th lord (evil) and 11th lord (most evil); Moolatrikona Libra = 11th; doubly malefic.",
        },
        "Saturn": {
            "quality": "killer",
            "houses": [2, 3],
            "note": "2nd lord (Marak/Capricorn) and 3rd lord (evil); Moolatrikona Aquarius = 3rd; Marak plus evil house.",
        },
    },
    "Capricorn": {
        "Venus": {
            "quality": "yogakaraka",
            "houses": [5, 10],
            "note": "Single planet lords 5th (trine/Taurus) and 10th (angle/Libra); Moolatrikona Taurus = 5th; Yogakaraka for Capricorn.",
        },
        "Mercury": {
            "quality": "auspicious",
            "houses": [6, 9],
            "note": "9th lord (Virgo = 9th); Moolatrikona Virgo = 9th dominates over 6th evil lordship; auspicious per BPHS.",
        },
        "Mars": {
            "quality": "malefic",
            "houses": [4, 11],
            "note": "11th lord (evil/Scorpio) and 4th lord (angle); Moolatrikona Aries = 4th angular, but 11th evil lordship makes Mars malefic.",
        },
        "Jupiter": {
            "quality": "malefic",
            "houses": [3, 12],
            "note": "3rd lord (evil) and 12th lord; Moolatrikona Sagittarius = 3rd evil; predominantly malefic.",
        },
        "Moon": {
            "quality": "malefic",
            "houses": [7],
            "note": "7th lord (Marak/Cancer); Kendradhipatya (natural benefic in angle) plus Marak status.",
        },
    },
    "Aquarius": {
        "Venus": {
            "quality": "yogakaraka",
            "houses": [4, 9],
            "note": "Single planet lords 4th (angle/Taurus) and 9th (trine/Libra); Moolatrikona Taurus = 4th; Yogakaraka for Aquarius.",
        },
        "Saturn": {
            "quality": "auspicious",
            "houses": [1, 12],
            "note": "Lagna lord (Aquarius = 1st); Moolatrikona Aquarius = 1st (both angle and trine); natural malefic so no Kendradhipatya.",
        },
        "Jupiter": {
            "quality": "malefic",
            "houses": [2, 11],
            "note": "2nd lord (Marak) and 11th lord (most evil); Moolatrikona Sagittarius = 11th evil; doubly malefic.",
        },
        "Moon": {
            "quality": "malefic",
            "houses": [6],
            "note": "Pure 6th lord (evil house/Cancer).",
        },
        "Mars": {
            "quality": "malefic",
            "houses": [3, 10],
            "note": "3rd lord (evil/Aries); Moolatrikona Aries = 3rd evil; despite 10th angular lordship, 3rd evil predominates.",
        },
    },
    "Pisces": {
        "Mars": {
            "quality": "yogakaraka",
            "houses": [2, 9],
            "note": "9th lord (trine/Scorpio) and 2nd lord (Marak/Aries); BPHS classifies as Yogakaraka for Pisces — 9th trine quality dominates, making Mars the best planet for this lagna.",
        },
        "Moon": {
            "quality": "auspicious",
            "houses": [5],
            "note": "Pure 5th lord (trine/Cancer); single lordship with no evil house.",
        },
        "Jupiter": {
            "quality": "yogakaraka",
            "houses": [1, 10],
            "note": "Lagna lord (Pisces = 1st) and 10th lord (angle/Sagittarius); 1st is both angle and trine; Yogakaraka for Pisces alongside Mars.",
        },
        "Saturn": {
            "quality": "malefic",
            "houses": [11, 12],
            "note": "11th lord (most evil/Capricorn) and 12th lord; Moolatrikona Aquarius = 12th; predominantly malefic.",
        },
        "Venus": {
            "quality": "malefic",
            "houses": [3, 8],
            "note": "3rd lord (evil) and 8th lord (evil); Moolatrikona Taurus = 3rd; doubly malefic.",
        },
        "Sun": {
            "quality": "malefic",
            "houses": [6],
            "note": "Pure 6th lord (evil house/Leo).",
        },
        "Mercury": {
            "quality": "malefic",
            "houses": [4, 7],
            "note": "7th lord (Marak/Virgo) and 4th lord (angle); Moolatrikona Virgo = 7th Marak; Kendradhipatya (natural benefic in angle) plus Marak.",
        },
    },
}

QUALITY_LABELS = {
    "auspicious": "Auspicious",
    "malefic":    "Malefic",
    "yogakaraka": "Yogakaraka",
    "neutral":    "Neutral",
    "killer":     "Killer / Marak",
}

QUALITY_EFFECTS = {
    "auspicious": (
        "Acts as a beneficial planet for this ascendant. Gives good results — "
        "prosperity, growth, and favourable outcomes — during its Mahadasha and "
        "Antardasha periods. Strengthens the houses it lords and occupies."
    ),
    "malefic": (
        "Acts as a malefic planet for this ascendant. Gives adverse results — "
        "obstacles, losses, or harm to the significations of the houses it lords — "
        "during its Mahadasha and Antardasha periods."
    ),
    "yogakaraka": (
        "Acts as the Yogakaraka — the single most powerful benefic planet for this "
        "ascendant. Lords both an angular house and a trinal house simultaneously, "
        "combining the power of Vishnu (angles) and Lakshmi (trines). Gives "
        "exceptionally auspicious results during its Dasha periods."
    ),
    "neutral": (
        "Acts as a neutral planet for this ascendant. Gives moderate or mixed results "
        "depending on its placement, associations, and the houses it lords. Not "
        "clearly benefic or malefic; context-dependent in application."
    ),
    "killer": (
        "Acts as a Marak (killer / death-inflicting) planet for this ascendant. "
        "Lords one or both of the Marak houses (2nd and 7th), conferring the ability "
        "to harm longevity and inflict adversity during its Dasha periods, especially "
        "in the final Dasha at old age."
    ),
}

# ── Non-lagna rule data ───────────────────────────────────────────────────────

NON_LAGNA_RULES: list[dict] = [

    # ═══════════════════════════════════════════════════════════════════════════
    # 1. LORDSHIP PRINCIPLES (LU 34.1–34.6)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":      "Kendradhipatya Dosha — Angular Blemish for Natural Benefics",
        "sloka":          "ch34-lu-34.1",
        "group":          "lordship_principle",
        "condition_type": "general_principle",
        "formation":      (
            "A natural benefic planet (Jupiter, Venus, Mercury, or the Moon) owns "
            "one or more of the angular houses (1st, 4th, 7th, 10th). The ownership "
            "of angles by natural benefics produces the Kendradhipatya Dosha — the "
            "angular blemish — causing the planet to lose its benefic nature and "
            "give reduced or adverse results."
        ),
        "effect":         (
            "The natural benefic loses its benefic status due to angular lordship. "
            "Its normally good significations are diminished or obstructed. The "
            "stronger the angular ownership (especially 7th and 10th), the more "
            "pronounced the blemish. Exception: the 1st house is also a trine, "
            "which partially mitigates the dosha for lagna lords."
        ),
        "is_benefic":     False,
        "life_domains":   ["general", "benefic_planet_quality"],
        "yoga_check": {
            "type":      "manual",
            "checkable": False,
            "blockers":  ["L"],
            "description": (
                "Requires identifying which angular houses (1,4,7,10) a given natural "
                "benefic lords — depends on lagna-specific house lordship (L blocker)."
            ),
        },
    },
    {
        "yoga_name":      "Malefic Angular Rule — Natural Malefics Gain in Angles",
        "sloka":          "ch34-lu-34.2",
        "group":          "lordship_principle",
        "condition_type": "general_principle",
        "formation":      (
            "A natural malefic planet (Sun, Mars, or Saturn) owns one or more angular "
            "houses (1st, 4th, 7th, 10th). Unlike natural benefics, natural malefics "
            "are not harmed by angular lordship — they do not acquire the Kendradhipatya "
            "dosha. Angular lordship may even improve a malefic's results. However, a "
            "malefic becomes truly auspicious only when it also owns a trinal house (5th "
            "or 9th), forming a Rajayoga or Yogakaraka combination."
        ),
        "effect":         (
            "The natural malefic retains its strength without the angular blemish. It "
            "gives moderately improved results due to angular lordship but is not "
            "fully auspicious unless it also owns a trine. Pure angular lordship "
            "without trinal lordship makes the malefic less harmful but not benefic."
        ),
        "is_benefic":     True,
        "life_domains":   ["general", "malefic_planet_quality"],
        "yoga_check": {
            "type":      "manual",
            "checkable": False,
            "blockers":  ["L"],
            "description": (
                "Requires identifying whether the natural malefic lords an angular "
                "house — lagna-specific lordship computation (L blocker)."
            ),
        },
    },
    {
        "yoga_name":      "Trinal Lordship Rule — 5th and 9th Lords Are Always Auspicious",
        "sloka":          "ch34-lu-34.3",
        "group":          "lordship_principle",
        "condition_type": "general_principle",
        "formation":      (
            "A planet owns the 5th house (the Purva Punya trine — Lakshmisthana) "
            "or the 9th house (the Dharma trine — primary Lakshmisthana). Ownership "
            "of the 5th or 9th house always confers auspicious, wealth-giving status "
            "regardless of the planet's natural nature. This rule applies universally "
            "across all ascendants."
        ),
        "effect":         (
            "The planet gives auspicious, fortune-producing results during its Dasha "
            "periods. The 5th and 9th lords are the primary givers of Lakshmi "
            "(prosperity, divine grace) in any horoscope. The 9th lord is generally "
            "stronger than the 5th lord. Their positive results manifest regardless "
            "of the planet's natural malefic or benefic status."
        ),
        "is_benefic":     True,
        "life_domains":   ["wealth", "fortune", "dharma", "prosperity"],
        "yoga_check": {
            "type":      "manual",
            "checkable": False,
            "blockers":  ["L"],
            "description": "Requires identifying the 5th and 9th lords for the given ascendant (L blocker).",
        },
    },
    {
        "yoga_name":      "Evil House Engine — 3rd, 6th, 11th Lords Are Always Malefic",
        "sloka":          "ch34-lu-34.4",
        "group":          "lordship_principle",
        "condition_type": "general_principle",
        "formation":      (
            "A planet owns the 3rd, 6th, or 11th house. These are the Trishadaya "
            "houses — the houses of upachaya (increase/growth) that simultaneously "
            "indicate difficulties, enemies, disease, and material desires. Ownership "
            "of these houses always confers malefic status. The hierarchy of maleficence: "
            "11th (most evil) > 6th > 3rd (least evil)."
        ),
        "effect":         (
            "The planet gives evil, adverse results during its Dasha periods — "
            "creating enemies, illness, losses, or unfulfilled desires depending on "
            "the specific house lordship. The 11th lord is the most harmful, then "
            "the 6th, then the 3rd. These results manifest regardless of the "
            "planet's natural benefic or malefic status."
        ),
        "is_benefic":     False,
        "life_domains":   ["general", "evil_house_lordship"],
        "yoga_check": {
            "type":      "manual",
            "checkable": False,
            "blockers":  ["L"],
            "description": "Requires identifying the 3rd, 6th, 11th lords for the ascendant (L blocker).",
        },
    },
    {
        "yoga_name":      "Terminal House Logic — 2nd, 8th, 12th Lord Results by Association",
        "sloka":          "ch34-lu-34.5",
        "group":          "lordship_principle",
        "condition_type": "general_principle",
        "formation":      (
            "A planet owns the 2nd house (Marak/wealth), 8th house (longevity/death), "
            "or 12th house (liberation/loss). The results of these lordships are not "
            "fixed — they depend entirely on the planet's associations (conjunctions, "
            "aspects, placement). Exception: the Sun and Moon as 8th lords do not "
            "confer evil results from that lordship alone."
        ),
        "effect":         (
            "The 2nd lord becomes a Marak (death-inflicting) planet; its results "
            "depend on placement and associations. The 8th lord gives results based "
            "on whom it is associated with — good associations produce longevity and "
            "research abilities; evil associations harm these. The 12th lord governs "
            "expenditure and liberation — its nature depends on context. Sun and Moon "
            "as 8th lords are not inherently evil despite the evil-house lordship."
        ),
        "is_benefic":     None,
        "life_domains":   ["longevity", "wealth", "liberation", "general"],
        "yoga_check": {
            "type":      "manual",
            "checkable": False,
            "blockers":  ["L"],
            "description": (
                "Context-dependent rule; requires identifying 2nd/8th/12th lords and "
                "their associations (L + aspect/conjunction analysis)."
            ),
        },
    },
    {
        "yoga_name":      "Moolatrikona Priority — Dominant House When a Planet Lords Two",
        "sloka":          "ch34-lu-34.6",
        "group":          "lordship_principle",
        "condition_type": "general_principle",
        "formation":      (
            "A planet owns two houses (all planets except Sun and Moon own two signs). "
            "One of those houses contains the planet's Moolatrikona sign (the sign "
            "where it has special strength beyond mere rulership). The Moolatrikona "
            "house is the planet's primary house of ownership — its results manifest "
            "more strongly from that house's significations."
        ),
        "effect":         (
            "The house containing the planet's Moolatrikona sign predominates in "
            "determining the planet's quality for any ascendant. If the Moolatrikona "
            "house is a trine, the planet tends to be auspicious; if evil, malefic; "
            "if angle, the planet's angular nature is primary. This rule resolves "
            "conflicts when a planet lords both an auspicious and an inauspicious house."
        ),
        "is_benefic":     None,
        "life_domains":   ["general", "planet_strength"],
        "yoga_check": {
            "type":      "manual",
            "checkable": False,
            "blockers":  ["L"],
            "description": (
                "Requires knowing which house contains the planet's Moolatrikona sign "
                "for the given ascendant — lagna-specific computation (L blocker)."
            ),
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 2. GENERAL PRINCIPLES (LU 34.7–34.10)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":      "Planetary Stalling Logic — Mixed Lordship Produces Mixed Results",
        "sloka":          "ch34-lu-34.7",
        "group":          "general_principle",
        "condition_type": "general_principle",
        "formation":      (
            "A planet owns both an auspicious house (trine or angular without blemish) "
            "and an inauspicious house (evil house or Marak house) simultaneously. "
            "The two contradictory lordships 'stall' each other — neither the "
            "auspicious nor the malefic nature fully manifests."
        ),
        "effect":         (
            "The planet gives mixed results during its Dasha. The dominant quality "
            "depends on the planet's associations, placement, and strength. When "
            "associated with or aspected by natural benefics, the auspicious lordship "
            "predominates; when associated with natural malefics, the evil lordship "
            "prevails. Neither extreme (wholly good or wholly bad) manifests fully."
        ),
        "is_benefic":     None,
        "life_domains":   ["general"],
        "yoga_check": {
            "type":      "manual",
            "checkable": False,
            "blockers":  ["L"],
            "description": "Requires identifying house lordships for both houses owned by the planet (L blocker).",
        },
    },
    {
        "yoga_name":      "House Graduation Scales — Hierarchy of Angular and Trinal Houses",
        "sloka":          "ch34-lu-34.8",
        "group":          "general_principle",
        "condition_type": "general_principle",
        "formation":      (
            "Among the angular houses (Kendras): 10th > 7th > 4th > 1st in strength "
            "of angular power. Among the trinal houses (Trikonas): 9th > 5th > 1st "
            "in fortune-giving strength. The 1st house occupies a unique position "
            "as both an angle and a trine — it combines both types of power."
        ),
        "effect":         (
            "The 10th lord gives the strongest angular results; the 9th lord gives "
            "the strongest trinal/fortune results. When comparing two Yogakaraka "
            "planets (each owning one angle and one trine), the one whose angular "
            "lordship is a higher-ranked angle (closer to 10th) gives more powerful "
            "Rajayoga results. The 1st house lordship is moderate — both angular and "
            "trinal but weaker than the specialized houses."
        ),
        "is_benefic":     True,
        "life_domains":   ["status", "fortune", "general"],
        "yoga_check": {
            "type":      "manual",
            "checkable": False,
            "blockers":  ["L"],
            "description": "Interpretive scale applied during chart reading; no single-configuration check.",
        },
    },
    {
        "yoga_name":      "Counterpart Adversity Rule — Evil Lordship Qualifies Good Lordship",
        "sloka":          "ch34-lu-34.9",
        "group":          "general_principle",
        "condition_type": "general_principle",
        "formation":      (
            "A planet owns both a beneficial house and an evil house. The evil "
            "lordship introduces an adversity that qualifies and reduces the full "
            "expression of the beneficial lordship. Conversely, the good lordship "
            "also softens some of the evil. Both lordships modify each other in "
            "a bidirectional counterpart relationship."
        ),
        "effect":         (
            "The planet's beneficial results are tempered by its evil house lordship. "
            "For example, a 9th lord that also lords the 6th cannot give pure fortune "
            "results — the 6th (enemies, disease) introduces an obstacle or price "
            "for the 9th house blessings. Similarly, the evil house's worst effects "
            "are not fully expressed because the good lordship mitigates them. Final "
            "result depends on Moolatrikona house and planetary associations."
        ),
        "is_benefic":     None,
        "life_domains":   ["general"],
        "yoga_check": {
            "type":      "manual",
            "checkable": False,
            "blockers":  ["L"],
            "description": "Applied as a modifier in chart reading; requires full lordship analysis (L blocker).",
        },
    },
    {
        "yoga_name":      "Graduation of Natural Disposition — Natural Nature Amplifies Lordship",
        "sloka":          "ch34-lu-34.10",
        "group":          "general_principle",
        "condition_type": "general_principle",
        "formation":      (
            "A planet's inherent natural nature (natural benefic or natural malefic) "
            "amplifies the effect of its functional lordship quality. When a natural "
            "benefic also lords a trinal house (functionally benefic), the combination "
            "produces doubly good results. When a natural malefic also lords an evil "
            "house (functionally malefic), the combination is doubly harmful."
        ),
        "effect":         (
            "Natural benefic + functional benefic lordship → strongest positive Dasha "
            "results. Natural malefic + functional malefic lordship → strongest adverse "
            "results. Combinations where natural and functional natures oppose each other "
            "(natural benefic + evil lordship, natural malefic + good lordship) produce "
            "moderate results modified by the Kendradhipatya and related rules."
        ),
        "is_benefic":     None,
        "life_domains":   ["general"],
        "yoga_check": {
            "type":      "manual",
            "checkable": False,
            "blockers":  ["L"],
            "description": "Applied as a meta-modifier over functional lordship assessment; no direct automated check.",
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 3. RAJAYOGA / YOGAKARAKA RULES (LU 34.11–34.15)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":      "Rajayoga Relationship Triad — Angular and Trinal Lords Connect",
        "sloka":          "ch34-lu-34.11",
        "group":          "rajayoga_definition",
        "condition_type": "yoga_combination",
        "formation":      (
            "The lord of an angular house (1st, 4th, 7th, or 10th — Vishnusthanas) "
            "and the lord of a trinal house (1st, 5th, or 9th — Lakshmisthanas) "
            "establish one of three qualifying relationships: (1) conjunction — both "
            "planets in the same house; (2) mutual aspect — each planet aspects the "
            "other's house; (3) sign exchange (Parivartana) — each planet is placed "
            "in the other's sign. The 1st house is both angle and trine — its lord "
            "participates in either capacity."
        ),
        "effect":         (
            "A Rajayoga is formed. The native enjoys high status, authority, prosperity, "
            "and favourable circumstances — the degree depending on the specific lords "
            "involved (10th + 9th > 4th + 5th etc.) and their Varga dignity. Results "
            "manifest during the Dasha periods of either planet involved in the yoga."
        ),
        "is_benefic":     True,
        "life_domains":   ["status", "royalty", "prosperity", "leadership"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Conjunction branch: check whether the angular lord and trinal lord "
                "occupy the same house — standard house-position check. Mutual aspect "
                "and exchange branches require aspect detection and sign-exchange "
                "identification (A blocker for full coverage). Conjunction-only "
                "implementation is checkable immediately."
            ),
        },
    },
    {
        "yoga_name":      "Single-Planet Yogakaraka — Owns Both Angle and Trine",
        "sloka":          "ch34-lu-34.12",
        "group":          "rajayoga_definition",
        "condition_type": "yoga_combination",
        "formation":      (
            "A single planet simultaneously lords one angular house (1st, 4th, 7th, "
            "or 10th) AND one trinal house (1st, 5th, or 9th). This is only possible "
            "when a planet owns signs that fall in both an angle and a trine for the "
            "given ascendant. The planet is called a Yogakaraka — it embodies the "
            "Rajayoga principle within itself without requiring a second planet."
        ),
        "effect":         (
            "The Yogakaraka gives the most powerful auspicious results of any planet "
            "for that ascendant during its Dasha and Antardasha periods. It combines "
            "the power of Vishnu (angles) and Lakshmi (trines) in a single planet. "
            "Even if the Yogakaraka is a natural malefic (e.g., Saturn for Taurus or "
            "Libra), it overrides its natural malefic tendency and gives supremely "
            "good results."
        ),
        "is_benefic":     True,
        "life_domains":   ["status", "royalty", "prosperity", "general"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Check: does a single planet lord one house from {1,4,7,10} AND one "
                "house from {1,5,9} for the given ascendant? Requires house lord "
                "identification (L), but this is a straightforward lagna-table lookup "
                "once the lagna is known."
            ),
        },
    },
    {
        "yoga_name":      "Malefic Angular Auspiciousness Gate — Conditions for Malefic Angular Lords",
        "sloka":          "ch34-lu-34.13",
        "group":          "rajayoga_definition",
        "condition_type": "general_principle",
        "formation":      (
            "For a natural malefic (Sun, Mars, Saturn) to become truly auspicious "
            "through angular house lordship alone, two conditions must hold: (1) it "
            "must own the angular house without simultaneously owning an evil house "
            "(3rd, 6th, or 11th); (2) it must not own a Marak house (2nd or 7th) as "
            "its primary (Moolatrikona) house. Pure angular ownership without evil "
            "contamination is the gate to auspiciousness for natural malefics."
        ),
        "effect":         (
            "A natural malefic owning only an angular house (no evil house, no Marak "
            "house as primary) gives clearly auspicious results. When the angular "
            "malefic also owns an evil or Marak house, its auspiciousness is qualified "
            "or negated. This gate determines whether the malefic angular rule (LU 34.2) "
            "fully applies or is blocked."
        ),
        "is_benefic":     True,
        "life_domains":   ["general", "malefic_planet_quality"],
        "yoga_check": {
            "type":      "manual",
            "checkable": False,
            "blockers":  ["L"],
            "description": "Requires full house lordship analysis for the specific lagna and planet (L blocker).",
        },
    },
    {
        "yoga_name":      "Evil House Rajayoga Obstruction — 3rd/6th/11th Lordship Blocks Rajayoga",
        "sloka":          "ch34-lu-34.14",
        "group":          "rajayoga_definition",
        "condition_type": "yoga_combination",
        "formation":      (
            "An angular lord or trinal lord also owns an evil house (3rd, 6th, or 11th). "
            "The evil house lordship contaminates the Rajayoga potential of the good "
            "lordship. Even if this planet connects with another angular or trinal lord "
            "(via conjunction, aspect, or exchange), the full Rajayoga does not form "
            "because the evil house lordship obstructs it."
        ),
        "effect":         (
            "The Rajayoga is blocked or significantly diminished. The native may have "
            "some elevation in status but the results are mixed with adversity, enemies, "
            "or obstacles tied to the evil house lordship. The intensity of obstruction "
            "is proportional to the evil house rank: 11th obstructs most, then 6th, "
            "then 3rd. Exception: if the planet is also a Yogakaraka (owns angle + trine), "
            "the Yogakaraka status partially overrides this obstruction."
        ),
        "is_benefic":     False,
        "life_domains":   ["status", "general"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Check: does the planet in question (angular or trinal lord) also lord "
                "an evil house (3rd, 6th, or 11th)? Requires lagna-specific house "
                "lordship lookup (L). Once the lordship table is available, this is "
                "a straightforward set-membership check."
            ),
        },
    },
    {
        "yoga_name":      "Node Rajayoga Trigger — Rahu/Ketu Absorb Rajayoga Through Placement",
        "sloka":          "ch34-lu-34.15",
        "group":          "rajayoga_definition",
        "condition_type": "yoga_combination",
        "formation":      (
            "Rahu or Ketu (the lunar nodes) are placed in a house owned by a Rajayoga-"
            "forming planet, or in a sign whose lord is forming a Rajayoga. The nodes "
            "absorb the Rajayoga power of the sign lord through their placement and "
            "transmit it during their own Dasha periods. Additionally, if Rahu or Ketu "
            "conjoins a Yogakaraka planet, the node also participates in the Rajayoga."
        ),
        "effect":         (
            "The node (Rahu or Ketu) acts as a proxy Rajayoga planet during its "
            "Mahadasha or Antardasha, delivering elevated status, recognition, and "
            "power similar to the Rajayoga planet it mirrors. This is the basis for "
            "Rahu Dasha producing unexpected career peaks when Rahu is in the house "
            "of a Yogakaraka or Rajayoga lord."
        ),
        "is_benefic":     True,
        "life_domains":   ["status", "career", "recognition"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Check: is Rahu or Ketu placed in a house owned by a planet that "
                "qualifies as a Rajayoga lord (angular + trinal connection) or "
                "Yogakaraka? Requires planetary position lookup + lordship "
                "identification (L). House-position check is straightforward once "
                "lordship tables are built."
            ),
        },
    },
]


# ── Build lagna-planet rules ──────────────────────────────────────────────────

def _build_lagna_rules() -> list[dict]:
    rules = []
    for lagna, planets in LAGNA_QUALITY_TABLE.items():
        for planet, data in planets.items():
            quality = data["quality"]
            houses  = data["houses"]
            note    = data["note"]
            extra   = data.get("extra_label")  # e.g. "killer" for dual-label rules

            house_str = " and ".join(
                [f"{h}th" if h not in (1,) else "1st" for h in houses]
            )
            quality_label = QUALITY_LABELS[quality]
            if extra:
                quality_label = f"{quality_label} + {QUALITY_LABELS[extra]}"

            yoga_name = f"{planet} for {lagna} Ascendant — {quality_label}"

            formation = (
                f"For {lagna} ascendant, {planet} lords the {note.split(';')[0].split('.')[0].strip()}"
                f". {note}"
            )

            base_effect = QUALITY_EFFECTS[quality]
            if extra:
                base_effect = base_effect + " " + QUALITY_EFFECTS[extra]

            effect = (
                f"{planet} is classified as {quality_label} for {lagna} ascendant. "
                f"{base_effect}"
            )

            life_domains = ["lagna_planet_quality", lagna.lower(), planet.lower()]

            rules.append({
                "yoga_name":      yoga_name,
                "sloka":          f"ch34-lagna-{lagna.lower()}",
                "group":          "lagna_planet_quality",
                "condition_type": "lagna_planet_quality",
                "formation":      formation,
                "effect":         effect,
                "is_benefic":     quality in ("auspicious", "yogakaraka"),
                "life_domains":   life_domains,
                "yoga_check": {
                    "type":      "manual",
                    "checkable": False,
                    "blockers":  ["L"],
                    "description": (
                        f"Lagna-specific quality classification for {planet} in {lagna} ascendant. "
                        f"Requires lagna identification and house lordship table (L blocker). "
                        f"Phase 2: lagna_planet_quality evaluator will automate this once "
                        f"lagna-specific lordship tables are built."
                    ),
                },
            })
    return rules


# ── Yoga data = non-lagna rules + lagna rules ─────────────────────────────────

YOGA_DATA: list[dict] = NON_LAGNA_RULES + _build_lagna_rules()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_summary(effect: str, max_chars: int = 250) -> str:
    if not effect:
        return ""
    if len(effect) <= max_chars:
        return effect
    chunk = effect[:max_chars]
    last_dot = chunk.rfind(". ")
    if last_dot > 60:
        return effect[:last_dot + 1]
    return chunk


# ── Rule builder ──────────────────────────────────────────────────────────────

def build_rule(yoga: dict, index: int) -> dict:
    rule_id      = f"bphs-ch34-{index:03d}"
    yoga_name    = yoga["yoga_name"]
    sloka        = yoga.get("sloka", "")
    group        = yoga.get("group", "lordship_principle")
    is_benefic   = yoga.get("is_benefic", None)
    life_domains = yoga.get("life_domains", [])
    formation    = yoga.get("formation", "")
    effect       = yoga.get("effect", "")
    yoga_check   = yoga.get("yoga_check", {})
    cond_type    = yoga.get("condition_type", "general_principle")
    checkable    = yoga_check.get("checkable", False)

    group_lbl = {
        "lordship_principle":  "Lordship Principle",
        "general_principle":   "General Principle",
        "rajayoga_definition": "Rajayoga / Yogakaraka Definition",
        "lagna_planet_quality": "Lagna Planet Quality Profile",
    }.get(group, "Lordship Rule")

    detailed = f"Formation: {formation}\n\nEffect: {effect}".strip()
    tags = ["lordship", f"group:{group}"]
    if checkable:
        tags.append("yoga_checkable")

    return {
        "rule_id":         rule_id,
        "science_id":      SCIENCE,
        "source": {
            "book":           BOOK,
            "book_id":        BOOK_ID,
            "chapter":        CHAPTER,
            "chapter_name":   CHAP_NAME,
            "sloka":          sloka,
            "batch_id":       BATCH_ID,
            "primary":        BOOK,
            "page_ref":       None,
            "passage_ref_id": None,
        },
        "condition": {
            "type":               cond_type,
            "sub_type":           "lordship_quality",
            "yoga_name":          yoga_name,
            "yoga_group":         group,
            "yoga_group_label":   group_lbl,
            "planets_involved":   [],
            "houses_involved":    [],
            "sub_conditions":     [],
            "operator":           "and",
            "gender_context":     "neutral",
            "condition_group_id": f"bphs-ch34-{group}",
            "is_group_summary":   False,
            "is_benefic":         is_benefic,
            "yoga_check":         yoga_check,
        },
        "interpretation": {
            "summary":            _make_summary(effect),
            "detailed":           detailed,
            "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
            "remedies":           [],
            "life_domain":        life_domains[0] if life_domains else "general",
            "life_domains":       life_domains,
            "tags":               tags,
            "physical_markers":   [],
        },
        "metadata": {
            "planets_involved":     [],
            "houses_involved":      [],
            "signs_involved":       [],
            "condition_count":      1,
            "gender_context":       "neutral",
            "condition_group_id":   f"bphs-ch34-{group}",
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
        "created_at":      datetime.now(timezone.utc).isoformat(),
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest BPHS Ch 34 Nature of Planets Due to Lordship"
    )
    parser.add_argument("--dry-run",  action="store_true",
                        help="Build rules and print summary without writing")
    parser.add_argument("--save",     metavar="PATH",
                        help="Save dry-run JSON to file")
    parser.add_argument("--upload",   metavar="PATH",
                        help="Upload rules from saved JSON (zero API calls)")
    parser.add_argument("--mongo-url", default="mongodb://localhost:27017")
    parser.add_argument("--db-name",   default="horoscope_db")
    args = parser.parse_args()

    # ── Upload path ──────────────────────────────────────────────────────────
    if args.upload:
        from pymongo import MongoClient
        path = Path(args.upload)
        if not path.exists():
            print(f"ERROR: file not found: {path}", file=sys.stderr)
            sys.exit(1)
        with open(path) as f:
            rules = json.load(f)
        client = MongoClient(args.mongo_url)
        coll = client[args.db_name]["interpretation_rules"]
        result = coll.insert_many(rules)
        print(f"✅ Uploaded {len(result.inserted_ids)} rules to "
              f"{args.db_name}.interpretation_rules")
        print(f"   Batch ID: {BATCH_ID}")
        print(f"\nNext step — validate:")
        print(f"   python3 scripts/validate_rules.py "
              f"--mongo-url $MONGO_URL --db-name {args.db_name} "
              f"--batch-id {BATCH_ID}")
        client.close()
        return

    # ── Build rules ──────────────────────────────────────────────────────────
    rules = [build_rule(y, i + 1) for i, y in enumerate(YOGA_DATA)]

    # ── Summary ──────────────────────────────────────────────────────────────
    checkable_rules = [r for r in rules if r["metadata"]["yoga_checkable"]]
    total = len(rules)

    print(f"\nBPHS Ch {CHAPTER} — {CHAP_NAME}")
    print(f"  Total rules  : {total}")
    print(f"  Checkable    : {len(checkable_rules)} / {total} "
          f"({100 * len(checkable_rules) // total if total else 0}%)")
    print(f"  Batch ID     : {BATCH_ID}")

    groups: dict[str, int] = {}
    for r in rules:
        g = r["condition"]["yoga_group"]
        groups[g] = groups.get(g, 0) + 1
    print("\n  Groups:")
    for g, n in groups.items():
        lbl = {
            "lordship_principle":   "Lordship Principle",
            "general_principle":    "General Principle",
            "rajayoga_definition":  "Rajayoga / Yogakaraka Definition",
            "lagna_planet_quality": "Lagna Planet Quality Profile",
        }.get(g, g)
        print(f"    {lbl:<42} {n} rules")

    print("\n  Non-lagna rules (checkable status):")
    for r in rules:
        if r["condition"]["yoga_group"] == "lagna_planet_quality":
            continue
        yc = r["condition"]["yoga_check"]
        mark = "✅" if yc.get("checkable") else "❌"
        blockers = yc.get("blockers", [])
        print(f"    {r['rule_id']}  [{mark}]  "
              f"{r['condition']['yoga_name'][:55]}"
              f"  blockers={blockers}")

    print("\n  Lagna planet quality rules by lagna:")
    lagna_counts: dict[str, int] = {}
    for r in rules:
        if r["condition"]["yoga_group"] != "lagna_planet_quality":
            continue
        sloka = r["source"]["sloka"]
        lagna = sloka.replace("ch34-lagna-", "").capitalize()
        lagna_counts[lagna] = lagna_counts.get(lagna, 0) + 1
    for lagna, n in lagna_counts.items():
        print(f"    {lagna:<15} {n} planets")

    if args.dry_run and not args.save:
        print("\n  [dry-run only — use --save to write JSON]")
        return

    # ── Save ─────────────────────────────────────────────────────────────────
    out_path = Path(args.save) if args.save else None
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(rules, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"\n✅ Saved {total} rules → {out_path}")
        print(f"\nNext step — review {out_path}, then upload:")
        print(f"   python3 scripts/ingest_bphs_ch34_v1.py \\")
        print(f"     --upload {out_path} --mongo-url $MONGO_URL --db-name {args.db_name}")

    if args.dry_run:
        print("\n  [dry-run complete]")


if __name__ == "__main__":
    main()
