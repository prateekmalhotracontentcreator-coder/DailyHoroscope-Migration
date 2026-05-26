# Phaladeepika -- CC Decode Guide

> **Single authoritative reference for this thread.**
> Book: Phaladeepika -- Classic Sanskrit Parashari text (translated edition)
> Workflow: User provides NLM .md output per chapter → CC converts to Rules.json. NLM has NOT been run yet -- chapters are split and ready, NLM runs one chapter at a time as decode progresses.
> Decode AFTER BPHS Vol 1 Thread A completes -- heavy overlap expected.
> Operate autonomously chapter by chapter. No toggling to parent session required.
> Last updated: 2026-05-26

---

## 🔴 MANDATORY FIRST ACTION -- Do this NOW, before reading anything else

**Step 1:** Create the output folder and a thread-start marker file:

| # | File path | Initial content |
|---|---|---|
| 1 | `/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode/PD_ThreadStart.md` | `# Phaladeepika Decode Thread\n\nStarted: [date]. Awaiting Phase 0 + user confirmation before first chapter decode.` |

**Step 2:** Post this one line in the context window:
> "Output folder created. Reading guide and chapter PDFs for Phase 0."

**Do not create any chapter Rules.json files yet. NLM has not been run. Chapter files are created only when the user provides the NLM .md output for a specific chapter.**

---

## PHASE 0 -- Fresh Eyes Assessment

**You have split this book into chapters and can read the chapter PDFs directly. NLM has not been run yet. Read this guide fully, then read through the chapter PDFs and answer these questions based on what you find in the actual text.**

Write your answers to:
`/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode/PD_FreshEyes.md`

Answer each point in 2-5 lines. Be specific -- name chapters where relevant.

---

**1. Schema gaps**
Does this book contain condition types or rule structures NOT covered by the schema in Part 3? (e.g., rules tied to planetary war, rules involving combustion thresholds, sign-specific exceptions to house-effect rules, multi-condition chains)

**2. Dimension gaps or additions**
The guide assumes 9 dimensions per planet-in-house (appearance, health, personality, career, wealth, relationships, children, spiritual, enemies). Did you encounter dimensions this book addresses that are NOT on that list? Or dimensions it consistently skips compared to BPHS?

**3. Yoga density**
The guide covers yogas as a condition type but the rule count targets are built around house-effect chapters. Which chapters in this book are predominantly yoga chapters? Do they follow the standard [planets] → [named yoga] → [outcome] pattern, or is the structure more complex?

**4. Sloka quality**
Phaladeepika is a verse text -- sloka numbers are valuable provenance. Are shlokas clearly numbered in the chapter PDFs? Note the format used (e.g., "Ch.5.12" or "verse 12" or inline numbers). This determines whether NLM will capture them and how to populate the `source.sloka` field during conversion.

**5. BPHS overlap signal**
From scanning the chapters: where do you see the heaviest overlap with BPHS Vol 1? And where does Phaladeepika appear to give genuinely different outcomes for the same condition -- these cross-book contradictions are the highest-value findings in this decode.

**6. Chapters with zero rules**
Did you spot any chapters that are pure mythology, creation narrative, or introductory framing with no extractable rules? List them so they can be skipped.

**7. Recommended decode sequence**
There is no pre-set order for Phaladeepika -- you are the first to read this book in this thread. Based on reading the chapter PDFs, write a recommended numbered sequence covering:
- Chapters that define foundational doctrine or planetary natures (decode first -- context for all other chapters)
- House-effect chapters (the core bulk -- can these be decoded in any order, or do earlier houses reference later ones?)
- Yoga chapters (typically independent -- recommend where they slot in the sequence)
- Dasha chapters (decode after house effects and yogas)
- Chapters that are pure narrative/mythology with zero rules (list as skip)
- Any dependency chains between specific chapters

Write the complete recommended sequence as a numbered list. The user will review and confirm before NLM is run on the first chapter.

**8. Guide gaps**
Anything in this guide that is unclear, incorrect, or doesn't match what you see in this book?

---

After writing the file, post one line:
> `"Fresh Eyes written -- [N] flags raised, [N] zero-rule chapters identified. Recommended sequence in file. Awaiting your confirmation of sequence + go-ahead to begin NLM on Chapter 1."`

