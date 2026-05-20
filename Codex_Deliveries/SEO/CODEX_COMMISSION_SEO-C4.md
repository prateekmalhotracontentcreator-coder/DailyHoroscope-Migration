# Commission Brief: SEO-C4 -- Ekadashi / Amavasya / Purnima Hub Pages

**Commission ID:** SEO-C4  
**Track:** C -- Codex Feature Builds  
**Priority:** Tier 2 -- Phase 5  
**Date:** 2026-05-20  
**Status:** READY TO ISSUE  

---

## What to Build

Three devotional date hub pages -- all pull from the existing Panchang engine:

| Page | Route | What it shows |
|---|---|---|
| Ekadashi | `/ekadashi` | Next Ekadashi date + Panchang + fasting rules |
| Amavasya | `/amavasya` | Next Amavasya date + Panchang + rituals |
| Purnima | `/purnima` | Next Purnima date + Panchang + significance |

High-devotion India SEO traffic. Monthly searches are recurring -- these pages stay relevant year-round.

---

## Files to Create

### Frontend
- `frontend/src/pages/devotional/DevotionalDatePage.jsx`  
  (Single component -- parameterised by `type` prop: `"ekadashi"` | `"amavasya"` | `"purnima"`)

### Backend
- No new files -- all data from `panchang_router.py` (see backend calls below)

---

## Route Wiring (App.js additions)

```jsx
import { DevotionalDatePage } from './pages/devotional/DevotionalDatePage';

// Add inside <Routes>:
<Route path="/ekadashi" element={<DevotionalDatePage type="ekadashi" />} />
<Route path="/amavasya" element={<DevotionalDatePage type="amavasya" />} />
<Route path="/purnima"  element={<DevotionalDatePage type="purnima"  />} />
```

---

## Backend Data Sources

### Finding the next date for each Tithi

**Ekadashi** = Tithi 11 (Shukla Paksha) and Tithi 26 (Krishna Paksha)  
**Amavasya** = Tithi 30 (new moon / Amavasya)  
**Purnima** = Tithi 15 (full moon / Purnima)

Use the festival list endpoint to find upcoming dates:
```
GET /api/panchang/festivals?year={YYYY}
```
Filter by observance name containing "Ekadashi", "Amavasya", or "Purnima". Take the next upcoming date (first one after today).

### Panchang for the next occurrence
```
GET /api/panchang/daily?date={next_date}&location_slug=new-delhi
```
Returns full Panchang for that day including Tithi, Nakshatra, Yoga, timing windows.

**All data from existing `panchang_router.py` -- no new backend calculations needed.**

---

## Devotional Content (hardcode per type)

