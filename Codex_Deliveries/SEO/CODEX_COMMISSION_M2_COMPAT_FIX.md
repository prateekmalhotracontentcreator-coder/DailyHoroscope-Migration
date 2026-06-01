# Codex Commission: M2-COMPAT-FIX -- Sign Compatibility Narrative Fix (v2)
> Thread: SEO Legacy (M2 section) | File: `backend/compatibility_router.py`
> Issued: 2026-06-02 (v2 -- first delivery regressed L1 from 50.0% → 73.9% BLOCKED)
> Scan script: `tests/echo_pace_seo20k_scan.py` | Scan report: `SEO_20K/SEO_TRACKER.md`

---

## Commission Brief (5 lines)

First delivery made things worse: L1 jumped from 50.0% FLAGGED → 73.9% BLOCKED. A new closing sentence `"unless broader charts compensate"` now appears on 74% of all 144 pages, and `"broader charts compensate well"` on 74% -- these are new boilerplate phrases introduced by v1. The element-pair framing was added but the shared vocabulary in the koota narrative blocks was not reduced. Fix: (1) **delete every occurrence of** `"unless broader charts compensate"`, `"broader charts compensate well"`, and `"pressure point unless broader"` -- these must not appear on more than 1 page each; (2) `_koota_narrative()` must produce genuinely distinct text per koota per sign-pair -- use a `_hash_index(sign1, sign2, koota_name, modulus=6)` selector drawing from ≥6 fully different sentence pools per koota (not just swapping 1-2 words); (3) `_build_summary()` must select from ≥8 structural variants (not just a different opening word), hash-selected by sign-pair; (4) **no 4-gram sequence may appear on more than 2 of the 144 pages** -- this is the hard gate. Single file: `backend/compatibility_router.py`.

---

## 1. SEO Pages -- Module Overview

| Page Type | URL Pattern | Total Pages | Dimensions | Content Fields Scanned |
|---|---|---|---|---|
| Sign Compatibility | `/compatibility/{sign1}-and-{sign2}` | 144 | 12C2 unique sign pairs | `summary`, koota narratives × 8 kootas, timing note |

---

## 2. Pages Impacted -- Rework Required

| Cluster | Pages Affected | Issue | Fix Required |
|---|---|---|---|
| All sign pairs | 144 / 144 | New closing sentence shared across 74% of pages | Delete `"unless broader charts compensate"` and variants entirely |
| Koota narratives (8 per page) | 144 / 144 | Shared 4-grams still dominate despite v1 changes | ≥6 fully distinct sentence pools per koota, hash-selected by sign-pair |
| Summary block | 144 / 144 | ≥8 structural variants required, not just opener swap | Full structural rewrites, not word substitutions |
| **Total impacted** | **144 / 144** | L1 73.9% BLOCKED (regression) · L2 FAIL · L3 FLAGGED | Structural rewrite of koota + summary blocks |

**Phrases that MUST NOT appear on more than 1 page (from v1 re-scan -- delete entirely):**
- `"unless broader charts compensate"` -- 74% of pages
- `"broader charts compensate well"` -- 74% of pages
- `"pressure point unless broader"` -- 74% of pages
- `"varna vashya clear strength"` -- was 100%, must be eliminated
- `"full chart review nadi"` -- was 100%, must be eliminated
- `"adjustment graha maitri needs"` -- was 100%, must be eliminated

---

## 3. Tests -- Required Before Integration

| Test | Layer | Tool | Pass Criterion | Run Command |
|---|---|---|---|---|
| TF-IDF Cosine | L1 | `tests/echo_pace_seo20k_scan.py` | Sign Compatibility worst pair **< 50%** | `python3 tests/echo_pace_seo20k_scan.py` |
| N-gram Match | L2 | `tests/echo_pace_seo20k_scan.py` | **0** four-gram violations > 15% frequency | Same script |
| Jaccard Titles | L3 | `tests/echo_pace_seo20k_scan.py` | No title pair > 60% Jaccard | Same script |

---

## 4. Scan History

| Scan | Date | L1 | L1 Status | L2 Violations | L3 Worst Jaccard | Verdict |
|---|---|---|---|---|---|---|
| Pre-fix (original) | 2026-05-31 | 50.0% | ⚠️ FLAGGED (on gate) | 10 at 100% | 75% | FAIL |
| v1 delivery re-scan | 2026-06-02 | **73.9%** | ❌ BLOCKED -- regression | 10 at 74% | 75% | ❌ FAIL -- got worse |
| v2 delivery (target) | -- | **< 50%** | ✅ PASS | 0 | < 60% | -- |

**Top v1 L2 violations (must be eliminated in v2):**
- `"unless broader charts compensate"` -- 74%
- `"broader charts compensate well"` -- 74%
- `"pressure point unless broader"` -- 74%
