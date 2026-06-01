# SEO & Web Performance -- Module Tracker
> Update this file at the end of every session that touches this module.
> Last updated: 2026-06-02 · v5.5 (M3-CP-FIX v2 re-scan: L1 62.7% FLAGGED, still failing. v3 brief issued with chart-point-native architecture separation. Sequence blocked at M3-CP-FIX pending v3 delivery.)

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- prior SEO wave live; SEO-20K M4 local delivery and TAR-SEO-2 data rewrite prepared after M3 integration |
| **GA4** | G-3HJC8BTHRQ -- wired and live |
| **GSC** | Verified + sitemap submitted |
| **Bing** | Verified + sitemap submitted |
| **OG tags** | Present on all major pages |
| **JSON-LD** | Present on all major routes |
| **SEO component** | `frontend/src/components/SEO.jsx` -- used sitewide |
| **Sitemap** | `frontend/public/sitemap-index.xml` + backend-served dynamic sitemap routes |

---

## Commission Status

| ID | Commission | Track | Priority | Status | Brief |
|---|---|---|---|---|---|
| **SEO-WebPerf** | SEO + Marketing + Web Performance Optimisation | -- | Issue Last | 🟣 READY -- ISSUE LAST | `CODEX_COMMISSION_SEO_WEBPERF.md` |
| **SEO-20K** | 22,170 Programmatic SEO Pages + Web Performance (Umbrella) | SEO | M1-M4 | 🟡 IN PROGRESS -- M1 ✅ `2a4ed4e` · M2 ✅ `aba7d5c` · M3 integrated by TT · M4 local delivery prepared (Tarot SEO 199 pages) | `CODEX_COMMISSION_SEO_20K.md` |
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
| ~~SEO-OP-6~~ | ~~**SEO-20K M2 review**~~ | CC | ✅ DONE | CC reviewed, committed, and pushed `aba7d5c`. `compatibility_router.py` (214 lines, ashtakoot via vedic_calculator), `remedy_matching_router.py` (204 lines, 12 dosha slugs), `CompatibilityPage.jsx`, `RemedyHubPage.jsx`, server.py wiring, seo_router.py sitemap, App.js routes, vercel.json cache headers, sitemap-index.xml updated. Build clean. |
| SEO-OP-7 | **TT production smoke test** -- `/compatibility/aries-and-scorpio/` and `/remedies/shani-sade-sati/` | TT | 🟠 MED | After Render deploy settles (~3 min from push). Verify pages render, ashtakoot score appears, dosha content loads, JSON-LD in source. |

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
| v3.3 | 2026-05-22 | SEO-20K M1 local delivery prepared. Added dynamic sitemap endpoints in `backend/seo_router.py`, upgraded `SEO.jsx` with canonical/hreflang/JSON-LD support, added `/panchang/:citySlug/:date` and `/choghadiya/:citySlug/:period`, created `sitemap-index.xml`, updated robots, added Vercel route cache headers, and wrote `docs/SEO_WEBPERF_REPORT.md` plus `docs/SEO_30DAY_PLAN.md`. Frontend production build passed and backend AST syntax checks passed. No live production changes in this session. | Codex | `CODEX_COMMISSION_SEO_20K.md` |
| v3.4 | 2026-05-22 | SEO-20K M2 local delivery prepared. Added sign-pair compatibility pages, remedy hub pages, new backend compatibility and remedy-matching routers, compatibility/remedies sitemap endpoints, `App.js` public routes, and Vercel cache headers for the new programmatic route groups. No live production changes in this session. | Codex | `CODEX_COMMISSION_SEO_20K.md` |
| v3.5 | 2026-05-22 | SEO-20K M2 INTEGRATED. CC reviewed `compatibility_router.py` (no architecture violations -- uses `vedic_calculator.calculate_ashtakoot()`), `remedy_matching_router.py` (no KE/dasha imports), `CompatibilityPage.jsx`, `RemedyHubPage.jsx`. All 9 files committed `aba7d5c` and pushed to main. M2 confirmation sent to SEO Codex thread requesting M3. SEO-OP-6 closed. SEO-OP-7 (TT production smoke test) opened. | CC | `aba7d5c` |
| v3.6 | 2026-05-23 | SEO-20K M3 local delivery prepared. Added `seo_m3_router.py`, shared SEO M3 catalog/builders, seed scripts for `transit_profiles`, `festival_region_pages`, and `character_placements`, public React pages for `/transits/:transitSlug`, `/festivals/:festivalSlug/:region`, and `/traits/:sign/:chartPoint/:house`, plus transits/festivals/traits sitemap endpoints and Vercel cache headers. Seed dry-runs returned 108 transit docs, 480 festival-region docs, and 432 character-placement docs. Frontend production build passed and backend syntax checks passed. No live production changes in this session. | Codex | `CODEX_COMMISSION_SEO_20K_M3.md` |
| v3.7 | 2026-05-25 | SEO-20K M4 / TAR-SEO-1 local delivery prepared. Added `backend/tarot_seo_router.py`, tarot sitemap support in `backend/seo_router.py`, `server.py` router wiring, four new public React pages under `frontend/src/pages/tarot-seo/`, public routes for `/tarot/spreads`, `/tarot/spread/:spreadSlug`, `/tarot/card/:cardSlug`, and `/tarot/for/:intentionSlug`, plus Vercel cache headers and sitemap-index wiring. Frontend production build passed, backend syntax checks passed, and the interactive `/tarot` module remained untouched. | Codex | `Tarot/CODEX_COMMISSION_TAR_SEO_1.md` |
| v3.8 | 2026-05-25 | TAR-SEO-2 local data rewrite prepared as a follow-on fix to M4. Reworked only `backend/tarot_seo_data.py` to replace source-derived spread prose and rigid card templates. `py_compile` passed, legacy repeated phrases were removed, and record counts remained `100` spreads, `78` cards, `20` intentions. No router, frontend, or wiring files changed in this session. | Codex | `Tarot/CODEX_COMMISSION_TAR_SEO_2_REWRITE.md` |
| v4.0 | 2026-05-29 | QA reconciliation completed. Final master status table + ECHO/PACE score framework added. M3-FIX-1 and TAR-SEO-1 flagged as live integration gaps. | TT | This session |
| v5.0 | 2026-05-31 | ECHO/PACE scans run for RUD-1, CRY-1, FAITH-20K, Angel Numbers. Paid API column added. Full scores recorded. Commission briefs written: RUD-L2, CRY-L2, FAITH-REWRITE, ANGEL-3. | CC | Session 12 |
| v5.1 | 2026-05-31 | ECHO/PACE scans run for all 7 SEO-20K infrastructure modules. Scores recorded for City Panchang (N/A), Choghadiya (N/A), Sign Compatibility, Remedy Hub, Transit Profiles, Character Placements, Festival Regions, Per-Sign Horoscopes (meta), Festival/Calendar. | CC | Session 12 |
| v5.2 | 2026-05-31 | ECHO/PACE scans run for SEO-C pooled (14 pages) and all 3 Tarot SEO page types (198 pages). Full scores added to ECHO/PACE table. Failing modules listed in "Commissions Pending" table. | CC | Session 12 |
| v5.5 | 2026-06-02 | M3-CP-FIX v2 re-scan: L1 62.7% FLAGGED (improvement from 94.4% but still failing). New L2 violations: "house turns attention toward" 100%, "blend makes house site" 43%, "life themes revolve around" 42%. Worst pair: Scorpio Moon 2H vs Scorpio Sun 2H. v3 brief issued -- chart-point-native architecture (Sun=identity, Moon=emotion, Rising=presentation), all new stems to be deleted. Sequence blocked at M3-CP-FIX. | CC | `CODEX_COMMISSION_M3_CP_FIX.md` v3 |
| v5.4 | 2026-06-02 | RUD-L2 delivered by Codex + verified. `rudraksha_content.py` rewritten. Re-scan: Mukhi L1=25.2%, Planet L1=11.7%, Problem L1=17.5%, Sign L1=6.0% -- all L2/L3 PASS. Module unblocked. Rudraksha rows updated in ECHO/PACE table. | CC | `CODEX_COMMISSION_RUD_L2.md` |
| v5.3 | 2026-05-31 | Fix commission briefs written for all 4 failing SEO module clusters: M3-CP-FIX (Character Placements, CRITICAL), M3-TR-FIX (Transit Profiles, BLOCKED), M2-COMPAT-FIX (Sign Compatibility, FLAGGED), TAR-SEO-FIX (Tarot Spreads+Cards+Intentions, L2/L3 FAIL). Briefs in `Codex_Deliveries/SEO/`. "Commissions Pending" table updated with all 8 open commissions. | CC | Session 12 |

