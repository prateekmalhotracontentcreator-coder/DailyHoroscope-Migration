#!/usr/bin/env python3
"""
patch_lalkitab_ch25_flags.py

Inspects and (with --patch) patches all flagged rules and the false contradiction
pair in the lalkitab-ch25-v1-20260505 batch to pending_human_review.

2 flagged rules (Group A — validator reading-window truncation false flags):
  Both rules have complete text in the DB. The validator's read buffer cut off
  mid-display, triggering a spurious "truncation" flag. Content is source-confirmed.

    lalkitab-ch25-moon-h11
      52-day birth protocol (Moon H11 → H5 aspect on child) confirmed in LU 25.5.
      Validator saw "...to break the aspec" — buffer artifact, not actual truncation.

    lalkitab-ch25-mars-mercury-sister
      Mars isolated burial remedy (earthen pot with Mars objects) confirmed in LU 25.19.
      Validator saw "...removes Mars's malefic ene" — buffer artifact, not truncation.

1 false contradiction pair:

  sun-sat-property ↔ sun-sat-gold-loss
    Validator: "Opposite attackers (Saturn vs Sun) and opposite remedies for same conjunction."
    Resolution: False positive — the two rules have mutually exclusive secondary triggers.
      LU 25.15 (sun-sat-property): Saturn's objects/property being destroyed → Sun is
        the attacker → Enemy Sacrifice: donate Sun objects (copper, jaggery, wheat).
      LU 25.16 (sun-sat-gold-loss): Sun's objects (gold/jaggery) being lost → Saturn
        is the attacker → Enemy Sacrifice: donate Saturn objects (iron, oil, almonds).
    The "Enemy Sacrifice Protocol" works symmetrically: the remedy planet is ALWAYS the
    attacker, not the victim. Different `trigger` fields make these rules mutually exclusive
    — only one can apply at a time.

Usage:
  # Inspect only (no changes):
  python3 scripts/patch_lalkitab_ch25_flags.py --mongo-url "$MONGO_URL"

  # Inspect + patch:
  python3 scripts/patch_lalkitab_ch25_flags.py --mongo-url "$MONGO_URL" --patch
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

BATCH_ID = "lalkitab-ch25-v1-20260505"

GROUP_A = {
    "lalkitab-ch25-moon-h11",
    "lalkitab-ch25-mars-mercury-sister",
}

CONTRADICTION_PAIRS = [
    {
        "rules": [
            "lalkitab-ch25-sun-sat-property",
            "lalkitab-ch25-sun-sat-gold-loss",
        ],
        "resolution": (
            "False contradiction: both rules apply to Sun+Saturn conjunction but address "
            "mutually exclusive secondary triggers. "
            "LU 25.15 (sun-sat-property): Saturn's objects/property are being destroyed — "
            "Sun is the attacker — Enemy Sacrifice: donate Sun objects (copper/jaggery/wheat). "
            "LU 25.16 (sun-sat-gold-loss): Sun's objects (gold/jaggery) are being lost — "
            "Saturn is the attacker — Enemy Sacrifice: donate Saturn objects (iron/oil/almonds). "
            "The Enemy Sacrifice Protocol is symmetric: remedy planet = attacker, not victim. "
            "Different `trigger` fields make these rules mutually exclusive — no conflict."
        ),
    },
]

REASON_A = (
    "False flag — validator reading-window truncation artifact: text appears cut off in "
    "validator's read buffer but is complete in the database. "
    "moon-h11: 52-day birth protocol (Moon H11 → H5 aspect on child) confirmed in LU 25.5 "
    "source material. "
    "mars-mercury-sister: Mars isolated burial remedy (earthen pot with Mars objects) confirmed "
    "in LU 25.19 source material. "
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

    # ── Inspect contradiction pair ────────────────────────────────────────────
    print(f"\n\nFalse contradiction pairs: {len(CONTRADICTION_PAIRS)}\n{'─'*70}")
    for pair in CONTRADICTION_PAIRS:
        print(f"\n  Rules : {' ↔ '.join(pair['rules'])}")
        print(f"  Resolution: {pair['resolution'][:150]}...")

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
                "validation.validated_by": "patch_lalkitab_ch25_flags.py",
                "validation.validated_at": now,
            }},
        )
        if result.modified_count:
            print(f"  ✅ patched [{rid}]")
            patched += 1
        else:
            print(f"  ⚠️  No change: {rid}")

    # ── Clear false contradiction pair ────────────────────────────────────────
    print(f"\n── Clearing false contradiction pair ──\n")
    cleared = 0
    for pair in CONTRADICTION_PAIRS:
        for rid in pair["rules"]:
            result = col.update_one(
                {"rule_id": rid},
                {"$set": {
                    "validation.contradiction_ids":     [],
                    "validation.contradiction_summary": "",
                    "validation.contradiction_note":    pair["resolution"],
                    "validation.validated_by":          "patch_lalkitab_ch25_flags.py",
                    "validation.validated_at":          now,
                }},
            )
            if result.modified_count:
                print(f"  ✅ cleared contradiction: {rid}")
                cleared += 1
            else:
                print(f"  ⚠️  No change: {rid}")

    print(f"\n{patched} / {len(flagged)} rules patched → pending_human_review")
    print(f"{cleared} / {sum(len(p['rules']) for p in CONTRADICTION_PAIRS)} "
          f"contradiction entries cleared")
    client.close()


if __name__ == "__main__":
    main()
