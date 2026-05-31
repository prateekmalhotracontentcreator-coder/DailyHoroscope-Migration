#!/usr/bin/env python3
"""
patch_phase2_source_batch_id.py
------------------------------------------------------------------------
One-shot patch: add source.batch_id to all Phase 2 rules that are
missing it.

Root cause: ingest_bphs_vol1_phase2.py set `ingest_batch_id` (top-level)
but did NOT write `source.batch_id`. validate_rules.py queries
`source.batch_id` (line 51), so it found 0 rules to validate.

Fix: for every rule in the Phase 2 batch, $set source.batch_id to the
same value already stored in ingest_batch_id.

Also fixes ingest_bphs_vol1_phase2.py so future runs write source.batch_id
correctly (edit required separately in inject_fields()).

Run:
  # Dry run -- shows count
  python3 backend/scripts/patch_phase2_source_batch_id.py \
    --mongo-url "$MONGO_URL" --db-name horoscope_db

  # Apply
  python3 backend/scripts/patch_phase2_source_batch_id.py \
    --mongo-url "$MONGO_URL" --db-name horoscope_db --apply
"""

import argparse
import os
import sys

BATCH_ID = "bphs-vol1-phase2-v1-20260601"


def main():
    parser = argparse.ArgumentParser(
        description="Patch source.batch_id on Phase 2 BPHS rules"
    )
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument(
        "--apply", action="store_true",
        help="Write changes (default is dry run)"
    )
    args = parser.parse_args()

    if not args.mongo_url:
        print("❌ --mongo-url required (or set $MONGO_URL)")
        sys.exit(1)

    try:
        from pymongo import MongoClient
        client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10000)
        col = client[args.db_name]["interpretation_rules"]
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        sys.exit(1)

    # Find all Phase 2 rules that do NOT have source.batch_id set correctly
    query = {
        "ingest_batch_id": BATCH_ID,
        "source.batch_id": {"$ne": BATCH_ID},
    }

    count = col.count_documents(query)
    print(f"\nRules matching (missing source.batch_id): {count}")

    if count == 0:
        print("✅ Nothing to patch -- source.batch_id already set on all rules.")
        client.close()
        return

    if not args.apply:
        print(f"\n[DRY RUN] Would patch {count} rules → set source.batch_id = \"{BATCH_ID}\"")
        print("Re-run with --apply to write changes.")
        client.close()
        return

    # Apply patch
    result = col.update_many(
        query,
        {"$set": {"source.batch_id": BATCH_ID}}
    )
    print(f"\n✅ Patched {result.modified_count} rules → source.batch_id = \"{BATCH_ID}\"")

    # Verify
    still_missing = col.count_documents(query)
    if still_missing == 0:
        print("✅ Verification passed -- 0 rules still missing source.batch_id")
    else:
        print(f"⚠  {still_missing} rules still missing source.batch_id -- investigate")

    client.close()
    print(f"\nNEXT: Run validate_rules.py --batch-id {BATCH_ID}")


if __name__ == "__main__":
    main()
