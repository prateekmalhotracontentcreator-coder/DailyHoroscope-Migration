# Kundali / Birth Chart -- Module Tracker
> Path: `Codex_Deliveries/Kundali/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-15 · v1.0

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟣 PLANNED -- basic UI live, full Kundali module pending |
| **Frontend (live)** | `frontend/src/pages/BirthChartPage.jsx` · `frontend/src/pages/BrihatKundliPage.jsx` |
| **Backend** | `backend/vedic_calculator.py` -- single source of truth for all computation |
| **Live URLs** | `/birth-chart` · `/brihat-kundali` |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| KUN-Shadbala | Shadbala Engine (`vedic_calculator.py`) | ✅ INTEGRATED | `_archive/CODEX_COMMISSION_SHADBALA_ENGINE_delivered.md` |
| **KUN-1** | Lagna Kundali Module Contract (full UI + chart + dasha + PDF) | 🟣 READY TO ISSUE | `CODEX_COMMISSION_KUNDALI_LAGNA_CONTRACT.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| KUN-OP-1 | **Issue KUN-1 to Codex** (Week 4+) | TT | 🟡 MED | Large scope: house descriptions, planet-in-sign, dasha timeline visualisation, transit overlay, premium PDF |
| KUN-OP-2 | KUN-1 must NOT touch `vedic_calculator.py` computation logic | CX | 🔴 ENFORCE | Visual and interpretive layer only. All chart data from existing backend endpoints. |
| KUN-OP-3 | Do NOT add dasha calculation functions to `knowledge_engine.py` as part of KUN-1 | CX | 🔴 ENFORCE | Architecture rule -- all dasha data from `vedic_calculator.py` |

---

## Architecture Notes

- `vedic_calculator.py` is the SINGLE SOURCE OF TRUTH for all birth chart and dasha computation
- Key functions: `calculate_vimshottari_dasha(birth_date, moon_longitude)` · `get_current_dasha(dashas)`
- `DASHA_ORDER = ['Ketu','Venus','Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury']`
- `DASHA_YEARS = {'Ketu':7,'Venus':20,'Sun':6,'Moon':10,'Mars':7,'Rahu':18,'Jupiter':16,'Saturn':19,'Mercury':17}`

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-04-25 | Shadbala Engine integrated. KUN-1 brief written. Tracker created. | Codex + CC | `_archive/CODEX_COMMISSION_SHADBALA_ENGINE_delivered.md` |
