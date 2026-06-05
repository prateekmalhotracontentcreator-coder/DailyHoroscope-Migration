#!/usr/bin/env python3
"""
patch_ch34_flagged.py
--------------------------------------------------------------------
BPHS Vol 1 Phase 1 -- Ch34 flagged-rule cleanup

Two actions in one script:
  1. INVESTIGATE (dry-run): Prints full content of the 3 content-flag rules
     (bphs-ch34-024, bphs-ch34-035, bphs-ch34-049) so TT can review.
     These are NOT patched -- they need manual NLM/TT decision.

  2. PATCH: Moves 12 confirmed truncation-artifact rules from
     approval_status=flagged → pending_human_review.
     Adds a decode_note so NLM knows why they landed in PHR.
     These are NOT approved -- they need NLM re-decode of source sloka.

Run sequence (mandatory):
  Step 0: python3 backend/scripts/patch_ch34_flagged.py --mongo-url "..." --dry-run
  Step 1: Review printed content for 024/035/049 -- record TT decisions
  Step 2: python3 backend/scripts/patch_ch34_flagged.py --mongo-url "..." --apply
  Step 3: Validate (re-run inspect_bphs_phase1_issues.py) -- Ch34 flagged count should drop to 3
  Step 4: Record decisions for 024/035/049 in BPHS_VOL1_NLM.md
  Step 5: Commit this script and inspect output to git
"""

import argparse
import os
from datetime import datetime, timezone
from pymongo import MongoClient

# ── Rule sets ─────────────────────────────────────────────────────────────────

# These 3 have substantive content flags -- print for investigation, do NOT patch
INVESTIGATE_IDS = [
    "bphs-ch34-024",  # Jupiter for Taurus -- "incorrectly labels" claim
    "bphs-ch34-035",  # Venus for Cancer -- "Moolatrikona Taurus = 4th" claim
    "bphs-ch34-049",  # Saturn logical inconsistency -- "lords 5th AND ..." claim
]

# These 12 are confirmed truncation artifacts -- rule content cut off mid-sentence
# during decode. flagged → pending_human_review so NLM can re-decode from source sloka.
TRUNCATION_IDS = [
    "bphs-ch34-041",
    "bphs-ch34-042",
    "bphs-ch34-045",
    "bphs-ch34-047",
    "bphs-ch34-050",
    "bphs-ch34-053",
    "bphs-ch34-054",
    "bphs-ch34-055",
    "bphs-ch34-058",
    "bphs-ch34-059",
    "bphs-ch34-060",
    "bphs-ch34-082",
]

PATCH_NOTE = (
    "Batch-patched 2026-06-01: truncation artifact -- rule text cut off mid-sentence "
    "during decode pass. Moved flagged→pending_human_review for NLM re-decode from "
    "source sloka. Do NOT approve without re-reading source chapter 34."
)

PATCH_DATE = datetime.now(timezone.utc).isoformat()


