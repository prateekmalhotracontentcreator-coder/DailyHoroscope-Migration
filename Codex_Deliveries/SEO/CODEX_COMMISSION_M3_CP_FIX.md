# Codex Commission: M3-CP-FIX -- Character Placements Generator Fix (v4)
> Thread: SEO Legacy (M3 section) | File: `backend/seo_m3_builders.py`
> Issued: 2026-06-02 (v4 -- v3 improved L1 to 52.0% but still FLAGGED; two residual failure modes identified)
> Scan script: `tests/echo_pace_seo20k_scan.py` | Scan report: `SEO_20K/SEO_TRACKER.md`

---

## Commission Brief (5 lines)

v3 improved L1 from 62.7% → 52.0% -- the Scorpio Sun/Moon/Rising 2H self-check is now clearly separated and the chart-point psychology is working. Two residual failure modes remain: (1) **shared house-bank sentences across signs** -- within the same chart point + house, sentences in `strengths`, `challenges`, and `life_themes` are still drawn from a single pool regardless of sign, so e.g. all 12 Rising-in-7th-House pages share the same house-bank phrasing; fix by adding sign-family variance pools -- for each chart-point × house block, provide at least 3 variant banks selected by `_hash_index(sign_slug, chartpoint, house, modulus=3)` so the same sentence cannot appear across more than 4 of the 12 sign pages for that house; (2) **Pattern B title clustering** -- `"{ChartPoint} in {Sign}: {HouseDomain} Placement Guide"` places the house domain word at a fixed structural position, causing all Rising-in-7th pages across signs to produce "Rising in X: Partnership Placement Guide" -- high Jaccard because `{HouseDomain}` is identical for all 12 signs; fix: Pattern B must include a **sign-flavour adjective** so the title is unique per sign, e.g. `"Rising in Capricorn: Structured Partnership Placement"` vs `"Rising in Taurus: Grounded Partnership Placement"` -- use a sign-native adjective drawn from a per-sign adjective dict; (3) **delete these three phrase families entirely** (do not rephrase -- remove the generating code): `"blend makes house site"` (43%), `"life themes revolve around"` (28%), `"recurring theme learning how"` (21%).

---

## 1. SEO Pages -- Module Overview

| Page Type | URL Pattern | Total Pages | Dimensions | Content Fields Scanned |
|---|---|---|---|---|
| Character Placements | `/traits/{sign}/{chart_point}/{house}` | 432 | 12 signs × 3 chart points (Sun/Moon/Rising) × 12 houses | `summary`, `overview`, `traits.strengths`, `traits.challenges`, `traits.life_themes`, FAQ answers, `meta_title` |

---

## 2. Pages Impacted -- Rework Required

| Cluster | Pages Affected | Issue | Fix Required |
|---|---|---|---|
| Same-chart-point, same-house, diff sign (e.g. all Rising-7th pages) | 144 clusters of 12 | House-bank sentences shared across all 12 sign pages for same house+chartpoint | ≥3 sign-family variant banks per chart-point × house block; hash-select by sign |
| Pattern B `meta_title` | 432 / 432 | `{HouseDomain}` is identical for all signs in same house → L3 title clustering | Add sign-native adjective: `"Rising in Capricorn: Structured Partnership Placement"` |
| Residual shared stems | 432 / 432 | 3 new shared 4-gram families introduced in v3 body | Delete generating code entirely |
| **Total impacted** | **432 / 432** | L1 52.0% FLAGGED · L2 FAIL · L3 FAIL | Sign-family variance + title uniqueness |

**Phrases that MUST NOT appear anywhere in the output -- delete generating code, do not rephrase:**

*New v3 violations:*
- `"blend makes house site"` -- 43% of pages
- `"life themes revolve around"` -- 28% of pages
- `"recurring theme learning how"` -- 21% of pages

*Carried from prior versions (must remain gone):*
- `"house turns attention toward"` -- was 100% in v2
- `"time place details house"` -- was 100% in v1
- `"details house based placements"` -- was 100% in v1
- Any closing sentence shared across chart points (timing notes, chart-consultation prompts)

---

## 3. Architecture Specification

### 3a. Sign-Family Variance Pools (new in v4)

The chart-point-native paragraph banks from v3 are working -- keep them. The new requirement is that within each chart-point × house block, the content must also vary by sign so no sentence appears on more than 4 of the 12 sign pages.

**Minimum structure:**
```python
# For each (chartpoint, house) combination, define 3 pools:
HOUSE_CHARTPOINT_POOLS = {
    ("rising", 7): [
        POOL_A,  # used for signs where hash % 3 == 0
        POOL_B,  # used for signs where hash % 3 == 1
        POOL_C,  # used for signs where hash % 3 == 2
    ],
    ...
}

def get_pool_idx(sign_slug, chartpoint, house):
    return _hash_index(sign_slug, chartpoint, house, modulus=3)
```

