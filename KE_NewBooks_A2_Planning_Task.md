# Account 2 Task -- New Book Decode Guides
> Issued: 2026-05-26 | Session type: Guide authoring only -- no decoding
> Context window rule: ONE LINE per task completed. Nothing else.
> Previous plan already complete -- do NOT reassess books. Build the guides.

---

## CONTEXT (read, do not summarise)

The book assessment is already done at:
`/Users/apple/Documents/Knowledge Engine_eBooks/D. New Books Plan.md`

**CRITICAL -- read this section before authoring any guide. Every guide must embed these learnings.**

---

## LEARNINGS FROM PREVIOUS DECODES -- Mandatory in All 3 Guides

### L1 -- Full Schema (every rule, no exceptions)

The simplified schema in the task sections below is a STARTING POINT only. Every rule must have ALL of these fields. Reference: `KE_Book_Decode_Process_Technical.md` Part 3.

```json
{
  "rule_id": "bphs-ch12-001",
  "science_id": "vedic_astrology",
  "approval_status": "pending_human_review",
  "checkable": true,
  "active": true,

  "source": {
    "book": "BPHS Vol 1",
    "book_id": "bphs_vol1_20260526",
    "chapter": 12,
    "chapter_name": "Effects of 1st House",
    "sloka": "12.14",
    "batch_id": "bphs-ch12-v1-20260526",
    "passage_ref_id": null
  },

  "title": "Sun in Lagna -- Assertive and Commanding Personality",
  "summary": "Sun placed in the 1st house gives a dominant, courageous, and self-reliant nature.",
  "full_text": "When the Sun occupies the Ascendant at birth, the native possesses strong leadership ability, a commanding presence, and natural authority. Health may be robust but eyes and heart require attention.",
  "tags": ["sun", "lagna", "1st_house", "personality", "health"],
  "category": "house_effects",

  "condition": {
    "type": "planet_in_house",
    "planet": "sun",
    "house": 1,
    "sign": null,
    "nakshatra": null,
    "strength_requirement": null,
    "dasha_lord": null,
    "antardasha_planet": null,
    "applies_to_all_dasha_lords": false
  },

  "claim_axis": "career_growth",
  "claim_scope": "natal_trait",
  "claim_polarity": "positive",
  "timing_bias": "sustained",
  "strength_band": "high",
  "subject_scope": "self",
  "authority_override": null,
  "mutually_exclusive_with": [],

  "result": {
    "effect": "Commanding personality, leadership ability, robust constitution; susceptibility to eye and heart conditions.",
    "severity": "high",
    "remedy_available": false,
    "remedy_ref_id": null
  },

  "contradiction_flag": false,
  "duplicate_candidate": false,
  "duplicate_source": null
}
```

**checkable for each science:**
- BPHS / Phaladeepika → `"vedic_astrology"` → `checkable: true`
- KP Astrology → `"kp_jyotish"` → `checkable: false` (KP sub-lord engine not yet built)

**Valid condition.type for Vedic (BPHS / Phaladeepika):**
`planet_in_house`, `house_position`, `yoga_combination`, `planet_conjunction`, `planetary_position`, `planet_affliction`, `planet_combust`, `dasha_period`, `varga_dignity_tier`, `house_placement`

**Valid condition.type for KP:**
`kp_sub_lord`, `kp_significator`, `kp_badhaka`, `kp_longevity_factor`

**Valid claim_axis values:**
`health_vitality`, `career_growth`, `financial_security`, `partnership_stability`, `marriage_timing`, `spirituality`, `family_life`, `longevity`, `accident_risk`, `travel`, `creativity`, `social_network`, `general`

---

### L2 -- Multi-Dimension Extraction (Numerology lesson -- CRITICAL for house chapters)

**Lesson:** The Numerology decode under-extracted Ch4 by 108 rules because it merged all dimensions of each number into one rule. Ch4 re-extraction identified 7 distinct dimensions per number.

