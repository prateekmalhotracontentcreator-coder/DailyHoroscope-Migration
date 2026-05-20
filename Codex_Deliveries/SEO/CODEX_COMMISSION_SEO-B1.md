# Commission Brief: SEO-B1 -- Tomorrow / Weekly / Monthly Per-Sign Horoscope Pages

**Commission ID:** SEO-B1  
**Track:** B -- Codex Content Pages  
**Priority:** HIGHEST in Tier 1  
**Date:** 2026-05-20  
**Status:** READY TO ISSUE  

---

## What to Build

36 new public SEO pages -- 12 zodiac signs × 3 time periods:

| Period | Route pattern | Example |
|---|---|---|
| Tomorrow | `/horoscope/:sign/tomorrow` | `/horoscope/aries/tomorrow` |
| Weekly | `/horoscope/:sign/weekly` | `/horoscope/aries/weekly` |
| Monthly | `/horoscope/:sign/monthly` | `/horoscope/aries/monthly` |

All 12 signs: `aries`, `taurus`, `gemini`, `cancer`, `leo`, `virgo`, `libra`, `scorpio`, `sagittarius`, `capricorn`, `aquarius`, `pisces`

---

## Files to Create

### Frontend
- `frontend/src/pages/horoscope/HoroscopeSignPage.jsx`  
  (Single component -- handles all 3 time periods via `period` prop / route param)

### Backend
- No new file needed -- add one route to `backend/server.py` (see Backend Changes below)

---

## Backend Changes Required

### Existing endpoint
```
GET /api/horoscope/{sign}/{type}
```
Currently accepts `type`: `daily` | `weekly` | `monthly`

### New type to add
Add `tomorrow` as a valid type in `HoroscopeType` enum in `server.py`.

In `get_prediction_date()`:
```python
elif horoscope_type == "tomorrow":
    return (today + timedelta(days=1)).isoformat()
```

In `generate_horoscope_with_llm()`, add a `tomorrow_prompt`:
```python
tomorrow_prompt = ("You are a Vedic astrologer specialising in Jyotish. Generate a tomorrow's horoscope for " + sign + ".\n\nCRITICAL FORMATTING RULES:\n1. Start with one sentence of tomorrow's overall energy.\n2. Output EXACTLY these 4 sections with EXACTLY these headings on their own line:\n   Love & Relationships:\n   Career & Finances:\n   Health & Wellness:\n   Lucky Elements:\n3. Under Lucky Elements include: Lucky Number: [number], Lucky Colour: [colour], Lucky Time: [time]\n4. NO markdown (no **, no ##, no ---)\n5. Each section: 2-3 sentences. Total 120-150 words.\n6. Begin with: \"" + sign_dash + "\"")
```

No other backend changes needed. The existing caching logic (find_one → insert_one) works for `tomorrow` automatically.

---

## Component Spec: `HoroscopeSignPage.jsx`

### Route wiring (App.js additions)
```jsx
import { HoroscopeSignPage } from './pages/horoscope/HoroscopeSignPage';

// Add inside <Routes> after existing horoscope routes:
<Route path="/horoscope/:sign/tomorrow" element={<HoroscopeSignPage period="tomorrow" />} />
<Route path="/horoscope/:sign/weekly"   element={<HoroscopeSignPage period="weekly" />} />
<Route path="/horoscope/:sign/monthly"  element={<HoroscopeSignPage period="monthly" />} />
```

### Component behaviour
1. Read `:sign` from `useParams()`
2. Read `period` from props (`"tomorrow"` | `"weekly"` | `"monthly"`)
3. Call `POST /api/horoscope/generate` with `{ sign, type: period }` -- existing endpoint handles generate-or-fetch
4. Display the horoscope content with sign branding

### Data flow
```
Page load → POST /api/horoscope/generate { sign, type: period }
         → Backend checks cache (today's prediction_date) → returns cached or generates new
         → Page renders content
```

### UI Layout
```
[Sign hero banner -- sign glyph + sign name + dates + period badge]
[Horoscope content card -- styled text in 4 sections]
[Sign navigation grid -- all 12 signs × current period links]
[Upsell CTA -- "Get your personalised Birth Chart reading"]
```

