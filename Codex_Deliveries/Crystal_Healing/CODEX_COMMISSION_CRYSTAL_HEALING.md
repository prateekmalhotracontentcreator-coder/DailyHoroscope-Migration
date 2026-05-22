# CRY-1 Commission Brief
> Thread: Crystal Healing Codex Thread  
> Module: Crystal Healing Hub + Crystal Pages + Intention Pages + Calculator  
> Pages: 1 hub + ~50 crystal pages + ~20 intention pages + 1 calculator = ~72 pages  
> Date: 2026-05-23  
> Status: READY TO BUILD -- decoded gemstone data available, source PDF available

---

## Context

EverydayHoroscope (`everydayhoroscope.in`) is a live React 18 + FastAPI + MongoDB + Tailwind CSS platform. This commission adds the Crystal Healing module -- crystal detail pages, intention-based crystal pages, and a birth-chart-powered crystal recommendation calculator.

**Repo:** `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`  
**Stack:** React 18 · FastAPI · MongoDB · Tailwind CSS  
**Internal engine:** `backend/vedic_calculator.py` -- for birth-chart data in the calculator. Do NOT add chart logic to any other file.

**Source material (reference only -- all content must be original Codex writing):**

Primary:
```
/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/Crystal Healing/Proofread-Gemstones-book-copy.pdf
```
(96 pages -- covers crystals, healing properties, chakras, usage)

Pre-decoded structured data (already available -- use as data reference):
```
/Users/apple/Documents/Knowledge Engine_eBooks/Remedies + The Strategist/3. Remedies_Gemstones.md
/Users/apple/Documents/Knowledge Engine_eBooks/Remedies + The Strategist/4. Crystal Remedies_JSON.md
/Users/apple/Documents/Knowledge Engine_eBooks/DestinyNumerology_CC_Decode/Numerology_Ch17_GemstoneNumerology_Rules.json
/Users/apple/Documents/Knowledge Engine_eBooks/DestinyNumerology_CC_Decode/Numerology_Ch17_GemstoneNumerology_DataTables.md
```

The `3. Remedies_Gemstones.md` file contains structured JSON for Navaratnas and extended gemstone remedies (IDs 101+) with: primary gemstone, synergy/conflict pairings, metal, finger, mantra, activation rules. Use this as a reference data source for the calculator and crystal pages.

**Copyright compliance mandatory:** No direct quotes from the source PDF. All page copy is original Codex writing inspired by crystal healing traditions.

---

## Module Architecture

### URL Patterns

| URL | Purpose |
|---|---|
| `/crystals/` | Hub page -- what is crystal healing, crystal grid, intention guide |
| `/crystals/{crystal-slug}/` | Individual crystal detail page (~50 crystals) |
| `/crystals/for/{intention-slug}/` | Intention page -- best crystals for this purpose (~20 pages) |
| `/crystals/calculator/` | Birth-chart crystal recommendation calculator |

**Total pages:** 1 hub + 50 crystal + 20 intention + 1 calculator = **72 pages**

---

## Crystal List (Phase 1 -- top 50 by search volume)

**Navaratnas (9 Vedic gemstones -- highest priority):**
ruby, pearl, red-coral, emerald, yellow-sapphire, diamond, blue-sapphire, hessonite-garnet, cats-eye

**Western healing crystals (top 41 by search traffic):**
amethyst, rose-quartz, clear-quartz, black-tourmaline, citrine, lapis-lazuli, obsidian, selenite, malachite, carnelian, moonstone, labradorite, pyrite, amazonite, sodalite, aventurine, tigers-eye, jade, hematite, lepidolite, rhodonite, fluorite, aquamarine, chrysocolla, sunstone, bloodstone, turquoise, garnet, onyx, shungite, rhodochrosite, prehnite, calcite, apatite, angelite, celestite, kunzite, kyanite, larimar, moldavite, nuummite

---

## Intention Categories (20)

| Slug | Display |
|---|---|
| `love-relationships` | Love & Relationships |
| `anxiety-stress` | Anxiety & Stress Relief |
| `protection` | Protection & Grounding |
| `abundance-money` | Abundance & Money |
| `clarity-focus` | Clarity & Focus |
| `confidence` | Confidence & Courage |
| `sleep` | Sleep & Relaxation |
| `grief-healing` | Grief & Emotional Healing |
| `spiritual-growth` | Spiritual Growth |
| `intuition` | Intuition & Psychic Ability |
| `creativity` | Creativity |
| `communication` | Communication |
| `health-vitality` | Health & Vitality |
| `travel-protection` | Travel Protection |
| `career-success` | Career Success |
| `new-beginnings` | New Beginnings |
| `fertility` | Fertility & Pregnancy |
| `forgiveness` | Forgiveness & Release |
| `truth-honesty` | Truth & Honesty |
| `meditation` | Meditation & Mindfulness |

