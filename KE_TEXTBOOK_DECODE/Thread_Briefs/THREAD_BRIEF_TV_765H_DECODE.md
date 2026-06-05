# Thread Brief -- 765 Notable Horoscopes: Profession Library Decode
## KE Milestone 2 · Thread 2 · Profession Library + Test Vectors (Layer A)

> Prepared by: CC (Claude Code) + Temple Team
> Date: 2026-06-05 | Updated: 2026-06-05 (Step 2 Complete)
> Status: **✅ STEP 2 DELIVERED -- 765 JSON VECTORS + PROFESSION LIBRARY. AWAITING TT REVIEW.**
> Batch ID: `tv_765h_decode_v1`
> Parallel thread: Thread 1 (Longevity + Unnatural Deaths) ✅ Step 2 also complete

---

## Step 2 Delivery Summary (2026-06-05)

| Metric | Value |
|---|---|
| Total entries | 765 (9 mythological, 756 real) |
| Date recovered | 739/756 (97.8%) |
| Time recovered | 716/756 (94.7%) |
| Place recovered | 741/756 (98.0%) |
| Dasha balance | 708/756 (93.7%) · 8 planet unclear |
| Planet degrees | 753/756 have ≥ 1 planet |
| Explicit profession | 113 (14.9%) |
| Inferred profession | 643 (85.1%) -- `profession_inferred: true`, flagged for TT review |
| OCR corrected | 1 (Akbar year 1942→1542) |
| Errors | 0 |

**Output files:** `KE_TEXTBOOK_DECODE/Test_Vectors/JSON/765_horoscopes/`
- `tv_765h_0001_*.json` ... `tv_765h_0765_*.json` (765 individual vectors)
- `Profession_Library_Raw.json`
- `Profession_Library_Aggregated.json`
- `765H_Decode_Notes.md`

**Decode script:** `/Users/apple/Documents/Knowledge Engine_eBooks/5 New test Books/765 Notable Horoscopes/decode_765_horoscopes.py`

**Do NOT ingest.** JSON output only. TT + CC review first per session constraint.

**Next step (Phase 4):** Run `vedic_calculator.py + pyswisseph` against all 756 real birth charts to compute lagna signs, house assignments, and verify `dasha_balance_from_book` against `calculate_vimshottari_dasha()` output.

---

## One-Liner

Decode all 765 horoscope entries from "765 Notable Horoscopes" -- extracting birth data, profession, and chart positions to build the KE Profession Library: the first empirical dataset mapping Planet × House × Sign × Lagna to real-world professions at scale.

---

## Source Book Details

| Field | Value |
|---|---|
| Book title | 765 Notable Horoscopes |
| Source PDF | `/Users/apple/Documents/Knowledge Engine_eBooks/5 New test Books/765 Notable Horoscopes/765 Notable Horoscopes.pdf` |
| Split files | `/Users/apple/Documents/Knowledge Engine_eBooks/5 New test Books/765 Notable Horoscopes/765_Individual_Horoscopes/` |
| File naming | `{serial:04d}_{chart_id}_{name}.pdf` (e.g., `0011_A-2_Aamir_Khan.pdf`) |
| Total files | 765 (0001-0765) |
| Manifest | `_index.csv` in the same folder |
| Output folder | `KE_TEXTBOOK_DECODE/Test_Vectors/JSON/765_horoscopes/` |

**Structure:**
- 0001-0009: Divine Horoscopes (Lord Ram, Lord Krishna, Mahavir Jain, Gautam Buddha, Lord Jesus Christ, Adi Shankaracharya, Prophet Mohammed, Guru Nanak Dev, Sai Baba of Shirdi)
- 0010-0765: Alphabetical A through Z

---

## What This Thread Produces

### Primary Output: Profession Library

This is the unique value of the 765 Horoscopes book. Each chart gives us a REAL person with a KNOWN profession + birth chart. 765 data points aggregated = statistical patterns of which planetary placements correlate with which professions.

**Profession Library Raw JSON (`Profession_Library_Raw.json`):**
One entry per person with profession + all chart positions.

**Profession Library Aggregated (`Profession_Library_Aggregated.json`):**
Frequency tables: for each profession category, what are the most common lagna signs, planet placements, house occupations?

### Secondary Output: 765 Test Vector JSONs (Layer A only)
Each JSON also serves as a Layer A calibration vector -- once CC computes the charts, we verify our engine matches the book's charts.

