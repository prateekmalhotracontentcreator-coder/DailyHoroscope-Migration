# Commission SEO-20K -- 22,170 Programmatic SEO Pages + Web Performance

> EverydayHoroscope · Stack: FastAPI + React 18 + Tailwind CSS + MongoDB (Motor async) + pyswisseph 2.10.x
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Live app: https://www.everydayhoroscope.in
> Backend API: https://everydayhoroscope-api.onrender.com (Render, Docker)
> Frontend: Vercel (deploy-on-push to main)
> Issued: 2026-05-22
> **Umbrella commission -- deliver in batches per priority order below.**

---

## CRITICAL ENGINEERING CONSTRAINT -- Internal Engines Only

**ALL SEO pages must rely exclusively on internal calculation engines. No paid third-party API calls per page request.**

| Engine | File | What It Computes |
|---|---|---|
| Panchang Engine | `backend/panchang_router.py` | Sunrise/Sunset, Tithi, Nakshatra, Yoga, Karana, Rahu Kaal, Choghadiya, Amrit Kalam, 318 cities |
| Vedic Calculator | `backend/vedic_calculator.py` | Birth chart, Vimshottari Dasha, house lords, planetary positions, Shadbala |
| Swiss Ephemeris | `pyswisseph` (bundled) | All astronomical calculations via `swe.calc_ut`, `swe.rise_trans` |
| MongoDB | Motor async driver | All pre-computed content served from DB -- zero per-request recalculation |

**Batches flagged ⚠️ below require pre-generated content** (written once at build time, stored in MongoDB, served statically -- zero ongoing API cost). This is acceptable. What is NOT acceptable is real-time LLM calls per page load.

---

## Part A -- SEO & Web Performance (Existing SEO-1 Scope)

*Previously commissioned as SEO-1. Merged here for unified delivery.*

### Deliverable: `docs/SEO_WEBPERF_REPORT.md`

#### A1 -- Technical SEO Audit & Fix
- Audit Core Web Vitals (LCP, FID, CLS) via Lighthouse -- document baseline
- Structured data (JSON-LD) optimisation for all existing page types:
  - `HoroscopeReading` schema on Daily/Weekly/Monthly horoscope pages
  - `Dataset` schema on Panchang pages (per city, per date)
  - `Event` schema on Festival pages
  - `FAQPage` schema on Panchang and report landing pages
- Canonical tag enforcement: `<link rel="canonical" href={`https://everydayhoroscope.in${location.pathname}`} />` on all pages
- Sitemap splitting: one sitemap per content type, capped at 1,000 URLs each, referenced from `sitemap-index.xml`

#### A2 -- Dynamic XML Sitemap Generator (FastAPI)
- `GET /api/seo/sitemap/panchang` -- generates URLs for all 318 city × 7 day combinations
- `GET /api/seo/sitemap/horoscope` -- 36 sign × 3 period pages
- `GET /api/seo/sitemap/angel-numbers` -- 9,000 URLs (once Batch 5 is built)
- `GET /api/seo/sitemap/tarot` -- 2,184 URLs (once Batch 6 is built)
- Save output files to `frontend/public/` as static XML on each build

#### A3 -- Performance Optimisation
- Implement Vercel Edge Caching headers on all programmatic pages (`Cache-Control: s-maxage=86400`)
- Lazy load all images below the fold
- Code-split all large React pages (lazy import with Suspense)
- Add `hreflang` tags for en-IN and en-US on key pages

#### A4 -- 30-Day SEO Launch Plan
Write `docs/SEO_30DAY_PLAN.md` covering:
- Week 1: Technical fixes (above)
- Week 2: Content seeding (festival pages, angel number hub, panchang city pages)
- Week 3: Link building triggers (shareable cards, social posting)
- Week 4: GSC + Bing monitoring, keyword ranking baseline

---

## Part B -- 22,170 Programmatic Pages (Priority Order)

### BATCH 1 -- Daily Panchang City Hubs (2,226 pages) 🔴 PRIORITY 1

**Formula:** 318 cities × 7 days (today + 6 days forward)
**Internal engine:** ✅ `panchang_router.py` -- fully computable, zero external cost
**URL pattern:** `/panchang/{city-slug}/{date}/` (e.g., `/panchang/new-delhi/2026-05-22/`)