---

## Final Master Status Table -- All SEO Commissions

> Status as of 2026-05-29 (reconciled vs CODEX_QA_INTEGRATION_AUDIT_2026-05-27)

| Commission ID | Name | Pages / Scope | Integration Status | Live URL (sample) | Open Gaps |
|---|---|---|---|---|---|
| **SEO-20K M1** | SEO infra + City Panchang + Choghadiya | ~2,000 city-date panchang + ~600 choghadiya pages | ✅ LIVE | `/panchang/new-delhi-india/2026-05-27` | None |
| **SEO-20K M2** | Compatibility Hub + Remedy Hub | ~144 sign-pair + ~12 remedy pages | ✅ LIVE `aba7d5c` | `/compatibility/aries-and-scorpio` | None |
| **SEO-20K M3** | Transit Profiles + Festival Regions + Character Placements | 108 transits + 480 festival-regions + 432 character placements = ~1,020 pages | ✅ LIVE (integrated by TT) | `/transits/sun-in-aries` | **M3-FIX-1**: festival-region summary variation fix local only -- not integrated |
| **SEO-20K M4 / TAR-SEO-1** | Tarot SEO Hub + 199 programmatic pages (spreads, cards, intentions) | 199 programmatic pages + hub + sitemap | 🟠 LOCAL DELIVERY -- NOT INTEGRATED | N/A | **TT to integrate from `Codex_Deliveries/Tarot/`** |
| **TAR-SEO-2** | Tarot SEO data rewrite (`tarot_seo_data.py`) | Data quality fix only | 🟡 BLOCKED on TAR-SEO-1 | N/A | Depends on TAR-SEO-1 merge |
| **SEO-B1** | Tomorrow / Weekly / Monthly per-sign horoscope (36 pages) | 36 pages | ✅ LIVE `963dc82` | `/horoscope/aries/tomorrow` | None |
| **SEO-B2** | Festival Pages (Holi, Diwali, Karwa Chauth) | 3 pages | ✅ LIVE `963dc82` | `/festivals/holi` | None |
| **SEO-B3** | Festival Hub + Indian Calendar + Hora Today | 3 hub pages | ✅ LIVE `963dc82` | `/festivals`, `/calendar`, `/hora` | None |
| **SEO-C1** | Legal Pages (noindex + policy seed) | 5 legal pages | ✅ LIVE `963dc82` | `/privacy`, `/terms` | None |
| **SEO-C2** | Rashi Calculator + Nakshatra Calculator | 2 pages | ✅ LIVE `963dc82` | `/rashi-calculator` | None |
| **SEO-C3** | Name Compatibility | 1 page | ✅ LIVE `963dc82` | `/compatibility/name` | None |
| **SEO-C4** | Ekadashi / Amavasya / Purnima Hubs | 3 pages | ✅ LIVE `963dc82` | `/ekadashi` | None |
| **SEO-C5** | Marriage Muhurat Page | 1 page | ✅ LIVE `963dc82` | `/muhurat/marriage` | None |
| **SEO-C6** | Report Category Discovery Pages | 4 pages | 🟡 CODE LIVE -- launch gated | `/reports/kundali` | Razorpay live keys required |
| **SEO-C7** | Celebrity Horoscope Hub | 2 pages (hub + detail template) | ✅ LIVE `963dc82` | `/celebrity-horoscopes` | None |
| **SEO-C8** | Love Calculator | 1 page | ✅ LIVE `963dc82` | `/love-calculator` | None |
| **SEO-C9** | Angel Numbers Hub (14 pages) | 14 pages | ✅ LIVE (code) | `/angel-numbers` | ANGEL-2 content not re-seeded -- stale Mongo content in production |
| **SEO-WebPerf** | SEO + Marketing + Web Performance Optimisation | Platform-wide | 🟣 READY TO ISSUE LAST | N/A | Issue after all high-priority threads running |
| **ECHO-1** | ECHO/PACE Admin Engine + tab | Admin tool | 🟡 PARTIAL -- backend live, UI not in bundle | `/api/admin/echo-pace/history` | **ECHO-UI-1**: frontend tab not deployed |

