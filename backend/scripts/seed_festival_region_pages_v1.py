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

from seo_m3_builders import build_festival_region_doc
from seo_m3_catalog import FESTIVAL_SLUGS, REGION_SLUGS


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed festival_region_pages collection for SEO-20K M3")
    parser.add_argument("--mongo-url", default=os.environ.get("MONGO_URL"))
    parser.add_argument("--db-name", default=os.environ.get("DB_NAME", "horoscope_db"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.mongo_url:
        print("ERROR: --mongo-url or MONGO_URL environment variable is required")
        sys.exit(1)

    docs = []
    now = datetime.now(timezone.utc).isoformat()
    for festival_slug in FESTIVAL_SLUGS:
        for region_slug in REGION_SLUGS:
            doc = build_festival_region_doc(festival_slug, region_slug)
            doc["seeded_at"] = now
            doc["version"] = "seo-20k-m3-v1"
            docs.append(doc)

    if args.dry_run:
        print(f"Prepared {len(docs)} festival region docs")
        print(docs[0]["meta_title"])
        return

    client = MongoClient(args.mongo_url)
    collection = client[args.db_name]["festival_region_pages"]
    modified = 0
    for doc in docs:
        collection.update_one(
            {"festival_slug": doc["festival_slug"], "region_slug": doc["region_slug"]},
            {"$set": doc},
            upsert=True,
        )
        modified += 1
    print(f"Upserted {modified} documents into festival_region_pages")


if __name__ == "__main__":
    main()
