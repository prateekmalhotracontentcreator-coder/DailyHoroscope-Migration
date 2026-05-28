# KE -- Your Destiny Is In Your Name & DOB: Full Book Decode Guide

> **Single authoritative reference for the CC thread decoding this book.**
> Operate autonomously chapter by chapter. No toggling back to the parent session required.
> Last updated: 2026-05-18 | Status: Not started

---

## **🔴 MANDATORY FIRST ACTION -- Do this NOW, before reading anything else**

**Do not read this guide yet. Do not begin decoding. Execute these Write tool calls first -- one per file:**

Create all 4 output files for Chapter 3:

| # | File path | Initial content |
|---|---|---|
| 1 | `/Users/apple/Documents/Knowledge Engine_eBooks/DestinyNumerology_CC_Decode/Numerology_Ch03_Calculations_Rules.json` | `[]` |
| 2 | `/Users/apple/Documents/Knowledge Engine_eBooks/DestinyNumerology_CC_Decode/Numerology_Ch03_Calculations_DataTables.md` | `# Ch3 Data Tables\n\n[Writing in progress]` |
| 3 | `/Users/apple/Documents/Knowledge Engine_eBooks/DestinyNumerology_CC_Decode/Numerology_Ch03_Calculations_Summary.md` | `# Ch3 Technical Summary\n\n[Writing in progress]` |
| 4 | `/Users/apple/Documents/Knowledge Engine_eBooks/DestinyNumerology_CC_Decode/Numerology_Ch03_Calculations_Diagnostic.md` | `# Ch3 Chapter Diagnostic\n\n[Writing in progress]` |

**Then post this one line in the context window:**
> "4 files created for Ch3. Reading guide now."

**This is non-negotiable.** All 4 files must exist on disk before any decoding begins. Every chapter gets its own 4 files created the same way before decoding starts. This keeps the thread alive through the full book.

---

> ## **⚠️ OUTPUT METHOD -- Zero Tolerance Rule**
> **DO NOT write any decoded content into the context window. Not a single rule. Not a single JSON block. Not a summary. Nothing.**
> **The only text permitted in the context window is one short status line per chapter (see Chapter Start Protocol below).**
> **Every chapter produces exactly 4 output files. Each file is written separately via the Write tool.**
> **JSON rules are written in batches of ≤25 rules per Write call. Never attempt to write more than 25 rules in one call.**
> **Reason: the 32,000 token output limit is hit instantly when large chapters (Ch4, Ch9, Ch16) are written in one pass. Batching is mandatory.**
> **Output folder:** `/Users/apple/Documents/Knowledge Engine_eBooks/DestinyNumerology_CC_Decode/`
> **File naming:** `Numerology_Ch{NN}_{ShortTitle}_{Type}.json/.md` -- see Part 3.5 for full spec.

---

## Chapter Start Protocol -- Execute at the start of EVERY chapter

### Step 1 -- Create all 4 output files (Write tool × 4)

Before reading the PDF, create placeholder files:
- `Numerology_Ch{NN}_{ShortTitle}_Rules.json` → initial content: `[]`
- `Numerology_Ch{NN}_{ShortTitle}_DataTables.md` → initial content: `# Ch{NN} Data Tables\n\n[Writing in progress]`
- `Numerology_Ch{NN}_{ShortTitle}_Summary.md` → initial content: `# Ch{NN} Technical Summary\n\n[Writing in progress]`
- `Numerology_Ch{NN}_{ShortTitle}_Diagnostic.md` → initial content: `# Ch{NN} Chapter Diagnostic\n\n[Writing in progress]`

### Step 2 -- Context window: one line only
> `"4 files created for Ch[NN]. Beginning decode."`

### Step 3 -- Read the PDF fully before writing any content

### Step 4 -- Write DataTables file (single Write call)
All data tables for the chapter in one pass. Data tables are compact -- this will not hit the output limit.

### Step 5 -- Write JSON Rules file (batched -- CRITICAL)

**⚠️ NEVER write more than 25 rules in a single Write tool call.**

- **Small chapters (≤25 rules):** Write the complete JSON array in one call → `Numerology_Ch{NN}_{ShortTitle}_Rules.json`
- **Large chapters (>25 rules):** Write in part files -- each part is a complete, valid JSON array:
  - Part 1 → `Numerology_Ch{NN}_{ShortTitle}_Rules_Part1.json` (rules 001-025)
  - Part 2 → `Numerology_Ch{NN}_{ShortTitle}_Rules_Part2.json` (rules 026-050)
  - Part 3 → `Numerology_Ch{NN}_{ShortTitle}_Rules_Part3.json` (rules 051-075)
  - Continue until all rules are written

