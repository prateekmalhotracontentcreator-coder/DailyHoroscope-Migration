# Commission Brief: SEO-C6 -- Report Category Discovery Pages

**Commission ID:** SEO-C6  
**Track:** C -- Codex Feature Builds  
**Priority:** Tier 3 -- Phase 6 (needs Razorpay live keys first)  
**Date:** 2026-05-20  
**Status:** READY TO ISSUE -- ⚠️ Prerequisite: SEO-C1 (legal pages) + Razorpay live keys active  

---

## Context -- What Already Exists

The app has **many individual premium report landing pages** already built (KarmicDebt, CareerBlueprint, ShadowSelf, etc. at routes like `/karmic-debt-report`). What is **missing** are **SEO category discovery pages** -- broader pages that rank for generic searches like "kundali report", "numerology reading", "love astrology report" and funnel visitors into the relevant premium products.

---

## What to Build

4 new category landing pages (SEO discovery, not product pages):

| Route | Category | Covers |
|---|---|---|
| `/reports/kundali` | Birth Chart Reports | Links to `/birth-chart`, `/brihat-kundli`, individual report landings |
| `/reports/numerology` | Numerology Reports | Links to `/numerology`, all numerology report types |
| `/reports/love` | Love & Compatibility | Links to love reports, `/kundali-milan`, `/love-calculator` |
| `/reports/career` | Career & Life Purpose | Links to career reports, `/the-strategist` |

**Note on Longevity:** `/longevity` and `/the-longevity-report` already exist as dedicated pages. No new longevity category page needed.

---

## Files to Create

### Frontend
- `frontend/src/pages/reports/category/KundaliReportsPage.jsx`
- `frontend/src/pages/reports/category/NumerologyReportsPage.jsx`
- `frontend/src/pages/reports/category/LoveReportsPage.jsx`
- `frontend/src/pages/reports/category/CareerReportsPage.jsx`

### Backend
No backend changes. All pages are static content + links to existing pages/reports.

---

## Route Wiring (App.js)

```jsx
import { KundaliReportsPage }    from './pages/reports/category/KundaliReportsPage';
import { NumerologyReportsPage } from './pages/reports/category/NumerologyReportsPage';
import { LoveReportsPage }       from './pages/reports/category/LoveReportsPage';
import { CareerReportsPage }     from './pages/reports/category/CareerReportsPage';

<Route path="/reports/kundali"     element={<KundaliReportsPage />} />
<Route path="/reports/numerology"  element={<NumerologyReportsPage />} />
<Route path="/reports/love"        element={<LoveReportsPage />} />
<Route path="/reports/career"      element={<CareerReportsPage />} />
```

---

## Page Structure (same template for all 4, different content)

```
[Category hero]
  ├── Category name (Cinzel, large)
  ├── 2-sentence category description
  └── Primary CTA → most popular report in this category

[What you'll discover -- 3 bullet GlassCard]
  └── 3 key insights this category of reports provides

[Reports in this category -- card grid]
  └── Each card:
       ├── Report name
       ├── 2-sentence description
       ├── What it reveals (3 bullet points)
       ├── "Most popular" / "Premium" badge
       └── [Get This Report] → report landing page

[How it works -- 3-step card]
  ├── Step 1: Enter your birth details
  ├── Step 2: Our Vedic engine calculates your chart
  └── Step 3: Receive your personalised report

[FAQ accordion -- category-specific questions]

[Related categories -- links to other 3 category pages]
```

---

## Category Content

### `/reports/kundali` -- Kundali & Birth Chart Reports

**Hero:** "Kundali Reports -- Your Complete Vedic Birth Chart"  
**Description:** "Your Kundali is the blueprint of your life -- a precise map of planetary positions at the moment of your birth, calculated using KP Jyotish and Swiss Ephemeris."

**Reports in this category:**
| Report | Route | Description |
|---|---|---|
| Birth Chart (Lagna Kundali) | `/birth-chart` | Full D1 chart, planetary positions, basic dashas |
| Brihat Kundali Pro | `/brihat-kundli` | Extended chart with all 16 divisional charts |
| Kundali Milan | `/kundali-milan` | Marriage compatibility -- 36-point Ashtakoot matching |
| Karmic Debt Analysis | `/karmic-debt-report` | Karmic patterns from birth chart |
| Life Cycles Report | `/life-cycles-report` | Dasha-based life phase analysis |

**FAQ:**
- "What is a Kundali?" / "What is an Ashi?" / "How accurate is Vedic birth chart calculation?" / "What is KP Jyotish?"

---

### `/reports/numerology` -- Numerology Reports

**Hero:** "Numerology Reports -- The Hidden Code in Your Name and Birth Date"  
**Description:** "Vedic numerology (Ankjyotish) reveals the vibrational patterns in your name and birth date. Your numbers are as unique as your fingerprint."

**Reports in this category:**
| Report | Route | Description |
|---|---|---|
| Life Path Report | `/numerology` | Core numbers: Life Path, Destiny, Soul Urge, Personality |
| Name Correction Report | `/numerology` | Align your name vibration with your destiny |
| Relationship Compatibility | `/numerology` | Compare numbers for relationship harmony |
| Career Blueprint | `/numerology` | Career path from numerology profile |
| Annual Forecast | `/numerology` | Personal Year timing forecast |
| Name Compatibility | `/compatibility/name` | Quick name compatibility check (free) |

