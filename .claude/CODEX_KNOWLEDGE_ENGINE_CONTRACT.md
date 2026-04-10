# Draft Contract — Commission I: Jyotish Knowledge Engine
> Status: **ARCHITECTURE LOCKED — READY FOR BUILD CONTRACT**
> Client: EverydayHoroscope (SkyHound Studios)
> Date: 10 April 2026
> Companion Brief: `.claude/CODEX_COMMISSION_I_BRIEF.md` — read this first
> Amendment Template: `.claude/CODEX_LIBRARY_AMENDMENT_TEMPLATE.md`

---

> **How to read this document:**
> Sections marked `[LOCKED]` are Temple Team decisions — design to these exactly.
> Sections marked `[CONFIRMED]` are already decided — please design around them.
> Sections marked `[PROPOSED]` are still open — Codex may advise before build starts.
> All major architecture decisions (TD-01 through TD-22) are now locked. This document is ready for final build contract issuance.

---

## Temple Team Decision Log

### Round 1 — 10 April 2026 (Initial Locks)

| # | Topic | Decision |
|---|---|---|
| TD-01 | Cross-science scoring model | 3-layer model confirmed: fixed weights + qualitative tiers + α/β/γ contextual multipliers. Fixed weights are the mathematical backbone — do not remove. See Section 15. |
| TD-02 | AI Paraphrase pipeline | Codex leads paraphrase generation using the WIM. Claude reviews flagged passages only (MEDIUM 1-in-5, LOW every one). See Section 16 + `CODEX_PARAPHRASE_WIM.md`. |
| TD-03 | author_voices + narrative_bridges | These remain as MongoDB collections. Seeded JSON on first run, managed via Library Console thereafter. Not merged, not hardcoded. |
| TD-04 | Library Console scope | Full 5-tab spec confirmed. No reduction, no Phase 2 deferral. Separate `library_admin` role confirmed. See Section 9. |
| TD-05 | Excerpt policy (Policy Decision 1) | AI-generated equivalents only in MongoDB + Claude prompts. No verbatim text from any copyrighted source. Classical Sanskrit texts (BPHS etc.) — technical vocabulary and astrological logic may be expressed in original prose, not copied. See Section 16. |
| TD-06 | Citation policy (Policy Decision 2) | Citations are internal to Test Console only. End-user reports attribute to "classical Vedic tradition" generically. No user-facing book references in Phase 1. |
| TD-07 | Science Arbitration mechanism | Schema-ready in Phase 1. Mathematical framework pending Codex's response to `CODEX_SCIENCE_ARBITRATION_REQUEST.md`. See Section 17. |
| TD-08 | Schema simulation | Three simulations requested before locking schema decisions. See `CODEX_SCHEMA_SIMULATION_REQUEST.md`. |
| TD-09 | Revised effort estimate | 125–150h accepted for lean Phase 1 scope as defined here. |
| TD-10 | World Context Engine | Defined as Commission J — separate from Commission I. Commission I builds integration hooks. See Section 18. |

### Round 2 — 10 April 2026 (Locked following Codex simulation + science arbitration response)

**Schema Decisions (from simulation results)**

| # | Topic | Decision |
|---|---|---|
| TD-11 | Rule document structure | Embedded paraphrased passages confirmed for Phase 1. Add `passage_ref_id: null` to every rule document as a migration-ready field. Separate `source_passages` collection deferred to Phase 2. |
| TD-12 | Index refresh strategy | Strategy C (stale-read tolerant) confirmed for Phase 1. Import endpoint must return `{"imported": N, "index_refreshed": true/false}` separately — Library Console waits for `index_refreshed: true` before showing "batch live". |

**Science Arbitration Decisions (from arbitration response + Temple Team strategic input)**

