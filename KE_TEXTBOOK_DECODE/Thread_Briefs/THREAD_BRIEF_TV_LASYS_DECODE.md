# Thread Brief -- Longevity and Astro System: Full Case Study Decode
## KE Milestone 2 · Thread 5 · Test Vectors + Case-Derived Rules

> Prepared by: CC (Claude Code) + Temple Team
> Date: 2026-06-05
> Status: **✅ GREEN-LIT -- NO PRE-DECODE Q&A REQUIRED · PROCEED DIRECTLY TO STEP 2**
> Batch ID: `tv_lasys_decode_v1`
> Science: KP Jyotish (Krishnamurti Paddhati) -- same system as T1 (Longevity + Unnatural Deaths)

### Why No Pre-Decode Q&A?
All schema-critical questions are already answered:
- Ch25-Ch58 are fully benchmarked in `Longevity_Benchmarks_CaseStudies_Ch25-58.md` (used as reference -- see Section 1B)
- KP format confirmed: star lord / sub lord / cuspal sub lord tables, VMD at death, same as T1
- OCR quality confirmed via prior decode: readable body-longitude tables, ayanamsha in sidebar
- Chapter scope confirmed by direct PDF inspection: Ch20 + Ch29 are intro-only (0 cases), all others have ≥1 case

---

## One-Liner

Decode all case study chapters (Ch21-Ch58, skipping intros Ch20+Ch29) from "Longevity and Astro System" in a **single comprehensive pass** -- extracting everything needed for Layer A (birth data + aayu bucket classification), Layer B (KP rule accuracy testing), and Layer C (gap detection). For Ch25-Ch58, the existing benchmark file is the primary reference; thread verifies against PDF and structures into TV JSON format.

---

## Section 1A -- Source Book Details

| Field | Value |
|---|---|
| Book title | Longevity and Astro System |
| Author framework | Krishnamurti Paddhati (KP Jyotish) |
| `book_id` | `longevity_astro_system_v1_20260605` |
| `science_id` | `kp_jyotish` |
| Source PDFs | `/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/LongevityAstroSystem/` |
| Each chapter is a separate PDF | Named `{ChN}_{Title}.pdf` |
| Output folder | `KE_TEXTBOOK_DECODE/Test_Vectors/JSON/longevity_astro_system/` |
| Related prior decode | `Longevity_Benchmarks_CaseStudies_Ch25-58.md` (rules + benchmark log -- use as reference) |

**Case Study Chapter Range:**

| Chapters | Type | Count | Notes |
|---|---|---|---|
| Ch20 | Intro -- Balarishta definition | 0 cases | Skip -- no birth data |
| Ch21-Ch24 | Balarishta (infant mortality) | 4 cases | Decode fresh from PDF |
| Ch25 | Twins (Balarishta) | 2 cases | CS-01 Elder, CS-02 Younger |
| Ch26-Ch28 | Balarishta / early death | 3 cases | |
| Ch29 | Intro -- Alpa Aayu definition | 0 cases | Skip -- 1-page intro only |
| Ch30-Ch35 | Alpa Aayu (8-33 years) | 6 cases | |
| Ch36-Ch48 | Madhya Aayu (33-75 years) | 13 cases | Ch39+Ch46: rotation technique |
| Ch49-Ch58 | Purna / Aparimita / Blind | 10 cases | Ch50: rotation technique |
| Rotation sub-charts | Spouse/parent analysis | +3 | Ch39 Rajiv, Ch46 Rajiv, Ch50 Mother |
| **Total** | | **~44 entries** | User-estimated ~50 (sub-cases may add) |

**Notable subjects:**
Ch25 Twins (Bangalore) · Ch26 Franklin Roosevelt Jr. · Ch31 Alexei Nikolaevich · Ch33 Maria Romanov · Ch34 Lee Harvey Oswald · Ch35 Luís Filipe (Crown Prince) · Ch36 Marilyn Monroe · Ch38 Sanjay Gandhi · Ch39 Maneka Gandhi · Ch40 Swami Vivekananda · Ch43 JFK · Ch45 Christina Onassis · Ch46 Sonia Gandhi · Ch49 Sirhan Sirhan · Ch51 John Hinckley Jr. · Ch52 M. Visweswaraya · Ch53 Herbert Hoover · Ch54 Rose Kennedy · Ch55 Jeanne Calment

---

