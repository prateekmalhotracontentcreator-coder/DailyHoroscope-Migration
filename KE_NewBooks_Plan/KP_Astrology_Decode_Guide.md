# KP Astrology -- CC Decode Guide (Krishnamurty Vol 3)

> **Single authoritative reference for this thread.**
> Book: Predictive Stellar Astrology Vol 3 -- Prof K.S. Krishnamurty (founder of KP system)
> Workflow: User provides NLM .md output per chapter → CC converts to Rules.json. NLM has NOT been run yet -- chapters are split and ready, NLM runs one chapter at a time as decode progresses.
> Operate autonomously chapter by chapter. No toggling to parent session required.
> Last updated: 2026-05-26

---

## 🔴 MANDATORY FIRST ACTION -- Do this NOW, before reading anything else

**Step 1:** Create the output folder and a thread-start marker file:

| # | File path | Initial content |
|---|---|---|
| 1 | `/Users/apple/Documents/Knowledge Engine_eBooks/KP_CC_Decode/KP_ThreadStart.md` | `# KP Vol3 Decode Thread\n\nStarted: [date]. Awaiting Phase 0 + user confirmation before first chapter decode.` |

**Step 2:** Post this one line in the context window:
> "Output folder created. Reading guide and chapter PDFs for Phase 0."

**Do not create any chapter Rules.json files yet. NLM has not been run. Chapter files are created only when the user provides the NLM .md output for a specific chapter.**

---

## PHASE 0 -- Fresh Eyes Assessment

**You have split this book into chapters and can read the chapter PDFs directly. NLM has not been run yet. Read this guide fully, then read through the chapter PDFs and answer these questions based on what you find in the actual text.**

Write your answers to:
`/Users/apple/Documents/Knowledge Engine_eBooks/KP_CC_Decode/KP_Vol3_FreshEyes.md`

Answer each point in 2-5 lines. Be specific -- name chapters where relevant.

---

**1. Schema gaps**
Does this book contain KP rule structures NOT covered by the condition types in Part 3? (e.g., ruling planet combinations, transit-over-natal rules, KP annual chart rules, Nirayana Bhava Chalit-specific logic)

**2. Case study density**
KP Vol 3 mixes rules with example charts heavily. From reading the chapter PDFs -- which chapters are predominantly case studies (0 extractable rules)? Which chapters have rules clearly separated from examples?

**3. Sub-lord vs significator split**
The guide treats sub-lord rules and significator rules as distinct condition types. Does this book mix them in ways that make that separation difficult? Any chapters where the two types blur?

**4. Recommended decode sequence**
There is no pre-set order for KP Vol 3 -- you are the first to read this book in this thread. Based on reading the chapter PDFs, write a recommended numbered sequence covering:
- Chapters that define foundational KP terminology or methodology (decode first -- later chapters depend on these)
- Chapters that are predominantly case studies with zero rules (decode last or note as skip)
- Chapters that can be decoded independently in any order (bulk of the book)
- Any dependency chains (Chapter X should come before Chapter Y because...)

Write the complete recommended sequence as a numbered list. The user will review and confirm before NLM is run on the first chapter.

**5. Dedup signal**
From scanning the chapter content -- how much overlap do you expect with the 300 Horoscopes decode (same KP system)? Which chapters look most likely to produce duplicate rules?

**6. Guide gaps**
Anything in this guide that is unclear, missing, or conflicts with what you actually see in this book's content?

---

After writing the file, post one line:
> `"Fresh Eyes written -- [N] flags raised. Recommended sequence in file. Awaiting your confirmation of sequence + go-ahead to begin NLM on Chapter 1."`

**Do not request NLM or begin decode until user confirms the sequence.**

---

## ⚠️ OUTPUT METHOD -- Absolute Rule

**ALL converted content goes into files via the Write tool. Zero exceptions.**
**The context window receives one-line status updates only -- nothing more.**
**Every chapter produces exactly 3 output files (Rules.json, Diagnostic.md, Summary.md).**
**JSON rules written in batches of ≤25 per Write call. Large chapters use Part files.**
**Output folder:** `/Users/apple/Documents/Knowledge Engine_eBooks/KP_CC_Decode/`

---

## Chapter Conversion Protocol -- Execute for EVERY chapter

### Step 1 -- Create output files (Write tool × 3)
- `KP3_Ch{NN}_{ShortTitle}_Rules.json` → `[]`
- `KP3_Ch{NN}_{ShortTitle}_Diagnostic.md` → placeholder
- `KP3_Ch{NN}_{ShortTitle}_Summary.md` → placeholder

### Step 2 -- Context window: one line only
> `"3 files created for Ch[NN]. Beginning conversion."`

