#!/usr/bin/env python3
"""
inspect_cat_b_post_validation.py

Shows current approval_status + full flag_reason for the 7 Category B rules
after re-validation, so we can triage what the validator is now objecting to.

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/inspect_cat_b_post_validation.py --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
from pymongo import MongoClient

CAT_B_RULES = [
    "mehta-ch10-saturn-rahu-capricorn-regime-change",
    "mundane-gopal-ch14-mars-perigee-manufacturing",
    "mundane-gopal-ch5-hora-lagna-fixed-veto",
    "mundane-gopal-ch5-rasi-sandhi-veto",
    "mundane-gopal-ch4-destiny-anchor-karkamsha",
    "mundane-gopal-ch4-eleventh-house-dasha-surge",
    "mundane-gopal-ch12-india-bpo-destiny-3rd-house",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]

    flagged = []
    phr     = []
    approved = []

    for rid in CAT_B_RULES:
        r = col.find_one(
            {"rule_id": rid, "science_id": "mundane_jyotish"},
            {"_id": 0, "rule_id": 1, "title": 1, "approval_status": 1,
             "validation": 1},
        )
        if not r:
            print(f"⚠️  NOT FOUND: {rid}")
            continue

        status = r.get("approval_status", "?")
        v      = r.get("validation", {})
        reason = v.get("flag_reason", "") or v.get("verdict", "")

        print(f"\n{'═'*70}")
        print(f"RULE   : {rid}")
        print(f"STATUS : {status}")
        print(f"VERDICT: {v.get('verdict', 'n/a')}")
        if reason:
            print(f"REASON :\n{reason}")

        if status == "flagged":
            flagged.append(rid)
        elif status == "pending_human_review":
            phr.append(rid)
        elif status in ("approved", "auto_approved"):
            approved.append(rid)

    print(f"\n{'─'*70}")
    print(f"Summary: flagged={len(flagged)}  PHR={len(phr)}  approved={len(approved)}")

    client.close()


if __name__ == "__main__":
    main()