**Applied to BPHS house chapters:** For each planet-in-house combination, extract SEPARATE rules for each distinct dimension the text addresses:

| Dimension | BPHS example |
|---|---|
| Physical appearance / body | "Sun in Lagna -- Fair complexion, commanding stature" |
| Health tendencies | "Sun in Lagna -- Susceptibility to eye and heart conditions" |
| Personality / character | "Sun in Lagna -- Leadership, authority, self-reliance" |
| Career / professional | "Sun in Lagna -- Success in government, leadership roles" |
| Wealth / financial | "Sun in Lagna -- Moderate wealth through authority positions" |
| Relationships / spouse | "Sun in Lagna -- Domineering in relationships" |
| Children | "Sun in Lagna -- Few but distinguished children" (if stated) |
| Spiritual / dharmic | "Sun in Lagna -- Interest in father's tradition and authority" (if stated) |
| Enemies / opposition | "Sun in Lagna -- Overcomes enemies through assertiveness" (if stated) |

**Rule:** Each dimension the text explicitly addresses = one separate rule. Do NOT merge. A chapter with 9 planets × 8 dimensions = potentially 72+ rules, not 9.

---

### L3 -- Yoga and Combination Rules (300 Combinations lesson)

When a chapter contains YOGA conditions (multiple planets involved, not a single planet-in-house):
- `condition.type` = `"yoga_combination"`
- List ALL planets involved in the condition array
- Capture the yoga name if given (e.g., "Gajakesari Yoga", "Budhaditya Yoga")
- Add tag: the yoga name in snake_case
- `claim_scope` = `"natal_trait"` for yogas that describe character; `"event_timing"` for timing yogas

---

### L4 -- Dedup Against Already-Ingested Rules (300 Horoscopes lesson)

During decode, keep aware of cross-book overlaps:
- BPHS house rules may duplicate Longevity rules (same Parashari tradition)
- Phaladeepika will heavily duplicate BPHS (same tradition -- flag all overlaps)
- KP rules may duplicate 300 Horoscopes decode (same system)

Flag: `"duplicate_candidate": true, "duplicate_source": "bphs_vol1"` (or whichever source)
Do NOT skip the rule -- capture it fully, just flag it. The arbitration runtime handles duplicates.

---

### L5 -- What NOT to Decode (SBC and Longevity lesson)

| Content type | Action |
|---|---|
| Case study chapters (named horoscopes, historical examples) | → `case_studies` collection, NOT `interpretation_rules`. Separate pipeline. |
| Lookup tables (planet dignities, sign rulers, nakshatra lists) | → `DataTables.md` file only. Not rules. |
| Procedural/methodology chapters | → `claim_scope: "engine_specification"`. Still rules, but flagged. |
| Mythological/cosmological narrative | → Summary.md only. Zero rules. |
| Numeric coefficients (0.30×, 1.5× multipliers) | → Translate to intensity language: "significant", "moderate". No numbers in `effect` text. |

---

### L6 -- Rule Count Targets (Numerology lesson)

Set minimum rule count targets before starting each chapter. If actual count falls more than 30% below target, re-read before closing the chapter.

| Chapter type | Expected rule density |
|---|---|
| BPHS House chapter (Ch12-Ch23) | 40-80 rules per chapter (9 planets × multiple dimensions) |
| BPHS Yoga chapter (Ch35-Ch42) | 20-50 rules per chapter |
| KP chapter | 15-35 rules per chapter |
| Phaladeepika house chapter | 30-60 rules (overlaps expected -- still capture) |

If actual count is below the floor: post a flag line in context before closing the chapter. Do not silently under-extract.

---

BPHS Vol 1 recon is already done:

| Status | Chapters |
|---|---|
| ✅ Already decoded | Ch27, Ch34, Ch40, Ch41, Ch43, Ch44 |
| 🔴 Thread A -- START HERE | Ch11-Ch24 (House Effects + Bhava Lords) -- 14 chapters, all pending |
| 🟠 Thread B | Ch25, Ch26, Ch28-Ch33, Ch35, Ch36 -- 10 chapters pending |
| 🟡 Thread C | Ch37-Ch39, Ch42, Ch45 -- 5 chapters pending |
| ⬇️ Low priority | Ch01, Ch02, Ch05-Ch10 -- NLM summary only |

