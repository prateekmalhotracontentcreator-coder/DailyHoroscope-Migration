#!/usr/bin/env python3
"""
triage_remedies_flagged.py
---------------------------
Triages flagged rules in the Remedies batches (Crystals, Gemstones, Chakra, Dhana).

Two categories:

  BUCKET B -- Framework mismatch (validator_error):
    Validator applied classical Vedic standards to a modern remedy library.
    Flag reason contains keywords like "non-Vedic", "not classical", "not a
    classical Vedic gemstone", etc. These are NOT genuine content errors.
    Action: approval_status → pending_human_review, validator_error: true

  BUCKET C -- Genuine issues (keep flagged, TT review):
    Actual data errors: condition/houses_involved mismatch, truncated text,
    pseudo-science phrases, wrong mantra for wrong planet, etc.
    Action: no change, stays flagged.

Every run saves a timestamped log.

Usage:
    # Dry-run (no writes):
    python3 backend/scripts/triage_remedies_flagged.py --dry-run

    # Live:
    python3 backend/scripts/triage_remedies_flagged.py
"""

from __future__ import annotations
import argparse
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from pymongo import MongoClient

# ---------------------------------------------------------------------------
# Args + logging
# ---------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
mode_tag = "dry-run" if args.dry_run else "live"
log_path = LOG_DIR / f"triage_remedies_flagged_{mode_tag}_{ts}.log"

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

print(f"╔══════════════════════════════════════════════════════════════╗")
print(f"  triage_remedies_flagged.py  [{mode_tag.upper()}]")
print(f"  Run timestamp : {ts} UTC")
print(f"  Log file      : {log_path}")
print(f"╚══════════════════════════════════════════════════════════════╝")
print()

if args.dry_run:
    print("  ⚠️  DRY-RUN -- no changes written to MongoDB.")
    print()

# ---------------------------------------------------------------------------
# Framework-mismatch keywords → Bucket B (promote to PHR)
# If flag_reason (lowercase) contains ANY of these → Bucket B
# ---------------------------------------------------------------------------
BUCKET_B_KEYWORDS = [
    # Broad crystal remedy framework flags (catches "...but crystal remedies..." patterns)
    "crystal remedies",              # any flag mentioning "crystal remedies" (non-Vedic framework)
    "crystal remedy",                # singular -- "crystal remedy framework/systems"
    # Specific non-Vedic / non-classical phrases
    "not part of classical vedic",
    "non-classical source",
    "is not a classical",            # broad -- "is not a classical Vedic gemstone/yoga/Venus gemstone etc."
    "is not a recognized vedic",
    "is not a standard vedic",
    "is not a primary vedic",
    "is not a recognized classical vedic",
    "is a modern/new age stone",
    "is a modern crystal with no classical",
    "no classical vedic",            # broad -- covers "no classical Vedic authority/precedent/provenance/foundation"
    "classical vedic precedent",     # catches "lacks classical Vedic precedent" too
    "not a recognized vedic",
    "not found in classical vedic texts",
    # Chakra framework flags
    "non-classical source and modern chakra",
    "seven chakra healing remedy library",
    "chakra-based interpretations are not part",
    "chakra-crystal healing",
    # Validator's own doctrinal error on dhana-005
    # (validator wrongly states "Jupiter exalted in Capricorn" -- Jupiter is DEBILITATED in Capricorn)
    "exalted in capricorn",
    # Modern / New Age language
    "new age",
]

# Genuine error keywords → Bucket C (keep flagged)
BUCKET_C_KEYWORDS = [
    "condition mismatch",
    "houses_involved lists",
    "direct contradiction in the data",
    "truncated",
    "incomplete",
    "pseudo-science",
    "incoherent and medic",
    "vampiric",
    "contradicts stated",
    "mismatched to",
    "conflicts with",
    "non-standard; classical vedic",  # e.g. start day conflicts
    "shanda",
    "mismatch in condition vs",
]

def classify(flag_reason: str) -> str:
    """Return 'B' (promote to PHR) or 'C' (keep flagged)."""
    r = flag_reason.lower()
    for kw in BUCKET_B_KEYWORDS:
        if kw.lower() in r:
            return "B"
    for kw in BUCKET_C_KEYWORDS:
        if kw.lower() in r:
            return "C"
    # Default: keep flagged (conservative)
    return "C"

# ---------------------------------------------------------------------------
# Connect
# ---------------------------------------------------------------------------
MONGO_URL = os.environ.get("MONGO_URL")
if not MONGO_URL:
    print("ERROR: MONGO_URL not set."); sys.exit(1)

