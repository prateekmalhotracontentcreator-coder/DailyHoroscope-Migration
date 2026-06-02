# Codex Commission: M3-CP-FIX -- Character Placements Generator Fix (v5-FULL)
> Thread: SEO Legacy (M3 section) | File: `backend/seo_m3_builders.py`
> Issued: 2026-06-02 (v5-FULL -- definitive brief from actual repo baseline; 4 prior passes analysed)
> Scan script: `tests/echo_pace_seo20k_scan.py` | Scan report: `SEO_20K/SEO_TRACKER.md`

---

## Commission Brief (5 lines)

This brief starts from the actual committed repo state (93.4% BLOCKED). Prior v1-v4 passes never reached the repo -- all were local thread edits. After reading the live `_placement_traits()` function (lines 290-347) directly, the failure is concentrated in **two hardcoded FAQ answer strings** that are identical on all 432 pages: `"It depends on chart support. Every placement has strengths and shadows that become clearer..."` (→ `"strengths shadows become clearer"` at 100%) and `"Run your birth chart with accurate birth time. Rising and house placements especially..."` (→ `"rising house placements especially"` at 100%). Fix these two strings first -- replace each with a **12-entry per-chartpoint-per-sign dict** (no new function, just a dict literal and a `.get()` call). The remaining structural work is: (1) break the `summary` f-string (lines 294-297) -- it uses `"blends"` + `"The result is a placement that expresses itself through"` as fixed stems across all 432 pages; replace with 3 variants hash-selected by `(sign_slug, chart_point_slug, house_slug)` modulus 3; (2) apply chart-point vocabulary separation -- Sun sentences use identity/purpose/achievement vocab, Moon sentences use emotion/memory/comfort vocab, Rising sentences use presentation/instinct/outer-style vocab -- **inside the existing `strengths`, `shadow_side`, and `vedic_perspective` f-string lists only, by editing the f-string text, not by adding new structures**; (3) fix `meta_title` -- replace the single template with 2 alternating patterns plus a `_SIGN_ADJ` dict (12 entries, module-level constant). **Critical constraint from v1-v4 learnings: do not add any new function, class, or loop -- every new code structure across 4 prior passes introduced universal stems that collapsed L1 back above 90%.**

---

## 1. Exact Code Location

File: `backend/seo_m3_builders.py`
Function: `_placement_traits()` at line 290 and `build_character_placement_doc()` at line 350.

**Read these two functions before making any change.** The full function body is lines 290-363.

---

## 2. Fixes in Order of Impact

### Fix A -- Two hardcoded FAQ answers (removes 2 × 100% violations immediately)

**Current code (lines 336-345):**
```python
{
    "question": "Is this placement good or difficult?",
    "answer": "It depends on chart support. Every placement has strengths and shadows that become clearer through dignity, aspects, and dasha timing.",
},
{
    "question": "How do I confirm if this is my placement?",
    "answer": "Run your birth chart with accurate birth time. Rising and house placements especially depend on exact time and location.",
},
```

**Fix:** Replace the hardcoded `answer` strings with **dict lookups** drawing from per-chartpoint answer pools defined as module-level dict literals. No new function. Pattern:

```python
# Module-level constant (add near top of file, after existing imports/dicts):
_CP_FAQ_GOOD_DIFFICULT = {
    "sun": [
        "Solar placements carry purposeful energy when the Sun is well-dignified. Challenged dignity can make the drive to shine in this area feel blocked or over-effortful.",
        "Sun here sharpens identity through this house. Whether that feels empowering or pressuring depends on dignity, aspect support, and dasha activation.",
        "This Sun position can be a source of real confidence. Squares or debilitation to the Sun may turn the same domain into a recurring test of ego strength.",
    ],
    "moon": [
        "Moon placements are sensitive to dignity and waxing-waning cycle. In a strong sign the emotional intelligence here flows easily; in a challenged sign the same instincts can feel reactive.",
        "The Moon here makes this life area emotionally central. Nourishing transits and a healthy dasha cycle often bring out its best; malefic aspects can amplify anxiety around this theme.",
        "Comfort and security needs are concentrated in this house. Supportive aspects make the placement stabilising; difficult ones can make needs feel hard to meet.",
    ],
    "rising": [
        "Rising sign placements shape first impressions and body. Their expression depends heavily on lagna lord strength and any planets aspecting the ascendant.",
        "The Ascendant here colours how others read you in this area before you speak. A strong lagna lord makes that impression feel natural; a weak one may cause self-consciousness.",
        "This Rising placement defines the outer layer of personality. Its quality shifts with the lagna lord's dignity, house position, and the dashas running at any given time.",
    ],
}

_CP_FAQ_CONFIRM = {
    "sun": [
        "Check your birth chart for the Sun's house position. An accurate birth time within 15 minutes is enough to confirm solar house placement reliably.",
        "The Sun changes signs roughly once a month but moves through houses based on birth time. Use a Vedic chart with your exact birth time and place.",
        "Solar house placement is birth-time-sensitive but more forgiving than the Ascendant. A birth time accurate to ±30 minutes is usually sufficient.",
    ],
    "moon": [
        "Moon house placement requires a birth time accurate to within 2 hours. Use a Vedic calculator with your exact date, time, and place of birth.",
        "Confirm by running a Vedic birth chart. The Moon moves roughly 13° per day, so a precise birth time is important for accurate house placement.",
        "For Moon placements: an accurate birth time is essential. Even a 30-minute error can shift the Moon's house. Use hospital records if possible.",
    ],
    "rising": [
        "The Rising sign changes every 2 hours on average. You need a birth time accurate to within 15-20 minutes to confirm your Ascendant reliably.",
        "Ascendant placement is the most time-sensitive point in the chart. Verify with your birth certificate or hospital record for the most accurate reading.",
        "Confirm your Rising sign with an exact birth time. Even a 10-minute difference can shift the Ascendant, especially near sign boundaries.",
    ],
}
```