| # | Topic | Decision |
|---|---|---|
| TD-13 | Backbone science selection | **Module-determined, not statically Vedic Astrology.** The module the user opens determines which science leads. Jyotish Report → Vedic Astrology backbone. Numerology Report → Numerology backbone. Palmistry Report → Palmistry backbone. KP Report → KP backbone. The backbone science is passed as `backbone_science_id` in every report context. Secondary sciences serve as supportive precision layers — not competitors. |
| TD-14 | Supersession table scope | The supersession table (category + claim_axis → lead science) governs **secondary science priority only**. The backbone science always leads its own report. The table arbitrates which secondary science gets the highest support weight. See Section 17. |
| TD-15 | New rule schema fields | The following fields are required on every `interpretation_rules` document: `claim_axis` (e.g. `marriage_timing`, `career_growth`), `claim_scope` (tendency / event_timing / window / trait), `claim_polarity` (positive / negative / mixed / neutral), `timing_bias` (early / on_time / late / cyclical / none), `strength_band` (low / medium / high / extreme), `subject_scope` (self / partner / household / family). Optional: `authority_override`, `mutually_exclusive_with`. |
| TD-16 | Contradiction detection | Two rules are contradiction candidates when `life_domain` matches and `claim_axis` matches. Orthogonal if `claim_scope` differs. Contradiction score C = 0.40×polarity_distance + 0.35×timing_distance + 0.15×strength_distance + 0.10×authority_overlap. Flag contradiction if C ≥ 0.55 and both claims have effective_confidence ≥ 0.18. |
| TD-17 | Arbitration framework | Production runtime: Supersession table (category + claim_axis → lead science) → confidence-delta tiebreaker → representation mode selection. MCDA scoring used internally to compute `effective_confidence` per claim. No Bayesian or D-S in Phase 1 runtime. |
| TD-18 | Tranche layer | **Phase 1 — full rule engine.** Between contradiction detection and narration: a **Tranche Filter** applies user circumstance If-Then rules before the narrative engine receives the evidence packet. Rules suppress false negatives based on context (e.g. `IF family_wealth_tier = HIGH AND claim_axis = financial_security THEN dampen negative financial indicators from secondary sciences`). Seeded domain rules built in Phase 1. Questionnaire data populates when the questionnaire commission (TD-25) ships. |
| TD-19 | Questionnaire-driven β + γ | Subscription member onboarding questionnaire feeds β (micro) and γ (family) multipliers. Key data points: salary bracket, family wealth tier, siblings count, current city, travel frequency, relationship status, parents' data. **Schema and Tranche hooks Phase 1 (Commission I). Questionnaire UI and flow is a separate Phase 1 commission (TD-25) — outside Commission I build hours.** |
| TD-20 | tension_block JSON | The evidence packet sent to the narrative engine uses the JSON structure defined in Section 17.3. Accepted as specified in Codex's arbitration response. |
| TD-21 | Representation mode thresholds | synthesis if C < 0.30 or same directional polarity and Δ ≥ 0.05. tension if C 0.30–0.75 and top effective_confidence ≥ 0.20. honest_uncertainty if C > 0.75 or all effective_confidences < 0.20. Max tension blocks per report: 20% of domain sections. Max honest_uncertainty: 5%. |
| TD-22 | Kota Chakra / Parents data hook | Schema-ready Phase 1: optional `parents_data` field on user profile (father DOB/place, mother DOB/place, self current city). Feeds enhanced Vedic accuracy layer for Subscription members. Full Kota Chakra integration is a separate commission — Phase 1 builds the data schema only. |

**Additional locks — Round 2**

| # | Topic | Decision |
|---|---|---|
| TD-23 | Arc Angel — 12 Areas of Life | Left Nav Panel persistent user profile snapshot across all 12 life domains (12 Bhavas). Shows Auspicious / Neutral / Inauspicious period per domain + Confidence % score. Activates on Premium membership + birth data entry. Confidence improves as user provides more data (questionnaire, additional module runs). Every module report must correlate its output back to the relevant Arc Angel dimension(s). Master validation layer — the cross-module truth anchor. See Section 19. |
| TD-24 | Case Study Validation Pipeline | 1,000+ published case studies of public figures (known birth data + known life outcomes) are available as Phase 1 validation data. ~50 cases from Numerology Phase 1 book; ~300 from the Longevity book; balance from additional sources. These are the Knowledge Engine's empirical acceptance test suite. Case studies must be structured, extracted, and run through the engine once built. Outcomes compared against known results. Threshold tuning (contradiction C-score, confidence tiers) validated against this data before Phase 2 launch. See Section 20. |
| TD-25 | Questionnaire Commission | Questionnaire UI and flow (onboarding + continuous dialogue for Subscription members) is a **separate Phase 1 commission** — outside Commission I build hours. Commission I builds the data schema and β/γ hooks. The questionnaire commission delivers the UI, flow, and β/γ population logic. These two commissions run in parallel or sequentially in Phase 1. |

**Phased implementations (spec Phase 1, runtime Phase 2)**

| # | Topic | Decision |
|---|---|---|
| TDF-P1 | Full Arbitration Runtime | Full MCDA + supersession + confidence-delta runtime: fully **spec'd and schema'd in Phase 1**. Phase 2 implementation after case study validation confirms thresholds. Phase 1 runtime uses simplified "backbone leads; secondary acknowledges; surface tension if C ≥ 0.55" logic. |
| TDF-P2 | MCDA Internal Scoring | Full MCDA spec locked Phase 1. Phase 2 implementation once case study data enables empirical calibration of criteria weights. Phase 1 uses weighted average as `effective_confidence` proxy. |

**Deferred to Phase 2 / Phase 3**

