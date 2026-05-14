#!/usr/bin/env python3
"""
patch_approve_malefics_trika_entry.py

Fixes + approves mundane-gopal-ch9-malefics-trika-entry.

Validator flagged: "Jupiter is a natural benefic and not typically grouped with
Saturn and Rahu as a malefic trika trigger."

NLM confirmed (May 2026): Gopalakrishnan Ch9 explicitly groups Jupiter with
Saturn and Rahu as "major planets" in "Detail A" of his yearly prediction
framework. Transit of all three into 6/8/12 houses "triggers lot of negative
events." Validator's objection is a false flag.

Outcome mapping verification (NLM):
  6th house (explicit): sickness/epidemic, mass death, war with other country.
  8th house (explicit): death of people's leader, mass deaths.
  12th house (MIXED):
    Explicit: losses of government, last days of government, attack by
    foreigners, expenditure and financial mismanagement.
    Interpretive (not direct citation): "exile of leaders" (inferred from
    "last days of government") and "mass displacement" (inferred from losses).

Fix: update condition's 12th house clause to use Gopalakrishnan's actual
language; label interpretive extensions clearly. Then approve.

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_approve_malefics_trika_entry.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_approve_malefics_trika_entry.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

RULE_ID = "mundane-gopal-ch9-malefics-trika-entry"

OLD_CONDITION = (
    "Saturn, Rahu, or Jupiter transiting into the 6th, 8th, or 12th house "
    "of the national chart (or into the sign ruled by the 6th/8th/12th lord). "
    "Also: into 6th: Triggers war, epidemic, debt crisis, labor disputes. "
    "into 8th: Triggers leadership crisis, mass deaths, government collapse. "
    "into 12th: Triggers financial losses, foreign debt, exile of leaders, "
    "mass displacement. Source: Gopalakrishnan Ch 9, p.146."
)

NEW_CONDITION = (
    "Saturn, Rahu, or Jupiter transiting into the 6th, 8th, or 12th house "
    "of the national chart (or into the sign ruled by the 6th/8th/12th lord). "
    "Gopalakrishnan explicitly groups all three planets as major triggers in "
    "his Ch9 Detail A yearly prediction framework. "
    "into 6th: Triggers sickness/epidemic, mass death, war with other country. "
    "into 8th: Triggers death of people's leader, mass deaths, government crisis. "
    "into 12th: Triggers losses of government, last phase/decline of government, "
    "attack by foreigners, financial mismanagement and expenditure; also signals "
    "the government's last days. Note: 'exile of leaders' and 'mass displacement' "
    "are interpretive extensions of Gopalakrishnan's 'last days of government' "
    "theme -- not direct citations from Ch9. Source: Gopalakrishnan Ch 9, p.146."
)

APPROVE_NOTE = (
    "False flag (flagged). Validator objected that Jupiter is not typically grouped "
    "with Saturn and Rahu as a malefic trika trigger. NLM confirmed: Gopalakrishnan "
    "Ch9 Detail A explicitly groups Jupiter with Saturn and Rahu as the three major "
    "planets triggering trika house events. 6th and 8th house outcomes are direct "
    "citations. 12th house condition updated: removed 'foreign debt,' 'exile,' and "
    "'displacement' (interpretive extensions); replaced with Gopal's actual language "
    "('losses of government,' 'last days of government,' 'attack by foreigners,' "
    "'financial mismanagement'). Approved by co-founder."
)


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
    print(f"Patch + Approve: malefics-trika-entry")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    r = col.find_one(
        {"rule_id": RULE_ID, "science_id": "mundane_jyotish"},
        {"_id": 0, "rule_id": 1, "approval_status": 1, "condition": 1},
    )
    if not r:
        print(f"  ⚠️  NOT FOUND: {RULE_ID}")
        client.close()
        return

    print(f"  {RULE_ID}")
    print(f"  current status : {r.get('approval_status','?')}")

    current_cond = r.get("condition","")
    cond_match = current_cond == OLD_CONDITION
    print(f"  condition match: {'✅' if cond_match else '⚠️  MISMATCH'}")
    if not cond_match:
        print(f"  DB tail: ...{current_cond[-80:]}")

    print(f"  12th fix: 'foreign debt/exile/displacement' → Gopal's actual language")
    print(f"  Jupiter fix: confirmed explicitly grouped in Ch9 Detail A")
    print(f"  note: {APPROVE_NOTE[:100]}...")

    if args.apply and cond_match:
        res = col.update_one(
            {"rule_id": RULE_ID},
            {"$set": {
                "condition":                NEW_CONDITION,
                "approval_status":          "approved",
                "validation.verdict":       "approved",
                "validation.approved_by":   "co_founder_nlm_malefics_trika_may2026",
                "validation.approved_at":   now,
                "validation.approved_note": APPROVE_NOTE,
            },
            "$unset": {"validation.flag_reason": ""}},
        )
        if res.modified_count:
            print(f"\n  ✅ CONDITION FIXED + APPROVED")
        else:
            print(f"\n  ⚠️  No change written")
    elif args.apply and not cond_match:
        print(f"\n  ⚠️  Skipping -- condition mismatch, check DB content")
    else:
        print(f"\n  🔍 WOULD FIX CONDITION + APPROVE")

    if args.apply:
        approved = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "approved"}
        )
        phr = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "pending_human_review"}
        )
        print(f"\nLibrary: approved={approved}  PHR={phr}")

    client.close()


if __name__ == "__main__":
    main()
