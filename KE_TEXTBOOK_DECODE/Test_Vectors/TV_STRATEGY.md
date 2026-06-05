# KE Milestone 2 -- Test Vector & Case Study Decode Strategy
## Affirming KE Highest Standards via Classical Case Studies

> Prepared: 2026-06-05 · CC (Claude Code)
> Revised: 2026-06-05 (v2) · Incorporates TT inputs + GAI evaluation framework review
> Status: **🟢 ACTIVE -- All 4 threads running. Combined Pre-Decode review complete.**
> Purpose: Empirical accuracy benchmark + new rule extraction + profession library -- enabling co-founder KE rule approval

---

## 1. The Three Goals of This Milestone

| Goal | What It Produces | Why It Matters |
|---|---|---|
| **G1 -- Test Vectors** | Structured JSON for each historical chart with birth data + known outcomes | Benchmarks rule accuracy; pass/fail for each rule claim |
| **G2 -- Case-Derived Rules** | New rules extracted FROM the case study books (not just testing existing rules) | These books analyse real charts in ways the classical textbooks don't -- they are a rule source, not just a test bench |
| **G3 -- Profession Library** | Aggregated profession × placement mappings (Planet × House × Sign × Lagna) | 765+ data points → statistical patterns → a dedicated Profession inference engine layer |

**Together:** G1 validates existing KE rules. G2 fills gaps those rules don't cover. G3 opens a new KE capability (profession prediction) that no classical textbook alone provides at this sample size.

---

## 2. Source Inventory -- Revised

| # | Book | Split Files | Cases | Primary G | Secondary G | Hold |
|---|---|---|---|---|---|---|
| B1 | **Longevity + Unnatural Deaths** | 93 split PDFs | 93 | G1 + G2 | -- | -- |
| B2 | **765 Notable Horoscopes** | 765 half-page PDFs | 765 | G3 | G1 (Layer A) · Layer B deferred to Phase 4 | -- |
| B3 | **300 Horoscopes Vol 1 Part 1** | 136 split PDFs | 136 | G1 + G2 | -- | -- |
| B4 | **300 Horoscopes Vol 2 Part 2** | 153 split PDFs | 153 | G1 + G2 | -- | -- |
| B5 | Destiny Numerology | ~50 JSONs | ~50 | -- | -- | ⏸ HOLD |

**Total active cases: ~1,147**

---

## 3. Three Extraction Layers -- One Decode Pass, Three Outputs

**Core principle: Each book is decoded ONCE. The thread extracts everything needed for all three layers in a single pass. Layers A, B, and C are then CC-side computation/evaluation tasks run against the already-extracted JSON -- the PDFs are never re-read.**

```
Thread (single pass)          CC (computation -- runs when ready)
─────────────────────         ──────────────────────────────────
Extract birth data        →   Layer A: run vedic_calculator.py → match rate
Extract author analysis   →   Layer B: run scan_chart() → rule hit rate
Extract profession/facts  →   Layer B (765H): match profession label vs KE output
Flag gap observations     →   Layer C: encode as new KE rule candidates
```

### Layer A -- Engine Calibration
**Question:** Does `vedic_calculator.py` compute the same chart as the book?
- **Thread extracts:** stated lagna + moon sign from author text
- **CC computes:** run vedic_calculator.py on birth data, fill `chart_verification` block
- **Gate: ≥99% lagna match across Gold-tier vectors** *(upgraded from 90% -- the deterministic computation layer must be near-perfect; mismatches are engine bugs, not acceptable margin)*
- **Secondary gate (765H):** dasha balance match within ±1 day vs `dasha_balance_from_book` -- precision test for `calculate_vimshottari_dasha()`

### Layer B -- Rule Accuracy
**Question:** Do our KE rules correctly fire on these charts?
- **Thread extracts:** every author "condition → outcome" observation, structured in `author_observations[]`
  - For 765H: no author analysis exists -- `profession` label IS the Layer B expected output (`layer_b_expected`)
  - For Longevity/300H: author analysis text mapped to condition types + claim_axis
