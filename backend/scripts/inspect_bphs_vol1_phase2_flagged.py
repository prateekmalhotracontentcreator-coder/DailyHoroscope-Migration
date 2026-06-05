#!/usr/bin/env python3
"""inspect_bphs_vol1_phase2_flagged.py

Pulls all flagged rules from BPHS Vol 1 Phase 2 batch and produces a
triage-ready report classifying each rule as:

  Bucket A -- Truncation artifact only (summary too short, detailed OK)
              → auto-patch to auto_approved
  Bucket B -- Validator doctrinal error (validator made a wrong Vedic claim)
              → patch to PHR with validator_error:true
  Bucket C -- Genuine issue (Codex fabrication, formula conflict,
              factual error, extreme outcome, real contradiction)
              → stay flagged, export for GAI/TT queue

Also reports current counts for all approval_status values in the batch.

Usage:
  python3 backend/scripts/inspect_bphs_vol1_phase2_flagged.py \\
    --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

BATCH_ID = "bphs-vol1-phase2-v1-20260601"
LOG_DIR  = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")

# Validator flag reasons that are known doctrinal errors (Bucket B)
# These are patterns where the validator mis-applies rules to BPHS content
BUCKET_B_PATTERNS = [
    "natural malefic",
    "natural benefic",
    "chapa",
    "dhwaja",          # validator misclassifies Dhwaja yoga descriptions
    "moon in cancer",
    "sun in leo",
    "yoga karaka",
    "yogakaraka",
    "moolatrikona",
    "moola trikona",
    "exalt",
    "debili",
]

# Keywords in flag_reason / validation notes that suggest Bucket C
BUCKET_C_PATTERNS = [
    "fabricat",
    "invented",
    "not found in source",
    "no source",
    "extreme",
    "death",
    "formula conflict",
    "factual error",
    "non-standard",
    "contradicts",
    "contradiction",
]


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


def classify(rule: dict) -> str:
    """Return 'A', 'B', or 'C' bucket classification."""
    # Pull all available flag text
    flag_texts = []
    val = rule.get("validation") or {}
    if isinstance(val, dict):
        flag_texts.append(str(val.get("flag_reason", "")))
        flag_texts.append(str(val.get("flag_note", "")))
        flag_texts.append(str(val.get("issues", "")))
        flag_texts.append(str(val.get("note", "")))
        flag_texts.append(str(val.get("quality_note", "")))
    flag_texts.append(str(rule.get("flag_reason", "")))
    flag_texts.append(str(rule.get("flag_note", "")))
    combined = " ".join(flag_texts).lower()

    interp = rule.get("interpretation") or {}
    detailed  = str(interp.get("detailed", "") or "")
    summary   = str(interp.get("summary", "") or "")

    # Bucket A: summary is very short but detailed is OK
    # Only if no C-pattern and no other flag signal
    if (len(summary) < 30 and len(detailed) > 80
            and not any(p in combined for p in BUCKET_C_PATTERNS)
            and not any(p in combined for p in BUCKET_B_PATTERNS)):
        return "A"

    # Bucket B: validator doctrinal error signals
    if any(p in combined for p in BUCKET_B_PATTERNS):
        return "B"

    # Default to C for anything genuinely flagged
    return "C"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", default="horoscope_db")
    args = parser.parse_args()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"inspect_bphs_vol1_phase2_flagged_{ts}.log"
    tee = _Tee(log_path)
    sys.stdout = tee
    print("=" * 60)
    print(f"  LOG FILE: {log_path}")
    print("=" * 60)
    print()

    try:
        from pymongo import MongoClient
    except ImportError:
        print("pymongo required."); raise SystemExit(1)

    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10_000)
    col = client[args.db_name]["interpretation_rules"]

    # ── Batch summary ──────────────────────────────────────────────
    print(f"BATCH: {BATCH_ID}")
    print()
    for status in ["auto_approved", "pending_human_review", "pending_review",
                   "flagged", "rejected"]:
        n = col.count_documents({"source.batch_id": BATCH_ID,
                                  "approval_status": status})
        print(f"  {status:<30} {n}")
    total = col.count_documents({"source.batch_id": BATCH_ID})
    print(f"  {'TOTAL':<30} {total}")
    print()

    # ── Pull flagged rules ─────────────────────────────────────────
    flagged = list(col.find(
        {"source.batch_id": BATCH_ID, "approval_status": "flagged"},
        {"rule_id": 1, "source_chapter": 1, "validation": 1,
         "flag_reason": 1, "flag_note": 1,
         "interpretation.detailed": 1, "interpretation.summary": 1,
         "interpretation.tags": 1,
         "condition": 1, "_id": 0},
    ).sort("rule_id", 1))

    print(f"Flagged rules: {len(flagged)}")
    print()

    buckets: dict[str, list[dict]] = {"A": [], "B": [], "C": []}
    for rule in flagged:
        b = classify(rule)
        buckets[b].append(rule)

    # ── Bucket summary ─────────────────────────────────────────────
    print(f"Bucket A (truncation artifact → auto_approved): {len(buckets['A'])}")
    print(f"Bucket B (validator doctrinal error → PHR):     {len(buckets['B'])}")
    print(f"Bucket C (genuine issue → GAI/TT queue):        {len(buckets['C'])}")
    print()

    # ── Bucket A detail ───────────────────────────────────────────
    if buckets["A"]:
        print("─" * 60)
        print("BUCKET A -- Truncation artifacts (patch → auto_approved)")
        print("─" * 60)
        for r in buckets["A"]:
            interp = r.get("interpretation") or {}
            print(f"  {r['rule_id']}")
            print(f"    summary  : {str(interp.get('summary',''))[:120]}")
            print(f"    detailed : {str(interp.get('detailed',''))[:120]}")
            val = r.get("validation") or {}
            note = (val.get("flag_reason") or val.get("flag_note") or
                    val.get("quality_note") or r.get("flag_reason") or "")
            if note:
                print(f"    flag     : {str(note)[:200]}")
            print()

    # ── Bucket B detail ───────────────────────────────────────────
    if buckets["B"]:
        print("─" * 60)
        print("BUCKET B -- Validator doctrinal errors (patch → PHR + validator_error:true)")
        print("─" * 60)
        for r in buckets["B"]:
            interp = r.get("interpretation") or {}
            print(f"  {r['rule_id']}")
            print(f"    summary  : {str(interp.get('summary',''))[:120]}")
            val = r.get("validation") or {}
            note = (val.get("flag_reason") or val.get("flag_note") or
                    val.get("quality_note") or r.get("flag_reason") or "")
            if note:
                print(f"    flag     : {str(note)[:200]}")
            print()

    # ── Bucket C detail ───────────────────────────────────────────
    if buckets["C"]:
        print("─" * 60)
        print("BUCKET C -- Genuine issues (stay flagged, export for GAI/TT)")
        print("─" * 60)
        for r in buckets["C"]:
            interp = r.get("interpretation") or {}
            print(f"  {r['rule_id']}")
            print(f"    summary  : {str(interp.get('summary',''))[:140]}")
            print(f"    detailed : {str(interp.get('detailed',''))[:140]}")
            val = r.get("validation") or {}
            note = (val.get("flag_reason") or val.get("flag_note") or
                    val.get("quality_note") or r.get("flag_reason") or "")
            if note:
                print(f"    flag     : {str(note)[:300]}")
            tags = (interp.get("tags") or [])
            if tags:
                print(f"    tags     : {tags}")
            print()

    # ── Export Bucket C for GAI ────────────────────────────────────
    if buckets["C"]:
        gai_path = LOG_DIR / f"bphs_vol1_phase2_bucket_c_{ts}.json"
        gai_export = []
        for r in buckets["C"]:
            interp = r.get("interpretation") or {}
            val   = r.get("validation") or {}
            gai_export.append({
                "rule_id":    r["rule_id"],
                "chapter":    r.get("source_chapter", ""),
                "summary":    str(interp.get("summary", "") or ""),
                "detailed":   str(interp.get("detailed", "") or ""),
                "flag_reason": (val.get("flag_reason") or val.get("flag_note") or
                                val.get("quality_note") or r.get("flag_reason") or ""),
                "condition":  r.get("condition", {}),
                "tags":       interp.get("tags", []),
            })
        gai_path.write_text(
            json.dumps(gai_export, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        print(f"\nBucket C JSON export: {gai_path}")
        print(f"  → Upload to GAI with BPHS source PDF for doctrinal review")

    print()
    print("=" * 60)
    print("NEXT STEPS:")
    if buckets["A"]:
        print(f"  1. Patch {len(buckets['A'])} Bucket A rules → auto_approved")
        print(f"     (run patch_bphs_vol1_phase2_flagged.py --bucket A)")
    if buckets["B"]:
        print(f"  2. Patch {len(buckets['B'])} Bucket B rules → PHR + validator_error:true")
        print(f"     (run patch_bphs_vol1_phase2_flagged.py --bucket B)")
    if buckets["C"]:
        print(f"  3. Review {len(buckets['C'])} Bucket C rules via GAI")
        print(f"     Upload bphs_vol1_phase2_bucket_c_{ts}.json to GAI with BPHS PDF")
    print()
    print(f"Log saved: {log_path}")

    client.close()


if __name__ == "__main__":
    main()
