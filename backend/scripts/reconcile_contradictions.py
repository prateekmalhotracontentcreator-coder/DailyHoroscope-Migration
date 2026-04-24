#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

import anthropic
from pymongo import MongoClient


SCRIPT_DIR = Path(__file__).resolve().parent
REPORTS_DIR = SCRIPT_DIR / "reports"
INPUT_CSV = REPORTS_DIR / "horoscope_db_contradictions.csv"
OUTPUT_CSV = REPORTS_DIR / "horoscope_db_contradictions_reconciled.csv"
MODEL_FALLBACK = "claude-haiku-4-5"
OUTPUT_FIELDS = [
    "pair_id",
    "rule_id_a",
    "status_a",
    "book_a",
    "chapter_a",
    "condition_a",
    "planet_a",
    "house_a",
    "interpretation_a",
    "rule_id_b",
    "status_b",
    "book_b",
    "chapter_b",
    "condition_b",
    "planet_b",
    "house_b",
    "interpretation_b",
    "contradiction_summary",
    "recommended_action",
    "codex_recommendation",
    "codex_reasoning",
    "final_action",
]
ALLOWED_ACTIONS = {"keep_a", "keep_b", "keep_both", "deprecate_both"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate first-pass contradiction recommendations.")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--model", default=MODEL_FALLBACK)
    return parser.parse_args()


def load_existing_export() -> list[dict[str, str]]:
    if not INPUT_CSV.exists():
        return []
    with INPUT_CSV.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def pair_key(rule_id_a: str, rule_id_b: str) -> tuple[str, str]:
    return tuple(sorted((rule_id_a, rule_id_b)))


def fetch_pairs_from_db(db) -> list[dict[str, str]]:
    rule_index: dict[str, dict[str, Any]] = {}
    cursor = db["interpretation_rules"].find(
        {"validation.contradiction_ids": {"$exists": True, "$ne": []}},
        {
            "_id": 0,
            "rule_id": 1,
            "approval_status": 1,
            "source": 1,
            "condition": 1,
            "interpretation": 1,
            "validation": 1,
        },
    )
    for rule in cursor:
        rule_index[rule["rule_id"]] = rule

    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    counter = 0
    for rule_id_a in sorted(rule_index):
        rule_a = rule_index[rule_id_a]
        contradiction_ids = sorted((rule_a.get("validation") or {}).get("contradiction_ids") or [])
        for rule_id_b in contradiction_ids:
            key = pair_key(rule_id_a, rule_id_b)
            if key in seen:
                continue
            seen.add(key)
            counter += 1
            rows.append(build_pair_row(f"pair-{counter:03d}", rule_a, rule_index.get(rule_id_b, {})))
    return rows


def build_pair_row(pair_id: str, rule_a: dict[str, Any], rule_b: dict[str, Any]) -> dict[str, str]:
    source_a = rule_a.get("source") or {}
    source_b = rule_b.get("source") or {}
    condition_a = rule_a.get("condition") or {}
    condition_b = rule_b.get("condition") or {}
    interpretation_a = rule_a.get("interpretation") or {}
    interpretation_b = rule_b.get("interpretation") or {}
    passages_a = interpretation_a.get("full_text_passages") or []
    passages_b = interpretation_b.get("full_text_passages") or []
    validation_a = rule_a.get("validation") or {}
    validation_b = rule_b.get("validation") or {}
    return {
        "pair_id": pair_id,
        "rule_id_a": rule_a.get("rule_id", ""),
        "status_a": rule_a.get("approval_status", ""),
        "book_a": source_a.get("primary", ""),
        "chapter_a": source_a.get("chapter", ""),
        "condition_a": condition_a.get("type", ""),
        "planet_a": condition_a.get("planet", ""),
        "house_a": str(condition_a.get("house", "")),
        "interpretation_a": first_text(passages_a),
        "rule_id_b": rule_b.get("rule_id", ""),
        "status_b": rule_b.get("approval_status", ""),
        "book_b": source_b.get("primary", ""),
        "chapter_b": source_b.get("chapter", ""),
        "condition_b": condition_b.get("type", ""),
        "planet_b": condition_b.get("planet", ""),
        "house_b": str(condition_b.get("house", "")),
        "interpretation_b": first_text(passages_b),
        "contradiction_summary": validation_a.get("contradiction_summary")
        or validation_b.get("contradiction_summary")
        or "",
        "recommended_action": "",
    }


def first_text(passages: list[dict[str, Any]]) -> str:
    if not passages:
        return ""
    return str(passages[0].get("text", "")).strip()


