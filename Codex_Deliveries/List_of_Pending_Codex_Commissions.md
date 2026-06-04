# List of Pending Codex Commissions
> EverydayHoroscope · Temple Team Master Tracker
> Last updated: 2026-05-31 (Session 12 -- Full ECHO/PACE scan cycle completed for all delivered modules. 8 fix commissions now READY TO ISSUE: ANGEL-3, RUD-L2, CRY-L2, FAITH-REWRITE, M3-CP-FIX, M3-TR-FIX, M2-COMPAT-FIX, TAR-SEO-FIX.)
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

## 🔴 NEW -- Added 2026-05-25

| ID | Commission | Thread | Brief File | Status | Notes |
|---|---|---|---|---|---|
| **SHC-1** | Self-Healing Dashboard -- Part 1: Telemetry Engine + Diagnostics Admin View | Self-Heal (new thread) | `Self_Healing_Center/CODEX_COMMISSION_SHC.md` | 🟡 READY TO ISSUE | FastAPI middleware + `user_diagnostics` collection + DiagnosticsTab.jsx. Issue first. |
| **SHC-2** | Self-Healing Dashboard -- Part 2: Razorpay Lifecycle Ledger + Webhook | Self-Heal thread | `Self_Healing_Center/CODEX_COMMISSION_SHC.md` | ⏸ AFTER SHC-1 | Server-side Razorpay webhook + `orders_ledger` + 2 APScheduler jobs. Requires `RAZORPAY_WEBHOOK_SECRET` on Render. |
| **SHC-3** | Self-Healing Dashboard -- Part 3: GST Ledger + Gmail Sync | Self-Heal thread | `Self_Healing_Center/CODEX_COMMISSION_SHC.md` | ⏸ AFTER SHC-2 | `gst_recon_ledger` + pdfplumber + Gmail OAuth + 3 APScheduler jobs. Requires 5 new Render env vars. |

---

## 🔴 CRITICAL -- Issue Immediately (Blocking Other Work)

