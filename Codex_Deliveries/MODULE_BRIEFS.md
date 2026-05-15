# Module Briefs -- EverydayHoroscope
> One-pager orientation for every Codex thread. Read your module brief before opening the full commission file.
> Last updated: 2026-05-15

---

## How to Use This File

Each section below is a **5-line brief** for one module. It tells you: what the module does, what is live, what is pending, the key constraint, and which commission files to read. Open the linked brief for the full spec.

---

## 1. Knowledge Engine

**What it is:** The Jyotish rule library and scoring engine -- 1,036+ curated Vedic rules ingested from BPHS and other classical texts, matched to a user's birth chart, scored, arbitrated, and surfaced across all modules.
**What's live:** CPath-1 items 1-8 complete (batch ingest, validation, tranche filter, library console, Brihat Kundali route). Sprint 1 (α/β/γ scoring) gate passed, commit `57e347a`. `science_registry` seeded in MongoDB.
**What's pending:** Sprint 2 (arbitration runtime -- G-03/G-04/G-05/G-06) is CRITICAL and blocks the ingest freeze. Sprint 3 (Arc Angel computation) follows Sprint 2 gate. KE-IQ (questionnaire β/γ wiring) and KE-2A (Yoga Check) are independent tracks.
**Key constraint:** ⚠️ INGEST FREEZE active -- no new chapters until Sprint 2 gate passes. All dasha/astronomical data must come from `vedic_calculator.py`, never from `knowledge_engine.py`.
**Commission files:** `Knowledge_Engine/CODEX_COMMISSION_KE_SPRINT2_ARBITRATION.md` · `Knowledge_Engine/CODEX_COMMISSION_KE_IQ_QUESTIONNAIRE_UI.md` · `Knowledge_Engine/CODEX_COMMISSION_KE_2A_YOGA_CHECK.md` · Reference: `Knowledge_Engine/CODEX_KNOWLEDGE_ENGINE_CONTRACT.md`

---

## 2. KP Oracle (Krishna Prashnavali)

**What it is:** A sacred 18×18 grid oracle -- user taps a cell, receives one of 36 canonical Krishna answers (chaupai + teaching + remedy). Currently live with v2 bundle. Acts as Gate 0 clearance for The Strategist.
**What's live:** Full grid mechanic at `/krishna-prashnavali`. `/api/krishna-prashnavali/select`, `/history`, `/api/remedies/` endpoints live. v2 bundle has `behavioral_remedy` and `remedy_ref` fields populated. KP is also Gate 0 of The Strategist.
**What's pending:** KP-2A (bundle slot-level editorial + visual share card + Remedies Admin frontend tab). KP-Sprint2 (/ask-question LLM Logic Router -- currently a ComingSoonPage stub). KP-2B (White Light ritual animation + 3-pillar Guidance Report UX + Astro-Filter transit enrichment on answer) -- depends on KP-2A.
**Key constraint:** KP production smoke test (M-3) must be done by Temple Team before KP-2A integration. `/api/remedies/ref/{remedy_ref_id}` endpoint is missing from `remedies_router.py` -- Claude Code direct fix needed (not Codex).
**Commission files:** `KP/CODEX_COMMISSION_KP_2A.md` · `KP/CODEX_COMMISSION_KP_SPRINT2_ASK_QUESTION.md` · `KP/CODEX_COMMISSION_KP_2B.md` (depends on KP-2A)

---

## 3. Individual Reports

**What it is:** Five personalised Vedic report types (Natal, Dasha, Compatibility, Career, Remedial) backed by the Knowledge Engine scoring layer. Delivered as structured premium reports from the user's birth chart.
**What's live:** Backend report generation endpoints exist. `BirthChartPage.jsx` and `BrihatKundliPage.jsx` are live. No public SEO landing pages exist -- all five report types are app-only, zero Google discoverability.
**What's pending:** IR-1 -- five public SEO landing pages (one per report type) plus a master `/individual-reports` hub page. Pure frontend, zero backend dependency, can be issued immediately.
**Key constraint:** None. IR-1 is fully independent -- issue to Codex in Week 1 alongside KE-Sprint2.
**Commission files:** `Individual_Reports/CODEX_COMMISSION_IR_1_LANDING_PAGES.md` · Archive: `Individual_Reports/_archive/` (3 historical contract versions)

---

## 4. Remedies Engine

