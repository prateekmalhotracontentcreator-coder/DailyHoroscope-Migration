# 300_COMBINATIONS_INGEST.md
> B.V. Raman -- Three Hundred Important Combinations
> Last updated: 2026-06-01 · Status: ✅ INGESTED · ✅ TRIAGE COMPLETE · ✅ OP-08 CLOSED -- 0 FLAGGED

---

## One-Liner

329 rules ingested. All open items closed 2026-06-01.
**141 auto_approved · 188 PHR · 0 flagged · 0 pending_review.**
OP-08 closed: 14 tba conditions encoded from Diagnostics (Y264-Y274, Y292-Y294); 4 engine-dep rules (Y130-Y134) → PHR.
3 Nabhasa contradiction pairs tagged `strength_dependent`. All validator errors resolved (Bucket B → PHR).
Awaiting co-founder sign-off on 141 auto_approved.

---

## Ingest Summary

| Metric | Value |
|---|---|
| Batch ID | `300-combinations-v1-20260601` |
| Source folder | `/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredCombinations_CC_Decode/` |
| Ingest date | 2026-06-01 |
| Ingest script | `backend/scripts/ingest_from_json_folder.py` |
| Rules inserted | 329 |
| Duplicates skipped | 0 |
| Errors | 0 |
| Pre-ingest dedup | ✅ Clean -- 0 matches, 0 contradictions vs MongoDB export (9,196 rules) |

---

## Validation Results

| Status | Count | Notes |
|---|---|---|
| auto_approved | 97 | 37% of 259 old-schema rules -- passed AI quality check |
| pending_human_review | 145 | 70 new-schema (see Open Items) + 75 old-schema AI-reviewed |
| flagged | 73 | 4 root causes -- see Flagged Triage section below |
| pending_review | 14 | interpretation_too_short -- Nabhasa yogas (Y075-Y116 range) |
| **Total** | **329** | |

---

## Schema Notes (IMPORTANT for future re-validation)

The 300 Combinations decode has **two distinct schemas**:

### NEW schema (Y001-040 + intro + strength sections, ~70 rules)
Files: `Combo_Y001-040_Rules.json`, `Combo_Intro_Strength_Rules.json`

```json
{
  "full_text": "...",
  "claim_polarity": "positive|negative|mixed|neutral",
  "condition": { "type": "...", ... }
}
```
These rules were ingested with `full_text` mapped to `interpretation.detailed` by the ingest script.

### OLD schema (Y044-Y300, ~259 rules)
Files: `Combo_Y044-060_Rules.json` through `Combo_Y288-300_Rules.json`

```json
{
  "yoga_name": "...",
  "results": ["outcome 1", "outcome 2", ...],
  "special_notes": "...",
  "polarity": "positive|negative|mixed",
  "conditions": [{ ... }, ...]
}
```
OLD schema required post-ingest patching via `backend/scripts/patch_300combo_old_schema.py`:
- `results` list + `special_notes` + `yoga_name` → `interpretation.detailed`
- `polarity` → `claim_polarity`
- `conditions` list → `condition` dict (sub_conditions + operator=AND for multiple conditions)

Patch result: 259/259 patched, 0 errors.

---

## 3 Contradiction Pairs (all strength-dependent -- L5 false positives)

| Pair | Rule A | Rule B | Nature |
|---|---|---|---|
| Nabhasa: Danda vs Chapa | `combo-y074-001` | `combo-y078-001` | Danda (10,11,12,1) = unhappy from family; Chapa (10,11,12,1,2,3,4) = happy comfortable life. Different house span -- Chapa extends Danda; outcomes scale with chart strength. |
| Nabhasa: Chandra vs Samudra | `combo-y080-001` | `combo-y090-001` | Chandra = all planets odd houses → king; Samudra = all planets even houses → ruler. Mutually exclusive conditions -- NOT a contradiction. AI flagged overlap in outcomes. |
| Nabhasa: Sakata vs Kamala | `combo-y082-001` | `combo-y088-001` | Sakata (1,7) = poverty, domestic unhappiness; Kamala (1,4,7,10) = prestige, fame. Kamala extends Sakata. Raman explicitly notes strength of yoga determines magnitude. |

