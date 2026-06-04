# Codex Commission · PAN-TM-1
## The Cosmic Clock -- Panchang Time Map Redesign
> Module: Panchang · Route: `/panchang/today` (embedded in PanchangPage)
> Issued: 2026-06-03 · Revised: 2026-06-04
> Priority: 🟠 HIGH
> Type: CD Visual Redesign -- HTML + CSS + Interaction prototype only.

---

## READ THIS FIRST -- Role Split

This commission is **Design only**. The backend engine logic is already built by CC and is
NOT your concern. You will receive a clean, pre-computed data object (defined in §4).
You render it beautifully. You do not compute muhurat timings, parse ISO strings, calculate
solar arc positions, or touch any API.

```
CC owns:  API calls · ISO time parsing · hour-from-clock · pct() geometry · window segmenting
CD owns:  Parchment scroll · Embroidery border · Magnifying glass lens · Colour system · Typography · Interactions
```

---

## 1. What Already Exists (CC-Built -- Do Not Rebuild)

### 1.1 Existing Component
File: `frontend/src/components/PanchangCosmicMap.jsx`
File: `frontend/src/panchang.css` (CSS tokens + all `.panchang-cosmic-map__*` class rules)

The current component renders a functional but visually basic Time Map. It already handles:
- Fetching from `/api/panchang/daily?location_slug=X&date=Y`
- Computing `sunriseH`, `sunsetH`, `dayStart`, `dayEnd` (all in decimal hours, e.g. `6.38`)
- Computing `focusHour` from cursor position as a decimal hour
- Building `timeWindows` array (each: `{ label, start, end, tone }` -- start/end already in decimal hours, `left%` and `width%` already computed)
- Building `timeRows` array (Tithi/Nakshatra/Yoga/Karana -- each segment with name, left%, width%)
- `solarIntensity(focusHour)` -- returns 0-1 float
- `formatHour(decimalHour)` -- returns formatted string like "12:33 PM"
- Active window detection at any cursor position
- Active limb (Tithi/Nakshatra/Yoga/Karana) at any cursor position

### 1.2 Existing CSS Tokens (from `panchang.css` :root)
These tokens are already defined globally. Use them -- do not redefine:
```css
--panchang-bg:           #f6efe1
--panchang-surface:      rgba(255, 250, 240, 0.84)
--panchang-surface-strong: #fff8ed
--panchang-ink:          #2d2318
--panchang-muted:        #6e6251
--panchang-line:         rgba(77, 56, 32, 0.14)
--panchang-saffron:      #c67f20
--panchang-saffron-deep: #8d5614
--panchang-vermilion:    #b34d22
--panchang-leaf:         #5e7441
--panchang-shadow:       0 20px 48px rgba(74, 50, 24, 0.12)
--panchang-radius-xl:    30px
--panchang-radius-lg:    20px
--panchang-radius-md:    14px
```

### 1.3 What CC Will Wire After Delivery
Once you deliver `pan-tm1-cosmic-clock.html`, CC will:
1. Convert to `PanchangCosmicMapV2.jsx` (React component, props: `{ locationSlug, dayOffset }`)
2. Replace the hardcoded `DEMO` object with the live engine output (same shape -- §4)
3. Add your CSS as `.ptm-*` classes in `panchang.css`
4. Swap one import line in `PanchangPage.jsx`

---

## 2. Deliverable

**One file:** `pan-tm1-cosmic-clock.html`

Requirements:
- Completely standalone (no external CDN beyond Google Fonts)
- All CSS in a `<style>` block, all JS in a `<script>` block at end of `<body>`
- Uses the hardcoded `DEMO` object from §5 -- no API calls
- Interactive: mouse/touch move along the scroll updates the magnifying lens
- Renders cleanly at 1280px, 960px, 768px, 375px
- No React, no build step, no npm -- pure HTML/CSS/vanilla JS

---

## 3. Reference Image

The reference image (attached to this thread) establishes the non-negotiable visual mood:

**Lock these 10 elements:**
1. Parchment scroll with rolled left/right ends -- the entire timeline sits on this scroll
2. Circular magnifying glass with thick bronze rim and gold angled handle
3. Glass focused on the green Abhijit window -- green tint inside glass when over auspicious window
4. Green pill band for auspicious windows (Brahma Muhurta, Abhijit, Vijaya, Amrit Kalam)
5. Red pill band for inauspicious windows (Rahu Kaal, Yamaganda, Gulika, Dur Muhurta)
6. Clock SVG icon visible inside each window pill (inline SVG, not emoji)
7. Embroidery border frame inside the scroll -- lotus corner ornaments, double-line frame
8. Hour tick marks readable along the scroll bottom edge
9. Critical Guidance bar at bottom -- bold, coloured by window type
10. Background outside the scroll uses `--panchang-bg: #f6efe1` (already the app's page colour)

**Permitted adaptations for web interactivity:**
- Reference is a static image -- the web version animates (cursor pulse, lens tracks mouse)
- Reference shows one focused moment -- web version is fully interactive (any hour)
- Constellation dots in the background (top-right of reference) -- include if time permits

---

## 4. The Data Contract -- What CC Hands to CD's Component

This is the exact shape of the pre-computed object your component will receive.
All heavy computation is done by CC before reaching your render layer.
In the prototype, this is the `DEMO` constant (§5).

```js
const data = {
  // ── Identity ────────────────────────────────────────────────────
  locationLabel: "New Delhi, India",       // string
  dateLabel:     "Tuesday, 3 June 2026",   // pre-formatted string
  sunriseLabel:  "05:23 AM",               // pre-formatted
  sunsetLabel:   "07:14 PM",               // pre-formatted

  // ── Geometry (all values are 0-100 percentages across the strip) ─
  // CC has already converted decimal hours → % of (dayStart→dayEnd)
  sunrisePct:  12.4,    // % left position of sunrise marker
  sunsetPct:   90.6,    // % left position of sunset marker
  hourTicks: [          // array of tick marks to render
    { label: "5 AM",  pct: 0    },
    { label: "6",     pct: 6.25 },
    { label: "7",     pct: 12.5 },
    // ... one per hour across dayStart→dayEnd
    { label: "8 PM",  pct: 100  },
  ],

  // ── Timing Windows (pre-positioned as % strips) ─────────────────
  windows: [
    {
      label:    "Brahma Muhurta",
      quality:  "good",              // "good" | "caution" | "neutral"
      leftPct:  2.1,                 // CSS left %
      widthPct: 10.4,                // CSS width %
      timeRange: "04:47 -- 05:35 AM", // pre-formatted for display
    },
    {
      label:    "Rahu Kaal",
      quality:  "caution",
      leftPct:  22.3,
      widthPct: 20.8,
      timeRange: "07:38 -- 09:17 AM",
    },
    // ... all windows follow same shape
  ],

  // ── Panchang Limbs (for the 2×2 grid inside the lens) ───────────
  // Active values at the current focusPct -- CC recomputes on cursor move
  // In the prototype, your JS derives this from the static demo data
  activeLimbs: {
    tithi:     "Ashtami",
    nakshatra: "Shravana",
    yoga:      "Siddhi",
    karana:    "Vanija",
  },

  // ── Focus State (cursor-driven, updates on mousemove) ────────────
  // CC provides a helper: getStateAtPct(pct) → focusState
  // In the prototype, compute this from DEMO.windows + DEMO.hourTicks
  focusState: {
    pct:         47.2,               // current cursor position as %
    timeLabel:   "12:33 PM",         // pre-formatted by CC's formatHour()
    activeWindow: {                  // null if no window active
      label:    "Abhijit Muhurta",
      quality:  "good",
      timeRange: "11:51 AM -- 12:43 PM",
      subline:  "Safe Start Window", // CC derives from quality
    },
    solarIntensity: 0.94,            // 0-1 float (for lens display "Solar intensity 94%")
    glassTint: "good",               // "good" | "caution" | null (drives lens fill colour)
  },

  // ── Critical Guidance (pre-computed by CC, one of 4 tiers) ──────
  guidance: {
    tier:    "upcoming-auspicious",   // "active-auspicious" | "upcoming-auspicious" | "active-inauspicious" | "default"
    icon:    "warning",               // "star" | "warning" | "dot"
    text:    "Critical: Abhijit Muhurta opens at 11:51 AM -- the Safe Victory Window is short today. Act with precision between 11:51 AM and 12:43 PM.",
  },
};
```

**Your component's only job:** read `data`, render it. No math. No date parsing.
The only computation your JS does is updating `focusState` on mousemove -- derive `pct` from cursor X,
then look up which window contains that pct, format the time label from a simple linear interpolation
of the tick labels. Keep it under 30 lines of JS.

---

## 5. Hardcoded Demo Data (for the prototype)

```js
const DEMO = {
  locationLabel: "New Delhi, India",
  dateLabel:     "Tuesday, 3 June 2026",
  sunriseLabel:  "05:23 AM",
  sunsetLabel:   "07:14 PM",

  sunrisePct: 9.4,
  sunsetPct:  91.6,

  hourTicks: [
    { label:"4 AM", pct:0 },    { label:"5",  pct:6.25 },
    { label:"6",    pct:12.5 }, { label:"7",  pct:18.75 },
    { label:"8",    pct:25.0 }, { label:"9",  pct:31.25 },
    { label:"10",   pct:37.5 }, { label:"11", pct:43.75 },
    { label:"12",   pct:50.0 }, { label:"1 PM",pct:56.25 },
    { label:"2",    pct:62.5 }, { label:"3",  pct:68.75 },
    { label:"4",    pct:75.0 }, { label:"5",  pct:81.25 },
    { label:"6",    pct:87.5 }, { label:"7",  pct:93.75 },
    { label:"8 PM", pct:100  },
  ],

  windows: [
    { label:"Brahma Muhurta",  quality:"good",    leftPct:4.7,  widthPct:10.4, timeRange:"04:47 -- 05:35 AM" },
    { label:"Rahu Kaal",       quality:"caution", leftPct:21.5, widthPct:20.8, timeRange:"07:38 -- 09:17 AM" },
    { label:"Yamaganda",       quality:"caution", leftPct:42.0, widthPct:20.8, timeRange:"10:56 AM -- 12:35 PM" },
    { label:"Abhijit Muhurta", quality:"good",    leftPct:48.8, widthPct:10.4, timeRange:"11:51 AM -- 12:43 PM" },
    { label:"Gulika Kaal",     quality:"caution", leftPct:62.8, widthPct:20.8, timeRange:"02:13 -- 03:52 PM" },
    { label:"Vijaya Muhurta",  quality:"good",    leftPct:64.1, widthPct:10.4, timeRange:"02:30 -- 03:19 PM" },
    { label:"Dur Muhurta",     quality:"caution", leftPct:69.8, widthPct:10.4, timeRange:"03:16 -- 04:05 PM" },
    { label:"Amrit Kalam",     quality:"good",    leftPct:79.2, widthPct:20.8, timeRange:"05:02 -- 06:42 PM" },
  ],

  activeLimbs: {
    tithi:     "Ashtami",
    nakshatra: "Shravana",
    yoga:      "Siddhi",
    karana:    "Vanija",
  },

  // Initial focus = 12:33 PM (between Yamaganda and Abhijit midpoint)
  // This reproduces the reference image tip text exactly
  focusState: {
    pct:          49.5,
    timeLabel:    "12:33 PM",
    activeWindow: {
      label:    "Abhijit Muhurta",
      quality:  "good",
      timeRange: "11:51 AM -- 12:43 PM",
      subline:  "Safe Start Window",
    },
    solarIntensity: 0.94,
    glassTint:    "good",
  },

  guidance: {
    tier: "upcoming-auspicious",
    icon: "warning",
    text: "Critical: Abhijit Muhurta opens at 11:51 AM -- the Safe Victory Window is short today. Act with precision between 11:51 AM and 12:43 PM.",
  },
};
```

**Subline mapping (derive in prototype JS -- CC provides this as a utility in the real component):**
```js
function subline(quality) {
  if (quality === "good")    return "Safe Start Window";
  if (quality === "caution") return "Avoid";
  return "Neutral";
}
```

---

## 6. Layout Specification

### 6.1 Overall Structure (three stacked regions)

```
┌──────────────────────────────────────────────────────────────────┐
│  HEADER  eyebrow | "The Cosmic Clock" title | date + location    │
├──────────────────────────────────────────────────────────────────┤
│  SCROLL CANVAS  (parchment scroll with embroidery border)        │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  [MAGNIFYING GLASS]   TIMELINE STRIP                       │  │
│  │                       ── solar arc band ──                 │  │
│  │                       ── window pills   ──                 │  │
│  │                       ── hour tick row  ──                 │  │
│  └────────────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────────────┤
│  CRITICAL GUIDANCE BAR  ⚠ / ✦ / ◉  [guidance.text]              │
└──────────────────────────────────────────────────────────────────┘
```

Desktop height: ~500px total. No vertical scroll inside the component.

---

### 6.2 Parchment Scroll Canvas

The scroll canvas is the central visual. It must feel like an aged devotional scroll.

**Background:**
```css
background:
  url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)' opacity='0.04'/></svg>") repeat,
  linear-gradient(180deg, #fdf6e3 0%, #f5e8c9 28%, #f0ddb5 50%, #f5e9c8 72%, #fdf6e3 100%);
```

**Rolled scroll ends (CSS pseudo-elements):**
Add `::before` (left edge) and `::after` (right edge):
```css
position: absolute; top: 8%; bottom: 8%;
width: 32px; border-radius: 50%;
background: linear-gradient(90deg, #a87030 0%, #e8c87e 42%, #c4985a 70%, #8d6228 100%);
box-shadow: inset -4px 0 10px rgba(0,0,0,0.24), 5px 0 16px rgba(0,0,0,0.16);
```
Left end: `left: 0; transform: translateX(-40%)`
Right end: `right: 0; transform: translateX(40%); mirror the gradient`

**Embroidery border (inline SVG overlay, `position:absolute; inset:0; pointer-events:none`):**

The SVG `viewBox="0 0 1000 400"` `preserveAspectRatio="xMidYMid meet"` (scales to parent).
Draw using only `<path>` and `<use>`:

```
• Outer frame rect:   path d="M 30 20 H 970 V 380 H 30 Z"
                      stroke="rgba(130,85,20,0.22)" stroke-width="1.5" fill="none"
• Inner frame rect:   path d="M 38 28 H 962 V 372 H 38 Z"
                      stroke="rgba(160,110,40,0.35)" stroke-width="1" fill="none"

• Corner lotus (×4):  A 4-petal lotus, 24×24 units, centred on each corner of inner rect.
                      Petals drawn as 4 overlapping ellipses rotated 0/90/180/270 deg.
                      Fill: rgba(198,127,32,0.55)
                      Corners: (38,28)  (962,28)  (38,372)  (962,372)
                      Use <symbol id="lotus"> + <use href="#lotus" x="..." y="...">

• Centre-top star:    A simple 6-point asterisk at (500, 28), fill rgba(198,127,32,0.45), 12×12 units
• Centre-bottom star: Same at (500, 372)
```

---

### 6.3 Magnifying Glass Lens

Positioned: `absolute; top: 40px` vertically fixed. Horizontally follows cursor X, clamped
`[12%, 72%]` so it never clips the canvas edge.

**Glass circle:** `width: 220px; height: 220px; border-radius: 50%; overflow: hidden`

**Glass fill (3 layers):**
```css
/* Layer 1 -- tint overlay (changes with glassTint) */
background-color: rgba(64,130,75,0.10);  /* good = green tint */
/* caution = rgba(179,62,42,0.10);  red tint */
/* null    = rgba(255,248,230,0.08); neutral warm */
transition: background-color 0.28s ease;

/* Layer 2 -- glass refraction */
background: radial-gradient(circle at 30% 28%,
  rgba(255,255,255,0.72) 0%,
  rgba(220,245,230,0.50) 38%,
  rgba(195,235,215,0.32) 100%);

/* Layer 3 -- lens rim */
border: 10px solid rgba(169,128,76,0.88);
box-shadow:
  0 18px 42px rgba(80,50,16,0.22),
  inset 0 2px 8px rgba(255,240,200,0.40),
  0 0 0 3px rgba(255,236,195,0.50);
```

**Handle:**
```css
position: absolute;
bottom: -68px; right: 22px;
width: 14px; height: 80px; border-radius: 7px;
background: linear-gradient(180deg, #b8862e 0%, #8c6420 60%, #6b4b14 100%);
box-shadow: 2px 4px 10px rgba(0,0,0,0.26);
transform: rotate(-35deg);
transform-origin: top center;
```

**Content inside the glass (circular clip, centred, padding 22px):**

```
ROW 1:  [time label]          0.74rem · 800wt · letter-spacing 0.18em · uppercase · color #5b5f2d
ROW 2:  [window name]         1.25rem · 700wt · font: Playfair Display/Georgia · color #2d2318
ROW 3:  [subline]             0.76rem · 400wt · color #5e7441 (good) or #9d3f1e (caution)
ROW 4:  [timeRange]           0.78rem · 600wt · color #4a3820
──────  divider 1px rgba(150,100,40,0.18)  ──────
ROW 5:  2×2 grid: Tithi · Nakshatra · Yoga · Karana
        label: 0.68rem · 700wt · uppercase · letter-spacing 0.1em · color #5b6a3f
        value: 0.88rem · 700wt · color #2d3522
```

If `activeWindow` is null → show "Open Sky" as window name, "No restrictions active" as subline,
omit timeRange row. Show dashes in the 2×2 grid.

---

### 6.4 Timeline Strip

Positioned vertically at ~58% down the scroll canvas. Three stacked rows:

**Row A -- Solar arc band** (`height: 52px; border-radius: 999px; overflow: hidden`)
```css
background: linear-gradient(90deg,
  rgba(200,120,50,0.18) 0%,
  rgba(255,200,80,0.52) 12%,
  rgba(255,238,160,0.76) 38%,
  rgba(255,255,200,0.92) 50%,
  rgba(255,210,120,0.70) 64%,
  rgba(220,140,60,0.52) 88%,
  rgba(160,90,40,0.18) 100%);
```

Sunrise marker at `left: data.sunrisePct%`:
- Vertical tick line (`width:1px, height:24px, bg:#c67f20`)
- Half-sun icon: CSS circle `width:14px; height:7px; border-radius:7px 7px 0 0; background:#ffb835; margin:0 auto`
- Time label below: `data.sunriseLabel`

Sunset marker at `left: data.sunsetPct%`: mirror of sunrise marker.

**Row B -- Window pills** (`height: 48px; position: relative`)

Each `data.windows` entry renders as an absolute pill:
```css
position: absolute;
left:  calc(var(--w-left) * 1%);
width: calc(var(--w-width) * 1%);
height: 38px; top: 5px;
border-radius: 999px;
display: flex; align-items: center; gap: 6px;
padding: 0 10px;
white-space: nowrap; overflow: hidden;
font-size: 0.76rem; font-weight: 700; color: #fff;
```

Colour by quality:
```css
/* good    */ background: rgba(60,110,68,0.88); border: 1px solid rgba(40,90,50,0.6);
/* caution */ background: rgba(168,55,38,0.88); border: 1px solid rgba(140,40,28,0.6);
/* neutral */ background: rgba(168,120,40,0.75); border: 1px solid rgba(140,95,28,0.5);
```

Hide label text (keep colour only) if `widthPct < 6`. Show clock icon if `widthPct >= 8`.

**Clock icon SVG (inline, 15×15px):**
```svg
<svg width="15" height="15" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="8" cy="8" r="6.5" stroke="rgba(255,255,255,0.85)" stroke-width="1.3"/>
  <line x1="8" y1="8" x2="8" y2="3.8" stroke="rgba(255,255,255,0.9)" stroke-width="1.4" stroke-linecap="round"/>
  <line x1="8" y1="8" x2="11" y2="9.6" stroke="rgba(255,255,255,0.9)" stroke-width="1.4" stroke-linecap="round"/>
</svg>
```

**Row C -- Hour ticks** (`height: 22px; position: relative`)

For each entry in `data.hourTicks`:
```html
<span style="left: calc(N%)">label</span>
```
Font: `0.76rem; color: rgba(78,58,31,0.68)`. At ≤640px: show only ticks where label contains "AM"/"PM".

---

### 6.5 Cursor

A vertical indicator line tracking cursor position across the entire strip height:

```css
/* Vertical line */
position: absolute; top: 0; bottom: 0; width: 2px;
background: linear-gradient(180deg,
  transparent 0%, rgba(137,85,28,0.55) 30%,
  rgba(235,198,97,0.92) 55%, rgba(137,85,28,0.55) 80%, transparent 100%);
transform: translateX(-50%); pointer-events: none;

/* Pulse ring -- at Row B vertical centre */
width: 28px; height: 28px; border-radius: 50%;
border: 2px solid rgba(255,234,158,0.92);
box-shadow: 0 0 0 8px rgba(255,218,101,0.16);
animation: ptm-pulse 2.6s ease-in-out infinite;

/* Centre dot */
width: 10px; height: 10px; border-radius: 50%;
background: radial-gradient(circle, #fff7b5 0%, #f2ab3e 72%);
box-shadow: 0 0 16px rgba(246,184,61,0.64);
```

---

### 6.6 Critical Guidance Bar

Full-width bar below the scroll canvas:

```css
/* Tier: active-auspicious or upcoming-auspicious */
background: linear-gradient(135deg, rgba(50,100,58,0.10), rgba(80,130,78,0.07));
border-left: 4px solid #3d7344; color: #2d4a26; padding: 14px 20px;

/* Tier: active-inauspicious */
background: linear-gradient(135deg, rgba(150,50,32,0.10), rgba(180,70,42,0.07));
border-left: 4px solid #b33e2a; color: #7a2810;

/* Tier: default */
background: rgba(198,127,32,0.09);
border-left: 4px solid #c67f20; color: #5a3a10;
```

Icon prefix: `✦` (auspicious) · `⚠` (inauspicious/upcoming-auspicious) · `◉` (default)
Font: `0.92rem; font-weight: 700; line-height: 1.5`

---

### 6.7 Header

```html
<p class="ptm-eyebrow">Time Map · The Cosmic Clock</p>
<h2 class="ptm-title">{locationLabel} -- {dateLabel}</h2>
<p class="ptm-subtitle">Move across the scroll to inspect any moment of the day.</p>
```

Typography:
- Eyebrow: `0.74rem · 700 · uppercase · letter-spacing 0.22em · color var(--panchang-saffron-deep)`
- Title: `Playfair Display / Georgia · clamp(1.8rem,3.5vw,2.6rem) · color var(--panchang-ink)`
- Subtitle: `0.86rem · var(--panchang-muted)`

---

## 7. Typography

| Element | Font | Size | Weight | Colour |
|---|---|---|---|---|
| Eyebrow | system-ui | 0.74rem | 700 | `var(--panchang-saffron-deep)` |
| Title | Playfair Display / Georgia | clamp(1.8,3.5vw,2.6rem) | 400 | `var(--panchang-ink)` |
| Subtitle | system-ui | 0.86rem | 400 | `var(--panchang-muted)` |
| Lens time | system-ui | 0.74rem | 800 | `#5b5f2d` |
| Lens name | Playfair Display / Georgia | 1.25rem | 700 | `var(--panchang-ink)` |
| Lens subline | system-ui | 0.76rem | 400 | `#5e7441` / `#9d3f1e` |
| Lens time range | system-ui | 0.78rem | 600 | `#4a3820` |
| Lens grid labels | system-ui | 0.68rem | 700 | `#5b6a3f` |
| Lens grid values | system-ui | 0.88rem | 700 | `#2d3522` |
| Window pill text | system-ui | 0.76rem | 700 | `#fff` |
| Hour ticks | system-ui | 0.76rem | 400 | `rgba(78,58,31,0.68)` |
| Guidance bar | system-ui | 0.92rem | 700 | *varies by tier* |

Google Fonts import (add to `<head>`):
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
```

---

## 8. CSS Architecture

**All classes must use the `.ptm-` prefix.** The existing `panchang.css` uses `.panchang-*`.
Do not touch or override any `.panchang-*` class.

Core class names:
```
.ptm-shell            outer wrapper
.ptm-header           header row
.ptm-scroll           parchment scroll canvas
.ptm-scroll__border   SVG embroidery border (absolute overlay)
.ptm-lens             magnifying glass assembly (glass + handle)
.ptm-lens__glass      circular glass element
.ptm-lens__handle     gold angled handle
.ptm-lens__content    clipped content inside glass
.ptm-timeline         horizontal strip wrapper
.ptm-solar            solar arc band (Row A)
.ptm-solar__marker    sunrise / sunset tick + label
.ptm-windows          window pills row (Row B)
.ptm-window           individual window pill
.ptm-window--good     green auspicious
.ptm-window--caution  red inauspicious
.ptm-window--neutral  gold neutral
.ptm-ticks            hour tick row (Row C)
.ptm-cursor           vertical cursor line assembly
.ptm-cursor__ring     pulsating ring
.ptm-cursor__dot      centre dot
.ptm-guidance         Critical Guidance bar
.ptm-guidance--auspicious
.ptm-guidance--inauspicious
.ptm-guidance--default
```

---

## 9. Interaction -- Vanilla JS (≤40 lines)

```js
const scroll   = document.querySelector('.ptm-scroll');
const timeline = document.querySelector('.ptm-timeline');
const cursor   = document.querySelector('.ptm-cursor');
const lens     = document.querySelector('.ptm-lens');

function updateFocus(clientX) {
  const rect = timeline.getBoundingClientRect();
  const pct  = Math.min(Math.max((clientX - rect.left) / rect.width, 0), 1) * 100;

  // Move cursor
  cursor.style.left = pct + '%';

  // Clamp lens X within canvas
  const lensPct = Math.min(Math.max(pct, 14), 76);
  lens.style.left = lensPct + '%';

  // Derive current state
  const state = getStateAtPct(pct, DEMO);
  renderLens(state);
  renderGuidance(state);
}

scroll.addEventListener('mousemove', e => updateFocus(e.clientX));
scroll.addEventListener('touchmove',  e => { e.preventDefault(); updateFocus(e.touches[0].clientX); }, { passive: false });

// Initialise at demo focus position
updateFocus(timeline.getBoundingClientRect().left + (DEMO.focusState.pct / 100) * timeline.getBoundingClientRect().width);
```

**`getStateAtPct(pct, data)`** -- your only non-trivial JS function:
1. Find which window (if any) contains `pct` → set `activeWindow`
2. Interpolate `timeLabel` from `data.hourTicks` array (linear between nearest ticks)
3. Return a `focusState` object in the same shape as `data.focusState`

This should be ~20 lines. No moment.js, no date math.

---

## 10. Animation Tokens

```css
@keyframes ptm-pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(0.92); opacity: 0.76; }
  50%       { transform: translate(-50%, -50%) scale(1.14); opacity: 1.00; }
}
@keyframes ptm-fade-in {
  from { opacity: 0; transform: scale(0.97); }
  to   { opacity: 1; transform: scale(1.00); }
}
```

Cursor ring: `animation: ptm-pulse 2.6s ease-in-out infinite`
Lens content on update: `animation: ptm-fade-in 0.16s ease`
Lens glass tint change: `transition: background-color 0.28s ease`

---

## 11. Responsive Breakpoints

| Viewport | Changes |
|---|---|
| ≥ 960px | Full layout. Lens 220px diameter, tracks cursor horizontally. |
| 768-959px | Lens shrinks to 180px. Window pill text truncates if `widthPct < 10`. Canvas height 420px. |
| ≤ 640px | Lens **fixed at bottom-centre** of canvas (`position:absolute; bottom:12px; left:50%; transform:translateX(-50%)`). Lens does not track cursor. Canvas height 340px. Rolled ends hidden. Show every 2nd hour tick. |
| ≤ 375px | Lens 150px. Handle hidden. Guidance text max 2 lines, `font-size: 0.82rem`. |

---

## 12. Acceptance Checklist

CC and TT verify against this checklist before closing PAN-TM-1:

**Visual:**
- [ ] Parchment scroll background -- warm cream/gold grain texture visible
- [ ] Rolled left and right ends on the scroll canvas
- [ ] Embroidery border -- double-line frame + lotus corner ornaments visible
- [ ] Background outside scroll matches `--panchang-bg: #f6efe1`