**Do not request NLM or begin decode until user confirms the sequence.**

---

## ⚠️ OUTPUT METHOD -- Absolute Rule

**ALL converted content goes into files via the Write tool. Zero exceptions.**
**The context window receives one-line status updates only -- nothing more.**
**Every chapter produces exactly 4 output files (Rules.json, Diagnostic.md, Summary.md, Contradictions.json).**
**JSON rules written in batches of ≤25 per Write call. Large chapters use Part files.**
**Output folder:** `/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode/`

---

## Table & Chart Handling Protocol

When a chapter contains tables, charts, or diagrams, classify each one before extracting:

| Content type | What it looks like | Action |
|---|---|---|
| **Rule-dense table** | Grid where each row/cell states a planet, house/condition, and an outcome | Extract each non-empty cell as a **separate JSON rule**. A 9×3 table = up to 27 rules -- do not compress |
| **Reference / lookup table** | Dignity tables, planetary nature lists, Nakshatra lists, sign quality data | → `Summary.md` only. Not rules |
| **Calculation procedure table** | Step-by-step computation with inputs and outputs | → `engine_specification` rule if it defines Parashari methodology; `Summary.md` if pure reference |
| **Visual chart / diagram** | Rasi wheel, house diagram, dasha timeline visual | → Note in Diagnostic only: "Chapter contains [type] -- visual content, not extractable as rules." Zero rule extraction |

**The test:** Does each row or cell state a condition **and** an outcome? Yes → rules. No → `Summary.md`.

---

## Chapter Conversion Protocol -- Execute for EVERY chapter

### Step 1 -- Create output files (Write tool × 4)
- `PD_Ch{NN}_{ShortTitle}_Rules.json` → `[]`
- `PD_Ch{NN}_{ShortTitle}_Diagnostic.md` → placeholder
- `PD_Ch{NN}_{ShortTitle}_Summary.md` → placeholder
- `PD_Ch{NN}_{ShortTitle}_Contradictions.json` → `[]`

### Step 2 -- Context window: one line only
> `"4 files created for Ch[NN]. Beginning conversion."`

### Step 3 -- Receive and read the NLM .md file for this chapter

The user runs NLM on one chapter at a time and provides the .md output to this thread.
**Do not proceed to Step 4 until the user provides the NLM .md for this chapter.**
Post: `"Ready for Ch[NN] NLM output."` and wait.

### Step 4 -- Classify the NLM content

| Content type | Action |
|---|---|
| Rules in format "[Planet] in [House] → [Outcome]" | → Full JSON rule |
| Combination rules (multiple planets) | → Full JSON rule with `condition.type: "yoga_combination"` |
| Dasha-based timing rules | → Full JSON rule with `claim_scope: "event_timing"` |
| Lookup tables (planetary natures, sign lists, dignity tables) | → Summary.md only. Not rules. |
| Mythological / cosmological narrative | → Summary.md only. Not rules. |
| Methodology / calculation procedures | → Rule with `claim_scope: "engine_specification"` |
| Example charts / named horoscopes | → Diagnostic.md benchmark section only. Zero rules. |

### Step 5 -- Dedup pass (CRITICAL for this book)
Before finalising each chapter's rules, check against BPHS Vol 1 decode:
- BPHS Vol 1 output folder: `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/`
- If a rule in this chapter is substantively identical to a BPHS Vol 1 rule → set `duplicate_candidate: true, duplicate_source: "bphs_vol1"`
- If a rule contradicts a BPHS Vol 1 rule on the same condition → set `contradiction_flag: true` and log in Diagnostic under "Cross-Book Contradictions"

### Step 6 -- Write JSON Rules (batched -- ≤25 per Write call)

### Step 7 -- Write Contradictions.json

### Step 8 -- Write Summary.md

### Step 9 -- Write Diagnostic.md

### Step 10 -- Context window: one line only
> `"Ch[NN] complete. [N] rules. [N] duplicates flagged. [N] contradictions. Proceeding to Ch[NN+1]."`

**Rule count expectation: 30-60 rules per house chapter.**
If actual count below 20: Post flag -- "LOW YIELD -- NLM output may have summarised rules as narrative. Flag for user before proceeding to next chapter."

---

## PART 1 -- Project Identity