Existing templates to reuse (read, do not summarise):
- `/Users/apple/DailyHoroscope-Migration/KE_Longevity_Decode_Guide.md` -- master template
- `/Users/apple/DailyHoroscope-Migration/KE_NewBook_Thread_Start_Template.md`
- `/Users/apple/DailyHoroscope-Migration/KE_Book_Decode_Process_Technical.md`

---

## RECON FINDINGS -- In-Flight Books (read before authoring guides)

The following books are already partially or fully decoded. Account 2 must incorporate these statuses into the Master Decode Plan (Task D) and author the BPHS Vol 2 guide (Task E).

### LongevityUnnatural -- ✅ COMPLETE

All 4 sections decoded. 44 rules total across:

| Section | File | Rules | Status |
|---|---|---|---|
| S1 -- Fundamental Rules | `LU_S01_FundamentalRules_Rules.json` | 10 | ✅ Done |
| S2 -- House/Planet Significations | `LU_S02_HousePlanetSignifications_Rules.json` | 7 | ✅ Done |
| S3 -- Node Significations | `LU_S03_NodeSignifications_Rules.json` | 6 | ✅ Done |
| S4 -- Badhaka/Maraka | `LU_S04_BadhakaMaraka_Rules.json` | 21 | ✅ Done |
| CS1 -- Lincoln (benchmark) | `LU_CS1_LincolnBenchmark_Rules.json` | 0 | ✅ Correct |
| CS2 -- Gandhi (benchmark) | `LU_CS2_GandhiBenchmark_Rules.json` | 0 | ✅ Correct |

Decode guide: `/Users/apple/Documents/Knowledge Engine_eBooks/LongevityUnnatural_CC_Decode/KE_LongevityUnnatural_Decode_Guide.md`
Output folder: `/Users/apple/Documents/Knowledge Engine_eBooks/LongevityUnnatural_CC_Decode/`
**No further decode work needed.** Record in Master Plan as COMPLETE. Note: `1. Some Fundamental Rules_*` files in same folder are an earlier draft -- superseded by LU_S01 set.

---

### BPHS Vol 2 -- ⏳ NLM DONE, JSON PENDING

3 chapters in scope. NotebookLM decodes already done as `.md` files. JSON conversion not yet done.

| Chapter | Source PDF | NLM Output (exists) | JSON (pending) |
|---|---|---|---|
| Ch49 | `BPHS - 2 RSanthanam_Ch49.pdf` | `BPHS Ch49 Decode_Vol 2_JSON_NoteBookLM.md` | ❌ Not done |
| Ch50 | `BPHS - 2 RSanthanam-Ch50.pdf` | `BPHS_Ch50_Decode_Vol 2_JSON_Notebook LM.md` | ❌ Not done |
| Ch51 | `BPHS - 2 RSanthanam_ch51.pdf` | `BPHS_Ch51_Decode_Vol 2_JSON_NotebookLM.md` | ❌ Not done |

Source folder: `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS Vol 2 Decode/`
Output folder (to create): `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/`
**Task E below covers this.** The NLM `.md` files are the input -- do NOT re-run NLM, just convert to JSON.

---

### Longevity KP (CC_Decode) -- 🔒 BLOCKED

Status: Ch06-Ch19 decoded as `.md` files (13 chapters). Held pending aayu bucket methodology sign-off by co-founder.
Output folder: `/Users/apple/Documents/Knowledge Engine_eBooks/Longevity_CC_Decode/`
**Do NOT add to active queue.** Record in Master Plan as BLOCKED. No work until CC1 confirms approval.

---

## MANDATORY FIRST ACTION

Write tool -- create 5 files now:

```
1. /Users/apple/DailyHoroscope-Migration/KE_NewBooks_Plan/BPHS_Vol1_Decode_Guide.md            → "# BPHS Vol1 Decode Guide\n\n[Writing in progress]"
2. /Users/apple/DailyHoroscope-Migration/KE_NewBooks_Plan/KP_Astrology_Decode_Guide.md         → "# KP Astrology Decode Guide\n\n[Writing in progress]"
3. /Users/apple/DailyHoroscope-Migration/KE_NewBooks_Plan/Phaladeepika_Decode_Guide.md         → "# Phaladeepika Decode Guide\n\n[Writing in progress]"
4. /Users/apple/DailyHoroscope-Migration/KE_NewBooks_Plan/BPHS_Vol2_JSON_Conversion_Guide.md   → "# BPHS Vol2 JSON Conversion Guide\n\n[Writing in progress]"
5. /Users/apple/DailyHoroscope-Migration/KE_NewBooks_Plan/MASTER_DECODE_PLAN.md                → "# Master Decode Plan\n\n[Writing in progress]"
```

Post ONE line: "5 guide files created. Starting Task A."

---

## TASK A -- BPHS Vol 1 Decode Guide

Write to: `BPHS_Vol1_Decode_Guide.md`
Model: `KE_Longevity_Decode_Guide.md` -- copy the full structure, adapt for BPHS.

**Key adaptations from the Longevity guide:**

**1. Mandatory First Action block** -- adapt to BPHS Thread A first chapter:
- Output folder: `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/`
- First files: `BPHS_Ch11_JudgementHouses_Rules.json`, `_DataTables.md`, `_Summary.md`, `_Diagnostic.md`

**2. Chapter Start Protocol** -- same 5-step pattern from Longevity guide, adapted:
- Step 1: Write 4 output files (+ 1 Contradictions file for Ch11-Ch24)
- Step 2: Post one line confirmation
- Step 3: Read chapter PDF from `/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/BPHS_Vol1/`
- Step 4: Decode → write all files
- Step 5: Post one line completion

**3. Thread chapter maps -- include all 3 threads:**

```
THREAD A (issue first): Ch11, Ch12, Ch13, Ch14, Ch15, Ch16, Ch17, Ch18, Ch19, Ch20, Ch21, Ch22, Ch23, Ch24
THREAD B: Ch25, Ch26, Ch28, Ch29, Ch30, Ch31, Ch32, Ch33, Ch35, Ch36
THREAD C: Ch37, Ch38, Ch39, Ch42, Ch45
LOW PRI (NLM only -- no CC thread): Ch01, Ch02, Ch05, Ch06, Ch07, Ch08, Ch09, Ch10
SKIP (already decoded): Ch27 ✅ Ch34 ✅ Ch40 ✅ Ch41 ✅ Ch43 ✅ Ch44 ✅
```

**4. House Chapter Special Protocol (Ch11-Ch24 only) -- add this section:**

Standard 4 files + 1 additional:

**File 5 -- Contradictions.json:**
When the same condition appears in two shlokas with opposite outcomes, log:
```json
{
  "contradiction_id": "BPHS_Ch12_C01",
  "chapter": 12,
  "condition": "Sun in 1st house",
  "rule_a_shloka": "12.x",
  "outcome_a": "...",
  "rule_b_shloka": "12.y",
  "outcome_b": "...",
  "resolution": "context_dependent|strength_dependent|unresolved"
}
```

**TBA Rules (new rules not yet captured):**
After standard decode, re-read and flag rules missing a clean trigger condition.
Tag: `"approval_status": "tba_needs_trigger"` in JSON.
Do not skip -- placeholder rules preserve the reference.

**5. JSON Schema for BPHS** -- add these fields beyond the base schema:
```json
{
  "science_id": "bphs_vol1",
  "chapter": 12,
  "shloka_ref": "12.14",
  "planet": "Sun",
  "house": 1,
  "condition": "Sun placed in Lagna",
  "outcome": "...",
  "outcome_type": "positive|negative|neutral|conditional",
  "contradiction_flag": false,
  "approval_status": "pending_human_review"
}
```

