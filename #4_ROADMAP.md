# EverydayHoroscope -- Master Roadmap
> **Single living doc. Update this at every session. Do not create parallel roadmap files.**
> Owner: Prateek Malhotra + Temple Team
> Last updated: 2026-05-29
> Previous: `CODEX_MASTER_ROADMAP.md` (archived) + `RoadMap to Playstore and Live App Razorpay Enablement.md` (Documents folder)

---

## PART A -- Play Store & Revenue Roadmap

### Phase 1A -- Finish & Ship (Play Store Ready)

**Goal: Ship a clean, working, Play Store-ready app with all features already built.**

| # | Item | Status | Owner |
|---|---|---|---|
| 1a | **Premium Report consistency** -- decide hard-coded vs API-call route for Kundali, Brihat Kundali, Kundali Milan | 🟡 Open | TT |
| 1b | **Remedy formula** -- formalise reusable prompt module for Brihat Kundali remedies | 🟡 Open | Codex |
| 1c | **Report structure standard** -- Visual Kundali chart (SVG) + 12-house reading on every premium report | 🟡 Open | Codex (KUN-1) |
| 1d | **My Reports page** -- full build with saved reports; primary mobile UX feature | ✅ DONE | IR thread |
| 1e | **Password-protected PDF downloads** (pypdf) -- `FirstName+BirthYear+Month` formula | 🟡 Open | Codex |
| 2 | **Razorpay live keys** -- switch from test to live, end-to-end payment test on all 3 premium products | ⏸ HOLD | TT |
| 3 | **Admin Panel -- Revenue Intelligence** -- Orders, MRR, top products, refund rate live dashboard | 🟡 Open | Codex |
| 4 | **Admin Panel -- AI Brain Control** -- swap system prompts per engine from admin UI | 🟡 Open | Codex |
| 5 | **Admin Panel -- Cache Dashboard** -- today's horoscope cache by sign, manual trigger, API token usage | 🟡 Open | Codex |
| 6 | **Delete Account option** -- Google Play requirement for any app with account creation | 🟡 Open | Codex |

### Phase 1B -- Pre-Launch Non-Code Actions

| # | Item | Status | Owner |
|---|---|---|---|
| L1 | Payments live mode -- switch to live Razorpay keys, E2E test on Android Chrome + iOS Safari | ⏸ HOLD | TT |
| L2 | Full user journey QA -- Register → horoscope → buy → download on Android + iOS | ⏸ HOLD | TT |
| L3 | Lighthouse audit -- target 90+ on Performance/Accessibility/Best Practices/SEO | ⏸ HOLD | TT + CC |
| L4 | Sentry error monitoring -- frontend + backend; 5xx alerts on Render | 🟡 Open | Codex |
| L5 | 12 sign-specific screenshot cards, content rating, Play Store listing copy | ⏸ HOLD | TT |
| L6 | Delete test subscription doc (`prateekmalhotra20@gmail.com`) before go-live | ⏸ HOLD | TT |
| L7 | Google Play submission -- APK → Play Console → live; Google Pay + UPI compliance | ⏸ HOLD | TT |

### Phase 2 -- Mobile App Launch

| # | Item | Status |
|---|---|---|
| 2a | Android APK via Capacitor (same React frontend, minimal code change) | ⏸ HOLD |
| 2b | Push notifications via Firebase Cloud Messaging (dasha changes, astrological events) | ⏸ HOLD |
| 2c | Google Pay compliance -- Razorpay UPI + card flows in-app | ⏸ HOLD |
| 2d | Play Store listing: icon, screenshots, description EN+HI, content rating, Data Safety form | ⏸ HOLD |
| 2e | Growth loops: referral system, annual subscription discount, Manifestation Calendar | ⏸ HOLD |

**App Testing Stages:**
- Stage 1 (Internal): Prateek tests with detailed questionnaire from CC
- Stage 2 (Closed Testing -- 14-day requirement): Prateek to engage testing agency
- Stage 3 (Production): CC to provide go-live checklist

---

## PART B -- Active Codex Commission Plan (2026-05-29)

### Threads Currently Active

| Thread | Commission | Status |
|---|---|---|
| KP Oracle | KP-Sprint2: /ask-question LLM Router (Guna + Gita) | 🔵 IN PROGRESS -- issued 2026-05-15 |

### Issue Immediately (no blockers)

| Commission | Module | Brief |
|---|---|---|
| KE-DEDUP-CONTRADICTION-1 | Knowledge Engine | `Codex_Deliveries/Knowledge_Engine/CODEX_COMMISSION_KE_DEDUP_CONTRADICTION.md` -- issue when quota resets ~2026-05-31 |
| KUN-1 | Kundali | Frontend only, backend live |
| LK-1 | Lal Kitab | After TT batch approval of `jyotish_lk_remedies` |
| PAN-L1 | Panchang | Language/regional pages -- independent |

### TT Integration Actions (no Codex needed)

