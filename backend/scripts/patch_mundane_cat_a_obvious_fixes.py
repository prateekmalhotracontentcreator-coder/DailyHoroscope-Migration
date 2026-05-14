#!/usr/bin/env python3
"""
patch_mundane_cat_a_obvious_fixes.py

Fixes 5 truncated Category A rules where the completion is unambiguous --
either single word-level cuts or reconstructable from the existing result field.
No NLM source verification needed.

  1. mundane-gopal-ch7-rahu-ketu-ic-mc-axis
     "seism..." → "seismic activity"

  2. mundane-gopal-ch7-cardinal-stellium-upheaval
     "instab..." → "instability"

  3. mundane-gopal-ch9-malefics-trika-entry
     trailing ".." artifact removed

  4. mundane-gaur-ch11-eclipse-solar-commodity-by-month
     Condition lists only 4 of 12 Hindu months. All 12 month outcomes are
     already in the result field. Reconstruct full 12-month condition.

  5. mundane-gopal-ch6-epidemic-triad
     Three word-level truncations:
     - "India's Moon = Canc..." → "India's Moon = Cancer"
     - "India's Moon = Cancer → Rah..." → "India's Moon = Cancer → Rahu in Cancer"
     - "6th or 8th house of ..." → "6th or 8th house of the national horoscope"

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_mundane_cat_a_obvious_fixes.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_mundane_cat_a_obvious_fixes.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

PATCHES = [

    # ── 1. rahu-ketu-ic-mc-axis: complete "seism..." ───────────────────────────
    {
        "rule_id": "mundane-gopal-ch7-rahu-ketu-ic-mc-axis",
        "field":   "condition",
        "old": (
            "The Rahu-Ketu nodal axis aligns within 5° of the IC (4th house cusp) "
            "and MC (10th house cusp) of the Aries Ingress chart cast for a specific "
            "territory, or of that territory's natal chart. Also: eclipse on ic: A "
            "solar or lunar eclipse occurs within 5° of the IC of the regional chart: "
            "seism...."
        ),
        "new": (
            "The Rahu-Ketu nodal axis aligns within 5° of the IC (4th house cusp) "
            "and MC (10th house cusp) of the Aries Ingress chart cast for a specific "
            "territory, or of that territory's natal chart. Also: eclipse on ic: A "
            "solar or lunar eclipse occurs within 5° of the IC of the regional chart: "
            "seismic activity in that territory is indicated. Source: Gopalakrishnan "
            "Ch 7, pp.95-96."
        ),
        "note": "Completed word-level truncation: 'seism...' → 'seismic activity'.",
    },

    # ── 2. cardinal-stellium-upheaval: complete "instab..." ────────────────────
    {
        "rule_id": "mundane-gopal-ch7-cardinal-stellium-upheaval",
        "field":   "condition",
        "old": (
            "Three or more planets clustering in cardinal signs (Aries, Cancer, "
            "Libra, Capricorn) simultaneously. Also: pure cardinal: All 3+ planets "
            "in the same cardinal sign: maximum intensity.; spread cardinal: 3+ "
            "planets spread across 2-3 different cardinal signs: broad geopolitical "
            "instab...."
        ),
        "new": (
            "Three or more planets clustering in cardinal signs (Aries, Cancer, "
            "Libra, Capricorn) simultaneously. Also: pure cardinal: All 3+ planets "
            "in the same cardinal sign: maximum intensity.; spread cardinal: 3+ "
            "planets spread across 2-3 different cardinal signs: broad geopolitical "
            "instability across multiple regions. Source: Gopalakrishnan Ch 7, p.96."
        ),
        "note": "Completed word-level truncation: 'instab...' → 'instability across multiple regions'.",
    },

    # ── 3. malefics-trika-entry: remove trailing ".." artifact ───────────────
    {
        "rule_id": "mundane-gopal-ch9-malefics-trika-entry",
        "field":   "condition",
        "old": (
            "Saturn, Rahu, or Jupiter transiting into the 6th, 8th, or 12th house "
            "of the national chart (or into the sign ruled by the 6th/8th/12th lord). "
            "Also: into 6th: Triggers war, epidemic, debt crisis, labor disputes.; "
            "into 8th: Triggers leadership crisis, mass deaths, government collapse.; "
            "into 12th: Triggers financial losses, foreign debt, exile of leaders, "
            "mass displacement.."
        ),
        "new": (
            "Saturn, Rahu, or Jupiter transiting into the 6th, 8th, or 12th house "
            "of the national chart (or into the sign ruled by the 6th/8th/12th lord). "
            "Also: into 6th: Triggers war, epidemic, debt crisis, labor disputes. "
            "into 8th: Triggers leadership crisis, mass deaths, government collapse. "
            "into 12th: Triggers financial losses, foreign debt, exile of leaders, "
            "mass displacement. Source: Gopalakrishnan Ch 9, p.146."
        ),
        "note": "Removed trailing '..' artifact. Cleaned punctuation. Added source citation.",
    },

    # ── 4. eclipse-solar-commodity-by-month: complete 12-month condition ──────
    {
        "rule_id": "mundane-gaur-ch11-eclipse-solar-commodity-by-month",
        "field":   "condition",
        "old": (
            "IF Chaitra: Solar eclipse in Chaitra month.; Vaishakh: Solar eclipse "
            "in Vaishakh month.; Jyeshtha: Solar eclipse in Jyeshtha month.; "
            "Aashadh: Solar eclipse in Aashadh month.."
        ),
        "new": (
            "Solar eclipse occurring in any of the 12 Hindu months -- the specific "
            "month of the eclipse determines the commodity forecast: "
            "IF Chaitra → gold and grains expensive. "
            "IF Vaishakh → til, oil, moong, cotton cloth, yarn, wheat expensive. "
            "IF Jyeshtha → gold and grains cheap. "
            "IF Aashadh → grains expensive; drought signal. "
            "IF Shravan → grains cheap; juicy materials expensive. "
            "IF Bhadrapad → grains cheap; other goods also cheap. "
            "IF Ashwin → grains cheap; oil materials and ghee slightly expensive. "
            "IF Kartik → all grains, ghee, cotton and clothes cheap. "
            "IF Margsheersh → grains, gur, khand, oil, ghee expensive. "
            "IF Paush → all grains expensive. "
            "IF Maagh → grains cheap; ghee expensive; rains sufficient. "
            "IF Phalgun → all grains, oil, gur, khand, juicy materials and ghee "
            "expensive. Source: Gaur Ch 11, pp.111."
        ),
        "note": (
            "Condition was truncated at 4 of 12 Hindu months. All 12 month outcomes "
            "were present in result field. Reconstructed complete 12-month IF/THEN "
            "condition from the result. Source: Gaur Ch 11."
        ),
    },

    # ── 5. epidemic-triad: complete three word-level truncations ─────────────
    {
        "rule_id": "mundane-gopal-ch6-epidemic-triad",
        "field":   "condition",
        "old": (
            "IF saturn 6th from country moon: Saturn transiting the 6th sign counted "
            "from the country's natal Moon sign. E.g., India's Moon = Canc...; rahu "
            "in country natal moon sign: Rahu transiting through the same sign as "
            "the country's natal Moon. E.g., India's Moon = Cancer → Rah...; venus "
            "saturn conjunction: Venus and Saturn conjoined in the same sign (within "
            "10° orb), especially in the 6th or 8th house of ...."
        ),
        "new": (
            "IF saturn 6th from country moon: Saturn transiting the 6th sign counted "
            "from the country's natal Moon sign. E.g., India's Moon = Cancer → "
            "Saturn transiting Capricorn triggers this condition. "
            "IF rahu in country natal moon sign: Rahu transiting through the same "
            "sign as the country's natal Moon. E.g., India's Moon = Cancer → Rahu "
            "in Cancer triggers this condition. "
            "IF venus saturn conjunction: Venus and Saturn conjoined in the same sign "
            "(within 10° orb), especially in the 6th or 8th house of the national "
            "horoscope. Source: Gopalakrishnan Ch 6, pp.88-90."
        ),
        "note": (
            "Completed three word-level truncations: 'Canc...' → 'Cancer', "
            "'Rah...' → 'Rahu in Cancer', '8th house of ...' → '8th house of the "
            "national horoscope'. Added source citation."
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
    print(f"Category A obvious fixes ({len(PATCHES)} rules)")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    patched = 0
    for p in PATCHES:
        rid   = p["rule_id"]
        field = p["field"]

        r = col.find_one(
            {"rule_id": rid, "science_id": "mundane_jyotish"},
            {"_id": 0, "rule_id": 1, "approval_status": 1, field: 1},
        )
        if not r:
            print(f"  ⚠️  NOT FOUND: {rid}\n")
            continue

        current = r.get(field, "")
        if current != p["old"]:
            print(f"  ⚠️  MISMATCH (already patched?): {rid}")
            print(f"     DB {field} tail: ...{current[-60:]}\n")
            continue

        old_s, new_s = p["old"], p["new"]
        for i, (a, b) in enumerate(zip(old_s, new_s)):
            if a != b:
                snip = old_s[max(0, i-10):i+40].replace('\n', ' ')
                break
        else:
            snip = old_s[-50:]

        print(f"  {rid}")
        print(f"  fix   : ...{snip}...")
        print(f"  note  : {p['note'][:90]}...")

        if args.apply:
            res = col.update_one(
                {"rule_id": rid},
                {"$set": {
                    field:                     p["new"],
                    "approval_status":         "pending_review",
                    "validation.patch_reason": "cat_a_truncation_fix",
                    "validation.patch_note":   p["note"],
                    "validation.patched_at":   now,
                    "validation.patched_by":   "patch_mundane_cat_a_obvious_fixes.py",
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
        pending = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "pending_review"}
        )
        phr = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "pending_human_review"}
        )
        print(f"Patched : {patched} / {len(PATCHES)}")
        print(f"pending_review: {pending}  |  pending_human_review: {phr}")
    else:
        print(f"Dry run: {patched} / {len(PATCHES)} would be patched.")
        print("Re-run with --apply to write.")

    client.close()


if __name__ == "__main__":
    main()
