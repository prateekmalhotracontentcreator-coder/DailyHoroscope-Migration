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
| KE-Sprint2 | Arbitration Runtime -- `_contradiction_score`, `_representation_mode`, `_build_tension_block`, supersession lookup | `backend/knowledge_engine.py` | | | `/api/knowledge-engine/scan` | | | | |
| KE-2A | Yoga Check Evaluation Engine -- 16 evaluator types, 26 dispatch entries, 52 tests | `backend/ke_yoga_evaluator.py` | | | `/api/knowledge-engine/evaluate-yoga` | | | | |
| KE-IQ | Questionnaire UI + β/γ KE wiring, 75 tests green | `backend/knowledge_router.py`, `frontend/src/pages/QuestionnairePage.jsx`, `frontend/src/components/ArcAngelPanel.jsx` | | | `/questionnaire` | | | | |
| KE-Ingest | Batch Book Ingest Automation v2 | `backend/scripts/` ingest scripts | | | `N/A` | | | | |
| KE-Val | Automated Rule Validation Engine | Rule validation pipeline files | | | `N/A` | | | | |
| KE-2B2 | Varga Dignity Wiring -- facts layer | `backend/knowledge_engine.py` (lines ~195-208, 312, 488-508) | | | `N/A` | | | | |
| KE-2D | Varga Dignity Tier Evaluator, 37 tests green | `backend/ke_yoga_evaluator.py` (lines ~373-387, 631) | | | `N/A` | | | | |
| KE-Item5 | Library Console | _(confirm files)_ | | | `/knowledge-engine/library` | | | | |
| KE-Item6 | Brihat Kundali × KE Route | _(confirm files)_ | | | `/brihat-kundali` | | | | |
| KE-Item7 | Simplified Tranche Filter | _(confirm files)_ | | | `N/A` | | | | |
| KE-Item8 | Tranche Filter UI Feedback | _(confirm files)_ | | | `N/A` | | | | |
| _(add rows)_ | | | | | | | | | |

**KE Thread -- Audit Summary**
- Overall Status: _(fill in)_
- Total Rows Audited: ___
- Gaps Found: ___
- Signed off by KE Thread: _(date)_

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

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| STR-1 | Strategist Premium Landing Page | `frontend/src/pages/strategist/TheStrategistLandingPage.jsx` | | | `/strategist` | | | | |
| STR-1 | War Room Visual Rebuild | `frontend/src/pages/strategist/StrategistPage.jsx` | | | `/strategist/war-room` | | | | |
| STR-1 | App.js route wiring + sitemap entries | `frontend/src/App.js`, `frontend/public/sitemap.xml` | | | `/strategist`, `/strategist/war-room` | | | | |
| STR-2J | Missions UI -- MissionCard responsive + dasha display | `frontend/src/components/strategist/war-room/StrategistWarRoom.jsx`, MissionCard component | | | `/strategist/war-room` (missions panel) | | | | |
| STR (backend) | Dashboard + Missions API endpoints | `backend/server.py` `/api/strategist/dashboard`, `/api/strategist/missions` | | | `/api/strategist/dashboard` | | | | |
| _(add rows)_ | | | | | | | | | |

**Strategist Thread -- Audit Summary**
- Overall Status: _(fill in)_
- Total Rows Audited: ___
- Gaps Found: ___
- Signed off by STR Thread: _(date)_

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

