# Kundali / Birth Chart -- Module Tracker
> Path: `Codex_Deliveries/Kundali/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-22 · v2.0

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- KUN-1 integrated; open points below |
| **Frontend (live)** | `frontend/src/pages/kundali/KundaliPage.jsx` (full workspace) · `frontend/src/pages/BirthChartPage.jsx` · `frontend/src/pages/BrihatKundliPage.jsx` |
| **Backend** | `backend/vedic_calculator.py` -- single source of truth for all computation · `backend/kundali_router.py` |
| **Live URLs** | `/kundali` (free public) · `/kundali/view/:chartId` (free public, saved chart) · `/lagna-kundali` (premium gated) · `/birth-chart` · `/brihat-kundali` |
| **User Manual** | `docs/LAGNA_KUNDALI_USER_MANUAL.md` |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| KUN-Shadbala | Shadbala Engine (`vedic_calculator.py`) | ✅ INTEGRATED | `_archive/CODEX_COMMISSION_SHADBALA_ENGINE_delivered.md` |
| **KUN-1** | Lagna Kundali Frontend Module | ✅ INTEGRATED -- commits `1d6fc47` + `e741ee5` | `CODEX_COMMISSION_KUNDALI_LAGNA_CONTRACT.md` |

---

## KUN-1 Integration Notes (2026-05-22)

Codex delivered to worktree (`/Documents/New project/ke_phase2a_worktree/`). CC applied targeted edits to main repo rather than wholesale replacement.

**What was integrated:**
- `/kundali` public free route in `App.js` (no PremiumRoute gate)
- `/kundali/view/:chartId` public free route in `App.js`
- `/lagna-kundali` premium route preserved unchanged
- `unknownBirthTime` checkbox -- locks time to 12:00 noon, sets precision to Unknown, restricts Dasha/Shadbala tabs
- House Summary table (House | Rashi | Lord for all 12 houses) added to Kundali tab
- Route-aware SEO: `/kundali` indexed with public title/description/canonical; `/lagna-kundali` stays noindex
- User Manual: `docs/LAGNA_KUNDALI_USER_MANUAL.md` (all 8 tabs, dual chart workspace, free vs premium table, glossary)

**What was NOT integrated:**
- Share button / clipboard copy feature (deferred -- share is premium paid reports only per TT direction)

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| KUN-OP-2 | Architecture rule: KUN-1 must NOT touch `vedic_calculator.py` computation logic | CX | 🔴 ENFORCE | Visual + interpretive layer only. All chart data from existing backend endpoints. |
| KUN-OP-3 | Architecture rule: Do NOT add dasha calc functions to `knowledge_engine.py` | CX | 🔴 ENFORCE | All dasha data from `vedic_calculator.py` |
| KUN-OP-4 | TT browser smoke test of `/kundali` free route | TT | 🟡 MED | Verify generate D1, save chart, unknown birth time checkbox, House Summary table visible. |
| KUN-OP-5 | Share Report feature (premium only) | TT | 🟢 LOW | Not in free Kundali. To be built as part of future premium paid report delivery flow. |

---

## Architecture Notes

- `vedic_calculator.py` is the SINGLE SOURCE OF TRUTH for all birth chart and dasha computation
- Key functions: `calculate_vimshottari_dasha(birth_date, moon_longitude)` · `get_current_dasha(dashas)`
- `DASHA_ORDER = ['Ketu','Venus','Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury']`
- `DASHA_YEARS = {'Ketu':7,'Venus':20,'Sun':6,'Moon':10,'Mars':7,'Rahu':18,'Jupiter':16,'Saturn':19,'Mercury':17}`
- Free `/kundali` entry point is designed to drive registrations -- logged-in users who register are one step closer to monetisation

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-04-25 | Shadbala Engine integrated. KUN-1 brief written. Tracker created. | Codex + CC | `_archive/CODEX_COMMISSION_SHADBALA_ENGINE_delivered.md` |
| v2.0 | 2026-05-22 | KUN-1 integrated. Public `/kundali` route, unknown birth time checkbox, House Summary table, route-aware SEO, User Manual. | CC | commits `1d6fc47` · `e741ee5` |