**Each page includes:**
- Real-time Sunrise, Sunset, Moonrise, Moonset (with seconds)
- Tithi, Nakshatra, Yoga, Karana, Vara with end times
- Rahu Kaal, Yamaganda, Gulika Kaal, Abhijit Muhurta, Dur Muhurta
- Choghadiya (8 day + 8 night slots)
- Special Yogas (Amrit Siddhi, Sarvartha Siddhi, Ravi Yoga)
- Observances (Ekadashi, festivals, etc.)
- Next/Previous day navigation links

**SEO metadata per page:**
- Title: `{City} Panchang Today {Date} -- Tithi, Rahu Kaal & Muhurta | EverydayHoroscope`
- Description: `Accurate daily Panchang for {City} on {Date}. Includes Tithi, Nakshatra, Choghadiya, Rahu Kaal, and all auspicious windows.`
- JSON-LD: `Dataset` schema with `spatialCoverage: {City}`

**Implementation:**
- React route: `/panchang/:citySlug/:date` → `CityPanchangPage.jsx`
- Data source: existing `GET /api/panchang/daily?date={date}&location_slug={slug}`
- Pre-render top 50 cities at build time; remaining 268 on first request + cache

---

### BATCH 2 -- Regional Choghadiya Pages (1,272 pages) 🔴 PRIORITY 1

**Formula:** 318 cities × 4 time elements (Today Day / Today Night / Tomorrow Day / Tomorrow Night)
**Internal engine:** ✅ `panchang_router.py` -- fully computable
**URL pattern:** `/choghadiya/{city-slug}/{period}/` (e.g., `/choghadiya/mumbai/today/`)

**Each page includes:**
- Full 8-slot Choghadiya table for selected period
- Planetary rulers per slot with quality badge (Amrit / Shubh / Labh / Char / Rog / Kaal / Udveg)
- Current slot highlighted with "Now" indicator
- City-specific sunrise/sunset used for slot calculation

**SEO metadata:**
- Title: `{City} Choghadiya Today -- Best Auspicious Hours | EverydayHoroscope`
- Description: `Check today's Choghadiya timings in {City}. Find the best Amrit and Shubh hours for starting new activities.`

---

### BATCH 5 -- Angel Numbers Module (9,000 pages) 🔴 PRIORITY 1

**Formula:** 1,000 base numbers (0-999) × 9 intent vectors
**Internal engine:** ⚠️ Content-based -- NO live calculation required. Pre-generate all 9,000 interpretations in one Codex session. Store in MongoDB collection `angel_number_content`. Serve statically -- zero ongoing API cost.
**URL pattern:** `/angel-number/{number}/{intent}/` (e.g., `/angel-number/444/career/`)

**9 Intent vectors:** `love`, `career`, `money`, `health`, `twin-flame`, `spiritual`, `manifestation`, `warning`, `general`

**Each page includes:**
- Number breakdown (digit sum, repeating pattern analysis)
- Intent-specific interpretation (pre-written, stored in MongoDB)
- Related numbers section (sequential, mirror, reduce)
- CTA: "Get your personal numerology reading"

**Pre-generation task (Codex writes the content corpus):**
- Write 9,000 unique interpretation blocks (avg 150 words each)
- Structure as MongoDB documents: `{ number: int, intent: str, title: str, interpretation: str, related_numbers: [] }`
- Batch insert into `angel_number_content` collection
- FastAPI route: `GET /api/angel-numbers/{number}/{intent}` → reads from MongoDB

**SEO metadata:**
- Title: `Angel Number {number} Meaning for {Intent} -- What It Signifies | EverydayHoroscope`
- Description: `Seeing {number} repeatedly? Discover the spiritual meaning of angel number {number} for {intent} and what your guides are telling you.`

---

### BATCH 6 -- Tarot Spread Matrices (2,184 pages) 🟠 PRIORITY 2

**Formula:** 78 Tarot cards × 28 classic spreads
**Internal engine:** ⚠️ Content-based -- pre-generate card × spread combination meanings. Store in MongoDB `tarot_combination_content`. Serve statically.
**URL pattern:** `/tarot/{card-slug}/{spread-slug}/` (e.g., `/tarot/the-tower/three-card-love/`)

