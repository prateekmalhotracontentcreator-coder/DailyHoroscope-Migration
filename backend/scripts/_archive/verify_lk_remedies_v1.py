#!/usr/bin/env python3
"""
verify_lk_remedies_v1.py — Post-Ingest Verification for LK Remedies

Runs all 8 health checks from LK_REMEDIES_TEST_PLAN.md §7
Reports PASS / FAIL with expected vs. actual values.

Usage:
  python3 backend/scripts/verify_lk_remedies_v1.py --mongo-url "$MONGO_URL"
  python3 backend/scripts/verify_lk_remedies_v1.py --mongo-url "$MONGO_URL" --db-name horoscope_db
"""
from __future__ import annotations

import argparse
import os
import sys

SCIENCE_ID = "jyotish_lk_remedies"
COLLECTION = "knowledge_rules"


def run(mongo_url: str, db_name: str) -> None:
    try:
        from pymongo import MongoClient
    except ImportError:
        print("ERROR: pymongo not installed")
        sys.exit(1)

    client = MongoClient(mongo_url)
    col    = client[db_name][COLLECTION]

    passes = 0
    fails  = 0

    def check(label: str, actual, expected, note: str = "") -> None:
        nonlocal passes, fails
        ok = actual == expected
        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"  {status}  {label}")
        print(f"          Expected : {expected}")
        print(f"          Actual   : {actual}")
        if note:
            print(f"          Note     : {note}")
        if ok:
            passes += 1
        else:
            fails += 1
        print()

    print(f"\n{'='*62}")
    print(f"  LK Remedies — Post-Ingest Verification")
    print(f"  Collection : {db_name}.{COLLECTION}")
    print(f"  Science ID : {SCIENCE_ID}")
    print(f"{'='*62}\n")

    # ── Check 1: Total count ─────────────────────────────────────────────────
    total = col.count_documents({"science_id": SCIENCE_ID})
    check("Total record count", total, 361)

    # ── Check 2: No decimal IDs (all must be integers) ───────────────────────
    decimal_ids = list(col.find(
        {"science_id": SCIENCE_ID, "id": {"$type": "double"}},
        {"id": 1, "_id": 0}
    ))
    check("No decimal IDs", len(decimal_ids), 0,
          note=f"Found: {[r['id'] for r in decimal_ids]}" if decimal_ids else "")

    # ── Check 3: No duplicate IDs ────────────────────────────────────────────
    pipeline = [
        {"$match": {"science_id": SCIENCE_ID}},
        {"$group": {"_id": "$id", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}},
    ]
    dupes = list(col.aggregate(pipeline))
    check("No duplicate IDs", len(dupes), 0,
          note=f"Duplicate IDs: {[d['_id'] for d in dupes]}" if dupes else "")

    # ── Check 4: Conflict gates tagged ──────────────────────────────────────
    conflict_count = col.count_documents({
        "science_id": SCIENCE_ID,
        "record_type": "conflict_gate",
    })
    check("Conflict gates tagged (IDs 616–625)", conflict_count, 10,
          note="All 10 must have record_type='conflict_gate'")

    # ── Check 4b: All conflict gates have ⚠️ SAFETY GATE ke_inference ───────
    conflict_records = list(col.find(
        {"science_id": SCIENCE_ID, "record_type": "conflict_gate"},
        {"id": 1, "ke_inference": 1, "_id": 0}
    ))
    bad_ke = [r["id"] for r in conflict_records
              if not r.get("ke_inference", "").startswith("⚠️ SAFETY GATE")]
    check("Conflict gate ke_inference format",
          len(bad_ke), 0,
          note=f"IDs missing ⚠️ SAFETY GATE prefix: {bad_ke}" if bad_ke else
               "All start with '⚠️ SAFETY GATE'")

    # ── Check 5: Supplementary records (656–668) ─────────────────────────────
    suppl_count = col.count_documents({
        "science_id": SCIENCE_ID,
        "id": {"$gte": 656, "$lte": 668},
    })
    check("Supplementary records (IDs 656–668)", suppl_count, 13)

    # ── Check 5b: All supplementary have parent_id ───────────────────────────
    suppl_no_pid = col.count_documents({
        "science_id": SCIENCE_ID,
        "id": {"$gte": 656, "$lte": 668},
        "parent_id": {"$exists": False},
    })
    check("Supplementary records all have parent_id", suppl_no_pid, 0,
          note="Every ID 656–668 must carry parent_id field")

    # ── Check 6: Destructive merge — ID 505 must be Directional ─────────────
    r505 = col.find_one(
        {"science_id": SCIENCE_ID, "id": 505},
        {"focus_area": 1, "_id": 0}
    )
    fa505 = r505.get("focus_area", "MISSING") if r505 else "RECORD MISSING"
    merge_ok = "Directional" in fa505 or "Geographical" in fa505
    print(f"  {'✅ PASS' if merge_ok else '❌ FAIL'}  Destructive merge — ID 505 focus_area")
    print(f"          Value    : '{fa505}'")
    print(f"          Rule     : Must contain 'Directional' or 'Geographical'")
    print(f"          {'OK — Version 2 (Directional Realignment) is live' if merge_ok else 'FAIL — Version 1 (Inheritance Lock) not overwritten!'}")
    print()
    if merge_ok:
        passes += 1
    else:
        fails += 1

    # ── Check 7: Building ban conflict gate (ID 622) ─────────────────────────
    r622 = col.find_one(
        {"science_id": SCIENCE_ID, "id": 622},
        {"record_type": 1, "ke_inference": 1, "_id": 0}
    )
    if r622:
        rt_ok  = r622.get("record_type") == "conflict_gate"
        ke_ok  = r622.get("ke_inference", "").startswith("⚠️ SAFETY GATE")
        gate_ok = rt_ok and ke_ok
        print(f"  {'✅ PASS' if gate_ok else '❌ FAIL'}  Building ban conflict gate (ID 622)")
        print(f"          record_type  : {r622.get('record_type')}  {'✅' if rt_ok else '❌ (expected conflict_gate)'}")
        print(f"          ke_inference : {r622.get('ke_inference', '')[:80]}...")
        print(f"          SAFETY GATE prefix: {'✅' if ke_ok else '❌'}")
        if gate_ok:
            passes += 1
        else:
            fails += 1
    else:
        print("  ❌ FAIL  Building ban conflict gate (ID 622) — RECORD MISSING")
        fails += 1
    print()

    # ── Check 8: Mercury Solitary H10 supplementary (ID 659) ────────────────
    r659 = col.find_one(
        {"science_id": SCIENCE_ID, "id": 659},
        {"primary_planet": 1, "house": 1, "parent_id": 1, "record_type": 1, "_id": 0}
    )
    if r659:
        p_ok  = r659.get("primary_planet") == "Mercury"
        h_ok  = r659.get("house") == 10
        pid_ok = r659.get("parent_id") == 382
        rt_ok  = r659.get("record_type") == "supplementary"
        all_ok = p_ok and h_ok and pid_ok and rt_ok
        print(f"  {'✅ PASS' if all_ok else '❌ FAIL'}  Mercury Solitary H10 supplementary (ID 659)")
        print(f"          primary_planet : {r659.get('primary_planet')}  {'✅' if p_ok else '❌ (expected Mercury)'}")
        print(f"          house          : {r659.get('house')}   {'✅' if h_ok else '❌ (expected 10)'}")
        print(f"          parent_id      : {r659.get('parent_id')}  {'✅' if pid_ok else '❌ (expected 382)'}")
        print(f"          record_type    : {r659.get('record_type')}  {'✅' if rt_ok else '❌ (expected supplementary)'}")
        if all_ok:
            passes += 1
        else:
            fails += 1
    else:
        print("  ❌ FAIL  Mercury Solitary H10 (ID 659) — RECORD MISSING")
        fails += 1
    print()

    # ── Check 9: Severity scale in bounds (1–5) ──────────────────────────────
    bad_sev = col.count_documents({
        "science_id": SCIENCE_ID,
        "severity_scale": {"$gt": 5},
    })
    check("Severity scale all ≤ 5", bad_sev, 0)

    # ── Check 10: All records have approval_status ───────────────────────────
    no_status = col.count_documents({
        "science_id": SCIENCE_ID,
        "approval_status": {"$exists": False},
    })
    check("All records have approval_status", no_status, 0)

    # ── Summary ──────────────────────────────────────────────────────────────
    total_checks = passes + fails
    print(f"{'='*62}")
    print(f"  Result: {passes}/{total_checks} checks passed")
    if fails == 0:
        print(f"  ✅ ALL CHECKS PASSED — LK Remedies collection is healthy")
    else:
        print(f"  ❌ {fails} check(s) failed — review output above")
    print(f"{'='*62}\n")

    client.close()
    sys.exit(0 if fails == 0 else 1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Post-ingest verification for LK Remedies (knowledge_rules collection)"
    )
    parser.add_argument("--mongo-url", default=os.environ.get("MONGO_URL", ""), metavar="URL")
    parser.add_argument("--db-name",   default=os.environ.get("DB_NAME", "horoscope_db"))
    args = parser.parse_args()
    if not args.mongo_url:
        print("[ERROR] --mongo-url required (or set MONGO_URL env var)", file=sys.stderr)
        sys.exit(1)
    run(args.mongo_url, args.db_name)


if __name__ == "__main__":
    main()
