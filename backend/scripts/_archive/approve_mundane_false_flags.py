#!/usr/bin/env python3
"""
approve_mundane_false_flags.py

Approves mundane PHR rules that were confirmed as false flags by the
co-founder audit (May 2026). These rules need no content fixes —
the validator applied the wrong standard.

Usage:
  # Dry run:
  python3 backend/scripts/approve_mundane_false_flags.py --mongo-url "$MONGO_URL"

  # Apply:
  python3 backend/scripts/approve_mundane_false_flags.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

FALSE_FLAGS = {
    "mundane-mehta-ch13-eclipse-national-validation": (
        "False flag (content_validity_dispute) — Mehta/Rao explicitly use India's "
        "Independence chart (15 Aug 1947, Taurus Lagna) as the reference chart for "
        "eclipse impact analysis. Validator applied the wrong classical frame "
        "(generic eclipse rules) instead of the source's documented methodology."
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--apply",     action="store_true")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]
    now    = datetime.now(timezone.utc).isoformat()

    print(f"\n{'═'*60}")
    print(f"Mundane false-flag approvals")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*60}\n")

    for rid, note in FALSE_FLAGS.items():
        r = col.find_one(
            {"rule_id": rid, "science_id": "mundane_jyotish"},
            {"_id": 0, "rule_id": 1, "approval_status": 1, "title": 1},
        )
        if not r:
            print(f"  ⚠️  NOT FOUND : {rid}")
            continue

        print(f"  rule_id : {rid}")
        print(f"  title   : {r.get('title', 'n/a')}")
        print(f"  status  : {r.get('approval_status', '?')}")
        print(f"  note    : {note[:120]}…")

        if args.apply:
            result = col.update_one(
                {"rule_id": rid},
                {"$set": {
                    "approval_status":          "approved",
                    "validation.verdict":       "approved",
                    "validation.approved_by":   "co_founder_false_flag_resolution_may2026",
                    "validation.approved_at":   now,
                    "validation.approved_note": note,
                }},
            )
            if result.modified_count:
                print(f"  ✅ APPROVED\n")
            else:
                print(f"  ⚠️  No change written\n")
        else:
            print(f"  🔍 WOULD APPROVE\n")

    if args.apply:
        approved = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "approved"}
        )
        phr = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "pending_human_review"}
        )
        flagged = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "flagged"}
        )
        print(f"{'─'*60}")
        print(f"Library status:")
        print(f"  approved             : {approved}")
        print(f"  pending_human_review : {phr}")
        print(f"  flagged              : {flagged}")

    client.close()


if __name__ == "__main__":
    main()
