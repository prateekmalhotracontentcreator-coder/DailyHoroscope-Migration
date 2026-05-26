# CD Commission -- The Strategist Phase 2 Full UI
> Agent: Claude Design
> Module: The Strategist -- Premium Integrated Vedic Career Mentor
> Issued: 2026-05-27
> Covers: STR-2F · STR-2E · STR-2C · STR-2D · STR-2I · STR-2G · STR-2B (shell)
> Depends on: STR-R01 ✅ · STR-R02 ✅ · STR-R03 ✅ · STR-R04 ✅

---

## R-01 Gap: CLOSED ✅

The engine→prop-bag selector gap (Delivery Plan §07) is now confirmed resolved.

`StrategistWarRoomPage.jsx` fetches `/api/strategist/dashboard` + `/api/strategist/missions` on
mount and maps all engine output to the War Room prop-bag. The three props that carried placeholder
fallbacks while their backend feeds were built are now fully wired:

| Prop | Was | Now |
|---|---|---|
| `goldenHour` | `[]` placeholder | `computeGoldenHourWindows(dashboard.sunset_iso)` -- 3-window state machine (STR-R02) |
| `pitruRin` | `[]` placeholder | `dashboard.pitru_rin_ledger` -- Gate 1 records mapped to PitruRin shape (STR-R03) |
| `transition` | `undefined` placeholder | `formatTransitionDate(dashboard.current_mahadasha_end)` -- human-readable month/year (STR-R04) |

`<StrategistWarRoom />` is unmodified. R-01 delivery plan §07 satisfied.

---

## Phase 2 -- Full UI Commission

You are now commissioned to complete The Strategist module end-to-end. The goal is a single
calibration session: build everything with toggle views so the module can be reviewed and signed
off in one pass.

**Principle:** Build all components with `data-variant` or local state toggles so design options
can be switched live in the browser. Do not deliver single fixed layouts -- every component with a
meaningful design choice gets Toggle View A/B built in.

---

## What the Backend Already Returns (no blockers)

All data below flows from `GET /api/strategist/dashboard`. No new backend work needed for these:

```
scoreboard.conquest_score, score_tier, score_directive, streak_days,
streak_tier, karmic_debt_cleared, gate0_last_verdict, gate0_days_since,
next_threshold, next_threshold_label, points_to_next

gate_summaries[5] → gate, name, status, narrative, dormant_count (G2),
planet + age_range (G3)

golden_hour[3] → state (OFFENSIVE_GOLD / GOLDEN_HOUR / DEFENSIVE_MIDNIGHT),
startIso, endIso, active, countdownSeconds

pitru_rin_ledger[] → name, type, severity, ritual, streakDays, cleared

transition → "December 2031" (formatted Mahadasha end date)
```

---

## Commission 1 -- War Room Additions (renders below existing War Room)

These two components slot directly below `<StrategistWarRoom />` on `/strategist/war-room`.
Data is live. Wire via `mapWarRoomProps()` in `StrategistWarRoomPage.jsx`.

### STR-2F: `ConquestScoreboard.jsx`

- Header: `◆ Conquest Scoreboard` (Cinzel, gold, small caps)
- **Toggle View A -- Compact:** Score number (large Cinzel gold) + tier badge + directive in 1 card row
- **Toggle View B -- Expanded:** Score + tier + directive + animated progress bar to `next_threshold`
  + streak counter (`streak_days` / `streak_tier`) + Gate 0 verdict chip (YES=emerald / WAIT=amber /
  NO=red / PRAY=purple-gold) + karmic debt badge (Cleared=emerald / Active=red)
- Default: Expanded. Toggle pill A/B in card header lets user switch

Props:
```javascript
ConquestScoreboard.propTypes = {
  scoreboard: PropTypes.object,  // dashboard.scoreboard
};
```

### STR-2E: `LKGateSummaries.jsx`

- Header: `◆ Lal Kitab Diagnostics`
- **Toggle View A -- List:** 5 rows, each: Gate number (muted) + name + status chip + 2-line truncated
  narrative. G2 appends dormant house count. G3 appends planet + age range
- **Toggle View B -- Card Grid:** 5 compact cards in 2+3 grid layout, same data, more visual breathing room
- Status chips: CLEAR=emerald / WARNING or DORMANT=red / ACTIVE=gold
- Default: List. Toggle in section header

Props:
```javascript
LKGateSummaries.propTypes = {
  gateSummaries: PropTypes.array,  // dashboard.gate_summaries
};
```

**`StrategistWarRoomPage.jsx` wiring -- add to `mapWarRoomProps()`:**
```javascript
scoreboard: dashboard?.scoreboard || null,
gateSummaries: Array.isArray(dashboard?.gate_summaries) ? dashboard.gate_summaries : [],
```

**Render below `<StrategistWarRoom {...warRoomProps} />`:**
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

## Commission 2 -- KP Pre-Flight Banners (War Room gate layer)

These render as a banner/overlay zone at the top of the War Room, above the existing components.
The KP verdict from Gate 0 (`kpVerdict` prop, already in the War Room) determines which banner is
active.

### STR-2B: KP Gate 0 Inline Panel

A compact verdict display panel showing:
- Verdict chip: YES / WAIT / NO / PRAY with appropriate colour
- Question asked (from session)
- Days since reading
- "Re-consult Gate 0" CTA if > 30 days

Use **stub verdict data** for now -- CC will wire the live KP verdict feed once KP files are
migrated (STR-2A2). The visual shell is deliverable today.

