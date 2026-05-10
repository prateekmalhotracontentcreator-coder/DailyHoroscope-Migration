#!/usr/bin/env python3
"""
ingest_strategist_v1.py -- Lal Kitab Strategist module records

Sources:
  7. Lal Kitab_Career_The Strategist_Master Document (1).md
  The Strategist Module_LLM Specific Q&A_GAI.md
  Premium Report Generator (ID 1022 Narrative) + Full Module JSON Reconciliation Statement.md

science_id:  "lalkitab_strategist"
collection:  "knowledge_rules"
upsert key:  {id, science_id}
IDs covered: 701-1027, 651-675 (surrogates)

Usage:
  python3 scripts/ingest_strategist_v1.py --dry-run
  python3 scripts/ingest_strategist_v1.py --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCIENCE_ID = "lalkitab_strategist"
APPROVAL   = "pending_human_review"
MODULE_IDS = {933, 936, 937, 939, 1022, 1027}

SOURCE_MASTER = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/"
    "Remedies + The Strategist/"
    "7. Lal Kitab_Career_The Strategist_Master Document (1).md"
)
SOURCE_QA = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/"
    "Remedies + The Strategist/"
    "The Strategist Module_LLM Specific Q&A_GAI.md"
)
SOURCE_RECONCILIATION = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/"
    "Remedies + The Strategist/"
    "Premium Report Generator (ID 1022 Narrative) + Full Module JSON Reconciliation Statement.md"
)
SOURCE_PATCH_V2 = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/"
    "Remedies + The Strategist/"
    "The Strategist_Patch Work_Pivot, etc Fields_(850+)_V2.md"
)
SOURCE_STRATEGY_PATCH = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/"
    "Remedies + The Strategist/"
    "The Strategist_Missing Field__Strategy_.md"
)

REQUIRED_FIELDS = [
    "id", "science_id", "trigger_condition", "strategy",
    "decision_logic", "pivot_logic", "pivot_action",
    "kpi_target", "remedy_id", "approval_status",
]

# Only accept IDs in Strategist range (651-675 retired — replaced by 1201-1225 Universal Surrogates)
VALID_ID_RANGES = [(701, 1125), (1201, 1225)]

# Field aliases: master doc early batches use older names
FIELD_ALIASES = {
    "ke_logic_trigger":  "trigger_condition",
    "battle_strategy":   "strategy",
    "business_strategy": "strategy",
    "action":            "pivot_action",
    "pivot_reason":      "pivot_logic",
    "kpi":               "kpi_target",
    "primary_planet":    "command_planet",
    "focus_area":        "mission_objective",
    "scenario":          "mission_name",
    "battle_type":       "mission_objective",
    "decision_route":    "decision_logic",
    "forecast_window":   "trigger_condition",
}


def _unescape_markdown(text):
    """Normalise all markdown formatting artifacts before JSON parsing."""
    # Strip markdown bold markers (**text**) -- ID 900+ blocks use these
    text = re.sub(r"\*\*", "", text)
    # Unescape \\[ \\] -> [ ]
    text = text.replace("\\[", "[").replace("\\]", "]")
    # Unescape \\_ -> _
    text = text.replace("\\_", "_")
    # Unescape \\+ -> +
    text = text.replace("\\+", "+")
    # Unescape \\== -> ==
    text = text.replace("\\==", "==")
    # Unescape remaining markdown special chars invalid as JSON escapes
    for ch in (")", ">", "<", "-", "&", ".", "*", "#", "`", "="):
        text = text.replace("\\" + ch, ch)
    # Curly/smart quotes -> ASCII (using chr() to avoid encoding issues in source)
    text = text.replace(chr(0x2018), "'").replace(chr(0x2019), "'")
    text = text.replace(chr(0x201C), '"').replace(chr(0x201D), '"')
    # Trailing two-space markdown newlines
    text = re.sub(r"  \n", "\n", text)
    return text


def _clean_text(s):
    """Clean a single string value."""
    s = s.replace(chr(0x2018), "'").replace(chr(0x2019), "'")
    s = s.replace(chr(0x201C), '"').replace(chr(0x201D), '"')
    s = s.replace(chr(0x2013), "-").replace(chr(0x2014), "-")
    s = re.sub(r"\\\n", "", s)
    return s.strip()


def _extract_json_with_bracket_match(text):
    """Extract JSON arrays and objects using bracket-matching (handles nesting)."""
    results = []
    i = 0
    n = len(text)

    while i < n:
        if text[i] not in ('[', '{'):
            i += 1
            continue

        open_char = text[i]
        close_char = ']' if open_char == '[' else '}'
        depth = 0
        start = i

        for j in range(i, n):
            if text[j] == open_char:
                depth += 1
            elif text[j] == close_char:
                depth -= 1
                if depth == 0:
                    candidate = text[start:j+1]
                    try:
                        parsed = json.loads(candidate)
                        results.append((start, j+1, parsed))
                        i = j + 1
                        break
                    except json.JSONDecodeError:
                        pass
                    break
        else:
            i += 1
            continue
        if i <= start:
            i += 1

    return results


def _extract_json_blocks(text):
    """Extract all Strategist records from markdown source."""
    text = _unescape_markdown(text)
    records = []
    seen_ids = set()

    parsed_blocks = _extract_json_with_bracket_match(text)

    for _, _, obj in parsed_blocks:
        # Could be a list (array) or dict (single object)
        items = obj if isinstance(obj, list) else [obj]
        for item in items:
            if not isinstance(item, dict):
                continue
            rid = item.get("id")
            if rid is None:
                continue
            try:
                rid = int(rid)
            except (TypeError, ValueError):
                continue
            if rid in seen_ids:
                continue
            seen_ids.add(rid)
            records.append(item)

    return records


def _in_valid_range(rid):
    return any(lo <= rid <= hi for lo, hi in VALID_ID_RANGES)


def _normalise_record(r):
    """Apply field aliases, add metadata, coerce types."""
    out = {}
    for k, v in r.items():
        key = k.replace("\\", "").strip()
        key = FIELD_ALIASES.get(key, key)
        if isinstance(v, dict):
            # Promote sub-fields before flattening (IDs 800-950 embed strategy/pivot_action inside decision_logic)
            for sub_key in ("strategy", "pivot_action", "pivot_logic", "kpi_target"):
                if sub_key in v and sub_key not in out:
                    sv = v[sub_key]
                    out[sub_key] = _clean_text(sv) if isinstance(sv, str) else sv
            val = json.dumps(v)
        elif isinstance(v, str):
            val = _clean_text(v)
        else:
            val = v
        if key not in out:
            out[key] = val

    # Fallback: use mission_objective (from focus_area alias) as strategy if strategy still absent
    if "strategy" not in out and "mission_objective" in out:
        out["strategy"] = out["mission_objective"]

    out["science_id"]      = SCIENCE_ID
    out["approval_status"] = APPROVAL
    out["ingested_at"]     = datetime.now(timezone.utc).isoformat()

    for int_field in ("id", "remedy_id"):
        if int_field in out:
            try:
                out[int_field] = int(out[int_field])
            except (TypeError, ValueError):
                pass

    return out


def validate_batch(batch):
    errors = []
    for r in batch:
        rid = r.get("id")
        if rid in MODULE_IDS:
            continue
        missing = [f for f in REQUIRED_FIELDS if f not in r]
        if missing:
            errors.append({"id": rid, "missing": missing})
    return {"total": len(batch), "errors": len(errors), "detail": errors}


def load_records():
    all_records = {}

    for source in [SOURCE_QA, SOURCE_RECONCILIATION, SOURCE_PATCH_V2, SOURCE_STRATEGY_PATCH]:
        if not source.exists():
            print("[WARN] Source not found: {}".format(source), file=sys.stderr)
            continue

        text = source.read_text(encoding="utf-8", errors="replace")
        extracted = _extract_json_blocks(text)
        in_range = [r for r in extracted if _in_valid_range(int(r.get("id", 0)))]
        print("[INFO] {}: extracted {} raw, {} in Strategist range".format(
            source.name, len(extracted), len(in_range)))

        for r in in_range:
            rid = int(r.get("id", 0))
            if rid not in all_records:
                all_records[rid] = r
            else:
                # Merge: later file wins for non-empty fields
                existing = all_records[rid]
                for k, v in r.items():
                    if v and v != "" and k != "id":
                        existing[k] = v

    normalised = [_normalise_record(r) for r in all_records.values()]
    normalised.sort(key=lambda r: r.get("id", 0))
    return normalised


def main():
    parser = argparse.ArgumentParser(description="Ingest Strategist records")
    parser.add_argument("--mongo-url", default="")
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument("--dry-run", action="store_true", default=False)
    args = parser.parse_args()

    records = load_records()
    print("[INFO] Total unique records: {}".format(len(records)))

    validation = validate_batch(records)
    print("[INFO] Gate 0: {} records, {} errors".format(
        validation["total"], validation["errors"]))
    if validation["errors"]:
        for e in validation["detail"][:20]:
            print("  [WARN] ID {}: missing {}".format(e["id"], e["missing"]))

    if args.dry_run:
        print("[DRY-RUN] Sample record (first):")
        if records:
            print(json.dumps(records[0], indent=2, default=str))
        # Show a fully-formed record if any
        complete = [r for r in records if all(f in r for f in REQUIRED_FIELDS)]
        if complete:
            print("[DRY-RUN] Sample COMPLETE record:")
            print(json.dumps(complete[0], indent=2, default=str))
        print("[DRY-RUN] Would upsert {} records into knowledge_rules".format(len(records)))
        print("[DRY-RUN] Complete (all required fields): {}/{}".format(len(complete), len(records)))
        return

    if not args.mongo_url:
        print("[ERROR] --mongo-url required for upload", file=sys.stderr)
        sys.exit(1)

    from pymongo import MongoClient, UpdateOne

    client = MongoClient(args.mongo_url)
    db = client[args.db_name]
    coll = db.knowledge_rules

    ops = [
        UpdateOne(
            {"id": r["id"], "science_id": SCIENCE_ID},
            {"$set": r},
            upsert=True,
        )
        for r in records
    ]

    if ops:
        result = coll.bulk_write(ops, ordered=False)
        print("[OK] Upserted {} new, modified {} existing".format(
            result.upserted_count, result.modified_count))
    else:
        print("[WARN] No records to upsert")

    client.close()


if __name__ == "__main__":
    main()
