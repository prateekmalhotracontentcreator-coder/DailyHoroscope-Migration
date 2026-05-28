# Commission Brief: SEO-B3 -- Festival Calendar Hub + Hora Today + Indian Calendar

**Commission ID:** SEO-B3  
**Track:** B -- Codex Content Pages  
**Priority:** Tier 1 -- Phase 2 (after Track A + SEO-C1)  
**Date:** 2026-05-20  
**Status:** READY TO ISSUE  

---

## What to Build

Three tightly related utility/hub pages -- commission as one brief:

| Page | Route | Purpose |
|---|---|---|
| Festival Calendar Hub | `/festivals` | Master hub listing all festivals by month; links to individual festival pages |
| Indian Calendar | `/calendar` | Monthly view with festivals, auspicious days, Tithi per day |
| Hora Today | `/hora` | Today's Hora schedule (planetary hours), similar to Choghadiya tab in Panchang |

All three are recurring-visit utility pages with high-volume India SEO traffic.

---

## Files to Create

### Frontend
- `frontend/src/pages/festivals/FestivalsHubPage.jsx`
- `frontend/src/pages/calendar/IndianCalendarPage.jsx`
- `frontend/src/pages/hora/HoraTodayPage.jsx`

### Backend
- No new routers needed -- all data comes from existing `panchang_router.py` endpoints (details below)

---

## Route Wiring (App.js additions)

```jsx
import { FestivalsHubPage }    from './pages/festivals/FestivalsHubPage';
import { IndianCalendarPage }  from './pages/calendar/IndianCalendarPage';
import { HoraTodayPage }       from './pages/hora/HoraTodayPage';

// Add inside <Routes>:
<Route path="/festivals"           element={<FestivalsHubPage />} />
<Route path="/calendar"            element={<IndianCalendarPage />} />
<Route path="/calendar/:year/:month" element={<IndianCalendarPage />} />
<Route path="/hora"                element={<HoraTodayPage />} />
```

---

## Page 1: Festival Calendar Hub (`/festivals`)

### Data source
```
GET /api/panchang/festivals?year={YYYY}
```
Existing endpoint -- returns festival list for the year.

### UI Layout
```
[Page header: "Hindu Festival Calendar {Year}"]
[Year navigator: ← 2025 | 2026 | 2027 →]
[Month-by-month accordion/grid]
  ├── Each month = card listing festivals that month
  │     ├── Festival name (linked to /festivals/{slug} -- future SEO-B2 page)
  │     ├── Date + day of week
  │     ├── Tithi + type badge (Festival / Vrat / Observance)
  └── "View full Panchang for this day" link → /panchang/date/{YYYY-MM-DD}
[Bottom CTA: "Get Panchang for any date" → /panchang]
```

### SEO
- Title: `Hindu Festival Calendar 2026 -- Dates, Panchang & Muhurat | EverydayHoroscope`
- Description: `Complete Hindu festival calendar for 2026. Dates for Holi, Diwali, Navratri, Ekadashi, Purnima and all major Indian festivals with Panchang details.`
- JSON-LD: `@type: "ItemList"` -- each festival is a `ListItem`

---

## Page 2: Indian Calendar (`/calendar` and `/calendar/:year/:month`)

### Data source
```
GET /api/panchang/calendar/{year}/{month}
```
Existing endpoint -- returns monthly Panchang calendar data (Tithi per day, festivals, etc.)

Default: current year + month. Year/month from URL params if provided.

### UI Layout
```
[Page header: "Indian Calendar -- {Month} {Year}"]
[Month navigator: ← April | May 2026 | June →]
[Calendar grid -- 7-column (Sun-Sat)]
  ├── Each cell:
  │     ├── Gregorian date (large)
  │     ├── Tithi name (small, below date)
  │     └── Festival dot/badge if festival that day
[Below calendar: Festival list for the month with dates]
[Panchang quick-link: "View full Panchang for today" → /panchang]
```

### SEO
- Title: `Indian Calendar {Month} {Year} -- Tithi, Festivals & Panchang | EverydayHoroscope`
- Description: `Indian calendar for {Month} {Year} with daily Tithi, Hindu festivals, Ekadashi, Purnima and auspicious dates. Powered by Vedic Panchang.`
- JSON-LD: `@type: "Event"` array for festivals in the month

---

## Page 3: Hora Today (`/hora`)

### What is Hora?
Hora = planetary hours. Each day is divided into 24 equal hours, each ruled by a planet in sequence. Used in Vedic astrology to determine auspicious timing for activities.

### Data source
The existing Panchang engine already computes Choghadiya (similar concept). For Hora:

**Backend calculation needed** -- add a function to `panchang_router.py`:

```python
def compute_hora_schedule(sunrise: datetime, sunset: datetime, date: date) -> list[dict]:
    """
    Compute 24 Hora periods for a given day.
    Day Hora = 12 equal slots between sunrise and sunset
    Night Hora = 12 equal slots between sunset and next sunrise
    Planet order starts from the day ruler:
    Sun=Sun, Mon=Moon, Tue=Mars, Wed=Mercury, Thu=Jupiter, Fri=Venus, Sat=Saturn
    Sequence: Sun, Venus, Mercury, Moon, Saturn, Jupiter, Mars (then repeat)
    """
```

**New API endpoint** -- add to `panchang_router.py`:
```
GET /api/panchang/hora?date=YYYY-MM-DD&location_slug=xxx
```

Returns list of 24 Hora periods: `[{ planet, start_time, end_time, quality, period (day/night) }]`

Hora quality mapping:
```python
HORA_QUALITY = {
    'Sun':     'Power & Authority',
    'Moon':    'Mind & Emotions',
    'Mars':    'Energy & Action',
    'Mercury': 'Communication & Trade',
    'Jupiter': 'Wisdom & Expansion',
    'Venus':   'Love & Creativity',
    'Saturn':  'Discipline & Labour',
}
```

### UI Layout
```
[Page header: "Hora Today -- Planetary Hours"]
[Current Hora highlight card -- "Now: Jupiter Hora -- Wisdom & Expansion (ends 14:32)"]
[Location picker -- reuse existing Panchang location picker]
[Day Horas: 12-row table -- Planet | Start | End | Quality | Active indicator]
[Divider: Sunset -- Night begins]
[Night Horas: 12-row table -- Planet | Start | End | Quality]
[Info card: "What is Hora?" -- brief explanation]
[Link: "View today's full Panchang" → /panchang]
```

### SEO
- Title: `Hora Today -- Planetary Hours Schedule | EverydayHoroscope`
- Description: `Today's Hora schedule with all 24 planetary hours. Find the most auspicious time for your activities using Vedic Hora timing.`
- JSON-LD: `@type: "WebPage"` with `datePublished` = today

---

## Visual Spec (all 3 pages)

- GlassCard pattern: `rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`
- Gold accent tokens: `text-gold`, `border-gold`, `bg-gold/15`
- Festival badges: color-coded by type:
  - Festival → `bg-orange-500/15 text-orange-400 border-orange-400/30`
  - Vrat → `bg-purple-500/15 text-purple-400 border-purple-400/30`
  - Observance → `bg-sky-500/15 text-sky-400 border-sky-400/30`
- Hora planet badges: planet-specific color (Sun=amber, Moon=slate, Mars=red, Mercury=green, Jupiter=gold, Venus=pink, Saturn=indigo)
- "Now" indicator: pulsing gold dot (same as Panchang timing windows)
- No custom CSS -- Tailwind only

---

## Upsell Hooks

### Festival Hub
- Each festival entry: "Plan your Puja -- Check Muhurat" → `/panchang`
- Bottom: "Get personalised auspicious timing for your events" → `/birth-chart`

### Indian Calendar
- "See full Panchang for [festival name]" → `/panchang/date/{YYYY-MM-DD}`
- Sidebar: "Your Personalised Auspicious Calendar -- Premium" → `/pricing`

### Hora Today
- "Find the best Hora for your business launch / travel / investment"
- CTA: "Get personalised timing based on your birth chart" → `/birth-chart`

---

## ⚠️ Critical Notes

1. **All data from existing Panchang backend** -- `panchang_router.py` is the sole data source
2. **Hora backend function** -- must be added to `panchang_router.py`, NOT a new file
3. **Do NOT add astronomical calculation libraries** -- use existing `pyswisseph` functions already in `panchang_router.py` for Hora sunrise/sunset times
4. **Location picker** -- Hora page must reuse the same 318-city catalogue used by Panchang (`GET /api/panchang/locations`)
5. **Default location** -- use `localStorage.getItem('selectedCity')` (same key as Panchang page) for persistence
6. **Smart quote fix** -- run on all 3 new `.jsx` files before handing over
7. **Lazy load** -- all 3 components can be lazy-loaded

---

## Acceptance Criteria

- [ ] `/festivals` loads with festival list grouped by month
- [ ] `/calendar` loads with current month grid + Tithi per cell
- [ ] `/calendar/:year/:month` loads correct month on navigation
- [ ] `/hora` loads today's 24 Hora periods with current Hora highlighted
- [ ] Hora location picker works and persists to localStorage
- [ ] All 3 pages have unique `<title>`, `<meta description>`, JSON-LD
- [ ] Festival links point to `/festivals/{slug}` (even if those pages don't exist yet -- they will be built in SEO-B2)
- [ ] No console errors
- [ ] Build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
