#!/usr/bin/env python3
"""
patch_approve_mundane_nlm_source_fixes.py

7 PHR rules -- NLM-verified, approved with co-founder review remarks.
NO conditions or results are stripped. Analyst logic that is directionally
correct but unverified is kept intact and flagged for co-founder review.

Rules and remarks:

  1. gaur-ch6-ownership-rain-confirm
     Approved. NLM confirmed: cross-ownership rain signal is in Gaur Ch6.
     CO-FOUNDER REVIEW: "24-48 hour" timing window is analyst-added (Gaur states
     only "there will be rains"). Timing is plausible but unverified. Review whether
     to keep, narrow, or remove.

  2. gaur-ch8-gold-reserve-banking-crisis-veto
     Approved. CO-FOUNDER REVIEW: (a) "Sanghatta grid" is a Mehta Ch8 term -- Gaur
     Ch8 does not use it. (b) Triple condition is analyst-synthesised from Gaur Ch8
     significations + Mehta Ch8 Vedha methodology. Core logic (Sun+Jupiter Vedha +
     Saturn in Capricorn = gold/banking stress) is directionally sound; confirm
     whether to keep as synthesis rule or split into separate Gaur/Mehta entries.

  3. gaur-ch10-jupiter-cancer-sun-aspect-supremacy
     Approved. CO-FOUNDER REVIEW: "trine" is Western terminology not in Gaur Ch10.
     Vedic equivalent = Jupiter's 9th-place Drishti. Logic (Sun-Jupiter Drishti in
     Jupiter's exaltation = Digvijay Yoga analog) is sound -- confirm Vedic
     terminology and whether the Digvijay Yoga label is appropriate.

  4. mundane-mehta-ch22-saturn-dhanesh-treasury-depletion
     Approved. CO-FOUNDER REVIEW: "Dhanesh appointed at Sun's entry into Virgo" is
     Gaur Ch2 framework -- Mehta Ch22 uses Kalaprakasika 8-member cabinet with no
     Dhanesh. Core logic (Saturn as treasury lord + Mars aspect = depletion) is
     coherent; confirm whether to reassign source attribution to Gaur Ch2 or treat
     as synthesis rule. Dual-chart clause "(or within the Dhanesh appointment chart)"
     is ambiguous -- confirm whether one chart or both are intended.

  5. mundane-gopal-ch3-widow-pm-multiplier
     Approved. NLM confirmed: Gopal documents qualitative longevity pattern (unmarried/
     widowed + Saturn 10th lord = extended tenure). CO-FOUNDER REVIEW: "+0.2 weight
     multiplier" is analyst-derived numeric coefficient not in Gopalakrishnan's text.
     Direction of signal is correct. Confirm whether to keep the coefficient, adjust
     its value, or replace with qualitative language only.

  6. mundane-gopal-ch4-volatile-nomination-chart
     Approved. CO-FOUNDER REVIEW: "2 or more planets at Rasi Sandhi" threshold is
     analyst-derived. Gopalakrishnan uses qualitative case-study language (4 planets
     in one example; 1 "spoiler" in another). Confirm whether the "2+" count is the
     right universal threshold or should be expressed as a qualitative signal.

  7. mundane-gopal-ch11-rains-rahu-capricorn-moderate
     Approved. NLM confirmed: Gopal Ch11 includes Capricorn in the Rahu Transit Veto
     system. CO-FOUNDER REVIEW: "NE monsoon disruption," "Himalayan watershed stress,"
     "erratic J&K/Himachal snowfall," and "Gangetic plain river flow reduction" are
     analyst-added meteorological interpretations not in Gopal's Ch11 source text.
     Logic is directionally plausible. Confirm whether to retain, narrow, or remove
     these regional specifics.

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_approve_mundane_nlm_source_fixes.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_approve_mundane_nlm_source_fixes.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

ITEMS = [

    # ── 1. gaur-ch6-ownership-rain-confirm ───────────────────────────────────
    {
        "rule_id": "mundane-gaur-ch6-ownership-rain-confirm",
        "note": (
            "NLM Q1 confirmed: Gaur Ch6 'Constellation Number Indication Chart' "
            "explicitly states 'When Sun is in Moon's constellation and Moon is on "
            "Sun's constellation... there will be rains.' Cross-ownership rain signal "
            "is source-verified. CO-FOUNDER REVIEW: The '24-48 hour' timing window in "
            "the result is analyst-added -- Gaur Ch6 states only 'there will be rains' "
            "with no specific timing for this configuration (Gaur provides 36-72 hours "
            "for Jala Nadi bundling, a different rule). Timing window is plausible but "
            "unverified for this specific cross-ownership pattern. Condition and result "
            "kept intact. Approved by co-founder; timing precision to be confirmed."
        ),
    },

    # ── 2. gaur-ch8-gold-reserve-banking-crisis-veto ─────────────────────────
    {
        "rule_id": "gaur-ch8-gold-reserve-banking-crisis-veto",
        "note": (
            "NLM Q2 audit: Core logic (Sun+Jupiter = Gold significators per Gaur Ch8; "
            "Vedha + Saturn in Capricorn = gold/banking crisis) is directionally sound. "
            "CO-FOUNDER REVIEW: (a) 'Sanghatta grid' is Mehta Ch8 terminology -- Gaur "
            "Ch8 does not define a Sanghatta grid; Gaur Ch8 is a significations list. "
            "(b) The triple condition (Sun-Jupiter mutual Vedha + Saturn in Capricorn) "
            "is analyst-synthesised from Gaur Ch8 significations + Mehta Ch8 Vedha "
            "methodology; it is not a single explicit Gaur Ch8 statement. Condition and "
            "result kept intact. Confirm: (1) whether to label as synthesis rule; "
            "(2) whether the Sanghatta/Vedha methodology attribution should reference "
            "Mehta Ch8 explicitly. Approved by co-founder; attribution to be confirmed."
        ),
    },

    # ── 3. gaur-ch10-jupiter-cancer-sun-aspect-supremacy ─────────────────────
    {
        "rule_id": "gaur-ch10-jupiter-cancer-sun-aspect-supremacy",
        "note": (
            "NLM Q3 audit: Jupiter in Cancer (exaltation) + Sun-Jupiter connection "
            "producing global supremacy signal is a Gaur Ch10 concept. CO-FOUNDER "
            "REVIEW: 'Trine' is a Western astrological term not used in Gaur Ch10. "
            "In Vedic astrology the 120° relationship is Jupiter's 9th-place Drishti "
            "(special aspect). NLM identified this configuration as a Digvijay Yoga "
            "analog in Gaur's framework. Logic is correct; terminology is non-standard. "
            "Condition kept intact. Confirm: (1) whether 'trine' should be replaced "
            "with '9th-place Drishti'; (2) whether 'Digvijay Yoga' is the correct "
            "label. Approved by co-founder; terminology to be standardised."
        ),
    },

    # ── 4. mundane-mehta-ch22-saturn-dhanesh-treasury-depletion ──────────────
    {
        "rule_id": "mundane-mehta-ch22-saturn-dhanesh-treasury-depletion",
        "note": (
            "NLM Q7 audit: Core logic (Saturn as treasury lord + Mars aspect = "
            "treasury depletion) is coherent. CO-FOUNDER REVIEW: (a) 'Dhanesh "
            "(Lord of Treasury) appointed at Sun's entry into Virgo' is a Gaur Ch2 "
            "concept -- Mehta Ch22 uses the Kalaprakasika 8-member cabinet system "
            "(Raja/Mantri/Sasya/Nira/Megha/Rasa/Dhanvantari/Arghya) which has no "
            "Dhanesh position. Source attribution in rule_id and condition references "
            "Mehta Ch22 but the Dhanesh framework belongs to Gaur Ch2. (b) The clause "
            "'or within the Dhanesh appointment chart' is an ambiguous dual-chart "
            "reference -- confirm whether New Year chart only, or Dhanesh appointment "
            "chart only, or both are intended. Condition and result kept intact. "
            "Confirm correct source attribution and resolve dual-chart ambiguity. "
            "Approved by co-founder; source attribution to be corrected."
        ),
    },

    # ── 5. mundane-gopal-ch3-widow-pm-multiplier ─────────────────────────────
    {
        "rule_id": "mundane-gopal-ch3-widow-pm-multiplier",
        "note": (
            "NLM Q8 confirmed: Gopalakrishnan documents the qualitative observation "
            "that unmarried/widowed leaders with Saturn as 10th lord (Nehru, Indira "
            "Gandhi, Vajpayee) show patterns of extended PM tenure -- this observational "
            "finding IS in the source text. CO-FOUNDER REVIEW: The '+0.2 weight "
            "multiplier' is analyst-derived and does NOT appear in Gopalakrishnan's "
            "text. The direction of the signal is confirmed; the specific numeric "
            "coefficient is unverified. Condition and result kept intact. Confirm: "
            "whether to keep +0.2, adjust its value, or replace with qualitative "
            "language. Approved by co-founder; coefficient to be confirmed."
        ),
    },

    # ── 6. mundane-gopal-ch4-volatile-nomination-chart ───────────────────────
    {
        "rule_id": "mundane-gopal-ch4-volatile-nomination-chart",
        "note": (
            "NLM Q9 confirmed: Gopalakrishnan identifies Rasi Sandhi planets as "
            "'spoilers' that negate candidate strength in case studies -- Kerry 2004 "
            "(single spoiler planet), Oommen Chandy government (four Rasi Sandhi "
            "planets). The Rasi Sandhi = volatile candidacy signal is source-confirmed. "
            "CO-FOUNDER REVIEW: The '2 or more planets' universal threshold is "
            "analyst-derived -- Gopalakrishnan uses qualitative case-study language "
            "without defining a specific count threshold for nomination charts. The "
            "threshold is plausible given the case studies but is not explicitly stated. "
            "Condition and result kept intact. Confirm: whether '2 or more' is the "
            "right threshold or should be expressed as a qualitative signal. "
            "Approved by co-founder; threshold to be confirmed."
        ),
    },

    # ── 7. mundane-gopal-ch11-rains-rahu-capricorn-moderate ──────────────────
    {
        "rule_id": "mundane-gopal-ch11-rains-rahu-capricorn-moderate",
        "note": (
            "NLM Q10 confirmed: Gopalakrishnan Ch11 Rahu Transit Veto system includes "
            "Capricorn (Makara) as a sign where Rahu's transit causes general problems "
            "with rainfall in India. Core rain-veto signal is source-verified. "
            "CO-FOUNDER REVIEW: The specific regional details in the result -- 'NE "
            "monsoon disruption,' 'Himalayan watershed stress,' 'erratic J&K/Himachal "
            "snowfall,' 'Gangetic plain river flow reduction' -- are analyst-added "
            "meteorological interpretations that do NOT appear in Gopalakrishnan's "
            "Ch11 source text. These interpretations are directionally plausible for "
            "Rahu in Capricorn (earth sign, winter season) but are unverified. "
            "Result kept intact. Confirm: whether to retain, narrow, or remove these "
            "regional specifics. Approved by co-founder; regional detail to be confirmed."
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
    print(f"NLM-verified approvals + co-founder remarks ({len(ITEMS)} rules)")
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
            "validation.approved_by":   "co_founder_nlm_verified_may2026",
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
                print(f"  ✅ APPROVED (with co-founder review remarks)\n")
                promoted += 1
            else:
                print(f"  ⚠️  No change written\n")
        else:
            print(f"  🔍 WOULD APPROVE (with co-founder review remarks)\n")
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
