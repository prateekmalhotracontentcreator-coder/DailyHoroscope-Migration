# CODEX COMMISSION -- FAITH-20K
> Commission ID: FAITH-20K
> Platform: EverydayHoroscope.in
> Module: Faith & Scripture SEO Hub
> Date Issued: 2026-05-27
> Target: 16,800 English faith pages (Phase 1-3) + 144 evergreen daily pages
> Status: OPEN -- READY FOR CODEX

---

## 0. Pre-Flight Checklist (Read Before Starting)

- [ ] All source PDFs are on the local system at paths listed in Section 2
- [ ] All verse text quoted must be accurately reproduced from source -- zero paraphrasing presented as the actual verse
- [ ] All commentary, application text, and interpretation is 100% ORIGINAL -- zero paragraph reproduction from source PDFs
- [ ] JSON-LD schema uses `Article` + `FAQPage` -- NOT `CommentaryAction` (that type does not exist at schema.org)
- [ ] Daily scripture URLs follow evergreen pattern: `/faith/daily/{sign}/{month}` -- date-stamped URLs are BANNED
- [ ] Hindi transliteration blocks are COMPONENTS of English pages -- NOT separate URLs
- [ ] Hindi pages (`/hi/faith/...`) are OUT OF SCOPE for this commission -- flagged as a separate project dependency
- [ ] Sitemap is a backend API endpoint -- NOT a static XML file written to disk
- [ ] Run `backend/tests/faith_audit.py` on each content cluster before final delivery

---

## 1. Commission Scope

### What This Commission Builds

| Phase | Category | Formula | Pages | Route Pattern |
|---|---|---|---|---|
| **1A** | Transit × Scripture | 78 transits × 2 traditions | **156** | `/faith/transit/{planet-sign}/{tradition}` |
| **1B** | Daily Scripture (Evergreen) | 12 signs × 12 months | **144** | `/faith/daily/{sign}/{month}` |
| **2** | Gita Verse × Life Situation | 700 verses × 15 situations | **10,500** | `/faith/gita/{chapter}-{verse}/{situation-slug}` |
| **3** | Bible Promise × Life Transition | 120 topics × 50 transitions | **6,000** | `/faith/bible/{topic-slug}/{transition-slug}` |
| **-- Hub pages** | Category hubs | Fixed | **8** | `/faith`, `/faith/gita`, `/faith/bible`, `/faith/transit`, `/faith/daily`, plus 3 sub-hubs |
| **-- HINDI (dependency)** | Hindi expansion | Dependent on /hi/ infrastructure | **~1,444** | `/hi/faith/...` -- OUT OF SCOPE |
| **TOTAL (English)** | | | **~16,808** | |

### What This Commission Does NOT Build
- Interactive scripture search tool (separate commission)
- User account / personalized scripture plan backend (separate commission)
- Hindi faith pages -- requires `/hi/` subdirectory infrastructure decision first
- Runtime LLM content generation -- all content is statically pre-generated in `faith_seo_data.py`

---

## 2. Source Material

All PDFs are on the local system. Content must be INSPIRED by source material, not reproduced from it.

```
Bhagavad Gita:
- /Users/apple/Documents/Knowledge Engine_eBooks/Bhagavad-gita-As-It-Is.pdf
  (A.C. Bhaktivedanta Swami Prabhupada translation -- use verse text only, not purports)
- /Users/apple/Documents/Knowledge Engine_eBooks/The Bhagavad Gita.pdf
- /Users/apple/Documents/Knowledge Engine_eBooks/Srimad_Bhagavad-Gita_Slokas_for_Daily_Recitation.pdf

Bible:
- /Users/apple/Documents/Knowledge Engine_eBooks/Bible Meanings.pdf
- /Users/apple/Documents/Knowledge Engine_eBooks/the_book_of_bible_promises.pdf
- /Users/apple/Documents/Knowledge Engine_eBooks/Scripture_for_Every_Moment.pdf
- /Users/apple/Documents/Knowledge Engine_eBooks/Magic In The Bible.pdf
```

**Copyright rule:** Verse text (public domain) may be quoted verbatim. All commentary, application text, etymology breakdowns, life-situation interpretations, and FAQ answers must be 100% original writing. The Prabhupada purports (from Bhagavad-gita As It Is) are NOT public domain -- use verse text only, not the commentary paragraphs.

---

## 3. Tech Stack Integration

### Backend
- **Framework:** FastAPI (Python)
- **Router file:** `backend/faith_seo_router.py` (new file -- do NOT modify `backend/tarot_router.py` or any existing router)
- **Data file:** `backend/faith_seo_data.py` (new file -- contains all pre-generated page content)
- **Seed script:** `backend/scripts/seed_faith_seo.py` (new file)
- **Register in:** `backend/server.py` -- add `app.include_router(faith_seo_router.router)`
- **Sitemap endpoint:** add to `backend/seo_router.py` -- `GET /api/seo/sitemap/faith`

