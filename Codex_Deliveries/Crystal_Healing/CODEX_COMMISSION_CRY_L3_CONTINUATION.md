# Codex Commission: CRY-L3 Continuation
> Status: READY TO ISSUE
> File: `backend/crystal_data.py`
> Scan command: `PYTHONDONTWRITEBYTECODE=1 python3 tests/echo_pace_cry_scan.py`
> Target: Crystal L1 < 20% · Intention L1 < 25% · L2 = 0 · L3 = 0

---

## Current Scan (CRY-L3 partial delivery)

```
Crystal pages:   L1 32.1%  L2 FAIL  L3 PASS
Intention pages: L1 38.6%  L2 FAIL  L3 PASS
```

Progress: L1 moved (Crystal 49.5% → 32.1%, Intention 45.4% → 38.6%). L3 clean.
Still failing: L2 violations remain. L1 targets not met (< 20% / < 25%).

---

## L2 Root Cause -- Three Functions, Three Fixed Closing Phrases

Code review identifies three functions that produce fixed sentences appearing
on a large majority of the 50 crystal pages. These are the L2 violation source.

### Source 1 -- `_care_note()` sunlight closing (line ~2065)

```python
# This sentence appears on ~45 of 50 pages (all non-photosensitive crystals):
sun = f"Sunlight for {name} should stay brief; repeated heat is harder on
        {name.lower()} than {first_method} or {second_method}."
```

45/50 = 90% repetition rate. The bigrams `"stay brief"`, `"repeated heat"`, 
`"harder on"` are L2 violations at 90%.

**Fix:** Replace with a hash-selected variant pool (modulus=5, seed from slug):

```python
SUN_SAFE_VARIANTS = [
    f"For {name}, sunlight works as a quick energiser but extended direct exposure can stress the surface over time; {first_method} or {second_method} is a gentler default.",
    f"{name} can take brief morning light, but leaving it in full sun for hours is harder on the stone than {first_method} and tends to dry the surface.",
    f"With {name}, brief sunlight is fine; sustained heat accumulates in the structure, so {first_method} after a long sun session is worth doing.",
    f"Use sunlight sparingly with {name} -- a short clearing pause is useful, but {first_method} or {second_method} accomplishes the same reset without the prolonged heat.",
    f"Sunlight is not the primary tool for {name}; {first_method} and {second_method} are more reliable and gentler on the surface over many uses.",
]
sun_seed = _hash_index(slug, "sun", modulus=5)
sun = SUN_SAFE_VARIANTS[sun_seed]
```

For photosensitive crystals (amethyst, rose-quartz, fluorite, aquamarine, kunzite),
keep the current moonlight-only sentence but also make it hash-selected (2 variants,
modulus=2) to avoid structural repetition across those 5 crystals.

### Source 2 -- `_daily_use_note()` middle-ground closing (line ~2079)

```python
# This sentence appears on ~29 of 50 pages (neither high-intensity nor gentle):
return f"{name} usually sits in the middle ground: steady enough for regular use,
        but clearer when you work with it on purpose instead of leaving it on
        autopilot. Think in focused windows rather than nonstop exposure."
```

29/50 = 58% repetition. The bigrams `"focused windows"`, `"nonstop exposure"`,
`"middle ground"` are L2 violations.

**Fix:** Replace with 6 structurally distinct variants (modulus=6, seed from slug):

```python
MIDGROUND_VARIANTS = [
    f"{name} is reliable for regular use, but intentional sessions serve it better than passive wearing. A few focused hours tend to be cleaner than all-day contact.",
    f"Most people find {name} steady enough for daily practice without the intensity spikes that higher-energy stones can produce. Working with it deliberately rather than continuously keeps the relationship clearer.",
    f"{name} sits in the cooperative middle: it does not demand breaks the way high-intensity stones do, but it responds better when you bring actual attention to the session rather than wearing it passively.",
    f"Regular use of {name} is fine. Where it works best is in purposeful contact -- meditation, ritual, or a deliberate carry -- rather than being forgotten in a pocket for days at a time.",
    f"{name} is a consistent everyday stone that works across most energy levels. The main guideline is attention over duration: thirty focused minutes matters more than twelve distracted hours.",
    f"For {name}, the quality of the session matters more than the length of it. Daily use is comfortable; the only real guideline is to engage with it on purpose rather than treating it as permanent jewelry.",
]
mid_seed = _hash_index(slug, "daily", modulus=6)
return MIDGROUND_VARIANTS[mid_seed]
```

### Source 3 -- `_who_note()` non-Navaratna closing (line ~2101)

