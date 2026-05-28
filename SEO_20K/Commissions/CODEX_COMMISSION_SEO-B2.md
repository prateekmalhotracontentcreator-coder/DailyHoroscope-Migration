# Commission Brief: SEO-B2 -- Festival Pages Bundle (Holi, Diwali, Karwa Chauth)

**Commission ID:** SEO-B2  
**Track:** B -- Codex Content Pages  
**Priority:** Tier 1 -- Phase 2 (build after SEO-B3 Festival Hub is live)  
**Date:** 2026-05-20  
**Status:** READY TO ISSUE (depends on SEO-B3 for parent `/festivals` hub)  

---

## What to Build

3 standalone seasonal festival pages:

| Festival | Route | Search volume ref |
|---|---|---|
| Holi | `/festivals/holi` | 476K searches, KD=11 (highest ROI) |
| Diwali | `/festivals/diwali` | High-volume, peak Oct |
| Karwa Chauth | `/festivals/karwa-chauth` | High-volume, peak Oct |

---

## Files to Create

### Frontend
- `frontend/src/pages/festivals/FestivalPage.jsx`  
  (Single component -- parameterised by `slug` prop or route param)

### Backend
No new files. All data from existing endpoints (details below).

---

## Route Wiring (App.js additions)

```jsx
import { FestivalPage } from './pages/festivals/FestivalPage';

// Add inside <Routes> (must come BEFORE any existing /festivals route):
<Route path="/festivals/holi"          element={<FestivalPage slug="holi" />} />
<Route path="/festivals/diwali"        element={<FestivalPage slug="diwali" />} />
<Route path="/festivals/karwa-chauth"  element={<FestivalPage slug="karwa-chauth" />} />
```

Note: `/festivals` (hub page from SEO-B3) should already be wired. These child routes go above it.

---

## Festival Content Data

Hardcode festival metadata in the component (this never changes year-to-year structurally):

```javascript
const FESTIVAL_DATA = {
  holi: {
    name: 'Holi',
    hindi: 'होली',
    tagline: 'The Festival of Colours',
    description: 'Holi is the ancient Hindu festival of colours, celebrated on Purnima (full moon) of Phalguna month. It marks the victory of good over evil and the arrival of spring.',
    significance: 'Holi celebrates the divine love of Radha and Krishna, the triumph of devotee Prahlad over the demon Holika, and the joyous arrival of spring.',
    rituals: [
      'Holika Dahan -- bonfire lit on the eve of Holi (Choti Holi)',
      'Playing with colours -- gulal, abir and water on the main day',
      'Thandai -- traditional spiced milk drink',
      'Visiting family and exchanging sweets',
      'Puja of Lord Vishnu and Prahlad',
    ],
    panchang_slug: 'holi',
    colour: 'from-pink-500/20 to-orange-500/10',
    icon: '🎨',
  },
  diwali: {
    name: 'Diwali',
    hindi: 'दिवाली',
    tagline: 'The Festival of Lights',
    description: 'Diwali is the most celebrated Hindu festival, marking Lord Ram\'s return to Ayodhya and the victory of light over darkness, on Amavasya of Kartik month.',
    significance: 'Diwali honours the return of Lord Ram after 14 years of exile, the worship of Goddess Lakshmi for wealth and prosperity, and the New Year for many Indian communities.',
    rituals: [
      'Lakshmi Puja on the main night (Amavasya)',
      'Lighting diyas (oil lamps) and candles throughout the home',
      'Rangoli -- decorative patterns at the entrance',
      'Fireworks and celebrations',
      'Exchanging sweets and gifts',
      'Dhanteras -- buying gold/silver on the day before Diwali',
    ],
    panchang_slug: 'diwali',
    colour: 'from-yellow-500/20 to-orange-500/10',
    icon: '🪔',
  },
  'karwa-chauth': {
    name: 'Karwa Chauth',
    hindi: 'करवा चौथ',
    tagline: 'The Festival of Marital Love',
    description: 'Karwa Chauth is observed by married Hindu women who fast from sunrise to moonrise, praying for the long life and wellbeing of their husbands.',
    significance: 'The festival celebrates the bond of marriage and is observed on the Chaturthi (4th day) of Krishna Paksha in the month of Kartik.',
    rituals: [
      'Nirjala fast (no food or water) from sunrise to moonrise',
      'Dressed in bridal attire and jewellery',
      'Karwa Chauth Puja in a group of married women in the evening',
      'Sargi -- pre-dawn meal eaten before sunrise (given by mother-in-law)',
      'Breaking fast after sighting the moon through a sieve',
    ],
    panchang_slug: 'karwa-chauth',
    colour: 'from-red-500/20 to-pink-500/10',
    icon: '🌕',
  },
};
```

