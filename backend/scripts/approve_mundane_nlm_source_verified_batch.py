#!/usr/bin/env python3
"""
approve_mundane_nlm_source_verified_batch.py

Approves 4 PHR rules -- all NLM-confirmed, no content changes needed.

  1. gaur-ch11-eclipse-scorpio-drought
     NLM Q4: Gaur Ch11 explicitly states "8. Scorpio: Due to solar/lunar eclipse
     there is drought that causes agony to masses." Direct source match. Approved.

  2. mehta-ch2-double-eclipse-14-days-destruction
     NLM Q5: Mehta explicitly states "If two eclipses -- one solar and one lunar --
     occur within 14 days, there will generally be national disaster like war,
     assassination etc." The apparent contradiction with gaur-ch11-eclipse-lunar-
     solar-sequence-religious-happiness is resolved: they measure DIFFERENT things.
     Mehta = temporal proximity → intensity/severity gate.
     Gaur = sequence order → directional modifier (Solar→Lunar = religious happiness;
     Lunar→Solar = tyrant rulers). These are complementary, not contradictory.

  3. mehta-ch7-koorma-northwest-affliction-tribal-insurgency
     NLM Q6: Mehta Ch7 explicitly lists North Pakistan, Afghanistan, Northern
     Kashmir, Jodhpur, Upper Oxus Valley, and Madra (between Ravi and Jhelum rivers)
     as regions for the NW Koorma cluster. Geographic specificity is source-faithful.

  4. mundane-gopal-ch14-mars-proximity-children
     NLM Q11: Gopalakrishnan Ch14 explicitly documents all three outcomes of Mars
     perigee: (a) mass death of children; (b) high efficiency in manufacturing;
     (c) surge in surgical costs and fire accidents. Validated against July 2003
     Mars perigee (55.8M km -- closest in 73,000 years).

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_nlm_source_verified_batch.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_nlm_source_verified_batch.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

ITEMS = [

    # ── 1. gaur-ch11-eclipse-scorpio-drought ─────────────────────────────────
    {
        "rule_id": "mundane-gaur-ch11-eclipse-scorpio-drought",
        "note": (
            "NLM source-verified (Q4). Gaur Ch11 'Results of Eclipses in Different "
            "Signs' explicitly states: '8. Scorpio: Due to solar/lunar eclipse there "
            "is drought that causes agony to masses.' Direct source match -- drought "
            "attribution to Scorpio eclipse is explicit, not inferred from Ketu axis "
            "or 8th-house themes. Result faithfully represents Gaur's text. "
            "Approved by co-founder."
        ),
    },

    # ── 2. mehta-ch2-double-eclipse-14-days-destruction ──────────────────────
    {
        "rule_id": "mehta-ch2-double-eclipse-14-days-destruction",
        "note": (
            "NLM source-verified (Q5). Mehta Ch2 explicitly states: 'If two eclipses "
            "-- one solar and one lunar -- occur within 14 days, there will generally "
            "be national disaster like war, assassination etc.' Confirmed. The flagged "
            "contradiction with gaur-ch11-eclipse-lunar-solar-sequence-religious-happiness "
            "is resolved: the two rules are NOT contradictory -- they measure different "
            "dimensions. Mehta (Q5 / proximity): temporal closeness = SEVERITY GATE "
            "(intensity of crisis window). Gaur Ch11 (sequence): Solar-before-Lunar = "
            "religious happiness; Lunar-before-Solar = tyrant rulers = DIRECTIONAL "
            "MODIFIER. Engine should apply Mehta as severity gate; Gaur Ch11 as "
            "directional/flavor modifier. Both confirmed; no contradiction. "
            "Approved by co-founder."
        ),
    },

    # ── 3. mehta-ch7-koorma-northwest-affliction-tribal-insurgency ────────────
    {
        "rule_id": "mehta-ch7-koorma-northwest-affliction-tribal-insurgency",
        "note": (
            "NLM source-verified (Q6). Mehta Ch7 'VII North West' section explicitly "
            "lists the NW Koorma cluster (Uttarashadha, Sravana, Dhanishtha) and maps "
            "it to: North Pakistan, Afghanistan, Northern Kashmir, Jodhpur, Upper Oxus "
            "Valley, and the ancient region of Madra (between the Ravi and Jhelum "
            "rivers -- modern Sialkot/West Punjab area). Mehta explicitly links "
            "affliction of these stars to destruction of kings/regimes in those regions. "
            "All geographic specificity in the rule is source-faithful. "
            "Approved by co-founder."
        ),
    },

    # ── 4. mundane-gopal-ch14-mars-proximity-children ────────────────────────
    {
        "rule_id": "mundane-gopal-ch14-mars-proximity-children",
        "note": (
            "NLM source-verified (Q11). Gopalakrishnan Ch14 (Hits of 2006) explicitly "
            "documents all three Mars perigee outcomes: (a) mass death of children via "
            "epidemic or violence; (b) high efficiency in manufacturing units; "
            "(c) surge in surgical costs and fire accidents. All outcomes validated "
            "against the July 2003 Mars perigee benchmark (55.8M km -- closest approach "
            "in 73,000 years). The extraordinary claim is Gopal's own empirical "
            "finding, not analyst interpolation. Result is complete and source-faithful. "
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
    print(f"NLM source-verified approvals ({len(ITEMS)} rules -- no content changes)")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    promoted = 0
    for item in ITEMS:
        rid = item["rule_id"]
        r = col.find_one(
            {"rule_id": rid, "science_id": "mundane_jyotish"},
            {"_id": 0, "rule_id": 1, "approval_status": 1},
        )
        if not r:
            print(f"  ⚠️  NOT FOUND: {rid}\n")
            continue

        print(f"  {rid}")
        print(f"  status : {r.get('approval_status','?')}")
        print(f"  note   : {item['note'][:100]}...")

        update_set = {
            "approval_status":          "approved",
            "validation.verdict":       "approved",
            "validation.approved_by":   "co_founder_nlm_verified_may2026",
            "validation.approved_at":   now,
            "validation.approved_note": item["note"],
        }

        if args.apply:
            res = col.update_one(
                {"rule_id": rid},
                {"$set": update_set,
                 "$unset": {"validation.spot_check_reason": "",
                            "validation.flag_reason": ""}},
            )
            if res.modified_count:
                print(f"  ✅ APPROVED\n")
                promoted += 1
            else:
                print(f"  ⚠️  No change written\n")
        else:
            print(f"  🔍 WOULD APPROVE\n")
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
