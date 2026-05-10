#!/usr/bin/env python3
"""
ingest_strategist_v1.py — Lal Kitab Strategist module records

Sources:
  7. Lal Kitab_Career_The Strategist_Master Document (1).md
  The Strategist Module_LLM Specific Q&A_GAI.md
  Premium Report Generator (ID 1022 Narrative) + Full Module JSON Reconciliation Statement.md

science_id:  "lalkitab_strategist"
collection:  "knowledge_rules"
upsert key:  {id, science_id}
IDs covered: 701–1025, 1027, 651–675 (surrogates — kept at original IDs, no remap)

Usage:
  python3 scripts/ingest_strategist_v1.py --dry-run
  python3 scripts/ingest_strategist_v1.py --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCIENCE_ID = "lalkitab_strategist"
APPROVAL   = "pending_human_review"
MODULE_IDS = {1022, 1027}

SOURCE_MASTER = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/"
    "Remedies + The Strategist/"
    "7. Lal Kitab_Career_The Strategist_Master Document (1).md"
)
SOURCE_QA = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/"
    "Remedies + The Strategist/"
    "The Strategist Module_LLM Specific Q&A_GAI.md"
)
SOURCE_RECONCILIATION = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/"
    "Remedies + The Strategist/"
    "Premium Report Generator (ID 1022 Narrative) + Full Module JSON Reconciliation Statement.md"
)

REQUIRED_FIELDS = [
    "id", "science_id", "trigger_condition", "strategy",
    "decision_logic", "pivot_logic", "pivot_action",
    "kpi_target", "remedy_id", "approval_status",
]

SURROGATE_EXTRA = ["surrogate_type", "relative_unavailable"]
HURDLE_EXTRA    = ["ui_warning"]


def _clean_text(s: str) -> str:
    s = re.sub(r"[‘’]", "'", s)
    s = re.sub(r"[“”]", '"', s)
    s = re.sub(r"\\\n", "", s)
    s = re.sub(r"\\(.)", r"\1", s)
    return s.strip()


def _extract_json_blocks(text: str) -> list[dict]:
    """Extract all JSON objects/arrays from markdown text."""
    records: list[dict] = []

    # Normalise curly/escaped characters
    text = _clean_text(text)

    # Try to find JSON arrays ([ ... ]) containing objects with "id" field
    for match in re.finditer(r'\[\s*\{.*?\}\s*\]', text, re.DOTALL):
        raw = match.group()
        try:
            batch = json.loads(raw)
            if isinstance(batch, list):
                for item in batch:
                    if isinstance(item, dict) and "id" in item:
                        records.append(item)
        except json.JSONDecodeError:
            pass

    # Also try individual objects with "id" field (for loose records)
    for match in re.finditer(r'\{[^{}]*"id"\s*:\s*\d+[^{}]*\}', text, re.DOTALL):
        raw = match.group()
        try:
            obj = json.loads(raw)
            if isinstance(obj, dict) and "id" in obj:
                if not any(r["id"] == obj["id"] for r in records):
                    records.append(obj)
        except json.JSONDecodeError:
            pass

    return records


def _normalise_record(r: dict) -> dict:
    """Ensure mandatory fields + science_id + approval_status."""
    out = {}
    for k, v in r.items():
        key = k.replace("\\", "").strip()
        val = _clean_text(str(v)) if isinstance(v, str) else v
        out[key] = val

    out["science_id"]       = SCIENCE_ID
    out["approval_status"]  = APPROVAL
    out["ingested_at"]      = datetime.now(timezone.utc).isoformat()

    # Ensure remedy_id is int
    if "remedy_id" in out:
        try:
            out["remedy_id"] = int(out["remedy_id"])
        except (TypeError, ValueError):
            pass

    # Ensure id is int
    if "id" in out:
        try:
            out["id"] = int(out["id"])
        except (TypeError, ValueError):
            pass

    return out


def validate_batch(batch: list[dict]) -> dict:
    errors = []
    for r in batch:
        rid = r.get("id")
        if rid in MODULE_IDS:
            continue
        missing = [f for f in REQUIRED_FIELDS if f not in r]
        if missing:
            errors.append({"id": rid, "missing": missing})
    return {"total": len(batch), "errors": len(errors), "detail": errors}


def load_records() -> list[dict]:
    all_records: dict[int, dict] = {}

    for source in [SOURCE_MASTER, SOURCE_QA, SOURCE_RECONCILIATION]:
        if not source.exists():
            print(f"[WARN] Source not found: {source}", file=sys.stderr)
            continue

        text = source.read_text(encoding="utf-8", errors="replace")
        extracted = _extract_json_blocks(text)
        print(f"[INFO] {source.name}: extracted {len(extracted)} raw records")

        for r in extracted:
            rid = r.get("id")
            if not isinstance(rid, (int, float)):
                continue
            rid = int(rid)
            # Later source overrides earlier if same id
            if rid not in all_records:
                all_records[rid] = r
            else:
                # Merge — later file wins for non-empty fields
                existing = all_records[rid]
                for k, v in r.items():
                    if v and v != "" and k != "id":
                        existing[k] = v

    normalised = [_normalise_record(r) for r in all_records.values()]
    normalised.sort(key=lambda r: r.get("id", 0))
    return normalised


def main():
    parser = argparse.ArgumentParser(description="Ingest Strategist records")
    parser.add_argument("--mongo-url", default="")
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument("--dry-run", action="store_true", default=False)
    args = parser.parse_args()

    records = load_records()
    print(f"[INFO] Total unique records loaded: {len(records)}")

    validation = validate_batch(records)
    print(f"[INFO] Gate 0 validation: {validation['total']} records, {validation['errors']} errors")
    if validation["errors"]:
        for e in validation["detail"][:20]:
            print(f"  [WARN] ID {e['id']}: missing {e['missing']}")

    if args.dry_run:
        print("[DRY-RUN] Sample record:")
        if records:
            print(json.dumps(records[0], indent=2, default=str))
        print(f"[DRY-RUN] Would upsert {len(records)} records into knowledge_rules")
        return

    if not args.mongo_url:
        print("[ERROR] --mongo-url required for upload", file=sys.stderr)
        sys.exit(1)

    from pymongo import MongoClient
    from pymongo import UpdateOne

    client = MongoClient(args.mongo_url)
    db = client[args.db_name]
    coll = db.knowledge_rules

    ops = [
        UpdateOne(
            {"id": r["id"], "science_id": SCIENCE_ID},
            {"$set": r},
            upsert=True,
        )
        for r in records
    ]

    if ops:
        result = coll.bulk_write(ops, ordered=False)
        print(f"[OK] Upserted {result.upserted_count} new, modified {result.modified_count} existing records")
    else:
        print("[WARN] No records to upsert")

    client.close()


if __name__ == "__main__":
    main()
