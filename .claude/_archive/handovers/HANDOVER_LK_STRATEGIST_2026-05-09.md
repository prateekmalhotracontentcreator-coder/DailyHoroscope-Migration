# Handover Brief -- LK Module + The Strategist
> For: Claude Code Account 2
> Date: 2026-05-09
> Build mode: Option B -- Account 2 builds from specs

---

## Context

EverydayHoroscope (everydayhoroscope.in) is a Vedic astrology platform. The backend is FastAPI on Render, frontend is React on Vercel, database is MongoDB.

Two new modules need to be built. All data is already ingested and verified. You are building the application layer only.

---

## What's Already Done (Do Not Rebuild)

| Item | Status |
|---|---|
| 666 remedy records in MongoDB `knowledge_rules` collection | ✅ Live |
| Panchang engine (`panchang_router.py`) -- sunrise/sunset | ✅ Live |
| Birth chart engine (`vedic_calculator.py`) | ✅ Live |
| Razorpay subscription paywall | ✅ Live |
| Admin Console, Auth, all existing routes | ✅ Live |

Verify data: `python3 backend/scripts/verify_lk_remedies_v1.py --mongo-url "$MONGO_URL"`

---

## Module 1: LK Standalone

**Full spec:** `.claude/LK_STANDALONE_MODULE_SPEC.md`

**Build order:**
1. `backend/lk_remedies_router.py` -- all `/api/lk/*` routes
2. `backend/lk_diagnostics.py` -- 5-gate query engine
3. Frontend pages (Onboard → Report → Tracker → Debt Audit → Browse)
4. Wire router into `server.py`, pages into `App.js`

**Start here:** Read `LK_STANDALONE_MODULE_SPEC.md` fully before writing any code.

---

## Module 2: The Strategist

**Full spec:** `.claude/THE_STRATEGIST_SPEC.md`

**Dependency:** LK Standalone must be live first (Strategist calls `/api/lk/diagnose`).

**Build order:**
1. `backend/scripts/ingest_strategist_v1.py` -- ingest Strategist records (read source doc first)
2. `backend/strategist_engine.py` -- mission triggers, probability calc, surrogate logic
3. `backend/strategist_router.py` -- all `/api/strategist/*` routes
4. Frontend War Room pages
5. Wire in `server.py` and `App.js`

**Source docs to read:**
- `/Users/apple/Documents/Knowledge Engine_eBooks/Remedies + The Strategist/7. Lal Kitab_Career_The Strategist_Master Document (1).md`
- `/Users/apple/Documents/Knowledge Engine_eBooks/Remedies + The Strategist/The Strategist Module_LLM Specific Q&A_GAI.md`

**Critical ID note:** Surrogate rows in Q&A show IDs 651-675. Ingest them as **701-725** (ID 651-668 already used by `jyotish_lk_remedies`).

---

## Architecture Rules (MANDATORY)

1. ALL live astronomical/dasha data from `vedic_calculator.py` only -- never replicate
2. Call `vedic_calculator.calculate_vimshottari_dasha()` for dasha -- never rewrite
3. `knowledge_rules` collection uses `science_id` to partition -- always filter by it
4. `approval_status: "pending_human_review"` on all new records
5. Follow Temple App theme from `CLAUDE.md §11`
6. Commit format: `feat(lk): description` / `feat(strategist): description`

---

## Environment

- `MONGO_URL` -- set on Render, also in local `.env`
- `DB_NAME` -- `horoscope_db`
- All other env vars in `CLAUDE.md §12`

## LK Standalone -- Phased Build Order (Within Module)

Build in this exact order to avoid dependency failures:

1. `lk_remedies_router.py` + `lk_diagnostics.py` (backend core)
2. `POST /api/lk/onboard` + `lk_user_profiles` collection (prerequisite for all other routes)
3. `POST /api/lk/diagnose` (5-gate engine -- depends on user profile)
4. `POST /api/lk/conflict-check` (safe to build in parallel with step 3)
5. `POST /api/lk/debt-audit` (depends on user profile)
6. `GET|POST /api/lk/tracker` (depends on diagnose output for remedy IDs)
7. Frontend: Onboard → Report → Conflict Modal → Debt Audit → Tracker → Browse

---

## Additional GAI Reference Files (Read Before Building)

These supplement the specs with structural query patterns and edge cases:

```
/Users/apple/Documents/Knowledge Engine_eBooks/Remedies + The Strategist/
  Lal Kitab Remedies_Claude Code 5 Structural Query Responses_GAI.md
  Lal Kitab Remedies_Claude Code 5 Structural Query Responses+1_Master Testig Ingestion Logic_GAI.md
  Lal Kitab_Remedies_Gap Fill_Update from GAI.md
  Section B_ Additional Information by GAI to supplyment our Lal Kitab Remedies Ingest Plan.md
```

For Strategist specifically -- read these before writing `ingest_strategist_v1.py`:
```
  7. Lal Kitab_Career_The Strategist_Master Document (1).md   ← primary source
  The Strategist Module_LLM Specific Q&A_GAI.md               ← IDs 953-1027, surrogates
```

---

## Verification After Build

```bash
# LK data health
python3 backend/scripts/verify_lk_remedies_v1.py --mongo-url "$MONGO_URL"

# LK 5-gate test
python3 backend/scripts/master_test_query_lk.py --mongo-url "$MONGO_URL"

# Strategist ingest dry-run
python3 backend/scripts/ingest_strategist_v1.py --mongo-url "$MONGO_URL" --dry-run
```
