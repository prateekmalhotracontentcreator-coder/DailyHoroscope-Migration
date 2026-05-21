# Individual Reports -- Module Tracker
> Path: `Codex_Deliveries/Individual_Reports/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-22 IST · v2.9

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- Phase 1 fully live · Phase 2 enrichment live · IR-1 through IR-4 integrated · IR-5 12 Areas Enhancement delivered locally and build-verified; Temple review pending |
| **Phase 1 Frontend** | `frontend/src/pages/reports/IndividualReportsPage.jsx` at `/reports` (PremiumRoute) |
| **Phase 2+3 Frontend** | `frontend/src/pages/reports/LoveReportsPage.jsx` at `/love-reports` (PremiumRoute) |
| **Public Hub** | `frontend/src/pages/reports/PremiumReportsLanding.jsx` at `/individual-reports` |
| **Backend prefix (core reports)** | `/api/reports/{report-slug}` |
| **Backend prefix (IR-5 enhancement)** | `/api/reports/enhanced-analysis` |
| **Backend prefix (Kundali)** | `/api/lagna-kundali` |

---

## Active Runtime Surface

### Natal Individual Reports

| Report | Backend Router | Frontend Surface | Status |
|---|---|---|---|
| Karmic Debt | `karmic_debt_router.py` | `IndividualReportsPage.jsx` | **LIVE** |
| Career Blueprint | `career_blueprint_router.py` | `IndividualReportsPage.jsx` | **LIVE** |
| Shadow Self | `shadow_self_router.py` | `IndividualReportsPage.jsx` | **LIVE** |
| Retrograde Survival | `retrograde_survival_router.py` | `IndividualReportsPage.jsx` | **LIVE** |
| Life Cycles | `life_cycles_router.py` | `IndividualReportsPage.jsx` | **LIVE** |
| Wealth Blueprint | `wealth_blueprint_router.py` | `IndividualReportsPage.jsx` | **LIVE** |
| Romance & Creative Destiny | `romance_creative_router.py` | `IndividualReportsPage.jsx` | **LIVE** |
| Vitality & Health Karma | `vitality_health_router.py` | `IndividualReportsPage.jsx` | **LIVE** |
| Partnership Window | `partnership_window_router.py` | `IndividualReportsPage.jsx` | **LIVE** |
| Dharma & Purpose | `dharma_purpose_router.py` | `IndividualReportsPage.jsx` | **LIVE** |
| Gains & Network Karma | `gains_network_router.py` | `IndividualReportsPage.jsx` | **LIVE** |

### Love / Transit Extensions

| Report | Backend Router | Frontend Surface | Status |
|---|---|---|---|
| Lunar Cycle Wellness | `lunar_cycle_router.py` | `LoveReportsPage.jsx` | **LIVE** |
| Encounter Window | `encounter_window_router.py` | `LoveReportsPage.jsx` | **LIVE** |
| Seasonal Love Weather | `love_weather_router.py` | `LoveReportsPage.jsx` | **LIVE** |
| Date-Night Score | `date_night_router.py` | `LoveReportsPage.jsx` | **LIVE** |
| Intimacy & Vitality | `intimacy_vitality_router.py` | `LoveReportsPage.jsx` | **LIVE** |
| Venus Retrograde | `venus_retrograde_router.py` | `LoveReportsPage.jsx` | **LIVE** |
| Soulmate Timing | `soulmate_timing_router.py` | `LoveReportsPage.jsx` | **LIVE** |
| Soul Connection | `soul_connection_router.py` | `LoveReportsPage.jsx` | **LIVE** |
| Digital Dating | `digital_dating_router.py` | `LoveReportsPage.jsx` | **LIVE** |

### IR-5 Enhancement Layer

| Component | File | Status | Notes |
|---|---|---|---|
| Enhancement endpoint | `backend/ir_enhancement_router.py` | delivered_locally | New shared enhancement endpoint for the 12-area suite |
| Vedic analytics helpers | `backend/vedic_calculator.py` | delivered_locally | Adds donut resilience, graha drishti, and 10-year horizon primitives |
| System prompt | `backend/prompts/vedic_12areas_system_prompt.txt` | delivered_locally | Temple-authored 12 Areas prompt content mirrored into runtime |
| Shared visuals | `frontend/src/components/reports/DonutChart.jsx`, `frontend/src/components/reports/TenYearTimeline.jsx` | delivered_locally | Reused across `/reports` and `/love-reports` |
| Natal page integration | `frontend/src/pages/reports/IndividualReportsPage.jsx` | delivered_locally | Enhancement panel added for the 11 natal reports |
| Love page integration | `frontend/src/pages/reports/LoveReportsPage.jsx` | delivered_locally | Enhancement panel added for Lunar Cycle Wellness only |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| IR-Contract-v1 | Original contract (30 Mar 2026) | SUPERSEDED | `_archive/CONTRACT_APPOINTMENT_v2026-03-30.md` |
| IR-Contract-v2 | Contract update (2 Apr 2026) | SUPERSEDED | `_archive/CONTRACT_UPDATE_v2026-04-02.md` |
| **IR-1** | 5 Public SEO Landing Pages + `/individual-reports` hub | ✅ INTEGRATED -- commit `825a294` | `CODEX_COMMISSION_IR_1_LANDING_PAGES.md` |
| **IR-2** | Lunar Cycle Wellness backend | ✅ INTEGRATED -- commit `f9f6690` | `CODEX_COMMISSION_IR_2_LUNAR_CYCLE.md` |
| **IR-2A** | Lunar Cycle rework | ✅ INTEGRATED -- commit `692fefa` | `CODEX_COMMISSION_IR_2A_LUNAR_CYCLE_REWORK.md` |
| **IR-3** | 8 Love public landing pages | ✅ INTEGRATED -- commit `739c3fa` | `CODEX_COMMISSION_IR_3_LOVE_LANDING_PAGES.md` |
| **IR-4** | 6 new natal reports | ✅ INTEGRATED -- commit `1be1e58` | `CODEX_COMMISSION_IR_4_SIX_NEW_REPORTS.md` |
| **IR-5** | 12 Areas enhancement layer | 🟡 DELIVERED LOCALLY -- Temple review pending | `CODEX_COMMISSION_IR_5_12AREAS_ENHANCEMENT.md` |

---

## IR-5 Runtime Alignment Notes

- The brief describes 12 separate report pages, but the runtime product already consolidates these into two shared premium workspaces:
  - `frontend/src/pages/reports/IndividualReportsPage.jsx` for the 11 natal reports
  - `frontend/src/pages/reports/LoveReportsPage.jsx` for Lunar Cycle Wellness
- The brief's explicit enhancement request body was implemented as a runtime-aligned derived payload:
  - frontend sends `report_type` plus `input_payload` or `birth_data`
  - backend derives the house focus, dasha context, resilience score, drishti map, and 10-year horizon
- Existing report routers were left untouched. IR-5 adds a shared endpoint rather than changing 12 existing endpoints.

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| IR-OP-10 | Minor display formatting polish on Lunar Cycle report | CC | 🟡 MED | Older TT note remains open as a follow-up candidate |
| IR-OP-12 | Temple live verification of IR-4 six Phase 3 natal reports | TT | 🟠 HIGH | Integrated `1be1e58`; runtime spot-check still useful |
| IR-OP-13 | Temple review of IR-5 enhancement endpoint and frontend panels | TT | 🟠 HIGH | Confirm enhancement payload quality on `/reports` and Lunar Cycle at `/love-reports` |

---

## Verification

- Backend verification: `python3 -m py_compile` passed for `backend/vedic_calculator.py`, `backend/ir_enhancement_router.py`, and `backend/server.py`
- Frontend verification: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` passed in `frontend/`
- Runtime gap: no live Render/Vercel walkthrough has been recorded for IR-5 yet

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v2.7 | 2026-05-18 | IR-4 delivered locally. Added 6 backend routers, 6 prompt services, `server.py` registration, `/reports` expansion, 6 public landing pages, routes, sitemap entries, backend `py_compile`, and successful frontend production build. | Codex | 2026-05-18 |
| v2.8 | 2026-05-18 | IR-4 integrated. `Promise.all` → `Promise.allSettled` in `IndividualReportsPage.jsx`; questionnaire save hardened. | CC | `1be1e58` |
| v2.9 | 2026-05-22 | IR-5 delivered locally. Added `ir_enhancement_router.py`, 12 Areas prompt file, new analytics helpers in `vedic_calculator.py`, donut/timeline UI components, and enhancement panels on `/reports` plus Lunar Cycle on `/love-reports`. Backend compile and frontend production build passed. | Codex | 2026-05-22 |
