#!/usr/bin/env python3
"""
split_mundane_cat_c1_rules.py

Splits 2 Category C1 compound rules into 4 standalone rules.

── Split 1: mundane-gaur-ch9-sarvatobhadra-currency-spike ──────────────────
Original condition: "Saturn OR Rahu transiting Dhanishtha (malefic) OR Mars
has Right Vedha on Krittika" -- two completely different Sarvatobhadra
mechanisms bundled into one OR.

→ Rule 1A: mundane-gaur-ch9-dhanishtha-malefic-transit-currency-spike
   Condition: Saturn or Rahu transiting Dhanishtha nakshatra (Sarvatobhadra
   malefic vedha on the nakshatra of currencies).

→ Rule 1B: mundane-gaur-ch9-mars-right-vedha-krittika-metal-spike
   Condition: Mars has Right Vedha on Krittika nakshatra (Sarvatobhadra).

── Split 2: mundane-gaur-ch8-gold-silver-bullion-gate ──────────────────────
Original condition: "Jupiter transiting Pushya AND Sun in Aries simultaneously"
-- a compound AND gate that only fires when both signals coincide, losing
independent signal value.

→ Rule 2A: mundane-gaur-ch8-jupiter-pushya-gold-silver-bullish
   Condition: Jupiter transiting Pushya nakshatra (nakshatra ownership of Gold
   and Silver in Gaur Ch8 commodity matrix).

→ Rule 2B: mundane-gaur-ch8-sun-aries-gold-silver-bullish
   Condition: Sun transiting Aries (sign-level planetary ownership of Gold and
   Silver). When both 2A and 2B fire simultaneously, engine applies both
   signals independently → compound bullish confirmation.

Action:
  - Insert 4 new rules with approval_status = pending_review
  - Retire the 2 original rules with note referencing new rule_ids

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/split_mundane_cat_c1_rules.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/split_mundane_cat_c1_rules.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

NEW_RULES: list[dict] = [

    # ── 1A ───────────────────────────────────────────────────────────────────
    {
        "rule_id":   "mundane-gaur-ch9-dhanishtha-malefic-transit-currency-spike",
        "split_from": "mundane-gaur-ch9-sarvatobhadra-currency-spike",
        "title": (
            "Sarvatobhadra -- Malefic Transit of Dhanishtha = Currency & Metal Spike"
        ),
        "science_id":  "mundane_jyotish",
        "batch_id":    "mundane-interp-v16-split-20260508",
        "sub_type":    "commodity_price_forecast",
        "condition": (
            "Saturn OR Rahu transiting Dhanishtha nakshatra in the Sarvatobhadra "
            "Chakra -- constituting a malefic vedha on Dhanishtha, the nakshatra "
            "that governs all currencies and financial instruments."
        ),
        "result": (
            "CRITICAL METAL & CURRENCY ALERT: Rapid price increase for Gold, "
            "Silver, All Currencies, Ruby, and Pearl predicted. Dhanishtha "
            "nakshatra governs all currencies in the Sarvatobhadra Chakra -- "
            "Saturn or Rahu transit creates malefic vedha pressure signalling "
            "financial market stress and precious metal safe-haven demand. "
            "Source: Gaur Ch9."
        ),
        "approval_status": "pending_review",
    },

    # ── 1B ───────────────────────────────────────────────────────────────────
    {
        "rule_id":   "mundane-gaur-ch9-mars-right-vedha-krittika-metal-spike",
        "split_from": "mundane-gaur-ch9-sarvatobhadra-currency-spike",
        "title": (
            "Sarvatobhadra -- Mars Right Vedha on Krittika = Metal & Currency Spike"
        ),
        "science_id":  "mundane_jyotish",
        "batch_id":    "mundane-interp-v16-split-20260508",
        "sub_type":    "commodity_price_forecast",
        "condition": (
            "Mars has Right Vedha on Krittika nakshatra in the Sarvatobhadra "
            "Chakra -- constituting a malefic directional vedha pressure on the "
            "Krittika-governed commodity cluster."
        ),
        "result": (
            "CRITICAL METAL & CURRENCY ALERT: Rapid price increase for Gold, "
            "Silver, All Currencies, Ruby, and Pearl predicted. Mars Right Vedha "
            "on Krittika in the Sarvatobhadra Chakra activates malefic pressure "
            "on precious metals and currency markets. "
            "Source: Gaur Ch9."
        ),
        "approval_status": "pending_review",
    },

    # ── 2A ───────────────────────────────────────────────────────────────────
    {
        "rule_id":   "mundane-gaur-ch8-jupiter-pushya-gold-silver-bullish",
        "split_from": "mundane-gaur-ch8-gold-silver-bullion-gate",
        "title": (
            "Jupiter Transits Pushya -- Gold & Silver Bullish (Nakshatra Ownership)"
        ),
        "science_id":  "mundane_jyotish",
        "batch_id":    "mundane-interp-v16-split-20260508",
        "sub_type":    "commodity_price_forecast",
        "condition": (
            "Jupiter transiting Pushya nakshatra in the Sarvatobhadra commodity "
            "matrix (Pushya nakshatra ownership: Gold and Silver)."
        ),
        "result": (
            "BULLISH PRECIOUS METALS: Gold and Silver price surge expected. "
            "Jupiter transiting Pushya nakshatra activates the nakshatra's "
            "ownership of Gold and Silver in the Gaur Ch8 commodity matrix -- "
            "Jupiter's expansive quality amplifies the Pushya bullion signal. "
            "If Sun is simultaneously in Aries (see companion rule "
            "mundane-gaur-ch8-sun-aries-gold-silver-bullish), both signals "
            "fire independently for compound bullish confirmation. "
            "Source: Gaur Ch8."
        ),
        "approval_status": "pending_review",
    },

    # ── 2B ───────────────────────────────────────────────────────────────────
    {
        "rule_id":   "mundane-gaur-ch8-sun-aries-gold-silver-bullish",
        "split_from": "mundane-gaur-ch8-gold-silver-bullion-gate",
        "title": (
            "Sun in Aries -- Gold & Silver Bullish (Sign-Level Planetary Ownership)"
        ),
        "science_id":  "mundane_jyotish",
        "batch_id":    "mundane-interp-v16-split-20260508",
        "sub_type":    "commodity_price_forecast",
        "condition": (
            "Sun transiting Aries -- activating the sign's planetary ownership "
            "connection to Gold and Silver in the Gaur Ch8 commodity mapping."
        ),
        "result": (
            "BULLISH PRECIOUS METALS: Gold and Silver price surge expected. "
            "Sun in Aries activates the sign-level planetary ownership of Gold "
            "and Silver in Gaur Ch8's commodity matrix. Sun's transit through "
            "its exaltation sign strengthens the bullion signal. "
            "If Jupiter is simultaneously in Pushya (see companion rule "
            "mundane-gaur-ch8-jupiter-pushya-gold-silver-bullish), both signals "
            "fire independently for compound bullish confirmation. "
            "Source: Gaur Ch8."
        ),
        "approval_status": "pending_review",
    },
]

RETIREMENTS = [
    {
        "rule_id": "mundane-gaur-ch9-sarvatobhadra-currency-spike",
        "split_into": [
            "mundane-gaur-ch9-dhanishtha-malefic-transit-currency-spike",
            "mundane-gaur-ch9-mars-right-vedha-krittika-metal-spike",
        ],
    },
    {
        "rule_id": "mundane-gaur-ch8-gold-silver-bullion-gate",
        "split_into": [
            "mundane-gaur-ch8-jupiter-pushya-gold-silver-bullish",
            "mundane-gaur-ch8-sun-aries-gold-silver-bullish",
        ],
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
    print(f"C1 Splits: 2 compound rules → 4 standalone rules")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    inserted = 0
    retired  = 0

    # ── Insert new split rules ────────────────────────────────────────────────
    print("── New rules to insert ──")
    for rule in NEW_RULES:
        rid = rule["rule_id"]
        existing = col.find_one({"rule_id": rid}, {"_id": 1})
        if existing:
            print(f"  ⚠️  Already exists: {rid}")
            continue

        print(f"  {rid}")
        print(f"  split_from: {rule['split_from']}")
        print(f"  condition : {rule['condition'][:70]}...")
        print(f"  result    : {rule['result'][:70]}...")

        if args.apply:
            doc = {
                **rule,
                "validation": {
                    "split_from":  rule.pop("split_from"),
                    "split_at":    now,
                    "split_by":    "split_mundane_cat_c1_rules.py",
                    "patch_reason": "cat_c1_compound_rule_split",
                },
            }
            col.insert_one(doc)
            print(f"  ✅ Inserted → pending_review\n")
            inserted += 1
        else:
            print(f"  🔍 WOULD INSERT → pending_review\n")
            inserted += 1

    # ── Retire original compound rules ───────────────────────────────────────
    print("── Original rules to retire ──")
    for ret in RETIREMENTS:
        rid = ret["rule_id"]
        r = col.find_one({"rule_id": rid}, {"_id": 0, "rule_id": 1, "approval_status": 1})
        if not r:
            print(f"  ⚠️  NOT FOUND: {rid}\n")
            continue

        print(f"  {rid}  (status: {r.get('approval_status','?')})")
        print(f"  split_into: {ret['split_into']}")

        if args.apply:
            res = col.update_one(
                {"rule_id": rid},
                {"$set": {
                    "approval_status":          "retired",
                    "validation.verdict":       "retired",
                    "validation.retired_reason": (
                        f"Compound rule split into standalone rules: "
                        f"{', '.join(ret['split_into'])}"
                    ),
                    "validation.split_into":   ret["split_into"],
                    "validation.retired_at":   now,
                    "validation.retired_by":   "split_mundane_cat_c1_rules.py",
                }},
            )
            if res.modified_count:
                print(f"  ✅ Retired\n")
                retired += 1
            else:
                print(f"  ⚠️  No change written\n")
        else:
            print(f"  🔍 WOULD RETIRE\n")
            retired += 1

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
        ret_count = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "retired"}
        )
        print(f"Inserted : {inserted} new rules → pending_review")
        print(f"Retired  : {retired} compound rules")
        print(f"\nLibrary status:")
        print(f"  approved             : {approved}")
        print(f"  pending_human_review : {phr}")
        print(f"  flagged              : {flagged}")
        print(f"  pending_review       : {pending}")
        print(f"  retired              : {ret_count}")
    else:
        print(f"Dry run: {inserted} would be inserted, {retired} would be retired.")
        print(f"Re-run with --apply to write.")

    client.close()


if __name__ == "__main__":
    main()
