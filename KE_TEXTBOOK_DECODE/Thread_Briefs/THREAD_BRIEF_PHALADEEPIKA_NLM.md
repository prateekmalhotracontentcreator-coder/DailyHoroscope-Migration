# Thread Brief -- Phaladeepika NLM Decode
## Status Update + Queries + Next Steps

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-28
> For: Phaladeepika NLM Decode Thread
> Status: **UNBLOCKED -- Ready to begin Tier 1**

---

## Current Status

The schema amendment commission (KE-SCHEMA-AMENDMENT-PD1) that was blocking this thread is now **fully delivered and committed**. All 8 schema flags from the Fresh Eyes assessment have been resolved. The NLM thread can begin decoding immediately.

**What is now available in the schema:**

| Schema addition | Use in Phaladeepika |
|---|---|
| `condition.type: "neechabhanga_rule"` | Adhyaya VII -- Maharajayogas (Neechabhanga Raja Yoga, slokas 26-30) |
| `condition.type: "lagna_sign"` + `scope: "natal_lagna"` | Adhyaya IX -- Signs as Lagna |
| `condition.type: "ashtakavarga_threshold"` | Adhyaya XXIV -- Ashtakavarga Effects |
| `vedha_nullifier` block on rule root | Adhyaya XXVI -- Transits (Vedha obstruction pairs) |
| `engine_dependency: ["kalachakra_dasa_calculator"]` | Adhyaya XXII -- Kalachakra Dasa |
| `engine_dependency: ["ashtakavarga_calculator"]` | Adhyaya XXIII/XXIV |
| `engine_dependency: ["upagraha_calculator"]` | Adhyaya XXV -- Upagrahas |
| `planet` enum extended: `mandi`, `dhuma`, `vyatipata`, `paridhi`, `indra_dhanus`, `upaketu` | Adhyaya XXV |
| `claim_axis: "longevity"` | Adhyaya XIII, XIV, XVII |
| `dasha_system: "kalachakra"` on `dasha_period` condition | Adhyaya XXII |

**Schema constants source of truth:** `backend/ke_schema_constants.py`
**Schema validation layer:** `backend/knowledge_schema.py`
**Neechabhanga pre-processor:** `compute_neechabhanga_flags()` in `backend/vedic_calculator.py`

---

## Confirmed Decode Sequence (27 chapters, 6 tiers)

```
TIER 1 -- Foundational Doctrine (start here)
  Adhyaya II   -- Planets (Karakas & significations)        ← BEGIN HERE
  Adhyaya I    -- Definitions (summary.md heavy)
  Adhyaya III  -- Zodiac Divisions (engine_specification heavy)
  Adhyaya IV   -- Shadbalas (summary.md only)

TIER 2 -- Yoga Chapters
  Adhyaya VI   -- Yogas (70+ named yogas -- heaviest chapter)
  Adhyaya VII  -- Maharajayogas (Raja Yogas + Neechabhanga)
  Adhyaya XVIII-- Conjunctions of Two Planets
  Adhyaya XXVII-- Ascetic Yogas (4 pages -- small)

TIER 3 -- House Effects
  Adhyaya VIII -- Planets in 12 Bhavas (9×12 -- largest rule chapter)
  Adhyaya IX   -- Signs as Lagna (use lagna_sign + natal_lagna scope)
  Adhyaya XVI  -- General Effects of 12 Bhavas
  Adhyaya XV   -- Method of Studying Bhava Effects
  Adhyaya X    -- Kalatra Bhava / 7th House
  Adhyaya XI   -- Female Horoscopes
  Adhyaya XII  -- Issues / Children
  Adhyaya V    -- Profession & Livelihood

TIER 4 -- Life-Span, Disease, Death (decode together)
  Adhyaya XIII -- Length of Life (longevity -- claim_axis: "longevity")
  Adhyaya XIV  -- Diseases, Death, Past & Future Births
  Adhyaya XVII -- Exit from the World (transit-based death timing)

TIER 5 -- Dasha Chapters
  Adhyaya XIX  -- Dasas and their Effects (Vimshottari)
  Adhyaya XX   -- Dasas of the Bhava-Lords and Bhuktis
  Adhyaya XXI  -- Sub-divisions of Dasas

TIER 6 -- Special Calculation Chapters
  Adhyaya XXIII-- Ashtakavarga (engine_specification heavy)
  Adhyaya XXIV -- Ashtakavarga Effects (outcome rules)
  Adhyaya XXV  -- Upagrahas (use extended planet enum + planet_category: "upagraha")
  Adhyaya XXVI -- Transits (use vedha_nullifier block for each transit rule)
  Adhyaya XXII -- Kalachakra Dasa (use dasha_system: "kalachakra" + engine_dependency)

SKIP:
  Adhyaya XXVIII -- Zero rules. Pure colophon. Do not decode.
```

---

## Encoding Notes by Chapter Type

**Adhyaya VI -- Parivartana Yogas:** 66 permutations (30 Dainya + 8 Khala + 28 Maha). Extract as individual rules, grouped by category. Do not consolidate into a single meta-rule.

