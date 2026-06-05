#!/usr/bin/env python3
"""
ingest_from_json_folder.py
--------------------------------------------------------------------
Generic KE decode-folder ingest script.
Reads all *_Rules*.json files from a given folder and upserts them
into MongoDB horoscope_db.interpretation_rules.

Handles both JSON formats:
  - List format: [...]
  - Dict wrapper: {"rules": [...], "metadata": {...}}

Run sequence (mandatory):
  Step 1 -- Dry run + save JSON (review before any DB writes):
    python3 backend/scripts/ingest_from_json_folder.py \
      --folder "/path/to/Book_CC_Decode" \
      --book "300 Combinations" \
      --batch-id "300-combinations-v1-20260531" \
      --db-name horoscope_db \
      --dry-run --save backend/scripts/300_combinations_rules.json

  Step 2 -- Review saved JSON (spot-check first + last rule per file)

  Step 3 -- Upload to MongoDB:
    python3 backend/scripts/ingest_from_json_folder.py \
      --folder "/path/to/Book_CC_Decode" \
      --book "300 Combinations" \
      --batch-id "300-combinations-v1-20260531" \
      --mongo-url "$MONGO_URL" --db-name horoscope_db \
      --upload backend/scripts/300_combinations_rules.json

  Step 4 -- Validate:
    python3 backend/scripts/validate_rules.py \
      --batch-id 300-combinations-v1-20260531 \
      --mongo-url "$MONGO_URL" --db-name horoscope_db

Schema notes:
  - approval_status: "pending_review" (NOT "pending_human_review" -- validate_rules.py queries pending_review)
  - source.batch_id is set for validate_rules.py --batch-id filter
  - full_text -> interpretation.detailed if interpretation.detailed is absent
  - summary   -> interpretation.summary  if interpretation.summary  is absent
  - active: false rules are skipped (not inserted)
  - Rules without rule_id are rejected (logged, not inserted)
  - Duplicate rule_ids (ordered=False) are skipped silently
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SKIP_FILENAME_FRAGMENTS = ("Contradictions", "NLM_Extract", "OCR", "_archive")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generic KE decode-folder ingest script."
    )
    parser.add_argument(
        "--folder", required=True,
        help="Path to decode folder containing *_Rules*.json files",
    )
    parser.add_argument(
        "--book", required=True,
        help="Human-readable book name (stored in source_book field)",
    )
    parser.add_argument(
        "--batch-id", required=True,
        help="Unique batch identifier (used for idempotency and validate_rules.py)",
    )
    parser.add_argument(
        "--mongo-url", default=os.getenv("MONGO_URL"),
        help="MongoDB connection string",
    )
    parser.add_argument(
        "--db-name", default="horoscope_db",
        help="MongoDB database name",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Build rule docs, print summary, save JSON -- write nothing to MongoDB",
    )
    parser.add_argument(
        "--save", metavar="PATH",
        help="Save built rules to JSON file (use with --dry-run to review before upload)",
    )
    parser.add_argument(
        "--upload", metavar="PATH",
        help="Upload rules from a previously saved JSON file to MongoDB",
    )
    parser.add_argument(
        "--batch-size", type=int, default=200,
        help="Insert batch size (reduce to 50 if timeouts occur)",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# File loading
# ---------------------------------------------------------------------------

def load_rules_from_file(path: Path) -> list[dict[str, Any]]:
    """Load rules from a JSON file. Handles list and dict-wrapper formats."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"  [error] JSON parse error in {path.name}: {exc}", file=sys.stderr)
        return []

    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        rules = raw.get("rules", [])
        if isinstance(rules, list):
            return rules
        print(f"  [warn] {path.name}: 'rules' key is not a list -- skipped", file=sys.stderr)
        return []
    print(f"  [warn] {path.name}: unexpected JSON root type {type(raw).__name__} -- skipped", file=sys.stderr)
    return []


