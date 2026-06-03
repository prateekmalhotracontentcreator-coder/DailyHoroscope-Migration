# Codex Commission · PAN-TM-1
## The Cosmic Clock -- Panchang Time Map Redesign
> Module: Panchang · Route: `/panchang/today` (embedded in PanchangPage)
> Issued: 2026-06-03
> Priority: 🟠 HIGH
> Type: CD Visual Redesign -- HTML + CSS prototype only. No backend changes.

---

## 1. Context & What Exists Today

The Panchang page at `https://www.everydayhoroscope.in/panchang/today` includes an interactive
Time Map component (`PanchangCosmicMap.jsx`). The current implementation is functional but visually
basic: flat coloured bars on a parchment-gradient frame, a small ellipse-shaped lens card, and no
strong identity.

The upgrade direction is locked: **The Cosmic Clock** -- a parchment scroll with embroidery border,
a large circular magnifying glass that acts as the focal lens, colour-coded time window bands with
clock imagery, and a dynamic "Critical Guidance" callout at the bottom.

A reference visual is included (see §7 below). Match the reference mood and layout precisely.

---

## 2. Deliverable

One self-contained HTML prototype file: `pan-tm1-cosmic-clock.html`

The HTML file must:
- Be completely standalone (no external CDN beyond Google Fonts, no build step)
- Contain all CSS inline in a `<style>` block
- Use hardcoded representative data (see §6) -- real data is wired by CC post-delivery
- Render correctly at 1280px, 960px, 768px, and 375px viewport widths
- Be interactive: hovering or clicking along the scroll timeline updates the magnifying lens

No React, no JavaScript framework. Vanilla JS only.

---

## 3. Visual Design Specification

### 3.1 Overall Layout

The component has three stacked regions:

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER ROW  [eyebrow | title "The Cosmic Clock" | date | loc]  │
├─────────────────────────────────────────────────────────────────┤
│  SCROLL CANVAS  (parchment + embroidery border)                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ [LENS]   TIMELINE STRIP with colour-coded window bands   │   │
│  │          hour tick marks along the bottom edge           │   │
│  └──────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  CRITICAL GUIDANCE BAR  ⚠ [computed tip text]                   │
└─────────────────────────────────────────────────────────────────┘
```

Total component height (desktop): ~500px. No vertical scroll inside the component.

---

### 3.2 Parchment Scroll Canvas

The scroll canvas is the central visual element. It must feel like an aged devotional scroll:

**Background texture:**
```css
background:
  url("data:image/svg+xml,<svg ...>") repeat,   /* fine noise texture via SVG */
  linear-gradient(180deg,
    #fdf6e3 0%,
    #f5e8c9 28%,
    #f0ddb5 50%,
    #f5e9c8 72%,
    #fdf6e3 100%
  );
```
Use `#fdf6e3 → #f0ddb5` warm cream-to-gold range. The texture SVG should be a subtle grain
(`<feTurbulence baseFrequency="0.65" numOctaves="3" type="fractalNoise"/>`).

**Rolled scroll edges:**
Add CSS `::before` and `::after` pseudo-elements at left and right edges of the canvas to
simulate rolled parchment ends. Each rolled edge is a vertical pill shape:
```
width: 28px, border-radius: 50%,
background: linear-gradient(90deg, #c4985a 0%, #e8c87e 40%, #c4985a 100%),
box-shadow: inset -3px 0 8px rgba(0,0,0,0.22), 4px 0 14px rgba(0,0,0,0.14)
```

**Embroidery border:**
Draw a continuous SVG border *inside* the canvas (inset ~14px), styled as an ornamental frame.
The border consists of:
- Thin double-line frame (inner: 1px rgba(160,110,40,0.35), outer: 1.5px rgba(130,85,20,0.22))
- Corner ornaments: 4-petal lotus at each corner, in saffron `#c67f20` at 48×48px
- Mid-edge ornaments (top & bottom centre): a small 6-pointed star / asterisk, same saffron
- The entire border SVG is `position:absolute; inset:0; pointer-events:none`

The border SVG viewBox should be `0 0 1000 400` (scale to parent), `preserveAspectRatio="none"`.
Draw it as a pure SVG `<path>` + `<use>` pattern -- no raster images.

