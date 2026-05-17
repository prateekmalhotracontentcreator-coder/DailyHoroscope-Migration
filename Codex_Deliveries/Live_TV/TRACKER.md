# Live TV -- Module Tracker
> Path: `Codex_Deliveries/Live_TV/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-17 · v2.0

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- live in production, one open cosmetic item (LTV-OP-1) |
| **Backend** | `backend/live_tv_router.py` registered in `server.py` ✅ |
| **Frontend panel** | `frontend/src/components/LiveTVPanel.jsx` ✅ |
| **Hook** | `frontend/src/hooks/useLiveTv.js` ✅ |
| **SEO route** | `/live-sai-baba-arti` → `LiveSaiBabaArtiPage.jsx` ✅ |
| **Static assets** | `frontend/public/live_tv/active_live_tv.mp4` + `.jpg` -- Vercel CDN ✅ |
| **Live URL** | https://www.everydayhoroscope.in/live-sai-baba-arti |
| **Panel coverage** | `/` (Landing) · `/home` (Home logged-in) · `/panchang/today` + all Panchang sub-routes ✅ |
| **Punya hook** | `live_tv_view` -- wired ✅ |
| **Infrastructure** | Render Starter plan (always-on, no cold starts as of 2026-05-17) ✅ |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| LTV-1 | Live TV: Sai Baba Arti (backend + frontend) | ✅ INTEGRATED | `CODEX_COMMISSION_LIVE_TV_SAI_BABA_ARTI.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| LTV-OP-1 | **Player console redesign** -- console bar (Play/Mute/YouTube buttons) on `/live-sai-baba-arti` visible and functional but visual design does not match original spec intent. Polish needed. | TT | 🟡 MED | Raise as new Codex brief when exact design is confirmed. Not blocking live status. |

**Phase 2 parking lot (not active):**
- Additional channels (Ganesh Vandana, Hanuman Chalisa, Durga Arti) -- library cards in UI as "Coming Soon"
- Programme schedule with countdown
- Scheduled daily social auto-post (6 AM FB + YT) -- tied to Notifications thread

---

## Bug Fixes Resolved (2026-05-16 / 2026-05-17 sessions)

| Bug | Root Cause | Fix | Commit |
|---|---|---|---|
| Panel invisible on logged-in Home | `Home.jsx` had no `<LiveTVPanel />` mount | Added import + mount to `Home.jsx` | `90825c7` |
| Panel invisible on Panchang (logged-in) | Navbar links `/panchang/today` → `PanchangPage.jsx` which had no panel | Added import + mount to `PanchangPage.jsx` | `1466004` |
| Console bar clipped on Live page | Console inside `overflow-hidden aspect-video` section -- clipped on mobile | Decoupled: video canvas owns `aspect-video`, console sits outside section | `1466004` |
| Video not playing (autoplay blocked) | React `muted` prop doesn't reflect to DOM before autoplay decision | Callback ref sets `el.muted = true` synchronously before `el.play()` | Earlier |
| Mixed-content `http://` video URL | Render proxy strips SSL; backend constructs `http://` URLs blocked on HTTPS | MP4 + thumbnail moved to `frontend/public/live_tv/`; hook overrides with Vercel CDN path | Earlier |
| Panel invisible during Render cold start (30-60s) | `loading = true` held for full cold-start duration | 5s AbortController timeout + immediate `FALLBACK_DATA` with static Vercel assets | Earlier |

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-04-25 | LTV-1 integrated. Video player, arti schedule, countdown live. Punya hook wired. Tracker created. | Codex + CC | -- |
| v2.0 | 2026-05-17 | Full production activation. 6 bugs fixed. Panel live on Home (logged-in), PanchangPage, Landing. Console bar visible. Vercel CDN assets. Render Starter (always-on). Open: LTV-OP-1 console polish. | CC | `90825c7`, `1466004` |
