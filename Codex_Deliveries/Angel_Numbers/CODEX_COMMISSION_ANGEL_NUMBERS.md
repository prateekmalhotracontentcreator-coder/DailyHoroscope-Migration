# ANGEL-1 Commission Brief
> Thread: Angel Numbers Codex Thread  
> Module: Angel Numbers SEO + Hub  
> Maps to: SEO 20K Batch 5  
> Pages: ~9,000 (1,000 numbers × 9 intents) + hub pages  
> Date: 2026-05-23  
> Status: READY TO BUILD -- all engines available, no dependencies

---

## Context

EverydayHoroscope (`everydayhoroscope.in`) is a live React 18 + FastAPI + MongoDB + Tailwind CSS platform. This commission adds the Angel Numbers module -- a high-traffic SEO cluster covering 1,000 angel numbers across 9 intent categories.

**Repo:** `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`  
**Stack:** React 18 · FastAPI · MongoDB · Tailwind CSS  
**Internal engine:** `backend/vedic_calculator.py` -- for any birth-chart data. Do NOT add calculation logic to any other file.

**Source material (do not copy -- use as reference for Codex-written original content):**
- `Angel Numbers -- Kyle Gray.pdf` -- numerological meanings per number, spiritual themes
- `Angel Numbers -- Fortuna Noir.pdf` -- intent-based guidance, affirmations

All content must be **original Codex writing** inspired by angel number traditions -- not reproduced from any source. Copyright compliance is mandatory: no direct quotes, no paragraph reproduction.

---

## Module Architecture

### URL Patterns

| URL | Purpose |
|---|---|
| `/angel-numbers/` | Hub page -- what are angel numbers, number range grid, intent guides |
| `/angel-numbers/{number}/` | Core number page (1-999, plus 1000, 1111, 1212, 2222 etc.) |
| `/angel-numbers/{number}/{intent}/` | Intent-specific deep dive |

**Phase 1 scope (this commission):**
- Hub page
- Core number pages: **111, 222, 333, 444, 555, 666, 777, 888, 999, 000** (top 10 highest-traffic repeating numbers) + all **double-digit** repetitions (11, 22, 33, 44, 55, 66, 77, 88, 99) = **19 core number pages**
- Intent pages for all 19 core numbers × 9 intents = **171 intent pages**
- Total Phase 1: **191 pages** (1 hub + 19 core + 171 intent)

**Phase 2 (future brief):** Expand to full 1,000 numbers using the same patterns established here.

### Intent Categories (9 total)

| Slug | Display Name |
|---|---|
| `love` | Love & Relationships |
| `career` | Career & Money |
| `twin-flame` | Twin Flame |
| `manifestation` | Manifestation |
| `health` | Health & Wellbeing |
| `spiritual-growth` | Spiritual Growth |
| `family` | Family & Home |
| `protection` | Protection & Guidance |
| `new-beginnings` | New Beginnings |

---

## Backend

### Router File
`backend/angel_numbers_router.py`

Register in `backend/server.py` as: `app.include_router(angel_numbers_router, prefix="/api/seo")`

### Endpoints

```
GET /api/seo/angel-numbers/{number}           → core number data + all 9 intent summaries
GET /api/seo/angel-numbers/{number}/{intent}  → full intent-specific content
GET /api/seo/angel-numbers/hub                → hub metadata
GET /api/seo/sitemap/angel-numbers            → sitemap URLs list
```

### MongoDB Collections

**Collection: `angel_number_core`**
One document per number:
```json
{
  "number": "111",
  "display": "111",
  "headline": "111 Angel Number -- Meaning, Message & What To Do",
  "summary": "2-sentence punchy hook",
  "numerology_base": "1",
  "key_themes": ["manifestation", "new beginnings", "alignment", "divine spark", "leadership"],
  "vibration": "High-frequency activation number...",
  "seeing_it_means": "3-4 sentences -- what it means when you keep seeing 111",
  "what_to_do": ["3 concrete actions"],
  "affirmation": "I am aligned with divine timing...",
  "meta_title": "111 Angel Number Meaning -- Signs, Love, Career & More | EverydayHoroscope",
  "meta_description": "Seeing 111 everywhere? Discover the meaning of angel number 111 -- messages for love, career, twin flame, and manifestation."
}
```

