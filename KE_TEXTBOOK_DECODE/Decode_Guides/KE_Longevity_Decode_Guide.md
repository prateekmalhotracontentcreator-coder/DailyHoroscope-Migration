# KE -- Longevity and Astro System: Full Book Decode Guide

> **This is the single authoritative reference for all CC threads decoding this book.**
> A new thread picks this up, reads it fully, and operates autonomously chapter by chapter.
> No toggling back to the parent session is required.
> Last updated: 2026-05-18 | Ch4 ✅ Ch5 ✅ | Ch6 next

---

## **🔴 MANDATORY FIRST ACTION -- Do this NOW, before reading anything else**

**Do not read this guide yet. Do not begin decoding. Execute these Write tool calls first -- one per file:**

Create all 4 output files for Chapter 6:

| # | File path | Initial content |
|---|---|---|
| 1 | `/Users/apple/Documents/Knowledge Engine_eBooks/Longevity_CC_Decode/Longevity_Ch06_GeneralHouseTraits_Rules.json` | `[]` |
| 2 | `/Users/apple/Documents/Knowledge Engine_eBooks/Longevity_CC_Decode/Longevity_Ch06_GeneralHouseTraits_DataTables.md` | `# Ch6 Data Tables\n\n[Writing in progress]` |
| 3 | `/Users/apple/Documents/Knowledge Engine_eBooks/Longevity_CC_Decode/Longevity_Ch06_GeneralHouseTraits_Summary.md` | `# Ch6 Technical Summary\n\n[Writing in progress]` |
| 4 | `/Users/apple/Documents/Knowledge Engine_eBooks/Longevity_CC_Decode/Longevity_Ch06_GeneralHouseTraits_Diagnostic.md` | `# Ch6 Chapter Diagnostic\n\n[Writing in progress]` |

**Then post this one line in the context window:**
> "4 files created for Ch6. Reading guide now."

**This is non-negotiable.** All 4 files must exist on disk before any decoding begins. Every chapter gets its own 4 files. This is what keeps the thread alive through the full book.

---

> ## **⚠️ OUTPUT METHOD -- Absolute Rule**
> **ALL decoded content goes into files via the Write tool. Nothing else.**
> **The context window receives one-line status updates only -- nothing more.**
> **Every chapter produces exactly 4 output files. Each file is written in a separate Write tool call.**
> **JSON rules are written in batches of ≤25 rules per Write call. Large chapters use Part files.**
> **Reason: attempting to write 40+ rules in one pass hits the 32,000 token output limit and terminates the session.**
> **Output folder:** `/Users/apple/Documents/Knowledge Engine_eBooks/Longevity_CC_Decode/`
> **File naming:** `Longevity_Ch{NN}_{ShortTitle}_{Type}.json/.md`

---

## Chapter Start Protocol -- Execute at the start of EVERY chapter

### Step 1 -- Create all 4 output files (Write tool × 4)

Before reading the PDF, create placeholder files for the chapter:
- `Longevity_Ch{NN}_{ShortTitle}_Rules.json` → initial content: `[]`
- `Longevity_Ch{NN}_{ShortTitle}_DataTables.md` → initial content: `# Ch{NN} Data Tables\n\n[Writing in progress]`
- `Longevity_Ch{NN}_{ShortTitle}_Summary.md` → initial content: `# Ch{NN} Technical Summary\n\n[Writing in progress]`
- `Longevity_Ch{NN}_{ShortTitle}_Diagnostic.md` → initial content: `# Ch{NN} Chapter Diagnostic\n\n[Writing in progress]`

### Step 2 -- Context window: one line only
> `"4 files created for Ch[NN]. Beginning decode."`

### Step 3 -- Read the PDF fully before writing any content

### Step 4 -- Write DataTables file (single Write call)

### Step 5 -- Write JSON Rules file (batched -- CRITICAL)

**⚠️ NEVER write more than 25 rules in a single Write tool call.**

- **Small chapters (≤25 rules):** Write the complete JSON array in one call → `Longevity_Ch{NN}_{ShortTitle}_Rules.json`
- **Large chapters (>25 rules):** Write in part files -- each part is a complete, valid JSON array:
  - Part 1 → `Longevity_Ch{NN}_{ShortTitle}_Rules_Part1.json` (rules 001-025)
  - Part 2 → `Longevity_Ch{NN}_{ShortTitle}_Rules_Part2.json` (rules 026-050)
  - Continue until all rules are written

### Step 6 -- Write Summary file (single Write call, ≤10 lines)

### Step 7 -- Write Diagnostic file (single Write call)

### Step 8 -- Context window: one line only
> `"Ch[NN] complete. [N] rules across [N] part files. [N] tables. Proceeding to Ch[NN+1]."`

