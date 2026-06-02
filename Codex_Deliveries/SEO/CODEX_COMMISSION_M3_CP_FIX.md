# Codex Commission: M3-CP-FIX -- Character Placements Generator Fix (v7)
> Thread: SEO Legacy (M3 section) | File: `backend/seo_m3_builders.py`
> Issued: 2026-06-02 (v7 -- v6 confirmed FAQ fix; two residual failures precisely identified)
> Scan script: `tests/echo_pace_seo20k_scan.py` | Scan report: `SEO_20K/SEO_TRACKER.md`

---

## Commission Brief (5 lines)

v6 confirmed: FAQ fix holds, `_CP_TITLE_LABEL` 2-word labels are correct, `_SIGN_ADJ` is correct. Two surgical changes remain. (1) **L2 -- "style outer style rising" at 22%**: the summary f-string uses `{chart_point['lens'].split(',')[0].strip()}` which for Rising produces `"outer style"` (two words from lens `"outer style, approach, and first impact"`), creating `"...{sign}-style outer style."` at the end of every Rising summary -- the word "style" appears from both the hyphenated sign token and the "outer style" lens fragment, creating the cross-field 4-gram; fix by adding a single-word dict `_CP_LENS_WORD = {"sun": "identity", "moon": "emotion", "rising": "presence"}` and replacing `{chart_point['lens'].split(',')[0].strip()}` with `{_CP_LENS_WORD[chart_point_slug]}` in the summary f-string -- this gives `"...with aries-style presence."` for Rising, eliminating the double-style sequence. (2) **L3 -- Pattern B cross-house clustering**: Pattern B `f"Ascendant Style in {sign}: {adj} {topic_word} Placement"` contains no house label, so for the same sign+chartpoint across 12 different houses only `{topic_word}` varies -- 5 of 6 tokens are fixed → Jaccard ~71% across houses for same sign+chartpoint; fix by **deleting Pattern B entirely** and using one single title template for all 432 pages that includes all four differentiating axes: `f"{sign} {_CP_TITLE_LABEL[chart_point_slug]}, {house['label']}: {_SIGN_ADJ[sign_slug]} {house['topic'].split(',')[0].strip().title()}"` -- Jaccard verified at 55% across all three axes (sign, chartpoint, house). Also update `_CP_TITLE_LABEL["rising"]` from `"Ascendant Style"` to `"Ascendant Presence"` to remove the word "style" from Rising titles entirely.

---

## 1. Two Changes Only

### Change 1 -- Add `_CP_LENS_WORD` dict and update summary f-string

**Add at module level** (one dict, no function):
```python
_CP_LENS_WORD = {
    "sun": "identity",
    "moon": "emotion",
    "rising": "presence",
}
```

**Update** the summary f-string in `_placement_traits()`:

Before:
```python
summary = f"{sign['name']} {chart_point['name']}, {house['label']}: {house['topic'].split(',')[0].strip()} themes with {sign['name'].lower()}-style {chart_point['lens'].split(',')[0].strip()}."
```

After:
```python
summary = f"{sign['name']} {chart_point['name']}, {house['label']}: {house['topic'].split(',')[0].strip()} themes with {sign['name'].lower()}-style {_CP_LENS_WORD[chart_point_slug]}."
```

That is the only change to the summary line. `chart_point['lens']` is no longer used in the summary.

**Why this works:** for Rising, the ending is now `"...with aries-style presence."` -- no double "style" token. The 4-gram `"{sign}-style presence"` is unique per sign and appears on at most 12 pages (1 sign × 12 houses, 1 chartpoint) = 2.8%. For Sun: `"...aries-style identity."` = 12 pages = 2.8%. For Moon: same. All well below the 15% gate.

**Verify:**
```bash
grep -n "lens\]\[.split\|outer style\|lens\]" backend/seo_m3_builders.py | grep -i summary
# Expected: no output (summary line no longer references chart_point['lens'])
```

---

### Change 2 -- Delete Pattern B, use one single title template, update `_CP_TITLE_LABEL["rising"]`

**Update `_CP_TITLE_LABEL`** (change the "rising" value only):
```python
_CP_TITLE_LABEL = {
    "sun": "Solar Drive",
    "moon": "Lunar Instinct",
    "rising": "Ascendant Presence",  # was "Ascendant Style" -- removes "Style" word from all Rising titles
}
```

**Replace** the `meta_title` assignment in `build_character_placement_doc()` with one single template (no hash, no Pattern B, no conditional):
```python
"meta_title": f"{sign} {_CP_TITLE_LABEL[chart_point_slug]}, {house['label']}: {_SIGN_ADJ[sign_slug]} {house['topic'].split(',')[0].strip().title()}",
```

Delete Pattern B and the `_hash_index` call in the `meta_title` line entirely -- they are no longer needed.

**Jaccard proof -- all three axes (stop words excluded from token count):**

Axis 1 -- same chartpoint + same house, different sign (Rising 7th: Capricorn vs Taurus):
- `"Capricorn Ascendant Presence, 7th House: Structured Partnership"`
- `"Taurus Ascendant Presence, 7th House: Grounded Partnership"`
- Tokens: {capricorn, ascendant, presence, 7th, house, structured, partnership} = 7
- vs {taurus, ascendant, presence, 7th, house, grounded, partnership} = 7
- Intersection: {ascendant, presence, 7th, house, partnership} = 5
- Union: {capricorn, taurus, ascendant, presence, 7th, house, structured, grounded, partnership} = 9
- **Jaccard: 5/9 = 55%** ✅

