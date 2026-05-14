#!/usr/bin/env python3
"""
tag_cofounder_review_required.py

Tags 7 approved mundane_jyotish rules with:
  validation.cofounders_review_required = True

These rules are approved and live, but contain analyst-derived elements
(timing windows, numeric coefficients, Western terminology, source
attributions) flagged for expert review. The full review remark is in
validation.approved_note with explicit "CO-FOUNDER REVIEW:" sections.

This tag makes them queryable without changing approval status.

Query to find them after tagging:
  col.find({
      "science_id": "mundane_jyotish",
      "validation.cofounders_review_required": True
  })

Rules:
  1. mundane-gaur-ch6-ownership-rain-confirm
     -- 24-48h timing window analyst-added (Gaur Ch6 states only "there will be rains")

  2. gaur-ch8-gold-reserve-banking-crisis-veto
     -- "Sanghatta grid" = Mehta Ch8 term; triple condition = analyst synthesis

  3. gaur-ch10-jupiter-cancer-sun-aspect-supremacy
     -- "trine" = Western term; Vedic = Jupiter's 9th-place Drishti; Digvijay Yoga label to confirm

  4. mundane-mehta-ch22-saturn-dhanesh-treasury-depletion
     -- Dhanesh at Virgo ingress = Gaur Ch2 (not Mehta Ch22); dual-chart clause ambiguous

  5. mundane-gopal-ch3-widow-pm-multiplier
     -- +0.2 weight multiplier analyst-derived; qualitative signal confirmed by NLM

  6. mundane-gopal-ch4-volatile-nomination-chart
     -- "2 or more planets" threshold analyst-derived; Gopal uses qualitative case-study language

  7. mundane-gopal-ch11-rains-rahu-capricorn-moderate
     -- NE monsoon / Himalayan / J&K specifics analyst-added; general rain-veto confirmed

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/tag_cofounder_review_required.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/tag_cofounder_review_required.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

RULE_IDS = [
    "mundane-gaur-ch6-ownership-rain-confirm",
    "gaur-ch8-gold-reserve-banking-crisis-veto",
    "gaur-ch10-jupiter-cancer-sun-aspect-supremacy",
    "mundane-mehta-ch22-saturn-dhanesh-treasury-depletion",
    "mundane-gopal-ch3-widow-pm-multiplier",
    "mundane-gopal-ch4-volatile-nomination-chart",
    "mundane-gopal-ch11-rains-rahu-capricorn-moderate",
]

REVIEW_TOPICS = {
    "mundane-gaur-ch6-ownership-rain-confirm":
        "24-48h timing window is analyst-added; Gaur Ch6 states only 'there will be rains'",
    "gaur-ch8-gold-reserve-banking-crisis-veto":
        "'Sanghatta grid' is Mehta Ch8 terminology (not Gaur Ch8); triple condition is analyst synthesis",
    "gaur-ch10-jupiter-cancer-sun-aspect-supremacy":
        "'Trine' is Western terminology; Vedic equivalent = Jupiter's 9th-place Drishti; confirm Digvijay Yoga label",
    "mundane-mehta-ch22-saturn-dhanesh-treasury-depletion":
        "Dhanesh at Virgo ingress = Gaur Ch2 concept (not Mehta Ch22); dual-chart clause ambiguous",
    "mundane-gopal-ch3-widow-pm-multiplier":
        "+0.2 weight multiplier is analyst-derived numeric coefficient; qualitative signal confirmed by NLM",
    "mundane-gopal-ch4-volatile-nomination-chart":
        "'2 or more planets' threshold is analyst-derived; Gopal uses qualitative case-study language",
    "mundane-gopal-ch11-rains-rahu-capricorn-moderate":
        "NE monsoon / Himalayan / J&K snowfall specifics are analyst-added; general rain-veto confirmed by NLM",
}


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
    print(f"Tag co-founder review required ({len(RULE_IDS)} rules)")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    tagged = 0
    for rid in RULE_IDS:
        r = col.find_one(
            {"rule_id": rid, "science_id": "mundane_jyotish"},
            {"_id": 0, "rule_id": 1, "approval_status": 1,
             "validation.cofounders_review_required": 1},
        )
        if not r:
            print(f"  ⚠️  NOT FOUND: {rid}\n")
            continue

        already = r.get("validation", {}).get("cofounders_review_required", False)
        print(f"  {rid}")
        print(f"  status  : {r.get('approval_status','?')}")
        print(f"  tagged  : {'already tagged ✅' if already else 'not yet tagged'}")
        print(f"  topic   : {REVIEW_TOPICS[rid]}")

        if args.apply:
            res = col.update_one(
                {"rule_id": rid},
                {"$set": {
                    "validation.cofounders_review_required": True,
                    "validation.cofounders_review_topic":    REVIEW_TOPICS[rid],
                    "validation.cofounders_review_tagged_at": now,
                }},
            )
            if res.modified_count:
                print(f"  ✅ TAGGED\n")
                tagged += 1
            else:
                print(f"  ⚠️  No change written (already tagged?)\n")
                tagged += 1  # already tagged counts as done
        else:
            print(f"  🔍 WOULD TAG\n")
            tagged += 1

    print(f"{'─'*65}")
    if args.apply:
        total_tagged = col.count_documents({
            "science_id": "mundane_jyotish",
            "validation.cofounders_review_required": True,
        })
        print(f"Tagged this run : {tagged} / {len(RULE_IDS)}")
        print(f"Total in DB with cofounders_review_required=True : {total_tagged}")
        print(f"\nTo query all flagged rules:")
        print(f'  col.find({{"science_id":"mundane_jyotish","validation.cofounders_review_required":True}})')
    else:
        print(f"Dry run: {tagged} / {len(RULE_IDS)} would be tagged.")
        print("Re-run with --apply to write.")

    client.close()


if __name__ == "__main__":
    main()
