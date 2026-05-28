# Phaladeepika Decode -- Schema Flags: Proposed Answers
## GAI Consultation Response + Schema Implementation Status

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-28
> Status: All 8 flags resolved -- KE-SCHEMA-AMENDMENT-PD1 delivered and committed

---

## How to Read This Document

The Phaladeepika NLM thread raised 8 schema flags before decode began. This document gives the resolved answer to each flag: what was decided, what was implemented in the schema, and exactly how the NLM thread should encode affected rules.

**Schema implementation:** All additions are live in `backend/ke_schema_constants.py` and `backend/knowledge_schema.py` as of commit 25201e4.

---

## FLAG 1 -- Vedha Nullification in Transit Rules (Adhyaya XXVI)

**Original workaround proposed:** Put Vedha exception in `notes` field as plain text.

**Decision: REJECTED -- notes field workaround causes data loss.**

The `notes` field is unstructured. The transit rule engine cannot evaluate a Vedha check from plain text. This would have made all Adhyaya XXVI rules engine-dead for transit matching.

**Resolution implemented:** `vedha_nullifier` block added as an optional top-level field on the rule document.

**Encode every Adhyaya XXVI transit rule as follows:**

```json
{
  "rule_id": "PD.XXVI.1.1",
  "scope": "transit",
  "condition": {
    "type": "transit_position",
    "planet": "sun",
    "house": 11
  },
  "outcome": {
    "effect": "auspicious",
    "claim_axis": "wealth_gains"
  },
  "vedha_nullifier": {
    "vedha_house": 5,
    "exception_planets": ["saturn"],
    "nullification_type": "positive_result_cancelled"
  }
}
```

**Rules:**
- Every transit rule in Adhyaya XXVI gets a `vedha_nullifier` block
- `exception_planets` is usually `["saturn"]` -- check the text for any additional exceptions (Jupiter is exempted for some pairs)
- `nullification_type` is always `"positive_result_cancelled"` for Vedha
- Do NOT use `notes` for this -- the `vedha_nullifier` block is machine-readable

---

## FLAG 2 -- Ashtakavarga Dot-Count Thresholds (Adhyaya XXIII-XXIV)

**Original workaround proposed:** Encode XXIV rules as `planet_in_house` with threshold in `notes` field; XXIII as `engine_specification`.

**Decision: PARTIALLY ACCEPTED -- XXIII workaround accepted; XXIV workaround rejected.**

The XXIII approach (`engine_specification`) is correct. The XXIV workaround is rejected -- dot counts in `notes` are not queryable by the rule engine.

**Resolution implemented:** `condition.type: "ashtakavarga_threshold"` added. `engine_dependency: ["ashtakavarga_calculator"]` field added.

**Adhyaya XXIII:** Encode all as `scope: "engine_specification"` + `engine_dependency: ["ashtakavarga_calculator"]`. No matchable rules. Content goes to Summary.md only.

**Adhyaya XXIV:** Encode all as:

```json
{
  "rule_id": "PD.XXIV.3.1",
  "scope": "natal",
  "engine_dependency": ["ashtakavarga_calculator"],
  "condition": {
    "type": "ashtakavarga_threshold",
    "system": "sarvashtakavarga",
    "house": 11,
    "dot_count_min": 30,
    "dot_count_max": null
  },
  "outcome": {
    "effect": "auspicious",
    "claim_axis": "wealth_gains"
  }
}
```

**Rules:**
- `system` is either `"sarvashtakavarga"` (total across all planets) or `"bhinnashtakavarga"` (individual planet chart) -- check the text
- `dot_count_max` is optional -- set to `null` for open-ended upper bound
- All Adhyaya XXIV rules require `engine_dependency: ["ashtakavarga_calculator"]` on the root
- These rules will not fire at runtime until the Ashtakavarga calculator is built -- that is expected and acceptable

---

## FLAG 3 -- Kalachakra Dasa System (Adhyaya XXII)

**Original workaround proposed:** Add `"dasha_system": "kalachakra"` to the condition block.

**Decision: ACCEPTED as proposed.**

This is additive and non-breaking. Existing Vimshottari rules without the field default to `"vimshottari"`.