**6. NLM chapters (Ch01-Ch10):**
These go through NotebookLM only. Include the NLM prompt:
```
NOTEBOOKLM PROMPT -- BPHS SUMMARY CHAPTER:
Extract from this chapter:
1. Any planetary/house rules in format: [Condition] → [Outcome]
2. Data tables (planetary natures, sign characteristics)
3. Flag any rule that contradicts standard Parashari doctrine
Output format: numbered list of rules, plain text, ready for JSON conversion.
Do NOT summarise narrative. Rules only.
```

Post ONE line: "Task A complete -- BPHS_Vol1_Decode_Guide.md written."

---

## TASK B -- KP Astrology Decode Guide

Book confirmed (from D. New Books Plan): **Prof K.S. Krishnamurty Vol 3**
`/Users/apple/Documents/Knowledge Engine_eBooks/KP Astology Text Books/03-predictive-stellar-astrology-3-kp-system-by-prof-k-s-krishnamurty-good-quality.pdf`

Write to: `KP_Astrology_Decode_Guide.md`

**Architecture (user-confirmed):**
- NotebookLM → Summary.md + DataTables.md per chapter (~25% token saving)
- CC → Rules.json + Diagnostic.md only

**Guide must include:**

**1. Mandatory First Action block:**
- Output folder: `/Users/apple/Documents/Knowledge Engine_eBooks/KP_CC_Decode/`
- Note: You (user) will pre-split the PDF into individual chapters before issuing the thread

**2. NotebookLM prompt for KP:**
```
NOTEBOOKLM PROMPT -- KP CHAPTER DECODE:
Book: KP Astrology (Krishnamurty). Chapter: [X].
Extract ONLY:
1. Significator rules: [Planet] as significator of [House] → [Outcome]
2. Sub-lord rules: Sub-lord of [cusp] in [sign/house] → [Result]
3. Any house + planet combination rules
4. Tables: sub-lord tables, significator lists (plain text)
5. Flag any rule contradicting standard Krishnamurty doctrine
Output: numbered list, plain text. No narrative. Ready for CC JSON conversion.
```

**3. KP JSON Schema -- add KP-specific fields:**
```json
{
  "science_id": "kp_astrology",
  "chapter": 3,
  "significator_planet": "Venus",
  "cusp": 7,
  "sub_lord": "Mercury",
  "condition": "Sub-lord of 7th cusp is Mercury in 6th house",
  "outcome": "...",
  "kp_principle": "sub_lord|significator|ruling_planet",
  "contradiction_flag": false,
  "approval_status": "pending_human_review"
}
```

**4. Dedup note -- include in guide:**
KP rules will overlap with 300 Horoscopes decode (same system).
During decode: keep `/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredHoroscopes_CC_Decode/` open.
Flag any KP rule already captured there -- tag `"duplicate_candidate": true`.

**5. Chapter Start Protocol** -- same 5-step pattern, adapted for NLM handoff:
- Step 1: Write 3 output files (Rules.json, Diagnostic.md, NLM_Input_Notes.md)
- Step 2: User runs NLM → pastes output into CC thread
- Step 3: CC converts NLM output to JSON
- Step 4: CC writes Rules.json + Diagnostic.md
- Step 5: One line confirmation

Post ONE line: "Task B complete -- KP_Astrology_Decode_Guide.md written."

---

## TASK C -- Phaladeepika Decode Guide

Book confirmed: `/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika/phaladeepika.pdf`
Strategy (from D. New Books Plan): Decode AFTER BPHS Vol 1. Same NLM + CC split.

Write to: `Phaladeepika_Decode_Guide.md`

**Guide must include:**

**1. Mandatory First Action block:**
- Output folder: `/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode/`
- Note: PDF not yet split -- user splits chapters as prep before thread starts

