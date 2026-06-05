# Thread Brief -- Longevity + Unnatural Deaths: Full Case Study Decode
## KE Milestone 2 · Thread 1 · Test Vectors + Case-Derived Rules

> Prepared by: CC (Claude Code) + Temple Team
> Date: 2026-06-05 | Updated: 2026-06-05 (Step 2 Complete)
> Status: **✅ STEP 2 COMPLETE -- 93 TEST VECTORS DELIVERED · AWAITING TT REVIEW**
> Batch ID: `tv_lu_decode_v1`
> Parallel thread: Thread 2 (765 Notable Horoscopes) running simultaneously

### Step 2 Delivery Summary (2026-06-05)
| Item | Status | Detail |
|---|---|---|
| 93 test-vector JSONs | ✅ DELIVERED | `KE_TEXTBOOK_DECODE/Test_Vectors/JSON/longevity_unnatural/tv_lu_ch07_*` - `tv_lu_ch99_*` |
| `LU_CaseDerived_Rules.json` | ✅ DELIVERED | 183 rule candidates · all `approval_status: pending_human_review` |
| `LU_Gap_Report.md` | ✅ DELIVERED | 183 observations with no current KE rule match |
| Decode script | ✅ SAVED | `KE_TEXTBOOK_DECODE/decode_longevity_unnatural.py` |
| **Coverage** | 93/93 · 0 errors | 91 chapters vmd=True · 90 birth=True · 87+ full 10-planet tables |
| **Exceptions flagged** | Ch25/Ch26/Ch28 | Birth chart image-only -- KP table not extractable via OCR |
| **Exceptions flagged** | Ch24/Ch53/Ch63/Ch79/Ch87 | Birth date OCR-garbled (year mangled in scan) |
| **MongoDB ingest** | ❌ NOT DONE | Per brief: JSON output only. CC+TT review before any ingest. |

---

## One-Liner

Decode all 93 case study chapters from "Longevity and Unnatural Deaths" in a **single comprehensive pass** -- extracting everything needed for Layer A (birth data for chart computation), Layer B (author observations for rule accuracy testing), and Layer C (gap detection for new rule candidates). The PDFs are read exactly once.

**What "single pass" means:** The thread extracts all fields in each JSON fully. CC then runs chart computation (Layer A) and rule evaluation (Layer B) against the already-extracted JSON -- no second decode of any chapter is ever needed.

---

## Source Book Details

| Field | Value |
|---|---|
| Book title | Longevity and Un-Natural Deaths |
| Source PDF | `/Users/apple/Documents/Knowledge Engine_eBooks/5 New test Books/Longevity and Unnatural Deaths/Longevity and Un-Natural Deaths.pdf` |
| Split chapters | `/Users/apple/Documents/Knowledge Engine_eBooks/5 New test Books/Longevity and Unnatural Deaths/Chapter_Splits/` |
| Chapter range | Ch07-Ch99 (93 chapters, Ch01-06 not in scan) |
| Output folder | `KE_TEXTBOOK_DECODE/Test_Vectors/JSON/longevity_unnatural/` |
| Note | Ch07 (Garfield) is partially present -- starts from book page 31. Chapters 1-6 are NOT in the scan (Abraham Lincoln, MK Gandhi, James Garfield p.30 missing) |

**Notable subjects in this book:**
Ch08 Osama Bin Laden · Ch09 Rajiv Gandhi · Ch10 William McKinley · Ch11 John F. Kennedy · Ch12 Indira Gandhi · Ch14 Robert F. Kennedy · Ch15 JFK Jr. · Ch17 Ronald Reagan · Ch18 Sanjay Gandhi · Ch96 Virginia Woolf · Ch99 John Lennon · and 82 more.

---

## What This Thread Produces

### Output 1: 93 Test Vector JSONs
One JSON file per chapter. See schema in Section 4 below.
File naming: `tv_lu_ch{NN}_{subject_name_snake}.json`

### Output 2: `LU_CaseDerived_Rules.json`
New rules extracted from patterns across cases -- conditions the author identifies that are NOT already covered in the existing KE textbook rules. These are structured as KE rule candidates for a future ingest pass.

### Output 3: `LU_Gap_Report.md`
Plain-language list of author observations that have NO matching rule in the current KE -- prioritised by how many cases confirm the same pattern.

---

## STEP 1 -- MANDATORY FIRST: Answer Pre-Decode Questions

**Before decoding any full chapter, read 5-8 sample chapters from the split folder and answer ALL questions below. Return answers to TT. CC + TT will review and confirm schema adjustments. Only then proceed to full decode.**

