#!/usr/bin/env python3
"""
patch_mundane_cat_a_nlm_batch.py

Completes 5 truncated Category A rules using NLM-sourced text (May 2026).

  1. mundane-gaur-ch10-mercury-motion-differentials
     Gap in Direct motion entry: "later expensive.... IF retrograde" was missing
     "Gur and perfumes are also expensive." NLM: no additional text between
     Direct and Retrograde entries.

  2. mundane-mehta-ch20-terrorism-ten-parameters
     Parameters 2 (partial) and 3 (partial) completed; parameters 4-10 added.
     Full 10-parameter condition now complete.

  3. mundane-mehta-ch26-congress-i-dasha-history
     Truncated at "Sanjay G...". Complete passage: aircrash 23.06.1980. Plus
     all remaining dasha correlations (Mars, Rahu, Venus Dashas).

  4. mundane-mehta-ch26-bjp-dasha-history
     Truncated at "Mercury (lagna lord) in Rahu...". Complete: "in Rahu/Ketu
     axis aspected by malefics Mars and Saturn; also aspected by 10th lord
     Jupiter." Plus all remaining dasha correlations.

  5. mundane-mehta-ch26-retrograde-malefic-dasha-crisis
     Four sub-rules each truncated. Complete text from NLM for all four.

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_mundane_cat_a_nlm_batch.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/patch_mundane_cat_a_nlm_batch.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

PATCHES: list[dict] = [

    # ── 1. mercury-motion-differentials ──────────────────────────────────────
    {
        "rule_id": "mundane-gaur-ch10-mercury-motion-differentials",
        "field":   "condition",
        "old": (
            "IF direct motion → Mercury direct: grains expensive. Silver and "
            "cotton undergo fluctuations initially, later expensive.... IF "
            "retrograde → Mercury retrograde: juicy materials (gur/khand) "
            "expensive. Grains cheap. IF rising → Mercury rises: wheat and "
            "gram expensive. IF combusted → Mercury combusted: wheat, gram, "
            "ghee cheap.."
        ),
        "new": (
            "IF direct motion → Mercury direct: grains expensive. Silver and "
            "cotton undergo fluctuations initially, later expensive. Gur and "
            "perfumes are also expensive. "
            "IF retrograde → Mercury retrograde: juicy materials (gur/khand) "
            "expensive. Grains cheap. "
            "IF rising → Mercury rises: wheat and gram expensive. "
            "IF combusted → Mercury combusted: wheat, gram, ghee cheap. "
            "Source: Gaur Ch 10, pp.98."
        ),
        "note": (
            "NLM confirmed missing text: 'Gur and perfumes are also expensive' "
            "completes the Direct motion entry. No additional text between "
            "Direct and Retrograde entries. Trailing '..' artifact removed."
        ),
    },

    # ── 2. terrorism-ten-parameters ──────────────────────────────────────────
    {
        "rule_id": "mundane-mehta-ch20-terrorism-ten-parameters",
        "field":   "condition",
        "old": (
            "IF source article: K.N. Rao in Journal of Astrology, "
            "July-September 2002; parameter 1: Combination of Mars with "
            "Rahu/Ketu -- together, in opposition, or in kendras from each "
            "other.; parameter 2: Combination of Saturn-Rahu conjunction, "
            "opposition or in square. 'When Saturn and Rahu join together...; "
            "parameter 3: Combination of Saturn and Mars conjunction, "
            "opposition or in square. 'Saturn or Mars opposition few ...."
        ),
        "new": (
            "Source: K.N. Rao, Journal of Astrology, July-September 2002 "
            "(Mehta/Rao Ch20). "
            "When 4 or more of the following 10 parameters are simultaneously "
            "active in a national or world chart, increased terrorist activity "
            "is indicated: "
            "Parameter 1: Combination of Mars with Rahu/Ketu -- together, in "
            "opposition, or in kendras from each other. "
            "Parameter 2: Saturn-Rahu conjunction, opposition, or in square. "
            "Rao: 'When Saturn and Rahu join together, anarchical conditions "
            "and nihilistic philosophy gets accepted. Religious fundamentalism "
            "of extreme form... gets noticed. Saturn and Rahu are tamasic "
            "planets and terrorism is an act of tamasic. These two planets "
            "show cruelty, a single-minded purpose to kill and destroy.' "
            "Parameter 3: Saturn or Mars opposition few months before or during "
            "Saturn-Rahu conjunction -- Mars ignites it all. "
            "Parameter 4: Affliction to Sun. "
            "Parameter 5: Affliction to Moon -- when under influence of Saturn "
            "and Rahu, signals acceptance of nihilistic philosophy and extreme "
            "cruelty. When all four (Rahu, Saturn, Sun, Moon) join in one "
            "rashi, society becomes aware of their terrorist presence. "
            "Parameter 6: Saturn or Rahu in Rohini nakshatra, or alternatively "
            "in Taurus rashi. "
            "Parameter 7: Benefic planets (Jupiter, Venus, Mercury) relegated "
            "to secondary role with no protective power; Guru-chandal yoga "
            "often forms when terrorism becomes explosive. "
            "Parameter 8: Retrograde Mars and/or Saturn -- become more sinister "
            "and deadly, causing maximum damage. 'Whenever wars take place or "
            "break out, Mars has been found to be retrograde.' "
            "Parameter 9: Role of eclipses -- timing of affliction of eclipse "
            "point to be carefully noted; eclipses last for a long time. "
            "Parameter 10: Degrees of closeness of planets to be carefully "
            "observed -- tighter orbs indicate higher severity."
        ),
        "note": (
            "NLM completed parameters 2 and 3 (full Rao quotes) and provided "
            "parameters 4-10. Full 10-parameter condition now source-faithful "
            "to Mehta/Rao Ch20 (Journal of Astrology July-September 2002)."
        ),
    },

    # ── 3. congress-i-dasha-history ──────────────────────────────────────────
    {
        "rule_id": "mundane-mehta-ch26-congress-i-dasha-history",
        "field":   "condition",
        "old": (
            "IF party birth: Congress-I (Indira Congress): 2 January 1978, "
            "Lagna 15°01'; key correlations -- Elections Jan 1980 -- won 351 "
            "of 524 seats (landslide). But tragedy too: Sanjay G...."
        ),
        "new": (
            "IF party birth: Congress-I (Indira Congress): 2 January 1978, "
            "Lagna 15°01'. "
            "Key dasha correlations (Mehta/Rao Ch26): "
            "Moon-Mercury Dasha (1980): Landslide victory (351 of 524 seats); "
            "India entered the space age with satellite launch. Tragedy within "
            "same dasha: Sanjay Gandhi died in aircrash on 23.06.1980. Indira "
            "Gandhi had admitted to Pupul Jayakar that astrologers had warned "
            "her about early violent death of Sanjay Gandhi. "
            "Mars Mahadasha (1984-1991): Assassination of Indira Gandhi "
            "(31 Oct 1984) under Mars/Venus antardasha; Mars is planet of "
            "violence and lord of the 9th house (religion). "
            "Mars/Ketu antardasha: Rajiv Gandhi faced the Bofors scandal and "
            "fell from power in 1989. "
            "Rahu/Rahu chidra dasha (1991): Assassination of Rajiv Gandhi in "
            "a suicidal attack; Rahu is with Moon in whose rashi debilitated "
            "Mars is placed. "
            "Rahu/Venus (2004): Return to power with support of leftist parties. "
            "Source: Mehta/Rao Ch26."
        ),
        "note": (
            "NLM completed Sanjay Gandhi aircrash passage (23.06.1980) and "
            "provided all remaining dasha correlations: Moon-Mercury, Mars, "
            "Mars/Ketu, Rahu/Rahu, Rahu/Venus. Full condition now source-faithful."
        ),
    },

    # ── 4. bjp-dasha-history ─────────────────────────────────────────────────
    {
        "rule_id": "mundane-mehta-ch26-bjp-dasha-history",
        "field":   "condition",
        "old": (
            "IF party birth: BJP: 6 April 1980, 11:45, Delhi. Lagna 23°36'.; "
            "key correlations -- BJP obtained only 2 seats of 543 in 1984 "
            "elections. Mercury (lagna lord) in Rahu...."
        ),
        "new": (
            "IF party birth: BJP: 6 April 1980, 11:45, Delhi. Lagna 23°36'. "
            "Key dasha correlations (Mehta/Rao Ch26): "
            "Natal chart: Mercury (lagna lord) in Rahu/Ketu axis aspected by "
            "malefics Mars and Saturn; also aspected by 10th lord Jupiter. "
            "Result: BJP obtained only 2 seats of 543 in 1984 elections "
            "(lagna lord in Rahu/Ketu axis with malefic aspect = minimal "
            "electoral performance). "
            "Ketu/Jupiter antardasha (1989): Electoral breakthrough (88 seats); "
            "Jupiter is the 10th lord. "
            "Ketu/Saturn antardasha (1990): Arrest of L.K. Advani and "
            "withdrawal of support from government. "
            "Venus/Venus (1992): Ayodhya structure demolished -- violent "
            "disturbance in the 4th house of peace. "
            "Venus/Mars and Venus/Rahu (1998-1999): Pokhran nuclear tests and "
            "Kargil War; Mars and Rahu in 10th house from Venus raised India's "
            "international stature. "
            "Venus/Jupiter (2004): Loss of mandate; Jupiter is 8th lord from "
            "Venus antardasha. "
            "Source: Mehta/Rao Ch26."
        ),
        "note": (
            "NLM completed Mercury-Rahu/Ketu sentence: 'aspected by malefics "
            "Mars and Saturn; also aspected by 10th lord Jupiter.' Plus all "
            "remaining dasha correlations (Ketu/Jupiter, Venus/Venus, "
            "Venus/Mars-Rahu, Venus/Jupiter). Full condition now source-faithful."
        ),
    },

    # ── 5. retrograde-malefic-dasha-crisis ───────────────────────────────────
    {
        "rule_id": "mundane-mehta-ch26-retrograde-malefic-dasha-crisis",
        "field":   "condition",
        "old": (
            "IF primary rule: When a retrograde malefic planet (Mars R, Saturn "
            "R, Rahu -- always retrograde) is the active Mahadash...; mars "
            "retrograde rule: Mars retrograde as Mahadasha lord: Mars is planet "
            "of violence and lord of marka house. Being retrogr...; rahu chidra "
            "dasha rule: Rahu chidra dasha (Rahu/Rahu sub-period) is the "
            "transition antardasha before Rahu Mahadasha ends. If...; compound "
            "signal: If BOTH the Mahadasha lord is retrograde malefic AND the "
            "party's 8th house (or marka lords 2nd/7th) ...."
        ),
        "new": (
            "Primary rule: When a retrograde malefic planet (Mars R, Saturn R, "
            "or Rahu -- always retrograde) is the active Mahadasha lord for a "
            "political party chart, major changes -- good or bad -- have taken "
            "place. The retrograde state intensifies the planet's significations. "
            "Mars retrograde rule: Mars retrograde as Mahadasha lord -- Mars is "
            "the planet of violence and lord of the marka house. Being retrograde "
            "it becomes more evil. Historical anchor: Indira Gandhi was brutally "
            "murdered under Mars Mahadasha (Mars R = marka + violence, intensified). "
            "Rahu chidra dasha rule: Rahu/Rahu (chidra dasha -- the transition "
            "antardasha before Rahu Mahadasha ends) is particularly dangerous. "
            "Historical anchor: On 21.05.1991 during Rahu/Rahu, Congress party "
            "lost its leader Rajiv Gandhi, assassinated in a suicidal attack. "
            "Compound signal: If BOTH the Mahadasha lord is a retrograde malefic "
            "AND Rahu is placed in a marka house (2nd or 7th) -- particularly "
            "with Moon in a rashi where a debilitated Mars is also placed -- the "
            "compound signal indicates violent death of the party's leader. "
            "Rahu is a violent planet clearly indicating violent death to its "
            "leader when positioned in marka-house partnerships. "
            "Source: Mehta/Rao Ch26."
        ),
        "note": (
            "NLM completed all four sub-rules: (a) primary rule -- 'major changes "
            "good or bad'; (b) Mars R rule -- Indira Gandhi murder under Mars "
            "Mahadasha; (c) Rahu chidra dasha -- Rajiv Gandhi 21.05.1991; "
            "(d) compound signal -- Rahu in marka + Moon in Mars-debilitated rashi "
            "= violent death to leader. Full condition now source-faithful to "
            "Mehta/Rao Ch26."
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
    print(f"Category A NLM batch ({len(PATCHES)} rules)")
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
            print(f"     DB tail: ...{current[-60:]}\n")
            continue

        print(f"  {rid}")
        print(f"  status: {r.get('approval_status','?')}")
        print(f"  note  : {p['note'][:90]}...")

        if args.apply:
            res = col.update_one(
                {"rule_id": rid},
                {"$set": {
                    field:                     p["new"],
                    "approval_status":         "pending_review",
                    "validation.patch_reason": "cat_a_nlm_truncation_completion",
                    "validation.patch_note":   p["note"],
                    "validation.patched_at":   now,
                    "validation.patched_by":   "patch_mundane_cat_a_nlm_batch.py",
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
        approved = col.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "approved"}
        )
        print(f"Patched: {patched} / {len(PATCHES)}")
        print(f"approved={approved}  PHR={phr}  pending_review={pending}")
    else:
        print(f"Dry run: {patched} / {len(PATCHES)} would be patched.")
        print("Re-run with --apply to write.")

    client.close()


if __name__ == "__main__":
    main()
