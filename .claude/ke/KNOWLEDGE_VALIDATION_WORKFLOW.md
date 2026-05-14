# Knowledge Engine — Automated Rule Validation Workflow

> Document type: Design + Codex Commission Brief
> Scope: Phase 1 rules (948 rules, approval_status = pending_review)
> Principle: Claude validates; humans only review what Claude flags

---

## 1. The Problem With Manual Review

948 rules across 8 books. Manual review would take days, introduce human bias,
and miss cross-book contradictions that only become visible at scale.

The right approach: Claude reads Vedic astrology fluently. Use it to:
- Evaluate every rule for quality and correctness in batches (cheap, fast)
- Detect contradictions across books automatically
- Auto-approve rules that pass; surface only genuine problems to humans
- Expect <10% of rules to need human eyes

---

## 2. Validation Pipeline — Four Stages

```
Stage 1: Structural Check (free — no API call)
   └─ Does rule have all required fields?
   └─ Is condition parseable?
   └─ Is interpretation text non-empty and not OCR garbage?
   └─ Verdict: PASS / STRUCTURAL_FAIL

Stage 2: Claude Quality + Correctness Check (batched API calls)
   └─ Is this astrologically coherent and consistent with classical texts?
   └─ Is the paraphrase a faithful rendering of what a classical source would say?
   └─ Does it make logical sense as a prediction rule?
   └─ Verdict per rule: APPROVE / FLAG / SPOT_CHECK

Stage 3: Cross-Rule Contradiction Detection (grouped + Claude)
   └─ Group rules by condition type + planet + house/sign
   └─ For each group: do any rules say directly opposite things?
   └─ Verdict: CORROBORATED / CONTRADICTS (with rule_id of the conflicting rule)

Stage 4: Final Disposition
   └─ APPROVE + CORROBORATED  → auto_approved  (live in engine immediately)
   └─ APPROVE + no contradiction → auto_approved
   └─ SPOT_CHECK              → pending_human_review  (sampled 10%)
   └─ FLAG or CONTRADICTS     → flagged  (human reviews these only)
   └─ STRUCTURAL_FAIL         → rejected
```

---

## 3. Expected Outcome

| Tier | Expected % | Action |
|---|---|---|
| `auto_approved` | ~70% (~660 rules) | Immediately live in Knowledge Engine |
| `pending_human_review` | ~10% (~95 rules) | Spot-check sample — quick human pass |
| `flagged` | ~15% (~140 rules) | Human reviews with Claude's reason attached |
| `rejected` | ~5% (~50 rules) | Structural failures — discarded |

Human effort: ~235 rules instead of 948. ~75% reduction.

---

## 4. Files to Build

| File | Purpose |
|---|---|
| `backend/scripts/validate_rules.py` | Main validation + auto-approval script |
| `backend/knowledge_validator.py` | Claude batch validation logic (imported by router too) |

---

## 5. `validate_rules.py` — CLI Script

### 5a. CLI interface

```bash
# Validate all pending_review rules (primary usage):
python scripts/validate_rules.py \
  --mongo-url "$MONGO_URL" \
  --db-name "$DB_NAME" \
  [--batch-size 20]        # rules per Claude call, default 20
  [--science-id vedic_astrology]  # filter to one science, default all
  [--dry-run]              # print verdicts but do NOT write to MongoDB
  [--report-path ./output/validation_report.md]
```

### 5b. Structural check (free — no Claude)

```python
GARBAGE_PATTERNS = re.compile(
    r"(.)\1{6,}|"           # repeated chars: xxxxxxx
    r"[^\x00-\x7F]{10,}|"   # long non-ASCII runs (OCR artifacts)
    r"\b[A-Z]{15,}\b"       # very long ALL-CAPS tokens
)

def structural_check(rule: dict) -> tuple[bool, str]:
    interp = rule.get("interpretation", {})
    detailed = interp.get("detailed", "") or ""
    summary  = interp.get("summary", "")  or ""
    if not detailed.strip() and not summary.strip():
        return False, "empty_interpretation"
    if GARBAGE_PATTERNS.search(detailed):
        return False, "ocr_garbage_detected"
    if len(detailed.split()) < 10:
        return False, "interpretation_too_short"
    condition = rule.get("condition")
    if not condition or not isinstance(condition, dict):
        return False, "missing_condition"
    return True, "ok"
```

