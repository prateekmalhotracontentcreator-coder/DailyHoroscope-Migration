# KE Book De-code Process -- Technical Reference
> Temple Team / Claude Code  
> Created: 18 May 2026  
> Purpose: Definitive briefing for any new AI thread tasked with de-coding books for the Knowledge Engine ingest pipeline.  
> Read this in full before touching a single JSON rule or PDF chapter.

---

## Part 1 -- What This Document Is

This document governs the process by which source astrology books are decoded, validated, and prepared for ingestion into the EverydayHoroscope Knowledge Engine (KE) MongoDB database.

It is written specifically to prevent repeating the mistakes made by earlier decode threads, which did not understand:
- The mandatory Dry Run gate before any live ingest
- How to use the Validator
- Which fields, field types, and naming conventions are required
- The difference between "upsert", "insert", and "ingest" (critical -- see Section 7)
- What Contradiction Pairs are and how to identify them
- The approval workflow: rules are NOT live until co-founder signs off
- The difference between `checkable: true` and `checkable: false` rules

**This document does NOT replace the KE Contract (`CODEX_KNOWLEDGE_ENGINE_CONTRACT.md`). Read both.**

---

## Part 2 -- Database and Collection Architecture

### MongoDB Collections in Scope

| Collection | Purpose | Who writes to it |
|---|---|---|
| `interpretation_rules` | All decoded book rules -- the core KE dataset | Ingest scripts only |
| `import_batches` | One document per ingest run -- tracks status, counts, approval state | Ingest scripts via `batch_ingest.py` |
| `science_registry` | One document per science system (jyotish, kp_jyotish, sbc, mundane_jyotish, etc.) | `seed_science_registry.py` |
| `geo_entities` | Geographic lookups for Mundane Astrology (Koorma Chakra, Zodiac Geography) | `ingest_mundane_geo_entities_v1.py` |
| `case_studies` | Historical validation cases -- Phase 1.2 (NOT Phase 1 rule ingest) | Separate pipeline |

**The decode thread writes only to `interpretation_rules` and `import_batches` (via the ingest script). It never writes directly to MongoDB by hand.**

---

## Part 3 -- The `interpretation_rules` Schema (Every Field)

Every rule document in `interpretation_rules` must have these fields. The new thread must populate all mandatory fields and leave optional fields as `null` (not absent).

### 3a -- Core Identity Fields

```json
{
  "rule_id": "sbc-ch04-001",
  "science_id": "sbc",
  "approval_status": "pending_human_review",
  "checkable": false,
  "active": true
}
```

| Field | Type | Rule |
|---|---|---|
| `rule_id` | string | Format: `{science_prefix}-ch{nn}-{sequence}`. Lowercase. Hyphens only. No underscores. Example: `sbc-ch04-001`, `kp-ch07-023` |
| `science_id` | string | Must match a document in `science_registry`. See Section 5 for valid values. |
| `approval_status` | string | Always `"pending_human_review"` on ingest. Never `"approved"`. |
| `checkable` | boolean | `true` only if the KE evaluation engine can compute the condition at runtime. `false` for all SBC and KP rules in Phase 1. See Section 8. |
| `active` | boolean | Always `true` on ingest. |

### 3b -- Source Provenance Fields (Required)

```json
{
  "source": {
    "book": "Sarvato Bhadra Chakra",
    "book_id": "sbc_v2_20260518",
    "chapter": 4,
    "chapter_name": "All About Stars",
    "sloka": "4.12",
    "batch_id": "sbc-ch04-v1-20260518",
    "passage_ref_id": null
  }
}
```

| Field | Rule |
|---|---|
| `book` | Full book title as it appears on cover. |
| `book_id` | Slug for the book edition. Format: `{science}_{version}_{date}`. |
| `chapter` | Integer. |
| `chapter_name` | Plain English chapter name. |
| `sloka` | Page or sloka reference from the source PDF. Format: `{chapter}.{sloka}` or `{chapter}.{page}`. `null` if not applicable. |
| `batch_id` | Unique per ingest run. Format: `{book-slug}-ch{nn}-v{n}-{YYYYMMDD}`. This is the key the idempotency check uses -- running the same batch twice will skip on the second run. |
| `passage_ref_id` | Always `null` in Phase 1. Phase 2 field for embedded passage linking. |

### 3c -- Content Fields