**What it is:** A cross-module remedy pipeline that connects KP Oracle answers, Lal Kitab prescriptions, and Vedic remedies into a unified `remedy_ref` system -- searchable, filterable, and surfaceable across the app.
**What's live:** `remedies_router.py` exists with `/api/remedies/admin/records` (backend live at line 866 in `server.py`). `krishna_prashnavali_remedies` collection seeded in MongoDB. KP bundle v2 has `remedy_ref` fields.
**What's pending:** REM-P1 -- Phase 1 build: `/api/remedies/ref/{remedy_ref_id}` endpoint (currently missing -- Claude Code direct fix), admin-facing remedy browser frontend, and full `remedy_ref` pipeline validation.
**Key constraint:** `/api/remedies/ref/{remedy_ref_id}` is a Claude Code direct fix (not a Codex commission) -- must land before KP-2A integration can complete. The ingest script must be run by Temple Team: `python3 backend/scripts/ingest_krishna_prashnavali_remedies_v1.py`.
**Commission files:** `Remedies/CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md`

---

## 5. The Strategist

**What it is:** A premium Integrated Vedic Career Mentor -- "Bloomberg Terminal for Karma". Combines Krishna Prashnavali (Gate 0), Lal Kitab 5-gate diagnostics, and live Vedic birth chart into a war room for founders and executives. 823 rules in MongoDB. Live at `/strategist`.
**What's live:** Full backend (strategist_router.py, strategist_engine.py), all 6 layers, Gate 0 oracle, Conquest Gauge, Golden Hour state machine, Scoreboard, 5-gate LK diagnostics, Mission Board, Surrogate Bridge, 43-day Action Plan, PDF Executive Report -- all working. Visually basic.
**What's pending:** STR-1 -- new public landing page at `/the-strategist` + full War Room visual rebuild (premium UX to match Longevity/KP quality bar). STR-2J -- Missions page improvements (decision_logic/pivot_logic rendering, command planet badge, Dasha timing bar, responsive grid).
**Key constraint:** STR-1 is fully unblocked -- M-4 cleared 2026-05-15 (22 records confirmed live; `strategist_engine.py` does not filter on `approval_status`). STR-2J ✅ INTEGRATED commit `9ad2e0a`. STR-1 explicitly excludes `StrategistMissionsPage.jsx` (owned by STR-2J).
**Commission files:** `Strategist/CODEX_COMMISSION_STRATEGIST_LANDING_WARROOM.md` (STR-1) · `Strategist/CODEX_COMMISSION_STR_2J_MISSIONS_UI.md` (STR-2J) · Reference: `Strategist/THE_STRATEGIST_FULL_SPEC.md`

---

## 6. Arc Angel

**What it is:** A 12-domain life panel (Health, Career, Finances, Relationships, etc.) showing auspicious and inauspicious dasha periods for each area of life -- computed from the Knowledge Engine post-arbitration output. Lives in the NavBar mobile drawer and at `/arc-angel`.
**What's live:** `ArcAngelPanel.jsx` in NavBar drawer (commit `c01ec8d`). `ArcAngelPage.jsx` full detail view. `GET /api/knowledge-engine/arc-angel-windows` endpoint. Confidence % hardcoded at 42. Mobile only. Stateless (no MongoDB persistence). All 12 domains visible to all logged-in users.
**What's pending:** ARC-2 -- confidence % growth (42→60→72 via questionnaire + module usage), premium gate on period columns, desktop sticky sidebar in `ArcAngelPage.jsx`, and `user_arc_angel_profiles` MongoDB persistence with 24h cache.
**Key constraint:** ARC-2 confidence % logic is co-owned with KE-IQ commission -- ARC-2 consumes the endpoint, KE-IQ owns the backend computation. Do NOT duplicate the confidence scoring. KE Sprint 2 should ideally pass before ARC-2 is issued (for post-arbitration quality).
**Commission files:** `Arc_Angel/CODEX_COMMISSION_ARC_2_CONFIDENCE_QUESTIONNAIRE.md` (ARC-2) · Baseline handoff: `Arc_Angel/CODEX_COMMISSION_ARC_ANGEL_UI_PANEL.md`

---

## 7. Tarot

