# CRY-2 Commission Brief -- Crystal Healing Expansion (Textbook-Decoded Pages)
> Thread: Crystal Healing Codex Thread (same thread as CRY-1)
> Commission ID: CRY-2
> Date: 2026-05-26
> Status: READY TO ISSUE
> Prerequisite: CRY-1 integrated ✅

---

## Objective

CRY-1 built the structural foundation (50 crystal pages, 20 intention pages, calculator, hub).

**CRY-2 adds three new page categories derived from decoded textbook content:**

1. **Planet-Crystal pages** -- "Best Crystals for [Planet] in Your Chart" (9 pages, one per Vedic planet)
2. **Sign-Crystal pages** -- "Best Crystals for [Sign]" (12 pages, one per rashi)
3. **Problem-Area pages** -- "Crystals for [Specific Problem]" (20 pages, decoded from source PDFs)

**Total new pages: 41**  
**New sitemap total: 72 (CRY-1) + 41 (CRY-2) = 113 pages**

---

## Source Material (Decoded Data -- Use as Reference)

All content must be original Codex writing inspired by these sources. No direct quotes.

```
Primary textbook:
/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/Crystal Healing/7. Crystal Healing.pdf

Secondary textbook:
/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/Crystal Healing/Proofread-Gemstones-book-copy.pdf

Pre-decoded structured data:
/Users/apple/Documents/Knowledge Engine_eBooks/Remedies + The Strategist/3. Remedies_Gemstones.md
/Users/apple/Documents/Knowledge Engine_eBooks/Remedies + The Strategist/4. Crystal Remedies_JSON.md
/Users/apple/Documents/Knowledge Engine_eBooks/Remedies + The Strategist/5. 7 Chakra Healing_JSON _ Brief Docs.md
/Users/apple/Documents/Knowledge Engine_eBooks/DestinyNumerology_CC_Decode/Numerology_Ch17_GemstoneNumerology_Rules.json
```

---

## Page Category 1 -- Planet-Crystal Pages (9 pages)

### URL Pattern
```
/crystals/for/planet/{planet-slug}
```

### Planets & Slugs
| Planet | Slug | Primary Vedic Gemstone |
|---|---|---|
| Sun | `sun` | Ruby |
| Moon | `moon` | Pearl |
| Mars | `mars` | Red Coral |
| Mercury | `mercury` | Emerald |
| Jupiter | `jupiter` | Yellow Sapphire |
| Venus | `venus` | Diamond / Clear Quartz |
| Saturn | `saturn` | Blue Sapphire |
| Rahu | `rahu` | Hessonite Garnet |
| Ketu | `ketu` | Cat's Eye |

### Page Content Template
- H1: `Best Crystals for [Planet] -- Vedic Gemstones & Healing Stones`
- Intro: Planet's energy in Vedic astrology (2-3 sentences)
- **Primary Vedic Gemstone card**: Name, wearing instructions (metal, finger, mantra, activation), who should wear
- **Supporting healing crystals** (3-4 cards): Western crystals that amplify the planet's positive energy
- **Crystals to avoid** (1-2): Which stones conflict with this planet
- **How to use** section: 3 practical steps
- **FAQ accordion**: 5 Q&As (e.g., "Which finger for Sun gemstone?", "Can I wear Ruby without consulting an astrologer?")
- CTA → `/crystals/calculator`
- SEO: `JSON-LD FAQPage + Article`
- Meta title: `Best Crystals for [Planet] -- Vedic Gemstones & Healing Stones | EverydayHoroscope`

---

## Page Category 2 -- Sign-Crystal Pages (12 pages)

### URL Pattern
```
/crystals/for/sign/{sign-slug}
```

### Signs
aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius, pisces

### Page Content Template
- H1: `Best Crystals for [Sign] -- Healing Stones for [Sign] Energy`
- Intro: Sign's nature (element, ruling planet, key traits) -- 2-3 sentences
- **Signature crystals grid** (3-5): Each with name, why it works for this sign, how to use
- **Crystals for [Sign]'s shadow side**: 2-3 crystals addressing the sign's common challenges (e.g., Aries: impulsiveness → Amethyst)
- **Monthly crystal ritual**: Simple monthly practice aligned with this sign's season
- **FAQ accordion**: 4 Q&As
- CTA → `/crystals/calculator`
- Meta title: `Best Crystals for [Sign] -- Healing Stones for [Sign] Energy | EverydayHoroscope`

---

## Page Category 3 -- Problem-Area Pages (20 pages)

Derived from decoded textbook problem-area content. Each page addresses a specific life challenge.

### URL Pattern
```
/crystals/for/problem/{problem-slug}
```