### Sign metadata (hardcode in component)
```javascript
const SIGNS = {
  aries:       { name: 'Aries',       dates: 'Mar 21 - Apr 19', element: 'Fire',  glyph: '♈' },
  taurus:      { name: 'Taurus',      dates: 'Apr 20 - May 20', element: 'Earth', glyph: '♉' },
  gemini:      { name: 'Gemini',      dates: 'May 21 - Jun 20', element: 'Air',   glyph: '♊' },
  cancer:      { name: 'Cancer',      dates: 'Jun 21 - Jul 22', element: 'Water', glyph: '♋' },
  leo:         { name: 'Leo',         dates: 'Jul 23 - Aug 22', element: 'Fire',  glyph: '♌' },
  virgo:       { name: 'Virgo',       dates: 'Aug 23 - Sep 22', element: 'Earth', glyph: '♍' },
  libra:       { name: 'Libra',       dates: 'Sep 23 - Oct 22', element: 'Air',   glyph: '♎' },
  scorpio:     { name: 'Scorpio',     dates: 'Oct 23 - Nov 21', element: 'Water', glyph: '♏' },
  sagittarius: { name: 'Sagittarius', dates: 'Nov 22 - Dec 21', element: 'Fire',  glyph: '♐' },
  capricorn:   { name: 'Capricorn',   dates: 'Dec 22 - Jan 19', element: 'Earth', glyph: '♑' },
  aquarius:    { name: 'Aquarius',    dates: 'Jan 20 - Feb 18', element: 'Air',   glyph: '♒' },
  pisces:      { name: 'Pisces',      dates: 'Feb 19 - Mar 20', element: 'Water', glyph: '♓' },
};

const ELEMENT_COLORS = {
  Fire:  'from-orange-500/20 to-red-500/10',
  Earth: 'from-green-600/20 to-emerald-500/10',
  Air:   'from-sky-400/20 to-blue-400/10',
  Water: 'from-blue-600/20 to-indigo-500/10',
};
```

---

## SEO Requirements

### Meta title (per page)
| Period | Title pattern |
|---|---|
| Tomorrow | `{Sign} Horoscope Tomorrow -- Vedic Prediction \| EverydayHoroscope` |
| Weekly | `{Sign} Weekly Horoscope -- This Week's Vedic Forecast \| EverydayHoroscope` |
| Monthly | `{Sign} Monthly Horoscope -- {Month} {Year} Vedic Forecast \| EverydayHoroscope` |

Example: `Aries Horoscope Tomorrow -- Vedic Prediction | EverydayHoroscope`

### Meta description
- Tomorrow: `Get your Aries horoscope for tomorrow. Vedic astrology prediction for love, career, health and lucky elements.`
- Weekly: `Aries weekly horoscope -- your 7-day Vedic forecast for love, career, and wellness. Updated every week.`
- Monthly: `Aries horoscope for {Month} {Year} -- full monthly Vedic forecast covering love, career, health, and auspicious dates.`

### JSON-LD schema
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{Sign} {Period} Horoscope",
  "datePublished": "{today ISO}",
  "dateModified": "{today ISO}",
  "author": { "@type": "Organization", "name": "EverydayHoroscope" },
  "publisher": { "@type": "Organization", "name": "EverydayHoroscope", "url": "https://www.everydayhoroscope.in" }
}
```

### Canonical
Each page canonical = its own URL (e.g. `https://www.everydayhoroscope.in/horoscope/aries/tomorrow`)

### Internal links
- Each page must include a **sign navigation grid** -- all 12 signs × same period (e.g. all 12 "tomorrow" links from the Aries tomorrow page)
- Period switcher tabs: `Tomorrow | Weekly | Monthly` at top of page

---

## Upsell Hook

Below the horoscope content, add a CTA card:
```
"Want a reading that's personalised to your exact birth chart?"
[Button] → Unlock Your Birth Chart -- [/birth-chart]
```

Secondary CTA (below sign grid):
```
"Explore your full {period} horoscope across all areas of life"
[Button] → View Full {Period} Horoscope → [/horoscope/{period}]
```

---

## Visual Spec

- Use existing `GlassCard` pattern: `rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`
- Sign glyph in element-colored circle (same as `HoroscopeShareCard` -- `ELEMENT_COLORS` map above)
- Period badge: pill with `bg-gold/15 text-gold border border-gold/30`
- Section headings (`Love & Relationships:` etc.) in `text-gold font-semibold`
- Body text in `text-foreground`
- Sign navigation grid: 4-column grid of sign pills, current sign highlighted with `bg-gold/20`
- No custom CSS files -- Tailwind only, using existing CSS variable tokens

---

## ⚠️ Critical Notes

1. **Do NOT add dasha/astronomical calculation functions** -- horoscope content comes from existing `/api/horoscope/generate` endpoint only
2. **All astrological data** from existing backend -- no hardcoded predictions
3. **Smart quote fix** -- after generating, run the smart-quote fix script on the new `.jsx` file before handing over
4. **Lazy load** -- this component can be lazy-loaded (not in the eager bundle)
5. **Premium gate** -- these pages are **public** (no PremiumRoute wrapper) -- they are SEO discovery pages that upsell to premium

---

## Sitemap additions needed (CC task after Codex delivers)

Add all 36 routes to `frontend/public/sitemap.xml` -- Claude Code handles this after integration.

---

## Acceptance Criteria

- [ ] 36 routes all load without 404
- [ ] Each page has unique `<title>` and `<meta name="description">`
- [ ] JSON-LD present on each page
- [ ] Sign navigation grid shows all 12 signs with correct links
- [ ] Period switcher works (Tomorrow / Weekly / Monthly)
- [ ] `tomorrow` type works in backend -- generates and caches correctly
- [ ] No console errors
- [ ] Build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