- **CC evaluates (when KE rules are ready):** run `scan_chart()`, score hits vs. expected
- **765H note:** Layer B computation deferred until KE profession-inference rules are encoded from G3 data. The JSON is fully populated in the single decode pass. No second decode ever needed.

### Layer C -- Gap Detection (New Rules Needed)
**Question:** What do these case studies teach that our 12,380 rules DON'T yet cover?
- **Thread flags:** observations with no matching KE rule → `gap_flag: true`
- **CC encodes:** flagged observations become `LU_CaseDerived_Rules.json` etc.
- **This is as important as A + B** -- case study books are a rule source, not just a test bench

---

## 4. What Each Book Delivers -- Comprehensive Extraction

### B1: Longevity + Unnatural Deaths (93 charts)
**Full extraction target per chart:**
```
birth_data         : date, time, place (lat/long, TZ)
chart_positions    : planet in house (extracted from text + diagram)
lagna              : stated by author
cause_of_death     : explicit (assassination, accident, disease, etc.)
age_at_death       : exact or approximate
key_life_events    : with dates
author_analysis    : full text of case commentary
death_related_factors : 8th lord, maraka, badhaka, dasha at death
rule_observations  : structured extraction of every "X causes Y" statement
gap_flags          : observations with no matching KE rule
```
**Output A:** 93 Test Vector JSONs
**Output B:** `LU_CaseDerived_Rules.json` -- new rules extracted from patterns across all 93 charts
**Output C:** Layer C gap list -- death-related conditions not yet encoded in KE

### B2: 765 Notable Horoscopes
**Full extraction target per chart:**
```
birth_data         : date, time, place
chart_positions    : lagna + planets in houses (from text; visual grid not OCR-able)
lagna              : from birth data computation / stated in text
profession         : MANDATORY -- stated in heading or body for every chart
profession_category: mapped to taxonomy (see Section 6 below)
author_note        : any brief notes the book provides
```
**Output A:** 765 Test Vector JSONs (Layer A calibration)
**Output B:** `Profession_Library_Raw.json` -- 765 × {profession, lagna, planet_positions}
**Output C:** Aggregated profession × placement frequency table
**Note:** 765 Horoscopes has no deep author analysis per chart. G3 (Profession Library) is the primary deliverable. Layer B rule accuracy is NOT applicable here.

### B3 + B4: 300 Horoscopes Vol 1 + Vol 2 (289 charts total)
**Full extraction target per chart:**
```
birth_data         : date, time, place
lagna              : stated
moon_sign          : stated
key_life_outcomes  : profession, marriage, wealth, death (where applicable)
author_analysis    : full text
rule_observations  : every "X causes Y" statement structured
dasha_at_event     : if author mentions dasha running during a key event
gap_flags          : no matching KE rule
```
**Output A:** 289 Test Vector JSONs
**Output B:** `300H_CaseDerived_Rules_Vol1.json` + `300H_CaseDerived_Rules_Vol2.json`
**Output C:** Layer C gap list -- life outcome conditions not yet in KE

---

## 5. Case-Derived Rules -- Output Schema

Each observation the author makes about a chart that can be generalised becomes a Case-Derived Rule:

```json
{
  "rule_id": "lu-cdr-001",
  "source": "case_study_derived",
  "source_book": "Longevity and Unnatural Deaths",
  "source_chapter": "Ch11_John_F_Kennedy",
  "subject_name": "John F. Kennedy",
  "birth_data_ref": "tv-lu-ch11",
  "observation_verbatim": "Mars as 8th lord in lagna with Rahu aspecting 8th house...",
  "generalised_condition": {
    "type": "planet_in_house",
    "planet": "MARS",
    "house": 1,
    "additional_factors": ["mars_is_8th_lord", "rahu_aspects_8th"]
  },
  "claim_axis": "longevity",
  "claim_polarity": "negative",
  "effect": "Violent or accidental death indicated when 8th lord is in lagna with malefic aspect on 8th",
  "confirmed_by_cases": ["tv-lu-ch11"],
  "science_id": "jyotish",
  "approval_status": "pending_human_review",
  "gap_in_existing_ke": true,
  "existing_rule_match": null
}
```

