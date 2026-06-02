#!/usr/bin/env python3
"""
validate_ingest_batch.py
--------------------------------------------------------------------
Post-ingest structural validation for a specific batch_id.
Checks that all rules were inserted with the correct fields.

Usage:
    python3 backend/scripts/validate_ingest_batch.py \
      --batch-id "300-combinations-v1-20260531" \
      --mongo-url "$MONGO_URL" --db-name horoscope_db

Note: This script checks structural correctness only (rule_id, approval_status,
source_book, source.batch_id). For AI quality validation, use validate_rules.py.
"""

from __future__ import annotations

import argparse
import os
import sys
from pymongo import MongoClient


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Post-ingest structural batch validator.")
    parser.add_argument("--batch-id", required=True, help="Batch ID to validate")
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    parser.add_argument("--db-name", default="horoscope_db")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.mongo_url:
        print("ERROR: --mongo-url not provided and MONGO_URL env var not set.", file=sys.stderr)
        sys.exit(1)

    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10000)
    db = client[args.db_name]

    batch_id = args.batch_id
    print(f"\nValidating batch: {batch_id}")
    print(f"Database:         {args.db_name}")

    # Check import_batches record
    batch_record = db["import_batches"].find_one({"batch_id": batch_id})
    if not batch_record:
        print(f"\n❌ ERROR: batch '{batch_id}' not found in import_batches collection")
        sys.exit(1)

    print(f"\nimport_batches record:")
    for k, v in batch_record.items():
        if k != "_id":
            print(f"  {k}: {v}")

    # Fetch all rules for this batch (by ingest_batch_id)
    rules = list(db["interpretation_rules"].find(
        {"ingest_batch_id": batch_id}, {"_id": 0}
    ))
    print(f"\nRules found in DB (ingest_batch_id={batch_id}): {len(rules)}")

    if not rules:
        print("⚠  No rules found -- batch may not have inserted via ingest_from_json_folder.py")
        # Check by source.batch_id (validate_rules.py uses this)
        rules_by_source = list(db["interpretation_rules"].find(
            {"source.batch_id": batch_id}, {"_id": 0}
        ))
        print(f"Rules found (source.batch_id={batch_id}): {len(rules_by_source)}")
        if rules_by_source:
            rules = rules_by_source
            print("Using source.batch_id match for validation.")

    if not rules:
        print("❌ No rules found for this batch. Ingest may have failed.")
        sys.exit(1)

    # Structural checks
    missing_rule_id  = [r for r in rules if not r.get("rule_id")]
    wrong_status     = [r for r in rules if r.get("approval_status") not in
                        ("pending_review", "auto_approved", "pending_human_review", "flagged", "rejected", "approved")]
    missing_book     = [r for r in rules if not r.get("source_book")]
    missing_interp   = [r for r in rules if not (
        (r.get("interpretation") or {}).get("detailed") or
        (r.get("interpretation") or {}).get("summary") or
        r.get("full_text")
    )]
    source_batch_ok  = [r for r in rules if (r.get("source") or {}).get("batch_id") == batch_id]
    source_batch_missing = len(rules) - len(source_batch_ok)

    # Approval status breakdown
    status_counts: dict[str, int] = {}
    for r in rules:
        s = r.get("approval_status", "UNKNOWN")
        status_counts[s] = status_counts.get(s, 0) + 1

    print(f"\n{'─'*60}")
    print(f"  Total rules in DB:        {len(rules)}")
    print(f"  Reported inserted:        {batch_record.get('rules_inserted', '?')}")
    print(f"  Duplicates skipped:       {batch_record.get('duplicates_skipped', '?')}")
    print(f"\n  Approval status breakdown:")
    for status, count in sorted(status_counts.items()):
        print(f"    {status}: {count}")

    print(f"\n  Structural checks:")
    print(f"    Missing rule_id:          {len(missing_rule_id)}")
    print(f"    Invalid approval_status:  {len(wrong_status)}")
    print(f"    Missing source_book:      {len(missing_book)}")
    print(f"    Missing interpretation:   {len(missing_interp)}")
    print(f"    source.batch_id missing:  {source_batch_missing}")

    all_clean = (
        len(missing_rule_id) == 0
        and len(wrong_status) == 0
        and len(missing_book) == 0
        and source_batch_missing == 0
    )

    print(f"\n{'─'*60}")
    if all_clean:
        print(f"✅ STRUCTURAL CHECK: CLEAN")
        print(f"   Next: python3 backend/scripts/validate_rules.py --batch-id {batch_id} "
              f"--mongo-url \"$MONGO_URL\" --db-name {args.db_name}")
    else:
        print(f"❌ STRUCTURAL CHECK: ISSUES FOUND")
        if missing_rule_id:
            print(f"   → {len(missing_rule_id)} rules missing rule_id")
        if wrong_status:
            print(f"   → {len(wrong_status)} rules with invalid approval_status: "
                  f"{[r.get('rule_id') for r in wrong_status[:3]]}")
        if missing_book:
            print(f"   → {len(missing_book)} rules missing source_book")
        if source_batch_missing:
            print(f"   → {source_batch_missing} rules missing source.batch_id")
        sys.exit(1)

    client.close()


if __name__ == "__main__":
    main()
