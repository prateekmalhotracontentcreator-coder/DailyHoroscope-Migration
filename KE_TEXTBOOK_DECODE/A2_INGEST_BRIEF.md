# KE Book Ingest -- Account 2 Operational Brief
> Prepared by: A1 (Claude Code Account 1) | Date: 2026-05-31
> Recipient: A2 (Claude Code Account 2) -- Full 1-week usage allocated
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`

---

## ⚠️ CRITICAL: READ BEFORE ANY ACTION

### What A2 OWNS (Operational)
Everything in this brief. You execute -- do not strategize.

### What A2 does NOT TOUCH (Strategic -- A1 gates)
| Off-limits | Reason |
|---|---|
| **Contradiction pair resolutions** | A2 documents all pairs found. A1 + GAI session resolves each pair. Do NOT decide outcomes. |
| **SBC book (any work)** | Blocked -- 7 TT decisions required. Do not touch. |
| **Longevity 58 Chapters** | Hard blocked -- co-founder aayu sign-off required. Do not touch. |
| **Destiny Numerology** | CRITICAL OCR items unresolved. Do not touch. |
| **KP Astrology** | Near-ready only -- Cat B/C/G/H open. Do not touch ingest yet. |
| **Co-founder approval workflow** | A2 does not interact with this. Rules enter as `pending_review` only. |
| **Any new decode work** | Decode is complete for all target books. A2 ingests only. |

### INGEST FREEZE -- CLEARED ✅
Freeze was lifted 2026-05-22. KE-Sprint2 (the arbitration runtime that the freeze depended on) was **closed by Temple Team on 2026-05-17** -- all 5 acceptance gate tests passed live. CLAUDE.md §8 flag is stale. **A2 may proceed with ingest immediately after Phase 1 environment check -- no gate message to A1 required on this point.**

---

## The Big Picture -- What You Are Actually Doing

The KE has **7 books READY for ingest** into MongoDB (`horoscope_db`, collection: `interpretation_rules`).

**Critical discovery:** Two of these books (BPHS Vol 1 and Vol 2) are ALREADY PARTIALLY INGESTED from earlier engineering sessions. You are adding the remaining decoded-but-not-yet-ingested chapters only -- not re-ingesting what is already there.

**No generic JSON-folder-to-MongoDB ingest script currently exists.** All existing ingest scripts are hard-coded chapter-by-chapter Python files. Your first major deliverable is writing a reusable `ingest_from_json_folder.py` script that reads from the decode folders and pushes to MongoDB. This unblocks all 7 books.

---

## Folder & File Map -- Complete Input/Output Inventory

### Source Decode Folders (Input)

| Book | Decode Folder (absolute path) | Status |
|---|---|---|
| BPHS Vol 1 | `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/` | READY -- partial new chapters only |
| BPHS Vol 2 | `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/` | READY -- Ch49-51 only (Ch47-60 already ingested) |
| 300 Combinations | `/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredCombinations_CC_Decode/` | READY |
| 300 Horoscopes Vol 1 | `/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredHoroscopes_CC_Decode/` | READY |
| Longevity Unnatural Death | `/Users/apple/Documents/Knowledge Engine_eBooks/LongevityUnnatural_CC_Decode/` | READY |
| Medical Astrology | `/Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode/` | READY |
| Phaladeepika | `/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode/` | READY |

### Rule File Pattern (Input -- per book)
Each decode folder contains `*_Rules.json` files (some have `*_Rules_Part1.json`, `Part2.json` etc.).
- **File wrapper**: Each JSON file is either a plain list `[...]` or an object `{"metadata": {}, "rules": [...]}`.
- **The `rules` array** is the target. Each element in `rules` is one document to ingest.
- **Ignore**: `*_Diagnostic.md`, `*_Summary.md`, `*_DataTables.md`, `*_Contradictions.json`, `*_NLM_Extract.md`, `*_OCR*.md` -- these are reference files, NOT ingest targets.

### Key Config Files (Read -- do not edit without A1)

| File | Location | Purpose |
|---|---|---|
| `knowledge_schema.py` | `backend/knowledge_schema.py` | Pydantic validation models -- use for schema reference |
| `ke_schema_constants.py` | `backend/ke_schema_constants.py` | Valid enum values for all schema fields |
| `ke_dedup_script.py` | `backend/ke_dedup_script.py` | Cross-text dedup and contradiction detector |
| `BPHS_VOL1_INGEST.md` | `.claude/ke/ingest/BPHS_VOL1_INGEST.md` | Tracks what BPHS Vol 1 chapters are already in MongoDB |
| `BPHS_VOL2_INGEST.md` | `.claude/ke/ingest/BPHS_VOL2_INGEST.md` | Tracks what BPHS Vol 2 chapters are already in MongoDB |
| `INGEST_SUMMARY.md` | `KE_TEXTBOOK_DECODE/INGEST_SUMMARY.md` | Master status of all books |
| `TEMPLE_TRACKER.md` | `TEMPLE_TRACKER.md` | Module dashboard -- update at end of session |

### MongoDB Output Target

| Item | Value |
|---|---|
| Connection | `MONGO_URL` env var (Render env -- available locally when using `dotenv` or direct export) |
| Database | `horoscope_db` |
| Collection | `interpretation_rules` |
| Batch tracking | `import_batches` collection (one document per ingest run) |
| Initial approval_status | `pending_review` on ALL new rules -- no exceptions (⚠️ NOT `pending_human_review` -- validate_rules.py queries `pending_review`) |

### Script Output Files (you produce these -- save in repo)

| Output | Location | Purpose |
|---|---|---|
| `ingest_from_json_folder.py` | `backend/scripts/ingest_from_json_folder.py` | Generic ingest script (your primary deliverable) |
| `ke_dedup_report_[bookA]_vs_[bookB].json` | `KE_TEXTBOOK_DECODE/Dedup_Reports/` | One file per book pair |
| `ke_contradiction_pairs_master.md` | `KE_TEXTBOOK_DECODE/Dedup_Reports/` | Consolidated contradiction summary for A1 |
| `A2_INGEST_LOG.md` | `KE_TEXTBOOK_DECODE/` | Running log of every action taken, result, and timestamp |

---

## Exact BPHS Ingest Scope -- What Is New vs Already Done

### BPHS Vol 1 -- Already Ingested (DO NOT RE-INGEST)

Per `.claude/ke/ingest/BPHS_VOL1_INGEST.md` (last updated 2026-05-08):

| Already in MongoDB | Chapters |
|---|---|
| ✅ Ingested | Ch12, Ch13, Ch14, Ch15, Ch16, Ch17, Ch18, Ch19, Ch20, Ch21, Ch22, Ch23, Ch24, Ch27, Ch34, Ch35, Ch36, Ch37, Ch38, Ch39, Ch40, Ch43, Ch44 |

### BPHS Vol 1 -- NEW Chapters to Ingest (Decode folder only)

These are in `BPHS_CC_Decode/` but NOT yet in MongoDB:

| Chapter | Rule Files | Notes |
|---|---|---|
| Ch03 | `BPHS_Ch03_*_Rules_Part1/2/3.json` | 3 parts |
| Ch04 | `BPHS_Ch04_*_Rules_Part1.json` | |
| Ch05 | `BPHS_Ch05_*_Rules_Part1.json` | |
| Ch06 | `BPHS_Ch06_*_Rules_Part1.json` + `Part2.json` | ⚠️ Rules 027/028 have `chapter:5` -- ingest under Ch05 |
| Ch07 | `BPHS_Ch07_*_Rules_Part1.json` | |
| Ch08 | `BPHS_Ch08_*_Rules_Part1.json` | |
| Ch09 | `BPHS_Ch09_*_Rules_Part1.json` + `Part2.json` | 2 parts |
| Ch10 | `BPHS_Ch10_*_Rules_Part1.json` | |
| Ch11 | `BPHS_Ch11_Judgement_of_Houses_Rules.json` | |
| Ch25 | `BPHS_Ch25_*_Diagnostic.md` exists -- check if Rules.json present | |
| Ch26 | Same -- check | |
| Ch28 | `BPHS_Ch28_Ishta_Kashta_Balas_Rules_Part1.json` | Just updated by A1 today |
| Ch29 | `BPHS_Ch29_*_Rules_Part1.json` | |
| Ch30 | `BPHS_Ch30_*_Rules_Part1/2/3.json` | 3 parts. Just updated by A1. |
| Ch31 | `BPHS_Ch31_*_Rules_Part1.json` + `Part2.json` | 2 parts. Just updated by A1. |
| Ch32 | Check for Rules.json | |
| Ch33 | Check for Rules.json | |

**Before ingesting**: Run this to audit what rule files exist vs what's already in MongoDB:
```bash
# List all Rules.json files in BPHS decode folder
find "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/" -name "*Rules*.json" | sort

