# KE -- Medical Astrology: Full Book Decode Guide

> **This is the single authoritative reference for the CC thread decoding this book.**
> Operate autonomously chapter by chapter. No toggling back to the parent session required.
> Last updated: 2026-05-18 | Status: Not started

---

## **🔴 MANDATORY FIRST ACTION -- Do this NOW, before reading anything else**

**Do not read this guide yet. Do not begin decoding. Execute these Write tool calls first -- one per file:**

Create all 4 output files for Chapter 1:

| # | File path | Initial content |
|---|---|---|
| 1 | `/Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode/MedAstro_Ch01_DefinitionsYogas_Rules.json` | `[]` |
| 2 | `/Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode/MedAstro_Ch01_DefinitionsYogas_DataTables.md` | `# Ch1 Data Tables\n\n[Writing in progress]` |
| 3 | `/Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode/MedAstro_Ch01_DefinitionsYogas_Summary.md` | `# Ch1 Technical Summary\n\n[Writing in progress]` |
| 4 | `/Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode/MedAstro_Ch01_DefinitionsYogas_Diagnostic.md` | `# Ch1 Chapter Diagnostic\n\n[Writing in progress]` |

**Then post this one line in the context window:**
> "4 files created for Ch1. Reading guide now."

**This is non-negotiable.** All 4 files must exist on disk before any decoding begins. Every chapter gets its own 4 files. This is what keeps the thread alive through the full book.

---

> ## **⚠️ OUTPUT METHOD -- Absolute Rule**
> **ALL decoded content goes into files via the Write tool. Nothing else.**
> **The context window receives one-line status updates only -- nothing more.**
> **Every chapter produces exactly 4 output files. Each file is written in a separate Write tool call.**
> **JSON rules are written in batches of ≤25 rules per Write call. Large chapters use Part files.**
> **Reason: attempting to write 40+ rules in one pass hits the 32,000 token output limit and terminates the session.**
> **Output folder:** `/Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode/`
> **File naming:** `MedAstro_Ch{NN}_{ShortTitle}_{Type}.json/.md`

---

## Chapter Start Protocol -- Execute at the start of EVERY chapter

### Step 1 -- Create all 4 output files (Write tool × 4)

Before reading the PDF, create placeholder files for the chapter:
- `MedAstro_Ch{NN}_{ShortTitle}_Rules.json` → initial content: `[]`
- `MedAstro_Ch{NN}_{ShortTitle}_DataTables.md` → initial content: `# Ch{NN} Data Tables\n\n[Writing in progress]`
- `MedAstro_Ch{NN}_{ShortTitle}_Summary.md` → initial content: `# Ch{NN} Technical Summary\n\n[Writing in progress]`
- `MedAstro_Ch{NN}_{ShortTitle}_Diagnostic.md` → initial content: `# Ch{NN} Chapter Diagnostic\n\n[Writing in progress]`

### Step 2 -- Context window: one line only
> `"4 files created for Ch[NN]. Beginning decode."`

### Step 3 -- Read the PDF section fully before writing any content

### Step 4 -- Write DataTables file (single Write call)

### Step 5 -- Write JSON Rules file (batched -- CRITICAL)

**⚠️ NEVER write more than 25 rules in a single Write tool call.**

