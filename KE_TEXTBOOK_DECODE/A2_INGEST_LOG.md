# A2 Ingest Session Log
> Session start: 2026-06-01T00:00:00Z (A2 session)
> A2 account: Account 2 (Claude Code Account 2)
> Brief source: `KE_TEXTBOOK_DECODE/A2_INGEST_BRIEF.md`

---

## Phase 1 -- Environment Audit

- [x] A2_INGEST_BRIEF.md read
- [x] TEMPLE_TRACKER.md read (via INGEST_SUMMARY.md)
- [x] KE_TEXTBOOK_DECODE/INGEST_SUMMARY.md read
- [x] .claude/ke/ingest/BPHS_VOL1_INGEST.md read
- [x] .claude/ke/ingest/BPHS_VOL2_INGEST.md read
- [x] backend/knowledge_schema.py read (lines 1-150)
- [x] backend/ke_schema_constants.py read (full)
- [x] backend/ke_dedup_script.py read (full)
- [x] Python env verified: Python 3.9.6 | pymongo 4.16.0 | motor 3.7.1 | pydantic 2.11.3
- [x] MONGO_URL: confirmed (provided directly by TT)
- [x] MongoDB baseline count recorded -- see table below
- [x] Decode folder audit complete -- see table below

### MongoDB Baseline (2026-06-01)

| Metric | Count |
|---|---|
| Total rules | 8,867 |
| pending_review | 604 |
| pending_human_review | 2,275 |
| approved | 470 |
| auto_approved | 3,800 |
| flagged | 1,157 |
| Import batches tracked | 2 |

### Already Ingested (confirmed via MongoDB)

| Book | Batch ID | Rules | Status |
|---|---|---|---|
| BPHS Vol 1 Phase 1 (Ch12-44) | old scripts (no batch tracking) | ~1,069 (source_book=null) | ✅ In MongoDB |
| BPHS Vol 1 Phase 2 (Ch03-11, Ch25-33) | `bphs-vol1-phase2-v1-20260601` | 696 | ✅ In MongoDB |
| BPHS Vol 2 (Ch49-51) | `bphs-vol2-ch49-51-v1` | 249 | ✅ In MongoDB |

### Decode Folder Rule Counts (2026-06-01)

| Book | Files | Total Rules | Active Rules | In MongoDB? |
|---|---|---|---|---|
| BPHS_Vol1 | 81 | 1,456 | 1,456 | ✅ FULLY INGESTED |
| BPHS_Vol2 | 7 | 354 | 353 | ✅ INGESTED (Ch49-51: 249 rules) |
| 300_Combinations | 22 | 329 | 329 | ❌ NOT YET INGESTED |
| 300_Horoscopes | 5 | 57 | 57 | ❌ NOT YET INGESTED |
| Longevity_Unnatural | 7 | 44 | 44 | ❌ NOT YET INGESTED |
| Medical_Astrology | 20 | 270 | 270 | ❌ NOT YET INGESTED |
| Phaladeepika | 28 | 1,218 | 1,206 | ❌ NOT YET INGESTED |
| **TOTAL** | **170** | **3,728** | **3,715** | -- |

### Notes

- BPHS Vol 2 folder has legacy Part files (Ch49_Part1.json=25, Ch49_Part2.json=18) alongside master Ch49_Rules.json=154. Already ingested from master files only (per `ingest_bphs_vol2_ch49_51.py`). No action needed.
- BPHS Vol 1 folder has superseded bare 0-rule files for Ch16/17/18/20/24/32/33. These have 0 rules and will be skipped by the ingest script.
- INGEST_SUMMARY.md shows BPHS Vol 2 as "🟢 READY" but it is actually already in MongoDB (249 rules confirmed). INGEST_SUMMARY.md update needed (Phase 6 action).
- 300 Combinations `approval_status` in source JSON = `"pending_human_review"` -- ingest script overwrites to `"pending_review"` per L1 gotcha.

---

## Phase 2 -- Ingest Scripts Written

- [x] `backend/scripts/ingest_from_json_folder.py` -- generic ingest script (primary deliverable)
- [x] `backend/scripts/audit_decode_folders.py` -- pre-ingest audit
- [x] `backend/scripts/validate_ingest_batch.py` -- post-ingest structural validator

---

## Phase 3 -- Dedup

