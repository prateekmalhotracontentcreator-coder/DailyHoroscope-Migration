#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from pymongo import MongoClient


SCRIPT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SCRIPT_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from knowledge_validator import RuleValidator


def parse_args():
    parser = argparse.ArgumentParser(
        description="Auto-validate pending_review rules in Knowledge Engine"
    )
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", required=True)
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--science-id", default=None, help="Filter to one science_id (default: all)")
    parser.add_argument("--batch-id", default=None, help="Filter to one import batch_id (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="Print verdicts but do NOT write to MongoDB")
    parser.add_argument("--report-path", default=None, help="Optional path to write Markdown report")
    return parser.parse_args()


def fetch_pending(db, science_id: str | None, batch_id: str | None = None) -> list[dict]:
    query: dict = {"approval_status": "pending_review"}
    if science_id:
        query["science_id"] = science_id
    if batch_id:
        query["source.batch_id"] = batch_id
    return list(db["interpretation_rules"].find(query, {"_id": 0}))


def group_for_contradiction(rules: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for rule in rules:
        cond = rule.get("condition") or {}
        ctype = cond.get("type", "unknown")
        planet = cond.get("planet", "")
        house = str(cond.get("house", cond.get("sign", "")))
        key = f"{ctype}|{planet}|{house}"
        groups[key].append(rule)
    return {key: group for key, group in groups.items() if len(group) >= 2}


def current_confidence(rule: dict) -> str:
    validation = rule.get("validation") or {}
    if validation.get("corrected_confidence"):
        return str(validation["corrected_confidence"]).upper()
    passages = ((rule.get("interpretation") or {}).get("full_text_passages") or [])
    if passages:
        confidence = passages[0].get("confidence")
        if confidence:
            return str(confidence).upper()
    return "MEDIUM"


def apply_verdict(
    db,
    rule_id: str,
    verdict: str,
    reason: str,
    corrected_confidence: str,
    validated_by: str,
    contradiction_ids: list[str],
    contradiction_summary: str,
    dry_run: bool,
) -> str:
    status_map = {
        "approve": "auto_approved",
        "spot_check": "pending_human_review",
        "flag": "flagged",
        "structural_fail": "rejected",
    }
    new_status = status_map.get(verdict, "pending_review")

    validation_doc = {
        "verdict": verdict,
        "flag_reason": reason,
        "corrected_confidence": corrected_confidence,
        "validated_by": validated_by,
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "contradiction_ids": contradiction_ids,
        "contradiction_summary": contradiction_summary,
    }

    if not dry_run:
        db["interpretation_rules"].update_one(
            {"rule_id": rule_id},
            {"$set": {"approval_status": new_status, "validation": validation_doc}},
        )
    return new_status


def write_report(path: str, counters: dict, contradictions: list, flagged_sample: list, rejected: list):
    total = sum(counters.values())
    lines = [
        "# Knowledge Engine Validation Report",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Summary",
        "",
        "| Status | Count | % |",
        "|---|---|---|",
    ]
    for status, count in sorted(counters.items(), key=lambda item: -item[1]):
        pct = f"{count / total * 100:.0f}%" if total else "0%"
        lines.append(f"| {status} | {count} | {pct} |")
    lines += [f"| **Total** | **{total}** | |", ""]

    if contradictions:
        lines += ["## Contradictions Detected", ""]
        for contradiction in contradictions:
            lines.append(
                f"- `{contradiction['rule_id_a']}` <-> `{contradiction['rule_id_b']}`: "
                f"{contradiction['contradiction_summary']}"
            )
        lines.append("")

    if flagged_sample:
        lines += [f"## Flagged Rules (first {len(flagged_sample)})", "", "| rule_id | book | reason |", "|---|---|---|"]
        for rule in flagged_sample:
            source = rule.get("source") or {}
            lines.append(f"| {rule['rule_id']} | {source.get('primary', '')} | {rule.get('_reason', '')} |")
        lines.append("")

    if rejected:
        lines += ["## Rejected Rules (structural failures)", "", "| rule_id | reason |", "|---|---|"]
        for rule in rejected:
            lines.append(f"| {rule['rule_id']} | {rule.get('_reason', '')} |")
        lines.append("")

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines), encoding="utf-8")
    print(f"\n  Report written to {path}")


