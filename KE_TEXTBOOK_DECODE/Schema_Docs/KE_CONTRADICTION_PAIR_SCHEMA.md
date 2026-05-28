# KE Contradiction Pair Schema
## Encoding Standard for All Decode Threads

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-28
> Applies to: All active and future KE decode threads
> Schema constants: `backend/ke_schema_constants.py`

---

## What Is a Contradiction Pair

A contradiction pair is two rules that share the same (or highly similar) condition but predict opposite or incompatible outcomes.

**Example:**
- Rule A (BPHS Ch19): "8th lord in the Lagna confers long life." (`claim_polarity: "positive"`)
- Rule B (Phaladeepika XIII): "8th lord in Lagna with malefic aspect shortens life." (`claim_polarity: "negative"`)

Both rules share condition: `house_lord_in_house`, lord_of_house=8, placed_in_house=1. Their outcomes conflict.

Contradictions can be:
- **Within-text**: Two rules in the same source book that conflict
- **Cross-text**: Rules from two different source books that conflict

---

## Within-Text Contradictions -- How to Encode

### During decode (NLM thread responsibility)

When the NLM thread identifies two rules in the same chapter or across chapters of the same book that contradict each other:

**Step 1** -- Create the `Contradictions.json` file for that chapter (standard -- already done by all active threads).

**Step 2** -- On each conflicting rule document, populate the `conflicts_with` field:

```json
{
  "rule_id": "BPHS.Ch19.1.1",
  "conflicts_with": ["BPHS.Ch19.2.1"],
  "full_text": "8th lord in angle = long life.",
  "claim_polarity": "positive"
}
```

```json
{
  "rule_id": "BPHS.Ch19.2.1",
  "conflicts_with": ["BPHS.Ch19.1.1"],
  "full_text": "8th lord in 8th with malefic = short life.",
  "claim_polarity": "negative"
}
```

**Step 3** -- Record the contradiction in the chapter `Diagnostic.md` with a proposed resolution:

```markdown
## Contradictions

**BPHS.Ch19.1.1 vs BPHS.Ch19.2.1 -- 8th lord in angle**
- Ch19 Sl.1: 8th lord in angle = long life (positive)
- Ch19 Sl.2: 8th lord in 8th with malefic = short life (negative)
- Resolution proposed: strength_dependent -- 8th lord in angle without malefic aspect = long life; with malefic = short life. Not a genuine contradiction, a strength modifier.
```

### `conflicts_with` field rules

| Rule | Value |
|---|---|
| Field type | `list[str]` -- list of rule_id strings |
| Default | `[]` (empty list -- not null) |
| Direction | Bidirectional -- both rules must reference each other |
| Scope | Within-text only -- do NOT use `conflicts_with` for cross-text contradictions |

---

## Cross-Text Contradictions -- How to Encode

Cross-text contradictions are detected automatically by the dedup script (`ke_dedup_script.py`). NLM threads do **not** need to manually identify cross-text contradictions.

However, NLM threads must ensure:
1. `claim_polarity` is populated on every rule (required for automated detection)
2. Condition fields (`type`, `planet`, `house`, `sign`) are structurally accurate -- the dedup script matches on condition structure, not prose

When the dedup script runs, it populates `cross_text_matches` on both rules:

```json
{
  "rule_id": "BPHS.Ch19.1.1",
  "cross_text_matches": [
    {
      "rule_id": "PD.XIII.5.1",
      "similarity_score": 0.44,
      "relationship": "contradicts"
    }
  ]
}
```

NLM threads must leave `cross_text_matches: null` during decode. The dedup script populates it post-decode.

---

## Valid `relationship` Values (Full List)

From `VALID_CROSS_TEXT_RELATIONSHIPS` in `backend/ke_schema_constants.py`:

| Value | Meaning | When to use |
|---|---|---|
| `"identical_claim"` | Same condition, same outcome, nearly identical wording (score ≥ 0.95) | Strong duplicate -- likely same rule copied across texts |
| `"near_identical"` | Same condition, same outcome, slightly different wording (score ≥ 0.90) | Strong duplicate -- same tradition, minor translation variation |
| `"same_principle_different_phrasing"` | Same condition and principle, noticeably different phrasing (score ≥ 0.82) | Moderate duplicate -- cross-text agreement signal |
| `"partial_overlap"` | Related conditions, overlapping but not identical outcome (score ≥ 0.82) | Soft duplicate -- may or may not be the same rule |
| `"contradicts"` | Same condition, directly opposite polarity (positive vs negative) | Hard contradiction -- requires editorial review |
| `"partial_contradiction"` | Same condition, incompatible but not direct-opposite outcomes | Soft contradiction -- often resolved by a strength modifier |

