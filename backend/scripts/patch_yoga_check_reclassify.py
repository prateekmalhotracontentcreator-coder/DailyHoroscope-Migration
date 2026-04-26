#!/usr/bin/env python3
"""
Patch: yoga_check type reclassification — complex → multi_house_requirements
=============================================================================

Promotes four rules whose yoga_check conditions are fully positional (checkable
purely from Rasi chart planet positions) but were incorrectly tagged `complex`.

Rules patched
-------------
bphs-ch35-011  Vajra Yoga    complex/False → multi_house_requirements/True
bphs-ch35-012  Yava Yoga     complex/False → multi_house_requirements/True
bphs-ch36-006  Parvata Yoga  complex/False → multi_house_requirements/True
bphs-ch36-014  Matsya Yoga   complex/True  → multi_house_requirements/True  (type rename only)

New type: multi_house_requirements
-----------------------------------
Applies when yoga detection requires simultaneously evaluating planet-type
occupancy across multiple distinct house groups. Each entry in `house_requirements`
specifies:
  houses        : list of house numbers
  planet_type   : "benefic" | "malefic" | "mixed"
  constraint    : "present" (≥1 planet of type in any of houses; DEFAULT)
                  "absent"  (0 planets of type in any of houses)

All requirements are joined by `operator` (default "and").

constraint semantics
--------------------
"present"  — at least one natural planet of planet_type occupies any of the
             listed houses.
"absent"   — no natural planet of planet_type occupies any of the listed houses.

Usage
-----
python3 backend/scripts/patch_yoga_check_reclassify.py \\
    --mongo-url "$MONGO_URL" --db-name horoscope_db

Run from: ~/DailyHoroscope-Migration  (repo root)
"""

import argparse
import sys
from datetime import datetime, timezone
from pymongo import MongoClient

PATCH_NOTES = "yoga_check reclassification: complex → multi_house_requirements (26 Apr 2026)"

PATCHES = [
    # ── Ch 35 ────────────────────────────────────────────────────────────────
    {
        "rule_id": "bphs-ch35-011",
        "yoga_name": "Vajra Yoga",
        "new_yoga_check": {
            "type": "multi_house_requirements",
            "checkable": True,
            "description": (
                "Natural benefics placed in houses 1 and 7 (horizon axis); "
                "natural malefics placed in houses 4 and 10 (meridian axis). "
                "All conditions evaluated from the ascendant."
            ),
            "operator": "and",
            "house_requirements": [
                {"houses": [1, 7],   "planet_type": "benefic", "constraint": "present"},
                {"houses": [4, 10],  "planet_type": "malefic", "constraint": "present"},
            ],
        },
    },
    {
        "rule_id": "bphs-ch35-012",
        "yoga_name": "Yava Yoga",
        "new_yoga_check": {
            "type": "multi_house_requirements",
            "checkable": True,
            "description": (
                "Natural benefics placed in houses 4 and 10 (meridian axis); "
                "natural malefics placed in houses 1 and 7 (horizon axis). "
                "Mirror formation of Vajra Yoga."
            ),
            "operator": "and",
            "house_requirements": [
                {"houses": [4, 10],  "planet_type": "benefic", "constraint": "present"},
                {"houses": [1, 7],   "planet_type": "malefic", "constraint": "present"},
            ],
        },
    },
    # ── Ch 36 ────────────────────────────────────────────────────────────────
    {
        "rule_id": "bphs-ch36-006",
        "yoga_name": "Parvata Yoga",
        "new_yoga_check": {
            "type": "multi_house_requirements",
            "checkable": True,
            "description": (
                "Natural benefics must occupy the angular houses (1, 4, 7, 10); "
                "houses 7 and 8 must be free from natural malefics "
                "(vacant or benefic-only). Primary classical form per Parasara."
            ),
            "operator": "and",
            "house_requirements": [
                {"houses": [1, 4, 7, 10], "planet_type": "benefic", "constraint": "present"},
                {"houses": [7, 8],         "planet_type": "malefic", "constraint": "absent"},
            ],
        },
    },
]

