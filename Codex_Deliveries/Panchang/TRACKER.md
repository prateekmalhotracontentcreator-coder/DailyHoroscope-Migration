# Panchang -- Module Tracker
> Path: `Codex_Deliveries/Panchang/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-22 · v1.1

---

## Current Status

| Field | Value |
|---|---|
| **Status** | ✅ LIVE -- fully complete and verified |
| **Frontend** | `frontend/src/pages/PanchangPage.jsx` |
| **Backend** | `backend/panchang_router.py` (current version: v11-swiss) |
| **Live URL** | `/panchang` |
| **Coverage** | 318 cities · 81 countries |
| **Accuracy** | Verified vs Drik Panchang ±1 min (New Delhi benchmark) |
| **Punya hook** | `panchang_daily_view` -- wired |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| **PAN-L1** | Language/Regional Pages (Tamil, Telugu, Malayalam, Kannada, Hindi) | 🟢 CODEX IMPLEMENTED | `CODEX_COMMISSION_PANCHANG_LANGUAGE_PAGES.md` · SEO wiring completed 2026-05-22 |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| PAN-OP-1 | **PAN-L1 language SEO pages** | CX | 🟢 DONE | Existing routes/page wrapper verified; language-aware SEO, hreflang, canonical, and regional JSON-LD added in `frontend/src/pages/panchang/PanchangPage.jsx`. |
| PAN-OP-2 | **Bump `ENGINE_VERSION`** in `panchang_router.py` before any backend change | CC | 🔴 ENFORCE | Format: `panchang-router-vN-swiss` (currently v11). Never skip this. |
| PAN-OP-3 | PAN-L1 must use existing `/api/panchang/daily` endpoint with location slugs -- no new backend routes | CX | 🔴 ENFORCE | `hreflang` tags and regional JSON-LD schema required |

---

## Architecture Notes

- Engine: pyswisseph `swe.rise_trans` + `swe.calc_ut` for all computations
- Routes: `GET /api/panchang/daily` · `/api/panchang/locations` · `/api/panchang/calendar/{y}/{m}` · `/api/panchang/festivals`
- PanchangShareCard + HoroscopeShareCard: offscreen positioning at `left: -9999px` -- no flash on capture
- Facebook + YouTube posting working from Admin Console Social Media tab

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-04-30 | PAN-L1 brief written. Panchang engine fully live (v11-swiss, 318 cities). Tracker created. | CC | `CODEX_COMMISSION_PANCHANG_LANGUAGE_PAGES.md` |
| v1.1 | 2026-05-22 | PAN-L1 implemented. Existing language routes and sitemap were already present; Codex added language-aware SEO title/description, hreflang alternates, English-primary canonical, and language-aware JSON-LD without backend changes. Build passed. Live route headers for all 5 language URLs returned HTTP 200. | CX | `frontend/src/pages/panchang/PanchangPage.jsx`, `frontend/src/components/SEO.jsx` |
