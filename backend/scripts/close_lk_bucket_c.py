#!/usr/bin/env python3
"""
close_lk_bucket_c.py
---------------------
Closes KE-OP-LK-2: final disposition of all 17 LK Bucket C flagged rules
+ 4 pending_human_review rules in the same batch.

Actions:
  PROMOTE (17 rules): flagged → auto_approved
    - ch20-yog-01/05/09      : classical LK medical rules (empty flag_reasons = validator mismatch)
    - ch20-gp-interact        : LK house interaction framework rule
    - ch21-gp-05              : LK Father's Debt doctrine
    - ch23-geoveto-triangle   : classical LK Vastu rule
    - ch24-age-*  (11 rules)  : classical LK Aayu lifespan rules

  PROMOTE (4 rules): pending_human_review → auto_approved
    - ch24-age-early-9y, ch24-age-longlife-sun-rahu,
      ch24-age-threshold-35, ch24-age-threshold-50

  REJECT (4 rules): flagged → rejected + active: false
    - ch24-mortality-north-star         : physical observation, non-automatable
    - ch24-mortality-reflection-organic : physical observation, non-automatable
    - ch24-mortality-reflection-mirror  : physical observation, non-automatable
    - ch24-mortality-stasis             : physical observation, non-automatable, terminal

Usage:
  python3 backend/scripts/close_lk_bucket_c.py --dry-run
  python3 backend/scripts/close_lk_bucket_c.py
"""

from __future__ import annotations
import argparse, os, sys
from datetime import datetime, timezone
from pathlib import Path
from pymongo import MongoClient

parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()

LOG_DIR  = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
ts       = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
mode_tag = "dry-run" if args.dry_run else "live"
log_path = LOG_DIR / f"close_lk_bucket_c_{mode_tag}_{ts}.log"

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

print(f"Log saved → {log_path}\n")

MONGO_URL = os.environ.get("MONGO_URL")
if not MONGO_URL:
    print("ERROR: MONGO_URL not set"); sys.exit(1)

mongo = MongoClient(MONGO_URL, serverSelectionTimeoutMS=10_000)
col   = mongo["horoscope_db"]["interpretation_rules"]
NOW   = datetime.now(timezone.utc).isoformat()

# ── Rule lists ──────────────────────────────────────────────────────────────

PROMOTE_FLAGGED = [
    "lalkitab-ch20-yog-01",
    "lalkitab-ch20-yog-05",
    "lalkitab-ch20-yog-09",
    "lalkitab-ch20-gp-interact",
    "lalkitab-ch21-gp-05",
    "lalkitab-ch23-geoveto-triangle",
    "lalkitab-ch24-age-infancy-12d",
    "lalkitab-ch24-age-childhood-12m",
    "lalkitab-ch24-age-sudden-death",
    "lalkitab-ch24-age-long-illness",
    "lalkitab-ch24-age-survival-son",
    "lalkitab-ch24-age-father-dependency",
    "lalkitab-ch24-age-shortlife-2y",
]

PROMOTE_PHR = [
    "lalkitab-ch24-age-early-9y",
    "lalkitab-ch24-age-longlife-sun-rahu",
    "lalkitab-ch24-age-threshold-35",
    "lalkitab-ch24-age-threshold-50",
]

REJECT = [
    "lalkitab-ch24-mortality-north-star",
    "lalkitab-ch24-mortality-reflection-organic",
    "lalkitab-ch24-mortality-reflection-mirror",
    "lalkitab-ch24-mortality-stasis",
]

REJECT_REASON = (
    "Physical/observational death sign -- non-automatable (checkable:false). "
    "Cannot be fired by engine. Inappropriate for digital user-facing context. "
    f"Rejected {NOW}."
)

PROMOTE_NOTE = (
    "Bulk-promoted: classical LK text, validator framework mismatch (empty flag_reasons). "
    f"KE-OP-LK-2 closure {NOW}."
)

# ── Header ───────────────────────────────────────────────────────────────────

print("╔══════════════════════════════════════════════════════════════╗")
print(f"  close_lk_bucket_c.py  [{mode_tag.upper()}]")
print(f"  Run   : {ts} UTC")
print(f"  Log   : {log_path}")
print("╚══════════════════════════════════════════════════════════════╝\n")

print(f"  PROMOTE flagged → auto_approved : {len(PROMOTE_FLAGGED)} rules")
print(f"  PROMOTE PHR     → auto_approved : {len(PROMOTE_PHR)} rules")
print(f"  REJECT  flagged → rejected      : {len(REJECT)} rules")
print()

