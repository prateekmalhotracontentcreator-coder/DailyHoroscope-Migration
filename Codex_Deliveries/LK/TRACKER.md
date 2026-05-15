# Lal Kitab (LK) -- Module Tracker
> Path: `Codex_Deliveries/LK/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-15 · v1.0

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟣 PLANNED -- data feeds The Strategist, no standalone UI yet |
| **Frontend** | None (standalone) -- LK data surfaces via The Strategist |
| **Backend** | LK data embedded in `backend/strategist_router.py` + `backend/strategist_engine.py` |
| **DB Collections** | `lalkitab_strategist` (462 records) · `jyotish_lk_remedies` (361 records) · `lk_user_profiles` schema exists |
| **Live URL** | None standalone -- see `/strategist` |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| **LK-1** | LK Standalone Module (onboard, debt audit, 9-debt tracker, remedies, PDF) | 🟣 READY TO ISSUE | `CODEX_COMMISSION_LK_STANDALONE_MODULE.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| LK-OP-1 | **Issue LK-1 to Codex** (Week 4+) | TT | 🟡 MED | Full standalone module: onboarding wizard, debt audit, planetary remedies by house, 43-day tracker, premium PDF |
| LK-OP-2 | LK-1 must use existing MongoDB collections -- do NOT create new ones | CX | 🔴 ENFORCE | Route new LK UI to `jyotish_lk_remedies` + `lalkitab_strategist` -- already seeded |
| LK-OP-3 | All planetary/dasha data from `vedic_calculator.py` | CX | 🔴 ENFORCE | Architecture rule |
| LK-OP-4 | Slot 33 → LK Debt Audit cross-module trigger (PRAY verdict → surfaces Debt Audit) -- Phase 2 | TT | 🟡 MED | KP / LK cross-module feature. Parking lot for now. |

---

## Architecture Notes

- LK data underpins The Strategist's 5-gate karmic diagnostics (Gate 1 Pitru Rin, Gate 5 Digbala)
- 9 Lal Kitab debt types -- tracker is the primary user-facing output
- LK-1 is independent of The Strategist UI -- do not couple the two in the same commission

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-05-09 | LK-1 brief written. Collections confirmed seeded (462 + 361 records). Tracker created. | CC | `CODEX_COMMISSION_LK_STANDALONE_MODULE.md` |
