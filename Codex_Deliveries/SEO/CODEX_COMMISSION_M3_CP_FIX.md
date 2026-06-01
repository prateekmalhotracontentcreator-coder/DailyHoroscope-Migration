# Codex Commission: M3-CP-FIX -- Character Placements Generator Fix
> Thread: SEO Legacy (M3 section) | File: `backend/seo_m3_builders.py` (primary), `backend/seo_m3_catalog.py` (secondary)
> Issued: 2026-05-31 | Scan script: `tests/echo_pace_seo20k_scan.py` | Scan report: `SEO_20K/SEO_TRACKER.md`

---

## Commission Brief (5 lines)

ECHO/PACE scan: Character Placements L1 = 93.4% BLOCKED -- critical, worst score across all modules. Root cause: `build_character_placement_doc()` populates trait/theme body text from fixed catalog constants that are identical for the same sign×chart_point combination regardless of house. Every page for "Virgo Sun in any house" shares near-identical body text -- only the house number changes. Fix requires three things: (1) create ≥6 trait variant blocks per sign×chart_point combination, select one using `_hash_index(sign_slug, chart_point_slug, house_slug, modulus=6)`; (2) make the house context explicit and distinct in `strengths`, `challenges`, and `life_themes` -- each house must contribute ≥2 house-specific sentences; (3) vary the FAQ answers per placement (≥4 variants per question, hash-selected). Single file deliverable: `backend/seo_m3_builders.py` -- do not modify catalog slugs or URL structure.

---

## 1. SEO Pages -- Module Overview

| Page Type | URL Pattern | Total Pages | Dimensions | Content Fields Scanned |
|---|---|---|---|---|
| Character Placements | `/traits/{sign}/{chart_point}/{house}` | 432 | 12 signs × 3 chart points (Sun/Moon/Ascendant) × 12 houses | `summary`, `overview`, `traits.strengths`, `traits.challenges`, `traits.life_themes`, FAQ answers |

---

## 2. Pages Impacted -- Rework Required

| Cluster | Pages Affected | Issue | Fix Required |
|---|---|---|---|
| All sign × Sun | 144 (12 signs × 12 houses) | `strengths`/`challenges` identical across all 12 houses for same sign | ≥6 variant blocks per sign; house-specific sentences per house |
| All sign × Moon | 144 (12 signs × 12 houses) | Same as above | Same fix |
| All sign × Ascendant | 144 (12 signs × 12 houses) | Same as above | Same fix |
| **Total impacted** | **432 / 432** | L1 93.4% · L2 FAIL · L3 FLAGGED | Single file change |

**Specific boilerplate phrases appearing verbatim on 100% of pages (must be eliminated):**
- `"birth time rising house"` -- 100% frequency
- `"become clearer dignity aspects"` -- 100% frequency
- `"birth chart accurate birth"` -- 100% frequency

---

## 3. Tests -- Required Before Integration

| Test | Layer | Tool | Pass Criterion | Run Command |
|---|---|---|---|---|
| TF-IDF Cosine Similarity | L1 | `tests/echo_pace_seo20k_scan.py` | Character Placements worst pair < 50% | `python3 tests/echo_pace_seo20k_scan.py` |
| N-gram Phrase Match | L2 | `tests/echo_pace_seo20k_scan.py` | 0 four-gram violations > 15% frequency | Same script |
| Jaccard Title Similarity | L3 | `tests/echo_pace_seo20k_scan.py` | No title pair > 60% Jaccard | Same script |
| Google Duplication | Layer G | `tests/echo_pace_seo20k_scan.py` | ≤ 1 Google hit per sampled phrase | `SERPER_API_KEY=xxx python3 tests/echo_pace_seo20k_scan.py` |

---

## 4. Current Test Scores (Scan: 2026-05-31, sample 120/432)

| Page Type | Sample | L1 Score | L1 Status | L2 Violations | L2 Status | L3 Worst Jaccard | L3 Status |
|---|---|---|---|---|---|---|---|
| Character Placements | 120 | **93.4%** | ❌ BLOCKED | 10 at 100% freq | ❌ FAIL | 100% (same sign, diff house) | ⚠️ FLAGGED |

**Target after fix:** L1 < 50% · L2 = 0 violations · L3 Jaccard < 60%
