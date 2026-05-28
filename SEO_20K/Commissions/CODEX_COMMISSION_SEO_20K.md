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

All sitemaps are **served dynamically from the FastAPI backend** (Render). Do NOT write XML files into `frontend/public/` -- Render cannot update Vercel's deployed static assets at runtime. See Part D for the full architecture.

Active M1-M3 sitemap endpoints to build now:
- `GET /api/seo/sitemap/panchang` -- 318 cities × 7 days = 2,226 URLs
- `GET /api/seo/sitemap/choghadiya` -- 318 cities × 4 periods = 1,272 URLs
- `GET /api/seo/sitemap/horoscope` -- 36 sign × 3 period pages
- `GET /api/seo/sitemap/compatibility` -- 144 canonical sign-pair URLs
- `GET /api/seo/sitemap/remedies` -- 12 affliction hub URLs
- `GET /api/seo/sitemap/transits` -- 108 URLs (9 planets × 12 signs)
- `GET /api/seo/sitemap/traits` -- 432 URLs (12 signs × 3 chart points × 12 houses)
- `GET /api/seo/sitemap/festivals` -- 300 URLs (50 festivals × 6 regions)

Parked -- build when engines are ready (do not build now):
- `GET /api/seo/sitemap/angel-numbers` -- 9,000 URLs (Batch 5 ⏸)
- `GET /api/seo/sitemap/tarot` -- 2,184 URLs (Batch 6 ⏸)

Update `frontend/public/sitemap-index.xml` manually to reference all Render-hosted sitemap URLs (see Part D for the exact XML block).

#### A3 -- Performance Optimisation
- Implement Vercel Edge Caching headers on all programmatic pages (`Cache-Control: s-maxage=86400`)
- Lazy load all images below the fold
- Code-split all large React pages (lazy import with Suspense)
- Add `hreflang` tags for en-IN and en-US on key pages

#### A4 -- 30-Day SEO Launch Plan
Write `docs/SEO_30DAY_PLAN.md` covering:
- Week 1: Technical fixes (above)
- Week 2: Content seeding (festival pages, panchang city pages, compatibility pages -- Angel Numbers parked)
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

### BATCH 5 -- Angel Numbers Module ⏸ PARKED

**Status:** PARKED -- requires a dedicated Angel Number interpretation engine built from textbook source material. Temple Team will provide source books. Do not build until engine spec is issued separately.
**Pages:** 9,000 (1,000 numbers × 9 intent vectors) -- reserved for future commission.

---

### BATCH 6 -- Tarot Spread Matrices ⏸ PARKED

**Status:** PARKED -- requires a dedicated Tarot combination engine built from authoritative tarot textbooks. Temple Team will provide source material. Do not build until engine spec is issued separately.
**Pages:** 2,184 (78 cards × 28 spreads) -- reserved for future commission.

---

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

**Canonicalization (IMPORTANT):** Sign pairs are symmetric. Always sort signs alphabetically to determine the canonical URL.
- Canonical: `/compatibility/aries-and-scorpio/` (aries < scorpio alphabetically)
- Non-canonical: `/compatibility/scorpio-and-aries/` → 301 redirect to canonical URL
- React Router must detect reversed order and redirect before rendering
- `<link rel="canonical">` always points to the alphabetically-sorted URL

**SEO metadata:**
- Title: `{Sign1} and {Sign2} Compatibility -- Marriage Gun Milan Score | EverydayHoroscope`
- Description: `Are {Sign1} and {Sign2} compatible for marriage? View full Ashta-Koota Gun Milan analysis with score out of 36.`

---

### BATCH 9 -- Remedy Hub Pages (12 pages + remedy matching engine) 🟠 PRIORITY 2

**Revised scope:** No city-specific pages. One SEO hub page per planetary affliction, pulling from the existing remedy catalog across all collections.
**Formula:** 12 affliction hub pages + remedy matching/filtering engine
**Internal engine:** ✅ Affliction detection via `vedic_calculator.py`. Remedy content from existing MongoDB remedy collections (~800 remedies already seeded).
**URL pattern:** `/remedies/{dosha-slug}/` (e.g., `/remedies/shani-sade-sati/`)

**12 afflictions:** Shani Sade Sati, Manglik Dosha, Pitru Dosha, Kaal Sarp Dosha, Shani Mahadasha, Rahu Mahadasha, Ketu Mahadasha, Guru Chandal Yoga, Grahan Yoga, Nadi Dosha, Gana Dosha, Bhakoot Dosha

**Actual MongoDB collections (NOT `spiritual_remedies` -- use these):**

