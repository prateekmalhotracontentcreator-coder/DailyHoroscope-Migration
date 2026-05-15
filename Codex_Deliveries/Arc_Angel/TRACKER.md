# Arc Angel -- Module Tracker
> Path: `Codex_Deliveries/Arc_Angel/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-15 · v1.1

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- panel live, confidence hardcoded, no premium gate yet |
| **Frontend** | `frontend/src/components/ArcAngelPanel.jsx` (NavBar drawer) · `frontend/src/pages/ArcAngelPage.jsx` (full view) |
| **Backend** | `GET /api/knowledge-engine/arc-angel-windows` |
| **Live URL** | `/arc-angel` + NavBar mobile drawer |
| **Confidence %** | Hardcoded at 42 -- NOT dynamic yet |
| **Premium gate** | None -- all 12 domains visible to all logged-in users |
| **Persistence** | Stateless -- no MongoDB profile storage |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| ARC-UI | Arc Angel UI Panel (ArcAngelPanel.jsx) | ✅ INTEGRATED | `CODEX_COMMISSION_ARC_ANGEL_UI_PANEL.md` · Commit `c01ec8d` |
| **ARC-2** | Confidence % lift + Questionnaire gating + Desktop sidebar | 🟣 READY TO ISSUE | `CODEX_COMMISSION_ARC_2_CONFIDENCE_QUESTIONNAIRE.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| ARC-OP-1 | **Issue ARC-2 to Codex** (Week 2 -- after KE-Sprint2 ideally, can run parallel) | TT | 🟠 HIGH | Brief at `CODEX_COMMISSION_ARC_2_CONFIDENCE_QUESTIONNAIRE.md` |
| ARC-OP-2 | Confidence % growth: 42 (birth data only) → 60 (questionnaire done) → 72 (3 modules used, +4% each) | CX | 🟠 HIGH | Part of ARC-2. Backend compute owned by KE-IQ -- ARC-2 consumes the endpoint only |
| ARC-OP-3 | Premium gate: period columns blurred for free users; upgrade CTA overlay | CX | 🟠 HIGH | Part of ARC-2 |
| ARC-OP-4 | Desktop sticky sidebar (`w-80`, collapsible, `lg+`) in `ArcAngelPage.jsx` · preference stored in `localStorage.arcAngelSidebarOpen` | CX | 🟠 HIGH | Part of ARC-2 |
| ARC-OP-5 | `user_arc_angel_profiles` MongoDB persistence + 24h cache + `?refresh=true` force recompute | CX | 🟠 HIGH | Part of ARC-2 |
| ARC-OP-6 | **Do NOT duplicate confidence scoring logic** -- KE-IQ owns the backend compute; ARC-2 only consumes `confidence_pct` from the endpoint response | BOTH | 🔴 ENFORCE | Co-owned with KE-IQ commission |

---

## Architecture Notes

- ARC-2 confidence % is co-owned between two commissions: **KE-IQ** owns the backend compute (`user_questionnaire_profiles`, confidence formula), **ARC-2** owns the frontend display and `user_arc_angel_profiles` persistence
- Natural benefic/malefic baseline: Jupiter/Venus/Mercury(waxing)/Moon(waxing) = Auspicious · Saturn/Mars/Rahu/Ketu/Sun = Inauspicious
- Period quality defaults to Legacy Model classification when zero `approved` KE rules exist

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-04-19 | ARC-UI (ArcAngelPanel.jsx) delivered and integrated. Panel live in NavBar. | Codex + CC | Commit `c01ec8d` |
| v1.1 | 2026-05-15 | ARC-2 brief written. Tracker created. | CC | `CODEX_COMMISSION_ARC_2_CONFIDENCE_QUESTIONNAIRE.md` |