**Single decode pass -- all layers covered.**

This book has no author analysis text per chart, so the standard Layer B "author said X → rule fires?" approach cannot be applied from the source material. However, **the profession label IS the Layer B expected output** and must be captured in this single decode pass.

The thread populates `layer_b_expected` in every JSON now. When CC later runs KE profession-inference rules (built from G3 data) against 300H cases to validate them, the 765H JSONs are already ready as a supplementary held-out test set -- with no second decode required.

**This thread's single pass covers:**
- Layer A input: birth data (for `vedic_calculator.py` chart computation by CC)
- Layer B expected output: `layer_b_expected.profession` = ground truth for KE profession rule testing
- G3: profession + chart positions → Profession Library aggregation

---

## Schema Adjustments Confirmed (2026-06-05)

Based on Pre-Decode Q&A (`765_horoscopes/PRE_DECODE_QA_765H.md`), six flags reviewed and decisions made:

| Flag | Decision | Change |
|---|---|---|
| S1 | ✅ ADDED | `dasha_balance_from_book: {planet, years, months, days, raw_text}` -- present in **100% of entries**; primary Layer A calibration field |
| S2 | ✅ ADDED | `planet_degrees_from_text: {PLANET: {degree_in_sign, retrograde}}` -- degrees readable from chart text; signs computed by CC via `vedic_calculator.py` |
| S3 | ✅ CONFIRMED | CropBox: chart-ID-anchored extraction using `{ID}:` marker (e.g., `A-2:`) in extracted text to isolate target entry from the full-page text layer |
| S4 *(Q-CC-1)* | ✅ APPROVED | ~35% unlabelled profession entries → infer from life-events keywords; mark `profession_inferred: true`. Do NOT set null/Other. |
| S5 *(Q-CC-2)* | ✅ APPROVED | OCR year errors (e.g., Akbar 1542 → OCR reads 1942): auto-correct, flag `ocr_corrected: true`. Apply to any clearly wrong historical date. |
| S6 | ✅ APPROVED | Divine entries 0001-0009 → `mythological: true`, `time_confidence: "mythological"`. Exclude from Profession Library aggregation stats. |

**On `dasha_balance_from_book`:** Every entry states `"Balance of dasha {planet} {y-m-d}"`. After CC computes the chart, `calculate_vimshottari_dasha()` output is compared against this value -- this is the precision dasha-engine calibration test for 765H.

See full combined review: `KE_TEXTBOOK_DECODE/Test_Vectors/COMBINED_PREDECODE_REVIEW.md`

---

## STEP 1 -- ✅ COMPLETE

Pre-Decode Q&A received and reviewed. **Proceed directly to Step 2 (full decode of all 765 entries).**

Pre-Decode Q&A file: `KE_TEXTBOOK_DECODE/Test_Vectors/JSON/765_horoscopes/PRE_DECODE_QA_765H.md`

Key confirmed findings from Step 1:
- Layout: `{ID}: {Name}-{Profession}: Born on {date} at {time} at {place}: Balance of dasha {planet} {y-m-d}:`
- ~60-65% profession explicitly labelled; ~30% inferable from life-events; ~5-10% manual
- Planet degrees extractable from chart text (`Su4:47`, `Ma14:55` format); signs must be computed
- Ayanamsha: **Lahiri confirmed** (Aamir Khan As21:3 cross-check passed)
- pdfplumber ignores CropBox -- both horoscopes in text per file; chart-ID-anchored extraction required
- `time_confidence: "rectified"` for pre-1900 births (e.g., Akbar 1542)

---

## STEP 1 ORIGINAL -- Pre-Decode Questions (ARCHIVED -- for reference only)

**Before decoding all 765, read 10 sample PDFs from different sections and answer ALL questions below. Return answers to TT. CC + TT will review before you proceed to full decode.**