**Resolution implemented:** `dasha_system` field added to `dasha_period` condition block. `engine_dependency: ["kalachakra_dasa_calculator"]` field added.

**Every Adhyaya XXII rule must be encoded as:**

```json
{
  "rule_id": "PD.XXII.4.1",
  "scope": "dasha",
  "engine_dependency": ["kalachakra_dasa_calculator"],
  "condition": {
    "type": "dasha_period",
    "planet": "moon",
    "dasha_system": "kalachakra"
  },
  "outcome": {
    "effect": "auspicious",
    "claim_axis": "general"
  }
}
```

**Kalachakra dasha years for reference (DO NOT confuse with Vimshottari):**

| Planet | Kalachakra years | Vimshottari years |
|---|---|---|
| Sun | 5 | 6 |
| Moon | 21 | 10 |
| Mars | 7 | 7 |
| Mercury | 9 | 17 |
| Jupiter | 10 | 16 |
| Venus | 16 | 20 |
| Saturn | 4 | 19 |

**Rules:**
- All Adhyaya XXII rules require both `dasha_system: "kalachakra"` AND `engine_dependency: ["kalachakra_dasa_calculator"]`
- These rules will not fire at runtime until the Kalachakra calculator is built -- that is expected and acceptable
- Adhyaya XXII is Tier 6 (last to decode) -- this flag is non-blocking for Tiers 1-5

---

## FLAG 4 -- Upagrahas / Shadow Sub-Planets (Adhyaya XXV)

**Original workaround proposed:** Use lowercase snake_case strings as non-enum `planet` values; note in Diagnostic.md.

**Decision: REJECTED -- non-enum strings break schema validation.**

**Resolution implemented:** 6 Upagraha planets added to the `planet` enum. `planet_category` sub-field added. `engine_dependency: ["upagraha_calculator"]` field added.

**Valid Upagraha planet values (now in schema):**
`mandi`, `dhuma`, `vyatipata`, `paridhi`, `indra_dhanus`, `upaketu`

**Note:** Gulika = Mandi. They are the same point. Always use `mandi`.

**Every Adhyaya XXV rule must be encoded as:**

```json
{
  "rule_id": "PD.XXV.2.1",
  "scope": "natal",
  "engine_dependency": ["upagraha_calculator"],
  "condition": {
    "type": "planet_in_house",
    "planet": "mandi",
    "planet_category": "upagraha",
    "house": 8
  },
  "outcome": {
    "effect": "inauspicious",
    "claim_axis": "longevity"
  }
}
```

**Rules:**
- `planet_category: "upagraha"` is MANDATORY on every condition block that references an Upagraha planet
- All Adhyaya XXV rules require `engine_dependency: ["upagraha_calculator"]` on the root
- These rules will not fire at runtime until the Upagraha calculator is built -- that is expected and acceptable

---

## FLAG 5 -- Neechabhanga (Debilitation Cancellation) (Adhyaya VII)

**Original workaround proposed:** Encode as `yoga_combination` with prose `configuration` field.

**Decision: REJECTED -- `yoga_combination` loses structural information; rule engine cannot evaluate cancellation conditions from prose.**

This was rated **MUST_FIX_BEFORE_NLM** because Adhyaya VII (Maharajayogas) is Tier 2 and is decoded early.

**Resolution implemented:**
- `condition.type: "neechabhanga_rule"` added to schema
- `compute_neechabhanga_flags(chart)` pre-processor added to `backend/vedic_calculator.py`
- The chart engine evaluates all 5 cancellation conditions at chart computation time and sets `is_neechabhanga: true` on each planet before rule matching

**The 5 valid `cancellation_trigger` values:**

| Value | Meaning |
|---|---|
| `sign_lord_in_kendra` | Lord of the debilitated planet's sign occupies house 1/4/7/10 from Lagna or Moon |
| `exaltation_lord_in_kendra` | Planet exalted in that sign occupies a Kendra |
| `sign_lord_aspects_debilitated` | Sign lord aspects the debilitated planet |
| `mutual_reception` | Debilitated planet exchanges signs with the sign lord |
| `exaltation_lord_aspects_debilitated` | Exaltation lord aspects the debilitated planet |

