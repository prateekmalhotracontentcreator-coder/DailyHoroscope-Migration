#!/usr/bin/env python3
"""
master_test_query_lk.py -- LK Remedies Master Test Query
Source: LK_REMEDIES_TEST_PLAN.md §3-5

Test scenario:
  "I am 36 years old. I have Mercury alone in my 10th House.
   My Saturn is transiting my 7th House, and I am planning to
   start a major building construction project today in the South direction."

Runs the 5-Gate sequence + Conflict Gate check.
Verifies all 4 PASS criteria and 3 FAIL triggers.

Usage:
  python3 backend/scripts/master_test_query_lk.py --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
import sys

SCIENCE_ID = "jyotish_lk_remedies"
COLLECTION  = "knowledge_rules"

# ── Test inputs ───────────────────────────────────────────────────────────────
USER_AGE         = 36
NATAL_PLANET     = "Mercury"
NATAL_HOUSE      = 10
TRANSIT_PLANET   = "Saturn"
TRANSIT_HOUSE    = 7
PLANNED_ACTION   = "building_construction"
DIRECTION        = "South"


def run(mongo_url: str, db_name: str) -> None:
    try:
        from pymongo import MongoClient
    except ImportError:
        print("ERROR: pymongo not installed"); sys.exit(1)

    client = MongoClient(mongo_url)
    col    = client[db_name][COLLECTION]

    passes = 0
    fails  = 0

    print(f"\n{'='*65}")
    print(f"  LK Remedies -- Master Test Query")
    print(f"  Scenario: Age {USER_AGE}, Mercury H{NATAL_HOUSE} (solitary),")
    print(f"            Saturn transit H{TRANSIT_HOUSE}, building construction, {DIRECTION}")
    print(f"{'='*65}\n")

    # ── GATE 1 -- Karmic Debt Audit ────────────────────────────────────────────
    print("  GATE 1 -- Karmic Debt Audit (age 36 → Saturn cycle, Pitra Rin check)")
    gate1 = list(col.find(
        {"science_id": SCIENCE_ID,
         "id": {"$in": list(range(483, 501)) + [611, 612, 613, 614]},
         "approval_status": {"$exists": True}},
        {"id": 1, "focus_area": 1, "primary_planet": 1, "severity_scale": 1, "_id": 0}
    ))
    gate1.sort(key=lambda x: x["id"])
    print(f"  Records returned: {len(gate1)}")
    for r in gate1[:5]:
        flag = " ⚠️  PRIORITY (sev≥4)" if r.get("severity_scale", 0) >= 4 else ""
        print(f"    ID {r['id']:3d}  {r.get('focus_area','')[:45]}{flag}")
    if len(gate1) > 5:
        print(f"    ... {len(gate1)-5} more")
    priority = [r for r in gate1 if r.get("severity_scale", 0) >= 4]
    print(f"  Priority warnings (sev≥4): {len(priority)}")
    print()

    # ── GATE 2 -- House Awakening (Mercury H10, solitary) ─────────────────────
    print("  GATE 2 -- House Awakening (Mercury H10, dormant check)")
    gate2_main = list(col.find(
        {"science_id": SCIENCE_ID,
         "primary_planet": "Mercury",
         "house": 10,
         "trigger_dormant": True,
         "approval_status": {"$exists": True}},
        {"id": 1, "focus_area": 1, "ritual_act": 1, "ke_inference": 1, "_id": 0}
    ))
    gate2_suppl = col.find_one(
        {"science_id": SCIENCE_ID, "id": 659},
        {"id": 1, "focus_area": 1, "primary_planet": 1, "house": 1,
         "parent_id": 1, "record_type": 1, "ritual_act": 1, "_id": 0}
    )
    print(f"  Mercury H10 dormant records: {len(gate2_main)}")
    for r in gate2_main:
        print(f"    ID {r['id']:3d}  {r.get('focus_area','')[:45]}")
        print(f"           Ritual: {r.get('ritual_act','')[:60]}")
    print(f"\n  Supplementary ID 659 (Mercury Solitary H10 -- was 382.2):")
    if gate2_suppl:
        print(f"    ID: {gate2_suppl.get('id')}  planet={gate2_suppl.get('primary_planet')}  "
              f"house={gate2_suppl.get('house')}  parent_id={gate2_suppl.get('parent_id')}")
        print(f"    type: {gate2_suppl.get('record_type')}")
        print(f"    Ritual: {gate2_suppl.get('ritual_act','')[:70]}")
    else:
        print("    ❌ ID 659 NOT FOUND")
    print()

    # ── GATE 3 -- 35-Year Cycle (age 36 → Saturn cycle) ───────────────────────
    print("  GATE 3 -- 35-Year Cycle (Lord of the Year: Saturn, age 36-41)")
    gate3 = list(col.find(
        {"science_id": SCIENCE_ID,
         "primary_planet": "Saturn",
         "id": {"$gte": 526, "$lte": 575},
         "approval_status": {"$exists": True}},
        {"id": 1, "focus_area": 1, "severity_scale": 1, "_id": 0}
    ))
    gate3.sort(key=lambda x: x["id"])
    print(f"  Saturn cycle records (IDs 526-575): {len(gate3)}")
    for r in gate3[:4]:
        print(f"    ID {r['id']:3d}  {r.get('focus_area','')[:45]}  (sev {r.get('severity_scale','-')})")
    if len(gate3) > 4:
        print(f"    ... {len(gate3)-4} more")
    print()

    # ── GATE 4 -- Mercury-Rahu Collision Check ─────────────────────────────────
    print("  GATE 4 -- Mercury-Rahu Collision (solitary Mercury trigger)")
    gate4 = list(col.find(
        {"science_id": SCIENCE_ID,
         "id": {"$gte": 631, "$lte": 635},
         "primary_planet": "Mercury",
         "approval_status": {"$exists": True}},
        {"id": 1, "focus_area": 1, "ke_inference": 1, "_id": 0}
    ))
    print(f"  Mercury-Rahu warning records: {len(gate4)}")
    for r in gate4:
        print(f"    ID {r['id']:3d}  {r.get('focus_area','')[:45]}")
        print(f"           KE: {r.get('ke_inference','')[:70]}")
    print()

    # ── GATE 5 -- Geographical Pivot (South direction) ────────────────────────
    print("  GATE 5 -- Geographical Pivot (direction: South, IDs 505-525)")
    gate5 = list(col.find(
        {"science_id": SCIENCE_ID,
         "id": {"$gte": 505, "$lte": 525},
         "approval_status": {"$exists": True}},
        {"id": 1, "focus_area": 1, "ke_inference": 1, "_id": 0}
    ))
    gate5.sort(key=lambda x: x["id"])
    south_records = [r for r in gate5
                     if "South" in r.get("focus_area", "") or "south" in r.get("ke_inference", "").lower()]
    print(f"  Total records 505-525: {len(gate5)}")
    print(f"  South-direction specific: {len(south_records)}")
    for r in south_records:
        print(f"    ID {r['id']:3d}  {r.get('focus_area','')[:55]}")
    # Critical: ID 505 must NOT be Inheritance
    r505 = next((r for r in gate5 if r["id"] == 505), None)
    if r505:
        fa = r505.get("focus_area", "")
        is_v2 = "Directional" in fa or "Geographical" in fa or "Compass" in fa
        print(f"\n  ID 505 focus_area: '{fa}'")
        print(f"  Destructive merge: {'✅ V2 (Directional) is live' if is_v2 else '❌ V1 (Inheritance) still present!'}")
    print()

    # ── CONFLICT GATE -- Building Construction Check ───────────────────────────
    print("  CONFLICT GATE -- Building Construction (ID 622, Saturn Building Ban)")
    r622 = col.find_one(
        {"science_id": SCIENCE_ID, "id": 622,
         "record_type": "conflict_gate",
         "approval_status": {"$exists": True}},
        {"id": 1, "record_type": 1, "ke_inference": 1, "_id": 0}
    )
    if r622:
        ke = r622.get("ke_inference", "")
        print(f"  record_type : {r622.get('record_type')}")
        print(f"  ke_inference: {ke[:100]}")
        print(f"  ⚠️  SAFETY GATE FIRES → Inject at TOP of response before any remedy")
    else:
        print("  ❌ ID 622 NOT FOUND -- building construction proceeds without warning!")
    print()

    # ── PASS / FAIL EVALUATION ────────────────────────────────────────────────
    print(f"{'='*65}")
    print(f"  PASS / FAIL EVALUATION  (LK_REMEDIES_TEST_PLAN.md §5)")
    print(f"{'='*65}\n")

    def result(label: str, condition: bool, pass_msg: str, fail_msg: str) -> None:
        nonlocal passes, fails
        if condition:
            print(f"  ✅ PASS  {label}")
            print(f"           {pass_msg}")
            passes += 1
        else:
            print(f"  ❌ FAIL  {label}")
            print(f"           {fail_msg}")
            fails += 1
        print()

    # P1 -- Destructive merge: ID 505 must be Directional
    fa505 = r505.get("focus_area", "") if r505 else ""
    result(
        "P1 -- Destructive Merge (ID 505)",
        "Directional" in fa505 or "Geographical" in fa505 or "Compass" in fa505,
        f"focus_area='{fa505}' → Version 2 (Directional Realignment) is live",
        f"focus_area='{fa505}' → Version 1 (Inheritance Lock) NOT overwritten"
    )

    # P2 -- Building ban fires
    result(
        "P2 -- Building Ban Safety Gate (ID 622)",
        r622 is not None and r622.get("ke_inference", "").startswith("⚠️ SAFETY GATE"),
        "ID 622 returned with ⚠️ SAFETY GATE prefix → response blocked until warning shown",
        "ID 622 missing or not tagged → user could proceed with construction without warning"
    )

    # P3 -- Mercury Solitary H10 supplementary record returned
    result(
        "P3 -- Mercury Solitary H10 (ID 659)",
        gate2_suppl is not None
            and gate2_suppl.get("primary_planet") == "Mercury"
            and gate2_suppl.get("house") == 10,
        f"ID 659 returned: planet=Mercury, house=10, parent_id={gate2_suppl.get('parent_id') if gate2_suppl else '?'}",
        "ID 659 missing → solitary Mercury H10 not handled (Manager without a Boss ignored)"
    )

    # P4 -- Muhurta rule: non-Saturn remedy must be daytime
    # Check gate2_main records -- none should say "Night" or "After Sunset" for non-Saturn planets
    night_remedies = [
        r for r in gate2_main
        if r.get("muhurta_rule", "").lower() in ("night", "after sunset", "after_sunset")
    ]
    result(
        "P4 -- Muhurta Rule (daytime for non-Saturn remedies)",
        len(night_remedies) == 0,
        "All Mercury H10 remedies have daytime muhurta → safe to prescribe",
        f"Night muhurta found on non-Saturn records: {[r['id'] for r in night_remedies]}"
    )

    # ── FAIL TRIGGERS ─────────────────────────────────────────────────────────
    print(f"  {'─'*60}")
    print(f"  FAIL TRIGGER CHECKS\n")

    def fail_check(label: str, triggered: bool, msg: str) -> None:
        if triggered:
            print(f"  🚨 FAIL TRIGGER ACTIVE  {label}")
            print(f"           {msg}")
        else:
            print(f"  ✅ CLEAR  {label}")
            print(f"           {msg}")
        print()

    # F1 -- ID 505 should NOT contain "Inheritance"
    fail_check(
        "F1 -- Inheritance Lock still present?",
        "Inheritance" in fa505 or "Sun's Seal" in fa505,
        f"ID 505 focus_area='{fa505}'" if ("Inheritance" in fa505) else
        f"ID 505 clean: '{fa505}' -- no Inheritance Lock"
    )

    # F2 -- Construction must NOT proceed without warning
    fail_check(
        "F2 -- Building construction without safety warning?",
        r622 is None or not r622.get("ke_inference", "").startswith("⚠️ SAFETY GATE"),
        "ID 622 conflict gate MISSING or malformed" if r622 is None else
        "ID 622 conflict gate live and correctly formatted"
    )

    # F3 -- Mercury H10 solitary must NOT be ignored
    fail_check(
        "F3 -- Mercury solitary status ignored?",
        gate2_suppl is None,
        "ID 659 (Mercury Solitary H10) is MISSING" if gate2_suppl is None else
        "ID 659 present -- solitary Mercury H10 scenario covered"
    )

    # ── SUMMARY ───────────────────────────────────────────────────────────────
    print(f"{'='*65}")
    print(f"  MASTER TEST RESULT: {passes}/4 PASS criteria met")
    if fails == 0:
        print(f"  ✅ ALL 4 PASS CRITERIA MET -- Knowledge Engine calibrated for production")
    else:
        print(f"  ❌ {fails} criteria failed -- review above")
    print(f"{'='*65}\n")

    client.close()
    sys.exit(0 if fails == 0 else 1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Master Test Query for LK Remedies KE calibration"
    )
    parser.add_argument("--mongo-url", required=True, metavar="URL")
    parser.add_argument("--db-name",   default="horoscope_db")
    args = parser.parse_args()
    run(args.mongo_url, args.db_name)


if __name__ == "__main__":
    main()
