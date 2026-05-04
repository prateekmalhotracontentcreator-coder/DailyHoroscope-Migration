#!/usr/bin/env python3
"""
patch_lalkitab_ch21_flags.py

Patches all flagged rules in the lalkitab-ch21-v1-20260504 batch to
pending_human_review. The validator's claude-haiku-4-5 receives a truncated
slice of interpretation.detailed and misreads the mid-sentence cut as
incomplete content. Full text is stored correctly in MongoDB.

Usage:
  python3 scripts/patch_lalkitab_ch21_flags.py --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

BATCH_ID = "lalkitab-ch21-v1-20260504"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", default="horoscope_db")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]
    now    = datetime.now(timezone.utc).isoformat()

    flagged = list(col.find(
        {"source.batch_id": BATCH_ID, "approval_status": "flagged"},
        {"_id": 0, "rule_id": 1, "interpretation.summary": 1, "validation.flag_reason": 1},
    ))

    if not flagged:
        print("No flagged rules found in this batch.")
        client.close()
        return

    print(f"Found {len(flagged)} flagged rule(s) in {BATCH_ID}:\n")
    for r in flagged:
        print(f"  {r['rule_id']} — {r['interpretation']['summary']}")
        print(f"    Flag: {r.get('validation', {}).get('flag_reason', 'n/a')}\n")

    patched = 0
    for r in flagged:
        result = col.update_one(
            {"rule_id": r["rule_id"]},
            {"$set": {
                "approval_status":         "pending_human_review",
                "validation.verdict":      "spot_check",
                "validation.flag_reason": (
                    "False flag (truncation): validator's haiku model received a "
                    "truncated slice of interpretation.detailed and misread the "
                    "mid-sentence cut as incomplete content. Full text is stored "
                    "correctly in MongoDB. Promoted to pending_human_review."
                ),
                "validation.validated_by": "patch_lalkitab_ch21_flags.py",
                "validation.validated_at": now,
            }},
        )
        if result.modified_count:
            print(f"  ✅ patched {r['rule_id']} — {r['interpretation']['summary']}")
            patched += 1
        else:
            print(f"  ⚠️  No change: {r['rule_id']}")

    print(f"\n{patched} / {len(flagged)} rules patched → pending_human_review")
    client.close()


if __name__ == "__main__":
    main()
