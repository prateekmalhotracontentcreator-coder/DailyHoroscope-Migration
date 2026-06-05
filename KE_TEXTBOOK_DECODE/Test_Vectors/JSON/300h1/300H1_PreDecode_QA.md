# Pre-Decode Q&A -- 300 Important Horoscopes Vol 1 Part 1
## Thread 3 · Step 1 Output · Awaiting Temple Team Review

> **Prepared by:** CC (Claude Code)
> **Date:** 2026-06-05
> **Batch ID:** `tv_300h1_decode_v1`
> **Status:** 🟠 AWAITING TT REVIEW -- Do not proceed to Step 2 until TT signs off
> **Samples read:** Ch001, Ch002, Ch004, Ch005, Ch007, Ch009, Ch010, Ch118, Ch135 (9 chapters)

---

## Q1 -- Birth Data Format

**Three distinct formats exist across chapters -- not one uniform format:**

### Format A -- Labeled Table
Most complete. Typical for anonymous/non-famous subjects. Rows: `Date/Time | Time Zone | Place | Star | Ayanamsha`

> *Verbatim from Ch007 (Standard Nativity):*
> ```
> Date /Time    05 Nov 2001 @ 19:05 M
> Time Zone     05:30 (East of GMT)
> Place         Nellore, India 79E58'00", 14N26' 00"
> Star          Aardra (Ra)
> Ayanamsha     23-47-10.50
> ```

### Format B -- Chart-Embedded
Common for famous subjects. Birth data is inside the Jyotish chart box -- OCRs partially and inconsistently.

> *Verbatim from Ch001 (Lincoln) -- as OCR'd from chart area:*
> ```
> Abraham Lincoln / Febrv•ry 12, 180V / 7:32:00 (5:00 west) / 84 W27, 38 N 2
> ```
> (OCR artifacts: "Febrv•ry" = February, "180V" = 1809)

### Format C -- Intro Paragraph Only
Rare. Date/place in the opening biographical sentence; time is in the chart area and may not OCR.

> *From Ch004 (Obama):*
> `"Barack Hussein Obama II was born on 04 Aug 1961 at Honolulu, Hawai"`
> *(time embedded in chart area -- not reliably extractable as text)*

**Decoder note:** The **body-longitude planet table** (Lagna → Ketu with house significations) is the single most reliably OCR'd data source on every page and should be the primary extraction target. The labeled table (Format A) gives the cleanest birth data when present. Format B (chart-embedded) is the hardest to parse.

---

## Q2 -- Birth Time Availability

| Chapter | Subject | Time Visible | Format | Confidence |
|---|---|---|---|---|
| Ch001 | Abraham Lincoln | 7:32:00 | HH:MM:SS | `from_chart` |
| Ch004 | Barack Obama | Not visible in OCR | -- | `unknown` |
| Ch009 | Hema Malini | 1:30:40 | HH:MM:SS | `from_chart` |
| Ch010 | LB Shastri | Not visible in OCR | -- | `unknown` |
| Ch118 | Martin Luther King | 13:01:00 | HH:MM:SS | `from_chart` |
| Ch135 | Princess Diana | 16:45:00 | HH:MM:SS | `from_chart`* |
| Ch002 | Girl -- Love Affair | Not visible | -- | `unknown` |
| Ch005 | Three Planets Exalted | 0:25:28 | HH:MM:SS | `from_chart` |
| Ch007 | Standard Nativity | 19:05 | HH:MM | `approximate` |

**Of 9 samples: 5 have exact time to seconds · 1 approximate · 3 not extractable from OCR**

*Diana's time flagged as potentially incorrect -- see Q10.

**Important:** Even when birth time doesn't OCR, the Lagna degree from the body-longitude table (e.g., `Lagna 17 Li 20'`) implies a specific time range and can be used to cross-check or narrow the time via the engine.

---

## Q3 -- Lagna in Text Body vs. Table

**Lagna is NEVER stated in the narrative text body.** It appears only in:

1. **Body-longitude table** -- e.g., `Lagna 00 Aq 45' 18 Dhan 3` -- present and reliably OCR'd on every chapter
2. **Chart header `Aa:` line** -- e.g., `Aa: 17 Sg 22` -- partially OCR'd, sometimes garbled

The author's narrative refers to "01st house" or "lagna" contextually but never writes "Aquarius lagna" or "Tula lagna" as a phrase in prose. The sign must always be read from the table, not the narrative.

---

## Q4 -- Ayanamsha Check (Obama)

**Book states:** Lagna = **17 Li 20'** (Libra) · DOB 04 Aug 1961 · Honolulu

