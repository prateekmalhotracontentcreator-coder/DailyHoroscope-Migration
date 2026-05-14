# Codex Brief — Commission I: Batch Book Ingest Automation (v2)

> To: Codex
> From: EverydayHoroscope / Temple Team
> Type: Operations tooling (standalone scripts — not a CPath-1 item)
> Priority: HIGH — gates all Phase 1 book processing
> Depends on: CPath-1 complete ✅
> Updated: 2026-04-11 — OpenAI paraphrase mode + all-books master run

---

## Context

CPath-1 is complete. The Knowledge Engine can scan charts, generate narratives, and
manage the rule library. But the `interpretation_rules` collection is empty — no books
have been processed yet.

Phase 1 books are stored as chapter-wise OCR PDFs (text layer already present — no
live OCR needed). `backend/scripts/extract_book.py` already handles text → structured
rules extraction and paraphrasing. What is missing is:

1. **PDF → text extraction** (books are PDFs; the script reads `.txt` files)
2. **OpenAI paraphrase mode** (`extract_book.py` only supports Claude; we want GPT-4o-mini
   as the default — ~20× cheaper, same quality for paraphrasing)
3. **Batch orchestration** — loop over all chapters in a book, then all books, in one run
4. **MongoDB insertion** — get extracted JSON into the database
5. **Resume safety** — don't re-import a chapter that already exists

---

## Files to Create / Modify

| File | Action | Purpose |
|---|---|---|
| `backend/scripts/batch_ingest.py` | **CREATE** | Main automation + orchestration script |
| `backend/scripts/BOOK_CONFIG_TEMPLATE.json` | **CREATE** | Per-book config template |
| `backend/scripts/BOOKS_MASTER_CONFIG.json` | **CREATE** | Master list of all Phase 1 books (one-command run) |
| `backend/scripts/extract_book.py` | **MODIFY** | Add `paraphrase_with_openai()` + `"openai"` mode to `paraphrase_block()` |
| `backend/requirements.txt` | **MODIFY** | Add `openai>=1.0.0` |

---

## 1. `backend/requirements.txt` change

Add one line after the `anthropic` entry:

```
openai>=1.0.0
```

---

## 2. `extract_book.py` changes

### 2a. Add `paraphrase_with_openai()` function

Insert this function immediately after the existing `paraphrase_with_claude()` function
(currently around line 598). Follow the exact same signature and return shape:

```python
def paraphrase_with_openai(
    source_text: str,
    voice: str,
    book: str,
    condition: dict[str, Any] | None,
    model: str = "gpt-4o-mini",
) -> dict[str, Any] | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        import openai  # type: ignore
    except Exception:
        return None

    client = openai.OpenAI(api_key=api_key)
    prompt = build_paraphrase_prompt(source_text, voice, book, condition)
    try:
        response = client.chat.completions.create(
            model=model,
            max_tokens=900,
            temperature=0.35,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception:
        return None

    content = response.choices[0].message.content if response.choices else ""
    if not content:
        return None
    return extract_json_object(content)
```

### 2b. Update `paraphrase_block()` to handle `"openai"` mode

Current code (around line 630):
```python
if args.paraphrase_mode in {"claude", "hybrid"}:
    response = paraphrase_with_claude(block.text, args.voice, args.book, condition, args.model)
```

Replace with:
```python
if args.paraphrase_mode == "openai":
    response = paraphrase_with_openai(block.text, args.voice, args.book, condition)
elif args.paraphrase_mode in {"claude", "hybrid"}:
    response = paraphrase_with_claude(block.text, args.voice, args.book, condition, args.model)
```

Also update the existing `claude` mode hard-fail guard (around line 638):
```python
# existing:
if args.paraphrase_mode == "claude":
    raise RuntimeError("Claude paraphrase was requested, but no valid model response was returned.")

# change to:
if args.paraphrase_mode in {"claude", "openai"}:
    raise RuntimeError(
        f"{args.paraphrase_mode.title()} paraphrase was requested, "
        "but no valid model response was returned."
    )
```