def main():
    parser = argparse.ArgumentParser(
        description="Ch34 flag cleanup: investigate content flags, patch truncation artifacts"
    )
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"), required=True,
                        help="MongoDB Atlas connection string")
    parser.add_argument("--db-name", default="horoscope_db")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true",
                      help="Print full content of investigate rules + preview patch (no writes)")
    mode.add_argument("--apply", action="store_true",
                      help="Apply patch to 12 truncation rules (writes to MongoDB)")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10000)
    col = client[args.db_name]["interpretation_rules"]

    # ── SECTION 1: Investigate content-flag rules ──────────────────────────────
    print("\n" + "=" * 70)
    print("SECTION 1 -- CONTENT-FLAG RULES (require TT/NLM review -- NOT patched)")
    print("=" * 70)

    for rid in INVESTIGATE_IDS:
        rule = col.find_one({"rule_id": rid})
        if not rule:
            print(f"\n  ⚠  {rid} -- NOT FOUND in MongoDB")
            continue

        val = rule.get("validation") or {}
        cond = rule.get("condition") or {}
        res = rule.get("result") or {}

        print(f"\n{'─' * 60}")
        print(f"  rule_id       : {rid}")
        print(f"  status        : {rule.get('approval_status')}")
        print(f"  flag_reason   : {val.get('flag_reason', 'n/a')}")
        print(f"  condition.type: {cond.get('type')}")
        print(f"  condition.notes: {cond.get('notes', '')[:200]}")
        print(f"  result.primary : {res.get('primary', '')}")
        print(f"  result.secondary: {res.get('secondary', '')}")
        print(f"  sloka          : {(rule.get('source') or {}).get('sloka', 'n/a')}")
        print()
        print("  TT DECISION NEEDED:")
        if rid == "bphs-ch34-024":
            print("  → Validator claims text INCORRECTLY describes Jupiter for Taurus lagna.")
            print("  → Jupiter rules Sagittarius (8th) + Pisces (11th) for Taurus.")
            print("  → If rule states Jupiter is 'benefic lord' without noting 8th+11th = malefic,")
            print("    that IS an error. Verify against source sloka 34.x.")
            print("  → Options: (a) Approve as-is if rule is accurate, (b) Edit rule text, (c) Reject")
        elif rid == "bphs-ch34-035":
            print("  → Validator claims rule states 'Moolatrikona Taurus = 4th house' for Cancer lagna.")
            print("  → Taurus is 11th from Cancer -- NOT 4th. If rule says 4th, that IS an error.")
            print("  → Verify against source sloka. If error confirmed: edit condition.notes to say 11th.")
            print("  → Options: (a) Edit and approve, (b) Reject this rule object")
        elif rid == "bphs-ch34-049":
            print("  → Validator flags logical inconsistency -- Saturn lords 5th (trine) AND ...")
            print("  → For which ascendant? Virgo: Saturn = 5th (Capricorn) + 6th (Aquarius).")
            print("  → 5th+6th is trine+dusthana -- not contradictory per se.")
            print("  → Verify exact lagna context in source sloka. May be a false flag.")
            print("  → Options: (a) Approve with note clarifying lagna, (b) Edit for clarity")

    # ── SECTION 2: Truncation patch preview / apply ───────────────────────────
    print(f"\n{'=' * 70}")
    if args.dry_run:
        print("SECTION 2 -- TRUNCATION PATCH PREVIEW (dry-run -- no writes)")
    else:
        print("SECTION 2 -- TRUNCATION PATCH APPLYING")
    print("=" * 70)

    # Verify these are still flagged
    found_flagged = []
    found_other = []
    not_found = []

    for rid in TRUNCATION_IDS:
        rule = col.find_one({"rule_id": rid}, {"rule_id": 1, "approval_status": 1})
        if not rule:
            not_found.append(rid)
        elif rule.get("approval_status") == "flagged":
            found_flagged.append(rid)
        else:
            found_other.append((rid, rule.get("approval_status")))

    print(f"\n  Rules confirmed flagged   : {len(found_flagged)}")
    print(f"  Rules with different status: {len(found_other)}")
    print(f"  Rules not found in DB      : {len(not_found)}")

    if found_other:
        print("\n  Skipped (not flagged -- already patched or changed):")
        for rid, status in found_other:
            print(f"    {rid} → currently: {status}")

    if not_found:
        print("\n  NOT FOUND:")
        for rid in not_found:
            print(f"    {rid}")

    if not found_flagged:
        print("\n  No truncation rules to patch. Nothing to write.")
        client.close()
        return

    print(f"\n  Will patch {len(found_flagged)} rules: flagged → pending_human_review")
    for rid in found_flagged:
        print(f"    {rid}")

    if args.dry_run:
        print("\n  [DRY RUN] No writes made.")
        print("  Re-run with --apply to execute the patch.")
        client.close()
        return

    # ── APPLY ──────────────────────────────────────────────────────────────────
    print("\n  Applying patch...")
    patched = 0
    errors = []

    for rid in found_flagged:
        try:
            result = col.update_one(
                {"rule_id": rid, "approval_status": "flagged"},
                {
                    "$set": {
                        "approval_status": "pending_human_review",
                        "validation.patch_note": PATCH_NOTE,
                        "validation.patched_at": PATCH_DATE,
                        "validation.patched_by": "patch_ch34_flagged.py",
                    }
                }
            )
            if result.modified_count == 1:
                patched += 1
                print(f"    ✅ {rid}")
            else:
                errors.append(f"{rid} -- matched {result.matched_count}, modified {result.modified_count}")
        except Exception as e:
            errors.append(f"{rid} -- {e}")

    print(f"\n  Patched: {patched} / {len(found_flagged)}")
    if errors:
        print("\n  ERRORS:")
        for e in errors:
            print(f"    {e}")

    # ── Summary ────────────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Content-flag rules printed for TT review : {len(INVESTIGATE_IDS)}")
    print(f"    bphs-ch34-024, bphs-ch34-035, bphs-ch34-049")
    print(f"    → These remain 'flagged' in MongoDB until TT makes a decision")
    print(f"  Truncation rules patched (flagged→PHR)   : {patched}")
    print()
    print("  NEXT STEPS:")
    print("  1. Re-run inspect_bphs_phase1_issues.py -- Ch34 flagged count should be 3")
    print("  2. Review bphs-ch34-024/035/049 against source BPHS PDF chapter 34")
    print("  3. Record TT decisions for 024/035/049 in BPHS_VOL1_NLM.md")
    print("  4. NLM thread: re-decode Ch34 truncated rules from source slokas")
    print()

    client.close()


if __name__ == "__main__":
    main()
