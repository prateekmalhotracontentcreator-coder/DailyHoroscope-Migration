# Knowledge Engine -- Module Tracker
> Path: `Codex_Deliveries/Knowledge_Engine/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-15 · v1.5

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🔴 CRITICAL -- INGEST FREEZE ACTIVE |
| **Backend** | `backend/knowledge_engine.py` · `backend/ke_router.py` |
| **Live endpoint** | `GET /api/knowledge-engine/arc-angel-windows` |
| **Rules in DB** | 1,036+ · zero `approved` · all `pending_human_review` |
| **Sprint phase** | Phase 1.2 -- Sprint 2 IN PROGRESS · **RECONCILIATION-FIRST** -- arbitration helpers already in main repo; Codex to verify gate criteria, not re-implement |
| **Module home** | `/Users/apple/Documents/New project/MODULE_KNOWLEDGE_ENGINE/` |
| **Codex metrics** | Spec 88% · Build 79% · Integration 63% · Live readiness 28% (source: 05_MODULE_DASHBOARD.md 2026-05-15) |

---

## Sprint Tracker

| Sprint | Gaps | Status | Gate |
|---|---|---|---|
| Sprint 1 -- Scoring Foundation | G-01 (α/β/γ wiring) | ✅ COMPLETE | Commit `57e347a` -- all 6 tests passed |
| **Sprint 2 -- Arbitration Runtime** | G-03, G-05, G-06, G-04 | 🔵 IN PROGRESS -- RECONCILIATION-FIRST | Issued to Codex 2026-05-15. `_contradiction_score`, `_representation_mode`, `_build_tension_block` already present in main repo. Codex task: verify gate criteria against live code, not re-implement. ⚠️ INGEST FREEZE until gate passes. |
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
| **KE-2B2** | Varga Dignity Wiring (facts layer) | ✅ INTEGRATED -- confirmed 2026-05-15 | `knowledge_engine.py` lines 195-208, 312, 360, 488-508. Built internally. |
| **KE-2D** | Varga Dignity Tier Evaluator | ✅ INTEGRATED -- confirmed 2026-05-15 | `ke_yoga_evaluator.py` lines 373-387, 631. 37 tests green. Migration script archived. Built internally. |
| **KE-Sprint2** | Arbitration Runtime (G-03/G-04/G-05/G-06) | 🔵 IN PROGRESS | Issued to Codex 2026-05-15. `CODEX_COMMISSION_KE_SPRINT2_ARBITRATION.md` |
| **KE-2A** | Yoga Check Evaluation Engine (16 evaluator types) | 🔵 IN PROGRESS | Issued to Codex 2026-05-15. `CODEX_COMMISSION_KE_2A_YOGA_CHECK.md` |
| **KE-IQ** | Questionnaire UI + β/γ KE Wiring (TD-19/TD-25/G-10) | 🟣 READY TO ISSUE | `CODEX_COMMISSION_KE_IQ_QUESTIONNAIRE_UI.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| ~~KE-OP-1~~ | ~~Issue KE-Sprint2 to Codex immediately~~ | TT | ✅ DONE | Issued 2026-05-15. |
| ~~KE-OP-2~~ | ~~Issue KE-2A to Codex~~ | TT | ✅ DONE | Issued 2026-05-15. |
| KE-OP-3 | Issue KE-IQ (ideally after Sprint 2; can run parallel) | TT | 🟠 HIGH | `QuestionnairePage.jsx` exists (29 lines). `QuestionnaireWidget.jsx` exists (1101 lines). Backend β/γ wiring needed. |
| KE-OP-4 | Co-founder sign-off on first rule batch (`pending_human_review` → `approved`) | TT | 🟠 HIGH | Until signed off, Legacy Model is the only active signal. Zero `approved` rules currently. |
| KE-OP-5 | After Sprint 2 gate passes: issue Sprint 3 (G-07/G-08/G-09 Arc Angel computation) | TT | 🟠 HIGH | Depends strictly on KE-Sprint2 gate. |
| KE-OP-6 | Architecture rule enforcement: never add dasha functions to `knowledge_engine.py` | CC | 🔴 ENFORCE | All astronomical data from `vedic_calculator.py`. Verify on every integration. |
| KE-OP-7 | `compute_dasha_timeline()` in `knowledge_engine.py` (line 829) -- flag for future refactor to import from `vedic_calculator` | CC | 🟢 LOW | Reads pre-computed dict only -- not a duplicate calculator. Do not add further dasha logic here. |
| KE-OP-8 | Reconcile Sprint 2 acceptance against current repo state | CX | 🔴 CRITICAL | Intake audit on 2026-05-15 found `_contradiction_score`, `_representation_mode`, `_build_tension_block`, and arbitration summary wiring already present in `backend/knowledge_engine.py`. Do not re-implement blindly; verify gate criteria and tracker alignment first. |
| ~~KE-OP-9~~ | ~~Verify `yoga_combination` dispatch hook: `knowledge_engine.py` → `ke_yoga_evaluator.evaluate_yoga_check`~~ | CC | ✅ DONE | Already present in `knowledge_engine.py` lines 634-636. No action needed. Confirmed 2026-05-15. |
| ~~KE-OP-10~~ | ~~Verify `combust` extraction path in `knowledge_engine.py` for `free_from_combustion` conditions~~ | CC | ✅ DONE | Gap was in `ke_yoga_evaluator._planet_in_kendra_conditions_ok`. Added `combust_ok` guard using `ChartFacts.planet_positions[planet]["combust"]`. `_unsupported_note` cleaned up. Fixed 2026-05-15. |
| ~~KE-OP-11~~ | ~~Run `migrate_ch41_varga_checkable.py` -- 24 Ch 41 Varga-tier rules need Mongo update~~ | CC + TT | ✅ DONE | Run 2026-05-15 against `horoscope_db`. Summary: updated=24, skipped=0, errors=0. All 24 rules now `checkable=True` with `varga_dignity_tier` condition type. |

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
| v1.3 | 2026-05-15 | KE-2B2 (Varga Dignity Wiring) + KE-2D (Varga Dignity Tier Evaluator) confirmed INTEGRATED via live-repo audit -- both built internally, not issued to Codex. KE-Sprint2 + KE-2A issued to Codex KE thread. KE-OP-1 + KE-OP-2 closed. Sprint 2 status: IN PROGRESS. | TT + CC | 2026-05-15 |
| v1.4 | 2026-05-15 | Commission intake audit added KE-OP-8 after confirming the current repo already contains Sprint 2 arbitration helpers. Active work now centers on acceptance / integration reconciliation, not assuming a zero-state implementation. | CX | Intake audit 2026-05-15 19:28 IST |
| v1.5 | 2026-05-15 | Codex KE thread response summary ingested. Sprint 2 row updated to RECONCILIATION-FIRST. Module home recorded. Codex dashboard metrics added (Spec 88% / Build 79% / Integration 63% / Live 28%). Three new open points added: KE-OP-9 (yoga_combination dispatch verify), KE-OP-10 (combust extraction verify), KE-OP-11 (migration script run). | TT + CX | 06_RESPONSE_SUMMARY.md 2026-05-15 |
| v1.6 | 2026-05-15 | KE-OP-9 confirmed already present (knowledge_engine.py lines 634-636). KE-OP-10 fixed: added `combust_ok` guard to `_planet_in_kendra_conditions_ok` in `ke_yoga_evaluator.py`; cleaned up `_unsupported_note`. Both closed. | CC | commit `f1d200a` |
| v1.7 | 2026-05-15 | KE-OP-11 complete: `migrate_ch41_varga_checkable.py` run against `horoscope_db`. 24 Ch 41 Varga-tier rules updated to `checkable=True` with `varga_dignity_tier` condition type. updated=24, skipped=0, errors=0. All CC direct actions (OP-9/10/11) now closed. | CC + TT | -- |
