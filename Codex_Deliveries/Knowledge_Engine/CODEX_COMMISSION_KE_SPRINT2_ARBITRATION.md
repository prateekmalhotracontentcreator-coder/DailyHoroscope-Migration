# Codex Commission Brief -- KE Phase 1.2 Sprint 2: Arbitration Runtime
> Commission ID: KE-Sprint2
> Thread: Knowledge Engine (Commission I -- Phase 1.2)
> Issued: 2026-05-15 | Priority: 🔴 CRITICAL
> Pre-condition: Sprint 1 gate ✅ passed (commit `57e347a`). `science_registry` seeded in MongoDB.

---

## INGEST FREEZE IN EFFECT

**No new chapters may be ingested until this Sprint 2 gate passes.** This includes Ch 54-60, A Text Book Ch 15, and all Yoga chapters. Validation re-runs on existing batches are still allowed.

---

## Context

Sprint 1 wired α/β/γ contextual multipliers into `_score_rule()`. Sprint 2 builds the full arbitration runtime -- four tightly coupled gaps that must be delivered as a single diff.

**Gaps in scope:**
- G-03 -- Contradiction C-score formula (TD-16)
- G-05 -- Representation mode selector (TD-21)
- G-06 -- Tension block builder (TD-20)
- G-04 -- Supersession table runtime lookup (TD-14/TD-17)

**Single file target:** `backend/knowledge_engine.py`

---

## Architecture Rule (Mandatory -- Read Before Writing)

All live astronomical and dasha computations MUST use `vedic_calculator.py` + `pyswisseph`. Do NOT add dasha calculation functions to `knowledge_engine.py`. The `compute_dasha_timeline()` function added in Sprint 3 preview should be the only KE-internal dasha function and it delegates to `vedic_calculator`.

---

## G-03 -- Contradiction C-Score Formula (TD-16)

Implement the contradiction scoring function exactly per Section 16 of the KE Contract:

```
C = 0.40×polarity_delta + 0.35×timing_delta + 0.15×strength_delta + 0.10×authority_delta
Flag as contradiction if C ≥ 0.55
```

**Delta definitions:**
- `polarity_delta`: 1.0 if opposing polarity (positive vs negative); 0.5 if one is mixed; 0.0 if same polarity
- `timing_delta`: 1.0 if same timing window with opposite outcome; scaled proportionally otherwise
- `strength_delta`: absolute difference in `strength_band` mapped linearly to 0.0-1.0
- `authority_delta`: 0.0 if same science; scaled by `hierarchy_rank` difference from `science_registry`

**Function signature:**
```python
def _contradiction_score(
    rule_a: InterpretationRuleDocument,
    rule_b: InterpretationRuleDocument
) -> tuple[float, bool]:
    """
    Returns (c_score: float, is_contradiction: bool).
    is_contradiction = True if c_score >= 0.55
    """
```

---

## G-05 -- Representation Mode Selector (TD-21)

Select per domain after contradiction scoring:

| C-score range | Representation mode |
|---|---|
| C < 0.30 | `synthesis` |
| 0.30 ≤ C ≤ 0.75 | `tension` |
| C > 0.75 | `honest_uncertainty` |

**Function signature:**
```python
def _representation_mode(
    c_scores: list[float]
) -> Literal["synthesis", "tension", "honest_uncertainty"]:
    """
    Takes all pairwise C-scores for matched rules in a domain.
    Returns the mode for that domain.
    """
```

---

## G-06 -- Tension Block Builder (TD-20)

Build `tension_block` JSON evidence packet per Section 17.3 of the KE Contract when `representation_mode == "tension"`:

```python
tension_block = {
    "rule_a_id": str,           # ObjectId string
    "rule_b_id": str,           # ObjectId string
    "c_score": float,           # the pairwise C-score
    "polarity_delta": float,
    "timing_delta": float,
    "strength_delta": float,
    "authority_delta": float,
    "domain": str,              # the domain slug (e.g. "career", "health")
    "resolution_hint": str      # brief note: which rule has higher authority and why
}
```

