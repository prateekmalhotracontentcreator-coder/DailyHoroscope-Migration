---
title: CODEX Commission -- Faith Rewrite 2
version: v1.0
date: 2026-06-12
status: READY TO ISSUE
baseline: main at 86e53af
delivery_branch: codex/faith/rewrite-2
issued_by: Temple Team / CC
---

# CODEX Commission -- Faith Rewrite 2

## Context: What Pass 5 Fixed (Do Not Redo)

Pass 5 (CC direct edits, 2026-06-07, commit `86e53af`) cleared L2 across all four Faith types. This is the authoritative baseline.

| Type | L1 (Pass 5) | L2 (Pass 5) | L3 (Pass 5) |
|---|---|---|---|
| GITA | 91.25% ❌ | PASS ✅ | 81.82% ❌ |
| BIBLE | 78.35% ❌ | PASS ✅ | 50.00% ✅ |
| TRANSIT | 84.60% ❌ | PASS ✅ | 66.67% ❌ |
| DAILY | AI seeder path | PASS ✅ | PASS ✅ |

**DAILY is out of scope for this commission.** It is handled by the AI seeder (`scripts/seed_faith_daily_haiku.py` Phase 1, already written).

**L2 is out of scope.** It is PASS. Do not touch FAQ modulus, faq_seed, or any variation-count parameters.

---

## Strategy (Temple Team directive, 2026-06-12)

Three-part strategy for the remaining L1/L3 failures:

1. **Mix AI-seeded unique content + generator redesign** -- replace situation/transition-level constant phrases with verse-specific vocabulary tokens; extend the AI seeder (already in place for DAILY) to Transit pages.
2. **Timing SEO upload strategy** -- produce non-similar page batches; Google indexes each batch before the next batch uploads (minimum one week between batches).
3. **Expand verse range** -- Bible verse pool is critically thin. Root cause confirmed by live scan (2026-06-12): only 174 unique Bible verses serve all 6,000 Bible pages; the `salvation` source bucket has exactly 12 unique verses. Expand to ≥ 30 unique verses per source bucket.

---

## Root Cause: BIBLE Verse Pool Exhaustion

Live scan confirmed: 174 unique Bible verses across 6,000 pages. Average: 34.5 pages share each verse. Worst case: `Heb. 6:12` appears on **163 pages**.

| Source bucket | Unique verses (current) | Target |
|---|---|---|
| salvation | 12 | ≥ 30 |
| hope | 21 | ≥ 30 |
| faith | 23 | ≥ 30 |
| suffering | 29 | ≥ 30 |
| forgiveness | 41 | ≥ 50 |
| guidance | 43 | ≥ 50 |
| financial-need | 43 | ≥ 50 |
| peace | 44 | ≥ 50 |
| marriage | 45 | ≥ 50 |
| joy | 46 | ≥ 50 |
| fear | 53 | ≥ 60 |
| worry | 60 | ≥ 60 |

When 163 pages share the same verse text, TF-IDF cosine similarity between those pages is structurally high regardless of topic variation. Expanding the verse pool is the single highest-leverage fix for Bible L1.

---

## Root Cause: GITA Situation-Constant Ceiling

10,500 pages: 700 unique verses × 15 situations. Within each situation cluster (~700 pages), all pages share identical `situation['hidden_fear']` and `situation['practice_shift']` text verbatim in `_gita_hook()`, and `situation['action_focus']` verbatim in all 8 variants of `_gita_application()`. These ~150 shared tokens at IDF 1.5 overwhelm the 3 verse-unique tokens at IDF 2.0. This structural ceiling cannot be resolved by modulus expansion alone -- it requires replacing full-phrase situation fills with single-token vocabulary.

---

## Root Cause: TRANSIT Planet-Core Shared Across 12 Signs

`TRANSIT_FAMILIES` assigns identical `core`, `watch_for`, and `practice` text to all 12 sign pages for each planet. Mercury-in-Aries and Mercury-in-Pisces share 100% of planet body vocabulary → near-identical TF-IDF vectors. Fix: add sign-element and sign-modality vocabulary layers to differentiate pages within a planet cluster.

---

## Problem 1 -- BIBLE: Expand Verse Pool

**File:** `backend/assets/faith/` -- the Bible verse JSON asset(s) that back `_select_bible_verse()`

### What to do

1. Locate the Bible verse source JSON. It is keyed by source bucket (salvation, hope, faith, etc.).
2. For each bucket at < 30 unique verses, add verses until you reach the target (see table above).
3. Each added verse must be:
   - Short: ≤ 260 characters of verse text
   - Thematically matched to the source bucket
   - A distinct book+chapter+verse reference not already present in the pool
   - English (NIV, ESV, or KJV -- match the format already in use)
4. After adding, verify: run `_select_bible_verse()` across all 6,000 topic-transition combinations and confirm the verse sharing is within target.