```json
{
  "title": "Janma Nakshatra -- Lethal Threshold at Three Malefic Vedhas",
  "summary": "When the birth star receives Vedha from three or more malefic planets simultaneously, the SBC diagnostic engine signals destruction and financial defeat for the native.",
  "full_text": "When three or more malefic planets cast their Vedha upon the Janma Nakshatra, the SBC engine raises a destruction and defeat flag. This threshold governs the intensity of adverse planetary influence on the native's birth star coordinate and is the standard marker for significant life setbacks, financial loss, and defeat in competitive endeavours.",
  "tags": ["janma_nakshatra", "vedha", "malefic_threshold", "transit_timing"],
  "category": "transit_diagnostics"
}
```

| Field | Rule |
|---|---|
| `title` | 10-15 words. Specific. Never generic like "Venus Rule" or "General Principle". |
| `summary` | 1-2 sentences. What the rule says in plain English. No Sanskrit jargon without explanation. |
| `full_text` | 2-5 sentences. Paraphrased from source -- NOT copied verbatim (copyright). Must be complete enough for Claude to use in a report without needing the original book. |
| `tags` | Array of lowercase snake_case strings. Minimum 3 tags. Use consistent vocabulary. |
| `category` | Single string. See Section 5 for valid categories per science. |

### 3d -- Condition Fields (TD-15 -- Required)

```json
{
  "condition": {
    "type": "transit_vedha",
    "planet": "saturn",
    "placement": null,
    "house": null,
    "sign": null,
    "nakshatra": "ardra",
    "strength_requirement": null,
    "dasha_lord": null,
    "antardasha_planet": null,
    "applies_to_all_dasha_lords": false
  }
}
```

**TD-15 additional fields (mandatory on every rule):**

```json
{
  "claim_axis": "health_vitality",
  "claim_scope": "event_timing",
  "claim_polarity": "negative",
  "timing_bias": "immediate",
  "strength_band": "high",
  "subject_scope": "self",
  "authority_override": null,
  "mutually_exclusive_with": [],
  "passage_ref_id": null
}
```

| TD-15 Field | Valid Values | Meaning |
|---|---|---|
| `claim_axis` | `health_vitality`, `career_growth`, `financial_security`, `partnership_stability`, `marriage_timing`, `spirituality`, `family_life`, `longevity`, `accident_risk`, `travel`, `creativity`, `social_network`, `general` | Domain this rule speaks to |
| `claim_scope` | `natal_trait`, `event_timing`, `period_quality`, `strength_assessment`, `remedy`, `engine_specification` | What kind of claim this is |
| `claim_polarity` | `positive`, `negative`, `neutral`, `conditional` | Direction of the prediction |
| `timing_bias` | `early`, `mid`, `late`, `immediate`, `sustained`, `periodic`, `null` | When in the period the effect tends to manifest |
| `strength_band` | `low`, `medium`, `high`, `extreme` | How strong the effect is stated to be |
| `subject_scope` | `self`, `spouse`, `parent`, `child`, `sibling`, `nation`, `collective` | Who the rule applies to |
| `authority_override` | `null` or string | Only set when a rule overrides contradicting rules from other sciences |
| `mutually_exclusive_with` | Array of `rule_id` strings | Rules that cannot both fire simultaneously |

### 3e -- Result Field

```json
{
  "result": {
    "effect": "Destruction and defeat; financial loss and failure in competitive endeavours.",
    "severity": "high",
    "remedy_available": false,
    "remedy_ref_id": null
  }
}
```

**Critical:** `effect` text must be qualitative only. No numeric coefficients (0.30, 1.5×, etc.). If the source book uses numbers, translate to intensity language: "significant", "moderate", "severe", "mild". Numeric weights go in the engine layer, not in interpretation rules.

---

## Part 4 -- The Two Branches of the Decode Process

### Branch A -- Full NotebookLM Triple-Doc Available

This is the preferred path. NotebookLM (NLM) has already processed the source book and produced three structured output documents:

| NLM Document | What it contains | How CC uses it |
|---|---|---|
| **Summaries doc** | Chapter-by-chapter plain English summaries of all principles | Cross-reference to verify the JSON doc captured the intent correctly; catch omissions |
| **Data Tables doc** | Structured tables of planetary correspondences, lookup tables, grid coordinates, threshold values | Source for lookup-type rules; use tables directly as rule conditions |
| **JSON Ready doc** | Draft JSON rules already structured in near-ingest format by NLM | Primary working source -- refine, validate fields, add TD-15 fields, fix condition types |