- [x] Dedup_Reports/ folder created: ✅ `KE_TEXTBOOK_DECODE/Dedup_Reports/`
- [x] **300 Combinations dedup (MongoDB export method)** → `dedup_300combo_vs_mongodb.json` -- 0 matches, 0 contradictions vs 9,196 MongoDB rules ✅
- [ ] Run 1 (local): 300_Combinations vs BPHS_Vol1 → `dedup_300combo_vs_bphs1.json` (SKIP -- covered by MongoDB export dedup above)
- [ ] Run 2 (local): 300_Combinations vs BPHS_Vol2 → `dedup_300combo_vs_bphs2.json` (SKIP -- covered by MongoDB export dedup above)
- [ ] Run 3: 300_Horoscopes vs BPHS_Vol1 → `dedup_300horo_vs_bphs1.json`
- [ ] Run 4: 300_Horoscopes vs BPHS_Vol2 → `dedup_300horo_vs_bphs2.json`
- [ ] Run 5: 300_Horoscopes vs 300_Combinations → `dedup_300horo_vs_300combo.json`
- [ ] Run 6: Longevity_Unnatural vs BPHS_Vol1 → `dedup_lu_vs_bphs1.json`
- [ ] Run 7: Longevity_Unnatural vs BPHS_Vol2 → `dedup_lu_vs_bphs2.json`
- [ ] Run 8: Medical_Astrology vs BPHS_Vol1 → `dedup_medastro_vs_bphs1.json`
- [ ] Run 9: Medical_Astrology vs BPHS_Vol2 → `dedup_medastro_vs_bphs2.json`
- [ ] Run 10: Medical_Astrology vs Longevity_Unnatural → `dedup_medastro_vs_lu.json`
- [ ] Run 11: Phaladeepika vs BPHS_Vol1 → `dedup_pd_vs_bphs1.json`
- [ ] Run 12: Phaladeepika vs BPHS_Vol2 → `dedup_pd_vs_bphs2.json`
- [ ] Run 13: Phaladeepika vs 300_Combinations → `dedup_pd_vs_300combo.json`
- [ ] Run 14: Phaladeepika vs 300_Horoscopes → `dedup_pd_vs_300horo.json`
- [ ] Run 15: Phaladeepika vs Medical_Astrology → `dedup_pd_vs_medastro.json`
- [ ] Run 16: BPHS_Vol1 vs BPHS_Vol2 → `dedup_bphs1_vs_bphs2.json`
- [ ] `ke_contradiction_pairs_master.md` produced

---

## Phase 4 -- Live Ingest

| Book | Batch ID | Rules Inserted | Duplicates | Errors | Validated |
|---|---|---|---|---|---|
| 300 Combinations | `300-combinations-v1-20260601` | 329 | 0 | 0 | ✅ Stage 1+2+3 |

---

## Phase 5 -- Validation

| Book | Batch ID | Structural Check | AI Validation | auto_approved | pending_human_review | flagged | pending_review |
|---|---|---|---|---|---|---|---|
| 300 Combinations | `300-combinations-v1-20260601` | ✅ 0 failures | ✅ Claude AI | **141** | **188** | **0** | **0** |

### 300 Combinations Validation Notes (final -- post OP-08)
- **Structural (Stage 1):** 0 failures. All 329 rules have `rule_id`, `source_book`, `source.batch_id`, `interpretation.detailed`.
- **AI Quality (Stage 2):** Multi-pass validation. Initial: 97 AA / 145 PHR / 73 flagged / 14 pending_review. After all OPs: 141 AA / 188 PHR / 0 flagged / 0 pending_review.
- **Contradictions (Stage 3):** 3 pairs detected. All Nabhasa yoga cross-pairs (Y074/Y078, Y080/Y090, Y082/Y088). All `strength_dependent` per L5 rule. No rejections.
- **Post-ingest patches applied:**
  - `patch_300combo_old_schema.py` → 259 OLD-schema rules (results/polarity/conditions → canonical KE fields)
  - `patch_300combo_all_open_items.py` → OP-01 through OP-06 (dict-result extraction, dict-condition mapping, re-validation, Nabhasa pairs, short interps, variant pairs)
  - `patch_300combo_op08.py` → OP-08 (14 tba conditions added; 4 engine-dep → PHR; source JSONs updated)
- **OP-08 final triage (Y264-Y274, Y292-Y294 + Y130-Y134):** See `.claude/ke/ingest/300_COMBINATIONS_INGEST.md` v3.0 for full detail. Key learnings:
  - Conditions marked `None` in source JSON are often fully documented in Diagnostic files -- always check Diagnostics before marking `tba: true` permanently.
  - When AI validator says "not in standard texts" for a Raman 300 Combinations rule, it's Bucket B -- validator is comparing to BPHS, a different text.
  - Speculative metadata fields (engine_note overlays like day/night modifiers) must be stripped if not confirmed in the source text.
  - Condition encoding errors (e.g., Saturn "in 2/12" vs Saturn "aspects 2/12") are Bucket C and must be corrected, not just PHR'd.

