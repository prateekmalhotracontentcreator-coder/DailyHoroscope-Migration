#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

from pymongo import MongoClient


TARGET_CHAPTERS = ["47", "54", "56", "57", "58"]
ANTARDASHA_RE = re.compile(r"during\s+(\w+)\s+Antardasha", re.IGNORECASE)
PLANETS = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Backfill condition.antardasha_planet on existing BPHS antardasha rules"
    )
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL", "mongodb://localhost:27017"))
    parser.add_argument("--db-name", default=os.getenv("DB_NAME", "horoscope_db"))
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def extract_antardasha_planet(summary: str) -> str | None:
    match = ANTARDASHA_RE.search(summary or "")
    if not match:
        return None
    planet = match.group(1).strip().title()
    return planet if planet in PLANETS else None


def main() -> int:
    args = parse_args()
    client = MongoClient(args.mongo_url)
    collection = client[args.db_name]["interpretation_rules"]

    query = {
        "condition.type": "dasha_planet",
        "source.chapter": {"$in": TARGET_CHAPTERS},
        "$or": [
            {"condition.antardasha_planet": {"$exists": False}},
            {"condition.antardasha_planet": None},
            {"condition.antardasha_planet": ""},
        ],
    }
    projection = {"_id": 1, "rule_id": 1, "interpretation.summary": 1}
    docs = list(collection.find(query, projection))

    updated = 0
    failed: list[str] = []

    print(f"Found {len(docs)} candidate rule(s) across chapters {', '.join(TARGET_CHAPTERS)}")
    for doc in docs:
        rule_id = str(doc.get("rule_id") or "")
        interpretation = doc.get("interpretation") or {}
        summary = str(interpretation.get("summary") or "")
        antardasha_planet = extract_antardasha_planet(summary)
        if not antardasha_planet:
            failed.append(rule_id or str(doc.get("_id")))
            continue

        if args.dry_run:
            print(f"[DRY RUN] {rule_id} -> {antardasha_planet}")
            updated += 1
            continue

        result = collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"condition.antardasha_planet": antardasha_planet}},
        )
        if result.modified_count == 1:
            updated += 1

    remaining = collection.count_documents(query)
    print("")
    print(f"Updated: {updated}")
    print(f"Remaining missing antardasha_planet: {remaining}")
    if failed:
        print(f"Regex failed for {len(failed)} rule(s):")
        for rule_id in failed[:25]:
            print(f"  - {rule_id}")
        if len(failed) > 25:
            print(f"  ... and {len(failed) - 25} more")

    client.close()
    return 0 if remaining == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
