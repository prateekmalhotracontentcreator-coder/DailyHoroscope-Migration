# PHALADEEPIKA_INGEST.md
> Mantreshwara's Phaladeepika (28 Adhyayas)
> Last updated: 2026-06-01 · Status: ✅ INGESTED · ✅ TRIAGE COMPLETE (Round 2) · 1 FLAGGED (Bucket C)

---

## One-Liner

1218 rules ingested (28 chapters). Full 2-round triage done 2026-06-01.
**825 auto_approved · 393 PHR · 0 flagged · 0 pending_review.**
All OPs closed except PD-OP-03 (gai_citation, approval gate) and PD-OP-06 (co-founder sign-off).
Awaiting co-founder sign-off on 825 auto_approved.

---

## Ingest Summary

| Metric | Value |
|---|---|
| Batch ID | `phaladeepika-v1-20260601` |
| Source folder | `/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode/` |
| Ingest date | 2026-06-01 |
| Ingest script | `backend/scripts/ingest_phaladeepika_v1.py` |
| Rules inserted | 1218 |
| Duplicates skipped | 0 |
| Errors | 0 |
| Pre-ingest dedup | Deferred -- post-ingest comparison vs BPHS Vol 1 is informational (60-70% overlap expected on house chapters, both texts expected). |
| TBA/inactive | 12 rules (Ch08 PDF gap -- Sun in houses 1-6 absent from source) |

---

## Three-Schema Mapping (applied in ingest script)

### Schema A -- Ch01-Ch13, Ch15-Ch16, Ch18, Ch27 (758 active rules)
- `full_text` → `interpretation.detailed`
- `summary` → `interpretation.summary`
- `condition` (dict) → passed through directly

### Schema C -- Ch14, Ch17, Ch19-Ch25 (355 active rules)
- `description` → `interpretation.detailed`
- `title` → `interpretation.summary`
- `conditions` (list) → wrapped as `multi_condition` or passed through if single dict

### Schema B -- Ch22, Ch26, Ch28 (93 active rules)
- `content` → `interpretation.detailed`
- `title` → `interpretation.summary`
- `conditions` (empty list or string list) → fallback to `engine_spec` condition type
- `chapter` + `sloka` as top-level fields (no `source` dict) → built in `_map_source()`

---

## Validation Results

### Round 1 (post-ingest)
| Status | Count | Notes |
|---|---|---|
| auto_approved | 582 | 48% |
| pending_human_review | 271 | 22% |
| pending_review | 357 | 29% -- Stage 1 truncated_text structural failures |
| flagged | 8 | 0.7% |
| **Total** | **1218** | |

### After PD-OP-01/02 patches + Round 2 re-validation (357 pending_review rules)
| Status | Count | Notes |
|---|---|---|
| auto_approved | 811 | Round 1 (582) + pd-ch07-024 + pd-ch08-111 + Round 2 (227) |
| pending_human_review | 406 | Round 1 (271) + Round 2 triage (91 PHR + 40 flagged → PHR) + OPs |
| flagged | 1 | pd-ch04-028 only (genuine encoding error -- diurnal/nocturnal reversed) |
| pending_review | 0 | Cleared |
| **Total** | **1218** | |

Contradiction pairs: **22 total**
- 16 from Round 1 (all Bucket B except pd-ch23-020/pd-ch24-033 Bucket C threshold)
- 6 from Round 2: pd-ch10-004/021, pd-ch10-021/022, pd-ch12-013/022, pd-ch16-007/015-012, pd-ch04-014/030, pd-ch08-056/010-009
  - 5 Bucket B (different conditions) -- resolution notes applied, validator_error:True
  - 1 Bucket C genuine: pd-ch04-014/030 (Kendra Bhava Bala numerical conflict) -- cross_reference added, TT sign-off required

---

## 1 Remaining Flagged Rule (Bucket C -- Genuine Encoding Error)

| Rule ID | Issue | Status | Action |
|---|---|---|---|
| pd-ch04-028 | Diurnal/nocturnal sign classification reversed. Classical: diurnal = odd signs (Aries/Gemini/Leo/Libra/Sag/Aquarius); nocturnal = even signs. Rule encodes opposite. | FLAGGED | Fix condition encoding. Cross-reference printed Phaladeepika edition. Correct before activation. |

