# Knowledge Engine -- Module Tracker
> Path: `Codex_Deliveries/Knowledge_Engine/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-17 · v2.3

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- Sprint 1 + 2 + 3 + KE-2A complete · KE-OP-14 open (window granularity fix needed before ARC-2 final) · KE-IQ ready to issue |
| **Backend** | `backend/knowledge_engine.py` · `backend/ke_router.py` · `backend/ke_yoga_evaluator.py` |
| **Live endpoint** | `GET /api/knowledge-engine/arc-angel-windows` |
| **Rules in DB** | 1,036+ · zero `approved` · all `pending_human_review` |
| **Sprint phase** | Phase 1.2 -- Sprint 2 ✅ · KE-2A ✅ · Sprint 3 (G-07/G-08/G-09) delivered locally 2026-05-17 |
| **Yoga evaluators** | 26 types in `EVALUATOR_DISPATCH` · 0 missing mappings · 52 tests green |
| **Module home** | `/Users/apple/Documents/New project/MODULE_KNOWLEDGE_ENGINE/` |

---

## Sprint Tracker

| Sprint | Gaps | Status | Gate |
|---|---|---|---|
| Sprint 1 -- Scoring Foundation | G-01 (α/β/γ wiring) | ✅ COMPLETE | Commit `57e347a` -- all 6 tests passed |
| **Sprint 2 -- Arbitration Runtime** | G-03, G-05, G-06, G-04 | ✅ COMPLETE -- self-certified 2026-05-17 | All 5 gates verified against live code by CC. Codex was in admin reconciliation state. TT self-certified. INGEST FREEZE lifted for Sprint 2 dependency. Sprint 3 now unblocked. |
| Sprint 3 -- Arc Angel Computation | G-07, G-08, G-09 | ✅ LIVE -- verified 2026-05-17 | G-07 verified, G-08 verified, G-09 built, TD-28 corrected. Both routes live on Render, persistence confirmed in MongoDB, 6h cache working. KE-OP-14 open: window granularity returns MD-level (1 period/domain) instead of AD-level (3 periods/domain). Fix in KE thread before ARC-2 finalises. |
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
| **KE-Sprint2** | Arbitration Runtime (G-03/G-04/G-05/G-06) | ✅ INTEGRATED -- self-certified 2026-05-17 | All 5 acceptance gates pass against live code. `_contradiction_score`, `_representation_mode`, `_build_tension_block`, supersession lookup, `scan_chart()` payload all confirmed. Codex was in admin reconciliation state -- TT self-certified per gate evidence. |
| **KE-2A** | Yoga Check Evaluation Engine (16 evaluator types) | ✅ INTEGRATED -- 2026-05-17 | All 9 missing handlers added by Codex (`yoga`, `planet_affliction`, `house_position`, `planet_afflicted`, `planet_conjunction`, `planet_in_house_from_sun`, `planetary_position`, `planet_combust`, `house_placement`). 52 tests pass. 0 missing mappings. 26 total dispatch entries. CC-verified. |
| **KE-Sprint3** | Arc Angel Computation Engine (G-07/G-08/G-09) | ✅ LIVE -- verified 2026-05-17 | Routes live on Render. `overall_confidence_pct: 40` ✅ · `engine_label` ✅ · `arc-angel-profile` 200 ✅ · MongoDB persistence ✅ · 6h cache ✅. KE-OP-13 CLOSED. KE-OP-14 opened: window granularity (1 period/domain returned vs expected 3 AD-level windows -- MD grouping issue). |
| **KE-IQ** | Questionnaire UI + β/γ KE Wiring (TD-19/TD-25/G-10) | 🟣 READY TO ISSUE | `CODEX_COMMISSION_KE_IQ_QUESTIONNAIRE_UI.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| ~~KE-OP-1~~ | ~~Issue KE-Sprint2 to Codex immediately~~ | TT | ✅ DONE | Issued 2026-05-15. |
| ~~KE-OP-2~~ | ~~Issue KE-2A to Codex~~ | TT | ✅ DONE | Issued 2026-05-15. |
| KE-OP-3 | Issue KE-IQ (ideally after Sprint 3 integration check; can run parallel) | TT | 🟠 HIGH | `QuestionnairePage.jsx` exists (29 lines). `QuestionnaireWidget.jsx` exists (1101 lines). Backend β/γ wiring needed. |
| KE-OP-4 | Co-founder sign-off on first rule batch (`pending_human_review` → `approved`) | TT | 🟠 HIGH | Until signed off, Legacy Model is the only active signal. Zero `approved` rules currently. |
| ~~KE-OP-5~~ | ~~Issue Sprint 3 brief to Codex~~ | TT | ✅ DONE | Issued 2026-05-17 and delivered locally the same day. |
| KE-OP-6 | Architecture rule enforcement: never add dasha functions to `knowledge_engine.py` | CC | 🔴 ENFORCE | TD-28 corrected on 2026-05-17. `knowledge_engine.compute_dasha_timeline()` is now only a shim into `vedic_calculator.build_dasha_timeline()`. Keep it that way. |
| ~~KE-OP-7~~ | ~~`compute_dasha_timeline()` in `knowledge_engine.py` future refactor~~ | CC | ✅ DONE | Closed 2026-05-17 by the Sprint 3 TD-28 fix. |
| ~~KE-OP-13~~ | ~~Temple integration / live verification for Sprint 3 routes and persistence~~ | TT | ✅ CLEARED 2026-05-17 | Both routes verified live on Render. `confidence_pct: 40` ✅, `engine_label` ✅, profile route 200 ✅, MongoDB document stored ✅, 6h cache ✅. |
| KE-OP-14 | **Window granularity** -- `arc-angel-windows` returns only 1 auspicious + 1 inauspicious period per domain (MD-level grouping). UI needs 3 AD-level windows per domain for a useful 10-year roadmap. Investigate `build_arc_angel_windows()` grouping logic in KE Codex thread. | CX | 🟠 HIGH | V2 output: `Rahu AD in Rahu MD 2026-05→2029-12` + `Jupiter AD in Jupiter MD 2029-12→2036-05` only. Expected: 3 AD sub-periods within each MD (e.g. Moon AD, Mars AD, Venus AD within Rahu MD). Fix before ARC-2 Codex integration is final. |
| ~~KE-OP-8~~ | ~~Reconcile Sprint 2 acceptance against current repo state~~ | CX | ✅ DONE | All 5 gates verified by CC on 2026-05-17. Sprint 2 self-certified INTEGRATED. |
| ~~KE-OP-12~~ | ~~KE-2A dispatch mapping confirmation~~ | CX | ✅ DONE | CC repo scan identified 9 missing checkable types (79 rules affected). Codex added all 9 handlers. 52 tests pass. 0 missing mappings. Closed 2026-05-17. |
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
| v1.8 | 2026-05-17 | KE-Sprint2 self-certified INTEGRATED after CC ran all 5 acceptance gates against live code -- all passed. Codex was in admin reconciliation state only. Sprint 2 row updated to COMPLETE. KE-OP-8 closed. KE-OP-5 unblocked. KE-2A confirmed incomplete: dispatch table uses 17 evaluators under different names than brief; KE-OP-12 opened requiring Codex to confirm dispatch mapping covers all DB `yoga_check.type` values. | CC | 2026-05-17 |
| v1.9 | 2026-05-17 | Codex attempted KE-OP-12 live verification. `EVALUATOR_DISPATCH` confirmed at 17 entries, but the required Mongo distinct query could not run because this Codex session has no `MONGO_URL` / live DB connection. Repo-side source scan completed only as a fallback and is not a substitute for the required DB audit. | CX | 2026-05-17 |
| v2.0 | 2026-05-17 | **KE-2A INTEGRATED.** CC repo scan of all ingest scripts identified 9 `checkable=True` yoga_check types (79 rules) with no dispatch handler: `yoga`, `planet_affliction`, `house_position`, `planet_afflicted`, `planet_conjunction`, `planet_in_house_from_sun`, `planetary_position`, `planet_combust`, `house_placement`. Codex added all 9 handlers + regression tests. CC verified: 52/52 tests pass, 0 missing mappings, 26 total dispatch entries. KE-OP-12 closed. Sprint 3 (G-07/G-08/G-09) now fully unblocked. INGEST FREEZE lifted. Status → 🟡 ACTIVE. | Codex + CC | `ke_yoga_evaluator.py`, `tests/test_ke_yoga_evaluator.py` |
| v2.1 | 2026-05-17 | **KE-Sprint3 brief written + formula locked.** `CODEX_COMMISSION_KE_SPRINT3_ARC_ANGEL.md`. Formula: 3-Pillar architecture -- Foundation 40% (Vedic Engine, label "Vedic Astrology Engine Activated") + Pillar 1 +24% (12 Areas × 2%, Social Sphere is 6 of 12) + Pillar 2 +12% (IRs × 1%) + Pillar 3 +10% (Daily Rituals, decay after 3-day miss) = cap 86%. Case studies confirmed as internal KE accuracy benchmark only (not formula). Pillar 3 decay engine deferred to ARC-2. Schema includes `pillar_1/2/3` blocks + `last_ritual_date` + `decay_started_at`. 19 acceptance tests specified. | CC + TT | `CODEX_COMMISSION_KE_SPRINT3_ARC_ANGEL.md` |
| v2.2 | 2026-05-17 | **KE-Sprint3 locally delivered.** Added `vedic_calculator.build_dasha_timeline()`, exposed `moon_longitude` from `calculate_vedic_chart()`, converted `knowledge_engine.compute_dasha_timeline()` to a TD-28 shim, added Arc Angel confidence/profile builders and freshness logic, extended `server.py` with cached `arc-angel-windows` + new `arc-angel-profile/{user_id}` retrieval, expanded `user_arc_angel_profile` schema, and added 19 Sprint 3 acceptance tests. Verification: 19/19 Sprint 3 tests pass; 71/71 combined KE tests pass. | Codex | `knowledge_engine.py`, `knowledge_schema.py`, `vedic_calculator.py`, `server.py`, `tests/test_ke_sprint3_arc_angel.py` |
| v2.3 | 2026-05-17 | **KE-OP-13 CLEARED -- Sprint 3 live verified.** Both routes confirmed live on Render: `overall_confidence_pct: 40` ✅, `engine_label: "Vedic Astrology Engine Activated"` ✅, `arc-angel-profile/{user_id}` returns 200 ✅, MongoDB document stored and retrieved ✅, 6h cache `cached: false` on first call ✅. KE-OP-13 closed. KE-OP-14 opened: window granularity returns 1 period/domain (MD-level) instead of 3 (AD-level) -- ARC-2 UI needs the granular AD sub-period view. Fix to be issued to KE Codex thread. | TT + CC | URL V2 outputs 2026-05-17 |