---

## 6. Profession Library -- Taxonomy + Schema

### Profession Taxonomy (for 765 Horoscopes mapping)

| Category | Sub-types |
|---|---|
| Politics | Head of State · Minister · Politician · Freedom Fighter |
| Military | General · Admiral · Military Leader |
| Judiciary / Law | Judge · Lawyer · IPS/IAS Officer |
| Business | Industrialist · Entrepreneur · Banker |
| Entertainment | Actor · Singer · Dancer · Film Director |
| Sports | Cricketer · Athlete · Boxer |
| Spiritual / Religious | Saint · Spiritual Leader · Priest |
| Science / Academia | Scientist · Professor · Doctor |
| Arts / Literature | Writer · Poet · Journalist · Painter |
| Royalty / Nobility | King · Queen · Prince · Nawab |
| Criminal / Notorious | Criminal · Terrorist (for control chart study) |
| Other | |

### Profession Library JSON Schema (per person)
```json
{
  "subject_id": "765h-0011",
  "name": "Aamir Khan",
  "profession": "Actor",
  "profession_category": "Entertainment",
  "profession_subcategory": "Actor",
  "birth_data": { ... },
  "chart_positions": {
    "lagna": "Libra",
    "sun_house": 3,
    "moon_house": 7,
    "mars_house": 1,
    "mercury_house": 3,
    "jupiter_house": 9,
    "venus_house": 2,
    "saturn_house": 6,
    "rahu_house": 10,
    "ketu_house": 4,
    "sun_sign": "Sagittarius",
    "moon_sign": "Aries"
  },
  "source_book": "765 Notable Horoscopes",
  "source_file": "0011_A-2_Aamir_Khan.pdf",
  "layer_a_verified": null
}
```

### Profession Library Aggregation Output
After all 765 charts processed → frequency tables:
```
Profession: Actor (N=47)
  Most common lagna: Libra (23%), Leo (19%), Gemini (15%)
  Venus placement: House 1 (29%), House 7 (21%), House 5 (18%)
  Mercury placement: House 1 (26%), House 3 (22%)
  ...
```
This becomes the statistical backbone for a new KE inference layer: **Profession Prediction by Placement**.

---

## 7. Phase 4 -- Scoring & Evaluation Framework
*(Added 2026-06-05 -- based on GAI evaluation framework review)*

After CC runs chart computation against all four thread outputs, the evaluation is scored across four tiers. This moves us beyond binary pass/fail to a calibrated accuracy picture we can show co-founders.

### 4-Metric Evaluation Matrix

| Tier | Metric | How Calculated | Target |
|---|---|---|---|
| **1. Engine Accuracy** | Lagna match + dasha balance | Binary per vector: computed lagna = book lagna; dasha balance within ±1 day | **≥99%** |
| **2. Timing Precision** | Dasha window overlap at event | Does engine-computed dasha at death/event date match the book's stated dasha? | **≥90%** |
| **3. Rule Application Precision** | Jaccard similarity | `rules_fired ∩ expected_rules` / `rules_fired ∪ expected_rules` per case | **≥85%** |
| **4. Reasoning Faithfulness** | LLM-as-Judge (1-5 rubric) | Claude grades whether the KE's fired rules logically match the book's stated reasoning | **≥4.5 / 5** |

### LLM-as-Judge Scoring Rubric (Tier 4)

Applied to cases where `gap_flag: false` -- i.e., rules exist that should have fired:

| Score | Meaning |
|---|---|
| **5** | KE fired the correct rules AND dasha timing matches the book's stated period exactly |
| **4** | KE fired correct rules; timing off by one antardasha period or one house interpretation differs |
| **3** | KE identified the correct life outcome (career/death/marriage) but via wrong rules or different planetary reasoning |
| **2** | KE partially matched -- some correct elements but significant divergence in reasoning |
| **1** | KE output contradicts the book's case study -- wrong outcome OR wrong dasha |

### False Positive Guardrail

**Rule:** A test case where `event_category` is correct BUT `rule_precision_score < 0.70` is marked `false_positive_flag: true` and does NOT count as a Layer B pass.

