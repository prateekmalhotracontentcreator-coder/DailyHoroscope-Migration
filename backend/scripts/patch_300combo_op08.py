#!/usr/bin/env python3
"""
patch_300combo_op08.py
--------------------------------------------------------------------
Closes OP-08: restore proper conditions for 18 remaining flagged rules
in the 300 Combinations batch, sourced directly from the Diagnostic files.

Two groups:

GROUP A -- Y264-Y274, Y292-Y294 (14 rules):
  conditions were None in source JSON -- Diagnostics contain the full
  condition descriptions, encoded here as structured dicts.
  Action: add conditions, remove tba:true, reset to pending_review.

  Additionally updates the source JSON files so the decode folder
  remains authoritative.

GROUP B -- Y130, Y131, Y133, Y134 (4 rules):
  conditions are complete and correct post-OP-02 patch.
  AI validator hallucinated truncation quotes not present in data.
  Action: patch to pending_human_review with validator_error:true.

Run:
    python3 backend/scripts/patch_300combo_op08.py --dry-run
    python3 backend/scripts/patch_300combo_op08.py \
      --mongo-url "mongodb+srv://..." --db-name horoscope_db
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DECODE_FOLDER = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredCombinations_CC_Decode"
)
BATCH_ID = "300-combinations-v1-20260601"

# ──────────────────────────────────────────────────────────────────────
# GROUP A: conditions derived from Diagnostic files
# ──────────────────────────────────────────────────────────────────────
GROUP_A_CONDITIONS: dict[str, dict[str, Any]] = {

    "combo-y264-001": {
        "type": "multi_trigger", "min_satisfied": 1,
        "description": "Galakarna Yoga -- 6th lord or malefic configurations causing ear disease",
        "triggers": [
            {"id": "t1", "type": "lord_in_house_with_malefic", "lord_of_house": 6, "house": 1,
             "description": "6th lord in Lagna with malefic"},
            {"id": "t2", "type": "malefic_in_house_with_malefic_aspect", "house": 6,
             "description": "Malefic in 6th house with another malefic aspecting the 6th lord"},
        ]
    },

    "combo-y265-001": {
        "type": "multi_trigger", "min_satisfied": 1,
        "description": "Vrana Yoga -- 6th lord/Mars configurations causing wounds and scars",
        "triggers": [
            {"id": "t1", "type": "lord_in_house", "lord_of_house": 6, "house": 1,
             "description": "6th lord in Lagna"},
            {"id": "t2", "type": "planet_in_house_with_malefic", "planet": "Mars", "house": 6,
             "description": "Mars in 6th with another malefic"},
            {"id": "t3", "type": "conjunction_in_house", "planets": ["Mars", "Saturn"], "house": 6,
             "description": "Mars and Saturn conjunct in 6th house"},
        ]
    },

    "combo-y266-001": {
        "type": "multi_condition", "min_conditions": 2, "all_required": False,
        "description": "Sisnavyadhi Yoga -- minimum 2 of 3 Venus/7th house afflictions required; all 3 increases severity",
        "conditions": [
            {"id": "c1", "type": "planet_afflicted_by_malefic", "planet": "Venus",
             "malefics": ["Saturn", "Mars"],
             "description": "Venus afflicted by Saturn or Mars (conjunction or aspect)"},
            {"id": "c2", "type": "lord_afflicted_by_malefic", "lord_of_house": 7,
             "malefics": ["Saturn", "Mars"],
             "description": "7th lord afflicted by Saturn or Mars"},
            {"id": "c3", "type": "house_under_malefic_affliction", "house": 7,
             "malefics": ["Saturn", "Mars"],
             "description": "7th house afflicted by Saturn or Mars"},
        ]
    },

    "combo-y267-001": {
        "type": "multi_condition", "min_conditions": 2, "all_required": False,
        "description": "Kalatrashanda Yoga -- minimum 2 of 3 required; wife's infertility or barrenness",
        "conditions": [
            {"id": "c1", "type": "lord_afflicted", "lord_of_house": 7,
             "description": "7th lord afflicted by malefic"},
            {"id": "c2", "type": "planet_afflicted", "planet": "Venus",
             "description": "Venus afflicted by malefic"},
            {"id": "c3", "type": "papakarthari_yoga", "house": 7,
             "description": "7th house hemmed between malefics (Papakarthari)"},
        ]
    },

    "combo-y268-001": {
        "type": "multi_trigger", "min_satisfied": 1,
        "description": "Kushtaroga Yoga (type 1) -- Saturn-Moon combinations causing leprosy or chronic skin disease",
        "triggers": [
            {"id": "t1", "type": "conjunction_in_house", "planets": ["Moon", "Saturn"], "house": 7,
             "description": "Moon and Saturn conjunct in 7th house"},
            {"id": "t2", "type": "multi_condition",
             "conditions": [
                 {"type": "moon_in_navamsa_of_planet", "navamsa_owner": "Saturn",
                  "description": "Moon in Saturn's navamsa sign"},
                 {"type": "planet_in_house", "planet_type": "malefic",
                  "description": "Malefic present with Moon"},
             ],
             "description": "Moon in Saturn's navamsa sign with malefic present"},
            {"id": "t3", "type": "multi_condition",
             "conditions": [
                 {"type": "planetary_position", "planet": "Saturn", "house": 1},
                 {"type": "planetary_position", "planet": "Moon", "house": 7},
             ],
             "description": "Saturn in Lagna and Moon in 7th house"},
        ]
    },

    "combo-y269-001": {
        "type": "multi_trigger", "min_satisfied": 1,
        "description": "Kushtaroga Yoga (type 2) -- 6th lord-Saturn or Moon-Mars combinations",
        "triggers": [
            {"id": "t1", "type": "multi_condition",
             "conditions": [
                 {"type": "lord_in_house", "lord_of_house": 6, "house": 1},
                 {"type": "planetary_position", "planet": "Saturn", "house": 1},
             ],
             "description": "6th lord and Saturn both in Lagna"},
            {"id": "t2", "type": "conjunction_in_house", "planets": ["Moon", "Mars"], "house": 8,
             "description": "Moon and Mars conjunct in 8th house"},
        ]
    },

    "combo-y270-001": {
        "type": "multi_trigger", "min_satisfied": 1,
        "gate_note": "t3 is supporting indicator only -- cannot activate independently; must co-occur with t1 or t2",
        "description": "Kshaya Roga Yoga -- Moon affliction causing consumption or wasting disease",
        "triggers": [
            {"id": "t1", "type": "planet_in_dusthana_with_malefic", "planet": "Moon",
             "dusthana_houses": [6, 8, 12],
             "description": "Moon in dusthana (6th, 8th, or 12th) with malefic"},
            {"id": "t2", "type": "conjunction_in_house", "planets": ["Saturn", "Moon"], "house": 8,
             "description": "Saturn and Moon conjunct in 8th house"},
            {"id": "t3", "type": "planetary_position", "planet": "Saturn", "house": 4,
             "qualifier": "supporting_only",
             "engine_note": "t3 alone is insufficient -- must co-occur with t1 or t2",
             "description": "Saturn in 4th house (supporting indicator only)"},
        ]
    },

    "combo-y271-001": {
        "type": "multi_trigger", "min_satisfied": 1, "timing_bias": "dasa_dependent",
        "description": "Bandhana Yoga -- imprisonment or captivity configurations",
        "triggers": [
            {"id": "t1", "type": "multi_condition",
             "conditions": [
                 {"type": "lord_in_house", "lord_of_house": 12, "house": 1},
                 {"type": "planet_in_house", "planet_type": "malefic", "house": 12},
             ],
             "description": "12th lord in Lagna with malefic in 12th house"},
            {"id": "t2", "type": "multi_condition",
             "conditions": [
                 {"type": "planetary_position", "planet": "Sun", "houses": [2, 12]},
                 {"type": "planetary_position", "planet": "Moon", "houses": [2, 12]},
                 {"type": "planetary_position", "planet": "Saturn", "houses": [2, 12]},
             ],
             "description": "Sun, Moon, and Saturn all in 2nd or 12th house"},
        ]
    },

    "combo-y272-001": {
        "type": "multi_trigger", "min_satisfied": 1,
        "description": "Karascheda Yoga -- Mars-Saturn configurations causing limb loss or amputation",
        "triggers": [
            {"id": "t1", "type": "multi_condition",
             "conditions": [
                 {"type": "planetary_position", "planet": "Mars", "houses": [2, 8]},
                 {"type": "planet_aspects_planet", "aspecting_planet": "Saturn", "aspected_planet": "Mars"},
             ],
             "description": "Mars in 2nd or 8th with Saturn aspecting Mars"},
            {"id": "t2", "type": "multi_condition",
             "conditions": [
                 {"type": "planetary_position", "planet": "Mars", "house": 8},
                 {"type": "lord_in_house", "lord_of_house": 8, "house": 8},
             ],
             "description": "Mars and 8th lord both in 8th house"},
        ]
    },

    "combo-y273-001": {
        "type": "multi_trigger", "min_satisfied": 1,
        "extreme_outcome_note": "Violent death yoga -- requires strong arishta confirmation; low confidence unless multiple indicators present",
        "description": "Sirachcheda Yoga -- Mars-8th lord configurations associated with decapitation or execution",
        "triggers": [
            {"id": "t1", "type": "multi_condition",
             "conditions": [
                 {"type": "multi_variant", "min_satisfied": 1, "variants": [
                     {"type": "lord_and_planet_in_house", "lord_of_house": 8, "planet": "Mars", "house": 1},
                     {"type": "lord_and_planet_in_house", "lord_of_house": 8, "planet": "Mars", "house": 8},
                 ]},
                 {"type": "strength_modifier", "planet": "lagna_lord", "qualifier": "weak"},
             ],
             "description": "8th lord and Mars in Lagna or 8th, with weak Lagna lord"},
            {"id": "t2", "type": "multi_condition",
             "conditions": [
                 {"type": "planet_in_house", "planet_type": "malefic", "house": 8},
                 {"type": "planet_aspected_by_planet_type", "planet": "8th_lord", "aspecting_type": "malefic"},
             ],
             "description": "Malefic in 8th house with another malefic aspecting the 8th lord"},
        ]
    },

    "combo-y274-001": {
        "type": "multi_trigger", "min_satisfied": 1,
        "description": "Durmarana Yoga -- violent or unnatural death configurations",
        "triggers": [
            {"id": "t1", "type": "multi_condition",
             "conditions": [
                 {"type": "lord_afflicted", "lord_of_house": 8},
                 {"type": "multiple_malefics_prominent",
                  "description": "Multiple malefics prominent in chart"},
             ],
             "description": "8th lord afflicted with multiple malefics prominent"},
            {"id": "t2", "type": "multi_condition",
             "conditions": [
                 {"type": "planetary_position", "planet": "Moon", "house": 8},
                 {"type": "no_benefic_aspect_on_house", "house": 8},
             ],
             "description": "Moon in 8th house without benefic aspect"},
            {"id": "t3", "type": "drekkana_navamsa_check",
             "anchor_planet": "Saturn",
             "derive": "drekkana_lord",
             "terminal_check": "navamsa_in_martian_sign",
             "martian_signs": ["Aries", "Scorpio"],
             "qualifier": "medium_complexity",
             "engine_dependency": "D3_D9_computation_required",
             "description": "Saturn's D3 (drekkana) lord must be in Aries or Scorpio navamsa (D9)"},
        ]
    },

    "combo-y292-001": {
        "type": "multi_condition", "all_required": True,
        "description": "Matibhramana Yoga (292) -- Saturn in Lagna with Mars in trikona causing mental derangement",
        "conditions": [
            {"id": "c1", "type": "planetary_position", "planet": "Saturn", "house": 1,
             "description": "Saturn in Lagna (1st house)"},
            {"id": "c2", "type": "planetary_position", "planet": "Mars", "houses": [5, 7, 9],
             "description": "Mars in 5th, 7th, or 9th house from Lagna"},
        ]
    },

    "combo-y293-001": {
        "type": "multi_condition", "all_required": True,
        "description": "Matibhramana Yoga (293) -- Saturn and waning Moon in 12th causing mental affliction",
        "conditions": [
            {"id": "c1", "type": "conjunction_in_house", "planets": ["Saturn", "Moon"], "house": 12,
             "description": "Saturn and Moon conjunct in 12th house"},
            {"id": "c2", "type": "moon_phase", "phase": "waning",
             "description": "Moon must be waning (Krishna paksha -- after Purnima, before Amavasya)"},
        ]
    },

    "combo-y294-001": {
        "type": "multi_condition", "all_required": True, "confidence": "medium_low",
        "day_night_modifier": True,
        "engine_note": "Day chart + Saturn afflictor → epilepsy; night chart + Rahu afflictor → insanity; Mars afflictor → insanity by day / epilepsy by night",
        "description": "Matibhramana Yoga (294) -- Moon and Mercury in kendra under malefic affliction",
        "conditions": [
            {"id": "c1", "type": "multi_condition",
             "conditions": [
                 {"type": "planetary_position", "planet": "Moon",
                  "house_type": "kendra", "houses": [1, 4, 7, 10]},
                 {"type": "planetary_position", "planet": "Mercury",
                  "house_type": "kendra", "houses": [1, 4, 7, 10]},
             ],
             "description": "Moon and Mercury both in kendra houses (1st, 4th, 7th, or 10th)"},
            {"id": "c2", "type": "multi_variant", "min_satisfied": 1,
             "variants": [
                 {"type": "conjunction_with_malefic", "planet": "Moon",
                  "description": "Moon conjunct malefic"},
                 {"type": "planet_aspected_by_planet_type", "planet": "Moon",
                  "aspecting_type": "malefic",
                  "description": "Moon aspected by malefic"},
                 {"type": "conjunction_with_malefic", "planet": "Mercury",
                  "description": "Mercury conjunct malefic"},
                 {"type": "planet_aspected_by_planet_type", "planet": "Mercury",
                  "aspecting_type": "malefic",
                  "description": "Mercury aspected by malefic"},
             ],
             "description": "Moon or Mercury afflicted by malefic (conjunction or aspect)"},
        ]
    },
}

# ──────────────────────────────────────────────────────────────────────
# GROUP B: Bucket B validator errors -- patch to PHR
# ──────────────────────────────────────────────────────────────────────
GROUP_B_IDS = [
    "combo-y130-001",  # Vaiseshikamsa condition: complete in source, validator hallucinated quote
    "combo-y131-001",  # Navamsa chain: correctly documented, validator flagged algorithm as truncation
    "combo-y133-001",  # Kalabala: engine dependency noted in Diagnostic; interpretation complete
    "combo-y134-001",  # Dispositor-in-Lagna: condition complete; interpretation complete
]

# ──────────────────────────────────────────────────────────────────────
# Source JSON file map (rule_id prefix → filename)
# ──────────────────────────────────────────────────────────────────────
SOURCE_FILE_MAP = {
    "combo-y264-001": "Combo_Y264-287_Rules.json",
    "combo-y265-001": "Combo_Y264-287_Rules.json",
    "combo-y266-001": "Combo_Y264-287_Rules.json",
    "combo-y267-001": "Combo_Y264-287_Rules.json",
    "combo-y268-001": "Combo_Y264-287_Rules.json",
    "combo-y269-001": "Combo_Y264-287_Rules.json",
    "combo-y270-001": "Combo_Y264-287_Rules.json",
    "combo-y271-001": "Combo_Y264-287_Rules.json",
    "combo-y272-001": "Combo_Y264-287_Rules.json",
    "combo-y273-001": "Combo_Y264-287_Rules.json",
    "combo-y274-001": "Combo_Y264-287_Rules.json",
    "combo-y292-001": "Combo_Y288-300_Rules.json",
    "combo-y293-001": "Combo_Y288-300_Rules.json",
    "combo-y294-001": "Combo_Y288-300_Rules.json",
}


def update_source_json(filename: str, conditions_by_id: dict[str, dict], dry: bool) -> int:
    """Write conditions back to source JSON file. Returns count updated."""
    fp = DECODE_FOLDER / filename
    if not fp.exists():
        print(f"  [warn] source file not found: {filename}")
        return 0
    data = json.loads(fp.read_text(encoding="utf-8"))
    rules = data.get("rules", data) if isinstance(data, dict) else data
    updated = 0
    for rule in rules:
        rid = rule.get("rule_id", "")
        if rid in conditions_by_id:
            rule["conditions"] = conditions_by_id[rid]
            updated += 1
    if not dry:
        if isinstance(data, dict):
            data["rules"] = rules
            fp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            fp.write_text(json.dumps(rules, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  Source JSON updated: {filename} ({updated} rules)")
    else:
        print(f"  DRY: would update {filename} ({updated} rules)")
    return updated


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Patch 300 Combinations OP-08.")
    p.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    p.add_argument("--db-name", default="horoscope_db")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    now = datetime.now(timezone.utc).isoformat()
    dry = args.dry_run

    print("\n" + "=" * 65)
    print("patch_300combo_op08.py -- OP-08 closure")
    print(f"Mode:  {'DRY RUN' if dry else 'LIVE'}")
    print("=" * 65)

    # ─── Update source JSON files ───
    print("\n── Updating source JSON files ──")
    # Group by file
    files_to_update: dict[str, dict[str, dict]] = {}
    for rid, cond in GROUP_A_CONDITIONS.items():
        fname = SOURCE_FILE_MAP.get(rid, "")
        if fname:
            files_to_update.setdefault(fname, {})[rid] = cond
    total_source_updated = 0
    for fname, conds in files_to_update.items():
        total_source_updated += update_source_json(fname, conds, dry)

    if not dry:
        if not args.mongo_url:
            print("ERROR: --mongo-url required", file=sys.stderr)
            sys.exit(1)
        from pymongo import MongoClient
        client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=15000)
        db = client[args.db_name]

    # ─── GROUP A: Add conditions + reset to pending_review ───
    print(f"\n── GROUP A: {len(GROUP_A_CONDITIONS)} rules -- add conditions, clear tba, reset to pending_review ──")
    group_a_patched = 0
    for rid, cond in sorted(GROUP_A_CONDITIONS.items()):
        update: dict[str, Any] = {
            "condition":        cond,
            "approval_status":  "pending_review",
            "patched_at":       now,
            "patch_note":       "op08: conditions added from Diagnostic file; tba cleared",
        }
        # Remove tba fields
        unset = {"tba": "", "tba_note": ""}
        if dry:
            print(f"  DRY {rid}: condition.type={cond.get('type')} → pending_review")
            group_a_patched += 1
        else:
            try:
                res = db["interpretation_rules"].update_one(
                    {"rule_id": rid, "ingest_batch_id": BATCH_ID},
                    {"$set": update, "$unset": unset},
                )
                if res.matched_count:
                    group_a_patched += 1
                else:
                    print(f"  [warn] {rid} not found in MongoDB")
            except Exception as e:
                print(f"  [error] {rid}: {e}")
    print(f"  Patched: {group_a_patched}/{len(GROUP_A_CONDITIONS)}")

    # ─── GROUP B: Validator errors → PHR ───
    print(f"\n── GROUP B: {len(GROUP_B_IDS)} rules -- validator_error:true → pending_human_review ──")
    group_b_patched = 0
    for rid in GROUP_B_IDS:
        update = {
            "approval_status":     "pending_human_review",
            "validator_error":     True,
            "validator_error_note": (
                "Bucket B triage: AI validator hallucinated or misattributed truncation "
                "quotes not present in the actual interpretation text. Conditions are "
                "complete and correct per Y129-143 Diagnostic (all gates PASS). "
                "Engine dependency noted (Vaiseshikamsa/Kalabala) -- rules marked "
                "engine_dependency_required for partial evaluation until Shodasavarga "
                "and Kalabala are implemented."
            ),
            "engine_dependency_required": True,
            "patched_at": now,
        }
        if dry:
            print(f"  DRY {rid}: validator_error=True → pending_human_review")
            group_b_patched += 1
        else:
            try:
                res = db["interpretation_rules"].update_one(
                    {"rule_id": rid, "ingest_batch_id": BATCH_ID},
                    {"$set": update},
                )
                if res.matched_count:
                    group_b_patched += 1
            except Exception as e:
                print(f"  [error] {rid}: {e}")
    print(f"  Patched: {group_b_patched}/{len(GROUP_B_IDS)}")

    # ─── Final status check ───
    if not dry:
        from collections import Counter
        rules = list(db["interpretation_rules"].find(
            {"ingest_batch_id": BATCH_ID}, {"_id": 0, "approval_status": 1}
        ))
        statuses = Counter(r["approval_status"] for r in rules)
        print(f"\n── Post-patch status (before re-validation) ──")
        for s, c in sorted(statuses.items(), key=lambda x: -x[1]):
            print(f"  {s}: {c}")
        print(f"  TOTAL: {len(rules)}")
        client.close()

    print(f"\n{'=' * 65}")
    print("SUMMARY")
    print(f"  Source JSON files updated:  {total_source_updated} rules across 2 files")
    print(f"  Group A (conditions added): {group_a_patched}/{len(GROUP_A_CONDITIONS)}")
    print(f"  Group B (validator error):  {group_b_patched}/{len(GROUP_B_IDS)}")
    if dry:
        print("\n[DRY RUN] No writes made.")
    else:
        print(f"\nNEXT:")
        print(f"  Run validate_rules.py on the {len(GROUP_A_CONDITIONS)} pending_review rules:")
        print(f"  ANTHROPIC_API_KEY='sk-ant-...' python3 backend/scripts/validate_rules.py \\")
        print(f"    --batch-id {BATCH_ID} --mongo-url \"$MONGO_URL\" --db-name {args.db_name}")
    print("=" * 65)


if __name__ == "__main__":
    main()
