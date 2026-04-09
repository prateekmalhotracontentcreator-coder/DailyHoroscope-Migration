# Draft Contract — Commission I: Jyotish Knowledge Engine
> Status: **DRAFT FOR CODEX INPUT — NOT A BUILD ORDER**
> Client: EverydayHoroscope (SkyHound Studios)
> Date: 10 April 2026
> Companion Brief: `.claude/CODEX_COMMISSION_I_BRIEF.md` — read this first
> Amendment Template: `.claude/CODEX_LIBRARY_AMENDMENT_TEMPLATE.md`

---

> **How to read this document:**
> Sections marked `[PROPOSED]` are our current thinking — we are asking for your recommendation before we lock them in.
> Sections marked `[CONFIRMED]` are already decided — please design around them.
> Sections marked `[INPUT REQUESTED]` have specific questions we want answered.
> Please annotate your response with which section you are addressing.

---

## 1. Module Overview [CONFIRMED]

Build an **internal Knowledge Engine** — infrastructure that powers every interpretation module on the platform. This is not a user-facing page.

### What It Does
Takes a computed Vedic birth chart → matches it against a curated rule library extracted from classical and modern Jyotish texts → passes matched rules + full book passages to Claude → returns a coherent, book-grounded narrative.

### Why This Approach
Current modules generate interpretations via direct LLM prompting. This produces generic output. The Knowledge Engine grounds the LLM in actual classical text — reducing hallucination, increasing depth, and enabling multi-authorial voice blending.

### Architecture: 3-Layer Stack [CONFIRMED conceptually — details open for input]

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: NARRATIVE LAYER (Claude API)                      │
│  Receives matched rules + full text passages + chart context │
│  → generates coherent multi-paragraph prose narrative        │
│  → never bullet points — full reading style at all times    │
└────────────────────────┬────────────────────────────────────┘
                         │ matched rules + passages
┌────────────────────────┴────────────────────────────────────┐
│  Layer 2: RULE ENGINE (Python / FastAPI)                    │
│  Evaluates chart against rule conditions                     │
│  Scores relevance, resolves source conflicts                 │
│  Filters by category: career / health / relationships etc.   │
└────────────────────────┬────────────────────────────────────┘
                         │ chart positions + dashas + transits
┌────────────────────────┴────────────────────────────────────┐
│  Layer 1: DATA LAYER (MongoDB)                              │
│  Hierarchical Interpretation Database                        │
│  Structured rules from classical + modern texts              │
│  If-Then conditions, multi-source attribution, full passages  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. The Workflow [CONFIRMED]

```
Temple Team Workstation      Codex (local execution)        MongoDB (Live DB)
OCR books stored here   →  Amendment Contract issued   →  extraction script runs
                                                                  ↓
                                                      interpretation_rules populated
                                                                  ↓
                                              Library Console (review + approve rules)
```

- No book content ever touches the production server
- Library Console has **no file upload feature** — it manages rules already in the database
- Phase 1: Codex builds the full schema and populates from the seed book list below
- Phase 2+: Each new book is a discrete Amendment Contract

---

## 3. Phase 1 — Book List [CONFIRMED]

### Tier 1 — Core (Phase 1 mandatory)

| # | Title | Category | Format |
|---|---|---|---|
| 1 | A Text Book of Astrology | Foundational Astrology, Panchang, Charts | Index + Chapter-wise PDF |
| 2 | Lal Kitab | Astrology — Rules and Remedies | Index + Chapter-wise PDF |
| 3 | Longevity and Astro System | Longevity — Basic Concepts, Rule-Based, 30+ Case Studies | Index + Chapter-wise PDF |

### Tier 2 — Core-Optional (Phase 1 if effort permits)

| # | Title | Category | Format |
|---|---|---|---|
| 4 | Ascendants and Astrological Tables | Astronomical Data, Muhurat Tables, Festival Rules | Index + Chapter-wise PDF |

### Tier 3 — Module Specific (Phase 1)

