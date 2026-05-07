#!/usr/bin/env python3
"""
Mundane Astrology — Interpretation Rules Validator
===================================================
Validates all `interpretation_rules` documents with science_id = 'mundane_jyotish'
that are in 'pending_review' status.

Adapts the validate_rules.py 3-stage pattern (structural → Claude quality →
contradiction detection) to the mundane rule schema, which is structurally
different from BPHS/Lal Kitab rules:

  Mundane schema:
    condition      : str  (free-form "IF ... AND ..." text)
    result         : str  (free-form outcome text)
    sub_type       : str  (e.g. "monsoon_forecast", "election_prediction")
    severity       : str  (low / medium / high / critical)
    source_chapter : str
    checkable      : bool

  BPHS/Lal Kitab schema (NOT used here):
    interpretation : { detailed: str, summary: str }
    condition      : dict { type, planet, house, ... }

Usage:
    python3 backend/scripts/validate_mundane_rules.py \\
        --mongo-url "$MONGO_URL" --db-name horoscope_db

    # Dry run — print verdicts, no writes:
    python3 backend/scripts/validate_mundane_rules.py \\
        --mongo-url "$MONGO_URL" --db-name horoscope_db --dry-run

    # Restrict to one batch:
    python3 backend/scripts/validate_mundane_rules.py \\
        --mongo-url "$MONGO_URL" --db-name horoscope_db \\
        --batch-id mundane-interp-v19-20260507

    # Write Markdown report:
    python3 backend/scripts/validate_mundane_rules.py \\
        --mongo-url "$MONGO_URL" --db-name horoscope_db \\
        --report-path backend/scripts/reports/mundane_validation.md

Verdict → approval_status mapping:
    approve         → auto_approved
    spot_check      → pending_human_review
    flag            → flagged
    structural_fail → rejected
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from pymongo import MongoClient
from pymongo.errors import AutoReconnect


# ── Constants ─────────────────────────────────────────────────────────────────

VALID_SEVERITIES  = {"low", "medium", "high", "critical"}
VALID_SUB_TYPES   = {
    # weather / natural
    "monsoon_forecast", "weather_prediction", "seismic_prediction",
    "crop_prediction", "flood_prediction",
    # governance / political
    "oath_chart_tenure", "oath_chart_finance", "oath_muhurta_selection",
    "election_prediction", "yearly_governance", "leadership_autopsy",
    # simhasan / authority
    "simhasan_chakra",
    # market / economic
    "market_prediction", "commodity_prediction",
    # war / geopolitical
    "war_prediction", "geopolitical_prediction", "assassination_hazard",
    "terrorism_prediction",
    # celebrity / natal
    "celebrity_authenticity", "natal_timing",
    # general
    "eclipse_prediction", "transit_prediction", "foundation_chart",
    "synthesis_rule", "validation_rule",
}

GARBAGE_RE = re.compile(
    r"(.)\1{6,}|"            # 7+ repeated chars
    r"[^\x00-\x7F]{15,}|"   # 15+ non-ASCII
    r"\b[A-Z]{20,}\b"        # 20+ all-caps word
)

MIN_WORDS_CONDITION = 4   # short but precise transit/ingress conditions are valid (e.g. "Saturn enters Leo")
MIN_WORDS_RESULT    = 10


# ── Validation prompt (mundane-specific) ─────────────────────────────────────

VALIDATION_SYSTEM = (
    "You are a senior Vedic astrology scholar and mundane astrology expert. "
    "You evaluate mundane interpretation rules for correctness, coherence, "
    "and faithfulness to classical and modern mundane Vedic astrology sources "
    "including Gopalakrishnan, Mehta, Gaur (AIFAS), Gaur Astrology, and Raphael."
)

VALIDATION_PROMPT = """\
Evaluate each mundane astrology rule below and return a JSON array — one object per rule.

For each rule assess:
1. CORRECTNESS  — Is the astrological logic consistent with mundane astrology principles?
2. QUALITY      — Is the condition/result pair coherent, specific, and usable as a forecast?
3. FAITHFULNESS — Does it faithfully represent what the source chapter would say?

Mundane rules cover: elections, oath charts, yearly governance (planetary cabinet),
weather/monsoon, war, seismic, markets, celebrity authenticity, eclipse prediction,
transits, and Simhasan Chakra.

