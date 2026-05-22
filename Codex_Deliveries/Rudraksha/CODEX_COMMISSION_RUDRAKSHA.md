# RUD-1 Commission Brief
> Thread: Rudraksha Codex Thread  
> Module: Rudraksha Hub + Calculator  
> Pages: 21 mukhi pages + hub + calculator = ~25 pages  
> Date: 2026-05-23  
> Status: READY TO BUILD -- all engines available, no dependencies

---

## Context

EverydayHoroscope (`everydayhoroscope.in`) is a live React 18 + FastAPI + MongoDB + Tailwind CSS platform. This commission adds the Rudraksha module -- a hub covering all 21 mukhis, a birth-chart-powered Rudraksha recommendation calculator, and individual mukhi detail pages.

**Repo:** `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`  
**Stack:** React 18 · FastAPI · MongoDB · Tailwind CSS  
**Internal engine:** `backend/vedic_calculator.py` -- ALL birth-chart calculations. Do NOT add chart logic to any other file.

**Source material (do not copy -- use as reference for Codex-written original content):**
- `Rudraksha-Revealed-1-Mukhi-21-Mukhi.pdf` (compressed) -- covers each mukhi: ruling deity, ruling planet, benefits, wearing instructions, cautions

All content must be **original Codex writing** inspired by Rudraksha/Vedic traditions -- not reproduced from the source PDF. Copyright compliance is mandatory: no direct quotes, no paragraph reproduction.

---

## Module Architecture

### URL Patterns

| URL | Purpose |
|---|---|
| `/rudraksha/` | Hub page -- what is Rudraksha, mukhi grid, calculator entry |
| `/rudraksha/{N}-mukhi/` | Individual mukhi detail page (1-mukhi through 21-mukhi) |
| `/rudraksha/calculator/` | Birth-chart Rudraksha recommendation calculator |

**Total pages:** 1 hub + 21 mukhi pages + 1 calculator page = **23 pages**

---

## Backend

### Router File
`backend/rudraksha_router.py`

Register in `backend/server.py` as: `app.include_router(rudraksha_router, prefix="/api")`

### Endpoints

```
GET  /api/rudraksha/mukhis                    → list of all 21 mukhis (from MongoDB)
GET  /api/rudraksha/mukhi/{n}                 → single mukhi detail
POST /api/rudraksha/calculator                → accepts birth data → returns recommendations
GET  /api/seo/sitemap/rudraksha               → sitemap URLs list
```

### Calculator Logic (`POST /api/rudraksha/calculator`)

**Input:**
```json
{
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "place": "city name or lat/lon"
}
```

**Processing (all via `vedic_calculator.py` -- do NOT reimplement):**
1. Call `vedic_calculator.py` functions to get birth chart data: Lagna (ascendant sign), Moon sign, current Mahadasha planet, Atmakaraka planet, weakest house lord (6th, 8th, 12th lords strength check)
2. Apply Rudraksha recommendation rules (hardcoded mapping -- see table below)

**Recommendation rules (hardcoded in `rudraksha_router.py`):**

| Trigger condition | Recommended Mukhi(s) |
|---|---|
| Sun weak or Mahadasha = Sun | 1-Mukhi, 12-Mukhi |
| Moon weak or Mahadasha = Moon | 2-Mukhi |
| Mars weak or Mahadasha = Mars | 3-Mukhi |
| Mercury weak or Mahadasha = Mercury | 4-Mukhi |
| Jupiter weak or Mahadasha = Jupiter | 5-Mukhi |
| Venus weak or Mahadasha = Venus | 6-Mukhi |
| Saturn weak or Mahadasha = Saturn | 7-Mukhi, 14-Mukhi |
| Rahu Mahadasha or Lagna = Aquarius | 8-Mukhi |
| Ketu Mahadasha or Lagna = Scorpio | 9-Mukhi |
| General balance / health | 5-Mukhi (universal) |
| Lagna lord weakly placed | Mukhi corresponding to Lagna lord planet |

"Weak" = planet in debilitation sign, or in 6th/8th/12th house from Lagna with no aspect support. Use `vedic_calculator.py` planet position data to determine.

**Output:**
```json
{
  "primary": { "mukhi": 5, "reason": "Jupiter Mahadasha active -- 5-Mukhi strengthens Jupiter energy" },
  "secondary": [
    { "mukhi": 7, "reason": "Saturn rules your 7th and 8th house -- 7-Mukhi provides protection" }
  ],
  "universal": { "mukhi": 5, "note": "5-Mukhi is always beneficial as a base" },
  "wearing_day": "Thursday",
  "mantra": "Om Hreem Namah"
}
```