> **CRITICAL -- Branch A is refinement, NOT writing from scratch.**
> The JSON Ready doc is your starting point. NLM has already extracted the rules. Your job is to complete the NLM draft to the full schema standard -- adding all missing TD-15 fields (`claim_axis`, `claim_polarity`, `timing_bias`, `strength_band`, `subject_scope`, `mutually_exclusive_with`), correcting `condition.type` values to the correct vocabulary for this science, and cross-checking intent against the Summaries doc. Writing rules from scratch when a JSON Ready doc exists is wasted effort and a process violation. If a chapter has a JSON Ready doc, you must start from it.

**Three-document parallel read protocol:**
1. Open all three docs simultaneously in the decode session.
2. **Start from the JSON Ready doc as your working base -- do not write rules from scratch.**
3. Cross-check every rule's intent against the Summaries doc. Flag any rule in the JSON doc that is contradicted by or absent from the Summaries doc -- these are NLM extraction errors to correct.
4. Pull precise values (threshold numbers, star indices, directional codes) from the Data Tables doc.
5. Add all missing TD-15 fields to every rule.
6. Correct `condition.type` values to match the valid types for this science (see Part 5).

**Branch A books in the current pipeline:**
- Sarvato Bhadra Chakra V2 (8 NLM docs -- superset of the triple-doc)
- Lal Kitab Ch 19 Update 2 (chapter diagnostic + JSON Ready pair)
- Longevity KP -- Ch 4, 5, 15 (diagnostic + JSON Ready pairs)

### Branch B -- PDF + PDF-to-JSON Only

CC does the heavy lifting: reads the chapter PDF directly and produces the JSON rules from scratch.

**Branch B process:**
1. Read the chapter PDF carefully -- mark every rule statement (if X then Y structure).
2. Draft the rule JSON manually, populating all fields from Section 3.
3. Run through the Contradiction Check protocol (Section 6) before finalising.
4. Produce a Diagnostic doc (what you decoded, what you skipped and why) alongside the JSON.

**Branch B books:**
- Longevity KP -- chapters without NLM diagnostic (Ch 6-14 lagna chapters, Ch 15-19 method chapters)
- Any new book where NLM has not been run yet.

---

## Part 5 -- Science IDs, Category Codes, and Condition Types

### Valid `science_id` values

| science_id | Book family | Notes |
|---|---|---|
| `vedic_astrology` | BPHS, TBA (Text Book of Astrology), general Vedic | Default for classical Jyotish |
| `lal_kitab` | Lal Kitab all chapters | Already seeded |
| `mundane_jyotish` | Mundane Astrology (Gaur, Mehta, Gopalakrishnan, Raphael) | National/global events -- never mix with individual chart rules |
| `kp_jyotish` | Longevity KP system | CRITICAL -- KP uses different house division, ayanamsha, sub-lord logic. Must not be tagged as `vedic_astrology`. |
| `sbc` | Sarvato Bhadra Chakra | Grid-based transit Vedha system -- NOT natal-placement-based |
| `jyotish_remedies` | Mantra/Yantra remedies | The prescription layer |
| `jyotish_remedies_dhana` | Dhana-specific remedies | Wealth remedies subset |
| `jyotish_remedies_gemstones` | Gemstone remedies | |
| `jyotish_remedies_crystals` | Crystal remedies | |
| `jyotish_remedies_chakra` | 7 Chakra healing remedies | |

### Condition types by science

**Vedic Astrology / Lal Kitab (natal, checkable in Phase 1):**
`house_position`, `planet_in_house`, `yoga_combination`, `planet_conjunction`, `planetary_position`, `planet_affliction`, `planet_combust`, `dasha_period`, `varga_dignity_tier`, `house_placement`

**Mundane Jyotish (checkable partially, engine_specification for procedure rules):**
`mundane_transit`, `mundane_period`, `engine_specification`, `historical_validation`

**SBC (ALL `checkable: false` in Phase 1 -- no evaluator built yet):**
`transit_vedha`, `latta_kick`, `nadi_classification`, `panchaka_affliction`, `auxiliary_chakra`, `financial_market`, `geopolitical`

**KP Jyotish (ALL `checkable: false` in Phase 1 -- KP sub-lord engine not in vedic_calculator.py):**
`kp_sub_lord`, `kp_significator`, `kp_badhaka`, `kp_longevity_factor`, `kp_case_study`

---

## Part 6 -- Contradiction Detection Protocol

Before finalising any chapter's JSON, the decode thread must run a contradiction check. This is NOT optional.

### What a Contradiction is

Two rules that:
1. Have the same `claim_axis` (same life domain)
2. Have opposite `claim_polarity` (one positive, one negative)
3. Share a significant `claim_scope` and `subject_scope` overlap
4. Could fire simultaneously for the same chart configuration

