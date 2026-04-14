#!/usr/bin/env python3
"""
Full book review — shows ALL rules by verdict category.
Writes NOTHING to MongoDB. Use before re-ingesting to understand quality.

Usage:
  python3 scripts/review_book.py --book "Text Book" --mongo-url ... --db-name ...

Flags:
  --status   Filter to one category: approved / spot_check / flagged / rejected / all (default: all)
  --limit    Max rules per category (default: 0 = all)
  --book     Partial book name match (required)
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from knowledge_validator import RuleValidator

DIVIDER = "=" * 70
MINI_DIV = "-" * 70


def fmt_rule(rank: int, rule: dict, reason: str, conf: str) -> str:
    interp   = rule.get("interpretation") or {}
    source   = rule.get("source") or {}
    cond     = rule.get("condition") or {}
    summary  = (interp.get("summary") or "").strip()
    detailed = (interp.get("detailed") or "").strip()
    planets  = cond.get("planet") or cond.get("planets") or ""
    lines = [
        f"[{rank:03d}] {rule.get('rule_id')}",
        f"  Book      : {source.get('primary','')}",
        f"  Chapter   : {source.get('chapter','')}",
        f"  Domain    : {rule.get('life_domain','')}",
        f"  Condition : {cond.get('type','')} | planet={planets} | "
        f"house={cond.get('house','')} sign={cond.get('sign','')}",
        f"  Confidence: {conf}",
        f"  Summary   : {summary[:300]}",
    ]
    if detailed and detailed != summary:
        lines.append(f"  Detailed  : {detailed[:400]}")
    if reason:
        lines.append(f"  ⚠ Reason  : {reason}")
    return "\n".join(lines)


def print_section(title: str, emoji: str, rules_data: list[tuple], limit: int) -> None:
    to_show = rules_data[:limit] if limit else rules_data
    print(f"\n{DIVIDER}")
    print(f"{emoji}  {title}  ({len(to_show)} of {len(rules_data)} shown)")
    print(DIVIDER)
    if not rules_data:
        print("  (none)")
        return
    for i, (rule, reason, conf) in enumerate(to_show, 1):
        print(fmt_rule(i, rule, reason, conf))
        print(MINI_DIV)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", required=True)
    parser.add_argument("--book", required=True, help="Partial book name match")
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--status", default="all",
                        choices=["all", "approved", "spot_check", "flagged", "rejected"])
    parser.add_argument("--limit", type=int, default=0,
                        help="Max rules to show per category (0 = all)")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    db = client[args.db_name]
    validator = RuleValidator()

    rules = list(db["interpretation_rules"].find(
        {"source.primary": {"$regex": args.book, "$options": "i"}},
        {"_id": 0}
    ))

    if not rules:
        print(f"No rules found for book matching '{args.book}'")
        client.close()
        return

    print(f"\nLoaded {len(rules)} rules for: {args.book}\n")

    # ── Stage 1: Structural check ────────────────────────────────────────────
    ok_rules, rejected = [], []
    for r in rules:
        passed, reason = validator.structural_check(r)
        if passed:
            ok_rules.append(r)
        else:
            rejected.append((r, reason, "LOW"))

    print(f"Structural pass : {len(ok_rules)}")
    print(f"Structural fail : {len(rejected)}")

    # ── Stage 2: Claude Haiku quality check ──────────────────────────────────
    approved, spot_check, flagged = [], [], []
    batches = [ok_rules[i:i + args.batch_size]
               for i in range(0, len(ok_rules), args.batch_size)]

    print(f"Running {len(batches)} validation batches...\n")
    for idx, batch in enumerate(batches):
        print(f"  Batch {idx+1}/{len(batches)} ({len(batch)} rules)...", end=" ", flush=True)
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
        print("done")

    # ── Results summary ──────────────────────────────────────────────────────
    print(f"\n{DIVIDER}")
    print("FULL REVIEW SUMMARY")
    print(DIVIDER)
    print(f"  ✅ Auto-approved       : {len(approved):>4}  ({len(approved)/len(rules)*100:.0f}%)")
    print(f"  🔶 Pending human review: {len(spot_check):>4}  ({len(spot_check)/len(rules)*100:.0f}%)")
    print(f"  ⛔ Flagged             : {len(flagged):>4}  ({len(flagged)/len(rules)*100:.0f}%)")
    print(f"  ❌ Rejected (struct)   : {len(rejected):>4}  ({len(rejected)/len(rules)*100:.0f}%)")
    print(f"  {'─'*40}")
    print(f"     Total               : {len(rules):>4}")

    # ── Print sections based on --status filter ──────────────────────────────
    show_all = args.status == "all"

    if show_all or args.status == "approved":
        print_section("AUTO-APPROVED — Ready for production", "✅", approved, args.limit)

    if show_all or args.status == "spot_check":
        print_section("PENDING HUMAN REVIEW — Quick expert check needed", "🔶", spot_check, args.limit)

    if show_all or args.status == "flagged":
        print_section("FLAGGED — Issues found by Claude Haiku", "⛔", flagged, args.limit)

    if show_all or args.status == "rejected":
        print_section("REJECTED — Failed structural check", "❌", rejected, args.limit)

    # ── Flag pattern analysis ─────────────────────────────────────────────────
    if flagged and (show_all or args.status == "flagged"):
        print(f"\n{DIVIDER}")
        print("FLAG REASON PATTERNS (top issues to fix)\n")
        from collections import Counter
        # Extract first 8 words of each reason as a pattern
        patterns: Counter = Counter()
        for _, reason, _ in flagged:
            key = " ".join(reason.split()[:8]) if reason else "no reason given"
            patterns[key] += 1
        for pattern, count in patterns.most_common(10):
            print(f"  {count:>3}x  {pattern}")

    client.close()
    print(f"\n{DIVIDER}")
    print("Review complete. Nothing written to MongoDB.")
    print(DIVIDER)


if __name__ == "__main__":
    main()
