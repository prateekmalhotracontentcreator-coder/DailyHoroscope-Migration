# Tarot -- Module Tracker
> Path: `Codex_Deliveries/Tarot/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-25 · v1.4

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- TAR-v4 live; TAR-SEO-1 local SEO delivery prepared; TAR-SEO-2 local data rewrite prepared |
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
| **TAR-SEO-1** | Tarot SEO module (hub + spreads + cards + intentions) | 🟡 LOCAL BUILD VERIFIED | `CODEX_COMMISSION_TAR_SEO_1.md` |
| **TAR-SEO-2** | Tarot SEO data rewrite (copyright + quality fix) | 🟡 LOCAL FILE VERIFIED | `CODEX_COMMISSION_TAR_SEO_2_REWRITE.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| TAR-OP-1 | **Temple review TAR-v4 local implementation** | TT | 🟡 MED | Implemented in `frontend/src/pages/tarot/TarotPage.jsx`; older brief path is stale |
| TAR-OP-2 | TAR-v4 must NOT modify `tarot_router.py` or `tarot_cards.json` -- visual layer only | CX | 🔴 ENFORCE | No logic changes, no new endpoints, no deck changes |
| TAR-OP-3 | **Temple review TAR-SEO-1 local delivery** | TT | 🟡 MED | `tarot_seo_data.py` committed by TT. This session added `tarot_seo_router.py`, 4 public SEO pages, sitemap wiring, App.js routes, and Vercel cache headers without touching the interactive `/tarot` tool. |
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
