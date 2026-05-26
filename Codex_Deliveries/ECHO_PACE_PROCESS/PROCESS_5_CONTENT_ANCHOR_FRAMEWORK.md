# Process Doc 5 -- Content Anchor Framework (3-Anchor Rule)
> EverydayHoroscope.in -- E.C.H.O. // P.A.C.E. Compliance System
> Document Type: Platform-Wide Process Reference
> Version: 1.0
> Date: 2026-05-27
> Scope: All SEO modules building programmatic pages from a fixed content catalogue

---

## 1. The Problem This Document Solves

Every programmatic SEO module on this platform is built from a **fixed source catalogue**:
- Festival module: fixed list of festivals × fixed list of regions
- Tarot module: fixed deck of 78 cards × fixed list of spreads
- Faith module: fixed corpus of ~700 Gita verses × fixed list of life situations

The compliance ceiling is **≤40% TF-IDF cosine similarity** between any two pages in the same thematic cluster.

The failure mode that causes Google's spam filter to trigger is **template reuse**: same sentence skeleton, only nouns swapped. TF-IDF detects structural word patterns even after stop-word filtering.

**Synonym swapping does NOT fix this.** Structural variation does.

---

## 2. The Universal Solution -- The 3-Anchor Rule

Every page in a programmatic cluster must contain **3 structurally unique anchors** -- content blocks where:
- Each block uses a vocabulary cluster not shared with other pages in the cluster
- Each block's sentence structure is distinct (different subject, verb pattern, paragraph opening)
- The 3 anchors together account for ≥60% of the page's total word count

The 3-anchor rule is the primary mechanism that guarantees <40% similarity between any two pages regardless of how similar their source material is.

---

## 3. Cross-Module Anchor Mapping

