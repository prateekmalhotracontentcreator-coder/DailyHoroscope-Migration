# Phaladeepika Decode -- Schema Flag Consultation
## GAI Input Requested on 8 Rule-Encoding Flags

> Document prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-28
> Purpose: Pre-decode schema review -- requesting GAI input before NLM begins on Phaladeepika

---

## Background (Read First)

We are building a **Jyotish Knowledge Engine** -- an interpretation database that extracts rules from classical Vedic astrology texts into a structured JSON schema, then uses those rules to power AI-generated birth chart readings.

**Current pipeline:**
1. Classical texts (Phaladeepika, BPHS, Longevity books, etc.) are decoded chapter by chapter into structured JSON rule documents
2. Each rule follows a strict schema: `condition` block (what planetary configuration triggers the rule) + `outcome` block (what life effect is predicted)
3. Rules are stored in MongoDB and matched against a user's computed birth chart at runtime
4. Matched rules feed a narrative engine (Claude API) that generates coherent readings

**The decode process:**
- An NLM (language model thread) reads each chapter and extracts rules into the schema
- A human reviewer (Temple Team) reviews the JSON output, approves or flags rules
- Dedup pass compares each new rule against already-decoded chapters to flag near-identical content

**Phaladeepika** is the next text to be decoded -- a complete 28-chapter classical Vedic astrology manual covering everything from planetary significations to transit rules, yogas, dashas, longevity, and disease.

**The current rule schema structure (simplified):**
```json
{
  "rule_id": "PD.VIII.3.2",
  "source": { "text": "Phaladeepika", "chapter": 8, "sloka": "8.3" },
  "scope": "natal",
  "condition": {
    "type": "planet_in_house",
    "planet": "sun",
    "house": 3
  },
  "outcome": {
    "effect": "auspicious",
    "dimension": "career",
    "claim_axis": "career_growth",
    "strength_band": "medium"
  },
  "full_text": "Sun in the 3rd house makes the native courageous, wealthy, and successful in undertakings.",
  "notes": "",
  "approval_status": "pending"
}
```

**Valid `condition.type` values (current schema):**
`planet_in_house`, `planet_in_sign`, `planet_in_house_and_sign`, `yoga_combination`, `dasha_period`, `transit_position`, `house_lord_in_house`, `aspect_rule`, `engine_specification`

**Valid `planet` values (current schema):**
`sun`, `moon`, `mars`, `mercury`, `jupiter`, `venus`, `saturn`, `rahu`, `ketu`

**Valid `scope` values:**
`natal`, `transit`, `dasha`, `engine_specification`

---

## The 8 Flags -- GAI Input Requested

A Fresh Eyes review of all 28 Phaladeepika chapters before decoding began raised 8 schema flags. Temple Team has drafted initial workarounds for each. We are requesting GAI to review each flag and:

1. **Confirm or improve** the proposed workaround
2. **Flag any data loss** -- if the workaround loses information that the schema should capture
3. **Recommend schema extensions** if a proper field is needed (and how it should look)
4. **Advise on priority** -- which flags are critical to resolve before NLM begins, vs. which can be handled during the decode

---

### FLAG 1 -- Vedha Nullification in Transit Rules (Adhyaya XXVI)

**What Vedha is:**
In Vedic transit astrology, every planet-in-house transit result comes with a *Vedha* (obstruction) rule. Vedha means: the positive result of Planet X in House Y is **nullified** if any other planet (with specific exceptions, usually Saturn) simultaneously occupies the paired "Vedha house" of Y.

Example: "Sun transiting the 11th house gives financial gain and fulfilment of desires -- unless any planet except Saturn simultaneously occupies the 5th house (the Vedha house for Sun in 11th)."

**The schema gap:**
The current schema has no field to capture this two-layer structure. A transit rule has a primary outcome AND an exception condition. The condition block covers the primary trigger but has no `exception` or `vedha_nullifier` sub-field.