| # | Title | Category | Format |
|---|---|---|---|
| 5 | Your Destiny Is In Your Name & DOB | Numerology | Index + Chapter-wise PDF |
| 6 | Vedic Numerology — Ank Jyotish | Numerology | Index + Chapter-wise PDF |
| 7 | Crystal Healing | Remedies / Healing | Crystal knowledge, situational areas |

### Tier 4 — Additional (Phase 2 via Amendment Contracts)

| # | Title | Category | Format |
|---|---|---|---|
| 8 | A Book of 300 Important Horoscopes Vol. I | Astrology — Star Lord System, Sign Lords, Case Studies | Chapter guide + case studies |
| 9 | Longevity and Un-Natural Deaths | Longevity — Nakshatra System, Fundamental Rules | Chapter-wise PDF + case studies |

> **Note on classical texts:** BPHS, Phaladeepika, Saravali, B.V. Raman (How to Judge a Horoscope) are to be used as supplementary cross-reference sources during Phase 1 extraction, where Codex spots overlapping rules. They will be formally ingested as Amendment Contracts in Phase 2.

---

## 4. Data Layer — Proposed MongoDB Schema [PROPOSED — input requested]

> **[INPUT REQUESTED — Section 4]**
> We are proposing 4 collections. Before we lock this schema, please advise:
> - Is this the right collection structure? Would you merge or split any collections?
> - How would you handle rule versioning across Amendment Contracts?
> - What would your compound indexing strategy look like for < 500ms evaluation at 1,000+ rules?
> - Is there anything in the rule document schema that is missing or over-engineered?

### 4a. Collection: `interpretation_rules`

