# Codex Commission: CRY-L3 -- Crystal Healing L1 TF-IDF Reduction
> Status: READY TO ISSUE
> Target file: `backend/crystal_data.py`
> Gate: ECHO/PACE L1 worst pair < 20% (currently 49.5%)
> Acceptance test: `PYTHONDONTWRITEBYTECODE=1 python3 tests/echo_pace_cry_scan.py`

---

## Background

CRY-L2 resolved L2 (verbatim n-gram) and L3 (title Jaccard) violations.
The module now reads:

```
Crystal pages:   L1 49.5% PASS | L2 0 | L3 0
Intention pages: L1 45.4% PASS | L2 0 | L3 0
```

L1 is technically PASS (gate < 50%) but it is dangerously close to FLAGGED
and well above the production ideal. Crystal is a high-value SEO vertical.
The target is worst-pair L1 < 20%, which requires structural fixes to three
content fields -- not just vocabulary swaps.

---

## Root Cause (Diagnosed by CC 2026-06-04)

### 1. FAQ answers use a fill-in template (PRIMARY driver)

Every crystal's FAQ reuses the same 5 sentence skeletons with only the crystal
name and intent slug substituted. For the worst pair (Citrine vs Pyrite, 50.0%),
the FAQ body carries 20 shared tokens out of 80-84 total -- the single biggest
contributor to cosine similarity.

The exact template being repeated:

```
Q1: "[X] tends to be explored when the real goal is [intent], [intent2], or the
    steadier side of [intent3]."

Q2: "[X] is most often associated with [chakra], so people use it when they want
    those centers to feel clearer and more cooperative."

Q3: "[X] is usually refreshed with [method1], then [method2] or [method3] as
    needed. Keep the routine light if you want the surface to stay bright."

Q4: "For [X], [intent] work usually feels cleaner in brief contact windows than
    in wearing it from dawn to sleep."

Q5: "If you want support around [intent1], [intent2], [intent3] and prefer
    [element] energy in [intent] rituals, [X] gives a steadier [intent] pulse
    than hotter stones."
```

The intent slug ("abundance & money", "love & relationships") is pasted
verbatim 3-4 times per crystal into FAQ answers. Crystals in the same intent
family (e.g. Citrine + Pyrite, both wealth stones) therefore share dense
clusters of high-IDF tokens.

### 2. Healing properties are keyword-pair fragments, not prose

Current format: `['abundance calm', 'joy steadiness', 'confidence calm']`

These 2-word fragments carry almost no differentiating signal. The L1 similarity
computation sees Citrine and Pyrite sharing 9 tokens in healing_properties alone.

### 3. Cross-crystal name mentions create artificial IDF spikes

Citrine `how_to_use`: "Pair with **pyrite** when you want strategy plus optimism."
Pyrite `how_to_use`: "Pair with **citrine** for wealth rituals."

"Pyrite" is a rare word in the corpus (high IDF weight). When it appears in BOTH
Citrine's body AND Pyrite's own body, the cosine score is artificially inflated.
Same pattern repeats across the corpus wherever crystals cross-reference each other
by name.

### 4. Mohs hardness and water_safe fields are missing

All 50 crystals show `mohs=?`, `water_safe=?`. This means cleansing methods
cannot reflect physical properties. Pyrite (iron sulfide, Mohs 6-6.5) MUST NOT
use water. Selenite (Mohs 2) dissolves in water. Citrine (quartz, Mohs 7) is
safe. When all crystals draw from the same cleansing method pool regardless of
material, cleansing sections contribute to shared vocabulary.

---

## The Three Required Fixes

### FIX 1 -- Rewrite all 250 FAQ answers (50 crystals × 5 answers)

**Rule: no FAQ answer may contain the intent slug string.**
"abundance & money", "love & relationships", "grief & emotional healing" etc.
must NOT appear in any FAQ answer. These are category labels, not prose.

**Each answer must be written from a different angle:**

