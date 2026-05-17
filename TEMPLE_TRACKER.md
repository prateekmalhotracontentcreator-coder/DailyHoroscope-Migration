# Temple Tracker -- Master Index
> EverydayHoroscope · Module Status Dashboard
> **Read this at session start. Then open the individual module tracker for the module you are working on.**
> Last updated: 2026-05-18 (session 4 -- ARC-2 `c1a7cb0` + KE-IQ `f7aa78b` integrated, 75/75 tests)

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
| 2 | KP Oracle | [`KP/TRACKER.md`](Codex_Deliveries/KP/TRACKER.md) | 🟡 ACTIVE | KP-2A + KP-Sprint2 ready to issue (TT). All CC blockers cleared 2026-05-15. | TT |
| 3 | Individual Reports | [`Individual_Reports/TRACKER.md`](Codex_Deliveries/Individual_Reports/TRACKER.md) | 🟣 PLANNED | IR-1 ready to issue Week 1 -- no dependency | TT |
| 4 | Remedies Engine | [`Remedies/TRACKER.md`](Codex_Deliveries/Remedies/TRACKER.md) | 🟡 ACTIVE | `/api/remedies/ref/{id}` confirmed live. `krishna_prashnavali_remedies` seeded (36 records). REM-P1 ready to issue. | TT |
| 5 | The Strategist | [`Strategist/TRACKER.md`](Codex_Deliveries/Strategist/TRACKER.md) | ✅ LIVE | STR-OP-3: Verify DashaTimingBar live data on `/strategist/missions` (TT) | TT |
| 6 | Arc Angel | [`Arc_Angel/TRACKER.md`](Codex_Deliveries/Arc_Angel/TRACKER.md) | 🟡 ACTIVE | **ARC-2 ✅ INTEGRATED** commit `c1a7cb0` 2026-05-18. 3-pillar confidence live, decay engine active, ArcAngelPanel rebuilt. Pillar 1 bridge (4-section → 12-domain) is a stopgap -- KE-IQ will deliver full 12-area questionnaire. | TT |
| 7 | Tarot | [`Tarot/TRACKER.md`](Codex_Deliveries/Tarot/TRACKER.md) | 🟡 ACTIVE | TAR-v4 visual uplift -- issue Week 3 | TT |
| 8 | Kundali / Birth Chart | [`Kundali/TRACKER.md`](Codex_Deliveries/Kundali/TRACKER.md) | 🟣 PLANNED | KUN-1 ready to issue Week 4+ | TT |
| 9 | Lal Kitab | [`LK/TRACKER.md`](Codex_Deliveries/LK/TRACKER.md) | 🟣 PLANNED | LK-1 ready to issue Week 4+ | TT |
| 10 | Longevity Report | [`Longevity/TRACKER.md`](Codex_Deliveries/Longevity/TRACKER.md) | 🟣 PLANNED | KE Sprint 2 gate ✅ cleared 2026-05-17. LON-1 READY TO ISSUE. Verify Render load (LON-OP-1) first. Large scope (~48h). | TT |
| 11 | Love & Engagement | [`Love_Module/TRACKER.md`](Codex_Deliveries/Love_Module/TRACKER.md) | ✅ LIVE | Nothing open | -- |
| 12 | Live TV | [`Live_TV/TRACKER.md`](Codex_Deliveries/Live_TV/TRACKER.md) | 🟡 ACTIVE | LTV-OP-1: console polish deferred. Panel live on Home (logged-in) + PanchangPage. Render Starter activated. | TT |
| 13 | Punya Rewards | [`Punya_Rewards/TRACKER.md`](Codex_Deliveries/Punya_Rewards/TRACKER.md) | ✅ LIVE | Nothing open | -- |
| 14 | Notifications | [`Notifications/TRACKER.md`](Codex_Deliveries/Notifications/TRACKER.md) | 🟡 ACTIVE | M-5 WhatsApp OTP + M-6 Instagram Business ID | TT |
| 15 | Panchang | [`Panchang/TRACKER.md`](Codex_Deliveries/Panchang/TRACKER.md) | ✅ LIVE | PAN-L1 language pages -- issue Week 3+ | TT |
| 16 | SEO & Web Performance | [`SEO/TRACKER.md`](Codex_Deliveries/SEO/TRACKER.md) | 🟣 PLANNED | Issue LAST -- after high-priority threads running | TT |
| 17 | World Oracles | [`World_Oracles/TRACKER.md`](Codex_Deliveries/World_Oracles/TRACKER.md) | 🟣 PLANNED | Phase 3 -- do not issue until KP Oracle 30+ days live | TT |

---

## Cross-Cutting Temple Team Actions

| ID | Item | Priority | Status |
|---|---|---|---|
| M-1 | Replace OG image -- 1200×630 PNG ≤80 KB (`frontend/public/og-image.png`) | 🔴 HIGH | Open |
| M-2 | Run `seed_policies_v1.py` on Render (`--mongo-url "$MONGO_URL" --db-name horoscope_db`) | 🔴 HIGH | Open |
| ~~M-3~~ | ~~KP Oracle end-to-end production smoke test~~ | ✅ DONE | Cleared 2026-05-15. KP-2A unblocked. |
| ~~M-4~~ | ~~Strategist 22 records sign-off~~ | -- | ✅ CLEARED 2026-05-15 |
| M-5 | WhatsApp OTP + payment method on WABA Meta | 🟡 MED | Open |
| M-6 | Instagram Business Account ID -- not loading in Meta dashboard | 🟡 MED | Open |
| M-7 | react-snap vs helmet-async design decision | 🟢 LOW | Await SEO-1 recommendation |
| M-8 | PWA offline caching decision | 🟢 LOW | Await SEO-1 |
| M-9 | App.js lazy audit sign-off | 🟢 LOW | Non-blocking |

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
