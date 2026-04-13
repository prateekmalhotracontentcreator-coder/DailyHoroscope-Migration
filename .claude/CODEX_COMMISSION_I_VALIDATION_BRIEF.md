# Codex Brief — Commission I: Automated Rule Validation Engine

> To: Codex
> From: EverydayHoroscope / Temple Team
> Type: Knowledge Engine tooling
> Priority: HIGH — gates Library approval and Knowledge Engine quality
> Depends on: CPath-1 complete ✅, batch_ingest.py complete ✅
> 948 rules currently in MongoDB with approval_status = "pending_review"

---

## Context

The Knowledge Engine rule library has been seeded with 948 rules extracted from
8 Phase 1 books. All rules sit at `approval_status = "pending_review"`. Manual
review of 948 rules is impractical. This brief specifies an automated validation
pipeline that uses Claude (Haiku model — cheap and fast) to:

1. Structurally validate every rule (free — no API call)
2. Batch-evaluate quality and astrological correctness via Claude
3. Detect cross-rule contradictions
4. Auto-approve passing rules and flag problems with one-line reasons
5. Surface only ~20% of rules to humans for final review

Expected cost: ~$0.15 total. Expected runtime: ~3 minutes for 948 rules.

---

## Files to Create / Modify

| File | Action | Purpose |
|---|---|---|
| `backend/scripts/validate_rules.py` | **CREATE** | CLI validation script |
| `backend/knowledge_validator.py` | **CREATE** | Reusable RuleValidator class |
| `backend/knowledge_schema.py` | **MODIFY** | Add `validation` field to `InterpretationRuleDocument` |
| `backend/knowledge_router.py` | **MODIFY** | Add `POST /api/knowledge/validate-batch` endpoint |
| `frontend/src/pages/admin/LibraryConsolePage.jsx` | **MODIFY** | Validation badges + Run Validation button |

---

## 1. `backend/knowledge_schema.py` change

Add a `ValidationResult` model and `validation` field to `InterpretationRuleDocument`.

### 1a. New model — add near other sub-models

```python
class ValidationResult(BaseModel):
    verdict: str = ""                    # "approve" | "spot_check" | "flag" | "structural_fail"
    flag_reason: str = ""
    corrected_confidence: str = ""       # "HIGH" | "MEDIUM" | "LOW"
    validated_by: str = ""               # e.g. "claude-haiku-4-5"
    validated_at: str = ""               # ISO datetime string
    contradiction_ids: list[str] = Field(default_factory=list)
    contradiction_summary: str = ""

    model_config = ConfigDict(extra="ignore")
```

### 1b. Add field to `InterpretationRuleDocument`

Add as the last field, with a default so existing documents are not broken:

```python
validation: ValidationResult = Field(default_factory=ValidationResult)
```

### 1c. Update `_coerce_rules()` coercion helper (if present)

If `_coerce_rules()` calls `.setdefault()` on rule dicts before constructing
`InterpretationRuleDocument`, add:
```python
item.setdefault("validation", {})
```

---

## 2. `backend/knowledge_validator.py` — Reusable class

This module has NO FastAPI or Motor imports. It is imported by both the CLI
script and the router.

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from typing import Any

GARBAGE_RE = re.compile(
    r"(.)\1{6,}|"            # 7+ repeated chars
    r"[^\x00-\x7F]{15,}|"   # 15+ consecutive non-ASCII (OCR artifacts)
    r"\b[A-Z]{20,}\b"        # 20+ char ALL-CAPS token
)

VALIDATION_SYSTEM = (
    "You are a senior Vedic astrology scholar and knowledge engineer. "
    "You evaluate extracted interpretation rules for correctness, coherence, "
    "and faithfulness to classical Vedic texts including BPHS, Phaladeepika, "
    "Lal Kitab, and other authoritative sources."
)