### How to identify them (within a chapter batch)

Scan the rule list for any pairs where:
- `claim_polarity` differs AND
- `claim_axis` is the same AND
- The planetary/house conditions could both be true at once (e.g., both triggered by Saturn in the 7th house, but one says "partnership delays" and the other says "stable marriage")

### How to flag them

Add to the batch's Diagnostic doc:

```
CONTRADICTION PAIR FLAGGED:
Rule A: {rule_id} -- "{title}" -- polarity: negative -- condition: {summary of condition}
Rule B: {rule_id} -- "{title}" -- polarity: positive -- condition: {summary of condition}
Overlap: Both fire when [describe the shared trigger]
Resolution needed: [note which source text has stronger authority or if both are valid in different sub-conditions]
```

Do NOT attempt to resolve contradictions unilaterally. Flag them and let the Temple Team resolve via the Library Console Contradiction Browser.

### Cross-book contradictions

If a new rule contradicts a rule already in the DB from a different book:
- Set `authority_override: null` (do not pre-resolve)
- Add to the Diagnostic doc with the conflicting `rule_id` from the existing DB

---

## Part 7 -- Mandatory Terminology

Previous decode threads used inconsistent language that caused confusion in review. Use only these terms:

| Correct term | Meaning | Wrong terms to NEVER use |
|---|---|---|
| **Dry Run** | Running the ingest script with `--dry-run` flag -- validates rules, counts them, checks duplicates, but does NOT write to MongoDB | "test", "preview", "simulate" |
| **Ingest** | The act of writing validated rules to MongoDB via the ingest script after Dry Run passes | "insert", "upload", "push", "commit to DB" |
| **Upsert** | Updating an existing rule document by its `rule_id` -- used only for patches and corrections, NEVER for new content | Do not use "upsert" to mean "ingest new rules" |
| **Batch** | One ingest run = one batch. Identified by `batch_id`. Tracked in `import_batches` collection. | "set", "group", "pack" |
| **Pending Human Review** | `approval_status = "pending_human_review"` -- rule is in the DB but NOT active in the KE until co-founder approves | "drafted", "ready", "live" |
| **Approved** | `approval_status = "approved"` -- co-founder has explicitly signed off via Library Console | "verified", "validated", "accepted" |
| **Checkable** | `checkable: true` -- the KE evaluation engine can compute the condition at runtime from the user's chart data | "computable", "active", "evaluable" |
| **Decorative** | `checkable: false` -- rule is stored but the engine cannot evaluate it yet (Phase 1 placeholder) | "placeholder", "stub", "disabled" |
| **Contradiction Pair** | Two rules with opposite polarity that could fire simultaneously | "conflict", "clash", "overlap" |
| **False Flag** | A validator rejection that is incorrect -- the source text actually does support the rule | "false positive", "validator error", "wrong rejection" |

---

## Part 8 -- The Ingest Pipeline (Step by Step)

### Step 0 -- Pre-Flight Check

Before writing a single rule:
1. Confirm the `science_id` for this book exists in `science_registry`. If not, add it via `seed_science_registry.py` first.
2. Confirm the `batch_id` naming convention for this book and chapter.
3. Confirm whether this science has an evaluator in `ke_yoga_evaluator.py`. If not, all rules are `checkable: false`.
4. Check the SCRIPTS_INDEX.md -- has any version of this chapter already been ingested? If yes, the new batch is a v2 patch, not a v1 ingest.

### Step 1 -- Decode the Chapter

**Branch A:** Use the three-document parallel-read protocol (Section 4). Start from the NLM JSON Ready doc -- refine and complete it. Do NOT write rules from scratch. The NLM has already done the extraction; your job is schema completion and quality control.

**Branch B:** Read the PDF, draft rules manually.

For every rule extracted:
- Populate all fields from Section 3 (no field left absent -- use `null` for optional fields)
- Assign `claim_axis`, `claim_polarity`, `timing_bias`, `strength_band` (TD-15 fields -- mandatory)
- Set `checkable: false` for all SBC and KP rules
- Set `approval_status: "pending_human_review"` always

### Step 2 -- Produce the Diagnostic Document

A Diagnostic doc must accompany every chapter's JSON. It contains:
1. **Chapter summary** -- what the chapter covers
2. **Decode decisions** -- what was included and why; what was excluded and why
3. **Excluded content** -- list rules that were NOT decoded (e.g., commodity trading logic, horary-only rules, case-study narrative text)
4. **Contradiction pairs** -- list all flagged pairs (see Section 6)
5. **False flags encountered** -- validator rejections that were overruled with source citation
6. **Open questions** -- anything the new thread could not resolve

