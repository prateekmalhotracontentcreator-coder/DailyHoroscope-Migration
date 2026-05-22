# TAR-SEO-1 Commission Brief
> Thread: Tarot SEO Codex Thread  
> Module: Tarot SEO Pages (Batch 6) + Spread Add-On  
> Maps to: SEO 20K Batch 6  
> Pages: ~5,000 (78 cards × top 60 spreads = 4,680) + hub + spread index + card index  
> Date: 2026-05-23  
> Status: READY TO BUILD -- EPUB source available, existing Tarot page live

---

## Context

EverydayHoroscope (`everydayhoroscope.in`) is a live React 18 + FastAPI + MongoDB + Tailwind CSS platform. A Tarot module already exists at `/tarot` (draws + spreads + history). This commission adds a **Tarot SEO layer** -- high-traffic pages for every card × spread combination, plus card and spread index pages.

**Repo:** `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`  
**Stack:** React 18 · FastAPI · MongoDB · Tailwind CSS

**Source material (single source -- do not copy, use as reference):**
```
/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/Tarot/
  1001-tarot-spreads-the-complete-book-of-tarot-spreads-for-every-purpose.epub
```

The EPUB is a zip archive of HTML/XML files. To extract content:
1. Copy the file, rename with `.zip` extension, unzip
2. Content is in `OEBPS/` or similar folder -- HTML chapter files
3. Extract spread names, spread descriptions, card positions from chapter HTML

**Copyright compliance is mandatory:** All page content must be original Codex writing inspired by tarot traditions. No paragraph reproduction from the EPUB. Spread names may be used (titles are not copyrightable) -- descriptions and position interpretations must be original writing.

---

## Module Architecture

### URL Patterns

| URL | Purpose |
|---|---|
| `/tarot/cards/` | Card index hub -- 78 cards grid |
| `/tarot/cards/{card-slug}/` | Individual card page (78 pages) |
| `/tarot/spreads/` | Spread index hub -- top 60 spreads |
| `/tarot/spreads/{spread-slug}/` | Spread detail page (60 pages) |
| `/tarot/cards/{card-slug}/{spread-slug}/` | Card × Spread combination page (~4,680 pages) |

**Total scope:**
- 1 card hub + 78 card pages = 79 pages
- 1 spread hub + 60 spread pages = 61 pages  
- 78 × 60 = 4,680 card×spread pages
- **Grand total: ~4,820 pages**

---

## The 78 Tarot Cards

**Major Arcana (22):**
the-fool, the-magician, the-high-priestess, the-empress, the-emperor, the-hierophant, the-lovers, the-chariot, strength, the-hermit, wheel-of-fortune, justice, the-hanged-man, death, temperance, the-devil, the-tower, the-star, the-moon, the-sun, judgement, the-world

**Minor Arcana -- Wands (14):**
ace-of-wands, two-of-wands, three-of-wands, four-of-wands, five-of-wands, six-of-wands, seven-of-wands, eight-of-wands, nine-of-wands, ten-of-wands, page-of-wands, knight-of-wands, queen-of-wands, king-of-wands

**Minor Arcana -- Cups (14):**
ace-of-cups, two-of-cups, three-of-cups, four-of-cups, five-of-cups, six-of-cups, seven-of-cups, eight-of-cups, nine-of-cups, ten-of-cups, page-of-cups, knight-of-cups, queen-of-cups, king-of-cups

**Minor Arcana -- Swords (14):**
ace-of-swords, two-of-swords, three-of-swords, four-of-swords, five-of-swords, six-of-swords, seven-of-swords, eight-of-swords, nine-of-swords, ten-of-swords, page-of-swords, knight-of-swords, queen-of-swords, king-of-swords

**Minor Arcana -- Pentacles (14):**
ace-of-pentacles, two-of-pentacles, three-of-pentacles, four-of-pentacles, five-of-pentacles, six-of-pentacles, seven-of-pentacles, eight-of-pentacles, nine-of-pentacles, ten-of-pentacles, page-of-pentacles, knight-of-pentacles, queen-of-pentacles, king-of-pentacles

---

## The 60 Target Spreads

Extract from EPUB -- select the 60 highest-traffic spread types based on these priorities:
1. Universal spreads (Celtic Cross, Three-Card, Past-Present-Future, Yes/No, etc.)
2. Love + Relationship spreads
3. Career + Money spreads
4. Daily guidance spreads
5. Healing + Spiritual growth spreads