| Field | Value |
|---|---|
| Book | Phaladeepika (classic Sanskrit Parashari text -- translated edition) |
| `book_id` | `phaladeepika_20260526` |
| `science_id` | `vedic_astrology` |
| `checkable` | `true` |
| Astrological system | Classical Parashari Vedic Astrology (same tradition as BPHS) |
| Source PDF | `/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika/phaladeepika.pdf` |
| NLM workflow | User runs NLM one chapter at a time and provides output to CC thread on request |
| Output folder | `/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode/` |
| Decode method | NLM → CC Conversion |
| Rule ID prefix | `pd-ch{NN}-{NNN}` |
| Related books | BPHS Vol 1 (same Parashari tradition -- heavy overlap expected) |

### Why Phaladeepika After BPHS Vol 1

Phaladeepika is written in the same Parashari tradition as BPHS. It covers planetary natures, house effects, yogas, dashas, and special combinations -- topics that heavily overlap with BPHS Vol 1. The dedup pass (Step 5 above) is critical. Phaladeepika's unique value is:
- Different framing of the same rules (complements BPHS wording)
- Phaladeepika-specific rules not found in BPHS (capture fully, no dedup flag)
- Direct contradictions with BPHS on the same condition (highest value -- flag clearly)

---

## PART 2 -- Vedic System Primer

**Houses (Bhavas):** 12 houses numbered from Ascendant (Lagna = 1st).
- Kendras (Angular): 1, 4, 7, 10
- Trikonas (Trine): 1, 5, 9
- Dusthanas (Malefic): 6, 8, 12
- Upachayas (Growing): 3, 6, 10, 11

**Planets:** Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu
- Natural Benefics: Jupiter, Venus, Mercury (waxing), Moon (waxing)
- Natural Malefics: Sun, Mars, Saturn, Rahu, Ketu

**Functional benefic/malefic** depends on house lordship for a specific Lagna.

**Yogas:** Named combinations of planets. Examples: Gajakesari (Jupiter-Moon), Budhaditya (Sun-Mercury), Raja Yogas (Kendra-Trikona lord conjunction). Capture each yoga as its own rule.

**Dashas:** Vimshottari dasha system -- planetary periods in fixed order: Ketu (7y), Venus (20y), Sun (6y), Moon (10y), Mars (7y), Rahu (18y), Jupiter (16y), Saturn (19y), Mercury (17y).

---

## PART 3 -- Full KE Schema

```json
{
  "rule_id": "pd-ch05-001",
  "science_id": "vedic_astrology",
  "active": true,
  "approval_status": "pending_human_review",
  "checkable": true,
  "source": {
    "book": "Phaladeepika",
    "book_id": "phaladeepika_20260526",
    "chapter": 5,
    "chapter_name": "[Exact chapter title from chapter PDF]",
    "sloka": "5.12",
    "batch_id": "pd-ch05-v1-20260526",
    "passage_ref_id": null
  },
  "title": "Moon in 7th House -- Charming Spouse",
  "summary": "Moon in the 7th house gives a charming, attractive spouse and harmonious partnership.",
  "full_text": "When the Moon occupies the 7th house, the native is blessed with a charming, fair, and emotionally expressive spouse. The partnership is generally harmonious. The native may be inclined toward more than one relationship.",
  "tags": ["moon", "7th_house", "spouse", "relationships", "marriage"],
  "category": "house_effects",
  "condition": {
    "type": "planet_in_house",
    "planet": "moon",
    "house": 7,
    "sign": null,
    "nakshatra": null,
    "strength_requirement": null,
    "dasha_lord": null,
    "antardasha_planet": null,
    "applies_to_all_dasha_lords": false
  },
  "claim_axis": "partnership_stability",
  "claim_scope": "natal_trait",
  "claim_polarity": "positive",
  "timing_bias": "sustained",
  "strength_band": "medium",
  "subject_scope": "spouse",
  "authority_override": null,
  "mutually_exclusive_with": [],
  "result": {
    "effect": "Charming, attractive spouse; harmonious partnership; possible inclination toward multiple relationships.",
    "severity": "medium",
    "remedy_available": false,
    "remedy_ref_id": null
  },
  "contradiction_flag": false,
  "duplicate_candidate": true,
  "duplicate_source": "bphs_vol1"
}
```