| ID | Commission | Thread | Brief File | Status | Dependency | Notes |
|---|---|---|---|---|---|---|
| **SEO-20K** | 22,170 Programmatic SEO Pages (Umbrella -- M4/M5 queued) | SEO Legacy Thread | `SEO/CODEX_COMMISSION_SEO_20K.md` | 🟡 DELIVERED -- PENDING INTEGRATION (M4) · M5 READY | None | M1 ✅ `2a4ed4e` M2 ✅ `aba7d5c` M3 ✅ integrated by TT. **M4 / TAR-SEO-1** (Tarot SEO, 199 pages) local delivery prepared 2026-05-25 with clean build -- ⏸ HOLD (TT sorting internally). **M5 / FAITH-20K** (16,800+ pages) → brief complete at `Faith_Hubs/CODEX_COMMISSION_FAITH_20K.md` -- READY TO ISSUE. |
| ~~**FAITH-20K**~~ | ~~Faith & Scripture SEO Hub -- 16,800 English pages~~ | Faith Hubs | `Faith_Hubs/CODEX_COMMISSION_FAITH_20K.md` | ✅ DELIVERED -- ECHO/PACE CRITICAL FAIL (L1) | None | Generator delivered (faith_gita_data.py, faith_bible_data.py, faith_seo_data.py). Gita L1=100%, Bible L1=82%, Transit L1=100%. Root cause: fixed situation/topic boilerplate. MUST NOT seed. |
| **FAITH-REWRITE** | Faith & Scripture Generator Rewrite -- verse-specific anchoring (Gita), topic body variation (Bible), tradition separation (Transit), seasonal variation (Daily) | Faith Hubs thread | `Faith_Hubs/CODEX_COMMISSION_FAITH_REWRITE.md` | 🔴 READY TO ISSUE -- CRITICAL | FAITH-20K ✅ | Brief complete. Gita L1=100%, Bible L1=82%, Transit L1=99.5%. Same failure mode as ANGEL-1. All types must reach L1 < 50%. |
| ~~**ANGEL-1**~~ | ~~Angel Numbers -- Full module: 1,000 core pages × 9 intents = 10,001 pages~~ | Angel Numbers | `Angel_Numbers/CODEX_COMMISSION_ANGEL_NUMBERS.md` | ✅ INTEGRATED (code + routes in repo; Mongo seeded with ANGEL-1 content) | -- | All routes, seed scripts, frontend pages in repo. ECHO/PACE FAIL confirmed 2026-05-31. |
| ~~**ANGEL-2**~~ | ~~Angel Numbers Generator Rewrite -- fix all 3 ECHO/PACE failure modes + `how_to_manifest` field~~ | Angel Numbers | `Angel_Numbers/CODEX_COMMISSION_ANGEL_2_REWRITE.md` | ✅ INTEGRATED -- commit `2271c36` 2026-05-31 | -- | L2 + L3 now PASS. L1 still fails (45--57%, gate < 40%). Seed blocked. |
| ~~**ANGEL-3**~~ | ~~Angel Numbers L1 TF-IDF Fix -- expand 8 vocabulary pools so all L1 clusters reach < 40%~~ | Angel Numbers | `Angel_Numbers/CODEX_COMMISSION_ANGEL_3_L1_FIX.md` | ✅ INTEGRATED 2026-06-04 | ANGEL-2 ✅ | All 10 clusters < 40% (worst 39.9%). L2 0 violations. L3 55.6%. Seed unblocked. TT: re-seed both Mongo collections on Render. |
| ~~**RUD-1**~~ | ~~Rudraksha Hub + 21 Mukhi Pages + Calculator~~ | Rudraksha | `Rudraksha/CODEX_COMMISSION_RUDRAKSHA.md` | ✅ DELIVERED -- ECHO/PACE FAIL (L2/L3) | None | Backend delivered + registered. L1 PASS (worst 29%). L2 FAIL (100% boilerplate freq). L3 FLAGGED (title template). Needs RUD-L2 fix before seeding. |
| ~~**RUD-L2**~~ | ~~Rudraksha L2/L3 Fix~~ | Rudraksha thread | `Rudraksha/CODEX_COMMISSION_RUD_L2.md` | ✅ INTEGRATED 2026-06-02 -- L1 ≤25.2%, L2 0 violations, L3 PASS | RUD-1 ✅ | `rudraksha_content.py` rewritten. All ECHO/PACE layers clear. App.js wiring + Mongo seed unblocked. |
| **LSG-1 + LSG-2** | Lo Shu Grid -- full module (57 URLs) | Lo Shu Grid | `Lo_Shu_Grid/CODEX_COMMISSION_LO_SHU_GRID.md` | ✅ INTEGRATED `4538d1e` 2026-05-30 | None | All 7 routes live. TT: seed Mongo + smoke test 8 routes. |
| ~~**CRY-1**~~ | ~~Crystal Healing Hub + 50 Crystal Pages + 20 Intention Pages + Calculator~~ | Crystal Healing | `Crystal_Healing/CODEX_COMMISSION_CRYSTAL_HEALING.md` | ✅ DELIVERED -- ECHO/PACE FAIL (L2/L3) | None | Backend delivered + registered. L1 PASS borderline (47.7% crystal, 20.8% intention). L2 FAIL (100% boilerplate). L3 FLAGGED. Needs CRY-L2 fix before seeding. |
| **CRY-L2** | Crystal Healing L2/L3 Fix -- `_build_faq()` + caution phrase variants (5+ per template, hash-selected); meta_title suffix variation | Crystal Healing thread | `Crystal_Healing/CODEX_COMMISSION_CRY_L2.md` | 🔴 READY TO ISSUE | CRY-1 ✅ | Brief complete. L1 hard constraint: Crystal must not regress past 50%. |
| **M3-CP-FIX** | Character Placements Generator Fix -- ≥6 trait variant blocks per sign×chartpoint×house combo, hash-selected; house-explicit sentences in strengths/challenges/life_themes; FAQ answer variants | SEO Legacy thread | `SEO/CODEX_COMMISSION_M3_CP_FIX.md` | 🔴 READY TO ISSUE -- CRITICAL | SEO-20K M3 ✅ | L1=93.4% CRITICAL -- worst score in full scan. Single file: `seo_m3_builders.py`. |
| **M3-TR-FIX** | Transit Profiles Generator Fix -- ≥8 planet-specific narrative openers, ≥3 phrasing pools for watch_for/transit_themes, FAQ answer variants | SEO Legacy thread | `SEO/CODEX_COMMISSION_M3_TR_FIX.md` | 🔴 READY TO ISSUE | SEO-20K M3 ✅ | L1=71.2% BLOCKED. Single file: `seo_m3_builders.py`. |
| **M2-COMPAT-FIX** | Sign Compatibility Narrative Fix -- ≥6 summary variants + ≥4 koota phrase pools + element-pair framing, all hash-selected | SEO Legacy thread | `SEO/CODEX_COMMISSION_M2_COMPAT_FIX.md` | 🟠 READY TO ISSUE | SEO-20K M2 ✅ | L1=50.0% on gate -- must go strictly below. Single file: `compatibility_router.py`. |
| **TAR-SEO-FIX** | Tarot SEO Generator Fix -- Spreads L2 intro variation (≥6 spread-type openers), Cards L3 meta title (include suit name), Intentions L2+L3 intro + meta title variation | Tarot SEO thread | `SEO/CODEX_COMMISSION_TAR_SEO_FIX.md` | 🟠 READY TO ISSUE | TAR-SEO-1 ✅ TAR-SEO-2 ✅ | Single file: `tarot_seo_data.py`. L1 passes for all 3 types -- must not regress. |
| ~~**ZIB-1**~~ | ~~Zibu Symbols Hub + 88 Symbol Pages~~ | ~~Zibu Symbols~~ | `Zibu_Symbols/CODEX_COMMISSION_ZIBU_SYMBOLS.md` | ❌ CANCELLED -- Copyright Risk | -- | Excluded by TT 2026-05-31. Zibu symbols are proprietary to Shanna Freeke. Module permanently dropped. Do not issue. |
| **IR-5** | 12 Areas of Life Enhancement (Donut Chart + 10-Year Timeline + Graha Drishti + Claude 4-page reports) | Individual Reports | `Individual_Reports/CODEX_COMMISSION_IR_5_12AREAS_ENHANCEMENT.md` | 🔵 IN PROGRESS | IR-4 live verification (IR-OP-12) must pass first | Issued 2026-05-22. Vedic-only (Rahu/Ketu replace Uranus/Neptune). Adds 3 new calc functions to vedic_calculator.py + new router + 2 UI components. |

