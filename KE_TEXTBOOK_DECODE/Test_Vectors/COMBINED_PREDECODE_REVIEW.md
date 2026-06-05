# KE Milestone 2 -- Combined Pre-Decode Review
## All Four Threads · TT Sign-Off Document

> **Prepared by:** CC (Claude Code) + Temple Team
> **Date:** 2026-06-05
> **Status:** ✅ ALL FOUR THREADS GREEN-LIT (with brief updates noted below)
> **Covers:** T1 Longevity · T2 765H · T3 300H Part 1 · T4 300H Part 2

---

## 1. Thread Status Summary

| Thread | Book | Chapters | Pre-Decode Q&A | CC Review | Status |
|---|---|---|---|---|---|
| **T1** | Longevity + Unnatural Deaths | 93 | `PRE_DECODE_QA_TV_LONGEVITY.md` | ✅ Reviewed 2026-06-05 | 🟢 **GREEN-LIT** -- already running |
| **T2** | 765 Notable Horoscopes | 765 | `765_horoscopes/PRE_DECODE_QA_765H.md` | ✅ Reviewed 2026-06-05 | 🟢 **GREEN-LIT** |
| **T3** | 300 Important Horoscopes Vol 1 Part 1 | 136 | `300h1/300H1_PreDecode_QA.md` | ✅ Reviewed 2026-06-05 | 🟢 **GREEN-LIT** |
| **T4** | 300 Important Horoscopes Vol 1 Part 2 | 153 | `300h2/300H2_PreDecode_QA.md` | ✅ Reviewed 2026-06-05 | 🟢 **GREEN-LIT** |

**Total case studies across all four threads:** ~1,147

---

## 2. Cross-Thread Decisions (Apply to All Four)

### D1 -- Ayanamsha
**Decision: Lahiri ayanamsha confirmed across all four books.**

| Book | Confirmation method |
|---|---|
| T1 Longevity | KP Body table sidebar value (`22-42-12.76`); KP framework uses Lahiri |
| T2 765H | Aamir Khan cross-check: `As21:3` matches Lahiri-computed lagna for Mar 1965, Mumbai |
| T3 300H Part 1 | Two labeled-table explicit values: Ch005 (`23-28-18.29`), Ch007 (`23-47-10.50`) |
| T4 300H Part 2 | Amitabh Bachchan: stated `22-57-40.37` = textbook Lahiri for 1942 |

All four threads compute charts using **Lahiri ayanamsha only.**

---

### D2 -- Framework
**Decision: KP framework confirmed across T1, T3, T4. T2 is a data book (no framework analysis).**

| Thread | Framework | Implication |
|---|---|---|
| T1 Longevity | KP | All `author_observations[]` tagged `science_id: "kp_jyotish"` |
| T2 765H | None (data book -- no author analysis) | No `author_observations[]` needed |
| T3 300H Part 1 | Pure KP | All observations tagged `science_id: "kp_jyotish"` |
| T4 300H Part 2 | Pure KP | All observations tagged `science_id: "kp_jyotish"` |

**KP-specific `condition_type_guess` values approved for T3 and T4:**

| Value | Use when |
|---|---|
| `kp_star_lord` | Planet-in-star-of-another-planet chain |
| `kp_sub_lord` | Sub-lord signification |
| `kp_planet_signification` | Planet significates a set of houses |
| `kp_signification_chain` | Multi-planet chain (Rahu offers result of X through Y) |
| `planet_in_house` | Still valid for straightforward house placement |
| `dasha_planet` | Dasha lord triggering an event |

BPHS condition types (`yoga_combination`, `house_lord_placement`) are illustrative examples in the brief schemas only -- replace with KP-appropriate values from the list above.

---

### D3 -- Planet Positions: Primary Extraction Source

