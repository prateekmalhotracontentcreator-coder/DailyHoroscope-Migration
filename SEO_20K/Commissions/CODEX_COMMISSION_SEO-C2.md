# Commission Brief: SEO-C2 -- Rashi Calculator + Nakshatra Calculator

**Commission ID:** SEO-C2  
**Track:** C -- Codex Feature Builds  
**Priority:** Tier 2 -- Phase 4  
**Date:** 2026-05-20  
**Status:** READY TO ISSUE  

---

## What to Build

Two calculator tool pages:

| Calculator | Route | What it does |
|---|---|---|
| Rashi Calculator | `/rashi-calculator` | Input DOB → output Moon sign (Rashi) + traits |
| Nakshatra Calculator | `/nakshatra-calculator` | Input DOB + TOB + place → output birth Nakshatra + Pada |

---

## Files to Create

### Frontend
- `frontend/src/pages/calculators/RashiCalculatorPage.jsx`
- `frontend/src/pages/calculators/NakshatraCalculatorPage.jsx`

### Backend
- No new files -- both calculators call existing `vedic_calculator.py` via existing routes (see below)

---

## Route Wiring (App.js additions)

```jsx
import { RashiCalculatorPage }     from './pages/calculators/RashiCalculatorPage';
import { NakshatraCalculatorPage } from './pages/calculators/NakshatraCalculatorPage';

// Add inside <Routes>:
<Route path="/rashi-calculator"     element={<RashiCalculatorPage />} />
<Route path="/nakshatra-calculator" element={<NakshatraCalculatorPage />} />
```

---

## Calculator 1: Rashi Calculator (`/rashi-calculator`)

### What is Rashi?
Rashi = Moon sign in Vedic astrology (not Sun sign). Determined by the Moon's position at the exact moment of birth. This is the primary sign used in Indian astrology (unlike Western astrology which uses Sun signs).

### Input required
- Date of Birth (date picker)
- Time of Birth (time picker) -- optional but improves accuracy
- Place of Birth (city picker) -- optional but improves accuracy

### Backend call
```
POST /api/calculate-birth-chart
Body: {
  "date_of_birth": "YYYY-MM-DD",
  "time_of_birth": "HH:MM",          // if provided
  "place_of_birth": "City Name",      // if provided; default to "New Delhi" if not
  "timezone": "Asia/Kolkata"          // inferred from place
}
```

This is the existing birth chart calculation endpoint. From the response, extract:
- `moon_sign` (Rashi)
- `moon_sign_lord` (ruling planet)
- `moon_degree` (if available)

**⚠️ All astrological calculations must come from `vedic_calculator.py` via the existing birth chart API. Do NOT add any calculation logic in the frontend or in any new file.**

### Output to display

```javascript
const RASHI_DATA = {
  aries:       { hindi: 'मेष',      lord: 'Mars',    element: 'Fire',  quality: 'Cardinal', traits: ['Energetic', 'Courageous', 'Impulsive', 'Leadership'] },
  taurus:      { hindi: 'वृषभ',     lord: 'Venus',   element: 'Earth', quality: 'Fixed',    traits: ['Patient', 'Reliable', 'Artistic', 'Stubborn'] },
  gemini:      { hindi: 'मिथुन',    lord: 'Mercury', element: 'Air',   quality: 'Mutable',  traits: ['Curious', 'Adaptable', 'Communicative', 'Restless'] },
  cancer:      { hindi: 'कर्क',     lord: 'Moon',    element: 'Water', quality: 'Cardinal', traits: ['Intuitive', 'Nurturing', 'Emotional', 'Protective'] },
  leo:         { hindi: 'सिंह',     lord: 'Sun',     element: 'Fire',  quality: 'Fixed',    traits: ['Creative', 'Generous', 'Charismatic', 'Proud'] },
  virgo:       { hindi: 'कन्या',    lord: 'Mercury', element: 'Earth', quality: 'Mutable',  traits: ['Analytical', 'Perfectionist', 'Practical', 'Helpful'] },
  libra:       { hindi: 'तुला',     lord: 'Venus',   element: 'Air',   quality: 'Cardinal', traits: ['Diplomatic', 'Charming', 'Indecisive', 'Fair'] },
  scorpio:     { hindi: 'वृश्चिक',  lord: 'Mars',    element: 'Water', quality: 'Fixed',    traits: ['Intense', 'Passionate', 'Secretive', 'Transformative'] },
  sagittarius: { hindi: 'धनु',      lord: 'Jupiter', element: 'Fire',  quality: 'Mutable',  traits: ['Optimistic', 'Adventurous', 'Philosophical', 'Restless'] },
  capricorn:   { hindi: 'मकर',      lord: 'Saturn',  element: 'Earth', quality: 'Cardinal', traits: ['Disciplined', 'Ambitious', 'Patient', 'Reserved'] },
  aquarius:    { hindi: 'कुम्भ',    lord: 'Saturn',  element: 'Air',   quality: 'Fixed',    traits: ['Innovative', 'Independent', 'Humanitarian', 'Detached'] },
  pisces:      { hindi: 'मीन',      lord: 'Jupiter', element: 'Water', quality: 'Mutable',  traits: ['Intuitive', 'Creative', 'Compassionate', 'Escapist'] },
};
```