**Collection: `angel_number_intents`**
One document per number+intent combination:
```json
{
  "number": "111",
  "intent": "love",
  "headline": "111 Angel Number in Love -- What the Angels Want You to Know",
  "opening": "2-sentence hook specific to this number+intent",
  "message": "3-4 sentences -- the angel's message for this intent",
  "action_steps": ["3-4 specific actions to take"],
  "affirmation": "Intent-specific affirmation",
  "faq": [
    { "q": "What does 111 mean for love?", "a": "..." },
    { "q": "Is 111 a twin flame number?", "a": "..." },
    { "q": "Does 111 mean someone is thinking of you?", "a": "..." },
    { "q": "What should I do when I see 111 in love?", "a": "..." },
    { "q": "Is 111 a good sign for relationships?", "a": "..." }
  ],
  "related_numbers": ["222", "444", "1111"],
  "meta_title": "111 Angel Number Love Meaning -- Twin Flame & Relationships | EverydayHoroscope",
  "meta_description": "Angel number 111 in love signals alignment and new beginnings. Discover what 111 means for your relationship, twin flame connection, and heart matters."
}
```

### Seed Script
`backend/scripts/seed_angel_numbers.py`

Must seed all documents for Phase 1 (19 core numbers × 9 intents = 171 intent docs + 19 core docs + 1 hub doc). Content is Codex-authored directly in the seed script -- original writing, not copied from sources.

---

## Frontend

### Hub Page
**File:** `frontend/src/pages/seo/AngelNumbersHubPage.jsx`

**Page content:**
- H1: `Angel Numbers -- Meanings, Messages & What They Mean for You`
- Intro paragraph: What are angel numbers? (3-4 sentences, original Codex writing)
- **Number spotlight grid:** Cards for the 19 Phase 1 numbers, each linking to their core page. GlassCard style, gold number display, 1-line theme label.
- **Intent guides strip:** 9 intent pills -- clicking filters the grid to show numbers strong for that intent
- **How to work with angel numbers:** 4-step short list
- **FAQ accordion:** 5 questions (What are angel numbers? Are they real? Why do I keep seeing the same number? etc.)
- JSON-LD: `FAQPage` + `BreadcrumbList`
- SEO: Title: `Angel Numbers -- Meanings, Sequences & Messages | EverydayHoroscope` · Description: `Discover the meaning of every angel number. From 111 to 999, explore messages for love, career, twin flame, and spiritual growth.`

### Core Number Page
**File:** `frontend/src/pages/seo/AngelNumberPage.jsx`

**Page content:**
- H1: `{Number} Angel Number -- Meaning, Message & What To Do`
- **Gold number hero:** Large Cinzel display of the number with a 1-line vibration summary
- **Seeing it means:** 3-4 sentence explanation
- **Key themes:** 5-7 gold pills (manifestation / alignment / leadership etc.)
- **What to do:** 3 concrete action steps (bullets)
- **Intent navigator:** 9 intent tab/pill links -- each routes to the intent page. Shows a 1-line preview of the intent message.
- **Affirmation block:** Gold-bordered card with affirmation text (italic Playfair)
- **Related numbers:** 3-4 cards linking to related number pages
- **FAQ accordion:** 5 questions
- **CTA:** "Check your personal numbers" → `/birth-chart` (birth chart reveals life path number)
- JSON-LD: `FAQPage` + `Article`

### Intent Page
**File:** `frontend/src/pages/seo/AngelNumberIntentPage.jsx`

**Page content:**
- H1: `{Number} Angel Number {IntentDisplayName} -- {Punchy Subtitle}`
  - Example: `111 Angel Number Love -- What the Angels Want You to Know`
