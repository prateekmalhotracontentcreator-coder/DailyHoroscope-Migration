# 300HOROSCOPES_INGEST.md
> 300 Horoscopes Vol. 1 -- MK Viswanath Nair | KP Jyotish
> Last updated: 2026-06-02 · Status: ✅ INGESTED · ⏳ TT REVIEW (pending_human_review, AI validator bypassed)

---

## One-Liner

57 KP Jyotish rules ingested 2026-06-02.
**57 pending_human_review · 51 active · 6 superseded (active:False) · 2 TT-decision flags.**
AI validator bypassed -- TT reviews at co-founder approval stage.

---

## Ingest Summary

| Metric | Value |
|---|---|
| Batch ID | `300_horoscopes_vol1_v1` |
| Source folder | `/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredHoroscopes_CC_Decode/` |
| Ingest date | 2026-06-02 |
| Ingest script | `backend/scripts/ingest_300horoscopes_v1.py` |
| Rules inserted | 57 |
| Duplicates skipped | 0 |
| Errors | 0 |
| Pre-ingest dedup | ✅ 0 matches / 0 contradictions vs 10,414 MongoDB rules (593,598 pairs) |
| Report | `H300_Dedup_vs_FullMongoDB.md` |
| Case studies | NOT ingested -- H300_TestVectors.json contains benchmark chart vectors, not rules |

---

## Schema Mapping (single schema -- all 5 JSON files identical)

| Source field | MongoDB field |
|---|---|
| `full_text` (top-level) | `interpretation.detailed` |
| `summary` (top-level) | `interpretation.summary` |
| `condition` (dict) | `condition` (pass-through) |
| `result` (dict) | `result` (pass-through) |
| `source["batch_id"]` | **OVERRIDDEN** → `300_horoscopes_vol1_v1` |
| `approval_status` | **OVERRIDDEN** → `pending_human_review` |

---

## Validation Status

**AI validator bypassed.** Per thread brief: all 57 rules enter as `pending_human_review`.
This batch goes directly to TT review at co-founder approval stage.

| Status | Count |
|---|---|
| pending_human_review | 57 |
| auto_approved | 0 |
| flagged | 0 |
| pending_review | 0 |
| **Total** | **57** |

---

## Special Rule Handling

### 6 Superseded Rules (active: False)

Intra-book duplicates -- same rule stated multiple times across sections:

| Rule ID | Reason |
|---|---|
| h300-s02-010 | Aspects reiteration -- overlaps h300-s01a-001 to 005 + h300-s01a-010 |
| h300-s02-011 | Rahu/Ketu 4-level hierarchy -- 2nd statement (overlaps h300-s01a-011) |
| h300-s02-012 | Planets in node stars -- 2nd statement (overlaps h300-s01a-012) |
| h300-s04-003 | Rahu/Ketu 4-level hierarchy -- 3rd statement (overlaps s01a-011, s02-011) |
| h300-s04-006 | Planets in node stars -- 3rd statement (overlaps s01a-012, s02-012) |
| h300-s04-007 | Aspects summary reiteration -- overlaps s01a-001..005, s02-010 |

### 2 TT-Decision Duplicate Candidates (pending_review: True)

| Rule ID | Issue | Decode Notes |
|---|---|---|
| h300-s01a-009 | Lagna/Moon sign rule may conflict with KP's strict Placidus lagna doctrine | See `decode_notes` on rule in MongoDB |
| h300-s03-004 | Short-dasha planet grouping (Sun/Mars/Ketu/Moon) -- verify vs Longevity book categorisation | See `decode_notes` on rule in MongoDB |

---

## Pre-Ingest Dedup Results

| Comparison | Pairs Evaluated | Matches | Contradictions |
|---|---|---|---|
| H300 vs Full MongoDB (10,414 rules) | 593,598 | 0 | 0 |

Note: The H300_DuplicateCandidateReport.md (47 cross-book candidates vs Longevity book) was pre-computed by the decode thread. These are informational flags for TT at approval stage -- NOT blocking ingest. The ke_dedup_script.py full-collection dedup (0 matches) is the authoritative pre-ingest check.

---

## Cross-Book Duplicate Report Summary

File: `H300_DuplicateCandidateReport.md`

| Category | Count | Action |
|---|---|---|
| `merge` candidates | 29 | TT decision at approval: designate one as canonical, deactivate the other |
| `keep-both` (complementary) | 16 | Both wordings add independent value -- retain both |
| `needs-human-call` (TT decision) | 2 | h300-s01a-009, h300-s03-004 -- flagged with `pending_review:True` + `decode_notes` |

---

## Case Studies

File: `H300_CaseStudies_BenchmarkLog.md`

**15 case studies -- NOT ingested as rules.** Protocol: zero rules extracted from case studies.
Each case study is a KP principle validation benchmark, validating specific rule_ids
against real chart data (15 individuals: presidents, spiritual leaders, ordinary citizens,
foreign nationals). Used for KP Oracle accuracy benchmarking only.

Validated rule_ids (most cited):
- h300-s04-003 (Rahu/Ketu 4-level) -- 5 cases
- h300-s02-001 (6-column bhava method) -- 4 cases
- h300-s01a-007 (dasha/bhukti timing) -- 4 cases
- h300-s02-009 (star lord cascade) -- 4 cases

---

## Open Items

| ID | Priority | Detail | Status |
|---|---|---|---|
| **H300-OP-01** | 🟡 TT | h300-s01a-009 -- lagna/moon sign rule KP orthodoxy decision | TT at approval stage |
| **H300-OP-02** | 🟡 TT | h300-s03-004 -- short-dasha planet grouping vs Longevity categorisation | TT at approval stage |
| **H300-OP-03** | 🟢 LOW | 47 cross-book dedup decisions (29 merge-safe, 16 keep-both) at approval stage | TT at approval stage |
| **H300-OP-04** | 🟢 LOW | Co-founder sign-off on 51 active rules (pending_human_review → approved) | Blocked on TT sign-off |

---

## Version History

| Date | Version | Action | By |
|---|---|---|---|
| 2026-06-02 | v1.0 | Initial ingest: 57 rules, batch `300_horoscopes_vol1_v1`. Single-schema handler. 6 superseded, 2 TT-decision flags. Pre-ingest dedup: 0 matches vs 10,414 MongoDB rules. | CC |
