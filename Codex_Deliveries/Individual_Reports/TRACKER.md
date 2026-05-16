# Individual Reports -- Module Tracker
> Path: `Codex_Deliveries/Individual_Reports/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-16 · v2.1

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- Phase 1 fully live · Phase 2 backends now complete in local runtime · Phase 3 backends fully live · Love frontend hub live · Public SEO gap for Phase 2+3 reports · IR-2 delivered locally 2026-05-16 · IR-3 still ready to issue |
| **Phase 1 Frontend** | `frontend/src/pages/reports/IndividualReportsPage.jsx` at `/reports` (PremiumRoute) |
| **Phase 2+3 Frontend** | `frontend/src/pages/reports/LoveReportsPage.jsx` at `/love-reports` (PremiumRoute) |
| **Public Hub** | `frontend/src/pages/reports/PremiumReportsLanding.jsx` at `/individual-reports` |
| **Backend prefix (Phase 1)** | `/api/reports/{report-slug}` |
| **Backend prefix (Phase 2+3)** | `/api/reports/{report-slug}` |
| **Backend prefix (Kundali)** | `/api/lagna-kundali` |

---

## Full Reconciliation (2026-05-16)

### Phase 1 -- Natal Reports (Contract Items 9-A to 9-E)

| Report | Backend Router | Frontend (generation) | Public SEO Page | Status |
|---|---|---|---|---|
| Karmic Debt | `karmic_debt_router.py` ✅ | `IndividualReportsPage.jsx` ✅ | `KarmicDebtLandingPage.jsx` ✅ (IR-1) | **FULLY LIVE** |
| Career Blueprint | `career_blueprint_router.py` ✅ | `IndividualReportsPage.jsx` ✅ | `CareerBlueprintLandingPage.jsx` ✅ (IR-1) | **FULLY LIVE** |
| Shadow Self | `shadow_self_router.py` ✅ | `IndividualReportsPage.jsx` ✅ | `ShadowSelfLandingPage.jsx` ✅ (IR-1) | **FULLY LIVE** |
| Retrograde Survival | `retrograde_survival_router.py` ✅ | `IndividualReportsPage.jsx` ✅ | `RetrogradeSurvivalLandingPage.jsx` ✅ (IR-1) | **FULLY LIVE** |
| Life Cycles | `life_cycles_router.py` ✅ | `IndividualReportsPage.jsx` ✅ | `LifeCyclesLandingPage.jsx` ✅ (IR-1) | **FULLY LIVE** |

### Phase 2 -- Transit / Love Reports (Contract Items 8)

| Report | Backend Router | Frontend (generation) | Public SEO Page | Status |
|---|---|---|---|---|
| Encounter Window | `encounter_window_router.py` ✅ | `LoveReportsPage.jsx` ✅ | ❌ (IR-3 pending) | Backend + frontend live; SEO page missing |
| Seasonal Love Weather | `love_weather_router.py` ✅ | `LoveReportsPage.jsx` ✅ | ❌ (IR-3 pending) | Backend + frontend live; SEO page missing |
| **Lunar Cycle Wellness** | `lunar_cycle_router.py` ✅ | `LoveReportsPage.jsx` ✅ | ❌ (IR-3 pending) | Backend delivered locally via IR-2; Temple review/integration pending |
| Date-Night Score | `date_night_router.py` ✅ | `LoveReportsPage.jsx` ✅ | ❌ (IR-3 pending) | Backend + frontend live; SEO page missing |
| Intimacy & Vitality | `intimacy_vitality_router.py` ✅ | `LoveReportsPage.jsx` ✅ | ❌ (IR-3 pending) | Backend + frontend live; SEO page missing |
| Venus Retrograde (bonus) | `venus_retrograde_router.py` ✅ | `LoveReportsPage.jsx` ✅ | ❌ (IR-3 pending) | Backend + frontend live; SEO page missing |

### Phase 3 -- Extended Reports (Contract Item 9+)

| Report | Backend Router | Frontend (generation) | Public SEO Page | Status |
|---|---|---|---|---|
| Soulmate Timing | `soulmate_timing_router.py` ✅ | `LoveReportsPage.jsx` ✅ | ❌ (IR-3 pending) | Backend + frontend live; SEO page missing |
| Soul Connection | `soul_connection_router.py` ✅ | `LoveReportsPage.jsx` ✅ | ❌ (IR-3 pending) | Backend + frontend live; SEO page missing |
| Digital Dating | `digital_dating_router.py` ✅ | `LoveReportsPage.jsx` ✅ | ❌ (IR-3 pending) | Backend + frontend live; SEO page missing |

### Contract 8A -- Lagna Kundali

| Component | Status | Notes |
|---|---|---|
| Backend router | ✅ LIVE | `kundali_router.py` at `/api/lagna-kundali` -- all endpoints live |
| Frontend module | ❌ NOT BUILT | KUN-1 re-scoped to frontend-only 2026-05-16 |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| IR-Contract-v1 | Original contract (30 Mar 2026) | SUPERSEDED | `_archive/CONTRACT_APPOINTMENT_v2026-03-30.md` |
| IR-Contract-v2 | Contract update (2 Apr 2026) | SUPERSEDED | `_archive/CONTRACT_UPDATE_v2026-04-02.md` |
| IR-Frontend-v1 | Frontend commission (2 Apr 2026) | SUPERSEDED by IR-1 | `_archive/INDIVIDUAL_REPORTS_FRONTEND_v2026-04-02.md` |
| **IR-1** | 5 Public SEO Landing Pages + `/individual-reports` hub | ✅ INTEGRATED -- commit `825a294` | `CODEX_COMMISSION_IR_1_LANDING_PAGES.md` · Delivered + integrated 2026-05-15 |
| **IR-2** | Lunar Cycle Wellness backend (`lunar_cycle_router.py`) | ✅ INTEGRATED -- commit `f9f6690` | `CODEX_COMMISSION_IR_2_LUNAR_CYCLE.md` · Integrated. Datetime bug fixed `021a799`. |
| **IR-2A** | Lunar Cycle Rework -- Action Tracker + Rich Content | 🟣 READY TO ISSUE | `CODEX_COMMISSION_IR_2A_LUNAR_CYCLE_REWORK.md` · Amends router + prompt service + frontend display. 7-day Action Tracker, richer Claude output. |
| **IR-3** | 8 Love Report public SEO landing pages | 🟣 READY TO ISSUE | `CODEX_COMMISSION_IR_3_LOVE_LANDING_PAGES.md` · Frontend-only. Lunar Cycle copy should reflect IR-2A richer output. |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| ~~IR-OP-1~~ | ~~Temple review of IR-1 frontend slice~~ | TT | ✅ DONE | Reviewed and approved 2026-05-15. Build green. Integrated at commit `825a294`. |
| ~~IR-OP-2~~ | ~~Decide whether `/individual-reports` public hub behavior is accepted as canonical~~ | TT | ✅ DONE | Confirmed canonical 2026-05-15. |
| ~~IR-OP-3~~ | ~~Resolve unrelated global frontend build blocker in `StrategistPage.jsx`~~ | CC | ✅ DONE | Fixed at commit `667fc34` 2026-05-15. |
| ~~IR-OP-4~~ | ~~Temple review and validate IR-2 (Lunar Cycle backend)~~ | TT | ✅ DONE | Live verified 2026-05-16. Datetime bug fixed `021a799`. Tile visible on LovePage. |
| IR-OP-5 | Issue IR-3 to Codex (8 Love landing pages) | TT | 🟠 HIGH | Brief complete. No backend dependency -- can issue independently. |
| IR-OP-6 | Issue KUN-1 to Codex (Kundali frontend only) | TT | 🟡 MED | Brief updated 2026-05-16 -- backend already live, frontend only. |
| ~~IR-OP-7~~ | ~~TT live verification of Love Reports at `/love-reports`~~ | TT | ✅ DONE | Verified 2026-05-16 -- 5 Phase 1 reports visible. Lunar Cycle tile confirmed in Love hub. |
| IR-OP-8 | Issue IR-2A to Codex (Lunar Cycle rework + Action Tracker) | TT | 🟠 HIGH | Brief ready 2026-05-16. Amends router + prompt service + LoveReportsPage display. |

---

## Architecture Notes

- **Phase 1** reports live at `/reports` (PremiumRoute, `IndividualReportsPage.jsx`) -- natal only, no birth partner needed
- **Phase 2+3** reports live at `/love-reports` (PremiumRoute, `LoveReportsPage.jsx`) -- transit-based, one birth chart input
- **Public hubs**: `/individual-reports` (Phase 1 hub), no Phase 2 public hub yet
- **Public landing pages**: `/karmic-debt-report` etc (Phase 1 ✅), Phase 2+3 missing (IR-3 scope)
- **Kundali backend**: `/api/lagna-kundali` (NOT `/api/kundali` -- old brief had wrong prefix)
- **Lunar Cycle**: IR-2 now adds the final missing Phase 2 backend plus the LoveReportsPage config entry; public SEO page still belongs to IR-3
- `vedic_shared_utils.py` is the shared utility layer for all report routers -- do not duplicate its functions

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-05-15 | Tracker created. IR-1 brief finalised. Module state documented. | CC | This session |
| v1.1 | 2026-05-15 | IR-1 landing pages built locally, public routes added, sitemap updated. | Codex | This session |
| v1.2 | 2026-05-15 | IR-1 issued to Codex IR thread. IR-OP-3 (Strategist build blocker) closed. | TT + CC | `667fc34` |
| v1.3 | 2026-05-15 | IR-1 delivered + integrated. Route canonical confirmed. | CC + TT | `825a294` |
| v2.0 | 2026-05-16 | **Full reconciliation.** All backends audited against server.py. Phase 1 fully live. Phase 2+3 backends mostly live (lunar_cycle missing). LoveReportsPage confirmed as Phase 2+3 frontend hub. Kundali backend confirmed fully live at `/api/lagna-kundali`. IR-2 (lunar cycle backend) + IR-3 (8 love landing pages) briefs written and ready to issue. KUN-1 re-scoped to frontend-only. | CC | 2026-05-16 |
| v2.1 | 2026-05-16 | IR-2 delivered locally. Added `lunar_cycle_router.py`, `lunar_cycle_prompt_service.py`, `server.py` registration, and the `LoveReportsPage.jsx` card entry. Temple review still pending. | Codex | 2026-05-16 |
| v2.2 | 2026-05-16 | IR-2 integrated + bugs fixed (`021a799`): datetime serialisation crash + LovePage hub tile. IR-2A brief written (Action Tracker + rich content rework). 12 Areas of Life map published. Architecture doc published. IR-3 cross-referenced with IR-2A. | CC | `ced0972` |