Verdict options:
  "approve"     — correct and ready for production review
  "spot_check"  — probably fine but borderline; flag for quick human glance
  "flag"        — incorrect, incoherent, internally contradictory, or factually wrong

Return ONLY valid JSON — no markdown fences, no commentary:
[
  {{
    "rule_id": "<rule_id>",
    "verdict": "approve" | "spot_check" | "flag",
    "reason": "<one sentence — required for spot_check and flag, empty string for approve>",
    "corrected_confidence": "HIGH" | "MEDIUM" | "LOW"
  }}
]

Rules to evaluate:
{rules_json}
"""

CONTRADICTION_PROMPT = """\
Check whether any rules below directly contradict each other.

A true contradiction is when two rules make OPPOSITE factual claims about the
same astrological configuration — e.g. one says "Jupiter in X produces prosperity"
and another says "Jupiter in X produces poverty" for an identical condition.

Different emphasis, different time-scales, or different source books are NOT contradictions.
Partial overlap (one rule more specific than another) is NOT a contradiction.

Return ONLY valid JSON — no markdown fences:
[
  {{
    "rule_id_a": "...",
    "rule_id_b": "...",
    "contradiction_summary": "<one sentence>"
  }}
]
Return an empty array [] if no contradictions found.

Rules to compare:
{rules_json}
"""


# ── Structural check ──────────────────────────────────────────────────────────

def structural_check(rule: dict) -> tuple[bool, str]:
    """
    Validate the mundane rule schema.
    Returns (True, 'ok') or (True, 'old_schema') if the rule passes.
    Returns (False, reason) for genuine structural failures.

    Two special cases handled gracefully (not rejected):
    1. Old-schema rules (v1/v2): condition is a dict or missing, result is missing.
       These use the legacy pymongo schema (interpretation.detailed / summary).
       Marked spot_check with reason 'old_schema_migration_pending' — not rejected,
       because they are not wrong, just awaiting a separate migration decision.
    2. Condition terminal punctuation is NOT checked: mundane conditions use the
       format "IF ... AND ... → trigger" which ends with a word by design.
       Only result text is checked for terminal punctuation.
    """
    # ── Old-schema / matrix-condition detection ──────────────────────────────
    # Two non-rejected special cases:
    #
    # 1. Old-schema (v1/v2 pymongo rules): condition is a dict or missing AND
    #    an 'interpretation' sub-dict is present. Different from motor schema.
    #    → spot_check with reason 'old_schema_migration_pending'
    #
    # 2. Matrix-engine rules (v3–v7): condition is a dict lookup-table BUT
    #    result IS a valid string. These are legitimate engine-input specs
    #    (e.g. Celestial Council king/minister outcome matrices) where the
    #    condition encodes a planet→outcome lookup rather than a prose IF clause.
    #    → spot_check with reason 'matrix_condition_dict_pending_review'
    #
    # In both cases the rule is NOT rejected — it is routed to pending_human_review.
    condition_raw = rule.get("condition")
    result_raw    = rule.get("result")
    has_interp    = isinstance(rule.get("interpretation"), dict)

    if (condition_raw is None or isinstance(condition_raw, dict)) and has_interp:
        # Old-schema BPHS/pymongo-style rule in the mundane collection
        return True, "old_schema_migration_pending"

    if result_raw is None and has_interp:
        return True, "old_schema_migration_pending"

    if isinstance(condition_raw, dict) and (
        (isinstance(result_raw, str) and result_raw.strip())
        or isinstance(result_raw, dict)
    ):
        # v3–v7 matrix-engine rules: structured dict condition + prose result
        # (or dual-dict lookup table where both condition and result are dicts).
        # These are valid rules awaiting a condition/result string migration pass.
        return True, "matrix_condition_dict_pending_review"

    # ── Required string fields ────────────────────────────────────────────────
    for field in ("rule_id", "science_id", "sub_type", "title",
                  "source_chapter", "condition", "result"):
        val = rule.get(field)
        if not val or not isinstance(val, str) or not val.strip():
            return False, f"missing_or_empty_{field}"

    # ── science_id ────────────────────────────────────────────────────────────
    if rule.get("science_id") != "mundane_jyotish":
        return False, f"wrong_science_id:{rule.get('science_id')}"

    # ── Severity ─────────────────────────────────────────────────────────────
    severity = rule.get("severity", "")
    if severity not in VALID_SEVERITIES:
        return False, f"invalid_severity:{severity}"

    condition = rule.get("condition", "")
    result    = rule.get("result", "")

    # ── Garbage / OCR check ──────────────────────────────────────────────────
    if GARBAGE_RE.search(condition) or GARBAGE_RE.search(result):
        return False, "garbage_text_detected"

    # ── Minimum word counts ───────────────────────────────────────────────────
    if len(condition.split()) < MIN_WORDS_CONDITION:
        return False, f"condition_too_short({len(condition.split())} words)"

    if len(result.split()) < MIN_WORDS_RESULT:
        return False, f"result_too_short({len(result.split())} words)"

    # ── Terminal punctuation on RESULT only ───────────────────────────────────
    # NOTE: condition is intentionally NOT checked for terminal punctuation.
    # Mundane conditions use the "IF ... AND ... → trigger" format which
    # ends with a word by design — this is valid mundane rule syntax, not
    # truncation. The BPHS truncation-detection heuristic does not apply here.
    last_result = result.strip()[-1] if result.strip() else ""
    if last_result not in ".!?)\"'":
        return False, "truncated_result_text"

    # ── synthesis_sources must be a list if present ───────────────────────────
    sources = rule.get("synthesis_sources")
    if sources is not None and not isinstance(sources, list):
        return False, "synthesis_sources_not_list"

    return True, "ok"


# ── Claude quality check ──────────────────────────────────────────────────────

def _rule_to_prompt_item(rule: dict) -> dict:
    return {
        "rule_id":        rule.get("rule_id", ""),
        "source_chapter": rule.get("source_chapter", ""),
        "sub_type":       rule.get("sub_type", ""),
        "severity":       rule.get("severity", ""),
        "condition":      (rule.get("condition") or "")[:400],
        "result":         (rule.get("result") or "")[:400],
    }


def _call_claude(prompt: str, model: str) -> list[dict]:
    try:
        import anthropic
    except ImportError as exc:
        raise RuntimeError("anthropic package not installed — pip3 install anthropic") from exc
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set in environment")
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        temperature=0.1,
        system=VALIDATION_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    content = (response.content[0].text or "").strip()
    content = re.sub(r"^```[a-z]*\n?", "", content)
    content = re.sub(r"\n?```$",        "", content)
    try:
        result = json.loads(content)
        return result if isinstance(result, list) else []
    except json.JSONDecodeError:
        return []


def validate_batch(rules: list[dict], model: str) -> list[dict]:
    if not rules:
        return []
    items  = [_rule_to_prompt_item(r) for r in rules]
    prompt = VALIDATION_PROMPT.format(rules_json=json.dumps(items, indent=2))
    return _call_claude(prompt, model)


def detect_contradictions(rules: list[dict], model: str) -> list[dict]:
    if len(rules) < 2:
        return []
    items  = [_rule_to_prompt_item(r) for r in rules]
    prompt = CONTRADICTION_PROMPT.format(rules_json=json.dumps(items, indent=2))
    return _call_claude(prompt, model)


# ── MongoDB helpers ───────────────────────────────────────────────────────────

def fetch_pending(db, batch_id: str | None) -> list[dict]:
    query: dict = {
        "approval_status": "pending_review",
        "science_id":      "mundane_jyotish",
    }
    if batch_id:
        query["batch_id"] = batch_id
    return list(
        db["interpretation_rules"]
        .find(query, {"_id": 0})
        .sort("rule_id", 1)
    )


STATUS_MAP = {
    "approve":        "auto_approved",
    "spot_check":     "pending_human_review",
    "flag":           "flagged",
    "structural_fail":"rejected",
}


def apply_verdict(db, rule_id: str, verdict: str, reason: str,
                  corrected_confidence: str, validated_by: str,
                  contradiction_ids: list[str], contradiction_summary: str,
                  dry_run: bool) -> str:
    new_status = STATUS_MAP.get(verdict, "pending_review")
    validation_doc = {
        "verdict":               verdict,
        "flag_reason":           reason,
        "corrected_confidence":  corrected_confidence,
        "validated_by":          validated_by,
        "validated_at":          datetime.now(timezone.utc).isoformat(),
        "contradiction_ids":     contradiction_ids,
        "contradiction_summary": contradiction_summary,
    }
    if not dry_run:
        for attempt in range(4):
            try:
                db["interpretation_rules"].update_many(
                    {"rule_id": rule_id},
                    {"$set": {
                        "approval_status": new_status,
                        "validation":      validation_doc,
                    }},
                )
                break
            except AutoReconnect as exc:
                if attempt < 3:
                    wait = 2 ** attempt
                    print(f"\n    [retry {attempt+1}/3] MongoDB timeout for "
                          f"{rule_id} — retrying in {wait}s ({exc})")
                    time.sleep(wait)
                else:
                    raise
    return new_status


# ── Report writer ─────────────────────────────────────────────────────────────

def write_report(path: str, counters: dict, contradictions: list,
                 flagged: list, rejected: list):
    total = sum(counters.values())
    lines = [
        "# Mundane Astrology Validation Report",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Summary",
        "",
        "| Status | Count | % |",
        "|---|---|---|",
    ]
    for status, count in sorted(counters.items(), key=lambda x: -x[1]):
        pct = f"{count/total*100:.0f}%" if total else "0%"
        lines.append(f"| {status} | {count} | {pct} |")
    lines += [f"| **Total** | **{total}** | |", ""]

    if contradictions:
        lines += ["## Contradictions Detected", ""]
        for c in contradictions:
            lines.append(
                f"- `{c['rule_id_a']}` ↔ `{c['rule_id_b']}`: {c['contradiction_summary']}"
            )
        lines.append("")

    if flagged:
        lines += [f"## Flagged Rules (first {len(flagged)})", "",
                  "| rule_id | sub_type | severity | reason |",
                  "|---|---|---|---|"]
        for r in flagged:
            lines.append(
                f"| {r['rule_id']} | {r.get('sub_type','')} | "
                f"{r.get('severity','')} | {r.get('_reason','')} |"
            )
        lines.append("")

    if rejected:
        lines += ["## Rejected Rules (structural failures)", "",
                  "| rule_id | reason |", "|---|---|"]
        for r in rejected:
            lines.append(f"| {r['rule_id']} | {r.get('_reason','')} |")
        lines.append("")

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines), encoding="utf-8")
    print(f"\n  Report written → {path}")


# ── Main ──────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description="Validate mundane_jyotish interpretation rules"
    )
    p.add_argument("--mongo-url",   required=True)
    p.add_argument("--db-name",     required=True)
    p.add_argument("--batch-size",  type=int, default=20,
                   help="Rules per Claude Haiku batch (default 20)")
    p.add_argument("--batch-id",    default=None,
                   help="Restrict to one ingest batch_id (default: all pending)")
    p.add_argument("--model",       default="claude-haiku-4-5",
                   help="Anthropic model for quality check (default: claude-haiku-4-5)")
    p.add_argument("--dry-run",     action="store_true",
                   help="Print verdicts but do NOT write to MongoDB")
    p.add_argument("--report-path", default=None,
                   help="Optional Markdown report output path")
    p.add_argument("--skip-claude", action="store_true",
                   help="Skip Claude quality check (structural check only) — useful for quick schema audit")
    return p.parse_args()


def main():
    args  = parse_args()
    client = MongoClient(args.mongo_url)
    try:
        db = client[args.db_name]

        print("\nFetching pending_review mundane rules...")
        rules = fetch_pending(db, args.batch_id)
        print(f"Found {len(rules)} rules  (science_id=mundane_jyotish, status=pending_review)")
        if not rules:
            print("Nothing to validate.")
            return

        counters:       dict[str, int]  = {}
        all_verdicts:   dict[str, dict] = {}
        flagged_rules:  list[dict]      = []
        rejected_rules: list[dict]      = []
        all_contradictions: list[dict]  = []

        # ── Stage 1: Structural check ─────────────────────────────────────────
        print(f"\nStage 1: Structural checks ({len(rules)} rules)...")
        structurally_ok:  list[dict] = []
        old_schema_rules: list[dict] = []
        for rule in rules:
            passed, reason = structural_check(rule)
            if not passed:
                all_verdicts[rule["rule_id"]] = {
                    "verdict":              "structural_fail",
                    "reason":               reason,
                    "corrected_confidence": "LOW",
                }
                rule["_reason"] = reason
                rejected_rules.append(rule)
                if args.dry_run:
                    print(f"    ✗ REJECTED            {rule['rule_id']}  [{reason}]")
            elif reason in ("old_schema_migration_pending",
                            "matrix_condition_dict_pending_review"):
                # These rules are valid but need a migration pass:
                #   old_schema_migration_pending   → v1/v2 pymongo schema
                #   matrix_condition_dict_pending_review → v3–v7 dict-condition matrix rules
                # Both bypass Claude quality check and go straight to pending_human_review.
                all_verdicts[rule["rule_id"]] = {
                    "verdict":              "spot_check",
                    "reason":               reason,
                    "corrected_confidence": "MEDIUM",
                }
                old_schema_rules.append(rule)
                if args.dry_run:
                    tag = "OLD_SCHEMA" if reason == "old_schema_migration_pending" else "MATRIX_COND"
                    print(f"    ~ {tag}_PENDING  {rule['rule_id']}")
            else:
                structurally_ok.append(rule)

        print(f"  Structural failures    : {len(rejected_rules)} / {len(rules)}")
        print(f"  Migration-pending      : {len(old_schema_rules)} / {len(rules)}")
        print(f"  Proceeding with Claude : {len(structurally_ok)} rules")

        # ── Stage 2: Claude quality check ────────────────────────────────────
        if args.skip_claude:
            print("\nStage 2: Skipped (--skip-claude flag set)")
            for rule in structurally_ok:
                all_verdicts[rule["rule_id"]] = {
                    "verdict":              "spot_check",
                    "reason":               "skipped_claude_check",
                    "corrected_confidence": "MEDIUM",
                }
        else:
            print(f"\nStage 2: Claude quality check  "
                  f"(model={args.model}, batch_size={args.batch_size})...")
            total_batches = (len(structurally_ok) + args.batch_size - 1) // args.batch_size

            for i in range(0, len(structurally_ok), args.batch_size):
                batch     = structurally_ok[i : i + args.batch_size]
                batch_num = i // args.batch_size + 1
                print(f"  Batch {batch_num}/{total_batches} "
                      f"({len(batch)} rules)...", end=" ", flush=True)
                try:
                    results = validate_batch(batch, args.model)
                except Exception as exc:
                    print(f"ERROR: {exc} — marking batch as spot_check")
                    results = [
                        {
                            "rule_id":              r["rule_id"],
                            "verdict":              "spot_check",
                            "reason":               f"batch_error: {exc}",
                            "corrected_confidence": "MEDIUM",
                        }
                        for r in batch
                    ]

                result_map = {r["rule_id"]: r for r in results}
                for rule in batch:
                    rid = rule["rule_id"]
                    res = result_map.get(rid, {
                        "rule_id":              rid,
                        "verdict":              "spot_check",
                        "reason":               "no_response_from_model",
                        "corrected_confidence": "MEDIUM",
                    })
                    all_verdicts[rid] = res

                # Streaming write — commit batch immediately
                if not args.dry_run:
                    for rule in batch:
                        rid = rule["rule_id"]
                        res = all_verdicts[rid]
                        apply_verdict(
                            db, rid,
                            res.get("verdict", "spot_check"),
                            res.get("reason", ""),
                            res.get("corrected_confidence", "MEDIUM"),
                            args.model,
                            [], "",
                            args.dry_run,
                        )
                print("done")

        # ── Stage 3: Contradiction detection ─────────────────────────────────
        if not args.skip_claude:
            print("\nStage 3: Contradiction detection (grouped by sub_type)...")
            sub_type_groups: dict[str, list[dict]] = defaultdict(list)
            for rule in structurally_ok:
                sub_type_groups[rule.get("sub_type", "unknown")].append(rule)

            groups_checked = 0
            for sub_type, group_rules in sub_type_groups.items():
                if len(group_rules) < 2:
                    continue
                groups_checked += 1
                print(f"  sub_type={sub_type!r}  ({len(group_rules)} rules)...",
                      end=" ", flush=True)
                try:
                    contras = detect_contradictions(group_rules, args.model)
                except Exception:
                    contras = []
                all_contradictions.extend(contras)
                print(f"{len(contras)} contradiction(s)")

            print(f"  Groups checked      : {groups_checked}")
            print(f"  Contradictions found: {len(all_contradictions)} pair(s)")
        else:
            print("\nStage 3: Skipped (--skip-claude flag set)")

        # Build contradiction map for downgrade
        contra_map: dict[str, list[str]] = defaultdict(list)
        for c in all_contradictions:
            contra_map[c["rule_id_a"]].append(c["rule_id_b"])
            contra_map[c["rule_id_b"]].append(c["rule_id_a"])

        # Downgrade auto_approved → pending_human_review for contradicting rules
        if not args.dry_run and all_contradictions:
            print("  Applying contradiction downgrades...")
            for c in all_contradictions:
                for rid in [c["rule_id_a"], c["rule_id_b"]]:
                    db["interpretation_rules"].update_one(
                        {"rule_id": rid, "approval_status": "auto_approved"},
                        {"$set": {
                            "approval_status":          "pending_human_review",
                            "validation.verdict":        "spot_check",
                            "validation.flag_reason":    (
                                f"Contradicts: {', '.join(contra_map.get(rid,[]))}"
                            ),
                            "validation.contradiction_ids":     contra_map.get(rid, []),
                            "validation.contradiction_summary": c.get("contradiction_summary", ""),
                        }},
                    )

        # ── Stage 4: Write skipped-batch verdicts + final tally ──────────────
        print(f"\nStage 4: {'[DRY RUN] ' if args.dry_run else ''}Finalising verdicts...")
        for rule in rules:
            rid          = rule["rule_id"]
            verdict_info = all_verdicts.get(rid, {
                "verdict":              "spot_check",
                "reason":               "not_processed",
                "corrected_confidence": "MEDIUM",
            })
            verdict  = verdict_info.get("verdict", "spot_check")
            reason   = verdict_info.get("reason", "")
            conf     = verdict_info.get("corrected_confidence", "MEDIUM")
            contra_ids = contra_map.get(rid, [])

            # For streamed rules (Stage 2 non-skipped), read back actual status
            if not args.skip_claude and not args.dry_run and verdict != "structural_fail":
                doc = db["interpretation_rules"].find_one(
                    {"rule_id": rid}, {"approval_status": 1, "_id": 0}
                )
                actual = (doc or {}).get("approval_status", "pending_review")
                counters[actual] = counters.get(actual, 0) + 1
                if actual == "flagged":
                    rule["_reason"] = reason
                    flagged_rules.append(rule)
                continue

            # Structural fails and skip-claude path: write here
            if verdict == "approve" and contra_ids:
                verdict = "spot_check"
                reason  = f"Contradicts: {', '.join(contra_ids)}"
            contra_summary = next(
                (c.get("contradiction_summary","")
                 for c in all_contradictions
                 if c["rule_id_a"] == rid or c["rule_id_b"] == rid),
                ""
            )
            new_status = apply_verdict(
                db, rid, verdict, reason, conf,
                args.model, contra_ids, contra_summary, args.dry_run,
            )
            counters[new_status] = counters.get(new_status, 0) + 1
            if new_status == "flagged":
                rule["_reason"] = reason
                flagged_rules.append(rule)

            if args.dry_run:
                icon = {"auto_approved": "✓", "flagged": "⚑",
                        "rejected": "✗", "pending_human_review": "~"}.get(new_status, "?")
                msg  = f" [{reason}]" if reason else ""
                print(f"    {icon} {new_status:<28} {rid}{msg}")

        # ── Summary ───────────────────────────────────────────────────────────
        total = sum(counters.values())
        print(f"\n{'='*60}")
        print(f"{'[DRY RUN] ' if args.dry_run else ''}MUNDANE VALIDATION COMPLETE")
        print(f"{'='*60}")
        for status, count in sorted(counters.items(), key=lambda x: -x[1]):
            pct = f"{count/total*100:.0f}%" if total else "0%"
            print(f"  {status:<32} {count:>4}  ({pct})")
        print(f"  {'-'*46}")
        print(f"  {'Total':<32} {total:>4}")
        print(f"\n  Contradictions: {len(all_contradictions)} pair(s)")

        if old_schema_rules:
            print(f"\n  ℹ️  {len(old_schema_rules)} old-schema rule(s) (v1/v2 legacy) set to "
                  f"pending_human_review with reason 'old_schema_migration_pending'.\n"
                  f"  These require a separate schema migration — not content errors.")

        if not args.dry_run:
            print(
                "\n  auto_approved rules have approval_status='auto_approved' in MongoDB.\n"
                "  NOTE: The live backend queries approval_status='approved' only.\n"
                "  No rules reach live users until explicitly promoted to 'approved'\n"
                "  via co-founder sign-off. Review flagged/spot_check rules at\n"
                "  /admin/library → Rules Browser → filter: flagged / pending_human_review"
            )

        if args.report_path:
            write_report(
                args.report_path, counters,
                all_contradictions, flagged_rules[:30], rejected_rules,
            )

    finally:
        client.close()


if __name__ == "__main__":
    main()
