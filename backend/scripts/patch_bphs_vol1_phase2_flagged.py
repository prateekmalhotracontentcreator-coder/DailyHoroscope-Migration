#!/usr/bin/env python3
"""patch_bphs_vol1_phase2_flagged.py

Patches BPHS Vol 1 Phase 2 flagged rules based on triage classification.

Bucket B (14 rules) -- Validator doctrinal errors:
  flagged → pending_human_review + validator_error:true

Direct CC fixes (2 rules):
  bphs1-ch03-044  Sun+Cancer factual error  → PHR + corrected text
  bphs1-ch32-033  Wife in 2nd house error   → PHR + corrected text

Usage:
  python3 backend/scripts/patch_bphs_vol1_phase2_flagged.py \\
    --mongo-url "$MONGO_URL" --dry-run

  python3 backend/scripts/patch_bphs_vol1_phase2_flagged.py \\
    --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

BATCH_ID = "bphs-vol1-phase2-v1-20260601"
LOG_DIR  = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")

# ── Bucket B: validator doctrinal errors ──────────────────────────────────────
BUCKET_B_RULES = [
    # 12 Dhwaja house rules -- validator doesn't recognise Dhwaja as a valid
    # Upagraha in BPHS Ch25, but Santhanam translation explicitly includes
    # house-wise Dhwaja results. These are legitimate BPHS rules.
    "bphs1-ch25-055", "bphs1-ch25-056", "bphs1-ch25-057", "bphs1-ch25-058",
    "bphs1-ch25-059", "bphs1-ch25-060", "bphs1-ch25-061", "bphs1-ch25-062",
    "bphs1-ch25-063", "bphs1-ch25-064", "bphs1-ch25-065", "bphs1-ch25-066",
    # Uchcha Rasmi formula -- confirmed correct per TT-CH28-01 encode pass.
    # Validator applies a different formula variant than Santhanam source.
    "bphs1-ch28-002",
    # Parasparayogakaraka -- validator over-restricts to angular+dignity only.
    # Some BPHS commentaries support a dignity-based softened form.
    "bphs1-ch32-028",
]

BUCKET_B_NOTE = (
    "validator_error: validator applied non-Santhanam doctrinal standard; "
    "rule content is consistent with BPHS source text"
)

# ── Direct CC fixes ───────────────────────────────────────────────────────────

# bphs1-ch03-044: Sun does NOT own Cancer. Moon owns Cancer. Sun owns Leo only.
# The 'Note: Sun's second own sign Cancer' line is a Codex fabrication.
CH03_044_DETAILED_CORRECTED = (
    "Sun: Moolatrikona = Leo 0°-20°. "
    "Swakshetra (own sign) = Leo 20°-30°. "
    "Sun owns only Leo; there is no second own sign for the Sun."
)
CH03_044_SUMMARY_CORRECTED = (
    "Sun's dignities in Leo: First 20 degrees of Leo are Moolatrikona; "
    "the remaining 10 degrees (20°-30°) are own house (Swakshetra). "
    "Sun owns Leo only -- no second sign."
)
CH03_044_NOTE = (
    "CC direct fix: removed fabricated 'Sun owns Cancer' statement. "
    "Sun owns Leo only per standard BPHS and all classical sources. "
    "Moon owns Cancer."
)

# bphs1-ch32-033: PDF READ (Ch32 p.325 v.31-34) CONFIRMS wife IS a valid 2nd house
# signification in Ch32 context.  Santhanam's table p.325 explicitly lists:
#   "Jupiter: 2nd house (family, finance, wife etc.)"
# Sanskrit verse 31 includes "darakaraka" (wife indicator) in the 2nd house context.
# The PREVIOUS plan to remove "wife" was INCORRECT.
# Correct action: validator_error -- do NOT overwrite interpretation text.
CH32_033_NOTE_REVISED = (
    "CC PDF read (Ch32 p.325 v.31-34 Santhanam): 'wife' IS a valid 2nd house "
    "signification in Ch32 context.  Santhanam's translator table (p.325) explicitly "
    "states 'Jupiter: 2nd house (family, finance, wife etc.)'. Sanskrit verse 31 "
    "includes darakaraka (wife indicator) in the 2nd house bhava context. "
    "Validator error -- original rule content is correct per BPHS source. "
    "Note: 7th house (Venus) is the primary wife indicator; 2nd house secondary "
    "via Jupiter per Ch32 only."
)


class _Tee:
    def __init__(self, log_path: Path):
        log_path.parent.mkdir(parents=True, exist_ok=True)
        self._log = open(log_path, "w", encoding="utf-8")
        self._stdout = sys.__stdout__
    def write(self, data: str) -> None:
        self._stdout.write(data); self._stdout.flush()
        self._log.write(data); self._log.flush()
    def flush(self) -> None:
        self._stdout.flush(); self._log.flush()
    def close(self) -> None:
        self._log.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = "_dryrun" if args.dry_run else "_live"
    log_path = LOG_DIR / f"patch_bphs_vol1_phase2_flagged_{ts}{suffix}.log"
    tee = _Tee(log_path)
    sys.stdout = tee
    print("=" * 60)
    print(f"  LOG FILE: {log_path}")
    print("=" * 60)
    print()
    print("BPHS Vol 1 Phase 2 -- Flagged Rules Triage Patch")
    print(f"Batch: {BATCH_ID}")
    print(f"Mode : {'DRY RUN' if args.dry_run else 'LIVE'}")
    print()

    try:
        from pymongo import MongoClient
    except ImportError:
        print("pymongo required."); raise SystemExit(1)

    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10_000)
    col = client[args.db_name]["interpretation_rules"]
    now = datetime.now(timezone.utc).isoformat()

    patched_b = skipped_b = errors_b = 0
    patched_direct = skipped_direct = errors_direct = 0

    # ── Bucket B ──────────────────────────────────────────────────────────────
    print(f"── Bucket B ({len(BUCKET_B_RULES)} rules) → PHR + validator_error:true ──")
    for rule_id in BUCKET_B_RULES:
        doc = col.find_one(
            {"rule_id": rule_id, "source.batch_id": BATCH_ID},
            {"rule_id": 1, "approval_status": 1, "_id": 0},
        )
        if not doc:
            print(f"  [MISS]  {rule_id} -- not found in batch")
            skipped_b += 1
            continue
        if doc.get("approval_status") != "flagged":
            print(f"  [SKIP]  {rule_id} -- status={doc.get('approval_status')} (not flagged)")
            skipped_b += 1
            continue
        if args.dry_run:
            print(f"  [DRY]   {rule_id} → pending_human_review + validator_error:true")
            patched_b += 1
        else:
            try:
                r = col.update_one(
                    {"rule_id": rule_id, "source.batch_id": BATCH_ID},
                    {"$set": {
                        "approval_status": "pending_human_review",
                        "validator_error": True,
                        "validator_error_note": BUCKET_B_NOTE,
                        "triage_patched_at": now,
                        "triage_bucket": "B",
                    }},
                )
                if r.modified_count:
                    print(f"  [OK]    {rule_id} → pending_human_review")
                    patched_b += 1
                else:
                    print(f"  [SKIP]  {rule_id} -- 0 modified")
                    skipped_b += 1
            except Exception as exc:
                print(f"  [ERR]   {rule_id}: {exc}")
                errors_b += 1
    print()

    # ── Direct CC fix: bphs1-ch03-044 ─────────────────────────────────────────
    print("── Direct CC fix: bphs1-ch03-044 (Sun+Cancer factual error) ──")
    rule_id = "bphs1-ch03-044"
    doc = col.find_one(
        {"rule_id": rule_id, "source.batch_id": BATCH_ID},
        {"rule_id": 1, "approval_status": 1, "_id": 0},
    )
    if not doc:
        print(f"  [MISS]  {rule_id} -- not found")
        skipped_direct += 1
    elif args.dry_run:
        print(f"  [DRY]   {rule_id} → PHR + corrected Sun-sign text (remove 'Sun owns Cancer')")
        patched_direct += 1
    else:
        try:
            r = col.update_one(
                {"rule_id": rule_id, "source.batch_id": BATCH_ID},
                {"$set": {
                    "approval_status": "pending_human_review",
                    "interpretation.detailed": CH03_044_DETAILED_CORRECTED,
                    "interpretation.summary":  CH03_044_SUMMARY_CORRECTED,
                    "cc_fix_note": CH03_044_NOTE,
                    "triage_patched_at": now,
                    "triage_bucket": "C-direct",
                }},
            )
            if r.modified_count:
                print(f"  [OK]    {rule_id} → PHR + corrected text")
                patched_direct += 1
            else:
                print(f"  [SKIP]  {rule_id} -- 0 modified")
                skipped_direct += 1
        except Exception as exc:
            print(f"  [ERR]   {rule_id}: {exc}")
            errors_direct += 1
    print()

    # ── Direct CC fix: bphs1-ch32-033 ─────────────────────────────────────────
    # PDF READ CORRECTION: Ch32 p.325 CONFIRMS wife IS in 2nd house per source.
    # Original plan (remove 'wife') was wrong.  Treat as validator_error -- no
    # interpretation text changes, just promote to PHR with validator_error flag.
    print("── PDF fix: bphs1-ch32-033 (validator error -- wife in 2nd house IS in source) ──")
    rule_id = "bphs1-ch32-033"
    doc = col.find_one(
        {"rule_id": rule_id, "source.batch_id": BATCH_ID},
        {"rule_id": 1, "approval_status": 1, "_id": 0},
    )
    if not doc:
        print(f"  [MISS]  {rule_id} -- not found")
        skipped_direct += 1
    elif args.dry_run:
        print(f"  [DRY]   {rule_id} → PHR + validator_error:true (wife in 2nd house confirmed p.325)")
        patched_direct += 1
    else:
        try:
            r = col.update_one(
                {"rule_id": rule_id, "source.batch_id": BATCH_ID},
                {"$set": {
                    "approval_status": "pending_human_review",
                    "validator_error": True,
                    "validator_error_note": CH32_033_NOTE_REVISED,
                    "triage_patched_at": now,
                    "triage_bucket": "B-pdf",
                }},
            )
            if r.modified_count:
                print(f"  [OK]    {rule_id} → PHR + validator_error (no text change)")
                patched_direct += 1
            else:
                print(f"  [SKIP]  {rule_id} -- 0 modified")
                skipped_direct += 1
        except Exception as exc:
            print(f"  [ERR]   {rule_id}: {exc}")
            errors_direct += 1
    print()

    # ── Summary ───────────────────────────────────────────────────────────────
    total_patched = patched_b + patched_direct
    print("=" * 60)
    if args.dry_run:
        print(f"[DRY RUN] Would patch {total_patched} rules:")
        print(f"  Bucket B (validator_error → PHR) : {patched_b}")
        print(f"  Direct CC fix (corrected → PHR)  : {patched_direct}")
    else:
        print(f"Patch complete:")
        print(f"  Bucket B patched  : {patched_b} / {len(BUCKET_B_RULES)}")
        print(f"  Direct CC patched : {patched_direct}")
        print(f"  Skipped           : {skipped_b + skipped_direct}")
        print(f"  Errors            : {errors_b + errors_direct}")
        print()
        print(f"Batch status after patch:")
        for status in ["auto_approved", "pending_human_review", "flagged"]:
            n = col.count_documents({"source.batch_id": BATCH_ID,
                                      "approval_status": status})
            print(f"  {status:<30} {n}")
        remaining_flagged = col.count_documents({
            "source.batch_id": BATCH_ID, "approval_status": "flagged"
        })
        print()
        print(f"Remaining flagged: {remaining_flagged} (these go to PDF read / GAI queue)")

    client.close()


if __name__ == "__main__":
    main()