### 2c. Update `argparse` choices to include `"openai"`

Around line 833:
```python
# existing:
parser.add_argument("--paraphrase-mode", choices=("hybrid", "claude", "local"), default="hybrid")

# change to:
parser.add_argument("--paraphrase-mode", choices=("openai", "hybrid", "claude", "local"), default="openai")
```

---

## 3. `backend/scripts/BOOK_CONFIG_TEMPLATE.json`

Template Prateek fills in once per book. Saved as e.g. `bphs.json`, `lal_kitab.json`
in the same `scripts/` directory.

```json
{
  "_comment": "Copy this file, rename it to <book_slug>.json, and fill in all fields.",
  "book": "Brihat Parashara Hora Shastra",
  "science_id": "vedic_astrology",
  "voice": "classical",
  "categories": "career,wealth,relationships,health,spirituality,general",
  "max_rules_per_chapter": 100,
  "min_words": 45,
  "paraphrase_mode": "openai",
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
| `min_words` | optional | Default 45 |
| `paraphrase_mode` | optional | `openai` (default, GPT-4o-mini) / `hybrid` (Claude Sonnet) / `local` (no API) |
| `chapters[].file` | ✅ | PDF filename relative to `--books-dir` |
| `chapters[].name` | ✅ | Human-readable chapter name — stored on rules |
| `chapters[].categories` | optional | Override book-level categories for this chapter only |

---

## 4. `backend/scripts/BOOKS_MASTER_CONFIG.json`

This is the **single file Prateek runs to ingest all Phase 1 books in one command**.
Each entry points to a per-book config file and the folder containing that book's PDFs.

```json
{
  "_comment": "Master list of all Phase 1 books. Run: python scripts/batch_ingest.py --master scripts/BOOKS_MASTER_CONFIG.json --mongo-url $MONGO_URL --db-name $DB_NAME",
  "books": [
    {
      "config": "scripts/bphs.json",
      "books_dir": "~/Books/Phase1/BPHS/"
    },
    {
      "config": "scripts/lal_kitab.json",
      "books_dir": "~/Books/Phase1/LalKitab/"
    },
    {
      "config": "scripts/saravali.json",
      "books_dir": "~/Books/Phase1/Saravali/"
    },
    {
      "config": "scripts/jataka_parijata.json",
      "books_dir": "~/Books/Phase1/JatakaParijata/"
    }
  ]
}
```

Notes:
- `config` paths are relative to the repo root (where Prateek runs the script from)
- `books_dir` paths support `~` expansion
- Books are processed sequentially (one at a time) — resume safety ensures partial runs
  can be continued by re-running the same command
- Add/remove book entries freely — the `--force` flag can re-process any book

---

## 5. `backend/scripts/batch_ingest.py`

### 5a. CLI interface

```
# Process a single book:
python scripts/batch_ingest.py \
  --config scripts/bphs.json \
  --books-dir ~/Books/Phase1/BPHS/ \
  --mongo-url "mongodb+srv://..." \
  --db-name EverydayHoroscope \
  [--output-dir ./output/bphs] \
  [--dry-run] \
  [--force]

# Process ALL books in one command (primary usage):
python scripts/batch_ingest.py \
  --master scripts/BOOKS_MASTER_CONFIG.json \
  --mongo-url "mongodb+srv://..." \
  --db-name EverydayHoroscope \
  [--output-dir ./output] \
  [--dry-run] \
  [--force]
