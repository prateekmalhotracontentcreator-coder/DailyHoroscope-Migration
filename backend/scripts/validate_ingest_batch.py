#!/usr/bin/env python3
"""
validate_ingest_batch.py
--------------------------------------------------------------------
Post-ingest structural validation for a specific batch_id.
Checks that all rules were inserted with the correct fields.

Usage:
    python3 backend/scripts/validate_ingest_batch.py \
      --batch-id medical_astrology_v1 \
      --mongo-url "$MONGO_URL" --db-name horoscope_db

Note: This script checks structural correctness only (rule_id, approval_status,
source_book, source.batch_id). For AI quality validation, use validate_rules.py.
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from pymongo import MongoClient

# ---------------------------------------------------------------------------
LOG_DIR = "KE_TEXTBOOK_DECODE/Dedup_Reports"

_buf: list[str] = []


def out(msg: str = "") -> None:
    print(msg)
    _buf.append(msg)


def _write_log(log_path: str) -> None:
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    Path(log_path).write_text("\n".join(_buf) + "\n", encoding="utf-8")
    print(f"\nLog saved: {log_path}")

# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Post-ingest structural batch validator.")
    parser.add_argument("--batch-id",  required=True, help="Batch ID to validate")
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    parser.add_argument("--db-name",   default="horoscope_db")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = f"{LOG_DIR}/validate_ingest_{args.batch_id}_{ts}.log"

    out("=" * 75)
    out(f"  LOG FILE : {log_path}")
    out("=" * 75)
    out()
    out(f"POST-INGEST STRUCTURAL VALIDATION")
    out(f"Batch    : {args.batch_id}")
    out(f"Database : {args.db_name}")
    out()

    if not args.mongo_url:
        out("ERROR: --mongo-url not provided and MONGO_URL env var not set.")
        _write_log(log_path)
        sys.exit(1)

    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10000)
    db     = client[args.db_name]
    batch_id = args.batch_id

    # ── import_batches record ────────────────────────────────────────────────
    batch_record = db["import_batches"].find_one({"batch_id": batch_id})
    if not batch_record:
        out(f"❌ ERROR: batch '{batch_id}' not found in import_batches collection")
        _write_log(log_path)
        sys.exit(1)

    out("import_batches record:")
    for k, v in batch_record.items():
        if k != "_id":
            out(f"  {k}: {v}")
    out()

    # ── fetch rules ──────────────────────────────────────────────────────────
    rules = list(db["interpretation_rules"].find(
        {"ingest_batch_id": batch_id}, {"_id": 0}
    ))
    out(f"Rules found in DB (ingest_batch_id={batch_id}): {len(rules)}")

    if not rules:
        out("⚠  No rules found by ingest_batch_id -- trying source.batch_id...")
        rules = list(db["interpretation_rules"].find(
            {"source.batch_id": batch_id}, {"_id": 0}
        ))
        out(f"Rules found (source.batch_id={batch_id}): {len(rules)}")
        if rules:
            out("Using source.batch_id match for validation.")

    if not rules:
        out("❌ No rules found for this batch. Ingest may have failed.")
        _write_log(log_path)
        sys.exit(1)

    # ── structural checks ────────────────────────────────────────────────────
    missing_rule_id       = [r for r in rules if not r.get("rule_id")]
    wrong_status          = [r for r in rules if r.get("approval_status") not in
                             ("pending_review", "auto_approved", "pending_human_review",
                              "flagged", "rejected", "approved")]
    missing_book          = [r for r in rules if not r.get("source_book")]
    missing_interp        = [r for r in rules if not (
                                 (r.get("interpretation") or {}).get("detailed") or
                                 (r.get("interpretation") or {}).get("summary") or
                                 r.get("full_text")
                             )]
    source_batch_ok       = [r for r in rules if (r.get("source") or {}).get("batch_id") == batch_id]
    source_batch_missing  = len(rules) - len(source_batch_ok)

    # ── approval status breakdown ────────────────────────────────────────────
    status_counts: dict[str, int] = {}
    for r in rules:
        s = r.get("approval_status", "UNKNOWN")
        status_counts[s] = status_counts.get(s, 0) + 1

    out()
    out("─" * 60)
    out(f"  Total rules in DB        : {len(rules)}")
    out(f"  Reported inserted        : {batch_record.get('rules_inserted', '?')}")
    dup_skipped  = batch_record.get("duplicates_skipped")
    dup_display  = dup_skipped if dup_skipped is not None else "N/A (upsert mode)"
    out(f"  Duplicates skipped       : {dup_display}")
    out()
    out("  Approval status breakdown:")
    for status, count in sorted(status_counts.items()):
        out(f"    {status}: {count}")

    out()
    out("  Structural checks:")
    out(f"    Missing rule_id         : {len(missing_rule_id)}")
    out(f"    Invalid approval_status : {len(wrong_status)}")
    out(f"    Missing source_book     : {len(missing_book)}")
    out(f"    Missing interpretation  : {len(missing_interp)}")
    out(f"    source.batch_id missing : {source_batch_missing}")

    all_clean = (
        len(missing_rule_id)  == 0 and
        len(wrong_status)     == 0 and
        len(missing_book)     == 0 and
        source_batch_missing  == 0
    )

    out()
    out("─" * 60)
    if all_clean:
        out("✅ STRUCTURAL CHECK: CLEAN")
        out()
        out("NEXT STEP -- AI quality validation (if not already run pre-upload):")
        out(f'  python3 backend/scripts/validate_rules.py \\')
        out(f'    --batch-id {batch_id} \\')
        out(f'    --mongo-url "$MONGO_URL" --db-name {args.db_name}')
    else:
        out("❌ STRUCTURAL CHECK: ISSUES FOUND")
        if missing_rule_id:
            out(f"  → {len(missing_rule_id)} rules missing rule_id")
        if wrong_status:
            out(f"  → {len(wrong_status)} rules with invalid approval_status: "
                f"{[r.get('rule_id') for r in wrong_status[:5]]}")
        if missing_book:
            out(f"  → {len(missing_book)} rules missing source_book")
        if source_batch_missing:
            out(f"  → {source_batch_missing} rules missing source.batch_id")

    client.close()
    _write_log(log_path)

    if not all_clean:
        sys.exit(1)


if __name__ == "__main__":
    main()
