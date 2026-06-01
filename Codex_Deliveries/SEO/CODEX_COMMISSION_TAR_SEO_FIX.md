# Codex Commission: TAR-SEO-FIX -- Tarot SEO Generator Fix
> Thread: Tarot SEO | File: `backend/tarot_seo_data.py` (single file)
> Issued: 2026-05-31 | Scan script: `tests/echo_pace_seoc_tarot_scan.py` | Scan report: `SEO_20K/SEO_TRACKER.md`

---

## Commission Brief (5 lines)

ECHO/PACE scan: All 3 Tarot page types pass L1 (Spreads 32.9%, Cards 34.8%, Intentions 14.2%) but fail L2 and/or L3. Three targeted fixes required -- all in `backend/tarot_seo_data.py`. (1) **Spreads L2**: the phrase "page reads spread card layout" appears on 100% of 100 spread pages -- this is a fixed intro sentence; replace with ≥6 spread-type-specific openers (Celtic Cross gets its own, 3-card gets its own, etc.) selected by slug hash. (2) **Cards L3**: `meta_title` format "X Tarot Card - minor Meaning & Guide" is identical for all minor arcana -- include the suit name prominently ("Ace of Wands -- Wands Suit, Minor Arcana Guide") so each card is uniquely described. (3) **Intentions L2+L3**: "pages explain layouts symbolism" appears on 100% of 20 pages (intro boilerplate) -- replace with ≥4 intention-specific framing variants; also vary the meta_title beyond "Best Tarot Spreads for X -- Top Layout" (e.g., "Tarot for Career -- Spreads, Cards & Reading Guide").

---

## 1. SEO Pages -- Module Overview

| Page Type | URL Pattern | Total Pages | Content Fields Scanned |
|---|---|---|---|
| Spreads | `/tarot/spread/{slug}` | 100 | `purpose`, `how_to`, `when_to_use`, `positions[].meaning`, `sample_reading`, FAQ answers |
| Cards | `/tarot/card/{slug}` | 78 | `upright`, `reversed`, `love`, `career`, `health`, `imagery` |
| Intentions | `/tarot/for/{slug}` | 20 | `intro`, `sample_walkthrough`, `caution_cards[].note`, FAQ answers |
| **Total** | | **198** | |

---

## 2. Pages Impacted -- Rework Required

| Page Type | Pages Affected | Issue | Fix Required |
|---|---|---|---|
| Spreads | 100 / 100 | Intro sentence fixed ("page reads spread card layout") -- 100% freq | ≥6 spread-type openers (3-card / Celtic Cross / relationship / career / etc.) hash-selected by slug |
| Cards -- Minor Arcana | 56 / 78 | `meta_title` "X of Y Tarot Card - minor Meaning & Guide" -- suit word filtered by tokeniser → 75% Jaccard | Include suit name explicitly: "Ace of Wands -- Wands Suit Minor Arcana Guide" |
| Intentions | 20 / 20 | Intro boilerplate 100% + "Best Tarot Spreads for X" meta_title template | ≥4 intention-type intro variants; diversify meta_title beyond template |

**Boilerplate phrases to eliminate:**
- Spreads: `"page reads spread card layout"` -- 100% of 100 pages
- Spreads: `"reads spread card layout come"` -- 87% of 100 pages
- Intentions: `"pages explain layouts symbolism"` -- 100% of 20 pages
- Intentions: `"explain layouts symbolism while"` -- 100% of 20 pages

---

## 3. Tests -- Required Before Integration

| Test | Layer | Tool | Pass Criterion | Run Command |
|---|---|---|---|---|
| TF-IDF Cosine | L1 | `tests/echo_pace_seoc_tarot_scan.py` | All 3 types < 50% (currently passing -- must not regress) | `python3 tests/echo_pace_seoc_tarot_scan.py` |
| N-gram Match | L2 | `tests/echo_pace_seoc_tarot_scan.py` | Spreads 0 violations · Intentions 0 violations | Same script |
| Jaccard Titles | L3 | `tests/echo_pace_seoc_tarot_scan.py` | Cards < 60% · Intentions < 60% | Same script |
| Layer G | Layer G | `tests/echo_pace_seoc_tarot_scan.py` | ≤ 1 Google hit per sampled phrase | `SERPER_API_KEY=xxx python3 tests/echo_pace_seoc_tarot_scan.py` |

---

## 4. Current Test Scores (Scan: 2026-05-31)

| Page Type | Pages | L1 Score | L1 Status | L2 Violations | L2 Status | L3 Worst Jaccard | L3 Status |
|---|---|---|---|---|---|---|---|
| Tarot Spreads | 100 | 32.9% | ✅ PASS | 6 at 87-100% freq | ❌ FAIL | 70% | ⚠️ Minor |
| Tarot Cards | 78 | 34.8% | ✅ PASS | 0 | ✅ PASS | 75% (same-suit) | ⚠️ FLAGGED |
| Tarot Intentions | 20 | 14.2% | ✅ PASS | 10 at 100% freq | ❌ FAIL | 75% | ⚠️ FLAGGED |

**Target after fix:** All types L1 < 50% (no regression) · Spreads L2 = 0 · Intentions L2 = 0 · Cards L3 < 60% · Intentions L3 < 60%