---

| ~~**KE-Sprint2**~~ | ~~KE Arbitration Runtime (G-03/G-05/G-06/G-04)~~ | Knowledge Engine | `Knowledge_Engine/CODEX_COMMISSION_KE_SPRINT2_ARBITRATION.md` | ✅ INTEGRATED -- self-certified 2026-05-17 | -- | All 5 acceptance gates pass. `_contradiction_score`, `_representation_mode`, `_build_tension_block`, supersession lookup, `scan_chart()` payload confirmed. |
| ~~**KE-2A**~~ | ~~Yoga Check Evaluation Engine (16 evaluator types)~~ | Knowledge Engine | `Knowledge_Engine/CODEX_COMMISSION_KE_2A_YOGA_CHECK.md` | ✅ INTEGRATED -- 2026-05-17 | -- | All 9 missing handlers added. 52 tests pass. 26 dispatch entries. CC-verified. |

---

## 🟠 HIGH PRIORITY -- Issue This Week

| ID | Commission | Thread | Brief File | Status | Dependency | Notes |
|---|---|---|---|---|---|---|
| ~~**KP-2A**~~ | ~~KP Bundle Editorial + Share Card + Remedies Admin Frontend~~ | KP Oracle | `KP/CODEX_COMMISSION_KP_2A.md` | ✅ INTEGRATED -- commit `7d42880` | -- | Delivered + integrated 2026-05-15. TT live verification (KP-OP-9) required before issuing KP-2B. |
| ~~**KP-Sprint2**~~ | ~~KP Ask Question -- Guna Logic Router (20 focus areas, 60-route JSON, 3-card reveal)~~ | KP Oracle | `KP/CODEX_COMMISSION_KP_SPRINT2_ASK_QUESTION.md` | ✅ INTEGRATED -- commit `20d4d29` | None | `AskQuestionPage.jsx` + `ask_question_logic_router.json` (60 routes) + `scriptural_oracle_router.py` ask endpoint. Build clean. TT acceptance checklist verification pending. |
| ~~**KE-IQ**~~ | ~~Questionnaire UI + β/γ KE Wiring~~ | Knowledge Engine | `Knowledge_Engine/CODEX_COMMISSION_KE_IQ_QUESTIONNAIRE_UI.md` | ✅ INTEGRATED -- commit `f7aa78b` 2026-05-18 | -- | `knowledge_router.py`, `QuestionnaireWidget.jsx`, `QuestionnairePage.jsx`, `ArcAngelPanel.jsx`. 75/75 KE tests green. TT live verification pending (KE-OP-15). |
| ~~**IR-1**~~ | ~~5 Public SEO Landing Pages (Individual Reports)~~ | Individual Reports | `Individual_Reports/CODEX_COMMISSION_IR_1_LANDING_PAGES.md` | ✅ INTEGRATED -- commit `825a294` | None | 5 landing pages + public hub live. Route canonical confirmed by TT 2026-05-15. |
| ~~**IR-2**~~ | ~~Lunar Cycle Wellness Backend~~ | Individual Reports | `Individual_Reports/CODEX_COMMISSION_IR_2_LUNAR_CYCLE.md` | ✅ INTEGRATED -- commit `f9f6690` + `021a799` | -- | Live. Datetime bug fixed. Tile on LovePage. IR-2A rework also integrated `692fefa`. |
| ~~**IR-3**~~ | ~~8 Love Report Public SEO Landing Pages~~ | Individual Reports | `Individual_Reports/CODEX_COMMISSION_IR_3_LOVE_LANDING_PAGES.md` | ✅ INTEGRATED -- commit `739c3fa` | -- | 8 wrappers + 8 routes + 8 sitemap URLs. CTA content-driven. TT live spot-check pending. |
| ~~**ARC-2**~~ | ~~Arc Angel Phase 2 -- Confidence % lift + Questionnaire gating + Desktop sidebar~~ | Arc Angel | `Arc_Angel/CODEX_COMMISSION_ARC_2_CONFIDENCE_QUESTIONNAIRE.md` | ✅ INTEGRATED -- commit `c1a7cb0` 2026-05-18 | -- | 18 files, 746 insertions. 72/72 tests green. 3-pillar confidence live (40% base + P1 24% + P2 12% + P3 10%, cap 86%). ArcAngelPanel rebuilt. Left nav split. PrivateRoute for all signed-up users. |
| ~~**REM-P1**~~ | ~~Remedies Engine Phase 1 (KP collection + remedy_ref pipeline)~~ | Remedies | `Remedies/CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md` | ✅ INTEGRATED -- runtime confirmed 2026-05-16 | -- | All 3 tasks complete: `/ref/` endpoint live (line 851), 36 KP remedy records seeded (modified=36 2026-05-15), KP fallback wiring confirmed. ⚠️ TT content note: JSON verdict split is 10/8/8/10 (YES/WAIT/NO/PRAY) vs spec'd 9/9/9/9 -- confirm intentional or re-ingest. |
| ~~**PUN-2**~~ | ~~Punya Rewards Home Page Promo + Module Hooks + SVG Wheel~~ | Punya Rewards | `Punya_Rewards/CODEX_COMMISSION_PUN_2_FRONTEND_INTEGRATION.md` | ✅ INTEGRATED -- commit `2a4ed4e` | PUN-1 ✅ | Landing.jsx promo, SVG wheel, countdown, streak, grouped ledger. Build passed. ⚠️ Open point: `individual_report` action code missing from `DEFAULT_ACTION_RULES` backend -- needs backend fix before that hook can be wired (PUN-OP-1). |

