# Thread Brief -- KP Astrology NLM Decode
## Status Update + Queries + Next Steps

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-28 · Status updated: 2026-05-31
> For: KP Astrology Decode Thread
> Status: **🟡 NEAR READY -- claim_axis retroactive pass 12 of ~66 corrected 2026-05-31. 54 general-scope rules confirmed legitimate. Cat B/C/G/H open items remain.**

---

## One-Liner

Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_KP_DECODE.md` for all KP Astrology KE Ingest.

---

## Status Update (2026-05-31)

`claim_axis` retroactive pass completed for 12 specifically miscategorised rules:
- P01→ `physical_appearance`
- P09-003 → `legal`
- P33-002 → `career_finance`
- P34-002 → `career`
- P55-005 → `health`
- P75-001 → `social_relationships`
- P77-001 → `career_growth`
- T09-003/009 → `travel`
- T09-004 → `education`

54 remaining "general" claim_axis rules confirmed as legitimately methodology/cross-domain -- no change needed.

Entries 248-249 T05 PDF-verified (T06 p.110) ✅.

**Remaining open items blocking final close:**
- Cat B: T05 duplicate/skipped entry numbers -- needs OCR docx or T05 PDF
- Cat C: Missing Rahu-star stubs (Swathi 131-138, Sathabisha 213-221)
- Cat G: Conditional vs direct delineation inconsistency (1 item)
- Cat H: Formatting inconsistencies (3 items)
- F-01 to F-06: Ambiguous terms batch → GAI/NLM pass pending

**Next step for ingest thread:** Resolve Cat B/C/G/H + F-01 to F-06 → then ingest.

---

---

## Current State -- What Has Been Delivered

The KP Astrology decode folder is the most mature decode thread in the Knowledge Engine.

| Metric | Count |
|---|---|
| Total files in folder | 190 |
| Rules.json files | 77 |
| Total decoded rules | 256 |
| Summary.md files | Present across chapters |
| Diagnostic.md files | Present across chapters |

**The core decode is complete.** No new sloka extraction or chapter decodes are required at this stage.

---

## What Is Pending (Retroactive Actions)

### Pending Action 1 -- `claim_axis: "longevity"` Population

Approximately **20 rules across ~15 files** relate to longevity, death timing, or lifespan determination but do not currently carry `claim_axis: "longevity"`.

The `claim_axis: "longevity"` value is now confirmed present in the schema (`VALID_CLAIM_AXES` in `backend/ke_schema_constants.py`).

**Files with likely longevity rules (identified from decode audit):**

These are rules whose conditions involve:
- 8th house / 8th lord placements
- Maraka planets / lords of 2nd and 7th
- Span of life calculations
- Badhaka placements affecting lifespan
- Death-timing transit indicators

The thread should audit all 77 Rules.json files and populate `claim_axis: "longevity"` on every rule that determines, modifies, or predicts lifespan or death timing.

**This is non-blocking for other threads -- but should be completed before the KP decode is declared fully closed.**

---

### Pending Action 2 -- JSON Parse Error in KP3_ChT04 (NOW FIXED)

The JSON parse error in `KP3_ChT04_Rules.json` was flagged in the KE-SCHEMA-AMENDMENT-PD1 commission and confirmed fixed in the schema amendment delivery. The thread does not need to action this -- it is resolved.

---

### Pending Action 3 -- Custom Condition Type Decision

The KP decode uses **5 non-standard condition types** not present in other decode threads:

| Condition type | Usage in KP decode |
|---|---|
| `kp_significator` | Planet's house significator chain |
| `kp_sub_lord` | Sub-lord of a cusp or planet |
| `kp_badhaka` | Badhaka planet identification |
| `kp_longevity_factor` | KP-specific longevity weighting |
| `planet_conjunction` | Standard -- already in schema |
| `planet_in_house` | Standard -- already in schema |
| `planet_in_sign` | Standard -- already in schema |

The **5 KP-custom types** are functional in the current rules and correctly describe KP-specific conditions. However, **`kp_longevity_factor` requires a schema-level decision:**

> **Q: Should `kp_longevity_factor` be added to the master `VALID_CONDITION_TYPES` list in `ke_schema_constants.py`?**
>
> Or should these rules be re-encoded using the standard `claim_axis: "longevity"` mechanism instead -- treating the condition as a standard house/planet condition and pushing the longevity claim to the `claim_axis` field?

This is a schema philosophy question. The `kp_longevity_factor` type currently acts as both a condition type AND a claim signal, which is redundant if `claim_axis` is populated correctly.

**Temple Team recommendation:** Re-encode `kp_longevity_factor` conditions as standard `planet_in_house` or `planet_in_sign` conditions + `claim_axis: "longevity"`. This keeps the schema clean across all decode threads and avoids a KP-only custom type that the rule engine would need special handling for.

**However, this is a medium-term exercise. It is NOT blocking anything currently.**

---

## Schema Notes

**Schema constants source of truth:** `backend/ke_schema_constants.py`
**Schema validation layer:** `backend/knowledge_schema.py`

The following schema additions (from KE-SCHEMA-AMENDMENT-PD1) are relevant to existing KP rules:

| Schema addition | KP application |
|---|---|
| `claim_axis: "longevity"` | Retroactive population on ~20 longevity rules |
| `claim_axis: "longevity_trend"` | May apply to rules that indicate longevity quality (long/short life indicators) rather than precise timing |

No new condition types, engine dependencies, or scope values are required for KP.

---

## Cross-Thread Dedup Status

| Dedup target | Status |
|---|---|
| KP × Phaladeepika | Cannot run -- Phaladeepika decode not yet started |
| KP × BPHS Vol 1 | Cannot run -- BPHS Vol 1 not yet decoded |
| KP × LongevityUnnatural | Can run when LongevityUnnatural is complete |
| KP × 300 Combinations | Can run when 300 Combinations is complete |

Leave `cross_text_matches: null` on all KP rules for now. The automated dedup script will be commissioned separately once partner threads are complete.

**High overlap expected:**
- KP longevity rules × LongevityUnnatural rules: Moderate-High overlap
- KP Badhaka rules × 300 Combinations: Low overlap (KP Badhaka formulation is more specific)

**When dedup runs happen (at ingest time), review THREE sections in the JSON report:**
1. `matches` -- lexical similarity duplicates (TF-IDF threshold 0.82)
2. `contradictions` -- same condition signature, opposite polarity
3. `positional_conflicts_detail` -- same planet×house or planet×sign, different claimed result (NEW 2026-06-02). `positional_polarity_conflict` = explicit +/− clash (high confidence); `positional_alternate_result` = same condition, dissimilar result text. Flag all for TT review. KP rules are heavily positional (planet in house/sign) so this section will likely produce the most flags.

**At ingest time -- CRITICAL (KOP-03):**
> Set `approval_status = "pending_review"` on every rule at upload -- NOT `"pending_human_review"`. The AI validator (`validate_rules.py`) queries `pending_review`. If you upload `pending_human_review`, the validator silently finds 0 rules and the AI quality check is skipped.

> Run pre-upload validation before touching MongoDB:
> ```bash
> python3 backend/scripts/validate_rules.py --json-file /tmp/kp_dry_run.json --batch-id kp_astrology_v1
> ```
> KP methodology rules (sub-lord theory, cusp analysis, Badhaka) will be flagged as Bucket B by the validator (which applies BPHS standards). These are framework mismatches -- set `validator_error:True` + PHR, not genuine flags. See INGEST_PROCESS_BRIEF.md KOP-04.

---

## Open Queries -- Please Confirm

| # | Query | Action owner |
|---|---|---|
| Q1 | Retroactive `claim_axis` pass -- can the thread complete a self-audit of all 77 files and populate `claim_axis: "longevity"` on relevant rules? Estimated effort: 1 focused session. | **KP decode thread** |
| Q2 | `kp_longevity_factor` condition type -- does the thread prefer to keep it as a KP-custom type (requires schema addition), or re-encode to standard conditions + `claim_axis: "longevity"`? | **KP decode thread to propose -- Temple Team to confirm** |
| Q3 | Are there any chapters in the KP system that the thread considers partially decoded or under-decoded? If so, which chapters and what is missing? | **KP decode thread** |
| Q4 | The `source.sloka` format across KP files -- confirm the format being used (e.g., `"chapter.sloka"` or `"book.chapter.sloka"` or other). This is needed for the dedup script's citation matching logic. | **KP decode thread** |

---

## Immediate Next Actions

| Action | Owner | Priority |
|---|---|---|
| Self-audit all 77 files → populate `claim_axis: "longevity"` on longevity rules | KP decode thread | HIGH -- complete before thread is closed |
| Confirm `kp_longevity_factor` decision (keep custom vs re-encode) | KP decode thread + Temple Team | MEDIUM -- not blocking |
| Confirm `source.sloka` citation format | KP decode thread | MEDIUM -- needed for dedup pass later |
| Report any under-decoded chapters | KP decode thread | LOW -- only if gaps exist |

**The KP thread is the closest to completion of all active decode threads. One focused retroactive session should close it out.**

---

## Summary -- What This Thread Has Achieved

The KP Astrology decode produced 256 rules across 77 files covering the full KP system: significator chains, sub-lord theory, cusp analysis, Badhaka identification, dasha period activation, transit timing, and longevity factors. This is the single largest completed decode in the Knowledge Engine.

The retroactive `claim_axis` pass is the last outstanding action before this thread can be declared **CLOSED**.

---

*Brief prepared by Temple Team -- EverydayHoroscope, 2026-05-28*
