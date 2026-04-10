# Codex Brief — Commission I: Batch Book Ingest Automation

> To: Codex  
> From: EverydayHoroscope / Temple Team  
> Type: Operations tooling (not a CPath-1 item — standalone script)  
> Priority: HIGH — gates all Phase 1 book processing  
> Depends on: CPath-1 complete ✅

---

## Context

CPath-1 is complete. The Knowledge Engine can scan charts, generate narratives, and
manage the rule library. But the `interpretation_rules` collection is empty — no books
have been processed yet.

Phase 1 books are stored as chapter-wise OCR PDFs (text layer already present — no
live OCR needed). `backend/scripts/extract_book.py` already handles text → structured
rules extraction and paraphrasing via Claude. What is missing is:

1. **PDF → text extraction** (books are PDFs, the script reads `.txt` files)
2. **Batch orchestration** (loop over all chapters in a book, then all books)
3. **MongoDB insertion** (get the extracted JSON into the database)
4. **Resume safety** (don't re-import a chapter that already exists)

This brief specifies a `batch_ingest.py` script and a `BOOK_CONFIG_TEMPLATE.json`
that together automate the entire pipeline.

---

## Files to Create

| File | Purpose |
|---|---|
| `backend/scripts/batch_ingest.py` | Main automation script |
| `backend/scripts/BOOK_CONFIG_TEMPLATE.json` | Config template (one file per book) |

No changes to any existing files.

---

## 1. `backend/scripts/BOOK_CONFIG_TEMPLATE.json`

This is the template Prateek fills in once per book. Saved as e.g. `bphs.json`,
`lal_kitab.json`, etc. in the same `scripts/` directory.

```json
{
  "_comment": "Copy this file, rename it, and fill in all fields. Then run batch_ingest.py --config <file>.",
  "book": "Brihat Parashara Hora Shastra",
  "science_id": "vedic_astrology",
  "voice": "classical",
  "categories": "career,wealth,relationships,health,spirituality,general",
  "max_rules_per_chapter": 100,
  "min_words": 45,
  "paraphrase_mode": "hybrid",
  "chapters": [
    {
      "file": "Chapter_01_Planets.pdf",
      "name": "Chapter 1 — Planets"
    },
    {
      "file": "Chapter_02_Signs.pdf",
      "name": "Chapter 2 — Signs"
    }
  ]
}
```

**Field reference:**

| Field | Required | Notes |
|---|---|---|
| `book` | ✅ | Full book title — stored on every rule |
| `science_id` | ✅ | `vedic_astrology` / `numerology` / `palmistry` / `tarot` |
| `voice` | ✅ | `classical` or `modern_analytical` |
| `categories` | ✅ | Comma-separated. Used for all chapters unless overridden per chapter |
| `max_rules_per_chapter` | optional | Default 100 |
| `min_words` | optional | Default 45 — minimum word count for a candidate block |
| `paraphrase_mode` | optional | `hybrid` (default) / `claude` / `local`. `hybrid` and `claude` require `ANTHROPIC_API_KEY` in env |
| `chapters[].file` | ✅ | PDF filename relative to `--books-dir` |
| `chapters[].name` | ✅ | Human-readable chapter name — stored on rules |
| `chapters[].categories` | optional | Override book-level categories for this chapter only |

---

## 2. `backend/scripts/batch_ingest.py`

### 2a. CLI interface

```
python batch_ingest.py \
  --config bphs.json \
  --books-dir /path/to/pdf/folder \
  --mongo-url "mongodb+srv://..." \
  --db-name EverydayHoroscope \
  [--output-dir ./output]   # optional — save JSON + report files locally
  [--dry-run]               # extract but do NOT write to MongoDB
  [--force]                 # re-process chapters that already exist in MongoDB
```

All flags:

| Flag | Required | Default | Notes |
|---|---|---|---|
| `--config` | ✅ | — | Path to book JSON config file |
| `--books-dir` | ✅ | — | Directory containing the chapter PDF files |
| `--mongo-url` | ✅ | — | MongoDB connection string (same as Render `MONGO_URL` env) |
| `--db-name` | ✅ | — | MongoDB database name (same as Render `DB_NAME` env) |
| `--output-dir` | optional | None | If provided, saves `{batch_id}.json` and `{batch_id}_report.md` |
| `--dry-run` | optional | False | Runs full extraction but skips MongoDB writes — prints what would be inserted |
| `--force` | optional | False | Re-processes chapters even if their `batch_id` already exists in `import_batches` |

### 2b. Batch ID convention

Each chapter gets a unique batch ID:
```
{book_slug}_{chapter_index:03d}_{yyyymmdd}
```
Example: `bphs_001_20260411`, `bphs_002_20260411`

`book_slug` = lowercase, hyphens-only version of the book title
(e.g. `brihat-parashara-hora-shastra` → `bphs` is too short; use first 20 chars slugified)

Use this function:
```python
import re
from datetime import datetime, timezone

def make_batch_id(book: str, chapter_index: int) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", book.lower()).strip("-")[:20].rstrip("-")
    date = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"{slug}_{chapter_index:03d}_{date}"
```

### 2c. PDF text extraction

`pypdf` is already in `requirements.txt`. Use it:

```python
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    return "\n\n".join(pages)
```

### 2d. Calling the extraction pipeline

`extract_book.py` exports `extract_rules(args: ExtractionArgs) -> tuple[dict, str]`
and the `ExtractionArgs` dataclass. Import them directly — do NOT use subprocess.

The script must add `BACKEND_DIR` and `SCRIPT_DIR` to `sys.path` before importing,
exactly as `extract_book.py` does at lines 17–19.

Write the PDF text to a `tempfile.NamedTemporaryFile` with `.txt` suffix, then
construct `ExtractionArgs` pointing to it. Delete the temp file after extraction:

```python
import tempfile
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(SCRIPT_DIR))

from extract_book import extract_rules, ExtractionArgs, parse_categories

def run_extraction(
    text: str,
    book: str,
    chapter_name: str,
    batch_id: str,
    config: dict,
    output_path: Path,
    report_path: Path,
) -> dict:
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
            paraphrase_mode=config.get("paraphrase_mode", "hybrid"),
            model=os.getenv("EXTRACT_BOOK_CLAUDE_MODEL", "claude-sonnet-4-6"),
        )
        payload, report = extract_rules(args)
        return payload, report
    finally:
        tmp_path.unlink(missing_ok=True)
```

### 2e. MongoDB insertion

Use `pymongo` (sync — this is a local script, no async needed).

**Collections to write:**
- `interpretation_rules` — one document per extracted rule (strip `_extraction_meta`)
- `import_batches` — one document per chapter batch

```python
from pymongo import MongoClient, InsertOne
from pymongo.errors import BulkWriteError
from datetime import datetime, timezone

def insert_batch(
    client: MongoClient,
    db_name: str,
    payload: dict,
    batch_id: str,
    dry_run: bool = False,
) -> dict:
    db = client[db_name]

    rules = payload.get("rules", [])
    rule_docs = []
    for rule in rules:
        doc = {k: v for k, v in rule.items() if k != "_extraction_meta"}
        rule_docs.append(doc)

    rules_imported = 0
    duplicate_count = 0
    error_count = 0

    if not dry_run and rule_docs:
        try:
            result = db["interpretation_rules"].insert_many(rule_docs, ordered=False)
            rules_imported = len(result.inserted_ids)
        except BulkWriteError as bwe:
            # Partial success — some duplicates or errors
            rules_imported = bwe.details.get("nInserted", 0)
            duplicate_count = sum(
                1 for e in bwe.details.get("writeErrors", [])
                if e.get("code") == 11000
            )
            error_count = len(bwe.details.get("writeErrors", [])) - duplicate_count

    stats = payload.get("stats", {})
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
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
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
```

### 2f. Resume check

Before processing a chapter, check if its `batch_id` already exists:

```python
def batch_already_imported(client: MongoClient, db_name: str, batch_id: str) -> bool:
    result = client[db_name]["import_batches"].find_one(
        {"batch_id": batch_id, "import_status": "imported"},
        {"batch_id": 1},
    )
    return result is not None
```

### 2g. Main orchestration loop

```python
def main():
    args = parse_cli_args()
    config = load_config(args.config)
    books_dir = Path(args.books_dir)
    output_dir = Path(args.output_dir) if args.output_dir else None
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    client = MongoClient(args.mongo_url)
    
    book_title = config["book"]
    chapters = config.get("chapters", [])
    
    print(f"\nBook: {book_title}")
    print(f"Chapters to process: {len(chapters)}")
    print(f"Dry run: {args.dry_run}\n")

    totals = {"submitted": 0, "imported": 0, "duplicates": 0, "errors": 0, "skipped": 0}

    for i, chapter in enumerate(chapters, start=1):
        batch_id = make_batch_id(book_title, i)
        chapter_name = chapter.get("name", f"Chapter {i}")
        pdf_file = books_dir / chapter["file"]

        print(f"[{i}/{len(chapters)}] {chapter_name} ({chapter['file']})")

        if not pdf_file.exists():
            print(f"  ⚠ PDF not found: {pdf_file} — skipping")
            totals["errors"] += 1
            continue

        if not args.force and not args.dry_run:
            if batch_already_imported(client, args.db_name, batch_id):
                print(f"  ✓ Already imported (batch_id={batch_id}) — skipping")
                totals["skipped"] += 1
                continue

        # Override categories at chapter level if provided
        chapter_config = dict(config)
        if "categories" in chapter:
            chapter_config["categories"] = chapter["categories"]

        try:
            text = extract_text_from_pdf(pdf_file)
            if not text.strip():
                print(f"  ⚠ No text extracted from PDF — skipping")
                totals["errors"] += 1
                continue

            out_path = (output_dir / f"{batch_id}.json") if output_dir else Path(tempfile.mktemp(suffix=".json"))
            rpt_path = (output_dir / f"{batch_id}_report.md") if output_dir else Path(tempfile.mktemp(suffix=".md"))

            payload, report = run_extraction(text, book_title, chapter_name, batch_id, chapter_config, out_path, rpt_path)
            rule_count = len(payload.get("rules", []))
            print(f"  → Extracted {rule_count} rules")

            stats = insert_batch(client, args.db_name, payload, batch_id, dry_run=args.dry_run)
            action = "Would insert" if args.dry_run else "Inserted"
            print(f"  → {action}: {stats['rules_imported']}/{stats['rules_submitted']} rules "
                  f"({stats['duplicate_count']} dupes, {stats['error_count']} errors)")

            totals["submitted"] += stats["rules_submitted"]
            totals["imported"] += stats["rules_imported"]
            totals["duplicates"] += stats["duplicate_count"]
            totals["errors"] += stats["error_count"]

            if not output_dir:
                # Temp files — clean up
                out_path.unlink(missing_ok=True)
                rpt_path.unlink(missing_ok=True)

        except Exception as exc:
            print(f"  ✗ Error processing chapter: {exc}")
            totals["errors"] += 1
            continue

    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Done.")
    print(f"  Submitted : {totals['submitted']}")
    print(f"  Imported  : {totals['imported']}")
    print(f"  Duplicates: {totals['duplicates']}")
    print(f"  Errors    : {totals['errors']}")
    print(f"  Skipped   : {totals['skipped']}")
    if not args.dry_run and totals["imported"] > 0:
        print(f"\n  Rules are in MongoDB with approval_status='pending_review'.")
        print(f"  Open the Library Console at /admin/library to review and approve.")
    
    client.close()
```

---

## 3. Constraints

- **`pypdf` is already in `requirements.txt`** — do not add pdfplumber or any other PDF lib.
- **`pymongo` is already installed** — use sync pymongo in this script (no asyncio).
- **Import `extract_rules` and `ExtractionArgs` directly** from `extract_book` — no subprocess.
- **`sys.path` setup must happen before any local imports** — same pattern as `extract_book.py` lines 17–19.
- **`_extraction_meta` key must be stripped** before inserting into MongoDB — it is internal to the extraction pipeline and not part of `InterpretationRuleDocument`.
- **`paraphrase_mode="hybrid"` requires `ANTHROPIC_API_KEY`** in the shell environment. If the user sets `paraphrase_mode: "local"` in the config, no Claude calls are made during extraction.
- **`insert_many` with `ordered=False`** — allows partial success on duplicate key errors instead of aborting the whole batch.
- **Batch doc uses `.isoformat()` strings** for `created_at`/`updated_at` (not datetime objects) — consistent with how `extract_book.py` stores timestamps.

---

## 4. Validation Checklist (Codex self-check)

- [ ] `batch_ingest.py` has no imports at module level that require fastapi/motor (local script only needs stdlib + pymongo + pypdf + anthropic transitively via extract_book)
- [ ] `sys.path` setup is the first code executed before any local imports
- [ ] `ExtractionArgs` and `parse_categories` are imported from `extract_book`, not re-defined
- [ ] Temp file is always deleted in a `finally` block even if extraction raises
- [ ] `_extraction_meta` stripped before MongoDB insert
- [ ] `insert_many(ordered=False)` used — not `insert_one` in a loop
- [ ] `batch_already_imported()` check happens before PDF extraction (fast fail)
- [ ] `--dry-run` skips ALL MongoDB writes (both `interpretation_rules` and `import_batches`)
- [ ] `--force` bypasses the resume check
- [ ] `BOOK_CONFIG_TEMPLATE.json` has a `_comment` field explaining usage
- [ ] Progress output is printed per chapter (not silently)
- [ ] Final summary always printed even if some chapters errored

---

## 5. Usage Example (what Prateek will run)

```bash
# 1 — activate the backend venv
cd /path/to/DailyHoroscope-Migration/backend
source .venv/bin/activate   # or conda activate, etc.

# 2 — set API key (needed for paraphrase_mode=hybrid)
export ANTHROPIC_API_KEY=sk-ant-...
export MONGO_URL="mongodb+srv://..."
export DB_NAME="EverydayHoroscope"

# 3 — create a book config
cp scripts/BOOK_CONFIG_TEMPLATE.json scripts/bphs.json
# ... edit bphs.json with the correct chapter filenames ...

# 4 — dry run first to validate
python scripts/batch_ingest.py \
  --config scripts/bphs.json \
  --books-dir ~/Books/Phase1/BPHS/ \
  --mongo-url "$MONGO_URL" \
  --db-name "$DB_NAME" \
  --output-dir ./output/bphs \
  --dry-run

# 5 — real run
python scripts/batch_ingest.py \
  --config scripts/bphs.json \
  --books-dir ~/Books/Phase1/BPHS/ \
  --mongo-url "$MONGO_URL" \
  --db-name "$DB_NAME" \
  --output-dir ./output/bphs

# 6 — open Library Console at /admin/library to review and approve
```

---

## 6. What the Temple Team Will Do After Receiving This Code

1. Verify `sys.path` setup is correct and `extract_book` imports cleanly
2. Test `extract_text_from_pdf()` against one real OCR chapter PDF
3. Verify MongoDB document shape matches `ImportBatchDocument` schema exactly
4. Do a `--dry-run` against one chapter before running for real
5. Commit as: `feat(knowledge-engine): batch book ingest automation (batch_ingest.py)`
