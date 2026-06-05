# Codex QA Integration Audit -- Central Tracker
> EverydayHoroscope · Temple Team
> Issued: 2026-05-27
> Purpose: Every active Codex thread audits all work they have delivered and reports integration status here.
> Live App: https://www.everydayhoroscope.in
> Backend API: https://everydayhoroscope-api.onrender.com
> Repo: `/Users/apple/DailyHoroscope-Migration/`

---

## Column Guide

| Column | What to Enter |
|---|---|
| **Commission ID** | Use the ID from your commission brief (e.g. KE-Sprint2). If your work has no listed ID, write `UNLISTED-[your-thread-initials]-[sequence]` and add a row. |
| **Feature / Description** | One-line description of what was built |
| **Key Files Delivered** | Comma-separated list of backend + frontend files (use short paths from repo root) |
| **Files Present in Repo** | `Yes` / `No` / `Partial` -- check `/Users/apple/DailyHoroscope-Migration/` |
| **Integrated to Live App** | `Yes` / `No` / `Partial` -- has this been deployed to https://www.everydayhoroscope.in? |
| **Live URL** | The URL to test (e.g. `/tarot`, `/api/tarot/draw`) -- write `N/A` for internal-only |
| **URL Working** | `Yes` / `No` / `Error: [paste error]` / `N/A` |
| **Gap Description** | What specifically is missing, broken, or incomplete. Write `None` if fully working. |
| **Priority** | `🔴 Critical` / `🟠 High` / `🔶 Medium` / `🔵 Low` |
| **Thread Notes** | Any additional context, caveats, or recommendations |

**Status values for Integrated to Live App:**
| Value | Meaning |
|---|---|
| `Yes` | Committed to main, deployed, URL returns correct response |
| `Partial` | Some parts live, others missing or broken |
| `No` | Code delivered but never merged / integrated / deployed |
| `N/A` | Internal tool, seed script, or DB-only change -- no public URL expected |

---

## SECTION 1 -- Knowledge Engine Thread

> Review all KE commissions AND any additional work done that is not listed. Add rows as needed.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| KE-Sprint2 | Arbitration Runtime -- `_contradiction_score`, `_representation_mode`, `_build_tension_block`, supersession lookup | `backend/knowledge_engine.py`, `backend/server.py` | Yes | Partial | `/api/knowledge/generate-narrative` | Yes -- `GET` returns `405 Method Not Allowed`; empty `POST` returns `422` validation, confirming the live route exists | Original tracker URL `/api/knowledge-engine/scan` is stale; production KE scan/arbitration is exposed through `/api/knowledge/generate-narrative` and downstream consumers, not a standalone public scan endpoint. | 🔶 Medium | Core Sprint 2 helpers are present in repo and live runtime paths. |
| KE-2A | Yoga Check Evaluation Engine -- 16 evaluator types, 26 dispatch entries, 52 tests | `backend/ke_yoga_evaluator.py`, `backend/knowledge_engine.py` | Yes | Yes | `N/A` | N/A | No standalone public evaluator endpoint exists in production; verification is indirect through KE consumers rather than a dedicated `/evaluate-yoga` route. | 🔵 Low | The tracker-listed `/api/knowledge-engine/evaluate-yoga` route does not exist live and should be treated as stale contract text unless Temple wants it exposed. |
| KE-IQ | Questionnaire UI + β/γ KE wiring, 75 tests green | `backend/knowledge_router.py`, `backend/server.py`, `frontend/src/pages/account/QuestionnairePage.jsx`, `frontend/src/components/QuestionnaireWidget.jsx`, `frontend/src/components/ArcAngelPanel.jsx` | Yes | Partial | `/questionnaire`, `/api/knowledge-engine/questionnaire/profile`, `/api/knowledge-engine/questionnaire/submit` | Partial -- `/questionnaire` returns `200`; profile returns `401 Authentication required`; empty submit `POST` returns `422` validation | Authenticated questionnaire submit/profile flow and `user_questionnaire_profiles` persistence were not fully smoke-tested in this audit. | 🔶 Medium | Row path corrected from stale `frontend/src/pages/QuestionnairePage.jsx` to `frontend/src/pages/account/QuestionnairePage.jsx`. |
| KE-Ingest | Batch Book Ingest Automation v2 | `backend/scripts/batch_ingest.py`, `backend/scripts/ingest_*.py` | Yes | N/A | `N/A` | N/A | None | 🔵 Low | Script inventory is present in repo; this audit did not re-verify live Mongo ingest contents batch-by-batch. |
| KE-Val | Automated Rule Validation Engine | `backend/knowledge_validator.py`, `backend/knowledge_router.py` | Yes | Partial | `/api/knowledge/index/status`, `/api/knowledge/validate-batch` | Partial -- index status returns `401 Admin authentication required`; validate-batch was not executed without admin session | Admin-authenticated end-to-end validation run was not repeated in this unauthenticated audit. | 🔵 Low | Validation pipeline code is present and live admin routes are mounted. |
| KE-2B2 | Varga Dignity Wiring -- facts layer | `backend/knowledge_engine.py` | Yes | Yes | `N/A` | N/A | None | 🔵 Low | Internal facts-layer feature with no standalone public URL; runtime is present in the live KE stack. |
| KE-2D | Varga Dignity Tier Evaluator, 37 tests green | `backend/ke_yoga_evaluator.py`, `backend/scripts/_archive/migrate_ch41_varga_checkable.py` | Yes | Yes | `N/A` | N/A | None | 🔵 Low | Internal evaluator layer only; migration script is archived in repo and no public route is expected. |
| KE-Item5 | Library Console | `frontend/src/pages/admin/LibraryConsolePage.jsx`, `backend/knowledge_router.py`, `backend/server.py` | Yes | Partial | `/admin/library`, `/api/knowledge/rules` | Partial -- `/admin/library` returns `200`; `/api/knowledge/rules` returns `401 Admin authentication required` | Admin-authenticated rule browse / approve / reject workflow was not fully smoke-tested in this audit. | 🔶 Medium | Live URL corrected from stale `/knowledge-engine/library` to actual `/admin/library`. |
| KE-Item6 | Brihat Kundali × KE Route | `frontend/src/pages/kundali/BrihatKundliPage.jsx`, `backend/server.py`, `backend/knowledge_engine.py` | Yes | Partial | `/brihat-kundli`, `/api/brihat-kundli/generate` | Yes -- `/brihat-kundli` returns `200`; empty `POST` to generate returns `422` validation | Full premium/authenticated Brihat generation and PDF download path were not re-smoked in this audit. | 🔵 Low | Repo wiring shows the page calling `/api/brihat-kundli/generate` and the backend route is mounted live. |
| KE-Item7 | Simplified Tranche Filter | `backend/tranche_filter.py`, `backend/knowledge_engine.py` | Yes | Yes | `N/A` | N/A | None | 🔵 Low | Runtime-only filter layer; no public URL expected. |
| KE-Item8 | Tranche Filter UI Feedback | `frontend/src/pages/kundali/BrihatKundliPage.jsx`, `frontend/src/pages/admin/LibraryConsolePage.jsx` | Yes | Partial | `/brihat-kundli`, `/admin/library` | Yes -- both frontend routes return `200` | Authenticated/premium and admin UX states for the tranche-adjusted messaging were not fully smoke-tested in this audit. | 🔵 Low | UI feedback surfaces are present in repo and deployed shells are live. |
| KE-Sprint3 | Arc Angel computation runtime, profile persistence, and AD-window output | `backend/knowledge_engine.py`, `backend/knowledge_schema.py`, `backend/vedic_calculator.py`, `backend/server.py` | Yes | Yes | `/arc-angel`, `/api/knowledge-engine/arc-angel-windows`, `/api/knowledge-engine/arc-angel-profile/[user_id]` | Partial -- `/arc-angel` returns `200`; windows route returns `200`; fake profile id returns expected `404 Arc Angel profile not found` | Authenticated saved-profile retrieval and questionnaire-enriched Arc Angel persistence were not fully smoke-tested in this audit. | 🔶 Medium | Unauthenticated live probe returned the expected Arc Angel payload with `overall_confidence_pct: 40`, `questionnaire_completed: false`, and `cached: false`. |
| _(add rows)_ | | | | | | | | | |

**KE Thread -- Audit Summary**
- Overall Status: PARTIAL -- core KE runtime is present in repo and major live surfaces are deployed, but some tracker-listed URLs were stale/non-public and multiple authenticated/admin flows were not fully smoke-tested in this audit.
- Total Rows Audited: 12
- Gaps Found: 6
- Signed off by KE Thread: 2026-05-27

---

## SECTION 2 -- KP Oracle Thread

> Review all KP commissions AND any additional work done that is not listed. Add rows as needed.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| KP-2A | KP Bundle Editorial + Share Card + Remedies Admin Frontend | `backend/scriptural_oracle_router.py`, `frontend/src/pages/kp/` | | | `/kp-oracle` | | | | |
| KP-Sprint2 | Ask Question -- Guna Logic Router, 60-route JSON, 3-card reveal | `backend/ask_question_logic_router.json`, `frontend/src/pages/AskQuestionPage.jsx` | | | `/kp-oracle/ask` | | | | |
| KP-2B | Ritual Animation + 3-Pillar UX + Astro-Filter | `frontend/src/pages/kp/KrishnaRitualScreen.jsx`, `KrishnaOraclePage.jsx` | | | `/kp-oracle` (3-pillar view) | | | | |
| _(add rows)_ | | | | | | | | | |

**KP Thread -- Audit Summary**
- Overall Status: _(fill in)_
- Total Rows Audited: ___
- Gaps Found: ___
- Signed off by KP Thread: _(date)_

---

## SECTION 3 -- Arc Angel Thread

> Review all Arc Angel commissions AND any additional work done that is not listed. Add rows as needed.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| ARC-UI | Arc Angel UI Panel | `frontend/src/components/ArcAngelPanel.jsx` | | | `/arc-angel` | | | | |
| ARC-2 | 3-Pillar Confidence Engine (40%+24%+12%+10%, cap 86%) | `backend/` arc angel router / server.py wiring | | | `/api/arc-angel/windows` | | | | |
| ARC-2 | Questionnaire Gating + PrivateRoute for signed-up users | `frontend/src/pages/QuestionnairePage.jsx`, PrivateRoute wiring in `App.js` | | | `/questionnaire` | | | | |
| ARC-2 | Desktop Sidebar -- left nav split | `frontend/src/components/ArcAngelPanel.jsx` (desktop layout) | | | `/arc-angel` (desktop) | | | | |
| _(add rows)_ | | | | | | | | | |

**Arc Angel Thread -- Audit Summary**
- Overall Status: _(fill in)_
- Total Rows Audited: ___
- Gaps Found: ___
- Signed off by ARC Thread: _(date)_

---

## SECTION 4 -- Individual Reports Thread

