# EverydayHoroscope -- Master Codex Commission Table
> Single source of truth for all commissions ever issued, in progress, or pending.
> Use the **Commission ID** when opening or referencing a Codex thread.
> Last updated: 2026-05-16

---

## Status Key

| Symbol | Meaning |
|---|---|
| ✅ INTEGRATED | Code live in `main`. Commission closed. |
| 🔵 IN PROGRESS | Issued to Codex. Awaiting delivery. |
| 🟣 READY TO ISSUE | Brief complete. Open Codex thread and share brief file. |
| 🟡 BLOCKED | Has an unresolved dependency -- do not issue yet. |
| ⏸ PARKING LOT | Phase 2/3 -- brief not written. Hold. |

---

## MODULE 1 -- Knowledge Engine

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| KE-Ingest | Batch Book Ingest Automation v2 | ✅ INTEGRATED | `Knowledge_Engine/CODEX_COMMISSION_KE_BATCH_INGEST.md` | Integrated |
| KE-Val | Automated Rule Validation Engine | ✅ INTEGRATED | `Knowledge_Engine/CODEX_COMMISSION_KE_VALIDATION_ENGINE.md` | Integrated |
| KE-Item5 | Library Console (CPath-1 Item 5) | ✅ INTEGRATED | archived | Integrated |
| KE-Item6 | Brihat Kundali × KE Route (CPath-1 Item 6) | ✅ INTEGRATED | archived | Integrated |
| KE-Item7 | Simplified Tranche Filter (CPath-1 Item 7) | ✅ INTEGRATED | archived | Integrated |
| KE-Item8 | Tranche Filter UI Feedback (CPath-1 Item 8) | ✅ INTEGRATED | archived | Integrated |
| KE-2B2 | Varga Dignity Wiring (facts layer) | ✅ INTEGRATED | `knowledge_engine.py` lines 195-208, 312, 488-508 | Built internally |
| KE-2D | Varga Dignity Tier Evaluator | ✅ INTEGRATED | `ke_yoga_evaluator.py` | 37 tests green |
| **KE-Sprint2** | KE Arbitration Runtime (G-03/G-05/G-06/G-04) | 🔵 IN PROGRESS | `Knowledge_Engine/CODEX_COMMISSION_KE_SPRINT2_ARBITRATION.md` | Issued 2026-05-15. INGEST FREEZE active until gate passes. |
| **KE-2A** | Yoga Check Evaluation Engine (16 evaluator types) | 🔵 IN PROGRESS | `Knowledge_Engine/CODEX_COMMISSION_KE_2A_YOGA_CHECK.md` | Issued 2026-05-15. `ke_yoga_evaluator.py` scaffold + `varga_dignity_tier` live. |
| **KE-IQ** | Questionnaire UI + β/γ KE Wiring | 🟡 BLOCKED | `Knowledge_Engine/CODEX_COMMISSION_KE_IQ_QUESTIONNAIRE_UI.md` | Issue after KE Sprint 2 gate passes. QuestionnaireWidget.jsx (1101 lines) exists. |

---

## MODULE 2 -- KP Oracle

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **KP-2A** | Bundle Editorial + Share Card + Remedies Admin Frontend | ✅ INTEGRATED | `KP/CODEX_COMMISSION_KP_2A.md` | Commit `7d42880`. TT live verification KP-OP-9 pending. |
| **KP-Sprint2** | /ask-question LLM Logic Router (Guna + Gita) | 🔵 IN PROGRESS | `KP/CODEX_COMMISSION_KP_SPRINT2_ASK_QUESTION.md` | Issued 2026-05-15. |
| **KP-2B** | Ritual Animation + 3-Pillar UX + Astro-Filter | 🟡 BLOCKED | `KP/CODEX_COMMISSION_KP_2B.md` | Issue after TT verifies KP-OP-9 items 2+3. |

---

## MODULE 3 -- Individual Reports (Phase 1 -- Natal Reports)

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **IR-1** | 5 Public SEO Landing Pages + `/individual-reports` hub | ✅ INTEGRATED | `Individual_Reports/CODEX_COMMISSION_IR_1_LANDING_PAGES.md` | Commit `825a294`. All 5 natal report landing pages live. |
| **IR-2** | Lunar Cycle Wellness Backend (`lunar_cycle_router.py`) | 🟣 READY TO ISSUE | `Individual_Reports/CODEX_COMMISSION_IR_2_LUNAR_CYCLE.md` | Only missing Phase 2 backend. 2 files + 2-line server.py + 1 LoveReportsPage entry. |
| **IR-3** | 8 Love Report Public SEO Landing Pages | 🟣 READY TO ISSUE | `Individual_Reports/CODEX_COMMISSION_IR_3_LOVE_LANDING_PAGES.md` | Frontend-only. 8 landing pages for Love Bundle reports. No backend dependency. |

