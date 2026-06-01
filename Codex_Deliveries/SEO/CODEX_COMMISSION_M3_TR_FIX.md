# Codex Commission: M3-TR-FIX -- Transit Profiles Generator Fix (v2)
> Thread: SEO Legacy (M3 section) | File: `backend/seo_m3_builders.py`
> Issued: 2026-06-02 (v2 -- first delivery partially improved L1 but introduced new L2 boilerplate)
> Scan script: `tests/echo_pace_seo20k_scan.py` | Scan report: `SEO_20K/SEO_TRACKER.md`

---

## Commission Brief (5 lines)

First delivery improved L1 from 71.2% BLOCKED → 64.3% FLAGGED -- progress, but still failing, and new L2 violations were introduced: `"excess heat choose timing"` 100%, `"one grounded weekly discipline"` 100%, `"avoid acting day strongest"` 100%. These are shared remedy/timing sentences that appear on every page regardless of planet. Fix: (1) planet-specific openers are working -- keep them, extend to ≥10 variants per planet; (2) the shared remedy block is the new L2 source -- replace with a `_hash_index(planet_slug, sign_slug, modulus=6)` selected remedy sentence drawn from a planet-specific pool (Saturn remedies must differ from Sun remedies); (3) the `watch_for` and `transit_themes` pools still share vocabulary across sign families -- add ≥3 element-aware variants (Fire/Earth/Air/Water signs get different phrasing); (4) **no sentence or 4-gram may appear on more than 1 in 10 pages (10% threshold)** -- the scanner uses 15% but target 10% to leave margin. Do NOT introduce any universal closing, disclaimer, or duration-note sentence shared across planets.

---

## 1. SEO Pages -- Module Overview

| Page Type | URL Pattern | Total Pages | Dimensions | Content Fields Scanned |
|---|---|---|---|---|
| Transit Profiles | `/transits/{planet}-in-{sign}` | 108 | 9 planets × 12 signs | `summary`, `transit_themes`, `watch_for`, `remedies`, `sign_impacts[].message`, FAQ answers |

---

## 2. Pages Impacted -- Rework Required

| Cluster | Pages Affected | Issue | Fix Required |
|---|---|---|---|
| Remedy / timing sentences | 108 / 108 | New shared sentences introduced in v1 | Planet-specific remedy pool, hash-selected per sign |
| `watch_for` / `transit_themes` | 108 / 108 | Cross-sign vocabulary still shared | Element-aware variants (Fire/Earth/Air/Water × planet) |
| FAQ answers | 108 / 108 | Partial improvement -- some phrases still shared | Extend to ≥6 variants per question, hash-selected |
| **Total impacted** | **108 / 108** | L1 64.3% FLAGGED · L2 FAIL | Targeted deepening of v1 |

**Phrases that MUST NOT appear on more than 1 page (found in v1 re-scan):**
- `"excess heat choose timing"` -- delete entirely
- `"one grounded weekly discipline"` -- delete entirely
- `"avoid acting day strongest"` -- delete entirely
- Any shared duration/timing note (e.g. "exact duration depends on...", "check your full natal chart") -- eliminate or hash-select

---

## 3. Tests -- Required Before Integration

| Test | Layer | Tool | Pass Criterion | Run Command |
|---|---|---|---|---|
| TF-IDF Cosine | L1 | `tests/echo_pace_seo20k_scan.py` | Transit Profiles worst pair **< 50%** | `python3 tests/echo_pace_seo20k_scan.py` |
| N-gram Match | L2 | `tests/echo_pace_seo20k_scan.py` | **0** four-gram violations > 15% | Same script |
| Jaccard Titles | L3 | `tests/echo_pace_seo20k_scan.py` | No title pair > 60% Jaccard | Same script |

---

## 4. Scan History

| Scan | Date | L1 | L1 Status | L2 Violations | L3 Worst Jaccard | Verdict |
|---|---|---|---|---|---|---|
| Pre-fix (original) | 2026-05-31 | 71.2% | ❌ BLOCKED | 10 at 100% | 67% | FAIL |
| v1 delivery re-scan | 2026-06-02 | **64.3%** | ⚠️ FLAGGED | 10 at 100% | 67% | ❌ FAIL -- new boilerplate introduced |
| v2 delivery (target) | -- | **< 50%** | ✅ PASS | 0 | < 60% | -- |

**Top v1 L2 violations (must be eliminated in v2):**
- `"excess heat choose timing"` -- 100%
- `"one grounded weekly discipline"` -- 100%
- `"avoid acting day strongest"` -- 100%