**Large chapters that MUST use Part files:** Ch4 (~108 rules), Ch9 (61 rules), Ch16 (~81 rules).

### Step 6 -- Write Summary file (single Write call, ≤10 lines)

Cap the Summary at:
- Chapter scope: 1 sentence
- Content extracted: 3-5 bullet points
- Total rules: N | Total data tables: N | Batch ID: `num-ch{NN}-v1-YYYYMMDD`

### Step 7 -- Write Diagnostic file (single Write call)
Quality gate results + benchmark test cases + any issues flagged.

### Step 8 -- Context window: one line only
> `"Ch[NN] complete. [N] rules across [N] part files. [N] tables. Proceeding to Ch[NN+1]."`

**That is all that ever appears in the context window. Two lines per chapter. Nothing else. Ever.**

---

## PART 1 -- Project Identity

| Field | Value |
|---|---|
| Book | Your Destiny Is In Your Name & DOB |
| `book_id` | `destiny_numerology_v1_20260518` |
| `science_id` | `numerology` |
| System | Chaldean / Pythagorean / Lo Shu Grid (Chinese) -- hybrid numerology |
| PDF root | `/Users/apple/Documents/Knowledge Engine_eBooks/5. YOUR DESTINY IS IN YOUR NAME & DOB/` |
| Output folder | `/Users/apple/Documents/Knowledge Engine_eBooks/DestinyNumerology_CC_Decode/` |
| Target collection | MongoDB: `interpretation_rules` |
| Parent process doc | `/Users/apple/DailyHoroscope-Migration/KE_Book_Decode_Process_Technical.md` |

### ⚠️ Science System Isolation

`science_id: "numerology"` -- this is a numerology system, completely separate from `"kp_jyotish"` and `"vedic_astrology"`. These systems must never be mixed. No planetary dasha logic, no house signification, no sub-lord system applies here.

---

## PART 2 -- Numerology System Primer

### Three Primary Number Types

| Number | Calculation | Significance |
|---|---|---|
| **Basic Number** | Reduce birth day to single digit (e.g., 28 → 2+8 = 10 → 1+0 = 1) | Core personality, primary traits |
| **Destiny Number** | Sum ALL digits of full DOB (DD+MM+YYYY) to single digit | Life path, overall destiny |
| **Kua Number** | Male: 11 − year_sum; Female: 4 + year_sum | Feng Shui / directional luck |

**Exception:** Numbers 10, 20, 30 are NOT reduced further -- they carry distinct compound meanings.

### Planetary Rulers of Numbers 1-9

| Number | Planet | Key Traits |
|---|---|---|
| 1 | Sun | Leadership, authority, independence |
| 2 | Moon | Sensitivity, intuition, cooperation |
| 3 | Jupiter | Optimism, creativity, expansion |
| 4 | Rahu | Unconventional, hardworking, rebellious |
| 5 | Mercury | Versatile, communicative, restless |
| 6 | Venus | Harmony, beauty, relationships |
| 7 | Ketu | Spiritual, introspective, mystical |
| 8 | Saturn | Discipline, karma, materialism |
| 9 | Mars | Courage, aggression, leadership |

### Compound Numbers (10-70)

Each two-digit number from 10 to 70 carries a distinct meaning before reduction. These are NOT the same as the single-digit result. Always evaluate compound number FIRST, then the reduced single digit. Total: 61 compound number profiles.

### Lo Shu Grid -- 3×3 Magic Square

```
4 | 9 | 2
---------
3 | 5 | 7
---------
8 | 1 | 6
```

Each cell = one number (1-9). Numbers present in a person's DOB are placed in the grid. Numbers absent = missing numbers. Three types of analysis:
- **Arrows (complete rows/columns/diagonals)** = strengths
- **Missing arrows** = weaknesses
- **Rajayoga** = special combinations indicating success

### 81 Combinations Matrix

Every Basic Number (1-9) × Destiny Number (1-9) = 81 compatibility/synergy pairs, each rated 1-5 stars. This is a lookup table AND a set of diagnostic rules -- the star rating is data, the interpretation text is a rule.

### The 3-Layer Diagnostic Framework

- **Layer 1 (Foundation):** Definitions, calculation methods, number assignments
- **Layer 2 (Diagnostic):** Number characteristics, compound meanings, Lo Shu arrows, 81 combinations
- **Layer 3 (Correction):** Name correction, number optimisation, gemstone recommendations, remedies