---

## Backend

### Router File
`backend/crystal_router.py`

Register in `backend/server.py` as: `app.include_router(crystal_router, prefix="/api")`

### Endpoints

```
GET  /api/crystals/list                        → all 50 crystals with basic meta
GET  /api/crystals/{slug}                      → crystal detail content
GET  /api/crystals/intention/{slug}            → intention page content
POST /api/crystals/calculator                  → birth chart → crystal recommendations
GET  /api/seo/sitemap/crystals                 → sitemap URLs (72 URLs)
```

### Calculator Logic (`POST /api/crystals/calculator`)

**Input:**
```json
{
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "place": "city or lat/lon",
  "intention": "love-relationships"
}
```

**Processing (via `vedic_calculator.py`):**
1. Get birth chart: Lagna, Moon sign, current Mahadasha planet, weak planets (debilitated or in 6th/8th/12th without strength)
2. Apply crystal recommendation rules:

**Planet → Vedic Gemstone mapping (hardcoded in router):**

| Planet | Primary Vedic Stone | Secondary |
|---|---|---|
| Sun | Ruby | Sunstone, Red Garnet |
| Moon | Pearl | Moonstone, Selenite |
| Mars | Red Coral | Bloodstone, Carnelian |
| Mercury | Emerald | Green Aventurine, Amazonite |
| Jupiter | Yellow Sapphire | Citrine, Tiger's Eye |
| Venus | Diamond | Clear Quartz, Rose Quartz |
| Saturn | Blue Sapphire | Amethyst, Obsidian |
| Rahu | Hessonite Garnet | Labradorite, Obsidian |
| Ketu | Cat's Eye | Fluorite, Lepidolite |

**Intention overlay mapping (hardcoded):**

| Intention | Booster Crystal |
|---|---|
| love-relationships | Rose Quartz + Rhodonite |
| anxiety-stress | Lepidolite + Amethyst |
| protection | Black Tourmaline + Obsidian |
| abundance-money | Pyrite + Citrine |
| clarity-focus | Clear Quartz + Sodalite |
| confidence | Tiger's Eye + Carnelian |
| sleep | Selenite + Moonstone |
| spiritual-growth | Labradorite + Amethyst |
| intuition | Lapis Lazuli + Moonstone |
| career-success | Pyrite + Yellow Sapphire |

**Output:**
```json
{
  "primary_vedic": {
    "crystal": "Yellow Sapphire",
    "slug": "yellow-sapphire",
    "reason": "Jupiter Mahadasha active -- Yellow Sapphire amplifies Jupiter blessings",
    "wearing": { "metal": "Gold", "finger": "Index finger", "day": "Thursday", "mantra": "Om Brim Brihaspataye Namah" }
  },
  "healing_recommendations": [
    { "crystal": "Amethyst", "slug": "amethyst", "reason": "Saturn in 8th house -- Amethyst provides protective grounding" },
    { "crystal": "Rose Quartz", "slug": "rose-quartz", "reason": "Intention: Love & Relationships -- Rose Quartz opens the heart chakra" }
  ],
  "intention_boosters": [
    { "crystal": "Rhodonite", "slug": "rhodonite", "reason": "Balances emotional energy in love matters" }
  ],
  "placement_tip": "Keep primary crystal on right side of desk or wear as pendant. Healing crystals: place under pillow or carry in left pocket."
}
```

### MongoDB Collection: `crystals`
50 documents:

```json
{
  "slug": "amethyst",
  "display_name": "Amethyst",
  "tagline": "The stone of peace and spiritual protection",
  "color": "Purple to violet",
  "chakras": ["Crown", "Third Eye"],
  "element": "Air",
  "planet": "Saturn / Neptune",
  "zodiac": ["Aquarius", "Pisces", "Capricorn"],
  "hardness_mohs": 7,
  "healing_properties": {
    "emotional": ["calms anxiety", "reduces stress", "aids grief", "promotes emotional clarity"],
    "physical": ["supports sleep", "headache relief", "immune system"],
    "spiritual": ["enhances intuition", "deepens meditation", "psychic protection"]
  },
  "best_intentions": ["anxiety-stress", "sleep", "spiritual-growth", "intuition", "protection"],
  "how_to_use": ["Place on bedside table for sleep", "Wear as pendant for continuous protection", "Hold during meditation", "Place in corners of room for protection grid"],
  "cleansing_methods": ["Moonlight overnight", "Running water (30 sec)", "Selenite slab", "Sound bath"],
  "pairs_well_with": ["clear-quartz", "black-tourmaline", "rose-quartz"],
  "avoid_with": ["citrine (opposing energies for some)", ""],
  "affirmation": "I am calm, protected, and deeply connected to my intuition.",
  "caution": "Fades in direct sunlight -- cleanse with moonlight instead.",
  "faq": [
    { "q": "What is amethyst good for?", "a": "..." },
    { "q": "How do I cleanse amethyst?", "a": "..." },
    { "q": "Can I wear amethyst every day?", "a": "..." },
    { "q": "What chakra is amethyst?", "a": "..." },
    { "q": "Who should wear amethyst?", "a": "..." }
  ],
  "meta_title": "Amethyst Crystal -- Meaning, Healing Properties & How to Use | EverydayHoroscope",
  "meta_description": "Amethyst promotes peace, intuition, and spiritual protection. Discover amethyst healing properties, chakra connections, how to use it, and who should wear it."
}
```

**Vedic gemstone documents** additionally include: `vedic_name`, `wearing.metal`, `wearing.finger`, `wearing.mantra`, `wearing.day`, `wearing.activation`, `synergy`, `conflict` -- pulled from the pre-decoded `3. Remedies_Gemstones.md` file.

**Collection: `crystal_intentions`** -- 20 documents

```json
{
  "slug": "love-relationships",
  "display": "Love & Relationships",
  "intro": "2-3 sentences -- how crystals support love and relationships",
  "top_crystals": ["rose-quartz", "rhodonite", "moonstone", "ruby", "emerald"],
  "how_to_use": ["Place rose quartz in bedroom", "...", "..."],
  "affirmation": "I am open to giving and receiving love...",
  "faq": [
    { "q": "What crystal is best for love?", "a": "..." },
    { "q": "Can crystals attract a partner?", "a": "..." },
    { "q": "Which crystal to wear for relationships?", "a": "..." },
    { "q": "What crystals help with heartbreak?", "a": "..." },
    { "q": "How do I use crystals for love?", "a": "..." }
  ],
  "meta_title": "Best Crystals for Love & Relationships -- Top 5 + How to Use | EverydayHoroscope",
  "meta_description": "Discover the best crystals for love -- rose quartz, rhodonite, moonstone, and more. Learn how to use them to attract love, heal heartbreak, and strengthen bonds."
}
```

### Seed Script
`backend/scripts/seed_crystals.py` -- seeds 50 crystal documents + 20 intention documents.

---

## Frontend

### Hub Page
**File:** `frontend/src/pages/crystals/CrystalHubPage.jsx`

**Page content:**
- H1: `Crystal Healing -- Stones for Every Intention`
- Intro: What is crystal healing? How does it work? (3-4 sentences, original)
- **Calculator CTA card:** Gold GlassCard -- "Find Your Crystal by Birth Chart" → `/crystals/calculator/`
- **By Intention:** 20 intention pills -- each → intention page
- **Crystal grid:** 50 crystal cards (filterable by chakra/element/planet) -- name, colour badge, 1-line tagline, link
- **FAQ accordion:** 5 questions
- JSON-LD: `FAQPage` + `BreadcrumbList`

### Crystal Detail Page
**File:** `frontend/src/pages/crystals/CrystalPage.jsx`

**Page content:**
- H1: `{Crystal Name} -- Meaning, Healing Properties & How to Use`
- **Meta strip:** Color · Chakras · Element · Planet · Zodiac -- 5 chips
- **Healing properties:** 3 sub-sections (Emotional / Physical / Spiritual) -- each 3-4 bullets
- **Best intentions:** Pills linking to intention pages
- **How to use:** 3-4 bullet points (wearable / placement / meditation)
- **Pairs well with:** 3 crystal cards
- **Cleansing methods:** 3-4 bullets
- **Affirmation block:** Gold-bordered italic Playfair
- **Vedic gemstone section** (only for 9 Navaratnas): Wearing instructions, mantra, activation timing, synergy/conflict
- **Caution note** (if applicable -- e.g. sunlight warning)
- **FAQ accordion:** 5 questions
- **CTA:** "Find your crystal by birth chart" → `/crystals/calculator/`
- JSON-LD: `FAQPage` + `Article`

