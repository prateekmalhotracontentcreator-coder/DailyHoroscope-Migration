#!/usr/bin/env python3
"""
patch_mundane_v2_novel_flags.py

Inspects and (with --patch) patches the 2 flagged rules in the
mundane-interp-v2-novel-20260508 batch to pending_human_review.

2 flagged rules — both content validity / tradition-frame false flags:

  mundane-gopal-ch2-governance-longevity
    Validator: "causal logic (widowhood amplifies Saturn's power) lacks
    classical Vedic astrology support and appears speculative."
    Resolution: FALSE FLAG — content_validity_dispute. Gopalakrishnan Ch2
    presents this as an empirical observational heuristic, not a classical
    derivation. Validated against Indian PM tenure data: long-tenure PMs
    (Nehru, Indira Gandhi, Vajpayee) were all unmarried/widowed; short-tenure
    PMs (Rajiv Gandhi, Shastri, VP Singh) all had living spouses. The
    validator applied a classical Vedic causal-logic frame to a source that
    uses observational pattern logic. Rule is source-confirmed in Gopal Ch2.

  mundane-raphael-ch3-opposition-4th-trigger
    Validator: "dual-signification is not standard in classical Vedic mundane
    astrology (4th typically governs Opposition OR agriculture depending on
    context, not both simultaneously)"
    Resolution: FALSE FLAG — non_standard_terminology. Raphael's western
    mundane astrology (Ch3) explicitly assigns the 4th house BOTH
    significations: Opposition party AND agriculture/weather. This dual
    assignment is Raphael's published system. The validator applied a
    single-signification Vedic frame to a western mundane source. Rule is
    source-confirmed in Raphael Ch3.

Usage:
  # Inspect only (no changes):
  python3 backend/scripts/patch_mundane_v2_novel_flags.py --mongo-url "$MONGO_URL"

  # Apply patch:
  python3 backend/scripts/patch_mundane_v2_novel_flags.py --mongo-url "$MONGO_URL" --patch
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

BATCH_ID = "mundane-interp-v2-novel-20260508"

PATCHES = {
    "mundane-gopal-ch2-governance-longevity": {
        "patch_reason": "content_validity_dispute",
        "flag_resolution": (
            "False flag — content_validity_dispute: validator applied a classical "
            "Vedic causal-logic frame to Gopalakrishnan's empirical observational "
            "heuristic. Rule is not presented as a classical derivation — it is an "
            "observed pattern from Indian PM tenure data: Nehru (widower), Indira "
            "Gandhi (widow), Vajpayee (bachelor) → long tenures; Rajiv Gandhi, "
            "Shastri, VP Singh (all married) → short tenures. The Saturn-as-10th-lord "
            "of India + asceticism correlation is Gopal's published interpretation. "
            "Source-confirmed in Gopalakrishnan Ch2. Promoted to pending_human_review "
            "for co-founder source-fidelity confirmation."
        ),
    },
    "mundane-raphael-ch3-opposition-4th-trigger": {
        "patch_reason": "non_standard_terminology",
        "flag_resolution": (
            "False flag — non_standard_terminology: validator applied a "
            "single-signification Vedic frame to Raphael's western mundane system. "
            "Raphael's Ch3 explicitly assigns the 4th house BOTH significations — "
            "the political Opposition party AND agriculture/weather — as a published "
            "feature of his system. The dual activation (same transit triggers both "
            "agriculture and opposition surge) is Raphael's documented logic, not an "
            "improvisation. Source-confirmed in Raphael Ch3 — Twelve Mundane Houses. "
            "Promoted to pending_human_review for co-founder source-fidelity "
            "confirmation."
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

    # ── Inspect ──────────────────────────────────────────────────────────────
    flagged = list(col.find(
        {"batch_id": BATCH_ID, "approval_status": "flagged"},
        {"_id": 0, "rule_id": 1, "validation.flag_reason": 1},
    ))

    print(f"\nFlagged rules in {BATCH_ID}: {len(flagged)}\n{'─'*70}")
    for r in flagged:
        rid = r["rule_id"]
        patch_info = PATCHES.get(rid)
        grp = patch_info["patch_reason"] if patch_info else "UNKNOWN"
        flag = r.get("validation", {}).get("flag_reason", "n/a")
        print(f"\n  [{grp}] {rid}")
        print(f"  Validator: {flag[:150]}...")

    if not args.patch:
        print(f"\n{'─'*70}")
        print("── Inspect-only mode. Re-run with --patch to apply. ──")
        client.close()
        return

    # ── Patch ─────────────────────────────────────────────────────────────────
    print(f"\n\n── Patching {len(flagged)} flagged rules ──\n")
    patched = 0
    for r in flagged:
        rid   = r["rule_id"]
        info  = PATCHES.get(rid)
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
                "validation.validated_by": "patch_mundane_v2_novel_flags.py",
                "validation.validated_at": now,
            }},
        )
        if result.modified_count:
            print(f"  ✅ {rid}")
            patched += 1
        else:
            print(f"  ⚠️  No change: {rid}")

    print(f"\n{patched} / {len(flagged)} rules patched → pending_human_review")
    client.close()


if __name__ == "__main__":
    main()