# Count documents already in MongoDB for BPHS Vol 1
python3 -c "
from pymongo import MongoClient; import os
client = MongoClient(os.environ['MONGO_URL'])
count = client['horoscope_db']['interpretation_rules'].count_documents({'source_book': {'$regex': 'BPHS', '\$options': 'i'}})
print(f'BPHS rules in MongoDB: {count}')
"
```

### BPHS Vol 2 -- Scope (CLEARED ✅)

Per `.claude/ke/ingest/BPHS_VOL2_INGEST.md`:

| Already in MongoDB | Ch47, Ch48, Ch52-Ch60 -- **do not re-ingest** |
|---|---|
| **NEW -- ingest these** | Ch49, Ch50, Ch51 only |

**A1 CONFIRMED (2026-05-31):** Ch49-51 exclusion from `.claude/ke/ingest/BPHS_VOL2_INGEST.md` is superseded. A1 has cleared Ch49-51 for ingest as `pending_human_review`. Proceed without gate.

Ch49: 154 rules (153 active + 1 source_gap inactive). Ch50: 73 rules. Ch51: 22 rules. Total new = 249 rules.

---

## Reference Ingest Scripts -- Study These Before Writing Your Script

Existing ingest scripts follow a consistent pattern. Read these before writing `ingest_from_json_folder.py` so your script matches the established conventions exactly.

### Pattern Reference Scripts (in order of usefulness)

| Script | Location | What to Learn From It |
|---|---|---|
| `ingest_bphs_ch35_v1.py` | `backend/scripts/ingest_bphs_ch35_v1.py` | **Primary pattern** -- `--dry-run`/`--save`/`--upload` workflow, `BATCH_ID` constant, `SCIENCE`/`BOOK`/`BOOK_ID` constants, `insert_many` with `ordered=False`, `import_batches` write |
| `ingest_bphs_ch41_v1.py` | `backend/scripts/ingest_bphs_ch41_v1.py` | yoga_check field shapes (note: uses old `"pending_human_review"` -- use `"pending_review"` instead) |
| `ingest_bphs_ch40_v1.py` | `backend/scripts/ingest_bphs_ch40_v1.py` | Rule document field ordering, `source` sub-document pattern |
| `batch_ingest.py` | `backend/scripts/batch_ingest.py` | `batch_already_imported()` check (idempotency), `insert_batch()` with stats tracking, `import_batches` collection document shape -- **read this carefully, the batch tracking logic is reusable verbatim** |
| `migrate_ch41_varga_checkable.py` | `backend/scripts/migrate_ch41_varga_checkable.py` | `--mongo-url`/`--db-name`/`--dry-run` CLI arg pattern using `argparse` |

### Key Patterns to Copy Exactly

**CLI args (from any existing script):**
```python
parser = argparse.ArgumentParser()
parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
parser.add_argument("--db-name", default="horoscope_db")
parser.add_argument("--dry-run", action="store_true")
```

**Idempotency check (from batch_ingest.py):**
```python
def batch_already_imported(client, db_name, batch_id):
    return client[db_name]["import_batches"].find_one(
        {"batch_id": batch_id, "import_status": "imported"},
        {"batch_id": 1},
    ) is not None
