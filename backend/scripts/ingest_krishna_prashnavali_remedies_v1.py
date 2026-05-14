#!/usr/bin/env python3
"""
ingest_krishna_prashnavali_remedies_v1.py

Temple-run import utility for the Krishna Prashnavali Remedies collection.

Source bundle:
  /Users/apple/Documents/New project/KRISHNA_PRASHNAVALI_REMEDIES_INGEST_V1.json

Target collection:
  horoscope_db.krishna_prashnavali_remedies

Workflow:
  python3 backend/scripts/ingest_krishna_prashnavali_remedies_v1.py --dry-run
  python3 backend/scripts/ingest_krishna_prashnavali_remedies_v1.py --save /tmp/kp_remedies.json
  python3 backend/scripts/ingest_krishna_prashnavali_remedies_v1.py --upload \
      --mongo-url "$MONGO_URL" --db-name horoscope_db
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SOURCE_JSON = Path("/Users/apple/Documents/New project/KRISHNA_PRASHNAVALI_REMEDIES_INGEST_V1.json")
COLLECTION = "krishna_prashnavali_remedies"
SCIENCE_ID = "krishna_prashnavali_remedies"
EXPECTED_COUNT = 36


def _load_records() -> list[dict]:
    if not SOURCE_JSON.exists():
        raise FileNotFoundError(f"Source bundle not found: {SOURCE_JSON}")

    payload = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    records = payload.get("records", [])
    if len(records) != EXPECTED_COUNT:
        raise ValueError(f"Expected {EXPECTED_COUNT} records, found {len(records)}")

    validated: list[dict] = []
    seen_ids: set[str] = set()
    for index, record in enumerate(records, start=1):
        remedy_id = str(record.get("remedy_id", "")).strip()
        if not remedy_id:
            raise ValueError(f"Record {index} missing remedy_id")
        if remedy_id in seen_ids:
            raise ValueError(f"Duplicate remedy_id detected: {remedy_id}")
        if record.get("science_id") != SCIENCE_ID:
            raise ValueError(
                f"Record {remedy_id} has science_id={record.get('science_id')} "
                f"but expected {SCIENCE_ID}"
            )
        seen_ids.add(remedy_id)
        validated.append(record)
    return validated


def _print_summary(records: list[dict]) -> None:
    by_verdict: dict[str, int] = {}
    for record in records:
        verdict = str(record.get("verdict_display", "UNKNOWN"))
        by_verdict[verdict] = by_verdict.get(verdict, 0) + 1

    print("\n" + "=" * 64)
    print(" Krishna Prashnavali Remedies -- Dry Run")
    print(f" Total records: {len(records)}")
    print(f" Science ID:    {SCIENCE_ID}")
    print(f" Collection:    {COLLECTION}")
    print("=" * 64)
    print("\n Verdict split:")
    for verdict, count in sorted(by_verdict.items()):
        print(f"   {verdict:<8} {count:>3d}")
    sample = records[0]
    print("\n Sample record:")
    print(f"   remedy_id : {sample.get('remedy_id')}")
    print(f"   answer_id : {sample.get('answer_id')}")
    print(f"   title     : {sample.get('title', {}).get('english_block', '')}")
    print(f"   ritual    : {sample.get('ritual_remedy', {}).get('english_block', '')}")
    print(f"   behavioral: {sample.get('behavioral_display_hint', {}).get('english_block', '')}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import Krishna Prashnavali remedy records into MongoDB"
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--save", metavar="FILE")
    parser.add_argument("--upload", action="store_true")
    parser.add_argument("--mongo-url", default="")
    parser.add_argument("--db-name", default="horoscope_db")
    args = parser.parse_args()

    if not args.dry_run and not args.save and not args.upload:
        parser.print_help()
        sys.exit(1)

    records = _load_records()

    if args.dry_run or args.save:
        _print_summary(records)
        if args.save:
            out_path = Path(args.save)
            out_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"Saved {len(records)} records → {out_path}")
        if not args.upload:
            return

    if args.upload:
        if not args.mongo_url:
            print("ERROR: --mongo-url required when using --upload")
            sys.exit(1)
        try:
            from pymongo import MongoClient, UpdateOne
        except ImportError:
            print("ERROR: pymongo is not installed in this environment")
            sys.exit(1)

        client = MongoClient(args.mongo_url)
        collection = client[args.db_name][COLLECTION]
        ops = [
            UpdateOne(
                {"remedy_id": record["remedy_id"]},
                {"$set": record},
                upsert=True,
            )
            for record in records
        ]
        result = collection.bulk_write(ops, ordered=False)
        print(
            f"Imported {len(records)} Krishna remedy records → "
            f"{args.db_name}.{COLLECTION} "
            f"(upserted={result.upserted_count}, modified={result.modified_count})"
        )
        client.close()


if __name__ == "__main__":
    main()
