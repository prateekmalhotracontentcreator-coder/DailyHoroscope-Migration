# Contract: Jyotish Narrative Engine — Hierarchical Interpretation Database
> Client: EverydayHoroscope (SkyHound Studios)
> Platform: https://www.everydayhoroscope.in
> Backend: FastAPI on Render · Frontend: React 18 on Vercel
> Repo: github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration
> Astronomy Engine: pyswisseph 2.10.x (Lahiri ayanamsa, Swiss Ephemeris)

---

## 1. Module Overview

Build an **internal Knowledge Engine** that transforms traditional Vedic astrology texts into a
structured, queryable rule database — then uses an LLM layer to weave matched rules into
coherent, personalised narratives.

This is **not a user-facing page** — it is an **infrastructure module** that powers every
interpretation across the platform (Kundali reports, Longevity analysis, Horoscope narratives,
Tarot insights, Numerology guidance).

### Architecture: 3-Layer Stack

```
┌─────────────────────────────────────────────────────────┐
│  Layer 3: NARRATIVE LAYER (Claude API)                  │
│  Receives matched rules + chart context → generates     │
│  coherent multi-paragraph interpretation in user's tone │
└────────────────────────┬────────────────────────────────┘
                         │ matched rules + context
┌────────────────────────┴────────────────────────────────┐
│  Layer 2: RULE ENGINE (Python)                          │
│  Evaluates chart data against rule conditions            │
│  Scores relevance, resolves conflicts between sources   │
│  Filters by category (career, health, relationships)    │
└────────────────────────┬────────────────────────────────┘
                         │ chart positions + dashas
┌────────────────────────┴────────────────────────────────┐
│  Layer 1: DATA LAYER (MongoDB)                          │
│  Hierarchical Interpretation Database                    │
│  Structured rules extracted from classical texts         │
│  If-Then conditions with multi-source attribution       │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Data Layer — Hierarchical Interpretation Database

### 2a. MongoDB Collection: `interpretation_rules`

Each rule is a document with this schema:

```json
{
  "_id": "ObjectId",
  "rule_id": "R-SAT-7H-001",
  "version": 1,

  "condition": {
    "type": "planet_in_house",
    "planet": "Saturn",
    "house": 7,
    "sign": null,
    "dignity": null,
    "retrograde": null,
    "aspected_by": null,
    "conjunct_with": null,
    "nakshatra": null,
    "dasha_active": null
  },

  "interpretation": {
    "summary": "Saturn in the 7th house indicates delayed marriage, a serious & committed partner, and a relationship built on duty and responsibility.",
    "detailed": "When Saturn occupies the 7th house of partnerships, the native tends to approach marriage with caution and maturity. Marriage may be delayed past 28-30 years. The spouse is often older, more responsible, or from a different social background. While the early years may feel restrictive, Saturn rewards long-term commitment with a stable, enduring bond.",
    "full_text_passages": [
      {
        "text": "The native whose 7th house is occupied by Shani shall find marriage delayed, the spouse being elder, austere in nature, and devoted to duty. The bond, though tested by early hardship, shall endure as iron endures the forge...",
        "source": "Brihat Parashara Hora Shastra",
        "chapter": "Chapter 24, Shloka 42-44",
        "word_count": 280,
        "voice_tone": "classical"
      },
      {
        "text": "Saturn in the seventh house often manifests as a partner who brings structure and seriousness to the relationship. In modern contexts, this may indicate a late marriage or a partner met through professional settings...",
        "source": "B.V. Raman — How to Judge a Horoscope Vol. 1",
        "chapter": "Chapter 7",
        "word_count": 320,
        "voice_tone": "modern_analytical"
      }
    ],
    "positive_aspects": [
      "Lasting and stable marriage once established",
      "Partner is responsible and dependable",
      "Good for business partnerships requiring patience"
    ],
    "challenging_aspects": [
      "Delay in finding a suitable partner",
      "Emotional coldness or distance in early marriage",
      "Possible age gap with spouse"
    ],
    "remedies": [
      "Worship Lord Shani on Saturdays",
      "Donate black sesame seeds on Saturdays",
      "Recite Shani Beej Mantra 108 times"
    ]
  },

  "categories": ["relationships", "marriage", "partnerships"],
  "priority": 8,
  "intensity_score": 8.5,
  "source": {
    "primary": "Brihat Parashara Hora Shastra",
    "chapter": "Chapter 24 — Effects of Planets in Houses",
    "author_voice": "classical",
    "secondary_sources": [
      { "text": "Phaladeepika", "chapter": "Chapter 7", "voice_tone": "classical" },
      { "text": "Saravali", "chapter": "Chapter 30", "voice_tone": "classical" },
      { "text": "B.V. Raman — How to Judge a Horoscope", "chapter": "Ch 7", "voice_tone": "modern_analytical" }
    ]
  },

  "modifiers": [
    {
      "condition": { "aspected_by": "Jupiter" },
      "effect": "amplify_positive",
      "note": "Jupiter's aspect on Saturn in 7H significantly improves marital harmony and reduces delays."
    },
    {
      "condition": { "conjunct_with": "Rahu" },
      "effect": "amplify_negative",
      "note": "Saturn-Rahu conjunction in 7H can indicate unconventional or inter-caste marriage with initial family resistance."
    },
    {
      "condition": { "retrograde": true },
      "effect": "intensify",
      "note": "Retrograde Saturn in 7H deepens karmic lessons in relationships — past-life debts with spouse."
    }
  ],

  "conflicts_with": ["R-JUP-7H-001"],
  "weight": 0.85,
  "tags": ["saturn", "7th_house", "marriage", "delay", "karmic"],
  "active": true,
  "created_at": "2026-04-08T00:00:00Z",
  "updated_at": "2026-04-08T00:00:00Z"
}
```

### 2b. MongoDB Collection: `author_voices`

Track different source "voices" so the LLM can blend classical and modern perspectives.

```json
{
  "_id": "ObjectId",
  "voice_id": "classical",
  "display_name": "Classical Sanskrit Tradition",
  "tone_description": "Formal, verse-like, uses Sanskrit terminology with English translation in parentheses. Speaks with authority of ancient shastras.",
  "example_authors": ["Parashara", "Varahamihira", "Kalyana Varma"],
  "llm_instruction": "Write in a reverent, scholarly tone. Use phrases like 'The ancient texts declare...' and 'As per the shastras...'. Include Sanskrit terms with English translations."
}
```

Supported voice types:
| Voice | Description | Use Case |
|---|---|---|
| `classical` | Formal, shastra-based, Sanskrit terms | BPHS, Saravali, Phaladeepika |
| `modern_analytical` | Clear, psychological, practical | B.V. Raman, K.N. Rao |
| `kp_technical` | Precise, sub-lord focused, scientific tone | KP Reader, Krishnamurti |
| `spiritual` | Karmic, soul-purpose, philosophical | Yogananda, spiritual texts |
| `popular` | Conversational, accessible, encouraging | Modern horoscope columns |

### 2c. MongoDB Collection: `narrative_bridges`

Bridging phrases that help the LLM stitch multi-source text blocks into a single flow.

```json
{
  "_id": "ObjectId",
  "bridge_type": "contrast",
  "context": "When two rules give opposing predictions",
  "phrases": [
    "While your chart indicates {positive_theme}, the current planetary alignment introduces a counterbalancing energy of {negative_theme}...",
    "Ancient texts like {source_a} suggest {view_a}. However, the interpretation from {source_b} adds nuance — {view_b}. These competing energies in your chart create...",
    "There is a creative tension in your chart between {theme_a} and {theme_b}. Rather than seeing these as contradictions, think of them as..."
  ]
}
```

Bridge types:
| Type | When Used |
|---|---|
| `contrast` | Two rules contradict (wealth vs losses) |
| `reinforcement` | Multiple rules confirm same theme |
| `transition` | Moving from one life area to another (career → relationships) |
| `deepening` | Adding a modifier layer on top of a base interpretation |
| `temporal` | Connecting dasha periods ("In the years ahead...") |
| `cross_science` | Bridging astrology finding with numerology/tarot confirmation |

### 2d. Rule Condition Types

The engine must support these condition types (each maps to a query pattern):

| Condition Type | Example | Fields |
|---|---|---|
| `planet_in_house` | Saturn in 7th | planet, house |
| `planet_in_sign` | Moon in Cancer | planet, sign |
| `planet_in_nakshatra` | Moon in Rohini | planet, nakshatra |
| `planet_aspect` | Jupiter aspects 7th | planet, aspecting_house |
| `planet_conjunction` | Sun + Mercury in same house | planets[], house |
| `planet_dignity` | Jupiter exalted (Cancer) | planet, dignity (exalted/debilitated/own/enemy) |
| `planet_retrograde` | Saturn retrograde | planet, retrograde |
| `house_lord_in_house` | 7th lord in 12th | source_house, target_house |
| `yoga` | Gajakesari Yoga | yoga_name, planets[] |
| `dasha_period` | Saturn Maha Dasha | dasha_lord, level (maha/antar/pratyantar) |
| `transit` | Saturn transiting 8th from Moon | planet, transit_house, reference |
| `kp_sublord` | Sub-lord of 8th cusp is Jupiter | cusp_num, sub_lord |
| `composite` | Saturn in 7H AND Jupiter aspects | sub_conditions[], operator (AND/OR) |

### 2f. MongoDB Collection: `cross_science_combinations`

The "Multi-Factor Confirmation" engine — when different sciences (Astrology, Numerology,
Palmistry, Tarot) independently point to the same life theme, the prediction gains
significantly higher confidence.

```json
{
  "_id": "ObjectId",
  "combo_id": "COMBO_0042",
  "title": "The Born Leader",
  "theme": "leadership",
  "description": "Multiple sciences confirm strong authority and leadership potential",

  "triggers": {
    "astrology": {
      "conditions": ["Sun_in_10th", "Jupiter_aspects_10th"],
      "min_match": 1
    },
    "numerology": {
      "conditions": [
        { "number_type": "life_path", "values": [1, 8] },
        { "number_type": "expression", "values": [1, 22] }
      ],
      "min_match": 1
    },
    "palmistry": {
      "conditions": ["strong_sun_line", "mount_of_jupiter_developed"],
      "min_match": 1
    },
    "tarot": {
      "conditions": ["The Emperor", "The Sun", "Ace of Wands"],
      "min_match": 1
    }
  },

  "confidence_weights": {
    "astrology": 0.40,
    "numerology": 0.20,
    "palmistry": 0.25,
    "tarot": 0.15
  },

  "scoring": {
    "min_sciences_matched": 2,
    "intensity_when_all_four": 9.8,
    "intensity_when_three": 8.5,
    "intensity_when_two": 6.5
  },

  "narrative_template": "Your charts align powerfully for leadership. Your {astro_detail} mirrors your Life Path {numerology_detail} energy, while your palm reveals {palmistry_detail}. This rare multi-science confirmation suggests...",
  "categories": ["career", "leadership", "authority"],
  "active": true
}
```

**Phase 1 scope:** Define the schema + build the matching logic for astrology + numerology
cross-checks (the two sciences we have full engines for today).

**Phase 2 scope:** Add palmistry + tarot triggers once those modules have structured output.

**Starter cross-science combos (Phase 1 seed — ~50 combos):**
| Theme | Astrology Trigger | Numerology Trigger | Count |
|---|---|---|---|
| Leadership | Sun in 10th, Leo Lagna | LP 1, 8 | 5 |
| Wealth | Dhana Yoga, 2nd/11th lords | LP 8, Expression 22 | 8 |
| Spiritual | Ketu in 12th, Jupiter in 9th | LP 7, 11 | 5 |
| Creative | Venus in 5th, Moon in 2nd | LP 3, Expression 6 | 5 |
| Health Caution | Saturn in 6th/8th, Mars afflicted | LP 4 (overwork) | 5 |
| Relationships | Venus strong, 7th lord well-placed | LP 2, 6 | 8 |
| Travel/Foreign | 12th house strong, Rahu in 9th | LP 5, 9 | 5 |
| Education | Mercury in 4th/5th, Jupiter aspects | LP 7, Expression 11 | 5 |
| Late Bloomer | Saturn in Lagna, Kemadruma cancelled | LP 4, 8 | 4 |
| **Total** | | | **~50** |

### 2g. Rule Indexing Strategy

MongoDB indexes for fast lookup:
```javascript
db.interpretation_rules.createIndex({ "condition.type": 1, "condition.planet": 1, "condition.house": 1 })
db.interpretation_rules.createIndex({ "categories": 1 })
db.interpretation_rules.createIndex({ "tags": 1 })
db.interpretation_rules.createIndex({ "active": 1, "priority": -1 })
```

### 2h. Redis Cache Layer (Phase 2)

For production scale (>1000 concurrent users), add Redis caching:
- Cache key: `rules:{condition_type}:{planet}:{house}` → TTL 24h
- Invalidate on rule update via admin
- Phase 1: Direct MongoDB queries (sufficient for current scale)
- Phase 2: Redis via `aioredis` when user base exceeds 1000 DAU

---

## 3. Rule Engine — Python Backend

### 3a. New file: `backend/narrative_engine.py`

```python
class NarrativeEngine:
    """
    Core engine that matches chart data against the interpretation rule database,
    scores and ranks matches, resolves conflicts, then hands off to LLM for narrative.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.rules_collection = db["interpretation_rules"]

    async def scan_chart(
        self,
        chart: dict,
        categories: list[str] | None = None,
        max_rules: int = 50
    ) -> list[dict]:
        """
        Scan a computed chart against all active rules.

        1. Extract all chartable facts (planet positions, house lords, aspects, yogas)
        2. Build query conditions from facts
        3. Query MongoDB for matching rules
        4. Apply modifiers (amplify/diminish based on aspects, retrogrades, etc.)
        5. Score each match: base_weight × modifier_factor × priority
        6. Resolve conflicts (e.g., Jupiter in 7H vs Saturn in 7H — both valid, flag tension)
        7. Sort by score descending
        8. Return top max_rules matches

        Args:
            chart: Output from calculate_vedic_chart() or KP engine
            categories: Filter to specific report type ["career"] or None for all
            max_rules: Cap on returned rules (prevents bloated LLM prompts)

        Returns: list of matched rules with computed scores and applied modifiers
        """

    async def resolve_conflicts(self, matched_rules: list[dict]) -> list[dict]:
        """
        When two rules contradict (e.g., one says 'early marriage', another says 'delayed'),
        don't discard — flag as 'tension' and let the LLM weave both perspectives.

        Conflict resolution strategy:
        1. If both from same source & same priority → keep higher-scored
        2. If from different sources → keep both, tag as "multi-perspective"
        3. If one has a modifier that cancels the other → apply modifier, adjust scores
        """

    async def generate_narrative(
        self,
        matched_rules: list[dict],
        chart: dict,
        report_type: str,
        language: str = "en",
        voice_blend: str = "classical+modern_analytical"
    ) -> str:
        """
        The "Scholar-Storyteller" engine — pass matched rules + full_text_passages
        + chart context to Claude for narrative-first generation.

        NARRATIVE-FIRST approach (not bullet-point summaries):
        1. Gather full_text_passages (500+ words each) from matched rules
        2. Load author voice instructions from `author_voices` collection
        3. Load appropriate narrative bridges from `narrative_bridges` collection
        4. Build a rich context block for the LLM with:
           - Full book excerpts (the "meat" — reduces hallucination)
           - Author voice blending instructions
           - Bridging phrase templates for transitions
           - Conflict flags tagged as "competing energies"
        5. Claude synthesizes into a cohesive multi-paragraph narrative
           (NOT bullet points — full prose, first-person reading style)

        The LLM receives:
        - Full-text book passages (verbatim classical + modern excerpts)
        - Author voice tone instructions for blending
        - Narrative bridge templates for transitions between themes
        - Chart context (birth details, current dasha, key positions)
        - Report type for tone/focus guidance
        - Conflict flags for nuanced "competing energies" handling

        Returns: Markdown-formatted narrative (500-3000 words depending on report type)
        """

    async def scan_cross_science(
        self,
        astro_chart: dict | None = None,
        numerology_data: dict | None = None,
        palmistry_data: dict | None = None,
        tarot_data: dict | None = None,
        categories: list[str] | None = None
    ) -> list[dict]:
        """
        Multi-Factor Confirmation engine — scans `cross_science_combinations`
        collection to find themes confirmed by 2+ sciences.

        Scoring: weighted sum of matched sciences
        (astrology 40%, palmistry 25%, numerology 20%, tarot 15%)

        Returns matched combos sorted by intensity score.
        """
```

### 3b. Chart Fact Extractor

```python
def extract_chart_facts(chart: dict) -> list[dict]:
    """
    Convert a computed Vedic chart into a flat list of 'facts' that can be
    matched against rule conditions.

    Example output:
    [
        { "type": "planet_in_house", "planet": "Saturn", "house": 7, "sign": "Libra",
          "dignity": "exalted", "retrograde": false, "nakshatra": "Swati" },
        { "type": "planet_aspect", "planet": "Jupiter", "aspecting_house": 7 },
        { "type": "house_lord_in_house", "source_house": 7, "lord": "Venus",
          "target_house": 12, "target_sign": "Virgo" },
        { "type": "yoga", "yoga_name": "Gajakesari", "planets": ["Jupiter", "Moon"],
          "houses": [1, 7] },
        { "type": "planet_conjunction", "planets": ["Sun", "Mercury"], "house": 9 },
        ...
    ]
    """
```

### 3c. Yoga Detection Library

```python
YOGA_DEFINITIONS = [
    {
        "name": "Gajakesari Yoga",
        "description": "Jupiter in kendra from Moon",
        "condition": lambda chart: jupiter_in_kendra_from_moon(chart),
        "effect": "Wisdom, fame, prosperity, good reputation",
        "category": ["general", "career", "wealth"]
    },
    {
        "name": "Budhaditya Yoga",
        "description": "Sun + Mercury conjunction",
        "condition": lambda chart: sun_mercury_same_house(chart),
        "effect": "Intelligence, communication skill, scholarly nature",
        "category": ["education", "career"]
    },
    {
        "name": "Chandra Mangal Yoga",
        "description": "Moon + Mars conjunction or mutual aspect",
        "condition": lambda chart: moon_mars_conjunction_or_aspect(chart),
        "effect": "Wealth through enterprise, courage, real estate gains",
        "category": ["wealth", "career"]
    },
    {
        "name": "Viparita Raja Yoga",
        "description": "Lords of 6, 8, 12 in each other's houses",
        "condition": lambda chart: viparita_raja_check(chart),
        "effect": "Success through adversity, gains from hidden sources",
        "category": ["wealth", "career", "general"]
    },
    {
        "name": "Kemadruma Yoga",
        "description": "Moon with no planets in 2nd or 12th from it",
        "condition": lambda chart: kemadruma_check(chart),
        "effect": "Emotional isolation, financial struggles (cancelled if aspects present)",
        "category": ["mental_health", "wealth"]
    },
    # ... expand to 30-50 classical yogas
]

def detect_yogas(chart: dict) -> list[dict]:
    """Run all yoga checks against chart, return list of active yogas with details."""
```

### 3d. New router: `backend/narrative_router.py`

Register at prefix `/api/narrative` in `server.py`.

#### Endpoint 1 — Generate Interpretation
```
POST /api/narrative/interpret
Auth: Required
```
Request:
```json
{
  "chart_data": { /* output of calculate_vedic_chart() */ },
  "report_type": "career" | "health" | "marriage" | "general" | "yearly",
  "categories": ["career", "wealth"],
  "language": "en",
  "depth": "summary" | "detailed" | "comprehensive"
}
```
Response:
```json
{
  "narrative": "/* Claude-generated markdown */",
  "matched_rules_count": 23,
  "top_influences": [
    { "rule_id": "R-SAT-7H-001", "summary": "Saturn in 7th — delayed but stable marriage", "score": 0.92 }
  ],
  "yogas_detected": ["Gajakesari Yoga", "Budhaditya Yoga"],
  "conflicts_flagged": 2,
  "meta": { "rules_scanned": 847, "time_ms": 320, "llm_time_ms": 4200 }
}
```

#### Endpoint 2 — Rule CRUD (Admin only)
```
GET    /api/narrative/rules?category=career&page=1&limit=20
POST   /api/narrative/rules           — create rule
PUT    /api/narrative/rules/:rule_id  — update rule
DELETE /api/narrative/rules/:rule_id  — soft-delete (set active=false)
```

#### Endpoint 3 — Bulk Import Rules
```
POST /api/narrative/rules/import
Auth: Admin
Content-Type: application/json
Body: { "rules": [ /* array of rule documents */ ], "source": "BPHS Chapter 24" }
```
For importing extracted rules from OCR'd books.

#### Endpoint 4 — Rule Statistics
```
GET /api/narrative/rules/stats
Auth: Admin
```
Returns: total rules, rules by category, rules by source, coverage map (which condition types have rules).

---

## 4. Admin Console — Rule Management UI

### 4a. New tab in Admin Console: "Knowledge Engine"

**Sub-tabs:**

**4a-i. Rules Browser**
- Filterable table: category, source, condition type, planet, house
- Search by keyword in interpretation text
- Inline edit for quick corrections
- Active/Inactive toggle
- Priority slider (1-10)

**4a-ii. Rule Editor**
- Full form for creating/editing a rule
- Condition builder: dropdown selects for type → planet → house → modifiers
- Interpretation editor: summary (short), detailed (long), positive/negative aspects, remedies
- Source attribution fields (primary text, chapter, secondary sources)
- Modifier builder: add conditional modifiers with effect type
- Preview: "If chart has [condition], the engine would say: [interpretation]"
- Conflict checker: highlights rules that may contradict

**4a-iii. Bulk Import**
- Upload JSON file of rules (from OCR extraction pipeline)
- Validation preview: shows valid/invalid rules before committing
- Source tagging: apply source metadata to all imported rules
- Duplicate detection: flag rules with >80% condition overlap

**4a-iv. Coverage Dashboard**
- Heatmap: 12 houses × 9 planets — cells colored by rule count
- Gap analysis: "No rules for Mercury in 8th house (career category)"
- Category breakdown: pie chart of rules per category
- Source breakdown: bar chart showing contribution per text

**4a-v. Test Console**
- Input birth details → run engine → see matched rules + narrative
- Side-by-side: raw rules vs generated narrative
- Useful for QA and tuning

---

## 5. Book Ingestion Pipeline (Phase 2 — OCR → Rules)

### Architecture for scaling to hundreds of books:

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  OCR'd Book  │───→│  Claude API  │───→│  Structured  │───→│  Admin       │
│  (PDF/text)  │    │  Extraction  │    │  Rules JSON  │    │  Review +    │
│              │    │  Prompt      │    │              │    │  Import      │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

#### Extraction Prompt (for Claude API):
```python
BOOK_EXTRACTION_PROMPT = """
You are extracting structured astrological rules from a classical Vedic text.

