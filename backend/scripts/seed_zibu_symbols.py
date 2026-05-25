#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

try:
    from pymongo import MongoClient
except ImportError:
    print("ERROR: pymongo not installed. Run: pip install pymongo")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from zibu_catalog import get_all_symbols  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed the zibu_symbols collection with the canonical 88-symbol catalog.")
    parser.add_argument("--mongo-url", default=os.environ.get("MONGO_URL"), help="MongoDB connection string")
    parser.add_argument("--db-name", default=os.environ.get("DB_NAME", "horoscope_db"), help="MongoDB database name")
    parser.add_argument("--dry-run", action="store_true", help="Print counts without writing to MongoDB")
    args = parser.parse_args()

    if not args.mongo_url:
        print("ERROR: --mongo-url or MONGO_URL environment variable is required")
        sys.exit(1)

    documents = get_all_symbols()
    print(f"Prepared {len(documents)} Zibu symbol documents.")

    if args.dry_run:
        print("Dry run complete. No database writes were performed.")
        return

    client = MongoClient(args.mongo_url)
    collection = client[args.db_name].zibu_symbols

    upserted = 0
    for document in documents:
        result = collection.update_one({"slug": document["slug"]}, {"$set": document}, upsert=True)
        if result.upserted_id is not None or result.modified_count:
            upserted += 1

    print(f"Upserted {upserted} documents into {args.db_name}.zibu_symbols.")


if __name__ == "__main__":
    main()
