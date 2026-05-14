#!/usr/bin/env python3
"""
approve_mundane_raphael_koorma_false_flags.py

Approves 7 PHR rules -- all false flags: validator claimed result or condition
was truncated, but the DB contains the complete text in every case.

  Raphael false flags (6):
    1. raphael-ch8-malefic-1st     -- "NEPTUNE in 1st: agitation...socialism, vice, crime,
                                      suicides, fraud and swindling. If the malefic is
                                      itself afflicted by other planets, the evil is more
                                      marked." -- complete.
    2. raphael-ch14-mars-7th       -- "Signs between the four cardinals point to intermediate
                                      compass directions. The sign in which Mars is placed
                                      also shows WHICH COUNTRY is opposed to the nation..."
                                      -- complete.
    3. raphael-ch22-eclipse-fixed  -- Full fixed/cardinal/mutable modality description
                                      present. Validator stopped at final 't' of 'interrupted'
                                      -- complete.
    4. raphael-ch26-eclipse-meridian -- "...earthquakes occur in that part of the world which
                                        is the same distance from Greenwich." -- complete.
    5. raphael-ch27-comet-sign     -- "Countries ruled by the sign in which the comet appears
                                      will suffer serious troubles. Comet's house...9th=scandal;
                                      10th/12th=pestilence; 8th=many sudden deaths." -- complete.
    6. raphael-ch28-mars-transit   -- "Johannesburg = Libra 27°; Copenhagen = Libra 1°."
                                      -- complete.

  Koorma false flag (1):
    7. koorma-triple-directional-audit -- Condition flag: "cuts off at 'Libra='".
       DB has: "Mars in Aries=East, Cancer=North, Libra=West, Capricorn=South."
       Both condition and result complete.

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_raphael_koorma_false_flags.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_raphael_koorma_false_flags.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

ITEMS = [

    # ── 1. raphael-ch8-malefic-1st ───────────────────────────────────────────
    {
        "rule_id": "mundane-raphael-ch8-malefic-1st-national-troubles",
        "note": (
            "False flag (spot_check). Validator claimed result truncated at 'NEPTUNE in 1st: "
            "agitation, secret propaganda, sociali'. DB has the complete result: '...socialism, "
            "vice, crime, suicides, fraud and swindling. If the malefic is itself afflicted by "
            "other planets, the evil is more marked.' All four malefics (Mars/Saturn/Uranus/"
            "Neptune) fully described. Result is coherent and complete. Approved by co-founder."
        ),
    },

    # ── 2. raphael-ch14-mars-7th ─────────────────────────────────────────────
    {
        "rule_id": "mundane-raphael-ch14-mars-7th-war-direction",
        "note": (
            "False flag (spot_check). Validator claimed result truncated at 'Signs betwee'. "
            "DB has the complete result: 'Signs between the four cardinals point to intermediate "
            "compass directions. The sign in which Mars is placed also shows WHICH COUNTRY is "
            "opposed to the nation (according to the country or region ruled by that sign).' "
            "Directional mapping (Aries=East, Cancer=North, Libra=West, Capricorn=South) and "
            "intermediate-sign handling both fully described. Approved by co-founder."
        ),
    },

    # ── 3. raphael-ch22-eclipse-fixed ────────────────────────────────────────
    {
        "rule_id": "mundane-raphael-ch22-eclipse-fixed-lasting-cardinal-brief",
        "note": (
            "False flag (spot_check). Validator claimed result truncated at 't'. DB has the "
            "complete result for all three modalities: Fixed='VERY LASTING EFFECT -- the most "
            "enduring and serious in mundane impact'; Cardinal='BRIEF AND SOON OVER -- effects "
            "are intense but pass quickly'; Mutable='commence SOONER and last LONGER, but "
            "liable to INTERRUPTION -- continue for a time, suddenly cease, then commence "
            "again.' Validator stopped at the final 't' of the word 'interrupted'. Result "
            "is complete. Approved by co-founder."
        ),
    },

    # ── 4. raphael-ch26-eclipse-meridian ─────────────────────────────────────
    {
        "rule_id": "mundane-raphael-ch26-eclipse-on-meridian-nadir-earthquake",
        "note": (
            "False flag (spot_check). Validator claimed result truncated at 'same distance "
            "from'. DB has the complete sentence: '...earthquakes occur in that part of the "
            "world which is the same distance from Greenwich.' Both the meridian/nadir primary "
            "rule and the fixed-sign planet secondary rule are fully stated. Result is "
            "complete. Approved by co-founder."
        ),
    },

    # ── 5. raphael-ch27-comet-sign ───────────────────────────────────────────
    {
        "rule_id": "mundane-raphael-ch27-comet-sign-type-effects",
        "note": (
            "False flag (spot_check). Validator claimed result truncated at 'Countries ruled "
            "by the sign in which'. DB has the complete result continuing: '...the comet "
            "appears will suffer serious troubles. Comet's house in mundane chart also matters: "
            "9th house = scandal or detriment to religion; 10th or 12th = pestilence or "
            "scarcity of corn; 8th house = many sudden and terrible deaths.' Cardinal/Fixed/"
            "Mutable sign mapping and horizon position rules all fully stated. Result is "
            "complete. Approved by co-founder."
        ),
    },

    # ── 6. raphael-ch28-mars-transit ─────────────────────────────────────────
    {
        "rule_id": "mundane-raphael-ch28-mars-transit-country-sign-fires",
        "note": (
            "False flag (spot_check). Validator claimed result truncated at 'Johannesburg = L'. "
            "DB has the complete result: '...Johannesburg = Libra 27°; Copenhagen = Libra 1°.' "
            "The rule body (fires/incendiarism/insurrections; city meridian degree precision) "
            "and the city examples are all fully stated. Result is complete. Approved by "
            "co-founder."
        ),
    },

    # ── 7. koorma-triple-directional-audit ───────────────────────────────────
    {
        "rule_id": "mehta-ch7-koorma-triple-directional-audit",
        "note": (
            "False flag (spot_check). Validator claimed condition truncated at 'Libra='. DB has "
            "the complete condition item (3): 'Mars in Aries=East, Cancer=North, Libra=West, "
            "Capricorn=South.' All four cardinal-sign/direction pairings present. Result is "
            "also complete: all three audit steps described with a worked example (Saturn West + "
            "Jyeshtha West + Mars in Libra West = Critical conflict alert for Baluchistan/"
            "West Punjab corridor). Approved by co-founder."
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
    print(f"Raphael + Koorma false flags ({len(ITEMS)} rules)")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    promoted = 0
    for item in ITEMS:
        rid = item["rule_id"]
        r = col.find_one(
            {"rule_id": rid, "science_id": "mundane_jyotish"},
            {"_id": 0, "rule_id": 1, "approval_status": 1},
        )
        if not r:
            print(f"  ⚠️  NOT FOUND: {rid}\n")
            continue

        print(f"  {rid}")
        print(f"  status : {r.get('approval_status','?')}")
        print(f"  note   : {item['note'][:100]}...")

        update_set = {
            "approval_status":          "approved",
            "validation.verdict":       "approved",
            "validation.approved_by":   "co_founder_raphael_koorma_may2026",
            "validation.approved_at":   now,
            "validation.approved_note": item["note"],
        }

        if args.apply:
            res = col.update_one(
                {"rule_id": rid},
                {"$set": update_set,
                 "$unset": {"validation.spot_check_reason": "",
                            "validation.flag_reason": ""}},
            )
            if res.modified_count:
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
        print(f"Promoted : {promoted} / {len(ITEMS)}")
        print(f"Library  : approved={approved}  PHR={phr}")
    else:
        print(f"Dry run: {promoted} / {len(ITEMS)} would be approved.")
        print("Re-run with --apply to write.")

    client.close()


if __name__ == "__main__":
    main()
