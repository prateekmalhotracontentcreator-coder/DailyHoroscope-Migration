#!/usr/bin/env python3
"""
audit_remedies_flagged.py
--------------------------
Reads all flagged rules from the Remedies batches and prints a breakdown
of flag reasons to determine whether they are genuine content errors or
validator style-mismatch (remedy prescription format vs classical text).

Every run saves a timestamped log.

Usage:
    python3 backend/scripts/audit_remedies_flagged.py
"""

from __future__ import annotations
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from pymongo import MongoClient

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
log_path = LOG_DIR / f"audit_remedies_flagged_{ts}.log"

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
print(f"  audit_remedies_flagged.py")
print(f"  Run timestamp : {ts} UTC")
print(f"  Log file      : {log_path}")
print(f"╚══════════════════════════════════════════════════════════════╝")
print()

MONGO_URL = os.environ.get("MONGO_URL")
if not MONGO_URL:
    print("ERROR: MONGO_URL not set."); sys.exit(1)

client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=10_000)
col = client["horoscope_db"]["interpretation_rules"]

REMEDY_BATCHES = {
    "remedies-crystals-v1-20260510":  "Crystals",
    "remedies-gemstones-v1-20260510": "Gemstones",
    "remedies-chakra-v1-20260510":    "Chakra",
    "remedies-dhana-v1-20260510":     "Dhana",
}

for batch_id, label in REMEDY_BATCHES.items():
    flagged = list(col.find(
        {"source.batch_id": batch_id, "approval_status": "flagged"},
        {"rule_id": 1, "validation": 1, "interpretation": 1,
         "condition": 1, "source": 1, "_id": 0}
    ))
    total = col.count_documents({"source.batch_id": batch_id})

    print(f"{'═'*60}")
    print(f"  {label} ({batch_id})")
    print(f"  Flagged: {len(flagged)} / {total}")
    print(f"{'═'*60}")

    if not flagged:
        print("  (none flagged)")
        print()
        continue

    # Tally flag_reasons
    reason_counter: Counter = Counter()
    for r in flagged:
        val = r.get("validation") or {}
        reason = val.get("flag_reason") or val.get("reason") or "(no reason)"
        reason_counter[reason] += 1

    print(f"  Flag reason breakdown:")
    for reason, count in reason_counter.most_common():
        print(f"    {count:>3}x  {reason[:90]}")
    print()

    # Show 3 sample flagged rules
    print(f"  Sample flagged rules (first 3):")
    for r in flagged[:3]:
        rid = r.get("rule_id", "?")
        val = r.get("validation") or {}
        reason = val.get("flag_reason") or val.get("reason") or "(no reason)"
        interp = r.get("interpretation") or {}
        summary = (interp.get("summary") or "")[:80]
        detailed = (interp.get("detailed") or "")[:120]
        cond_type = (r.get("condition") or {}).get("type", "?")
        print(f"    rule_id  : {rid}")
        print(f"    cond_type: {cond_type}")
        print(f"    reason   : {reason[:100]}")
        print(f"    summary  : {summary}")
        print(f"    detailed : {detailed}")
        print()

client.close()

print(f"╔══════════════════════════════════════════════════════════════╗")
print(f"  ✅ Audit complete")
print(f"  Log saved → {log_path}")
print(f"╚══════════════════════════════════════════════════════════════╝")

sys.stdout = sys.__stdout__
tee.close()