---

## Phase 6 -- Tracking Updates

- [x] BPHS_VOL1_INGEST.md confirmed current (no new action needed -- already FULLY INGESTED)
- [x] BPHS_VOL2_INGEST.md updated -- Ch49-51 Phase 2 ingest documented, stale "Ch 49-51 EXCLUDED" note removed
- [x] `.claude/ke/ingest/300_COMBINATIONS_INGEST.md` created (2026-06-01) → updated to v3.0 post OP-08
- [ ] `.claude/ke/ingest/300_HOROSCOPES_INGEST.md` -- pending that book's ingest
- [ ] `.claude/ke/ingest/LONGEVITY_UNNATURAL_INGEST.md` -- pending that book's ingest
- [ ] `.claude/ke/ingest/MEDICAL_ASTROLOGY_INGEST.md` -- pending that book's ingest
- [ ] `.claude/ke/ingest/PHALADEEPIKA_INGEST.md` -- pending that book's ingest
- [x] `INGEST_SUMMARY.md` updated -- P1-3 final stats (141 AA / 188 PHR / 0 flagged) + footer updated
- [x] `Codex_Deliveries/Knowledge_Engine/TRACKER.md` updated -- v2.19, Rules in DB 9,525+
- [x] `TEMPLE_TRACKER.md` KE module row updated -- 300 Combinations TRIAGE COMPLETE, 9,525+ rules

---

## Phase 7 -- OP-08 Closure (300 Combinations)

- [x] Diagnostic files read: `Combo_Y264-287_Diagnostic.md`, `Combo_Y288-300_Diagnostic.md`, `Combo_Y129-143_Diagnostic.md`
- [x] `patch_300combo_op08.py` written + dry-run verified
- [x] GROUP A (14 rules): conditions patched from Diagnostics. Source JSONs `Combo_Y264-287_Rules.json` + `Combo_Y288-300_Rules.json` updated. Rules reset to `pending_review`.
- [x] GROUP B (4 rules): Y130/131/133/134 patched to PHR + `validator_error:true` + `engine_dependency_required:true`
- [x] AI validation: 3 auto_approved (Y266, Y292, Y293) · 6 PHR · 5 flagged (mid-triage)
- [x] Mid-triage: Y271 condition error corrected (Saturn aspects, not conjunct in 2/12) → re-validated → PHR
- [x] Mid-triage: Y294 day/night overlay stripped (not from Raman text) → re-validated → flagged
- [x] Y294 flagged: validator applying BPHS standard to Raman text (Bucket B) → PHR + `validator_error:true`
- [x] Y268/273/274 flagged: encoding style flags only (Bucket B) → PHR
- [x] **Final: 141 auto_approved / 188 PHR / 0 flagged / 329 total**
- [x] `300_COMBINATIONS_INGEST.md` v3.0 updated, OP-08 closed
- [x] KE TRACKER v2.19 updated
- [x] INGEST_SUMMARY.md P1-3 updated
- [x] TEMPLE_TRACKER.md updated

---

## Phase 8 -- Phaladeepika Ingest (P2-5)

