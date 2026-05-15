# Longevity Report -- Module Tracker
> Path: `Codex_Deliveries/Longevity/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-15 · v1.0

---

## Current Status

| Field | Value |
|---|---|
| **Status** | ⛔ BLOCKED -- depends on KE Sprint 2 gate |
| **Frontend** | `frontend/src/pages/LongevityReportPage.jsx` -- visual quality bar for all other modules |
| **Backend** | `backend/longevity_router.py` -- ⚠️ verify load on Render (may have startup warning) |
| **Live URL** | `/longevity-report` (may be functional but unverified) |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| LON-H | Commission H brief (older, superseded) | SUPERSEDED | `_archive/CODEX_COMMISSION_H_BRIEF_v2026-04-10.md` |
| **LON-1** | Ayur Jyotish Longevity Report (main contract) | ⛔ BLOCKED -- do not issue yet | `CODEX_COMMISSION_LONGEVITY_REPORT_CONTRACT.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| LON-OP-1 | **Verify `longevity_router.py` loads on Render** -- check for `longevity_router failed to load` in logs | TT | 🟠 HIGH | If failing: Claude Code direct fix needed. Check Render dashboard logs. |
| LON-OP-2 | **Do NOT issue LON-1** until KE Sprint 2 gate passes | TT | 🔴 GATE | Needs post-arbitration rule scoring for accurate 8th house and dasha interpretations |
| LON-OP-3 | `LongevityReportPage.jsx` is the **visual quality benchmark** -- all other modules' outputs should match or exceed it | CC | 🟢 NOTE | Reference during integration reviews for all report-type modules |

---

## Architecture Notes

- LON-1 covers: vitality score · 8th house analysis · dasha health trajectory · Ayurvedic dosha profiling · remedies · premium PDF
- Large scope (~48h Codex estimate) -- plan accordingly
- All data from `vedic_calculator.py` -- no KE dasha duplication

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-04-10 | LON-1 main contract brief written (superseding Commission H). Tracker created. | CC | `CODEX_COMMISSION_LONGEVITY_REPORT_CONTRACT.md` |