**Background alignment with Temple App theme:**
The parchang CSS tokens are:
```
--panchang-bg:      #f6efe1
--panchang-saffron: #c67f20
--panchang-ink:     #2d2318
--panchang-muted:   #6e6251
```
The parchment scroll sits *inside* the page background which is already `#f6efe1`.
Use a slightly warmer, lighter tone for the scroll itself (`#fdf6e3`) so the scroll stands out.

---

### 3.3 The Magnifying Glass Lens

This is the centrepiece interaction. A large circular magnifying glass floats over the left portion
of the scroll and tracks the cursor X position along the timeline.

**Lens anatomy (4 layers, front to back):**
1. **Glass circle** -- `width: 220px; height: 220px; border-radius: 50%`
   - Inner fill: `radial-gradient(circle at 30% 28%, rgba(255,255,255,0.72) 0%, rgba(220,245,230,0.55) 45%, rgba(195,235,215,0.38) 100%)`
   - This should look like translucent glass with a light-source highlight at top-left.
2. **Handle** -- a tapered rectangle below the circle, angled ~−35deg, matching the reference image.
   - `width: 14px; height: 80px; border-radius: 7px`
   - `background: linear-gradient(180deg, #b8862e 0%, #8c6420 60%, #6b4b14 100%)`
   - Connected flush to the bottom-right of the glass circle, rotated −35deg from circle center
3. **Lens rim** -- `border: 10px solid rgba(169,128,76,0.88)` on the glass circle
   - `box-shadow: 0 18px 42px rgba(80,50,16,0.22), inset 0 2px 8px rgba(255,240,200,0.4), 0 0 0 3px rgba(255,236,195,0.5)`
   - The thick bronze rim matches the reference image
4. **Content inside the glass** -- the lens content region (circular clip, `overflow:hidden`).

**Lens content (what is shown inside the glass):**

Layout inside the lens (from top):
```
   ● CURRENT TIME  e.g. "12:33 PM"       ← 0.75rem, gold, letter-spaced
   ● WINDOW NAME   e.g. "Abhijit Muhurta" ← 1.3rem, serif, #2d2318, bold
     subline       e.g. "Safe Start Window"← 0.78rem, #5e7441, if quality=good
                        "Avoid"           ← 0.78rem, #9d3f1e, if quality=caution
   ● TIME RANGE    e.g. "11:51 AM - 12:12 PM" ← 0.82rem, medium weight
   ● DIVIDER LINE  1px rgba(150,100,40,0.2)
   ● 2×2 GRID: Tithi / Nakshatra / Yoga / Karana  ← active values at cursor time
```

If no window is active at the cursor position, show "Open Sky" as the window name with
"No restrictions active" as the subline.

The lens floats at a fixed vertical position (top ~100px from canvas top on desktop).
Horizontally it follows the cursor X, clamped so it never clips the canvas edge.
On mobile it is fixed-position at the bottom of the canvas.

---

### 3.4 Timeline Strip

The timeline strip runs horizontally across the scroll canvas, positioned vertically at ~55% of
canvas height (below the lens midpoint). It consists of three stacked rows:

**Row A -- Solar arc band** (height: 56px)
- A continuous horizontal band with a warm sunrise-to-peak-to-sunset colour arc:
  ```css
  background: linear-gradient(90deg,
    rgba(200,120,50,0.2) 0%,      /* pre-sunrise cool amber */
    rgba(255,200,80,0.55) 15%,    /* sunrise */
    rgba(255,238,160,0.78) 40%,   /* morning */
    rgba(255,255,200,0.9) 50%,    /* solar noon */
    rgba(255,210,120,0.72) 65%,   /* afternoon */
    rgba(220,140,60,0.55) 85%,    /* sunset */
    rgba(160,90,40,0.2) 100%      /* post-sunset */
  );
  border-radius: 999px;
  ```
- Sunrise and sunset markers: vertical tick + small sun-half icon (CSS, no raster) + time label
- The solar arc maps from `dayStart` to `dayEnd` (already computed in existing JS logic)

**Row B -- Window bands** (height: 44px)
Each timing window is a rounded pill overlaid on the strip at its proportional X position.
Width proportional to `(end − start) / (dayEnd − dayStart) * 100%`.