---

## PART 3 -- Full KE Schema for Numerology

```json
{
  "rule_id": "num-ch04-001",
  "science_id": "numerology",
  "active": true,
  "approval_status": "pending_human_review",
  "checkable": false,
  "source": {
    "book": "Your Destiny Is In Your Name & DOB",
    "book_id": "destiny_numerology_v1_20260518",
    "chapter": 4,
    "chapter_name": "Characteristics of Numbers 1 to 9",
    "sloka": null,
    "batch_id": "num-ch04-v1-20260518",
    "passage_ref_id": null
  },
  "title": "Number 1 -- Core Leadership Trait",
  "summary": "Persons with Basic Number 1 exhibit strong leadership and independent authority.",
  "full_text": "Number 1, ruled by the Sun, confers natural leadership, self-reliance, and the drive to be first. These individuals resist subordination and are most effective in roles of authority and independent initiative.",
  "tags": ["diagnostic", "basic_number", "number_1", "sun", "leadership"],
  "category": "numerology_diagnostic",
  "condition": {
    "type": "basic_number_trait",
    "numerology_layer": "diagnostic",
    "number_type": "basic",
    "numbers_involved": [1],
    "lagna_modality": null,
    "badhaka_house": null,
    "maraka_houses": null
  },
  "claim_axis": "personality",
  "claim_scope": "natal_trait",
  "claim_polarity": "positive",
  "timing_bias": "sustained",
  "strength_band": "high",
  "result": {
    "effect": "Strong leadership drive, difficulty accepting subordination",
    "severity": null,
    "aayu_bucket": null,
    "number_outcome": "leadership",
    "correction_type": null,
    "remedy_available": false,
    "remedy_ref_id": null
  }
}
```

### Field-by-Field Rules

**`rule_id`**
Format: `num-ch{NN}-{NNN}` -- "num" prefix for numerology, chapter zero-padded to 2 digits, sequence to 3.
Examples: `num-ch04-001`, `num-ch16-081`

**`science_id`**
Always `"numerology"`. Never `"kp_jyotish"` or `"vedic_astrology"`.

**`active`** -- Always `true`

**`approval_status`** -- Always `"pending_human_review"`

**`checkable`** -- Always `false`

**`source` block -- all 7 fields required:**
- `book`: "Your Destiny Is In Your Name & DOB"
- `book_id`: "destiny_numerology_v1_20260518"
- `chapter`: integer
- `chapter_name`: exact chapter title from PDF
- `sloka`: `null`
- `batch_id`: `"num-ch{NN}-v1-20260518"`
- `passage_ref_id`: `null`

**`category`**
- `"numerology_foundation"` -- calculation methods, definitions
- `"numerology_diagnostic"` -- number characteristics, compound meanings, Lo Shu arrows, 81 combinations
- `"numerology_correction"` -- name correction, number optimisation, gemstone, remedy

**`condition` block -- all fields required:**

| Field | Values |
|---|---|
| `type` | `"basic_number_trait"` / `"destiny_number_trait"` / `"compound_number"` / `"lo_shu_arrow"` / `"compatibility_pair"` / `"name_correction"` / `"calculation_method"` / `"engine_specification"` |
| `numerology_layer` | `"foundation"` / `"diagnostic"` / `"correction"` |
| `number_type` | `"basic"` / `"destiny"` / `"kua"` / `"name"` / `"compound"` / `"lo_shu"` / `null` |
| `numbers_involved` | Array of numbers relevant to the rule e.g. `[1]`, `[4, 8]`, `[1, 9]` -- or `null` |
| `lagna_modality` | Always `null` for numerology |
| `badhaka_house` | Always `null` for numerology |
| `maraka_houses` | Always `null` for numerology |

**`claim_axis`**
- `"personality"` -- character traits, strengths, weaknesses
- `"compatibility"` -- number pair interactions
- `"correction"` -- name, phone, house number optimisation
- `"timing"` -- year/period-specific predictions
- `"world_events"` -- wars, disasters, nations (Ch19-25)
- `"general"` -- engine specifications only

**`claim_polarity`**
- `"positive"` -- favourable, auspicious, strengthening
- `"negative"` -- unfavourable, challenging, weakening
- `"neutral"` -- informational / definitional
- `"conditional"` -- depends on context or other numbers

**`strength_band`**
Words only: `"extreme"` / `"high"` / `"medium"` / `"low"`

**`result` block -- all 7 fields required:**