Each pool must be semantically distinct -- not just word swaps. Pools should reflect different **experiential angles** of the same house domain: e.g. for Rising-7th House: Pool A = relationship initiation style, Pool B = how others experience this person in partnership, Pool C = what this placement requires from the native in one-on-one settings.

### 3b. Pattern B Title Fix (new in v4)

**Sign-native adjective dict** (provide all 12):
```python
SIGN_ADJECTIVES = {
    "aries": "Bold", "taurus": "Grounded", "gemini": "Adaptive",
    "cancer": "Nurturing", "leo": "Radiant", "virgo": "Discerning",
    "libra": "Balanced", "scorpio": "Intense", "sagittarius": "Expansive",
    "capricorn": "Structured", "aquarius": "Independent", "pisces": "Fluid",
}
```

Pattern B becomes: `"{ChartPoint} in {Sign}: {SignAdj} {HouseDomain} Placement"`

Examples:
- `"Rising in Capricorn: Structured Partnership Placement"` ✅
- `"Rising in Taurus: Grounded Partnership Placement"` ✅  
- `"Sun in Scorpio: Intense Resources Placement"` ✅

This guarantees every title is unique while keeping the structural template recognisable.

### 3c. Chart-Point Architecture (retain from v3 -- confirmed working)

| Chart Point | Psychological Frame | Vocabulary Domain |
|---|---|---|
| **Sun** | Identity · Purpose · Visibility · Ego-expression | drive, achievement, recognition, creative will, authority |
| **Moon** | Emotion · Memory · Security · Instinctive response | comfort, nurturing, past, feeling-tone, inner landscape |
| **Rising** | Presentation · First impression · Instinct · Body | approach, style, how others perceive, physical manner, outer layer |

**This separation is confirmed working in v3 -- do not regress it.** The Scorpio Sun/Moon/Rising 2H triplet is now distinct. Keep chart-point-native framing; only add the sign-family variance layer on top.

---

## 4. Tests -- Required Before Integration

| Test | Layer | Tool | Pass Criterion | Run Command |
|---|---|---|---|---|
| TF-IDF Cosine | L1 | `tests/echo_pace_seo20k_scan.py` | Character Placements worst pair **< 50%** | `python3 tests/echo_pace_seo20k_scan.py` |
| N-gram Match | L2 | `tests/echo_pace_seo20k_scan.py` | **0** four-gram violations > 15% frequency | Same script |
| Jaccard Titles | L3 | `tests/echo_pace_seo20k_scan.py` | No title pair > 60% Jaccard | Same script |

**Self-checks before submitting:**
1. Take Rising + any house (e.g. 7th). Pull all 12 sign pages. No two pages may share a sentence in `strengths`, `challenges`, or `life_themes`.
2. Take the same sign (e.g. Capricorn) + same house (e.g. 7th). Compare Sun, Moon, Rising pages. The three must read as entirely different psychological experiences (v3 confirmed this -- do not regress).
3. Pull all 12 Pattern B titles for Rising-7th. Each must contain a distinct sign adjective. None should share 3+ consecutive tokens.

---

## 5. Scan History

| Scan | Date | L1 | L1 Status | L2 Violations | L3 Worst Pair | Verdict |
|---|---|---|---|---|---|---|
| Pre-fix (original) | 2026-05-31 | 93.4% | ❌ BLOCKED | 10 at 100% | -- | FAIL |
| v1 re-scan | 2026-06-02 | 94.4% | ❌ BLOCKED | 10 at 32% | -- | ❌ FAIL -- no improvement |
| v2 re-scan | 2026-06-02 | 62.7% | ⚠️ FLAGGED | "house turns attention toward" 100% | Scorpio Moon 2H vs Sun 2H | ❌ FAIL |
| v3 re-scan | 2026-06-02 | **52.0%** | ⚠️ FLAGGED | "blend makes house site" 43%, "recurring theme" 21% | Rising Capricorn 7H vs Rising Taurus 7H | ❌ FAIL |
| **v4 target** | -- | **< 50%** | ✅ PASS | **0** | < 60% Jaccard | -- |

**v3 worst pair:** `Rising in Capricorn: Partnership Placement Guide` vs `Rising in Taurus: Partnership Placement Guide`
**Root cause:** Pattern B title identical for all signs in same house + shared house-bank sentences within same chart-point across signs.
**What is working (do not regress):** Chart-point psychological separation (Sun/Moon/Rising) -- confirmed clean in Scorpio 2H self-check.

**Top v3 L2 violations (must be eliminated in v4):**
- `"blend makes house site"` -- 43%
- `"life themes revolve around"` -- 28%
- `"recurring theme learning how"` -- 21%