**Slugs must be URL-safe kebab-case.** Example spread slugs:
`celtic-cross`, `three-card-spread`, `past-present-future`, `yes-or-no`, `love-reading`, `twin-flame-spread`, `career-path`, `monthly-forecast`, `chakra-spread`, `horseshoe-spread`

---

## Backend

### Router File
`backend/tarot_seo_router.py`

Register in `backend/server.py` as: `app.include_router(tarot_seo_router, prefix="/api/seo")`

**Note:** Do NOT modify existing `backend/tarot_router.py` -- the new SEO router is additive only.

### Endpoints

```
GET /api/seo/tarot/cards                        → list of 78 cards with meta
GET /api/seo/tarot/cards/{card_slug}            → card page content
GET /api/seo/tarot/spreads                      → list of 60 spreads
GET /api/seo/tarot/spreads/{spread_slug}        → spread detail content
GET /api/seo/tarot/cards/{card_slug}/{spread_slug}  → card×spread combination content
GET /api/seo/sitemap/tarot-seo                  → sitemap URL list (top 1,000 priority URLs)
```

### MongoDB Collections

**Collection: `tarot_cards`** -- 78 documents

```json
{
  "slug": "the-fool",
  "display_name": "The Fool",
  "arcana": "major",
  "suit": null,
  "number": 0,
  "keywords": ["new beginnings", "innocence", "spontaneity", "adventure", "potential"],
  "upright_meaning": "2-3 sentences -- core upright meaning (original Codex writing)",
  "reversed_meaning": "2-3 sentences -- core reversed meaning",
  "element": "Air",
  "yes_or_no": "Yes",
  "zodiac": "Uranus / Aquarius",
  "numerology": 0,
  "key_themes": ["career", "love", "spiritual-growth"],
  "faq": [
    { "q": "What does The Fool tarot card mean?", "a": "..." },
    { "q": "Is The Fool a good card?", "a": "..." },
    { "q": "What does The Fool mean in love?", "a": "..." },
    { "q": "What does The Fool reversed mean?", "a": "..." },
    { "q": "What number is The Fool in tarot?", "a": "..." }
  ],
  "related_cards": ["the-magician", "the-world", "ace-of-wands"],
  "meta_title": "The Fool Tarot Card -- Meaning, Upright, Reversed & Spreads | EverydayHoroscope",
  "meta_description": "The Fool tarot card meaning: new beginnings, innocence, and limitless potential. Discover upright and reversed meanings, love, career, and spread interpretations."
}
```

**Collection: `tarot_spreads`** -- 60 documents

```json
{
  "slug": "celtic-cross",
  "display_name": "Celtic Cross",
  "positions": 10,
  "intent": "general",
  "difficulty": "intermediate",
  "description": "2-3 sentences -- what this spread is for and when to use it",
  "position_names": [
    "The Present", "The Challenge", "The Past", "The Future",
    "Above (Conscious)", "Below (Unconscious)", "Advice", "External Influences",
    "Hopes and Fears", "Outcome"
  ],
  "best_questions": ["What is the overall energy of my situation?", "What challenges am I facing?"],
  "when_to_use": "When you need a comprehensive overview of any complex situation",
  "faq": [
    { "q": "What is the Celtic Cross tarot spread?", "a": "..." },
    { "q": "How do I read a Celtic Cross spread?", "a": "..." },
    { "q": "How many cards are in a Celtic Cross?", "a": "..." },
    { "q": "What does each position mean in Celtic Cross?", "a": "..." },
    { "q": "Is Celtic Cross good for beginners?", "a": "..." }
  ],
  "meta_title": "Celtic Cross Tarot Spread -- How to Read All 10 Positions | EverydayHoroscope",
  "meta_description": "The Celtic Cross is the most complete tarot spread -- 10 positions covering past, present, future, and hidden influences. Learn to read each position with any card."
}
```

**Collection: `tarot_combinations`** -- 4,680 documents (78 × 60)