### 5c. Claude batch quality check

Call Claude once per batch of 20 rules. Use `claude-haiku-4-5` for cost efficiency
(~$0.25 per million tokens). Prompt:

```python
VALIDATION_PROMPT = """
You are a senior Vedic astrology scholar and knowledge engineer reviewing
extracted interpretation rules for EverydayHoroscope's Knowledge Engine.

For each rule below, evaluate:
1. CORRECTNESS — Is this consistent with classical Vedic astrology?
   (Brihat Parashara Hora Shastra, Phaladeepika, Lal Kitab, etc.)
2. QUALITY — Is the text coherent, specific, and useful as a prediction rule?
3. SOURCE_FAITHFULNESS — Does it sound like a faithful paraphrase of a classical source?

Verdict options:
- "approve"     — Correct, coherent, ready for production use
- "spot_check"  — Probably fine but borderline; needs a quick human glance
- "flag"        — Incorrect, incoherent, or suspicious; needs human review

Return ONLY a JSON array — one object per rule — in this exact shape:
[
  {
    "rule_id": "<rule_id>",
    "verdict": "approve" | "spot_check" | "flag",
    "reason": "<one sentence — only required for spot_check and flag>",
    "corrected_confidence": "HIGH" | "MEDIUM" | "LOW"
  }
]

Rules to evaluate:
{rules_json}
"""
```

Format each rule for the prompt as:
```python
{
  "rule_id": rule["rule_id"],
  "source_book": rule.get("source", {}).get("book", ""),
  "chapter": rule.get("source", {}).get("chapter", ""),
  "condition": rule.get("condition", {}),
  "summary": rule["interpretation"]["summary"],
  "detailed": rule["interpretation"]["detailed"][:400],   # cap at 400 chars
  "current_confidence": rule.get("confidence", "MEDIUM")
}
```

### 5d. Contradiction detection

After Stage 2, group rules by `(condition.type, condition.planet, condition.house OR condition.sign)`.
For any group with ≥2 rules, call Claude once per group to compare:

```python
CONTRADICTION_PROMPT = """
You are checking whether any of the following Vedic astrology rules directly
contradict each other. Rules from different books may naturally differ in
emphasis — that is NOT a contradiction. A true contradiction is when two rules
make opposite factual claims about the same planetary position.

Return ONLY a JSON array of contradiction pairs (empty array if none):
[
  {
    "rule_id_a": "...",
    "rule_id_b": "...",
    "contradiction_summary": "<one sentence explaining the conflict>"
  }
]

Rules to compare:
{rules_json}
"""
```

### 5e. MongoDB updates

After validation, write results back:

```python
# auto_approved
db["interpretation_rules"].update_one(
    {"rule_id": rule_id},
    {"$set": {
        "approval_status": "auto_approved",
        "validation": {
            "verdict": "approve",
            "validated_by": "claude-haiku-4-5",
            "validated_at": now_iso(),
            "corrected_confidence": corrected_confidence,
            "contradiction_ids": []
        }
    }}
)

# flagged
db["interpretation_rules"].update_one(
    {"rule_id": rule_id},
    {"$set": {
        "approval_status": "flagged",
        "validation": {
            "verdict": "flag",
            "flag_reason": reason,
            "validated_by": "claude-haiku-4-5",
            "validated_at": now_iso(),
            "contradiction_ids": contradiction_ids   # list, may be empty
        }
    }}
)
```

After writing all verdicts, call `schedule_index_refresh()` via a direct pymongo
update on `app_settings` to signal the engine (or use an HTTP call to
`POST /api/knowledge/refresh-index` with admin auth).

### 5f. Validation report (Markdown)

Write to `--report-path` if provided:

```markdown
# Knowledge Engine Validation Report
Generated: {datetime}
Science: {science_id or "all"}

## Summary
| Verdict         | Count | % |
|---|---|---|
| auto_approved   | 660   | 70% |
| pending_human   | 95    | 10% |
| flagged         | 140   | 15% |
| rejected        | 53    | 5%  |
| **Total**       | **948** | |

## Contradictions Detected
{list of pairs with summaries}

## Flagged Rules (sample — first 20)
{rule_id | book | chapter | reason}

## Rejected Rules
{rule_id | book | reason}
```

---

## 6. `knowledge_validator.py` — Backend Module

This is a thin wrapper so the same validation logic can be called from:
- `validate_rules.py` (batch script, local)
- `POST /api/knowledge/validate-batch` (admin API endpoint — future)

```python
# knowledge_validator.py
class RuleValidator:
    def __init__(self, model: str = "claude-haiku-4-5"):
        self.model = model
        self.client = anthropic.Anthropic()

    def validate_batch(self, rules: list[dict]) -> list[dict]:
        """Returns list of {rule_id, verdict, reason, corrected_confidence}"""
        ...

    def detect_contradictions(self, rules: list[dict]) -> list[dict]:
        """Returns list of {rule_id_a, rule_id_b, contradiction_summary}"""
        ...

    def structural_check(self, rule: dict) -> tuple[bool, str]:
        ...
```

---

## 7. Library Console Updates (LibraryConsolePage.jsx)

Add validation status badges to the Rules Browser tab:

| Badge | Colour | Meaning |
|---|---|---|
| Auto-approved | green | Passed Claude validation |
| Pending review | amber | Awaiting human spot-check |
| Flagged | red | Claude found an issue — reason shown on hover |
| Rejected | grey | Structural failure |
| Contradicts | orange | Conflicts with another rule — linked |

Add **"Run Validation"** button to Import Batches tab:
- Calls `POST /api/knowledge/validate-batch?batch_id=xxx`
- Shows spinner → completion toast with summary counts

---

## 8. Codex Commission — What to Build

### Files to create
| File | Notes |
|---|---|
| `backend/scripts/validate_rules.py` | Full CLI script per spec above |
| `backend/knowledge_validator.py` | `RuleValidator` class — no FastAPI dependency |

### Files to modify
| File | Change |
|---|---|
| `backend/knowledge_schema.py` | Add `validation` sub-object to `InterpretationRuleDocument` |
| `backend/knowledge_router.py` | Add `POST /api/knowledge/validate-batch` endpoint |
| `frontend/.../LibraryConsolePage.jsx` | Validation badges + Run Validation button |

### Model to use
`claude-haiku-4-5` — not Sonnet. Cost for 948 rules:
- ~48 batch calls × ~2,500 tokens = ~120k tokens
- ~$0.15 total. Fast (~3 min for full run).

### Key constraints
- `validate_rules.py` must have NO fastapi/motor imports — local script only
- `knowledge_validator.py` must be importable by both script and router
- Structural check runs before any Claude call (fast fail, saves API cost)
- Batch size default 20, configurable via `--batch-size`
- `--dry-run` prints verdicts table but writes nothing to MongoDB
- `validation` field added to schema with `extra="allow"` guard OR explicit field
- Contradiction detection only runs on groups with ≥2 rules (skip singletons)
- After run, auto-approved rules must trigger index refresh

---

## 9. Temple Team Post-Validation Steps

1. Run `validate_rules.py --dry-run` → read report → confirm approach
2. Run `validate_rules.py` (real run) → ~3 minutes → ~660 rules auto-approved
3. Open `/admin/library` → Rules Browser → filter by `flagged` → review ~140 rules
4. For contradictions: read both rules side by side → keep the one from the
   more authoritative source (BPHS > Phaladeepika > Lal Kitab > modern texts)
5. Approve remaining `pending_human_review` batch (spot-check ~95 rules quickly)
6. Trigger final Refresh Index → all approved rules live in Knowledge Engine
