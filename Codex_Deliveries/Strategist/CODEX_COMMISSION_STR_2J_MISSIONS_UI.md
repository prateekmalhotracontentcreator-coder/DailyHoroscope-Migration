# Codex Commission Brief -- STR-2J: Strategist Missions Page UI
> Commission ID: STR-2J
> Thread: The Strategist
> Issued: 2026-05-15 | Priority: 🟡 MEDIUM
> Pre-condition: STR-1 (Landing + War Room visual rebuild) ideally delivered first -- both touch Strategist pages. Can run in parallel if Codex has capacity.

---

## Context

The Strategist module's War Room (`/strategist`) and Landing page (`/the-strategist`) are covered by **STR-1**. That commission explicitly says `"Do NOT touch: frontend/src/pages/StrategistMissionsPage.jsx"`. This commission -- **STR-2J** -- covers exactly that file plus the related mission card display improvements identified in the Session 8 review.

**Problems found in current `StrategistMissionsPage.jsx`:**
1. `MissionCard.jsx` has zero responsive breakpoints -- breaks on mobile
2. `decision_logic` and `pivot_logic` fields come from the API but are **never rendered**
3. No command planet badge/chip on mission cards
4. The missions page is locked to `max-w-2xl` -- looks cramped on desktop
5. Dasha display shows only Mahadasha label -- no Antardasha, no timing bar, no remaining period

---

## Source of Truth Files (Read These First)

```
frontend/src/pages/StrategistMissionsPage.jsx     ← primary target
frontend/src/components/MissionCard.jsx            ← mission card component (if separate file)
                                                     or inline in StrategistMissionsPage.jsx
backend/strategist_router.py                       ← mission API (read only -- do not modify)
backend/vedic_calculator.py                        ← dasha data source (read only)
```

Also study for visual reference:
```
frontend/src/pages/KrishnaOraclePage.jsx           ← premium UX bar
frontend/src/pages/LongevityReportPage.jsx         ← premium UX bar
```

---

## Architecture Rule

All dasha data comes from `vedic_calculator.py` via the existing `/api/strategist/dashboard` endpoint. Do NOT call `knowledge_engine.py` for dasha or planetary data in this commission.

---

## Deliverable 1 -- MissionCard.jsx: Full Responsive + Field Completeness

### 1.1 Responsive Breakpoints

**Current:** Card has no `sm:` or `md:` breakpoints -- all padding/grid is fixed.

**Fix:**
- Mobile (default): single column, full width, `px-4 py-4`
- `sm:` (≥640px): padding increases to `px-5 py-5`
- `md:` (≥768px): two-column card grid on missions list page
- `lg:` (≥1024px): three-column card grid on missions list page
- Max width of page container: change `max-w-2xl` → `max-w-5xl` (matches the rest of the War Room)

### 1.2 Render decision_logic and pivot_logic

These fields come from `lalkitab_strategist` MongoDB records but are never shown to the user. Add them to the card:

**Card structure (per mission):**

```
┌─────────────────────────────────────────────────────┐
│  [Layer badge]  Mission #xxx  [Command Planet chip]  │
│                                                      │
│  Strategy:                                           │
│  [strategy text]                                     │
│                                                      │
│  Decision Logic:                                     │
│  [decision_logic text] (expandable if >100 chars)   │
│                                                      │
│  Pivot Action:                                       │
│  [pivot_action text]                                 │
│                                                      │
│  Pivot Logic:    (expandable, show/hide toggle)      │
│  [pivot_logic text]                                  │
│                                                      │
│  [KPI Target chip]   [Status chip]                   │
└─────────────────────────────────────────────────────┘
```

Field mapping from API response:
- `strategy` → **Strategy** section (already rendered, keep)
- `decision_logic` → **Decision Logic** section (NEW)
- `pivot_action` → **Pivot Action** section (already rendered, keep)
- `pivot_logic` → **Pivot Logic** section (NEW, expandable)
- `kpi_target` → chip at bottom (already rendered, keep)

**Expand/collapse:**
- `decision_logic`: if text > 120 chars, show first 120 chars + "... Show more" toggle
- `pivot_logic`: collapsed by default. Toggle: "▼ Show Pivot Logic" / "▲ Hide Pivot Logic"
- Use `useState` per card for expand state

### 1.3 Command Planet Badge

