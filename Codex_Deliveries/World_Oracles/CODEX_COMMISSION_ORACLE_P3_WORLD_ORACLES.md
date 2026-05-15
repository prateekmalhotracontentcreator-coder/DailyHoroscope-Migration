# Codex Commission Brief -- ORACLE-P3: Multi-Scriptural World Oracles (Phase 3)
> Commission ID: ORACLE-P3
> Thread: World Oracles (new thread -- Phase 3)
> Issued: 2026-05-15 | Priority: 🟢 LOW -- Phase 3
> Pre-condition: KP Oracle fully live and battle-tested (KP-2A + KP-2B + KP-Sprint2 all integrated). No earlier dependency.

---

## Overview

EverydayHoroscope's vision extends beyond Vedic astrology to become a **universal spiritual guidance platform**. Phase 3 introduces five additional oracle modules -- each sharing the same grid-based interaction mechanic as Krishna Prashnavali but with distinct sacred traditions, content packs, visual rituals, and audio identities.

**The 5 World Oracle Modules:**

| Module | Tradition | Grid | Audio | Priority |
|---|---|---|---|---|
| **Bible Oracle** ("The Promise Box") | Christian | 66 Books of the Bible | Cathedral organ + choir | Phase 3A |
| **Islamic Fal-nama** | Islamic / Sufi | 28 Arabic letters (ط and ظ variants) | Ney flute + Bismillah | Phase 3A |
| **Taoist I Ching** | Taoist / Chinese | 64 Hexagrams (coin toss mechanic) | Nature ambience (water, birds) | Phase 3A |
| **Greek Oracle of Delphi** | Greek | 24 Greek letters on ostraca (pottery shards) | Lyre + marble ambience | Phase 3B |
| **Sikh Hukamnama** | Sikh | 31 Raags (musical modes) | Raag strings + Waheguru chant | Phase 3B |

**Also in scope for Phase 3:**
- Guna-Meter gamification (Tamas / Rajas / Sattva progress bar) -- tied to KP Oracle remedy completion

---

## Shared Architecture (The Oracle Framework)

All 5 modules share the same backend + frontend pattern as Krishna Prashnavali. Do NOT build each from scratch -- build a reusable **OracleFramework** and configure per-module.

### Shared Backend Pattern

```python
# Each oracle gets its own router file:
# bible_oracle_router.py
# falnama_oracle_router.py
# iching_oracle_router.py
# greek_oracle_router.py
# hukamnama_oracle_router.py

# All share the same endpoints pattern:
GET  /api/{oracle-slug}/meta           # grid config (size, cell labels, tradition info)
POST /api/{oracle-slug}/select         # { row, col } or { hexagram } → returns oracle answer
GET  /api/{oracle-slug}/history        # user's reading history (requires auth)
GET  /api/{oracle-slug}/answer/{id}    # single answer by ID
```

### Shared Frontend Pattern

```
frontend/src/pages/{OracleName}Page.jsx    ← per-module page
frontend/src/components/OracleGrid.jsx     ← reusable grid (already exists as KrishnaOracleGrid -- extend to be configurable)
frontend/src/components/OracleReveal.jsx   ← reusable reveal card (configurable per tradition)
frontend/src/components/OracleRitual.jsx   ← pre-grid ritual animation (configurable per tradition)
```

### Shared MongoDB Pattern

Each oracle gets its own collection:
```
bible_oracle_answers      ← 66 books × N verses
falnama_oracle_answers    ← 28 letters × N answers
iching_hexagrams          ← 64 hexagrams with Wilhelm interpretation
greek_oracle_answers      ← 24 letters × N answers
sikh_hukamnama_raags      ← 31 raags × N shabads
```

---

## Module Specs

### Module 1 -- Bible Oracle ("The Promise Box")

**Theme:** Personal promise and covenant. "What does God's Word say about this?"

**Grid:** 66 cells -- one per Book of the Bible
- Old Testament Books: 39 cells (dark leather/parchment texture)
- New Testament Books: 27 cells (lighter gold/cream texture)
- User taps one Book → system returns a promise/verse from that Book

**Content pack:**
- Each of 66 Books has 3-5 curated promise verses (∼250 total answers)
- Answer format: Verse text + Book name + Chapter:Verse reference + "The Promise" -- a 2-sentence personalised application of the verse to the user's situation