For each interpretive statement in the text, extract:
1. The condition (planet, house, sign, aspect, conjunction, yoga)
2. The interpretation (summary + detailed)
3. Positive and challenging aspects
4. Any remedies mentioned
5. The source location (chapter, verse/shloka number)

Output as JSON array matching this schema: [rule_schema]

RULES:
- One condition per rule (compound conditions → composite type with sub_conditions)
- Keep interpretations faithful to the source text — do not modernise or editorialise
- Tag categories: general, career, wealth, relationships, marriage, health, education, spirituality
- If the text gives contradictory interpretations for different contexts, create separate rules
- Preserve Sanskrit terms in parentheses alongside English translations
"""
```

#### Phase 2 Endpoints:
```
POST /api/narrative/extract
Auth: Admin
Body: { "text": "/* OCR content */", "source_name": "BPHS", "chapter": "24" }
Response: { "extracted_rules": [...], "confidence_scores": [...], "needs_review": [...] }
```

This is **not in Phase 1 scope** — Phase 1 uses manually curated rules + JSON import.
Documented here so the data model supports it from day one.

---

## 6. Seed Data — Starter Rule Pack

Phase 1 ships with a curated seed pack of **~300+ rules** plus **~50 cross-science combos**
plus **5 author voices** and **~30 narrative bridges**.

### 6a. Interpretation Rules (~300)

| Category | Rule Count | Source |
|---|---|---|
| Planets in Houses (9 × 12) | 108 | BPHS, Phaladeepika, B.V. Raman |
| Major Yogas (top 30) | 30 | BPHS, Saravali |
| House Lords in Houses (key combos) | 36 | BPHS |
| Retrograde effects (9 planets) | 9 | Saravali, Uttara Kalamrita |
| Dignity effects (exalted/debilitated × 9) | 18 | BPHS |
| Nakshatra-based (Moon in 27 nakshatras) | 27 | Brihat Samhita |
| Planetary Aspects / Drishti rules | 18 | BPHS (see reference rules below) |
| Combustion effects (7 planets) | 7 | BPHS, Saravali |
| Functional benefic/malefic per Lagna (12 × key) | 24 | BPHS |
| Life Area mappings (Career/Wealth/Health/Relationships/Spirituality) | 25 | Mixed |
| **Total seed rules** | **~302** | |

### 6b. Vedic Reference Rules (baked into seed data)

The following foundational rules from the Codex prompt reference MUST be codified
as seed data entries. These are the "backbone rules" that apply to every chart:

**Planetary Aspects (Drishti):**
- Sun, Moon, Mercury, Venus: Aspect the 7th house only
- Mars: Aspects the 4th, 7th, and 8th houses
- Jupiter: Aspects the 5th, 7th, and 9th houses
- Saturn: Aspects the 3rd, 7th, and 10th houses
- Rahu and Ketu: Aspect the 5th and 9th houses

**Exaltation / Debilitation Table:**
| Planet | Exalted | Debilitated |
|---|---|---|
| Sun | Aries | Libra |
| Moon | Taurus | Scorpio |
| Mars | Capricorn | Cancer |
| Mercury | Virgo | Pisces |
| Jupiter | Cancer | Capricorn |
| Venus | Pisces | Virgo |
| Saturn | Libra | Aries |

**Moolatrikona Signs:**
Sun → Leo, Moon → Taurus, Mars → Aries, Mercury → Virgo,
Jupiter → Sagittarius, Venus → Libra, Saturn → Aquarius

**Planetary Friendships (for dignity calculation):**
- Sun: Friends — Moon, Mars, Jupiter | Enemies — Venus, Saturn
- Moon: Friends — Sun, Mercury
- Mars: Friends — Sun, Moon, Jupiter | Enemy — Mercury
- Mercury: Friends — Sun, Venus | Enemy — Moon
- Jupiter: Friends — Sun, Moon, Mars | Enemies — Mercury, Venus
- Venus: Friends — Mercury, Saturn | Enemies — Sun, Moon
- Saturn: Friends — Mercury, Venus | Enemies — Sun, Moon, Mars

**Life Area → House Mapping (for category filtering):**
- Career: 10th (primary), 6th and 2nd (supporting). Planets: Saturn, Sun, Mercury, Mars
- Relationships: 7th (core), 2nd, 5th, 11th. Men: Venus. Women: Mars/Jupiter
- Wealth: 2nd, 9th, 11th. Planets: Jupiter, Venus, Saturn
- Health: 1st, 6th, 8th. Planets: Mars, Moon, Saturn, Rahu/Ketu
- Spirituality: 8th, 9th, 12th. Planets: Jupiter, Ketu, Moon

**Deity & Remedy Mapping (for remedial guidance):**
| Planet | Deity | Color | Direction |
|---|---|---|---|
| Sun | Lord Surya | Red/Orange/Golden | East |
| Moon | Parvati / Shiva | White/Silver | NW |
| Mars | Hanuman / Murugan | Red/Pink/Coral | South |
| Mercury | Vishnu | Green/Olive | North |
| Jupiter | Brihaspati / Shiva | Yellow/Gold | NE |
| Venus | Lakshmi | White/Pastels | SE |
| Saturn | Shani / Hanuman | Dark Blue/Black | West |
| Rahu | Durga / Saraswati | — | — |
| Ketu | Ganesha | — | — |

### 6c. Cross-Science Combinations (~50)

See Section 2f for schema. Starter pack covers 9 themes × ~5 combos each,
linking Astrology triggers + Numerology triggers. Stored as
`backend/data/seed_cross_science.json`.

### 6d. Author Voices (5) + Narrative Bridges (~30)

- 5 voice profiles: `classical`, `modern_analytical`, `kp_technical`, `spiritual`, `popular`
- ~30 bridge phrases across 6 types: contrast, reinforcement, transition, deepening, temporal, cross_science
- Stored as `backend/data/seed_voices.json` and `backend/data/seed_bridges.json`

All seed data imported via bulk import endpoint on first deployment.

---

## 7. Integration Points — How Other Modules Use the Engine

Once deployed, the Narrative Engine becomes the **interpretation backbone** for:

| Module | How It Uses the Engine |
|---|---|
| **Kundali Report** | `scan_chart(chart, categories=["general"])` → full birth chart interpretation |
| **Longevity Report** | `scan_chart(chart, categories=["health"])` → health narrative sections |
| **Daily Horoscope** | `scan_chart(transit_chart, categories=["general"], depth="summary")` → daily paragraph |
| **Tarot** | Phase 1: cross-science combos match tarot cards to astro themes |
| **Numerology** | Phase 1: `scan_cross_science(astro_chart, numerology_data)` → unified reading |
| **Palmistry** | Phase 2: add palmistry triggers to cross-science combos |
| **Kundali Milan** | `scan_chart(composite, categories=["relationships", "marriage"])` |

**Integration pattern — single science:**
```python
from narrative_engine import NarrativeEngine

engine = NarrativeEngine(db)
rules = await engine.scan_chart(chart_data, categories=["career"], max_rules=30)
narrative = await engine.generate_narrative(
    rules, chart_data, report_type="career",
    voice_blend="classical+modern_analytical"
)
```

**Integration pattern — cross-science confirmation:**
```python
# When user has both birth chart AND numerology data:
combos = await engine.scan_cross_science(
    astro_chart=chart_data,
    numerology_data={"life_path": 1, "expression": 8},
    categories=["career"]
)
# combos enriches the narrative with "multi-science confirmation" insights
```

---

## 8. Technical Constraints

- MongoDB (Motor async) — already in stack, no new DB
- No Redis in Phase 1 — direct MongoDB queries (indexed) are sufficient
- Claude API: use `claude-sonnet-4-6` for narrative generation (cost:quality balance)
- No Celery/worker in Phase 1 — use FastAPI `BackgroundTasks` for deep reports
- Rule evaluation must complete in < 500ms for up to 1000 rules
- LLM narrative generation: < 8s for detailed, < 3s for summary
- Admin rule management: standard CRUD, no real-time collaboration
- All rules stored in English; multilingual narratives handled at LLM layer (prompt includes language param)

---

## 9. Acceptance Criteria

- [ ] Rule schema validates — all 13 condition types can be stored and queried
- [ ] `full_text_passages` stored and retrieved correctly (500+ words per passage)
- [ ] `author_voices` collection seeded with 5 voice profiles
- [ ] `narrative_bridges` collection seeded with ~30 bridge phrases (6 types)
- [ ] `scan_chart()` correctly matches rules for a test chart (Saturn in 7H should match R-SAT-7H-001)
- [ ] Modifier application works — Jupiter aspecting Saturn in 7H amplifies positive score
- [ ] Conflict detection flags contradictory rules as "competing energies"
- [ ] Category filtering returns only relevant rules (career query skips health rules)
- [ ] Bulk import of 300+ seed rules completes in < 15s
- [ ] Cross-science combos: `scan_cross_science(astro, numerology)` finds matching themes
- [ ] Cross-science scoring: 2-science match scores lower than 3-science match
- [ ] Admin Rules Browser loads with pagination, search, and filters
- [ ] Admin Rule Editor creates and saves a new rule correctly (including full_text_passages)
- [ ] Coverage Dashboard shows accurate heatmap
- [ ] Test Console generates narrative for a sample chart
- [ ] `generate_narrative()` produces coherent, multi-paragraph PROSE (not bullets) in < 8s
- [ ] Narrative uses book excerpts as grounding — no hallucinated astrological claims
- [ ] Narrative transitions between multi-source text blocks feel seamless (bridge phrases)
- [ ] Integration: Kundali report page can call engine and display enriched narrative
- [ ] MongoDB indexes are created and queries use them (explain plan check)

---

## 10. Phase 1 vs Phase 2 Boundary

| Feature | Phase 1 (this commission) | Phase 2 (future) |
|---|---|---|
| Rule database + CRUD | ✅ | |
| Full-text book passages (narrative-first) | ✅ | |
| Author voices collection (5 voices) | ✅ | |
| Narrative bridges collection (30 phrases) | ✅ | |
| Rule engine (scan, score, rank) | ✅ | |
| LLM narrative generation (prose, not bullets) | ✅ | |
| Cross-science combos (astro + numerology) | ✅ | |
| Admin: Rules Browser + Editor | ✅ | |
| Admin: Bulk Import (JSON) | ✅ | |
| Admin: Coverage Dashboard | ✅ | |
| Admin: Test Console | ✅ | |
| Seed pack (~300 rules + 50 combos) | ✅ | |
| Integration with Kundali | ✅ | |
| Integration with Longevity | ✅ (if Commission H deployed) | |
| Cross-science: palmistry + tarot triggers | | ✅ |
| OCR → Rule extraction pipeline | | ✅ |
| Redis caching layer | | ✅ |
| Celery background workers | | ✅ |
| Multilingual rule content | | ✅ |
| Body silhouette SVG (health) | | ✅ |
| Rule versioning + diff tracking | | ✅ |
| A/B testing of interpretations | | ✅ |
| Vector DB (semantic search for passages) | | ✅ |

---

## 11. Estimated Effort

| Component | Hours |
|---|---|
| `narrative_engine.py` — core engine (scan, score, resolve, generate) | 12h |
| Cross-science combination engine (`scan_cross_science`) | 6h |
| Chart fact extractor + yoga detection library (30-50 yogas) | 8h |
| Rule schema + author voices + narrative bridges + MongoDB indexes | 6h |
| Seed data: 300+ rules + 50 cross-science combos + voices + bridges JSON | 10h |
| `narrative_router.py` — API endpoints (interpret, CRUD, import, stats) | 6h |
| Claude prompt engineering (narrative-first, voice blending, bridge stitching) | 6h |
| Admin Console: Rules Browser + Editor + Bulk Import | 10h |
| Admin Console: Coverage Dashboard + Test Console | 6h |
| Integration with Kundali report page | 3h |
| Testing + validation (including cross-science matching) | 7h |
| **Total** | **~80h** |