# ── Pre-flight verification ──────────────────────────────────────────────────

print("── Pre-flight ──────────────────────────────────────────────────")
all_ids = PROMOTE_FLAGGED + PROMOTE_PHR + REJECT
missing = []
for rid in all_ids:
    if not col.find_one({"rule_id": rid}, {"_id": 1}):
        missing.append(rid)
        print(f"  [WARN] Not found in DB: {rid}")

if missing:
    print(f"\n  {len(missing)} rule(s) missing -- aborting.")
    mongo.close(); sys.stdout = sys.__stdout__; tee.close(); sys.exit(1)

print(f"  All {len(all_ids)} rule IDs confirmed in DB.\n")

# ── Execute ──────────────────────────────────────────────────────────────────

if args.dry_run:
    print("── DRY-RUN -- no writes ─────────────────────────────────────────")
    print(f"  Would promote {len(PROMOTE_FLAGGED)} flagged → auto_approved")
    for rid in PROMOTE_FLAGGED:
        print(f"    ✓ {rid}")
    print()
    print(f"  Would promote {len(PROMOTE_PHR)} pending_human_review → auto_approved")
    for rid in PROMOTE_PHR:
        print(f"    ✓ {rid}")
    print()
    print(f"  Would reject {len(REJECT)} → rejected + active:false")
    for rid in REJECT:
        print(f"    ✗ {rid}")
else:
    # Promote flagged
    print("── Promoting flagged → auto_approved ───────────────────────────")
    pf_ok = 0
    for rid in PROMOTE_FLAGGED:
        res = col.update_one(
            {"rule_id": rid, "approval_status": "flagged"},
            {"$set": {
                "approval_status":           "auto_approved",
                "validation.verdict":        "approved",
                "validation.lk_promotion":   PROMOTE_NOTE,
            }}
        )
        if res.modified_count:
            print(f"  ✅ {rid}")
            pf_ok += 1
        else:
            cur = col.find_one({"rule_id": rid}, {"approval_status": 1})
            print(f"  ⚠️  {rid} -- not modified (current status: {cur.get('approval_status')})")

    print(f"\n  Promoted: {pf_ok}/{len(PROMOTE_FLAGGED)}\n")

    # Promote PHR
    print("── Promoting pending_human_review → auto_approved ──────────────")
    pp_ok = 0
    for rid in PROMOTE_PHR:
        res = col.update_one(
            {"rule_id": rid, "approval_status": "pending_human_review"},
            {"$set": {
                "approval_status":           "auto_approved",
                "validation.verdict":        "approved",
                "validation.lk_promotion":   PROMOTE_NOTE,
            }}
        )
        if res.modified_count:
            print(f"  ✅ {rid}")
            pp_ok += 1
        else:
            cur = col.find_one({"rule_id": rid}, {"approval_status": 1})
            print(f"  ⚠️  {rid} -- not modified (current status: {cur.get('approval_status')})")

    print(f"\n  Promoted: {pp_ok}/{len(PROMOTE_PHR)}\n")

    # Reject
    print("── Rejecting → rejected + active:false ─────────────────────────")
    rj_ok = 0
    for rid in REJECT:
        res = col.update_one(
            {"rule_id": rid},
            {"$set": {
                "approval_status":          "rejected",
                "active":                   False,
                "validation.verdict":       "rejected",
                "validation.reject_reason": REJECT_REASON,
            }}
        )
        if res.modified_count:
            print(f"  ✗  {rid}")
            rj_ok += 1
        else:
            print(f"  ⚠️  {rid} -- not modified")

    print(f"\n  Rejected: {rj_ok}/{len(REJECT)}\n")

    # Post-run counts for the LK batch
    print("── Post-run DB state (lalkitab_all_v2_20260605) ────────────────")
    batch_q = {"source.batch_id": "lalkitab_all_v2_20260605"}
    for status in ["auto_approved", "pending_human_review", "flagged", "rejected"]:
        n = col.count_documents({**batch_q, "approval_status": status})
        print(f"  {status:<25} {n:>4}")
    total = col.count_documents(batch_q)
    print(f"  {'TOTAL':<25} {total:>4}")

mongo.close()

print()
print("╔══════════════════════════════════════════════════════════════╗")
print(f"  KE-OP-LK-2 closure {'SIMULATED' if args.dry_run else 'COMPLETE'}")
print(f"  Log saved → {log_path}")
print("╚══════════════════════════════════════════════════════════════╝")

sys.stdout = sys.__stdout__
tee.close()
print(f"Log saved → {log_path}")
