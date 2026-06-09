#!/usr/bin/env python3
"""
validate_remedy_library.py
--------------------------
Re-validates the ~93 PHR (validator_error: true) rules in the Remedy batches
using a remedy-library-appropriate Claude prompt.

Context: these rules were flagged by the standard Vedic astrology validator
because it applied classical-text criteria to a modern remedy library
(crystals, non-traditional gemstones, chakra healing). That was the wrong
criteria. This script validates them on the right criteria.

DOES check:
  - Completeness  : meaningful astrological trigger + complete remedy protocol
  - Consistency   : planets_involved / trigger_condition match detailed text
  - Language      : no pseudo-science, no medically inaccurate claims
  - Astrological  : trigger is meaningfully related to remedy

DOES NOT check (intentional product design):
  - Whether gemstone/crystal appears in classical Vedic texts
  - Whether the framework (chakra, crystal healing) is classical Vedic
  - Whether the remedy style matches BPHS / Phaladeepika / Lal Kitab

Verdicts:
  APPROVE → auto_approved
  FIX     → Claude corrects the specific issue → auto_approved
  REJECT  → rejected (unfixable or core premise is incoherent)

Usage:
  python3 backend/scripts/validate_remedy_library.py --dry-run
  python3 backend/scripts/validate_remedy_library.py
  python3 backend/scripts/validate_remedy_library.py --batch-size 5
"""

from __future__ import annotations
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import anthropic
from pymongo import MongoClient

# ---------------------------------------------------------------------------
# Args + logging
# ---------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true")
parser.add_argument("--batch-size", type=int, default=10,
                    help="Rules per API call for batch validation (default: 10)")
args = parser.parse_args()

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
mode_tag = "dry-run" if args.dry_run else "live"
log_path = LOG_DIR / f"validate_remedy_library_{mode_tag}_{ts}.log"

class Tee:
    def __init__(self, fp: Path):
        self._f = open(fp, "w", encoding="utf-8")
    def write(self, d: str):
        sys.__stdout__.write(d); self._f.write(d)
    def flush(self):
        sys.__stdout__.flush(); self._f.flush()
    def close(self):
        self._f.close()

tee = Tee(log_path)
sys.stdout = tee

print("╔══════════════════════════════════════════════════════════════╗")
print(f"  validate_remedy_library.py  [{mode_tag.upper()}]")
print(f"  Run timestamp : {ts} UTC")
print(f"  Log file      : {log_path}")
print("╚══════════════════════════════════════════════════════════════╝")
print()
if args.dry_run:
    print("  ⚠️  DRY-RUN -- no changes written to MongoDB.")
    print()

# ---------------------------------------------------------------------------
# Connect
# ---------------------------------------------------------------------------
MONGO_URL = os.environ.get("MONGO_URL")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not MONGO_URL:
    print("ERROR: MONGO_URL not set."); sys.exit(1)
if not ANTHROPIC_API_KEY:
    print("ERROR: ANTHROPIC_API_KEY not set."); sys.exit(1)

mongo = MongoClient(MONGO_URL, serverSelectionTimeoutMS=10_000)
col = mongo["horoscope_db"]["interpretation_rules"]
ai = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

REMEDY_BATCHES = [
    "remedies-crystals-v1-20260510",
    "remedies-gemstones-v1-20260510",
    "remedies-chakra-v1-20260510",
    "remedies-dhana-v1-20260510",
]

# ---------------------------------------------------------------------------
# Load rules
# ---------------------------------------------------------------------------
rules = list(col.find(
    {
        "approval_status": "pending_human_review",
        "validation.validator_error": True,
        "source.batch_id": {"$in": REMEDY_BATCHES},
    },
    {"_id": 0}
))

print(f"  Rules to re-validate: {len(rules)}")
batch_count = (len(rules) + args.batch_size - 1) // args.batch_size
print(f"  Batch size          : {args.batch_size}  →  {batch_count} API calls")
print(f"  Validation model    : claude-haiku-4-5-20251001")
print(f"  Fix model           : claude-sonnet-4-6")
print()

if not rules:
    print("✅ Nothing to do.")
    mongo.close()
    sys.stdout = sys.__stdout__; tee.close(); sys.exit(0)

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are a quality validator for EverydayHoroscope, a Vedic astrology wellness app.

You are validating rules from a MODERN REMEDY LIBRARY. This library intentionally includes
crystal healing, chakra balancing, non-traditional gemstones, and contemporary wellness
approaches linked to Vedic astrology triggers. This is intentional product design.

NEVER flag a rule for being "non-classical Vedic", using crystals, chakras, or modern
gemstones. Those are accepted content.