**Nothing else goes in the context window. Ever.**

---

## PART 1 -- Project Identity

| Field | Value |
|---|---|
| Book | Longevity and Astro System |
| `book_id` | `longevity_kp_v1_20260518` |
| `science_id` | `kp_jyotish` |
| Publisher | Nairs Publishing House, Hyderabad |
| Astrological system | Krishnamurti Paddhati (KP) -- Placidus house division, KP Ayanamsha 23°55'58" |
| Target collection | MongoDB: `interpretation_rules` |
| PDF root path | `/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/LongevityAstroSystem/` |
| Decode method | **CC Direct** -- CC reads each PDF and produces output in one pass |
| Parent process doc | `/Users/apple/DailyHoroscope-Migration/KE_Book_Decode_Process_Technical.md` |

### Why CC Direct (not NotebookLM)

NLM was used for Ch4 and Ch5. It was abandoned after Ch5 due to persistent failures (documented in Part 9). CC reads PDFs directly, applies the schema in one pass, and self-audits. NLM required 2-3 correction rounds per chapter and never resolved the `maraka_houses` field despite three explicit briefs.

---

## PART 2 -- KP System Primer (Context for Rule Extraction)

Before decoding, understand these KP fundamentals so rules are classified correctly:

**The 4-Level Signification Hierarchy (strongest → weakest):**
- Level 1: Planets in the stars of occupants of the house (strongest)
- Level 2: Planets occupying the house directly
- Level 3: Planets in the stars of the lord of the house cusp
- Level 4: Sign lord of the house (weakest -- fallback only)

**Longevity Houses (primary triangle):** 1st (Lagna), 3rd, 8th

**Negating Houses:**
- Maraka (death-inflicting): 2nd and 7th -- universal for ALL lagnas
- Badhaka (obstructing): 11th for moveable, 9th for fixed, 7th for dual lagnas
- Dush-sthana (malefic): 6th, 8th, 12th

**Protective Houses (Punya):** 1st, 5th, 9th, 10th

**Badhaka Configuration by Lagna Modality:**
| Modality | Signs | Badhaka House |
|---|---|---|
| Moveable (Chara) | Aries, Cancer, Libra, Capricorn | 11th |
| Fixed (Sthira) | Taurus, Leo, Scorpio, Aquarius | 9th |
| Dual (Dwiswabhava) | Gemini, Virgo, Sagittarius, Pisces | 7th |

**⚠️ Critical -- Dual Lagna:** For dual lagnas, the 7th house is BOTH a maraka AND badhaka house simultaneously. This is the highest-risk configuration and requires explicit note in any rule covering dual lagnas.

**⚠️ Critical -- Fixed Lagna:** The 9th house is traditionally protective (punya) but becomes the badhaka for fixed lagnas. Any rule referencing the 9th house for fixed lagnas must carry `"claim_polarity": "conditional"` and note the dual role.

**The 4-Gate Longevity Framework:**
- Gate 1: Birth time verification
- Gate 2: Cuspal Sub-Lord event gate -- determines aayu bucket (what life span is promised)
- Gate 3: Toxicity filter -- malefic intensifiers and protective vetoes
- Gate 4: Temporal resolution -- DBAS + transit timing (when the event fires)

**Node Proxy Priority (Rahu/Ketu):** a) Planet conjoined → b) Planet aspecting → c) Star lord → d) Sign lord

**Aayu Buckets:**
| Bucket | `aayu_bucket` value | Age Range |
|---|---|---|
| Infant mortality | `"balarishta"` | 0-8 years |
| Short life | `"alpa_aayu"` | 8-33 years |
| Middle life | `"madhya_aayu"` | 33-66 years |
| Full life | `"purna_aayu"` | 66-99 years |
| Super-centenarian | `"aparimita_aayu"` | 100+ years |

> **Never use `"alpa_aayu"` for Balarishta.** They are separate buckets.

---

## PART 3 -- Full KE Schema

Every rule is a MongoDB document. The complete schema:

```json
{
  "rule_id": "kp-ch06-001",
  "science_id": "kp_jyotish",
  "active": true,
  "approval_status": "pending_human_review",
  "checkable": false,
  "source": {
    "book": "Longevity and Astro System",
    "book_id": "longevity_kp_v1_20260518",
    "chapter": 6,
    "chapter_name": "General Longevity Traits for All Houses",
    "sloka": null,
    "batch_id": "kp-ch06-v1-20260518",
    "passage_ref_id": null
  },
  "title": "Short descriptive title",
  "summary": "One sentence -- what the rule says.",
  "full_text": "Full diagnostic logic as written, stripped of numeric coefficients. No percentages, no multipliers -- use intensity words (significant, severe, extreme).",
  "tags": ["gate_2", "longevity", "alpa_aayu"],
  "category": "kp_foundation",
  "condition": {
    "type": "engine_specification",
    "kp_gate": "foundation",
    "signification_level": null,
    "lagna_modality": "universal",
    "badhaka_house": null,
    "maraka_houses": null
  },
  "claim_axis": "general",
  "claim_scope": "engine_specification",
  "claim_polarity": "neutral",
  "timing_bias": "sustained",
  "strength_band": "extreme",
  "mutually_exclusive_with": ["kp-ch05-008"],
  "result": {
    "effect": "Short description of outcome.",
    "severity": null,
    "aayu_bucket": null,
    "remedy_available": false,
    "remedy_ref_id": null
  }
}
```

