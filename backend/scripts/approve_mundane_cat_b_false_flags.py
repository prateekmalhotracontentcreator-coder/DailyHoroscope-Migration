#!/usr/bin/env python3
"""
approve_mundane_cat_b_false_flags.py

Promotes 7 Category B rules from flagged/pending_human_review → approved.

All 7 were re-flagged by the validator after arithmetic artifact removal.
Both NLM and Google AI independently confirmed all 7 as false flags —
the validator applied classical Sanskrit standards to the modern empirical
methodologies of Gopalakrishnan (Ch4/5/12/14) and Mehta (Ch10).

Source anchors confirmed per rule:
  1. mehta-ch10-saturn-rahu-capricorn     — Mehta Ch10 1991 Gulf War audit
  2. gopal-ch14-mars-perigee-mfg          — Gopal Ch14 Mars perigee ontology
  3. gopal-ch5-hora-lagna-fixed-veto      — Gopal Ch5 p.73 Oommen Chandy double-fixed
  4. gopal-ch5-rasi-sandhi-veto           — Gopal Ch5 p.74 Oommen Chandy 4-planet hit
  5. gopal-ch4-destiny-anchor-karkamsha   — Jaimini Karkamsha for electoral destiny
  6. gopal-ch4-eleventh-house-dasha-surge — Gopal Ch4 11th house winning momentum
  7. gopal-ch12-india-bpo-destiny         — Gopal Ch12 p.191 "BACK BONE of BPO"

Usage:
  # Dry run:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_cat_b_false_flags.py --mongo-url "$MONGO_URL"

  # Apply:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_cat_b_false_flags.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

APPROVALS: dict[str, str] = {
    "mehta-ch10-saturn-rahu-capricorn-regime-change": (
        "False flag (content_validity_dispute) — validator objected to geographic "
        "attribution but Mehta explicitly audits the 1991 Gulf War in Ch10, linking "
        "Saturn-Rahu in Capricorn to catastrophic defeat in the Middle East and "
        "regional economic paradigm shift. NLM + Google AI confirmed source anchor."
    ),
    "mundane-gopal-ch14-mars-perigee-manufacturing": (
        "False flag (content_validity_dispute) — validator objected that Mars perigee "
        "is not in the classical Vedic framework. Correct, but Gopalakrishnan explicitly "
        "uses Mars perigee in Ch14 as part of his 21st-century mundane ontology — "
        "this is the documented methodology of the source. NLM + Google AI confirmed."
    ),
    "mundane-gopal-ch5-hora-lagna-fixed-veto": (
        "False flag (content_validity_dispute) — validator said double-fixed veto is "
        "not explicitly documented. Incorrect: Gopalakrishnan Ch5 p.73 explicitly states "
        "'Both Lagna and hora lagna... are in fixed sign so it is short life' in the "
        "Oommen Chandy case analysis. NLM confirmed source anchor."
    ),
    "mundane-gopal-ch5-rasi-sandhi-veto": (
        "False flag (content_validity_dispute) — validator objected to missing explicit "
        "threshold. Rule already corrected: 'multiple planets' replaces '4 or more', "
        "with Oommen Chandy 4-planet case (Gopal Ch5 p.74) as the documented benchmark. "
        "NLM confirmed this is source-faithful. Google AI confirmed as documented refinement."
    ),
    "mundane-gopal-ch4-destiny-anchor-karkamsha": (
        "False flag (content_validity_dispute) — validator incorrectly stated Karkamsha "
        "is a D-7 chart for spiritual evolution. Karkamsha is a Jaimini concept (Atmakaraka "
        "in navamsa). Gopalakrishnan explicitly mandates checking 10th lord strength from "
        "Karkamsha Lagna to determine electoral destiny and global greatness. "
        "NLM + Google AI confirmed source anchor."
    ),
    "mundane-gopal-ch4-eleventh-house-dasha-surge": (
        "False flag (content_validity_dispute) — validator challenged 'single most reliable' "
        "claim and Bush 2000 case. Gopalakrishnan defines the 11th house as the house of "
        "fulfillment of desires and winning momentum in Ch4, and his methodology explicitly "
        "prioritises the 11th house Dasha as the decisive timing push for electoral victory. "
        "NLM + Google AI confirmed source anchor."
    ),
    "mundane-gopal-ch12-india-bpo-destiny-3rd-house": (
        "False flag (content_validity_dispute) — validator objected to 'EVERGREEN planetary "
        "mandate' as unfalsifiable. The source text (Gopal Ch12 p.191) uses the literal "
        "phrase 'India will surely become the BACK BONE of BPO in the world in the coming "
        "years.' Rule faithfully captures this stated natal promise. NLM + Google AI "
        "confirmed source anchor."
    ),
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
    print(f"Category B false flag approvals ({len(APPROVALS)} rules)")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    promoted = 0
    for rid, note in APPROVALS.items():
        r = col.find_one(
            {"rule_id": rid, "science_id": "mundane_jyotish"},
            {"_id": 0, "rule_id": 1, "approval_status": 1, "title": 1},
        )
        if not r:
            print(f"  ⚠️  NOT FOUND: {rid}\n")
            continue

        status = r.get("approval_status", "?")
        print(f"  {rid}")
        print(f"  status : {status}")
        print(f"  note   : {note[:100]}…")

        if args.apply:
            result = col.update_one(
                {"rule_id": rid},
                {"$set": {
                    "approval_status":          "approved",
                    "validation.verdict":       "approved",
                    "validation.approved_by":   "co_founder_nlm_googleai_false_flag_may2026",
                    "validation.approved_at":   now,
                    "validation.approved_note": note,
                }},
            )
            if result.modified_count:
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
        flagged = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "flagged"}
        )
        print(f"Promoted : {promoted} / {len(APPROVALS)}")
        print(f"\nLibrary status:")
        print(f"  approved             : {approved}")
        print(f"  pending_human_review : {phr}")
        print(f"  flagged              : {flagged}")
    else:
        print(f"Dry run: {promoted} / {len(APPROVALS)} rules would be approved.")
        print(f"Re-run with --apply to write.")

    client.close()


if __name__ == "__main__":
    main()
