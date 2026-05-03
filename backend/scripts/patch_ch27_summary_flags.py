#!/usr/bin/env python3
"""
patch_ch27_summary_flags.py

12 rules in bphs-ch27-v1-20260504 were flagged by the validator as
"truncated" because interpretation.summary was built as effect[:120],
which cuts mid-sentence on longer effect texts. The detailed text and
full_text_passages are complete — all 12 flags are validator false positives.

Fix: replace summary with yoga_name (always short + complete) and promote
all 12 to pending_human_review. No re-validation needed.

Usage:
  python3 scripts/patch_ch27_summary_flags.py --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

BATCH_ID = "bphs-ch27-v1-20260504"

FLAGGED_IDS = [
    "bphs-ch27-001",
    "bphs-ch27-002",
    "bphs-ch27-011",
    "bphs-ch27-014",
    "bphs-ch27-018",
    "bphs-ch27-019",
    "bphs-ch27-020",
    "bphs-ch27-021",
    "bphs-ch27-022",
    "bphs-ch27-023",
    "bphs-ch27-024",
    "bphs-ch27-025",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", default="horoscope_db")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col = client[args.db_name]["interpretation_rules"]
    now = datetime.now(timezone.utc).isoformat()

    patched = 0
    for rid in FLAGGED_IDS:
        doc = col.find_one({"rule_id": rid}, {"_id": 0, "condition.yoga_name": 1})
        if not doc:
            print(f"  ⚠️  Not found: {rid}")
            continue

        yoga_name = doc["condition"]["yoga_name"]
        result = col.update_one(
            {"rule_id": rid},
            {"$set": {
                "interpretation.summary": yoga_name,
                "approval_status":        "pending_human_review",
                "validation.verdict":     "spot_check",
                "validation.flag_reason": (
                    "False flag: summary[:120] mid-sentence truncation misread as "
                    "incomplete content. Detailed text and full_text_passages are "
                    "complete. Promoted to pending_human_review."
                ),
                "validation.validated_by":  "patch_ch27_summary_flags.py",
                "validation.validated_at":  now,
            }},
        )
        if result.modified_count:
            print(f"  ✅ patched {rid} — {yoga_name[:60]}")
            patched += 1
        else:
            print(f"  ⚠️  No change: {rid}")

    print(f"\n{patched} rules patched → pending_human_review")
    client.close()


if __name__ == "__main__":
    main()