- **Small chapters (≤25 rules):** Write the complete JSON array in one call → `MedAstro_Ch{NN}_{ShortTitle}_Rules.json`
- **Large chapters (>25 rules):** Write in part files -- each part is a complete, valid JSON array:
  - Part 1 → `MedAstro_Ch{NN}_{ShortTitle}_Rules_Part1.json` (rules 001-025)
  - Part 2 → `MedAstro_Ch{NN}_{ShortTitle}_Rules_Part2.json` (rules 026-050)
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
| Book | Medical Astrology (Text Book) |
| `book_id` | `medical_astrology_v1_20260518` |
| `science_id` | `vedic_astrology` |
| Author | Dr. S. Krishna Kumar (Indian Council of Astrological Sciences, Bangalore Chapter) |
| System | Classical Vedic (Parashari) + Ayurvedic Tridosha integration |
| House system | Placidus / Equal (Vedic standard) |
| Cross-validation source | Medical Astrology Journal (Rajakaladevi & Kalaivani, IAJMRR 2022) |
| Primary PDF | `/Users/apple/Documents/Knowledge Engine_eBooks/Medical Astrology_Text Book/Medical Astrology_Text Book.pdf` |
| Journal PDF | `/Users/apple/Documents/Knowledge Engine_eBooks/Medical Astrology_Text Book/Medical Astrology_Journal.pdf` |
| Output folder | `/Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode/` |
| Target collection | MongoDB: `interpretation_rules` |
| Parent process doc | `/Users/apple/DailyHoroscope-Migration/KE_Book_Decode_Process_Technical.md` |

### ⚠️ Science System Isolation

`science_id: "vedic_astrology"` -- this is classical Parashari Vedic, NOT KP Jyotish. These two systems must **never** be mixed. Rules from this book must never reference KP sub-lord logic, KP ayanamsha, or the KP 4-Gate framework. Keep completely separate from Longevity book rules.

---

## PART 2 -- Vedic Medical Astrology Primer

### Core Signification Framework

**Planets → Body Systems & Diseases:**
| Planet | Body Domain |
|---|---|
| Sun | Heart, spine, eyes (right), bones, vitality, brain |
| Moon | Mind, lungs, blood, phlegm, left eye, uterus |
| Mars | Blood, bile, muscles, surgery, accidents, fever |
| Mercury | Nervous system, skin, speech, lungs |
| Jupiter | Liver, fat, arteries, diabetes, growth |
| Venus | Reproductive system, kidneys, semen, beauty |
| Saturn | Chronic illness, bones, nerves, teeth, joints |
| Rahu | Mysterious/incurable disease, poison, epidemic |
| Ketu | Fevers, wounds, intestines, occult diseases |

**Houses → Body Parts (standard Vedic assignment):**
| House | Body Part |
|---|---|
| 1st | Head, brain, skull, overall vitality |
| 2nd | Face, eyes, mouth, teeth, throat, speech |
| 3rd | Arms, shoulders, ears, throat, lungs |
| 4th | Chest, heart, lungs, stomach |
| 5th | Stomach, upper abdomen, liver, heart, spine |
| 6th | Intestines, lower abdomen, diseases (primary disease house) |
| 7th | Kidneys, lower back, reproductive organs |
| 8th | Genitals, excretory organs, chronic illness, death |
| 9th | Hips, thighs, nervous system |
| 10th | Knees, joints, skin |
| 11th | Legs, ankles, left ear |
| 12th | Feet, left eye, hospitalisation, bed confinement |

**Tridosha -- Ayurvedic Disease Classification:**
| Dosha | Planet | Nature |
|---|---|---|
| Vata | Saturn, Rahu | Neurological, joint, chronic, degenerative |
| Pitta | Sun, Mars, Ketu | Inflammatory, fever, liver, blood |
| Kapha | Moon, Venus, Jupiter | Phlegm, obesity, respiratory, reproductive |

**The 3-Layer Diagnostic Framework (equivalent of KP Gates):**
- **Layer 1 (Foundation):** Definitions, mappings, classifications -- planet-disease, house-body, Nakshatra-organ, sign-body
- **Layer 2 (Diagnostic):** Yoga conditions -- multi-factor combinations → specific disease or condition
- **Layer 3 (Timing):** Disease onset, duration, severity via dasha, Nakshatra, Tithi, Weekday

**Key Disease Houses:** 6th (illness), 8th (chronic/fatal illness), 12th (hospitalisation/bed rest)
**Badhaka applies:** Same modality rules as Longevity book -- 11th (moveable), 9th (fixed), 7th (dual)

---

## PART 3 -- Full KE Schema for Medical Astrology

