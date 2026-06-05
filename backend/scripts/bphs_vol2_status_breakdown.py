#!/usr/bin/env python3
"""
BPHS Vol 2 Phase 1 -- Approval Status Breakdown per Batch
Run: MONGO_URL=<url> python3 backend/scripts/bphs_vol2_status_breakdown.py
"""
import os, sys
from datetime import datetime
from pathlib import Path
from pymongo import MongoClient

url = os.environ.get("MONGO_URL", "")
if not url:
    print("ERROR: MONGO_URL not set"); sys.exit(1)

# ── Log file setup ─────────────────────────────────────────────────────────────
LOG_DIR  = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")
LOG_DIR.mkdir(parents=True, exist_ok=True)
ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
log_path = LOG_DIR / f"bphs_vol2_status_breakdown_{ts}.log"

class _Tee:
    def __init__(self, path):
        self._log    = open(path, "w", encoding="utf-8")
        self._stdout = sys.__stdout__
    def write(self, data):
        self._stdout.write(data); self._stdout.flush()
        self._log.write(data);   self._log.flush()
    def flush(self):
        self._stdout.flush(); self._log.flush()
    def close(self):
        self._log.close()

tee = _Tee(log_path)
sys.stdout = tee

# ── Header ─────────────────────────────────────────────────────────────────────
print("=" * 70)
print(f"  LOG FILE: {log_path}")
print("=" * 70)
print()

col = MongoClient(url, serverSelectionTimeoutMS=8000)["horoscope_db"]["interpretation_rules"]

BATCHES = [
    ("Ch47", "bphs-ch47-dasha-20260416"),
    ("Ch53", "bphs-ch53-dasha-20260417"),
    ("Ch54", "bphs-ch54-dasha-20260417"),
    ("Ch55", "bphs-ch55-dasha-20260417"),
    ("Ch56", "bphs-ch56-dasha-20260418"),
    ("Ch57", "bphs-ch57-dasha-20260419"),
    ("Ch58", "bphs-ch58-dasha-20260419"),
]

STATUSES = ["auto_approved", "pending_human_review", "pending_review",
            "flagged", "deprecated", "rejected"]

print(f"\n{'Ch':<6} {'Total':<7} {'AA':<6} {'PHR':<6} {'PR':<5} {'FLAG':<6} {'DEPR':<6} {'REJ':<5}")
print("─" * 65)

grand = {s: 0 for s in STATUSES}
grand["total"] = 0

for ch, batch_id in BATCHES:
    total = col.count_documents({"source.batch_id": batch_id})
    counts = {}
    for s in STATUSES:
        counts[s] = col.count_documents({"source.batch_id": batch_id, "approval_status": s})
        grand[s] += counts[s]
    grand["total"] += total

    markers = ""
    if counts["flagged"] > 0:    markers += " ⚠️"
    if counts["deprecated"] > 0: markers += " 🔴"

    print(f"  {ch:<6} {total:<7} "
          f"{counts['auto_approved']:<6} "
          f"{counts['pending_human_review']:<6} "
          f"{counts['pending_review']:<5} "
          f"{counts['flagged']:<6} "
          f"{counts['deprecated']:<6} "
          f"{counts['rejected']:<5}{markers}")

print("─" * 65)
print(f"  {'TOTAL':<6} {grand['total']:<7} "
      f"{grand['auto_approved']:<6} "
      f"{grand['pending_human_review']:<6} "
      f"{grand['pending_review']:<5} "
      f"{grand['flagged']:<6} "
      f"{grand['deprecated']:<6} "
      f"{grand['rejected']:<5}")

# --- Active only (exclude deprecated) ---
print("\n── Active rules only (excl. deprecated) ─────────────────────────")
batch_ids = [b for _, b in BATCHES]
active_q   = {"source.batch_id": {"$in": batch_ids}, "approval_status": {"$ne": "deprecated"}}
active_tot = col.count_documents(active_q)
active_aa  = col.count_documents({**active_q, "approval_status": "auto_approved"})
active_phr = col.count_documents({**active_q, "approval_status": "pending_human_review"})
active_pr  = col.count_documents({**active_q, "approval_status": "pending_review"})
active_fl  = col.count_documents({**active_q, "approval_status": "flagged"})

print(f"  Active total         : {active_tot}")
print(f"  auto_approved        : {active_aa}")
print(f"  pending_human_review : {active_phr}")
print(f"  pending_review       : {active_pr}")
print(f"  flagged              : {active_fl}  ← triage target")

# --- Flagged breakdown by chapter ---
if active_fl > 0:
    print("\n── Flagged breakdown by chapter ──────────────────────────────────")
    for ch, batch_id in BATCHES:
        fl = col.count_documents({"source.batch_id": batch_id, "approval_status": "flagged"})
        if fl > 0:
            print(f"  {ch} : {fl} flagged")

    # Sample 5 flagged rules to see structure
    print("\n── Sample flagged rules (up to 5) ────────────────────────────────")
    samples = list(col.find(
        {**active_q, "approval_status": "flagged"},
        {"rule_id": 1, "approval_status": 1, "source.batch_id": 1,
         "flag_reason": 1, "text": 1, "_id": 0}
    ).limit(5))
    for r in samples:
        rid    = r.get("rule_id", "?")
        reason = r.get("flag_reason") or r.get("flags", {})
        txt    = (r.get("text") or "")[:80]
        print(f"  {rid}")
        print(f"    flag_reason : {reason}")
        print(f"    text        : {txt}...")
        print()

# --- Deprecated breakdown ---
depr_tot = col.count_documents({"source.batch_id": {"$in": batch_ids}, "approval_status": "deprecated"})
if depr_tot > 0:
    print(f"\n── Deprecated rules ({depr_tot} total) ──────────────────────────────")
    print("  These are superseded by re-ingest passes -- OK to ignore for triage.")
    for ch, batch_id in BATCHES:
        dp = col.count_documents({"source.batch_id": batch_id, "approval_status": "deprecated"})
        if dp > 0:
            print(f"  {ch} : {dp} deprecated")
    # Check overlap: deprecated rule_ids that also have an active copy
    depr_ids  = set(r["rule_id"] for r in
                    col.find({"source.batch_id": {"$in": batch_ids}, "approval_status": "deprecated"},
                             {"rule_id": 1, "_id": 0}))
    active_ids = set(r["rule_id"] for r in
                     col.find(active_q, {"rule_id": 1, "_id": 0}))
    overlap = depr_ids & active_ids
    print(f"\n  Deprecated rule_ids that also have an active copy : {len(overlap)}")
    print(f"  Deprecated rule_ids with NO active copy (orphans)  : {len(depr_ids - active_ids)}")

print()
print("=" * 70)
print(f"Log saved: {log_path}")
print("=" * 70)

tee.close()