**Total pages across all live SEO commissions:** ~4,300+ programmatic + ~55 editorial (excl. TAR-SEO-1 pending)
**Total pages in pipeline (delivered, pre-seed):** ~16,800 Faith + ~10,001 Angel Numbers + ~62 Rudraksha + ~70 Crystal = ~26,933 additional pages pending scan clearance

---

## ECHO/PACE Score Table

> **Layers:** L1 = TF-IDF cosine (PASS < 50% · FLAGGED 50-69% · BLOCKED ≥ 70%) | L2 = 4-gram phrase match (PASS = 0 violations in > 15% of pages) | L3 = Jaccard title similarity (PASS < 60%) | Layer G = Google exact-phrase hits (PASS ≤ 1 hit)
> **Script location:** `tests/echo_pace_[module]_scan.py` per module
> **Scan date column:** date the test was last run. Blank = not yet run.

### SEO-20K Modules (infrastructure + editorial)

> Scan script: `tests/echo_pace_seo20k_scan.py` | Last run: 2026-05-31
> **Paid API Column** -- "YES" = Anthropic/Claude API called on every live page render (token cost per user request). "NO" = pyswisseph local compute / MongoDB query / static data only.

| Commission | Page Type | Pages | Paid API? | L1 Score | L1 Status | L2 Violations | L2 Status | L3 Worst Jaccard | L3 Status | Layer G | Scan Date | Next Action |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SEO-20K M1 | **City Panchang** | ~2,000 | ❌ NO (pyswisseph) | N/A | ✅ N/A -- live computed | N/A | ✅ N/A -- unique per city+date | N/A | ✅ N/A | ⬜ Not run | 2026-05-31 | No static content risk -- monitor via GSC |
| SEO-20K M1 | **Choghadiya** | ~600 | ❌ NO (pyswisseph) | N/A | ✅ N/A -- live computed | N/A | ✅ N/A -- unique per city+date | N/A | ✅ N/A | ⬜ Not run | 2026-05-31 | No static content risk -- monitor via GSC |
| SEO-20K M2 | **Sign Compatibility** | 144 | ❌ NO (vedic_calculator) | 50.0% | ⚠️ FLAGGED | 10 at 100% freq | ❌ FAIL | 75% | ⚠️ FLAGGED | ⬜ Not run | 2026-05-31 | Issue fix commission -- koota narrative template variation |
| SEO-20K M2 | **Remedy Hub** | 12 | ❌ NO (MongoDB read) | 15.4% | ✅ PASS | 0 | ✅ PASS | < 60% | ✅ PASS | ⬜ Not run | 2026-05-31 | ✅ Clear -- run Layer G before seeding |
| SEO-20K M3 | **Transit Profiles** | 108 | ❌ NO (static generator) | 71.2% | ❌ BLOCKED | 10 at 100% freq | ❌ FAIL | 67% | ⚠️ FLAGGED | ⬜ Not run | 2026-05-31 | Issue fix commission -- transit narrative pool expansion |
| SEO-20K M3 | **Festival Regions** | 480 | ❌ NO (static generator) | 64.5% | ⚠️ FLAGGED | 10 at 100% freq | ❌ FAIL | 75% | ⚠️ FLAGGED | ⬜ Not run | 2026-05-31 | M3-FIX-1 still not integrated -- fix L2 boilerplate too |
| SEO-20K M3 | **Character Placements** | 432 | ❌ NO (static generator) | 93.4% | ❌ BLOCKED | 10 at 100% freq | ❌ FAIL | 100% | ⚠️ FLAGGED | ⬜ Not run | 2026-05-31 | Issue fix commission -- critical, worst score in full scan |
| SEO-B1 | **Per-Sign Horoscopes** (meta layer) | 36 | ✅ YES (claude-sonnet-4 per request) | 62.5% | ⚠️ FLAGGED (meta only) | 10 at 33% freq | ❌ FAIL (meta) | 71% | ⚠️ FLAGGED | ⬜ Not run | 2026-05-31 | Fix meta title templates -- LLM body not scanned (unique per run) |
| SEO-B2/B3 | **Festival / Calendar / Hora** | 5 | ❌ NO (panchang live dates only) | 12.1% | ✅ PASS | 10 at 20% freq | ⚠️ Minor (3-page set) | < 60% | ✅ PASS | ⬜ Not run | 2026-05-31 | ✅ Acceptable -- small page set, low duplication risk |
| SEO-C series | **SEO-C pooled** (all 14 editorial pages) | 14 | ❌ NO | 43.2% | ✅ PASS | 0 | ✅ PASS | 71% (Name Compat vs Love Calc) | ⚠️ Minor | ⬜ Not run | 2026-05-31 | Fix meta title tail -- "Vedic Numerology Match" duplicated across 2 pages |
| TAR-SEO-1/2 | **Tarot Spreads** | 100 | ❌ NO (static data) | 32.9% | ✅ PASS | 6 at 100% freq | ❌ FAIL | 70% (2 isolation titles) | ⚠️ Minor | ⬜ Not run | 2026-05-31 | Vary spread intro sentence ("page reads spread card layout" 100%) |
| TAR-SEO-1/2 | **Tarot Cards** | 78 | ❌ NO (static data) | 34.8% | ✅ PASS | 0 | ✅ PASS | 75% (same-suit cards) | ⚠️ FLAGGED | ⬜ Not run | 2026-05-31 | Fix meta_title -- "minor Meaning & Guide" tail identical for all minor arcana |
| TAR-SEO-1/2 | **Tarot Intentions** | 20 | ❌ NO (static data) | 14.2% | ✅ PASS | 10 at 100% freq | ❌ FAIL | 75% (Love/Career/Money/Health) | ⚠️ FLAGGED | ⬜ Not run | 2026-05-31 | Vary intro sentence + diversify meta title beyond "Best Tarot Spreads for X" |

