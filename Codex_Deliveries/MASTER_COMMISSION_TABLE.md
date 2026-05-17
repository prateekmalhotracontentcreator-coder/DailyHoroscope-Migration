# EverydayHoroscope -- Master Codex Commission Table
> Single source of truth for all commissions ever issued, in progress, or pending.
> Use the **Commission ID** when opening or referencing a Codex thread.
> Last updated: 2026-05-17 (session 3 -- KE-OP-13 cleared, ARC-2 pre-condition updated)

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
| **KE-Sprint2** | KE Arbitration Runtime (G-03/G-05/G-06/G-04) | ✅ INTEGRATED | `Knowledge_Engine/CODEX_COMMISSION_KE_SPRINT2_ARBITRATION.md` | Self-certified 2026-05-17. All 5 acceptance gates pass: `_contradiction_score`, `_representation_mode`, `_build_tension_block`, supersession lookup, `scan_chart()` payload confirmed. INGEST FREEZE lifted. |
| **KE-2A** | Yoga Check Evaluation Engine (26 evaluator types) | ✅ INTEGRATED | `Knowledge_Engine/CODEX_COMMISSION_KE_2A_YOGA_CHECK.md` | Delivered + CC-verified 2026-05-17. 9 missing handlers added (`yoga`, `planet_affliction`, `house_position`, `planet_afflicted`, `planet_conjunction`, `planet_in_house_from_sun`, `planetary_position`, `planet_combust`, `house_placement`). 52/52 tests pass. 0 missing mappings. 26 total dispatch entries. |
| **KE-Sprint3** | Arc Angel Computation (G-07/G-08/G-09) | ✅ LIVE -- verified 2026-05-17 | `Knowledge_Engine/CODEX_COMMISSION_KE_SPRINT3_ARC_ANGEL.md` | KE-OP-13 CLEARED. Both routes live on Render: `confidence_pct: 40` ✅ · `engine_label` ✅ · `arc-angel-profile/{user_id}` 200 ✅ · MongoDB persistence ✅ · 6h cache ✅. **KE-OP-14 open:** window granularity returns MD-level (1 period/domain) instead of AD-level (3/domain) -- fix in KE Codex thread before ARC-2 finalises. |
| **KE-IQ** | Questionnaire UI + β/γ KE Wiring | 🟣 READY TO ISSUE | `Knowledge_Engine/CODEX_COMMISSION_KE_IQ_QUESTIONNAIRE_UI.md` | KE Sprint 2 gate passed 2026-05-17. Blocker cleared. QuestionnaireWidget.jsx (1101 lines) exists. Issue now. |

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
| **IR-2** | Lunar Cycle Wellness Backend (`lunar_cycle_router.py`) | ✅ INTEGRATED -- commit `f9f6690` | `Individual_Reports/CODEX_COMMISSION_IR_2_LUNAR_CYCLE.md` | Delivered by Codex IR 2026-05-16. CC fix: removed erroneous `["house"]` subscript on `house_entry_from_longitude` (returns int, not dict). All 4 files live. |
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
| **REM-P1** | Remedies Engine Phase 1 (KP collection + remedy_ref pipeline) | ✅ INTEGRATED -- runtime confirmed | `Remedies/CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md` | All 3 tasks complete: `/ref/` endpoint live (line 851), `krishna_prashnavali_remedies` seeded (36 records, modified=36 on 2026-05-15), KP fallback wiring confirmed. ⚠️ Open content note: JSON verdict split is 10/8/8/10 (YES/WAIT/NO/PRAY) vs spec'd 9/9/9/9 -- TT to confirm intentional or re-ingest needed. Commission closed. |

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
| **ARC-2** | Arc Angel Dynamic Confidence Engine (3-pillar wiring + decay + notifications) | 🟣 READY TO ISSUE | `Arc_Angel/CODEX_COMMISSION_ARC_2_CONFIDENCE_QUESTIONNAIRE.md` | KE-Sprint3 live ✅ (KE-OP-13 cleared 2026-05-17). Formula: Base 40% + Pillar 1 24% + Pillar 2 12% + Pillar 3 10% (decay) = cap 86%. Deliverables: questionnaire hooks, IR hooks, Pillar 3 decay APScheduler job, notification triggers. UI deliverables (premium gate, sidebar, upgrade prompt) ⏸ HOLD pending TT approval. **Pre-condition: issue KE-OP-14 (window granularity fix) to KE Codex thread first** so ARC-2 gets 3 AD-level windows per domain. |

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
| **LON-1** | Ayur Jyotish Longevity Report | 🟣 READY TO ISSUE | `Longevity/CODEX_COMMISSION_LONGEVITY_REPORT_CONTRACT.md` | KE Sprint 2 gate passed 2026-05-17. Blocker cleared. Large scope -- issue after higher-priority threads running. |

