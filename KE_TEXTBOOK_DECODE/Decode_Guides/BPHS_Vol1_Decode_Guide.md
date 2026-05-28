# BPHS Vol 1 -- CC Decode Guide (Thread A: Ch11-Ch24)

> **Single authoritative reference for this thread. Read fully before decoding.**
> This thread covers Thread A only: Ch11-Ch24 (House Effects + Bhava Lords).
> Operate autonomously chapter by chapter. No toggling to parent session required.
> Last updated: 2026-05-26

---

## 🔴 MANDATORY FIRST ACTION -- Do this NOW, before reading anything else

Create the output folder anchor file:

| # | File path | Initial content |
|---|---|---|
| 1 | `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/BPHS_Vol1_ThreadStart.md` | `# BPHS Vol1 Thread A\n\nStarted: [date]. Awaiting Phase 0 + user confirmation before Ch11 decode begins.` |

Then post this one line in the context window:
> "Output folder anchored. Reading guide and chapter PDFs for Phase 0."

**Do not create any chapter Rules.json or output files yet. Those are created chapter by chapter inside the Chapter Start Protocol, after Phase 0 is confirmed by the user.**

---

## PHASE 0 -- Fresh Eyes Assessment

**The chapter PDFs for Thread A (Ch11-Ch24) are pre-split and available in the source folder. Before creating any decode files or extracting any rules, read this guide fully, then read through the chapter PDFs and answer these questions from what you find in the actual text.**

Write your answers to:
`/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/BPHS_Vol1_ThreadA_FreshEyes.md`

Answer each point in 2-5 lines. Be specific -- name chapters and shlokas where relevant.

---

**1. Schema gaps**
Does this book contain condition types, rule structures, or content categories that are NOT covered by the schema in Part 3 of this guide? (e.g., conditional rules with multiple triggers, rules involving planetary strength thresholds, rules that only apply to specific Lagnas)

**2. Content surprises**
Did any chapters contain unexpected content -- sections that look like rules but aren't, or content types the guide doesn't account for? (e.g., lengthy exceptions, interpolated commentary by the translator, contradictory shlokas in the same verse block)

**3. Dimension coverage gaps**
The guide targets 9 dimensions per planet-in-house (appearance, health, personality, career, wealth, relationships, children, spiritual, enemies). Did you notice this book addresses dimensions not in that list? Or consistently omits some?

**4. Rule density signals**
Which chapters in Thread A look denser or thinner than the 40-80 rule target? Call out any that look like they will go well above or well below that range.

**5. Contradiction density**
BPHS is known for internal contradictions. Did you observe any chapters where contradictions are especially frequent? Any chapters that appear to have been interpolated (later additions that conflict with earlier shlokas)?

**6. Recommended decode sequence**
The default sequence is Ch11 → Ch12 → Ch13 → ... → Ch24 (numerical order). Based on reading the chapter PDFs:
- Does any chapter need to be decoded before another for context to make sense?
- Are any chapters unusually short or thin (could be batched quickly)?
- Are any chapters dense enough to warrant decoding before adjacent ones (e.g., Ch24 Bhava Lords is 144+ rules -- should it be last within Thread A)?

Write your recommended numbered sequence for Thread A. If numerical order is fine, confirm that explicitly.

**7. Guide gaps**
Anything in this guide that is unclear, missing, or conflicts with what you actually see in the chapters?

---

After writing the file, post one line:
> `"Fresh Eyes written -- [N] flags raised. Recommended sequence in file. Awaiting your confirmation of sequence + go-ahead to begin decode."`

**Do not begin decode until user confirms the sequence. Chapter 11 output files are created inside the Chapter Start Protocol -- not before.**

---

## ⚠️ OUTPUT METHOD -- Absolute Rule

**ALL decoded content goes into files via the Write tool. Zero exceptions.**
**The context window receives one-line status updates only -- nothing more.**
**Every chapter (Ch11-Ch23) produces exactly 5 output files. Ch24 produces 4 files (no Contradictions.json).**
**JSON rules are written in batches of ≤25 rules per Write call. Large chapters use Part files.**
**Reason: attempting to write 40+ rules in one pass hits the 32,000 token output limit and crashes the thread.**
**Output folder:** `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/`
**File naming:** `BPHS_Ch{NN}_{ShortTitle}_{Type}.json/.md`

---

## Chapter Start Protocol -- Execute at the start of EVERY chapter

### Step 1 -- Create all output files (Write tool × 5 for Ch11-Ch23, × 4 for Ch24)

