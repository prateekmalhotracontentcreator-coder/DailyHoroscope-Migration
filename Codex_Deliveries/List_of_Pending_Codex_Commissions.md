# List of Pending Codex Commissions
> EverydayHoroscope · Temple Team Master Tracker
> Last updated: 2026-05-22 (SEO-20K + IR-5 added; KE-Sprint2, KE-2A, KE-IQ, ARC-2, IR-4 confirmed INTEGRATED)
> **Rule:** Every commission issued to Codex has a row here AND a brief file in `Codex_Deliveries/[Module]/`. This file is the single view of what is blocked, what is ready, and what is integrated.
>
> **Per-module open points, status, and revision history → `TEMPLE_TRACKER.md` (repo root).** Update that file whenever a commission is integrated or a new open point is discovered.

---

## Status Key

| Status | Meaning |
|---|---|
| `READY TO ISSUE` | Brief complete. Open a Codex thread and share the brief file. |
| `IN PROGRESS` | Commission open in Codex. Awaiting delivery. |
| `DELIVERED -- PENDING INTEGRATION` | Codex output received. Claude Code to review + integrate. |
| `INTEGRATED` | Code built, committed to `main`. Commission closed. |

---

## 🔴 CRITICAL -- Issue Immediately (Blocking Other Work)

| ID | Commission | Thread | Brief File | Status | Dependency | Notes |
|---|---|---|---|---|---|---|
| **SEO-20K** | 22,170 Programmatic SEO Pages + Web Performance (Umbrella) | SEO | `SEO/CODEX_COMMISSION_SEO_20K.md` | READY TO ISSUE | None | Merges SEO-1. Deliver in 4 milestones: M1=Panchang city+Choghadiya, M2=Angel Numbers (9K), M3=Tarot+Compat+Remedies, M4=Festivals+Transits+Character. Internal engines only. |
| **IR-5** | 12 Areas of Life Enhancement (Donut Chart + 10-Year Timeline + Graha Drishti + Claude 4-page reports) | Individual Reports | `Individual_Reports/CODEX_COMMISSION_IR_5_12AREAS_ENHANCEMENT.md` | READY TO ISSUE | IR-4 must be integrated first | Vedic-only (Rahu/Ketu replace Uranus/Neptune). Adds 3 new calc functions to vedic_calculator.py + new router + 2 UI components. |

---

| ~~**KE-Sprint2**~~ | ~~KE Arbitration Runtime (G-03/G-05/G-06/G-04)~~ | Knowledge Engine | `Knowledge_Engine/CODEX_COMMISSION_KE_SPRINT2_ARBITRATION.md` | ✅ INTEGRATED -- self-certified 2026-05-17 | -- | All 5 acceptance gates pass. `_contradiction_score`, `_representation_mode`, `_build_tension_block`, supersession lookup, `scan_chart()` payload confirmed. |
| ~~**KE-2A**~~ | ~~Yoga Check Evaluation Engine (16 evaluator types)~~ | Knowledge Engine | `Knowledge_Engine/CODEX_COMMISSION_KE_2A_YOGA_CHECK.md` | ✅ INTEGRATED -- 2026-05-17 | -- | All 9 missing handlers added. 52 tests pass. 26 dispatch entries. CC-verified. |

---

## 🟠 HIGH PRIORITY -- Issue This Week