```python
# This sentence appears on ~40 of 50 pages (all non-Navaratna crystals):
return f"{name} usually suits {notes['best_for']}. Its {profile['planet'].lower()} 
        symbolism gives the stone a recognizable ritual personality instead of making
        it feel interchangeable with every other crystal in the same category."
```

40/50 = 80% repetition. The bigrams `"recognizable ritual"`, `"feel interchangeable"`,
`"every other crystal"` are L2 violations.

**Fix:** Replace the fixed closing with 6 hash-selected variants:

```python
WHO_CLOSE_VARIANTS = [
    f"Its {profile['planet'].lower()} symbolism gives it a distinct energetic signature that makes it a considered choice rather than a generic substitution.",
    f"The {profile['planet'].lower()} connection gives {name} a ritual personality that tends to appeal most to practitioners who want something specific, not something general.",
    f"Its association with {profile['planet'].lower()} energy gives the stone a recognizable character across different traditions, which makes it a reliable anchor rather than a filler stone.",
    f"Because of its {profile['planet'].lower()} lineage, {name} carries a more defined quality than generalist stones -- useful when the practitioner has a clear intention rather than a broad one.",
    f"The {profile['planet'].lower()} resonance gives it a focused quality that suits practitioners who know what they are working with rather than those building a first collection.",
    f"Its {profile['planet'].lower()} character makes it a stone with a point of view -- it is not interchangeable with every other crystal in the same color family.",
]
who_seed = _hash_index(slug, "who", modulus=6)
closing = WHO_CLOSE_VARIANTS[who_seed]
return f"{name} usually suits {notes['best_for']}. {closing}"
```

---

## L1 Gap -- healing_properties Must Be Prose Strings (Not Lists)

The original CRY-L3 brief required Fix 2: `healing_properties` sub-fields must
be **strings** (prose), not lists. The current delivery still returns lists:

```python
# Current (WRONG -- still list format):
"healing_properties": {
    "emotional": ["string1; string2; string3.", "string4; string5.", ...],
    "physical":  ["string6; string7.", ...],
    "spiritual": ["string8; string9.", ...],
}
```

The scanner reads list fields with `str(v)`, which converts the list to a string
representation including the bracket/quote characters. The short tag-pair fragments
inside those lists still share vocabulary across crystals in the same intent family.

**Fix:** `_build_healing_properties()` must return:
```python
{
    "emotional": "A single prose string of 2-4 sentences.",
    "physical":  "A single prose string of 2-4 sentences.",
    "spiritual": "A single prose string of 2-4 sentences.",
}
```

Each prose string must:
- Contain the crystal's geological name or a distinctive physical property
- NOT use the benefit tag labels as vocabulary ("abundance calm", "joy steadiness" etc.)
- Use the CRYSTAL_COPY dict's `identity`, `signature`, `best_for` fields as the prose vocabulary anchor

Example for Citrine:
```python
"emotional": (
    "Citrine carries a warm, solar quality built around its iron-trace yellow colour. "
    "It tends to shift stagnant inner states by restoring a sense of forward possibility "
    "rather than by processing the source of the block. People reach for it when they need "
    "momentum more than comfort."
),
```

Example for Pyrite:
```python
"emotional": (
    "Pyrite brings an iron-structured, strategic quality to emotional work. "
    "It does not open or soften -- it organises. The metallic density of its surface "
    "is part of the signal: this is a stone that builds a frame around a goal rather "
    "than dissolving resistance around it."
),
```

Write prose in this form for ALL 50 crystals across all three axes (emotional/physical/spiritual).
Each prose string must contain at least one geological or compositional vocabulary word
specific to that crystal (iron sulfide, manganese silicate, calcium carbonate, etc.)
OR a cultural/mythological reference that is unique to that stone.

---

## Summary -- Three Fixes Required

| Fix | Function | Change |
|---|---|---|
| L2-1 | `_care_note()` | Replace fixed sunlight sentence with 5 hash-selected variants |
| L2-2 | `_daily_use_note()` | Replace fixed middle-ground return with 6 hash-selected variants |
| L2-3 | `_who_note()` | Replace fixed closing phrase with 6 hash-selected variants |
| L1 | `_build_healing_properties()` | Convert list fields to single prose strings (2-4 sentences each, geological vocabulary, no benefit tag labels) |

**No other files are modified.**

---

## Acceptance Criteria (unchanged from CRY-L3 brief)

1. Scan passes: Crystal L1 < 20% · Intention L1 < 25% · L2 = 0 · L3 = 0
2. `healing_properties.emotional`, `healing_properties.physical`, `healing_properties.spiritual` are all strings (not lists)
3. No FAQ answer contains an intent slug string verbatim
4. No `how_to_use` entry contains another crystal's proper name
