#!/usr/bin/env python3
"""
Dedup Lal Kitab Ch 19 rules — removes the second set of 78 duplicates
caused by running ingest_lalkitab_ch19_v1.py twice.

Keeps the first 78 documents (by _id insertion order),
deletes the remaining 78.
"""

import os
import sys
from pymongo import MongoClient

BATCH_ID  = "lalkitab-ch19-v1-20260426"
COLL_NAME = "interpretation_rules"
DB_NAME   = "horoscope_db"
EXPECTED_TOTAL  = 156
EXPECTED_UNIQUE =  78

def main():
    mongo_url = os.environ.get("MONGO_URL", "").strip()
    if not mongo_url:
        mongo_url = input("Paste MongoDB Atlas URL: ").strip()
    if not mongo_url:
        sys.exit("ERROR: no MONGO_URL provided")

    client = MongoClient(mongo_url)
    coll   = client[DB_NAME][COLL_NAME]

    # Count current docs for this batch
    total = coll.count_documents({"source.batch_id": BATCH_ID})
    print(f"Found {total} docs with batch_id={BATCH_ID}")

    if total == EXPECTED_UNIQUE:
        print("Already clean — nothing to delete.")
        return

    if total != EXPECTED_TOTAL:
        print(f"WARNING: expected {EXPECTED_TOTAL} or {EXPECTED_UNIQUE}, got {total}.")
        print("Proceeding to delete everything past position 78.")

    # Fetch all by insertion order (_id is ObjectId → monotonically increasing)
    docs = list(
        coll.find(
            {"source.batch_id": BATCH_ID},
            {"_id": 1, "rule_id": 1}
        ).sort("_id", 1)
    )
    print(f"Fetched {len(docs)} docs sorted by _id.")

    keep = docs[:EXPECTED_UNIQUE]
    delete = docs[EXPECTED_UNIQUE:]

    print(f"Keeping  : {len(keep)} docs  (first {EXPECTED_UNIQUE})")
    print(f"Deleting : {len(delete)} docs  (duplicates)")

    if not delete:
        print("Nothing to delete.")
        return

    ids_to_delete = [d["_id"] for d in delete]
    print(f"\nSample rule_ids being DELETED: {[d['rule_id'] for d in delete[:5]]}")
    print(f"Sample rule_ids being KEPT   : {[d['rule_id'] for d in keep[:5]]}")

    confirm = input("\nProceed with deletion? [y/N]: ").strip().lower()
    if confirm != "y":
        print("Aborted.")
        return

    result = coll.delete_many({"_id": {"$in": ids_to_delete}})
    print(f"\nDeleted {result.deleted_count} documents.")

    remaining = coll.count_documents({"source.batch_id": BATCH_ID})
    print(f"Remaining docs for batch: {remaining}")
    if remaining != EXPECTED_UNIQUE:
        print(f"⚠️  Unexpected count after dedup: {remaining}")
        return

    print("✅ Dedup complete — exactly 78 rules remain.")

    # Reset approval_status → pending_review so validator will re-process them.
    # The first validation run used update_many(rule_id) which updated BOTH duplicate
    # copies.  After dedup the surviving 78 docs still have their old (wrong) status.
    reset_result = coll.update_many(
        {"source.batch_id": BATCH_ID},
        {"$set": {"approval_status": "pending_review"}, "$unset": {"validation": ""}},
    )
    print(f"✅ Reset {reset_result.modified_count} rules → pending_review (validation cleared).")

if __name__ == "__main__":
    main()
