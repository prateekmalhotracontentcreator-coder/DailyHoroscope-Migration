from __future__ import annotations

from typing import Any


TRANCHE_RULES: list[dict[str, Any]] = [
    {
        "condition": {"family_wealth_tier": "high"},
        "axis": "financial_security",
        "action": "dampen_secondary_negatives",
        "factor": 0.60,
    },
    {
        "condition": {"relationship_status": "married", "gamma_score": {"gte": 0.70}},
        "axis": "partnership_stability",
        "action": "suppress_secondary_delay_indicators",
        "factor": 0.50,
    },
    {
        "condition": {"salary_bracket": "high"},
        "axis": "career_growth",
        "action": "dampen_secondary_negatives",
        "factor": 0.65,
    },
    {
        "condition": {"beta_score": {"gte": 0.70}},
        "axis": "health_vitality",
        "action": "dampen_secondary_negatives",
        "factor": 0.70,
    },
]


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


def _action_applies(
    action: str,
    rule: dict[str, Any],
    backbone_science_id: str | None,
) -> bool:
    """Return True if the tranche action should be applied to this rule."""
    science_id = rule.get("science_id", "")
    if backbone_science_id and science_id == backbone_science_id:
        return False

    polarity = rule.get("claim_polarity", "")
    timing_bias = rule.get("timing_bias", "")

    if action == "dampen_secondary_negatives":
        return polarity == "negative"
    if action == "suppress_secondary_delay_indicators":
        return timing_bias in ("late", "cyclical")
    return False


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
        adjusted = dict(rule)

        for tranche_rule in TRANCHE_RULES:
            if tranche_rule["axis"] != claim_axis:
                continue
            if not _eval_predicate(tranche_rule["condition"], user_context):
                continue
            if not _action_applies(tranche_rule["action"], rule, backbone):
                continue
            current_ec = float(adjusted.get("effective_confidence", 1.0))
            adjusted["effective_confidence"] = round(current_ec * tranche_rule["factor"], 4)
            adjusted["_tranche_adjusted"] = True

        result.append(adjusted)

    return result
