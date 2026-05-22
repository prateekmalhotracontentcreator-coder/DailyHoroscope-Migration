# FAITH-1 Commission Brief
> Thread: Faith Hubs Codex Thread  
> Module: Bible Promises + Bhagavad Gita Shloka Pages (SEO Batch 7)  
> Maps to: SEO 20K Batch 7  
> Pages: ~100 Bible promise pages + ~60 Gita shloka pages + 2 hubs = ~162 pages  
> Date: 2026-05-23  
> Status: READY TO BUILD -- source PDFs available, no dependencies

---

## Context

EverydayHoroscope (`everydayhoroscope.in`) is a live React 18 + FastAPI + MongoDB + Tailwind CSS platform. This commission adds the Faith Hubs module -- spiritual content pages drawing from two sacred sources: the Bible (promise themes) and the Bhagavad Gita (key shlokas from Chapters 1-4 in Phase 1).

These pages build the ORACLE-P3 and Community Bridge features -- spiritually-minded users seeking daily guidance from scripture. High-intent search traffic: "Bhagavad Gita on fear", "Bible verse for peace", "Gita shloka on karma" etc.

**Repo:** `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`  
**Stack:** React 18 · FastAPI · MongoDB · Tailwind CSS

**Source material:**
```
/Users/apple/Documents/Knowledge Engine_eBooks/Bible & Gita/
  the_book_of_bible_promises.pdf        -- Bible promise themes + verses (KJV)
  The Bhagavad Gita.pdf                 -- Full Bhagavad Gita with commentary
  Bhagavad-gita-As-It-Is.pdf           -- Prabhupada translation with purports
  Srimad_Bhagavad-Gita_Slokas_-_For_Daily_Recitation.pdf  -- Romanised Sanskrit
  Bible Meanings.pdf                    -- Thematic Bible reference
  Magic In The Bible.pdf               -- Additional Bible context
```

**Copyright notes:**
- **KJV Bible (King James Version):** Public domain -- verse text may be used directly
- **Bhagavad Gita original Sanskrit shlokas:** Ancient text -- public domain. Romanised transliteration: public domain.
- **Commentary text (Prabhupada, ISKCON):** Copyrighted -- DO NOT reproduce. Write original commentary.
- **Bible Promises PDF commentary:** May be copyrighted -- use only verse references, write original commentary.

All explanatory text, theme summaries, and reflections must be **original Codex writing**.

---

## Module Architecture

### URL Patterns

| URL | Purpose |
|---|---|
| `/faith/` | Faith Hub -- landing, links to Bible Promises + Gita |
| `/faith/bible/` | Bible Promises hub |
| `/faith/bible/{promise-theme}/` | Promise theme page (~100 themes) |
| `/faith/gita/` | Bhagavad Gita hub |
| `/faith/gita/{chapter}-{verse}/` | Gita shloka page (Phase 1: Ch1-4, ~60 shlokas) |

**Phase 1 scope:**
- Faith hub: 1 page
- Bible hub: 1 page + ~100 promise theme pages
- Gita hub: 1 page + ~60 shloka pages (Chapters 1-4: highest-traffic shlokas)
- **Total: ~163 pages**

---

## Bible Promises Module

### The 100 Promise Themes

Extract from `the_book_of_bible_promises.pdf` -- the book is organised by life situation. Target the 100 highest-traffic themes. Examples:

`peace`, `strength`, `hope`, `love`, `forgiveness`, `healing`, `protection`, `wisdom`, `courage`, `faith`, `joy`, `fear`, `anxiety`, `grief`, `guidance`, `patience`, `salvation`, `prayer`, `trust`, `abundance`, `purpose`, `relationships`, `marriage`, `children`, `family`, `work`, `money`, `enemies`, `sickness`, `death-grief`, `loneliness`, `depression`, `addiction`, `new-beginnings`, `gratitude`, `obedience`, `humility`, `perseverance`, `leadership`, `justice`, `truth`, `light`, `resurrection`, `eternal-life`, `redemption`, `mercy`, `grace`, `righteousness`, `holiness`, `identity-in-christ` ... (continue to 100)

### Page Content (per theme)

**File:** `frontend/src/pages/seo/FaithBiblePage.jsx`

**Page content:**
- H1: `Bible Verses About {Theme} -- God's Promise for {Situation}`
  - Example: `Bible Verses About Peace -- God's Promise for Anxious Hearts`
- **Featured verse:** 1 KJV verse (the strongest for this theme) -- large display, gold quote styling
- **Promise message:** Original Codex reflection -- 3-4 sentences on what this promise means
- **More verses:** 4-6 additional KJV verses on this theme -- each with a 1-sentence original reflection
- **How to receive this promise:** 3 action steps (prayer, meditation, journaling)
- **Related themes:** 4 pills linking to related promise pages
- **Prayer:** Original short prayer (3-5 sentences) aligned to this promise
- **FAQ accordion:** 5 questions specific to this theme
- **CTA:** "Explore daily guidance" → `/panchang` or `/birth-chart`
- JSON-LD: `FAQPage` + `Article`

