# KE Retroactive Impact Assessment -- Schema Amendment PD1
## Which Already-Decoded Files Need Changes?

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-28
> Based on: Live audit of all decoded JSON files across 6 decode threads
> Commission reference: KE-SCHEMA-AMENDMENT-PD1

---

## Audit Summary

Temple Team ran a programmatic audit of every decoded JSON file across all active KE decode threads before writing this assessment. The findings changed the retroactive picture significantly -- mostly for the better.

**Files audited:**
| Decode Thread | Files | Total Rules |
|---|---|---|
| BPHS Vol 1 De-code | 6 JSON files | ~0 readable (structure mismatch -- see below) |
| LongevityUnnatural_CC_Decode | 7 JSON files | 44 rules |
| ThreeHundredCombinations_CC_Decode | 28 JSON files | 329 rules |
| ThreeHundredHoroscopes_CC_Decode | 5 JSON files | 57 rules |
| KP_CC_Decode | 80+ JSON files | ~200+ rules |
| DestinyNumerology_CC_Decode | 30+ JSON files | ~500+ rules |
| Medical Astrology Ch1 | 1 JSON file | not yet parsed |

---

## Finding 1 -- BPHS Vol 1 JSON Files Are Unreadable by Standard Audit Script

The 6 BPHS JSON files (Ch 27, 34, 40, 41, 43, 44) returned 0 rules from the audit script. This indicates their internal structure uses a non-standard root key -- not `rules` or `interpretation_rules`. They may use a chapter-level wrapper object.

**Retroactive impact:** Cannot be assessed programmatically until the structure is confirmed. However, given that these are the oldest files in the decode pipeline and likely predate the current schema formalization, they should be treated as needing a manual schema alignment check. This is low urgency -- these files feed the dedup comparison for Phaladeepika, not the live rule engine.

**Action:** BPHS Vol 1 decode thread -- confirm the root JSON structure of their output files and align to the standard schema shape before Phaladeepika dedup begins.

---

## Finding 2 -- `claim_axis` Is Unpopulated Across ALL Non-BPHS Decode Threads

**This is the most important finding from the audit.**

Every single rule across LongevityUnnatural, KP, Numerology, 300 Combinations, and 300 Horoscopes has `claim_axis: "?"` (absent/unset). This means **no decoded text has ever populated `claim_axis` correctly** -- it is not a case of some rules having the wrong value, but of the field being universally absent.

This has two implications:

1. **The `claim_axis: "longevity"` amendment is not a "fix" to existing wrong values -- it is a new tagging exercise.** There is nothing to retroactively change in existing files in the sense of replacing wrong values. The field simply needs to be populated, which was always planned but never actioned.

2. **The schema amendment (adding `"longevity"` to the valid enum) is necessary but not sufficient.** A separate data enrichment commission is needed to populate `claim_axis` across all existing files. This is a significant piece of work.

**Retroactive impact on Flag 7 (Longevity):** LOW urgency for the schema amendment itself. The enum addition is clean. The actual `claim_axis` population is a separate, larger exercise that applies to all decode threads, not just longevity-specific ones.

---

## Finding 3 -- Neechabhanga Content in 300 Combinations Uses Non-Standard Types

The 300 Combinations decode has **30 rules that mention Neechabhanga** (rule IDs: combo-intro-014, combo-y001-001, combo-y007-002, combo-y009-001, combo-y021-002 and 25 others).

**Critical finding:** None of these use `condition.type: "yoga_combination"` -- they use custom types like `planetary_position`, `house_occupation_pattern`, `multi_variant`. These are condition types invented by the 300 Combinations decode thread that do not exist in the standard schema.

This means our Flag 5 workaround (encode Neechabhanga as `yoga_combination`) was **never applied to any existing file**. The 300 Combinations thread used its own approach.

**Retroactive impact on Flag 5 (Neechabhanga):** The new `neechabhanga_rule` condition type does not break any existing file, because no existing file uses `yoga_combination` for Neechabhanga. However, the 30 Neechabhanga-mentioning rules in 300 Combinations are encoded with non-standard types that also cannot be evaluated by the rule engine. They need attention, but that is a separate decode-thread alignment issue, not a consequence of the schema amendment.