> Review all IR commissions AND any additional work done that is not listed. IR-5 is in progress -- mark as N/A for now.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| IR-BASE-1 | Phase 1 natal report backend suite -- 5 deterministic report routers | `backend/karmic_debt_router.py`, `backend/career_blueprint_router.py`, `backend/shadow_self_router.py`, `backend/retrograde_survival_router.py`, `backend/life_cycles_router.py`, `backend/server.py` | Yes | Yes | `/api/reports/karmic-debt/generate` sample | Yes -- live route returns expected `422` validation on empty payload | Full authenticated generation not re-smoked in this audit; prior Temple production acceptance recorded. | 🔵 Low | Added because original Phase 1 backend delivery was not pre-listed. |
| IR-AI-1 | Claude enrichment services for Phase 1 natal reports | `backend/karmic_debt_prompt_service.py`, `backend/career_blueprint_prompt_service.py`, `backend/shadow_self_prompt_service.py`, `backend/retrograde_survival_prompt_service.py`, `backend/life_cycles_prompt_service.py` | Yes | Yes | N/A | N/A | No direct URL; runs inside generate flow. | 🔵 Low | Prompt services are present and imported by report routers. |
| IR-FE-1 | Individual Reports premium page + report renderers + history support | `frontend/src/pages/reports/IndividualReportsPage.jsx`, `frontend/src/pages/reports/MyReportsPage.jsx`, `frontend/src/App.js` | Yes | Yes | `/reports`, `/my-reports` | Yes -- both URLs return `200` | Premium generate/history user journey not fully re-smoked with entitled account during this audit. | 🔵 Low | `/reports` is PremiumRoute-wrapped in production. |
| IR-1 | 5 Public SEO Landing Pages + `/individual-reports` hub | `frontend/src/pages/reports/landing/*LandingPage.jsx`, `frontend/src/pages/reports/landing/reportLandingContent.jsx`, `frontend/src/pages/reports/PremiumReportsLanding.jsx`, `frontend/src/App.js`, `frontend/public/sitemap.xml` | Yes | Yes | `/individual-reports`, `/karmic-debt-report` | Yes -- both sample URLs return `200` | None for public route availability. | 🔵 Low | Tracker source path corrected from old `frontend/src/pages/individual-reports/` expectation to live `reports/landing/` implementation. |
| IR-2 | Lunar Cycle Wellness Backend | `backend/lunar_cycle_router.py`, `backend/lunar_cycle_prompt_service.py`, `backend/server.py` | Yes | Yes | `/api/reports/lunar-cycle/generate` | Yes -- live route returns expected `422` validation on empty payload | Full generation not re-smoked in this audit. | 🔵 Low | Live prefix is `/api/reports/lunar-cycle`, not `/api/lunar-cycle`. |
| IR-2A | Lunar Cycle Rework -- Action Tracker + Rich Content | `backend/lunar_cycle_router.py`, `backend/lunar_cycle_prompt_service.py`, `frontend/src/pages/reports/LoveReportsPage.jsx` | Yes | Yes | `/love-reports`, `/lunar-cycle-wellness` | Yes -- both URLs return `200` | Premium Lunar generate/display flow not fully re-smoked with entitled account. | 🔵 Low | Action tracker model and Lunar renderer are present in repo. |
| IR-3 | 8 Love Report SEO Landing Pages | `frontend/src/pages/reports/landing/*LandingPage.jsx`, `frontend/src/pages/reports/landing/reportLandingContent.jsx`, `frontend/src/App.js`, `frontend/public/sitemap.xml` | Yes | Yes | `/love-weather-report` sample | Yes -- sample URL returns `200` | None for public route availability. | 🔵 Low | Tracker source path corrected from old `frontend/src/pages/love/` expectation to live `reports/landing/` implementation. |
| IR-4 | 6 Phase 3 Natal Reports -- `/reports` expanded 5→11 tiles | `backend/wealth_blueprint_router.py`, `backend/romance_creative_router.py`, `backend/vitality_health_router.py`, `backend/partnership_window_router.py`, `backend/dharma_purpose_router.py`, `backend/gains_network_router.py`, matching prompt services, `frontend/src/pages/reports/IndividualReportsPage.jsx`, landing pages, `backend/server.py`, `frontend/src/App.js` | Yes | Yes | `/reports`, `/wealth-blueprint-report`, `/api/reports/wealth-blueprint/generate` | Yes -- page URLs return `200`; API route returns expected `422` validation on empty payload | `/reports` 11-tile premium journey not fully re-smoked with entitled account during this audit. | 🔵 Low | Backend and landing pages are present and registered. |
| IR-5 | 12 Areas of Life Enhancement | `backend/ir_enhancement_router.py`, `backend/vedic_calculator.py`, `backend/prompts/vedic_12areas_system_prompt.txt`, `frontend/src/components/reports/DonutChart.jsx`, `frontend/src/components/reports/TenYearTimeline.jsx`, `frontend/src/pages/reports/IndividualReportsPage.jsx`, `frontend/src/pages/reports/LoveReportsPage.jsx`, `backend/server.py` | Yes | Yes | `/api/reports/enhanced-analysis` | Yes -- live route returns expected `400: report_type is required` on empty payload | Full enhanced-analysis panel flow not re-smoked with saved report data during this audit. | 🔶 Medium | Tracker previously marked IR-5 in progress; repo shows runtime files integrated. |

**IR Thread -- Audit Summary**
- Overall Status: Partial -- code present and deployed; public URLs and representative backend routes are live; authenticated premium report journeys need final entitled-account smoke coverage.
- Total Rows Audited: 9
- Gaps Found: 3
- Signed off by IR Thread: 2026-05-27

---

## SECTION 5 -- Strategist Thread

> Review all Strategist commissions AND any additional work done that is not listed. Add rows as needed.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL Tested | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| STR-1 | Strategist Premium Landing Page | `frontend/src/pages/strategist/TheStrategistLandingPage.jsx` | Yes | Yes | Yes | `/the-strategist` | Yes | None confirmed in route availability. | 🔵 Low | Public landing route is live and returns `200`; landing code is present in the repo at the Strategist path. |
| STR-1 | War Room Visual Rebuild | `frontend/src/pages/strategist/StrategistPage.jsx`, `frontend/src/components/strategist/war-room/StrategistWarRoom.jsx` | Yes | Yes | Yes | `/strategist/war-room` | Yes | None confirmed from unauthenticated route-shell check. | 🔵 Low | Route shell loads in production and the locked War Room component tree is present in repo. Authenticated full-session walkthrough was not repeated in this audit. |
| STR-1 | App.js route wiring + sitemap entries | `frontend/src/App.js`, `frontend/public/sitemap.xml` | Yes | Partial | Yes | `/strategist`, `/the-strategist`, `/sitemap.xml` | Error -- routes return `200`, sitemap is correct, but raw HTML metadata is still generic root metadata/canonical `/` | Live sitemap is correct (`/the-strategist` present, `/strategist` omitted), but raw HTML fetches for both public Strategist routes still return generic root metadata/canonical `/` instead of route-specific Strategist SEO. | 🟠 High | This is a live SEO delivery gap rather than a route outage. |
| STR-2J | Missions UI -- responsive MissionCard + dasha timing panel | `frontend/src/pages/strategist/StrategistMissionsPage.jsx`, `frontend/src/components/MissionCard.jsx` | Yes | Yes | Yes | `/strategist/missions` | Yes | None confirmed in public route-shell availability. | 🔵 Low | Repo contains the responsive grid, `decision_logic`, `pivot_logic`, command-planet highlighting, and dasha timing UI. |
| STR (backend) | Dashboard + Missions API endpoints | `backend/strategist_router.py` | Yes | Yes | Yes | `/api/strategist/dashboard`, `/api/strategist/missions` | Yes | None | 🔵 Low | Live probes returned expected auth behavior: dashboard `401 Authentication required`, missions `401 Authentication required`, confirming the deployed endpoints exist. |
| STR-R01 | War Room selector page -- parallel fetch + prop mapping | `frontend/src/pages/strategist/StrategistWarRoomPage.jsx`, `frontend/src/App.js` | Yes | Yes | Yes | `/strategist/war-room` | Yes | None | 🔵 Low | Selector wrapper is present and routed live; Temple already applied the one-frame derived-props fix before `main` push. |
| STR-R02 | Golden Hour sunset payload + 3-window frontend mapping | `backend/strategist_router.py`, `frontend/src/pages/strategist/StrategistWarRoomPage.jsx` | Yes | Yes | Yes | `/api/strategist/dashboard`, `/strategist/war-room` | Yes | None | 🔵 Low | `sunset_iso` is live in dashboard payload and the frontend computes the three Golden Hour windows from it. |
| STR-R03 | Pitru Rin ledger payload + frontend wiring | `backend/strategist_router.py`, `frontend/src/pages/strategist/StrategistWarRoomPage.jsx` | Yes | Yes | Yes | `/api/strategist/dashboard`, `/strategist/war-room` | Yes | None | 🔵 Low | `pitru_rin_ledger` is now part of the live dashboard payload and replaces the earlier placeholder. |
| STR-R04 | Dasha transition date wiring | `frontend/src/pages/strategist/StrategistWarRoomPage.jsx` | Yes | Yes | Yes | `/strategist/war-room` | Yes | None | 🔵 Low | Transition date is wired from `dashboard.current_mahadasha_end`. |
| STR-2A1 | NavBar + Footer Strategist placement cleanup | `frontend/src/components/NavBar.jsx`, `frontend/src/components/Footer.jsx` | Yes | Yes | Yes | `/`, `/the-strategist` | Yes | None | 🔵 Low | `/strategist` remains top-level in nav, the premium crown was removed there, and the Blog footer duplication was cleaned up. |
| UNLISTED-STR-01 | Action Plan page + backend endpoint | `frontend/src/pages/strategist/StrategistActionPlanPage.jsx`, `backend/strategist_router.py` | Yes | Yes | Yes | `/strategist/action-plan`, `/api/strategist/action-plan` | Yes | None | 🔵 Low | Live public route shell returns `200`; backend endpoint returns expected auth gating in production. |
| UNLISTED-STR-02 | Surrogate Bridge page + surrogate endpoint | `frontend/src/pages/strategist/StrategistSurrogatePage.jsx`, `backend/strategist_router.py` | Yes | Yes | Yes | `/strategist/surrogate`, `/api/strategist/surrogate` | Yes | None | 🔵 Low | Live public route shell returns `200`; surrogate API reaches validation/auth logic in production. |
| UNLISTED-STR-03 | Strategist notification trigger registry + email templates | `backend/notification_trigger_router.py`, `backend/notification_email_service.py` | Yes | Yes | Not Applicable | Not Applicable | Not Applicable | None confirmed in repo audit. | 🔵 Low | Delivery exists in repo and is backend/supporting infrastructure rather than a direct public route. |

**Strategist Thread -- Audit Summary**
- Overall Status: INTEGRATED WITH 1 HIGH-PRIORITY LIVE SEO GAP
- Total Rows Audited: 13
- Gaps Found: 1
- Signed off by STR Thread: 2026-05-27

---

## SECTION 6 -- Tarot Thread

