# Codex Commission: CRY-L2 -- Crystal Healing L2/L3 Fix
> Thread: Crystal Healing | File: `backend/crystal_data.py` (single file change)
> Issued: 2026-05-31 | Scan report: `Codex_Deliveries/ECHO_PACE/ECHO_PACE_SCAN_RUD_CRY_FAITH_2026-05-31.md`

---

## Commission Brief (5 lines)

ECHO/PACE scan passed L1 (barely -- 47.7%, gate is 50%) but failed L2 and L3. Root cause: `_build_faq()` and caution/cleansing copy blocks use fixed template strings -- same phrases appear on 100% of pages. Fix: add ≥5 variant phrasings per structural template sentence in `_build_faq()`, caution fields, and intention page FAQ templates; select one per page via `_hash_index(crystal_slug, sentence_index, modulus=5)`. For L3: the `meta_title` suffix is identical for all 50 crystal pages -- rotate 3-4 suffix variants using slug hash (e.g. "Healing Properties & Chakra Guide", "Crystal Meaning, Uses & Benefits", "Healing Stone -- Properties & Uses"). Critical constraint: do NOT increase shared vocabulary across pages -- L1 is 2.3% from the FLAGGED gate and must not regress past 50%.

---

## 1. SEO Pages -- Module Overview

| Page Type | URL Pattern | Count | Content Fields Scanned |
|---|---|---|---|
| Crystal Profile | `/crystals/{slug}` | 50 | `tagline`, `healing_properties` (emotional/physical/spiritual), `how_to_use`, `caution`, `affirmation`, `cleansing_methods`, FAQ answers |
| Intention Guide | `/crystals/intention/{slug}` | 20 | `description`, `guidance`, `affirmation`, `practices`, FAQ answers |
| **Total** | | **70** | |

---

## 2. Pages Impacted -- Rework Required

| Page Type | Pages Affected | Issue | Fix Required |
|---|---|---|---|
| Crystal Profile | All 50 | FAQ + caution boilerplate at 100% frequency; meta_title suffix identical | Vary FAQ/caution templates (≥5 variants); rotate meta_title suffix (3-4 variants, hash-selected) |
| Intention Guide | All 20 | FAQ boilerplate at 100% frequency | Vary FAQ answer templates (≥5 variants per phrase) |
| **Total impacted** | **70 / 70** | L2 all · L3 crystal pages | Single file: `crystal_data.py` |

**⚠️ Hard constraint on Crystal Profile pages:** L1 cosine is currently 47.7% -- within 2.3% of the FLAGGED threshold. Adding variant content must diversify vocabulary, not add shared boilerplate. Do not introduce new template phrases that repeat across all 50 pages.

---

## 3. Tests -- Required Before Integration

| Test | Layer | Tool | Pass Criterion | Run Command |
|---|---|---|---|---|
| TF-IDF Cosine Similarity | L1 | `tests/echo_pace_cry_scan.py` | Crystal < 50% · Intention < 50% (must not regress) | `python3 tests/echo_pace_cry_scan.py` |
| N-gram Phrase Match | L2 | `tests/echo_pace_cry_scan.py` | 0 four-gram violations (> 15% frequency) for both page types | Same script |
| Jaccard Title Similarity | L3 | `tests/echo_pace_cry_scan.py` | No title pair > 60% Jaccard for both page types | Same script |
| Google Duplication | Layer G | `tests/echo_pace_cry_scan.py` | ≤ 1 Google hit per sampled phrase | `SERPER_API_KEY=xxx python3 tests/echo_pace_cry_scan.py` |

All 4 layers must PASS. L1 regression (Crystal moving from PASS to FLAGGED) is an automatic reject.

---

## 4. Current Test Scores (Scan: 2026-05-31)

| Page Type | Pages | L1 Score | L1 Status | L2 Violations | L2 Status | L3 Worst Jaccard | L3 Status | Layer G |
|---|---|---|---|---|---|---|---|---|
| Crystal Profile | 50 | 47.7% | ✅ PASS ⚠️ borderline | 10 at 100% freq | ❌ FAIL | 88% (Hessonite vs Garnet) | ⚠️ FLAGGED | Not run |
| Intention Guide | 20 | 20.8% | ✅ PASS | 10 at 100% freq | ❌ FAIL | 71% (Protection vs Travel Protection) | ⚠️ FLAGGED | Not run |

**Top L2 violating phrases (examples):**
- `"option stone soft porous"` -- 100% Crystal pages (water-cleansing caution)
- `"use emotional spiritual balancing"` -- 100% Crystal pages (FAQ template)
- `"spiritual balancing simple cleansing"` -- 100% Crystal pages (FAQ overlap)
- `"where theme shows strongly"` -- 100% Intention pages
- `"feels balanced weekly cleansing"` -- 100% Intention pages

**Target after fix:** All L2 = 0 violations · All L3 Jaccard < 60% · L1 Crystal < 50% (no regression)
