# Knowledge Engine -- Module Tracker
> Path: `Codex_Deliveries/Knowledge_Engine/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-15 · v1.2

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🔴 CRITICAL -- INGEST FREEZE ACTIVE |
| **Backend** | `backend/knowledge_engine.py` · `backend/ke_router.py` |
| **Live endpoint** | `GET /api/knowledge-engine/arc-angel-windows` |
| **Rules in DB** | 1,036+ · zero `approved` · all `pending_human_review` |
| **Sprint phase** | Phase 1.2 -- Sprint 2 in progress (brief complete, not yet issued) |

---

## Sprint Tracker

| Sprint | Gaps | Status | Gate |
|---|---|---|---|
| Sprint 1 -- Scoring Foundation | G-01 (α/β/γ wiring) | ✅ COMPLETE | Commit `57e347a` -- all 6 tests passed |
| **Sprint 2 -- Arbitration Runtime** | G-03, G-05, G-06, G-04 | 🔴 READY TO ISSUE | ⚠️ INGEST FREEZE until this gate passes |
| Sprint 3 -- Arc Angel Computation | G-07, G-08, G-09 | ⛔ BLOCKED on Sprint 2 | Must consume post-arbitration output |
| Sprint 4 -- Questionnaire β/γ | G-10 | 🟣 KE-IQ commission (separate track) | Independent of Sprint 2/3 |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| KE-Ingest | Batch Book Ingest Automation v2 | ✅ INTEGRATED | `_archive/` |
| KE-Val | Automated Rule Validation Engine | ✅ INTEGRATED | `_archive/` |
| KE-Item5 | Library Console (CPath-1 Item 5) | ✅ INTEGRATED | `_archive/` |
| KE-Item6 | Brihat Kundali × KE Route (CPath-1 Item 6) | ✅ INTEGRATED | `_archive/` |
| KE-Item7 | Simplified Tranche Filter (CPath-1 Item 7) | ✅ INTEGRATED | `_archive/` |
| KE-Item8 | Tranche Filter UI Feedback (CPath-1 Item 8) | ✅ INTEGRATED | `_archive/` |
| **KE-Sprint2** | Arbitration Runtime (G-03/G-04/G-05/G-06) | 🔴 READY TO ISSUE | `CODEX_COMMISSION_KE_SPRINT2_ARBITRATION.md` |
| **KE-2A** | Yoga Check Evaluation Engine (16 evaluator types) | 🔴 READY TO ISSUE | `CODEX_COMMISSION_KE_2A_YOGA_CHECK.md` |
| **KE-IQ** | Questionnaire UI + β/γ KE Wiring (TD-19/TD-25/G-10) | 🟣 READY TO ISSUE | `CODEX_COMMISSION_KE_IQ_QUESTIONNAIRE_UI.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| KE-OP-1 | **Issue KE-Sprint2 to Codex immediately** | TT | 🔴 CRITICAL | Ingest freeze lifts only after Sprint 2 gate passes. Brief complete. |
| KE-OP-2 | **Issue KE-2A to Codex** (independent of Sprint 2) | TT | 🔴 CRITICAL | New `ke_yoga_evaluator.py` + one-line hook into `_condition_matches()` |
| KE-OP-3 | Issue KE-IQ (ideally after Sprint 2; can run parallel) | TT | 🟠 HIGH | `QuestionnairePage.jsx` exists (29 lines). `QuestionnaireWidget.jsx` exists (1101 lines). Backend β/γ wiring needed. |
| KE-OP-4 | Co-founder sign-off on first rule batch (`pending_human_review` → `approved`) | TT | 🟠 HIGH | Until signed off, Legacy Model is the only active signal. Zero `approved` rules currently. |
| KE-OP-5 | After Sprint 2 gate passes: issue Sprint 3 (G-07/G-08/G-09 Arc Angel computation) | TT | 🟠 HIGH | Depends strictly on KE-Sprint2 gate. |
| KE-OP-6 | Architecture rule enforcement: never add dasha functions to `knowledge_engine.py` | CC | 🔴 ENFORCE | All astronomical data from `vedic_calculator.py`. Verify on every integration. |
| KE-OP-7 | `compute_dasha_timeline()` in `knowledge_engine.py` (line 829) -- flag for future refactor to import from `vedic_calculator` | CC | 🟢 LOW | Reads pre-computed dict only -- not a duplicate calculator. Do not add further dasha logic here. |

---

## Architecture Notes (Permanent)

- **C-score formula:** `C = 0.40×polarity_delta + 0.35×timing_delta + 0.15×strength_delta + 0.10×authority_delta`
- **Contradiction flag:** C ≥ 0.55
- **Representation modes:** `synthesis` (C < 0.30) · `tension` (0.30-0.75) · `honest_uncertainty` (C > 0.75)
- **β/γ multipliers:** range 0.78-1.22 · computed from questionnaire · stored in `user_questionnaire_profiles`
- **Approval levels:** `auto_approved` = AI validation passed (NOT live to users) · `approved` = co-founder signed off (ONLY this reaches users)
- **DB:** all ingest targets `horoscope_db` -- do NOT use stale `EverydayHoroscope` DB

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-04-10 | CPath-1 Items 1-8 complete. Ingest, validation, tranche filter, library console, Brihat KE route. `science_registry` seeded. | Codex + CC | Multiple commits |
| v1.1 | 2026-05-14 | Sprint 1 gate passed (α/β/γ scoring). All 6 acceptance tests green. INGEST FREEZE declared. | CC | Commit `57e347a` |
| v1.2 | 2026-05-15 | KE-Sprint2 brief written. KE-2A brief written. KE-IQ brief written. Tracker created. | CC | `CODEX_COMMISSION_KE_SPRINT2_ARBITRATION.md` etc. |