**Valid `reference_point` values:** `lagna`, `moon`, `either`

**Encode each cancellation condition as a separate rule:**

```json
{
  "rule_id": "PD.VII.26.1",
  "scope": "natal",
  "condition": {
    "type": "neechabhanga_rule",
    "planet": "mars",
    "cancellation_trigger": "sign_lord_in_kendra",
    "reference_point": "lagna"
  },
  "outcome": {
    "effect": "auspicious",
    "claim_axis": "career_growth",
    "strength_band": "extreme"
  },
  "full_text": "When Mars is in debilitation (Cancer) and the lord of Cancer (Moon) is in a Kendra from Lagna, the debilitation is cancelled and a Raja Yoga is formed."
}
```

**Rules:**
- Each cancellation trigger is a separate rule document (do not combine into one rule)
- Do NOT use `yoga_combination` for Neechabhanga -- use `neechabhanga_rule` exclusively
- The chart engine sets the pre-computed flag; the rule just checks for `is_neechabhanga: true` on the planet -- do not try to re-evaluate the cancellation logic in the rule document

---

## FLAG 6 -- Sign-as-Lagna Rules (Adhyaya IX)

**Original workaround proposed:** Use `planet_in_sign` with `planet: "lagna"` convention.

**Decision: REJECTED -- semantically incorrect; rule engine looks up planet positions, not Lagna sign, in the `planet_in_sign` path.**

This was rated **MUST_FIX_BEFORE_NLM** because Adhyaya IX is Tier 3.

**Resolution implemented:**
- `condition.type: "lagna_sign"` added to schema
- `scope: "natal_lagna"` added as a valid scope value
- Cross-field validator enforces: `lagna_sign` condition type requires `scope: "natal_lagna"`

**Encode every Adhyaya IX rule as:**

```json
{
  "rule_id": "PD.IX.1.1",
  "scope": "natal_lagna",
  "condition": {
    "type": "lagna_sign",
    "sign": "aries"
  },
  "outcome": {
    "effect": "descriptive",
    "claim_axis": "general"
  },
  "full_text": "A native born with Mesha Lagna is courageous, quick to anger, and rises by personal effort."
}
```

**Rules:**
- ALL Adhyaya IX rules: `condition.type: "lagna_sign"` + `scope: "natal_lagna"`
- Do NOT use `planet: "lagna"` anywhere -- that workaround is explicitly rejected
- `sign` values: `aries`, `taurus`, `gemini`, `cancer`, `leo`, `virgo`, `libra`, `scorpio`, `sagittarius`, `capricorn`, `aquarius`, `pisces`
- Typical output: 12 rules per sub-topic (one per sign)

---

## FLAG 7 -- Longevity as `claim_axis` (Adhyaya XIII, XIV, XVII)

**Original workaround proposed:** Use `claim_axis: "health_vitality"` + `tags: ["longevity"]`.

**Decision: REJECTED -- workaround conflates two distinct life domains and makes longevity rules non-filterable.**

**Resolution implemented:** `claim_axis: "longevity"` and `claim_axis: "longevity_trend"` added to `VALID_CLAIM_AXES`.

**Distinction between longevity types:**

| Content type | How to encode |
|---|---|
| Algorithmic content (Pinda formulas, longitude sums, calculation methods) | `scope: "engine_specification"` + `engine_dependency: ["longevity_calculator"]` |
| Configurational rules (8th lord aspects, Maraka planets, specific combos that shorten/extend life) | `scope: "natal"` + `claim_axis: "longevity"` |
| Quality indicators (strong/weak long life vs. short life patterns, without fixed calculation) | `scope: "natal"` + `claim_axis: "longevity_trend"` |

**Example -- configurational rule:**

```json
{
  "rule_id": "PD.XIII.5.1",
  "scope": "natal",
  "condition": {
    "type": "house_lord_in_house",
    "lord_of_house": 8,
    "placed_in_house": 1
  },
  "outcome": {
    "effect": "auspicious",
    "claim_axis": "longevity",
    "strength_band": "medium"
  },
  "full_text": "8th lord in the Lagna confers long life."
}
```

