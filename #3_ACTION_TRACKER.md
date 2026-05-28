# Action Items -- Temple App
> Single Source of Truth for all open items across Claude Code sessions.
> Referenced in all handover docs. **Do not create parallel lists elsewhere.**
> Last updated: 2026-05-29 (post-reorg; QA gap register added; KE decode status updated)

---

## Owner: Me (Prateek) -- Action Required

These items are blocked on my input or approval. Nothing can proceed until actioned.

| # | Item | Why Blocked | Priority |
|---|---|---|---|
| ~~M-1~~ | ~~OG image replaced~~ | -- | ✅ DONE -- replaced 2026-05-20, <82KB 1200×630 |
| ~~M-2~~ | ~~Legal pages compliance refresh~~ | -- | ✅ DONE -- seed run 2026-05-20, 5 policies updated in production |
| ~~M-3~~ | ~~**KP production smoke test**~~ -- ✅ **CLEARED 2026-05-15.** Report excellent. Premium gate confirmed working. Two findings fed into KP-2A scope: (a) section box re-alignment needed, (b) share card + download not yet present in module -- both in KP-2A brief. KP-2A now unblocked. | ~~Blocks KP-2A integration~~ | ✅ DONE |
| ~~M-4~~ | ~~**Strategist 22 records approval sign-off**~~ -- ✅ **CLEARED 2026-05-15.** All 22 records (IDs 1011-1020 + 1126-1137) confirmed ingested and live. `strategist_engine.py` does not filter on `approval_status` -- pending_human_review has zero functional effect. STR-1 is unblocked. | ~~Blocks STR-1 integration~~ | ✅ DONE |
| M-5 | **WhatsApp** -- complete OTP verification for +91 96431 10001 in WhatsApp Manager + add payment method to WABA on Meta | WhatsApp notifications blocked | 🟡 MED |
| M-6 | **Instagram Business Account ID** -- not loading in Meta dashboard. Resolve to enable Instagram posting from Admin Console | Instagram posting blocked | 🟡 MED |
| M-7 | **react-snap vs helmet-async** -- design decision on pre-render strategy. Await SEO-1 thread findings before deciding | SEO-1 thread will recommend | 🟢 LOW |
| M-8 | **Service worker** -- decide if PWA offline caching is in scope. Await SEO-1 thread | SEO-1 thread scope | 🟢 LOW |
| M-9 | **App.js lazy audit** -- confirm: keep Landing + DailyHoroscope + Login eager, lazy-load the rest? | Minor perf gain; not blocking | 🟢 LOW |
| M-10 | **MODULE_ARC_ANGEL doc audit** -- only 3 files present post-cleanup. Verify whether additional docs (specs, QA notes, handoff notes, source maps) should be migrated from `Codex_Deliveries/Arc_Angel/` into the module home. | Reconciliation gap found 2026-05-15 | 🟢 LOW |
| M-11 | **MODULE_LAL_KITAB doc audit** -- only 3 files present post-cleanup (created 2026-05-15). Verify whether additional docs should migrate from `Codex_Deliveries/LK/` into the module home. | Reconciliation gap found 2026-05-15 | 🟢 LOW |
| M-12 | **MODULE_SEO_WEB_PERFORMANCE doc audit** -- only 3 files present post-cleanup (created 2026-05-15). Verify whether additional docs should migrate from `Codex_Deliveries/SEO/` into the module home. | Reconciliation gap found 2026-05-15 | 🟢 LOW |
| M-13 | **Live TV console polish (LTV-OP-1)** -- player console bar on `/live-sai-baba-arti` functional but visual design does not match original spec intent. Raise as Codex commission when final design is confirmed. | Design decision needed from TT | 🟡 MED |
| M-15 | **TAR-SEO-1 integration** -- Tarot SEO 199-page module is build-verified locally. TT to integrate from `Codex_Deliveries/Tarot/` | Blocking Tarot SEO from going live | 🔴 HIGH |
| M-16 | **LSG-1 integration** -- Lo Shu Grid full module delivered locally. TT to integrate from `Codex_Deliveries/Lo_Shu_Grid/` | Blocking Lo Shu Grid from going live | 🟠 HIGH |
| M-17 | **KE-OP-15** -- Verify KE questionnaire live endpoints on Render: `/questionnaire`, `/api/knowledge-engine/questionnaire/profile`, `/api/knowledge-engine/questionnaire/submit`; confirm `user_questionnaire_profiles` writes in MongoDB | KE-IQ integration sign-off pending | 🟠 HIGH |
| M-18 | **LON-OP-2** -- Longevity preview API at `/api/longevity/generate` takes ~46s. Profile + optimise to bring under 10s contract target | Performance gap flagged in QA audit | 🟠 HIGH |
| M-19 | **ANGEL-OP-1** -- Re-seed Angel Numbers Mongo collections with ANGEL-2 rewrite content: run `seed_angel_numbers_core.py` + `seed_angel_numbers_intents.py` | ANGEL-2 quality fix not live in production | 🟠 HIGH |
| M-20 | **ECHO-UI-1** -- Deploy ECHO/PACE admin frontend: `EchoPaceTab.jsx` + `AdminDashboard.jsx` changes not in current production bundle | ECHO/PACE admin unreachable in production | 🟠 HIGH |
| M-21 | **SHC-UI-1** -- Verify Self-Healing Center "Self-Heal" tab live in Admin Console. `DiagnosticsTab.jsx` IS imported (line 25) + rendered (line 742) in `AdminDashboard.jsx` with 4 SHC strings confirmed -- QA audit finding was stale. TT to confirm tab visible at `/admin/dashboard` on current Vercel deploy. | Confirm tab visible in production; no code change needed | 🟡 MED |
| M-22 | **SHC-OPS-1** -- Configure 5 Render env vars for Gmail/GST: `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`, `SUPPORT_EMAIL`, `BUSINESS_STATE`, then run Gmail OAuth flow | GST + Gmail scheduler jobs blocked | 🟠 HIGH |
| ~~M-23~~ | ~~**KE-DEDUP-CONTRADICTION-1**~~ -- ✅ **DONE 2026-05-29.** `backend/ke_dedup_script.py` delivered. TF-IDF similarity + contradiction detection + idempotent write-back. 1/1 tests pass. `scikit-learn>=1.3.0` added to `requirements.txt`. | ✅ DONE | ✅ |
| M-24 | **Phaladeepika NLM** -- Begin Adhyaya II decode. Brief at `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_PHALADEEPIKA_NLM.md` | Fully unblocked -- no dependency | 🟡 MED |
| M-25 | **BPHS Vol 1 Thread A** -- Confirm Q1 (Ch11-Ch24 completeness) and Q2 (folder: `BPHS_CC_Decode/` canonical), then continue with Karaka → Yoga → Dasha chapters | Brief at `KE_TEXTBOOK_DECODE/Thread_Briefs/` | 🟡 MED |
| M-26 | **KP Astrology claim_axis pass** -- Retroactive self-audit of all 77 files to populate `claim_axis: "longevity"` on ~20 rules across ~15 files | Near-complete close-out action | 🟡 MED |
| M-27 | **LTV-SCOPE-1** -- Remove `LiveTVPanel` mounts from non-home pages (`Home.jsx`, `PanchangLandingPage.jsx`, `PanchangPage.jsx`). Re-test `/`, `/home`, Panchang routes. | Scope drift from original "home page only" spec | 🟠 HIGH |
| M-28 | **KP-Sprint2 delivery review** -- KP /ask-question LLM router issued 2026-05-15. Chase delivery and integrate when received. | In progress with Codex | 🔴 HIGH |
| ~~M-14~~ | ~~**Render Free → Starter upgrade**~~ -- ✅ **DONE 2026-05-17.** Render now on Starter plan ($7/mo). Server always-on, no more cold starts. API responds in ms for first user of each session. SEO crawlers now get instant 200 responses. | ~~Cold starts hurting UX + SEO~~ | ✅ DONE |

