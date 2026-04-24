# Codex Commission — Knowledge Engine Reconciliation
**Date:** 2026-04-25
**From:** Temple App Team
**Re:** Three outstanding reconciliation tasks for the Knowledge Engine rules library

---

## Context

The EverydayHoroscope Knowledge Engine stores Vedic astrology interpretation rules in MongoDB. Rules are extracted from classical source books (BPHS, A Textbook of Astrology, Lal Kitab, etc.) using AI-assisted ingest pipelines. A full validation pass has been completed across the library. Three items now require Codex to generate recommendations and scripts before the co-founder review session can conclude.

All three deliverables are backend Python scripts and/or data files. No frontend work. No new API routes.

---

## Deliverable 1 — Mars-H03 Manual Correction Patch

### Background

During TBA Chapter 15 ingest, the live run under-extracted rules for Mars in the Third House. Two OR-conditions were stored as single merged rules instead of being split into individual rules + grouped summary (per SPLITTING GUIDANCE A and B). The dry run correctly produced ~16 rules; the live run produced 12. Four rules are missing.

### Source Text (Mars in Third House — TBA Ch 15)

**Neutral gender block:**
> "IF with malefics or aspected by malefics — unfavourable for elder co-borns"

This OR-condition should have produced:
- Rule A: `IF Mars is conjunct malefics → unfavourable for elder co-borns`
- Rule B: `IF Mars is aspected by malefics → unfavourable for elder co-borns`
- Rule C: grouped summary (sign-list grouped summary style — `is_group_summary: false`, covers both conditions)

**Female horoscope block:**
> "IF Mars is in own sign or exalted — prosperous"

This OR-condition should have produced:
- Rule D: `IF Mars is in own sign → prosperous` (female)
- Rule E: `IF Mars is exalted → prosperous` (female)
- Rule F: grouped summary (covers both, `is_group_summary: false`)

### Existing Merged Rules to Deprecate

These are currently stored in `horoscope_db`, collection `interpretation_rules`:

```
condition_group_id: "tba15-mars-h03-neutral"   → find the merged malefics rule
condition_group_id: "tba15-mars-h03-female"    → find the merged own-sign/exalted rule
```

### Rule Document Schema

Every rule in the collection follows this structure:

```json
{
  "rule_id": "string — unique, format: {SOURCE_PREFIX}-{PLANET}-H{NN}-{gender}-{seq:03d}",
  "science_id": "vedic_astrology",
  "approval_status": "pending_review",
  "condition": {
    "type": "planet_in_house | planet_in_sign | combination | aspect_rule | ...",
    "planet": "Mars",
    "house": 3,
    "gender": "neutral | female",
    "additional_condition": "string describing secondary condition"
  },
  "interpretation": {
    "full_text_passages": [
      {
        "text": "interpretation text",
        "confidence": "HIGH | MEDIUM | LOW",
        "context": "natal"
      }
    ]
  },
  "condition_group_id": "tba15-mars-h03-neutral | tba15-mars-h03-female",
  "is_group_summary": false,
  "source": {
    "primary": "A Textbook of Astrology",
    "chapter": "Chapter 15 — Mars",
    "batch_id": "tba-ch15-v1-20260424",
    "author_voice": "modern_analytical"
  },
  "tags": ["planet_occupation", "house_placement"]
}
```

### What Codex Must Deliver

**File: `patch_mars_h03.py`**

A standalone Python script that:

1. Connects to MongoDB using `--mongo-url` and `--db-name` CLI args (same pattern as `validate_rules.py`)
2. Finds the two merged rules via `condition_group_id` filter
3. Prints them for confirmation (dry-run mode default)
4. When `--apply` flag is passed:
   - Inserts the 6 new split rules (Rules A–F above) with `approval_status: "pending_review"`
   - Sets the 2 merged originals to `approval_status: "deprecated"` with `validation.flag_reason: "merged_or_condition_split_by_patch_mars_h03"`
5. Prints a summary of what was inserted and deprecated