**What it is:** A 78-card Vedic-flavoured Tarot module with daily draw, multi-card spreads, and reading history. Cards are custom SVG illustrations served from `tarot_cards.json`. Live at `/tarot`.
**What's live:** Full `TarotPage.jsx` with 3 tabs (Daily Draw / Spreads / History), flipping card animations, 78-card deck, bookmark/history tracking, `tarot_router.py` with daily reminder endpoints. Punya Rewards earn hooks wired (`tarot_daily_draw`, `tarot_spread_complete`, `tarot_bookmark`).
**What's pending:** TAR-v4 -- visual uplift to v4 standard (premium UI matching the Longevity/KP quality bar). No backend changes -- purely frontend visual enhancement.
**Key constraint:** TAR-v4 is purely visual. Do NOT modify `tarot_router.py` or the 78-card JSON bundle. No logic changes.
**Commission files:** `Tarot/CODEX_COMMISSION_TAROT_V4_UI.md`

---

## 8. Kundali / Birth Chart

**What it is:** Full Vedic birth chart computation via `vedic_calculator.py` + `pyswisseph` -- Lagna, all 9 planets, Shadbala strength, Digbala power direction, Vimshottari Dasha timeline. Two pages live: `BirthChartPage.jsx` (basic) and `BrihatKundliPage.jsx` (extended with KE route).
**What's live:** `vedic_calculator.py` (single source of truth for all astronomical computation). `BirthChartPage.jsx` and `BrihatKundliPage.jsx` live. `Shadbala Engine` delivered and integrated (commit in `_archive`). `birth_chart_generate` Punya Rewards hook wired.
**What's pending:** KUN-1 -- the full Lagna Kundali Module contract: complete chart UI, house descriptions, planet-in-sign interpretations, dasha timeline visualisation, transit overlay, and premium report output.
**Key constraint:** KUN-1 must not touch `vedic_calculator.py` computation logic -- visual and interpretive layer only. All chart data comes from the existing backend endpoints. Do NOT add dasha functions to `knowledge_engine.py`.
**Commission files:** `Kundali/CODEX_COMMISSION_KUNDALI_LAGNA_CONTRACT.md` · Archive: `Kundali/_archive/CODEX_COMMISSION_SHADBALA_ENGINE_delivered.md`

---

## 9. Lal Kitab (LK)

**What it is:** A standalone Lal Kitab astrology product -- onboarding (birth data + family census), planetary debt diagnosis, 9-debt clearance tracker, and LK remedy prescriptions. Underpins The Strategist's 5-gate karmic diagnostics and debt audit.
**What's live:** LK data feeds The Strategist (Gate 1 Pitru Rin, Gate 5 Digbala). `lalkitab_strategist` collection (462 records). `jyotish_lk_remedies` (361 records). `lk_user_profiles` collection schema exists. No standalone LK product UI.
**What's pending:** LK-1 -- full standalone module: onboarding wizard, debt audit (9 debt types), planetary remedies by house, 43-day tracker, and premium PDF report. Independent of The Strategist UI.
**Key constraint:** LK-1 must use the same debt/remedy collections already live in MongoDB (`jyotish_lk_remedies`, `lalkitab_strategist`). Do NOT create new collections -- route new LK UI to existing backend data. All planetary/dasha data from `vedic_calculator.py`.
**Commission files:** `LK/CODEX_COMMISSION_LK_STANDALONE_MODULE.md`

---

## 10. Longevity Report

**What it is:** The Ayur Jyotish Longevity Report -- a deep Vedic health and longevity analysis combining 8th house analysis, Ashtakavarga vitality score, Mahadasha health trajectory, and Ayurvedic dosha profiling into a premium structured report.
**What's live:** `longevity_router.py` exists (check Render logs for `longevity_router failed to load` warning -- Temple Team to verify). The report endpoint is either live or close to live. `LongevityReportPage.jsx` exists and is the visual quality bar for all other modules.
**What's pending:** LON-1 -- main contract delivery: full Longevity Report with all sections (vitality score, 8th house analysis, dasha health trajectory, dosha profile, remedies, premium PDF). Large scope (~48h estimate). Build after KE Sprint 2 gate passes.
**Key constraint:** LON-1 depends on KE Sprint 2 (post-arbitration rule scoring) for accurate 8th house and dasha interpretations. Issue after KE-Sprint2 gate passes. All data from `vedic_calculator.py` -- no KE dasha duplication.
**Commission files:** `Longevity/CODEX_COMMISSION_LONGEVITY_REPORT_CONTRACT.md` · Archive: `Longevity/_archive/CODEX_COMMISSION_H_BRIEF_v2026-04-10.md` (superseded)

---

## 11. Love & Engagement Module

