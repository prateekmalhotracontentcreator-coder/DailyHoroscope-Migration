#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader
from pymongo import MongoClient
from pymongo.errors import BulkWriteError


SCRIPT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SCRIPT_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from extract_book import ExtractionArgs, extract_rules, parse_categories


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "book"


def make_batch_id(book: str, chapter_index: int) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", book.lower()).strip("-")[:20].rstrip("-")
    date = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"{slug}_{chapter_index:03d}_{date}"


def extract_text_from_pdf(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(pages)


def run_extraction(
    text: str,
    book: str,
    chapter_name: str,
    batch_id: str,
    config: dict,
    output_path: Path,
    report_path: Path,
) -> tuple[dict, str]:
    tmp_path: Path | None = None
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    try:
        args = ExtractionArgs(
            input_path=tmp_path,
            book=book,
            voice=config.get("voice", "classical"),
            categories=parse_categories(config.get("categories", "general")),
            output_path=output_path,
            report_path=report_path,
            science_id=config.get("science_id", "vedic_astrology"),
            batch_id=batch_id,
            chapter=chapter_name,
            max_rules=config.get("max_rules_per_chapter", 100),
            min_words=config.get("min_words", 45),
            paraphrase_mode=config.get("paraphrase_mode", "openai"),
            model=os.getenv("EXTRACT_BOOK_CLAUDE_MODEL", "claude-sonnet-4-6"),
        )
        payload, report = extract_rules(args)
        return payload, report
    finally:
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)


def batch_already_imported(client: MongoClient, db_name: str, batch_id: str) -> bool:
    return client[db_name]["import_batches"].find_one(
        {"batch_id": batch_id, "import_status": "imported"},
        {"batch_id": 1},
    ) is not None


def insert_batch(
    client: MongoClient,
    db_name: str,
    payload: dict,
    batch_id: str,
    dry_run: bool = False,
) -> dict:
    db = client[db_name]
    rule_docs = [{key: value for key, value in rule.items() if key != "_extraction_meta"} for rule in payload.get("rules", [])]

    rules_imported = 0
    duplicate_count = 0
    error_count = 0

    if not dry_run and rule_docs:
        try:
            result = db["interpretation_rules"].insert_many(rule_docs, ordered=False)
            rules_imported = len(result.inserted_ids)
        except BulkWriteError as bwe:
            rules_imported = bwe.details.get("nInserted", 0)
            write_errors = bwe.details.get("writeErrors", [])
            duplicate_count = sum(1 for error in write_errors if error.get("code") == 11000)
            error_count = len(write_errors) - duplicate_count

    stats = payload.get("stats", {})
    timestamp = datetime.now(timezone.utc).isoformat()
    batch_doc = {
        "batch_id": batch_id,
        "source_book": payload.get("source_book", ""),
        "import_status": "imported" if not dry_run else "staged",
        "approval_status": "pending_review",
        "file_name": None,
        "rules_submitted": len(rule_docs),
        "rules_imported": rules_imported,
        "duplicate_count": duplicate_count,
        "conflict_count": 0,
        "error_count": error_count,
        "index_refreshed": False,
        "notes": f"Batch-ingested via batch_ingest.py. Candidate blocks: {stats.get('candidate_blocks', 0)}",
        "created_at": timestamp,
        "updated_at": timestamp,
    }

    if not dry_run:
        db["import_batches"].update_one(
            {"batch_id": batch_id},
            {"$setOnInsert": batch_doc},
            upsert=True,
        )

    return {
        "rules_submitted": len(rule_docs),
        "rules_imported": rules_imported,
        "duplicate_count": duplicate_count,
        "error_count": error_count,
    }