## Section 1B -- ⭐ HEAD-START REFERENCE (Critical -- Read This First)

**Ch25-Ch58 benchmark data already exists. Do NOT re-derive from scratch.**

The prior CC decode of this book produced:
```
/Users/apple/Documents/Knowledge Engine_eBooks/Longevity_CC_Decode/
  Longevity_Benchmarks_CaseStudies_Ch25-58.md   ← PRIMARY REFERENCE for Ch25-58
  Longevity_CaseStudies_Ch36-58_Diagnostic.md   ← Supplementary diagnostic
  Longevity_CaseStudies_Ch36-58_Rules.json       ← 21 extracted rules (context)
```

**How to use the benchmark file:**
1. Open `Longevity_Benchmarks_CaseStudies_Ch25-58.md`
2. Find the chapter section (e.g., `## Ch43 -- John Fitzgerald Kennedy`)
3. The benchmark entry has: birth data, planet table, lagna CSL, 8th CSL, badhaka house, VMD at death, aayu bucket, and rules validated
4. Populate the TV JSON fields from this data -- **then verify each key field against the PDF** (spot-check birth date, lagna, 8th CSL, VMD)
5. If PDF contradicts benchmark, trust the PDF and note the discrepancy

**Ch21-Ch24 have NO prior benchmark data.** Decode these chapters fresh from their PDF files.

---

## What This Thread Produces

### Output 1: ~44 Test Vector JSONs
One JSON file per subject (rotation sub-charts = separate JSON files).
File naming: `tv_lasys_ch{NN}_{subject_snake_case}.json`
Rotation sub-charts: `tv_lasys_ch{NN}b_{subject_snake_case}.json`
Output folder: `KE_TEXTBOOK_DECODE/Test_Vectors/JSON/longevity_astro_system/`

Examples:
- `tv_lasys_ch21_balarishta_chart_i.json`
- `tv_lasys_ch25a_twin_i_elder.json`
- `tv_lasys_ch25b_twin_ii_younger.json`
- `tv_lasys_ch43_jfk.json`
- `tv_lasys_ch39a_maneka_gandhi.json`
- `tv_lasys_ch39b_rajiv_gandhi_rotation.json`

### Output 2: `LASYS_CaseDerived_Rules.json`
New KP rule candidates from patterns across cases -- conditions the author identifies that are NOT already covered in the existing KE. Structured as KE rule candidates, `approval_status: pending_human_review`.

### Output 3: `LASYS_Gap_Report.md`
Author observations with no matching rule in current KE -- prioritised by case-count confirmation.

---

## STEP 2 -- Full Decode Instructions

### Decode Order (recommended)

1. **Ch21-Ch24 first** (fresh decode, Balarishta cases, simple format)
2. **Ch25-Ch35** (Balarishta + Alpa Aayu, use benchmark reference)
3. **Ch36-Ch58** (Madhya/Purna/Aparimita, use benchmark reference)

### Per-Chapter Decode Checklist

For each chapter, produce a JSON matching the schema in Section 4:

- [ ] `birth_data` -- date, time, timezone, place, lat/long, ayanamsha
- [ ] `chart_verification.lagna_stated_in_book` -- exactly as author states
- [ ] `kp_cuspal_data.lagna_csl` -- Lagna Cusp Sub Lord (always stated in KP books)
- [ ] `kp_cuspal_data.8th_csl` -- 8th House Cusp Sub Lord (key longevity gate)
- [ ] `kp_cuspal_data.badhaka_house` -- derived from lagna type (moveable/fixed/dual)
- [ ] `kp_cuspal_data.maraka_houses` -- typically [2, 7] (confirm from text)
- [ ] `aayu_bucket_stated` -- author's classification (Balarishta/Alpa/Madhya/Purna/Aparimita)
- [ ] `planet_positions_from_table` -- sign + house + significations[] (from KP body-longitude table)
- [ ] `death_data` -- cause, date, age, death_type
- [ ] `dasha_at_death` -- VMD stated by author (expected: ~95% coverage in this book)
- [ ] `author_observations` -- each distinct claim the author makes, structured
- [ ] `gap_flag` -- true if observation has no matching KE rule

### Handling Rotation Technique Chapters (Ch39, Ch46, Ch50)