> Review all Tarot commissions AND any additional work done that is not listed. Add rows as needed.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| TAR-v4 | TarotHero + Animated Starfield + Particle Burst | `frontend/src/pages/tarot/TarotPage.jsx`, hero + animation components | Yes | Yes | `/tarot` | Yes | None | 🔵 Low | Current app path is `frontend/src/pages/tarot/TarotPage.jsx`; the older tracker path `frontend/src/pages/TarotPage.jsx` was stale. Live route returns `200`; Temple smoke confirmed hero/starfield/fanned cards/CTA. |
| TAR-v4 | Card Modal + Drawer + Celtic Cross Layout | `frontend/src/pages/tarot/TarotPage.jsx` modal, drawer, Celtic Cross layout | Yes | Yes | `/tarot` (spread view) | Yes | None confirmed | 🔵 Low | Source contains modal/drawer/Celtic Cross layout. Full interactive verification requires authenticated spread draw; Temple source/smoke confirmation received. |
| TAR-v4 | Streak / XP Widget + Month-grouped History | `frontend/src/pages/tarot/TarotPage.jsx`, history timeline components | Yes | Yes | `/tarot` (history tab) | Yes | None confirmed | 🔵 Low | Streak/XP widget and grouped history/timeline logic present. History data remains auth/user dependent as expected. |
| TAR-v4 | Vedic focus-area cards + final 5-tab Tarot shell | `frontend/src/pages/tarot/TarotPage.jsx` | Yes | Yes | `/tarot` | Yes | None | 🔵 Low | Live/smoke confirmed all 5 tabs: Daily Draw, Spreads, Favorable Periods, Journal, History; focus cards include Rahu/Ketu, Venus/Shukra, Saturn/Shani, Moon/Chandra, Mercury/Budha labels. |
| TAR-Contract4 | Full 78-card Tarot deck + asset bundle | `frontend/public/tarot_cards.json`, `backend/tarot_router.py` `DEFAULT_CARDS` | Yes | Yes | `/tarot_cards.json` | Yes | None | 🔵 Low | Static asset returns `200`; repo has full 78-card JSON bundle and router card pool. Asset file intentionally untouched in v4 UI uplift. |
| TAR-Backend-Core | Daily draw, spread generate, history, bookmark, feedback | `backend/tarot_router.py`, `frontend/src/pages/tarot/TarotPage.jsx`, `frontend/src/pages/tarot/TarotHistoryPage.jsx`, `frontend/src/utils/tarotFeedback.js` | Yes | Yes | `/api/tarot/daily/draw`, `/api/tarot/spread/generate`, `/api/tarot/history`, `/api/tarot/bookmark` | Yes | None | 🔵 Low | Correct draw route is `/api/tarot/daily/draw`, not stale `/api/tarot/draw`. User-specific operations are auth-gated by design. Feedback schema is `{report_id, rating, comment}`. |
| CONTRACT_TAR_FIX | Remediation endpoints: spread access, single reading, favorable periods, offers | `backend/tarot_router.py`, `frontend/src/pages/tarot/TarotPage.jsx` | Yes | Yes | `/api/tarot/spreads`, `/api/tarot/favorable-periods`, `/api/tarot/offers`, `/api/tarot/reading/{report_id}` | Yes | None | 🔵 Low | Public spreads endpoint live and returns full catalogue including premium spreads. User/report-specific endpoint behavior remains auth/data dependent as expected. |
| TAR-Manifestation | Manifestation Journal, calendar data, reminders, tasks, stats | `backend/tarot_router.py`, `frontend/src/pages/tarot/TarotPage.jsx` | Yes | Yes | `/tarot` (Journal tab), `/api/tarot/manifestations`, `/api/tarot/manifestation/stats` | Yes | None confirmed | 🔵 Low | UI and backend routes are present. Manifestation data persistence requires authenticated user session and MongoDB writes; no confirmed integration gap in this audit. |
| TAR-Docs | Tarot reconciliation, v4 handoff, and Common Space audit records | `Codex_Deliveries/Tarot/`, Common Space Tarot packet docs | Yes | Not Applicable | Not Applicable | Not Applicable | None | 🔵 Low | Documentation/reconciliation work remains separate from runtime app integration. Current tracker distinguishes remediation slice from later v4 UI uplift. |
| TAR-SEO-1 | Tarot SEO module: hub + 199 programmatic pages + sitemap/cache wiring | `backend/tarot_seo_data.py`, `backend/tarot_seo_router.py`, `frontend/src/pages/tarot-seo/`, `frontend/src/App.js`, `frontend/vercel.json`, `frontend/public/sitemap-index.xml` | Yes | No | Not Applicable | Not Applicable | Local-only delivery; Temple Team has not merged or deployed the Tarot SEO bundle yet. | 🟠 High | This thread delivered the router, four SEO page templates, sitemap endpoint wiring, and cache headers without touching `backend/tarot_router.py` or the interactive Tarot page. |
| TAR-SEO-2 | Tarot SEO content rewrite for spreads + cards | `backend/tarot_seo_data.py` | Yes | No | Not Applicable | Not Applicable | Rewrite exists only in local repo state and depends on TAR-SEO-1 integration to have any production effect. | 🔶 Medium | Rewrote spread/card copy to remove repeated phrasing while preserving record counts (`100` spreads, `78` cards, `20` intentions). |

**Tarot Thread -- Audit Summary**
- Overall Status: PARTIAL -- core Tarot runtime is live, but TAR-SEO-1 and TAR-SEO-2 remain local-only and are not integrated
- Total Rows Audited: 11
- Gaps Found: 2
- Signed off by TAR Thread: 2026-05-27

---

## SECTION 7 -- Kundali Thread

> Review all Kundali commissions AND any additional work done that is not listed. Add rows as needed.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| KUN-1 | Lagna Kundali Frontend -- `/kundali` route | `frontend/src/pages/BirthChartPage.jsx` or `KundaliPage.jsx`, `App.js` route | | | `/kundali` | | | | |
| KUN-1 | Kundali Detail View -- `/kundali/view/:chartId` | Detail page component + route | | | `/kundali/view/[id]` | | | | |
| KUN-1 | Unknown Birth Time checkbox | UI element in Kundali form | | | `/kundali` (form) | | | | |
| KUN-1 | House Summary table | House summary component | | | `/kundali/view` | | | | |
| KUN-Shadbala | Shadbala Engine | `backend/vedic_calculator.py` Shadbala functions | | | `/api/kundali` (response payload) | | | | |
| _(add rows)_ | | | | | | | | | |

**Kundali Thread -- Audit Summary**
- Overall Status: _(fill in)_
- Total Rows Audited: ___
- Gaps Found: ___
- Signed off by KUN Thread: _(date)_

---

## SECTION 8 -- Lal Kitab (LK) Thread

> Review all LK work delivered AND any additional work not listed. LK-1 is in reconciliation phase -- audit what is live now.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| LK-1 | LK Remedies Router (existing runtime found) | `backend/lk_remedies_router.py` | | | `/api/lk/remedies` | | | | |
| LK-1 | LK Diagnostics (existing runtime found) | `backend/lk_diagnostics.py` | | | `/api/lk/diagnostics` | | | | |
| LK-1 | LK Frontend Pages (7 pages in `pages/lk/`) | `frontend/src/pages/lk/` | | | `/lk/` | | | | |
| LK-1 | 361 LK Rules + Affliction Tags seeded in MongoDB | MongoDB `lk_rules` collection | `N/A` | `N/A` | `N/A` | `N/A` | DB-only | | |
| LK-1 | Premium Gating on LK paid features | Premium gate wiring | | | `/lk/` (premium features) | | | | |
| LK-1 | Conflict Interstitial + Tracker Rule Parity | _(in progress)_ | `N/A` | `N/A` | `N/A` | `N/A` | In progress | | |
| _(add rows)_ | | | | | | | | | |

**LK Thread -- Audit Summary**
- Overall Status: _(fill in)_
- Total Rows Audited: ___
- Gaps Found: ___
- Signed off by LK Thread: _(date)_

---

## SECTION 9 -- Longevity Thread

> Review all Longevity commissions AND any additional work done that is not listed. Add rows as needed.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| LON-1 | Longevity backend router + server include + contract aliases | `backend/longevity_router.py`, `backend/server.py` | Yes | Yes | `/api/longevity/eligibility`, `/api/longevity/report` | Yes | None on route presence. | 🔵 Low | Live probes on 2026-05-27 confirmed `GET /eligibility` returned the pricing/disclaimer payload, empty `POST /report` returned FastAPI validation, and auth-gated routes `/save`, `/history`, `/my-reports`, `/alerts`, and `/report/[id]` all responded from the deployed backend. |
| LON-1 | Deterministic KP engine + live preview generation | `backend/kp_engine.py`, `backend/longevity_router.py` | Yes | Yes | `/api/longevity/generate` | Yes | Preview generation succeeded, but the live response took about 46 seconds, far above the module target of under 10 seconds total. | 🟠 High | Live preview POST on 2026-05-27 returned a full report payload and reported `knowledge_engine.available = true`. |
| LON-1 | Longevity frontend page + live route aliases | `frontend/src/pages/reports/LongevityReportPage.jsx`, `frontend/src/App.js`, `frontend/src/components/NavBar.jsx` | Yes | Yes | `/longevity`, `/longevity-report` | Yes | None observed in live browser render. | 🔵 Low | Chrome verification on 2026-05-27 showed the mandatory disclaimer, premium state, section preview cards, and input form rendering successfully. |
| LON-1 | Save + history + alerts flow | `backend/longevity_router.py`, `frontend/src/pages/reports/LongevityReportPage.jsx` | Yes | Partial | `/api/longevity/save`, `/api/longevity/history`, `/api/longevity/my-reports`, `/api/longevity/alerts` | Error: unauthenticated live probes return `Authenticated user email or explicit user_email is required.` | Authenticated end-to-end save/history/alerts verification was not completed in this audit. | 🔶 Medium | Route presence is confirmed, but this pass did not complete a persisted full-report journey on production. |
| LON-1 | Report detail route (`/longevity/report/:reportId`) | `frontend/src/pages/reports/LongevityReportPage.jsx`, `frontend/src/App.js`, `backend/longevity_router.py` | Yes | Partial | `/longevity/report/[id]`, `/api/longevity/report/[id]` | Error: tested fake ID returned `Longevity report not found.` | Browser/API verification with a persisted full-report ID remains open, so the saved-report detail journey is not fully signed off. | 🔶 Medium | Frontend and backend route aliases are present in repo and deployed, but preview IDs are not persisted. |

**Longevity Thread -- Audit Summary**
- Overall Status: PARTIAL -- live page and preview API are working in production, but preview latency misses target and the authenticated save/detail journey is not fully verified
- Total Rows Audited: 5
- Gaps Found: 2
- Signed off by LON Thread: 2026-05-27

---

## SECTION 10 -- SEO Legacy Thread

