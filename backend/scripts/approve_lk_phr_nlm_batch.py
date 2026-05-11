#!/usr/bin/env python3
"""
approve_lk_phr_nlm_batch.py

Applies NLM decisions from: Lal Kitab de-code_CC additional Queries_144 Rules.md
Dated: 2026-05-11

Three action groups:

  Group 1 — BULK APPROVE (25 rules): Truncation false flags. Content complete.
  Group 2 — APPROVE + SPLIT NOTE (5 rules): Source-faithful but OR-logic needs
             splitting into separate rule IDs. Approved for engine; split_required
             flag set so a future cleanup pass can split them.
  Group 3 — APPROVE (114 rules): Source-confirmed folk/physiognomy teachings.
             Validator's "non-classical Vedic" objections overruled by primary text.

Usage:
  python3 backend/scripts/approve_lk_phr_nlm_batch.py            # dry-run
  python3 backend/scripts/approve_lk_phr_nlm_batch.py --apply    # write to DB
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone

REVIEWER   = "NLM — Lal Kitab de-code_CC additional Queries_144 Rules (2026-05-11)"
COLLECTION = "interpretation_rules"

# ── Group 1: Bulk Approve — Truncation False Flags (25 rules) ─────────────────
GROUP1_TRUNCATION: list[str] = [
    # CH19
    "lalkitab-ch19-075", "lalkitab-ch19-076", "lalkitab-ch19-077", "lalkitab-ch19-078",
    # CH20
    "lalkitab-ch20-dos-jupiter", "lalkitab-ch20-dos-saturn", "lalkitab-ch20-gp-interact",
    "lalkitab-ch20-gp-seq", "lalkitab-ch20-gp-sign", "lalkitab-ch20-met-succession",
    "lalkitab-ch20-trial-charity",
    # CH21
    "lalkitab-ch21-debt-jupiter", "lalkitab-ch21-debt-mercury",
    "lalkitab-ch21-debt-moon", "lalkitab-ch21-debt-sun",
    # CH22
    "lalkitab-ch22-ctx-04",
    # CH23
    "lalkitab-ch23-formula-remainder",
    # CH25
    "lalkitab-ch25-mars-mercury-sister", "lalkitab-ch25-moon-h11",
    "lalkitab-ch25-saturn-h10-h4-benefit", "lalkitab-ch25-significators-aries-base",
    "lalkitab-ch25-sun-affliction",
    # CH26
    "lalkitab-ch26-mars-debilitation", "lalkitab-ch26-mercury-debilitation",
    "lalkitab-ch26-venus-debilitation",
]

# ── Group 2: Approve + Split Required (5 rules) ───────────────────────────────
GROUP2_SPLIT: dict[str, str] = {
    "lalkitab-ch21-fam-04": (
        "Split into two rules: (1) '40–43 consecutive days' condition; "
        "(2) '1 day/week for 40–43 weeks' condition."
    ),
    "lalkitab-ch24-age-childhood-12m": (
        "Split: (1) 'Sun+Saturn in Jupiter's house' branch; "
        "(2) 'unfriendly male planet' branch."
    ),
    "lalkitab-ch24-age-infancy-12d": (
        "Split: (1) 'Moon H6 + Sun H10' condition; "
        "(2) 'Moon+Ketu H6' condition."
    ),
    "lalkitab-ch24-age-shortlife-2y": (
        "Split: (1) 'Jupiter H8–11 + H7 cluster'; "
        "(2) 'H5 planetary cluster'."
    ),
    "lalkitab-ch24-age-survival-son": (
        "Separate planetary condition (Moon/Rahu H6) from physical physiognomy markers "
        "into two distinct rules."
    ),
}

# ── Group 3: Approve — Source Confirmed (114 rules) ──────────────────────────
# Identified by chapter batch prefix; we query the DB rather than listing all 114
# to avoid hardcoding errors. The filter is:
#   source.batch_id in the lalkitab chapters listed
#   approval_status = pending_human_review
#   rule_id NOT IN group1 + group2 keys
GROUP3_BATCHES: list[str] = [
    "lalkitab-ch19-",
    "lalkitab-ch20-",
    "lalkitab-ch21-",
    "lalkitab-ch22-",
    "lalkitab-ch23-",
    "lalkitab-ch24-",
    "lalkitab-ch25-",
    "lalkitab-ch26-",
    "lalkitab-ch27-",
]

GROUP3_APPROVAL_NOTE = (
    "Source confirmed by NLM review (2026-05-11). Validator's 'non-classical Vedic' "
    "objections overruled — Lal Kitab is a folk-astrological text; these teachings "
    "are verified against the primary Lal Kitab source chapters."
)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply NLM LK PHR decisions (144 rules)")
    parser.add_argument("--mongo-url", default=os.environ.get("MONGO_URL", ""))
    parser.add_argument("--db-name",   default=os.environ.get("DB_NAME", "horoscope_db"))
    parser.add_argument("--apply",     action="store_true",
                        help="Write changes to DB. Omit for dry-run.")
    args = parser.parse_args()

    if not args.mongo_url:
        print("[ERROR] --mongo-url required (or set MONGO_URL env var)", file=sys.stderr)
        sys.exit(1)

    from pymongo import MongoClient, UpdateOne
    client = MongoClient(args.mongo_url)
    col    = client[args.db_name][COLLECTION]
    now    = stamp()
    mode   = "APPLY" if args.apply else "DRY-RUN"
    print(f"[{mode}] Starting NLM batch approval — {now}\n")

    ops: list[UpdateOne] = []

    # ── Group 1 ───────────────────────────────────────────────────────────────
    print(f"Group 1 — Truncation False Flags: {len(GROUP1_TRUNCATION)} rules")
    for rid in GROUP1_TRUNCATION:
        exists = col.find_one({"rule_id": rid}, {"rule_id": 1})
        status = "FOUND" if exists else "NOT FOUND"
        print(f"  [{status}] {rid}")
        if exists:
            ops.append(UpdateOne(
                {"rule_id": rid},
                {"$set": {
                    "approval_status":         "approved",
                    "validation.approved_by":  REVIEWER,
                    "validation.approved_at":  now,
                    "validation.approved_note": (
                        "Bulk approved — truncation false flag confirmed by NLM. "
                        "Content is complete and source-faithful."
                    ),
                }},
            ))

    print()

    # ── Group 2 ───────────────────────────────────────────────────────────────
    print(f"Group 2 — Approve + Split Required: {len(GROUP2_SPLIT)} rules")
    for rid, split_note in GROUP2_SPLIT.items():
        exists = col.find_one({"rule_id": rid}, {"rule_id": 1})
        status = "FOUND" if exists else "NOT FOUND"
        print(f"  [{status}] {rid}")
        print(f"           Split: {split_note[:80]}…")
        if exists:
            ops.append(UpdateOne(
                {"rule_id": rid},
                {"$set": {
                    "approval_status":              "approved",
                    "validation.approved_by":       REVIEWER,
                    "validation.approved_at":       now,
                    "validation.approved_note":     (
                        "Approved — source-faithful. OR-logic compound condition "
                        "requires splitting. See split_instructions."
                    ),
                    "validation.split_required":    True,
                    "validation.split_instructions": split_note,
                }},
            ))

    print()

    # ── Group 3 ───────────────────────────────────────────────────────────────
    exclude_ids = set(GROUP1_TRUNCATION) | set(GROUP2_SPLIT.keys())
    batch_regex = "|".join(GROUP3_BATCHES)
    group3_rules = list(col.find(
        {
            "science_id":      "jyotish",
            "approval_status": "pending_human_review",
            "source.batch_id": {"$regex": "^(" + batch_regex + ")"},
            "rule_id":         {"$nin": list(exclude_ids)},
        },
        {"rule_id": 1, "_id": 0},
    ))
    print(f"Group 3 — Source Confirmed: {len(group3_rules)} rules (expected ~114)")
    for r in group3_rules:
        rid = r["rule_id"]
        print(f"  {rid}")
        ops.append(UpdateOne(
            {"rule_id": rid},
            {"$set": {
                "approval_status":         "approved",
                "validation.approved_by":  REVIEWER,
                "validation.approved_at":  now,
                "validation.approved_note": GROUP3_APPROVAL_NOTE,
            }},
        ))

    print()
    print(f"Total ops queued: {len(ops)}")

    if not args.apply:
        print(f"\n[DRY-RUN] No changes written. Re-run with --apply to commit.")
        client.close()
        return

    if ops:
        result = col.bulk_write(ops, ordered=False)
        print(f"[OK] Modified: {result.modified_count} | Matched: {result.matched_count}")
    else:
        print("[WARN] No ops to apply.")

    client.close()


if __name__ == "__main__":
    main()
