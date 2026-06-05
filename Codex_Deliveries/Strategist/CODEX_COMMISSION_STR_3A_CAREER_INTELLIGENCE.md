# Codex Commission -- STR-3A: Career Intelligence Layer
> Module: The Strategist
> Closes: STR-OP-31 (KP guidance surfaced in UI), STR-OP-32 (LK remedy linked to missions), STR-OP-33 (transit narrative bar)
> Depends on: STR-FIX-1/2/3 ✅ (`dc4b557` -- Shadbala + transit missions + Digbala fixed)
> Last updated: 2026-06-05

---

## What This Commission Delivers

The Strategist backend now returns real data -- live Shadbala, transit-triggered missions, LK gate diagnostics, KP Oracle verdicts. What is still missing is **narrative intelligence** in the UI: the module shows numbers and chips but does not tell the user *what any of it means for their career right now*.

This commission adds three intelligence layers to existing components. No new pages. No new routes. No backend changes.

---

## What You Must NOT Touch

| File | Rule |
|---|---|
| `backend/strategist_router.py` | Do NOT modify. All required fields already in API response. |
| `backend/strategist_engine.py` | Do NOT modify. |
| `backend/vedic_calculator.py` | Do NOT touch. |
| `frontend/src/pages/strategist/WarRoomHScrollPage.jsx` | Only add the TransitBar component defined below -- do not restructure panels or nav. |
| `frontend/src/pages/strategist/StrategistActionPlanPage.jsx` | Only add the KP guidance block and mission remedy links defined below -- do not restructure sections. |
| Any `.css` file that already exists | Append new rules only -- never overwrite existing rules. |

---

## Intelligence Layer 1 -- Transit Narrative Bar (WarRoomHScrollPage, Panel 1)

### Where it goes

Inside `PanelConquest` (Panel 1 / Conquest Score), immediately below the `<WrsGauge>` SVG and above the war-state segments strip.

### What it looks like

A slim horizontal bar (full panel width, ~52px tall) with a dark parchment background (`#1a1208` in dark/cr modes, `#f5efe0` in light). It shows the **single most significant active transit** for the user's command planet today.

```
┌─────────────────────────────────────────────────────────────────────┐
│  ⚡  Sun is in your 10th House  ·  Authority Expansion window open  │
│     Mission: Operation Solar South  ·  Act before Oct 2026          │
└─────────────────────────────────────────────────────────────────────┘
```

- Left icon: a glyph that matches the command planet (use the existing `PLANET_DP_CLASS` map for the `.wrs-dp-*` class)
- Centre text: `[Planet] is in your [Nth] House · [narrative from mission record]`
- Right text: Mission name (from `missions[0].name` if available) + dasha end date
- If no transit mission fires: show `"[CommandPlanet] Dasha active · [directive from conquest_probability.directive]"` as fallback

### Data contract

All required data is already in the `dashboard` API response that `WarRoomHScrollPage` fetches:

```js
// dashboard response fields you need:
dashboard.command_planet              // "Sun", "Saturn", etc.
dashboard.conquest_probability.directive  // "Expansion / All-In"
dashboard.current_mahadasha           // "Saturn"
dashboard.current_mahadasha_end       // "2028-11-14"

// missions array (from /api/strategist/missions):
missions[0].planet                    // "Sun · H10"
missions[0].name                      // "Operation Solar South"
missions[0].obj                       // objective text
```

`missions` is already fetched in `WarRoomShell` via `useEffect`. Use `missions[0]` for the bar if available.

### CSS

Add a new class `.wrs-transit-bar` to `war-room-hscroll.css`:
```css
.wrs-transit-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  border-radius: 8px;
  margin: 12px 0;
  font-size: 13px;
  line-height: 1.4;
}
[data-mode="light"] .wrs-transit-bar   { background: #f0e8d0; color: #2a2418; border: 1px solid #c5a059; }
[data-mode="dark"] .wrs-transit-bar    { background: #1a1208; color: #e8d5a0; border: 1px solid #8a6a2a; }
[data-mode="cr-ambient"] .wrs-transit-bar { background: #0d1a0d; color: #7adb7a; border: 1px solid #3a6a3a; }
[data-mode="cr-tactical"] .wrs-transit-bar { background: #0d1a0d; color: #7adb7a; border: 1px solid #3a6a3a; }
.wrs-transit-bar__planet { font-size: 16px; flex-shrink: 0; }
.wrs-transit-bar__body   { flex: 1; }
.wrs-transit-bar__title  { font-weight: 600; }
.wrs-transit-bar__sub    { opacity: 0.75; font-size: 11px; margin-top: 2px; }
.wrs-transit-bar__right  { text-align: right; font-size: 11px; opacity: 0.7; flex-shrink: 0; }
```

---

## Intelligence Layer 2 -- LK Remedy Linked to Each Mission (WarRoomHScrollPage, Panel 2)

### Where it goes

Inside `PanelMissions` (Panel 2), at the bottom of each mission card, when `mission.rem` (remedy ref) is non-empty.

### What it adds

A single line below each mission card's KPI row:

```
┌──────────────────────────────────────────────────────────────────────┐
│  [KPI line already there]                                            │
│  ◈ Remedy · [mission.rem]                          → LK Remedies   │
└──────────────────────────────────────────────────────────────────────┘
```

- Show only when `m.rem` (the `lk_remedy_ref` field) is non-empty
- `→ LK Remedies` is a small link: `<Link to="/lk-remedies/remedies">→ LK Remedies</Link>`
- This closes the loop: transit fires → mission card → specific LK remedy → user acts

