# Tarot V4 UI Reconciliation Note

Last updated: 2026-05-22 03:09 IST; implementation addendum 2026-05-22

## Purpose

This note reconciles three Tarot states after the sanitization drive:

- previous Codex / Temple remediation and fuller-v4 planning work
- the current `DailyHoroscope-Migration` build
- the new Temple Team commission award in `Codex_Deliveries/Tarot`

## Authoritative New Commission

Current commission file:

- `/Users/apple/DailyHoroscope-Migration/Codex_Deliveries/Tarot/CODEX_COMMISSION_TAROT_V4_UI.md`

The new commission is a pure frontend visual uplift. It must not modify:

- `backend/tarot_router.py`
- `frontend/public/tarot_cards.json`
- Tarot backend API contracts
- Tarot reading, bookmark, history, deck, or Punya reward logic

## Path Correction

The commission brief still names the older path:

- `frontend/src/pages/TarotPage.jsx`

The current Migration build uses:

- `/Users/apple/DailyHoroscope-Migration/frontend/src/pages/tarot/TarotPage.jsx`

All TAR-v4 UI implementation should target the current path unless Temple explicitly asks to move the file.

## What Is Present In Current Migration Build

Current frontend route registration:

- `/Users/apple/DailyHoroscope-Migration/frontend/src/App.js`
- `/tarot` loads `./pages/tarot/TarotPage`
- `/the-tarot` loads `./pages/tarot/TarotLanding`
- `/tarot/history` loads `./pages/tarot/TarotHistoryPage` behind `PremiumRoute`

Current runtime surfaces confirmed in `frontend/src/pages/tarot/TarotPage.jsx`:

- Daily Draw tab
- Spreads tab
- Favorable Periods tab
- Journal tab
- History tab
- 78-card asset loading from `/tarot_cards.json`
- existing card flip animation
- scene narrative player
- focus-area selector
- question input
- bookmark toggle using `POST /api/tarot/bookmark`
- canonical paginated history read via `res.data.items`
- manifestation journal calls
- favorable-periods and offers calls
- Punya hooks for daily draw, spread completion, and bookmark
- Tarot-specific SEO component call

Current backend surface confirmed in `backend/tarot_router.py`:

- engine version identifies as `tarot-router-v4`
- richer `TarotSpread` model exists
- manifestation collection support exists
- current TAR-v4 commission still treats backend as out of scope

## What Is Not Yet Present From TAR-v4 UI

The following commission components / behaviors are not currently present in the Migration `TarotPage.jsx` and remain implementation work:

- `TarotHero` immersive mystical landing hero
- enhanced `FlippingCard` with particle burst, glow ring, and `perspective: 1200px`
- `ReadingModal` full-screen detail modal
- `CelticCrossLayout` premium 10-card visual layout
- Vedic icon focus-area cards with planet labels
- history timeline grouped by month with fade-in observer
- `StreakWidget` with seven day circles and XP progress
- `CardDrawer` using Vaul / responsive right panel

## Relationship To Earlier Sanitized Prompt Pack

Earlier prompt-pack copies were found in internal `.claude` / worktree folders and mirrored under:

- `/Users/apple/Documents/New project/MODULE_TAROT/06_INTERNAL_DOCS_RELOCATED/`

Those files are the same UI-uplift family as the new commission, but they are no longer the governing source. The governing source is now:

- `/Users/apple/DailyHoroscope-Migration/Codex_Deliveries/Tarot/CODEX_COMMISSION_TAROT_V4_UI.md`

## Reconciliation Outcome

Status:

- remediation slice remains closed
- current Migration build has a working Tarot module
- TAR-v4 local implementation has now been applied to the current `pages/tarot/TarotPage.jsx`
- production React build passes from `/Users/apple/DailyHoroscope-Migration/frontend`

Recommended build posture:

- preserve all existing API calls and reward hooks
- preserve current premium gating behavior unless Temple separately changes the product policy
- implement the eight TAR-v4 visual prompts inside the current page path
- do not touch backend or card bundle
- after implementation, run the frontend build from `/Users/apple/DailyHoroscope-Migration/frontend`

## 2026-05-22 Implementation Addendum

Implemented in:

- `/Users/apple/DailyHoroscope-Migration/frontend/src/pages/tarot/TarotPage.jsx`

Implemented TAR-v4 UI surfaces:

- `TarotHero` mystical hero with animated starfield and fanned cards
- enhanced card flip with particle burst, glow ring, and `perspective: 1200px`
- desktop reading detail modal
- mobile Vaul card drawer
- Celtic Cross visual layout for 10-card spreads
- Vedic focus-area cards with planet labels
- timeline-style history grouped by month with `IntersectionObserver` fade-in
- daily streak / XP widget derived from history and gamification data

Scope preserved:

- no backend edits
- no tarot card bundle edits
- existing API calls preserved
- existing Punya reward hooks preserved

Validation:

- `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
- result: compiled successfully

## Open Queries

No blocking query for reconciliation.

Implementation note:

- Treat `/Users/apple/DailyHoroscope-Migration/frontend/src/pages/tarot/TarotPage.jsx` as the implementation target, despite the older path written in the commission brief.