| Thread | Primary source | Notes |
|---|---|---|
| T1 Longevity | **KP Body table** (Lagna → Ketu + house significations) | Chart header `Aa:` line = cross-check only (frequently garbled) |
| T2 765H | **Chart text layer** (`Su4:47` format -- degrees only) | Signs must be computed via `vedic_calculator.py` |
| T3 300H Part 1 | **Body-longitude table** (Lagna → Ketu + sign + degree + significations) | Reliably OCR'd on every page |
| T4 300H Part 2 | **Body-longitude table** (same format as T3) | Narrative text = clean OCR; chart grid area = image only |

---

### D4 -- Lagna Stated in Text Body?
**Decision: Lagna is NEVER stated in narrative text across all four books. Always read from table.**

All four books require lagna to be extracted from structured table data, not prose. The sign is absent in T2 (must compute). Present in T1, T3, T4 via their respective tables.

---

### D5 -- OCR Correction Policy
**Decision: Auto-correct confirmed wrong historical dates. Flag `ocr_corrected: true`.**

Applies across all threads. Examples confirmed:
- T2 765H: Akbar the Great -- OCR reads 1942, correct to **1542**
- T3 300H Part 1: Princess Diana -- OCR reads 1901, correct to **1961**

General rule: If the OCR year produces a chronologically impossible or historically definitive error (birth year that predates or contradicts the person's known life), auto-correct and flag. Do NOT guess on ambiguous cases -- flag `ocr_error_suspected: true` and set `time_confidence: "unknown"`.

---

### D6 -- Pre-1900 Birth Times
**Decision: `time_confidence: "rectified"` for ALL pre-1900 births, unless author explicitly sources the time.**

Applies to T3 and T4 (which contain historical figures). T1 Longevity (famous modern subjects) is not affected. T2 765H has only one truly ancient case (Akbar 1542) -- apply `"rectified"` there too.

The author states specific HH:MM:SS times for kings and historical figures without disclaimers. These are rectified or taken from secondary astrological sources. Do not use `"from_chart"` for pre-1900 births.

---

### D7 -- Birth Times Not OCR-Recoverable
**Decision: Set `time_confidence: "unknown"` and `time_local: null`. Do NOT back-infer time from Lagna degree.**

Back-inference from Lagna degree is circular reasoning (using book-computed lagna to reverse-engineer a time, then recomputing that lagna). These vectors are still valid for Layer C gap detection and for `author_observations[]`. They cannot contribute to Layer A calibration -- this is acceptable; we have strong coverage from the majority of cases that do have times.

---

## 3. Thread-Specific Decisions

### Thread 2 -- 765 Notable Horoscopes

**Q-CC-1 -- Unlabelled profession (~35% entries):**
**→ Option (a) approved.** Infer from life-events keywords, mark `profession_inferred: true`.
Rationale: 35% null would cripple the Profession Library. Life-events text is almost always unambiguous. The `profession_inferred` flag enables TT spot-check without blocking extraction.

**Q-CC-2 -- Akbar birth year OCR error:**
**→ Option (a) approved.** Auto-correct to 1542, flag `ocr_corrected: true`. (Covered under D5 above.)

**Schema additions (S1-S6):**

| Flag | Decision | Field Added |
|---|---|---|
| S1 | ✅ ADDED | `dasha_balance_from_book: {planet, years, months, days, raw_text}` -- present in 100% of entries |
| S2 | ✅ ADDED | `planet_degrees_from_text: {PLANET: {degree_in_sign, retrograde}}` -- degrees readable, signs computed |
| S3 | ✅ CONFIRMED | CropBox: chart-ID-anchored extraction using `{ID}:` marker in text |
| S4 | ✅ APPROVED | `profession_inferred: true` for unlabelled entries |
| S5 | ✅ APPROVED | `ocr_corrected: true` for confirmed year errors |
| S6 | ✅ APPROVED | Divine 0001-0009: `mythological: true`, excluded from Profession Library stats |

**Note on `dasha_balance_from_book`:** This is the most valuable Layer A calibration field in 765H. Every entry states `"Balance of dasha {planet} {y-m-d}"`. After CC computes the chart, `calculate_vimshottari_dasha()` output should match this value exactly. This is a precision test for the dasha engine.

---

### Thread 3 -- 300 Important Horoscopes Vol 1 Part 1

**F1 -- Three birth data formats:**
✅ Decoder reads all three. Body-longitude table = primary for planet positions. Format A labeled table = primary for birth data. Format B/C: extract what OCRs; fallback to `time_confidence: "unknown"` for corrupted times.

**F2 -- ~33% birth time not OCR-recoverable:**
✅ `time_confidence: "unknown"` and `time_local: null` for these cases. No back-inference from Lagna.

**F3 -- Ch135 Diana OCR year 1901 → 1961:**
✅ Hard-correct to 1961 (`ocr_corrected: true`). For Diana's time discrepancy (book: 16:45 vs historical 19:45 BST): use book value, add `"time_discrepancy_note": "Historical records suggest 19:45 BST; book states 16:45"`.

**F4 -- Pure KP framework:**
✅ Confirmed. All observations tagged `science_id: "kp_jyotish"`. KP condition types approved (see D2 above).

**F5 -- Lahiri confirmed.** ✅ No action needed.

**F6 -- 3-6 author_observations per chapter:**
✅ Confirmed. Do not over-extract. Each distinct KP observation = one entry. Do not split a single sentence into sub-observations.

**F7 -- Obama engine check:**
✅ Proceed without waiting. Obama Libra lagna (04 Aug 1961, 17:54 UTC, Honolulu) is well-established in KP literature. Expected to pass. TT can run as a spot-check in parallel -- does not gate the 136-chapter decode.

**Schema additions (S1-S2):**

| Flag | Decision | Field Added |
|---|---|---|
| S1 | ✅ UPDATED | Rename `planet_positions_from_text` → `planet_positions_from_table`. Add `degree` + `significations[]`. Aligns with T1 schema. |
| S2 | ✅ ADDED | `ayanamsha_stated` in `birth_data` (from Format A labeled table when present; `null` for Format B/C). |

**New field -- `kp_significations[]` in dasha object:**
T3's parenthetical dasha format -- e.g., `"Saturn-Saturn (05, 03, 08)"` -- includes house signification numbers in parentheses. These are NOT sub-period identifiers. Capture as:
```json
"dasha_at_event": {
  "mahadasha": "SATURN",
  "antardasha": "SATURN",
  "pratyantardasha": null,
  "sookshma": null,
  "kp_significations": [5, 3, 8],
  "stated_by_author": true,
  "raw_text": "Saturn-Saturn (05, 03, 08)"
}
```

---

### Thread 4 -- 300 Important Horoscopes Vol 1 Part 2

**Item 1 -- John Lennon not in this book:**
✅ Confirmed. The brief was written with speculative sample subjects -- this was a drafting error. Thread 4's chapter mapping is authoritative:

| Brief reference (WRONG) | Correct file |
|---|---|
| Ch086_Sirhan_Sirhan | Ch024_23_Sirhan_Sirhan |
| Ch088_Amitabh_Bachchan | Ch029_28_Amitabh_Bachchan |
| Ch096_Virginia_Woolf | Ch038_37_Virginia_Woolf |
| Ch099_John_Lennon | **Does not exist in this book** |
| Ch090_Nicolae_Ceausescu | Ch031_30_Nicolae_Ceausescu |

The `THREAD_BRIEF_TV_300H2_DECODE.md` will be corrected in the next brief update. Thread 4 proceeds using actual chapter files -- the thread's own mapping is correct.

**Item 2 -- KP-specific `condition_type_guess` values:**
✅ Approved (same as T3, F4, D2 above).

**Item 3 -- `time_confidence: "rectified"` for pre-1900 births:**
✅ Confirmed (see D6 above).

**Item 4 -- `dasha_at_death` when not stated by author:**
**Decision: Leave as `null` with `stated_by_author: false` during extraction (Step 2). CC computes in Phase 4.**

T4's author almost never names the dasha at death -- this is a fundamental difference from T1 (Longevity) where VMD at death was reliably stated. The correct split:

- **Thread Step 2 (extraction):** Set `dasha_at_death.stated_by_author: false`, all dasha fields `null`. Do NOT invent or compute during extraction.
- **CC Phase 4 (computation):** CC runs `calculate_vimshottari_dasha(birth_date, moon_longitude)` + `get_current_dasha(dashas, death_date)` to populate dasha at death for all cases where `death_date` is known. Tagged `cc_computed: true`.

This is actually more useful than author-stated dasha for Layer A testing -- it directly tests our engine's dasha computation against the death event.

```json
"dasha_at_death": {
  "mahadasha": null,
  "antardasha": null,
  "pratyantardasha": null,
  "sookshma": null,
  "stated_by_author": false,
  "cc_computed": false,
  "raw_text": null
}
```

**Schema alignment -- T4 matches T3 entirely**, with two additions:

| Field | T3 | T4 |
|---|---|---|
| `planet_positions_from_table` with sign + degree + significations | ✅ | ✅ Same |
| `ayanamsha_stated` in birth_data | ✅ | ✅ Same |
| `kp_significations[]` in dasha object | ✅ | ✅ Same |
| `kp_special_points` (HL/GL) | Not confirmed | **ADD** -- HL and GL appear in every T4 chart header |
| Pre-1900 time_confidence | -- | `"rectified"` default |

**T4-only addition -- `kp_special_points`:**
Hora Lagna (HL) and Ghati Lagna (GL) appear in every T4 chart header (e.g., `HL: 22Ta55 GL: 7Sg33`). Capture in a `kp_special_points{}` block. Not required for Layer A/B evaluation, but free data:
```json
"kp_special_points": {
  "hora_lagna":  { "sign": "Taurus",      "degree": 22.92 },
  "ghati_lagna": { "sign": "Sagittarius", "degree": 7.55  }
}
```
If HL/GL also appear in T3 chart headers (not confirmed), apply the same field there.

---

## 4. Updated Schema: Common Fields Across T3 and T4

T3 and T4 are structurally identical books by the same author using the same framework. Their schemas are now fully aligned:

```json
{
  "vector_id": "tv-300h2-ch029",
  "book_id": "300_horoscopes_vol1_part2",

  "birth_data": {
    "date": "1942-10-11",
    "time_local": "15:04:29",
    "timezone_offset_hours": 5.5,
    "time_utc": "1942-10-11T09:34:29Z",
    "latitude": 26.4499,
    "longitude": 81.9333,
    "place": "Allahabad, India",
    "time_confidence": "from_chart",
    "ayanamsha": "lahiri",
    "ayanamsha_stated": "22-57-40.37",
    "ocr_corrected": false,
    "notes": ""
  },

  "planet_positions_from_table": {
    "LAGNA":   { "sign": "Aquarius", "degree": 3.52,  "house": 1,  "significations": [1] },
    "SUN":     { "sign": "Libra",    "degree": 24.45, "house": 9,  "significations": [9, 12] },
    "MOON":    { "sign": "Libra",    "degree": 19.33, "house": 9,  "significations": [9, 4]  }
  },

  "kp_special_points": {
    "hora_lagna":  { "sign": null, "degree": null },
    "ghati_lagna": { "sign": null, "degree": null }
  },

  "death_data": {
    "cause_of_death": null,
    "death_type": null,
    "death_date": null,
    "age_at_death": null,
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

  "author_observations": [
    {
      "obs_id": "obs-001",
      "verbatim": "exact quote or very close paraphrase",
      "condition_type_guess": "kp_planet_signification",
      "science_id": "kp_jyotish",
      "claim_axis": "career",
      "claim_polarity": "positive",
      "gap_flag": false,
      "potential_rule_id": null
    }
  ]
}
```

---

## 5. Master Schema Comparison Across All Four Threads

| Field | T1 Longevity | T2 765H | T3 300H-1 | T4 300H-2 |
|---|---|---|---|---|
| `planet_positions_from_table` (sign + degree + house + significations) | ✅ | ❌ degrees only → `planet_degrees_from_text` | ✅ | ✅ |
| `dasha_balance_from_book` | ❌ not applicable | ✅ (every entry) | ❌ not in book | ❌ not in book |
| `life_events[]` array | ✅ | ❌ | ✅ | ✅ |
| `death_data{}` block | ✅ mandatory | ❌ (only if in life-events text) | ✅ | ✅ mandatory |
| `dasha_at_death.stated_by_author` | ~80% true | n/a | ~50-70% true | ~5-10% true |
| `dasha_at_death.cc_computed` | Phase 4 | Phase 4 | Phase 4 | Phase 4 (primary source for T4) |
| `author_observations[]` | ✅ KP | ❌ (no analysis text) | ✅ KP | ✅ KP |
| `science_id` per observation | `kp_jyotish` | n/a | `kp_jyotish` | `kp_jyotish` |
| `ayanamsha_stated` | ✅ | ❌ (not in text) | ✅ (Format A only) | ✅ (every entry) |
| `kp_significations[]` in dasha object | ❌ | ❌ | ✅ | ✅ |
| `kp_special_points` (HL/GL) | ❌ | ❌ | TBD | ✅ |
| `mythological: true` flag | ❌ | ✅ (0001-0009) | ❌ | ❌ |
| `profession_inferred: true` flag | ❌ | ✅ (~35% entries) | ❌ | ❌ |
| `ocr_corrected: true` flag | If needed | ✅ (Akbar + others) | ✅ (Diana + others) | ✅ (if needed) |
| Pre-1900 → `time_confidence: "rectified"` | ❌ | ✅ (Akbar) | ✅ | ✅ |
| `cross_reference{}` | ❌ | ❌ | ✅ | ✅ |
| `public_figure` | ✅ | ✅ | ✅ | ✅ |

---

## 6. Brief Updates Required Before Step 2

The following thread briefs need minor updates based on this review. These are clarifications, not redesigns -- Step 2 (full decode) can begin immediately.

| Brief | Update needed |
|---|---|
| `THREAD_BRIEF_TV_765H_DECODE.md` | Add S1 (`dasha_balance_from_book`) + S2 (`planet_degrees_from_text`) to schema; add Q-CC-1/Q-CC-2 decisions |
| `THREAD_BRIEF_TV_300H1_DECODE.md` | Rename to `planet_positions_from_table`; add `ayanamsha_stated`; add `kp_significations[]` in dasha object; add F2/F4/F7 decisions |
| `THREAD_BRIEF_TV_300H2_DECODE.md` | Correct chapter numbers (Lennon not in book); add `kp_special_points`; add `cc_computed` flag to `dasha_at_death`; add Item 1-4 decisions |

---

## 7. Phase 4 Computation Plan (CC -- after all Step 2 decodes complete)

When all four threads deliver their JSON output, CC will run a single computation pass:

1. **Layer A:** For every vector with `time_confidence: "from_chart"` or `"rectified"` -- run `vedic_calculator.py` with birth data → compute lagna + full chart → populate `chart_verification.lagna_computed` + `engine_matches_book`.

2. **Layer A (T2 special):** For every 765H vector -- run `calculate_vimshottari_dasha()` → compare computed dasha balance against `dasha_balance_from_book`. This is the precision calibration test.

3. **Layer A (T4 special):** For every T4 death vector -- run `get_current_dasha(dashas, death_date)` → populate `dasha_at_death` with `cc_computed: true`.

4. **Layer B:** For all T1/T3/T4 vectors with `author_observations[]` -- scan KP rules in KE (`science_id: "kp_jyotish"`) → evaluate which rules fire → update `rule_evaluation{}`.

5. **Layer C:** Aggregate all `gap_flag: true` observations across all four books → rank by case-count confirmation → produce master gap report.

---

*Combined Pre-Decode Review -- KE Milestone 2*
*All four threads reviewed and green-lit: 2026-06-05*
*CC: Claude Code · TT: Temple Team*