### Step 3 -- Validate (JSON Schema Gate)

Run the validator before the ingest script:

```bash
# For Vedic / Lal Kitab / SBC / KP rules:
python3 backend/scripts/validate_rules.py --input {your_rules.json}

# For Mundane Astrology rules ONLY:
python3 backend/scripts/validate_mundane_rules.py --input {your_rules.json}
```

**The validator checks:**
- All required fields present
- `rule_id` format is correct
- `science_id` exists in registry
- `claim_axis` is a valid value
- `claim_polarity` is one of the four valid values
- `approval_status` is `"pending_human_review"` (rejects anything else)
- No duplicate `rule_id` within the batch

**Do not proceed to Step 4 until the validator shows 0 errors.**

### Step 4 -- Dry Run

```bash
python3 backend/scripts/batch_ingest.py \
  --config {book_config.json} \
  --chapter {chapter_name} \
  --dry-run
```

The Dry Run output must show:
- `rules_candidate: N` (total extracted)
- `rules_valid: N` (passed schema check)
- `rules_duplicate: 0` (no batch_id already in DB)
- `rules_invalid: 0` (zero schema errors)

**Do not proceed to Step 5 until Dry Run shows 0 invalid and 0 duplicates.**

### Step 5 -- Live Ingest

```bash
python3 backend/scripts/batch_ingest.py \
  --config {book_config.json} \
  --chapter {chapter_name}
```

The ingest script automatically:
1. Writes all rules to `interpretation_rules` collection
2. Creates an `import_batches` document with status `"imported"`, rule counts, and timestamp
3. Returns `index_refreshed: true` if the in-memory index was updated

### Step 6 -- Post-Ingest Verification

After live ingest, confirm:
1. `import_batches` shows `import_status: "imported"` for this `batch_id`
2. Rule count in MongoDB matches the expected count from Dry Run
3. Sample 3-5 rules in Library Console Rules Browser -- verify they appear under correct `science_id`
4. All rules show `approval_status: "pending_human_review"`

### Step 7 -- Deliver to Temple Team

Deliver to CC (Claude Code in the main session) for Audit before co-founder approval:
1. The Diagnostic doc (`.md`)
2. The JSON rules file (`.json`)
3. The batch_id(s) used
4. Rule counts per chapter
5. Any open questions or flagged contradiction pairs

CC will run the Audit before clearing for co-founder review.

---

## Part 9 -- Book-Wise Decode Plan

### BOOK 1 -- Sarvato Bhadra Chakra (SBC) V2

**Branch:** A -- Full NotebookLM decode available  
**Folder:** `/Users/apple/Documents/Knowledge Engine_eBooks/New Ingest_5 Books/1. Sarvato Bhadra Chakra_V2/`  
**science_id:** `sbc`  
**All rules:** `checkable: false` (no SBC evaluator in Phase 1)  
**Ingest status:** NOT ingested -- no scripts exist

#### NLM Documents Available

| File | Role |
|---|---|
| `README_ Sarvato Bhadra Chakra (SBC) Diagnostic Engine.md` | Architecture overview -- read first |
| `Core Methodology and Preparation_ SBC Diagnostic Engine.md` | The "Laws of Physics" -- use as Summaries doc |
| `SBC_Update_Summaries_LM.md` | Chapter-by-chapter summaries -- cross-reference layer |
| `SBC_Update_Data Tables_LM.md` | Grid coordinates, Panchaka lookup tables, threshold values |
| `SBC_Update_JSON_LM.md` | Draft JSON rules -- PRIMARY working source |
| `SBC_Master Diagnostic Report.md` | Chapter-level diagnostic -- cross-reference |
| `SBC_Master Testing and Audit Plan for LLM.md` | Acceptance test cases -- use to verify completeness |
| `SBC_Ch19_Case Study_Analysis.md` | Historical case studies -- test vectors only, do NOT decode as rules |

#### Chapter Decode Scope

