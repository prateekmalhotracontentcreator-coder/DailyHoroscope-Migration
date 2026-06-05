#!/usr/bin/env python3
"""Export Lal Kitab rules from MongoDB to /tmp/lalkitab_rules_for_dedup/
for use by retroactive_dedup_lalkitab.sh.

Usage (from repo root):
    python3 backend/scripts/export_lalkitab_for_dedup.py --mongo-url "$MONGO_URL"

Retries up to 3 times on connection failure with 10s wait between attempts.
Tee-logging: LOG FILE is printed as first line; log saved to
KE_TEXTBOOK_DECODE/Dedup_Reports/ with try/finally guarantee.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR  = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")
TS       = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
LOG_PATH = LOG_DIR / f"export_lalkitab_for_dedup_{TS}.log"

_buf: list[str] = []

def out(msg: str = "") -> None:
    print(msg); _buf.append(msg)

def _write_log(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(_buf) + "\n", encoding="utf-8")
    print(f"Log saved: {p}")


LK_BATCH   = "lalkitab_all_v2_20260605"
OUT_DIR    = Path("/tmp/lalkitab_rules_for_dedup")
MAX_TRIES  = 3
RETRY_WAIT = 10  # seconds


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    parser.add_argument("--db-name", default="horoscope_db")
    return parser.parse_args()


def export_rules(mongo_url: str, db_name: str) -> int:
    from pymongo import MongoClient, ReadPreference
    # SECONDARY_PREFERRED: read from any available replica (primary or secondary).
    # This bypasses the Atlas primary-shard SSL timeout seen repeatedly -- shard-01
    # secondary stays reachable even when shards 00 and 02 have SSL failures.
    client = MongoClient(
        mongo_url,
        serverSelectionTimeoutMS=30000,
        read_preference=ReadPreference.SECONDARY_PREFERRED,
    )
    db = client[db_name]

    query = {"ingest_batch_id": LK_BATCH}
    rules = list(db["interpretation_rules"].find(query, {"_id": 0}))
    client.close()

    if not rules:
        raise RuntimeError(
            f"0 rules fetched for batch '{LK_BATCH}'. "
            "Check MONGO_URL and that patch_lalkitab_schema.py ran successfully."
        )

    mapped = []
    for r in rules:
        interp    = r.get("interpretation") or {}
        full_text = (
            r.get("full_text")
            or interp.get("detailed")
            or interp.get("full_text")
            or ""
        )
        raw_cond = r.get("condition")
        if isinstance(raw_cond, dict):
            cond = raw_cond
        elif isinstance(raw_cond, str):
            cond = {"type": raw_cond}
        else:
            cond = {}

        mapped.append({
            "rule_id":         r.get("rule_id", ""),
            "condition":       cond,
            "full_text":       full_text,
            "claim_polarity":  r.get("claim_polarity") or r.get("polarity") or "neutral",
            "source_book":     r.get("source_book", ""),
            "ingest_batch_id": r.get("ingest_batch_id"),
        })

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
        out(f"Cleared stale export dir: {OUT_DIR}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    out_file = OUT_DIR / "LalKitab_Ch19_29_Rules.json"
    out_file.write_text(json.dumps(mapped, ensure_ascii=False, indent=2), encoding="utf-8")
    out(f"Saved {len(mapped)} rules → {out_file}")
    return len(mapped)


def main() -> None:
    out(f"LOG FILE: {LOG_PATH}")
    out("=" * 60)
    out(f"Lal Kitab MongoDB Export for Dedup")
    out(f"Batch:   {LK_BATCH}")
    out(f"Output:  {OUT_DIR}")
    out(f"Run:     {TS}")
    out("=" * 60)
    out()

    args = parse_args()
    if not args.mongo_url:
        out("ERROR: --mongo-url not provided and MONGO_URL env var not set.")
        sys.exit(1)

    for attempt in range(1, MAX_TRIES + 1):
        out(f"Attempt {attempt}/{MAX_TRIES} ...")
        try:
            count = export_rules(args.mongo_url, args.db_name)
            out()
            out(f"✅  Export complete: {count} LK rules → {OUT_DIR}/LalKitab_Ch19_29_Rules.json")
            out()
            out("Next step -- run the dedup:")
            out("  bash backend/scripts/retroactive_dedup_lalkitab.sh")
            return
        except Exception as e:
            out(f"ATTEMPT {attempt} FAILED: {e}")
            if attempt < MAX_TRIES:
                out(f"Retrying in {RETRY_WAIT}s ...")
                time.sleep(RETRY_WAIT)
            else:
                out()
                out(f"FATAL: All {MAX_TRIES} attempts failed. Check Atlas connectivity and retry.")
                sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    finally:
        _write_log(LOG_PATH)
