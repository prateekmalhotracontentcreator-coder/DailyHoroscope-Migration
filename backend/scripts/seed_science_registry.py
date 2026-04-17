#!/usr/bin/env python3
"""
Seed the science_registry collection in MongoDB.

This collection is required by Sprint 2 (G-04 supersession table runtime lookup).
Run once — script aborts safely if documents already exist.

Usage (from ~/DailyHoroscope-Migration/):
    python3 backend/scripts/seed_science_registry.py \
        --mongo-url "$MONGO_URL" --db-name EverydayHoroscope

Seed data confirmed by Codex (Commission I Phase 1.2, 18 Apr 2026).
"""
import argparse
import sys
from datetime import datetime, timezone

from pymongo import MongoClient

SEED = [
    {
        "science_id": "vedic_astrology",
        "display_name": "Vedic Astrology",
        "hierarchy_rank": 1,
        "authority_domain": [
            "career", "wealth", "relationships", "health",
            "education", "spirituality", "longevity", "general"
        ],
        "defers_to": [],
        "complements": ["numerology", "palmistry", "tarot"],
        "contradiction_policy": "backbone_or_primary_lead",
    },
    {
        "science_id": "numerology",
        "display_name": "Numerology",
        "hierarchy_rank": 2,
        "authority_domain": ["general", "career", "relationships", "wealth"],
        "defers_to": ["vedic_astrology"],
        "complements": ["vedic_astrology", "tarot"],
        "contradiction_policy": "secondary_supportive",
    },
    {
        "science_id": "palmistry",
        "display_name": "Palmistry",
        "hierarchy_rank": 3,
        "authority_domain": ["health", "longevity", "relationships"],
        "defers_to": ["vedic_astrology"],
        "complements": ["vedic_astrology", "numerology"],
        "contradiction_policy": "secondary_specialist",
    },
    {
        "science_id": "tarot",
        "display_name": "Tarot",
        "hierarchy_rank": 4,
        "authority_domain": ["spirituality", "general", "relationships"],
        "defers_to": ["vedic_astrology", "numerology"],
        "complements": ["numerology", "vedic_astrology"],
        "contradiction_policy": "reflective_advisory",
    },
]


def main():
    parser = argparse.ArgumentParser(description="Seed science_registry collection")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   required=True)
    parser.add_argument("--dry-run",   action="store_true")
    args = parser.parse_args()

    now = datetime.now(timezone.utc).isoformat()

    if args.dry_run:
        print(f"\nDRY RUN — {len(SEED)} documents would be inserted into science_registry\n")
        for doc in SEED:
            print(f"  [{doc['hierarchy_rank']}] {doc['science_id']:<20} rank={doc['hierarchy_rank']}  policy={doc['contradiction_policy']}")
            print(f"       authority: {doc['authority_domain']}")
            print(f"       defers_to: {doc['defers_to']}")
        print()
        return

    client = MongoClient(args.mongo_url)
    db     = client[args.db_name]
    col    = db["science_registry"]

    existing = col.count_documents({})
    if existing > 0:
        print(f"\n⚠️  science_registry already contains {existing} document(s) — aborting.")
        print("   Run with --dry-run to inspect, or drop the collection manually first.\n")
        sys.exit(1)

    docs = [{**doc, "created_at": now} for doc in SEED]
    result = col.insert_many(docs)

    print(f"\n✅  Seeded science_registry — {len(result.inserted_ids)} documents")
    for doc in SEED:
        print(f"   [{doc['hierarchy_rank']}] {doc['science_id']:<20} → {doc['contradiction_policy']}")

    cols = sorted(db.list_collection_names())
    print(f"\n   Collections in {args.db_name}: {cols}")
    print(f"\n   Sprint 2 G-04 blocker: CLEARED — science_registry is now available.\n")


if __name__ == "__main__":
    main()
