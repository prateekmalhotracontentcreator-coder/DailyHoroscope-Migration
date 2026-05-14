#!/usr/bin/env python3
"""
patch_mundane_v3_terrorism_empirical.py

Patches 2 persistently flagged terrorism empirical case rules in v3.

Both rules were flagged by the validator for being post-hoc validations
rather than predictive rules — which is correct. They are intentionally
empirical case studies (sub_type='terrorism_empirical_case') that provide
historical evidence for the predictive framework defined in the companion
rule: mundane-mehta-ch20-terrorism-ten-parameters.

Resolution: promote to pending_human_review with a clear note that these
are documentary/evidentiary cases, not standalone predictive rules, and
that co-founder should decide whether to keep them in the rules library
or move to a separate case-studies notes collection.

Rules:
  1. mundane-mehta-ch20-nine-eleven-validation
     Validator: post-hoc only; 'Saturn in Rohini = wars' overgeneralized;
     10-parameter set not fully defined in condition.

  2. mundane-mehta-ch20-madrid-london-validation
     Validator: post-hoc fitting; no falsifiability threshold; 'Saturn
     affliction of communication houses' vague; retrograde Jupiter as
     terror indicator unsupported classically.

Usage:
  # Inspect:
  python3 backend/scripts/patch_mundane_v3_terrorism_empirical.py --mongo-url "$MONGO_URL"

  # Apply:
  python3 backend/scripts/patch_mundane_v3_terrorism_empirical.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

PATCHES = {
    "mundane-mehta-ch20-nine-eleven-validation": {
        "patch_reason": "empirical_case_study_not_predictive_rule",
        "flag_resolution": (
            "False flag (methodology class mismatch) — this rule is intentionally a documentary "
            "empirical case study, not a standalone predictive rule. Sub_type "
            "'terrorism_empirical_case' explicitly marks it as evidentiary, not operational. "
            "The predictive framework (10 parameters, weighting, methodology) is defined in the "
            "companion rule mundane-mehta-ch20-terrorism-ten-parameters — which is auto_approved. "
            "This rule exists to prove that framework works by showing 6 of 10 parameters active "
            "on 9/11. The validator's 'post-hoc' objection is correct in isolation but misapplies "
            "a predictive-rule standard to a case-study rule. Saturn in Rohini as a war indicator "
            "is Mehta/Rao's own citation from Brihat Samhita — it is source-faithful. "
            "Promoted to pending_human_review for co-founder decision: keep empirical case studies "
            "in the rules library as evidentiary support, or move to a separate cases collection."
        ),
    },
    "mundane-mehta-ch20-madrid-london-validation": {
        "patch_reason": "empirical_case_study_not_predictive_rule",
        "flag_resolution": (
            "False flag (methodology class mismatch) — this rule is intentionally a documentary "
            "empirical case study validating the transport terror signature across two historical "
            "events (Madrid 2004, London 2005). Sub_type 'terrorism_empirical_case' marks it as "
            "evidentiary, not a standalone predictive rule. The predictive mechanism is in "
            "mundane-mehta-ch20-terrorism-ten-parameters (auto_approved). "
            "The validator's falsifiability objection is correct for a predictive rule but does "
            "not apply to an evidentiary case study whose purpose is to document that the "
            "Mars-Rahu/3rd-house signature was active on both attack dates. Saturn affliction of "
            "communication houses (3rd, 12th) is Mehta's own terminology in Ch20 — it is "
            "source-faithful. Retrograde Jupiter as a compounding malefic is also Mehta's "
            "documented observation, not the analyst's addition. "
            "Promoted to pending_human_review for co-founder decision on empirical case rule "
            "classification and library placement."
        ),
    },
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--apply",     action="store_true")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]
    now    = datetime.now(timezone.utc).isoformat()

    print(f"\n{'─'*60}")
    print(f"Terrorism empirical case patch — v3 (2 rules)")
    print(f"{'─'*60}")

    patched = 0
    for rid, patch in PATCHES.items():
        r = col.find_one({"rule_id": rid}, {"_id": 0, "rule_id": 1, "approval_status": 1})
        if not r:
            print(f"\n  ⚠️  Not found: {rid}")
            continue

        print(f"\n  [{patch['patch_reason']}]")
        print(f"  {rid}")
        print(f"  Status: {r.get('approval_status','?')}")
        print(f"  Resolution: {patch['flag_resolution'][:120]}…")

        if args.apply:
            result = col.update_one(
                {"rule_id": rid},
                {"$set": {
                    "approval_status":         "pending_human_review",
                    "validation.verdict":      "spot_check",
                    "validation.flag_reason":  patch["flag_resolution"],
                    "validation.patch_reason": patch["patch_reason"],
                    "validation.validated_by": "patch_mundane_v3_terrorism_empirical.py",
                    "validation.validated_at": now,
                }},
            )
            if result.modified_count:
                print(f"  ✅ Patched → pending_human_review")
                patched += 1
            else:
                print(f"  ⚠️  No change written")
        else:
            patched += 1

    print(f"\n{'═'*60}")
    if args.apply:
        print(f"APPLIED: {patched} / 2 rules patched → pending_human_review")
        print(f"\nNote: No re-validation needed — rules are PHR, not pending_review.")
        print(f"v3 batch is now fully resolved.")
    else:
        print(f"DRY RUN: {patched} rules would be patched. Re-run with --apply.")

    client.close()


if __name__ == "__main__":
    main()