def merge_export_with_db(export_rows: list[dict[str, str]], db_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    if not export_rows:
        return db_rows
    db_map = {pair_key(row["rule_id_a"], row["rule_id_b"]): row for row in db_rows}
    merged: list[dict[str, str]] = []
    seen_keys: set[tuple[str, str]] = set()
    for export_row in export_rows:
        key = pair_key(export_row["rule_id_a"], export_row["rule_id_b"])
        seen_keys.add(key)
        fallback = db_map.get(key, {})
        row = dict(export_row)
        for field in OUTPUT_FIELDS:
            if field in {"codex_recommendation", "codex_reasoning", "final_action"}:
                continue
            if not row.get(field):
                row[field] = fallback.get(field, "")
        merged.append(row)
    for key, db_row in db_map.items():
        if key not in seen_keys:
            merged.append(db_row)
    return merged


def load_done_pair_ids() -> set[str]:
    if not OUTPUT_CSV.exists():
        return set()
    with OUTPUT_CSV.open(encoding="utf-8", newline="") as handle:
        return {row["pair_id"] for row in csv.DictReader(handle) if row.get("pair_id")}


def strip_json(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text


def ask_model(client: anthropic.Anthropic, model: str, row: dict[str, str]) -> tuple[str, str]:
    prompt = f"""You are a Vedic astrology Knowledge Engine editor reviewing conflicting interpretation rules.

Rule A:
  Source: {row['book_a']}, {row['chapter_a']}
  Condition: {row['planet_a']} in House {row['house_a']} — {row['condition_a']}
  Interpretation: {row['interpretation_a']}

Rule B:
  Source: {row['book_b']}, {row['chapter_b']}
  Condition: {row['planet_b']} in House {row['house_b']} — {row['condition_b']}
  Interpretation: {row['interpretation_b']}

These two rules conflict on the same condition. Recommend one of:
  keep_a     — Rule A is more accurate or authoritative; deprecate B
  keep_b     — Rule B is more accurate or authoritative; deprecate A
  keep_both  — Both are valid; they represent different classical schools or contexts
  deprecate_both — Neither is reliable; both should be removed

Respond in JSON:
{{
  "recommendation": "keep_a | keep_b | keep_both | deprecate_both",
  "reasoning": "one sentence"
}}"""
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text if response.content else "{}"
    try:
        parsed = json.loads(strip_json(text))
    except json.JSONDecodeError:
        return "keep_both", "Model response was not valid JSON; conservative fallback is keep_both."
    recommendation = str(parsed.get("recommendation", "keep_both"))
    reasoning = str(parsed.get("reasoning", "")).strip() or "No reasoning returned by model."
    if recommendation not in ALLOWED_ACTIONS:
        return "keep_both", f"Unexpected recommendation '{recommendation}'; conservative fallback is keep_both."
    return recommendation, reasoning


def open_writer(path: Path, append: bool):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a" if append else "w", encoding="utf-8", newline="")
    writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
    if not append:
        writer.writeheader()
    return handle, writer


def main() -> None:
    args = parse_args()
    client = MongoClient(args.mongo_url)
    try:
        db = client[args.db_name]
        export_rows = load_existing_export()
        db_rows = fetch_pairs_from_db(db)
        all_rows = merge_export_with_db(export_rows, db_rows)
        done_pair_ids = load_done_pair_ids() if args.resume else set()
        pending = [row for row in all_rows if row["pair_id"] not in done_pair_ids]

        print(f"Loaded {len(all_rows)} contradiction pairs.")
        if args.resume:
            print(f"Resume mode: {len(done_pair_ids)} already written, {len(pending)} remaining.")
        else:
            print(f"Fresh run: {len(pending)} pairs to process.")

        if not pending:
            print("Nothing to do.")
            return

        if args.dry_run:
            print("[DRY RUN] No CSV will be written.")

        anthropic_client = anthropic.Anthropic()
        handle = None
        writer = None
        if not args.dry_run:
            handle, writer = open_writer(OUTPUT_CSV, append=args.resume and OUTPUT_CSV.exists())

        try:
            total_batches = (len(pending) + 9) // 10
            for batch_index in range(total_batches):
                batch = pending[batch_index * 10 : (batch_index + 1) * 10]
                print(f"\nBatch {batch_index + 1}/{total_batches} ({len(batch)} pair(s))")
                output_rows: list[dict[str, str]] = []
                for row in batch:
                    try:
                        recommendation, reasoning = ask_model(anthropic_client, args.model, row)
                    except Exception as exc:
                        recommendation = "keep_both"
                        reasoning = f"Model call failed; conservative fallback is keep_both ({exc})."
                    output_row = dict(row)
                    output_row["codex_recommendation"] = recommendation
                    output_row["codex_reasoning"] = reasoning
                    output_row["final_action"] = ""
                    output_rows.append(output_row)
                    print(f"  {row['pair_id']}: {recommendation}")

                if writer is not None:
                    for output_row in output_rows:
                        writer.writerow(output_row)
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