### Field-by-Field Rules

**`rule_id`:** `pd-ch{NN}-{NNN}` -- chapter zero-padded to 2 digits, sequence to 3.

**`science_id`:** Always `"vedic_astrology"`.

**`checkable`:** Always `true` for Phaladeepika.

**`approval_status`:** Always `"pending_human_review"`. Use `"tba_needs_trigger"` if trigger condition is unclear from NLM output.

**`source.sloka`:** If the NLM file includes shloka references (e.g., "5.12"), capture them. Otherwise `null`. Phaladeepika is a verse text -- sloka references are highly valuable.

**`condition.type` valid values:**
- `"planet_in_house"` -- most house-effect rules
- `"house_lord_placement"` -- lord of house X placed in house Y
- `"yoga_combination"` -- named multi-planet combination
- `"planet_conjunction"` -- two or more planets in same house
- `"planet_in_sign"` -- planet in a specific zodiac sign
- `"planet_affliction"` -- aspected/conjoined by malefic
- `"planet_combust"` -- within Sun's combustion range
- `"dasha_period"` -- rule fires during a specific planet's dasha
- `"varga_dignity_tier"` -- rule based on divisional chart dignity

**`claim_axis` valid values:**
`health_vitality`, `career_growth`, `financial_security`, `partnership_stability`, `marriage_timing`, `spirituality`, `family_life`, `longevity`, `accident_risk`, `travel`, `creativity`, `social_network`, `general`

**`subject_scope`:** `self` / `spouse` / `children` / `father` / `mother` / `siblings`

**`duplicate_candidate`:** `true` if this rule is substantially the same as a BPHS Vol 1 rule. Set `"duplicate_source": "bphs_vol1"`. Still capture the rule fully -- dedup arbitration happens at ingest.

**`contradiction_flag`:** `true` if this rule contradicts:
1. Another rule in the same Phaladeepika chapter (same condition, opposite outcome)
2. A BPHS Vol 1 rule on the same condition (cross-book contradiction -- highest value)
Log both types in Contradictions.json.

---

## PART 4 -- Multi-Dimension Extraction (CRITICAL)

For each planet-in-house combination, extract a SEPARATE rule for each distinct dimension addressed in the text.

| Dimension | Example tag | claim_axis |
|---|---|---|
| Physical appearance | `appearance` | `health_vitality` |
| Health / ailments | `health` | `health_vitality` |
| Personality / character | `personality` | `general` |
| Career / profession | `career` | `career_growth` |
| Wealth / finances | `wealth` | `financial_security` |
| Spouse / relationships | `relationships` | `partnership_stability` |
| Children | `children` | `family_life` |
| Spiritual / dharmic | `spiritual` | `spirituality` |
| Enemies / adversaries | `enemies` | `social_network` |

**Rule count target per house chapter: 30-60 rules.**
(9 planets × ~5 dimensions average = 45 minimum for a full house chapter.)

Do NOT merge. "Jupiter in 9th gives wealth, wisdom, and pious father" = 3 separate rules.

---

## PART 5 -- Yoga Rules (Multi-Planet Combinations)

When a chapter contains YOGA conditions (multiple planets involved, not a single planet-in-house):

```json
{
  "rule_id": "pd-ch08-017",
  "condition": {
    "type": "yoga_combination",
    "planets_involved": ["jupiter", "moon"],
    "yoga_name": "Gajakesari Yoga",
    "configuration": "Jupiter and Moon in mutual Kendra from each other"
  },
  "tags": ["gajakesari_yoga", "jupiter", "moon", "kendra", "wealth"],
  "category": "yoga_effects"
}
```

- List ALL planets involved in `planets_involved`
- Capture the yoga name in `yoga_name` if given
- Add the yoga name in snake_case to `tags`
- `claim_scope`: `"natal_trait"` for yogas that describe character/promise; `"event_timing"` for timing yogas

---

## PART 6 -- Contradictions.json Format

```json
{
  "contradiction_id": "PD_Ch05_C01",
  "chapter": 5,
  "scope": "within_book",
  "condition": "Moon in 7th house",
  "rule_a_shloka": "5.12",
  "outcome_a": "Charming, devoted spouse",
  "rule_b_shloka": "5.28",
  "outcome_b": "Multiple relationships, unstable marriage",
  "resolution": "strength_dependent",
  "cross_book_note": null
}
```