> Review all SEO commissions M1-M3 and SEO-B/C series. Add rows for any unlisted work. M4 is on hold -- mark N/A.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| SEO-B1 | 36 Per-Sign Horoscope Pages (tomorrow / weekly / monthly) | `frontend/src/pages/horoscope/HoroscopeSignPage.jsx`, `frontend/src/components/HoroscopeCard.jsx`, `frontend/src/App.js`, `backend/server.py` | Yes | Yes | `/horoscope/aries/tomorrow` | Yes | None | 🔵 Low | Live public route returned `200`; backend support for `tomorrow`, `weekly`, and `monthly` is integrated. |
| SEO-B2 | Festival Pages -- Holi, Diwali, Karwa Chauth | `frontend/src/pages/festivals/FestivalPage.jsx`, `frontend/src/App.js` | Yes | Yes | `/festivals/holi` | Yes | None | 🔵 Low | Sample live route returned `200`; page family depends on the Panchang festival engine now live from B3/M1 work. |
| SEO-B3 | Festival Hub + Indian Calendar + Hora Today | `frontend/src/pages/festivals/FestivalsHubPage.jsx`, `frontend/src/pages/calendar/IndianCalendarPage.jsx`, `frontend/src/pages/hora/HoraTodayPage.jsx`, `frontend/src/App.js`, `backend/panchang_router.py` | Yes | Yes | `/festivals`, `/calendar`, `/hora` | Yes | None | 🔵 Low | All three public surfaces are live; sample frontend routes and `/api/panchang/hora` returned success in audit. |
| SEO-C1 | Legal Pages noindex + Policy Seed | `frontend/src/pages/system/PolicyPage.jsx`, `backend/scripts/seed_policies_v1.py` | Yes | Yes | `/privacy`, `/terms`, `/refund-policy`, `/cookie-policy`, `/subscription-terms` | Yes | None | 🔵 Low | Public legal routes returned `200`; content is live and indexation controls are in place. |
| SEO-C2 | Rashi Calculator + Nakshatra Calculator | `frontend/src/pages/calculators/RashiCalculatorPage.jsx`, `frontend/src/pages/calculators/NakshatraCalculatorPage.jsx`, `frontend/src/App.js`, `backend/server.py` | Yes | Yes | `/rashi-calculator`, `/nakshatra-calculator` | Yes | None | 🔵 Low | Public calculator routes returned `200`; backend alias `/api/calculate-birth-chart` is live. |
| SEO-C3 | Name Compatibility | `frontend/src/pages/calculators/NameCompatibilityPage.jsx`, `frontend/src/App.js`, `backend/numerology_router.py` | Yes | Yes | `/compatibility/name` | Yes | None | 🔵 Low | Public route returned `200`; backing POST endpoint is live and responds with request validation when called without payload. |
| SEO-C4 | Ekadashi / Amavasya / Purnima Hubs | `frontend/src/pages/devotional/DevotionalDatePage.jsx`, `frontend/src/App.js` | Yes | Yes | `/ekadashi`, `/amavasya`, `/purnima` | Yes | None | 🔵 Low | Sample live route returned `200`; pages are integrated to existing festival/date APIs. |
| SEO-C5 | Marriage Muhurat Page | `frontend/src/pages/muhurat/MarriageMuhuratPage.jsx`, `frontend/src/App.js`, `backend/panchang_router.py` | Yes | Yes | `/muhurat/marriage` | Yes | None | 🔵 Low | Public route and backend endpoint `/api/panchang/muhurat/marriage` both returned success in audit. |
| SEO-C6 | Report Category Discovery Pages | `frontend/src/pages/reports/category/`, `frontend/src/App.js` | Yes | Partial | `/reports/kundali` | Yes | Discovery/category pages are live, but downstream paid report purchase flow is still launch-gated on Razorpay/live-sales enablement. | 🔶 Medium | Sample live category route returned `200`; module should stay marked partial until Temple confirms the intended commercial launch state. |
| SEO-C7 | Celebrity Horoscope Hub | `frontend/src/pages/celebrity/CelebrityHubPage.jsx`, `frontend/src/pages/celebrity/CelebrityChartPage.jsx`, `frontend/src/App.js`, `backend/server.py` | Yes | Yes | `/celebrity-horoscopes` | Yes | None | 🔵 Low | Public hub route returned `200`; backing `/api/celebrities` endpoint also returned `200`. |
| SEO-C8 | Love Calculator | `frontend/src/pages/calculators/LoveCalculatorPage.jsx`, `frontend/src/App.js`, `backend/server.py`, `backend/numerology_router.py` | Yes | Yes | `/love-calculator` | Yes | None | 🔵 Low | Public route returned `200`; live feature is present in the deployed bundle. |
| SEO-C9 | Angel Numbers Hub -- 14 pages | `frontend/src/pages/angel-numbers/AngelNumbersHubPage.jsx`, `frontend/src/pages/angel-numbers/AngelNumberPage.jsx`, `frontend/src/pages/angel-numbers/angelNumberContent.js`, `frontend/src/App.js` | Yes | Partial | `/angel-numbers` | Yes | Original legacy 14-page delivery is no longer the sole live owner; Angel Numbers are now governed by dedicated ANGEL commissions and live content quality depends on those seeded collections. | 🔶 Medium | Public route returned `200`, but this legacy commission should remain partial because the production feature set has moved under ANGEL-1/ANGEL-2 ownership. |
| SEO-20K M1 | SEO infra + City Panchang + Choghadiya | `backend/seo_router.py`, `frontend/src/components/SEO.jsx`, `frontend/src/pages/panchang/CityPanchangPage.jsx`, `frontend/src/pages/panchang/ChoghadiyaPage.jsx`, `frontend/src/App.js`, `frontend/vercel.json`, `frontend/public/sitemap-index.xml`, `frontend/public/robots.txt` | Yes | Yes | `/panchang/new-delhi-india/2026-05-27`, `/choghadiya/new-delhi-india/today` | Yes | None | 🔵 Low | Both sample public routes returned `200`; sitemap endpoints `/api/seo/sitemap/panchang` and `/api/seo/sitemap/choghadiya` are live. |
| SEO-20K M2 | Compatibility + Remedy Hubs | `backend/compatibility_router.py`, `backend/remedy_matching_router.py`, `backend/seo_router.py`, `frontend/src/pages/kundali/CompatibilityPage.jsx`, `frontend/src/pages/remedies/RemedyHubPage.jsx`, `frontend/src/App.js`, `frontend/vercel.json` | Yes | Yes | `/compatibility/aries-and-scorpio`, `/remedies/shani-sade-sati` | Yes | None | 🔵 Low | Sample public routes returned `200`; backing endpoints and sitemap coverage are live. |
| SEO-20K M3 | Transit Profiles + Festival Regions + Character Placements | `backend/seo_m3_router.py`, `backend/seo_m3_catalog.py`, `backend/seo_m3_builders.py`, `frontend/src/pages/seo/TransitProfilePage.jsx`, `frontend/src/pages/seo/FestivalRegionPage.jsx`, `frontend/src/pages/seo/CharacterPlacementPage.jsx`, `frontend/src/App.js`, `frontend/vercel.json`, `frontend/public/sitemap-index.xml` | Yes | Yes | `/transits/sun-in-aries`, `/festivals/diwali/gujarat`, `/traits/scorpio/moon/7th-house` | Yes | None in the core route set | 🔵 Low | All three sample route families returned `200`; `/api/seo/sitemap/transits` also returned live XML. |
| SEO-20K M4 | TAR-SEO (199 Tarot SEO pages) | `backend/tarot_seo_data.py`, `backend/tarot_seo_router.py`, `frontend/src/pages/tarot-seo/`, `frontend/src/App.js`, `frontend/vercel.json`, `frontend/public/sitemap-index.xml` | Yes | No | Not Applicable | Not Applicable | Local-only Tarot SEO bundle was delivered in this thread but has not been merged or deployed. | 🟠 High | Keep this marked not integrated until Temple Team decides merge/deploy timing for the Tarot SEO module. |
| M3-FIX-1 | Festival-region summary variation fix | `backend/seo_m3_builders.py` | Yes | No | `/festivals/diwali/gujarat` | Yes | Generator-level summary-variation fix exists only locally; live festival-region pages still need the updated builder merged and re-seeded. | 🟠 High | Public page family is live, but the content-quality fix itself is not yet integrated into production data. |

**SEO Thread -- Audit Summary**
- Overall Status: MOSTLY INTEGRATED -- SEO-B/C and SEO-20K M1-M3 are live; SEO-C6 is partial; SEO-20K M4 and M3-FIX-1 are not integrated
- Total Rows Audited: 17
- Gaps Found: 4
- Signed off by SEO Thread: 2026-05-27

---

## SECTION 11 -- Remedies Thread

> Review all Remedies commissions AND any additional work done that is not listed. Add rows as needed.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| REM-P1 | `/ref/` Remedy Reference Endpoint | `backend/remedies_router.py` | Yes | Partial | `/api/remedies/ref/kp-001` | Error: `{"detail":"Remedy ref 'kp-001' not found or not approved"}` | Endpoint is live, but KP fallback references are unusable in production until the seeded KP remedy records are in an approved status path compatible with `/ref`. | 🟠 High | Earlier tracker file path `backend/server.py` was stale. |
| REM-P1 | 36 KP Remedy Records seeded in MongoDB | MongoDB `krishna_prashnavali_remedies` collection, `backend/scripts/ingest_krishna_prashnavali_remedies_v1.py` | `N/A` | `N/A` | `N/A` | `N/A` | Records exist, but live `/api/remedies/traditions` shows `total_records: 36` and `approved_records: 0`, which blocks live `/ref` resolution. | 🟠 High | KP runtime now primarily uses in-bundle remedies, so this gap mainly affects fallback/admin/reference behavior. |
| REM-P1 | KP Fallback Wiring in remedy lookup | `backend/remedies_router.py`, `backend/scriptural_oracle_router.py` | Yes | Partial | `N/A` | `N/A` | Fallback is internal rather than a stable public URL surface, and it currently depends on `/ref` records that are not approved. | 🔶 Medium | Earlier tracker URL `/api/kp/verdict` was stale and does not reflect the current runtime contract. |
| ⚠️ OPEN | Verdict split is 10/8/8/10 (YES/WAIT/NO/PRAY) -- spec was 9/9/9/9. Confirm intentional or re-seed. | DB audit | `N/A` | `N/A` | `N/A` | `N/A` | Confirm split | 🔶 Medium | No live runtime break confirmed from this audit, but the historical spec mismatch remains worth closing explicitly. |
| UNLISTED-REM-1 | `POST /api/remedies/suggest` cross-tradition remedy suggestion endpoint | `backend/remedies_router.py` | Yes | Yes | `/api/remedies/suggest` | Yes | Live sample request succeeded, but returned an empty `remedies` array for a Daily Horoscope-style test input, so dependent UI may silently render nothing in production. | 🟠 High | Added because this was a major delivered endpoint and was not pre-listed. |
| UNLISTED-REM-2 | `GET /api/remedies/traditions` collection summary endpoint | `backend/remedies_router.py` | Yes | Yes | `/api/remedies/traditions` | Yes | None at route level; operational signal shows `approved_records: 0` for key traditions, including KP. | 🔶 Medium | Useful live proof surface for the actual state of remedy collections. |
| UNLISTED-REM-3 | Remedies Admin records/status API + admin UI | `backend/remedies_router.py`, `frontend/src/pages/admin/RemediesAdminPanel.jsx`, `frontend/src/pages/admin/AdminDashboard.jsx` | Yes | Partial | `/api/remedies/admin/records` | Error: `{"detail":"Admin authentication required"}` | Backend admin route is live, but this audit did not verify authenticated admin UI deployment or status-change flow in production. | 🔶 Medium | Auth error confirms the route exists and is protected as expected. |
| UNLISTED-REM-4 | Daily Horoscope "Today's Vedic Remedy" card | `frontend/src/pages/horoscope/DailyHoroscope.jsx`, `backend/remedies_router.py` | Yes | Partial | `/horoscope/daily` | Yes | Public route shell is live, but with live `/suggest` currently returning empty results for sampled public input, the remedy card may not render at all in production. | 🟠 High | This is a functional integration risk rather than a route outage. |
| CRY-1 | Crystal Healing base module -- hub, 50 crystal pages, 20 intention pages, calculator API/UI, and sitemap | `backend/crystal_data.py`, `backend/crystal_router.py`, `backend/seo_router.py`, `backend/server.py`, `backend/vedic_calculator.py`, `frontend/src/pages/crystals/`, `frontend/src/App.js`, `frontend/public/sitemap-index.xml`, `frontend/vercel.json` | Yes | Yes | `/crystals`, `/api/crystals/list`, `/api/seo/sitemap/crystals`, `/crystals/calculator` | Yes | None | 🔵 Low | Live `GET` probes passed for the catalog and crystal sitemap, the deployed frontend bundle contains the Crystal route chunks, and calculator `POST` returned `200` with production payload shape on 2026-05-27. |
| CRY-2 | Crystal expansion -- 9 planet pages, 12 sign pages, 20 problem-area pages, hub discoverability, and route-order protection | `backend/crystal_data.py`, `backend/crystal_router.py`, `backend/scripts/seed_crystals.py`, `frontend/src/pages/crystals/CrystalPlanetPage.jsx`, `frontend/src/pages/crystals/CrystalSignPage.jsx`, `frontend/src/pages/crystals/CrystalProblemPage.jsx`, `frontend/src/pages/crystals/CrystalHubPage.jsx`, `frontend/src/App.js` | Yes | Yes | `/crystals/for/planet/sun`, `/crystals/for/sign/aries`, `/crystals/for/problem/insomnia`, `/api/crystals/planet/sun` | Yes | None | 🔵 Low | Live API probes for planet, sign, and problem pages returned expected JSON. The public crystal sitemap now exposes the full 113-URL Crystal surface in production. |
| UNLISTED-REM-CRY-SEED | Crystal seed script and collection expansion for `crystals`, `crystal_intentions`, `crystal_planets`, `crystal_signs`, and `crystal_problems` | `backend/scripts/seed_crystals.py` | Yes | `N/A` | `N/A` | `N/A` | No public endpoint for the seed script itself. | 🔵 Low | Runtime surfaces are already live; this row covers the operational seeding asset only. |