### Step 3 -- Receive and read the NLM .md file for this chapter

The user runs NLM on one chapter at a time and provides the .md output to this thread.
**Do not proceed to Step 4 until the user pastes or confirms the NLM .md file path for this chapter.**
Post: `"Ready for Ch[NN] NLM output."` and wait.

**NLM Report Format -- What to request:**

| Chapter type | NLM report to request |
|---|---|
| Rule chapters (Block 1, 3, 4, 5 -- all prediction chapters) | **JSON report only** -- structured output CC can parse into KE schema |
| Table-only chapters (Block 2: T02, T03, T05, P89) | **Data Tables & Conventional Array report** -- these chapters produce zero rules; tables go to Summary.md |

Do NOT request Summary or Diagnostic reports from NLM -- CC generates its own Summary.md and Diagnostic.md per the protocol above.

### Step 4 -- Classify the NLM content

| Content type | Action |
|---|---|
| Significator rules: "[Planet] as significator of [House] → [Outcome]" | → Full JSON rule |
| Sub-lord rules: "Sub-lord of [cusp] in [sign/house] → [Result]" | → Full JSON rule |
| House + planet combination rules | → Full JSON rule |
| KP methodology procedures | → Rule with `claim_scope: "engine_specification"` |
| Rule-dense table (grid of condition × outcome cells) | → Extract each non-empty cell as a **separate JSON rule** -- do not compress |
| Lookup tables (sub-lord tables, significator lists, cusp tables) | → Summary.md only. Not rules. |
| Visual chart or diagram (KP wheel, dasha timeline) | → Note in Diagnostic only. Not rules. |
| Illustrative examples / case study charts | → Diagnostic.md benchmark section only. Not rules. |
| Narrative / biographical or historical text | → Discard |

### Step 5 -- Write JSON Rules (batched -- ≤25 per Write call)

### Step 6 -- Write Summary.md (chapter scope, KP principle covered, rule count, NLM quality notes)

### Step 7 -- Write Diagnostic.md (see Part 5 for required sections)

### Step 8 -- Context window: one line only
> `"Ch[NN] complete. [N] rules. Proceeding to Ch[NN+1]."`

**Rule count expectation: 15-35 rules per chapter.**
If actual count is below 15: Post flag -- "LOW YIELD -- NLM output may have summarised rules as narrative. Flag for user before proceeding to next chapter."

---

## Table & Chart Handling Protocol

When a chapter contains tables, charts, or diagrams, classify each one before extracting:

| Content type | What it looks like | Action |
|---|---|---|
| **Rule-dense table** | Grid where each row/cell states a KP condition (cusp/sub-lord/significator) and an outcome | Extract each non-empty cell as a **separate JSON rule**. A 9×3 table = up to 27 rules -- do not compress |
| **Reference / lookup table** | Sub-lord tables, significator lists, Nakshatra-to-sub-lord mappings, cusp degree tables | → `Summary.md` only. Not rules |
| **Calculation procedure table** | Step-by-step KP computation with inputs and outputs | → `engine_specification` rule if it defines KP methodology; `Summary.md` if pure reference |
| **Visual chart / diagram** | KP Nirayana wheel, dasha timeline visual, Placidus house diagram | → Note in Diagnostic only: "Chapter contains [type] -- visual content, not extractable as rules." Zero rule extraction |

**The test:** Does each row or cell state a condition **and** an outcome? Yes → rules. No → `Summary.md`.

---

## PART 1 -- Project Identity

| Field | Value |
|---|---|
| Book | Predictive Stellar Astrology Vol 3 -- Prof K.S. Krishnamurty |
| `book_id` | `kp_vol3_20260526` |
| `science_id` | `kp_jyotish` |
| `checkable` | `false` (KP sub-lord engine not yet built in the platform) |
| Astrological system | Krishnamurti Paddhati (KP) -- Placidus house division, KP Ayanamsha |
| Source PDF | `/Users/apple/Documents/Knowledge Engine_eBooks/KP Astology Text Books/03-predictive-stellar-astrology-3-kp-system-by-prof-k-s-krishnamurty-good-quality.pdf` |
| Chapter PDFs | User has pre-split the source PDF -- chapters available for reading |
| NLM workflow | User runs NLM one chapter at a time and provides output to CC thread on request |
| Output folder | `/Users/apple/Documents/Knowledge Engine_eBooks/KP_CC_Decode/` |
| Decode method | CC reads chapter PDF (Phase 0) → user runs NLM per chapter → CC converts .md → Rules.json |
| Rule ID prefix | `kp3-ch{NN}-{NNN}` |
| Related books | Longevity and Astro System (same KP system -- flag overlaps as `duplicate_candidate: true, duplicate_source: "longevity_kp"`) |

