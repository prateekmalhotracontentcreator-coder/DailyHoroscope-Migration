#!/usr/bin/env python3
"""
migrate_yoga_check.py
--------------------------------------------------------------------
BPHS Vol 1 -- yoga_check field migration for Ch35-41

Background
----------
197 rules across Ch35-41 have validation.yoga_check = None (not set).
These chapters contain yoga rules. The checkability determination was done
during the original decode: the source JSON files carry a top-level
`checkable` boolean on each rule.

This script:
  1. Loads source JSON files for Ch35-41 to build rule_id → checkable map
  2. For each MongoDB rule in Ch35-41, sets validation.yoga_check based on
     source JSON checkable value:
       checkable=True  → validation.yoga_check = "checkable"
       checkable=False → validation.yoga_check = "not_checkable"
  3. For Ch40 (no source JSON -- 15 rules ingested without corresponding file):
     Uses condition.type heuristic (yoga_combination = checkable, else not_checkable)
     AND flags these with validation.yoga_check_method = "heuristic_no_source_json"
     for future TT review.

Run sequence (mandatory):
  Step 0: python3 backend/scripts/migrate_yoga_check.py --mongo-url "..." --dry-run
  Step 1: Review output -- confirm counts match inspection results
  Step 2: python3 backend/scripts/migrate_yoga_check.py --mongo-url "..." --apply
  Step 3: Re-run inspect_bphs_phase1_issues.py -- yoga_check populated counts should be non-zero
  Step 4: Commit this script to git
"""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from pymongo import MongoClient

DECODE_FOLDER = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode"
)

PATCH_DATE = datetime.now(timezone.utc).isoformat()

# Source JSON mapping: chapter number → list of JSON filenames in DECODE_FOLDER
CHAPTER_SOURCE_FILES = {
    35: [
        "BPHS_Ch35_Nabhasa_Yogas_Rules_Part1.json",
        "BPHS_Ch35_Nabhasa_Yogas_Rules_Part2.json",
    ],
    36: [
        "BPHS_Ch36_Many_Other_Yogas_Rules_Part1.json",
        "BPHS_Ch36_Many_Other_Yogas_Rules_Part2.json",
    ],
    37: [
        "BPHS_Ch37_Lunar_Yogas_Rules_Part1.json",
    ],
    38: [
        "BPHS_Ch38_Solar_Yogas_Rules_Part1.json",
    ],
    39: [
        "BPHS_Ch39_Raja_Yogas_Rules_Part1.json",
        "BPHS_Ch39_Raja_Yogas_Rules_Part2.json",
    ],
    # Ch40 has no source JSON -- handled via heuristic
    40: [],
    41: [
        "BPHS_Ch41_Yogas_for_Wealth_Rules_Part1.json",
        "BPHS_Ch41_Yogas_for_Wealth_Rules_Part2.json",
    ],
}

# Condition types that indicate a yoga is algorithmically checkable
CHECKABLE_CONDITION_TYPES = {
    "yoga_combination",
    "planetary_conjunction",
    "house_lord_in_house",
    "aspect_rule",
    "sign_placement",
}


def load_source_checkability(chapter: int) -> dict:
    """
    Returns rule_id → checkable (bool) map from source JSON files.
    Returns {} for chapters with no source files.
    """
    checkability = {}
    files = CHAPTER_SOURCE_FILES.get(chapter, [])
    for fname in files:
        fpath = DECODE_FOLDER / fname
        if not fpath.exists():
            print(f"    ⚠  Source file NOT FOUND: {fpath}")
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        rules = data if isinstance(data, list) else data.get("rules", [])
        for rule in rules:
            rid = rule.get("rule_id")
            checkable = rule.get("checkable", False)
            if rid:
                checkability[rid] = bool(checkable)
    return checkability


def heuristic_checkable(rule: dict) -> bool:
    """
    Heuristic for Ch40 (no source JSON): derive from condition.type.
    """
    cond = rule.get("condition") or {}
    return cond.get("type") in CHECKABLE_CONDITION_TYPES


def get_chapter_rules(col, chapter: int) -> list:
    """
    Query MongoDB for all rules in a given chapter.
    Handles both source_chapter regex and source.chapter int patterns.
    """
    rules = list(col.find(
        {"$or": [
            {"source_chapter": {"$regex": f"ch.?{chapter}\\b", "$options": "i"}},
            {"source.chapter": chapter},
        ]},
        {"_id": 0, "rule_id": 1, "approval_status": 1,
         "condition": 1, "validation": 1, "source": 1, "source_chapter": 1}
    ))
    return rules