These chapters analyse longevity of a **related person** (spouse or parent) by rotating the birth chart:
- **Ch39**: Maneka Gandhi (primary subject) + Rajiv Gandhi (spouse, via 7th house rotation)
- **Ch46**: Sonia Gandhi (primary subject) + Rajiv Gandhi (spouse, via 7th house rotation)
- **Ch50**: Native (primary subject, unnamed) + Mother (via 4th house rotation)

**Rule:** Produce **two separate JSON files** per rotation chapter:
1. **Primary subject** (`_a` suffix) -- normal birth chart decode
2. **Rotation subject** (`_b` suffix) -- birth data from the rotated chart as stated in the chapter

For the rotation JSON, set:
```json
"rotation_technique": {
  "is_rotation_chart": true,
  "rotation_type": "7th_house",
  "primary_subject_vector_id": "tv-lasys-ch39a",
  "rotation_rationale": "Spouse longevity derived by treating 7th cusp as lagna"
}
```

### Handling Blind Chart (Ch58)

Ch58 is a "prediction for a person born now" -- no historical death data. Extract birth data and author's predicted aayu bucket. Set `death_data: null` and add `"is_blind_chart": true` at top level. Phase 4 will compute the predicted aayu bucket from the engine and compare.

### Handling Missing Death Data (Survival cases)

Sirhan Sirhan (Ch49), John Hinckley Jr. (Ch51), Robert Marchand (Ch56 -- alive at decode time):
- Set `death_data.death_date: null` and `death_data.death_type: "survived"`
- Set `aayu_bucket_stated` to author's bucket (Purna/Aparimita)
- These validate the ENGINE'S POSITIVE longevity call -- equally important as the death cases

---

## 3. Case-Derived Rule Extraction (LASYS-Specific)

The author's primary rule framework in this book is:

**Gate 1 -- Balarishta Gate:**
If 8th CSL's star lord or sub lord is in badhaka / maraka house → infant mortality risk

**Gate 2 -- Aayu Bucket Determination:**
- Lagna CSL's star lord planet's house significations → determines life bracket
- Badhaka lord placement + 8th CSL + Lagna CSL → triangulate bucket

**Gate 3 -- DBAS (Dasha-Bhukti-Antara-Sookshma) Override:**
- VMD at actual death must be lords of badhaka + maraka + 8th house

Flag every statement where the author demonstrates:
> "[KP condition X] placed subject in [aayu bucket Y] / caused [longevity outcome Z]"

These become candidates for `LASYS_CaseDerived_Rules.json`.

**Schema for each LASYS Case-Derived Rule:**
```json
{
  "rule_id": "lasys-cdr-{NNN}",
  "source": "case_study_derived",
  "source_book": "Longevity and Astro System",
  "source_chapter": "Ch43",
  "subject_name": "John F. Kennedy",
  "observation_verbatim": "exact quote from the text",
  "generalised_condition": {
    "type": "kp_csl | kp_star_lord | kp_signification_chain",
    "house_csl": 8,
    "csl_planet": "MERCURY",
    "csl_star_lord_planet": "SUN",
    "additional_factors": []
  },
  "claim_axis": "longevity",
  "aayu_gate": "gate_1 | gate_2 | gate_3",
  "aayu_bucket_outcome": "balarishta | alpa | madhya | purna | aparimita",
  "confirmed_by_cases": ["tv-lasys-ch43"],
  "science_id": "kp_jyotish",
  "approval_status": "pending_human_review",
  "gap_in_existing_ke": true
}
```

---

## 4. Test Vector JSON Schema