| # | Topic | Deferred decision |
|---|---|---|
| TDF-01 | source_passages collection | Migrate when editorial correction fan-out at 3,000 rules becomes operationally painful. Triggered by Phase 2 review. |
| TDF-02 | Double-buffer index refresh | Implement Strategy B if import frequency grows or stale-read window causes user-visible issues. |
| TDF-03 | Bayesian / Dempster-Shafer | Previously estimated Phase 3. **Re-evaluate at Phase 2** — 1,000+ case studies (TD-24) may provide the empirical priors needed to move this forward. |
| TDF-04 | Kota Chakra full integration | Parents birth data schema ready Phase 1 (TD-22). Full Kota Chakra calculation engine is a separate Phase 2 commission. |

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

### Tier 4 — Classical Foundation Texts (Phase 1 — Core Rule Seed)

These are the texts from which the original seed files were planned. **Phase 1 mandatory** — the foundational rule library upon which all other books build.

| # | Title | Author / Tradition | Category |
|---|---|---|---|
| 10 | Brihat Parashara Hora Shastra (BPHS) | Parashara | Foundational Vedic — all houses, planets, yogas |
| 11 | Phaladeepika | Mantreswara | Classical Vedic — planetary results, house lords |
| 12 | Saravali | Kalyana Varma | Classical Vedic — planetary combinations, results |
| 13 | How to Judge a Horoscope (Vol. 1 & 2) | B.V. Raman | Modern analytical — house-by-house interpretation |

### Tier 5 — Additional (Post-Phase 1 via Amendment Contracts)

| # | Title | Category | Format |
|---|---|---|---|
| 14 | A Book of 300 Important Horoscopes Vol. I | Astrology — Star Lord System, Sign Lords, Case Studies | Chapter guide + case studies |
| 15 | Longevity and Un-Natural Deaths | Longevity — Nakshatra System, Fundamental Rules | Chapter-wise PDF + case studies |

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
| `classical` | Formal, shastra-based, Sanskrit terms | BPHS, Phaladeepika, Saravali, A Text Book of Astrology, Lal Kitab |
| `modern_analytical` | Clear, psychological, practical | B.V. Raman — How to Judge a Horoscope |
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

> **[LOCKED — TEMPLE TEAM DECISION TD-01]**
> Fixed science weights are the mathematical backbone and are retained. Cross-science scoring uses a 3-layer model. Full specification in Section 15.

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

> **[LOCKED — TEMPLE TEAM DECISION TD-04]**
> Full 5-tab spec is Phase 1 scope. No tabs deferred. Separate `library_admin` role is mandatory — it represents editorial command, not operational access. The extra auth work is accepted and budgeted.

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
| `seed_rules.json` | ~300+ foundational rules | BPHS, Phaladeepika, Saravali, B.V. Raman + A Text Book of Astrology, Lal Kitab, Longevity and Astro System |
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

## 14. Pending Inputs From Codex

The following remain open pending Codex's simulation and maths responses:

1. **Schema simulation results** — see `CODEX_SCHEMA_SIMULATION_REQUEST.md`
2. **Science Arbitration mathematical framework** — see `CODEX_SCIENCE_ARBITRATION_REQUEST.md`
3. **Confirmation of build sequence** given all locked decisions above

All other sections are now locked by Temple Team decision log above.

---

## 15. Cross-Science Scoring — 3-Layer Model [LOCKED — TD-01, TD-13]

### Architecture Principle: Module-Determined Backbone Science [LOCKED — TD-13]

**The backbone science is not fixed globally. It is determined by which report module the user opens.**

| Module / Report | Backbone Science | Supporting Sciences |
|---|---|---|
| Brihat Kundali / Jyotish Report | Vedic Astrology | Numerology, Palmistry (Phase 2), Tarot (Phase 2) |
| Numerology Report | Numerology | Vedic Astrology |
| Palmistry Report | Palmistry | Vedic Astrology, Numerology |
| KP Report | Krishnamurti Paddhati | Vedic Astrology |
| Daily Guidance | Vedic Astrology | Numerology, World Context (α) |
| Longevity Report | Vedic Astrology | Palmistry (Phase 2), Numerology |

The backbone science always receives authority priority within its own module. Supporting sciences serve as precision layers — adding granularity and confirmation, not competition.

**Strategic rationale:** Users who believe in Numerology or Palmistry as their primary tool remain engaged because their science is treated as the backbone in those modules. This also prevents the platform from being perceived as "Astrology with extras". Each science is sovereign in its own report.

```python
# Every report evaluation passes backbone_science_id in context
rules = await engine.scan_chart(
    chart_data,
    categories=["career"],
    context={
        "backbone_science_id": "numerology",   # module-determined
        "alpha": 1.0,
        "beta":  1.0,
        "gamma": 1.0,
    }
)
```

### Layer 1 — Fixed Science Weights (Mathematical Backbone)

Fixed weights express the relative interpretive depth of each science across all content domains. They remain fixed — the backbone science selection adjusts *authority priority*, not these weights.