### Field-by-Field Rules

**`rule_id`**
Format: `kp-ch{NN}-{NNN}` -- chapter number zero-padded to 2 digits, sequence zero-padded to 3. Example: `kp-ch06-001`.

**`science_id`**
Always `"kp_jyotish"`. NEVER `"vedic_astrology"`. These are different systems and must never be mixed.

**`active`**
Always `true`.

**`approval_status`**
Always `"pending_human_review"`. Only the co-founder can set to `"approved"` via the Library Console. Never set to `"approved"` during decode.

**`checkable`**
Always `false`. Phase 1 -- no evaluator is built yet.

**`source` block -- all 7 fields required, always:**
- `book`: "Longevity and Astro System"
- `book_id`: "longevity_kp_v1_20260518"
- `chapter`: integer
- `chapter_name`: exact chapter title from PDF
- `sloka`: `null` unless the chapter has numbered verses/rules
- `batch_id`: `"kp-ch{NN}-v1-20260518"` (e.g., `"kp-ch06-v1-20260518"`)
- `passage_ref_id`: `null`

**`title`**
Short noun phrase, max 10 words. Unique within the chapter.

**`summary`**
Single sentence. What the rule does. No jargon.

**`full_text`**
The diagnostic logic in plain language. No numeric coefficients. Replace percentages/multipliers with: significant / severe / extreme / moderate / limited.

**`tags`**
Array of lowercase snake_case strings. Always include the gate (`"foundation"`, `"gate_2"`, etc.) and domain (`"longevity"`, `"badhaka"`, `"maraka"`, etc.).

**`category`**
- Foundation rules: `"kp_foundation"`
- Gate 2 outcome rules: `"kp_longevity_gate_2"`
- Gate 3 filter rules: `"kp_longevity_gate_3"`
- Gate 4 timing rules: `"kp_longevity_gate_4"`

**`condition.type`**
- `"engine_specification"` -- rule defines a constant or protocol
- `"kp_sub_lord"` -- rule fires based on sub-lord evaluation
- `"kp_longevity_factor"` -- rule fires based on house signification
- `"kp_badhaka"` -- rule defines or invokes badhaka logic
- `"kp_significator"` -- rule involves the 4-level signification hierarchy

**`condition.kp_gate`**
One of: `"foundation"` / `"gate_1"` / `"gate_2"` / `"gate_3"` / `"gate_4"`

**`condition.signification_level`**
- `null` -- rule is universal / meta-principle (most rules)
- `1` -- rule ONLY applies to planets in stars of occupants
- `2` -- rule ONLY applies to house occupants
- `3` -- rule ONLY applies to planets in stars of the cusp lord
- `4` -- rule ONLY applies to sign lord evaluation
**Test:** "Does this rule only fire at level X, or regardless of level?" If regardless -- use `null`.

**`condition.lagna_modality`**
- `"universal"` -- applies to all lagnas
- `"moveable"` -- Aries, Cancer, Libra, Capricorn only
- `"fixed"` -- Taurus, Leo, Scorpio, Aquarius only
- `"dual"` -- Gemini, Virgo, Sagittarius, Pisces only
- For Ch7-18: use the specific sign name (e.g., `"aries"`)

**`condition.badhaka_house`**
- `null` for universal rules
- `11` for moveable lagna rules
- `9` for fixed lagna rules
- `7` for dual lagna rules

**`condition.maraka_houses`**
- `null` -- Foundation/definition rules only
- `[2, 7]` -- ALL Gate 2/3/4 outcome rules that evaluate maraka signification
> **⚠️ This field must ALWAYS have a value. Never leave it blank after the colon.**

**`claim_axis`**
- `"general"` -- engine specification, universal mechanics
- `"longevity"` -- any rule producing a longevity outcome or affecting aayu bucket

**`claim_scope`**
- `"engine_specification"` -- defines how the engine works (no outcome)
- `"natal_trait"` -- characteristic present from birth (sustained)
- `"event_timing"` -- fires at a specific dasha/transit moment

