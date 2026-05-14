#!/usr/bin/env python3
"""
Diagnostic + reset for Lal Kitab Ch 19 rules.

1. Prints current approval_status breakdown for the batch.
2. If dedup is still needed (156 docs), removes the second 78.
3. Resets all surviving docs → pending_review so validator can process them.
"""

import os
import sys
from collections import Counter
from pymongo import MongoClient

BATCH_ID        = "lalkitab-ch19-v1-20260426"
DB_NAME         = "horoscope_db"
COLL_NAME       = "interpretation_rules"
EXPECTED_UNIQUE = 78


def main():
    mongo_url = os.environ.get("MONGO_URL", "").strip()
    if not mongo_url:
        mongo_url = input("Paste MongoDB Atlas URL: ").strip()
    if not mongo_url:
        sys.exit("ERROR: no MONGO_URL provided")

    client = MongoClient(mongo_url)
    coll   = client[DB_NAME][COLL_NAME]

    # ── 1. Diagnostic ────────────────────────────────────────────────────────
    docs = list(
        coll.find(
            {"source.batch_id": BATCH_ID},
            {"_id": 1, "rule_id": 1, "approval_status": 1}
        ).sort("_id", 1)
    )
    total = len(docs)
    status_counts = Counter(d.get("approval_status", "???") for d in docs)

    print(f"\nBatch: {BATCH_ID}")
    print(f"Total docs found: {total}")
    print("Status breakdown:")
    for status, count in status_counts.most_common():
        print(f"  {status:<30} {count}")

    # ── 2. Dedup if still doubled ─────────────────────────────────────────────
    if total > EXPECTED_UNIQUE:
        extra = total - EXPECTED_UNIQUE
        ids_to_delete = [d["_id"] for d in docs[EXPECTED_UNIQUE:]]
        print(f"\n→ Deleting {extra} duplicate(s)...")
        result = coll.delete_many({"_id": {"$in": ids_to_delete}})
        print(f"  Deleted {result.deleted_count} documents.")
    elif total == 0:
        print("\nERROR: No docs found for this batch_id. Check DB_NAME or BATCH_ID.")
        return
    else:
        print(f"\n→ Count already correct ({total} docs). No deletion needed.")

    # ── 3. Reset all surviving docs → pending_review ─────────────────────────
    reset = coll.update_many(
        {"source.batch_id": BATCH_ID},
        {"$set": {"approval_status": "pending_review"}, "$unset": {"validation": ""}},
    )
    print(f"→ Reset {reset.modified_count} docs → pending_review (validation cleared).")

    # ── 4. Verify ─────────────────────────────────────────────────────────────
    remaining = coll.count_documents({"source.batch_id": BATCH_ID})
    pending   = coll.count_documents({"source.batch_id": BATCH_ID, "approval_status": "pending_review"})
    print(f"\n✅ Final state: {remaining} total, {pending} pending_review")
    if remaining == EXPECTED_UNIQUE and pending == EXPECTED_UNIQUE:
        print("   Ready to validate.")
    else:
        print("   ⚠️  Mismatch -- investigate before running validator.")


if __name__ == "__main__":
    main()
