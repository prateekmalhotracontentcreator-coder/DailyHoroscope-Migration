# Faith Content Generation Template
> EverydayHoroscope.in -- Faith & Scripture Hub
> Document Type: Codex Content Generation Reference (Process Doc 8)
> Version: 1.0
> Date: 2026-05-27
> Scope: Static pre-generation of all Faith module page content before MongoDB seed

---

## Overview

This document provides the exact content generation templates that Codex must use to produce faith page content. These are **static pre-generation templates** -- content is generated once, stored in `faith_seo_data.py`, and served via API. We do NOT make runtime LLM calls for page content.

All content is generated from these templates in a single Codex pass, reviewed for compliance, then seeded into MongoDB.

---

## Template 1 -- Gita Verse × Life Situation Page

**Route:** `/faith/gita/{chapter}-{verse}/{situation-slug}`
**Example:** `/faith/gita/2-47/career-failure`

### Content Generation Prompt Template

Use the following structure to generate content for each of the 10,500 verse × situation combinations. Generate content in FULL -- do not truncate, do not use placeholders.

```
CONTEXT:
- Verse: Bhagavad Gita Chapter {CHAPTER}, Verse {VERSE}
- Sanskrit (IAST): {SANSKRIT_TEXT}
- Transliteration: {TRANSLITERATION}
- English Translation: {TRANSLATION}
- Situation: {SITUATION_LABEL} (e.g., "career failure", "grief", "relationship breakdown")
- Planet/Transit Relevance: {PLANET_SLUG} (e.g., "saturn-in-capricorn")

SECTION 1 -- Situation Hook (80-100 words)
Write a paragraph that opens ENTIRELY in the emotional vocabulary of {SITUATION_LABEL}.
Do NOT mention the Gita, verse number, Krishna, Arjuna, or any scripture.
Open inside the reader's experience. What does this situation feel like? What is the specific
emotional texture? What is the question the person is carrying?
Vocabulary must be: contemporary, psychological, specific to this situation.
Forbidden: generic spiritual encouragement, platitudes, "everything happens for a reason".

SECTION 2 -- Verse Presentation (50-70 words)
Present the verse naturally as the answer to the situation.
Format:
- Sanskrit with IAST diacritics on one line
- Transliteration on the next line (italicised in HTML)
- English translation credited to {TRANSLATION_SOURCE}
One connecting sentence showing why this verse speaks directly to what was described in Section 1.

SECTION 3 -- Etymology Block (100-120 words) [ANCHOR 2]
Break down 2-3 key Sanskrit words from this verse.
For each word:
- Sanskrit term (Devanagari + IAST)
- Root etymology (Sanskrit root verb/noun it derives from)
- Literal meaning of the root
- How the layered meaning of this root applies specifically to {SITUATION_LABEL}
This section must feel like a genuine linguistic deep-dive, not a dictionary definition.

SECTION 4 -- Modern Application (100-120 words)
How does the teaching of this verse practically change how someone in {SITUATION_LABEL} acts TODAY?
Be specific. Name a concrete behavior change. Name what to stop doing and what to start doing.
Forbidden: "trust the process", "let go and let God", "everything will work out".
Required: at minimum one specific, actionable instruction.

SECTION 5 -- Astrological Transit Layer (80-100 words) [ANCHOR 3]
Which planetary transit or dasha period makes this teaching most relevant?
Reference: {PLANET_SLUG} transit.
Connect the planetary energy archetype to the teaching of this verse.
Include a link reference to: /transits/{PLANET_SLUG}
Include a link reference to the panchang for auspicious practice timing.
State specifically: during a {planet} transit, the verse's instruction manifests as [specific practice].

SECTION 6 -- FAQ (3 questions, 50 words each)
Q1: "What does Bhagavad Gita {CHAPTER}:{VERSE} say about {situation-keyword}?"
Q2: "How do I apply Gita {CHAPTER}:{VERSE} in {situation-keyword} practically?"
Q3: One long-tail question a person in this situation would actually type into Google.
Answers must be original -- do not repeat content from sections above verbatim.
```

### Data Object Structure (Python -- `faith_seo_data.py`)

