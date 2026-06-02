#!/usr/bin/env python3
"""Export existing MongoDB rules to a temp folder for cross-text dedup.

Maps interpretation.detailed → full_text and coerces legacy string conditions
so ke_dedup_script.py can compare them against new decode-folder rules.

Usage:
    # Export ALL rules (default -- use when new book has 0 rules in MongoDB):
    MONGO_URL="..." python3 backend/scripts/export_mongo_for_dedup.py

    # Export all rules EXCEPT a specific batch (use when re-running dedup post-ingest):
    MONGO_URL="..." python3 backend/scripts/export_mongo_for_dedup.py \
      --exclude-batch "300-combinations-v1-20260531"
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from pymongo import MongoClient

OUTPUT_DIR = Path("/tmp/mongo_existing_rules_dedup")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export MongoDB rules for dedup.")
    parser.add_argument(
        "--exclude-batch", default=None,
        help="Optional batch_id to exclude (e.g. the batch currently being ingested)",
    )
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR))
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    parser.add_argument("--db-name", default="horoscope_db")
    return parser.parse_args()


def build_query(exclude_batch: str | None) -> dict:
    """
    Build MongoDB query to fetch all rules (optionally excluding one batch).

    L4 gotcha: legacy rules have ingest_batch_id = null (field exists, value is null).
    Using $nin alone won't reliably match them. Use explicit $or to cover all cases.
    """
    if not exclude_batch:
        return {}  # all rules

    return {
        "$or": [
            {"ingest_batch_id": {"$exists": False}},
            {"ingest_batch_id": None},
            {"ingest_batch_id": {"$nin": [exclude_batch]}},
        ]
    }


def main() -> None:
    args = parse_args()

    if not args.mongo_url:
        print("ERROR: --mongo-url not provided and MONGO_URL env var not set.", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir)
    # Always clear the output directory before writing to prevent stale files
    # from a previous run appearing as false positives in the dedup comparison.
    if output_dir.exists():
        shutil.rmtree(output_dir)
        print(f"Cleared stale export directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=15000)
    db = client[args.db_name]

    query = build_query(args.exclude_batch)
    if args.exclude_batch:
        print(f"Excluding batch: {args.exclude_batch}")
    else:
        print("Exporting ALL rules from MongoDB (no exclusion)")

    rules = list(db["interpretation_rules"].find(query, {"_id": 0}))
    print(f"Fetched {len(rules)} rules from MongoDB")

    # Group by source_book for manageable file sizes
    groups: dict[str, list[dict]] = {}
    for rule in rules:
        book = rule.get("source_book") or "unknown"
        key = book.replace(" ", "_").replace("/", "_")
        groups.setdefault(key, []).append(rule)

    exported = 0
    for book_key, book_rules in sorted(groups.items()):
        mapped = []
        for r in book_rules:
            # L3: map interpretation.detailed → full_text for dedup compatibility
            interp = r.get("interpretation") or {}
            full_text = (
                interp.get("detailed")
                or interp.get("full_text")
                or r.get("full_text")
                or ""
            )

            # L3: coerce legacy string conditions → dict
            raw_cond = r.get("condition")
            if isinstance(raw_cond, dict):
                cond = raw_cond
            elif isinstance(raw_cond, str):
                cond = {"type": raw_cond}
            else:
                cond = {}

            mapped_rule = {
                "rule_id":        r.get("rule_id", ""),
                "condition":      cond,
                "full_text":      full_text,
                "claim_polarity": r.get("claim_polarity") or r.get("polarity") or r.get("outcome_polarity") or "neutral",
                "source_book":    r.get("source_book", ""),
                "ingest_batch_id": r.get("ingest_batch_id"),
            }
            mapped.append(mapped_rule)

        # Save as a *_Rules*.json file (ke_dedup_script requires this glob pattern)
        out_path = output_dir / f"{book_key}_Rules.json"
        out_path.write_text(
            json.dumps(mapped, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        exported += len(mapped)
        print(f"  {book_key}: {len(mapped)} rules → {out_path.name}")

    print(f"\nTotal exported: {exported} rules across {len(groups)} source_book groups")
    print(f"Output directory: {output_dir}")
    client.close()


if __name__ == "__main__":
    main()