| ID | Commission | Thread | Brief File | Status | Dependency | Notes |
|---|---|---|---|---|---|---|
| ~~**KP-2A**~~ | ~~KP Bundle Editorial + Share Card + Remedies Admin Frontend~~ | KP Oracle | `KP/CODEX_COMMISSION_KP_2A.md` | ✅ INTEGRATED -- commit `7d42880` | -- | Delivered + integrated 2026-05-15. TT live verification (KP-OP-9) required before issuing KP-2B. |
| **KP-Sprint2** | /ask-question LLM Logic Router (Guna + Gita) | KP Oracle | `KP/CODEX_COMMISSION_KP_SPRINT2_ASK_QUESTION.md` | 🔵 IN PROGRESS | None | Issued 2026-05-15. Independent of KP-2A. |
| ~~**KE-IQ**~~ | ~~Questionnaire UI + β/γ KE Wiring~~ | Knowledge Engine | `Knowledge_Engine/CODEX_COMMISSION_KE_IQ_QUESTIONNAIRE_UI.md` | ✅ INTEGRATED -- commit `f7aa78b` 2026-05-18 | -- | `knowledge_router.py`, `QuestionnaireWidget.jsx`, `QuestionnairePage.jsx`, `ArcAngelPanel.jsx`. 75/75 KE tests green. TT live verification pending (KE-OP-15). |
| ~~**IR-1**~~ | ~~5 Public SEO Landing Pages (Individual Reports)~~ | Individual Reports | `Individual_Reports/CODEX_COMMISSION_IR_1_LANDING_PAGES.md` | ✅ INTEGRATED -- commit `825a294` | None | 5 landing pages + public hub live. Route canonical confirmed by TT 2026-05-15. |
| ~~**IR-2**~~ | ~~Lunar Cycle Wellness Backend~~ | Individual Reports | `Individual_Reports/CODEX_COMMISSION_IR_2_LUNAR_CYCLE.md` | ✅ INTEGRATED -- commit `f9f6690` + `021a799` | -- | Live. Datetime bug fixed. Tile on LovePage. IR-2A rework also integrated `692fefa`. |
| ~~**IR-3**~~ | ~~8 Love Report Public SEO Landing Pages~~ | Individual Reports | `Individual_Reports/CODEX_COMMISSION_IR_3_LOVE_LANDING_PAGES.md` | ✅ INTEGRATED -- commit `739c3fa` | -- | 8 wrappers + 8 routes + 8 sitemap URLs. CTA content-driven. TT live spot-check pending. |
| ~~**ARC-2**~~ | ~~Arc Angel Phase 2 -- Confidence % lift + Questionnaire gating + Desktop sidebar~~ | Arc Angel | `Arc_Angel/CODEX_COMMISSION_ARC_2_CONFIDENCE_QUESTIONNAIRE.md` | ✅ INTEGRATED -- commit `c1a7cb0` 2026-05-18 | -- | 18 files, 746 insertions. 72/72 tests green. 3-pillar confidence live (40% base + P1 24% + P2 12% + P3 10%, cap 86%). ArcAngelPanel rebuilt. Left nav split. PrivateRoute for all signed-up users. |
| ~~**REM-P1**~~ | ~~Remedies Engine Phase 1 (KP collection + remedy_ref pipeline)~~ | Remedies | `Remedies/CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md` | ✅ INTEGRATED -- runtime confirmed 2026-05-16 | -- | All 3 tasks complete: `/ref/` endpoint live (line 851), 36 KP remedy records seeded (modified=36 2026-05-15), KP fallback wiring confirmed. ⚠️ TT content note: JSON verdict split is 10/8/8/10 (YES/WAIT/NO/PRAY) vs spec'd 9/9/9/9 -- confirm intentional or re-ingest. |
| **PUN-2** | Punya Rewards Home Page Promo + Module Hooks + SVG Wheel | Punya Rewards | `Punya_Rewards/CODEX_COMMISSION_PUN_2_FRONTEND_INTEGRATION.md` | READY TO ISSUE | PUN-1 ✅ | Backend fully live. PunyaRewardsPage baseline exists. Home promo section + 8 module hooks + wheel UX upgrade needed. No NavBar entry. |

---

## 🟡 MEDIUM PRIORITY -- Issue After High Priority Threads Start