**Resolution:** All 3 are `strength_dependent` Nabhasa yoga cross-pairs. Both rules in each pair are valid. No rejection needed. These are expected per L5 (complementary polarity rules). 

**Action for TT:** At co-founder approval stage, tag all 6 rules with `contradiction_resolution: "strength_dependent"` and `contradiction_note: "Nabhasa yoga -- outcome scales with chart strength; both rules valid"`. No rule should be rejected.

---

## Flagged Rules Triage (73 total -- 4 root cause buckets)

### Bucket F1 -- Empty composite condition (Y123-Y134 range, ~14 rules)
Rules: combo-y123 through combo-y134 and some in Y138-Y140 range.
**Root cause:** Original yoga has multi-step calculation requirements (Shadbal, Vaiseshikamsa, Kalabala) that the Codex decode left as placeholder composite conditions. The `condition` dict has `type: "composite"` with no sub_conditions filled.
**Also:** Detailed text is incomplete or references "requires full Shadbal" without specifying the actual condition.
**Action:** TT/GAI queue -- need TT to supply the actual condition logic from the PDF or mark these as `tba: true` with note that the full condition requires engine-level calculation. These are NOT Codex errors per se -- the yogas genuinely require complex runtime computation.

### Bucket F2 -- JSON object corruption in interpretation fields (Y168-Y174, ~7 rules)
Rules: combo-y168 through combo-y174.
**Root cause:** The Codex output for these rules placed JSON object notation (`{...}`) inside the `results` list entries instead of plain text prose. The old-schema patch converted them to `interpretation.detailed` but the JSON structure leaked through.
**Example flagged reason:** "Summary and detailed fields contain JSON objects instead of plain text prose."
**Action:** Codex re-encode pass on the 7 source JSON files. These 7 rules need the `results` field corrected in the source JSON and the MongoDB records re-patched. File: `Combo_Y168-180_Rules.json` is the primary affected file.

### Bucket F3 -- Within-book duplicate pairs (Y189-Y197 range, ~3 rules)
Rules: combo-y190, combo-y192, combo-y197 (with their Y189, Y191, Y196 counterparts).
**Root cause:** Raman's book has sequential yogas with near-identical conditions but slightly different wording. These are likely intended as variant descriptions within the same yoga cluster (Y181-Y200 Asubha/Subha yoga series).
**Example:** Y190 = "little effort" vs Y189 = "hardly any effort" -- trivial wording variation.
**Action:** At co-founder approval, check source PDF. If genuinely redundant: reject the lower-quality rule. If distinguishable by condition nuance: keep both with `variant_note` added.

### Bucket F4 -- General AI flags (remaining ~49 rules)
All other flagged rules where the AI validator raised doctrinal, completeness, or ambiguity concerns.
**Action:** Standard Bucket B/C triage at approval stage. Validate against PDF first (Bucket B: validator error → PHR). Only retain flagged status if the concern is genuine (Bucket C: Codex fabrication or real ambiguity).

---

## 14 pending_review Rules (interpretation_too_short)

All 14 are Nabhasa yogas from the Y075-Y116 range:
- Y075 Nav Yoga, Y076 Kuta, Y077 Chhatra, Y081 Gada, Y084 Vajra, Y085, Y086, Y087, Y100, Y110, Y114, Y115, Y116, Y295

**Root cause:** Raman's original text for these yogas is genuinely brief -- 1-3 short outcomes (e.g., "A happy individual", "A liar; A jailor"). The OLD-schema patch correctly built `interpretation.detailed` as `"YogaName. Results: outcome1; outcome2."` -- this text is correct but short (~37-80 chars), below validate_rules.py's minimum length threshold.

**These are NOT decode errors** -- the source text is brief by nature.