Then in the FAQ block, replace the hardcoded answers:
```python
{
    "question": "Is this placement good or difficult?",
    "answer": _CP_FAQ_GOOD_DIFFICULT[chart_point_slug][_hash_index(sign_slug, chart_point_slug, house_slug, 3)],
},
{
    "question": "How do I confirm if this is my placement?",
    "answer": _CP_FAQ_CONFIRM[chart_point_slug][_hash_index(sign_slug, chart_point_slug, house_slug, 3)],
},
```

If `_hash_index()` does not already exist in the file, add this minimal version at module level:
```python
def _hash_index(a: str, b: str, c: str, n: int) -> int:
    import hashlib
    return int(hashlib.md5(f"{a}|{b}|{c}".encode()).hexdigest(), 16) % n
```

**Verify Fix A:** after editing, grep the file:
```bash
grep -n "strengths and shadows that become clearer\|Rising and house placements especially" backend/seo_m3_builders.py
# Expected: no output
```

---

### Fix B -- Break the summary f-string (removes "blends" + "The result is a placement" shared stems)

**Current code (lines 294-297):**
```python
summary = (
    f"{sign['name']} {chart_point['name']} in the {house['label']} blends {chart_point['lens']} with themes of {house['topic']}. "
    f"The result is a placement that expresses itself through {sign['element'].lower()} instinct and {sign['modality'].lower()} pacing."
)
```

**Fix:** Replace with 3 variant templates, hash-selected. Add as a module-level list:
```python
_SUMMARY_TEMPLATES = [
    lambda s, cp, h: (
        f"{s['name']} {cp['name']} in the {h['label']} brings {cp['lens']} energy into the domain of {h['topic']}. "
        f"{s['element']} instinct and {s['modality'].lower()} rhythm shape how this placement unfolds."
    ),
    lambda s, cp, h: (
        f"With {s['name']} as the sign and {h['label']} as the stage, {cp['name']} energy here is filtered through {h['topic']}. "
        f"The {s['element'].lower()} element gives this combination a {s['modality'].lower()} quality in action."
    ),
    lambda s, cp, h: (
        f"This placement places {cp['lens']} within the context of {h['topic']}. "
        f"{s['name']}'s {s['element'].lower()} nature and {s['modality'].lower()} drive give it a distinct experiential texture."
    ),
]
```

Then replace the `summary` assignment:
```python
summary = _SUMMARY_TEMPLATES[_hash_index(sign_slug, chart_point_slug, house_slug, 3)](sign, chart_point, house)
```

---

### Fix C -- Chart-point vocabulary in strengths and shadow_side f-strings

The `strengths` and `shadow_side` lists (lines 312-321) currently use neutral vocabulary for all three chart points. Edit the f-string text **inside the existing lists** to use chart-point-appropriate vocabulary. Do not restructure the lists -- only edit the string values.

**Vocabulary rule (inline, no new function needed):**

In the **existing `strengths` f-strings**: for each sentence that mentions the chart point's expression, use:
- Sun: words from `{drive, purpose, recognition, authority, creative will}`
- Moon: words from `{comfort, instinct, emotional attunement, nurturing, inner security}`
- Rising: words from `{presentation, first impression, physical approach, outer style, instinctive manner}`

Example change -- existing line 315:
```python
# Before (neutral):
f"Often memorable because the {chart_point['name']} expresses itself clearly in public or close relationships.",
# After (use chart_point_slug to choose vocabulary):
f"Often recognised for the {('purposeful drive' if chart_point_slug == 'sun' else 'emotional attunement' if chart_point_slug == 'moon' else 'distinctive outer style')} this {chart_point['name']} placement projects.",
```

Apply the same pattern to the `shadow_side` f-strings (lines 317-321): Sun shadows = ego/pride patterns, Moon shadows = emotional reactivity/insecurity, Rising shadows = self-consciousness/projection.

---

### Fix D -- meta_title two-pattern alternation with sign adjective

