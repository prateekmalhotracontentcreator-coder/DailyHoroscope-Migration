#!/usr/bin/env python3
"""
patch_lalkitab_ch24_v2_flags.py

Inspects and (with --patch) patches all flagged rules and false contradiction
pairs in the lalkitab-ch24-v1-20260504 batch to pending_human_review.

9 flagged rules across 3 categories:

  Group A — Persistent content validity disputes (4 rules):
    Haiku validator disputes mortality-symptom teachings as esoteric/non-classical.
    All 4 are confirmed in the Ch 24 AI De-coded source file (5 May 2026).
    Rules: mortality-north-star, mortality-reflection-organic,
           mortality-reflection-mirror, mortality-stasis

  Group B — False structural flags (4 rules):
    Content is source-faithful; validator raises structural objections already
    addressed in the schema design.
    - age-infancy-12d: two-house AND conditions are documented throughout Lal Kitab
    - age-childhood-12m: OR branching is correct per source
    - age-survival-son: physical markers already marked checkable=False; validator
      flagging what the schema explicitly acknowledges
    - age-shortlife-2y: compound AND gate (Jupiter H8-11 + triple conjunction H7)
      is the source rule; specificity is intentional

  Group C — Persistent source-confidence dispute (1 rule):
    - foundation-debilitation-clock: "1 month after birth" rule confirmed in source;
      same flag raised and resolved in v1

2 false contradiction pairs:

  Pair 1: mod-venus ↔ mod-male-planet
    Validator: "Moon+Venus (age 85) conflicts with Moon+male planet (age 96)."
    Resolution: False positive — Venus is a female planet in Jyotish, not in the
    male set (Jupiter/Sun/Mars). The two rules are mutually exclusive by definition.

  Pair 2: age-threshold-85 ↔ moon-h7
    Validator: "Moon+Mars H7 (85yr) ambiguous vs Moon H7 base table (85yr)."
    Resolution: False positive — both rules give identical output (85yr). The Mars
    conjunction in H7 confirms the base Moon-H7 reading, not contradicts it.

Usage:
  # Inspect only (no changes):
  python3 scripts/patch_lalkitab_ch24_v2_flags.py --mongo-url "$MONGO_URL"

  # Inspect + patch:
  python3 scripts/patch_lalkitab_ch24_v2_flags.py --mongo-url "$MONGO_URL" --patch
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

BATCH_ID = "lalkitab-ch24-v1-20260504"

GROUP_A = {
    "lalkitab-ch24-mortality-north-star",
    "lalkitab-ch24-mortality-reflection-organic",
    "lalkitab-ch24-mortality-reflection-mirror",
    "lalkitab-ch24-mortality-stasis",
}

GROUP_B = {
    "lalkitab-ch24-age-infancy-12d",
    "lalkitab-ch24-age-childhood-12m",
    "lalkitab-ch24-age-survival-son",
    "lalkitab-ch24-age-shortlife-2y",
}

GROUP_C = {
    "lalkitab-ch24-foundation-debilitation-clock",
}

# Rules involved in false contradiction pairs
CONTRADICTION_PAIRS = [
    {
        "rules": ["lalkitab-ch24-mod-venus", "lalkitab-ch24-mod-male-planet"],
        "resolution": (
            "False contradiction: Venus is a female planet in Jyotish — not in the male "
            "set (Jupiter/Sun/Mars). Moon+Venus (age 85) and Moon+male planet (age 96) are "
            "mutually exclusive conditions. No conflict."
        ),
    },
    {
        "rules": ["lalkitab-ch24-age-threshold-85", "lalkitab-ch24-moon-h7"],
        "resolution": (
            "False contradiction: both rules produce identical output (age 85yr). "
            "Moon+Mars in H7 confirms the base Moon-H7 reading rather than contradicting it. "
            "Same prediction from two valid trigger paths is not a conflict."
        ),
    },
]

REASON_A = (
    "Persistent content validity dispute (false flag): haiku validator disputes mortality "
    "symptom teachings as esoteric/non-classical. All 4 mortality symptom rules are confirmed "
    "in Ch 24 AI De-coded master source (5 May 2026). Lal Kitab integrates folk observation "
    "and physiognomy with astrology. Promoted to pending_human_review for co-founder "
    "source-fidelity confirmation."
)

REASON_B = (
    "False structural flag: content is source-faithful; validator raises objections already "
    "addressed in schema design. Two-house AND conditions are documented throughout Lal Kitab "
    "(age-infancy-12d); OR branching is correct per source (age-childhood-12m); physical "
    "markers are already marked checkable=False (age-survival-son); compound AND gate is the "
    "source rule — specificity is intentional (age-shortlife-2y). Promoted to "
    "pending_human_review for co-founder review."
)

REASON_C = (
    "Persistent source-confidence dispute (false flag): '1 month after birth' debilitation "
    "clock is confirmed in Ch 24 source material. Same flag raised and resolved in v1. "
    "Promoted to pending_human_review for co-founder source-fidelity confirmation."
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument("--patch", action="store_true",
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
        grp = ("A (content dispute)" if rid in GROUP_A else
               "B (structural flag)" if rid in GROUP_B else
               "C (source confidence)" if rid in GROUP_C else "UNKNOWN")
        print(f"\n  [{grp}] {rid}")
        print(f"    {r['interpretation']['summary']}")
        flag = r.get("validation", {}).get("flag_reason", "n/a")
        print(f"    Flag: {flag[:100]}...")

    # ── Inspect contradiction pairs ───────────────────────────────────────────
    print(f"\n\nFalse contradiction pairs: {len(CONTRADICTION_PAIRS)}\n{'─'*70}")
    for pair in CONTRADICTION_PAIRS:
        print(f"\n  Rules : {' ↔ '.join(pair['rules'])}")
        print(f"  Resolution: {pair['resolution'][:120]}...")

    if not args.patch:
        print(f"\n{'─'*70}")
        print("── Inspect-only mode. Re-run with --patch to apply patches. ──")
        client.close()
        return

    # ── Patch flagged rules ───────────────────────────────────────────────────
    print(f"\n\n── Patching flagged rules ──\n")
    patched = 0
    for r in flagged:
        rid = r["rule_id"]
        reason = (REASON_A if rid in GROUP_A else
                  REASON_B if rid in GROUP_B else
                  REASON_C if rid in GROUP_C else
                  "Unknown category — manual review required.")
        result = col.update_one(
            {"rule_id": rid},
            {"$set": {
                "approval_status":         "pending_human_review",
                "validation.verdict":      "spot_check",
                "validation.flag_reason":  reason,
                "validation.validated_by": "patch_lalkitab_ch24_v2_flags.py",
                "validation.validated_at": now,
            }},
        )
        if result.modified_count:
            print(f"  ✅ patched [{rid}]")
            patched += 1
        else:
            print(f"  ⚠️  No change: {rid}")

    # ── Clear false contradiction pairs ───────────────────────────────────────
    print(f"\n── Clearing false contradiction pairs ──\n")
    cleared = 0
    for pair in CONTRADICTION_PAIRS:
        for rid in pair["rules"]:
            result = col.update_one(
                {"rule_id": rid},
                {"$set": {
                    "validation.contradiction_ids":     [],
                    "validation.contradiction_summary": "",
                    "validation.contradiction_note":    pair["resolution"],
                    "validation.validated_by":          "patch_lalkitab_ch24_v2_flags.py",
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
