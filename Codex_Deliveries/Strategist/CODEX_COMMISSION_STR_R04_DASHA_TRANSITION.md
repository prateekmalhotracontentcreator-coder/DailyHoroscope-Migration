# Codex Commission -- STR-R04: Dasha Transition Date

> Module: The Strategist
> Closes: War Room `transition: undefined` hardcoded placeholder
> Depends on: STR-R01 ✅
> Stack: FastAPI + React 18
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Issued: 2026-05-26
> Scope: FRONTEND ONLY -- backend already returns the data

---

## The Gap Being Closed

`StrategistWarRoomPage.jsx` → `mapWarRoomProps()` returns `transition: undefined` -- hardcoded.

The backend (`GET /api/strategist/dashboard`) already returns `current_mahadasha_end` in the response (set inside `_build_war_room_state` via `_dasha_context`). The data exists -- it is simply not being mapped.

This commission is a **1-line frontend fix + 1 new helper** only. No backend changes.

---

## What You Must NOT Touch

| File | Rule |
|---|---|
| `frontend/src/components/strategist/war-room/StrategistWarRoom.jsx` | DO NOT modify |
| `frontend/src/components/strategist/war-room/*.jsx` | DO NOT modify |
| `backend/strategist_router.py` | DO NOT modify |
| `backend/vedic_calculator.py` | DO NOT touch |

---

## Deliverable (1 file)

### File 1 -- `frontend/src/pages/strategist/StrategistWarRoomPage.jsx`

**Add transition formatter helper** (add near `formatDisplayDate`):
```javascript
function formatTransitionDate(isoString) {
  if (!isoString) return undefined;
  const d = new Date(isoString);
  if (Number.isNaN(d.getTime())) return undefined;
  return d.toLocaleDateString('en-IN', { month: 'long', year: 'numeric' });
}
```

**Update `mapWarRoomProps`** -- replace the hardcoded line:
```javascript
// BEFORE:
transition: undefined,

// AFTER:
transition: formatTransitionDate(dashboard?.current_mahadasha_end),
```

That is the entire change required. The `DashaTimeline` component inside `StrategistWarRoom` already handles the `transition` prop -- it will render the next Mahadasha transition date once this is populated.

---

## Acceptance Checklist

- [ ] `formatTransitionDate` returns a human-readable string (e.g. `"December 2031"`) for valid ISO input
- [ ] `formatTransitionDate` returns `undefined` for `null`, `undefined`, or invalid input -- no crash
- [ ] `transition` prop in `mapWarRoomProps` is no longer hardcoded `undefined`
- [ ] `DashaTimeline` renders the transition date when data is present
- [ ] Build: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` → 0 errors
