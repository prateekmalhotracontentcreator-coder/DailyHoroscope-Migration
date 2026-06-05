# Pre-Decode Q&A -- Longevity + Unnatural Deaths
## TV-Longevity Decode v1 | Batch ID: `tv_lu_decode_v1`
> Prepared by: CC (Claude Code)
> Date: 2026-06-05
> Status: **✅ REVIEWED + APPROVED 2026-06-05 -- S1/S2/S3/S4 all approved + 2 additional schema fields added. Thread 1 green-lit for full decode.**
> Samples read: Ch07 (Garfield), Ch11 (JFK), Ch12 (Indira Gandhi), Ch17 (Reagan), Ch88 (Amitabh Bachchan), Ch99 (John Lennon)

---

## Q1 -- Exact Format of Birth Data

**Format: Labelled sidebar block + inline confirmation sentence + detailed KP table.**

Each chapter opens with a structured block (typeset sidebar/box on page 1) followed by an inline sentence, then a planet table. Example from **2 chapters**:

**Ch12 -- Indira Gandhi (exact extract):**
```
Date: Nov 19, 1917
Time: 11:39:00 pm
Time Zone: 5:30: (E of GMT)
Place: 81 E 84', 25 N 45'
         Allahabad, India
Lunar Yr-Mo: Pingala - Karthika
Tithi: Sukla Shashthi
Vedic Weekday: Monday (Mo)
Nakshatra: Uttarashadha
Yoga: Ganda (Sa)
Hora Lord: Mars
Sunrise: 6:24:36 am  |  Sunset: 5:06:40 pm
Janma Ghatis: 43.0999
Ayanamsa: 22-36-49.00
Sidereal Time: 3:31:23
```
Followed by: *"Mrs. Indira Gandhi was born on 19 Nov 1917 at 11-39 pm Allahabad, 81 E 84', 25 N 45', India."*

**Ch99 -- John Lennon (exact extract):**
```
Date: 09 Oct 1940
Time: 6:30:00 pm
Time Zone: 1:00 (E of GMT)
Place: 3 W 00', 53 N 25'
         Liverpool, UK
Lunar Yr-Mo: Vikrama - Aswayuja
Tithi: Sukla Navami (Su)
Vedic Weekday: Wednesday (Me)
Nakshatra: Sravanam (Mo)
Hora Lord: Jupiter
Sunrise: 7:33:11 am  |  Sunset: 6:24:28 pm
Janma Ghatis: 27.3672
Ayanamsa: 22-55-59.66
Sidereal Time: 18:30:43
```
Followed by: *"John Lennon was born on 09 Oct 1940 at 06-30 pm Liverpool, England."*

Below that -- a full **KP planet table** (Body | Longitude | Star/Pada | Significations) is always present.

> **⚠️ Note for Ch07 (Garfield):** The chapter title page (book p.30) is missing from this scan. The structured sidebar block is absent. Birth data is recoverable from the chart header text on page 31: `November 19, 1831 | 6:28:00 (5:00 west) | 80W31, 41N20` and the inline sentence: *"...born on 19 Nov 1831 at 06-28 a.m., Orangeville, 80 W 31' 09", 41 N 20' 21" Ohio, USA."*

---

## Q2 -- Birth Time Availability

**All 6 sample chapters have exact birth times (HH:MM or HH:MM:SS):**

| Chapter | Time | Format |
|---|---|---|
| Ch07 Garfield | 6:28:00 am | HH:MM:SS |
| Ch11 JFK | 3:09:00 pm | HH:MM:SS |
| Ch12 Indira Gandhi | 11:39:00 pm | HH:MM:SS |
| Ch17 Ronald Reagan | 4:16:00 am | HH:MM:SS |
| Ch88 Amitabh Bachchan | 3:04:30 pm | HH:MM:SS (including seconds) |
| Ch99 John Lennon | 6:30:00 pm | HH:MM:SS |

All are sourced from software output (Free Jaganadha Hora). These are chart-rectified or software-sourced times, not necessarily birth register times. No "approximate" markers appear in these 6 samples. Birth time confidence should be recorded as `"from_chart"` for all. It is likely a handful of the 93 chapters may have approximate times -- this will surface during full decode.

---

## Q3 -- Ayanamsha Used + Lahiri Check for JFK

**Yes -- ayanamsha is explicitly stated in every chapter's sidebar block.** Format: `DD-MM-SS.ss` (degrees-minutes-seconds).

Book ayanamsha values across the 6 samples:

| Chapter | Subject DOB Year | Ayanamsha Stated |
|---|---|---|
| Ch11 | 1917 | `22-42-12.76` |
| Ch12 | 1917 | `22-36-49.00` |
| Ch17 | 1911 | `22-31-07.92` |
| Ch88 | 1942 | `22-57-40.37` |
| Ch99 | 1940 | `22-55-59.66` |

