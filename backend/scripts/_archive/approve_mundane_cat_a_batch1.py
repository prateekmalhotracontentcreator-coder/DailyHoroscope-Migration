#!/usr/bin/env python3
"""
approve_mundane_cat_a_batch1.py

Resolves 4 Category A rules after validation:

  1. mundane-gopal-ch7-cardinal-stellium-upheaval  [result fix + approve]
     Flagged: "co-occurs with seismic events" claim not a Gopalakrishnan
     seismic principle. Fix: remove the speculative earthquake co-occurrence
     sentence from result. Keep core rule (cardinal stellium = geopolitical
     upheaval). No NLM needed -- removing unsourced inference.

  2. mundane-gopal-ch7-rahu-ketu-ic-mc-axis  [approve -- false flag]
     Spot_check. Validator confirmed "Rahu-Ketu on IC/MC axis is a recognized
     seismic indicator in classical mundane astrology." Core logic sound.
     Minor epicenter note is consistent with Gopal Ch7 seismic framework.

  3. mundane-gaur-ch11-eclipse-solar-commodity-by-month  [approve -- false flag]
     Spot_check. Validator confirmed "internally coherent and follows Gaur's
     documented eclipse-commodity methodology." Truncation concern is a
     validator artifact -- full 12-month condition is correctly stored.

  4. mundane-gopal-ch6-epidemic-triad  [approve -- false flag]
     Spot_check. Validator confirmed "three-condition framework is coherent and
     aligns with classical 6th-house disease signification." Minor 10° orb
     concern is a source detail, not a structural flaw.

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_cat_a_batch1.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_cat_a_batch1.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

RESULT_FIX = {
    "rule_id":  "mundane-gopal-ch7-cardinal-stellium-upheaval",
    "old_result": (
        "Geopolitical upheaval, leadership crises, sudden large-scale events. "
        "Not a direct earthquake indicator but frequently co-occurs with seismic "
        "events as part of a broader world-crisis configuration."
    ),
    "new_result": (
        "Geopolitical upheaval, leadership crises, and sudden large-scale events. "
        "A cardinal stellium is a general mundane stress indicator -- its primary "
        "signal is political and economic disruption rather than seismic activity. "
        "Source: Gopalakrishnan Ch 7, p.96."
    ),
}

APPROVALS = [
    {
        "rule_id": "mundane-gopal-ch7-cardinal-stellium-upheaval",
        "note": (
            "Flagged -- result contained 'frequently co-occurs with seismic events' "
            "claim not in Gopalakrishnan Ch7 as a stated seismic principle. Removed "
            "speculative earthquake co-occurrence sentence. Core rule (cardinal "
            "stellium = geopolitical upheaval) is source-faithful and retained. "
            "Approved by co-founder."
        ),
    },
    {
        "rule_id": "mundane-gopal-ch7-rahu-ketu-ic-mc-axis",
        "note": (
            "False flag (spot_check). Validator confirmed 'Rahu-Ketu on IC/MC axis "
            "is a recognized seismic indicator in classical mundane astrology.' Core "
            "logic and seismic signal are sound and consistent with Gopal Ch7. "
            "Approved by co-founder."
        ),
    },
    {
        "rule_id": "mundane-gaur-ch11-eclipse-solar-commodity-by-month",
        "note": (
            "False flag (spot_check). Validator confirmed 'internally coherent and "
            "follows Gaur's documented eclipse-commodity methodology.' Validator's "
            "truncation concern ('expe...') is a validator artifact -- full 12-month "
            "condition is correctly stored in DB. Approved by co-founder."
        ),
    },
    {
        "rule_id": "mundane-gopal-ch6-epidemic-triad",
        "note": (
            "False flag (spot_check). Validator confirmed 'three-condition framework "
            "is coherent and aligns with classical 6th-house disease signification.' "
            "Minor 10° orb concern is a source-detail spot_check, not a structural "
            "flaw. Core epidemic triad logic is sound. Approved by co-founder."
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
    print(f"Category A batch-1 approvals ({len(APPROVALS)} rules)")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    promoted = 0
    for item in APPROVALS:
        rid = item["rule_id"]
        r = col.find_one(
            {"rule_id": rid, "science_id": "mundane_jyotish"},
            {"_id": 0, "rule_id": 1, "approval_status": 1, "result": 1},
        )
        if not r:
            print(f"  ⚠️  NOT FOUND: {rid}\n")
            continue

        print(f"  {rid}")
        print(f"  status : {r.get('approval_status','?')}")

        update_set = {
            "approval_status":          "approved",
            "validation.verdict":       "approved",
            "validation.approved_by":   "co_founder_cat_a_batch1_may2026",
            "validation.approved_at":   now,
            "validation.approved_note": item["note"],
        }

        # Apply result fix for cardinal-stellium-upheaval
        if rid == RESULT_FIX["rule_id"]:
            current_result = r.get("result", "")
            if current_result == RESULT_FIX["old_result"]:
                update_set["result"] = RESULT_FIX["new_result"]
                print(f"  result fix: removed earthquake co-occurrence claim")
            else:
                print(f"  result fix: ⚠️  mismatch -- skipping result update")

        print(f"  note   : {item['note'][:100]}...")

        if args.apply:
            result = col.update_one(
                {"rule_id": rid},
                {"$set": update_set,
                 "$unset": {"validation.flag_reason": ""}},
            )
            if result.modified_count:
                action = "RESULT FIX + APPROVED" if rid == RESULT_FIX["rule_id"] else "APPROVED"
                print(f"  ✅ {action}\n")
                promoted += 1
            else:
                print(f"  ⚠️  No change written\n")
        else:
            action = "RESULT FIX + APPROVE" if rid == RESULT_FIX["rule_id"] else "APPROVE"
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