**What it is:** Synastry-based compatibility analysis -- comparing two birth charts for relationship compatibility across multiple life domains. Backend contract + frontend + SEO both delivered and integrated.
**What's live:** LOVE-1 (backend) and LOVE-FE (frontend + SEO) both INTEGRATED. Module is live and complete. No pending commissions.
**What's pending:** Nothing in the active commission queue. Future: Phase 2 enhancements (deeper domain analysis, relationship timeline) are parking-lot items.
**Key constraint:** Do not open a new thread for Love Module without explicit Temple Team instruction. Current state is production-ready.
**Commission files:** `Love_Module/CODEX_COMMISSION_LOVE_ENGAGEMENT_MODULE.md` (INTEGRATED) · `Love_Module/CODEX_COMMISSION_LOVE_MODULE_FRONTEND.md` (INTEGRATED)

---

## 12. Live TV

**What it is:** A live-streamed Sai Baba Arti experience -- video player with real-time arti schedule, countdown timer, and devotional content. Backend + frontend both integrated.
**What's live:** LTV-1 INTEGRATED -- `live_tv_router.py` live in `server.py`. Frontend live. Punya Rewards earn hook wired. No pending commissions.
**What's pending:** Nothing in the active queue. Scheduled daily social posts (auto-post to FB + YT at 6 AM) are a Phase 2 parking-lot item tied to the Notifications thread.
**Key constraint:** Do not open a new thread without Temple Team instruction. Phase 2 enhancements (more channels, programme schedule) are backlog items.
**Commission files:** `Live_TV/CODEX_COMMISSION_LIVE_TV_SAI_BABA_ARTI.md` (INTEGRATED)

---

## 13. Punya Rewards

**What it is:** A gamification layer -- users earn Punya points for completing spiritual actions (viewing horoscopes, drawing Tarot cards, generating reports, viewing Panchang). Points accumulate in a leaderboard/wallet. Underpins the confidence % growth in Arc Angel.
**What's live:** PUN-1 INTEGRATED -- `punya_rewards_router.py` live in `server.py`. `DEFAULT_ACTION_RULES` in `punya_rewards_service.py` defines 9 action codes. `safeClaimPunyaAction()` frontend hook wired to 7 pages (Daily/Weekly/Monthly Horoscope, Tarot 3 actions, Numerology, BirthChart, Panchang) -- commit this session.
**What's pending:** Arc Angel confidence % uses `user_action_logs` from Punya Rewards to count module usage (+4% per module, capped at 3). This is read-only consumption -- no new Punya commission needed.
**Key constraint:** `safeClaimPunyaAction` is fire-and-forget -- never throws, only fires when user is authenticated. Do NOT block page rendering on Punya calls. Action codes are locked in `DEFAULT_ACTION_RULES` -- new codes require a backend change.
**Commission files:** `Punya_Rewards/CODEX_COMMISSION_PUNYA_REWARDS_GAMIFICATION.md` (INTEGRATED)

---

## 14. Notifications

**What it is:** A full notification engine -- email (via Resend), in-app notifications, WhatsApp (pending verification), and web push. Includes subscriber management, compose, scheduled sends, and history log in the Admin Console.
**What's live:** NOTIF-1 INTEGRATED -- email via Resend ✅, APScheduler for scheduled sends ✅, subscriber management ✅, notification history ✅. WhatsApp blocked on phone verification (M-5). Instagram posting pending (M-6).
**What's pending:** WhatsApp unblocked once M-5 (OTP + payment method) is done by Temple Team. Scheduled daily social posts (6 AM auto-post to FB + YT) are a Phase 2 item. No active Codex commission needed now.
**Key constraint:** WhatsApp template `everydayhoroscope_update` is pending Meta approval. Token must be WhatsApp-specific (not Facebook System User token). Phone ID: `1062698816928895`, WABA ID: `754513054261096`.
**Commission files:** `Notifications/CODEX_COMMISSION_NOTIFICATION_ENGINE.md` (INTEGRATED)

---

## 15. Panchang

**What it is:** A Swiss Ephemeris-powered daily Panchang (Vedic almanac) -- Tithi, Nakshatra, Yoga, Karana, Vara, Sunrise/Sunset/Moonrise/Moonset to the second, Choghadiya, Timing Windows, Special Yogas, and Festival calendar. 318 cities across 81 countries.
**What's live:** `panchang_router.py` v11-swiss fully live. `PanchangPage.jsx` with 6 tabs. Share card wired. Facebook + YouTube posting from Admin Console. Punya Rewards earn hook wired (`panchang_daily_view`). Accuracy verified vs Drik Panchang ±1 min.
**What's pending:** PAN-L1 -- dedicated language/regional landing pages for Tamil, Telugu, Malayalam, Kannada, Hindi, and Marathi audiences (SEO play -- regional panchang searches in India). Pure frontend, no backend changes.
**Key constraint:** PAN-L1 must use the existing `/api/panchang/daily` endpoint with location slugs -- no new backend routes. Language pages must have correct `hreflang` tags and regional schema. `ENGINE_VERSION` must be bumped in `panchang_router.py` before any backend change.
**Commission files:** `Panchang/CODEX_COMMISSION_PANCHANG_LANGUAGE_PAGES.md`