### Problem Areas & Slugs
| Problem | Slug |
|---|---|
| Broken Sleep / Insomnia | `insomnia` |
| Relationship Conflict | `relationship-conflict` |
| Career Stagnation | `career-stagnation` |
| Financial Loss | `financial-loss` |
| Exam Stress / Study Focus | `exam-stress` |
| Grief / Bereavement | `grief` |
| Anxiety Attacks | `anxiety-attacks` |
| Low Self-Confidence | `low-confidence` |
| Toxic Work Environment | `toxic-workplace` |
| Addiction Recovery | `addiction` |
| Chronic Fatigue | `chronic-fatigue` |
| Digestive Issues | `digestive-issues` |
| Heart Chakra Blockage | `heart-chakra-blockage` |
| Third Eye Activation | `third-eye-activation` |
| Root Chakra Imbalance | `root-chakra-imbalance` |
| EMF / Tech Sensitivity | `emf-sensitivity` |
| Negative Energy Clearing | `negative-energy` |
| Past Trauma Release | `past-trauma` |
| Manifestation Block | `manifestation-block` |
| Loneliness / Isolation | `loneliness` |

### Page Content Template
- H1: `Crystals for [Problem] -- Best Healing Stones & How to Use Them`
- Intro: What causes this problem energetically (2-3 sentences)
- **Top 3 crystals** (large cards): Name, why it works for this problem, exact usage (placement, wear, meditation)
- **Supporting crystals** (3-4 smaller cards)
- **Crystal grid suggestion**: Simple 3-5 stone layout for this problem
- **Affirmation**: 1 short affirmation paired with the primary crystal
- **FAQ accordion**: 5 Q&As
- CTA → `/crystals/calculator`
- Meta title: `Crystals for [Problem] -- Best Healing Stones | EverydayHoroscope`

---

## Technical Requirements

### Backend additions to `crystal_data.py`

Add three new data dictionaries:
```python
PLANET_CRYSTAL_DATA = { "sun": {...}, "moon": {...}, ... }   # 9 planets
SIGN_CRYSTAL_DATA = { "aries": {...}, "taurus": {...}, ... }  # 12 signs
PROBLEM_CRYSTAL_DATA = { "insomnia": {...}, ... }             # 20 problems
```

Add three new sitemap helper functions:
```python
def get_planet_crystal_sitemap_urls() -> list[str]  # 9 URLs
def get_sign_crystal_sitemap_urls() -> list[str]    # 12 URLs
def get_problem_crystal_sitemap_urls() -> list[str] # 20 URLs
```

### Backend additions to `crystal_router.py`

```
GET /api/crystals/planet/{planet_slug}     → planet crystal page data
GET /api/crystals/sign/{sign_slug}         → sign crystal page data
GET /api/crystals/problem/{problem_slug}   → problem crystal page data
```

### Sitemap update in `seo_router.py`

Update the existing `/api/seo/sitemap/crystals` endpoint to include all 113 URLs (existing 72 + 41 new).

### New frontend pages

```
frontend/src/pages/crystals/CrystalPlanetPage.jsx    # /crystals/for/planet/:planet
frontend/src/pages/crystals/CrystalSignPage.jsx      # /crystals/for/sign/:sign
frontend/src/pages/crystals/CrystalProblemPage.jsx   # /crystals/for/problem/:problem
```

### App.js route additions

```jsx
<Route path="/crystals/for/planet/:planet" element={<CrystalPlanetPage />} />
<Route path="/crystals/for/sign/:sign" element={<CrystalSignPage />} />
<Route path="/crystals/for/problem/:problem" element={<CrystalProblemPage />} />
```

**Important:** These routes must be added BEFORE the existing `/crystals/for/:intentionSlug` catch-all route to avoid route conflicts.

### Seed script update

Update `backend/scripts/seed_crystals.py` to also seed planet, sign, and problem collections.

### Vercel cache headers

Add to `frontend/vercel.json` (pattern already covers `/crystals/*` -- no change needed if wildcard is already present).

---

## Acceptance Checklist

- [ ] 9 planet pages render at `/crystals/for/planet/{slug}` with Vedic gemstone + supporting crystals
- [ ] 12 sign pages render at `/crystals/for/sign/{slug}` with signature crystals + shadow crystals
- [ ] 20 problem pages render at `/crystals/for/problem/{slug}` with top crystals + crystal grid
- [ ] All pages include FAQ accordion, CTA to calculator, SEO component, JSON-LD
- [ ] Sitemap returns 113 URLs (72 existing + 41 new)
- [ ] Seed script seeds all new documents
- [ ] No route conflict with existing `/crystals/for/:intentionSlug` -- planet/sign/problem prefix the URL correctly
- [ ] Build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
