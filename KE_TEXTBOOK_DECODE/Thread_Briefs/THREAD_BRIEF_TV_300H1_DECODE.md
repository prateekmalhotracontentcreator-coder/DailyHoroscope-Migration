# Thread Brief -- 300 Important Horoscopes Vol 1 Part 1: Case Study Decode
## KE Milestone 2 · Thread 3 · Test Vectors + Case-Derived Rules

> Prepared by: CC (Claude Code) + Temple Team
> Date: 2026-06-05 | Updated: 2026-06-05 (Step 2 Complete)
> Status: **✅ STEP 2 COMPLETE -- ALL 136 CHAPTERS DECODED · AWAITING TT REVIEW**
> Batch ID: `tv_300h1_decode_v1`
> Parallel threads: Thread 1 (Longevity), Thread 2 (765H), Thread 4 (300H Vol 2)

---

## One-Liner

Decode all 136 case study chapters from "300 Important Horoscopes Vol 1 Part 1" in a **single comprehensive pass** -- extracting everything needed for Layer A (engine calibration), Layer B (rule accuracy), and Layer C (gap detection + new rule candidates). PDFs are read exactly once.

---

## Source Book Details

| Field | Value |
|---|---|
| Book title | A Book of 300 Important Horoscopes Vol-1 Part-1 |
| Source PDF | `/Users/apple/Documents/Knowledge Engine_eBooks/5 New test Books/300 Horoscope Vol1/A Book of 300 imporant Horoscopes Vol-1-Part-1.pdf` |
| Split chapters | `/Users/apple/Documents/Knowledge Engine_eBooks/5 New test Books/300 Horoscope Vol1/Split_Chapters/` |
| Chapter range | Ch001-Ch136 (136 individual horoscope PDFs, 1 page each) |
| Output folder | `KE_TEXTBOOK_DECODE/Test_Vectors/JSON/300h1/` |

**Sample subjects in this book:**
Ch001 Abraham Lincoln · Ch002 A Girl Married Through Love Affair · Ch003 Lord Rama · Ch004 Barack Obama · Ch009 Hema Malini · Ch010 LB Shastri · Ch118 Martin Luther King · Ch135 Princess Diana · Ch136 Benigno Aquino · and 127 more spanning politics, judiciary, entertainment, sports, royalty, spiritual figures.

---

## What This Thread Produces

### Output 1: 136 Test Vector JSONs
One JSON file per chapter. See schema in Section 4.
File naming: `tv_300h1_ch{NNN}_{subject_name_snake}.json`

### Output 2: `300H1_CaseDerived_Rules.json`
New rules extracted from patterns across cases -- author observations that are NOT already covered by existing KE rules. Structured as KE rule candidates for a future ingest pass.

### Output 3: `300H1_Gap_Report.md`
Plain-language list of author observations with no KE rule match, prioritised by how many cases confirm the same pattern.

---

## Single Decode Pass -- What All Three Layers Need

```
Layer A input  →  birth data + stated lagna/moon sign
Layer B input  →  author_observations[] with condition_type_guess + claim_axis + gap_flag
Layer B expected → life_outcomes{} with known profession + key events (ground truth)
Layer C input  →  gap_flag: true observations → 300H1_CaseDerived_Rules.json
```

All fields extracted in one pass. CC runs chart computation (Layer A) and rule evaluation (Layer B) against the extracted JSON -- no second decode of any chapter.

---

## Schema Adjustments Confirmed (2026-06-05)

Based on Pre-Decode Q&A (`300h1/300H1_PreDecode_QA.md`), seven flags reviewed and decisions made:

| Flag | Decision | Change |
|---|---|---|
| F1 | ✅ CONFIRMED | Three birth data formats exist (labeled table / chart-embedded / intro paragraph). Body-longitude table = primary for planet positions always. Format A labeled table = primary for birth date/time. |
| F2 | ✅ DECIDED | ~33% birth times not OCR-recoverable → `time_confidence: "unknown"`, `time_local: null`. Do NOT back-infer time from Lagna degree. |
| F3 | ✅ CONFIRMED | Ch135 Diana: OCR reads 1901 → hard-correct to **1961**, flag `ocr_corrected: true`. Time: use book value (16:45), add `time_discrepancy_note` noting historical records suggest 19:45 BST. |
| F4 | ✅ CONFIRMED | **Pure KP framework** throughout. All `author_observations[]` tagged `science_id: "kp_jyotish"`. KP-specific `condition_type_guess` values approved -- see Section 3. |
| F5 | ✅ CONFIRMED | Lahiri ayanamsha confirmed from two labeled-table explicit values. No action needed. |
| F6 | ✅ CONFIRMED | 3-6 `author_observations[]` per chapter. Do not over-extract. Each distinct KP observation = one entry. Do not split a single sentence into sub-observations. |
| F7 | ✅ PROCEED | Obama engine check (Libra lagna, 04 Aug 1961, Honolulu) expected to pass. Does NOT gate full decode. TT can run in parallel. |
| S1 | ✅ UPDATED | Renamed `planet_positions_from_text` → `planet_positions_from_table`. Added `degree` (decimal) + `significations[]` per planet. Aligns with T1 (Longevity) schema. |
| S2 | ✅ ADDED | `ayanamsha_stated` in `birth_data` -- capture explicit ayanamsha value when Format A labeled table is present (e.g., `"23-47-10.50"`). Set `null` for Format B/C chapters. |
| New | ✅ ADDED | `kp_significations[]` in dasha object -- captures house numbers from the author's parenthetical notation e.g., `"Saturn-Saturn (05, 03, 08)"`. These are KP house significations of the dasha lord, NOT sub-period identifiers. |

See full combined review: `KE_TEXTBOOK_DECODE/Test_Vectors/COMBINED_PREDECODE_REVIEW.md`

---

## STEP 1 -- ✅ COMPLETE

Pre-Decode Q&A received and reviewed. **Proceed directly to Step 2 (full decode of all 136 chapters).**

Pre-Decode Q&A file: `KE_TEXTBOOK_DECODE/Test_Vectors/JSON/300h1/300H1_PreDecode_QA.md`

Key confirmed findings from Step 1:
- **Framework: Pure KP** -- zero BPHS terminology across all samples. No yoga names, no drishti.
- **Primary data source:** Body-longitude table (`Lagna → Ketu` with sign, degree, house, significations) -- reliably OCR'd on every page.
- Lagna is NEVER in narrative text -- always from body-longitude table or `Aa:` header line.
- ~2013 writing date established (Ch007: "boy is 12 years old as on 2013") -- use for live consultation case dasha timing.
- Dasha stated in ~50-70% of cases. Death cases reliably include dasha. Format: `MD-AD (house, house, house)`.

---

## STEP 1 ORIGINAL -- Pre-Decode Questions (ARCHIVED -- for reference only)

**Before decoding any full chapter, read 6-8 sample chapters spread across different subject types and answer ALL questions below. Return answers to TT. Only then proceed to full decode.**

```
THREAD: Read these as samples:
  Ch001_US_PRESIDENT_16_ABRAHAM_LINCOLN.pdf
  Ch004_US_PRESIDENT_44_BARACK_OBAMA.pdf
  Ch009_ACTRESS_AND_DANCER--HEMA_MALINI.pdf
  Ch010_INDIAN_PRIME_MINISTER--LB_SHASTRI.pdf
  Ch118_CIVIL_RIGHTS_ICON--MARTIN_LUTHER_KING.pdf
  Ch135_PRINCES_OF_WALES_--DIANA_SPENCER.pdf
  One chapter with a non-famous subject (e.g., Ch002, Ch005, Ch007)

Q1.  What is the exact format for birth data?
     Is it a labelled table, an inline paragraph, or embedded in the chart area?
     Paste the birth data section text verbatim from 2 different chapters.

Q2.  Is birth time stated for most entries? Exact (HH:MM) or approximate?
     Of your sample chapters, how many have exact time vs. approximate vs. no time?

Q3.  Does the author always explicitly state the lagna sign in the text body
     (e.g., "Capricorn lagna", "Tula lagna"), or is lagna only visible in the
     visual chart diagram?

Q4.  Ayanamsha check: take one well-known subject (Obama DOB 1961-08-04,
     07:24 HST, Honolulu Hawaii). Stated lagna in book vs. Lahiri-computed lagna.
     Do they match?

Q5.  What types of life outcomes does the author most commonly analyse?
     Rank by frequency across your samples: career / death / marriage / wealth /
     foreign travel / spiritual / other.

Q6.  Does the author reference the dasha or antardasha running during key events?
     Give a verbatim example from 1-2 chapters where dasha is mentioned.

Q7.  Typical author analysis length per case -- estimate word or paragraph count
     for Abraham Lincoln and one shorter case.

Q8.  Does the book primarily use BPHS framework, KP framework, or a mix?
     Clue: does the author mention "sub-lord", "cusp", "significator" (KP terms)
     or "house lord", "yoga", "lagna lord" (BPHS terms)?

Q9.  Are there any cases with more than one person on a single page?
     Any very short cases (less than half a page of author analysis)?

Q10. What OCR issues are visible?
     List any chapters with blurry text, garbled passages, or unreadable sections.

Q11. For non-famous subjects (Ch002 "A Girl Married Through Love Affair", etc.) --
     does the book provide any identifying information, or just birth data + analysis?

Q12. Does the book include the subject's age at the time of analysis, or is it
     purely a retrospective case study?
```