**Remedies Thread -- Audit Summary**
- Overall Status: PARTIAL -- Crystal Healing CRY-1 and CRY-2 are live in production, while legacy Remedies gaps remain around KP reference approvals and empty public suggestion results.
- Total Rows Audited: 11
- Gaps Found: 3 consolidated items -- 2 production issues (`/ref` approval-state and empty `/suggest` results) plus 1 medium open-spec verdict-split question
- Signed off by REM Thread: 2026-05-27

---

## SECTION 12 -- Punya Rewards Thread

> Review all Punya commissions AND any additional work done that is not listed. Add rows as needed.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| PUN-1 | Punya Gamification Engine backend, ledger APIs, spin APIs, leaderboard, and server registration | `backend/punya_rewards_router.py`, `backend/punya_rewards_service.py`, `backend/server.py` | Yes | Yes | `/api/punya/leaderboard` | Yes | None observed from unauthenticated live probe | 🔵 Low | Live `GET` probe returned leaderboard JSON from `https://everydayhoroscope-api.onrender.com/api/punya/leaderboard`; repo also confirms `app.include_router(punya_rewards_router)` in `backend/server.py`. |
| PUN-2 | Landing promo block + SVG wheel teaser + countdown/streak callouts | `frontend/src/pages/home/Landing.jsx`, `frontend/src/pages/rewards/PunyaRewardsPage.jsx` | Yes | Yes | `/` | Yes | None observed from public route probe | 🔵 Low | Landing page returns `200` in production. PUN-2 promo copy and rewards-page teaser strings are present in the deployed frontend bundle. |
| PUN-2 | Rewards page uplift: SVG wheel, Daily Blessing countdown, streak card, and grouped/color-coded ledger view | `frontend/src/pages/rewards/PunyaRewardsPage.jsx` | Yes | Partial | `/punya-rewards` | Yes | Public route is live, but authenticated ledger/spin rendering was not exercised end-to-end in this audit | 🔶 Medium | Production route returns `200`, and `/punya-rewards` is present in the deployed JS bundle. Full logged-in interaction still needs smoke coverage. |
| UNLISTED-PUN-01 | Protected `/punya-rewards` route, user-menu entry, balance badge, and client helper layer | `frontend/src/App.js`, `frontend/src/components/UserAccountMenu.jsx`, `frontend/src/lib/punyaRewards.js` | Yes | Yes | `/punya-rewards` | Yes | None confirmed beyond auth-required interaction limits | 🔵 Low | Repo wiring confirms the protected route and dropdown link; the production app shell serves the route successfully. |
| UNLISTED-PUN-02 | Admin Console Punya Rewards configuration tab | `frontend/src/pages/admin/PunyaRewardsAdminPanel.jsx`, `frontend/src/pages/admin/AdminDashboard.jsx` | Yes | Partial | `/admin/dashboard` | Yes | Admin-authenticated Punya tab interaction was not validated live in this audit | 🔶 Medium | Repo mount is present and the public admin route shell returns `200`, but an authenticated admin walk-through was not performed here. |
| UNLISTED-PUN-03 | Cross-module earn hooks across Horoscope, Tarot, Panchang, Numerology, and Birth Chart pages | `frontend/src/pages/horoscope/DailyHoroscope.jsx`, `frontend/src/pages/horoscope/WeeklyHoroscope.jsx`, `frontend/src/pages/horoscope/MonthlyHoroscope.jsx`, `frontend/src/pages/tarot/TarotPage.jsx`, `frontend/src/pages/panchang/PanchangPage.jsx`, `frontend/src/pages/numerology/NumerologyPage.jsx`, `frontend/src/pages/kundali/BirthChartPage.jsx`, `frontend/src/lib/punyaRewards.js` | Yes | Partial | `Multiple module routes` | Not Applicable | Repo hooks are wired, but live reward-claim calls were not individually observed during this audit | 🔶 Medium | Confirmed repo action hooks for `horoscope_daily_view`, `horoscope_weekly_view`, `horoscope_monthly_view`, `tarot_daily_draw`, `tarot_spread_complete`, `tarot_bookmark`, `panchang_daily_view`, `numerology_report_generate`, and `birth_chart_generate`. |
| ⚠️ PUN-OP-1 | `individual_report` reward mapping requested by PUN-2 brief is still missing from backend action rules | `backend/punya_rewards_service.py` `DEFAULT_ACTION_RULES`, `frontend/src/pages/reports/IndividualReportsPage.jsx` | Yes | Partial | `N/A` | `N/A` | Action code missing -- Punya points are not awarded for Individual Reports because backend does not define `individual_report` and no frontend hook is wired | 🔶 Medium | `award_punya_action(...)` returns `unknown_action` for unmapped codes. The live-safe choice remains to leave Individual Reports unwired until Temple defines a canonical action code. |

**Punya Rewards Thread -- Audit Summary**
- Overall Status: PARTIAL -- backend and public Punya surfaces are live; authenticated user/admin smoke coverage is still incomplete, and the `individual_report` reward mapping remains open
- Total Rows Audited: 7
- Gaps Found: 2
- Signed off by PUN Thread: 2026-05-27

---

## SECTION 13 -- Lo Shu Grid Thread

> LSG-1 is delivered but pending integration into the main repo. Audit what you have built and confirm delivery is complete.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| LSG-1 | Lo Shu Grid Backend Router | `backend/lo_shu_grid_router.py` | | `No` | `/api/lo-shu/` | `N/A` | Delivered locally -- pending Temple Team integration | 🟠 High | |
| LSG-1 | 4 Public Frontend Pages | `frontend/src/pages/lo-shu/` | | `No` | `/lo-shu-grid` | `N/A` | Pending integration | 🟠 High | |
| LSG-1 | Sitemap entries + vercel.json cache headers | `sitemap.xml`, `vercel.json` additions | | `No` | `N/A` | `N/A` | Pending integration | 🟠 High | |
| LSG-1 | Seed Script | `backend/scripts/seed_lo_shu.py` | | `No` | `N/A` | `N/A` | Pending integration | 🟠 High | |
| _(add rows for any other work delivered)_ | | | | | | | | | |

**Lo Shu Grid Thread -- Audit Summary**
- Overall Status: DELIVERED -- PENDING INTEGRATION
- Total Rows Audited: ___
- Gaps Found: _(list any gaps in your own delivery)_
- Signed off by LSG Thread: _(date)_

---

## SECTION 14 -- Love Module Thread

> Review all Love Module commissions AND any additional work done that is not listed. Add rows as needed.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| LOVE-1 | Love & Engagement Module Backend | Love module backend router | | | `/api/love/` | | | | |
| LOVE-FE | Love Module Frontend + SEO | `frontend/src/pages/love/` hub + landing | | | `/love` | | | | |
| _(add rows)_ | | | | | | | | | |

**Love Module Thread -- Audit Summary**
- Overall Status: _(fill in)_
- Total Rows Audited: ___
- Gaps Found: ___
- Signed off by LOVE Thread: _(date)_

---

## SECTION 14A -- Notification Engine Thread

> Notification Engine was not pre-listed in the central tracker. These rows were added during audit for the shared backend notification infrastructure delivered by this thread.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| UNLISTED-NOTIF-01 | Notification preferences, in-app feed, and admin log routers | `backend/notification_preferences_router.py`, `backend/notification_feed_router.py`, `backend/notification_log_router.py`, `backend/server.py` | Yes | Yes | `/api/notifications/preferences`, `/api/notifications/feed`, `/api/notifications/log` | Yes -- live probes returned expected `401 Authentication required` for user routes and `403 Admin access required` for the admin log route | None at route level. Authenticated end-to-end user/admin journeys were not exercised in this audit. | 🔵 Low | Repo confirms all three routers are present and included in `backend/server.py`. |
| UNLISTED-NOTIF-02 | Trigger router + Temple scheduler wiring for report-ready, Panchang daily, encounter window, Love Weather weekly, and Date Night Score | `backend/notification_trigger_router.py`, `backend/server.py` | Yes | Yes | `/api/notifications/trigger/report-ready` | Yes -- live probe returned expected `403 Invalid trigger key` | None at route level. Actual sends require a valid Temple trigger key and downstream channel readiness. | 🔵 Low | `backend/server.py` contains the trigger call helper plus APScheduler jobs for four scheduled notification triggers. |
| UNLISTED-NOTIF-03 | Transactional email delivery service via Resend | `backend/notification_email_service.py`, `backend/notification_trigger_router.py` | Yes | Yes | `N/A` | `N/A` | No direct public URL; service runs inside trigger flows. No current production failure signal surfaced in this audit. | 🔵 Low | Prior Temple acceptance for this thread explicitly confirmed `report-ready` email delivery via Resend in production. |
| UNLISTED-NOTIF-04 | WhatsApp channel service with graceful skip behavior when BSP/env is unavailable | `backend/notification_whatsapp_service.py`, `backend/notification_trigger_router.py` | Yes | Partial | `N/A` | `N/A` | WhatsApp delivery remains intentionally non-operational in production until BSP setup and valid credentials are completed. | 🔶 Medium | This is a planned partial integration state, not a missing repo file. |
| UNLISTED-NOTIF-05 | Web push backend service, dependency, and push subscription API | `backend/notification_push_service.py`, `backend/notification_push_router.py`, `backend/server.py`, `backend/requirements.txt` | Yes | Partial | `/api/notifications/push/subscribe` | Yes -- unauthenticated live `POST` returned expected `401 Authentication required` | Push backend is deployed, but production push delivery still depends on VAPID env vars plus Temple-owned frontend service worker and subscription flow. | 🔶 Medium | Repo confirms `pywebpush==2.0.0` in `backend/requirements.txt`; no frontend notification bell or push UI was part of this thread. |

**Notification Engine Thread -- Audit Summary**
- Overall Status: PARTIAL -- backend notification infrastructure is live and deployed, but WhatsApp and push channels remain only partially operational because Temple-owned activation steps are still pending
- Total Rows Audited: 5
- Gaps Found: 2 consolidated channel-activation gaps (WhatsApp BSP/credentials and push VAPID + frontend activation)
- Signed off by Notification Engine Thread: 2026-05-27

---

## SECTION 15 -- Panchang Thread

> Review all Panchang commissions AND any additional work done that is not listed. Add rows as needed.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| PAN-L1 | Language/Regional Pages -- 5-language config, hreflang, JSON-LD | `frontend/src/pages/PanchangPage.jsx` language config additions | | | `/panchang` | | | | |
| PAN-L1 | HTTP 200 confirmed on all 5 language routes | `App.js` route wiring | | | `/panchang/[lang]` (all 5) | | | | |
| _(add rows for any other work delivered)_ | | | | | | | | | |

**Panchang Thread -- Audit Summary**
- Overall Status: _(fill in)_
- Total Rows Audited: ___
- Gaps Found: ___
- Signed off by PAN Thread: _(date)_

---

## SECTION 16 -- ECHO//PACE Thread

