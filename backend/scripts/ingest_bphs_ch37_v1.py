#!/usr/bin/env python3
"""
ingest_bphs_ch37_v1.py — BPHS Chapter 37: Lunar Yogas

14 rules total:
  3  Moon-Sun position rules     (Sloka 1)
  3  Moon Navamsa rules          (Slokas 2-4)
  1  Adhi Yoga from Moon         (Sloka 5)
  3  Dhana Yoga variants         (Sloka 6)
  3  Sunapha / Anapha / Duradhara (Slokas 7-10)
  1  Kemadruma Yoga              (Slokas 11-13)

Hard-coded from RTF — zero AI extraction cost.
Checkable: 11 / 14 (79%) — highest ratio across all Ch 35-37.

New yoga_check types introduced:
  moon_from_sun_position    — Moon in kendra / panaphara / apoklima from Sun
  planet_in_house_from_moon — non-Sun planet in specific house(s) from Moon
  kemadruma_check           — absence check: no qualifying planet in 3 positions

Standard --save / --upload workflow:
  Step 1 — Dry run:
    python3 scripts/ingest_bphs_ch37_v1.py --dry-run --save scripts/bphs_ch37_rules.json

  Step 2 — Review bphs_ch37_rules.json; amend as needed.

  Step 3 — Upload (zero API calls):
    python3 scripts/ingest_bphs_ch37_v1.py \\
      --upload scripts/bphs_ch37_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 4 — Validate:
    python3 scripts/validate_rules.py \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id bphs-ch37-v1-20260426
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
CHAPTER   = 37
CHAP_NAME = "Lunar Yogas"
BATCH_ID  = "bphs-ch37-v1-20260426"

# ── yoga_check.type legend ────────────────────────────────────────────────────
# moon_from_sun_position    — Moon in kendra/panaphara/apoklima from the Sun
# benefics_in_houses        — benefics in specified houses from Moon (Adhi/Dhana)
# planet_in_house_from_moon — non-Sun planet in specific house(s) from Moon
# kemadruma_check           — absence check: no qualifying planet in any of 3 positions
# complex                   — Navamsa + aspect + birth-time condition; checkable=False

# ── Yoga source data ──────────────────────────────────────────────────────────

YOGA_DATA: list[dict] = [

    # ── 1. MOON IN KENDRA FROM SUN (Sloka 1) ──────────────────────────────────
    {
        "yoga_name":    "Moon in Kendra from Sun",
        "sloka":        "ch37-sl01-kendra",
        "group":        "moon_sun_position",
        "formation":    (
            "The Moon is in an angular position (1st, 4th, 7th, or 10th house) "
            "from the Sun — the Moon's sign is a kendra from the Sun's sign."
        ),
        "effect":       (
            "One's wealth will be little. The kendra placement of the Moon from the "
            "Sun is associated with limited material prosperity, though other chart "
            "factors can modify the outcome."
        ),
        "is_benefic":   False,
        "life_domains": ["wealth"],
        "yoga_check": {
            "type":            "moon_from_sun_position",
            "checkable":       True,
            "position_type":   "kendra",
            "houses_from_sun": [1, 4, 7, 10],
            "description":     (
                "Moon is in angular (kendra) position from the Sun: the Moon's sign "
                "is the 1st, 4th, 7th, or 10th sign counted from the Sun's sign. "
                "Equivalent to Moon being 0°, 90°, 180°, or 270° ahead of the Sun."
            ),
        },
    },

    # ── 2. MOON IN PANAPHARA FROM SUN (Sloka 1) ───────────────────────────────
    {
        "yoga_name":    "Moon in Panaphara from Sun",
        "sloka":        "ch37-sl01-panaphara",
        "group":        "moon_sun_position",
        "formation":    (
            "The Moon is in Panaphara (succedent position: 2nd, 5th, 8th, or 11th "
            "house) from the Sun — the Moon's sign is a Panaphara from the Sun's sign."
        ),
        "effect":       (
            "One's intelligence will be meddling (ordinary / moderate). The Panaphara "
            "position of the Moon from the Sun indicates average intellectual capacity "
            "— neither exceptional nor deficient."
        ),
        "is_benefic":   True,
        "life_domains": ["intelligence"],
        "yoga_check": {
            "type":            "moon_from_sun_position",
            "checkable":       True,
            "position_type":   "panaphara",
            "houses_from_sun": [2, 5, 8, 11],
            "description":     (
                "Moon is in Panaphara (succedent) position from the Sun: the Moon's "
                "sign is the 2nd, 5th, 8th, or 11th from the Sun's sign."
            ),
        },
    },

    # ── 3. MOON IN APOKLIMA FROM SUN (Sloka 1) ────────────────────────────────
    {
        "yoga_name":    "Moon in Apoklima from Sun",
        "sloka":        "ch37-sl01-apoklima",
        "group":        "moon_sun_position",
        "formation":    (
            "The Moon is in Apoklima (cadent position: 3rd, 6th, 9th, or 12th house) "
            "from the Sun — the Moon's sign is an Apoklima from the Sun's sign."
        ),
        "effect":       (
            "One's skill will be excellent. The Apoklima position of the Moon from "
            "the Sun confers exceptional skill, dexterity, and technical mastery in "
            "one's chosen field."
        ),
        "is_benefic":   True,
        "life_domains": ["intelligence", "career"],
        "yoga_check": {
            "type":            "moon_from_sun_position",
            "checkable":       True,
            "position_type":   "apoklima",
            "houses_from_sun": [3, 6, 9, 12],
            "description":     (
                "Moon is in Apoklima (cadent) position from the Sun: the Moon's sign "
                "is the 3rd, 6th, 9th, or 12th from the Sun's sign."
            ),
        },
    },

    # ── 4. MOON NAVAMSA YOGA — DAY BIRTH (Slokas 2-4) ────────────────────────
    {
        "yoga_name":    "Moon Navamsa Yoga (Day Birth)",
        "sloka":        "ch37-sl02-04-day",
        "group":        "moon_navamsa",
        "formation":    (
            "Day birth: The Moon is placed in its own Navamsa or in a friendly "
            "Navamsa (D-9 chart), and is aspected by Jupiter in the Rasi chart."
        ),
        "effect":       (
            "One will be endowed with wealth and happiness. Jupiter's aspect on the "
            "Moon in a favorable Navamsa amplifies prosperity and contentment for "
            "those born during the day."
        ),
        "is_benefic":   True,
        "life_domains": ["wealth", "happiness"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Three simultaneous conditions: (1) Day birth — Sun above horizon at "
                "birth time, (2) Moon in own or friendly Navamsa in D-9 chart, "
                "(3) Jupiter aspects Moon in Rasi chart. Navamsa chart required. "
                "Phase 2 implementation."
            ),
        },
    },

    # ── 5. MOON NAVAMSA YOGA — NIGHT BIRTH (Slokas 2-4) ──────────────────────
    {
        "yoga_name":    "Moon Navamsa Yoga (Night Birth)",
        "sloka":        "ch37-sl02-04-night",
        "group":        "moon_navamsa",
        "formation":    (
            "Night birth: The Moon is placed in its own Navamsa or in a friendly "
            "Navamsa (D-9 chart), and is aspected by Venus in the Rasi chart."
        ),
        "effect":       (
            "One will enjoy similar effects — endowed with wealth and happiness. "
            "Venus's aspect on the Moon in a favorable Navamsa confers prosperity "
            "and contentment for those born during the night."
        ),
        "is_benefic":   True,
        "life_domains": ["wealth", "happiness"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Three simultaneous conditions: (1) Night birth — Sun below horizon "
                "at birth time, (2) Moon in own or friendly Navamsa in D-9 chart, "
                "(3) Venus aspects Moon in Rasi chart. Navamsa chart required. "
                "Phase 2 implementation."
            ),
        },
    },

    # ── 6. MOON NAVAMSA — ADVERSE (Slokas 2-4) ───────────────────────────────
    {
        "yoga_name":    "Moon Navamsa Adverse",
        "sloka":        "ch37-sl02-04-adverse",
        "group":        "moon_navamsa",
        "formation":    (
            "Contrary situation: The Moon is NOT in its own Navamsa or a friendly "
            "Navamsa (Moon in enemy or neutral Navamsa), yet is aspected by Jupiter "
            "(day birth) or Venus (night birth)."
        ),
        "effect":       (
            "The native will have little wealth or even none at all. The auspicious "
            "aspect of Jupiter or Venus cannot overcome the Moon's unfavorable "
            "Navamsa placement."
        ),
        "is_benefic":   False,
        "life_domains": ["wealth"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Moon in enemy or neutral Navamsa (not own or friendly Navamsa) AND "
                "aspected by Jupiter (day birth) or Venus (night birth). Navamsa "
                "chart required for dignity check. Phase 2 implementation."
            ),
        },
    },

    # ── 7. ADHI YOGA FROM THE MOON (Sloka 5) ─────────────────────────────────
    {
        "yoga_name":    "Adhi Yoga (from Moon)",
        "sloka":        "ch37-sl05-adhi",
        "group":        "adhi_yoga",
        "formation":    (
            "Natural benefics (Jupiter, Venus, Mercury) occupy the 6th, 7th, and "
            "8th houses counted from the Moon's sign. Reference point is the Moon, "
            "not the ascendant. Cross-reference: BPHS Ch 36 Sloka 37 Notes describes "
            "the same formation as Chandradhi Yoga (rule bphs-ch36-025) — these are "
            "complementary textual sources for the same yoga."
        ),
        "effect":       (
            "According to the strength of the participating planets, the native will "
            "be either a king, a minister, or an army chief. Stronger benefics in "
            "these positions yield higher social rank and authority."
        ),
        "is_benefic":   True,
        "life_domains": ["royalty", "leadership", "power"],
        "yoga_check": {
            "type":        "benefics_in_houses",
            "checkable":   True,
            "houses":      [6, 7, 8],
            "reference":   "Moon",
            "planet_type": "benefic",
            "description": (
                "Natural benefics (Jupiter, Venus, Mercury) must occupy any of the "
                "6th, 7th, and 8th houses counted from the Moon's sign. Optimal: "
                "all three houses occupied by distinct benefics. Cross-ref: "
                "Chandradhi Yoga (bphs-ch36-025) — identical formation."
            ),
        },
    },

    # ── 8. DHANA YOGA — ALL THREE BENEFICS (Sloka 6) ─────────────────────────
    {
        "yoga_name":    "Dhana Yoga — Full (from Moon)",
        "sloka":        "ch37-sl06-dhana-full",
        "group":        "dhana_yoga",
        "formation":    (
            "All three natural benefics (Jupiter, Venus, Mercury) are placed in "
            "Upachaya houses (3rd, 6th, 10th, or 11th) counted from the Moon."
        ),
        "effect":       (
            "One will be very affluent. All three benefics in Upachaya from the "
            "Moon produces the greatest material prosperity of the three Dhana yoga "
            "variants."
        ),
        "is_benefic":   True,
        "life_domains": ["wealth"],
        "yoga_check": {
            "type":          "benefics_in_houses",
            "checkable":     True,
            "houses":        [3, 6, 10, 11],
            "reference":     "Moon",
            "planet_type":   "benefic",
            "minimum_count": 3,
            "description":   (
                "All three natural benefics (Jupiter, Venus, Mercury) must each be "
                "placed in one of the Upachaya houses (3, 6, 10, 11) counted from "
                "the Moon. All three required for maximum effect."
            ),
        },
    },

    # ── 9. DHANA YOGA — TWO BENEFICS (Sloka 6) ───────────────────────────────
    {
        "yoga_name":    "Dhana Yoga — Medium (from Moon)",
        "sloka":        "ch37-sl06-dhana-medium",
        "group":        "dhana_yoga",
        "formation":    (
            "Exactly two of the three natural benefics (Jupiter, Venus, Mercury) are "
            "placed in Upachaya houses (3rd, 6th, 10th, or 11th) counted from the Moon."
        ),
        "effect":       (
            "One will have medium wealth. Two benefics in Upachaya from the Moon "
            "give moderate prosperity — lesser than the full Dhana yoga but still "
            "materially comfortable."
        ),
        "is_benefic":   True,
        "life_domains": ["wealth"],
        "yoga_check": {
            "type":          "benefics_in_houses",
            "checkable":     True,
            "houses":        [3, 6, 10, 11],
            "reference":     "Moon",
            "planet_type":   "benefic",
            "minimum_count": 2,
            "maximum_count": 2,
            "description":   (
                "Exactly two natural benefics placed in Upachaya houses (3, 6, 10, "
                "11) from the Moon. Third benefic absent from Upachaya."
            ),
        },
    },

    # ── 10. DHANA YOGA — ONE BENEFIC (Sloka 6) ───────────────────────────────
    {
        "yoga_name":    "Dhana Yoga — Weak (from Moon)",
        "sloka":        "ch37-sl06-dhana-weak",
        "group":        "dhana_yoga",
        "formation":    (
            "Only one of the three natural benefics (Jupiter, Venus, Mercury) is "
            "placed in Upachaya houses (3rd, 6th, 10th, or 11th) counted from the Moon."
        ),
        "effect":       (
            "One will have negligible wealth. A single benefic in Upachaya from the "
            "Moon gives only minimal material prosperity — the weakest Dhana yoga variant."
        ),
        "is_benefic":   True,
        "life_domains": ["wealth"],
        "yoga_check": {
            "type":          "benefics_in_houses",
            "checkable":     True,
            "houses":        [3, 6, 10, 11],
            "reference":     "Moon",
            "planet_type":   "benefic",
            "minimum_count": 1,
            "maximum_count": 1,
            "description":   (
                "Only one natural benefic placed in Upachaya houses (3, 6, 10, 11) "
                "from the Moon. Weakest form of Dhana yoga."
            ),
        },
    },

    # ── 11. SUNAPHA YOGA (Slokas 7-10) ───────────────────────────────────────
    {
        "yoga_name":    "Sunapha Yoga",
        "sloka":        "ch37-sl07-10-sunapha",
        "group":        "sunapha_group",
        "formation":    (
            "A planet other than the Sun occupies the 2nd house from the Moon's sign. "
            "Any non-Sun planet (Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu) "
            "in the 2nd from Moon qualifies."
        ),
        "effect":       (
            "One with Sunapha yoga will be a king or equal to a king, endowed with "
            "intelligence, wealth, fame, and self-earned wealth."
        ),
        "is_benefic":   True,
        "life_domains": ["royalty", "wealth", "fame", "intelligence"],
        "yoga_check": {
            "type":            "planet_in_house_from_moon",
            "checkable":       True,
            "house":           2,
            "exclude_planets": ["Sun"],
            "description":     (
                "Any planet except the Sun must occupy the 2nd house counted from "
                "the Moon's sign. Mars, Mercury, Jupiter, Venus, Saturn, Rahu, or "
                "Ketu in the 2nd from Moon qualifies."
            ),
        },
    },

    # ── 12. ANAPHA YOGA (Slokas 7-10) ────────────────────────────────────────
    {
        "yoga_name":    "Anapha Yoga",
        "sloka":        "ch37-sl07-10-anapha",
        "group":        "sunapha_group",
        "formation":    (
            "A planet other than the Sun occupies the 12th house from the Moon's sign."
        ),
        "effect":       (
            "One born in Anapha yoga will be a king, free from diseases, virtuous, "
            "famous, charming, and happy."
        ),
        "is_benefic":   True,
        "life_domains": ["royalty", "health", "fame", "character", "happiness"],
        "yoga_check": {
            "type":            "planet_in_house_from_moon",
            "checkable":       True,
            "house":           12,
            "exclude_planets": ["Sun"],
            "description":     (
                "Any planet except the Sun must occupy the 12th house counted from "
                "the Moon's sign."
            ),
        },
    },

    # ── 13. DURADHARA YOGA (Slokas 7-10) ─────────────────────────────────────
    {
        "yoga_name":    "Duradhara Yoga",
        "sloka":        "ch37-sl07-10-duradhara",
        "group":        "sunapha_group",
        "formation":    (
            "Planets other than the Sun occupy BOTH the 2nd and the 12th houses from "
            "the Moon simultaneously. This is the combined form of Sunapha (planet in "
            "2nd from Moon) and Anapha (planet in 12th from Moon)."
        ),
        "effect":       (
            "One born in Duradhara yoga will enjoy pleasures, be charitable, and be "
            "endowed with wealth, conveyances, and an excellent serving force."
        ),
        "is_benefic":   True,
        "life_domains": ["wealth", "happiness", "character"],
        "yoga_check": {
            "type":            "planet_in_house_from_moon",
            "checkable":       True,
            "houses":          [2, 12],
            "operator":        "and",
            "exclude_planets": ["Sun"],
            "description":     (
                "Non-Sun planets must occupy BOTH the 2nd AND the 12th house from "
                "the Moon simultaneously. Compound of Sunapha + Anapha. Both "
                "positions must be filled by non-Sun planets."
            ),
        },
    },

    # ── 14. KEMADRUMA YOGA (Slokas 11-13) ────────────────────────────────────
    {
        "yoga_name":    "Kemadruma Yoga",
        "sloka":        "ch37-sl11-13-kemadruma",
        "group":        "kemadruma",
        "formation":    (
            "Excluding the Sun, there is no planet in any of these three positions "
            "simultaneously: (1) conjunct the Moon (same sign), (2) in the 2nd or "
            "12th from the Moon, OR (3) in any angular house (1st, 4th, 7th, 10th) "
            "from the ascendant. All three absence conditions must hold."
        ),
        "effect":       (
            "One born in Kemadruma yoga will be very much reproached, bereft of "
            "intelligence and learning, and reduced to penury and perils."
        ),
        "is_benefic":   False,
        "life_domains": ["hardship", "poverty", "intelligence"],
        "yoga_check": {
            "type":        "kemadruma_check",
            "checkable":   True,
            "description": (
                "Negative / absence check — the yoga forms when ALL three conditions "
                "are absent simultaneously: (1) no non-Sun planet conjunct the Moon, "
                "(2) no non-Sun planet in the 2nd or 12th from the Moon, "
                "(3) no planet (including Sun) in angular houses (1, 4, 7, 10) from "
                "the ascendant. Sun is excluded from conditions 1 and 2."
            ),
            "absent_conditions": [
                "non_sun_planet_conjunct_moon",
                "non_sun_planet_in_2nd_or_12th_from_moon",
                "any_planet_in_angle_from_ascendant",
            ],
        },
    },
]

# ── Group labels ──────────────────────────────────────────────────────────────

GROUP_LABEL: dict[str, str] = {
    "moon_sun_position": "Moon-Sun Position Yogas",
    "moon_navamsa":      "Moon Navamsa Yogas",
    "adhi_yoga":         "Adhi Yoga (from Moon)",
    "dhana_yoga":        "Dhana Yoga (from Moon)",
    "sunapha_group":     "Sunapha / Anapha / Duradhara",
    "kemadruma":         "Kemadruma Yoga",
}

# ── build_rule ────────────────────────────────────────────────────────────────

def build_rule(yoga: dict, index: int) -> dict:
    rule_id   = f"bphs-ch37-{index:03d}"
    group     = yoga["group"]
    group_lbl = GROUP_LABEL.get(group, group)
    yoga_name = yoga["yoga_name"]
    is_ben    = yoga["is_benefic"]
    formation = yoga["formation"]
    effect    = yoga["effect"]
    domains   = yoga["life_domains"]
    yc        = yoga["yoga_check"]
    sloka     = yoga.get("sloka", f"ch37-{yoga_name.lower().replace(' ', '-')}")
    checkable = yc.get("checkable", False)

    # ── Derive houses / planets from yoga_check ───────────────────────────────
    houses: list[int] = []
    if "house" in yc:
        houses = [yc["house"]]
    elif "houses" in yc:
        houses = list(yc["houses"])
    elif "houses_from_sun" in yc:
        houses = list(yc["houses_from_sun"])

    planets: list[str] = []

    # ── Interpretation text ───────────────────────────────────────────────────
    detailed = (
        f"Yoga: {yoga_name} [{group_lbl}]\n\n"
        f"Formation: {formation}\n\n"
        f"Effect: {effect}"
    )
    summary_effect = effect[:200] + ("..." if len(effect) > 200 else "")
    summary = f"{yoga_name} — {summary_effect}"

    # ── Tags ──────────────────────────────────────────────────────────────────
    sentiment = "benefic" if is_ben else "malefic"
    tags = [
        "verbatim", "yoga", "chapter37",
        "yoga_combination", "yoga_formation",
        f"group:bphs-ch37-{group}",
        sentiment,
    ]
    if checkable:
        tags.append("yoga_checkable")

    return {
        "rule_id":    rule_id,
        "science_id": SCIENCE,
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
            "type":               "yoga_combination",
            "sub_type":           "yoga_formation",
            "yoga_name":          yoga_name,
            "yoga_group":         group,
            "yoga_group_label":   group_lbl,
            "planets_involved":   planets,
            "houses_involved":    houses,
            "sub_conditions":     [],
            "operator":           "and",
            "gender_context":     "neutral",
            "condition_group_id": f"bphs-ch37-{group}",
            "is_group_summary":   False,
            "is_benefic":         is_ben,
            "yoga_check":         yc,
        },
        "interpretation": {
            "summary":            summary,
            "detailed":           detailed,
            "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
            "remedies":           [],
            "life_domain":        domains[0] if domains else "general",
            "life_domains":       domains,
            "tags":               tags,
            "physical_markers":   [],
        },
        "metadata": {
            "planets_involved":     planets,
            "houses_involved":      houses,
            "signs_involved":       [],
            "condition_count":      1,
            "gender_context":       "neutral",
            "condition_group_id":   f"bphs-ch37-{group}",
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


# ── MongoDB insert ────────────────────────────────────────────────────────────

def insert_rules_to_mongo(all_rules: list[dict], mongo_url: str, db_name: str) -> None:
    from pymongo import MongoClient
    client = MongoClient(mongo_url)
    col    = client[db_name]["interpretation_rules"]
    existing = col.count_documents({"source.batch_id": BATCH_ID})
    if existing:
        print(f"\n⚠  Batch '{BATCH_ID}' already has {existing} rules in MongoDB.")
        print("   Nothing inserted. Drop the batch first if you want to re-ingest.")
        client.close()
        return
    result = col.insert_many(all_rules, ordered=False)
    print(f"\n✅  Inserted {len(result.inserted_ids)} rules into MongoDB")
    print(f"   batch_id : {BATCH_ID}")
    client.close()


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest BPHS Ch 37 Lunar Yogas into Knowledge Engine"
    )
    parser.add_argument("--mongo-url", default=None)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--dry-run",   action="store_true")
    parser.add_argument("--save",      default=None, metavar="FILE")
    parser.add_argument("--upload",    default=None, metavar="FILE")
    args = parser.parse_args()

    # ── --upload path ──────────────────────────────────────────────────────────
    if args.upload:
        if not args.mongo_url:
            print("⚠  --upload requires --mongo-url"); sys.exit(1)
        p = Path(args.upload)
        if not p.exists():
            print(f"⚠  File not found: {args.upload}"); sys.exit(1)
        with open(p, encoding="utf-8") as fh:
            all_rules = json.load(fh)
        print(f"\n✅  Loaded {len(all_rules)} rules from {args.upload}")
        insert_rules_to_mongo(all_rules, args.mongo_url, args.db_name)
        print(f"\n   Validate with:")
        print(f"   python3 scripts/validate_rules.py --mongo-url $MONGO_URL \\")
        print(f"     --db-name {args.db_name} --batch-id {BATCH_ID}")
        return

    # ── Build rules ────────────────────────────────────────────────────────────
    all_rules: list[dict] = []
    for idx, yoga in enumerate(YOGA_DATA, start=1):
        all_rules.append(build_rule(yoga, idx))

    total     = len(all_rules)
    benefic   = sum(1 for r in all_rules if r["condition"]["is_benefic"])
    adverse   = total - benefic
    checkable = sum(1 for r in all_rules if r["metadata"]["yoga_checkable"])

    # Group breakdown
    groups: dict[str, int] = {}
    for r in all_rules:
        g = r["condition"].get("yoga_group", "other")
        groups[g] = groups.get(g, 0) + 1

    print(f"\n{'─' * 65}")
    print(f"BPHS Chapter {CHAPTER} — {CHAP_NAME}  [v1 hard-coded]")
    print(f"batch_id : {BATCH_ID}")
    print(f"{'─' * 65}")
    print(f"\nGroup breakdown:")
    for g, cnt in groups.items():
        print(f"  {GROUP_LABEL.get(g, g):<32} : {cnt}")
    print(f"  {'─' * 39}")
    print(f"  {'TOTAL':<32} : {total}")
    print(f"\nBenefic rules  : {benefic}")
    print(f"Adverse rules  : {adverse}")
    print(f"Yoga-checkable : {checkable} / {total}")

    # Sample output
    print(f"\nSample rules (first 3):")
    print("─" * 65)
    for r in all_rules[:3]:
        cond = r["condition"]
        yc   = cond.get("yoga_check", {})
        print(f"  rule_id   : {r['rule_id']}")
        print(f"  yoga      : {cond['yoga_name']}  [{cond['yoga_group_label']}]")
        print(f"  check_type: {yc.get('type','—'):<28}  checkable={yc.get('checkable',False)}")
        print(f"  is_benefic: {cond['is_benefic']}")
        print(f"  summary   : {r['interpretation']['summary'][:100]}...")
        print()

    print(f"Isolation: approval_status='pending_review' — zero rules reach live users")

    if not args.dry_run and not args.save:
        if not args.mongo_url:
            print(f"\n⚠  Live run requires --mongo-url  (or use --dry-run / --upload)")
            sys.exit(1)
        insert_rules_to_mongo(all_rules, args.mongo_url, args.db_name)
        print(f"\n   Validate with:")
        print(f"   python3 scripts/validate_rules.py --mongo-url $MONGO_URL \\")
        print(f"     --db-name horoscope_db --batch-id {BATCH_ID}")
        return

    if args.save:
        save_path = Path(args.save)
        with open(save_path, "w", encoding="utf-8") as fh:
            json.dump(all_rules, fh, indent=2, ensure_ascii=False, default=str)
        print(f"\n✅  Rules saved to {args.save}  ({total} rules)")
        print(f"   Review the file, then upload with:")
        print(f"   python3 scripts/ingest_bphs_ch37_v1.py \\")
        print(f"     --upload {args.save} --mongo-url $MONGO_URL --db-name {args.db_name}")


if __name__ == "__main__":
    main()