Add at module level (one dict, no function):
```python
_SIGN_ADJ = {
    "aries": "Bold", "taurus": "Grounded", "gemini": "Versatile",
    "cancer": "Nurturing", "leo": "Radiant", "virgo": "Discerning",
    "libra": "Balanced", "scorpio": "Intense", "sagittarius": "Expansive",
    "capricorn": "Structured", "aquarius": "Independent", "pisces": "Fluid",
}
```

In `build_character_placement_doc()` (line 350), replace the single `meta_title` template:
```python
# Before:
"meta_title": f"{sign} {chart_point} in the {house['label']} - Personality & Life Themes",

# After:
"meta_title": (
    f"{sign} {chart_point} in the {house['label']} -- {house['topic'].title()} & Life Themes"
    if _hash_index(sign_slug, chart_point_slug, house_slug, 2) == 0
    else f"{chart_point} in {sign}: {_SIGN_ADJ[sign_slug]} {house['topic'].title()} Placement"
),
```

---

## 3. What NOT to Do (lessons from v1-v4)

Every prior pass that added new helper functions, generator classes, or sentence template systems introduced a new set of universal stems and collapsed L1 back above 90%. The pattern was consistent across all 4 attempts:

| Pass | New structure added | Result |
|---|---|---|
| v1 | New sentence pool functions | 94.4% BLOCKED -- new boilerplate replaced old |
| v2 | House-primary pool architecture | 62.7% FLAGGED -- new "house turns attention toward" 100% |
| v3 | Chart-point paragraph banks | 52.0% FLAGGED -- 3 new shared stems at 21-43% |
| v4 | Sign-family variance pool selectors | 96.1% BLOCKED -- new helper functions: "house story tends feel" 100% |

**Rule:** if you find yourself writing a new `def`, a new class, or a new loop to implement any fix -- stop. The only new code permitted is:
- `_hash_index()` if it doesn't already exist (4-line function, Fix A above)
- `_SIGN_ADJ` dict (Fix D)
- `_SUMMARY_TEMPLATES` list of lambdas (Fix B)
- `_CP_FAQ_GOOD_DIFFICULT` and `_CP_FAQ_CONFIRM` dicts (Fix A)

Everything else must be inline edits to the f-string text in the existing lists.

---

## 4. Tests -- Required Before Submitting

```bash
python3 tests/echo_pace_seo20k_scan.py
```

Pass criteria -- **all three required**:
- L1 Character Placements worst pair **< 50%** ✅
- L2 **0** four-gram violations > 15% frequency ✅
- L3 no title pair > 60% Jaccard ✅

**Include the scan output in your delivery note. Do not submit without passing scores.**

**Grep checks before submitting:**
```bash
# Fix A confirmed:
grep -n "strengths and shadows that become clearer\|Rising and house placements especially" backend/seo_m3_builders.py

# Fix B confirmed:
grep -n "blends.*lens\|The result is a placement" backend/seo_m3_builders.py

# All banned stems confirmed absent:
grep -n "blend makes house\|life themes revolve\|recurring theme learning\|house turns attention\|house story tends\|behaviour often sharpens\|house reading generically" backend/seo_m3_builders.py
# All three greps expected: no output
```

**Self-checks:**
1. Pull Scorpio Sun / Moon / Rising in 2nd House -- three pages must read as distinct psychological experiences (Sun=purpose/authority frame, Moon=emotional security frame, Rising=outer style frame).
2. Pull all 12 meta_titles for Rising in any house -- each must contain a distinct sign adjective; no two titles identical.
3. Pull all 12 "Is this placement good or difficult?" FAQ answers for Sun -- answers must vary (3 distinct answers across 12 signs, 4 signs per answer is fine; identical answer on all 12 is not).

---

## 5. Scan History

| Scan | Date | L1 | L1 Status | Top L2 Violation | Verdict |
|---|---|---|---|---|---|
| Pre-fix (original) | 2026-05-31 | 93.4% | ❌ BLOCKED | "time rising house placements" 100% | FAIL |
| v1 re-scan | 2026-06-02 | 94.4% | ❌ BLOCKED | New boilerplate at 32% | ❌ FAIL |
| v2 re-scan | 2026-06-02 | 62.7% | ⚠️ FLAGGED | "house turns attention toward" 100% | ❌ FAIL |
| v3 re-scan | 2026-06-02 | 52.0% | ⚠️ FLAGGED | "blend makes house site" 43% | ❌ FAIL -- closest result |
| v4 re-scan | 2026-06-02 | 96.1% | ❌ BLOCKED | "house story tends feel" 100% | ❌ FAIL -- regression |
| **v5 target** | -- | **< 50%** | ✅ PASS | **0** | -- |

**Cumulative banned phrases (must not appear on more than 1 page):**
`"strengths and shadows that become clearer"` · `"rising house placements especially"` · `"blend makes house site"` · `"life themes revolve around"` · `"recurring theme learning how"` · `"house turns attention toward"` · `"house story tends feel"` · `"behaviour often sharpens native"` · `"house reading generically gives"` · `"time place details house"` · `"details house based placements"`
