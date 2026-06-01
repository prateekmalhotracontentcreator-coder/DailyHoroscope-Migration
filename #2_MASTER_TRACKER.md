# Temple Tracker -- Master Index
> EverydayHoroscope · Module Status Dashboard
> **Read this at session start. Then open the individual module tracker for the module you are working on.**
> Last updated: 2026-05-31 v5.1 (session 12 complete -- Full ECHO/PACE scan cycle done for all 15 delivered SEO module types. 8 fix commissions READY TO ISSUE: ANGEL-3, RUD-L2, CRY-L2, FAITH-REWRITE, M3-CP-FIX, M3-TR-FIX, M2-COMPAT-FIX, TAR-SEO-FIX. Brief files in `Codex_Deliveries/SEO/`. SEO_TRACKER.md updated to v5.3.)

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
| 1 | Knowledge Engine | [`Knowledge_Engine/TRACKER.md`](Codex_Deliveries/Knowledge_Engine/TRACKER.md) | 🟡 ACTIVE | KE-IQ ✅ INTEGRATED commit `f7aa78b` 2026-05-18. 75/75 tests. **KE-OP-15 open: TT to verify `POST /api/knowledge-engine/questionnaire/submit`, `GET /api/knowledge-engine/questionnaire/profile`, Arc Angel β/γ enrichment, and `user_questionnaire_profiles` persistence on Render.** KE-OP-4 (rule approval) open. | TT |
| 2 | KP Oracle | [`KP/TRACKER.md`](Codex_Deliveries/KP/TRACKER.md) | 🟡 ACTIVE | KP-Sprint2 ✅ INTEGRATED `20d4d29` (AskQuestionPage, 60-route logic router, ask endpoint). KP-2B ✅ INTEGRATED `20f7b83` (ritual screen, 3-pillar UX, astro enrichment). **KP-OP-10: Share card format needs redesign. KP-OP-11: Report structure UX review. TT to verify both deliveries on production (acceptance checklists).** | TT |
| 3 | Individual Reports | [`Individual_Reports/TRACKER.md`](Codex_Deliveries/Individual_Reports/TRACKER.md) | 🟣 PLANNED | IR-1 ready to issue Week 1 -- no dependency | TT |
| 4 | Remedies Engine | [`Remedies/TRACKER.md`](Codex_Deliveries/Remedies/TRACKER.md) | 🟡 ACTIVE | `/api/remedies/ref/{id}` confirmed live. `krishna_prashnavali_remedies` seeded (36 records). REM-P1 ready to issue. | TT |
| 5 | The Strategist | [`Strategist/TRACKER.md`](Codex_Deliveries/Strategist/TRACKER.md) | 🟢 PHASE 2 INTEGRATED | Phase 2 all 7 CD components integrated (STR-OP-8 through STR-OP-13 ✅). `StrategistActionPlanPage.jsx` rebuilt as 2G composition shell. Pending: commit to main + STR-OP-15 TT verification across modes. STR-OP-3: DashaTimingBar live data verify still open. | TT + CC |
| 6 | Arc Angel | [`Arc_Angel/TRACKER.md`](Codex_Deliveries/Arc_Angel/TRACKER.md) | 🟡 ACTIVE | **ARC-2 ✅ INTEGRATED** commit `c1a7cb0` 2026-05-18. 3-pillar confidence live, decay engine active, ArcAngelPanel rebuilt. Pillar 1 bridge (4-section → 12-domain) is a stopgap -- KE-IQ will deliver full 12-area questionnaire. | TT |
| 7 | Tarot | [`Tarot/TRACKER.md`](Codex_Deliveries/Tarot/TRACKER.md) | 🟢 QA-CLEARED | TAR-v4 ✅ · TAR-SEO-1 ✅ integrated `8f36fc8` · TAR-SEO-2 ✅ QA-CLEARED `cc52900` · 199 pages live · ECHO/PACE strict full pass (L1-L3 + Layer G 15/15 PASS 0% dup) · **TAR-SEO-3 READY TO ISSUE** (4,621 card×spread combination pages -- brief at `Tarot/CODEX_COMMISSION_TAR_SEO_3_COMBINATIONS.md`) | TT |
| 8 | Kundali / Birth Chart | [`Kundali/TRACKER.md`](Codex_Deliveries/Kundali/TRACKER.md) | 🟡 ACTIVE | KUN-1 integrated `1d6fc47`. Public `/kundali` free route, unknown birth time, House Summary table, User Manual. **KUN-OP-4: TT browser smoke test `/kundali` in production.** | TT |
| 9 | Lal Kitab | [`LK/TRACKER.md`](Codex_Deliveries/LK/TRACKER.md) | 🟣 PLANNED | LK-1 ready to issue Week 4+ | TT |
| 10 | Longevity Report | [`Longevity/TRACKER.md`](Codex_Deliveries/Longevity/TRACKER.md) | 🟡 ACTIVE | LON-1 integrated `2a4ed4e` -- backend aliases `/report`,`/save`,`/my-reports`,`/alerts`,`/report/:id` + LongevityReportPage. **LON-OP-1: TT live review of save/detail flow required.** | TT |
| 11 | Love & Engagement | [`Love_Module/TRACKER.md`](Codex_Deliveries/Love_Module/TRACKER.md) | ✅ LIVE | Nothing open | -- |
| 12 | Live TV | [`Live_TV/TRACKER.md`](Codex_Deliveries/Live_TV/TRACKER.md) | 🟡 ACTIVE | LTV-OP-1: console polish deferred. Panel live on Home (logged-in) + PanchangPage. Render Starter activated. | TT |
| 13 | Punya Rewards | [`Punya_Rewards/TRACKER.md`](Codex_Deliveries/Punya_Rewards/TRACKER.md) | 🟡 ACTIVE | PUN-2 integrated `2a4ed4e` -- Landing promo, SVG wheel, streak, grouped ledger. **PUN-OP-1: `individual_report` action code missing from `DEFAULT_ACTION_RULES` -- backend fix needed before that hook can be wired.** | TT |
| 14 | Notifications | [`Notifications/TRACKER.md`](Codex_Deliveries/Notifications/TRACKER.md) | 🟡 ACTIVE | M-5 WhatsApp OTP + M-6 Instagram Business ID | TT |
| 15 | Panchang | [`Panchang/TRACKER.md`](Codex_Deliveries/Panchang/TRACKER.md) | ✅ LIVE | PAN-L1 integrated `2a4ed4e` -- 5 language pages (Hindi/Tamil/Telugu/Malayalam/Kannada), hreflang, JSON-LD. HTTP 200 confirmed. | -- |
| 16 | SEO & Web Performance | [`SEO/TRACKER.md`](Codex_Deliveries/SEO/TRACKER.md) | 🟡 ACTIVE | SEO-20K M1 ✅ · M2 ✅ · M3 ✅ · **M4 (TAR-SEO-1/2) ✅ QA-CLEARED 2026-05-30** -- 199 Tarot SEO pages live, ECHO/PACE strict + Layer G full pass. M5 (FAITH-20K) → brief at `Faith_Hubs/CODEX_COMMISSION_FAITH_20K.md` -- READY TO ISSUE. | TT |
| 17 | World Oracles | [`World_Oracles/TRACKER.md`](Codex_Deliveries/World_Oracles/TRACKER.md) | 🟣 PLANNED | Phase 3 -- do not issue until KP Oracle 30+ days live | TT |
| 18 | Lo Shu Grid | [`Lo_Shu_Grid/TRACKER.md`](Codex_Deliveries/Lo_Shu_Grid/TRACKER.md) | ✅ COMPLETE | LSG-1 + LSG-2 fully live · 57 URLs · seeded · smoke tested · ECHO/PACE L1-L3 + Layer G all PASS · NavBar wired · all open points closed. | -- |
| 19 | Rudraksha | [`Rudraksha/TRACKER.md`](Codex_Deliveries/Rudraksha/TRACKER.md) | ✅ LIVE | RUD-L2 ✅ · ECHO/PACE all 4 layers PASS (L1 ≤25.2%, L2 0, L3 0, Layer G 0/8) · 6 App.js routes wired · 62 Mongo docs seeded (mukhis/planets/problems/signs) · **TT: smoke test `/rudraksha` on production** | CC |
| 20 | Crystal Healing | [`Crystal_Healing/TRACKER.md`](Codex_Deliveries/Crystal_Healing/TRACKER.md) | 🔴 BLOCKED | CRY-1 ✅ backend delivered + registered. ECHO/PACE 2026-05-31: **L1 borderline PASS (47.7%)**, L2 FAIL (100% boilerplate), L3 FLAGGED. **CRY-L2 commission READY TO ISSUE.** Routes + seed blocked. ⚠️ CRY-2 + CRY-3 also delivered -- assess if they compound L2 violations. | CC/TT |
| 21 | Faith & Scripture | [`Faith_Hubs/TRACKER.md`](Codex_Deliveries/Faith_Hubs/TRACKER.md) | 🔴 CRITICAL | FAITH-20K ✅ generator delivered. ECHO/PACE 2026-05-31: **Gita L1=100% BLOCKED · Bible L1=82% BLOCKED · Transit L1=100% BLOCKED**. Root cause: fixed situation/topic boilerplate in summary/hook/application fields -- same failure mode as ANGEL-1. **FAITH-REWRITE commission READY TO ISSUE (CRITICAL).** Do NOT seed any Faith collections. | CC/TT |
| 22 | Angel Numbers | [`Angel_Numbers/TRACKER.md`](Codex_Deliveries/Angel_Numbers/TRACKER.md) | 🔴 BLOCKED | ANGEL-2 ✅ integrated `2271c36`. L1 still fails (45-57%, gate < 40%). **ANGEL-3 READY TO ISSUE** (brief: `Angel_Numbers/CODEX_COMMISSION_ANGEL_3_L1_FIX.md`). Seed blocked until ANGEL-3 passes. | CC/TT |
| 23 | SEO-20K M3 Fix (Character Placements + Transit Profiles) | [`SEO/`](Codex_Deliveries/SEO/) | 🔴 CRITICAL | ECHO/PACE 2026-05-31: Character Placements **L1=93.4% BLOCKED** (worst in scan), Transit Profiles **L1=71.2% BLOCKED**. Both live in production but serving duplicate content. **M3-CP-FIX + M3-TR-FIX READY TO ISSUE.** Briefs: `Codex_Deliveries/SEO/CODEX_COMMISSION_M3_CP_FIX.md` + `M3_TR_FIX.md`. | CC/TT |
| 24 | SEO-20K M2 Fix (Sign Compatibility) | [`SEO/`](Codex_Deliveries/SEO/) | ⚠️ FLAGGED | ECHO/PACE 2026-05-31: **L1=50.0% on gate** (must go below 50%). L2 FAIL (koota narrative boilerplate). **M2-COMPAT-FIX READY TO ISSUE.** Brief: `Codex_Deliveries/SEO/CODEX_COMMISSION_M2_COMPAT_FIX.md`. | CC/TT |
| 25 | Tarot SEO Fix | [`SEO/`](Codex_Deliveries/SEO/) | ⚠️ FLAGGED | ECHO/PACE 2026-05-31: Spreads L2 FAIL ("page reads spread card layout" 100%), Cards L3 FLAGGED (75% same-suit), Intentions L2+L3 FAIL. L1 PASSES all types -- must not regress. **TAR-SEO-FIX READY TO ISSUE.** Brief: `Codex_Deliveries/SEO/CODEX_COMMISSION_TAR_SEO_FIX.md`. | CC/TT |

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