**MongoDB collection: `bible_promises`** -- 100 documents:
```json
{
  "slug": "peace",
  "theme": "Peace",
  "headline": "Bible Verses About Peace -- God's Promise for Anxious Hearts",
  "featured_verse": { "reference": "John 14:27", "text": "Peace I leave with you; my peace I give you..." },
  "promise_message": "Original 3-4 sentence reflection (Codex-written)",
  "verses": [
    { "reference": "Philippians 4:7", "text": "And the peace of God, which passeth all understanding...", "reflection": "1-sentence original reflection" },
    ...
  ],
  "prayer": "Original prayer text (Codex-written)",
  "action_steps": ["...", "...", "..."],
  "related_themes": ["hope", "anxiety", "trust", "strength"],
  "faq": [...],
  "meta_title": "Bible Verses About Peace -- Promises from God's Word | EverydayHoroscope",
  "meta_description": "Discover Bible verses about peace -- God's promise for anxious hearts. Key scriptures, reflections, and a prayer to help you find peace today."
}
```

### SEO Metadata Formula (Bible)
- **Title:** `Bible Verses About {Theme} -- God's Promise for {Context} | EverydayHoroscope`
- **Description:** `Find Bible verses about {theme}. God's promises for {context} -- key scriptures, reflections, and a prayer for when you need {theme} most.`

---

## Bhagavad Gita Module

### Phase 1 Scope -- Chapters 1-4 (top-traffic shlokas)

Total shlokas in Ch1-4: Ch1 (46) + Ch2 (72) + Ch3 (43) + Ch4 (42) = 203 shlokas total.

**Select the ~60 most-searched shlokas** from Chapters 1-4. Prioritise by search intent -- the verses most commonly searched by English-speaking seekers:

**Must-include (highest traffic):**
- BG 2.47 -- "Karmanye vadhikaraste..." (duty without attachment -- most famous shloka)
- BG 2.19 -- "Ya enam vetti hantaram..." (eternal soul -- death is illusion)
- BG 2.22 -- "Vasamsi jirnani..." (soul changing bodies -- reincarnation)
- BG 2.14 -- "Matra-sparsas tu kaunteya..." (pleasure and pain are temporary)
- BG 2.27 -- Birth is certain for the dead, death for the born
- BG 4.7 -- "Yada yada hi dharmasya..." (whenever dharma declines, I appear)
- BG 4.8 -- (continuation -- to protect the good and destroy evil)
- BG 3.21 -- What a great person does, others follow
- BG 3.27 -- All actions by the modes of nature
- BG 2.23 -- Weapons cannot cut the soul
- BG 2.40 -- In this endeavour there is no loss or diminution
- BG 2.41 -- The resolute determination is focused on one goal
- BG 1.1 -- Dhritarashtra asks about Kurukshetra
- BG 2.1 -- Krishna addresses the grieving Arjuna
- ... (continue to 60 shlokas total, covering highest-traffic from all four chapters)

### Page Content (per shloka)

**File:** `frontend/src/pages/seo/FaithGitaPage.jsx`

**Page content:**
- H1: `Bhagavad Gita {Chapter}.{Verse} -- {Punchy Theme Title}`
  - Example: `Bhagavad Gita 2.47 -- Duty Without Attachment (Nishkama Karma)`
- **Sanskrit shloka:** Display in Devanagari (if supported) + Romanised transliteration (from `Srimad_Bhagavad-Gita_Slokas_-_For_Daily_Recitation.pdf`)
- **Translation:** Clean English translation -- paraphrased from public domain (not Prabhupada commentary text)
- **What Krishna is teaching:** Original Codex explanation -- 3-4 sentences
- **Core lesson:** 2-3 bullets -- practical takeaways
- **How to apply this shloka today:** 3 actionable reflections
- **Related shlokas:** 3 cards linking to related verses (same chapter or same theme)
- **Chant guidance** (for key shlokas): How to chant / meditate on this verse
- **FAQ accordion:** 5 questions specific to this shloka
- **CTA:** "Get your personal Vedic chart reading" → `/birth-chart`
- JSON-LD: `FAQPage` + `Article`

**MongoDB collection: `gita_shlokas`** -- 60 documents (Phase 1):
```json
{
  "slug": "2-47",
  "chapter": 2,
  "verse": 47,
  "url_id": "2-47",
  "theme": "Duty Without Attachment",
  "subtitle": "Nishkama Karma -- Action Without Desire for Fruits",
  "sanskrit_devanagari": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन...",
  "romanised": "karmanye vadhikaraste ma phaleshu kadachana...",
  "translation": "Clean paraphrase -- original Codex writing",
  "teaching": "3-4 sentence original explanation of what Krishna means",
  "core_lessons": ["...", "...", "..."],
  "application": ["...", "...", "..."],
  "related_shlokas": ["2-14", "3-19", "4-7"],
  "faq": [...],
  "meta_title": "Bhagavad Gita 2.47 -- Meaning, Translation & Teaching | EverydayHoroscope",
  "meta_description": "Bhagavad Gita 2.47 (karmanye vadhikaraste) teaches duty without attachment. Discover the full meaning, translation, and how to apply this teaching in daily life."
}
```

