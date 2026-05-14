#!/usr/bin/env python3
"""
Find and re-validate the 1 stuck pending_review rule in lalkitab-ch20 batch.
If Claude call fails, force it to pending_human_review for manual review.
"""
import os, sys
from datetime import datetime, timezone
from pymongo import MongoClient

BATCH_ID = "lalkitab-ch20-v1-20260427"
DB_NAME  = "horoscope_db"

def main():
    mongo_url = os.environ.get("MONGO_URL", "").strip()
    if not mongo_url:
        mongo_url = input("Paste MongoDB Atlas URL: ").strip()

    client = MongoClient(mongo_url)
    coll   = client[DB_NAME]["interpretation_rules"]

    stuck = list(coll.find(
        {"source.batch_id": BATCH_ID, "approval_status": "pending_review"},
        {"rule_id": 1, "condition": 1, "interpretation": 1, "_id": 0}
    ))

    if not stuck:
        print("No stuck rules found — batch is fully validated.")
        return

    print(f"Found {len(stuck)} stuck rule(s):")
    for r in stuck:
        print(f"  rule_id : {r['rule_id']}")
        print(f"  cond    : {r.get('condition', {}).get('type')} / {r.get('condition', {}).get('sub_type','—')}")
        print(f"  summary : {r.get('interpretation', {}).get('summary', '')[:80]}")
        print()

    # Try Claude validation first
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if api_key:
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from knowledge_validator import RuleValidator
        validator = RuleValidator(model="claude-haiku-4-5")
        for r in stuck:
            try:
                results = validator.validate_batch([r])
                res = results[0] if results else None
                verdict = (res or {}).get("verdict", "spot_check")
                reason  = (res or {}).get("reason", "single_rule_retry")
                status_map = {"approve": "auto_approved", "spot_check": "pending_human_review", "flag": "flagged"}
                new_status = status_map.get(verdict, "pending_human_review")
                coll.update_one(
                    {"rule_id": r["rule_id"]},
                    {"$set": {
                        "approval_status": new_status,
                        "validation": {
                            "verdict": verdict,
                            "flag_reason": reason,
                            "validated_by": "claude-haiku-4-5",
                            "validated_at": datetime.now(timezone.utc).isoformat(),
                        }
                    }}
                )
                print(f"✅ {r['rule_id']} → {new_status} (verdict: {verdict})")
            except Exception as e:
                print(f"Claude call failed: {e}. Forcing pending_human_review.")
                _force_phr(coll, r["rule_id"])
    else:
        print("No ANTHROPIC_API_KEY — forcing pending_human_review for manual review.")
        for r in stuck:
            _force_phr(coll, r["rule_id"])

def _force_phr(coll, rule_id):
    coll.update_one(
        {"rule_id": rule_id},
        {"$set": {
            "approval_status": "pending_human_review",
            "validation": {
                "verdict": "spot_check",
                "flag_reason": "forced_phr_after_stuck_pending_review",
                "validated_by": "manual_fix",
                "validated_at": datetime.now(timezone.utc).isoformat(),
            }
        }}
    )
    print(f"✅ {rule_id} → pending_human_review (forced)")

if __name__ == "__main__":
    main()
