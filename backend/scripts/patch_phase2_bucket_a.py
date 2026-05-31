#!/usr/bin/env python3
"""
patch_phase2_bucket_a.py
------------------------------------------------------------------------
Phase 2 validation triage -- Bucket A (19 rules)

Summary truncation only; Claude confirmed detailed text is coherent and
correct. Fix: replace truncated interpretation.summary with a clean
word-boundary truncation of interpretation.detailed, then promote to
auto_approved.

Rules: bphs1-ch03-{030,033,036,039,040} | ch04-{006,008,009,010,011,012,015,016,018}
       ch09-007 | ch26-003 | ch28-{010,011,014}

Run:
  python3 backend/scripts/patch_phase2_bucket_a.py \
    --mongo-url "$MONGO_URL" --db-name horoscope_db          # dry run
  python3 backend/scripts/patch_phase2_bucket_a.py \
    --mongo-url "$MONGO_URL" --db-name horoscope_db --apply  # apply
"""

import argparse, os, sys
from datetime import datetime, timezone

BUCKET_A_IDS = [
    "bphs1-ch03-030", "bphs1-ch03-033", "bphs1-ch03-036",
    "bphs1-ch03-039", "bphs1-ch03-040",
    "bphs1-ch04-006", "bphs1-ch04-008", "bphs1-ch04-009",
    "bphs1-ch04-010", "bphs1-ch04-011", "bphs1-ch04-012",
    "bphs1-ch04-015", "bphs1-ch04-016", "bphs1-ch04-018",
    "bphs1-ch09-007",
    "bphs1-ch26-003",
    "bphs1-ch28-010", "bphs1-ch28-011", "bphs1-ch28-014",
]


def clean_summary(detailed: str, max_chars: int = 200) -> str:
    """Return first max_chars of detailed, truncated at last word boundary."""
    if not detailed:
        return ""
    text = detailed.strip()
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars].rsplit(" ", 1)[0].rstrip(",;:")
    return cut


def main():
    parser = argparse.ArgumentParser(
        description="Bucket A: fix summary truncation → auto_approved"
    )
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument("--apply", action="store_true",
                        help="Write changes (default: dry run)")
    args = parser.parse_args()

    if not args.mongo_url:
        sys.exit("❌ --mongo-url required")

    from pymongo import MongoClient
    col = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10000)[args.db_name]["interpretation_rules"]

    now = datetime.now(timezone.utc).isoformat()
    patched = 0
    skipped = 0
    missing = []

    print(f"\n{'='*70}")
    print(f"BUCKET A PATCH -- {len(BUCKET_A_IDS)} rules → auto_approved + summary fix")
    print(f"{'='*70}")
    print(f"Mode: {'APPLY' if args.apply else 'DRY RUN'}\n")

    for rid in BUCKET_A_IDS:
        doc = col.find_one({"rule_id": rid}, {"_id": 0, "interpretation": 1,
                                               "approval_status": 1})
        if not doc:
            missing.append(rid)
            print(f"  ⚠  NOT FOUND: {rid}")
            continue

        interp   = doc.get("interpretation") or {}
        detailed = (interp.get("detailed") or "").strip()
        old_sum  = (interp.get("summary") or "").strip()
        new_sum  = clean_summary(detailed)

        if not detailed:
            print(f"  ⚠  {rid}: detailed is empty -- skipping")
            skipped += 1
            continue

        print(f"  {rid}")
        print(f"    old summary: {repr(old_sum[:60])}")
        print(f"    new summary: {repr(new_sum[:60])}")

        if args.apply:
            col.update_one(
                {"rule_id": rid},
                {"$set": {
                    "approval_status":    "auto_approved",
                    "interpretation.summary": new_sum,
                    "validation.verdict":     "approve",
                    "validation.flag_reason": (
                        "Bucket A patch 2026-06-01: summary truncation artifact corrected. "
                        "Detailed text confirmed correct by Claude quality check. "
                        "Summary replaced with clean truncation of detailed text."
                    ),
                    "validation.validated_at": now,
                }}
            )
            patched += 1
        else:
            patched += 1  # count for dry-run report

    print(f"\n{'─'*70}")
    print(f"  Would patch / Patched : {patched}")
    print(f"  Skipped (no detailed) : {skipped}")
    print(f"  Missing in DB         : {len(missing)}")
    if not args.apply:
        print(f"\n[DRY RUN] No changes written. Re-run with --apply.")
    else:
        print(f"\n✅ Done. {patched} rules → auto_approved.")


if __name__ == "__main__":
    main()