> Review all ECHO//PACE work delivered in the dedicated admin-console commission thread. Add rows for any follow-up delivery work if needed.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| ECHO-1 | ECHO//PACE backend engine, admin API, audit log index, PDF export | `backend/echo_pace_engine.py`, `backend/echo_pace_router.py`, `backend/server.py`, `backend/requirements.txt` | Yes | Yes | `/api/admin/echo-pace/history` | Yes | None observed from unauthenticated live probe | 🔵 Low | Live `GET` probe returned expected `401 Admin authentication required`, confirming deployed admin route exists. Authenticated end-to-end process run was not performed in this audit. |
| ECHO-1 | ECHO//PACE Admin Console tab with Process + History UI | `frontend/src/components/admin/EchoPaceTab.jsx`, `frontend/src/pages/admin/AdminDashboard.jsx` | Yes | Partial | `/admin/dashboard` | Error: route loads but deployed JS bundle lacks `echo-pace` / `EchoPace` strings | ECHO//PACE frontend tab is present in repo but not present in the currently deployed frontend bundle, so the UI is not live in production. | 🟠 High | Public route returns `200`, but production bundle `/static/js/main.9f2aa2a5.js` does not contain the ECHO//PACE admin tab strings from the delivered component. |

**ECHO//PACE Thread -- Audit Summary**
- Overall Status: PARTIAL -- backend route live, frontend admin tab not deployed
- Total Rows Audited: 2
- Gaps Found: 1
- Signed off by ECHO Thread: 2026-05-27

---

## SECTION 17 -- Angel Numbers Thread

> Review all Angel Numbers work delivered in ANGEL-1 and ANGEL-2, plus any additional delivered files such as routes, seed scripts, tests, and sitemap work.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| ANGEL-1 | Full Angel Numbers backend -- generator, router, API endpoints, paginated sitemap | `backend/angel_numbers_data.py`, `backend/angel_numbers_router.py`, `backend/server.py` | Yes | Partial | `/api/seo/angel-numbers/hub`, `/api/seo/angel-numbers/111`, `/api/seo/angel-numbers/111/love`, `/api/seo/sitemap/angel-numbers?page=1` | Yes | Live API and sitemap respond, but `/api/seo/angel-numbers/111` and `/api/seo/angel-numbers/111/love` still return pre-ANGEL-2 content from stored Mongo documents, including the old universal closing sentence and generic intent action steps. | 🟠 High | Repo contains the ANGEL-2 rewrite logic, so the live mismatch appears to be stale DB content overriding generated output rather than missing code files. |
| ANGEL-1 | Full Angel Numbers frontend -- hub, core page, intent page, route wiring | `frontend/src/pages/angel-numbers/AngelNumbersHubPage.jsx`, `frontend/src/pages/angel-numbers/AngelNumberPage.jsx`, `frontend/src/pages/angel-numbers/AngelNumberIntentPage.jsx`, `frontend/src/pages/angel-numbers/angelNumbersApi.js`, `frontend/src/App.js` | Yes | Partial | `/angel-numbers`, `/angel-numbers/111`, `/angel-numbers/111/love` | Yes | Routes return HTTP 200 and are wired in the repo, but the user-facing content path depends on API data that is still serving stale pre-ANGEL-2 records. | 🟠 High | Frontend integration is present in repo and deployed at route level; the current gap is content freshness/quality, not missing page wiring. |
| UNLISTED-ANGEL-1-SCRIPTS | Seed scripts for `angel_number_core` and `angel_number_intents` collections | `backend/scripts/seed_angel_numbers_core.py`, `backend/scripts/seed_angel_numbers_intents.py` | Yes | N/A | `N/A` | N/A | Scripts are present, but live API behavior indicates ANGEL-2-quality data has not been re-seeded into the live Mongo collections after the rewrite. | 🟠 High | This is the most likely operational gap behind the stale live payloads. |
| ANGEL-2 | Generator rewrite quality fix -- varied endings, intent-specific messages, intent-specific action steps | `backend/angel_numbers_data.py` | Yes | Partial | `/api/seo/angel-numbers/111/love` | Yes | Repo file contains the rewrite, but the live payload still exposes the old generic `message` body and old generic action steps, so ANGEL-2 is not effective in production. | 🟠 High | Verified by comparing repo content with live API output on 2026-05-27. |
| UNLISTED-ANGEL-TESTS | Automated data-contract tests for Angel Numbers generator | `tests/test_angel_numbers_data.py` | Yes | N/A | `N/A` | N/A | Internal QA asset only; no public URL expected. | 🔵 Low | Useful for regression checks, but not a live-app surface. |

**Angel Numbers Thread -- Audit Summary**
- Overall Status: PARTIAL -- ANGEL-1 is integrated at repo and route level, but ANGEL-2 quality rewrite is not effective on the live API because stale Mongo-backed content is still being served.
- Total Rows Audited: 5
- Gaps Found: 1 high-priority live-content gap (ANGEL-2 rewrite not reflected in live API / frontend content path)
- Signed off by Angel Numbers Thread: 2026-05-27

---

## SECTION 17 -- Live TV Thread

> Review all Live TV delivery work and any additional integration or asset-path changes that were required to make the feature playable in the real app.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| UNLISTED-LTV-01 | Dedicated SEO page + route + indexation entries for Sai Baba Arti | `frontend/src/pages/live/LiveSaiBabaArtiPage.jsx`, `frontend/src/App.js`, `frontend/public/robots.txt`, `frontend/public/sitemap.xml` | Yes | Yes | `/live-sai-baba-arti` | Yes | None | 🔵 Low | Public route returned HTTP 200 from `https://www.everydayhoroscope.in/live-sai-baba-arti` on 2026-05-27. |
| UNLISTED-LTV-02 | Fixed floating Live TV player for the public home experience | `frontend/src/components/LiveTVPanel.jsx`, `frontend/src/pages/home/Landing.jsx`, `frontend/src/components/NavBar.jsx` | Yes | Partial | `/` | Yes | Repo drift: `LiveTVPanel` is mounted in `frontend/src/pages/home/Home.jsx`, `frontend/src/pages/panchang/PanchangLandingPage.jsx`, and `frontend/src/pages/panchang/PanchangPage.jsx` in addition to `Landing.jsx`, so the locked "home page only (/)" scope is no longer respected. | 🟠 High | Homepage URL is live, but Temple Team should remove non-home mounts and then rerun a browser smoke test on `/`, `/home`, and Panchang routes. |
| UNLISTED-LTV-03 | Backend active-video API + media pipeline for Live TV | `backend/live_tv_router.py`, `backend/live_tv_service.py`, `backend/scripts/generate_live_tv_video.py`, `backend/server.py`, `backend/assets/live_tv/README.md` | Yes | Partial | `/api/live-tv/active` | Yes | Production API returns an active record, but `website_video_url` and `thumbnail_url` are emitted as `http://everydayhoroscope-api.onrender.com/...`; direct use from the `https://` frontend would cause mixed-content blocking. | 🟠 High | Current production frontend survives because `frontend/src/hooks/useLiveTv.js` overrides media URLs to static Vercel-hosted files. Backend contract still needs cleanup. |
| UNLISTED-LTV-04 | Static Vercel-hosted MP4/JPG playback assets used by production fallback path | `frontend/public/live_tv/active_live_tv.mp4`, `frontend/public/live_tv/active_live_tv.jpg`, `frontend/src/hooks/useLiveTv.js` | Yes | Yes | `/live_tv/active_live_tv.mp4` | Yes | None | 🔵 Low | Public MP4 and JPG returned HTTP 200 from Vercel on 2026-05-27 and are currently the real production playback path. |

**Live TV Thread -- Audit Summary**
- Overall Status: PARTIAL -- public SEO page and static playback path are live, but panel scope drift and backend media URL contract still need cleanup.
- Total Rows Audited: 4
- Gaps Found: 2
- Signed off by Live TV Thread: 2026-05-27

---


## SECTION 18 -- Palmistry Thread

> Review all Palmistry / Hasta Rekha work delivered by this thread. Palmistry was not pre-listed in the tracker, so these rows were added during audit.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| UNLISTED-PALM-1 | Palmistry analysis + structured Samudrika Shastra report API | `backend/palmistry_router.py`, `backend/palmistry_prompt_service.py`, `backend/server.py` | Yes | Yes | `/api/palmistry/analyse` | Yes | None | 🔵 Low | Live POST on 2026-05-27 returned a full structured report with derived hand shape and remedies. |
| UNLISTED-PALM-2 | Palmistry persistence + history/detail retrieval | `backend/palmistry_router.py` | Yes | Yes | `/api/palmistry/reports?user_email=audit.palmistry.integration@example.com`, `/api/palmistry/reports/[id]` | Yes | None | 🔵 Low | Live save test with audit email succeeded; list endpoint returned the saved record and detail lookup returned the full document. |
| UNLISTED-PALM-3 | Palmistry premium frontend route + questionnaire/report UI | `frontend/src/pages/palmistry/PalmistryPage.jsx`, `frontend/src/App.js`, `frontend/src/components/NavBar.jsx` | Yes | Yes | `/palmistry` | Yes | Frontend informational copy says palmistry combines hand analysis with Vedic birth data, but the current `/api/palmistry/analyse` runtime does not collect or send birth data in this flow. | 🔶 Medium | Verified by live `/palmistry` HTTP 200 plus deployed bundle strings for `/palmistry`, `Hasta Rekha`, and `Samudrika Shastra`; no browser-driven visual walkthrough was performed in this pass. |

**Palmistry Thread -- Audit Summary**
- Overall Status: LIVE WITH ONE CONTENT-INTEGRITY GAP
- Total Rows Audited: 3
- Gaps Found: 1
- Signed off by PALM Thread: 2026-05-27

---

## SECTION 19 -- Self-Healing Center Thread

> Review all SHC commissions (SHC-1 to SHC-3) and any follow-up delivery work. Add rows for any unlisted delivery surfaced in this audit.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| SHC-1 | Telemetry engine backend + `user_diagnostics` admin API + page-view / Razorpay telemetry wiring | `backend/server.py`, `backend/models/diagnostics.py`, `frontend/src/diagnostics/telemetry.js`, `frontend/src/App.js`, `frontend/src/components/PaymentModal.jsx`, `frontend/src/components/admin/DiagnosticsTab.jsx`, `frontend/src/pages/admin/AdminDashboard.jsx` | Yes | Partial | `/admin/dashboard`, `/api/diagnostics/log`, `/api/admin/diagnostics/test` | Error: `/admin/dashboard` returns `200`, but deployed JS bundle lacks `Self-Heal` / `Dispute Flagged` strings; `POST /api/diagnostics/log` returns `422` on empty body; `GET /api/admin/diagnostics/test` returns `401 Admin authentication required` | Telemetry backend and frontend event hooks are deployed, but the admin Self-Heal diagnostics UI is not present in the currently deployed frontend bundle. | 🟠 High | Live bundle contains `RAZORPAY_POPUP_OPEN` and `diagnostics/log`, confirming telemetry code is in production. Authenticated admin timeline flow was not exercised in this audit. |
| SHC-2 | Razorpay lifecycle ledger, gateway-open tracking, server-side webhook, and stuck-order self-heal jobs | `backend/server.py`, `backend/models/orders.py`, `frontend/src/components/PaymentModal.jsx`, `frontend/src/pages/kundali/BrihatKundliPage.jsx`, `frontend/src/components/admin/DiagnosticsTab.jsx` | Yes | Partial | `/api/webhooks/razorpay`, `/api/admin/orders/test`, `/api/diagnostics/order/test/gateway-open`, `/admin/dashboard` | Error: `POST /api/webhooks/razorpay` returns `422` for missing `x-razorpay-signature`; `GET /api/admin/orders/test` returns `401 Admin authentication required`; `POST /api/diagnostics/order/test/gateway-open` returns `404 Order ledger row not found`; `/admin/dashboard` returns `200`, but deployed JS bundle lacks `Lifecycle Ledger` / `Force Re-Run` strings | Backend lifecycle ledger and webhook routes are live, but the admin lifecycle ledger UI is not present in the deployed frontend bundle. End-to-end paid-order funnel verification against a real Razorpay payment was not performed in this audit. | 🟠 High | The webhook is deployed and validating request shape correctly. The gateway-open route is live and reaching order lookup logic. |
| SHC-3 | GST ledger, Gmail OAuth/sync scaffolding, support triage, and GST scheduler jobs | `backend/server.py`, `backend/models/gst.py`, `backend/services/gst_parser.py`, `backend/services/gmail_ingest.py`, `backend/requirements.txt`, `frontend/src/components/admin/DiagnosticsTab.jsx` | Yes | Partial | `/api/admin/gmail/auth-url`, `/api/admin/gmail/status`, `/api/admin/gst/summary`, `/admin/dashboard` | Error: admin Gmail/GST endpoints return `401 Admin authentication required`; `/admin/dashboard` returns `200`, but deployed JS bundle lacks `GST Ledger` / `Gmail` strings | Backend Gmail/GST routes are deployed, but the Gmail/GST admin UI is not in the live frontend bundle. Gmail/GST jobs also remain operationally blocked until Render Gmail env vars and OAuth refresh token are configured. Live `pdfplumber` runtime import was not directly confirmed in this audit. | 🟠 High | Repo code is designed to fail gracefully when Gmail vars are absent. This row includes vendor email ingest, daily GST summary, and support-ticket triage jobs. |