def find_rule_files(folder: Path) -> list[Path]:
    """Return all *_Rules*.json files in folder, sorted, excluding skip fragments."""
    candidates = sorted(folder.rglob("*Rules*.json"))
    result = []
    for f in candidates:
        skip = False
        for fragment in SKIP_FILENAME_FRAGMENTS:
            if fragment in f.name or fragment in str(f.parent):
                skip = True
                break
        if skip:
            print(f"  [skip] {f.name}")
            continue
        result.append(f)
    return result


# ---------------------------------------------------------------------------
# Schema mapping helpers
# ---------------------------------------------------------------------------

def map_interpretation(rule: dict[str, Any]) -> dict[str, Any]:
    """
    Map full_text / summary → interpretation.detailed / interpretation.summary
    if the interpretation dict is absent or empty.

    validate_rules.py (Stage 2) reads interpretation.detailed for AI review.
    """
    interp = rule.get("interpretation")
    if not isinstance(interp, dict):
        interp = {}

    if interp.get("detailed") and interp.get("summary"):
        rule["interpretation"] = interp
        return rule  # already correctly populated

    full_text     = str(rule.get("full_text") or "").strip()
    summary       = str(rule.get("summary") or "").strip()
    title         = str(rule.get("title") or "").strip()
    yoga_name     = str(rule.get("yoga_name") or "").strip()
    result        = rule.get("result")
    claim         = rule.get("claim")
    # OLD schema: results is a list of short outcome strings
    results_list  = rule.get("results")
    special_notes = str(rule.get("special_notes") or "").strip()

    # detailed: preference order:
    #   1. full_text (new schema)
    #   2. claim text (BPHS schema A1/A2)
    #   3. result string (BPHS schema C)
    #   4. results list + special_notes (old 300 Combinations / older book schema)
    #   5. summary fallback
    if not interp.get("detailed"):
        if full_text:
            interp["detailed"] = full_text
        elif isinstance(claim, dict) and claim.get("text"):
            interp["detailed"] = str(claim["text"]).strip()
        elif isinstance(claim, str) and claim.strip():
            interp["detailed"] = claim.strip()
        elif isinstance(result, str) and result.strip() and not result.strip().startswith("{"):
            interp["detailed"] = result.strip()
        elif isinstance(results_list, list) and results_list:
            # Old schema: join list items into prose
            results_str = "; ".join(str(r).strip() for r in results_list if str(r).strip())
            parts = []
            if yoga_name:
                parts.append(f"{yoga_name}.")
            if results_str:
                parts.append(f"Results: {results_str}.")
            if special_notes:
                parts.append(f"Notes: {special_notes}")
            interp["detailed"] = " ".join(parts).strip() or summary
        else:
            interp["detailed"] = summary

    # summary: prefer summary; fall back to yoga_name + first 2 results; then title; then first 300 chars
    if not interp.get("summary"):
        if summary:
            interp["summary"] = summary
        elif isinstance(results_list, list) and results_list:
            top = "; ".join(str(r).strip() for r in results_list[:2] if str(r).strip())
            interp["summary"] = f"{yoga_name}: {top}." if yoga_name else top
        elif title:
            interp["summary"] = title
        elif yoga_name:
            interp["summary"] = yoga_name
        else:
            interp["summary"] = interp.get("detailed", "")[:300]

    rule["interpretation"] = interp
    return rule


def ensure_condition_dict(rule: dict[str, Any]) -> dict[str, Any]:
    """
    Ensure rule has a 'condition' dict (singular).
    If only 'conditions' (list) exists, use conditions[0] as the condition.
    validate_rules.py structural check requires condition to be a non-empty dict.
    """
    if isinstance(rule.get("condition"), dict) and rule["condition"]:
        return rule

    conditions = rule.get("conditions", [])
    if isinstance(conditions, list) and conditions and isinstance(conditions[0], dict):
        rule["condition"] = conditions[0]
    else:
        # Synthetic fallback for general-principle / engine-spec rules
        rule_type = rule.get("type") or rule.get("rule_type") or "general_principle"
        rule["condition"] = {"type": str(rule_type)}

    return rule


