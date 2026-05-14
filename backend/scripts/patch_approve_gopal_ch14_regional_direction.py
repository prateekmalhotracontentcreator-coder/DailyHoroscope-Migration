#!/usr/bin/env python3
"""
patch_approve_gopal_ch14_regional_direction.py

Fixes + approves mundane-gopal-ch14-regional-direction-leadership.

NLM audit (May 2026):
  - Gopal Ch14 explicitly states only "Mars means south direction" -- using the
    Mars perigee → South India connection to explain the 2005-2006 replacement
    of multiple South Indian Chief Ministers (Kerala, Karnataka, Andhra Pradesh).
  - The full 6-planet directional mapping (Sun→East, Moon→NW, Mercury→North,
    Venus→SE, Saturn→West) is from Mehta Ch7, p.381 -- not Gopal Ch14. Its
    inclusion in the original condition was analyst synthesis.
  - "Proximity to Earth" = Mars perigee (Mars at opposition, ~60M km from Earth).
    Gopalakrishnan documents two windows: July 2003 + October 2005.

Fix:
  - Narrow condition to Mars only (Gopal's actual statement).
  - Remove the 5-planet extension -- that belongs to a Mehta Ch7 rule.
  - Define "proximity to Earth" explicitly as Mars perigee.
  - Update title and result to match Gopal's actual scope.
  - Note: Broader planetary directional framework (Mehta Ch7 p.381) can be
    encoded as a separate Mehta Ch7 rule if needed.

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_approve_gopal_ch14_regional_direction.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_approve_gopal_ch14_regional_direction.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

RULE_ID = "mundane-gopal-ch14-regional-direction-leadership"

OLD_CONDITION = (
    "IF (Malefic planet -- Mars, Saturn, or Rahu -- transits a sign strongly "
    "associated with a geographic direction) AND (That malefic is afflicted "
    "or in close proximity to Earth)"
)

NEW_CONDITION = (
    "IF Mars reaches perigee (opposition to Sun -- approximately 60M km from "
    "Earth, maximum terrestrial influence). Mars direction = South. "
    "Perigee windows documented by Gopalakrishnan: July 2003 and October 2005. "
    "Note: The broader 6-planet directional mapping (Sun→East, Moon→NW, "
    "Mercury→North, Venus→SE, Saturn→West) is from Mehta Ch7, p.381 -- not "
    "this rule. This rule applies to Mars perigee only. "
    "Source: Gopalakrishnan Ch 14 -- Hits of 2006."
)

OLD_RESULT = (
    "Regional Stability Alert: 'High probability of incumbency failure for "
    "leaders in the geographic direction associated with that sign/planet. "
    "Apply directional mapping: Sun→East, Venus→South-East, Mars→South, "
    "Saturn→West, Moon→North-West, Mercury→North'."
)

NEW_RESULT = (
    "South India Regional Alert: High probability of simultaneous incumbency "
    "failure for multiple Chief Ministers in South Indian states (Kerala, "
    "Karnataka, Andhra Pradesh -- the South direction governed by Mars). "
    "Manufacturing and industrial sectors in the South show above-normal growth "
    "and efficiency during the same perigee window. "
    "Validation: October 2005 Mars perigee → structural replacement of all "
    "South Indian Chief Ministers in the 2006 election cycle. "
    "Note: The 5-planet directional extension (Saturn→West, Sun→East, etc.) "
    "is sourced from Mehta Ch7 p.381 -- it is not part of Gopal Ch14's stated "
    "rule and should not be applied from this entry. "
    "Source: Gopalakrishnan Ch 14 -- Hits of 2006."
)

NEW_TITLE = "Mars Perigee -- South Indian Regional Leadership Change (South Direction)"

APPROVE_NOTE = (
    "Partial false flag + condition fix. NLM confirmed: Gopal Ch14 explicitly "
    "states only 'Mars means south direction' -- applied to explain simultaneous "
    "South Indian CM replacements (Kerala/Karnataka/AP) at Mars perigee "
    "(Oct 2005). The 5-planet directional mapping in the original condition "
    "(Sun→East, Moon→NW, etc.) is from Mehta Ch7 p.381, not Gopal Ch14 -- it "
    "was analyst synthesis. 'Proximity to Earth' clarified as Mars perigee "
    "(opposition). Condition narrowed to Mars only; result updated to Gopal's "
    "actual South India scope. Approved by co-founder."
)


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
    print(f"Patch + Approve: regional-direction-leadership")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    r = col.find_one(
        {"rule_id": RULE_ID, "science_id": "mundane_jyotish"},
        {"_id": 0, "rule_id": 1, "approval_status": 1,
         "condition": 1, "result": 1, "title": 1},
    )
    if not r:
        print(f"  ⚠️  NOT FOUND: {RULE_ID}")
        client.close()
        return

    print(f"  {RULE_ID}")
    print(f"  status : {r.get('approval_status','?')}")

    cond_match   = r.get("condition", "") == OLD_CONDITION
    result_match = r.get("result", "")   == OLD_RESULT

    print(f"  condition match : {'✅' if cond_match   else '⚠️  MISMATCH'}")
    print(f"  result match    : {'✅' if result_match else '⚠️  MISMATCH'}")
    if not cond_match:
        print(f"  DB condition tail: ...{r.get('condition','')[-80:]}")
    if not result_match:
        print(f"  DB result tail   : ...{r.get('result','')[-80:]}")

    print(f"  title → {NEW_TITLE}")
    print(f"  fix   : Remove 5-planet extension; define 'proximity to Earth' "
          f"as Mars perigee; narrow scope to South India")
    print(f"  note  : {APPROVE_NOTE[:100]}...")

    if args.apply and cond_match and result_match:
        res = col.update_one(
            {"rule_id": RULE_ID},
            {"$set": {
                "condition":                NEW_CONDITION,
                "result":                   NEW_RESULT,
                "title":                    NEW_TITLE,
                "approval_status":          "approved",
                "validation.verdict":       "approved",
                "validation.approved_by":   "co_founder_gopal_ch14_may2026",
                "validation.approved_at":   now,
                "validation.approved_note": APPROVE_NOTE,
            },
            "$unset": {"validation.flag_reason": "",
                       "validation.spot_check_reason": ""}},
        )
        if res.modified_count:
            print(f"\n  ✅ CONDITION + RESULT + TITLE FIXED AND APPROVED")
        else:
            print(f"\n  ⚠️  No change written")
    elif args.apply:
        print(f"\n  ⚠️  Skipping -- mismatch on condition or result")
    else:
        print(f"\n  🔍 WOULD FIX CONDITION + RESULT + TITLE + APPROVE")

    if args.apply:
        approved = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "approved"}
        )
        phr = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "pending_human_review"}
        )
        print(f"\nLibrary: approved={approved}  PHR={phr}")

    client.close()


if __name__ == "__main__":
    main()