```python
{
    "id": "gita-{chapter}-{verse}-{situation_slug}",
    "route": f"/faith/gita/{chapter}-{verse}/{situation_slug}",
    "chapter": int,
    "verse": int,
    "situation_slug": str,          # e.g., "career-failure"
    "situation_label": str,         # e.g., "Career Failure"
    "sanskrit": str,                # Full Sanskrit text (IAST)
    "transliteration": str,
    "translation": str,
    "translation_source": str,      # e.g., "A.C. Bhaktivedanta Swami"
    "hook": str,                    # Section 1 -- 80-100 words
    "etymology": str,               # Section 3 -- 100-120 words
    "application": str,             # Section 4 -- 100-120 words
    "transit_layer": str,           # Section 5 -- 80-100 words
    "transit_slug": str,            # e.g., "saturn-in-capricorn"
    "faq": [
        {"q": str, "a": str},
        {"q": str, "a": str},
        {"q": str, "a": str}
    ],
    "meta_title": str,              # Max 60 chars
    "meta_description": str,        # Max 155 chars
    "sitemap_priority": "0.7"
}
```

---

## Template 2 -- Bible Promise × Life Transition Page

**Route:** `/faith/bible/{topic-slug}/{transition-slug}`
**Example:** `/faith/bible/anxiety/divorce`

### Content Generation Prompt Template

```
CONTEXT:
- Bible Topic: {TOPIC_LABEL} (e.g., "anxiety", "fear", "provision")
- Life Transition: {TRANSITION_LABEL} (e.g., "divorce", "job loss", "grief", "new city")
- Primary Verse: {VERSE_TEXT} -- {BOOK} {CHAPTER}:{VERSE}
- Translation: {TRANSLATION} (NIV / KJV / ESV -- specify)
- Vedic Resonance Planet: {PLANET} (for cross-tradition bridge)

SECTION 1 -- Emotional Frame (80-100 words)
Open ENTIRELY in the emotional vocabulary of {TRANSITION_LABEL}.
Do NOT mention the Bible, verse, God, or any scripture.
Write from inside the experience. What does {TRANSITION} feel like at 2am?
What is the specific fear? The specific loss? The specific confusion?
This section must make someone in this transition feel seen.

SECTION 2 -- Verse Presentation (30-50 words)
Present the verse as the answer.
Format: verse text -- Book Chapter:Verse (Translation Version)
One sentence connecting the verse to the emotional state described in Section 1.

SECTION 3 -- Hermeneutical Unpacking (100-120 words) [ANCHOR 2]
What does this verse actually promise? What does it NOT promise?
Original language note (Hebrew/Greek term) for 1 key word where meaningful.
What was the original context of this verse? Who was it written to?
How does that original context make the promise MORE applicable to {TRANSITION}, not less?
This section demonstrates expertise -- do not produce generic commentary.

SECTION 4 -- Practical Application (100-120 words)
What can the reader do TODAY with this promise?
Minimum: one specific prayer practice, one specific thought-replacement exercise,
or one specific decision the verse helps them make.
Forbidden: "just trust God", "surrender your worries", "have faith".
Required: the HOW -- not just the what.

SECTION 5 -- Vedic Resonance Bridge (80-100 words) [ANCHOR 3]
How does Vedic astrology or the Bhagavad Gita view the same theme?
Which planet governs {TRANSITION_LABEL}'s domain (Saturn for loss, Moon for grief, etc.)?
What Gita teaching parallels this Bible promise?
This section is the unique cross-tradition bridge that makes our pages distinct from
any other Bible promise site. It directly serves our Indian + NRI audience.
Include a link reference to the parallel Gita verse page.

SECTION 6 -- FAQ (3 questions, 50 words each)
Q1: "What does the Bible say about {transition-keyword}?"
Q2: One specific long-tail question about the verse itself.
Q3: One long-tail question about applying the promise practically.
```

### Data Object Structure

```python
{
    "id": "bible-{topic_slug}-{transition_slug}",
    "route": f"/faith/bible/{topic_slug}/{transition_slug}",
    "topic_slug": str,
    "topic_label": str,
    "transition_slug": str,
    "transition_label": str,
    "verse_text": str,
    "verse_ref": str,               # e.g., "Philippians 4:6"
    "verse_translation": str,       # "NIV" | "KJV" | "ESV"
    "emotional_frame": str,         # Section 1
    "hermeneutical": str,           # Section 3
    "application": str,             # Section 4
    "vedic_bridge": str,            # Section 5
    "gita_cross_link": str,         # e.g., "/faith/gita/2-47/anxiety"
    "faq": [
        {"q": str, "a": str},
        {"q": str, "a": str},
        {"q": str, "a": str}
    ],
    "meta_title": str,
    "meta_description": str,
    "sitemap_priority": "0.7"
}
```

---

## Template 3 -- Transit × Scripture Page