Colour rules (strict):
| Window label | Fill | Border | Text |
|---|---|---|---|
| Brahma Muhurta | `rgba(94,116,65,0.82)` | `#5e7441` | `#fff` |
| Abhijit Muhurta | `rgba(64,130,75,0.88)` | `#3d7a46` | `#fff` |
| Vijaya Muhurta | `rgba(82,118,68,0.82)` | `#527244` | `#fff` |
| Amrit Kalam | `rgba(60,120,90,0.82)` | `#3c7856` | `#fff` |
| Rahu Kaal | `rgba(179,62,42,0.85)` | `#b33e2a` | `#fff` |
| Yamaganda | `rgba(160,70,38,0.82)` | `#a04626` | `#fff` |
| Gulika Kaal | `rgba(175,80,45,0.8)` | `#af502d` | `#fff` |
| Dur Muhurta | `rgba(168,74,40,0.80)` | `#a84a28` | `#fff` |
| Varjyam | `rgba(155,68,45,0.78)` | `#9b442d` | `#fff` |
| *default/unknown* | `rgba(198,127,32,0.55)` | `#c67f20` | `#fff` |

Each pill shows:
- Window name (truncated if <60px wide, full name if ≥60px)
- A small clock face SVG icon (16×16) at the left edge of the pill (only if pill width ≥52px)

The clock SVG is a simple circle with two hands:
```svg
<svg viewBox="0 0 16 16" fill="none">
  <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.4"/>
  <line x1="8" y1="8" x2="8" y2="3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="8" y1="8" x2="11" y2="9.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
</svg>
```

**Row C -- Hour tick marks** (height: 20px below the window strip)
Fine vertical ticks every whole hour, with hour label (e.g. "6", "7", "8") in
`rgba(78,58,31,0.7)` at 0.78rem. The first and last visible ticks show AM/PM suffixed times.

---

### 3.5 Live Cursor

A vertical line + pulsating ring tracks mouse/touch position across the strip.

- Vertical line: `2px wide, linear-gradient(180deg, transparent 0%, rgba(137,85,28,0.6) 40%, rgba(235,198,97,0.9) 60%, transparent 100%)`
- Ring at midpoint of window band: `width:28px; height:28px; border-radius:50%; border: 2px solid rgba(255,234,158,0.95)`
  - Pulse animation: scale 0.92→1.12 over 2.6s ease-in-out, opacity 0.78→1.0
- Centre dot: `width:10px; height:10px; background: radial-gradient(circle, #fff7b5 0%, #f2ab3e 72%)`

The cursor starts at the Abhijit Muhurta midpoint on load, or at the current real time if within
the visible range.

---

### 3.6 Critical Guidance Bar

Below the scroll canvas, a full-width bar shows a contextual tip computed from the data.

**Logic (priority order):**
1. If current time is inside an auspicious window → "✦ Golden Window Active -- [window name] runs until [end time]. Act now."
2. If next auspicious window is <60 min away → "⚠ Critical: [window name] opens at [start time] -- only [N] minutes away."
3. If current time is inside an inauspicious window → "⚠ [window name] is active until [end time]. Avoid new starts."
4. Default → "Today's strongest window: [most important auspicious window name] · [start]-[end]."

**Bar styling:**
```css
/* Case 1/2: upcoming/active auspicious */
background: linear-gradient(135deg, rgba(64,115,68,0.12), rgba(94,140,78,0.08));
border-left: 4px solid #4d7344;
color: #2d4a26;

/* Case 3: active inauspicious */
background: linear-gradient(135deg, rgba(160,60,38,0.11), rgba(190,80,48,0.07));
border-left: 4px solid #b33e2a;
color: #7a2810;

/* Case 4: default */
background: rgba(198,127,32,0.09);
border-left: 4px solid #c67f20;
color: #5a3a10;
```

The bar prefix icon is a `⚠` (warning triangle) for inauspicious, `✦` (asterism) for auspicious,
and `◉` (circled dot) for default. Use Unicode -- no separate SVG needed here.

Font: `font-size: 0.94rem; font-weight: 700; letter-spacing: 0.02em; line-height: 1.4`

---

### 3.7 Header

Left-aligned header above the scroll canvas:

```
THE COSMIC CLOCK               [eyebrow / uppercase saffron, 0.75rem, tracking 0.22em]
New Delhi -- 3 June 2026        [h2, Playfair Display / Georgia serif, 2.2rem]
Tap the scroll to inspect any moment of the day.  [subtext, muted, 0.88rem]
```