**28 spreads:** Celtic Cross, Three-Card (Love/Career/General/Past-Present-Future), Single Card, Yes-No, Daily Draw, Horseshoe, Relationship, Career Path, Month Ahead, Year Ahead, chakra spread, obstacle spread, decision spread, new moon, full moon, and 13 others (Codex to define the complete 28-spread list)

**Each page includes:**
- Card meaning in isolation
- How this card modifies the spread
- Common combinations with other cards in this spread
- Reversal interpretation
- CTA: "Draw your own {spread} reading now"

**Pre-generation:** 2,184 interpretation documents → MongoDB `tarot_combination_content`

**SEO metadata:**
- Title: `{Card Name} in a {Spread Name} Tarot Reading -- Meaning & Interpretation`
- Description: `What does {Card} mean in a {Spread} reading? Full interpretation for love, career, and life decisions.`

---

### BATCH 3 -- Kundli / Love Matching (1,296 pages) 🟠 PRIORITY 2

**Formula:** 12 Moon Signs × 12 Moon Signs × 9 Ashta-Koota aspects (but present as 144 sign-pair pages with all 9 Koota scores per page)
**Internal engine:** ✅ `vedic_calculator.py` -- Ashta-Koota Gun Milan is fully computable
**URL pattern:** `/compatibility/{sign1}-and-{sign2}/` (e.g., `/compatibility/aries-and-scorpio/`)

**Each page includes:**
- Overall compatibility score (out of 36)
- All 8 Koota scores in a table (Varna, Vashya, Tara, Yoni, Graha Maitri, Gana, Bhakoot, Nadi)
- Strength/weakness narrative per Koota
- Marriage timing recommendations
- CTA: "Get your full 36-attribute Gun Milan report"

**SEO metadata:**
- Title: `{Sign1} and {Sign2} Compatibility -- Marriage Gun Milan Score | EverydayHoroscope`
- Description: `Are {Sign1} and {Sign2} compatible for marriage? View full Ashta-Koota Gun Milan analysis with score out of 36.`

---

### BATCH 9 -- Localized Remedies (1,284 pages) 🟠 PRIORITY 2

**Formula:** 12 planetary afflictions × 107 metro regions
**Internal engine:** ⚠️ Remedy content is static/pre-written. Planetary affliction detection is internal (`vedic_calculator.py`). Store remedy content in MongoDB `remedy_content` (extending existing `spiritual_remedies` collection).
**URL pattern:** `/remedies/{dosha}/{city-slug}/` (e.g., `/remedies/shani-dosha/mumbai/`)

**12 afflictions:** Shani Sade Sati, Manglik Dosha, Pitru Dosha, Kaal Sarp Dosha, Shani Mahadasha, Rahu Mahadasha, Ketu Mahadasha, Guru Chandal Yoga, Grahan Yoga, Nadi Dosha, Gana Dosha, Bhakoot Dosha

**Each page includes:**
- Affliction explanation
- How to detect it in your chart (link to Kundali page)
- City-specific remedy guidance (local temple suggestions, regional practices)
- Gemstone + yantra recommendations
- CTA: "Check your chart for {dosha}"

---

### BATCH 8 -- Global Festival Hubs (300 pages) 🟡 PRIORITY 3

**Formula:** 50 festivals × 6 international regions (India, USA, UK, UAE, Canada, Australia)
**Internal engine:** ✅ `panchang_router.py` -- festival dates + muhurta windows are computed
**URL pattern:** `/festivals/{festival-slug}/{region}/` (e.g., `/festivals/diwali/usa/`)

**SEO metadata:**
- Title: `{Festival} {Year} Date & Puja Timings in {Region} | EverydayHoroscope`
- Description: `Find exact {Festival} date and puja muhurta for {Region} {Year}. Includes Tithi, Nakshatra, and auspicious windows.`

---

### BATCH 4 -- Transit & Dasha Profiles (108 pages) 🟡 PRIORITY 3

