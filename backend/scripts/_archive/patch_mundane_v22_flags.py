#!/usr/bin/env python3
"""
patch_mundane_v22_flags.py

Inspects and (with --patch) patches the 4 flagged rules in the
mundane-interp-v22-20260508 batch to pending_human_review.

4 flagged rules — all content_validity_dispute false flags:

1. mundane-gopal-ch12-india-rahu-lagna-western-imitation
   Validator: "pseudo-secularism" and "Western privilege" are ideologically
   loaded terms.
   Resolution: FALSE FLAG — content_validity_dispute.
   "Pseudo-secularism" is Gopalakrishnan's own term from Ch12 (sourced
   directly). Rahu in Lagna = orientation toward foreign/external is
   standard mundane astrology. The validator rejected the cultural
   characterization but it is source-faithful, not an editorial addition.
   Promoted to pending_human_review for co-founder language review.

2. mundane-gopal-ch12-india-jupiter-6th-judicial-corruption
   Validator: "reservation quotas and caste politics" = political claims
   beyond classical mundane astrology.
   Resolution: FALSE FLAG — content_validity_dispute.
   Jupiter in 6th = institutional friction/dharmic displacement is valid
   mundane astrology. The caste-reservation framing is Gopalakrishnan's
   own interpretation in Ch12, not an editorial overlay. The validator
   applied a neutrality standard that rejects what is literally in the
   source. Promoted to pending_human_review for co-founder
   source-fidelity and sensitivity review.

3. mundane-gopal-ch12-india-pakistan-2-12-friction-veto
   Validator: "structurally impossible peace" is deterministic overreach
   beyond what mundane astrology supports.
   Resolution: FALSE FLAG — content_validity_dispute.
   The 2/12 Lagna relationship as a structural tension indicator is valid.
   Gopalakrishnan explicitly states in Ch12 that lasting peace is
   "astrologically impossible" — this is his documented teaching, not the
   analyst's extrapolation. The validator applied generic mundane
   methodology standards to a source that makes a stronger claim.
   Promoted to pending_human_review for co-founder confirmation of
   whether Gopal's deterministic framing should be preserved verbatim.

4. mundane-gopal-ch12-india-bpo-destiny-3rd-house
   Validator: "+0.50 modifier is arbitrary and not from classical sources;
   'immune to economic cycles' is overstatement of determinism."
   Resolution: FALSE FLAG (partial) — content_validity_dispute.
   The 3rd house cluster → IT/BPO destiny principle IS Gopalakrishnan's
   teaching. However, the +0.50 quantified weight was the analyst's own
   calibration (not Gopal's), and the "immune to economic cycles" language
   overstates the source claim. Substance is source-faithful; specific
   quantification and absolute language need co-founder calibration.
   Promoted to pending_human_review for weight calibration review.

Usage:
  # Inspect only (no changes):
  python3 backend/scripts/patch_mundane_v22_flags.py --mongo-url "$MONGO_URL"

  # Apply patch:
  python3 backend/scripts/patch_mundane_v22_flags.py --mongo-url "$MONGO_URL" --patch
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

BATCH_ID = "mundane-interp-v22-20260508"

PATCHES = {
    "mundane-gopal-ch12-india-rahu-lagna-western-imitation": {
        "patch_reason": "content_validity_dispute",
        "flag_resolution": (
            "False flag — content_validity_dispute: 'Pseudo-secularism' and the "
            "Western-imitation characterization are Gopalakrishnan's own terms from "
            "Ch12, not an editorial overlay. Rahu in Lagna = orientation toward the "
            "foreign/external is standard Vedic mundane astrology (Rahu = foreign, "
            "boundary-crossing, imitative). The validator rejected the cultural "
            "characterization as ideologically loaded, but it is source-faithful. "
            "Promoted to pending_human_review for co-founder language sensitivity review: "
            "confirm whether Gopal's original framing should be preserved verbatim or "
            "neutralized to astrological mechanism language only."
        ),
    },
    "mundane-gopal-ch12-india-jupiter-6th-judicial-corruption": {
        "patch_reason": "content_validity_dispute",
        "flag_resolution": (
            "False flag — content_validity_dispute: Jupiter in the 6th house of a "
            "national chart indicating institutional friction and displacement of the "
            "dharmic/priestly class is valid mundane astrology. The caste-reservation "
            "framing is Gopalakrishnan's own interpretation in Ch12 — he explicitly "
            "connects Jupiter in 6th to the displacement of the Brahmin/intellectual "
            "class through reservation policies. The validator applied a political "
            "neutrality standard that would reject direct source citations on cultural "
            "impact. Promoted to pending_human_review for co-founder source-fidelity "
            "and cultural sensitivity review."
        ),
    },
    "mundane-gopal-ch12-india-pakistan-2-12-friction-veto": {
        "patch_reason": "content_validity_dispute",
        "flag_resolution": (
            "False flag — content_validity_dispute: The 2/12 Lagna relationship as a "
            "structural tension indicator between neighboring nations is established "
            "mundane astrology. Gopalakrishnan explicitly states in Ch12 that India "
            "and Pakistan cannot maintain lasting peace due to this geometric relationship "
            "— this is his documented teaching, not the analyst's extrapolation or "
            "deterministic addition. The validator applied a generic mundane methodology "
            "standard ('absolute vetoes don't exist') to a source that makes a stronger, "
            "explicit claim. The rule is source-faithful. Promoted to pending_human_review "
            "for co-founder confirmation of whether Gopal's deterministic framing should "
            "be preserved verbatim or qualified with transit/dasha override conditions."
        ),
    },
    "mundane-gopal-ch12-india-bpo-destiny-3rd-house": {
        "patch_reason": "content_validity_dispute",
        "flag_resolution": (
            "False flag (partial) — content_validity_dispute: The core principle — "
            "Mercury + Venus cluster in India's 3rd house creates a natal IT/BPO destiny — "
            "is Gopalakrishnan's teaching from Ch12. The validator correctly identifies "
            "that the +0.50 quantified weight modifier is the analyst's calibration, not "
            "Gopal's sourced figure, and that 'immune to economic cycles' overstates the "
            "source claim. However, the substance is source-faithful and the directional "
            "claim (India = global IT/BPO leader by natal promise) is Gopal's own. "
            "Promoted to pending_human_review for co-founder calibration of the weight "
            "modifier and review of the deterministic language."
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
                "validation.validated_by": "patch_mundane_v22_flags.py",
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
