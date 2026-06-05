#!/usr/bin/env python3
"""
patch_ch34_content_flags_v2.py
--------------------------------------------------------------------
BPHS Vol 1 Phase 1 -- Ch34 content-flag rule resolution

Applies GAI-reviewed decisions for the 3 content-flag rules in Ch34
that could NOT be batch-patched by patch_ch34_flagged.py.

Source: GAI doctrinal review session, 2026-06-01
Decisions:
  bphs-ch34-024 → APPROVED_WITH_EDITS  (valid flag, condition_notes corrected)
  bphs-ch34-035 → APPROVED_WITH_EDITS  (valid flag, condition_notes corrected)
  bphs-ch34-049 → APPROVED_AS_IS       (false flag, decode_note added, Yogakaraka)

Result approval_status → auto_approved
  (AI/GAI validation passed. Co-founder sign-off still required before live users.)

Run sequence:
  Step 0: python3 backend/scripts/patch_ch34_content_flags_v2.py --mongo-url "..." --dry-run
  Step 1: python3 backend/scripts/patch_ch34_content_flags_v2.py --mongo-url "..." --apply
  Step 2: Re-run inspect_bphs_phase1_issues.py -- Ch34 flagged count should be 0
  Step 3: Commit this script to git
"""

import argparse
import os
from datetime import datetime, timezone
from pymongo import MongoClient

PATCH_DATE = datetime.now(timezone.utc).isoformat()
PATCH_AUTHOR = "GAI doctrinal review 2026-06-01 + patch_ch34_content_flags_v2.py"

PATCHES = [
    {
        "rule_id": "bphs-ch34-024",
        "decision": "APPROVED_WITH_EDITS",
        "lagna": "Taurus",
        "planet": "Jupiter",
        "functional_classification": "Functional Malefic (Conditional)",
        "condition_notes_update": {
            "legacy_text_error": "Characterised the 11th house as 'most evil'.",
            "corrected_theological_logic": (
                "Jupiter acts as a difficult and tricky planet for Taurus lagna primarily "
                "due to its 8th house (Sagittarius) lordship, which rules crises, "
                "transformations, and vulnerabilities. Its 11th house (Pisces) lordship "
                "yields financial gains but absorbs the negative traits of the 8th house, "
                "resulting in material wealth often accompanied by sudden obstacles or "
                "health friction."
            ),
        },
        "decode_note": (
            "Flag resolved 2026-06-01 via GAI doctrinal review. Flag was valid: rule "
            "incorrectly labelled the 11th house as 'most evil'. Corrected: Jupiter's "
            "malefic quality for Taurus lagna derives from 8th (Randhresh) lordship; "
            "11th (Labha) lordship gives gains but is tainted by the 8th lordship blemish."
        ),
    },
    {
        "rule_id": "bphs-ch34-035",
        "decision": "APPROVED_WITH_EDITS",
        "lagna": "Cancer",
        "planet": "Venus",
        "functional_classification": None,
        "condition_notes_update": {
            "legacy_text_error": "Stated Taurus as Moolatrikona and mapped it to the 4th house.",
            "corrected_astronomical_mapping": (
                "Venus rules the 4th House via Libra (which holds its highly potent "
                "Moolatrikona degree span: 0-15 Libra) making it a key component for "
                "domestic stability and assets. Simultaneously, it rules the 11th House "
                "via Taurus (its own sign), driving desires and income. The engine must "
                "track the 4th house as the primary Moolatrikona node."
            ),
        },
        "decode_note": (
            "Flag resolved 2026-06-01 via GAI doctrinal review. Flag was valid: rule "
            "conflated Venus's Moolatrikona sign (Libra) with its own sign (Taurus), and "
            "incorrectly placed Taurus at the 4th house for Cancer lagna (Taurus is 11th "
            "from Cancer; Libra is 4th). Corrected: Libra = 4th (Moolatrikona, kendra), "
            "Taurus = 11th (own sign, labha)."
        ),
    },
    {
        "rule_id": "bphs-ch34-049",
        "decision": "APPROVED_AS_IS",
        "lagna": "Libra",
        "planet": "Saturn",
        "functional_classification": "Yogakaraka (Supreme Benefic)",
        "condition_notes_update": None,
        "decode_note": (
            "Flag resolved 2026-06-01 via GAI doctrinal review. Flag was a FALSE FLAG: "
            "the validator failed to recognise the Yogakaraka exception clause. Saturn "
            "rules Capricorn (4th, Kendra) and Aquarius (5th, Trikona) for Libra lagna. "
            "Per Parashara, simultaneous lordship of a Kendra and Trikona overrides all "
            "minor blemishes including Kendradhipatya Dosha. Saturn is the supreme "
            "Yogakaraka for Libra lagna. Rule approved as-is."
        ),
    },
]


