# Tarot Module -- Complete File Manifest
> Last updated: 2026-06-18
> **Read this before starting any Tarot commission.** Every file in scope is listed here.
> Worktree copies in `.claude/worktrees/` are stale snapshots -- always work from the paths below.

---

## Frontend -- Interactive Tool

| File | Route | Notes |
|---|---|---|
| `frontend/src/pages/tarot/TarotPage.jsx` | `/tarot` | Main tool -- 5 tabs (Daily Draw, Spreads, Favorable Periods, Journal, History). Premium-gated inline. |
| `frontend/src/pages/tarot/TarotLanding.jsx` | `/the-tarot` | Public SEO landing page. Currently uses amber/cinzel/playfair tokens -- NOT Temple gold system. |
| `frontend/src/pages/tarot/TarotHistoryPage.jsx` | `/tarot/history` | Premium-gated via PremiumRoute. Currently uses raw BEM CSS -- no Tailwind at all. |
| `frontend/src/utils/tarotFeedback.js` | utility | `submitTarotFeedback()` calls `POST /api/tarot/feedback`. No UI wired yet -- dead feature. |
| `frontend/public/tarot_cards.json` | static | 78-card SVG deck. Do NOT modify without TT instruction -- deck swap handled separately. |

## Frontend -- SEO Content Pages (Phase 1 -- 199 pages live)

| File | Route | Notes |
|---|---|---|
| `frontend/src/pages/tarot-seo/TarotSeoHubPage.jsx` | `/tarot/spreads` | Spread hub -- 100 spreads listed |
| `frontend/src/pages/tarot-seo/TarotSpreadPage.jsx` | `/tarot/spread/:spreadSlug` | Individual spread detail |
| `frontend/src/pages/tarot-seo/TarotCardPage.jsx` | `/tarot/card/:cardSlug` | Individual card meaning page |
| `frontend/src/pages/tarot-seo/TarotIntentionPage.jsx` | `/tarot/for/:intentionSlug` | Intention-based reading guide |

## Frontend -- SEO Pages (Phase 2 -- TAR-SEO-3, not yet built)

| File | Route | Notes |
|---|---|---|
| `frontend/src/pages/tarot-seo/TarotCardHubPage.jsx` | `/tarot/cards` | 78-card index hub. Does NOT exist yet. |
| `frontend/src/pages/tarot-seo/TarotCombinationPage.jsx` | `/tarot/card/:cardSlug/:spreadSlug` | Card × spread combination page. Does NOT exist yet. |

---

## Backend

| File | Purpose | Notes |
|---|---|---|
| `backend/tarot_router.py` | Interactive draw tool endpoints | DO NOT TOUCH in SEO or design commissions |
| `backend/tarot_seo_router.py` | SEO page data endpoints (`/api/seo/tarot-seo/*`) | Phase 1 router -- registered in server.py |
| `backend/tarot_seo_data.py` | All Phase 1 content -- 100 spreads, 78 cards, 20 intentions | Single source of truth for SEO content. QA-cleared. |
| `backend/tarot_combinations_router.py` | Phase 2 combination page endpoints | Does NOT exist yet -- TAR-SEO-3 |
| `backend/scripts/seed_tarot_seo.py` | Seeds tarot SEO data to MongoDB | Already run -- do not re-run without TT instruction |
| `backend/scripts/seed_tarot_combinations.py` | Seeds `tarot_combinations` collection | Does NOT exist yet -- TAR-SEO-3 |
| `backend/scripts/verify_tarot_compliance.py` | Verifies tarot SEO data structure | Reference only |

---

## Tests

| File | Purpose | Status |
|---|---|---|
| `tests/echo_pace_tarot_scan.py` | L1-L3 ECHO/PACE scanner -- all 3 page types | ✅ Active. Run after any content change. |
| `tests/echo_pace_tarot_serper_detail.py` | Layer G Serper validation -- 15 queries | ✅ Active. Needs `Serper_Default_key`. |
| `tests/echo_pace_seoc_tarot_scan.py` | SEO combination page scanner variant | Reference |
| `tests/test_tarot_compliance.py` | CI/CD compliance test for combination pages | Inactive until TAR-SEO-3 seeded. Auto-activates. |
| `tests/echo_pace_tarot_report.json` | Last L1-L3 scan output | Last run: 2026-05-30. All PASS. |
| `tests/tarot_serper_detail_report.json` | Last Layer G scan output | Last run: 2026-05-30. 15/15 PASS, 0% dup. |

---

## Commission Docs

| File | Commission | Status |
|---|---|---|
| `Codex_Deliveries/Tarot/CODEX_COMMISSION_TAROT_V4_UI.md` | TAR-v4 | ✅ INTEGRATED |
| `Codex_Deliveries/Tarot/CODEX_COMMISSION_TAR_SEO_1.md` | TAR-SEO-1 | ✅ INTEGRATED |
| `Codex_Deliveries/Tarot/CODEX_COMMISSION_TAR_SEO_2_REWRITE.md` | TAR-SEO-2 | ✅ QA-CLEARED |
| `Codex_Deliveries/Tarot/CODEX_COMMISSION_TAR_SEO_3_COMBINATIONS.md` | TAR-SEO-3 | 🟡 READY TO ISSUE |
| `Codex_Deliveries/Tarot/CODEX_COMMISSION_TAR_DESIGN_1.md` | TAR-DESIGN-1 | 🟡 READY TO ISSUE |
| `Codex_Deliveries/Tarot/TAR_ECHO_PACE_GAI_CONSULTATION.md` | ECHO/PACE guidance | Reference |
| `Codex_Deliveries/Tarot/TAR_SEO_TITLE_HUMANIZATION_LIST.md` | Title humanization | ✅ RESOLVED |
| `Codex_Deliveries/Tarot/TRACKER.md` | Module tracker | Update at end of every session |

---

## Key Architecture Rules (repeat here for any thread starting cold)

1. `tarot_router.py` and `tarot_cards.json` are the **interactive draw tool** -- never modify in SEO or design work
2. `tarot_seo_data.py` is the **single source of truth** for all 199 Phase 1 SEO pages -- QA-cleared, do not touch content without re-running ECHO/PACE
3. Phase 2 route family: hub at `/tarot/cards` (plural), detail at `/tarot/card/:slug` (singular), combo at `/tarot/card/:slug/:spreadSlug` (singular extension) -- do not introduce `/tarot/cards/:slug`
4. All design work must use Temple tokens: `text-gold / border-gold / bg-gold` (#c5a059), GlassCard pattern, no arbitrary hex values
5. `font-cinzel` and `font-playfair` are NOT in the production font build -- use `font-serif` (Georgia fallback)
6. Punya hooks (`tarot_daily_draw`, `tarot_spread_complete`, `tarot_bookmark`) are fire-and-forget via `safeClaimPunyaAction()` -- never block render or remove
