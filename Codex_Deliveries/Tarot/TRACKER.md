# Tarot -- Module Tracker
> Path: `Codex_Deliveries/Tarot/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-15 · v1.0

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- fully functional, visual uplift pending |
| **Frontend** | `frontend/src/pages/TarotPage.jsx` |
| **Backend** | `backend/tarot_router.py` |
| **Live URL** | `/tarot` |
| **Deck** | `frontend/public/tarot_cards.json` -- 78 SVG cards |
| **Tabs** | Daily Draw · Spreads · History |
| **Punya hooks** | `tarot_daily_draw` · `tarot_spread_complete` · `tarot_bookmark` -- all wired |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| **TAR-v4** | Tarot UI v4 Enhancement | 🟣 READY TO ISSUE | `CODEX_COMMISSION_TAROT_V4_UI.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| TAR-OP-1 | **Issue TAR-v4 to Codex** (Week 3) | TT | 🟡 MED | Brief at `CODEX_COMMISSION_TAROT_V4_UI.md` |
| TAR-OP-2 | TAR-v4 must NOT modify `tarot_router.py` or `tarot_cards.json` -- visual layer only | CX | 🔴 ENFORCE | No logic changes, no new endpoints, no deck changes |

---

## Architecture Notes

- TAR-v4 is a pure visual uplift -- no backend changes, no JSON changes
- Punya Rewards hooks are fire-and-forget via `safeClaimPunyaAction()` -- do not block page render

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-04-30 | TAR-v4 brief written. Module fully live (78 cards, 3 tabs, Punya hooks wired). Tracker created. | CC | `CODEX_COMMISSION_TAROT_V4_UI.md` |