Every rule is a complete MongoDB document. Schema for this book:

```json
{
  "rule_id": "ma-ch01-001",
  "science_id": "vedic_astrology",
  "active": true,
  "approval_status": "pending_human_review",
  "checkable": false,
  "yoga_name": "Jwara Yoga",
  "source": {
    "book": "Medical Astrology",
    "book_id": "medical_astrology_v1_20260518",
    "chapter": 1,
    "chapter_name": "Introduction, Definitions and Yogas",
    "sloka": null,
    "batch_id": "ma-ch01-v1-20260518",
    "passage_ref_id": null
  },
  "title": "Jwara Yoga: Fever Combination",
  "summary": "Specific planetary combination indicating fever-prone constitution.",
  "full_text": "When Sun and Moon are placed in the 6th house and aspected by Mars, the native is prone to recurrent fevers. The pitta aggravation from Mars intensifies the Sun-Moon combination in the disease house.",
  "tags": ["diagnostic", "fever", "pitta_disorder", "sun", "moon", "mars"],
  "category": "vedic_medical_diagnostic",
  "condition": {
    "type": "vedic_yoga",
    "vedic_layer": "diagnostic",
    "signification_level": null,
    "lagna_modality": "universal",
    "badhaka_house": null,
    "maraka_houses": null,
    "planets_involved": ["Sun", "Moon", "Mars"],
    "houses_involved": [6],
    "aspect_condition": "Mars aspects Sun-Moon conjunction"
  },
  "claim_axis": "medical",
  "claim_scope": "natal_trait",
  "claim_polarity": "negative",
  "timing_bias": "sustained",
  "strength_band": "high",
  "result": {
    "effect": "Recurrent fever tendency",
    "severity": "high",
    "disease_category": "pitta_disorder",
    "body_system": "immune",
    "aayu_bucket": null,
    "remedy_available": false,
    "remedy_ref_id": null
  }
}
```

### Field-by-Field Rules

**`rule_id`**
Format: `ma-ch{NN}-{NNN}` -- "ma" prefix for Medical Astrology, chapter zero-padded to 2 digits, sequence to 3.
Examples: `ma-ch01-001`, `ma-ch08-012`

**`science_id`**
Always `"vedic_astrology"`. Never `"kp_jyotish"`.

**`active`** -- Always `true`

**`approval_status`** -- Always `"pending_human_review"`

**`checkable`** -- Always `false`

**`yoga_name`**
- Named yoga (e.g., `"Jwara Yoga"`, `"Vrana Yoga"`, `"Dergha Roga Yoga"`) when the text gives a name
- `null` for unnamed planet-disease mappings and foundation rules
- Omit entirely if null -- do not include `"yoga_name": null` in foundation/mapping rules

**`source` block -- all 7 fields required:**
- `book`: "Medical Astrology"
- `book_id`: "medical_astrology_v1_20260518"
- `chapter`: integer
- `chapter_name`: exact chapter title from PDF
- `sloka`: `null` unless numbered
- `batch_id`: `"ma-ch{NN}-v1-20260518"`
- `passage_ref_id`: `null`

**`title`** -- Short noun phrase, max 10 words, unique within chapter

**`summary`** -- Single sentence. What the rule identifies or produces.

**`full_text`** -- Full diagnostic logic in plain language. No numeric coefficients. No percentages. Intensity words only: significant / severe / extreme / moderate / limited.

**`tags`** -- Include: layer tag (`"foundation"` / `"diagnostic"` / `"timing"`), relevant planets (lowercase), relevant houses (`"house_6"` etc.), disease category, dosha if applicable.

**`category`**
- `"vedic_medical_foundation"` -- definitions, mappings, classifications
- `"vedic_medical_diagnostic"` -- yoga conditions → disease identification
- `"vedic_medical_timing"` -- disease onset/duration logic

**`condition` block -- all fields required:**