**Modules needing fix commissions from this scan:**

| Module | Commission ID | Severity | Root Cause | Brief Location |
|---|---|---|---|---|
| Character Placements | M3-CP-FIX | 🔴 CRITICAL (L1 = 93.4%) | `build_character_placement_doc()` shares fixed trait/theme boilerplate across all sign×chartpoint×house combos | Draft brief in `Codex_Deliveries/SEO/` |
| Transit Profiles | M3-TR-FIX | 🔴 BLOCKED (L1 = 71.2%) | `build_transit_profile_doc()` uses fixed FAQ + narrative pool -- same phrases on all 108 pages | Draft brief in `Codex_Deliveries/SEO/` |
| Sign Compatibility | M2-COMPAT-FIX | ⚠️ FLAGGED (L1 = 50.0%) | `_koota_narrative()` and `_build_summary()` use fixed templates -- all 144 pages share structural vocabulary | Draft brief in `Codex_Deliveries/SEO/` |
| Festival Regions | M3-FIX-1 (existing) | ⚠️ FLAGGED (L1 = 64.5%) | L2 boilerplate still present after M3-FIX-1 -- M3-FIX-1 not yet integrated either | `backend/seo_m3_builders.py` -- integrate M3-FIX-1 first then reassess |
| Per-Sign Horoscopes | SEO-B1-META-FIX | ⚠️ FLAGGED (meta layer) | Title/description templates share too much vocabulary across the 36 sign×period pages | Vary PERIOD_META description templates per sign element (Fire/Earth/Air/Water) |

