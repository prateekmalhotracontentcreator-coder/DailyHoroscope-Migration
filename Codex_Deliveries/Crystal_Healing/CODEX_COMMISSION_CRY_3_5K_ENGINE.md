# CRY-3 Commission Brief -- Crystal Cross-Reference Engine (5,000-Page Mission)
> Thread: Crystal Healing Codex Thread (same thread as CRY-1 / CRY-2)
> Commission ID: CRY-3
> Date: 2026-05-26
> Status: READY TO ISSUE
> Prerequisite: CRY-1 ✅ CRY-2 ✅

---

## Objective

CRY-1 and CRY-2 built the foundation (113 pages). CRY-3 scales to **5,000+ pages** by building a
cross-reference engine that pairs every crystal against every major dimension of meaning -- chakra,
zodiac sign, planet, intention, nakshatra, astrological house, and life path number -- generating
unique, book-decoded, SEO-rich pages for each combination.

**The key difference from CRY-1/CRY-2:** This is not generic content. Every page must be grounded
in specific data decoded from the source books. The crystal's unique properties within that specific
context (e.g. "What does Amethyst specifically do for the Crown Chakra?" vs just "Amethyst general
meaning") must come from the books. Codex's primary task here is **deep book decoding first**, then
page generation from that decoded data.

---

## Source Books (Decode These First)

```
Primary:
/Users/apple/Documents/Knowledge Engine_eBooks/Crystals/7. Crystal Healing.pdf
/Users/apple/Documents/Knowledge Engine_eBooks/Crystals/Proofread-Gemstones-book-copy.pdf

Supporting:
/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/tantra-mantra-yantra.pdf
/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/Numerology/Numerology-With Tantra, Ayurveda, and Astrology.pdf
```

---

## Book Decode Schema -- What to Extract Per Crystal

For each of the 50 crystals (slugs in `CRYSTAL_SLUGS` in `backend/crystal_data.py`), decode and
record the following from the source books into a structured Python dict:

```python
CRYSTAL_XREF_DATA = {
    "amethyst": {
        # Chakra associations (from book)
        "chakras": {
            "crown":       { "strength": "primary",   "mechanism": "...", "benefit": "...", "practice": "..." },
            "third-eye":   { "strength": "secondary",  "mechanism": "...", "benefit": "...", "practice": "..." },
            # include all 7 chakras, mark strength: primary / secondary / supportive / minimal
        },

        # Zodiac sign affinities (from book)
        "signs": {
            "pisces":      { "affinity": "primary",   "why": "...", "shadow_help": "...", "wear_tip": "..." },
            "aquarius":    { "affinity": "secondary",  "why": "...", "shadow_help": "...", "wear_tip": "..." },
            # all 12 signs
        },

        # Vedic planet rulerships (from book)
        "planets": {
            "jupiter":     { "rulership": "primary",  "how_it_amplifies": "...", "mantra_pairing": "...", "metal": "..." },
            "saturn":      { "rulership": "secondary", "how_it_amplifies": "...", "mantra_pairing": "...", "metal": "..." },
            # all 9 planets: sun, moon, mars, mercury, jupiter, venus, saturn, rahu, ketu
        },

        # Intention deep-dives (from book)
        "intentions": {
            "love":        { "mechanism": "...", "placement": "...", "affirmation": "...", "ritual": "..." },
            "career":      { "mechanism": "...", "placement": "...", "affirmation": "...", "ritual": "..." },
            # all 20 intentions from INTENTION_DEFINITIONS in crystal_data.py
        },

        # Nakshatra affinities (Vedic -- from tantra/ayurveda book)
        "nakshatras": {
            "ashwini":     { "fit": "strong", "reason": "...", "remedy_use": "..." },
            "bharani":     { "fit": "moderate", "reason": "...", "remedy_use": "..." },
            # all 27 nakshatras
        },

        # Astrological houses (from book)
        "houses": {
            "1":  { "effect": "...", "placement_tip": "...", "caution": "..." },
            "2":  { "effect": "...", "placement_tip": "...", "caution": "..." },
            # houses 1-12
        },

        # Numerology life path (from numerology book)
        "life_paths": {
            "1": { "synergy": "high",   "why": "...", "how_to_use": "..." },
            "2": { "synergy": "medium", "why": "...", "how_to_use": "..." },
            # life paths 1-9
        },

        # Thematic data
        "element":   "water",           # fire / water / earth / air / ether
        "color_ray": "violet",          # the colour energy this crystal carries
        "body_systems": [               # body areas/systems this crystal addresses (from healing book)
            { "system": "nervous-system",   "benefit": "...", "how": "..." },
            { "system": "immune-system",    "benefit": "...", "how": "..." },
        ],
        "combinations": [               # best crystal pairings (from book)
            { "with": "rose-quartz",    "effect": "..." },
            { "with": "clear-quartz",   "effect": "..." },
        ],
    },
    # repeat for all 50 crystals
}
```

**This decode is the core deliverable.** Everything else is generated from it.
Write it as `backend/crystal_xref_data.py`. It will be large -- use multiple Write tool calls,
batching 5 crystals per call.

---

## Page Architecture -- 12 New Categories (~5,100 new pages)

### Category 1 -- Crystal × Chakra Pages (350 pages)

URL: `/crystals/{crystal-slug}/chakra/{chakra-slug}`

Chakras: `root`, `sacral`, `solar-plexus`, `heart`, `throat`, `third-eye`, `crown`

**Page content:**
- H1: `{Crystal} for the {Chakra} Chakra -- How It Works & How to Use It`
- What this crystal does specifically for this chakra (mechanism from book data)
- Strength rating (Primary / Secondary / Supportive)
- **Placement guide**: Where to place during meditation
- **Activation practice**: Specific ritual or meditation for this crystal-chakra pair
- **Signs this chakra needs this crystal**: 3-4 symptoms
- **Affirmation**: Chakra-specific affirmation using this crystal's energy
- **FAQ accordion**: 4 Q&As
- CTA → `/crystals/{crystal-slug}` (full crystal page) + `/crystals/chakra/{chakra-slug}` (chakra hub)
- JSON-LD: FAQPage + Article

### Category 2 -- Crystal × Zodiac Sign Pages (600 pages)

URL: `/crystals/{crystal-slug}/sign/{sign-slug}`

Signs: aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius, pisces

**Page content:**
- H1: `{Crystal} for {Sign} -- How This Stone Supports {Sign} Energy`
- Why this crystal resonates with this sign (from book data)
- **Affinity level**: Primary / Secondary / Supportive
- **The shadow it helps**: What typical {Sign} challenge does this crystal address?
- **Wear/carry guidance**: Best wearing method for this sign
- **Best life areas for this pairing**: 3 areas where this combination shines
- **Combined with**: 1-2 other crystals that amplify this crystal for this sign
- **FAQ accordion**: 4 Q&As
- CTA → full crystal page + `/crystals/for/sign/{sign}` (sign hub)
- JSON-LD: FAQPage + Article

### Category 3 -- Crystal × Vedic Planet Pages (450 pages)

URL: `/crystals/{crystal-slug}/planet/{planet-slug}`

Planets: sun, moon, mars, mercury, jupiter, venus, saturn, rahu, ketu

**Page content:**
- H1: `{Crystal} for {Planet} -- Vedic Properties, Mantra & Wearing Method`
- How this crystal amplifies or balances this planet's energy (from book)
- **Rulership type**: Primary / Secondary
- **How it amplifies**: What planetary quality does this crystal enhance
- **Mantra pairing**: Which mantra to chant while holding this crystal for this planet
- **Metal & day**: Best metal to set in and day to wear
- **Who benefits most**: People with this planet prominent or afflicted in their chart
- **FAQ accordion**: 4 Q&As
- CTA → full crystal page + `/crystals/for/planet/{planet}`
- JSON-LD: FAQPage + Article

### Category 4 -- Crystal × Intention Deep-Dive Pages (1,000 pages)

URL: `/crystals/{crystal-slug}/for/{intention-slug}`

All 20 intentions from `INTENTION_DEFINITIONS` in `crystal_data.py`:
love, career, anxiety, grief, protection, abundance, clarity, creativity, grounding, health,
intuition, manifestation, relationships, sleep, spiritual-growth, strength, stress-relief,
transformation, travel, wisdom

**Page content:**
- H1: `{Crystal} for {Intention} -- How to Use It, Where to Place It & What to Expect`
- Mechanism: How this crystal specifically supports this intention (from book)
- **Placement guide**: Where in the home/body/workspace
- **3-step ritual**: Specific practice for this crystal + intention combination
- **Affirmation**: Crystal-specific affirmation for this intention
- **When to use**: Best timing (moon phase, day of week, etc.)
- **What to expect**: Realistic outcome framing
- **FAQ accordion**: 4 Q&As
- CTA → full crystal page + intention hub
- JSON-LD: FAQPage + HowTo

### Category 5 -- Crystal × Nakshatra Pages (1,350 pages)

URL: `/crystals/{crystal-slug}/nakshatra/{nakshatra-slug}`

All 27 Nakshatras:
ashwini, bharani, krittika, rohini, mrigashira, ardra, punarvasu, pushya, ashlesha,
magha, purva-phalguni, uttara-phalguni, hasta, chitra, swati, vishakha, anuradha, jyeshtha,
mula, purva-ashadha, uttara-ashadha, shravana, dhanishtha, shatabhisha, purva-bhadrapada,
uttara-bhadrapada, revati

**Page content:**
- H1: `{Crystal} for {Nakshatra} Nakshatra -- Vedic Crystal Remedy & Guidance`
- Why this crystal resonates with this nakshatra's ruling deity and energy
- **Fit level**: Strong / Moderate / Supportive
- **Remedy use**: Specific Vedic use-case for this nakshatra person
- **Wearing ritual**: How to activate and wear for this nakshatra
- **What it corrects**: Nakshatra shadow traits this crystal softens
- **Mantra**: Short mantra to pair with this crystal for this nakshatra
- **FAQ accordion**: 4 Q&As
- CTA → full crystal page + `/crystals` hub
- JSON-LD: FAQPage + Article

### Category 6 -- Crystal × Astrological House Pages (600 pages)

URL: `/crystals/{crystal-slug}/house/{house-number}`

Houses 1-12

**Page content:**
- H1: `{Crystal} in the {N}th House -- Crystal Remedy for {House Theme}`
- What this crystal does for the themes of this house
- **Effect**: How it supports the positive expression of this house
- **Placement tip**: Where to place (home vastu zone matching this house)
- **Caution**: Any house-crystal conflict to be aware of
- **Best for**: Who should use this combination (transit, natal, progression)
- **FAQ accordion**: 4 Q&As
- CTA → full crystal page
- JSON-LD: FAQPage + Article

### Category 7 -- Crystal × Life Path Number Pages (450 pages)

URL: `/crystals/{crystal-slug}/life-path/{number}`

Life Paths: 1-9

**Page content:**
- H1: `{Crystal} for Life Path {N} -- How This Stone Supports Your Numerology`
- Why this crystal resonates with Life Path {N} energy
- **Synergy level**: High / Medium / Low
- **How to use it**: Specific method tailored to this life path's challenges
- **Career angle**: How this combination helps Life Path {N} professionally
- **Relationship angle**: How it helps in relationships for this life path
- **FAQ accordion**: 4 Q&As
- CTA → full crystal page + Lo Shu Grid calculator
- JSON-LD: FAQPage + Article

### Category 8 -- Chakra Hub Pages (7 pages)

URL: `/crystals/chakra/{chakra-slug}`

**Page content:**
- H1: `Best Crystals for the {Chakra} Chakra -- Top Stones & How to Use Them`
- What this chakra governs and signs it is blocked
- **Top 5 crystals**: Ranked by strength (Primary first), each with 2-3 sentence explanation
- **Placement diagram**: Where to place on the body
- **Chakra meditation**: Step-by-step crystal meditation for this chakra
- **FAQ accordion**: 4 Q&As
- CTA → individual crystal-chakra cross-ref pages

### Category 9 -- Color Ray Pages (10 pages)

URL: `/crystals/color/{color-slug}`

Colors: red, orange, yellow, green, blue, indigo, violet, pink, white-clear, black-grey

**Page content:**
- H1: `{Color} Crystals -- Meaning, Healing Properties & Top Stones`
- What this color ray means in crystal healing
- **Top 6 crystals of this color**: With key properties
- **Color-chakra link**: Which chakra this color primarily heals
- **How to use color therapy**: Practical guide
- **FAQ accordion**: 4 Q&As

### Category 10 -- Element Pages (5 pages)

URL: `/crystals/element/{element-slug}`

Elements: earth, water, fire, air, ether

**Page content:**
- H1: `{Element} Crystals -- Best Stones for {Element} Energy`
- What this element represents in crystal healing
- **Top 8 crystals**: With elemental explanation
- **Who needs these**: Vedic constitution (Vata/Pitta/Kapha) correlation
- **Placement**: Vastu directions for this element
- **FAQ accordion**: 4 Q&As

### Category 11 -- Body/Health Area Pages (200 pages)

URL: `/crystals/body/{body-area-slug}`

200 body systems and areas decoded from the crystal healing book, including:
nervous-system, immune-system, heart-circulation, lungs-respiratory, digestive-system,
kidneys-bladder, liver-gallbladder, reproductive-system, endocrine-hormones, skin,
spine-back, joints-arthritis, headaches-migraines, sleep-insomnia, anxiety-stress,
depression-mood, thyroid, blood-pressure, diabetes-blood-sugar, eye-health, ear-health,
dental-oral, hair-nails, lymphatic-system, chronic-fatigue, inflammation, weight-management,
addiction-recovery, trauma-ptsd, menopause, fertility-reproductive, and ~168 more from the book.

**Page content:**
- H1: `Best Crystals for {Body Area} -- Crystal Healing Guide`
- How crystal healing addresses this area (energetic mechanism from book)
- **Top 3 crystals**: Each with specific mechanism, placement, and duration
- **Placement method**: Exact placement on/near body
- **Complementary practice**: 2-3 lifestyle/holistic tips
- **What to avoid**: Any crystals that are contraindicated for this area
- **FAQ accordion**: 4 Q&As
- CTA → relevant crystal pages
- JSON-LD: FAQPage + Article

### Category 12 -- Crystal Combination Pages (50 pages)

URL: `/crystals/combine/{slug1}-and-{slug2}`

Top 50 most searched crystal pairings, decoded from book recommendations.

**Page content:**
- H1: `{Crystal 1} and {Crystal 2} Together -- Combined Meaning & Uses`
- Why these two crystals work together (synergy mechanism from book)
- **Combined effect**: What this pairing achieves that neither does alone
- **Best intentions for this pair**: Top 3 use cases
- **How to use together**: Carrying, meditation, placement grid
- **Who should use this combination**: Life situations
- **FAQ accordion**: 4 Q&As
- CTA → individual crystal pages

---

## Page Count Summary

| Category | Count |
|---|---|
| Crystal × Chakra | 350 |
| Crystal × Zodiac Sign | 600 |
| Crystal × Vedic Planet | 450 |
| Crystal × Intention | 1,000 |
| Crystal × Nakshatra | 1,350 |
| Crystal × House | 600 |
| Crystal × Life Path | 450 |
| Chakra Hubs | 7 |
| Color Hubs | 10 |
| Element Hubs | 5 |
| Body/Health | 200 |
| Combinations | 50 |
| **New pages (CRY-3)** | **5,072** |
| Existing (CRY-1 + CRY-2) | 113 |
| **Grand Total** | **5,185** |

---

## Technical Requirements

### New files

**Backend:**
```
backend/crystal_xref_data.py          # Full decoded cross-reference data (primary deliverable)
backend/crystal_xref_router.py        # FastAPI router, prefix /api/crystals-xref
backend/scripts/seed_crystal_xref.py  # Seed script (reads MONGO_URL/DB_NAME from env)
```

**Frontend (7 template pages handle all 5,072 routes):**
```
frontend/src/pages/crystals/CrystalChakraPage.jsx      # /crystals/:crystal/chakra/:chakra
frontend/src/pages/crystals/CrystalSignDeepPage.jsx    # /crystals/:crystal/sign/:sign
frontend/src/pages/crystals/CrystalPlanetDeepPage.jsx  # /crystals/:crystal/planet/:planet
frontend/src/pages/crystals/CrystalIntentionDeepPage.jsx # /crystals/:crystal/for/:intention
frontend/src/pages/crystals/CrystalNakshatraPage.jsx   # /crystals/:crystal/nakshatra/:nak
frontend/src/pages/crystals/CrystalHousePage.jsx       # /crystals/:crystal/house/:house
frontend/src/pages/crystals/CrystalLifePathPage.jsx    # /crystals/:crystal/life-path/:n
frontend/src/pages/crystals/ChakraHubPage.jsx          # /crystals/chakra/:chakra
frontend/src/pages/crystals/ColorCrystalPage.jsx       # /crystals/color/:color
frontend/src/pages/crystals/ElementCrystalPage.jsx     # /crystals/element/:element
frontend/src/pages/crystals/BodyAreaPage.jsx           # /crystals/body/:area
frontend/src/pages/crystals/CrystalCombinePage.jsx     # /crystals/combine/:pair
```

### Backend routes (crystal_xref_router.py)

```
GET /api/crystals-xref/{crystal}/chakra/{chakra}
GET /api/crystals-xref/{crystal}/sign/{sign}
GET /api/crystals-xref/{crystal}/planet/{planet}
GET /api/crystals-xref/{crystal}/for/{intention}
GET /api/crystals-xref/{crystal}/nakshatra/{nakshatra}
GET /api/crystals-xref/{crystal}/house/{house}
GET /api/crystals-xref/{crystal}/life-path/{n}
GET /api/crystals-xref/chakra/{chakra}
GET /api/crystals-xref/color/{color}
GET /api/crystals-xref/element/{element}
GET /api/crystals-xref/body/{area}
GET /api/crystals-xref/combine/{pair}
GET /api/crystals-xref/sitemap          → returns all 5,072 URLs
```

### Wire in server.py

```python
from crystal_xref_router import router as crystal_xref_router
app.include_router(crystal_xref_router, prefix="/api/seo")
```

### App.js routes (add BEFORE existing `/crystals/:crystalSlug` catch-all)

```jsx
{/* CRY-3 cross-reference routes -- BEFORE :crystalSlug catch-all */}
<Route path="/crystals/chakra/:chakra" element={<ChakraHubPage />} />
<Route path="/crystals/color/:color" element={<ColorCrystalPage />} />
<Route path="/crystals/element/:element" element={<ElementCrystalPage />} />
<Route path="/crystals/body/:area" element={<BodyAreaPage />} />
<Route path="/crystals/combine/:pair" element={<CrystalCombinePage />} />
<Route path="/crystals/:crystal/chakra/:chakra" element={<CrystalChakraPage />} />
<Route path="/crystals/:crystal/sign/:sign" element={<CrystalSignDeepPage />} />
<Route path="/crystals/:crystal/planet/:planet" element={<CrystalPlanetDeepPage />} />
<Route path="/crystals/:crystal/for/:intention" element={<CrystalIntentionDeepPage />} />
<Route path="/crystals/:crystal/nakshatra/:nak" element={<CrystalNakshatraPage />} />
<Route path="/crystals/:crystal/house/:house" element={<CrystalHousePage />} />
<Route path="/crystals/:crystal/life-path/:n" element={<CrystalLifePathPage />} />
```

### Sitemap update in seo_router.py

New endpoint:
```
GET /api/seo/sitemap/crystals-xref    # 5,072 URLs
```

Add to `sitemap-index.xml`.

### Vercel cache headers

Add these patterns to `vercel.json` with `s-maxage=86400`:
```
/crystals/*/chakra/*
/crystals/*/sign/*
/crystals/*/planet/*
/crystals/*/for/*
/crystals/*/nakshatra/*
/crystals/*/house/*
/crystals/*/life-path/*
/crystals/chakra/*
/crystals/color/*
/crystals/element/*
/crystals/body/*
/crystals/combine/*
```

### Seed script pattern

`seed_crystal_xref.py` must follow the same pattern as `seed_crystals.py`:
- Read `MONGO_URL` and `DB_NAME` from `os.environ` (no required argparse args)
- Use `motor.motor_asyncio.AsyncIOMotorClient`
- Upsert into MongoDB collections:
  - `crystal_chakra` (350 docs)
  - `crystal_sign_deep` (600 docs)
  - `crystal_planet_deep` (450 docs)
  - `crystal_intention_deep` (1,000 docs)
  - `crystal_nakshatra` (1,350 docs)
  - `crystal_house` (600 docs)
  - `crystal_life_path` (450 docs)
  - `crystal_chakra_hubs` (7 docs)
  - `crystal_colors` (10 docs)
  - `crystal_elements` (5 docs)
  - `crystal_body_areas` (200 docs)
  - `crystal_combinations` (50 docs)

---

## Architecture Rules

1. **Do NOT modify** `backend/crystal_data.py`, `backend/crystal_router.py`, or any CRY-1/CRY-2 files
2. **Do NOT modify** any existing crystal JSX pages
3. All new routes go into `crystal_xref_router.py` -- separate file from `crystal_router.py`
4. `crystal_xref_data.py` imports nothing from `crystal_data.py` -- it is a standalone data file
5. GlassCard pattern, Gold accent, Tailwind only
6. `SEO` component + JSON-LD on every page
7. All content is original Codex writing decoded from source books -- no direct reproduction
8. Internal links: every cross-ref page links back to the main crystal page AND the relevant hub
9. Sitemap for CRY-3 is a separate endpoint so it can be paginated if needed

---

## Delivery Order (Recommended)

Deliver in this order to keep each part testable:

1. **`crystal_xref_data.py`** -- the book-decoded data (most important, batch across multiple Write calls: 5 crystals per call)
2. **`crystal_xref_router.py`** -- all backend routes
3. **`seed_crystal_xref.py`** -- seed script
4. **Frontend pages** (12 JSX files -- can be delivered as batches: cross-ref templates first, hub pages second)
5. **App.js + server.py + seo_router.py + vercel.json** wiring

---

## Acceptance Checklist

- [ ] `crystal_xref_data.py` covers all 50 crystals × all 12 dimensions with book-decoded content
- [ ] 350 chakra pages render with placement + practice + affirmation
- [ ] 600 sign pages render with affinity level + shadow help + wear guidance
- [ ] 450 planet pages render with mantra + metal + day + who benefits
- [ ] 1,000 intention pages render with ritual + affirmation + placement
- [ ] 1,350 nakshatra pages render with Vedic remedy + mantra
- [ ] 600 house pages render with effect + vastu placement
- [ ] 450 life path pages render with synergy level + career/relationship angles
- [ ] 7 chakra hubs render with top 5 crystals + meditation
- [ ] 10 color pages render with top 6 crystals + color-chakra link
- [ ] 5 element pages render with top 8 crystals + Ayurvedic correlation
- [ ] 200 body area pages render with top 3 crystals + placement method
- [ ] 50 combination pages render with synergy + top 3 use cases
- [ ] No route conflict with existing CRY-1/CRY-2 routes
- [ ] Sitemap returns 5,072 URLs
- [ ] Seed script runs cleanly from `/app` with no args
- [ ] Build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