```
THREAD: Read these chapters first as samples:
  Ch07_James_Abram_Garfield.pdf
  Ch11_John_F_Kennedy.pdf
  Ch12_Indira_Gandhi.pdf
  Ch17_Ronald_Reagan.pdf
  Ch88_Amitabh_Bachchan.pdf
  Ch99_John_Lennon.pdf

Q1.  What is the exact format for birth data? Table with labelled fields? Inline paragraph?
     Paste the birth data section text from 2 different chapters.

Q2.  Is birth time stated for most entries? Approximate or exact?
     How many of your 6 sample chapters have exact birth time (HH:MM) vs. approximate?

Q3.  Does the book state ayanamsha used? Check if book-stated lagna matches
     Lahiri computation for JFK (DOB 1917-05-29, ~03:00 EST, Brookline MA).
     Report: stated lagna vs. Lahiri-computed lagna.

Q4.  Are house cusps given numerically, or only the visual chart diagram?

Q5.  Does the author always explicitly state the lagna in text (e.g., "Gemini lagna")?
     Or is lagna only visible in the chart grid diagram?

Q6.  Is the death information always explicitly stated?
     e.g., "died on [date] at age [X] due to [cause]"
     Or is it implied? Give 1-2 example sentences from actual chapters.

Q7.  Does the author always name the dasha/antardasha running at time of death?
     Give verbatim example from 2 chapters.

Q8.  Does the author use BPHS terminology (8th lord, maraka, badhaka) explicitly,
     KP terminology (CSL, sub-lord, significator), or a mixed framework?

Q9.  What is the typical analysis length per case?
     Estimate: word count or paragraph count for JFK and one short case.

Q10. Are there any chapters with 2 or more persons on the same page?
     Are there any very short entries (less than half a page)?

Q11. What OCR issues are visible? (blurry pages, garbled paragraphs, missing text)?
     List any chapters where the text is partially unreadable.

Q12. Are planet positions in the visual chart diagram always consistent with
     what the author states in text? (spot-check 1-2 charts)
```

**Return answers as a structured reply before starting full decode.**

---

## Schema Adjustments Confirmed (2026-06-05)

Based on Pre-Decode Q&A (PRE_DECODE_QA_TV_LONGEVITY.md), four schema flags approved plus two additions:

| Flag | Decision | Change |
|---|---|---|
| S1 | ✅ APPROVED | Add `life_events[]` array for non-terminal events; `death_data{}` = terminal death only |
| S2 | ✅ APPROVED | VMD stored as structured object `{mahadasha, antardasha, pratyantardasha, sookshma, stated_by_author, raw_text}` -- not raw string |
| S3 | ✅ APPROVED | Use `birth_data.notes` for Ch07 partial-chapter extraction note |
| S4 | ✅ APPROVED | Hard rule: planet positions always from KP Body table -- chart header line is cross-check only |
| +1 | ✅ ADDED | `birth_data.ayanamsha_stated` -- capture exact ayanamsha value from sidebar (e.g., `"22-42-12.76"`) |
| +2 | ✅ ADDED | `planet_positions_from_table` (renamed from `_from_text`) -- add `degree` (decimal) + `significations[]` (KP house list) per planet |

See Section 4 below for updated full schema.

---

## STEP 2 -- Full Decode

After TT + CC confirm the Pre-Decode answers, decode ALL 93 chapters.

### Per-Chapter Decode Checklist
For each chapter, produce a JSON matching the schema in Section 4:

- [ ] `birth_data` -- date, time, place, lat/long (look up coordinates if not stated)
- [ ] `lagna_stated` -- exactly as the author states it (e.g., "Gemini", "Taurus")
- [ ] `moon_sign_stated` -- if stated
- [ ] `death_data` -- cause, date, age, death_type classification
- [ ] `dasha_at_death` -- mahadasha + antardasha running at time of death (if stated)
- [ ] `planet_positions` -- planet in house, extracted from text (not the visual grid)
- [ ] `author_observations` -- each distinct claim the author makes, structured
- [ ] `rule_observation_raw` -- verbatim key sentences that constitute rule statements
- [ ] `gap_flag` -- true if the observation has no matching KE rule you can identify

### Handling Missing Birth Times
- If birth time is not stated or clearly approximate: set `time_confidence: "approximate"` or `"unknown"`
- Do NOT invent or guess birth times
- Still extract all other data -- these vectors are usable for Layer C even without exact time

### Handling Missing Death Data
- If cause of death is unclear from the text: set `cause_of_death: null` and `death_type: "unknown"`
- Note what IS present in the `author_notes` field

---

## 3. Case-Derived Rule Extraction

While decoding, flag every statement where the author says (explicitly or implicitly):
> "[Planetary condition X] caused / indicates / explains [life outcome Y]"

These become candidates for `LU_CaseDerived_Rules.json`.

**Examples of extractable rule statements:**
- "Mars as 8th lord in the lagna caused violent death" → condition: Mars 8th lord in house 1
- "Saturn and Rahu in the 8th house with no benefic aspect -- death by drowning" → condition: Saturn + Rahu in house 8
- "Dasha of 2nd lord running at the time of death indicates maraka activated" → condition: 2nd lord dasha