| Field | Rule |
|---|---|
| `effect` | Plain description of outcome |
| `severity` | `null` for foundation rules; `"extreme"/"high"/"medium"/"low"` for outcome rules |
| `aayu_bucket` | Always `null` -- longevity not in scope here |
| `number_outcome` | Short keyword: `"leadership"` / `"financial_gain"` / `"spiritual"` / `"conflict"` / `"correction_needed"` / `"auspicious"` / `null` |
| `correction_type` | `"name"` / `"mobile"` / `"house"` / `"company"` / `"gemstone"` / `null` |
| `remedy_available` | `true` if text explicitly states a remedy; otherwise `false` |
| `remedy_ref_id` | `null` |

---

## PART 3.5 -- Output File Structure Per Chapter

Every chapter produces exactly 4 file types. File priorities: **JSON Rules first, Diagnostic second, DataTables third, Summary last.**

### File naming

| File | Naming | Format | Priority |
|---|---|---|---|
| JSON Rules | `Numerology_Ch{NN}_{ShortTitle}_Rules.json` | Valid JSON array | 🔴 Highest |
| Chapter Diagnostic | `Numerology_Ch{NN}_{ShortTitle}_Diagnostic.md` | Markdown | 🟠 High |
| Data Tables | `Numerology_Ch{NN}_{ShortTitle}_DataTables.md` | Markdown | 🟡 Medium |
| Technical Summary | `Numerology_Ch{NN}_{ShortTitle}_Summary.md` | Markdown (≤10 lines) | 🟢 Low |

### Part file naming (large chapters only)

When a chapter has >25 rules, use numbered part files instead of a single rules file:

```
Numerology_Ch04_Characteristics_Rules_Part1.json   ← rules 001-025
Numerology_Ch04_Characteristics_Rules_Part2.json   ← rules 026-050
Numerology_Ch04_Characteristics_Rules_Part3.json   ← rules 051-075
Numerology_Ch04_Characteristics_Rules_Part4.json   ← rules 076-100
Numerology_Ch04_Characteristics_Rules_Part5.json   ← rules 101-108
```

Each part file is a **complete, valid JSON array** `[{...}, {...}]` -- not a fragment. The ingest pipeline processes all part files matching `*_Rules_Part*.json`.

### Chapter output size estimates

| Chapter | Est. Rules | Parts needed | Est. total files |
|---|---|---|---|
| Ch3 (Calculations) | ~12 | None | 4 |
| Ch4 (Characteristics) | ~108 | 5 parts | 8 |
| Ch9 (Compound Numbers) | ~61 | 3 parts | 6 |
| Ch16 (81 Combinations) | ~81 | 4 parts | 7 |
| Ch6, Ch5, Ch7, Ch13, Ch14 | 10-20 each | None | 4 each |
| Correction chapters (Ch10-12, Ch17) | 9-20 each | None | 4 each |

---

## PART 4 -- Critical Distinction: Rules vs. Data Tables

### Goes into DATA TABLES (not rules):

| Content | Table Name |
|---|---|
| Alphabet A-Z → number assignments | Table 8.1: Alphabet Number Chart |
| Number 1-9 → planetary ruler | Table 4.1: Number-Planet Assignment |
| Lo Shu Grid layout (3×3 positions) | Table 6.1: Lo Shu Grid Reference |
| 81 Combinations star ratings (the scores only) | Table 16.1: 81 Combinations Matrix |
| Compound numbers 10-70 titles only | Table 9.1: Compound Number Index |
| Friends / Non-Friends / Neutral number pairs | Table 5.1: Number Compatibility Reference |
| Gemstone → number assignments | Table 17.1: Gemstone-Number Chart |
| Donation items for missing numbers | Table 18.1: Donation Remedies Reference |
| Country / City / State name numbers | Table 23-25: Geographic Number Reference |

### Goes into JSON RULES (diagnostic logic):

| Content | Example |
|---|---|
| Number characteristic descriptions | "Number 4 persons face unusual obstacles from authorities" |
| Sub-date variations | "Born on 13th = 4 with Mars influence -- more aggressive than standard 4" |
| Lo Shu arrow interpretations | "Arrow of Determination (1-5-9) = strong willpower, completes tasks" |
| 81 combination interpretations | "Basic 1, Destiny 8 -- powerful but prone to arrogance conflicts" |
| Compound number meanings | "Number 16 -- Tower struck by lightning; sudden reversals; spiritual test" |
| Name correction conditions | "If Destiny is 8, avoid name numbers 4 or 8 -- doubles Saturn burden" |
| Missing number implications | "Missing 5 = communication difficulties, restlessness in career" |
| Repeat number implications | "Three 1s in grid = extreme ego, isolation risk" |
| Gemstone prescription rules | "Destiny 1 → Ruby strengthens Sun energy" |