```python
SCIENCE_WEIGHTS = {
    "vedic_astrology": 0.40,
    "palmistry":       0.25,   # schema-ready, Phase 2 populated
    "numerology":      0.20,
    "tarot":           0.15,   # schema-ready, Phase 2 populated
}
# Phase 1: normalise only across active sciences
# e.g. astrology + numerology only → normalise to 0.60 base → scale to 1.0
# When backbone_science_id != vedic_astrology, that science receives a +0.10 authority boost
# in its own module before normalisation
```

### Layer 2 — Qualitative Confidence Tiers

Applied on top of Layer 1 as a multiplier reflecting how many sciences converge on the same claim.

| Sciences matched | Tier label | Score multiplier |
|---|---|---|
| 1 | Indication | × 0.60 |
| 2 | Partial Confirmation | × 0.80 |
| 3 | Strong Convergence | × 1.00 |
| 4 | Full Alignment | × 1.15 |

### Layer 3 — Contextual Multipliers α, β, γ

Three independent dimensions applied after Layers 1 and 2. Schema-ready in Phase 1. Data sourced from World Context Engine (Commission J) and user questionnaire (TD-19).

| Dimension | Scale | Captures | Phase 1 default | Phase 2 source |
|---|---|---|---|---|
| **α (Alpha)** | Macro | Geopolitical, cultural, environmental, seasonal context | 1.0 (neutral) | World Context Engine (Commission J) |
| **β (Beta)** | Micro | Individual life circumstances — profession, finances, health | 1.0 (neutral) | Subscription questionnaire (TD-19) |
| **γ (Gamma)** | Family | Household context, relationship status, family dynamics | 1.0 (neutral) | Subscription questionnaire (TD-19) |

```python
contextual_adjustment = 1.0 + (
    alpha_weight * alpha_score +   # default weight: 0.15
    beta_weight  * beta_score  +   # default weight: 0.10
    gamma_weight * gamma_score     # default weight: 0.10
)
# Range: ~0.78 → 1.22 — contextually amplifies or dampens final intensity

final_intensity = base_science_score * tier_multiplier * contextual_adjustment
```

**Phase 1 behaviour:** α, β, γ all default to neutral (1.0). Schema and scoring math live from day one. Intelligence grows as Commission J and the questionnaire system are built.

### MongoDB Schema — `contextual_scores` (request context)

```json
{
  "backbone_science_id": "vedic_astrology",
  "alpha": { "score": 0.92, "source": "world_context_engine", "event": "Diwali -3 days", "region": "IN" },
  "beta":  { "score": 0.75, "source": "user_questionnaire", "factors": ["salaried", "urban", "mid_wealth"] },
  "gamma": { "score": 0.60, "source": "user_questionnaire", "factors": ["married", "dependents", "parents_healthy"] }
}
```

### MongoDB Schema — `user_context_profile` (subscription member, Phase 2)

Schema-ready in Phase 1 — populated Phase 2 via onboarding questionnaire (TD-19).

```json
{
  "user_id": "ObjectId",
  "questionnaire_version": "1.0",
  "salary_bracket": "mid",
  "family_wealth_tier": "high",
  "siblings_count": 2,
  "current_city": "new-delhi",
  "travel_frequency": "monthly",
  "relationship_status": "married",
  "parents_birth_data": {
    "father": { "dob": "1955-03-15", "pob_city": "jaipur", "current_city": "jaipur" },
    "mother": { "dob": "1960-07-22", "pob_city": "delhi", "current_city": "jaipur" }
  },
  "beta_score": 0.75,
  "gamma_score": 0.60,
  "last_updated": "2026-04-10T00:00:00Z"
}
```

---

## 16. AI Paraphrase Pipeline [LOCKED — TD-02, TD-05]

### Policy

No verbatim text from any source enters MongoDB or Claude prompts. All content stored and transmitted is Temple Team's original AI-generated prose — attributed to classical Vedic tradition, not copied from it.

### Pipeline (runs locally inside `extract_book.py`)

```
OCR Source Text (stays on workstation)
         ↓
[Step 1] OCR Cleanup — noise, hyphen repair, line joining, header/footer strip
         ↓
[Step 2] Rule Extraction — structured If-Then rule + metadata + source excerpt (local only)
         ↓
[Step 3] Codex Paraphrase — generate original prose equivalent (see CODEX_PARAPHRASE_WIM.md)
         ↓
[Step 4] Codex Self-Check — confidence scoring (HIGH / MEDIUM / LOW)
         ↓
[Step 5] QA Triage
         HIGH   → staged for Library Console import review (Temple Team approves)
         MEDIUM → 1-in-5 flagged for Claude spot-check
         LOW    → every one reviewed by Claude before staging
         ↓
[Step 6] Original excerpt discarded locally
         ↓
[Step 7] AI-generated passage + metadata → output JSON → MongoDB via import endpoint
```

### Cost Model

- Codex handles ~85–90% of paraphrase passes
- Claude handles ~10–15% (flagged MEDIUM sample + all LOW)
- One-time cost per Amendment Contract — not a recurring runtime cost

