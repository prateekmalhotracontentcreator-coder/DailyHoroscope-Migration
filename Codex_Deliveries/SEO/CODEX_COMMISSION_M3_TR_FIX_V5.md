# Codex Commission: M3-TR-FIX v5 -- Transit Profiles
> File: `backend/seo_m3_builders.py`
> Scan: `python3 tests/echo_pace_seo20k_scan.py`
> Target: Transit Profiles L1 < 50% · L2 = 0 · L3 = 0

---

## Current Scan (v4 delivery, not committed)

```
Transit Profiles: L1 70.4% BLOCKED · L2 FAIL · L3 FAIL
```

FAQ lines 758 + 762 were fixed in v4. New L2 source now exposed: the
unchanged personal-impact FAQ answer at line 789.

---

## The One Remaining L2 Violation -- Line 789

**Root cause:** The fourth FAQ item ("How do I check my personal impact?") is a fully fixed sentence with only `{sign}` and `{planet}` as variable fills. The fixed skeleton words -- "Ascendant", "review", "touches", "natal", "grahas", "current", "dashas", "zone" -- survive stop-word filtering and appear identically on all 108 transit pages.

**Violating line (line 789 in `_transit_faq()`):**
```python
{
    "question": "How do I check my personal impact?",
    "answer": f"Check which house {sign} occupies from your Ascendant, then review whether {planet} touches natal grahas or current dashas in the same zone.",
},
```

**Replace with a hash-selected variant pool:**

```python
personal_impact_seed = _hash_index(planet_slug, sign_slug, "pimpact", 6)
personal_impact_answers = [
    f"Start with the house {sign} rules in your natal chart. If {planet} is moving through that zone or forming an aspect to natal placements there, the personal effect is direct.",
    f"Look up which house {sign} falls in from your Ascendant. When {planet} transits that sector, the theme of that house intensifies first.",
    f"Check your natal chart for {sign} placements. {planet} transiting through or aspecting that house activates the zone where its effects will be most personally felt.",
    f"The personal impact depends on which house {sign} occupies for your Ascendant. {planet} will do its strongest work in the life domain that house governs.",
    f"Your Ascendant determines which house {sign} rules for you. A {planet} transit becomes personal when it crosses into or aspects natal planets in that house.",
    f"Review your natal placements in {sign}. Wherever {planet} makes contact -- through the same house or a direct aspect -- is where this transit becomes personally relevant.",
]
```

Then replace the fixed answer with:
```python
{
    "question": "How do I check my personal impact?",
    "answer": personal_impact_answers[personal_impact_seed],
},
```

**Note:** `planet_slug` and `sign_slug` are already in scope in `_transit_faq()` (they are used for the other variant seeds added in v4). The seed key `"pimpact"` is distinct from `"faq_q2"` and `"faq_q3"` used for the v4 fixes.

---

## What Must NOT Change

- Lines 758-762 (the v4 fixes for FAQ Q2 and Q3) -- already correct, do not touch
- All other functions in the file -- do not touch
- The scan script -- do not touch

---

## Acceptance Criteria

Single run of `python3 tests/echo_pace_seo20k_scan.py`:
- Transit Profiles L1 < 50%
- Transit Profiles L2 = 0 violations
- Transit Profiles L3 < 60% Jaccard

Do not commit until the scan is clean.