**Ayanamsha evidence from labeled-table chapters:**
- Ch005 (May 2, 1971): `Ayanamsha 23-28-18.29` → matches Lahiri ~23°28' for 1971 ✓
- Ch007 (Nov 5, 2001): `Ayanamsha 23-47-10.50` → matches Lahiri ~23°47' for 2001 ✓

Both values are textbook Lahiri. The ayanamsha used throughout the book is **Lahiri** -- confirmed.

**Engine verification pending:** Cannot compute Obama's ascendant without `vedic_calculator.py`. Recommend TT run: DOB 04 Aug 1961, 07:24 HST (17:54 UTC), Honolulu (21.3069°N, 157.8583°W), Lahiri ayanamsha → expected: Libra lagna. If the engine returns Libra lagna, Q4 is confirmed.

---

## Q5 -- Life Outcome Types -- Frequency Ranking

| Rank | Outcome Type | Chapters in Sample | Notes |
|---|---|---|---|
| 1 | **Career / rise to power / profession** | 9/9 -- unanimous | Every single chapter |
| 2 | **Marriage / relationships / marital discord** | 5/9 | Diana, Ch002, Ch005, Lincoln (brief), Hema Malini |
| 3 | **Death / assassination / tragic end** | 4/9 | Lincoln, Shastri, MLK, Diana |
| 4 | **Wealth / financial outcomes** | 2/9 | Ch005, Ch007 |
| 5 | **Spiritual / activism / social leadership** | 1/9 | MLK |
| 6 | **Foreign / exile / settlement** | 1/9 | Shastri (died in Tashkent) -- indirect |

**Key pattern:** Every chapter -- without exception -- analyses career/professional rise. Death is the second most analysed axis for famous subjects. Marriage/relationships is the primary axis for non-famous female subjects.

---

## Q6 -- Dasha References

**Yes -- dasha is consistently mentioned.** Format: `Mahadasha-Antardasha[-Sub-antardasha]` paired with house signification commentary.

> **Ch004 (Obama) -- verbatim:**
> *"In the VMD of Jupiter-Sun-Jupiter, the native became President of his country."*
> (VMD = Vimshottari Maha Dasha; Jupiter MD → Sun AD → Jupiter sub-AD)

> **Ch005 (Three Planets Exalted) -- verbatim:**
> *"Education was broken during Saturn-Saturn (05, 03, 08) in teens."*
> (Saturn MD → Saturn AD; house numbers in parentheses = houses the dasha lord signifies)

**Pattern:** Dasha is mentioned in roughly 50-70% of cases, but only when the author is tying a specific event to a time period. Career-rise analyses typically state planetary combinations without a dasha period. **Death cases reliably include dasha.**

---

## Q7 -- Analysis Length per Case

| Chapter | Subject | Sentences | Approx. Words |
|---|---|---|---|
| Ch001 | Abraham Lincoln | 7 | ~145 |
| Ch004 | Barack Obama | 4 | ~80 |
| Ch009 | Hema Malini | 8 | ~155 |
| Ch010 | LB Shastri | 6 | ~120 |
| Ch118 | Martin Luther King | 5 | ~90 |
| Ch135 | Princess Diana | 7 | ~130 |
| Ch002 | Girl -- Love Affair | 5 | ~100 |
| Ch005 | Three Planets Exalted | 6 | ~120 |
| Ch007 | Standard Nativity | 5 | ~110 |

**Range: 4-8 sentences / 80-155 words per chapter.** These are very concise case analyses -- typically 3-5 distinct KP observations per case. Each sentence is almost always a standalone observation. Expect **3-6 `author_observations[]` entries per chapter**, not 10+.

---

## Q8 -- Framework: KP or BPHS?

**Pure KP (Krishnamurti Paddhati) -- unambiguous across all 9 samples.**

| KP Indicator | Evidence |
|---|---|
| "own star" | Planet in its own nakshatra -- core KP term |
| "posited in star of..." | Star lord signification chain |
| "Significations" column | Lists house numbers a planet significates via its star lord -- KP sub-lord table |
| "Rahu offers result of Jupiter" | Rahu/Ketu acting as proxies for dispositors -- KP rule |
| `(Democracy)` for Saturn, `(Government)` for Sun, `(Power)` for Mars | KP planetary significator conventions |
| VMD with MD-AD notation | Vimshottari Maha Dasha as used in KP |

**Zero BPHS terminology** across all 9 samples -- no yoga names, no drishti, no Navamsa references, no Panchamahapurusha, no Parashari house-lord combinations.

**The `p` column** in the body-longitude table is likely **Pada** (KP nakshatra sub-division marker, 1-4).

---

## Q9 -- Multiple Persons / Very Short Cases