- [x] Session start gate confirmed: BPHS Vol 1 Phase 1+2 ✅ in MongoDB, BPHS Vol 2 Ch49-51 ✅ in MongoDB
- [x] Schema audit complete: 3 schemas (A/C/B) across 28 chapters
- [x] `ingest_phaladeepika_v1.py` written with `_map_interpretation()`, `_map_condition()`, `_map_source()` helpers
- [x] Dry-run: 1,218 rules loaded, Issues: 0 ✅
- [x] Live upload: 1,218 inserted · 0 skipped · 0 errors (batch `phaladeepika-v1-20260601`)
- [x] `import_batches` record written
- [x] Verification: 1,218 rules confirmed in DB
- [x] AI validation (validate_rules.py): 582 auto_approved / 189 PHR / 357 pending_review (truncated_text Stage 1 failures) / 90 flagged
- [x] Triage: 82 flagged → PHR (Bucket B). 8 remain flagged (Bucket C). pd-ch07-049 → tba:true.
- [x] **Final: 582 auto_approved / 271 PHR / 357 pending_review (PD-OP-01) / 8 flagged / 1,218 total**
- [x] `PHALADEEPIKA_INGEST.md` created (`.claude/ke/ingest/`)
- [x] `INGEST_SUMMARY.md` P2-5 updated to INGESTED + TRIAGE COMPLETE
- [x] KE TRACKER v2.20 added
- [x] TEMPLE_TRACKER.md updated (10,414 rules in DB)
- [x] Full MongoDB dedup run (all 10,414 rules) -- 0 genuine matches, 0 contradictions
- [x] PD-OP-02 patches: 5/6 fixes applied (pd-ch06-028/030 corrected, pd-ch07-024 AA, pd-ch07-028 PHR, pd-ch18-102 PHR + cross_ref)
- [x] pd-ch08-111 activated (Bhava Madhya Sloka 35 content recovered)
- [x] PD-OP-01 decode thread fix: source JSONs corrected (659 rules, 15 chapters). Punctuation fix applied to 357 pending_review rules in MongoDB
- [x] Round 2 re-validation: 357 → 227 AA / 91 PHR / 39 flagged / 6 contradiction pairs
- [x] Round 2 triage: 40/41 flagged → PHR (truncation_artifact / TBA / Bucket B). pd-ch04-028 stays flagged (genuine encoding error)
- [x] 6 contradiction pairs: 5 Bucket B (resolution notes applied) / 1 Bucket C genuine (pd-ch04-014/030 cross-reference added)
- [x] **ROUND 2 FINAL: 811 AA / 406 PHR / 1 flagged (pd-ch04-028) / 0 pending_review / 1,218 total**
- [x] KE TRACKER v2.21 added · TEMPLE_TRACKER updated · PHALADEEPIKA_INGEST.md v1.5
- [x] **PD-OP-07 CLOSED**: Summaries restored from corrected source JSONs for 13 truncation-artifact rules. Round 3 re-validation: 12→AA, 2→PHR. knowledge_validator.py char limits fixed.
- [x] **pd-ch04-028 CLOSED**: Diurnal/nocturnal corrected + validated → auto_approved.
- [x] **PD-OP-05 CLOSED**: Dual-layer resolution confirmed. Ch23 Sl.20 = transit filter (>28). Ch24 Sl.37 = natal bhava tier. Edge case 25-28 = middling natally, volatile transitionally.
- [x] **FINAL: 825 AA / 393 PHR / 0 flagged / 0 pending_review / 1218 total. All CC OPs closed.**
- [x] Post-ingest dedup: deferred per PHALADEEPIKA_INGEST.md (60-70% conceptual overlap expected, informational only)

---

## Phase 9 -- 300 Horoscopes Vol 1 Ingest (P2-6)

- [x] Thread brief read: `THREAD_BRIEF_300HOROSCOPES_INGEST.md`
- [x] Schema audit complete: single schema (all 5 files), `full_text`→detailed, top-level `summary`→summary, `condition` dict, `result` dict
- [x] Case studies (H300_CaseStudies_BenchmarkLog.md): NOT rules -- benchmarks only, SKIP during ingest
- [x] Duplicate report read: 47 candidates (29 merge-safe, 16 keep-both, 2 TT-decision at approval)
- [x] S04 Diagnostic read: 6 superseded rules confirmed (h300-s02-010/011/012, h300-s04-003/006/007)
- [x] Pre-ingest dedup: MongoDB export (10,414 rules) → ke_dedup_script.py → 0 matches / 0 contradictions across 593,598 pairs ✅
- [x] Report: `H300_Dedup_vs_FullMongoDB.md`
- [x] `ingest_300horoscopes_v1.py` written with single-schema handler
- [x] Dry-run: 57 rules loaded, Issues: 0 ✅
- [x] Live upload: 57 inserted · 0 skipped · 0 errors (batch `300_horoscopes_vol1_v1`)
- [x] `import_batches` record written
- [x] Verification: 57 total / 51 active / 57 pending_human_review ✅
- [x] TT-decision rules confirmed: h300-s01a-009 (pending_review:True, decode_notes set) / h300-s03-004 (same) ✅
- [x] Superseded rules confirmed: h300-s02-010/011/012 + h300-s04-003/006/007 → active:False ✅
- [x] DB total: **10,471** rules
- [x] `.claude/ke/ingest/300HOROSCOPES_INGEST.md` created
- [x] KE TRACKER v2.24 added
- [x] TEMPLE_TRACKER.md updated (10,471 rules, 300 Horoscopes ✅)

