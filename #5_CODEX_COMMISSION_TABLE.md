# EverydayHoroscope -- Master Codex Commission Table
> Single source of truth for all commissions ever issued, in progress, or pending.
> Use the **Commission ID** when opening or referencing a Codex thread.
> Last updated: 2026-05-29 (GAP reconciliation vs CODEX_QA_INTEGRATION_AUDIT_2026-05-27)

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
| **KE-Sprint3** | Arc Angel Computation (G-07/G-08/G-09) | ✅ LIVE -- fully verified 2026-05-17 | `Knowledge_Engine/CODEX_COMMISSION_KE_SPRINT3_ARC_ANGEL.md` | KE-OP-13 ✅ (routes live, persistence confirmed) · KE-OP-14 ✅ (AD-level window granularity fixed, commit `c4f4b43`) · 20/20 Sprint 3 tests · 72/72 combined KE tests. All Sprint 3 gates cleared. ARC-2 fully unblocked. |
| **KE-IQ** | Questionnaire UI + β/γ KE Wiring | ✅ INTEGRATED `f7aa78b` 2026-05-18 | `Knowledge_Engine/CODEX_COMMISSION_KE_IQ_QUESTIONNAIRE_UI.md` | 75/75 KE tests. KE-OP-15 OPEN: TT to verify live questionnaire endpoints + `user_questionnaire_profiles` persistence on Render. |
| **KE-DEDUP-1** | Dedup Script + Contradiction Detection (`ke_dedup_script.py`) | ✅ INTEGRATED 2026-05-29 | `Knowledge_Engine/CODEX_COMMISSION_KE_DEDUP_CONTRADICTION.md` | TF-IDF cosine similarity, 0.82 threshold, separate contradiction detection via `claim_polarity`, `--dry-run` / `--update-files`, idempotent write-back, summary report. 1/1 tests pass. `scikit-learn>=1.3.0` added to requirements.txt. |

---

## MODULE 2 -- KP Oracle

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **KP-2A** | Bundle Editorial + Share Card + Remedies Admin Frontend | ✅ INTEGRATED | `KP/CODEX_COMMISSION_KP_2A.md` | Commit `7d42880`. TT live verification KP-OP-9 pending. |
| **KP-Sprint2** | /ask-question LLM Logic Router (Guna + Gita) | ✅ INTEGRATED `20d4d29` | `KP/CODEX_COMMISSION_KP_SPRINT2_ASK_QUESTION.md` | `AskQuestionPage.jsx` (514 lines), 60-route logic router JSON (20 SATTVA/RAJAS/TAMAS). **KP-OP-12 OPEN**: TT to verify on production. |
| **KP-2B** | Ritual Animation + 3-Pillar UX + Astro-Filter | ✅ INTEGRATED `20f7b83` | `KP/CODEX_COMMISSION_KP_2B.md` | `KrishnaRitualScreen.jsx`, 3-pillar `KrishnaOraclePage.jsx` (799 lines), astro enrichment. CC fix: lazy sessionStorage init applied. **KP-OP-13 OPEN**: TT to verify on production. |

---

## MODULE 3 -- Individual Reports (Phase 1 -- Natal Reports)

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **IR-1** | 5 Public SEO Landing Pages + `/individual-reports` hub | ✅ INTEGRATED | `Individual_Reports/CODEX_COMMISSION_IR_1_LANDING_PAGES.md` | Commit `825a294`. All 5 natal report landing pages live. |
| **IR-2** | Lunar Cycle Wellness Backend (`lunar_cycle_router.py`) | ✅ INTEGRATED -- commit `f9f6690` | `Individual_Reports/CODEX_COMMISSION_IR_2_LUNAR_CYCLE.md` | Delivered by Codex IR 2026-05-16. CC fix: removed erroneous `["house"]` subscript on `house_entry_from_longitude` (returns int, not dict). All 4 files live. |
| **IR-3** | 8 Love Report Public SEO Landing Pages | ✅ INTEGRATED (QA 2026-05-27) | `Individual_Reports/CODEX_COMMISSION_IR_3_LOVE_LANDING_PAGES.md` | 8 landing pages live. Sample `/love-weather-report` returns 200. |
| **IR-4** | 6 Phase 3 Natal Reports (Wealth/H2, Romance/H5, Vitality/H6, Partnership/H7, Dharma/H9, Gains/H11) | ✅ INTEGRATED (QA 2026-05-27) | `Individual_Reports/CODEX_COMMISSION_IR_4_SIX_NEW_REPORTS.md` | `/reports` expanded 5→11 tiles. Backends + landing pages + server.py wiring live. |
| **IR-5** | 12 Areas of Life Enhancement | ✅ INTEGRATED (QA 2026-05-27) | Inline (no separate brief file) | `/api/reports/enhanced-analysis` live, returns 400 on empty payload. Full panel smoke with real data still needed. |

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
| **ARC-2** | Arc Angel Dynamic Confidence Engine (3-pillar wiring + decay + notifications) | ✅ INTEGRATED `c1a7cb0` 2026-05-18 | `Arc_Angel/CODEX_COMMISSION_ARC_2_CONFIDENCE_QUESTIONNAIRE.md` | 18 files, 746 insertions, 72/72 tests green. 3-pillar confidence wired. Pillar 1 bridge (4→12 domain) stopgap pending KE-IQ enrichment. Decay + notification hooks live. PrivateRoute applied. |