---

## Data Sources (Backend)

### Festival date for the current year
```
GET /api/panchang/festivals?year={YYYY}
```
Filter response by `slug === festivalSlug` to get this year's date.

### Full Panchang for festival day
```
GET /api/panchang/daily?date={festival_date}&location_slug=new-delhi
```
Use New Delhi as default location for festival pages (national significance).

---

## UI Layout

```
[Breadcrumb: Home / Festivals / {Festival Name}]

[Hero section]
  ├── Festival icon + name (Hindi + English)
  ├── Tagline
  └── "2026 Date: [date] -- [Tithi] | [day of week]"

[Significance card -- GlassCard]
  └── Description paragraph + Significance paragraph

[Panchang for Festival Day -- GlassCard]
  ├── Tithi, Nakshatra, Yoga (from /api/panchang/daily)
  ├── Sunrise / Sunset times
  ├── Muhurat (Abhijit + Brahma) from Panchang
  └── "Full Panchang for this day →" link to /panchang/date/{date}

[Rituals card -- GlassCard]
  └── Bulleted list of rituals

[FAQ section -- below main content]
  ├── "When is {Festival} in 2026?"
  ├── "What is the significance of {Festival}?"
  ├── "What are the rituals of {Festival}?"
  └── "What is the Muhurat for {Festival} Puja in 2026?"

[Upsell CTA]
  └── "Get auspicious timing for your {Festival} Puja" → /birth-chart

[Back link: ← View all festivals]  → /festivals
```

---

## SEO Requirements

### Meta title
| Festival | Title |
|---|---|
| Holi | `Holi 2026 -- Date, Puja Muhurat & Rituals \| EverydayHoroscope` |
| Diwali | `Diwali 2026 -- Date, Lakshmi Puja Muhurat & Rituals \| EverydayHoroscope` |
| Karwa Chauth | `Karwa Chauth 2026 -- Date, Moonrise Time & Puja Muhurat \| EverydayHoroscope` |

### Meta description
- Holi: `Holi 2026 date, Holika Dahan time, puja muhurat and complete festival guide. Discover the significance and rituals of Holi according to Vedic Panchang.`
- Diwali: `Diwali 2026 date, Lakshmi Puja muhurat, and complete festival guide. Get auspicious timing for your Diwali puja according to Vedic Panchang.`
- Karwa Chauth: `Karwa Chauth 2026 date, moonrise time, and puja muhurat. Complete guide to Karwa Chauth rituals, significance, and Sargi timing.`

### JSON-LD -- Event schema (required)
```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Holi 2026",
  "startDate": "{festival_date}",
  "location": { "@type": "Place", "name": "India" },
  "description": "{festival description}",
  "organizer": { "@type": "Organization", "name": "EverydayHoroscope" }
}
```

### FAQ schema (required -- this is the high-CTR element)
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "When is Holi in 2026?",
      "acceptedAnswer": { "@type": "Answer", "text": "Holi 2026 is on [date]." }
    },
    ...
  ]
}
```

---

## Visual Spec

- Same GlassCard pattern as all other pages
- Festival colour gradient in hero (`colour` field in `FESTIVAL_DATA`)
- Festival icon (emoji) in large display at hero
- Panchang data card: gold-bordered, same styling as Panchang page cards
- Ritual list: checkmark or bullet icons in `text-gold`
- FAQ accordion: collapsible, gold expand icon
- No custom CSS -- Tailwind only

---

## ⚠️ Critical Notes

1. **Prerequisite**: `/festivals` hub (SEO-B3) should already be live -- these pages link back to it
2. **Festival date is dynamic** -- fetch from `/api/panchang/festivals?year={currentYear}`, do not hardcode dates
3. **Panchang data** -- all from existing `panchang_router.py` endpoint, no new calculations
4. **FAQ schema** -- non-negotiable for SEO; Holi has KD=11 (easy to rank) with FAQ appearing in Google rich results
5. **Smart quote fix** -- run on `FestivalPage.jsx` before handover
6. **Lazy load** -- component can be lazy-loaded

---

## Acceptance Criteria

- [ ] `/festivals/holi`, `/festivals/diwali`, `/festivals/karwa-chauth` all load without 404
- [ ] Festival date for 2026 loads dynamically from Panchang API
- [ ] Panchang card shows correct data for festival date
- [ ] Each page has unique `<title>`, `<meta description>`
- [ ] JSON-LD Event schema present on each page
- [ ] JSON-LD FAQPage schema present on each page
- [ ] "← View all festivals" link works → `/festivals`
- [ ] No console errors
- [ ] Build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
