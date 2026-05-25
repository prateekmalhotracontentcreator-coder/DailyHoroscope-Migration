#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from pymongo import MongoClient
except ImportError:
    print("ERROR: pymongo not installed. Run: pip install pymongo")
    sys.exit(1)


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from lo_shu_router import ARROW_DOCUMENTS, MISSING_NUMBER_DOCUMENTS  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed Lo Shu Grid content collections.")
    parser.add_argument("--mongo-url", default=os.environ.get("MONGO_URL"), help="MongoDB connection URL")
    parser.add_argument("--db-name", default=os.environ.get("DB_NAME", "horoscope_db"), help="MongoDB database name")
    parser.add_argument("--dry-run", action="store_true", help="Print counts without writing to MongoDB")
    return parser.parse_args()


def stamp_documents(documents: list[dict], collection_name: str) -> list[dict]:
    now = datetime.now(timezone.utc)
    stamped: list[dict] = []
    for document in documents:
        payload = dict(document)
        payload["collection"] = collection_name
        payload["seed_batch"] = "lo-shu-grid-v1-2026-05-23"
        payload["updated_at"] = now
        payload.setdefault("created_at", now)
        stamped.append(payload)
    return stamped


def main() -> int:
    args = parse_args()
    missing_docs = stamp_documents(MISSING_NUMBER_DOCUMENTS, "lo_shu_missing_numbers")
    arrow_docs = stamp_documents(ARROW_DOCUMENTS, "lo_shu_arrows")

    if args.dry_run:
        print(f"Dry run: would seed {len(missing_docs)} missing-number docs and {len(arrow_docs)} arrow docs.")
        return 0

    if not args.mongo_url:
        print("ERROR: Mongo URL missing. Pass --mongo-url or set MONGO_URL.")
        return 1

    client = MongoClient(args.mongo_url)
    db = client[args.db_name]

    for document in missing_docs:
        db.lo_shu_missing_numbers.update_one({"number": document["number"]}, {"$set": document}, upsert=True)

    for document in arrow_docs:
        db.lo_shu_arrows.update_one({"slug": document["slug"]}, {"$set": document}, upsert=True)

    print(
        f"Seeded {len(missing_docs)} documents into lo_shu_missing_numbers and "
        f"{len(arrow_docs)} documents into lo_shu_arrows."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