### SEO Metadata Formula (Gita)
- **Title:** `Bhagavad Gita {Chapter}.{Verse} -- Meaning, Translation & {Theme} | EverydayHoroscope`
- **Description:** `Bhagavad Gita {Chapter}.{Verse}: "{first 6 words of transliteration}..." -- {theme}. Discover the full meaning, Sanskrit text, and how to apply this teaching.`

---

## Hub Pages

### Faith Hub
**File:** `frontend/src/pages/seo/FaithHubPage.jsx`

- H1: `Faith & Scripture -- Daily Wisdom from the Bible and Bhagavad Gita`
- 2 large GlassCards: Bible Promises → `/faith/bible/` and Bhagavad Gita → `/faith/gita/`
- 1-para intro on why spiritual scripture is timeless
- Popular searches: 6 theme pills + 6 shloka pills
- JSON-LD: `BreadcrumbList`

### Bible Hub
**File:** `frontend/src/pages/seo/FaithBibleHubPage.jsx`

- H1: `Bible Promises -- Verses for Every Situation`
- 100 theme pills (filterable) -- each → promise page
- "How to use this guide" -- 3 bullets
- JSON-LD: `FAQPage`

### Gita Hub
**File:** `frontend/src/pages/seo/FaithGitaHubPage.jsx`

- H1: `Bhagavad Gita Shlokas -- Key Verses with Meaning & Teachings`
- Chapter tabs: Ch1 / Ch2 / Ch3 / Ch4 (Phase 1)
- Selected shlokas grid -- shloka reference, 1-line theme, link
- "Why read the Bhagavad Gita?" -- 3-bullet intro
- JSON-LD: `FAQPage`

---

## Backend

### Router File
`backend/faith_router.py`

Register in `backend/server.py` as: `app.include_router(faith_router, prefix="/api/seo")`

### Endpoints

```
GET /api/seo/faith/bible/themes          → list all 100 promise theme slugs
GET /api/seo/faith/bible/{slug}          → Bible promise page content
GET /api/seo/faith/gita/shlokas          → list all Phase 1 shloka slugs
GET /api/seo/faith/gita/{slug}           → Gita shloka content (slug format: "2-47")
GET /api/seo/sitemap/faith               → sitemap URLs (163 URLs)
```

### Seed Scripts
```
backend/scripts/seed_bible_promises.py   # 100 documents
backend/scripts/seed_gita_shlokas.py     # 60 documents
```

---

## Routes (App.js additions)

```jsx
<Route path="/faith" element={<FaithHubPage />} />
<Route path="/faith/bible" element={<FaithBibleHubPage />} />
<Route path="/faith/bible/:themeSlug" element={<FaithBiblePage />} />
<Route path="/faith/gita" element={<FaithGitaHubPage />} />
<Route path="/faith/gita/:shlokaSlug" element={<FaithGitaPage />} />
```

All routes: public, no auth gate.

---

## Sitemap

Add to `backend/seo_router.py`:
```python
GET /api/seo/sitemap/faith   # 163 URLs
```

Add to `frontend/public/sitemap-index.xml`.

---

## Technical Requirements

- New React pages in `frontend/src/pages/seo/` (5 new files)
- New FastAPI router: `backend/faith_router.py`
- Register in `backend/server.py`
- New routes in `frontend/src/App.js`
- Sitemap endpoint in `backend/seo_router.py`
- Cache headers in `frontend/vercel.json` (s-maxage=86400) for `/faith/*`
- MongoDB seed scripts x2
- `SEO` component on every page

**Tailwind / theme:** GlassCard pattern. Gold accent `#c5a059`. No new dependencies.

**Build:** `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` -- must pass clean.

---

## Acceptance Checklist

- [ ] Faith hub renders at `/faith/`
- [ ] Bible hub renders at `/faith/bible/` with 100 theme pills
- [ ] Sample Bible promise pages render at `/faith/bible/{slug}/`
- [ ] Gita hub renders at `/faith/gita/` with chapter tabs
- [ ] 60 Gita shloka pages render at `/faith/gita/{slug}/`
- [ ] Sitemap returns 163 URLs
- [ ] Routes wired in App.js
- [ ] Vercel cache headers applied to `/faith/*`
- [ ] Both seed scripts run without errors
- [ ] Build clean -- zero errors
- [ ] JSON-LD on all page types
- [ ] SEO meta applied on all pages
- [ ] KJV Bible verses used directly (public domain -- OK)
- [ ] Sanskrit shlokas + romanised transliteration used directly (public domain -- OK)
- [ ] NO Prabhupada/ISKCON commentary reproduced -- all explanatory text original Codex writing
- [ ] NO Bible Promises PDF commentary reproduced -- verse references only, original reflections
