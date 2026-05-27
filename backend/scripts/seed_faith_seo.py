#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

try:
    from pymongo import MongoClient
except ImportError:
    print("ERROR: pymongo not installed. Run: pip install pymongo")
    sys.exit(1)

from faith_bible_data import build_bible_pages
from faith_gita_data import build_gita_pages
from faith_seo_data import build_daily_pages, build_transit_pages


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed Faith module phase-one SEO documents.")
    parser.add_argument("--mongo-url", required=True, help="MongoDB connection string")
    parser.add_argument("--db-name", default="horoscope_db", help="MongoDB database name")
    parser.add_argument("--dry-run", action="store_true", help="Print counts without writing to MongoDB")
    args = parser.parse_args()

    transit_pages = build_transit_pages()
    daily_pages = build_daily_pages()
    gita_pages = build_gita_pages()
    bible_pages = build_bible_pages()
    print(
        f"Prepared {len(transit_pages)} faith transit pages, {len(daily_pages)} faith daily pages, "
        f"{len(gita_pages)} faith Gita pages, and {len(bible_pages)} faith Bible pages."
    )

    if args.dry_run:
        print("Dry run complete. No database writes were performed.")
        return

    client = MongoClient(args.mongo_url)
    db = client[args.db_name]

    transit_upserts = 0
    for document in transit_pages:
        result = db.faith_transit_pages.update_one(
            {"transit_slug": document["transit_slug"], "tradition": document["tradition"]},
            {"$set": document},
            upsert=True,
        )
        if result.upserted_id is not None or result.modified_count:
            transit_upserts += 1

    daily_upserts = 0
    for document in daily_pages:
        result = db.faith_daily_pages.update_one(
            {"sign_slug": document["sign_slug"], "month_slug": document["month_slug"]},
            {"$set": document},
            upsert=True,
        )
        if result.upserted_id is not None or result.modified_count:
            daily_upserts += 1

    gita_upserts = 0
    for document in gita_pages:
        result = db.faith_gita_pages.update_one(
            {
                "chapter": document["chapter"],
                "verse": document["verse"],
                "situation_slug": document["situation_slug"],
            },
            {"$set": document},
            upsert=True,
        )
        if result.upserted_id is not None or result.modified_count:
            gita_upserts += 1

    bible_upserts = 0
    for document in bible_pages:
        result = db.faith_bible_pages.update_one(
            {
                "topic_slug": document["topic_slug"],
                "transition_slug": document["transition_slug"],
            },
            {"$set": document},
            upsert=True,
        )
        if result.upserted_id is not None or result.modified_count:
            bible_upserts += 1

    print(f"Upserted {transit_upserts} documents into {args.db_name}.faith_transit_pages.")
    print(f"Upserted {daily_upserts} documents into {args.db_name}.faith_daily_pages.")
    print(f"Upserted {gita_upserts} documents into {args.db_name}.faith_gita_pages.")
    print(f"Upserted {bible_upserts} documents into {args.db_name}.faith_bible_pages.")


if __name__ == "__main__":
    main()