### Intention Page
**File:** `frontend/src/pages/crystals/CrystalIntentionPage.jsx`

**Page content:**
- H1: `Best Crystals for {Intention} -- Top {N} Stones & How to Use Them`
- Intro: 2-3 sentences
- **Top crystal grid:** 4-6 crystal cards -- name, tagline, "How to use for {intention}" 1-liner, link
- **How to use guide:** 3-4 actionable steps
- **Affirmation block**
- **FAQ accordion:** 5 questions
- **CTA:** "Get your personal crystal recommendation" → `/crystals/calculator/`
- JSON-LD: `FAQPage` + `Article`

### Calculator Page
**File:** `frontend/src/pages/crystals/CrystalCalculatorPage.jsx`

**Page content:**
- H1: `Crystal Calculator -- Your Personal Recommendation from Your Birth Chart`
- **Form:** Date of birth · Time · Place · Intention (dropdown -- 20 options) · Submit
- **Results:**
  - Primary Vedic gemstone: Large GlassCard -- crystal name, reason, wearing instructions (for Navaratnas)
  - Healing recommendations: 2-3 medium cards
  - Intention boosters: 1-2 small cards
  - Placement tip
  - "Learn more about {crystal}" links → crystal pages
- JSON-LD: `FAQPage`

---

## SEO Metadata Formulas

### Crystal Page
- **Title:** `{Crystal} Crystal -- Healing Properties, Chakra & How to Use | EverydayHoroscope`
- **Description:** `{Crystal} promotes {keyword1} and {keyword2}. Discover healing properties, chakra connections, best intentions, and how to use {crystal} for maximum benefit.`

### Intention Page
- **Title:** `Best Crystals for {Intention} -- {Top Crystal} & More | EverydayHoroscope`
- **Description:** `Looking for crystals for {intention}? Discover the top {N} stones -- how to use them, which chakras they activate, and how to maximise their healing energy.`

---

## Routes (App.js additions)

```jsx
<Route path="/crystals" element={<CrystalHubPage />} />
<Route path="/crystals/calculator" element={<CrystalCalculatorPage />} />
<Route path="/crystals/for/:intentionSlug" element={<CrystalIntentionPage />} />
<Route path="/crystals/:crystalSlug" element={<CrystalPage />} />
```

All routes: public, no auth gate.

---

## Sitemap

Add to `backend/seo_router.py`:
```python
GET /api/seo/sitemap/crystals   # 72 URLs
```

Add to `frontend/public/sitemap-index.xml`.

---

## Technical Requirements

- New React pages in `frontend/src/pages/crystals/` (new subdirectory)
- New FastAPI router: `backend/crystal_router.py`
- Register in `backend/server.py`
- New routes in `frontend/src/App.js`
- Sitemap endpoint in `backend/seo_router.py`
- Cache headers in `frontend/vercel.json` (s-maxage=86400) for `/crystals/*`
- MongoDB seed script: `backend/scripts/seed_crystals.py`
- `SEO` component on every page
- **Calculator:** POST to `/api/crystals/calculator` -- calls `vedic_calculator.py` for chart data. Recommendation logic is hardcoded mapping in router -- no chart logic in router itself.

**Tailwind / theme:** GlassCard pattern. Gold accent `#c5a059`. No new dependencies.

**Build:** `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` -- must pass clean.

---

## Acceptance Checklist

- [ ] Hub page renders at `/crystals/`
- [ ] 50 crystal pages render at `/crystals/{slug}/`
- [ ] 20 intention pages render at `/crystals/for/{slug}/`
- [ ] Calculator renders at `/crystals/calculator/`
- [ ] Calculator returns recommendations for a test birth input + intention
- [ ] Vedic gemstone sections render on Navaratna pages (Ruby, Pearl, etc.) with wearing instructions + mantra
- [ ] Sitemap endpoint returns 72 URLs
- [ ] Vercel cache headers applied to `/crystals/*`
- [ ] Seed script seeds all 70 documents
- [ ] Build clean -- zero errors
- [ ] JSON-LD on all page types
- [ ] SEO meta applied on all pages
- [ ] No direct quotes from source PDF -- all content original Codex writing
