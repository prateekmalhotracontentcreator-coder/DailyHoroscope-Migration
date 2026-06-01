# Codex Commission: M3-CP-FIX -- Character Placements Generator Fix (v2)
> Thread: SEO Legacy (M3 section) | File: `backend/seo_m3_builders.py`
> Issued: 2026-06-02 (v2 -- first delivery failed re-scan, L1=94.4% BLOCKED)
> Scan script: `tests/echo_pace_seo20k_scan.py` | Scan report: `SEO_20K/SEO_TRACKER.md`

---

## Commission Brief (5 lines)

First delivery failed: L1 went from 93.4% → 94.4% (no improvement). The old boilerplate was replaced with new boilerplate -- `"time place details house"`, `"details house based placements"`, `"place details house based"` now appear on 32% of pages. The root cause is that `build_character_placement_doc()` still derives `strengths`, `challenges`, and `life_themes` from a single pool keyed only on sign+chartpoint, then appends the same house-context sentence across all 12 houses. Fix must be structural: **the body text for every page must be primarily driven by the house, not the sign.** Each of the 12 houses must have its own distinct vocabulary pool (≥6 sentences per house covering its domain -- work, relationships, home, etc.); the sign+chartpoint layer adds flavour ON TOP of the house base, not the other way around. The FAQ answers must use no shared 4-gram sequence across more than 1 in 8 pages -- build a `_hash_index(sign_slug, chartpoint_slug, house_num, answer_idx, modulus=8)` selector. Do NOT introduce any closing sentence, transition phrase, or timing note that appears on more than 2 pages.

---

## 1. SEO Pages -- Module Overview

| Page Type | URL Pattern | Total Pages | Dimensions | Content Fields Scanned |
|---|---|---|---|---|
| Character Placements | `/traits/{sign}/{chart_point}/{house}` | 432 | 12 signs × 3 chart points × 12 houses | `summary`, `overview`, `traits.strengths`, `traits.challenges`, `traits.life_themes`, FAQ answers |

---

## 2. Pages Impacted -- Rework Required

| Cluster | Pages Affected | Issue | Fix Required |
|---|---|---|---|
| All 432 pages | 432 / 432 | Body text keyed on sign+chartpoint; house adds nothing distinctive | Invert architecture: house vocabulary pool is PRIMARY, sign adds flavour |
| FAQ answers | 432 / 432 | New shared 4-grams introduced by v1 delivery | `_hash_index` with modulus=8; no closing sentence shared across >2 pages |
| **Total impacted** | **432 / 432** | L1 94.4% BLOCKED · L2 FAIL | Full structural rewrite |

**Phrases that MUST NOT appear on more than 1 page each (found in re-scan):**
- `"time place details house"` -- delete entirely
- `"details house based placements"` -- delete entirely
- `"place details house based"` -- delete entirely
- Any variation of `"birth time"`, `"accurate birth"`, `"birth chart"` as a standalone closing sentence

**Architecture rule:** The 12 house domains are: (1) self/identity (2) finances/possessions (3) communication/siblings (4) home/roots (5) creativity/children (6) health/service (7) partnerships (8) transformation (9) philosophy/travel (10) career/reputation (11) friendships/goals (12) spirituality/retreat. Every `strengths`, `challenges`, and `life_themes` field must contain ≥2 sentences that could ONLY apply to that house domain -- a reader must be able to identify the house from the body text alone.

---

## 3. Tests -- Required Before Integration

| Test | Layer | Tool | Pass Criterion | Run Command |
|---|---|---|---|---|
| TF-IDF Cosine | L1 | `tests/echo_pace_seo20k_scan.py` | Character Placements worst pair **< 50%** | `python3 tests/echo_pace_seo20k_scan.py` |
| N-gram Match | L2 | `tests/echo_pace_seo20k_scan.py` | **0** four-gram violations > 15% frequency | Same script |
| Jaccard Titles | L3 | `tests/echo_pace_seo20k_scan.py` | No title pair > 60% Jaccard | Same script |

---

## 4. Scan History

| Scan | Date | L1 | L1 Status | L2 Violations | L3 Worst Jaccard | Verdict |
|---|---|---|---|---|---|---|
| Pre-fix (original) | 2026-05-31 | 93.4% | ❌ BLOCKED | 10 at 100% | 100% | FAIL |
| v1 delivery re-scan | 2026-06-02 | **94.4%** | ❌ BLOCKED | 10 at 32% | 100% | ❌ FAIL -- regression |
| v2 delivery (target) | -- | **< 50%** | ✅ PASS | 0 | < 60% | -- |

**Top v1 L2 violations (must be eliminated in v2):**
- `"time place details house"` -- 32%
- `"details house based placements"` -- 32%
- `"place details house based"` -- 32%
