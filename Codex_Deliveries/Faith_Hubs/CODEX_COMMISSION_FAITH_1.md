# FAITH-1 Commission Brief -- Lumina Faith Hubs (SEO-20K M5)
> Thread: SEO Legacy Thread (same thread as SEO-20K M1/M2/M3/M4)
> Commission ID: FAITH-1 / SEO-20K M5
> Date: 2026-05-26
> Status: READY TO ISSUE

---

## Objective

Build the Lumina Faith Hubs module -- programmatic SEO pages derived from decoded scripture content. Pages cover Bhagavad Gita verses and Bible promises organised by life situation, planet/transit context, and daily guidance.

**Source material:**
```
Bhagavad Gita:
/Users/apple/Documents/Knowledge Engine_eBooks/Bible & Gita/Bhagavad-gita-As-It-Is.pdf
/Users/apple/Documents/Knowledge Engine_eBooks/Bible & Gita/The Bhagavad Gita.pdf
/Users/apple/Documents/Knowledge Engine_eBooks/Bible & Gita/Srimad_Bhagavad-Gita_Slokas_-_For_Daily_Recitation_-_Simplified_Romanized_Sanskrit.pdf

Bible:
/Users/apple/Documents/Knowledge Engine_eBooks/Bible & Gita/Bible Meanings.pdf
/Users/apple/Documents/Knowledge Engine_eBooks/Bible & Gita/the_book_of_bible_promises.pdf
/Users/apple/Documents/Knowledge Engine_eBooks/Bible & Gita/Scripture_for_Every_Moment.pdf
/Users/apple/Documents/Knowledge Engine_eBooks/Bible & Gita/Magic In The Bible.pdf
```

---

## Page Architecture -- 4 Categories

### Category 1 -- Gita Verse Pages (40 pages)

URL: `/faith/gita/{chapter}-{verse}`

The top 40 most searched and most universally applicable Bhagavad Gita verses -- decoded and explained for modern life.

Examples: 2.47 (Karma Yoga), 2.20 (soul is eternal), 4.7 (dharma protection), 9.22 (surrender), 18.66 (surrender completely), etc. Codex selects the 40 most impactful.

**Page content:**
- H1: `Bhagavad Gita [Chapter].[Verse] -- Meaning, Commentary & Life Application`
- Sanskrit verse (transliterated)
- English translation
- **Plain meaning**: What this verse says in simple terms (2-3 sentences)
- **Life application**: How to apply this teaching in modern daily life (3-4 practical points)
- **This verse for**: Which life situations this verse helps with (career, relationships, loss, fear, etc.)
- **Related verses**: 2-3 other Gita verses that complement this one (with links)
- **Affirmation**: A modern affirmation derived from this verse
- **FAQ accordion**: 4 Q&As
- JSON-LD: FAQPage + Article
- Meta title: `Bhagavad Gita [X].[Y] -- Meaning & Life Application | EverydayHoroscope`

### Category 2 -- Bible Promise Pages (40 pages)

URL: `/faith/bible/{topic-slug}`

Pages organised by life topic. Each page surfaces the strongest Bible promises/verses for that topic.

**Topics (40):**
faith, hope, healing, strength, peace, love, forgiveness, anxiety, depression, loneliness, marriage, family, money-prosperity, wisdom, protection, grief-loss, new-beginnings, purpose, patience, prayer, courage, gratitude, salvation, guidance, trust, humility, anger, addiction-recovery, parenting, work-career, friendship, identity, fear, rest, abundance, suffering, hope-in-darkness, joy, truth, perseverance

**Page content:**
- H1: `Bible Verses About [Topic] -- Scripture for [Topic] | Promises & Guidance`
- Intro: What the Bible teaches about this topic (2-3 sentences)
- **Top 5 verses**: Each with full text, reference, and 2-3 sentence plain explanation
- **How to apply**: 3 practical ways to use these scriptures in daily life
- **Prayer**: A short prayer inspired by these verses
- **Related topics**: Links to 3-4 other Faith Hub topic pages
- **FAQ accordion**: 4 Q&As
- JSON-LD: FAQPage + Article
- Meta title: `Bible Verses About [Topic] -- Scripture & Promises | EverydayHoroscope`

### Category 3 -- Astrological Faith Pages (20 pages)

URL: `/faith/transit/{transit-slug}`

Pairing spiritual guidance with planetary transits -- e.g., "Saturn Return: What the Gita Teaches", "Mercury Retrograde: Bible Verses for Confusion". These are high-search-volume intersections of astrology and spirituality.

**20 Transits/Situations:**
saturn-return, mercury-retrograde, mars-retrograde, jupiter-return, rahu-transit, ketu-transit, sade-sati, new-moon-intentions, full-moon-release, solar-eclipse, lunar-eclipse, venus-retrograde, sun-in-scorpio, saturn-in-aquarius, jupiter-in-aries, ketu-mahadasha, rahu-mahadasha, saturn-mahadasha, shani-sade-sati, mangal-dosha