| Chapter | Title | Include for Rules | Notes |
|---|---|---|---|
| Ch 2 | Elementary Norms + Time Conversion | ✅ Yes | Panchaka grid basics, Tithi lookup tables |
| Ch 3 | Grid Architecture | ✅ Yes | 81-varga layout, 28-star system including Abhijit |
| Ch 4 | All About Stars | ✅ Yes | 9-star classification, Janma Nakshatra rules, lethality thresholds |
| Ch 5 | Planetary Dynamics | ✅ Yes | Tri-directional Vedha, Micro-Vedha supremacy |
| Ch 7 & 8 | Numerical Strength (Shadbala SBC) | ✅ Yes | Potency quantification -- note: SBC Shadbala ≠ BPHS Shadbala |
| Ch 9 | Vedha Vectors | ✅ Yes | Speed-based vector rules, conjunction victory rules |
| Ch 10 | Individual Diagnostics | ✅ Yes | Temporal snapshot rules, critical thresholds |
| Ch 11 | Muhurata and Horary | ⚠️ Partial | Include Muhurata rules; exclude horary (Prashna) rules |
| Ch 12 | Sickness and Death | ✅ Yes | Clinical indicators, Jupiter Safety Veto |
| Ch 13 | National Politics and War | ✅ Yes | `claim_scope: "engine_specification"` for directional affliction rules; tag `subject_scope: "nation"` |
| Ch 14 | Directional Analysis | ✅ Yes | |
| Ch 15-18 | Auxiliary Chakras (Latta, Sapta Nadi, Kurm, Kalanal) | ✅ Yes | Condition type: `auxiliary_chakra`. Each sub-system = separate category tag. |
| Ch 19 | Case Studies (Nehru, Indira Gandhi) | ❌ Exclude | Test vectors only -- deliver separately as case study records, not rules |
| Ch 20 | Financial Markets (Teji/Mandi) | ❌ Exclude | Explicitly out of scope per project decision |

#### SBC-Specific Field Rules

- `claim_axis` for transit/timing rules → `general` or the specific domain (health, career, etc.)
- `claim_axis` for grid/architecture rules → `general` with `claim_scope: "engine_specification"`
- `timing_bias` for transit rules → `immediate` (SBC predicts current transit windows)
- `subject_scope` for national/war rules → `nation`; for personal rules → `self`
- `mutually_exclusive_with` → flag Jupiter Veto rules as mutually exclusive with 5-malefic death rules

#### New condition_type values for SBC

```
transit_vedha     -- planet transiting a varga that aspects a Panchaka component
latta_kick        -- planet's Latta star coincides with native's Birth Star
nadi_classification -- current Sapta Nadi channel for the native
panchaka_affliction -- multiple Panchaka components under simultaneous malefic Vedha
auxiliary_chakra  -- Latta / Surya Kalanal / Chandra Kalanal / Sapt Salaka / Kurm Chakra checks
```

---

### BOOK 2 -- Lal Kitab Ch 19 Update 2

**Branch:** A -- Diagnostic + JSON Ready pair available  
**Folder:** `/Users/apple/Documents/Knowledge Engine_eBooks/New Ingest_5 Books/2. LaL Kitab_Notebook LM_Chapter Decode/`  
**science_id:** `lal_kitab`  
**Ingest status:** Ch 19 v1 already in DB (batch `lalkitab-ch19-v1-20260426`). This is a PATCH.

**Key distinction:** This is NOT a fresh ingest. It is an addendum to an existing batch.
- File: `Lal Kitab_Ch 19_Update 2_De-code.md` + `Lal Kitab_Chapter 19_Update_LM.md`
- Decode only rules that do NOT already exist in the Ch 19 v1 batch
- `batch_id` must be `lalkitab-ch19-v2-{date}` (not v1)
- Flag any rules that conflict with existing v1 rules as contradiction pairs

---

### BOOK 3 -- Longevity and Astro System (KP System)

**Branch:** A for decoded chapters (Ch 4, 5, 15 have NLM diagnostic + JSON Ready pairs); Branch B for remaining lagna chapters  
**Folder:** `/Users/apple/Documents/Knowledge Engine_eBooks/New Ingest_5 Books/4. Longetivity_Notebook_LM_Chapter Decode/`  
**science_id:** `kp_jyotish` -- CRITICAL. Never use `vedic_astrology` for KP rules.  
**All rules:** `checkable: false` (KP Sub-lord computation not in `vedic_calculator.py`)  
**Ingest status:** Config JSON exists (`longevity_astro_system.json`); NO ingest scripts written yet.

#### Chapter Scope

