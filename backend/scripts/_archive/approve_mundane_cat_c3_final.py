#!/usr/bin/env python3
"""
approve_mundane_cat_c3_final.py

Final resolution for the last 3 Category C3 rules:

  1. gaur-ch10-45-muhurti-ingress-overrides-drought  [condition reword + approve]
     Validator kept reading "The Sun enters any zodiac sign WHILE the Sun is in
     a 45-Muhurti constellation" as two separate simultaneous conditions, causing
     repeated 'conflation' flags. The condition is actually one event: the Sankranti
     moment falling within a 45-Muhurti nakshatra. Reword removes the ambiguity.
     Remaining validator objections (Gaur's rain rules don't use solar ingress;
     nakshatras not established in classical sources) are false flags -- NLM
     confirmed Gaur Ch10 explicitly defines this rule. Approve directly.

  2. mundane-gaur-ch6-saptnadi-amrita-rain  [approve -- false flag]
     Validator: "Rule correctly identifies Amrita Nadi nakshatras and Moon's
     classical association with rainfall." Spot-check concern about compound
     condition lacking "explicit textual support" is a minor sourcing quibble --
     the Saptnadi method in Gaur Ch6 (pp.57-59) IS the source. Approve.

  3. gaur-ch10-mercury-combust-leo-stock-market-crash  [auto_approved → approved]
     Auto-approved cleanly after NLM-corrected rewrite to Gaur's actual
     commodity text. Promote to approved.

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_cat_c3_final.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_cat_c3_final.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

CONDITION_FIX = {
    "rule_id": "gaur-ch10-45-muhurti-ingress-overrides-drought",
    "old_condition": (
        "The Sun enters any zodiac sign while the Sun is in a 45-Muhurti "
        "constellation: Rohini, Punarvasu, Uttaraphalguni, Vishakha, "
        "Uttarashadh, or Uttarabhadrapad."
    ),
    "new_condition": (
        "IF the Sun's Sankranti (sign ingress) falls within one of the six "
        "45-Muhurti nakshatras: Rohini, Punarvasu, Uttaraphalguni, Vishakha, "
        "Uttarashadha, or Uttarabhadrapada. This is a single-moment condition -- "
        "the ingress nakshatra at the exact time of Sankranti determines whether "
        "the 45-Muhurti gate is active. Source: Gaur Ch10."
    ),
}

APPROVALS = [
    {
        "rule_id": "gaur-ch10-45-muhurti-ingress-overrides-drought",
        "note": (
            "False flag (flagged). Condition reworded to clarify the 45-Muhurti "
            "trigger is a single-moment event (Sankranti nakshatra), not two "
            "separate conditions. Remaining validator objections overruled: "
            "(1) 'Gaur rain rules use Moon position' -- false flag; Gaur Ch10 "
            "explicitly defines solar ingress-based commodity/rain rules. "
            "(2) 'Nakshatras not established in classical sources as 45-Muhurti "
            "set' -- false flag; NLM confirmed Gaur Ch10 defines this set "
            "explicitly. Approved by co-founder."
        ),
    },
    {
        "rule_id": "mundane-gaur-ch6-saptnadi-amrita-rain",
        "note": (
            "False flag (spot_check). Validator confirmed 'rule correctly "
            "identifies Amrita Nadi nakshatras and Moon's classical association "
            "with rainfall.' Spot-check concern about 'compound condition lacking "
            "explicit textual support' is a minor sourcing quibble -- the Saptnadi "
            "method in Gaur Ch6 (pp.57-59) is the source and the compound "
            "condition is the Saptnadi method itself. Conflicting-signals note "
            "correctly reflects NLM finding (no explicit precedence stated). "
            "Approved by co-founder."
        ),
    },
    {
        "rule_id": "gaur-ch10-mercury-combust-leo-stock-market-crash",
        "note": (
            "Auto-approved cleanly after NLM-verified rewrite to Gaur Ch10 "
            "actual commodity text (grains medium; metals/gur/khand cheap; "
            "combust: wheat/gram/ghee cheap). Promoted auto_approved → approved "
            "by co-founder."
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
    print(f"Category C3 final approvals ({len(APPROVALS)} rules)")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    promoted = 0

    for item in APPROVALS:
        rid = item["rule_id"]
        r = col.find_one(
            {"rule_id": rid, "science_id": "mundane_jyotish"},
            {"_id": 0, "rule_id": 1, "approval_status": 1, "condition": 1},
        )
        if not r:
            print(f"  ⚠️  NOT FOUND: {rid}\n")
            continue

        print(f"  {rid}")
        print(f"  current status : {r.get('approval_status','?')}")

        update_set = {
            "approval_status":          "approved",
            "validation.verdict":       "approved",
            "validation.approved_by":   "co_founder_cat_c3_final_may2026",
            "validation.approved_at":   now,
            "validation.approved_note": item["note"],
        }

        # Apply condition reword for 45-muhurti rule
        if rid == CONDITION_FIX["rule_id"]:
            current_cond = r.get("condition", "")
            if current_cond == CONDITION_FIX["old_condition"]:
                update_set["condition"] = CONDITION_FIX["new_condition"]
                print(f"  condition fix  : reworded to single-moment Sankranti nakshatra trigger")
            else:
                print(f"  condition      : already updated or unexpected value -- skipping reword")

        print(f"  note           : {item['note'][:100]}...")

        if args.apply:
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
            print(f"  🔍 WOULD APPROVE\n")
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
        auto_app = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "auto_approved"}
        )
        print(f"Promoted : {promoted} / {len(APPROVALS)}")
        print(f"\nLibrary status:")
        print(f"  approved             : {approved}")
        print(f"  pending_human_review : {phr}")
        print(f"  flagged              : {flagged}")
        print(f"  pending_review       : {pending}")
        print(f"  auto_approved        : {auto_app}")
    else:
        print(f"Dry run: {promoted} / {len(APPROVALS)} rules would be approved.")
        print(f"Re-run with --apply to write.")

    client.close()


if __name__ == "__main__":
    main()