Axis 2 -- same sign + same house, different chartpoint (Capricorn 7th: Sun vs Moon):
- `"Capricorn Solar Drive, 7th House: Structured Partnership"`
- `"Capricorn Lunar Instinct, 7th House: Structured Partnership"`
- Intersection: {capricorn, 7th, house, structured, partnership} = 5
- Union: {capricorn, solar, drive, lunar, instinct, 7th, house, structured, partnership} = 9
- **Jaccard: 5/9 = 55%** ✅

Axis 3 -- same sign + same chartpoint, different house (Capricorn Rising: 1H vs 7H):
- `"Capricorn Ascendant Presence, 1st House: Structured Identity"`
- `"Capricorn Ascendant Presence, 7th House: Structured Partnership"`
- Intersection: {capricorn, ascendant, presence, house, structured} = 5
- Union: {capricorn, ascendant, presence, 1st, 7th, house, structured, identity, partnership} = 9
- **Jaccard: 5/9 = 55%** ✅

All three axes: 55% < 60% gate. ✅

**Verify:**
```bash
grep -n "hash_index.*meta_title\|Pattern B\|SIGN_ADJ.*Placement\|Ascendant Style" backend/seo_m3_builders.py
# Expected: no output
```

---

## 2. What to Keep Unchanged

| Element | Status | Action |
|---|---|---|
| `_CP_FAQ_GOOD_DIFFICULT` dict | ✅ Confirmed working | Keep exactly as-is |
| `_CP_FAQ_CONFIRM` dict | ✅ Confirmed working | Keep exactly as-is |
| `_hash_index()` function | Still used by FAQ | Keep (remove from meta_title only) |
| `_SIGN_ADJ` dict | Used in new title template | Keep |
| Chart-point vocab edits in `strengths` / `shadow_side` f-strings | Keep if present | Keep |

---

## 3. Tests -- Required Before Submitting

```bash
python3 tests/echo_pace_seo20k_scan.py
```

All three required:
- L1 Character Placements worst pair **< 50%** ✅
- L2 **0** four-gram violations > 15% ✅
- L3 no title pair > 60% Jaccard ✅

**Grep checks before submitting:**
```bash
# Change 1 confirmed -- no more lens/outer style in summary:
grep -n "outer style\|chart_point\['lens'\]" backend/seo_m3_builders.py

# Change 2 confirmed -- no more Pattern B or Ascendant Style:
grep -n "Ascendant Style\|hash_index.*meta_title\|Placement\"" backend/seo_m3_builders.py

# All banned stems still absent:
grep -n "strengths and shadows that become clearer\|Rising and house placements especially\|blend makes house\|life themes revolve\|recurring theme learning\|house turns attention\|house story tends\|distinct experiential texture\|rhythm shape how" backend/seo_m3_builders.py
# All expected: no output
```

**Self-checks:**
1. Print summary for Gemini Rising in 1st House: must end with `"gemini-style presence."` -- no "outer style", no "style" repeated.
2. Print all 3 meta_titles for Capricorn in 7th House: must be `"Capricorn Solar Drive, 7th House: Structured Partnership"` / `"Capricorn Lunar Instinct, 7th House: Structured Partnership"` / `"Capricorn Ascendant Presence, 7th House: Structured Partnership"`. Each has a distinct 2-word chartpoint label.
3. Print all 12 meta_titles for Rising in 7th House: each must have a distinct sign adjective. No two identical.
4. Print meta_titles for Capricorn Rising across all 12 houses: each house must differ in both the house label AND the topic word. Verify Jaccard between any two is below 60%.

---

## 4. Scan History

| Scan | Date | L1 | Status | Top L2 Violation | L3 Worst Pair | Verdict |
|---|---|---|---|---|---|---|
| Pre-fix (original) | 2026-05-31 | 93.4% | ❌ BLOCKED | "time rising house placements" 100% | -- | FAIL |
| v1-v5 | 2026-06-02 | 52.0%-96.1% | ❌ various | Various boilerplate 21-100% | -- | FAIL |
| v5-FULL | 2026-06-02 | 92.4% | ❌ BLOCKED | "shape how placement unfolds" 35% | Rising Capricorn 7H vs Rising Taurus 7H | ❌ FAQ fix confirmed; summary templates re-introduced stems |
| v6 | 2026-06-02 | 96.1% | ❌ BLOCKED | "style outer style rising" 22% | Rising Capricorn 7H vs Gemini Ascendant Style | ❌ "outer style" 2-word lens fragment + Pattern B cross-house clustering |
| **v7 target** | -- | **< 50%** | ✅ PASS | **0** | < 60% Jaccard | -- |

**Confirmed working (do not touch):** `_CP_FAQ_GOOD_DIFFICULT`, `_CP_FAQ_CONFIRM`, `_SIGN_ADJ`, `_CP_TITLE_LABEL` shape (update "rising" value only).

**Cumulative banned phrases:**
`"strengths and shadows that become clearer"` · `"rising house placements especially"` · `"shape how placement unfolds"` · `"distinct experiential texture"` · `"style outer style rising"` · `"blend makes house site"` · `"life themes revolve around"` · `"recurring theme learning how"` · `"house turns attention toward"` · `"house story tends feel"` · `"time place details house"`