---

## MODULE 8 -- Tarot

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **TAR-v4** | Tarot UI v4 Enhancement (hero, starfield, 5-tab shell, streaks) | ✅ INTEGRATED (QA 2026-05-27) | `Tarot/CODEX_COMMISSION_TAROT_V4_UI.md` | Live at `/tarot`. All 5 tabs confirmed: Daily Draw, Spreads, Favorable Periods, Journal, History. |
| **TAR-SEO-1** | Tarot SEO module: hub + 199 programmatic pages + sitemap | 🟠 LOCAL DELIVERY -- TT to integrate | `Tarot/CODEX_COMMISSION_TAR_SEO_1.md` | Build-verified locally. Not merged/deployed. **TT action required.** |
| **TAR-SEO-2** | Tarot SEO content rewrite (`tarot_seo_data.py`) | 🟡 BLOCKED on TAR-SEO-1 | `Tarot/CODEX_COMMISSION_TAR_SEO_2_REWRITE.md` | Local rewrite ready. Has no production effect until TAR-SEO-1 is integrated. |

---

## MODULE 9 -- Kundali / Birth Chart

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **KUN-1** | Lagna Kundali Frontend Module | 🟣 READY TO ISSUE | `Kundali/CODEX_COMMISSION_KUNDALI_LAGNA_CONTRACT.md` | **Re-scoped 2026-05-16: backend fully live at `/api/lagna-kundali`. Frontend only: `KundaliPage.jsx` + SVG chart + planet table + dasha timeline.** |

---

## MODULE 10 -- Lal Kitab

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **LK-1** | Lal Kitab Standalone Module (onboard, remedies, debt audit, tracker) | ✅ INTEGRATED A2 session 2026-05-09 to 2026-05-13 | `LK/CODEX_COMMISSION_LK_STANDALONE_MODULE.md` | Built in full by Account 2 (A2 session). 7 frontend pages + `lk_diagnostics.py` (272 lines) + `lk_remedies_router.py` (348 lines) live. **Open:** LK-OP-5 PDF not built · LK-OP-6 5 split-required rules · LK-OP-7 96 salvage records · LK-OP-8 TT acceptance verify. |

---

## MODULE 11 -- Longevity

| Commission ID | Commission Name | Status | Brief File | Notes |
|---|---|---|---|---|
| **LON-1** | Ayur Jyotish Longevity Report | 🟡 PARTIAL -- live with gaps | `Longevity/CODEX_COMMISSION_LONGEVITY_REPORT_CONTRACT.md` | Page live at `/longevity-report`. Preview generation works but **LON-OP-2**: 46s response time (target <10s). **LON-OP-1**: save/history/detail path not fully verified. |

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
| **PUN-2** | Punya Rewards Home Promo + Module Hooks + SVG Wheel | 🟡 PARTIAL -- mostly integrated | `Punya_Rewards/CODEX_COMMISSION_PUN_2_FRONTEND_INTEGRATION.md` | Home promo + SVG wheel + cross-module hooks live. **PUN-OP-1 OPEN**: `individual_report` action code missing from backend -- no Punya points for IR generates. Authenticated ledger/spin and admin tab smoke coverage still needed. |

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

## MODULE 19 -- Palmistry (discovered in QA audit 2026-05-27)