| Q | Required angle |
|---|---|
| Q1 (What is X good for?) | The crystal's UNIQUE energy signature -- geological character, felt sense, or traditional use. NOT the intent category. |
| Q2 (Which chakra?) | WHY this chakra -- link to the crystal's color, composition, or mythology. "Citrine's warm yellow activates the solar plexus because..." not just "Solar Plexus." |
| Q3 (How to cleanse?) | Based on ACTUAL physical properties (Mohs hardness, water safety, composition). See material table below. NO generic template sentence. |
| Q4 (Daily use?) | Crystal-specific energy intensity. Moldavite and Shungite are high-intensity -- warn accordingly. Selenite and Rose Quartz are gentle -- state accordingly. |
| Q5 (Who should work with it?) | Crystal's archetype, mythology, cultural history, or astrological/Vedic association. NOT a re-statement of intents. |

**Example -- current (BAD):**
```
A1: Rhodonite tends to be explored when the real goal is healing, compassion,
    or the steadier side of love & relationships.
```

**Example -- target (GOOD):**
```
A1: Rhodonite is a manganese silicate with a distinctive rose-pink body cut
    through by black manganese oxide veins. That visual tension between softness
    and structure is exactly what it works with -- the capacity to hold both
    tenderness and accountability at the same time, which is why it is used
    in practices around forgiveness and emotional repair rather than just
    sentimental love.
```

**Example -- current (BAD):**
```
A1: Pyrite tends to be explored when the real goal is abundance & money,
    career success, or the steadier side of confidence & courage.
```

**Example -- target (GOOD):**
```
A1: Pyrite is an iron disulfide mineral whose metallic sheen earned it the
    nickname fool's gold, but its working energy is anything but naive.
    It brings an iron-framed, strategic quality to intention work -- the kind
    of confidence that builds a plan and defends it, rather than the open-handed
    optimism of yellow Citrine. People reach for it when they need structure
    around a goal, not just momentum.
```

### FIX 2 -- Replace healing_properties tag-pairs with prose sentences

**Current format (BAD):**
```python
"healing_properties": {
    "emotional": ["abundance calm", "joy steadiness", "confidence calm", "manifestation steadiness"],
    "physical":  ["supports energized action", "encourages lighter motivation", ...],
    "spiritual": ["abundance order", "joy focus", "confidence signal", "manifestation order"]
}
```

**Target format (GOOD):**
```python
"healing_properties": {
    "emotional": "Citrine carries a warm, solar quality that brightens emotional states
                  without forcing positivity. It tends to shift stagnant moods by
                  restoring a sense of forward possibility rather than by processing
                  what caused the block.",
    "physical":  "Often placed at the solar plexus or kept in a workspace, Citrine is
                  used to support sustained energetic output during planning and creative
                  work. It is one of the few crystals considered self-cleansing.",
    "spiritual": "In Vedic tradition Citrine is associated with Jupiter energy -- expansive,
                  optimistic, and connected to wealth earned through wisdom rather than
                  aggression. It is used in abundance grids as the activating, light-giving
                  anchor rather than as a protective boundary stone."
}
```

Each prose entry must be 2-4 sentences. Must contain crystal-specific vocabulary
(geological name, color description, physical structure, cultural/Vedic association,
or unique characteristic). Must NOT repeat the intent slug.

### FIX 3 -- Remove cross-crystal name mentions from how_to_use

**Rule:** No crystal's `how_to_use` list may contain another crystal's name.

Replace specific crystal names with directional descriptions:
- ~~"Pair with pyrite"~~ → "Pair with a metallic grounding stone"
- ~~"Pair with citrine"~~ → "Add a solar abundance stone"
- ~~"Pair with rose quartz"~~ → "Layer with a gentle heart-centered stone"
- ~~"Pair with rhodonite"~~ → "Combine with a forgiveness-and-accountability stone"

---

## Material Safety Table -- For Cleansing Methods

Use this to write accurate, differentiated cleansing methods per crystal.