Before reading the PDF, create placeholder files:
- `BPHS_Ch{NN}_{ShortTitle}_Rules.json` → `[]`
- `BPHS_Ch{NN}_{ShortTitle}_DataTables.md` → `# Ch{NN} Data Tables\n\n[Writing in progress]`
- `BPHS_Ch{NN}_{ShortTitle}_Summary.md` → `# Ch{NN} Technical Summary\n\n[Writing in progress]`
- `BPHS_Ch{NN}_{ShortTitle}_Diagnostic.md` → `# Ch{NN} Diagnostic\n\n[Writing in progress]`
- `BPHS_Ch{NN}_{ShortTitle}_Contradictions.json` → `[]` (**Ch11-Ch23 only**)

### Step 2 -- Context window: one line only
> `"5 files created for Ch[NN]. Beginning decode."`

### Step 3 -- Read the PDF fully before writing any content

Read the complete chapter PDF. Identify:
- Total distinct logical statements (rule count estimate)
- Which sections are rules vs. lookup tables vs. narrative
- Any contradictions (same condition, opposite outcome in different shlokas)
- Missing trigger conditions (TBA rules)

### Step 4 -- Classify and write DataTables file (single Write call)

**Before writing, apply the Table Handling Protocol below to every table, chart, or diagram you found in the chapter.**

### Step 5 -- Write JSON Rules file (batched -- CRITICAL)

**⚠️ NEVER write more than 25 rules in a single Write tool call.**

- **Small chapters (≤25 rules):** Write the complete JSON array in one call
- **Large chapters (>25 rules):** Write in Part files:
  - Part 1 → `BPHS_Ch{NN}_{ShortTitle}_Rules_Part1.json` (rules 001-025)
  - Part 2 → `BPHS_Ch{NN}_{ShortTitle}_Rules_Part2.json` (rules 026-050)
  - Continue until all rules are written

### Step 6 -- Write Contradictions.json (Ch11-Ch23 only)

### Step 7 -- Write Summary file (≤10 lines)

### Step 8 -- Write Diagnostic file

### Step 9 -- Context window: one line only
> `"Ch[NN] complete. [N] rules across [N] part files. [N] contradictions. Proceeding to Ch[NN+1]."`

**Nothing else goes in the context window. Ever.**

---

## Table & Chart Handling Protocol

When a chapter contains tables, charts, or diagrams, classify each one before extracting:

| Content type | What it looks like | Action |
|---|---|---|
| **Rule-dense table** | Grid where each row/cell states a planet, house/condition, and an outcome (e.g., Sun in 1st → bold personality) | Extract each non-empty cell as a **separate JSON rule**. A 9×3 table = up to 27 rules -- do not compress into one |
| **Reference / lookup table** | Dignity tables, planetary nature lists, Nakshatra lists, sign quality data | → `DataTables.md` only. Not rules |
| **Calculation procedure table** | Step-by-step computation with inputs and outputs | → `engine_specification` rule if it defines Parashari methodology; `DataTables.md` if pure reference |
| **Visual chart / diagram** | Rasi wheel, house diagram, dasha timeline visual | → Note existence in Diagnostic only: "Chapter contains [type] -- visual content, not extractable as rules." Zero rule extraction |

**The test:** Does each row or cell state a condition **and** an outcome? Yes → rules. No → `DataTables.md`.

**DataTables.md format:** Write each lookup table as a Markdown table. Include:
- The table title or heading from the PDF
- Page or shloka reference if visible
- Complete table data in `| col1 | col2 |` format

Do NOT convert DataTables content into JSON rules.

---

## PART 1 -- Project Identity

| Field | Value |
|---|---|
| Book | Brihat Parashara Hora Shastra (BPHS) Vol 1 -- R. Santhanam translation |
| `book_id` | `bphs_vol1_20260526` |
| `science_id` | `vedic_astrology` |
| `checkable` | `true` |
| Astrological system | Classical Parashari Vedic Astrology |
| Target collection | MongoDB: `interpretation_rules` |
| PDF source folder | `/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/BPHS_Vol1/` |
| Output folder | `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/` |
| Decode method | CC Direct -- read PDF, produce all 5 output files |
| Rule ID prefix | `bphs1-ch{NN}-{NNN}` |
| Related books | Phaladeepika (same Parashari tradition -- flag overlaps as `duplicate_candidate: true`) |

### This Thread's Scope

