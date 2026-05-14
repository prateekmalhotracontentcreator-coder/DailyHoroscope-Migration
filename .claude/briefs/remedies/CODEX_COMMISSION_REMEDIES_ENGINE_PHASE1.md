# Remedies Engine Phase 1 -- Codex Commission Brief
> EverydayHoroscope / Temple App | Issued: 2026-05-14
> Assignee: Codex (new thread)
> Status: Ready to execute -- all prerequisites confirmed live

---

## 1. What You Are Building

The Remedies Engine Phase 1 connects the Krishna Prashnavali oracle to a structured remedy database in MongoDB. The primary deliverables are:

1. **Run the ingest script** -- loads 36 pre-authored remedy records into `horoscope_db.krishna_prashnavali_remedies`
2. **Add one new API endpoint** -- `GET /api/remedies/ref/{remedy_ref_id}` in `remedies_router.py`
3. **Verify the Engine fallback wiring** -- `scriptural_oracle_router.py` already calls this collection; confirm it works end-to-end
4. **Run smoke tests** -- confirm the KP reading flow returns structured remedy data from the collection

**Out of scope for this commission:**
- KP v2 bundle swap (`KRISHNA_ORACLE_CONTENT_CANONICAL_V2_FOR_TEMPLE.json`) -- this is a separate commission that depends on Phase 1 being done first
- Lal Kitab, Crystal Therapy, Feng Shui ingestion -- Phase 2
- Remedies Engine `POST /api/remedies/suggest` logic changes -- already functional in live router

---

## 2. Live Repo

```
Repo: github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration
Local: /Users/apple/DailyHoroscope-Migration/
Frontend: React → Vercel (~2 min deploy)
Backend: FastAPI → Render Docker (~3 min deploy)
DB: MongoDB Motor async -- DB_NAME=horoscope_db
```

**Always work in the live Temple repo, not any Codex-Test folder.**

---

## 3. What Already Exists (Do Not Rebuild)

### 3A. Ingest Script -- WRITTEN, NOT YET RUN

File: `backend/scripts/ingest_krishna_prashnavali_remedies_v1.py` (140 lines)

This script is complete. It:
- Loads `KRISHNA_PRASHNAVALI_REMEDIES_INGEST_V1.json` (36 records) from `/Users/apple/Documents/New project/`
- Validates remedy_id uniqueness and science_id consistency
- Upserts into `horoscope_db.krishna_prashnavali_remedies` via `UpdateOne(upsert=True)`
- Usage: `--dry-run` | `--save FILE` | `--upload --mongo-url "$MONGO_URL" --db-name horoscope_db`

**Your job: run it (dry-run first, then upload).**

### 3B. Engine Fallback -- ALREADY WIRED in `scriptural_oracle_router.py`

The `KrishnaCanonicalAnswer` model has a `remedy_ref` field (line 70):
```python
remedy_ref: str | None = None  # v2 bundle: lookup key → krishna_prashnavali_remedies
```

The resolver function (line 275):
```python
async def _resolve_kp_remedy_doc(request: Request, remedy_ref: str) -> dict[str, Any] | None:
    db = request.app.state.db
    col = db["krishna_prashnavali_remedies"]
    return await col.find_one({"remedy_id": remedy_ref, "approval_status": "approved"})
```

The fallback call (lines 592-596):
```python
# Engine fallback: only called when bundle behavioral_remedy is absent AND remedy_ref exists
ritual_remedy_doc: dict[str, Any] | None = None
bundle_remedy_missing = not (answer.behavioral_remedy and answer.behavioral_remedy.english_block)
if bundle_remedy_missing and answer.remedy_ref:
    ritual_remedy_doc = await _resolve_kp_remedy_doc(request, answer.remedy_ref)
```

The remedy doc flows into `_summary_report()` and `_practical_action_block()` at line 617. The `sacred_mantra` field also uses it (lines 512-517).

**This wiring is complete. Do NOT rewrite it.**

### 3C. Existing `GET /api/remedies/rule/{remedy_id}` Endpoint

`remedies_router.py` line 808 has a `GET /api/remedies/rule/{remedy_id}` endpoint. This route works but uses a different code path with collection aliasing. You need to add a simpler, clean `/ref/` endpoint (see Section 5 below) -- do not modify the existing `/rule/` endpoint.

---

## 4. Source Data

### 4A. JSON Ingest File

```
Path: /Users/apple/Documents/New project/KRISHNA_PRASHNAVALI_REMEDIES_INGEST_V1.json
Expected record count: 36
Science ID on all records: "krishna_prashnavali_remedies"
```

