# Thread Brief -- Phaladeepika NLM Decode
## Status Update + Queries + Next Steps

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-28 · Last decode session: 2026-05-30 (Ch15) · Status updated: 2026-05-31
> For: Phaladeepika NLM Decode Thread
> Status: **🟢 READY FOR INGEST -- ALL 28 CHAPTERS DECODED. 743 rules (16 ch confirmed + Tier 4-6 decoded). All 6 HIGH OCR items resolved 2026-05-31.**

---

## One-Liner (Ingest)

Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_PHALADEEPIKA_INGEST.md` for all Phaladeepika KE Ingest. 743+ rules, 28 chapters decoded, all 6 HIGH items resolved -- Phase 2 ingest after BPHS Vol 1 + Vol 2 complete.

> This file (`THREAD_BRIEF_PHALADEEPIKA_NLM.md`) is the **decode brief** -- encoding notes, chapter sequence, schema types, open queries. For ingest steps, schema checklist, and inject_fields, use the ingest brief above.

---

## Status Update (2026-05-31)

All 28 chapters decoded. All 6 HIGH OCR items resolved via PDF validation 2026-05-31.

**6 HIGH items resolved:**
- pd-ch22-c001 ✅ · pd-ch25-c002 ✅ · pd-ch26-c004 ✅
- pd-ch12-c001 ✅ Benefic own sign/exalt in 5th → child loss -- TEXT-NATIVE CONFIRMED (Ch12 Sloka 3, p.117)
- pd-ch27-c001 ✅ Emancipation vs ascetic -- NOT A CONTRADICTION, complementary facets
- pd-ch21-c003 ✅ Jupiter/Mercury Bhukti -- cross-text majority POSITIVE. claim_polarity → positive. gai_citation_unverified on pd-ch21-041.

**Ch08 TBA rules:** 6 rules (Sun in houses 1-8) confirmed PDF gap -- Ch08 PDF starts at Sloka 4. Ingest with `tba:true`. TT to source clean scan.

**Remaining MED items (~25):** Ingest with `pending_review:true`. Do not block ingest.

**Ingest thread note:** Cross-check gai_citation_unverified entry for pd-ch21-041 before co-founder approval gate (not before ingest).

**"Tier 4 (3 chapters) still pending" entries in older docs are STALE.** All 28 chapters are decoded.

---

---

## Decode Progress Log (updated 2026-05-30)

| Chapter | Title | Tier | Rules | Status | Files |
|---------|-------|------|-------|--------|-------|
| Ch01 | Definitions | 1 | 10 | ✅ Complete | All 5 files |
| Ch02 | Planets | 1 | 19 | ✅ Complete | All 5 files |
| Ch03 | Zodiac | 1 | 49 | ✅ Complete | All 5 files |
| Ch04 | Shadbalas | 1 | 44 | ✅ Complete | All 5 files |
| Ch06 | Yogas | 2 | 82 | ✅ Complete | All 5 files |
| Ch07 | Maharajayogas | 2 | 49 | ✅ Complete | All 5 files |
| Ch18 | Conjunctions | 2 | 141 | ✅ Complete | All 5 files |
| Ch27 | Ascetic Yogas | 2 | 20 | ✅ Complete | All 5 files |
| Ch08 | Planets in 12 Bhavas | 3 | 111 | ✅ Complete | All 5 files |
| Ch09 | Signs as Lagna | 3 | 22 | ✅ Complete | All 5 files |
| Ch16 | General Effects of 12 Bhavas | 3 | 58 | ✅ Complete | All 5 files |
| Ch15 | Method of Studying Bhava Effects | 3 | 33 | ✅ Complete | All 5 files |
| Ch10 | Kalatra Bhava / 7th House | 3 | 38 | ✅ Complete | All 5 files |
| Ch11 | Female Horoscopes | 3 | 23 | ✅ Complete | All 5 files |
| Ch12 | Children (Issue) | 3 | 33 | ✅ Complete | All 5 files |
| Ch05 | Profession & Livelihood | 3 | 11 | ✅ Complete | All 5 files |
| **Total decoded** | | | **743** | **16 of 27 chapters** | |

**Notes on Ch08:** PDF starts mid-chapter -- Sun houses 1-6 encoded as 6 TBA placeholders (active:false). Sloka 34 truncated mid-sentence (1 TBA). Total active rules: 104 of 111. Two dignity/phase splits: Moon 1st (waxing/waning) and Saturn 1st (exaltation-or-own-sign vs other). All 9 grahas covered including Rahu and Ketu.

**Notes on Ch09:** Chapter fully present, zero TBA rules. Two sections: (1) 12 Lagna sign profiles (condition.type: "lagna_sign", scope: "natal_lagna"), (2) 9 dignity/Dasha effect rules (varga_dignity_tier + planet_combust). Key items: Moon-as-Lagna meta-rule (Rule 013) doubles activation surface; retrograde=exaltation and vargottama=own-sign equivalences (Rules 021, 022). Bonus: Ch09 page 1 contains complete Ch08 Sloka 35 text -- pd-ch08-111 recovery pending a dedicated retroactive pass. Duplicate_candidate:true for 7 of 22 rules (dignity/Dasha rules only).

**Notes on Ch16:** 58 rules, all active, zero TBA. Dominant type: yoga_combination (30+ rules). 3 batches merged. OCR errors resolved (Slokas 15/18/31 misread). Rule 015 (Moon + 2nd lord) active with placeholder outcome -- OCR corrupt. XV-30 connection types cross-referenced throughout. Transit methodology rules (Slokas 31-34) encoded as engine_specification.

**Notes on Ch15:** 33 rules, all active, zero TBA. Methodology chapter -- 23 of 33 rules are engine_specification/methodology (lowest checkable rate in Tier 3: 30%). Dominant type: methodology. Critical rules: Bhavasandhi override (017 -- highest engine priority, suppress all house predictions), Bhava interpolation (018), Bhava Karaka table (021), Dusstthana inversion (023/024), XV-30 five connection types (033). Sloka 29 body in Ch15 PDF; completion on Ch16 PDF page 1. Sloka 30 (XV-30) physically on Ch16 PDF page 1 -- encoded under Ch15 as Rule 033.

**Notes on Ch11:** 23 rules, all active, zero TBA. Female horoscopy chapter -- all rules default subject_scope: "native_female". Key elements: house remapping framework (001), even/odd sign character rules (002-003), 7th house husband quality + widow/remarriage indicators (004-009), Trimsamsa character lookup tables (018-019, encoded as 2 engine_specification rules covering all 7 sign groups × 5 Trimsamsa rulers), Trimsamsa strength resolution (020), Nakshatra adversity (021, partially OCR-corrupt), conception timing methodology (023). OCR issues: Sloka 4 final clause truncated (Rule 013 partial) and Sloka 9 Nakshatra mapping partially unclear (Rule 021 partial). 4 contradictions identified, 0 contradiction_flag:true, 2 open (c001 benefics-in-2nd, c003 OCR truncation).

**Ingest freeze:** Active since 2026-05-14. These files are pre-ingest preparation only. No DB writes until KE Phase 1.2 Sprint 2 (arbitration runtime) is delivered and freeze lifted.

**Output directory:** `/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode/`

---

---

## Schema Status (reference)

The schema amendment commission (KE-SCHEMA-AMENDMENT-PD1) is **fully delivered and committed**. All 8 schema flags from the Fresh Eyes assessment have been resolved.

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

**Tier 3 COMPLETE. Next: Tier 4 -- Ch13 (Length of Life).**

Ch05 is now complete (11 rules, all 5 files). Tier 3 fully decoded (8/8). Next: Ch13, Ch14, Ch17 (Longevity/Death tier -- decode together).

---

*Brief prepared by Temple Team -- EverydayHoroscope, 2026-05-28*
