#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from pymongo import MongoClient
from pymongo.errors import AutoReconnect


SCRIPT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SCRIPT_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from knowledge_validator import RuleValidator


def parse_args():
    parser = argparse.ArgumentParser(
        description="Auto-validate pending_review rules in Knowledge Engine"
    )
    # --- Source: either MongoDB (post-upload) or local JSON (pre-upload) ---
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--mongo-url", help="MongoDB connection string (post-upload mode)")
    source.add_argument(
        "--json-file",
        help=(
            "Path to local JSON rules file (pre-upload mode). "
            "Validates without touching MongoDB. "
            "Writes results to --output-file (default: same path with _VALIDATED suffix). "
            "Use this BEFORE uploading to MongoDB."
        ),
    )
    parser.add_argument("--db-name", default="horoscope_db", help="MongoDB database name (mongo-url mode only)")
    parser.add_argument("--output-file", default=None, help="Output path for validated JSON (json-file mode only)")
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--science-id", default=None, help="Filter to one science_id (default: all)")
    parser.add_argument("--batch-id", default=None, help="Filter to one import batch_id (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="Print verdicts but do NOT write results")
    parser.add_argument("--report-path", default=None, help="Optional path to write Markdown report")
    parser.add_argument(
        "--resume-from-batch", type=int, default=0,
        help=(
            "Skip the first N batches of Stage 2 (already processed in a previous run). "
            "Rules in skipped batches are marked spot_check with reason 'skipped_resume'. "
            "Rules are sorted by rule_id before batching to guarantee consistent ordering "
            "across runs. Example: --resume-from-batch 54 restarts from batch 55."
        ),
    )
    return parser.parse_args()


def fetch_from_json(json_path: str, science_id: str | None, batch_id: str | None) -> list[dict]:
    """Load rules from a local JSON file (pre-upload mode)."""
    import json
    rules = json.loads(Path(json_path).read_text(encoding="utf-8"))
    if not isinstance(rules, list):
        raise SystemExit(f"ERROR: {json_path} must be a JSON array of rules at the top level")
    # Filter to pending_review or treat all as pending (pre-upload files may not have status yet)
    pending = [
        r for r in rules
        if r.get("approval_status") in ("pending_review", None, "")
        or "approval_status" not in r
    ]
    if science_id:
        pending = [r for r in pending if r.get("science_id") == science_id]
    if batch_id:
        pending = [r for r in pending if (r.get("source") or {}).get("batch_id") == batch_id]
    return sorted(pending, key=lambda r: r.get("rule_id", ""))


def apply_verdict_json(
    rules_by_id: dict,
    rule_id: str,
    verdict: str,
    reason: str,
    corrected_confidence: str,
    validated_by: str,
    contradiction_ids: list[str],
    contradiction_summary: str,
) -> str:
    """Write validation result into an in-memory rule dict (json-file mode)."""
    status_map = {
        "approve": "auto_approved",
        "spot_check": "pending_human_review",
        "flag": "flagged",
        "structural_fail": "rejected",
    }
    new_status = status_map.get(verdict, "pending_human_review")
    if rule_id in rules_by_id:
        rules_by_id[rule_id]["approval_status"] = new_status
        rules_by_id[rule_id]["validation"] = {
            "verdict": verdict,
            "flag_reason": reason,
            "corrected_confidence": corrected_confidence,
            "validated_by": validated_by,
            "validated_at": datetime.now(timezone.utc).isoformat(),
            "contradiction_ids": contradiction_ids,
            "contradiction_summary": contradiction_summary,
        }
    return new_status


def fetch_pending(db, science_id: str | None, batch_id: str | None = None) -> list[dict]:
    query: dict = {"approval_status": "pending_review"}
    if science_id:
        query["science_id"] = science_id
    if batch_id:
        query["source.batch_id"] = batch_id
    # Sort by rule_id for deterministic ordering -- essential for --resume-from-batch
    return list(db["interpretation_rules"].find(query, {"_id": 0}).sort("rule_id", 1))


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
        for attempt in range(4):
            try:
                db["interpretation_rules"].update_many(
                    {"rule_id": rule_id},
                    {"$set": {"approval_status": new_status, "validation": validation_doc}},
                )
                break
            except AutoReconnect as exc:
                if attempt < 3:
                    wait = 2 ** attempt  # 1s, 2s, 4s
                    print(f"\n    [retry {attempt + 1}/3] MongoDB timeout for {rule_id} -- retrying in {wait}s ({exc})")
                    time.sleep(wait)
                else:
                    raise
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
    import json as _json

    args = parse_args()
    json_mode = bool(args.json_file)

    # --- Set up source / sink ---
    if json_mode:
        client = None
        db = None
        print(f"\n[PRE-UPLOAD MODE] Reading from: {args.json_file}")
        rules = fetch_from_json(args.json_file, args.science_id, args.batch_id)
        rules_by_id = {r["rule_id"]: r for r in rules}
        # Determine output path
        output_path = args.output_file
        if not output_path:
            p = Path(args.json_file)
            output_path = str(p.parent / (p.stem + "_VALIDATED" + p.suffix))
        # Also keep the full original list (including already-approved rules) for final save
        all_original = _json.loads(Path(args.json_file).read_text(encoding="utf-8"))
        orig_by_id = {r["rule_id"]: r for r in all_original}
    else:
        client = MongoClient(args.mongo_url)
        db = client[args.db_name]

    try:
        validator = RuleValidator(model="claude-haiku-4-5")

        print("\nFetching pending_review rules...")
        if json_mode:
            pass  # already fetched above
        else:
            rules = fetch_pending(db, args.science_id, getattr(args, "batch_id", None))
        print(f"Found {len(rules)} rules to validate")
        if not rules:
            if not json_mode:
                print("Nothing to do.")
                print("\n  [HINT] If you just uploaded rules, check that:")
                print("    1. approval_status was set to 'pending_review' (not 'pending_human_review')")
                print("    2. source.batch_id matches the --batch-id you provided")
            else:
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

        resume_n   = args.resume_from_batch   # batches to skip (0 = no skip)
        skipped_ids: set[str] = set()          # rule_ids skipped due to resume

        print(f"\nStage 2: Claude quality check (batch_size={args.batch_size}"
              + (f", resuming from batch {resume_n + 1}" if resume_n else "") + ")...")
        total_batches = (len(structurally_ok) + args.batch_size - 1) // args.batch_size
        for i in range(0, len(structurally_ok), args.batch_size):
            batch = structurally_ok[i : i + args.batch_size]
            batch_num = i // args.batch_size + 1

            # ── Resume: skip batches already processed in a previous run ──────
            if resume_n and batch_num <= resume_n:
                for rule in batch:
                    rid = rule["rule_id"]
                    all_verdicts[rid] = {
                        "rule_id": rid,
                        "verdict": "spot_check",
                        "reason": f"skipped_resume_from_batch_{resume_n}",
                        "corrected_confidence": current_confidence(rule),
                    }
                    skipped_ids.add(rid)
                print(f"  Batch {batch_num}/{total_batches} -- skipped (resume mode)")
                continue

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

            # ── Streaming write: commit this batch immediately ─────────────────
            # Protects against future interruptions -- each batch is persisted
            # before moving to the next. Contradiction updates happen in Stage 3.
            if not args.dry_run:
                for rule in batch:
                    rid = rule["rule_id"]
                    res = all_verdicts[rid]
                    if json_mode:
                        apply_verdict_json(
                            rules_by_id, rid,
                            res.get("verdict", "spot_check"),
                            res.get("reason", ""),
                            res.get("corrected_confidence", current_confidence(rule)),
                            "claude-haiku-4-5",
                            [], "",
                        )
                    else:
                        apply_verdict(
                            db, rid,
                            res.get("verdict", "spot_check"),
                            res.get("reason", ""),
                            res.get("corrected_confidence", current_confidence(rule)),
                            "claude-haiku-4-5",
                            [], "",   # contradictions resolved in Stage 3
                            args.dry_run,
                        )
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

        # Targeted contradiction updates -- downgrade auto_approved → spot_check
        # for any rule involved in a contradiction (streaming already wrote approve).
        if not args.dry_run and all_contradictions:
            print("  Applying contradiction downgrades...")
            for contradiction in all_contradictions:
                for rid in [contradiction["rule_id_a"], contradiction["rule_id_b"]]:
                    contra_ids     = contra_map.get(rid, [])
                    contra_summary = contradiction.get("contradiction_summary", "")
                    if json_mode:
                        if rid in rules_by_id and rules_by_id[rid].get("approval_status") == "auto_approved":
                            rules_by_id[rid]["approval_status"] = "pending_human_review"
                            v = rules_by_id[rid].setdefault("validation", {})
                            v["verdict"] = "spot_check"
                            v["flag_reason"] = f"Contradicts rule(s): {', '.join(contra_ids)}"
                            v["contradiction_ids"] = contra_ids
                            v["contradiction_summary"] = contra_summary
                    else:
                        db["interpretation_rules"].update_one(
                            {"rule_id": rid, "approval_status": "auto_approved"},
                            {"$set": {
                                "approval_status": "pending_human_review",
                                "validation.verdict": "spot_check",
                                "validation.flag_reason": f"Contradicts rule(s): {', '.join(contra_ids)}",
                                "validation.contradiction_ids": contra_ids,
                                "validation.contradiction_summary": contra_summary,
                            }},
                        )

        print(f"\nStage 4: {'[DRY RUN] ' if args.dry_run else ''}Writing skipped-batch verdicts + summary...")
        for rule in rules:
            rid = rule["rule_id"]
            verdict_info = all_verdicts.get(
                rid,
                {"verdict": "spot_check", "reason": "", "corrected_confidence": "MEDIUM"},
            )
            verdict = verdict_info.get("verdict", "spot_check")
            reason  = verdict_info.get("reason", "")
            conf    = verdict_info.get("corrected_confidence", current_confidence(rule))
            contra_ids = contra_map.get(rid, [])

            # For streamed rules (not skipped), read back the actual status so the
            # counter reflects contradiction-downgraded values.
            if rid not in skipped_ids and not args.dry_run:
                if json_mode:
                    actual_status = rules_by_id.get(rid, {}).get("approval_status", "pending_human_review")
                else:
                    doc = db["interpretation_rules"].find_one(
                        {"rule_id": rid}, {"approval_status": 1, "_id": 0}
                    )
                    actual_status = (doc or {}).get("approval_status", "pending_review")
                counters[actual_status] = counters.get(actual_status, 0) + 1
                if actual_status == "flagged":
                    rule["_reason"] = reason
                    flagged_rules.append(rule)
                continue

            # Skipped-batch rules and dry-run: write / count here
            if verdict == "approve" and contra_ids:
                verdict = "spot_check"
                reason  = f"Contradicts rule(s): {', '.join(contra_ids)}"
            contra_summary = ""
            for contradiction in all_contradictions:
                if contradiction["rule_id_a"] == rid or contradiction["rule_id_b"] == rid:
                    contra_summary = contradiction.get("contradiction_summary", "")
                    break
            if json_mode and not args.dry_run:
                new_status = apply_verdict_json(
                    rules_by_id, rid, verdict, reason, conf,
                    "claude-haiku-4-5", contra_ids, contra_summary,
                )
            else:
                new_status = apply_verdict(
                    db, rid, verdict, reason, conf,
                    "claude-haiku-4-5", contra_ids, contra_summary, args.dry_run,
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

        # --- Save validated JSON (json-file mode) ---
        if json_mode and not args.dry_run:
            # Merge validation results back into original full list
            for r in all_original:
                rid = r["rule_id"]
                if rid in rules_by_id:
                    r.update(rules_by_id[rid])
            Path(output_path).write_text(
                _json.dumps(all_original, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            print(f"\n  Validated JSON saved to: {output_path}")
            print("  Next step -- upload validated rules to MongoDB:")
            print(f"    python3 backend/scripts/ingest_[name].py \\")
            print(f"      --upload {output_path} \\")
            print(f"      --mongo-url \"$MONGO_URL\"")
            print(f"\n  Rules flagged ({counters.get('flagged', 0)}) must be triaged before upload.")
            print(f"  Review flagged rules in the output JSON and fix or remove them.")
        elif not json_mode and not args.dry_run:
            print("\n  auto_approved rules have approval_status='auto_approved' in MongoDB.")
            print("  NOTE: The live backend queries approval_status='approved' only.")
            print("  No rules reach live users until explicitly promoted to 'approved'")
            print("  via co-founder sign-off after full Phase 1 validation.")
            print("  Review flagged rules at /admin/library -> Rules Browser -> filter: flagged")

        if args.report_path:
            write_report(args.report_path, counters, all_contradictions, flagged_rules[:20], rejected_rules)
    finally:
        if client:
            client.close()


if __name__ == "__main__":
    main()
