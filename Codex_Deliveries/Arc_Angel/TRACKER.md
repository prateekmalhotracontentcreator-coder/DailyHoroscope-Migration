# Arc Angel -- Module Tracker
> Path: `Codex_Deliveries/Arc_Angel/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-17 · v1.3

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- KE-Sprint3 live ✅ · ARC-2 ready to issue (after KE-OP-14 fix) |
| **Frontend** | `frontend/src/components/ArcAngelPanel.jsx` (NavBar drawer) · `frontend/src/pages/ArcAngelPage.jsx` (full view) |
| **Backend** | `GET /api/knowledge-engine/arc-angel-windows` · `GET /api/knowledge-engine/arc-angel-profile/{user_id}` |
| **Live URL** | `/arc-angel` + NavBar mobile drawer |
| **Confidence %** | Base 40% live (3-pillar formula built, dynamic wiring in ARC-2) |
| **Premium gate** | None yet -- ⏸ HOLD pending TT design approval |
| **Persistence** | `user_arc_angel_profiles` MongoDB collection live. 6h cache. Profile upserted on every arc-angel-windows call. KE-Sprint3 2026-05-17. |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| ARC-UI | Arc Angel UI Panel (ArcAngelPanel.jsx) | ✅ INTEGRATED | `CODEX_COMMISSION_ARC_ANGEL_UI_PANEL.md` · Commit `c01ec8d` |
| **ARC-2** | Dynamic Confidence Engine (3-pillar wiring + decay + notifications) | 🟣 READY TO ISSUE | `CODEX_COMMISSION_ARC_2_CONFIDENCE_QUESTIONNAIRE.md` -- brief rewritten 2026-05-17. KE-Sprint3 live ✅ (KE-OP-13 cleared). **Issue after KE-OP-14 (window granularity fix) is confirmed in KE thread.** |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| ARC-OP-1 | **Issue ARC-2 to Codex** -- after KE-OP-14 (window granularity) is fixed in KE thread | TT | 🟠 HIGH | Brief at `CODEX_COMMISSION_ARC_2_CONFIDENCE_QUESTIONNAIRE.md`. KE-Sprint3 live ✅. One pre-condition remaining: KE-OP-14 fix so ARC-2 UI gets 3 AD-level windows/domain. |
| ARC-OP-2 | **3-Pillar confidence formula** (locked 2026-05-17): Base 40% + Pillar 1 +24% (questionnaire, 2%/area) + Pillar 2 +12% (IRs, 1%/report) + Pillar 3 +10% (daily rituals, decay) = cap 86%. Schema + `_compute_confidence()` skeleton owned by KE-Sprint3. ARC-2 wires dynamic data. | CX | 🟠 HIGH | Formula locked. Case studies = internal KE benchmark only, not formula. |
| ARC-OP-3 | Pillar 3 decay engine: APScheduler job at 02:00 IST. 2-day grace → decay day 3+ → −1/day → tiered recovery on resume. Sub-pillars (tarot_love, strategist) decay independently. | CX | 🟠 HIGH | Part of ARC-2. Requires KE-Sprint3 schema. |
| ARC-OP-4 | Notification hooks: day-2 miss = motivational alert · day-3+ miss = score-dip-risk alert · re-fire every 2 days during decay. | CX | 🟠 HIGH | Part of ARC-2. Hooks into existing Notifications module. |
| ARC-OP-5 | MongoDB persistence: `user_arc_angel_profile` schema + 6h cache owned by KE-Sprint3. ARC-2 extends with dynamic pillar data via hooks on questionnaire answers + IR generation + ritual events. | CX | 🟠 HIGH | Do NOT rebuild schema -- extend Sprint 3's work. |
| ARC-OP-6 | Premium gate (period columns blurred for free users) + Desktop sidebar (`w-80`, sticky, collapsible) | CX | ⏸ HOLD | UI locked. TT to explicitly approve design before issuing to Codex. |
| ARC-OP-7 | "Upgrade Confidence" dashboard prompt (+10% via Tarot + Strategist) | CX | ⏸ HOLD | UI locked. TT to confirm design/mockup before building. |

---

## Architecture Notes

- **Confidence formula (locked 2026-05-17):** Base 40% (Vedic Engine) + Pillar 1 +24% (questionnaire, 2%/area, 12 areas) + Pillar 2 +12% (IRs, 1% each, 12 max) + Pillar 3 +10% (daily rituals, decays) = cap 86%. Case studies = internal benchmark only.
- **Commission split:** KE-Sprint3 owns schema + `_compute_confidence()` skeleton. ARC-2 owns dynamic wiring (questionnaire hooks, IR hooks, decay job, notification triggers).
- **UI lock (2026-05-17):** Existing 3-column LeftNav panel with confidence donut is frozen. No UI changes without explicit TT approval. Premium gate + sidebar + upgrade prompt are all ⏸ HOLD.
- Natural benefic/malefic baseline: Jupiter/Venus/Mercury(waxing)/Moon(waxing) = Auspicious · Saturn/Mars/Rahu/Ketu/Sun = Inauspicious
- Period quality defaults to Legacy Model when zero `approved` KE rules exist

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-04-19 | ARC-UI (ArcAngelPanel.jsx) delivered and integrated. Panel live in NavBar. | Codex + CC | Commit `c01ec8d` |
| v1.1 | 2026-05-15 | ARC-2 brief written. Tracker created. | CC | `CODEX_COMMISSION_ARC_2_CONFIDENCE_QUESTIONNAIRE.md` |
| v1.2 | 2026-05-17 | **ARC-2 brief fully rewritten.** Formula locked: 3-pillar model (Base 40% + Pillar 1 24% + Pillar 2 12% + Pillar 3 10%, cap 86%). Old formula (42 base, +18 questionnaire, +4/module, 72 max) retired. Decay engine specified (2-day grace, −1/day, tiered recovery). Notification hooks added. Deliverables 6+7 (premium gate + sidebar) moved to ⏸ HOLD pending TT UI approval. Schema/persistence split: KE-Sprint3 owns skeleton, ARC-2 owns dynamic wiring. Case studies confirmed as internal KE benchmark only. Pre-condition updated: ARC-2 must wait for KE-Sprint3. | TT + CC | `CODEX_COMMISSION_ARC_2_CONFIDENCE_QUESTIONNAIRE.md` |
| v1.3 | 2026-05-17 | **KE-Sprint3 live verified (KE-OP-13 cleared).** Tracker updated to reflect live state: `confidence_pct: 40` live, `engine_label` live, `arc-angel-profile/{user_id}` route live, MongoDB persistence live, 6h cache live. Status field updated from "hardcoded 42 / stateless" to live values. ARC-2 pre-condition updated: issue after KE-OP-14 (window granularity fix in KE thread) -- returns 1 period/domain instead of expected 3 AD-level windows. | CC | KE-OP-13 cleared 2026-05-17 |