def main():
    parser = argparse.ArgumentParser(
        description="Apply GAI decisions for 3 Ch34 content-flag rules"
    )
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"), required=True)
    parser.add_argument("--db-name", default="horoscope_db")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true",
                      help="Preview patches -- no writes")
    mode.add_argument("--apply", action="store_true",
                      help="Write patches to MongoDB")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10000)
    col = client[args.db_name]["interpretation_rules"]

    print("\n" + "=" * 70)
    if args.dry_run:
        print("Ch34 CONTENT-FLAG PATCH -- DRY RUN (no writes)")
    else:
        print("Ch34 CONTENT-FLAG PATCH -- APPLYING")
    print("=" * 70)

    patched = 0
    errors = []

    for p in PATCHES:
        rid = p["rule_id"]
        print(f"\n── {rid} ({p['planet']} / {p['lagna']} lagna) ──")
        print(f"  Decision : {p['decision']}")

        # Verify current state
        rule = col.find_one({"rule_id": rid},
                            {"_id": 0, "rule_id": 1, "approval_status": 1, "condition": 1})
        if not rule:
            print(f"  ❌ NOT FOUND in MongoDB")
            errors.append(f"{rid} -- not found")
            continue

        current_status = rule.get("approval_status")
        print(f"  Current status: {current_status}")

        if current_status == "auto_approved":
            print(f"  ⚠  Already auto_approved -- skipping (already patched)")
            continue

        # Build update document
        set_doc = {
            "approval_status": "auto_approved",
            "validation.verdict": "approve",
            "validation.flag_reason": "",
            "validation.patched_at": PATCH_DATE,
            "validation.patched_by": PATCH_AUTHOR,
            "validation.gai_decision": p["decision"],
            "decode_notes": p["decode_note"],
        }

        if p.get("functional_classification"):
            set_doc["functional_classification"] = p["functional_classification"]

        if p.get("condition_notes_update"):
            for key, val in p["condition_notes_update"].items():
                set_doc[f"condition.condition_notes.{key}"] = val

        if args.dry_run:
            print(f"  [DRY] Would set:")
            for k, v in set_doc.items():
                display_val = str(v)[:80] + "..." if len(str(v)) > 80 else str(v)
                print(f"    {k}: {display_val}")
            patched += 1
        else:
            try:
                result = col.update_one(
                    {"rule_id": rid},
                    {"$set": set_doc}
                )
                if result.modified_count == 1:
                    print(f"  ✅ Patched → auto_approved")
                    patched += 1
                else:
                    print(f"  ⚠  matched={result.matched_count}, modified={result.modified_count}")
                    errors.append(f"{rid} -- no modify")
            except Exception as e:
                print(f"  ❌ Error: {e}")
                errors.append(f"{rid} -- {e}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  {'Would patch' if args.dry_run else 'Patched'} : {patched} / {len(PATCHES)} rules")
    if errors:
        print(f"  Errors : {len(errors)}")
        for e in errors:
            print(f"    {e}")

    if not args.dry_run and patched == len(PATCHES):
        print()
        print("  NEXT STEPS:")
        print("  1. Re-run inspect_bphs_phase1_issues.py -- Ch34 flagged should now be 0")
        print("  2. These 3 rules are auto_approved (AI-validated).")
        print("     Co-founder sign-off still required before they reach live users.")
        print("  3. Commit this script + output to git")

    client.close()


if __name__ == "__main__":
    main()