Rationale: A KE that gets the right answer for the wrong astrological reason will fail on novel charts. Lucky text associations are not engine calibration. This guardrail ensures the engine is genuinely analytical.

### Updated `rule_evaluation` Block (all test vectors)

```json
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
}
```

### What Doesn't Apply to Our Architecture

The following from the GAI framework are RAG/vector-search-specific and do NOT apply:
- Vector Search / embedding models (we use structured MongoDB -- deterministic and more reliable)
- Context Precision / Recall IR metrics (only relevant for semantic retrieval, not our structured queries)
- deepeval / Ragas / Promptfoo (designed for RAG pipelines -- our structured query pipeline uses simpler Python scripts)
- `prompt_query` field (our KE works via `scan_chart(chart_json)` -- not prompt-based)

---

## 8. Parallel Thread Execution Plan -- Current State

| Thread | Book | Cases | Status |
|---|---|---|---|
| **Thread 1** | Longevity + Unnatural Deaths | 93 | 🟢 Running -- full decode in progress |
| **Thread 2** | 765 Notable Horoscopes | 765 | 🟢 Running -- full decode in progress |
| **Thread 3** | 300 Horoscopes Vol 1 Part 1 | 136 | ✅ Step 2 Complete -- 136 JSONs delivered |
| **Thread 4** | 300 Horoscopes Vol 1 Part 2 | 153 | ✅ Step 2 Complete -- 151 JSONs delivered |

**Next trigger:** When T1 and T2 deliver → CC runs Phase 4 (chart computation + scoring) across all four threads simultaneously.

---

## 8. Pre-Decode Questions -- Each Thread Must Answer First

**Before starting full decode, each thread reads their book's split PDFs (5-10 sample chapters) and answers these questions. Answers become the Brief's Blocker Annex.**

### Common Questions (all threads):
```
Q1. What is the exact format for birth data? (table, paragraph, combination?)
Q2. Is birth time stated in most entries, or often missing/approximate?
Q3. What ayanamsha does the book use? (Lahiri, KP, Raman -- check any chart that states lagna vs. sun sign)
Q4. Are house cusps given or only planet placements?
Q5. Is lagna always explicitly stated in text, or only shown in the visual chart grid?
Q6. What is the page/section structure? (1 person per page? Multi-page entries?)
Q7. Are there any chapters/sections with different formats that need special handling?
Q8. What OCR issues are visible? (blurry pages, garbled text, missing sections)
```

### Thread 1 -- Longevity + Unnatural Deaths (Additional):
```
Q9.  Is cause of death explicitly stated for every case, or implied from the analysis?
Q10. Does the author always state the dasha/antardasha running at time of death?
Q11. Does the book explicitly name 8th lord, maraka, badhaka -- or use other terminology?
Q12. Are there cases where multiple death charts are compared on one page?
Q13. What is the typical length of author analysis per case? (1 paragraph? 1 page? More?)
Q14. Are age-at-death and death date always present, or sometimes missing?
```

### Thread 2 -- 765 Notable Horoscopes (Additional):
```
Q9.  Where exactly is the profession stated -- in the filename/heading, or within the chart area?
Q10. Is profession always a single category, or sometimes compound (e.g., "Politician and Lawyer")?
Q11. Is there any author analysis text at all, or purely birth data + chart?
Q12. Are the 9 Divine Horoscopes (Lord Ram, Krishna, etc.) formatted differently from the alphabetical section?
Q13. How are multiple persons with the same profession distinguished?
Q14. Roughly what percentage of the 765 charts have the birth time clearly stated (vs. approximate)?
```

### Thread 3 -- 300 Horoscopes Vol 1 Part 1 (Additional):
```
Q9.  Does the author state lagna explicitly in text, or only in the chart?
Q10. What types of life outcomes are most commonly analysed? (career, death, marriage, wealth?)
Q11. Does the author reference dasha periods during key events?
Q12. Are there multi-person comparison cases on a single page?
Q13. What is the typical analysis length? Estimate words per case.
Q14. Does the book use KP, BPHS, or a mixed framework?
```