| ID | Commission | Thread | Brief File | Status | Dependency | Notes |
|---|---|---|---|---|---|---|
| **KP-2B** | Ritual Animation + 3-Pillar UX + Astro-Filter | KP Oracle | `KP/CODEX_COMMISSION_KP_2B.md` | READY TO ISSUE | KP-2A delivered | White Light meditation + 3-pillar Guidance Report + transit/dasha enrichment |
| ~~STR-1~~ | ~~Strategist Premium Landing Page + War Room Visual Rebuild~~ | The Strategist | `Strategist/CODEX_COMMISSION_STRATEGIST_LANDING_WARROOM.md` | ✅ INTEGRATED -- commit `ba58192` | -- | TheStrategistLandingPage.jsx + StrategistPage.jsx + App.js + sitemap.xml all live. Build verified. |
| ~~STR-2J~~ | ~~Strategist Missions UI (MissionCard responsive + dasha display)~~ | The Strategist | `Strategist/CODEX_COMMISSION_STR_2J_MISSIONS_UI.md` | ✅ INTEGRATED -- commit `9ad2e0a` | -- | Delivered by Codex 2026-05-15. Dasha backend fix applied by Claude Code. |
| **TAR-v4** | Tarot UI v4 Enhancement | Tarot | `Tarot/CODEX_COMMISSION_TAROT_V4_UI.md` | READY TO ISSUE | None | Existing Tarot UI visual uplift to v4 standard |
| **KUN-1** | Lagna Kundali Frontend Module | Kundali | `Kundali/CODEX_COMMISSION_KUNDALI_LAGNA_CONTRACT.md` | READY TO ISSUE | None | **Backend already live** at `/api/lagna-kundali` (re-scoped 2026-05-16). Frontend only: `KundaliPage.jsx` + SVG chart + planet table + dasha timeline. |
| **LK-1** | LK Standalone Module (onboard, remedies, debt audit, tracker) | Lal Kitab | `LK/CODEX_COMMISSION_LK_STANDALONE_MODULE.md` | READY TO ISSUE | None | Lal Kitab standalone product |
| **SEO-1** | SEO + Marketing + Web Performance Optimisation | SEO | `SEO/CODEX_COMMISSION_SEO_WEBPERF.md` | READY TO ISSUE | None | ⚠️ Issue LAST -- start only after high-priority Codex threads are running |

---

## 🟢 LOWER PRIORITY -- Phase 2 / Phase 3

| ID | Commission | Thread | Brief File | Status | Phase | Notes |
|---|---|---|---|---|---|---|
| **LON-1** | Ayur Jyotish Longevity Report | Longevity | `Longevity/CODEX_COMMISSION_LONGEVITY_REPORT_CONTRACT.md` | READY TO ISSUE | Phase 2 | Large scope -- build after KE Sprint 2 gate passes |
| **PAN-L1** | Panchang Language/Regional Pages (Tamil, Telugu, Malayalam) | Panchang | `Panchang/CODEX_COMMISSION_PANCHANG_LANGUAGE_PAGES.md` | READY TO ISSUE | Phase 2 | -- |
| **ORACLE-P3** | 5 World Oracle Modules (Bible, Islamic, Taoist, Greek, Sikh) | World Oracles | `World_Oracles/CODEX_COMMISSION_ORACLE_P3_WORLD_ORACLES.md` | READY TO ISSUE | Phase 3 | LOW -- planning document. Same grid mechanic as KP Oracle. |

---

## ✅ INTEGRATED -- Closed Commissions