---

## 🟡 MEDIUM PRIORITY -- Issue After High Priority Threads Start

| ID | Commission | Thread | Brief File | Status | Dependency | Notes |
|---|---|---|---|---|---|---|
| ~~**KP-2B**~~ | ~~Ritual Animation + 3-Pillar UX + Astro-Filter~~ | KP Oracle | `KP/CODEX_COMMISSION_KP_2B.md` | ✅ INTEGRATED -- commit `20f7b83` | KP-2A ✅ KP-OP-9 ✅ | `KrishnaRitualScreen.jsx` + 3-pillar `KrishnaOraclePage.jsx` + `scriptural_oracle_router.py` astro enrichment. sessionStorage ritual gate, VerdictBadge, Mahadasha/Antardasha Pillar 2, lazy init fix applied by CC. Build clean. TT acceptance checklist verification pending. |
| ~~STR-1~~ | ~~Strategist Premium Landing Page + War Room Visual Rebuild~~ | The Strategist | `Strategist/CODEX_COMMISSION_STRATEGIST_LANDING_WARROOM.md` | ✅ INTEGRATED -- commit `ba58192` | -- | TheStrategistLandingPage.jsx + StrategistPage.jsx + App.js + sitemap.xml all live. Build verified. |
| ~~STR-2J~~ | ~~Strategist Missions UI (MissionCard responsive + dasha display)~~ | The Strategist | `Strategist/CODEX_COMMISSION_STR_2J_MISSIONS_UI.md` | ✅ INTEGRATED -- commit `9ad2e0a` | -- | Delivered by Codex 2026-05-15. Dasha backend fix applied by Claude Code. |
| ~~**TAR-v4**~~ | ~~Tarot UI v4 Enhancement~~ | Tarot | `Tarot/CODEX_COMMISSION_TAROT_V4_UI.md` | ✅ INTEGRATED -- commit `2a4ed4e` | None | TarotHero, animated starfield, particle burst, card modal+drawer, Celtic Cross layout, streak/XP widget, month-grouped history. Build passed. |
| ~~**KUN-1**~~ | ~~Lagna Kundali Frontend Module~~ | Kundali | `Kundali/CODEX_COMMISSION_KUNDALI_LAGNA_CONTRACT.md` | ✅ INTEGRATED -- commits `1d6fc47` + `e741ee5` | None | Public `/kundali` + `/kundali/view/:chartId` routes wired. Unknown birth time checkbox, House Summary table, route-aware SEO. Build verified. User Manual at `docs/LAGNA_KUNDALI_USER_MANUAL.md`. Share button not integrated (premium paid reports only). ⚠️ TT smoke test `/kundali` in production (KUN-OP-4). |
| **LK-1** | LK Standalone Module (onboard, remedies, debt audit, tracker) | Lal Kitab | `LK/CODEX_COMMISSION_LK_STANDALONE_MODULE.md` | 🔵 IN PROGRESS -- RECONCILIATION PHASE | None | Codex found existing runtime (lk_remedies_router.py, lk_diagnostics.py, 7 LK pages in `pages/lk/`). Proceeding as finish-phase not greenfield. Next targets: premium gating, conflict-interstitial, tracker-rule parity. 361 LK rules + affliction tags live in MongoDB. |
| ~~**SEO-1**~~ | ~~SEO + Marketing + Web Performance Optimisation~~ | SEO | `SEO/CODEX_COMMISSION_SEO_WEBPERF.md` | 🔒 RECLASSIFIED | -- | **Technical SEO items (Core Web Vitals, JSON-LD, sitemaps, caching, hreflang) → absorbed into SEO-20K Part A. Do NOT re-issue to Codex.** Remaining marketing items (blog content, social scheduling, email drip, influencer outreach) are **Temple Team operational tasks**, not Codex commissions. No further Codex action needed on SEO-1. |