```
Always check this at the top of your script -- if the batch is already imported, exit cleanly.

**Insert with duplicate tolerance (from batch_ingest.py):**
```python
try:
    result = db["interpretation_rules"].insert_many(rule_docs, ordered=False)
    rules_inserted = len(result.inserted_ids)
except BulkWriteError as bwe:
    rules_inserted = bwe.details.get("nInserted", 0)
    duplicate_count = sum(1 for e in bwe.details.get("writeErrors", []) if e.get("code") == 11000)
```

**import_batches record (from batch_ingest.py -- copy this structure exactly):**
```python
batch_doc = {
    "batch_id": batch_id,
    "source_book": book_name,
    "import_status": "imported",
    "rules_inserted": rules_inserted,
    "duplicates_skipped": duplicate_count,
    "errors": error_count,
    "timestamp": datetime.now(timezone.utc).isoformat(),
}
db["import_batches"].insert_one(batch_doc)
```

**Rule document fields to ADD before inserting (your script must inject these):**
```python
rule_doc["approval_status"] = "pending_review"   # ⚠️ NOT "pending_human_review" -- validate_rules.py queries "pending_review"
rule_doc["ingested_at"] = datetime.now(timezone.utc).isoformat()
rule_doc["ingest_batch_id"] = batch_id
rule_doc["source_book"] = book_name
rule_doc["source_file"] = os.path.basename(json_file_path)
# Do NOT overwrite rule_id -- it must come from the source JSON
```

**Rule document fields to PRESERVE from source JSON (pass through as-is):**
```python
# These flags vary per rule -- never overwrite, just pass through:
# active, gai_citation_unverified, birth_data_unavailable,
# analytical_description_only, pending_review, tba, provisional,
# source_gap, decode_notes, resolution_status, chapter, sloka
```

### Validation Script Reference

After each ingest, the existing `validate_rules.py` in `backend/scripts/` may be usable. Check if it exists:
```bash
ls backend/scripts/validate_rules.py
```
If it does, study its `--batch-id` filter pattern for your own `validate_ingest_batch.py`.

---

## Phase-by-Phase Execution Plan

---

### PHASE 1 -- Environment Setup & Audit (No writes, no risk)

**Goal:** Confirm everything is in place before a single document is written to MongoDB.

**Step 1.1 -- Read these files first (mandatory)**
```
TEMPLE_TRACKER.md
KE_TEXTBOOK_DECODE/INGEST_SUMMARY.md
.claude/ke/ingest/BPHS_VOL1_INGEST.md
.claude/ke/ingest/BPHS_VOL2_INGEST.md
backend/knowledge_schema.py  (lines 1-150 -- field definitions)
backend/ke_schema_constants.py  (full file -- all valid enum values)
backend/ke_dedup_script.py  (full file -- understand the interface)
```

**Step 1.2 -- Verify Python environment**
```bash
cd /Users/apple/DailyHoroscope-Migration
python3 --version  # Need 3.10+
pip3 show pymongo motor pydantic  # Must all be installed
python3 -c "import pymongo; print('pymongo OK')"
```

**Step 1.3 -- Verify MONGO_URL**
```bash
# Check env var is available
echo $MONGO_URL | head -c 30  # Should show mongodb+srv://...
# Or load from .env:
export $(cat backend/.env | grep MONGO_URL) && echo $MONGO_URL | head -c 30
```

**Step 1.4 -- Count existing rules in MongoDB (dry audit)**
```bash
python3 -c "
from pymongo import MongoClient; import os
client = MongoClient(os.environ['MONGO_URL'])
db = client['horoscope_db']
total = db['interpretation_rules'].count_documents({})
phr = db['interpretation_rules'].count_documents({'approval_status': 'pending_human_review'})
approved = db['interpretation_rules'].count_documents({'approval_status': 'approved'})
auto = db['interpretation_rules'].count_documents({'approval_status': 'auto_approved'})
batches = db['import_batches'].count_documents({})
print(f'Total rules: {total}')
print(f'pending_human_review: {phr}')
print(f'approved: {approved}')
print(f'auto_approved: {auto}')
print(f'Import batches: {batches}')
"
```

**Step 1.5 -- Inventory all decode folder rule files**
```bash
# Count rules in each READY book decode folder
for dir in \
  "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode" \
  "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode" \
  "/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredCombinations_CC_Decode" \
  "/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredHoroscopes_CC_Decode" \
  "/Users/apple/Documents/Knowledge Engine_eBooks/LongevityUnnatural_CC_Decode" \
  "/Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode" \
  "/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode"; do
  count=$(find "$dir" -name "*Rules*.json" | wc -l)
  echo "$count files -- $dir"
done
```

**Step 1.6 -- Count rules in each JSON file**
Write and run this Python audit script:
```python
# save as: scripts/audit_decode_folders.py
import json, glob, os