---

## Sitting with Codex -- Active Commissions

All items below have been moved into commission briefs in `Codex_Deliveries/`. Nothing is pending here -- each is either READY TO ISSUE or has a brief written and ready to issue.

### Knowledge Engine Thread
- ~~KE-2A: Yoga Check Evaluation Engine~~ → ✅ INTEGRATED 2026-05-17. 9 handlers added, 52 tests pass, 0 missing mappings, 26 dispatch entries.
- ~~KE-Sprint2: Arbitration Runtime~~ → ✅ INTEGRATED 2026-05-17 (self-certified). All 5 gates passed against live code.
- ~~KE-Sprint3: Arc Angel Computation (G-07/G-08/G-09)~~ → ✅ FULLY COMPLETE 2026-05-17. KE-OP-13 ✅ (live verified) + KE-OP-14 ✅ (AD-level window granularity fixed, commit `c4f4b43`, 72/72 tests).
- ~~KE-IQ: Questionnaire UI + β/γ wiring (TD-19/TD-25/G-10)~~ → ✅ **INTEGRATED 2026-05-18** commit `f7aa78b`. 75/75 KE tests. KE-OP-15 open: TT to verify live endpoints + `user_questionnaire_profiles` persistence on Render.
- ~~KE-DEDUP-CONTRADICTION-1~~ → ✅ **INTEGRATED 2026-05-29.** `backend/ke_dedup_script.py` live. 1/1 tests pass.