For **cross-book contradictions** (Phaladeepika vs BPHS Vol 1):

```json
{
  "contradiction_id": "PD_Ch05_XB01",
  "chapter": 5,
  "scope": "cross_book",
  "condition": "Mars in 7th house",
  "rule_a_shloka": "5.15",
  "outcome_a": "Phaladeepika: Quarrelsome spouse, marital strife",
  "rule_b_shloka": null,
  "outcome_b": "BPHS Vol 1 Ch18: Courageous spouse, active partner",
  "resolution": "unresolved",
  "cross_book_note": "Phaladeepika and BPHS differ on Mars-7th outcome. Flag for human arbitration."
}
```

**`scope`:** `"within_book"` or `"cross_book"`
**`resolution`:** `"context_dependent"` / `"strength_dependent"` / `"unresolved"`

---

## PART 7 -- Diagnostic.md Required Sections

```
## Ch[NN] Diagnostic

### 1. Chapter Scope
[What topic does this chapter cover?]

### 2. Rule Count
Total: [N] | Unique to Phaladeepika: [N] | Duplicates of BPHS Vol 1: [N]
Breakdown by condition type: planet_in_house: [N] | yoga_combination: [N] | other: [N]

### 3. NLM Output Notes
[Quality of the NLM .md provided for this chapter -- narrative-heavy sections, missing sloka refs, unclear conditions, judgement calls made during conversion]

### 4. Exclusions
[Content NOT converted to rules, and why]

### 5. Within-Book Contradictions
[Rules with contradiction_flag: true within this chapter]

### 6. Cross-Book Contradictions (Phaladeepika vs BPHS Vol 1)
[Rules that contradict BPHS Vol 1 on the same condition -- highest value findings]

### 7. Duplicate Candidates
[Rules flagged as duplicate_candidate: true -- confirm they match BPHS Vol 1 rules]

### 8. TBA Rules
[Rules with tba_needs_trigger -- outcome known, trigger unclear]

### 9. Open Questions
[Anything the NLM output hints at but doesn't fully resolve]
```

---

## PART 8 -- Quality Gate Checklist

- [ ] `rule_id` format: `pd-ch{NN}-{NNN}` -- correct chapter, sequential
- [ ] `science_id`: `"vedic_astrology"`
- [ ] `active: true` and `checkable: true`
- [ ] `approval_status`: `"pending_human_review"` or `"tba_needs_trigger"`
- [ ] `source` block: all 7 fields present; `sloka` captured where visible
- [ ] `condition.type`: valid value from Part 3 list
- [ ] `full_text`: no numeric coefficients -- intensity words only
- [ ] Multi-dimension: each distinct life dimension is a separate rule (not merged)
- [ ] Yoga rules: `condition.type: "yoga_combination"`, `planets_involved` array populated
- [ ] `duplicate_candidate`: dedup pass against BPHS Vol 1 completed per chapter
- [ ] `contradiction_flag`: `true` for within-book and cross-book contradictions
- [ ] Contradictions.json populated for all `contradiction_flag: true` rules
- [ ] Rule count: ≥30 rules per house chapter -- if below, flag in Diagnostic before closing
- [ ] No rules written to context window

---

## PART 9 -- Known Issues to Avoid

1. **Context window overflow:** Never write rule arrays to context window. Write tool only.

2. **Dedup fatigue:** After many chapters, the dedup pass may feel repetitive. Do not skip it. Cross-book contradictions (Phaladeepika vs BPHS) are the highest-value findings in this decode.

3. **Sloka capture:** Phaladeepika is a verse text. Sloka references (e.g., "Ch.5, v.12") give the engine precise provenance. Capture from either the NLM output or the source PDF if NLM drops them.

4. **Dimension merging:** The most common under-extraction error. Do not merge personality + career + health into one rule.

5. **NLM narrative absorption:** Phaladeepika includes explanatory commentary around each verse. NLM may summarise commentary rather than extract the core rule. If rule count is low, re-read NLM output for rules buried in explanatory paragraphs.

6. **Nodes (Rahu/Ketu):** Phaladeepika may give conflicting outcomes for nodes in different chapters. Capture all -- flag contradictions. Do not arbitrate.