**The 6 new rule documents** should also be included as a JSON array in the script file as a constant (`PATCH_RULES = [...]`) so the co-founder can review the exact content before running `--apply`.

### Acceptance Criteria

- Dry run prints the 2 merged rules correctly identified
- `--apply` inserts exactly 6 new rules and deprecates exactly 2
- All 6 new rules have `approval_status: "pending_review"` (not auto-approved — they need co-founder review)
- `condition_group_id` on all 6 new rules matches the existing group IDs
- `is_group_summary: false` on all 6 (including the grouped summaries — per SPLITTING GUIDANCE A)
- Validate against Python 3.12

---

## Deliverable 2 — Contradiction Reconciliation Script

### Background

During validation, 125 unique contradiction pairs were detected in `horoscope_db`. A contradiction is two rules that share the same `condition.type / planet / house` grouping key but give conflicting interpretations. These rules were automatically downgraded from `auto_approved` to `pending_human_review` and tagged with `contradiction_ids` in their `validation` sub-document.

The co-founder needs to decide for each pair: keep rule A, keep rule B, keep both (different classical schools), or deprecate both. Codex must do the first pass so the co-founder is reviewing recommendations rather than blank rows.

### Contradiction Rule Document Shape

Rules involved in contradictions carry:

```json
{
  "rule_id": "...",
  "approval_status": "pending_human_review",
  "condition": { "type": "...", "planet": "...", "house": ... },
  "interpretation": { "full_text_passages": [{ "text": "..." }] },
  "source": { "primary": "...", "chapter": "...", "batch_id": "..." },
  "validation": {
    "verdict": "spot_check",
    "flag_reason": "Contradicts rule(s): RULE-ID-B",
    "contradiction_ids": ["RULE-ID-B"],
    "contradiction_summary": "Rule A says X; Rule B says Y"
  }
}
```

### Existing Export File

A CSV export already exists at:
`backend/scripts/reports/horoscope_db_contradictions.csv`

Columns:
```
pair_id, rule_id_a, status_a, book_a, chapter_a, condition_a, planet_a, house_a,
interpretation_a, rule_id_b, status_b, book_b, chapter_b, condition_b, planet_b,
house_b, interpretation_b, contradiction_summary, recommended_action
```

The `recommended_action` column is currently blank — this is what Codex fills.

### What Codex Must Deliver

**File: `reconcile_contradictions.py`**

A standalone Python script that:

1. Connects to MongoDB using `--mongo-url`, `--db-name` CLI args
2. Fetches all rules with `validation.contradiction_ids` non-empty
3. Pairs them up (same deduplication logic as the export — use `frozenset` to avoid double-counting)
4. For each pair, calls Claude with a prompt structured as:

```
You are a Vedic astrology Knowledge Engine editor reviewing conflicting interpretation rules.

Rule A:
  Source: {book_a}, {chapter_a}
  Condition: {planet} in House {house} — {condition_type}
  Interpretation: {text_a}

Rule B:
  Source: {book_b}, {chapter_b}
  Condition: {planet} in House {house} — {condition_type}
  Interpretation: {text_b}

These two rules conflict on the same condition. Recommend one of:
  keep_a     — Rule A is more accurate or authoritative; deprecate B
  keep_b     — Rule B is more accurate or authoritative; deprecate A
  keep_both  — Both are valid; they represent different classical schools or contexts
  deprecate_both — Neither is reliable; both should be removed

Respond in JSON:
{
  "recommendation": "keep_a | keep_b | keep_both | deprecate_both",
  "reasoning": "one sentence"
}
```

5. Writes results to an enriched CSV:
   `backend/scripts/reports/horoscope_db_contradictions_reconciled.csv`

   Same columns as the original export plus:
   - `codex_recommendation` — `keep_a / keep_b / keep_both / deprecate_both`
   - `codex_reasoning` — one-sentence reasoning
   - `final_action` — blank (co-founder fills this, can override codex_recommendation)