BOOKS = {
    "BPHS_Vol1": "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode",
    "BPHS_Vol2": "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode",
    "300_Combinations": "/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredCombinations_CC_Decode",
    "300_Horoscopes": "/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredHoroscopes_CC_Decode",
    "Longevity_Unnatural": "/Users/apple/Documents/Knowledge Engine_eBooks/LongevityUnnatural_CC_Decode",
    "Medical_Astrology": "/Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode",
    "Phaladeepika": "/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode",
}

for book, folder in BOOKS.items():
    files = sorted(glob.glob(f"{folder}/**/*Rules*.json", recursive=True))
    total_rules = 0
    active_rules = 0
    file_list = []
    for f in files:
        try:
            raw = json.load(open(f, encoding="utf-8"))
            rules = raw.get("rules", raw) if isinstance(raw, dict) else raw
            rules = [r for r in rules if isinstance(r, dict)]
            active = [r for r in rules if r.get("active", True) is not False]
            total_rules += len(rules)
            active_rules += len(active)
            file_list.append(f"  {os.path.basename(f)}: {len(rules)} total / {len(active)} active")
        except Exception as e:
            file_list.append(f"  ERROR {os.path.basename(f)}: {e}")
    print(f"\n{'='*60}")
    print(f"BOOK: {book}")
    print(f"  Files: {len(files)} | Total rules: {total_rules} | Active: {active_rules}")
    for line in file_list:
        print(line)
```

**→ PAUSE after Phase 1. Log all counts in `A2_INGEST_LOG.md`. Message A1 with:**
1. Total rules per book from audit
2. Current MongoDB rule count
3. BPHS Vol 2 Ch49-51 gate question
4. Any files that threw errors during audit

---

### PHASE 2 -- Write the Generic Ingest Script

**Goal:** Create `backend/scripts/ingest_from_json_folder.py` -- this is your primary engineering deliverable. No existing script does what we need.

**What it must do:**
1. Accept `--folder` (path to decode folder), `--book` (book name), `--batch-id` (unique string), `--dry-run` flag, `--mongo-url`, `--db-name`
2. Recursively find all `*_Rules*.json` files in the folder (skip `*Contradictions*`, `*NLM_Extract*`)
3. For each file, load and extract the `rules` array (handle both `{"rules": [...]}` wrapper and plain list)
4. Filter: skip rules where `active: false`
5. For each active rule document, add/overwrite these fields before insert:
   - `approval_status: "pending_human_review"`
   - `ingested_at: <UTC ISO timestamp>`
   - `source_book: <book argument>`
   - `ingest_batch_id: <batch-id argument>`
   - `source_file: <basename of json file>`
   - Do NOT overwrite `rule_id` -- it must already exist in the source JSON
6. Validate: every document must have `rule_id` -- reject any without it (log to error file)
7. Use `insert_many` with `ordered=False` -- duplicate `rule_id`s get logged, not crashed
8. Write to `import_batches` collection after completion with: batch_id, book, files_processed, rules_inserted, duplicates_skipped, errors, timestamp
9. `--dry-run`: prints counts and first 3 sample documents -- writes nothing to MongoDB

**Script signature:**
```bash
# Dry run (always run this first):
python3 backend/scripts/ingest_from_json_folder.py \
  --folder "/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredCombinations_CC_Decode" \
  --book "300 Combinations" \
  --batch-id "300-combinations-v1-20260531" \
  --db-name horoscope_db \
  --dry-run

# Live run:
python3 backend/scripts/ingest_from_json_folder.py \
  --folder "/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredCombinations_CC_Decode" \
  --book "300 Combinations" \
  --batch-id "300-combinations-v1-20260531" \
  --mongo-url "$MONGO_URL" \
  --db-name horoscope_db
```

**Important schema notes from `knowledge_schema.py`:**
- `approval_status` valid values: `"pending_review"`, `"approved"`, `"rejected"`, `"auto_approved"`, `"pending_human_review"`, `"flagged"`
- Use `"pending_review"` for all new rules (NOT `"pending_human_review"` -- validate_rules.py won't find them)
- MongoDB collection: `interpretation_rules`
- Batch tracking collection: `import_batches`
- Field `rule_id` is the natural key -- use as the upsert/dedup key

**BPHS Vol 1 special case:** Rules 027 and 028 in `BPHS_Ch06_Sixteen_Divisions_Rules_Part2.json` have `chapter: 5`. The script should preserve this field as-is from the source JSON.

**→ PAUSE after Phase 2. Run the dry-run against 300 Combinations first. Send output to A1 for review before any live writes.**

---

---

## 🔧 Session Learnings & Known Gotchas
> Captured from BPHS Vol 2 Ch49-51 ingest session (2026-06-01). Apply to ALL future ingests.

---

### L1 -- `approval_status` must be `"pending_review"`, NOT `"pending_human_review"`

`validate_rules.py` (Stage 2 Claude quality check) queries `approval_status: "pending_review"`. If you set `"pending_human_review"` on ingest, the script fetches 0 rules and exits silently -- you get no validation output and no auto_approved rules. All existing reference scripts use the old value -- **do not copy it**.

```python
# ✅ CORRECT
rule_doc["approval_status"] = "pending_review"

# ❌ WRONG -- validate_rules.py won't find these
rule_doc["approval_status"] = "pending_human_review"
```

---

### L2 -- Dedup requires TWO passes, not one

The dedup plan in Phase 3 covers local folder-to-folder pairs only. **A second pass against existing MongoDB rules is mandatory.** Without it, you may ingest rules that are already in MongoDB under a different source book.

**Pass 1 (already in this brief):** New rules folder vs other local CC_Decode folders.

**Pass 2 (new -- add to every ingest):** New rules folder vs all existing MongoDB rules exported to a temp folder.

Script to export: `backend/scripts/export_mongo_for_dedup.py`

```bash
# Step 1: Export existing MongoDB rules (excluding current batch) to temp folder
python3 backend/scripts/export_mongo_for_dedup.py  # outputs to /tmp/mongo_existing_rules_dedup/