VALIDATION_PROMPT = """\
Evaluate each rule below and return a JSON array — one object per rule.

For each rule assess:
1. CORRECTNESS — consistent with classical Vedic astrology?
2. QUALITY — coherent, specific, usable as a prediction statement?
3. FAITHFULNESS — does it faithfully paraphrase what a classical source would say?

Verdict options:
  "approve"     — correct and ready for production
  "spot_check"  — probably fine but borderline; flag for quick human glance
  "flag"        — incorrect, incoherent, or suspicious

Return ONLY valid JSON — no markdown fences, no commentary:
[
  {{
    "rule_id": "<rule_id>",
    "verdict": "approve" | "spot_check" | "flag",
    "reason": "<one sentence — required for spot_check and flag, empty for approve>",
    "corrected_confidence": "HIGH" | "MEDIUM" | "LOW"
  }}
]

Rules to evaluate:
{rules_json}
"""

CONTRADICTION_PROMPT = """\
Check whether any rules below directly contradict each other.
Different emphasis or wording across books is NOT a contradiction.
A true contradiction is when two rules make opposite factual claims about
the same planetary placement (e.g. one says "gives wealth", another says
"destroys wealth" for identical conditions).

Return ONLY valid JSON — no markdown fences:
[
  {{
    "rule_id_a": "...",
    "rule_id_b": "...",
    "contradiction_summary": "<one sentence>"
  }}
]
Return an empty array [] if no contradictions found.

Rules to compare:
{rules_json}
"""