6. Processes in batches of 10 pairs with streaming writes to CSV after each batch (so progress is saved if interrupted)
7. Supports `--resume` flag to skip pairs already written to the output CSV (match on `pair_id`)
8. Uses `--model claude-haiku-4-5` for cost efficiency (same model as validate_rules.py)

**File: `apply_contradiction_decisions.py`**

A second script that:

1. Reads the reconciled CSV (after co-founder has filled `final_action` column)
2. For each row where `final_action` is filled:
   - `keep_a` → sets `rule_id_b` to `deprecated`
   - `keep_b` → sets `rule_id_a` to `deprecated`
   - `keep_both` → sets both to `pending_human_review` with note `contradiction_acknowledged_keep_both`
   - `deprecate_both` → sets both to `deprecated`
3. Dry-run mode by default; `--apply` flag executes writes
4. Prints summary of actions taken

### Acceptance Criteria

- Processes all 125 pairs without error
- Resume works correctly — re-running skips already-processed pairs
- Output CSV is valid and opens correctly in Excel / Numbers / Google Sheets
- `apply_contradiction_decisions.py` in dry-run mode prints each planned action before writing
- Validate against Python 3.12

---

## Deliverable 3 — Flagged Rules Reconciliation Script

### Background

1,329 rules in `horoscope_db` have `approval_status: "flagged"`. These were flagged by Claude during validation for quality issues. The most common `flag_reason` values are:

- Vague or ambiguous condition language
- Missing or weak interpretation text
- Over-generic interpretation (applies to too many conditions)
- Confidence mismatch (flagged as LOW but content seems valid)
- Structural edge case (passed structural check but borderline)

The co-founder needs a first-pass recommendation for each flagged rule: `approve` / `needs_edit` / `deprecate`. Codex processes all 1,329 rules in batches and outputs a CSV with recommendations. Co-founder spot-checks by source chapter and approves batches.

### Flagged Rule Document Shape

```json
{
  "rule_id": "...",
  "approval_status": "flagged",
  "condition": { "type": "...", "planet": "...", "house": ..., "sign": "..." },
  "interpretation": { "full_text_passages": [{ "text": "...", "confidence": "..." }] },
  "source": { "primary": "...", "chapter": "...", "batch_id": "..." },
  "validation": {
    "verdict": "flag",
    "flag_reason": "reason Claude flagged this rule",
    "corrected_confidence": "HIGH | MEDIUM | LOW",
    "validated_by": "claude-haiku-4-5"
  }
}
```

### What Codex Must Deliver

**File: `reconcile_flagged.py`**

A standalone Python script that:

1. Connects to MongoDB using `--mongo-url`, `--db-name` CLI args
2. Fetches all rules with `approval_status: "flagged"`, sorted by `source.primary` then `source.chapter` then `rule_id`
3. Groups rules by source book + chapter for context-aware batching (rules from the same chapter are reviewed together so Claude has chapter-level context)
4. For each batch of up to 10 rules from the same chapter, calls Claude with a prompt structured as:

```
You are a Vedic astrology Knowledge Engine editor reviewing flagged interpretation rules.
These rules were flagged during automated validation. Review each and recommend an action.

Source book: {book}
Chapter: {chapter}

For each rule below, recommend:
  approve      — rule is valid as-is; flag was overly cautious
  needs_edit   — rule has merit but needs the specific issue fixed (note what)
  deprecate    — rule is too vague, wrong, or not useful; should be removed

Rules to review:
{numbered list of rule_id + flag_reason + interpretation text}

Respond in JSON array — one object per rule in the same order:
[
  {
    "rule_id": "...",
    "recommendation": "approve | needs_edit | deprecate",
    "reasoning": "one sentence",
    "suggested_edit": "only if needs_edit — specific suggested change, else null"
  }
]
```

