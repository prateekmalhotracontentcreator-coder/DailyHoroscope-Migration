# Contract: Lagna Kundli (Birth Chart) Module
> Client: EverydayHoroscope (SkyHound Studios)
> Platform: https://www.everydayhoroscope.in
> Backend: FastAPI on Render · Frontend: React 18 on Vercel
> Repo: github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration
> Astronomy Engine: pyswisseph 2.10.x (Lahiri ayanamsa, Swiss Ephemeris)

---

## 1. Module Overview

Build a complete **Lagna Kundli (Vedic Birth Chart)** module with:
1. Birth details input form
2. North Indian diamond-style chart SVG renderer (client-side)
3. Planet positions table with degrees & rashi
4. House (Bhava) summary
5. Dasha periods (Vimshottari) timeline
6. Optional: Navamsa (D9) chart
7. Full SEO on all sub-routes

The backend `vedic_calculator.py` is **already committed** and computing birth charts via pyswisseph. The contract is to build the API endpoints + frontend UI on top of it.

---

## 2. Existing Backend

File: `backend/vedic_calculator.py`

Already computes:
- Planet longitudes (sidereal, Lahiri)
- Lagna (Ascendant) degree & rashi
- House (Bhava) cusps
- Nakshatra for each planet
- Navamsa (D9) positions
- Vimshottari Dasha periods

Currently **not exposed via API** -- needs a router added.

---

## 3. Backend Deliverables

### 3a. New router file: `backend/kundali_router.py`

Register at prefix `/api/kundali` in `backend/main.py`.

#### Endpoint 1 -- Compute Kundali
```
POST /api/kundali/compute
```
Request body:
```json
{
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "timezone": "Asia/Kolkata",
  "city_name": "New Delhi"
}
```
Response (see Section 5 for full schema).

#### Endpoint 2 -- Save Kundali (auth required)
```
POST /api/kundali/save
```
Saves computed kundali to Supabase for the logged-in user.

#### Endpoint 3 -- Get saved Kundalis
```
GET /api/kundali/my-charts
```
Returns list of saved charts for the logged-in user.

#### Endpoint 4 -- Today's Lagna (no birth data needed)
```
GET /api/kundali/lagna-now?location_slug=new-delhi-india
```
Computes the current Lagna (ascendant) for the given location and current time.
Used in the Panchang page hero section.
Response: `{ "lagna_rashi": "Vrishabha", "lagna_degree": 14.7, "lagna_nakshatra": "Rohini", "computed_at": "2026-03-26T06:18:00+05:30" }`

---

## 4. Frontend Deliverables

### File: `frontend/src/pages/KundaliPage.jsx` (replace existing placeholder)

#### 4a. Birth Details Form
Fields:
- Date of birth (date picker)
- Time of birth (time picker, 12hr format)
- City/place (searchable dropdown -- use the same 91-city list from Panchang, PLUS a free-text fallback with lat/lng)
- "I don't know my birth time" checkbox → uses 12:00 noon as fallback, shows a note

UX:
- Clean card layout, same gold design system as rest of app
- Validation: date required, time optional (with disclaimer), city required
- Submit button: "Generate My Kundali"

#### 4b. North Indian Chart SVG Renderer
Build a pure React SVG component `NorthIndianChart` that renders the classic diamond layout:

```
North Indian Chart Layout (12 houses, diamond arrangement):
┌─────────┬─────────┬─────────┐
│  Hs 12  │  Hs 1   │  Hs 2   │
├─────────┼─────────┼─────────┤
│  Hs 11  │  ////// │  Hs 3   │
├─────────┼─────────┼─────────┤
│  Hs 10  │  Hs 9   │  Hs 4   │
└─────────┴─────────┴─────────┘
         plus 4 corner triangles:
         Hs 5 (top-left inner triangle),
         Hs 6 (top-right),
         Hs 7 (bottom-right),
         Hs 8 (bottom-left)
```

More precisely, it's a 3x3 grid where:
- Corner cells = triangles formed by diagonal lines
- Each cell shows: Rashi number (1-12), Rashi symbol/name, planet abbreviations

Component props: `{ houses: HouseData[], planets: PlanetData[], size: number }`

Requirements:
- Pure SVG, no canvas, no external chart library
- Responsive: `viewBox="0 0 400 400"` with `width="100%"`
- Planet abbreviations: Su (Sun), Mo (Moon), Ma (Mars), Me (Mercury), Ju (Jupiter), Ve (Venus), Sa (Saturn), Ra (Rahu), Ke (Ketu)
- Rashi numbers shown in each cell (1=Aries, 2=Taurus ... 12=Pisces)
- Planets shown as small text inside their house cell
- Lagna marked with "Lg" or an arrow
- Colors: gold borders (`#C5A059`), cream background (`#FEFCF7`), dark text

