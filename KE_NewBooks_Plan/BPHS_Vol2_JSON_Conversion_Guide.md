# BPHS Vol 2 -- JSON Conversion Guide (Ch49, Ch50, Ch51)

> **Single authoritative reference for this thread.**
> This thread does NOT decode from PDF. NotebookLM (NLM) has already produced .md outputs for all 3 chapters.
> This thread reads those .md files and converts each extracted rule to the full KE JSON schema.
> Last updated: 2026-05-26

---

## 🔴 MANDATORY FIRST ACTION -- Do this NOW, before reading anything else

Create the output folder anchor file:

| # | File path | Initial content |
|---|---|---|
| 1 | `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/BPHS_Vol2_ThreadStart.md` | `# BPHS Vol2 JSON Conversion Thread\n\nStarted: [date]. Awaiting Phase 0 + user confirmation before Ch49 conversion begins.` |

Then post this one line in the context window:
> "Output folder anchored. Reading guide and NLM files for Phase 0."

**Do not create any chapter Rules.json or output files yet. Ch49 files are created inside the Chapter Conversion Protocol, after Phase 0 is confirmed by the user.**

---

## PHASE 0 -- Fresh Eyes Assessment

**You have already seen the NLM .md files for these 3 chapters. Before creating any conversion files or writing any rules, read this guide fully -- then answer these questions from what you observed in the NLM outputs.**

Write your answers to:
`/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/BPHS_Vol2_FreshEyes.md`

Answer each point in 2-5 lines. Be specific -- name chapters where relevant.

---

**1. NLM output quality**
For each of the 3 chapters: was the NLM output clearly structured as rules, or was it narrative-heavy / table-only / ambiguous? Which chapter looks thinnest and may need extra scrutiny during conversion?

**2. Schema gaps**
Does the content of these chapters contain condition types or rule structures NOT covered by the schema in Part 3? (e.g., special lagna conditions, varga-chart-specific rules, conditional multi-factor chains)

**3. Shloka references**
Did the NLM outputs preserve shloka numbers (e.g., "49.7")? Or were they stripped during NLM processing? This affects the `source.sloka` field quality.

**4. Dimension coverage**
BPHS Vol 2 late chapters may address different dimensions than the standard house-effect set. What dimensions or topics do these 3 chapters actually cover? Anything not in this guide's list?

**5. BPHS Vol 1 overlap signal**
From what you saw in the NLM outputs, do these chapters duplicate BPHS Vol 1 content heavily, or is this genuinely new material? Rough estimate: what percentage looks unique?

**6. Recommended conversion sequence**
The default sequence is Ch49 → Ch50 → Ch51. Based on reading the NLM .md files:
- Does any chapter need to be converted before another for context or dedup reasons?
- Is any chapter's NLM output so thin that it should be flagged before starting rather than converted first?

Write your recommended numbered sequence for these 3 chapters. If Ch49→50→51 order is fine, confirm that explicitly.

**7. Guide gaps**
Anything in this guide that is unclear, incorrect, or doesn't match what you see in the actual NLM files?

---

After writing the file, post one line:
> `"Fresh Eyes written -- [N] flags raised. Recommended sequence in file. Awaiting your confirmation of sequence + go-ahead to begin conversion."`

**Do not begin conversion until user confirms the sequence. Chapter 49 output files are created inside the Chapter Conversion Protocol -- not before.**

---

## ⚠️ OUTPUT METHOD -- Absolute Rule

**ALL converted content goes into files via the Write tool. Zero exceptions.**
**The context window receives one-line status updates only -- nothing more.**
**Every chapter produces exactly 3 output files (Rules.json, Diagnostic.md, Summary.md).**
**JSON rules are written in batches of ≤25 rules per Write call. Use Part files if >25 rules.**
**Output folder:** `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/`

---

## Chapter Conversion Protocol -- Execute for EVERY chapter

### Step 1 -- Create output files (Write tool × 3)
- `BPHS_Vol2_Ch{NN}_Rules.json` → `[]`
- `BPHS_Vol2_Ch{NN}_Diagnostic.md` → placeholder
- `BPHS_Vol2_Ch{NN}_Summary.md` → placeholder

### Step 2 -- Context window: one line only
> `"3 files created for Ch[NN]. Beginning conversion."`

### Step 3 -- Read the NLM .md file for this chapter

| Chapter | NLM file to read |
|---|---|
| Ch49 | `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS Vol 2 Decode/BPHS Ch49 Decode_Vol 2_JSON_NoteBookLM.md` |
| Ch50 | `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS Vol 2 Decode/BPHS_Ch50_Decode_Vol 2_JSON_Notebook LM.md` |
| Ch51 | `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS Vol 2 Decode/BPHS_Ch51_Decode_Vol 2_JSON_NotebookLM.md` |

### Step 4 -- Classify the NLM content

