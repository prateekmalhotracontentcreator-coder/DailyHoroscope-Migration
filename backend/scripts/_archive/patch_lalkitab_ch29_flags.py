#!/usr/bin/env python3
"""
patch_lalkitab_ch29_flags.py

Inspects and (with --patch) patches the 2 flagged rules in the
lalkitab-ch29-v1-20260505 batch to pending_human_review.

2 flagged rules (Group A — validator reading-window truncation false flags):
  Both rules have complete text in the DB. The validator's read buffer cut off
  mid-display, triggering a spurious "truncation" flag. Content is source-confirmed.

  lalkitab-ch29-arch-lion
    Validator saw "...Trigger 3 (weight 0.5): eye" — buffer artifact.
    Full text confirms: weighted Lion Archetype across 3 body parts
    (fleshy elbows + strong fleshy thighs + fierce lion-like eyes), score
    threshold 1.0, result = Maximum Financial Prosperity and Courage.
    Sourced from JSON_AI_Mode_Final + Diagnostic cross-cutting archetype schema.

  lalkitab-ch29-generational-wealth
    Validator saw "...so the KE can perform multi-generational wealt" — buffer artifact.
    Full text confirms: black and soft hair → triple-generational wealth
    (Father, Native, Son), HIGH PRIORITY flag, standalone rule surfacing the
    family continuity dimension from ch29-hair-traits.
    Sourced from Diagnostic_LM "Family Prosperity Continuity Logic" section.

Usage:
  # Inspect only (no changes):
  python3 scripts/patch_lalkitab_ch29_flags.py --mongo-url "$MONGO_URL"

  # Inspect + patch:
  python3 scripts/patch_lalkitab_ch29_flags.py --mongo-url "$MONGO_URL" --patch
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

BATCH_ID = "lalkitab-ch29-v1-20260505"

GROUP_A = {
    "lalkitab-ch29-arch-lion",
    "lalkitab-ch29-generational-wealth",
}

REASON_A = (
    "False flag — validator reading-window truncation artifact: text appears cut off in "
    "validator's read buffer but is complete in the database. "
    "arch-lion: full weighted Lion Archetype text present — 3 body-part triggers "
    "(fleshy elbows, strong fleshy thighs, fierce eyes), score threshold 1.0, confirmed "
    "in Ch 29 JSON_AI_Mode_Final + Diagnostic cross-cutting archetype schema. "
    "generational-wealth: full Family Prosperity Continuity text present — black+soft hair "
    "→ triple-generational wealth (Father/Native/Son), confirmed in Diagnostic_LM "
    "'Family Prosperity Continuity Logic' section. "
    "Promoted to pending_human_review for co-founder source-fidelity confirmation."
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--patch",     action="store_true",
                        help="Apply patches. Omit to inspect only.")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]
    now    = datetime.now(timezone.utc).isoformat()

    # ── Inspect flagged rules ─────────────────────────────────────────────────
    flagged = list(col.find(
        {"source.batch_id": BATCH_ID, "approval_status": "flagged"},
        {"_id": 0, "rule_id": 1, "interpretation.summary": 1,
         "validation.flag_reason": 1},
    ))

    print(f"\nFlagged rules: {len(flagged)} in {BATCH_ID}\n{'─'*70}")
    for r in flagged:
        rid = r["rule_id"]
        grp = "A (truncation false flag)" if rid in GROUP_A else "UNKNOWN"
        print(f"\n  [{grp}] {rid}")
        print(f"    {r['interpretation']['summary']}")
        flag = r.get("validation", {}).get("flag_reason", "n/a")
        print(f"    Flag: {flag[:120]}...")

    if not args.patch:
        print(f"\n{'─'*70}")
        print("── Inspect-only mode. Re-run with --patch to apply patches. ──")
        client.close()
        return

    # ── Patch flagged rules ───────────────────────────────────────────────────
    print(f"\n\n── Patching flagged rules ──\n")
    patched = 0
    for r in flagged:
        rid    = r["rule_id"]
        reason = REASON_A if rid in GROUP_A else "Unknown category — manual review required."
        result = col.update_one(
            {"rule_id": rid},
            {"$set": {
                "approval_status":         "pending_human_review",
                "validation.verdict":      "spot_check",
                "validation.flag_reason":  reason,
                "validation.validated_by": "patch_lalkitab_ch29_flags.py",
                "validation.validated_at": now,
            }},
        )
        if result.modified_count:
            print(f"  ✅ patched [{rid}]")
            patched += 1
        else:
            print(f"  ⚠️  No change: {rid}")

    print(f"\n{patched} / {len(flagged)} rules patched → pending_human_review")
    client.close()


if __name__ == "__main__":
    main()
