#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re

from pymongo import MongoClient


TARGET_CHAPTERS = ["52", "53", "54", "55", "56", "57", "58"]
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


def _summary_planets(summary: str) -> list[str]:
    planets: list[str] = []
    for match in re.finditer(r"\b(Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)\b", summary or "", re.IGNORECASE):
        planet = match.group(1).strip().title()
        if planet in PLANETS and planet not in planets:
            planets.append(planet)
    return planets


def derive_antardasha_planet(summary: str, condition: dict) -> tuple[str | None, str]:
    dasha_lord = str(condition.get("dasha_lord") or "").strip().title()
    planets_involved = condition.get("planets_involved") or []
    candidates: list[str] = []
    all_planets: list[str] = []
    for planet in planets_involved:
        normalized = str(planet or "").strip().title()
        if normalized not in PLANETS:
            continue
        if normalized not in all_planets:
            all_planets.append(normalized)
        if normalized == dasha_lord:
            continue
        if normalized not in candidates:
            candidates.append(normalized)

    if len(candidates) == 1:
        return candidates[0], "derived"
    if not candidates and dasha_lord and dasha_lord in all_planets:
        return dasha_lord, "self_antardasha"
    if len(candidates) > 1:
        for planet in _summary_planets(summary):
            if planet != dasha_lord:
                return planet, "first_planet_heuristic"
        return None, "ambiguous"
    return None, "missing"


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
    projection = {
        "_id": 1,
        "rule_id": 1,
        "interpretation.summary": 1,
        "condition.dasha_lord": 1,
        "condition.planets_involved": 1,
    }
    docs = list(collection.find(query, projection))

    updated = 0
    regex_hits = 0
    derived_hits = 0
    failed: list[str] = []
    ambiguous: list[str] = []

    print(f"Found {len(docs)} candidate rule(s) across chapters {', '.join(TARGET_CHAPTERS)}")
    for doc in docs:
        rule_id = str(doc.get("rule_id") or "")
        interpretation = doc.get("interpretation") or {}
        summary = str(interpretation.get("summary") or "")
        condition = doc.get("condition") or {}

        antardasha_planet = extract_antardasha_planet(summary)
        source = "regex"
        if not antardasha_planet:
            antardasha_planet, source = derive_antardasha_planet(summary, condition)
        if not antardasha_planet:
            if source == "ambiguous":
                ambiguous.append(rule_id or str(doc.get("_id")))
            else:
                failed.append(rule_id or str(doc.get("_id")))
            continue

        if source == "regex":
            regex_hits += 1
        elif source == "derived":
            derived_hits += 1

        if args.dry_run:
            print(f"[DRY RUN] {rule_id} -> {antardasha_planet} ({source})")
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
    print(f"Regex matches: {regex_hits}")
    print(f"Derived matches: {derived_hits}")
    print(f"Remaining missing antardasha_planet: {remaining}")
    if ambiguous:
        print(f"Ambiguous manual-review cases: {len(ambiguous)}")
        for rule_id in ambiguous[:25]:
            print(f"  - {rule_id}")
        if len(ambiguous) > 25:
            print(f"  ... and {len(ambiguous) - 25} more")
    if failed:
        print(f"Unresolved after regex + derivation: {len(failed)} rule(s)")
        for rule_id in failed[:25]:
            print(f"  - {rule_id}")
        if len(failed) > 25:
            print(f"  ... and {len(failed) - 25} more")

    client.close()
    return 0 if remaining == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