| Thread | Chapters | Priority | Content |
|---|---|---|---|
| **A -- THIS THREAD** | **Ch11-Ch24** | **🔴 HIGHEST** | **House Effects + Bhava Lords** |
| B (future thread) | Ch25,26,28-33,35,36 | 🟠 | Strengths, Yogas, Karakatwa |
| C (future thread) | Ch37-39,42,45 | 🟡 | Raja Yogas, Longevity, Maraka |
| Already decoded -- SKIP | Ch27,34,40,41,43,44 | ✅ | Complete |

**Do not decode chapters outside Thread A. Do not attempt Thread B or C chapters.**

---

## PART 2 -- Vedic System Primer (Context for Rule Extraction)

Before decoding, understand these Parashari fundamentals:

**Houses (Bhavas):** 12 houses numbered from the Ascendant (Lagna = 1st house).
- **Kendras (Angular):** 1, 4, 7, 10 -- strongest placement
- **Trikonas (Trines):** 1, 5, 9 -- most auspicious
- **Dusthanas (Malefic):** 6, 8, 12 -- generally harmful
- **Upachayas (Growing):** 3, 6, 10, 11 -- improve over time

**Planets (Grahas):** Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu
- **Natural Benefics:** Jupiter, Venus, Mercury (waxing), Moon (waxing)
- **Natural Malefics:** Sun, Mars, Saturn, Rahu, Ketu, Mercury (waning), Moon (waning)

**Functional benefic/malefic** depends on house lordship for the specific Lagna -- BPHS house chapters use natural classification unless a specific Lagna is mentioned.

**Shloka references:** BPHS uses numbered shlokas (verses). Format `{chapter}.{shloka_number}` -- e.g., `12.14`. Capture these in the `sloka` field.

**Bhava Lord (house lord):** The planet that rules the zodiac sign occupying that house cusp.

**Ch24 (Bhava Lords):** 12 lords × 12 possible house placements = 144+ rules. Dense chapter. Use Part files.

---

## PART 3 -- Full KE Schema

Every rule is a MongoDB document. Complete schema:

