# Temple Team -- Module Tracker
> EverydayHoroscope · Single source of truth for per-module status, open points, and revision history.
> **READ THIS AT THE START OF EVERY CLAUDE CODE SESSION.**
> Last updated: 2026-05-15

---

## How This File Works

- **Status** -- current live state of the module.
- **Open Points** -- everything unresolved, with owner and priority. Nothing should live only in a session summary.
- **Revision Log** -- one row per meaningful change. Date + what + commit or ref.
- **Owner codes:** `TT` = Temple Team (Prateek) · `CC` = Claude Code · `CX` = Codex thread · `BOTH` = joint

Claude Code must update the relevant module section at the end of every session that touches that module.

---

## Status Key

| Badge | Meaning |
|---|---|
| `✅ LIVE` | Module complete and in production |
| `🟡 ACTIVE` | Module live but commission(s) open |
| `🔴 CRITICAL` | Blocking issue -- must resolve before other work |
| `🔵 COMMISSION OPEN` | Codex thread running or ready to issue |
| `🟣 PLANNED` | Brief written, not yet issued |
| `⛔ BLOCKED` | Cannot proceed -- dependency unmet |

---

## Module Index

| # | Module | Status | Hottest Open Point |
|---|---|---|---|
| 1 | [Knowledge Engine](#1-knowledge-engine) | 🔴 CRITICAL | Sprint 2 arbitration -- INGEST FREEZE active |
| 2 | [KP Oracle](#2-kp-oracle-krishna-prashnavali) | 🟡 ACTIVE | M-3 smoke test + /remedies/ref/ endpoint |
| 3 | [Individual Reports](#3-individual-reports) | 🟣 PLANNED | IR-1 ready to issue Week 1 |
| 4 | [Remedies Engine](#4-remedies-engine) | 🟡 ACTIVE | `/api/remedies/ref/{id}` endpoint missing -- CC fix |
| 5 | [The Strategist](#5-the-strategist) | 🟡 ACTIVE | STR-1 unblocked -- issue to Codex now |
| 6 | [Arc Angel](#6-arc-angel) | 🟡 ACTIVE | Confidence % hardcoded 42 -- ARC-2 pending |
| 7 | [Tarot](#7-tarot) | 🟡 ACTIVE | TAR-v4 visual uplift ready to issue |
| 8 | [Kundali / Birth Chart](#8-kundali--birth-chart) | 🟣 PLANNED | KUN-1 ready to issue |
| 9 | [Lal Kitab](#9-lal-kitab-lk) | 🟣 PLANNED | LK-1 ready to issue |
| 10 | [Longevity Report](#10-longevity-report) | ⛔ BLOCKED | Blocked on KE Sprint 2 gate |
| 11 | [Love & Engagement](#11-love--engagement-module) | ✅ LIVE | Nothing open |
| 12 | [Live TV](#12-live-tv) | ✅ LIVE | Nothing open |
| 13 | [Punya Rewards](#13-punya-rewards) | ✅ LIVE | Nothing open |
| 14 | [Notifications](#14-notifications) | 🟡 ACTIVE | WhatsApp (M-5) + Instagram (M-6) blocked on TT |
| 15 | [Panchang](#15-panchang) | ✅ LIVE | PAN-L1 language pages -- issue Week 3+ |
| 16 | [SEO & Web Performance](#16-seo--web-performance) | 🟣 PLANNED | Issue LAST -- after high-priority threads running |
| 17 | [World Oracles](#17-world-oracles-phase-3) | 🟣 PLANNED | Phase 3 -- do not issue yet |
| 18 | [Commission J -- World Context Engine](#18-commission-j--world-context-engine) | 🟣 PLANNED | Phase 2 -- brief not yet written |

---

## Cross-Cutting Items (Temple Team Actions)

These are not tied to one module -- they block multiple threads.

| ID | Item | Owner | Priority | Status |
|---|---|---|---|---|
| M-1 | Replace OG image `frontend/public/og-image.png` -- must be 1200×630 PNG ≤80 KB. Current: 626 KB wrong ratio | TT | 🔴 HIGH | Open |
| M-2 | Run `python3 backend/scripts/seed_policies_v1.py --mongo-url "$MONGO_URL" --db-name horoscope_db` on Render | TT | 🔴 HIGH | Open |
| M-3 | KP Oracle end-to-end smoke test in production -- verify grid, answer, remedy, history | TT | 🔴 HIGH | Open -- blocks KP-2A integration |
| M-5 | WhatsApp OTP verification for +91 96431 10001 in WhatsApp Manager + add payment method to WABA on Meta | TT | 🟡 MED | Open |
| M-6 | Instagram Business Account ID -- not loading in Meta dashboard. Resolve to enable Instagram posting | TT | 🟡 MED | Open |
| M-7 | Design decision: react-snap vs helmet-async pre-render strategy | TT | 🟢 LOW | Open -- await SEO-1 thread recommendation |
| M-8 | Decide if PWA offline caching is in scope | TT | 🟢 LOW | Open -- await SEO-1 thread |
| M-9 | App.js lazy audit -- confirm eager/lazy split | TT | 🟢 LOW | Open -- minor, non-blocking |

---

---

## 1. Knowledge Engine

**Status:** 🔴 CRITICAL -- INGEST FREEZE ACTIVE
**Backend:** `backend/knowledge_engine.py` · `backend/ke_router.py`
**Live endpoint:** `GET /api/knowledge-engine/arc-angel-windows`
**Rules in DB:** 1,036+ (zero `approved` -- all `pending_human_review`)

### Sprint Tracker

| Sprint | Gaps | Status | Gate |
|---|---|---|---|
| Sprint 1 -- Scoring Foundation | G-01 (α/β/γ wiring) | ✅ COMPLETE | Commit `57e347a` -- all 6 tests passed |
| **Sprint 2 -- Arbitration Runtime** | G-03, G-05, G-06, G-04 | 🔴 READY TO ISSUE -- brief complete | **INGEST FREEZE until this gate passes** |
| Sprint 3 -- Arc Angel Computation | G-07, G-08, G-09 | ⛔ BLOCKED on Sprint 2 | Must consume post-arbitration output |
| Sprint 4 -- Questionnaire β/γ | G-10 | 🟣 KE-IQ commission (separate) | Independent track |

### Commission Status

| ID | Commission | Status | Notes |
|---|---|---|---|
| KE-Ingest | Batch Book Ingest Automation v2 | ✅ INTEGRATED | -- |
| KE-Val | Automated Rule Validation Engine | ✅ INTEGRATED | -- |
| KE-Item5-8 | CPath-1 Library Console, Brihat KE Route, Tranche Filter, UI Feedback | ✅ INTEGRATED | -- |
| **KE-Sprint2** | Arbitration Runtime (G-03/G-04/G-05/G-06) | 🔴 READY TO ISSUE | Brief: `Knowledge_Engine/CODEX_COMMISSION_KE_SPRINT2_ARBITRATION.md` |
| **KE-IQ** | Questionnaire UI + β/γ KE Wiring | 🟣 READY TO ISSUE | Brief: `Knowledge_Engine/CODEX_COMMISSION_KE_IQ_QUESTIONNAIRE_UI.md` |
| **KE-2A** | Yoga Check Evaluation Engine (16 evaluator types) | 🟣 READY TO ISSUE | Brief: `Knowledge_Engine/CODEX_COMMISSION_KE_2A_YOGA_CHECK.md` |

### Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| KE-OP-1 | Issue KE-Sprint2 to Codex immediately | TT | 🔴 CRITICAL | Ingest freeze lifts only after this gate passes |
| KE-OP-2 | Issue KE-2A to Codex (independent of Sprint 2) | TT | 🔴 CRITICAL | New `ke_yoga_evaluator.py` + one-line hook into `_condition_matches()` |
| KE-OP-3 | Issue KE-IQ after Sprint 2 ideally (can run in parallel) | TT | 🟠 HIGH | `QuestionnairePage.jsx` exists (29 lines). `QuestionnaireWidget.jsx` exists (1101 lines). |
| KE-OP-4 | Co-founder sign-off on first batch of rules (changes status from `pending_human_review` → `approved`) | TT | 🟠 HIGH | Until approved, Legacy Model is the only active signal |
| KE-OP-5 | After Sprint 2 gate: issue Sprint 3 (Arc Angel computation G-07/G-08/G-09) | CX | 🟠 HIGH | Depends on KE-Sprint2 gate passing first |
| KE-OP-6 | Architecture rule: never add dasha functions to `knowledge_engine.py` -- all astronomical data from `vedic_calculator.py` | CC | 🔴 ENFORCE | Verify on every integration |

### Revision Log

| Date | Change | Ref |
|---|---|---|
| 2026-04-10 | CPath-1 Items 1-8 complete (ingest, validation, tranche filter, library console, Brihat KE route) | Multiple commits |
| 2026-05-14 | Sprint 1 gate passed (α/β/γ scoring) | Commit `57e347a` |
| 2026-05-15 | KE-Sprint2 brief written -- INGEST FREEZE declared | `Knowledge_Engine/CODEX_COMMISSION_KE_SPRINT2_ARBITRATION.md` |
| 2026-05-15 | KE-IQ and KE-2A briefs written | `Knowledge_Engine/CODEX_COMMISSION_KE_IQ_QUESTIONNAIRE_UI.md` · `CODEX_COMMISSION_KE_2A_YOGA_CHECK.md` |

---

## 2. KP Oracle (Krishna Prashnavali)

**Status:** 🟡 ACTIVE -- live, commissions pending
**Frontend:** `frontend/src/pages/KrishnaOraclePage.jsx`
**Backend:** `backend/krishna_prashnavali_router.py`
**Live URL:** `/krishna-prashnavali`

### Commission Status

| ID | Commission | Status | Notes |
|---|---|---|---|
| **KP-2A** | Bundle Editorial + Share Card + Remedies Admin Frontend | 🟣 READY TO ISSUE | Blocked on M-3 smoke test before integration |
| **KP-Sprint2** | /ask-question LLM Logic Router (Guna + Gita) | 🟣 READY TO ISSUE | Currently a ComingSoonPage stub. Independent of KP-2A |
| **KP-2B** | Ritual Animation + 3-Pillar UX + Astro-Filter | 🟣 READY TO ISSUE | Depends on KP-2A delivered first |

### Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| KP-OP-1 | **M-3: KP production smoke test** -- verify grid, answer, remedy, history end-to-end | TT | 🔴 HIGH | Must be done before KP-2A integration begins |
| KP-OP-2 | **`/api/remedies/ref/{remedy_ref_id}` endpoint missing** from `remedies_router.py` | CC | 🔴 HIGH | Claude Code direct fix -- not a Codex commission. Blocks KP-2A integration |
| KP-OP-3 | Issue KP-2A to Codex (after M-3 done) | TT | 🟠 HIGH | Brief: `KP/CODEX_COMMISSION_KP_2A.md` |
| KP-OP-4 | Issue KP-Sprint2 to Codex (independent -- can issue Week 1) | TT | 🟠 HIGH | Brief: `KP/CODEX_COMMISSION_KP_SPRINT2_ASK_QUESTION.md` |
| KP-OP-5 | `krishna_answer` ≠ slot title audit -- KP-G13 slot-level editorial verify | TT | 🟡 MED | Flagged in KP-2A brief. Phase 2 if not done in KP-2A |
| KP-OP-6 | Run `ingest_krishna_prashnavali_remedies_v1.py` against Render if not already done | TT | 🟠 HIGH | Required for remedy_ref pipeline to be populated |

### Revision Log

| Date | Change | Ref |
|---|---|---|
| 2026-05-14 | KP-2A, KP-Sprint2, KP-2B briefs written | `KP/` folder |
| 2026-05-15 | KP-OP-2 identified -- `/api/remedies/ref/{remedy_ref_id}` missing, added as CC direct fix | This session |

---

## 3. Individual Reports

**Status:** 🟣 PLANNED -- backend live, no public landing pages
**Frontend:** `frontend/src/pages/BirthChartPage.jsx` · `BrihatKundliPage.jsx`
**Backend:** `vedic_calculator.py` · individual report endpoints

### Commission Status

| ID | Commission | Status | Notes |
|---|---|---|---|
| **IR-1** | 5 Public SEO Landing Pages | 🟣 READY TO ISSUE | Pure frontend -- zero backend dependency |

### Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| IR-OP-1 | Issue IR-1 to Codex in Week 1 | TT | 🟠 HIGH | No dependency -- can run in parallel with KE-Sprint2 |
| IR-OP-2 | Confirm which 5 report types get landing pages (brief specifies: Natal, Dasha, Compatibility, Career, Remedial) | TT | 🟠 HIGH | Review `Individual_Reports/CODEX_COMMISSION_IR_1_LANDING_PAGES.md` before issuing |

### Revision Log

| Date | Change | Ref |
|---|---|---|
| 2026-05-14 | IR-1 brief written | `Individual_Reports/CODEX_COMMISSION_IR_1_LANDING_PAGES.md` |

---

## 4. Remedies Engine

**Status:** 🟡 ACTIVE -- collections seeded, endpoint missing
**Backend:** `backend/remedies_router.py`
**Collections:** `krishna_prashnavali_remedies` · `jyotish_lk_remedies`

### Commission Status

| ID | Commission | Status | Notes |
|---|---|---|---|
| **REM-P1** | Remedies Engine Phase 1 (KP collection + remedy_ref pipeline) | 🟣 READY TO ISSUE | `/api/remedies/ref/{id}` is a CC direct fix before REM-P1 integration |

### Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| REM-OP-1 | **Add `/api/remedies/ref/{remedy_ref_id}` endpoint** to `remedies_router.py` | CC | 🔴 HIGH | Direct fix -- lookup `remedy_ref_id` in `krishna_prashnavali_remedies`. Must land before KP-2A integration |
| REM-OP-2 | Issue REM-P1 to Codex (Week 2) | TT | 🟠 HIGH | Brief: `Remedies/CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md` |
| REM-OP-3 | Run `ingest_krishna_prashnavali_remedies_v1.py` on Render if not already seeded | TT | 🟠 HIGH | Required for remedy_ref pipeline |

### Revision Log

| Date | Change | Ref |
|---|---|---|
| 2026-05-14 | REM-P1 brief written | `Remedies/CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md` |
| 2026-05-15 | REM-OP-1 identified as CC direct fix (not Codex commission) | This session |

---

## 5. The Strategist

**Status:** 🟡 ACTIVE -- fully functional backend, visual uplift pending
**Frontend:** `frontend/src/pages/strategist/` (multiple pages)
**Backend:** `backend/strategist_router.py` · `backend/strategist_engine.py`
**Live URL:** `/strategist`
**Rules in DB:** 823 (`lalkitab_strategist`) + 22 records IDs 1011-1020, 1126-1137

### Commission Status

| ID | Commission | Status | Notes |
|---|---|---|---|
| **STR-2J** | Strategist Missions UI (MissionCard responsive + dasha display) | ✅ INTEGRATED | Commit `9ad2e0a` -- 2026-05-15. Dasha backend fix by CC. |
| **STR-1** | Premium Landing Page + War Room Visual Rebuild | 🟣 READY TO ISSUE | **Fully unblocked** -- M-4 cleared 2026-05-15 |

### Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| STR-OP-1 | **Issue STR-1 to Codex now** -- M-4 cleared, STR-2J integrated | TT | 🔴 HIGH | Brief: `Strategist/CODEX_COMMISSION_STRATEGIST_LANDING_WARROOM.md` |
| STR-OP-2 | Verify DashaTimingBar live data in production after `9ad2e0a` deploy | TT | 🟠 HIGH | Check `/strategist/missions` -- Mahadasha + Antardasha should show with date ranges |
| STR-OP-3 | M-4 CLOSED -- 22 records (IDs 1011-1020 + 1126-1137) confirmed live | -- | ✅ DONE | `strategist_engine.py` has no `approval_status` filter |

### Architecture Note
`strategist_engine.py` queries `db.knowledge_rules.find({"science_id": SCIENCE_ID})` -- **no `approval_status` filter**. All rules (including `pending_human_review`) are served. This is intentional -- the KE interpretation layer enforces that filter separately.

### Revision Log

| Date | Change | Ref |
|---|---|---|
| 2026-05-14 | STR-1 and STR-2J briefs written | `Strategist/` folder |
| 2026-05-15 | STR-2J delivered by Codex -- MissionCard.jsx + StrategistMissionsPage.jsx integrated | Commit `9ad2e0a` |
| 2026-05-15 | `strategist_router.py` -- Vimshottari antardasha computation added to `_build_war_room_state` | Commit `9ad2e0a` |
| 2026-05-15 | M-4 confirmed cleared -- 22 records live in production | -- |
| 2026-05-15 | STR-1 dependency cleared -- fully unblocked | Commit `df49e5e` |

---

## 6. Arc Angel

**Status:** 🟡 ACTIVE -- panel live, confidence hardcoded, no premium gate
**Frontend:** `frontend/src/components/ArcAngelPanel.jsx` · `frontend/src/pages/ArcAngelPage.jsx`
**Backend:** `GET /api/knowledge-engine/arc-angel-windows`
**Live URL:** `/arc-angel` + NavBar mobile drawer

### Commission Status

| ID | Commission | Status | Notes |
|---|---|---|---|
| ARC-UI | Arc Angel UI Panel (ArcAngelPanel.jsx) | ✅ INTEGRATED | Commit `c01ec8d` |
| **ARC-2** | Confidence % lift + Questionnaire gating + Desktop sidebar | 🟣 READY TO ISSUE | Brief: `Arc_Angel/CODEX_COMMISSION_ARC_2_CONFIDENCE_QUESTIONNAIRE.md` |

### Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| ARC-OP-1 | Issue ARC-2 to Codex (Week 2 -- after KE-Sprint2 ideally, but can run in parallel) | TT | 🟠 HIGH | Confidence % growth: 42 (base) → 60 (questionnaire done) → 72 (3 modules used) |
| ARC-OP-2 | Premium gate -- period columns blurred for free users; upgrade CTA | CX | 🟠 HIGH | Part of ARC-2 commission |
| ARC-OP-3 | Desktop sticky sidebar (`w-80`, collapsible, `lg+` breakpoint) | CX | 🟠 HIGH | Part of ARC-2 commission -- `ArcAngelPage.jsx` |
| ARC-OP-4 | `user_arc_angel_profiles` MongoDB persistence + 24h cache + `?refresh=true` | CX | 🟠 HIGH | Part of ARC-2 commission |
| ARC-OP-5 | Confidence % backend is co-owned with KE-IQ commission -- ARC-2 consumes, KE-IQ owns the compute | BOTH | 🟠 HIGH | Do NOT duplicate confidence scoring logic |

### Revision Log

| Date | Change | Ref |
|---|---|---|
| 2026-04-19 | ARC-UI delivered and integrated -- ArcAngelPanel.jsx live | Commit `c01ec8d` |
| 2026-05-15 | ARC-2 brief written -- confidence %, premium gate, desktop sidebar | `Arc_Angel/CODEX_COMMISSION_ARC_2_CONFIDENCE_QUESTIONNAIRE.md` |

---

## 7. Tarot

**Status:** 🟡 ACTIVE -- fully functional, visual uplift pending
**Frontend:** `frontend/src/pages/TarotPage.jsx`
**Backend:** `backend/tarot_router.py`
**Live URL:** `/tarot`
**Deck:** `frontend/public/tarot_cards.json` (78 SVG cards)

### Commission Status

| ID | Commission | Status | Notes |
|---|---|---|---|
| **TAR-v4** | Tarot UI v4 Enhancement | 🟣 READY TO ISSUE | Pure frontend visual uplift -- no backend changes |

### Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| TAR-OP-1 | Issue TAR-v4 to Codex (Week 3) | TT | 🟡 MED | Brief: `Tarot/CODEX_COMMISSION_TAROT_V4_UI.md` |
| TAR-OP-2 | TAR-v4 must NOT modify `tarot_router.py` or 78-card JSON bundle | CX | 🔴 ENFORCE | Visual layer only |

### Revision Log

| Date | Change | Ref |
|---|---|---|
| 2026-04-30 | TAR-v4 brief written | `Tarot/CODEX_COMMISSION_TAROT_V4_UI.md` |

---

## 8. Kundali / Birth Chart

**Status:** 🟣 PLANNED -- basic UI live, full module pending
**Frontend:** `frontend/src/pages/BirthChartPage.jsx` · `BrihatKundliPage.jsx`
**Backend:** `backend/vedic_calculator.py` (single source of truth)
**Live URL:** `/birth-chart` · `/brihat-kundali`

### Commission Status

| ID | Commission | Status | Notes |
|---|---|---|---|
| KUN-Shadbala | Shadbala Engine | ✅ INTEGRATED | `vedic_calculator.py` -- archived |
| **KUN-1** | Lagna Kundali Module Contract (full UI) | 🟣 READY TO ISSUE | Brief: `Kundali/CODEX_COMMISSION_KUNDALI_LAGNA_CONTRACT.md` |

### Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| KUN-OP-1 | Issue KUN-1 to Codex (Week 4+) | TT | 🟡 MED | Large scope -- house descriptions, planet-in-sign, dasha timeline, transit overlay, PDF |
| KUN-OP-2 | KUN-1 must NOT touch `vedic_calculator.py` computation logic -- visual/interpretive layer only | CX | 🔴 ENFORCE | All chart data from existing endpoints |

### Revision Log

| Date | Change | Ref |
|---|---|---|
| 2026-04-10 | KUN-1 brief written | `Kundali/CODEX_COMMISSION_KUNDALI_LAGNA_CONTRACT.md` |
| 2026-04-25 | Shadbala Engine integrated | `Kundali/_archive/` |

---

## 9. Lal Kitab (LK)

**Status:** 🟣 PLANNED -- data feeds Strategist, no standalone UI
**Backend collections:** `lalkitab_strategist` (462 records) · `jyotish_lk_remedies` (361 records) · `lk_user_profiles` schema exists
**Live URL:** None (standalone) -- data surfaces via The Strategist

### Commission Status

| ID | Commission | Status | Notes |
|---|---|---|---|
| **LK-1** | LK Standalone Module (onboard, remedies, debt audit, tracker) | 🟣 READY TO ISSUE | Brief: `LK/CODEX_COMMISSION_LK_STANDALONE_MODULE.md` |

### Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| LK-OP-1 | Issue LK-1 to Codex (Week 4+) | TT | 🟡 MED | Brief: `LK/CODEX_COMMISSION_LK_STANDALONE_MODULE.md` |
| LK-OP-2 | LK-1 must use existing MongoDB collections -- do NOT create new ones | CX | 🔴 ENFORCE | `jyotish_lk_remedies` + `lalkitab_strategist` already seeded |
| LK-OP-3 | All planetary/dasha data from `vedic_calculator.py` | CX | 🔴 ENFORCE | Architecture rule |

### Revision Log

| Date | Change | Ref |
|---|---|---|
| 2026-05-09 | LK-1 brief written | `LK/CODEX_COMMISSION_LK_STANDALONE_MODULE.md` |

---

## 10. Longevity Report

**Status:** ⛔ BLOCKED -- depends on KE Sprint 2 gate
**Frontend:** `frontend/src/pages/LongevityReportPage.jsx` (quality bar for all modules)
**Backend:** `backend/longevity_router.py` (⚠️ verify -- may have load warning on Render)

### Commission Status

| ID | Commission | Status | Notes |
|---|---|---|---|
| **LON-1** | Ayur Jyotish Longevity Report (main contract) | ⛔ BLOCKED | Must follow KE Sprint 2 gate. Brief ready. |

### Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| LON-OP-1 | Verify `longevity_router.py` loads cleanly on Render -- check for `longevity_router failed to load` in logs | TT | 🟠 HIGH | If failing, Claude Code direct fix needed |
| LON-OP-2 | Do NOT issue LON-1 until KE Sprint 2 gate passes | TT | 🔴 ENFORCE | Needs post-arbitration rule scoring for 8th house and dasha interpretations |
| LON-OP-3 | `LongevityReportPage.jsx` is the quality bar -- all other modules' visual output should match or exceed it | CC | 🟢 NOTE | Reference during all integration reviews |

### Revision Log

| Date | Change | Ref |
|---|---|---|
| 2026-04-10 | LON-1 brief written | `Longevity/CODEX_COMMISSION_LONGEVITY_REPORT_CONTRACT.md` |

---

## 11. Love & Engagement Module

**Status:** ✅ LIVE -- complete, no open commissions
**Frontend:** `frontend/src/pages/LoveModulePage.jsx`
**Backend:** `love_module_router.py` registered in `server.py`

### Commission Status

| ID | Commission | Status |
|---|---|---|
| LOVE-1 | Backend Contract | ✅ INTEGRATED |
| LOVE-FE | Frontend + SEO | ✅ INTEGRATED |

### Open Points

None. Module complete.

### Revision Log

| Date | Change | Ref |
|---|---|---|
| 2026-04-02 | LOVE-1 and LOVE-FE both integrated | -- |

---

## 12. Live TV

**Status:** ✅ LIVE -- complete, no open commissions
**Frontend:** Live TV page
**Backend:** `live_tv_router.py` registered in `server.py`

### Commission Status

| ID | Commission | Status |
|---|---|---|
| LTV-1 | Sai Baba Arti (backend + frontend) | ✅ INTEGRATED |

### Open Points

Scheduled daily social posts (6 AM auto-post to FB + YT) -- Phase 2 parking lot. Not active.

### Revision Log

| Date | Change | Ref |
|---|---|---|
| 2026-04-25 | LTV-1 integrated | -- |

---

## 13. Punya Rewards

**Status:** ✅ LIVE -- engine + earn hooks complete
**Backend:** `backend/punya_rewards_router.py` · `backend/punya_rewards_service.py`
**DB collection:** `user_action_logs` · `DEFAULT_ACTION_RULES` (9 action codes)

### Commission Status

| ID | Commission | Status |
|---|---|---|
| PUN-1 | Punya Rewards Gamification Engine | ✅ INTEGRATED |

### Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| PUN-OP-1 | Arc Angel confidence % consumes `user_action_logs` (+4% per module, capped at 3) -- read-only, no new Punya commission | -- | 🟢 NOTE | ARC-2 commission handles this read |

### Revision Log

| Date | Change | Ref |
|---|---|---|
| 2026-04-25 | PUN-1 integrated | -- |
| 2026-05-15 | Earn hooks wired to 7 pages (Daily/Weekly/Monthly Horoscope, Tarot 3 actions, Numerology, BirthChart, Panchang) | This session |

---

## 14. Notifications

**Status:** 🟡 ACTIVE -- email live, WhatsApp + Instagram blocked
**Backend:** APScheduler + Resend + Meta Cloud API v22.0
**Admin Console:** Notifications tab (5 sub-tabs: Subscribers, Compose, Scheduled, History, Social Media)

### Commission Status

| ID | Commission | Status |
|---|---|---|
| NOTIF-1 | Notification Engine | ✅ INTEGRATED |

### Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| NOTIF-OP-1 | **M-5: WhatsApp OTP** -- complete OTP for +91 96431 10001 in WhatsApp Manager + add payment method to WABA | TT | 🟡 MED | Phone ID: `1062698816928895` · WABA ID: `754513054261096` |
| NOTIF-OP-2 | **M-6: Instagram Business Account ID** -- not loading in Meta dashboard | TT | 🟡 MED | Needed for Instagram posting from Admin Console |
| NOTIF-OP-3 | Scheduled daily social posts (6 AM auto-post FB + YT) | TT | 🟢 LOW | Phase 2 parking lot -- APScheduler ready, needs endpoint + Admin toggle |

### Revision Log

| Date | Change | Ref |
|---|---|---|
| 2026-04-02 | NOTIF-1 integrated -- email via Resend, scheduled sends, subscriber management | -- |

---

## 15. Panchang

**Status:** ✅ LIVE -- fully complete
**Frontend:** `frontend/src/pages/PanchangPage.jsx`
**Backend:** `backend/panchang_router.py` (v11-swiss, 318 cities, 81 countries)
**Live URL:** `/panchang`

### Commission Status

| ID | Commission | Status | Notes |
|---|---|---|---|
| **PAN-L1** | Language/Regional Pages (Tamil, Telugu, Malayalam etc.) | 🟣 READY TO ISSUE | Week 3+ -- issue after high-priority threads running |

### Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| PAN-OP-1 | Issue PAN-L1 to Codex (Week 3+) | TT | 🟡 MED | Brief: `Panchang/CODEX_COMMISSION_PANCHANG_LANGUAGE_PAGES.md` |
| PAN-OP-2 | Bump `ENGINE_VERSION` in `panchang_router.py` before any backend change | CC | 🔴 ENFORCE | Format: `panchang-router-v12-swiss` etc. |

### Revision Log

| Date | Change | Ref |
|---|---|---|
| 2026-04-30 | PAN-L1 brief written | `Panchang/CODEX_COMMISSION_PANCHANG_LANGUAGE_PAGES.md` |

---

## 16. SEO & Web Performance

**Status:** 🟣 PLANNED -- foundations live, comprehensive thread pending
**What's live:** GA4 (G-3HJC8BTHRQ) · GSC + Bing verified · OG tags · JSON-LD · sitemap

### Commission Status

| ID | Commission | Status | Notes |
|---|---|---|---|
| **SEO-1** | SEO + Marketing + Web Performance Optimisation | 🟣 READY TO ISSUE | ⚠️ Issue LAST -- after all high-priority threads running |

### Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| SEO-OP-1 | **M-1: Replace OG image** -- 1200×630 PNG ≤80 KB. Current file: 626 KB wrong ratio | TT | 🔴 HIGH | Blocks social sharing quality |
| SEO-OP-2 | Issue SEO-1 to Codex last (Week 4+ after KE, KP, IR threads running) | TT | 🟢 LOW | Brief: `SEO/CODEX_COMMISSION_SEO_WEBPERF.md` |
| SEO-OP-3 | M-7 design decision (react-snap vs helmet-async) needed before SEO-1 can start | TT | 🟢 LOW | Await SEO-1 thread recommendation |

### Revision Log

| Date | Change | Ref |
|---|---|---|
| 2026-04-30 | SEO-1 brief written | `SEO/CODEX_COMMISSION_SEO_WEBPERF.md` |

---

## 17. World Oracles (Phase 3)

**Status:** 🟣 PLANNED -- Phase 3, do not issue
**Five modules:** Bible ("The Promise Box") · Islamic Fal-nama · Taoist I Ching · Greek Oracle of Delphi · Sikh Hukamnama

### Commission Status

| ID | Commission | Status | Notes |
|---|---|---|---|
| **ORACLE-P3** | Multi-Scriptural World Oracles | 🟣 READY TO ISSUE | ⚠️ Phase 3 only -- do NOT open until KP Oracle live 30+ days |

### Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| ORC-OP-1 | Do NOT issue ORACLE-P3 until KP-2A + KP-2B + KP-Sprint2 all integrated and KP live 30+ days | TT | 🔴 GATE | Phase 3A: Bible + Fal-nama + I Ching first; Phase 3B: Greek + Sikh |
| ORC-OP-2 | Content packs (Bible verses, Fal-nama texts, I Ching hexagrams) must be prepared by Temple Team before Codex can build | TT | 🟠 HIGH | Phase 3 gate -- prep during Phase 2 |

### Revision Log

| Date | Change | Ref |
|---|---|---|
| 2026-05-15 | ORACLE-P3 brief written -- Phase 3 planning doc | `World_Oracles/CODEX_COMMISSION_ORACLE_P3_WORLD_ORACLES.md` |

---

## 18. Commission J -- World Context Engine

**Status:** 🟣 PLANNED -- Phase 2, brief not yet written
**What it is:** Macro α signal layer -- world events (conflict zones, elections, exam periods, festival seasons, economic shocks) feeding into KE rule scoring as an α multiplier. Currently α=1.0 hardcoded in `knowledge_engine.py`.

### Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| CJ-OP-1 | Do NOT write Commission J brief until KE Phase 1.2 Sprints 1-3 all gated and 3,000+ rules approved | TT | 🟢 LOW | Phase 2 minimum |
| CJ-OP-2 | TD-26 (Country Kundali as Alpha Signal) and TD-27 (Forecast Tier) spec-locked in CONTRACT.md -- waiting for Commission J | CC | 🟢 NOTE | Reference `Knowledge_Engine/CODEX_KNOWLEDGE_ENGINE_CONTRACT.md` §TD-26/TD-27 |

### Revision Log

| Date | Change | Ref |
|---|---|---|
| 2026-05-15 | Phase 2 parking lot item documented | This session |

---

## Recommended Issue Order (Current)

```
Week 1 (NOW):
  KE-Sprint2   ← 🔴 CRITICAL -- issue first, ingest freeze
  KE-2A        ← 🔴 CRITICAL -- independent, issue alongside Sprint 2
  KP-Sprint2   ← 🟠 HIGH -- independent
  IR-1         ← 🟠 HIGH -- pure frontend, zero dependency
  STR-1        ← 🟠 HIGH -- M-4 cleared, unblocked

Week 2:
  KP-2A        ← after M-3 smoke test (TT) + /remedies/ref/ endpoint (CC)
  KE-IQ        ← ideally after Sprint 2 gate; can run parallel
  REM-P1       ← after /remedies/ref/ endpoint (CC direct fix)
  ARC-2        ← after KE Sprint 2 ideally

Week 3:
  KP-2B        ← after KP-2A delivered
  TAR-v4       ← independent
  PAN-L1       ← independent

Week 4+:
  KUN-1  ·  LK-1  ·  LON-1 (after KE Sprint 2 gate)  ·  SEO-1 (issue last)

Phase 3:
  ORACLE-P3 (after KP live 30+ days + content packs ready)
```

---

*Cross-reference: `Action Items_ Claude Code.md` (TT action items) · `Codex_Deliveries/List_of_Pending_Codex_Commissions.md` (commission queue) · `Codex_Deliveries/MODULE_BRIEFS.md` (5-liner orientation per module) · `Codex_Deliveries/INDEX.md` (commission registry)*
