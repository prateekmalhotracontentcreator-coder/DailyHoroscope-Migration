# Panchang -- Module Tracker
> Path: `Codex_Deliveries/Panchang/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-06-05 · v1.3

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
| **PAN-TM-1** | The Cosmic Clock -- Time Map Visual Redesign (parchment scroll, magnifying lens, embroidery border) | ✅ INTEGRATED | `CODEX_COMMISSION_PAN_TM1_COSMIC_CLOCK.md` · CD Handover Pack integrated commit `ae3b683` 2026-06-05. `PanchangCosmicMapV2.jsx` live. Light theme (Golden Beige) only. |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| PAN-OP-1 | **PAN-L1 language SEO pages** | CX | 🟢 DONE | Existing routes/page wrapper verified; language-aware SEO, hreflang, canonical, and regional JSON-LD added in `frontend/src/pages/panchang/PanchangPage.jsx`. |
| PAN-OP-2 | **Bump `ENGINE_VERSION`** in `panchang_router.py` before any backend change | CC | 🔴 ENFORCE | Format: `panchang-router-vN-swiss` (currently v21). Never skip this. |
| PAN-OP-3 | PAN-L1 must use existing `/api/panchang/daily` endpoint with location slugs -- no new backend routes | CX | 🔴 ENFORCE | `hreflang` tags and regional JSON-LD schema required |
| ~~PAN-OP-4~~ | ~~**Issue PAN-TM-1 to CD**~~ | -- | ✅ DONE | CD delivered Handover Pack. CC integrated `ae3b683`. |
| PAN-OP-5 | **TT: smoke test The Cosmic Clock on production** -- verify `/panchang/today` shows the parchment scroll, lens tracks cursor, window pills render in green/red, and guidance bar updates. | TT | 🟠 HIGH | After Vercel auto-deploy (~2 min). |

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
| v1.2 | 2026-06-03 | PAN-TM-1 brief written. `CODEX_COMMISSION_PAN_TM1_COSMIC_CLOCK.md` created. Commission added to open points as PAN-OP-4. Ready to issue to CD. | CC | -- |
| v1.3 | 2026-06-05 | PAN-TM-1 integrated (`ae3b683`). `PanchangCosmicMapV2.jsx` + `.ptm-*` CSS + 3 art PNGs. Theme locked: Light Golden Beige only. Import swapped in `PanchangPage.jsx`. Build 0 errors. Pushed to Vercel. Status: ACTIVE (PAN-OP-5 TT smoke test pending). | CC | `ae3b683` |
| v1.1 | 2026-05-22 | PAN-L1 implemented. Existing language routes and sitemap were already present; Codex added language-aware SEO title/description, hreflang alternates, English-primary canonical, and language-aware JSON-LD without backend changes. Build passed. Live route headers for all 5 language URLs returned HTTP 200. | CX | `frontend/src/pages/panchang/PanchangPage.jsx`, `frontend/src/components/SEO.jsx` |