**FAQ:**
- "What is numerology?" / "Is Chaldean or Pythagorean numerology more accurate?" / "What is a Life Path number?"

---

### `/reports/love` -- Love & Compatibility Reports

**Hero:** "Love & Compatibility Reports -- Your Relationship Blueprint"  
**Description:** "Vedic astrology reveals relationship dynamics with precision -- from Kundali matching to dasha-timed love windows. Understand your connections at the deepest level."

**Reports in this category:**
| Report | Route | Description |
|---|---|---|
| Kundali Milan | `/kundali-milan` | Traditional 36-point marriage compatibility |
| Love Weather Report | `/love-weather-report` | Current planetary influences on your love life |
| Romance & Creative Report | `/romance-creative-report` | Venus-led relationship timing |
| Partnership Window Report | `/partnership-window-report` | When is your next relationship window? |
| Intimacy & Vitality Report | `/intimacy-vitality-report` | Physical + emotional compatibility |
| Soulmate Timing Report | `/soulmate-timing-report` | Dasha timing for significant relationships |
| Soul Connection Report | `/soul-connection-report` | Karmic relationship analysis |
| Love Calculator (free) | `/love-calculator` | Quick name/DOB compatibility check |
| Relationship Numerology | `/numerology` | Name-based relationship analysis |

**FAQ:**
- "What is Kundali matching?" / "What is a compatibility score?" / "Can astrology predict when I'll find love?"

---

### `/reports/career` -- Career & Life Purpose Reports

**Hero:** "Career & Life Purpose Reports -- Your Professional Blueprint"  
**Description:** "Vedic astrology maps your career potential, timing windows, and professional destiny through planetary positions, Dasha timing, and Yoga analysis."

**Reports in this category:**
| Report | Route | Description |
|---|---|---|
| Career Blueprint Report | `/career-blueprint-report` | Full career potential analysis |
| The Strategist | `/the-strategist` | KP Oracle-powered career intelligence system |
| Dharma & Purpose Report | `/dharma-purpose-report` | Soul purpose and life mission |
| Wealth Blueprint Report | `/wealth-blueprint-report` | Financial potential and timing |
| Gains & Network Report | `/gains-network-report` | 11th house analysis -- income streams |
| Arc Angel (12 Life Areas) | `/arc-angel` | All 12 life areas with Dasha timing |

**FAQ:**
- "Which planet rules career in Vedic astrology?" / "What is a Dasha?" / "How does KP Jyotish predict career timing?"

---

## SEO Requirements

### Titles
| Page | Title |
|---|---|
| Kundali Reports | `Kundali & Birth Chart Reports -- Vedic Astrology \| EverydayHoroscope` |
| Numerology Reports | `Numerology Reports -- Vedic Ankjyotish Readings \| EverydayHoroscope` |
| Love Reports | `Love & Compatibility Reports -- Vedic Astrology \| EverydayHoroscope` |
| Career Reports | `Career & Life Purpose Reports -- Vedic Astrology \| EverydayHoroscope` |

### Meta descriptions
- Kundali: `Explore Kundali and birth chart reports. Full D1 chart, Brihat Kundali, Kundali Milan, and Karmic Debt analysis -- powered by KP Jyotish and Swiss Ephemeris.`
- Numerology: `Discover your numerology reports -- Life Path, Name Correction, Relationship Compatibility, and Annual Forecast. Vedic Ankjyotish for deep personal insight.`
- Love: `Love and compatibility reports using Vedic astrology. Kundali Milan, Love Weather, Soulmate Timing, Soul Connection -- find your relationship blueprint.`
- Career: `Career and life purpose reports using Vedic astrology. Career Blueprint, The Strategist, Dharma Purpose, Wealth Blueprint -- powered by KP Jyotish.`

### JSON-LD
`@type: "ItemList"` for each category page -- each report card is a `ListItem`.

### FAQ schema on each page -- required.

---

## Visual Spec

- Category hero: full-width GlassCard with gold radial gradient header
- Report cards: GlassCard, 2-column grid on desktop, 1-column mobile
- "Most Popular" badge: `bg-gold/15 text-gold border border-gold/30`
- "Premium" badge: `bg-purple-500/15 text-purple-400 border border-purple-400/30`
- CTA buttons: `bg-gold text-background` (primary), `border border-gold/30 text-gold` (secondary)
- Related category links at bottom: 3 pills linking to sibling category pages
- No custom CSS -- Tailwind only

---

## ⚠️ Critical Notes

1. **No new report functionality** -- these are discovery/navigation pages only. All report links point to existing pages.
2. **Revenue gate** -- SEO-C1 (legal pages content) + Razorpay live keys must be active before these category pages go live, since they prominently promote premium reports
3. **Smart quote fix** on all 4 `.jsx` files
4. **Lazy load** all 4 components

---

## Acceptance Criteria

- [ ] All 4 category routes load without 404
- [ ] Each page has correct `<title>` and `<meta description>`
- [ ] ItemList JSON-LD present on each page
- [ ] FAQ schema present on each page
- [ ] All report links resolve correctly (no dead links)
- [ ] Related category cross-links work across all 4 pages
- [ ] No console errors
- [ ] Build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