# Step 2: Dedup new rules vs exported MongoDB rules
python3 backend/ke_dedup_script.py \
  --folder-a "/path/to/NewBook_CC_Decode/" \
  --folder-b "/tmp/mongo_existing_rules_dedup/" \
  --output-report dedup_newbook_vs_mongodb.md \
  --threshold 0.82
```

---

### L3 -- MongoDB export for dedup: field mapping + condition coercion

`ke_dedup_script.py` uses `rule.get("full_text", "")` for comparison. MongoDB rules store text in `interpretation.detailed`, not `full_text`. When exporting for dedup, map the field:

```python
interp = rule.get("interpretation") or {}
mapped_rule["full_text"] = interp.get("detailed") or interp.get("full_text") or ""
```

Also: **legacy rules may have `condition` as a string, not a dict.** The dedup script calls `condition.get(...)` and crashes on string values. Coerce before saving:

```python
raw_cond = rule.get("condition")
if isinstance(raw_cond, dict):
    cond = raw_cond
elif isinstance(raw_cond, str):
    cond = {"type": raw_cond}
else:
    cond = {}
```

---

### L4 -- `ingest_batch_id: null` filter gotcha

Legacy rules (pre-batch-tracking) have `ingest_batch_id: null` -- the **field exists but its value is null**. This means:
- `{'ingest_batch_id': {'$exists': False}}` → returns 0 (field exists)
- `{'ingest_batch_id': {'$ne': 'your-new-batch'}}` → returns 0 (null does not satisfy `$ne` in Mongo)

To correctly select "all rules except the new batch", use:
```python
query = {
    "$or": [
        {"ingest_batch_id": {"$exists": False}},
        {"ingest_batch_id": None},
        {"ingest_batch_id": {"$nin": ["your-new-batch-id"]}},
    ]
}
```

---

### L5 -- Complementary polarity rules are NOT contradictions

The automated Stage 3 contradiction detector will flag two rules as a contradiction whenever they share a condition signature (same house, same type) but describe opposite outcomes. **This is a systematic false positive** when the rules describe opposite planet categories for the same position.

**Pattern:** Rule A = "malefics in 5th from Dasa Rasi → distress" + Rule B = "benefics in 5th from Dasa Rasi → favourable" → flagged as contradictions. They are not. Both rules must be retained.

**What to check:** If two rules are flagged as contradicting each other and one says "malefic" while the other says "benefic" (or "debilitated" vs "exalted", "enemy sign" vs "friend sign"), treat as Bucket B (validator error), not Bucket C. Raise to GAI for confirmation only if the planet categories are ambiguous.

**Bucket A (triage) updated definition:** Data artifact only -- the core claim is present and verifiable in either `interpretation.detailed` or `interpretation.summary`, even if extended commentary is truncated. The original definition ("summary truncated, detailed OK") was too narrow. Truncation in the detailed field is also Bucket A if the summary is intact and the core rule is unambiguous.

---

### PHASE 3 -- Pre-Ingest Dedup

**Goal:** Run `ke_dedup_script.py` across all book pairs before any ingest. Dedup output guides what gets tagged as a cross-text match or contradiction in MongoDB.

**Command format:**
```bash
python3 backend/ke_dedup_script.py \
  --folder-a "/path/to/BookA_CC_Decode" \
  --folder-b "/path/to/BookB_CC_Decode" \
  --output-report "KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_BookA_vs_BookB.json" \
  --threshold 0.82 \
  --dry-run
```
Note: `--dry-run` generates the report without modifying source JSON files. Run with `--update-files` only after A1 reviews the report.

**Required Dedup Pairs -- run ALL of these:**

Create folder first: `mkdir -p /Users/apple/DailyHoroscope-Migration/KE_TEXTBOOK_DECODE/Dedup_Reports/`

| Run # | Folder A | Folder B | Output File |
|---|---|---|---|
| 1 | BPHS_CC_Decode | BPHS_Vol2_CC_Decode | dedup_bphs1_vs_bphs2.json |
| 2 | ThreeHundredCombinations_CC_Decode | BPHS_CC_Decode | dedup_300combo_vs_bphs1.json |
| 3 | ThreeHundredCombinations_CC_Decode | BPHS_Vol2_CC_Decode | dedup_300combo_vs_bphs2.json |
| 4 | ThreeHundredHoroscopes_CC_Decode | BPHS_CC_Decode | dedup_300horo_vs_bphs1.json |
| 5 | ThreeHundredHoroscopes_CC_Decode | BPHS_Vol2_CC_Decode | dedup_300horo_vs_bphs2.json |
| 6 | ThreeHundredHoroscopes_CC_Decode | ThreeHundredCombinations_CC_Decode | dedup_300horo_vs_300combo.json |
| 7 | LongevityUnnatural_CC_Decode | BPHS_CC_Decode | dedup_lu_vs_bphs1.json |
| 8 | LongevityUnnatural_CC_Decode | BPHS_Vol2_CC_Decode | dedup_lu_vs_bphs2.json |
| 9 | MedicalAstrology_CC_Decode | BPHS_CC_Decode | dedup_medastro_vs_bphs1.json |
| 10 | MedicalAstrology_CC_Decode | BPHS_Vol2_CC_Decode | dedup_medastro_vs_bphs2.json |
| 11 | MedicalAstrology_CC_Decode | LongevityUnnatural_CC_Decode | dedup_medastro_vs_lu.json |
| 12 | Phaladeepika_CC_Decode | BPHS_CC_Decode | dedup_pd_vs_bphs1.json |
| 13 | Phaladeepika_CC_Decode | BPHS_Vol2_CC_Decode | dedup_pd_vs_bphs2.json |
| 14 | Phaladeepika_CC_Decode | ThreeHundredCombinations_CC_Decode | dedup_pd_vs_300combo.json |
| 15 | Phaladeepika_CC_Decode | ThreeHundredHoroscopes_CC_Decode | dedup_pd_vs_300horo.json |
| 16 | Phaladeepika_CC_Decode | MedicalAstrology_CC_Decode | dedup_pd_vs_medastro.json |

**Run all 16 as `--dry-run` first.** Once generated, parse each report and produce `ke_contradiction_pairs_master.md` with:

```markdown
# KE Cross-Text Contradiction Pairs -- Master Log
> Generated: 2026-05-31 by A2

