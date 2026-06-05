#!/usr/bin/env python3
"""BPHS Vol 2 Ch.46 Status Check.

Queries horoscope_db for any rules that might be Ch.46 content:
  1. Batch IDs containing 'ch46'
  2. source.chapter == 46 in BPHS Vol 2 batches
  3. Any import_batches record for a Vol 2 Ch.46 batch

Run from repo root:
  python3 backend/scripts/check_bphs_ch46.py --mongo-url "$MONGO_URL"

Tee-logs to KE_TEXTBOOK_DECODE/Dedup_Reports/
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

_buf: list[str] = []


def out(msg: str = "") -> None:
    print(msg)
    _buf.append(msg)


def _write_log(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("\n".join(_buf), encoding="utf-8")
    print(f"Log saved: {log_path}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Check BPHS Vol 2 Ch.46 status in MongoDB.")
    p.add_argument("--mongo-url", required=True, help="MongoDB connection URL")
    p.add_argument("--db-name", default="horoscope_db")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    log_path = Path(f"KE_TEXTBOOK_DECODE/Dedup_Reports/check_bphs_ch46_{ts}.log")

    out("=" * 75)
    out(f"  LOG FILE : {log_path}")
    out("=" * 75)
    out()
    out("BPHS VOL 2 CH.46 STATUS CHECK")
    out(f"Database : {args.db_name}")
    out(f"Timestamp: {ts}")
    out()

    try:
        import motor.motor_asyncio as _motor_check  # noqa: F401
    except ImportError:
        pass

    try:
        from pymongo import MongoClient
    except ImportError:
        out("ERROR: pymongo not installed. Run: pip install pymongo")
        _write_log(log_path)
        sys.exit(1)

    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=5000)
    db = client[args.db_name]

    try:
        client.admin.command("ping")
        out("✅ MongoDB connection OK")
    except Exception as exc:
        out(f"❌ MongoDB connection FAILED: {exc}")
        _write_log(log_path)
        sys.exit(1)

    out()

    # ──────────────────────────────────────────────────────────────────────────
    # 1. Check import_batches for any Ch.46-related batch
    # ──────────────────────────────────────────────────────────────────────────
    out("─" * 60)
    out("1. IMPORT_BATCHES -- searching for 'ch46' / chapter 46 records")
    out("─" * 60)

    import_batches = db["import_batches"]

    # Search for any batch with ch46 in batch_id
    ch46_batches = list(import_batches.find(
        {"batch_id": {"$regex": "ch46", "$options": "i"}},
        {"_id": 0}
    ))
    out(f"  Batch IDs containing 'ch46': {len(ch46_batches)}")
    if ch46_batches:
        for b in ch46_batches:
            out(f"    batch_id  : {b.get('batch_id')}")
            out(f"    book      : {b.get('book')}")
            out(f"    chapter   : {b.get('chapter')}")
            out(f"    total_rules: {b.get('total_rules')}")
            out(f"    uploaded_at: {b.get('uploaded_at')}")
            out()
    else:
        out("    → None found")

    # Search for batches with chapter: 46 in BPHS Vol 2
    ch46_by_chapter = list(import_batches.find(
        {"chapter": 46},
        {"_id": 0}
    ))
    out()
    out(f"  Batches with chapter == 46: {len(ch46_by_chapter)}")
    if ch46_by_chapter:
        for b in ch46_by_chapter:
            out(f"    batch_id: {b.get('batch_id')}")
            out(f"    book    : {b.get('book')}")
    else:
        out("    → None found")

    out()

    # ──────────────────────────────────────────────────────────────────────────
    # 2. Check interpretation_rules for Ch.46 content
    # ──────────────────────────────────────────────────────────────────────────
    out("─" * 60)
    out("2. INTERPRETATION_RULES -- searching for Ch.46 content")
    out("─" * 60)

    rules = db["interpretation_rules"]

    # By rule_id prefix
    ch46_by_rule_id = rules.count_documents(
        {"rule_id": {"$regex": "bphs.*ch.*46", "$options": "i"}}
    )
    out(f"  Rules with rule_id matching 'bphs*ch*46': {ch46_by_rule_id}")

    # By ingest_batch_id
    ch46_by_batch = rules.count_documents(
        {"ingest_batch_id": {"$regex": "ch46", "$options": "i"}}
    )
    out(f"  Rules with ingest_batch_id containing 'ch46': {ch46_by_batch}")

    # By source chapter
    ch46_by_source_ch = rules.count_documents({
        "source_book": {"$regex": "bphs", "$options": "i"},
        "source.chapter": 46
    })
    out(f"  Rules with source_book=BPHS and source.chapter==46: {ch46_by_source_ch}")

    # Sample any matches
    total_ch46 = max(ch46_by_rule_id, ch46_by_batch, ch46_by_source_ch)
    if total_ch46 > 0:
        out()
        out("  Sample rules found:")
        sample = list(rules.find(
            {"rule_id": {"$regex": "bphs.*ch.*46", "$options": "i"}},
            {"rule_id": 1, "ingest_batch_id": 1, "approval_status": 1, "source_book": 1, "_id": 0}
        ).limit(5))
        for r in sample:
            out(f"    rule_id={r.get('rule_id')}  batch={r.get('ingest_batch_id')}  status={r.get('approval_status')}")
    else:
        out()
        out("  → No Ch.46 rules found in interpretation_rules")

    out()

    # ──────────────────────────────────────────────────────────────────────────
    # 3. Summary of all BPHS Vol 2 batches in MongoDB
    # ──────────────────────────────────────────────────────────────────────────
    out("─" * 60)
    out("3. ALL BPHS VOL 2 BATCHES IN MONGODB")
    out("─" * 60)

    vol2_batches = list(import_batches.find(
        {"$or": [
            {"batch_id": {"$regex": "bphs.*ch4[0-9]|bphs.*ch5[0-9]", "$options": "i"}},
            {"book": {"$regex": "bphs vol 2", "$options": "i"}},
        ]},
        {"_id": 0, "batch_id": 1, "chapter": 1, "book": 1, "total_rules": 1, "uploaded_at": 1}
    ).sort("batch_id", 1))

    if vol2_batches:
        out(f"  Found {len(vol2_batches)} BPHS Vol 2 batch(es):")
        for b in vol2_batches:
            out(f"    Ch{str(b.get('chapter', '?')):>2}  {b.get('batch_id', '?'):<45}  {b.get('total_rules', '?')} rules")
    else:
        out("  No BPHS Vol 2 batches found via book field -- trying batch_id pattern search...")
        bphs2_batches = list(import_batches.find(
            {"batch_id": {"$regex": "bphs", "$options": "i"}},
            {"_id": 0, "batch_id": 1, "chapter": 1, "book": 1, "total_rules": 1}
        ).sort("batch_id", 1))
        out(f"  All BPHS-related batches ({len(bphs2_batches)}):")
        for b in bphs2_batches:
            out(f"    {b.get('batch_id', '?'):<50}  rules={b.get('total_rules', '?')}")

    out()

    # ──────────────────────────────────────────────────────────────────────────
    # Verdict
    # ──────────────────────────────────────────────────────────────────────────
    out("─" * 60)
    out("VERDICT")
    out("─" * 60)
    if total_ch46 == 0 and not ch46_batches and not ch46_by_chapter:
        out("  ✅ Ch.46 NOT FOUND in horoscope_db.")
        out("  → No decode or ingest has occurred for BPHS Vol 2 Ch.46.")
        out("  → Next step: determine scope of Ch.46 (check PDF) and decide whether")
        out("    to issue a Codex decode sprint or defer.")
    else:
        out("  ⚠️  Ch.46 content DETECTED in horoscope_db.")
        out("  → Review batch details above and confirm triage status.")

    out()
    out("=" * 75)

    client.close()
    _write_log(log_path)


if __name__ == "__main__":
    main()