**Function signature:**
```python
def _build_tension_block(
    rule_a: InterpretationRuleDocument,
    rule_b: InterpretationRuleDocument,
    c_score: float,
    domain: str
) -> dict:
```

---

## G-04 -- Supersession Table Runtime Lookup (TD-14/TD-17)

Look up `science_registry` in MongoDB to determine which science's rule takes precedence when a contradiction is detected. Use `DEFAULT_SUPERSESSION_MAP` as the in-process fallback if the collection lookup fails or is unavailable.

**`science_registry` documents already seeded in MongoDB (18 Apr 2026):**

| Science | Role |
|---|---|
| `vedic_astrology` | `backbone_or_primary_lead` |
| `numerology` | `secondary_supportive` |
| `palmistry` | `secondary_specialist` |
| `tarot` | `reflective_advisory` |

**Fallback map (use if DB lookup fails):**
```python
DEFAULT_SUPERSESSION_MAP = {
    "career": {
        "career_growth": ["vedic_astrology", "numerology", "palmistry", "tarot"]
    },
    "wealth": {
        "financial_security": ["vedic_astrology", "numerology", "tarot", "palmistry"]
    },
    "relationships": {
        "partnership_stability": ["vedic_astrology", "numerology", "tarot", "palmistry"],
        "marriage_timing":       ["vedic_astrology", "numerology", "tarot", "palmistry"]
    },
    "health": {
        "health_vitality": ["vedic_astrology", "palmistry", "numerology", "tarot"]
    },
    "general": {
        "*": ["vedic_astrology", "numerology", "palmistry", "tarot"]
    },
}
```

---

## G-02 -- Still Deferred

Do NOT include tier multipliers (×0.60→×1.15) in Sprint 2. These require claim clustering which is a Sprint 2 output -- Codex to determine the right insertion point once G-03/G-05/G-06 are wired.

---

## Output Integration

The `scan_chart()` function response payload must include two new top-level fields:

```python
{
    # ... existing fields ...
    "representation_mode": "synthesis" | "tension" | "honest_uncertainty",
    "tension_blocks": [
        {
            "rule_a_id": "...",
            "rule_b_id": "...",
            "c_score": 0.62,
            # ... all tension_block fields
        }
    ]
}
```

`tension_blocks` is an empty list `[]` when `representation_mode == "synthesis"`.

---

## Sprint 2 Acceptance Gate

All 5 criteria must pass before Sprint 3 brief is issued:

1. `_contradiction_score(rule_a, rule_b)` returns correct C-score for known opposing and agreeing rule pairs
2. `_representation_mode([c_score_list])` returns `synthesis` for C < 0.30, `tension` for 0.30-0.75, `honest_uncertainty` for C > 0.75
3. `_build_tension_block(rule_a, rule_b, c_score, domain)` returns a correctly shaped dict matching the schema above
4. Supersession lookup returns the highest-ranked science for a given domain (with fallback to `DEFAULT_SUPERSESSION_MAP` on DB miss)
5. `scan_chart()` response includes `representation_mode` and `tension_blocks` in the payload

**Deliver as a single diff against `backend/knowledge_engine.py`. Commit to `main`.**

---

## What Comes Next (Sprint 3 -- do not build in this commission)

Sprint 3 covers G-07, G-08, G-09 (Arc Angel period quality computation + 10-year windows). Sprint 3 must consume post-arbitration, post-convergence output -- not raw matched rules. Sprint 3 brief will be issued after Sprint 2 gate passes.

---

## Files to Modify

```
backend/knowledge_engine.py    ← only file in scope
```

Do NOT touch:
```
backend/vedic_calculator.py
backend/panchang_router.py
backend/server.py              (unless absolutely required for a response shape change)
frontend/                      (zero frontend changes in this commission)
```

---

## Build Verification

```bash
cd backend
python -c "import knowledge_engine; print('import OK')"
```

Then run the 5 acceptance gate tests above manually against the live backend.

---

## Commit Format

```
feat(knowledge-engine): implement sprint 2 arbitration runtime (G-03/G-04/G-05/G-06)
```
