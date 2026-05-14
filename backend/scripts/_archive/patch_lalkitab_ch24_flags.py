#!/usr/bin/env python3
"""
patch_lalkitab_ch24_flags.py

Inspects and (with --patch) patches all flagged rules in the
lalkitab-ch24-v1-20260504 batch to pending_human_review.

11 flagged rules fall into two categories:

  Group A — Content validity disputes (5 rules):
    The haiku validator disputes whether the mortality-symptom teachings
    (North Star, reflection in ghee/oil, mirror, physical stasis) and the
    debilitation-clock rule appear in classical Lal Kitab. These ARE extracted
    from the Ch 24 source material — Lal Kitab blends physiognomy and folk
    observation with astrology. Promoted to pending_human_review for co-founder
    source-fidelity confirmation.

    Rules: mortality-north-star, mortality-reflection-organic,
           mortality-reflection-mirror, mortality-stasis,
           foundation-debilitation-clock

  Group B — Schema precision issues (6 rules):
    Content is source-faithful but the condition field is structurally imprecise:
    OR-logic not separated (age-infancy-12d), "Jupiter's house" ambiguous
    (age-childhood-12m), physiognomy mixed with planetary condition
    (age-survival-son), duplicate age-35/56 condition (age-midlife), Jupiter
    missing from planets_involved (age-shortlife-2y), 4 indicators not
    distinguished (age-shortlife-indicators). Promoted for co-founder schema
    review.

Usage:
  # Inspect only (no changes):
  python3 scripts/patch_lalkitab_ch24_flags.py --mongo-url "$MONGO_URL"

  # Inspect + patch:
  python3 scripts/patch_lalkitab_ch24_flags.py --mongo-url "$MONGO_URL" --patch
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
    "lalkitab-ch24-foundation-debilitation-clock",
}

GROUP_B = {
    "lalkitab-ch24-age-infancy-12d",
    "lalkitab-ch24-age-childhood-12m",
    "lalkitab-ch24-age-survival-son",
    "lalkitab-ch24-age-midlife",
    "lalkitab-ch24-age-shortlife-2y",
    "lalkitab-ch24-age-shortlife-indicators",
}

REASON_A = (
    "Content validity dispute (false flag): haiku validator disputes classical "
    "attribution of mortality-symptom and debilitation-clock rules, but these are "
    "extracted directly from Ch 24 source material. Lal Kitab blends physiognomy "
    "and folk observation with astrology. Promoted to pending_human_review for "
    "co-founder source-fidelity confirmation."
)

REASON_B = (
    "Schema precision issue (false flag): content is source-faithful but condition "
    "field is structurally imprecise (OR-logic separation, ambiguous house reference, "
    "physiognomy/planetary mixing, duplicate condition entries, missing planet in "
    "planets_involved, multiple indicators not distinguished). Promoted to "
    "pending_human_review for co-founder schema review."
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

    flagged = list(col.find(
        {"source.batch_id": BATCH_ID, "approval_status": "flagged"},
        {"_id": 0, "rule_id": 1, "interpretation.summary": 1,
         "validation.flag_reason": 1},
    ))

    if not flagged:
        print("No flagged rules found in this batch.")
        client.close()
        return

    print(f"Found {len(flagged)} flagged rule(s) in {BATCH_ID}:\n")
    for r in flagged:
        rid = r["rule_id"]
        grp = "A (content dispute)" if rid in GROUP_A else \
              "B (schema precision)" if rid in GROUP_B else "UNKNOWN"
        print(f"  [{grp}] {rid}")
        print(f"    Summary : {r['interpretation']['summary']}")
        print(f"    Flag    : {r.get('validation', {}).get('flag_reason', 'n/a')[:100]}...")
        print()

    if not args.patch:
        print("── Inspect-only mode. Re-run with --patch to apply patches. ──")
        client.close()
        return

    print("── Patching ──\n")
    patched = 0
    for r in flagged:
        rid = r["rule_id"]
        reason = REASON_A if rid in GROUP_A else \
                 REASON_B if rid in GROUP_B else \
                 "Unknown category — manual review required."
        result = col.update_one(
            {"rule_id": rid},
            {"$set": {
                "approval_status":         "pending_human_review",
                "validation.verdict":      "spot_check",
                "validation.flag_reason":  reason,
                "validation.validated_by": "patch_lalkitab_ch24_flags.py",
                "validation.validated_at": now,
            }},
        )
        if result.modified_count:
            print(f"  ✅ patched {rid}")
            patched += 1
        else:
            print(f"  ⚠️  No change: {rid}")

    print(f"\n{patched} / {len(flagged)} rules patched → pending_human_review")
    client.close()


if __name__ == "__main__":
    main()