**Page content:**
- H1: `[Transit/Situation]: Gita & Bible Wisdom for This Planetary Phase`
- What this transit means astrologically (2-3 sentences -- link to relevant transit page on the site)
- **Bhagavad Gita wisdom**: 2-3 relevant verses with plain meaning and application to this transit
- **Bible guidance**: 2-3 relevant Bible promises/verses for this transit's challenges
- **Spiritual practices**: 3 practices combining Vedic + Biblical wisdom for this period
- **Affirmations**: 2 -- one Gita-inspired, one Bible-inspired
- **FAQ accordion**: 4 Q&As
- CTA → Relevant transit page or Panchang
- JSON-LD: FAQPage + Article
- Meta title: `[Transit]: Gita & Bible Wisdom for This Planetary Phase | EverydayHoroscope`

### Category 4 -- Daily Scripture Pages (12 pages -- one per month theme)

URL: `/faith/monthly/{month-slug}`

Monthly scripture guides combining Gita and Bible verses aligned to the month's planetary energy.

**Months:** january, february, march, april, may, june, july, august, september, october, november, december

**Page content:**
- H1: `[Month] Scripture Guide -- Gita & Bible Verses for [Month]`
- The planetary energy of this month (1-2 sentences)
- **Gita verse of the month**: Full verse + commentary
- **Bible promise of the month**: Full verse + commentary
- **Daily practice**: A 5-minute morning ritual using these scriptures
- **Affirmation for [Month]**
- **FAQ accordion**: 3 Q&As
- JSON-LD: FAQPage + Article

---

## Total Pages

| Category | Count |
|---|---|
| Gita verse pages | 40 |
| Bible topic pages | 40 |
| Astrological faith pages | 20 |
| Monthly scripture pages | 12 |
| Hub | 1 |
| **Total** | **113** |

---

## Technical Requirements

### New files

**Backend:**
```
backend/faith_hubs_data.py       # All content data
backend/faith_hubs_router.py     # FastAPI router, prefix /api/faith
backend/scripts/seed_faith_hubs.py
```

**Frontend:**
```
frontend/src/pages/faith/FaithHubPage.jsx          # /faith (hub)
frontend/src/pages/faith/GitaVersePage.jsx          # /faith/gita/:verseSlug
frontend/src/pages/faith/BibleTopicPage.jsx         # /faith/bible/:topicSlug
frontend/src/pages/faith/FaithTransitPage.jsx       # /faith/transit/:transitSlug
frontend/src/pages/faith/FaithMonthlyPage.jsx       # /faith/monthly/:monthSlug
```

### Backend routes

```
GET /api/faith/hub                     → hub data (lists all categories)
GET /api/faith/gita/{verse_slug}       → Gita verse page data
GET /api/faith/bible/{topic_slug}      → Bible topic page data
GET /api/faith/transit/{transit_slug}  → Transit faith page data
GET /api/faith/monthly/{month_slug}    → Monthly scripture page data
```

### Sitemap

New endpoint in `seo_router.py`:
```
GET /api/seo/sitemap/faith    # 113 URLs
```

Add to `sitemap-index.xml`.

### App.js routes

```jsx
<Route path="/faith" element={<FaithHubPage />} />
<Route path="/faith/gita/:verseSlug" element={<GitaVersePage />} />
<Route path="/faith/bible/:topicSlug" element={<BibleTopicPage />} />
<Route path="/faith/transit/:transitSlug" element={<FaithTransitPage />} />
<Route path="/faith/monthly/:monthSlug" element={<FaithMonthlyPage />} />
```

### Wire in `server.py`

```python
from faith_hubs_router import router as faith_hubs_router
app.include_router(faith_hubs_router, prefix="/api/seo")
```

### Vercel cache headers

Add `/faith/*` pattern with `s-maxage=86400`.

---

## Copyright Compliance (Critical)

**Bhagavad Gita:** Traditional Sanskrit shlokas are not copyright-protected. Translations may be. Use the Romanised transliteration from the source + original plain-English paraphrase (do NOT copy publisher translations word-for-word).

**Bible:** King James Version (KJV) is public domain -- use KJV text only. All other translations (NIV, ESV, NLT) are copyright-protected. State "KJV" after every Bible reference.

**ECHO//PACE check recommended** on all generated content before deployment.

---

## Architecture Rules

1. GlassCard pattern, Gold accent, Tailwind only
2. `SEO` component + JSON-LD on every page
3. All content is original writing -- no direct copying from source PDFs
4. Bible references use KJV only
5. Internal linking: Gita verse pages should link to relevant Panchang/horoscope; transit pages link to relevant `/transits/` SEO pages

---

## Acceptance Checklist

- [ ] Hub page renders at `/faith` with category listings
- [ ] 40 Gita verse pages render with Sanskrit + translation + application + FAQ
- [ ] 40 Bible topic pages render with top 5 verses + application + prayer + FAQ
- [ ] 20 transit faith pages render with Gita + Bible wisdom + practices
- [ ] 12 monthly pages render with verse of month + practice + affirmation
- [ ] Bible text uses KJV only
- [ ] Sitemap returns 113 URLs
- [ ] Seed script runs cleanly
- [ ] Build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
