#!/usr/bin/env python3
"""
Pull validation results for lalkitab-ch27-v1-20260427:
- 1 contradiction pair
- 7 flagged rules with flag reasons
- PHR count by group
"""
import os
from pymongo import MongoClient

BATCH_ID = "lalkitab-ch27-v1-20260427"
DB_NAME  = "horoscope_db"

def main():
    mongo_url = os.environ.get("MONGO_URL", "").strip()
    if not mongo_url:
        mongo_url = input("Paste MongoDB Atlas URL: ").strip()

    coll = MongoClient(mongo_url)[DB_NAME]["interpretation_rules"]

    # ── Contradictions ──
    print("\n=== CONTRADICTION PAIR(S) ===")
    contras = list(coll.find(
        {"source.batch_id": BATCH_ID, "approval_status": "flagged",
         "validation.flag_reason": {"$regex": "contradiction", "$options": "i"}},
        {"rule_id": 1, "condition": 1, "validation": 1, "_id": 0}
    ))
    if contras:
        for r in contras:
            print(f"  {r['rule_id']}")
            print(f"    type    : {r.get('condition', {}).get('type')} / {r.get('condition', {}).get('sub_type', '—')}")
            print(f"    reason  : {r.get('validation', {}).get('flag_reason', '')}")
            print()
    else:
        # Contradictions may be tagged differently — pull all flagged
        print("  (no 'contradiction' keyword in flag_reason — showing all flagged below)\n")

    # ── All flagged ──
    print("=== FLAGGED RULES (7) ===")
    flagged = list(coll.find(
        {"source.batch_id": BATCH_ID, "approval_status": "flagged"},
        {"rule_id": 1, "condition": 1, "interpretation": 1, "validation": 1, "_id": 0}
    ))
    for r in flagged:
        cond = r.get("condition", {})
        val  = r.get("validation", {})
        print(f"  {r['rule_id']}")
        print(f"    group   : {cond.get('type')} / {cond.get('sub_type', '—')}")
        print(f"    planet  : {cond.get('planet', cond.get('planets_involved', '—'))}")
        print(f"    verdict : {val.get('verdict', '—')}")
        print(f"    reason  : {val.get('flag_reason', '—')[:180]}")
        print(f"    summary : {r.get('interpretation', {}).get('summary', '')[:100]}")
        print()

    # ── PHR breakdown by group ──
    print("=== PHR RULES BY GROUP ===")
    phr = list(coll.find(
        {"source.batch_id": BATCH_ID, "approval_status": "pending_human_review"},
        {"rule_id": 1, "_id": 0}
    ))
    groups: dict[str, int] = {}
    for r in phr:
        parts = r["rule_id"].split("-")
        grp = parts[3] if len(parts) > 3 else "unknown"
        groups[grp] = groups.get(grp, 0) + 1
    for g, n in sorted(groups.items(), key=lambda x: -x[1]):
        print(f"  {g:<20} {n} rules")
    print(f"\n  Total PHR: {len(phr)}")

if __name__ == "__main__":
    main()
