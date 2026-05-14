#!/usr/bin/env python3
"""
approve_mundane_c1_split_rules.py

Approves all 4 Category C1 split rules after NLM verification (May 2026).

All 4 validator flags were false flags -- NLM confirmed Gaur explicitly states
directional price rises (not generic volatility) for each trigger.

  1. mundane-gaur-ch9-dhanishtha-malefic-transit-currency-spike
     Validator: "malefic vedha = volatility, not price surge."
     NLM confirmed: Gaur Ch9 states "Obstruction (Vedha) by malefics cause rise
     of prices." Dhanishtha malefic vedha → gold/silver/currencies "expensive."
     FALSE FLAG. Approve.

  2. mundane-gaur-ch9-mars-right-vedha-krittika-metal-spike
     Validator: same mechanism objection.
     NLM confirmed: Gaur Ch9 -- Krittika malefic vedha → metals/grains "expensive."
     FALSE FLAG. Approve.

  3. mundane-gaur-ch8-jupiter-pushya-gold-silver-bullish
     Validator: spot_check -- "requires source verification."
     NLM confirmed: Gaur Ch8 Pushya nakshatra ownership = "Gold, silver, ghee,
     rice, rock salt, asafoetida, oil, mustard, vegetables."
     FALSE FLAG. Approve. Also update result to use Gaur's exact commodity list.

  4. mundane-gaur-ch8-sun-aries-gold-silver-bullish
     Validator: "Gaur Ch8 only uses nakshatra ownership, not sign ownership."
     NLM confirmed: Gaur uses BOTH sign-level and nakshatra-level ownership.
     Aries sign mapping: "gold, silver, herbs, masoor etc."
     Sun transit Aries table: "Gold, silver, gur, sugar... become expensive."
     EXPLICIT source statement, not inference. FALSE FLAG. Approve.
     Also update result to use Gaur's exact language.

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_c1_split_rules.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_c1_split_rules.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

APPROVALS: list[dict] = [
    {
        "rule_id":      "mundane-gaur-ch9-dhanishtha-malefic-transit-currency-spike",
        "result_fix":   None,
        "note": (
            "False flag (flagged). Validator objected that malefic vedha = volatility, "
            "not directional price surge. NLM confirmed: Gaur Ch9 explicitly states "
            "'Obstruction (Vedha) by malefics cause rise of prices.' Dhanishtha "
            "malefic vedha → gold, silver, currencies, and gems become 'expensive.' "
            "Directional bullish signal is source-faithful. Approved by co-founder."
        ),
    },
    {
        "rule_id":      "mundane-gaur-ch9-mars-right-vedha-krittika-metal-spike",
        "result_fix":   None,
        "note": (
            "False flag (flagged). Same mechanism objection. NLM confirmed: Gaur Ch9 "
            "-- Krittika malefic vedha → metals and grains become 'expensive.' General "
            "principle: 'malefics cause rise of prices.' Directional signal confirmed "
            "source-faithful. Approved by co-founder."
        ),
    },
    {
        "rule_id":      "mundane-gaur-ch8-jupiter-pushya-gold-silver-bullish",
        "result_fix": (
            "BULLISH PRECIOUS METALS: Gold, silver, ghee, rice, rock salt, and related "
            "commodities become expensive. Jupiter transiting Pushya nakshatra activates "
            "Pushya's explicit commodity ownership in Gaur Ch8's nakshatra-commodity "
            "matrix. If Sun is simultaneously in Aries (see companion rule "
            "mundane-gaur-ch8-sun-aries-gold-silver-bullish), both signals fire "
            "independently for compound bullish confirmation. Source: Gaur Ch8."
        ),
        "note": (
            "False flag (spot_check). Validator requested source verification. NLM "
            "confirmed: Gaur Ch8 explicitly maps Pushya to 'Gold, silver, ghee, rice, "
            "rock salt, asafoetida, oil, mustard, vegetables.' Rule is source-faithful. "
            "Result updated to reflect Gaur's exact commodity list. Approved by co-founder."
        ),
    },
    {
        "rule_id":      "mundane-gaur-ch8-sun-aries-gold-silver-bullish",
        "result_fix": (
            "BULLISH PRECIOUS METALS: Gold, silver, gur, and sugar become expensive. "
            "Gaur Ch8 explicitly maps Aries sign to gold and silver at the sign-level "
            "ownership layer; Sun transit table for Aries states 'Gold, silver, gur, "
            "sugar... become expensive.' Gaur uses both nakshatra-level and sign-level "
            "commodity ownership -- the validator's claim that only nakshatra ownership "
            "is used is incorrect. If Jupiter is simultaneously in Pushya (see companion "
            "rule mundane-gaur-ch8-jupiter-pushya-gold-silver-bullish), both signals "
            "fire independently for compound bullish confirmation. Source: Gaur Ch8."
        ),
        "note": (
            "False flag (flagged). Validator claimed Gaur Ch8 only uses nakshatra "
            "ownership. NLM confirmed: Gaur uses BOTH sign-level and nakshatra-level "
            "ownership. Aries sign → 'gold, silver, herbs, masoor.' Sun transit Aries "
            "table → 'Gold, silver, gur, sugar... become expensive.' Explicit source "
            "statement, not inference. Result updated to Gaur's exact language. "
            "Approved by co-founder."
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
    print(f"C1 Split rules -- NLM false flag approvals ({len(APPROVALS)} rules)")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    promoted = 0
    for item in APPROVALS:
        rid = item["rule_id"]
        r = col.find_one(
            {"rule_id": rid, "science_id": "mundane_jyotish"},
            {"_id": 0, "rule_id": 1, "approval_status": 1},
        )
        if not r:
            print(f"  ⚠️  NOT FOUND: {rid}\n")
            continue

        print(f"  {rid}")
        print(f"  current status : {r.get('approval_status','?')}")
        if item["result_fix"]:
            print(f"  result update  : yes (Gaur exact language)")
        print(f"  note           : {item['note'][:100]}...")

        update_set = {
            "approval_status":          "approved",
            "validation.verdict":       "approved",
            "validation.approved_by":   "co_founder_nlm_c1_split_may2026",
            "validation.approved_at":   now,
            "validation.approved_note": item["note"],
        }
        if item["result_fix"]:
            update_set["result"] = item["result_fix"]

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
            action = "RESULT UPDATE + APPROVE" if item["result_fix"] else "APPROVE"
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