## Summary Table
| Pair | identical_claim | near_identical | partial_overlap | contradicts | partial_contradiction |
|---|---|---|---|---|---|
| BPHS1 vs BPHS2 | X | X | X | X | X |
...

## Contradiction Pairs Requiring Resolution (CONTRADICTS + PARTIAL_CONTRADICTION only)
> A1 resolves these via GAI session. Do NOT touch resolution_type fields.

### BPHS1 vs BPHS2
| Rule A (ID) | Rule B (ID) | Relationship | Claim A | Claim B |
...
```

**→ PAUSE after Phase 3. Send `ke_contradiction_pairs_master.md` to A1 before proceeding to ingest.**

---

### PHASE 4 -- Ingest (Live Writes)

**Gate conditions before starting Phase 4:**
- [ ] A1 has confirmed ingest freeze is lifted
- [ ] A1 has reviewed Phase 2 dry-run output
- [ ] A1 has reviewed Phase 3 contradiction pairs master
- [ ] BPHS Vol 2 Ch49-51 gate explicitly addressed by A1

**Ingest Order (strictly follow -- BPHS first as foundational):**

#### 4.1 -- 300 Combinations (Priority 1 -- No dedup dependencies)
```bash
# Dry run
python3 backend/scripts/ingest_from_json_folder.py \
  --folder "/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredCombinations_CC_Decode" \
  --book "300 Combinations" --batch-id "300-combinations-v1-20260531" \
  --db-name horoscope_db --dry-run

# Live (only after A1 confirmation)
python3 backend/scripts/ingest_from_json_folder.py \
  --folder "/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredCombinations_CC_Decode" \
  --book "300 Combinations" --batch-id "300-combinations-v1-20260531" \
  --mongo-url "$MONGO_URL" --db-name horoscope_db
```

#### 4.2 -- BPHS Vol 1 (NEW chapters only -- Ch03-Ch11, Ch25-Ch33, Ch28, Ch29, Ch30, Ch31)
```bash
# IMPORTANT: Do NOT run against the full BPHS_CC_Decode folder blindly.
# Ch12-24, Ch27, Ch34, Ch35-44 are already in MongoDB.
# You MUST create a subfolder or pass a filtered chapter list.

# Option A -- Create a staging folder with only the new chapters:
mkdir -p /tmp/bphs_vol1_new_chapters/
cp /Users/apple/Documents/Knowledge\ Engine_eBooks/BPHS_CC_Decode/BPHS_Ch03_*.json /tmp/bphs_vol1_new_chapters/
cp /Users/apple/Documents/Knowledge\ Engine_eBooks/BPHS_CC_Decode/BPHS_Ch04_*.json /tmp/bphs_vol1_new_chapters/
cp /Users/apple/Documents/Knowledge\ Engine_eBooks/BPHS_CC_Decode/BPHS_Ch05_*.json /tmp/bphs_vol1_new_chapters/
cp /Users/apple/Documents/Knowledge\ Engine_eBooks/BPHS_CC_Decode/BPHS_Ch06_*.json /tmp/bphs_vol1_new_chapters/
cp /Users/apple/Documents/Knowledge\ Engine_eBooks/BPHS_CC_Decode/BPHS_Ch07_*.json /tmp/bphs_vol1_new_chapters/
cp /Users/apple/Documents/Knowledge\ Engine_eBooks/BPHS_CC_Decode/BPHS_Ch08_*.json /tmp/bphs_vol1_new_chapters/
cp /Users/apple/Documents/Knowledge\ Engine_eBooks/BPHS_CC_Decode/BPHS_Ch09_*.json /tmp/bphs_vol1_new_chapters/
cp /Users/apple/Documents/Knowledge\ Engine_eBooks/BPHS_CC_Decode/BPHS_Ch10_*.json /tmp/bphs_vol1_new_chapters/
cp /Users/apple/Documents/Knowledge\ Engine_eBooks/BPHS_CC_Decode/BPHS_Ch11_*.json /tmp/bphs_vol1_new_chapters/
cp /Users/apple/Documents/Knowledge\ Engine_eBooks/BPHS_CC_Decode/BPHS_Ch28_*.json /tmp/bphs_vol1_new_chapters/
cp /Users/apple/Documents/Knowledge\ Engine_eBooks/BPHS_CC_Decode/BPHS_Ch29_*.json /tmp/bphs_vol1_new_chapters/
cp /Users/apple/Documents/Knowledge\ Engine_eBooks/BPHS_CC_Decode/BPHS_Ch30_*.json /tmp/bphs_vol1_new_chapters/
cp /Users/apple/Documents/Knowledge\ Engine_eBooks/BPHS_CC_Decode/BPHS_Ch31_*.json /tmp/bphs_vol1_new_chapters/
cp /Users/apple/Documents/Knowledge\ Engine_eBooks/BPHS_CC_Decode/BPHS_Ch32_*.json /tmp/bphs_vol1_new_chapters/ 2>/dev/null || true
cp /Users/apple/Documents/Knowledge\ Engine_eBooks/BPHS_CC_Decode/BPHS_Ch33_*.json /tmp/bphs_vol1_new_chapters/ 2>/dev/null || true
# Also check Ch25, Ch26 -- check if Rules.json files exist first
ls /Users/apple/Documents/Knowledge\ Engine_eBooks/BPHS_CC_Decode/ | grep "Ch25\|Ch26"