**Formula:** 9 planets × 12 target houses
**Internal engine:** ✅ `vedic_calculator.py` -- transit effects fully computable
**URL pattern:** `/transits/{planet}-in-{sign}/` (e.g., `/transits/saturn-in-aquarius/`)

---

### BATCH 10 -- Character Placements (432 pages) 🟡 PRIORITY 3

**Formula:** 12 zodiac signs × 12 dimensions × 3 chart points (Sun/Moon/Rising)
**Internal engine:** ✅ `vedic_calculator.py` -- sign placements fully computable
**URL pattern:** `/traits/{sign}/{placement}/` (e.g., `/traits/scorpio/moon-sign/`)

---

### BATCH 7 -- Lumina Faith Hubs (450 pages) 🟢 PRIORITY 4

**Formula:** 150 Bible verses × 3 transit intersections
**Internal engine:** ⚠️ Bible verse content is static. Transit intersection content pre-generated. Store in MongoDB `faith_hub_content`.
**URL pattern:** `/faith/{verse-id}/{transit}/`
**Note:** Transit calculation (which planet is active) uses internal `panchang_router.py` / `vedic_calculator.py`.

---

## Part C -- Directory Routing (React Router additions)

```
/panchang/:citySlug/:date/          → CityPanchangPage.jsx
/choghadiya/:citySlug/:period/      → ChoghadiyaPage.jsx
/angel-number/:number/:intent/      → AngelNumberPage.jsx
/tarot/:cardSlug/:spreadSlug/       → TarotCombinationPage.jsx
/compatibility/:signPair/           → CompatibilityPage.jsx
/remedies/:dosha/:citySlug/         → RemedyCityPage.jsx
/festivals/:festivalSlug/:region/   → FestivalRegionPage.jsx
/transits/:planet-in-:sign/         → TransitProfilePage.jsx
/traits/:sign/:placement/           → CharacterPlacementPage.jsx
/faith/:verseId/:transit/           → FaithHubPage.jsx
```

---

## Part D -- SEO Infrastructure

### Metadata Builder (Dynamic per page)
All pages inject via `react-helmet-async`:
- `<title>` -- per batch formula above (max 60 chars)
- `<meta name="description">` -- per batch formula (max 155 chars)
- `<link rel="canonical">`
- `<link rel="alternate" hreflang="en-in">` + `<link rel="alternate" hreflang="en-us">`
- JSON-LD structured data per page type

### Sitemap Generation
FastAPI generates separate sitemaps per batch. Frontend `public/sitemap-index.xml` references all.

### Caching Strategy
- Panchang/Choghadiya pages: `Cache-Control: s-maxage=3600` (hourly -- data changes daily)
- Static content pages (Angel Numbers, Tarot, Faith): `Cache-Control: s-maxage=604800` (7 days)
- Compatibility/Character/Transit pages: `Cache-Control: s-maxage=86400` (daily)

---

## Delivery Sequence

Issue to Codex as sequential milestones:

| Milestone | Batches | Pages | Deliverable |
|---|---|---|---|
| M1 | Part A (SEO-1) + Batch 1 + Batch 2 | 3,498 + infra | SEO audit doc + Panchang city pages + Choghadiya pages |
| M2 | Batch 5 (Angel Numbers content corpus + pages) | 9,000 | Content DB + route + 9,000 pages |
| M3 | Batch 6 + Batch 3 + Batch 9 | 4,764 | Tarot combos + Compatibility + Remedies |
| M4 | Batch 8 + Batch 4 + Batch 10 + Batch 7 | 1,290 | Festivals + Transits + Character + Faith |

---

## Architecture Rules

1. **Internal engines only** -- no paid API call per page request
2. **Pre-generated content** (Batches 5, 6, 7, 9) stored in MongoDB, served from DB
3. **Database:** MongoDB with Motor async driver -- NOT PostgreSQL. Use Motor patterns matching existing codebase.
4. **Do NOT modify** `vedic_calculator.py`, `panchang_router.py`, `server.py` core logic
5. **Add new routes** to `server.py` via `include_router()` pattern (see existing panchang, tarot, numerology routers)
6. **Frontend:** All new pages added to `App.js` as lazy-imported routes with React.Suspense
7. **Build verification:** `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` must pass before PR
