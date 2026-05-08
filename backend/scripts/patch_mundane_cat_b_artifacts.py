#!/usr/bin/env python3
"""
patch_mundane_cat_b_artifacts.py

Strips arithmetic artifacts (quantitative multipliers, coefficients, weight
modifiers) from 7 Category B PHR rules. All rules are made purely qualitative
so they can be re-validated and promoted to approved.

Changes per rule:
  1. mehta-ch10-saturn-rahu-capricorn-regime-change
     result: remove "(3× weight when within 1°)"

  2. mundane-gopal-ch14-mars-perigee-manufacturing
     result: "1.5× normal growth" → "significantly above-normal growth"

  3. mundane-gopal-ch5-hora-lagna-fixed-veto
     result: "Survival Probability coefficient = 0.10 (terminal)."
           → "Critical risk of premature collapse (terminal signal)."

  4. mundane-gopal-ch4-destiny-anchor-karkamsha
     result: remove sentence "Weight modifier: +0.30 to overall Tri-Lagna
             strength coefficient."

  5. mundane-gopal-ch4-eleventh-house-dasha-surge
     title:  remove "Winning Momentum Coefficient 0.90" → clean title
     result: "Winning Momentum coefficient = 0.90."
           → "Strongest surge for electoral victory."

  6. mundane-gopal-ch12-india-bpo-destiny-3rd-house
     result: remove sentence "Forecast modifier: +0.50 positive weight for
             all India IT/BPO/knowledge economy growth queries."

  7. mundane-gopal-ch5-rasi-sandhi-veto
     result: "Effective Governance coefficient = 0.20."
           → "Severe effective governance risk."

Usage:
  # Dry run:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_mundane_cat_b_artifacts.py --mongo-url "$MONGO_URL"

  # Apply:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_mundane_cat_b_artifacts.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

PATCHES: list[dict] = [
    {
        "rule_id": "mehta-ch10-saturn-rahu-capricorn-regime-change",
        "result_old": (
            "Major_Regime_Change_Middle_East = TRUE. Multi-planet concentration in "
            "Capricorn (especially within 1° orb) triggers 'Economic Paradigm Shift' "
            "AND 'Catastrophic Event' (3× weight when within 1°)."
        ),
        "result_new": (
            "Major regime change in the Middle East and South Asia is indicated. "
            "Multi-planet concentration in Capricorn, especially within 1° orb, "
            "triggers both an economic paradigm shift and catastrophic destabilising "
            "events. The closer the conjunction orb, the more severe and sudden the "
            "political disruption."
        ),
    },
    {
        "rule_id": "mundane-gopal-ch14-mars-perigee-manufacturing",
        "result_old": (
            "Manufacturing Boost: 'High efficiency in manufacturing units and electrical "
            "components. Automotive, medical equipment, and metal sectors achieve 1.5× "
            "normal growth. Auto ancillaries turn into export-oriented profit centres'. "
            "Note: Same transit also correlates with increased risk of fire accidents, "
            "blasts, and political violence."
        ),
        "result_new": (
            "Manufacturing Boost: High efficiency in manufacturing units and electrical "
            "components. Automotive, medical equipment, and metal sectors achieve "
            "significantly above-normal growth. Auto ancillaries turn into export-oriented "
            "profit centres. Note: The same transit also correlates with increased risk of "
            "fire accidents, blasts, and political violence."
        ),
    },
    {
        "rule_id": "mundane-gopal-ch5-hora-lagna-fixed-veto",
        "result_old": (
            "Survival Probability coefficient = 0.10 (terminal). This is the most "
            "dangerous configuration in oath chart analysis — the rigidity of both Lagna "
            "and Hora Lagna in Fixed signs signals near-certain premature collapse "
            "regardless of parliamentary majority. No amount of beneficial planetary "
            "support can override this structural veto. Government will not complete its "
            "mandate. Cross-check Jaimini Ayurdaya for confirmation."
        ),
        "result_new": (
            "Critical risk of premature collapse (terminal signal). This is the most "
            "dangerous configuration in oath chart analysis — the rigidity of both Lagna "
            "and Hora Lagna in Fixed signs signals near-certain premature collapse "
            "regardless of parliamentary majority. No amount of beneficial planetary "
            "support can override this structural veto. Government will not complete its "
            "mandate. Cross-check Jaimini Ayurdaya for confirmation."
        ),
    },
    {
        "rule_id": "mundane-gopal-ch4-destiny-anchor-karkamsha",
        "result_old": (
            "Destiny Alert: This candidate has a soul-level mandate for high political "
            "office. The Karkamsha represents the deepest destiny blueprint of the "
            "individual. A Trikona connection to the 10th lord here indicates that "
            "leadership is fated — the divine mandate for governance is present regardless "
            "of immediate transit conditions or opposition strength. Weight modifier: "
            "+0.30 to overall Tri-Lagna strength coefficient. A candidate with this "
            "configuration should never be written off, even when external political "
            "conditions appear unfavourable."
        ),
        "result_new": (
            "Destiny Alert: This candidate has a soul-level mandate for high political "
            "office. The Karkamsha represents the deepest destiny blueprint of the "
            "individual. A Trikona connection to the 10th lord here indicates that "
            "leadership is fated — the divine mandate for governance is present regardless "
            "of immediate transit conditions or opposition strength. A candidate with this "
            "configuration should never be written off, even when external political "
            "conditions appear unfavourable."
        ),
    },
    {
        "rule_id": "mundane-gopal-ch4-eleventh-house-dasha-surge",
        "title_old": "11th House Dasha Surge — Winning Momentum Coefficient 0.90",
        "title_new": "11th House Dasha Surge — Strongest Electoral Winning Momentum",
        "result_old": (
            "Winning Momentum coefficient = 0.90. The 11th house is the house of gains, "
            "fulfillment of desires, and electoral victory. A Dasha/Bhukti whose period "
            "lord occupies the 11th house from either key Lagna provides the decisive "
            "timing push for electoral victory. This is the single most reliable "
            "Dasha-level confirmation of a win. Validated: Bush 2000 — Saturn/Rahu Dasha "
            "with Rahu in 11th from Lagna. A candidate with a moderate Tri-Lagna score "
            "but 11th house Dasha lord can still win a close race."
        ),
        "result_new": (
            "Strongest surge for electoral victory. The 11th house is the house of gains, "
            "fulfillment of desires, and electoral victory. A Dasha/Bhukti whose period "
            "lord occupies the 11th house from either key Lagna provides the decisive "
            "timing push for electoral victory. This is the single most reliable "
            "Dasha-level confirmation of a win. Validated: Bush 2000 — Saturn/Rahu Dasha "
            "with Rahu in 11th from Lagna. A candidate with a moderate Tri-Lagna score "
            "but 11th house Dasha lord can still win a close race."
        ),
    },
    {
        "rule_id": "mundane-gopal-ch12-india-bpo-destiny-3rd-house",
        "result_old": (
            "STRUCTURAL DESTINY — EVERGREEN: The cluster of Mercury (communication, "
            "trade, data) and Venus (services, aesthetics, relational skills) in the 3rd "
            "house of India's Independence chart creates a natal promise: India is "
            "structurally destined to remain the global backbone of IT, BPO, and "
            "back-office processing. This is not a temporary trend driven by cost "
            "arbitrage — it is a planetary mandate. Forecast modifier: +0.50 positive "
            "weight for all India IT/BPO/knowledge economy growth queries. Even in "
            "periods of global IT downturn, India's share of global outsourcing will "
            "remain disproportionately high. The 3rd house also governs neighbors and "
            "short-distance connectivity — India's geographic and cultural proximity to "
            "the English-speaking world is a structural advantage, not a coincidence."
        ),
        "result_new": (
            "STRUCTURAL DESTINY — EVERGREEN: The cluster of Mercury (communication, "
            "trade, data) and Venus (services, aesthetics, relational skills) in the 3rd "
            "house of India's Independence chart creates a natal promise: India is "
            "structurally destined to remain the global backbone of IT, BPO, and "
            "back-office processing. This is not a temporary trend driven by cost "
            "arbitrage — it is a planetary mandate. Even in periods of global IT "
            "downturn, India's share of global outsourcing will remain "
            "disproportionately high. The 3rd house also governs neighbors and "
            "short-distance connectivity — India's geographic and cultural proximity to "
            "the English-speaking world is a structural advantage, not a coincidence."
        ),
    },
    {
        "rule_id": "mundane-gopal-ch5-rasi-sandhi-veto",
        # Condition also fixed: "4 or more" is an empirical benchmark from the
        # Oommen Chandy case study (Ch5), not a formalised classical threshold.
        # NLM confirmed: change to "multiple planets" with Chandy case as benchmark.
        "condition_old": (
            "IF 4 or more planets in the oath chart are placed at 0° or 29° of their "
            "sign (Rasi Sandhi — sign cusp / junction point) → Rasi Sandhi veto triggered"
        ),
        "condition_new": (
            "IF multiple planets in the oath chart are placed at 0° or 29° of their "
            "sign (Rasi Sandhi — sign cusp / junction point) → Rasi Sandhi veto triggered. "
            "Historical benchmark: the Oommen Chandy government (2004) had four planets "
            "(Venus, Jupiter, Moon, Saturn) in Rasi Sandhi and was structurally unstable "
            "throughout its term (Gopalakrishnan Ch5)."
        ),
        "result_old": (
            "Effective Governance coefficient = 0.20. Planets at Rasi Sandhi are in a "
            "'between worlds' state — they cannot express their natural significations "
            "reliably. An oath chart with 4+ planets at the cusp becomes structurally "
            "incapable of coherent governance. Administration will be marked by policy "
            "paralysis, indecision, and inability to execute on any significant agenda. "
            "Government may technically survive its term but will be functionally hollow."
        ),
        "result_new": (
            "Severe effective governance risk. Planets at Rasi Sandhi are in a 'between "
            "worlds' state — they cannot express their natural significations reliably. "
            "An oath chart with multiple planets at the cusp becomes structurally "
            "incapable of coherent governance. Administration will be marked by policy "
            "paralysis, indecision, and inability to execute on any significant agenda. "
            "Government may technically survive its term but will be functionally hollow."
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
    print(f"Category B — Arithmetic artifact removal ({len(PATCHES)} rules)")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    patched = 0
    for p in PATCHES:
        rid = p["rule_id"]
        r = col.find_one(
            {"rule_id": rid, "science_id": "mundane_jyotish"},
            {"_id": 0, "rule_id": 1, "title": 1, "result": 1,
             "approval_status": 1},
        )
        if not r:
            print(f"  ⚠️  NOT FOUND : {rid}\n")
            continue

        # Verify old result text is present
        if r.get("result", "") != p["result_old"]:
            print(f"  ⚠️  RESULT MISMATCH (already patched?): {rid}")
            print(f"     DB result starts: {r.get('result','')[:80]}…\n")
            continue

        print(f"  {rid}")
        if "title_old" in p:
            print(f"  title  : {p['title_old']}")
            print(f"        → {p['title_new']}")
        if "condition_old" in p:
            print(f"  cond   : {p['condition_old'][:80]}…")
            print(f"        → {p['condition_new'][:80]}…")

        # Show result change snippet
        old_r, new_r = p["result_old"], p["result_new"]
        for i, (a, b) in enumerate(zip(old_r, new_r)):
            if a != b:
                snippet_old = old_r[max(0, i-10):i+60].replace('\n', ' ')
                snippet_new = new_r[max(0, i-10):i+60].replace('\n', ' ')
                print(f"  result : …{snippet_old}…")
                print(f"        → …{snippet_new}…")
                break

        if args.apply:
            update_fields = {
                "result":                  p["result_new"],
                "approval_status":         "pending_review",
                "validation.patch_reason": "cat_b_arithmetic_artifact_removal_nlm_verified",
                "validation.patched_at":   now,
                "validation.patched_by":   "patch_mundane_cat_b_artifacts.py",
            }
            if "title_new" in p:
                update_fields["title"] = p["title_new"]
            if "condition_new" in p:
                update_fields["condition"] = p["condition_new"]
            unset_fields = {"validation.verdict": "", "validation.flag_reason": ""}

            res = col.update_one(
                {"rule_id": rid},
                {"$set": update_fields, "$unset": unset_fields},
            )
            if res.modified_count:
                print(f"  ✅ Patched → pending_review\n")
                patched += 1
            else:
                print(f"  ⚠️  No change written\n")
        else:
            print(f"  🔍 WOULD PATCH → pending_review\n")
            patched += 1

    print(f"{'─'*65}")
    if args.apply:
        print(f"Applied: {patched} / {len(PATCHES)} rules patched → pending_review")
        print(f"\nNext: run validate_mundane_rules.py on these 7 rules to re-validate.")
    else:
        print(f"Dry run: {patched} / {len(PATCHES)} rules would be patched.")
        print(f"Re-run with --apply to write.")

    client.close()


if __name__ == "__main__":
    main()