### Thread 4 -- 300 Horoscopes Vol 2 Part 2 (Additional):
```
Q9-Q14: Same as Thread 3.
Q15. Vol 2 seems to focus more on violent/political deaths -- confirm and characterise the death type distribution.
Q16. How many cases have cross-references to Vol 1 subjects (same person analysed in both)?
```

---

## 9. Thread Brief Structure -- What Each Thread Receives

Each thread gets a brief with:

```
1. Book Overview (1 paragraph)
2. Canonical Source Folder path
3. Split PDF folder path
4. Primary Deliverables (Test Vectors + Case-Derived Rules + [Profession Library for B2])
5. Output Schemas (from this strategy doc + TV_SCHEMA.md)
6. Pre-Decode Questions (from Section 8 above) -- ANSWER THESE FIRST
7. Sample decode: 3 chapters fully decoded as examples
8. Known OCR issues (from existing split scripts)
9. Batch ID + output folder
10. Review handoff: what CC + TT will check after decode
```

Individual thread briefs:
- `THREAD_BRIEF_TV_LONGEVITY_DECODE.md`
- `THREAD_BRIEF_TV_765H_DECODE.md`
- `THREAD_BRIEF_TV_300H1_DECODE.md`
- `THREAD_BRIEF_TV_300H2_DECODE.md`

---

## 10. Output Folder Structure

```
KE_TEXTBOOK_DECODE/Test_Vectors/
  TV_STRATEGY.md                          ← this file
  TV_SCHEMA.md                            ← full field reference (to be written)

  JSON/
    longevity_unnatural/                  ← 93 Test Vector JSONs (Thread 1)
      tv_lu_ch07_james_garfield.json
      tv_lu_ch08_osama_bin_laden.json
      ...
      LU_CaseDerived_Rules.json           ← G2 output
      LU_Gap_Report.md                    ← Layer C gaps

    765_horoscopes/                       ← 765 Test Vector JSONs (Thread 2)
      tv_765h_0011_aamir_khan.json
      ...
      Profession_Library_Raw.json         ← G3 raw output
      Profession_Library_Aggregated.json  ← G3 aggregated frequency tables

    300h1/                                ← 136 Test Vectors (Thread 3)
      tv_300h1_ch001_lincoln.json
      ...
      300H1_CaseDerived_Rules.json        ← G2 output

    300h2/                                ← 153 Test Vectors (Thread 4)
      tv_300h2_ch001_...json
      ...
      300H2_CaseDerived_Rules.json        ← G2 output

  Reports/
    layer_a_calibration_report.md         ← engine match rate (Phase 2)
    layer_b_accuracy_report.md            ← rule hit rate (Phase 3)
    layer_c_gap_report.md                 ← new rules needed (Phase 3)
    profession_library_summary.md         ← G3 summary (Phase 2)

Thread_Briefs/
  THREAD_BRIEF_TV_LONGEVITY_DECODE.md     ← Thread 1 brief (to be written)
  THREAD_BRIEF_TV_765H_DECODE.md          ← Thread 2 brief (to be written)
  THREAD_BRIEF_TV_300H1_DECODE.md         ← Thread 3 brief (to be written -- after T1+T2 review)
  THREAD_BRIEF_TV_300H2_DECODE.md         ← Thread 4 brief (to be written -- after T1+T2 review)
```

---

## 11. Revised Decisions -- Confirmed / Pending

| # | Decision | Status | Value |
|---|---|---|---|
| D1 | Store vectors as local JSON | ✅ Confirmed | Local JSON Phase 1-3, MongoDB Phase 4 |
| D2 | Ayanamsha | ✅ Confirmed | Lahiri (engine default) -- each thread to verify per book |
| D3 | Layer A pass rate gate | ✅ UPGRADED | ≥99% lagna match (GAI review: deterministic layer must be near-perfect) + dasha balance ±1 day for 765H |
| D4 | Numerology | ✅ Confirmed | ⏸ HOLD |
| D5 | Phase 4 Codex commission | ✅ Confirmed | After Phase 3 |
| D6 | Profession taxonomy | ✅ Added | 11-category system (Section 6) |
| D7 | Thread execution | ✅ Confirmed | 2 parallel (T1+T2 first), then 2 more (T3+T4) |
| D8 | Pre-decode Q&A | ✅ Added | Each thread answers Qs before full decode |
| D9 | 765H primary deliverable | ✅ Confirmed | Profession Library (G3), not rule accuracy |