```
THREAD: Read these as samples (spread across alphabet and sections):
  0001_Div-1_Lord_Ram.pdf          (Divine section)
  0009_Div-9_Sirdhi_Ke_Sai_Baba.pdf
  0011_A-2_Aamir_Khan.pdf          (Alphabetical - Actor)
  0013_A-4_Agrawal_PK.pdf
  0015_A-6_Akbar_the_great.pdf
  A mid-alphabet entry (around 0300-0400)
  A Z-section entry (near 0765)
  One entry where profession looks complex or dual
  One entry where birth time looks approximate
  One entry where the PDF crop seems incomplete

Q1.  Describe the exact layout of the half-page crop.
     What text appears above the chart grid? What text appears below?
     Is the profession always in a specific position (e.g., subtitle under the name)?

Q2.  Where exactly is the profession stated?
     a) In the filename only? (e.g., "Akbar_the_great")
     b) As a subtitle/heading on the page?
     c) In typed text near the chart?
     d) Inside the chart grid itself?
     Give 3 verbatim examples.

Q3.  Is the birth data (date/time/place) always in a typed text block?
     Or is it handwritten/embedded in the chart diagram?
     Paste the exact birth data text from 3 different entries.

Q4.  Is birth time stated as exact (HH:MM) or approximate (e.g., "morning", "sunrise")?
     Of your 10 samples, how many have exact time vs. approximate vs. no time?

Q5.  What ayanamsha does the book appear to use?
     Pick any well-known entry (Aamir Khan, Akbar, etc.) and check:
     stated lagna in the chart vs. Lahiri-computed lagna for that birth data.
     Do they match?

Q6.  Are planet positions (which planet in which house) visible in the visual chart
     grid? Is the grid readable -- can you make out the Sanskrit/abbreviated
     planet names in each box?

Q7.  Does the book always state the lagna sign explicitly in text?
     Or is lagna only inferable from the chart grid?

Q8.  For the Divine Horoscopes (Lord Ram, Krishna, etc.) --
     are birth dates approximate/mythological? How should these be handled?

Q9.  Are there any entries where the name or profession in the filename appears
     wrong or truncated (OCR artifact from the split script)?
     List any you notice.

Q10. Estimate: what percentage of the 765 entries have ALL of these:
     exact birth time + birth place + profession clearly stated?
     (rough % is fine -- e.g., "~80%", "maybe 50%")

Q11. Is there any author text BEYOND the chart and birth data?
     Or is every entry purely: name + chart + birth data?

Q12. How is a compound profession handled?
     e.g., if a person is both a "Politician and Businessman"
     -- does the book give one label or two?
```

**Return answers as a structured reply before starting full decode.**

---

## STEP 2 -- Full Decode (✅ CLEARED TO START)

Decode ALL 765 entries. Schema has been updated per Pre-Decode review -- see Section 4.

### Per-Entry Decode Checklist

For each entry, produce a JSON matching the schema in Section 4:

- [ ] Identify target entry using chart-ID-anchored extraction (`{ID}:` marker in extracted text)
- [ ] `name` -- full name as stated in book opening line (not filename)
- [ ] `profession_raw` -- exact hyphenated suffix from name-tag line (e.g., `"Paedriatic"`, `"IAS & astro"`)
- [ ] `profession_category` -- map to 11-category taxonomy (Section 5)
- [ ] `profession_subcategory` -- specific role
- [ ] `profession_inferred` -- `true` if inferred from life-events text; `false` if explicitly labelled
- [ ] `profession_compound` -- `true` if compound (e.g., `"IAS & astro"`); add `profession_secondary`
- [ ] `birth_data` -- date, time, place (or lat/long if no place name), timezone
- [ ] `time_confidence` -- `from_chart` / `approximate` / `unknown` / `mythological` / `rectified`
- [ ] `dasha_balance_from_book` -- extract `{planet, years, months, days}` from `"Balance of dasha..."` line
- [ ] `planet_degrees_from_text` -- extract all `Su4:47` / `Mo9:33` style values from chart text; flag retrograde (`JuR`, `SaR`)
- [ ] `layer_b_expected` -- profession category + subcategory as ground truth
- [ ] `ocr_corrected: true` -- if you corrected a clearly wrong historical date
- [ ] `source_file` -- PDF filename

### Handling Missing / Edge Cases
- **Profession not labelled (~35%):** Infer from life-events keywords (e.g., "film debut" → Actor, "became CM" → Politics). Set `profession_inferred: true`. Do NOT set null.
- **Birth time not stated:** `time_confidence: "unknown"`, `time_local: null` -- still extract everything else
- **Pre-1900 births:** `time_confidence: "rectified"` -- even if a specific time is stated (these are author rectifications)
- **OCR year errors (e.g., Akbar 1942 → 1542):** Auto-correct, set `ocr_corrected: true`
- **Divine Horoscopes (0001-0009):** `mythological: true`, `time_confidence: "mythological"`, excluded from Profession Library aggregation
- **Compound professions:** `profession_compound: true`, fill both `profession_category` (primary) and `profession_secondary` (secondary)
- **Coordinates instead of city name:** Use lat/long as-is; leave `place` as null or fill with reverse-geocoded name