- `type`: `"vedic_mapping"` (planet/house/nakshatra → body part) | `"vedic_yoga"` (multi-factor → disease) | `"vedic_timing"` (dasha/nakshatra duration) | `"engine_specification"` (definition rule)
- `vedic_layer`: `"foundation"` | `"diagnostic"` | `"timing"`
- `signification_level`: `null` for most rules; `1`-`4` only when the rule explicitly targets a specific level in the Vedic signification hierarchy
- `lagna_modality`: `"universal"` | `"moveable"` | `"fixed"` | `"dual"`
- `badhaka_house`: `null` | `7` | `9` | `11`
- `maraka_houses`: `null` | `[2, 7]`
- `planets_involved`: array of planet names involved in the yoga, or `null` for mapping/foundation rules
- `houses_involved`: array of house numbers relevant to the condition, or `null`
- `aspect_condition`: string describing aspect requirement, or `null`

**`claim_axis`**
- `"medical"` -- disease identification, body-part signification, health outcomes
- `"general"` -- engine specifications, definitions only

**`claim_scope`**
- `"engine_specification"` -- defines how the engine works, no outcome
- `"natal_trait"` -- inherent constitutional tendency from birth
- `"event_timing"` -- fires at a specific dasha/transit moment

**`claim_polarity`**
- `"neutral"` -- definitions, mappings
- `"negative"` -- disease-indicating, malefic
- `"positive"` -- protective, health-enhancing
- `"conditional"` -- depends on other chart factors

**`timing_bias`**
- `"sustained"` -- lifelong constitutional tendency
- `"early"` / `"mid"` / `"late"` -- life-phase specific
- `"immediate"` -- fires at specific dasha/transit point

**`strength_band`** -- `"extreme"` / `"high"` / `"medium"` / `"low"` (words only)

**`result` block -- all 6 fields required:**
- `effect`: Plain description of health outcome
- `severity`: `null` for foundation rules; `"extreme"` / `"high"` / `"medium"` / `"low"` for diagnostic/timing rules
- `disease_category`: See taxonomy below -- `null` for foundation rules
- `body_system`: Affected body system (see list below) -- `null` for foundation rules
- `aayu_bucket`: Always `null` for medical rules (longevity bucket is determined by the Longevity book rules, not here)
- `remedy_available`: `false` unless text explicitly states a remedy
- `remedy_ref_id`: `null`

### Disease Category Taxonomy (`disease_category` values)

```
cardiovascular | respiratory | neurological | reproductive | digestive
musculoskeletal | dermatological | mental | ophthalmic | renal
endocrine | haematological | oncological | infectious | metabolic
vata_disorder | pitta_disorder | kapha_disorder | general
```

### Body System Values (`body_system`)

```
head | eyes | ears | throat | cardiovascular | respiratory | digestive
hepatic | renal | reproductive | musculoskeletal | nervous | dermatological
haematological | endocrine | lymphatic | immune | general
```

---

## PART 4 -- Critical Distinction: Rules vs. Data Tables

**This is the single most important decision in this decode.**

The Medical Astrology book contains large volumes of mapping content that LOOKS like rules but is actually static lookup data. Misclassifying these as rules would produce hundreds of low-value atomic records that clog the rules collection.

### Goes into DATA TABLES (not rules):

| Content | Example | Table Name |
|---|---|---|
| Planet → body part list | Sun → heart, spine, right eye | Table 1.1: Planet-Body Part Assignments |
| Planet → disease list | Moon → phlegm, TB, lunacy | Table 1.2: Planet-Disease Correspondences |
| House → body part | 6th → intestines | Table 1.3: House-Body Part Assignments |
| Sign → body part | Aries → head | Table 1.4: Sign-Body Part Assignments |
| Nakshatra → organ | Ashwini → head/brain | Table 1.5: Nakshatra-Organ Assignments |
| Nakshatra → disease proneness | Bharani → reproductive | Table 1.6: Nakshatra-Disease Proneness |
| Planet → Tridosha | Mars → Pitta | Table 1.7: Planet-Tridosha Assignments |
| Sign → Tridosha | Aries → Pitta | Table 1.8: Sign-Tridosha Assignments |
| Nakshatra → Devata | Ashwini → Ashwini Kumaras | (reference only, low priority) |