Each record follows this schema (abridged):
```json
{
  "remedy_id": "KPR-001",
  "science_id": "krishna_prashnavali_remedies",
  "answer_id": "KP36-01",
  "approval_status": "approved",
  "verdict_display": "SUCCESS | PATIENCE | WARNING | SURRENDER",
  "title": {
    "english_block": "...",
    "sanskrit_block": "..."
  },
  "ritual_remedy": {
    "english_block": "Full ritual instruction text",
    "sanskrit_block": "Hindi equivalent"
  },
  "mantra": {
    "english_block": "Om Shri Krishnaya Namah",
    "sanskrit_block": "ॐ श्री कृष्णाय नमः"
  },
  "behavioral_display_hint": {
    "english_block": "Contemplative practice hint",
    "sanskrit_block": "..."
  }
}
```

### 4B. MongoDB Collection Target

```
Database: horoscope_db
Collection: krishna_prashnavali_remedies
Index required: { remedy_id: 1 } unique
Index required: { answer_id: 1 }
Index required: { approval_status: 1 }
```

---

## 5. Task 1 -- Run the Ingest Script

### Step 1: Dry run (no DB writes)

```bash
cd /Users/apple/DailyHoroscope-Migration
python3 backend/scripts/ingest_krishna_prashnavali_remedies_v1.py --dry-run
```

Expected output:
```
Total records: 36
Science ID:    krishna_prashnavali_remedies
Collection:    krishna_prashnavali_remedies
Verdict split:
  SUCCESS     9
  PATIENCE    9
  WARNING     9
  SURRENDER   9
```

If counts differ or any validation error appears → **stop and report to Prateek before uploading**.

### Step 2: Upload to MongoDB

```bash
python3 backend/scripts/ingest_krishna_prashnavali_remedies_v1.py \
  --upload \
  --mongo-url "$MONGO_URL" \
  --db-name horoscope_db
```

Expected output: `Imported 36 Krishna remedy records → horoscope_db.krishna_prashnavali_remedies (upserted=36, modified=0)`

### Step 3: Verify in MongoDB

```python
# Quick verification query (Motor or pymongo)
count = await db.krishna_prashnavali_remedies.count_documents({"approval_status": "approved"})
# Expected: 36
```

### Step 4: Create Indexes

```python
await db.krishna_prashnavali_remedies.create_index("remedy_id", unique=True)
await db.krishna_prashnavali_remedies.create_index("answer_id")
await db.krishna_prashnavali_remedies.create_index("approval_status")
```

Run this as a one-shot script or add to a startup migration. Do not add index creation to the FastAPI lifespan -- it is already handled by Motor's lazy index creation on first query if you use `ensure_index` patterns, but explicit creation is preferred for production.

---

## 6. Task 2 -- Add `GET /api/remedies/ref/{remedy_ref_id}` Endpoint

File: `backend/remedies_router.py`

Add this endpoint. Insert it **after** the existing `GET /api/remedies/rule/{remedy_id}` block (currently at line 808). Do not modify any existing endpoints.

```python
@router.get("/ref/{remedy_ref_id}")
async def get_remedy_by_ref(
    remedy_ref_id: str,
    request: Request,
) -> dict[str, Any]:
    """
    Fetch a single Krishna Prashnavali remedy record by remedy_ref lookup key.
    Only returns records with approval_status=approved.
    Called by: scriptural_oracle_router (Engine fallback), frontend direct lookup.
    """
    db = _get_db(request)
    doc = await db["krishna_prashnavali_remedies"].find_one(
        {"remedy_id": remedy_ref_id, "approval_status": "approved"},
        {"_id": 0},
    )
    if not doc:
        raise HTTPException(
            status_code=404,
            detail=f"Remedy ref '{remedy_ref_id}' not found or not approved",
        )
    return {"remedy_ref_id": remedy_ref_id, "remedy": doc}
```

**Constraints:**
- Return `{"_id": 0}` projection -- never expose MongoDB `_id` to the client
- `approval_status: "approved"` filter is mandatory -- same gate as all other knowledge engine routes
- Do not add auth gating -- this is a public read endpoint (same as `/traditions`, `/rule/{id}`)
- Return shape: `{ "remedy_ref_id": str, "remedy": { full doc } }`

---

## 7. Task 3 -- Verify End-to-End Engine Fallback

The `scriptural_oracle_router.py` fallback (Section 3B) is already wired. After the collection is populated, verify it works:

### Verification Steps

**Step 1: Hit the KP reading endpoint with a real payload**

```bash
curl -s -X POST https://everydayhoroscope-api.onrender.com/api/krishna-prashnavali/reading \
  -H "Content-Type: application/json" \
  -d '{
    "row": 1,
    "col": 1,
    "sequence_indices": [0, 5, 12, 18, 24],
    "question_text": "Should I proceed with this endeavour?",
    "focus_area": "career"
  }' | python3 -m json.tool | grep -A 5 "behavioral_remedy\|sacred_mantra\|practical_action"
```

**Step 2: Confirm remedy data is from the Engine (not provisional)**