### Acceptance check (run this before submitting PR)

```python
import sys; sys.path.insert(0, 'backend')
from collections import Counter
from faith_bible_data import BIBLE_TOPICS, TRANSITIONS, _select_bible_verse

verse_count = Counter()
for topic in BIBLE_TOPICS:
    for trans in TRANSITIONS:
        v = _select_bible_verse(topic['slug'], trans['slug'])
        verse_count[v['reference']] += 1

print(f"Unique verses: {len(verse_count)}")
print(f"Max sharing: {verse_count.most_common(1)}")
assert max(verse_count.values()) <= 30, f"Verse still over-shared: {verse_count.most_common(3)}"
assert len(verse_count) >= 300, f"Need more unique verses: only {len(verse_count)}"
```

---

## Problem 2 -- BIBLE: Generator Fix -- `symbolic_clause`

**File:** `backend/faith_bible_data.py`, function `_bible_hermeneutical()` (~line 1358)

### Root cause

`symbolic_clause` is computed once outside the options list and reused in ALL 8 options. The phrase `"here becomes a cue for"` therefore appears in every Bible page → L2 flag AND structural similarity.

### Fix

Move `symbolic_clause` inside the options list and give each option a distinct phrasing. Use the existing `seed` (already computed by `_hash_index`) to select which option is built -- but each option must use a different structural form of the same semantic idea.

```python
# Currently (BAD):
symbolic_clause = f"{sym_label} here becomes a cue for {faith_token} while {transition['label'].lower()} is active"
options = [
    f"...text... {symbolic_clause}...",
    f"...text... {symbolic_clause}...",  # same phrase repeated
    ...
]

# Fix (GOOD): define 8 distinct forms, use one per option
symbolic_forms = [
    f"{sym_label} here becomes a cue for {faith_token} while {transition['label'].lower()} is active",
    f"when {transition['label'].lower()} is present, {sym_label} begins signalling the need for {faith_token}",
    f"{sym_label} marks the threshold where {faith_token} is most required in {transition['label'].lower()}",
    f"in this transition, {sym_label} acts as a compass pointing toward {faith_token}",
    f"the {sym_label} quality of this verse is precisely what {transition['label'].lower()} is asking for",
    f"{faith_token} is the pastoral response that {sym_label} is pointing at during {transition['label'].lower()}",
    f"when {sym_label} rises in {transition['label'].lower()}, the need is specifically {faith_token}",
    f"{transition['label']} calls for {faith_token}; {sym_label} is how this verse names that need",
]
# Then each option[i] uses symbolic_forms[i]
options = [
    f"...option 0 text... {symbolic_forms[0]}...",
    f"...option 1 text... {symbolic_forms[1]}...",
    # etc -- one form per option, no sharing
]
```

---

## Problem 3 -- GITA: Replace Situation Constants with Verse-Anchored Tokens

**File:** `backend/faith_gita_data.py`

### Fix A -- `_gita_hook()` (~line 518)

Currently 6 of 8 variants use `situation['hidden_fear'].lower()` (full phrase, ~8 words) verbatim. Replace full-phrase fills with `_situation_vocabulary(situation, limit=1)` -- a single high-frequency token from the situation, not the full phrase. The function `_situation_vocabulary()` already exists; check its signature.

```python
# Currently (BAD):
f"...when {situation['hidden_fear'].lower()} takes hold..."

# Fix (GOOD):
f"...when {_situation_vocabulary(situation, limit=1)} takes hold..."
```

Apply this replacement in every hook variant that uses the full `hidden_fear` or `practice_shift` phrase.

### Fix B -- `_gita_application()` (~line 539)

Currently uses `situation['action_focus']` (~6 words) verbatim in ALL 8 variants. Same fix: replace with `_situation_vocabulary(situation, limit=1)`.

### Fix C -- `_how_to_apply_steps()` (~line 570)

This function returns a fixed 3-item list. Rewrite with 4 variant sets selected by `_gita_seed(modulus=4)`:

```python
def _how_to_apply_steps(verse: dict, situation: dict) -> list[str]:
    verse_focus = _verse_focus_fragment(verse)
    seed = _gita_seed(verse["chapter"], verse["verse"], situation["slug"], modulus=4)
    step_sets = [
        [
            f"Name the exact place where {situation['label'].lower()} is pushing you away from {situation['practice_shift']}.",
            f"Read {verse['reference']} once slowly and ask how '{verse_focus}' changes the next action in front of you.",
            f"Take one step that matches {situation['action_focus']} before demanding that the situation feel resolved.",
        ],
        [
            f"Write down where {situation['label'].lower()} is consuming the most energy right now.",
            f"Let '{verse_focus}' from {verse['reference']} reframe the single most immediate task before you.",
            f"Choose one act aligned with {situation['action_focus']} without waiting for the difficulty to pass first.",
        ],
        [
            f"Identify the specific resistance {situation['label'].lower()} is producing -- not the general pattern.",
            f"Read {verse['reference']} with the question: what does '{verse_focus}' look like as behavior today?",
            f"Before closing the day, act once on {situation['action_focus']} rather than on the impulse to resolve everything.",
        ],
        [
            f"Locate the one point where {situation['label'].lower()} is narrowing choice most sharply.",
            f"Allow '{verse_focus}' in {verse['reference']} to define the smallest complete next step available.",
            f"Carry {situation['action_focus']} into one concrete act before expecting the tension to change.",
        ],
    ]
    return step_sets[seed]
```

