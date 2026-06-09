#!/usr/bin/env python3
"""
promote_sbc_to_auto_approved.py
--------------------------------
Bulk-promotes all SBC (Sarvato Bhadra Chakra) rules from pending_human_review
→ auto_approved.

No AI validation needed: SBC rules are textbook-decoded classical knowledge
with structural validation already passed (0 issues on ingest). The condition
arrays are intentionally empty -- SBC uses engine_specification conditions, not
natal chart planet/house arrays.

Usage:
  python3 backend/scripts/promote_sbc_to_auto_approved.py --dry-run
  python3 backend/scripts/promote_sbc_to_auto_approved.py
"""

from __future__ import annotations
import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from pymongo import MongoClient

parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
ts       = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
mode_tag = "dry-run" if args.dry_run else "live"
log_path = LOG_DIR / f"promote_sbc_{mode_tag}_{ts}.log"

class Tee:
    def __init__(self, fp: Path):
        self._f = open(fp, "w", encoding="utf-8")
    def write(self, d: str):
        sys.__stdout__.write(d); self._f.write(d)
    def flush(self):
        sys.__stdout__.flush(); self._f.flush()
    def close(self):
        self._f.close()

tee = Tee(log_path)
sys.stdout = tee

MONGO_URL = os.environ.get("MONGO_URL")
if not MONGO_URL:
    print("ERROR: MONGO_URL not set."); sys.exit(1)

mongo = MongoClient(MONGO_URL, serverSelectionTimeoutMS=10_000)
col   = mongo["horoscope_db"]["interpretation_rules"]

BATCH_ID = "sbc_v1_20260605"
NOW      = datetime.now(timezone.utc).isoformat()

print("╔══════════════════════════════════════════════════════════════╗")
print(f"  promote_sbc_to_auto_approved.py  [{mode_tag.upper()}]")
print(f"  Batch : {BATCH_ID}")
print(f"  Run   : {ts} UTC")
print(f"  Log   : {log_path}")
print("╚══════════════════════════════════════════════════════════════╝")
print()

query = {
    "source.batch_id": BATCH_ID,
    "approval_status": {"$in": ["pending_human_review", "pending_review", "flagged"]},
}

count = col.count_documents(query)
print(f"  Rules to promote : {count}")
print()

if count == 0:
    print("✅ Nothing to do.")
    mongo.close()
    sys.stdout = sys.__stdout__; tee.close(); sys.exit(0)

# Per-chapter breakdown
pipeline = [
    {"$match": query},
    {"$group": {"_id": "$source.chapter_name", "count": {"$sum": 1}}},
    {"$sort": {"_id": 1}},
]
for doc in col.aggregate(pipeline):
    print(f"  {(doc['_id'] or 'unknown')[:55]:<55} {doc['count']:>3}")
print()

if args.dry_run:
    print(f"  DRY-RUN -- would promote {count} rules → auto_approved")
    print(f"  Reason: SBC textbook-decoded rules, structural validation 0 issues,")
    print(f"          condition arrays intentionally empty (engine_specification type).")
else:
    result = col.update_many(
        query,
        {"$set": {
            "approval_status":           "auto_approved",
            "validation.verdict":        "approved",
            "validation.sbc_promotion":  f"Bulk-promoted: textbook-decoded classical rules, structural validation passed {NOW}",
        }}
    )
    print(f"  ✅ Promoted : {result.modified_count} rules → auto_approved")

    # Post-run counts
    aa  = col.count_documents({"source.batch_id": BATCH_ID, "approval_status": "auto_approved"})
    rej = col.count_documents({"source.batch_id": BATCH_ID, "approval_status": "rejected"})
    phr = col.count_documents({"source.batch_id": BATCH_ID, "approval_status": "pending_human_review"})
    print()
    print(f"  DB post-run: auto_approved={aa}  pending_human_review={phr}  rejected={rej}")

mongo.close()

print()
print("╔══════════════════════════════════════════════════════════════╗")
print("  ✅ SBC promotion complete")
print(f"  Log saved → {log_path}")
print("╚══════════════════════════════════════════════════════════════╝")

sys.stdout = sys.__stdout__
tee.close()