A provisional fallback (pre-ingest) will show:
```
"sacred_mantra": { "sanskrit_block": "ॐ श्री कृष्णाय नमः", "english_block": "Om Shri Krishnaya Namah" }
```

After the collection is populated AND the KP v2 bundle (separate commission) provides a `remedy_ref` in the answer, the `sacred_mantra` and `behavioral_remedy` fields will be sourced from `krishna_prashnavali_remedies`.

**Note:** Full Engine fallback activation requires the KP v2 bundle to supply `remedy_ref` values. The Phase 1 commission establishes the collection and endpoint so the v2 bundle commission can proceed. If the current bundle (v1) does not set `remedy_ref`, the Engine fallback at line 595 (`if bundle_remedy_missing and answer.remedy_ref:`) will not fire -- this is expected behaviour. Do not modify this conditional.

**Step 3: Hit the new `/ref/` endpoint directly**

Once the collection is populated, test the new endpoint:

```bash
curl -s https://everydayhoroscope-api.onrender.com/api/remedies/ref/KPR-001 | python3 -m json.tool
```

Expected: `{ "remedy_ref_id": "KPR-001", "remedy": { ...full record... } }`

---

## 8. Commit Protocol

Use these commit messages exactly:

```
feat(remedies): ingest 36 KP remedy records into krishna_prashnavali_remedies
feat(remedies): add GET /api/remedies/ref/{remedy_ref_id} endpoint
```

Commit separately -- one commit per task. Do not bundle.

The `MONGO_URL` env var is set in Render. Do not hardcode it. The ingest script reads it from the environment when `--upload` is used.

---

## 9. Architecture Constraints -- Read Before Writing Any Code

1. **No astrology computation in remedies code.** The remedies layer only reads MongoDB. If you ever need live chart data, call `vedic_calculator.py`. Never duplicate its functions.

2. **No hardcoded remedy text in Python.** All content (mantras, ritual instructions, titles) lives in MongoDB. Python only contains routing and query logic.

3. **`approval_status: "approved"` gate is mandatory** on every user-facing query. Admin routes may bypass this but must be explicitly gated with `require_admin`.

4. **Motor async only.** No synchronous pymongo calls inside FastAPI routes. Use `await` on all DB operations.

5. **KP v2 bundle is a separate commission.** Do not touch `KRISHNA_ORACLE_CONTENT_CANONICAL_V2_FOR_TEMPLE.json`, do not swap the bundle file, do not update `scriptural_oracle_router.py` beyond what is documented here.

6. **Smart-quote hygiene.** If you write any Python files or edit any JSON, ensure no curly quotes (`"`, `"`, `'`, `'`) appear in code. Use straight ASCII quotes only.

7. **Build verification before committing.** Run: `cd frontend && CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` -- must exit 0. This commission is backend-only so no frontend build is strictly required, but run it if you touch any frontend file.

---

## 10. Files to Touch (Exact List)

| File | Action |
|---|---|
| `backend/scripts/ingest_krishna_prashnavali_remedies_v1.py` | Run only -- do not edit |
| `backend/remedies_router.py` | Add one endpoint (Section 6) |
| `backend/scriptural_oracle_router.py` | Read-only verification -- do not edit |

**Do not touch any other file.**

---

## 11. Definition of Done

- [ ] `python3 backend/scripts/ingest_krishna_prashnavali_remedies_v1.py --dry-run` shows 36 records, 4 verdict buckets of 9 each
- [ ] `--upload` run shows `upserted=36, modified=0`
- [ ] `db.krishna_prashnavali_remedies.count_documents({"approval_status": "approved"})` returns 36
- [ ] `GET /api/remedies/ref/KPR-001` (or any valid remedy_ref_id) returns HTTP 200 with remedy doc
- [ ] `GET /api/remedies/ref/DOES-NOT-EXIST` returns HTTP 404
- [ ] KP reading endpoint (`POST /api/krishna-prashnavali/reading`) still returns HTTP 200 with no regression
- [ ] Two clean commits pushed: one for ingest verification docs, one for the new endpoint
- [ ] Summary report to Prateek: record count confirmed, endpoint URL, sample response

---

## 12. Reference Files

| File | Purpose |
|---|---|
| `.claude/REMEDIES_ENGINE_SPEC_V1.md` | Full architecture spec -- read for broader context |
| `.claude/MASTER_DECISIONS_18_MODULE_RECONCILIATION_2026-05-14.md` | Module decisions -- Section 4 Remedies Engine row |
| `backend/remedies_router.py` | Live router -- add endpoint here |
| `backend/scriptural_oracle_router.py` | KP oracle -- Engine fallback already wired |
| `backend/scripts/ingest_krishna_prashnavali_remedies_v1.py` | Ingest script -- run, do not edit |
| `/Users/apple/Documents/New project/KRISHNA_PRASHNAVALI_REMEDIES_INGEST_V1.json` | Source data -- 36 records |
