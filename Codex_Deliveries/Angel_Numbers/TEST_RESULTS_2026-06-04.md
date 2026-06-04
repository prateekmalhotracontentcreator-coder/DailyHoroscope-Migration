# Angel Numbers -- Full Test Results Record
> Date: 2026-06-04
> Purpose: Permanent audit trail for all compliance and copyright tests run before sign-off.
> Referenced in: `Codex_Deliveries/Angel_Numbers/TRACKER.md` · `#2_MASTER_TRACKER.md`

---

## Module State at Test Date

| Field | Value |
|---|---|
| Data generator version | ANGEL-3 (`backend/angel_numbers_data.py`, committed `2dbea98`) |
| Collections live | `angel_number_core` (1,000 docs) · `angel_number_intents` (9,000 docs) |
| Frontend pages live | `/angel-numbers` · `/angel-numbers/:number` · `/angel-numbers/:number/:intent` |
| Browser smoke test | ✅ Cleared by TT 2026-06-04 |

---

## TEST 1 -- ECHO/PACE Internal Compliance (L1-L3)

**Script:** `backend/scripts/verify_angel_numbers_compliance.py`
**Run date:** 2026-06-04
**Data version:** ANGEL-3

### Layer 1 -- TF-IDF Cosine Similarity

Gate: all clusters < 40% | Flagged >= 50% | Blocked >= 70%
Sample: 50 numbers

| Cluster | Worst Pair | Result |
|---|---|---|
| career | 38.8% | ✅ PASS |
| core | 33.3% | ✅ PASS |
| family | 39.9% | ✅ PASS |
| health | 39.9% | ✅ PASS |
| love | 39.3% | ✅ PASS |
| manifestation | 39.7% | ✅ PASS |
| new-beginnings | 38.7% | ✅ PASS |
| protection | 38.6% | ✅ PASS |
| spiritual-growth | 39.7% | ✅ PASS |
| twin-flame | 38.6% | ✅ PASS |
| **GLOBAL WORST** | **39.9%** | ✅ **PASS** |

### Layer 2 -- N-gram Phrase Match (stop-word filtered)

Gate: no 4+ word phrase in > 15% of records

| Result | Detail |
|---|---|
| ✅ PASS | No violations found |

### Layer 3 -- Jaccard Heading / Key Themes Match

Gate: worst pair Jaccard < 75%

| Result | Detail |
|---|---|
| ✅ PASS | Worst pair = 55.6% (< 75% threshold) |

**OVERALL L1-L3: PASS -- all 3 layers within tolerance.**

---

## TEST 2 -- COPYRIGHT SIMILARITY vs REFERENCE PDFs

**Script:** `tests/copyright_angel_vs_books.py`
**Report:** `tests/copyright_angel_report.json`
**Run date:** 2026-06-04 02:32 UTC

### Reference PDFs

| PDF | Words | Sentences |
|---|---|---|
| Kyle Gray -- Angel Numbers | 29,118 | 1,908 |
| Fortuna Noir -- Angel Numbers | 20,284 | 1,263 |

### Our Corpus Tested

| Field | Value |
|---|---|
| Numbers | 111, 222, 333, 444, 555, 666, 777, 888, 999, 1111, 1212, 1234, 1010, 123, 456, 789 |
| Page types | Core + love + career + twin-flame + spiritual-growth + manifestation |
| Pages tested | 96 |
| Our sentences | 1,042 |
| Total sentence comparisons | 1,042 × 3,171 = 3,304,482 pairs |

### Test A -- Verbatim N-gram Match (4+ meaningful words)

| PDF | Result | Detail |
|---|---|---|
| Kyle Gray | ✅ PASS | 0 verbatim matches |
| Fortuna Noir | ✅ PASS | 0 verbatim matches |

### Test B -- TF-IDF Cosine Similarity (our pages vs PDF paragraphs)

Thresholds: FAIL >= 40% | HIGH RISK >= 25%

| PDF | FAIL (>= 40%) | HIGH RISK (>= 25%) | Result |
|---|---|---|---|
| Kyle Gray | 0 | 0 | ✅ PASS |
| Fortuna Noir | 0 | 0 | ✅ PASS |

### Test C -- Sentence-level Jaccard Token Overlap

Thresholds: FAIL >= 50% | HIGH RISK >= 30%

| PDF | FAIL (>= 50%) | HIGH RISK (>= 30%) | Result |
|---|---|---|---|
| Kyle Gray | 0 | 0 | ✅ PASS |
| Fortuna Noir | 0 | 1 (WATCH) | ✅ PASS |

**WATCH detail (Fortuna Noir):**

| Field | Value |
|---|---|
| Our page | `core/1111` |
| Our sentence | "Angel number 1111 highlights stability, order, and dependable structure." |
| PDF sentence | "Like the core number 4, angel number 444 is about stability and dedication." |
| Jaccard score | 30.0% |
| Assessment | Both sentences describe the same numerological concept: 4-energy = stability. This is factual public domain knowledge analogous to "Venus rules love" or "Saturn rules discipline." The phrasing is distinct. **Not a copyright risk.** |

### Overall Copyright Verdict

```
PASS -- no copyright threshold breached. Content is sufficiently original.
```

---

## TEST 3 -- LAYER G SERPER (Google Similarity)

**Script:** `tests/echo_pace_angel_serper_detail.py`
**Status:** PENDING -- TT to run with Serper key
**Command:** `Serper_Default_key=YOUR_KEY python3 tests/echo_pace_angel_serper_detail.py`
**Credits:** ~10 Serper credits
**Report output:** `tests/angel_serper_detail_report.json`

**Queries planned (10 total):**

| Type | Sample | Body fields |
|---|---|---|
| Core | 111, 333, 555, 888 | `seeing_it_means + vibration` |
| Intent | 111/love, 222/twin-flame, 333/spiritual-growth, 444/protection, 555/career, 777/manifestation | `intent_message` |

**Thresholds:** BLOCKED > 40% | WATCH > 20% (matches Angel Numbers brief gate)

*This section to be updated once TT runs the script.*

---

## Sign-off Checklist

| Gate | Status | Date | By |
|---|---|---|---|
| ECHO/PACE L1-L3 PASS | ✅ | 2026-06-04 | CC |
| Copyright test PASS (both PDFs) | ✅ | 2026-06-04 | CC |
| Mongo seeded (1,000 core + 9,000 intents) | ✅ | 2026-06-04 | TT |
| API smoke test (3 endpoints live) | ✅ | 2026-06-04 | CC |
| Browser smoke test (3 page types) | ✅ | 2026-06-04 | TT |
| Layer G Serper (Google similarity) | 🟡 PENDING | -- | TT |

**Module sign-off complete when Layer G Serper returns PASS.**