def main():
    parser = argparse.ArgumentParser(
        description="Populate validation.yoga_check for BPHS Ch35-41 yoga rules"
    )
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"), required=True,
                        help="MongoDB Atlas connection string")
    parser.add_argument("--db-name", default="horoscope_db")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true",
                      help="Show what would be patched -- no writes")
    mode.add_argument("--apply", action="store_true",
                      help="Write validation.yoga_check to MongoDB")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10000)
    col = client[args.db_name]["interpretation_rules"]

    print("\n" + "=" * 70)
    if args.dry_run:
        print("YOGA_CHECK MIGRATION -- DRY RUN (no writes)")
    else:
        print("YOGA_CHECK MIGRATION -- APPLYING")
    print("=" * 70)

    total_rules = 0
    total_checkable = 0
    total_not_checkable = 0
    total_already_set = 0
    total_patched = 0
    total_errors = 0
    ch40_heuristic_count = 0

    for chapter in range(35, 42):
        print(f"\n── Chapter {chapter} ──")

        # Load source JSON checkability
        source_map = load_source_checkability(chapter)
        use_heuristic = (chapter == 40)

        if use_heuristic:
            print(f"  ⚠  No source JSON for Ch40 -- using condition.type heuristic")
        else:
            print(f"  Source map: {len(source_map)} rule_ids loaded from JSON")

        # Get MongoDB rules
        db_rules = get_chapter_rules(col, chapter)
        print(f"  MongoDB rules found: {len(db_rules)}")

        if not db_rules:
            print("  Nothing to migrate for this chapter.")
            continue

        total_rules += len(db_rules)

        chapter_checkable = 0
        chapter_not_checkable = 0
        chapter_already_set = 0
        chapter_patched = 0
        missing_from_source = []

        for rule in db_rules:
            rid = rule.get("rule_id", "?")
            val = rule.get("validation") or {}

            # Skip if already set
            if val.get("yoga_check") is not None:
                chapter_already_set += 1
                total_already_set += 1
                continue

            # Determine checkable
            if use_heuristic:
                checkable = heuristic_checkable(rule)
                method = "heuristic"
                ch40_heuristic_count += 1
            elif rid in source_map:
                checkable = source_map[rid]
                method = "source_json"
            else:
                # Rule is in MongoDB but not in source JSON
                # Use heuristic as fallback
                checkable = heuristic_checkable(rule)
                method = "heuristic_source_missing"
                missing_from_source.append(rid)

            yoga_check_val = "checkable" if checkable else "not_checkable"
            if checkable:
                chapter_checkable += 1
                total_checkable += 1
            else:
                chapter_not_checkable += 1
                total_not_checkable += 1

            if args.dry_run:
                print(f"  [DRY] {rid} → yoga_check={yoga_check_val} (method={method})")
                chapter_patched += 1
                total_patched += 1
            else:
                update_doc = {
                    "validation.yoga_check": yoga_check_val,
                    "validation.yoga_check_method": method,
                    "validation.yoga_check_migrated_at": PATCH_DATE,
                }
                if method == "heuristic" or method == "heuristic_source_missing":
                    update_doc["validation.yoga_check_needs_review"] = True

                try:
                    result = col.update_one(
                        {"rule_id": rid},
                        {"$set": update_doc}
                    )
                    if result.modified_count == 1:
                        chapter_patched += 1
                        total_patched += 1
                    else:
                        print(f"    ⚠  {rid} -- matched {result.matched_count} docs (no modify)")
                        total_errors += 1
                except Exception as e:
                    print(f"    ❌ {rid} -- {e}")
                    total_errors += 1

        if missing_from_source:
            print(f"  ⚠  {len(missing_from_source)} rules in DB but absent from source JSON "
                  f"(heuristic used):")
            for rid in missing_from_source[:5]:
                print(f"      {rid}")
            if len(missing_from_source) > 5:
                print(f"      ... and {len(missing_from_source) - 5} more")

        print(f"  Already set (skipped) : {chapter_already_set}")
        print(f"  Checkable             : {chapter_checkable}")
        print(f"  Not checkable         : {chapter_not_checkable}")
        print(f"  {'Would patch' if args.dry_run else 'Patched'}: {chapter_patched}")

    # ── Final summary ──────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("MIGRATION SUMMARY")
    print("=" * 70)
    print(f"  Total rules scanned      : {total_rules}")
    print(f"  Already had yoga_check   : {total_already_set}")
    print(f"  Marked checkable         : {total_checkable}")
    print(f"  Marked not_checkable     : {total_not_checkable}")
    print(f"  {'Would patch' if args.dry_run else 'Patched'} total: {total_patched}")
    print(f"  Errors                   : {total_errors}")
    if ch40_heuristic_count:
        print(f"  Ch40 heuristic (no source JSON): {ch40_heuristic_count} rules -- "
              f"validation.yoga_check_needs_review=True on these")

    if args.dry_run:
        print("\n  [DRY RUN] No writes made. Re-run with --apply to execute.")
    else:
        print("\n  NEXT STEPS:")
        print("  1. Re-run inspect_bphs_phase1_issues.py -- yoga_check counts should be non-zero")
        print("  2. Review Ch40 rules (yoga_check_needs_review=True) with NLM when convenient")
        print("  3. Any rule with yoga_check_method=heuristic_source_missing also needs review")
        print("  4. Commit this script to git")

    client.close()


if __name__ == "__main__":
    main()
