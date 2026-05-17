# Individual Reports -- Module Tracker
> Path: `Codex_Deliveries/Individual_Reports/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-18 · v2.7

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- Phase 1 fully live · Phase 2 backends integrated with IR-2 and IR-2A · Phase 3 Love frontend hub live · IR-3 Love landing pages delivered locally · IR-4 six-report natal suite delivered locally and build-verified · Temple review pending on the newest IR slices |
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
| Encounter Window | `encounter_window_router.py` ✅ | `LoveReportsPage.jsx` ✅ | `EncounterWindowLandingPage.jsx` ✅ (IR-3) | SEO landing page delivered locally; Temple review pending |
| Seasonal Love Weather | `love_weather_router.py` ✅ | `LoveReportsPage.jsx` ✅ | `LoveWeatherLandingPage.jsx` ✅ (IR-3) | SEO landing page delivered locally; Temple review pending |
| **Lunar Cycle Wellness** | `lunar_cycle_router.py` ✅ | `LoveReportsPage.jsx` ✅ | `LunarCycleWellnessLandingPage.jsx` ✅ (IR-3) | Backend integrated; Love SEO landing page delivered locally |
| Date-Night Score | `date_night_router.py` ✅ | `LoveReportsPage.jsx` ✅ | `DateNightLandingPage.jsx` ✅ (IR-3) | SEO landing page delivered locally; Temple review pending |
| Intimacy & Vitality | `intimacy_vitality_router.py` ✅ | `LoveReportsPage.jsx` ✅ | `IntimacyVitalityLandingPage.jsx` ✅ (IR-3) | SEO landing page delivered locally; Temple review pending |
| Venus Retrograde (bonus) | `venus_retrograde_router.py` ✅ | `LoveReportsPage.jsx` ✅ | `VenusRetrogradeLandingPage.jsx` ✅ (IR-3) | SEO landing page delivered locally; Temple review pending |

### Phase 3 -- Extended Reports (Contract Item 9+)

| Report | Backend Router | Frontend (generation) | Public SEO Page | Status |
|---|---|---|---|---|
| Soulmate Timing | `soulmate_timing_router.py` ✅ | `LoveReportsPage.jsx` ✅ | `SoulmateLandingPage.jsx` ✅ (IR-3) | SEO landing page delivered locally; Temple review pending |
| Soul Connection | `soul_connection_router.py` ✅ | `LoveReportsPage.jsx` ✅ | `SoulConnectionLandingPage.jsx` ✅ (IR-3) | SEO landing page delivered locally; Temple review pending |
| Digital Dating | `digital_dating_router.py` ✅ | `LoveReportsPage.jsx` ✅ | ❌ | No IR-3 landing page in brief; premium tool only for now |

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
| **IR-2A** | Lunar Cycle Rework -- Action Tracker + Rich Content | ✅ INTEGRATED -- commit `692fefa` | `CODEX_COMMISSION_IR_2A_LUNAR_CYCLE_REWORK.md` · CC fixes applied: transit_house subscript bug + f-string fix. Build green. Pushed. |
| **IR-3** | 8 Love Report public SEO landing pages | ✅ INTEGRATED -- commit `739c3fa` | `CODEX_COMMISSION_IR_3_LOVE_LANDING_PAGES.md` · 8 wrappers, 8 routes, 8 sitemap URLs, content-driven CTA (love→/love-reports, phase1→/reports). Build green. |
| **IR-4** | 6 New Phase 3 Natal Reports (Wealth · Romance · Vitality · Partnership · Dharma · Gains) | ✅ INTEGRATED -- commit `1be1e58` | `CODEX_COMMISSION_IR_4_SIX_NEW_REPORTS.md` · Integrated 2026-05-18. 12 backend files, 6 landing wrappers, `server.py` registration, `/reports` expansion (5→11 reports), routes, sitemap, build green. Temple live verification pending (IR-OP-12). |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| ~~IR-OP-1~~ | ~~Temple review of IR-1 frontend slice~~ | TT | ✅ DONE | Reviewed and approved 2026-05-15. Build green. Integrated at commit `825a294`. |
| ~~IR-OP-2~~ | ~~Decide whether `/individual-reports` public hub behavior is accepted as canonical~~ | TT | ✅ DONE | Confirmed canonical 2026-05-15. |
| ~~IR-OP-3~~ | ~~Resolve unrelated global frontend build blocker in `StrategistPage.jsx`~~ | CC | ✅ DONE | Fixed at commit `667fc34` 2026-05-15. |
| ~~IR-OP-4~~ | ~~Temple review and validate IR-2 (Lunar Cycle backend)~~ | TT | ✅ DONE | Live verified 2026-05-16. Datetime bug fixed `021a799`. Tile visible on LovePage. |
| IR-OP-5 | TT live verification of IR-3 (8 Love landing pages) | TT | 🟠 HIGH | Integrated `739c3fa`. Spot-check 2-3 public routes, confirm CTA routes to `/love-reports`, check mobile layout. |
| IR-OP-6 | Issue KUN-1 to Codex (Kundali frontend only) | TT | 🟡 MED | Brief updated 2026-05-16 -- backend already live, frontend only. |
| ~~IR-OP-7~~ | ~~TT live verification of Love Reports at `/love-reports`~~ | TT | ✅ DONE | Verified 2026-05-16 -- 5 Phase 1 reports visible. Lunar Cycle tile confirmed in Love hub. |
| ~~IR-OP-8~~ | ~~Temple review and validate IR-2A~~ | CC | ✅ DONE | Integrated `692fefa` 2026-05-16. Two runtime bugs fixed before commit. TT to verify live report content quality. |
| ~~IR-OP-9~~ | ~~TT live verification of Lunar Cycle richer output~~ | TT | ✅ DONE | Verified live 2026-05-16. Report confirmed brilliant. Minor display formatting improvements noted -- logged as IR-OP-10. |
| IR-OP-10 | Minor display formatting polish on Lunar Cycle report | CC | 🟡 MED | TT flagged minor formatting improvements post live review. Scope to be defined; candidate for inclusion in a future IR patch or IR-3 delivery scope. |
| ~~IR-OP-11~~ | ~~Issue IR-3 to Codex (8 Love Report SEO landing pages)~~ | TT | ✅ DONE | Delivered locally by Codex 2026-05-16. Awaiting Temple review under IR-OP-5. |
| IR-OP-12 | Temple live verification of IR-4 six Phase 3 natal reports | TT | 🟠 HIGH | Integrated `1be1e58` 2026-05-18. Spot-check `/reports` -- confirm all 11 report tiles visible. Generate one new Phase 3 report (e.g. Wealth Blueprint) end-to-end. Verify six new SEO landing pages load at their public routes. |

---

## Architecture Notes

- **Phase 1** reports live at `/reports` (PremiumRoute, `IndividualReportsPage.jsx`) -- natal only, no birth partner needed
- **Phase 2+3** reports live at `/love-reports` (PremiumRoute, `LoveReportsPage.jsx`) -- transit-based, one birth chart input
- **Public hubs**: `/individual-reports` (Phase 1 hub), no Phase 2 public hub yet
- **Public landing pages**: Phase 1 set integrated; IR-3 adds 8 Love landing pages locally on public routes, all CTA-linked to `/love-reports`
- **Kundali backend**: `/api/lagna-kundali` (NOT `/api/kundali` -- old brief had wrong prefix)
- **Lunar Cycle**: IR-2 now adds the final missing Phase 2 backend plus the LoveReportsPage config entry; public SEO page still belongs to IR-3
- **IR-4 natal suite**: extends the original `/reports` premium surface from 5 to 11 report types while preserving the live single-collection `individual_reports` storage helper and existing report-envelope pattern
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
| v2.3 | 2026-05-16 | IR-2A delivered by Codex + integrated by CC. Two runtime bugs fixed: transit_house subscript crash + fallback f-string. Frontend LunarCycleRenderer with 7-Day Action Tracker and today-highlight committed. | CC | `692fefa` |
| v2.4 | 2026-05-16 | IR-2A live-verified by TT -- report confirmed brilliant. Minor formatting note logged IR-OP-10. IR-OP-9 closed. IR-3 confirmed ready to issue (IR-OP-11). | TT + CC | `0a4d16f` |
| v2.5 | 2026-05-16 | IR-3 delivered by Codex + integrated by CC. 8 landing pages, 8 routes, 8 sitemap URLs. CTA content-driven shell tweak (Phase 1 unaffected). Build green. | CC | `739c3fa` |
| v2.5 | 2026-05-16 | IR-3 delivered locally. Added 8 Love landing pages via shared shell, public routes, sitemap URLs, `/love-reports` CTA wiring, and successful frontend production build. | Codex | 2026-05-16 |
| v2.6 | 2026-05-18 | IR-4 commission brief written. 6 Phase 3 natal reports (Wealth/H2, Romance/H5, Vitality/H6, Partnership/H7, Dharma/H9, Gains/H11). 516-line brief, 18 new files, 4 modified. READY TO ISSUE. IR-OP-12 opened. | CC | 2026-05-18 |
| v2.7 | 2026-05-18 | IR-4 delivered locally. Added 6 backend routers, 6 prompt services, `server.py` registration, `/reports` expansion for all 6 report types, 6 public landing pages, routes, sitemap entries, backend `py_compile`, and successful frontend production build. | Codex | 2026-05-18 |
| v2.8 | 2026-05-18 | IR-4 integrated. `Promise.all` → `Promise.allSettled` in `IndividualReportsPage.jsx` loadHistory (root cause of Karmic Debt "no Render logs" bug). Questionnaire save hardened: secondary enrichment steps (`sync_arc_angel`, `_upsert_questionnaire_profile`) wrapped in best-effort try/except so a secondary crash cannot return 500 and block the save. All pushed commit `1be1e58`. | CC | `1be1e58` |
