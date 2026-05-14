#!/usr/bin/env python3
"""
patch_mundane_cat_c3_nlm_corrections.py

Applies NLM-verified corrections to 4 Category C3 rules that were held
pending source verification. All findings confirmed by NLM (May 2026).

Rules:
  1. mundane-gaur-ch6-saptnadi-amrita-rain
     Remove the Trinadi > Saptnadi hierarchy note added in the C3 patch.
     NLM confirmed: Gaur Ch6 presents Trinadi (pp.55-56) and Saptnadi (pp.57-59)
     as fully independent diagnostic tools with NO explicit precedence stated.
     The hierarchy note was a reasonable inference but not source-backed -- remove it.

  2. gaur-ch10-45-muhurti-ingress-overrides-drought
     Condition: CORRECT as patched (simultaneous Sankranti + specific nakshatra
     trigger). Validator's "conflation" objection was wrong. No condition change.
     Result: Soften further to match Gaur's actual language -- he says results are
     "generally broad in nature" requiring "minute analysis of other planetary
     factors." Remove the "strongly mitigates" claim about other signals.

  3. gaur-ch10-mercury-combust-leo-stock-market-crash
     Complete result rewrite. NLM confirmed Gaur Ch10 actual text for Mercury in
     Leo: "Grains are medium. Metals such as gold and silver, gur, khand etc are
     cheap." For Mercury combust: "Wheat, gram, ghee etc are cheap."
     Stock market crash and textile/jute bearishness are NOT in Gaur Ch10.
     Textile/jute maps to Gemini (Ch8), not Leo. Both references were analyst
     fabrications and must be removed entirely.

  4. mundane-gopal-ch3-trikona-trikona-billionaire
     NLM confirmed: Gopal Ch3 is titled "CELEBRITY HOROSCOPE - AN ANALYSIS"
     (natal astrology -- individual opulence, not collective/mundane).
     Trikona-Trikona Raja Yoga + Bill Gates analysis = natal rule, misclassified
     as mundane. Action: retire from mundane library with misclassification note.
     Set approval_status = pending_human_review for co-founder decision on
     long-term disposition (retire or move to natal library).

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_mundane_cat_c3_nlm_corrections.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_mundane_cat_c3_nlm_corrections.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

# ── Patch definitions ──────────────────────────────────────────────────────────

PATCHES: list[dict] = [

    # ── 1. saptnadi-amrita-rain: remove unsourced Trinadi hierarchy note ──────
    {
        "rule_id": "mundane-gaur-ch6-saptnadi-amrita-rain",
        "field":   "result",
        "old": (
            "METEOROLOGICAL ALERT: Continuous rainfall predicted for 1 to 7 days "
            "(may recur multiple times). Moon is lord of Amrita Nadi -- its presence "
            "is the primary rain trigger. High confidence forecast. "
            "Hierarchy note: If the Trinadi no-rain veto is simultaneously active "
            "(malefics in Patal Nadi + benefics in Heaven Nadi), the Trinadi veto "
            "takes precedence and this signal is suppressed."
        ),
        "new": (
            "METEOROLOGICAL ALERT: Continuous rainfall predicted for 1 to 7 days "
            "(may recur multiple times). Moon is lord of Amrita Nadi -- its presence "
            "is the primary rain trigger. High confidence forecast. "
            "Note: Gaur presents Trinadi (Ch6 pp.55-56) and Saptnadi (pp.57-59) as "
            "independent diagnostic tools for provincial rainfall forecasting. No "
            "explicit precedence is stated when both signals fire simultaneously -- "
            "treat as conflicting signals requiring human synthesis."
        ),
        "note": (
            "NLM confirmed: Gaur Ch6 does not state Trinadi > Saptnadi precedence. "
            "Both are standalone methods. Previous hierarchy note was an unsourced "
            "inference -- replaced with accurate 'conflicting signals' guidance."
        ),
    },

    # ── 2. 45-muhurti-ingress: soften result to match Gaur's actual language ──
    {
        "rule_id": "gaur-ch10-45-muhurti-ingress-overrides-drought",
        "field":   "result",
        "old": (
            "Good rains are assured. Grains, ghee, oil, and cotton become cheap. "
            "This strongly mitigates dry-season signals, malefic weekday ingress "
            "results, and drought indications from sign or star placements."
        ),
        "new": (
            "Good rains are assured. Grains, ghee, oil, and cotton become cheap. "
            "Source: Gaur Ch10. Note: Gaur states these results are 'generally "
            "broad in nature' and require minute analysis of other planetary factors "
            "for precise timing and magnitude. Treat as a strong positive rain signal, "
            "not an absolute override of contrary indicators."
        ),
        "note": (
            "NLM confirmed: condition is correctly a simultaneous Sankranti + "
            "specific nakshatra trigger (validator's 'conflation' objection was wrong). "
            "Result softened to match Gaur's actual language: 'generally broad in "
            "nature, requiring minute analysis.' Removed 'strongly mitigates' claim "
            "about other signals -- Gaur does not state this."
        ),
    },

    # ── 3. mercury-combust-leo: rewrite result to Gaur's actual text ──────────
    {
        "rule_id": "gaur-ch10-mercury-combust-leo-stock-market-crash",
        "field":   "result",
        "old": (
            "Two sector-specific alerts: "
            "(1) Stock Market Decline -- Leo is the sign of rulers and the stock "
            "exchange; Mercury combustion suppresses the market-intelligence and "
            "trading function, triggering sudden decline in equity values. "
            "(2) Textile/Jute Bearishness -- Mercury governs trade and textile "
            "commodities; affliction in Leo (a non-Mercury sign) depresses "
            "sentiment and prices in the textile and jute sectors. "
            "Both signals require independent confirmation from house-lord transits."
        ),
        "new": (
            "Commodity signal (Gaur Ch10 transit table): Grains are medium in "
            "availability and price. Metals (gold, silver), gur, and khand become "
            "cheap. When Mercury is additionally combust in Leo: wheat, gram, and "
            "ghee become cheap. "
            "Note: Stock market crash and textile/jute bearishness attributions are "
            "not present in Gaur Ch10 for this configuration -- those references have "
            "been removed as unsourced analyst inferences. Textile/jute maps to "
            "Gemini (Gaur Ch8), not Leo."
        ),
        "note": (
            "NLM confirmed: Gaur Ch10 actual text for Mercury in Leo = 'Grains "
            "medium; metals/gur/khand cheap.' Mercury combust = 'wheat/gram/ghee "
            "cheap.' Stock market and textile/jute NOT in source. Textile/jute "
            "belongs to Gemini (Gaur Ch8). Complete rewrite to source-faithful "
            "commodity signal."
        ),
    },
]

# ── Misclassification retirement (rule 4) ─────────────────────────────────────

MISCLASSIFIED = {
    "rule_id": "mundane-gopal-ch3-trikona-trikona-billionaire",
    "note": (
        "MISCLASSIFIED AS MUNDANE. NLM confirmed: Gopal Ch3 is titled 'CELEBRITY "
        "HOROSCOPE -- AN ANALYSIS' and covers natal astrology for individual opulence "
        "(Amitabh Bachchan, B.V. Raman, Bill Gates, etc.). Trikona-Trikona Raja Yoga "
        "analysis of Bill Gates is explicitly a natal rule for individual destiny -- "
        "not a collective/national wealth forecast. Rule does not belong in "
        "mundane_jyotish library. Set to pending_human_review for co-founder "
        "decision: retire permanently or move to natal_jyotish science library."
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
    print(f"Category C3 NLM corrections ({len(PATCHES)} patches + 1 misclassification)")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    patched = 0

    # ── Field patches ──────────────────────────────────────────────────────────
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
        print(f"  note: {p['note'][:100]}...")

        if args.apply:
            res = col.update_one(
                {"rule_id": rid},
                {"$set": {
                    field:                     p["new"],
                    "approval_status":         "pending_review",
                    "validation.patch_reason": "cat_c3_nlm_correction",
                    "validation.patch_note":   p["note"],
                    "validation.patched_at":   now,
                    "validation.patched_by":   "patch_mundane_cat_c3_nlm_corrections.py",
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

    # ── Misclassification retirement ───────────────────────────────────────────
    rid = MISCLASSIFIED["rule_id"]
    r = col.find_one(
        {"rule_id": rid, "science_id": "mundane_jyotish"},
        {"_id": 0, "rule_id": 1, "title": 1, "approval_status": 1},
    )
    print(f"  {rid}")
    if not r:
        print(f"  ⚠️  NOT FOUND\n")
    else:
        print(f"  current status : {r.get('approval_status','?')}")
        print(f"  action         : RETIRE → pending_human_review (misclassified as mundane)")
        print(f"  note           : {MISCLASSIFIED['note'][:100]}...")

        if args.apply:
            res = col.update_one(
                {"rule_id": rid},
                {"$set": {
                    "approval_status":                    "pending_human_review",
                    "validation.verdict":                 "misclassified",
                    "validation.flag_reason":             MISCLASSIFIED["note"],
                    "validation.classification_note":     (
                        "MISCLASSIFIED_NATAL: This is a natal astrology rule. "
                        "Source: Gopal Ch3 Celebrity Horoscope Analysis. "
                        "Does not belong in mundane_jyotish library."
                    ),
                    "validation.misclassified_at":        now,
                    "validation.misclassified_by":        "patch_mundane_cat_c3_nlm_corrections.py",
                }},
            )
            if res.modified_count:
                print(f"  ✅ Retired → pending_human_review (misclassified_natal)\n")
                patched += 1
            else:
                print(f"  ⚠️  No change written\n")
        else:
            print(f"  🔍 WOULD RETIRE → pending_human_review\n")
            patched += 1

    # ── Summary ────────────────────────────────────────────────────────────────
    print(f"{'─'*65}")
    total = len(PATCHES) + 1
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
        pending = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "pending_review"}
        )
        print(f"Applied: {patched} / {total}")
        print(f"\nLibrary status:")
        print(f"  approved             : {approved}")
        print(f"  pending_human_review : {phr}")
        print(f"  flagged              : {flagged}")
        print(f"  pending_review       : {pending}")
    else:
        print(f"Dry run: {patched} / {total} would be patched.")
        print(f"Re-run with --apply to write.")

    client.close()


if __name__ == "__main__":
    main()