class RuleValidator:
    def __init__(self, model: str = "claude-haiku-4-5"):
        self.model = model
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                import anthropic  # type: ignore
            except ImportError as exc:
                raise RuntimeError("anthropic package not installed") from exc
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise RuntimeError("ANTHROPIC_API_KEY not set in environment")
            self._client = anthropic.Anthropic(api_key=api_key)
        return self._client

    # ── Structural check (free) ────────────────────────────────────────────

    def structural_check(self, rule: dict) -> tuple[bool, str]:
        interp = rule.get("interpretation") or {}
        detailed = (interp.get("detailed") or "").strip()
        summary  = (interp.get("summary") or "").strip()
        if not detailed and not summary:
            return False, "empty_interpretation"
        text = detailed or summary
        if GARBAGE_RE.search(text):
            return False, "ocr_garbage_detected"
        if len(text.split()) < 8:
            return False, "interpretation_too_short"
        condition = rule.get("condition")
        if not condition or not isinstance(condition, dict):
            return False, "missing_condition"
        return True, "ok"

    # ── Claude quality check ───────────────────────────────────────────────

    def _rule_to_prompt_item(self, rule: dict) -> dict:
        interp = rule.get("interpretation") or {}
        source = rule.get("source") or {}
        return {
            "rule_id": rule.get("rule_id", ""),
            "source_book": source.get("book", ""),
            "chapter": source.get("chapter", ""),
            "condition": rule.get("condition", {}),
            "summary": (interp.get("summary") or "")[:200],
            "detailed": (interp.get("detailed") or "")[:400],
            "current_confidence": rule.get("confidence", "MEDIUM"),
        }

    def _call_claude(self, prompt: str) -> list[dict]:
        client = self._get_client()
        response = client.messages.create(
            model=self.model,
            max_tokens=4096,
            temperature=0.1,
            system=VALIDATION_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.content[0].text.strip() if response.content else "[]"
        # Strip markdown fences if model adds them despite instructions
        content = re.sub(r"^```[a-z]*\n?", "", content)
        content = re.sub(r"\n?```$", "", content)
        try:
            result = json.loads(content)
            return result if isinstance(result, list) else []
        except json.JSONDecodeError:
            return []

    def validate_batch(self, rules: list[dict]) -> list[dict]:
        """
        Returns list of:
        {rule_id, verdict, reason, corrected_confidence}
        """
        if not rules:
            return []
        items = [self._rule_to_prompt_item(r) for r in rules]
        prompt = VALIDATION_PROMPT.format(rules_json=json.dumps(items, indent=2))
        return self._call_claude(prompt)

    def detect_contradictions(self, rules: list[dict]) -> list[dict]:
        """
        Returns list of:
        {rule_id_a, rule_id_b, contradiction_summary}
        """
        if len(rules) < 2:
            return []
        items = [self._rule_to_prompt_item(r) for r in rules]
        prompt = CONTRADICTION_PROMPT.format(rules_json=json.dumps(items, indent=2))
        return self._call_claude(prompt)

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()
```

---

## 3. `backend/scripts/validate_rules.py` — CLI script

### 3a. Full implementation

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from pymongo import MongoClient

SCRIPT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SCRIPT_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from knowledge_validator import RuleValidator


def parse_args():
    parser = argparse.ArgumentParser(
        description="Auto-validate pending_review rules in Knowledge Engine"
    )
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", required=True)
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--science-id", default=None,
                        help="Filter to one science_id (default: all)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print verdicts but do NOT write to MongoDB")
    parser.add_argument("--report-path", default=None,
                        help="Optional path to write Markdown report")
    return parser.parse_args()


def fetch_pending(db, science_id: str | None) -> list[dict]:
    query: dict = {"approval_status": "pending_review"}
    if science_id:
        query["science_id"] = science_id
    return list(db["interpretation_rules"].find(query, {"_id": 0}))


def group_for_contradiction(rules: list[dict]) -> dict[str, list[dict]]:
    """Group rules by (condition_type, planet, house/sign) for contradiction check."""
    groups: dict[str, list[dict]] = defaultdict(list)
    for rule in rules:
        cond = rule.get("condition") or {}
        ctype = cond.get("type", "unknown")
        planet = cond.get("planet", "")
        house  = str(cond.get("house", cond.get("sign", "")))
        key = f"{ctype}|{planet}|{house}"
        groups[key].append(rule)
    return {k: v for k, v in groups.items() if len(v) >= 2}


def apply_verdict(
    db,
    rule_id: str,
    verdict: str,
    reason: str,
    corrected_confidence: str,
    validated_by: str,
    contradiction_ids: list[str],
    contradiction_summary: str,
    dry_run: bool,
) -> str:
    """Returns the final approval_status string."""
    status_map = {
        "approve":          "auto_approved",
        "spot_check":       "pending_human_review",
        "flag":             "flagged",
        "structural_fail":  "rejected",
    }
    new_status = status_map.get(verdict, "pending_review")

    validation_doc = {
        "verdict": verdict,
        "flag_reason": reason,
        "corrected_confidence": corrected_confidence,
        "validated_by": validated_by,
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "contradiction_ids": contradiction_ids,
        "contradiction_summary": contradiction_summary,
    }

    if not dry_run:
        db["interpretation_rules"].update_one(
            {"rule_id": rule_id},
            {"$set": {
                "approval_status": new_status,
                "validation": validation_doc,
            }}
        )
    return new_status


def write_report(path: str, counters: dict, contradictions: list, flagged_sample: list, rejected: list):
    total = sum(counters.values())
    lines = [
        "# Knowledge Engine Validation Report",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Summary",
        "",
        "| Status | Count | % |",
        "|---|---|---|",
    ]
    for status, count in sorted(counters.items(), key=lambda x: -x[1]):
        pct = f"{count/total*100:.0f}%" if total else "0%"
        lines.append(f"| {status} | {count} | {pct} |")
    lines += [f"| **Total** | **{total}** | |", ""]

    if contradictions:
        lines += ["## Contradictions Detected", ""]
        for c in contradictions:
            lines.append(f"- `{c['rule_id_a']}` ↔ `{c['rule_id_b']}`: {c['contradiction_summary']}")
        lines.append("")

    if flagged_sample:
        lines += [f"## Flagged Rules (first {len(flagged_sample)})", "",
                  "| rule_id | book | reason |",
                  "|---|---|---|"]
        for r in flagged_sample:
            source = r.get("source") or {}
            lines.append(f"| {r['rule_id']} | {source.get('book','')} | {r.get('_reason','')} |")
        lines.append("")

    if rejected:
        lines += ["## Rejected Rules (structural failures)", "",
                  "| rule_id | reason |", "|---|---|"]
        for r in rejected:
            lines.append(f"| {r['rule_id']} | {r.get('_reason','')} |")
        lines.append("")

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines), encoding="utf-8")
    print(f"\n  Report written to {path}")


def main():
    args = parse_args()
    client = MongoClient(args.mongo_url)
    db = client[args.db_name]
    validator = RuleValidator(model="claude-haiku-4-5")

    print("\nFetching pending_review rules...")
    rules = fetch_pending(db, args.science_id)
    print(f"Found {len(rules)} rules to validate")
    if not rules:
        print("Nothing to do.")
        return

    counters: dict[str, int] = {}
    all_verdicts: dict[str, dict] = {}   # rule_id → verdict info
    flagged_rules: list[dict] = []
    rejected_rules: list[dict] = []
    all_contradictions: list[dict] = []

    # ── Stage 1: Structural check ──────────────────────────────────────────
    print("\nStage 1: Structural checks...")
    structurally_ok: list[dict] = []
    for rule in rules:
        passed, reason = validator.structural_check(rule)
        if not passed:
            all_verdicts[rule["rule_id"]] = {
                "verdict": "structural_fail", "reason": reason,
                "corrected_confidence": rule.get("confidence", "LOW"),
            }
            rule["_reason"] = reason
            rejected_rules.append(rule)
        else:
            structurally_ok.append(rule)
    print(f"  Structural failures: {len(rejected_rules)} / {len(rules)}")
    print(f"  Proceeding with: {len(structurally_ok)} rules")

    # ── Stage 2: Claude quality check (batched) ────────────────────────────
    print(f"\nStage 2: Claude quality check (batch_size={args.batch_size})...")
    total_batches = (len(structurally_ok) + args.batch_size - 1) // args.batch_size

    for i in range(0, len(structurally_ok), args.batch_size):
        batch = structurally_ok[i: i + args.batch_size]
        batch_num = i // args.batch_size + 1
        print(f"  Batch {batch_num}/{total_batches} ({len(batch)} rules)...", end=" ", flush=True)
        try:
            results = validator.validate_batch(batch)
        except Exception as exc:
            print(f"ERROR: {exc} — marking batch as spot_check")
            results = [{"rule_id": r["rule_id"], "verdict": "spot_check",
                        "reason": f"batch_error: {exc}", "corrected_confidence": "MEDIUM"}
                       for r in batch]

        # Index by rule_id
        result_map = {r["rule_id"]: r for r in results}
        for rule in batch:
            rid = rule["rule_id"]
            res = result_map.get(rid, {
                "rule_id": rid, "verdict": "spot_check",
                "reason": "no_response_from_model", "corrected_confidence": "MEDIUM"
            })
            all_verdicts[rid] = res
        print("done")

    # ── Stage 3: Contradiction detection ──────────────────────────────────
    print("\nStage 3: Contradiction detection...")
    groups = group_for_contradiction(structurally_ok)
    print(f"  {len(groups)} condition groups with ≥2 rules to check")
    for key, group_rules in groups.items():
        try:
            contradictions = validator.detect_contradictions(group_rules)
        except Exception:
            contradictions = []
        all_contradictions.extend(contradictions)

    # Build contradiction lookup: rule_id → [other_rule_ids]
    contra_map: dict[str, list[str]] = defaultdict(list)
    for c in all_contradictions:
        contra_map[c["rule_id_a"]].append(c["rule_id_b"])
        contra_map[c["rule_id_b"]].append(c["rule_id_a"])
    print(f"  Contradictions found: {len(all_contradictions)} pair(s)")

    # ── Stage 4: Write verdicts ────────────────────────────────────────────
    print(f"\nStage 4: {'[DRY RUN] ' if args.dry_run else ''}Writing verdicts...")
    for rule in rules:
        rid = rule["rule_id"]
        v = all_verdicts.get(rid, {"verdict": "spot_check", "reason": "", "corrected_confidence": "MEDIUM"})
        verdict = v.get("verdict", "spot_check")
        reason  = v.get("reason", "")
        conf    = v.get("corrected_confidence", rule.get("confidence", "MEDIUM"))
        contra_ids = contra_map.get(rid, [])
        # Escalate: approved rules with contradictions → spot_check
        if verdict == "approve" and contra_ids:
            verdict = "spot_check"
            reason  = f"Contradicts rule(s): {', '.join(contra_ids)}"
        contra_summary = ""
        for c in all_contradictions:
            if c["rule_id_a"] == rid or c["rule_id_b"] == rid:
                contra_summary = c.get("contradiction_summary", "")
                break
        new_status = apply_verdict(
            db, rid, verdict, reason, conf,
            f"claude-haiku-4-5", contra_ids, contra_summary, args.dry_run
        )
        counters[new_status] = counters.get(new_status, 0) + 1
        if new_status == "flagged":
            rule["_reason"] = reason
            flagged_rules.append(rule)

    # ── Summary ────────────────────────────────────────────────────────────
    total = sum(counters.values())
    print(f"\n{'=' * 55}")
    print(f"{'[DRY RUN] ' if args.dry_run else ''}VALIDATION COMPLETE")
    for status, count in sorted(counters.items(), key=lambda x: -x[1]):
        pct = f"{count/total*100:.0f}%"
        print(f"  {status:<28} {count:>4}  ({pct})")
    print(f"  {'─'*40}")
    print(f"  {'Total':<28} {total:>4}")
    print(f"\n  Contradictions: {len(all_contradictions)} pair(s)")
    if not args.dry_run:
        print(f"\n  auto_approved rules are live after next index refresh.")
        print(f"  Review flagged rules at /admin/library → Rules Browser → filter: flagged")

    if args.report_path:
        write_report(
            args.report_path, counters,
            all_contradictions, flagged_rules[:20], rejected_rules
        )

    client.close()


if __name__ == "__main__":
    main()
```

---

## 4. `backend/knowledge_router.py` — new endpoint

Add one endpoint after the existing `approve-all` route:

```python
@router.post("/validate-batch")
async def validate_batch_endpoint(
    batch_id: str | None = None,
    science_id: str | None = None,
    request: Request = None,
):
    """
    Trigger Claude validation on pending_review rules.
    Optional: filter by batch_id or science_id.
    Runs as a background task — returns immediately.
    """
    db = _db_from_request(request)
    await require_admin(request, db)

    query: dict = {"approval_status": "pending_review"}
    if batch_id:
        query["source.batch_id"] = batch_id
    if science_id:
        query["science_id"] = science_id

    async def _run():
        from knowledge_validator import RuleValidator
        from pymongo import MongoClient
        import os, json
        from datetime import datetime, timezone
        from collections import defaultdict

        mongo_url = os.getenv("MONGO_URL", "")
        db_name   = os.getenv("DB_NAME", "EverydayHoroscope")
        sync_client = MongoClient(mongo_url)
        sync_db = sync_client[db_name]

        rules = list(sync_db["interpretation_rules"].find(query, {"_id": 0}))
        validator = RuleValidator(model="claude-haiku-4-5")

        BATCH = 20
        all_verdicts: dict = {}

        # Structural
        ok_rules = []
        for rule in rules:
            passed, reason = validator.structural_check(rule)
            if not passed:
                all_verdicts[rule["rule_id"]] = {"verdict": "structural_fail", "reason": reason, "corrected_confidence": "LOW"}
            else:
                ok_rules.append(rule)

        # Quality
        for i in range(0, len(ok_rules), BATCH):
            batch = ok_rules[i: i + BATCH]
            try:
                results = validator.validate_batch(batch)
            except Exception as exc:
                results = [{"rule_id": r["rule_id"], "verdict": "spot_check", "reason": str(exc), "corrected_confidence": "MEDIUM"} for r in batch]
            for res in results:
                all_verdicts[res["rule_id"]] = res

        # Contradictions
        from collections import defaultdict
        groups: dict = defaultdict(list)
        for rule in ok_rules:
            cond = rule.get("condition") or {}
            key = f"{cond.get('type','')}|{cond.get('planet','')}|{cond.get('house', cond.get('sign',''))}"
            groups[key].append(rule)
        contra_map: dict = defaultdict(list)
        for key, grp in groups.items():
            if len(grp) >= 2:
                try:
                    pairs = validator.detect_contradictions(grp)
                except Exception:
                    pairs = []
                for p in pairs:
                    contra_map[p["rule_id_a"]].append(p["rule_id_b"])
                    contra_map[p["rule_id_b"]].append(p["rule_id_a"])

        # Write
        status_map = {"approve": "auto_approved", "spot_check": "pending_human_review",
                      "flag": "flagged", "structural_fail": "rejected"}
        now = datetime.now(timezone.utc).isoformat()
        for rule in rules:
            rid = rule["rule_id"]
            v = all_verdicts.get(rid, {"verdict": "spot_check", "reason": "", "corrected_confidence": "MEDIUM"})
            verdict = v.get("verdict", "spot_check")
            reason  = v.get("reason", "")
            conf    = v.get("corrected_confidence", "MEDIUM")
            contra_ids = contra_map.get(rid, [])
            if verdict == "approve" and contra_ids:
                verdict = "spot_check"
                reason  = f"Contradicts: {', '.join(contra_ids)}"
            new_status = status_map.get(verdict, "pending_review")
            sync_db["interpretation_rules"].update_one(
                {"rule_id": rid},
                {"$set": {
                    "approval_status": new_status,
                    "validation": {
                        "verdict": verdict, "flag_reason": reason,
                        "corrected_confidence": conf,
                        "validated_by": "claude-haiku-4-5",
                        "validated_at": now,
                        "contradiction_ids": contra_ids,
                    }
                }}
            )

        sync_client.close()
        schedule_index_refresh()

    import asyncio
    asyncio.create_task(_run())
    return {"status": "validation_started", "message": "Validation running in background. Check Rules Browser in ~3 minutes."}
```

---

## 5. `frontend/src/pages/admin/LibraryConsolePage.jsx` changes

### 5a. Validation status badge helper

Add this helper function inside the component (before the return):

```jsx
function ValidationBadge({ rule }) {
  const status = rule.approval_status;
  const reason = rule.validation?.flag_reason || rule.validation?.contradiction_summary || '';
  const map = {
    auto_approved:        { label: 'Auto-approved', color: 'bg-green-500/15 text-green-400 border-green-500/30' },
    pending_human_review: { label: 'Spot-check',    color: 'bg-amber-500/15 text-amber-400 border-amber-500/30' },
    flagged:              { label: 'Flagged',        color: 'bg-red-500/15 text-red-400 border-red-500/30' },
    rejected:             { label: 'Rejected',       color: 'bg-zinc-500/15 text-zinc-400 border-zinc-500/30' },
    pending_review:       { label: 'Pending',        color: 'bg-blue-500/15 text-blue-400 border-blue-500/30' },
  };
  const cfg = map[status] || map['pending_review'];
  return (
    <span
      className={`inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-medium ${cfg.color}`}
      title={reason || undefined}
    >
      {cfg.label}
    </span>
  );
}
```

### 5b. "Run Validation" button in Import Batches tab

In the Import Batches tab, add a button next to each batch's "Approve All":

```jsx
<button
  onClick={async () => {
    try {
      const headers = getAuthHeaders();
      const res = await fetch(
        `${backendUrl}/api/knowledge/validate-batch?batch_id=${encodeURIComponent(batch.batch_id)}`,
        { method: 'POST', headers }
      );
      const data = await res.json();
      alert(data.message || 'Validation started — check Rules Browser in ~3 minutes.');
    } catch (err) {
      alert('Validation request failed: ' + err.message);
    }
  }}
  className="rounded-lg border border-indigo-500/30 bg-indigo-500/10 px-3 py-1.5 text-xs text-indigo-400 hover:bg-indigo-500/20"
>
  Run Validation
</button>
```

### 5c. Add `ValidationBadge` to Rules Browser rows

In the Rules Browser tab, wherever the rule approval_status is displayed,
replace the plain text with `<ValidationBadge rule={rule} />`.

Also add a filter dropdown above the rules list:

```jsx
<select
  value={statusFilter}
  onChange={e => setStatusFilter(e.target.value)}
  className="rounded-lg border border-gold/20 bg-card px-3 py-1.5 text-sm text-foreground"
>
  <option value="">All statuses</option>
  <option value="pending_review">Pending</option>
  <option value="auto_approved">Auto-approved</option>
  <option value="pending_human_review">Spot-check</option>
  <option value="flagged">Flagged</option>
  <option value="rejected">Rejected</option>
</select>
```

Use `statusFilter` state to filter the displayed rules client-side.

---

## 6. Constraints

- `knowledge_validator.py` has NO fastapi / motor imports — pure stdlib + anthropic
- `validate_rules.py` has NO fastapi / motor imports — uses sync pymongo only
- Model is `claude-haiku-4-5` — NOT Sonnet (cost control)
- `ANTHROPIC_API_KEY` must be in environment for Claude calls
- Structural check always runs first — failures never reach Claude (saves cost)
- `--dry-run` writes nothing to MongoDB
- Background task in router uses sync pymongo in a thread-safe way (not Motor)
- `ValidationResult` model uses `extra="ignore"` so old rules without the field load cleanly
- `schedule_index_refresh()` called after background task completes

---

## 7. Validation Checklist (Codex self-check)

- [ ] `knowledge_validator.py` has no FastAPI/Motor imports
- [ ] `validate_rules.py` has no FastAPI/Motor imports
- [ ] `sys.path` setup in `validate_rules.py` comes before local imports
- [ ] Structural check runs before any Claude API call
- [ ] Batch loop handles Claude API errors gracefully (falls back to `spot_check`)
- [ ] Contradiction detection only runs on groups with ≥2 rules
- [ ] Approved rules with contradictions are escalated to `spot_check`
- [ ] `--dry-run` skips all MongoDB writes
- [ ] `ValidationResult` added to `InterpretationRuleDocument` with default
- [ ] `_coerce_rules()` updated with `item.setdefault("validation", {})`
- [ ] `/validate-batch` endpoint runs as `asyncio.create_task` (non-blocking)
- [ ] `ValidationBadge` component uses `title` prop to show reason on hover
- [ ] Status filter dropdown added to Rules Browser
- [ ] `Run Validation` button calls correct endpoint with batch_id param

---

## 8. Usage — What Prateek Will Run

```bash
cd /path/to/DailyHoroscope-Migration/backend
source .venv/bin/activate

export ANTHROPIC_API_KEY=sk-ant-...
export MONGO_URL="mongodb+srv://..."
export DB_NAME="EverydayHoroscope"

# Dry run first — see verdicts without touching MongoDB
python scripts/validate_rules.py \
  --mongo-url "$MONGO_URL" \
  --db-name "$DB_NAME" \
  --report-path ./output/validation_report.md \
  --dry-run

# Real run — auto-approve + flag in one shot (~3 minutes)
python scripts/validate_rules.py \
  --mongo-url "$MONGO_URL" \
  --db-name "$DB_NAME" \
  --report-path ./output/validation_report.md

# Then open /admin/library → Rules Browser → filter "Flagged"
# Review ~100-150 rules with Claude's one-line reason attached
# Approve or reject each — done.
```
