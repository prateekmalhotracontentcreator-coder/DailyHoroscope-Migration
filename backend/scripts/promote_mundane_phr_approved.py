#!/usr/bin/env python3
"""
promote_mundane_phr_approved.py

Promotes 114 PHR rules to 'approved' based on co-founder + NotebookLM
sign-off review (May 2026, 186-rule full triage).

These rules are confirmed faithful to source, structurally clean, and
carry no arithmetic artifacts or logic collisions. They are ready for
live use by the Knowledge Engine.

Remaining 72 PHR rules are NOT included — they require text completion
(truncation fixes), arithmetic artifact removal, logic splits, or source
verification before promotion. See: backend/scripts/INGEST_NOTES.md

Usage:
  # Dry run (inspect only):
  python3 backend/scripts/promote_mundane_phr_approved.py --mongo-url "$MONGO_URL"

  # Apply:
  python3 backend/scripts/promote_mundane_phr_approved.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

# ── 114 PHR rules approved for promotion ────────────────────────────────────
# Source: NotebookLM 186-rule triage (May 2026) + co-founder sign-off review
# Rule IDs are as stored in MongoDB (some have 'mundane-' prefix, some do not)
# The script tries the exact ID first, then adds/removes 'mundane-' prefix as
# a fallback to handle ingestion-era prefix inconsistencies.

APPROVED_PHR_RULE_IDS: list[str] = [
    # ── Batch 1 — Raphael Ch28 + Gaur Ch1 Samvatsar ──
    "mundane-raphael-ch28-mars-exact-city-degree-fire-accident",
    "gaur-ch1-samvatsar-ketu-lord-plentiful-rains-loose-morals",
    "gaur-ch1-samvatsar-moon-lord-all-months-excellent",

    # ── Batch 2 — Gaur Ch3/11 + Mehta Ch2 ──
    "gaur-ch3-universal-horoscope-malefics-7th-crop-damage",
    "mehta-ch2-king-of-year-sun-moon-governance",
    "mehta-ch2-mars-retrograde-jyeshtha-anuradha-fall-of-kings",
    "mehta-ch2-sat-jup-conjunction-us-president-mortality",
    "mehta-ch2-sat-rahu-conjunction-imperialism-ends",
    "mehta-ch2-three-saturdays-tuesdays-paksha-alert",
    "gaur-ch11-eclipse-jupiter-aspect-neutralizes",
    "gaur-ch11-eclipse-lunar-solar-sequence-tyrant-rulers",

    # ── Batch 3 — Gaur Ch4/8/9 Koorma + Commodity ──
    "gaur-ch11-eclipse-solar-lunar-sequence-religious-happiness",
    "gaur-ch4-koorma-back-malefic-heartland-unrest",
    "gaur-ch4-koorma-benefic-segment-progress",
    "gaur-ch4-koorma-northeast-enemy-attack",
    "gaur-ch4-koorma-vedha-synchronization",
    "gaur-ch8-commodity-malefic-vedha-price-spike",
    "gaur-ch8-saturn-mars-capricorn-chemical",
    "gaur-ch8-saturn-retrograde-industrial",

    # ── Batch 4 — Mehta Ch10 + Gaur Ch10 ──
    "mehta-ch10-saturn-jupiter-us-president-mortality-veto",
    "mehta-ch10-saturn-mars-sixth-house-internal-military",
    "mehta-ch10-saturn-rahu-gemini-nuclear-shift",
    "gaur-ch10-jupiter-capricorn-afflicted-banking-crisis",
    "gaur-ch10-mars-12th-lord-afflicted-military-insubordination",
    "gaur-ch10-mars-gemini-sudden-price-volatility",

    # ── Batch 5 — Gaur Ch10 + Mehta Ch7 + Gaur Ch5/6 ──
    "gaur-ch10-mercury-sign-ingress-weather-disturbance",
    "mehta-ch7-koorma-saturn-west-triple-amplifier",
    "mundane-gaur-ch5-ardra-afternoon-entry",
    "mundane-gaur-ch5-ardra-bumper-harvest",
    "mundane-gaur-ch5-ardra-krithika-fire",
    "mundane-gaur-ch5-ardra-saturday-disease",
    "mundane-gaur-ch5-rohini-sea-flash-flood",
    "mundane-gaur-ch6-mars-venus-jupiter-catastrophic",

    # ── Batch 6 — Gaur Ch6/7/8 ──
    "mundane-gaur-ch6-trinadi-catastrophic-flood",
    "mundane-gaur-ch6-trinadi-hail-storm",
    "mundane-gaur-ch6-trinadi-no-rain-veto",
    "mundane-gaur-ch7-conspiracy-yoga-vi",
    "mundane-gaur-ch7-total-crop-failure-yoga-ix",

    # ── Batch 7 — Gaur Ch9 + Gopal Ch14 ──
    "mundane-gaur-ch9-sarvatobhadra-market-sentiment",
    "mundane-gaur-ch9-sarvatobhadra-textile-shortage",
    "mundane-gopal-ch14-mars-perigee-south-cm",
    "mundane-gopal-ch14-mercury-bhukti-epidemic-recovery",
    "mundane-gopal-ch14-nadi-saturn-8th-from-jupiter",

    # ── Batch 8 — Gopal Ch14/3/5 ──
    "mundane-gopal-ch14-saturn-kataka-bloodshed",
    "mundane-gopal-ch14-saturn-ketu-leo-oil",
    "mundane-gopal-ch3-rasi-sandhi-spoiler",
    "mundane-gopal-ch3-triple-check-pass",
    "mundane-gopal-ch5-jaimini-long-tenure",

    # ── Batch 9 — Mehta Ch18 Oath/Simhasan ──
    "mundane-mehta-ch18-ashtakvarga-8th-lord-stronger",
    "mundane-mehta-ch18-cancer-leo-partner-discord",
    "mundane-mehta-ch18-capricorn-lagna-exclusion",
    "mundane-mehta-ch18-sandhi-bharani-lethality",

    # ── Batch 10 — Mehta Ch18 + Gopal Ch4 ──
    "mundane-mehta-ch18-simha-moon-rahu-dasha",
    "mundane-mehta-ch18-simhasan-jupiter-protection",
    "mundane-mehta-ch18-simhasan-martial-king",
    "mundane-mehta-ch18-simhasan-moon-absolute-power",
    "mundane-gopal-ch4-eighth-saturn-sudden-reversal",

    # ── Batch 11 — Gopal Ch4 + Mehta Ch22 ──
    "mundane-gopal-ch4-incumbent-vulnerability-trigger",
    "mundane-gopal-ch4-indian-pm-lagna-bias",
    "mundane-gopal-ch4-indian-pm-widowhood-rule",
    "mundane-gopal-ch4-sonia-dramatic-change-trigger",
    "mundane-mehta-ch22-combustion-veto-reversal",
    "mundane-mehta-ch22-golden-year-jupiter-venus",
    "mundane-mehta-ch22-jupiter-raja-afflicted-banking-crisis",

    # ── Batch 12 — Mehta Ch22 + Gopal Ch2 ──
    "mundane-mehta-ch22-saturn-durgesh-defense-humiliation",
    "mundane-mehta-ch22-winter-prosperity-dhanyesh-meghesh",
    "mundane-gopal-ch2-10th-lord-triage",
    "mundane-gopal-ch2-election-comparative-audit",
    "mundane-gopal-ch2-governance-longevity",

    # ── Batch 13 — Gopal Ch2 + Gopal Ch10 Sports (10/10 clean) ──
    "mundane-gopal-ch2-india-lagna-filter",
    "mundane-mehta-ch6-5th-malefic-assassination",
    "mundane-mehta-ch6-sat-10th-democracy",
    "mundane-mehta-ch6-sun-6th-border-war",
    "mundane-raphael-ch3-intellectual-triad",
    "mundane-raphael-ch3-opposition-4th-trigger",
    "mundane-gopal-ch10-sports-batting-first-winner-gate",
    "mundane-gopal-ch10-sports-chasing-victory-trigger",
    "mundane-gopal-ch10-sports-injury-scandal-alert",
    "mundane-gopal-ch10-sports-match-longevity-gate",

    # ── Batch 14 — Gopal Ch10/11/12 India profile ──
    "mundane-gopal-ch10-sports-umpire-conflict-filter",
    "mundane-gopal-ch11-rains-rahu-saturn-bhukti-monsoon-failure",
    "mundane-gopal-ch11-rains-tajika-4th-watery-positive",
    "mundane-gopal-ch12-india-cancer-transit-south-it",
    "mundane-gopal-ch12-india-jupiter-6th-judicial-corruption",
    "mundane-gopal-ch12-india-pakistan-2-12-friction-veto",
    "mundane-gopal-ch12-india-rahu-lagna-western-imitation",
    "mundane-gopal-ch12-india-venus-moon-sports-obsession",

    # ── Batch 15 — Gaur Ch2 + Mehta Ch13/20 ──
    "mundane-gaur-ch2-dhanyesh-outcome-matrix",
    "mundane-gaur-ch2-dvadasha-sarpa-snake-forecast",
    "mundane-gaur-ch2-meghesh-outcome-matrix",
    "mundane-mehta-ch20-delhi-bombs-national-affliction",
    "mundane-mehta-ch20-india-temple-attack-signature",
    "mundane-mehta-ch20-madrid-london-validation",
    "mundane-mehta-ch20-nine-eleven-validation",

    # ── Batch 16 — Mehta Ch26 + Gaur Ch10/11 ──
    "mundane-mehta-ch26-party-dasha-framework",
    "mundane-gaur-ch10-jupiter-motion-differentials",
    "mundane-gaur-ch10-rahu-drought-aries-libra",
    "mundane-gaur-ch10-saturn-motion-differentials",
    "mundane-gaur-ch10-venus-motion-differentials",
    "mundane-gaur-ch11-two-eclipses-fortnight-calamity",

    # ── Batch 17 — Gopal Ch6/7/8/9/10/13 ──
    "mundane-gopal-ch8-india-pakistan-2-12-lagna",
    "mundane-gopal-ch9-planet-bundle-crisis",
    "mundane-gopal-ch10-mars-perigee-leadership-change",
    "mundane-gopal-ch13-jupiter-6th-dasa-no-peace",
    "mundane-gopal-ch13-saturn-bhukthi-raja-yoga-stock-market",
    "mundane-gopal-ch13-saturn-ketu-conjunction-civil-war",

    # ── Batch 18 — Gopal Ch15 + Raphael Ch26 ──
    "mundane-gopal-ch15-jupiter-6th-national-dharma-down",
    "mundane-gopal-ch15-rahu-11th-national-stock-boom",
    "mundane-gopal-ch15-saturn-3rd-national-it-boom",
    "mundane-raphael-ch26-great-conjunction-4th-cusp-earthquake",

    # ── Final batch — Mehta Ch10 + Gaur Ch10 ──
    "mehta-ch10-mars-ketu-fiery-sign-terrorism",
    "gaur-ch10-saturn-28-degree-aries-market-correction",
]

# Deduplicate (gaur-ch8-saturn-mars-capricorn-chemical appears in batches 3 and 6)
APPROVED_PHR_RULE_IDS = list(dict.fromkeys(APPROVED_PHR_RULE_IDS))


def resolve_rule_id(col, rule_id: str) -> dict | None:
    """Find rule by exact ID, then try with/without 'mundane-' prefix."""
    r = col.find_one(
        {"rule_id": rule_id, "science_id": "mundane_jyotish"},
        {"_id": 0, "rule_id": 1, "approval_status": 1, "title": 1},
    )
    if r:
        return r

    # Try with 'mundane-' prefix added
    alt = "mundane-" + rule_id if not rule_id.startswith("mundane-") else rule_id[len("mundane-"):]
    r = col.find_one(
        {"rule_id": alt, "science_id": "mundane_jyotish"},
        {"_id": 0, "rule_id": 1, "approval_status": 1, "title": 1},
    )
    return r


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--apply",     action="store_true",
                        help="Write changes to DB (default: dry run)")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]
    now    = datetime.now(timezone.utc).isoformat()

    print(f"\n{'═'*65}")
    print(f"Mundane PHR → Approved promotion  ({len(APPROVED_PHR_RULE_IDS)} rules)")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍  (use --apply to write)'}")
    print(f"{'═'*65}\n")

    promoted     = []
    already_done = []
    not_found    = []
    wrong_status = []

    for rid in APPROVED_PHR_RULE_IDS:
        r = resolve_rule_id(col, rid)
        if not r:
            not_found.append(rid)
            print(f"  ⚠️  NOT FOUND : {rid}")
            continue

        actual_rid    = r["rule_id"]
        actual_status = r.get("approval_status", "unknown")

        if actual_status == "approved":
            already_done.append(actual_rid)
            continue  # silent skip

        if actual_status not in ("pending_human_review", "auto_approved"):
            wrong_status.append((actual_rid, actual_status))
            print(f"  ⛔ SKIP ({actual_status:20s}): {actual_rid}")
            continue

        if args.apply:
            result = col.update_one(
                {"rule_id": actual_rid},
                {"$set": {
                    "approval_status":             "approved",
                    "validation.verdict":          "approved",
                    "validation.approved_by":      "co_founder_notebooklm_review_may2026",
                    "validation.approved_at":      now,
                    "validation.approved_note":    (
                        "Promoted via NotebookLM 186-rule triage + co-founder sign-off "
                        "(promote_mundane_phr_approved.py, May 2026)."
                    ),
                }},
            )
            if result.modified_count:
                promoted.append(actual_rid)
                print(f"  ✅ PROMOTED : {actual_rid}")
            else:
                print(f"  ⚠️  NO CHANGE: {actual_rid}")
        else:
            promoted.append(actual_rid)
            print(f"  🔍 WOULD PROMOTE: {actual_rid}  [{actual_status}]")

    print(f"\n{'─'*65}")
    print(f"Results:")
    print(f"  {'Promoted' if args.apply else 'Would promote'} : {len(promoted)}")
    print(f"  Already approved : {len(already_done)}")
    print(f"  Not found in DB  : {len(not_found)}")
    print(f"  Wrong status     : {len(wrong_status)}")
    print(f"  Total attempted  : {len(APPROVED_PHR_RULE_IDS)}")

    if not_found:
        print(f"\n⚠️  Not found (check rule_id spellings):")
        for rid in not_found:
            print(f"     {rid}")

    if wrong_status:
        print(f"\n⛔ Wrong status (not PHR/auto_approved):")
        for rid, st in wrong_status:
            print(f"     {rid}  →  {st}")

    if not args.apply and promoted:
        print(f"\n✏️  Re-run with --apply to write {len(promoted)} promotions to MongoDB.")

    client.close()


if __name__ == "__main__":
    main()
