# M3-FIX-1 Commission Brief -- Festival-Region Summary Fix (Template Repetition)
> Thread: SEO M3 Codex Thread
> Commission ID: M3-FIX-1
> Date: 2026-05-26
> Status: READY TO ISSUE
> Prerequisite: SEO-M3 Module delivered ✅

---

## Context -- Why This Brief Exists

The SEO M3 module delivered `backend/seo_m3_builders.py`, which generates 480
festival-region pages via `build_festival_region_doc(festival_slug, region_slug)`.

A content audit found one critical problem that must be fixed before re-seeding:

**No router, frontend, or wiring changes are needed. This brief touches ONE file only:**
`backend/seo_m3_builders.py`

---

## Problem -- Festival `summary` Field: Identical Across All 480 Pages 🔴

Every one of the 480 festival-region pages shares the same closing sentence in its
`summary` field. Only the festival name and region name at the very start differ.

**Current code (inside `build_festival_region_doc()`):**
```python
"summary": (
    f"{festival_name} in {region_name} brings together local ritual timing, family tradition, and community celebration. "
    f"This page focuses on date, customs, food, and how the region typically gives the festival its own voice."
),
```

**Result -- all 480 pages read like this:**
- "Diwali in Andhra Pradesh brings together local ritual timing, family tradition, and community celebration. This page focuses on date, customs, food, and how the region typically gives the festival its own voice."
- "Holi in Tamil Nadu brings together local ritual timing, family tradition, and community celebration. This page focuses on date, customs, food, and how the region typically gives the festival its own voice."

The second sentence is **word-for-word identical across all 480 pages**. Google Helpful
Content treats 480 pages with the same paragraph as thin, duplicate content.

---

## The Fix -- Generator-Level Rewrite

The fix must happen inside `build_festival_region_doc()`. Do NOT try to patch
individual records -- the data is built dynamically every call.

### What metadata is available

`FESTIVAL_META[festival_slug]` has these fields for each of the 16 festivals:
- `name` -- display name (e.g. "Diwali")
- `season` -- cultural theme phrase (e.g. "light, prosperity, and renewal")

`REGION_META[region_slug]` has these fields for each of the 30 regions:
- `name` -- display name (e.g. "Andhra Pradesh")
- `zone` -- geographic zone: "south", "north", "east", "west", "northeast", "central"
- `food` -- region-specific festive food (e.g. "pulihora and laddus")
- `marker` -- region's celebration marker (e.g. "temple processions and decorated entrances")

### Summary composition rule

The `summary` must be 2-3 sentences. Each sentence must draw from BOTH the festival's
`season` theme AND the region's unique `zone`/`food`/`marker` combination so that no
two summaries end with the same sentence.

### Approach

Build a helper function `_festival_summary(festival_slug, region_slug)` that composes
the summary using the available metadata fields. Use zone-specific phrasing and
festival-season-specific framing so the combination is always distinct.

**Examples of acceptable output (same meaning, different expression):**

> "Diwali in Andhra Pradesh centres on light, prosperity, and renewal, expressed through
> the region's distinctive temple processions and decorated entrances. Families gather
> around pulihora and laddus, and the celebration carries the warm, community-led rhythm
> that defines south-region observance."

> "Holi in Punjab takes its colour, play, and spring release energy and channels it
> through the north's open community style -- large gatherings, bhangra rhythms, and tables
> laid with makki and sarson. The festival here is loud, physical, and unapologetically social."

> "Pongal in Tamil Nadu is rooted in harvest thanks and gratitude, expressed through the
> south's distinctive Thai Pongal puja, the cooking of fresh rice in new clay pots, and a
> day-long rhythm that starts before sunrise and ends with family and community feasts."

**Minimum requirements:**
- No two `summary` values should end with the same sentence
- Each summary must reference something specific to the festival's `season` theme
- Each summary must reference something specific to the region's `food` or `marker`
- Length: 2-3 sentences, 40-80 words

---

## Deliverable -- Updated `seo_m3_builders.py`

Deliver the **complete updated** `backend/seo_m3_builders.py`.

**Only change:**
- Add `_festival_summary(festival_slug, region_slug)` helper function
- Update `build_festival_region_doc()` to call `_festival_summary()` for the `summary` field
- Do NOT change any other function, constant, or logic in the file

**Do NOT change:**
- `build_transit_profile_doc()` -- already correct
- `build_character_placement_doc()` -- already correct
- All helper functions for transit and character placement
- `TRANSIT_HOOK_TEMPLATES` constant
- Function signatures and return types

---

## Verify Before Delivering

```bash
python3 -c "
import sys; sys.path.insert(0, 'backend')
from seo_m3_builders import build_festival_region_doc
from seo_m3_catalog import FESTIVAL_SLUGS, REGION_SLUGS

docs = [
    build_festival_region_doc(f, r)
    for f in FESTIVAL_SLUGS
    for r in REGION_SLUGS
]
summaries = [d['summary'] for d in docs]
endings = set(s[-80:] for s in summaries)
print(f'Total docs: {len(docs)}')
print(f'Unique summary endings (last 80 chars): {len(endings)}')
assert len(docs) == 480, f'Expected 480, got {len(docs)}'
assert len(endings) >= 60, f'Not enough unique endings: {len(endings)}'
print('All checks passed.')
"
python3 -m py_compile backend/seo_m3_builders.py && echo "Compile OK"
```

---

## Acceptance Checklist

- [ ] `summary` field: no two records end with the same sentence (across all 480)
- [ ] Each summary references the festival's `season` theme
- [ ] Each summary references the region's `food` or `marker`
- [ ] Length: 2-3 sentences per summary
- [ ] `python3 -m py_compile backend/seo_m3_builders.py` passes
- [ ] Total docs = 480 (16 festivals × 30 regions)
- [ ] `build_transit_profile_doc()` unchanged
- [ ] `build_character_placement_doc()` unchanged
- [ ] No other files changed
