#!/usr/bin/env python3
"""
investigate_old_batches.py
--------------------------
Investigates the old April 2026 batches (lal-kitab_XXX_20260413,
a-text-book-of-astro_XXX_20260413, longevity-and-astro_XXX_20260413,
a-book-of-300-import_XXX_20260413, longevity-and-un-nat_XXX_20260413)
that are sitting at approval_status = 'pending_review'.

Checks whether these are superseded by the properly-named later ingests
and whether their science_id matches expectations for each book.

Every run saves a timestamped log file to backend/scripts/logs/ for audit.

Usage:
    python3 backend/scripts/investigate_old_batches.py
"""

from __future__ import annotations
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from pymongo import MongoClient

# ---------------------------------------------------------------------------
# Log file setup
# ---------------------------------------------------------------------------
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
log_path = LOG_DIR / f"investigate_old_batches_{timestamp}.log"

class Tee:
    def __init__(self, filepath: Path):
        self._file = open(filepath, "w", encoding="utf-8")
    def write(self, data: str):
        sys.__stdout__.write(data)
        self._file.write(data)
    def flush(self):
        sys.__stdout__.flush()
        self._file.flush()
    def close(self):
        self._file.close()

tee = Tee(log_path)
sys.stdout = tee

print(f"╔══════════════════════════════════════════════════════════════╗")
print(f"  investigate_old_batches.py")
print(f"  Run timestamp : {timestamp} UTC")
print(f"  Log file      : {log_path}")
print(f"╚══════════════════════════════════════════════════════════════╝")
print()

# ---------------------------------------------------------------------------
# Connect
# ---------------------------------------------------------------------------
MONGO_URL = os.environ.get("MONGO_URL")
if not MONGO_URL:
    print("ERROR: MONGO_URL not set.")
    sys.exit(1)

client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=10_000)
col = client["horoscope_db"]["interpretation_rules"]

# ---------------------------------------------------------------------------
# Old batch prefixes to investigate
# ---------------------------------------------------------------------------
OLD_PREFIXES = [
    "lal-kitab_",
    "a-text-book-of-astro_",
    "longevity-and-astro_",
    "a-book-of-300-import_",
    "longevity-and-un-nat_",
]

# Expected science_id and known current batch patterns for each book
EXPECTED = {
    "lal-kitab_": {
        "correct_science_id": "jyotish",
        "current_batch_pattern": "lalkitab-ch",
        "book_label": "Lal Kitab",
    },
    "a-text-book-of-astro_": {
        "correct_science_id": "vedic_astrology",
        "current_batch_pattern": "tba-ch",
        "book_label": "A Text-Book of Astrology",
    },
    "longevity-and-astro_": {
        "correct_science_id": "kp_jyotish",
        "current_batch_pattern": "longevity_58ch",
        "book_label": "Longevity & Astro System (58Ch)",
    },
    "a-book-of-300-import_": {
        "correct_science_id": "jyotish",
        "current_batch_pattern": "300-combinations-v1",
        "book_label": "300 Important Combinations",
    },
    "longevity-and-un-nat_": {
        "correct_science_id": "kp_jyotish",
        "current_batch_pattern": "longevity_unnatural_v1",
        "book_label": "Longevity Unnatural Deaths",
    },
}

# ---------------------------------------------------------------------------
# For each old batch prefix: count old vs current rules
# ---------------------------------------------------------------------------
for prefix, meta in EXPECTED.items():
    book = meta["book_label"]
    correct_sid = meta["correct_science_id"]
    current_pat = meta["current_batch_pattern"]

    print(f"{'═'*60}")
    print(f"  {book}")
    print(f"{'═'*60}")

    # Old batch rules (pending_review)
    old_count = col.count_documents({
        "approval_status": "pending_review",
        "batch_id": {"$regex": f"^{prefix}"}
    })

    # Science IDs used in old batches
    old_sids = col.distinct("science_id", {
        "approval_status": "pending_review",
        "batch_id": {"$regex": f"^{prefix}"}
    })

    # Sample rule_ids and summaries from old batches
    samples = list(col.find(
        {"approval_status": "pending_review", "batch_id": {"$regex": f"^{prefix}"}},
        {"rule_id": 1, "batch_id": 1, "science_id": 1,
         "interpretation.summary": 1, "interpretation.detailed": 1, "_id": 0}
    ).limit(3))

    # Current (properly-ingested) rules for the same book
    current_count = col.count_documents({
        "batch_id": {"$regex": f"^{current_pat}"}
    })
    current_statuses = {}
    for s in ["approved", "auto_approved", "pending_human_review", "flagged", "deprecated"]:
        n = col.count_documents({
            "batch_id": {"$regex": f"^{current_pat}"},
            "approval_status": s
        })
        if n:
            current_statuses[s] = n

    print(f"  Old pending_review rules  : {old_count}")
    print(f"  Old science_id(s) used    : {old_sids}")
    print(f"  Correct science_id        : {correct_sid}")
    sid_ok = set(old_sids) == {correct_sid}
    print(f"  science_id match          : {'✅ CORRECT' if sid_ok else '❌ WRONG -- old batches used wrong science_id'}")
    print()
    print(f"  Current ingest (pattern '{current_pat}*'):")
    print(f"    Total rules             : {current_count}")
    for s, n in current_statuses.items():
        print(f"    {s:<28}: {n}")
    print()

    if current_count > 0:
        print(f"  ⚠️  VERDICT: Current ingest EXISTS ({current_count} rules).")
        if not sid_ok:
            print(f"     Old batches used WRONG science_id ({old_sids}).")
        print(f"     Old batches are almost certainly SUPERSEDED.")
        print(f"     Recommendation: DEPRECATE old {old_count} rules, do NOT validate.")
    else:
        print(f"  ℹ️  VERDICT: No current ingest found. Old batches may be the only version.")
        print(f"     Recommendation: Validate old batches (fix science_id first if wrong).")

    print()
    print(f"  Sample rules from old batches:")
    for r in samples:
        rid = r.get("rule_id", "?")
        bid = r.get("batch_id", "?")
        sid = r.get("science_id", "?")
        interp = r.get("interpretation") or {}
        text = (interp.get("summary") or interp.get("detailed") or "")[:80]
        print(f"    rule_id   : {rid}")
        print(f"    batch_id  : {bid}")
        print(f"    science_id: {sid}")
        print(f"    text      : {text}...")
        print()

print(f"{'═'*60}")
print()

# ---------------------------------------------------------------------------
# Summary recommendation
# ---------------------------------------------------------------------------
total_old = col.count_documents({
    "approval_status": "pending_review",
    "batch_id": {"$regex": "_(0[0-9][0-9]|[0-9]+)_20260413$"}
})
print(f"Total old _20260413 pending_review rules : {total_old}")
print()
print("Next steps:")
print("  1. Review the VERDICT for each book above.")
print("  2. If SUPERSEDED: run deprecate_old_batches.py (to be written)")
print("  3. If NOT superseded: fix science_id then validate.")
print()

client.close()

print(f"╔══════════════════════════════════════════════════════════════╗")
print(f"  ✅ Investigation complete")
print(f"  Log saved → {log_path}")
print(f"╚══════════════════════════════════════════════════════════════╝")

sys.stdout = sys.__stdout__
tee.close()
