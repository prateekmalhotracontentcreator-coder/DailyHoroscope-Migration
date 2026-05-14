#!/usr/bin/env python3
"""
approve_mundane_cat_a_nlm_batch.py

Fixes + approves 5 Category A NLM-batch rules after validation.

  1. mundane-gaur-ch10-mercury-motion-differentials  [result fix + approve]
     Spot_check. Result misleadingly says "reverses grain vs gur price signals"
     -- but gur is expensive in BOTH Direct AND Retrograde states; only grains
     reverse. Fix result to accurately describe which commodity reverses.

  2. mundane-mehta-ch20-terrorism-ten-parameters  [result fix + approve]
     Flagged: (a) "truncated" -- FALSE, condition is 1774 chars and complete.
     (b) Result has analyst-derived thresholds (4+, 6+ parameters, "core terror
     quartet", "military-grade coordination") not in Rao's source text.
     Fix: remove analyst thresholds from result; keep Rao's actual framework.

  3. mundane-mehta-ch26-retrograde-malefic-dasha-crisis  [result fix + approve]
     Flagged: (a) "truncated" -- FALSE, condition is complete per NLM.
     (b) "Triple convergence" (party chart + leader's personal chart + India's
     national chart) is a synthetic cross-chart construct Mehta does not state.
     Fix: remove triple-convergence methodology from result; keep party-chart
     analysis only as sourced in Mehta/Rao Ch26.

  4. mundane-mehta-ch26-congress-i-dasha-history  [approve -- false flag]
     Spot_check. Validator confirmed dasha correlations "anchor major events
     and are internally consistent." Approve.

  5. mundane-mehta-ch26-bjp-dasha-history  [approve -- false flag]
     Spot_check. Validator confirmed correlations "plausible within Mehta/Rao's
     political pattern framework." Approve.

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_cat_a_nlm_batch.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_cat_a_nlm_batch.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

ITEMS = [
    # ── 1. mercury-motion-differentials ──────────────────────────────────────
    {
        "rule_id":      "mundane-gaur-ch10-mercury-motion-differentials",
        "result_old": (
            "Mercury's motion state reverses grain vs gur price signals. "
            "Direct = grains up, gur/khand up. Retrograde = grains down, "
            "gur/khand up. Combusted = grains down."
        ),
        "result_new": (
            "Mercury's motion state determines commodity price direction. "
            "Only grains reverse between motion states: Direct → grains "
            "expensive; Retrograde → grains cheap. Gur, khand, and perfumes "
            "remain expensive in BOTH Direct and Retrograde states -- they do "
            "not reverse. Rising → wheat and gram expensive. Combusted → "
            "grains and ghee cheap. Source: Gaur Ch 10, pp.98."
        ),
        "note": (
            "False flag (spot_check). Validator found internal contradiction "
            "in result -- 'reverses grain vs gur signals' was misleading since "
            "gur/khand is expensive in both Direct and Retrograde states; only "
            "grains reverse. Result updated to accurately describe the per-commodity "
            "directionality. NLM confirmed Direct motion text: 'Gur and perfumes "
            "also expensive.' Approved by co-founder."
        ),
    },

    # ── 2. terrorism-ten-parameters ──────────────────────────────────────────
    {
        "rule_id":      "mundane-mehta-ch20-terrorism-ten-parameters",
        "result_old": (
            "When 4+ parameters are simultaneously active in any national or "
            "world chart, increased terrorist activity is indicated. When 6+ "
            "parameters converge with an eclipse active within 4 months -- "
            "catastrophic multi-casualty event risk. Parameters 1+2+3+6 "
            "together constitute the core terror quartet. When parameter 8 "
            "(retrograde Mars) is also active, the event is likely to involve "
            "military-grade coordination and mass casualties."
        ),
        "result_new": (
            "When multiple parameters from K.N. Rao's list are simultaneously "
            "active in a national or world chart, increased terrorist activity "
            "risk is indicated. The more parameters that converge, the higher "
            "the severity. Eclipse activation (parameter 9) adds timing "
            "precision. Retrograde Mars (parameter 8) intensifies destructive "
            "potential. Source: K.N. Rao, Journal of Astrology, "
            "July-September 2002 (Mehta/Rao Ch20)."
        ),
        "note": (
            "False flag (flagged). Validator hallucinated truncation -- condition "
            "is 1774 chars and contains all 10 parameters per NLM. Result fixed: "
            "removed analyst-derived specifics not in Rao's source ('4+ threshold', "
            "'6+ catastrophic', 'core terror quartet' label, 'military-grade "
            "coordination' claim). Kept Rao's actual framework: multiple parameter "
            "convergence = elevated terrorism risk. Approved by co-founder."
        ),
    },

    # ── 3. retrograde-malefic-dasha-crisis ───────────────────────────────────
    {
        "rule_id":      "mundane-mehta-ch26-retrograde-malefic-dasha-crisis",
        "result_old": (
            "Monitor: (1) Is the current Mahadasha lord of the party chart a "
            "retrograde malefic? (2) Is the leader's personal chart also showing "
            "marka dasha? (3) Is India's national chart simultaneously showing "
            "8th lord activation or Rahu-marka-house conjunction? Triple "
            "convergence = very high risk of leader assassination or sudden "
            "violent death. Single signal alone = heightened vigilance only."
        ),
        "result_new": (
            "Monitor the active Mahadasha lord in the political party's natal "
            "chart: retrograde malefic Mahadasha = elevated risk of major "
            "disruption or violent leadership change. Mars R as Mahadasha lord "
            "(marka house lord + intensified violence) = assassination risk. "
            "Rahu/Rahu chidra dasha = transition period of extreme vulnerability. "
            "Compound signal: retrograde malefic Mahadasha + Rahu placed in "
            "marka house (2nd/7th) of the party chart = high probability of "
            "violent death to the party leader. Analysis confined to the party "
            "natal chart; cross-referencing with the leader's personal chart or "
            "India's national chart adds context but is not part of Mehta/Rao's "
            "stated methodology. Source: Mehta/Rao Ch26."
        ),
        "note": (
            "False flag (flagged). Validator hallucinated truncation -- condition "
            "is complete per NLM. Result fixed: removed 'triple convergence' "
            "cross-chart methodology (party + leader's personal + India's "
            "national chart) -- this is a synthetic construct not stated in "
            "Mehta/Rao Ch26. Kept party-chart-only analysis as sourced. NLM "
            "confirmed all four sub-rules. Approved by co-founder."
        ),
    },

    # ── 4. congress-i-dasha-history ──────────────────────────────────────────
    {
        "rule_id":      "mundane-mehta-ch26-congress-i-dasha-history",
        "result_old":   None,
        "result_new":   None,
        "note": (
            "False flag (spot_check). Validator confirmed dasha correlations "
            "'anchor major events and are internally consistent.' NLM verified "
            "all correlations (Moon-Mercury 1980, Mars Dasha 1984, Rahu chidra "
            "dasha 1991, Rahu/Venus 2004). Approved by co-founder."
        ),
    },

    # ── 5. bjp-dasha-history ─────────────────────────────────────────────────
    {
        "rule_id":      "mundane-mehta-ch26-bjp-dasha-history",
        "result_old":   None,
        "result_new":   None,
        "note": (
            "False flag (spot_check). Validator confirmed correlations 'plausible "
            "within Mehta/Rao's political party pattern framework.' NLM verified "
            "all correlations (Mercury-Rahu/Ketu axis, Ketu/Jupiter 1989, "
            "Venus/Venus 1992, Venus/Mars-Rahu 1998-99, Venus/Jupiter 2004). "
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
    print(f"Category A NLM batch approvals ({len(ITEMS)} rules)")
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
            "validation.approved_by":   "co_founder_cat_a_nlm_batch_may2026",
            "validation.approved_at":   now,
            "validation.approved_note": item["note"],
        }

        has_result_fix = item["result_old"] is not None
        if has_result_fix:
            current_result = r.get("result", "")
            if current_result == item["result_old"]:
                update_set["result"] = item["result_new"]
                print(f"  result fix: ✅ matched -- will update")
            else:
                print(f"  result fix: ⚠️  mismatch -- skipping result update")
                has_result_fix = False

        print(f"  note   : {item['note'][:100]}...")

        if args.apply:
            res = col.update_one(
                {"rule_id": rid},
                {"$set": update_set,
                 "$unset": {"validation.flag_reason": ""}},
            )
            if res.modified_count:
                action = "RESULT FIX + APPROVED" if has_result_fix else "APPROVED"
                print(f"  ✅ {action}\n")
                promoted += 1
            else:
                print(f"  ⚠️  No change written\n")
        else:
            action = "RESULT FIX + APPROVE" if has_result_fix else "APPROVE"
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
