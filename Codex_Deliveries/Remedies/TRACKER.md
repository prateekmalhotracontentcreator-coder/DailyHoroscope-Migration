# Remedies Engine -- Module Tracker
> Path: `Codex_Deliveries/Remedies/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-15 · v1.1

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- collections seeded, `/ref/` endpoint missing |
| **Backend** | `backend/remedies_router.py` |
| **DB Collections** | `krishna_prashnavali_remedies` · `jyotish_lk_remedies` |
| **Live endpoint** | `GET /api/remedies/admin/records` (admin only) |
| **Missing endpoint** | `GET /api/remedies/ref/{remedy_ref_id}` -- CC direct fix required |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| **REM-P1** | Remedies Engine Phase 1 (KP collection + remedy_ref pipeline + admin frontend) | 🟣 READY TO ISSUE | `CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| REM-OP-1 | **Add `/api/remedies/ref/{remedy_ref_id}` endpoint** to `remedies_router.py` | CC | 🔴 HIGH | Lookup `remedy_ref_id` in `krishna_prashnavali_remedies` collection. Simple GET. Must land before KP-2A integration. NOT a Codex commission. |
| REM-OP-2 | Run `ingest_krishna_prashnavali_remedies_v1.py` on Render if not already seeded | TT | 🟠 HIGH | Prerequisite for remedy_ref pipeline to work |
| REM-OP-3 | **Issue REM-P1 to Codex** (Week 2) | TT | 🟠 HIGH | After `/ref/` endpoint (REM-OP-1) is live |

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
