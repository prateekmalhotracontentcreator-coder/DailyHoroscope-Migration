#!/usr/bin/env python3
"""
patch_bphs_vol2_phase1_api_bucket_b.py

Patches 7 rules upgraded from Bucket C → Bucket B by the API validator
(claude-haiku-4-5) during BPHS Vol 2 Phase 1 triage (2026-06-03).

Bucket B = validator doctrinal error → pending_human_review + validator_error:true
These rules were originally flagged, then the API validator confirmed the
underlying content is authentic BPHS doctrine; only the KE validator's logic
was wrong, not the rule itself.

Dry run by default. Pass --live to apply.

Usage:
  MONGO_URL=<url> python3 backend/scripts/patch_bphs_vol2_phase1_api_bucket_b.py
  MONGO_URL=<url> python3 backend/scripts/patch_bphs_vol2_phase1_api_bucket_b.py --live
"""
import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR        = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")
TRIAGE_DATE    = "2026-06-03"
TRIAGE_SESSION = "bphs-vol2-ph1-triage-20260603"

# ── 7 API-confirmed Bucket B rules ────────────────────────────────────────────
# Format: (rule_id, api_confidence, cc_review_note)
BUCKET_B_API = [
    (
        "R-BPHS47-077",
        0.85,
        "API validator (haiku): JSON field-mapping error -- condition text "
        "belongs in effect slot and vice versa. Content is authentic BPHS Ch.47 "
        "doctrine (Ketu Dasa final phase → ailments and distant journeys). "
        "Requires field re-mapping only; no doctrinal change needed.",
    ),
    (
        "R-BPHS47-PATCH-D722F2",
        0.82,
        "API validator (haiku): 'Own sign' is a valid unified dignity state "
        "covering both Venus signs (Taurus and Libra). BPHS doctrine on "
        "planetary dignity does not require sign-specific disambiguation in "
        "dasha effects. Rule content correctly reflects Santhanam Ch.47 "
        "Sun-Venus dasha combinations.",
    ),
    (
        "R-BPHS53-PATCH-6951E2",
        0.78,
        "API validator (haiku): Mixed auspicious-then-inauspicious results for "
        "Rahu AD in Moon MD is explicit BPHS Ch.53 doctrine. Validator "
        "incorrectly flagged the apparent paradox (trikona placement yet "
        "inauspicious results) as a logical encoding error. Rule content is "
        "authentic despite appearing contradictory.",
    ),
    (
        "R-BPHS57-PATCH-7B534F",
        0.75,
        "API validator (haiku): Maraka principle (Sun as 7th lord = "
        "death-inflicting) is correct BPHS doctrine. Summary oversimplifies "
        "what the detailed condition correctly specifies: manifestation requires "
        "Saturn Antardasha activation context. Validator flagged "
        "oversimplification in summary, not a doctrinal error in the rule body.",
    ),
    (
        "R-BPHS58-040",
        0.75,
        "API validator (haiku): 'In the circumstances mentioned above' is a "
        "legitimate BPHS literary cross-reference convention pointing to prior "
        "slokas. BPHS Ch.58 uses sequential contextual rules of this type. "
        "The rule structure is consistent with BPHS methodology even if "
        "operationally incomplete without the preceding sloka context.",
    ),
    (
        "R-BPHS58-052",
        0.72,
        "API validator (haiku): Natal Moon lordship (2nd or 7th from Ascendant) "
        "correctly modifies Mercury dasha effects in BPHS Ch.58. Summary "
        "phrasing is imprecise ('during Mercury Mahadasha' should read 'natal "
        "condition active during Mercury Mahadasha') but doctrinally sound. "
        "Validator applied dasha-specificity requirement too strictly.",
    ),
    (
        "R-BPHS58-PATCH-1A2F4A",
        0.72,
        "API validator (haiku): 'Which of the king and fire' is an OCR or "
        "transcription artifact in the KE database text. Underlying rule "
        "premise (Mars + malefics in 8th from Mercury dasha lord → distress, "
        "danger from kinsmen, loss of position) is valid per BPHS Ch.58 "
        "affliction doctrine. Text correction needed; rule premise is sound.",
    ),
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
    parser.add_argument("--live",      action="store_true",
                        help="Apply patches (default: dry run)")
    args = parser.parse_args()

    if not args.mongo_url:
        print("ERROR: MONGO_URL env var not set."); sys.exit(1)

    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    mode     = "live" if args.live else "dryrun"
    log_path = LOG_DIR / f"patch_bphs_vol2_phase1_api_bucket_b_{ts}_{mode}.log"
    tee      = _Tee(log_path)
    sys.stdout = tee

    print("=" * 70)
    print(f"  LOG FILE: {log_path}")
    print("=" * 70)
    print()
    print("BPHS Vol 2 Phase 1 -- API-Confirmed Bucket B Patch")
    print(f"Mode    : {'🔴 LIVE -- WRITING TO DB' if args.live else '🟡 DRY RUN -- no changes'}")
    print(f"Rules   : {len(BUCKET_B_API)}")
    print(f"Action  : flagged → pending_human_review + validator_error:true")
    print(f"Source  : claude-haiku-4-5 API validator (2026-06-03 session)")
    print()

    from pymongo import MongoClient
    col = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10_000)[
        args.db_name]["interpretation_rules"]

    now     = datetime.now(timezone.utc)
    patched = 0
    skipped = 0
    errors  = []

    print(f"{'#':<4} {'Rule ID':<40} {'Pre-status':<22} Result")
    print("─" * 85)

    for i, (rule_id, confidence, note) in enumerate(BUCKET_B_API, 1):
        existing = col.find_one({"rule_id": rule_id},
                                {"approval_status": 1, "_id": 1})
        if not existing:
            print(f"  {i:<4} {rule_id:<40} {'NOT FOUND':<22} ⚠️  SKIP")
            errors.append(f"{rule_id}: not found in DB")
            skipped += 1
            continue

        pre_status = existing.get("approval_status", "?")
        if pre_status != "flagged":
            print(f"  {i:<4} {rule_id:<40} {pre_status:<22} ⏭  SKIP (not flagged)")
            skipped += 1
            continue

        update_doc = {
            "$set": {
                "approval_status":              "pending_human_review",
                "validation.validator_error":   True,
                "validation.api_verdict":       "validator_error",
                "validation.api_confidence":    confidence,
                "validation.api_model":         "claude-haiku-4-5",
                "validation.cc_review_note":    note,
                "validation.triage_date":       TRIAGE_DATE,
                "validation.triage_session":    TRIAGE_SESSION,
                "validation.triage_bucket":     "B_api_confirmed",
                "updated_at":                   now,
            }
        }

        if args.live:
            result = col.update_one({"rule_id": rule_id}, update_doc)
            ok = result.modified_count == 1
            status = "✅ PATCHED" if ok else "❌ FAILED"
            if ok:
                patched += 1
            else:
                errors.append(f"{rule_id}: update returned modified_count=0")
        else:
            status = "🟡 DRY RUN"
            patched += 1

        print(f"  {i:<4} {rule_id:<40} {pre_status:<22} {status}")

    print()
    print("=" * 70)
    print("Summary")
    print(f"  Mode    : {'LIVE' if args.live else 'DRY RUN'}")
    print(f"  Patched : {patched} / {len(BUCKET_B_API)}")
    print(f"  Skipped : {skipped}")
    if errors:
        print(f"  Errors  : {len(errors)}")
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
