# Codex Commission Brief -- ARC-2: Arc Angel Phase 2
> Commission ID: ARC-2
> Thread: Arc Angel
> Issued: 2026-05-15 | Priority: 🔴 HIGH
> Pre-condition: ARC-UI ✅ INTEGRATED (commit `c01ec8d`). KE Sprint 2 ideally passed (for post-arbitration confidence scoring).

---

## Context

`ArcAngelPanel.jsx` is live and baseline. The Phase 1 panel delivers:
- 4-column domain table (Domain | Auspicious Periods | Inauspicious Periods | Confidence %)
- Mobile drawer in NavBar (logged-in users only)
- Hardcoded `overall_confidence_pct: 42` (birth data baseline)
- No premium gate on period columns
- No desktop sidebar
- Stateless -- computed on demand, no MongoDB persistence

**Phase 2 builds on this baseline.** Do NOT rebuild -- extend.

---

## Source of Truth Files (Read These First)

```
Codex_Deliveries/Arc_Angel/CODEX_COMMISSION_ARC_ANGEL_UI_PANEL.md   ← Phase 1 handoff
backend/knowledge_engine.py                                          ← Arc Angel computation
backend/knowledge_schema.py                                          ← ArcAngelDomainSnapshot, UserArcAngelProfileDocument
backend/server.py                                                    ← GET /api/knowledge-engine/arc-angel-windows
frontend/src/components/ArcAngelPanel.jsx                           ← baseline panel (live)
frontend/src/pages/ArcAngelPage.jsx                                 ← full detail view (live)
```

---

## Architecture Rule

All dasha/astronomical computations come from `vedic_calculator.py`. Do NOT add dasha calculation to `knowledge_engine.py`. `compute_dasha_timeline()` in KE delegates -- keep that pattern.

---

## 12 Domain Contract (Locked -- Do Not Change Slugs)

```
health · career · finances · learning · emotional · spirituality
relationships · family · social · adventure · environment · creativity
```

---

## Deliverables

### Deliverable 1 -- Confidence % Growth (Session 8, S8-A requirement)

> *"Arc Angel panel: Confidence % increase with User's use of other modules and more importantly answers our Questionnaire which leads to more informed decision making."* -- Session 8

**Current state:** `confidence_pct: 42` hardcoded per domain and at `overall_confidence_pct`.

**Target computation** (coordinate with KE-IQ commission which owns the backend logic):

```
Base (birth data):          42%
Questionnaire completed:   +18%  → 60%
Module usage (per module):  +4%  (capped at 3 modules = +12%)
Maximum:                    72%
```

Module usage signals to count (check `punya_rewards_log` or `user_action_logs` for these action codes):
- `birth_chart_generate`
- `numerology_report_generate`
- `tarot_daily_draw`
- `panchang_daily_view`

**Frontend changes in `ArcAngelPanel.jsx`:**
- Replace the static `42` display with the live `overall_confidence_pct` returned from the endpoint
- Add a visual confidence meter bar below the panel header:
  ```
  Accuracy: ████████░░░░  60%
  ✦ Complete your Cosmic Profile to reach 72%  [Complete →]
  ```
- If questionnaire completed: show "Accuracy: 60% ✦ Profile calibrated"
- If not completed: show CTA linking to `/questionnaire`
- Animate the progress bar on first load (CSS transition, 0.8s ease)

**Backend:** The confidence computation logic belongs in KE-IQ commission (same `GET /api/knowledge-engine/arc-angel-windows` endpoint). ARC-2 only consumes the response -- do not duplicate logic.

---

### Deliverable 2 -- Premium Gate on Period Columns

**Current state:** All logged-in users see auspicious/inauspicious periods regardless of subscription tier.

**Phase 2 gate:**
- `is_premium = user?.is_premium ?? false` (already in panel -- confirmed)
- **Free users**: Period columns show blurred/locked state with upgrade CTA
  ```
  [Auspicious Periods column]  [Inauspicious Periods column]
        🔒 Premium               🔒 Premium
   "Unlock 10-year windows"  "See inauspicious periods"
   [Upgrade to Premium →]
  ```
- **Premium users**: Full period data shown as now
- `Confidence %` column and `Domain` column always visible (free + premium)
- Gate text: *"Upgrade to Premium to unlock your 10-year Auspicious and Inauspicious windows"*
- CTA: Navigate to `/pricing` or open Razorpay upgrade flow (use existing upgrade pattern from codebase)

---

### Deliverable 3 -- Desktop Sidebar Integration