**Ritual animation:**
- Pre-grid: gentle cross-shaped gold light beam, soft cathedral bells (2 seconds)
- Reveal: page turns open animation, verse appears as if handwritten on parchment

**Audio:**
- Background: cathedral organ drone (low, reverberant)
- On reveal: single choir "Amen" tone

**SEO route:** `/bible-oracle`
**Page title:** "Bible Oracle -- God's Promise for Your Question"

---

### Module 2 -- Islamic Fal-nama (Oracle of the Unseen)

**Theme:** Seeking divine guidance through the sacred letters of Arabic.

**Grid:** 28 cells -- the 28 letters of the Arabic alphabet (including ط and ظ variants)
- Each cell shows the Arabic letter + its English transliteration
- Geometric tile background (Islamic tessellation pattern in gold/teal)

**Interaction:** User asks their question silently, then taps a letter "as guided by the heart"

**Content pack:**
- Each letter maps to a Quranic concept + Sufi teaching + practical action
- Answer format: Arabic phrase (Bismillah opening) + Quranic verse + Sufi interpretation + Practical action

**Ritual animation:**
- Pre-grid: geometric pattern assembles piece by piece (2.5 seconds), "اَللّٰهُ" fades in at centre
- Reveal: scroll unfurls from right to left (Arabic reading direction)

**Audio:**
- Background: Ney flute drone
- On reveal: soft "Bismillah ir-Rahman ir-Rahim" whisper

**SEO route:** `/falnama-oracle`
**Page title:** "Islamic Fal-nama -- Divine Guidance from the Sacred Letters"

---

### Module 3 -- Taoist I Ching

**Theme:** The Book of Changes. "What is the nature of this moment?"

**Grid:** 3-coin toss mechanic → generates 6 lines → one of 64 hexagrams
- NOT a tap-grid. User tosses 3 virtual coins 6 times (tap to toss each round)
- Each toss: coin flip animation (heads/tails), auto-assigns yin/yang line
- After 6 tosses: hexagram is constructed line by line with animation

**Content pack:**
- 64 hexagrams, each with:
  - Hexagram name (Chinese + English)
  - King Wen text (paraphrased, non-copyrighted)
  - Wilhelm interpretation (public domain -- Richard Wilhelm 1924 translation)
  - Temple Team modern application (brief, 2-3 sentences)
  - Changing lines guidance (if any toss produced a "moving line")

**Ritual animation:**
- Pre-ritual: bamboo stalks animation (traditional alternative to coins) fades to coin interface
- Coin toss: satisfying flip animation, heads (Yang ─) or tails (Yin ─ ─)
- Hexagram build: lines appear one by one, bottom to top (traditional direction)

**Audio:**
- Background: water flowing + birds (forest ambience)
- On each coin toss: light percussion click
- On hexagram reveal: gentle gong strike

**SEO route:** `/i-ching`
**Page title:** "I Ching -- The Oracle of Changes | Cast Your Hexagram"

---

### Module 4 -- Greek Oracle of Delphi

**Theme:** The Pythia speaks. Ancient Greek wisdom for modern decisions.

**Grid:** 24 cells -- the 24 letters of the Greek alphabet
- Cells styled as ostraca (pottery shards) with letter inscribed
- Dark marble/stone background with torch-light gold accents

**Content pack:**
- Each letter maps to one of the 147 Delphic Maxims (attributed to the Temple of Apollo)
- Answer format: Greek letter + name + Maxim (in Greek + English translation) + 2-sentence modern interpretation

