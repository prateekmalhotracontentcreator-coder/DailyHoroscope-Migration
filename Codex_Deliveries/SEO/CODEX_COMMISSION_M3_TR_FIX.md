# Codex Commission: M3-TR-FIX -- Transit Profiles Generator Fix
> Thread: SEO Legacy (M3 section) | File: `backend/seo_m3_builders.py`
> Issued: 2026-05-31 | Scan script: `tests/echo_pace_seo20k_scan.py` | Scan report: `SEO_20K/SEO_TRACKER.md`

---

## Commission Brief (5 lines)

ECHO/PACE scan: Transit Profiles L1 = 71.2% BLOCKED. Root cause: `build_transit_profile_doc()` draws `transit_themes`, `watch_for`, `remedies`, and FAQ answers from a shared pool with insufficient variation -- every planet in a given sign shares structural vocabulary (e.g., all Venus transits share the same "expression taking temporary confidence" framing). Fix: (1) create ≥8 planet-specific narrative openers for each planet, selected by `_hash_index(planet_slug, sign_slug, modulus=8)`; (2) vary `watch_for` and `transit_themes` per planet-sign combination using at least 3 distinct phrasing pools -- the current `TRANSIT_HOOK_TEMPLATES` has insufficient variety; (3) vary FAQ answers (≥4 variants per question, hash-selected by planet+sign). Single file: `backend/seo_m3_builders.py`.

---

## 1. SEO Pages -- Module Overview

| Page Type | URL Pattern | Total Pages | Dimensions | Content Fields Scanned |
|---|---|---|---|---|
| Transit Profiles | `/transits/{planet}-in-{sign}` | 108 | 9 planets × 12 signs | `summary`, `transit_themes`, `watch_for`, `remedies`, `sign_impacts[].message`, FAQ answers |

---

## 2. Pages Impacted -- Rework Required

| Cluster | Pages Affected | Issue | Fix Required |
|---|---|---|---|
| Venus transits (all signs) | 12 | Narrative framing identical across signs | ≥8 planet-specific openers; hash-selected per sign |
| Saturn transits (all signs) | 12 | Same issue | Same fix |
| All other planets | 84 | Shared pool exhaustion | Expand TRANSIT_HOOK_TEMPLATES to ≥3 pools per planet |
| **Total impacted** | **108 / 108** | L1 71.2% · L2 FAIL · L3 FLAGGED | Single file change |

**Boilerplate phrases appearing verbatim on 100% of pages:**
- `"exact duration depends planet"` -- 100%
- `"expression taking temporary confidence"` -- 100%
- `"sign full natal chart"` -- 100%

---

## 3. Tests -- Required Before Integration

| Test | Layer | Tool | Pass Criterion | Run Command |
|---|---|---|---|---|
| TF-IDF Cosine | L1 | `tests/echo_pace_seo20k_scan.py` | Transit Profiles worst pair < 50% | `python3 tests/echo_pace_seo20k_scan.py` |
| N-gram Match | L2 | `tests/echo_pace_seo20k_scan.py` | 0 four-gram violations > 15% frequency | Same script |
| Jaccard Titles | L3 | `tests/echo_pace_seo20k_scan.py` | No title pair > 60% Jaccard | Same script |
| Layer G | Layer G | `tests/echo_pace_seo20k_scan.py` | ≤ 1 Google hit per sampled phrase | `SERPER_API_KEY=xxx python3 tests/echo_pace_seo20k_scan.py` |

---

## 4. Current Test Scores (Scan: 2026-05-31, sample 80/108)

| Page Type | Sample | L1 Score | L1 Status | L2 Violations | L2 Status | L3 Worst Jaccard | L3 Status |
|---|---|---|---|---|---|---|---|
| Transit Profiles | 80 | **71.2%** | ❌ BLOCKED | 10 at 100% freq | ❌ FAIL | 67% | ⚠️ FLAGGED |

**Worst pair:** `Venus in Capricorn` vs `Venus in Leo` (same planet, different sign → near-identical narrative)
**Target after fix:** L1 < 50% · L2 = 0 violations · L3 < 60%
