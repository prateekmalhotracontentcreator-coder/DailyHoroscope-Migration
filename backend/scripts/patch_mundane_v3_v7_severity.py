#!/usr/bin/env python3
"""
patch_mundane_v3_v7_severity.py

Patches the ~30 rules across mundane-interp-v3–v7 that are missing a top-level
`severity` field (stored as None / absent in MongoDB).

Root cause:
  The v3–v7 ingest scripts used `_rule(..., severity=None, ...)` as default and
  only stored the field when truthy:
      if severity:
          d["severity"] = severity
  Rules written without an explicit severity call therefore have NO `severity`
  key in MongoDB. The validator requires severity ∈ {low, medium, high, critical}.

Fix:
  Set severity = "medium" for every rule in v3–v7 that is missing the field
  (i.e., `rule.get("severity")` is falsy).
  Also reset approval_status → "pending_review" and clear validation subdoc
  so the re-validation treats them as fresh.

Per-batch rule overrides (rules whose context clearly calls for a non-medium default):
  These are pre-loaded in SEVERITY_OVERRIDES below. All others get "medium".

Usage:
  # Inspect (no writes):
  python3 backend/scripts/patch_mundane_v3_v7_severity.py --mongo-url "$MONGO_URL"

  # Apply:
  python3 backend/scripts/patch_mundane_v3_v7_severity.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

BATCHES = [
    "mundane-interp-v3-20260506",
    "mundane-interp-v4-20260506",
    "mundane-interp-v5-20260506",
    "mundane-interp-v6-20260506",
    "mundane-interp-v7-20260506",
]

DEFAULT_SEVERITY = "medium"

# Rules that clearly warrant a non-medium severity based on content.
# Everything not listed here gets DEFAULT_SEVERITY = "medium".
SEVERITY_OVERRIDES: dict[str, str] = {
    # v3 — Gaur Ch2 Celestial Council (annual forecast — medium is correct)
    # v3 — Mehta Ch13 Eclipse rules (eclipse timing/context modifiers — medium)
    # v3 — Mehta Ch20 Terrorism (empirical case studies — high)
    "mundane-mehta-ch20-terrorism-ten-parameters":       "high",
    "mundane-mehta-ch20-nine-eleven-validation":         "high",
    "mundane-mehta-ch20-madrid-london-validation":       "high",
    "mundane-mehta-ch20-india-temple-attack-signature":  "high",
    "mundane-mehta-ch20-delhi-bombs-national-affliction":"high",
    # v3 — Mehta Ch26 Political Party (analytical framework — medium)
    # v4 — Gaur Ch10 price differentials (commodity price signals — low/medium)
    "mundane-gaur-ch10-mars-motion-differentials":       "low",
    "mundane-gaur-ch10-mercury-motion-differentials":    "low",
    "mundane-gaur-ch10-jupiter-motion-differentials":    "low",
    "mundane-gaur-ch10-venus-motion-differentials":      "low",
    "mundane-gaur-ch10-saturn-motion-differentials":     "low",
    "mundane-gaur-ch10-sun-ingress-muhurti-tier":        "medium",
    "mundane-gaur-ch10-transit-synthesis-methodology":   "medium",
    # v4 — Gaur Ch11 eclipse modifiers (modifier rules — medium)
    "mundane-gaur-ch11-eclipse-severity-duration":       "medium",
    "mundane-gaur-ch11-saturn-in-eclipse-sign":          "medium",
    "mundane-gaur-ch11-jupiter-aspect-eclipse-benefic":  "medium",
    "mundane-gaur-ch11-eclipse-solar-commodity-by-month":"medium",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--apply",     action="store_true",
                        help="Write patches. Omit for dry-run inspection.")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]
    now    = datetime.now(timezone.utc).isoformat()

    total_found = total_patched = total_skipped = 0

    for batch in BATCHES:
        rules = list(col.find(
            {"batch_id": batch},
            {"_id": 0, "rule_id": 1, "severity": 1, "approval_status": 1},
        ))
        missing = [r for r in rules if not r.get("severity")]

        print(f"\n{'─'*60}")
        print(f"Batch: {batch}")
        print(f"  Total: {len(rules)} | Missing severity: {len(missing)}")

        total_found += len(missing)

        for r in missing:
            rid = r["rule_id"]
            sev = SEVERITY_OVERRIDES.get(rid, DEFAULT_SEVERITY)
            print(f"\n  [{rid}]  → severity = '{sev}'")

            if args.apply:
                result = col.update_one(
                    {"rule_id": rid},
                    {
                        "$set": {
                            "severity":        sev,
                            "approval_status": "pending_review",
                            "updated_at":      now,
                        },
                        "$unset": {"validation": ""},
                    },
                )
                if result.modified_count:
                    print(f"  ✅ Patched")
                    total_patched += 1
                else:
                    print(f"  ⚠️  No change written")
                    total_skipped += 1
            else:
                total_patched += 1  # count as would-patch in dry run

    print(f"\n{'═'*60}")
    if args.apply:
        print(f"APPLIED: {total_patched} patched, {total_skipped} skipped")
        print(f"All patched rules reset to approval_status='pending_review'")
        print(f"Validation subdoc cleared — ready for re-validation.\n")
        print(f"Next step: re-validate each batch:")
        for b in BATCHES:
            print(f"  --batch-id {b}")
    else:
        print(f"DRY RUN: {total_patched} rules would be patched with severity")
        print(f"Re-run with --apply to write changes.")

    client.close()


if __name__ == "__main__":
    main()
