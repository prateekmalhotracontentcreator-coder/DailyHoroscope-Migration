# CODEX COMMISSION: KE-SCHEMA-AMENDMENT-PD1
## Knowledge Engine -- Schema Amendment (Phaladeepika Pre-Decode)

> Commission ID: KE-SCHEMA-AMENDMENT-PD1
> Date: 2026-05-28
> Status: READY TO ISSUE
> Thread: Knowledge Engine Codex Thread
> Prerequisite: GAI schema flag consultation complete ✅
> Blocks: Phaladeepika NLM cannot begin until this commission is DELIVERED and VERIFIED

---

## Why This Commission Exists

A Fresh Eyes review of all 28 Phaladeepika chapters identified 8 schema gaps. GAI reviewed the gaps and issued recommendations (see `PD_SCHEMA_FLAGS_GAI_CONSULTATION.md` + GAI response). Two flags were rated **MUST_FIX_BEFORE_NLM** -- the NLM thread cannot decode Phaladeepika using the workarounds proposed; they cause irrecoverable data loss or semantic errors.

This commission implements all GAI-approved schema additions before the Phaladeepika decode begins.

**This commission touches:**
- The KE schema definition / validation layer
- `backend/vedic_calculator.py` -- one new pre-processing function
- No user-facing changes, no frontend changes, no router changes

---

## Deliverable 1 -- Schema Definition Updates

### 1A. New `condition.type` values

Add the following to the valid enum of `condition.type`:

#### `neechabhanga_rule`
For debilitation-cancellation conditions (Raja Yoga arising from Neechabhanga).

```json
{
  "condition": {
    "type": "neechabhanga_rule",
    "planet": "mars",
    "cancellation_trigger": "sign_lord_in_kendra",
    "reference_point": "lagna"
  }
}
```

**Valid `cancellation_trigger` values:**
- `sign_lord_in_kendra` -- lord of the debilitated planet's sign occupies a Kendra from Lagna or Moon
- `exaltation_lord_in_kendra` -- planet that would be exalted in that sign occupies a Kendra
- `sign_lord_aspects_debilitated` -- sign lord aspects the debilitated planet
- `mutual_reception` -- debilitated planet exchanges signs with the sign lord
- `exaltation_lord_aspects_debilitated` -- exaltation lord aspects the debilitated planet

**Valid `reference_point` values:** `lagna`, `moon`, `either`

---

#### `lagna_sign`
For effects given for each Rasi as the rising Ascendant.

```json
{
  "condition": {
    "type": "lagna_sign",
    "sign": "aries"
  }
}
```

Valid `sign` values: `aries`, `taurus`, `gemini`, `cancer`, `leo`, `virgo`, `libra`, `scorpio`, `sagittarius`, `capricorn`, `aquarius`, `pisces`

---

#### `ashtakavarga_threshold`
For rules based on benefic dot counts in Ashtakavarga.

```json
{
  "condition": {
    "type": "ashtakavarga_threshold",
    "system": "sarvashtakavarga",
    "house": 11,
    "dot_count_min": 30,
    "dot_count_max": 56
  }
}
```

Valid `system` values: `sarvashtakavarga`, `bhinnashtakavarga`
`dot_count_max` is optional (null for open-ended upper bound).

---

### 1B. New `scope` value

Add `natal_lagna` to the valid enum of `scope`:

| Scope value | Used for |
|---|---|
| `natal` | Standard natal planetary rules |
| `natal_lagna` | **NEW** -- Rules for each sign as the Ascendant (Adhyaya IX type) |
| `transit` | Transit-based rules |
| `dasha` | Dasha period rules |
| `engine_specification` | Calculation methodology, not a matchable rule |

All rules with `condition.type: "lagna_sign"` must use `scope: "natal_lagna"`.

---

### 1C. New top-level rule fields

Add these optional fields to the rule document root. All default to `null` when not populated.

#### `vedha_nullifier`
For transit rules with Vedha obstruction pairs (Adhyaya XXVI type).

```json
"vedha_nullifier": {
  "vedha_house": 5,
  "exception_planets": ["saturn"],
  "nullification_type": "positive_result_cancelled"
}
```

Valid `nullification_type` values: `positive_result_cancelled`, `result_reversed`, `result_delayed`

---

#### `engine_dependency`
Array of engine capability identifiers. A rule with this field set must NOT be evaluated at runtime until all listed engines are available in the platform.

```json
"engine_dependency": ["kalachakra_dasa_calculator"]
```

Known dependency identifiers:
- `kalachakra_dasa_calculator` -- required for Adhyaya XXII rules
- `ashtakavarga_calculator` -- required for `ashtakavarga_threshold` conditions
- `upagraha_calculator` -- required for Upagraha planet rules

---