| Commission ID | Commission Name | Status | Notes |
|---|---|---|---|
| **PALM-1** | Palmistry analysis + Samudrika Shastra report + persistence | ✅ LIVE | Backend API + frontend at `/palmistry`. Full analysis + history tested. **PALM-OP-1**: frontend copy says birth data used, backend does not collect it -- content drift, medium priority. |

---

## MODULE 20 -- Self-Healing Center (discovered in QA audit 2026-05-27)

| Commission ID | Commission Name | Status | Notes |
|---|---|---|---|
| **SHC-1** | Telemetry engine + diagnostics API + admin UI | 🟡 PARTIAL | Backend + telemetry hooks live. **SHC-UI-1**: `DiagnosticsTab.jsx` IS imported (line 25) + rendered (line 742) in `AdminDashboard.jsx` -- 4 SHC strings confirmed 2026-05-29. QA audit finding was stale. TT to verify "Self-Heal" tab visible at `/admin/dashboard`. |
| **SHC-2** | Razorpay lifecycle ledger + webhook + self-heal jobs | 🟡 PARTIAL | Backend + webhook live. Admin lifecycle ledger UI not in production bundle. |
| **SHC-3** | GST ledger + Gmail OAuth + support triage jobs | 🟡 PARTIAL | Backend routes deployed. **SHC-OPS-1**: Gmail/GST blocked pending 5 Render env vars + OAuth flow. Frontend UI not in deployed bundle. |

---

## MODULE 21 -- Lumina (discovered in QA audit 2026-05-27)

| Commission ID | Commission Name | Status | Notes |
|---|---|---|---|
| **LUM-1** | Lumina AI backend (scripture, chaplain, discernment, prayers, manifestation) | 🟡 PARTIAL | AI/read routes live. Write-path smoke (prayers, manifestation completion) not fully verified. |
| **LUM-FE-1** | Lumina frontend route + 9-tab UI + nav entry | 🟡 PARTIAL | Live at `/lumina`. Frontend has Temple-side drift: 9-tab gold variant vs original 6-tab dark-indigo Phase 1 contract. TT to confirm as accepted v2 scope. |

---

## MODULE 22 -- Lo Shu Grid (discovered in QA audit 2026-05-27)

| Commission ID | Commission Name | Status | Notes |
|---|---|---|---|
| **LSG-1** | Lo Shu Grid backend + 4 public frontend pages + sitemap | 🟠 LOCAL DELIVERY -- not integrated | Delivered locally. Backend router + 4 pages + seed script + sitemap/vercel.json additions. **TT to integrate.** |

---

## MODULE 23 -- Angel Numbers (discovered in QA audit 2026-05-27)

| Commission ID | Commission Name | Status | Notes |
|---|---|---|---|
| **ANGEL-1** | Angel Numbers backend + frontend hub + core + intent pages | 🟡 PARTIAL -- content stale | Routes live at `/angel-numbers/111` and `/angel-numbers/111/love`. API returns 200 but serving pre-ANGEL-2 Mongo content -- old generic closing sentences and action steps. |
| **ANGEL-2** | Angel Numbers generator rewrite (varied endings, intent-specific messages) | 🟡 PARTIAL -- not re-seeded | Code in repo. Not effective in production because Mongo collections still have stale pre-rewrite docs. **Re-seed required.** |

---

## MODULE 24 -- Crystal Healing (discovered in QA audit 2026-05-27)

| Commission ID | Commission Name | Status | Notes |
|---|---|---|---|
| **CRY-1** | Crystal Healing hub + 50 crystal pages + 20 intention pages + calculator | ✅ LIVE | `/crystals`, `/api/crystals/list`, calculator all live and verified 2026-05-27. |
| **CRY-2** | Crystal expansion: 9 planet + 12 sign + 20 problem-area pages | ✅ LIVE | Planet/sign/problem API probes passed. Full 113-URL crystal sitemap live. |

---

## MODULE 25 -- Numerology (full scope, discovered in QA audit 2026-05-27)

| Commission ID | Commission Name | Status | Notes |
|---|---|---|---|
| **NUM-1** | Numerology backend + 11 tiles + Premium Ankjyotish | 🟡 PARTIAL | `/numerology` live. Premium Ankjyotish present. **NUM-OP-1**: backend missing `remedy_card`, `supportive_gems`, `supportive_metals`, `remediation_plan` payload fields vs Codex delivery contract. |
| **NUM-FE-1** | Numerology frontend: standalone report page + structured components | 🟡 PARTIAL | `/numerology/report/test` live. **NUM-OP-2**: main `NumerologyPage` uses generic Brihat-Kundali CTA instead of tile-aware CTA map. |