If no location data yet, the h2 reads "The Living Panchang".

---

## 4. Typography

| Element | Font | Size | Weight | Colour |
|---|---|---|---|---|
| Eyebrow | system-ui | 0.75rem | 700 | `#8d5614` |
| H2 title | Playfair Display (or Georgia fallback) | clamp(1.8rem,3.5vw,2.8rem) | 400 | `#2d2318` |
| Subtext | system-ui | 0.88rem | 400 | `#6e6251` |
| Lens time | system-ui | 0.75rem | 800 | `#5b5f2d` |
| Lens window name | Playfair Display | 1.3rem | 700 | `#2d2318` |
| Lens grid labels | system-ui | 0.7rem | 700, uppercase | `#5b6a3f` |
| Lens grid values | system-ui | 0.96rem | 700 | `#2d3522` |
| Window pill text | system-ui | 0.78rem | 700 | `#fff` |
| Hour ticks | system-ui | 0.78rem | 400 | `rgba(78,58,31,0.7)` |
| Critical guidance | system-ui | 0.94rem | 700 | *varies by case* |

Use `@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap')`.

---

## 5. Interaction Behaviour

| Event | Behaviour |
|---|---|
| `mousemove` on scroll canvas | Cursor tracks X. Lens content updates to show data at that hour. Guidance bar updates. |
| `touchmove` on scroll canvas | Same as mousemove, using touch.clientX |
| `click` / `tap` on a window pill | Cursor snaps to that window's midpoint. Lens focuses that window. |
| Page load | Cursor initialises at Abhijit Muhurta midpoint (or current real time if within visible range) |
| Resize | Layout reflows; lens stays clamped within canvas. On ≤640px lens moves to bottom-fixed. |

---

## 6. Hardcoded Demo Data (for prototype)

Use New Delhi, June 3 2026 as the representative dataset:

```js
const DEMO = {
  location: "New Delhi, India",
  date: "Tuesday, June 3, 2026",
  sunrise: "05:23",
  sunset: "19:14",
  dayStart: 4,      // hour
  dayEnd: 20,       // hour
  panchang: {
    tithi:     { name: "Ashtami",    index: 7,  end: "2026-06-03T19:42:00+05:30" },
    nakshatra: { name: "Shravana",   index: 21, end: "2026-06-03T22:11:00+05:30" },
    yoga:      { name: "Siddhi",     index: 16, end: "2026-06-04T00:34:00+05:30" },
    karana:    { name: "Vanija",     index: 6,  end: "2026-06-03T08:15:00+05:30" },
  },
  windows: [
    { label: "Brahma Muhurta",  start: "04:47", end: "05:35", quality: "good"    },
    { label: "Rahu Kaal",       start: "07:38", end: "09:17", quality: "caution" },
    { label: "Yamaganda",       start: "10:56", end: "12:35", quality: "caution" },
    { label: "Abhijit Muhurta", start: "11:51", end: "12:43", quality: "good"    },
    { label: "Gulika Kaal",     start: "14:13", end: "15:52", quality: "caution" },
    { label: "Vijaya Muhurta",  start: "14:30", end: "15:19", quality: "good"    },
    { label: "Dur Muhurta",     start: "15:16", end: "16:05", quality: "caution" },
    { label: "Amrit Kalam",     start: "17:02", end: "18:42", quality: "good"    },
  ],
};
```

The demo should simulate "current time = 12:33 PM" (between Yamaganda end and Abhijit mid)
so that the Critical Guidance bar shows: "⚠ Critical: Abhijit Muhurta opens at 11:51 AM --
the Safe Victory Window is short today. Act with precision between 11:51 AM and 12:43 PM."
(This matches the reference image tone exactly.)

---

## 7. Reference Image Analysis

The reference image attached to the commission brief establishes the following non-negotiable
visual decisions:

**Non-negotiable elements -- must match:**
1. **Parchment scroll** with rolled left/right ends -- the entire timeline sits on this scroll
2. **Circular magnifying glass with bronze/gold handle** -- large, left-leaning, with the
   glass centred on the most important window (Abhijit green section in the reference)
