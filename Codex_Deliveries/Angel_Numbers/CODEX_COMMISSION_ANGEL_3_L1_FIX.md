# ANGEL-3 Commission Brief -- Angel Numbers L1 TF-IDF Fix (Third Pass)
> Thread: Angel Numbers Codex Thread (same thread as ANGEL-1 and ANGEL-2)
> Commission ID: ANGEL-3
> Date: 2026-05-31
> Status: READY TO ISSUE
> Prerequisite: ANGEL-2 delivered ✅
> TT Review: Temple Team sign-off doc 2026-05-31 -- see §TT Verdict below

---

## Message to Post in the Angel Numbers Codex Thread

> **ANGEL-2 rewrite: L2 and L3 cleared, L1 not yet at brief standard. Third pass required.**
>
> The brief requires all clusters < 40% L1 cosine. Current worst is 57.5% (protection), with 4 clusters FLAGGED ≥50% and 6 more above the 40% ceiling. The verifier's "PASS" is against its own internal thresholds, not the brief requirement.
>
> Root cause: number pages within each cluster share too much topic vocabulary. Rotating action families reduced L2 -- good. But L1 requires more digit-pattern specific language per number. Pages in the "career" cluster need to reference the numerological meaning of their specific number/pattern, not just career topics.
>
> **Target for next pass -- fix the 4 FLAGGED clusters specifically:**
> - protection (57.5%) -- most urgent
> - manifestation (55.2%)
> - spiritual-growth (51.9%)
> - career (53.0%)
>
> Approach: for each number in these clusters, ensure at least 2 sentences anchor to the digit pattern's specific energy (e.g. for 333 protection: the triple-3 triangle of mind/body/spirit as the protective force -- not generic "trust your guides"). The 6 "over target" clusters can be addressed in the same pass.
>
> Re-run verifier after changes. Target: all clusters < 40%. Do not submit until that ceiling is met.

---

## TT Verdict on ANGEL-2

| Gate | Requirement | Current | Decision |
|---|---|---|---|
| L1 all clusters | < 40% (brief) | All 10 fail, worst 57.5% | ❌ FAIL |
| L2 n-gram | < 15% records | 0 violations | ✅ PASS |
| L3 Jaccard | < 75% | 55.6% | ✅ PASS |

**Do not re-seed Mongo with ANGEL-2 generator. ANGEL-3 must pass all gates before seed.**

L2 and L3 are genuinely fixed. The rewrite direction is correct. L1 alone remains the blocker.

---

## TT Root Cause Diagnosis

Angel Numbers has a fundamentally different architecture from Tarot: 10 intent clusters × 1,000+ number pages. Pages within the same cluster (e.g. all 1,000 "career" pages) share the cluster's thematic vocabulary by design. That structural overlap is harder to reduce than page-to-page similarity.

The fix is not more action-family rotation -- it is making each number's body more **digit-pattern specific**, not just topic-specific.

- `111 career` should reference the amplification/alignment energy of three 1s
- `222 career` should reference patience and partnership timing
- `333 protection` should reference the triple-3 triangle of mind/body/spirit as the protective force -- not generic "trust your guides"

The content must anchor to the **number's numerological meaning**, not just the intent topic. Minimum: **2 sentences per number per intent that reference the specific digit pattern's energy**.

---

## Priority Clusters (address in order)

| Cluster | Score | Priority |
|---|---|---|
| protection | 57.5% | 🔴 1st |
| career | 53.0% | 🔴 2nd |
| spiritual-growth | 51.9% | 🔴 3rd |
| manifestation | 55.2% | 🔴 4th |
| new-beginnings | 49.5% | 🟠 5th |
| twin-flame | 47.8% | 🟠 6th |
| health | 47.0% | 🟠 7th |
| core | 47.0% | 🟠 8th |
| love | 46.1% | 🟠 9th |
| family | 45.8% | 🟠 10th |

All 10 must reach < 40% in the same pass.

---

## Technical Root Cause (Generator-Level)

ANGEL-2 fixed phrase repetition (L2) and key_theme collision (L3). The remaining L1 problem has two compounding causes:

### Cause 1 -- Vocabulary Pool Exhaustion

The following pools are too small. When many numbers share the same root digit or pattern type, they draw from a small fragment pool and end up with nearly identical weighted vocabulary:

| Pool | Current Size | Minimum Required |
|---|---|---|
| `ROOT_VIBRATION_FRAGMENTS` | 2 variants per root digit | 10 per root digit |
| `ROOT_SEEING_FRAGMENTS` | 2 variants per root digit | 10 per root digit |
| `PATTERN_VIBRATION_FRAGMENTS` | 2 variants per pattern type | 8 per pattern type |
| `PATTERN_SEEING_FRAGMENTS` | 2 variants per pattern type | 8 per pattern type |
| `VIBRATION_CADENCE` | 4 total | 20 total |

### Cause 2 -- Fixed Intent Focus/Challenge Strings (primary driver for FLAGGED clusters)

```python
INTENT_STYLES = {
    "love": {
        "focus": "...",      # FIXED -- identical across all 1,000 love records
        "challenge": "...",  # FIXED -- identical across all 1,000 love records
        "closing": [2 variants],
    },
    ...
}
```

