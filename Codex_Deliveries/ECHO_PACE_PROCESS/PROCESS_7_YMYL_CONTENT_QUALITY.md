# Process Doc 7 -- YMYL Content Quality Standards (E-E-A-T)
> EverydayHoroscope.in -- SEO Content Quality Reference
> Document Type: Platform-Wide Process Reference
> Version: 1.0
> Date: 2026-05-27
> Scope: Faith, Health, and all YMYL-adjacent modules

---

## 1. What Is YMYL?

**Your Money Your Life (YMYL)** -- Google's Search Quality Rater Guidelines classify content as YMYL when it has the potential to significantly impact a person's health, finances, safety, wellbeing, or major life decisions.

**EverydayHoroscope.in modules that are YMYL or YMYL-adjacent:**

| Module | YMYL Classification | Reason |
|---|---|---|
| Faith / Scripture Hub | **YMYL** | Religious and spiritual guidance can significantly impact life decisions, mental health, and daily behavior |
| Health-related horoscopes | **YMYL** | Health guidance |
| Longevity / Medical Astrology | **YMYL** | Direct health implication |
| Financial transit pages | **YMYL-adjacent** | Financial decision implications |
| Panchang / Muhurta | **YMYL-adjacent** | Timing of major life events (weddings, business starts) |
| Angel Numbers | **YMYL-adjacent** | Life guidance and decision-making influence |
| Crystal Healing | **YMYL-adjacent** | Health and wellbeing implications |

---

## 2. The E-E-A-T Framework

**Experience -- Expertise -- Authoritativeness -- Trustworthiness**

Google's quality raters evaluate YMYL content against all four dimensions. A programmatic site must compensate for the absence of a named individual expert through **structural E-E-A-T** -- building authority signals into the page architecture itself.

### 2.1 Experience
The content must demonstrate that the author has genuine familiarity with both the source tradition AND the modern life situation being addressed.

**Failure mode:** "Bhagavad Gita 2:47 teaches us about duties" -- generic theological summary that anyone could copy from a book.

**Pass:** "The first time you read *nishkama karma* in the context of a layoff, the natural reaction is resistance -- because western culture has trained us to define identity through output. The verse is not dismissing the grief of losing a job. It is distinguishing between the effort-self and the outcome-self." -- demonstrates engagement with both the text and the lived experience.

**Requirement:** Every faith page must contain at least ONE paragraph that demonstrates genuine engagement with the emotional or situational reality the reader is in -- not just the theological text.

### 2.2 Expertise
The content must reflect knowledge of the source tradition at more than surface level.