```json
{
  "card_slug": "the-fool",
  "spread_slug": "celtic-cross",
  "interpretation": {
    "opening": "2 sentences -- what it means when The Fool appears in a Celtic Cross reading",
    "by_position": [
      { "position": "The Present", "meaning": "The Fool here signals a fresh start is upon you..." },
      { "position": "The Challenge", "meaning": "..." }
    ],
    "overall_message": "2-3 sentences -- the combined energy of this card in this spread",
    "action": "1 concrete action step"
  },
  "meta_title": "The Fool in Celtic Cross -- What It Means in Each Position | EverydayHoroscope",
  "meta_description": "The Fool tarot card in a Celtic Cross spread. Discover what The Fool means in each of the 10 positions -- from Present to Outcome."
}
```

**Important -- seeding 4,680 documents:**  
Use a systematic generation approach. Codex writes the card-level + spread-level content fully, then generates combination documents using a template pattern:
- Opening: `[Card upright keyword] energy meets [spread intent] -- [1-sentence synthesis]`
- By-position: for each spread position, combine card meaning with position meaning
- The content does NOT need to be deeply unique for every combination -- it must be coherent and useful

### Seed Scripts
```
backend/scripts/seed_tarot_cards.py       # 78 documents
backend/scripts/seed_tarot_spreads.py     # 60 documents
backend/scripts/seed_tarot_combinations.py  # 4,680 documents
```

Each script is self-contained and can run independently.

---

## Frontend

### Card Hub Page
**File:** `frontend/src/pages/seo/TarotCardHubPage.jsx`

**Page content:**
- H1: `Tarot Card Meanings -- All 78 Cards Explained`
- Filter tabs: All · Major Arcana · Wands · Cups · Swords · Pentacles
- **78-card grid:** GlassCards -- card name, arcana/suit badge, 1-line keyword summary, link to card page
- **Popular spreads strip:** 5 spread pills
- **FAQ accordion:** 5 questions
- JSON-LD: `FAQPage` + `BreadcrumbList`

### Card Detail Page
**File:** `frontend/src/pages/seo/TarotCardPage.jsx`

**Page content:**
- H1: `{Card Name} Tarot Card -- Meaning, Upright & Reversed`
- **Card metadata strip:** Arcana · Element · Yes/No · Zodiac · Number -- 5 chips
- **Keywords:** 5-7 gold pills
- **Upright meaning:** 2-3 sentences
- **Reversed meaning:** 2-3 sentences
- **Spread navigator:** "See {Card} in a specific spread" -- pill grid of all 60 spreads, each → combination page
- **Related cards:** 3 cards
- **FAQ accordion:** 5 questions
- **CTA:** "Do a Tarot Reading Now" → `/tarot`
- JSON-LD: `FAQPage` + `Article`

### Spread Hub Page
**File:** `frontend/src/pages/seo/TarotSpreadHubPage.jsx`

**Page content:**
- H1: `Tarot Spreads -- 60 Layouts for Every Question`
- Filter by intent: General · Love · Career · Daily · Spiritual
- **60-spread grid:** GlassCards -- spread name, position count, intent badge, 1-line description, link
- **FAQ accordion:** 5 questions
- JSON-LD: `FAQPage`

### Spread Detail Page
**File:** `frontend/src/pages/seo/TarotSpreadPage.jsx`

**Page content:**
- H1: `{Spread Name} -- How to Lay It Out & Read Every Position`
- **Spread overview:** positions count, difficulty, intent, when to use
- **Position guide:** Numbered list -- position name + what it reveals
- **Best questions to ask:** 3-5 bullets
- **Card meaning quick-links:** "What does [any card] mean here?" → combo page
- **FAQ accordion:** 5 questions
- **CTA:** "Try this spread now" → `/tarot`
- JSON-LD: `FAQPage` + `HowTo`

### Card × Spread Combination Page
**File:** `frontend/src/pages/seo/TarotCombinationPage.jsx`

**Page content:**
- H1: `{Card Name} in a {Spread Name} -- What It Means in Each Position`
- **Opening:** 2-sentence synthesis
- **By-position accordion:** Each position as an expandable -- position name header, card meaning in that position
- **Overall message:** 2-3 sentences
- **Action step:** 1 concrete action
- **Try this spread CTA:** → `/tarot`
- **Explore other cards in this spread:** 3 related card×spread combos
- JSON-LD: `FAQPage` + `Article`

---

## SEO Metadata Formulas

### Card Hub
- **Title:** `Tarot Card Meanings -- All 78 Cards Upright & Reversed | EverydayHoroscope`
- **Description:** `Explore all 78 tarot cards -- Major Arcana, Wands, Cups, Swords, and Pentacles. Upright and reversed meanings for love, career, and spiritual guidance.`

