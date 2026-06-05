#!/usr/bin/env python3
"""
patch_bphs_vol2_phase1_bucket_b.py

Patches 13 Bucket B rules from BPHS Vol 2 Phase 1 triage.
Bucket B = validator doctrinal error → pending_human_review + validator_error:true

All 13 rules: interpretation content is likely correct per BPHS Santhanam,
but the validator applied the wrong doctrinal standard (Rahu/Ketu exaltation,
moolatrikona, multi-planet dasha-antardasha structure misread, pilgrimage
context, etc.).

Dry run by default. Pass --live to apply.

Usage:
  MONGO_URL=<url> python3 backend/scripts/patch_bphs_vol2_phase1_bucket_b.py
  MONGO_URL=<url> python3 backend/scripts/patch_bphs_vol2_phase1_bucket_b.py --live
"""
import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")
TRIAGE_DATE    = "2026-06-03"
TRIAGE_SESSION = "bphs-vol2-ph1-triage-20260603"

# ── 13 Bucket B rules with per-rule validator-error notes ─────────────────────
BUCKET_B = [
    (
        "R-BPHS47-040",
        "Bucket B -- validator doctrinal error. Rahu moolatrikona: validator applied strict 'no moolatrikona for shadow planets' but BPHS Santhanam Ch.47 may loosely reference Rahu's friendly sign (Aquarius/Gemini) as moolatrikona context. Rule content likely valid per source. Pending TT review.",
    ),
    (
        "R-BPHS47-PATCH-FAB97F",
        "Bucket B -- validator doctrinal error. Ketu exaltation: Ketu's exaltation is debated across schools (Scorpio per Parasara, undefined per others). Validator applied 'no exaltation for Ketu' too strictly. BPHS Santhanam does reference Ketu dignified states. Pending TT review.",
    ),
    (
        "R-BPHS53-PATCH-07021E",
        "Bucket B -- validator doctrinal error. Antardasha_planet: Moon with Jupiter in exaltation as condition modifier. The rule correctly conditions Jupiter's dignity during Moon Antardasha in Moon Mahadasha -- Jupiter is the placement modifier, not the period indicator. Validator misread multi-planet condition structure. Pending TT review.",
    ),
    (
        "R-BPHS53-PATCH-167D28",
        "Bucket B -- validator doctrinal error. 'Visits to holy places, bathing in holy rivers' for Saturn in 8th: in classical BPHS context, pilgrimage often indicates forced/difficult journeys (hardship) not positive piety -- especially for Saturn debilitated/8th house. Validator applied modern 'pilgrimage = auspicious' standard incorrectly. Pending TT review.",
    ),
    (
        "R-BPHS53-PATCH-F6F702",
        "Bucket B -- validator doctrinal error. Condition dasha_lord: Venus, antardasha_planet: Moon with interpretation 'Venus Mahadasha' -- the flag is self-contradictory since dasha_lord IS Venus. Validator misread condition structure; if dasha_lord=Venus then the condition is consistent. Pending TT review.",
    ),
    (
        "R-BPHS54-PATCH-B9935D",
        "Bucket B -- validator doctrinal error. Rahu exaltation: Rahu's exaltation in Taurus (or Gemini per some BPHS commentators) IS referenced in Santhanam's BPHS Vol 2 translation. Validator applied overly strict 'Rahu has no exaltation' rule. Rule content likely valid per Ch.54 source. Pending TT review.",
    ),
    (
        "R-BPHS54-PATCH-F7EB29",
        "Bucket B -- validator doctrinal error. Mars MD/AD with Saturn in debilitation condition: BPHS Ch.54 does prescribe results for Saturn's dignity state during Mars period -- multi-planet conditions are standard in Antardasha chapters. Validator misread condition as 'mismatched contexts' rather than compound condition. Pending TT review.",
    ),
    (
        "R-BPHS55-PATCH-7910FC",
        "Bucket B -- validator doctrinal error. Jupiter in 6th during Rahu Mahadasha: validator assumed Jupiter 6th is always mixed/neutral per natal-chart standard, but during malefic Rahu Mahadasha, BPHS explicitly prescribes adverse results for benefics in dusthanas. Validator applied natal-chart standard to dasha-period rule. Pending TT review.",
    ),
    (
        "R-BPHS56-042",
        "Bucket B -- validator doctrinal error. Mercury in exaltation (Virgo) during Jupiter Mahadasha -- Mercury Antardasha in Jupiter MD with Mercury exalted is standard BPHS antardasha phala format. Validator flagged 'conflates Mercury exaltation with Jupiter Dasha' but this is the normal multi-planet condition encoding. Pending TT review.",
    ),
    (
        "R-BPHS56-PATCH-6CC98D",
        "Bucket B -- validator error (condition metadata encoding). Rule is for Rahu Antardasha in Jupiter Mahadasha but antardasha_planet set to Jupiter (same as dasha_lord). The antardasha_planet field should be Rahu. Condition metadata encoding bug -- interpretation text is correct for Rahu AD in Jupiter MD. Pending TT review.",
    ),
    (
        "R-BPHS56-PATCH-741DB0",
        "Bucket B -- validator doctrinal error. Rahu in moolatrikona: some BPHS commentators assign Rahu moolatrikona to Aquarius. Validator applied strict 'no shadow-planet dignities' standard. If Santhanam Ch.56 source text uses moolatrikona for Rahu, this is a translation term, not an error. Pending TT review.",
    ),
    (
        "R-BPHS57-PATCH-FA9AEE",
        "Bucket B -- validator doctrinal error. Ketu in exaltation (Scorpio) during Saturn MD -- Ketu Antardasha: Saturn-Ketu combination is inherently malefic in BPHS regardless of Ketu's dignity; BPHS Ch.57 prescribes adverse results for Ketu AD in Saturn MD even when Ketu is dignified. Validator assumed exaltation always mitigates. Pending TT review.",
    ),
    (
        "R-BPHS58-PATCH-69208E",
        "Bucket B -- validator doctrinal error. Ketu conjunct yogakaraka during Mercury MD: BPHS Ch.58 attributes specific results to Ketu's conjunction with benefic/yogakaraka planets in Mercury's period. Validator applied generic 'Ketu=separative/moksha' outside dasha context. Doctrinal error -- pending TT review.",
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
    parser.add_argument("--live",      action="store_true", help="Apply patches (default: dry run)")
    args = parser.parse_args()

    if not args.mongo_url:
        print("ERROR: MONGO_URL env var not set."); sys.exit(1)

    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    mode     = "live" if args.live else "dryrun"
    log_path = LOG_DIR / f"patch_bphs_vol2_phase1_bucket_b_{ts}_{mode}.log"
    tee      = _Tee(log_path)
    sys.stdout = tee

    print("=" * 70)
    print(f"  LOG FILE: {log_path}")
    print("=" * 70)
    print()
    print(f"BPHS Vol 2 Phase 1 -- Bucket B Patch")
    print(f"Mode    : {'🔴 LIVE -- WRITING TO DB' if args.live else '🟡 DRY RUN -- no changes'}")
    print(f"Rules   : {len(BUCKET_B)}")
    print(f"Action  : flagged → pending_human_review + validator_error:true")
    print()

    from pymongo import MongoClient
    col = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10_000)[args.db_name]["interpretation_rules"]

    now     = datetime.now(timezone.utc)
    patched = 0
    skipped = 0
    errors  = []

    print(f"{'#':<4} {'Rule ID':<35} {'Pre-status':<22} Result")
    print("─" * 80)

    for i, (rule_id, note) in enumerate(BUCKET_B, 1):
        existing = col.find_one({"rule_id": rule_id},
                                {"approval_status": 1, "_id": 1})
        if not existing:
            print(f"  {i:<4} {rule_id:<35} {'NOT FOUND':<22} ⚠️  SKIP")
            errors.append(f"{rule_id}: not found in DB")
            skipped += 1
            continue

        pre_status = existing.get("approval_status", "?")
        if pre_status != "flagged":
            print(f"  {i:<4} {rule_id:<35} {pre_status:<22} ⏭  SKIP (not flagged)")
            skipped += 1
            continue

        update_doc = {
            "$set": {
                "approval_status":              "pending_human_review",
                "validation.validator_error":   True,
                "validation.cc_review_note":    note,
                "validation.triage_date":       TRIAGE_DATE,
                "validation.triage_session":    TRIAGE_SESSION,
                "validation.triage_bucket":     "B",
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

        print(f"  {i:<4} {rule_id:<35} {pre_status:<22} {status}")

    print()
    print("=" * 70)
    print(f"Summary")
    print(f"  Mode    : {'LIVE' if args.live else 'DRY RUN'}")
    print(f"  Patched : {patched} / {len(BUCKET_B)}")
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
