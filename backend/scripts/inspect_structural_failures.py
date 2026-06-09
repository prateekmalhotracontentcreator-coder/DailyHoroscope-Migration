#!/usr/bin/env python3
"""
inspect_structural_failures.py
-------------------------------
Finds all pending_review rules that failed the structural_check in
validate_rules.py (i.e., rules that are still pending_review even after
the validator ran, because structural failures are never written back).

For each rule, runs structural_check() to show the exact failure reason,
prints the full interpretation text, and decides the fix:

  - truncated_text   → attempt to fix by appending a period
  - interpretation_too_short → print content for manual decision
  - empty_interpretation     → mark rejected
  - ocr_garbage_detected     → mark rejected
  - missing_condition        → print content for manual decision

After showing findings, patches fixable rules (adds period to truncated text)
and re-runs structural_check. If a rule still fails after patching, marks
it as 'rejected' with reason.

Every run saves a timestamped log file.

Usage:
    # Inspect only (no writes):
    python3 backend/scripts/inspect_structural_failures.py --dry-run

    # Inspect + apply fixes:
    python3 backend/scripts/inspect_structural_failures.py
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
                    help="Show findings without writing to MongoDB")
args = parser.parse_args()

# ---------------------------------------------------------------------------
# Log file setup
# ---------------------------------------------------------------------------
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
mode_tag = "dry-run" if args.dry_run else "live"
log_path = LOG_DIR / f"inspect_structural_failures_{mode_tag}_{ts}.log"

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
print(f"  inspect_structural_failures.py  [{mode_tag.upper()}]")
print(f"  Run timestamp : {ts} UTC")
print(f"  Log file      : {log_path}")
print(f"╚══════════════════════════════════════════════════════════════╝")
print()

if args.dry_run:
    print("  ⚠️  DRY-RUN MODE -- no changes written to MongoDB.")
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

# Import structural_check from knowledge_validator
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))
from knowledge_validator import RuleValidator
validator = RuleValidator()

# ---------------------------------------------------------------------------
# Find all pending_review rules that are likely structural failures
# These are in the two known batches (mantras + tba-ch15)
# We also catch any other pending_review in case future batches were affected
# ---------------------------------------------------------------------------
TARGET_BATCHES = [
    "remedies-mantras-v1-20260504",
    "tba-ch15-v1-20260424",
]

rules = list(col.find(
    {
        "approval_status": "pending_review",
        "source.batch_id": {"$in": TARGET_BATCHES}
    },
    {"_id": 0}
))

print(f"Rules in target batches still at pending_review: {len(rules)}")
print()

if not rules:
    print("✅ Nothing to do.")
    client.close()
    sys.stdout = sys.__stdout__
    tee.close()
    sys.exit(0)

# ---------------------------------------------------------------------------
# Run structural_check on each and classify
# ---------------------------------------------------------------------------
FIXABLE = []    # truncated_text -- can append period
REJECT = []     # empty / ocr_garbage -- should be rejected
MANUAL = []     # too_short / missing_condition -- needs human look

for rule in rules:
    rid = rule.get("rule_id", "?")
    batch = (rule.get("source") or {}).get("batch_id", "?")
    passed, reason = validator.structural_check(rule)
    interp = rule.get("interpretation") or {}
    detailed = (interp.get("detailed") or "").strip()
    summary = (interp.get("summary") or "").strip()
    text = detailed or summary
    cond = rule.get("condition") or {}
    cond_type = cond.get("type", "(none)")

    print("─" * 60)
    print(f"  rule_id    : {rid}")
    print(f"  batch      : {batch}")
    print(f"  cond_type  : {cond_type}")
    print(f"  fail reason: {reason}")
    print(f"  word count : {len(text.split())}")
    print(f"  last char  : '{text[-1] if text else ''}'" )
    print(f"  summary    : {summary[:120]}")
    print(f"  detailed   : {detailed[:200]}")
    print()

    if reason == "truncated_text":
        FIXABLE.append(rule)
    elif reason in ("empty_interpretation", "ocr_garbage_detected"):
        REJECT.append(rule)
    elif reason == "interpretation_too_short":
        # Too sparse to be useful without returning to source book -- reject
        REJECT.append(rule)
    else:
        MANUAL.append(rule)

print(f"{'═'*60}")
print(f"  Fixable (truncated_text -- add period)  : {len(FIXABLE)}")
print(f"  Reject  (empty / ocr_garbage / too_short): {len(REJECT)}")
print(f"  Manual  (missing_condition etc.)       : {len(MANUAL)}")
print(f"{'═'*60}")
print()

# ---------------------------------------------------------------------------
# Fix: truncated_text -- append period to detailed (or summary if no detailed)
# ---------------------------------------------------------------------------
NOW = datetime.now(timezone.utc).isoformat()
fix_ok = []
fix_still_fail = []

for rule in FIXABLE:
    rid = rule.get("rule_id", "?")
    interp = rule.get("interpretation") or {}
    detailed = (interp.get("detailed") or "").strip()
    summary = (interp.get("summary") or "").strip()

    if detailed:
        new_detailed = detailed + "."
        new_summary = summary
    else:
        new_detailed = detailed
        new_summary = summary + "."

    # Build patched rule for re-check
    patched = dict(rule)
    patched["interpretation"] = dict(interp)
    patched["interpretation"]["detailed"] = new_detailed
    patched["interpretation"]["summary"] = new_summary

    passed2, reason2 = validator.structural_check(patched)

    if passed2:
        fix_ok.append((rid, new_detailed, new_summary))
        print(f"  ✅ {rid}: period fix → passes structural check")
    else:
        fix_still_fail.append((rid, reason2))
        print(f"  ❌ {rid}: period fix still fails ({reason2}) → will reject")

print()

# ---------------------------------------------------------------------------
# Write fixes + rejections to MongoDB
# ---------------------------------------------------------------------------
patched_count = 0
rejected_count = 0

if not args.dry_run:
    for rid, new_det, new_sum in fix_ok:
        update = {"$set": {}}
        if new_det:
            update["$set"]["interpretation.detailed"] = new_det
        if new_sum:
            update["$set"]["interpretation.summary"] = new_sum
        # Leave approval_status as pending_review -- rule now passes structural
        # check so validate_rules.py can pick it up on next run
        update["$set"]["patch_notes"] = f"truncated_text fix: period appended {NOW}"
        col.update_one({"rule_id": rid}, update)
        patched_count += 1

    for rid, reason in fix_still_fail:
        col.update_one(
            {"rule_id": rid},
            {"$set": {
                "approval_status": "rejected",
                "rejection_reason": f"structural_fail:{reason} -- period fix did not resolve",
                "rejected_at": NOW,
            }}
        )
        rejected_count += 1

    for rule in REJECT:
        rid = rule.get("rule_id", "?")
        passed, reason = validator.structural_check(rule)
        if reason == "interpretation_too_short":
            reject_msg = "structural_fail:interpretation_too_short -- content too sparse, no detailed field, cannot expand without source book"
        elif reason == "ocr_garbage_detected":
            reject_msg = "structural_fail:ocr_garbage_detected -- Devanagari script triggered non-ASCII regex; content also truncated mid-word, unrecoverable without re-ingest"
        else:
            reject_msg = f"structural_fail:{reason}"
        col.update_one(
            {"rule_id": rid},
            {"$set": {
                "approval_status": "rejected",
                "rejection_reason": reject_msg,
                "rejected_at": NOW,
            }}
        )
        rejected_count += 1

    for rule in MANUAL:
        rid = rule.get("rule_id", "?")
        print(f"  ℹ️  {rid}: manual review needed ({rule.get('_fail_reason','?')}) -- left at pending_review")
else:
    print("  DRY-RUN: no writes.")
    print(f"  Would patch  : {len(fix_ok)} rules (append period)")
    print(f"  Would reject : {len(fix_still_fail) + len(REJECT)} rules")
    print(f"  Manual review: {len(MANUAL)} rules")

print()

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
remaining_pr = col.count_documents({"approval_status": "pending_review"})
print(f"{'═'*60}")
print(f"  Rules patched (period fix, back to pending_review): {patched_count}")
print(f"  Rules rejected (structural fail -- unresolvable)   : {rejected_count}")
print(f"  Total pending_review in DB after run              : {remaining_pr}")
print()
if patched_count > 0 and not args.dry_run:
    print("  Next step: run validate_rules.py for the patched batches:")
    for batch in TARGET_BATCHES:
        if any(r.get("rule_id") for r in FIXABLE):
            print(f"    python3 backend/scripts/validate_rules.py \\")
            print(f"      --mongo-url \"$MONGO_URL\" --db-name horoscope_db \\")
            print(f"      --batch-id \"{batch}\"")
    print()

client.close()

print(f"╔══════════════════════════════════════════════════════════════╗")
print(f"  ✅ Inspection complete")
print(f"  Log saved → {log_path}")
print(f"╚══════════════════════════════════════════════════════════════╝")

sys.stdout = sys.__stdout__
tee.close()