---

## `claim_polarity` -- Required for Contradiction Detection

Every rule must have `claim_polarity` populated. The dedup script cannot detect contradictions if this field is missing.

| Value | Meaning |
|---|---|
| `"positive"` | Outcome is beneficial (wealth, health, success, longevity) |
| `"negative"` | Outcome is harmful (poverty, illness, failure, shortened life) |
| `"mixed"` | Outcome has both beneficial and harmful aspects |
| `"neutral"` | Outcome is descriptive only (no good/bad polarity) |

**NLM thread instruction:** Every rule in Rules.json must have one of the four values above. Leaving `claim_polarity` null will cause that rule to be skipped by contradiction detection.

---

## `Contradictions.json` File Format

Each chapter that has within-text contradictions should produce a `Contradictions.json` file alongside `Rules.json`. Standard format:

```json
[
  {
    "contradiction_id": "BPHS.Ch19.CONTR.1",
    "rule_a_id": "BPHS.Ch19.1.1",
    "rule_b_id": "BPHS.Ch19.2.1",
    "rule_a_summary": "8th lord in angle = long life",
    "rule_b_summary": "8th lord in 8th with malefic = short life",
    "condition_shared": {
      "type": "house_lord_in_house",
      "lord_of_house": 8
    },
    "polarity_a": "positive",
    "polarity_b": "negative",
    "contradiction_type": "within_text",
    "resolution_proposed": "strength_dependent",
    "resolution_note": "Both rules valid: Sl.1 applies when malefic aspect is absent, Sl.2 applies when malefic aspect is present. Context modifier resolves the apparent conflict.",
    "reviewer_status": "pending"
  }
]
```

| Field | Required | Description |
|---|---|---|
| `contradiction_id` | Yes | Format: `{SOURCE}.{CHAPTER}.CONTR.{N}` |
| `rule_a_id` / `rule_b_id` | Yes | The two conflicting rule IDs |
| `rule_a_summary` / `rule_b_summary` | Yes | One-line summary of each rule's outcome |
| `condition_shared` | Yes | The condition fields both rules share |
| `polarity_a` / `polarity_b` | Yes | The conflicting polarities |
| `contradiction_type` | Yes | `"within_text"` or `"cross_text"` |
| `resolution_proposed` | No | One of: `strength_dependent`, `timing_dependent`, `chart_context_dependent`, `genuine_disagreement`, `translator_interpolation` |
| `resolution_note` | No | Plain text explanation of the resolution |
| `reviewer_status` | Yes | `"pending"`, `"accepted"`, `"rejected"` |

---

## Resolution Types

| Value | Meaning |
|---|---|
| `"strength_dependent"` | Both rules valid -- one applies when planet/condition is strong, the other when weak |
| `"timing_dependent"` | Both rules valid -- one applies at different life stage or dasha period |
| `"chart_context_dependent"` | Both rules valid -- other chart factors (Lagna lord, benefic/malefic count) determine which fires |
| `"genuine_disagreement"` | The two texts genuinely disagree -- no reconciliation possible; human editor decides which to approve |
| `"translator_interpolation"` | One rule is translator commentary (not original sloka) and should be `approval_status: "tba_needs_trigger"` |

---

## Summary -- What Each Thread Must Produce

| Document | Responsible | When |
|---|---|---|
| `*_Rules.json` with `conflicts_with` populated | NLM decode thread | During chapter decode |
| `*_Contradictions.json` with full pair records | NLM decode thread | At chapter close |
| `claim_polarity` on every rule | NLM decode thread | During decode -- required for automated detection |
| `cross_text_matches` populated | Dedup script (automated) | Post-decode, after partner text is also decoded |
| `Dedup_Reports/*.json` summary report | Dedup script (automated) | After each cross-text pair run |

**NLM threads do NOT run the dedup script** -- Temple Team commissions and runs it after two or more text decodes are complete. NLM threads only need to produce clean `claim_polarity`, `conflicts_with`, and `Contradictions.json` during their decode session.

---

*Schema standard prepared by Temple Team -- EverydayHoroscope, 2026-05-28*
*Applies to all 10 books in the pending ingest plan*