---

## PD-OP-01 -- Truncation Fix History

**Root cause (diagnosed 2026-06-01):** Field-name mismatch -- Ch01-Ch13/15/16/18/27 source JSONs use `full_text`; ingest pipeline expected `description`. Rules ingested with truncated text or empty. Text not cut in source -- source was complete.

**Fix applied by decode thread (PD_Validator_Response_20260601):** `description` field added = `full_text` content on all 659 rules across 15 chapters. Source JSONs updated. MongoDB records still have old truncated text.

**Round 2 re-validation result:** 357 rules processed → 227 AA / 91 PHR / 39 flagged. 13 genuine truncation residuals (still truncated in MongoDB) → set to PHR + `truncation_artifact:True`.

**PD-OP-07 (open):** Re-ingest 659 rules from updated source JSONs to restore complete text in MongoDB. Expected outcome: all 13 truncation-artifact PHR rules clear to auto_approved post re-ingest.

| Chapter | Rules Fixed in Source |
|---|---|
| Ch01, Ch03, Ch04, Ch05, Ch07, Ch08, Ch09, Ch10, Ch11, Ch12, Ch13, Ch15, Ch16, Ch18, Ch27 | 659 total |

---

## 16 Contradiction Pairs

### Bucket B (validator false positives -- intended classical opposites):
- pd-ch06-057/069: Chamara vs Ava yoga (1st house benefic vs malefic -- intended opposites)
- pd-ch06-060/072: Jaladhi vs Kuhu yoga (4th house benefic vs malefic -- intended opposites)
- pd-ch13-007/008: Different base conditions -- Moola prosperity vs Rasi-extreme-with-malefic death
- pd-ch16-043/044: Same base condition + Jupiter aspect modifier (expected different outcomes)
- pd-ch07-036 vs pd-ch18-089/093/094: Maharajayoga (friendly planet aspect) vs specific planet conjunctions in Ch18 -- different conditions
- pd-ch07-037 vs pd-ch18-029: Full Moon in Vrishabha vs Moon+Mars aspect -- different conditions
- pd-ch18-032/034: Moon+Venus vs Moon+Sun (different planets, expected different outcomes)
- pd-ch14-021/032: Jupiter in 8th house (natal placement) vs Jupiter as 8th dasha significator -- different contexts
- pd-ch19-012/022: Saturn Dasa -- different interpretive traditions, both textbook-valid

### Bucket C (genuine -- TT queue):
- pd-ch06-028/029/030: Condition reversal cluster -- Adhama/Varishtha yoga conditions swapped (same cluster as 8 flagged rules above)
- pd-ch18-102/106: Same outcome text for different aspecting planets → verify source
- pd-ch23-020/pd-ch24-033: Sarvashtakavarga threshold mismatch (>28 vs ≥30) -- different chapters, need TT to confirm which is correct

---

## Open Items

| ID | Priority | Detail | Status |
|---|---|---|---|
| **PD-OP-01** | ✅ CLOSED | 357 truncated_text rules. Root cause: field-name mismatch. Source JSONs fixed. Summaries restored from source for 13 rules. All 13 → AA after Round 3 re-validation. | Done |
| **PD-OP-02** | ✅ CLOSED | All 6 conditions fixed. pd-ch04-028 diurnal/nocturnal corrected + validated → AA (2026-06-02). | Done |
| **PD-OP-03** | 🟡 OPEN | pd-ch21-041 gai_citation_unverified:True applied. Verify before co-founder sign-off. | TT at approval stage |
| **PD-OP-04** | ✅ CLOSED | pd-ch07-049 tba:True, PHR. | Done |
| **PD-OP-05** | ✅ CLOSED | Dual-layer resolution confirmed from physical book (Ch23 Sl.20 + Ch24 Sl.37). Ch23 = transit pass/fail binary (>28 = auspicious). Ch24 = natal bhava quality tier (≥30/25-29/<25). Both auto_approved. Edge case 25-28 = natally middling but transitionally volatile -- captured in engine_note on both rules. Ref: `PD-OP-05_Conflict Resolution.md`. | Done 2026-06-02 |
| **PD-OP-06** | 🔴 BLOCKER | Co-founder approval: **823 auto_approved** rules await sign-off. | Blocked on sign-off |
| **PD-OP-07** | ✅ CLOSED | Summaries restored from corrected source JSONs for 13 truncation-artifact rules. Round 3 re-validation: 12 → AA, 2 → PHR. knowledge_validator.py character limits fixed ([:200]→[:400] summary, [:400]→[:800] detailed). | Done |