### MongoDB Collection: `rudraksha_mukhis`
21 documents -- one per mukhi. Pre-seeded at build time.

```json
{
  "mukhi": 1,
  "name": "Ek Mukhi Rudraksha",
  "slug": "1-mukhi",
  "ruling_deity": "Shiva",
  "ruling_planet": "Sun",
  "benefits": ["clarity", "leadership", "spiritual awakening", "confidence", "solar energy"],
  "wearing_instructions": {
    "day": "Sunday",
    "metal": "Gold or copper",
    "mantra": "Om Hreem Namah",
    "finger": "Right hand index finger or worn as pendant"
  },
  "cautions": ["Not recommended for those with very weak Mars without proper guidance"],
  "best_for": ["Government jobs", "Leadership roles", "Eye-related health issues", "Meditation practitioners"],
  "rarity": "Extremely rare -- most common in Nepal",
  "price_range": "High",
  "faq": [
    { "q": "Who should wear 1 Mukhi Rudraksha?", "a": "..." },
    { "q": "What are the benefits of 1 Mukhi Rudraksha?", "a": "..." },
    { "q": "How do I activate 1 Mukhi Rudraksha?", "a": "..." },
    { "q": "Can anyone wear 1 Mukhi Rudraksha?", "a": "..." },
    { "q": "What is the difference between round and half-moon 1 Mukhi?", "a": "..." }
  ],
  "meta_title": "1 Mukhi Rudraksha -- Benefits, Who Should Wear & How to Activate | EverydayHoroscope",
  "meta_description": "1 Mukhi Rudraksha is ruled by the Sun -- the rarest of all Rudrakshas. Discover its benefits, who should wear it, activation mantra, and wearing instructions."
}
```

### Seed Script
`backend/scripts/seed_rudraksha.py`

Seeds all 21 mukhi documents. All content is Codex-authored -- not copied from source PDF.

---

## Frontend

### Hub Page
**File:** `frontend/src/pages/rudraksha/RudrakshaHubPage.jsx`

**Page content:**
- H1: `Rudraksha -- Sacred Beads for Healing, Protection & Vedic Guidance`
- Intro: What is Rudraksha? What are mukhis? (3-4 sentences, original)
- **Mukhi grid:** 21 GlassCards -- each showing mukhi number (Cinzel, large), ruling planet, 1-line benefit summary, "Learn More" link
- **Calculator CTA section:** Gold card -- "Find Your Rudraksha" -- 1-sentence description + button → `/rudraksha/calculator/`
- **How to wear:** 4-step summary (Cleanse → Energise → Mantra → Wear)
- **FAQ accordion:** 5 questions (What is Rudraksha? How many mukhis are there? Can I wear multiple? etc.)
- JSON-LD: `FAQPage` + `BreadcrumbList`
- SEO: Title: `Rudraksha -- All 21 Mukhis, Benefits & Calculator | EverydayHoroscope` · Description: `Explore all 21 Rudraksha mukhis -- ruling planets, benefits, and wearing instructions. Use our Vedic calculator to find which Rudraksha suits your birth chart.`

### Mukhi Detail Page
**File:** `frontend/src/pages/rudraksha/RudrakshaMukhiPage.jsx`

**Page content:**
- H1: `{N} Mukhi Rudraksha -- Benefits, Who Should Wear & Mantra`
- **Planet + deity badge:** Pill chips (Ruling Planet: Sun | Ruling Deity: Shiva)
- **Benefits:** 5-6 bullets from `benefits[]`
- **Best for:** 3-4 use-case pills
- **Wearing instructions table:** Day / Metal / Mantra / How to wear -- 4-row table in GlassCard
- **Cautions:** 2-3 bullets
- **Activation guide:** Step-by-step short list (Cleanse / Energise / Mantra / Wear)
- **Rarity + price band:** 1-line info chip
- **FAQ accordion:** 5 questions (from MongoDB)
- **Related mukhis:** 3 cards -- same ruling planet or complementary
- **CTA:** "Find your ideal Rudraksha" → `/rudraksha/calculator/`
- JSON-LD: `FAQPage` + `Article`

### Calculator Page
**File:** `frontend/src/pages/rudraksha/RudrakshaCalculatorPage.jsx`