---

## 🟢 LOWER PRIORITY -- Phase 2 / Phase 3

| ID | Commission | Thread | Brief File | Status | Phase | Notes |
|---|---|---|---|---|---|---|
| ~~**LON-1**~~ | ~~Ayur Jyotish Longevity Report~~ | Longevity | `Longevity/CODEX_COMMISSION_LONGEVITY_REPORT_CONTRACT.md` | ✅ INTEGRATED -- commit `2a4ed4e` | Phase 2 | Backend aliases `/report`,`/save`,`/my-reports`,`/alerts`,`/report/:id`. LongevityReportPage + App.js route. Build passed. ⚠️ **TT live review of save/detail flow still required (LON-OP-1).** |
| ~~**PAN-L1**~~ | ~~Panchang Language/Regional Pages~~ | Panchang | `Panchang/CODEX_COMMISSION_PANCHANG_LANGUAGE_PAGES.md` | ✅ INTEGRATED -- commit `2a4ed4e` | Phase 2 | PanchangPage.jsx: 5-language config, hreflang, JSON-LD. HTTP 200 on all 5 routes confirmed. |
| **ORACLE-P3** | 5 World Oracle Modules (Bible, Islamic, Taoist, Greek, Sikh) | World Oracles | `World_Oracles/CODEX_COMMISSION_ORACLE_P3_WORLD_ORACLES.md` | ⏸ OPENED -- DEPENDENCY BLOCKED | Phase 3 | Acknowledged by Codex. No runtime work started (correct). Waiting on KP-2A + KP-2B + KP-Sprint2 fully live. Docs updated. |

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
| KUN-1 | Lagna Kundali Frontend Module | `Kundali/CODEX_COMMISSION_KUNDALI_LAGNA_CONTRACT.md` | `1d6fc47` · `e741ee5` · build verified · User Manual written |
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