> **CC Direct Fix (not Codex):** Phase 1 reports now added to NavBar Reports dropdown → `/individual-reports` (commit pending this session).

---

## MODULE 4 -- Love Module (Phase 2+3 -- Love Question Reports + Ritual Engine)

### Love Question Reports (at `/love-reports` → `LoveReportsPage.jsx`)

| Commission ID | Commission Name | Status | Report Type | Notes |
|---|---|---|---|---|
| LOVE-1 | Love Module Backend | ✅ INTEGRATED | All 8 backends | `Love_Module/CODEX_COMMISSION_LOVE_ENGAGEMENT_MODULE.md` |
| LOVE-FE | Love Module Frontend (LovePage hub + LoveReportsPage) | ✅ INTEGRATED | Hub + report generator | `Love_Module/CODEX_COMMISSION_LOVE_MODULE_FRONTEND.md` |

**8 Love Question Reports -- all live in `LoveReportsPage.jsx`:**

| Report | Type Key | Backend Router | Frontend | Status |
|---|---|---|---|---|
| Love Weather | `love_weather` | `love_weather_router.py` ✅ | `LoveReportsPage.jsx` ✅ | ✅ LIVE |
| Encounter Window | `encounter_window` | `encounter_window_router.py` ✅ | `LoveReportsPage.jsx` ✅ | ✅ LIVE |
| Date Night Planner | `date_night_score` | `date_night_router.py` ✅ | `LoveReportsPage.jsx` ✅ | ✅ LIVE |
| Digital Dating Edge | `digital_dating_strategy` | `digital_dating_router.py` ✅ | `LoveReportsPage.jsx` ✅ | ✅ LIVE |
| Intimacy & Vitality | `intimacy_vitality_forecast` | `intimacy_vitality_router.py` ✅ | `LoveReportsPage.jsx` ✅ | ✅ LIVE |
| Venus Retrograde | `venus_retrograde_personal_impact` | `venus_retrograde_router.py` ✅ | `LoveReportsPage.jsx` ✅ | ✅ LIVE |
| Soulmate Timing | `soulmate_timing` | `soulmate_timing_router.py` ✅ | `LoveReportsPage.jsx` ✅ | ✅ LIVE |
| Soul Connection | `deep_synastry_soul_connection` | `soul_connection_router.py` ✅ | `LoveReportsPage.jsx` ✅ | ✅ LIVE |

### Ritual Engine (at `/ritual-engine` → `RitualEnginePage.jsx`)

| Report | Trigger Type | Backend | Frontend | Status |
|---|---|---|---|---|
| First Date Magnet | `first_date_magnet` | `ritual_trigger_router.py` ✅ | `RitualEnginePage.jsx` ✅ | ✅ LIVE |
| Steamy Encounter | `steamy_encounter` | `ritual_trigger_router.py` ✅ | `RitualEnginePage.jsx` ✅ | ✅ LIVE |
| Ex-Recovery Window | `ex_recovery` | `ritual_trigger_router.py` ✅ | `RitualEnginePage.jsx` ✅ | ✅ LIVE |
| Long Term Love Portal | `long_term_love` | `ritual_trigger_router.py` ✅ | `RitualEnginePage.jsx` ✅ | ✅ LIVE |
| Love Battery Score | `lunar_daily_score` | `ritual_trigger_router.py` ✅ | `RitualEnginePage.jsx` ✅ | ✅ LIVE |

> **Love Module verdict: ✅ Fully integrated -- nothing pending for Codex.**
> NavBar → Reports → Love Bundle → `/love` (hub) → links to `/love-reports` + `/ritual-engine`.

---

## MODULE 5 -- Remedies Engine

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **REM-P1** | Remedies Engine Phase 1 (KP collection + remedy_ref pipeline) | 🟣 READY TO ISSUE | `Remedies/CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md` | `/api/remedies/ref/{remedy_ref_id}` confirmed live. All blockers cleared. |

---

