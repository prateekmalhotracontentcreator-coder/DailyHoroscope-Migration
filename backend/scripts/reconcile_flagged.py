#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from itertools import groupby
from pathlib import Path
from typing import Any

import anthropic
from pymongo import MongoClient


SCRIPT_DIR = Path(__file__).resolve().parent
REPORTS_DIR = SCRIPT_DIR / "reports"
OUTPUT_CSV = REPORTS_DIR / "horoscope_db_flagged_reconciled.csv"
MODEL_FALLBACK = "claude-haiku-4-5"
OUTPUT_FIELDS = [
    "rule_id",
    "book",
    "chapter",
    "batch_id",
    "condition_type",
    "planet",
    "house",
    "flag_reason",
    "interpretation_summary",
    "claude_recommendation",
    "claude_reasoning",
    "suggested_edit",
    "final_action",
]
ALLOWED_ACTIONS = {"approve", "needs_edit", "deprecate"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate first-pass recommendations for flagged rules.")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--science-id", default=None)
    parser.add_argument("--batch-id", default=None)
    parser.add_argument("--model", default=MODEL_FALLBACK)
    return parser.parse_args()


def fetch_flagged_rules(db, science_id: str | None, batch_id: str | None) -> list[dict[str, Any]]:
    query: dict[str, Any] = {"approval_status": "flagged"}
    if science_id:
        query["science_id"] = science_id
    if batch_id:
        query["source.batch_id"] = batch_id
    return list(
        db["interpretation_rules"]
        .find(
            query,
            {
                "_id": 0,
                "rule_id": 1,
                "source": 1,
                "condition": 1,
                "interpretation": 1,
                "validation": 1,
            },
        )
        .sort([("source.primary", 1), ("source.chapter", 1), ("rule_id", 1)])
    )


def interpretation_summary(rule: dict[str, Any]) -> str:
    interpretation = rule.get("interpretation") or {}
    passages = interpretation.get("full_text_passages") or []
    if passages:
        return str(passages[0].get("text", "")).strip()
    return str(interpretation.get("summary", "")).strip()


def load_done_rule_ids() -> set[str]:
    if not OUTPUT_CSV.exists():
        return set()
    with OUTPUT_CSV.open(encoding="utf-8", newline="") as handle:
        return {row["rule_id"] for row in csv.DictReader(handle) if row.get("rule_id")}


def strip_json(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    match = re.search(r"\[.*\]", text, re.DOTALL)
    return match.group(0) if match else text


def build_prompt(book: str, chapter: str, rules: list[dict[str, Any]]) -> str:
    blocks: list[str] = []
    for index, rule in enumerate(rules, start=1):
        condition = rule.get("condition") or {}
        validation = rule.get("validation") or {}
        blocks.append(
            f"{index}. rule_id={rule.get('rule_id','')}\n"
            f"   flag_reason={validation.get('flag_reason','')}\n"
            f"   condition_type={condition.get('type','')}\n"
            f"   interpretation={interpretation_summary(rule)}"
        )
    joined = "\n\n".join(blocks)
    return f"""You are a Vedic astrology Knowledge Engine editor reviewing flagged interpretation rules.
These rules were flagged during automated validation. Review each and recommend an action.

Source book: {book}
Chapter: {chapter}

For each rule below, recommend:
  approve      — rule is valid as-is; flag was overly cautious
  needs_edit   — rule has merit but needs the specific issue fixed (note what)
  deprecate    — rule is too vague, wrong, or not useful; should be removed

Rules to review:
{joined}

Respond in JSON array — one object per rule in the same order:
[
  {{
    "rule_id": "...",
    "recommendation": "approve | needs_edit | deprecate",
    "reasoning": "one sentence",
    "suggested_edit": "only if needs_edit — specific suggested change, else null"
  }}
]"""


def ask_model(client: anthropic.Anthropic, model: str, book: str, chapter: str, rules: list[dict[str, Any]]) -> list[dict[str, str]]:
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[{"role": "user", "content": build_prompt(book, chapter, rules)}],
    )
    text = response.content[0].text if response.content else "[]"
    try:
        parsed = json.loads(strip_json(text))
    except json.JSONDecodeError:
        parsed = []

    results: list[dict[str, str]] = []
    for index, rule in enumerate(rules):
        item = parsed[index] if index < len(parsed) and isinstance(parsed[index], dict) else {}
        recommendation = str(item.get("recommendation", "needs_edit"))
        if recommendation not in ALLOWED_ACTIONS:
            recommendation = "needs_edit"
        reasoning = str(item.get("reasoning", "")).strip() or "Model did not return valid structured reasoning."
        suggested_edit = item.get("suggested_edit")
        results.append(
            {
                "rule_id": rule.get("rule_id", ""),
                "recommendation": recommendation,
                "reasoning": reasoning,
                "suggested_edit": "" if suggested_edit in (None, "null") else str(suggested_edit),
            }
        )
    return results


