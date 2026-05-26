# Codex Commission -- STR-R01: War Room Engine Selector
> Module: The Strategist
> Closes: R-01 (live-integration parity gap)
> Depends on: STR-1 ✅ (War Room shell live), STR-2J ✅ (MissionCard live)
> Last updated: 2026-05-26

---

## The Gap Being Closed

`/strategist/war-room` currently renders `<StrategistWarRoom />` with **zero props** -- all component defaults (`score: 0`, `missions: []`, etc.). The backend engine (`GET /api/strategist/dashboard`) is fully built and returns real data. The missing piece is the **selector**: a hook + page wrapper that fetches the engine output and maps it to the component prop-bag.

This commission delivers that selector. No backend changes required.

---

## What You Must NOT Touch

| File | Rule |
|---|---|
| `frontend/src/components/strategist/war-room/StrategistWarRoom.jsx` | Do NOT modify. Prop-bag signature is locked. |
| `frontend/src/components/strategist/war-room/*.jsx` (all sub-components) | Do NOT modify any war-room component. |
| `frontend/src/pages/strategist/StrategistMissionsPage.jsx` | Do NOT touch. |
| `backend/strategist_router.py` | Do NOT modify. |
| `backend/strategist_engine.py` | Do NOT modify. |
| `backend/vedic_calculator.py` | Do NOT touch. |

---

## Deliverables (2 files only)

### File 1 -- `frontend/src/pages/strategist/StrategistWarRoomPage.jsx`

A new page component that:
1. Calls `GET /api/strategist/dashboard` on mount (auth token from localStorage key `token`)
2. Calls `POST /api/strategist/missions` on mount (parallel to dashboard fetch)
3. Maps the response to the `<StrategistWarRoom />` prop-bag (full mapping spec below)
4. Renders a loading state while fetches are in flight
5. Renders a gated error state if profile is missing (backend returns `{ error: "LK profile missing..." }`)
6. Passes the mapped props to `<StrategistWarRoom />`

### File 2 -- `frontend/src/App.js` (route update only)

Change the war-room route from:
```jsx
<Route path="/strategist/war-room" element={<ProtectedRoute><StrategistWarRoom /></ProtectedRoute>} />
```
to:
```jsx
<Route path="/strategist/war-room" element={<ProtectedRoute><StrategistWarRoomPage /></ProtectedRoute>} />
```

Add the lazy import at the top of App.js alongside the other Strategist imports:
```jsx
const StrategistWarRoomPage = lazy(() => import('./pages/strategist/StrategistWarRoomPage'));
```

---

## Prop Mapping Specification

### Backend response shape (`GET /api/strategist/dashboard`)

```js
{
  // identity
  user_id, generated_at, command_planet, success_direction,

  // dasha (flat fields)
  current_mahadasha, current_mahadasha_start, current_mahadasha_end,
  current_antardasha, current_antardasha_start, current_antardasha_end,

  // engine output
  conquest_probability: {
    score,          // number 0-100
    tier,           // string
    directive,      // string
    narrative,      // string
    factors: [      // array -- maps directly to <FactorTable>
      { factor, delta, detail }
    ]
  },

  // counts (not used directly -- missions fetched separately)
  active_missions_count, active_hurdles_count,
  ritual_streak,

  // diagnosis
  diagnosis_summary: { pitru_rin_active, year_lord },

  // scoreboard
  scoreboard: {
    conquest_score, score_tier, score_directive,
    streak_days, streak_tier, karmic_debt_cleared,
    gate0_last_verdict, gate0_days_since,
    next_threshold, next_threshold_label, points_to_next
  },

  // gate narratives
  gate_summaries: [ { gate, name, status, narrative, ... } ]
}
```

### Backend response shape (`POST /api/strategist/missions`)

Request body: `{ "user_id": null, "date": "<today ISO string>" }`

```js
{
  missions: [
    { id, title, code, module, trigger, priority, status, ... }
  ],
  count
}
```

---

### Mapping Table

| `<StrategistWarRoom />` prop | Source | Derivation |
|---|---|---|
| `conquestScore` | `dashboard` | `{ score: conquest_probability.score, stampLabel: scoreboard.score_tier }` |
| `factors` | `dashboard` | `conquest_probability.factors` (pass through directly) |
| `missions` | `missions POST` | `missions_response.missions` |
| `dasha` | `dashboard` | Shape from flat dasha fields (see §Dasha shaping below) |
| `transition` | `dashboard` | `null` -- not yet returned by engine. Pass `undefined`. |
| `pitruRin` | `dashboard` | `[]` -- detailed debt array not yet in engine. Pass `[]`. |
| `pitruDelta` | `dashboard` | `diagnosis_summary.pitru_rin_active ? -20 : 0` |
| `pitruEmptyMeta` | `dashboard` | `diagnosis_summary.pitru_rin_active ? undefined : { message: "No active ancestral debt detected." }` |
| `goldenHour` | `dashboard` | `[]` -- not yet in engine. Pass `[]`. |
| `kpVerdict` | `dashboard` | `scoreboard.gate0_last_verdict ?? ''` |
| `locationLabel` | `dashboard` | `success_direction ? \`Power direction: \${success_direction}\` : undefined` |
| `dateLabel` | local | `new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' })` |
| `layout` | local | `window.innerWidth < 768 ? 'snap' : 'grid'` |
| `onRecalibrate` | local | `() => window.location.reload()` |

---

### §Dasha Shaping

`DashaTimeline` expects:
```js
dasha: {
  mahadasha:  { planet, elapsedDays, totalDays, startedLabel, endsLabel },
  antardasha: { planet, elapsedDays, totalDays, startedLabel, endsLabel },
}
```

