---
title: "[CC] Commission -- Rudraksha L1/L2 Fix"
version: v1.0
date: 2026-06-12
status: ISSUED
authored_by: CC (Claude Code / ECHO.PaceScanner)
github_issue: https://github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration/issues/2
target_file: backend/rudraksha_content.py
delivery_branch: codex/commission-rud-l1-l2-fix
---

# [CC] Commission -- Rudraksha L1/L2 Fix

## Overview

Four Rudraksha page types (MUKHI, PLANET, PROBLEM, SIGN) are blocked by L2 phrase violations and -- for MUKHI and SIGN -- also by L1 structural similarity failures. Root causes confirmed by live ECHO.PaceScanner engine scan on 2026-06-12.

**All changes are in one file: `backend/rudraksha_content.py`.**

---

## Live Scan Results (2026-06-12)

| Type | Pages | L1 worst | L1 batch | L2 fails |
|---|---|---|---|---|
| MUKHI | 21 | 97.6% ❌ | FAIL | 12 |
| PLANET | 9 | 94.9% (pair) | PASS | 32 |
| PROBLEM | 20 | 23.1% ✅ | PASS | 43 |
| SIGN | 12 | 96.5% ❌ | FAIL | 16 |

---

## Problem 1 -- L2: FAQ Question Templates (all 4 types)

All four page types use fixed question strings. The 3-gram substrings within questions appear at 100% prevalence across all pages of each type.

**Confirmed failing phrases:**

MUKHI: `'are the benefits'` · `'who should wear'` · `'can anyone wear'` · `'how do activate'`

PLANET: `'can wear rudraksha'` · `'with other beads'` · `'who should wear'` · `'is best for'`

PROBLEM: `'be worn together'` · `'alongside rudraksha for'` · `'should do alongside'` · `'to use it'`

SIGN: `'mukhi beads for'` · `'is best for'` · `'rudraksha is best'` · `'wear more than'`

### Fix

Replace all fixed question strings in `_faq_items()` (MUKHI, ~line 508) and the equivalent FAQ builders for PLANET (~line 968), PROBLEM (~line 1530), and SIGN (~line 1836) with 5-variant templates selected using the existing `_hash_index()` / `_variant_text()` infrastructure already in this file.

**Pattern (mirror existing answer variation -- same infrastructure, apply to questions):**

```python
# Current (wrong -- fixed question):
{"q": f"Who should wear {name}?", "a": answers[0]},

# Fixed (vary the question using existing _variant_text):
_q_who = _variant_text(
    page_key, 0,
    [
        "Who should wear {name}?",
        "Who is {name} most suited for?",
        "Which people benefit most from {name}?",
        "Who traditionally wears {name}?",
        "For whom is {name} most appropriate?",
    ],
    name=name,
)
{"q": _q_who, "a": answers[0]},
```

**Required question slots per type:**

MUKHI (`_faq_items`, ~line 594):
1. "Who should wear {name}?" → 5 variants
2. "What are the benefits of {name}?" → 5 variants
3. "How do I activate {name}?" → 5 variants (activate / energise / prepare / purify / initiate)
4. "Can anyone wear {name}?" → 5 variants
5. "How should {name} be worn?" → 5 variants

PLANET (~line 968):
1. "Which Rudraksha is best for {planet}?" → 5 variants
2. "Who should wear Rudraksha for {planet}?" → 5 variants
3. "When should Rudraksha for {planet} be energised?" → 5 variants
4. "Can I wear Rudraksha for {planet} with other beads?" → 5 variants
5. "Should everyone wear Rudraksha for {planet}?" → 5 variants

PROBLEM (~line 1530) and SIGN (~line 1836): Apply the same pattern to all question strings in those FAQ builders.

---

## Problem 2 -- L1: Body Differentiation (MUKHI + SIGN)

**MUKHI** (97.6%: 1-mukhi × 21-mukhi): Shared vocabulary in `overview` and body fields. 1-mukhi is about Shiva/consciousness/singularity. 21-mukhi is about Kubera/abundance/material fulfilment. These are semantically distinct -- the overview text must reflect that in vocabulary.

**SIGN** (96.5%: taurus × capricorn): Both earth signs share stability/grounded/material/practical vocabulary. Must be differentiated:
- Taurus → Venus, beauty, sensory, patience, stubbornness
- Capricorn → Saturn, ambition, time, discipline, authority

### Fix

In `_MUKHI_CORE` data: update the `overview` field for mukhi 1 and mukhi 21 to use semantically distinct vocabulary (at least 3 unique high-frequency tokens per entry that do not appear in the other).

In `_SIGN_CORE` data: update `intro` and `who_needs_this` fields for taurus and capricorn to use sign-specific vocabulary as described above.

---

## Acceptance Criteria

Run `tests/echo_pace_rud_scan.py` after delivery:
- L1 batch PASS for all four types (MUKHI worst pair < 85%, SIGN worst pair < 85%)
- L2: 0 FAIL phrases across all four types
- No regression on existing PASS verdicts (PLANET L1 PASS, PROBLEM L1 PASS)

**Do NOT change** `_hash_index()`, `_variant_text()`, or any routing/API logic.

---

## Files Changed

| File | Change |
|---|---|
| `backend/rudraksha_content.py` | Vary FAQ questions in `_faq_items()` + 3 equivalent builders; differentiate body text for 1-mukhi, 21-mukhi, taurus, capricorn |

---

*[CC]_COMMISSION_RUD_L1_L2_FIX · Echo.PaceScanner · CC Authored · v1.0 · 2026-06-12*