### Scale efficiency note
Layout is uniform across all 765 entries -- batch processing is feasible. The `{ID}: {Name}-{Profession}: Born on...` format is consistent. Scripted extraction anchored to chart ID is the recommended approach.

---

## 3. Profession Library Aggregation

After all 765 entries are decoded, produce TWO additional output files:

### `Profession_Library_Raw.json`
Array of all 765 decoded entries (same as the individual JSONs, consolidated).

### `Profession_Library_Aggregated.json`
For each profession category (and subcategory), compute frequency counts:
```json
{
  "profession_category": "Entertainment",
  "total_cases": 47,
  "lagna_distribution": {
    "Libra": 11,
    "Leo": 9,
    "Gemini": 7,
    ...
  },
  "sun_house_distribution": { "1": 8, "3": 12, ... },
  "moon_house_distribution": { "1": 5, "7": 10, ... },
  "mars_house_distribution": { "1": 13, "4": 7, ... },
  "venus_house_distribution": { "1": 14, "5": 9, ... },
  "jupiter_house_distribution": { "9": 15, "1": 8, ... },
  "saturn_house_distribution": { "6": 10, "10": 8, ... },
  "rahu_house_distribution": { "10": 18, "1": 9, ... },
  "top_3_planet_house_combinations": [
    { "planet": "VENUS", "house": 1, "count": 14, "pct": 29.8 },
    { "planet": "RAHU", "house": 10, "count": 18, "pct": 38.3 },
    ...
  ]
}
```

---

## 4. Test Vector JSON Schema (updated 2026-06-05 -- S1/S2/S3/S4/S5/S6 applied)

```json
{
  "vector_id": "tv-765h-0011",
  "book_id": "765_notable_horoscopes",
  "source_serial": "0011",
  "source_file": "0011_A-2_Aamir_Khan.pdf",

  "subject": {
    "name": "Aamir Khan",
    "name_from_filename": "Aamir_Khan",
    "mythological": false
  },

  "profession": {
    "profession_raw": "Actor",
    "profession_category": "Entertainment",
    "profession_subcategory": "Actor",
    "profession_compound": false,
    "profession_secondary": null,
    "profession_inferred": false,
    "profession_ambiguous": false
  },

  "birth_data": {
    "date": "1965-03-14",
    "time_local": "09:21",
    "timezone_offset_hours": 5.5,
    "time_utc": "1965-03-14T03:51:00Z",
    "latitude": 19.076,
    "longitude": 72.877,
    "place": "Mumbai, Maharashtra, India",
    "time_confidence": "from_chart",
    "ayanamsha": "lahiri",
    "mythological": false,
    "ocr_corrected": false,
    "notes": ""
  },

  "dasha_balance_from_book": {
    "planet": "SUN",
    "years": 0,
    "months": 2,
    "days": 13,
    "raw_text": "Balance of dasha Sun 0-2-13"
  },

  "planet_degrees_from_text": {
    "LAGNA":   { "degree_in_sign": 21.05, "retrograde": false },
    "SUN":     { "degree_in_sign": 4.78,  "retrograde": false },
    "MOON":    { "degree_in_sign": 9.55,  "retrograde": false },
    "MARS":    { "degree_in_sign": 14.92, "retrograde": false },
    "MERCURY": { "degree_in_sign": 12.47, "retrograde": false },
    "JUPITER": { "degree_in_sign": 28.92, "retrograde": false },
    "VENUS":   { "degree_in_sign": 8.03,  "retrograde": false },
    "SATURN":  { "degree_in_sign": 28.78, "retrograde": false },
    "RAHU":    { "degree_in_sign": 23.92, "retrograde": false },
    "KETU":    { "degree_in_sign": 23.92, "retrograde": false }
  },

  "chart_verification": {
    "lagna_degree_from_book": 21.05,
    "lagna_sign_computed": null,
    "lagna_computed_matches_degree": null,
    "dasha_balance_engine_match": null,
    "engine_notes": ""
  },

  "layer_b_expected": {
    "type": "profession_match",
    "profession_raw": "Actor",
    "profession_category": "Entertainment",
    "profession_subcategory": "Actor",
    "profession_inferred": false,
    "note": "Profession label is the Layer B ground truth. KE profession-inference rules (built from G3 data) will be evaluated against this."
  },

  "test_status": {
    "extraction_complete": false,
    "chart_computed": false,
    "dasha_balance_verified": false,
    "layer_a_evaluated": false,
    "layer_b_evaluated": false
  }
}
```

