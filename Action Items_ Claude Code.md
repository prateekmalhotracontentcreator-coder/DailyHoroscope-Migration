# Action Items — Temple App
> Single Source of Truth for all open items across Claude Code sessions.
> Referenced in all handover docs. **Do not create parallel lists elsewhere.**
> Last updated: 2026-05-15

---

## Owner: Me (Prateek) — Action Required

These items are blocked on my input or approval. Nothing can proceed until actioned.

| # | Item | Why Blocked | Priority |
|---|---|---|---|
| M-1 | **OG image** — replace `frontend/public/og-image.png` with proper 1200×630 PNG (~80 KB). Current file is 626 KB at wrong aspect ratio. | SEO + social sharing broken until fixed | 🔴 HIGH |
| M-2 | **Legal pages seed** — run `python3 backend/scripts/seed_policies_v1.py --mongo-url "$MONGO_URL" --db-name horoscope_db` against Render | Legal/Privacy/Terms pages show empty | 🔴 HIGH |
| M-3 | **KP production smoke test** (manual) — verify KrishnaOraclePage end-to-end before opening KP-2A commission integration | Blocks KP-2A integration | 🔴 HIGH |
| ~~M-4~~ | ~~**Strategist 22 records approval sign-off**~~ — ✅ **CLEARED 2026-05-15.** All 22 records (IDs 1011–1020 + 1126–1137) confirmed ingested and live. `strategist_engine.py` does not filter on `approval_status` — pending_human_review has zero functional effect. STR-1 is unblocked. | ~~Blocks STR-1 integration~~ | ✅ DONE |
| M-5 | **WhatsApp** — complete OTP verification for +91 96431 10001 in WhatsApp Manager + add payment method to WABA on Meta | WhatsApp notifications blocked | 🟡 MED |
| M-6 | **Instagram Business Account ID** — not loading in Meta dashboard. Resolve to enable Instagram posting from Admin Console | Instagram posting blocked | 🟡 MED |
| M-7 | **react-snap vs helmet-async** — design decision on pre-render strategy. Await SEO-1 thread findings before deciding | SEO-1 thread will recommend | 🟢 LOW |
| M-8 | **Service worker** — decide if PWA offline caching is in scope. Await SEO-1 thread | SEO-1 thread scope | 🟢 LOW |
| M-9 | **App.js lazy audit** — confirm: keep Landing + DailyHoroscope + Login eager, lazy-load the rest? | Minor perf gain; not blocking | 🟢 LOW |

---

## Sitting with Codex — Active Commissions

All items below have been moved into commission briefs in `Codex_Deliveries/`. Nothing is pending here — each is either READY TO ISSUE or has a brief written and ready to issue.

### Knowledge Engine Thread
- ~~KE-2A: Yoga Check Evaluation Engine (16 evaluator types)~~ → `Knowledge_Engine/CODEX_COMMISSION_KE_2A_YOGA_CHECK.md` · READY TO ISSUE
- ~~KE-Sprint2: Arbitration Runtime (G-03/G-05/G-06/G-04 — ingest freeze active)~~ → `Knowledge_Engine/CODEX_COMMISSION_KE_SPRINT2_ARBITRATION.md` · READY TO ISSUE *(written 2026-05-15)*
- ~~KE-IQ: Questionnaire UI + β/γ wiring (TD-19/TD-25/G-10)~~ → `Knowledge_Engine/CODEX_COMMISSION_KE_IQ_QUESTIONNAIRE_UI.md` · READY TO ISSUE *(written 2026-05-15)*

### KP Oracle Thread
- ~~KP-2A: Bundle editorial + visual share card + Remedies Admin tab~~ → `KP/CODEX_COMMISSION_KP_2A.md` · READY TO ISSUE
- ~~KP-Sprint2: /ask-question LLM Logic Router (Guna + Gita)~~ → `KP/CODEX_COMMISSION_KP_SPRINT2_ASK_QUESTION.md` · READY TO ISSUE
- ~~KP-2B: Ritual Animation + 3-Pillar UX + Astro-Filter~~ → `KP/CODEX_COMMISSION_KP_2B.md` · READY TO ISSUE (depends on KP-2A)

### Individual Reports Thread
- ~~IR-1: 5 public SEO landing pages~~ → `Individual_Reports/CODEX_COMMISSION_IR_1_LANDING_PAGES.md` · READY TO ISSUE

