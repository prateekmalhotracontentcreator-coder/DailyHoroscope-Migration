#!/usr/bin/env python3
"""
patch_bphs_vol2_phase1_c_empty_reject.py

Rejects 6 gap-fill rules from BPHS Vol 2 Phase 1 triage.
All 6 have the -GF suffix and share these defects:
  - detailed interpretation field is empty
  - method = 'gap_fill_direct' (non-standard, unverifiable)
  - condition structure malformed (missing type/sloka fields)
  - not verifiable against BPHS source text

Treatment: flagged → rejected

These are all in Ch57 (Saturn Mahadasha) batch.
If content exists in source, these should be re-encoded from scratch via
a new Codex commission referencing the specific slokas.

Dry run by default. Pass --live to apply.

Usage:
  MONGO_URL=<url> python3 backend/scripts/patch_bphs_vol2_phase1_c_empty_reject.py
  MONGO_URL=<url> python3 backend/scripts/patch_bphs_vol2_phase1_c_empty_reject.py --live
"""
import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR        = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")
TRIAGE_DATE    = "2026-06-03"
TRIAGE_SESSION = "bphs-vol2-ph1-triage-20260603"

_REJECT_NOTE = (
    "C_empty reject -- CC Triage 2026-06-03 (Vol 2 Phase 1): "
    "Gap-fill rule with empty `detailed` interpretation field. "
    "Method=gap_fill_direct (non-standard). "
    "Condition structure malformed (missing type/sloka fields). "
    "Not verifiable against BPHS Ch.57 Santhanam source. "
    "Rejected -- to be re-encoded from source sloka via new Codex commission if content exists."
)

C_EMPTY = [
    "R-BPHS57-PATCH-4B17E8-GF",   # Mercury 2nd lord → physical distress (empty detailed)
    "R-BPHS57-PATCH-5F5F3B-GF",   # Venus 2nd lord → physical distress (empty detailed)
    "R-BPHS57-PATCH-60E6E0-GF",   # Mercury 7th lord → physical distress (empty detailed)
    "R-BPHS57-PATCH-92F798-GF",   # Ketu in 2nd from Ascendant (empty detailed)
    "R-BPHS57-PATCH-DE1D14-GF",   # Venus 7th lord → physical distress (empty detailed)
    "R-BPHS57-PATCH-F0541B-GF",   # Rahu favourable middle Rahu AD in Saturn MD (empty detailed)
]


class _Tee:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._log    = open(path, "w", encoding="utf-8")
        self._stdout = sys.__stdout__
    def write(self, data: str) -> None:
        self._stdout.write(data); self._stdout.flush()
        self._log.write(data);   self._log.flush()
    def flush(self) -> None:
        self._stdout.flush(); self._log.flush()
    def close(self) -> None:
        self._log.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", default=os.environ.get("MONGO_URL", ""))
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--live",      action="store_true")
    args = parser.parse_args()

    if not args.mongo_url:
        print("ERROR: MONGO_URL env var not set."); sys.exit(1)

    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    mode     = "live" if args.live else "dryrun"
    log_path = LOG_DIR / f"patch_bphs_vol2_phase1_c_empty_reject_{ts}_{mode}.log"
    tee      = _Tee(log_path)
    sys.stdout = tee

    print("=" * 70)
    print(f"  LOG FILE: {log_path}")
    print("=" * 70)
    print()
    print(f"BPHS Vol 2 Phase 1 -- C_empty Reject")
    print(f"Mode    : {'🔴 LIVE -- WRITING TO DB' if args.live else '🟡 DRY RUN -- no changes'}")
    print(f"Rules   : {len(C_EMPTY)}")
    print(f"Action  : flagged → rejected  (gap_fill_direct, empty detailed, malformed condition)")
    print()

    from pymongo import MongoClient
    col = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10_000)[args.db_name]["interpretation_rules"]

    now     = datetime.now(timezone.utc)
    patched = 0
    skipped = 0
    errors  = []

    print(f"{'#':<4} {'Rule ID':<40} {'Pre-status':<22} Result")
    print("─" * 85)

    for i, rule_id in enumerate(C_EMPTY, 1):
        existing = col.find_one({"rule_id": rule_id},
                                {"approval_status": 1, "interpretation": 1, "_id": 1})
        if not existing:
            print(f"  {i:<4} {rule_id:<40} {'NOT FOUND':<22} ⚠️  SKIP")
            errors.append(f"{rule_id}: not found in DB")
            skipped += 1
            continue

        pre_status = existing.get("approval_status", "?")
        if pre_status not in ("flagged",):
            print(f"  {i:<4} {rule_id:<40} {pre_status:<22} ⏭  SKIP (not flagged)")
            skipped += 1
            continue

        # Confirm detailed is empty before rejecting
        interp    = existing.get("interpretation") or {}
        detailed  = str(interp.get("detailed", "") or "").strip()
        if detailed:
            print(f"  {i:<4} {rule_id:<40} {pre_status:<22} ⚠️  SKIP (detailed NOT empty: {detailed[:60]}...)")
            errors.append(f"{rule_id}: detailed field is not empty -- manual review needed")
            skipped += 1
            continue

        update_doc = {
            "$set": {
                "approval_status":           "rejected",
                "validation.reject_reason":  _REJECT_NOTE,
                "validation.triage_date":    TRIAGE_DATE,
                "validation.triage_session": TRIAGE_SESSION,
                "validation.triage_bucket":  "C_empty",
                "updated_at":                datetime.now(timezone.utc),
            }
        }

        if args.live:
            result = col.update_one({"rule_id": rule_id}, update_doc)
            ok = result.modified_count == 1
            status = "✅ REJECTED" if ok else "❌ FAILED"
            if ok:
                patched += 1
            else:
                errors.append(f"{rule_id}: update returned modified_count=0")
        else:
            status = "🟡 DRY RUN → rejected"
            patched += 1

        print(f"  {i:<4} {rule_id:<40} {pre_status:<22} {status}")

    print()
    print("=" * 70)
    print(f"Summary")
    print(f"  Mode     : {'LIVE' if args.live else 'DRY RUN'}")
    print(f"  Rejected : {patched} / {len(C_EMPTY)}")
    print(f"  Skipped  : {skipped}")
    if errors:
        print(f"  Errors   : {len(errors)}")
        for e in errors:
            print(f"    {e}")
    if not args.live:
        print()
        print("  Re-run with --live to apply.")
    print()
    print(f"Log saved: {log_path}")
    tee.close()


if __name__ == "__main__":
    main()
