#!/usr/bin/env python3
"""
ingest_lalkitab_ch23_v1.py — Lal Kitab Chapter 23: House Construction & Family Prosperity

31 rules total across 6 groups:
   12  Saturn-House construction rules  (saturn-h1 through saturn-h12) — all 12
    6  Geometric veto rules             (structural-right-angle + 5 shape doshas)
    3  Formula / spatial rules          (formula-remainder, spatial-distribution,
                                          structural-dead-end)
    2  Internal layout rules            (layout-entrance, layout-corner-map)
    4  Diagnostic / environmental       (diag-moon-pot, diag-secret-pits,
                                          env-peepal-shadow, diag-danger-gate)
    4  Refinement + protocol rules      (env-bhatti-mars-h8, refine-uncle-veto,
                                          refine-idol-veto, timing-pushya)

Sources:
  Primary:    Lal Kitab Ch 23 JSON Ready (V6)
  Additional: Lal Kitab_Ch23_House construction_Additional info.md
              (fills Saturn H2/H3/H6/H7/H8/H10/H11/H12, geometric vetoes,
               layout paradigm, refinement vetoes, danger gate)
  Diagnostic: Lal Kitab Ch 23 Diagnostic file

Note on formula-remainder: Additional info provides specific per-remainder outcomes
(all 8 remainders) and corrects the original file's remedy references.

BATCH_ID = "lalkitab-ch23-v1-20260504"

Standard workflow:
  Step 1 — Dry run + save:
    python3 scripts/ingest_lalkitab_ch23_v1.py --dry-run \\
      --save scripts/lalkitab_ch23_rules.json

  Step 2 — Review JSON; amend as needed.

  Step 3 — Upload:
    python3 scripts/ingest_lalkitab_ch23_v1.py \\
      --upload scripts/lalkitab_ch23_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 4 — Validate:
    python3 scripts/validate_rules.py \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id lalkitab-ch23-v1-20260504
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCIENCE   = "jyotish"
BOOK      = "Lal Kitab"
BOOK_ID   = "lal-kitab"
CHAPTER   = 23
CHAP_NAME = "House Construction and Family Prosperity"
BATCH_ID  = "lalkitab-ch23-v1-20260504"


def _base(rule_id: str, now: str) -> dict:
    return {
        "rule_id":    rule_id,
        "science_id": SCIENCE,
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
        "approval_status": "pending_review",
        "created_at":      now,
    }


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: Saturn-House Construction Engine — All 12 Houses
# ─────────────────────────────────────────────────────────────────────────────

SATURN_HOUSE_RULES = [
    {
        "house": 1,
        "name":  "Saturn in H1 — The Ruin Rule",
        "text": (
            "If Saturn is in the 1st house and the native builds or arranges to build "
            "a house, the outcome is poverty and total ruin. Exception: if no planets "
            "occupy both the 7th and 10th houses simultaneously, construction becomes "
            "auspicious — the ruin rule activates only when H7 or H10 is occupied."
        ),
        "remedies": [],
        "tags":     ["saturn", "h1", "ruin", "poverty", "construction"],
        "source":   "JSON Ready V6 — Logic Unit 23.1",
    },
    {
        "house": 2,
        "name":  "Saturn in H2 — Venus Sign (Auspicious Construction)",
        "text": (
            "Saturn in the 2nd house is a Venus sign placement for construction "
            "purposes. The native may build however they wish — the house will bestow "
            "good effects only. This is one of the fully auspicious Saturn positions "
            "for house construction with no restrictions."
        ),
        "remedies": [],
        "tags":     ["saturn", "h2", "auspicious", "venus_sign", "construction"],
        "source":   "Additional Info — Saturn House Rules H02",
    },
    {
        "house": 3,
        "name":  "Saturn in H3 — Mercury Enmity (Three Dogs Remedy)",
        "text": (
            "Saturn in the 3rd house creates Mercury Enmity — both Saturn and Mercury "
            "are rendered 'impotent' in this configuration, making standard construction "
            "problematic. Remedy: keep three dogs as pets before and during construction "
            "to facilitate the building process and neutralize the enmity."
        ),
        "remedies": [
            {"text": "Keep three dogs as pets before and during the construction period.", "category": "ritual"},
        ],
        "tags":     ["saturn", "h3", "mercury_enmity", "three_dogs", "construction"],
        "source":   "Additional Info — Saturn House Rules H03",
    },
    {
        "house": 4,
        "name":  "Saturn in H4 — In-Law Affliction (Foundation Veto)",
        "text": (
            "Saturn in the 4th house creates enmity with the Moon. Starting to dig "
            "the foundation brings immediate trouble and problems to the maternal "
            "grandfather and in-laws. The Lal Kitab instruction is: do not build "
            "your own house with this placement."
        ),
        "remedies": [],
        "tags":     ["saturn", "h4", "in_laws", "foundation", "veto", "construction"],
        "source":   "JSON Ready V6 — Logic Unit 23.4 + Additional Info H04",
    },
    {
        "house": 5,
        "name":  "Saturn in H5 — Son's Penalty (Age 48 + Buffalo Remedy)",
        "text": (
            "Saturn in the 5th house: building a house causes an ill effect on the "
            "son. Exception: if the son himself builds the house, the outcome is "
            "auspicious. If the native must build: wait until the native reaches age "
            "48 AND bring a buffalo, mark it, and feed it before starting construction."
        ),
        "remedies": [
            {"text": "Wait until age 48. Before starting: bring a buffalo, mark it, and feed it.", "category": "ritual"},
            {"text": "Allow the son to build the house himself — fully negates the ill effect.", "category": "succour"},
        ],
        "tags":     ["saturn", "h5", "son", "age_48", "buffalo", "construction"],
        "source":   "JSON Ready V6 — Logic Unit 23.5 + Additional Info H05",
    },
    {
        "house": 6,
        "name":  "Saturn in H6 — Virgo (Age 39 Rule, Daughter's Relatives)",
        "text": (
            "Saturn in the 6th house (Virgo-friendly sign): the native should build "
            "only after reaching the age of 39. Building before age 39 ruins the "
            "daughter's relatives (the family of married daughters). After age 39, "
            "construction proceeds without this penalty."
        ),
        "remedies": [],
        "tags":     ["saturn", "h6", "age_39", "daughters", "virgo", "construction"],
        "source":   "Additional Info — Saturn House Rules H06",
    },
    {
        "house": 7,
        "name":  "Saturn in H7 — Threshold Rule (Ready-Made Houses Favorable)",
        "text": (
            "Saturn in the 7th house: ready-made (pre-built) houses are favorable for "
            "the native to buy and occupy. If the native is selling a house, they must "
            "keep the oldest threshold (chaukhat — the door frame) to ensure future "
            "construction capacity is retained."
        ),
        "remedies": [
            {"text": "When selling a house: retain the oldest threshold (chaukhat) — do not sell it with the property.", "category": "ritual"},
        ],
        "tags":     ["saturn", "h7", "threshold", "chaukhat", "ready_made", "construction"],
        "source":   "Additional Info — Saturn House Rules H07",
    },
    {
        "house": 8,
        "name":  "Saturn in H8 — Death Veto (Scorpio / Mars Sign)",
        "text": (
            "Saturn in the 8th house (Scorpio/Mars sign) is the most severe construction "
            "veto. Death starts to circle the native the moment building begins. The "
            "specific death effects vary depending on the positions of Rahu and Ketu in "
            "the chart — their house placements determine who in the family is affected "
            "and the timeline of the crisis."
        ),
        "remedies": [],
        "tags":     ["saturn", "h8", "death_veto", "scorpio", "mars_sign", "construction"],
        "source":   "Additional Info — Saturn House Rules H08",
    },
    {
        "house": 9,
        "name":  "Saturn in H9 — Father's Penalty (Pregnancy Trigger)",
        "text": (
            "Saturn in the 9th house: construction should begin ONLY when the wife or "
            "mother is pregnant — this is the auspicious trigger. Warning: building "
            "from the native's own earnings without this trigger causes the father's "
            "death with certainty upon completion of the 3rd house (third room or floor)."
        ),
        "remedies": [],
        "tags":     ["saturn", "h9", "father", "pregnancy_trigger", "death", "construction"],
        "source":   "JSON Ready V6 — Logic Unit 23.9 + Additional Info H09",
    },
    {
        "house": 10,
        "name":  "Saturn in H10 — Money Trap (Earns Until Building Begins)",
        "text": (
            "Saturn in the 10th house creates a money trap: the native earns well "
            "until the moment house construction begins, then becomes poor. If Saturn "
            "is additionally weak in the chart, the house remains permanently "
            "incomplete — the native cannot finish what they started."
        ),
        "remedies": [],
        "tags":     ["saturn", "h10", "poverty", "money_trap", "incomplete", "construction"],
        "source":   "Additional Info — Saturn House Rules H10",
    },
    {
        "house": 11,
        "name":  "Saturn in H11 — Age Veto (Build After 55, South Entrance Warning)",
        "text": (
            "Saturn in the 11th house: the native should build only after reaching "
            "age 55. An additional specific warning: if the house has a south-facing "
            "main entrance, this leads to poor health and a painful death. Avoid "
            "south-facing construction with this placement regardless of age."
        ),
        "remedies": [],
        "tags":     ["saturn", "h11", "age_55", "south_entrance", "health", "construction"],
        "source":   "Additional Info — Saturn House Rules H11",
    },
    {
        "house": 12,
        "name":  "Saturn in H12 — Rectangular Rule (Auspicious Without Desire)",
        "text": (
            "Saturn in the 12th house: the native builds the house without true desire "
            "or emotional attachment — yet the results are auspicious. Even if the Sun "
            "is present in the chart, the native should not stop or abandon the "
            "construction once started. Completing it brings positive outcomes."
        ),
        "remedies": [],
        "tags":     ["saturn", "h12", "auspicious", "rectangular", "no_desire", "construction"],
        "source":   "Additional Info — Saturn House Rules H12",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: Geometric Veto Rules (6 — right-angle + 5 shape doshas)
# ─────────────────────────────────────────────────────────────────────────────

GEOMETRIC_RULES = [
    {
        "rule_id": "lalkitab-ch23-structural-right-angle",
        "name":    "Right-Angle Structure — Four 90° Corners as Gold Standard",
        "sub_type": "structural",
        "text": (
            "A house with four right angles (90-degree corners) is the gold standard "
            "for auspiciousness in Lal Kitab construction logic. Any non-rectangular "
            "shape — octagon, pentagon, polygon, triangle, or fish-belly — carries a "
            "specific familial penalty defined by the deviated angle. Only four "
            "right-angle construction is recommended."
        ),
        "remedies": [],
        "tags":    ["right_angle", "structural_safety", "rectangle", "vastu", "gold_standard"],
        "source":  "Diagnostic file + Additional Info — geometric vetoes",
    },
    {
        "rule_id": "lalkitab-ch23-geoveto-octagon",
        "name":    "Octagon Plot — Disease Dosha",
        "sub_type": "structural",
        "text": (
            "Building on or in an octagonal (8-sided) plot or constructing an "
            "octagonal house is inauspicious. The outcome is disease for family members. "
            "Avoid octagonal plot shapes entirely for residential construction."
        ),
        "remedies": [],
        "tags":    ["octagon", "disease", "structural_dosha", "vastu"],
        "source":  "Additional Info — geometric vetoes 02",
    },
    {
        "rule_id": "lalkitab-ch23-geoveto-polygon",
        "name":    "18-Sided Polygon Plot — Gold and Silver Destruction Dosha",
        "sub_type": "structural",
        "text": (
            "Building on an 18-sided polygon plot results in destruction of gold, "
            "silver, and jewelry belonging to the family. Accumulated wealth in "
            "precious metals is systematically lost when the native lives in a "
            "polygon-shaped structure."
        ),
        "remedies": [],
        "tags":    ["polygon", "gold_silver", "wealth_destruction", "structural_dosha", "vastu"],
        "source":  "Additional Info — geometric vetoes 03",
    },
    {
        "rule_id": "lalkitab-ch23-geoveto-triangle",
        "name":    "Triangular (13-Sided) Plot — Brothers' Trouble and Death Dosha",
        "sub_type": "structural",
        "text": (
            "Building on a triangular or 13-sided plot causes trouble for brothers, "
            "leading to punishment and death. The triangular form creates a Mars-like "
            "aggression that is directed at the native's fraternal relationships."
        ),
        "remedies": [],
        "tags":    ["triangle", "brothers", "death", "structural_dosha", "vastu"],
        "source":  "Additional Info — geometric vetoes 04",
    },
    {
        "rule_id": "lalkitab-ch23-geoveto-pentagon",
        "name":    "Pentagon Plot — Son's Doom Dosha",
        "sub_type": "structural",
        "text": (
            "Building on a pentagonal (5-sided) plot causes trouble to the son and "
            "brings doom to the progeny channel. The pentagon shape specifically "
            "afflicts the 5th house domain — children and intelligence — of the "
            "occupying family."
        ),
        "remedies": [],
        "tags":    ["pentagon", "son", "doom", "structural_dosha", "vastu"],
        "source":  "Additional Info — geometric vetoes 05",
    },
    {
        "rule_id": "lalkitab-ch23-geoveto-fish-belly",
        "name":    "Fish-Belly Plot — Childlessness Across Three Generations Dosha",
        "sub_type": "structural",
        "text": (
            "Building on a fish-belly shaped plot (wider in the middle, narrowing at "
            "both ends) results in childlessness and trouble across three generations. "
            "This is the most severe geometric veto — the affliction persists not just "
            "for the native but for the next three family generations."
        ),
        "remedies": [],
        "tags":    ["fish_belly", "childlessness", "three_generations", "structural_dosha", "vastu"],
        "source":  "Additional Info — geometric vetoes 06",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: Formula, Spatial, Structural Rules
# ─────────────────────────────────────────────────────────────────────────────

FORMULA_RULES = [
    {
        "rule_id":   "lalkitab-ch23-formula-remainder",
        "name":      "Remainder Formula — (L+B)×3÷8 Complete Vibe Diagnostic",
        "type":      "general_principle",
        "sub_type":  "construction",
        "checkable": False,
        "yoga_type": "manual",
        "yoga_desc": "Calculated formula — requires length and breadth of the proposed house plot.",
        "planets":   [],
        "houses":    [],
        "text": (
            "Construction auspiciousness formula: (Length + Breadth) × 3 ÷ 8. "
            "Evaluate the remainder for the house's 'vibe':\n"
            "Remainder 1 — Royal Honor: Jupiter in H1 energy. Excellent.\n"
            "Remainder 2 — Poverty: Jupiter in H6. Native faces financial hardship.\n"
            "Remainder 3 — Lion's Den: Mars in H3. Good for trade; bad for children.\n"
            "Remainder 4 — Starvation: Moon in H4. Two meals difficult to earn daily.\n"
            "Remainder 5 — Peace: Sun in H5. Wife and children get happiness.\n"
            "Remainder 6 — Directionless: Sun in H6. Loss of happiness.\n"
            "Remainder 7 — Excellent: Venus in H7. Best outcome.\n"
            "Remainder 8 — Death Dwelling: Mars + Saturn in H8. Extreme inauspicious.\n"
            "Auspicious: 1, 3 (trade only), 5, 7. "
            "Inauspicious: 2, 4, 6, 8."
        ),
        "remedies": [
            {"text": "Remainder 2 (Poverty — Jupiter H6): perform Jupiter-strengthening remedy.", "category": "succour"},
            {"text": "Remainder 4 (Starvation — Moon H4): perform Moon + Saturn remedy.", "category": "succour"},
            {"text": "Remainder 8 (Death — Mars+Saturn H8): perform Mars + Venus remedy.", "category": "succour"},
        ],
        "domains":   ["property", "vastu", "timing"],
        "tags":      ["formula", "remainder", "construction", "vastu", "calculation"],
        "source":    "JSON Ready V6 — Logic Unit 23.13 + Additional Info mathematical_validation_walls",
    },
    {
        "rule_id":   "lalkitab-ch23-spatial-distribution",
        "name":      "Spatial Distribution — H1–9 Right Side, H10–12 Left Side, H7 Master",
        "type":      "general_principle",
        "sub_type":  "construction",
        "checkable": False,
        "yoga_type": "manual",
        "yoga_desc": "Requires natal chart + house-to-physical-space mapping.",
        "planets":   [],
        "houses":    list(range(1, 13)),
        "text": (
            "Planets in houses 1–9 affect the right-hand side of the house at the "
            "entrance. Planets in houses 10–12 affect the left-hand side. "
            "House 7 acts as the master indicator for the home's overall joy, sorrow, "
            "and general situation — it is the primary house to examine when assessing "
            "a built home's character."
        ),
        "remedies":  [],
        "domains":   ["property", "vastu", "spatial"],
        "tags":      ["spatial_distribution", "h7_master", "right_left", "vastu"],
        "source":    "Diagnostic file + Additional Info — right vs left paradigm",
    },
    {
        "rule_id":   "lalkitab-ch23-structural-dead-end",
        "name":      "Dead-End Lane / Street Air — Structural Dosha",
        "type":      "dosha",
        "sub_type":  "structural",
        "checkable": False,
        "yoga_type": "manual",
        "yoga_desc": "Spatial/environmental — requires physical inspection of house location.",
        "planets":   [],
        "houses":    [],
        "text": (
            "A structural dosha arises when the house is the last house of a lane "
            "(dead-end position) OR when air blows directly from the street into "
            "the house. Both conditions cause problems for children and wife, "
            "including blindness, joint pain, or remaining unmarried."
        ),
        "remedies":  [],
        "domains":   ["property", "vastu", "family", "health"],
        "tags":      ["dead_end", "structural_dosha", "vastu", "street_air"],
        "source":    "JSON Ready V6 — Logic Unit 23.14",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: Internal Layout Rules
# ─────────────────────────────────────────────────────────────────────────────

LAYOUT_RULES = [
    {
        "rule_id":   "lalkitab-ch23-layout-entrance",
        "name":      "Main Entrance Direction — East Best, South Lethal for Females",
        "type":      "general_principle",
        "sub_type":  "structural",
        "checkable": False,
        "yoga_type": "manual",
        "yoga_desc": "Architectural inspection — direction of main entrance.",
        "text": (
            "Directional outcomes for the main house entrance:\n"
            "East — Excellent; total joy for the family.\n"
            "West — Second best; generally good.\n"
            "North — Superb; happy journey through life.\n"
            "South — Jinxed and lethal specifically for females in the household. "
            "A south-facing main entrance should be avoided, especially when Saturn "
            "is in H11."
        ),
        "remedies":  [],
        "domains":   ["property", "vastu", "family"],
        "tags":      ["entrance_direction", "south_facing", "vastu", "layout"],
        "source":    "Additional Info — internal_layout_paradigm main_entrance",
    },
    {
        "rule_id":   "lalkitab-ch23-layout-corner-map",
        "name":      "Poonya Corner Map — Room Assignment by Direction",
        "type":      "general_principle",
        "sub_type":  "structural",
        "checkable": False,
        "yoga_type": "manual",
        "yoga_desc": "Architectural layout — directional room placement within the house.",
        "text": (
            "Lal Kitab Poonya corner map for room assignment by compass direction:\n"
            "Northeast — Water storage and Worship/Prayer room.\n"
            "Southeast — Kitchen (Fire element).\n"
            "Southwest — Wealth storage / Treasure room.\n"
            "Northwest — Guest Room.\n"
            "West — Drawing Room / Reception.\n"
            "East — Sitting Room / Main living area."
        ),
        "remedies":  [],
        "domains":   ["property", "vastu", "spatial"],
        "tags":      ["poonya_corner", "room_layout", "vastu", "directions"],
        "source":    "Additional Info — internal_layout_paradigm poonya_corner_map",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: Diagnostic + Environmental Rules
# ─────────────────────────────────────────────────────────────────────────────

DIAGNOSTIC_RULES = [
    {
        "rule_id":   "lalkitab-ch23-diag-moon-pot",
        "name":      "Moon Pot Remedy — Illness / Court Cases During Construction",
        "type":      "dosha",
        "sub_type":  "structural",
        "checkable": False,
        "yoga_type": "behavioral",
        "planets":   ["Moon"],
        "houses":    [],
        "text": (
            "Diagnostic: if the native or family members suffer illness, court cases, "
            "or public infamy during house construction, a 'Moon Pot' (sealed pot with "
            "Moon-associated items) must be buried for exactly 40 days, then drowned "
            "in running water to remove the unfavorable effect."
        ),
        "remedies": [
            {"text": "Bury a Moon Pot for exactly 40 days during construction; drown it in running water.", "category": "ritual"},
        ],
        "domains":   ["property", "health", "legal"],
        "tags":      ["moon_pot", "construction", "diagnosis", "court_cases"],
        "source":    "Diagnostic file — symptom-to-remedy / Additional Info Moon Pot Test",
    },
    {
        "rule_id":   "lalkitab-ch23-diag-secret-pits",
        "name":      "Secret Pits — Useless Talk Diagnostic",
        "type":      "dosha",
        "sub_type":  "structural",
        "checkable": False,
        "yoga_type": "behavioral",
        "planets":   [],
        "houses":    [],
        "text": (
            "Diagnostic: if the native habitually talks uselessly (excessive idle "
            "speech), secret empty pits exist somewhere in the house. Empty pits "
            "meant for wealth storage that have been left unfilled trigger this "
            "condition. Remedy: fill the pits with almonds, dates (or sweets), "
            "and bury with earth."
        ),
        "remedies": [
            {"text": "Locate secret pits in the house; fill completely with almonds, dates or sweets, and earth.", "category": "ritual"},
        ],
        "domains":   ["property", "vastu", "mind"],
        "tags":      ["secret_pits", "useless_talk", "vastu", "diagnosis"],
        "source":    "Diagnostic file + Additional Info — Secret Pit Anchor",
    },
    {
        "rule_id":   "lalkitab-ch23-env-peepal-shadow",
        "name":      "Peepal Tree Shadow — House Doomed if Shadow Falls on Home",
        "type":      "dosha",
        "sub_type":  "structural",
        "checkable": False,
        "yoga_type": "manual",
        "planets":   [],
        "houses":    [],
        "text": (
            "If the shadow of a Peepal tree falls on the house at any time of day, "
            "the area is considered doomed. Remedies: "
            "(A) Water the Peepal tree's roots AND pour milk into a nearby well; OR "
            "(B) Water a Keekar tree every Saturday before dawn for 40 consecutive Saturdays."
        ),
        "remedies": [
            {"text": "Path A: Water the Peepal tree roots AND pour milk into a nearby well.", "category": "ritual"},
            {"text": "Path B: Water a Keekar tree every Saturday before dawn for 40 consecutive Saturdays.", "category": "ritual"},
        ],
        "domains":   ["property", "vastu", "environment"],
        "tags":      ["peepal_tree", "shadow", "doomed", "keekar", "vastu"],
        "source":    "Diagnostic file — environmental remediation",
    },
    {
        "rule_id":   "lalkitab-ch23-diag-danger-gate",
        "name":      "Immediate Danger Gate — Saturn H4/H8 + Foundation Dug",
        "type":      "planetary_combination",
        "sub_type":  "construction",
        "checkable": True,
        "yoga_type": "planet_in_house",
        "yoga_desc": "Saturn in H4 or H8 (natal) — triggers on act of digging foundation.",
        "planets":   ["Saturn"],
        "houses":    [4, 8],
        "text": (
            "Immediate Crisis Gate: IF Saturn is in H4 OR H8 AND the foundation is "
            "dug, the result is an immediate crisis warning — high risk to in-laws "
            "(H4) or to the native's own life (H8). Lal Kitab categorizes this as "
            "a veto: stop construction immediately. "
            "Additional context: if Saturn's position is made auspicious via Rahu/Ketu "
            "configurations, the native will construct houses repeatedly throughout "
            "life — the longevity-of-construction check is the positive variant of "
            "this gate."
        ),
        "remedies":  [],
        "domains":   ["property", "family", "health", "life_risk"],
        "tags":      ["danger_gate", "saturn", "h4", "h8", "veto", "foundation"],
        "source":    "Additional Info — diagnostics immediate_danger_gate",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6: Refinement + Protocol Rules
# ─────────────────────────────────────────────────────────────────────────────

REFINEMENT_RULES = [
    {
        "rule_id":   "lalkitab-ch23-env-bhatti-mars-h8",
        "name":      "Fixed Oven (Bhatti) + Mars in H8 — Family Ruin Trigger",
        "type":      "planetary_combination",
        "sub_type":  "structural",
        "checkable": True,
        "yoga_type": "planet_in_house",
        "yoga_desc": "Mars in H8 in natal chart of child born while family has sealed bhatti in the house.",
        "planets":   ["Mars"],
        "houses":    [8],
        "text": (
            "A fixed oven (bhatti) that has been sealed closed with earth inside the "
            "home is a 'ticking bomb.' If a child is born with Mars in the 8th house "
            "while the family lives in a house with this sealed bhatti, the entire "
            "family is ruined. The bhatti must be permanently opened or removed before "
            "such a child is born."
        ),
        "remedies": [
            {"text": "Remove or permanently open the sealed fixed oven (bhatti) — especially before the birth of a child.", "category": "ritual"},
        ],
        "domains":   ["property", "family", "vastu", "health"],
        "tags":      ["bhatti", "fixed_oven", "mars", "h8", "family_ruin", "structural"],
        "source":    "Diagnostic file + Additional Info — Bhatti Monitor",
    },
    {
        "rule_id":   "lalkitab-ch23-refine-uncle-veto",
        "name":      "Uncle in Saturn's Room — Sun+Saturn in H4 Death Veto",
        "type":      "planetary_combination",
        "sub_type":  "structural",
        "checkable": True,
        "yoga_type": "planet_in_house",
        "yoga_desc": "Sun AND Saturn both in H4 (natal). Compound two-planet check.",
        "planets":   ["Sun", "Saturn"],
        "houses":    [4],
        "text": (
            "If both Sun and Saturn occupy the 4th house, the native's uncle will "
            "certainly die in the room designated for Saturn (typically the left side "
            "of the house used for iron storage). This is a specific family fatality "
            "veto for the paternal uncle when the Saturn/Sun H4 combination is present."
        ),
        "remedies":  [],
        "domains":   ["property", "family", "death"],
        "tags":      ["uncle_veto", "sun", "saturn", "h4", "death", "room_veto"],
        "source":    "Additional Info — JSON refinements uncle_in_saturns_room",
    },
    {
        "rule_id":   "lalkitab-ch23-refine-idol-veto",
        "name":      "Idol Installation Veto — Pran Pratishtha Causes Childlessness",
        "type":      "general_principle",
        "sub_type":  "structural",
        "checkable": False,
        "yoga_type": "behavioral",
        "planets":   [],
        "houses":    [],
        "text": (
            "If idols are installed in the house with full Pran Pratishtha ceremony "
            "(consecration ritual), the native will remain childless. Lal Kitab "
            "recommends using photos or paintings of deities instead of consecrated "
            "idols in the residential home to avoid this progeny affliction."
        ),
        "remedies": [
            {"text": "Use photos or paintings of deities instead of consecrated (Pran Pratishtha) idols in the home.", "category": "ritual"},
        ],
        "domains":   ["property", "progeny", "spirituality"],
        "tags":      ["idol_veto", "pran_pratishtha", "childlessness", "photos", "vastu"],
        "source":    "Additional Info — JSON refinements idol_installation_veto",
    },
    {
        "rule_id":   "lalkitab-ch23-timing-pushya",
        "name":      "Pushya Nakshatra — Mandatory Construction Start and Completion",
        "type":      "general_principle",
        "sub_type":  "construction",
        "checkable": False,
        "yoga_type": "manual",
        "planets":   [],
        "houses":    [],
        "text": (
            "Pushya Nakshatra is mandatory for both starting AND completing construction "
            "to ensure auspicious results. The groundbreaking ceremony AND the final "
            "grihapravesh (housewarming) must be timed to occur when Pushya Nakshatra "
            "is active. Using any other Nakshatra for these milestone events removes "
            "the auspicious protection."
        ),
        "remedies":  [],
        "domains":   ["property", "timing", "nakshatra"],
        "tags":      ["pushya", "nakshatra", "construction_timing", "mandatory"],
        "source":    "Diagnostic file — procedural formula logic",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Rule builder
# ─────────────────────────────────────────────────────────────────────────────

def _make_doc(rule_id: str, name: str, rtype: str, sub_type: str,
              checkable: bool, yoga_type: str, text: str, remedies: list,
              domains: list, tags: list, planets: list, houses: list,
              yoga_desc: str | None, now: str) -> dict:
    doc = _base(rule_id, now)
    yoga_check: dict = {"type": yoga_type, "checkable": checkable}
    if yoga_desc:
        yoga_check["description"] = yoga_desc
    elif not checkable:
        yoga_check["description"] = "Spatial/behavioral rule — not automatable in Phase 1."

    cond: dict = {"type": rtype, "sub_type": sub_type, "yoga_check": yoga_check}
    if planets:
        cond["planets_involved"] = planets
    if houses:
        cond["houses_involved"] = houses

    doc.update({
        "condition": cond,
        "interpretation": {
            "summary":  name,
            "detailed": text,
            "full_text_passages": [{"text": text, "confidence": "HIGH"}],
            "remedies":     remedies,
            "life_domain":  domains[0],
            "life_domains": domains,
            "tags":         tags,
            "physical_markers": [],
        },
        "metadata": {
            "planets_involved":     planets,
            "houses_involved":      houses,
            "signs_involved":       [],
            "condition_count":      1,
            "gender_context":       "neutral",
            "is_group_summary":     False,
            "has_physical_markers": False,
            "physical_categories":  [],
            "yoga_checkable":       checkable,
        },
        "confidence": {
            "source_confidence": "HIGH",
            "extraction_method": "hard_coded",
            "validated":         False,
        },
    })
    return doc


def build_all_rules() -> list[dict]:
    now   = datetime.now(timezone.utc).isoformat()
    docs: list[dict] = []

    # Section 1: Saturn-house rules (12)
    for sr in SATURN_HOUSE_RULES:
        h    = sr["house"]
        docs.append(_make_doc(
            rule_id   = f"lalkitab-ch23-saturn-h{h}",
            name      = sr["name"],
            rtype     = "planetary_combination",
            sub_type  = "construction",
            checkable = True,
            yoga_type = "planet_in_house",
            yoga_desc = f"Saturn in H{h} (natal). {sr.get('source','')}",
            text      = sr["text"],
            remedies  = sr["remedies"],
            domains   = ["property", "family", "construction"],
            tags      = sr["tags"],
            planets   = ["Saturn"],
            houses    = [h],
            now       = now,
        ))

    # Section 2: Geometric veto rules (6)
    for gr in GEOMETRIC_RULES:
        docs.append(_make_doc(
            rule_id   = gr["rule_id"],
            name      = gr["name"],
            rtype     = "dosha" if "geoveto" in gr["rule_id"] else "general_principle",
            sub_type  = gr["sub_type"],
            checkable = False,
            yoga_type = "manual",
            yoga_desc = "Architectural inspection — shape of house plot/structure.",
            text      = gr["text"],
            remedies  = gr["remedies"],
            domains   = ["property", "vastu", "family"],
            tags      = gr["tags"],
            planets   = [],
            houses    = [],
            now       = now,
        ))

    # Section 3: Formula / Spatial rules (3)
    for fr in FORMULA_RULES:
        docs.append(_make_doc(
            rule_id   = fr["rule_id"],
            name      = fr["name"],
            rtype     = fr["type"],
            sub_type  = fr["sub_type"],
            checkable = fr["checkable"],
            yoga_type = fr["yoga_type"],
            yoga_desc = fr.get("yoga_desc"),
            text      = fr["text"],
            remedies  = fr["remedies"],
            domains   = fr["domains"],
            tags      = fr["tags"],
            planets   = fr.get("planets", []),
            houses    = fr.get("houses", []),
            now       = now,
        ))

    # Section 4: Internal layout rules (2)
    for lr in LAYOUT_RULES:
        docs.append(_make_doc(
            rule_id   = lr["rule_id"],
            name      = lr["name"],
            rtype     = "general_principle",
            sub_type  = lr["sub_type"],
            checkable = False,
            yoga_type = "manual",
            yoga_desc = lr.get("yoga_desc", "Architectural layout rule."),
            text      = lr["text"],
            remedies  = lr["remedies"],
            domains   = lr["domains"],
            tags      = lr["tags"],
            planets   = [],
            houses    = [],
            now       = now,
        ))

    # Section 5: Diagnostic / environmental rules (4)
    for dr in DIAGNOSTIC_RULES:
        docs.append(_make_doc(
            rule_id   = dr["rule_id"],
            name      = dr["name"],
            rtype     = dr["type"],
            sub_type  = dr["sub_type"],
            checkable = dr["checkable"],
            yoga_type = dr["yoga_type"],
            yoga_desc = dr.get("yoga_desc"),
            text      = dr["text"],
            remedies  = dr["remedies"],
            domains   = dr["domains"],
            tags      = dr["tags"],
            planets   = dr.get("planets", []),
            houses    = dr.get("houses", []),
            now       = now,
        ))

    # Section 6: Refinement + protocol rules (4)
    for rr in REFINEMENT_RULES:
        docs.append(_make_doc(
            rule_id   = rr["rule_id"],
            name      = rr["name"],
            rtype     = rr["type"],
            sub_type  = rr["sub_type"],
            checkable = rr["checkable"],
            yoga_type = rr["yoga_type"],
            yoga_desc = rr.get("yoga_desc"),
            text      = rr["text"],
            remedies  = rr["remedies"],
            domains   = rr["domains"],
            tags      = rr["tags"],
            planets   = rr.get("planets", []),
            houses    = rr.get("houses", []),
            now       = now,
        ))

    return docs


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    group  = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--upload",  metavar="JSON_FILE")
    parser.add_argument("--save",   metavar="JSON_FILE")
    parser.add_argument("--mongo-url")
    parser.add_argument("--db-name", default="horoscope_db")
    args = parser.parse_args()

    if args.dry_run:
        rules = build_all_rules()
        print(f"Dry run: {len(rules)} rules generated\n")
        groups = {
            "saturn-h":         "Saturn-House (12)",
            "geoveto":          "Geometric Veto (5)",
            "structural-right": "Right-Angle Gold Standard (1)",
            "formula":          "Formula/Spatial",
            "spatial":          "Formula/Spatial",
            "structural-dead":  "Formula/Spatial",
            "layout":           "Layout (2)",
            "diag":             "Diagnostic/Environmental",
            "env":              "Diagnostic/Environmental",
            "refine":           "Refinement",
            "timing":           "Refinement",
        }
        for r in rules:
            rid = r["rule_id"]
            ct  = r["condition"]["type"]
            ck  = "✓" if r["condition"]["yoga_check"]["checkable"] else "·"
            print(f"  {ck} {rid:55s} [{ct}]")
        if args.save:
            Path(args.save).write_text(json.dumps(rules, indent=2, ensure_ascii=False))
            print(f"\nSaved → {args.save}")
        return

    if not args.mongo_url:
        print("ERROR: --mongo-url required for upload", file=sys.stderr)
        sys.exit(1)

    from pymongo import MongoClient
    rules    = json.loads(Path(args.upload).read_text())
    print(f"Loaded {len(rules)} rules from {args.upload}")

    client   = MongoClient(args.mongo_url)
    col      = client[args.db_name]["interpretation_rules"]
    inserted = updated = 0
    for r in rules:
        res = col.update_one({"rule_id": r["rule_id"]}, {"$set": r}, upsert=True)
        if res.upserted_id:
            inserted += 1
        elif res.modified_count:
            updated += 1

    print(f"✅ Inserted {inserted} / Updated {updated} rules → {args.db_name}.interpretation_rules")
    client.close()


if __name__ == "__main__":
    main()