The primary library. Each document = one interpretation rule from one source.

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
    "summary": "Saturn in the 7th house indicates delayed marriage, a serious partner, and a relationship built on duty.",
    "detailed": "500–1000 word interpretation ...",
    "full_text_passages": [
      {
        "text": "The native whose 7th house is occupied by Shani shall find marriage delayed...",
        "source": "A Text Book of Astrology",
        "chapter": "Chapter X",
        "word_count": 280,
        "voice_tone": "classical"
      }
    ],
    "positive_aspects": ["Lasting and stable marriage once established"],
    "challenging_aspects": ["Delay in finding a suitable partner"],
    "remedies": ["Worship Lord Shani on Saturdays"]
  },

  "categories": ["relationships", "marriage"],
  "priority": 8,
  "intensity_score": 8.5,

  "source": {
    "primary": "A Text Book of Astrology",
    "chapter": "Chapter X — Planets in Houses",
    "author_voice": "classical",
    "secondary_sources": [
      { "text": "Lal Kitab", "chapter": "Chapter Y", "voice_tone": "classical" }
    ],
    "batch_id": "PHASE1-CORE-001"
  },

  "modifiers": [
    {
      "condition": { "aspected_by": "Jupiter" },
      "effect": "amplify_positive",
      "note": "Jupiter's aspect on Saturn in 7H improves marital harmony."
    },
    {
      "condition": { "conjunct_with": "Rahu" },
      "effect": "amplify_negative",
      "note": "Saturn-Rahu in 7H — unconventional marriage circumstances."
    },
    {
      "condition": { "retrograde": true },
      "effect": "intensify",
      "note": "Retrograde Saturn in 7H deepens karmic relationship lessons."
    }
  ],

  "conflicts_with": [],
  "weight": 0.85,
  "tags": ["saturn", "7th_house", "marriage", "delay", "karmic"],
  "active": true,
  "created_at": "ISO datetime",
  "updated_at": "ISO datetime"
}
```

### 4b. Condition Types Supported [PROPOSED]

| Type | Example | Key Fields |
|---|---|---|
| `planet_in_house` | Saturn in 7th | planet, house |
| `planet_in_sign` | Moon in Cancer | planet, sign |
| `planet_in_nakshatra` | Moon in Rohini | planet, nakshatra |
| `planet_aspect` | Jupiter aspects 7th | planet, aspecting_house |
| `planet_conjunction` | Sun + Mercury same house | planets[], house |
| `planet_dignity` | Jupiter exalted | planet, dignity |
| `planet_retrograde` | Saturn retrograde | planet, retrograde |
| `house_lord_in_house` | 7th lord in 12th | source_house, target_house |
| `yoga` | Gajakesari Yoga | yoga_name, planets[] |
| `dasha_period` | Saturn Maha Dasha active | dasha_lord, level |
| `transit` | Saturn transiting 8th from Moon | planet, transit_house |
| `kp_sublord` | Sub-lord of 8th cusp is Jupiter | cusp_num, sub_lord |
| `composite` | Saturn in 7H AND Jupiter aspects | sub_conditions[], operator |

### 4c. Collection: `author_voices`

```json
{
  "_id": "ObjectId",
  "voice_id": "classical",
  "display_name": "Classical Sanskrit Tradition",
  "tone_description": "Formal, verse-like, uses Sanskrit terminology with English in parentheses.",
  "example_authors": ["Parashara", "Varahamihira", "Lal Kitab tradition"],
  "llm_instruction": "Write in a reverent, scholarly tone. Use phrases like 'The ancient texts declare...' Include Sanskrit terms with English translations."
}
```

**Five voice profiles:**
| Voice ID | Style | Books |
|---|---|---|
| `classical` | Formal, shastra-based, Sanskrit terms | A Text Book of Astrology, Lal Kitab |
| `modern_analytical` | Clear, psychological, practical | B.V. Raman (Phase 2) |
| `kp_technical` | Precise, sub-lord focused, scientific | A Book of 300 Important Horoscopes |
| `spiritual` | Karmic, soul-purpose, philosophical | Crystal Healing, Longevity texts |
| `popular` | Conversational, accessible, encouraging | General reading style |

### 4d. Collection: `narrative_bridges`

Bridging phrases that help the LLM stitch multi-source text into a single flow.

```json
{
  "_id": "ObjectId",
  "bridge_type": "contrast",
  "context": "Two rules give opposing predictions",
  "phrases": [
    "While your chart indicates {positive_theme}, the planetary alignment introduces a counterbalancing energy of {negative_theme}...",
    "The texts present a creative tension here — {source_a} suggests {view_a}, while {source_b} adds {view_b}..."
  ]
}
```

**Bridge types:** `contrast` / `reinforcement` / `transition` / `deepening` / `temporal` / `cross_science`

### 4e. Collection: `cross_science_combinations`

Multi-factor confirmation engine — when 2+ sciences confirm the same life theme.

```json
{
  "_id": "ObjectId",
  "combo_id": "COMBO_0042",
  "title": "The Born Leader",
  "theme": "leadership",
  "triggers": {
    "astrology": { "conditions": ["Sun_in_10th", "Jupiter_aspects_10th"], "min_match": 1 },
    "numerology": { "conditions": ["life_path_1", "life_path_8"], "min_match": 1 }
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
  "categories": ["career", "leadership"],
  "active": true
}
```

**Phase 1 scope:** Astrology + Numerology matching only. Palmistry + Tarot triggers are schema-ready but unpopulated until Phase 2.

> **[INPUT REQUESTED — Section 4e]**
> Is a fixed-weight confidence model the right approach? We are open to an adaptive or Bayesian approach if you believe it would serve the use case better. How should partial confirmation (only 1 science matches) be surfaced in the narrative?

---

## 5. Proposed Indexes [PROPOSED — input requested]

> **[INPUT REQUESTED — Section 5]**
> We have proposed the indexes below. Is this sufficient for < 500ms query time across 1,000–10,000 rules? Would you add anything? Is there a case for an in-memory index built on server startup?

```javascript
// interpretation_rules
db.interpretation_rules.createIndex({ "condition.type": 1, "condition.planet": 1, "condition.house": 1 })
db.interpretation_rules.createIndex({ "categories": 1 })
db.interpretation_rules.createIndex({ "tags": 1 })
db.interpretation_rules.createIndex({ "active": 1, "priority": -1 })
db.interpretation_rules.createIndex({ "source.batch_id": 1 })

// cross_science_combinations
db.cross_science_combinations.createIndex({ "theme": 1 })
db.cross_science_combinations.createIndex({ "categories": 1, "active": 1 })
```

---

## 6. Rule Engine — Backend [PROPOSED — input requested]

### File: `backend/knowledge_engine.py`

> **[INPUT REQUESTED — Section 6]**
> Please review the class API below. Key questions:
> - Is `scan_chart` / `generate_narrative` / `scan_cross_science` the right surface area?
> - How would you structure conflict resolution between rules from different books?
> - What is your recommended approach to prevent Claude from ignoring the provided passages and generating from training data instead?
> - Should bridge phrases be passed as part of the prompt, or as structural anchors?

```python
class KnowledgeEngine:
    """
    Core engine: matches chart data against rule library,
    scores matches, resolves conflicts, generates Claude narrative.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def scan_chart(
        self,
        chart: dict,
        categories: list[str] | None = None,
        max_rules: int = 50
    ) -> list[dict]:
        """
        Scan a computed chart against all active rules.
        1. Extract chart facts (positions, lords, aspects, yogas)
        2. Build MongoDB query conditions from facts
        3. Apply modifiers (amplify/diminish per aspects, retrograde, etc.)
        4. Score: base_weight × modifier_factor × priority
        5. Resolve conflicts — flag tensions rather than discard
        6. Return top max_rules matches sorted by score

        Target: < 500ms for 1,000 active rules
        """

    async def resolve_conflicts(self, matched_rules: list[dict]) -> list[dict]:
        """
        Two rules contradict — don't discard. Flag as 'tension'.
        Strategy:
        - Same source + same priority → keep higher-scored
        - Different sources → keep both, tag 'multi_perspective'
        - Modifier cancels the other → apply modifier, adjust scores
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
        Scholar-Storyteller engine — full prose, never bullet points.
        1. Gather full_text_passages from matched rules
        2. Load voice instructions from author_voices collection
        3. Load bridge phrases from narrative_bridges collection
        4. Build context block for Claude:
           - Full verbatim book passages (grounds the LLM)
           - Voice blend instructions
           - Bridge phrase templates for transitions
           - Conflict flags as 'competing energies'
        5. Claude synthesises into 500–3000 word narrative

        Returns: Markdown-formatted narrative
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
        Multi-Factor Confirmation — finds themes confirmed by 2+ sciences.
        Phase 1: astrology + numerology only.
        Returns matched combos sorted by intensity score.
        """
```

### Chart Fact Extractor

```python
def extract_chart_facts(chart: dict) -> list[dict]:
    """
    Convert computed Vedic chart → flat list of matchable facts.
    Example output:
    [
      { "type": "planet_in_house", "planet": "Saturn", "house": 7,
        "sign": "Libra", "dignity": "exalted", "retrograde": false, "nakshatra": "Swati" },
      { "type": "planet_aspect", "planet": "Jupiter", "aspecting_house": 7 },
      { "type": "house_lord_in_house", "source_house": 7, "lord": "Venus", "target_house": 12 },
      { "type": "yoga", "yoga_name": "Gajakesari", "planets": ["Jupiter", "Moon"] },
      { "type": "planet_conjunction", "planets": ["Sun", "Mercury"], "house": 9 }
    ]
    """
```

---

## 7. API Endpoints [PROPOSED]

> **[INPUT REQUESTED — Section 7]**
> Is this the right API surface for the Library Console + module integrations?
> Any endpoints missing? Any that are over-engineered for Phase 1?

### File: `backend/knowledge_router.py`
All routes under `/api/knowledge`.

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/interpret` | Full scan + narrative for a chart |
| `GET` | `/rules` | List rules (paginated, filterable) |
| `POST` | `/rules` | Create single rule |
| `PUT` | `/rules/{rule_id}` | Update rule |
| `DELETE` | `/rules/{rule_id}` | Soft-delete (sets active: false) |
| `POST` | `/rules/import` | Bulk import from Amendment Contract JSON |
| `GET` | `/rules/stats` | Coverage stats (by category, source, condition type) |
| `GET` | `/voices` | List author voice profiles |
| `GET` | `/bridges` | List narrative bridge phrases |
| `POST` | `/test` | Test Console — chart → matched rules + narrative preview |

---

## 8. Local Extraction Script [PROPOSED — input requested]

### File: `backend/scripts/extract_book.py`
Local-only. Never deployed to Render. Runs on Temple Team workstation.

> **[INPUT REQUESTED — Section 8]**
> This is the area where we most want your recommendation before specifying further.
>
> The OCR source files vary in quality (High/Medium as marked per book). The books include:
> - **A Text Book of Astrology** — systematic chapter structure, predictable If-Then rules
> - **Lal Kitab** — highly idiomatic, remedies-heavy, non-standard rule phrasing
> - **Longevity and Astro System** — case study format mixed with rule statements
> - **Numerology books** — formula-based with worked examples
> - **Crystal Healing** — descriptive/situational, not If-Then format
>
> Our current thinking: a hybrid approach — rule-template pattern matching for structured books (A Text Book of Astrology), LLM-assisted extraction for idiomatic/narrative books (Lal Kitab, Crystal Healing).
>
> **Questions:**
> 1. Do you agree with the hybrid approach, or would you recommend a different extraction strategy?
> 2. How should the script handle OCR noise — hyphenation across line breaks, column artefacts, multi-column PDF layouts?
> 3. What quality threshold would you apply before accepting an extracted passage (minimum word count, coherence check)?
> 4. Should the extraction script produce a human-readable review report alongside the JSON, so the Temple Team can spot-check before importing?

**Agreed interface (regardless of extraction approach):**

```python
# Input: path to OCR text file + extraction config
# Output: structured JSON in interpretation_rules schema + import report

python extract_book.py \
  --input "/Users/apple/Documents/Knowledge Engine_eBooks/1. A Text Book of Astrology/chapter_07.txt" \
  --book "A Text Book of Astrology" \
  --voice "classical" \
  --categories "relationships,career,wealth" \
  --output "backend/data/PHASE1-CORE-001_textbook_astrology_rules.json" \
  --report "backend/data/PHASE1-CORE-001_import_report.md"
```

---

## 9. Library Console [PROPOSED — scope open for input]

**Standalone page** — completely separate from the Operations Admin Console.
- Route: `/library`
- Role: `library_admin` (separate from `admin` — cannot access `/admin/dashboard`)
- File: `frontend/src/pages/LibraryConsolePage.jsx`

> **[INPUT REQUESTED — Section 9]**
> We have spec'd 5 tabs. Please advise which to include in Phase 1 and which to defer.
> Also advise whether `library_admin` should be a separate role or a permission on the existing `admin` role.

### Tab 1 — Rules Browser [Phase 1]
- Filterable table: category / source / condition type / active status
- Inline edit: active toggle, priority slider
- Row expand: full condition + passages preview
- Bulk actions: activate/deactivate, re-categorise

### Tab 2 — Rule Editor [Phase 1]
- Condition builder (type selector → dynamic fields per condition type)
- Full-text passage manager (add/edit/delete passages per rule)
- Modifier builder
- Live conflict checker (flag rules that conflict with existing DB)
- Save + preview

### Tab 3 — Library Import [Phase 1]
- Upload pre-extracted JSON from `extract_book.py` output
- Validation preview: schema check, duplicate detection, conflict flags
- Confirm import → batch tagged with Amendment Contract ID
- Import history log

### Tab 4 — Coverage Dashboard [Phase 1]
- 12×9 heatmap (12 houses × 9 planets — green = covered, yellow = sparse, red = gap)
- Category donut chart (career / health / relationships / wealth / spirituality)
- Source bar chart (rules per book)
- Cross-science coverage panel (Phase 1: astrology + numerology)
- Gap analysis: what is the least covered house/planet combination?

### Tab 5 — Test Console [Phase 1]
- Input: chart data (date/time/location or paste chart JSON)
- Output: matched rules list + narrative side-by-side
- Voice selector, depth selector (summary / detailed / full)
- Citation trail: which book passages contributed to which paragraph

---

## 10. Seed Data — Phase 1 Deliverables [CONFIRMED structure, book sources updated]

After extraction, Codex produces these files in `backend/data/`:

| File | Contents | Source Books |
|---|---|---|
| `seed_rules.json` | ~300+ foundational rules | A Text Book of Astrology, Lal Kitab, Longevity and Astro System |
| `seed_numerology_rules.json` | Numerology-specific rules | Your Destiny Is In Your Name & DOB, Vedic Numerology — Ank Jyotish |
| `seed_remedies_rules.json` | Remedy + healing rules | Crystal Healing, Lal Kitab (remedies chapters) |
| `seed_cross_science.json` | ~50 cross-science combos | Astrology + Numerology (Phase 1 only) |
| `seed_voices.json` | 5 author voice profiles | Derived from book style |
| `seed_bridges.json` | ~30 narrative bridge phrases | Authored by Codex |

**Schema requirement:** must support growth from ~300 rules (Phase 1) to 10,000+ rules (all future amendments) without any schema changes or code deployments. Sources, books, and traditions are all data — not code.

---

## 11. Integration Pattern — How Other Modules Call the Engine [CONFIRMED]

```python
from knowledge_engine import KnowledgeEngine

engine = KnowledgeEngine(db)

# Single science — Kundali report
rules = await engine.scan_chart(chart_data, categories=["career"], max_rules=30)
narrative = await engine.generate_narrative(
    rules, chart_data, report_type="career",
    voice_blend="classical+modern_analytical"
)

# Cross-science — astro + numerology unified reading
combos = await engine.scan_cross_science(
    astro_chart=chart_data,
    numerology_data={"life_path": 1, "expression": 8},
    categories=["career"]
)
```

---

## 12. Constraints [CONFIRMED]

| Constraint | Detail |
|---|---|
| Database | MongoDB (Motor async) — already in stack, no new DB |
| Cache | No Redis in Phase 1 — MongoDB indexes sufficient at current scale |
| AI model | `claude-sonnet-4-6` for narrative generation |
| Extraction script | Local only — never deployed to Render |
| Rule evaluation | < 500ms for up to 1,000 active rules |
| Narrative generation | < 8s detailed, < 3s summary |
| Role isolation | `library_admin` must not grant access to `/admin/dashboard` |
| Schema growth | Must support 10,000+ rules without schema changes |
| Book ingestion | No book content on production server — ever |

---

## 13. Acceptance Criteria [PROPOSED — open for Codex additions]

> **[INPUT REQUESTED — Section 13]**
> Are there any acceptance criteria you would add from a build quality / testability perspective?

- [ ] `scan_chart()` returns correct matches for a test chart with Saturn in 7H, Jupiter in 10H, Moon in Cancer
- [ ] `generate_narrative()` returns full prose with no bullet points and cites at least one book passage
- [ ] `scan_cross_science()` returns a matching combo when Life Path = 1 and Sun is in 10th
- [ ] Library Console Rules Browser loads 300 rules in < 2s
- [ ] Import endpoint correctly deduplicates rules with identical `rule_id`
- [ ] Test Console shows citation trail linking paragraph to source passage
- [ ] `library_admin` session cannot access any `/admin/*` route
- [ ] `admin` session cannot access `/library` route
- [ ] All 4 MongoDB collections have correct indexes applied at startup
- [ ] `extract_book.py` produces valid JSON that passes import endpoint schema validation
- [ ] Coverage Dashboard heatmap shows correct gap analysis for Phase 1 seed data
- [ ] Engine handles chart with no matched rules gracefully (returns fallback narrative)

---

## 14. What We Need From You Before We Finalise

1. **Answers to all `[INPUT REQUESTED]` sections above** (6 sections: 4, 4e, 5, 6, 7, 8, 9, 13)
2. **Any structural changes** you recommend to the schema, API, or workflow
3. **A revised effort estimate** — the original estimate was ~84h; does that hold after reviewing the actual Phase 1 book list and workflow?
4. **Questions you need answered** before you can start — fire them back to us
5. **Your recommended build sequence** — what do you build first to de-risk Phase 1?

---

> Stack: FastAPI (Render, Docker python:3.12.9-slim) + React 18 (Vercel) + MongoDB (Motor async) + pyswisseph 2.10.x + Claude API (`claude-sonnet-4-6`)
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Main branch: `main` (deploy-on-push)