**`claim_polarity`**
- `"neutral"` -- engine specs, definitions
- `"positive"` -- protective, life-extending
- `"negative"` -- negating, life-shortening, terminal
- `"conditional"` -- depends on other factors (e.g., 9th house dual-role)

**`timing_bias`**
- `"sustained"` -- always active from birth
- `"early"` -- fires in first third of life
- `"mid"` -- fires in middle third
- `"late"` -- fires in final third
- `"immediate"` -- fires at a specific dasha/transit point

**`strength_band`**
Words only: `"extreme"` / `"high"` / `"medium"` / `"low"`
Engine mapping (for reference -- do NOT put numbers in rules): extreme=0.90, high=0.70, medium=0.50, low=0.30

**`mutually_exclusive_with`**
- Array of rule_ids that this rule vetoes or is vetoed by
- OMIT this field entirely if not applicable -- do not include an empty array `[]`

**`result.effect`**
Short description of what happens when the rule fires. Plain language.

**`result.severity`**
- `null` -- Foundation/definition/engine_spec rules ALWAYS
- `"extreme"` / `"high"` / `"medium"` / `"low"` -- Gate 2/3/4 outcome rules only

**`result.aayu_bucket`**
- `null` -- Foundation rules, modifier rules, veto rules, event-timing rules
- One of the 5 bucket values for outcome rules that determine lifespan category

**`result.remedy_available`**
Always `false` for this book. Set `true` only if the text explicitly mentions a remedy.

**`result.remedy_ref_id`**
Always `null`.

---

## PART 4 -- Decode Process (Per Chapter)

### Step 1 -- Read the full PDF

Read the complete chapter PDF before writing any rules. Identify:
- Total number of distinct logical statements (rule count estimate)
- Which sections are rules vs. static data vs. examples vs. narrative
- Gate classification for each section
- Any contradictions or dual-role situations

### Step 2 -- Classify content into 4 categories

| Category | Action |
|---|---|
| Diagnostic logic / rules | Extract as JSON rules |
| Static lookup tables | Add to Data Tables document |
| Example charts / case studies | Log as Benchmark Test Case in Diagnostic |
| Narrative, spiritual, or illustrative | Discard |

### Step 3 -- Write the 4 documents

**Document 1: Technical Summary**
- Chapter domain
- Governing gates (e.g., Foundation + Gate 2)
- Key principle (1-2 sentences)
- Special protocols or warnings introduced
- Total rules extracted + gate distribution breakdown

**Document 2: Data Tables**
All static lookup content. Number tables sequentially within the chapter (Table 6.1, 6.2...). Carry forward any book-wide tables established in earlier chapters.

**Document 3: JSON Rules**
Single unified array `[...]`. All rules in sequential order. Self-audit using the Quality Gate checklist (Part 6) before writing the final output.