**Ritual animation:**
- Pre-grid: smoke/mist clears to reveal the marble grid (the Pythia's cave ambience)
- On letter tap: stone glows, cracks appear around it
- Reveal: tablet rises from the smoke with the maxim inscribed

**Audio:**
- Background: Lyre (simple melody, ancient mode)
- On reveal: marble "thud" sound + silence

**SEO route:** `/oracle-of-delphi`
**Page title:** "Oracle of Delphi -- Ancient Greek Wisdom for Your Question"

---

### Module 5 -- Sikh Hukamnama

**Theme:** The Divine Command. Guru Granth Sahib's guidance for the day.

**Grid:** 31 cells -- the 31 Raags (musical modes) of Guru Granth Sahib
- Cells show Raag name in Gurmukhi + romanisation
- Warm saffron/gold background with Khanda symbol

**Interaction:** User offers an Ardaas (silent prayer) then selects a Raag

**Content pack:**
- Each Raag maps to 3-5 Shabads (hymns) from Guru Granth Sahib
- Answer format: Shabad opening lines (Gurmukhi script + transliteration + English translation) + Gurmat (teaching) interpretation + Practical spiritual action

**Ritual animation:**
- Pre-grid: Ik Onkar symbol fades in, Ardaas pause prompt (5-second hold with progress ring)
- Reveal: Shabad lines appear one by one in Gurmukhi script + English below

**Audio:**
- Background: Raag string ambience (Sarangi or Dilruba)
- On reveal: "Waheguru" chant (single repetition, fading out)

**SEO route:** `/hukamnama`
**Page title:** "Sikh Hukamnama -- Guru Granth Sahib's Divine Command"

---

## Guna-Meter Gamification (Phase 3 -- tied to KP Oracle)

**Concept:** As users complete remedies, meditations, and spiritual practices across the app, their Guna state shifts. This is a cross-module gamification layer.

**Three Gunas:**
| Guna | State | Colour | Triggers |
|---|---|---|---|
| Tamas | Inertia / Darkness | Dark Red 🔴 | No remedy completion in 7+ days, declined KP prompts |
| Rajas | Action / Passion | Amber 🟡 | Active remedy streak 1-6 days, KP sessions without follow-through |
| Sattva | Clarity / Light | Emerald 🟢 | 7+ day remedy streak, questionnaire completed, 3+ modules used |

**Implementation:**
- Backend: `user_guna_profile` MongoDB collection
- Score: computed from Punya Rewards action_log + remedy completion log + questionnaire status
- Frontend: Guna-Meter progress bar (three-segment: Tamas | Rajas | Sattva) on user profile / dashboard
- App background: subtle gradient shift as Guna state changes (CSS variable update)

---

## Phase Sequence

| Phase | Modules | Pre-condition |
|---|---|---|
| Phase 3A | Bible Oracle + Islamic Fal-nama + Taoist I Ching | KP Oracle fully live |
| Phase 3B | Greek Oracle + Sikh Hukamnama | Phase 3A launched |
| Phase 3 Ongoing | Guna-Meter gamification | KP Oracle + at least 1 World Oracle live |

---

## Content Note

**Bible Oracle:** All Bible verses are public domain (KJV, ASV, or WEB translations). No copyright issue.
**I Ching:** Wilhelm translation (1924) is public domain. King Wen text (ancient) is public domain.
**Delphic Maxims:** Ancient text, fully public domain.
**Fal-nama / Hukamnama:** Sacred texts (Quran, Guru Granth Sahib) -- use reverent paraphrase + attribution. Do not reproduce verbatim without religious sensitivity review.

---

## Routes to Register (App.js -- Phase 3A first)

```jsx
const BibleOraclePage = lazy(() => import('./pages/BibleOraclePage'));
const FalnamaOraclePage = lazy(() => import('./pages/FalnamaOraclePage'));
const IChingPage = lazy(() => import('./pages/IChingPage'));

<Route path="/bible-oracle" element={<BibleOraclePage />} />
<Route path="/falnama-oracle" element={<FalnamaOraclePage />} />
<Route path="/i-ching" element={<IChingPage />} />
```

---

## Sitemap (add for Phase 3A launch)

```xml
<url><loc>https://www.everydayhoroscope.in/bible-oracle</loc><priority>0.80</priority></url>
<url><loc>https://www.everydayhoroscope.in/falnama-oracle</loc><priority>0.80</priority></url>
<url><loc>https://www.everydayhoroscope.in/i-ching</loc><priority>0.80</priority></url>
```

---

## Commit Format

```
feat(world-oracles): add [module-name] oracle -- Phase 3A
```

---

## ⚠️ This Is a Phase 3 Planning Document

**Do not start building until Temple Team explicitly opens the Phase 3 thread.** Issue this brief to Codex only when:
1. KP-2A, KP-2B, and KP-Sprint2 are all INTEGRATED
2. KP Oracle has been live for at least 30 days (user feedback collected)
3. Content packs for Phase 3A (Bible, Fal-nama, I Ching) are prepared by Temple Team
