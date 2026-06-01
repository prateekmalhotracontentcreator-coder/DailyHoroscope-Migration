# Codex Commission: M3-CP-FIX -- Character Placements Generator Fix (v3)
> Thread: SEO Legacy (M3 section) | File: `backend/seo_m3_builders.py`
> Issued: 2026-06-02 (v3 -- v2 improved L1 to 62.7% but still FLAGGED; new L2 boilerplate introduced)
> Scan script: `tests/echo_pace_seo20k_scan.py` | Scan report: `SEO_20K/SEO_TRACKER.md`

---

## Commission Brief (5 lines)

v2 improved L1 from 94.4% → 62.7% -- progress -- but still failing, and the worst pair is now `Scorpio Moon in the 2nd House` vs `Scorpio Sun in the 2nd House`. This reveals the remaining core problem: **Sun/Moon/Rising pages for the same sign in the same house are still too semantically close**. The architecture needs one more layer of separation: (1) **chart-point-native paragraph banks** -- Sun pages must be identity/purpose/visibility-led throughout (not just the opener), Moon pages must be emotion/memory/security-led throughout, Rising pages must be presentation/instinct/outer-style-led throughout -- every `strengths`, `challenges`, and `life_themes` sentence must be written from that chart-point's psychological frame, not generic astrological description; (2) **delete these three phrase families entirely**: `"house turns attention toward"` (100%), `"blend makes house site"` (43%), `"life themes revolve around"` (42%) -- these are universal structural stems that recur regardless of house or chart point; (3) **meta_title must use two alternating patterns** rotated by `_hash_index(sign, chartpoint, house, modulus=2)` so same-sign pages are not token-identical across houses; (4) **no sentence stem may be shared across chart points for the same house** -- a reader must be able to identify whether a page is Sun, Moon, or Rising from the body text alone, without seeing the title.

---

## 1. SEO Pages -- Module Overview

| Page Type | URL Pattern | Total Pages | Dimensions | Content Fields Scanned |
|---|---|---|---|---|
| Character Placements | `/traits/{sign}/{chart_point}/{house}` | 432 | 12 signs × 3 chart points (Sun/Moon/Rising) × 12 houses | `summary`, `overview`, `traits.strengths`, `traits.challenges`, `traits.life_themes`, FAQ answers, `meta_title` |

---

## 2. Pages Impacted -- Rework Required

| Cluster | Pages Affected | Issue | Fix Required |
|---|---|---|---|
| Same-sign, same-house, diff chart point (e.g. Scorpio Sun 2H vs Scorpio Moon 2H) | 144 clusters of 3 | Still too semantically close -- worst pair in v2 scan | Chart-point-native paragraph banks: Sun=purpose, Moon=emotion, Rising=presentation |
| Universal structural stems | 432 / 432 | New shared 4-grams from v2: "house turns attention toward" 100%, "life themes revolve around" 42% | Delete entirely -- no replacement, write natively |
| `meta_title` | 432 / 432 | Same-sign titles cluster by token across houses + chart points | 2 alternating title patterns, hash-rotated by sign+chartpoint+house |
| **Total impacted** | **432 / 432** | L1 62.7% FLAGGED · L2 FAIL · L3 FAIL | Chart-point separation + stem elimination |

**Phrases that MUST NOT appear anywhere in the output (delete, do not rephrase):**
- `"house turns attention toward"` -- 100% of pages in v2
- `"blend makes house site"` -- 43% of pages in v2
- `"life themes revolve around"` -- 42% of pages in v2
- `"time place details house"` -- from v1, must remain gone
- `"details house based placements"` -- from v1, must remain gone
- Any closing sentence shared across chart points (e.g. timing notes, chart-consultation prompts)

**Chart-point architecture rule (MANDATORY):**

Every sentence in `strengths`, `challenges`, and `life_themes` must be written from the chart-point's frame:

| Chart Point | Psychological Frame | Vocabulary Domain |
|---|---|---|
| **Sun** | Identity · Purpose · Visibility · Ego-expression | drive, achievement, recognition, creative will, authority |
| **Moon** | Emotion · Memory · Security · Instinctive response | comfort, nurturing, past, feeling-tone, inner landscape |
| **Rising** | Presentation · First impression · Instinct · Body | approach, style, how others perceive, physical manner, outer layer |

A Sun-in-2nd-House page and a Moon-in-2nd-House page for the same sign must read as **entirely different psychological experiences of the same house domain** -- not the same description with different adjectives.

**Meta_title pattern rule:**
Use two structurally different patterns, hash-rotated:
- Pattern A: `"{Sign} {ChartPoint} in the {OrdinalHouse} House -- {Domain} & Life Themes"`
- Pattern B: `"{ChartPoint} in {Sign}: {HouseDomain} Placement Guide"`

---

## 3. Tests -- Required Before Integration

| Test | Layer | Tool | Pass Criterion | Run Command |
|---|---|---|---|---|
| TF-IDF Cosine | L1 | `tests/echo_pace_seo20k_scan.py` | Character Placements worst pair **< 50%** | `python3 tests/echo_pace_seo20k_scan.py` |
| N-gram Match | L2 | `tests/echo_pace_seo20k_scan.py` | **0** four-gram violations > 15% frequency | Same script |
| Jaccard Titles | L3 | `tests/echo_pace_seo20k_scan.py` | No title pair > 60% Jaccard | Same script |

**Self-check before submitting:** Take any one sign (e.g. Scorpio), one house (e.g. 2nd), and compare the Sun, Moon, and Rising pages side by side. If the three pages share any sentence structure beyond the house-domain opener, the fix is not complete.

---

## 4. Scan History

| Scan | Date | L1 | L1 Status | L2 Violations | L3 Status | Verdict |
|---|---|---|---|---|---|---|
| Pre-fix (original) | 2026-05-31 | 93.4% | ❌ BLOCKED | 10 at 100% | FLAGGED | FAIL |
| v1 re-scan | 2026-06-02 | 94.4% | ❌ BLOCKED | 10 at 32% | FLAGGED | ❌ FAIL -- no improvement |
| v2 re-scan | 2026-06-02 | **62.7%** | ⚠️ FLAGGED | 10 ("house turns attention toward" 100%) | FAIL | ❌ FAIL -- new boilerplate |
| **v3 target** | -- | **< 50%** | ✅ PASS | **0** | PASS | -- |

**v2 worst pair:** `Scorpio Moon in the 2nd House` vs `Scorpio Sun in the 2nd House`
**Root cause:** Sun/Moon/Rising pages for same sign+house still share structural framing -- chart-point separation is the key unlock.

**Top v2 L2 violations (must be eliminated in v3):**
- `"house turns attention toward"` -- 100%
- `"blend makes house site"` -- 43%
- `"life themes revolve around"` -- 42%
