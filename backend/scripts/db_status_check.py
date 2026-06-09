#!/usr/bin/env python3
"""
db_status_check.py
------------------
Connects to horoscope_db and prints a full breakdown of interpretation_rules
by approval_status, science_id, and source book.

Every run saves a timestamped log file to backend/scripts/logs/ for audit.

Usage:
    python3 backend/scripts/db_status_check.py
"""

from __future__ import annotations
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from pymongo import MongoClient

# ---------------------------------------------------------------------------
# Log file setup
# ---------------------------------------------------------------------------
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
log_path = LOG_DIR / f"db_status_check_{timestamp}.log"

class Tee:
    """Writes every print() call to both stdout and the log file."""
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
print(f"  db_status_check.py")
print(f"  Run timestamp : {timestamp} UTC")
print(f"  Log file      : {log_path}")
print(f"╚══════════════════════════════════════════════════════════════╝")
print()

# ---------------------------------------------------------------------------
# Connect
# ---------------------------------------------------------------------------
MONGO_URL = os.environ.get("MONGO_URL")
if not MONGO_URL:
    print("ERROR: MONGO_URL environment variable is not set.")
    sys.exit(1)

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=10_000)
    dbs = client.list_database_names()
    print(f"✅ Connected to MongoDB")
    print(f"   Databases visible: {dbs}")
    print()
except Exception as e:
    print(f"❌ Connection failed: {e}")
    sys.exit(1)

if "horoscope_db" not in dbs:
    print("❌ horoscope_db not found in database list. Aborting.")
    sys.exit(1)

if "EverydayHoroscope" in dbs:
    print("⚠️  EverydayHoroscope DB visible -- RETIRED. Do not use.")
    print()

col = client["horoscope_db"]["interpretation_rules"]
total = col.count_documents({})
print(f"horoscope_db.interpretation_rules  →  {total:,} total documents")
print()

# ---------------------------------------------------------------------------
# Breakdown by approval_status
# ---------------------------------------------------------------------------
STATUSES = [
    "approved",
    "auto_approved",
    "pending_human_review",
    "pending_review",
    "flagged",
    "deprecated",
    "contradiction_hold",
]
print("─" * 50)
print("  By approval_status")
print("─" * 50)
status_total = 0
for s in STATUSES:
    n = col.count_documents({"approval_status": s})
    if n:
        print(f"  {s:<28} {n:>6,}")
        status_total += n
# catch any statuses not in the list above
other = total - status_total
if other:
    print(f"  {'(other / missing)':<28} {other:>6,}")
print(f"  {'TOTAL':<28} {total:>6,}")
print()

# ---------------------------------------------------------------------------
# Breakdown by science_id
# ---------------------------------------------------------------------------
print("─" * 50)
print("  By science_id")
print("─" * 50)
for s in sorted(col.distinct("science_id")):
    n = col.count_documents({"science_id": s})
    print(f"  {str(s):<28} {n:>6,}")
print()

# ---------------------------------------------------------------------------
# Breakdown by source book (top 20)
# ---------------------------------------------------------------------------
print("─" * 50)
print("  By source book (top 20)")
print("─" * 50)
books: list[str] = []
for r in col.find({}, {"source.book": 1, "source_chapter": 1, "_id": 0}):
    book = (r.get("source") or {}).get("book") or r.get("source_chapter") or "(none)"
    books.append(book)

for book, count in Counter(books).most_common(20):
    print(f"  {str(book)[:40]:<42} {count:>6,}")
print()

# ---------------------------------------------------------------------------
# Active (non-deprecated) summary
# ---------------------------------------------------------------------------
active = col.count_documents({"approval_status": {"$ne": "deprecated"}})
approved = col.count_documents({"approval_status": "approved"})
print("─" * 50)
print("  Summary")
print("─" * 50)
print(f"  Active (non-deprecated)          {active:>6,}")
print(f"  Approved (live to users)         {approved:>6,}")
print(f"  Deprecated                       {total - active:>6,}")
print()

client.close()

print(f"╔══════════════════════════════════════════════════════════════╗")
print(f"  ✅ Check complete")
print(f"  Log saved → {log_path}")
print(f"╚══════════════════════════════════════════════════════════════╝")

sys.stdout = sys.__stdout__
tee.close()
