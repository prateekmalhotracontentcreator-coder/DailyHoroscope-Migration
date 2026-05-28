# Lal Kitab (LK) -- Module Tracker
> Path: `Codex_Deliveries/LK/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-29 · v2.0

---

## Current Status

| Field | Value |
|---|---|
| **Status** | ✅ LIVE -- Standalone module built and integrated in A2 session (2026-05-09 to 2026-05-13) |
| **Frontend** | `frontend/src/pages/lk/` -- 7 pages live |
| **Backend** | `backend/lk_diagnostics.py` (272 lines) · `backend/lk_remedies_router.py` (348 lines) |
| **Router** | `server.py` line 133: `from lk_remedies_router import router as lk_router` · registered at line 3325 |
| **DB Collections** | `lalkitab_strategist` (823 records) · `jyotish_lk_remedies` (361 records) · `lk_user_profiles` (active) |
| **Live URLs** | `/lal-kitab-remedies` (public landing) · `/lk-remedies` (hub) · `/lk-remedies/onboard` · `/lk-remedies/report` · `/lk-remedies/tracker` · `/lk-remedies/debt-audit` · `/lk-remedies/remedies` |

---

## What Was Built (A2 Session, 2026-05-09 to 2026-05-13)

### Backend
| File | Lines | What It Does |
|---|---|---|
| `backend/lk_diagnostics.py` | 272 | 5-gate engine: Karmic Debt (IDs 483-615), House Awakening (636-650), 35-Year Cycle (526-575), Mercury Scan (626-635), Geographical (505-525 + 651-655), Debt Audit (601-615), Conflict Check (616-625) |
| `backend/lk_remedies_router.py` | 348 | `POST /api/lk/onboard`, `/api/lk/diagnose`, `/api/lk/conflict-check`, `/api/lk/debt-audit`, `/api/lk/tracker/log` · `GET /api/lk/tracker/{user_id}`, `/api/lk/remedies` |

### Frontend (7 pages in `frontend/src/pages/lk/`)
| Page | Route | Access |
|---|---|---|
| `LalKitabLandingPage.jsx` | `/lal-kitab-remedies` | Public SEO landing |
| `LKRemediesPage.jsx` | `/lk-remedies` | Free preview hub |
| `LKOnboardPage.jsx` | `/lk-remedies/onboard` | ProtectedRoute |
| `LKReportPage.jsx` | `/lk-remedies/report` | ProtectedRoute |
| `LKTrackerPage.jsx` | `/lk-remedies/tracker` | ProtectedRoute |
| `LKDebtAuditPage.jsx` | `/lk-remedies/debt-audit` | ProtectedRoute |
| `LKBrowsePage.jsx` | `/lk-remedies/remedies` | Public |

### Data Ingested (A2 session)
| Collection | Science ID | Records | Status |
|---|---|---|---|
| `knowledge_rules` (LK Remedies) | `jyotish_lk_remedies` | 361 | ✅ Live -- 0 Gate 0 errors |
| `knowledge_rules` (The Strategist) | `lalkitab_strategist` | 823 | ✅ Live (426 base + 22-record patch + 375 prior) |

### Other Changes in A2 Session
- **Rename**: "LK Remedies" → "Lal Kitab Remedies" across all 4 NavBar/UI display locations
- **Bug fix**: `_solar_event_jd` in `vedic_calculator.py` -- corrected `swe.rise_trans()` positional argument (`lon` was passed where `rsmi` expected)
- **KP integration**: 36 KP remedy records seeded to `krishna_prashnavali_remedies`

---

## Commission Status

| ID | Commission | Status | Notes |
|---|---|---|---|
| **LK-1** | LK Standalone Module (onboard, debt audit, 9-debt tracker, remedies) | ✅ INTEGRATED -- A2 session 2026-05-09 to 2026-05-13 | All 7 frontend pages + 2 backend files + router registration live. **PDF download not built** (see LK-OP-5). |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| LK-OP-5 | **Premium PDF download** not built | CC/Codex | 🟡 MED | Original LK-1 brief included password-protected PDF (`FirstName+BirthYear+Month` formula). Not implemented in A2 build. |
| LK-OP-6 | **5 split-required LK rules** -- `lalkitab-ch21-fam-04` + 4 age/infancy rules tagged `split_required=True` | NLM/TT | 🟡 MED | Rules affect quality but not blocking. NLM to review and provide splits. |
| LK-OP-7 | **96 in-range Master Doc records** not salvaged | NLM/TT | 🟡 MED | Unique master doc IDs not present in V2 -- need manual review. If worthwhile, add as suffix IDs (800A, 800B, etc.) per agreed protocol. |
| LK-OP-8 | **TT acceptance verification** on production | TT | 🟠 HIGH | Verify: `/lal-kitab-remedies` loads, onboard flow, diagnose returns 5 gates, debt audit, tracker persist, browse 361 records. |
| ~~LK-OP-1~~ | ~~Issue LK-1 to Codex~~ | -- | ✅ DONE | Built in A2 session -- not issued to Codex. Built directly. |
| ~~LK-OP-2~~ | ~~LK-1 must use existing MongoDB collections~~ | -- | ✅ SATISFIED | Confirmed: routes to `jyotish_lk_remedies` + `lalkitab_strategist`. |
| ~~LK-OP-3~~ | ~~All planetary/dasha data from `vedic_calculator.py`~~ | -- | ✅ SATISFIED | `lk_diagnostics.py` uses `vedic_calculator.py` for all dasha/planetary data. |
| LK-OP-4 | Slot 33 → LK Debt Audit cross-module trigger (PRAY verdict → surfaces Debt Audit) | TT | 🟡 MED | KP/LK cross-module feature. Parking lot. |

---

## Architecture Notes

- LK data underpins The Strategist's 5-gate karmic diagnostics (Gate 1 Pitru Rin, Gate 5 Digbala)
- 9 Lal Kitab debt types -- tracker is primary user-facing output
- `lk_diagnostics.py` is the 5-gate engine -- imports from `vedic_calculator.py`, never from `knowledge_engine.py`
- **Do NOT couple LK-1 UI with The Strategist UI in any future commission**

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-05-09 | LK-1 brief written. Collections confirmed seeded (462 + 361 records). Tracker created. | CC | `CODEX_COMMISSION_LK_STANDALONE_MODULE.md` |
| v2.0 | 2026-05-29 | **Full rewrite.** A2 session decode confirms LK-1 fully built in A2 (2026-05-09 to 2026-05-13). 7 frontend pages + 2 backend files live. 361 LK remedies + 823 Strategist records in MongoDB. Rename to Lal Kitab Remedies complete. 5 split-required rules + 96 salvage records still open. | CC Main Thread | A2 session export decode |
