#!/usr/bin/env python3
"""
approve_mundane_samvatsar_batch.py

Resolves all 8 Gaur Ch1 Samvatsar PHR rules.

  5 false flags -- approve as-is:
    1. samvatsar-group-quality-modifier    -- validator claimed "secondary b" truncation;
       DB has full sentence "...the group is a secondary background modifier."
    2. samvatsar-vishnu-lord               -- validator claimed truncation at "Ashwin -- juices";
       DB has "Ashwin -- juices costly but become cheap later. Kartik through Phalgun -- grains
       cheap." -- all 12 months complete.
    3. samvatsar-shiv-lord                 -- validator claimed truncation at "Phalgu";
       DB has "Phalgun -- full of difficulties and agony." -- all 12 months complete.
    4. samvatsar-sun-lord                  -- validator claimed truncation at "Magh -- juicy";
       DB has "Kartik/Margsheersh/Paush/Magh -- juicy materials dearer. Phalgun -- medium."
       -- all 12 months complete.
    5. samvatsar-venus-year-earthquake-calamity-specific
       -- validator flagged #37 Shobhan as non-existent; NLM confirmed Gaur Ch1 explicitly
       uses "Shobhan" for #37 (Venus-lord), not the standard "Shodhana". False flag.

  3 result completions + approve:
    6. samvatsar-jupiter-lord              -- Jyeshtha month missing from monthly pattern.
       NLM: varies by Samvatsar (diseases/Subhanu #17; cheap/Jai #28, Rudhirodgari #57;
       medium rains/Anand #48). Inserted between Baisakh and Aashadh.
    7. samvatsar-venus-lord-natural-calamities
       -- Kartik month missing from monthly pattern.
       NLM: varies by Samvatsar (high grain prices/Taran #18, Raktaksha #58;
       cheap/Manmath #29; diseases/Rakshas #49). Inserted between Bhadrapad and Ashwin.
    8. samvatsar-rahu-lord-drought-north-floods-east
       -- Ashwin month missing from monthly pattern; also #60 Kshaya group ambiguity.
       NLM: Ashwin = diseases + price instability (varies by Samvatsar).
       #60 Kshaya: Rahu-lord AND Shiv-group simultaneously -- both correct per Gaur Ch1.
       Inserted Ashwin between Bhadrapad and Kartik; added Kshaya dual-classification note.

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_samvatsar_batch.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/approve_mundane_samvatsar_batch.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

ITEMS = [

    # ── 1. group-quality-modifier -- false flag ────────────────────────────────
    {
        "rule_id":    "gaur-ch1-samvatsar-group-quality-modifier",
        "result_old": None,
        "result_new": None,
        "note": (
            "False flag (spot_check). Validator claimed result truncated at 'secondary b'. "
            "DB has the complete sentence: 'the group is a secondary background modifier.' "
            "Result is fully formed and coherent. No content change needed. "
            "Approved by co-founder."
        ),
    },

    # ── 2. vishnu-lord -- false flag ───────────────────────────────────────────
    {
        "rule_id":    "gaur-ch1-samvatsar-vishnu-lord-law-order-diseases",
        "result_old": None,
        "result_new": None,
        "note": (
            "False flag (spot_check). Validator claimed truncation at 'Ashwin -- juices'. "
            "DB has: 'Ashwin -- juices costly but become cheap later. Kartik through "
            "Phalgun -- grains cheap.' -- all 12 Hindu months accounted for. Monthly "
            "pattern is complete. No content change needed. Approved by co-founder."
        ),
    },

    # ── 3. shiv-lord -- false flag ─────────────────────────────────────────────
    {
        "rule_id":    "gaur-ch1-samvatsar-shiv-lord-rulers-overthrown",
        "result_old": None,
        "result_new": None,
        "note": (
            "False flag (spot_check). Validator claimed truncation at 'Phalgu'. "
            "DB has: 'Phalgun -- full of difficulties and agony.' -- all 12 months present. "
            "Monthly pattern is complete. No content change needed. Approved by co-founder."
        ),
    },

    # ── 4. sun-lord -- false flag ──────────────────────────────────────────────
    {
        "rule_id":    "gaur-ch1-samvatsar-sun-lord-less-rain-insurgency",
        "result_old": None,
        "result_new": None,
        "note": (
            "False flag (spot_check). Validator claimed truncation at 'Magh -- juicy "
            "materials dearer.' DB has: 'Kartik/Margsheersh/Paush/Magh -- juicy materials "
            "dearer. Phalgun -- medium.' -- all 12 months present. Monthly pattern is "
            "complete. No content change needed. Approved by co-founder."
        ),
    },

    # ── 5. venus-year-earthquake -- false flag ─────────────────────────────────
    {
        "rule_id":    "gaur-ch1-samvatsar-venus-year-earthquake-calamity-specific",
        "result_old": None,
        "result_new": None,
        "note": (
            "False flag (spot_check). Validator flagged '#37 Shobhan does not exist in "
            "standard 60-year Samvatsar cycle.' NLM confirmed: Gaur Ch1 explicitly uses "
            "'Shobhan' for Samvatsar #37 and assigns Venus as its lord. Gaur's text uses "
            "'Shobhkrit' for #36 (Jupiter-lord) and 'Shobhan' for #37 (Venus-lord) -- "
            "this is Gaur's own nomenclature, not a factual error. Condition is correct "
            "as stored. Approved by co-founder."
        ),
    },

    # ── 6. jupiter-lord -- Jyeshtha completion ────────────────────────────────
    {
        "rule_id": "gaur-ch1-samvatsar-jupiter-lord-excessive-rains-disease",
        "result_old": (
            "Diseases are excessive. Grain production is medium. Though rulers engage in "
            "wars, people have a feeling of security. Rains are excessive; cattle give "
            "more milk. All things are dear (high prices). MONTHLY PATTERN: Chaitra -- "
            "medium. Baisakh -- food materials costly. Aashadh/Shravan -- rains normal. "
            "Bhadrapad -- excessive rains. Ashwin -- excessive disease. Kartik -- "
            "beneficial. Margsheersh/Paush/Magh/Phalgun -- grains cheap."
        ),
        "result_new": (
            "Diseases are excessive. Grain production is medium. Though rulers engage in "
            "wars, people have a feeling of security. Rains are excessive; cattle give "
            "more milk. All things are dear (high prices). MONTHLY PATTERN: Chaitra -- "
            "medium. Baisakh -- food materials costly. Jyeshtha -- varies by Samvatsar "
            "(diseases/Subhanu #17; goods cheap/Jai #28, Rudhirodgari #57; rains "
            "medium/Anand #48). Aashadh/Shravan -- rains normal. Bhadrapad -- excessive "
            "rains. Ashwin -- excessive disease. Kartik -- beneficial. "
            "Margsheersh/Paush/Magh/Phalgun -- grains cheap. Source: Gaur Ch 1."
        ),
        "note": (
            "Genuine truncation. NLM confirmed: Jyeshtha month was missing from the "
            "general Jupiter Samvatsar summary. Outcomes vary by specific Samvatsar: "
            "diseases (Subhanu #17); goods cheap (Jai #28, Rudhirodgari #57); rains "
            "medium (Anand #48). Inserted between Baisakh and Aashadh. All 12 Hindu "
            "months now complete. Approved by co-founder."
        ),
    },

    # ── 7. venus-lord -- Kartik completion ────────────────────────────────────
    {
        "rule_id": "gaur-ch1-samvatsar-venus-lord-natural-calamities",
        "result_old": (
            "Milk production is good. Rains are excessive. Ladies remain engaged in "
            "activities of all types. Young people want luxuries. All people live "
            "comfortably. Supremacy of females is established. EARTHQUAKE AND CALAMITY "
            "RISK throughout the year. MONTHLY PATTERN: Chaitra/Baisakh -- natural "
            "calamities. Jyeshtha -- disease. Aashadh -- rains. Shravan -- winds, grains "
            "become costly. Bhadrapad -- floods cause loss. Ashwin/Margsheersh -- "
            "beneficial. Paush/Magh -- medium. Phalgun -- trouble."
        ),
        "result_new": (
            "Milk production is good. Rains are excessive. Ladies remain engaged in "
            "activities of all types. Young people want luxuries. All people live "
            "comfortably. Supremacy of females is established. EARTHQUAKE AND CALAMITY "
            "RISK throughout the year. MONTHLY PATTERN: Chaitra/Baisakh -- natural "
            "calamities. Jyeshtha -- disease. Aashadh -- rains. Shravan -- winds, grains "
            "become costly. Bhadrapad -- floods cause loss. Kartik -- varies by Samvatsar "
            "(high grain prices/Taran #18, Raktaksha #58; goods cheap/Manmath #29; "
            "diseases/Rakshas #49). Ashwin/Margsheersh -- beneficial. Paush/Magh -- "
            "medium. Phalgun -- trouble. Source: Gaur Ch 1."
        ),
        "note": (
            "Genuine truncation. NLM confirmed: Kartik month was missing from the "
            "general Venus Samvatsar summary. Outcomes vary by specific Samvatsar: "
            "high grain prices (Taran #18, Raktaksha #58); goods cheap (Manmath #29); "
            "diseases (Rakshas #49). Inserted between Bhadrapad and Ashwin. All 12 "
            "Hindu months now complete. Approved by co-founder."
        ),
    },

    # ── 8. rahu-lord -- Ashwin completion + Kshaya note ───────────────────────
    {
        "rule_id": "gaur-ch1-samvatsar-rahu-lord-drought-north-floods-east",
        "result_old": (
            "Superficially: all people live happily and fruits and grains are good. "
            "But GEOGRAPHIC EFFECTS are severe and directional: DROUGHT in the North; "
            "FLOODS in the East; WAR in the West. MONTHLY PATTERN: Chaitra/Baisakh -- "
            "things costly. Jyeshtha/Aashadh -- rains less. Shravan/Bhadrapad -- rains "
            "more. Kartik -- drought, essential goods costly. Margsheersh/Paush/Magh/"
            "Phalgun -- goods costly; lives lost to riots."
        ),
        "result_new": (
            "Superficially: all people live happily and fruits and grains are good. "
            "But GEOGRAPHIC EFFECTS are severe and directional: DROUGHT in the North; "
            "FLOODS in the East; WAR in the West. MONTHLY PATTERN: Chaitra/Baisakh -- "
            "things costly. Jyeshtha/Aashadh -- rains less. Shravan/Bhadrapad -- rains "
            "more. Ashwin -- diseases and price instability (varies by Samvatsar: "
            "diseases + high prices/Vyaya #20; rulers weaken/Hamelambi #31; medium "
            "prices/Pingal #51; diseases/Kshaya #60). Kartik -- drought, essential "
            "goods costly. Margsheersh/Paush/Magh/Phalgun -- goods costly; lives lost "
            "to riots. Note on #60 Kshaya: holds dual classification -- Rahu as "
            "individual planetary lord AND Shiv-group membership (#41-60); both "
            "correct per Gaur Ch1. Source: Gaur Ch 1."
        ),
        "note": (
            "Genuine truncation + group ambiguity resolved. NLM confirmed: (1) Ashwin "
            "month was missing -- outcome = diseases and price instability (varies by "
            "Samvatsar). Inserted between Bhadrapad and Kartik. (2) #60 Kshaya holds "
            "dual classification: Rahu as its individual planetary lord + Shiv-group "
            "membership (Samvatsars #41-60) -- both simultaneously correct in Gaur Ch1. "
            "Original condition listing Kshaya under Rahu-lord Samvatsars is therefore "
            "accurate. All 12 Hindu months now complete. Approved by co-founder."
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
    print(f"Samvatsar batch ({len(ITEMS)} rules -- 5 false flags + 3 completions)")
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
            "validation.approved_by":   "co_founder_samvatsar_batch_may2026",
            "validation.approved_at":   now,
            "validation.approved_note": item["note"],
        }

        has_fix = item["result_old"] is not None
        if has_fix:
            if r.get("result") == item["result_old"]:
                update_set["result"] = item["result_new"]
                print(f"  result : ✅ matched -- will complete monthly pattern")
            else:
                print(f"  result : ⚠️  mismatch -- skipping result update")
                has_fix = False

        print(f"  note   : {item['note'][:100]}...")

        if args.apply:
            res = col.update_one(
                {"rule_id": rid},
                {"$set": update_set,
                 "$unset": {"validation.spot_check_reason": "",
                            "validation.flag_reason": ""}},
            )
            if res.modified_count:
                action = "COMPLETED + APPROVED" if has_fix else "APPROVED"
                print(f"  ✅ {action}\n")
                promoted += 1
            else:
                print(f"  ⚠️  No change written\n")
        else:
            action = "WOULD COMPLETE + APPROVE" if has_fix else "WOULD APPROVE"
            print(f"  🔍 {action}\n")
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
        print(f"Dry run: {promoted} / {len(ITEMS)} would be processed.")
        print("Re-run with --apply to write.")

    client.close()


if __name__ == "__main__":
    main()