| Item | Source | Priority |
|---|---|---|
| TAR-SEO-1 integration | `Codex_Deliveries/Tarot/` | 🔴 HIGH |
| LSG-1 (Lo Shu Grid) integration | `Codex_Deliveries/Lo_Shu_Grid/` | 🟠 HIGH |

### Issue After KP-Sprint2 Delivers

| Commission | Module | Brief |
|---|---|---|
| KP-2B | KP Oracle | Ritual Animation + 3-Pillar UX + Astro-Filter (blocked on KP-OP-9) |

### Issue After High-Priority Threads Running

| Commission | Notes |
|---|---|
| SEO-1 (SEO + Web Performance) | Issue LAST |
| ORACLE-P3 (5 World Oracles) | Phase 3 -- after KP 30+ days live |

---

## PART C -- Knowledge Engine Decode Roadmap

### Active Decode Threads (3 books in last-mile)

| Book | Status | Next Action |
|---|---|---|
| Phaladeepika | 🟢 UNBLOCKED | Begin Adhyaya II immediately |
| BPHS Vol 1 | 🟡 PARTIAL (Ch11-Ch24 done) | Confirm Q1/Q2, then Karaka → Yoga → Dasha |
| KP Astrology | 🟡 NEAR COMPLETE (256 rules) | claim_axis longevity retroactive pass |

### After 3-Book Last-Mile: 10-Book Ingest Plan

- KE-DEDUP-CONTRADICTION-1 issued and delivered first
- Then begin systematic decode of: Longevity (Unnatural), Medical Astrology, Destiny Numerology, 300 Horoscopes Vol 1, and 6 additional books per `KE_TEXTBOOK_DECODE/KE_Ingest_Sequence_Approved.md`
- Dedup + contradiction pair work done together after every pair of books, not retrofitted later

### Schema State (as of 2026-05-29)

| Item | Status |
|---|---|
| KE-SCHEMA-AMENDMENT-PD1 | ✅ COMMITTED `25201e4` |
| 9 new schema constants | ✅ LIVE in `ke_schema_constants.py` |
| `compute_neechabhanga_flags()` | ✅ LIVE in `vedic_calculator.py` |
| `VedhaNullifier`, `CrossTextMatch` Pydantic models | ✅ LIVE in `knowledge_schema.py` |
| `contradicts`, `partial_contradiction` in `VALID_CROSS_TEXT_RELATIONSHIPS` | ✅ COMMITTED `ed02c73` |
| `VALID_CONTRADICTION_TYPES` constant | ✅ COMMITTED `ed02c73` |
| Rule count in MongoDB | 1,036+ (BPHS Vol 1/2 batches) |
| Approved rules (can run through KE) | ~70% auto-approved; 0 co-founder sign-offs yet |

---

## PART D -- Technical Decision Lock Registry

> Key locked decisions. See archived `CODEX_MASTER_ROADMAP.md` for full TD-01 to TD-27 detail.

| Decision | Status |
|---|---|
| **Legacy Model rule** -- all live computations via `vedic_calculator.py` + pyswisseph; KE is interpretation only | 🔒 LOCKED 2026-04-19 |
| **Architecture: 3-layer report model** -- simplified / modern / classical | 🔒 LOCKED |
| **KE Schema Amendment PD1** -- 9 constants, neechabhanga pre-processor, contradiction pairs | 🔒 LOCKED `25201e4` |
| **Contradiction encoding standard** -- `KE_TEXTBOOK_DECODE/Schema_Docs/KE_CONTRADICTION_PAIR_SCHEMA.md` | 🔒 LOCKED `ed02c73` |
| **TD-26 Country Kundali as Alpha Signal** | 🔒 Phase 2 spec locked -- do not build before Commission J |
| **TD-27 Forecast Tier / Life Area Outlook** | 🔒 Phase 2 spec locked |
| **Ingest freeze** | LIFTED (KE Phase 1.2 all sprints complete) |

---

## PART E -- Next Milestones Dashboard (2026-05-29)

| Milestone | Target | Key Actions |
|---|---|---|
| **KP-Sprint2 delivery + integration** | ~Next 2 weeks | Chase Codex delivery, integrate, verify on Render |
| **KE 3-book last-mile done** | ~3 CC sessions | Phaladeepika II + BPHS Q3+ + KP longevity pass |
| **KE-DEDUP-1 issued** | ~2026-05-31 | Quota resets; issue brief |
| **TAR-SEO-1 + LSG-1 integrated** | This work week | TT integration actions |
| **10 QA gaps closed (High priority)** | This work week | See `#5_CODEX_COMMISSION_TABLE.md` GAP REGISTER |
| **Play Store Phase 1B readiness** | After Razorpay live keys | Full E2E journey QA + Lighthouse + Sentry |

---

*For full commission brief index: see `#5_CODEX_COMMISSION_TABLE.md`*
*For KE decode detail: see `KE_TEXTBOOK_DECODE/README.md`*
*For SEO 20K status: see `SEO_20K/SEO_TRACKER.md`*
