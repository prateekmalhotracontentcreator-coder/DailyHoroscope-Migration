#!/usr/bin/env python3
"""
pending_review_audit.py
-----------------------
Identifies all rules still sitting at approval_status = 'pending_review'.
These are uploaded rules that have NOT yet been through the AI validator.

Every run saves a timestamped log file to backend/scripts/logs/ for audit.

Usage:
    python3 backend/scripts/pending_review_audit.py
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
log_path = LOG_DIR / f"pending_review_audit_{timestamp}.log"

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
print(f"  pending_review_audit.py")
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

total_pr = col.count_documents({"approval_status": "pending_review"})
print(f"Total pending_review rules: {total_pr:,}")
print()

if total_pr == 0:
    print("✅ Nothing to validate -- all rules have left pending_review.")
    sys.exit(0)

# ---------------------------------------------------------------------------
# Group by batch_id
# ---------------------------------------------------------------------------
batch_counts: dict[str, int] = defaultdict(int)
batch_sources: dict[str, set] = defaultdict(set)

cursor = col.find(
    {"approval_status": "pending_review"},
    {"batch_id": 1, "source": 1, "science_id": 1, "_id": 0}
)
for r in cursor:
    batch_id = r.get("batch_id") or (r.get("source") or {}).get("batch_id") or "(no batch_id)"
    science_id = r.get("science_id") or "?"
    batch_counts[batch_id] += 1
    batch_sources[batch_id].add(science_id)

print("─" * 70)
print(f"  {'batch_id':<45} {'count':>6}  science_id")
print("─" * 70)
for batch_id, count in sorted(batch_counts.items(), key=lambda x: -x[1]):
    sciences = ", ".join(sorted(batch_sources[batch_id]))
    print(f"  {str(batch_id):<45} {count:>6}  {sciences}")
print("─" * 70)
print(f"  {'TOTAL':<45} {total_pr:>6}")
print()

# ---------------------------------------------------------------------------
# Validator command hints
# ---------------------------------------------------------------------------
print("─" * 70)
print("  Suggested validate_rules.py commands (run in order):")
print("─" * 70)
for batch_id, count in sorted(batch_counts.items(), key=lambda x: -x[1]):
    if batch_id == "(no batch_id)":
        print(f"  # ⚠️  {count} rules have no batch_id -- cannot validate by batch. Investigate separately.")
    else:
        print(f"  python3 backend/scripts/validate_rules.py \\")
        print(f"    --batch-id \"{batch_id}\" \\")
        print(f"    --mongo-url \"$MONGO_URL\" \\")
        print(f"    --db-name horoscope_db")
        print()

client.close()

print(f"╔══════════════════════════════════════════════════════════════╗")
print(f"  ✅ Audit complete")
print(f"  Log saved → {log_path}")
print(f"╚══════════════════════════════════════════════════════════════╝")

sys.stdout = sys.__stdout__
tee.close()