3. **Green window band** for Abhijit/auspicious windows, clearly labelled "Safe Start Window"
   inside the pill (the label inside the pill is the window name, and the sub-label is the
   quality qualifier -- "Safe Start" for good quality, clock icon, exact time range)
4. **Red window band** for Rahu Kaal / inauspicious, labelled "Avoid" with clock + time range
5. **Embroidery border** around the entire scroll -- lotus corners, thin double-line frame
6. **The Critical Guidance text** at the bottom is bold, with `⚠ CRITICAL GUIDANCE:` prefix
7. **Background of the whole component** (outside the scroll) uses the cream/gold tone matching
   the app's existing `--panchang-bg: #f6efe1` -- the scroll appears warmer than the background
8. **Clock faces** visible in the window pills (use the inline SVG from §3.4)
9. **Time tick marks** along the scroll bottom edge are readable and spaced by whole hours
10. The lens glass itself should appear **slightly green-tinted** (as in the reference) due to
    the auspicious window being focused -- when cursor is over a red/inauspicious window,
    the glass tint shifts to red (subtle: opacity 0.12 overlay inside the glass circle)

**Permitted differences from reference (adapt for web responsiveness):**
- Reference shows a single focused moment; the web version is interactive (cursor moves)
- Reference is a static image; the web version animates the cursor pulse
- Reference decorative stars/constellation marks in background are optional (add if time permits)

---

## 8. CSS Architecture

All CSS classes must use the prefix `ptm-` to avoid collisions with the existing `panchang.css`.

The existing `panchang.css` file uses `.panchang-cosmic-map__*` classes.
**Do NOT use or override any existing `.panchang-*` classes.**
The new component CSS is fully isolated under `.ptm-*`.

Key class names to establish:
```
.ptm-shell           /* outer wrapper: full width, relative positioning */
.ptm-header          /* header row */
.ptm-scroll          /* the parchment scroll canvas */
.ptm-scroll__border  /* SVG embroidery border overlay */
.ptm-lens            /* magnifying glass assembly */
.ptm-lens__glass     /* circular glass element */
.ptm-lens__handle    /* gold handle below glass */
.ptm-lens__content   /* clipped content inside glass */
.ptm-timeline        /* horizontal strip container */
.ptm-solar           /* solar arc band */
.ptm-windows         /* window pills container */
.ptm-window          /* individual window pill */
.ptm-window--good    /* green auspicious */
.ptm-window--caution /* red inauspicious */
.ptm-ticks           /* hour tick row */
.ptm-cursor          /* vertical cursor line + ring */
.ptm-guidance        /* Critical Guidance bar */
.ptm-guidance--auspicious
.ptm-guidance--inauspicious
.ptm-guidance--default
```

---

## 9. Responsive Breakpoints

| Breakpoint | Behaviour |
|---|---|
| ≥960px | Full layout as specified above. Lens 220px circle, left-floating, tracks cursor. |
| 768px - 959px | Scroll canvas height 400px. Lens 180px circle, same behaviour. Window pills truncate to initials if <48px wide. |
| ≤640px | Scroll canvas height 320px (scroll width = 100vw - 28px padding). Lens **fixed at bottom-centre** of canvas (not tracking -- position fixed to bottom ~12px, centred). Window pills: hide label if width <40px, show only colour. Ticks: show every 2 hours. |
| ≤375px | Lens shrinks to 140px. Handle hidden. Critical guidance text wraps to 2 lines max. |

---

## 10. Animation Tokens

```css
@keyframes ptm-pulse {
  0%, 100% { transform: scale(0.92); opacity: 0.78; }
  50%       { transform: scale(1.12); opacity: 1.00; }
}
@keyframes ptm-glow-in {
  from { opacity: 0; transform: scale(0.96); }
  to   { opacity: 1; transform: scale(1.00); }
}
@keyframes ptm-lens-tint {
  /* for the colour shift when cursor crosses window boundaries */
  from { background-color: var(--ptm-tint-from); }
  to   { background-color: var(--ptm-tint-to);   }
}
```

The cursor pulse uses `ptm-pulse`, 2.6s, ease-in-out, infinite.
The lens content fades in with `ptm-glow-in` (0.18s) on every cursor update.
The lens glass tint transitions with `transition: background 0.28s ease` (not keyframes).

---

## 11. Backend Contract (Reference Only -- No Changes Required)