### Reference

Full Codex paraphrase instructions: `CODEX_PARAPHRASE_WIM.md`

---

## 17. Science Arbitration Mechanism [LOCKED — TD-13 through TD-21]

### 17.1 — `science_registry` Collection [LOCKED]

Extensible science catalogue — adding a new science is a data operation, not a code change.

```json
{
  "_id": "ObjectId",
  "science_id": "vedic_astrology",
  "display_name": "Vedic Astrology — BPHS Tradition",
  "hierarchy_rank": 1,
  "authority_domain": ["life_path", "character", "relationships", "health", "karma", "timing"],
  "defers_to": [],
  "complements": ["kp", "numerology", "palmistry", "tarot"],
  "contradiction_policy": "leads",
  "active": true,
  "added_phase": 1
}
```

```json
{
  "science_id": "kp",
  "display_name": "Krishnamurti Paddhati",
  "hierarchy_rank": 2,
  "authority_domain": ["timing", "event_prediction"],
  "defers_to": ["vedic_astrology"],
  "complements": ["vedic_astrology", "numerology"],
  "contradiction_policy": "precision_layer",
  "active": true,
  "added_phase": 1
}
```

### 17.2 — New Required Fields on `interpretation_rules` [LOCKED — TD-15]

Every rule document must include:

```json
{
  "claim_axis":        "marriage_timing",
  "claim_scope":       "event_timing",
  "claim_polarity":    "negative",
  "timing_bias":       "late",
  "strength_band":     "high",
  "subject_scope":     "self",
  "authority_override": null,
  "mutually_exclusive_with": [],
  "passage_ref_id":    null
}
```

- `claim_axis` — the specific interpretive axis (e.g. `marriage_timing`, `career_growth`, `financial_security`, `health_vitality`)
- `claim_scope` — `tendency` / `event_timing` / `window` / `trait`
- `claim_polarity` — `positive` / `negative` / `mixed` / `neutral`
- `timing_bias` — `early` / `on_time` / `late` / `cyclical` / `none`
- `strength_band` — `low` / `medium` / `high` / `extreme`
- `subject_scope` — `self` / `partner` / `household` / `family`
- `passage_ref_id: null` — migration hook; Phase 2 links to `source_passages` collection if extracted

### 17.3 — Contradiction Detection [LOCKED — TD-16]

**Candidate pair:** both rules share the same `life_domain` AND `claim_axis`.
**Orthogonal (not a contradiction):** `claim_scope` differs — e.g. one is `tendency`, one is `event_timing`. Treat as layered meaning.

**Contradiction score:**
```
C = 0.40 × polarity_distance
  + 0.35 × timing_distance
  + 0.15 × strength_distance
  + 0.10 × authority_overlap
```

**Flag contradiction if:** C ≥ 0.55 AND both claims have `effective_confidence` ≥ 0.18.

### 17.4 — Tranche Filter Layer [LOCKED — TD-18]

Between contradiction detection and the narrative engine, the Tranche Filter applies user-circumstance rules from questionnaire data. These are If-Then rules that prevent false negatives based on context:

```python
TRANCHE_RULES = [
    {
        "condition": {"family_wealth_tier": "high"},
        "axis": "financial_security",
        "action": "dampen_secondary_negatives",
        "factor": 0.60
    },
    {
        "condition": {"relationship_status": "married", "gamma_score": {"gte": 0.70}},
        "axis": "partnership_stability",
        "action": "suppress_secondary_delay_indicators",
        "factor": 0.50
    },
]
```

**Phase 1:** Tranche rules seeded for the most common domains (financial_security, partnership_stability, career_growth). Rules applied as post-detection, pre-narrative adjustments to `effective_confidence`. Schema-ready; questionnaire data Phase 2.

### 17.5 — Runtime Arbitration (Production) [LOCKED — TD-17]

```
Step 1: Contradiction detection (Section 17.3)
Step 2: Tranche Filter (Section 17.4) — adjusts effective_confidence based on user context
Step 3: Supersession table lookup (category + claim_axis → secondary science priority)
Step 4: Confidence-delta tiebreaker (if Δ ≤ 0.15 → tension block; if Δ > 0.15 → lead wins)
Step 5: Representation mode selection (Section 17.6)
Step 6: Build tension_block JSON (Section 17.7) → send to Narrative Planner
```

Note: MCDA scoring is used **internally** to compute `effective_confidence` per claim. It is not exposed as the runtime theory.

### 17.5a — Supersession Table [LOCKED — TD-14]

Governs secondary science priority only. Backbone science always leads its own module (TD-13).

