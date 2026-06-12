---
title: "[CC] Commission -- Crystal L2 Fix"
version: v1.1
date: 2026-06-12
status: ISSUED (corrected)
authored_by: CC (Claude Code / ECHO.PaceScanner)
github_issue: https://github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration/issues/3
target_file: backend/crystal_data.py
delivery_branch: codex/commission-cry-l2-fix
---

# [CC] Commission -- Crystal L2 Fix

> **v1.1 correction -- 2026-06-12**
>
> The v1.0 brief targeted FAQ **question** templates. Codex implemented that correctly and the question fixes are live -- **do not revert them.**
>
> This v1.1 corrects the scope: the DH canonical scanner (`tests/echo_pace_cry_scan.py`) evaluates FAQ **answers** only, using a 4-gram threshold at >15% prevalence. The question-variation fix cannot clear that gate. The remaining L2 failures are in answer templates, identified by live scan below.

---

## Current Status (after Codex question-variation fix)

```
CRYSTAL:   L1 28.7% PASS   L2 FAIL (10 violations)   L3 PASS
INTENTION: L1 44.5% PASS   L2 FAIL (10 violations)   L3 PASS
```

All violations are in FAQ **answer** text. Three answer-level root causes confirmed.

---

## Root Cause 1 -- CRYSTAL `_care_note()` variant 4 (~line 2069)

`_care_note()` uses `_pick_variant_key(f"{slug}:care-safe-base", 314, [...])` with 5 variants. **Variant index 4** (the last variant in the list) contains two fixed 4-gram sequences that appear at 24% prevalence each:

- `'usually needs modest care'`
- `'routine cleansing normally covered'`

**Current text (variant 4):**
```python
f"At about Mohs {profile['hardness_mohs']}, {name} usually only needs modest care. For {name}, routine cleansing is normally covered by {first_method} plus {second_method}.",
```

**Required fix -- replace variant 4 text only:**
```python
f"At about Mohs {profile['hardness_mohs']}, {name} holds up well with lighter attention. {first_method} and {second_method} both serve as reliable resets between uses.",
```

Only the last item in the `_pick_variant_key()` list changes. The function call, seed (314), and all other variants are unchanged.

---

## Root Cause 2 -- CRYSTAL FAQ Q1 answer (`_build_faq()`, ~line 2173)

The FAQ Q1 answer is a fixed-format string:
```python
"a": f"{name}: {notes['identity']}. {notes['signature']}. {notes['best_for']}. {benefit_a}, {benefit_b}, {benefit_c}.",
```

Where `benefit_a, benefit_b, benefit_c = _benefit_labels(profile)` returns the first 3 entries of `profile["benefit_tags"]` with hyphens stripped. Multiple crystals sharing the same first-3 benefit tags produce identical answer text.

**Failing phrase:**
- `'grief compassion emotional repair'` (22%) -- from crystals where benefit_tags opens with `["grief", "compassion", "emotional-repair", ...]`

**Required fix -- wrap the answer in `_pick_variant_key()`:**
```python
"a": _pick_variant_key(f"{slug}:faq-a0", 410, [
    f"{name}: {notes['identity']}. {notes['signature']}. {notes['best_for']}. {benefit_a}, {benefit_b}, {benefit_c}.",
    f"{name}: {notes['best_for']}. {notes['identity']}. Common uses include {benefit_a} and {benefit_b}.",
    f"{name}: {notes['signature']}. {notes['best_for']}. This stone particularly supports {benefit_a}.",
    f"{name} is associated with {notes['identity']}. Practical uses: {benefit_a}, {benefit_b}.",
    f"{name}: {notes['best_for']}. {notes['identity']}. Benefit areas: {benefit_a}, {benefit_b}, {benefit_c}.",
]),
```

The 5 variants use the same data (`notes`, `benefit_a/b/c`) -- no new fields needed. Seed 410 is unused in this file.

---

## Root Cause 3 -- INTENTION `_intention_identity_phrase()` variants 0 and 4 (~lines 2338, 2342)

`_intention_identity_phrase()` uses `_pick_variant_key(f"{intention_slug}:{crystal_slug}:identity", 333, [...])` with 6 variants. **Variants 0 and 4** contain fixed structural phrases that -- after stopword stripping by the DH scanner -- appear as identical 4-grams across multiple intention pages sharing the same element or color.

**Failing phrases and their source:**

| Variant | 4-gram | Prevalence | Current text |
|---|---|---|---|
| 0 | `'presence ritual moves distinctly'` | 50% | `f"{name} brings a {color} presence, and the ritual moves with a distinctly {element} tempo around it."` |
| 4 | `'suit work better louder'` / `'work better louder material'` | 40% | `f"{name} helps when a {color} stone and {element} pacing suit the work better than louder material."` |

**Required fix -- replace variant 0 and variant 4 text only:**

```python
# Variant 0 replacement:
f"{name} holds a {color} quality, giving the practice a {element}-oriented feel from the start.",

# Variant 4 replacement:
f"When the work calls for a {color} anchor, {name} brings a {element} character that serves the purpose.",
```

All other variants (1, 2, 3, 5) and the function call, seed (333) are unchanged.

---

## Acceptance Criteria

Run `tests/echo_pace_cry_scan.py` after delivery:
- L2: 0 FAIL phrases for both CRYSTAL and INTENTION
- L1 batch: PASS for both types (must not regress from 28.7% / 44.5%)

---

## Summary of Changes

| Location | Change |
|---|---|
| `_care_note()` ~line 2069 | Rewrite variant 4 text in `care-safe-base` picker (leave other 4 variants and seed unchanged) |
| `_build_faq()` ~line 2173 | Wrap FAQ Q1 answer in `_pick_variant_key(f"{slug}:faq-a0", 410, [...])` -- 5 variants using existing `notes` / `benefit_a/b/c` data |
| `_intention_identity_phrase()` ~lines 2338, 2342 | Rewrite variant 0 and variant 4 text in `identity` picker (leave other 4 variants and seed unchanged) |

**Do NOT change** `_hash_index()`, `_pick_variant_key()`, the question-level variations Codex already implemented, body content generators, or any routing/API logic.

---

*[CC]_COMMISSION_CRY_L2_FIX · Echo.PaceScanner · CC Authored · v1.1 · 2026-06-12*