### UI Layout
```
[Page header: "Rashi Calculator -- Find Your Vedic Moon Sign"]
[Input form card]
  ├── Date of Birth (required)
  ├── Time of Birth (optional -- "Improves accuracy")
  ├── Place of Birth (optional -- simple text input, default New Delhi)
  └── [Calculate My Rashi] button

[Result card -- appears after calculation]
  ├── "Your Rashi (Moon Sign) is:"
  ├── Sign name (large) + Hindi name
  ├── Sign glyph in element-coloured circle
  ├── Lord: {planet} | Element: {element} | Quality: {quality}
  ├── Key traits: badge pills
  └── Brief interpretation paragraph (2-3 sentences, hardcoded per sign)

[What is Rashi? info card]
  └── Brief explanation differentiating Rashi (Moon sign) from Western Sun signs

[Upsell CTA]
  ├── "Discover your complete Vedic profile with a full Birth Chart"
  └── [Unlock Full Birth Chart] → /birth-chart

[Related tools]
  ├── "Find your Nakshatra →" → /nakshatra-calculator
  └── "Check compatibility →" → /kundali-milan
```

---

## Calculator 2: Nakshatra Calculator (`/nakshatra-calculator`)

### What is Nakshatra?
Nakshatra = lunar mansion -- 27 divisions of the zodiac (each 13°20') used in Vedic astrology. The birth Nakshatra (Moon's Nakshatra) is used for Dasha timing, marriage matching, naming, and muhurat. Each Nakshatra has 4 Padas (quarters).

### Input required (all required for accuracy)
- Date of Birth
- Time of Birth (hour + minute)
- Place of Birth (city/country -- use a simple text input with city name, or a subset of the Panchang 318-city picker)

### Backend call
Same as Rashi Calculator:
```
POST /api/calculate-birth-chart
```

From response, extract:
- `moon_nakshatra` (birth Nakshatra)
- `moon_nakshatra_lord` (Nakshatra lord / Dasha lord)
- `moon_nakshatra_pada` (Pada 1-4)

**⚠️ All calculations from `vedic_calculator.py` -- no frontend calculations.**

### Output to display