Derive from dashboard flat fields:
```js
function shapeDasha(data) {
  if (!data.current_mahadasha) return undefined;

  const today = new Date();

  function parseDateToElapsed(startStr) {
    if (!startStr) return 0;
    const start = new Date(startStr);
    return Math.max(0, Math.floor((today - start) / 86400000));
  }

  function parseDateToTotal(startStr, endStr) {
    if (!startStr || !endStr) return 1;
    const start = new Date(startStr);
    const end = new Date(endStr);
    return Math.max(1, Math.floor((end - start) / 86400000));
  }

  function fmtDate(str) {
    if (!str) return '';
    return new Date(str).toLocaleDateString('en-IN', { month: 'short', year: 'numeric' });
  }

  return {
    mahadasha: {
      planet:      data.current_mahadasha,
      elapsedDays: parseDateToElapsed(data.current_mahadasha_start),
      totalDays:   parseDateToTotal(data.current_mahadasha_start, data.current_mahadasha_end),
      startedLabel: fmtDate(data.current_mahadasha_start),
      endsLabel:    fmtDate(data.current_mahadasha_end),
    },
    antardasha: data.current_antardasha ? {
      planet:      data.current_antardasha,
      elapsedDays: parseDateToElapsed(data.current_antardasha_start),
      totalDays:   parseDateToTotal(data.current_antardasha_start, data.current_antardasha_end),
      startedLabel: fmtDate(data.current_antardasha_start),
      endsLabel:    fmtDate(data.current_antardasha_end),
    } : undefined,
  };
}
```

---

## Loading State

While either fetch is in flight, render a full-screen loading indicator that matches the Strategist theme. Use the existing `strategist-tokens.css` CSS variables -- do not hardcode colours. Example skeleton:

```jsx
<StrategistThemeProvider>
  <ControlRoomBackdrop>
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '60vh' }}>
      <p style={{ color: 'var(--str-gold)', fontFamily: 'var(--str-font-display)', fontSize: '1.1rem', letterSpacing: '0.08em' }}>
        Calibrating War Room...
      </p>
    </div>
  </ControlRoomBackdrop>
</StrategistThemeProvider>
```

Import `StrategistThemeProvider` and `ControlRoomBackdrop` exactly as they are imported in `StrategistWarRoom.jsx`:
```jsx
import StrategistThemeProvider from '../components/strategist/StrategistThemeProvider';
import ControlRoomBackdrop from '../components/strategist/ControlRoomBackdrop';
```

---

## Error / No-Profile State

If `dashboard` returns `{ error: "LK profile missing..." }`, render:

```jsx
<StrategistThemeProvider>
  <ControlRoomBackdrop>
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '60vh', gap: '1.5rem' }}>
      <p style={{ color: 'var(--str-gold)', fontFamily: 'var(--str-font-display)', fontSize: '1.1rem' }}>
        War Room Locked
      </p>
      <p style={{ color: 'var(--str-muted)', fontSize: '0.9rem', textAlign: 'center', maxWidth: 340 }}>
        Complete your Strategist onboarding to activate the live engine.
      </p>
      <a href="/strategist" style={{ color: 'var(--str-gold)', textDecoration: 'underline', fontSize: '0.9rem' }}>
        Return to Strategist
      </a>
    </div>
  </ControlRoomBackdrop>
</StrategistThemeProvider>
```

---

## Fetch Pattern

Use `Promise.all` so both fetches run in parallel. Auth token from `localStorage.getItem('token')`.

```js
const BACKEND = process.env.REACT_APP_BACKEND_URL || '';

const [dashRes, missRes] = await Promise.all([
  fetch(`${BACKEND}/api/strategist/dashboard`, {
    headers: { Authorization: `Bearer ${token}` }
  }),
  fetch(`${BACKEND}/api/strategist/missions`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: null, date: new Date().toISOString().split('T')[0] })
  })
]);

const dashboard = await dashRes.json();
const missionsData = await missRes.json();
```

---

## Existing Imports Available in `App.js`

These lazy imports already exist -- do not duplicate them:
```jsx
const StrategistWarRoom = lazy(() => import('./components/strategist/war-room/StrategistWarRoom'));
const StrategistThemeProvider = ...  // already used elsewhere
```

The new import to add:
```jsx
const StrategistWarRoomPage = lazy(() => import('./pages/strategist/StrategistWarRoomPage'));
```

---

## Verification Checklist (for CC integration)

After Codex delivers, confirm these before closing R-01:

- [ ] `StrategistWarRoomPage.jsx` exists in `frontend/src/pages/strategist/`
- [ ] App.js route at `/strategist/war-room` now points to `<StrategistWarRoomPage />` (not `<StrategistWarRoom />`)
- [ ] `/strategist/war-room` loads without console errors on a user who has completed LK onboarding
- [ ] Conquest Score gauge shows a non-zero value from the live engine
- [ ] Dasha bars are visible and show real planet names (not empty)
- [ ] Mission Board shows at least 1 mission card (or empty-state message)
- [ ] No-profile users see the "War Room Locked" gate, not a crash
- [ ] `py_compile` passes on all Python files (no backend changes expected -- verify nothing leaked)
- [ ] `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` passes

---

## Do Not Include

- No new backend endpoints
- No changes to any `backend/` file
- No changes to `StrategistWarRoom.jsx` or any war-room component
- No Redux, no Zustand, no context providers -- a single `useState` + `useEffect` in the page component is sufficient
- No TypeScript -- plain JSX only