**Route:** `/faith/transit/{planet-sign}/{tradition}`
**Example:** `/faith/transit/saturn-in-capricorn/gita`

### Content Generation Prompt Template

```
CONTEXT:
- Planet: {PLANET}
- Sign: {SIGN}
- Transit Slug: {PLANET_SLUG} (matches existing /transits/{PLANET_SLUG} page)
- Tradition: {TRADITION} -- "gita" or "bible"

SECTION 1 -- Transit Energy Description (100 words)
What does {PLANET} in {SIGN} energetically represent?
Vocabulary: planetary archetype, elemental quality, historical pattern of this transit.
Link reference: /transits/{PLANET_SLUG}

SECTION 2 -- Scripture for This Transit (200 words)
For Gita tradition: 2 verses that speak to this planetary energy.
For Bible tradition: 2 verses (promises or teachings) relevant to this transit's themes.
For each verse: full text + why this verse specifically addresses what {PLANET_SLUG} brings.

SECTION 3 -- Spiritual Practice for This Transit (150 words)
What to DO during this transit from a faith perspective.
Specific practices. Times from panchang when practice is most powerful.
Link reference: /panchang/{city}/{date} (generic reference)

SECTION 4 -- Mantra / Prayer (50 words)
For Gita pages: Sanskrit mantra or shloka for daily recitation during this transit.
For Bible pages: A specific scripture-based prayer (original wording, not copied).
```

---

## Template 4 -- Daily Scripture Page (Evergreen)

**Route:** `/faith/daily/{sign}/{month}`
**Example:** `/faith/daily/aries/may`

### Content Generation Prompt Template

```
CONTEXT:
- Zodiac Sign: {SIGN}
- Month: {MONTH}
- Sign Element: {ELEMENT} (Fire/Earth/Air/Water)
- Sign Ruling Planet: {RULING_PLANET}
- Month's Dominant Vedic Energy: {MONTH_ENERGY} (e.g., "Venus-ruled, harvest focus" for October)

SECTION 1 -- Sign + Month Energy (100 words)
What does {MONTH} specifically call forth for {SIGN} natives?
Vocabulary: sign archetype + seasonal energy + ruling planet interaction.
NOT a generic monthly horoscope -- a spiritual LENS on the month.

SECTION 2 -- Gita Verse for This Month (150 words)
Which Gita verse best speaks to what {SIGN} needs to hear in {MONTH}?
Present verse + full application to sign-month combination.

SECTION 3 -- Bible Promise for This Month (150 words)
Which Bible promise best speaks to the {SIGN}-{MONTH} energy?
Present verse + full application.

SECTION 4 -- Daily Practice (100 words)
5 concrete daily practices for {SIGN} in {MONTH}.
Bulleted list. Specific, actionable.

SECTION 5 -- Premium CTA (50 words)
"Receive a personalized 21-day scripture plan matched to your Vedic birth chart."
Link to premium product. Do not make medical/health claims.
```

---

## ECHO // PACE Compliance Notes for Codex

1. **Run the compliance check** (`backend/tests/faith_audit.py`) on each cluster of 15 pages (same verse, 15 situations) before finalizing `faith_seo_data.py`. Ceiling: ≤30% worst-pair similarity.

2. **The Section 1 hook** is the primary compliance mechanism. If two pages in the same verse-cluster have similar Section 1 openers, they will fail TF-IDF. Each situation must open with entirely different vocabulary.

3. **The Section 5 transit layer** is the secondary compliance differentiator. Different transit slugs = different planetary vocabulary = lower similarity.

4. **Never start two pages in the same cluster with the same sentence structure.** If page 1 opens "When the weight of career failure settles...", page 2 cannot open "When the weight of relationship breakdown settles..." -- that is a structural repeat that TF-IDF will detect.

5. **FAQ questions** should use long-tail search vocabulary natural to someone in that life situation. Avoid the same question patterns across pages in the same cluster.

---

## References

- `ECHO_PACE_PROCESS/PROCESS_5_CONTENT_ANCHOR_FRAMEWORK.md` -- 3-anchor rule
- `ECHO_PACE_PROCESS/PROCESS_6_SCHEMA_ORG_TYPES_BY_MODULE.md` -- JSON-LD types
- `ECHO_PACE_PROCESS/PROCESS_7_YMYL_CONTENT_QUALITY.md` -- YMYL standards
- `Faith_Hubs/CODEX_COMMISSION_FAITH_20K.md` -- Full commission brief
- `backend/tests/faith_audit.py` -- TF-IDF compliance script