**Minimum signals for faith pages:**
- Sanskrit transliteration of the shloka with phonetic guide
- Word-by-word etymological breakdown of at least 2 key Sanskrit terms
- Reference to the original context of the verse (which chapter, what battle moment, what Arjuna's situation was)
- For Bible pages: recognition of the original language context (Hebrew/Greek) where relevant

**Failure mode:** Just printing the English translation and writing a paragraph of generic advice.

### 2.3 Authoritativeness
The page must position EverydayHoroscope as a trustworthy source within the Indian spiritual + astrological ecosystem.

**Structural authority signals:**
- Author byline or platform attribution in the article schema
- Internal linking to related authoritative pages (transit pages, panchang pages, traits pages)
- Citing the specific translation source (A.C. Bhaktivedanta Swami, etc.)
- Cross-linking between Gita and Bible pages where they share thematic resonance

**Note:** We do NOT need a named individual author for every page -- an organization entity in schema is acceptable for programmatic content at this scale.

### 2.4 Trustworthiness
The reader must be able to verify what we say and trust the intent behind it.

**Non-negotiable trust elements:**
- Verse text must be accurately quoted -- no paraphrasing presented as the actual verse
- Translation source must be acknowledged (public domain translations are permissible)
- We must not make absolute predictions about life outcomes ("this verse guarantees your job will return")
- Tone must be supportive and advisory, not commanding or fear-based

---

## 3. Minimum Content Requirements Per Faith Page Type

### 3.1 Gita Verse × Life Situation Page (10,500 pages)
Minimum 450 words original content structured as:

| Section | Word Count | Content Requirement |
|---|---|---|
| Situation Hook | 80-100 words | Opens entirely in modern situation vocabulary. No verse reference. Addresses the emotional state. |
| Verse Presentation | 50-70 words | Full Sanskrit shloka + transliteration + English translation. Source credited. |
| Etymology Block (Anchor 2) | 100-120 words | Word-by-word breakdown of 2-3 key Sanskrit terms. Connects root meaning to modern situation. |
| Modern Application | 100-120 words | How the teaching practically applies to the specific situation. Not generic -- situation-specific. |
| Astrological Layer (Anchor 3) | 80-100 words | Which planetary energies or transit periods make this teaching most relevant. Links to transit pages. |
| FAQ Section | 150-200 words | 3-4 questions in long-tail search vocabulary. Answers must be original, not repeated from above. |
| **Total** | **560-710 words** | All original. Verse text (public domain) quoted accurately. Zero paragraph reproduction from PDFs. |

### 3.2 Bible Promise × Life Transition Page (6,000 pages)
Minimum 450 words original content structured as:

| Section | Word Count | Content Requirement |
|---|---|---|
| Emotional Frame | 80-100 words | Opens in the emotional vocabulary of the transition. No verse reference. |
| Verse Presentation | 30-50 words | Verse text. KJV or NIV (widely cited, public domain or fair use). Book, chapter, verse cited. |
| Hermeneutical Unpacking (Anchor 2) | 100-120 words | What the verse means in its original context. Original language note where relevant. What the promise specifically covers. |
| Practical Application | 100-120 words | What the reader can do today with this promise. Specific, actionable, not generic. |
| Vedic Resonance Layer (Anchor 3) | 80-100 words | How Vedic astrology / Indian spiritual tradition views the same theme. Cross-tradition bridge for our audience. |
| FAQ Section | 150-200 words | 3-4 questions in long-tail search vocabulary. |
| **Total** | **540-690 words** | |

### 3.3 Transit × Scripture Page (156 pages)
Minimum 500 words:

| Section | Content |
|---|---|
| Transit Overview | What this planetary transit means astrologically (link to existing transit page) |
| Gita Teaching | 1-2 relevant verses with application to the transit's energy |
| Bible Promise | 1-2 relevant verses with application to the transit's energy |
| What To Do During This Transit | Practical guidance: spiritual practice, timing, mindset |
| Panchang Integration | Link to panchang for auspicious windows during this transit |

### 3.4 Daily Scripture Page -- Evergreen (144 pages)
Minimum 400 words. Format: monthly spiritual guide for a zodiac sign.

| Section | Content |
|---|---|
| Sign + Month Energy | What this zodiac-month combination energetically calls for |
| Gita Verse for This Month | 1 verse + application specific to this sign's tendencies in this month |
| Bible Promise for This Month | 1 verse + application |
| Daily Practice Suggestions | 3-5 concrete daily practice suggestions |
| Upsell Block | "Get your personalized 21-day scripture plan" (premium product link) |

---

## 4. The One Fatal Mistake -- Direct Scraped Commentary

**The most common programmatic faith site failure:** appending raw scraped commentary from published works (Prabhupada's Bhaktivedanta purports, Matthew Henry's Bible commentary, etc.).

**Why it fails:**
1. Those commentaries are fully indexed by publishers, universities, and major religious sites
2. TF-IDF will immediately flag high similarity to existing indexed content
3. It is a copyright violation if not public domain
4. It adds zero unique value -- Google's Helpful Content system specifically targets "content that adds nothing beyond what's already indexed"

**The Direct Practical Remedy Shield Rule (from GAI brief):**
Every faith page must answer the question: *"What can this person do differently TODAY because they read this page?"*

This question must be answerable with a specific action -- not a general encouragement. If the answer is "pray more" or "trust God" without specifics, the page has failed the YMYL quality standard.

**Correct:** "If you are in a period of job loss and reading Gita 2:47, the specific practice is: for the next 7 days, complete your daily job-application tasks with a timer-based focus session, then close the browser. The action is yours. The outcome is not. This is not passivity -- it is precision."

**Incorrect:** "Bhagavad Gita 2:47 teaches us to perform our duties without attachment to results, which is a valuable lesson for anyone going through difficult times."

---

## 5. Hindi Pages -- Separate Architecture

Hindi content expansion (`/hi/faith/...`) is a **separate project dependency** -- it requires a full Hindi subdirectory infrastructure decision before Faith Hindi pages can be built.

**Do NOT build Hindi URL slugs within the English faith module.** Hindi transliteration blocks (the phonetic guide for Sanskrit shlokas) are components of the English page -- they are NOT separate URLs.

**Scope isolation:**
- English faith pages: `/faith/gita/{verse-slug}/{situation-slug}` -- build now
- Hindi faith pages: `/hi/faith/gita/{verse-slug}/{situation-slug}` -- build after `/hi/` infrastructure is confirmed

---

## 6. Content Freshness -- Evergreen Rule

**All faith module URLs must be evergreen.** Date-stamped or season-stamped URLs are banned.

| Banned Pattern | Correct Pattern |
|---|---|
| `/faith/daily/aries/may-27-scripture` | `/faith/daily/aries/may` |
| `/faith/gita/2-47/career-may-2026` | `/faith/gita/2-47/career-failure` |
| `/faith/bible/anxiety-2026` | `/faith/bible/anxiety` |

Evergreen URLs accumulate authority over time. Date URLs go stale, lose rank, and create infinite URL spaces that trigger crawl budget waste.

---

## 7. References

- `PROCESS_5_CONTENT_ANCHOR_FRAMEWORK.md` -- 3-anchor rule and linguistic isolation
- `PROCESS_6_SCHEMA_ORG_TYPES_BY_MODULE.md` -- Correct JSON-LD types
- `Faith_Hubs/CODEX_COMMISSION_FAITH_20K.md` -- Faith module commission brief
- `Faith_Hubs/FAITH_CONTENT_GENERATION_TEMPLATE.md` -- Codex-ready content generation template