### Frontend
- **Framework:** React 18 (CRA + Craco)
- **New pages:**
  - `frontend/src/pages/faith-seo/FaithHubPage.jsx`
  - `frontend/src/pages/faith-seo/FaithGitaHubPage.jsx`
  - `frontend/src/pages/faith-seo/FaithBibleHubPage.jsx`
  - `frontend/src/pages/faith-seo/FaithTransitHubPage.jsx`
  - `frontend/src/pages/faith-seo/FaithDailyHubPage.jsx`
  - `frontend/src/pages/faith-seo/GitaVersePage.jsx`
  - `frontend/src/pages/faith-seo/BibleTopicPage.jsx`
  - `frontend/src/pages/faith-seo/TransitScripturePage.jsx`
  - `frontend/src/pages/faith-seo/DailyScripturePage.jsx`
- **Route wiring:** `frontend/src/App.js`
- **Sitemap index:** `frontend/public/sitemap-index.xml` -- add faith sitemap reference
- **Cache headers:** `frontend/vercel.json` -- add faith routes

### Database
- **MongoDB collections:**
  - `faith_gita_pages` -- 10,500 documents
  - `faith_bible_pages` -- 6,000 documents
  - `faith_transit_pages` -- 156 documents
  - `faith_daily_pages` -- 144 documents

---

## 4. URL Architecture -- Full Specification

### 4.1 Gita Verse × Life Situation (Phase 2 -- 10,500 pages)

**Pattern:** `/faith/gita/{chapter}-{verse}/{situation-slug}`

**Dimensions:**
- Chapter-Verse: All 700 verses of the Bhagavad Gita (Chapters 1-18)
  - Format: `2-47` (chapter 2, verse 47)
- Situations (15): `career-failure`, `relationship-breakdown`, `grief-and-loss`, `anxiety`, `depression`, `identity-crisis`, `financial-pressure`, `divorce`, `health-crisis`, `new-beginning`, `betrayal`, `loneliness`, `creative-block`, `parenting-challenges`, `major-decision`

**Sample URLs:**
```
/faith/gita/2-47/career-failure
/faith/gita/2-47/grief-and-loss
/faith/gita/6-5/depression
/faith/gita/18-66/anxiety
```

**API endpoint:** `GET /api/faith/gita/{chapter}/{verse}/{situation}`

### 4.2 Bible Promise × Life Transition (Phase 3 -- 6,000 pages)

**Pattern:** `/faith/bible/{topic-slug}/{transition-slug}`

**Dimensions:**
- Topics (120): Bible thematic areas -- `anxiety`, `fear`, `provision`, `healing`, `strength`, `hope`, `forgiveness`, `wisdom`, `peace`, `purpose`, etc. (full list in Appendix A)
- Transitions (50): `divorce`, `job-loss`, `grief`, `new-city`, `illness`, `retirement`, `new-baby`, `financial-crisis`, `relationship-end`, `starting-over`, etc. (full list in Appendix A)

**Sample URLs:**
```
/faith/bible/anxiety/divorce
/faith/bible/provision/job-loss
/faith/bible/healing/illness
/faith/bible/hope/grief
```

**API endpoint:** `GET /api/faith/bible/{topic}/{transition}`

### 4.3 Transit × Scripture (Phase 1A -- 156 pages)

**Pattern:** `/faith/transit/{planet-sign}/{tradition}`
- `{planet-sign}`: matches existing transit slugs from `/transits/{planet}-in-{sign}` (78 combinations)
- `{tradition}`: `gita` | `bible`

**Sample URLs:**
```
/faith/transit/saturn-in-capricorn/gita
/faith/transit/saturn-in-capricorn/bible
/faith/transit/jupiter-in-pisces/gita
/faith/transit/mercury-retrograde/gita
```

**Internal link:** Each transit scripture page MUST link to the corresponding `/transits/{planet-sign}` page.

**API endpoint:** `GET /api/faith/transit/{planet_sign}/{tradition}`

### 4.4 Daily Scripture Evergreen (Phase 1B -- 144 pages)

**Pattern:** `/faith/daily/{sign}/{month}`
- `{sign}`: 12 zodiac signs (lowercase: `aries`, `taurus`, etc.)
- `{month}`: 12 months (lowercase: `january`, `february`, etc.)

**⚠️ BANNED PATTERNS -- DO NOT BUILD:**
```
BANNED: /faith/daily/aries/may-27-scripture-reading
BANNED: /faith/daily/aries/may-2026
BANNED: /faith/daily/2026-05-27/aries
```

