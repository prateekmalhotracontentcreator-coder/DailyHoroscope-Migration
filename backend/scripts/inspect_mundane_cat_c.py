#!/usr/bin/env python3
"""
inspect_mundane_cat_c.py

Displays full condition + result for all 14 Category C (logic fixes/splits)
PHR rules so we can write precise patch scripts.

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/inspect_mundane_cat_c.py --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
from pymongo import MongoClient

CAT_C_RULES = [
    # C1 -- Split into separate rules
    "mundane-gaur-ch9-sarvatobhadra-currency-spike",
    "gaur-ch10-mercury-combust-leo-stock-market-crash",
    "gaur-ch10-mercury-retrograde-gemini-education-scandal",
    "mundane-gaur-ch8-gold-silver-bullion-gate",
    # C2 -- Move to engine_specs
    "mundane-gaur-ch8-dual-mapping-volatility",
    # C3 -- Condition/Result corrections
    "mundane-mehta-ch22-jupiter-raja-golden-year",
    "mundane-mehta-ch13-eclipse-lord-placement",
    "mundane-mehta-ch13-eclipse-ruler-royalty",
    "mundane-mehta-ch22-raja-mantri-enemy-deadlock",
    "mundane-gaur-ch6-saptnadi-amrita-rain",
    "gaur-ch10-45-muhurti-ingress-overrides-drought",
    "mundane-gopal-ch3-trikona-trikona-billionaire",
    "mundane-gopal-ch5-jaimini-short-tenure",
    "mundane-mehta-ch18-8th-house-vacancy-rule",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]

    found = 0
    for rid in CAT_C_RULES:
        r = col.find_one(
            {"rule_id": rid, "science_id": "mundane_jyotish"},
            {"_id": 0, "rule_id": 1, "title": 1, "condition": 1,
             "result": 1, "approval_status": 1, "batch_id": 1,
             "sub_type": 1},
        )
        if not r:
            print(f"\n⚠️  NOT FOUND: {rid}")
            continue

        found += 1
        print(f"\n{'═'*70}")
        print(f"RULE    : {r['rule_id']}")
        print(f"TITLE   : {r.get('title', 'n/a')}")
        print(f"BATCH   : {r.get('batch_id', 'n/a')}")
        print(f"STATUS  : {r.get('approval_status', '?')}")
        print(f"SUB_TYPE: {r.get('sub_type', 'n/a')}")
        print(f"{'─'*70}")
        print(f"CONDITION:\n{r.get('condition', '')}")
        print(f"{'─'*70}")
        print(f"RESULT:\n{r.get('result', '')}")

    print(f"\n{'─'*70}")
    print(f"Found {found} / {len(CAT_C_RULES)} rules")
    client.close()


if __name__ == "__main__":
    main()
