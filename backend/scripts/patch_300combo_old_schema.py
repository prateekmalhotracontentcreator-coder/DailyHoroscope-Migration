#!/usr/bin/env python3
"""
patch_300combo_old_schema.py
--------------------------------------------------------------------
Patches the 259 300 Combinations rules (Y044-Y300) that used the OLD
decode schema (results list + polarity) and ended up with empty
interpretation.detailed after ingest.

OLD schema fields → canonical KE schema:
  results (list of strings)   → interpretation.detailed (joined prose)
  special_notes (str)         → appended to interpretation.detailed
  polarity (str)              → claim_polarity
  conditions (list)           → condition (first element as dict, or composite)
  yoga_name + category        → used to build interpretation.summary

Source: re-reads the original decode JSON files for accurate field values.
Target: MongoDB horoscope_db.interpretation_rules, batch 300-combinations-v1-20260601

Run:
    python3 backend/scripts/patch_300combo_old_schema.py \
      --mongo-url "$MONGO_URL" --db-name horoscope_db

    # Dry run:
    python3 backend/scripts/patch_300combo_old_schema.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DECODE_FOLDER = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredCombinations_CC_Decode"
)
BATCH_ID = "300-combinations-v1-20260601"

# Files using OLD schema (results list instead of full_text)
OLD_SCHEMA_FILES = [
    "Combo_Y044-060_Rules.json",
    "Combo_Y061-070_Rules.json",
    "Combo_Y071-102_Rules_Part1.json",
    "Combo_Y071-102_Rules_Part2.json",
    "Combo_Y103-116_Rules.json",
    "Combo_Y117-128_Rules.json",
    "Combo_Y129-143_Rules.json",
    "Combo_Y144-153_Rules.json",
    "Combo_Y154-167_Rules.json",
    "Combo_Y168-180_Rules.json",
    "Combo_Y181-200_Rules.json",
    "Combo_Y201-221_Rules.json",
    "Combo_Y222-239_Rules.json",
    "Combo_Y240-263_Rules.json",
    "Combo_Y264-287_Rules.json",
    "Combo_Y288-300_Rules.json",
]


def polarity_map(raw_polarity: Any) -> str:
    """Map source polarity values to valid claim_polarity values."""
    p = str(raw_polarity or "").strip().lower()
    mapping = {
        "positive":   "positive",
        "auspicious": "positive",
        "negative":   "negative",
        "inauspicious": "negative",
        "mixed":      "mixed",
        "neutral":    "neutral",
        "conditional": "mixed",  # map conditional → mixed
    }
    return mapping.get(p, "neutral")


def build_interpretation(rule: dict[str, Any]) -> dict[str, str]:
    """
    Build interpretation.detailed and interpretation.summary from OLD schema fields.

    OLD schema:
      - results: list of short outcome strings
      - special_notes: additional context string (optional)
      - yoga_name: name of the yoga
      - category: yoga category
      - yoga_number: yoga number in book
    """
    results = rule.get("results") or []
    special_notes = str(rule.get("special_notes") or "").strip()
    yoga_name = str(rule.get("yoga_name") or "").strip()
    category = str(rule.get("category") or "").strip()

    # Build detailed: join results into readable list, append special_notes
    if isinstance(results, list) and results:
        results_str = "; ".join(str(r).strip() for r in results if str(r).strip())
    else:
        results_str = ""

    detailed_parts = []
    if yoga_name:
        detailed_parts.append(f"{yoga_name}.")
    if results_str:
        detailed_parts.append(f"Results: {results_str}.")
    if special_notes:
        detailed_parts.append(f"Notes: {special_notes}")

    detailed = " ".join(detailed_parts).strip()

    # Build summary: yoga_name + first 2 results
    if results_str:
        summary_results = "; ".join(str(r).strip() for r in results[:2] if str(r).strip())
        summary = f"{yoga_name}: {summary_results}." if yoga_name else summary_results
    else:
        summary = yoga_name or category or ""

    return {"detailed": detailed, "summary": summary[:500]}


def build_condition(rule: dict[str, Any]) -> dict[str, Any]:
    """
    Map conditions (list) → condition (dict).
    Uses first condition as primary; marks multi_condition if multiple exist.
    """
    conditions = rule.get("conditions") or []
    if not isinstance(conditions, list) or not conditions:
        rule_type = rule.get("type") or rule.get("rule_type") or "composite"
        return {"type": str(rule_type)}

    if len(conditions) == 1:
        cond = dict(conditions[0]) if isinstance(conditions[0], dict) else {"type": str(conditions[0])}
        return cond

    # Multiple conditions -- use first as primary, note it's composite
    primary = dict(conditions[0]) if isinstance(conditions[0], dict) else {"type": str(conditions[0])}
    primary["sub_conditions"] = [
        dict(c) if isinstance(c, dict) else {"type": str(c)}
        for c in conditions[1:]
    ]
    primary["operator"] = "AND"
    if not primary.get("type"):
        primary["type"] = "composite"
    return primary


def load_old_schema_rules() -> dict[str, dict[str, Any]]:
    """Load all OLD schema rules by rule_id from source JSON files."""
    rules_by_id: dict[str, dict[str, Any]] = {}
    for filename in OLD_SCHEMA_FILES:
        file_path = DECODE_FOLDER / filename
        if not file_path.exists():
            print(f"  [warn] File not found: {filename}")
            continue
        try:
            raw = json.loads(file_path.read_text(encoding="utf-8"))
            rules = raw.get("rules", raw) if isinstance(raw, dict) else raw
            for rule in rules:
                if isinstance(rule, dict) and rule.get("rule_id"):
                    rules_by_id[str(rule["rule_id"])] = rule
        except Exception as e:
            print(f"  [error] {filename}: {e}")
    return rules_by_id


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Patch 300 Combinations OLD schema rules.")
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("\n" + "=" * 60)
    print(f"Patch: 300 Combinations OLD schema rules")
    print(f"Batch: {BATCH_ID}")
    print(f"Mode:  {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("=" * 60 + "\n")

    # Load source rules
    print("Loading OLD schema rules from decode folder...")
    source_rules = load_old_schema_rules()
    print(f"  Loaded {len(source_rules)} rules from {len(OLD_SCHEMA_FILES)} files\n")

    if not args.dry_run:
        if not args.mongo_url:
            print("ERROR: --mongo-url required", file=sys.stderr)
            sys.exit(1)
        from pymongo import MongoClient
        client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=15000)
        db = client[args.db_name]

        # Fetch the 259 pending_review rules from this batch
        mongo_rules = list(db["interpretation_rules"].find(
            {"ingest_batch_id": BATCH_ID, "approval_status": "pending_review"},
            {"_id": 0, "rule_id": 1}
        ))
        mongo_rule_ids = {r["rule_id"] for r in mongo_rules}
        print(f"  MongoDB pending_review rules in batch: {len(mongo_rule_ids)}")
    else:
        # In dry run, use all old schema rule_ids
        mongo_rule_ids = set(source_rules.keys())
        print(f"  DRY RUN: processing {len(mongo_rule_ids)} rule_ids")

    # Build patches
    patched = 0
    skipped_no_source = 0
    patch_errors = 0

    now_ts = datetime.now(timezone.utc).isoformat()

    for rule_id in sorted(mongo_rule_ids):
        source = source_rules.get(rule_id)
        if not source:
            print(f"  [warn] {rule_id} -- no source rule found (skip)")
            skipped_no_source += 1
            continue

        # Build the interpretation from OLD schema
        interpretation = build_interpretation(source)

        # Build canonical condition from conditions list
        condition = build_condition(source)

        # Map polarity → claim_polarity
        raw_polarity = source.get("polarity") or source.get("claim_polarity") or ""
        claim_polarity = polarity_map(raw_polarity)

        # Build update doc
        update = {
            "interpretation": interpretation,
            "condition": condition,
            "claim_polarity": claim_polarity,
            "patched_at": now_ts,
            "patch_note": "old-schema-fix-v1: results+polarity+conditions mapped to canonical KE fields",
        }

        if args.dry_run:
            if patched < 5:
                print(f"\n  DRY RUN {rule_id}:")
                print(f"    interpretation.detailed: {interpretation['detailed'][:120]}")
                print(f"    interpretation.summary:  {interpretation['summary'][:80]}")
                print(f"    claim_polarity:          {claim_polarity}")
                print(f"    condition.type:          {condition.get('type')}")
            patched += 1
        else:
            try:
                result = db["interpretation_rules"].update_one(
                    {"rule_id": rule_id, "ingest_batch_id": BATCH_ID},
                    {"$set": update},
                )
                if result.matched_count:
                    patched += 1
                else:
                    print(f"  [warn] {rule_id} -- not found in MongoDB for update")
                    patch_errors += 1
            except Exception as e:
                print(f"  [error] {rule_id}: {e}")
                patch_errors += 1

    print(f"\n{'─'*60}")
    print(f"  Patched:                {patched}")
    print(f"  Skipped (no source):    {skipped_no_source}")
    print(f"  Errors:                 {patch_errors}")
    if args.dry_run:
        print(f"\n[DRY RUN] No writes made. Re-run without --dry-run to apply.")
    else:
        print(f"\nNEXT: Re-run validate_rules.py --batch-id {BATCH_ID}")
    print("=" * 60)

    if not args.dry_run and "client" in dir():
        client.close()


if __name__ == "__main__":
    main()
