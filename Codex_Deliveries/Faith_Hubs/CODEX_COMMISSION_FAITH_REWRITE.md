# Codex Commission: FAITH-REWRITE -- Faith & Scripture Generator Rewrite
> Thread: Faith Hubs | Files: `backend/faith_gita_data.py` · `backend/faith_bible_data.py` · `backend/faith_seo_data.py`
> Issued: 2026-05-31 | Scan report: `Codex_Deliveries/ECHO_PACE/ECHO_PACE_SCAN_RUD_CRY_FAITH_2026-05-31.md`

---

## Commission Brief (5 lines)

ECHO/PACE scan: Gita L1 = 100% BLOCKED, Bible L1 = 82% BLOCKED, Transit L1 = 99.5% BLOCKED -- same structural failure as Angel Numbers ANGEL-1. Root cause: `summary`, `hook`, and `application` fields in `get_gita_page()` / `get_bible_page()` are populated from situation/topic-level constants, making every page sharing the same situation word-for-word identical in body text. Fix requires three files: (1) `faith_gita_data.py` -- embed ≥2 verse-specific translation words into `hook`/`summary`; create ≥8 situation sub-templates selected via `_hash_index(chapter, verse_number, situation_slug, modulus=8)`; remove the fixed sentence "It does not ask for denial. It asks for a truer next step" which appears on all 10,500 pages. (2) `faith_bible_data.py` -- add ≥5 topic-variant body openings; remove fixed sentence "keeping the promise practical, emotionally honest, and connected to a parallel Vedic bridge." (3) `faith_seo_data.py` -- Gita and Bible tradition transit pages must diverge in ≥60% of body vocabulary via separate tradition-specific content pools; Daily pages need ≥5 monthly seasonal framing variants per sign. Do NOT seed any Faith collections until all page types reach L1 < 50%.

---

## 1. SEO Pages -- Module Overview

| Page Type | URL Pattern | Total Pages | Generator File | Content Fields Scanned |
|---|---|---|---|---|
| Gita × Situation | `/faith/gita/{ch}-{v}/{situation}` | 10,500 | `faith_gita_data.py` | `summary`, `hook`, `etymology_intro`, `application`, `practice_prompts`, FAQ answers |
| Bible × Transition | `/faith/bible/{topic}/{transition}` | 6,000 | `faith_bible_data.py` | `summary`, `hook`, `application`, `emotional_frame`, FAQ answers |
| Transit (Gita + Bible tradition) | `/faith/transit/{slug}/{tradition}` | 156 | `faith_seo_data.py` | `summary`, `guidance`, `application`, FAQ answers |
| Daily (Sign × Month) | `/faith/daily/{sign}/{month}` | 144 | `faith_seo_data.py` | `summary`, `message`, `guidance` |
| **Total** | | **16,800** | | |

---

## 2. Pages Impacted -- Rework Required

| Page Type | Pages Affected | Failure | Root Cause | Fix Required |
|---|---|---|---|---|
| Gita × Situation | All 10,500 | L1 = 100% BLOCKED · L2 FAIL | `hook`/`summary`/`application` filled from `situation['hook']`, `situation['hidden_fear']`, `situation['practice_shift']` -- fixed constants identical for every verse in same situation | ≥8 situation sub-templates; embed ≥2 verse-specific words from `verse["translation"]`; hash-select by `(chapter, verse, situation_slug)` |
| Bible × Transition | All 6,000 | L1 = 81.7% BLOCKED · L2 FAIL | `summary` fixed template: "This page approaches {transition} through the Bible theme of {topic}..." -- same structural sentence on every page | ≥5 topic-variant body openings; vary `emotional_frame` by verse content |
| Transit (both traditions) | All 156 | L1 = 99.5% BLOCKED · L2 FAIL | Gita-tradition and Bible-tradition transit pages share near-identical body text -- only verse citation differs | Separate content pools per tradition; ≥3 framing approaches per transit family (retrograde / ingress / station) |
| Daily (Sign × Month) | All 144 | L1 = 50.0% (on gate) · L2 FAIL | Seasonal framing fixed per sign; monthly vocabulary overlap across 12 months | ≥5 monthly framing variants per sign, hash-selected by `(sign_slug, month_slug)` |
| **Total impacted** | **16,800 / 16,800** | L1 BLOCKED (3 types) · L2 FAIL (all) | Template constants dominate body text | 3 file changes |

**Specific phrases to eliminate (appear verbatim across all Gita pages):**
- `"It does not ask for denial. It asks for a truer next step"` → 10,500 pages
- `"emotional honesty, and a specific spiritual response"` → 10,500 pages

**Specific phrases to eliminate (appear verbatim across all Bible pages):**
- `"keeping the promise practical, emotionally honest, and connected to a parallel Vedic bridge"` → 6,000 pages

---

## 3. Tests -- Required Before Integration

| Test | Layer | Tool | Pass Criterion | Run Command |
|---|---|---|---|---|
| TF-IDF Cosine Similarity | L1 | `tests/echo_pace_faith_scan.py` | All 4 page types: worst pair < 50% | `python3 tests/echo_pace_faith_scan.py` |
| N-gram Phrase Match | L2 | `tests/echo_pace_faith_scan.py` | 0 four-gram violations (> 15% frequency) for all 4 types | Same script |
| Jaccard Title Similarity | L3 | `tests/echo_pace_faith_scan.py` | No title pair > 60% Jaccard for all 4 types | Same script |
| Google Duplication | Layer G | `tests/echo_pace_faith_scan.py` | ≤ 1 Google hit per sampled phrase | `SERPER_API_KEY=xxx python3 tests/echo_pace_faith_scan.py` |

The script samples 3,480 Gita pages (chapters 1-5 × all 15 situations) and 100 Bible pages (10 topics × 10 transitions) -- representative enough to detect any surviving template repetition. All 4 layers must PASS for all 4 page types before seeding any Faith collection.

---

## 4. Current Test Scores (Scan: 2026-05-31)

| Page Type | Total | Sample Size | L1 Score | L1 Status | L2 Violations | L2 Status | L3 Worst Jaccard | L3 Status | Layer G |
|---|---|---|---|---|---|---|---|---|---|
| Gita × Situation | 10,500 | 3,480 | **100.0%** | ❌ BLOCKED | 10 at 100% freq | ❌ FAIL | 100% (same situation, diff verse) | ⚠️ FLAGGED | Not run |
| Bible × Transition | 6,000 | 100 | **81.7%** | ❌ BLOCKED | 10 at 100% freq | ❌ FAIL | 67% (same topic, diff transition) | ⚠️ FLAGGED | Not run |
| Transit | 156 | 156 (all) | **99.5%** | ❌ BLOCKED | 10 at 100% freq | ❌ FAIL | 71% (same transit, diff tradition) | ⚠️ FLAGGED | Not run |
| Daily | 144 | 144 (all) | **50.0%** | ⚠️ ON GATE | 5 at 100% freq | ❌ FAIL | 75% (same sign, diff month) | ⚠️ FLAGGED | Not run |

**Top L2 violating phrases (examples):**
- `"ask denial asks truer"` -- 100% Gita pages (fixed hook sentence)
- `"emotional honesty specific spiritual"` -- 100% Gita pages (fixed hook sentence)
- `"wise move usually dramatic"` -- 100% Bible pages (structural boilerplate)
- `"thoughtful practice dramatic overreaction"` -- 100% Transit pages
- `"seasonal mood scripture led"` -- 100% Daily pages

**Target after fix:** All page types L1 < 50% · L2 = 0 violations · L3 Jaccard < 60%