**Return answers as a structured reply before starting full decode.**

---

## STEP 2 -- ✅ COMPLETE (2026-06-05)

**Delivered to `KE_TEXTBOOK_DECODE/Test_Vectors/JSON/300h1/`:**
- 136 individual JSON test vectors (`tv_300h1_ch001_...` → `tv_300h1_ch136_...`)
- `300H1_CaseDerived_Rules.json` -- 4 gap rule candidates (kp_star_lord ×150 cases, kp_signification_chain ×10, etc.)
- `300H1_Gap_Report.md` -- field null-rate analysis + recommended TT actions

**Decode stats:** 136/136 chapters decoded · 0 errors · 55/136 lagna=null (chart-embedded OCR, expected) · ~40% time_local=null

**Key gap findings:**
- `kp_star_lord` (career): 150 observations across 136 chapters -- **primary KE gap**
- `kp_signification_chain` (career): 10 observations -- Rahu/Ketu proxy rule
- `kp_star_lord` (marriage, longevity): 3 observations total

**Awaiting TT:**
1. Engine verification -- run 5 sample chapters (Obama, Lincoln, Diana, Shastri, MLK) through vedic_calculator.py, populate `chart_verification.lagna_computed` / `moon_sign_computed` fields
2. Rule review -- approve/reject 4 gap candidates in `300H1_CaseDerived_Rules.json`
3. Ingest gate -- co-founder sign-off required before any ingest to `horoscope_db`

---

## STEP 2 ORIGINAL BRIEF -- Full Decode (✅ CLEARED TO START)

Decode ALL 136 chapters. Schema has been updated per Pre-Decode review -- see Section 5.

### Per-Chapter Decode Checklist

For each chapter, produce a JSON matching the schema in Section 5:

- [ ] `name` -- full name as stated in the book
- [ ] `description` -- profession or brief descriptor (e.g., "16th US President", "Indian Film Actress")
- [ ] `birth_data` -- date, time, place, lat/long, timezone, `ayanamsha_stated` (if Format A labeled table present)
- [ ] `time_confidence` -- `from_chart` / `rectified` / `approximate` / `unknown` (pre-1900 births → always `rectified`)
- [ ] `planet_positions_from_table` -- planet sign, degree, house, and significations[] from the body-longitude table (NOT the visual chart grid)
- [ ] `lagna_stated_in_book` -- sign as derived from body-longitude table `Lagna` row (e.g., `"Capricorn"`)
- [ ] `moon_sign_stated_in_book` -- from `Moon` row in table
- [ ] `life_outcomes` -- profession, key events with years, death data if applicable
- [ ] `author_observations[]` -- every distinct KP observation (3-6 per chapter); tag `science_id: "kp_jyotish"`
- [ ] `gap_flag` -- `true` if no matching KP rule exists in the existing KE for this observation

### Handling Missing Birth Times
- Birth time not OCR-recoverable (~33% of famous-subject chapters): `time_confidence: "unknown"`, `time_local: null`
- **Do NOT back-infer time from Lagna degree** -- circular reasoning
- Still extract all other fields -- these vectors are valid for Layer B/C even without exact time

### Handling Non-Famous Subjects
- For anonymous subjects (e.g., "A Girl Married Through Love Affair"): use chapter title as `name`
- Set `public_figure: false`; these are often the most analytically rich cases -- extract fully

### Live Consultation Cases (~2013 writing date)
- For present-tense narrative cases (Ch002, Ch005, Ch007 style): note `"consultation_type": "live_consultation"` in `notes`
- "Current" dasha year = ~2013 for these cases

### Death Cases
- Fill `death_data` block for all cases where death is mentioned (cause, date if given, age, death_type, dasha_at_death)
- death_type: `violent` / `accident` / `disease` / `suicide` / `natural` / `unknown`
- `dasha_at_death.kp_significations[]` -- capture house numbers from parenthetical notation (e.g., `"(05, 03, 08)"`)

### OCR Corrections
- Ch135 Diana: OCR reads year as 1901 → hard-correct to **1961**, set `ocr_corrected: true`; add `"time_discrepancy_note": "Historical records suggest 19:45 BST; book states 16:45"` for the time field