| ID | Commission | File | Commit |
|---|---|---|---|
| SEO-B1 | 36 Per-Sign Horoscope Pages (tomorrow/weekly/monthly) | `SEO/CODEX_COMMISSION_SEO-B1.md` | `963dc82` |
| SEO-B2 | Festival Pages (Holi, Diwali, Karwa Chauth) | `SEO/CODEX_COMMISSION_SEO-B2.md` | `963dc82` |
| SEO-B3 | Festival Hub + Indian Calendar + Hora Today | `SEO/CODEX_COMMISSION_SEO-B3.md` | `963dc82` |
| SEO-C1 | Legal Pages noindex + Policy Seed (production seeded 2026-05-20) | `SEO/CODEX_COMMISSION_SEO-C1.md` | `963dc82` |
| SEO-C2 | Rashi Calculator + Nakshatra Calculator | `SEO/CODEX_COMMISSION_SEO-C2.md` | `963dc82` |
| SEO-C3 | Name Compatibility (/compatibility/name) | `SEO/CODEX_COMMISSION_SEO-C3.md` | `963dc82` |
| SEO-C4 | Ekadashi / Amavasya / Purnima Hubs | `SEO/CODEX_COMMISSION_SEO-C4.md` | `963dc82` |
| SEO-C5 | Marriage Muhurat Page | `SEO/CODEX_COMMISSION_SEO-C5.md` | `963dc82` |
| SEO-C6 | Report Category Discovery Pages (code live, launch gated -- Razorpay) | `SEO/CODEX_COMMISSION_SEO-C6.md` | `963dc82` |
| SEO-C7 | Celebrity Horoscope Hub | `SEO/CODEX_COMMISSION_SEO-C7.md` | `963dc82` |
| SEO-C8 | Love Calculator | `SEO/CODEX_COMMISSION_SEO-C8.md` | `963dc82` |
| SEO-C9 | Angel Numbers Hub (14 pages) | `SEO/CODEX_COMMISSION_SEO-C9.md` | `963dc82` |
| IR-1 | 5 Public SEO Landing Pages + `/individual-reports` hub | `Individual_Reports/CODEX_COMMISSION_IR_1_LANDING_PAGES.md` | `825a294` |
| IR-2 | Lunar Cycle Wellness Backend | `Individual_Reports/CODEX_COMMISSION_IR_2_LUNAR_CYCLE.md` | `f9f6690` · `021a799` (bug fixes) |
| IR-2A | Lunar Cycle Rework -- Action Tracker + Rich Content | `Individual_Reports/CODEX_COMMISSION_IR_2A_LUNAR_CYCLE_REWORK.md` | `692fefa` · Live-verified by TT 2026-05-16 ✅ |
| IR-3 | 8 Love Report SEO Landing Pages | `Individual_Reports/CODEX_COMMISSION_IR_3_LOVE_LANDING_PAGES.md` | `739c3fa` |
| IR-4 | 6 Phase 3 Natal Reports (Wealth, Romance, Vitality, Partnership, Dharma, Gains) | `Individual_Reports/CODEX_COMMISSION_IR_4_SIX_NEW_REPORTS.md` | `1be1e58` · `/reports` expanded 5→11 tiles · TT live verification pending (IR-OP-12) |
| KP-2A | KP Bundle Editorial + Share Card + Remedies Admin Frontend | `KP/CODEX_COMMISSION_KP_2A.md` | `7d42880` |
| REM-P1 | Remedies Engine Phase 1 (KP collection + remedy_ref pipeline) | `Remedies/CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md` | Runtime confirmed 2026-05-16 -- endpoint line 851, 36 records seeded |
| KE-2B2 | Varga Dignity Wiring (facts layer) | `knowledge_engine.py` lines 195-208, 312, 488-508 | Built internally -- confirmed live 2026-05-15 |
| KE-2D | Varga Dignity Tier Evaluator | `ke_yoga_evaluator.py` lines 373-387, 631 | Built internally -- 37 tests green, migration archived -- confirmed live 2026-05-15 |
| ARC-UI | Arc Angel UI Panel (ArcAngelPanel.jsx) | `Arc_Angel/CODEX_COMMISSION_ARC_ANGEL_UI_PANEL.md` (archived) | `c01ec8d` |
| ARC-2 | Arc Angel Phase 2 -- 3-Pillar Confidence Engine + Decay + Notification hooks | `Arc_Angel/CODEX_COMMISSION_ARC_2_CONFIDENCE_QUESTIONNAIRE.md` | `c1a7cb0` · 72/72 tests green |
| KE-Sprint2 | KE Arbitration Runtime (G-03/G-04/G-05/G-06) | `Knowledge_Engine/CODEX_COMMISSION_KE_SPRINT2_ARBITRATION.md` | Self-certified 2026-05-17 · All 5 gates pass |
| KE-2A | Yoga Check Evaluation Engine (16 evaluator types) | `Knowledge_Engine/CODEX_COMMISSION_KE_2A_YOGA_CHECK.md` | 52 tests green · 26 dispatch entries · 2026-05-17 |
| KE-IQ | Questionnaire UI + β/γ KE Wiring | `Knowledge_Engine/CODEX_COMMISSION_KE_IQ_QUESTIONNAIRE_UI.md` | `f7aa78b` · 75/75 tests green · 2026-05-18 |
| KE-Ingest | Batch Book Ingest Automation v2 | `Knowledge_Engine/CODEX_COMMISSION_KE_BATCH_INGEST.md` | ✅ |
| KE-Val | Automated Rule Validation Engine | `Knowledge_Engine/CODEX_COMMISSION_KE_VALIDATION_ENGINE.md` | ✅ |
| KE-Item5 | Library Console (CPath-1 Item 5) | archived | ✅ |
| KE-Item6 | Brihat Kundali × KE Route (CPath-1 Item 6) | archived | ✅ |
| KE-Item7 | Simplified Tranche Filter (CPath-1 Item 7) | archived | ✅ |
| KE-Item8 | Tranche Filter UI Feedback (CPath-1 Item 8) | archived | ✅ |
| LOVE-1 | Love & Engagement Module Backend | `Love_Module/CODEX_COMMISSION_LOVE_ENGAGEMENT_MODULE.md` | ✅ |
| LOVE-FE | Love Module Frontend + SEO | `Love_Module/CODEX_COMMISSION_LOVE_MODULE_FRONTEND.md` | ✅ |
| LTV-1 | Live TV: Sai Baba Arti | `Live_TV/CODEX_COMMISSION_LIVE_TV_SAI_BABA_ARTI.md` | ✅ |
| PUN-1 | Punya Rewards Gamification Engine | `Punya_Rewards/CODEX_COMMISSION_PUNYA_REWARDS_GAMIFICATION.md` | ✅ |
| NOTIF-1 | Notification Engine (web-app wide) | `Notifications/CODEX_COMMISSION_NOTIFICATION_ENGINE.md` | ✅ |
| KUN-Shadbala | Shadbala Engine (vedic_calculator.py) | archived | ✅ |

