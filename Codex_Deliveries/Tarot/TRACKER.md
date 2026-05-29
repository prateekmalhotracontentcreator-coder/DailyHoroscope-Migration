# Tarot -- Module Tracker
> Path: `Codex_Deliveries/Tarot/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-29 · v1.6

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- TAR-v4 live; TAR-SEO-1 integrated; ECHO/PACE L1-L3 PASS (all flags accepted); Layer G pending Serper key from TT |
| **Frontend** | `frontend/src/pages/tarot/TarotPage.jsx` |
| **Backend** | `backend/tarot_router.py` |
| **Live URL** | `/tarot` |
| **Deck** | `frontend/public/tarot_cards.json` -- 78 SVG cards |
| **Tabs** | Daily Draw · Spreads · Favorable Periods · Journal · History |
| **Punya hooks** | `tarot_daily_draw` · `tarot_spread_complete` · `tarot_bookmark` -- all wired |
| **SEO routes** | `/tarot/spreads` · `/tarot/spread/:spreadSlug` · `/tarot/card/:cardSlug` · `/tarot/for/:intentionSlug` |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| **TAR-v4** | Tarot UI v4 Enhancement | 🟢 LOCAL BUILD VERIFIED | `CODEX_COMMISSION_TAROT_V4_UI.md` |
| **TAR-SEO-1** | Tarot SEO module (hub + spreads + cards + intentions) | 🟢 INTEGRATED + DEPLOYED | `CODEX_COMMISSION_TAR_SEO_1.md` |
| **TAR-SEO-2** | Tarot SEO data rewrite (copyright + quality fix) | 🟢 DEPLOYED (content template fix complete) | `CODEX_COMMISSION_TAR_SEO_2_REWRITE.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| TAR-OP-1 | **Temple review TAR-v4 local implementation** | TT | 🟡 MED | Implemented in `frontend/src/pages/tarot/TarotPage.jsx`; older brief path is stale |
| TAR-OP-2 | TAR-v4 must NOT modify `tarot_router.py` or `tarot_cards.json` -- visual layer only | CX | 🔴 ENFORCE | No logic changes, no new endpoints, no deck changes |
| TAR-OP-3 | **Layer G (Serper) sign-off** | TT | 🟠 BLOCKING for full QA pass | L1-L3 all PASS or accepted (see v1.7 notes). Provide `Serper_Default_key` from Render env and run: `Serper_Default_key=YOUR_KEY python3 tests/echo_pace_tarot_scan.py`. Uses ~6 credits. |
| TAR-OP-4 | **Temple review TAR-SEO-2 one-file rewrite** | TT | 🟡 MED | Rewrote only `backend/tarot_seo_data.py` to replace source-derived spread prose and rigid card templates. Record counts unchanged (`100 / 78 / 20`), compile passed, and no router/frontend files changed. |

---

## Architecture Notes

- TAR-v4 is a pure visual uplift -- no backend changes, no JSON changes
- Punya Rewards hooks are fire-and-forget via `safeClaimPunyaAction()` -- do not block page render
- Reconciliation note: `TAROT_V4_UI_RECONCILIATION_NOTE_2026-05-22.md`
- Build verified from `frontend/` with `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-04-30 | TAR-v4 brief written. Module fully live (78 cards, 3 tabs, Punya hooks wired). Tracker created. | CC | `CODEX_COMMISSION_TAROT_V4_UI.md` |
| v1.1 | 2026-05-22 | Reconciled new TAR-v4 UI award against current Migration build. Corrected frontend path to `frontend/src/pages/tarot/TarotPage.jsx`; confirmed TAR-v4 is frontend-only and not yet implemented in the current page. | CX | `TAROT_V4_UI_RECONCILIATION_NOTE_2026-05-22.md` |
| v1.2 | 2026-05-22 | Implemented TAR-v4 UI uplift in the current Tarot page: mystical hero, particle reveal, card modal/drawer, Celtic Cross layout, Vedic focus cards, timeline history, and streak widget. Production React build passed. | CX | `frontend/src/pages/tarot/TarotPage.jsx` |
| v1.3 | 2026-05-25 | Prepared TAR-SEO-1 local delivery without touching the interactive tarot module. Added `backend/tarot_seo_router.py`, tarot sitemap support, and 4 public SEO pages for `/tarot/spreads`, `/tarot/spread/:spreadSlug`, `/tarot/card/:cardSlug`, and `/tarot/for/:intentionSlug`. Production React build passed and backend syntax checks passed. | CX | `CODEX_COMMISSION_TAR_SEO_1.md` |
| v1.4 | 2026-05-25 | Prepared TAR-SEO-2 local one-file rewrite. Reworked all 100 spread `purpose`/`when` fields and all 78 card `upright`/`reversed`/`love`/`career`/`health` fields inside `backend/tarot_seo_data.py` to remove source-derived prose and repetitive templating. Compile passed and record counts stayed `100 / 78 / 20`. | CX | `CODEX_COMMISSION_TAR_SEO_2_REWRITE.md` |
| v1.5 | 2026-05-29 | TAR-SEO-1 integration completed. Confirmed backend router already registered in `server.py` (commit 8f2ede8). Added 4 lazy imports + routes to `App.js` for `/tarot/spreads`, `/tarot/spread/:spreadSlug`, `/tarot/card/:cardSlug`, `/tarot/for/:intentionSlug`. Confirmed sitemap endpoint `/api/seo/sitemap/tarot` already live in `seo_router.py`. Build passed, pushed to main (commit 8f36fc8). | CC (Tarot thread) | `HANDOVER_TAROT.md` |
| v1.6 | 2026-05-29 | TAR-SEO content template fix. Cosine similarity analysis revealed 83-88% cross-page similarity: 56 minor arcana cards sharing suit-element template sentences, and 100 spreads sharing 7 category-level boilerplate phrases. Rewrote all 5 content fields (upright/reversed/love/career/health) for all 56 minor arcana, and all purpose+when fields for all 100 spreads. Result: 0 pairs >40% for cards (was 72 pairs >50%), 0 pairs >40% for spreads (was 128 pairs >50%), avg max similarity now ~11% for both. Major arcana (22 cards) were clean and untouched. Build passed, pushed to main (commit b0dfdd4). | CC (Tarot thread) | |
| v1.7 | 2026-05-29 | ECHO/PACE L1-L3 finalised. Fixed 4 flagged spread pairs: rewrote purpose+when for settlement-vs-trial (offer evaluation angle) vs choosing-battle-vs-settlement (inner readiness angle); rewrote manifesting-urgent-financial-abundance (acute crisis relief) vs manifesting-fast-secondary-income (skill-to-income building). Varied deck description in `use` field for 18 spreads to eliminate shared structural boilerplate. Post-fix scan: Spreads L1 PASS peak 44.1% (was 60%), Cards L1 PASS peak 36.3%. Remaining L2/L1 Intentions flags all documented as acceptable: (a) Cards L2 Wands imagery -- original AI text, not from published source, L1 clean; (b) Intentions L1/L2 -- similarity driven by shared best_cards lists for thematically adjacent pages (health/anxiety share Strength+Temperance+The Star), not written prose dup. Layer G pending Serper key. Commit f283514. | CC (Tarot thread) | |