**2. Overlap handling:**
Phaladeepika is Parashari -- heavy overlap with BPHS Vol 1 expected.
During decode: compare against BPHS rules already in `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/`.
Tag overlapping rules: `"duplicate_candidate": true, "duplicate_source": "bphs_vol1"`.
For Phaladeepika-unique rules or contradictions with BPHS -- capture fully.

**3. JSON Schema** -- same as BPHS with:
```json
{ "science_id": "phaladeepika", "duplicate_candidate": false, "duplicate_source": null }
```

**4. NLM prompt** -- same pattern as KP, adapted:
```
NOTEBOOKLM PROMPT -- PHALADEEPIKA CHAPTER:
Classic Parashari text. Extract: [Planet] in [House] → [Outcome] rules.
Flag overlap with BPHS -- note chapter reference if recognisable.
Output: numbered rules only, no narrative.
```

**5. Chapter Start Protocol** -- same 5-step NLM handoff pattern as KP.

Post ONE line: "Task C complete -- Phaladeepika_Decode_Guide.md written."

---

## TASK D -- Master Decode Plan

Write to: `MASTER_DECODE_PLAN.md`

```markdown
# Master Decode Plan -- New Books
> Updated: 2026-05-26

## Full Decode Queue (All Books)

| Priority | Book | Thread | Scope | Status | Guide |
|---|---|---|---|---|---|
| 🔴 1 | BPHS Vol 1 | Thread A | Ch11-Ch24 (14 chs) | PENDING | BPHS_Vol1_Decode_Guide.md |
| 🟠 2 | BPHS Vol 2 | Thread F | Ch49-Ch51 (JSON conversion only) | NLM DONE -- JSON pending | BPHS_Vol2_JSON_Conversion_Guide.md |
| 🟠 2 | BPHS Vol 1 | Thread B | Ch25,26,28-33,35,36 (10 chs) | PENDING | BPHS_Vol1_Decode_Guide.md |
| 🟡 3 | BPHS Vol 1 | Thread C | Ch37-39,42,45 (5 chs) | PENDING | BPHS_Vol1_Decode_Guide.md |
| 🟡 3 | KP Astrology | Thread D | All chapters (user splits) | PENDING | KP_Astrology_Decode_Guide.md |
| ⬇️ 4 | Phaladeepika | Thread E | All chapters (user splits) | PENDING -- after BPHS Vol 1 | Phaladeepika_Decode_Guide.md |
| ⬇️ Low | BPHS Vol 1 | NLM only | Ch01,02,05-10 | NLM only -- no CC thread | BPHS_Vol1_Decode_Guide.md |
| ✅ Done | BPHS Vol 1 | -- | Ch27,34,40,41,43,44 | COMPLETE | -- |
| ✅ Done | Longevity (KP) -- Unnatural Death | -- | S1-S4 + 2 benchmarks | COMPLETE -- 44 rules | KE_LongevityUnnatural_Decode_Guide.md |
| 🔒 Blocked | Longevity (KP) -- Astro System | -- | Ch06-Ch19 (13 chs as .md) | BLOCKED -- awaiting aayu bucket approval | -- |

## Output Folders
- BPHS Vol 1: `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/`
- BPHS Vol 2: `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/` (create on first write)
- KP Astrology: `/Users/apple/Documents/Knowledge Engine_eBooks/KP_CC_Decode/`
- Phaladeepika: `/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode/`
- LongevityUnnatural: `/Users/apple/Documents/Knowledge Engine_eBooks/LongevityUnnatural_CC_Decode/` ✅
- Longevity Astro System: `/Users/apple/Documents/Knowledge Engine_eBooks/Longevity_CC_Decode/` (blocked)

## Thread Start Template
`/Users/apple/DailyHoroscope-Migration/KE_NewBook_Thread_Start_Template.md`

## User Pre-Prep Required Before Each Thread
- BPHS Thread A: Source PDFs ready ✅ (Ch11-Ch24 in BPHS_Vol1 folder)
- BPHS Vol 2 Thread F: NLM .md files ready ✅ -- no user prep needed
- KP Thread: User splits PDF into chapters first
- Phaladeepika Thread: User splits PDF into chapters first

## CC1 Confirmation Needed Before Issuing Threads
- [ ] BPHS Vol 1 guide approved → issue Thread A immediately
- [ ] BPHS Vol 2 guide approved → issue Thread F (short task -- 3 chapters, JSON only)
- [ ] KP book split ready → issue Thread D
- [ ] Phaladeepika split ready → issue Thread E (after Thread A completes)
- [ ] Longevity Astro System: DO NOT issue -- blocked. CC1 must confirm aayu approval first.
```