| Chapter Type | Chapters | Treatment |
|---|---|---|
| Foundation rules | Ch 4 (Basic Rules), Ch 5 (Basics of Longevity) | ✅ Rules -- decode fully |
| Lagna-specific rules | Ch 6-18 (12 lagna chapters) | ✅ Rules -- decode fully; condition type: `kp_longevity_factor` |
| Method chapters | Ch 15, 19 (Analysis Method) | ✅ Rules -- decode; condition type: `kp_significator` |
| Balarishta (infant mortality) | Ch 20-24 | ✅ Rules -- decode; `claim_axis: "longevity"`, `claim_polarity: "negative"`, `timing_bias: "early"` |
| Case studies | Ch 25-58 (all named as "Case Study_LM") | ❌ Test vectors ONLY. Do NOT decode as rules. |

#### KP-Specific Terminology Mapping

| KP Term | Maps to `condition.type` |
|---|---|
| Sub-lord | `kp_sub_lord` |
| Significator | `kp_significator` |
| Badhaka | `kp_badhaka` |
| Longevity factor | `kp_longevity_factor` |

---

### BOOK 4 -- Mundane Astrology

**Status: FULLY INGESTED.** Do not re-ingest.

- `ingest_mundane_interpretation_v22.py` ✅ Done
- `ingest_mundane_engine_specs_v22.py` ✅ Done
- `ingest_mundane_geo_entities_v1.py` ✅ Done
- `ingest_mundane_v2_novel_migrate.py` ✅ Done
- 14 patch scripts ✅ Done

The "Mundane Astrology De-code TextBook" folder contains the 4 source PDFs -- these are reference only, not pending ingest.

---

### BOOK 5 -- Remedies (Mantra + Yantra)

**Status: Scripts written and dry-run verified. Pending live upload confirmation.**

| Batch | Scope | Script | Status |
|---|---|---|---|
| Core Remedies | 100 Mantra rules | `ingest_remedies_v1.py` | ✅ Ingested |
| Dhana Remedies | IDs 1-100 | `ingest_remedies_dhana_v1.py` | ✅ Written, dry-run pass |
| Gemstone Remedies | IDs 101-200 | `ingest_remedies_gemstones_v1.py` | ✅ Written (98/100) |
| Crystal Remedies | IDs 201-300 | `ingest_remedies_crystals_v1.py` | ✅ Written (100/100) |
| 7 Chakra Healing | IDs 301-307 | `ingest_remedies_chakra_v1.py` | ✅ Written (7/7) |
| LK Remedies | IDs 308-668 | `ingest_lk_remedies_v1.py` | ✅ Written (361/361) |
| Krishna Prashnavali | Separate set | `ingest_krishna_prashnavali_remedies_v1.py` | ✅ Written |

No new decode work needed. Confirm live upload status before claiming complete.

---

## Part 10 -- What the New Thread Must NOT Do

These are the specific failures of the previous Account 2 thread:

| What they did | What to do instead |
|---|---|
| **Wrote rules from scratch on a Branch A chapter when a JSON Ready doc existed** | Branch A = refine the NLM JSON. Open the JSON Ready doc first. Add TD-15 fields, fix condition types, cross-check against Summaries. Never start from zero when NLM work already exists. |
| Wrote rules directly to MongoDB without running a Dry Run | Always run `--dry-run` first. Zero exceptions. |
| Ignored the Validator; submitted rules with missing TD-15 fields | Run `validate_rules.py` to 0 errors before anything else. |
| Called new rule creation "upserting" | Upsert = patching an existing rule. New rules = ingesting a new batch. |
| Called rules "live" or "active" as soon as they were in the DB | Rules are not active until `approval_status = "approved"`. Co-founder must sign off via Library Console. |
| Did not identify Contradiction Pairs | Contradiction detection is mandatory before delivering the JSON. |
| Used different `science_id` for the same science across chapters | Pick the correct `science_id` once and use it consistently across ALL chapters of the same book. |
| Did not produce a Diagnostic doc | Every chapter must have a Diagnostic doc. No Diagnostic = no delivery accepted. |
| Decoded case study chapters as rules | Case study chapters (Ch 19 in SBC, Ch 25-58 in Longevity) = test vectors only. They go to the `case_studies` collection, not `interpretation_rules`. |
| Left out TD-15 fields | `claim_axis`, `claim_polarity`, `timing_bias`, `strength_band`, `subject_scope` are MANDATORY on every single rule. |
| Set `checkable: true` for SBC / KP rules | Phase 1: SBC and KP are always `checkable: false`. No evaluator exists yet. |

---

## Part 11 -- Audit Handoff Protocol (New Thread → CC)

When the new thread completes its work for a chapter or book, it delivers to CC via the main Temple session:

### Delivery Package Required