### Card Page
- **Title:** `{Card Name} Tarot Card -- Meaning, Upright, Reversed & {Suit/Arcana} | EverydayHoroscope`
- **Description:** `{Card Name} tarot card means {keyword1} and {keyword2}. Discover upright and reversed meanings for love, career, and every spread type.`

### Spread Page
- **Title:** `{Spread Name} -- Tarot Spread Layout, Positions & How to Read | EverydayHoroscope`
- **Description:** `The {Spread Name} is a {N}-card tarot spread for {intent}. Learn each position's meaning and how to read this layout for any question.`

### Combination Page
- **Title:** `{Card Name} in {Spread Name} -- Position-by-Position Guide | EverydayHoroscope`
- **Description:** `{Card Name} appearing in a {Spread Name} spread? Discover what it means in each position -- from {position1} to {positionN}.`

---

## Routes (App.js additions)

```jsx
<Route path="/tarot/cards" element={<TarotCardHubPage />} />
<Route path="/tarot/cards/:cardSlug" element={<TarotCardPage />} />
<Route path="/tarot/spreads" element={<TarotSpreadHubPage />} />
<Route path="/tarot/spreads/:spreadSlug" element={<TarotSpreadPage />} />
<Route path="/tarot/cards/:cardSlug/:spreadSlug" element={<TarotCombinationPage />} />
```

All routes: public, no auth gate. **Do NOT modify existing `/tarot` route.**

---

## Sitemap

Add to `backend/seo_router.py`:
```python
GET /api/seo/sitemap/tarot-seo   # Returns top 1,000 priority URLs (Major Arcana × all spreads + all card hubs + spread hubs)
```

Full 4,820 URLs available via pagination parameter: `?page=1`, `?page=2`, etc. Sitemap index references multiple sub-sitemaps if needed.

Add to `frontend/public/sitemap-index.xml`.

---

## Technical Requirements

- New React pages in `frontend/src/pages/seo/` (5 files)
- New FastAPI router: `backend/tarot_seo_router.py` -- prefix `/api/seo`
- **Do NOT modify** `backend/tarot_router.py`
- Register new router in `backend/server.py`
- New routes in `frontend/src/App.js` (public, no auth gate)
- Sitemap endpoint added to `backend/seo_router.py`
- Cache headers in `frontend/vercel.json` (s-maxage=86400) for `/tarot/cards/*` and `/tarot/spreads/*`
- 3 MongoDB seed scripts
- `SEO` component from `frontend/src/components/SEO.jsx` on every page

**EPUB extraction note for Codex:**  
The source EPUB is at: `/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/Tarot/1001-tarot-spreads-the-complete-book-of-tarot-spreads-for-every-purpose.epub`  
It is 22MB. Treat it as a zip file: copy + rename to `.zip`, unzip, find HTML files in `OEBPS/` or equivalent, parse with BeautifulSoup or html.parser to extract spread names, position names, and descriptions. Copyright compliance: extract spread names and position structures only -- all prose is original Codex writing.

**Tailwind / theme:** GlassCard pattern (`rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`). Gold accent `#c5a059`. No new dependencies.

**Build verification:** `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` -- must pass clean.

---

## Acceptance Checklist

- [ ] Card hub renders at `/tarot/cards/` with all 78 cards filterable
- [ ] 78 card pages render at `/tarot/cards/{slug}/`
- [ ] Spread hub renders at `/tarot/spreads/` with all 60 spreads
- [ ] 60 spread pages render at `/tarot/spreads/{slug}/`
- [ ] Sample combination pages render at `/tarot/cards/{card}/{spread}/`
- [ ] Sitemap endpoint returns ≥1,000 URLs (priority Major Arcana × all spreads)
- [ ] Existing `/tarot` route untouched -- original Tarot page still works
- [ ] Routes wired in App.js -- all new pages HTTP 200
- [ ] Vercel cache headers applied to new Tarot SEO routes
- [ ] All 3 seed scripts run without errors (78 + 60 + 4,680 docs)
- [ ] Build clean -- zero errors
- [ ] JSON-LD on all 5 page types
- [ ] SEO meta applied on all pages
- [ ] EPUB content used as reference only -- all prose is original Codex writing