**Tarot Thread -- Audit Summary**
- Overall Status: ✅ Integrated / no confirmed Tarot gaps in this audit
- Total Rows Audited: 9
- Gaps Found: 0 confirmed
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
| SEO-B1 | 36 Per-Sign Horoscope Pages (tomorrow / weekly / monthly) | `frontend/src/pages/horoscope/` per-sign route files | | | `/horoscope/aries/today` (sample) | | | | |
| SEO-B2 | Festival Pages -- Holi, Diwali, Karwa Chauth | Festival page components | | | `/festival/holi` (sample) | | | | |
| SEO-B3 | Festival Hub + Indian Calendar + Hora Today | Hub + calendar + hora pages | | | `/festivals`, `/hora-today` | | | | |
| SEO-C1 | Legal Pages noindex + Policy Seed | Legal pages with noindex meta | | | `/privacy`, `/terms` | | | | |
| SEO-C2 | Rashi Calculator + Nakshatra Calculator | Calculator page components | | | `/rashi-calculator`, `/nakshatra-calculator` | | | | |
| SEO-C3 | Name Compatibility | Name compatibility page | | | `/compatibility/name` | | | | |
| SEO-C4 | Ekadashi / Amavasya / Purnima Hubs | Hub pages | | | `/ekadashi`, `/amavasya`, `/purnima` | | | | |
| SEO-C5 | Marriage Muhurat Page | Muhurat page | | | `/marriage-muhurat` | | | | |
| SEO-C6 | Report Category Discovery Pages | Category pages (launch gated) | | | `/reports/[category]` | | | | |
| SEO-C7 | Celebrity Horoscope Hub | Celebrity hub | | | `/celebrity-horoscope` | | | | |
| SEO-C8 | Love Calculator | Love calculator page | | | `/love-calculator` | | | | |
| SEO-C9 | Angel Numbers Hub -- 14 pages | 14 hub pages | | | `/angel-numbers` | | | | |
| SEO-20K M1 | Festival SEO Pages -- TF-IDF pass | Festival SEO page components | | | `/festival/[slug]` (sample) | | | | |
| SEO-20K M2 | TF-IDF compliance + sitemap additions | Sitemap XML entries | | | `sitemap.xml` | | | | |
| SEO-20K M3 | 30/30 TF-IDF PASS | M3 SEO page components | | | `/festival/[slug]` (M3 pages) | | | | |
| SEO-20K M4 | TAR-SEO (199 Tarot SEO pages) | Tarot SEO pages | `N/A` | `N/A` | `N/A` | `N/A` | On hold -- TT sorting internally | | |
| _(add rows)_ | | | | | | | | | |

**SEO Thread -- Audit Summary**
- Overall Status: _(fill in)_
- Total Rows Audited: ___
- Gaps Found: ___
- Signed off by SEO Thread: _(date)_

---

## SECTION 11 -- Remedies Thread

> Review all Remedies commissions AND any additional work done that is not listed. Add rows as needed.

| Commission ID | Feature / Description | Key Files Delivered | Files Present in Repo | Integrated to Live App | Live URL | URL Working | Gap Description | Priority | Thread Notes |
|---|---|---|---|---|---|---|---|---|---|
| REM-P1 | `/ref/` Remedy Reference Endpoint | `backend/server.py` ~line 851 | | | `/api/remedies/ref/` | | | | |
| REM-P1 | 36 KP Remedy Records seeded in MongoDB | MongoDB `remedies` collection | `N/A` | `N/A` | `N/A` | `N/A` | DB-only | | |
| REM-P1 | KP Fallback Wiring in remedy lookup | KP fallback logic in remedy router | | | `/api/kp/verdict` (remedy in response) | | | | |
| ⚠️ OPEN | Verdict split is 10/8/8/10 (YES/WAIT/NO/PRAY) -- spec was 9/9/9/9. Confirm intentional or re-seed. | DB audit | `N/A` | `N/A` | `N/A` | `N/A` | Confirm split | 🔶 Medium | |
| _(add rows)_ | | | | | | | | | |

**Remedies Thread -- Audit Summary**
- Overall Status: _(fill in)_
- Total Rows Audited: ___
- Gaps Found: ___
- Signed off by REM Thread: _(date)_

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

## MASTER GAP REGISTER

> All threads add their gaps here. Temple Team reviews and issues fix commissions.

| # | Thread | Commission ID | Gap Description | Files Affected | Integrated to Live App | Priority | Action Required | Assigned To | Resolved |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Remedies | REM-P1 | Verdict split is 10/8/8/10 (YES/WAIT/NO/PRAY) -- spec was 9/9/9/9. Intentional or re-seed? | MongoDB `remedies` collection | `N/A` | 🔶 Medium | Temple Team to confirm intent | Temple Team | ⬜ |
| 2 | Punya Rewards | PUN-OP-1 | `individual_report` action code is missing from `backend/punya_rewards_service.py` `DEFAULT_ACTION_RULES`, so Punya points are not awarded for Individual Reports and the frontend intentionally leaves that trigger unwired. | `backend/punya_rewards_service.py`, `frontend/src/pages/reports/IndividualReportsPage.jsx` | Partial | 🔶 Medium | Temple Team to define the canonical backend action code or confirm the correct existing code before wiring the frontend trigger. | Temple Team + Claude Code | ⬜ |
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
| _(threads add rows here)_ | | | | | | | | | |

---

## AUDIT COMPLETION STATUS

| # | Thread | Section | Audit Submitted | Date | Overall Status |
|---|---|---|---|---|---|
| 1 | Knowledge Engine | 1 | ⬜ | | |
| 2 | KP Oracle | 2 | ⬜ | | |
| 3 | Arc Angel | 3 | ⬜ | | |
| 4 | Individual Reports | 4 | ✅ | 2026-05-27 | Partial -- deployed, public/API route checks passed; entitled premium flows need final smoke |
| 5 | Strategist | 5 | ⬜ | | |
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