---

## 16. SEO & Web Performance

**What it is:** Technical SEO foundation, server-side meta rendering, pre-rendering strategy, sitemap management, Core Web Vitals optimisation, and structured data (JSON-LD) across the entire app.
**What's live:** GA4 (G-3HJC8BTHRQ) wired. GSC and Bing Webmaster verified + sitemaps submitted. OG tags and JSON-LD schema on all major pages. `SEO.jsx` component used sitewide. `/sitemap.xml` at `frontend/public/`.
**What's pending:** SEO-1 -- comprehensive SEO + web performance optimisation thread: server-side meta, pre-render strategy (react-snap vs helmet-async -- await Temple Team M-7 design decision), hreflang for regional pages, critical-path import optimisation, Vite migration assessment, service worker.
**Key constraint:** ⚠️ Issue SEO-1 LAST -- start only after all high-priority Codex threads (KE, KP, IR) are running. OG image (M-1) must be replaced by Temple Team before SEO work begins. React-snap vs helmet-async design decision (M-7) is required before SEO-1 can start.
**Commission files:** `SEO/CODEX_COMMISSION_SEO_WEBPERF.md`

---

## 17. World Oracles (Phase 3)

**What it is:** Five standalone oracle modules sharing the same grid interaction mechanic as Krishna Prashnavali, each rooted in a different sacred world tradition: Bible ("The Promise Box"), Islamic Fal-nama, Taoist I Ching, Greek Oracle of Delphi, and Sikh Hukamnama.
**What's live:** Nothing. Krishna Prashnavali is the only built oracle. This is a Phase 3 expansion.
**What's pending:** ORACLE-P3 -- full spec written (Phase 3A: Bible + Fal-nama + I Ching first; Phase 3B: Greek + Sikh). Also includes Guna-Meter gamification (Tamas/Rajas/Sattva progress bar tied to remedy completion). Do NOT issue until KP Oracle is fully live and battle-tested for 30+ days.
**Key constraint:** ⚠️ Phase 3 only. Do not open this thread until KP-2A + KP-2B + KP-Sprint2 are all integrated and KP Oracle has been live in production for at least 30 days. Content packs (Bible verses, Fal-nama, Hexagrams) must be prepared by Temple Team before Codex can build.
**Commission files:** `World_Oracles/CODEX_COMMISSION_ORACLE_P3_WORLD_ORACLES.md`

---

## 18. Commission J -- World Context Engine (Phase 2)

**What it is:** A macro-environmental alpha signal layer for the Knowledge Engine -- world events (conflict zones, election periods, festival seasons, exam periods, economic shocks) feeding into rule scoring as an α multiplier. Hooks exist in `knowledge_engine.py` (α=1.0 hardcoded). Commission J is the build.
**What's live:** `alpha` field exists in KE scoring. Currently hardcoded to 1.0 (neutral). No world event data is ingested.
**What's pending:** Commission J brief not yet written. Phase 2 item -- do not start until Knowledge Engine Phase 1.2 (Sprints 1-3) is complete and at least 3,000+ rules are approved. TD-26 (Country Kundali as Alpha Signal) and TD-27 (Forecast Tier) are spec-locked and waiting for Commission J.
**Key constraint:** Must NOT be built before Commission I Phase 1.2 Sprints 1-3 are all gated. Alpha population (Commission J) must not override or bypass the `vedic_calculator.py` dasha baseline. Phase 2 minimum -- no Codex brief will be written until Temple Team opens this phase.
**Commission files:** Brief not yet written. Reference: `Knowledge_Engine/CODEX_KNOWLEDGE_ENGINE_CONTRACT.md` §TD-10, §TD-26, §TD-27 · `CODEX_MASTER_ROADMAP.md` §TDF-P1

---

*See `Codex_Deliveries/INDEX.md` for the full commission registry and `Codex_Deliveries/List_of_Pending_Codex_Commissions.md` for the priority-ordered issue queue.*
