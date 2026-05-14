#!/usr/bin/env python3
"""
patch_mundane_cat_c3_corrections.py

Applies targeted field corrections to 8 Category C3 PHR rules.
These are confirmed fixes -- no source verification needed.

Rules patched:
  1. mundane-mehta-ch22-jupiter-raja-golden-year
     condition: "Mars" → "Jupiter" (typo -- rule is about Jupiter as Raja)

  2. mundane-gaur-ch6-saptnadi-amrita-rain
     result: add hierarchy note (Trinadi no-rain veto > Saptnadi rain signal)

  3. gaur-ch10-45-muhurti-ingress-overrides-drought
     result: "overrides all" → "strongly mitigates"

  4. mundane-gopal-ch3-trikona-trikona-billionaire
     result: "Billionaire calibre" → "exceptional wealth potential"

  5. mundane-gopal-ch5-jaimini-short-tenure
     result: add explicit complement note re jaimini-long-tenure

  6. mundane-mehta-ch18-8th-house-vacancy-rule
     condition: rewrite into two tiers (malefic vs benefic) resolving
     the condition/result contradiction

  7. gaur-ch10-mercury-retrograde-gemini-education-scandal
     result: remove speculative "education scandal" cross-reference;
     keep vegetable price rule only

  8. gaur-ch10-mercury-combust-leo-stock-market-crash
     result: rewrite to separate causal logic for each sector clearly
     (stock market + textile) while keeping as one compound rule

Usage:
  # Dry run:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_mundane_cat_c3_corrections.py --mongo-url "$MONGO_URL"

  # Apply:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_mundane_cat_c3_corrections.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

PATCHES: list[dict] = [
    # ── 1. jupiter-raja-golden-year -- fix "Mars" → "Jupiter" in condition ──
    {
        "rule_id": "mundane-mehta-ch22-jupiter-raja-golden-year",
        "field": "condition",
        "old": (
            "IF Mars is the Raja for the year (unafflicted, not combust, not in "
            "Grahayudha) → Jupiter prosperity activation IF Jupiter is also "
            "unafflicted in the Hindu New Year chart"
        ),
        "new": (
            "IF Jupiter is the Raja for the year (unafflicted, not combust, not in "
            "Grahayudha) → Golden Year prosperity activation IF Jupiter is also "
            "unafflicted in the Hindu New Year chart"
        ),
        "note": "Condition typo: 'Mars' corrected to 'Jupiter'. Rule describes Jupiter-as-Raja outcome.",
    },

    # ── 2. saptnadi-amrita-rain -- add Trinadi hierarchy note ──
    {
        "rule_id": "mundane-gaur-ch6-saptnadi-amrita-rain",
        "field": "result",
        "old": (
            "METEOROLOGICAL ALERT: Continuous rainfall predicted for 1 to 7 days "
            "(may recur multiple times). Moon is lord of Amrita Nadi -- its presence "
            "is the primary rain trigger. High confidence forecast."
        ),
        "new": (
            "METEOROLOGICAL ALERT: Continuous rainfall predicted for 1 to 7 days "
            "(may recur multiple times). Moon is lord of Amrita Nadi -- its presence "
            "is the primary rain trigger. High confidence forecast. "
            "Hierarchy note: If the Trinadi no-rain veto is simultaneously active "
            "(malefics in Patal Nadi + benefics in Heaven Nadi), the Trinadi veto "
            "takes precedence and this signal is suppressed."
        ),
        "note": "Added Trinadi > Saptnadi hierarchy to resolve logic collision with trinadi-no-rain-veto rule.",
    },

    # ── 3. 45-muhurti-ingress -- soften "overrides all" ──
    {
        "rule_id": "gaur-ch10-45-muhurti-ingress-overrides-drought",
        "field": "result",
        "old": (
            "Good rains are assured. Grains, ghee, oil, and cotton become cheap. "
            "This overrides all dry-season signals, malefic weekday ingress results, "
            "and any drought indications from sign or star placements."
        ),
        "new": (
            "Good rains are assured. Grains, ghee, oil, and cotton become cheap. "
            "This strongly mitigates dry-season signals, malefic weekday ingress "
            "results, and drought indications from sign or star placements."
        ),
        "note": "Softened 'overrides all' to 'strongly mitigates' -- 45-muhurti is a strong positive signal, not an absolute override.",
    },

    # ── 4. trikona-trikona-billionaire -- soften "billionaire calibre" ──
    {
        "rule_id": "mundane-gopal-ch3-trikona-trikona-billionaire",
        "field": "result",
        "old": (
            "Wealth Forecast: 'Native will achieve wealth at unheard-of levels -- "
            "Billionaire calibre. The high-order Trikona-Trikona Raja Yoga is the "
            "most powerful wealth combination in Vedic astrology'. Validation: Bill "
            "Gates -- 5th and 9th lords combined in 5th house."
        ),
        "new": (
            "Wealth Forecast: This native carries exceptional wealth potential -- "
            "among the most powerful wealth combinations in Vedic astrology. The "
            "high-order Trikona-Trikona Raja Yoga indicates wealth at extraordinary "
            "levels. Dasha-transit confirmation required for timing and magnitude. "
            "Validation: Bill Gates -- 5th and 9th lords combined in 5th house."
        ),
        "note": "Softened 'Billionaire calibre' to 'exceptional wealth potential'; added Dasha confirmation requirement.",
    },

    # ── 5. jaimini-short-tenure -- add complement note ──
    {
        "rule_id": "mundane-gopal-ch5-jaimini-short-tenure",
        "field": "result",
        "old": (
            "Government has HIGH RISK of premature fall, collapse of coalition, or "
            "forced early exit before the full mandate is completed. Fixed-sign "
            "rigidity in the 8th house signals functional longevity problems. "
            "Prognosis: government unlikely to reach full term. Validate against "
            "Vajpayee 1996 (13-day government) where this pattern was confirmed."
        ),
        "new": (
            "Government has HIGH RISK of premature fall, collapse of coalition, or "
            "forced early exit before the full mandate is completed. Fixed-sign "
            "rigidity in both the Lagna lord and 8th lord positions signals "
            "functional longevity problems. Prognosis: government unlikely to reach "
            "full term. Validate against Vajpayee 1996 (13-day government) where "
            "this pattern was confirmed. "
            "Note: This is the inverse complement of the Jaimini long-tenure gate "
            "(Chara+Chara = Long Life). Fixed+Fixed = Short Life per Gopalakrishnan "
            "Ch5. These two rules form a paired tenure-assessment system."
        ),
        "note": "Added complement note linking to jaimini-long-tenure rule. Resolves the validator's false contradiction flag.",
    },

    # ── 6. 8th-house-vacancy-rule -- rewrite condition into two tiers ──
    {
        "rule_id": "mundane-mehta-ch18-8th-house-vacancy-rule",
        "field": "condition",
        "old": (
            "IF the 8th house of the Muhurta chart contains any planet at time of "
            "oath taking → 8th house vacancy rule violated"
        ),
        "new": (
            "IF the 8th house of the Muhurta chart contains a malefic planet "
            "(Saturn, Mars, Rahu, or Ketu) at the time of oath taking → "
            "8th house vacancy SEVERELY violated. "
            "IF the 8th house contains a benefic planet (Jupiter, Venus, Mercury, "
            "or Moon) at the time of oath taking → 8th house vacancy MILDLY "
            "violated. "
            "Empty 8th house = Muhurta longevity gate passed."
        ),
        "note": "Rewrote condition into malefic/benefic tiers. Resolves internal contradiction with result (which already differentiates severity).",
    },

    # ── 7. mercury-retrograde-gemini -- remove speculative scandal component ──
    {
        "rule_id": "gaur-ch10-mercury-retrograde-gemini-education-scandal",
        "field": "result",
        "old": (
            "Vegetables become cheap. Cross-reference with House 5 (Education "
            "Ministry) -- 'Potential scams and scandals in educational institutions' "
            "alert triggered."
        ),
        "new": (
            "Vegetables become cheap. Mercury retrograde in its own sign (Gemini) "
            "creates supply pressure in perishable commodities governed by Mercury "
            "and Gemini. Source: Gaur Ch10 transit table."
        ),
        "note": "Removed 'education scandal' cross-reference -- analyst inference not in Gaur Ch10 source. Vegetable price rule retained and expanded with causal logic.",
    },

    # ── 8. mercury-combust-leo -- clarify dual-sector causal logic ──
    {
        "rule_id": "gaur-ch10-mercury-combust-leo-stock-market-crash",
        "field": "result",
        "old": (
            "'Sudden decline in Stock Market values and Textile/Jute sector "
            "bearishness' alert. Leo is the sign of rulers and the stock exchange. "
            "Combustion kills Mercury's trading function."
        ),
        "new": (
            "Two sector-specific alerts: "
            "(1) Stock Market Decline -- Leo is the sign of rulers and the stock "
            "exchange; Mercury combustion suppresses the market-intelligence and "
            "trading function, triggering sudden decline in equity values. "
            "(2) Textile/Jute Bearishness -- Mercury governs trade and textile "
            "commodities; affliction in Leo (a non-Mercury sign) depresses "
            "sentiment and prices in the textile and jute sectors. "
            "Both signals require independent confirmation from house-lord transits."
        ),
        "note": "Rewrote result to give explicit causal logic for each sector outcome. Resolves coherence failure while keeping as one compound rule (same transit trigger).",
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
    print(f"Category C3 -- Logic corrections ({len(PATCHES)} rules)")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    patched = 0
    for p in PATCHES:
        rid   = p["rule_id"]
        field = p["field"]

        r = col.find_one(
            {"rule_id": rid, "science_id": "mundane_jyotish"},
            {"_id": 0, "rule_id": 1, "title": 1, field: 1, "approval_status": 1},
        )
        if not r:
            print(f"  ⚠️  NOT FOUND: {rid}\n")
            continue

        current = r.get(field, "")
        if current != p["old"]:
            print(f"  ⚠️  MISMATCH (already patched?): {rid}")
            print(f"     DB {field} starts: {current[:80]}...\n")
            continue

        # Show snippet of change
        old_s, new_s = p["old"], p["new"]
        for i, (a, b) in enumerate(zip(old_s, new_s)):
            if a != b:
                snip_old = old_s[max(0, i-5):i+55].replace('\n', ' ')
                snip_new = new_s[max(0, i-5):i+55].replace('\n', ' ')
                break
        else:
            snip_old = old_s[:60]
            snip_new = new_s[:60]

        print(f"  {rid}")
        print(f"  {field}: ...{snip_old}...")
        print(f"       → ...{snip_new}...")
        print(f"  note: {p['note']}")

        if args.apply:
            res = col.update_one(
                {"rule_id": rid},
                {"$set": {
                    field:                     p["new"],
                    "approval_status":         "pending_review",
                    "validation.patch_reason": f"cat_c3_{field}_correction",
                    "validation.patch_note":   p["note"],
                    "validation.patched_at":   now,
                    "validation.patched_by":   "patch_mundane_cat_c3_corrections.py",
                },
                "$unset": {
                    "validation.verdict":     "",
                    "validation.flag_reason": "",
                }},
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
        print(f"Applied: {patched} / {len(PATCHES)} rules → pending_review")
    else:
        print(f"Dry run: {patched} / {len(PATCHES)} would be patched.")
        print(f"Re-run with --apply to write.")

    client.close()


if __name__ == "__main__":
    main()