**AI Validator bypassed** -- all 57 rules enter as `pending_human_review` per thread brief. TT reviews at approval stage.
TT actions:
- h300-s01a-009: decide keep vs deactivate (lagna/moon sign KP orthodoxy)
- h300-s03-004: verify short-dasha grouping vs Longevity book categorisation
- 47 cross-book dedup decisions (29 merge candidates, 16 keep-both) at approval stage

---

## Phase 10 -- Longevity 58-Chapter Book Ingest (P1-8) [Account 1]

- [x] Aayu gate cleared: Co-founder approved label-based aayu tagging + 66-75 edge case gate; architecture locked in `ke_schema_constants.py`
- [x] Ch36-58 rules extracted via CC thread (21 cross-chart case study rules extracted)
- [x] Multi-schema handler: NLM markdown escape format, CC decode JSON blocks, Ch12/Ch13 alternate schema, Ch36-58 pre-built JSON
- [x] `ingest_longevity_58ch.py` written (38.5KB), dry-run passes, 149 rules / Issues: 0
- [x] Pre-ingest dedup: 0 matches vs 10,471 MongoDB rules (1.56M pairs) ✅
- [x] Live upload: 149 inserted · 0 skipped · 0 errors (batch `longevity_58ch_v1`)
- [x] `import_batches` record written
- [x] Triage complete: 69 auto_approved (46%) · 80 pending_human_review (54%) · 0 flagged
  - Bucket A: 18 truncation artifacts → auto_approved
  - Bucket B: 11 validator framework errors (KP vs BPHS) + 1 contra pair → PHR
  - Bucket C: 0
- [x] DB total: **10,620** rules
- [x] KE TRACKER v2.25-v2.29 added

**TT actions:**
- 69 auto_approved rules need co-founder sign-off
- Contra pair (lon-cs-005 ↔ lon-cs-006): aparimita aayu conflicting conditions -- TT arbiter decision

---

## Phase 11 -- Longevity Unnatural Death Ingest (P1-5) [Account 1]

- [x] Pre-upload AI validation workflow via `validate_rules.py --json-file` (new tooling introduced by A1)
- [x] `ingest_longevity_unnatural_v1.py` written
- [x] `validate_ingest_batch.py` created (post-upload structural validator)
- [x] Live upload: 44 inserted · 0 skipped · 0 errors (batch `longevity_unnatural_v1`)
- [x] Triage complete: 33 auto_approved (75%) · 11 pending_human_review (25%) · 0 flagged
- [x] DB total: **10,664** rules
- [x] KE TRACKER v2.30 added
- [x] INGEST_SUMMARY P1-5 + P1-8 marked FULLY INGESTED

**TT actions:**
- 33 auto_approved rules need co-founder sign-off

---

## Phase 12 -- ke_dedup_script.py Positional Conflict Detector + Semantic Pass Spec [Account 2]

- [x] `extract_positional_key(rule)` added -- returns `("ph", planet, house)` or `("ps", planet, sign)` or None
- [x] `build_positional_conflict_entry(...)` added -- report entry builder for positional conflicts
- [x] `detect_positional_conflicts(rules_a, rules_b, score_lookup)` added -- groups by positional key, emits `positional_polarity_conflict` and `positional_alternate_result`
- [x] `parse_args()` updated -- `--skip-positional` flag added
- [x] `main()` updated -- calls detect_positional_conflicts, prints "Positional conflicts: N", adds `positional_conflicts_detail` to report JSON
- [x] Semantic pass spec written: `.claude/ke/KE_DEDUP_SEMANTIC_PASS_SPEC.md`
  - Documents why TF-IDF misses `engine_specification` rules (Jaccard 0.06-0.17 for known duplicates)
  - Proposes `sentence-transformers` (all-MiniLM-L6-v2) prototype → Claude API upgrade path
  - CLI: `--semantic-pass` opt-in flag, `semantic_duplicates_detail` in report JSON
  - Phase 2a: prototype | 2b: Claude API embeddings | 2c: extend scope
- [x] TEMPLE_TRACKER.md updated (DB total 10,664, all 3 new ingests reflected)
- [x] A2_INGEST_LOG.md updated (Phase 10, 11, 12 added)

---

## Phase 13 -- Retroactive Dedup Pipeline [Account 2]

### 13a -- Longevity 58Ch Retroactive Dedup + Patch (2026-06-03)