| Content type | Action |
|---|---|
| Rules in format "[Condition] → [Outcome]" | Convert to full JSON schema (see Part 3) |
| Rule-dense table (grid of condition × outcome cells) | → Extract each non-empty cell as a **separate JSON rule** -- do not compress |
| Lookup tables (planetary data, sign tables, dignity lists) | → Summary.md only. Not rules. |
| Visual chart or diagram (Rasi wheel, house diagram) | → Note in Diagnostic only. Not rules. |
| Narrative / explanatory paragraphs | → Summary.md only. Not rules. |
| Methodology / calculation procedures | → Rule with `claim_scope: "engine_specification"` |

### Step 5 -- Write JSON Rules (batched -- ≤25 per Write call)

### Step 6 -- Write Summary.md (chapter scope, key topics, rule count, any NLM quality issues)

### Step 7 -- Write Diagnostic.md (see Part 5 for required sections)

### Step 8 -- Context window: one line only
> `"Ch[NN] complete. [N] rules. Proceeding to Ch[NN+1]."`

**If rule count is below 15:** Post a flag before closing -- "LOW YIELD -- NLM may have summarised rules as narrative. Flag for human review."

---

## Table & Chart Handling Protocol

When the NLM output references tables, charts, or diagrams from the source chapter, classify each one before extracting:

| Content type | What it looks like | Action |
|---|---|---|
| **Rule-dense table** | Grid where each row/cell states a planet, house/condition, and an outcome | Extract each non-empty cell as a **separate JSON rule**. A 9×3 table = up to 27 rules -- do not compress |
| **Reference / lookup table** | Planetary dignity data, sign quality tables, Nakshatra lists, house lord lists | → `Summary.md` only. Not rules |
| **Calculation procedure table** | Step-by-step computation with inputs and outputs | → `engine_specification` rule if it defines Parashari methodology; `Summary.md` if pure reference |
| **Visual chart / diagram** | Rasi wheel, house diagram, dasha timeline visual | → Note in Diagnostic only: "Chapter contains [type] -- visual content, not extractable as rules." Zero rule extraction |

**The test:** Does each row or cell state a condition **and** an outcome? Yes → rules. No → `Summary.md`.

---

## PART 1 -- Project Identity

| Field | Value |
|---|---|
| Book | Brihat Parashara Hora Shastra (BPHS) Vol 2 -- R. Santhanam translation |
| `book_id` | `bphs_vol2_20260526` |
| `science_id` | `vedic_astrology` |
| `checkable` | `true` |
| Astrological system | Classical Parashari Vedic Astrology |
| Chapters in scope | Ch49, Ch50, Ch51 only |
| NLM source folder | `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS Vol 2 Decode/` |
| Output folder | `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/` |
| Decode method | **NLM → CC Conversion** -- NLM .md already produced; CC converts to JSON only |
| Rule ID prefix | `bphs2-ch{NN}-{NNN}` |
| Related book | BPHS Vol 1 -- same author/tradition. Flag overlaps as `duplicate_candidate: true, duplicate_source: "bphs_vol1"` |

### What NOT to do

- **Primary source is the NLM .md files** -- read these first for every chapter. Do NOT go to the source PDFs unless the NLM output is ambiguous, thin, or missing critical context for a specific rule.
- Do NOT re-run NotebookLM. The .md files are the final NLM output -- use them as-is.
- Do NOT decode chapters outside Ch49-Ch51. This thread is scoped to 3 chapters only.
- Do NOT write rules to the context window.

---

## PART 2 -- Vedic System Context

**Houses (Bhavas):** 12 houses numbered from Ascendant (Lagna = 1st).
- Kendras: 1, 4, 7, 10 | Trikonas: 1, 5, 9 | Dusthanas: 6, 8, 12

**Planets:** Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu
- Natural Benefics: Jupiter, Venus, Mercury (waxing), Moon (waxing)
- Natural Malefics: Sun, Mars, Saturn, Rahu, Ketu

**BPHS Vol 2 chapters (Ch49-Ch51) likely cover:**
Ch49-Ch51 are late chapters in the BPHS Vol 2 scope. Topics may include special lagnas, sub-divisional chart effects, or advanced combinations. The NLM .md file will reveal the actual content -- read it before classifying.

---

## PART 3 -- Full KE Schema

Every rule is a MongoDB document. Complete schema for BPHS Vol 2:

```json
{
  "rule_id": "bphs2-ch49-001",
  "science_id": "vedic_astrology",
  "active": true,
  "approval_status": "pending_human_review",
  "checkable": true,
  "source": {
    "book": "BPHS Vol 2",
    "book_id": "bphs_vol2_20260526",
    "chapter": 49,
    "chapter_name": "[Title from NLM file header]",
    "sloka": null,
    "batch_id": "bphs2-ch49-v1-20260526",
    "passage_ref_id": null
  },
  "title": "Short noun phrase describing the rule",
  "summary": "One sentence -- what the rule says.",
  "full_text": "Full diagnostic logic in plain language. No numeric coefficients -- use intensity words (significant, moderate, extreme, severe).",
  "tags": ["planet_or_house", "topic", "dimension"],
  "category": "house_effects",
  "condition": {
    "type": "planet_in_house",
    "planet": null,
    "house": null,
    "sign": null,
    "nakshatra": null,
    "strength_requirement": null,
    "dasha_lord": null,
    "antardasha_planet": null,
    "applies_to_all_dasha_lords": false
  },
  "claim_axis": "general",
  "claim_scope": "natal_trait",
  "claim_polarity": "positive",
  "timing_bias": "sustained",
  "strength_band": "medium",
  "subject_scope": "self",
  "authority_override": null,
  "mutually_exclusive_with": [],
  "result": {
    "effect": "Short description of outcome.",
    "severity": "medium",
    "remedy_available": false,
    "remedy_ref_id": null
  },
  "contradiction_flag": false,
  "duplicate_candidate": false,
  "duplicate_source": null
}
```