### Goes into JSON RULES:

| Content | Example |
|---|---|
| Named yogas (multi-factor → disease) | "If Saturn aspects 6th lord + Moon in 12th → chronic mental illness" |
| Specific planet combination → disease | "Sun + Moon in 12th aspected by Saturn → blindness" |
| Lagna lord condition → disease type | "If Lagna lord in 6th with malefic aspect → chronic constitutional illness" |
| Disease duration by Nakshatra/Tithi | "Disease in Rohini Nakshatra is curable quickly; in Ardra it persists" |
| Dasha-based disease onset | "Disease manifests in dasha of 6th lord when transit Saturn aspects natal 6th" |
| Specific body system condition | "Mars in 8th aspected by Saturn → surgical intervention likely" |
| Female horoscopy conditions | "Moon afflicted by Rahu in 5th → miscarriage risk" |
| Drekkana-based diagnosis | "Malefic in 1st Drekkana of 6th → head/face disease" |
| Protective combinations | "Jupiter in Lagna with benefic aspect → strong immunity, disease resistance" |

---

## PART 5 -- Chapter Map, Priority & Expectations

**PDF folder:** `/Users/apple/Documents/Knowledge Engine_eBooks/Medical Astrology_Text Book/`

| Priority | Ch | PDF File | Pages | Topic | Content Type | Est. Rules | Part files? |
|---|---|---|---|---|---|---|---|
| 1 | 1 | `Chapter_01.pdf` | 43 | Introduction, Definitions & Yogas | Foundation mappings + named disease yogas | 50-80 | ✅ Yes (3 parts) |
| 2 | 8 | `Chapter_08.pdf` | 11 | Three Humours and Diseases | Tridosha-disease classification | 20-30 | Maybe |
| 3 | 9 | `Chapter_09.pdf` | 21 | Duration of Disease and Stars | Nakshatra/Tithi/Weekday timing rules | 25-35 | Maybe |
| 4 | 5 | `Chapter_05.pdf` | 12 | Female Horoscopy | Pregnancy, feminine disease conditions | 20-30 | No |
| 5 | 2 | `Chapter_02.pdf` | 30 | Problems with Progeny, Curses & Remedies | Karma/progeny combinations | 25-40 | Maybe |
| 6 | 6 | `Chapter_06.pdf` | 6 | Analysis of Horoscopes for Various Diseases | Practical diagnostic combinations | 10-15 | No |
| 7 | 11 | `Chapter_11.pdf` | 3 | Analysis through Drekkana | Divisional chart diagnostic rules | 10-15 | No |
| 8 | 4 | `Chapter_04.pdf` | 3 | Combinations for Sexual Weakness | Specific planet combinations | 8-12 | No |
| 9 | 10 | `Chapter_10.pdf` | 2 | Effective Vedic Remedy for Pediatric Problems | Remedy protocols | 5-8 | No |
| 10 | 3 | `Chapter_03.pdf` | 5 | Moksha & Son | Spiritual/philosophical domain | 5-8 | No |
| Benchmark | 7 | `Chapter_07.pdf` | 39 | Case Histories | 20 annotated charts -- benchmarks only | 0 rules | -- |
| Data ref | -- | `Index.pdf` | 13 | Index + Glossary | Reference only | 0 rules | -- |
| Cross-validate | -- | `Medical Astrology_Journal.pdf` | -- | Vedic mappings survey | Cross-validation after Ch1 | 0 new rules | -- |

**Chapter output size estimates:**

| Chapter | Est. Rules | Parts needed | Est. total files |
|---|---|---|---|
| Ch1 (43pp) | 50-80 | 3 parts | 6 |
| Ch8 (11pp) | 20-30 | Maybe 2 | 4-5 |
| Ch9 (21pp) | 25-35 | Maybe 2 | 4-5 |
| Ch5, Ch2, Ch6, Ch11, Ch4, Ch10, Ch3 | 5-40 | No | 4 each |