The `/api/strategist/dashboard` response includes the user's command planet (from `vedic_calculator.py` via `AstrologyStrip`). Add a compact badge on each mission card:

```jsx
// If mission's planet_lord matches the user's command planet:
<span className="text-xs px-2 py-0.5 rounded-full bg-gold/10 border border-gold/40 text-gold font-medium">
  ⭐ Command Planet Active
</span>

// Standard planet badge (always shown):
<span className="text-xs px-2 py-0.5 rounded-full bg-card border border-border text-muted-foreground">
  ♄ Saturn Mission
</span>
```

Read the command planet from the parent component's state (already fetched in StrategistMissionsPage from the dashboard endpoint). Pass as a prop to each MissionCard.

---

## Deliverable 2 -- Dasha Display: Antardasha + Timing Bar

**Current state:** The War Room header or Scoreboard shows "Current Dasha: Saturn" -- plain text, no detail.

**Target:** The dasha section in `StrategistMissionsPage.jsx` (and/or the AstrologyStrip if present on this page) should show:

```
Mahadasha:    Saturn  (2019 - 2038)
Antardasha:   Mercury  (May 2026 - Oct 2027)
              ████████████░░░░░░░░  18 months remaining
```

**Implementation:**
- The backend at `/api/strategist/dashboard` already returns full dasha data including antardasha (`current_antardasha`, `antardasha_end`, `mahadasha_start`, `mahadasha_end`)
- Build a `DashaTimingBar` component (inline or separate file):
  ```jsx
  // Props: mahadasha, antardasha, mahadasha_start, mahadasha_end, antardasha_start, antardasha_end
  // Shows: name labels + date range + progress bar + "X months remaining"
  ```
- Progress bar: gold fill, percentage = elapsed / total duration
- "X months remaining" -- compute from `antardasha_end` vs today
- Colour: gold for currently active planet in natural benefic list (Jupiter, Venus, Mercury waxing, Moon waxing); amber for malefic (Saturn, Mars, Rahu, Ketu, Sun)

**Natural benefic list** (from CLAUDE.md Architecture Rule):
```
Benefic (gold): Jupiter, Venus, Mercury (waxing), Moon (waxing)
Malefic (amber/red): Saturn, Mars, Rahu, Ketu, Sun
```

---

## Deliverable 3 -- Page Layout: Desktop Expansion

**Current:** `max-w-2xl` container -- missions look cramped on desktop.

**Fix:**
- Change page container to `max-w-5xl mx-auto`
- Mission grid: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4` (from single column)
- Mission filter/sort bar (if present): full width, aligned left
- No horizontal overflow

---

## Files to Modify

```
frontend/src/pages/StrategistMissionsPage.jsx     ← primary (Deliverables 1, 2, 3)
frontend/src/components/MissionCard.jsx           ← if it exists as separate component
```

## Do NOT Touch

```
backend/strategist_router.py          ← no backend changes
backend/strategist_engine.py          ← no backend changes
backend/vedic_calculator.py           ← no changes
frontend/src/pages/StrategistPage.jsx ← covered by STR-1
frontend/src/pages/TheStrategistLandingPage.jsx  ← covered by STR-1
```

---

## Theme Tokens

```css
bg-background · bg-card · text-foreground · text-muted-foreground
text-gold / border-gold / bg-gold  (#c5a059)
font-cinzel (headings) · font-playfair (body)
```

GlassCard: `rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`

---

## Build Verification

```bash
cd frontend && CI=true DISABLE_ESLINT_PLUGIN=true npx craco build
```

Zero errors. Check at 375px, 768px, 1280px.

---

## Commit Format

```
feat(strategist): missions page responsive layout + decision_logic + dasha timing bar
```

---

## Definition of Done

- [ ] MissionCard renders at all breakpoints -- no overflow at 375px
- [ ] `decision_logic` field visible on all mission cards
- [ ] `pivot_logic` field in collapsible section, collapsed by default
- [ ] Command planet badge shows on cards where planet_lord matches user's command planet
- [ ] Page container expanded to `max-w-5xl`
- [ ] Mission grid: 1-col mobile / 2-col tablet / 3-col desktop
- [ ] Dasha section shows Mahadasha + Antardasha with date ranges
- [ ] Timing bar shows progress + months remaining
- [ ] Planet colour: gold for benefic, amber for malefic
- [ ] Build passes zero errors