### Key Field Rules

**`rule_id`:** `bphs2-ch{NN}-{NNN}` -- chapter zero-padded to 2 digits, sequence to 3. E.g., `bphs2-ch49-001`.

**`science_id`:** Always `"vedic_astrology"`.

**`approval_status`:**
- `"pending_human_review"` -- standard
- `"tba_needs_trigger"` -- if NLM captured an outcome but the trigger condition is unclear

**`source.sloka`:** If the NLM file includes shloka references (e.g., "49.7"), capture them. Otherwise `null`.

**`condition.type` valid values:**
`planet_in_house`, `house_lord_placement`, `yoga_combination`, `planet_conjunction`, `planet_in_sign`, `planet_affliction`, `planet_combust`, `varga_dignity_tier`, `engine_specification`

**`claim_axis` valid values:**
`health_vitality`, `career_growth`, `financial_security`, `partnership_stability`, `marriage_timing`, `spirituality`, `family_life`, `longevity`, `accident_risk`, `travel`, `creativity`, `social_network`, `general`

**`claim_scope`:**
- `"natal_trait"` -- characteristic present from birth
- `"event_timing"` -- fires at a specific dasha/transit
- `"engine_specification"` -- defines methodology

**`duplicate_candidate`:** Set `true` if this rule substantially overlaps with BPHS Vol 1 rules already decoded. Set `"duplicate_source": "bphs_vol1"`.

---

## PART 4 -- NLM Output Quality Handling

NLM .md files may have quality variations. Handle these cases:

| NLM output issue | How to handle |
|---|---|
| Rule stated clearly as "X in house Y → outcome Z" | Convert directly to JSON |
| Rule stated as narrative paragraph | Extract the condition→outcome logic; discard narrative framing |
| Table of planetary positions or dignities | → Summary.md only. Not a rule. |
| Numbered list mixing rules + tables | Separate: list items that are rules → JSON; items that are tables → Summary.md |
| Contradictory statements in same chapter | Capture both as separate rules; set `contradiction_flag: true` on both; note in Diagnostic |
| Outcome clear but trigger ambiguous | Set `approval_status: "tba_needs_trigger"`; fill what you can; tag `"tba_trigger"` |

---

## PART 5 -- Diagnostic.md Required Sections

Each chapter's Diagnostic.md must include:

```
## Ch[NN] Diagnostic

### 1. Chapter Scope
[What topic does this chapter cover? Based on NLM file.]

### 2. Rule Count
Total rules extracted: [N]
Breakdown by condition type: planet_in_house: [N] | yoga_combination: [N] | other: [N]

### 3. NLM Quality Notes
[Any issues with the NLM .md file -- missing content, narrative-heavy sections, unclear conditions]

### 4. Exclusions
[What was in the NLM file but NOT converted to rules, and why]

### 5. Contradictions
[Any rules with contradiction_flag: true -- list the pair and the NLM passage]

### 6. TBA Rules
[Rules with tba_needs_trigger -- what is known, what is missing]

### 7. Duplicate Candidates
[Any rules flagged as duplicate_candidate: true -- which BPHS Vol 1 chapter they overlap with]

### 8. Open Questions
[Anything the NLM output hints at but doesn't fully resolve]
```

---

## PART 6 -- Quality Gate Checklist

Run on every rule before finalising.

- [ ] `rule_id` format: `bphs2-ch{NN}-{NNN}` -- correct chapter, sequential
- [ ] `science_id`: `"vedic_astrology"`
- [ ] `active: true` and `checkable: true`
- [ ] `approval_status`: `"pending_human_review"` or `"tba_needs_trigger"`
- [ ] `source` block: all 7 fields present
- [ ] `condition.type`: valid value from Part 3 list
- [ ] `full_text`: no numeric coefficients -- intensity words only
- [ ] `claim_axis`: valid value from Part 3 list
- [ ] `duplicate_candidate`: `true` if overlaps with BPHS Vol 1; `duplicate_source` populated
- [ ] `contradiction_flag`: `true` if paired with a contradicting rule
- [ ] Rule count: ≥15 per chapter -- if below, flag in Diagnostic before closing
- [ ] Part files used if >25 rules (each Part file is a complete valid JSON array)
- [ ] No rules written to context window