def process_book(config: dict, books_dir: Path, client: MongoClient, args) -> dict:
    book_title = config["book"]
    chapters = config.get("chapters", [])
    output_dir = Path(args.output_dir) / slugify(book_title) if args.output_dir else None
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'=' * 60}")
    print(f"Book  : {book_title}")
    print(f"Chapters: {len(chapters)}  |  Dry run: {args.dry_run}")
    print(f"{'=' * 60}")

    totals = {"submitted": 0, "imported": 0, "duplicates": 0, "errors": 0, "skipped": 0}

    for i, chapter in enumerate(chapters, start=1):
        batch_id = make_batch_id(book_title, i)
        chapter_name = chapter.get("name", f"Chapter {i}")
        pdf_file = books_dir / chapter["file"]

        print(f"\n  [{i}/{len(chapters)}] {chapter_name}")

        if not pdf_file.exists():
            print(f"  PDF not found: {pdf_file} - skipping")
            totals["errors"] += 1
            continue

        if not args.force and not args.dry_run:
            if batch_already_imported(client, args.db_name, batch_id):
                print(f"  Already imported ({batch_id}) - skipping")
                totals["skipped"] += 1
                continue

        chapter_config = {**config}
        if "categories" in chapter:
            chapter_config["categories"] = chapter["categories"]

        out_path: Path | None = None
        rpt_path: Path | None = None
        try:
            text = extract_text_from_pdf(pdf_file)
            if not text.strip():
                print("  No text extracted from PDF - skipping")
                totals["errors"] += 1
                continue

            if output_dir:
                out_path = output_dir / f"{batch_id}.json"
                rpt_path = output_dir / f"{batch_id}_report.md"
            else:
                out_path = Path(tempfile.mktemp(suffix=".json"))
                rpt_path = Path(tempfile.mktemp(suffix=".md"))

            payload, _ = run_extraction(text, book_title, chapter_name, batch_id, chapter_config, out_path, rpt_path)
            rule_count = len(payload.get("rules", []))
            print(f"  -> Extracted {rule_count} rules")

            stats = insert_batch(client, args.db_name, payload, batch_id, dry_run=args.dry_run)
            action = "Would insert" if args.dry_run else "Inserted"
            print(
                f"  -> {action}: {stats['rules_imported']}/{stats['rules_submitted']} "
                f"({stats['duplicate_count']} dupes, {stats['error_count']} errors)"
            )

            totals["submitted"] += stats["rules_submitted"]
            totals["imported"] += stats["rules_imported"]
            totals["duplicates"] += stats["duplicate_count"]
            totals["errors"] += stats["error_count"]

            if not output_dir:
                out_path.unlink(missing_ok=True)
                rpt_path.unlink(missing_ok=True)
        except Exception as exc:
            print(f"  Error: {exc}")
            totals["errors"] += 1
            if not output_dir:
                if out_path is not None:
                    out_path.unlink(missing_ok=True)
                if rpt_path is not None:
                    rpt_path.unlink(missing_ok=True)

    return totals


def parse_cli_args():
    parser = argparse.ArgumentParser(description="Batch-ingest chapter-wise OCR PDFs into Knowledge Engine rule batches.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--master")
    group.add_argument("--config")
    parser.add_argument("--books-dir")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", required=True)
    parser.add_argument("--output-dir")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.config and not args.books_dir:
        parser.error("--books-dir is required when using --config")
    return args


def main():
    args = parse_cli_args()
    client = MongoClient(args.mongo_url)

    grand_totals = {"submitted": 0, "imported": 0, "duplicates": 0, "errors": 0, "skipped": 0}

    if args.master:
        master = load_json(Path(args.master).expanduser().resolve())
        books = master.get("books", [])
        print(f"\nMaster run: {len(books)} book(s) queued")

        for entry in books:
            config_path = Path(entry["config"]).expanduser().resolve()
            books_dir = Path(entry["books_dir"]).expanduser().resolve()
            config = load_json(config_path)
            totals = process_book(config, books_dir, client, args)
            for key in grand_totals:
                grand_totals[key] += totals[key]
    else:
        config = load_json(Path(args.config).expanduser().resolve())
        books_dir = Path(args.books_dir).expanduser().resolve()
        totals = process_book(config, books_dir, client, args)
        grand_totals = totals

    print(f"\n{'=' * 60}")
    print(f"{'[DRY RUN] ' if args.dry_run else ''}ALL DONE")
    print(f"  Submitted  : {grand_totals['submitted']}")
    print(f"  Imported   : {grand_totals['imported']}")
    print(f"  Duplicates : {grand_totals['duplicates']}")
    print(f"  Errors     : {grand_totals['errors']}")
    print(f"  Skipped    : {grand_totals['skipped']}")
    if not args.dry_run and grand_totals["imported"] > 0:
        print("\n  All rules are in MongoDB with approval_status='pending_review'.")
        print("  Open /admin/library -> Import Batches to review and approve in one session.")
    client.close()


if __name__ == "__main__":
    main()