- **Opening hook:** 2 sentences, intent-specific
- **Angel's message:** 3-4 sentences
- **Action steps:** 3-4 bullets -- specific and actionable
- **Affirmation block:** Gold-bordered, italic Playfair
- **Related intents:** Pill strip linking to other intent pages for same number
- **Related numbers for {intent}:** 3 other numbers strong for this intent
- **FAQ accordion:** 5 questions (pulled from `angel_number_intents` collection)
- **CTA:** "Get your personal angel number reading" → `/birth-chart`
- JSON-LD: `FAQPage` + `Article`

---

## SEO Metadata Formulas

### Core Number Page
- **Title:** `{Number} Angel Number Meaning -- Signs, {Intent1} & {Intent2} | EverydayHoroscope`
  - Example: `111 Angel Number Meaning -- Signs, Love & Career | EverydayHoroscope`
- **Description:** `Seeing {number} everywhere? Discover the meaning of angel number {number} -- messages for love, career, twin flame, and manifestation.`

### Intent Page
- **Title:** `{Number} Angel Number {Intent} Meaning -- [2-word theme] | EverydayHoroscope`
  - Example: `111 Angel Number Love Meaning -- New Beginnings | EverydayHoroscope`
- **Description:** `Angel number {number} in {intent} means [1-line message]. Discover what {number} signals for your {intent} and what action to take.`

---

## Routes (App.js additions)

```jsx
<Route path="/angel-numbers" element={<AngelNumbersHubPage />} />
<Route path="/angel-numbers/:number" element={<AngelNumberPage />} />
<Route path="/angel-numbers/:number/:intent" element={<AngelNumberIntentPage />} />
```

All routes: public, no auth gate.

---

## Sitemap

Add to `backend/seo_router.py`:
```python
GET /api/seo/sitemap/angel-numbers   # Phase 1: 191 URLs
```

Add to `frontend/public/sitemap-index.xml`.

---

## Technical Requirements

**Follow exactly the M1/M2/M3 SEO patterns:**
- New React pages in `frontend/src/pages/seo/`
- New FastAPI router: `backend/angel_numbers_router.py` -- prefix `/api/seo`
- Register router in `backend/server.py`
- New routes in `frontend/src/App.js` (public, no auth gate)
- Sitemap endpoint added to `backend/seo_router.py`
- Cache headers in `frontend/vercel.json` (s-maxage=86400) for `/angel-numbers/*`
- MongoDB seed script: `backend/scripts/seed_angel_numbers.py`
- `SEO` component from `frontend/src/components/SEO.jsx` on every page

**Tailwind / theme:** GlassCard pattern (`rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`). Gold accent `#c5a059`. No new dependencies.

**Build verification:** `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` -- must pass clean.

---

## Content Quality Standards

- All copy is original Codex writing -- inspired by numerology and angel number traditions
- No direct reproduction from source PDFs (copyright compliance mandatory)
- Tone: warm, spiritual, grounded -- not vague or generic
- Each intent page must feel meaningfully different from the generic core page
- Affirmations: first-person, present tense, positive
- FAQ answers: 2-4 sentences each, specific to number+intent
- Action steps: concrete and immediately actionable (not vague spiritual advice)

---

## Phase 1 Number List

**Repeating triples (top traffic):**
111, 222, 333, 444, 555, 666, 777, 888, 999, 000

**Double-digit repetitions:**
11, 22, 33, 44, 55, 66, 77, 88, 99

Total: **19 numbers** -- seed all core docs + all 9 intent docs per number.

---

## Acceptance Checklist

- [ ] Hub page renders at `/angel-numbers/`
- [ ] 19 core number pages render at `/angel-numbers/{number}/`
- [ ] 171 intent pages render at `/angel-numbers/{number}/{intent}/`
- [ ] Sitemap endpoint returns 191 URLs
- [ ] Routes wired in App.js -- all pages HTTP 200
- [ ] Vercel cache headers applied to `/angel-numbers/*`
- [ ] MongoDB seed script seeds all 191 documents
- [ ] Build clean -- zero errors
- [ ] JSON-LD present on all 3 page types
- [ ] SEO meta title/description formula applied on all pages
- [ ] All 9 intents navigable from core number page
- [ ] No direct quotes from source PDFs -- all content is original Codex writing
