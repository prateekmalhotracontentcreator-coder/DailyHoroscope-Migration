# Codex Commission: M2-COMPAT-FIX -- Sign Compatibility Narrative Fix
> Thread: SEO Legacy (M2 section) | File: `backend/compatibility_router.py`
> Issued: 2026-05-31 | Scan script: `tests/echo_pace_seo20k_scan.py` | Scan report: `SEO_20K/SEO_TRACKER.md`

---

## Commission Brief (5 lines)

ECHO/PACE scan: Sign Compatibility L1 = 50.0% FLAGGED -- on the gate, must be brought below 50%. Root cause: `_build_summary()` and `_koota_narrative()` use fixed template strings that repeat structural vocabulary across all 144 sign-pair pages -- the only variation is the sign name substitution. Fix: (1) add ≥6 variant summary openings in `_build_summary()`, selected by `_hash_index(sign1_slug, sign2_slug, modulus=6)`; (2) add ≥4 variant phrasing pools per koota in `_koota_narrative()`, selected by hash -- the "varna vashya clear strength" and "nadi full chart review" phrases currently appear on 100% of pages; (3) add ≥3 element-pair specific framing (Fire-Earth, Air-Water, etc.) to diversify sign-pair vocabulary beyond name substitution. Single file: `backend/compatibility_router.py`.

---

## 1. SEO Pages -- Module Overview

| Page Type | URL Pattern | Total Pages | Dimensions | Content Fields Scanned |
|---|---|---|---|---|
| Sign Compatibility | `/compatibility/{sign1}-and-{sign2}` | 144 | 12C2 unique sign pairs | `summary`, koota narratives × 8 kootas, timing note |

---

## 2. Pages Impacted -- Rework Required

| Cluster | Pages Affected | Issue | Fix Required |
|---|---|---|---|
| All sign pairs | 144 / 144 | `_build_summary()` + `_koota_narrative()` fixed templates | ≥6 summary variants + ≥4 koota phrase pools, hash-selected |
| Same-element pairs (e.g., Aries-Leo) | ~36 | No element-aware framing -- shares vocabulary with cross-element pairs | Add element-pair framing pool (Fire-Fire, Fire-Earth, etc.) |
| **Total impacted** | **144 / 144** | L1 50.0% · L2 FAIL · L3 FLAGGED | Single file change |

**Boilerplate phrases appearing verbatim on 100% of pages:**
- `"varna vashya clear strength"` -- 100%
- `"full chart review nadi"` -- 100%
- `"adjustment graha maitri needs"` -- 100%

---

## 3. Tests -- Required Before Integration

| Test | Layer | Tool | Pass Criterion | Run Command |
|---|---|---|---|---|
| TF-IDF Cosine | L1 | `tests/echo_pace_seo20k_scan.py` | Sign Compatibility worst pair **< 50%** (currently on gate) | `python3 tests/echo_pace_seo20k_scan.py` |
| N-gram Match | L2 | `tests/echo_pace_seo20k_scan.py` | 0 four-gram violations > 15% frequency | Same script |
| Jaccard Titles | L3 | `tests/echo_pace_seo20k_scan.py` | No title pair > 60% Jaccard | Same script |
| Layer G | Layer G | `tests/echo_pace_seo20k_scan.py` | ≤ 1 Google hit per sampled phrase | `SERPER_API_KEY=xxx python3 tests/echo_pace_seo20k_scan.py` |

---

## 4. Current Test Scores (Scan: 2026-05-31)

| Page Type | Pages | L1 Score | L1 Status | L2 Violations | L2 Status | L3 Worst Jaccard | L3 Status |
|---|---|---|---|---|---|---|---|
| Sign Compatibility | 66 pairs | **50.0%** | ⚠️ FLAGGED (on gate) | 10 at 100% freq | ❌ FAIL | 75% | ⚠️ FLAGGED |

**Target after fix:** L1 **< 50%** (strictly below gate) · L2 = 0 violations · L3 < 60%