| Collection | `science_id` filter | Count | Remedy type |
|---|---|---|---|
| `interpretation_rules` | `jyotish_remedies_mantras` | 100 | Mantra + Yantra |
| `interpretation_rules` | `jyotish_remedies_gemstones` | 100 | Gemstone |
| `interpretation_rules` | `jyotish_remedies_crystals` | 100 | Crystal |
| `interpretation_rules` | `jyotish_remedies_dhana` | 100 | Donation / Dhana |
| `interpretation_rules` | `jyotish_remedies_chakra` | 7 | Chakra healing |
| `knowledge_rules` | `jyotish_lk_remedies` | 361 | Lal Kitab ritual |

**Tagging -- ALREADY DONE:** Multi-parameter tags have been pre-generated and are ready to upload via:
`backend/scripts/tag_remedies_afflictions_v1.py --mongo-url "$MONGO_URL" --db-name horoscope_db`

**Tags added per remedy document:**
- `affliction_tags: [str]` -- list of dosha slugs (e.g. `["shani-sade-sati", "shani-mahadasha"]`)
- `seo_focus_area: [str]` -- e.g. `["Career & Work", "Finances"]`
- `seo_problem_area: [str]` -- e.g. `["Job Loss", "Financial Loss"]`
- `seo_planet_remedy: [str]` -- canonical planet names (e.g. `["Saturn"]`)
- `seo_zodiac_sign: [str]` -- e.g. `["Capricorn", "Aquarius", "Libra"]`
- `remedy_type: str` -- `mantra | gemstone | crystal | donation | chakra_ritual | lk_ritual`

**Remedy matching engine (new -- `backend/remedy_matching_router.py`):**
- `GET /api/remedies/{dosha-slug}` -- queries both `interpretation_rules` AND `knowledge_rules` where `affliction_tags` contains `{dosha-slug}`, returns combined list sorted by `remedy_type` priority (gemstone → mantra → donation → crystal → lk_ritual), then by `priority_weight` if present
- Response shape: `{ "dosha": str, "remedies": [{ "rule_id", "remedy_type", "summary", "planet", "zodiac_signs", "detailed" }] }`

**Each hub page includes:**
- Affliction explanation (what it is, how it manifests)
- How to detect it in your chart (inline calculator widget linking to Kundali page)
- Remedy listing filtered from the ~800 catalog: gemstones, yantras, mantras, Lal Kitab rituals -- filtered by `affliction_tags`
- Tabs or sections by `remedy_type` (Gemstones / Mantras / Donations / Crystals / Lal Kitab)
- CTA: "Check if you have {dosha} in your chart"

**No Temple Team confirmation needed** -- tagging script and collection schema are confirmed.

---

### BATCH 8 -- Global Festival Hubs (300 pages) 🟡 PRIORITY 3

**Formula:** 50 festivals × 6 international regions (India, USA, UK, UAE, Canada, Australia)
**Internal engine:** ✅ `panchang_router.py` -- festival dates + muhurta windows are computed
**URL pattern:** `/festivals/{festival-slug}/{region}/` (e.g., `/festivals/diwali/usa/`)

**SEO metadata:**
- Title: `{Festival} {Year} Date & Puja Timings in {Region} | EverydayHoroscope`
- Description: `Find exact {Festival} date and puja muhurta for {Region} {Year}. Includes Tithi, Nakshatra, and auspicious windows.`

---

### BATCH 4 -- Transit Profiles (108 pages) 🟡 PRIORITY 3

**Formula:** 9 planets × 12 zodiac signs = 108 pages (planet transiting each sign, not houses)
**Internal engine:** ✅ `vedic_calculator.py` -- planetary sign placements fully computable
**URL pattern:** `/transits/{planet}-in-{sign}/` (e.g., `/transits/saturn-in-aquarius/`)

**9 planets:** Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu
**12 signs:** Aries through Pisces

**Each page includes:**
- What this planet's transit through this sign means generally
- Effects on each of the 12 rising signs (brief per-ascendant impact)
- Duration of this transit (pulled from ephemeris via `vedic_calculator.py`)
- Current/upcoming transit dates

**SEO metadata:**
- Title: `{Planet} in {Sign} Transit Effects -- All Rising Signs | EverydayHoroscope`
- Description: `What does {Planet} in {Sign} mean? Find effects on all 12 rising signs, transit duration, and dates.`

---

### BATCH 10 -- Character Placements (432 pages) 🟡 PRIORITY 3

**Formula:** 12 zodiac signs × 12 houses × 3 chart points (Sun/Moon/Rising) = 432 pages
**Internal engine:** ✅ `vedic_calculator.py` -- sign and house placements fully computable
**URL pattern:** `/traits/{sign}/{chart-point}/{house}/` (e.g., `/traits/scorpio/moon/7th-house/`)