#### `cross_text_matches`
Array of matching rules from other decoded texts (populated during dedup pass).

```json
"cross_text_matches": [
  {
    "rule_id": "BPHS.XI.12.1",
    "similarity_score": 0.89,
    "relationship": "identical_claim"
  }
]
```

Valid `relationship` values: `identical_claim`, `near_identical`, `same_principle_different_phrasing`, `partial_overlap`

---

### 1D. Planet enum extension

Add the following to the valid `planet` values:

```
mandi, dhuma, vyatipata, paridhi, indra_dhanus, upaketu
```

All 6 are classified as Upagrahas. Any rule using these values must also include `"planet_category": "upagraha"` in its condition block.

---

### 1E. New condition sub-field: `planet_category`

Optional field on any condition block that specifies a planet:

```json
"condition": {
  "type": "planet_in_house",
  "planet": "mandi",
  "planet_category": "upagraha",
  "house": 8
}
```

Valid `planet_category` values: `physical` (default, all 9 standard planets), `upagraha` (the 6 shadow sub-planets)

When `planet_category` is absent, assume `physical`.

---

### 1F. New `claim_axis` value

Add `"longevity"` to the valid `claim_axis` enum.

**Distinction from `health_vitality`:**
- `health_vitality` -- day-to-day energy, illness episodes, constitution
- `longevity` -- predicted lifespan, Ayur calculation, death timing, Maraka effects

**Arc Angel mapping:** `longevity` maps to the **8th Bhava (Ayur Bhava)** in the Arc Angel 12-domain framework.

**Rule classification for Adhyaya XIII:**
- Algorithmic rules (Pinda calculation, longitude-sum formulas) → `scope: "engine_specification"`, `engine_dependency: ["longevity_calculator"]`
- Configurational rules (8th lord aspects, Maraka planets, benefic/malefic configurations) → `scope: "natal"`, `claim_axis: "longevity"`

Also add `"longevity"` to the dasha `condition.type` specific `claim_axis` set so dasha-period longevity rules can be filtered correctly.

---

### 1G. Kalachakra Dasa -- `dasha_system` field

Add `dasha_system` as an optional field inside the `dasha_period` condition block:

```json
"condition": {
  "type": "dasha_period",
  "planet": "moon",
  "dasha_system": "kalachakra"
}
```

Valid `dasha_system` values: `vimshottari` (default), `kalachakra`, `yogini`, `jaimini`

When `dasha_system` is absent, assume `vimshottari`.

Kalachakra period years for reference (must be stored in the rule engine config):
```
Sun=5, Moon=21, Mars=7, Mercury=9, Jupiter=10, Venus=16, Saturn=4
```
(Note: different from Vimshottari -- do not confuse)

All Adhyaya XXII rules must also carry `"engine_dependency": ["kalachakra_dasa_calculator"]`.

---

## Deliverable 2 -- Chart Engine Pre-Processor (vedic_calculator.py)

Add a new function to `backend/vedic_calculator.py`:

```python
def compute_neechabhanga_flags(chart: dict) -> dict:
    """
    For each debilitated planet in the chart, evaluate the 5 classical
    Neechabhanga cancellation conditions and set is_neechabhanga: bool.

    Returns the chart dict with is_neechabhanga added to each planet object.

    Neechabhanga conditions (any one is sufficient):
    1. sign_lord_in_kendra: lord of debilitated planet's sign occupies
       house 1, 4, 7, or 10 from Lagna OR Moon
    2. exaltation_lord_in_kendra: planet that would exalt in that sign
       occupies house 1, 4, 7, or 10 from Lagna OR Moon
    3. sign_lord_aspects_debilitated: sign lord aspects the debilitated planet
       (use Parashari full aspects: 7th from every planet;
       Mars 4th/8th; Jupiter 5th/9th; Saturn 3rd/10th)
    4. mutual_reception: debilitated planet and its sign lord exchange signs
    5. exaltation_lord_aspects_debilitated: exaltation lord aspects the
       debilitated planet

    Debilitation signs (neecha rasi) reference:
    Sun=Libra, Moon=Scorpio, Mars=Cancer, Mercury=Pisces,
    Jupiter=Capricorn, Venus=Virgo, Saturn=Aries,
    Rahu=Scorpio (or Sagittarius per tradition), Ketu=Taurus
    """
```

**Important:** This function runs AFTER `calculate_vimshottari_dasha()` and AFTER the main chart calculation -- it is a post-processing enrichment step, not a replacement for any existing function. Call it at the end of the chart-building pipeline.

The `is_neechabhanga` boolean is then available on each planetary object when the rule engine evaluates `condition.type: "neechabhanga_rule"` -- the engine reads the pre-computed flag rather than re-evaluating the conditions at match time.

---

## Deliverable 3 -- JSON Parse Error Fix

