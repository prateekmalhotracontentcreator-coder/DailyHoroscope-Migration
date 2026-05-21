# Longevity Report -- Module Tracker
> Path: `Codex_Deliveries/Longevity/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-22 IST · v1.2

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- LON-1 runtime alignment pass delivered locally and build-verified; Temple review pending |
| **Frontend** | `frontend/src/pages/reports/LongevityReportPage.jsx` at `/longevity` |
| **Backend** | `backend/longevity_router.py` and `backend/kp_engine.py` |
| **Public Landing** | `frontend/src/pages/reports/LongevityLanding.jsx` at `/the-longevity-report` |
| **Saved Report Route** | `/longevity/report/:reportId` |

---

## LON-1 Delivery Focus

This session treated LON-1 as a contract-alignment pass on the existing runtime Longevity module, not as a greenfield build.

Delivered in runtime:

- Added contract-facing Longevity endpoint aliases:
  - `POST /api/longevity/report`
  - `POST /api/longevity/save`
  - `GET /api/longevity/my-reports`
  - `GET /api/longevity/alerts`
  - `GET /api/longevity/report/{report_id}`
- Preserved the stronger existing runtime endpoints:
  - `GET /api/longevity/eligibility`
  - `POST /api/longevity/generate`
  - `GET /api/longevity/history`
  - `GET /api/longevity/reports/{report_id}`
- Added `full_report_markdown` support to the narrative layer with a clean deterministic fallback
- Added saved-report route loading and explicit save flow on the frontend

---

## Runtime Alignment Notes

- The live module already had richer behavior than the written contract in a few places:
  - Shared city search via `SharedBirthCityPicker`
  - Premium preview flow on `/longevity`
  - Auto-persist on full entitled generation
- LON-1 preserved those stronger runtime behaviors while adding the contract-facing API and route surface instead of removing the live conveniences.

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| LON-H | Commission H brief (older, superseded) | SUPERSEDED | `_archive/CODEX_COMMISSION_H_BRIEF_v2026-04-10.md` |
| **LON-1** | Ayur Jyotish Longevity Report (main contract) | 🟡 DELIVERED LOCALLY -- Temple review pending | `CODEX_COMMISSION_LONGEVITY_REPORT_CONTRACT.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| LON-OP-1 | Temple runtime review of Longevity endpoint loading and full report flow | TT | 🟠 HIGH | Verify the new alias endpoints and `/longevity/report/:reportId` route in the live app |
| LON-OP-2 | Confirm whether the current preview-plus-premium UX is the accepted canonical interpretation of LON-1 | TT | 🟡 MED | Existing runtime flow is stronger than the older contract wording |
| LON-OP-3 | Decide whether a later pass should add PDF/share-card parity | TT | 🟢 NOTE | Not required for this alignment slice |

---

## Verification

- Backend verification: `PYTHONPYCACHEPREFIX=/private/tmp/longevity-pyc python3 -m py_compile backend/longevity_router.py backend/kp_engine.py backend/server.py`
- Frontend verification: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
- Result: passed

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-04-10 | LON-1 main contract brief written, superseding Commission H. | CC | `CODEX_COMMISSION_LONGEVITY_REPORT_CONTRACT.md` |
| v1.1 | 2026-05-17 | KE Sprint 2 gate cleared; LON-1 marked ready to issue. | CC | -- |
| v1.2 | 2026-05-22 | LON-1 delivered locally as a runtime alignment pass. Added contract-facing endpoint aliases, save/alerts/detail support, full narrative markdown fallback, saved-report route loading, and explicit save UX. Backend compile and frontend production build passed. | Codex | 2026-05-22 |
