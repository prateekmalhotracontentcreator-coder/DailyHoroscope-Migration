# Commission Brief: SEO-C7 -- Celebrity Horoscope Hub

**Commission ID:** SEO-C7  
**Track:** C -- Codex Feature Builds  
**Priority:** Tier 3 -- Phase 7  
**Date:** 2026-05-20  
**Status:** READY TO ISSUE  

---

## What to Build

A celebrity birth chart hub -- browse famous people's Vedic charts, with individual pages per celebrity.

| Route | What |
|---|---|
| `/celebrity-horoscopes` | Hub page -- browse all celebrities by category |
| `/celebrity-horoscopes/:slug` | Individual celebrity chart page |

High curiosity + shareability traffic. Demonstrates the birth chart engine on real famous charts.

---

## Files to Create

### Frontend
- `frontend/src/pages/celebrity/CelebrityHubPage.jsx`
- `frontend/src/pages/celebrity/CelebrityChartPage.jsx`

### Backend
Add one data file + two endpoints to `backend/server.py`. No new router file.

---

## Route Wiring (App.js)

```jsx
import { CelebrityHubPage }   from './pages/celebrity/CelebrityHubPage';
import { CelebrityChartPage } from './pages/celebrity/CelebrityChartPage';

<Route path="/celebrity-horoscopes"       element={<CelebrityHubPage />} />
<Route path="/celebrity-horoscopes/:slug" element={<CelebrityChartPage />} />
```

---

## Celebrity Seed Data (20 initial celebrities -- hardcode in backend)

Store as a Python list in `server.py` or a `celebrity_data.py` module:

```python
CELEBRITY_DATA = [
    # --- Bollywood ---
    {"slug": "amitabh-bachchan",    "name": "Amitabh Bachchan",    "category": "bollywood",  "dob": "1942-10-11", "tob": "16:00", "pob": "Allahabad, India",   "lat": 25.4358, "lon": 81.8463, "tz": "Asia/Kolkata"},
    {"slug": "shah-rukh-khan",      "name": "Shah Rukh Khan",      "category": "bollywood",  "dob": "1965-11-02", "tob": "02:00", "pob": "New Delhi, India",    "lat": 28.6139, "lon": 77.2090, "tz": "Asia/Kolkata"},
    {"slug": "deepika-padukone",    "name": "Deepika Padukone",    "category": "bollywood",  "dob": "1986-01-05", "tob": "00:00", "pob": "Copenhagen, Denmark",  "lat": 55.6761, "lon": 12.5683, "tz": "Europe/Copenhagen"},
    {"slug": "priyanka-chopra",     "name": "Priyanka Chopra",     "category": "bollywood",  "dob": "1982-07-18", "tob": "10:00", "pob": "Jamshedpur, India",    "lat": 22.8046, "lon": 86.2029, "tz": "Asia/Kolkata"},
    # --- Indian Politics ---
    {"slug": "narendra-modi",       "name": "Narendra Modi",       "category": "politics",   "dob": "1950-09-17", "tob": "11:00", "pob": "Vadnagar, India",      "lat": 23.7869, "lon": 72.6394, "tz": "Asia/Kolkata"},
    {"slug": "rahul-gandhi",        "name": "Rahul Gandhi",        "category": "politics",   "dob": "1970-06-19", "tob": "14:28", "pob": "New Delhi, India",    "lat": 28.6139, "lon": 77.2090, "tz": "Asia/Kolkata"},
    # --- Indian Cricket ---
    {"slug": "virat-kohli",         "name": "Virat Kohli",         "category": "cricket",    "dob": "1988-11-05", "tob": "05:00", "pob": "New Delhi, India",    "lat": 28.6139, "lon": 77.2090, "tz": "Asia/Kolkata"},
    {"slug": "ms-dhoni",            "name": "MS Dhoni",            "category": "cricket",    "dob": "1981-07-07", "tob": "02:30", "pob": "Ranchi, India",        "lat": 23.3441, "lon": 85.3096, "tz": "Asia/Kolkata"},
    {"slug": "sachin-tendulkar",    "name": "Sachin Tendulkar",    "category": "cricket",    "dob": "1973-04-24", "tob": "17:45", "pob": "Mumbai, India",        "lat": 19.0760, "lon": 72.8777, "tz": "Asia/Kolkata"},
    {"slug": "rohit-sharma",        "name": "Rohit Sharma",        "category": "cricket",    "dob": "1987-04-30", "tob": "07:00", "pob": "Nagpur, India",        "lat": 21.1458, "lon": 79.0882, "tz": "Asia/Kolkata"},
    # --- Indian Business ---
    {"slug": "mukesh-ambani",       "name": "Mukesh Ambani",       "category": "business",   "dob": "1957-04-19", "tob": "06:00", "pob": "Aden, Yemen",          "lat": 12.7855, "lon": 45.0187, "tz": "Asia/Aden"},
    {"slug": "ratan-tata",          "name": "Ratan Tata",          "category": "business",   "dob": "1937-12-28", "tob": "06:30", "pob": "Mumbai, India",        "lat": 19.0760, "lon": 72.8777, "tz": "Asia/Kolkata"},
    # --- Global ---
    {"slug": "elon-musk",           "name": "Elon Musk",           "category": "global",     "dob": "1971-06-28", "tob": "07:30", "pob": "Pretoria, South Africa","lat": -25.7479,"lon": 28.2293, "tz": "Africa/Johannesburg"},
    {"slug": "taylor-swift",        "name": "Taylor Swift",        "category": "global",     "dob": "1989-12-13", "tob": "05:17", "pob": "West Reading, USA",    "lat": 40.3362, "lon": -75.9471,"tz": "America/New_York"},
    {"slug": "cristiano-ronaldo",   "name": "Cristiano Ronaldo",   "category": "global",     "dob": "1985-02-05", "tob": "05:25", "pob": "Funchal, Portugal",    "lat": 32.6669, "lon": -16.9241,"tz": "Atlantic/Madeira"},
    # --- Spiritual ---
    {"slug": "sadhguru",            "name": "Sadhguru",            "category": "spiritual",  "dob": "1957-09-03", "tob": "09:00", "pob": "Mysore, India",        "lat": 12.2958, "lon": 76.6394, "tz": "Asia/Kolkata"},
    {"slug": "baba-ramdev",         "name": "Baba Ramdev",         "category": "spiritual",  "dob": "1965-12-25", "tob": "06:00", "pob": "Mahendragarh, India",  "lat": 28.2780, "lon": 76.1514, "tz": "Asia/Kolkata"},
    # --- Historical ---
    {"slug": "mahatma-gandhi",      "name": "Mahatma Gandhi",      "category": "historical", "dob": "1869-10-02", "tob": "07:35", "pob": "Porbandar, India",     "lat": 21.6417, "lon": 69.6293, "tz": "Asia/Kolkata"},
    {"slug": "jawaharlal-nehru",    "name": "Jawaharlal Nehru",    "category": "historical", "dob": "1889-11-14", "tob": "23:15", "pob": "Allahabad, India",     "lat": 25.4358, "lon": 81.8463, "tz": "Asia/Kolkata"},
    {"slug": "subhas-chandra-bose", "name": "Subhas Chandra Bose", "category": "historical", "dob": "1897-01-23", "tob": "12:15", "pob": "Cuttack, India",       "lat": 20.4625, "lon": 85.8830, "tz": "Asia/Kolkata"},
]
```

---

## Backend Endpoints

### 1. Celebrity list
```
GET /api/celebrities
Returns: list of all celebrities with slug, name, category (no chart data)
```

### 2. Celebrity chart
```
GET /api/celebrities/:slug
Returns: celebrity metadata + computed birth chart
```

The chart is computed by calling `vedic_calculator.py` functions with the celebrity's DOB/TOB/location. Cache the result in MongoDB (`celebrities` collection) on first request.

**⚠️ All chart calculations must use `vedic_calculator.py`. Do NOT add chart calculation logic anywhere else.**

```python
@api_router.get("/celebrities/{slug}")
async def get_celebrity_chart(slug: str):
    # 1. Find celebrity in CELEBRITY_DATA by slug
    # 2. Check MongoDB cache: db.celebrities.find_one({"slug": slug})
    # 3. If cached, return cached chart
    # 4. If not cached, compute chart using vedic_calculator functions
    # 5. Store in MongoDB, return result
```

