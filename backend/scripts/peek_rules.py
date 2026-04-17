#!/usr/bin/env python3
"""Quick diagnostic — show sample rules from MongoDB to understand what went wrong."""
import argparse, sys
from pymongo import MongoClient

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", required=True)
    parser.add_argument("--n", type=int, default=5)
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    db = client[args.db_name]

    rules = list(db["interpretation_rules"].find({}, {"_id": 0}).limit(args.n))
    print(f"\nShowing {len(rules)} sample rules:\n{'='*70}")
    for r in rules:
        interp = r.get("interpretation") or {}
        print(f"rule_id   : {r.get('rule_id')}")
        print(f"source    : {(r.get('source') or {}).get('primary','')}")
        print(f"condition : {r.get('condition')}")
        print(f"summary   : {(interp.get('summary') or '')[:200]}")
        print(f"detailed  : {(interp.get('detailed') or '')[:200]}")
        print(f"tags      : {r.get('tags')}")
        print("-"*70)

    # Count how many look like error messages
    total = db["interpretation_rules"].count_documents({})
    error_count = db["interpretation_rules"].count_documents(
        {"interpretation.summary": {"$regex": "^Extraction failed"}}
    )
    real_count = total - error_count
    print(f"\nTotal rules       : {total}")
    print(f"Error placeholders: {error_count}  ({error_count/total*100:.0f}%)")
    print(f"Real content      : {real_count}  ({real_count/total*100:.0f}%)")
    client.close()

if __name__ == "__main__":
    main()