**3 chart points:** `sun`, `moon`, `rising`
**12 houses:** `1st-house` through `12th-house`
**Example URLs:**
- `/traits/scorpio/moon/7th-house/` → Moon in Scorpio in the 7th House: relationship traits
- `/traits/aries/sun/10th-house/` → Sun in Aries in the 10th House: career identity traits
- `/traits/cancer/rising/1st-house/` → Cancer Rising in the 1st House: personality traits

**React Router param:** `/traits/:sign/:chartPoint/:house` → `CharacterPlacementPage.jsx`

**SEO metadata:**
- Title: `{ChartPoint} in {Sign} in {House} -- Traits & Personality | EverydayHoroscope`
- Description: `What does {ChartPoint} in {Sign} in the {House} mean? Explore personality traits, strengths, and Vedic insights.`

---

### BATCH 7 -- Lumina Faith Hubs ⏸ PARKED

**Status:** PARKED -- requires a dedicated Faith interpretation engine. Temple Team will provide textbook/scripture source material. Do not build until engine spec is issued separately.
**Pages:** 450 reserved for future commission.

---

## Part C -- Directory Routing (React Router additions)

**Active routes (M1-M3 only):**
```
/panchang/:citySlug/:date/               → CityPanchangPage.jsx       (Batch 1)
/choghadiya/:citySlug/:period/           → ChoghadiyaPage.jsx          (Batch 2)
/compatibility/:signPair/                → CompatibilityPage.jsx       (Batch 3)
/remedies/:dosha/                        → RemedyHubPage.jsx           (Batch 9 -- NO citySlug)
/festivals/:festivalSlug/:region/        → FestivalRegionPage.jsx      (Batch 8)
/transits/:planet/:sign/                 → TransitProfilePage.jsx      (Batch 4)
/traits/:sign/:chartPoint/:house/        → CharacterPlacementPage.jsx  (Batch 10)
```

**Parked routes (do NOT build yet -- awaiting engine source material):**
```
/angel-number/:number/:intent/           → AngelNumberPage.jsx         (Batch 5 ⏸)
/tarot/:cardSlug/:spreadSlug/            → TarotCombinationPage.jsx    (Batch 6 ⏸)
/faith/:verseId/:transit/               → FaithHubPage.jsx            (Batch 7 ⏸)
```

**Compatibility redirect rule:**
```javascript
// In CompatibilityPage.jsx -- detect non-canonical order, redirect before render
const [s1, s2] = signPair.split('-and-');
const sorted = [s1, s2].sort().join('-and-');
if (sorted !== signPair) return <Navigate to={`/compatibility/${sorted}/`} replace />;
```

---

## Part D -- SEO Infrastructure

### Metadata Builder (Dynamic per page)

**Use the existing `SEO.jsx` component** (`frontend/src/components/SEO.jsx`) -- do NOT add `react-helmet-async` as a new dependency. `SEO.jsx` already wraps Helmet internally. Add a `jsonLd` prop if not already present:

```jsx
// Usage pattern on every new page:
<SEO
  title="{City} Panchang Today {Date} | EverydayHoroscope"
  description="Accurate daily Panchang for {City}..."
  canonical={`https://everydayhoroscope.in${location.pathname}`}
  hreflang={[
    { lang: "en-in", href: `https://everydayhoroscope.in${location.pathname}` },
    { lang: "en-us", href: `https://everydayhoroscope.in${location.pathname}` }
  ]}
  jsonLd={datasetSchema}   // JSON-LD object -- SEO.jsx renders as <script type="application/ld+json">
/>
```

Fields per page:
- `title` -- per batch formula (max 60 chars)
- `description` -- per batch formula (max 155 chars)
- `canonical` -- always `https://everydayhoroscope.in` + `location.pathname`
- `hreflang` -- en-IN and en-US pointing to same canonical URL
- `jsonLd` -- JSON-LD structured data object (Dataset / HoroscopeReading / FAQPage per batch)

### Sitemap Generation

**Architecture constraint:** FastAPI runs on Render; Vercel serves the frontend. A Render endpoint cannot write files into Vercel's deployed static assets at runtime. Do NOT attempt to save sitemap XML into `frontend/public/` via an API call.

**Correct approach -- backend-served dynamic sitemaps:**

Add FastAPI routes that serve XML directly. Vercel's `frontend/public/sitemap-index.xml` references the Render backend URLs:

```
FastAPI endpoints (serve XML, no file writes):
  GET /api/seo/sitemap/panchang     → 318 cities × 7 days = 2,226 URLs
  GET /api/seo/sitemap/choghadiya   → 318 cities × 4 periods = 1,272 URLs
  GET /api/seo/sitemap/horoscope    → 36 sign × 3 period pages = 108 URLs
  GET /api/seo/sitemap/compatibility → 144 pair URLs
  GET /api/seo/sitemap/remedies     → 12 affliction hub URLs
  GET /api/seo/sitemap/transits     → 108 URLs
  GET /api/seo/sitemap/traits       → 432 URLs
  GET /api/seo/sitemap/festivals    → 300 URLs
```