**Lens:**
- [ ] Lens is circular with thick bronze rim
- [ ] Gold angled handle visible at bottom-right of glass
- [ ] Top-left glass highlight (light source effect) visible
- [ ] Glass tint is green when over auspicious window, red over inauspicious
- [ ] Lens shows: time · window name · subline · time range · 4 limb grid
- [ ] "Open Sky" state shows when no window is active

**Timeline:**
- [ ] Solar arc band: warm gradient sunrise→noon→sunset
- [ ] Sunrise and sunset markers with time labels
- [ ] Auspicious windows GREEN, inauspicious windows RED
- [ ] Clock SVG icon visible in pills wide enough to show it
- [ ] Hour tick labels readable along bottom of strip

**Interaction:**
- [ ] Mouse/touch move updates cursor position and lens content
- [ ] Cursor pulse animation running
- [ ] Lens tracks cursor horizontally, clamped within canvas
- [ ] Clicking a window pill snaps cursor to that window midpoint
- [ ] Mobile: lens fixed at bottom-centre, not tracking

**Critical Guidance:**
- [ ] Bar text matches `guidance.text` from data
- [ ] Bar border-left colour matches guidance tier (green/red/gold)
- [ ] Icon prefix correct (✦ / ⚠ / ◉)

**Layout & Responsive:**
- [ ] No horizontal scroll at 1280px / 960px / 768px / 375px
- [ ] All `.ptm-*` CSS classes -- zero `.panchang-*` classes used or overridden