### Chapter 1 -- Detailed Sub-Section Map

Chapter 1 is the largest and most complex. Decode in this sub-order:

1. **Planets and their body domains** → Data Table 1.1 + 1.2
2. **Signs and body parts** → Data Table 1.4
3. **Houses and body parts** → Data Table 1.3
4. **Nakshatras and organs/diseases** → Data Tables 1.5 + 1.6
5. **Tridosha assignments** → Data Tables 1.7 + 1.8
6. **Named disease yogas (A-Z, 26 categories)** → JSON Rules (these ARE rules -- multi-factor yogas)
7. **Mental disease yogas** → JSON Rules
8. **Longevity combinations sub-section** → Flag for cross-reference with Longevity book; extract only if NOT already covered by a Longevity book rule

### Journal -- Cross-Validation Protocol

After Ch1 rules are written, read the Journal PDF. For each mapping in the Journal:
- If it matches a Ch1 Data Table entry → confirm, no action
- If it contradicts a Ch1 Data Table entry → flag in Chapter Diagnostic as "Contradiction: Journal vs. Text Book -- [detail]"
- If it adds a mapping NOT in the Text Book → add to the relevant Data Table with `source: "journal"`
- Do NOT create separate rules from Journal content

---

## PART 6 -- Decode Process (Per Chapter)

### Step 1 -- Read the chapter PDF fully before writing anything

Identify:
- How many distinct logical statements exist (rule count estimate)
- What is lookup data vs. diagnostic logic
- Which named yogas appear
- Any case charts to log as benchmarks

### Step 2 -- Write Data Tables first

Extract all static lookup content into Data Tables. Build the tables in the output file before the JSON rules array. Number tables: Table {NN}.1, {NN}.2...

### Step 3 -- Write JSON Rules

Write all diagnostic logic as rules. One rule per distinct condition-outcome pair. Self-audit each rule against the Quality Gate (Part 7) as you write it.

### Step 4 -- Write all 4 documents to file

**Write to file immediately. Do not accumulate output in the context window.**

File path: `/Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode/MedAstro_Ch{NN}_{ShortTitle}_Decoded.md`

Document structure in the file:
1. Technical Summary
2. Data Tables
3. JSON Rules (single unified array)
4. Chapter Diagnostic

### Step 5 -- Report status in context window only

After writing the file, post a brief status message:
> "Ch1 decoded. 47 rules, 8 data tables. File written to MedAstro_Ch01_DefinitionsYogas_Decoded.md. Proceeding to Ch8."

---

## PART 7 -- Quality Gate Checklist

Run on every rule before finalising the JSON. Fix before writing to file.

### Schema Checks

- [ ] `rule_id` format: `ma-ch{NN}-{NNN}` with correct chapter number
- [ ] `science_id` is `"vedic_astrology"` -- not `"kp_jyotish"`, not `"vedic_medical"`
- [ ] `active: true` present
- [ ] `approval_status: "pending_human_review"` present
- [ ] `checkable: false` present
- [ ] `source` block has all 7 fields including `sloka` and `passage_ref_id`
- [ ] `condition` block has all 9 fields including `planets_involved`, `houses_involved`, `aspect_condition`
- [ ] `result` block has all 6 fields including `disease_category` and `body_system`
- [ ] `yoga_name` present for named yogas; field omitted entirely for unnamed rules
- [ ] `maraka_houses` has actual value -- `[2, 7]` or `null` -- never blank

### Content Checks