---

## PART 5 -- Chapter Map, Priority & Expectations

| Priority | Ch | File | Topic | Content Type | Est. Rules |
|---|---|---|---|---|---|
| 1 | 3 | `3_Basic number...pdf` | Calculation methods (Basic, Destiny, Kua) | Foundation rules + formulas | 12 |
| 2 | 4 | `4_Characteristics of numbers 1 to 9.pdf` | Core personality diagnostics | Diagnostic rules | 72 |
| 3 | 9 | `9_Compound numbers from 10 to 70.pdf` | Compound number profiles | Diagnostic rules | 61 |
| 4 | 16 | `16_81 Combinations.pdf` | Basic × Destiny compatibility matrix | Diagnostic rules + data table | 81 |
| 5 | 6 | `6_Lo Shu Grid...pdf` | Grid arrows, Rajayoga, deficiencies | Diagnostic rules | 15 |
| 6 | 5 | `5_Friends, Non-Friends...pdf` | Number relationship types | Data table + rules | 20 |
| 7 | 7 | `7_Calculation of Lucky numbers.pdf` | Lucky number derivation | Foundation rules | 10 |
| 8 | 13 | `13_Repeat Numbers...pdf` | Repeated digit implications | Diagnostic rules | 15 |
| 9 | 14 | `14_Missing numbers...pdf` | Missing digit implications | Diagnostic rules | 15 |
| 10 | 10 | `10_Prefect Name Correction...pdf` | Name correction rules | Correction rules | 20 |
| 11 | 11 | `11_Mobile number...pdf` | Mobile/bank number correction | Correction rules | 10 |
| 12 | 12 | `12_House number...pdf` | House/shop number correction | Correction rules | 10 |
| 13 | 17 | `17_Gemstone Numerology.pdf` | Gemstone prescriptions | Correction rules | 9 |
| 14 | 8 | `8_Alphabet numbers...pdf` | A-Z number values | Data table only | 0 rules |
| 15 | 18 | `18_Donations...pdf` | Donation remedies | Remedy reference | 0 rules |
| 16 | 28 | `28_Remarriage...pdf` | Remarriage number conditions | Diagnostic rules | 10 |
| Park | 19-25 | Wars, Cyclones, Nations, Cities | World events / geopolitical | Context-dependent | TBD |
| Park | 26-27 | Company numbers / logos | Business numerology | Diagnostic rules | TBD |
| Benchmark | 15 | `15_Comprehensive...pdf` + 50 sub-files | 50 celebrity charts | Case studies -- zero rules | 0 |
| Skip | 1 | `1_Introduction...pdf` | Philosophy / origin | Narrative | 0 |
| Skip | 2 | `2_Qualities to become a Numerologist.pdf` | Career advice | Narrative | 0 |

**Total estimated rules: 350-400 across all chapters**

### Chapter 4 -- Sub-Date Variations (important)

Each of the 9 base numbers has multiple birth-date sub-variants. Treat each sub-date as a separate rule:
- Number 1: born on 1st, 10th, 19th, 28th → 4 variants
- Number 2: born on 2nd, 11th, 20th, 29th → 4 variants
- (and so on for 3-9)

That gives ~36 sub-date rules ON TOP of the 9 base number rules. Extract all of them.

### Chapter 16 -- 81 Combinations

The matrix has some cells marked "?" (undefined). Extract only cells with actual content. For each pair, the star rating goes in the Data Table; the interpretation text becomes the rule. If a cell is undefined, skip it.

---

## PART 6 -- Quality Gate Checklist

Run on every rule before writing to file.

### Schema Checks

- [ ] `rule_id` format: `num-ch{NN}-{NNN}`
- [ ] `science_id` is `"numerology"` -- not `"kp_jyotish"`, not `"vedic_astrology"`
- [ ] `active: true` present
- [ ] `approval_status: "pending_human_review"` present
- [ ] `checkable: false` present
- [ ] `source` block has all 7 fields including `sloka: null` and `passage_ref_id: null`
- [ ] `condition` block has all 7 fields -- `lagna_modality`, `badhaka_house`, `maraka_houses` always `null`
- [ ] `result` block has all 7 fields including `number_outcome` and `correction_type`
- [ ] `aayu_bucket` is always `null`

