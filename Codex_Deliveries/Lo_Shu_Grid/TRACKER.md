# Lo Shu Grid -- Module Tracker
> Path: `Codex_Deliveries/Lo_Shu_Grid/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-23 IST · v1.0

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- LSG-1 local delivery prepared, build-verified, Temple review pending |
| **Backend router** | `backend/lo_shu_router.py` |
| **Seed script** | `backend/scripts/seed_lo_shu.py` |
| **SEO sitemap** | `GET /api/seo/sitemap/lo-shu-grid` via `backend/seo_router.py` |
| **Frontend pages** | `frontend/src/pages/lo_shu_grid/LoShuHubPage.jsx`, `LoShuCalculatorPage.jsx`, `LoShuMissingNumberPage.jsx`, `LoShuArrowPage.jsx` |
| **Shared UI** | `frontend/src/components/lo-shu/LoShuGridBoard.jsx` |
| **Collections** | `lo_shu_missing_numbers`, `lo_shu_arrows` |
| **Public routes** | `/lo-shu-grid`, `/lo-shu-grid/calculator`, `/lo-shu-grid/missing-:number`, `/lo-shu-grid/arrow/:slug` |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| **LSG-1** | Lo Shu Grid Calculator + Hub + 9 Missing Number + 8 Arrow Pages | 🟡 DELIVERED LOCALLY -- Temple review pending | `CODEX_COMMISSION_LO_SHU_GRID.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| LSG-OP-1 | Confirm runtime assumption for the missing Action arrow | TT | 🟠 MED | Decoded source labels one missing arrow as `8,7,6`, but Lo Shu grid geometry and commission math imply `2,7,6`. Runtime logic follows `2,7,6`. |
| LSG-OP-2 | Seed Lo Shu content collections on target DB if Temple wants Mongo-backed page content immediately | TT | 🟡 MED | `python3 backend/scripts/seed_lo_shu.py --mongo-url "$MONGO_URL" --db-name horoscope_db` |
| LSG-OP-3 | Browser smoke test public routes after Render/Vercel deploy | TT | 🟠 HIGH | Verify hub, calculator, one missing-number page, one arrow page, and `/api/seo/sitemap/lo-shu-grid`. |

---

## Verification

- Backend verification: `python3 -m py_compile` passed for `backend/lo_shu_router.py`, `backend/seo_router.py`, `backend/server.py`, and `backend/scripts/seed_lo_shu.py`
- Frontend verification: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` passed in `frontend/`
- Runtime note: page endpoints fall back to in-code content if Mongo seed data has not been inserted yet

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-05-23 | LSG-1 delivered locally. Added dedicated Lo Shu backend router, SEO sitemap endpoint, Mongo seed script, four public frontend pages, shared grid component, App routes, sitemap index entry, and Vercel cache headers. Backend compile and frontend production build passed. | Codex | `CODEX_COMMISSION_LO_SHU_GRID.md` |