- [x] Root cause identified: `export_mongo_for_dedup.py` did not clear output dir before writing -- stale `Longevity_(58_Chapters)_Rules.json` from prior run caused 6 self-match false positives. Fixed: `shutil.rmtree(output_dir)` before each export.
- [x] Dedup report: `dedup_58ch_vs_mongodb_v2_positional.json` -- 75 positional conflicts triaged:
  - 6 self-match artifacts → SKIP (stale dir bug, now fixed)
  - 4 `positional_polarity_conflict` → PATCH (KP longevity negative vs Phaladeepika positive)
  - 65 `positional_alternate_result` → REVIEW-ONLY (KP longevity vs classical natal frameworks, not genuine contradictions)
- [x] `patch_58ch_positional_conflicts.py` rewritten -- triage-aware (skip self-matches, only patch polarity_conflicts, log alt_results as review-only)
- [x] Dry-run confirmed: 3 unique rules (kp-ch12-001, kp-ch12-002, kp-ch13-001) · 4 conflict notes
- [x] **Live patch applied 2026-06-03**: 3 patched / 0 skipped / 0 errors
  - `kp-ch12-001` → pending_review=True (Jupiter H7 vs pd-ch08-056)
  - `kp-ch12-002` → pending_review=True (Jupiter H1 vs pd-ch08-050 + pd-ch13-022)
  - `kp-ch13-001` → pending_review=True (Sun H11 vs pd-ch08-011)
- [x] Final DB state `longevity_58ch_v1`: 69 auto_approved · 80 PHR · 3 with pending_review=True flag
- [x] Log: `KE_TEXTBOOK_DECODE/Dedup_Reports/patch_58ch_20260603_042016_live.log`

### 13b -- Longevity Unnatural Retroactive Dedup (2026-06-03)

- [x] Source: `/Users/apple/Documents/Knowledge Engine_eBooks/LongevityUnnatural_CC_Decode` (4 files, 44 rules)
- [x] 467,280 pairs evaluated vs full MongoDB (10,620 rules)
- [x] **CLEAN**: 0 matches · 0 contradictions · 0 positional conflicts
- [x] Note: Unnatural rules have 0 planet×position keys -- methodology/timing rules, no positional conditions → nothing to conflict
- [x] No patch required
- [x] Log: `KE_TEXTBOOK_DECODE/Dedup_Reports/longevity_unnatural_dedup_20260603_041549.md`

### 13c -- 300 Horoscopes Retroactive Dedup (2026-06-03)

- [x] Source: `ThreeHundredHoroscopes_CC_Decode/` (5 files, 57 rules, batch `300_horoscopes_vol1_v1`)
- [x] 604,599 pairs evaluated vs full MongoDB (10,607 rules)
- [x] **CLEAN**: 0 matches · 0 contradictions · 0 positional conflicts
- [x] Note: 300 Horoscopes rules have 0 planet×position keys -- KP methodology/case-study rules, no positional conditions
- [x] No patch required
- [x] Log: `KE_TEXTBOOK_DECODE/Dedup_Reports/300horoscopes_dedup_20260603_042519.md`

### 13d -- 300 Combinations Retroactive Dedup (2026-06-03)

- [x] Source: `ThreeHundredCombinations_CC_Decode/` (22 files, 329 rules, batch `300-combinations-v1-20260601`)
- [x] Export excluded batch `300-combinations-v1-20260601` → 10,335 rules in MongoDB export
- [x] 3,400,215 pairs evaluated vs full MongoDB
- [x] **CLEAN**: 0 similarity matches · 0 contradictions · 0 positional conflicts
- [x] Key diagnostic: `[positional] Keyed 0 planet×position groups from A, 308 from B -- 0 shared keys`
  - 300 Combinations yoga/combination rules have no planet×position conditions -- all 329 rules have 0 `planet_in_house` / `planet_in_sign` condition types
- [x] Gap context: original pre-ingest dedup (2026-06-01) ran against 8,867 rules with no positional detector. This pass covers both the ~1,797 rule delta AND the positional conflict detector. Gap formally closed.
- [x] No patch required
- [x] Log: `KE_TEXTBOOK_DECODE/Dedup_Reports/300combinations_dedup_20260603_043412.md`
- [x] JSON report: `KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_300combinations_vs_mongodb_positional.json`
- [x] `300_COMBINATIONS_INGEST.md` OP-09 closed

### 13e -- Phaladeepika Retroactive Dedup + Patch (2026-06-03)

- [x] Source: `/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode` (28 files, 1,218 rules, batch `phaladeepika-v1-20260601`)
- [x] Export excluded batch `phaladeepika-v1-20260601` → 9,446 rules in MongoDB export
- [x] 11,505,228 pairs evaluated vs full MongoDB
- [x] Positional detector: 133 planet×position groups keyed from A, 282 from B -- **108 shared keys**
- [x] Results: 0 TF-IDF matches · 0 contradictions · **2,701 positional conflicts**
  - 0 self-match artifacts ✅ (export dir clearing working)
  - **7** `positional_polarity_conflict` → PATCH
  - 2,694 `positional_alternate_result` → REVIEW-ONLY (multi-authority cross-references, no action)
