# Codex Commission -- STR-3B: Command Planet Strength Panel
> Module: The Strategist
> Closes: STR-OP-34 (Shadbala strength display)
> Depends on: STR-FIX-1 ✅ (`dc4b557` -- real Shadbala now in dashboard API response)
> Last updated: 2026-06-05

---

## What This Commission Delivers

The Strategist backend (`GET /api/strategist/dashboard`) now returns a `command_planet_shadbala` dict with the user's command planet's Vedic strength score. This data is live but invisible -- nothing in the UI displays it.

This commission adds a **Command Planet Strength Panel** to the Conquest Score layer (Panel 1 of the H-scroll War Room) and a matching compact chip to the snapshot page's ConquestScoreboard.

No backend changes. No new routes. Append-only to existing components.

---

## What You Must NOT Touch

| File | Rule |
|---|---|
| `backend/` -- any file | Do NOT modify. |
| Existing `.wrs-*` CSS classes | Do NOT modify existing rules. Append only. |
| `StrategistWarRoom.jsx` and sub-components | Do NOT touch. |
| Panel structure or nav logic in `WarRoomHScrollPage.jsx` | Do NOT restructure. Add component in Panel 1 only. |

---

## API Data Available

`GET /api/strategist/dashboard` returns (as of `dc4b557`):

```json
{
  "command_planet": "Saturn",
  "command_planet_shadbala": {
    "rupas": 7.42,
    "minimum_rupas": 5.0,
    "strength_ratio": 1.484,
    "is_strong": true
  },
  "conquest_probability": {
    "score": 65,
    "tier": "Operational Friction",
    "directive": "Patch & Pivot",
    "factors": [
      { "factor": "Shadbala", "delta": 10, "detail": "Command planet strong" },
      ...
    ]
  }
}
```

`strength_ratio` is `null` when birth details are unavailable (fall back to showing nothing).
`is_strong` is `null` when birth details unavailable.

---

## Deliverable 1 -- `WrsShadbalaPanel` component (add to `WarRoomHScrollPage.jsx`)

A self-contained component rendered inside `PanelConquest`, below the transit bar (from STR-3A) and above the war-state segments.

### Visual design

```
┌─────────────────────────────────────────────────────────────────────┐
│  Command Planet Strength  ·  Saturn (Shani)                         │
│                                                                     │
│  ██████████████████░░░░░░░  148%  STRONG                           │
│  Shadbala: 7.42 rupas  ·  Minimum: 5.00 rupas                      │
│                                                                     │
│  Factor contribution: +10 to Conquest Score                         │
└─────────────────────────────────────────────────────────────────────┘
```

**When `is_strong = true`:** filled progress bar at `strength_ratio * 66%` width (capped at 100%), label "STRONG", green accent.
**When `is_strong = false`:** bar at `strength_ratio * 66%` width, label "NEEDS SUPPORT", amber accent.
**When `is_strong = null` (no birth data):** do not render the panel at all.

The strength ratio 1.0 = threshold. Map to bar:
```js
const barPct = Math.min(100, Math.round((strengthRatio / 2.0) * 100));
// 1.0 ratio → 50% bar, 2.0 ratio → 100% bar, 0.5 ratio → 25% bar
```

### Props

```js
function WrsShadbalaPanel({ dashboard }) {
  const bala = dashboard?.command_planet_shadbala;
  if (!bala || bala.strength_ratio === null) return null;
  // ... render
}
```

### CSS (append to `war-room-hscroll.css`):

```css
.wrs-shadbala {
  margin: 12px 0;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid rgba(197,160,89,0.3);
}
[data-mode="light"] .wrs-shadbala    { background: #faf4e6; }
[data-mode="dark"] .wrs-shadbala     { background: #1a150a; }
[data-mode="cr-ambient"] .wrs-shadbala,
[data-mode="cr-tactical"] .wrs-shadbala { background: #0a150a; border-color: rgba(58,106,58,0.4); }

.wrs-shadbala__title { font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; opacity: 0.65; margin-bottom: 8px; }
.wrs-shadbala__track {
  height: 6px; border-radius: 3px;
  background: rgba(197,160,89,0.2);
  margin: 6px 0;
  overflow: hidden;
}
.wrs-shadbala__fill {
  height: 100%; border-radius: 3px;
  transition: width 0.6s ease;
}
.wrs-shadbala__fill--strong { background: #4caf72; }
.wrs-shadbala__fill--weak   { background: #c5a059; }

.wrs-shadbala__row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 13px;
}
.wrs-shadbala__label { font-weight: 600; }
.wrs-shadbala__badge {
  padding: 2px 8px; border-radius: 10px;
  font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;
}
.wrs-shadbala__badge--strong { background: rgba(76,175,114,0.2); color: #4caf72; }
.wrs-shadbala__badge--weak   { background: rgba(197,160,89,0.2); color: #c5a059; }
.wrs-shadbala__meta { font-size: 11px; opacity: 0.65; margin-top: 4px; }
.wrs-shadbala__factor { font-size: 11px; margin-top: 6px; opacity: 0.8; }
```

---

## Deliverable 2 -- Shadbala chip on ConquestScoreboard (StrategistWarRoomPage snapshot)

In `frontend/src/pages/strategist/StrategistWarRoomPage.jsx`, the `<ConquestScoreboard>` already receives `scoreboardData`. Add a `shadbalaBadge` prop to the `scoreboardData` object:

```js
// In mapWarRoomProps() or wherever scoreboardData is assembled:
scoreboardData: {
  // ... existing fields ...
  shadbalaBadge: data.command_planet_shadbala?.is_strong === true
    ? `${data.command_planet} · Strong`
    : data.command_planet_shadbala?.is_strong === false
      ? `${data.command_planet} · Needs Support`
      : null,
}
```

In `ConquestScoreboard.jsx`, if `scoreboardData.shadbalaBadge` is present, render it as a small `<KarmicChip>` (already defined in `StrategistPrimitives.jsx`) below the conquest score gauge.

If `is_strong === null`: do not render the chip.

---

## Deliverables Checklist

| File | Change type |
|---|---|
| `frontend/src/pages/strategist/WarRoomHScrollPage.jsx` | Add `WrsShadbalaPanel` component; render inside `PanelConquest` |
| `frontend/src/styles/war-room-hscroll.css` | Append `.wrs-shadbala*` CSS block |
| `frontend/src/pages/strategist/StrategistWarRoomPage.jsx` | Add `shadbalaBadge` to `scoreboardData` in `mapWarRoomProps` |
| `frontend/src/pages/strategist/phase2/ConquestScoreboard.jsx` | Render `shadbalaBadge` as `<KarmicChip>` when present |

**No new files. No new routes. No backend changes.**