### Fix D -- L3 sentence-opening variation in `_gita_application()`

The 8 variants of `_gita_application()` currently start with similar grammatical patterns. Restructure so:
- Variants 0-3 open with a **subject clause** (e.g., `"The practice here is..."`, `"This verse offers..."`)
- Variants 4-7 open with an **action clause** (e.g., `"Start with..."`, `"Bring this verse to..."`)

This reduces L3 structural similarity between pages that land on different variants.

---

## Problem 4 -- TRANSIT: Sign-Specific Vocabulary

**File:** `backend/faith_seo_data.py`

### What to build

Add a `_sign_modifier(sign_slug: str) -> dict` function that returns element and modality vocabulary for a given sign:

```python
SIGN_ELEMENT_VOCAB = {
    "aries": {"element": "fire", "tokens": ["impulse", "ignition", "declaration", "forward motion"]},
    "taurus": {"element": "earth", "tokens": ["grounding", "material", "patience", "steadiness"]},
    "gemini": {"element": "air", "tokens": ["exchange", "thought", "perspective", "connection"]},
    "cancer": {"element": "water", "tokens": ["feeling", "memory", "depth", "protection"]},
    "leo": {"element": "fire", "tokens": ["visibility", "courage", "creative force", "identity"]},
    "virgo": {"element": "earth", "tokens": ["refinement", "discernment", "service", "precision"]},
    "libra": {"element": "air", "tokens": ["balance", "relatedness", "fairness", "deliberation"]},
    "scorpio": {"element": "water", "tokens": ["depth", "transformation", "intensity", "truth"]},
    "sagittarius": {"element": "fire", "tokens": ["expansion", "vision", "meaning", "direction"]},
    "capricorn": {"element": "earth", "tokens": ["structure", "accountability", "time", "authority"]},
    "aquarius": {"element": "air", "tokens": ["innovation", "detachment", "collective", "clarity"]},
    "pisces": {"element": "water", "tokens": ["dissolution", "compassion", "surrender", "flow"]},
}
```

### Where to use it

In `_transit_summary()`, `_transit_energy()`, and `_transit_application()` (all use `modulus=12`): within each option template, add 1 sentence that references the sign-element vocabulary when `sign_slug` is not None.

For `TRANSIT_SPECIALS` (retrograde/eclipse events, `sign_slug = None`): skip sign modifier -- use planet vocabulary only.

The existing `modulus=12` already produces 12 distinct template variants per transit event. The sign modifier injects sign-specific tokens on top of the variant -- it does not replace the variant logic.

### L3 fix for TRANSIT

In `_transit_application()`: vary sentence-opening structure across the 12 modulus variants:
- Variants 0-5: subject-clause opening
- Variants 6-11: action-clause opening

---

## Problem 5 -- AI Seeder: Phase 2 (Transit, 156 pages)

**File:** `backend/scripts/seed_faith_daily_haiku.py`

The seeder already handles Phase 1 (DAILY, 144 pages). Add Phase 2 to seed `faith_transit_pages`.

### Architecture (follow existing DAILY pattern exactly)

The transit router must follow the same merge pattern as daily:
```python
base = get_transit_page(transit_slug, tradition)    # generator output
stored = faith_transit_pages.find_one(...)          # seeder writes here
return _merge(base, stored)                          # stored fields WIN
```

Confirm this merge pattern is already wired in `faith_seo_router.py` for transit. If not, add it.

### Fields to seed

For each of 78 transit events × 2 traditions (gita/bible) = 156 documents:
- `summary` -- unique 2-sentence summary per transit-tradition
- `application` -- unique 1-sentence application per transit-tradition

### Prompt template

```python
TRANSIT_SEED_PROMPT = """
You are writing content for a {tradition_label}-tradition SEO page about {transit_label}.
Planet: {planet_name}. Sign: {sign_name_or_none}. Core theme: {transit_core}. Watch for: {transit_watch_for}.

Write:
1. summary: 2 sentences (50-70 words). Must mention the specific planet and {sign_name_or_element} vocabulary. Reference how this transit affects practical life from a {tradition_label} perspective.
2. application: 1 sentence (20-30 words). An actionable practice that is specific to this transit. Do not use the word "practice" as the first word.

Output as JSON: {{"summary": "...", "application": "..."}}
""".strip()
```