**Water SAFE (Mohs 7+, non-reactive):**
Amethyst, Citrine, Clear Quartz, Rose Quartz, Smoky Quartz, Aquamarine, Tiger's Eye,
Carnelian, Bloodstone, Garnet, Ruby, Emerald, Diamond, Blue Sapphire, Yellow Sapphire,
Jade, Green Aventurine, Sunstone

**Water NOT SAFE -- will corrode or oxidise:**
- Pyrite (iron sulfide -- rusts on contact, never use water)
- Hematite (iron oxide -- oxidises)
- Malachite (copper carbonate -- toxic if wet and abraded)
- Red Coral, Pearl (organic -- water degrades surface over time)

**Water NOT SAFE -- will dissolve or crack:**
- Selenite, Angelite, Celestite (halides/evaporites, Mohs 2-3.5 -- dissolve)
- Calcite (Mohs 3 -- slowly dissolves in acidic water)
- Lepidolite (mica, flaky -- water damages layers)

**Photosensitive (will fade in sunlight):**
- Amethyst, Rose Quartz, Fluorite, Aquamarine, Kunzite -- use moonlight only

**Safe for all methods:**
- Clear Quartz, Tiger's Eye, Bloodstone, Carnelian, Black Tourmaline

Each crystal must have cleansing methods that are physically accurate for its
material. This is also important user safety information for our audience.

---

## Target Scores

| Metric | Current | Target |
|---|---|---|
| Crystal L1 worst pair | 49.5% | < 20% |
| Intention L1 worst pair | 45.4% | < 25% |
| L2 n-gram violations | 0 | 0 (must not regress) |
| L3 Jaccard violations | 0 | 0 (must not regress) |

The worst pairs currently are:
1. Citrine vs Pyrite (50.0%) -- both wealth crystals
2. Rhodonite vs Rhodochrosite (48.3%) -- both heart/healing crystals, similar names
3. Rose Quartz vs Rhodonite (41.8%) -- both love/heart
4. Amazonite vs Aquamarine (40.6%) -- both throat/water crystals

Even with perfect differentiation, semantically similar crystal pairs will always
share SOME vocabulary. The target of < 20% is achievable if FAQ answers contain
genuinely crystal-specific prose (geological identity, mythology, Vedic association)
rather than intent-category template fills.

---

## Acceptance Criteria

1. `PYTHONDONTWRITEBYTECODE=1 python3 tests/echo_pace_cry_scan.py` passes with:
   - Crystal pages L1 < 20%
   - Intention pages L1 < 25%
   - L2 = 0 violations (must not regress)
   - L3 = 0 violations (must not regress)

2. No FAQ answer contains any of these strings verbatim:
   `"abundance & money"`, `"love & relationships"`, `"grief & emotional healing"`,
   `"protection & safety"`, `"spiritual growth"`, `"career success"`,
   `"confidence & courage"`, `"clarity & focus"`, `"forgiveness & release"`,
   `"stress & anxiety"`, `"sleep & rest"`

3. `healing_properties.emotional`, `healing_properties.physical`,
   `healing_properties.spiritual` are all strings (prose), not lists.

4. No `how_to_use` entry contains another crystal's proper name.

5. `py_compile` passes (or `PYTHONDONTWRITEBYTECODE=1` import succeeds).

---

## Scope

Only `backend/crystal_data.py` is modified. No other file is touched.
The data structure itself does not change (same keys, same nesting) --
only the string values and the type of `healing_properties` sub-fields
(list → string).

**Note on healing_properties type change:** The scan body extractor
(`_crystal_body` in `tests/echo_pace_cry_scan.py`) already handles both
list and dict values via `str(v)` -- so changing from list to prose string
is safe without touching the scan script.

---

## Files for Reference

- Current data: `backend/crystal_data.py`
- Scan script: `tests/echo_pace_cry_scan.py`
- Prior commission: `Codex_Deliveries/Crystal_Healing/CODEX_COMMISSION_CRYSTAL_HEALING.md`
- Module tracker: `Codex_Deliveries/Crystal_Healing/TRACKER.md`