```javascript
const DEVOTIONAL_DATA = {
  ekadashi: {
    name: 'Ekadashi',
    hindi: 'एकादशी',
    tithi: 'Tithi 11 (Shukla) & Tithi 26 (Krishna)',
    deity: 'Lord Vishnu',
    icon: '🕉️',
    tagline: 'The Sacred Fasting Day of Lord Vishnu',
    description: 'Ekadashi falls on the 11th lunar day (Tithi) of both the waxing (Shukla Paksha) and waning (Krishna Paksha) moon. Fasting on Ekadashi is one of the most auspicious practices in Vaishnavism, believed to remove sins and grant liberation.',
    significance: 'Ekadashi is dedicated to Lord Vishnu. Fasting and devotion on this day is said to bestow spiritual merit equivalent to performing great yagnas and going on pilgrimage.',
    fasting_rules: [
      'Begin fast at sunrise on Ekadashi, break at sunrise on Dwadashi (next day)',
      'Avoid grains, lentils, and certain vegetables (onion, garlic, non-sattvic foods)',
      'Fruits, milk, nuts, and root vegetables are permitted (Phalahar)',
      'Strict Nirjala Ekadashi -- no water at all -- is observed on Jyeshtha Shukla Ekadashi',
      'Chant Vishnu Sahasranam, read Bhagavad Gita, or listen to Vishnu Katha',
      'Wake before sunrise, take bath, and perform Vishnu Puja',
      'Donate food to Brahmins or the poor',
      'Avoid sleeping during the day',
    ],
    what_to_eat: 'Sabudana (sago), fruits, milk, curd, nuts, potatoes, sweet potato, kuttu atta (buckwheat). Avoid rice, wheat, lentils, onion, garlic.',
    what_to_avoid: 'Rice, wheat, barley, lentils, chickpeas, onion, garlic, non-vegetarian food.',
    colour: 'from-indigo-500/20 to-blue-500/10',
  },
  amavasya: {
    name: 'Amavasya',
    hindi: 'अमावस्या',
    tithi: 'Tithi 30 (New Moon)',
    deity: 'Pitrs (Ancestors)',
    icon: '🌑',
    tagline: 'The New Moon -- Day of Ancestral Offerings',
    description: 'Amavasya is the new moon day -- the last Tithi of the lunar month when the Moon is not visible. It is the most important day for Pitru Tarpan (ancestral offerings) in Hindu tradition.',
    significance: 'Amavasya is considered highly auspicious for ancestral rites (Pitru Karma) and Shradh rituals. Ancestors are believed to be especially receptive to offerings made on this day. It is also important for Shiva worship in many traditions.',
    fasting_rules: [
      'Optional fast (not mandatory like Ekadashi)',
      'Perform Pitru Tarpan -- offering water + sesame seeds (til) to ancestors',
      'Visit a river, lake, or water body for the Tarpan ritual',
      'Light a lamp (diya) in the evening for ancestors',
      'Donate food (especially to Brahmins) in the name of ancestors',
      'Avoid auspicious events (marriages, housewarming) on Amavasya',
    ],
    what_to_eat: 'Simple sattvic food. Many observe partial fast.',
    what_to_avoid: 'Non-vegetarian food, alcohol. Avoid starting new ventures.',
    colour: 'from-slate-500/20 to-gray-500/10',
  },
  purnima: {
    name: 'Purnima',
    hindi: 'पूर्णिमा',
    tithi: 'Tithi 15 (Full Moon)',
    deity: 'Chandra (Moon) and Lord Vishnu / Shiva (by month)',
    icon: '🌕',
    tagline: 'The Full Moon -- Day of Illumination and Devotion',
    description: 'Purnima is the full moon day, the 15th Tithi of the waxing lunar fortnight. Each Purnima has a special name and significance depending on the month. It is considered highly auspicious for all spiritual activities.',
    significance: 'Purnima marks the peak of the lunar cycle. The full moon amplifies spiritual energy and is associated with clarity, abundance, and the fulfilment of desires. Many major Hindu festivals -- Holi, Guru Purnima, Sharad Purnima, Buddha Purnima -- fall on Purnima.',
    fasting_rules: [
      'Observe Purnima fast (Phalahar -- fruits and milk permitted)',
      'Chant the name of the presiding deity for the month',
      'Offer Arghya (water) to the rising full moon',
      'Light ghee lamp and perform evening Puja',
      'Satyanarayana Puja is traditionally done on Purnima',
      'Donate to Brahmins or charity',
    ],
    what_to_eat: 'Fruits, milk, curd, nuts, sago. Sattvic food.',
    what_to_avoid: 'Non-vegetarian food, alcohol.',
    colour: 'from-amber-500/20 to-yellow-500/10',
  },
};
```

---

## UI Layout (all 3 pages -- same component, different data)