- **No multiple persons on any sample page** -- each chapter PDF is strictly one subject
- **Shortest cases:** Obama (4 sentences) and MLK (5 sentences)
- **No case under 4 sentences** in the 9 samples
- Some chapters are thematic (Ch005: "Three Planets Exalted") rather than biographical -- these tend to be slightly more analytical but not longer

---

## Q10 -- OCR Issues

| Chapter | Issue | Severity | Mitigation |
|---|---|---|---|
| All | Chart grid (Rasi diagram) area garbles consistently | High | Not needed -- body-longitude table covers planet positions |
| Ch001 | "Febrv•ry 12, 180V" (= February 12, 1809) | Medium | Parse-able with correction |
| Ch004 | `Aa: Ill U4{1 111 en 04-BK` -- lagna header garbled | High | Use body-longitude table |
| Ch009 | Date area: "oetot><>r16.19<18" (= October 16, 1948) | Medium | Parse-able |
| Ch010 | Chart header almost entirely garbled -- birth date/time not extractable | High | Set `time_confidence: "unknown"` |
| Ch118 | Minor character substitutions -- readable | Low | None needed |
| **Ch135** | **"July 1, 1901"** -- OCR error, must be corrected to **1961** | **Critical** | Hard-code correction |
| Ch135 | Timezone garbled as "(1;00 ••..C)" -- likely 1:00 East (BST), not west | Medium | Correct to UTC+1 |
| Ch135 | Time 16:45 vs. historical record of 19:45 BST | Medium | Flag; use book value, note discrepancy |
| Ch002 | Birth date/time not visible in OCR -- chart image area only | High | Lagna degree (17 Sg 22) is readable from `Aa:` line |

**Reliable on every page without exception:** Body-longitude planet table (Lagna through Ketu + Significations column). This is the primary extraction surface for the decoder.

---

## Q11 -- Non-Famous Subjects: Identifying Information

**None provided.** For all anonymous subjects:
- No name -- chapter title becomes the `name` field (e.g., `"A Girl Married Through Love Affair"`)
- No identifying information whatsoever -- author uses "the native" or "the following native" exclusively
- Coordinates given (lat/long) but no place name
- `public_figure: false` for all

**Exception -- Ch007:** States `"The boy is 12 years old as on 2013"` -- the author discloses the approximate year of writing and subject's age, enabling DOB cross-check: Nov 2001 + 12 years = ~2013 ✓. This also establishes the book's approximate writing date.

---

## Q12 -- Age at Time of Analysis

**Mixed -- both retrospective and live consultation cases exist:**

| Type | Chapters | Notes |
|---|---|---|
| **Retrospective** (historical figures) | Ch001, Ch004, Ch009, Ch010, Ch118, Ch135 | No age stated; post-mortem analysis for deceased |
| **Current consultation** (~2013 writing date) | Ch002, Ch005, Ch007 | Present-tense narrative; author is active counsellor |

- Ch007: *"The boy is 12 years old as on 2013"* -- predictive case
- Ch005: *"complaints that the wealth factors are low and asks why"* -- active consultation

**Writing date established as ~2013** from Ch007. This matters for dasha computation in non-famous living subjects: "current" dasha = ~2013.

---

## Summary Flags for TT Decision

| # | Flag | TT Action Required |
|---|---|---|
| F1 | **3 distinct birth data formats** -- labeled table, chart-embedded, intro paragraph | Confirm: decoder reads all three; body-longitude table is fallback primary |
| F2 | **~33% of chapters: birth date/time not OCR-recoverable** (famous subjects, chart-embedded) | Confirm: use Lagna degree from table to cross-check computed time? Or accept `time_confidence: "unknown"` |
| F3 | **Ch135 Diana: OCR reads 1961 as "1901"** -- must hard-correct | Confirm: apply correction in decoder |
| F4 | **Framework is pure KP** -- no BPHS. Significations column = KP house significator system | Confirm: existing KE rules are KP-compatible for Layer B evaluation |
| F5 | **Ayanamsha = Lahiri** -- confirmed by labeled table values | Confirmed -- engine already uses Lahiri |
| F6 | **Analysis length: 4-8 sentences / 80-155 words** -- each sentence = 1 KP observation | Confirm: expect 3-6 `author_observations[]` per chapter, not 10+ |
| F7 | **Obama ayanamsha engine check pending** -- need TT/CC to run before full decode | Run: DOB 04 Aug 1961, 17:54 UTC, Honolulu → expected Libra lagna |

---

*Step 1 complete. Awaiting TT review and sign-off before Step 2 (full 136-chapter decode).*
*Thread 3 -- 300 Important Horoscopes Vol 1 Part 1*
*Batch ID: `tv_300h1_decode_v1`*