```javascript
const NAKSHATRA_DATA = {
  ashwini:      { number: 1,  lord: 'Ketu',    deity: 'Ashwini Kumaras', symbol: 'Horse Head',    qualities: ['Swift', 'Healing', 'Pioneering'], pada_akshar: ['Chu', 'Che', 'Cho', 'La'] },
  bharani:      { number: 2,  lord: 'Venus',   deity: 'Yama',            symbol: 'Yoni',          qualities: ['Restraint', 'Creative', 'Transformative'], pada_akshar: ['Li', 'Lu', 'Le', 'Lo'] },
  krittika:     { number: 3,  lord: 'Sun',     deity: 'Agni',            symbol: 'Razor/Flame',   qualities: ['Sharp', 'Purifying', 'Courageous'], pada_akshar: ['A', 'I', 'U', 'E'] },
  rohini:       { number: 4,  lord: 'Moon',    deity: 'Brahma',          symbol: 'Ox Cart',       qualities: ['Creative', 'Fertile', 'Sensual'], pada_akshar: ['O', 'Va', 'Vi', 'Vu'] },
  mrigashira:   { number: 5,  lord: 'Mars',    deity: 'Soma',            symbol: 'Deer Head',     qualities: ['Curious', 'Gentle', 'Seeking'], pada_akshar: ['Ve', 'Vo', 'Ka', 'Ki'] },
  ardra:        { number: 6,  lord: 'Rahu',    deity: 'Rudra',           symbol: 'Teardrop',      qualities: ['Intense', 'Destructive', 'Transforming'], pada_akshar: ['Ku', 'Gha', 'Ing', 'Jha'] },
  punarvasu:    { number: 7,  lord: 'Jupiter', deity: 'Aditi',           symbol: 'Bow & Quiver',  qualities: ['Generous', 'Returning', 'Nourishing'], pada_akshar: ['Ke', 'Ko', 'Ha', 'Hi'] },
  pushya:       { number: 8,  lord: 'Saturn',  deity: 'Brihaspati',      symbol: 'Flower/Circle', qualities: ['Nourishing', 'Protective', 'Spiritual'], pada_akshar: ['Hu', 'He', 'Ho', 'Da'] },
  ashlesha:     { number: 9,  lord: 'Mercury', deity: 'Nagas',           symbol: 'Serpent',       qualities: ['Penetrating', 'Clinging', 'Mystical'], pada_akshar: ['Di', 'Du', 'De', 'Do'] },
  magha:        { number: 10, lord: 'Ketu',    deity: 'Pitrs',           symbol: 'Throne/Palanquin', qualities: ['Regal', 'Ancestral', 'Authoritative'], pada_akshar: ['Ma', 'Mi', 'Mu', 'Me'] },
  purva_phalguni: { number: 11, lord: 'Venus', deity: 'Bhaga',           symbol: 'Hammock',       qualities: ['Pleasure', 'Creative', 'Romantic'], pada_akshar: ['Mo', 'Ta', 'Ti', 'Tu'] },
  uttara_phalguni: { number: 12, lord: 'Sun',  deity: 'Aryaman',         symbol: 'Bed/Legs',      qualities: ['Helpful', 'Responsible', 'Patronising'], pada_akshar: ['Te', 'To', 'Pa', 'Pi'] },
  hasta:        { number: 13, lord: 'Moon',    deity: 'Savitar',         symbol: 'Hand',          qualities: ['Skilled', 'Dexterous', 'Resourceful'], pada_akshar: ['Pu', 'Sha', 'Na', 'Tha'] },
  chitra:       { number: 14, lord: 'Mars',    deity: 'Tvastar',         symbol: 'Bright Jewel',  qualities: ['Creative', 'Artistic', 'Perceptive'], pada_akshar: ['Pe', 'Po', 'Ra', 'Ri'] },
  swati:        { number: 15, lord: 'Rahu',    deity: 'Vayu',            symbol: 'Coral/Sword',   qualities: ['Independent', 'Flexible', 'Spreading'], pada_akshar: ['Ru', 'Re', 'Ro', 'Ta'] },
  vishakha:     { number: 16, lord: 'Jupiter', deity: 'Indragni',        symbol: 'Triumphal Arch', qualities: ['Goal-oriented', 'Determined', 'Competitive'], pada_akshar: ['Ti', 'Tu', 'Te', 'To'] },
  anuradha:     { number: 17, lord: 'Saturn',  deity: 'Mitra',           symbol: 'Lotus',         qualities: ['Devoted', 'Friendly', 'Disciplined'], pada_akshar: ['Na', 'Ni', 'Nu', 'Ne'] },
  jyeshtha:     { number: 18, lord: 'Mercury', deity: 'Indra',           symbol: 'Circular Amulet', qualities: ['Senior', 'Protective', 'Powerful'], pada_akshar: ['No', 'Ya', 'Yi', 'Yu'] },
  mula:         { number: 19, lord: 'Ketu',    deity: 'Niritti',         symbol: 'Tied Roots',    qualities: ['Investigative', 'Destructive', 'Transforming'], pada_akshar: ['Ye', 'Yo', 'Bha', 'Bhi'] },
  purva_ashadha: { number: 20, lord: 'Venus',  deity: 'Apas',            symbol: 'Fan/Winnowing Basket', qualities: ['Invincible', 'Purifying', 'Energising'], pada_akshar: ['Bhu', 'Dha', 'Pha', 'Da'] },
  uttara_ashadha: { number: 21, lord: 'Sun',   deity: 'Vishvadevas',     symbol: 'Elephant Tusk', qualities: ['Victorious', 'Responsible', 'Principled'], pada_akshar: ['Be', 'Bo', 'Ja', 'Ji'] },
  shravana:     { number: 22, lord: 'Moon',    deity: 'Vishnu',          symbol: 'Ear/Trident',   qualities: ['Learning', 'Listening', 'Connecting'], pada_akshar: ['Ju', 'Je', 'Jo', 'Gha'] },
  dhanishtha:   { number: 23, lord: 'Mars',    deity: 'Ashta Vasus',     symbol: 'Drum',          qualities: ['Wealthy', 'Musical', 'Courageous'], pada_akshar: ['Ga', 'Gi', 'Gu', 'Ge'] },
  shatabhisha:  { number: 24, lord: 'Rahu',    deity: 'Varuna',          symbol: 'Empty Circle',  qualities: ['Healing', 'Secretive', 'Mystical'], pada_akshar: ['Go', 'Sa', 'Si', 'Su'] },
  purva_bhadra: { number: 25, lord: 'Jupiter', deity: 'Aja Ekapad',      symbol: 'Front Legs of Funeral Cot', qualities: ['Passionate', 'Fiery', 'Otherworldly'], pada_akshar: ['Se', 'So', 'Da', 'Di'] },
  uttara_bhadra: { number: 26, lord: 'Saturn', deity: 'Ahir Budhnya',    symbol: 'Back Legs of Funeral Cot', qualities: ['Stable', 'Serpentine', 'Deep'], pada_akshar: ['Du', 'Tha', 'Jha', 'Da'] },
  revati:       { number: 27, lord: 'Mercury', deity: 'Pushan',          symbol: 'Fish/Drum',     qualities: ['Nourishing', 'Protective', 'Completing'], pada_akshar: ['De', 'Do', 'Cha', 'Chi'] },
};
```

