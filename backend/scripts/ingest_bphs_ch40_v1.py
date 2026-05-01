#!/usr/bin/env python3
"""
ingest_bphs_ch40_v1.py — BPHS Chapter 40: Yogas for Royal Association

15 rules total across 4 groups:
  7  Court & Ministerial Yogas     (Slokas 1-6, 9, 15)
  1  Army Chief Yoga               (Sloka 7)
  6  Royal Association Yogas       (Slokas 8, 10, 11, 12, 13)
  1  Royal Insignia Yoga           (Sloka 14)

Hard-coded from PDF + Notebook LM decode — zero AI extraction cost.
Checkable: 0 / 15 (0%) — chapter is entirely Jaimini-based:
  Amatyakaraka, Atmakaraka, Karakamsa Lagna, Arudha Lagna.
  None of these are computable by the current Rasi-chart engine.

Note: Sloka 48 visible at the top of the PDF page belongs to Ch 39
(already ingested as bphs-ch39-050 "All Benefics in Angles, Malefics
in 3-6-11"). It is NOT a Ch 40 rule.

Blocker legend:
  K = Karakamsa / Jaimini (Atmakaraka, Amatyakaraka, Arudha Lagna,
      Karakamsa Lagna — all require Jaimini karaka computation)
  L = House lord identification required
  A = Aspect detection required
  D = Dignity / strength check required

Standard --save / --upload workflow:
  Step 1 — Dry run:
    python3 scripts/ingest_bphs_ch40_v1.py --dry-run --save scripts/bphs_ch40_rules.json

  Step 2 — Review bphs_ch40_rules.json; amend as needed.

  Step 3 — Upload (zero API calls):
    python3 scripts/ingest_bphs_ch40_v1.py \\
      --upload scripts/bphs_ch40_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 4 — Validate:
    python3 scripts/validate_rules.py \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id bphs-ch40-v1-20260502
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
CHAPTER   = 40
CHAP_NAME = "Yogas for Royal Association"
BATCH_ID  = "bphs-ch40-v1-20260502"

# ── Yoga source data ──────────────────────────────────────────────────────────

YOGA_DATA: list[dict] = [

    # ═══════════════════════════════════════════════════════════════════════════
    # 1. COURT & MINISTERIAL YOGAS (Slokas 1–6, 9, 15)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":     "Chief in King's Court — Amatyakaraka Connection",
        "sloka":         "ch40-sloka-01",
        "group":         "court_ministerial_yoga",
        "condition_type": "yoga_combination",
        "formation":     (
            "The 10th lord counted from the ascendant is conjunct or aspected "
            "by the dispositor of Amatyakaraka (the lord of the sign occupied "
            "by Amatyakaraka), OR the 10th lord is conjunct or aspected by "
            "Amatyakaraka himself. Amatyakaraka is the Chara Karaka that is the "
            "immediate successor of the Atmakaraka (second highest degree planet "
            "among Sun through Saturn)."
        ),
        "effect":        (
            "The native will be a chief in the king's court. In modern terms: "
            "a high governmental position, senior civil service, or chief of a "
            "major organisation. The Amatyakaraka taking the role of its "
            "dispositor yields similar effects."
        ),
        "is_benefic":    True,
        "life_domains":  ["status", "government", "power", "leadership"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "L", "A"],
            "description": (
                "Requires identifying Amatyakaraka (second highest degree planet "
                "— Jaimini Chara Karaka computation), then its dispositor (lord "
                "of AK's sign), then the 10th lord from ascendant. Finally, "
                "conjunction or aspect relationship between 10th lord and "
                "AK/AK-dispositor. All three steps outside current engine scope."
            ),
        },
    },
    {
        "yoga_name":     "Chief in King's Court — Clean House Diagnostic",
        "sloka":         "ch40-sloka-02",
        "group":         "court_ministerial_yoga",
        "condition_type": "yoga_combination",
        "formation":     (
            "The 10th and 11th houses are both devoid of malefic occupation "
            "and malefic aspect. The 11th house is aspected by its own lord "
            "(the planet that rules the 11th house sign). Alternate interpretation: "
            "the 10th house should additionally be aspected by its own lord, "
            "and both the 10th and 11th should be simultaneously free from "
            "malefic aspect and occupation."
        ),
        "effect":        (
            "The native will be a chief in the king's court. The 'purity' of "
            "the Karma (10th) and Gains (11th) houses is the key diagnostic — "
            "if any malefic occupies or aspects these houses the result is "
            "voided unless overridden by Amatyakaraka strength."
        ),
        "is_benefic":    True,
        "life_domains":  ["status", "government", "leadership", "gains"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["L", "A"],
            "description": (
                "Requires identifying the 11th lord (and optionally the 10th "
                "lord) — house lord identification needed. Malefic "
                "aspect/occupation check requires aspect detection across both "
                "houses. Phase 2: implement with lord-identification engine."
            ),
        },
    },
    {
        "yoga_name":     "King's Minister — Amatyakaraka + Atmakaraka Dispositor Conjunction",
        "sloka":         "ch40-sloka-03",
        "group":         "court_ministerial_yoga",
        "condition_type": "yoga_combination",
        "formation":     (
            "Amatyakaraka (second highest degree planet, Chara Karaka) and the "
            "dispositor of Atmakaraka (lord of the sign occupied by Atmakaraka, "
            "the highest degree planet) are conjunct in the same house."
        ),
        "effect":        (
            "The native will be endowed with great intelligence and will be "
            "a king's minister. The conjunction of these two Jaimini anchor "
            "planets produces both intellectual distinction and high governmental "
            "service."
        ),
        "is_benefic":    True,
        "life_domains":  ["status", "government", "intelligence"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K"],
            "description": (
                "Requires identifying Atmakaraka (highest degree planet among "
                "Sun–Saturn), its dispositor (lord of AK's sign), and "
                "Amatyakaraka (second highest degree). Both are Jaimini Chara "
                "Karaka computations outside current engine scope."
            ),
        },
    },
    {
        "yoga_name":     "King's Minister — Dignified Amatyakaraka",
        "sloka":         "ch40-sloka-04",
        "group":         "court_ministerial_yoga",
        "condition_type": "yoga_combination",
        "formation":     (
            "Condition A: Amatyakaraka is strong (well-placed or in a powerful "
            "position) AND is conjunct a natural benefic planet. "
            "Condition B (alternate): Amatyakaraka is in its own house "
            "(the sign it rules) OR in its exaltation sign. "
            "Either condition is sufficient."
        ),
        "effect":        "The native will surely become a king's minister.",
        "is_benefic":    True,
        "life_domains":  ["status", "government"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "D"],
            "description": (
                "Requires identifying Amatyakaraka (Jaimini). Condition A "
                "requires a general 'strength' assessment of AK's placement. "
                "Condition B requires checking AK's dignity (own sign or "
                "exaltation) — both Jaimini identification and dignity check "
                "outside current engine scope."
            ),
        },
    },
    {
        "yoga_name":     "Famous King's Minister — Amatyakaraka in 1st/5th/9th",
        "sloka":         "ch40-sloka-05",
        "group":         "court_ministerial_yoga",
        "condition_type": "yoga_combination",
        "formation":     (
            "Amatyakaraka (second highest degree Chara Karaka) is placed in "
            "the ascendant (1st house), the 5th house, or the 9th house "
            "counted from the natal ascendant."
        ),
        "effect":        (
            "There is no doubt in the native becoming a king's minister and "
            "famous. Placement in the ascendant (personal power), 5th "
            "(intelligence, purva punya), or 9th (luck, dharma, fortune) "
            "from Lagna gives the highest ministerial distinction."
        ),
        "is_benefic":    True,
        "life_domains":  ["status", "government", "fame"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K"],
            "description": (
                "Requires identifying Amatyakaraka (second highest degree planet "
                "— Jaimini Chara Karaka). Once identified, house position check "
                "against houses 1, 5, 9 would be straightforward. Phase 2: "
                "implement as 'planet_in_house' with planets=['Amatyakaraka'] "
                "and houses=[1,5,9] once AK identification is available."
            ),
        },
    },
    {
        "yoga_name":     "Royal Patronage & Happiness — Amatyakaraka or Atmakaraka in Angle/Trine",
        "sloka":         "ch40-sloka-06",
        "group":         "court_ministerial_yoga",
        "condition_type": "yoga_combination",
        "formation":     (
            "Amatyakaraka OR Atmakaraka (the two primary Jaimini Chara Karakas) "
            "is placed in an angular house (1st, 4th, 7th, or 10th) or in a "
            "trinal house (1st, 5th, or 9th) counted from the natal ascendant."
        ),
        "effect":        (
            "The native will beget royal mercy, royal patronage, and happiness "
            "therefrom. In modern context: government favour, institutional "
            "support, and professional satisfaction through association with "
            "powerful figures."
        ),
        "is_benefic":    True,
        "life_domains":  ["status", "government", "wealth", "happiness"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K"],
            "description": (
                "Requires identifying both Atmakaraka (highest degree planet) "
                "and Amatyakaraka (second highest degree). Angular houses "
                "{1,4,7,10} and trinal houses {1,5,9} checks are "
                "straightforward once the karaka planets are identified. "
                "Phase 2: implement with Jaimini karaka engine."
            ),
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 2. ARMY CHIEF YOGA (Sloka 7)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":     "Army Chief — Malefics in 3rd and 6th from AK/AL/Ascendant",
        "sloka":         "ch40-sloka-07",
        "group":         "army_yoga",
        "condition_type": "yoga_combination",
        "formation":     (
            "Natural malefic planets are placed in the 3rd and 6th houses "
            "counted from any one of three reference points: "
            "(A) the Atmakaraka's house position, "
            "(B) the Arudha Lagna (the Pada of the 1st house, derived via "
            "Jaimini counting algorithm), or "
            "(C) the natal ascendant (Lagna). "
            "Unlike court positions which require clean houses (free of "
            "malefics), military leadership specifically requires malefics in "
            "the 3rd (courage, conflict) and 6th (enemies, warfare) positions."
        ),
        "effect":        (
            "The native will become an army chief. The 3rd and 6th house "
            "malefic placement from the key pivot (AK, AL, or Lagna) is the "
            "diagnostic for military authority — inversely, the same positions "
            "that would harm courtly functions enable warrior leadership."
        ),
        "is_benefic":    True,
        "life_domains":  ["military", "leadership", "power", "enemies"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K"],
            "description": (
                "The natal ascendant (C) reference is straightforward — malefics "
                "in houses 3 and 6 is a pure positional check. However, the "
                "Atmakaraka (A) and Arudha Lagna (B) reference points require "
                "Jaimini computation: AK = highest degree planet; AL = derived "
                "via counting the Lagna lord's distance from Lagna and then "
                "counting same distance from the lord. The OR structure across "
                "three pivots keeps this rule complex/False. Phase 2: split "
                "into three sub-rules once AK + AL are available."
            ),
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 3. ROYAL ASSOCIATION YOGAS (Slokas 8, 10, 11, 12, 13)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":     "King's Minister — Atmakaraka Strong + 9th Lord Aspect",
        "sloka":         "ch40-sloka-08",
        "group":         "royal_association_yoga",
        "condition_type": "yoga_combination",
        "formation":     (
            "Atmakaraka (highest degree planet, Chara Karaka) is placed in an "
            "angular house (1st, 4th, 7th, or 10th), a trinal house (1st, 5th, "
            "or 9th), in its exaltation sign, or in its own sign — AND is "
            "simultaneously aspected by the 9th lord (the planet ruling the "
            "9th house sign). Both conditions must hold: AK in strength AND "
            "9th lord's aspect."
        ),
        "effect":        (
            "The native will be a king's minister. The 9th lord's aspect "
            "provides the dharmic sanction (fortune, luck, higher wisdom) that "
            "elevates the Atmakaraka's strength into ministerial authority."
        ),
        "is_benefic":    True,
        "life_domains":  ["status", "government", "fortune"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "L", "A"],
            "description": (
                "Requires identifying Atmakaraka (Jaimini). Angle/trine check "
                "is straightforward once AK is identified. Exaltation/own-sign "
                "check requires dignity evaluation. The 9th lord identification "
                "and its aspect to AK require lord lookup + aspect detection. "
                "All three blockers must be cleared for Phase 2 promotion."
            ),
        },
    },
    {
        "yoga_name":     "King's Minister at Advanced Age — Moon Sign Lord as Atmakaraka",
        "sloka":         "ch40-sloka-09",
        "group":         "court_ministerial_yoga",
        "condition_type": "yoga_combination",
        "formation":     (
            "The lord of the Moon's natal sign (the planet that rules the sign "
            "where the Moon is placed in the birth chart) is itself the "
            "Atmakaraka (the highest degree planet among Sun through Saturn). "
            "This same planet — simultaneously the Moon sign lord and the "
            "Atmakaraka — is placed in the natal ascendant (1st house) and is "
            "conjunct a natural benefic."
        ),
        "effect":        (
            "The native will become a king's minister at his advanced age. "
            "This 'advanced age' timing is specific to this combination — the "
            "dual role of the planet (Moon sign lord + Atmakaraka) delays the "
            "maturation of ministerial authority until later life."
        ),
        "is_benefic":    True,
        "life_domains":  ["status", "government", "career", "timing"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K"],
            "description": (
                "Requires identifying: (1) Moon sign lord (which planet rules "
                "the sign where Moon is placed — lord identification), (2) "
                "Atmakaraka (highest degree planet — Jaimini), (3) confirming "
                "they are the same planet. The ascendant placement and benefic "
                "conjunction would then be straightforward positional checks. "
                "Phase 2: implement once lord identification + AK engine exist."
            ),
        },
    },
    {
        "yoga_name":     "Wealth Through Royal Patronage — Atmakaraka in Trikona/Kendra with Benefic",
        "sloka":         "ch40-sloka-10",
        "group":         "royal_association_yoga",
        "condition_type": "yoga_combination",
        "formation":     (
            "Atmakaraka (highest degree Chara Karaka) is placed in the 5th, "
            "7th, 10th, or 9th house from the natal ascendant AND is conjunct "
            "a natural benefic planet. Both conditions (house placement AND "
            "benefic conjunction) must hold simultaneously."
        ),
        "effect":        (
            "The native will earn wealth through royal patronage. Association "
            "with powerful figures (king, government, authority) becomes the "
            "vehicle for material prosperity."
        ),
        "is_benefic":    True,
        "life_domains":  ["wealth", "royal_patronage", "government"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K"],
            "description": (
                "Requires identifying Atmakaraka (Jaimini). Once identified, "
                "house position check (5th, 7th, 9th, 10th) and benefic "
                "conjunction check are straightforward. Phase 2: implement as "
                "compound check 'planet_in_house' (AK) + conjunction with "
                "benefic once AK identification is available."
            ),
        },
    },
    {
        "yoga_name":     "Association with Royal Circles — Arudha of 9th or AK in 9th",
        "sloka":         "ch40-sloka-11",
        "group":         "royal_association_yoga",
        "condition_type": "yoga_combination",
        "formation":     (
            "Condition A: The Arudha of the 9th house (the Pada derived by "
            "counting the 9th lord's distance from the 9th house, then counting "
            "the same distance from the 9th lord) coincides with the natal "
            "ascendant sign. "
            "Condition B (alternate): Atmakaraka (highest degree planet) is "
            "placed in the 9th house from the natal ascendant. "
            "Either condition is sufficient."
        ),
        "effect":        (
            "The native will be associated with royal circles. The 9th house "
            "connection (via its Pada or via the Atmakaraka's placement) links "
            "the native to fortune, higher authority, and powerful social networks."
        ),
        "is_benefic":    True,
        "life_domains":  ["status", "social_position", "government", "fortune"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "L"],
            "description": (
                "Condition A requires Arudha (Pada) derivation for the 9th "
                "house — a Jaimini counting algorithm requiring 9th lord "
                "identification. Condition B (AK in 9th) requires Atmakaraka "
                "identification. Phase 2: Condition B alone becomes checkable "
                "once AK identification is available."
            ),
        },
    },
    {
        "yoga_name":     "Gain Through Royal Association — 11th Lord in 11th + AK with Benefic",
        "sloka":         "ch40-sloka-12",
        "group":         "royal_association_yoga",
        "condition_type": "yoga_combination",
        "formation":     (
            "Three simultaneous conditions: "
            "(1) The 11th house is occupied by its own lord (the planet that "
            "rules the 11th house sign is placed in the 11th house itself). "
            "(2) The 11th house is devoid of any malefic aspect. "
            "(3) Atmakaraka is conjunct a natural benefic planet. "
            "All three conditions must hold together."
        ),
        "effect":        (
            "The native will gain through royal association — material rewards, "
            "wealth, and advancement through connection with the powerful. "
            "The 11th house (gains/income) must be pure and strengthened by "
            "its own lord while the Atmakaraka's benefic support provides "
            "the social conduit."
        ),
        "is_benefic":    True,
        "life_domains":  ["wealth", "gains", "government", "status"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "L", "A"],
            "description": (
                "Condition 1 requires 11th lord identification (L). "
                "Condition 2 requires malefic aspect detection on house 11 (A). "
                "Condition 3 requires Atmakaraka identification (K). All three "
                "blockers active. Phase 2: conditions 1+2 become checkable once "
                "lord identification + aspect detection are available; condition "
                "3 requires Jaimini engine."
            ),
        },
    },
    {
        "yoga_name":     "Highly Associated with the King — 10th-Ascendant Lord Sign Exchange",
        "sloka":         "ch40-sloka-13",
        "group":         "royal_association_yoga",
        "condition_type": "yoga_combination",
        "formation":     (
            "An exchange of signs (Parivartana Yoga) between the 10th lord and "
            "the ascendant lord: the 10th lord is placed in the sign of the "
            "ascendant lord, AND the ascendant lord is placed in the sign of "
            "the 10th lord. Both lords must simultaneously occupy each other's "
            "signs."
        ),
        "effect":        (
            "The native will be highly associated with the king — the strongest "
            "possible royal connection yoga in this chapter. In modern context: "
            "deep integration into government, powerful institutional backing, "
            "or direct access to heads of state or major organisations."
        ),
        "is_benefic":    True,
        "life_domains":  ["status", "government", "royalty", "power"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["L"],
            "description": (
                "Requires identifying the 10th lord and the ascendant lord — "
                "house lord identification for both. Sign exchange (Parivartana) "
                "verification is then a positional check (is 10th lord in Lagna "
                "lord's sign AND Lagna lord in 10th lord's sign?). Phase 2: "
                "implement as 'lord_exchange' yoga_check type (same as used "
                "for TBA Ch 16 Vipreet Rajyoga variants) once lord "
                "identification is available."
            ),
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 4. ROYAL INSIGNIA YOGA (Sloka 14)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":     "Royal Insignia — Venus and Moon in 4th from Karakamsa Lagna",
        "sloka":         "ch40-sloka-14",
        "group":         "royal_insignia_yoga",
        "condition_type": "yoga_combination",
        "formation":     (
            "Venus and the Moon are both placed in the 4th house counted from "
            "the Karakamsa Lagna (the Navamsa sign occupied by the Atmakaraka, "
            "i.e., the sign of the Atmakaraka in the D-9 divisional chart, "
            "used as the ascendant for Jaimini analysis)."
        ),
        "effect":        (
            "The native will be endowed with royal insignia — symbols of "
            "authority, official titles, ceremonial objects, and distinctions "
            "of rank. The combination of Venus (luxury, beauty, authority "
            "symbols) and Moon (mind, public image) in the 4th from Karakamsa "
            "gives tangible tokens of royal or governmental recognition."
        ),
        "is_benefic":    True,
        "life_domains":  ["status", "royalty", "honors", "recognition"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "V"],
            "description": (
                "Karakamsa Lagna requires: (1) identifying Atmakaraka (highest "
                "degree planet — Jaimini), (2) computing the D-9 Navamsa chart, "
                "(3) finding the Navamsa sign of the Atmakaraka. Houses are "
                "then counted from this Karakamsa Lagna. Both Jaimini (K) and "
                "divisional chart (V) blockers active — cannot be promoted "
                "until both are resolved."
            ),
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 5. COURT MINISTERIAL — continued (Sloka 15)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":     "King's Minister — Ascendant Lord or Atmakaraka + 5th Lord in Angle/Trine",
        "sloka":         "ch40-sloka-15",
        "group":         "court_ministerial_yoga",
        "condition_type": "yoga_combination",
        "formation":     (
            "The ascendant lord OR the Atmakaraka (highest degree Chara Karaka) "
            "is conjunct the 5th lord (the planet ruling the 5th house sign), "
            "AND this conjunction is placed in an angular house (1st, 4th, 7th, "
            "or 10th) or a trinal house (1st, 5th, or 9th) from the natal "
            "ascendant. Both the conjunction AND the angular/trinal placement "
            "must hold."
        ),
        "effect":        (
            "The native will be a king's minister. The 5th lord (intelligence, "
            "counsel, purva punya) joining the self (ascendant lord) or soul "
            "(Atmakaraka) in a power position (angle or trine) channels "
            "intellectual authority into ministerial service."
        ),
        "is_benefic":    True,
        "life_domains":  ["status", "government", "intelligence", "counsel"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "blockers":  ["K", "L"],
            "description": (
                "Requires: (1) ascendant lord identification (L), (2) "
                "Atmakaraka identification (K — Jaimini), (3) 5th lord "
                "identification (L). The conjunction and angle/trine placement "
                "are then positional checks. Phase 2: the ascendant-lord branch "
                "becomes checkable once lord identification is available "
                "(AK branch still requires Jaimini engine)."
            ),
        },
    },
]


# ── Rule builder ──────────────────────────────────────────────────────────────

def build_rule(yoga: dict, index: int) -> dict:
    rule_id      = f"bphs-ch40-{index:03d}"
    yoga_name    = yoga["yoga_name"]
    sloka        = yoga.get("sloka", "")
    group        = yoga.get("group", "royal_association_yoga")
    is_benefic   = yoga.get("is_benefic", True)
    life_domains = yoga.get("life_domains", [])
    formation    = yoga.get("formation", "")
    effect       = yoga.get("effect", "")
    yoga_check   = yoga.get("yoga_check", {})
    cond_type    = yoga.get("condition_type", "yoga_combination")
    checkable    = yoga_check.get("checkable", False)

    group_lbl = {
        "court_ministerial_yoga": "Court & Ministerial Yoga",
        "army_yoga":              "Army Chief Yoga",
        "royal_association_yoga": "Royal Association Yoga",
        "royal_insignia_yoga":    "Royal Insignia Yoga",
    }.get(group, "Royal Association Yoga")

    detailed = f"Formation: {formation}\n\nEffect: {effect}".strip()
    tags = ["royal_association_yoga", f"group:{group}"]
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
            "houses_involved":    [],
            "sub_conditions":     [],
            "operator":           "and",
            "gender_context":     "neutral",
            "condition_group_id": f"bphs-ch40-{group}",
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
            "houses_involved":      [],
            "signs_involved":       [],
            "condition_count":      1,
            "gender_context":       "neutral",
            "condition_group_id":   f"bphs-ch40-{group}",
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
        description="Ingest BPHS Ch 40 Yogas for Royal Association"
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
            "court_ministerial_yoga": "Court & Ministerial Yoga",
            "army_yoga":              "Army Chief Yoga",
            "royal_association_yoga": "Royal Association Yoga",
            "royal_insignia_yoga":    "Royal Insignia Yoga",
        }.get(g, g)
        print(f"    {lbl:<35} {n} rules")

    print("\n  All rules (checkable status):")
    for r in rules:
        yc = r["condition"]["yoga_check"]
        mark = "✅" if yc.get("checkable") else "❌"
        blockers = yc.get("blockers", [])
        print(f"    {r['rule_id']}  [{mark}]  "
              f"{r['condition']['yoga_name'][:55]}"
              f"  blockers={blockers}")

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
        print(f"   python3 scripts/ingest_bphs_ch40_v1.py \\")
        print(f"     --upload {out_path} --mongo-url $MONGO_URL --db-name {args.db_name}")

    if args.dry_run:
        print("\n  [dry-run complete]")


if __name__ == "__main__":
    main()
