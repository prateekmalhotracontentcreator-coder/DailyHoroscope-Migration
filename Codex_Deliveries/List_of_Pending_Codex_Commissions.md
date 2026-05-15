# List of Pending Codex Commissions
> EverydayHoroscope · Temple Team Master Tracker
> Last updated: 2026-05-15
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
| **KE-Sprint2** | KE Arbitration Runtime (G-03/G-05/G-06/G-04) | Knowledge Engine | `Knowledge_Engine/CODEX_COMMISSION_KE_SPRINT2_ARBITRATION.md` | READY TO ISSUE | KE Sprint 1 ✅ done | **INGEST FREEZE active** -- no new chapters until this gate passes. Blocks Sprint 3 (Arc Angel computation) |
| **KE-2A** | Yoga Check Evaluation Engine (16 evaluator types) | Knowledge Engine | `Knowledge_Engine/CODEX_COMMISSION_KE_2A_YOGA_CHECK.md` | READY TO ISSUE | None | New `ke_yoga_evaluator.py` + one-line hook into `_condition_matches()` |

---

## 🟠 HIGH PRIORITY -- Issue This Week

| ID | Commission | Thread | Brief File | Status | Dependency | Notes |
|---|---|---|---|---|---|---|
| **KP-2A** | KP Bundle Editorial + Share Card + Remedies Admin Frontend | KP Oracle | `KP/CODEX_COMMISSION_KP_2A.md` | READY TO ISSUE | KP smoke test (M-3) | Includes krishna_answer audit + visual share card + Admin Remedies tab |
| **KP-Sprint2** | /ask-question LLM Logic Router (Guna + Gita) | KP Oracle | `KP/CODEX_COMMISSION_KP_SPRINT2_ASK_QUESTION.md` | READY TO ISSUE | None | Independent of KP-2A |
| **KE-IQ** | Questionnaire UI + β/γ KE Wiring | Knowledge Engine | `Knowledge_Engine/CODEX_COMMISSION_KE_IQ_QUESTIONNAIRE_UI.md` | READY TO ISSUE | KE Sprint 2 (ideally) | QuestionnairePage.jsx exists (29 lines). QuestionnaireWidget.jsx exists (1101 lines). Need backend β/γ wiring + endpoint |
| **IR-1** | 5 Public SEO Landing Pages (Individual Reports) | Individual Reports | `Individual_Reports/CODEX_COMMISSION_IR_1_LANDING_PAGES.md` | READY TO ISSUE | None | Pure frontend -- no backend dependency |
| **ARC-2** | Arc Angel Phase 2 -- Confidence % lift + Questionnaire gating + Desktop sidebar | Arc Angel | `Arc_Angel/CODEX_COMMISSION_ARC_2_CONFIDENCE_QUESTIONNAIRE.md` | READY TO ISSUE | KE Sprint 2 (for confidence scoring) | `ArcAngelPanel.jsx` is live and baseline. This is the next phase. |
| **REM-P1** | Remedies Engine Phase 1 (KP collection + remedy_ref pipeline) | Remedies | `Remedies/CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md` | READY TO ISSUE | None | `/api/remedies/ref/{remedy_ref_id}` endpoint also needed (Claude Code direct fix -- not Codex) |

---

## 🟡 MEDIUM PRIORITY -- Issue After High Priority Threads Start

| ID | Commission | Thread | Brief File | Status | Dependency | Notes |
|---|---|---|---|---|---|---|
| **KP-2B** | Ritual Animation + 3-Pillar UX + Astro-Filter | KP Oracle | `KP/CODEX_COMMISSION_KP_2B.md` | READY TO ISSUE | KP-2A delivered | White Light meditation + 3-pillar Guidance Report + transit/dasha enrichment |
| **STR-1** | Strategist Premium Landing Page + War Room Visual Rebuild | The Strategist | `Strategist/CODEX_COMMISSION_STRATEGIST_LANDING_WARROOM.md` | **DELIVERED -- PENDING INTEGRATION** | None ✅ M-4 cleared | Built in Codex workspace 2026-05-15. Paste output to Claude Code for review + integration. |
| ~~STR-2J~~ | ~~Strategist Missions UI (MissionCard responsive + dasha display)~~ | The Strategist | `Strategist/CODEX_COMMISSION_STR_2J_MISSIONS_UI.md` | ✅ INTEGRATED -- commit `9ad2e0a` | -- | Delivered by Codex 2026-05-15. Dasha backend fix applied by Claude Code. |
| **TAR-v4** | Tarot UI v4 Enhancement | Tarot | `Tarot/CODEX_COMMISSION_TAROT_V4_UI.md` | READY TO ISSUE | None | Existing Tarot UI visual uplift to v4 standard |
| **KUN-1** | Lagna Kundali Module Contract | Kundali | `Kundali/CODEX_COMMISSION_KUNDALI_LAGNA_CONTRACT.md` | READY TO ISSUE | None | Full Kundali/birth chart module |
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
| ARC-UI | Arc Angel UI Panel (ArcAngelPanel.jsx) | `Arc_Angel/CODEX_COMMISSION_ARC_ANGEL_UI_PANEL.md` (archived) | `c01ec8d` |
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
| **Sprint 2 -- Arbitration Runtime** | G-03, G-05, G-06, G-04 | **READY TO ISSUE** → brief at `KE-Sprint2` | Ingest freeze until gate passes |
| Sprint 3 -- Arc Angel Computation | G-07, G-08, G-09 | Blocked on Sprint 2 gate | Must consume post-arbitration output |
| Sprint 4 -- Questionnaire β/γ | G-10 | Separate commission KE-IQ | -- |

---

## Recommended Issue Order

```
Week 1:  KE-Sprint2 + KE-2A + KP-Sprint2 (3 independent threads)
Week 1:  IR-1 (pure frontend -- zero backend dependency)

Week 2:  KP-2A (after KP smoke test M-3 done)
         KE-IQ (ideally after Sprint 2 gate passes)
         REM-P1 (plus Claude Code direct fix for /ref/ endpoint)

Week 3:  KP-2B (after KP-2A delivered)
         ARC-2 (after KE Sprint 2 gate passes)
         STR-1 + STR-2J (after M-4 Strategist sign-off)
         TAR-v4

Week 4+: LON-1 · LK-1 · KUN-1 · PAN-L1 · SEO-1
Phase 3: ORACLE-P3
```