---

## Summary Dashboard

> Last refreshed: 2026-05-29 (reconciled vs CODEX_QA_INTEGRATION_AUDIT_2026-05-27)

| Priority | Commission ID | Module | Name | Status |
|---|---|---|---|---|
| ✅ DONE | KE-Sprint2 | Knowledge Engine | KE Arbitration Runtime | ✅ INTEGRATED 2026-05-17 |
| ✅ DONE | KE-2A | Knowledge Engine | Yoga Check Evaluation Engine (26 types) | ✅ INTEGRATED 2026-05-17 |
| ✅ DONE | KE-Sprint3 | Knowledge Engine | Arc Angel Computation (G-07/08/09) | ✅ LIVE -- all gates cleared. 72/72 tests. |
| ✅ DONE | KE-IQ | Knowledge Engine | Questionnaire UI + β/γ Wiring | ✅ INTEGRATED `f7aa78b` 2026-05-18. KE-OP-15 open. |
| ✅ DONE | ARC-2 | Arc Angel | Dynamic Confidence Engine (3-pillar + decay) | ✅ INTEGRATED `c1a7cb0` 2026-05-18. 72/72 tests. |
| ✅ DONE | KP-2A | KP Oracle | Bundle Editorial + Share Card + Remedies Admin | ✅ INTEGRATED commit `7d42880`. KP-OP-9 items 2+3 pending TT. |
| ✅ DONE | REM-P1 | Remedies Engine | Remedies Engine Phase 1 | ✅ INTEGRATED 2026-05-16. KP remedy approval gap open. |
| ✅ DONE | IR-1 | Individual Reports | 5 Public SEO Landing Pages | ✅ INTEGRATED commit `825a294` |
| ✅ DONE | IR-2 | Individual Reports | Lunar Cycle Wellness Backend | ✅ INTEGRATED commit `f9f6690` |
| ✅ DONE | IR-3 | Individual Reports | 8 Love Report SEO Landing Pages | ✅ INTEGRATED (QA 2026-05-27) |
| ✅ DONE | IR-4 | Individual Reports | 6 Phase 3 Natal Reports | ✅ INTEGRATED (QA 2026-05-27) |
| ✅ DONE | IR-5 | Individual Reports | 12 Areas of Life Enhancement | ✅ INTEGRATED (QA 2026-05-27) |
| ✅ DONE | STR-1 | The Strategist | Premium Landing + War Room Visual Rebuild | ✅ INTEGRATED commit `ba58192` |
| ✅ DONE | STR-2J | The Strategist | Missions UI (MissionCard + dasha display) | ✅ INTEGRATED commit `9ad2e0a` |
| ✅ DONE | TAR-v4 | Tarot | Tarot UI v4 Enhancement | ✅ INTEGRATED (QA 2026-05-27). All 5 tabs confirmed. |
| ✅ DONE | CRY-1/CRY-2 | Crystal Healing | Full Crystal Healing module | ✅ LIVE (QA 2026-05-27) |
| ✅ DONE | PALM-1 | Palmistry | Full Palmistry analysis + persistence | ✅ LIVE (QA 2026-05-27). Content drift open (medium). |
| ✅ DONE | KP-Sprint2 | KP Oracle | /ask-question LLM Router (Guna + Gita) | ✅ INTEGRATED `20d4d29`. KP-OP-12: TT production verify pending. |
| 🔴 HIGH | TAR-SEO-1 | Tarot | Tarot SEO module (199 programmatic pages) | 🟠 LOCAL DELIVERY -- TT to integrate |
| ✅ DONE | KE-DEDUP-1 | Knowledge Engine | Dedup script + contradiction detection | ✅ INTEGRATED 2026-05-29. 1/1 tests pass. |
| ✅ DONE | KP-2B | KP Oracle | Ritual Animation + 3-Pillar UX + Astro-Filter | ✅ INTEGRATED `20f7b83`. KP-OP-13: TT production verify pending. |
| 🟠 HIGH | LSG-1 | Lo Shu Grid | Full Lo Shu Grid module | 🟠 LOCAL DELIVERY -- TT to integrate |
| 🟡 MED | LON-1 | Longevity | Ayur Jyotish Longevity Report | 🟡 PARTIAL -- LON-OP-2 (46s latency) + LON-OP-1 (save/history) open |
| 🟡 MED | PUN-2 | Punya Rewards | Home Promo + Module Hooks + SVG Wheel | 🟡 PARTIAL -- PUN-OP-1 (IR action code) open |
| 🟡 MED | ANGEL-1/2 | Angel Numbers | Full Angel Numbers + ANGEL-2 content rewrite | 🟡 PARTIAL -- ANGEL-2 re-seed required in Mongo |
| 🟡 MED | SHC-1/2/3 | Self-Healing Center | Telemetry + lifecycle + GST/Gmail | 🟡 PARTIAL -- admin UI not in bundle, Gmail/GST blocked |
| 🟡 MED | LUM-1/LUM-FE-1 | Lumina | Lumina AI backend + 9-tab frontend | 🟡 PARTIAL -- write-path smoke pending, frontend spec drift |
| 🟡 MED | KUN-1 | Kundali | Lagna Kundali Frontend (backend live) | 🟣 READY TO ISSUE -- frontend only |
| ✅ DONE | LK-1 | Lal Kitab | LK Standalone Module | ✅ INTEGRATED A2 session. LK-OP-8 TT acceptance verify pending. |
| 🟡 MED | NUM-1/NUM-FE-1 | Numerology | Full Numerology scope | 🟡 PARTIAL -- payload drift + CTA drift open |
| 🟢 LOW | PAN-L1 | Panchang | Language/Regional Pages (Tamil, Telugu, etc.) | 🟣 READY TO ISSUE -- independent |
| 🟢 LOW | SEO-1 | SEO | SEO + Web Performance Optimisation | 🟣 READY TO ISSUE -- issue LAST |
| ⏸ HOLD | ORACLE-P3 | World Oracles | 5 World Oracle Modules | ⏸ PARKING LOT -- Phase 3, after KP 30+ days live |
| ⏸ HOLD | WCE-1 | Commission J | World Context Engine | ⏸ PARKING LOT -- Phase 2, brief not written |

