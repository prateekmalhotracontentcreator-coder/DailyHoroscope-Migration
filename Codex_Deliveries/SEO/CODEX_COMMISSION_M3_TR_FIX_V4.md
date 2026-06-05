# Codex Commission: M3-TR-FIX v4 -- Transit Profiles
> File: `backend/seo_m3_builders.py`
> Scan: `python3 tests/echo_pace_seo20k_scan.py`
> Target: Transit Profiles L1 < 50% · L2 = 0 · L3 = 0

---

## Current Scan (v3 delivery, not committed)

```
Transit Profiles: L1 72.7% BLOCKED · L2 FAIL · L3 FAIL
```

L1 REGRESSED from 64.3% → 72.7%. L2 still failing with three new fixed phrases.

---

## Step 1 -- Fix the two fixed sentences in `_transit_faq()` (lines 757-762)

This is the only change in Step 1. Do not touch anything else yet.

**Location:** `_transit_faq()` function. The two violating answers are:

```python
# LINE 758 -- VIOLATING (clear gifts, pressure points, timing lessons -- 100% shared):
{
    "question": f"Is {planet} in {sign} good or bad?",
    "answer": f"It is not purely good or bad. {planet} in {sign} has clear gifts, pressure points, and timing lessons that show up differently in each chart.",
},

# LINE 762 -- VIOLATING (fully fixed, no fills -- 100% shared on all 108 pages):
{
    "question": f"What should I avoid during {planet} in {sign}?",
    "answer": "Avoid the transit's excess expression: impatience, overconfidence, scattered timing, or reacting before your chart context is clear.",
},
```

**Replace with hash-selected variants. Seed: `_hash_index(planet_slug, sign_slug, "faq_q2", 6)` for the first, `_hash_index(planet_slug, sign_slug, "faq_q3", 6)` for the second.**

```python
faq_q2_variant = _hash_index(planet_slug, sign_slug, "faq_q2", 6)
faq_q2_answers = [
    f"{planet} in {sign} carries both a productive edge and a pressure pattern. Which one dominates depends on how well your natal chart handles {sign_meta['element'].lower()} energy.",
    f"Neither purely helpful nor purely difficult. {planet} in {sign} opens certain kinds of growth while also exposing friction -- especially where {sign_meta['name']} themes are already under pressure in your chart.",
    f"The same transit lands differently for different charts. {planet} in {sign} has a characteristic gift and a characteristic blind spot; your rising sign and current dasha determine which of those feels louder.",
    f"It carries opportunity and challenge in proportion to your chart's relationship with {sign_meta['name']}. What works well for one Ascendant can be the friction point for another.",
    f"Not a fixed good or bad -- it depends on the house {sign_meta['name']} rules for your Ascendant and whether {planet} aspects natal placements during the window.",
    f"Every transit has a productive face and a distorted one. {planet} in {sign} is no exception; the difference between the two is usually a question of timing, intention, and chart context.",
]

faq_q3_variant = _hash_index(planet_slug, sign_slug, "faq_q3", 6)
faq_q3_answers = [
    f"Watch for the {sign_meta['element'].lower()} sign tendency to amplify {planet_meta['watch']} beyond what the situation actually requires.",
    f"The main risk is letting {planet_meta['watch']} drive decisions before the chart context for this transit becomes clear.",
    f"Avoid committing to the transit's first impulse. {planet_meta['watch']} tends to peak early; giving it a few days before acting usually changes the picture.",
    f"The distorted expression of this transit is {planet_meta['watch']} wearing the mask of certainty. Wait until the pattern repeats before trusting it.",
    f"Over-relying on {sign_meta['modality'].lower()} momentum is the usual risk. {planet_meta['watch']} grows louder as the transit peaks -- pacing matters more than speed.",
    f"React only after the transiting pattern has shown up at least twice. {planet_meta['watch']} under {sign_meta['element'].lower()} sign energy can look like clarity before it becomes a mistake.",
]
```

Then in the FAQ list, use:
```python
{
    "question": f"Is {planet} in {sign} good or bad?",
    "answer": faq_q2_answers[faq_q2_variant],
},
{
    "question": f"What should I avoid during {planet} in {sign}?",
    "answer": faq_q3_answers[faq_q3_variant],
},
```

---

## Step 2 -- Run the scan BEFORE any further changes

After applying only Step 1, run:
```
python3 tests/echo_pace_seo20k_scan.py
```

Report the Transit Profiles L1, L2, L3 result.

- If L2 passes and L1 drops below 50%: delivery is complete.
- If L2 passes but L1 is still ≥ 50%: report the result. The L1 regression (64.3% → 72.7%) suggests a change in the previous pass introduced new structural vocabulary. That needs a separate investigation -- do not attempt to fix L1 further without reporting first.
- If any new L2 violations appear: report the exact phrases.

---

## What Must NOT Change

- `_transit_themes()` -- do not alter (element-aware variants are correct)
- `_transit_watch_for()` -- do not alter (element-aware variants are correct)
- `_transit_remedies()` -- do not alter (planet-specific 6-variant pool is correct)
- `_transit_sign_impacts()` -- do not alter
- `summary` field at line 791 -- do not alter
- All scan scripts -- do not alter

---

## Acceptance Criteria

Single run of `python3 tests/echo_pace_seo20k_scan.py` shows:
- Transit Profiles L1 < 50%
- Transit Profiles L2 = 0 violations
- Transit Profiles L3 < 60% Jaccard
