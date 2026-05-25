#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone
from pathlib import Path
import sys

try:
    from pymongo import MongoClient
except ImportError:
    print("ERROR: pymongo not installed. Run: pip install pymongo")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from seo_m3_builders import build_character_placement_doc
from seo_m3_catalog import CHART_POINTS, HOUSES, SIGN_SLUGS


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed character_placements collection for SEO-20K M3")
    parser.add_argument("--mongo-url", default=os.environ.get("MONGO_URL"))
    parser.add_argument("--db-name", default=os.environ.get("DB_NAME", "horoscope_db"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.mongo_url:
        print("ERROR: --mongo-url or MONGO_URL environment variable is required")
        sys.exit(1)

    docs = []
    now = datetime.now(timezone.utc).isoformat()
    for sign_slug in SIGN_SLUGS:
        for chart_point in CHART_POINTS:
            for house in HOUSES:
                doc = build_character_placement_doc(sign_slug, chart_point["slug"], house["slug"])
                doc["seeded_at"] = now
                doc["version"] = "seo-20k-m3-v1"
                docs.append(doc)

    if args.dry_run:
        print(f"Prepared {len(docs)} character placement docs")
        print(docs[0]["title"])
        return

    client = MongoClient(args.mongo_url)
    collection = client[args.db_name]["character_placements"]
    modified = 0
    for doc in docs:
        collection.update_one(
            {
                "sign_slug": doc["sign_slug"],
                "chart_point_slug": doc["chart_point_slug"],
                "house_slug": doc["house_slug"],
            },
            {"$set": doc},
            upsert=True,
        )
        modified += 1
    print(f"Upserted {modified} documents into character_placements")


if __name__ == "__main__":
    main()