---

## Recommended Issue Order (updated 2026-05-17 session 3 -- KE-OP-14 fixed)

```
✅ CLOSED / LIVE (no action needed):
  KE-Sprint2   ✅ INTEGRATED -- arbitration runtime, all 5 gates
  KE-2A        ✅ INTEGRATED -- 26 evaluator types, 52 tests
  KE-Sprint3   ✅ LIVE -- arc angel persistence + formula + windows (all gates cleared)
  KE-OP-14     ✅ FIXED -- AD-level granularity restored. 72/72 tests. Commit c4f4b43.
  KP-2A        ✅ INTEGRATED -- bundle editorial + share card + remedies admin
  REM-P1       ✅ INTEGRATED -- remedies ref pipeline + 36 records seeded
  IR-1         ✅ INTEGRATED -- 5 natal report SEO landing pages
  IR-2         ✅ INTEGRATED -- lunar cycle wellness backend
  STR-1        ✅ INTEGRATED -- strategist premium landing + war room
  STR-2J       ✅ INTEGRATED -- missions UI + dasha display

NOW ACTIVE (Codex threads in flight):
  KP-Sprint2   🔵 IN PROGRESS -- KP /ask-question LLM router

ISSUE IMMEDIATELY -- NO REMAINING BLOCKERS:
  ARC-2        🟣 Issue to Arc Angel thread -- 3-pillar dynamic wiring + decay engine
               + notification hooks. All pre-conditions cleared. Issue now.
  KE-IQ        🟣 Issue to KE Codex thread -- questionnaire UI + β/γ wiring.
               No dependency. Can run parallel with ARC-2.

ISSUE IN PARALLEL (no dependencies -- any time):
  PUN-2        🟣 Punya Rewards home promo + module hooks + SVG wheel
  IR-3         🟣 8 Love Report SEO landing pages (frontend only)

ISSUE AFTER KP-OP-9 TT VERIFICATION:
  KP-2B        🟡 KP ritual animation + 3-pillar UX + astro-filter

ISSUE WHEN QUOTA RESETS (~2026-05-31):
  KE-DEDUP-1   🟣 KE dedup script + contradiction detection

TT INTEGRATION ACTIONS (no Codex needed):
  TAR-SEO-1    🟠 Integrate from Codex_Deliveries/Tarot/ -- build verified
  LSG-1        🟠 Integrate Lo Shu Grid from Codex_Deliveries/Lo_Shu_Grid/

ISSUE AFTER HIGH-PRIORITY THREADS RUNNING:
  KUN-1        Lagna Kundali frontend -- backend live
  ~~LK-1~~     ✅ ALREADY LIVE -- A2 session built full module. TT to verify at /lk-remedies (LK-OP-8).
  PAN-L1       Panchang language pages -- independent

ISSUE LAST:
  SEO-1        SEO + web performance -- only after all high-priority threads running

PARKING LOT (Phase 2/3 -- hold):
  ORACLE-P3    5 World Oracle Modules -- after KP 30+ days live
  WCE-1        World Context Engine -- Phase 2, brief not written
```

