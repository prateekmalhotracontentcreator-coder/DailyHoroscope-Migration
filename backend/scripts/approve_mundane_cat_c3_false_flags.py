#!/usr/bin/env python3
"""
approve_mundane_cat_c3_false_flags.py

Approves 4 Category C3 rules after post-patch validation:

  3 false flags (validator raised minor concerns but acknowledged sound logic):
    1. mundane-mehta-ch22-jupiter-raja-golden-year
       Validator: "Core logic sound and faithful to Mehta's yearly governance
       framework." Spot-check concern about Grahayudha terminology is a minor
       wording note, not a content flaw. Rule now correctly reads Jupiter
       (not Mars) as Raja -- typo resolved.

    2. mundane-gopal-ch5-jaimini-short-tenure
       Validator: "Rule correctly applies Jaimini Ayurdaya logic (Fixed+Fixed =
       Short Life as inverse of Chara+Chara = Long Life)." Vajpayee 1996
       verification concern is a historical footnote, not a logic error.
       Complement note linking long-tenure / short-tenure pair is sound.

    3. mundane-mehta-ch18-8th-house-vacancy-rule
       Validator objected that "severity gradation lacks explicit Mehta Ch18
       sourcing." Overruled: malefic > benefic severity is universal classical
       Muhurta logic, not an analyst invention. The two-tier condition resolves
       the pre-existing condition/result contradiction. Approve.

  1 title fix + approve:
    4. gaur-ch10-mercury-retrograde-gemini-education-scandal
       Validator correctly flagged title/result mismatch -- rule title still
       referenced "education scandal" after result was updated to vegetable
       prices only. Fix: update title field to reflect actual content, then
       approve.

Usage:
  # Dry run:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_cat_c3_false_flags.py --mongo-url "$MONGO_URL"

  # Apply:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_cat_c3_false_flags.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

APPROVALS: list[dict] = [
    {
        "rule_id": "mundane-mehta-ch22-jupiter-raja-golden-year",
        "title_fix": None,
        "note": (
            "False flag (spot_check). Validator confirmed 'core logic is sound and "
            "faithful to Mehta's yearly governance framework.' Minor concern about "
            "Grahayudha terminology is a wording observation, not a content flaw. "
            "Primary fix (Mars → Jupiter typo in condition) is confirmed correct. "
            "Approved by co-founder."
        ),
    },
    {
        "rule_id": "mundane-gopal-ch5-jaimini-short-tenure",
        "title_fix": None,
        "note": (
            "False flag (spot_check). Validator confirmed 'rule correctly applies "
            "Jaimini Ayurdaya logic (Fixed+Fixed = Short Life as inverse of "
            "Chara+Chara = Long Life).' Vajpayee 1996 verification concern is a "
            "historical footnote, not a logic error. Complement note linking the "
            "paired short/long tenure rules is structurally sound. Approved by "
            "co-founder."
        ),
    },
    {
        "rule_id": "mundane-mehta-ch18-8th-house-vacancy-rule",
        "title_fix": None,
        "note": (
            "False flag (flagged). Validator objected that malefic/benefic severity "
            "gradation 'lacks explicit Mehta Ch18 sourcing.' Overruled: malefic > "
            "benefic severity is universal classical Muhurta logic applied consistently "
            "across all Muhurta texts including Mehta's framework -- not an analyst "
            "invention. The two-tier condition (malefic = severely violated, benefic = "
            "mildly violated, empty = gate passed) resolves the pre-existing "
            "condition/result contradiction. Approved by co-founder."
        ),
    },
    {
        "rule_id": "gaur-ch10-mercury-retrograde-gemini-education-scandal",
        "title_fix": (
            "Mercury Retrograde in Gemini -- Vegetable Price Signal (Gaur Ch10)"
        ),
        "note": (
            "Validator correctly identified title/result mismatch: rule title still "
            "referenced 'education scandal' after result was updated to vegetable "
            "price signal only. Fix: title updated to reflect actual content. "
            "Core rule (Mercury retrograde in own sign Gemini → vegetables become "
            "cheap, perishable commodity supply pressure) is source-faithful to "
            "Gaur Ch10 transit table. Approved by co-founder."
        ),
    },
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--apply",     action="store_true")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]
    now    = datetime.now(timezone.utc).isoformat()

    print(f"\n{'═'*65}")
    print(f"Category C3 false flag approvals ({len(APPROVALS)} rules)")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    promoted = 0
    for item in APPROVALS:
        rid = item["rule_id"]
        r = col.find_one(
            {"rule_id": rid, "science_id": "mundane_jyotish"},
            {"_id": 0, "rule_id": 1, "title": 1, "approval_status": 1},
        )
        if not r:
            print(f"  ⚠️  NOT FOUND: {rid}\n")
            continue

        print(f"  {rid}")
        print(f"  current status : {r.get('approval_status','?')}")
        if item["title_fix"]:
            print(f"  title fix      : {r.get('title','?')[:60]}")
            print(f"               → {item['title_fix'][:60]}")
        print(f"  note           : {item['note'][:100]}...")

        if args.apply:
            update_set = {
                "approval_status":          "approved",
                "validation.verdict":       "approved",
                "validation.approved_by":   "co_founder_cat_c3_review_may2026",
                "validation.approved_at":   now,
                "validation.approved_note": item["note"],
            }
            if item["title_fix"]:
                update_set["title"] = item["title_fix"]

            result = col.update_one(
                {"rule_id": rid},
                {"$set": update_set,
                 "$unset": {"validation.flag_reason": ""}},
            )
            if result.modified_count:
                print(f"  ✅ APPROVED\n")
                promoted += 1
            else:
                print(f"  ⚠️  No change written\n")
        else:
            action = "TITLE FIX + APPROVE" if item["title_fix"] else "APPROVE"
            print(f"  🔍 WOULD {action}\n")
            promoted += 1

    print(f"{'─'*65}")
    if args.apply:
        approved = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "approved"}
        )
        phr = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "pending_human_review"}
        )
        flagged = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "flagged"}
        )
        pending = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "pending_review"}
        )
        print(f"Promoted : {promoted} / {len(APPROVALS)}")
        print(f"\nLibrary status:")
        print(f"  approved             : {approved}")
        print(f"  pending_human_review : {phr}")
        print(f"  flagged              : {flagged}")
        print(f"  pending_review       : {pending}")
    else:
        print(f"Dry run: {promoted} / {len(APPROVALS)} rules would be approved.")
        print(f"Re-run with --apply to write.")

    client.close()


if __name__ == "__main__":
    main()
