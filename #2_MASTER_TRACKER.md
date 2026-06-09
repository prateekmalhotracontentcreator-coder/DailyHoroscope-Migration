# Temple Tracker -- Master Index
> EverydayHoroscope · Module Status Dashboard
> **Read this at session start. Then open the individual module tracker for the module you are working on.**
> Last updated: 2026-06-09 v7.5 (Growth #26 added: GRW-1→SOCIAL-1 CC-verified, TT live validation pending 8 Render env vars. KE: 5 Layer B architectural rulings locked. KE-OP-18 🔴 CRITICAL: KP condition types (`kp_planet_signification`/`kp_star_lord`/`kp_csl`) not implemented in `_condition_matches` -- entire KP corpus returns False. Script updated to include PHR rules (~10,234 total). KE-OP-19/20/21 opened.)

---

## How Module Trackers Work

Each module has its own tracker file at:
```
Codex_Deliveries/[Module]/TRACKER.md
```

Each tracker contains: **Current Status · Commission Status · Open Points (owner + priority) · Version History**

**Updating rule:** At the end of every session, update the tracker for every module touched -- add a version history row, update open points, change status badge if applicable.

**Owner codes:** `TT` = Temple Team (Prateek) · `CC` = Claude Code · `CX` = Codex thread

---

## Status Key

| Badge | Meaning |
|---|---|
| `✅ LIVE` | Complete and in production, no open commissions |
| `🟡 ACTIVE` | Live but commission(s) open or pending |
| `🔴 CRITICAL` | Blocking issue -- must resolve before other work |
| `🟣 PLANNED` | Brief written, not yet issued to Codex |
| `⛔ BLOCKED` | Cannot proceed -- hard dependency unmet |

---

## Module Dashboard

| # | Module | Tracker | Status | Hottest Open Point | Owner |
|---|---|---|---|---|---|
| 1 | Knowledge Engine | [`Knowledge_Engine/TRACKER.md`](Codex_Deliveries/Knowledge_Engine/TRACKER.md) | 🟡 ACTIVE | **DB ~12,095 total · auto_approved ~5,892 · flagged ~995 · rejected ~112.** Phase 4B script ✅ BUILT (10,234-rule corpus). **🔴 KE-OP-18 CRITICAL: `kp_planet_signification`/`kp_star_lord`/`kp_csl` not in `_condition_matches` -- KP corpus returns False unconditionally. Engine change needed before Layer B is meaningful.** KE-OP-19 (dasha-gate audit) · KE-OP-20 (secondary_axis schema) · KE-OP-21 (composite audit). 5 architectural rulings locked. Layer C LLM-as-Judge mandatory before KE-OP-4. | TT/CC |
| 2 | KP Oracle | [`KP/TRACKER.md`](Codex_Deliveries/KP/TRACKER.md) | 🟡 ACTIVE | KP-Sprint2 ✅ INTEGRATED `20d4d29` (AskQuestionPage, 60-route logic router, ask endpoint). KP-2B ✅ INTEGRATED `20f7b83` (ritual screen, 3-pillar UX, astro enrichment). **KP-OP-10: Share card format needs redesign. KP-OP-11: Report structure UX review. TT to verify both deliveries on production (acceptance checklists).** | TT |
| 3 | Individual Reports | [`Individual_Reports/TRACKER.md`](Codex_Deliveries/Individual_Reports/TRACKER.md) | 🟣 PLANNED | IR-1 ready to issue Week 1 -- no dependency | TT |
| 4 | Remedies Engine | [`Remedies/TRACKER.md`](Codex_Deliveries/Remedies/TRACKER.md) | 🟡 ACTIVE | `/api/remedies/ref/{id}` confirmed live. `krishna_prashnavali_remedies` seeded (36 records). REM-P1 ready to issue. | TT |
| 5 | The Strategist | [`Strategist/TRACKER.md`](Codex_Deliveries/Strategist/TRACKER.md) | 🟡 ACTIVE | **`036005b` 2026-06-07**: Birth data auto-seed (Dasha+Shadbala unblocked for Birth Chart users) + KP detail blank panel hidden. All audit CCs complete. TT verify: STR-OP-5/24/25/29. KP chain (sub-lord/sig/cuspal) pending STR-2A2 commission. | TT |
| 6 | Arc Angel | [`Arc_Angel/TRACKER.md`](Codex_Deliveries/Arc_Angel/TRACKER.md) | 🟡 ACTIVE | **ARC-2 ✅ INTEGRATED** commit `c1a7cb0` 2026-05-18. 3-pillar confidence live, decay engine active, ArcAngelPanel rebuilt. Pillar 1 bridge (4-section → 12-domain) is a stopgap -- KE-IQ will deliver full 12-area questionnaire. | TT |
| 7 | Tarot | [`Tarot/TRACKER.md`](Codex_Deliveries/Tarot/TRACKER.md) | 🟢 QA-CLEARED | TAR-v4 ✅ · TAR-SEO-1 ✅ integrated `8f36fc8` · TAR-SEO-2 ✅ QA-CLEARED `cc52900` · 199 pages live · ECHO/PACE strict full pass (L1-L3 + Layer G 15/15 PASS 0% dup) · **TAR-SEO-3 READY TO ISSUE** (4,621 card×spread combination pages -- brief at `Tarot/CODEX_COMMISSION_TAR_SEO_3_COMBINATIONS.md`) | TT |
| 8 | Kundali / Birth Chart | [`Kundali/TRACKER.md`](Codex_Deliveries/Kundali/TRACKER.md) | 🟡 ACTIVE | KUN-1 integrated `1d6fc47`. Public `/kundali` free route, unknown birth time, House Summary table, User Manual. **KUN-OP-4: TT browser smoke test `/kundali` in production.** | TT |
| 9 | Lal Kitab | [`LK/TRACKER.md`](Codex_Deliveries/LK/TRACKER.md) | 🟣 PLANNED | LK-1 ready to issue Week 4+ | TT |
| 10 | Longevity Report | [`Longevity/TRACKER.md`](Codex_Deliveries/Longevity/TRACKER.md) | 🟡 ACTIVE | LON-1 integrated `2a4ed4e` -- backend aliases `/report`,`/save`,`/my-reports`,`/alerts`,`/report/:id` + LongevityReportPage. **LON-OP-1: TT live review of save/detail flow required.** | TT |
| 11 | Love & Engagement | [`Love_Module/TRACKER.md`](Codex_Deliveries/Love_Module/TRACKER.md) | ✅ LIVE | Nothing open | -- |
| 12 | Live TV | [`Live_TV/TRACKER.md`](Codex_Deliveries/Live_TV/TRACKER.md) | 🟡 ACTIVE | LTV-OP-1: console polish deferred. Panel live on Home (logged-in) + PanchangPage. Render Starter activated. | TT |
| 13 | Punya Rewards | [`Punya_Rewards/TRACKER.md`](Codex_Deliveries/Punya_Rewards/TRACKER.md) | 🟡 ACTIVE | PUN-2 integrated `2a4ed4e` -- Landing promo, SVG wheel, streak, grouped ledger. **PUN-OP-1: `individual_report` action code missing from `DEFAULT_ACTION_RULES` -- backend fix needed before that hook can be wired.** | TT |
| 14 | Notifications | [`Notifications/TRACKER.md`](Codex_Deliveries/Notifications/TRACKER.md) | 🟡 ACTIVE | M-5 WhatsApp OTP + M-6 Instagram Business ID | TT |
| 15 | Panchang | [`Panchang/TRACKER.md`](Codex_Deliveries/Panchang/TRACKER.md) | 🟡 ACTIVE | PAN-L1 ✅ · **PAN-TM-1 ✅ INTEGRATED `ae3b683` 2026-06-05** -- The Cosmic Clock: parchment scroll, magnifying lens, window pills, limb rows, guidance bar. Light theme only. **PAN-OP-5: TT smoke test `/panchang/today` on production.** | TT |
| 16 | SEO & Web Performance | [`SEO/TRACKER.md`](Codex_Deliveries/SEO/TRACKER.md) | 🟡 ACTIVE | SEO-20K M1 ✅ · M2 ✅ · M3 ✅ · **M4 (TAR-SEO-1/2) ✅ QA-CLEARED 2026-05-30** -- 199 Tarot SEO pages live, ECHO/PACE strict + Layer G full pass. M5 (FAITH-20K) → brief at `Faith_Hubs/CODEX_COMMISSION_FAITH_20K.md` -- READY TO ISSUE. **SEO-LP-1 ✅ INTEGRATED 2026-06-09** (9 module landing pages: Birth Chart, Kundali Milan, Brihat Kundli, KP Oracle, Palmistry, Arc Angel, Ritual Engine, Lumina, Numerology) -- `ModuleLandingPage.jsx` shared frame, all 9 Playwright smoke tests PASS, pending deploy. | TT |
| 17 | World Oracles | [`World_Oracles/TRACKER.md`](Codex_Deliveries/World_Oracles/TRACKER.md) | 🟣 PLANNED | Phase 3 -- do not issue until KP Oracle 30+ days live | TT |
| 18 | Lo Shu Grid | [`Lo_Shu_Grid/TRACKER.md`](Codex_Deliveries/Lo_Shu_Grid/TRACKER.md) | ✅ COMPLETE | LSG-1 + LSG-2 fully live · 57 URLs · seeded · smoke tested · ECHO/PACE L1-L3 + Layer G all PASS · NavBar wired · all open points closed. | -- |
| 19 | Rudraksha | [`Rudraksha/TRACKER.md`](Codex_Deliveries/Rudraksha/TRACKER.md) | ✅ LIVE | RUD-L2 ✅ · ECHO/PACE all 4 layers PASS (L1 ≤25.2%, L2 0, L3 0, Layer G 0/8) · 6 App.js routes wired · 62 Mongo docs seeded (mukhis/planets/problems/signs) · **TT: smoke test `/rudraksha` on production** | CC |
| 20 | Crystal Healing | [`Crystal_Healing/TRACKER.md`](Codex_Deliveries/Crystal_Healing/TRACKER.md) | 🟡 ACTIVE | CRY-L3 partial delivery: Crystal L1 32.1%, Intention 38.6%, L2 FAIL, L3 PASS. **CRY-L3-CONT READY TO ISSUE** -- 3 fixed-phrase functions (90%/58%/80% repeat) + healing_properties prose. Brief: `CODEX_COMMISSION_CRY_L3_CONTINUATION.md`. | TT |
| 21 | Faith & Scripture | [`Faith_Hubs/TRACKER.md`](Codex_Deliveries/Faith_Hubs/TRACKER.md) | 🔴 CRITICAL | Pass 3 NOT accepted: GITA 96.22%, BIBLE 77.47%, TRANSIT 79.33%, DAILY 68.76% -- all L1/L2 FAIL. **Pass 4 brief written 2026-06-05** -- root cause: `_gita_hook`/`_gita_application` use multi-word situation constants verbatim (hidden_fear/practice_shift/action_focus) → fix: replace with `sit_vocab` single tokens. BIBLE: `transition['faith_need']`/`core_pain` → single tokens. TRANSIT: modulus 6→12 (+6 variants per function). DAILY: sign vocab reduction + month fills + modulus 4→8. Brief: `FAITH_REWRITE_PASS4_BRIEF.md` in staging worktree. Do NOT seed any Faith collections. | CC/TT |
| 22 | Angel Numbers | [`Angel_Numbers/TRACKER.md`](Codex_Deliveries/Angel_Numbers/TRACKER.md) | ✅ COMPLETE | All 6 sign-off gates PASSED 2026-06-04. ECHO/PACE L1-L3 ✅ (worst 39.9%), Copyright ✅ (0 breaches vs Kyle Gray + Fortuna Noir), Seed ✅ (1,000 + 9,000 docs), API ✅, Browser ✅, Layer G Serper ✅ (10/10 PASS, 0 hits). 10,001 pages cleared. Full audit: `TEST_RESULTS_2026-06-04.md`. | -- |
| 23 | SEO-20K M3 Fix (Character Placements + Transit Profiles) | [`SEO/`](Codex_Deliveries/SEO/) | 🔴 CRITICAL | v4 NOT accepted: L1 70.4%, L2 FAIL (new violation: line 789 personal-impact FAQ fully fixed skeleton on all 108 pages). **M3-TR-FIX v5 READY TO ISSUE** -- 1 line fix: `personal_impact_answers` hash-selected pool replacing line 789. Brief: `CODEX_COMMISSION_M3_TR_FIX_V5.md`. | CC/TT |
| 24 | SEO-20K M2 Fix (Sign Compatibility) | [`SEO/`](Codex_Deliveries/SEO/) | ⚠️ FLAGGED | ECHO/PACE 2026-05-31: **L1=50.0% on gate** (must go below 50%). L2 FAIL (koota narrative boilerplate). **M2-COMPAT-FIX READY TO ISSUE.** Brief: `Codex_Deliveries/SEO/CODEX_COMMISSION_M2_COMPAT_FIX.md`. | CC/TT |
| 25 | Tarot SEO Fix | [`SEO/`](Codex_Deliveries/SEO/) | ⚠️ FLAGGED | v4 NOT accepted: all L1 holding (Spreads 43.8%, Cards 34.8%, Intentions 16.3%). Remaining: Spreads L2 (raw `spread["use"]` in FAQ line 1764 at 30% + q3 variant 2 at 17%), Cards L3 (scan's `_card_title()` ignores `meta_title`, must change to use it), Intentions L2 (int_q1 variant 7 line 2827 at 35%). **TAR-SEO-FIX v5 READY TO ISSUE** -- 4 fixes (scan script + 3 data lines). Brief: `CODEX_COMMISSION_TAR_SEO_FIX_V5.md`. | CC/TT |
| 26 | Growth (Transit Segmentation, Email Lifecycle, Intelligence Dashboard, Sales CRM, Instagram+X) | [`Growth/TRACKER.md`](Codex_Deliveries/Growth/TRACKER.md) | 🟡 ACTIVE | **GRW-1 through SOCIAL-1 ✅ CC-VERIFIED 2026-06-08** (17/17 structural checks pass). All 5 commissions locally build-verified. **TT: add 8 Render env vars to unlock live validation** (`SERPER_API_KEY`, `GSC_CLIENT_ID/SECRET`, `INSTAGRAM_BUSINESS_ACCOUNT_ID`, 4 `TWITTER_*` keys). Ads/B2B API Widget → Phase 2. | TT |

---

## Cross-Cutting Temple Team Actions

| ID | Item | Priority | Status |
|---|---|---|---|
| ~~M-1~~ | ~~Replace OG image -- 1200×630 PNG ≤80 KB (`frontend/public/og-image.png`)~~ | ✅ DONE | Replaced 2026-05-20. <82KB, 1200×630. |
| ~~M-2~~ | ~~Run refreshed `seed_policies_v1.py` on Render (`--mongo-url "$MONGO_URL" --db-name horoscope_db`) to update legal wording (Razorpay, Google Analytics, cookie controls, 7-day unused-service refund terms)~~ | ✅ DONE | Seed run 2026-05-20. 5 policies updated in production MongoDB. |
| ~~M-3~~ | ~~KP Oracle end-to-end production smoke test~~ | ✅ DONE | Cleared 2026-05-15. KP-2A unblocked. |
| ~~M-4~~ | ~~Strategist 22 records sign-off~~ | -- | ✅ CLEARED 2026-05-15 |
| M-5 | WhatsApp OTP + payment method on WABA Meta | 🟡 MED | Open |
| M-6 | Instagram Business Account ID -- not loading in Meta dashboard | 🟡 MED | Open |
| M-7 | react-snap vs helmet-async design decision | 🟢 LOW | Await SEO-1 recommendation |
| M-8 | PWA offline caching decision | 🟢 LOW | Await SEO-1 |
| M-9 | App.js lazy audit sign-off | 🟢 LOW | Non-blocking |
| M-10 | **Approve LK decoded rules in `knowledge_rules` collection** -- Admin → Remedies tab → review + approve Ch25/Ch26 decoded rules so they flow through the Remedies Engine to users | 🟠 HIGH | Blocker for REM-P1 delivering LK remedies in KP Oracle + other modules. TT to review and approve/flag each rule. |

---

## Recommended Commission Issue Order

```
Week 1 (NOW):
  ~~KE-Sprint2~~  ✅ ISSUED 2026-05-15
  ~~KE-2A~~       ✅ ISSUED 2026-05-15
  KP-Sprint2   🟠 HIGH -- independent, no dependency
  IR-1         🟠 HIGH -- pure frontend, zero dependency

Week 2:
  KP-2A        ✅ ALL BLOCKERS CLEARED -- issue now (brief updated 2026-05-15)
  KE-IQ        ideally after Sprint 2 gate; can run parallel
  REM-P1       remedies endpoint confirmed live + collection seeded -- issue now
  ARC-2        after KE Sprint 2 ideally

Week 3:
  KP-2B        after KP-2A delivered
  TAR-v4       independent
  PAN-L1       independent

Week 4+:
  KUN-1  ·  LK-1  ·  LON-1 (after KE Sprint 2 gate)  ·  SEO-1 (issue last)

Phase 3:
  ORACLE-P3 -- only after KP live 30+ days + content packs prepared by TT
```

---

*Full commission registry → `Codex_Deliveries/INDEX.md`*
*Commission queue + priorities → `Codex_Deliveries/List_of_Pending_Codex_Commissions.md`*
*5-line module orientation briefs → `Codex_Deliveries/MODULE_BRIEFS.md`*
*Temple Team action items → `Action Items_ Claude Code.md`*