```
1. Chapter Diagnostic Doc (.md)
   - Chapter summary
   - Decode decisions (what included / excluded)
   - Contradiction pairs flagged
   - Open questions

2. Rules JSON File (.json)
   - All rules with full schema
   - batch_id clearly stated at top
   - Rule count stated

3. Validator output
   - Paste the validate_rules.py output showing "0 errors"

4. Dry Run output
   - Paste the batch_ingest.py --dry-run output showing counts
```

### CC Audit Process

CC will:
1. Spot-check 10-15% of rules against source documents
2. Verify all TD-15 fields are populated
3. Run contradiction detection across the new batch against the existing DB rules
4. Verify `science_id` is correct
5. Confirm `checkable` assignments are correct for the science
6. Run the live ingest and post-ingest verification (Section 8, Steps 5-6)
7. Update SCRIPTS_INDEX.md and TRACKER.md with completion status

CC does NOT approve rules for the co-founder -- that is a separate step via the Library Console.

---

## Part 12 -- Current KE Ingest Status (as of 18 May 2026)

### Fully Ingested ✅

| Book | Chapters / Scope |
|---|---|
| BPHS Vol 1 | Ch 3, 12-24, 27, 34-44 |
| BPHS Vol 2 | Ch 47-58 (Dasha / Vimshottari) |
| A Text Book of Astrology | Ch 15, 16 |
| Lal Kitab | Ch 19-29 (all chapters) |
| Mundane Astrology | Full -- interpretation rules, engine specs, geo entities, novel migration |
| Remedies (Core) | 100 Mantra + Yantra rules |

### Written / Dry-Run Verified -- Pending Live Upload Confirmation

| Book | Script | Count |
|---|---|---|
| Dhana Remedies | `ingest_remedies_dhana_v1.py` | 100 |
| Gemstone Remedies | `ingest_remedies_gemstones_v1.py` | 98 |
| Crystal Remedies | `ingest_remedies_crystals_v1.py` | 100 |
| 7 Chakra Healing | `ingest_remedies_chakra_v1.py` | 7 |
| LK Remedies | `ingest_lk_remedies_v1.py` | 361 |

### Pending New Thread Decode + Ingest

| Book | Branch | Priority | Notes |
|---|---|---|---|
| Sarvato Bhadra Chakra V2 | A | 1 -- Start here | All `checkable: false`, new condition types |
| Lal Kitab Ch 19 Update 2 | A | 2 | Patch only -- addendum to existing batch |
| Longevity KP Ch 4, 5, 15 | A | 3 | Decoded chapters available |
| Longevity KP Ch 6-19, 20-24 | B | 4 | PDF-only decode required |
| Strategist (300 Horoscopes + 300 Combinations) | B | 5 | No ingest scripts yet |

### NOT in Scope for This Thread

| Book / Area | Reason |
|---|---|
| SBC Ch 19 case studies | Test vectors -- deliver to `case_studies` collection separately |
| Longevity KP Ch 25-58 case studies | Test vectors only |
| SBC Ch 20 (Teji/Mandi commodity market) | Out of scope -- project decision |
| SBC Ch 11 Horary (Dhuajadi Chakra) | Separate `science_id: "prashna"` -- pending decision |

---

## Part 13 -- Reference Files

| File | Location | Read for |
|---|---|---|
| KE Contract (22 sections) | `Codex_Deliveries/Knowledge_Engine/CODEX_KNOWLEDGE_ENGINE_CONTRACT.md` | Full schema + architecture spec |
| Build Order (CPath-1) | `Codex_Deliveries/Knowledge_Engine/CODEX_KE_CPATH1_BUILD_ORDER.md` | Phase sequencing, what is in/out of scope |
| Paraphrase WIM | `Codex_Deliveries/Knowledge_Engine/CODEX_PARAPHRASE_WIM.md` | How to write `full_text` field |
| Scripts Index | `backend/scripts/SCRIPTS_INDEX.md` | Which chapters have already been ingested |
| Ingest Notes | `backend/scripts/INGEST_NOTES.md` | Parser quirks, known issues per chapter |
| TRACKER | `Codex_Deliveries/Knowledge_Engine/TRACKER.md` | Live sprint status |
| batch_ingest.py | `backend/scripts/batch_ingest.py` | The ingest runner |
| validate_rules.py | `backend/scripts/validate_rules.py` | Schema validator |
| 5-Book Strategy | `/Users/apple/Documents/Knowledge Engine_eBooks/New Ingest_5 Books/5 Book Ingest Strategy_Account 1 Analysis.md` | 25 open questions per book -- read before decoding SBC or Longevity |

---

*Document owner: Temple Team / Claude Code. Update after every major decode cycle.*