**Example -- algorithmic rule (Pinda calculation):**

```json
{
  "rule_id": "PD.XIII.1.1",
  "scope": "engine_specification",
  "engine_dependency": ["longevity_calculator"],
  "condition": {
    "type": "engine_specification"
  },
  "full_text": "Add the longitudes of Lagna, Sun, and Moon. The result, expressed in terms of signs, gives the Pinda -- the base unit for longevity calculation."
}
```

**Rules:**
- Adhyaya XIII, XIV, XVII all use this split -- identify which slokas are formulaic vs. configurational
- Never use `claim_axis: "health_vitality"` for longevity rules -- use `"longevity"` or `"longevity_trend"`
- `"health_vitality"` remains valid for disease, illness, vitality, and energy rules (Adhyaya XIV disease content)

---

## FLAG 8 -- BPHS Path Discrepancy (Infrastructure / Dedup)

**Original issue:** The Phaladeepika decode guide referenced `BPHS_CC_Decode/` as the dedup folder but it appeared to contain only a ThreadStart.md.

**Decision: RESOLVED -- folder is now active with 86 files covering Ch11-Ch24.**

**Current dedup status per Phaladeepika chapter:**

| Phaladeepika chapter | BPHS counterpart | Dedup ready? |
|---|---|---|
| Adhyaya VIII -- Planets in 12 Bhavas | BPHS Ch12-Ch23 (Effects of houses) | **YES** -- BPHS Ch11-Ch23 decoded |
| Adhyaya II -- Karakas & Significations | BPHS Karaka chapters | No -- not yet decoded |
| Adhyaya VI -- Pancha Mahapurusha Yogas | BPHS Yoga chapters | No -- not yet decoded |
| Adhyaya XIX -- Vimshottari Dasas | BPHS Dasha chapters | No -- not yet decoded |

**Action for NLM thread:**
- Leave `cross_text_matches: null` on all rules during initial decode
- The automated dedup script (cosine similarity threshold: 0.82) will populate this field after both Phaladeepika and BPHS relevant chapters are complete
- Do not attempt manual dedup -- the volume (expected 300+ Phaladeepika rules vs 86 BPHS files) makes manual dedup error-prone

**Dedup folder to use (canonical):**
```
/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/
```

---

## Summary -- All 8 Flags

| Flag | Chapter | Workaround decision | Schema change | Status |
|---|---|---|---|---|
| 1 -- Vedha nullification | XXVI | REJECTED -- use `vedha_nullifier` block | `vedha_nullifier` root field added | ✅ Resolved |
| 2 -- Ashtakavarga thresholds | XXIII-XXIV | PARTIAL -- XXIII accepted, XXIV rejected | `ashtakavarga_threshold` condition type added | ✅ Resolved |
| 3 -- Kalachakra dasha | XXII | ACCEPTED -- `dasha_system` field on condition | `dasha_system` field + `engine_dependency` added | ✅ Resolved |
| 4 -- Upagrahas | XXV | REJECTED -- extend enum formally | 6 planets added to enum + `planet_category` field | ✅ Resolved |
| 5 -- Neechabhanga | VII | REJECTED -- dedicated condition type needed | `neechabhanga_rule` type + pre-processor added | ✅ Resolved |
| 6 -- Sign-as-Lagna | IX | REJECTED -- use `lagna_sign` type | `lagna_sign` type + `natal_lagna` scope added | ✅ Resolved |
| 7 -- Longevity claim_axis | XIII/XIV/XVII | REJECTED -- add `longevity` as valid value | `claim_axis: "longevity"` + `"longevity_trend"` added | ✅ Resolved |
| 8 -- BPHS path discrepancy | All | RESOLVED -- folder now active | No schema change needed | ✅ Resolved |

**All 8 flags resolved. Phaladeepika NLM decode is unblocked. Begin with Adhyaya II.**

---

*Prepared by Temple Team -- EverydayHoroscope, 2026-05-28*
*In response to PD_SCHEMA_FLAGS_GAI_CONSULTATION.md -- schema implementation via KE-SCHEMA-AMENDMENT-PD1*