**Action:** At TT approval stage, add `short_interpretation_justified: true` flag and manually approve. Alternatively, enrich each with a sentence of Raman's commentary context from the source PDF. Do NOT auto-reject -- these are valid textbook rules.

---

## 70 New-Schema Rules Needing AI Re-Validation

**Issue:** When `validate_rules.py` ran (Stage 2 AI quality check), `ANTHROPIC_API_KEY` was not set in the shell environment for the first batch. The 70 new-schema rules (Y001-040, intro, strength) were already at `pending_human_review` status at that point (ingested with the old `approval_status` from source files, overriding the expected `pending_review`).

**Wait -- re-checking:** The ingest script sets `approval_status = "pending_review"` on all rules. After AI validation ran, the 70 new-schema rules that didn't pass AI check landed at `pending_human_review` without the benefit of Claude's quality evaluation.

**Current state:** 70 rules at `approval_status: "pending_human_review"` -- they went through structural Stage 1 validation only.

**Action to get AI quality scores on these 70:**
```bash
# Reset the 70 new-schema rules back to pending_review, then re-run validate_rules.py
# Step 1: identify the new-schema rule_ids (Y001-040 prefix + intro/strength)
# Step 2: reset in MongoDB:
python3 -c "
from pymongo import MongoClient
MONGO_URL='...'
client = MongoClient(MONGO_URL)
db = client['horoscope_db']
# New-schema rules are Y001-040 + intro/strength
# Filter: combo-y0[0-3][0-9]-* and combo-intro-*, combo-strength-*
import re
rules = list(db.interpretation_rules.find(
    {'ingest_batch_id': '300-combinations-v1-20260601', 'approval_status': 'pending_human_review'},
    {'_id':0,'rule_id':1}
))
new_schema_ids = [r['rule_id'] for r in rules
    if re.match(r'combo-(y0[0-3]\d|intro|strength)', r['rule_id'])]
print(f'New-schema PHR rules to reset: {len(new_schema_ids)}')
# Uncomment to reset:
# result = db.interpretation_rules.update_many(
#     {'rule_id': {'\\$in': new_schema_ids}},
#     {'\\$set': {'approval_status': 'pending_review'}}
# )
"
# Step 3: re-run validate_rules.py with ANTHROPIC_API_KEY set
ANTHROPIC_API_KEY='sk-ant-...' python3 backend/scripts/validate_rules.py \
  --batch-id 300-combinations-v1-20260601 \
  --mongo-url "..." --db-name horoscope_db
```

**This is OPTIONAL** -- the 70 rules are still usable at PHR status and will reach co-founder review. AI validation gives a quality score but does not change the approval gate (co-founder sign-off is still required for `approved` status).

---

## Open Items