---

## MODULE 12 -- Live TV

| Commission ID | Commission Name | Status | Notes |
|---|---|---|---|
| **LTV-1** | Live TV: Sai Baba Arti | ✅ INTEGRATED | `Live_TV/CODEX_COMMISSION_LIVE_TV_SAI_BABA_ARTI.md`. Panel live on Landing, Home (logged-in), PanchangPage + all sub-routes, dedicated SEO page. Vercel CDN assets. Render Starter (always-on). Open: LTV-OP-1 console polish (deferred). |

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

> Last refreshed: 2026-05-17 (session 3)

| Priority | Commission ID | Module | Name | Status |
|---|---|---|---|---|
| ✅ DONE | KE-Sprint2 | Knowledge Engine | KE Arbitration Runtime | ✅ INTEGRATED 2026-05-17 |
| ✅ DONE | KE-2A | Knowledge Engine | Yoga Check Evaluation Engine (26 types) | ✅ INTEGRATED 2026-05-17 |
| ✅ DONE | KE-Sprint3 | Knowledge Engine | Arc Angel Computation (G-07/08/09) | ✅ LIVE -- KE-OP-13 cleared 2026-05-17. KE-OP-14 open (window granularity -- fix in KE thread) |
| ✅ DONE | KP-2A | KP Oracle | Bundle Editorial + Share Card + Remedies Admin | ✅ INTEGRATED commit `7d42880`. KP-OP-9 items 2+3 pending TT. |
| ✅ DONE | REM-P1 | Remedies Engine | Remedies Engine Phase 1 | ✅ INTEGRATED 2026-05-16 |
| ✅ DONE | IR-1 | Individual Reports | 5 Public SEO Landing Pages | ✅ INTEGRATED commit `825a294` |
| ✅ DONE | IR-2 | Individual Reports | Lunar Cycle Wellness Backend | ✅ INTEGRATED commit `f9f6690` |
| ✅ DONE | STR-1 | The Strategist | Premium Landing + War Room Visual Rebuild | ✅ INTEGRATED commit `ba58192` |
| ✅ DONE | STR-2J | The Strategist | Missions UI (MissionCard + dasha display) | ✅ INTEGRATED commit `9ad2e0a` |
| 🔴 HIGH | KE-OP-14 | Knowledge Engine | Window granularity fix (AD-level periods) | 🔴 ISSUE TO KE THREAD FIRST -- blocks ARC-2 final UI |
| 🔴 HIGH | KP-Sprint2 | KP Oracle | /ask-question LLM Router (Guna + Gita) | 🔵 IN PROGRESS -- issued 2026-05-15 |
| 🔴 HIGH | KE-IQ | Knowledge Engine | Questionnaire UI + β/γ Wiring | 🟣 READY TO ISSUE -- no dependency |
| 🔴 HIGH | ARC-2 | Arc Angel | Dynamic Confidence Engine (3-pillar + decay + notifications) | 🟣 READY TO ISSUE -- issue after KE-OP-14 fix confirmed |
| 🟠 HIGH | KP-2B | KP Oracle | Ritual Animation + 3-Pillar UX + Astro-Filter | 🟡 BLOCKED -- KP-OP-9 items 2+3 pending TT verification |
| 🟠 HIGH | PUN-2 | Punya Rewards | Home Promo + Module Hooks + SVG Wheel | 🟣 READY TO ISSUE -- no dependency |
| 🟠 HIGH | IR-3 | Individual Reports | 8 Love Report SEO Landing Pages | 🟣 READY TO ISSUE -- frontend only, no dependency |
| 🟡 MED | TAR-v4 | Tarot | Tarot UI v4 Enhancement | 🟣 READY TO ISSUE -- independent |
| 🟡 MED | KUN-1 | Kundali | Lagna Kundali Frontend (backend live) | 🟣 READY TO ISSUE -- frontend only |
| 🟡 MED | LK-1 | Lal Kitab | LK Standalone Module | 🟣 READY TO ISSUE -- after batch TT approval |
| 🟡 MED | LON-1 | Longevity | Ayur Jyotish Longevity Report | 🟣 READY TO ISSUE -- verify LON-OP-1 (Render load) first. Large scope ~48h. |
| 🟢 LOW | PAN-L1 | Panchang | Language/Regional Pages (Tamil, Telugu, etc.) | 🟣 READY TO ISSUE -- independent |
| 🟢 LOW | SEO-1 | SEO | SEO + Web Performance Optimisation | 🟣 READY TO ISSUE -- issue LAST |
| ⏸ HOLD | ORACLE-P3 | World Oracles | 5 World Oracle Modules | ⏸ PARKING LOT -- Phase 3, after KP 30+ days live |
| ⏸ HOLD | WCE-1 | Commission J | World Context Engine | ⏸ PARKING LOT -- Phase 2, brief not written |

