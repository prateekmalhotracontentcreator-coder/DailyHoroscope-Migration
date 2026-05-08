#!/usr/bin/env python3
"""
inspect_mundane_cat_b.py

Displays full condition + result text for the 8 Category B
(arithmetic artifact) PHR rules so we can write a clean patch.

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/inspect_mundane_cat_b.py --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
from pymongo import MongoClient

CAT_B_RULES = [
    "mehta-ch10-saturn-rahu-capricorn-regime-change",
    "mundane-gopal-ch14-mars-perigee-manufacturing",
    "mundane-gopal-ch5-hora-lagna-fixed-veto",
    "mundane-gopal-ch4-destiny-anchor-karkamsha",
    "mundane-gopal-ch4-eleventh-house-dasha-surge",
    "mundane-gopal-ch12-india-bpo-destiny-3rd-house",
    "mundane-gopal-ch5-rasi-sandhi-veto",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]

    for rid in CAT_B_RULES:
        r = col.find_one(
            {"rule_id": rid, "science_id": "mundane_jyotish"},
            {"_id": 0, "rule_id": 1, "title": 1, "condition": 1,
             "result": 1, "approval_status": 1},
        )
        if not r:
            print(f"\n⚠️  NOT FOUND: {rid}")
            continue

        print(f"\n{'═'*70}")
        print(f"RULE  : {r['rule_id']}")
        print(f"TITLE : {r.get('title', 'n/a')}")
        print(f"STATUS: {r.get('approval_status', '?')}")
        print(f"{'─'*70}")
        print(f"CONDITION:\n{r.get('condition', '')}")
        print(f"{'─'*70}")
        print(f"RESULT:\n{r.get('result', '')}")

    client.close()


if __name__ == "__main__":
    main()