```
[Page header: "{Name} -- {Tagline}"]

[Next date card -- GlassCard, gold border]
  ├── "Next {Name}: [Date] -- [Day of Week]"
  ├── Tithi name from Panchang (e.g. "Ekadashi -- Shukla Paksha")
  ├── Nakshatra of the day
  └── "View full Panchang for this day →" → /panchang/date/{date}

[Upcoming dates -- this year's list]
  └── Next 4-6 occurrences (from festival API, filtered by type)

[Panchang card for next date -- GlassCard]
  ├── Sunrise / Sunset
  ├── Timing windows: Brahma Muhurta, Abhijit, Rahu Kaal
  └── (from GET /api/panchang/daily?date={next_date}&location_slug=new-delhi)

[Significance card]
  └── Description + Significance text

[Fasting rules card]
  └── Bulleted list

[What to eat / What to avoid -- 2-column card]

[FAQ section]
  ├── "When is the next {Name}?"
  ├── "What to eat during {Name} fast?"
  ├── "What are the rituals of {Name}?"
  └── "Can we eat [food] on {Name}?"

[Upsell CTA]
  └── "Get personalised Puja timing for your birth chart" → /birth-chart

[Related devotional dates]
  ├── Ekadashi page → /ekadashi
  ├── Amavasya page → /amavasya
  └── Purnima page → /purnima
  (Show the other 2, not the current one)
```

---

## SEO Requirements

### Meta titles
| Page | Title |
|---|---|
| Ekadashi | `Ekadashi 2026 -- Next Date, Fasting Rules & Significance \| EverydayHoroscope` |
| Amavasya | `Amavasya 2026 -- Next Date, Rituals & Puja Muhurat \| EverydayHoroscope` |
| Purnima | `Purnima 2026 -- Next Full Moon Date, Fasting & Significance \| EverydayHoroscope` |

### Meta descriptions
- Ekadashi: `When is the next Ekadashi in 2026? Get the exact date, Panchang details, fasting rules, and what to eat and avoid during Ekadashi vrat.`
- Amavasya: `When is the next Amavasya in 2026? Get the exact date, Pitru Tarpan muhurat, rituals and Panchang for Amavasya.`
- Purnima: `When is the next Purnima (full moon) in 2026? Get the date, Panchang, fasting rules and puja muhurat for Purnima.`

### JSON-LD -- Event schema
```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Ekadashi -- [Month] 2026",
  "startDate": "{next_date}",
  "description": "{tagline}",
  "location": { "@type": "Place", "name": "India" }
}
```

### FAQ schema (required -- "when is next ekadashi" queries dominate this niche)
Include at minimum:
- "When is the next {Name}?"
- "What to eat during {Name} fast?"
- "What rituals should be done on {Name}?"

---

## Visual Spec

- Gold-border GlassCard for all data cards
- Next date card: hero size with gold gradient background `bg-gradient-to-br from-gold/15 to-gold/5`
- Upcoming dates list: simple timeline with gold dots
- Fasting rules: gold checkmark bullets
- FAQ: gold expand icon, collapsible
- Type icon (🕉️ / 🌑 / 🌕) displayed prominently in header
- No custom CSS -- Tailwind only

---

## ⚠️ Critical Notes

1. **"Next date" is dynamic** -- always computed from `GET /api/panchang/festivals?year={currentYear}`, never hardcoded
2. **If no match found this year** (e.g. late December) -- also query `?year={nextYear}` as fallback
3. **Panchang data** -- from existing `panchang_router.py` endpoint
4. **New Delhi default** -- use New Delhi as the location for the Panchang card (these are national observances)
5. **Smart quote fix** -- run on `DevotionalDatePage.jsx` before handover
6. **Lazy load** -- component can be lazy-loaded

---

## Acceptance Criteria

- [ ] `/ekadashi`, `/amavasya`, `/purnima` all load without 404
- [ ] "Next date" is accurate (matches Panchang calendar)
- [ ] Upcoming dates list shows correct future dates
- [ ] Panchang card for next date populates correctly
- [ ] FAQ schema present and correct
- [ ] Event JSON-LD present on each page
- [ ] Cross-links between devotional pages work
- [ ] No console errors
- [ ] Build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