## MODULE 6 -- The Strategist

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **STR-1** | Strategist Premium Landing Page + War Room Visual Rebuild | ✅ INTEGRATED | `Strategist/CODEX_COMMISSION_STRATEGIST_LANDING_WARROOM.md` | Commit `ba58192`. |
| **STR-2J** | Strategist Missions UI (MissionCard responsive + dasha display) | ✅ INTEGRATED | `Strategist/CODEX_COMMISSION_STR_2J_MISSIONS_UI.md` | Commit `9ad2e0a`. Dasha backend fix applied by CC. |

---

## MODULE 7 -- Arc Angel

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **ARC-UI** | Arc Angel UI Panel (ArcAngelPanel.jsx) | ✅ INTEGRATED | `Arc_Angel/CODEX_COMMISSION_ARC_ANGEL_UI_PANEL.md` (archived) | Commit `c01ec8d`. |
| **ARC-2** | Arc Angel Phase 2 -- Confidence % lift + Questionnaire gating + Desktop sidebar | 🟡 BLOCKED | `Arc_Angel/CODEX_COMMISSION_ARC_2_CONFIDENCE_QUESTIONNAIRE.md` | Issue after KE Sprint 2 gate passes. |

---

## MODULE 8 -- Tarot

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **TAR-v4** | Tarot UI v4 Enhancement | 🟣 READY TO ISSUE | `Tarot/CODEX_COMMISSION_TAROT_V4_UI.md` | Existing Tarot UI visual uplift. No backend dependency. |

---

## MODULE 9 -- Kundali / Birth Chart

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **KUN-1** | Lagna Kundali Frontend Module | 🟣 READY TO ISSUE | `Kundali/CODEX_COMMISSION_KUNDALI_LAGNA_CONTRACT.md` | **Re-scoped 2026-05-16: backend fully live at `/api/lagna-kundali`. Frontend only: `KundaliPage.jsx` + SVG chart + planet table + dasha timeline.** |

---

## MODULE 10 -- Lal Kitab

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **LK-1** | Lal Kitab Standalone Module (onboard, remedies, debt audit, tracker) | 🟣 READY TO ISSUE | `LK/CODEX_COMMISSION_LK_STANDALONE_MODULE.md` | Issue after `jyotish_lk_remedies` batch-approved by TT. |

---

## MODULE 11 -- Longevity

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **LON-1** | Ayur Jyotish Longevity Report | 🟡 BLOCKED | `Longevity/CODEX_COMMISSION_LONGEVITY_REPORT_CONTRACT.md` | Issue after KE Sprint 2 gate passes. Large scope. |

---

## MODULE 12 -- Live TV

| Commission ID | Commission Name | Status | Notes |
|---|---|---|---|
| **LTV-1** | Live TV: Sai Baba Arti | ✅ INTEGRATED | `Live_TV/CODEX_COMMISSION_LIVE_TV_SAI_BABA_ARTI.md`. NavBar entry + PanchangLandingPage + dedicated SEO page all live. |

---

## MODULE 13 -- Punya Rewards

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **PUN-1** | Punya Rewards Gamification Engine | ✅ INTEGRATED | `Punya_Rewards/CODEX_COMMISSION_PUNYA_REWARDS_GAMIFICATION.md` | Backend fully live. |
| **PUN-2** | Punya Rewards Home Promo + Module Hooks + SVG Wheel | 🟣 READY TO ISSUE | `Punya_Rewards/CODEX_COMMISSION_PUN_2_FRONTEND_INTEGRATION.md` | No NavBar entry. User Profile section only. Home promo + 8 module earn hooks + wheel UX. |

---

## MODULE 14 -- Notifications

| Commission ID | Commission Name | Status | Notes |
|---|---|---|---|
| **NOTIF-1** | Notification Engine (web-app wide) | ✅ INTEGRATED | `Notifications/CODEX_COMMISSION_NOTIFICATION_ENGINE.md`. Email ✅, WhatsApp 🔜 (phone pending Meta OTP). |

---

## MODULE 15 -- Panchang

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **PAN-L1** | Panchang Language/Regional Pages (Tamil, Telugu, Malayalam) | 🟣 READY TO ISSUE | `Panchang/CODEX_COMMISSION_PANCHANG_LANGUAGE_PAGES.md` | Issue after high-priority threads running. |

---

## MODULE 16 -- SEO & Web Performance

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **SEO-1** | SEO + Marketing + Web Performance Optimisation | 🟣 READY TO ISSUE | `SEO/CODEX_COMMISSION_SEO_WEBPERF.md` | ⚠️ Issue LAST -- only after all other high-priority threads are running. |

---