Every one of 1,000 records in the same intent cluster uses the same `focus` and `challenge` vocabulary. This is the primary driver of FLAGGED scores in protection (57.5%) and manifestation (55.2%) -- the topic vocabulary dominates the TF-IDF fingerprint regardless of how the intro/bridge templates are rotated.

**Fix:** Replace fixed strings with root-digit-keyed variants. Structure required:

```python
INTENT_STYLES = {
    "protection": {
        "focus_by_root": {
            1: "...(protection as self-directed clarity, declaring boundaries from conviction)...",
            2: "...(protection as relational discernment, timing-aware safety)...",
            3: "...(protection as voice and truth-telling as the boundary)...",
            4: "...(protection as structural fortification, practical barriers)...",
            5: "...(protection as freedom-preserving movement, exit strategy)...",
            6: "...(protection as caring for the home atmosphere, sheltering what matters)...",
            7: "...(protection as spiritual discernment, inner knowing as the shield)...",
            8: "...(protection as stewardship, guarding value and authority)...",
            9: "...(protection as completion and release, closing what drains)...",
        },
        "challenge_by_root": {
            1: "...", 2: "...", 3: "...", 4: "...", 5: "...",
            6: "...", 7: "...", 8: "...", 9: "...",
        },
        "closing": [  # minimum 12 variants (current: 2)
            "...", "...", "...", ...
        ],
    },
    # same structure for all 9 intents
}
```

The generator already uses `root_digit` for seeding -- it just needs these pools to exist.

### Cause 3 -- Intent Closing Pools Too Small

`INTENT_STYLES.closing`: 2 variants per intent. ~500 records per intent share the same closing sentence. Expand to **minimum 12 variants per intent** (108 total).

---

## The Digit-Pattern Anchoring Requirement (TT Directive)

For every number × intent combination, the generated `message` field must contain **at least 2 sentences that reference the specific digit pattern's energy** -- not just the intent's topic.

**Examples of what this means in practice:**

| Number | Intent | Required anchor (2+ sentences) |
|---|---|---|
| 111 | career | Must reference: amplification of root-1 energy, alignment signal, the 3×1 amplified initiation -- not generic "take action" career advice |
| 222 | career | Must reference: root-2 partnership timing, patience-as-strategy, the mirrored balance of 2s -- not generic "opportunities incoming" |
| 333 | protection | Must reference: triple-3 triangle (mind/body/spirit as the protective force), creative expression as the protective layer -- not generic "trust your guides" |
| 444 | protection | Must reference: four-pillar structure, the 4×4 guardian wall, practical barriers -- not generic "angels are with you" |
| 555 | spiritual-growth | Must reference: 5-energy catalyst, conscious change over restless escape, the transformation doorway -- not generic "awakening is happening" |
| 888 | manifestation | Must reference: 8-energy karmic return, stewardship of what arrives, abundance as earned result -- not generic "align your thoughts" |

The digit-pattern anchor sentences can come from the `PATTERN_LANGUAGE`, `BASE_ARCHETYPES`, `DIGIT_LEXICON`, or `PATTERN_DETAILS` structures already in the generator. The fix is ensuring these structures are actually injected into the `message` field with enough specificity per number -- not just used for the `vibration` and `seeing_it_means` fields.

---

## What Must NOT Change

- All function signatures: `iter_core_records()`, `iter_intent_records()`, `get_core_numbers()`, `build_sitemap_paths()`, `sitemap_page_count()`
- Total record counts: 1,000 core + 9,000 intent
- `INTENT_ORDER`, `INTENT_CONFIG`, `PAGE_SIZE`, `SITE_URL`
- All structural fields on every record
- `BASE_ARCHETYPES`, `PATTERN_DETAILS`, `DIGIT_LEXICON`, `SPECIAL_NUMBER_OVERRIDES`, `PATTERN_LANGUAGE`
- `how_to_manifest` field must remain present on all 1,000 manifestation records with 7 action families and max 30% per type
- No other file is to be touched -- only `backend/angel_numbers_data.py`

---

## Verification Gate

```bash
PYTHONPATH=backend python3 backend/scripts/verify_angel_numbers_compliance.py
```

**All clusters must show < 40%. No exceptions.** Paste full output in delivery confirmation.

| Layer | Gate | Note |
|---|---|---|
| L1 TF-IDF | ALL clusters < 40% | Hard requirement per brief |
| L2 N-gram | No 4-gram in > 15% records | Currently PASS -- must stay PASS |
| L3 Jaccard | < 75% | Currently PASS -- must stay PASS |

Also confirm record counts and `how_to_manifest`:

```bash
python3 -c "
import sys; sys.path.insert(0, 'backend')
from angel_numbers_data import iter_core_records, iter_intent_records
core = list(iter_core_records())
intents = list(iter_intent_records())
print('Core:', len(core))
print('Intent:', len(intents))
assert len(core) == 1000 and len(intents) == 9000
manifest = sum(1 for r in intents if r.get('how_to_manifest'))
print('how_to_manifest present:', manifest)
assert manifest == 1000
print('All checks passed.')
"
```

---

## Deliverable

One updated file only: `backend/angel_numbers_data.py`

All 3 fix categories applied (pool expansion + root-digit-keyed focus/challenge + digit-pattern anchoring in message field). Record counts unchanged. All checks above passing.