**Action required:** 300 Combinations decode thread -- identify all Neechabhanga-encoded rules and re-encode using the new `neechabhanga_rule` condition type. Estimated scope: 30 rules.

---

## Finding 4 -- No Existing File Uses `planet: "lagna"` Convention

The Flag 6 workaround (encoding Lagna-sign rules as `planet: "lagna"` in a `planet_in_sign` condition) was never applied to any existing decoded file. Zero files contain this pattern.

**Retroactive impact on Flag 6 (Sign-as-Lagna):** None. The new `lagna_sign` condition type and `natal_lagna` scope are purely forward-looking for Phaladeepika. No existing files need changing.

---

## Finding 5 -- No Upagraha Planets in Any Existing File

No existing decoded file contains planet values of `mandi`, `gulika`, `dhuma`, `vyatipata`, `paridhi`, `indra_dhanus`, or `upaketu`.

**Retroactive impact on Flag 4 (Upagrahas):** None. The planet enum extension is purely forward-looking for Phaladeepika Adhyaya XXV.

---

## Finding 6 -- KP Thread Has a Broken JSON File

```
KP3_ChT04_Role_of_Sub_Rules.json
```
JSON parse error at line 451, column 304 (char 20486): `Expecting ',' delimiter`

This file is currently unreadable. It is included in the KE-SCHEMA-AMENDMENT-PD1 commission for fixing.

**Retroactive impact:** This file's rules are excluded from any rule engine queries until fixed. Unknown how many rules it contains. Fix is included in Deliverable 3 of the schema amendment commission.

---

## Finding 7 -- 11 Longevity-Mentioning Rules in 300 Combinations

11 rules in the 300 Combinations files mention longevity (combo-y001-001, combo-y007-001, combo-y008-001, combo-y055-001, combo-y060-001 and 6 others).

All have `claim_axis: "?"` -- not mislabelled as `health_vitality`, but simply unlabelled.

**Retroactive impact:** These rules need `claim_axis: "longevity"` added as part of the broader claim_axis population exercise. Not an emergency -- the schema amendment adds the valid enum value; the tagging is a data enrichment exercise.

---

## Finding 8 -- KP Thread Has Multiple Longevity-Specific Rules Without `claim_axis`

The KP thread contains rules directly about longevity in:
- `KP3_ChP02_Mode_of_Death_Rules.json` (3 rules -- mode of death)
- `KP3_ChP01_Physical_Features_Rules.json` (4 rules -- longevity references)
- `KP3_ChT10_Constellation_and_Sub_Rules.json` (4 rules -- uses custom type `kp_longevity_factor`)
- `KP3_ChT08_How_to_Judge_Benefic_or_Malefic_Rules.json` (3 rules -- longevity context)
- `KP3_ChT07_Behaviour_of_Planets_Rules.json` (1 rule)
- `KP3_ChP10_Brothers_Sisters_Rules.json` (1 rule)
- `KP3_ChP12_Mother_Rules.json` (2 rules)
- `KP3_ChP19_Disease_Rules.json` (1 rule)
- `KP3_ChP23_Time_of_Marriage_Rules.json` (1 rule)
- `KP3_ChP81_Kendra_Adhipathya_Rules.json` (2 rules)

Also notably: `kp_longevity_factor` is a custom KP-specific condition type used in LongevityUnnatural and KP files -- it is not in the standard schema. This type handles KP's distinctive approach to longevity (using significator houses 1, 8, 3 as longevity houses).

**Retroactive impact:** Once `claim_axis: "longevity"` is a valid enum value, these rules need tagging. The `kp_longevity_factor` custom type also needs a decision: absorb into standard schema or keep as KP-specific extension? Recommend keeping as KP-specific (it is semantically different from the Vedic `neechabhanga_rule` approach).

---

## Finding 9 -- LongevityUnnatural Thread Has All Rules as `engine_specification` With No claim_axis

The entire LongevityUnnatural decode (44 rules across S01-S04) uses `scope: "engine_specification"` and `claim_axis: "?"` across the board. Every rule is a methodology or signification rule -- none are direct outcome-match rules.

This is actually correct for this content type (these are calculation framework rules, not "if Mars in 8th then longevity decreases" outcome rules). The issue is not the schema encoding but the missing `claim_axis`.

