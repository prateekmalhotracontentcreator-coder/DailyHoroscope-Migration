# Codex Commission -- STR-R02: Golden Hour Strip

> Module: The Strategist
> Closes: War Room `goldenHour: []` hardcoded placeholder
> Depends on: STR-R01 ✅
> Stack: FastAPI + React 18 + Tailwind + pyswisseph
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Issued: 2026-05-26

---

## The Gap Being Closed

`StrategistWarRoomPage.jsx` → `mapWarRoomProps()` currently returns `goldenHour: []` -- hardcoded.
The `GoldenHourStrip` component inside `StrategistWarRoom.jsx` receives this empty array and renders a blank/placeholder state.

This commission:
1. Adds `sunset_iso` to the `/api/strategist/dashboard` response (backend)
2. Computes the 3-state Golden Hour windows from that timestamp (frontend)
3. Maps the result to the `goldenHour[]` prop (frontend)

---

## What You Must NOT Touch

| File | Rule |
|---|---|
| `frontend/src/components/strategist/war-room/StrategistWarRoom.jsx` | DO NOT modify |
| `frontend/src/components/strategist/war-room/*.jsx` (all sub-components) | DO NOT modify |
| `backend/vedic_calculator.py` | DO NOT touch |
| `backend/strategist_engine.py` | DO NOT touch |
| Any existing panchang route handlers | DO NOT modify |

---

## Deliverables (2 files)

### File 1 -- `backend/strategist_router.py`

**Add sunset lookup to `_build_war_room_state()`:**

Import at top of file (add to existing imports):
```python
from panchang_router import (
    _resolve_location,
    _sunrise_sunset_moonrise_moonset,
    DEFAULT_LOCATIONS,
)
from datetime import date as _date
```

Inside `_build_war_room_state()`, after the existing `location_slug` line, add:
```python
# Fetch today's sunset for the user's location (used by Golden Hour state machine on frontend)
_sunset_iso = None
try:
    _loc_slug = location_slug or "new-delhi"
    _loc = DEFAULT_LOCATIONS.get(_loc_slug)
    if _loc:
        from zoneinfo import ZoneInfo
        _tz = ZoneInfo(_loc.timezone)
        _today = _date.today()
        _ss = _sunrise_sunset_moonrise_moonset(_today, _loc, _tz)
        _sunset_iso = _ss.sunset.isoformat()
except Exception:
    pass
```

Add `"sunset_iso": _sunset_iso` to the return dict (alongside existing fields like `"command_planet"`, `"success_direction"` etc.).

---

### File 2 -- `frontend/src/pages/strategist/StrategistWarRoomPage.jsx`

**Add Golden Hour window computation helper** (add before `mapWarRoomProps`):
```javascript
const SUNSET_BUFFER_MS = 30 * 60 * 1000;

function computeGoldenHourWindows(sunsetIso) {
  if (!sunsetIso) return [];
  const sunset = new Date(sunsetIso).getTime();
  if (Number.isNaN(sunset)) return [];
  const now = Date.now();

  return [
    {
      id: 'offensive',
      label: 'Offensive Window',
      state: 'OFFENSIVE_GOLD',
      startIso: null,
      endIso: new Date(sunset - SUNSET_BUFFER_MS).toISOString(),
      active: now < sunset - SUNSET_BUFFER_MS,
      countdownSeconds: null,
    },
    {
      id: 'golden',
      label: 'Golden Hour',
      state: 'GOLDEN_HOUR',
      startIso: new Date(sunset - SUNSET_BUFFER_MS).toISOString(),
      endIso: new Date(sunset).toISOString(),
      active: now >= sunset - SUNSET_BUFFER_MS && now <= sunset,
      countdownSeconds:
        now >= sunset - SUNSET_BUFFER_MS && now <= sunset
          ? Math.max(0, Math.floor((sunset - now) / 1000))
          : null,
    },
    {
      id: 'defensive',
      label: 'Defensive Window',
      state: 'DEFENSIVE_MIDNIGHT',
      startIso: new Date(sunset).toISOString(),
      endIso: null,
      active: now > sunset,
      countdownSeconds: null,
    },
  ];
}
```

**Update `mapWarRoomProps`** -- replace the hardcoded line:
```javascript
// BEFORE:
goldenHour: [],

// AFTER:
goldenHour: computeGoldenHourWindows(dashboard?.sunset_iso),
```

---

## Acceptance Checklist

- [ ] `_build_war_room_state` returns `sunset_iso` as an ISO-8601 string (or `null` on failure)
- [ ] `GET /api/strategist/dashboard` response includes `"sunset_iso"` field
- [ ] `computeGoldenHourWindows` returns an array of 3 window objects
- [ ] Exactly one window has `active: true` at any given time
- [ ] `goldenHour` prop in `mapWarRoomProps` is no longer hardcoded `[]`
- [ ] On failure (no location, panchang error): `sunset_iso` is `null`, `goldenHour` is `[]`, no crash
- [ ] Existing War Room render is unaffected
- [ ] Build: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` → 0 errors
