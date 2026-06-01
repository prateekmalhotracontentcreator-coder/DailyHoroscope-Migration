# Codex Commission: RUD-L2 -- Rudraksha L2/L3 Fix
> Thread: Rudraksha | File: `backend/rudraksha_content.py` (single file change)
> Issued: 2026-05-31 | Scan report: `Codex_Deliveries/ECHO_PACE/ECHO_PACE_SCAN_RUD_CRY_FAITH_2026-05-31.md`

---

## Commission Brief (5 lines)

ECHO/PACE scan passed L1 but failed L2 and L3 across all 4 page types. Root cause: `_faq_items()` uses fixed-string FAQ answer templates -- identical phrases appear on 100% of pages. Fix: add ≥5 variant phrasings per FAQ answer template, select one per page via `_hash_index(page_key, answer_index, modulus=5)`. Apply the same variant pattern to planet, problem, and sign page FAQ templates. Additionally, MUKHI `meta_title` uses digits ("1 Mukhi...") which collapse to 100% Jaccard after tokenisation -- replace with word-form numbers ("One Mukhi Rudraksha -- Benefits, Mantra & Wearing Guide") for all 21 entries.

---

## 1. SEO Pages -- Module Overview

| Page Type | URL Pattern | Count | Content Fields Scanned |
|---|---|---|---|
| Mukhi | `/rudraksha/{n}-mukhi` | 21 | `overview`, `benefits`, `cautions`, `wearing_instructions`, FAQ answers |
| Planet | `/rudraksha/planet/{slug}` | 9 | `description`, `recommendation`, FAQ answers |
| Problem | `/rudraksha/problem/{slug}` | 20 | `guidance`, `body`, FAQ answers |
| Sign | `/rudraksha/sign/{slug}` | 12 | `intro`, `recommendation`, FAQ answers |
| **Total** | | **62** | |

---

## 2. Pages Impacted -- Rework Required

| Page Type | Pages Affected | Issue | Fix Required |
|---|---|---|---|
| Mukhi | All 21 | FAQ boilerplate at 100% frequency + meta_title digit format | Vary FAQ answers (≥5 variants); change "1 Mukhi" → "One Mukhi" etc. |
| Planet | All 9 | FAQ boilerplate at 100% frequency | Vary FAQ answers (≥5 variants per template phrase) |
| Problem | All 20 | FAQ boilerplate at 100% frequency | Vary FAQ answers (≥5 variants per template phrase) |
| Sign | All 12 | FAQ boilerplate at 100% frequency | Vary FAQ answers (≥5 variants per template phrase) |
| **Total impacted** | **62 / 62** | L2 + L3 (MUKHI only) | Single file: `rudraksha_content.py` |

---

## 3. Tests -- Required Before Integration

| Test | Layer | Tool | Pass Criterion | Run Command |
|---|---|---|---|---|
| TF-IDF Cosine Similarity | L1 | `tests/echo_pace_rud_scan.py` | Worst pair < 50% across all 4 page types | `python3 tests/echo_pace_rud_scan.py` |
| N-gram Phrase Match | L2 | `tests/echo_pace_rud_scan.py` | 0 four-gram violations (> 15% frequency) across all 4 types | Same script |
| Jaccard Title Similarity | L3 | `tests/echo_pace_rud_scan.py` | No title pair > 60% Jaccard across all 4 types | Same script |
| Google Duplication | Layer G | `tests/echo_pace_rud_scan.py` | ≤ 1 Google hit per sampled phrase | `SERPER_API_KEY=xxx python3 tests/echo_pace_rud_scan.py` |

All 4 layers must PASS before routes are wired or Mongo is seeded.

---

## 4. Current Test Scores (Scan: 2026-05-31)

| Page Type | Pages | L1 Score | L1 Status | L2 Violations | L2 Status | L3 Worst Jaccard | L3 Status | Layer G |
|---|---|---|---|---|---|---|---|---|
| Mukhi | 21 | 27.0% | ✅ PASS | 10 at 100% freq | ❌ FAIL | 100% | ⚠️ FLAGGED | Not run |
| Planet | 9 | 8.4% | ✅ PASS | 10 at 100% freq | ❌ FAIL | 71% | ⚠️ FLAGGED | Not run |
| Problem | 20 | 29.0% | ✅ PASS | 10 at 100% freq | ❌ FAIL | 75% | ⚠️ FLAGGED | Not run |
| Sign | 12 | 4.7% | ✅ PASS | 10 at 100% freq | ❌ FAIL | 71% | ⚠️ FLAGGED | Not run |

**Top L2 violating phrases (examples):**
- `"mukhi rudraksha generally chosen"` -- 100% MUKHI pages
- `"clear purpose instead layering"` -- 100% PLANET pages
- `"here mukhi rudraksha supported"` -- 100% PROBLEM pages
- `"yes better combine primary"` -- 100% SIGN pages

**Target after fix:** All L2 = 0 violations · All L3 Jaccard < 60% · L1 to remain PASS (< 50%)
