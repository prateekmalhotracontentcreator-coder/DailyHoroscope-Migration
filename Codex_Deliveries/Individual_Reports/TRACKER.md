# Individual Reports -- Module Tracker
> Path: `Codex_Deliveries/Individual_Reports/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-15 · v1.0

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟣 PLANNED -- backend live, no public SEO landing pages |
| **Frontend (live)** | `frontend/src/pages/BirthChartPage.jsx` · `BrihatKundliPage.jsx` |
| **Backend** | `backend/vedic_calculator.py` + individual report endpoints |
| **Live URL** | App-only (no public pages -- zero Google discoverability) |
| **Report types** | Natal · Dasha · Compatibility · Career · Remedial |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| IR-Contract-v1 | Original contract (30 Mar 2026) | SUPERSEDED | `_archive/CONTRACT_APPOINTMENT_v2026-03-30.md` |
| IR-Contract-v2 | Contract update (2 Apr 2026) | SUPERSEDED | `_archive/CONTRACT_UPDATE_v2026-04-02.md` |
| IR-Frontend-v1 | Frontend commission (2 Apr 2026) | SUPERSEDED by IR-1 | `_archive/INDIVIDUAL_REPORTS_FRONTEND_v2026-04-02.md` |
| **IR-1** | 5 Public SEO Landing Pages + `/individual-reports` hub | 🟣 READY TO ISSUE | `CODEX_COMMISSION_IR_1_LANDING_PAGES.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| IR-OP-1 | **Issue IR-1 to Codex** -- pure frontend, no dependency, issue Week 1 | TT | 🟠 HIGH | Can run in parallel with KE-Sprint2. Zero backend changes. |
| IR-OP-2 | Confirm 5 report type landing page names before issuing (Natal, Dasha, Compatibility, Career, Remedial) | TT | 🟠 HIGH | Review `CODEX_COMMISSION_IR_1_LANDING_PAGES.md` §Deliverables before opening thread |

---

## Architecture Notes

- IR-1 is purely frontend -- no backend dependency whatsoever
- Do NOT modify `vedic_calculator.py` or report generation endpoints as part of IR-1
- All five landing pages must include proper JSON-LD schema and OG tags

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-05-15 | Tracker created. IR-1 brief finalised. Module state documented. | CC | This session |
