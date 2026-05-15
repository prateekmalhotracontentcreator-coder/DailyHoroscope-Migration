# Codex Brief -- Commission I CPath-1 Item 7: Simplified Tranche Filter

> To: Codex  
> From: EverydayHoroscope / Temple Team  
> CPath-1 Item: 7 of 8  
> Priority: HIGH -- gates item 8 (UI feedback)  
> Depends on: Items 1-6 (all committed ✅)

---

## What This Item Is

The **Tranche Filter** is a context-aware rule engine that sits between `scan_chart()`
and `generate_narrative()`. It reads the user's context profile (wealth tier, relationship
status, health indicators, career data) and dampens the `effective_confidence` of specific
secondary-science claims before the evidence packet reaches the Claude narrative planner.

**Purpose:** prevent false negatives. A negative financial claim from Tarot (a secondary
science) should carry less narrative weight when the user is demonstrably wealthy. A delay
indicator for partnerships should be suppressed when the user is happily married with a
high family-stability score.

**Phase 1 scope:**
- Full rule engine build -- not a stub or passthrough
- Seeded with rules for exactly 4 domains: `financial_security`, `partnership_stability`,
  `career_growth`, `health_vitality`
- Runs when user context is present; passes through unchanged when it is absent
- Only touches secondary science claims -- backbone science claims are never dampened

---

## Files to Create / Edit

| File | Type |
|---|---|
| `backend/tranche_filter.py` | NEW |
| `backend/knowledge_engine.py` | EDIT -- 2 small changes |

No other files. No server.py changes. No frontend changes (that is item 8).

---

## 1. New File -- `backend/tranche_filter.py`

### 1a. Seeded Tranche Rules

```python
from __future__ import annotations
from typing import Any

# Phase 1 seed rules -- 4 domains: financial_security, partnership_stability,
# career_growth, health_vitality.
# action values: "dampen_secondary_negatives" | "suppress_secondary_delay_indicators"
# factor: multiplied against effective_confidence (always < 1.0 in Phase 1)

TRANCHE_RULES: list[dict[str, Any]] = [
    # ── financial_security ───────────────────────────────────────────────────
    {
        "condition": {"family_wealth_tier": "high"},
        "axis": "financial_security",
        "action": "dampen_secondary_negatives",
        "factor": 0.60,
    },
    # ── partnership_stability ────────────────────────────────────────────────
    {
        "condition": {"relationship_status": "married", "gamma_score": {"gte": 0.70}},
        "axis": "partnership_stability",
        "action": "suppress_secondary_delay_indicators",
        "factor": 0.50,
    },
    # ── career_growth ────────────────────────────────────────────────────────
    {
        "condition": {"salary_bracket": "high"},
        "axis": "career_growth",
        "action": "dampen_secondary_negatives",
        "factor": 0.65,
    },
    # ── health_vitality ──────────────────────────────────────────────────────
    {
        "condition": {"beta_score": {"gte": 0.70}},
        "axis": "health_vitality",
        "action": "dampen_secondary_negatives",
        "factor": 0.70,
    },
]
```

### 1b. Condition Evaluator

The condition dict is a flat set of predicates; ALL must match (logical AND).
Values are either:
- A scalar: the user_context field must equal it exactly.
- A dict with comparison operators: `{"gte": X}` means `field >= X`,
  `{"lte": X}` means `field <= X`. Both can appear together.

```python
def _eval_predicate(condition: dict[str, Any], user_context: dict[str, Any]) -> bool:
    """Return True iff ALL condition predicates match user_context."""
    for key, expected in condition.items():
        actual = user_context.get(key)
        if actual is None:
            return False
        if isinstance(expected, dict):
            try:
                val = float(actual)
            except (TypeError, ValueError):
                return False
            if "gte" in expected and not (val >= float(expected["gte"])):
                return False
            if "lte" in expected and not (val <= float(expected["lte"])):
                return False
        else:
            if actual != expected:
                return False
    return True
```

### 1c. Action Matcher

The Tranche Filter only dampens **secondary-science** claims.
`backbone_science_id` is stored on each matched rule dict (set by `scan_chart()`).

```python
def _action_applies(
    action: str,
    rule: dict[str, Any],
    backbone_science_id: str | None,
) -> bool:
    """Return True if the tranche action should be applied to this rule."""
    # Only secondary sciences are subject to dampening
    science_id = rule.get("science_id", "")
    if backbone_science_id and science_id == backbone_science_id:
        return False  # backbone science -- never dampen

    polarity = rule.get("claim_polarity", "")
    timing_bias = rule.get("timing_bias", "")

    if action == "dampen_secondary_negatives":
        return polarity == "negative"
    if action == "suppress_secondary_delay_indicators":
        return timing_bias in ("late", "cyclical")
    return False
```

### 1d. Main Entry Point

