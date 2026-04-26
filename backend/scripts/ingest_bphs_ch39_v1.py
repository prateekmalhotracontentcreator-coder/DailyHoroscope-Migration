#!/usr/bin/env python3
"""
ingest_bphs_ch39_v1.py — BPHS Chapter 39: Raja Yogas

50 rules total across 8 groups:
  1  Framework / General Principle         (Slokas 3-5)
  2  Maha Raja Yoga                        (Slokas 6-7)
  9  Karakamsa & Jaimini Raja Yogas        (Slokas 8-16)
 16  Positional Raja Yogas                 (Slokas 17-31)
  9  Lord Conjunction Raja Yogas           (Slokas 33-39)
  3  Birth Time / Koteeswara Yogas         (Sloka 40)
  2  Mutual Position Yogas                 (Sloka 41)
  8  Dignity & Count Raja Yogas            (Slokas 42-48)

Hard-coded from RTF — zero AI extraction cost.
Checkable: 3 / 50 (6%) — chapter is overwhelmingly Jaimini-based
(Atmakaraka, Karakamsa, Arudha Pada, special Lagnas) and lord-heavy.

Checkable rules:
  bphs-ch39-012  Sloka 17  — benefics in {1,2,4} + malefic in {3}
  bphs-ch39-017  Sloka 21B — benefics in angles {1,4,7,10}
  bphs-ch39-050  Sloka 48  — benefics in {1,4,7,10} + malefics in {3,6,11}

yoga_check blocker categories (for non-checkable rules):
  K = Karakamsa / Jaimini concepts (Atmakaraka, Karakamsa Lagna, Arudha Pada,
      Darapada, Hora Lagna, Ghatika Lagna)
  L = House lord identification required
  D = Dignity / strength check (own sign, exaltation, moolatrikona, debilitation)
  V = Multiple divisional charts (Shadvarga, Drekkana, Navamsa, Uttamamsa)
  T = Birth-time (day/night, solar midday) — not a chart position
  A = Mutual aspect detection
  R = Relative planet-to-planet house distance (not from Lagna)

Standard --save / --upload workflow:
  Step 1 — Dry run:
    python3 scripts/ingest_bphs_ch39_v1.py --dry-run --save scripts/bphs_ch39_rules.json

  Step 2 — Review bphs_ch39_rules.json; amend as needed.

  Step 3 — Upload (zero API calls):
    python3 scripts/ingest_bphs_ch39_v1.py \\
      --upload scripts/bphs_ch39_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 4 — Validate:
    python3 scripts/validate_rules.py \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id bphs-ch39-v1-20260426
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
CHAPTER   = 39
CHAP_NAME = "Raja Yogas"
BATCH_ID  = "bphs-ch39-v1-20260426"

# ── Blocker legend (for yoga_check descriptions) ─────────────────────────────
# K = Karakamsa / Jaimini  L = Lord identification  D = Dignity/strength
# V = Divisional charts    T = Birth time           A = Mutual aspect
# R = Relative planet-to-planet position

# ── Yoga source data ──────────────────────────────────────────────────────────

YOGA_DATA: list[dict] = [

    # ═══════════════════════════════════════════════════════════════════════════
    # 1. FRAMEWORK / GENERAL PRINCIPLE (Slokas 3-5)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":     "Raja Yoga — Framework",
        "sloka":         "ch39-framework",
        "group":         "framework",
        "condition_type": "general_principle",
        "formation":     (
            "Raja Yogas are to be evaluated from two reference points: "
            "(1) the Karakamsa Lagna (Navamsa sign of the Atmakaraka) and "
            "(2) the natal ascendant. From the Karakamsa reference, the "
            "Atmakaraka and Putrakaraka (Chara Karaka, 6th in the Karakamsa "
            "scheme) are the key planets. From the natal ascendant, the "
            "ascendant lord and 5th lord are the key planets. The 5th lord is "
            "equated in importance to the 9th lord for Raja Yoga analysis. "
            "Effects are full, half, or quarter according to the strength of "
            "the participating planets."
        ),
        "effect":        (
            "Framework rule — determines which planetary pairs and reference "
            "points to use when assessing the strength and maturity of any "
            "Raja Yoga in the horoscope."
        ),
        "is_benefic":    True,
        "life_domains":  ["status", "power", "leadership"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "L"],
            "description": (
                "Meta-framework rule. Requires identifying Atmakaraka (highest "
                "degree planet), computing Karakamsa Lagna (Navamsa sign of "
                "Atmakaraka), and evaluating Chara Karaka scheme — all Jaimini "
                "concepts outside current engine scope."
            ),
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 2. MAHA RAJA YOGA (Slokas 6-7)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":     "Maha Raja Yoga",
        "sloka":         "ch39-maha-raja-yoga",
        "group":         "maha_raja_yoga",
        "formation":     (
            "Condition A: Ascendant lord and 5th lord exchange their signs "
            "(Parivartana Yoga between houses 1 and 5). "
            "Condition B: Atmakaraka and Putrakaraka (Chara Karaka) are "
            "together in the natal ascendant or 5th house (or Karakamsa Lagna "
            "and 5th therefrom), OR separately in their exaltation/own/own "
            "Navamsa signs and aspected by a natural benefic."
        ),
        "effect":        (
            "The native will be famous and happy. Considered the supreme Raja "
            "Yoga — bestows the highest status and recognition."
        ),
        "is_benefic":    True,
        "life_domains":  ["fame", "status", "royalty", "happiness"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "L", "D", "V"],
            "description": (
                "Condition A requires identifying Asc lord and 5th lord and "
                "verifying sign exchange (Parivartana) — lord identification "
                "required. Condition B requires Atmakaraka identification "
                "(highest-degree planet), Chara Putrakaraka, and Navamsa "
                "dignity check — Jaimini + divisional chart required."
            ),
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 3. KARAKAMSA & JAIMINI RAJA YOGAS (Slokas 8-16)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":     "Atmakaraka-Ascendant Lord Raja Yoga",
        "sloka":         "ch39-sloka-08",
        "group":         "karakamsa_raja_yoga",
        "formation":     (
            "The natal ascendant lord and the Atmakaraka are conjunct in the "
            "ascendant, 5th, or 7th house, with a natural benefic in conjunction "
            "with or aspecting them. If the ascendant lord himself is the "
            "Atmakaraka, his placement in the 1st, 5th, or 7th with a benefic "
            "suffices."
        ),
        "effect":        "A Raja yoga is formed; the native attains high status.",
        "is_benefic":    True,
        "life_domains":  ["status", "power"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "L"],
            "description": (
                "Requires identifying Atmakaraka (highest-degree planet among "
                "Sun through Saturn) and Asc lord. Atmakaraka is a Jaimini "
                "concept outside current engine scope."
            ),
        },
    },
    {
        "yoga_name":     "Benefics from Atmakaraka / Ascendant Lord Raja Yoga",
        "sloka":         "ch39-sloka-09-10a",
        "group":         "karakamsa_raja_yoga",
        "formation":     (
            "Natural benefics occupy the 2nd, 4th, and 5th houses counted from "
            "the natal ascendant lord's sign position OR from the Atmakaraka's "
            "sign position."
        ),
        "effect":        "The native will become a king.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty", "wealth"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "L"],
            "description": (
                "Houses 2/4/5 are counted from the ascendant lord's sign "
                "(not from Lagna) and from Atmakaraka's sign — both require "
                "lord identification and Jaimini Atmakaraka computation."
            ),
        },
    },
    {
        "yoga_name":     "Malefics from Atmakaraka / Ascendant Lord Raja Yoga",
        "sloka":         "ch39-sloka-09-10b",
        "group":         "karakamsa_raja_yoga",
        "formation":     (
            "Natural malefics occupy the 3rd and 6th houses counted from the "
            "natal ascendant lord's sign position OR from the Atmakaraka's "
            "sign position."
        ),
        "effect":        "The native will become a king.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty", "enemies"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "L"],
            "description": (
                "3rd and 6th counted from Asc lord's sign and Atmakaraka sign — "
                "requires lord identification + Jaimini Atmakaraka."
            ),
        },
    },
    {
        "yoga_name":     "Venus in Karakamsa — Royal Association Yoga",
        "sloka":         "ch39-sloka-11",
        "group":         "karakamsa_raja_yoga",
        "formation":     (
            "Venus occupies one of four positions: the Karakamsa Lagna, the 5th "
            "from Karakamsa Lagna, the natal ascendant, or the Arudha (Pada) "
            "ascendant — AND is in aspect to or conjunction with Jupiter or "
            "the Moon."
        ),
        "effect":        "The native will be related to royal circles.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty", "social_position"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K"],
            "description": (
                "Karakamsa Lagna (Navamsa sign of Atmakaraka) and Arudha Pada "
                "(Pada for the Lagna) are both Jaimini concepts requiring "
                "divisional chart computation and special ascendant derivation."
            ),
        },
    },
    {
        "yoga_name":     "Single Planet Aspects Special Lagna — Raja Yoga",
        "sloka":         "ch39-sloka-12",
        "group":         "karakamsa_raja_yoga",
        "formation":     (
            "Even a single planet aspects any one of the three special ascendants: "
            "the natal ascendant (Lagna), Hora Lagna, or Ghatika Lagna."
        ),
        "effect":        "The native will become a king.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "A"],
            "description": (
                "Hora Lagna and Ghatika Lagna are time-based special ascendants "
                "(derived from birth time, sunrise, and duration of day) outside "
                "current Rasi-chart scope. Aspect detection also required."
            ),
        },
    },
    {
        "yoga_name":     "Shadvarga Lagna Raja Yoga",
        "sloka":         "ch39-sloka-13-14",
        "group":         "karakamsa_raja_yoga",
        "formation":     (
            "The six divisional ascendants (Shadvarga: Rasi, Hora, Drekkana, "
            "Trimsamsa, Navamsa, and Dvadasamsa) are all occupied or aspected "
            "by one and the same planet. The yoga is full/medium/negligible "
            "according to whether the planet's aspect is full/half/quarter."
        ),
        "effect":        "A Raja yoga is doubtlessly formed.",
        "is_benefic":    True,
        "life_domains":  ["status", "power", "royalty"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["V", "A"],
            "description": (
                "Requires computation of 6 separate divisional chart ascendants "
                "(D-1 through D-12) and aspect evaluation across all six — "
                "far beyond current Rasi-only engine scope."
            ),
        },
    },
    {
        "yoga_name":     "Three Ascendants Exalted — Raja Yoga (A)",
        "sloka":         "ch39-sloka-15a",
        "group":         "karakamsa_raja_yoga",
        "formation":     (
            "The natal ascendant, Hora Lagna, and Ghatika Lagna are each "
            "occupied by a planet in exaltation or in its own sign."
        ),
        "effect":        "A Raja yoga is formed.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "D"],
            "description": (
                "Hora Lagna and Ghatika Lagna are time-based special ascendants "
                "outside current scope. Exaltation/own sign check (dignity) "
                "also required."
            ),
        },
    },
    {
        "yoga_name":     "Three Ascendants Exalted — Raja Yoga (B)",
        "sloka":         "ch39-sloka-15b",
        "group":         "karakamsa_raja_yoga",
        "formation":     (
            "The natal ascendant, the Drekkana ascendant (ascendant of the "
            "Drekkana/D-3 chart), and the Navamsa ascendant (ascendant of "
            "the D-9 chart) are all occupied by exalted planets."
        ),
        "effect":        "A Raja yoga is formed.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["V", "D"],
            "description": (
                "Requires computing Drekkana (D-3) and Navamsa (D-9) ascendants "
                "and checking dignity in those divisional charts."
            ),
        },
    },
    {
        "yoga_name":     "Arudha Lagna Moon-Jupiter Raja Yoga",
        "sloka":         "ch39-sloka-16",
        "group":         "karakamsa_raja_yoga",
        "formation":     (
            "The Moon and a natural benefic are conjunct in the Arudha Lagna "
            "(Pada of the natal ascendant), Jupiter is in the 2nd house from "
            "the natal ascendant, and both the Arudha Lagna position and the "
            "2nd house are aspected by planets in exaltation or in their own "
            "signs."
        ),
        "effect":        "A Raja yoga is formed.",
        "is_benefic":    True,
        "life_domains":  ["status", "wealth", "royalty"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "D", "A"],
            "description": (
                "Arudha Lagna (Pada of the 1st house) is a Jaimini concept "
                "requiring special derivation. Dignity and aspect checks "
                "additionally required."
            ),
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 4. POSITIONAL RAJA YOGAS (Slokas 17-31)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":     "Benefics in 1-2-4, Malefic in 3 — Raja Yoga",
        "sloka":         "ch39-sloka-17",
        "group":         "positional_raja_yoga",
        "formation":     (
            "Natural benefics occupy the ascendant (1st), 2nd, and 4th houses "
            "while a natural malefic is placed in the 3rd house."
        ),
        "effect":        "The native will become a king or equal to a king.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty", "wealth"],
        "yoga_check": {
            "type":      "multi_house_requirements",
            "checkable": True,
            "description": (
                "Benefics in houses 1, 2, and 4 AND malefic in house 3. "
                "All conditions evaluated from natal ascendant. "
                "Pure planet-position check — no lord or dignity lookup required."
            ),
            "operator": "and",
            "house_requirements": [
                {"houses": [1, 2, 4], "planet_type": "benefic",  "constraint": "present"},
                {"houses": [3],        "planet_type": "malefic",  "constraint": "present"},
            ],
        },
    },
    {
        "yoga_name":     "Benefic Exalted in 2nd — Wealth Yoga",
        "sloka":         "ch39-sloka-18",
        "group":         "positional_raja_yoga",
        "formation":     (
            "One among the Moon, Jupiter, Venus, or Mercury is placed in the "
            "2nd house in its exaltation sign."
        ),
        "effect":        "The native will be wealthy.",
        "is_benefic":    True,
        "life_domains":  ["wealth"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["D"],
            "description": (
                "Requires checking whether the planet in house 2 is in its "
                "exaltation sign — dignity check needed (Moon exalted in "
                "Taurus, Jupiter in Cancer, Venus in Pisces, Mercury in Virgo). "
                "Phase 2: new type 'planet_exalted_in_house' with "
                "house=2, planets=[Moon, Jupiter, Venus, Mercury]."
            ),
        },
    },
    {
        "yoga_name":     "Debilitated Planets in 6-8-3, Exalted Asc Lord — Raja Yoga",
        "sloka":         "ch39-sloka-19",
        "group":         "positional_raja_yoga",
        "formation":     (
            "Debilitated (neecha) planets occupy the 6th, 8th, and 3rd houses "
            "while the ascendant lord is in exaltation or in his other own sign "
            "and aspects the natal ascendant."
        ),
        "effect":        "A Raja yoga is formed.",
        "is_benefic":    True,
        "life_domains":  ["status", "power", "enemies"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["L", "D"],
            "description": (
                "Requires identifying Asc lord + checking its dignity "
                "(exaltation/own sign) + aspect to Lagna. Debilitation in "
                "specific houses also requires dignity check per planet."
            ),
        },
    },
    {
        "yoga_name":     "6-8-12 Lords Afflicted, Asc Lord Strong — Raja Yoga",
        "sloka":         "ch39-sloka-20",
        "group":         "positional_raja_yoga",
        "formation":     (
            "The lords of the 6th, 8th, and 12th houses are in debilitation "
            "(fall), inimical signs, or combustion, while the ascendant lord "
            "is in his own sign or exaltation sign and aspects the natal "
            "ascendant."
        ),
        "effect":        "A Raja yoga is formed.",
        "is_benefic":    True,
        "life_domains":  ["status", "power", "enemies"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["L", "D"],
            "description": (
                "Requires identifying lords of houses 6, 8, 12, and the Asc "
                "lord. Dignity checks for debilitation/inimical/combustion and "
                "own/exalt required for all four lords."
            ),
        },
    },
    {
        "yoga_name":     "10th Lord Own-Exalt Aspects Lagna — Raja Yoga",
        "sloka":         "ch39-sloka-21a",
        "group":         "positional_raja_yoga",
        "formation":     (
            "The 10th lord is placed in his own sign or exaltation sign and "
            "aspects the natal ascendant."
        ),
        "effect":        "A Raja yoga is formed.",
        "is_benefic":    True,
        "life_domains":  ["career", "status", "power"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["L", "D", "A"],
            "description": (
                "Requires identifying the 10th lord, verifying its dignity "
                "(own/exalt sign), and checking its aspect to the Lagna."
            ),
        },
    },
    {
        "yoga_name":     "Benefics in Angles — Raja Yoga",
        "sloka":         "ch39-sloka-21b",
        "group":         "positional_raja_yoga",
        "formation":     (
            "Natural benefics (Jupiter, Venus, Mercury, waxing Moon) are placed "
            "in the angular houses (1st, 4th, 7th, 10th)."
        ),
        "effect":        "A Raja yoga is formed.",
        "is_benefic":    True,
        "life_domains":  ["status", "power", "wealth"],
        "yoga_check": {
            "type":      "benefics_in_houses",
            "checkable": True,
            "houses":    [1, 4, 7, 10],
            "planet_type": "benefic",
            "description": (
                "Natural benefics in the four angular (kendra) houses from "
                "the natal ascendant. Pure positional check."
            ),
        },
    },
    {
        "yoga_name":     "Atmakaraka in Benefic Rasi — Wealth Yoga",
        "sloka":         "ch39-sloka-22a",
        "group":         "karakamsa_raja_yoga",
        "formation":     (
            "The Atmakaraka planet is placed in a sign owned by a natural "
            "benefic (Jupiter, Venus, Mercury, Moon) or in a benefic's "
            "Navamsa sign."
        ),
        "effect":        "The native will be wealthy.",
        "is_benefic":    True,
        "life_domains":  ["wealth"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "V"],
            "description": (
                "Requires identifying Atmakaraka (highest-degree planet) — "
                "Jaimini concept. Navamsa check additionally requires D-9 chart."
            ),
        },
    },
    {
        "yoga_name":     "Benefics in Angles from Karakamsa Lagna — Raja Yoga",
        "sloka":         "ch39-sloka-22b",
        "group":         "karakamsa_raja_yoga",
        "formation":     (
            "Natural benefics are placed in the angular houses (kendras) "
            "counted from the Karakamsa Lagna (Navamsa sign of the Atmakaraka)."
        ),
        "effect":        "The native will become a king.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "V"],
            "description": (
                "Angular houses are counted from Karakamsa Lagna, not natal "
                "Lagna. Karakamsa requires Atmakaraka identification + D-9 "
                "computation — both outside current engine scope."
            ),
        },
    },
    {
        "yoga_name":     "Arudha Lagna and Darapada — Raja Yoga",
        "sloka":         "ch39-sloka-23a",
        "group":         "karakamsa_raja_yoga",
        "formation":     (
            "The Arudha Lagna (Pada of the 1st house) and Darapada (Pada of "
            "the 7th house) are in mutual angular positions (1-4-7-10 from "
            "each other), mutual trinal positions (1-5-9), or in mutual "
            "3rd/11th relationship."
        ),
        "effect":        "The native will doubtlessly become a king.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty", "social_position"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K"],
            "description": (
                "Arudha Lagna and Darapada are Jaimini Pada (image) concepts "
                "derived via a specific counting algorithm from the 1st and 7th "
                "house lords. Outside current engine scope."
            ),
        },
    },
    {
        "yoga_name":     "Arudha-Darapada Adverse — Poverty",
        "sloka":         "ch39-sloka-23b",
        "group":         "karakamsa_raja_yoga",
        "condition_type": "yoga_combination",
        "formation":     (
            "The Arudha Lagna and Darapada are in mutual 6th/8th signs or "
            "mutual 2nd/12th signs."
        ),
        "effect":        (
            "The native will suffer from poverty and will not receive the "
            "beneficial effects of any Raja Yogas in the horoscope. The "
            "good relationship between Arudha Pada and Dara Pada is an "
            "essential prerequisite for maturity of Raja Yogas."
        ),
        "is_benefic":    False,
        "life_domains":  ["poverty", "hardship", "status"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K"],
            "description": (
                "Adverse form of Arudha-Darapada yoga — mutual 6/8 or 2/12 "
                "positions destroy Raja Yoga maturity. Requires Jaimini Pada "
                "derivation for both Arudha Lagna and Darapada."
            ),
        },
    },
    {
        "yoga_name":     "Arudha Pada with Exalted Planet — Raja Yoga (A)",
        "sloka":         "ch39-sloka-26-27a",
        "group":         "karakamsa_raja_yoga",
        "formation":     (
            "The Arudha Pada (Arudha Lagna) is occupied by an exalted planet — "
            "especially the Moon in exaltation (Taurus) or by Jupiter or Venus "
            "(with or without exaltation) — and there is no Argala (intervention) "
            "by a natural malefic planet."
        ),
        "effect":        "The native will become a king.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "D"],
            "description": (
                "Arudha Pada requires Jaimini Pada derivation. Exaltation "
                "(dignity) check and Argala (intervention analysis) also required."
            ),
        },
    },
    {
        "yoga_name":     "Arudha Pada with Moon in Benefic Sign — Raja Yoga (B)",
        "sloka":         "ch39-sloka-26-27b",
        "group":         "karakamsa_raja_yoga",
        "formation":     (
            "The Arudha Pada is a benefic sign (sign owned by Jupiter, Venus, "
            "Mercury, or Moon) AND the Moon occupies the Arudha Pada AND "
            "Jupiter is in the 2nd house from the natal ascendant."
        ),
        "effect":        "The native will become a king.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty", "wealth"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "D"],
            "description": (
                "Arudha Pada requires Jaimini Pada derivation. Benefic sign "
                "classification (sign owned by benefic planet) is a dignity "
                "check. Jupiter in house 2 from natal Lagna is checkable alone "
                "but the combined condition requires Arudha Pada."
            ),
        },
    },
    {
        "yoga_name":     "Dusthana Lord Debilitated Aspects Lagna — Raja Yoga",
        "sloka":         "ch39-sloka-28",
        "group":         "positional_raja_yoga",
        "formation":     (
            "Even if one among the lords of the 6th, 8th, and 12th houses is "
            "in debilitation (neecha) and aspects the natal ascendant, a "
            "Raja yoga is formed."
        ),
        "effect":        "A Raja yoga is formed.",
        "is_benefic":    True,
        "life_domains":  ["status", "enemies", "obstacles"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["L", "D", "A"],
            "description": (
                "Requires identifying lords of houses 6, 8, and 12 and checking "
                "their debilitation sign + aspect to Lagna."
            ),
        },
    },
    {
        "yoga_name":     "Kendra-Trikona Lord Aspects Lagna with Venus and Arudha — Raja Yoga",
        "sloka":         "ch39-sloka-29-31a",
        "group":         "positional_raja_yoga",
        "formation":     (
            "A planet ruling the 4th, 10th, 2nd, or 11th house aspects the "
            "natal ascendant, while Venus aspects the 11th house from the "
            "Arudha Lagna AND the Arudha Lagna itself is occupied by a "
            "natural benefic."
        ),
        "effect":        "The native will become a king.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty", "wealth"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "L", "A"],
            "description": (
                "Triple condition: lord of 4/10/2/11 identification, Arudha "
                "Lagna derivation (Jaimini), and aspect checks on Lagna and "
                "Arudha Lagna 11th position."
            ),
        },
    },
    {
        "yoga_name":     "Debilitated Planet in 6th-8th Aspects Lagna — Raja Yoga",
        "sloka":         "ch39-sloka-29-31b",
        "group":         "positional_raja_yoga",
        "formation":     (
            "A debilitated (neecha) planet placed in the 6th or 8th house "
            "aspects the natal ascendant."
        ),
        "effect":        "The native will become a king.",
        "is_benefic":    True,
        "life_domains":  ["status", "enemies", "obstacles"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["D", "A"],
            "description": (
                "Requires checking debilitation (neecha) sign for any planet "
                "in house 6 or 8 — dignity check. Aspect to Lagna also required."
            ),
        },
    },
    {
        "yoga_name":     "Debilitated Planet in 3rd-11th Aspects Lagna — Raja Yoga",
        "sloka":         "ch39-sloka-29-31c",
        "group":         "positional_raja_yoga",
        "formation":     (
            "A debilitated (neecha) planet placed in the 3rd or 11th house "
            "aspects the natal ascendant."
        ),
        "effect":        "The native will become a king.",
        "is_benefic":    True,
        "life_domains":  ["status", "upachaya"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["D", "A"],
            "description": (
                "Requires checking debilitation sign for any planet in house "
                "3 or 11 + aspect to Lagna. Neecha determination requires "
                "knowing each planet's debilitation sign."
            ),
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 5. LORD CONJUNCTION RAJA YOGAS (Slokas 33-39)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":     "5th and 9th Lord Mutual Aspect or Conjunction — Raja Yoga",
        "sloka":         "ch39-sloka-33-34",
        "group":         "lord_conjunction_yoga",
        "formation":     (
            "The 9th lord (equated to a minister) and the 5th lord (equated to "
            "the chief minister) mutually aspect each other, or are conjunct in "
            "any house, or are in mutual 7th positions. For a person of royal "
            "lineage, this combination gives the kingdom."
        ),
        "effect":        "The native will obtain a kingdom.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty", "power"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["L", "A"],
            "description": (
                "Requires identifying 5th lord and 9th lord. Mutual aspect "
                "and mutual 7th position checks also needed."
            ),
        },
    },
    {
        "yoga_name":     "4th-10th Parivartana with 5th-9th Aspect — Raja Yoga",
        "sloka":         "ch39-sloka-35",
        "group":         "lord_conjunction_yoga",
        "formation":     (
            "The 4th lord is placed in the 10th house AND the 10th lord is "
            "placed in the 4th house (a Parivartana / sign-exchange between "
            "houses 4 and 10) and both are aspected by the 5th and 9th lords."
        ),
        "effect":        "The native will attain kingdom.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty", "home", "career"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["L", "A"],
            "description": (
                "Requires identifying lords of houses 4, 5, 9, 10. Four separate "
                "lord lookups + sign exchange verification + aspect detection."
            ),
        },
    },
    {
        "yoga_name":     "Lords of 5-10-4-Asc All in 9th — Raja Yoga",
        "sloka":         "ch39-sloka-36",
        "group":         "lord_conjunction_yoga",
        "formation":     (
            "The lords of the 5th, 10th, 4th, and ascendant are all conjunct "
            "in the 9th house."
        ),
        "effect":        (
            "The native will become a ruler with fame spreading over the "
            "four directions."
        ),
        "is_benefic":    True,
        "life_domains":  ["status", "royalty", "fame", "power"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["L"],
            "description": (
                "Requires identifying lords of houses 1, 4, 5, and 10 — four "
                "lord lookups — and verifying all are in house 9."
            ),
        },
    },
    {
        "yoga_name":     "4th Lord Joins 5th Lord — Raja Yoga",
        "sloka":         "ch39-sloka-37a",
        "group":         "lord_conjunction_yoga",
        "formation":     (
            "The lord of the 4th house is conjunct with the lord of the 5th "
            "house (angular lord joins trinal lord). Per the text: 'It will "
            "be still superior if the 4th lord joins both the 5th and 9th lords.'"
        ),
        "effect":        "The native will obtain kingdom.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty", "home"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["L"],
            "description": "Requires identifying 4th lord and 5th lord.",
        },
    },
    {
        "yoga_name":     "4th Lord Joins 9th Lord — Raja Yoga",
        "sloka":         "ch39-sloka-37b",
        "group":         "lord_conjunction_yoga",
        "formation":     (
            "The lord of the 4th house is conjunct with the lord of the 9th "
            "house (angular lord joins trinal lord)."
        ),
        "effect":        "The native will obtain kingdom.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty", "fortune"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["L"],
            "description": "Requires identifying 4th lord and 9th lord.",
        },
    },
    {
        "yoga_name":     "10th Lord Joins 9th Lord — Raja Yoga",
        "sloka":         "ch39-sloka-37c",
        "group":         "lord_conjunction_yoga",
        "formation":     (
            "The lord of the 10th house is conjunct with the lord of the 9th "
            "house (angular lord joins trinal lord)."
        ),
        "effect":        "The native will obtain kingdom.",
        "is_benefic":    True,
        "life_domains":  ["career", "status", "fortune"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["L"],
            "description": "Requires identifying 10th lord and 9th lord.",
        },
    },
    {
        "yoga_name":     "10th Lord Joins 5th Lord — Raja Yoga",
        "sloka":         "ch39-sloka-37d",
        "group":         "lord_conjunction_yoga",
        "formation":     (
            "The lord of the 10th house is conjunct with the lord of the 5th "
            "house (angular lord joins trinal lord)."
        ),
        "effect":        "The native will obtain kingdom.",
        "is_benefic":    True,
        "life_domains":  ["career", "status", "intelligence"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["L"],
            "description": "Requires identifying 10th lord and 5th lord.",
        },
    },
    {
        "yoga_name":     "5th Lord in Kendra with 9th or Asc Lord — Raja Yoga",
        "sloka":         "ch39-sloka-38",
        "group":         "lord_conjunction_yoga",
        "formation":     (
            "The lord of the 5th house is placed in the ascendant (1st), 4th, "
            "or 10th house AND is in conjunction with either the 9th lord or "
            "the ascendant lord."
        ),
        "effect":        "The native will become a king.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty", "intelligence"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["L"],
            "description": (
                "Requires identifying lords of houses 1, 5, 9 and verifying "
                "5th lord's house position."
            ),
        },
    },
    {
        "yoga_name":     "Jupiter in Own Sign in 9th with Venus or 5th Lord — Raja Yoga",
        "sloka":         "ch39-sloka-39",
        "group":         "lord_conjunction_yoga",
        "formation":     (
            "Jupiter is placed in the 9th house in his own sign (Sagittarius "
            "or Pisces must be the 9th house for the given ascendant) AND is "
            "in conjunction with either Venus or the lord of the 5th house."
        ),
        "effect":        "The native will obtain kinghood.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty", "fortune", "wisdom"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["L", "D"],
            "description": (
                "Jupiter's own sign in 9th house requires knowing which sign "
                "occupies house 9 for the given ascendant (dignity check). "
                "5th lord identification also required."
            ),
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 6. BIRTH TIME YOGAS (Sloka 40)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":     "Birth Near Dinardha / Nisardha — Raja Yoga",
        "sloka":         "ch39-sloka-40",
        "group":         "birth_time_yoga",
        "formation":     (
            "Birth occurs within two-and-a-half ghatis (60 minutes by Parasara; "
            "48 minutes per Uttara Kalamrita) of Dinardha (the middle of the "
            "day — half the daylight duration from sunrise) or Nisardha "
            "(the middle of the night — half the night duration from sunset). "
            "Note: Dinardha is NOT fixed 12 Noon but the actual midpoint of "
            "daylight hours at the given location."
        ),
        "effect":        "The native will be a king or equal to a king.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["T"],
            "description": (
                "Birth-time check, not a chart position check. Requires birth "
                "time, sunrise, sunset at birth location to compute Dinardha "
                "and Nisardha, then measure time difference. Cannot be "
                "determined from Rasi chart planetary positions alone."
            ),
        },
    },
    {
        "yoga_name":     "Koteeswara Yoga",
        "sloka":         "ch39-sloka-40-koteeswara",
        "group":         "birth_time_yoga",
        "formation":     (
            "An exalted planet is placed in the 2nd house AND is aspected by "
            "another exalted planet (from Uttara Kalamrita tradition)."
        ),
        "effect":        "A Koteeswara (multi-millionaire / crorepati) is born.",
        "is_benefic":    True,
        "life_domains":  ["extreme_wealth", "status"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["D", "A"],
            "description": (
                "Both conditions require exaltation (dignity) check — which "
                "planet in house 2 is exalted, and which aspecting planet is "
                "also exalted. Aspect detection also required."
            ),
        },
    },
    {
        "yoga_name":     "Lakshadheew Yoga",
        "sloka":         "ch39-sloka-40-lakshadheew",
        "group":         "birth_time_yoga",
        "formation":     (
            "An exalted planet is placed in the 2nd house AND is aspected by "
            "a planet in its own sign (not exaltation — lesser form of "
            "Koteeswara Yoga)."
        ),
        "effect":        (
            "The native will be a Lakshadhipati (lakhs-owner) — highly wealthy "
            "but with relatively less riches than Koteeswara."
        ),
        "is_benefic":    True,
        "life_domains":  ["wealth", "status"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["D", "A"],
            "description": (
                "Exaltation check for planet in house 2 + own-sign check for "
                "aspecting planet (dignity checks) + aspect detection required."
            ),
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 7. MUTUAL POSITION YOGAS (Sloka 41)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":     "Moon and Venus in Mutual 3rd-11th — Raja Yoga",
        "sloka":         "ch39-sloka-41a",
        "group":         "mutual_position_yoga",
        "formation":     (
            "The Moon and Venus are placed in mutual 3rd and 11th positions "
            "from each other — one is in the 3rd sign from the other (and "
            "therefore the other is simultaneously in the 11th from the first)."
        ),
        "effect":        "A Raja yoga is obtained.",
        "is_benefic":    True,
        "life_domains":  ["status", "wealth", "relationships"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["R"],
            "description": (
                "Requires computing the relative house distance between Moon "
                "and Venus — not a check from the Lagna. Phase 2: implement "
                "as new type 'mutual_house_distance' with planets=[Moon, Venus] "
                "and distances=[3, 11]."
            ),
        },
    },
    {
        "yoga_name":     "Moon and Venus Mutually Aspecting — Raja Yoga",
        "sloka":         "ch39-sloka-41b",
        "group":         "mutual_position_yoga",
        "formation":     (
            "The Moon and Venus are placed in any houses but aspect each other "
            "mutually (either by 7th-house opposition aspect or by special "
            "aspects if applicable)."
        ),
        "effect":        "A Raja yoga is obtained.",
        "is_benefic":    True,
        "life_domains":  ["status", "wealth", "relationships"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["A"],
            "description": (
                "Mutual aspect detection between Moon and Venus. Mutual 7th "
                "aspect (opposition) is the primary form. Aspect checks are "
                "outside current Rasi position-only engine scope."
            ),
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 8. DIGNITY & COUNT RAJA YOGAS (Slokas 42-48)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":     "Moon in Vargothamsa with 4+ Aspects — Raja Yoga",
        "sloka":         "ch39-sloka-42",
        "group":         "dignity_raja_yoga",
        "formation":     (
            "The Moon is in Vargothamsa (same sign in the Rasi chart D-1 and "
            "the Navamsa chart D-9, indicating it is in the same Navamsa as "
            "its Rasi sign) AND is aspected by four or more planets."
        ),
        "effect":        "The native will become a king.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty", "mind"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["V", "A"],
            "description": (
                "Vargothamsa requires comparing Moon's sign in D-1 and D-9 "
                "charts — D-9 computation required. Counting aspects from "
                "4+ planets also requires aspect detection."
            ),
        },
    },
    {
        "yoga_name":     "Ascendant in Uttamamsa with 4+ Aspects — Raja Yoga",
        "sloka":         "ch39-sloka-43",
        "group":         "dignity_raja_yoga",
        "formation":     (
            "The natal ascendant is in Uttamamsa (highest dignity classification "
            "in the Shadvarga / six-divisional scheme) AND is aspected by four "
            "or more planets, among which the Moon should NOT be one."
        ),
        "effect":        "The native will become a king.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["V", "A"],
            "description": (
                "Uttamamsa requires computing all 6 Shadvarga divisional charts "
                "and evaluating cumulative dignity score of the ascendant. "
                "Aspect count (excluding Moon) also requires aspect detection."
            ),
        },
    },
    {
        "yoga_name":     "1 Planet Exalted — Raja Yoga (Partial)",
        "sloka":         "ch39-sloka-44a",
        "group":         "dignity_raja_yoga",
        "formation":     "One planet is in its exaltation sign.",
        "effect":        (
            "A person of royal lineage will become a king. This is the lowest "
            "tier of the exaltation-count Raja Yoga series."
        ),
        "is_benefic":    True,
        "life_domains":  ["status", "royalty"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["D"],
            "description": (
                "Requires checking each planet's sign against its exaltation "
                "sign (Sun=Aries, Moon=Taurus, Mars=Capricorn, Mercury=Virgo, "
                "Jupiter=Cancer, Venus=Pisces, Saturn=Libra). Dignity check "
                "not yet in current engine. Phase 2: new type "
                "'planets_in_dignity_count' with dignity='exaltation', count=1."
            ),
        },
    },
    {
        "yoga_name":     "2 Planets Exalted — Raja Yoga (Medium)",
        "sloka":         "ch39-sloka-44b",
        "group":         "dignity_raja_yoga",
        "formation":     "Two planets are in their respective exaltation signs.",
        "effect":        "The native will be equal to a king.",
        "is_benefic":    True,
        "life_domains":  ["status", "near_royalty"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["D"],
            "description": (
                "Count of exalted planets = 2. Phase 2: "
                "'planets_in_dignity_count' with dignity='exaltation', count=2."
            ),
        },
    },
    {
        "yoga_name":     "3 Planets Exalted — Wealth Yoga",
        "sloka":         "ch39-sloka-44c",
        "group":         "dignity_raja_yoga",
        "formation":     "Three planets are in their respective exaltation signs.",
        "effect":        "The native will be wealthy.",
        "is_benefic":    True,
        "life_domains":  ["wealth"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["D"],
            "description": (
                "Count of exalted planets = 3. Phase 2: "
                "'planets_in_dignity_count' with dignity='exaltation', count=3."
            ),
        },
    },
    {
        "yoga_name":     "4-5 Planets Exalted or Moolatrikona — Raja Yoga",
        "sloka":         "ch39-sloka-45",
        "group":         "dignity_raja_yoga",
        "formation":     (
            "Four or five planets are in their exaltation signs or "
            "Moolatrikona signs."
        ),
        "effect":        "Even a person of base birth will become a king.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["D"],
            "description": (
                "Count of planets in exaltation or Moolatrikona = 4 or 5. "
                "Phase 2: 'planets_in_dignity_count' with "
                "dignity=['exaltation','moolatrikona'], min_count=4, max_count=5."
            ),
        },
    },
    {
        "yoga_name":     "6 Planets Exalted — Emperor Yoga",
        "sloka":         "ch39-sloka-46",
        "group":         "dignity_raja_yoga",
        "formation":     "Six planets are in their exaltation signs.",
        "effect":        "The native will become emperor and will enjoy various royal paraphernalia.",
        "is_benefic":    True,
        "life_domains":  ["status", "emperor", "power"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["D"],
            "description": (
                "Count of exalted planets = 6. Phase 2: "
                "'planets_in_dignity_count' with dignity='exaltation', count=6."
            ),
        },
    },
    {
        "yoga_name":     "Jupiter-Venus-Mercury Exalted with Benefic in Angle — Raja Yoga",
        "sloka":         "ch39-sloka-47",
        "group":         "dignity_raja_yoga",
        "formation":     (
            "At least one among Jupiter, Venus, and Mercury is in its exaltation "
            "sign AND a natural benefic is placed in an angular house "
            "(1st, 4th, 7th, or 10th)."
        ),
        "effect":        "The native will become a king or be equal to a king.",
        "is_benefic":    True,
        "life_domains":  ["status", "royalty"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["D"],
            "description": (
                "The exaltation condition (Jupiter exalted in Cancer, Venus "
                "in Pisces, Mercury in Virgo) requires dignity check. The "
                "benefic-in-angle part alone is checkable but the combined "
                "rule requires dignity. Phase 2: compound type with "
                "dignity check + benefics_in_houses."
            ),
        },
    },
    {
        "yoga_name":     "All Benefics in Angles, Malefics in 3-6-11 — Raja Yoga",
        "sloka":         "ch39-sloka-48",
        "group":         "dignity_raja_yoga",
        "formation":     (
            "All natural benefics are relegated to angular houses (1st, 4th, "
            "7th, 10th) while natural malefics are placed in the 3rd, 6th, and "
            "11th houses (Upachaya houses)."
        ),
        "effect":        (
            "The native, though of mean descent, will ascend the throne."
        ),
        "is_benefic":    True,
        "life_domains":  ["status", "royalty", "power"],
        "yoga_check": {
            "type":      "multi_house_requirements",
            "checkable": True,
            "description": (
                "Benefics in angular houses {1,4,7,10} AND malefics in "
                "upachaya houses {3,6,11}. All conditions purely positional — "
                "no lord or dignity lookup required."
            ),
            "operator": "and",
            "house_requirements": [
                {"houses": [1, 4, 7, 10], "planet_type": "benefic",  "constraint": "present"},
                {"houses": [3, 6, 11],     "planet_type": "malefic",  "constraint": "present"},
            ],
        },
    },
]


# ── Rule builder ──────────────────────────────────────────────────────────────

def build_rule(yoga: dict, index: int) -> dict:
    rule_id      = f"bphs-ch39-{index:03d}"
    yoga_name    = yoga["yoga_name"]
    sloka        = yoga.get("sloka", "")
    group        = yoga.get("group", "raja_yoga")
    is_benefic   = yoga.get("is_benefic", True)
    life_domains = yoga.get("life_domains", [])
    formation    = yoga.get("formation", "")
    effect       = yoga.get("effect", "")
    yoga_check   = yoga.get("yoga_check", {})
    cond_type    = yoga.get("condition_type", "yoga_combination")
    checkable    = yoga_check.get("checkable", False)

    houses = []
    yc_type = yoga_check.get("type", "")
    if yc_type == "benefics_in_houses":
        houses = yoga_check.get("houses", [])
    elif yc_type == "multi_house_requirements":
        for hr in yoga_check.get("house_requirements", []):
            houses.extend(hr.get("houses", []))
        houses = sorted(set(houses))

    group_lbl = {
        "framework":             "Framework",
        "maha_raja_yoga":        "Maha Raja Yoga",
        "karakamsa_raja_yoga":   "Karakamsa & Jaimini Raja Yoga",
        "positional_raja_yoga":  "Positional Raja Yoga",
        "lord_conjunction_yoga": "Lord Conjunction Raja Yoga",
        "birth_time_yoga":       "Birth Time & Named Yogas",
        "mutual_position_yoga":  "Mutual Position Raja Yoga",
        "dignity_raja_yoga":     "Dignity & Count Raja Yoga",
    }.get(group, "Raja Yoga")

    detailed = f"Formation: {formation}\n\nEffect: {effect}".strip()
    tags = ["raja_yoga", f"group:{group}"]
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
            "sub_type":           "yoga_formation",
            "yoga_name":          yoga_name,
            "yoga_group":         group,
            "yoga_group_label":   group_lbl,
            "planets_involved":   [],
            "houses_involved":    houses,
            "sub_conditions":     [],
            "operator":           "and",
            "gender_context":     "neutral",
            "condition_group_id": f"bphs-ch39-{group}",
            "is_group_summary":   False,
            "is_benefic":         is_benefic,
            "yoga_check":         yoga_check,
        },
        "interpretation": {
            "summary":            effect[:120] if effect else "",
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
            "houses_involved":      houses,
            "signs_involved":       [],
            "condition_count":      1,
            "gender_context":       "neutral",
            "condition_group_id":   f"bphs-ch39-{group}",
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
        description="Ingest BPHS Ch 39 Raja Yogas"
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
    checkable = [r for r in rules
                 if r["metadata"]["yoga_checkable"]]
    total = len(rules)

    print(f"\nBPHS Ch {CHAPTER} — {CHAP_NAME}")
    print(f"  Total rules  : {total}")
    print(f"  Checkable    : {len(checkable)} / {total} "
          f"({100 * len(checkable) // total}%)")
    print(f"  Batch ID     : {BATCH_ID}")

    groups: dict[str, int] = {}
    for r in rules:
        g = r["condition"]["yoga_group"]
        groups[g] = groups.get(g, 0) + 1
    print("\n  Groups:")
    for g, n in groups.items():
        print(f"    {g:<30} {n} rules")

    print("\n  Checkable rules:")
    for r in checkable:
        yc = r["condition"]["yoga_check"]
        print(f"    {r['rule_id']}  {r['condition']['yoga_name']}")
        print(f"      type={yc['type']}")

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
        print(f"   python3 scripts/ingest_bphs_ch39_v1.py \\")
        print(f"     --upload {out_path} --mongo-url $MONGO_URL --db-name {args.db_name}")

    if args.dry_run:
        print("\nDetailed rule list:")
        for r in rules:
            yc = r["condition"]["yoga_check"]
            print(f"  {r['rule_id']}  "
                  f"[{'✅' if yc.get('checkable') else '❌'}]  "
                  f"{r['condition']['yoga_name'][:55]}")


if __name__ == "__main__":
    main()