**Phaladeepika Adhyaya XXVI** is 33 pages with Vedha pairs given for all 9 planets across multiple house positions -- roughly 40-60 transit rules with Vedha modifiers.

**Temple Team's proposed workaround:**
Encode the primary transit rule normally. Put the Vedha exception in the `notes` field as plain text:
```json
"notes": "Vedha nullifier: result is obstructed if any planet except Saturn simultaneously transits house 5. Vedha house pair for Sun in 11th."
```

**Concerns with this workaround:**
- The `notes` field is unstructured -- the rule engine cannot programmatically evaluate a Vedha check from plain text
- If the KE is ever built to check Vedha in transit matching, it needs a machine-readable structure, not a prose note
- Some Vedha pairs have planet-specific exceptions (Saturn is exempted from Vedha for most planets; Jupiter is exempted for some)

**Questions for GAI:**
1. Is the `notes` workaround acceptable given Phase 1 scope, or does it create technical debt that will block the transit rule engine?
2. Should we add a structured `vedha_nullifier` block now even though the transit evaluation engine is Phase 2? Suggested structure:
   ```json
   "vedha_nullifier": {
     "vedha_house": 5,
     "exception_planets": ["saturn"],
     "nullification_type": "positive_result_cancelled"
   }
   ```
3. Should Vedha rules be encoded as separate "anti-rule" linked documents, or as a modifier field on the primary rule? What are the trade-offs for the rule engine architecture?
4. Are there other classical texts you are aware of where Vedha is encoded differently that we should align to?

---

### FLAG 2 -- Ashtakavarga Numeric Dot Thresholds (Adhyaya XXIII-XXIV)

**What Ashtakavarga is:**
A point-scoring system in Vedic astrology where each planet contributes "benefic dots" (0 or 1) to each of the 12 houses, based on the positions of all 8 relevant planets. The total across all 8 planets' charts gives the Sarvashtakavarga score for each house (max 56 dots). Rules then say: "if a house has X or more dots, the transit of a planet through it is [highly auspicious / neutral / inauspicious]."

**The schema gap:**
Rules like "if the 11th house has 30 or more benefic dots in the Sarvashtakavarga, transit through it is highly auspicious" require a **numeric threshold condition**. The current condition block has no `threshold_value`, `dot_count_min`, or comparable field.

**Phaladeepika coverage:**
- **Adhyaya XXIII**: Calculation methodology for building the Ashtakavarga tables -- no outcome rules, just the mathematics
- **Adhyaya XXIV**: Outcome rules using dot-count thresholds -- this is where machine-readable rules are needed

**Temple Team's proposed workaround:**
- Adhyaya XXIII: encode all entries as `scope: "engine_specification"` (no rule matching needed -- these are calculation instructions)
- Adhyaya XXIV: encode as `condition.type: "planet_in_house"` with the threshold carried in `full_text` and a `notes` field: `"dot_count_min": 30`

**Concerns:**
- `dot_count_min` in `notes` is not machine-readable
- The rule engine cannot evaluate "house has 30+ dots" without a proper numeric condition field
- Ashtakavarga scoring requires a separate calculation layer before rule matching can happen

**Questions for GAI:**
1. What is the correct schema structure for a numeric threshold condition? Suggested extension:
   ```json
   "condition": {
     "type": "ashtakavarga_threshold",
     "system": "sarvashtakavarga",
     "house": 11,
     "dot_count_min": 30,
     "dot_count_max": null
   }
   ```
2. Does the Ashtakavarga calculation need to be a pre-processing step that adds dot scores to the chart data object before rule matching runs? If yes, how should this be architecturally separated from the natal rule engine?
3. Should Adhyaya XXIII (calculation methodology) be encoded at all, or simply documented in a Summary.md and left for the engineering team to implement as a calculation function?
4. Are there range-based rules (e.g., "between 25-30 dots = neutral, 30+ = auspicious") -- if so, how should ranges be encoded?

---

### FLAG 3 -- Kalachakra Dasa System (Adhyaya XXII)