**CC Direct Actions -- KE gaps confirmed by Codex intake audit 2026-05-15:**
- [x] **KE-OP-9** -- ✅ Already present: `knowledge_engine.py` lines 634-636 dispatch `yoga_combination` through `ke_yoga_evaluator.evaluate_yoga_check`. No action needed. Confirmed 2026-05-15.
- [x] **KE-OP-10** -- ✅ Fixed 2026-05-15: added `combust_ok` guard to `_planet_in_kendra_conditions_ok` in `ke_yoga_evaluator.py`. `free_from_combustion` now evaluated via `ChartFacts.planet_positions[planet]["combust"]`. `_unsupported_note` cleaned up.
- [x] **KE-OP-11** -- ✅ Done 2026-05-15. `migrate_ch41_varga_checkable.py` run against `horoscope_db`. 24 Ch 41 Varga-tier rules updated: `checkable=True`, `condition_type: varga_dignity_tier`. Summary: updated=24, skipped=0, errors=0.

### KP Oracle Thread
- ~~KP-2A: Bundle editorial + visual share card + Remedies Admin tab~~ → `KP/CODEX_COMMISSION_KP_2A.md` · READY TO ISSUE
- ~~KP-Sprint2: /ask-question LLM Logic Router (Guna + Gita)~~ → `KP/CODEX_COMMISSION_KP_SPRINT2_ASK_QUESTION.md` · READY TO ISSUE
- ~~KP-2B: Ritual Animation + 3-Pillar UX + Astro-Filter~~ → `KP/CODEX_COMMISSION_KP_2B.md` · READY TO ISSUE (depends on KP-2A)

### Individual Reports Thread
- ~~IR-1: 5 public SEO landing pages~~ → `Individual_Reports/CODEX_COMMISSION_IR_1_LANDING_PAGES.md` · READY TO ISSUE
- ~~IR-4: 6 Phase 3 Natal Reports (Wealth/H2 · Romance/H5 · Vitality/H6 · Partnership/H7 · Dharma/H9 · Gains/H11)~~ → `Individual_Reports/CODEX_COMMISSION_IR_4_SIX_NEW_REPORTS.md` · READY TO ISSUE (written 2026-05-18 -- 516 lines, 18 new files)

### Remedies Engine Thread
- ~~REM-P1: Remedies Engine Phase 1 (KP collection + remedy_ref pipeline)~~ → `Remedies/CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md` · READY TO ISSUE

### The Strategist Thread
- ~~STR-1: Premium Landing Page + War Room Visual Rebuild~~ → `Strategist/CODEX_COMMISSION_STRATEGIST_LANDING_WARROOM.md` · READY TO ISSUE
- ~~STR-2J: Strategist Missions UI improvements (MissionCard responsive + dasha display)~~ → `Strategist/CODEX_COMMISSION_STR_2J_MISSIONS_UI.md` · ✅ INTEGRATED commit `9ad2e0a` *(delivered + dasha backend fix 2026-05-15)*

### Arc Angel Thread
- ~~ARC-2: Arc Angel Dynamic Confidence Engine~~ → ✅ **INTEGRATED 2026-05-18** commit `c1a7cb0`. 18 files, 746 insertions, 72/72 tests green. 3-pillar confidence fully wired. Pillar 1 bridge (4-section → 12-domain) is stopgap pending KE-IQ enrichment. Decay engine + notification hooks live. ArcAngelPanel rebuilt. PrivateRoute applied.

### Tarot Thread
- ~~TAR-v4: Tarot UI v4 Enhancement~~ → `Tarot/CODEX_COMMISSION_TAROT_V4_UI.md` · READY TO ISSUE

### Kundali Thread
- ~~KUN-1: Lagna Kundali Module Contract~~ → `Kundali/CODEX_COMMISSION_KUNDALI_LAGNA_CONTRACT.md` · READY TO ISSUE

### Lal Kitab Thread
- ~~LK-1: LK Standalone Module~~ → `LK/CODEX_COMMISSION_LK_STANDALONE_MODULE.md` · READY TO ISSUE

### Longevity Thread
- ~~LON-1: Ayur Jyotish Longevity Report~~ → `Longevity/CODEX_COMMISSION_LONGEVITY_REPORT_CONTRACT.md` · READY TO ISSUE

