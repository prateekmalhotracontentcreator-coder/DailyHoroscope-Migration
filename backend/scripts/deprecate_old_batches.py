#!/usr/bin/env python3
"""
deprecate_old_batches.py
------------------------
Marks all 'pending_review' rules from the old April 2026 batch ingest
(batch IDs ending in _NNN_20260413) as 'deprecated'.

These are early prototype batches from before the per-chapter ingest
process was established. Every book in these batches has since been
properly re-ingested with correct batch naming and science_ids:
  - lal-kitab_XXX_20260413   → superseded by lalkitab-chXX-v2-* (467 rules, jyotish)
  - a-text-book-of-astro_XXX → superseded by tba-chXX-v1-*       (1,665 rules, vedic_astrology)
  - longevity-and-astro_XXX  → superseded by longevity_58ch_v1    (149 rules, kp_jyotish)
  - a-book-of-300-import_XXX → superseded by 300-combinations-v1  (329 rules, jyotish)
  - longevity-and-un-nat_XXX → superseded by longevity_unnatural_v1(44 rules, kp_jyotish)

All old batches also used incorrect science_id='vedic_astrology' for books
that should be jyotish or kp_jyotish.

Adds a deprecation_reason field for traceability.

Every run prints the log file name and saves output to a timestamped log.

Usage:
    # Dry-run first (no writes):
    python3 backend/scripts/deprecate_old_batches.py --dry-run

    # Live run:
    python3 backend/scripts/deprecate_old_batches.py
"""

from __future__ import annotations
import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from pymongo import MongoClient

# ---------------------------------------------------------------------------
# Args
# ---------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true",
                    help="Print what would be deprecated without writing to MongoDB")
args = parser.parse_args()

# ---------------------------------------------------------------------------
# Log file setup
# ---------------------------------------------------------------------------
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
mode_tag = "dry-run" if args.dry_run else "live"
log_path = LOG_DIR / f"deprecate_old_batches_{mode_tag}_{timestamp}.log"

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
print(f"  deprecate_old_batches.py  [{mode_tag.upper()}]")
print(f"  Run timestamp : {timestamp} UTC")
print(f"  Log file      : {log_path}")
print(f"╚══════════════════════════════════════════════════════════════╝")
print()

if args.dry_run:
    print("  ⚠️  DRY-RUN MODE -- no changes will be written to MongoDB.")
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
# Identify all old _20260413 pending_review rules
# ---------------------------------------------------------------------------
# Old batches (April 2026) stored batch_id inside source.batch_id only --
# the top-level batch_id field was not set. Filter on source.batch_id.
OLD_BATCH_FILTER = {
    "approval_status": "pending_review",
    "source.batch_id": {"$regex": "_20260413$"}
}

total_to_deprecate = col.count_documents(OLD_BATCH_FILTER)
print(f"Rules matching (pending_review + _20260413 batch): {total_to_deprecate}")
print()

if total_to_deprecate == 0:
    print("✅ Nothing to deprecate -- no old _20260413 pending_review rules found.")
    client.close()
    sys.exit(0)

# ---------------------------------------------------------------------------
# Show per-batch breakdown before acting
# ---------------------------------------------------------------------------
from collections import defaultdict
batch_counts: dict[str, int] = defaultdict(int)
batch_sids: dict[str, set] = defaultdict(set)

for r in col.find(OLD_BATCH_FILTER, {"batch_id": 1, "source": 1, "science_id": 1, "_id": 0}):
    bid = r.get("batch_id") or (r.get("source") or {}).get("batch_id") or "?"
    sid = r.get("science_id", "?")
    batch_counts[bid] += 1
    batch_sids[bid].add(sid)

print("─" * 60)
print(f"  {'batch_id':<42} {'count':>5}  science_id")
print("─" * 60)
for bid, cnt in sorted(batch_counts.items()):
    sids = ", ".join(sorted(batch_sids[bid]))
    print(f"  {bid:<42} {cnt:>5}  {sids}")
print("─" * 60)
print(f"  TOTAL                                         {total_to_deprecate:>5}")
print()

# ---------------------------------------------------------------------------
# Deprecate (or dry-run)
# ---------------------------------------------------------------------------
DEPRECATION_REASON = (
    "Superseded by properly-named per-chapter ingest batches. "
    "Original batch used wrong science_id (vedic_astrology) for non-vedic books. "
    "Deprecated 2026-06-08."
)

if args.dry_run:
    print(f"  DRY-RUN: would set approval_status='deprecated' on {total_to_deprecate} rules.")
    print(f"  deprecation_reason: '{DEPRECATION_REASON}'")
    print()
    print("  Re-run without --dry-run to apply.")
else:
    result = col.update_many(
        OLD_BATCH_FILTER,
        {"$set": {
            "approval_status": "deprecated",
            "deprecation_reason": DEPRECATION_REASON,
            "deprecated_at": datetime.now(timezone.utc).isoformat(),
        }}
    )
    matched = result.matched_count
    modified = result.modified_count
    print(f"  ✅ Updated: matched={matched}, modified={modified}")
    print()

    if modified != total_to_deprecate:
        print(f"  ⚠️  Warning: expected to modify {total_to_deprecate} but only modified {modified}.")
        print(f"     Some rules may have changed status between the query and the update.")
    else:
        print(f"  ✅ All {modified} old batch rules successfully deprecated.")
    print()

    # Verify
    remaining = col.count_documents(OLD_BATCH_FILTER)
    print(f"  Post-deprecation pending_review in _20260413 batches: {remaining}")
    if remaining == 0:
        print(f"  ✅ Confirmed -- no _20260413 rules remain in pending_review.")
    else:
        print(f"  ⚠️  {remaining} rules still pending_review. Investigate.")
    print()

    total_pr_remaining = col.count_documents({"approval_status": "pending_review"})
    print(f"  Total pending_review remaining in DB: {total_pr_remaining}")
    print(f"  (Should be ~311 -- the 5 Remedies batches + tba-ch15)")
    print()

client.close()

print(f"╔══════════════════════════════════════════════════════════════╗")
print(f"  ✅ {'Dry-run complete' if args.dry_run else 'Deprecation complete'}")
print(f"  Log saved → {log_path}")
print(f"╚══════════════════════════════════════════════════════════════╝")

sys.stdout = sys.__stdout__
tee.close()
