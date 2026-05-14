#!/usr/bin/env python3
"""
patch_approve_mundane_cat_f_rewrites.py

Category F rewrites -- 2 rules. Full rewrite + source correction + approve.

  1. gaur-ch10-mars-ahead-sun-monsoon-failure
     NLM: Rule is in Gaur Ch 6 (not Ch 10). Sign restriction (Gemini/Cancer)
     is NOT in source -- Gaur states "If Mars is ahead of Sun, there will be
     hurdles in rain" with no sign qualification. Mehta's 1987 drought
     benchmark confirms rule applies throughout rainy season (Sun in Leo).
     Fix: remove Gemini/Cancer restriction; update source_chapter to Ch 6;
     update result to match Gaur's actual language + Mehta benchmark note.

  2. gaur-ch10-saturn-retrograde-uttarashadh-poorvashadh-famine
     NLM: Gaur's actual text = "there is drought and grains become expensive."
     No "famine", no 12-year duration, no Rohini Gate comparison.
     The 12-year figure belongs to Rohini Shakata Bhedan Yoga (Mehta) --
     a separate configuration. Fix: rewrite result + title; downgrade severity
     from critical → high.

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_approve_mundane_cat_f_rewrites.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_approve_mundane_cat_f_rewrites.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

RULES = [

    # ── 1. mars-ahead-sun-monsoon-failure ────────────────────────────────────
    {
        "rule_id": "gaur-ch10-mars-ahead-sun-monsoon-failure",

        # Source correction: rule is in Ch 6, not Ch 10
        "source_chapter_old": "Gaur/AIFAS Ch 10",
        "source_chapter_new": "Gaur/AIFAS Ch 6 -- Weather / Prediction of Rain by Horary",

        # Condition: remove Gemini/Cancer restriction
        "condition_old": (
            "Mars is at a higher zodiacal degree than the Sun during the rainy "
            "season -- specifically when the Sun is in Gemini or Cancer."
        ),
        "condition_new": (
            "Mars is at a higher zodiacal degree than the Sun during the rainy "
            "season (June through August / Ashadh through Bhadrapad). "
            "No zodiacal sign restriction in Gaur's text -- the rule is "
            "sign-agnostic. Source: Gaur Ch 6 -- Weather, Prediction of Rain "
            "by Horary, rule 7."
        ),

        # Result: match Gaur's actual language + Mehta benchmark note
        "result_old": (
            "'Monsoon Failure: Rains will be obstructed or delayed.' "
            "Agricultural crisis follows -- below-normal southwest monsoon for India."
        ),
        "result_new": (
            "Hurdles in rain -- rains will be obstructed or delayed. "
            "Gaur's exact text: 'If Mars is ahead of Sun, there will be "
            "hurdles in rain.' Applies throughout the rainy season regardless "
            "of the Sun's sign. Benchmark: 1987 India drought -- Mehta "
            "documented Sun behind Mars until August 24 (Sun in Leo at the "
            "time), confirming sign-agnostic application. Agricultural "
            "disruption and below-normal southwest monsoon follow. "
            "Source: Gaur Ch 6; Mehta 1987 benchmark."
        ),

        # New title (minor tightening)
        "title_new": "Mars Ahead of Sun During Rainy Season = Hurdles in Rain (Monsoon Failure)",

        "note": (
            "Cat F rewrite. NLM confirmed: (1) rule is in Gaur Ch 6, not Ch 10; "
            "(2) Gaur's text 'If Mars is ahead of Sun, there will be hurdles in rain' "
            "carries no Gemini/Cancer sign restriction -- the narrow sign scope was an "
            "analyst interpolation; (3) Mehta's 1987 drought benchmark (Sun in Leo, "
            "behind Mars until Aug 24) confirms sign-agnostic seasonal application. "
            "Source chapter corrected; condition broadened to full rainy season; "
            "result rewritten to Gaur's actual language. Approved by co-founder."
        ),
    },

    # ── 2. saturn-retrograde-uttarashadh-poorvashadh-famine ─────────────────
    {
        "rule_id": "gaur-ch10-saturn-retrograde-uttarashadh-poorvashadh-famine",

        "source_chapter_old": None,   # no source_chapter change needed
        "source_chapter_new": None,

        "condition_old": None,   # condition is correct -- no change
        "condition_new": None,

        # Title: remove "Famine Protocol"
        "title_new": (
            "Saturn Retrograde Re-Entry from Uttarashadha into Poorvashadha "
            "= Drought and Grain Inflation Alert"
        ),

        # Result: downgrade -- remove 12-year claim, Rohini Gate comparison, CAPS alarm
        "result_old": (
            "CRITICAL LONG-TERM FAMINE AND AGRICULTURAL COLLAPSE ALERT. "
            "Severe drought and grain crisis extending up to 12 years. "
            "Escalate to the highest diagnostic level -- this matches the "
            "Rohini Gate severity for agricultural destruction."
        ),
        "result_new": (
            "Drought and grain price inflation indicated. Gaur's source "
            "text: 'there is drought and grains become expensive.' "
            "Duration is unspecified in Gaur Ch 10 -- do not assign a "
            "12-year duration (that figure belongs to Rohini Shakata Bhedan "
            "Yoga, a separate configuration documented by Mehta). Severity "
            "is significant but is not comparable to the Rohini Gate. "
            "Source: Gaur Ch 10 -- Transit of Planets."
        ),

        # Severity downgrade: critical → high
        "severity_new": "high",

        "note": (
            "Cat F rewrite. NLM confirmed: (1) Gaur Ch 10 actual text = 'there "
            "is drought and grains become expensive' -- the word 'famine' does not "
            "appear in this entry; (2) the 12-year duration belongs to Rohini "
            "Shakata Bhedan Yoga (Mehta), a distinct configuration -- it was "
            "incorrectly imported here; (3) Gaur makes no comparison to the "
            "Rohini Gate in this entry. Result rewritten to source-faithful text; "
            "title updated; severity downgraded from critical → high. "
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
    print(f"Category F rewrites -- {len(RULES)} rules")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    promoted = 0
    for item in RULES:
        rid = item["rule_id"]
        r = col.find_one(
            {"rule_id": rid, "science_id": "mundane_jyotish"},
            {"_id": 0, "rule_id": 1, "approval_status": 1,
             "condition": 1, "result": 1, "title": 1,
             "source_chapter": 1, "severity": 1},
        )
        if not r:
            print(f"  ⚠️  NOT FOUND: {rid}\n")
            continue

        print(f"  {rid}")
        print(f"  status : {r.get('approval_status','?')}")

        update_set = {
            "approval_status":          "approved",
            "validation.verdict":       "approved",
            "validation.approved_by":   "co_founder_cat_f_rewrite_may2026",
            "validation.approved_at":   now,
            "validation.approved_note": item["note"],
        }

        changes = []

        # Source chapter correction
        if item["source_chapter_new"] is not None:
            if r.get("source_chapter") == item["source_chapter_old"]:
                update_set["source_chapter"] = item["source_chapter_new"]
                changes.append("source_chapter ✅ matched -- will update")
            else:
                changes.append(f"source_chapter ⚠️ mismatch -- DB: {r.get('source_chapter','')[:60]}")

        # Condition rewrite
        if item["condition_new"] is not None:
            if r.get("condition") == item["condition_old"]:
                update_set["condition"] = item["condition_new"]
                changes.append("condition ✅ matched -- will update")
            else:
                changes.append(f"condition ⚠️ mismatch")

        # Result rewrite
        if item["result_old"] is not None:
            if r.get("result") == item["result_old"]:
                update_set["result"] = item["result_new"]
                changes.append("result ✅ matched -- will update")
            else:
                changes.append(f"result ⚠️ mismatch -- DB: ...{r.get('result','')[-60:]}")

        # Title update
        update_set["title"] = item["title_new"]
        changes.append(f"title → {item['title_new'][:60]}")

        # Severity downgrade (rule 2 only)
        if "severity_new" in item:
            update_set["severity"] = item["severity_new"]
            changes.append(f"severity: {r.get('severity','?')} → {item['severity_new']}")

        for c in changes:
            print(f"  {c}")
        print(f"  note   : {item['note'][:100]}...")

        if args.apply:
            res = col.update_one(
                {"rule_id": rid},
                {"$set": update_set,
                 "$unset": {"validation.flag_reason": "",
                            "validation.spot_check_reason": ""}},
            )
            if res.modified_count:
                print(f"  ✅ REWRITTEN + APPROVED\n")
                promoted += 1
            else:
                print(f"  ⚠️  No change written\n")
        else:
            print(f"  🔍 WOULD REWRITE + APPROVE\n")
            promoted += 1

    print(f"{'─'*65}")
    if args.apply:
        approved = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "approved"}
        )
        phr = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "pending_human_review"}
        )
        print(f"Promoted : {promoted} / {len(RULES)}")
        print(f"Library  : approved={approved}  PHR={phr}")
    else:
        print(f"Dry run: {promoted} / {len(RULES)} would be rewritten + approved.")
        print("Re-run with --apply to write.")

    client.close()


if __name__ == "__main__":
    main()
