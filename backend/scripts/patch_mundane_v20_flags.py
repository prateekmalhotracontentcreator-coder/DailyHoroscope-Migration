#!/usr/bin/env python3
"""
patch_mundane_v20_flags.py

Inspects and (with --patch) patches the 1 flagged rule in the
mundane-interp-v20-20260508 batch to pending_human_review.

1 flagged rule — internal_logic_misread false flag:

  mundane-gopal-ch10-sports-chasing-victory-trigger
    Validator: "4th lord Exaltation/Vargottam 'overrides' a moderately strong
    10th lord — contradicts the Toss Winner Victory Gate and lacks classical
    Vedic mundane precedent for such override mechanics."

    Resolution: FALSE FLAG — internal_logic_misread.
    The validator treated "override" as a separate mechanical exception, but
    the two rules describe the same mechanism at different specificity levels:
      - Toss Winner Gate: "stronger lord wins"
      - Chasing Trigger: "Exalted/Vargottam 4th lord IS the stronger lord"
    An Exalted planet sits at the top of the Vedic strength hierarchy
    (Exaltation > Own sign > Friendly > Neutral > Debilitation). An Exalted
    4th lord IS by definition stronger than a "moderately strong" 10th lord —
    this is a natural outcome of the base comparison, not a separate override.
    The +0.30 weight modifier is the quantified expression of this elevated
    strength within the triage system. No genuine contradiction exists.
    Source confirmed in Gopalakrishnan Ch10: "chasing rule" explicitly states
    4th lord exalted/in own sign → successful run-chase, even when 10th lord
    is strong — consistent with strength hierarchy, not an exception to it.
    Promoted to pending_human_review for co-founder source-fidelity confirmation.

Usage:
  # Inspect only (no changes):
  python3 backend/scripts/patch_mundane_v20_flags.py --mongo-url "$MONGO_URL"

  # Apply patch:
  python3 backend/scripts/patch_mundane_v20_flags.py --mongo-url "$MONGO_URL" --patch
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

BATCH_ID = "mundane-interp-v20-20260508"

PATCHES = {
    "mundane-gopal-ch10-sports-chasing-victory-trigger": {
        "patch_reason": "internal_logic_misread",
        "flag_resolution": (
            "False flag — internal_logic_misread: the validator treated the Chasing "
            "Victory Trigger as a mechanical override of the Toss Winner Victory Gate, "
            "but both rules describe the same underlying mechanism — the stronger lord "
            "wins. An Exalted or Vargottam 4th lord occupies the highest tier of the "
            "Vedic planetary strength hierarchy and IS by definition stronger than a "
            "'moderately strong' 10th lord. The Chasing Trigger is a specific "
            "instantiation of the base comparison, not an exception to it. "
            "The +0.30 weight modifier quantifies the elevated strength of an Exalted "
            "4th lord within the triage system — no separate override mechanic exists. "
            "Source confirmed in Gopalakrishnan Ch10 'chasing rule': 4th lord exalted "
            "or in own sign → successful run-chase, consistent with strength hierarchy. "
            "Promoted to pending_human_review for co-founder source-fidelity confirmation."
        ),
    },
}


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

    # ── Inspect ───────────────────────────────────────────────────────────────
    flagged = list(col.find(
        {"batch_id": BATCH_ID, "approval_status": "flagged"},
        {"_id": 0, "rule_id": 1, "validation.flag_reason": 1},
    ))

    print(f"\nFlagged rules in {BATCH_ID}: {len(flagged)}\n{'─'*70}")
    for r in flagged:
        rid       = r["rule_id"]
        info      = PATCHES.get(rid)
        patch_tag = info["patch_reason"] if info else "UNKNOWN"
        flag      = r.get("validation", {}).get("flag_reason", "n/a")
        print(f"\n  [{patch_tag}] {rid}")
        print(f"  Validator: {flag[:200]}...")

    if not args.patch:
        print(f"\n{'─'*70}")
        print("── Inspect-only mode. Re-run with --patch to apply. ──")
        client.close()
        return

    # ── Patch ─────────────────────────────────────────────────────────────────
    print(f"\n\n── Patching {len(flagged)} flagged rule(s) ──\n")
    patched = 0
    for r in flagged:
        rid  = r["rule_id"]
        info = PATCHES.get(rid)
        if not info:
            print(f"  ⚠️  No patch defined for {rid} — skipping")
            continue

        result = col.update_one(
            {"rule_id": rid},
            {"$set": {
                "approval_status":         "pending_human_review",
                "validation.verdict":      "spot_check",
                "validation.flag_reason":  info["flag_resolution"],
                "validation.patch_reason": info["patch_reason"],
                "validation.validated_by": "patch_mundane_v20_flags.py",
                "validation.validated_at": now,
            }},
        )
        if result.modified_count:
            print(f"  ✅ {rid}")
            patched += 1
        else:
            print(f"  ⚠️  No change: {rid}")

    print(f"\n{patched} / {len(flagged)} rule(s) patched → pending_human_review")
    client.close()


if __name__ == "__main__":
    main()
