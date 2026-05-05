#!/usr/bin/env python3
"""
patch_lalkitab_ch28_flags.py

Inspects and (with --patch) patches the 1 flagged rule in the
lalkitab-ch28-v1-20260505 batch to pending_human_review.

1 flagged rule (Group A — content validity false flag):

  lalkitab-ch28-influence-priority
    Validator: "Three-step propagation sequence (natal house → enemy planets →
    friendly planets) is not a standard Vedic principle and appears to be a
    synthetic construct without clear classical basis."
    Resolution: False flag — this propagation rule is explicitly documented in
    both Ch 28 source files:
      - JSON Ready LM: "Influence Priority: A planet entering House 1 first
        influences its original natal house, then enemy planets, then friendly
        planets."
      - Diagnostic LM: Steps 1–4 detail the exact propagation sequence.
    Lal Kitab is a folk astrology text with its own Varshaphalam-specific
    mechanics that differ from classical Vedic jyotish. The validator is
    applying the wrong classical frame. Content is source-confirmed.
    Promoted to pending_human_review for co-founder source-fidelity confirmation.

Usage:
  # Inspect only (no changes):
  python3 scripts/patch_lalkitab_ch28_flags.py --mongo-url "$MONGO_URL"

  # Inspect + patch:
  python3 scripts/patch_lalkitab_ch28_flags.py --mongo-url "$MONGO_URL" --patch
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

BATCH_ID = "lalkitab-ch28-v1-20260505"

GROUP_A = {
    "lalkitab-ch28-influence-priority",
}

REASON_A = (
    "False flag — content validity dispute: validator claims the three-step propagation "
    "sequence (natal house → enemy planets → friendly planets) is non-classical. "
    "Rule is explicitly documented in both Ch 28 source files: "
    "JSON Ready LM lists 'Influence Priority' as a named annual chart principle; "
    "Diagnostic LM details the same sequence as Steps 1–4 of the Varshaphalam "
    "influence propagation logic. "
    "Lal Kitab is a folk astrology text with Varshaphalam-specific mechanics distinct "
    "from classical Vedic jyotish — the validator is applying the wrong classical frame. "
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
        grp = "A (content validity false flag)" if rid in GROUP_A else "UNKNOWN"
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
                "validation.validated_by": "patch_lalkitab_ch28_flags.py",
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