### STR-2C: Pre-flight Banners -- build all 4 states as toggle-selectable

- `YES` -- emerald banner: "Gate open. Mission execution authorised."
- `WAIT` -- amber banner: "Timing window not yet open. Hold position." + estimated re-entry signal
- `NO` -- red banner: "Gate closed. Offensive missions suspended." + redirect to remedies
- `PRAY` -- deep gold/purple banner: "Surrender protocol active. See PRAY path below." + link to STR-2I
- **Toggle:** A pill selector in the preview lets you switch between all 4 banner states for review

### STR-2D: Score-Gated Re-Entry Loop

Compact UI block that appears when verdict is NO or WAIT:
- Current score vs required threshold (e.g. "Score 58 → need 60 for NO gate to clear")
- Progress indicator
- Primary CTA: "Accelerate with Remedies"
- **Toggle View A:** Minimal (score gap + CTA only) | **Toggle View B:** Expanded (timeline estimate
  + remedy shortcuts)

---

## Commission 3 -- PRAY Path (STR-2I)

Renders when Gate 0 verdict = PRAY. Surfaces below the PRAY banner.

- Section header: `◆ Surrender Protocol`
- Mantra block: Command Planet mantra (stub text, styled as verse with gold left border, Cinzel font)
- LK Debt Audit summary: links to the Pitru Rin ledger (already built in War Room)
- Surrogate Bridge CTA: links to `/strategist/surrogate`
- **Toggle View A -- Minimal:** Mantra + 1 CTA | **Toggle View B -- Full:** Mantra + Debt Audit
  summary rows + Surrogate CTA + 43-Day Tracker shortcut

---

## Commission 4 -- Unified Action Plan Page (STR-2G · `/strategist/action-plan`)

Full page -- route already exists at `StrategistActionPlanPage.jsx`. Replace stub with complete layout.

Sections (all use stub data -- CC wires live data after):

1. `◆ Strategic Situation` -- conquest score summary + active verdict + current Dasha period (transition date)
2. `◆ Active Missions` -- mission cards (3 stub cards, card pattern from existing War Room)
3. `◆ Karmic Clearance` -- Pitru Rin ledger rows + ritual streak
4. `◆ 43-Day Roadmap` -- timeline visualization (7 rows, each row = 1 week, shows Mission / Remedy / Ritual columns)
5. `◆ Recommended Remedies` -- 3 remedy cards with planet, action, timing window

**Toggle View:** Top-right toggle switches between `Command View` (dense, data-heavy) and
`Briefing View` (narrative-first, summary language)

---

## Dependency Map -- Build Order

**NOW (no blockers):**
```
STR-2F  ConquestScoreboard
STR-2E  LKGateSummaries
STR-2C  Pre-flight banners (all 4 states -- stub verdict data)
STR-2D  Score-gated re-entry loop
STR-2I  PRAY path
STR-2G  Action Plan page
```

**BLOCKED on KP files (STR-2A2 -- pending):**
```
STR-2B  KP Gate 0 inline panel (needs /krishna-prashnavali backend)
→ Build the visual shell for STR-2B with stub KP data now.
  CC will wire the live verdict feed once KP files are migrated.
```

**Build everything now. For STR-2B, deliver the visual shell only -- backend wiring follows.**

**Delivery order: 2F → 2E → 2C → 2D → 2I → 2G → 2B shell last**

---

## Style Reference (do not modify these files -- use for pattern only)

| File | What to reference |
|---|---|
| `frontend/src/styles/strategist-tokens.css` | Full token registry -- use `var(--strategist-*)` exclusively |
| `frontend/src/components/strategist/war-room/StrategistWarRoom.jsx` | Card patterns, layout structure, section header style |
| `frontend/src/components/strategist/ControlRoomBackdrop.jsx` | Backdrop pattern for full-page sections |
| `frontend/src/components/strategist/StrategistThemeProvider.jsx` | Theme wrapper -- all new pages wrap with this |
| `frontend/src/components/strategist/StrategistThemeToggle.jsx` | Toggle pill pattern for A/B view selectors |

**All components must render correctly across all 4 theme modes: light / dark / cr-ambient /
cr-tactical.** Zero hardcoded hex values. Use `var(--strategist-*)` tokens only.

---

## Delivery Format

- New component files: `frontend/src/components/strategist/war-room/`
- New page files: `frontend/src/pages/strategist/`
- No App.js changes (routes already exist)
- No backend changes
- No modifications to any existing War Room components
- Build test: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` → 0 errors

---

## Acceptance Checklist

- [ ] `ConquestScoreboard.jsx` -- Toggle A/B renders correctly, both views, no hardcoded hex
- [ ] `LKGateSummaries.jsx` -- Toggle A/B, all 5 gates, status chips correct colours
- [ ] Pre-flight banners (STR-2C) -- all 4 verdict states toggle-selectable
- [ ] Score-Gated Re-Entry (STR-2D) -- Toggle A/B, progress bar visible
- [ ] PRAY Path (STR-2I) -- Toggle A/B, all 3 CTAs present
- [ ] Action Plan page (STR-2G) -- all 5 sections, Command/Briefing toggle
- [ ] KP Gate 0 Panel shell (STR-2B) -- stub data renders without crash
- [ ] All components render correctly in all 4 theme modes (light / dark / cr-ambient / cr-tactical)
- [ ] `StrategistWarRoomPage.jsx` wired for STR-2E + STR-2F props
- [ ] Build: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` → 0 errors