These values are consistent with **Lahiri/Chitrapaksha ayanamsha** progression across years. The copyright page of the book confirms: *"Charts generated through Software: Free Jaganadha Hora"* -- which uses Lahiri by default.

**JFK Lahiri verification:**
- DOB: 29 May 1917 | 3:09 PM EST | Brookline MA (42°21'30"N, 71°03'37"W)
- Book stated lagna: **Virgo -- 29° Vi 05'** (from KP table: `Lagna 29 Vi 05' 04.32"`)
- Text confirms: *"lagna lord Mercury"* → Mercury rules Virgo ✓
- Book ayanamsha: `22-42-12.76` for 1917. Lahiri for this date ≈ 22°40'-22°43' ✓
- **Engine match expected: YES** -- Virgo lagna at 29°05' is internally consistent with Lahiri ayanamsha for this birth data.

> **Recommendation:** Use `"ayanamsha": "lahiri"` uniformly for all 93 chapters. Verify by computing lagna from `vedic_calculator.py` against `lagna_stated_in_book` for each chapter; flag mismatches in `mismatch_notes`.

---

## Q4 -- House Cusps: Numerical or Visual Only?

**Numerical planet longitudes are always given. Bhava cusps (houses 2-12) are NOT given.**

The KP table provides exact longitudes for each planet (e.g., `Lagna 29 Vi 05' 04.32"`). The **lagna degree is always given numerically as the first row**. However, there are **no separate Bhava/house cusp tables** -- cusps for houses 2-12 are not listed anywhere in the text. The visual Rasi chart shows the South Indian grid diagram but without printed cusp degrees.

For computation purposes: the lagna degree + planet sign/degree is sufficient to reconstruct the chart.

---

## Q5 -- Does Author Explicitly State Lagna in Text?

**Lagna is always available from the KP table (first row: "Lagna DD Sign MM'"). The author almost always names the lagna sign or its lord explicitly in the analytical prose.**

Examples:

| Chapter | Quote from text | Lagna |
|---|---|---|
| Ch07 Garfield | *"Sun is badhka for Libra lagna"* | Libra -- explicit ✓ |
| Ch11 JFK | *"lagna lord Mercury"* | Virgo (Mercury rules Virgo) ✓ |
| Ch12 Indira Gandhi | *"lagna lord Sun"* | Leo (Sun rules Leo) ✓ |
| Ch17 Reagan | *"lagna lord Jupiter"* | Sagittarius (Jupiter rules Sagittarius) ✓ |
| Ch99 Lennon | *"Asc. is falling in the star of Mercury, who is maraca and badhaka"* | Pisces (Mercury is maraka/badhaka for Pisces) ✓ |

**Sign abbreviations in the KP table** (reliable, low OCR error):
`Ar Ta Ge Cn Le Vi Li Sc Sg Cp Aq Pi`

> **Note:** The chart header "As: XX YY" line sometimes has OCR garbling (e.g., Ch07 shows `"24 U 56"` where `"U"` is a misread of `"Li"` for Libra). The **KP table lagna row is the authoritative source** -- always prefer it over the chart header abbreviation line.

---

## Q6 -- Is Death Information Explicitly Stated?

**Yes -- always explicitly stated for death cases. Survival cases also explicitly describe the event, date, and outcome.**

Verbatim examples:

> **Garfield:** *"Garfield died on 19-Sep-1881 at 10-35 p.m. due to septic and shock resulted from the gunshot during the VMD period of Jupiter Sun-Mars in his 50th year."*

> **Indira Gandhi:** *"Mrs. Gandhi was killed by her own security guards on 31 Oct 1984 in New Delhi in her 67th year."*

> **John Lennon:** *"he was shot by Mark David Chapman at the entrance of the building where he lived, in New York City, on Monday, 08 Dec 1980"* + *"Death occurred when native was 40 years and 02 months old"*

For **survival cases**, event + outcome are both explicitly stated:

> **Reagan:** *"On March 30, 1981, Reagan...were shot by John Hinckley, Jr., outside of the Hilton Washington hotel"* + *"In fact President Reagan died of pneumonia, after a long struggle with Alzheimer's disease, on June 5, 2004."*
> → Two distinct events: assassination attempt (survived) + natural death (2004).

> **Amitabh Bachchan:** *"Mr. Bachchan was critically injured on 26 July 1982 in the intestines while filming a fight scene...which almost cost him his life"* -- survived.

> **Schema implication:** Some chapters contain **two events** (life-threatening event survived + separate actual death). The JSON should support both. → See Schema Flag S1 below.

---

## Q7 -- Does Author Always Name Dasha/Antardasha at Death?

**Yes -- without exception in all 6 samples.** Always stated, formatted as hyphen-separated VMD levels:

| Chapter | Period at Death/Event | Levels |
|---|---|---|
| Ch07 Garfield | `Jupiter Sun-Mars` | MD-AD-PD (3 levels) |
| Ch11 JFK | `Jupiter Saturn-Saturn-Jupiter` | MD-AD-PD-SD (4 levels) |
| Ch12 Indira Gandhi | `Saturn-Rahu-Jupiter-Saturn` | MD-AD-PD-SD (4 levels) |
| Ch17 Reagan (injury) | `Saturn-Mercury-Jupiter-Jupiter` | MD-AD-PD-SD (4 levels) |
| Ch88 Bachchan (injury) | `Saturn-Sun-Venus Mercury` | MD-AD-PD-SD (4 levels) |
| Ch99 Lennon | `Jupiter-Mercury-Moon` | MD-AD-PD (3 levels) |

**VMD = Vimshottari Mahadasha + Bhukti (Antardasha) + Antara (Pratyantardasha) + Sookshma (optional 4th level)**

> **Parsing note:** OCR sometimes drops hyphens between the 3rd and 4th levels (e.g., `"Venus Mercury"` instead of `"Venus-Mercury"`). Parser must tolerate space-separated as well as hyphen-separated tokens.

---

## Q8 -- Terminology Framework: BPHS, KP, or Mixed?

**Primary framework: KP Jyotish + Jaimini Karakas + BPHS maraka/badhaka concepts.** A hybrid -- but unmistakably KP in its core signification analysis method.

**KP elements present:**
- House significator tables (e.g., `02,11,04,05`) -- classic KP star-based signification
- Nakshatra/star lord chain for significations (e.g., *"Mars is in the star of Moon, who is occupant of 08th"*)
- Sub-lord concept implied through star lord analysis
- No explicit "CSL" (Cuspal Sub-Lord) terminology found in these samples

**Jaimini Karakas (always listed in chart header and KP table):**

| Code | Karaka |
|---|---|
| AK | Atma Karaka |
| AmK | Amatya Karaka |
| BK | Bhratru Karaka |
| DK | Dara Karaka |
| GK | Gnati Karaka |
| MK | Matru Karaka |
| PiK | Pitru Karaka |
| PK | Putra Karaka |

**BPHS elements present:**
- Maraka (2nd and 7th lords/occupants)
- Badhaka (badhaka house and its lord -- sign-type specific)
- Longevity classification: Alpa/Madhya/Poorna Aayu (short/medium/long life)
- Vimshottari dasha system (shared between KP and BPHS)

**Not present:** Traditional BPHS Ashtakavarga, Shadbala, or explicit KP CSL methodology.

> **Extraction note:** In `rule_observation_raw`, preserve the author's exact house-number notation (e.g., `"08th lord"`, `"06th house"`) -- this is the source vocabulary for rule candidate extraction and must not be normalised during decode.

---

## Q9 -- Typical Analysis Length Per Case

| Chapter | PDF Pages | Est. Prose Word Count |
|---|---|---|
| Ch11 JFK | 4 pages | ~700-800 words |
| Ch12 Indira Gandhi | 4 pages | ~600-700 words |
| Ch17 Ronald Reagan | 4 pages | ~650-750 words |
| Ch88 Amitabh Bachchan | 4 pages | ~550-650 words |
| Ch99 John Lennon | 4 pages | ~600-700 words |

Each page yields approximately 250-300 words of analytical prose (after deducting tables and chart diagram area).

Short cases (3-page chapters: Ch25, Ch26, Ch27, Ch28, Ch68, Ch69, Ch76, Ch84) likely run **~350-500 words** of analysis.

---

## Q10 -- Chapters with 2+ Persons / Very Short Entries

**No chapter in the 6 samples contains 2 persons.** Each chapter is dedicated to exactly one subject.

Notable observations from the full chapter list:
- **Romanov family (Ch52-Ch58):** 7 consecutive chapters -- Emperor Nicholas II, Empress Alexandra, Grand Duchesses Maria/Olga/Tatiana/Anastasia, and Alexei. All died in the same event (1918). These chapters likely share near-identical analytical structure. The children's charts may be very short entries (possibly 3 pages each).
- **3-page chapters** (Ch25, Ch26, Ch27, Ch28, Ch68, Ch69, Ch76, Ch84) are likely the shortest entries -- some may be under half a page of actual prose analysis.

---

## Q11 -- OCR Issues Observed

| Chapter | Issue | Severity |
|---|---|---|
| **Ch07 Garfield** | Chapter title page (book p.30) entirely missing from scan. Birth sidebar block absent. All other data recoverable. | 🔴 High |
| **Ch11 JFK** | Chart header planet line severely garbled: `"k: 2!1Yil5 SU: 1Hol8-PI< Mo: 24lt3S-BK Ma: 25h#M«"` | 🟡 Medium |
| **Ch17 Reagan** | Chart area has scattered label fragments (`"a Ra"`, `"Mo"`, `"Ve"`) -- prose text is clean | 🟢 Low |
| **Ch88 Bachchan** | Chart area OCR artifacts (`"(Sa) HL Ke Gk"`, `"Ke Md"`) -- normal chart label scatter | 🟢 Low |
| **Ch99 Lennon** | Retrograde notation (`"Jup.(R)-AmK"`, `"Saturn (R)-BK"`) may be read inconsistently across chapters | 🟢 Low |
| **All chapters** | The compact chart header line `"As: / Su: / Mo: / Ma: / Me: / Ju: / Ve: / Sa: / Ra:"` is the primary OCR-garbled zone | 🟡 Medium |

**Reliable data sources in order of OCR quality:**
1. ✅ **KP Body table** (Body | Longitude | Star/p | Significations) -- always clean, use this as primary planet source
2. ✅ **Prose narrative** -- generally clean
3. ✅ **Birth sidebar block** (Date / Time / Place fields) -- always clean
4. ⚠️ **Chart header abbreviation line** (`"As: XX Su: XX-PK..."`) -- frequently garbled, use as secondary/cross-check only

---

## Q12 -- Consistency: Chart Diagram vs. Text

**Spot-checked JFK and Indira Gandhi -- fully consistent.**

**JFK check:**
- Table: `Moon-BK 24 Le 34'` → Moon in Leo = 12th house from Virgo lagna; significations include `12` ✓
- Table: `Mercury-AK 27 Ar 53'` → Mercury in Aries = 8th house from Virgo; significations include `08` ✓
- Text: *"lagna lord Mercury in Q8th house"* → matches Mercury in Aries (8th from Virgo) ✓
- Text: *"mutual aspect of Q6th lord Saturn and Q8th lord Mars"* → Saturn rules Aquarius (6th from Virgo) ✓; Mars rules Aries (8th from Virgo) ✓

**Indira Gandhi check:**
- Table: `Mars-MK 16 Le 29'` → Mars in Leo = 1st house (Leo lagna)
- Text: *"Mars is posited in lagna, being badhaka lord"* ✓
- Table: `Jupiter(R)-PiK 15 Ta 05'` → Jupiter in Taurus = 10th house from Leo lagna
- Text: *"Jupiter, lord of 05 and 08, is in 10th house"* ✓

**Conclusion: Chart data and textual analysis are fully consistent across all samples checked.** The visual Rasi chart, the KP planet table, and the prose analysis all refer to the same underlying chart and do not contradict each other.

---

## Schema Adjustment Flags -- Requires TT + CC Confirmation

**Before full decode of 93 chapters, please confirm the following 4 adjustments to the JSON schema:**

| # | Flag | Issue | Proposed Handling |
|---|---|---|---|
| **S1** | `events[]` array | Reagan has **2 distinct events**: assassination attempt survived (1981) + actual death from natural causes (2004). The base schema's single `death_data{}` block is insufficient for survival cases with a separate later death. | Add `events[]` array for life-threat events; keep `death_data{}` for the terminal death event. |
| **S2** | VMD depth variability | Author states 3-level periods (`MD-AD-PD`) in some chapters and 4-level (`MD-AD-PD-SD`) in others. OCR sometimes drops hyphens between the 3rd and 4th elements. | Store as a structured object: `{ "mahadasha": "X", "antardasha": "X", "pratyantardasha": "X", "sookshma": null }` with `null` for absent levels -- instead of a raw string. |
| **S3** | Ch07 partial chapter | Garfield chapter is missing its title page. Birth data is recoverable but the full structured sidebar block is absent. | Add `"extraction_note"` field on the birth_data object for this chapter: `"Chapter title page (book p.30) missing from scan. Birth data sourced from chart header and inline text."` |
| **S4** | OCR source priority | The chart header abbreviation line is frequently garbled. If decoded naively it would produce wrong planet signs. | Hard rule for decode: **always extract planet positions from the KP Body table**, not the chart header line. Note this in the decode instructions. |

---

*Pre-Decode Q&A complete. Awaiting TT + CC sign-off on Schema Flags S1-S4 before Step 2 (Full Decode) begins.*
*Thread 1 -- Longevity + Unnatural Deaths Decode | Batch: `tv_lu_decode_v1`*