| Module | Anchor 1 (Hook / S1) | Anchor 2 (Core Differentiation / S2) | Anchor 3 (Unique Close / S3) |
|---|---|---|---|
| **Festival × Region** (M3) | Regional ritual practice (vocabulary: offerings, customs, local deity, preparation method) | Communal expression (vocabulary: gathering, procession, collective act, celebration form) | Regional food and material culture (vocabulary: specific dish names, craft, textile, bazaar vocabulary) |
| **Tarot Card × Spread** (M4/TAR-M4) | Life-situation-intent frame (vocabulary: the specific situation the querent is in -- career crisis, relationship choice, etc.) | Inter-card dynamic in spread position (vocabulary: how this card speaks to the spread's surrounding cards, position-specific meaning) | Action guidance (vocabulary: concrete next step, decision point, what to do vs. avoid in the specific spread context) |
| **Faith: Gita Verse × Life Situation** (FAITH-1) | Modern psychological / emotional hook (vocabulary: contemporary life language -- burnout, anxiety, identity crisis, career pivot) | Etymological root-token deconstruction of the Sanskrit shloka (vocabulary: Sanskrit root words, transliteration, word-by-word unpacking) | Astrological transit mitigation layer (vocabulary: planetary energy, transit timing, dasha-specific application to the life situation) |
| **Faith: Bible × Life Transition** (FAITH-2) | Emotional resonance frame (vocabulary: the specific emotional state of someone in that life transition -- grief, fear, uncertainty, hope) | Hermeneutical unpacking of the promise (vocabulary: original Greek/Hebrew context, what the verse means precisely in its translation context) | Practical covenant application (vocabulary: what the reader can do today, the specific action, the specific prayer, the specific decision point) |
| **Transit × Scripture** (FAITH-3) | Planetary energy description (vocabulary: the transit's archetypal energy -- Saturn's restriction, Jupiter's expansion, Rahu's disruption) | Cross-tradition scriptural resonance (vocabulary: how both Gita and Bible speak to this exact planetary energy) | Timing-specific guidance (vocabulary: the exact window, what to do during vs. after the transit, panchang alignment) |
| **Angel Numbers** | Numerological frequency (vocabulary: the specific vibrational meaning of that number pattern) | Life-situation application (vocabulary: the specific situation or intention this number pattern applies to) | Action step (vocabulary: concrete, specific -- not generic spiritual language) |

---

## 4. The Fixed Content Trap -- Hardest Compliance Problem Per Module

### Festival Module: Same Festival, 15 Regions
**Problem:** "Diwali" has the same date, same mythology, same core ritual across all 15 regional pages.
**Solution:** Region-first vocabulary. The opening sentence leads with the region's UNIQUE cultural expression of the festival -- not the festival's universal description. Vocabulary pool = regional food, regional deity variant, regional craft, regional linguistic marker.

### Tarot Module: Same Card, 60 Spreads (The Tower Problem)
**Problem:** The Tower card has the same core meaning across all 60 spread positions.
**Solution:** Spread-position-first vocabulary. Every spread page opens with the SPREAD'S purpose (job interview spread, grief healing spread, relationship crossroads spread). The Tower's meaning is filtered THROUGH that spread's lens, not stated in isolation.

### Faith Module: Same Verse, 15 Life Situations
**Problem:** Gita 2:47 "You have the right to perform your prescribed duties, but you are not entitled to the fruits of your actions" has the same Sanskrit text across all 15 life-situation pages.
**Solution:** Situation-first Linguistic Isolation Framing. The page opens IN the situation's emotional language BEFORE the verse is introduced. A career failure page opens with the psychology of career failure. A grief page opens with the language of grief. The verse is a SOLUTION to an emotional state, not a text to be explained.

---

## 5. Linguistic Isolation Framing -- The Technique

**What it is:** Open the page entirely in the situation's vocabulary. Do not name the verse or text source until at least paragraph 2. Force the content engine to generate 80-100 words of situation-specific language before the fixed source material is introduced.

**Why it works:** TF-IDF similarity is defeated when the opening vocabulary cluster (which carries the highest TF weight because it appears first in the document) is situation-specific, not verse-specific. Two pages about different situations referencing the same verse will have low similarity because their highest-weight vocabulary clusters are completely different.

**Template Pattern:**
```
[Situation Hook -- 80-100 words entirely in situation vocabulary. No verse reference.]
[Verse introduction -- 1-2 sentences connecting situation to text.]
[Anchor 2: Etymological/hermeneutical unpacking]
[Anchor 3: Astrological transit or practical application]
[FAQ section: 3-5 questions in long-tail search vocabulary]
```

---

## 6. Stop-Word Registers Per Module

Before running TF-IDF similarity checks, the following module-specific vocabulary must be added to the custom stop-word list to prevent false positives (domain terminology appearing on every page by necessity).

### Festival Module Stop Words
`festival, puja, prasad, muhurta, region, celebrate, celebration, devotees, prayer, worship, auspicious, tithi, nakshatra`

### Tarot Module Stop Words
`tarot, card, spread, reading, position, upright, reversed, deck, querent, celtic, cross, draw, pull, layout`

### Faith Module Stop Words
`chapter, verse, shloka, slokas, gita, bhagavad, bible, scripture, testament, lord, god, krishna, arjuna, christ, jesus, holy, faith, unto, shall, thee, thou, recitation, meaning, translation, prayer, spiritual`

### Angel Numbers Stop Words
`angel, number, sequence, pattern, seeing, sign, divine, universe, synchronicity, numerology, frequency, vibration`

---

## 7. TF-IDF Compliance Script Reference

Use the platform compliance script in `backend/tests/faith_audit.py` as the canonical testing template. Adapt stop-word lists per module. The universal parameters are:

```python
TfidfVectorizer(stop_words=custom_stops, ngram_range=(1, 2))
CEILING = 40.0  # ≤40% worst-pair similarity
FAITH_CEILING = 30.0  # Faith module uses stricter 30% ceiling (YMYL content)
```

**Grouping logic:** Test within clusters (same verse across situations, NOT across different verses). Do NOT test inter-cluster similarity -- only intra-cluster.

**Pass/fail threshold:**
- ≤30%: Green -- optimal
- 31-40%: Amber -- acceptable but review content anchors
- >40%: Red -- FAIL -- rebuild Anchor 1 with stricter linguistic isolation

---

## 8. References

- `PROCESS_2_CICD_COMPLIANCE_TESTING.md` -- How to run the TF-IDF audit in CI
- `backend/tests/faith_audit.py` -- Faith module compliance script
- `Tarot/TAR_ECHO_PACE_GAI_CONSULTATION.md` -- Tarot-specific compliance resolution log
- `Faith_Hubs/CODEX_COMMISSION_FAITH_20K.md` -- Faith module commission brief
- `SEO/PROCESS_7_YMYL_CONTENT_QUALITY.md` -- E-E-A-T standards for YMYL modules