# Then ingest the staging folder
python3 backend/scripts/ingest_from_json_folder.py \
  --folder /tmp/bphs_vol1_new_chapters \
  --book "BPHS Vol 1" --batch-id "bphs-vol1-new-chapters-v1-20260531" \
  --mongo-url "$MONGO_URL" --db-name horoscope_db
```

#### 4.3 -- BPHS Vol 2 Ch49-51 (ONLY IF A1 CONFIRMS)
```bash
# Gate: A1 must explicitly say "proceed with BPHS Vol 2 Ch49-51"
# Ch47, Ch48, Ch52-Ch60 already in MongoDB -- do not re-ingest
python3 backend/scripts/ingest_from_json_folder.py \
  --folder "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode" \
  --book "BPHS Vol 2" --batch-id "bphs-vol2-ch4951-v1-20260531" \
  --mongo-url "$MONGO_URL" --db-name horoscope_db
```

#### 4.4 -- 300 Horoscopes Vol 1
```bash
python3 backend/scripts/ingest_from_json_folder.py \
  --folder "/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredHoroscopes_CC_Decode" \
  --book "300 Horoscopes Vol 1" --batch-id "300-horoscopes-v1-20260531" \
  --mongo-url "$MONGO_URL" --db-name horoscope_db
```
Special flags to preserve in source JSON: `birth_data_unavailable: true` on certain chart rules -- your script must pass-through all source fields as-is.

#### 4.5 -- Longevity Unnatural Death
```bash
python3 backend/scripts/ingest_from_json_folder.py \
  --folder "/Users/apple/Documents/Knowledge Engine_eBooks/LongevityUnnatural_CC_Decode" \
  --book "Longevity Unnatural Death" --batch-id "longevity-unnatural-v1-20260531" \
  --mongo-url "$MONGO_URL" --db-name horoscope_db
```
Note: Rules with remaining MEDIUM OCR items already have `pending_review: true` in source JSON. Preserve as-is.

#### 4.6 -- Medical Astrology
```bash
python3 backend/scripts/ingest_from_json_folder.py \
  --folder "/Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode" \
  --book "Medical Astrology" --batch-id "medical-astrology-v1-20260531" \
  --mongo-url "$MONGO_URL" --db-name horoscope_db
```
Note: Grade B rules have `gai_citation_unverified: true` flag -- preserve. bench-004 has `birth_data_unavailable: true` -- preserve. Grade C benchmark rules have `analytical_description_only: true` -- preserve. bench benchmarks may be in a `*_CaseHistories_*` file -- include these.

#### 4.7 -- Phaladeepika (28 chapters -- largest ingest)
```bash
python3 backend/scripts/ingest_from_json_folder.py \
  --folder "/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode" \
  --book "Phaladeepika" --batch-id "phaladeepika-v1-20260531" \
  --mongo-url "$MONGO_URL" --db-name horoscope_db
```
Note: Ch08 TBA Sun rules have `tba: true` -- preserve. pd-ch21-041 has `gai_citation_unverified: true` -- preserve.

---

### PHASE 5 -- Post-Ingest Validation

After each book ingest, run this validation:
```python
# save as: scripts/validate_ingest_batch.py
import sys
from pymongo import MongoClient
import os

batch_id = sys.argv[1]
client = MongoClient(os.environ['MONGO_URL'])
db = client['horoscope_db']

batch = db['import_batches'].find_one({"batch_id": batch_id})
if not batch:
    print(f"ERROR: batch {batch_id} not found in import_batches")
    sys.exit(1)

rules = list(db['interpretation_rules'].find({"ingest_batch_id": batch_id}))

# Checks
missing_rule_id = [r for r in rules if not r.get('rule_id')]
wrong_status = [r for r in rules if r.get('approval_status') != 'pending_human_review']
missing_book = [r for r in rules if not r.get('source_book')]

