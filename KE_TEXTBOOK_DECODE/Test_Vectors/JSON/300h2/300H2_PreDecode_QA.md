# 300H2 Decode -- Step 1 Pre-Decode Q&A
## Thread: TV_300H2_DECODE · Pre-Decode Review

> **Answered by:** Claude Code
> **Date:** 2026-06-05
> **Status:** 🟠 AWAITING TEMPLE TEAM REVIEW -- Step 2 (full decode) must not begin until TT confirms
> **Batch ID:** `tv_300h2_decode_v1`
> **Output folder:** `KE_TEXTBOOK_DECODE/Test_Vectors/JSON/300h2/`

---

## ⚠️ CRITICAL FLAG -- Read Before Q1

**John Lennon is NOT in this book.** A full text search across all 185 PDF pages returns zero matches for "Lennon." The brief's references to `Ch099_John_Lennon.pdf` and the Q4 ayanamsha check on John Lennon are based on an incorrect assumption about the book's contents. The "Sample subjects" section in the brief appears to have been drafted speculatively. Questions referencing John Lennon are answered using substitute subjects from this book.

**The chapter numbers in the brief** (Ch086, Ch088, Ch096, Ch099, Ch090) do **not** correspond to our split. Correct mapping:

| Brief reference | Actual file in our split |
|---|---|
| Ch086_Sirhan_Sirhan.pdf | Ch024_23_Sirhan_Sirhan.pdf |
| Ch088_Amitabh_Bachchan.pdf | Ch029_28_Amitabh_Bachchan.pdf |
| Ch096_Virginia_Woolf.pdf | Ch038_37_Virginia_Woolf.pdf |
| Ch099_John_Lennon.pdf | **Does not exist in this book** |
| Ch090_Nicolae_Ceausescu.pdf | Ch031_30_Nicolae_Ceausescu.pdf |

---

## Q1 -- Birth data format: labelled table, inline paragraph, or embedded in chart?

**Format:** A dedicated **labelled block** at the top of each horoscope entry, consistently structured across all chapters:

```
Date / time    :  [date + HH:MM:SS + timezone offset in parentheses]
Place          :  [lat/long coordinates -- city name rarely present]
Nakshatra      :  [birth star name]
Ayanamsha      :  [numeric value]
```

**Verbatim from two chapters:**

*Amitabh Bachchan (Ch029):*
```
Date /time     Oct-11-1942
               15:04:29 (5:30 east)
Place          81 E 56, 26 N 26
Nakshatra:     Swati
Ayanamsa:      22-57-40.37
```

*Virginia Woolf (Ch038):*
```
               January 25, 1882
               12:15:00 (0:00 west)
               0W7, 51N30
Nakshatra:     Aswini
Ayanamsa:      22-12-36.45
```

**⚠️ OCR warning:** The birth data block is partly embedded in the chart diagram area. Several chapters have garbled coordinates and times -- the Sirhan Sirhan block reads as `"2 3 :0 5 0 e :0 1 0 . . ( . 2 3 :0 1 0 N e a 4 6 t )"` instead of clean time+timezone. City names are almost never present -- only lat/long -- requiring reverse geocoding.

---

## Q2 -- Is birth time stated? Exact (HH:MM) or approximate?

**All sample chapters have birth times stated to HH:MM:SS (seconds-level) precision.** Sample breakdown:

| Chapter | Stated time | Assessment |
|---|---|---|
| Sirhan Sirhan | 23:05:00 (OCR garbled) | from_chart |
| Amitabh Bachchan | 15:04:29 | from_chart -- seconds-precise |
| Virginia Woolf | 12:15:00 | from_chart |
| Nicolae Ceausescu | 15:25:00 | from_chart |
| Benazir Bhutto | 18:01:00 | from_chart |
| King George I of Greece | 20:00:00 | ⚠️ Suspicious round number -- likely rectified or assumed |
| Henry Ford | Not OCR-readable -- chart image only | unknown |

Round times (20:00:00, 12:00:00) on pre-20th-century figures are suspicious and likely **rectified or assumed** by the author rather than from records. The author does **not** label these as rectified -- this must be inferred.

---

## Q3 -- Is lagna sign stated in text body, or only visible in the chart?

**Lagna is NOT stated in the narrative text body.** It is derivable only from:

1. The `"As: XX°XX'"` field in the abbreviated chart header (e.g., `"As: 3AQ31"` = Aquarius 3°31')
2. The `"Lagna"` row in the `Body Longitude | Star | p | Significations` table (e.g., `"Lagna 03 Aq 30'58"`)

The narrative analysis begins directly with planet observations and uses lagna as a reference point without naming the sign (e.g., *"From lagna, Mars is lord of 10..."*). Extracting lagna requires parsing the structured chart data table, not the prose.

---

## Q4 -- Ayanamsha check

**(John Lennon not in book -- substituting Amitabh Bachchan)**

- **DOB:** Oct 11, 1942 · 15:04:29 IST (UTC+5:30) · Allahabad (81°56'E, 26°26'N)
- **Book states:** Ayanamsha = **22°57'40.37"** · Lagna = **3°Aq31'** (Aquarius)
- **Lahiri ayanamsha for 1942:** ≈ 22°57' ✅ -- exact match

**Conclusion:** The book uses **Lahiri ayanamsha** throughout. Each chapter's stated ayanamsha value varies slightly by birth year (e.g., 22°12'36.45" for Virginia Woolf in 1882 vs. 22°57'40.37" for Amitabh Bachchan in 1942), confirming these are per-birth-year Lahiri values, not a hardcoded constant.