def open_writer(path: Path, append: bool):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a" if append else "w", encoding="utf-8", newline="")
    writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
    if not append:
        writer.writeheader()
    return handle, writer


def chunked(items: list[dict[str, Any]], size: int) -> list[list[dict[str, Any]]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def main() -> None:
    args = parse_args()
    client = MongoClient(args.mongo_url)
    try:
        db = client[args.db_name]
        rules = fetch_flagged_rules(db, args.science_id, args.batch_id)
        done_rule_ids = load_done_rule_ids() if args.resume else set()
        if args.resume:
            rules = [rule for rule in rules if rule.get("rule_id") not in done_rule_ids]

        print(f"Flagged rules to process: {len(rules)}")
        if not rules:
            return

        anthropic_client = anthropic.Anthropic()
        handle = None
        writer = None
        if not args.dry_run:
            handle, writer = open_writer(OUTPUT_CSV, append=args.resume and OUTPUT_CSV.exists())

        try:
            grouped = groupby(rules, key=lambda item: ((item.get("source") or {}).get("primary", ""), (item.get("source") or {}).get("chapter", "")))
            for (book, chapter), group_iter in grouped:
                group_rules = list(group_iter)
                for batch_number, batch in enumerate(chunked(group_rules, 10), start=1):
                    print(f"\n{book} | {chapter} | batch {batch_number} | {len(batch)} rule(s)")
                    try:
                        decisions = ask_model(anthropic_client, args.model, book, chapter, batch)
                    except Exception as exc:
                        decisions = [
                            {
                                "rule_id": rule.get("rule_id", ""),
                                "recommendation": "needs_edit",
                                "reasoning": f"Model call failed; conservative fallback is needs_edit ({exc}).",
                                "suggested_edit": "",
                            }
                            for rule in batch
                        ]

                    rows: list[dict[str, str]] = []
                    for rule, decision in zip(batch, decisions):
                        source = rule.get("source") or {}
                        condition = rule.get("condition") or {}
                        validation = rule.get("validation") or {}
                        row = {
                            "rule_id": rule.get("rule_id", ""),
                            "book": source.get("primary", ""),
                            "chapter": source.get("chapter", ""),
                            "batch_id": source.get("batch_id", ""),
                            "condition_type": condition.get("type", ""),
                            "planet": condition.get("planet", ""),
                            "house": str(condition.get("house", "")),
                            "flag_reason": validation.get("flag_reason", ""),
                            "interpretation_summary": interpretation_summary(rule),
                            "claude_recommendation": decision["recommendation"],
                            "claude_reasoning": decision["reasoning"],
                            "suggested_edit": decision["suggested_edit"],
                            "final_action": "",
                        }
                        rows.append(row)
                        print(f"  {row['rule_id']}: {row['claude_recommendation']}")

                    if writer is not None:
                        for row in rows:
                            writer.writerow(row)
                        handle.flush()
        finally:
            if handle is not None:
                handle.close()

        if not args.dry_run:
            print(f"\nWrote reconciled CSV to {OUTPUT_CSV}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
