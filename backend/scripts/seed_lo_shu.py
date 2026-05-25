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

from lo_shu_router import (  # noqa: E402
    ARROW_DOCUMENTS,
    MISSING_NUMBER_DOCUMENTS,
    NUMBER_DEEP_DIVE_DOCUMENTS,
    PERSONAL_YEAR_DOCUMENTS,
    PROBLEM_AREA_DOCUMENTS,
)


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
        payload["seed_batch"] = "lo-shu-grid-v2-2026-05-25"
        payload["updated_at"] = now
        payload.setdefault("created_at", now)
        stamped.append(payload)
    return stamped


def main() -> int:
    args = parse_args()
    missing_docs = stamp_documents(MISSING_NUMBER_DOCUMENTS, "lo_shu_missing_numbers")
    arrow_docs = stamp_documents(ARROW_DOCUMENTS, "lo_shu_arrows")
    number_docs = stamp_documents(NUMBER_DEEP_DIVE_DOCUMENTS, "lo_shu_numbers")
    problem_docs = stamp_documents(PROBLEM_AREA_DOCUMENTS, "lo_shu_problems")
    personal_year_docs = stamp_documents(PERSONAL_YEAR_DOCUMENTS, "lo_shu_personal_years")

    if args.dry_run:
        print(
            "Dry run: would seed "
            f"{len(missing_docs)} missing-number docs, "
            f"{len(arrow_docs)} arrow docs, "
            f"{len(number_docs)} number docs, "
            f"{len(problem_docs)} problem docs, and "
            f"{len(personal_year_docs)} personal-year docs."
        )
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

    for document in number_docs:
        db.lo_shu_numbers.update_one({"number": document["number"]}, {"$set": document}, upsert=True)

    for document in problem_docs:
        db.lo_shu_problems.update_one({"slug": document["slug"]}, {"$set": document}, upsert=True)

    for document in personal_year_docs:
        db.lo_shu_personal_years.update_one({"number": document["number"]}, {"$set": document}, upsert=True)

    print(
        f"Seeded {len(missing_docs)} documents into lo_shu_missing_numbers, "
        f"{len(arrow_docs)} into lo_shu_arrows, "
        f"{len(number_docs)} into lo_shu_numbers, "
        f"{len(problem_docs)} into lo_shu_problems, and "
        f"{len(personal_year_docs)} into lo_shu_personal_years."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
