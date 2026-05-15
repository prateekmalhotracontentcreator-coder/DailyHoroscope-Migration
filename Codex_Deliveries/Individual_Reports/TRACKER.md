# Individual Reports -- Module Tracker
> Path: `Codex_Deliveries/Individual_Reports/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-15 · v1.3

---

## Current Status

| Field | Value |
|---|---|
| **Status** | ✅ LIVE -- IR-1 integrated at commit `825a294`. 5 public landing pages + `/individual-reports` hub live. |
| **Frontend (live)** | `frontend/src/pages/BirthChartPage.jsx` · `frontend/src/pages/kundali/BrihatKundliPage.jsx` · premium report tool at `/reports` |
| **Backend** | `backend/vedic_calculator.py` + individual report endpoints |
| **Live URL** | Current production remains app-only for report generation; new public SEO pages are built locally and awaiting Temple integration |
| **Report types** | Natal · Dasha · Compatibility · Career · Remedial |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| IR-Contract-v1 | Original contract (30 Mar 2026) | SUPERSEDED | `_archive/CONTRACT_APPOINTMENT_v2026-03-30.md` |
| IR-Contract-v2 | Contract update (2 Apr 2026) | SUPERSEDED | `_archive/CONTRACT_UPDATE_v2026-04-02.md` |
| IR-Frontend-v1 | Frontend commission (2 Apr 2026) | SUPERSEDED by IR-1 | `_archive/INDIVIDUAL_REPORTS_FRONTEND_v2026-04-02.md` |
| **IR-1** | 5 Public SEO Landing Pages + `/individual-reports` hub | ✅ INTEGRATED -- commit `825a294` | `CODEX_COMMISSION_IR_1_LANDING_PAGES.md` · Delivered + integrated 2026-05-15 |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| ~~IR-OP-1~~ | ~~Temple review of IR-1 frontend slice~~ | TT | ✅ DONE | Reviewed and approved 2026-05-15. Build green. Integrated at commit `825a294`. |
| ~~IR-OP-2~~ | ~~Decide whether `/individual-reports` public hub behavior is accepted as canonical~~ | TT | ✅ DONE | Confirmed canonical 2026-05-15: `/individual-reports` = public hub (PremiumReportsLanding), `/reports` = premium tool (PremiumRoute gated IndividualReportsPage). |
| ~~IR-OP-3~~ | ~~Resolve unrelated global frontend build blocker in `StrategistPage.jsx`~~ | CC | ✅ DONE | Unescaped apostrophe in tagline string fixed by CC. Commit `667fc34` 2026-05-15. Vercel build green. |

---

## Architecture Notes

- IR-1 is purely frontend -- no backend dependency whatsoever
- Do NOT modify `vedic_calculator.py` or report generation endpoints as part of IR-1
- All five landing pages must include proper JSON-LD schema and OG tags
- Local IR-1 build also repurposes `/individual-reports` into the public hub while preserving the premium tool at `/reports`

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-05-15 | Tracker created. IR-1 brief finalised. Module state documented. | CC | This session |
| v1.1 | 2026-05-15 | IR-1 landing pages built locally, public routes added, sitemap updated, `/individual-reports` hub made public, and unrelated Strategist build blocker noted. | Codex | This session |
| v1.2 | 2026-05-15 | IR-1 issued to Codex IR thread. Status updated to IN PROGRESS. IR-OP-3 (Strategist build blocker) closed -- fixed by CC at commit `667fc34`. | TT + CC | `667fc34` |
| v1.3 | 2026-05-15 | IR-1 delivered by Codex and integrated. Build verified green. Route canonical confirmed by TT: `/individual-reports` = public hub, `/reports` = premium tool. IR-OP-1 + IR-OP-2 closed. Commission INTEGRATED at commit `825a294`. | CC + TT | `825a294` |