def main():
    args = parse_args()
    client = MongoClient(args.mongo_url)
    try:
        db = client[args.db_name]
        validator = RuleValidator(model="claude-haiku-4-5")

        print("\nFetching pending_review rules...")
        rules = fetch_pending(db, args.science_id, getattr(args, "batch_id", None))
        print(f"Found {len(rules)} rules to validate")
        if not rules:
            print("Nothing to do.")
            return

        counters: dict[str, int] = {}
        all_verdicts: dict[str, dict] = {}
        flagged_rules: list[dict] = []
        rejected_rules: list[dict] = []
        all_contradictions: list[dict] = []

        print("\nStage 1: Structural checks...")
        structurally_ok: list[dict] = []
        for rule in rules:
            passed, reason = validator.structural_check(rule)
            if not passed:
                all_verdicts[rule["rule_id"]] = {
                    "verdict": "structural_fail",
                    "reason": reason,
                    "corrected_confidence": current_confidence(rule),
                }
                rule["_reason"] = reason
                rejected_rules.append(rule)
            else:
                structurally_ok.append(rule)
        print(f"  Structural failures: {len(rejected_rules)} / {len(rules)}")
        print(f"  Proceeding with: {len(structurally_ok)} rules")

        print(f"\nStage 2: Claude quality check (batch_size={args.batch_size})...")
        total_batches = (len(structurally_ok) + args.batch_size - 1) // args.batch_size
        for i in range(0, len(structurally_ok), args.batch_size):
            batch = structurally_ok[i : i + args.batch_size]
            batch_num = i // args.batch_size + 1
            print(f"  Batch {batch_num}/{total_batches} ({len(batch)} rules)...", end=" ", flush=True)
            try:
                results = validator.validate_batch(batch)
            except Exception as exc:
                print(f"ERROR: {exc} - marking batch as spot_check")
                results = [
                    {
                        "rule_id": rule["rule_id"],
                        "verdict": "spot_check",
                        "reason": f"batch_error: {exc}",
                        "corrected_confidence": "MEDIUM",
                    }
                    for rule in batch
                ]

            result_map = {result["rule_id"]: result for result in results}
            for rule in batch:
                rid = rule["rule_id"]
                res = result_map.get(
                    rid,
                    {
                        "rule_id": rid,
                        "verdict": "spot_check",
                        "reason": "no_response_from_model",
                        "corrected_confidence": "MEDIUM",
                    },
                )
                all_verdicts[rid] = res
            print("done")

        print("\nStage 3: Contradiction detection...")
        groups = group_for_contradiction(structurally_ok)
        print(f"  {len(groups)} condition groups with >=2 rules to check")
        for _, group_rules in groups.items():
            try:
                contradictions = validator.detect_contradictions(group_rules)
            except Exception:
                contradictions = []
            all_contradictions.extend(contradictions)

        contra_map: dict[str, list[str]] = defaultdict(list)
        for contradiction in all_contradictions:
            contra_map[contradiction["rule_id_a"]].append(contradiction["rule_id_b"])
            contra_map[contradiction["rule_id_b"]].append(contradiction["rule_id_a"])
        print(f"  Contradictions found: {len(all_contradictions)} pair(s)")

        print(f"\nStage 4: {'[DRY RUN] ' if args.dry_run else ''}Writing verdicts...")
        for rule in rules:
            rid = rule["rule_id"]
            verdict_info = all_verdicts.get(
                rid,
                {"verdict": "spot_check", "reason": "", "corrected_confidence": "MEDIUM"},
            )
            verdict = verdict_info.get("verdict", "spot_check")
            reason = verdict_info.get("reason", "")
            conf = verdict_info.get("corrected_confidence", current_confidence(rule))
            contra_ids = contra_map.get(rid, [])
            if verdict == "approve" and contra_ids:
                verdict = "spot_check"
                reason = f"Contradicts rule(s): {', '.join(contra_ids)}"
            contra_summary = ""
            for contradiction in all_contradictions:
                if contradiction["rule_id_a"] == rid or contradiction["rule_id_b"] == rid:
                    contra_summary = contradiction.get("contradiction_summary", "")
                    break
            new_status = apply_verdict(
                db,
                rid,
                verdict,
                reason,
                conf,
                "claude-haiku-4-5",
                contra_ids,
                contra_summary,
                args.dry_run,
            )
            counters[new_status] = counters.get(new_status, 0) + 1
            if new_status == "flagged":
                rule["_reason"] = reason
                flagged_rules.append(rule)

        total = sum(counters.values())
        print(f"\n{'=' * 55}")
        print(f"{'[DRY RUN] ' if args.dry_run else ''}VALIDATION COMPLETE")
        for status, count in sorted(counters.items(), key=lambda item: -item[1]):
            pct = f"{count / total * 100:.0f}%" if total else "0%"
            print(f"  {status:<28} {count:>4}  ({pct})")
        print(f"  {'-' * 40}")
        print(f"  {'Total':<28} {total:>4}")
        print(f"\n  Contradictions: {len(all_contradictions)} pair(s)")
        if not args.dry_run:
            print("\n  auto_approved rules are live after next index refresh.")
            print("  Review flagged rules at /admin/library -> Rules Browser -> filter: flagged")

        if args.report_path:
            write_report(args.report_path, counters, all_contradictions, flagged_rules[:20], rejected_rules)
    finally:
        client.close()


if __name__ == "__main__":
    main()
