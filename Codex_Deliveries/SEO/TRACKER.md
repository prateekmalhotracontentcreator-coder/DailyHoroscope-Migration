# SEO & Web Performance -- Module Tracker
> Path: `Codex_Deliveries/SEO/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-15 · v1.0

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟣 PLANNED -- foundations live, comprehensive thread pending |
| **GA4** | G-3HJC8BTHRQ -- wired and live |
| **GSC** | Verified + sitemap submitted |
| **Bing** | Verified + sitemap submitted |
| **OG tags** | Present on all major pages |
| **JSON-LD** | Present on all major routes |
| **SEO component** | `frontend/src/components/SEO.jsx` -- used sitewide |
| **Sitemap** | `frontend/public/sitemap.xml` |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| **SEO-1** | SEO + Marketing + Web Performance Optimisation | 🟣 READY TO ISSUE -- ⚠️ ISSUE LAST | `CODEX_COMMISSION_SEO_WEBPERF.md` |

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