### Content Checks

- [ ] Alphabet chart (A-Z values) is in Data Table, not rules
- [ ] 81 Combinations star ratings are in Data Table; interpretation text is a rule
- [ ] Foundation/calculation rules: `severity: null`, `number_outcome: null`
- [ ] Correction rules: `correction_type` populated
- [ ] Sub-date variants extracted as separate rules (not merged into base number rule)
- [ ] Compound numbers 10-70 each get their own rule
- [ ] No numeric scoring in `full_text` -- use intensity words
- [ ] Celebrity charts logged as benchmarks, not decoded as rules
- [ ] Chapters 1 and 2 skipped (narrative only)

### Delivery Checks

- [ ] Output written to file, NOT to context window
- [ ] 4 separate files created for the chapter before decoding starts
- [ ] JSON rules written in batches of ≤25 per Write call
- [ ] Large chapters (>25 rules) use Part files (`_Part1.json`, `_Part2.json` etc.)
- [ ] Each part file is a complete, valid JSON array (not a fragment)
- [ ] Status confirmation in context window only -- two lines per chapter maximum
- [ ] Summary file is ≤10 lines

---

## PART 7 -- Exclusions Protocol

| Type | Action |
|---|---|
| A-Z alphabet table | Data Table only |
| Number-planet assignments | Data Table only |
| Narrative/philosophy (Ch1, Ch2) | Skip entirely |
| 50 celebrity charts (Ch15 + sub-files) | Benchmark log only -- zero rules |
| Donation remedy items (Ch18) | Data Table reference -- set `remedy_available: true` on the rule that requires it |
| War/disaster chapters (Ch19-22) | Park -- evaluate scope relevance first |
| Geographic name numbers (Ch23-25) | Park -- evaluate scope relevance first |
| Company logos chapter (Ch27) | Park -- visual content, limited rule extraction |

---

## PART 8 -- Benchmark Test Case Format

Log in Chapter Diagnostic under **"Benchmark Test Cases"**:

```
Chart: [Celebrity name]
Basic Number: [X] | Destiny Number: [Y] | Name Number: [Z]
Validates: [rule_id(s)]
Key finding: [What the author demonstrates about this chart]
Outcome category: [success / failure / correction / compatibility]
```

---

## PART 9 -- Known Issues to Avoid

1. **32,000 token output limit (CRITICAL)** -- Never generate more than 25 rules in a single Write tool call. Large chapters (Ch4, Ch9, Ch16) MUST use Part files. Attempting to write 60-100 rules in one pass will hit the output limit and terminate the session.
2. **Writing all 4 documents in one response** -- Each of the 4 files gets its own separate Write call. Never bundle them.
3. **Writing output to context window** -- Write tool only. Status line only in context.
4. **Merging sub-date variants** -- Each birth-date variant (e.g., born on 1st vs. 10th vs. 19th vs. 28th) is a separate rule.
5. **Treating A-Z chart as rules** -- It's a data table.
6. **Missing `result` block fields** -- All 7 fields required every time.
7. **Missing `source` block fields** -- All 7 fields required every time.
8. **Skipping undefined 81-combination cells** -- Log them in Diagnostic as "undefined pairs" but do not create empty rules.
9. **Writing a single rules file for large chapters** -- Ch4, Ch9, Ch16 must use `_Part1.json`, `_Part2.json` etc. A single `_Rules.json` for 80+ rules will exceed the output limit.
10. **Decoding celebrity charts as rules** -- They are benchmark logs only.

---

## PART 10 -- Decode Session Management

Suggested thread breakdown for this book:

| Thread | Chapters | Est. Rules | Est. Output Files |
|---|---|---|---|
| Thread A (primary) | Ch3, Ch4, Ch9 | ~145 | ~18 (4 + 8 + 6) |
| Thread B | Ch16, Ch6, Ch5, Ch7 | ~120 | ~19 (7 + 4 + 4 + 4) |
| Thread C | Ch13, Ch14, Ch10, Ch11, Ch12, Ch17 | ~80 | 24 (4 per chapter) |
| Thread D | Ch28, Ch26, Ch19-25 (parked) | TBD | TBD |
| Thread E | Ch15 + 50 sub-files (benchmarks) | 0 rules | 1 benchmark log file |

> File counts are higher than before because each chapter now produces 4 separate files + Part files for large chapters. This is by design -- it prevents the 32k output limit error.

Rule ID continuity must be maintained -- check the last rule_id used before starting each new chapter.