## MODULE 17 -- World Oracles (Phase 3)

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **ORACLE-P3** | 5 World Oracle Modules (Bible, Islamic, Taoist, Greek, Sikh) | ⏸ PARKING LOT | `World_Oracles/CODEX_COMMISSION_ORACLE_P3_WORLD_ORACLES.md` | Phase 3 -- do not open thread yet. |

---

## MODULE 18 -- Commission J / WCE

| Commission ID | Commission Name | Status | Notes |
|---|---|---|---|
| **WCE-1** | [TBD] | ⏸ PARKING LOT | Phase 2 -- brief not written. Hold. |

---

## Summary Dashboard

| Priority | Commission ID | Module | Name | Status |
|---|---|---|---|---|
| 🔴 CRITICAL | KE-Sprint2 | Knowledge Engine | KE Arbitration Runtime | 🔵 IN PROGRESS |
| 🔴 CRITICAL | KE-2A | Knowledge Engine | Yoga Check Evaluation Engine | 🔵 IN PROGRESS |
| 🔴 HIGH | KP-Sprint2 | KP Oracle | /ask-question LLM Router | 🔵 IN PROGRESS |
| 🟠 HIGH | REM-P1 | Remedies Engine | Remedies Engine Phase 1 | 🟣 READY TO ISSUE |
| 🟠 HIGH | PUN-2 | Punya Rewards | Home Promo + Module Hooks + Wheel | 🟣 READY TO ISSUE |
| 🟠 HIGH | IR-2 | Individual Reports | Lunar Cycle Wellness Backend | 🟣 READY TO ISSUE |
| 🟠 HIGH | IR-3 | Individual Reports | 8 Love Report SEO Landing Pages | 🟣 READY TO ISSUE |
| 🟡 MED | KP-2B | KP Oracle | Ritual Animation + 3-Pillar UX | 🟡 BLOCKED (KP-OP-9) |
| 🟡 MED | KE-IQ | Knowledge Engine | Questionnaire UI + β/γ Wiring | 🟡 BLOCKED (KE Sprint 2) |
| 🟡 MED | TAR-v4 | Tarot | Tarot UI v4 Enhancement | 🟣 READY TO ISSUE |
| 🟡 MED | KUN-1 | Kundali | Lagna Kundali Frontend | 🟣 READY TO ISSUE |
| 🟡 MED | LK-1 | Lal Kitab | LK Standalone Module | 🟣 READY TO ISSUE |
| 🟡 MED | ARC-2 | Arc Angel | Phase 2 Confidence + Questionnaire | 🟡 BLOCKED (KE Sprint 2) |
| 🟢 LOW | LON-1 | Longevity | Ayur Jyotish Longevity Report | 🟡 BLOCKED (KE Sprint 2) |
| 🟢 LOW | PAN-L1 | Panchang | Language/Regional Pages | 🟣 READY TO ISSUE |
| 🟢 LOW | SEO-1 | SEO | SEO + Web Performance | 🟣 READY TO ISSUE (LAST) |
| ⏸ HOLD | ORACLE-P3 | World Oracles | 5 World Oracle Modules | ⏸ PARKING LOT |
| ⏸ HOLD | WCE-1 | Commission J | [TBD] | ⏸ PARKING LOT |

---

## Recommended Issue Order (2026-05-16)

```
NOW ACTIVE (Codex threads open):
  KE-Sprint2   Knowledge Engine Arbitration Runtime
  KE-2A        Yoga Check Evaluation Engine
  KP-Sprint2   KP /ask-question LLM Router

ISSUE THIS WEEK (all briefs complete, no blockers):
  REM-P1       Remedies Engine Phase 1
  PUN-2        Punya Rewards Home Promo + Module Hooks + Wheel
  IR-2         Lunar Cycle Wellness Backend
  IR-3         8 Love Report SEO Landing Pages

ISSUE AFTER KP-OP-9 TT VERIFICATION:
  KP-2B        KP Ritual Animation + 3-Pillar UX

ISSUE AFTER HIGH-PRIORITY THREADS RUNNING:
  TAR-v4       Tarot UI v4
  KUN-1        Lagna Kundali Frontend (backend done)
  LK-1         Lal Kitab Standalone
  PAN-L1       Panchang Language Pages
  SEO-1        SEO + Web Performance (issue LAST)

ISSUE AFTER KE SPRINT 2 GATE PASSES:
  KE-IQ        Questionnaire UI + β/γ Wiring
  ARC-2        Arc Angel Phase 2
  LON-1        Longevity Report

PARKING LOT (Phase 2/3 -- hold):
  ORACLE-P3    5 World Oracle Modules
  WCE-1        Commission J / WCE
```
