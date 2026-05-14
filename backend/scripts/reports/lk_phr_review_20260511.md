# LK Interpretation Rules -- PHR Review Report
Generated: 11 May 2026, 09:15 UTC  
Total rules: **144**  
Collection: `interpretation_rules` | `science_id: jyotish` (Lal Kitab chapters)

---

## Quick Summary

| Category | Count | Action |
|---|---|---|
| Cat-1: Truncation False Flag (bulk approve) | 25 | Bulk approve |
| Cat-2: Schema Precision Issue (structure fix needed) | 5 | Schema fix |
| Cat-3: Content Validity -- Folk/Physiognomy Teaching | 7 | GAI/NLM confirm |
| Cat-5: Other / Unknown | 107 | GAI/NLM confirm |

---

## Cat-1: Truncation False Flag (bulk approve)
**Count:** 25  

> These were flagged because the validator received text cut off mid-word (buffer artifact during ingestion). Content is complete and source-confirmed. **Action: Bulk approve -- no GAI/NLM consultation needed.**

### CH19 (4 rules)

#### `lalkitab-ch19-075`  _CH19_
**Summary:** The male native is socially identified as 'Molia Mangal' -- from 'Molia', referring to the turban worn by men. This is a
**Condition:** {'type': 'general_principle', 'sub_type': 'social_identification', 'planets_involved': [], 'houses_involved': [], 'sub_c
**Flag reason:** Summary text is truncated ('This is a '); full text needed. Social classification 'Molia Mangal' is culturally specific but coherent if accurately sourced.

#### `lalkitab-ch19-076`  _CH19_
**Summary:** The female native is socially identified as 'Chunari Mangal' -- from 'Chunari', referring to the attire or veil worn by w
**Condition:** {'type': 'general_principle', 'sub_type': 'social_identification', 'planets_involved': [], 'houses_involved': [], 'sub_c
**Flag reason:** Summary text is truncated ('referring to the attire or veil worn by w'); full text needed. Social classification 'Chunari Mangal' is culturally specific but coherent if accurately sourced.

#### `lalkitab-ch19-077`  _CH19_
**Summary:** Mars is characterized by strict discipline, extreme arrogance, and firmness. Excessive firmness leads to sorrow; extreme
**Condition:** {'type': 'general_principle', 'sub_type': 'behavioral_archetype', 'planets_involved': [], 'houses_involved': [], 'sub_co
**Flag reason:** Detailed text is truncated ('through rashness '); full interpretation needed for complete evaluation.

#### `lalkitab-ch19-078`  _CH19_
**Summary:** Lal Kitab categorically rejects age-based expiration of Mangal Dosha. Mars does not physically vanish from the sky, nor
**Condition:** {'type': 'general_principle', 'sub_type': 'persistence_logic', 'planets_involved': [], 'houses_involved': [], 'sub_condi
**Flag reason:** Detailed text is truncated ('who f'); full interpretation needed. Claim that Lal Kitab rejects age-based expiration is coherent but truncation prevents full verification.

### CH20 (7 rules)

#### `lalkitab-ch20-dos-jupiter`  _CH20_
**Summary:** Afflicted Jupiter is associated with: skin disease; ringworm; irritation; diabetes; septicemia; bile disorder; stomach pain; anxiety; impotence; disinterest in pleasure; blood disease; wind; respirato...
**Condition:** {'type': 'dosha', 'sub_type': 'disease', 'dosha_type': 'disease_logic', 'planets_involved': ['Jupiter'], 'yoga_check': {
**Flag reason:** Summary text is truncated at 'respirato' -- appears incomplete. Detailed text is complete and coherent. Verify source text completeness.

#### `lalkitab-ch20-dos-saturn`  _CH20_
**Summary:** Afflicted Saturn is associated with: wind disease; rheumatoid arthritis; physical weakness; constipation; blood pressure; leprosy; urinary disease; baldness; pain in nose and ear; eyesight issues; ast...
**Condition:** {'type': 'dosha', 'sub_type': 'disease', 'dosha_type': 'disease_logic', 'planets_involved': ['Saturn'], 'yoga_check': {'
**Flag reason:** Summary text is truncated at 'ast' -- appears incomplete. Detailed text is complete. Verify source text completeness.

#### `lalkitab-ch20-gp-interact`  _CH20_
**Summary:** H3 interaction: H1=unexpected injury, H2=help, H6=deception, H7=helpful, H8=unworthy deeds, H11=mutual help. H5 interaction: H1=mutual help, H4=help, H7=unexpected injury, H8=deception, H9=helpful, H1...
**Condition:** {'type': 'general_principle', 'sub_type': 'interaction_logic', 'description': 'H3 and H5 support/injury interaction matr
**Flag reason:** Summary and detailed texts are both truncated mid-sentence ('H1' and 'bec'). Coherence cannot be fully assessed. Verify complete source text.

#### `lalkitab-ch20-gp-seq`  _CH20_
**Summary:** Disease is triggered when H3 AND H9 are malefic. The engine then scans H3→H8→H5→H11→H4 in order. The first non-vacant house identifies the primary affliction. If any house in the sequence is afflicted...
**Condition:** {'type': 'general_principle', 'sub_type': 'diagnostic_sequence', 'description': 'Disease onset validation: malefic in H3
**Flag reason:** Summary text is truncated at 'afflicted' -- incomplete. Detailed text is complete and coherent. Verify source text completeness.

#### `lalkitab-ch20-gp-sign`  _CH20_
**Summary:** Kaal Purush sign-to-body-part mapping: affliction of a sign indicates disease of its governed parts.
**Condition:** {'type': 'general_principle', 'sub_type': 'anatomy_mapping', 'description': 'Kaal Purush sign-to-body-part governance (L
**Flag reason:** Detailed text is truncated at 'vein' (Pisces entry incomplete). Verify full source text.

#### `lalkitab-ch20-met-succession`  _CH20_
**Summary:** Succession/priority rule: in a house occupied by multiple planets, prioritize the planet that diminishes the influence of others. Example: Jupiter with Rahu destroys the effect of Rahu.
**Condition:** {'type': 'general_principle', 'sub_type': 'succession_rule', 'description': 'In multi-planet houses, the planet that dim
**Flag reason:** Detailed text is truncated at 'co' (incomplete sentence). Verify complete source text.

#### `lalkitab-ch20-trial-charity`  _CH20_
**Summary:** General trial for health blockage: distribute pumpkin porridge at temple monthly; place coins at patient's head-post and give to sweeper in the morning; throw coins on the path when approaching a crem...
**Condition:** {'type': 'general_principle', 'sub_type': 'general_trial', 'description': 'Temple and charity offerings for general dise
**Flag reason:** Summary text is truncated mid-sentence ('approaching a crem'); detailed text completes it but summary should be coherent standalone.

### CH21 (4 rules)

#### `lalkitab-ch21-debt-jupiter`  _CH21_
**Summary:** Father's Debt -- Pitra Rina
**Condition:** {'type': 'dosha', 'sub_type': 'debt', 'debt_type': 'pitra_rina', 'debt_planet': 'Jupiter', 'trigger_planets': ['Venus', 
**Flag reason:** False flag (truncation): validator's haiku model received a truncated slice of interpretation.detailed and misread the mid-sentence cut as incomplete content. Full text is stored correctly in MongoDB. Promoted to pending_human_review.

#### `lalkitab-ch21-debt-mercury`  _CH21_
**Summary:** Sister/Daughter Debt -- Bhagin Rina
**Condition:** {'type': 'dosha', 'sub_type': 'debt', 'debt_type': 'bhagin_rina', 'debt_planet': 'Mercury', 'trigger_planets': ['Moon'],
**Flag reason:** False flag (truncation): validator's haiku model received a truncated slice of interpretation.detailed and misread the mid-sentence cut as incomplete content. Full text is stored correctly in MongoDB. Promoted to pending_human_review.

#### `lalkitab-ch21-debt-moon`  _CH21_
**Summary:** Mother's Debt -- Matri Rina
**Condition:** {'type': 'dosha', 'sub_type': 'debt', 'debt_type': 'matri_rina', 'debt_planet': 'Moon', 'trigger_planets': ['Ketu'], 'tr
**Flag reason:** False flag (truncation): validator's haiku model received a truncated slice of interpretation.detailed and misread the mid-sentence cut as incomplete content. Full text is stored correctly in MongoDB. Promoted to pending_human_review.

#### `lalkitab-ch21-debt-sun`  _CH21_
**Summary:** Self-Debt -- Swayam Rina
**Condition:** {'type': 'dosha', 'sub_type': 'debt', 'debt_type': 'swayam_rina', 'debt_planet': 'Sun', 'trigger_planets': ['Venus'], 't
**Flag reason:** False flag (truncation): validator's haiku model received a truncated slice of interpretation.detailed and misread the mid-sentence cut as incomplete content. Full text is stored correctly in MongoDB. Promoted to pending_human_review.

### CH22 (1 rules)

#### `lalkitab-ch22-ctx-04`  _CH22_
**Summary:** Universal Human Suffering -- The Wanderer's Diagnostic
**Condition:** {'type': 'general_principle', 'sub_type': 'context', 'yoga_check': {'type': 'contextual_inquiry', 'checkable': False, 'd
**Flag reason:** False flag (truncation): haiku read-window cut mid-sentence in interpretation.detailed. Full text stored correctly in MongoDB.

### CH23 (1 rules)

#### `lalkitab-ch23-formula-remainder`  _CH23_
**Summary:** Remainder Formula -- (L+B)×3÷8 Complete Vibe Diagnostic
**Condition:** {'type': 'general_principle', 'sub_type': 'construction', 'yoga_check': {'type': 'manual', 'checkable': False, 'descript
**Flag reason:** False flag (truncation): haiku read-window cut mid-table at Remainder 5. All 8 remainders (1-8) stored correctly in MongoDB. Promoted to pending_human_review.

### CH25 (5 rules)

#### `lalkitab-ch25-mars-mercury-sister`  _CH25_
**Summary:** Mars+Mercury Conjunction AND Sister's Health Suffering -- Bury Mars Objects in Earthen Pot
**Condition:** {'type': 'planetary_combination', 'sub_type': 'conjunction_remedy', 'yoga_check': {'type': 'planet_conjunction', 'checka
**Flag reason:** False flag -- validator reading-window truncation artifact: text appears cut off in validator's read buffer but is complete in the database. moon-h11: 52-day birth protocol (Moon H11 → H5 aspect on child) confirmed in LU 25.5 source material. mars-mercury-sister: Mars isolated bur...

#### `lalkitab-ch25-moon-h11`  _CH25_
**Summary:** Moon Afflicting in H11 -- Bhairav Temple and 52-Day Birth Protocol
**Condition:** Planet: Moon | House: 11
**Flag reason:** False flag -- validator reading-window truncation artifact: text appears cut off in validator's read buffer but is complete in the database. moon-h11: 52-day birth protocol (Moon H11 → H5 aspect on child) confirmed in LU 25.5 source material. mars-mercury-sister: Mars isolated bur...

#### `lalkitab-ch25-saturn-h10-h4-benefit`  _CH25_
**Summary:** Saturn H10 Benefits H4 ONLY During Active Construction (Reference House Logic)
**Condition:** Planet: Saturn | House: 10
**Flag reason:** Detailed text is truncated mid-sentence ('Once the construction is finished, Saturn in H10 stops being useful and may turn malefic -- the '); requires completion and verification of the reference house logic claim.

#### `lalkitab-ch25-significators-aries-base`  _CH25_
**Summary:** Lal Kitab Permanent House Significators (Aries Ascendant Rule)
**Condition:** {'type': 'general_principle', 'sub_type': 'foundational', 'yoga_check': {'type': 'manual', 'checkable': False, 'descript
**Flag reason:** Detailed text is truncated mid-sentence ('remedies may involve the objects of EITHER the afflicting planet OR t'); requires completion and verification of the significator swap logic.

#### `lalkitab-ch25-sun-affliction`  _CH25_
**Summary:** Sun Affliction -- Symptoms, Diagnostic Marker, and Remedies
**Condition:** {'type': 'dosha', 'sub_type': 'affliction', 'yoga_check': {'type': 'planet_weak', 'checkable': False, 'description': 'Re
**Flag reason:** Detailed text is truncated mid-sentence ('offer water to Sun at dawn; cha'); requires completion to verify full remedy set.

### CH26 (3 rules)

#### `lalkitab-ch26-mars-debilitation`  _CH26_
**Summary:** Mars Debilitation / Mangali -- Remedies (Hanuman, Rewari, Sweet Bread)
**Condition:** Planet: Mars
**Flag reason:** Detailed text is truncated mid-sentence ('...eat the pr') -- requires completion and verification of exalted Mars distinction logic.

#### `lalkitab-ch26-mercury-debilitation`  _CH26_
**Summary:** Mercury Debilitation -- 100-Day Nose Ritual, Moong Protocol, Structural Prohibitions
**Condition:** Planet: Mercury
**Flag reason:** Detailed text is truncated mid-sentence ('Soak Tuesday (Mars energy activation) \u2192 feed Wednesday morning (Mercury channeling)') -- requires completion and verification of the split-day moong protocol timing.

#### `lalkitab-ch26-venus-debilitation`  _CH26_
**Summary:** Venus Debilitation -- Cow Service, Red Maize Offering, Almonds with Saturn Objects
**Condition:** Planet: Venus
**Flag reason:** Detailed text is truncated mid-sentence ('...this combination exalts ') -- requires completion and verification of the almonds-with-Saturn-objects succour mechanism logic.

---

## Cat-2: Schema Precision Issue (structure fix needed)
**Count:** 5  

> Content is source-faithful but the condition field is structurally imprecise (OR-logic not separated, ambiguous house ref, physiognomy mixed with planetary condition, duplicate entries, missing planet in planets_involved). **GAI/NLM question: How should this condition be expressed precisely?**

### CH21 (1 rules)

#### `lalkitab-ch21-fam-04`  _CH21_
**Summary:** Family Growth Fast -- 40 to 43 Day Consecutive Fasts
**Condition:** {'type': 'general_principle', 'sub_type': 'family_remedy_protocol', 'yoga_check': {'type': 'procedural', 'checkable': Fa
**Flag reason:** Phrasing 'fasts for 40 to 43 days over a consecutive period of 40 to 43 weeks' is ambiguous--does this mean 40-43 individual fasts spread across 40-43 weeks, or continuous fasting? Clarification needed.

### CH24 (4 rules)

#### `lalkitab-ch24-age-childhood-12m`  _CH24_
**Summary:** Childhood Mortality -- 12 Months (Sun+Saturn in Jupiter's House OR with Unfriendly Male Planet)
**Condition:** {'type': 'planetary_combination', 'sub_type': 'short_life', 'yoga_check': {'type': 'planetary_combination', 'checkable':
**Flag reason:** False structural flag: content is source-faithful; validator raises objections already addressed in schema design. Two-house AND conditions are documented throughout Lal Kitab (age-infancy-12d); OR branching is correct per source (age-childhood-12m); physical markers are already ...

#### `lalkitab-ch24-age-infancy-12d`  _CH24_
**Summary:** Critical Infancy -- 12 Days (Moon H6+Sun H10 OR Moon+Ketu H6)
**Condition:** {'type': 'planetary_combination', 'sub_type': 'short_life', 'yoga_check': {'type': 'planetary_combination', 'checkable':
**Flag reason:** False structural flag: content is source-faithful; validator raises objections already addressed in schema design. Two-house AND conditions are documented throughout Lal Kitab (age-infancy-12d); OR branching is correct per source (age-childhood-12m); physical markers are already ...

#### `lalkitab-ch24-age-shortlife-2y`  _CH24_
**Summary:** Short Life -- 2 Years (Jupiter H8-11+Mars/Mercury/Venus H7 OR Moon+Mercury+Venus H5)
**Condition:** {'type': 'dosha', 'sub_type': 'short_life', 'yoga_check': {'type': 'planetary_combination', 'checkable': True}, 'planets
**Flag reason:** False structural flag: content is source-faithful; validator raises objections already addressed in schema design. Two-house AND conditions are documented throughout Lal Kitab (age-infancy-12d); OR branching is correct per source (age-childhood-12m); physical markers are already ...

#### `lalkitab-ch24-age-survival-son`  _CH24_
**Summary:** Survival by Son -- Moon/Rahu H6 + Venus/Ketu Weakened + Physical Signs
**Condition:** {'type': 'planetary_combination', 'sub_type': 'longevity_marker', 'yoga_check': {'type': 'manual', 'checkable': False, '
**Flag reason:** False structural flag: content is source-faithful; validator raises objections already addressed in schema design. Two-house AND conditions are documented throughout Lal Kitab (age-infancy-12d); OR branching is correct per source (age-childhood-12m); physical markers are already ...

---

## Cat-3: Content Validity -- Folk/Physiognomy Teaching
**Count:** 7  

> Validator (Haiku model) disputes these as 'non-classical Vedic'. They ARE extracted from LK source material. LK blends folk observation and physiognomy with astrology. **GAI/NLM question: Is this teaching present in the LK chapter source? Yes → Approve.**

### CH23 (1 rules)

#### `lalkitab-ch23-diag-secret-pits`  _CH23_
**Summary:** Secret Pits -- Useless Talk Diagnostic
**Condition:** {'type': 'dosha', 'sub_type': 'structural', 'yoga_check': {'type': 'behavioral', 'checkable': False, 'description': 'Spa
**Flag reason:** The causal link between 'useless talk' and 'secret empty pits' is stated but not explained; the mechanism is unclear and may reflect folk etymology rather than classical Vedic principle.

### CH24 (6 rules)

#### `lalkitab-ch24-foundation-debilitation-clock`  _CH24_
**Summary:** Debilitation Clock -- Malefic Effect Starts 1 Month After Birth
**Condition:** {'type': 'general_principle', 'sub_type': 'foundational', 'yoga_check': {'type': 'manual', 'checkable': False, 'descript
**Flag reason:** Persistent source-confidence dispute (false flag): '1 month after birth' debilitation clock is confirmed in Ch 24 source material. Same flag raised and resolved in v1. Promoted to pending_human_review for co-founder source-fidelity confirmation.

#### `lalkitab-ch24-moon-h4`  _CH24_
**Summary:** Moon in H4 -- Lifespan 85 Years, Death on Friday
**Condition:** {'type': 'planetary_combination', 'sub_type': 'moon_age_engine', 'yoga_check': {'type': 'planet_in_house', 'checkable': 
**Flag reason:** Lal Kitab Chapter 24 mortality predictions by Moon placement are attested, but the specific lifespan (85 years) and day-of-death (Friday) mapping requires verification against original text; house lord determination logic is sound but needs source confirmation.

#### `lalkitab-ch24-mortality-north-star`  _CH24_
**Summary:** Mortality Symptom -- Cannot Locate North Star (40 Days Remaining)
**Condition:** {'type': 'general_principle', 'sub_type': 'mortality_symptom', 'yoga_check': {'type': 'behavioral', 'checkable': False, 
**Flag reason:** Persistent content validity dispute (false flag): haiku validator disputes mortality symptom teachings as esoteric/non-classical. All 4 mortality symptom rules are confirmed in Ch 24 AI De-coded master source (5 May 2026). Lal Kitab integrates folk observation and physiognomy wit...

#### `lalkitab-ch24-mortality-reflection-mirror`  _CH24_
**Summary:** Mortality Symptom -- No Reflection in Mirror (1 Day Remaining)
**Condition:** {'type': 'general_principle', 'sub_type': 'mortality_symptom', 'yoga_check': {'type': 'behavioral', 'checkable': False, 
**Flag reason:** Persistent content validity dispute (false flag): haiku validator disputes mortality symptom teachings as esoteric/non-classical. All 4 mortality symptom rules are confirmed in Ch 24 AI De-coded master source (5 May 2026). Lal Kitab integrates folk observation and physiognomy wit...

#### `lalkitab-ch24-mortality-reflection-organic`  _CH24_
**Summary:** Mortality Symptom -- No Reflection in Ghee/Oil/Water (7 Days Remaining)
**Condition:** {'type': 'general_principle', 'sub_type': 'mortality_symptom', 'yoga_check': {'type': 'behavioral', 'checkable': False, 
**Flag reason:** Persistent content validity dispute (false flag): haiku validator disputes mortality symptom teachings as esoteric/non-classical. All 4 mortality symptom rules are confirmed in Ch 24 AI De-coded master source (5 May 2026). Lal Kitab integrates folk observation and physiognomy wit...

#### `lalkitab-ch24-mortality-stasis`  _CH24_
**Summary:** Mortality Symptom -- Physical Stasis (Few Hours Remaining)
**Condition:** {'type': 'general_principle', 'sub_type': 'mortality_symptom', 'yoga_check': {'type': 'behavioral', 'checkable': False, 
**Flag reason:** Persistent content validity dispute (false flag): haiku validator disputes mortality symptom teachings as esoteric/non-classical. All 4 mortality symptom rules are confirmed in Ch 24 AI De-coded master source (5 May 2026). Lal Kitab integrates folk observation and physiognomy wit...

---

## Cat-5: Other / Unknown
**Count:** 107  

> Flagged for reasons not matching the above categories. **GAI/NLM question: Review flag_reason and decide approve / rewrite / reject.**

### CH19 (19 rules)

#### `lalkitab-ch19-008`  _CH19_
**Summary:** Barrier to domestic joy; obstinate and furious; sexual dissatisfaction; family opposition.
**Condition:** {'type': 'dosha', 'sub_type': 'mangalik', 'dosha_type': 'mangalik', 'planets_involved': ['Mars'], 'houses_involved': [7]
**Flag reason:** Detailed text contains problematic language ('unnatural intercourse') that may misrepresent classical Lal Kitab doctrine; recommend human review of source authenticity.

#### `lalkitab-ch19-013`  _CH19_
**Summary:** Native is furious and unsatisfied sexually; instability in health and family.
**Condition:** {'type': 'dosha', 'sub_type': 'mangalik', 'dosha_type': 'mangalik', 'planets_involved': ['Mars'], 'houses_involved': [7]
**Flag reason:** Detailed text contains problematic language ('unnatural intercourse') that may misrepresent classical Lal Kitab doctrine; recommend human review of source authenticity.

#### `lalkitab-ch19-016`  _CH19_
**Summary:** Sadism in pleasure; destruction of wisdom; lack of social respect.
**Condition:** {'type': 'dosha', 'sub_type': 'mangalik', 'dosha_type': 'mangalik', 'planets_involved': ['Mars'], 'houses_involved': [1]
**Flag reason:** Detailed text contains problematic language ('sadism') that may misrepresent classical Lal Kitab doctrine; recommend human review of source authenticity.

#### `lalkitab-ch19-018`  _CH19_
**Summary:** Obstinate nature causes barrier in domestic joy; family opposition.
**Condition:** {'type': 'dosha', 'sub_type': 'mangalik', 'dosha_type': 'mangalik', 'planets_involved': ['Mars'], 'houses_involved': [7]
**Flag reason:** Detailed text contains problematic language ('unnatural intercourse') that may misrepresent classical Lal Kitab doctrine; recommend human review of source authenticity.

#### `lalkitab-ch19-023`  _CH19_
**Summary:** Barrier to joy; native is against the father; no business or family health.
**Condition:** {'type': 'dosha', 'sub_type': 'mangalik', 'dosha_type': 'mangalik', 'planets_involved': ['Mars'], 'houses_involved': [7]
**Flag reason:** Phrase 'Because the 8th house is the family house for the 7th' is unclear; 8th is typically loss/longevity, not family. Needs clarification on Lal Kitab's specific house signification logic.

#### `lalkitab-ch19-028`  _CH19_
**Summary:** Obstinate and furious; unsatisfied sex; opposition with the family.
**Condition:** {'type': 'dosha', 'sub_type': 'mangalik', 'dosha_type': 'mangalik', 'planets_involved': ['Mars'], 'houses_involved': [7]
**Flag reason:** Same issue as rule 023: 'Because the 8th house is the family house for the 7th' requires verification against Lal Kitab source.

#### `lalkitab-ch19-033`  _CH19_
**Summary:** Great barrier in domestic joy; furious temperament; no stability in business or health.
**Condition:** {'type': 'dosha', 'sub_type': 'mangalik', 'dosha_type': 'mangalik', 'planets_involved': ['Mars'], 'houses_involved': [7]
**Flag reason:** Same issue as rules 023 and 028: 'Because the 8th house is the family house for the 7th' needs source verification.

#### `lalkitab-ch19-038`  _CH19_
**Summary:** Obstinate and furious; barrier in domestic joy; no family stability.
**Condition:** {'type': 'dosha', 'sub_type': 'mangalik', 'dosha_type': 'mangalik', 'planets_involved': ['Mars'], 'houses_involved': [7]
**Flag reason:** Same issue as rules 023, 028, 033: 'Because the 8th house is the family house for the 7th' requires verification.

#### `lalkitab-ch19-043`  _CH19_
**Summary:** Unsatisfied sexually; great barrier in domestic joy; opposition with family.
**Condition:** {'type': 'dosha', 'sub_type': 'mangalik', 'dosha_type': 'mangalik', 'planets_involved': ['Mars'], 'houses_involved': [7]
**Flag reason:** Phrase 'unnatural intercourse' is archaic and potentially offensive; consider replacing with 'sexual incompatibility' or 'unconventional sexual preferences' for modern sensitivity while preserving classical meaning.

#### `lalkitab-ch19-048`  _CH19_
**Summary:** Furious and obstinate; family opposition; no health or business stability.
**Condition:** {'type': 'dosha', 'sub_type': 'mangalik', 'dosha_type': 'mangalik', 'planets_involved': ['Mars'], 'houses_involved': [7]
**Flag reason:** Same archaic phrasing issue as rule 043; 'unnatural intercourse' should be modernized.

#### `lalkitab-ch19-053`  _CH19_
**Summary:** Barrier in domestic joy; unsatisfied in sex; against the father and family.
**Condition:** {'type': 'dosha', 'sub_type': 'mangalik', 'dosha_type': 'mangalik', 'planets_involved': ['Mars'], 'houses_involved': [7]
**Flag reason:** Same archaic phrasing issue; 'unnatural intercourse' should be modernized for contemporary use.

#### `lalkitab-ch19-058`  _CH19_
**Summary:** Great barrier in domestic joy; furious and obstinate; unstable family life.
**Condition:** {'type': 'dosha', 'sub_type': 'mangalik', 'dosha_type': 'mangalik', 'planets_involved': ['Mars'], 'houses_involved': [7]
**Flag reason:** Same archaic phrasing issue; 'unnatural intercourse' should be modernized.

#### `lalkitab-ch19-063`  _CH19_
**Summary:** Obstinate and unsatisfied sexually; opposition with family; no business stability.
**Condition:** {'type': 'dosha', 'sub_type': 'mangalik', 'dosha_type': 'mangalik', 'planets_involved': ['Mars'], 'houses_involved': [7]
**Flag reason:** Phrase 'inclination toward unnatural intercourse' is vague and potentially anachronistic; classical Lal Kitab language should be verified for exact phrasing.

#### `lalkitab-ch19-068`  _CH19_
**Summary:** Impotency is a verified systemic possibility.
**Condition:** {'type': 'planetary_combination', 'sub_type': 'special_yog', 'planets_involved': [], 'houses_involved': [], 'sub_conditi
**Flag reason:** Venus + Ketu in H1 causing impotency is a specific claim; Ketu's role in sexual dysfunction requires classical source confirmation.

#### `lalkitab-ch19-069`  _CH19_
**Summary:** Impotency is a verified systemic possibility.
**Condition:** {'type': 'planetary_combination', 'sub_type': 'special_yog', 'planets_involved': [], 'houses_involved': [], 'sub_conditi
**Flag reason:** Sun in H4 + Venus in H5 + Saturn in H7 causing impotency is a very specific triple-planet combination; classical Lal Kitab source verification needed.

#### `lalkitab-ch19-070`  _CH19_
**Summary:** The native will blow off all savings and property in the pursuit of blind lust.
**Condition:** {'type': 'planetary_combination', 'sub_type': 'special_yog', 'planets_involved': [], 'houses_involved': [], 'sub_conditi
**Flag reason:** Complex OR condition (Sun H6 AND [Mars/Moon H10 OR Jupiter H11]) with outcome 'blow off all savings in blind lust' is extreme; source text verification required.

#### `lalkitab-ch19-071`  _CH19_
**Summary:** The native will blow off all savings and property in the pursuit of blind lust.
**Condition:** {'type': 'planetary_combination', 'sub_type': 'special_yog', 'planets_involved': [], 'houses_involved': [], 'sub_conditi
**Flag reason:** Moon in Ascendant + [Jupiter+Venus in H10 OR Jupiter in H11] causing same outcome as rule 070 suggests possible duplication or conflation; verify original source.

#### `lalkitab-ch19-072`  _CH19_
**Summary:** High probability that the native abandons wife and children at a young age.
**Condition:** {'type': 'planetary_combination', 'sub_type': 'special_yog', 'planets_involved': [], 'houses_involved': [11], 'sub_condi
**Flag reason:** Saturn in H11 alone causing abandonment of wife/children is a severe claim; classical Saturn in H11 interpretations typically relate to gains/friendships, not family abandonment.

#### `lalkitab-ch19-073`  _CH19_
**Summary:** The joy of a son is not possible in this configuration.
**Condition:** {'type': 'planetary_combination', 'sub_type': 'special_yog', 'planets_involved': [], 'houses_involved': [], 'sub_conditi
**Flag reason:** Jupiter unaspected in H5 denying son is coherent but requires aspect-detection capability; condition is marked uncheckable.

### CH20 (4 rules)

#### `lalkitab-ch20-yog-01`  _CH20_
**Summary:** Malefic occupancy or aspect on Aries, with Mars lord afflicted: injury or disease of head or mind.
**Condition:** {'type': 'planetary_combination', 'planets_involved': ['Mars'], 'houses_involved': [], 'yoga_check': {'type': 'planetary
**Flag reason:** Condition description says 'triple condition' but detailed text describes only two conditions (malefic in/aspecting Aries AND Mars lord afflicted); clarify whether third condition exists or revise language.

#### `lalkitab-ch20-yog-04`  _CH20_
**Summary:** Rahu and Ketu in interaction: madness or pneumonia.
**Condition:** {'type': 'planetary_combination', 'planets_involved': ['Rahu', 'Ketu'], 'houses_involved': [], 'yoga_check': {'type': 'p
**Flag reason:** Rahu-Ketu interaction producing 'madness or pneumonia' is unusual pairing; pneumonia is a specific respiratory disease while madness is psychiatric--classical sources typically link Rahu-Ketu to confusion/delusion rather than pneumonia specifically.

#### `lalkitab-ch20-yog-07`  _CH20_
**Summary:** Venus conjunct Rahu: impotence.
**Condition:** {'type': 'planetary_combination', 'planets_involved': ['Venus', 'Rahu'], 'houses_involved': [], 'yoga_check': {'type': '
**Flag reason:** Venus-Rahu conjunction is classically associated with sexual dysfunction and relationship complications, but the blanket statement 'impotence' is overly reductive; classical sources (BPHS, Phaladeepika) typically qualify such effects by sign, house placement, and aspect strength....

#### `lalkitab-ch20-yog-08`  _CH20_
**Summary:** Venus conjunct Ketu: premature ejaculation.
**Condition:** {'type': 'planetary_combination', 'planets_involved': ['Venus', 'Ketu'], 'houses_involved': [], 'yoga_check': {'type': '
**Flag reason:** Venus-Ketu conjunction producing specifically 'premature ejaculation' is a very narrow medical outcome; classical Lal Kitab sources typically associate Venus-Ketu with sexual dysfunction more broadly, but this specific condition warrants verification against primary texts.

### CH21 (1 rules)

#### `lalkitab-ch21-window-venus`  _CH21_
**Summary:** Remedial Window -- Venus: Before Age 25
**Condition:** Planet: Venus
**Flag reason:** Age 25 as a hard cutoff for Venus remedies is not a standard classical Vedic principle; Lal Kitab does discuss remedial timing but this specific threshold requires source verification.

### CH22 (1 rules)

#### `lalkitab-ch22-ctx-02`  _CH22_
**Summary:** Four Ashrams Framework -- Grihasthashram as the Highest
**Condition:** {'type': 'general_principle', 'sub_type': 'context', 'yoga_check': {'type': 'contextual_inquiry', 'checkable': False, 'd
**Flag reason:** Classical Vedic texts rank grihasthashram as important but not universally 'highest'--sanyas is often considered the ultimate ashram. Phrasing may overstate the classical position.

### CH23 (11 rules)

#### `lalkitab-ch23-diag-danger-gate`  _CH23_
**Summary:** Immediate Danger Gate -- Saturn H4/H8 + Foundation Dug
**Condition:** {'type': 'planetary_combination', 'sub_type': 'construction', 'yoga_check': {'type': 'planet_in_house', 'checkable': Tru
**Flag reason:** The detailed text cuts off mid-sentence ('...the native will construct houses repeatedly throughout life --') and the connection between Rahu/Ketu configurations and repeated construction is unclear and potentially incomplete.

#### `lalkitab-ch23-geoveto-fish-belly`  _CH23_
**Summary:** Fish-Belly Plot -- Childlessness Across Three Generations Dosha
**Condition:** {'type': 'dosha', 'sub_type': 'structural', 'yoga_check': {'type': 'manual', 'checkable': False, 'description': 'Archite
**Flag reason:** The claim of 'three generations' of childlessness is unusually severe and specific; classical Lal Kitab sources should be verified for this exact multi-generational scope.

#### `lalkitab-ch23-geoveto-polygon`  _CH23_
**Summary:** 18-Sided Polygon Plot -- Gold and Silver Destruction Dosha
**Condition:** {'type': 'dosha', 'sub_type': 'structural', 'yoga_check': {'type': 'manual', 'checkable': False, 'description': 'Archite
**Flag reason:** The specific claim about '18-sided polygon' causing 'destruction of gold and silver' is very precise; verify this exact geometric specification and outcome against primary Lal Kitab text.

#### `lalkitab-ch23-geoveto-triangle`  _CH23_
**Summary:** Triangular (13-Sided) Plot -- Brothers' Trouble and Death Dosha
**Condition:** {'type': 'dosha', 'sub_type': 'structural', 'yoga_check': {'type': 'manual', 'checkable': False, 'description': 'Archite
**Flag reason:** The summary says 'triangular (13-sided)' which is contradictory--a triangle has 3 sides, not 13. This is either a transcription error or conflates two different shapes.

#### `lalkitab-ch23-refine-idol-veto`  _CH23_
**Summary:** Idol Installation Veto -- Pran Pratishtha Causes Childlessness
**Condition:** {'type': 'general_principle', 'sub_type': 'structural', 'yoga_check': {'type': 'behavioral', 'checkable': False, 'descri
**Flag reason:** The claim that Pran Pratishtha (consecration) causes childlessness is severe and counter to most Hindu practice; verify this is authentic Lal Kitab doctrine and not a misinterpretation.

#### `lalkitab-ch23-refine-uncle-veto`  _CH23_
**Summary:** Uncle in Saturn's Room -- Sun+Saturn in H4 Death Veto
**Condition:** {'type': 'planetary_combination', 'sub_type': 'structural', 'yoga_check': {'type': 'planet_in_house', 'checkable': True,
**Flag reason:** The specific claim that the uncle dies 'in the room designated for Saturn (left side for iron storage)' is very particular; verify this exact spatial-fatality linkage in classical sources.

#### `lalkitab-ch23-saturn-h1`  _CH23_
**Summary:** Saturn in H1 -- The Ruin Rule
**Condition:** {'type': 'planetary_combination', 'sub_type': 'construction', 'yoga_check': {'type': 'planet_in_house', 'checkable': Tru
**Flag reason:** The exception clause ('if no planets occupy both H7 and H10 simultaneously') is logically awkward; clarify whether this means 'if neither H7 nor H10 is occupied' or 'if H7 and H10 are not both occupied at once'.

#### `lalkitab-ch23-saturn-h3`  _CH23_
**Summary:** Saturn in H3 -- Mercury Enmity (Three Dogs Remedy)
**Condition:** {'type': 'planetary_combination', 'sub_type': 'construction', 'yoga_check': {'type': 'planet_in_house', 'checkable': Tru
**Flag reason:** Mercury enmity with Saturn in H3 is attested in Lal Kitab, but the 'three dogs remedy' is unusual and should be verified against primary source text; phrasing 'impotent' is non-standard.

#### `lalkitab-ch23-saturn-h6`  _CH23_
**Summary:** Saturn in H6 -- Virgo (Age 39 Rule, Daughter's Relatives)
**Condition:** {'type': 'planetary_combination', 'sub_type': 'construction', 'yoga_check': {'type': 'planet_in_house', 'checkable': Tru
**Flag reason:** Age 39 rule for Saturn in H6 is plausible but the parenthetical '(Virgo-friendly sign)' is misleading--H6 is not inherently Virgo; the rule should clarify whether this applies universally or only when Saturn is in Virgo.

#### `lalkitab-ch23-saturn-h8`  _CH23_
**Summary:** Saturn in H8 -- Death Veto (Scorpio / Mars Sign)
**Condition:** {'type': 'planetary_combination', 'sub_type': 'construction', 'yoga_check': {'type': 'planet_in_house', 'checkable': Tru
**Flag reason:** Saturn in H8 as severe veto is classical, but the claim that 'death starts to circle' and the dependency on Rahu/Ketu positions for determining family impact is vague and requires source verification.

#### `lalkitab-ch23-saturn-h9`  _CH23_
**Summary:** Saturn in H9 -- Father's Penalty (Pregnancy Trigger)
**Condition:** {'type': 'planetary_combination', 'sub_type': 'construction', 'yoga_check': {'type': 'planet_in_house', 'checkable': Tru
**Flag reason:** The pregnancy trigger and father's death upon completion of 3rd room/floor is specific but unusual; requires verification against Lal Kitab Chapter 23 primary text.

### CH24 (27 rules)

#### `lalkitab-ch24-age-early-9y`  _CH24_
**Summary:** Early Childhood -- Sun+Moon in H11 → Age 9 Years
**Condition:** {'type': 'planetary_combination', 'sub_type': 'short_life', 'yoga_check': {'type': 'planetary_combination', 'checkable':
**Flag reason:** no_response_from_model

#### `lalkitab-ch24-age-father-dependency`  _CH24_
**Summary:** Father's Death Dependency -- Mercury+Jupiter H2 or Jupiter+Rahu H3 → Age 30
**Condition:** {'type': 'planetary_combination', 'sub_type': 'short_life', 'yoga_check': {'type': 'planetary_combination', 'checkable':
**Flag reason:** The rule introduces a novel concept ('father's death at native's age 16, 19, or 22') that is not standard in classical Lal Kitab longevity doctrine. The connection between Mercury+Jupiter H2 / Jupiter+Rahu H3 and paternal death timing requires verification against original text.

#### `lalkitab-ch24-age-long-illness`  _CH24_
**Summary:** Long Illness -- Jupiter+Rahu H2 or Mercury+Jupiter H6 → 20 Years
**Condition:** {'type': 'planetary_combination', 'sub_type': 'health_affliction', 'yoga_check': {'type': 'planetary_combination', 'chec
**Flag reason:** The 20-year illness duration is specific but unverified. Lal Kitab does discuss Jupiter+Rahu combinations for health afflictions, but the exact duration attribution requires source confirmation.

#### `lalkitab-ch24-age-longlife-sun-rahu`  _CH24_
**Summary:** Long Life -- Sun+Rahu H10/H11 AND Life-Slashers H8 AND Saturn H3/5/6
**Condition:** {'type': 'planetary_combination', 'sub_type': 'longevity_marker', 'yoga_check': {'type': 'planetary_combination', 'check
**Flag reason:** The three-condition AND gate (Sun+Rahu H10/11 AND life-slashers H8 AND Saturn H3/5/6) is complex and counter-intuitive. While the logic is coherent, the claim that H8 malefics become longevity markers requires verification against Lal Kitab Chapter 24 original text.

#### `lalkitab-ch24-age-sudden-death`  _CH24_
**Summary:** Sudden Death -- Moon+Rahu in H1 → Bullet Shot, Afternoon
**Condition:** {'type': 'planetary_combination', 'sub_type': 'death_cause', 'yoga_check': {'type': 'planetary_combination', 'checkable'
**Flag reason:** The specific death cause ('bullet shot') and time ('afternoon') are highly specific claims. While Moon+Rahu H1 is a recognized malefic combination, the attribution of violent death cause and specific time of day requires source verification.

#### `lalkitab-ch24-age-threshold-50`  _CH24_
**Summary:** Mid-Life Age 50 -- Moon+Rahu H5 OR Debilitated Planets in H2 and H7
**Condition:** {'type': 'planetary_combination', 'sub_type': 'age_threshold', 'yoga_check': {'type': 'planetary_combination', 'checkabl
**Flag reason:** Branch B ('planets debilitated in H2 and H7') is vague. It does not specify which planets or what constitutes debilitation in this context. The rule would benefit from explicit planet names and debilitation criteria.

#### `lalkitab-ch24-age-threshold-85`  _CH24_
**Summary:** Late-Life Age 85 -- Moon+Mars in H7
**Condition:** {'type': 'planetary_combination', 'sub_type': 'age_threshold', 'yoga_check': {'type': 'planetary_combination', 'checkabl
**Flag reason:** Contradicts rule(s): lalkitab-ch24-moon-h7

#### `lalkitab-ch24-effect-moon-h7`  _CH24_
**Summary:** Moon Exalted / Lord of H7 -- Native Marries at Age 24
**Condition:** {'type': 'planetary_combination', 'sub_type': 'age_effect', 'yoga_check': {'type': 'planet_in_house', 'checkable': True}
**Flag reason:** The summary conflates 'Moon exalted' with 'Moon in H7' and 'Moon lord of H7'--these are three distinct conditions. The rule should clarify which condition(s) apply. The age 24 activation is specific but requires source verification.

#### `lalkitab-ch24-effect-saturn-h4`  _CH24_
**Summary:** Saturn Exalted / Lord of H4 -- Native Acquires Land/Property
**Condition:** {'type': 'planetary_combination', 'sub_type': 'age_effect', 'yoga_check': {'type': 'planet_in_house', 'checkable': True}
**Flag reason:** Summary mentions 'Saturn Exalted / Lord of H4' but condition only specifies planet_in_house for Saturn in H4; exaltation status and lordship are not encoded in the condition structure.

#### `lalkitab-ch24-effect-sun-h4-debil`  _CH24_
**Summary:** Sun Debilitated in H4 -- Inauspicious Job/Business + Loss of House/Vehicle
**Condition:** {'type': 'planetary_combination', 'sub_type': 'age_effect', 'yoga_check': {'type': 'planet_in_house', 'checkable': True}
**Flag reason:** Summary and detailed text reference 'Sun debilitated in H4' but condition lacks explicit debilitation check; condition structure does not encode dignity state.

#### `lalkitab-ch24-effect-sun-h4-exalted`  _CH24_
**Summary:** Sun Exalted / Lord of H4 -- Starts Work + Home/Vehicle Joy at Age 22
**Condition:** {'type': 'planetary_combination', 'sub_type': 'age_effect', 'yoga_check': {'type': 'planet_in_house', 'checkable': True}
**Flag reason:** Summary mentions 'Sun Exalted / Lord of H4' but condition only specifies planet_in_house without encoding exaltation or lordship status.

#### `lalkitab-ch24-mod-male-planet`  _CH24_
**Summary:** Moon-Male Planet Conjunction Modifier -- Age 96
**Condition:** {'type': 'planetary_combination', 'sub_type': 'moon_modifier', 'yoga_check': {'type': 'planetary_combination', 'checkabl
**Flag reason:** Contradicts rule(s): lalkitab-ch24-mod-venus

#### `lalkitab-ch24-mod-venus`  _CH24_
**Summary:** Moon-Venus Conjunction Modifier -- Age 85
**Condition:** {'type': 'planetary_combination', 'sub_type': 'moon_modifier', 'yoga_check': {'type': 'planetary_combination', 'checkabl
**Flag reason:** Contradicts rule(s): lalkitab-ch24-mod-male-planet

#### `lalkitab-ch24-moon-h1`  _CH24_
**Summary:** Moon in H1 -- Lifespan 90 Years, Death on Wednesday
**Condition:** {'type': 'planetary_combination', 'sub_type': 'moon_age_engine', 'yoga_check': {'type': 'planet_in_house', 'checkable': 
**Flag reason:** Inclusion of 'day of death = Wednesday' as a deterministic output from Moon-House placement is unusual and requires verification against classical Lal Kitab texts; this level of specificity may be over-interpreted.

#### `lalkitab-ch24-moon-h10`  _CH24_
**Summary:** Moon in H10 -- Lifespan 90 Years, Death on Tuesday
**Condition:** {'type': 'planetary_combination', 'sub_type': 'moon_age_engine', 'yoga_check': {'type': 'planet_in_house', 'checkable': 
**Flag reason:** Deterministic day-of-death assignment (Tuesday) from Moon in H10 is highly specific and requires source verification; classical texts typically do not assign fixed weekdays to house placements.

#### `lalkitab-ch24-moon-h11`  _CH24_
**Summary:** Moon in H11 -- Lifespan 90 Years, Death on Saturday
**Condition:** {'type': 'planetary_combination', 'sub_type': 'moon_age_engine', 'yoga_check': {'type': 'planet_in_house', 'checkable': 
**Flag reason:** Deterministic day-of-death assignment (Saturday) from Moon in H11 is highly specific and requires source verification; classical texts typically do not assign fixed weekdays to house placements.

#### `lalkitab-ch24-moon-h12`  _CH24_
**Summary:** Moon in H12 -- Lifespan 90 Years, Death on Thursday
**Condition:** {'type': 'planetary_combination', 'sub_type': 'moon_age_engine', 'yoga_check': {'type': 'planet_in_house', 'checkable': 
**Flag reason:** Deterministic day-of-death assignment (Thursday) from Moon in H12 is highly specific and requires source verification; classical texts typically do not assign fixed weekdays to house placements.

#### `lalkitab-ch24-moon-h2`  _CH24_
**Summary:** Moon in H2 -- Lifespan 96 Years, Death on Friday
**Condition:** {'type': 'planetary_combination', 'sub_type': 'moon_age_engine', 'yoga_check': {'type': 'planet_in_house', 'checkable': 
**Flag reason:** Deterministic day-of-death assignment (Friday) from Moon in H2 is highly specific and requires source verification; classical texts typically do not assign fixed weekdays to house placements.

#### `lalkitab-ch24-moon-h3`  _CH24_
**Summary:** Moon in H3 -- Lifespan 80 Years, Death on Wednesday
**Condition:** {'type': 'planetary_combination', 'sub_type': 'moon_age_engine', 'yoga_check': {'type': 'planet_in_house', 'checkable': 
**Flag reason:** Deterministic day-of-death assignment (Wednesday) from Moon in H3 is highly specific and requires source verification; classical texts typically do not assign fixed weekdays to house placements.

#### `lalkitab-ch24-moon-h5`  _CH24_
**Summary:** Moon in H5 -- Lifespan 100 Years, Death on Tuesday
**Condition:** {'type': 'planetary_combination', 'sub_type': 'moon_age_engine', 'yoga_check': {'type': 'planet_in_house', 'checkable': 
**Flag reason:** Moon in H5 yielding 100 years is plausible (H5 is favorable), but the dual house lords (Ketu, Mercury) and Tuesday assignment need source verification; Ketu as H5 lord is unusual and requires clarification.

#### `lalkitab-ch24-moon-h6`  _CH24_
**Summary:** Moon in H6 -- Lifespan 80 Years, Death on Sunday
**Condition:** {'type': 'planetary_combination', 'sub_type': 'moon_age_engine', 'yoga_check': {'type': 'planet_in_house', 'checkable': 
**Flag reason:** Moon in H6 (6th house of disease/enemies) yielding 80 years is reasonable, but Venus as sole H6 lord is incorrect in standard Vedic astrology (H6 lord varies by ascendant); requires source verification.

#### `lalkitab-ch24-moon-h7`  _CH24_
**Summary:** Moon in H7 -- Lifespan 85 Years, Death on Monday
**Condition:** {'type': 'planetary_combination', 'sub_type': 'moon_age_engine', 'yoga_check': {'type': 'planet_in_house', 'checkable': 
**Flag reason:** Moon in H7 with 85-year lifespan is plausible, but Mars as H7 lord is ascendant-dependent; the Monday death-day assignment needs source confirmation.

#### `lalkitab-ch24-moon-h8`  _CH24_
**Summary:** Moon in H8 -- Lifespan 90 Years, Death on Wednesday
**Condition:** {'type': 'planetary_combination', 'sub_type': 'moon_age_engine', 'yoga_check': {'type': 'planet_in_house', 'checkable': 
**Flag reason:** Moon in H8 (8th house of longevity) yielding 90 years is reasonable, but Jupiter as H8 lord is ascendant-dependent; Wednesday assignment requires verification.

#### `lalkitab-ch24-moon-h9`  _CH24_
**Summary:** Moon in H9 -- Lifespan 75 Years, Death on Thursday
**Condition:** {'type': 'planetary_combination', 'sub_type': 'moon_age_engine', 'yoga_check': {'type': 'planet_in_house', 'checkable': 
**Flag reason:** Moon in H9 (9th house of fortune/dharma) yielding 75 years is plausible, but Jupiter as H9 lord is ascendant-dependent; Thursday assignment needs source confirmation.

#### `lalkitab-ch24-physical-forehead-broken`  _CH24_
**Summary:** Forehead Broken Lines -- Gender-Specific Age Table (1-4 Broken Lines)
**Condition:** {'type': 'general_principle', 'sub_type': 'physical_metric', 'yoga_check': {'type': 'manual', 'checkable': False, 'descr
**Flag reason:** Forehead line reading is attested in Lal Kitab, but the gender-specific age table (especially the 4-line male=40yr entry) requires verification against original text; the null value for 4-line female is noted but unexplained.

#### `lalkitab-ch24-physical-forehead-ear-to-ear`  _CH24_
**Summary:** Forehead Ear-to-Ear Lines -- 1 Line=100yr, 2 Lines=70yr
**Condition:** {'type': 'general_principle', 'sub_type': 'physical_metric', 'yoga_check': {'type': 'manual', 'checkable': False, 'descr
**Flag reason:** Ear-to-ear forehead lines are attested in Lal Kitab, but the inverse relationship (1 line = 100yr, 2 lines = 70yr) is counterintuitive and requires source verification.

#### `lalkitab-ch24-physical-forehead-whole`  _CH24_
**Summary:** Forehead Whole Lines -- Gender-Specific Age Table (0-7 Lines)
**Condition:** {'type': 'general_principle', 'sub_type': 'physical_metric', 'yoga_check': {'type': 'manual', 'checkable': False, 'descr
**Flag reason:** Whole forehead line reading is attested, but the 7-line entry (male=50yr, non-linear overextension) is unusual and poorly explained; the null values for female 0-line and 7-line entries need clarification.

### CH25 (4 rules)

#### `lalkitab-ch25-jupiter-h12`  _CH25_
**Summary:** Jupiter Afflicting in H12 -- Gram/Saffron/Gold at Night (Post-Father's Death)
**Condition:** Planet: Jupiter | House: 12
**Flag reason:** Remedy instruction contradicts stated timing constraint: rule says 'during the night' but daytime-conjunction-rule (lalkitab-ch25-daytime-conjunction-rule) mandates daytime for all Ch25 remedies; clarify whether H12 Jupiter is exception or if 'night' is a transcription error.

#### `lalkitab-ch25-moon-h3`  _CH25_
**Summary:** Moon Afflicting in H3 -- Donate Green Clothes to Maidens
**Condition:** Planet: Moon | House: 3
**Flag reason:** Remedy logic (donating green clothes to invoke Mercury succour for H3 Mars house) is creative but non-standard; verify against original Lal Kitab text to confirm this interpretation is faithful.

#### `lalkitab-ch25-sun-sat-gold-loss`  _CH25_
**Summary:** Sun+Saturn Conjunction AND Gold/Jaggery Loss -- Donate Saturn Objects
**Condition:** {'type': 'planetary_combination', 'sub_type': 'conjunction_remedy', 'yoga_check': {'type': 'planet_conjunction', 'checka
**Flag reason:** Contradicts rule(s): lalkitab-ch25-sun-sat-property

#### `lalkitab-ch25-sun-sat-property`  _CH25_
**Summary:** Sun+Saturn Conjunction AND Saturn Objects Being Destroyed -- Donate Sun Objects
**Condition:** {'type': 'planetary_combination', 'sub_type': 'conjunction_remedy', 'yoga_check': {'type': 'planet_conjunction', 'checka
**Flag reason:** Contradicts rule(s): lalkitab-ch25-sun-sat-gold-loss

### CH27 (40 rules)

#### `lalkitab-ch27-corr-jupiter`  _CH27_
**Summary:** Jupiter correspondences: Lord Brahma, colour Yellow, body parts Neck/Nose, objects Gram pulse/Gold.
**Condition:** Planet: Jupiter
**Flag reason:** Jupiter's lord is traditionally Indra or Brihaspati in Vedic texts, not Brahma; Brahma is creator but not Jupiter's presiding deity in standard Lal Kitab correspondences. Verify against original Ch. 27 table.

#### `lalkitab-ch27-corr-ketu`  _CH27_
**Summary:** Ketu correspondences: Lord Ganesh, colour Spotted, body parts Torso/Spinal cord/Knees/Toes/Palm/Ear, objects Sesame.
**Condition:** Planet: Ketu
**Flag reason:** Ketu's presiding lord is traditionally Ganesh or Chitragupta; assignment to Ganesh is plausible but less common than Chitragupta in classical Lal Kitab. Verify source table.

#### `lalkitab-ch27-corr-mercury`  _CH27_
**Summary:** Mercury correspondences: Lord Durga, colour Green, body parts Brain/Teeth/Neuron/Tongue/Nose, objects Whole moong.
**Condition:** Planet: Mercury
**Flag reason:** Mercury's presiding lord is traditionally Vishnu or Saraswati, not Durga. Durga is typically associated with Mars or Ketu. Verify against original Lal Kitab Ch. 27.

#### `lalkitab-ch27-corr-moon`  _CH27_
**Summary:** Moon correspondences: Lord Shiva, colour Milky white, body parts Heart/Left face, objects Rice/Milk/Silver.
**Condition:** Planet: Moon
**Flag reason:** Moon's presiding lord is traditionally Parvati or Gauri, not Shiva. Shiva is associated with Saturn or Ketu in Lal Kitab. Verify source table.

#### `lalkitab-ch27-corr-rahu`  _CH27_
**Summary:** Rahu correspondences: Lord Saraswati, colour Blue, body parts Head/Chin/Head-shaking, objects Mustard/Blue sapphire.
**Condition:** Planet: Rahu
**Flag reason:** Rahu's presiding lord is traditionally Durga or Kali, not Saraswati. Saraswati is Mercury's deity. Verify against original Ch. 27 correspondence table.

#### `lalkitab-ch27-invis-mars`  _CH27_
**Summary:** Mars invisible in houses 4/8. Totaka remedy: Immerse rewari (sesame-jaggery sweet) in running water.
**Condition:** Planet: Mars
**Flag reason:** Rewari remedy logic is coherent, but sesame is more commonly associated with Ketu/Saturn than Mars. Verify that rewari is the correct Mars invisible remedy in original Lal Kitab Ch. 27.

#### `lalkitab-ch27-proh-02`  _CH27_
**Summary:** If House 2 is vacant and evil planets occupy House 8, visiting a temple is strictly prohibited.
**Condition:** {'type': 'planetary_combination', 'description': 'Temple visit prohibition (H2 vacant + evil in H8)', 'yoga_check': {'ty
**Flag reason:** Temple visit prohibition based on H2 vacant + H8 evil is attested in Lal Kitab but the causal logic (negative axis) is interpretive; the rule itself is sound but borderline on specificity.

#### `lalkitab-ch27-proh-05`  _CH27_
**Summary:** Saturn in Ascendant and Jupiter in 5th: do not give copper to beggars.
**Condition:** {'type': 'planetary_combination', 'description': 'Saturn in Asc + Jupiter in 5th -- copper donation to beggars', 'yoga_ch
**Flag reason:** Saturn Asc + Jupiter 5th combination is valid, but the causal link (copper donation → child suffering) is specific to Lal Kitab and should be verified against primary text.

#### `lalkitab-ch27-proh-06`  _CH27_
**Summary:** Jupiter in 10th and Moon in 4th: do not construct a temple.
**Condition:** {'type': 'planetary_combination', 'description': 'Jupiter in 10th + Moon in 4th -- temple construction', 'yoga_check': {'
**Flag reason:** forced_phr: validator_conservatism -- rule is source-verbatim (Lal Kitab Ch 27); flagged due to standard Vedic logic vs LK mental wave / extreme-outcome prohibition system.

#### `lalkitab-ch27-proh-07`  _CH27_
**Summary:** Venus in 9th house: do not adopt a child.
**Condition:** Planet: Venus | House: 9
**Flag reason:** Venus 9th affecting adoption is plausible (Venus = progeny, 9th = fortune) but the specific prohibition on adoption under this placement is not universally attested in major Lal Kitab editions.

#### `lalkitab-ch27-proh-09`  _CH27_
**Summary:** Jupiter in 7th house: do not donate clothes.
**Condition:** Planet: Jupiter | House: 7
**Flag reason:** Jupiter 7th cloth donation rule is attested but the outcome 'family pines for clothes' is colloquial; verify against original Lal Kitab text.

#### `lalkitab-ch27-proh-10`  _CH27_
**Summary:** Sun in 7th or 8th house: do not donate during morning or evening.
**Condition:** Planet: Sun
**Flag reason:** forced_phr: validator_conservatism -- rule is source-verbatim (Lal Kitab Ch 27); flagged due to standard Vedic logic vs LK mental wave / extreme-outcome prohibition system.

#### `lalkitab-ch27-transfer-h03`  _CH27_
**Summary:** Wear the object as a gem on the hand.
**Condition:** House: 3
**Flag reason:** Transfer protocol for House 3 is plausible (hands/effort alignment), but Lal Kitab Chapter 27 transfer rules are not well-documented in standard English translations; recommend verification against original Hindi text.

#### `lalkitab-ch27-transfer-h04`  _CH27_
**Summary:** Immerse the object in running water.
**Condition:** House: 4
**Flag reason:** Water immersion for House 4 is thematically coherent (water/mother/home), but source attribution to Lal Kitab Ch 27 requires verification against primary text.

#### `lalkitab-ch27-transfer-h05`  _CH27_
**Summary:** Transfer the object to a school or college.
**Condition:** House: 5
**Flag reason:** Educational institution transfer for House 5 is logically sound (education/children), but specific sourcing to Lal Kitab Ch 27 needs confirmation.

#### `lalkitab-ch27-transfer-h06`  _CH27_
**Summary:** Drop the object in a well.
**Condition:** House: 6
**Flag reason:** Well-dropping for House 6 (enemies/disease removal) is thematically consistent with Lal Kitab remedial logic, but exact chapter attribution requires verification.

#### `lalkitab-ch27-transfer-h07`  _CH27_
**Summary:** Bury the object under the ground.
**Condition:** House: 7
**Flag reason:** forced_phr: grammar error in detailed text corrected (was: 'burying grounds and neutralises').

#### `lalkitab-ch27-transfer-h08`  _CH27_
**Summary:** Bury the object at the pyre ground.
**Condition:** House: 8
**Flag reason:** Pyre ground burial for House 8 is symbolically appropriate (death/transformation), but this extreme remedy is not widely attested in accessible Lal Kitab sources; flag for verification.

#### `lalkitab-ch27-transfer-h10`  _CH27_
**Summary:** Eatables: give to father. Wearables: wear them. Other objects: bury near public property shadow.
**Condition:** House: 10
**Flag reason:** Three-part rule for House 10 is detailed and logically coherent (father/career/karma), but the phrase 'bury near public property shadow' is unusual and requires source verification.

#### `lalkitab-ch27-transfer-h12`  _CH27_
**Summary:** Install the object on the roof of the house.
**Condition:** House: 12
**Flag reason:** Roof installation for House 12 (liberation/loss) is symbolically coherent, but this specific remedy is not widely documented in standard Lal Kitab references.

#### `lalkitab-ch27-wave-w01`  _CH27_
**Summary:** Section 1, House 1, Venus / Saturn: Love and Romance. Physical/sexual love driven by Venus; verbal expression of love driven by Saturn.
**Condition:** Planet: Venus / Saturn | House: 1
**Flag reason:** forced_phr: validator_conservatism -- rule is source-verbatim (Lal Kitab Ch 27); flagged due to standard Vedic logic vs LK mental wave / extreme-outcome prohibition system.

#### `lalkitab-ch27-wave-w02`  _CH27_
**Summary:** Section 2, House 2, Jupiter: Desire to Marry. Intensifying desire to formalise union and build family.
**Condition:** Planet: Jupiter | House: 2
**Flag reason:** Jupiter in House 2 for 'Desire to Marry' is plausible (Jupiter = expansion, House 2 = family), but the 42-section mental wave engine is not a standard Lal Kitab framework; requires source verification.

#### `lalkitab-ch27-wave-w03`  _CH27_
**Summary:** Section 3, House 3, Venus: Offspring Affection. Deep longing for a son; paternal/parental affection wave.
**Condition:** Planet: Venus | House: 3
**Flag reason:** forced_phr: validator_conservatism -- rule is source-verbatim (Lal Kitab Ch 27); flagged due to standard Vedic logic vs LK mental wave / extreme-outcome prohibition system.

#### `lalkitab-ch27-wave-w06`  _CH27_
**Summary:** Section 4, House 4, Mars Malefic: Destructor. Destructive tendency towards love relationships and friendships.
**Condition:** Planet: Mars Malefic | House: 4
**Flag reason:** Mars Malefic in House 4 for destructive tendency is plausible, but the term 'Mars Malefic' is non-standard; Mars is inherently malefic in classical texts. Clarify whether this refers to Mars in a weak/afflicted state.

#### `lalkitab-ch27-wave-w09`  _CH27_
**Summary:** Section 6, House 6, Venus: Interest in Progeny. Heightened attention and investment towards the male child.
**Condition:** Planet: Venus | House: 6
**Flag reason:** forced_phr: validator_conservatism -- rule is source-verbatim (Lal Kitab Ch 27); flagged due to standard Vedic logic vs LK mental wave / extreme-outcome prohibition system.

#### `lalkitab-ch27-wave-w10`  _CH27_
**Summary:** Section 7, House 7, Venus: Ambition. Burning desire to rise in social status and achieve higher standing.
**Condition:** Planet: Venus | House: 7
**Flag reason:** forced_phr: false contradiction -- mental wave engine permits multiple waves per house/planet; w10 (Ambition) and w38 (Object Recognition) are distinct psychological traits, not competing predictions.

#### `lalkitab-ch27-wave-w11`  _CH27_
**Summary:** Section 7, House 7, Mercury: Proof Desire. Strong desire to prove oneself. Particularly strong in flat-headed natives.
**Condition:** Planet: Mercury | House: 7
**Flag reason:** Reference to 'flat-headed natives' is physiognomical and lacks clear classical Vedic textual basis; the core principle (Mercury in H7 = proof desire) is plausible but needs verification against primary Lal Kitab sources.

#### `lalkitab-ch27-wave-w14`  _CH27_
**Summary:** Section 9, House 9, Saturn: Revengefulness. If unable to take revenge personally, the native teaches their child to take revenge before death.
**Condition:** Planet: Saturn | House: 9
**Flag reason:** The specific claim about teaching a child to take revenge before death is unusually dark and specific; while Saturn in H9 can indicate harsh karmic patterns, this phrasing warrants verification against original Lal Kitab text.

#### `lalkitab-ch27-wave-w16`  _CH27_
**Summary:** Section 11, House 11, Saturn: Wealth Amassing. Persistent engagement in accumulating wealth; may shade into compulsive hoarding or theft.
**Condition:** Planet: Saturn | House: 11
**Flag reason:** The escalation from wealth accumulation to 'compulsive hoarding or theft' is a significant interpretive leap; Saturn in H11 typically indicates disciplined wealth-building, but the theft implication needs source verification.

#### `lalkitab-ch27-wave-w17`  _CH27_
**Summary:** Section 12, House 12, Rahu: Secrecy. Tendency to swindle and maintain extreme secrecy about activities and intentions.
**Condition:** Planet: Rahu | House: 12
**Flag reason:** Rahu in H12 with 'tendency to swindle' is a strong negative claim; while Rahu-H12 can indicate deception, the explicit swindling attribution requires verification against classical Lal Kitab passages.

#### `lalkitab-ch27-wave-w27`  _CH27_
**Summary:** Section 21, House 4, Moon: Sympathy. Deep empathy for others. Particularly high in wide/high-forehead natives.
**Condition:** Planet: Moon | House: 4
**Flag reason:** Reference to 'wide/high-forehead natives' is physiognomical; while Moon in H4 = sympathy is sound, the forehead qualifier lacks clear classical Vedic basis and should be verified.

#### `lalkitab-ch27-wave-w28`  _CH27_
**Summary:** Section 22, House 5, Jupiter: Intelligence. Acts according to own mind rather than following others. Strong in wide/raised-forehead natives.
**Condition:** Planet: Jupiter | House: 5
**Flag reason:** Reference to 'wide/raised-forehead natives' is physiognomical; Jupiter in H5 = independent intelligence is sound, but the forehead qualifier needs source verification.

#### `lalkitab-ch27-wave-w31`  _CH27_
**Summary:** Section 25, House 8, Evil Planet: Imitator. Wonderful capacity to imitate others; belligerent when crossed.
**Condition:** Planet: Evil Planet | House: 8
**Flag reason:** Lal Kitab's 'Imitator' wave is poorly documented in English sources; the characterization as 'belligerent when crossed' needs verification against original text.

#### `lalkitab-ch27-wave-w33`  _CH27_
**Summary:** Section 26, House 9, Mercury: Excess Humour. Humour that tips into foolishness; wit without wisdom.
**Condition:** Planet: Mercury | House: 9
**Flag reason:** Contradicts rule(s): lalkitab-ch27-wave-w40

#### `lalkitab-ch27-wave-w34`  _CH27_
**Summary:** Section 27, House 3, Mars: Mental Strength. Knows the underlying truth behind every situation and person.
**Condition:** Planet: Mars | House: 3
**Flag reason:** Mars in House 3 traditionally governs courage and communication, not necessarily 'knowing underlying truth'; this interpretation may conflate Mars with Saturn or Ketu qualities.

#### `lalkitab-ch27-wave-w38`  _CH27_
**Summary:** Section 31, House 7, Venus: Object Recognition. Discerning perception of colour, face, and character of people and objects.
**Condition:** Planet: Venus | House: 7
**Flag reason:** forced_phr: false contradiction -- mental wave engine permits multiple waves per house/planet; w10 (Ambition) and w38 (Object Recognition) are distinct psychological traits, not competing predictions.

#### `lalkitab-ch27-wave-w39`  _CH27_
**Summary:** Section 32, House 8, Saturn: Cleanliness. Highly organised external life; may mask inner cunning.
**Condition:** Planet: Saturn | House: 8
**Flag reason:** Saturn in House 8 is traditionally associated with secrecy and hidden matters; 'cleanliness masking cunning' is plausible but needs source verification.

#### `lalkitab-ch27-wave-w40`  _CH27_
**Summary:** Section 33, House 9, Mercury: Judgement Strength. Balanced judgement between heart and mind; wise discernment.
**Condition:** Planet: Mercury | House: 9
**Flag reason:** Contradicts rule(s): lalkitab-ch27-wave-w33

#### `lalkitab-ch27-wave-w41`  _CH27_
**Summary:** Section 34, House 10, Mars Malefic: Memory Power. Exceptional memory; becomes a consummate cheat if Saturn is also malefic in House 10.
**Condition:** Planet: Mars Malefic | House: 10
**Flag reason:** Conditional statement about Saturn also being malefic in House 10 is complex; needs verification that this dual-planet condition is documented in Lal Kitab Chapter 27.

#### `lalkitab-ch27-wave-w44`  _CH27_
**Summary:** Section 37, House 1, Saturn: Musical Note. Natural understanding of musical notes and rhythmic patterns.
**Condition:** Planet: Saturn | House: 1
**Flag reason:** Saturn in House 1 (Ascendant) is traditionally associated with discipline and restraint, not specifically musical aptitude; this attribution needs source verification.

---
