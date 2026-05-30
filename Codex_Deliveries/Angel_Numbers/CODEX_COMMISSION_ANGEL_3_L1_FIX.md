# ANGEL-3 Commission Brief -- Angel Numbers L1 TF-IDF Fix
> Thread: Angel Numbers Codex Thread (same thread as ANGEL-1 and ANGEL-2)
> Commission ID: ANGEL-3
> Date: 2026-05-31
> Status: READY TO ISSUE
> Prerequisite: ANGEL-2 delivered ✅

---

## Pass / Fail Verdict on ANGEL-2

**ANGEL-2 does NOT clear Temple Team test criteria.**

The ANGEL-2 commission acceptance checklist (addendum, §Additional Requirement 2) states:

> Layer 1 PASS: all clusters < 40% TF-IDF cosine

ANGEL-2 delivery result:

| Cluster | Score | Gate (< 40%) |
|---|---|---|
| protection | 57.5% | ❌ FAIL |
| manifestation | 55.2% | ❌ FAIL |
| career | 53.0% | ❌ FAIL |
| spiritual-growth | 51.9% | ❌ FAIL |
| new-beginnings | 49.5% | ❌ FAIL |
| twin-flame | 47.8% | ❌ FAIL |
| health | 47.0% | ❌ FAIL |
| core | 47.0% | ❌ FAIL |
| love | 46.1% | ❌ FAIL |
| family | 45.8% | ❌ FAIL |

L2 and L3 now pass cleanly. L1 is the sole remaining blocker.
The verifier script says OVERALL PASS (it treats ≥70% as the hard block). The acceptance checklist sets a tighter standard: < 40%. All 10 clusters fail the checklist gate. Module seeding and deploy are blocked until L1 clears.

---

## Root Cause Analysis

ANGEL-2 fixed template-level sentence repetition (L2) and key_theme collision (L3). The L1 TF-IDF problem is different: it is a **vocabulary pool exhaustion problem**, not a phrase repetition problem. TF-IDF measures the distribution of all weighted terms across a document. When two records share the same pool fragments -- even if no single phrase repeats verbatim -- the TF-IDF cosine stays high because the vocabulary proportions look nearly identical.

**There are 4 specific pools that are too small:**

### Problem 1 -- ROOT_VIBRATION_FRAGMENTS: 2 variants per root digit

```python
ROOT_VIBRATION_FRAGMENTS = {
    1: [
        "It strengthens decisive self-trust and clears space for an honest beginning.",
        "It sharpens your inner yes so hesitation stops dressing up as caution.",
    ],
    2: [...],  # 2 items each
    ...
}
```

There are 9 root digits. Each digit has **exactly 2 fragment variants**. Approximately 111 numbers share each root digit (1,000 ÷ 9). With 2 variants, ~55 records share the same fragment. This produces high L1 similarity in the `vibration` field across any two records with the same root.

**Fix:** Expand to **minimum 10 distinct variants per root digit** (90 total fragments). Each should use different vocabulary -- not just reordering the same ideas.

---

### Problem 2 -- ROOT_SEEING_FRAGMENTS: 2 variants per root digit

```python
ROOT_SEEING_FRAGMENTS = {
    1: [
        "Treat the sighting as permission to stop waiting for perfect certainty.",
        "Let the repetition remind you that a clean beginning is already available.",
    ],
    ...
}
```

Same structural problem as above. ~55 numbers share each fragment in the `seeing_it_means` field.

**Fix:** Expand to **minimum 10 distinct variants per root digit** (90 total fragments).

---

### Problem 3 -- PATTERN_VIBRATION_FRAGMENTS and PATTERN_SEEING_FRAGMENTS: 2 variants per pattern type

```python
PATTERN_VIBRATION_FRAGMENTS = {
    "pure amplification": [
        "The amplified echo keeps pressing the exact same note until your response matches it.",
        "Because the digits repeat without dilution, the number does not support half-hearted participation.",
    ],
    ...  # 2 items per pattern type, 6 pattern types
}
```

There are 6 pattern types. Numbers are assigned a pattern type based on their digit structure. With 2 variants per pattern, and 100-200+ numbers per common pattern type, many records share identical pattern fragments in both `vibration` and `seeing_it_means`.

**Fix:** Expand to **minimum 8 distinct variants per pattern type** (48 total per table). Use clearly different vocabulary angles -- not rewording the same core sentence.

---

### Problem 4 -- INTENT_STYLES closings: 2 variants per intent

```python
INTENT_STYLES = {
    "love": {
        "focus": "...",  # fixed -- same for ALL 1,000 love records
        "challenge": "...",  # fixed -- same for ALL 1,000 love records
        "closing": [
            "Let the heart move with honesty, because...",
            "Use the number as permission to choose reciprocity...",
        ],
    },
    ...
}
```

This is the biggest driver of `protection` and `manifestation` failures. The `focus` and `challenge` strings are **completely fixed per intent** -- every one of 1,000 records for the same intent uses the identical `focus` and `challenge` values regardless of which template picks them up. Even if the intro/bridge/challenge templates rotate, the substituted values are identical across all 1,000 records in each cluster.

Additionally, only 2 closing variants per intent means ~500 records share the same closing sentence.

**Fix:** Two changes required:

**4a.** Expand intent `closing` pools from 2 → **minimum 12 distinct variants per intent** (108 total). Use different vocabulary angles, lengths, and structural rhythms.