#### 4c. Planet Positions Table
Responsive table:
| Planet | Rashi | Degree | Nakshatra | Pada | R/D |
|--------|-------|--------|-----------|------|-----|
(R = Retrograde, D = Direct)

- Each planet row has a color-coded circle (traditional planet colors)
- Retrograde planets shown with ℞ symbol in red
- Functional lords (exalted/debilitated/own sign) shown as badge

#### 4d. Vimshottari Dasha Timeline
Visual timeline showing:
- Current Maha Dasha (major period) with planet name and remaining time
- Sub-dashas (Antar Dasha) for current Maha Dasha as a horizontal bar
- Each period bar colored by planet
- "You are here" indicator on current period
- Next 3 Maha Dashas listed below

#### 4e. Navamsa (D9) Chart
Same `NorthIndianChart` component reused, smaller size.
Toggle button to show/hide: "Show Navamsa Chart (D9)"

#### 4f. Save & Share
- "Save Chart" button (requires login) -- calls `POST /api/kundali/save`
- "Share" button -- generates a shareable URL `/kundali/[chart-id]`
- Public chart view route: `/kundali/view/:chartId`

---

## 5. API Response Schema

```json
{
  "chart_id": "uuid",
  "input": {
    "date": "1990-06-15",
    "time": "14:30",
    "city": "Mumbai, India",
    "latitude": 19.076,
    "longitude": 72.8777,
    "timezone": "Asia/Kolkata"
  },
  "lagna": {
    "rashi": "Tula",
    "rashi_num": 7,
    "degree": 14.73,
    "nakshatra": "Swati",
    "pada": 2
  },
  "planets": [
    {
      "name": "Sun",
      "abbr": "Su",
      "rashi": "Mithuna",
      "rashi_num": 3,
      "degree": 1.45,
      "nakshatra": "Mrigashira",
      "pada": 3,
      "retrograde": false,
      "house": 9,
      "dignity": "neutral"
    }
    // ... all 9 grahas + Rahu/Ketu
  ],
  "houses": [
    { "house_num": 1, "rashi": "Tula", "rashi_num": 7, "lord": "Venus" }
    // ... all 12 houses
  ],
  "navamsa_planets": [ /* same structure as planets */ ],
  "dasha": {
    "current_maha": { "planet": "Jupiter", "start": "2020-03-15", "end": "2036-03-15" },
    "current_antar": { "planet": "Saturn", "start": "2025-06-01", "end": "2027-12-15" },
    "all_maha": [ /* list of all 9 maha dashas with dates */ ]
  },
  "meta": {
    "ayanamsa": "Lahiri",
    "ayanamsa_value": 24.11,
    "engine": "pyswisseph-2.10.x",
    "computed_at": "2026-03-26T10:00:00Z"
  }
}
```

---

## 6. SEO Requirements

Routes:
- `/kundali` -- main input form
- `/kundali/view/:chartId` -- public shared chart

SEO for main page:
- Title: "Free Kundali -- Vedic Birth Chart Online | Everyday Horoscope"
- Description: "Generate your free Kundali (Lagna chart) instantly. North Indian birth chart with planet positions, Dasha periods and Navamsa."
- JSON-LD: `SoftwareApplication` schema

---

## 7. Design Reference

Follow the gold/cream design system used throughout the app:
- Primary gold: `#C5A059` (Tailwind class: `text-gold`, `bg-gold`)
- Card style: `border border-border rounded-xl p-5`
- Heading font: Playfair Display (`font-playfair`)
- Body: Inter/system font

Reference: Drik Panchang's Kundali page layout (North Indian chart format)

---

## 8. Technical Constraints

- Python 3.12, FastAPI, pyswisseph 2.10.x (already in requirements.txt)
- Do NOT add new Python dependencies if avoidable
- React 18, Tailwind CSS -- no new npm packages unless essential
- Chart SVG must render server-side-friendly (no canvas)
- All times stored in UTC, displayed in user's local timezone

---

## 9. Acceptance Criteria

- [ ] Birth chart computes correctly for test case: 15 June 1990, 14:30, Mumbai → Lagna = Tula (Libra) ≈ 14°
- [ ] All 9 planets + Rahu/Ketu shown in correct houses
- [ ] Vimshottari Dasha dates match standard calculation
- [ ] Chart SVG renders without distortion at 320px and 800px width
- [ ] Page loads in < 3s (chart computation < 500ms backend)
- [ ] Works on iOS Safari and Chrome Android

---

## 10. Estimated Effort

| Component | Hours |
|---|---|
| Backend router + `/compute` endpoint | 4h |
| Backend Dasha calculation | 3h |
| North Indian SVG chart component | 6h |
| Planet table + Dasha timeline UI | 4h |
| Birth form + city search | 2h |
| Save/share + public view | 3h |
| SEO + JSON-LD | 1h |
| Testing + QA | 3h |
| **Total** | **~26h** |