- [x] Triage of 7 genuine conflicts:
  - `pd-ch08-050` + `pd-ch13-022` vs `kp-ch12-002`: Jupiter H1 -- PD general benefic vs KP Virgo-lagna badhaka
  - `pd-ch08-056` vs `kp-ch12-001`: Jupiter H7 -- PD general vs KP Virgo-lagna badhaka
  - `pd-ch08-011` vs `kp-ch13-001`: Sun H11 -- PD general benefic vs KP Libra-lagna badhaka
  - `pd-ch08-060` vs `R-ATEXTB-JUP-11H-007`: Jupiter H11 -- cross-authority interpretation
  - `pd-ch08-030` vs `R-BRIHAT-MAR-5H-216`: Mars H5 -- B-rule is Venus/Sag-lagna rule with Mars as secondary condition
  - `pd-ch08-032` vs `R-ATEXTB-MAR-7H-004`: Mars H7 -- B-rule is multi-planet condition (Moon+Venus vs Mars+Saturn)
  - Note: conflicts 1/2/3/4 are mirror-image of the 58Ch patch (same KP rules from the other direction)
- [x] **Live patch applied 2026-06-03**: 7 patched / 0 skipped / 0 errors
  - `pd-ch08-011`, `pd-ch08-030`, `pd-ch08-032`, `pd-ch08-050`, `pd-ch08-056`, `pd-ch08-060`, `pd-ch13-022` → `pending_review=True`
- [x] Final DB state `phaladeepika-v1-20260601`: 825 AA · 393 PHR · 0 flagged · 7 with `pending_review=True` flag
- [x] Logs: `phaladeepika_dedup_20260603_044150.md` · `patch_phaladeepika_20260603_044750_live.log`

---

## Retroactive Dedup Pipeline Summary

| Batch | Rules | Pairs | Result | Action |
|---|---|---|---|---|
| Longevity 58Ch | 149 | 1,588,936 | 4 genuine polarity conflicts | ✅ Patched (kp-ch12-001/002, kp-ch13-001) |
| Longevity Unnatural | 44 | 467,280 | CLEAN | ✅ None |
| 300 Horoscopes | 57 | 604,599 | CLEAN | ✅ None |
| 300 Combinations | 329 | 3,400,215 | CLEAN | ✅ None -- gap from 2026-06-01 dedup formally closed |
| **Phaladeepika** | **1,218** | **11,505,228** | **7 genuine polarity conflicts** | ✅ **Patched** (pd-ch08-011/030/032/050/056/060, pd-ch13-022) |

### 13f -- BPHS Vol 1 Phase 2 Retroactive Dedup (2026-06-03)

- [x] Script: `retroactive_dedup_bphs_vol1_phase2.sh`
- [x] FOLDER_A: `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/` (full folder, all chapters)
- [x] Export excluded batch `bphs-vol1-phase2-v1-20260601` → 9,968 rules in MongoDB export
- [x] 14,513,408 pairs evaluated · 240 planet×position keys from A, 258 from B · 54 shared keys
- [x] Raw results: 19 similarity matches · 0 contradictions · 2,387 positional conflicts
  - 29 `positional_polarity_conflict` · 2,358 `positional_alternate_result`
- [x] **FOLDER_A caveat:** BPHS_CC_Decode contains ALL 81 chapter files (Phase 1 + Phase 2). The script loaded 1,456 rules total; only ~696 are Phase 2. Phase 1 chapters (Ch12-24, Ch27, Ch34-44) were also loaded and compared.
- [x] **Chapter classification of 29 polarity conflicts:**
  - **Phase 2 chapters (Ch03-11, Ch25-26, Ch28-33): 0 conflicts ✅**
  - Phase 1 chapters (Ch12, Ch14, Ch16, Ch17, Ch18, Ch42): 29 conflicts
