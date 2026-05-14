#!/usr/bin/env python3
"""
patch_mundane_cat_c3_eclipse_rules.py

Applies NLM-verified fixes to 3 remaining Category C3 rules.

  1. mundane-mehta-ch13-eclipse-lord-placement  [condition + result rewrite]
     Current condition is mangled -- prefixes each tier with "IF Saturn in Xth
     house placement" when Saturn has nothing to do with the rule. The rule is
     about the eclipse SIGN LORD's placement. Result contains an unsourced
     "famine/pestilence" claim not found in NLM's Ch13 findings.
     Fix: rewrite condition as clean 3-tier IF/THEN. Remove famine claim.

  2. mundane-mehta-ch13-eclipse-ruler-royalty  [condition completion only]
     Condition is truncated mid-sentence ("Events may happen pr...") -- Cat A
     truncation artifact. Content is correct per NLM. Complete the truncated
     condition only; result is accurate as-is.

  3. mundane-mehta-ch22-raja-mantri-enemy-deadlock  [retire]
     NLM confirmed: Mehta Ch22 lists individual Raja/Mantri results but does
     NOT explicitly describe a Raja-Mantri deadlock/opposition scenario.
     "Policy deadlock and cabinet bickering" follows general astrological
     enmity principles but is an interpretive synthesis, not a literal Mehta
     citation. Retire from mundane library (same treatment as trikona-billionaire).

NLM source (May 2026):
  Q4: Mehta Ch13 eclipse lord → 8th house = deaths/accidents; 6th = diseases;
      3rd = rail/road/air accidents or strikes.
  Q5: Eclipse on/opposite ruler's natal Sun/Moon/Asc = mostly auspicious
      (elevation). If afflicted by BOTH Mars AND Saturn = assassination risk.
  Q6: No explicit Raja-Mantri deadlock in Mehta Ch22. Interpretive synthesis
      confirmed.

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_mundane_cat_c3_eclipse_rules.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_mundane_cat_c3_eclipse_rules.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

# ── Patches ───────────────────────────────────────────────────────────────────

ECLIPSE_LORD_CONDITION_OLD = (
    "IF Saturn in 8th house placement → Eclipse sign lord in 8th house → serious "
    "deaths and accidents. IF Saturn in 6th house placement → Eclipse sign lord in "
    "6th house → may cause diseases. IF Saturn in 3rd house placement → Eclipse "
    "sign lord in 3rd house → rail, road and air accidents or strikes in railways.."
)
ECLIPSE_LORD_CONDITION_NEW = (
    "Identify the zodiac sign containing the eclipse (solar or lunar). Find the "
    "planetary lord of that sign. Check that planet's house position in the "
    "national horoscope (India Independence chart or applicable national chart): "
    "IF eclipse sign lord is in the 8th house → serious deaths and accidents at "
    "national level. "
    "IF eclipse sign lord is in the 6th house → outbreak of diseases. "
    "IF eclipse sign lord is in the 3rd house → rail, road, and air accidents, "
    "or strikes in the transport/railway sector. "
    "Source: Mehta Ch13."
)

ECLIPSE_LORD_RESULT_OLD = (
    "After identifying eclipse sign, check its lord's natal house position in the "
    "national horoscope. 8th placement = death/accident signal. 3rd placement = "
    "transport crisis. Total eclipse + malefic aspect = national famine/pestilence trigger."
)
ECLIPSE_LORD_RESULT_NEW = (
    "After identifying the eclipse sign, locate its planetary lord in the national "
    "horoscope. 8th house placement = national death/accident alert. 6th house "
    "placement = disease/epidemic alert. 3rd house placement = transport sector "
    "crisis (rail, road, air accidents or strikes). Source: Mehta Ch13. "
    "Note: 'Total eclipse + famine/pestilence' attribution removed -- not found in "
    "Mehta Ch13 per NLM source verification."
)

ECLIPSE_ROYALTY_CONDITION_OLD = (
    "IF timing: Events may happen within 4 months of solar eclipse and a week of "
    "lunar eclipse. Events may happen pr...; auspicious rule: Eclipse on or in "
    "opposition to natal Sun, Moon or ascendant of a ruler → mostly auspicious; "
    "elevatio...; auspicious examples: Duke of York: natal Sun fell on eclipse "
    "13 Dec 1936 → became King George VI; inauspicious rule: Eclipse afflicted "
    "by BOTH Mars and Saturn → ominous for causing death by assassination.."
)
ECLIPSE_ROYALTY_CONDITION_NEW = (
    "For any ruling head of state, check whether the current eclipse (solar or "
    "lunar) falls on or in opposition to their natal Sun, Moon, or Ascendant: "
    "AUSPICIOUS: Eclipse at these sensitive natal points without Mars/Saturn "
    "affliction → mostly auspicious; indicates elevation, promotion, or accession "
    "to higher office. Example: Duke of York -- natal Sun fell on eclipse 13 Dec "
    "1936 → became King George VI (Harry Truman case similarly confirmed). "
    "OMINOUS: Eclipse at these sensitive natal points AND afflicted by BOTH Mars "
    "AND Saturn → ominous for death by assassination or death in office. "
    "TIMING: Solar eclipse effects manifest within approximately 4 months. Lunar "
    "eclipse effects manifest within approximately 1 week. "
    "ADDITIONAL: Two eclipses occurring within 15 days of each other → war imminent. "
    "Source: Mehta Ch13."
)

RETIREMENT_NOTE = (
    "INTERPRETIVE SYNTHESIS -- NOT EXPLICIT MEHTA CH22 TEXT. NLM confirmed: Mehta "
    "Ch22 lists individual results for the Raja and Mantri of the year but does NOT "
    "explicitly describe a Raja-Mantri opposition/deadlock scenario. 'Policy deadlock "
    "and cabinet bickering' follows general astrological enmity principles (inimical "
    "planetary pairs) applied to Mehta's Raja-Mantri framework -- it is analyst "
    "inference, not a literal Mehta citation. Retired pending explicit source "
    "discovery or reclassification as a derived rule. NLM review May 2026."
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
    print(f"Category C3 eclipse rules -- NLM corrections (3 rules)")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    patched = 0

    # ── 1. eclipse-lord-placement: rewrite condition + result ─────────────────
    rid = "mundane-mehta-ch13-eclipse-lord-placement"
    r = col.find_one({"rule_id": rid}, {"condition": 1, "result": 1, "approval_status": 1, "_id": 0})
    if not r:
        print(f"  ⚠️  NOT FOUND: {rid}\n")
    else:
        print(f"  {rid}")
        print(f"  status : {r.get('approval_status','?')}")
        cond_match = r.get("condition","") == ECLIPSE_LORD_CONDITION_OLD
        res_match  = r.get("result","")    == ECLIPSE_LORD_RESULT_OLD
        print(f"  condition match : {'✅' if cond_match else '⚠️  MISMATCH'}")
        print(f"  result match    : {'✅' if res_match else '⚠️  MISMATCH'}")

        if cond_match and res_match:
            if args.apply:
                col.update_one(
                    {"rule_id": rid},
                    {"$set": {
                        "condition":               ECLIPSE_LORD_CONDITION_NEW,
                        "result":                  ECLIPSE_LORD_RESULT_NEW,
                        "approval_status":         "pending_review",
                        "validation.patch_reason": "cat_c3_nlm_eclipse_lord_fix",
                        "validation.patch_note":   (
                            "Condition: removed erroneous 'Saturn' prefix from each tier; "
                            "rewritten as clean 3-tier eclipse-sign-lord placement rule. "
                            "Result: removed unsourced 'famine/pestilence' claim. "
                            "NLM confirmed: Mehta Ch13 -- 8th=deaths, 6th=diseases, "
                            "3rd=transport accidents."
                        ),
                        "validation.patched_at":   now,
                        "validation.patched_by":   "patch_mundane_cat_c3_eclipse_rules.py",
                    },
                    "$unset": {"validation.verdict": "", "validation.flag_reason": ""}},
                )
                print(f"  ✅ Patched → pending_review\n")
                patched += 1
            else:
                print(f"  🔍 WOULD PATCH → pending_review\n")
                patched += 1
        else:
            print(f"  ⚠️  Skipping -- field content does not match expected (already patched?)\n")

    # ── 2. eclipse-ruler-royalty: complete truncated condition ────────────────
    rid = "mundane-mehta-ch13-eclipse-ruler-royalty"
    r = col.find_one({"rule_id": rid}, {"condition": 1, "approval_status": 1, "_id": 0})
    if not r:
        print(f"  ⚠️  NOT FOUND: {rid}\n")
    else:
        print(f"  {rid}")
        print(f"  status : {r.get('approval_status','?')}")
        current_cond = r.get("condition", "")
        is_truncated = "pr..." in current_cond or "elevatio..." in current_cond
        print(f"  truncated       : {'✅ yes' if is_truncated else '⚠️  not detected -- check manually'}")

        if args.apply:
            col.update_one(
                {"rule_id": rid},
                {"$set": {
                    "condition":               ECLIPSE_ROYALTY_CONDITION_NEW,
                    "approval_status":         "pending_review",
                    "validation.patch_reason": "cat_c3_nlm_eclipse_royalty_truncation_fix",
                    "validation.patch_note":   (
                        "Condition was truncated (Cat A artifact). Completed with full "
                        "Mehta Ch13 rule text per NLM source verification: "
                        "auspicious = elevation; afflicted by Mars+Saturn = assassination "
                        "risk; solar = 4 months; lunar = 1 week; dual eclipse = war."
                    ),
                    "validation.patched_at":   now,
                    "validation.patched_by":   "patch_mundane_cat_c3_eclipse_rules.py",
                },
                "$unset": {"validation.verdict": "", "validation.flag_reason": ""}},
            )
            print(f"  ✅ Patched → pending_review\n")
            patched += 1
        else:
            print(f"  🔍 WOULD PATCH condition (truncation fix) → pending_review\n")
            patched += 1

    # ── 3. raja-mantri-enemy-deadlock: retire ────────────────────────────────
    rid = "mundane-mehta-ch22-raja-mantri-enemy-deadlock"
    r = col.find_one({"rule_id": rid}, {"approval_status": 1, "_id": 0})
    if not r:
        print(f"  ⚠️  NOT FOUND: {rid}\n")
    else:
        print(f"  {rid}")
        print(f"  status : {r.get('approval_status','?')}")
        print(f"  action : RETIRE → pending_human_review (interpretive synthesis, not source)")

        if args.apply:
            col.update_one(
                {"rule_id": rid},
                {"$set": {
                    "approval_status":                "pending_human_review",
                    "validation.verdict":             "misclassified",
                    "validation.flag_reason":         RETIREMENT_NOTE,
                    "validation.classification_note": (
                        "UNSOURCED_SYNTHESIS: Raja-Mantri deadlock outcome not in Mehta "
                        "Ch22. Analyst inference based on general planetary enmity logic. "
                        "Retire or reclassify as derived rule."
                    ),
                    "validation.misclassified_at":    now,
                    "validation.misclassified_by":    "patch_mundane_cat_c3_eclipse_rules.py",
                }},
            )
            print(f"  ✅ Retired → pending_human_review\n")
            patched += 1
        else:
            print(f"  🔍 WOULD RETIRE → pending_human_review\n")
            patched += 1

    print(f"{'─'*65}")
    if args.apply:
        approved = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "approved"}
        )
        phr = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "pending_human_review"}
        )
        pending = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "pending_review"}
        )
        print(f"Patched : {patched} / 3")
        print(f"\nLibrary status:")
        print(f"  approved             : {approved}")
        print(f"  pending_human_review : {phr}")
        print(f"  pending_review       : {pending}")
    else:
        print(f"Dry run: {patched} / 3 would be patched.")
        print(f"Re-run with --apply to write.")

    client.close()


if __name__ == "__main__":
    main()