```

All flags:

| Flag | Required | Notes |
|---|---|---|
| `--master` | ✅ or `--config` | Path to BOOKS_MASTER_CONFIG.json — processes all books |
| `--config` | ✅ or `--master` | Path to single book config — processes one book |
| `--books-dir` | ✅ with `--config` | Not used with `--master` (each book entry has its own path) |
| `--mongo-url` | ✅ | MongoDB connection string |
| `--db-name` | ✅ | MongoDB database name |
| `--output-dir` | optional | Saves `{batch_id}.json` + `{batch_id}_report.md` locally |
| `--dry-run` | optional | Full extraction but NO MongoDB writes |
| `--force` | optional | Re-processes chapters already in `import_batches` |

`--master` and `--config` are mutually exclusive. Raise `argparse` error if both provided.

### 5b. Batch ID convention

```python
import re
from datetime import datetime, timezone

def make_batch_id(book: str, chapter_index: int) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", book.lower()).strip("-")[:20].rstrip("-")
    date = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"{slug}_{chapter_index:03d}_{date}"
```

Example: `brihat-parashara-hora_001_20260411`

### 5c. PDF text extraction

`pypdf` is already in `requirements.txt`:

```python
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(pages)
```

### 5d. Calling the extraction pipeline

Import `extract_rules` and `ExtractionArgs` directly from `extract_book`. Do NOT use subprocess.

```python
import os
import sys
import tempfile
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
) -> tuple[dict, str]:
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
        tmp_path.unlink(missing_ok=True)
```

### 5e. MongoDB insertion

Use `pymongo` (sync — local script, no async needed).

```python
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from datetime import datetime, timezone

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
    rule_docs = [{k: v for k, v in r.items() if k != "_extraction_meta"} for r in payload.get("rules", [])]

    rules_imported = duplicate_count = error_count = 0

    if not dry_run and rule_docs:
        try:
            result = db["interpretation_rules"].insert_many(rule_docs, ordered=False)
            rules_imported = len(result.inserted_ids)
        except BulkWriteError as bwe:
            rules_imported = bwe.details.get("nInserted", 0)
            write_errors = bwe.details.get("writeErrors", [])
            duplicate_count = sum(1 for e in write_errors if e.get("code") == 11000)
            error_count = len(write_errors) - duplicate_count

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

### 5f. Single-book processing loop

```python
def process_book(config: dict, books_dir: Path, client: MongoClient, args) -> dict:
    book_title = config["book"]
    chapters = config.get("chapters", [])
    output_dir = Path(args.output_dir) / slugify(book_title) if args.output_dir else None
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"Book  : {book_title}")
    print(f"Chapters: {len(chapters)}  |  Dry run: {args.dry_run}")
    print(f"{'='*60}")

    totals = {"submitted": 0, "imported": 0, "duplicates": 0, "errors": 0, "skipped": 0}

    for i, chapter in enumerate(chapters, start=1):
        batch_id = make_batch_id(book_title, i)
        chapter_name = chapter.get("name", f"Chapter {i}")
        pdf_file = books_dir / chapter["file"]

        print(f"\n  [{i}/{len(chapters)}] {chapter_name}")

        if not pdf_file.exists():
            print(f"  ⚠  PDF not found: {pdf_file} — skipping")
            totals["errors"] += 1
            continue

        if not args.force and not args.dry_run:
            if batch_already_imported(client, args.db_name, batch_id):
                print(f"  ✓  Already imported ({batch_id}) — skipping")
                totals["skipped"] += 1
                continue

        chapter_config = {**config}
        if "categories" in chapter:
            chapter_config["categories"] = chapter["categories"]

        try:
            text = extract_text_from_pdf(pdf_file)
            if not text.strip():
                print(f"  ⚠  No text extracted from PDF — skipping")
                totals["errors"] += 1
                continue

            out_path = (output_dir / f"{batch_id}.json") if output_dir else Path(tempfile.mktemp(suffix=".json"))
            rpt_path = (output_dir / f"{batch_id}_report.md") if output_dir else Path(tempfile.mktemp(suffix=".md"))

            payload, _ = run_extraction(text, book_title, chapter_name, batch_id, chapter_config, out_path, rpt_path)
            rule_count = len(payload.get("rules", []))
            print(f"  → Extracted {rule_count} rules")

            stats = insert_batch(client, args.db_name, payload, batch_id, dry_run=args.dry_run)
            action = "Would insert" if args.dry_run else "Inserted"
            print(f"  → {action}: {stats['rules_imported']}/{stats['rules_submitted']} "
                  f"({stats['duplicate_count']} dupes, {stats['error_count']} errors)")

            totals["submitted"] += stats["rules_submitted"]
            totals["imported"] += stats["rules_imported"]
            totals["duplicates"] += stats["duplicate_count"]
            totals["errors"] += stats["error_count"]

            if not output_dir:
                out_path.unlink(missing_ok=True)
                rpt_path.unlink(missing_ok=True)

        except Exception as exc:
            print(f"  ✗  Error: {exc}")
            totals["errors"] += 1

    return totals
```

