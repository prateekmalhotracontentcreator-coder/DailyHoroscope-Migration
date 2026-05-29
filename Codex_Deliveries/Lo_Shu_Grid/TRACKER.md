# Lo Shu Grid -- Module Tracker
> Path: `Codex_Deliveries/Lo_Shu_Grid/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-25 IST · v2.0

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- LSG-2 local expansion prepared, build-verified, Temple review pending |
| **Backend router** | `backend/lo_shu_router.py` |
| **Seed script** | `backend/scripts/seed_lo_shu.py` |
| **SEO sitemap** | `GET /api/seo/sitemap/lo-shu-grid` via `backend/seo_router.py` |
| **Frontend pages** | `frontend/src/pages/lo_shu_grid/LoShuHubPage.jsx`, `LoShuCalculatorPage.jsx`, `LoShuMissingNumberPage.jsx`, `LoShuArrowPage.jsx`, `LoShuNumberPage.jsx`, `LoShuProblemPage.jsx`, `LoShuPersonalYearPage.jsx` |
| **Shared UI** | `frontend/src/components/lo-shu/LoShuGridBoard.jsx` |
| **Collections** | `lo_shu_missing_numbers`, `lo_shu_arrows`, `lo_shu_numbers`, `lo_shu_problems`, `lo_shu_personal_years` |
| **Public routes** | `/lo-shu-grid`, `/lo-shu-grid/calculator`, `/lo-shu-grid/missing-:number`, `/lo-shu-grid/arrow/:slug`, `/lo-shu-grid/number/:n`, `/lo-shu-grid/for/:problem`, `/lo-shu-grid/personal-year/:n` |
| **Lo Shu sitemap size** | `57` URLs (`19` from LSG-1 + `38` from LSG-2) |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| **LSG-1** | Lo Shu Grid Calculator + Hub + 9 Missing Number + 8 Arrow Pages | ✅ PREREQUISITE INTEGRATED | `CODEX_COMMISSION_LO_SHU_GRID.md` |
| **LSG-2** | Lo Shu Grid Expansion -- 9 Number Pages + 20 Problem Pages + 9 Personal Year Pages | 🟠 ECHO/PACE PASSED -- awaiting TT sign-off on `LSG_INTEGRATION_SIGNOFF_NOTE_2026-05-29.docx` | `CODEX_COMMISSION_LSG_2_EXPANSION.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| LSG-OP-1 | Confirm runtime assumption for the missing Action arrow | TT | 🟠 MED | Decoded source labels one missing arrow as `8,7,6`, but Lo Shu grid geometry and commission math imply `2,7,6`. Runtime logic follows `2,7,6`. |
| LSG-OP-2 | Seed Lo Shu content collections on target DB if Temple wants Mongo-backed page content immediately | TT | 🟡 MED | `python3 backend/scripts/seed_lo_shu.py --mongo-url "$MONGO_URL" --db-name horoscope_db` now seeds `lo_shu_missing_numbers`, `lo_shu_arrows`, `lo_shu_numbers`, `lo_shu_problems`, and `lo_shu_personal_years`. |
| LSG-OP-3 | Browser smoke test public routes after Render/Vercel deploy | TT | 🟠 HIGH | Verify hub, calculator, one missing-number page, one arrow page, one number page, one problem page, one personal-year page, and `/api/seo/sitemap/lo-shu-grid`. Full 8-item checklist in `LSG_INTEGRATION_SIGNOFF_NOTE_2026-05-29.docx` Section 4. |
| LSG-OP-4 | ECHO/PACE scanner coverage gap | CC | 🟡 MED | `echo_pace_lsg_scan.py` covers number pages + combination pairs only. Does not cover `lo_shu_problems` (20 pages) or `lo_shu_personal_years` (9 pages). Layer G thread check shows 0/10 hits across all page types -- acceptable given clean result, but scanner should be extended if content changes post-integration. |

---

## Verification

- Backend verification: `PYTHONPYCACHEPREFIX=/private/tmp/lo_shu_pycache backend/.venv/bin/python -m py_compile` passed for `backend/lo_shu_router.py`, `backend/seo_router.py`, and `backend/scripts/seed_lo_shu.py`
- Seed verification: `backend/.venv/bin/python backend/scripts/seed_lo_shu.py --dry-run` reported `9` missing-number docs, `8` arrow docs, `9` number docs, `20` problem docs, and `9` personal-year docs
- Sitemap verification: `len(LO_SHU_SITEMAP_URLS) == 57`
- Frontend verification: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` passed in `frontend/`
- Runtime note: page endpoints fall back to in-code content if Mongo seed data has not been inserted yet

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v2.0 | 2026-05-25 | LSG-2 delivered locally. Expanded the Lo Shu module with 9 number deep-dive pages, 20 problem-area pages, 9 personal-year pages, new backend endpoints, expanded seed coverage, hub discoverability links, and a 57-URL Lo Shu sitemap. Backend compile, seed dry-run, sitemap count, and frontend production build passed. | Codex | `CODEX_COMMISSION_LSG_2_EXPANSION.md` |
| v1.0 | 2026-05-23 | LSG-1 delivered locally. Added dedicated Lo Shu backend router, SEO sitemap endpoint, Mongo seed script, four public frontend pages, shared grid component, App routes, sitemap index entry, and Vercel cache headers. Backend compile and frontend production build passed. | Codex | `CODEX_COMMISSION_LO_SHU_GRID.md` |