### Cost estimate
156 documents × 2 fields × ~350 tokens average = ~$0.05 at Haiku rates. Add `--type transit` flag to the existing CLI.

---

## Problem 6 -- Batch Upload Planner

**New file:** `backend/scripts/generate_upload_batches.py`

### Purpose
Generate batched upload lists where within-batch pages have low structural similarity. Output is JSON consumed by whoever manages the SEO upload schedule.

### Batching rules

**GITA batches:**
- Rule: no two pages in the same batch share the same `situation_slug`
- Method: iterate over all 700 verses. For each pass, pick one verse per situation → 15 pages per "cross-situation sweep" batch
- Total batches: 700 (one per verse, each containing 15 pages from different situations)
- Within-batch similarity is low because each page uses a different situation's vocabulary
- Upload cadence suggestion: 1 verse-sweep batch per week = 700 weeks to seed all Gita pages. For faster upload: bundle 10 verse-sweeps per week = 150 pages per week, 70 weeks total.

**BIBLE batches:**
- Rule: no two pages in the same batch share the same `source_slug` (topic bucket)
- Method: for each transition, pick one topic from each of 12 source buckets → 12 pages per batch
- Total batches: 50 (one per transition, each containing 12 cross-bucket pages)
- Within-batch similarity is low because each page draws from a different source bucket

**TRANSIT batches:**
- Rule: batch by planet family
- Method: one batch per planet = 12 sign pages × 2 traditions = 24 pages per batch (6 planet batches)
- Special events batch: 6 retrograde/eclipse specials × 2 traditions = 12 pages (1 batch)
- Total: 7 transit batches

### Output

```json
{
    "generated": "YYYY-MM-DD",
    "page_type": "gita|bible|transit",
    "total_pages": 10500,
    "batch_count": 700,
    "recommended_weekly_upload": 10,
    "batches": [
        {
            "batch_id": 1,
            "similarity_group": "ch1-sweep",
            "pages": [
                "/faith/gita/1-1/grief-and-loss",
                "/faith/gita/1-2/career-direction",
                ...
            ]
        }
    ]
}
```

---

## Acceptance Criteria

Run `tests/echo_pace_faith_scan.py` from `main` after all changes. Required results:

| Type | L1 target | L3 target | L2 (must not regress) |
|---|---|---|---|
| GITA | < 85% worst pair | < 65% | PASS |
| BIBLE | < 72% worst pair | PASS (already) | PASS |
| TRANSIT | < 78% worst pair | < 62% | PASS |

**Verse pool gate:**
```python
assert max(verse_count.values()) <= 30  # no verse shared by more than 30 pages
assert len(verse_count) >= 300          # at least 300 unique Bible verses in use
```

**Batch planner gate:** output JSON valid; each GITA batch contains pages from ≥ 10 distinct situation slugs; each BIBLE batch contains pages from ≥ 8 distinct source buckets.

---

## Files Changed

| File | Change type |
|---|---|
| `backend/assets/faith/` (Bible verse JSON) | Expand verse pool: ≥ 30 unique verses per source bucket |
| `backend/faith_bible_data.py` | `symbolic_clause` → 8 `symbolic_forms` in `_bible_hermeneutical()` |
| `backend/faith_gita_data.py` | Replace situation-constant full phrases with single tokens in `_gita_hook()` + `_gita_application()`; 4-variant `_how_to_apply_steps()`; L3 sentence-opening variation |
| `backend/faith_seo_data.py` | `_sign_modifier()` function; inject sign vocabulary into transit body functions; L3 sentence-opening variation |
| `backend/scripts/seed_faith_daily_haiku.py` | Add Phase 2: Transit seeding (156 pages), `--type transit` CLI flag |
| `backend/scripts/generate_upload_batches.py` | NEW -- batch upload planner for GITA, BIBLE, TRANSIT |

---

## Do NOT Change

- L2 code of any kind
- DAILY generator or DAILY seeder (Phase 1)
- `_gita_summary()` -- 8 variants, already correct
- `_bible_summary()`, `_bible_emotional_frame()` -- already correct
- FAQ modulus values (faq_seed, bible_faq, transit_faq) -- L2 PASS, do not touch
- Any routing, API endpoints, or database schema
- `GITA_SITUATIONS` data entries -- add new situations only if explicitly directed in a follow-up commission

---

## Delivery Branch

`codex/faith/rewrite-2` -- branch from `main` at `86e53af`. Do not use `codex/everyday-horoscope/zibu-symbols` or any prior staging worktree as a baseline.

---

*CODEX_COMMISSION_FAITH_REWRITE_2 · DailyHoroscope-Migration · v1.0 · 2026-06-12*