def inject_ingest_fields(
    rule: dict[str, Any],
    batch_id: str,
    book_name: str,
    source_file: str,
    now: str,
) -> dict[str, Any]:
    """
    Inject standard ingest-time fields.
    Preserves all source fields -- only overwrites the tracked ingest fields.
    """
    rule["approval_status"]  = "pending_review"   # L1: NOT pending_human_review
    rule["ingest_batch_id"]  = batch_id
    rule["source_book"]      = book_name
    rule["source_file"]      = source_file
    rule["ingested_at"]      = now
    rule["active"]           = rule.get("active", True)

    # OLD schema: 'polarity' → 'claim_polarity' (if claim_polarity not already set)
    if not rule.get("claim_polarity") and rule.get("polarity"):
        _polarity_map = {
            "positive": "positive", "auspicious": "positive",
            "negative": "negative", "inauspicious": "negative",
            "mixed": "mixed", "conditional": "mixed", "neutral": "neutral",
        }
        raw_pol = str(rule["polarity"]).strip().lower()
        rule["claim_polarity"] = _polarity_map.get(raw_pol, "neutral")

    # source.batch_id -- validate_rules.py --batch-id filter uses source.batch_id
    source = rule.get("source")
    if not isinstance(source, dict):
        source = {}
    source["batch_id"] = batch_id
    rule["source"] = source

    return rule


# ---------------------------------------------------------------------------
# Core build
# ---------------------------------------------------------------------------