### CSS (append to `war-room-hscroll.css`):
```css
.wrs-mission-remedy {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 6px;
  padding-top: 6px;
  border-top: 1px solid rgba(197,160,89,0.2);
  font-size: 11px;
  opacity: 0.8;
}
.wrs-mission-remedy__label { color: inherit; }
.wrs-mission-remedy__link  { color: #c5a059; text-decoration: none; }
.wrs-mission-remedy__link:hover { text-decoration: underline; }
```

---

## Intelligence Layer 3 -- KP Gate 0 Guidance Block (StrategistActionPlanPage, Section §03)

### Where it goes

In `StrategistActionPlanPage.jsx`, inside the `§03 Verdict` section, **after** the `<OracleVerdictBanners>` component.

The `§03` section currently shows the verdict chip (YES/WAIT/NO/PRAY) via `OracleVerdictBanners`. It shows no text guidance from the actual KP reading.

### What it adds

A collapsible guidance block that shows the last KP Gate 0 reading's content when verdict is WAIT / NO / PRAY:

```
┌─────────────────────────────────────────────────────────────────────┐
│  ◆ Oracle Guidance  [last read: 3 days ago]              [▾ expand] │
├─────────────────────────────────────────────────────────────────────┤ ← collapsed by default
│  "Before you proceed, attend to what has been left incomplete..."    │
│                                                                     │
│  ॐ  Shri Shanaishcharaya Namah  ·  108 times on Saturday            │
│                                                                     │
│  [Re-enter Gate 0]                                                  │
└─────────────────────────────────────────────────────────────────────┘
```

### Data contract

The `/api/strategist/action-plan` response already returns:
```js
data.gate0.verdict         // "WAIT" | "NO" | "PRAY" | "YES"
data.gate0.days_since      // integer
```

The guidance text and mantra are **not** in the action-plan response yet. Add a **second fetch** on mount:

```js
// In StrategistActionPlanPage useEffect, parallel to the main fetch:
const kpRes = await fetch(`${BACKEND}/api/strategist/gate0/status`, {
  headers: { Authorization: `Bearer ${token}` }
});
const kpData = await kpRes.json();
// kpData.last_verdict, kpData.conquest_score etc already available
```

For the actual guidance text: fetch the last KP session report if verdict is non-YES. Use:
```js
// Only when verdict is WAIT/NO/PRAY:
const reportRes = await fetch(
  `${BACKEND}/api/kp/sessions/last?context=strategist_gate0`,
  { headers: { Authorization: `Bearer ${token}` } }
);
```

**Note to CC on integration:** The `/api/kp/sessions/last` endpoint may not exist yet. If it does not return data, show a static fallback: `"Return to Gate 0 to receive new Oracle guidance."` with a `[Re-enter Gate 0]` CTA linking to `/strategist`. Do NOT break the section if this fetch fails.

### Show condition

Only render this block when `gate0.verdict` is `"WAIT"`, `"NO"`, or `"PRAY"`. When `"YES"` or null: do not render.

### CSS (append to `strategist-2g-actionplan.css`):
```css
.ap-kp-guidance {
  margin-top: 16px;
  border: 1px solid var(--strategist-card-border, #c5a059);
  border-radius: 10px;
  overflow: hidden;
}
.ap-kp-guidance__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  background: var(--strategist-card-bg, #fff);
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  color: var(--strategist-fg, #2a2418);
}
.ap-kp-guidance__meta { font-size: 11px; font-weight: 400; opacity: 0.65; margin-left: 8px; }
.ap-kp-guidance__body {
  padding: 14px 16px;
  background: var(--strategist-card-elev, #fbf7ec);
  font-size: 13px;
  line-height: 1.6;
  color: var(--strategist-fg, #2a2418);
}
.ap-kp-guidance__mantra {
  margin-top: 12px;
  padding: 10px 14px;
  border-left: 3px solid #c5a059;
  font-style: italic;
  opacity: 0.9;
}
.ap-kp-guidance__cta {
  display: inline-block;
  margin-top: 12px;
  padding: 7px 16px;
  background: #c5a059;
  color: #fff;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  text-decoration: none;
}
```

---

## Deliverables Checklist

| File | Change type |
|---|---|
| `frontend/src/pages/strategist/WarRoomHScrollPage.jsx` | Add `WrsTransitBar` component + render in `PanelConquest`; add remedy line to mission cards in `PanelMissions` |
| `frontend/src/styles/war-room-hscroll.css` | Append `.wrs-transit-bar*` and `.wrs-mission-remedy*` CSS blocks |
| `frontend/src/pages/strategist/StrategistActionPlanPage.jsx` | Add second fetch for gate0 status + guidance; add `ApKpGuidance` component; render in §03 section |
| `frontend/src/styles/strategist-2g-actionplan.css` | Append `.ap-kp-guidance*` CSS block |

**No new files. No new routes. No backend changes. Append-only to CSS.**

---

## Integration Notes for CC

1. `WarRoomHScrollPage` already imports `Link` from `react-router-dom` -- use it for the remedy link.
2. The `missions` array in `WarRoomShell` already maps through `normalizeMissions()` -- `m.rem` is the remedy ref field.
3. `StrategistActionPlanPage` already has a `token` in state and a `BACKEND` const -- reuse them for the gate0 fetch.
4. All CSS is append-only. The existing `.wrs-*` and `.ap-*` namespaces are stable.
5. If the `/api/kp/sessions/last` endpoint does not yet exist, skip the guidance text and show only the static CTA line. The collapsible block should still render with fallback text.
