# CD Commission: STR-CD-WRS · War Room Horizontal Scroll Layout
> Issued: 2026-05-30 | Status: 🔵 READY TO SEND TO CD
> Module: The Strategist | Surface: `/strategist/war-room`
> Brief author: Temple Team | Design authority: CD

---

## 1. Context

The War Room page currently renders its 5 content layers (Gate 0 sub-header + Conquest Score / Mission Board / Dasha Timeline / Pitru-Rin Ledger / Golden Hour) as a **vertical stack** on desktop and as a **horizontal snap-scroll strip** only on mobile (< 768 px).

The Temple Team decision is: **the entire War Room should feel like a native app -- horizontal flick/scroll across all viewports, not just mobile.** Each layer occupies its own "screen" or "panel" in the scroll, and the user swipes or clicks through them.

The current desktop grid layout (CSS Grid 2-col / 3-row) is being retired in favour of this horizontal scroll architecture.

---

## 2. The Surfaces to Redesign

| Layer | ID | Current component |
|---|---|---|
| Gate 0 Sub-header | Layer 0 | `Gate0SubHeader.jsx` -- KP verdict strip |
| Conquest Score | Layer 1 | `ConquestGauge.jsx` + `FactorTable.jsx` -- gauge + breakdown |
| Mission Board | Layer 2 | `MissionCard.jsx` grid -- mission cards |
| Dasha Timeline | Layer 3 | `DashaTimeline.jsx` -- mahadasha + antardasha bars |
| Pitru-Rin Ledger | Layer 4 | `PitruRinLedger.jsx` -- ancestor debt rows |
| Golden Hour | Layer 5 | `GoldenHourStrip.jsx` -- time window strip |

Gate 0 (Layer 0) currently sits above the scroll area as a sticky sub-header. **It should remain fixed/sticky at the top** and is NOT part of the horizontal scroll. Layers 1-5 are the scrollable panels.

---

## 3. Design Brief

### 3.1 Overall Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Gate 0 Sub-header (sticky)                             │
│  KP Verdict · Conquest Score compact · Recalibrate CTA  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ◀  [ Layer 1: Conquest Score ] → swipe/arrow → L2 ...  │
│                                                         │
│  · · ● · ·   ← page indicator dots (5 dots)            │
└─────────────────────────────────────────────────────────┘
```

- Horizontal scroll container, **full viewport width**
- Each layer panel: **full-width panel** (100vw or capped at e.g. 900px on ultra-wide)
- Smooth **CSS scroll-snap** (`scroll-snap-type: x mandatory`)
- **Navigation:** two options -- CD decides which to use:
  - Option A: Side arrow buttons (left/right `◀ ▶`)
  - Option B: Swipe / keyboard arrow only with dot indicators
  - Option C: Hybrid -- dots + keyboard, no visible arrow buttons
- **Page indicator dots:** 5 dots, active dot scales up or fills with gold
- Layer label chip at top-left of each panel: `L1 · Conquest Score`, `L2 · Mission Board`, etc. (same style as current layer pills in StrategistPage.jsx nav)

### 3.2 Panel Design Notes

**General rule:** Each panel should feel self-contained -- a screen, not a card. Full-height panels. The user should not need to vertically scroll within a panel (unless the content is inherently tall, e.g. Mission Board with many cards -- in that case, the panel can scroll vertically internally).

**Layer 1 -- Conquest Score panel:**
- The existing gauge + factor table side-by-side layout (the `ConquestPanel` component) fills the panel
- Band-colour header accent (emerald / amber / orange / red based on score tier)
- The panel background can use a subtle band-colour tint

**Layer 2 -- Mission Board panel:**
- Mission cards in a responsive 2-column grid within the panel
- Variant toolbar (module / orbit / tactical) remains
- If missions overflow the panel height, enable internal vertical scroll

**Layer 3 -- Dasha Timeline panel:**
- Full-width dasha bars -- expanded view (not compact)
- Mahadasha + Antardasha timing prominently displayed

**Layer 4 -- Pitru-Rin Ledger panel:**
- Debt rows or empty state
- The panel should feel solemn -- no excess chrome

**Layer 5 -- Golden Hour panel:**
- 3-window state machine (Offensive / Golden / Defensive)
- Time display prominent -- this is a live-data panel

### 3.3 Theme Compatibility

All 4 Strategist themes must work: `light` · `dark` · `cr-ambient` · `cr-tactical`.

The horizontal scroll architecture uses CSS tokens from `strategist-tokens.css` -- CD has full access to extend/add tokens as needed for the new layout.

### 3.4 Navigation & Scroll Behaviour

- **Keyboard:** Left/Right arrow keys advance the active panel
- **Touch/mouse:** Native horizontal swipe / drag
- **Focus management:** When advancing to a panel, the panel heading receives focus (for screen reader compatibility)
- **URL hash update (optional):** TT decision -- CD can propose whether advancing panels updates `#layer-1`, `#layer-2` etc. in the URL for deep-linking