def build_rule_docs(
    folder: Path,
    batch_id: str,
    book_name: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """
    Scan folder for *_Rules*.json files, load, filter, inject fields.
    Returns (docs_ready_for_insert, stats_dict).
    """
    rule_files = find_rule_files(folder)
    if not rule_files:
        print(f"[warn] No *_Rules*.json files found in {folder}", file=sys.stderr)
        return [], {}

    now = datetime.now(timezone.utc).isoformat()
    all_docs: list[dict[str, Any]] = []
    stats: dict[str, Any] = {
        "files_found": len(rule_files),
        "files_loaded": 0,
        "total_raw": 0,
        "total_inactive": 0,
        "total_missing_rule_id": 0,
        "total_duplicate_in_folder": 0,
        "total_ready": 0,
        "per_file": [],
        "errors": [],
    }
    seen_ids: dict[str, str] = {}  # rule_id -> first_seen_filename

    for file_path in rule_files:
        rules = load_rules_from_file(file_path)
        basename = file_path.name
        file_stats = {"file": basename, "raw": len(rules), "inserted": 0, "inactive": 0, "no_id": 0, "dup_folder": 0}

        valid_in_file = 0
        for rule in rules:
            if not isinstance(rule, dict):
                continue
            stats["total_raw"] += 1

            # Skip inactive
            if rule.get("active") is False:
                stats["total_inactive"] += 1
                file_stats["inactive"] += 1
                continue

            # Validate rule_id
            rid = rule.get("rule_id")
            if not rid:
                stats["total_missing_rule_id"] += 1
                file_stats["no_id"] += 1
                stats["errors"].append({"file": basename, "issue": "missing_rule_id"})
                continue

            # Cross-file dedup within this ingest run
            if rid in seen_ids:
                stats["total_duplicate_in_folder"] += 1
                file_stats["dup_folder"] += 1
                print(f"  [dup] rule_id {rid} in {basename} already seen in {seen_ids[rid]} -- skipped")
                continue
            seen_ids[rid] = basename

            # Schema mapping
            doc = dict(rule)
            doc = map_interpretation(doc)
            doc = ensure_condition_dict(doc)
            doc = inject_ingest_fields(doc, batch_id, book_name, basename, now)

            all_docs.append(doc)
            valid_in_file += 1

        file_stats["inserted"] = valid_in_file
        stats["files_loaded"] += 1
        stats["per_file"].append(file_stats)
        print(f"  [loaded] {basename}: {valid_in_file} active rules")

    stats["total_ready"] = len(all_docs)
    return all_docs, stats


# ---------------------------------------------------------------------------
# MongoDB helpers
# ---------------------------------------------------------------------------

def batch_already_imported(client: Any, db_name: str, batch_id: str) -> bool:
    """Return True if this batch_id was already successfully imported (idempotency)."""
    return (
        client[db_name]["import_batches"].find_one(
            {"batch_id": batch_id, "import_status": "imported"},
            {"batch_id": 1},
        )
        is not None
    )


def upload_rules(
    all_docs: list[dict[str, Any]],
    mongo_url: str,
    db_name: str,
    batch_id: str,
    book_name: str,
    batch_size: int,
    files_loaded: int,
) -> None:
    """Insert docs into MongoDB. Duplicate rule_ids are skipped silently."""
    try:
        from pymongo import MongoClient
        from pymongo.errors import BulkWriteError
    except ImportError:
        print("ERROR: pymongo not installed. Run: pip install pymongo", file=sys.stderr)
        sys.exit(1)

    client = MongoClient(mongo_url, serverSelectionTimeoutMS=15000)
    db = client[db_name]

    # Idempotency check
    if batch_already_imported(client, db_name, batch_id):
        print(f"\nBatch '{batch_id}' already recorded as imported. Exiting (idempotent).")
        client.close()
        sys.exit(0)

    total_inserted  = 0
    total_dups      = 0
    total_errors    = 0

    print(f"\nInserting {len(all_docs)} documents in batches of {batch_size}...")
    for i in range(0, len(all_docs), batch_size):
        chunk = all_docs[i : i + batch_size]
        batch_num = i // batch_size + 1
        try:
            result = db["interpretation_rules"].insert_many(chunk, ordered=False)
            total_inserted += len(result.inserted_ids)
            print(f"  [batch {batch_num}] {len(result.inserted_ids)} inserted")
        except BulkWriteError as bwe:
            inserted_in_batch = bwe.details.get("nInserted", 0)
            total_inserted += inserted_in_batch
            write_errors = bwe.details.get("writeErrors", [])
            dups     = sum(1 for e in write_errors if e.get("code") == 11000)
            non_dups = len(write_errors) - dups
            total_dups   += dups
            total_errors += non_dups
            print(f"  [batch {batch_num}] {inserted_in_batch} inserted, {dups} dupes skipped"
                  + (f", {non_dups} errors" if non_dups else ""))
            if non_dups:
                for err in write_errors[:3]:
                    if err.get("code") != 11000:
                        print(f"    ERROR doc: {err.get('keyValue')}")

    now_ts = datetime.now(timezone.utc).isoformat()

    # Write import_batches record
    db["import_batches"].insert_one({
        "batch_id":          batch_id,
        "source_book":       book_name,
        "import_status":     "imported",
        "rules_inserted":    total_inserted,
        "duplicates_skipped": total_dups,
        "errors":            total_errors,
        "files_processed":   files_loaded,
        "timestamp":         now_ts,
    })

    print(f"\n{'─'*60}")
    print(f"  Inserted:         {total_inserted}")
    print(f"  Duplicates:       {total_dups}")
    print(f"  Errors:           {total_errors}")
    print(f"  import_batches:   {batch_id} recorded")
    print(f"{'─'*60}")
    print(f"\nNEXT: Run validate_rules.py --batch-id {batch_id}")

    client.close()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()

    if not args.dry_run and not args.upload:
        # Default mode: build + upload in one step (no save)
        pass  # handled below

    folder_path = Path(args.folder).expanduser().resolve()
    if not folder_path.exists() or not folder_path.is_dir():
        print(f"ERROR: folder does not exist: {folder_path}", file=sys.stderr)
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"Book:       {args.book}")
    print(f"Batch ID:   {args.batch_id}")
    print(f"Folder:     {folder_path}")
    print(f"DB:         {args.db_name}")
    mode = "DRY RUN" if args.dry_run else ("UPLOAD from JSON" if args.upload else "LIVE")
    print(f"Mode:       {mode}")
    print(f"{'='*60}\n")

    # ── UPLOAD from previously saved JSON ─────────────────────────────────────
    if args.upload:
        if not args.mongo_url:
            print("ERROR: --mongo-url required for upload", file=sys.stderr)
            sys.exit(1)
        upload_path = Path(args.upload)
        if not upload_path.exists():
            print(f"ERROR: saved JSON not found: {upload_path}", file=sys.stderr)
            sys.exit(1)
        all_docs = json.loads(upload_path.read_text(encoding="utf-8"))
        print(f"Loaded {len(all_docs)} rules from {upload_path}")
        upload_rules(all_docs, args.mongo_url, args.db_name, args.batch_id,
                     args.book, args.batch_size, 0)
        return

    # ── BUILD rule docs from folder ────────────────────────────────────────────
    print("Scanning and loading rule files...")
    all_docs, stats = build_rule_docs(folder_path, args.batch_id, args.book)

    print(f"\n{'─'*60}")
    print(f"  Files scanned:        {stats.get('files_found', 0)}")
    print(f"  Files loaded:         {stats.get('files_loaded', 0)}")
    print(f"  Total rules raw:      {stats.get('total_raw', 0)}")
    print(f"  Inactive (skipped):   {stats.get('total_inactive', 0)}")
    print(f"  Missing rule_id:      {stats.get('total_missing_rule_id', 0)}")
    print(f"  Folder duplicates:    {stats.get('total_duplicate_in_folder', 0)}")
    print(f"  Ready to insert:      {stats.get('total_ready', 0)}")
    print(f"{'─'*60}")

    if stats.get("errors"):
        print(f"\n  ⚠  {len(stats['errors'])} rules rejected (missing rule_id):")
        for e in stats["errors"][:5]:
            print(f"    {e['file']}")

    if not all_docs:
        print("\nNo rules to ingest. Exiting.")
        sys.exit(0)

    # ── DRY RUN ───────────────────────────────────────────────────────────────
    if args.dry_run:
        print("\n--- Sample documents (first 3) ---")
        for i, doc in enumerate(all_docs[:3]):
            preview = {k: v for k, v in doc.items() if k in (
                "rule_id", "approval_status", "source_book", "ingest_batch_id",
                "source_file", "ingested_at", "active", "science_id", "claim_polarity",
            )}
            interp = doc.get("interpretation") or {}
            preview["interpretation.detailed_preview"] = str(interp.get("detailed", ""))[:120]
            preview["interpretation.summary_preview"]  = str(interp.get("summary", ""))[:80]
            print(f"\n  Sample {i+1} (rule_id={doc['rule_id']}):")
            print(f"    {json.dumps(preview, indent=4, ensure_ascii=False)}")

        if args.save and all_docs:
            save_path = Path(args.save)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_text(
                json.dumps(all_docs, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            print(f"\n✅ Saved {len(all_docs)} rules → {save_path}")
        elif args.save and not all_docs:
            print("\n⚠  No rules built -- nothing saved.")

        print(f"\n[DRY RUN] No writes made. Review saved JSON, then re-run with:")
        print(f"  --upload {args.save or 'PATH'} --mongo-url \"$MONGO_URL\"")
        return

    # ── LIVE single-step (no --upload, no --dry-run) ───────────────────────────
    if not args.mongo_url:
        print("ERROR: --mongo-url not provided and MONGO_URL env var not set.", file=sys.stderr)
        sys.exit(1)

    if args.save:
        save_path = Path(args.save)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(
            json.dumps(all_docs, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"\n✅ Saved {len(all_docs)} rules → {save_path}")

    upload_rules(all_docs, args.mongo_url, args.db_name, args.batch_id,
                 args.book, args.batch_size, stats.get("files_loaded", 0))


if __name__ == "__main__":
    main()
