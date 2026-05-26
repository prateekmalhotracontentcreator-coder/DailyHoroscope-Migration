# Codex Commission -- STR-2E + STR-2F: Scoreboard & LK Gate Summaries

> Module: The Strategist -- War Room
> Spec refs: §P2.6 2E (Gate summaries) + §P2.6 2F (Scoreboard)
> Depends on: STR-R01 ✅
> Stack: React 18 + Tailwind + CSS tokens from `strategist-tokens.css`
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Issued: 2026-05-26

---

## Context -- Established Style Reference

All components in this commission must follow the Strategist aesthetic established in:
- `frontend/src/styles/strategist-tokens.css` -- CSS token registry (gold, dark navy, card surfaces)
- `frontend/src/components/strategist/war-room/StrategistWarRoom.jsx` -- existing War Room layout and card patterns
- `frontend/src/components/strategist/ControlRoomBackdrop.jsx` -- dark navy + green grid backdrop pattern

**Key tokens to use:**
```css
--strategist-gold          /* #C5A059 -- primary accent */
--strategist-bg            /* page/section background */
--strategist-card-bg       /* card surface */
--strategist-card-border   /* card border */
--strategist-text-primary  /* heading text */
--strategist-text-muted    /* secondary/label text */
--strategist-emerald       /* #3FAA7A -- success/clear */
--strategist-red           /* #E25C4B -- warning/active debt */
```

**Card pattern** (use for all new cards):
```jsx
<div className="rounded-xl border p-5"
  style={{
    background: 'var(--strategist-card-bg)',
    borderColor: 'var(--strategist-card-border)',
    color: 'var(--strategist-text-primary)',
  }}>
```

---

## What You Must NOT Touch

| File | Rule |
|---|---|
| `frontend/src/components/strategist/war-room/StrategistWarRoom.jsx` | DO NOT modify prop signature or existing layout |
| `frontend/src/components/strategist/war-room/*.jsx` (existing sub-components) | DO NOT modify |
| `backend/strategist_router.py` | DO NOT modify -- backend already returns all data needed |
| `backend/vedic_calculator.py` | DO NOT touch |

---

## Backend Data Already Available

`GET /api/strategist/dashboard` already returns these fields -- no new backend routes needed:

```json
{
  "scoreboard": {
    "conquest_score": 72,
    "score_tier": "Aggressive",
    "score_directive": "Push hard -- window is open",
    "streak_days": 14,
    "streak_tier": "Momentum",
    "karmic_debt_cleared": false,
    "gate0_last_verdict": "YES",
    "gate0_days_since": 3,
    "next_threshold": 75,
    "next_threshold_label": "75% -- PRAY gate clears",
    "points_to_next": 3
  },
  "gate_summaries": [
    { "gate": 1, "name": "Karmic Debt", "status": "WARNING", "narrative": "Ancestral Debt active..." },
    { "gate": 2, "name": "House Awakening", "status": "DORMANT", "narrative": "...", "dormant_count": 3 },
    { "gate": 3, "name": "Year Cycle", "status": "ACTIVE", "narrative": "...", "planet": "Jupiter", "age_range": "40-48" },
    { "gate": 4, "name": "Mercury Scan", "status": "CLEAR", "narrative": "..." },
    { "gate": 5, "name": "Geographical", "status": "ACTIVE", "narrative": "..." }
  ]
}
```

---

## Deliverables (3 files)

### File 1 -- `frontend/src/components/strategist/war-room/ConquestScoreboard.jsx`

New component. Displays the `scoreboard` data as a card panel.

**Layout:**
- Header: "◆ Conquest Scoreboard" (Cinzel font, gold, small caps)
- Score row: Large score number (`conquest_score`) + tier badge (`score_tier`)
- Directive line: `score_directive` in muted text
- Progress bar: shows progress from current score to `next_threshold` (if not null). Label: `next_threshold_label`
- Streak row: `streak_days` days + `streak_tier` label
- Gate 0 row: last verdict chip (YES=emerald, WAIT=amber, NO=red, PRAY=gold/purple) + days since label
- Karmic Debt row: green "Cleared" badge if `karmic_debt_cleared: true`; red "Active" badge if false

**Style:** Use the card pattern above. Score number: `font-cinzel text-4xl` in gold. Tier badge: small rounded pill in appropriate semantic colour.

**Props:**
```javascript
ConquestScoreboard.propTypes = {
  scoreboard: PropTypes.object,  // the scoreboard object from dashboard
};
```

---

### File 2 -- `frontend/src/components/strategist/war-room/LKGateSummaries.jsx`

New component. Displays the 5 LK Gate summaries as a compact card list.

**Layout:**
- Header: "◆ Lal Kitab Diagnostics" (Cinzel font, gold, small caps)
- 5 gate rows, each showing:
  - Gate number (small muted label)
  - Gate name (primary text)
  - Status chip: CLEAR=emerald, WARNING/DORMANT=red, ACTIVE=gold
  - Narrative (muted text, truncated to 2 lines)
  - For Gate 2: append `dormant_count` dormant houses if > 0
  - For Gate 3: append planet + age range

**Style:** Use the card pattern above. Gate rows separated by a 1px border in `var(--strategist-card-border)`.

**Props:**
```javascript
LKGateSummaries.propTypes = {
  gateSummaries: PropTypes.array,  // gate_summaries array from dashboard
};
```

---

### File 3 -- `frontend/src/pages/strategist/StrategistWarRoomPage.jsx`

**Add imports** at top of file:
```javascript
import ConquestScoreboard from '../../components/strategist/war-room/ConquestScoreboard';
import LKGateSummaries from '../../components/strategist/war-room/LKGateSummaries';
```

**Pass new props through `mapWarRoomProps`:**
```javascript
// ADD these two fields inside mapWarRoomProps return object:
scoreboard: dashboard?.scoreboard || null,
gateSummaries: Array.isArray(dashboard?.gate_summaries) ? dashboard.gate_summaries : [],
```

**Render the components** inside the existing `StrategistThemeProvider` wrapper (added by STR-R01), below `<StrategistWarRoom {...warRoomProps} />`:
```jsx
{warRoomProps.scoreboard && (
  <div style={{ padding: '0 20px 40px' }}>
    <ConquestScoreboard scoreboard={warRoomProps.scoreboard} />
    <div style={{ marginTop: 16 }}>
      <LKGateSummaries gateSummaries={warRoomProps.gateSummaries} />
    </div>
  </div>
)}
```

---

## Acceptance Checklist

- [ ] `ConquestScoreboard.jsx` renders with score, tier, directive, progress bar, streak, Gate 0 verdict, debt status
- [ ] `LKGateSummaries.jsx` renders all 5 gate rows with correct status chips
- [ ] Status chips use correct semantic colours (emerald/red/gold) matching `strategist-tokens.css`
- [ ] Both components use Strategist token CSS vars -- no hardcoded colour hex values
- [ ] Both components render gracefully with `null` / empty props -- no crash
- [ ] Components appear below the War Room on `/strategist/war-room`
- [ ] Existing War Room render and props are unaffected
- [ ] Build: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` → 0 errors
