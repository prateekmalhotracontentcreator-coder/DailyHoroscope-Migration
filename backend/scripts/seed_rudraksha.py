#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from pymongo import MongoClient


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rudraksha_content import (  # noqa: E402
    get_planet_rudraksha_documents,
    get_problem_rudraksha_documents,
    get_rudraksha_documents,
    get_sign_rudraksha_documents,
)


def _seed_documents(seed: list[dict], now: str) -> list[dict]:
    return [{**item, "seeded_at": now} for item in seed]


def _collection_payloads(now: str) -> dict[str, list[dict]]:
    return {
        "rudraksha_mukhis": _seed_documents(get_rudraksha_documents(), now),
        "rudraksha_planets": _seed_documents(get_planet_rudraksha_documents(), now),
        "rudraksha_problems": _seed_documents(get_problem_rudraksha_documents(), now),
        "rudraksha_signs": _seed_documents(get_sign_rudraksha_documents(), now),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed Rudraksha content collections")
    parser.add_argument("--mongo-url", default=os.environ.get("MONGO_URL"))
    parser.add_argument("--db-name", default=os.environ.get("DB_NAME", "horoscope_db"))
    parser.add_argument("--replace", action="store_true", help="Replace existing Rudraksha documents.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.mongo_url:
        print("ERROR: --mongo-url or MONGO_URL environment variable is required")
        sys.exit(1)

    now = datetime.now(timezone.utc).isoformat()
    payloads = _collection_payloads(now)

    if args.dry_run:
        for collection_name, documents in payloads.items():
            print(f"DRY RUN: {len(documents)} document(s) ready for {collection_name}")
            for item in documents[:3]:
                label = item.get("name") or item.get("title") or item.get("slug")
                print(f"  {item['slug']} -> {label}")
            if len(documents) > 3:
                print("  ...")
        return

    client = MongoClient(args.mongo_url)
    db = client[args.db_name]
    existing_counts = {
        collection_name: db[collection_name].count_documents({})
        for collection_name in payloads
    }
    occupied = {name: count for name, count in existing_counts.items() if count}
    if occupied and not args.replace:
        print("One or more Rudraksha collections already contain documents:")
        for collection_name, count in occupied.items():
            print(f"  {collection_name}: {count}")
        print("Re-run with --replace to refresh the collections.")
        sys.exit(1)

    for collection_name, documents in payloads.items():
        collection = db[collection_name]
        if args.replace:
            collection.delete_many({})
        collection.insert_many(documents)
        collection.create_index("slug", unique=True)
        if collection_name == "rudraksha_mukhis":
            collection.create_index("mukhi", unique=True)

    print("Seeded Rudraksha collections:")
    for collection_name, documents in payloads.items():
        print(f"  {collection_name}: {len(documents)} document(s)")
    print("Indexes ensured: slug (unique) on all collections, mukhi (unique) on rudraksha_mukhis")


if __name__ == "__main__":
    main()