**Current state:** `ArcAngelPanel` lives inside the NavBar mobile drawer only. On desktop (lg+), it is not visible -- users must navigate to `/arc-angel` for the full page.

**Phase 2 requirement:** Add a persistent desktop right sidebar to `ArcAngelPage.jsx` at `/arc-angel`.

**Layout:** On `lg+` screens, `ArcAngelPage.jsx` should render a two-column layout:
```
┌─────────────────────────────┬──────────────────────┐
│                             │  Arc Angel Panel      │
│   Main content area         │  (collapsible)        │
│   (12-domain detail view)   │                       │
│                             │  Confidence meter     │
│                             │  Domain quality now   │
│                             │  Questionnaire CTA    │
└─────────────────────────────┴──────────────────────┘
```

Implementation:
- On `lg+`: sidebar is sticky, `w-80`, positioned to the right of the main content area
- On mobile: sidebar collapses into the existing NavBar drawer (existing behaviour unchanged)
- Sidebar renders `<ArcAngelPanel />` component directly (reuse -- do not duplicate)
- Sidebar is always open on desktop (no toggle needed on initial load)
- Add a collapse toggle `[‹ Hide]` / `[› Show Panel]` button at the top of the sidebar for user preference -- save preference in `localStorage.arcAngelSidebarOpen`

---

### Deliverable 4 -- MongoDB Profile Persistence

**Current state:** Arc Angel is stateless -- endpoint computes fresh on every call.

**Phase 2:** Persist `UserArcAngelProfileDocument` in MongoDB after each successful computation.

Collection: `user_arc_angel_profiles`

Document shape (already in `knowledge_schema.py`):
```python
{
    "user_id": str,
    "birth_date": str,
    "birth_time": str,
    "birth_place": str,
    "overall_confidence_pct": int,
    "domain_quality_now": dict,        # { "health": "auspicious", ... }
    "arc_angel_windows": list,         # full 12-domain window list
    "questionnaire_completed": bool,
    "modules_used": int,
    "computed_at": datetime,
    "horizon_years": int               # default 10
}
```

**Endpoint behaviour change for `GET /api/knowledge-engine/arc-angel-windows`:**
1. Check if `user_arc_angel_profiles` has a document for this user computed within the last 24 hours
2. If yes: return the cached document (fast path -- no re-computation)
3. If no: compute fresh, persist, return
4. Add query param: `?refresh=true` forces recomputation regardless of cache age

**Why 24-hour cache:** Dasha periods change on a multi-month scale. Daily refresh is more than sufficient and avoids heavy computation on every page load.

---

## Files to Modify

```
frontend/src/components/ArcAngelPanel.jsx     ← confidence meter + premium gate + questionnaire CTA
frontend/src/pages/ArcAngelPage.jsx           ← desktop sidebar layout
backend/server.py                             ← profile persistence + cache logic in arc-angel-windows
```

## Do NOT Touch

```
backend/vedic_calculator.py
backend/knowledge_engine.py                  (confidence computation owned by KE-IQ)
backend/knowledge_schema.py                  (schema already has UserArcAngelProfileDocument)
frontend/src/components/NavBar.jsx           (existing mobile drawer behaviour unchanged)
```

---

## Theme Tokens

```css
bg-background · bg-card · text-foreground · text-muted-foreground
text-gold / border-gold / bg-gold  (#c5a059)
```

GlassCard: `rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`

---

## Build Verification

```bash
cd frontend && CI=true DISABLE_ESLINT_PLUGIN=true npx craco build
```

Zero errors. Check: desktop sidebar visible at lg+ breakpoint. Mobile drawer unchanged.

---

## Commit Format

```
feat(arc-angel): phase 2 confidence growth + premium gate + desktop sidebar + profile persistence
```

---

## Definition of Done

- [ ] Confidence % meter visible in panel header -- animates on load, shows live value
- [ ] Questionnaire CTA shown when `completed: false`, hidden when completed
- [ ] Free users see blurred/locked period columns with upgrade CTA
- [ ] Premium users see full period data (unchanged from Phase 1)
- [ ] Desktop sidebar renders in `ArcAngelPage.jsx` on `lg+` -- sticky, collapsible, preference saved in localStorage
- [ ] Mobile NavBar drawer behaviour unchanged
- [ ] `user_arc_angel_profiles` collection saves on each fresh computation
- [ ] 24-hour cache returns stored profile; `?refresh=true` forces recompute
- [ ] Build passes zero errors