print(f"Batch: {batch_id}")
print(f"Rules in DB: {len(rules)}")
print(f"Rules reported inserted: {batch.get('rules_inserted', '?')}")
print(f"Missing rule_id: {len(missing_rule_id)}")
print(f"Wrong approval_status: {len(wrong_status)}")
print(f"Missing source_book: {len(missing_book)}")
print(f"Status: {'✅ CLEAN' if not missing_rule_id and not wrong_status and not missing_book else '❌ ISSUES FOUND'}")
```

Run as: `python3 backend/scripts/validate_ingest_batch.py "300-combinations-v1-20260531"`

---

### PHASE 6 -- Tracking File Updates

After all ingests complete, update these files:

**1. `.claude/ke/ingest/BPHS_VOL1_INGEST.md`** -- add new section:
```markdown
## Phase 2 -- New Chapters (2026-05-31)
| Script | Purpose | Status |
|---|---|---|
| ingest_from_json_folder.py | Ch03-Ch11, Ch25-Ch33 (new decode chapters) | ✅ Done |
```

**2. Create new ingest tracking files for each new book:**
- `.claude/ke/ingest/300_COMBINATIONS_INGEST.md`
- `.claude/ke/ingest/300_HOROSCOPES_INGEST.md`
- `.claude/ke/ingest/LONGEVITY_UNNATURAL_INGEST.md`
- `.claude/ke/ingest/MEDICAL_ASTROLOGY_INGEST.md`
- `.claude/ke/ingest/PHALADEEPIKA_INGEST.md`

Each should follow the same format as `BPHS_VOL1_INGEST.md`.

**3. Update `KE_TEXTBOOK_DECODE/INGEST_SUMMARY.md`** -- for each book ingested:
- Change `Ingest status` from `🟢 READY` to `✅ INGESTED [date]`
- Add rule count ingested

**4. Update `TEMPLE_TRACKER.md`** -- find the KE row and update status.

**5. Update `Codex_Deliveries/Knowledge_Engine/TRACKER.md`** -- add a version history row for each major action. Follow the existing format exactly.

---

## Error Handling -- What To Do If X Goes Wrong

| Scenario | Action |
|---|---|
| `MONGO_URL` not set | Export from `.env` file: `export $(grep MONGO_URL backend/.env)` |
| Duplicate `rule_id` insert error | Expected -- script should log and skip. Check count of duplicates. If >10% are duplicates, stop and message A1. |
| Rule missing `rule_id` field | Log to error file. Do NOT insert the document. Report count to A1. |
| Dedup script crashes | Run `python3 -c "import sklearn"` to check if scikit-learn is installed. If not: `pip3 install scikit-learn`. |
| JSON parse error on a Rules file | Log filename and error. Skip that file. Report to A1. |
| Rule count mismatch (>5% fewer than expected) | Stop. Do NOT proceed to next book. Message A1 with: batch_id, expected count, actual count, list of files that had errors. |
| `insert_many` BulkWriteError | Script should catch and continue. Log error doc. Report error count post-run. |
| MongoDB timeout | Retry once with smaller batch size (add `--batch-size 50` flag to your script). |

---

## A2 Communication Protocol with A1

Message A1 at these gate points (do not proceed past each gate without response):

| Gate | Message to A1 |
|---|---|
| After Phase 1 | Audit results: rule counts per book, MongoDB current count, BPHS Vol 2 Ch49-51 question |
| After Phase 2 dry-run | Paste dry-run output for 300 Combinations -- counts + 3 sample documents |
| After Phase 3 (all 16 dedup pairs) | Send `ke_contradiction_pairs_master.md` -- counts of contradicts/partials per pair |
| Before starting Phase 4 | Final confirmation all gates cleared |
| After each Phase 4 book | Validation output from `validate_ingest_batch.py` |
| After Phase 6 complete | Final summary: total rules ingested, total contradiction pairs found, tracking files updated |

---

## A2 Log Template -- `KE_TEXTBOOK_DECODE/A2_INGEST_LOG.md`

Create this file immediately. Update after every action.

```markdown
# A2 Ingest Session Log
> Session start: [datetime]
> A2 account: Account 2

## Phase 1 -- Environment Audit
- [ ] Files read
- [ ] Python env verified
- [ ] MONGO_URL confirmed
- [ ] MongoDB baseline count: [number]
- [ ] Decode folder audit complete -- see table below

### Decode Folder Counts
| Book | Files | Total Rules | Active Rules |
|---|---|---|---|
...

## Phase 2 -- Ingest Script
- [ ] ingest_from_json_folder.py written
- [ ] Dry run on 300 Combinations: [count] rules, [count] would insert
- [ ] Dry run reviewed by A1: ✅ / ❌

## Phase 3 -- Dedup
- [ ] Dedup_Reports/ folder created
- [ ] Run 1 complete: BPHS1 vs BPHS2 -- [X contradicts, Y partials]
...
- [ ] ke_contradiction_pairs_master.md produced and sent to A1

## Phase 4 -- Live Ingest
| Book | Batch ID | Rules Inserted | Duplicates | Errors | Validated |
|---|---|---|---|---|---|
...

## Phase 5 -- Validation
...

## Phase 6 -- Tracking Updates
- [ ] BPHS_VOL1_INGEST.md updated
- [ ] New ingest tracking files created (5 books)
- [ ] INGEST_SUMMARY.md updated
- [ ] TEMPLE_TRACKER.md updated
- [ ] Knowledge_Engine/TRACKER.md updated (new version row)
```

---

## Summary -- Deliverables A2 Must Produce

| # | Deliverable | Location |
|---|---|---|
| 1 | `scripts/audit_decode_folders.py` | `backend/scripts/` |
| 2 | `scripts/ingest_from_json_folder.py` | `backend/scripts/` |
| 3 | `scripts/validate_ingest_batch.py` | `backend/scripts/` |
| 4 | 16 dedup report JSON files | `KE_TEXTBOOK_DECODE/Dedup_Reports/` |
| 5 | `ke_contradiction_pairs_master.md` | `KE_TEXTBOOK_DECODE/Dedup_Reports/` |
| 6 | `A2_INGEST_LOG.md` (complete, timestamped) | `KE_TEXTBOOK_DECODE/` |
| 7 | 5 new ingest tracking `.md` files | `.claude/ke/ingest/` |
| 8 | Updated `BPHS_VOL1_INGEST.md` | `.claude/ke/ingest/` |
| 9 | Updated `INGEST_SUMMARY.md` | `KE_TEXTBOOK_DECODE/` |
| 10 | Updated `TEMPLE_TRACKER.md` | repo root |
| 11 | New version row in `Codex_Deliveries/Knowledge_Engine/TRACKER.md` | repo |

---

*Brief prepared by A1 -- 2026-05-31. All strategic decisions remain with A1. A2 executes operational steps only.*