**CORRECT PATTERN:**
```
CORRECT: /faith/daily/aries/may
CORRECT: /faith/daily/scorpio/november
```

**API endpoint:** `GET /api/faith/daily/{sign}/{month}`

### 4.5 Hub Pages (8 pages)

| Page | Route | Purpose |
|---|---|---|
| Main faith hub | `/faith` | All traditions overview + links |
| Gita hub | `/faith/gita` | All 18 chapters + situation index |
| Bible hub | `/faith/bible` | Topic index + transition index |
| Transit scripture hub | `/faith/transit` | All 78 transit pairs |
| Daily scripture hub | `/faith/daily` | All 12 signs × monthly guide |
| Sign-specific daily | `/faith/daily/{sign}` | 12 pages, one per sign |
| Chapter hub | `/faith/gita/chapter-{n}` | 18 pages, one per chapter |

---

## 5. Content Structure -- Per Page Type

### 5.1 Gita Verse × Life Situation

Minimum word count: **550 words original content** (verse text does not count toward minimum)

```
H1: Bhagavad Gita {Chapter}:{Verse} for {Situation Label}
    (Example: "Bhagavad Gita 2:47 for Career Failure")

[Situation Hook -- 80-100 words]
Opens entirely in the vocabulary of the life situation.
No scripture reference in this block.
Addresses the emotional state with specificity.

[Verse Presentation]
Sanskrit shloka (IAST diacritics)
Transliteration (italicised)
English translation -- credited to source

[Etymology Block -- 100-120 words] ← ANCHOR 2
2-3 key Sanskrit words: term + root + literal meaning + situational application.

[Modern Application -- 100-120 words]
Specific, actionable guidance. What to do differently TODAY.
No generic spiritual encouragement.

[Astrological Transit Layer -- 80-100 words] ← ANCHOR 3
Planetary relevance. Links to /transits/{slug}.
Dasha-period application.

[FAQ Section -- 3 questions × ~50 words each]
Long-tail search vocabulary natural to someone in this situation.

[Internal Links]
- Link to: /faith/transit/{relevant-transit}/gita
- Link to: /faith/daily/{sign-closest-to-situation}/current-month
- Link to: /transits/{relevant-planet-slug}
- Link to: /panchang/{city}/{date} (nearest upcoming auspicious window)
```

### 5.2 Bible Promise × Life Transition

Minimum word count: **530 words original content**

```
H1: Bible Promises for {Transition Label} -- Scripture & Guidance
    (Example: "Bible Promises for Divorce -- Scripture & Guidance")

[Emotional Frame -- 80-100 words]
Opens in the emotional vocabulary of the transition.
No Bible reference in this block.

[Verse Presentation]
Verse text -- Book Chapter:Verse (Translation)

[Hermeneutical Unpacking -- 100-120 words] ← ANCHOR 2
What the verse promises. What it does NOT promise.
Original language note (1 term where relevant).
Original context -- who it was written for and why that matters HERE.

[Practical Application -- 100-120 words]
Specific practice. Specific prayer structure. Specific decision the verse informs.

[Vedic Resonance Bridge -- 80-100 words] ← ANCHOR 3
How Vedic tradition views the same theme.
Cross-link to corresponding Gita verse page.

[FAQ Section -- 3 questions × ~50 words each]

[Internal Links]
- Link to: parallel Gita verse page
- Link to: /faith/transit/{relevant-transit}/bible
- Link to: /traits/{sign}/{relevant-chart-point}/{house}
```

### 5.3 Transit × Scripture

Minimum word count: **500 words original content**

```
H1: {Planet} in {Sign} -- Gita & Bible Guidance for This Transit
    (Example: "Saturn in Capricorn -- Gita & Bible Guidance for This Transit")

[Transit Energy -- 100 words]
Planetary archetype for this transit. Internal link to /transits/{slug}.

[Scripture Block 1 -- 150 words]
Tradition-specific (Gita or Bible).
2 verses with application to this transit's energy.

[Scripture Block 2 -- 150 words]
Second verse + deeper application.

[Practice During This Transit -- 150 words]
Specific daily spiritual practice. Panchang timing reference.

[Internal Links]
- /transits/{planet-sign}
- /panchang/{city}/{date}
- Related traits page if applicable
```

### 5.4 Daily Scripture -- Evergreen

Minimum word count: **450 words original content**