### Dedup -- Critical

KP Vol 3 rules will overlap with the 300 Horoscopes decode (same KP system).
During decode, if a rule is substantively identical to an already-decoded KP rule:
- Set `"duplicate_candidate": true`
- Set `"duplicate_source": "h300_horoscopes"` or `"longevity_kp"` as appropriate
- Do NOT skip the rule -- capture it fully. Arbitration happens at ingest time.

---

## PART 2 -- KP System Primer

Before decoding, understand these KP fundamentals so rules are classified correctly:

**The 4-Level Signification Hierarchy (strongest → weakest):**
1. Planets in the stars (Nakshatras) of occupants of the house (strongest)
2. Planets directly occupying the house
3. Planets in the stars of the lord of the house cusp
4. Sign lord of the house (weakest -- fallback only)

**Sub-Lord:** The KP subdivision of a Nakshatra into 9 sub-divisions. The sub-lord of a cusp determines event quality for that house.

**Cusps (12 house cusps):** The exact degree/minute of each house cusp. The sub-lord of each cusp governs events related to that house.

**Significators:** Planets that signify a house through the 4-level hierarchy.

**Ruling Planets (RPs):** Active signifiers at the moment of judgment (Lagna lord, Moon sign lord, Moon star lord, and Day lord).

**Houses of Interest for KP Vol 3 (Prediction & Timing):**
- Event houses: vary by topic (2nd+7th+11th for marriage, 1st+8th for longevity, etc.)
- Promise houses: must be signified in natal chart for the event to be promised
- Fruitful Sub-lord: the sub-lord of the relevant cusp must signify event houses for manifestation

**KP Timing:** Dasha-Bhukti-Antara-Sookshma (DBAS) system. Planet must be a significator of relevant houses in all 4 periods.

---

## PART 3 -- Full KE Schema

```json
{
  "rule_id": "kp3-ch05-001",
  "science_id": "kp_jyotish",
  "active": true,
  "approval_status": "pending_human_review",
  "checkable": false,
  "source": {
    "book": "KP Astrology Vol 3",
    "book_id": "kp_vol3_20260526",
    "chapter": 5,
    "chapter_name": "[Exact chapter title from chapter PDF]",
    "sloka": null,
    "batch_id": "kp3-ch05-v1-20260526",
    "passage_ref_id": null
  },
  "title": "Sub-Lord of 7th Cusp in 6th -- Marriage Denial",
  "summary": "When the sub-lord of the 7th cusp is placed in the 6th house, the promise of marriage is denied or severely delayed.",
  "full_text": "The sub-lord of the 7th cusp governs the promise of marriage. If this sub-lord is posited in the 6th house (a dusthana), the native faces significant obstacles to marriage, including denial or extreme delay.",
  "tags": ["marriage", "7th_cusp", "sub_lord", "6th_house", "denial"],
  "category": "kp_prediction",
  "condition": {
    "type": "kp_sub_lord",
    "cusp": 7,
    "sub_lord_house": 6,
    "sub_lord_sign": null,
    "kp_gate": null,
    "signification_level": null,
    "lagna_modality": "universal",
    "event_houses": [2, 7, 11]
  },
  "claim_axis": "marriage_timing",
  "claim_scope": "natal_trait",
  "claim_polarity": "negative",
  "timing_bias": "sustained",
  "strength_band": "high",
  "subject_scope": "self",
  "authority_override": null,
  "mutually_exclusive_with": [],
  "result": {
    "effect": "Marriage denied or significantly delayed due to sub-lord in dusthana.",
    "severity": "high",
    "remedy_available": false,
    "remedy_ref_id": null
  },
  "contradiction_flag": false,
  "duplicate_candidate": false,
  "duplicate_source": null
}
```

### Field-by-Field Rules

**`rule_id`:** `kp3-ch{NN}-{NNN}` -- chapter zero-padded to 2 digits, sequence to 3.

**`science_id`:** Always `"kp_jyotish"`. Never `"vedic_astrology"`. These are different systems.

**`checkable`:** Always `false`. KP sub-lord engine is not yet built in the platform.

**`approval_status`:** Always `"pending_human_review"`. Use `"tba_needs_trigger"` if the trigger condition is unclear from the NLM output.

**`condition.type` valid values for KP:**
- `"kp_sub_lord"` -- rule fires based on sub-lord of a specific cusp
- `"kp_significator"` -- rule fires based on 4-level significator hierarchy
- `"kp_badhaka"` -- rule involves badhaka house logic
- `"kp_longevity_factor"` -- rule contributes to longevity/event assessment
- `"engine_specification"` -- rule defines KP methodology