**Mythological entry example (0001-0009):**
```json
{
  "vector_id": "tv-765h-0001",
  "subject": { "name": "Lord Ram", "mythological": true },
  "birth_data": {
    "date": null,
    "time_local": null,
    "time_confidence": "mythological",
    "mythological": true,
    "notes": "Mythological -- Treta Yuga, Chaitra Shukla Navami, Noon, as stated in book"
  },
  "dasha_balance_from_book": null,
  "planet_degrees_from_text": {},
  "profession": {
    "profession_raw": null,
    "profession_category": "Spiritual_Religious",
    "profession_inferred": true
  }
}
```

**Note:** Planet **signs** are NOT in the book text -- only degrees (`Su4:47` format). Signs are computed by CC via `vedic_calculator.py` in Phase 4. The `planet_degrees_from_text` stays as the book-stated calibration field; CC populates full sign+house positions separately.

---

## 5. Profession Taxonomy

Map every profession to one of these categories:

| Category | Sub-types |
|---|---|
| `Politics` | Head of State · Prime Minister · President · Minister · MP · Politician · Freedom Fighter |
| `Military` | General · Admiral · Marshal · Military Leader · Revolutionary |
| `Judiciary_Law` | Judge · Lawyer · IPS Officer · IAS Officer · Legal professional |
| `Business` | Industrialist · Entrepreneur · Banker · Businessman · Trader |
| `Entertainment` | Actor · Singer · Dancer · Film Director · Musician · Comedian |
| `Sports` | Cricketer · Footballer · Athlete · Boxer · Chess player |
| `Spiritual_Religious` | Saint · Swami · Yogi · Guru · Spiritual Leader · Prophet · Religious Leader |
| `Science_Academia` | Scientist · Professor · Doctor · Physician · Engineer · Academic |
| `Arts_Literature` | Writer · Poet · Journalist · Painter · Sculptor · Photographer |
| `Royalty_Nobility` | King · Queen · Emperor · Nawab · Maharaja · Prince · Czar · Duke |
| `Criminal_Notorious` | Criminal · Terrorist · Gangster (retain for control chart analysis) |
| `Housewife` | Housewife (explicitly listed as such in the book) |
| `Other` | Does not fit above categories -- describe in `profession_raw` |

**Compound professions:** If a person is listed as "Politician and Businessman", use the PRIMARY profession as `profession_category` and list both in `profession_raw`. Add `profession_compound: true`.

---

## 6. Handling Divine / Mythological Charts

For the 9 Divine Horoscopes (0001-0009):
- Set `mythological: true`
- Set `time_confidence: "mythological"`
- Still extract the birth data as stated in the book
- Still extract lagna/planet positions
- These will be excluded from statistical aggregation in the Profession Library
- They ARE included in the Test Vector JSONs as a separate category

---

## 7. Output Delivery

At the end of decode, deliver to `KE_TEXTBOOK_DECODE/Test_Vectors/JSON/765_horoscopes/`:

1. 765 individual JSON files (`tv_765h_{serial}_{name}.json`)
2. `Profession_Library_Raw.json` (consolidated array of all 765)
3. `Profession_Library_Aggregated.json` (frequency tables by profession category)
4. `765H_Decode_Notes.md` -- any patterns, issues, or exceptions you found

**Do NOT ingest anything to MongoDB.** JSON output only. CC + TT review first.

---

## 8. Quality Standards

- `profession_category` must always be one of the 11 taxonomy values (not free text)
- `birth_data.place` should be the full city + state/country -- not abbreviations
- If coordinates are not in the book, look them up for the stated place (standard city coords)
- Use `null` for missing fields -- not `""` or `"unknown"` (except `profession_raw` which is a direct quote)
- Each JSON must be valid JSON (no trailing commas, no smart quotes)

---

*Thread 2 -- 765 Notable Horoscopes Profession Library Decode*
*For questions or schema clarifications: raise with TT before proceeding*
*Parallel: Thread 1 (Longevity + Unnatural Deaths) running simultaneously*
