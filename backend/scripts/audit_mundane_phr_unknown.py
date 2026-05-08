#!/usr/bin/env python3
"""
audit_mundane_phr_unknown.py

Identifies any pending_human_review mundane rules that are NOT in the
72-rule fix catalogue (mundane_phr_fixes_required.md).

Expected: 78 PHR rules total — 72 catalogued + 6 unknown.
These 6 were likely escalated during the v3–v7 patch cycle after the
sign-off review was generated.

Usage:
  python3 backend/scripts/audit_mundane_phr_unknown.py --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
from pymongo import MongoClient

# ── 72 rules already catalogued in mundane_phr_fixes_required.md ────────────
CATALOGUED: set[str] = {
    # Category A — Truncated text (32)
    "gaur-ch1-samvatsar-vishnu-lord-law-order-diseases",
    "gaur-ch1-samvatsar-jupiter-lord-excessive-rains-disease",
    "gaur-ch1-samvatsar-rahu-lord-drought-north-floods-east",
    "gaur-ch1-samvatsar-shiv-lord-rulers-overthrown",
    "gaur-ch1-samvatsar-sun-lord-less-rain-insurgency",
    "gaur-ch1-samvatsar-venus-lord-natural-calamities",
    "gaur-ch1-samvatsar-group-quality-modifier",
    "mehta-ch7-koorma-triple-directional-audit",
    "mundane-mehta-ch18-enemy-lord-coalition",
    "mundane-mehta-ch18-many-bosses-constraint",
    "mundane-mehta-ch18-nakshatra-tithi-veto-combo",
    "mundane-mehta-ch18-narasimha-rao-liberalisation-dhana",
    "mundane-mehta-ch18-raman-democratic-lagnas",
    "mundane-mehta-ch18-shastri-terminal-leadership",
    "mundane-mehta-ch18-simhasan-aasan-saturn-terminal",
    "mundane-mehta-ch18-vajpayee-balarishta-pattern",
    "mundane-mehta-ch22-anarchy-gate-sun-raja-saturn-mantri",
    "mundane-mehta-ch22-mars-raja-year-of-sword",
    "mundane-mehta-ch22-mercury-dhanesh-it-boom",
    "mundane-mehta-ch22-saturn-dhanesh-treasury-depletion",
    "mundane-mehta-ch22-sun-raja-2001-validation",
    "mundane-mehta-ch26-bjp-dasha-history",
    "mundane-mehta-ch26-congress-i-dasha-history",
    "mundane-mehta-ch26-retrograde-malefic-dasha-crisis",
    "mundane-gaur-ch10-mercury-motion-differentials",
    "mundane-mehta-ch20-terrorism-ten-parameters",
    "mundane-raphael-ch14-mars-7th-war-direction",
    "mundane-raphael-ch8-malefic-1st-national-troubles",
    "mundane-raphael-ch22-eclipse-fixed-lasting-cardinal-brief",
    "mundane-raphael-ch26-eclipse-on-meridian-nadir-earthquake",
    "mundane-raphael-ch27-comet-sign-type-effects",
    "mundane-raphael-ch28-mars-transit-country-sign-fires",
    # Category B — Arithmetic artifacts (6)
    "mehta-ch10-saturn-rahu-capricorn-regime-change",
    "mundane-gopal-ch14-mars-perigee-manufacturing",
    "mundane-gopal-ch5-hora-lagna-fixed-veto",
    "mundane-gopal-ch4-destiny-anchor-karkamsha",
    "mundane-gopal-ch4-eleventh-house-dasha-surge",
    "mundane-gopal-ch12-india-bpo-destiny-3rd-house",
    # Category C — Logic fixes / splits (10)
    "mundane-gaur-ch9-sarvatobhadra-currency-spike",
    "gaur-ch10-mercury-combust-leo-stock-market-crash",
    "gaur-ch10-mercury-retrograde-gemini-education-scandal",
    "mundane-gaur-ch8-gold-silver-bullion-gate",
    "mundane-gaur-ch8-dual-mapping-volatility",
    "mundane-mehta-ch22-jupiter-raja-golden-year",
    "mundane-mehta-ch13-eclipse-lord-placement",
    "mundane-mehta-ch13-eclipse-ruler-royalty",
    "mundane-mehta-ch22-raja-mantri-enemy-deadlock",
    "mundane-gaur-ch6-saptnadi-amrita-rain",
    # Category D — Source verification (10)
    "gaur-ch8-gold-reserve-banking-crisis-veto",
    "gaur-ch10-jupiter-cancer-sun-aspect-supremacy",
    "mehta-ch2-double-eclipse-14-days-destruction",
    "mundane-gopal-ch14-bpo-contrarian-gate",
    "mundane-gopal-ch14-mars-proximity-children",
    "mundane-gopal-ch14-regional-direction-leadership",
    "mundane-gopal-ch14-saturn-leo-real-estate",
    "mundane-gopal-ch14-saturn-pushya-bull-run",
    "mundane-mehta-ch18-aadhaar-dependency-governance",
    "mundane-gopal-ch7-rahu-ketu-ic-mc-axis",
    # Category E — Contextual modifiers (8)
    "mundane-gopal-ch14-decentralised-terror",
    "mundane-gopal-ch3-widow-pm-multiplier",
    "mundane-gopal-ch4-volatile-nomination-chart",
    "mundane-gopal-ch11-rains-rahu-capricorn-moderate",
    "mundane-gopal-ch6-epidemic-triad",
    "mundane-gopal-ch7-cardinal-stellium-upheaval",
    "mundane-gopal-ch9-malefics-trika-entry",
    "mundane-gaur-ch6-ownership-rain-confirm",
    # Category F — Rewrites (3)
    "mehta-ch10-aries-1-degree-conjunction-paradigm-shift",
    "gaur-ch10-mars-ahead-sun-monsoon-failure",
    "gaur-ch10-saturn-retrograde-uttarashadh-poorvashadh-famine",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]

    phr_rules = list(col.find(
        {"science_id": "mundane_jyotish", "approval_status": "pending_human_review"},
        {"_id": 0, "rule_id": 1, "batch_id": 1, "title": 1,
         "validation.flag_reason": 1, "validation.patch_reason": 1},
    ).sort([("batch_id", 1), ("rule_id", 1)]))

    catalogued_found = [r for r in phr_rules if r["rule_id"] in CATALOGUED]
    unknown          = [r for r in phr_rules if r["rule_id"] not in CATALOGUED]

    print(f"\n{'═'*65}")
    print(f"Mundane PHR audit — unknown rules")
    print(f"{'═'*65}")
    print(f"\nTotal PHR rules in DB : {len(phr_rules)}")
    print(f"Catalogued (known)    : {len(catalogued_found)}")
    print(f"Unknown (not in list) : {len(unknown)}")

    if unknown:
        print(f"\n{'─'*65}")
        print(f"UNKNOWN RULES — need to be added to fix catalogue:\n")
        for r in unknown:
            print(f"  [{r.get('batch_id', 'unknown')}]")
            print(f"  rule_id : {r['rule_id']}")
            print(f"  title   : {r.get('title', 'n/a')}")
            reason = (
                r.get('validation', {}).get('flag_reason', '') or
                r.get('validation', {}).get('patch_reason', '')
            )
            if reason:
                print(f"  reason  : {reason[:200]}")
            print()
    else:
        print("\n✅ All PHR rules are accounted for in the fix catalogue.")

    if len(catalogued_found) < len(CATALOGUED):
        missing_from_db = CATALOGUED - {r["rule_id"] for r in phr_rules}
        print(f"\n⚠️  {len(missing_from_db)} catalogued rule_ids not found in PHR "
              f"(may have been promoted or use different ID):")
        for rid in sorted(missing_from_db):
            print(f"  {rid}")

    client.close()


if __name__ == "__main__":
    main()