```
H1: {Sign} Spiritual Guide -- {Month}
    (Example: "Aries Spiritual Guide -- May")

[Sign + Month Energy -- 100 words]
Sign archetype × seasonal energy × ruling planet interaction.
NOT a horoscope prediction. A spiritual lens.

[Gita Verse for This Month -- 150 words]
1 verse best suited to what this sign needs in this month.
Full application specific to sign-month.

[Bible Promise for This Month -- 150 words]
1 verse. Full application specific to sign-month.

[Daily Practice -- 100 words]
5 bulleted concrete practices. Actionable, sign-specific.

[Premium CTA]
"Receive a personalized 21-day scripture plan matched to your Vedic birth chart."
Link to premium product page.
```

---

## 6. E.C.H.O. // P.A.C.E. Compliance Rules

> Reference: `ECHO_PACE_PROCESS/PROCESS_5_CONTENT_ANCHOR_FRAMEWORK.md`

### 6.1 Custom Stop-Word List for Faith Module TF-IDF

Before running the compliance check, these terms MUST be added to the stop-word filter to prevent false positives:

```python
FAITH_STOP_WORDS = [
    "chapter", "verse", "shloka", "slokas", "gita", "bhagavad",
    "bible", "scripture", "testament", "lord", "god", "krishna",
    "arjuna", "christ", "jesus", "holy", "faith", "unto", "shall",
    "thee", "thou", "recitation", "meaning", "translation", "prayer",
    "spiritual", "teaching", "wisdom", "divine"
]
```

### 6.2 Compliance Rules Per Category

**Gita Verse × Situation (hardest compliance category):**
- Test group: all 15 pages for the SAME verse (e.g., all 15 pages for Gita 2:47)
- Ceiling: ≤30% worst-pair similarity (YMYL content -- stricter than standard 40%)
- Primary differentiator: Section 1 (Hook) -- must open with entirely different situation vocabulary
- Secondary differentiator: Section 5 (Transit Layer) -- different planetary slugs = different vocabulary
- FORBIDDEN: same sentence structure in Section 1 across any two pages in the same verse-cluster
- Example of FAIL: page 1 opens "When the weight of career failure settles..." and page 2 opens "When the weight of grief settles..." -- same structure, TF-IDF detects it

**Bible Promise × Transition (medium compliance risk):**
- Test group: all 50 pages for the same TOPIC (e.g., all 50 "anxiety" topic pages)
- Ceiling: ≤35% worst-pair similarity
- Primary differentiator: Section 1 (Emotional Frame) -- transition-specific vocabulary
- Secondary differentiator: Section 5 (Vedic Bridge) -- different Gita cross-links = different vocabulary

**Transit × Scripture (lowest compliance risk):**
- 156 pages, tested as one cluster by tradition (78 Gita + 78 Bible)
- Ceiling: ≤40% worst-pair similarity
- Natural differentiator: planetary vocabulary (each planet has distinct archetype vocabulary)

**Daily Scripture (low compliance risk):**
- 144 pages, tested as one cluster
- Ceiling: ≤40% worst-pair similarity
- Natural differentiator: sign-specific vocabulary + seasonal vocabulary

### 6.3 The Fixed Content Trap -- Gita Module Equivalent of The Tower Card Problem

In the Tarot module, The Tower card appearing in 60 different spreads was the hardest compliance challenge. In the Faith module, the equivalent is: **Gita 2:47 appearing in 15 different life situation pages**.

The verse text is fixed. The Sanskrit is fixed. The translation is fixed.

**The solution (Linguistic Isolation Framing):**
The page opens INSIDE the life situation's emotional experience -- before the verse is mentioned. The first 80-100 words must be entirely in the situation's vocabulary. By the time the verse is introduced, the page's highest-weight TF-IDF vocabulary cluster is already situation-specific.

Two pages sharing the same verse but different situations will have low similarity because their highest-weight vocabulary clusters are completely different.

### 6.4 Compliance Script

Save as `backend/tests/faith_audit.py`:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import text
import numpy as np

