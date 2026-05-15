# Remedies Engine -- Module Tracker
> Path: `Codex_Deliveries/Remedies/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-15 · v1.1

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- all endpoints live · `krishna_prashnavali_remedies` seeded · REM-P1 ready to issue |
| **Backend** | `backend/remedies_router.py` |
| **DB Collections** | `krishna_prashnavali_remedies` (36 records seeded 2026-05-15) · `jyotish_lk_remedies` |
| **Live endpoints** | `GET /api/remedies/admin/records` · `GET /api/remedies/ref/{remedy_ref_id}` (line 827) · `GET /api/remedies/traditions` |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| **REM-P1** | Remedies Engine Phase 1 (KP collection + remedy_ref pipeline + admin frontend) | 🟣 READY TO ISSUE | `CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| ~~REM-OP-1~~ | ~~**Add `/api/remedies/ref/{remedy_ref_id}` endpoint**~~ | CC | ✅ CONFIRMED PRESENT | Endpoint already existed at `remedies_router.py` line 827 with `{"_id": 0}` projection. Was a false alarm -- confirmed live 2026-05-15. |
| ~~REM-OP-2~~ | ~~Run `ingest_krishna_prashnavali_remedies_v1.py` on Render~~ | TT | ✅ DONE | Run 2026-05-15. upserted=0, modified=36. Collection was already seeded; all 36 records refreshed with current bundle. |
| REM-OP-3 | **Issue REM-P1 to Codex** | TT | 🟠 HIGH | All prerequisites met. `/ref/` endpoint live, collection seeded. Brief at `CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md`. |

---

## Architecture Notes

- `/api/remedies/ref/{remedy_ref_id}` is a **Claude Code direct fix** -- single endpoint, do not open a Codex thread for this
- REM-P1 covers: admin-facing remedy browser frontend + full `remedy_ref` pipeline validation
- Do NOT create new MongoDB collections -- route all new remedy UI to existing `krishna_prashnavali_remedies` and `jyotish_lk_remedies`

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-05-14 | REM-P1 brief written. Collections confirmed seeded. | CC | `CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md` |
| v1.1 | 2026-05-15 | REM-OP-1 (`/ref/` endpoint) identified as CC direct fix. Tracker created. | CC | This session |
| v1.2 | 2026-05-15 | REM-OP-1 confirmed false alarm -- endpoint already live at line 827. REM-OP-2 closed -- 36 records seeded (upserted=0, modified=36). REM-P1 fully unblocked. | CC + TT | 2026-05-15 |