**4b.** Break `focus` and `challenge` into **number-family-aware sub-pools** keyed by root digit. Instead of one fixed string, provide 9 variants -- one per root digit -- so that the love/protection/etc. message feels genuinely different for root-1 numbers vs root-5 numbers. Structure:

```python
"love": {
    "focus_by_root": {
        1: "...love framing for root-1 energy (initiative, new-love courage, self-declared affection)...",
        2: "...love framing for root-2 energy (partnership, patience, emotional balance)...",
        3: "...love framing for root-3 energy (communication, playfulness, expressive honesty)...",
        4: "...love framing for root-4 energy (committed structure, steadiness, reliable devotion)...",
        5: "...love framing for root-5 energy (freedom-aware love, space-giving, adaptive connection)...",
        6: "...love framing for root-6 energy (nurturing, harmony, responsible care)...",
        7: "...love framing for root-7 energy (soul depth, spiritual chemistry, inner knowing)...",
        8: "...love framing for root-8 energy (lasting commitment, value alignment, material security)...",
        9: "...love framing for root-9 energy (karmic love, compassion, completing old patterns)...",
    },
    "challenge_by_root": {
        1: "...", 2: "...", 3: "...", 4: "...", 5: "...",
        6: "...", 7: "...", 8: "...", 9: "...",
    },
    "closing": [  # minimum 12 variants
        "...", "...", "...", ...
    ],
}
```

The generator already uses `root_digit` to seed all lookups -- it just needs these pools to exist.

---

## VIBRATION_CADENCE: Expand from 4 → 20 variants

```python
VIBRATION_CADENCE = [
    "That is why this sequence tends to arrive right before a meaningful choice, not after one.",
    "That is what makes the number feel active rather than merely symbolic.",
    "That is where the sequence becomes guidance instead of decoration.",
    "That is why the message usually clarifies once you respond in a concrete way.",
]
```

4 variants across 1,000 records = 250 records sharing each cadence sentence. This contributes to L1 overlap across all clusters. Expand to **minimum 20 distinct closings** using varied vocabulary and rhythms -- not variations on the same "That is..." construction.

---

## Summary of Changes Required

| Item | Current Pool Size | Required Pool Size | Field Affected |
|---|---|---|---|
| `ROOT_VIBRATION_FRAGMENTS` | 2 per root digit | **10 per root digit** | `vibration` |
| `ROOT_SEEING_FRAGMENTS` | 2 per root digit | **10 per root digit** | `seeing_it_means` |
| `PATTERN_VIBRATION_FRAGMENTS` | 2 per pattern type | **8 per pattern type** | `vibration` |
| `PATTERN_SEEING_FRAGMENTS` | 2 per pattern type | **8 per pattern type** | `seeing_it_means` |
| `INTENT_STYLES.focus` | 1 fixed string per intent | **9 root-keyed variants per intent** | intent `message` |
| `INTENT_STYLES.challenge` | 1 fixed string per intent | **9 root-keyed variants per intent** | intent `message` |
| `INTENT_STYLES.closing` | 2 per intent | **12 per intent** | intent `message` |
| `VIBRATION_CADENCE` | 4 total | **20 total** | `vibration` |

---

## What Must NOT Change

- All function signatures: `iter_core_records()`, `iter_intent_records()`, `get_core_numbers()`, `build_sitemap_paths()`, `sitemap_page_count()`
- Total record counts: 1,000 core + 9,000 intent
- `INTENT_ORDER`, `INTENT_CONFIG`, `PAGE_SIZE`, `SITE_URL`
- All structural fields on every record (number, display, headline, slug, canonical_url, meta_title, meta_description, key_themes, related_numbers, faq, intent, display_name, all_intents, how_to_manifest)
- `BASE_ARCHETYPES`, `PATTERN_DETAILS`, `DIGIT_LEXICON`, `SPECIAL_NUMBER_OVERRIDES`
- Any logic in `choose_variant()`, `get_pattern_type()`, `digit_sum()`, `root_digit()`
- No other file is to be touched -- only `backend/angel_numbers_data.py`

---

## Verification Gate (run before delivering)

```bash
PYTHONPATH=backend python3 backend/scripts/verify_angel_numbers_compliance.py
```

**Acceptance threshold:**

| Layer | Target | Hard block |
|---|---|---|
| L1 TF-IDF cosine | ALL clusters **< 40%** | ≥ 70% BLOCKED |
| L2 N-gram | No 4-gram in > 15% records | Current PASS -- must stay PASS |
| L3 Jaccard | < 75% across all pairs | Current PASS -- must stay PASS |

**All 3 layers must show PASS and every L1 cluster must be < 40%.** Paste the full output in your delivery confirmation. Delivery not accepted without it.

Also confirm:
```bash
python3 -c "
import sys; sys.path.insert(0, 'backend')
from angel_numbers_data import iter_core_records, iter_intent_records
core = list(iter_core_records())
intents = list(iter_intent_records())
print('Core records:', len(core))
print('Intent records:', len(intents))
assert len(core) == 1000
assert len(intents) == 9000
print('how_to_manifest present:', sum(1 for r in intents if r.get('how_to_manifest')))
assert sum(1 for r in intents if r.get('how_to_manifest')) == 1000
print('All checks passed.')
"
```

---

## Deliverable

One updated file only: `backend/angel_numbers_data.py`

The 8 pool expansions above with all verification checks passing. Record counts unchanged.