**Document 4: Chapter Diagnostic**
1. Chapter scope
2. Rule count + gate distribution
3. Exclusions (what was excluded and why)
4. Contradiction pairs (rules that could fire simultaneously with opposite polarity)
5. Veto relationships (which rules cancel which)
6. Open questions (logic the text hints at but doesn't fully resolve)
7. Benchmark Test Cases (from example charts)

### Step 4 -- Self-audit

Run every item in the Quality Gate (Part 6) before delivering. Fix any failures before output.

---

## PART 5 -- Chapter Map, Status & Expectations

### Completed Chapters

| Ch | Title | Rules | Batch ID | Status |
|---|---|---|---|---|
| 4 | Some Basic Fundamental Rules | 14 | kp-ch04-v1-20260518 | ✅ Complete |
| 5 | Basics of Longevity | 15 | kp-ch05-v1-20260518 | ✅ Complete ⚠️ ingest patch |

### Active & Pending Chapters

**Ch6 -- General Longevity Traits for All Houses** 🔜 NEXT
- `6_General Longevity traits for all houses.pdf`
- Expect: House-by-house longevity indicators universal to all lagnas
- Expect: Classification of each of the 12 houses as protective / negating / neutral
- Expect: First house-strength modifier rules
- `lagna_modality: "universal"` on all rules
- `claim_axis: "longevity"` on all outcome rules
- Gate mix: Foundation + Gate 2 + Gate 3

**Ch19 -- Method of Analysis of Longevity** ⚡ HIGH PRIORITY (decode before Ch7-18)
- `19_Method of Analysis of Longevity.pdf`
- Expect: Full 4-Gate procedural SOP
- Expect: Step-by-step engine flow -- how the engine applies Ch4-18 rules in sequence
- Expect: Ruling planets confirmation protocol
- This chapter provides the structural framework that Ch7-18 rules slot into
- Decode Ch6 first, then Ch19, then proceed to Ch7-18

**Ch7-18 -- Lagna-Specific Chapters (12 signs)**
- One chapter per ascending sign
- `lagna_modality` must match: `"moveable"` / `"fixed"` / `"dual"` (not the sign name)
- `badhaka_house` must be populated per modality
- `maraka_houses`: `[2, 7]` on all outcome rules
- Expect: Specific planet combinations that are toxic or protective for each lagna
- Expect: Named planets as maraka or badhaka lords for that sign
- Expect: The first rules with `claim_scope: "natal_trait"` that are lagna-specific

**Sign → Modality mapping:**
| Sign | Modality | Badhaka |
|---|---|---|
| Aries (Ch7) | moveable | 11 |
| Taurus (Ch8) | fixed | 9 |
| Gemini (Ch9) | dual | 7 |
| Cancer (Ch10) | moveable | 11 |
| Leo (Ch11) | fixed | 9 |
| Virgo (Ch12) | dual | 7 |
| Libra (Ch13) | moveable | 11 |
| Scorpio (Ch14) | fixed | 9 |
| Sagittarius (Ch15) | dual | 7 |
| Capricorn (Ch16) | moveable | 11 |
| Aquarius (Ch17) | fixed | 9 |
| Pisces (Ch18) | dual | 7 |

**Ch20-24 -- Balarishta Case Chapters**
- `20_Balarishta horoscopes.pdf` through `24_Balarishta or Infant Mortality Chart-IV.pdf`
- **Extract ZERO rules.** These are case study chapters.
- Log each chart as a Benchmark Test Case validating kp-ch05-007 (Balarishta Diagnostic)
- Format: Chart name/date/location, planet positions, which Ch5 rules it validates

**Ch25-58 -- Historical Case Study Chapters**
- All remaining PDFs (famous charts: Kennedy, Vivekananda, Onassis, etc.)
- **Extract ZERO rules.**
- Log as Benchmark Test Cases against the relevant aayu bucket rules from Ch5
- Note: Some chapters are already named by aayu bucket (e.g., `29_Alpa Aayu or short longevity charts.pdf`, `36_Madhya Aayu or middle longevity.pdf`, `52_M Visweswarayya - Purna Aayu.pdf`, `55_Super Centenarian-Aparimita Aayu.pdf`)

**Decode Priority Order:**
```
Ch6  → Universal house traits (next)
Ch19 → 4-Gate procedural SOP (decode before lagna chapters)
Ch7  → Aries
Ch8  → Taurus
Ch9  → Gemini
Ch10 → Cancer
Ch11 → Leo
Ch12 → Virgo
Ch13 → Libra
Ch14 → Scorpio
Ch15 → Sagittarius
Ch16 → Capricorn
Ch17 → Aquarius
Ch18 → Pisces
Ch20-24 → Balarishta benchmarks
Ch25-58 → Case study benchmarks
```

---

## PART 6 -- Quality Gate Checklist

Run this on every rule before finalising the JSON array. Fix failures before output.

### Schema Checks (every rule, every chapter)

- [ ] `rule_id` follows format `kp-ch{NN}-{NNN}` with correct chapter number
- [ ] `science_id` is `"kp_jyotish"` -- not `"vedic_astrology"`
- [ ] `active: true` present
- [ ] `approval_status: "pending_human_review"` present
- [ ] `checkable: false` present
- [ ] `source` block has ALL 7 fields: book, book_id, chapter, chapter_name, **sloka**, **batch_id**, **passage_ref_id**
- [ ] `condition` block has ALL 6 fields: type, kp_gate, signification_level, lagna_modality, badhaka_house, **maraka_houses**
- [ ] `maraka_houses` has an actual value -- `[2, 7]` or `null` -- **never blank**
- [ ] `result` block has ALL 5 fields: effect, severity, aayu_bucket, remedy_available, **remedy_ref_id**
- [ ] `mutually_exclusive_with` field is OMITTED entirely if rule has no veto relationships

### Content Checks

- [ ] Foundation/engine_specification rules: `severity: null`
- [ ] Gate 2/3/4 outcome rules: `severity` populated
- [ ] Balarishta rules use `"balarishta"` not `"alpa_aayu"`
- [ ] Veto rules have `"veto_rule"` in tags AND `mutually_exclusive_with` field
- [ ] 9th house rules for fixed lagnas: `"claim_polarity": "conditional"`, dual-role noted in `full_text`
- [ ] 7th house rules for dual lagnas: `full_text` notes dual maraka+badhaka role
- [ ] No numeric coefficients or percentages in `full_text` -- intensity words only
- [ ] `signification_level` is `null` for universal/meta rules
- [ ] `claim_axis: "longevity"` for all outcome-bearing rules
- [ ] `lagna_modality` correctly reflects the rule scope (universal vs. specific modality)
- [ ] `badhaka_house` populated correctly for lagna-modality-specific rules

### Delivery Format

- [ ] Single unified JSON array `[...]`
- [ ] Rules sequential: kp-chXX-001, 002, 003... no gaps, no duplicates
- [ ] 4 documents delivered in one response
- [ ] Chapter Diagnostic includes: scope, count, gate distribution, exclusions, contradiction pairs, veto relationships, open questions, benchmark test cases

---

## PART 7 -- Completed Rule Index

### Chapter 4 -- 14 Rules | Batch: `kp-ch04-v1-20260518`

| Rule ID | Title | Gate | Scope |
|---|---|---|---|
| kp-ch04-001 | Sub-Lord Authority in Event Manifestation | Foundation | engine_specification |
| kp-ch04-002 | Shadow Planet (Node) Priority Protocol | Foundation | natal_trait |
| kp-ch04-003 | Exclusion of Moon Sign as Primary Reference | Foundation | engine_specification |
| kp-ch04-004 | Special Aspect Constraint for Mars | Foundation | natal_trait |
| kp-ch04-005 | Special Aspect Constraint for Jupiter | Foundation | natal_trait |
| kp-ch04-006 | Special Aspect Constraint for Saturn | Foundation | natal_trait |
| kp-ch04-007 | Node Aspect Immunity | Foundation | engine_specification |
| kp-ch04-008 | Stellar Primacy in Result Delivery | Foundation | natal_trait |
| kp-ch04-009 | Planetary Body Classification Protocol | Foundation | engine_specification |
| kp-ch04-010 | Sign Lordship Assignment (Level 4 Hierarchy) | Foundation | engine_specification |
| kp-ch04-011 | Sub-Lord Arc Mathematical Constant | Foundation | engine_specification |
| kp-ch04-012 | Planetary Result Mirroring in Node Stars | Foundation | natal_trait |
| kp-ch04-013 | Ruling Planets Selection Protocol | Gate 4 | engine_specification |
| kp-ch04-014 | Timing of Events: DBAS + Transit Logic Gate | Gate 4 | engine_specification |

### Chapter 5 -- 15 Rules | Batch: `kp-ch05-v1-20260518` | ⚠️ Ingest patch required

| Rule ID | Title | Gate | Aayu Bucket | Polarity |
|---|---|---|---|---|
| kp-ch05-001 | Six-Step House Signification Analysis Protocol | Foundation | null | neutral |
| kp-ch05-002 | Badhaka House Assignment: Moveable Lagna | Foundation | null | negative |
| kp-ch05-003 | Badhaka House Assignment: Fixed Lagna | Foundation | null | negative |
| kp-ch05-004 | Badhaka House Assignment: Dual Lagna | Foundation | null | negative |
| kp-ch05-005 | Universal Maraka House Definition | Foundation | null | negative |
| kp-ch05-006 | Punya Houses Protective Veto | Gate 3 | null (elevates) | positive |
| kp-ch05-007 | Balarishta (Infant Mortality) Diagnostic | Gate 2 | balarishta | negative |
| kp-ch05-008 | Alpa Aayu (Short Life) Diagnostic | Gate 2 | alpa_aayu | negative |
| kp-ch05-009 | Madhya Aayu (Middle Life) Diagnostic | Gate 2 | madhya_aayu | positive |
| kp-ch05-010 | Purnayu (Full Life) Diagnostic | Gate 2 | purna_aayu | positive |
| kp-ch05-011 | Harmful Toxicity Filter: 8th House Malefic Affliction | Gate 3 | null (modifier) | negative |
| kp-ch05-012 | Lethal Overlap: The 'Dead' Diagnostic Rule | Gate 2 | null (event) | negative |
| kp-ch05-013 | Terminal Death Trigger: DBA Period Rule | Gate 4 | null (timing) | negative |
| kp-ch05-014 | Dual Role Caution for 9th House | Foundation | null | conditional |
| kp-ch05-015 | Aparimita Aayu (Super-Centenarian) Diagnostic | Gate 2 | aparimita_aayu | positive |

---

## PART 8 -- Book-Wide Data Tables (Established)

These tables have been produced from Ch4 and Ch5. Do not re-derive them. Reference them when needed.

**Table 4.1 -- Vimshottari Dasha Period Allocation (VMD)**
Ketu 7yr | Venus 20yr | Sun 6yr | Moon 10yr | Mars 7yr | Rahu 18yr | Jupiter 16yr | Saturn 19yr | Mercury 17yr | Total 120yr

**Table 4.2 -- Special Planetary Aspects**
Mars: 4th, 7th, 8th | Jupiter: 5th, 7th, 9th | Saturn: 3rd, 7th, 10th | Nodes: none

**Table 4.3 -- Node Result Priority**
Level 1: Conjoined planet | Level 2: Aspecting planet | Level 3: Star lord | Level 4: Sign lord

**Table 4.4 -- Sub-Lord Arc Mathematical Calculation**
Ketu 0°46'40" | Venus 2°13'20" | Sun 0°40'00" | Moon 1°06'40" | Mars 0°46'40" | Rahu 2°00'00" | Jupiter 1°46'40" | Saturn 2°06'40" | Mercury 1°53'20" | Total = 13°20' (800 min)

**Table 5.1 -- Aayu Bucket Definitions**
Balarishta 0-8yr | Alpa 8-33yr | Madhya 33-66yr | Purna 66-99yr | Aparimita 100+yr

**Table 5.2 -- Master Badhaka & Maraka Configuration**
Moveable → 11th | Fixed → 9th | Dual → 7th | Maraka: 2nd & 7th (universal)

**Table 5.3 -- Longevity Logic Outcome Matrix**
Balarishta: Houses 1,3,8 + Badhaka + Maraka DBA at birth
Alpa Aayu: Houses 6,8,12 + Badhaka + Maraka dominant
Madhya Aayu: Mix of 1,5,9,10 and 6,8,12 + Badhaka + Maraka
Purna Aayu: Houses 1,5,9,10 dominant, isolated from Badhaka/Maraka
Aparimita: Complete isolation from Badhaka and Maraka

---

## PART 9 -- NLM Issues Log (Do Not Repeat)

This section documents every failure from the NotebookLM decode of Ch4 and Ch5. CC must not reproduce any of these errors.

### Issue 1 -- `maraka_houses` field consistently empty (CRITICAL)
- **What happened:** NLM produced `"maraka_houses":` with no value in 8 rules across Ch5. The field was blank after the colon -- invalid JSON. This persisted across THREE correction rounds and was never resolved by NLM.
- **Pattern:** NLM could write the field name but dropped the array value `[2, 7]` every time.
- **CC rule:** After writing `"maraka_houses":`, immediately type `[2, 7]` or `null`. Never leave blank. Validate before output.
- **Ingest patch (Ch5 only):** At MongoDB insert for Ch5, any outcome rule with null/missing `maraka_houses` → set `[2, 7]`.

### Issue 2 -- `source` block missing fields on first output
- **What happened:** Ch5 first output had source blocks with only 5 fields -- `sloka` and `passage_ref_id` were omitted. Required a correction round.
- **CC rule:** Source block must always have all 7 fields. Never omit `sloka: null` or `passage_ref_id: null`.

### Issue 3 -- `result` block missing `remedy_ref_id`
- **What happened:** Ch5 first output had result blocks with 4 fields -- `remedy_ref_id` was omitted. Required a correction round.
- **CC rule:** Result block must always have all 5 fields. Never omit `remedy_ref_id: null`.

### Issue 4 -- `severity` populated on foundation rules
- **What happened:** NLM added `"severity": "medium"` and `"severity": "high"` to badhaka definition rules (kp-ch05-002/003/004/005) and the analysis protocol rule (kp-ch05-001). Foundation rules do not produce outcomes and should never have severity.
- **CC rule:** `severity: null` on ALL foundation/engine_specification rules. Populate only on Gate 2/3/4 outcome rules.

### Issue 5 -- Balarishta mapped to wrong aayu_bucket
- **What happened:** kp-ch05-007 (Balarishta) was given `"aayu_bucket": "alpa_aayu"`. Balarishta (0-8yr) is a separate bucket from Alpa Aayu (8-33yr).
- **CC rule:** Balarishta always uses `"balarishta"`. Never use `"alpa_aayu"` for infant mortality rules.

### Issue 6 -- Veto rule aayu_bucket hardcoded incorrectly
- **What happened:** kp-ch05-006 (Punya Veto) was given `"aayu_bucket": "madhya_aayu"`. A veto rule elevates the bucket dynamically -- it does not produce a fixed bucket. Hardcoding madhya_aayu made it only useful when blocking alpa outcomes.
- **CC rule:** Veto/modifier rules → `aayu_bucket: null`. Effect text should describe the modification ("Life span bucket elevated by one level"), not the fixed outcome.

### Issue 7 -- Toxicity filter aayu_bucket hardcoded incorrectly
- **What happened:** kp-ch05-011 (8th House Malefic Toxicity) was given `"aayu_bucket": "alpa_aayu"`. A toxicity filter is a conditional modifier -- it reduces the bucket only when other protective factors are absent.
- **CC rule:** Filter/modifier rules → `aayu_bucket: null`. The final bucket is determined by the interaction of multiple rules, not by the modifier alone.

### Issue 8 -- Incomplete first output (missing rules)
- **What happened:** Ch4 first output had 8 rules. After cross-referencing the PDF, 6 were missing (planetary classification, sign lordship, sub-lord math, planets in node stars, ruling planets, timing of events). Required a complete correction brief.
- **CC rule:** Read the entire PDF before writing any rules. Identify ALL distinct logical statements first, then write. Do not stop at obvious rules -- check every section heading.

### Issue 9 -- Output split across multiple JSON arrays
- **What happened:** Ch5 second output contained two separate JSON arrays in the same document -- a first draft at the top and the corrected set below. Required a merge.
- **CC rule:** Always one unified JSON array `[...]` per chapter. Never produce multiple arrays in one output.

### Issue 10 -- Technical Summary gate count inconsistent with Diagnostic
- **What happened:** Document 1 (Summary) stated different gate counts than Document 4 (Diagnostic). The Diagnostic is built from the actual rules; the Summary should match it.
- **CC rule:** Write the Diagnostic first, count the rules by gate, then write the Summary gate distribution from those counts -- not from memory.

### Issue 11 -- First draft included in final output document
- **What happened:** Ch5 NLM output contained the 4-rule first draft at the top of the document followed by the 14-rule corrected set. The stale draft was never retired.
- **CC rule:** Produce one clean output. No drafts, no interim versions, no superseded content in the delivery document.

### Issue 12 -- `signification_level: 1` on universal meta-rule
- **What happened:** kp-ch04-008 (Stellar Primacy) was assigned `signification_level: 1`. This is a universal principle about how all planets derive results via their star lord -- it applies at all signification levels, not just Level 1.
- **CC rule:** `signification_level` is only populated when a rule EXPLICITLY targets a specific level. For kp-ch04-008-style universal principles, use `null`.

---

## PART 10 -- Ingest Patches (Known Issues to Fix at MongoDB Insert)

| Patch | Affected | Rule |
|---|---|---|
| Ch5 `maraka_houses` empty | kp-ch05-005, 007, 008, 009, 010, 012, 013, 015 | If `kp_gate` ∈ {gate_2, gate_3, gate_4} AND `maraka_houses` is null → set `[2, 7]` |

---

## PART 11 -- Benchmark Test Case Log Format

When a chapter contains example charts or case studies, log them in the Chapter Diagnostic under **"Benchmark Test Cases"** using this format:

```
Chart: [Name or description]
Date/Location: [Birth date and place if given]
Validates: [rule_id(s) this chart demonstrates]
Key data: [Relevant DBA period, planet positions, or sub-lord used by the author]
Author conclusion: [What the author derives from this chart]
```

Example (from Ch5):
```
Chart: Baby (Male), Banda, Sagar
Date/Location: 22-04-2012, Sagar
Validates: kp-ch05-007 (Balarishta), kp-ch05-012 (Lethal Overlap)
Key data: Birth in Ketu-Mars-Rahu DBA, all signifying maraka + badhaka; houses 1, 3, 8 unprotected
Author conclusion: Child died the same day -- lethal overlap confirmed
```

---

## PART 12 -- Decode Session Management

**One thread per phase is ideal. Suggested breakdown:**

| Thread | Scope | Chapters |
|---|---|---|
| Thread A (current) | Universal rules | Ch6, Ch19 |
| Thread B | Fixed lagna group | Ch8 (Taurus), Ch11 (Leo), Ch14 (Scorpio), Ch17 (Aquarius) |
| Thread C | Moveable lagna group | Ch7 (Aries), Ch10 (Cancer), Ch13 (Libra), Ch16 (Capricorn) |
| Thread D | Dual lagna group | Ch9 (Gemini), Ch12 (Virgo), Ch15 (Sagittarius), Ch18 (Pisces) |
| Thread E | Case studies | Ch20-58 (benchmark logs only) |

**After each chapter:** Update the status column in Part 5 of this guide. Add the chapter's rules to the Completed Rule Index in Part 7. Note any new ingest patches in Part 10.

**Rule ID continuity:** Each thread must check the last rule_id used in prior chapters before starting a new chapter. Rule IDs are unique across the entire book -- no duplicates.

---

## PART 13 -- Approval & Ingest Flow

1. CC produces 4-document output
2. CC self-audits against Quality Gate (Part 6)
3. Output reviewed by human (Prateek) -- content check only, not schema (schema is CC's job)
4. Rules ingested into MongoDB `interpretation_rules` collection with `approval_status: "pending_human_review"`
5. Co-founder reviews rules in Library Console → sets to `"approved"` chapter by chapter
6. Only `"approved"` rules are read by the KE engine at runtime

**Nothing in this decode is live until explicitly approved. All decoded rules are inert until approval.**