**SHC Thread -- Audit Summary**
- Overall Status: PARTIAL -- backend routes and telemetry hooks are live, but the Self-Heal admin frontend is not fully deployed and Gmail/GST activation is still pending
- Total Rows Audited: 3
- Gaps Found: 3
- Signed off by SHC Thread: 2026-05-27

---


## SECTION 20 -- Lumina Thread

> Review all Lumina Phase 1 delivery work and any live Temple-side amendments. Add rows for any unlisted Lumina delivery surfaced in this audit.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| LUM-1 | Lumina backend AI scripture + chaplain + discernment API suite | `backend/lumina_router.py`, `backend/lumina_prompt_service.py`, `backend/server.py` | Yes | Yes | `/api/lumina/daily-verse`, `/api/lumina/scripture`, `/api/lumina/chaplain` | Yes -- live probes on 2026-05-27 returned `200` for `daily-verse` (BIBLE and GITA), `scripture`, `chaplain`, `confessions`, `situation`, `kingdom-vision`, and `glory-scrolls` | None on read/AI route availability. | 🔵 Low | The deployed backend is serving Lumina content and the GITA toggle is active on the tested AI/read routes. |
| LUM-1 | Lumina prayer declarations + manifestation persistence flows | `backend/lumina_router.py`, `frontend/src/pages/lumina/LuminaPage.jsx` | Yes | Partial | `/api/lumina/prayers?user_email=audit@example.com`, `/api/lumina/manifestation?user_email=audit@example.com` | Yes -- safe GET probes returned `200` with an empty prayer list and the full 21-day manifestation payload | Live read endpoints are working, but production write paths for prayer create/strengthen/realize and manifestation day completion were not re-smoked in this audit to avoid mutating live user data. | 🔶 Medium | User-data routes are deployed; a controlled Temple audit account should verify persisted writes end to end. |
| LUM-FE-1 | Lumina route, page shell, nav entry, and home-card integration | `frontend/src/pages/lumina/LuminaPage.jsx`, `frontend/src/App.js`, `frontend/src/components/NavBar.jsx`, `frontend/src/pages/home/Home.jsx` | Yes | Partial | `/lumina` | Yes -- live route returns `200` from Vercel | The live Lumina frontend is deployed, but the production UX is the expanded 9-tab gold/premium-gated variant rather than the original 6-tab dark-indigo Phase 1 contract. | 🔶 Medium | Current repo path is `frontend/src/pages/lumina/LuminaPage.jsx`; route, nav, and home-surface wiring are present in production. |

**Lumina Thread -- Audit Summary**
- Overall Status: PARTIAL -- backend AI/read routes are live, safe persistence reads are live, but production write-path smoke coverage is incomplete and the frontend has Temple-side drift from the original Phase 1 contract
- Total Rows Audited: 3
- Gaps Found: 2
- Signed off by Lumina Thread: 2026-05-27

---
## SECTION 20 -- Numerology Thread

> Review all Numerology work delivered by this thread, including the core 10-tile module, Premium Ankjyotish, structured report renderer, and Temple-side integrated single-page Numerology flow.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| UNLISTED-NUM-01 | Numerology backend router -- 11 tiles, generate/retrieve/history/bookmark/feedback, Temple collection wiring | `backend/numerology_router.py`, `backend/numerology_prompt_service.py`, `backend/server.py` | Yes | Yes | `/api/numerology/tiles`, `/api/numerology/report/generate`, `/api/numerology/history` | Yes -- tiles returned `200`; empty POST generate returned expected `422`; history returned expected auth gate | None on route presence. Authenticated full history/bookmark flow was not re-smoked in this audit. | 🔵 Low | Live probes on 2026-05-27 confirm the backend is deployed and serving the current 11-tile catalog including Premium Ankjyotish. |
| UNLISTED-NUM-02 | Public Numerology landing + premium-gated single-page generate/report/history experience | `frontend/src/pages/numerology/NumerologyPage.jsx`, `frontend/src/App.js`, `frontend/src/numerology.css` | Yes | Yes | `/numerology` | Yes | Live route is up, but the integrated in-tab report flow uses a generic `ContinueJourney` CTA to Brihat Kundali instead of the approved tile-aware CTA map. | 🔶 Medium | Production route returned `200`. Repo wiring confirms `/numerology` lazy route plus premium-gated single-page report/history flow. |
| UNLISTED-NUM-03 | Standalone report page + structured components (`ContinueJourney`, `LoShuGrid`, `LuckyElementsTable`, `SEO`) | `frontend/src/pages/numerology/NumerologyReportPage.jsx`, `frontend/src/components/ContinueJourney.jsx`, `frontend/src/components/LoShuGrid.jsx`, `frontend/src/components/LuckyElementsTable.jsx`, `frontend/src/components/SEO.jsx` | Yes | Yes | `/numerology/report/test` | Yes | Route shell is live, but authenticated premium smoke with a real report ID was not completed in this audit; the richer standalone block set is also not mirrored inside the main in-tab `NumerologyPage` flow. | 🔶 Medium | Repo contains `RemediationPlan`, `TimingPanel`, `VedicCrossReference`, and `RemedyCard` in the standalone page. Public route probe on 2026-05-27 returned `200` HTML shell as expected for the SPA route. |
| UNLISTED-NUM-04 | Premium Ankjyotish structured payload + Temple Vedic auto-compute integration | `backend/numerology_router.py`, `backend/numerology_prompt_service.py`, `frontend/src/pages/numerology/NumerologyReportPage.jsx`, `frontend/src/components/LuckyElementsTable.jsx` | Yes | Partial | `/api/numerology/tiles` | Yes | Premium Ankjyotish is deployed, but backend payload has drift from the richer Codex-delivered contract: no `remedy_card`, no `supportive_gems` / `supportive_metals`, and no `remediation_plan` on `karmic_debt_loshu`, reducing structured frontend richness. | 🔶 Medium | Temple-side router adds live Vedic auto-compute and Claude enrichment, but it is not fully parity-aligned with the richer v2 delivery payload. |

**Numerology Thread -- Audit Summary**
- Overall Status: PARTIAL -- core Numerology routes, pages, and backend are live, but medium UX/payload drift remains and authenticated premium report journeys were not fully smoke-tested in this audit
- Total Rows Audited: 4
- Gaps Found: 2
- Signed off by Numerology Thread: 2026-05-27

---

## MASTER GAP REGISTER

> All threads add their gaps here. Temple Team reviews and issues fix commissions.