5. Writes results to:
   `backend/scripts/reports/horoscope_db_flagged_reconciled.csv`

   Columns:
   ```
   rule_id, book, chapter, batch_id, condition_type, planet, house,
   flag_reason, interpretation_summary, codex_recommendation,
   codex_reasoning, suggested_edit, final_action
   ```
   `final_action` is blank — co-founder fills this column.

6. Streaming writes after each batch — progress saved if interrupted
7. Supports `--resume` flag — skips `rule_id` values already in output CSV
8. Supports `--science-id` and `--batch-id` filters (same pattern as `validate_rules.py`) so specific chapters can be re-run if needed
9. Uses `--model claude-haiku-4-5`

**File: `apply_flagged_decisions.py`**

A second script that:

1. Reads the reconciled CSV (after co-founder has filled `final_action` column)
2. For each row with `final_action` filled:
   - `approve` → sets `approval_status: "auto_approved"`
   - `needs_edit` → sets `approval_status: "pending_human_review"` with `validation.edit_note` = `suggested_edit` value
   - `deprecate` → sets `approval_status: "deprecated"`
3. Dry-run mode by default; `--apply` flag executes writes
4. Prints grouped summary: how many approved / needs_edit / deprecated per source book
5. Validate against Python 3.12

### Acceptance Criteria

- Processes all 1,329 flagged rules without error
- Batching groups rules from the same chapter together correctly
- Resume works — re-running skips already-processed rule_ids
- `apply_flagged_decisions.py` dry-run prints a grouped breakdown before writing
- Output CSV opens correctly in Excel / Numbers / Google Sheets
- Validate against Python 3.12

---

## Shared Technical Constraints

All deliverables must follow these Temple App patterns without exception:

### CLI Pattern (same as validate_rules.py)
```python
parser.add_argument("--mongo-url", required=True)
parser.add_argument("--db-name", required=True)
parser.add_argument("--dry-run", action="store_true")
parser.add_argument("--apply", action="store_true")   # where relevant
parser.add_argument("--resume", action="store_true")  # where relevant
```

### MongoDB Write Pattern (with retry — same as validate_rules.py)
```python
from pymongo.errors import AutoReconnect
import time

for attempt in range(4):
    try:
        db["interpretation_rules"].update_many(
            {"rule_id": rule_id},
            {"$set": {...}}
        )
        break
    except AutoReconnect as exc:
        if attempt < 3:
            wait = 2 ** attempt
            print(f"[retry {attempt+1}/3] MongoDB timeout — retrying in {wait}s")
            time.sleep(wait)
        else:
            raise
```

Note: use `update_many` not `update_one` — the collection has duplicate `rule_id` documents from earlier ingest runs and `update_one` only writes the first match.

### Claude API Pattern
```python
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)
result = response.content[0].text
```

### File Header
```python
#!/usr/bin/env python3
from __future__ import annotations
```

### Python Version
All scripts must be validated against Python 3.12.

### No Temple Imports
No imports from any Temple App source file (`server.py`, `knowledge_engine.py`, `vedic_calculator.py`, etc.).

---

## Delivery Format

Three script pairs delivered as standalone `.py` files:

| File | Deliverable |
|---|---|
| `patch_mars_h03.py` | Item 1 — Mars H03 correction patch |
| `reconcile_contradictions.py` | Item 2 — contradiction first-pass recommendations |
| `apply_contradiction_decisions.py` | Item 2 — apply co-founder decisions |
| `reconcile_flagged.py` | Item 3 — flagged rules first-pass recommendations |
| `apply_flagged_decisions.py` | Item 3 — apply co-founder decisions |

Each file is a fully self-contained script. No shared utility modules. No new pip packages beyond `pymongo` and `anthropic` which are already installed.

---

## Priority Order

1. `patch_mars_h03.py` — highest priority, clears a known documented debt
2. `reconcile_contradictions.py` + `apply_contradiction_decisions.py` — second priority, unblocks the `auto_approved` pool
3. `reconcile_flagged.py` + `apply_flagged_decisions.py` — third priority, largest volume

Deliver in this order if sequencing is needed.