```json
{
  "rule_id": "bphs1-ch12-001",
  "science_id": "vedic_astrology",
  "active": true,
  "approval_status": "pending_human_review",
  "checkable": true,
  "source": {
    "book": "BPHS Vol 1",
    "book_id": "bphs_vol1_20260526",
    "chapter": 12,
    "chapter_name": "Effects of the First House",
    "sloka": "12.14",
    "batch_id": "bphs1-ch12-v1-20260526",
    "passage_ref_id": null
  },
  "title": "Sun in Lagna -- Commanding Personality",
  "summary": "Sun in the 1st house gives leadership, authority, and robust constitution.",
  "full_text": "When the Sun occupies the Ascendant, the native has a commanding presence, natural authority, and strong physical constitution. Eyes and heart may require attention over time.",
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

### Field-by-Field Rules

**`rule_id`**
Format: `bphs1-ch{NN}-{NNN}` -- chapter zero-padded to 2 digits, sequence zero-padded to 3.
Example: `bphs1-ch12-001`, `bphs1-ch12-002`.

**`science_id`**
Always `"vedic_astrology"`. Never `"kp_jyotish"` or `"bphs_vol1"`.

**`approval_status`**
Always `"pending_human_review"`. Exception: rules missing a clean trigger condition → `"tba_needs_trigger"`. Never set `"approved"` during decode.

**`checkable`**
Always `true` for BPHS -- the engine can verify Parashari rules against birth charts.

**`source` block -- all 7 fields required:**
- `book`: "BPHS Vol 1"
- `book_id`: "bphs_vol1_20260526"
- `chapter`: integer
- `chapter_name`: exact title from PDF header
- `sloka`: `"12.14"` format -- or `null` if chapter has no numbered verses
- `batch_id`: `"bphs1-ch{NN}-v1-20260526"`
- `passage_ref_id`: `null`

**`condition.type` valid values:**
- `"planet_in_house"` -- most Ch11-Ch23 rules (planet placed in a specific house)
- `"house_lord_placement"` -- Ch24 rules (lord of house X placed in house Y)
- `"yoga_combination"` -- multiple planets forming a named combination
- `"planet_conjunction"` -- two or more planets in the same house
- `"planet_in_sign"` -- planet in a specific zodiac sign
- `"planet_affliction"` -- planet aspected or conjoined by a malefic
- `"planet_combust"` -- planet within combustion range of Sun

**`claim_axis` valid values:**
`health_vitality`, `career_growth`, `financial_security`, `partnership_stability`, `marriage_timing`, `spirituality`, `family_life`, `longevity`, `accident_risk`, `travel`, `creativity`, `social_network`, `general`

**`claim_scope`:**
- `"natal_trait"` -- characteristic present from birth (most BPHS rules)
- `"event_timing"` -- fires at a specific dasha/transit
- `"engine_specification"` -- defines how the system works

**`claim_polarity`:**
- `"positive"` -- auspicious, beneficial outcome
- `"negative"` -- inauspicious, harmful outcome
- `"neutral"` -- factual/descriptive, no polarity
- `"conditional"` -- depends on other chart factors

**`timing_bias`:**
- `"sustained"` -- always active from birth (use for natal traits)
- `"early"` / `"mid"` / `"late"` -- if text specifies a life phase

**`strength_band`:** `"extreme"` / `"high"` / `"medium"` / `"low"` -- words only, no numbers.

**`subject_scope`:**
- `"self"` -- affects the native
- `"spouse"` -- affects the partner
- `"children"` -- affects offspring
- `"father"` -- affects father
- `"mother"` -- affects mother

**`contradiction_flag`:**
`true` if this rule contradicts another rule in the same chapter on the same condition. Also log in Contradictions.json.

**`duplicate_candidate`:**
`true` if this rule substantially overlaps with an existing decoded book (Phaladeepika especially).
Set `"duplicate_source": "phaladeepika"` (or relevant book).

---

## PART 4 -- Multi-Dimension Extraction (CRITICAL)

**This is the most important instruction for house chapters.**

For each planet-in-house combination, the text may address multiple distinct life dimensions. Each dimension = a **separate rule**. Do NOT merge them.

| Dimension | Example tag | claim_axis |
|---|---|---|
| Physical appearance / body | `appearance` | `health_vitality` |
| Health tendencies / ailments | `health` | `health_vitality` |
| Personality / character | `personality` | `general` |
| Career / professional life | `career` | `career_growth` |
| Wealth / finances | `wealth` | `financial_security` |
| Relationships / spouse | `relationships` | `partnership_stability` |
| Children | `children` | `family_life` |
| Spiritual / dharmic | `spiritual` | `spirituality` |
| Enemies / adversaries | `enemies` | `social_network` |

**Rule count target per house chapter: 40-80 rules.**
(9 planets × ~5 dimensions average = 45 minimum; some planets address 8+ dimensions.)

**If actual count falls more than 30% below 40 (i.e., below 28 rules):** Post a flag line in context before closing the chapter. Do not silently under-extract. Re-read the chapter.

---

## PART 5 -- Contradictions.json Format (Ch11-Ch23)

When two shlokas in the same chapter assign opposite outcomes to the same condition, log both in Contradictions.json and set `contradiction_flag: true` on both rules.

```json
{
  "contradiction_id": "BPHS_Ch12_C01",
  "chapter": 12,
  "condition": "Sun in 1st house",
  "rule_a_shloka": "12.7",
  "outcome_a": "Robust health and strong constitution",
  "rule_b_shloka": "12.22",
  "outcome_b": "Weak eyesight and heat-related ailments",
  "resolution": "context_dependent"
}
```

**`resolution` values:**
- `"context_dependent"` -- both rules valid, fires based on chart context (strength, aspect, etc.)
- `"strength_dependent"` -- strong planet gives A, weak planet gives B
- `"unresolved"` -- text does not clarify, flag for human review

**BPHS is known for internal contradictions**, especially around house effects, longevity, and Rahu/Ketu. Do not suppress -- capture and flag.

---

## PART 6 -- TBA Rules (Missing Trigger Conditions)

After completing each chapter's main decode pass, re-read and identify any rules where:
- The outcome is stated clearly but the trigger condition is ambiguous or missing
- The rule is conditional on a factor the text doesn't fully specify

For these rules:
- Set `"approval_status": "tba_needs_trigger"`
- Fill in the outcome you can extract; leave `condition` fields that are unknown as `null`
- Add tag: `"tba_trigger"`
- Log in Diagnostic under "TBA Rules" section

Do NOT skip TBA rules -- they preserve the reference for future clarification.

---

## PART 7 -- Chapter Map (Thread A)

| Ch | PDF filename (approx) | Content | Files | Priority |
|---|---|---|---|---|
| **Ch11** | `Ch11_*.pdf` | Judgement of Houses (general house analysis methodology) | 5 | 🔴 START HERE |
| **Ch12** | `Ch12_*.pdf` | Effects of 1st House | 5 | 🔴 |
| **Ch13** | `Ch13_*.pdf` | Effects of 2nd House | 5 | 🔴 |
| **Ch14** | `Ch14_*.pdf` | Effects of 3rd House | 5 | 🔴 |
| **Ch15** | `Ch15_*.pdf` | Effects of 4th House | 5 | 🔴 |
| **Ch16** | `Ch16_*.pdf` | Effects of 5th House | 5 | 🔴 |
| **Ch17** | `Ch17_*.pdf` | Effects of 6th House | 5 | 🔴 |
| **Ch18** | `Ch18_*.pdf` | Effects of 7th House | 5 | 🔴 |
| **Ch19** | `Ch19_*.pdf` | Effects of 8th House | 5 | 🔴 |
| **Ch20** | `Ch20_*.pdf` | Effects of 9th House | 5 | 🔴 |
| **Ch21** | `Ch21_*.pdf` | Effects of 10th House | 5 | 🔴 |
| **Ch22** | `Ch22_*.pdf` | Effects of 11th House | 5 | 🔴 |
| **Ch23** | `Ch23_*.pdf` | Effects of 12th House | 5 | 🔴 |
| **Ch24** | `Ch24_*.pdf` | Effects of Bhava Lords (12×12 = 144+ rules) | 4 | 🔴 Dense -- use Part files |

**PDFs are in:** `/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/BPHS_Vol1/`
**List the folder contents first** (Read tool on the folder) to confirm exact filenames before starting.

**Chapters to SKIP (already decoded in a prior thread):**
Ch27 ✅ Ch34 ✅ Ch40 ✅ Ch41 ✅ Ch43 ✅ Ch44 ✅ -- do not re-decode these.

---

## PART 8 -- Quality Gate Checklist

Run on every rule before finalising. Fix failures before writing the JSON file.

### Schema checks
- [ ] `rule_id` follows format `bphs1-ch{NN}-{NNN}` with correct chapter number
- [ ] `science_id` is `"vedic_astrology"`
- [ ] `active: true` present
- [ ] `approval_status` is `"pending_human_review"` (or `"tba_needs_trigger"` if trigger unknown)
- [ ] `checkable: true` present
- [ ] `source` block has all 7 fields including `sloka` and `batch_id`
- [ ] `condition` block: `type` is a valid value listed in Part 3
- [ ] `result` block has all 4 fields: `effect`, `severity`, `remedy_available`, `remedy_ref_id`
- [ ] `contradiction_flag` set correctly (true if logged in Contradictions.json)
- [ ] `duplicate_candidate` set correctly (true if same rule exists in Phaladeepika or other decoded book)

### Content checks
- [ ] Multi-dimension: each distinct life dimension is a separate rule (not merged)
- [ ] Ch24 lord placements: 12 possible house placements per lord × 12 lords = minimum 144 rules
- [ ] No numeric coefficients in `full_text` -- use intensity words only
- [ ] `claim_axis` is one of the 13 valid values
- [ ] `subject_scope` correctly identifies who is affected
- [ ] Tags include the planet name, house number, and dimension (e.g., `["sun", "1st_house", "personality"]`)
- [ ] Contradictions.json populated for any `contradiction_flag: true` rules
- [ ] TBA rules tagged `"tba_trigger"` and logged in Diagnostic

### Rule count checks
- [ ] House chapters (Ch12-Ch23): ≥40 rules -- if below, re-read before closing
- [ ] Ch11 (methodology): 10-25 rules expected
- [ ] Ch24 (Bhava Lords): ≥100 rules -- 144+ possible, flag if below 100

### Delivery checks
- [ ] Each Part file is a complete, valid JSON array `[...]`
- [ ] Rules sequential: bphs1-ch{NN}-001, 002, 003... no gaps, no duplicates
- [ ] Diagnostic includes: scope, rule count, contradictions list, TBA rules list, exclusions, open questions

---

## PART 9 -- Known Issues to Avoid

1. **Context window overflow:** The single most likely failure. NEVER write rule arrays to the context window. Write tool only. Even one rule set written to context can fill 4,000+ tokens.

2. **Merging dimensions:** The most common under-extraction error. "Sun in Lagna gives good health, wealth, and leadership" = 3 separate rules, not one.

3. **Shloka numbering:** Some BPHS translations have inconsistent shloka numbering across chapters. Use the number visible in the PDF. If no numbers, use `null` for `sloka`.

4. **Rahu/Ketu rules:** BPHS is contradictory on nodes. Capture all stated rules. If directly contradictory within the chapter, flag both with `contradiction_flag: true`.

5. **Ch24 scope:** Lord-in-house rules may span multiple paragraphs per lord. Read the entire lord's section before extracting rules for that lord.

6. **Narrative vs rule:** BPHS opens each house chapter with cosmological/mythological framing. Discard narrative, extract only the rule logic (condition → outcome).