**Schema for each Case-Derived Rule:**
```json
{
  "rule_id": "lu-cdr-{NNN}",
  "source": "case_study_derived",
  "source_book": "Longevity and Unnatural Deaths",
  "source_chapter": "Ch11_John_F_Kennedy",
  "subject_name": "John F. Kennedy",
  "observation_verbatim": "exact quote from the text",
  "generalised_condition": {
    "type": "planet_in_house | planet_aspect | dasha_planet | ...",
    "planet": "MARS | SATURN | ...",
    "house": 8,
    "additional_factors": []
  },
  "claim_axis": "longevity",
  "claim_polarity": "negative",
  "effect": "generalised rule statement (not about Kennedy specifically)",
  "confirmed_by_cases": ["tv-lu-ch11"],
  "science_id": "jyotish | kp_jyotish",
  "approval_status": "pending_human_review",
  "gap_in_existing_ke": true
}
```

**When the same pattern appears in MULTIPLE chapters:** Set `confirmed_by_cases` to all chapter IDs. Multi-case confirmation = high-priority new rule.

---

## 4. Test Vector JSON Schema (updated 2026-06-05 -- S1/S2/S3/S4 + 2 additions applied)

```json
{
  "vector_id": "tv-lu-ch11",
  "book_id": "longevity_unnatural",
  "source_chapter": "Ch11_John_F_Kennedy",
  "pdf_path": "Chapter_Splits/Ch11_John_F_Kennedy.pdf",

  "subject": {
    "name": "John F. Kennedy",
    "description": "35th US President",
    "nationality": "American"
  },

  "birth_data": {
    "date": "1917-05-29",
    "time_local": "15:09",
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

  "life_events": [],

  "death_data": {
    "cause_of_death": "Assassination -- shot by Lee Harvey Oswald",
    "death_type": "violent",
    "death_date": "1963-11-22",
    "age_at_death": 46,
    "dasha_at_death": {
      "mahadasha": "JUPITER",
      "antardasha": "SATURN",
      "pratyantardasha": "SATURN",
      "sookshma": "JUPITER",
      "stated_by_author": true,
      "raw_text": "Jupiter Saturn-Saturn-Jupiter"
    }
  },

  "known_facts": {
    "profession": "Politician",
    "profession_category": "Politics",
    "key_events": [
      { "event": "Became 35th US President", "year": 1961 },
      { "event": "Assassination", "year": 1963 }
    ]
  },

  "author_observations": [
    {
      "obs_id": "obs-001",
      "verbatim": "exact quote or close paraphrase from prose text",
      "condition_type_guess": "planet_in_house",
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
    "layer_b_pass": null
  },

  "test_status": {
    "extraction_complete": false,
    "chart_computed": false,
    "rules_evaluated": false
  }
}
```

**Reagan pattern (S1) -- two events example:**
```json
"life_events": [
  {
    "event_id": "ev-001",
    "event_type": "assassination_attempt",
    "description": "Shot by John Hinckley Jr. outside Hilton Washington hotel",
    "date": "1981-03-30",
    "age_at_event": 70,
    "survived": true,
    "dasha_at_event": {
      "mahadasha": "SATURN",
      "antardasha": "MERCURY",
      "pratyantardasha": "JUPITER",
      "sookshma": "JUPITER",
      "stated_by_author": true,
      "raw_text": "Saturn-Mercury-Jupiter-Jupiter"
    }
  }
],
"death_data": {
  "cause_of_death": "Pneumonia following Alzheimer's disease",
  "death_type": "natural",
  "death_date": "2004-06-05",
  "age_at_death": 93,
  "dasha_at_death": {
    "mahadasha": null,
    "antardasha": null,
    "pratyantardasha": null,
    "sookshma": null,
    "stated_by_author": false,
    "raw_text": null
  }
}
```

---

## 5. Death Type Classification

Use these exact values for `death_type`:

| Value | Use when |
|---|---|
| `violent` | Assassination, shooting, stabbing, bombing |
| `accident` | Car crash, plane crash, drowning, fall |
| `disease` | Cancer, heart disease, illness |
| `suicide` | Confirmed or strongly indicated |
| `natural` | Old age, natural causes |
| `unknown` | Not clear from the text |

---

## 6. Output Delivery

At the end of decode, deliver:
1. All JSON files in `KE_TEXTBOOK_DECODE/Test_Vectors/JSON/longevity_unnatural/`
2. `LU_CaseDerived_Rules.json` in the same folder
3. `LU_Gap_Report.md` -- list of author observations with no KE rule match, prioritised by case-count confirmation

**Do NOT ingest anything to MongoDB.** JSON output only. CC + TT will review before any ingest.

---

## 7. Quality Standards

- Every JSON must validate against the schema (no missing required fields)
- `observation_verbatim` must be a quote or close paraphrase -- not a summary
- If data is missing from the PDF: use `null` not `""` for string fields
- Flag uncertain extractions with a `"extraction_note": "..."` field
- `gap_flag: true` means you could NOT find a matching rule in the existing KE for this observation

---

*Thread 1 -- Longevity + Unnatural Deaths Decode*
*For questions or schema clarifications: raise with TT before proceeding*
*Parallel: Thread 2 (765 Notable Horoscopes) running simultaneously*