### 5g. Main orchestration — single book AND master mode

```python
def main():
    args = parse_cli_args()
    client = MongoClient(args.mongo_url)

    grand_totals = {"submitted": 0, "imported": 0, "duplicates": 0, "errors": 0, "skipped": 0}

    if args.master:
        # ── All-books mode ──────────────────────────────────────────────
        master = load_json(Path(args.master).expanduser().resolve())
        books = master.get("books", [])
        print(f"\nMaster run: {len(books)} book(s) queued")

        for entry in books:
            config_path = Path(entry["config"]).expanduser().resolve()
            books_dir   = Path(entry["books_dir"]).expanduser().resolve()
            config = load_json(config_path)
            totals = process_book(config, books_dir, client, args)
            for k in grand_totals:
                grand_totals[k] += totals[k]

    else:
        # ── Single-book mode ────────────────────────────────────────────
        config = load_json(Path(args.config).expanduser().resolve())
        books_dir = Path(args.books_dir).expanduser().resolve()
        totals = process_book(config, books_dir, client, args)
        grand_totals = totals

    # ── Grand summary ───────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"{'[DRY RUN] ' if args.dry_run else ''}ALL DONE")
    print(f"  Submitted  : {grand_totals['submitted']}")
    print(f"  Imported   : {grand_totals['imported']}")
    print(f"  Duplicates : {grand_totals['duplicates']}")
    print(f"  Errors     : {grand_totals['errors']}")
    print(f"  Skipped    : {grand_totals['skipped']}")
    if not args.dry_run and grand_totals["imported"] > 0:
        print(f"\n  All rules are in MongoDB with approval_status='pending_review'.")
        print(f"  Open /admin/library → Import Batches to review and approve in one session.")
    client.close()
```

`load_json` is a simple helper:
```python
import json
def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)
```

---

## 6. Constraints

- **`pypdf`** already in `requirements.txt` — do not add any other PDF library
- **`pymongo`** already installed — use sync pymongo (no asyncio)
- **`openai>=1.0.0`** must be added to `requirements.txt`
- **`extract_rules` / `ExtractionArgs` / `parse_categories`** imported directly from `extract_book` — no subprocess
- **`sys.path` setup** must be the first executable code, before all local imports
- **`_extraction_meta` key must be stripped** before MongoDB insert
- **`paraphrase_mode: "openai"`** is the new default in both `BOOK_CONFIG_TEMPLATE.json`
  and `extract_book.py` argparse — it uses `OPENAI_API_KEY` env var, calls `gpt-4o-mini`
- **`paraphrase_mode: "local"`** requires no API key — fallback paraphrase only
- **`insert_many(ordered=False)`** — allows partial success on duplicate keys
- **`--master` and `--config` are mutually exclusive** — raise argparse error if both given
- **`--books-dir` is required when using `--config`** and ignored when using `--master`
- **Batch doc timestamps** use `.isoformat()` strings, not datetime objects

---

## 7. Validation Checklist (Codex self-check)