## Commission Status Snapshot (updated 2026-05-23 · Session 8)

```
BRIEFS / DELIVERIES THIS SESSION (Session 8 -- 2026-05-23):
  ANGEL-1  🟡 READY TO ISSUE   RUD-1    🟡 READY TO ISSUE
  LSG-1    🟡 DELIVERED LOCALLY CRY-1    🟡 READY TO ISSUE
  ZIB-1    🟡 READY TO ISSUE
  SEO-20K M4 (TAR-SEO-1) → delivered locally 2026-05-25, pending TT/CC integration
  SEO-20K M5 (FAITH-1)   → SEO Legacy thread after M4
  ZIB-1    🟡 READY TO ISSUE   SEO-20K M3 🟡 DELIVERED LOCALLY

INTEGRATED (Session 7 -- 2026-05-22):
  KP-Sprint2  ✅ (20d4d29)  KP-2B       ✅ (20f7b83)
  SEO-20K M2  ✅ (aba7d5c)

INTEGRATED (Session 6 -- 2026-05-22):
  LON-1  ✅ (2a4ed4e)  PAN-L1  ✅ (2a4ed4e)  PUN-2   ✅ (2a4ed4e)
  TAR-v4 ✅ (2a4ed4e)  SEO-20K M1 ✅ (2a4ed4e) KUN-1  ✅ (1d6fc47 + e741ee5)

INTEGRATED (prior sessions):
  KE-Sprint2  ✅  KE-2A  ✅  KE-IQ  ✅  ARC-2  ✅  IR-4  ✅
  KP-2A  ✅  REM-P1  ✅  IR-1  ✅  IR-2  ✅  IR-2A  ✅  IR-3  ✅
  STR-1  ✅  STR-2J  ✅  + all SEO-B/C series ✅

IN PROGRESS (Codex threads open):
  SEO-20K     🟡 M4 delivered locally -- pending TT/CC integration
  IR-5        🔵 Issued 2026-05-22
  LK-1        🔵 Reconciliation phase
  ORACLE-P3   ⏸ Dependency-blocked

PENDING TT ACCEPTANCE VERIFICATION (live on production):
  KP-Sprint2  ⚠️ TT to verify /ask-question acceptance checklist
  KP-2B       ⚠️ TT to verify ritual screen + 3-pillar UX + astro enrichment
  LON-1       ⚠️ TT live review of save/detail flow (LON-OP-1)

ISSUING ORDER (Priority sequence for next Codex cycle):
  1. ANGEL-1     → new thread   (10,001 pages -- full module, no phasing)
  2. RUD-1       → new thread   (23 pages, Priority 2 module)
  3. CRY-1       → new thread   (72 pages, Priority 5)
  4. LSG-1       → Temple review / integrate local delivery
  5. SEO-20K M4  → Temple review / integrate local delivery   (Tarot SEO, 199 pages)
  6. SEO-20K M5  → SEO Legacy thread after M4   (Faith Hubs, 163 pages -- Batch 7)
  7. ZIB-1       → new thread   (89 pages, Priority 7)
```
