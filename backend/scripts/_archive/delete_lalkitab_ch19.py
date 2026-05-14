#!/usr/bin/env python3
"""
Delete ALL rules for batch lalkitab-ch19-v1-20260426 from MongoDB.
Run this, then re-ingest with ingest_lalkitab_ch19_v1.py (once only).
"""

import os
import sys
from pymongo import MongoClient

BATCH_ID  = "lalkitab-ch19-v1-20260426"
DB_NAME   = "horoscope_db"
COLL_NAME = "interpretation_rules"


def main():
    mongo_url = os.environ.get("MONGO_URL", "").strip()
    if not mongo_url:
        mongo_url = input("Paste MongoDB Atlas URL: ").strip()
    if not mongo_url:
        sys.exit("ERROR: no MONGO_URL provided")

    client = MongoClient(mongo_url)
    coll   = client[DB_NAME][COLL_NAME]

    count = coll.count_documents({"source.batch_id": BATCH_ID})
    print(f"Found {count} docs with batch_id={BATCH_ID}")

    if count == 0:
        print("Nothing to delete.")
        return

    confirm = input(f"Delete all {count} docs? [y/N]: ").strip().lower()
    if confirm != "y":
        print("Aborted.")
        return

    result = coll.delete_many({"source.batch_id": BATCH_ID})
    print(f"✅ Deleted {result.deleted_count} documents.")

    remaining = coll.count_documents({"source.batch_id": BATCH_ID})
    print(f"   Remaining: {remaining}")


if __name__ == "__main__":
    main()
