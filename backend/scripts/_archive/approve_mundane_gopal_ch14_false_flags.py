#!/usr/bin/env python3
"""
approve_mundane_gopal_ch14_false_flags.py

Approves 6 Gopal Ch14 PHR rules -- all false flags from the same pattern:
validator applies classical Saturn malefic principles to Gopalakrishnan Ch14's
empirical "Hits of 2006" validation methodology.

Gopal Ch14 is an empirical audit chapter -- rules are validated against observed
outcomes (2006 Sensex, 2006-2008 real estate boom, 2004-2006 IT expansion, etc.)
not derived from classical theory. Saturn producing counterintuitive benefic
results in specific transit conditions is Gopal's empirical finding, not a
classical doctrine violation.

  1. saturn-pushya-bull-run  [false flag -- approve]
     Validator: "contradicts Saturn's contraction principle."
     Reality: Condition includes Dasha/Bhukti qualifier (Rahu/Mercury/Venus for
     India); 2006 Sensex 6,000→12,000+ validates the rule empirically.

  2. saturn-leo-real-estate  [false flag -- approve]
     Validator: "contradicts Saturn's classical nature."
     Reality: 2006-2008 India real estate boom is historical fact; Gopal Ch14
     empirical methodology does not require classical consistency.

  3. saturn-3rd-it-backbone  [false flag -- approve]
     Validator: "Saturn 3rd = delay, not expansion."
     Reality: 2004-2006 India IT boom validated; validator applying classical
     theory to an empirical chapter.

  4. bpo-contrarian-gate  [result fix + approve]
     Validator: "'structurally guarantees' is an absolute assertion."
     Fix: "structurally guarantees" → "strongly indicates" to reflect Gopal's
     probabilistic empirical language rather than determinism.

  5. decentralised-terror  [false flag -- approve]
     Validator: "interpretive leap; Bin Laden validation is post-hoc."
     Reality: Saturn-12th = hidden enemies is classical; "decentralised cellular
     terror" is Gopal's Ch14 empirical interpretation; 2001 cellular model
     is the documented benchmark.

  6. mall-culture-venus-rahu  [false flag -- approve]
     Validator: "deterministic vs probabilistic; economic cycle not astrology."
     Reality: Venus-Rahu = material desire expansion is classical; 2006 India
     mall explosion is observed fact; same false flag pattern as other Ch14 rules.

  NOTE: mundane-gopal-ch14-regional-direction-leadership is NOT in this batch --
  it has two genuine issues (non-standard directional mapping + undefined
  "proximity to Earth") requiring NLM verification first.

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_gopal_ch14_false_flags.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_gopal_ch14_false_flags.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

ITEMS = [

    # ── 1. saturn-pushya-bull-run ─────────────────────────────────────────────
    {
        "rule_id":    "mundane-gopal-ch14-saturn-pushya-bull-run",
        "result_old": None,
        "result_new": None,
        "note": (
            "False flag (flagged). Validator applied classical Saturn contraction "
            "principle to Gopal Ch14's empirical audit chapter. Rule has a Dasha/"
            "Bhukti qualifier (India in Rahu/Mercury/Venus Raja Yoga period) -- not "
            "a blanket Saturn-in-Pushya claim. NLM confirmed at v17 ingest: 2006 "
            "Sensex move from 6,000 to 12,000+ validates the rule empirically. "
            "Gopal Ch14 is an observational/empirical chapter, not classical theory. "
            "Approved by co-founder."
        ),
    },

    # ── 2. saturn-leo-real-estate ─────────────────────────────────────────────
    {
        "rule_id":    "mundane-gopal-ch14-saturn-leo-real-estate",
        "result_old": None,
        "result_new": None,
        "note": (
            "False flag (flagged). Validator applied classical Saturn malefic "
            "principles to Gopal Ch14's empirical 'Hits of 2006' audit. The 2006-2008 "
            "India real estate boom (100% property gains in major metros) is historical "
            "fact; Gopal Ch14 empirical methodology documents observed outcomes, not "
            "classical derivations. Saturn producing benefic sectoral outcomes under "
            "specific transit conditions is Gopal's validated empirical finding. "
            "Approved by co-founder."
        ),
    },

    # ── 3. saturn-3rd-it-backbone ─────────────────────────────────────────────
    {
        "rule_id":    "mundane-gopal-ch14-saturn-3rd-it-backbone",
        "result_old": None,
        "result_new": None,
        "note": (
            "False flag (flagged). Validator applied classical '3rd house = delay "
            "and obstruction' to Gopal Ch14's empirical audit chapter. The 2004-2006 "
            "India IT/BPO boom is historical fact -- all media skeptics (predicting "
            "BPO collapse) were proven wrong. Gopal Ch14 empirical methodology "
            "identifies counterintuitive sectoral signals from Saturn transits; "
            "this is the same pattern as saturn-leo-real-estate and "
            "saturn-pushya-bull-run. Approved by co-founder."
        ),
    },

    # ── 4. bpo-contrarian-gate (result fix) ──────────────────────────────────
    {
        "rule_id":    "mundane-gopal-ch14-bpo-contrarian-gate",
        "result_old": (
            "Contrarian Alert: 'Override media skepticism entirely. BPO/IT sector "
            "will treble recruitment and set new export records. The Saturn-3rd-house "
            "transit structurally guarantees the knowledge-sector boom regardless of "
            "short-term noise. This is the single most reliable sectoral forecast from "
            "the 2006 audit'. Validation: Every media outlet predicted BPO slowdown in "
            "2004-2005. Actual result: BPO sector set all-time records."
        ),
        "result_new": (
            "Contrarian Alert: 'Override media skepticism entirely. BPO/IT sector "
            "will treble recruitment and set new export records. The Saturn-3rd-house "
            "transit strongly indicates a knowledge-sector boom regardless of "
            "short-term noise. This is the single most reliable sectoral forecast from "
            "the 2006 audit'. Validation: Every media outlet predicted BPO slowdown in "
            "2004-2005. Actual result: BPO sector set all-time records."
        ),
        "note": (
            "False flag (flagged) + minor result fix. Validator correctly noted "
            "'structurally guarantees' was an absolute assertion overstepping Gopal's "
            "empirical/probabilistic methodology. Fixed: 'structurally guarantees' → "
            "'strongly indicates'. Core rule (Saturn-3rd → IT/BPO boom signal) is "
            "the same empirically validated finding as saturn-3rd-it-backbone. "
            "Approved by co-founder."
        ),
    },

    # ── 5. decentralised-terror ───────────────────────────────────────────────
    {
        "rule_id":    "mundane-gopal-ch14-decentralised-terror",
        "result_old": None,
        "result_new": None,
        "note": (
            "False flag (flagged). Validator called the interpretation an 'interpretive "
            "leap' and the Bin Laden validation 'post-hoc.' Saturn-12th = hidden "
            "enemies, confinement, and clandestine activity is classical Vedic doctrine. "
            "Gopal Ch14's empirical extension to 'decentralised cellular terror doctrine' "
            "is a documented observational finding from the 2006 audit -- the Al-Qaeda "
            "cellular model is the benchmark. NLM confirmed at v17 ingest. Approved "
            "by co-founder."
        ),
    },

    # ── 6. mall-culture-venus-rahu ────────────────────────────────────────────
    {
        "rule_id":    "mundane-gopal-ch14-mall-culture-venus-rahu",
        "result_old": None,
        "result_new": None,
        "note": (
            "False flag (flagged). Validator questioned determinism vs probabilism "
            "and whether the outcome reflects economic cycle rather than astrology. "
            "Venus-Rahu axis = material desire, illusion, and consumer excess is "
            "classical. Gopal Ch14 documents the 2006 simultaneous launch of organised "
            "retail/mall culture across 12+ Indian metros as the empirical validation. "
            "Same observational methodology as all other Ch14 rules. Approved by "
            "co-founder."
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
    print(f"Gopal Ch14 false flag approvals ({len(ITEMS)} rules)")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    promoted = 0
    for item in ITEMS:
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
            "validation.approved_by":   "co_founder_gopal_ch14_may2026",
            "validation.approved_at":   now,
            "validation.approved_note": item["note"],
        }

        has_fix = item["result_old"] is not None
        if has_fix:
            if r.get("result") == item["result_old"]:
                update_set["result"] = item["result_new"]
                print(f"  result fix: ✅ matched -- 'guarantees' → 'strongly indicates'")
            else:
                print(f"  result fix: ⚠️  mismatch -- skipping result update")
                has_fix = False

        print(f"  note   : {item['note'][:100]}...")

        if args.apply:
            res = col.update_one(
                {"rule_id": rid},
                {"$set": update_set,
                 "$unset": {"validation.flag_reason": "",
                            "validation.spot_check_reason": ""}},
            )
            if res.modified_count:
                action = "RESULT FIX + APPROVED" if has_fix else "APPROVED"
                print(f"  ✅ {action}\n")
                promoted += 1
            else:
                print(f"  ⚠️  No change written\n")
        else:
            action = "RESULT FIX + APPROVE" if has_fix else "APPROVE"
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
        print(f"Promoted : {promoted} / {len(ITEMS)}")
        print(f"Library  : approved={approved}  PHR={phr}")
    else:
        print(f"Dry run: {promoted} / {len(ITEMS)} would be approved.")
        print("Re-run with --apply to write.")

    client.close()


if __name__ == "__main__":
    main()