**Adhyaya VII -- Neechabhanga:** Use `condition.type: "neechabhanga_rule"` with `cancellation_trigger` and `reference_point` fields. The chart engine will set `is_neechabhanga: true` on the planet before rule matching -- rules just check for that flag.

**Adhyaya IX -- Lagna Sign rules:** Every rule in this chapter uses `condition.type: "lagna_sign"` and `scope: "natal_lagna"`. Do not use `planet: "lagna"` -- that was the old workaround, rejected by schema review.

**Adhyaya XIII/XIV/XVII -- Longevity/Death:** Algorithmic content (Pinda calculation, longitude-sum formulas) → `scope: "engine_specification"` + `engine_dependency: ["longevity_calculator"]`. Configurational content (8th lord aspects, Maraka positions, benefic/malefic configurations) → `scope: "natal"` + `claim_axis: "longevity"`.

**Adhyaya XXII -- Kalachakra:** Every rule must carry `engine_dependency: ["kalachakra_dasa_calculator"]`. Period years for reference: Sun=5, Moon=21, Mars=7, Mercury=9, Jupiter=10, Venus=16, Saturn=4. Do not confuse with Vimshottari years.

**Adhyaya XXVI -- Transits:** Each transit rule has a primary condition block + vedha obstruction pairs. Use the `vedha_nullifier` block with `vedha_house`, `exception_planets` (usually `["saturn"]`), and `nullification_type: "positive_result_cancelled"`.

**Adhyaya XXV -- Upagrahas:** Include `planet_category: "upagraha"` on every condition block that references these planets. Valid planet values: `mandi`, `dhuma`, `vyatipata`, `paridhi`, `indra_dhanus`, `upaketu`. (Note: Gulika = Mandi -- same planet, use `mandi`.)

---

## Dedup Handling -- BPHS Not Yet Ready

The BPHS Vol 1 decode has not produced any rule JSON files yet (see separate BPHS brief). This means the `cross_text_matches` dedup pass cannot happen until BPHS Vol 1 completes.

**How to handle this:**
- Leave `cross_text_matches: null` on all rules for now. Do not attempt manual dedup.
- Flag chapters with high expected overlap in your Diagnostic.md: Adhyaya II, Adhyaya VIII, Adhyaya VI (Pancha Mahapurusha), Adhyaya XIX.
- The automated dedup script will be commissioned separately and run after BPHS Vol 1 completes.

**Expected overlap signal (from Fresh Eyes assessment):**
- Adhyaya VIII (Planets in 12 Bhavas): ~60-70% duplicate_candidate rate with BPHS house chapters
- Adhyaya II (Karakas): High overlap with BPHS Karaka chapter
- Adhyaya VII (Maharajayogas): **Low** overlap -- Phaladeepika's formulations are more specific
- Adhyaya XXII (Kalachakra), XXVI (Transits): Minimal overlap -- largely original to Phaladeepika

---

## Open Queries -- Please Confirm

| # | Query | Action owner |
|---|---|---|
| Q1 | Confirm PDF source in use for decode. Which edition/translation of Phaladeepika? (Raman's, Santhanam's, or other?) This affects sloka citation format. | **Phaladeepika thread** |
| Q2 | Confirm `source.sloka` format being used. Fresh Eyes recommendation: `"chapter.sloka"` e.g. `"8.4"` for Adhyaya VIII Sloka 4. Is this what the thread is using? | **Phaladeepika thread** |
| Q3 | Adhyaya I partial skip -- confirming: Slokas 1-3 (invocation) and the definitional slokas (Bhavasandhi, sign body parts, Uchcha/Neecha tables, etc.) go to Summary.md only, not Rules.json. Sloka 19 onwards (if any outcome rules appear) would go to Rules.json. Confirm this split. | **Phaladeepika thread** |
| Q4 | Adhyaya XIV includes "Past and Future Births" content. Proposed claim_axis: `"past_lives"`. This value IS in the current schema (`VALID_CLAIM_AXES`). Confirm this is acceptable or whether a more specific value is needed. | **Temple Team to confirm** |
| Q5 | Adhyaya VI -- Parivartana Yogas (66 permutations): Extract as 66 individual rules (recommended) or as fewer meta-rules with configuration arrays? The individual-rule approach allows the rule engine to match each exchange specifically. Confirm preferred approach before Adhyaya VI begins. | **Temple Team to confirm** |

---

## Output File Location

All Phaladeepika decoded output should go to:
```
/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode/
```

File naming convention (follow existing decode thread convention):
```
PD_AdhXXX_[ChapterName]_Rules.json
PD_AdhXXX_[ChapterName]_Summary.md
PD_AdhXXX_[ChapterName]_Diagnostic.md
```

---

## Immediate Next Action

**Begin Adhyaya II (Planets -- Karakas & Significations).**

This is the vocabulary foundation. Every other chapter references planetary significations that are established here. This chapter should be decoded first and completely before any Tier 2+ chapter begins.

---

*Brief prepared by Temple Team -- EverydayHoroscope, 2026-05-28*