| Category | Primary axis lead (secondary sciences) | Notes |
|---|---|---|
| general | vedic_astrology | Numerology may co-lead on temperament sub-axes |
| career | vedic_astrology | Timing always astrology-led |
| wealth | vedic_astrology | Numerology pattern support only |
| relationships | vedic_astrology | Numerology may co-lead on compatibility tone, not timing |
| health | vedic_astrology | Palmistry rises when active (Phase 2) |
| education | vedic_astrology | Numerology secondary |
| spirituality | vedic_astrology | Tarot can challenge for secondary lead when active |
| longevity | vedic_astrology | Strongest domain authority; Palmistry second when active |

**Axis overrides:** any `*_timing` axis → astrology always leads among secondary sciences. Any `*_temperament` axis → numerology may lead in `general`, `relationships`, `career`. Reflective axes in `spirituality` → tarot may challenge later.

### 17.6 — Representation Mode Thresholds [LOCKED — TD-21]

| Mode | Trigger condition | Narrative treatment |
|---|---|---|
| **synthesis** | C < 0.30, or same directional polarity and Δ ≥ 0.05 | "Both your chart and your numerological signature point in a similar direction…" |
| **tension** | C 0.30–0.75 AND top effective_confidence ≥ 0.20 | "Your planetary structure suggests one rhythm, while your numerological pattern points toward another…" |
| **honest_uncertainty** | C > 0.75, or all effective_confidences < 0.20 | "The sciences we have examined do not fully converge on this question…" |

**Frequency caps:** max tension blocks = 20% of domain sections per report. Max honest_uncertainty = 5% of domain sections. Default: 1 major tension block per report unless user is in Test Console debug context.

### 17.7 — `tension_block` JSON (evidence packet to Narrative Layer) [LOCKED — TD-20]

```json
{
  "life_domain": "relationships",
  "claim_axis": "marriage_timing",
  "representation_mode": "tension",
  "dominant_science": "vedic_astrology",
  "backbone_science_id": "vedic_astrology",
  "confidence_delta": 0.10,
  "contradiction_score": 0.71,
  "contradiction_types": ["temporal"],
  "tranche_adjustments_applied": true,
  "low_confidence": false,
  "claims": [
    {
      "science_id": "vedic_astrology",
      "summary": "The chart suggests delay, maturity, and duty before stable commitment.",
      "effective_confidence": 0.44,
      "authority_rank": 1
    },
    {
      "science_id": "numerology",
      "summary": "The numerological pattern supports strong domestic orientation and earlier partnership desire.",
      "effective_confidence": 0.34,
      "authority_rank": 2
    }
  ]
}
```

---

## 18. World Context Engine — Commission J Reference [CONFIRMED — separate commission]

The World Context Engine (WCE) feeds the α (Alpha) contextual multiplier in real time. It is **not part of Commission I** — it is Commission J with a defined integration contract.

### What Commission J builds

```
World Context Engine
├── Global Calendar Layer (Hindu, Christian, Islamic, Jewish, regional festivals)
├── Lifecycle Calendar Layer (exam seasons, appraisal cycles, wedding seasons by region)
├── Geopolitical Layer (conflict zones, economic stress flags — Phase J2)
└── User Signal Layer (explicit profile + implicit behaviour signals)
```

### Commission I integration hook (build this in Phase 1)

Commission I's `KnowledgeEngine` must accept a `context` parameter and pass α/β/γ scores through the scoring model. Defaults to neutral (1.0) until Commission J populates them.

```python
rules = await engine.scan_chart(
    chart_data,
    categories=["career"],
    context={
        "alpha": 1.0,   # Commission J will populate this
        "beta":  1.0,   # User profile will populate this
        "gamma": 1.0    # User profile will populate this
    }
)
```

### Notification use case (Commission J powers this)

```
WCE detects: Diwali in 3 days (Hindu calendar, user in India)
Planetary: Jupiter in 9H (spiritually auspicious)
→ Alpha raised to 0.92
→ Notification triggered: Diwali Muhurta + Lakshmi Pooja ritual personalised to user's Lagna
```

---

---

## 19. Arc Angel — 12 Areas of Life User Profile [LOCKED — TD-23]

### Concept

The Arc Angel panel is the platform's **persistent master validation layer** — a left nav panel snapshot that shows the user's current standing across all 12 life domains. It is the first thing a Premium member sees after entering their birth data. Every module report on the platform must correlate its output back to the relevant Arc Angel dimension(s).

The name reflects its role: the Arc Angel is the user's guardian intelligence — an ever-sharpening profile that knows more about their life pattern the more they engage.

### The 12 Life Domains