---

## Hub Page UI (`/celebrity-horoscopes`)

```
[Page header: "Celebrity Horoscopes -- Vedic Birth Charts of the Famous"]
[Subtitle: "Explore the Vedic birth charts of celebrities, leaders, and legends"]

[Category filter tabs]
  └── All | Bollywood | Cricket | Politics | Business | Spiritual | Historical | Global

[Celebrity grid -- 3-4 columns]
  └── Each card:
       ├── Name (large)
       ├── Category badge
       ├── DOB
       ├── "Born: {place}"
       └── [View Chart →] → /celebrity-horoscopes/{slug}

[Bottom CTA]
  └── "Discover your own Vedic birth chart" → /birth-chart
```

---

## Individual Celebrity Page UI (`/celebrity-horoscopes/:slug`)

```
[Breadcrumb: Celebrity Horoscopes / {Name}]

[Hero: Name + DOB + Place of Birth]

[Chart Summary card -- GlassCard]
  ├── Lagna (Ascendant): {sign}
  ├── Moon Sign (Rashi): {sign}
  ├── Sun Sign: {sign}
  ├── Nakshatra: {nakshatra} Pada {N}
  └── Current Mahadasha: {planet} ({period})

[Key Planetary Positions -- GlassCard]
  └── Simple table: Planet | Sign | House | Status

[Dasha Timeline -- compact]
  └── Life timeline bar showing major Mahadasha periods

[Notable Yogas -- GlassCard]
  └── List of significant yogas present in the chart (from vedic_calculator)

[Interpretation note]
  └── "This chart is computed using Vedic astrology (KP Ayanamsha, Placidus houses).
       Time of birth accuracy affects house positions."

[Upsell CTA]
  ├── "Get your own birth chart -- personalised, not famous"
  └── [Generate My Birth Chart] → /birth-chart

[Back: ← All Celebrity Charts] → /celebrity-horoscopes
```

---

## SEO Requirements

### Hub page
- **Title:** `Celebrity Horoscopes -- Vedic Birth Charts | EverydayHoroscope`
- **Description:** `Explore Vedic birth charts of Bollywood stars, cricketers, politicians, and global icons. Calculated with KP Jyotish -- Moon sign, Dasha, Nakshatra, and more.`

### Individual pages
- **Title:** `{Name} Birth Chart -- Vedic Horoscope & Kundali | EverydayHoroscope`
- **Description:** `{Name}'s Vedic birth chart -- Moon sign {sign}, Lagna {sign}, {nakshatra} Nakshatra. Full Kundali analysis with Dasha timeline.`
- **JSON-LD:** `@type: "Person"` with `birthDate`, `birthPlace`, `name`

---

## Visual Spec

- Celebrity cards: GlassCard, hover effect: `border-gold/40` + slight lift
- Category badges: colour-coded (Bollywood=pink, Cricket=blue, Politics=amber, etc.)
- Chart summary: gold-bordered GlassCard with data in 2-column grid
- Planet table: alternating `bg-gold/[0.02]` rows
- No custom CSS -- Tailwind only

---

## ⚠️ Critical Notes

1. **All chart calculations from `vedic_calculator.py`** -- not from any new file
2. **Cache in MongoDB** -- computing charts is expensive; cache on first request, never recompute
3. **TOB "00:00"** = unknown time of birth; in this case, skip Lagna calculation and note "Lagna unknown -- TOB not confirmed"
4. **Do NOT add calculation functions anywhere other than `vedic_calculator.py`**
5. **Smart quote fix** on both `.jsx` files
6. **Lazy load** both components

---

## Acceptance Criteria

- [ ] `/celebrity-horoscopes` loads with 20 celebrities in grid
- [ ] Category filter tabs work
- [ ] Each celebrity page loads with chart data
- [ ] Charts use `vedic_calculator.py` (no new calculation code)
- [ ] First load may be slow (computing), subsequent loads instant (MongoDB cache)
- [ ] Hub: `<title>` + `<meta description>` correct
- [ ] Individual pages: unique `<title>` + `<meta description>` + Person JSON-LD
- [ ] Build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