---

## 12. Next Steps -- Current State

| # | Action | Owner | Status | Output |
|---|---|---|---|---|
| 1 | Write thread briefs (all 4) | CC | ✅ Done | All 4 briefs written + updated |
| 2 | Dispatch T1 + T2 | TT | ✅ Done | Both threads running |
| 3 | Pre-Decode Q&As + combined review | TT + CC | ✅ Done | `COMBINED_PREDECODE_REVIEW.md` |
| 4 | Dispatch T3 + T4 | TT | ✅ Done | Both threads issued |
| 5 | T3 full decode (136 chapters) | Thread 3 | ✅ Done | 136 JSONs delivered |
| 6 | T4 full decode (153 chapters) | Thread 4 | ✅ Done | 151 JSONs delivered |
| 7 | T1 full decode (93 chapters) | Thread 1 | 🟢 Running | 93 JSONs + LU_CaseDerived_Rules.json |
| 8 | T2 full decode (765 entries) | Thread 2 | 🟢 Running | 765 JSONs + Profession_Library |
| **9** | **CC: Layer A computation** -- run `vedic_calculator.py` on all completed vectors | **CC** | ⏳ Pending T1+T2 | `layer_a_calibration_report.md` |
| **10** | **CC: Layer B evaluation** -- run `scan_chart()` + 4-metric scoring | **CC** | ⏳ Pending T1+T2 | `layer_b_accuracy_report.md` |
| **11** | **CC: Layer C gap aggregation** -- cross-book gap analysis | **CC** | ⏳ Pending T1+T2 | `layer_c_gap_report.md` |
| **12** | **CC: LLM-as-Judge pass** -- score all Layer B results 1-5 | **CC** | ⏳ Pending scoring | Judge scorecard per rule cluster |
| **13** | **TT + Co-founder: rule approval review** | **TT** | ⏳ Pending reports | First batch `approved` status |

---

## 13. Link to KE Rule Approval Path

```
Current state:
  ~12,380 rules -- 0 approved -- Legacy Model is sole live signal

This milestone produces:
  Layer A → Engine calibration ≥99% → confirms vedic_calculator.py is precise
  Layer B → Rule accuracy report with 4-metric scoring (not just binary pass/fail):
              Tier 1: Engine accuracy ≥99%
              Tier 2: Timing precision ≥90%
              Tier 3: Rule application precision ≥85% (Jaccard)
              Tier 4: Reasoning faithfulness ≥4.5/5 (LLM-as-Judge)
  Layer C → Gap report → prioritised list of new rules to encode (G2 output above)
  G3     → Profession Library → new inference capability

What the scoring gives the co-founder:
  - Not just "X% of rules passed" but "rules scored ≥4.5/5 on the reasoning rubric"
  - False positives explicitly flagged (correct outcome, wrong reasoning -- these do NOT count)
  - Rule clusters ranked by precision score → co-founder approves highest-confidence first
  - Jaccard score shows rule noise (are we firing 10 rules when 3 were needed?)

Review sequence for co-founder approval:
  1. CC presents Layer A + B + C reports with 4-metric scorecard to TT
  2. TT reviews with co-founder -- spot-checks specific charts + judge scores
  3. Co-founder selects first batch for approval (Judge Score ≥4.5 + Rule Precision ≥85%)
  4. Approval gate opens: auto_approved → approved → reaches live users
  5. Phase 5 Codex commission locks scoring into automated CI test harness

Target: first approved rules in production before KP Oracle 30-day review milestone
```

---

*KE Milestone 2 -- Test Vectors, Case-Derived Rules, and Profession Library*
*Supersedes earlier TV_STRATEGY.md draft (2026-06-05 v1)*