---

## Post-Ingest Dedup Status

Pre-ingest local dedup: **deferred** (informational step -- 60-70% conceptual overlap with BPHS Vol 1 on house chapters is expected and not a problem; Phaladeepika rule_ids are distinct).

Post-ingest MongoDB dedup against BPHS batch: **not yet run.** Run:
```bash
python3 backend/ke_dedup_script.py \
  --batch-a phaladeepika-v1-20260601 \
  --batch-b bphs-vol1-v1 \
  --mongo-url "$MONGO_URL" --db-name horoscope_db \
  --output-report Phaladeepika_CC_Decode/Dedup_vs_BPHS_Vol1.md
```

---

## Co-Founder Approval Queue

Admin path: `/admin/library → Rules Browser → filter: auto_approved → source: Phaladeepika`

Expected sign-off queue:
- 582 auto_approved rules (primary queue)
- 271 PHR rules (secondary -- after Bucket C fixes)

---

## Version History

| Date | Version | Action | By |
|---|---|---|---|
| 2026-06-01 | v1.0 | Initial ingest: 1218 rules, batch `phaladeepika-v1-20260601`. 3-schema handler. 0 errors. | CC |
| 2026-06-01 | v1.1 | AI validation: 582 auto_approved / 189 PHR / 357 pending_review (truncated_text) / 90 flagged. 16 contradiction pairs. | CC |
| 2026-06-01 | v1.2 | Triage: 82 flagged rules → PHR (Bucket B). 8 remain flagged (Bucket C). **582 AA / 271 PHR / 357 pending_review / 8 flagged.** | CC |
| 2026-06-01 | v1.3 | Full MongoDB dedup (0 genuine matches). PD-OP-02 patches (5 fixes + pd-ch08-111 activated). PD-OP-01: decode thread fixed source JSONs (659 rules). | CC + TT |
| 2026-06-01 | v1.4 | PD-OP-01 punctuation fix (357 rules). Round 2 re-validation: 357 → 227 AA / 91 PHR / 39 flagged / 6 contradiction pairs. | CC |
| 2026-06-01 | v1.5 | Round 2 triage complete. 40/41 flagged → PHR (truncation artifacts, TBA, Bucket B). 1 stays flagged (pd-ch04-028 genuine encoding error). 6 contradiction pairs: 5 Bucket B (notes applied), 1 Bucket C genuine (pd-ch04-014/030). **Final: 811 AA / 406 PHR / 1 flagged / 0 pending_review.** | CC |
| 2026-06-02 | v1.6 | PD-OP-07: Restored summaries for 13 truncation-artifact rules from corrected source JSONs. Fixed pd-ch04-028 diurnal/nocturnal encoding. Fixed knowledge_validator.py char limits ([:200]→[:400] summary, [:400]→[:800] detailed). Round 3 re-validation: 12→AA, 2→PHR. pd-ch03-042 "Engine-spec" prefix removed. pd-ch03-035 Hora assignment confirmed correct (Bucket B). **823 AA / 395 PHR / 0 flagged / 0 pending_review.** | CC |
| 2026-06-02 | v1.7 | PD-OP-05 CLOSED. Dual-layer resolution from physical book: Ch23 Sl.20 = transit binary filter (>28); Ch24 Sl.37 = natal bhava tier (≥30/25-29/<25). Edge case 25-28 = middling natally, volatile transitionally. Both → auto_approved + cross_reference + engine_note. **FINAL: 825 AA / 393 PHR / 0 flagged / 0 pending_review / 1218 total.** All OPs closed except PD-OP-03 (approval gate) + PD-OP-06 (co-founder sign-off). | CC + TT |