| # | Thread | Commission ID | Gap Description | Files Affected | Integrated to Live App | Priority | Action Required | Assigned To | Resolved |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Remedies | REM-P1 | Verdict split is 10/8/8/10 (YES/WAIT/NO/PRAY) -- spec was 9/9/9/9. Intentional or re-seed? | MongoDB `remedies` collection | `N/A` | 🔶 Medium | Temple Team to confirm intent | Temple Team | ⬜ |
| 2 | Punya Rewards | PUN-OP-1 | `individual_report` action code is missing from `backend/punya_rewards_service.py` `DEFAULT_ACTION_RULES`, so Punya points are not awarded for Individual Reports and the frontend intentionally leaves that trigger unwired. | `backend/punya_rewards_service.py`, `frontend/src/pages/reports/IndividualReportsPage.jsx` | Partial | 🔶 Medium | Temple Team to define the canonical backend action code or confirm the correct existing code before wiring the frontend trigger. | Temple Team + Claude Code | ⬜ |
| 3 | Notification Engine | UNLISTED-NOTIF-04 / UNLISTED-NOTIF-05 | WhatsApp and push channels are only partially integrated in production: WhatsApp still needs BSP/credential activation, and push still needs VAPID env vars plus Temple-owned frontend service-worker / subscription flow before real delivery can go live. | `backend/notification_whatsapp_service.py`, `backend/notification_push_service.py`, `backend/notification_push_router.py`, Temple frontend push/service-worker layer | Partial | 🔶 Medium | Temple Team to complete BSP/VAPID/frontend activation and then rerun channel-level smoke tests. | Temple Team | ⬜ |
| 3 | Kundali | KUN-OP-4 | Live smoke test of `/kundali` in production not completed | `frontend/src/pages/KundaliPage.jsx` | Unknown | 🔵 Low | Temple Team verify | Temple Team | ⬜ |
| 4 | Longevity | LON-OP-1 | Authenticated save/history/detail flow is not fully signed off in this audit; route presence is confirmed, but the full persisted report journey was not completed and `/api/longevity/report/[id]` returned `Longevity report not found` for the tested fake ID. | `backend/longevity_router.py`, `frontend/src/pages/reports/LongevityReportPage.jsx`, `frontend/src/App.js` | Partial | 🔶 Medium | Retest with a persisted full-report ID and complete the production save/history/detail walkthrough | Temple Team | ⬜ |
| 15 | Longevity | LON-OP-2 | Live preview generation on `/api/longevity/generate` succeeded but took about 46 seconds, which misses the module target of under 10 seconds total and indicates production performance drift. | `backend/kp_engine.py`, `backend/longevity_router.py` | Yes | 🟠 High | Profile live generation path, especially AI and DB timing, and bring production response time back within contract target. | Temple Team + Claude Code | ⬜ |
| 5 | Individual Reports | IR-OP-12 | `/reports` 11-tile page and representative backend routes are live, but full premium generate/history journey was not smoke-tested with an entitled account in this audit. | `backend/*_router.py`, `frontend/src/pages/reports/IndividualReportsPage.jsx` | Partial | 🔵 Low | Entitled-account smoke test for `/reports` generate + history | Temple Team | ⬜ |
| 7 | Angel Numbers | ANGEL-2 | Live API still serves pre-rewrite angel content from stored Mongo documents, so the ANGEL-2 quality fix is present in repo but not effective in production. Universal closing sentence and generic intent action steps still appear in `/api/seo/angel-numbers/111/love`. | `backend/angel_numbers_data.py`, `backend/angel_numbers_router.py`, `backend/scripts/seed_angel_numbers_core.py`, `backend/scripts/seed_angel_numbers_intents.py`, MongoDB `angel_number_core`, `angel_number_intents` | Partial | 🟠 High | Re-seed live Angel Numbers collections with ANGEL-2 output or change runtime precedence so stale stored documents do not override the updated generator. | Temple Team + Claude Code | ⬜ |
| 6 | ECHO//PACE | ECHO-1 | Frontend admin tab is in repo but not in the deployed frontend bundle; `/admin/dashboard` loads, but production JS does not contain `echo-pace` / `EchoPace` strings. | `frontend/src/components/admin/EchoPaceTab.jsx`, `frontend/src/pages/admin/AdminDashboard.jsx` | Partial | 🟠 High | Deploy the frontend admin dashboard changes so the ECHO//PACE tab is reachable in production. | Temple Team | ⬜ |
| 10 | Punya Rewards | PUN-QA-1 | Live authenticated smoke coverage for `/punya-rewards` ledger/spin flows and the `/admin/dashboard` Punya Rewards tab was not completed in this audit. | `frontend/src/pages/rewards/PunyaRewardsPage.jsx`, `frontend/src/pages/admin/PunyaRewardsAdminPanel.jsx`, `frontend/src/pages/admin/AdminDashboard.jsx` | Partial | 🔵 Low | Temple Team verify with logged-in user and admin sessions | Temple Team | ⬜ |
| 8 | Live TV | UNLISTED-LTV-02 | Fixed player scope drift: repo mounts `LiveTVPanel` on `/home` and Panchang surfaces in addition to `Landing.jsx`, which violates the locked "Home page only (/)" requirement. | `frontend/src/pages/home/Landing.jsx`, `frontend/src/pages/home/Home.jsx`, `frontend/src/pages/panchang/PanchangLandingPage.jsx`, `frontend/src/pages/panchang/PanchangPage.jsx` | Partial | 🟠 High | Remove non-home mounts and rerun browser QA on `/`, `/home`, and Panchang routes. | Temple Team | ⬜ |
| 9 | Live TV | UNLISTED-LTV-03 | Production `/api/live-tv/active` emits `http://everydayhoroscope-api.onrender.com/...` media URLs; direct consumption from the `https://` site would be mixed-content blocked without the frontend static-asset override. | `backend/live_tv_service.py`, `frontend/src/hooks/useLiveTv.js` | Partial | 🟠 High | Make backend media URLs HTTPS-safe or relative/proxy-safe so playback no longer depends on frontend override to static assets. | Temple Team | ⬜ |
| 15 | Individual Reports | IR-5 | 12 Areas enhancement endpoint is live, but full UI panel flow was not smoke-tested with saved report data. | `backend/ir_enhancement_router.py`, `frontend/src/components/reports/DonutChart.jsx`, `frontend/src/components/reports/TenYearTimeline.jsx`, `frontend/src/pages/reports/IndividualReportsPage.jsx`, `frontend/src/pages/reports/LoveReportsPage.jsx` | Partial | 🔶 Medium | Smoke test enhanced-analysis panel with real saved report payload | Temple Team | ⬜ |
| 16 | Palmistry | UNLISTED-PALM-3 | Frontend copy says palmistry combines hand analysis with Vedic birth data, but the current palmistry analyse flow does not collect or send birth data. | `frontend/src/pages/palmistry/PalmistryPage.jsx`, `backend/palmistry_router.py` | Yes | 🔶 Medium | Align frontend copy to actual runtime or add supported birth-data enrichment. | Temple Team | ⬜ |
| 17 | Self-Healing Center | SHC-UI-1 | Self-Heal admin frontend is present in repo but absent from the deployed frontend bundle; `/admin/dashboard` loads `200`, but production JS does not contain `Self-Heal`, `Lifecycle Ledger`, `GST Ledger`, or `Dispute Flagged` strings. | `frontend/src/components/admin/DiagnosticsTab.jsx`, `frontend/src/pages/admin/AdminDashboard.jsx` | Partial | 🟠 High | Deploy the frontend admin dashboard changes so the Self-Heal diagnostics, lifecycle ledger, and GST/Gmail panels are reachable in production. | Temple Team | ⬜ |
| 18 | Self-Healing Center | SHC-OPS-1 | Gmail/GST scheduler activation is still blocked until `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`, `SUPPORT_EMAIL`, and `BUSINESS_STATE` are configured on Render and the Gmail OAuth flow is completed. | Render env, `backend/server.py`, `backend/services/gmail_ingest.py` | Partial | 🟠 High | Configure the five Render env vars, run `/api/admin/gmail/auth-url`, and verify the stored refresh token so Gmail/GST jobs can execute live. | Temple Team | ⬜ |
| 19 | Self-Healing Center | SHC-OPS-2 | Live Render runtime import of `pdfplumber` was not directly confirmed during this unauthenticated audit, so GST PDF parsing remains unverified in production. | `backend/requirements.txt`, Render runtime | Unknown | 🔶 Medium | Temple Team to confirm `pdfplumber` is installed in the current Render runtime and that GST PDF parsing can import cleanly. | Temple Team | ⬜ |
| 20 | Strategist | STR-SEO-1 | Public Strategist routes are deployed and `/the-strategist` is correctly present in `sitemap.xml`, but raw HTML fetches for `/strategist` and `/the-strategist` still return generic root metadata/canonical `/` instead of route-specific Strategist SEO. | `frontend/src/App.js`, `frontend/public/sitemap.xml`, public SEO rendering path for Strategist routes | Partial | 🟠 High | Temple Team / SEO thread to confirm whether route-level SEO is exposed only after hydration; if not, issue a fix commission for prerender or route-specific HTML meta delivery. | Temple Team + SEO Thread | ⬜ |
| 24 | Lumina | LUM-OP-1 | Live Lumina frontend is deployed, but the production UX has drifted from the original Phase 1 contract into an expanded 9-tab gold/premium-gated variant. | `frontend/src/pages/lumina/LuminaPage.jsx`, `frontend/src/App.js`, `frontend/src/components/NavBar.jsx`, `frontend/src/pages/home/Home.jsx` | Partial | 🔶 Medium | Temple Team to confirm the current frontend as accepted v2 scope or issue a reconciliation commission back toward the original Lumina contract. | Temple Team | ⬜ |
| 25 | Lumina | LUM-OP-2 | Live prayers/manifestation read endpoints are working, but production write-path smoke coverage for prayer create/strengthen/realize and manifestation day completion was not completed in this audit. | `backend/lumina_router.py`, `frontend/src/pages/lumina/LuminaPage.jsx` | Partial | 🔶 Medium | Run a controlled production smoke with a dedicated audit account and verify persisted prayer + manifestation writes end to end. | Temple Team | ⬜ |
| 22 | Numerology | UNLISTED-NUM-02 | Integrated `NumerologyPage` report flow uses a generic Brihat-Kundali `ContinueJourney` CTA instead of the approved tile-aware CTA map, creating UX drift from the delivered journey design. | `frontend/src/pages/numerology/NumerologyPage.jsx`, `frontend/src/components/ContinueJourney.jsx` | Yes | 🔶 Medium | Decide whether Temple accepts the current single-page UX as canonical or wants CTA parity restored with the standalone report design. | Temple Team + Codex | ⬜ |
| 23 | Numerology | UNLISTED-NUM-04 | Live Numerology backend/router omits some richer structured fields from the Codex delivery contract (`remedy_card`, `supportive_gems`, `supportive_metals`, and `karmic_debt_loshu` remediation payload parity), which reduces structured frontend richness. | `backend/numerology_router.py`, `frontend/src/pages/numerology/NumerologyReportPage.jsx`, `frontend/src/components/LuckyElementsTable.jsx` | Partial | 🔶 Medium | Decide whether Temple wants parity restored with the richer structured Numerology payload contract. | Temple Team + Codex | ⬜ |
| 26 | Knowledge Engine | KE-QA-1 | Tracker-listed KE runtime URLs are stale: there is no live public `/api/knowledge-engine/scan` or `/api/knowledge-engine/evaluate-yoga` endpoint. Production access is through `/api/knowledge/generate-narrative` and downstream consumers such as Brihat Kundli and Arc Angel. | `backend/server.py`, `backend/ke_yoga_evaluator.py`, `Codex_Deliveries/CODEX_QA_INTEGRATION_AUDIT_2026-05-27.md` | Partial | 🔶 Medium | Temple Team to confirm whether standalone public KE scan/evaluator endpoints should exist; otherwise update QA/commission trackers to the actual live routes. | Temple Team + Codex | ⬜ |
| 27 | Knowledge Engine | KE-QA-2 | KE-IQ frontend shell is live, but the authenticated questionnaire submit/profile/persistence path was not fully signed off in this audit. `/questionnaire` returns `200`, while unauthenticated `/api/knowledge-engine/questionnaire/profile` returns `401` and empty `/submit` returns `422`, so real-session verification is still needed. | `backend/knowledge_router.py`, `backend/server.py`, `frontend/src/pages/account/QuestionnairePage.jsx`, `frontend/src/components/QuestionnaireWidget.jsx`, `frontend/src/components/ArcAngelPanel.jsx` | Partial | 🔶 Medium | Temple Team to verify the authenticated questionnaire journey, `user_questionnaire_profiles` writes, and Arc Angel β/γ enrichment with a real user session. | Temple Team | ⬜ |
| _(threads add rows here)_ | | | | | | | | | |

---

## AUDIT COMPLETION STATUS

| # | Thread | Section | Audit Submitted | Date | Overall Status |
|---|---|---|---|---|---|
| 1 | Knowledge Engine | 1 | ✅ | 2026-05-27 | PARTIAL -- core KE runtime is deployed, but tracker URL drift and authenticated/admin flow verification remain open |
| 2 | KP Oracle | 2 | ⬜ | | |
| 3 | Arc Angel | 3 | ⬜ | | |
| 4 | Individual Reports | 4 | ✅ | 2026-05-27 | Partial -- deployed, public/API route checks passed; entitled premium flows need final smoke |
| 5 | Strategist | 5 | ✅ | 2026-05-27 | Integrated with 1 High gap |
| 6 | Tarot | 6 | ⬜ | | |
| 7 | Kundali | 7 | ⬜ | | |
| 8 | Lal Kitab | 8 | ⬜ | | |
| 9 | Longevity | 9 | ✅ | 2026-05-27 | Partial -- live page and preview generation verified; latency high; authenticated save/detail still open |
| 10 | SEO Legacy | 10 | ⬜ | | |
| 11 | Remedies | 11 | ⬜ | | |
| 12 | Punya Rewards | 12 | ☑ | 2026-05-27 | PARTIAL -- backend and public Punya surfaces live; auth smoke coverage incomplete; `individual_report` mapping missing |
| 13 | Lo Shu Grid | 13 | ⬜ | | |
| 14 | Love Module | 14 | ⬜ | | |
| 15 | Panchang | 15 | ⬜ | | |
| 17 | Angel Numbers | 17 | ☑ | 2026-05-27 | PARTIAL |
| 16 | ECHO//PACE | 16 | ✅ | 2026-05-27 | PARTIAL -- backend live, frontend admin tab not deployed |
| 17 | Live TV | 17 | ✅ | 2026-05-27 | PARTIAL -- public page and static playback assets live; panel scope drift and backend media URL contract need cleanup |
| 18 | Palmistry | 18 | ✅ | 2026-05-27 | LIVE WITH ONE CONTENT-INTEGRITY GAP |
| 19 | Self-Healing Center | 19 | ✅ | 2026-05-27 | PARTIAL -- backend routes live, frontend admin bundle missing, Gmail/GST activation pending |
| 20 | Numerology | 20 | ✅ | 2026-05-27 | PARTIAL -- core routes live; medium UX/payload drift remains; authenticated premium report smoke incomplete |
| 20 | Lumina | 20 | ✅ | 2026-05-27 | PARTIAL -- backend AI/read routes live; write-path smoke pending; frontend live with Temple-side spec drift |