Post ONE line: "Task D complete. All 5 guides written. Ready for CC1 review."

---

## TASK E -- BPHS Vol 2 JSON Conversion Guide

Write to: `BPHS_Vol2_JSON_Conversion_Guide.md`
This is NOT a full decode guide -- NLM has already produced `.md` outputs for all 3 chapters.
The CC thread only needs to convert those `.md` files into Rules.json.

**Source files (already exist -- do NOT re-run NLM):**
```
/Users/apple/Documents/Knowledge Engine_eBooks/BPHS Vol 2 Decode/BPHS Ch49 Decode_Vol 2_JSON_NoteBookLM.md
/Users/apple/Documents/Knowledge Engine_eBooks/BPHS Vol 2 Decode/BPHS_Ch50_Decode_Vol 2_JSON_Notebook LM.md
/Users/apple/Documents/Knowledge Engine_eBooks/BPHS Vol 2 Decode/BPHS_Ch51_Decode_Vol 2_JSON_NotebookLM.md
```

**Output folder (CC thread creates this):** `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/`

**Guide must include:**

**1. Mandatory First Action block (same pattern as other guides):**
- Create output folder files for Ch49 first: `BPHS_Vol2_Ch49_Rules.json`, `_Diagnostic.md`, `_Summary.md`
- Post one line confirmation before reading anything

**2. Chapter conversion protocol (3 steps only -- simpler than full decode):**
```
Step 1: Read NLM .md file for the chapter
Step 2: Convert each extracted rule → full JSON schema (L1 schema, all 22+ fields)
Step 3: Write Rules.json + Diagnostic.md. Post one line summary.
```

**3. JSON schema** -- same full L1 schema from the Learnings section above:
- `science_id`: `"bphs_vol2"`
- `checkable`: `true`
- `book_id`: `"bphs_vol2_20260526"`
- Chapter source from NLM file header

**4. Dedup note:**
BPHS Vol 2 chapters (Ch49-51) cover late topics (special lagnas, sub-period effects).
Flag any rule that overlaps with BPHS Vol 1 already decoded chapters.
Tag: `"duplicate_candidate": true, "duplicate_source": "bphs_vol1"`

**5. What to do with NLM tables vs rules:**
- NLM may have included lookup tables (planetary data, dignity tables) → `DataTables.md` only, not rules
- NLM rules in format "[Condition] → [Outcome]" → convert to full JSON rule
- NLM narrative paragraphs → Summary.md only

**6. Rule count expectation:**
NLM output quality for these 3 chapters is unknown. After converting, if total rules < 15 per chapter:
- Post a flag in Diagnostic: "LOW YIELD -- re-read NLM output, check if rules were listed as narrative"
- Do not silently under-extract

Post ONE line: "Task E complete -- BPHS_Vol2_JSON_Conversion_Guide.md written."

---

## COMPLETION

Post: "PLANNING COMPLETE. 5 guide files in /Users/apple/DailyHoroscope-Migration/KE_NewBooks_Plan/. Awaiting CC1 confirmation to issue Thread A (BPHS Vol 1) and Thread F (BPHS Vol 2 JSON conversion)."

Do NOT begin decoding. Do NOT read full chapter PDFs. Guide authoring only.