| # | Domain | Vedic House | Core themes |
|---|---|---|---|
| 1 | Self & Vitality | 1st Bhava | Physical constitution, personality, health |
| 2 | Wealth & Family | 2nd Bhava | Income, family of origin, speech, accumulated assets |
| 3 | Courage & Communication | 3rd Bhava | Siblings, initiative, short travel, media |
| 4 | Home & Happiness | 4th Bhava | Property, mother, emotional security, vehicles |
| 5 | Intellect & Progeny | 5th Bhava | Children, creativity, education, speculation |
| 6 | Health & Challenges | 6th Bhava | Enemies, debt, disease, service, litigation |
| 7 | Partnerships | 7th Bhava | Marriage, business partners, contracts, public |
| 8 | Transformation | 8th Bhava | Longevity, inheritance, hidden matters, change |
| 9 | Luck & Dharma | 9th Bhava | Father, fortune, long travel, higher learning, spirituality |
| 10 | Career & Status | 10th Bhava | Profession, fame, authority, karma |
| 11 | Gains & Aspirations | 11th Bhava | Income from profession, friends, fulfilled desires |
| 12 | Liberation & Losses | 12th Bhava | Expenses, foreign lands, spirituality, moksha |

### Confidence % Scoring Model

Each domain has a Confidence % that reflects how much data the engine has to make an accurate assessment.

| Data input received | Confidence boost |
|---|---|
| Birth date + time + place only | Baseline ~40–50% |
| + Questionnaire complete (salary, family, residence, etc.) | +15–20% |
| + Additional module run (Numerology Report) | +5–8% per relevant domain |
| + Parents birth data provided | +8–12% |
| + Case study match found (similar chart on record) | +5% |
| + Subscription member (continuous dialogue) | Gradual improvement over sessions |

**Maximum Phase 1 confidence:** ~85% (full questionnaire + 2–3 module runs). 100% is never shown — maintains epistemic honesty that all prediction carries uncertainty.

### Per-Domain Output Structure

```json
{
  "domain_id": "career_status",
  "domain_label": "Career & Status",
  "bhava": 10,
  "period_quality": "auspicious",
  "period_indicator": "Jupiter dasha active — peak career period",
  "confidence_pct": 72,
  "auspicious_until": "2027-08",
  "correlated_modules": ["brihat_kundali", "numerology"],
  "last_updated": "2026-04-10T00:00:00Z"
}
```

### MongoDB Collection: `user_arc_angel_profile`

```json
{
  "user_id": "ObjectId",
  "computed_at": "2026-04-10T00:00:00Z",
  "overall_confidence_pct": 58,
  "data_completeness": {
    "birth_data": true,
    "questionnaire": false,
    "modules_run": ["brihat_kundali"],
    "parents_data": false
  },
  "domains": [
    {
      "domain_id": "self_vitality",
      "period_quality": "neutral",
      "confidence_pct": 55,
      "period_indicator": "Saturn transit 1H — discipline period"
    }
    // ... 11 more domains
  ]
}
```

### UI Behaviour

- **Left nav panel** — persistent across all pages for Premium members
- **On first load:** Shows 12 domains with confidence bars; domains with < 50% confidence show a "Provide more info" prompt
- **On module run:** Relevant domain confidence updates immediately; a subtle "Arc Angel updated" notification appears
- **Tap/click a domain:** Opens a mini-report for that domain (sourced from matched rules, not a full report)
- **Progress indicator:** Overall profile completeness % shown at top of panel

### Cross-Module Correlation Pattern

Every module report includes a correlation footer:

> *"This Career Report reinforces your Arc Angel Career & Status score of 72% (Auspicious). Jupiter's influence identified here aligns with the peak career window shown in your profile."*

---

## 20. Case Study Validation Pipeline [LOCKED — TD-24]

### Purpose

1,000+ published case studies of public figures (known birth data + documented life outcomes) serve as the Knowledge Engine's **empirical acceptance test suite and calibration dataset**.

This is not just validation data — it is what allows the engine to move from hand-authored confidence thresholds to empirically validated ones, and it is what may accelerate Bayesian priors from Phase 3 to Phase 2 (see TDF-03).

### Available Case Study Sources (Phase 1)

| Source | Volume | Domain focus |
|---|---|---|
| Numerology Phase 1 book (Your Destiny Is In Your Name & DOB) | ~50 case studies | Numerology — name/DOB outcomes |
| Longevity and Astro System (Tier 1 book) | ~30+ case studies | Longevity, health timing |
| Vedic Numerology — Ank Jyotish | ~50 case studies | Numerology cross-validation |
| Additional published sources | 800–900 | Multi-domain — public figures (deceased and living) |
| **Total Phase 1 target** | **~1,000+** | Multi-science, multi-domain |

### Case Study Document Structure

Each case study, once extracted, must be structured as:

```json
{
  "case_id": "CS-001",
  "subject": "Public figure name or anonymised ID",
  "birth_data": {
    "date": "1942-07-18",
    "time": "14:30",
    "place": "Johannesburg, South Africa",
    "latitude": -26.2041,
    "longitude": 28.0473,
    "timezone": "Africa/Johannesburg"
  },
  "known_outcomes": [
    {
      "life_domain": "career_status",
      "claim_axis": "career_peak",
      "outcome": "positive",
      "timing": "1964–1990",
      "notes": "Led major political movement, became head of state 1994"
    }
  ],
  "source_book": "additional_sources",
  "data_quality": "high",
  "added_phase": 1
}
```