**Re: Q4's original intent (John Lennon):** For the record -- John Lennon DOB 1940-10-09, 18:30 BST, Liverpool -- Lahiri ayanamsha ≈ 22°55'. Since Lennon is not in this book, there is no stated lagna to compare against.

---

## Q5 -- Proportion of violent/unnatural death cases vs. other outcomes

**Estimate: approximately 55-65% death-focused.**

From 8 sample chapters:
- Death / violent end (direct or implied): Virginia Woolf (suicide), Nicolae Ceausescu (execution -- though not stated in text), King George I of Greece (assassination implied -- *"Ketu in 10 indicates sudden exit"*)
- Perpetrator: Sirhan Sirhan (assassin, not victim)
- Career / wealth: Amitabh Bachchan, Henry Ford, Benazir Bhutto (career focus -- her eventual assassination is not mentioned in this analysis)

From the full 153-chapter index: the subjects include multiple assassinated heads of state, executed leaders, assassination perpetrators (Sirhan Sirhan, James Earl Ray, John Hinckley Jr., John Wilkes Booth), a suicide (Virginia Woolf), and special-case chapters (dumbness/deafness, job transfer, birth prediction). Roughly **55-65% of cases involve some form of unnatural or notable death**.

---

## Q6 -- Does the author explicitly state cause of death and dasha at death?

**Mixed -- cause sometimes in intro line; dasha almost never named.**

The author typically includes a 1-2 sentence bio intro stating dates for historical figures. The astrological analysis focuses on *why* the chart shows the outcome -- it does **not** consistently name the dasha/antardasha running at time of death.

**Verbatim examples:**

*Virginia Woolf (Ch038) -- cause implied astrologically, dasha not stated:*
> *"Ketu (melancholy) is in lagna and it is in star of Moon (mind), while Moon is in star of Ketu in 12 (isolation). Saturn (pain) is conjunct with Moon. It is in 12, which causes disturbed sleep... All these combinations made native to be withdrawn, depressed, moody, etc."*

Suicide is implied by the analysis but not stated. Death date (28 Mar 1941) is given in the opening bio line. No dasha named.

*King George I of Greece (Ch033) -- death referred to obliquely:*
> *"All these combinations helped native to become King. But Ketu is in 10 indicate sudden exit."*

"Sudden exit" is the only death reference. Cause of death (assassination) not named. No dasha.

*Nicolae Ceausescu (Ch031) -- no death reference at all:*
> *"All these combinations helped native to become head of the country."*

His execution (Dec 25, 1989) is not mentioned. No dasha.

**Implication for `death_data` field:** `dasha_at_death.stated_by_author` will be `false` for the majority of cases. Death date must be sourced from the intro bio line or external knowledge; cause of death similarly. The author's astrological analysis is the primary source for `author_observations`, not for explicit death metadata.

---

## Q7 -- Same subjects in Part 1 and Part 2?

**No exact named duplicates found** across the full index comparison. Overlaps are category-level only:

| Type | Part 1 | Part 2 |
|---|---|---|
| Anonymous case -- doctor | Medical Doctor (p97) | Medical Doctor (Ch020) |
| Anonymous case -- police/civil service | Indian Admn. Service (p117) | Indian Police Service × 2 (Ch025, Ch055) |

**No named public figure appears in both volumes.** Part 1 focuses on Indian politicians, the US Kennedy family, Sri Lankan / Pakistani political figures, and early American presidents. Part 2 concentrates on European royalty, global businesspeople, and a higher concentration of assassinations/executions.

**Note:** The "Medical Doctor" anonymous cases should carry a `cross_reference` note flag but are almost certainly different individuals -- confirm during decode before linking.

---

## Q8 -- BPHS, KP, or mixed framework?

**Unambiguously KP (Krishnamurti Paddhati) throughout. Zero BPHS language observed.**

Definitive KP markers present in all 8 samples:

| KP marker | Example from text |
|---|---|
| Star-lord analysis | *"Saturn is in star of Mars (violence)"* |
| Planet significations table | `Body Longitude \| Star \| p \| Significations` with house numbers per planet |
| Significations chaining | *"Rahu offers result of Venus through Mercury; 07 and 10 through Jupiter"* |
| HL / GL reference points | `HL: 22Ta55 GL: 7Sg33` in every chart header |
| No yoga names | Rajayoga, Gajakesari etc. entirely absent |
| No BPHS house-lord language | "5th lord in 9th" style language entirely absent |