**What the issue is:**
The current schema supports `condition.type: "dasha_period"` for rules that fire during a specific planetary dasha period. This implicitly assumes the **Vimshottari dasha system** (which the platform already computes via `vedic_calculator.py`).

**Adhyaya XXII** introduces the **Kalachakra Dasa** -- a completely different dasha system with different period lengths:

| Planet | Vimshottari (years) | Kalachakra (years) |
|---|---|---|
| Sun | 6 | 5 |
| Moon | 10 | 21 |
| Mars | 7 | 7 |
| Mercury | 17 | 9 |
| Jupiter | 16 | 10 |
| Venus | 20 | 16 |
| Saturn | 19 | 4 |

Kalachakra also uses a different calculation method (based on the Nakshatra pada of the birth Moon, not just the Nakshatra). Rahu and Ketu have different roles.

**Schema gap:**
The `condition.type: "dasha_period"` field has no `dasha_system` qualifier. A rule saying "during Moon dasha, X happens" means different things in Vimshottari vs. Kalachakra -- the Moon period is 10 years in one and 21 years in the other.

**Temple Team's proposed workaround:**
Add `"dasha_system": "kalachakra"` to the condition block for all Adhyaya XXII rules:
```json
"condition": {
  "type": "dasha_period",
  "planet": "moon",
  "dasha_system": "kalachakra"
}
```
This is an additive non-breaking field -- existing Vimshottari rules without this field are assumed to be `"vimshottari"` by default.

**Concerns:**
- The platform does not currently compute Kalachakra Dasa -- `vedic_calculator.py` only has Vimshottari
- Rules with `dasha_system: "kalachakra"` cannot be evaluated at runtime until a Kalachakra calculation engine is built
- These rules should perhaps be tagged with a flag that prevents them from firing until the engine exists

**Questions for GAI:**
1. Is `"dasha_system"` the correct field name, or is there a better convention?
2. Should Kalachakra rules carry a special `approval_status` or `engine_dependency` field that prevents them from being surfaced in reports until the Kalachakra engine is built?
3. How should the `dasha_period` condition block be structured to accommodate multiple dasha systems in the future? Should `dasha_system` be a required field on all `dasha_period` rules (defaulting to `"vimshottari"` for existing rules)?
4. Is Kalachakra commonly used in practice alongside Vimshottari, or is it typically a separate specialisation? This affects how much engineering priority to give it.

---

### FLAG 4 -- Upagrahas / Shadow Sub-Planets (Adhyaya XXV)

**What Upagrahas are:**
Classical Vedic astrology recognises several "shadow" or "sub-planets" that are calculated points (not physical bodies) derived from planetary positions. They are treated as significators and their house placements carry predictive weight.

**The 6 Upagrahas in Adhyaya XXV:**
- **Mandi** (also called Gulika) -- son of Saturn; most commonly used Upagraha
- **Dhuma** -- derived from Sun's longitude
- **Vyatipata** -- derived from Dhuma
- **Paridhi** (also called Indrachapa) -- derived from Vyatipata
- **Indra Dhanus** -- derived from Paridhi
- **Upaketu** -- derived from Sun

**Schema gap:**
The current `planet` enum contains only the 9 standard planets: `sun, moon, mars, mercury, jupiter, venus, saturn, rahu, ketu`. None of the 6 Upagrahas are valid values. Rules like "Mandi in the 8th house indicates an accidental death" cannot be encoded cleanly.

**Temple Team's proposed workaround:**
Use lowercase snake_case string extensions in the `planet` field, accepted as non-enum strings for now:
`"mandi"`, `"dhuma"`, `"vyatipata"`, `"paridhi"`, `"indra_dhanus"`, `"upaketu"`

Each rule using these values is noted in its Diagnostic.md with `"planet_enum_extension": true`.

**Concerns:**
- Using non-enum strings may break schema validation if strict validation is applied
- The platform does not currently compute Upagraha positions -- `vedic_calculator.py` has no Upagraha calculation
- Mandi/Gulika is the most commonly referenced Upagraha; the others appear far less frequently