### 3.5 Mobile vs Desktop

The design should be **identical** on mobile and desktop -- one horizontal scroll implementation for all viewports. The current split (snap on mobile, grid on desktop) is being retired entirely.

Panel width:
- Mobile (< 768px): `100vw`
- Tablet (768-1200px): `100vw` (or slight inset for breathing room -- CD decides)
- Desktop (> 1200px): `min(100vw, 1100px)` centred -- panels should not feel lost on ultra-wide screens

---

## 4. Deliverable Spec

CD must deliver:

| # | Deliverable | Format |
|---|---|---|
| 1 | Standalone HTML file: `war-room-h-scroll.html` | Self-contained · window.SEEKER mock · all CSS inline or in `<style>` |
| 2 | All 4 theme variants shown | Use `data-mode` toggles in the HTML or separate screenshots |
| 3 | Active-panel state shown | Show each of the 5 layer panels in the design |
| 4 | Dot indicator and navigation element designs | Included in the HTML |
| 5 | CSS token additions (if any) | Listed in a comment block at top of `<style>` |

**Integration notes for CC (to embed in the HTML for CC reference):**
- The scroll container replaces `wr__grid` and `wr__snap` in `StrategistWarRoom.jsx`
- `Gate0SubHeader` stays outside the scroll as a sticky element
- No changes to individual layer component internals -- only the shell/wrapper layout changes
- The `layout` prop on `StrategistWarRoom` will be retired (was `'grid' | 'snap'`) -- replaced by this unified horizontal scroll

---

## 5. Reference Files

| File | Purpose |
|---|---|
| `frontend/src/components/strategist/war-room/StrategistWarRoom.jsx` | Current shell -- layout to replace |
| `frontend/src/components/strategist/war-room/war-room.css` | Current CSS -- `.wr`, `.wr__grid`, `.wr__snap` |
| `frontend/src/styles/strategist-tokens.css` | Token registry -- all CSS vars available |
| `Codex_Deliveries/Strategist/CODEX_COMMISSION_STR_R01_WAR_ROOM_SELECTOR.md` | Original War Room commission -- context |

---

## 6. Open Questions for CD

1. Should the transition between panels be instant snap, smooth scroll (300ms), or a fade-crossfade?
2. Should Panel 2 (Mission Board) compress its grid to fit within one viewport height, or allow internal vertical scroll?
3. Should the Gate 0 Sub-header include a minimal layer-position indicator (e.g. `Layer 2 of 5`) or only the dot row handles navigation state?
4. On desktop, should left/right arrow nav buttons appear on panel hover, or always be visible?

---

## 7. Commission Priority

| Field | Value |
|---|---|
| Priority | 🟠 HIGH -- currently module un-wired (diagnostic in progress) |
| Blocking | War Room re-wire (Phase 5 of diagnostic plan) |
| Bundle with | Any other War Room post-diagnostic CD commissions |
| Estimated CD effort | Medium -- layout change, component internals unchanged |