def run_faith_compliance_check(
    page_content_list: list[str],
    ceiling: float = 30.0,
    cluster_name: str = "unnamed"
) -> bool:
    """
    Run E.C.H.O. // P.A.C.E. TF-IDF compliance check on a faith page cluster.

    Args:
        page_content_list: List of full page text content strings
        ceiling: Maximum allowed worst-pair similarity percentage
        cluster_name: Identifier for logging (e.g., "gita-2-47", "bible-anxiety")

    Returns:
        True if cluster passes (worst pair <= ceiling), False if fails
    """
    FAITH_STOP_WORDS = [
        "chapter", "verse", "shloka", "slokas", "gita", "bhagavad",
        "bible", "scripture", "testament", "lord", "god", "krishna",
        "arjuna", "christ", "jesus", "holy", "faith", "unto", "shall",
        "thee", "thou", "recitation", "meaning", "translation", "prayer",
        "spiritual", "teaching", "wisdom", "divine"
    ]
    custom_stops = list(text.ENGLISH_STOP_WORDS.union(FAITH_STOP_WORDS))

    vectorizer = TfidfVectorizer(stop_words=custom_stops, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(page_content_list)
    similarity_matrix = cosine_similarity(tfidf_matrix)
    np.fill_diagonal(similarity_matrix, 0)

    worst_pair_score = float(np.max(similarity_matrix)) * 100
    avg_score = float(np.mean(similarity_matrix[similarity_matrix > 0])) * 100

    status = "PASS ✅" if worst_pair_score <= ceiling else "FAIL ❌"
    print(f"[E.C.H.O. Audit] Cluster: {cluster_name}")
    print(f"  Pages tested: {len(page_content_list)}")
    print(f"  Worst-pair: {worst_pair_score:.2f}% (ceiling: {ceiling}%)")
    print(f"  Average: {avg_score:.2f}%")
    print(f"  Result: {status}")

    return worst_pair_score <= ceiling


def audit_gita_cluster(verse_data: list[dict]) -> bool:
    """Test all situation pages for a single Gita verse."""
    contents = [
        f"{p['hook']} {p['etymology']} {p['application']} {p['transit_layer']}"
        for p in verse_data
    ]
    cluster_name = f"gita-{verse_data[0]['chapter']}-{verse_data[0]['verse']}"
    return run_faith_compliance_check(contents, ceiling=30.0, cluster_name=cluster_name)


def audit_bible_topic_cluster(topic_data: list[dict]) -> bool:
    """Test all transition pages for a single Bible topic."""
    contents = [
        f"{p['emotional_frame']} {p['hermeneutical']} {p['application']} {p['vedic_bridge']}"
        for p in topic_data
    ]
    cluster_name = f"bible-{topic_data[0]['topic_slug']}"
    return run_faith_compliance_check(contents, ceiling=35.0, cluster_name=cluster_name)
```

---

## 7. JSON-LD Structured Data

> Reference: `ECHO_PACE_PROCESS/PROCESS_6_SCHEMA_ORG_TYPES_BY_MODULE.md`

### ⚠️ CRITICAL -- Schema Type Correction

`CommentaryAction` is **NOT a valid schema.org type**. It does not exist at schema.org. Do NOT use it. This was proposed by an external tool and is incorrect.

**Use these validated types only:**

**Gita Verse Pages:** `Article` (with `about: {Book}`) + `FAQPage`
**Bible Pages:** `Article` (with `about: {Book}`) + `FAQPage`
**Transit Pages:** `Article`
**Daily Scripture Pages:** `Article`
**Hub Pages:** `WebPage` or `CollectionPage`

### Gita Page Schema (Codex Implementation Template)

```jsx
// In GitaVersePage.jsx -- inside <Helmet> or SEO component
const schema = [
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": `Bhagavad Gita ${chapter}:${verse} for ${situationLabel}`,
    "about": {
      "@type": "Book",
      "name": "Bhagavad Gita",
      "author": { "@type": "Person", "name": "Vyasa" }
    },
    "author": {
      "@type": "Organization",
      "name": "EverydayHoroscope",
      "url": "https://www.everydayhoroscope.in"
    },
    "publisher": {
      "@type": "Organization",
      "name": "EverydayHoroscope",
      "url": "https://www.everydayhoroscope.in"
    },
    "inLanguage": "en",
    "url": `https://www.everydayhoroscope.in/faith/gita/${chapter}-${verse}/${situationSlug}`
  },
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": page.faq.map(item => ({
      "@type": "Question",
      "name": item.q,
      "acceptedAnswer": { "@type": "Answer", "text": item.a }
    }))
  }
];
```

### Bible Page Schema

```jsx
const schema = [
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": `Bible Promises for ${transitionLabel} -- Scripture & Guidance`,
    "about": { "@type": "Book", "name": "The Bible" },
    "author": { "@type": "Organization", "name": "EverydayHoroscope", "url": "https://www.everydayhoroscope.in" },
    "inLanguage": "en"
  },
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": page.faq.map(item => ({
      "@type": "Question",
      "name": item.q,
      "acceptedAnswer": { "@type": "Answer", "text": item.a }
    }))
  }
];
```

---

## 8. Internal Linking Architecture

### From Faith Pages → Existing Platform Pages

Every faith page MUST include at least 2 internal links to existing platform content:

| Faith Page Type | Required Internal Links |
|---|---|
| Gita Verse × Situation | `/transits/{relevant-planet-slug}` (planet governs the situation) |
| Gita Verse × Situation | `/panchang/{city}/{date}` (generic -- "find your auspicious practice window") |
| Bible × Transition | Parallel Gita verse page (cross-tradition bridge) |
| Bible × Transition | `/traits/{sign}/{relevant-point}/{house}` where applicable |
| Transit × Scripture | `/transits/{planet-sign}` (REQUIRED -- existing transit page) |
| Transit × Scripture | `/panchang/{city}/{date}` |
| Daily Scripture | `/traits/{sign}/{sun}/{house}` for the sign |
| Daily Scripture | `/panchang/{city}/{date}` |

### Planet → Situation Mapping (for transit links)

| Life Situation | Primary Planet | Transit Slug Example |
|---|---|---|
| Career failure, structure, delay | Saturn | `saturn-in-capricorn` |
| Grief, loss, endings | Saturn, Ketu | `saturn-in-scorpio` |
| Anxiety, mental pressure | Mercury, Rahu | `mercury-retrograde` |
| Relationship breakdown | Venus | `venus-in-scorpio` |
| Financial pressure | Venus, Jupiter | `jupiter-in-pisces` |
| Identity crisis | Sun, Rahu | `sun-in-aquarius` |
| New beginning | Jupiter | `jupiter-in-aries` |
| Health crisis | Mars, Saturn | `mars-in-virgo` |

### Faith Hub → Faith Detail Pages (Internal Cluster Linking)

- `/faith/gita` hub → links to all 18 chapter sub-hubs
- Chapter sub-hub → links to all verses in that chapter × top 5 situations
- `/faith/bible` hub → links to all 120 topic category pages
- Topic category page → links to its top 10 most-searched transitions
- `/faith/transit` hub → links to all 78 transit pairs

---

## 9. Sitemap Architecture

### ⚠️ Architecture Rule -- Backend API Endpoint, NOT Static File

Do NOT write XML to disk in `frontend/public/sitemaps/`. That approach does not work with our Render + Vercel split architecture.

**Correct implementation:**

**Step 1 -- Add to `backend/seo_router.py`:**

```python
@router.get("/sitemap/faith")
async def faith_sitemap(db=Depends(get_db)):
    """Serves faith module sitemap -- all ~16,800+ faith URLs."""
    base = "https://www.everydayhoroscope.in"
    urls = []

    # Hub pages
    hubs = ["/faith", "/faith/gita", "/faith/bible", "/faith/transit", "/faith/daily"]
    for hub in hubs:
        urls.append(f"""
  <url>
    <loc>{base}{hub}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>""")

    # Gita verse pages
    gita_pages = await db["faith_gita_pages"].find({}, {"route": 1}).to_list(None)
    for p in gita_pages:
        urls.append(f"""
  <url>
    <loc>{base}{p['route']}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>""")

    # Bible pages
    bible_pages = await db["faith_bible_pages"].find({}, {"route": 1}).to_list(None)
    for p in bible_pages:
        urls.append(f"""
  <url>
    <loc>{base}{p['route']}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>""")

    # Transit pages
    transit_pages = await db["faith_transit_pages"].find({}, {"route": 1}).to_list(None)
    for p in transit_pages:
        urls.append(f"""
  <url>
    <loc>{base}{p['route']}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")

    # Daily pages
    daily_pages = await db["faith_daily_pages"].find({}, {"route": 1}).to_list(None)
    for p in daily_pages:
        urls.append(f"""
  <url>
    <loc>{base}{p['route']}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>""")

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{"".join(urls)}
</urlset>"""

    return Response(content=sitemap_content, media_type="application/xml")
```

**Step 2 -- Add to `frontend/public/sitemap-index.xml`:**

```xml
<sitemap>
  <loc>https://everydayhoroscope-api.onrender.com/api/seo/sitemap/faith</loc>
  <lastmod>2026-05-27</lastmod>
</sitemap>
```

---

## 10. API Endpoints to Build

```
GET /api/faith/gita/{chapter}/{verse}/{situation}
    → Returns: full page content object from faith_gita_pages collection

GET /api/faith/gita/chapter/{chapter}
    → Returns: list of all verses in chapter with top 5 situations

GET /api/faith/bible/{topic}/{transition}
    → Returns: full page content object from faith_bible_pages collection

GET /api/faith/transit/{planet_sign}/{tradition}
    → Returns: full page content object from faith_transit_pages collection

GET /api/faith/daily/{sign}/{month}
    → Returns: full page content object from faith_daily_pages collection

GET /api/faith/hub
    → Returns: hub overview data (featured verses, popular topics, sign guides)

GET /api/seo/sitemap/faith
    → Returns: XML sitemap of all faith URLs
```

---

## 11. Frontend Page Specifications

### 11.1 GitaVersePage.jsx
```
Route: /faith/gita/:chapter-:verse/:situationSlug
API call: GET /api/faith/gita/{chapter}/{verse}/{situationSlug}

Render:
- H1: page.meta_title (descriptive, not the verse reference alone)
- Sanskrit shloka block (styled with Devanagari font support)
- Transliteration block (italic)
- Translation (credited)
- Section blocks in order: hook → etymology → application → transit_layer
- Astrological link card: "Saturn is currently transiting Capricorn → [read guidance]"
- FAQ accordion (structured data compatible)
- Internal link cards to transit page + panchang
- JSON-LD in Helmet
- SEO component with meta_title + meta_description
```

### 11.2 BibleTopicPage.jsx
```
Route: /faith/bible/:topicSlug/:transitionSlug
API call: GET /api/faith/bible/{topicSlug}/{transitionSlug}

Render:
- H1: descriptive title
- Verse block (styled, credited)
- Section blocks: emotional_frame → hermeneutical → application → vedic_bridge
- Cross-tradition link card: "Bhagavad Gita also speaks to this → [link]"
- FAQ accordion
- JSON-LD in Helmet
```

### 11.3 TransitScripturePage.jsx
```
Route: /faith/transit/:planetSign/:tradition
API call: GET /api/faith/transit/{planetSign}/{tradition}

Render:
- H1: {Planet} in {Sign} -- {Tradition} Guidance
- Transit summary card with link to /transits/{slug}
- Scripture blocks (2 verses)
- Practice section
- Panchang reference card
```

### 11.4 DailyScripturePage.jsx
```
Route: /faith/daily/:sign/:month
API call: GET /api/faith/daily/{sign}/{month}

Render:
- H1: {Sign} Spiritual Guide -- {Month}
- Sign + month energy intro
- Gita verse block
- Bible promise block
- Daily practice list (bulleted)
- Premium upsell card: "Get your personalized 21-day scripture plan"
```

---

## 12. Theme and Style

Use the EverydayHoroscope standard theme tokens:

```css
/* GlassCard container for verse blocks */
.verse-card {
  border-radius: 0.75rem;
  border: 1px solid rgba(197, 160, 89, 0.2);   /* border-gold/20 */
  background: rgba(197, 160, 89, 0.04);          /* bg-gold/[0.04] */
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

/* Sanskrit / scripture text */
.scripture-text {
  font-style: italic;
  color: var(--text-foreground);
  font-size: 1.05rem;
  line-height: 1.7;
}

/* Gold accent for verse reference */
.verse-reference {
  color: var(--text-gold);    /* #c5a059 */
  font-weight: 600;
  font-size: 0.9rem;
}
```

Colors:
- Gold: `#c5a059` (`text-gold`)
- Backgrounds: `bg-background`, `bg-card`
- Text: `text-foreground`, `text-muted-foreground`

---

## 13. Build Sequence -- Phase Priorities

Build in this order for fastest indexing return:

### Phase 1A -- Transit × Scripture (156 pages) -- BUILD FIRST
**Why:** These 156 pages connect to our 78 existing live transit pages. They will index fast because the transit pages already have authority. They create immediate internal link value.
**Delivery:** `faith_transit_pages` collection + `TransitScripturePage.jsx` + API route

### Phase 1B -- Daily Scripture Evergreen (144 pages) -- BUILD SECOND
**Why:** 144 evergreen pages with monthly sign energy. High return-visit potential. Upsell to premium scripture plan. Low content complexity.
**Delivery:** `faith_daily_pages` collection + `DailyScripturePage.jsx` + API route

### Phase 2 -- Gita Verse × Situation (10,500 pages) -- MAIN PHASE
**Why:** Largest volume, highest long-term traffic. Build Chapter 2 first (most searched). Then Chapter 6, Chapter 18, Chapter 12. Then remaining chapters.
**Priority chapter order:** Ch2 → Ch6 → Ch18 → Ch12 → Ch3 → Ch4 → Ch5 → Ch7-17 → Ch1
**ECHO/PACE check:** Run compliance audit on each chapter cluster before seeding

### Phase 3 -- Bible Promise × Transition (6,000 pages) -- AFTER GITA BASE
**Why:** Builds on the platform authority established by Gita pages. Cross-tradition internal links strengthen both clusters.
**Priority topic order:** anxiety → grief-and-loss → provision → fear → healing → strength → hope (by search volume)

---

## 14. Acceptance Checklist

- [ ] All 156 transit × scripture pages render at `/faith/transit/{planet-sign}/{tradition}`
- [ ] All 144 daily pages render at `/faith/daily/{sign}/{month}` -- NO date-stamped URLs
- [ ] All Gita verse pages render at `/faith/gita/{chapter}-{verse}/{situation}`
- [ ] All Bible pages render at `/faith/bible/{topic}/{transition}`
- [ ] Hub pages render: `/faith`, `/faith/gita`, `/faith/bible`, `/faith/transit`, `/faith/daily`
- [ ] Each faith page contains: H1, verse block, minimum 3 content sections, FAQ, internal links
- [ ] JSON-LD schema present on all pages -- using `Article` + `FAQPage` only (NOT `CommentaryAction`)
- [ ] No date-stamped URLs anywhere in the sitemap
- [ ] Hindi pages are NOT built -- transliteration is a text component within English pages only
- [ ] `GET /api/seo/sitemap/faith` returns valid XML with all faith URLs
- [ ] Sitemap reference added to `frontend/public/sitemap-index.xml`
- [ ] E.C.H.O. compliance audit passes for all Gita verse clusters (worst-pair ≤30%)
- [ ] E.C.H.O. compliance audit passes for all Bible topic clusters (worst-pair ≤35%)
- [ ] Frontend build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
- [ ] No smart/curly quotes in JSX files (run Unicode replacement check)
- [ ] No modifications to existing routers: `tarot_router.py`, `panchang_router.py`, `server.py` (only include_router addition)

---

## 15. Process Document References

This commission was built using these platform process standards. Codex engineers must read these before building:

| Document | Location | Purpose |
|---|---|---|
| Content Anchor Framework | `ECHO_PACE_PROCESS/PROCESS_5_CONTENT_ANCHOR_FRAMEWORK.md` | 3-anchor rule, linguistic isolation, stop-word registers |
| Schema.org Types by Module | `ECHO_PACE_PROCESS/PROCESS_6_SCHEMA_ORG_TYPES_BY_MODULE.md` | Correct JSON-LD types -- CommentaryAction correction |
| YMYL Content Quality | `ECHO_PACE_PROCESS/PROCESS_7_YMYL_CONTENT_QUALITY.md` | E-E-A-T standards, minimum content requirements, fatal mistake |
| Faith Content Template | `Faith_Hubs/FAITH_CONTENT_GENERATION_TEMPLATE.md` | Page-by-page content generation prompts and data object schemas |
| CI/CD Compliance Testing | `ECHO_PACE_PROCESS/PROCESS_2_CICD_COMPLIANCE_TESTING.md` | How to run TF-IDF audit in pipeline |
| Sitemap Architecture | `ECHO_PACE_PROCESS/PROCESS_3_SITEMAP_ARCHITECTURE.md` | Backend endpoint approach |

---

## Appendix A -- Full Dimension Lists

### Gita Life Situations (15)
1. `career-failure` -- Career Failure & Job Loss
2. `relationship-breakdown` -- Relationship Breakdown
3. `grief-and-loss` -- Grief and Loss
4. `anxiety` -- Anxiety & Overwhelm
5. `depression` -- Depression & Low Energy
6. `identity-crisis` -- Identity Crisis & Confusion
7. `financial-pressure` -- Financial Pressure & Debt
8. `divorce` -- Divorce & Separation
9. `health-crisis` -- Health Crisis & Recovery
10. `new-beginning` -- New Beginning & Fresh Start
11. `betrayal` -- Betrayal & Trust Issues
12. `loneliness` -- Loneliness & Isolation
13. `creative-block` -- Creative Block & Stagnation
14. `parenting-challenges` -- Parenting Challenges
15. `major-decision` -- Major Decision & Crossroads

### Bible Topics (120) -- Sample First 30
`anxiety`, `fear`, `provision`, `healing`, `strength`, `hope`, `forgiveness`,
`wisdom`, `peace`, `purpose`, `identity`, `patience`, `courage`, `joy`,
`guidance`, `protection`, `rest`, `restoration`, `redemption`, `grace`,
`faith`, `trust`, `gratitude`, `comfort`, `renewal`, `breakthrough`,
`deliverance`, `prosperity`, `relationships`, `family`
*(Full 120-item list to be generated by Codex from the source Bible PDFs)*

### Bible Life Transitions (50) -- Sample First 25
`divorce`, `job-loss`, `grief`, `new-city`, `illness`, `retirement`,
`new-baby`, `financial-crisis`, `relationship-end`, `starting-over`,
`addiction-recovery`, `empty-nest`, `career-change`, `marriage`,
`pregnancy-loss`, `aging-parent`, `graduation`, `immigration`,
`business-failure`, `natural-disaster`, `chronic-illness`, `mental-health-crisis`,
`estrangement`, `betrayal-by-friend`, `major-surgery`
*(Full 50-item list to be generated by Codex from the source Bible PDFs)*