---

## Recommended Issue Order (updated 2026-05-17 session 3)

```
✅ CLOSED / LIVE (no action needed):
  KE-Sprint2   ✅ INTEGRATED -- arbitration runtime, all 5 gates
  KE-2A        ✅ INTEGRATED -- 26 evaluator types, 52 tests
  KE-Sprint3   ✅ LIVE -- arc angel persistence + formula (KE-OP-13 cleared)
  KP-2A        ✅ INTEGRATED -- bundle editorial + share card + remedies admin
  REM-P1       ✅ INTEGRATED -- remedies ref pipeline + 36 records seeded
  IR-1         ✅ INTEGRATED -- 5 natal report SEO landing pages
  IR-2         ✅ INTEGRATED -- lunar cycle wellness backend
  STR-1        ✅ INTEGRATED -- strategist premium landing + war room
  STR-2J       ✅ INTEGRATED -- missions UI + dasha display

NOW ACTIVE (Codex threads in flight):
  KP-Sprint2   🔵 IN PROGRESS -- KP /ask-question LLM router

ISSUE IMMEDIATELY -- NEXT UP:
  KE-OP-14     🔴 Issue to KE Codex thread -- window granularity fix (AD-level periods
               instead of MD-level). Blocks ARC-2 full UI. Small scope.
  KE-IQ        🟣 Issue to KE Codex thread -- questionnaire UI + β/γ wiring.
               No dependency. Can run parallel with KE-OP-14.

ISSUE AFTER KE-OP-14 CONFIRMED:
  ARC-2        🟣 Issue to Arc Angel thread -- 3-pillar dynamic wiring + decay engine
               + notification hooks. Pre-condition: KE-OP-14 fix must be live.

ISSUE IN PARALLEL (no dependencies -- any time):
  PUN-2        🟣 Punya Rewards home promo + module hooks + SVG wheel
  IR-3         🟣 8 Love Report SEO landing pages (frontend only)

ISSUE AFTER KP-OP-9 TT VERIFICATION:
  KP-2B        🟡 KP ritual animation + 3-pillar UX + astro-filter

ISSUE AFTER HIGH-PRIORITY THREADS RUNNING:
  TAR-v4       Tarot UI v4 -- independent
  KUN-1        Lagna Kundali frontend -- backend live, verify LON-OP-1 pattern
  LK-1         Lal Kitab standalone -- after TT batch approval
  LON-1        Longevity report -- verify LON-OP-1 (Render load) first. Large scope.
  PAN-L1       Panchang language pages -- independent

ISSUE LAST:
  SEO-1        SEO + web performance -- only after all high-priority threads running

PARKING LOT (Phase 2/3 -- hold):
  ORACLE-P3    5 World Oracle Modules -- after KP 30+ days live
  WCE-1        World Context Engine -- Phase 2, brief not written
```
