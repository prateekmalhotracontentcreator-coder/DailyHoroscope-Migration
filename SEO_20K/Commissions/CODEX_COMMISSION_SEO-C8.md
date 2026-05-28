# Commission Brief: SEO-C8 -- Love Calculator

**Commission ID:** SEO-C8  
**Track:** C -- Codex Feature Builds  
**Priority:** Tier 3 -- Phase 8 | Benchmark: $91K/mo traffic  
**Date:** 2026-05-20  
**Status:** READY TO ISSUE  

---

## What to Build

A viral love compatibility calculator -- the highest-volume astrology tool on the internet.

| Route | What |
|---|---|
| `/love-calculator` | Two names / two DOBs → compatibility score + reading |

Mass appeal, high shareability, strong upsell path to premium relationship reports.

---

## Files to Create

### Frontend
- `frontend/src/pages/calculators/LoveCalculatorPage.jsx`

### Backend
Reuse existing endpoints. One new lightweight endpoint for the combined score (details below).

---

## Route Wiring (App.js)

```jsx
import { LoveCalculatorPage } from './pages/calculators/LoveCalculatorPage';

<Route path="/love-calculator" element={<LoveCalculatorPage />} />
```

---

## Two Calculation Modes

The calculator offers two modes -- user picks which to use:

| Mode | Inputs | Method |
|---|---|---|
| **Name Mode** | Two names | Chaldean name number compatibility (same as SEO-C3) |
| **Birth Date Mode** | Two DOBs | Life Path number compatibility via numerology |

### Backend endpoint

```
POST /api/love-calculator
Body: {
  "mode": "name" | "birthdate",
  "name1": "...",           // name mode
  "name2": "...",           // name mode
  "dob1": "YYYY-MM-DD",    // birthdate mode
  "dob2": "YYYY-MM-DD"     // birthdate mode
}
Returns: {
  "score": 82,
  "band": "high",
  "label": "Soulmate Connection",
  "description": "...",
  "elements": {
    "mind": 75,
    "heart": 90,
    "energy": 80
  }
}
```

**Add to `numerology_router.py`** -- reuses `CHALDEAN_MAP` and Life Path calculation already present. **No LLM call.**

### Scoring bands + labels

| Score | Band | Label |
|---|---|---|
| 90-100 | cosmic | "Cosmic Match" |
| 75-89 | high | "Soulmate Connection" |
| 60-74 | good | "Strong Compatibility" |
| 45-59 | moderate | "Balanced Pair" |
| 30-44 | challenging | "Growth Relationship" |
| <30 | low | "Opposites Attract" |

---

## UI Layout

```
[Page header: "Love Calculator ❤️"]
[Subtitle: "Discover your cosmic compatibility -- powered by Vedic numerology"]

[Mode toggle]
  └── [By Name] [By Birth Date]  ← pill toggle, gold active state

[Input card -- GlassCard]
  BY NAME MODE:
  ├── Name 1 input (Your name)
  ├── Heart divider (❤️)
  ├── Name 2 input (Their name)
  └── [Calculate Love Score] button

  BY BIRTH DATE MODE:
  ├── Your date of birth (date picker)
  ├── Heart divider
  ├── Their date of birth (date picker)
  └── [Calculate Love Score] button

[Result card -- full-width, dramatic -- appears after calculate]
  ├── Large score gauge: animated fill to score (CSS, no library)
  ├── Score number: "82%" in gold, large Cinzel font
  ├── Label: "Soulmate Connection" 
  ├── 3 sub-scores as mini bars:
  │     ├── Mind compatibility: 75%
  │     ├── Heart compatibility: 90%
  │     └── Energy compatibility: 80%
  ├── 3-sentence description
  ├── [💌 Share your score] → copy shareable URL
  └── [Calculate again] → reset

[Upsell section -- below result]
  ├── "Want the full picture?"
  ├── 3 report cards:
  │     ├── Relationship Numerology Report → /numerology
  │     ├── Kundali Milan (Birth Chart matching) → /kundali-milan
  │     └── Love Weather Report → /love-weather-report
  └── "Premium members get unlimited love readings + detailed compatibility reports"

[How it works -- info card]
  └── "Vedic numerology assigns each name/birthdate a cosmic number. The compatibility
       between two numbers reveals relationship dynamics across mind, heart, and energy."

[FAQ accordion]
  ├── "Is the love calculator accurate?"
  ├── "What's the difference between name and birth date mode?"
  ├── "What does a high compatibility score mean?"
  └── "How is this different from Kundali matching?"
```

---

## Shareability (critical for virality)

- **Shareable URL:** `/love-calculator?m=name&n1=Priya&n2=Arjun` or `?m=dob&d1=1990-01-15&d2=1988-07-22`
- On page load with URL params → auto-calculate and show result
- Share button copies URL with params to clipboard
- **Open Graph for share:** When URL params present, dynamically set OG title to `"Priya + Arjun = 82% Compatible 💕 | EverydayHoroscope"` (via `react-helmet` or `SEO.jsx` component)

---

## SEO Requirements

- **Title:** `Love Calculator -- Check Your Compatibility | EverydayHoroscope`
- **Description:** `Find your love compatibility score instantly. Enter two names or birth dates to calculate your cosmic connection -- powered by Vedic numerology.`
- **JSON-LD:**
```json
{
  "@type": "WebApplication",
  "applicationCategory": "AstrologyApplication",
  "name": "Love Calculator",
  "description": "Vedic numerology love compatibility calculator"
}
```
- **FAQ schema** -- required (covers "how accurate is love calculator" queries)

---

## Visual Spec

- Score gauge: circular progress ring, gold fill, animated on result appearance (CSS `stroke-dashoffset`, no JS library)
- Score number: `text-6xl font-cinzel text-gold`
- Score label: `text-2xl font-playfair italic text-foreground`
- Sub-score bars: thin `h-2` bars, gold fill, grey background, width = score%
- Mode toggle: gold pill on active, `border border-gold/30` on inactive
- Result card: GlassCard with stronger gold border `border-gold/40 bg-gold/[0.06]`
- Upsell report cards: 3-column grid of smaller GlassCards with gold CTA buttons
- Heart divider: `text-gold text-2xl` centred between inputs
- No custom CSS -- Tailwind only

---

## ⚠️ Critical Notes

1. **No LLM** -- all calculation is pure numerology math. Fast, free, unlimited uses.
2. **Reuse existing numerology functions** -- `CHALDEAN_MAP` in `numerology_router.py`, Life Path calculation already exists in the same file
3. **URL params for sharing** -- this is the primary viral distribution mechanism. Must work correctly.
4. **Dynamic OG tag** -- when URL params are present, update `og:title` to include names/score. Use existing `SEO.jsx` component.
5. **No login required** -- this is a fully public tool
6. **Smart quote fix** on `LoveCalculatorPage.jsx`
7. **Lazy load** -- can be lazy-loaded

---

## Acceptance Criteria

- [ ] `/love-calculator` loads, both modes work
- [ ] Name mode returns score using Chaldean system
- [ ] Birth date mode returns score using Life Path numbers
- [ ] Score, label, sub-scores displayed correctly
- [ ] Shareable URL encodes inputs; page auto-calculates on load with params
- [ ] Share button copies correct URL
- [ ] Dynamic OG title when URL params present
- [ ] FAQ schema present
- [ ] No console errors
- [ ] Build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
