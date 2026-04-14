#!/usr/bin/env python3
"""
Show all auto-approved rules from a validation dry run — writes NOTHING to MongoDB.
Prints each rule's content so you can review before committing verdicts.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from knowledge_validator import RuleValidator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", required=True)
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--book", help="Filter to a specific book (partial match)")
    parser.add_argument("--limit", type=int, default=0, help="Max rules to show (0 = all)")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    db = client[args.db_name]
    validator = RuleValidator()

    query = {}
    if args.book:
        query["source.primary"] = {"$regex": args.book, "$options": "i"}

    rules = list(db["interpretation_rules"].find(query, {"_id": 0}))
    print(f"Loaded {len(rules)} rules from MongoDB\n")

    # Stage 1 — structural check (free, no API)
    structurally_ok = []
    rejected = []
    for r in rules:
        ok, reason = validator.structural_check(r)
        if ok:
            structurally_ok.append(r)
        else:
            rejected.append((r, reason))

    print(f"Structural pass : {len(structurally_ok)}")
    print(f"Structural fail : {len(rejected)}\n")

    # Stage 2 — Claude Haiku quality check in batches
    approved = []
    spot_check = []
    flagged = []

    batches = [
        structurally_ok[i:i + args.batch_size]
        for i in range(0, len(structurally_ok), args.batch_size)
    ]

    for idx, batch in enumerate(batches):
        print(f"  Validating batch {idx+1}/{len(batches)} ({len(batch)} rules)...", end=" ", flush=True)
        results = validator.validate_batch(batch)
        for rule, result in zip(batch, results):
            verdict = (result or {}).get("verdict", "spot_check")
            reason  = (result or {}).get("reason", "")
            conf    = (result or {}).get("corrected_confidence", "MEDIUM")
            if verdict == "approve":
                approved.append((rule, reason, conf))
            elif verdict == "flag":
                flagged.append((rule, reason, conf))
            else:
                spot_check.append((rule, reason, conf))
        print(f"approve={sum(1 for _,v,_ in [(r,validator.validate_batch([r]),None) for r in []] if True)} done")

    print(f"\n{'='*70}")
    print(f"RESULTS  |  approve: {len(approved)}  |  spot_check: {len(spot_check)}  |  flagged: {len(flagged)}  |  rejected: {len(rejected)}")
    print(f"{'='*70}\n")

    # ── Print approved rules ──────────────────────────────────────────────────
    to_show = approved if not args.limit else approved[:args.limit]
    print(f"AUTO-APPROVED RULES ({len(to_show)} of {len(approved)} shown)\n")
    print("=" * 70)

    for i, (rule, reason, conf) in enumerate(to_show, 1):
        interp  = rule.get("interpretation") or {}
        source  = rule.get("source") or {}
        cond    = rule.get("condition") or {}
        summary = (interp.get("summary") or "").strip()
        detailed = (interp.get("detailed") or "").strip()

        print(f"[{i:03d}] {rule.get('rule_id')}")
        print(f"  Book      : {source.get('primary','')}")
        print(f"  Chapter   : {source.get('chapter','')}")
        print(f"  Domain    : {rule.get('life_domain','')}")
        print(f"  Condition : {cond.get('type','')} | "
              f"planet={cond.get('planet', cond.get('planets',''))} | "
              f"house={cond.get('house','')} sign={cond.get('sign','')}")
        print(f"  Confidence: {conf}")
        print(f"  Summary   : {summary[:300]}")
        if detailed and detailed != summary:
            print(f"  Detailed  : {detailed[:400]}")
        print()

    # ── Summary stats by book ────────────────────────────────────────────────
    print("=" * 70)
    print("APPROVED BY BOOK\n")
    book_counts: dict[str, int] = {}
    for rule, _, _ in approved:
        book = (rule.get("source") or {}).get("primary", "unknown")
        book_counts[book] = book_counts.get(book, 0) + 1
    for book, count in sorted(book_counts.items(), key=lambda x: -x[1]):
        print(f"  {count:>4}  {book}")

    client.close()


if __name__ == "__main__":
    main()