### How Case Studies Feed the Engine

**Phase 1 — Build:**
- Extract and structure 50–100 high-quality cases from Phase 1 books
- Run each case through `scan_chart()` once the engine is live
- Compare predicted period quality (auspicious/inauspicious) against known outcomes

**Phase 1.2 — Calibration:**
- Measure prediction accuracy across domains
- Identify which contradiction thresholds (C ≥ 0.55, effective_confidence ≥ 0.18) hold empirically
- Adjust if needed before Phase 2 launch

**Phase 2 — Full Validation:**
- Expand to 1,000+ cases
- Bayesian likelihood ratio estimation per domain (upgrades TDF-03 to Phase 2)
- MCDA criteria weight calibration (upgrades TDF-P2 to Phase 2)

### MongoDB Collection: `case_studies`

```json
{
  "_id": "ObjectId",
  "case_id": "CS-001",
  "subject": "...",
  "birth_data": { ... },
  "known_outcomes": [ ... ],
  "engine_predictions": [ ],
  "accuracy_score": null,
  "validated": false,
  "source_book": "longevity_astro_system",
  "data_quality": "high",
  "added_phase": 1
}
```

### Library Console Integration

A **Case Studies tab** is added to the Library Console (Tab 6 — Phase 1.2):
- Import structured case study JSON
- Run batch validation against the live engine
- View accuracy scores by domain and by science
- Flag cases where engine prediction diverged from known outcome for manual review

---

## 21. CPath-1 — Build Priority Sequence [LOCKED]

The contract has all architecture correct. This section specifies **build order** to ensure the core product ships before the editorial tooling.

### CPath-1 (Hours 1–80) — Core Engine: Non-Negotiable

These must be complete and tested before anything else proceeds:

| # | Deliverable | Why it is on the critical path |
|---|---|---|
| 1 | MongoDB schemas — all collections, all TD-15 fields, all indexes | Nothing works without this |
| 2 | `extract_book.py` + AI Paraphrase pipeline | Seed data production — blocks all rule library work |
| 3 | In-memory inverted index + `scan_chart()` | Core rule evaluation — blocks narrative layer |
| 4 | `generate_narrative()` + Claude API Narrative Planner | The product output — blocks report API |
| 5 | Library Console: Rules Browser + Import endpoint + Approval workflow | Required to load seed data into production |
| 6 | One complete report API route end-to-end (Brihat Kundali first) | Proves the stack works before adding complexity |
| 7 | Simplified Phase 1 arbitration runtime (backbone leads; secondary acknowledges) | Required for Phase 1 narrative coherence |
| 8 | Tranche Filter rule engine with seeded domain rules | Required for Phase 1 prediction accuracy |

### Phase 1.2 (Hours 80–125) — Builds on Running System

| # | Deliverable | Dependency |
|---|---|---|
| 9 | Coverage Dashboard heatmap | Needs import pipeline from CPath-1 |
| 10 | Arc Angel profile computation + `user_arc_angel_profile` collection | Needs `scan_chart()` from CPath-1 |
| 11 | Arc Angel left nav panel UI | Needs Arc Angel backend |
| 12 | Remaining report API routes (Numerology, Longevity, etc.) | Needs narrative layer from CPath-1 |
| 13 | Case Study extraction + batch validation (50–100 Phase 1 cases) | Needs full engine from CPath-1 |
| 14 | `user_context_profile` schema + β/γ hook integration | Needs Tranche Filter from CPath-1 |

### Phase 1.3 (Hours 125–150) — If Budget Holds

| # | Deliverable | Note |
|---|---|---|
| 15 | Test Console + Voice Profiles editor (Library Console tabs 4–5) | Editorial tooling — valuable but not blocking |
| 16 | `science_registry` editor in Library Console | Operational refinement |
| 17 | Threshold recalibration using case study results | Empirical improvement pass |

### Separate Phase 1 Commissions (Not in Commission I Hours)

| Commission | Scope | Dependency on Commission I |
|---|---|---|
| Commission I-Q (Questionnaire) | Onboarding questionnaire UI + flow + β/γ population | Needs `user_context_profile` schema from Commission I |
| Commission I-K (Kota Chakra) | Parents birth data calculation + enhanced accuracy layer | Needs vedic_calculator.py extension |
| Commission J (World Context Engine) | α multiplier population via global calendars | Needs context hooks from Commission I |

---

> Stack: FastAPI (Render, Docker python:3.12.9-slim) + React 18 (Vercel) + MongoDB (Motor async) + pyswisseph 2.10.x + Claude API (`claude-sonnet-4-6`)
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Main branch: `main` (deploy-on-push)
> Effort estimate: 125–150h Commission I core + separate commissions I-Q, I-K, J