```json
{
  "vector_id": "tv-lasys-ch43",
  "book_id": "longevity_astro_system_v1_20260605",
  "source_chapter": "Ch43",
  "chapter_title": "John Fitzgerald Kennedy -- Madhya Aayu",
  "pdf_path": "Text Books/LongevityAstroSystem/43_John Fitzgerald Kennedy-Madhya Aayu.pdf",
  "is_blind_chart": false,

  "subject": {
    "name": "John F. Kennedy",
    "description": "35th US President, assassinated 1963",
    "nationality": "American"
  },

  "birth_data": {
    "date": "1917-05-29",
    "time_local": "15:09:00",
    "timezone_offset_hours": -5.0,
    "time_utc": "1917-05-29T20:09:00Z",
    "latitude": 42.3317,
    "longitude": -71.1214,
    "place": "Brookline, Massachusetts, USA",
    "time_confidence": "from_chart",
    "ayanamsha": "lahiri",
    "ayanamsha_stated": "22-42-12.76",
    "notes": ""
  },

  "chart_verification": {
    "lagna_stated_in_book": "Virgo",
    "moon_sign_stated_in_book": "Leo",
    "lagna_computed": null,
    "moon_sign_computed": null,
    "engine_matches_book": null,
    "mismatch_notes": ""
  },

  "kp_cuspal_data": {
    "lagna_csl": "MOON",
    "8th_csl": "MARS",
    "badhaka_house": 11,
    "badhaka_house_rationale": "Virgo = dual lagna → 7th house is badhaka",
    "maraka_houses": [2, 7]
  },

  "aayu_bucket_stated": "madhya",
  "aayu_bucket_computed": null,

  "planet_positions_from_table": {
    "LAGNA":   { "sign": "Virgo",      "degree": 29.08, "house": 1,  "significations": [1] },
    "SUN":     { "sign": "Gemini",     "degree": 14.50, "house": 10, "significations": [10, 1] },
    "MOON":    { "sign": "Leo",        "degree": 24.58, "house": 12, "significations": [12, 2] },
    "MARS":    { "sign": "Aries",      "degree": 25.20, "house": 8,  "significations": [8, 3] },
    "MERCURY": { "sign": "Taurus",     "degree": 27.88, "house": 9,  "significations": [9, 12] },
    "JUPITER": { "sign": "Capricorn",  "degree": 15.12, "house": 5,  "significations": [5, 2] },
    "VENUS":   { "sign": "Gemini",     "degree": 16.33, "house": 10, "significations": [10, 11] },
    "SATURN":  { "sign": "Cancer",     "degree": 27.45, "house": 11, "significations": [11, 6] },
    "RAHU":    { "sign": "Capricorn",  "degree": 14.22, "house": 5,  "significations": [5, 8] },
    "KETU":    { "sign": "Cancer",     "degree": 14.22, "house": 11, "significations": [11, 2] }
  },

  "death_data": {
    "cause_of_death": "Assassination",
    "death_type": "violent",
    "death_date": "1963-11-22",
    "age_at_death": 46,
    "dasha_at_death": {
      "mahadasha": "JUPITER",
      "antardasha": "SATURN",
      "pratyantardasha": null,
      "sookshma": null,
      "kp_significations": [],
      "stated_by_author": true,
      "cc_computed": false,
      "raw_text": "Jupiter-Saturn period"
    }
  },

  "rotation_technique": null,

  "author_observations": [
    {
      "obs_id": "obs-001",
      "verbatim": "exact quote from author analysis",
      "aayu_gate": "gate_2",
      "condition_type_guess": "kp_csl",
      "claim_axis": "longevity",
      "claim_polarity": "negative",
      "gap_flag": false,
      "potential_rule_id": null
    }
  ],

  "rule_evaluation": {
    "evaluated": false,
    "evaluated_at": null,
    "rules_fired": [],
    "layer_a_pass": null,
    "layer_b_pass": null,
    "timing_precision_pass": null,
    "rule_precision_score": null,
    "judge_score": null,
    "false_positive_flag": false,
    "notes": ""
  },

  "test_status": {
    "extraction_complete": false,
    "chart_computed": false,
    "rules_evaluated": false
  }
}
```

