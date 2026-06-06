# Longevity Report -- Module Tracker
> Path: `Codex_Deliveries/Longevity/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-22 IST · v1.2

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- LON-1 ✅ integrated. LON-2 brief written and READY TO ISSUE (KP Engine Foundation + chart panel). |
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
| **Commission H** | Ayur Jyotish Longevity & Health Report -- the ONLY Codex brief ever issued for this module. Delivered by Codex, integrated commit `2a4ed4e` 2026-05-22. "LON-1" was a CC tracking label for this delivery -- not a separate commission. | ✅ INTEGRATED | `CODEX_COMMISSION_LONGEVITY_REPORT_CONTRACT.md` (updated from `_archive/CODEX_COMMISSION_H_BRIEF_v2026-04-10.md`) |
| **LON-2** | KP Engine Foundation Layer + Longevity Report Phase 2 -- first real numbered commission | ✅ DELIVERED -- CC VERIFIED 2026-06-07 | `CODEX_COMMISSION_LON_2_KP_ENGINE_FOUNDATION.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| LON-OP-1 | Temple runtime review of Longevity endpoint loading and full report flow | TT | ✅ CLEARED 2026-06-07 | Report confirmed working in production. |
| LON-OP-2 | Confirm preview-plus-premium UX as accepted canonical | TT | ✅ CLEARED 2026-06-07 | Report live and verified by TT. |
| LON-OP-3 | PDF/share-card parity | TT | 🟢 NOTE | Deferred to LON-3 |
| LON-OP-4 | KP Chart Panel delivered (LON-2). TT: verify panel renders on live Longevity Report. | TT | 🟠 HIGH | Collapsible "Your KP Chart" section above Section 01. Requires push + Render deploy. |
| LON-OP-5 | BSON integer-key crash fixed (commit `8a69611`) | ✅ FIXED | -- | `dasha_health_intensity` and all house_lords/signs/cusps now string-keyed. |
| LON-OP-6 | Arc Angel upsert conflict fixed (commit `8591f2b`) | ✅ FIXED | -- | `_upsert_arc_angel_profile_doc` `$setOnInsert` removed. |

---

## Verification

- Backend verification: `PYTHONPYCACHEPREFIX=/private/tmp/longevity-pyc python3 -m py_compile backend/longevity_router.py backend/kp_engine.py backend/server.py`
- Frontend verification: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
- Result: passed

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-04-10 | Commission H brief written. The contract file was updated/renamed to `CODEX_COMMISSION_LONGEVITY_REPORT_CONTRACT.md`. This is the only Codex brief ever issued for this module. | CC | `CODEX_COMMISSION_LONGEVITY_REPORT_CONTRACT.md` |
| v1.1 | 2026-05-17 | KE Sprint 2 gate cleared; LON-1 marked ready to issue. | CC | -- |
| v1.2 | 2026-05-22 | LON-1 delivered locally as a runtime alignment pass. Added contract-facing endpoint aliases, save/alerts/detail support, full narrative markdown fallback, saved-report route loading, and explicit save UX. Backend compile and frontend production build passed. | Codex | 2026-05-22 |
| v1.3 | 2026-06-07 | Runtime fixes: AYA-1 (Krishnamurti ayanamsha), BSON integer-key errors (`8a69611`), Arc Angel upsert conflict (`8591f2b`). Report confirmed working end-to-end in production. LON-2 commission brief written (KP Engine Foundation + chart panel). LON-OP-1/2 cleared. | CC | 2026-06-07 |
| v1.4 | 2026-06-07 | LON-2 delivered by Codex. All 8 acceptance gates PASS. `KPChart` TypedDict, `build_kp_chart()`, `compute_kp_chart()`, `build_longevity_context()` refactor in `kp_engine.py`. New `kp_chart_router.py` + `POST /api/kp/birth-chart` endpoint. KP Chart Panel in `LongevityReportPage.jsx` (4 sub-tables: planet, cusp, ascendant summary, significators). ENGINE_VERSION v27. Pending push + TT live verify (LON-OP-4). | Codex+CC | 2026-06-07 |