The following file has a JSON syntax error that makes it unreadable:

```
/Users/apple/Documents/Knowledge Engine_eBooks/KP_CC_Decode/KP3_ChT04_Role_of_Sub_Rules.json
```

Error: `Expecting ',' delimiter: line 451 column 304 (char 20486)`

Fix the JSON syntax error. Do not change any rule content -- only fix the syntax.

Verify after fix:
```bash
python3 -m json.tool "/Users/apple/Documents/Knowledge Engine_eBooks/KP_CC_Decode/KP3_ChT04_Role_of_Sub_Rules.json" > /dev/null && echo "VALID"
```

---

## Deliverable 4 -- Schema Validation Update

If the KE codebase has a JSON schema validation file or a Pydantic model that defines valid field values (condition types, scope values, claim_axis, planet enum), update it to include all new values from Deliverables 1A through 1G.

If no validation layer exists, create a `backend/ke_schema_constants.py` file:

```python
# backend/ke_schema_constants.py
# Single source of truth for all KE schema enumerated values

VALID_CONDITION_TYPES = [
    "planet_in_house", "planet_in_sign", "planet_in_house_and_sign",
    "yoga_combination", "dasha_period", "transit_position",
    "house_lord_in_house", "aspect_rule", "engine_specification",
    # PD1 additions:
    "neechabhanga_rule", "lagna_sign", "ashtakavarga_threshold",
]

VALID_SCOPES = [
    "natal", "transit", "dasha", "engine_specification",
    "natal_lagna",  # PD1 addition
]

VALID_CLAIM_AXES = [
    "career_growth", "career_timing", "wealth", "marriage_timing",
    "relationship_quality", "children", "health_vitality",
    "spiritual_growth", "enemies_adversaries", "past_lives",
    "longevity",  # PD1 addition
]

STANDARD_PLANETS = [
    "sun", "moon", "mars", "mercury", "jupiter",
    "venus", "saturn", "rahu", "ketu",
]

UPAGRAHA_PLANETS = [
    "mandi", "dhuma", "vyatipata", "paridhi", "indra_dhanus", "upaketu",
]

ALL_PLANETS = STANDARD_PLANETS + UPAGRAHA_PLANETS

VALID_DASHA_SYSTEMS = ["vimshottari", "kalachakra", "yogini", "jaimini"]

VALID_PLANET_CATEGORIES = ["physical", "upagraha"]

ENGINE_DEPENDENCY_IDENTIFIERS = [
    "kalachakra_dasa_calculator",
    "ashtakavarga_calculator",
    "upagraha_calculator",
    "longevity_calculator",
]
```

---

## Delivery Checklist

**Schema definition:**
- [ ] `neechabhanga_rule` added to valid condition types
- [ ] `lagna_sign` added to valid condition types
- [ ] `ashtakavarga_threshold` added to valid condition types
- [ ] `natal_lagna` added to valid scope values
- [ ] `vedha_nullifier` block defined as optional root field
- [ ] `engine_dependency` array defined as optional root field
- [ ] `cross_text_matches` array defined as optional root field
- [ ] `planet_category` sub-field defined for condition blocks
- [ ] 6 Upagraha planet names added to planet enum
- [ ] `"longevity"` added to valid claim_axis values
- [ ] `dasha_system` field added to `dasha_period` condition type

**Chart engine:**
- [ ] `compute_neechabhanga_flags(chart)` added to `backend/vedic_calculator.py`
- [ ] All 5 cancellation conditions implemented
- [ ] All 9 planets' debilitation signs correctly coded
- [ ] `is_neechabhanga` boolean added to each planetary object in chart output
- [ ] `python3 -m py_compile backend/vedic_calculator.py` → PASS

**Bug fix:**
- [ ] `KP3_ChT04_Role_of_Sub_Rules.json` JSON syntax error resolved
- [ ] `python3 -m json.tool KP3_ChT04_Role_of_Sub_Rules.json > /dev/null` → VALID

**Schema constants:**
- [ ] `backend/ke_schema_constants.py` created (or existing validation layer updated)
- [ ] All new values present in constants file

**Do NOT modify:** Any other existing file outside these deliverables. No frontend changes. No router changes. No changes to existing rule JSON content (rule content migration is a separate exercise -- see retroactive impact section).

---

## What This Commission Does NOT Cover

- Migrating `claim_axis` values in existing decoded JSON files -- this is a separate data migration exercise (see Retroactive Impact Assessment below)
- Implementing the Ashtakavarga or Kalachakra calculation engines -- both are Phase 2
- Implementing the Upagraha position calculator -- Phase 2
- Building the dedup automation script -- separate commission when BPHS Vol 1 decode completes

---

*Commission prepared by Temple Team -- EverydayHoroscope, 2026-05-28*