```python
def apply_tranche_filter(
    matched_rules: list[dict[str, Any]],
    user_context: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Apply seeded Tranche rules to a matched_rules list (output of scan_chart()).

    Returns a new list. Each rule dict that matches a Tranche rule has its
    effective_confidence multiplied by the tranche factor and gains a
    _tranche_adjusted=True marker.

    Passes through unchanged (returns original list) when:
    - user_context is empty or None
    - matched_rules is empty
    """
    if not user_context or not matched_rules:
        return matched_rules

    result: list[dict[str, Any]] = []
    for rule in matched_rules:
        claim_axis = rule.get("claim_axis", "")
        backbone = rule.get("backbone_science_id")
        adjusted = dict(rule)  # shallow copy -- do not mutate the original

        for tranche_rule in TRANCHE_RULES:
            if tranche_rule["axis"] != claim_axis:
                continue
            if not _eval_predicate(tranche_rule["condition"], user_context):
                continue
            if not _action_applies(tranche_rule["action"], rule, backbone):
                continue
            current_ec = float(adjusted.get("effective_confidence", 1.0))
            adjusted["effective_confidence"] = round(current_ec * tranche_rule["factor"], 4)
            adjusted["_tranche_adjusted"] = True  # item 8 reads this for UI feedback

        result.append(adjusted)

    return result
```

---

## 2. Edit -- `backend/knowledge_engine.py`

### Change A -- Import

At the top of `knowledge_engine.py` (after existing imports), add:

```python
from tranche_filter import apply_tranche_filter
```

### Change B -- Wire into `generate_narrative()`

`generate_narrative()` starts at around line 814. It currently calls:
```python
matched_domains, planner_domains = _build_domain_plan(
    matched_rules=matched_rules,
    ...
    user_context=user_context or {},
)
```

Before that call, add one line:
```python
matched_rules = apply_tranche_filter(matched_rules, user_context or {})
```

The full block should read:
```python
matched_rules = apply_tranche_filter(matched_rules, user_context or {})
matched_domains, planner_domains = _build_domain_plan(
    matched_rules=matched_rules,
    chart=chart,
    context=request_context,
    tension_blocks=all_tension_blocks,
    user_context=user_context or {},
)
```

That is the entire edit to `knowledge_engine.py`. One import, one line.

---

## 3. How the Filter Interacts with Existing Code

**Inputs from `scan_chart()` -- fields the filter reads per rule:**

| Field | Source | Used for |
|---|---|---|
| `claim_axis` | `InterpretationRuleDocument` | Match against tranche rule `axis` |
| `claim_polarity` | `InterpretationRuleDocument` | `dampen_secondary_negatives` action |
| `timing_bias` | `InterpretationRuleDocument` | `suppress_secondary_delay_indicators` action |
| `science_id` | `InterpretationRuleDocument` | Backbone vs secondary detection |
| `backbone_science_id` | Added by `scan_chart()` at line 804 | Same |
| `effective_confidence` | Computed by `_score_rule()` at line 460 | The field the filter mutates |

**User context fields the filter reads:**

| Field | Type | Used by |
|---|---|---|
| `family_wealth_tier` | `"high"` / `"mid"` / `"low"` | financial_security rule |
| `relationship_status` | `"married"` / `"single"` / etc. | partnership_stability rule |
| `gamma_score` | float 0.0-1.0 | partnership_stability rule |
| `salary_bracket` | `"high"` / `"mid"` / `"low"` | career_growth rule |
| `beta_score` | float 0.0-1.0 | health_vitality rule |

All reads use `.get(key)` -- missing keys return `None` and cause the predicate to fail
silently (passthrough behaviour preserved).

---

## 4. Constraints

- **Do not modify `scan_chart()`** -- the filter runs after it, not inside it.
- **Do not modify `_build_domain_plan()`** -- feed it the filtered list directly.
- **Do not raise exceptions** -- any unexpected key shapes should fail the predicate
  silently (return `False` from `_eval_predicate`) so the claim passes through unmodified.
- **No new npm packages, no new Python packages** -- `tranche_filter.py` uses only stdlib.
- **`_tranche_adjusted`** private key on the rule dict is intentional -- item 8 reads it
  for the frontend feedback layer. Do not remove it.

---

## 5. Validation Checklist (Codex self-check)

- [ ] `tranche_filter.py` imports cleanly with no external dependencies
- [ ] `TRANCHE_RULES` has exactly 4 entries (one per seeded domain)
- [ ] `_eval_predicate` handles both scalar equality and `{"gte": X}` / `{"lte": X}` dicts
- [ ] `_action_applies` returns `False` for backbone science claims
- [ ] `apply_tranche_filter` returns original list unchanged when `user_context` is `{}`
- [ ] `apply_tranche_filter` returns shallow-copied dicts -- original list not mutated
- [ ] `_tranche_adjusted = True` marker is present on every dampened rule
- [ ] `knowledge_engine.py` import added
- [ ] `apply_tranche_filter()` called in `generate_narrative()` before `_build_domain_plan()`

---

## 6. What the Temple Team Will Do

1. Verify `_eval_predicate` handles compound conditions correctly
2. Verify the 4 seed rules cover all seeded domains
3. Check that `_action_applies` correctly identifies secondary vs backbone science
4. Commit as: `feat(knowledge-engine): CPath-1 item 7 -- Simplified Tranche Filter (4 domains)`