**Rotation sub-chart example (Ch39b -- Rajiv Gandhi via 7th house rotation from Maneka's chart):**
```json
{
  "vector_id": "tv-lasys-ch39b",
  "book_id": "longevity_astro_system_v1_20260605",
  "source_chapter": "Ch39",
  "chapter_title": "Longevity of Spouse -- Maneka Gandhi (7th House Rotation for Rajiv)",
  "pdf_path": "Text Books/LongevityAstroSystem/39_Longevity of spouse-Maneka Gandhi.pdf",
  "is_blind_chart": false,

  "subject": {
    "name": "Rajiv Gandhi",
    "description": "Spouse of Maneka Gandhi -- analysed via 7th house rotation",
    "nationality": "Indian"
  },

  "rotation_technique": {
    "is_rotation_chart": true,
    "rotation_type": "7th_house",
    "primary_subject_vector_id": "tv-lasys-ch39a",
    "rotation_rationale": "Spouse longevity derived by treating Maneka's 7th cusp as rotated lagna",
    "rotated_lagna": null
  },

  "birth_data": {
    "date": "1944-08-20",
    "time_local": null,
    "timezone_offset_hours": null,
    "time_utc": null,
    "latitude": null,
    "longitude": null,
    "place": "India",
    "time_confidence": "from_rotation_technique",
    "notes": "Birth data derived via 7th house rotation from Maneka Gandhi's chart"
  }
}
```

**Blind chart example (Ch58):**
```json
{
  "vector_id": "tv-lasys-ch58",
  "is_blind_chart": true,
  "aayu_bucket_stated": "madhya",
  "death_data": null,
  "notes": "Author predicts aayu bucket for person born at decode time. Phase 4 validates engine prediction vs author prediction."
}
```

---

## 5. Aayu Bucket Reference

| Bucket | Life Span | `aayu_bucket_stated` value |
|---|---|---|
| Balarishta | 0-8 years (infant mortality) | `"balarishta"` |
| Alpa Aayu | 8-33 years (short life) | `"alpa"` |
| Madhya Aayu | 33-75 years (middle life) | `"madhya"` |
| Purna Aayu | 75-100 years (full life) | `"purna"` |
| Aparimita Aayu | 100+ years (super centenarian) | `"aparimita"` |

---

## 6. Badhaka House Reference (KP)

| Lagna Type | Lagna Signs | Badhaka House |
|---|---|---|
| Moveable (Chara) | Aries, Cancer, Libra, Capricorn | 11th |
| Fixed (Sthira) | Taurus, Leo, Scorpio, Aquarius | 9th |
| Dual (Dwiswabhava) | Gemini, Virgo, Sagittarius, Pisces | 7th |

---

## 7. Death Type Classification

| Value | Use when |
|---|---|
| `violent` | Assassination, shooting, stabbing, bombing |
| `accident` | Car crash, plane crash, drowning, fall |
| `disease` | Cancer, heart disease, illness |
| `suicide` | Confirmed or strongly indicated |
| `natural` | Old age, natural causes |
| `survived` | Subject is alive (Sirhan Sirhan, Hinckley, Marchand) |
| `unknown` | Not clear from text |

---

## 8. Phase 4 Computation Plan (CC runs after delivery)

When all ~44 JSONs are delivered, CC runs:

| Step | Action | Field Populated |
|---|---|---|
| Layer A-1 | `vedic_calculator.py` → compute lagna | `chart_verification.lagna_computed` |
| Layer A-2 | Compare lagna_computed vs lagna_stated_in_book | `chart_verification.engine_matches_book` |
| Layer A-3 | NEW: Validate aayu_bucket vs KP Gates 1-3 | `aayu_bucket_computed` |
| Layer B | `scan_chart()` → rules fired vs author observations | `rule_evaluation.rules_fired` |
| Layer B scoring | Jaccard rule precision | `rule_evaluation.rule_precision_score` |
| Layer B scoring | LLM-as-Judge (1-5 rubric) | `rule_evaluation.judge_score` |
| Layer C | Aggregate `gap_flag: true` observations → LASYS gap report | `LASYS_Gap_Report.md` |

**KP-specific Layer A-3 (new gate for LASYS):**
Engine computes: which aayu bucket does the chart fall in based on KP rules?
If `aayu_bucket_computed == aayu_bucket_stated` → Layer A-3 pass.
Target: ≥90% match rate across all ~44 cases.

---

## 9. Output Delivery Checklist

At the end of decode, deliver:
1. All ~44 JSON files → `KE_TEXTBOOK_DECODE/Test_Vectors/JSON/longevity_astro_system/`
2. `LASYS_CaseDerived_Rules.json` → same folder
3. `LASYS_Gap_Report.md` → same folder

**Do NOT ingest anything to MongoDB.** JSON output only. CC + TT will review before any ingest.

---

## 10. Quality Standards

- Every JSON must validate against the schema (no missing required fields)
- `lagna_csl` and `8th_csl` are mandatory -- if not stated in text, set `null` and add extraction_note
- `observation_verbatim` must be a quote or close paraphrase -- not a summary
- `aayu_bucket_stated` is mandatory for every chapter
- If data is missing from the PDF: use `null` not `""` for string fields
- Flag uncertain extractions with `"extraction_note": "..."` field

---

*Thread 5 -- Longevity and Astro System Test Vector Decode*
*Parallel threads: T1-T4 all complete. T5 is the final thread in KE Milestone 2.*
*For questions or schema clarifications: raise with TT before proceeding*