### Panchang Thread
- ~~PAN-L1: Language/Regional Pages (Tamil, Telugu, Malayalam, etc.)~~ → `Panchang/CODEX_COMMISSION_PANCHANG_LANGUAGE_PAGES.md` · READY TO ISSUE

### SEO & Web Performance Thread
- ~~SEO-1: SEO + Marketing + Web Performance Optimisation~~ → `SEO/CODEX_COMMISSION_SEO_WEBPERF.md` · READY TO ISSUE
- ~~SEO items deferred: SEO·1 through SEO·6, PERF·4/5/7/8~~ → absorbed into SEO-1 commission

### World Oracles Thread (Phase 3)
- ~~ORACLE-P3: 5 Multi-Scriptural Oracle Modules + Guna-Meter (Bible, Islamic, Taoist, Greek, Sikh)~~ → `World_Oracles/CODEX_COMMISSION_ORACLE_P3_WORLD_ORACLES.md` · READY TO ISSUE *(written 2026-05-15 -- Phase 3, LOW)*

---

## Done by Claude Code -- No Commission Needed

Small direct fixes completed in-session. No Codex thread required.

| Item | Status | Commit |
|---|---|---|
| Punya Rewards earn hooks -- 7 pages (Daily/Weekly/Monthly Horoscope, Tarot, Numerology, BirthChart, Panchang) | ✅ Done | This session |
| Arc Angel `isPremium` -- already correct (`user?.is_premium ?? false`) | ✅ Confirmed -- was a false alarm | -- |
| Punya Rewards + Live TV router registration in server.py | ✅ Confirmed -- already wired | -- |
| `ArcAngelPanel.jsx` API amendments (subscription, birth data source, birth_place param) | ✅ Done | `c01ec8d` |

### Still to do (Claude Code direct -- small, no commission)
- ~~🔧 **`/api/remedies/ref/{remedy_ref_id}` endpoint**~~ -- ✅ Already present at `remedies_router.py` line 827. Confirmed live 2026-05-15. Was a false alarm.
- ~~🔧 **KP Saved Previous Readings not loading** (KP-OP-8)~~ -- ✅ Fixed commit `80238a5`. Broken `window.scrollTo({top:0})` in `loadPastReading` was scrolling user away from the Guidance Report before React rendered it. Replaced with `useRef` + `useEffect` scroll-into-view.

---

## Phase 2 / Phase 3 Parking Lot -- Not Yet Actioned

Items confirmed deferred. Not in any active commission. Will be picked up in future planning sessions.

| Item | Phase | Priority | Thread |
|---|---|---|---|
| Commission J -- World Context Engine (macro α signals: conflict zones, festivals, exam periods) | Phase 2 | 🟢 LOW | KE / Commission J |
| ~~Arc Angel: persist `user_arc_angel_profile` in MongoDB (currently stateless)~~ | ✅ DONE 2026-05-17 | KE-Sprint3 built the full persistence layer -- schema, upsert, 6h cache, GET route. No longer parking lot. |
| TD-26 Country Kundali as Alpha Signal | Phase 2 | 🟡 MED | KE |
| TD-27 Forecast Tier / Life Area Outlook | Phase 2 | 🟡 MED | KE |
| KP-G7 Audio soundscapes (binaural + Sanskrit chanting) | Phase 3 | 🟢 LOW | KP |
| KP-G8 Spiritual Journal UX (beyond reading history) | Phase 3 | 🟢 LOW | KP |
| KP-G9 Panchapakshi bird state timing layer in KP | Phase 3 | 🟢 LOW | KP |
| KP-G12 Guna-Meter gamification (Tamas/Rajas/Sattva progress bar) | Phase 3 | 🟢 LOW | KP / ORACLE-P3 |
| KP-G13 krishna_answer ≠ title audit (slot-level editorial verify) | Phase 2 | 🟡 MED | KP-2A (flagged) |
| KP 20-category onboarding expansion (currently 5 categories) | Phase 2 | 🟡 MED | KP |
| Slot 33 → LK Debt Audit cross-module trigger (PRAY verdict → surfaces Debt Audit) | Phase 2 | 🟡 MED | KP / LK |
| Lumina v2 tab-by-tab audit before changes | Phase 2 | 🟡 MED | -- |
| Razorpay live keys | When Play Store ready | 🟡 MED | -- |
| Scheduled daily social posts (6 AM auto-post to FB + YT) | Phase 2 | 🟢 LOW | Notifications |