---

## Knowledge Engine -- Phase 1.2 Sprint Tracker

| Sprint | Gaps | Status | Gate |
|---|---|---|---|
| Sprint 1 -- Scoring Foundation | G-01 (α/β/γ wiring) | ✅ COMPLETE -- commit `57e347a` | ✅ ALL 6 tests passed |
| Sprint 2 -- Arbitration Runtime | G-03, G-05, G-06, G-04 | ✅ INTEGRATED -- self-certified 2026-05-17 | ✅ All 5 gates pass |
| Sprint 3 -- Arc Angel Computation | G-07, G-08, G-09 | ✅ INTEGRATED -- KE-Sprint3 live 2026-05-17 | ✅ KE-OP-13 cleared |
| Sprint 4 -- Questionnaire β/γ | G-10 | ✅ INTEGRATED -- commit `f7aa78b` 2026-05-18 | ✅ 75/75 tests green · KE-OP-15 TT verification pending |

---

## Recommended Issue Order (updated 2026-05-20 post-reconciliation)

```
INTEGRATED (all complete as of 2026-05-18):
  KE-Sprint2  ✅ -- Arbitration Runtime
  KE-2A       ✅ -- Yoga Check Evaluators
  KE-IQ       ✅ -- Questionnaire β/γ Wiring  (commit f7aa78b · KE-OP-15 TT verify pending)
  ARC-2       ✅ -- Arc Angel 3-Pillar Confidence (commit c1a7cb0 · TT verify pending)
  IR-4        ✅ -- 6 Phase 3 Natal Reports     (commit 1be1e58 · IR-OP-12 TT verify pending)

IN PROGRESS:
  KP-Sprint2  🔵 -- Ask-Question LLM Router (issued 2026-05-15)

ISSUE NOW (no blockers -- priority order):
  1. KUN-1    -- Lagna Kundali Frontend (backend live, frontend only)
  2. KP-2B    -- Ritual Animation + 3-Pillar UX
  3. PUN-2    -- Punya Rewards Home Promo + Module Hooks
  4. TAR-v4   -- Tarot UI v4
  5. PAN-L1   -- Panchang Language Pages
  6. LK-1     -- Lal Kitab Standalone Module
  7. LON-1    -- Longevity Report (large scope -- separate thread)

HOLD / NOT READY:
  SEO-WebPerf -- Issue LAST (all content pages must be live first)
  ORACLE-P3   -- Phase 3 (KP must be live 30+ days)
  KE-TV-1     -- Ch 19 test vectors (TechSpec TT approval needed)
```
