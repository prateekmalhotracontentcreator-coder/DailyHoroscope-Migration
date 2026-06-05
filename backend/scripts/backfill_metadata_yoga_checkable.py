#!/usr/bin/env python3
"""
backfill_metadata_yoga_checkable.py
--------------------------------------------------------------------
BPHS Vol 1 -- Sync metadata.yoga_checkable from condition.yoga_check

Background
----------
condition.yoga_check (rich structured object) is the authoritative yoga
checkability source -- set by the yoga checker script during original ingest.
metadata.yoga_checkable (boolean) is a convenience flag for fast queries.
These two are out of sync on a subset of Ch35-41 rules.

This script reads condition.yoga_check.checkable for every rule in Ch35-41
and writes the matching boolean to metadata.yoga_checkable, making both
fields consistent.

It also ensures interpretation.tags contains "yoga_checkable" (or not)
to match the checkable boolean.

Run sequence:
  Step 0: python3 backend/scripts/backfill_metadata_yoga_checkable.py --mongo-url "..." --dry-run
  Step 1: python3 backend/scripts/backfill_metadata_yoga_checkable.py --mongo-url "..." --apply
  Step 2: Re-run inspect_bphs_phase1_issues.py to confirm sync
  Step 3: Commit this script to git
"""

import argparse
import os
from datetime import datetime, timezone
from pymongo import MongoClient

PATCH_DATE = datetime.now(timezone.utc).isoformat()
CHAPTERS = list(range(35, 42))  # Ch35 through Ch41 (Ch42 has 0 rules)


def get_chapter_rules(col, chapter: int) -> list:
    return list(col.find(
        {"$or": [
            {"source_chapter": {"$regex": f"ch.?{chapter}\\b", "$options": "i"}},
            {"source.chapter": chapter},
        ]},
        {"_id": 0, "rule_id": 1, "condition": 1,
         "metadata": 1, "interpretation": 1}
    ))


def main():
    parser = argparse.ArgumentParser(
        description="Sync metadata.yoga_checkable from condition.yoga_check for Ch35-41"
    )
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"), required=True)
    parser.add_argument("--db-name", default="horoscope_db")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true",
                      help="Preview changes -- no writes")
    mode.add_argument("--apply", action="store_true",
                      help="Write metadata.yoga_checkable to MongoDB")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10000)
    col = client[args.db_name]["interpretation_rules"]

    print("\n" + "=" * 70)
    if args.dry_run:
        print("METADATA YOGA_CHECKABLE BACKFILL -- DRY RUN (no writes)")
    else:
        print("METADATA YOGA_CHECKABLE BACKFILL -- APPLYING")
    print("=" * 70)

    total_rules = 0
    total_already_correct = 0
    total_patched = 0
    total_no_yoga_check = 0
    total_errors = 0

    for chapter in CHAPTERS:
        rules = get_chapter_rules(col, chapter)
        if not rules:
            continue

        ch_correct = 0
        ch_patched = 0
        ch_no_yoga_check = 0

        print(f"\n── Chapter {chapter} ({len(rules)} rules) ──")

        for rule in rules:
            rid = rule.get("rule_id", "?")
            condition = rule.get("condition") or {}
            yoga_check = condition.get("yoga_check")
            metadata = rule.get("metadata") or {}
            tags = (rule.get("interpretation") or {}).get("tags") or []

            # No yoga_check object at all -- skip (shouldn't happen for Ch35-41)
            if yoga_check is None:
                ch_no_yoga_check += 1
                total_no_yoga_check += 1
                if args.dry_run:
                    print(f"  ⚠  {rid} -- condition.yoga_check is None (unexpected)")
                continue

            authoritative_checkable = bool(yoga_check.get("checkable", False))
            current_meta = metadata.get("yoga_checkable")

            # Check tag consistency
            has_tag = "yoga_checkable" in tags
            tag_needs_add = authoritative_checkable and not has_tag
            tag_needs_remove = not authoritative_checkable and has_tag

            # Already in sync -- skip
            if current_meta == authoritative_checkable and not tag_needs_add and not tag_needs_remove:
                ch_correct += 1
                total_already_correct += 1
                continue

            # Build update
            set_doc = {
                "metadata.yoga_checkable": authoritative_checkable,
                "metadata.yoga_checkable_synced_at": PATCH_DATE,
            }

            if args.dry_run:
                print(
                    f"  [DRY] {rid}: metadata.yoga_checkable "
                    f"{current_meta} → {authoritative_checkable}"
                    + (f" | add tag 'yoga_checkable'" if tag_needs_add else "")
                    + (f" | remove tag 'yoga_checkable'" if tag_needs_remove else "")
                )
                ch_patched += 1
                total_patched += 1
            else:
                update_ops = {"$set": set_doc}
                if tag_needs_add:
                    update_ops["$addToSet"] = {"interpretation.tags": "yoga_checkable"}
                if tag_needs_remove:
                    update_ops["$pull"] = {"interpretation.tags": "yoga_checkable"}

                try:
                    result = col.update_one({"rule_id": rid}, update_ops)
                    if result.modified_count == 1:
                        ch_patched += 1
                        total_patched += 1
                    else:
                        print(f"  ⚠  {rid} -- matched {result.matched_count}, "
                              f"modified {result.modified_count}")
                        total_errors += 1
                except Exception as e:
                    print(f"  ❌ {rid} -- {e}")
                    total_errors += 1

        print(f"  Already in sync : {ch_correct}")
        print(f"  {'Would patch' if args.dry_run else 'Patched'} : {ch_patched}")
        if ch_no_yoga_check:
            print(f"  No yoga_check   : {ch_no_yoga_check} (unexpected -- investigate)")

        total_rules += len(rules)

    # ── Final summary ──────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total rules scanned    : {total_rules}")
    print(f"  Already in sync        : {total_already_correct}")
    print(f"  {'Would patch' if args.dry_run else 'Patched'} : {total_patched}")
    print(f"  Missing yoga_check obj : {total_no_yoga_check}")
    print(f"  Errors                 : {total_errors}")

    if args.dry_run:
        print("\n  [DRY RUN] No writes made. Re-run with --apply to execute.")
    elif total_errors == 0:
        print("\n  ✅ Sync complete. metadata.yoga_checkable now matches condition.yoga_check.checkable")
        print("     on all Ch35-41 rules. Re-run inspect to verify.")

    client.close()


if __name__ == "__main__":
    main()