**Questions for GAI:**
1. Should the planet enum be formally extended now to include all 6 Upagrahas, even though only Mandi is commonly used? Or handle them case by case?
2. Is there a standard way to calculate Upagraha positions using pyswisseph or standard Vedic formulas? (Mandi's calculation: `[(day_duration / 8) × weekday_modifier] + sunrise_time`)
3. Should Upagraha-based rules carry a separate `planet_category` field to distinguish them from physical planets?
   ```json
   "condition": {
     "type": "planet_in_house",
     "planet": "mandi",
     "planet_category": "upagraha",
     "house": 8
   }
   ```
4. How significant is Mandi/Gulika in practice compared to the other 5 Upagrahas? Should we prioritise only Mandi for Phase 1 and defer the rest?

---

### FLAG 5 -- Neechabhanga (Debilitation Cancellation) (Adhyaya VII)

**What Neechabhanga is:**
When a planet is in its sign of debilitation (e.g., Sun in Libra, Mars in Cancer), it is said to be weakened. However, specific configurations can "cancel" this debilitation -- this is called Neechabhanga (lit. "breaking of debilitation"). When debilitation is cancelled, the planet is said to give results as if in exaltation, often producing a Raja Yoga (combination for power/success).

**The cancellation conditions (Adhyaya VII, Slokas 26-30):**
Examples of Neechabhanga conditions:
- The lord of the debilitated planet's sign is in a Kendra (angular house 1, 4, 7, 10) from Lagna or Moon
- The planet that would be exalted in the sign of debilitation is in a Kendra
- The debilitated planet is aspected by its own sign lord
- The debilitated planet exchanges signs with another planet (mutual reception)

**Schema gap:**
There is no `"neechabhanga"` condition type. These rules don't fit cleanly into `"planet_in_house"` or `"planet_in_sign"` because the condition involves multiple simultaneous factors (debilitated planet + cancelling configuration).

**Temple Team's proposed workaround:**
Encode as `condition.type: "yoga_combination"` with a `configuration` field:
```json
"condition": {
  "type": "yoga_combination",
  "yoga_name": "Neechabhanga Raja Yoga",
  "configuration": "Debilitated planet's sign lord occupies a Kendra (1st, 4th, 7th, or 10th house) from Lagna or Moon."
},
"outcome": {
  "effect": "auspicious",
  "claim_axis": "career_growth",
  "strength_band": "extreme"
}
```

**Concerns:**
- `"yoga_combination"` is meant for named yogas with fixed planet combinations -- Neechabhanga is conditional, not a fixed combination
- The multiple conditions (any one of 4+ cancellation rules qualifies) cannot be expressed in a single configuration string
- The rule engine would need to evaluate the configuration string as a logical expression, which prose cannot enable

**Questions for GAI:**
1. Should `"neechabhanga"` be added as a dedicated `condition.type` with structured sub-conditions?
   ```json
   "condition": {
     "type": "neechabhanga",
     "debilitated_planet": "mars",
     "cancellation_condition": "sign_lord_in_kendra",
     "reference_point": "lagna"
   }
   ```
2. How many distinct Neechabhanga cancellation conditions exist across classical texts, and should each be a separate rule document or combined into one?
3. Does the `"yoga_combination"` workaround lose enough information to create problems for the rule engine, or is prose configuration text acceptable for Phase 1?
4. At runtime, how should the engine evaluate Neechabhanga -- as a pre-processing flag on the chart object (`mars.is_neechabhanga: true`) or as a condition evaluated during rule matching?

---

### FLAG 6 -- Sign-as-Lagna Rules (Adhyaya IX)

**What the chapter covers:**
Adhyaya IX gives effects for each of the 12 Rashis (zodiac signs) when rising as the Lagna (Ascendant). These are not "planet in sign" rules -- they are "this sign is the Lagna" rules. Example: "A native born with Mesha (Aries) Lagna is courageous, quick to anger, and rises to a position of authority through personal effort."

**Schema gap:**
The current condition types do not include `"lagna_sign"`. The closest is `"planet_in_sign"` but the Lagna is not technically a planet.

**Temple Team's proposed workaround:**
Use `condition.type: "planet_in_sign"` with a convention: `"planet": "lagna"` and `"sign": "aries"`.
```json
"condition": {
  "type": "planet_in_sign",
  "planet": "lagna",
  "sign": "aries"
}
```
Note each rule with `"lagna_sign_workaround": true` in Diagnostic.md.

**Concerns:**
- "Lagna" is not a planet -- using it in the `planet` field is semantically incorrect
- The rule engine may not know to look up "where is the Lagna sign?" the same way it looks up "where is Mars?"
- A chart object already has a `lagna_sign` field -- a proper `"lagna_sign"` condition type could match against it directly

**Questions for GAI:**
1. Should `"lagna_sign"` be added as a first-class `condition.type`? Suggested structure:
   ```json
   "condition": {
     "type": "lagna_sign",
     "sign": "aries"
   }
   ```
2. How significant is this chapter for the KE? Adhyaya IX gives broad Lagna-level traits -- does the rule engine benefit from storing these as individual rules, or are they better encoded as a lookup table (a separate collection)?
3. Is the `planet: "lagna"` workaround ambiguous enough to cause rule-engine matching errors, or is it a safe convention?
4. In the broader KE architecture, where does Lagna-based interpretation sit relative to planet-in-house and yoga rules? Should it have a different `scope` value (e.g., `"natal_lagna"`)?

---

### FLAG 7 -- Longevity as `claim_axis` (Adhyaya XIII)

**What the chapter covers:**
Adhyaya XIII is entirely devoted to longevity calculation -- specifically how to determine the length of a native's life. This is distinct from general health effects. Methods include: combining the longitudes of Lagna, Sun, and Moon; identifying the "Pinda" (death indicator) planets; assessing the strength of the 8th house lord; and specific planetary combinations that shorten or extend life.

**Schema gap:**
The valid `claim_axis` values include `"health_vitality"` but not `"longevity"` as a distinct axis. Longevity is a measurable predicted outcome (how many years a person lives) -- different in kind from health vitality (how energetic/ill a person is day to day).

**Temple Team's proposed workaround:**
Use `claim_axis: "health_vitality"` with `"tags": ["longevity"]` on all Adhyaya XIII rules.

**Concerns:**
- Longevity rules and health rules occupy the same `claim_axis`, making it harder to filter or report on them separately
- When the Arc Angel module (TD-23 in the KE Contract) maps interpretations to life domains, longevity and health vitality should arguably map differently
- A `"longevity"` claim_axis would allow the KE to surface longevity-specific rules only for relevant report types

**Questions for GAI:**
1. Should `"longevity"` be added as a valid `claim_axis` value now, before decoding begins?
2. How should longevity rules interact with the Arc Angel 12-area-of-life framework? Which life domain (Bhava) does longevity map to -- the 8th house, or is it cross-domain?
3. The longevity calculation methods in classical texts are often algorithmic (e.g., add Lagna longitude + Sun longitude + Moon longitude, then apply a formula). Should these encode as `scope: "engine_specification"` rather than as matchable rules?
4. Is there a meaningful distinction between "longevity calculation rules" (how to compute lifespan) and "longevity indicator rules" (which configurations shorten/extend life)? If yes, should they use different condition types?

---

### FLAG 8 -- BPHS Path Discrepancy (Infrastructure / Dedup)

**What the issue is:**
The Phaladeepika decode guide references this folder for cross-text dedup:
```
/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/
```
That folder exists but is **empty** (only a `ThreadStart.md` inside). The actual decoded BPHS Vol 1 JSON files are at:
```
/Users/apple/Documents/Knowledge Engine_eBooks/BPHS Vol 1 De-code/
```
Chapters decoded so far: **Ch 27** (Strengths), **Ch 34** (Planetary Effects), **Ch 40** (Royal Association Yogas), **Ch 41** (Wealth Yogas), **Ch 43** (Longevity), **Ch 44** (Marakas).

**Why dedup matters:**
Phaladeepika and BPHS overlap significantly -- especially in house-effect chapters. When two classical texts encode the same rule identically, it is a signal of higher confidence (cross-textual agreement). If dedup is skipped, the rule base is inflated with duplicate rules that appear as independent evidence when they are actually the same claim from the same tradition.

**BPHS Vol 1 status:** Currently being decoded -- approximately halfway through. The house-effect chapters (planets in Bhavas, roughly Chs 15-26) are the highest-overlap sections and are **not yet decoded**.

**Temple Team decision:** Wait for BPHS Vol 1 to complete before beginning Phaladeepika NLM.

**Questions for GAI:**
1. Is this the right decision -- wait for BPHS Vol 1 completion before Phaladeepika, specifically to ensure a clean dedup on house-effect chapters?
2. Should the dedup process be automated (a script that compares candidate rule text against existing JSON using TF-IDF or n-gram similarity) or manual (the NLM thread checks manually)? What threshold similarity should trigger a `duplicate_candidate: true` flag?
3. When two texts encode the same rule, should we: (a) keep only one rule and tag it with both source references, (b) keep both rules and link them via a `cross_text_match` field, or (c) keep both with a `duplicate_candidate` flag and let the editor decide?
4. Beyond BPHS Vol 1, which other decoded classical texts should the Phaladeepika dedup pass check against? Are there other text decode projects underway that we should wait for?

---

## Summary Table

| Flag | Chapter | Issue | Workaround Proposed | Blocking? |
|---|---|---|---|---|
| 1 | XXVI | Vedha nullification -- no exception condition field | `notes` field prose | Not blocking -- low priority until transit engine built |
| 2 | XXIII-XXIV | Ashtakavarga dot-count thresholds -- no numeric condition | `notes` field + `engine_specification` scope | Not blocking -- Ashtakavarga engine is Phase 2 |
| 3 | XXII | Kalachakra Dasa -- different period system, no `dasha_system` field | Add `"dasha_system": "kalachakra"` to condition block | Not blocking -- Kalachakra is Tier 6 (last to decode) |
| 4 | XXV | Upagrahas -- not in planet enum | Lowercase snake_case string extensions | Not blocking -- Tier 6 (second to last) |
| 5 | VII | Neechabhanga -- no dedicated condition type | Encode as `yoga_combination` with configuration text | Potentially blocking -- Adhyaya VII is Tier 2 (early) |
| 6 | IX | Sign-as-Lagna -- no `lagna_sign` condition type | `planet: "lagna"` convention in `planet_in_sign` | Potentially blocking -- Adhyaya IX is Tier 3 |
| 7 | XIII | Longevity -- not a valid `claim_axis` | Use `health_vitality` + `tags: ["longevity"]` | Low priority -- easy to migrate later |
| 8 | All | BPHS path discrepancy -- wrong dedup folder in guide | Fixed: correct path confirmed | Infrastructure fix -- resolved before NLM starts |

---

## What We Need From GAI

For each of the 8 flags above:

1. **Confirm or improve** the Temple Team workaround
2. **Specify any data loss** the workaround causes that would matter at runtime
3. **Provide exact JSON structure** for any new schema field you recommend
4. **Rate priority:** `MUST_FIX_BEFORE_NLM` / `FIX_BEFORE_TIER_N` / `ACCEPTABLE_WORKAROUND` / `DEFER_TO_PHASE_2`

Please structure your response flag by flag (Flag 1 through Flag 8) and include specific JSON examples where you recommend schema additions.

---

*Prepared by Temple Team -- EverydayHoroscope, 2026-05-28*
*For GAI consultation before Phaladeepika decode NLM begins*