---

## 3. Author Observation Structuring

This book is **pure KP (Krishnamurti Paddhati)**. All observations use KP terminology -- star lord chains, signification tables, sub-lord analysis. Zero BPHS terminology (no yoga names, no drishti, no house-lord in house-X language).

For every KP claim the author makes, create one entry in `author_observations[]`:

**What to capture:**
> "Saturn is in star of Mars (violence); Mars significates 2 and 7 (maraka houses)" → one observation
> "Rahu offers result of Venus through Mercury; 07 and 10" → one observation
> "In the VMD of Jupiter-Sun-Jupiter, the native became President" → one observation (captures dasha + event)

**Each observation entry:**
```json
{
  "obs_id": "obs-001",
  "verbatim": "exact quote or close paraphrase from text",
  "condition_type_guess": "kp_star_lord | kp_sub_lord | kp_planet_signification | kp_signification_chain | planet_in_house | dasha_planet",
  "science_id": "kp_jyotish",
  "claim_axis": "career | marriage | wealth | longevity | spirituality | ...",
  "claim_polarity": "positive | negative | neutral",
  "gap_flag": false,
  "potential_rule_id": null
}
```

**KP `condition_type_guess` values to use:**

| Value | Use when |
|---|---|
| `kp_star_lord` | Planet-in-star-of-another-planet chain (e.g., "Saturn in star of Mars") |
| `kp_sub_lord` | Sub-lord signification drives outcome |
| `kp_planet_signification` | Planet significates a set of houses (from significations column) |
| `kp_signification_chain` | Multi-planet chain (e.g., "Rahu offers result of Venus through Mercury") |
| `planet_in_house` | Straightforward house placement |
| `dasha_planet` | Dasha lord triggering an event |

**`gap_flag: true`** when you cannot identify any KP rule in the existing KE that covers this condition + claim_axis combination. These become candidates for `300H1_CaseDerived_Rules.json`.

---

## 4. Case-Derived Rule Schema

For each `gap_flag: true` observation that generalises beyond the specific subject:

```json
{
  "rule_id": "300h1-cdr-{NNN}",
  "source": "case_study_derived",
  "source_book": "300 Important Horoscopes Vol 1 Part 1",
  "source_chapter": "Ch001_US_PRESIDENT_16_ABRAHAM_LINCOLN",
  "subject_name": "Abraham Lincoln",
  "observation_verbatim": "exact quote from text",
  "generalised_condition": {
    "type": "planet_in_house | dasha_planet | yoga_combination | ...",
    "planet": "SATURN",
    "house": 10,
    "additional_factors": []
  },
  "claim_axis": "career",
  "claim_polarity": "positive",
  "effect": "generalised rule statement -- not about Lincoln specifically",
  "confirmed_by_cases": ["tv-300h1-ch001"],
  "science_id": "kp_jyotish",
  "approval_status": "pending_human_review",
  "gap_in_existing_ke": true
}
```

**Multi-case confirmation:** When the same pattern appears in multiple chapters, list all chapter IDs in `confirmed_by_cases`. These are highest-priority new rules.

---

## 5. Test Vector JSON Schema (updated 2026-06-05 -- F1-F7 + S1/S2/New applied)