- [ ] Mapping content (planet → disease, house → body part, nakshatra → organ) is in DATA TABLES, not rules
- [ ] Foundation/mapping rules: `severity: null`, `disease_category: null`, `body_system: null`
- [ ] Diagnostic/timing rules: `severity` populated, `disease_category` populated, `body_system` populated
- [ ] `aayu_bucket` is always `null` -- longevity determination is not in scope for this book
- [ ] No numeric coefficients in `full_text` -- intensity words only
- [ ] `claim_axis: "medical"` for all disease-related rules
- [ ] `science_id: "vedic_astrology"` -- not KP system
- [ ] No sub-lord logic in any rule -- this is not a KP book
- [ ] Case charts are logged as benchmarks, not decoded as rules

### Delivery Checks

- [ ] Output written to file, NOT to context window
- [ ] Single unified JSON array per chapter
- [ ] Status confirmation posted in context window after file write
- [ ] Data Tables written before JSON rules in the file

---

## PART 8 -- Exclusions Protocol

| Type | Action |
|---|---|
| Static lookup mappings (planet/house/nakshatra → body part or disease) | Data Table only |
| Named diagnostic yogas (multi-planet → specific disease) | JSON Rule |
| Disease duration by Nakshatra/Tithi/Weekday | JSON Rule (timing layer) |
| Spiritual commentary, karma theory, philosophical narrative | Discard |
| Remedy prescriptions (mantras, gemstones, yagnas) | Discard -- remedy layer not built yet. Set `remedy_available: true` on the associated rule if remedy is mentioned, but do not extract the remedy detail. |
| Curse/karmic combinations (Ch2, Ch3) | Park -- evaluate scope fit before extracting |
| Case study charts (Ch7) | Benchmark Test Case log only |
| Journal content that duplicates Text Book tables | Confirm only -- no new records |
| Journal content that contradicts Text Book | Flag in Diagnostic -- do not resolve unilaterally |

---

## PART 9 -- Benchmark Test Case Format

Log in Chapter Diagnostic under **"Benchmark Test Cases"**:

```
Chart: [Name, date, location]
Validates: [rule_id(s)]
Key data: [Relevant planet placements, dasha period, yoga triggered]
Author conclusion: [Disease identified and author's reasoning]
Disease category: [disease_category value]
```

---

## PART 10 -- Known Issues to Avoid (from Longevity Decode)

These failures occurred in the prior decode thread. Do not repeat:

1. **Writing output into context window** -- All output goes to files via Write tool. Context window = status only.
2. **`maraka_houses` left blank** -- Always `[2, 7]` or `null`. Never blank after the colon.
3. **Missing source block fields** -- `sloka` and `passage_ref_id` must always be present, even as `null`.
4. **Missing result block fields** -- All 6 fields required on every rule.
5. **`severity` on foundation rules** -- Always `null` on definition/mapping rules.
6. **Mapping content extracted as rules** -- Planet-disease, house-body, nakshatra-organ lists are DATA TABLES, not rules.
7. **Split JSON arrays** -- One unified array per chapter, always.
8. **First output incomplete** -- Read the entire chapter before writing any rules. Don't stop at obvious rules.
9. **Summary gate count not matching Diagnostic** -- Write Diagnostic first, count actual rules, then write Summary.

---

## PART 11 -- Decode Session Management

This book can be completed in 2-3 threads given chapter groupings:

| Thread | Chapters | Output Files |
|---|---|---|
| Thread A | Ch1, Ch8, Ch9 (core rules) | 3 files |
| Thread B | Ch4, Ch5, Ch11 (specific conditions) | 3 files |
| Thread C | Ch7 (20 benchmark charts) + Journal cross-validation | 2 files |

After each chapter: update the status column in Part 5 of this guide. Rule ID continuity must be maintained across threads -- check the last rule_id used before starting a new chapter.

---

## PART 12 -- Approval & Ingest Flow

1. CC writes chapter output to file
2. Human reviews file -- content check only
3. Rules ingested into MongoDB `interpretation_rules` with `approval_status: "pending_human_review"`
4. Co-founder approves via Library Console chapter by chapter
5. Only `"approved"` rules are read by the KE engine at runtime

**Nothing decoded here is live until explicitly approved.**