**`condition.cusp`:** Integer 1-12. The house cusp being evaluated (for `kp_sub_lord` rules).

**`condition.sub_lord_house`:** Integer 1-12. Where the sub-lord is posited (for `kp_sub_lord` rules).

**`condition.event_houses`:** Array of integers. The houses relevant to the predicted event (e.g., `[2, 7, 11]` for marriage). `null` for engine_specification rules.

**`claim_axis` valid values:**
`health_vitality`, `career_growth`, `financial_security`, `partnership_stability`, `marriage_timing`, `spirituality`, `family_life`, `longevity`, `accident_risk`, `travel`, `creativity`, `social_network`, `general`

**`claim_scope`:**
- `"natal_trait"` -- promise in the natal chart (sustained from birth)
- `"event_timing"` -- fires at a specific DBAS period
- `"engine_specification"` -- KP methodology definition

**`claim_polarity`:**
- `"positive"` -- event manifests, promise fulfilled
- `"negative"` -- event denied, blocked, or harmful
- `"conditional"` -- depends on additional factors
- `"neutral"` -- engine specification rules

**`full_text`:** No numeric coefficients. No percentages. Use: significant / severe / extreme / moderate / limited.

**`duplicate_candidate`:** `true` if this rule is substantively identical to an already-decoded KP rule. Set `duplicate_source` to the relevant book ID.

---

## PART 4 -- Diagnostic.md Required Sections

```
## Ch[NN] Diagnostic

### 1. Chapter Scope
[What KP topic does this chapter cover?]

### 2. Rule Count
Total: [N]
Breakdown by type: kp_sub_lord: [N] | kp_significator: [N] | engine_specification: [N] | other: [N]

### 3. NLM Output Notes
[Quality of the NLM .md provided for this chapter -- missing rules, narrative-heavy sections, unclear conditions, anything that required judgement calls during conversion]

### 4. Exclusions
[Content in the NLM output that was NOT converted to rules, and why]

### 5. Contradictions
[Rules with contradiction_flag: true -- what they say and why they conflict]

### 6. TBA Rules
[Rules with tba_needs_trigger -- what outcome is known, what trigger is unclear]

### 7. Duplicate Candidates
[Rules flagged as duplicate_candidate: true -- which source book they duplicate]

### 8. Case Study Benchmarks
[Any example charts in the NLM file -- log chart data + which rule it validates]

### 9. Open Questions
[KP logic the chapter or NLM output hints at but doesn't fully specify]
```

---

## PART 5 -- Quality Gate Checklist

Run on every rule before finalising.

- [ ] `rule_id` format: `kp3-ch{NN}-{NNN}` -- correct chapter, sequential
- [ ] `science_id`: `"kp_jyotish"` -- NOT `"vedic_astrology"`
- [ ] `active: true` and `checkable: false`
- [ ] `approval_status`: `"pending_human_review"` or `"tba_needs_trigger"`
- [ ] `source` block: all 7 fields present including `batch_id`
- [ ] `condition.type`: valid KP value from Part 3 list
- [ ] `condition.event_houses`: populated for prediction rules; `null` for engine_spec
- [ ] `full_text`: no numeric coefficients -- intensity words only
- [ ] `claim_axis`: valid value from Part 3 list
- [ ] `duplicate_candidate`: checked against 300 Horoscopes + Longevity KP decodes
- [ ] `contradiction_flag`: `true` if contradicts another rule in same chapter
- [ ] Rule count: ≥15 per chapter -- if below, flag in Diagnostic
- [ ] No rules written to context window

---

## PART 6 -- Known Issues to Avoid

1. **Context window overflow:** Never write rule arrays to context window. Write tool only.

2. **Science ID confusion:** KP is NOT Vedic astrology. Always `"kp_jyotish"`. If a rule uses Parashari logic (house lordship, yogas), that is unusual for KP Vol 3 -- flag it in Diagnostic.

3. **Significator vs Sub-lord confusion:** Significator rules use the 4-level hierarchy. Sub-lord rules evaluate the cusp's sub-lord specifically. They are different rule types -- do not merge.

4. **NLM narrative absorption:** KP Vol 3 by Krishnamurty contains significant explanatory text around each rule. NLM may summarise explanations rather than extract rules. If rule count seems low, re-read the NLM output carefully for rules embedded in paragraphs.

5. **Chapter scope confirmation:** KP Vol 3 covers advanced prediction and timing. If a chapter is entirely case studies (example charts), extract zero rules and log all charts as benchmarks in Diagnostic.

6. **Event houses field:** Every prediction rule must specify what event it predicts and which houses form the promise. Do not leave `event_houses: null` on prediction rules.