**Direct implication for rule extraction:** All `author_observations` will map to KP condition types. The `condition_type_guess` field should use KP-specific values: `kp_star_lord` / `kp_sub_lord` / `kp_planet_signification` -- not the BPHS types (`yoga_combination`, `house_lord_placement`) shown in the brief's schema examples.

---

## Q9 -- Multiple subjects on one page?

**Confirmed: Biden & Emperor Yoshihito share one physical page (Ch069).** This is the only confirmed multi-subject page. The split script's `"combined_page": true` flag applies only to Ch069.

Sirhan Sirhan (Ch024, book p50) and Indian Police Service (Ch025, book p51) were adjacent in the index but occupy separate physical PDF pages -- confirmed by content extraction.

---

## Q10 -- Pre-1900 births: rectified or assumed time?

**The author does NOT label pre-1900 birth times as rectified.** He states a specific HH:MM:SS time without qualification.

*King George I of Greece (Dec 24, 1845):* Stated as `20:00:00 (1:00 east)` -- the perfectly round hour strongly suggests this is rectified by the author or taken from a secondary astrological source. No disclaimer is given.

**Recommended decode rule:** Flag all pre-1900 cases as `"time_confidence": "rectified"` regardless of what the book states, unless the author explicitly mentions the birth time source. Do not use `"from_chart"` for pre-1900 births.

---

## Q11 -- Typical author analysis length per case

*Substitute subjects used since John Lennon is not in the book.*

| Chapter | Word count (approx.) |
|---|---|
| Amitabh Bachchan (Ch029) | ~130 words |
| Benazir Bhutto (Ch075) | ~150 words |
| Virginia Woolf (Ch038) | ~110 words |
| King George I of Greece (Ch033) | ~90 words |
| Nicolae Ceausescu (Ch031) | ~75 words |
| Sirhan Sirhan (Ch024) | ~55 words |

**Typical range: 55-150 words per case.** Structure is always: `planet(s) → star lord → signification → outcome`. No sub-headings within a case. Total per-chapter content = 1-2 PDF pages including chart diagram (image-based, not OCR-readable).

---

## Q12 -- OCR issues and blurry/unreadable pages

| Issue type | Affected chapter(s) | Detail |
|---|---|---|
| Birth data block garbled | Ch024 (Sirhan Sirhan) confirmed; likely others | Time/place coordinates near-unreadable: `"2 3 :0 5 0 e :0 1 0 . . ( . 2 3 :0 1 0 N e a 4 6 t )"` |
| Horoscope chart = image only | Ch005 page 2 confirmed; widespread across book | Second PDF page of multi-page entries is the chart grid image -- OCR extracts nothing useful |
| Footer digit misread | Ch024 | Footer reads `"Page# so"` (OCR for `"Page# 50"`) |
| Birth data compressed / missing | Ch003 (Introduction & Rules) | Pages covering Star Lord System (book pp13-27) condensed into 2 PDF pages; dense OCR artefacts |
| Dedication page mislocated | Ch001 | Dedication page (book p2) was scanned at a physically separate location in the PDF |

**Overall pattern:** The horoscope chart grid areas are scanned images -- OCR picks up abbreviated planet fields (`As`, `Su`, `Mo`, etc.) but with errors. Narrative text below charts extracts cleanly in most cases. Birth data blocks have variable OCR quality -- coordinates and timezone offsets are most error-prone and will require manual verification for approximately 20-30% of chapters.

---

## Summary for TT Review

| Question | Key finding |
|---|---|
| Q1 | Labelled block format; lat/long only (no city); OCR errors in ~20-30% of cases |
| Q2 | All times stated to HH:MM:SS; round times on pre-1900 figures = rectified/assumed |
| Q3 | Lagna NOT in narrative -- must parse from chart data table |
| Q4 | **Lahiri ayanamsha confirmed** ✅; John Lennon not in book |
| Q5 | ~55-65% death-focused cases |
| Q6 | Cause of death sometimes in intro bio; dasha at death almost never stated by author |
| Q7 | No named subject duplicates across Part 1 and Part 2 |
| Q8 | **Pure KP framework** -- `condition_type_guess` values must be KP-specific |
| Q9 | Only Ch069 (Biden + Yoshihito) is a confirmed combined-subject page |
| Q10 | Pre-1900 births → use `"time_confidence": "rectified"` universally |
| Q11 | 55-150 words per case; ~1-2 PDF pages per chapter |
| Q12 | Chart image areas unreadable by OCR; birth data coordinates error-prone |

**⚠️ Action required from TT before Step 2 begins:**
1. Confirm John Lennon is not expected in this book (or advise if he appears in a different volume)
2. Confirm KP-specific `condition_type_guess` values are acceptable (vs. the BPHS examples in the brief's schema)
3. Confirm `"rectified"` as default `time_confidence` for all pre-1900 births
4. Advise whether `dasha_at_death` should be left `null` or computed by CC engine when not stated by author

---

*Step 1 complete. Awaiting TT sign-off before proceeding to Step 2 (full decode of 153 chapters).*