- [x] **Phase 2: CLEAN** -- zero conflicts for any Phase 2 rule confirmed
- [x] **19 similarity matches:** All Phase 1 chapters (Ch13-16). Intra-BPHS ID collision: local decode file uses `bphs1-ch16-007`, MongoDB Phase 1 (old ingest) uses `R-BPHS16-008`. Same content, different ID schemes -- NOT duplicates in DB. No action needed.
- [x] **29 Phase 1 polarity conflicts:** BPHS Ch17/18 conditional-negative rules (diseases/death scenarios) vs Phaladeepika general positive placement rules. Phaladeepika side already patched (pd-ch08-* rules have `pending_review=True`). BPHS Phase 1 side (R-BPHS* IDs in MongoDB "unknown" batch) not yet patched -- requires separate script.
- [x] **Do NOT run `patch_bphs_vol1_phase2_conflicts.py`** -- script queries by Phase 2 batch ID which won't match Phase 1 rules (`R-BPHS*` IDs). All 29 would be `[SKIP] not found in batch`.
- [x] Log: `KE_TEXTBOOK_DECODE/Dedup_Reports/bphs_vol1_phase2_dedup_20260603_045313.md`
- [x] **Phase 1 BPHS patch script built:** `backend/scripts/patch_bphs_vol1_phase1_conflicts.py` -- content-based text fragment lookup, targets R-BPHS* rule IDs in "unknown" batch. Searches `interpretation.detailed` by key phrase from `rule_a_full_text`. Skips `bphs1-ch42-019` (empty A-text). Run: `python3 backend/scripts/patch_bphs_vol1_phase1_conflicts.py --mongo-url "$MONGO_URL" --dry-run`

### 13g -- BPHS Vol 2 Retroactive Dedup (2026-06-03)

- [x] Script: `retroactive_dedup_bphs_vol2.sh`
- [x] FOLDER_A: `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/` (354 local rules loaded, batch `bphs-vol2-ch49-51-v1` excluded from MongoDB export)
- [x] Export: 10,415 rules (7 source groups: 300_Combinations/Horoscopes/BPHS_Vol_1/Longevity×2/Phaladeepika/unknown)
- [x] 3,686,910 pairs evaluated · 9 planet×position groups from A, 301 from B · **2 shared keys**
- [x] **CLEAN**: 0 TF-IDF matches · 0 contradictions · 0 `positional_polarity_conflict`
- [x] 106 `positional_alternate_result` → REVIEW-ONLY, no patch:
  - `rahu in house 10` (60 pairs): `bphs2-ch50-044` (Chara Dasa Rahu state) vs 30 `unknown`-batch `R-ATEXTB-RAH-10H-*` / `R-TBA15-*` natal rules + pd-ch08-096
  - `rahu in house 4` (46 pairs): `bphs2-ch50-043` (Chara Dasa Rahu state) vs 23 `unknown`-batch `R-ATEXTB-RAH-4H-*` / `R-TBA15-*` natal rules + pd-ch08-090
  - Both are Chara Dasa planet-state rules (Ch50) sharing a positional key with natal placement rules -- cross-methodology, not genuine conflicts
- [x] **No patch required** -- `patch_bphs_vol2_conflicts.py` not needed (0 genuine conflicts)
- [x] Log: `KE_TEXTBOOK_DECODE/Dedup_Reports/bphs_vol2_dedup_20260603_051037.md`
- [x] JSON: `KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_bphs_vol2_vs_mongodb_positional.json`

---

## Retroactive Dedup Pipeline Summary

| Batch | Rules | Pairs | Result | Action |
|---|---|---|---|---|
| Longevity 58Ch | 149 | 1,588,936 | 4 genuine polarity conflicts | ✅ Patched (kp-ch12-001/002, kp-ch13-001) |
| Longevity Unnatural | 44 | 467,280 | CLEAN | ✅ None |
| 300 Horoscopes | 57 | 604,599 | CLEAN | ✅ None |
| 300 Combinations | 329 | 3,400,215 | CLEAN | ✅ None -- gap from 2026-06-01 dedup formally closed |
| **Phaladeepika** | **1,218** | **11,505,228** | **7 genuine polarity conflicts** | ✅ **Patched** (pd-ch08-011/030/032/050/056/060, pd-ch13-022) |
| BPHS Vol 1 Phase 2 | 696 | 14,513,408 | **Phase 2 CLEAN** · 29 Phase 1 conflicts (FOLDER_A included all chapters) | ✅ Phase 2: No action · Phase 1 patch script ready (`patch_bphs_vol1_phase1_conflicts.py`) |
| **BPHS Vol 2** | **249** | **3,686,910** | **CLEAN** | ✅ None · 106 cross-methodology alt_results (no action) |

**Pipeline status: 7/7 COMPLETE** ✅ · All batches retroactively deduped · BPHS Phase 1 patch (29 R-BPHS* rules, content-based lookup) ready to run separately.