---

## QA INTEGRATION GAP REGISTER

> Source: `Codex_Deliveries/CODEX_QA_INTEGRATION_AUDIT_2026-05-27.md`
> Threads that have NOT submitted QA audit yet: KP Oracle, Arc Angel, Kundali, Lal Kitab, Love Module, Panchang.

| # | Gap ID | Module | Description | Priority | Owner | Resolved |
|---|---|---|---|---|---|---|
| 1 | LON-OP-2 | Longevity | Preview generation ~46s (target <10s) | 🟠 High | TT + CC | ⬜ |
| 2 | LON-OP-1 | Longevity | Save/history/detail path not fully verified | 🔶 Med | TT | ⬜ |
| 3 | TAR-SEO-INT | Tarot SEO | TAR-SEO-1 local delivery not merged/deployed | 🟠 High | TT | ⬜ |
| 4 | M3-FIX-1 | SEO | Festival-region summary variation fix -- local only | 🟠 High | TT + CC | ⬜ |
| 5 | REM-OP-1 | Remedies | `/api/remedies/ref/` fails -- 0 approved KP records | 🟠 High | TT | ⬜ |
| 6 | REM-OP-2 | Remedies | `/api/remedies/suggest` returns empty for public input | 🟠 High | TT + CC | ⬜ |
| 7 | ANGEL-OP-1 | Angel Numbers | ANGEL-2 in repo; Mongo collections not re-seeded | 🟠 High | TT | ⬜ |
| 8 | ECHO-UI-1 | ECHO/PACE | Admin tab in repo but not in deployed frontend bundle | 🟠 High | TT | ⬜ |
| 9 | LTV-SCOPE-1 | Live TV | `LiveTVPanel` on Panchang + Home pages -- scope drift | 🟠 High | TT | ⬜ |
| 10 | LTV-HTTP-1 | Live TV | Backend emits `http://` media URLs -- mixed-content risk | 🟠 High | TT + CC | ⬜ |
| 11 | STR-SEO-1 | Strategist | Routes return generic root metadata -- SEO gap | 🟠 High | TT + SEO thread | ⬜ |
| 12 | SHC-UI-1 | Self-Healing | `DiagnosticsTab.jsx` wired in repo (confirmed 2026-05-29) -- TT verify tab visible in prod | 🟡 Med | TT | ⬜ |
| 13 | SHC-OPS-1 | Self-Healing | Gmail/GST blocked -- 5 Render env vars + OAuth pending | 🟠 High | TT | ⬜ |
| 14 | KE-OP-15 | KE | KE-IQ live questionnaire endpoints + profiles persistence -- TT verify | 🔶 Med | TT | ⬜ |
| 15 | PUN-OP-1 | Punya | `individual_report` action code missing from backend | 🔶 Med | TT + CC | ⬜ |
| 16 | REM-REC-1 | Remedies | Verdict split 10/8/8/10 vs spec 9/9/9/9 | 🔶 Med | TT | ⬜ |
| 17 | KE-QA-1 | KE | Stale tracker URLs (`/api/knowledge-engine/scan`, `/evaluate-yoga`) | 🔶 Med | TT | ⬜ |
| 18 | PALM-OP-1 | Palmistry | Frontend says birth data used; backend does not collect it | 🔶 Med | TT + Codex | ⬜ |
| 19 | LUM-OP-1 | Lumina | 9-tab gold frontend vs original 6-tab Phase 1 contract -- drift | 🔶 Med | TT | ⬜ |
| 20 | NUM-OP-1 | Numerology | Missing `remedy_card`, `supportive_gems`, `remediation_plan` vs contract | 🔶 Med | TT + Codex | ⬜ |