### Programmatic SEO Modules (scanned 2026-05-31)

| Module | Commission | Page Type | Pages | L1 Score | L1 Status | L2 Violations | L2 Status | L3 Worst Jaccard | L3 Status | Layer G | Seed OK? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Lo Shu Grid** | LSG-1/2 | All (57 URLs) | 57 | ✅ PASS | ✅ PASS | 0 | ✅ PASS | < 60% | ✅ PASS | ✅ PASS | ✅ YES -- Live |
| **Angel Numbers** | ANGEL-2 | Core numbers | 1,000 | 45-57% | ❌ FAIL (gate < 40%) | 0 | ✅ PASS | < 60% | ✅ PASS | ⬜ Not run | ❌ Blocked -- ANGEL-3 |
| **Angel Numbers** | ANGEL-2 | Intent pages | 9,000 | 45-57% | ❌ FAIL (gate < 40%) | 0 | ✅ PASS | < 60% | ✅ PASS | ⬜ Not run | ❌ Blocked -- ANGEL-3 |
| **Rudraksha** | RUD-L2 ✅ | Mukhi (1-21) | 21 | **25.2%** | ✅ PASS | **0** | ✅ PASS | **0 pairs >60%** | ✅ PASS | ⬜ Not run | 🟠 Pending App.js + seed |
| **Rudraksha** | RUD-L2 ✅ | Planet (9) | 9 | **11.7%** | ✅ PASS | **0** | ✅ PASS | **0 pairs >60%** | ✅ PASS | ⬜ Not run | 🟠 Pending App.js + seed |
| **Rudraksha** | RUD-L2 ✅ | Problem (20) | 20 | **17.5%** | ✅ PASS | **0** | ✅ PASS | **0 pairs >60%** | ✅ PASS | ⬜ Not run | 🟠 Pending App.js + seed |
| **Rudraksha** | RUD-L2 ✅ | Sign (12) | 12 | **6.0%** | ✅ PASS | **0** | ✅ PASS | **0 pairs >60%** | ✅ PASS | ⬜ Not run | 🟠 Pending App.js + seed |
| **Crystal Healing** | CRY-1 | Crystal profiles | 50 | 47.7% ⚠️ | ✅ PASS (borderline) | 10 at 100% | ❌ FAIL | 88% | ⚠️ FLAGGED | ⬜ Not run | ❌ Blocked -- CRY-L2 |
| **Crystal Healing** | CRY-1 | Intention guides | 20 | 20.8% | ✅ PASS | 10 at 100% | ❌ FAIL | 71% | ⚠️ FLAGGED | ⬜ Not run | ❌ Blocked -- CRY-L2 |
| **Faith** | FAITH-20K | Gita × Situation | 10,500 | **100.0%** | ❌ BLOCKED | 10 at 100% | ❌ FAIL | 100% | ⚠️ FLAGGED | ⬜ Not run | ❌ Blocked -- FAITH-REWRITE |
| **Faith** | FAITH-20K | Bible × Transition | 6,000 | **81.7%** | ❌ BLOCKED | 10 at 100% | ❌ FAIL | 67% | ⚠️ FLAGGED | ⬜ Not run | ❌ Blocked -- FAITH-REWRITE |
| **Faith** | FAITH-20K | Transit pages | 156 | **99.5%** | ❌ BLOCKED | 10 at 100% | ❌ FAIL | 71% | ⚠️ FLAGGED | ⬜ Not run | ❌ Blocked -- FAITH-REWRITE |
| **Faith** | FAITH-20K | Daily pages | 144 | 50.0% ⚠️ | ⚠️ ON GATE | 5 at 100% | ❌ FAIL | 75% | ⚠️ FLAGGED | ⬜ Not run | ❌ Blocked -- FAITH-REWRITE |