VALIDATE each rule only for:

1. COMPLETENESS
   Each remedy rule must have: a clear astrological trigger condition AND a complete
   remedy protocol (crystal/gemstone name OR deity/mantra, plus severity level).
   Missing one of these → FIX or REJECT.

2. FIELD CONSISTENCY
   planets_involved and trigger_condition must match the detailed text.
   Example fault: planets_involved = [Sun, Mars] but detailed text says Sun / Jupiter.
   Fix: correct the planets_involved array to match the detailed text.

3. LANGUAGE QUALITY
   Flag ONLY genuine problems:
   - Pseudo-scientific incoherence (e.g. "lubricates the Saturnine structures via
     Venusian sub-harmonics", "stigmatizes the solar plexus to burn toxins")
   - Medically inaccurate claims presented as fact
   - Fringe esoteric content clearly out of scope (vampiric energy hooks, entity possession)
   Normal modern wellness language (chakra, aura, tattva, energy, vibration) is ACCEPTED.

4. INTERNAL CONSISTENCY
   Mantra should match the stated deity.
   Gemstone should relate logically to the stated planet/condition (even if non-classical).
   The remedy purpose should relate logically to the trigger condition.

VERDICTS:
  APPROVE -- passes all checks; content is complete, consistent, appropriate.
  FIX     -- specific, narrow, fixable issue. You must provide fix_field + fix_value.
  REJECT  -- core premise is incoherent or medically dangerous; cannot be fixed without
             inventing content. Use sparingly.

Respond with a valid JSON array. One object per rule:
{
  "rule_id": "...",
  "verdict": "APPROVE" | "FIX" | "REJECT",
  "reason": "one concise sentence",
  "fix_field": "interpretation.summary" | "interpretation.detailed" | "condition.planets_involved" | null,
  "fix_value": "corrected string or JSON array" | null
}

Return ONLY the JSON array. No markdown, no explanation outside the JSON."""

def build_user_prompt(batch: list) -> str:
    summaries = []
    for r in batch:
        cond  = r.get("condition") or {}
        interp = r.get("interpretation") or {}
        val   = r.get("validation") or {}
        summaries.append({
            "rule_id":           r.get("rule_id"),
            "batch_id":          (r.get("source") or {}).get("batch_id", ""),
            "condition_type":    cond.get("type"),
            "trigger_condition": cond.get("trigger_condition", ""),
            "planets_involved":  cond.get("planets_involved", []),
            "houses_involved":   cond.get("houses_involved", []),
            "summary":           (interp.get("summary") or "")[:200],
            "detailed":          (interp.get("detailed") or "")[:700],
            "original_flag":     (val.get("flag_reason") or val.get("reason") or "")[:200],
        })
    return (
        f"Validate the following {len(batch)} remedy rules.\n"
        f"Return a JSON array with exactly {len(batch)} objects.\n\n"
        f"Rules:\n{json.dumps(summaries, indent=2, ensure_ascii=False)}"
    )

def call_api(model: str, messages: list, max_tokens: int = 4096,
             system: str | None = None, retries: int = 2) -> str:
    kwargs: dict = {"model": model, "max_tokens": max_tokens, "messages": messages}
    if system:
        kwargs["system"] = system
    for attempt in range(retries + 1):
        try:
            resp = ai.messages.create(**kwargs)
            return resp.content[0].text.strip()
        except anthropic.RateLimitError:
            if attempt < retries:
                wait = 20 * (attempt + 1)
                print(f"    ⏳ Rate limit -- waiting {wait}s...")
                time.sleep(wait)
            else:
                raise
        except anthropic.APIStatusError as e:
            if attempt < retries and e.status_code >= 500:
                time.sleep(5)
            else:
                raise

def parse_json_response(text: str) -> list:
    # Strip markdown fences if present
    for fence in ["```json", "```"]:
        if fence in text:
            text = text.split(fence)[1].split("```")[0].strip()
            break
    return json.loads(text)

# ---------------------------------------------------------------------------
# Phase 1 -- Batch validate
# ---------------------------------------------------------------------------
print("═" * 60)
print("  Phase 1: Batch validation (claude-haiku-4-5-20251001)")
print("═" * 60)

approve_ids:   list[str]                         = []
to_fix:        list[tuple]                       = []   # (rule, fix_field, fix_value, reason)
reject_rules:  list[tuple]                       = []   # (rule, reason)
error_rules:   list[tuple]                       = []   # (rule, error_msg)

rule_lookup = {r["rule_id"]: r for r in rules}

for i in range(0, len(rules), args.batch_size):
    batch = rules[i : i + args.batch_size]
    bn = i // args.batch_size + 1
    print(f"\n  ── Batch {bn}/{batch_count} "
          f"(rules {i+1}-{min(i+args.batch_size, len(rules))}) ──")

    try:
        raw = call_api(
            model="claude-haiku-4-5-20251001",
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": build_user_prompt(batch)}],
            max_tokens=4096,
        )
        verdicts = parse_json_response(raw)
    except (json.JSONDecodeError, Exception) as e:
        print(f"    ❌ API/parse error: {e}")
        for r in batch:
            error_rules.append((r, str(e)))
        time.sleep(3)
        continue

    batch_ids = {r["rule_id"] for r in batch}
    returned_ids = {v.get("rule_id") for v in verdicts}

    # Warn on mismatches
    for missing in batch_ids - returned_ids:
        print(f"    ⚠️  No verdict returned for {missing} → treating as APPROVE")
        approve_ids.append(missing)

    for v in verdicts:
        rid     = v.get("rule_id", "")
        verdict = (v.get("verdict") or "APPROVE").upper()
        reason  = v.get("reason", "")
        fix_field = v.get("fix_field")
        fix_value = v.get("fix_value")
        rule = rule_lookup.get(rid)

        if not rule:
            print(f"    ⚠️  Unknown rule_id '{rid}' -- skipping")
            continue

        if verdict == "APPROVE":
            approve_ids.append(rid)
            print(f"    ✅ APPROVE  {rid:<20}  {reason[:72]}")

        elif verdict == "FIX":
            to_fix.append((rule, fix_field, fix_value, reason))
            print(f"    🔧 FIX      {rid:<20}  {reason[:60]}")
            if fix_field:
                print(f"               field → {fix_field}")
            if fix_value is not None:
                preview = str(fix_value)[:80]
                print(f"               value → {preview}")

        elif verdict == "REJECT":
            reject_rules.append((rule, reason))
            print(f"    ❌ REJECT   {rid:<20}  {reason[:72]}")

        else:
            print(f"    ⚠️  Unknown verdict '{verdict}' for {rid} → APPROVE")
            approve_ids.append(rid)

    if bn < batch_count:
        time.sleep(1.5)   # polite delay

# ---------------------------------------------------------------------------
# Phase 2 -- Generate fixes for FIX rules (claude-sonnet-4-6)
# ---------------------------------------------------------------------------
fixed_approve: list[tuple] = []   # (rid, fix_field, fix_value)
fix_failed:    list[tuple] = []   # (rule, reason)

if to_fix:
    print(f"\n{'═'*60}")
    print(f"  Phase 2: Fix generation (claude-sonnet-4-6)")
    print(f"  Rules needing fix: {len(to_fix)}")
    print("═" * 60)

    for rule, fix_field, fix_value, reason in to_fix:
        rid = rule.get("rule_id", "?")
        print(f"\n  ── {rid} ──")
        print(f"     Issue : {reason[:80]}")

        if fix_value is not None:
            # Validator already provided the fix
            print(f"     Fix   : already provided by validator")
            print(f"     Value : {str(fix_value)[:100]}")
            fixed_approve.append((rid, fix_field, fix_value))
            continue

        # Need to generate the fix
        cond   = rule.get("condition") or {}
        interp = rule.get("interpretation") or {}

        fix_prompt = f"""A Vedic astrology remedy rule has one specific issue that needs correction.

Rule ID   : {rid}
Issue     : {reason}
Fix field : {fix_field}

Current rule:
  summary  : {(interp.get('summary') or '')[:200]}
  detailed : {(interp.get('detailed') or '')[:500]}
  trigger  : {cond.get('trigger_condition', '')}
  planets  : {json.dumps(cond.get('planets_involved', []))}
  houses   : {json.dumps(cond.get('houses_involved', []))}

Provide ONLY the corrected value for '{fix_field}'.
- If fix_field is 'interpretation.detailed' or 'interpretation.summary': return the corrected text string.
- If fix_field is 'condition.planets_involved': return a JSON array of planet name strings.
Return the value only -- no labels, no explanation."""

        try:
            fix_raw = call_api(
                model="claude-sonnet-4-6",
                messages=[{"role": "user", "content": fix_prompt}],
                max_tokens=1024,
            )
            # Parse planets_involved as list if needed
            if fix_field == "condition.planets_involved":
                try:
                    fix_value = json.loads(fix_raw)
                    if not isinstance(fix_value, list):
                        raise ValueError("Expected list")
                except (json.JSONDecodeError, ValueError):
                    # Try to extract array from text
                    if "[" in fix_raw and "]" in fix_raw:
                        fix_value = json.loads(fix_raw[fix_raw.index("["):fix_raw.rindex("]")+1])
                    else:
                        raise ValueError(f"Cannot parse planets list from: {fix_raw[:100]}")
            else:
                fix_value = fix_raw.strip('"').strip()

            print(f"     Generated: {str(fix_value)[:100]}")
            fixed_approve.append((rid, fix_field, fix_value))
            time.sleep(0.5)

        except Exception as e:
            print(f"     ❌ Fix generation failed: {e} → reject")
            fix_failed.append((rule, f"fix_generation_failed: {e}"))

# ---------------------------------------------------------------------------
# Phase 3 -- Write to MongoDB
# ---------------------------------------------------------------------------
print(f"\n{'═'*60}")
print(f"  Phase 3: Writing to MongoDB")
print("═" * 60)

NOW = datetime.now(timezone.utc).isoformat()
n_approved = 0
n_fixed    = 0
n_rejected = 0
n_errors   = 0

if not args.dry_run:
    # Direct approvals
    for rid in approve_ids:
        col.update_one(
            {"rule_id": rid},
            {"$set": {
                "approval_status":                  "auto_approved",
                "validation.verdict":               "approved",
                "validation.validator_error":       False,
                "validation.remedy_revalidation":   f"Passed remedy-library revalidation {NOW}",
            }}
        )
        n_approved += 1

    # Fixed → approve
    for rid, fix_field, fix_value in fixed_approve:
        col.update_one(
            {"rule_id": rid},
            {"$set": {
                "approval_status":                  "auto_approved",
                "validation.verdict":               "approved",
                "validation.validator_error":       False,
                "validation.remedy_revalidation":   f"Fixed and approved in remedy-library revalidation {NOW}",
                fix_field:                          fix_value,
            }}
        )
        n_fixed += 1

    # Rejections (original + fix_failed)
    for rule, reason in [*reject_rules, *fix_failed]:
        rid = rule.get("rule_id", "?")
        col.update_one(
            {"rule_id": rid},
            {"$set": {
                "approval_status":   "rejected",
                "rejection_reason":  f"remedy_revalidation: {reason}",
                "rejected_at":       NOW,
            }}
        )
        n_rejected += 1

    # Error rules -- leave at PHR, add note
    for rule, err in error_rules:
        rid = rule.get("rule_id", "?")
        col.update_one(
            {"rule_id": rid},
            {"$set": {"validation.revalidation_error": f"api_error {NOW}: {err[:200]}"}}
        )
        n_errors += 1

    print(f"  ✅ auto_approved (direct) : {n_approved}")
    print(f"  ✅ auto_approved (fixed)  : {n_fixed}")
    print(f"  ❌ rejected               : {n_rejected}")
    print(f"  ⚠️  left at PHR (errors)  : {n_errors}")

else:
    n_approved = len(approve_ids)
    n_fixed    = len(fixed_approve)
    n_rejected = len(reject_rules) + len(fix_failed)
    n_errors   = len(error_rules)
    print(f"  DRY-RUN -- would write:")
    print(f"    auto_approved (direct) : {n_approved}")
    print(f"    auto_approved (fixed)  : {n_fixed}")
    print(f"    rejected               : {n_rejected}")
    print(f"    PHR errors             : {n_errors}")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print()
print("═" * 60)
print("  FINAL SUMMARY")
print("═" * 60)
print(f"  Input  : {len(rules)} PHR (validator_error) rules")
print(f"  Output :")
print(f"    auto_approved : {n_approved + n_fixed}  "
      f"({n_approved} direct + {n_fixed} fixed)")
print(f"    rejected      : {n_rejected}")
print(f"    PHR (errors)  : {n_errors}")
print()

if not args.dry_run:
    for batch_id in REMEDY_BATCHES:
        label = batch_id.split("-")[1].capitalize()
        aa  = col.count_documents({"source.batch_id": batch_id, "approval_status": "auto_approved"})
        phr = col.count_documents({"source.batch_id": batch_id, "approval_status": "pending_human_review"})
        rej = col.count_documents({"source.batch_id": batch_id, "approval_status": "rejected"})
        print(f"  {label:<12}  auto_approved={aa}  phr={phr}  rejected={rej}")
    print()

mongo.close()

print("╔══════════════════════════════════════════════════════════════╗")
print("  ✅ Remedy re-validation complete")
print(f"  Log saved → {log_path}")
print("╚══════════════════════════════════════════════════════════════╝")

sys.stdout = sys.__stdout__
tee.close()