---

## 13. Post-Delivery: CC Integration Steps

After CD delivers `pan-tm1-cosmic-clock.html`:

1. **Create** `frontend/src/components/PanchangCosmicMapV2.jsx`
   - Copy the HTML structure → JSX
   - Replace `DEMO` with live data (props: `{ locationSlug, dayOffset }`)
   - Map existing `buildWindowSegments()`, `buildRowSegments()`, `hourFromClock()`,
     `solarIntensity()`, `formatHour()`, `pct()` functions from `PanchangCosmicMap.jsx`
     to produce the `data` object shape (§4)
   - Add `getStateAtPct()` function (from CD's JS, ~20 lines, keep as-is)

2. **Add CSS** -- paste all `.ptm-*` rules from CD's `<style>` block into
   `frontend/src/panchang.css` (after the existing `.panchang-cosmic-map__*` block)

3. **Swap import** in `frontend/src/pages/panchang/PanchangPage.jsx`:
   ```js
   // Before:
   import PanchangCosmicMap from '../../components/PanchangCosmicMap';
   // After:
   import PanchangCosmicMap from '../../components/PanchangCosmicMapV2';
   ```
   Component name in JSX stays `<PanchangCosmicMap ...>` -- no other changes in PanchangPage.

4. **Archive** (do not delete) old `.panchang-cosmic-map__*` CSS block until TT signs off

5. **Build verify:** `CI=false DISABLE_ESLINT_PLUGIN=true npx craco build` -- 0 errors required

6. **Bump ENGINE_VERSION** in `backend/panchang_router.py` if any backend changes are made
   (there are none in this commission -- frontend-only)

---

*Brief written 2026-06-03 · Revised 2026-06-04 · CC*
*Reference image: "The Cosmic Clock (January 28, 2026)" -- attached to CD thread*