client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=10_000)
col = client["horoscope_db"]["interpretation_rules"]

REMEDY_BATCHES = [
    "remedies-crystals-v1-20260510",
    "remedies-gemstones-v1-20260510",
    "remedies-chakra-v1-20260510",
    "remedies-dhana-v1-20260510",
]

NOW = datetime.now(timezone.utc).isoformat()
total_b = 0
total_c = 0
total_unclassified = 0

BATCH_SUMMARY: dict[str, dict] = {}

for batch_id in REMEDY_BATCHES:
    flagged = list(col.find(
        {"source.batch_id": batch_id, "approval_status": "flagged"},
        {"rule_id": 1, "validation": 1, "_id": 0}
    ))

    b_rules = []
    c_rules = []
    unclassified = []

    for r in flagged:
        rid = r.get("rule_id", "?")
        val = r.get("validation") or {}
        reason = val.get("flag_reason") or val.get("reason") or ""
        bucket = classify(reason)
        if bucket == "B":
            b_rules.append((rid, reason))
        elif bucket == "C":
            c_rules.append((rid, reason))
        else:
            unclassified.append((rid, reason))

    BATCH_SUMMARY[batch_id] = {
        "total_flagged": len(flagged),
        "bucket_b": len(b_rules),
        "bucket_c": len(c_rules),
        "unclassified": len(unclassified),
    }

    label = batch_id.replace("remedies-", "").replace("-v1-20260510", "").capitalize()
    print(f"{'─'*60}")
    print(f"  {label} ({batch_id})")
    print(f"  Total flagged : {len(flagged)}")
    print(f"  Bucket B (→ PHR, framework mismatch): {len(b_rules)}")
    print(f"  Bucket C (keep flagged, TT review)  : {len(c_rules)}")
    if unclassified:
        print(f"  Unclassified (defaulted to C)       : {len(unclassified)}")

    if c_rules:
        print(f"\n  Bucket C rules (TT review queue):")
        for rid, reason in c_rules:
            print(f"    {rid}: {reason[:100]}")
    if unclassified:
        print(f"\n  Unclassified rules:")
        for rid, reason in unclassified:
            print(f"    {rid}: {reason[:100]}")
    print()

    total_b += len(b_rules)
    total_c += len(c_rules)
    total_unclassified += len(unclassified)

    # Apply changes
    if not args.dry_run:
        for rid, _ in b_rules:
            col.update_one(
                {"rule_id": rid},
                {"$set": {
                    "approval_status": "pending_human_review",
                    "validation.verdict": "spot_check",
                    "validation.validator_error": True,
                    "validation.triage_note": (
                        "Bucket B: validator applied classical Vedic criteria to a modern "
                        "remedy library -- framework mismatch, not a content error. "
                        f"Triaged {NOW}"
                    ),
                }}
            )

print(f"{'═'*60}")
print(f"  SUMMARY")
print(f"{'═'*60}")
print(f"  Batch                    Flagged  → PHR   Stay flagged")
for batch_id, s in BATCH_SUMMARY.items():
    label = batch_id.split("-")[1].capitalize()
    print(f"  {label:<24} {s['total_flagged']:>7}  {s['bucket_b']:>5}   {s['bucket_c']:>5} {'(+' + str(s['unclassified']) + ' unclassified→C)' if s['unclassified'] else ''}")
print(f"  {'─'*50}")
print(f"  {'TOTAL':<24} {total_b+total_c+total_unclassified:>7}  {total_b:>5}   {total_c+total_unclassified:>5}")
print()

if args.dry_run:
    print(f"  DRY-RUN: no writes. Re-run without --dry-run to apply.")
else:
    print(f"  ✅ {total_b} rules promoted to pending_human_review (Bucket B)")
    print(f"  ✅ {total_c + total_unclassified} rules remain flagged (Bucket C -- TT review)")
    remaining = col.count_documents({
        "approval_status": "flagged",
        "source.batch_id": {"$in": REMEDY_BATCHES}
    })
    print(f"  Flagged remaining in Remedies batches: {remaining}")
print()

client.close()

print(f"╔══════════════════════════════════════════════════════════════╗")
print(f"  ✅ Triage complete")
print(f"  Log saved → {log_path}")
print(f"╚══════════════════════════════════════════════════════════════╝")

sys.stdout = sys.__stdout__
tee.close()