### UI Layout
```
[Page header: "Nakshatra Calculator -- Find Your Birth Star"]
[Input form card -- all 3 inputs required]
  ├── Date of Birth
  ├── Time of Birth (HH:MM)
  └── Place of Birth (text input)
  └── [Calculate My Nakshatra] button

[Result card]
  ├── "Your Birth Nakshatra is:"
  ├── Nakshatra name (large) + number (e.g. "Rohini -- 4th Nakshatra")
  ├── Pada: "Pada {N}" with akshar (starting syllable)
  ├── Nakshatra Lord: {planet} -- this is your Mahadasha start planet
  ├── Deity: {deity} | Symbol: {symbol}
  ├── Key qualities: badge pills
  └── "Your Vimshottari Dasha sequence starts with {lord} Mahadasha"

[Naming guidance card]
  └── "Traditional Vedic names for this Nakshatra begin with: {pada_akshar[0]}, {pada_akshar[1]}, ..."

[What is Nakshatra? info card]

[Upsell CTA]
  ├── "Explore your complete Dasha timeline and life predictions"
  └── [Unlock Full Birth Chart & Dasha] → /birth-chart

[Related tools]
  └── "Find your Moon Sign (Rashi) →" → /rashi-calculator
```

---

## SEO Requirements (both pages)

### Rashi Calculator
- Title: `Rashi Calculator -- Find Your Vedic Moon Sign | EverydayHoroscope`
- Description: `Find your Rashi (Vedic Moon sign) instantly. Enter your date of birth to get your Moon sign, ruling planet, traits and personalised insights.`
- JSON-LD: `@type: "WebApplication"`, `applicationCategory: "AstrologyApplication"`

### Nakshatra Calculator
- Title: `Nakshatra Calculator -- Find Your Birth Star | EverydayHoroscope`
- Description: `Find your birth Nakshatra (lunar mansion) and Pada. Enter your date, time and place of birth for an accurate Vedic Nakshatra reading.`
- JSON-LD: `@type: "WebApplication"`, `applicationCategory: "AstrologyApplication"`

---

## Upsell Path
Both calculators feed into:
1. **Birth Chart** (`/birth-chart`) -- full Kundali with all planetary positions
2. **Kundali Milan** (`/kundali-milan`) -- compatibility matching (uses Nakshatra)
3. **Strategist** (`/strategist`) -- Dasha-based life strategy

---

## Visual Spec

- Input form: GlassCard with gold-bordered inputs
- Result card: GlassCard with gold header
- Nakshatra/Rashi name: large display text in `text-gold`
- Trait badges: `bg-gold/15 text-gold border border-gold/30`
- "Calculate" button: `bg-gold text-background font-semibold`
- Loading state: spinner inside result card area
- No custom CSS -- Tailwind only

---

## ⚠️ Critical Notes

1. **All calculations from `vedic_calculator.py`** via existing `/api/calculate-birth-chart` endpoint. Zero calculation logic in frontend.
2. **Do NOT add calculation functions to any new file** -- the backend already has everything
3. **Time of Birth** is optional for Rashi (Moon sign doesn't change hourly) but required for Nakshatra (accuracy depends on exact Moon degree)
4. **Place of Birth** -- simple text input is fine; if the API requires a timezone, default to `Asia/Kolkata` when no place is given
5. **Smart quote fix** -- run on both `.jsx` files before handover
6. **Lazy load** -- both components can be lazy-loaded

---

## Acceptance Criteria

- [ ] `/rashi-calculator` loads and form submits without errors
- [ ] `/nakshatra-calculator` loads and form submits without errors
- [ ] Both pages call `/api/calculate-birth-chart` (not any new calculation)
- [ ] Rashi result shows sign name, lord, element, traits
- [ ] Nakshatra result shows nakshatra name, pada, lord, deity, akshar
- [ ] Both pages have unique `<title>` and `<meta description>`
- [ ] JSON-LD WebApplication schema on both pages
- [ ] Upsell CTA links to `/birth-chart`
- [ ] Related tool cross-links work
- [ ] No console errors
- [ ] Build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