| ID | Priority | Detail | Status |
|---|---|---|---|
| ~~300C-OP-01~~ | ~~🟠 HIGH~~ | ~~Bucket F2: 7 JSON-corrupted rules (Y168-Y174)~~ | ✅ CLOSED 2026-06-01 -- dict-result `effect` extracted, conditions stored, rules re-validated |
| ~~300C-OP-02~~ | ~~🟡 MED~~ | ~~Bucket F1: ~14 empty-composite-condition rules (Y123-Y140)~~ | ✅ CLOSED 2026-06-01 -- dict-conditions stored directly; 59 flagged rules reset + re-validated; Bucket B validator errors → PHR |
| ~~300C-OP-03~~ | ~~🟡 MED~~ | ~~70 new-schema rules without AI validation~~ | ✅ CLOSED 2026-06-01 -- 66 rules reset to pending_review + AI-validated (41 auto_approved, 25 PHR/flagged) |
| ~~300C-OP-04~~ | ~~🟡 MED~~ | ~~3 Nabhasa contradiction pairs~~ | ✅ CLOSED 2026-06-01 -- all 6 rules tagged `contradiction_resolution: strength_dependent` |
| ~~300C-OP-05~~ | ~~🟢 LOW~~ | ~~14 interpretation_too_short Nabhasa yogas~~ | ✅ CLOSED 2026-06-01 -- `short_interpretation_justified: true` set; all 14 at PHR |
| ~~300C-OP-06~~ | ~~🟢 LOW~~ | ~~3 within-book variant pairs (Y189/190, Y191/192, Y196/197)~~ | ✅ CLOSED 2026-06-01 -- conditions confirmed distinct; `variant_note` + `variant_of` added to all 10 rules |
| ~~300C-OP-09~~ | ~~🟡 MED~~ | ~~Retroactive dedup gap: positional detector post-dates original pre-ingest dedup~~ | ✅ CLOSED 2026-06-03 -- 3,400,215 pairs vs full MongoDB (10,335 rules). CLEAN: 0 matches / 0 contradictions / 0 positional conflicts. Log: `300combinations_dedup_20260603_043412.md` |
| **300C-OP-07** | **🔴 BLOCKER** | **Co-founder approval: 141 auto_approved rules await sign-off.** | **Blocked on sign-off** |
| ~~300C-OP-08~~ | ~~🟡 MED~~ | ~~18 remaining flagged: 14 tba + 4 engine conditions~~ | ✅ CLOSED 2026-06-01 -- 14 conditions encoded from Diagnostics (Y264-Y274, Y292-Y294); 4 engine deps → PHR; Y271 condition error corrected; Y294 day/night overlay stripped; all Bucket B validator errors → PHR. Final: 0 flagged. |

---

## Co-Founder Approval Queue

After resolving 300C-OP-01 (Bucket F2 re-encode) and doing minimal Bucket F1 triage:

Admin path: `/admin/library → Rules Browser → filter: auto_approved → source: 300 Combinations`

Expected sign-off queue:
- 97 auto_approved rules (primary queue)
- 145 PHR rules (secondary -- after any Bucket B patches)

---

## Version History

| Date | Version | Action | By |
|---|---|---|---|
| 2026-06-01 | v1.0 | Initial ingest: 329 rules, batch `300-combinations-v1-20260601` | CC |
| 2026-06-01 | v1.1 | OLD schema patch: 259 rules -- results/polarity/conditions → canonical KE fields | CC |
| 2026-06-01 | v1.2 | AI validation: 97 auto_approved, 145 PHR, 73 flagged, 14 pending_review, 3 contradiction pairs | CC |
| 2026-06-01 | v1.3 | Ingest notes written -- triage buckets documented, open items filed | CC |
| 2026-06-01 | v2.0 | **All 6 OPs closed.** OP-01/02: 147 rules -- dict-result effect extracted + dict-conditions stored directly. OP-03: 66 new-schema rules AI-validated (41 auto_approved). OP-04: Nabhasa pairs tagged strength_dependent. OP-05: 14 short rules → PHR. OP-06: 10 variant rules annotated. Post-triage AI validation: 41 auto_approved, 54 PHR, 29 flagged from 125-rule pool. Bucket B triage: 25 validator-error rules → PHR. tba:true: 14 decode-gap rules. **Final: 138 auto_approved / 173 PHR / 18 flagged / 0 pending_review.** | CC |
| 2026-06-01 | v3.0 | **OP-08 CLOSED.** GROUP A (14 tba rules Y264-Y274, Y292-Y294): conditions fully encoded from Diagnostic files as structured multi_trigger/multi_condition dicts; source JSONs updated; tba cleared; validated → 3 auto_approved (Y266, Y292, Y293), 6 PHR, 5 initially flagged. Post-triage: Y271 condition error corrected (Saturn aspects, not conjunct); Y294 day/night overlay stripped (interpolation, not Raman source); Y268/273/274 = Bucket B encoding-style flags → PHR. GROUP B (Y130/131/133/134): engine dep → PHR with validator_error. **Final: 141 auto_approved / 188 PHR / 0 flagged / 0 pending_review.** | CC |
