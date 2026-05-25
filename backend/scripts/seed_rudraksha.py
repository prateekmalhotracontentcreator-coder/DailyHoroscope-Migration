#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from pymongo import MongoClient


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rudraksha_content import get_rudraksha_documents  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed the rudraksha_mukhis collection")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", required=True)
    parser.add_argument("--replace", action="store_true", help="Replace existing rudraksha_mukhis documents.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    seed = get_rudraksha_documents()
    now = datetime.now(timezone.utc).isoformat()
    documents = [{**item, "seeded_at": now} for item in seed]

    if args.dry_run:
        print(f"DRY RUN: {len(documents)} Rudraksha documents ready for rudraksha_mukhis")
        for item in documents[:5]:
            print(f"  {item['mukhi']:>2} -> {item['name']} | {item['ruling_planet']} | {item['price_range']}")
        print("  ...")
        return

    client = MongoClient(args.mongo_url)
    db = client[args.db_name]
    collection = db["rudraksha_mukhis"]

    existing = collection.count_documents({})
    if existing and not args.replace:
        print(
            "rudraksha_mukhis already contains "
            f"{existing} document(s). Re-run with --replace to refresh the collection."
        )
        sys.exit(1)

    if args.replace:
        collection.delete_many({})

    collection.insert_many(documents)
    collection.create_index("mukhi", unique=True)
    collection.create_index("slug", unique=True)

    print(f"Seeded rudraksha_mukhis with {len(documents)} documents.")
    print("Indexes ensured: mukhi (unique), slug (unique)")


if __name__ == "__main__":
    main()