**Page content:**
- H1: `Rudraksha Calculator -- Find Your Ideal Bead from Your Birth Chart`
- Brief intro: How the calculator works (2 sentences -- uses Vedic chart data)
- **Form:**
  - Date of birth (date picker)
  - Time of birth (time picker, with "I don't know my birth time" option -- defaults to noon)
  - Place of birth (text input with typeahead from existing location catalogue)
  - Submit button: "Calculate My Rudraksha"
- **Results panel (shown after API call):**
  - Primary recommendation: Large GlassCard -- mukhi number (Cinzel), reason, wearing instructions
  - Secondary recommendations: 2-3 smaller cards
  - Universal base: 5-Mukhi note
  - "Learn more about {N} Mukhi" links → mukhi detail pages
- **Disclaimer:** "This recommendation is based on Vedic astrology principles and is for spiritual guidance only."
- No auth gate -- accessible to all users. Results encourage sign-up for deeper birth chart reading.
- JSON-LD: `FAQPage`

---

## SEO Metadata Formulas

### Hub
- **Title:** `Rudraksha -- All 21 Mukhis, Benefits & Calculator | EverydayHoroscope`
- **Description:** `Explore all 21 Rudraksha mukhis -- ruling planets, benefits, and wearing instructions. Use our Vedic calculator to find which Rudraksha suits your birth chart.`

### Mukhi Detail Page
- **Title:** `{N} Mukhi Rudraksha -- Benefits, Mantra & Who Should Wear | EverydayHoroscope`
- **Description:** `{N} Mukhi Rudraksha is ruled by {Planet}. Discover its benefits, who should wear it, the activation mantra, and step-by-step wearing instructions.`

### Calculator Page
- **Title:** `Rudraksha Calculator -- Find Your Ideal Bead from Your Birth Chart | EverydayHoroscope`
- **Description:** `Enter your birth details and get a personalised Rudraksha recommendation based on your Vedic birth chart. Find the mukhi that strengthens your chart's weakest point.`

---

## Routes (App.js additions)

```jsx
<Route path="/rudraksha" element={<RudrakshaHubPage />} />
<Route path="/rudraksha/calculator" element={<RudrakshaCalculatorPage />} />
<Route path="/rudraksha/:mukhi" element={<RudrakshaMukhiPage />} />
```

All routes: public, no auth gate.

---

## Sitemap

Add to `backend/seo_router.py`:
```python
GET /api/seo/sitemap/rudraksha   # 23 URLs (hub + 21 mukhis + calculator)
```

Add to `frontend/public/sitemap-index.xml`.

---

## Technical Requirements

- New React pages in `frontend/src/pages/rudraksha/` (new subdirectory)
- New FastAPI router: `backend/rudraksha_router.py`
- Register router in `backend/server.py`
- New routes in `frontend/src/App.js` (public, no auth gate)
- Sitemap endpoint added to `backend/seo_router.py`
- Cache headers in `frontend/vercel.json` (s-maxage=86400) for `/rudraksha/*`
- MongoDB seed script: `backend/scripts/seed_rudraksha.py`
- `SEO` component from `frontend/src/components/SEO.jsx` on every page
- **Calculator ONLY:** POST to `/api/rudraksha/calculator` -- calls `vedic_calculator.py` for chart data. No calculation logic inside `rudraksha_router.py` itself beyond the recommendation mapping table.

**Tailwind / theme:** GlassCard pattern (`rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`). Gold accent `#c5a059`. No new dependencies.

**Build verification:** `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` -- must pass clean.

---

## Acceptance Checklist

- [ ] Hub page renders at `/rudraksha/`
- [ ] 21 mukhi detail pages render at `/rudraksha/{N}-mukhi/`
- [ ] Calculator page renders at `/rudraksha/calculator/`
- [ ] Calculator POST returns valid recommendation JSON for a test birth input
- [ ] Calculator calls `vedic_calculator.py` -- no duplicate chart logic in router
- [ ] Sitemap endpoint returns 23 URLs
- [ ] Routes wired in App.js -- all pages HTTP 200
- [ ] Vercel cache headers applied to `/rudraksha/*`
- [ ] MongoDB seed script seeds all 21 mukhi documents
- [ ] Build clean -- zero errors
- [ ] JSON-LD present on all page types
- [ ] SEO meta title/description applied on all pages
- [ ] No direct quotes from source PDF -- all content is original Codex writing
