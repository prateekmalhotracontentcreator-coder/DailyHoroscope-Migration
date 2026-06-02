# Codex Commission: M3-CP-FIX -- Character Placements Generator Fix (v5)
> Thread: SEO Legacy (M3 section) | File: `backend/seo_m3_builders.py`
> Issued: 2026-06-02 (v5 -- v4 regressed badly to 96.1%; restore v3 state and make only surgical data edits)
> Scan script: `tests/echo_pace_seo20k_scan.py` | Scan report: `SEO_20K/SEO_TRACKER.md`

---

## Commission Brief (5 lines)

v4 regressed from 52.0% → 96.1% BLOCKED because new sign-family helper functions introduced universal sentence scaffolding (`"house story tends feel"` 100%, `"behaviour often sharpens native"` 100%, `"house reading generically gives"` 100%). **v3 at 52.0% is the closest result -- start from v3, not v4.** The working tree has been reverted to the last clean commit (v3 state). Three targeted fixes remain to clear 52.0% → < 50%: (1) **delete the three residual v3 phrase families from the DATA pools directly** -- `"blend makes house site"` (43%), `"life themes revolve around"` (28%), `"recurring theme learning how"` (21%) -- find every string in the existing pool dicts that contains these substrings and rewrite just those strings; (2) **fix Pattern B title via a one-line dict lookup** -- add `SIGN_ADJECTIVES = {"aries": "Bold", "taurus": "Grounded", ...}` and insert the adjective with an f-string in the existing title builder, no new function; (3) **CRITICAL CONSTRAINT: do not add any new helper function, generator function, or sentence template** -- all changes must be to string values in existing data dicts; if a sentence pool needs a new variant, add the string to the existing list, do not wrap it in a new function.

---

## 1. Baseline State

**Revert v4 before starting.** The working tree was already reverted to last clean commit by CC (2026-06-02). Confirm v3 state is active:
```bash
python3 tests/echo_pace_seo20k_scan.py
# Expected: Character Placements L1 ~52.0% FLAGGED
# If L1 > 90%, v4 code is still present -- git checkout backend/seo_m3_builders.py
```

---

## 2. Three Surgical Fixes

### Fix 1 -- Delete 3 phrase families from existing data pools

Search `backend/seo_m3_builders.py` for every string containing any of these substrings:
- `"blend makes house"` or `"makes house site"`
- `"life themes revolve"` or `"themes revolve around"`
- `"recurring theme learning"` or `"theme learning how"`

For each match: rewrite the string with a unique, house/sign/chartpoint-specific phrasing drawn from the semantic domain of that house. Do not introduce any phrase that could appear on more than 2 of the 432 pages.

**How to verify Fix 1 worked:** grep the entire file for each substring after editing -- zero hits expected.
```bash
grep -n "blend makes house\|makes house site\|life themes revolve\|themes revolve around\|recurring theme learning\|theme learning how" backend/seo_m3_builders.py
# Expected: no output
```

### Fix 2 -- Pattern B title sign-adjective (one-line change only)

Locate the existing `meta_title` / Pattern B title builder in `seo_m3_builders.py`. Add this dict **at module level** (not inside a function):
```python
_SIGN_ADJ = {
    "aries": "Bold", "taurus": "Grounded", "gemini": "Versatile",
    "cancer": "Nurturing", "leo": "Radiant", "virgo": "Discerning",
    "libra": "Balanced", "scorpio": "Intense", "sagittarius": "Expansive",
    "capricorn": "Structured", "aquarius": "Independent", "pisces": "Fluid",
}
```

Then in the **existing** Pattern B title string, insert the adjective with an f-string. Example -- before:
```python
f"{chartpoint} in {sign_name}: {house_domain} Placement Guide"
```
After:
```python
f"{chartpoint} in {sign_name}: {_SIGN_ADJ.get(sign_slug, '')} {house_domain} Placement"
```

That is the entire change for Fix 2. Do not add any new function.

### Fix 3 -- No new code (hard constraint)

If you find yourself writing a new function, a new class, a new loop, or a new template string to implement any part of this fix -- stop. Every new structural element risks introducing a new universal stem. The only permitted additions are:
- New string values inside existing list/dict data structures
- The `_SIGN_ADJ` dict (module-level constant, not a function)
- The one f-string change in the existing Pattern B title line

---

## 3. Tests -- Required Before Submitting

```bash
python3 tests/echo_pace_seo20k_scan.py
```

All three must pass before submitting:
- L1 Character Placements worst pair **< 50%** ✅
- L2 **0** four-gram violations > 15% frequency ✅
- L3 no title pair > 60% Jaccard ✅

**Include the scan output in your delivery note.** Do not submit without passing scores.

**Self-checks:**
1. grep for all 5 banned phrase substrings (Fix 1 check above) -- must return zero hits
2. Pull all 12 Pattern B titles for any one house (e.g. 7th). Each must contain a distinct sign adjective. No two titles should be identical.
3. Scorpio Sun / Moon / Rising in the 2nd House -- three pages must still read as distinct psychological experiences (v3 confirmed this; do not regress).

---

## 4. Scan History

| Scan | Date | L1 | L1 Status | L2 Top Violation | L3 Worst Pair | Verdict |
|---|---|---|---|---|---|---|
| Pre-fix (original) | 2026-05-31 | 93.4% | ❌ BLOCKED | 10 phrases at 100% | -- | FAIL |
| v1 re-scan | 2026-06-02 | 94.4% | ❌ BLOCKED | 10 at 32% | -- | ❌ FAIL |
| v2 re-scan | 2026-06-02 | 62.7% | ⚠️ FLAGGED | "house turns attention toward" 100% | Scorpio Moon 2H vs Sun 2H | ❌ FAIL |
| v3 re-scan | 2026-06-02 | **52.0%** | ⚠️ FLAGGED | "blend makes house site" 43% | Rising Capricorn 7H vs Rising Taurus 7H | ❌ FAIL -- closest so far |
| v4 re-scan | 2026-06-02 | 96.1% | ❌ BLOCKED | "house story tends feel" 100% | Sun Libra 12H vs Libra Rising 12H | ❌ FAIL -- regression, new helper functions introduced universal stems |
| **v5 target** | -- | **< 50%** | ✅ PASS | **0** | < 60% Jaccard | -- |

**Pattern:** every version that introduced new helper functions / generators collapsed back to BLOCKED. v3 succeeded by working directly on data pools. v5 must follow the same principle -- data edits only, no new code structure.

**Banned phrases (cumulative -- must not appear on more than 1 page each):**
- `"blend makes house site"` · `"life themes revolve around"` · `"recurring theme learning how"` -- v3 residuals
- `"house story tends feel"` · `"behaviour often sharpens native"` · `"house reading generically gives"` -- v4 regressions (already gone after revert)
- `"house turns attention toward"` · `"time place details house"` · `"details house based placements"` -- v1/v2 (already gone)
