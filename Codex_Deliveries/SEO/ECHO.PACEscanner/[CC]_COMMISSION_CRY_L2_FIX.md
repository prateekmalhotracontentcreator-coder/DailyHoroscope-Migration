---
title: "[CC] Commission -- Crystal L2 Fix"
version: v1.0
date: 2026-06-12
status: ISSUED
authored_by: CC (Claude Code / ECHO.PaceScanner)
github_issue: https://github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration/issues/3
target_file: backend/crystal_data.py
delivery_branch: codex/commission-cry-l2-fix
---

# [CC] Commission -- Crystal L2 Fix

## Overview

Two Crystal page types (CRYSTAL and INTENTION) fail L2 due to fixed FAQ question text. L1 passes cleanly for both. Root cause confirmed by live ECHO.PaceScanner engine scan on 2026-06-12.

**All changes are in one file: `backend/crystal_data.py`.**

---

## Live Scan Results (2026-06-12)

| Type | Pages | L1 worst | L1 batch | L2 fails |
|---|---|---|---|---|
| CRYSTAL | 50 | 34.9% ✅ | PASS | 5 |
| INTENTION | 20 | 42.4% ✅ | PASS | 36 |

L1 is clean -- no body content changes needed.

---

## Problem -- L2: FAQ Question Templates (both types)

Fixed question strings in `_build_faq()` (~line 2158) produce 3-gram substrings at 100% prevalence across all pages of each type.

**Confirmed failing phrases:**

CRYSTAL: `'how do cleanse'` · `'which chakra is'` · `'who should work'` · `'should work with'`

INTENTION: `'crystals replace practical'` · `'should cleanse crystals'` · `'practical action for'` · `'is best for'`

---

## Fix Required

### CRYSTAL pages -- `_build_faq()` (~line 2158)

Use the existing `_pick_variant_key()` infrastructure (already present at ~line 1851) to vary each of the 5 FAQ questions:

```python
# Q1 -- "What is {name} good for?"
_pick_variant_key(f"{slug}:faq-q0", 400, [
    f"What is {name} good for?",
    f"What does {name} help with?",
    f"How is {name} used in practice?",
    f"What purposes does {name} serve?",
    f"Where does {name} fit in a crystal practice?",
])

# Q2 -- "Which chakra is {name} connected to?"
_pick_variant_key(f"{slug}:faq-q1", 401, [
    f"Which chakra is {name} connected to?",
    f"What energy centre does {name} work with?",
    f"How does {name} relate to the chakra system?",
    f"Which chakra does {name} activate?",
    f"What is the chakra alignment of {name}?",
])

# Q3 -- "How do I cleanse {name}?"
_pick_variant_key(f"{slug}:faq-q2", 402, [
    f"How do I cleanse {name}?",
    f"What is the best way to clear {name}?",
    f"How should {name} be energetically reset?",
    f"What cleansing methods suit {name}?",
    f"How often and how do I clear {name}?",
])

# Q4 -- "Can I use {name} every day?"
_pick_variant_key(f"{slug}:faq-q3", 403, [
    f"Can I use {name} every day?",
    f"Is {name} suitable for daily wear?",
    f"How frequently can {name} be used?",
    f"Is {name} safe to work with regularly?",
    f"What is the recommended frequency for {name}?",
])

# Q5 -- "Who should work with {name}?"
_pick_variant_key(f"{slug}:faq-q4", 404, [
    f"Who should work with {name}?",
    f"Who benefits most from {name}?",
    f"Which people are drawn to {name}?",
    f"For whom is {name} most meaningful?",
    f"Who traditionally uses {name}?",
])
```

### INTENTION pages -- FAQ builders (~line 2390)

1. Vary "Which crystal is best for X?" -- 5 variants using `_pick_variant_key()`
2. Vary the disclaimer phrase -- appears verbatim on every intention page:

```python
_pick_variant_key(f"{slug}:disclaimer", 405, [
    "Crystal work is a complement to practical action, not a replacement for it.",
    "Working with crystals supports real-world effort -- it does not substitute for it.",
    "These practices work alongside practical steps, not instead of them.",
    "Crystal practice amplifies intention; the action itself still needs to happen.",
    "The crystal holds the field -- the practical work still has to be done.",
])
```

3. Vary any question containing "should cleanse crystals" -- 5 question variants using the same pattern as CRYSTAL Q3 above.

---

## Acceptance Criteria

Run `tests/echo_pace_cry_scan.py` after delivery:
- L2: 0 FAIL phrases for both CRYSTAL and INTENTION
- L1 batch: PASS for both types (must not regress from 34.9% / 42.4%)

**Do NOT change** `_hash_index()`, `_pick_variant()`, `_pick_variant_key()`, body content generators, or any routing/API logic. Question template and disclaimer changes only.

---

## Files Changed

| File | Change |
|---|---|
| `backend/crystal_data.py` | Vary 5 question templates in `_build_faq()`; vary disclaimer phrase in INTENTION FAQ builder |

---

*[CC]_COMMISSION_CRY_L2_FIX · Echo.PaceScanner · CC Authored · v1.0 · 2026-06-12*