**Retroactive impact:** Low. These rules need `claim_axis: "longevity"` tagged, but their scope and condition types are appropriate as-is.

---

## Finding 10 -- 300 Combinations and KP Use Entirely Custom Condition Type Vocabularies

This is the most systemic finding. Neither the 300 Combinations thread nor the KP thread use the standard KE schema condition types. They have invented entirely parallel vocabularies:

**300 Combinations custom types (non-standard):**
`planetary_position`, `house_occupation_pattern`, `multi_variant`, `multi_trigger`, `multi_condition`, `lord_position`, `lord_strength_and_aspect`, `conjunction_or_mutual_aspect`, `absence_condition`, `cancellation_condition`, `navamsa_based_condition`, `sign_type_condition`, `strength_qualifier`, `strength_modifier`, `planet_condition_modifier`, `planet_in_own_or_exaltation_kendra`, `exaltation_plus_parivartana`, `conjunction_with_distance_qualifier`, `lord_exaltation_plus_conjunction`, `house_modifier`, `planet_nature_modifier`, `transit_condition`

**KP custom types (non-standard):**
`kp_significator`, `kp_sub_lord`, `kp_badhaka`, `kp_longevity_factor`, `planet_conjunction`, `planet_in_house`, `planet_in_sign` (these last two ARE standard)

**This is a separate schema harmonization issue** -- not caused by the PD1 schema amendment, and not something this commission should address. It requires a dedicated cross-thread schema alignment exercise. However it should be noted:

1. The rule engine cannot evaluate rules with non-standard condition types
2. These files exist but are essentially not matchable by the current engine
3. Some of the 300 Combinations types are arguably better than the standard types for their content (e.g., `multi_variant` for rules with multiple valid configurations)

**Retroactive impact on PD1 schema amendment:** None. The new condition types added by PD1 do not conflict with any existing custom types. PD1 is purely additive.

---

## Retroactive Action Plan

### Immediate (before Phaladeepika NLM begins)

| Action | Who | Files affected |
|---|---|---|
| Fix JSON parse error in `KP3_ChT04_Role_of_Sub_Rules.json` | Codex KE thread (via PD1 commission) | 1 file |
| Confirm BPHS Vol 1 JSON root structure | BPHS Vol 1 decode thread | 6 files |

### Short-term (after PD1 schema amendment is delivered and Phaladeepika decode is underway)

| Action | Who | Files affected | Est. scope |
|---|---|---|---|
| Re-encode 30 Neechabhanga rules in 300 Combinations to `neechabhanga_rule` type | 300 Combinations decode thread | 5-8 files | 30 rules |
| Populate `claim_axis: "longevity"` on KP longevity rules | KP decode thread | ~10 files | ~20 rules |
| Populate `claim_axis: "longevity"` on LongevityUnnatural rules | LongevityUnnatural decode thread | 4 files | 44 rules |
| Populate `claim_axis: "longevity"` on 300 Combinations longevity rules | 300 Combinations decode thread | ~5 files | 11 rules |

### Medium-term (Phase 2 planning)

| Action | Who | Note |
|---|---|---|
| Schema harmonization -- align 300 Combinations and KP custom types to standard vocabulary | Dedicated cross-thread commission | Large exercise -- requires systematic review of all ~529 rules with non-standard types |
| Populate `claim_axis` across ALL decoded texts | All decode threads | Universal gap -- no text has claim_axis populated |
| BPHS Vol 1 JSON structure alignment | BPHS Vol 1 decode thread | After BPHS Vol 1 decode completes |

---

## Summary: What Is NOT Broken by the Schema Amendment

To be clear on what the PD1 schema amendment does NOT break:

- All existing rules with standard condition types (`planet_in_house`, `planet_in_sign`, `yoga_combination`, `engine_specification`, etc.) are unaffected -- PD1 adds new types, does not modify existing ones
- All existing rules with standard scope values (`natal`, `transit`, `dasha`) are unaffected
- All existing planet values (`sun` through `ketu`) are unaffected
- The custom condition types in KP and 300 Combinations are not touched
- No JSON file content is modified by the schema amendment itself

**The schema amendment is purely additive. Zero breaking changes to existing decoded content.**

---

*Prepared by Temple Team -- EverydayHoroscope, 2026-05-28*