The existing `/api/panchang/daily` endpoint already returns all fields needed:

```json
{
  "date": "2026-06-03",
  "location": { "label": "New Delhi, India", "timezone": "Asia/Kolkata" },
  "summary": { "sunrise": "05:23", "sunset": "19:14", ... },
  "panchang": {
    "tithi":     { "name": "Ashtami",  "index": 7,  "end": "..." },
    "nakshatra": { "name": "Shravana", "index": 21, "end": "..." },
    "yoga":      { "name": "Siddhi",   "index": 16, "end": "..." },
    "karana":    { "name": "Vanija",   "index": 6,  "end": "..." }
  },
  "day_quality_windows": [
    { "label": "Brahma Muhurta", "start": "...", "end": "...", "quality": "good" },
    { "label": "Rahu Kaal",      "start": "...", "end": "...", "quality": "caution" },
    ...
  ],
  "special_timing_windows": [
    { "label": "Amrit Kalam", "start": "...", "end": "...", "quality": "good" },
    ...
  ]
}
```

CC will replace the hardcoded demo data with live API calls when integrating.

---

## 12. Integration Notes (for CC post-delivery)

After CD delivers `pan-tm1-cosmic-clock.html`:

1. Convert to `PanchangCosmicMapV2.jsx` -- all CSS moved to `.ptm-*` classes in `panchang.css`
2. The `PanchangCosmicMapV2` component receives the same props as the current component:
   `{ locationSlug, dayOffset }` -- no prop changes needed
3. Replace the `<PanchangCosmicMap ...>` import and usage in `PanchangPage.jsx` with
   `<PanchangCosmicMapV2 ...>` -- single line change
4. The old `.panchang-cosmic-map__*` CSS block in `panchang.css` may be archived but not deleted
   until TT signs off on production appearance
5. Run `CI=false DISABLE_ESLINT_PLUGIN=true npx craco build` to verify 0 errors before deploy

---

## 13. Acceptance Checklist

TT to verify against this checklist before closing PAN-TM-1:

- [ ] Parchment scroll visible with rolled left/right ends
- [ ] Embroidery border (lotus corners + double-line frame) visible inside scroll
- [ ] Magnifying glass lens: circular, bronze rim, gold handle, glass highlight at top-left
- [ ] Lens content shows correct time, window name, quality label, and 4 panchang limb values
- [ ] Auspicious windows appear GREEN (Brahma, Abhijit, Vijaya, Amrit Kalam)
- [ ] Inauspicious windows appear RED (Rahu Kaal, Yamaganda, Gulika, Dur Muhurta, Varjyam)
- [ ] Clock icon visible inside each pill wide enough to show it
- [ ] Hour tick marks readable along bottom of scroll
- [ ] Cursor pulse animation running (ring breathing)
- [ ] Moving cursor updates lens content
- [ ] Critical Guidance bar shows correct contextual tip
- [ ] Critical Guidance bar colour matches guidance type (green/red/gold)
- [ ] Responsive: 1280px / 960px / 768px / 375px all render cleanly
- [ ] Mobile lens drops to bottom-fixed position at ≤640px
- [ ] No horizontal scroll on any viewport
- [ ] CSS classes all prefixed `.ptm-*` (no conflicts with existing `.panchang-*`)

---

## 14. Open Points / Decisions

| # | Question | Default if not actioned |
|---|---|---|
| PAN-TM-OP-1 | Should Choghadiya windows (Amrit, Labh, Shubh etc.) also be shown in the strip? | No -- only the 8 windows listed in §6 demo data |
| PAN-TM-OP-2 | Should the component title "The Cosmic Clock" appear in the page `<title>` tag? | No -- SEO title is managed separately by PanchangPage.jsx |
| PAN-TM-OP-3 | Constellation / star background elements visible in reference image top-right area -- include? | Optional ornamental detail -- include if time permits, skip if it adds >20 lines of SVG |

---

## 15. Tracker Reference

- Module TRACKER: `Codex_Deliveries/Panchang/TRACKER.md`
- Commission added to open points as **PAN-OP-4** (issue this brief to CD)
- On delivery: add PAN-TM-1 row to commission table, update status to DELIVERED
- On CC integration: update status to INTEGRATED, add version history row to TRACKER

---

*Brief written 2026-06-03 · CC*
