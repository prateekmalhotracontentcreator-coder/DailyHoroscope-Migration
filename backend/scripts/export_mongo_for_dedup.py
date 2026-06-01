#!/usr/bin/env python3
"""Export existing MongoDB rules (excluding new batch) to a temp folder for dedup."""

import json
import sys
from pathlib import Path
from pymongo import MongoClient

MONGO_URL = "mongodb+srv://PrateekMalhotra:NewDB%40%21123@cluster0.bqtc8l9.mongodb.net/?appName=Cluster0"
DB_NAME = "horoscope_db"
EXCLUDE_BATCH = "bphs-vol2-ch49-51-v1"
OUTPUT_DIR = Path("/tmp/mongo_existing_rules_dedup")

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    client = MongoClient(MONGO_URL)
    db = client[DB_NAME]

    # Fetch all rules NOT from the new batch (null batch_id or different batch)
    query = {
        "$or": [
            {"ingest_batch_id": {"$exists": False}},
            {"ingest_batch_id": None},
            {"ingest_batch_id": {"$nin": [EXCLUDE_BATCH]}},
        ]
    }
    rules = list(db["interpretation_rules"].find(query, {"_id": 0}))
    print(f"Fetched {len(rules)} existing rules from MongoDB")

    # Group by source_book for manageable file sizes
    groups: dict[str, list[dict]] = {}
    for rule in rules:
        book = rule.get("source_book") or "unknown"
        # Sanitize for filename
        key = book.replace(" ", "_").replace("/", "_")
        groups.setdefault(key, []).append(rule)

    exported = 0
    for book_key, book_rules in sorted(groups.items()):
        # Map interpretation.detailed → full_text for dedup compatibility
        mapped = []
        for r in book_rules:
            interp = r.get("interpretation") or {}
            detailed = interp.get("detailed") or interp.get("full_text") or ""
            # Coerce condition to dict (legacy rules may have string conditions)
            raw_cond = r.get("condition")
            if isinstance(raw_cond, dict):
                cond = raw_cond
            elif isinstance(raw_cond, str):
                cond = {"type": raw_cond}
            else:
                cond = {}
            # Build a dedup-compatible record
            mapped_rule = {
                "rule_id": r.get("rule_id", ""),
                "condition": cond,
                "full_text": detailed,
                "polarity": r.get("polarity") or r.get("outcome_polarity") or "neutral",
                "source_book": r.get("source_book", ""),
                "ingest_batch_id": r.get("ingest_batch_id"),
            }
            mapped.append(mapped_rule)

        # Save as a *_Rules*.json file (ke_dedup_script requires this glob pattern)
        out_path = OUTPUT_DIR / f"{book_key}_Rules.json"
        out_path.write_text(json.dumps(mapped, ensure_ascii=False, indent=2), encoding="utf-8")
        exported += len(mapped)
        print(f"  {book_key}: {len(mapped)} rules → {out_path.name}")

    print(f"\nTotal exported: {exported} rules across {len(groups)} files")
    print(f"Output directory: {OUTPUT_DIR}")
    client.close()

if __name__ == "__main__":
    main()