```json
{
  "vector_id": "tv-300h1-ch001",
  "book_id": "300_horoscopes_vol1_part1",
  "source_chapter": "Ch001_US_PRESIDENT_16_ABRAHAM_LINCOLN",
  "pdf_path": "Split_Chapters/Ch001_US_PRESIDENT_16_ABRAHAM_LINCOLN.pdf",
  "public_figure": true,

  "subject": {
    "name": "Abraham Lincoln",
    "description": "16th President of the United States",
    "nationality": "American"
  },

  "birth_data": {
    "date": "1809-02-12",
    "time_local": "07:32",
    "timezone_offset_hours": -6.0,
    "time_utc": "1809-02-12T13:32:00Z",
    "latitude": 37.5667,
    "longitude": -85.7167,
    "place": "Hodgenville, Kentucky, USA",
    "time_confidence": "rectified",
    "ayanamsha": "lahiri",
    "ayanamsha_stated": null,
    "ocr_corrected": false,
    "notes": "Pre-1900 birth -- time marked rectified per decode policy"
  },

  "chart_verification": {
    "lagna_stated_in_book": "Capricorn",
    "moon_sign_stated_in_book": "Capricorn",
    "lagna_computed": null,
    "moon_sign_computed": null,
    "engine_matches_book": null,
    "mismatch_notes": ""
  },

  "planet_positions_from_table": {
    "LAGNA":   { "sign": "Capricorn", "degree": null, "house": 1,  "significations": [1] },
    "SUN":     { "sign": null,        "degree": null, "house": null, "significations": [] },
    "MOON":    { "sign": "Capricorn", "degree": null, "house": 1,  "significations": [1, 11] },
    "MARS":    { "sign": null,        "degree": null, "house": null, "significations": [] },
    "MERCURY": { "sign": null,        "degree": null, "house": null, "significations": [] },
    "JUPITER": { "sign": null,        "degree": null, "house": null, "significations": [] },
    "VENUS":   { "sign": null,        "degree": null, "house": null, "significations": [] },
    "SATURN":  { "sign": null,        "degree": null, "house": null, "significations": [] },
    "RAHU":    { "sign": null,        "degree": null, "house": null, "significations": [] },
    "KETU":    { "sign": null,        "degree": null, "house": null, "significations": [] }
  },

  "life_outcomes": {
    "profession": "Politician",
    "profession_category": "Politics",
    "key_events": [
      { "event": "Elected 16th US President", "year": 1861 },
      { "event": "Assassination", "year": 1865 }
    ]
  },

  "death_data": {
    "cause_of_death": "Assassination -- shot by John Wilkes Booth",
    "death_type": "violent",
    "death_date": "1865-04-15",
    "age_at_death": 56,
    "dasha_at_death": {
      "mahadasha": null,
      "antardasha": null,
      "pratyantardasha": null,
      "sookshma": null,
      "kp_significations": [],
      "stated_by_author": false,
      "cc_computed": false,
      "raw_text": null
    }
  },

  "layer_b_expected": {
    "profession_category": "Politics",
    "key_claim_axes": ["career", "longevity"],
    "note": "Author analysis should yield career + death-related KP rule hits"
  },

  "author_observations": [
    {
      "obs_id": "obs-001",
      "verbatim": "exact quote or close paraphrase",
      "condition_type_guess": "kp_planet_signification",
      "science_id": "kp_jyotish",
      "claim_axis": "career",
      "claim_polarity": "positive",
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
    "notes": ""
  },

  "test_status": {
    "extraction_complete": false,
    "chart_computed": false,
    "rules_evaluated": false
  }
}
```

**Notes on updated schema fields:**
- `planet_positions_from_table`: Source is the body-longitude table (`Lagna → Ketu` rows) -- NOT narrative text or visual chart grid. Fill sign + degree + house + significations[] from this table. Use `null` only where the value is genuinely absent from the table.
- `ayanamsha_stated`: Fill from Format A labeled table only (e.g., `"23-47-10.50"`). Set `null` for Format B/C chapters.
- `dasha_at_death.kp_significations[]`: Capture house numbers from parenthetical notation. e.g., `"Saturn-Saturn (05, 03, 08)"` → `kp_significations: [5, 3, 8]`. These are the KP house significations of the dasha lord.
- `dasha_at_death.cc_computed`: Always `false` during extraction -- CC populates in Phase 4.
- `time_confidence: "rectified"` for all pre-1900 births.
- `death_data` block: Include for ALL cases where death is mentioned. Leave null values where not applicable.

---

## 6. Output Delivery

Deliver to `KE_TEXTBOOK_DECODE/Test_Vectors/JSON/300h1/`:

1. All 136 individual JSON files
2. `300H1_CaseDerived_Rules.json` -- new rule candidates
3. `300H1_Gap_Report.md` -- gap observations prioritised by case-count confirmation

**Do NOT ingest anything to MongoDB.** JSON output only. CC + TT review before any ingest.

---

## 7. Quality Standards

- `author_observations` must be real observations from the text -- not paraphrases of general astrology knowledge
- `observation_verbatim` must be a direct quote or very close paraphrase -- not a summary
- `gap_flag: true` requires you to have genuinely checked whether a matching KE rule exists
- Use `null` for missing fields -- not `""` or `"unknown"` for string fields
- Every JSON must be valid (no trailing commas, no smart quotes)
- For pre-1900 births: flag `time_confidence: "rectified"` unless book explicitly states the time as verified

---

*Thread 3 -- 300 Important Horoscopes Vol 1 Part 1 Decode*
*For schema questions: refer to `KE_TEXTBOOK_DECODE/Test_Vectors/TV_STRATEGY.md` Sections 4 and 5*
*All 4 Milestone 2 threads running in parallel*