### Remedies Engine Thread
- ~~REM-P1: Remedies Engine Phase 1 (KP collection + remedy_ref pipeline)~~ → `Remedies/CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md` · READY TO ISSUE

### The Strategist Thread
- ~~STR-1: Premium Landing Page + War Room Visual Rebuild~~ → `Strategist/CODEX_COMMISSION_STRATEGIST_LANDING_WARROOM.md` · READY TO ISSUE
- ~~STR-2J: Strategist Missions UI improvements (MissionCard responsive + dasha display)~~ → `Strategist/CODEX_COMMISSION_STR_2J_MISSIONS_UI.md` · ✅ INTEGRATED commit `9ad2e0a` *(delivered + dasha backend fix 2026-05-15)*

### Arc Angel Thread
- ~~ARC-2: Arc Angel Phase 2 — Confidence % lift + questionnaire gating + desktop sidebar~~ → `Arc_Angel/CODEX_COMMISSION_ARC_2_CONFIDENCE_QUESTIONNAIRE.md` · READY TO ISSUE *(written 2026-05-15)*

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
- ~~ORACLE-P3: 5 Multi-Scriptural Oracle Modules + Guna-Meter (Bible, Islamic, Taoist, Greek, Sikh)~~ → `World_Oracles/CODEX_COMMISSION_ORACLE_P3_WORLD_ORACLES.md` · READY TO ISSUE *(written 2026-05-15 — Phase 3, LOW)*

---

## Done by Claude Code — No Commission Needed

Small direct fixes completed in-session. No Codex thread required.

| Item | Status | Commit |
|---|---|---|
| Punya Rewards earn hooks — 7 pages (Daily/Weekly/Monthly Horoscope, Tarot, Numerology, BirthChart, Panchang) | ✅ Done | This session |
| Arc Angel `isPremium` — already correct (`user?.is_premium ?? false`) | ✅ Confirmed — was a false alarm | — |
| Punya Rewards + Live TV router registration in server.py | ✅ Confirmed — already wired | — |
| `ArcAngelPanel.jsx` API amendments (subscription, birth data source, birth_place param) | ✅ Done | `c01ec8d` |

### Still to do (Claude Code direct — small, no commission)
- 🔧 **`/api/remedies/ref/{remedy_ref_id}` endpoint** — missing from `remedies_router.py`. Blocks KP-2A integration. One-file backend fix.

---

## Phase 2 / Phase 3 Parking Lot — Not Yet Actioned

Items confirmed deferred. Not in any active commission. Will be picked up in future planning sessions.

| Item | Phase | Priority | Thread |
|---|---|---|---|
| Commission J — World Context Engine (macro α signals: conflict zones, festivals, exam periods) | Phase 2 | 🟢 LOW | KE / Commission J |
| Arc Angel: persist `user_arc_angel_profile` in MongoDB (currently stateless) | Phase 2 | 🟡 MED | ARC-2 (partially) |
| TD-26 Country Kundali as Alpha Signal | Phase 2 | 🟡 MED | KE |
| TD-27 Forecast Tier / Life Area Outlook | Phase 2 | 🟡 MED | KE |
| KP-G7 Audio soundscapes (binaural + Sanskrit chanting) | Phase 3 | 🟢 LOW | KP |
| KP-G8 Spiritual Journal UX (beyond reading history) | Phase 3 | 🟢 LOW | KP |
| KP-G9 Panchapakshi bird state timing layer in KP | Phase 3 | 🟢 LOW | KP |
| KP-G12 Guna-Meter gamification (Tamas/Rajas/Sattva progress bar) | Phase 3 | 🟢 LOW | KP / ORACLE-P3 |
| KP-G13 krishna_answer ≠ title audit (slot-level editorial verify) | Phase 2 | 🟡 MED | KP-2A (flagged) |
| KP 20-category onboarding expansion (currently 5 categories) | Phase 2 | 🟡 MED | KP |
| Slot 33 → LK Debt Audit cross-module trigger (PRAY verdict → surfaces Debt Audit) | Phase 2 | 🟡 MED | KP / LK |
| Lumina v2 tab-by-tab audit before changes | Phase 2 | 🟡 MED | — |
| Razorpay live keys | When Play Store ready | 🟡 MED | — |
| Scheduled daily social posts (6 AM auto-post to FB + YT) | Phase 2 | 🟢 LOW | Notifications |
