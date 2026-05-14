#!/usr/bin/env python3
"""
deprecate_pre_split_merged.py

One-time post-sweep cleanup.
Marks all pre_split_merged original rules as 'deprecated' now that
split-upgrade is complete across all chapters (Ch 47/48/52-60).

These rules are superseded by their individually-split successors
(source_note='split_upgrade'). Deprecating removes them from the
co-founder review queue without deleting them from the DB.

Usage:
    python3 scripts/deprecate_pre_split_merged.py --mongo-url "$MONGO_URL" [--dry-run]
"""

import argparse
import pymongo


def main():
    parser = argparse.ArgumentParser(description="Deprecate all pre_split_merged rules.")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--dry-run",   action="store_true")
    args = parser.parse_args()

    mode = "DRY RUN" if args.dry_run else "LIVE"
    print(f"\ndeprecate_pre_split_merged.py  |  DB: {args.db_name}  |  Mode: {mode}")

    client = pymongo.MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]

    # ── Count what will be affected ────────────────────────────────────────────
    total = col.count_documents({"metadata.source_note": "pre_split_merged"})
    already_deprecated = col.count_documents({
        "metadata.source_note": "pre_split_merged",
        "approval_status":      "deprecated",
    })
    to_deprecate = total - already_deprecated

    print(f"\npre_split_merged rules in DB : {total}")
    print(f"Already deprecated           : {already_deprecated}")
    print(f"Will be deprecated           : {to_deprecate}")

    # Breakdown by batch
    print("\nBreakdown by batch:")
    pipeline = [
        {"$match": {
            "metadata.source_note": "pre_split_merged",
            "approval_status":      {"$ne": "deprecated"},
        }},
        {"$group": {"_id": "$source.batch_id", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]
    for doc in col.aggregate(pipeline):
        print(f"  {doc['_id']:45s}  {doc['count']} rules")

    if to_deprecate == 0:
        print("\n✅ Nothing to do -- all pre_split_merged rules already deprecated.")
        client.close()
        return

    # ── Apply deprecation ──────────────────────────────────────────────────────
    if not args.dry_run:
        result = col.update_many(
            {
                "metadata.source_note": "pre_split_merged",
                "approval_status":      {"$ne": "deprecated"},
            },
            {"$set": {"approval_status": "deprecated"}},
        )
        print(f"\n✅ Deprecated {result.modified_count} rules.")

        # Verify
        remaining = col.count_documents({
            "metadata.source_note": "pre_split_merged",
            "approval_status":      {"$ne": "deprecated"},
        })
        print(f"Verification -- remaining non-deprecated pre_split_merged: {remaining} (should be 0)")
        if remaining == 0:
            print("✅ Clean.")
        else:
            print(f"⚠️  {remaining} rules still not deprecated -- investigate.")
    else:
        print(f"\n[DRY RUN] Would deprecate {to_deprecate} rules.")

    client.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