`frontend/public/sitemap-index.xml` (update manually, not generated):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://everydayhoroscope-api.onrender.com/api/seo/sitemap/panchang</loc></sitemap>
  <sitemap><loc>https://everydayhoroscope-api.onrender.com/api/seo/sitemap/choghadiya</loc></sitemap>
  <sitemap><loc>https://everydayhoroscope-api.onrender.com/api/seo/sitemap/horoscope</loc></sitemap>
  <sitemap><loc>https://everydayhoroscope-api.onrender.com/api/seo/sitemap/compatibility</loc></sitemap>
  <sitemap><loc>https://everydayhoroscope-api.onrender.com/api/seo/sitemap/remedies</loc></sitemap>
  <sitemap><loc>https://everydayhoroscope-api.onrender.com/api/seo/sitemap/transits</loc></sitemap>
  <sitemap><loc>https://everydayhoroscope-api.onrender.com/api/seo/sitemap/traits</loc></sitemap>
  <sitemap><loc>https://everydayhoroscope-api.onrender.com/api/seo/sitemap/festivals</loc></sitemap>
</sitemapindex>
```

FastAPI sitemap response headers: `Content-Type: application/xml`, `Cache-Control: s-maxage=86400`

### Caching Strategy

**Vercel Edge Caching is configured via `vercel.json` headers** -- NOT in React component code. Add/update `frontend/vercel.json`:

```json
{
  "headers": [
    {
      "source": "/panchang/:citySlug/:date/",
      "headers": [{ "key": "Cache-Control", "value": "s-maxage=3600, stale-while-revalidate" }]
    },
    {
      "source": "/choghadiya/:citySlug/:period/",
      "headers": [{ "key": "Cache-Control", "value": "s-maxage=3600, stale-while-revalidate" }]
    },
    {
      "source": "/compatibility/:signPair/",
      "headers": [{ "key": "Cache-Control", "value": "s-maxage=86400, stale-while-revalidate" }]
    },
    {
      "source": "/remedies/:dosha/",
      "headers": [{ "key": "Cache-Control", "value": "s-maxage=86400, stale-while-revalidate" }]
    },
    {
      "source": "/transits/:planet/:sign/",
      "headers": [{ "key": "Cache-Control", "value": "s-maxage=86400, stale-while-revalidate" }]
    },
    {
      "source": "/traits/:sign/:chartPoint/:house/",
      "headers": [{ "key": "Cache-Control", "value": "s-maxage=86400, stale-while-revalidate" }]
    },
    {
      "source": "/festivals/:festivalSlug/:region/",
      "headers": [{ "key": "Cache-Control", "value": "s-maxage=86400, stale-while-revalidate" }]
    }
  ]
}
```

TTL values:
- Panchang/Choghadiya: `s-maxage=3600` (hourly -- data changes daily)
- Compatibility/Character/Transit/Festivals/Remedies: `s-maxage=86400` (daily)
- Parked batches (Angel Numbers, Tarot, Faith): `s-maxage=604800` when built (7 days)

---

## Delivery Sequence

Issue to Codex as sequential milestones:

| Milestone | Batches | Pages | Deliverable |
|---|---|---|---|
| M1 | Part A (SEO-1 merged) + Batch 1 + Batch 2 | 3,498 + infra | SEO audit doc + 318-city Panchang pages + Choghadiya pages |
| M2 | Batch 3 + Batch 9 | 1,308 | Compatibility (144 pairs) + Remedy hub pages (12) + remedy matching engine |
| M3 | Batch 8 + Batch 4 + Batch 10 | 840 | Festival region pages + Transit profiles + Character placements |
| PARKED | Batch 5, 6, 7 | 11,634 | Angel Numbers + Tarot + Faith -- awaiting engine source material |

---

## Architecture Rules

1. **Internal engines only** -- no paid API call per page request
2. **Pre-generated content** (Batches 5, 6, 7 -- PARKED) stored in MongoDB, served from DB when built. Batch 9 remedy content is already seeded; served via `remedy_matching_router.py` query on request.
3. **Database:** MongoDB with Motor async driver -- NOT PostgreSQL. Use Motor patterns matching existing codebase.
4. **Do NOT modify** `vedic_calculator.py`, `panchang_router.py`, `server.py` core logic
5. **Add new routes** to `server.py` via `include_router()` pattern (see existing panchang, tarot, numerology routers)
6. **Frontend:** All new pages added to `App.js` as lazy-imported routes with React.Suspense
7. **Build verification:** `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` must pass before PR