- [ ] `openai>=1.0.0` added to `requirements.txt`
- [ ] `paraphrase_with_openai()` added to `extract_book.py` after `paraphrase_with_claude()`
- [ ] `paraphrase_block()` handles `"openai"` mode before `"claude"/"hybrid"` check
- [ ] `argparse` choices for `--paraphrase-mode` include `"openai"`; default is `"openai"`
- [ ] `batch_ingest.py` has no module-level imports requiring fastapi/motor
- [ ] `sys.path` setup is first code executed before all local imports
- [ ] `ExtractionArgs`, `extract_rules`, `parse_categories` imported from `extract_book` — not redefined
- [ ] Temp `.txt` file always deleted in `finally` block
- [ ] `_extraction_meta` stripped before MongoDB insert
- [ ] `insert_many(ordered=False)` used — not `insert_one` in a loop
- [ ] `batch_already_imported()` check happens before PDF extraction (fast fail)
- [ ] `--dry-run` skips ALL MongoDB writes (both collections)
- [ ] `--force` bypasses resume check
- [ ] `--master` and `--config` are mutually exclusive (`argparse` group)
- [ ] `--books-dir` required when using `--config`, gracefully ignored with `--master`
- [ ] `BOOKS_MASTER_CONFIG.json` has 4 sample book entries with placeholder paths
- [ ] `BOOK_CONFIG_TEMPLATE.json` has `paraphrase_mode: "openai"` as default
- [ ] Per-chapter progress printed; grand summary always printed at end
- [ ] Errors in one chapter do not abort remaining chapters

---

## 8. Usage — What Prateek Will Run

```bash
# ── Step 1: activate backend venv ───────────────────────────────────────
cd /path/to/DailyHoroscope-Migration/backend
source .venv/bin/activate

# ── Step 2: set credentials (OpenAI key for paraphrasing; Mongo for insert) ─
export OPENAI_API_KEY=sk-...          # your existing OpenAI key
export MONGO_URL="mongodb+srv://..."  # same as Render MONGO_URL
export DB_NAME="EverydayHoroscope"

# ── Step 3: fill in per-book configs (one-time, per book) ────────────────
cp scripts/BOOK_CONFIG_TEMPLATE.json scripts/bphs.json
# edit bphs.json — set book title, chapter filenames, categories
# repeat for each book; update scripts/BOOKS_MASTER_CONFIG.json with paths

# ── Step 4: dry run — validate pipeline without writing to MongoDB ────────
python scripts/batch_ingest.py \
  --master scripts/BOOKS_MASTER_CONFIG.json \
  --mongo-url "$MONGO_URL" \
  --db-name "$DB_NAME" \
  --output-dir ./output \
  --dry-run

# ── Step 5: full run — ingest ALL books in one command ───────────────────
python scripts/batch_ingest.py \
  --master scripts/BOOKS_MASTER_CONFIG.json \
  --mongo-url "$MONGO_URL" \
  --db-name "$DB_NAME" \
  --output-dir ./output
# Script is safe to re-run — already-imported chapters are skipped automatically.
# If interrupted, re-run the same command to resume from where it stopped.

# ── Step 6: Temple Team reference check ──────────────────────────────────
# Open https://www.everydayhoroscope.in/admin/library
# → Import Batches tab — all chapters appear with approval_status = pending_review
# → Review rules batch by batch; use Approve All per batch or individual rule actions
# → Additions: approve the batch
# → Subtractions: reject specific rules or the whole batch
# → Once approved, click Refresh Index — Knowledge Engine picks up new rules immediately
```

---

## 9. What Temple Team Does After Receiving This Code

1. Confirm `sys.path` setup is correct; verify `extract_book` imports cleanly
2. Test `extract_text_from_pdf()` against one real OCR chapter PDF — confirm text is clean
3. Dry-run one book; check `--output-dir` JSON for sensible rule extraction
4. Full run — all books in one master command
5. Open Library Console (`/admin/library`), review and approve all batches in one session
6. Commit as: `feat(knowledge-engine): batch book ingest automation (batch_ingest.py)`