# Matsya only needs a type field rename — house_requirements already exist
MATSYA_TYPE_RENAME = "bphs-ch36-014"


def parse_args():
    p = argparse.ArgumentParser(description="Patch yoga_check type reclassification")
    p.add_argument("--mongo-url",  required=True, help="MongoDB connection string")
    p.add_argument("--db-name",    default="horoscope_db", help="Database name")
    p.add_argument("--dry-run",    action="store_true", help="Show what would change without writing")
    return p.parse_args()


def main():
    args = parse_args()

    client = MongoClient(args.mongo_url)
    coll = client[args.db_name]["interpretation_rules"]

    total_patched = 0

    for patch in PATCHES:
        rule_id   = patch["rule_id"]
        yoga_name = patch["yoga_name"]
        new_yc    = patch["new_yoga_check"]

        doc = coll.find_one({"rule_id": rule_id}, {"condition.yoga_check": 1})
        if not doc:
            print(f"⚠️  {rule_id} ({yoga_name}) — NOT FOUND in {args.db_name}")
            continue

        old_type = doc["condition"]["yoga_check"].get("type", "?")
        old_chk  = doc["condition"]["yoga_check"].get("checkable", "?")

        print(f"\n{rule_id} ({yoga_name})")
        print(f"  Before: type={old_type}  checkable={old_chk}")
        print(f"  After:  type={new_yc['type']}  checkable={new_yc['checkable']}")

        if not args.dry_run:
            result = coll.update_one(
                {"rule_id": rule_id},
                {
                    "$set": {
                        "condition.yoga_check": new_yc,
                        "patch_notes": PATCH_NOTES,
                        "patched_at": datetime.now(timezone.utc).isoformat(),
                    }
                },
            )
            if result.modified_count:
                total_patched += 1
                print(f"  ✅ Patched")
            else:
                print(f"  ⚠️  Matched but not modified")

    # Matsya — rename type only
    print(f"\n{MATSYA_TYPE_RENAME} (Matsya Yoga)")
    doc = coll.find_one({"rule_id": MATSYA_TYPE_RENAME}, {"condition.yoga_check": 1})
    if not doc:
        print("  ⚠️  NOT FOUND")
    else:
        old_type = doc["condition"]["yoga_check"].get("type", "?")
        old_chk  = doc["condition"]["yoga_check"].get("checkable", "?")
        hrs_count = len(doc["condition"]["yoga_check"].get("house_requirements", []))
        print(f"  Before: type={old_type}  checkable={old_chk}  house_requirements={hrs_count}")
        print(f"  After:  type=multi_house_requirements  checkable={old_chk}  (type rename only)")

        if not args.dry_run:
            result = coll.update_one(
                {"rule_id": MATSYA_TYPE_RENAME},
                {
                    "$set": {
                        "condition.yoga_check.type": "multi_house_requirements",
                        "patch_notes": PATCH_NOTES,
                        "patched_at": datetime.now(timezone.utc).isoformat(),
                    }
                },
            )
            if result.modified_count:
                total_patched += 1
                print(f"  ✅ Patched")
            else:
                print(f"  ⚠️  Matched but not modified")

    if args.dry_run:
        print(f"\n── DRY RUN — no changes written ──")
    else:
        print(f"\n── Done: {total_patched} / 4 rules patched ──")

    # Final verification read-back
    print("\n── Verification ──")
    for rid in ["bphs-ch35-011", "bphs-ch35-012", "bphs-ch36-006", "bphs-ch36-014"]:
        d = coll.find_one({"rule_id": rid},
                          {"condition.yoga_check.type": 1,
                           "condition.yoga_check.checkable": 1,
                           "condition.yoga_check.house_requirements": 1,
                           "condition.yoga_name": 1})
        if d:
            yc  = d["condition"]["yoga_check"]
            hrs = len(yc.get("house_requirements", []))
            print(f"  {rid}: type={yc.get('type','?')}  "
                  f"checkable={yc.get('checkable','?')}  "
                  f"house_requirements={hrs}")
        else:
            print(f"  {rid}: NOT FOUND")

    client.close()


if __name__ == "__main__":
    main()