### Commissions Pending -- Rework Required

| Module | Commission | Issue | Brief | Priority |
|---|---|---|---|---|
| Angel Numbers | **ANGEL-3** | L1 still 45-57% (gate < 40%). 8 vocabulary pools need expansion + digit-pattern anchoring. | `Codex_Deliveries/Angel_Numbers/CODEX_COMMISSION_ANGEL_3_L1_FIX.md` | 🔴 READY TO ISSUE |
| ~~Rudraksha~~ | ~~**RUD-L2**~~ | ~~L2 FAIL (100% FAQ boilerplate). L3 FLAGGED (digit meta titles).~~ | `Codex_Deliveries/Rudraksha/CODEX_COMMISSION_RUD_L2.md` | ✅ INTEGRATED 2026-06-02 -- all layers PASS |
| Crystal Healing | **CRY-L2** | L2 FAIL (100% caution/FAQ boilerplate). L3 FLAGGED. L1 borderline -- must not regress. | `Codex_Deliveries/Crystal_Healing/CODEX_COMMISSION_CRY_L2.md` | 🔴 READY TO ISSUE |
| Faith & Scripture | **FAITH-REWRITE** | L1 CRITICAL: Gita 100%, Bible 82%, Transit 100%. Fixed situation/topic boilerplate dominates body text. | `Codex_Deliveries/Faith_Hubs/CODEX_COMMISSION_FAITH_REWRITE.md` | 🔴 READY TO ISSUE -- CRITICAL |
| Character Placements | **M3-CP-FIX** | L1 93.4% BLOCKED. Fixed trait/theme boilerplate per sign×chartpoint -- house index is only variable. L2 FAIL. L3 100%. | `Codex_Deliveries/SEO/CODEX_COMMISSION_M3_CP_FIX.md` | 🔴 READY TO ISSUE -- CRITICAL |
| Transit Profiles | **M3-TR-FIX** | L1 71.2% BLOCKED. Shared narrative pool exhausted -- same phrases on all 108 planet×sign pages. L2 FAIL. | `Codex_Deliveries/SEO/CODEX_COMMISSION_M3_TR_FIX.md` | 🔴 READY TO ISSUE |
| Sign Compatibility | **M2-COMPAT-FIX** | L1 50.0% FLAGGED (on gate -- must go below). Fixed koota narrative templates. L2 FAIL. L3 75%. | `Codex_Deliveries/SEO/CODEX_COMMISSION_M2_COMPAT_FIX.md` | 🟠 READY TO ISSUE |
| Tarot SEO | **TAR-SEO-FIX** | Spreads L2 FAIL ("page reads spread card layout" 100%). Cards L3 FLAGGED (minor arcana titles). Intentions L2+L3 FAIL. | `Codex_Deliveries/SEO/CODEX_COMMISSION_TAR_SEO_FIX.md` | 🟠 READY TO ISSUE |

