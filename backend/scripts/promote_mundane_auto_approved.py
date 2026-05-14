#!/usr/bin/env python3
"""
promote_mundane_auto_approved.py

Promotes all mundane_jyotish rules at auto_approved → approved.

These are the Part A rules from the co-founder sign-off review -- rules that
passed all 3 validation stages (structural, Claude quality, spot-check) with
no flags or PHR escalations. Confirmed clean by co-founder review May 2026.

Usage:
  # Dry run:
  python3 backend/scripts/promote_mundane_auto_approved.py --mongo-url "$MONGO_URL"

  # Apply:
  python3 backend/scripts/promote_mundane_auto_approved.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--apply",     action="store_true")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]
    now    = datetime.now(timezone.utc).isoformat()

    query = {"science_id": "mundane_jyotish", "approval_status": "auto_approved"}
    count = col.count_documents(query)

    print(f"\n{'═'*60}")
    print(f"Mundane auto_approved → approved promotion")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍  (use --apply to write)'}")
    print(f"{'═'*60}")
    print(f"\nFound: {count} auto_approved rules\n")

    if args.apply:
        result = col.update_many(
            query,
            {"$set": {
                "approval_status":          "approved",
                "validation.verdict":       "approved",
                "validation.approved_by":   "co_founder_signoff_may2026",
                "validation.approved_at":   now,
                "validation.approved_note": (
                    "Passed all 3 validation stages with no flags. "
                    "Confirmed clean via co-founder sign-off review May 2026 "
                    "(promote_mundane_auto_approved.py)."
                ),
            }},
        )
        print(f"✅ Promoted: {result.modified_count} rules → approved")
    else:
        rules = list(col.find(query, {"_id": 0, "rule_id": 1, "batch_id": 1}).sort(
            [("batch_id", 1), ("rule_id", 1)]
        ))
        current_batch = None
        for r in rules:
            bid = r.get("batch_id", "unknown")
            if bid != current_batch:
                current_batch = bid
                print(f"  [{bid}]")
            print(f"    🔍 {r['rule_id']}")
        print(f"\n  Would promote: {count} rules")
        print(f"  Re-run with --apply to write.")

    # Final status check
    if args.apply:
        remaining = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "auto_approved"}
        )
        approved  = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "approved"}
        )
        phr       = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "pending_human_review"}
        )
        flagged   = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "flagged"}
        )
        print(f"\n{'─'*60}")
        print(f"Mundane library status after promotion:")
        print(f"  approved              : {approved}")
        print(f"  pending_human_review  : {phr}  (72 rules held for fixes)")
        print(f"  auto_approved         : {remaining}  (should be 0)")
        print(f"  flagged               : {flagged}  (Aries 1° -- rewrite pending)")

    client.close()


if __name__ == "__main__":
    main()
