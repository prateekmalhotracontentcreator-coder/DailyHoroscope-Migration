#!/usr/bin/env python3
"""
approve_mundane_mehta_ch18_ch22_batch.py

Resolves 13 Mehta Ch18 + Ch22 PHR rules.

  10 false flags (4 pre-NLM + 6 NLM-confirmed) -- approve as-is:
    1.  enemy-lord-coalition              -- complete; Chandrashekhar 1990 validation intact
    2.  narasimha-rao-liberalisation-dhana-- complete; Dhana Yoga 2nd-11th classical
    3.  many-bosses-constraint            -- complete; Manmohan Singh 2004 validated
    4.  mars-raja-year-of-sword           -- complete; classical Mars symbolism
    5.  aadhaar-dependency-governance     -- NLM Q3: Mehta Ch18 explicitly maps all 6
                                           nakshatras to Aadhaar level (Ketu+Mercury)
    6.  simhasan-aasan-saturn-terminal    -- NLM Q4: 5-level Simhasan Chakra framework +
                                           Aasan nakshatra list both explicit in Mehta Ch18
    7.  raman-democratic-lagnas           -- NLM Q5: Mehta directly quotes B.V. Raman on
                                           Aquarius/Libra democratic Lagnas
    8.  shastri-terminal-leadership       -- NLM Q2: Shastri condition uses 8th house/
                                           Saturn/Tajik methodology -- no Jaimini element;
                                           result "greater the risk" is complete in DB
    9.  mercury-dhanesh-it-boom           -- NLM Q7: Mehta himself adds IT/BPO Note in
                                           Ch22 (not analyst extrapolation)
    10. sun-raja-2001-validation          -- NLM Q8: Mehta explicitly cites Gujarat
                                           Earthquake + Tehelka + US-64 as 2001 validation

  3 content fixes + approve:
    11. nakshatra-tithi-veto-combo        -- Remove Mrigshira from malefic nakshatra list.
                                           NLM Q1: Mehta Ch18 explicitly calls Mrigshira a
                                           "friendly nakshatra" good for oath-taking.
                                           Magha stays (Ketu-ruled; flagged in Vajpayee
                                           case study as unfavorable).

    12. anarchy-gate-sun-raja-saturn-mantri
                                        -- Add synthesis note to result. NLM Q6: Mehta Ch22
                                          lists outcomes separately (Sun Raja: "senior ruler
                                          dies"; Saturn Mantri: "not good for people") but
                                          does NOT combine into a named formula. Rule is
                                          valid synthesis of two explicit Mehta statements.

    13. vajpayee-balarishta-pattern       -- Add attribution note for condition item (1).
                                           NLM Q2: Jaimini Ayurdaya "Fixed+Fixed = Short
                                           Life" is Gopalakrishnan Ch5's methodology, not
                                           Mehta Ch18's. Mehta uses Tajik/8th house/
                                           Simhasan for Vajpayee analysis. Conditions (2)-(5)
                                           align with Mehta. Note added to condition.

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_mehta_ch18_ch22_batch.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_mehta_ch18_ch22_batch.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

# ── Content fixes (old → new) ─────────────────────────────────────────────────

NAKSHATRA_TITHI_COND_OLD = (
    "IF the oath is taken on a Rikta Tithi (4th/9th/14th lunar day) AND the Moon "
    "is in a malefic nakshatra (Ashlesha/Jyeshtha/Moola/Magha/Mrigshira/Ardra) "
    "→ Double Muhurta veto triggered"
)
NAKSHATRA_TITHI_COND_NEW = (
    "IF the oath is taken on a Rikta Tithi (4th/9th/14th lunar day) AND the Moon "
    "is in a malefic nakshatra (Ashlesha/Jyeshtha/Moola/Magha/Ardra) → Double "
    "Muhurta veto triggered. Note: Mrigshira removed -- Mehta Ch18 explicitly "
    "classifies Mrigshira as a 'friendly nakshatra' suitable for coronation and "
    "oath-taking. Magha retained: Ketu-ruled, flagged in Vajpayee 1996 case study "
    "as 'not favorable for long life of government.' Source: Mehta Ch 18."
)

ANARCHY_RESULT_OLD = (
    "Systemic Instability Warning: Cruel administrative behavior and high-level "
    "leader mortality predicted for this year. The Sun-Saturn combination at the "
    "Raja-Mantri level is the most dangerous executive configuration in the annual "
    "cabinet system. Sun represents the head of state; Saturn represents obstruction, "
    "mortality, and structural breakdown. When Saturn implements the Sun's executive "
    "mandate, it does so with cruelty, bureaucratic rigidity, and ultimately -- in "
    "extreme cases -- physical harm to the leadership itself. Historical pattern: years "
    "with this configuration have seen assassination attempts, sudden deaths of sitting "
    "leaders, or abrupt forced removal from power."
)
ANARCHY_RESULT_NEW = (
    "Systemic Instability Warning: Cruel administrative behavior and high-level "
    "leader mortality predicted for this year. The Sun-Saturn combination at the "
    "Raja-Mantri level is the most dangerous executive configuration in the annual "
    "cabinet system. Sun represents the head of state; Saturn represents obstruction, "
    "mortality, and structural breakdown. When Saturn implements the Sun's executive "
    "mandate, it does so with cruelty, bureaucratic rigidity, and ultimately -- in "
    "extreme cases -- physical harm to the leadership itself. Historical pattern: years "
    "with this configuration have seen assassination attempts, sudden deaths of sitting "
    "leaders, or abrupt forced removal from power. Note: Mehta Ch22 states these "
    "outcomes separately (Sun Raja: 'senior ruler or leader dies / destructive attacks'; "
    "Saturn Mantri: 'not a very good time for people'). This rule synthesises both "
    "into a compound adverse gate -- not a single named formula in Mehta's text. "
    "Source: Mehta Ch 22."
)

VAJPAYEE_COND_OLD = (
    "IF oath chart shows ALL of the following simultaneously: (1) Jaimini Ayurdaya "
    "= Short Life (Fixed + Fixed sign types for Lagna/8th lords), (2) 10th lord weak "
    "(debilitated, combust, or in 6th/8th/12th), (3) Lagna lord not aspecting Lagna, "
    "(4) Moon afflicted by 2+ malefics simultaneously, (5) No majority coalition "
    "(verified externally -- not from chart alone) → Balarishta (infant death) "
    "government pattern triggered"
)
VAJPAYEE_COND_NEW = (
    "IF oath chart shows ALL of the following simultaneously: "
    "(1) Jaimini Short-Tenure indicator active -- Fixed + Fixed sign types for Lagna "
    "and 8th lords (sourced from Gopalakrishnan Ch5 Jaimini Ayurdaya framework, "
    "not Mehta Ch18; see rule: mundane-gopal-ch5-jaimini-short-tenure-gate), "
    "(2) 10th lord weak (debilitated, combust, or in 6th/8th/12th), "
    "(3) Lagna lord not aspecting Lagna, "
    "(4) Moon afflicted by 2+ malefics simultaneously, "
    "(5) No majority coalition (verified externally -- not from chart alone) "
    "→ Balarishta (infant death) government pattern triggered. "
    "Note: Mehta Ch18 analyses Vajpayee 1996 using Tajik yogas, 8th house vacancy, "
    "and Simhasan Chakra methodology. Condition (1) is the Gopalakrishnan Ch5 Jaimini "
    "cross-application to the same case. Source: Mehta Ch 18 + Gopalakrishnan Ch 5."
)

# ── ITEMS list ────────────────────────────────────────────────────────────────

ITEMS = [

    # ── Group 1: pre-NLM false flags ─────────────────────────────────────────

    {
        "rule_id":    "mundane-mehta-ch18-enemy-lord-coalition",
        "cond_old": None, "cond_new": None,
        "result_old": None, "result_new": None,
        "note": (
            "False flag (spot_check). Validator claimed result truncated at 'Adm'. "
            "DB has complete result: 'Administration will spend more time managing "
            "coalition partners than governing.' Full Chandrashekhar 1990 validation "
            "intact (7-month government, Congress-I withdrawal). No content change. "
            "Approved by co-founder."
        ),
    },
    {
        "rule_id":    "mundane-mehta-ch18-narasimha-rao-liberalisation-dhana",
        "cond_old": None, "cond_new": None,
        "result_old": None, "result_new": None,
        "note": (
            "False flag (spot_check). Validator claimed result truncated at 'The "
            "Dhana Yoga link between 2nd and'. DB has complete sentence: '...2nd and "
            "11th lords is the critical indicator of historic wealth generation under "
            "this government.' Result fully formed with 1991 liberalisation validation. "
            "Dhana Yoga (2nd-11th connection) is classical. Approved by co-founder."
        ),
    },
    {
        "rule_id":    "mundane-mehta-ch18-many-bosses-constraint",
        "cond_old": None, "cond_new": None,
        "result_old": None, "result_new": None,
        "note": (
            "False flag (spot_check). Validator claimed result truncated at 'The leader "
            "is an i'. DB has complete result: 'The leader is an implementer of others' "
            "vision, not an independent architect. Administration can still achieve "
            "significant results but the leader's personal agency is structurally "
            "limited throughout the tenure.' Manmohan Singh 2004 case study intact. "
            "Approved by co-founder."
        ),
    },
    {
        "rule_id":    "mundane-mehta-ch22-mars-raja-year-of-sword",
        "cond_old": None, "cond_new": None,
        "result_old": None, "result_new": None,
        "note": (
            "False flag (spot_check). Validator claimed result truncated at 'gold and'. "
            "DB has complete result: 'iron, copper, gold, and weapons will increase. "
            "All other cabinet forecasts this year are filtered through a Mars-hazard "
            "overlay.' Classical Mars symbolism throughout -- war, fire, robbery, disease. "
            "No content change. Approved by co-founder."
        ),
    },

    # ── Group 2: NLM-confirmed false flags ────────────────────────────────────

    {
        "rule_id":    "mundane-mehta-ch18-aadhaar-dependency-governance",
        "cond_old": None, "cond_new": None,
        "result_old": None, "result_new": None,
        "note": (
            "False flag (spot_check). NLM Q3 confirmed: Mehta Ch18 explicitly maps "
            "Ashwini/Ashlesha/Magha/Jyeshtha/Moola/Revati to the Aadhaar (foundation) "
            "level of the Simhasan Chakra Panch Nadi hierarchy, governed by Ketu and "
            "Mercury. Validator's concern about attribution 'lacking explicit source "
            "validation' was incorrect. Rule is fully source-faithful. "
            "Approved by co-founder."
        ),
    },
    {
        "rule_id":    "mundane-mehta-ch18-simhasan-aasan-saturn-terminal",
        "cond_old": None, "cond_new": None,
        "result_old": None, "result_new": None,
        "note": (
            "False flag (spot_check). NLM Q4 confirmed: (1) Mehta Ch18 explicitly "
            "defines the 5-level Simhasan Chakra (Panch Nadi) framework: Aadhaar, "
            "Aasan, Patta, Simha, Simhasan; (2) Bharani/Pushya/Purva Phalguni/"
            "Anuradha/Purva Ashadha/Uttara Bhadrapada explicitly listed as Aasan-level, "
            "governed by Venus and Saturn. Validator's 'needs verification' was a false "
            "flag. Result complete in DB ('leader has no independent agency...'). "
            "Approved by co-founder."
        ),
    },
    {
        "rule_id":    "mundane-mehta-ch18-raman-democratic-lagnas",
        "cond_old": None, "cond_new": None,
        "result_old": None, "result_new": None,
        "note": (
            "False flag (spot_check). NLM Q5 confirmed: Mehta Ch18 explicitly quotes "
            "B.V. Raman: 'According to Dr. BV Raman, in case of democratic rule, the "
            "new Government may begin at a time when Aquarius is rising... or in Libra.' "
            "Attribution is correct and directly sourced. Result complete in DB ('when "
            "free of affliction, is auspicious'). Approved by co-founder."
        ),
    },
    {
        "rule_id":    "mundane-mehta-ch18-shastri-terminal-leadership",
        "cond_old": None, "cond_new": None,
        "result_old": None, "result_new": None,
        "note": (
            "False flag (spot_check). NLM Q2 confirmed: Mehta Ch18 uses Tajik yogas, "
            "8th house vacancy, and Simhasan Chakra for Shastri analysis -- not Jaimini "
            "Ayurdaya. Shastri condition (8th lord/Saturn/Moon/Jupiter/Graha Yuddha) "
            "aligns with Mehta's methodology. Result complete in DB: 'The higher the "
            "adverse feature count above 5, the greater the risk of in-office death vs. "
            "mere non-completion of mandate.' Shastri death-in-office is historical fact. "
            "Approved by co-founder."
        ),
    },
    {
        "rule_id":    "mundane-mehta-ch22-mercury-dhanesh-it-boom",
        "cond_old": None, "cond_new": None,
        "result_old": None, "result_new": None,
        "note": (
            "False flag (spot_check). NLM Q7 confirmed: Mehta Ch22 himself adds a "
            "explicit Note modernizing Mercury Dhanesh to IT/BPO/communications sectors: "
            "'The modern significations of Mercury like media, communications also come "
            "into prominence...' The IT/BPO modernization is Mehta's own, not analyst "
            "extrapolation. Result complete in DB. Approved by co-founder."
        ),
    },
    {
        "rule_id":    "mundane-mehta-ch22-sun-raja-2001-validation",
        "cond_old": None, "cond_new": None,
        "result_old": None, "result_new": None,
        "note": (
            "False flag (spot_check). NLM Q8 confirmed: Mehta Ch22 explicitly cites "
            "Gujarat Earthquake, Tehelka sting operation, and US-64 mutual fund collapse "
            "as 2001 validation of Sun Raja year outcomes. Causal link is Mehta's own "
            "documented validation, not analyst inference. Result complete in DB. "
            "Approved by co-founder."
        ),
    },

    # ── Group 3: content fixes + approve ─────────────────────────────────────

    {
        "rule_id":    "mundane-mehta-ch18-nakshatra-tithi-veto-combo",
        "cond_old": NAKSHATRA_TITHI_COND_OLD,
        "cond_new": NAKSHATRA_TITHI_COND_NEW,
        "result_old": None, "result_new": None,
        "note": (
            "Condition fix. NLM Q1 confirmed: Mehta Ch18 explicitly classifies Mrigshira "
            "as a 'friendly nakshatra' suitable for coronation and oath-taking -- it should "
            "NOT appear in the malefic list. Removed from condition. Magha retained: Ketu- "
            "ruled and flagged in Vajpayee 1996 case study as unfavorable for government "
            "longevity. Remaining list (Ashlesha/Jyeshtha/Moola/Magha/Ardra) is source- "
            "faithful. Result complete in DB. Approved by co-founder."
        ),
    },
    {
        "rule_id":    "mundane-mehta-ch22-anarchy-gate-sun-raja-saturn-mantri",
        "cond_old": None, "cond_new": None,
        "result_old": ANARCHY_RESULT_OLD,
        "result_new": ANARCHY_RESULT_NEW,
        "note": (
            "Partial synthesis + result note added. NLM Q6 confirmed: Mehta Ch22 states "
            "Sun Raja and Saturn Mantri outcomes separately ('senior ruler dies / "
            "destructive attacks'; 'not a very good time for people') but does NOT combine "
            "them into a named formula. Rule is a valid synthesis of two explicit Mehta "
            "Ch22 statements. Synthesis note added to result clarifying it is not a single "
            "Mehta formula. Result was also complete in DB (validator hallucinated 'i' "
            "truncation). Approved by co-founder."
        ),
    },
    {
        "rule_id":    "mundane-mehta-ch18-vajpayee-balarishta-pattern",
        "cond_old": VAJPAYEE_COND_OLD,
        "cond_new": VAJPAYEE_COND_NEW,
        "result_old": None, "result_new": None,
        "note": (
            "Condition attribution fix. NLM Q2 confirmed: Jaimini Ayurdaya 'Fixed+Fixed "
            "= Short Life' in condition item (1) is Gopalakrishnan Ch5's methodology, not "
            "Mehta Ch18's. Mehta analyzes Vajpayee using Tajik yogas, 8th house vacancy, "
            "and Simhasan Chakra. Attribution note added to condition: item (1) sourced "
            "from Gopalakrishnan Ch5 (see: mundane-gopal-ch5-jaimini-short-tenure-gate); "
            "items (2)-(5) align with Mehta Ch18. Historical fact (13-day government) "
            "and result are correct. Approved by co-founder."
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
    print(f"Mehta Ch18+Ch22 batch ({len(ITEMS)} rules)")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    promoted = 0
    for item in ITEMS:
        rid = item["rule_id"]
        r = col.find_one(
            {"rule_id": rid, "science_id": "mundane_jyotish"},
            {"_id": 0, "rule_id": 1, "approval_status": 1,
             "condition": 1, "result": 1},
        )
        if not r:
            print(f"  ⚠️  NOT FOUND: {rid}\n")
            continue

        print(f"  {rid}")
        print(f"  status : {r.get('approval_status','?')}")

        update_set = {
            "approval_status":          "approved",
            "validation.verdict":       "approved",
            "validation.approved_by":   "co_founder_mehta_ch18_ch22_may2026",
            "validation.approved_at":   now,
            "validation.approved_note": item["note"],
        }

        has_cond_fix   = item["cond_old"]   is not None
        has_result_fix = item["result_old"] is not None
        any_fix = False

        if has_cond_fix:
            if r.get("condition") == item["cond_old"]:
                update_set["condition"] = item["cond_new"]
                print(f"  condition: ✅ matched -- will update")
                any_fix = True
            else:
                print(f"  condition: ⚠️  mismatch -- skipping")
                has_cond_fix = False

        if has_result_fix:
            if r.get("result") == item["result_old"]:
                update_set["result"] = item["result_new"]
                print(f"  result   : ✅ matched -- will update")
                any_fix = True
            else:
                print(f"  result   : ⚠️  mismatch -- skipping")
                has_result_fix = False

        print(f"  note     : {item['note'][:100]}...")

        if args.apply:
            res = col.update_one(
                {"rule_id": rid},
                {"$set": update_set,
                 "$unset": {"validation.flag_reason": "",
                            "validation.spot_check_reason": ""}},
            )
            if res.modified_count:
                action = "FIX + APPROVED" if any_fix else "APPROVED"
                print(f"  ✅ {action}\n")
                promoted += 1
            else:
                print(f"  ⚠️  No change written\n")
        else:
            action = "WOULD FIX + APPROVE" if any_fix else "WOULD APPROVE"
            print(f"  🔍 {action}\n")
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
        print(f"Dry run: {promoted} / {len(ITEMS)} would be processed.")
        print("Re-run with --apply to write.")

    client.close()


if __name__ == "__main__":
    main()