---

## Version History

| Version | Date | What Changed | By |
|---|---|---|---|
| v5.2 | 2026-05-31 | ECHO/PACE scans run for SEO-C series (14 pooled pages) + TAR-SEO-1/2 (198 pages) via `tests/echo_pace_seoc_tarot_scan.py`. SEO-C L1 43.2% PASS, L2 PASS, L3 minor flag (Name Compat vs Love Calc title). Tarot: Spreads L1 32.9% PASS, L2 FAIL (intro boilerplate). Cards L1 34.8% PASS, L3 FLAGGED (same-suit title). Intentions L1 14.2% PASS, L2+L3 FAIL. Fix commissions needed for Tarot. | CC |
| v5.1 | 2026-05-31 | ECHO/PACE scans run for all 7 SEO-20K infrastructure modules via `tests/echo_pace_seo20k_scan.py`. Results: Remedy Hub ✅ PASS · Festival/Hora ✅ PASS · Sign Compatibility ⚠️ FLAGGED (50.0%) · Festival Regions ⚠️ FLAGGED (64.5%) · Per-Sign Horoscopes ⚠️ FLAGGED (meta 62.5%) · Transit Profiles ❌ BLOCKED (71.2%) · Character Placements ❌ CRITICAL (93.4%). Paid API column added. 5 new fix commissions identified. | CC |
| v5.0 | 2026-05-31 | ECHO/PACE scans run for RUD-1 (62 pages), CRY-1 (70 pages), FAITH-20K (16,800 pages, sampled). Angel Numbers ANGEL-2 L1 scores recorded. All results added to score table. 4 new commission briefs ready to issue (ANGEL-3, RUD-LG2, CRY-L2, FAITH-REWRITE). Scan scripts created: `tests/echo_pace_rud_scan.py`, `tests/echo_pace_cry_scan.py`, `tests/echo_pace_faith_scan.py`. | CC |
| v4.0 | 2026-05-29 | QA reconciliation completed. Final master status table + ECHO/PACE score framework added. M3-FIX-1 and TAR-SEO-1 flagged as live integration gaps. | TT |

**M3 Festival Regions -- ECHO history:**
- 9 rounds of GAI-assisted content optimisation completed to reduce inter-page duplication below 40% ceiling
- Fix batch (M3-FIX-1) is in `backend/seo_m3_builders.py` locally but not yet integrated to production
- Integration of M3-FIX-1 is REQUIRED before running formal ECHO/PACE audit on festival-region pages
