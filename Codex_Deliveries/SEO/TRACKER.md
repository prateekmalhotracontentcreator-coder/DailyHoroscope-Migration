# SEO & Web Performance -- Module Tracker
> Path: `Codex_Deliveries/SEO/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-20 · v3.2

---

## Current Status

| Field | Value |
|---|---|
| **Status** | ✅ LIVE -- 12 of 13 commissions live in production |
| **GA4** | G-3HJC8BTHRQ -- wired and live |
| **GSC** | Verified + sitemap submitted |
| **Bing** | Verified + sitemap submitted |
| **OG tags** | Present on all major pages |
| **JSON-LD** | Present on all major routes |
| **SEO component** | `frontend/src/components/SEO.jsx` -- used sitewide |
| **Sitemap** | `frontend/public/sitemap.xml` |

---

## Commission Status

| ID | Commission | Track | Priority | Status | Brief |
|---|---|---|---|---|---|
| **SEO-WebPerf** | SEO + Marketing + Web Performance Optimisation | -- | Issue Last | 🟣 READY -- ISSUE LAST | `CODEX_COMMISSION_SEO_WEBPERF.md` |
| **SEO-C1** | Legal Pages Content (populate MongoDB policies) | C | Phase 1 | ✅ LIVE -- policies seeded to production 2026-05-20 | `CODEX_COMMISSION_SEO-C1.md` |
| **SEO-B1** | Tomorrow / Weekly / Monthly Per-Sign Horoscope (36 pages) | B | Phase 3 | ✅ LIVE -- commit 963dc82 | `CODEX_COMMISSION_SEO-B1.md` |
| **SEO-B3** | Festival Calendar Hub + Hora Today + Indian Calendar | B | Phase 2 | ✅ LIVE -- commit 963dc82 | `CODEX_COMMISSION_SEO-B3.md` |
| **SEO-B2** | Festival Pages (Holi, Diwali, Karwa Chauth) | B | Phase 2 | ✅ LIVE -- commit 963dc82 | `CODEX_COMMISSION_SEO-B2.md` |
| **SEO-C2** | Rashi Calculator + Nakshatra Calculator | C | Phase 4 | ✅ LIVE -- commit 963dc82 | `CODEX_COMMISSION_SEO-C2.md` |
| **SEO-C3** | Compatibility by Name | C | Phase 4 | ✅ LIVE -- commit 963dc82 | `CODEX_COMMISSION_SEO-C3.md` |
| **SEO-C4** | Ekadashi / Amavasya / Purnima Hub Pages | C | Phase 5 | ✅ LIVE -- commit 963dc82 | `CODEX_COMMISSION_SEO-C4.md` |
| **SEO-C5** | Marriage Muhurat Page | C | Phase 4 | ✅ LIVE -- commit 963dc82 | `CODEX_COMMISSION_SEO-C5.md` |
| **SEO-C6** | Report Category Discovery Pages (4 pages) | C | Phase 6 | 🟡 CODE LIVE -- launch gated (Razorpay live keys required) | `CODEX_COMMISSION_SEO-C6.md` |
| **SEO-C7** | Celebrity Horoscope Hub | C | Phase 7 | ✅ LIVE -- commit 963dc82 | `CODEX_COMMISSION_SEO-C7.md` |
| **SEO-C8** | Love Calculator | C | Phase 8 | ✅ LIVE -- commit 963dc82 | `CODEX_COMMISSION_SEO-C8.md` |
| **SEO-C9** | Angel Numbers Hub (14 pages) | C | Phase 8 | ✅ LIVE -- commit 963dc82 | `CODEX_COMMISSION_SEO-C9.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| SEO-OP-1 | **M-1: Replace OG image** -- `frontend/public/og-image.png` must be 1200×630 PNG ≤80 KB | TT | 🔴 HIGH | Current file is 626 KB at wrong ratio. Blocks social sharing quality. Must be fixed before SEO-1 |
| SEO-OP-2 | **Issue SEO-1 LAST** -- only after KE, KP, IR high-priority threads are running | TT | 🟢 LOW | SEO-1 scope: server-side meta, pre-render strategy, hreflang, Core Web Vitals, Vite migration assessment, service worker |
| SEO-OP-3 | **M-7: react-snap vs helmet-async** design decision needed before SEO-1 can start | TT | 🟢 LOW | Await SEO-1 thread recommendation |
| SEO-OP-4 | **M-8: PWA offline caching** -- decide if in scope | TT | 🟢 LOW | Await SEO-1 thread |
| SEO-OP-5 | **M-9: App.js lazy audit** -- confirm eager/lazy split: Landing + DailyHoroscope + Login eager, rest lazy | TT | 🟢 LOW | Minor perf gain, non-blocking |

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-04-30 | SEO-1 brief written. Foundation live (GA4, GSC, Bing, OG, JSON-LD). Tracker created. | CC | `CODEX_COMMISSION_SEO_WEBPERF.md` |
| v2.0 | 2026-05-20 | Full SEO commission plan added. 5 briefs written (SEO-C1, B1, B3, B2, C2, C4). Tracker updated with all 13 commissions. Legal page infra confirmed as already built. | CC | `SEO_Codex_Commission_Plan.md` |
| v2.1 | 2026-05-20 | SEO-C1 local delivery prepared without live writes. `PolicyPage.jsx` now marks legal pages `noindex`; `seed_policies_v1.py` now supports both legal-doc folders and injects compliance wording for Razorpay, Google Analytics, cookie controls, and 7-day unused-service refunds. | Codex | `CODEX_COMMISSION_SEO-C1.md` |
| v2.3 | 2026-05-20 | Remaining 6 briefs written (C3, C5, C6, C7, C8, C9). All 13 commissions now fully briefed. SEO-C6 reframed as category discovery pages -- individual report landings already exist in repo. | CC | -- |
| v2.2 | 2026-05-20 | SEO-B3 local delivery prepared. Added `/festivals`, `/calendar`, and `/hora` pages, plus the new `/api/panchang/hora` endpoint in `panchang_router.py`. Frontend production build passed. | Codex | `CODEX_COMMISSION_SEO-B3.md` |
| v2.4 | 2026-05-20 | SEO-B1 local delivery prepared. Added `tomorrow` horoscope support in `server.py`, new public per-sign routes for tomorrow/weekly/monthly, and `HoroscopeSignPage.jsx`. Frontend production build passed. | Codex | `CODEX_COMMISSION_SEO-B1.md` |
| v2.5 | 2026-05-20 | SEO-B2 local delivery prepared. Added `FestivalPage.jsx` plus explicit `/festivals/holi`, `/festivals/diwali`, and `/festivals/karwa-chauth` routes with Event + FAQ schema and dynamic Panchang-backed dates. Frontend production build passed. | Codex | `CODEX_COMMISSION_SEO-B2.md` |
| v2.6 | 2026-05-20 | SEO-C2 local delivery prepared. Added `/rashi-calculator` and `/nakshatra-calculator`, plus a thin `/api/calculate-birth-chart` alias route backed by `vedic_calculator.py`. Frontend production build and backend syntax checks passed. | Codex | `CODEX_COMMISSION_SEO-C2.md` |
| v2.7 | 2026-05-20 | SEO-C4 local delivery prepared. Added parameterised devotional date pages for `/ekadashi`, `/amavasya`, and `/purnima`, backed by existing Panchang festival and daily endpoints with Event + FAQ schema. Frontend production build passed. | Codex | `CODEX_COMMISSION_SEO-C4.md` |
| v2.8 | 2026-05-20 | SEO-C3 local delivery prepared. Added a pure-Python `/api/numerology/name-compatibility` endpoint in `numerology_router.py` and public `/compatibility/name` with query-string sharing, copy-link UX, and FAQ schema. Frontend production build and backend syntax checks passed. | Codex | `CODEX_COMMISSION_SEO-C3.md` |
| v2.9 | 2026-05-20 | SEO-C5 local delivery prepared. Added cached `/api/panchang/muhurat/marriage` for New Delhi reference dates plus public `/muhurat/marriage` with year switching, month tabs, Panchang links, and FAQ schema. Frontend production build passed and backend source compiled locally. | Codex | `CODEX_COMMISSION_SEO-C5.md` |
| v3.0 | 2026-05-20 | SEO-C7 local delivery prepared. Added cached celebrity chart endpoints in `server.py` plus public `/celebrity-horoscopes` hub and `/:slug` detail pages with Person schema, category filters, and Vedic chart summaries sourced from `vedic_calculator.py`. Frontend production build passed and backend source compiled locally. | Codex | `CODEX_COMMISSION_SEO-C7.md` |
| v3.1 | 2026-05-20 | SEO-C6, SEO-C8, and SEO-C9 local deliveries prepared. Added 4 public report-category discovery pages, public `/love-calculator` with shareable URL support plus a top-level API alias, and the full `/angel-numbers` hub with 14 static detail pages, FAQ schema, and article metadata. Frontend production build passed and backend AST syntax checks passed. | Codex | `CODEX_COMMISSION_SEO-C6.md` · `CODEX_COMMISSION_SEO-C8.md` · `CODEX_COMMISSION_SEO-C9.md` |
| v3.2 | 2026-05-20 | All 12 SEO commissions integrated and pushed to main (commit 963dc82). 13 new pages live. Policy seed run against production MongoDB (5 docs). OG image replaced (<82KB, 1200×630). SEO-C6 code live but launch gated on Razorpay live keys. SEO-WebPerf held for last. | CC | -- |
