#!/usr/bin/env python3
"""
validate_bucket_c_remedies.py
------------------------------
Validates and remediates the 42 Bucket C flagged rules in the Remedy batches.

Bucket C = genuine data issues that the triage script (triage_remedies_flagged.py)
identified as needing human or AI review rather than just a framework-mismatch
promotion. These stayed at approval_status='flagged'.

Issue types in Bucket C:
  1. FIELD MISMATCH   -- planets_involved or houses_involved doesn't match trigger_condition text
  2. FACTUAL ERROR    -- e.g. "Jupiter exalted in 12th" (correct: Cancer)
  3. TRUNCATED TEXT   -- detailed text cut off mid-sentence
  4. START DAY ERROR  -- wrong weekday for the remedy planet (e.g. Saturn → Saturday, not Tuesday)
  5. ESOTERIC LANG    -- "vampiric energy hooks", "entity possession" -- rewrite to wellness framing
  6. DOCTRINAL CONTRA -- remedy contradicts classical principle, but rule may be internally consistent
  7. NON-STANDARD YOG -- combo remedy not found in classical texts (acceptable in modern library)

Strategy per issue type:
  - FIELD MISMATCH   → FIX: read trigger_condition text, derive correct array, set fix_field
  - FACTUAL ERROR    → FIX: correct the factual claim in detailed text
  - TRUNCATED TEXT   → FIX: complete the sentence based on rule intent
  - START DAY ERROR  → FIX: correct the start_day
  - ESOTERIC LANG    → FIX: rewrite the sentence/phrase to equivalent wellness framing
  - DOCTRINAL CONTRA → APPROVE if internally consistent; REJECT only if remedy contradicts
                       the trigger condition itself (not just classical doctrine)
  - NON-STANDARD YOG → APPROVE (modern library, intentional product design)

Verdicts:
  APPROVE → auto_approved
  FIX     → apply fix(es) → auto_approved
  REJECT  → rejected (core premise incoherent or trigger/remedy self-contradict)

Usage:
  python3 backend/scripts/validate_bucket_c_remedies.py --dry-run
  python3 backend/scripts/validate_bucket_c_remedies.py
  python3 backend/scripts/validate_bucket_c_remedies.py --batch-size 7
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
parser.add_argument("--batch-size", type=int, default=7,
                    help="Rules per API call (default: 7 -- Bucket C rules need more tokens)")
args = parser.parse_args()

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
mode_tag = "dry-run" if args.dry_run else "live"
log_path = LOG_DIR / f"validate_bucket_c_remedies_{mode_tag}_{ts}.log"

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
print(f"  validate_bucket_c_remedies.py  [{mode_tag.upper()}]")
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
ai  = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

REMEDY_BATCHES = [
    "remedies-crystals-v1-20260510",
    "remedies-gemstones-v1-20260510",
    "remedies-chakra-v1-20260510",
    "remedies-dhana-v1-20260510",
]

# ---------------------------------------------------------------------------
# Load rules -- Bucket C: still at 'flagged', NOT promoted to PHR
# ---------------------------------------------------------------------------
rules = list(col.find(
    {
        "approval_status": "flagged",
        "source.batch_id": {"$in": REMEDY_BATCHES},
    },
    {"_id": 0}
))

print(f"  Flagged Bucket C rules found : {len(rules)}")
batch_count = (len(rules) + args.batch_size - 1) // args.batch_size if rules else 0
print(f"  Batch size                   : {args.batch_size}  →  {batch_count} API calls")
print(f"  Validation model             : claude-haiku-4-5-20251001")
print(f"  Fix generation model         : claude-sonnet-4-6")
print()

if not rules:
    print("✅ Nothing to do -- no flagged rules in Remedy batches.")
    mongo.close()
    sys.stdout = sys.__stdout__; tee.close(); sys.exit(0)

# Show breakdown by batch
for bid in REMEDY_BATCHES:
    label = bid.split("-")[1].capitalize()
    batch_rules = [r for r in rules if (r.get("source") or {}).get("batch_id") == bid]
    print(f"  {label:<12} : {len(batch_rules)} flagged rules")
print()

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are a quality remediation specialist for EverydayHoroscope, a Vedic
astrology wellness app. You are reviewing FLAGGED remedy rules from a modern remedy library.

This library intentionally includes crystal healing, chakra balancing, non-traditional
gemstones, and contemporary wellness approaches linked to Vedic astrology triggers.
These are accepted product design choices -- never reject a rule for being non-classical.

EACH RULE WAS FLAGGED for a specific data quality issue. Your job is to:
  1. Understand the rule's INTENT from the trigger_condition and detailed text
  2. FIX the specific issue(s) identified in the flag_reason
  3. APPROVE if the rule is already sound or after fixing
  4. REJECT ONLY if the trigger condition and the remedy self-contradict (e.g. remedy
     promises to strengthen what the trigger says is the malefic), or if the content
     is genuinely medically dangerous or incoherent beyond repair

ISSUE TYPES AND HOW TO FIX THEM:

FIELD MISMATCH (planets_involved / houses_involved don't match trigger text)
→ Read trigger_condition carefully. Derive the correct array from the text.
  Fix fix_field="condition.planets_involved" or "condition.houses_involved".
  Return the corrected JSON array as fix_value.
  If BOTH need fixing, return two entries in the "fixes" array.

FACTUAL ERROR (e.g. "Jupiter exalted in 12th" -- Jupiter is exalted in Cancer)
→ Correct the factual claim in interpretation.detailed.
  Return the full corrected detailed text as fix_value.

TRUNCATED TEXT (detailed text ends mid-sentence or mid-word)
→ Complete the text logically based on the rule's stated intent.
  Return the completed text as fix_value for fix_field="interpretation.detailed".

START DAY ERROR (wrong weekday for the remedy planet)
  Planet → Correct day: Sun=Sunday, Moon=Monday, Mars=Tuesday, Mercury=Wednesday,
  Jupiter=Thursday, Venus=Friday, Saturn=Saturday, Rahu/Ketu=Saturday
→ Return fix_field="interpretation.start_day" with the correct day string.
  If the MANTRA also doesn't match the deity, also fix interpretation.mantra.

ESOTERIC LANGUAGE (vampiric, entity, psychic attack, ghost, aura sealing)
→ Rewrite ONLY the specific sentence(s) to equivalent wellness framing.
  Examples: "vampiric energy hooks" → "draining emotional entanglements"
           "entity possession risk" → "energetic boundary depletion"
           "psychic cold" → "energetic sensitivity overload"
           "aura sealing" → "energetic field stabilization"
  Keep the remedy prescription (crystal, mantra, duration) exactly the same.
  Return fix_field="interpretation.detailed" with the full rewritten text.

DOCTRINAL CONTRADICTION (remedy contradicts classical principle)
→ APPROVE if the rule is internally consistent (trigger makes sense + remedy addresses it).
  The fact that a classical Vedic scholar would disagree is NOT a reason to reject.
  REJECT only if the trigger and remedy directly contradict each other within the rule.

NON-STANDARD COMBO / TERMINOLOGY
→ APPROVE if the combination has coherent internal logic for a modern remedy library.
  If terminology is genuinely obscure (e.g. "Shanda degrees"), rewrite to describe
  the condition plainly in fix_field="interpretation.detailed".

RESPONSE FORMAT -- return a valid JSON array, one object per rule:
{
  "rule_id": "...",
  "verdict": "APPROVE" | "FIX" | "REJECT",
  "reason": "one concise sentence explaining the decision",
  "fixes": [
    {"fix_field": "condition.planets_involved", "fix_value": ["Mars", "Saturn"]},
    {"fix_field": "condition.houses_involved", "fix_value": [1, 7]},
    {"fix_field": "interpretation.detailed", "fix_value": "corrected full text"},
    {"fix_field": "interpretation.start_day", "fix_value": "Saturday"}
  ]
}

For APPROVE or REJECT: "fixes" should be [] or omitted.
For FIX: "fixes" must contain at least one entry with fix_field + fix_value.
  fix_value for array fields (planets_involved, houses_involved) must be a JSON array.
  fix_value for text fields must be the complete corrected string.
  Do NOT include fix_field without fix_value.

Return ONLY the JSON array. No markdown, no explanation outside the JSON."""


def build_user_prompt(batch: list) -> str:
    summaries = []
    for r in batch:
        cond   = r.get("condition") or {}
        interp = r.get("interpretation") or {}
        val    = r.get("validation") or {}
        summaries.append({
            "rule_id":           r.get("rule_id"),
            "batch_id":          (r.get("source") or {}).get("batch_id", ""),
            "flag_reason":       (val.get("flag_reason") or val.get("reason") or "")[:300],
            "trigger_condition": cond.get("trigger_condition", ""),
            "planets_involved":  cond.get("planets_involved", []),
            "houses_involved":   cond.get("houses_involved", []),
            "condition_type":    cond.get("type"),
            "summary":           (interp.get("summary") or "")[:200],
            "detailed":          (interp.get("detailed") or "")[:800],
            "start_day":         interp.get("start_day", ""),
            "mantra":            (interp.get("mantra") or "")[:100],
        })
    return (
        f"Validate and fix the following {len(batch)} flagged remedy rules.\n"
        f"Each rule has a flag_reason explaining what was flagged.\n"
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
    for fence in ["```json", "```"]:
        if fence in text:
            text = text.split(fence)[1].split("```")[0].strip()
            break
    return json.loads(text)


# Normalise bare field names → dot-notation paths for MongoDB $set
FIELD_PATH_MAP = {
    "trigger_condition":  "condition.trigger_condition",
    "planets_involved":   "condition.planets_involved",
    "houses_involved":    "condition.houses_involved",
    "start_day":          "interpretation.start_day",
    "mantra":             "interpretation.mantra",
    "summary":            "interpretation.summary",
    "detailed":           "interpretation.detailed",
    "gemstone":           "interpretation.gemstone",
}

def normalise_fix_field(fix_field: str) -> str:
    """Convert bare field name to dot-notation path if needed."""
    return FIELD_PATH_MAP.get(fix_field, fix_field)


def normalise_fix_value(fix_field: str, raw_value) -> object:
    """Ensure fix_value is the right Python type for the given field."""
    array_fields = {"condition.planets_involved", "condition.houses_involved"}
    if fix_field in array_fields:
        if isinstance(raw_value, list):
            return raw_value
        if isinstance(raw_value, str):
            try:
                parsed = json.loads(raw_value)
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                pass
            # Try to extract array from freeform text
            if "[" in raw_value and "]" in raw_value:
                try:
                    return json.loads(raw_value[raw_value.index("["):raw_value.rindex("]")+1])
                except json.JSONDecodeError:
                    pass
        raise ValueError(f"Cannot parse array from fix_value for {fix_field}: {str(raw_value)[:100]}")
    # Text field -- return as string
    if isinstance(raw_value, str):
        return raw_value.strip().strip('"')
    return str(raw_value)


# ---------------------------------------------------------------------------
# Phase 1 -- Batch validate
# ---------------------------------------------------------------------------
print("═" * 64)
print("  Phase 1: Batch validation (claude-haiku-4-5-20251001)")
print("═" * 64)

# Each entry: (rule, list_of_(fix_field, fix_value))
approve_ids:  list[str]   = []
to_fix:       list[tuple] = []   # (rule, [(fix_field, fix_value)], reason)
reject_rules: list[tuple] = []   # (rule, reason)
error_rules:  list[tuple] = []   # (rule, error_msg)
needs_sonnet: list[tuple] = []   # (rule, [(fix_field, None)], reason) -- fix_value missing

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

    batch_ids    = {r["rule_id"] for r in batch}
    returned_ids = {v.get("rule_id") for v in verdicts}

    for missing in batch_ids - returned_ids:
        print(f"    ⚠️  No verdict for {missing} → APPROVE (conservative)")
        approve_ids.append(missing)

    for v in verdicts:
        rid     = v.get("rule_id", "")
        verdict = (v.get("verdict") or "APPROVE").upper()
        reason  = v.get("reason", "")
        rule    = rule_lookup.get(rid)

        if not rule:
            print(f"    ⚠️  Unknown rule_id '{rid}' -- skipping")
            continue

        if verdict == "APPROVE":
            approve_ids.append(rid)
            print(f"    ✅ APPROVE  {rid:<20}  {reason[:70]}")

        elif verdict == "FIX":
            # Parse the "fixes" array (new format) or fall back to fix_field/fix_value
            raw_fixes = v.get("fixes") or []
            if not raw_fixes:
                # Backward-compat: single fix_field/fix_value
                ff = normalise_fix_field(v.get("fix_field") or "")
                fv = v.get("fix_value")
                if ff:
                    raw_fixes = [{"fix_field": ff, "fix_value": fv}]

            if not raw_fixes:
                # Verdict is FIX but no fix info -- queue for Sonnet
                print(f"    🔧 FIX      {rid:<20}  {reason[:60]}  [no fix provided → Sonnet]")
                needs_sonnet.append((rule, [], reason))
                continue

            parsed_fixes = []
            sonnet_needed = False
            for fix_entry in raw_fixes:
                ff = normalise_fix_field(fix_entry.get("fix_field") or "")
                fv = fix_entry.get("fix_value")
                if not ff:
                    continue
                if fv is None:
                    print(f"               ⚠️  {ff} has no fix_value → Sonnet")
                    sonnet_needed = True
                    continue
                try:
                    fv_norm = normalise_fix_value(ff, fv)
                    parsed_fixes.append((ff, fv_norm))
                    preview = str(fv_norm)[:70]
                    print(f"    🔧 FIX      {rid:<20}  {reason[:50]}")
                    print(f"               {ff} → {preview}")
                except ValueError as exc:
                    print(f"               ⚠️  parse error for {ff}: {exc} → Sonnet")
                    sonnet_needed = True

            if sonnet_needed:
                needs_sonnet.append((rule, parsed_fixes, reason))
            else:
                to_fix.append((rule, parsed_fixes, reason))

        elif verdict == "REJECT":
            reject_rules.append((rule, reason))
            print(f"    ❌ REJECT   {rid:<20}  {reason[:70]}")

        else:
            print(f"    ⚠️  Unknown verdict '{verdict}' for {rid} → APPROVE")
            approve_ids.append(rid)

    if bn < batch_count:
        time.sleep(1.5)

# ---------------------------------------------------------------------------
# Phase 2 -- Sonnet fix generation for rules missing fix_value
# ---------------------------------------------------------------------------
if needs_sonnet:
    print(f"\n{'═'*64}")
    print(f"  Phase 2: Fix generation (claude-sonnet-4-6)")
    print(f"  Rules needing Sonnet fix: {len(needs_sonnet)}")
    print("═" * 64)

    for rule, existing_fixes, reason in needs_sonnet:
        rid   = rule.get("rule_id", "?")
        cond  = rule.get("condition") or {}
        interp = rule.get("interpretation") or {}
        val   = rule.get("validation") or {}
        print(f"\n  ── {rid} ──")
        print(f"     Issue : {reason[:80]}")

        fix_prompt = f"""A Vedic astrology remedy rule has been flagged and needs specific corrections.

Rule ID    : {rid}
Flag reason: {(val.get('flag_reason') or val.get('reason') or '')[:300]}
Fix needed : {reason}

Current rule data:
  trigger_condition : {cond.get('trigger_condition', '')}
  planets_involved  : {json.dumps(cond.get('planets_involved', []))}
  houses_involved   : {json.dumps(cond.get('houses_involved', []))}
  summary           : {(interp.get('summary') or '')[:200]}
  detailed          : {(interp.get('detailed') or '')[:600]}
  start_day         : {interp.get('start_day', '')}
  mantra            : {(interp.get('mantra') or '')[:100]}

Apply ALL necessary fixes to resolve the flagged issue(s).
Return a JSON array of fix operations:
[
  {{"fix_field": "condition.planets_involved", "fix_value": ["Mars", "Saturn"]}},
  {{"fix_field": "condition.houses_involved", "fix_value": [1, 7]}},
  {{"fix_field": "interpretation.detailed", "fix_value": "corrected full text here"}},
  {{"fix_field": "interpretation.start_day", "fix_value": "Saturday"}}
]
Include only the fields that actually need changing.
Return the JSON array only -- no explanation."""

        try:
            raw = call_api(
                model="claude-sonnet-4-6",
                messages=[{"role": "user", "content": fix_prompt}],
                max_tokens=2048,
            )
            sonnet_fixes_raw = parse_json_response(raw)
            sonnet_fixes = []
            for entry in sonnet_fixes_raw:
                ff = normalise_fix_field(entry.get("fix_field") or "")
                fv = entry.get("fix_value")
                if ff and fv is not None:
                    try:
                        fv_norm = normalise_fix_value(ff, fv)
                        sonnet_fixes.append((ff, fv_norm))
                        print(f"     {ff} → {str(fv_norm)[:80]}")
                    except ValueError as exc:
                        print(f"     ⚠️  {ff} parse error: {exc}")

            all_fixes = existing_fixes + sonnet_fixes
            if all_fixes:
                to_fix.append((rule, all_fixes, reason))
            else:
                print(f"     ❌ No valid fixes generated → REJECT")
                reject_rules.append((rule, f"sonnet_generated_no_fixes: {reason}"))

            time.sleep(0.5)
        except Exception as e:
            print(f"     ❌ Fix generation failed: {e} → REJECT")
            reject_rules.append((rule, f"fix_generation_failed: {e}"))

# ---------------------------------------------------------------------------
# Phase 3 -- Write to MongoDB
# ---------------------------------------------------------------------------
print(f"\n{'═'*64}")
print(f"  Phase 3: Writing to MongoDB")
print("═" * 64)

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
                "approval_status":                   "auto_approved",
                "validation.verdict":                "approved",
                "validation.bucket_c_revalidation":  f"Passed bucket-C revalidation {NOW}",
            }}
        )
        n_approved += 1
    print(f"  ✅ auto_approved (direct) : {n_approved}")

    # Fixed → approve (each rule may have multiple fix fields)
    for rule, fixes, reason in to_fix:
        rid = rule.get("rule_id", "?")
        set_doc: dict = {
            "approval_status":                   "auto_approved",
            "validation.verdict":                "approved",
            "validation.bucket_c_revalidation":  f"Fixed in bucket-C revalidation {NOW} -- {reason[:120]}",
        }
        for ff, fv in fixes:
            set_doc[ff] = fv

        col.update_one({"rule_id": rid}, {"$set": set_doc})
        n_fixed += 1
        fix_summary = ", ".join(ff for ff, _ in fixes)
        print(f"  🔧 fixed+approved  {rid:<20}  fields: {fix_summary}")

    print(f"\n  ✅ auto_approved (fixed)  : {n_fixed}")

    # Rejections
    for rule, reason in reject_rules:
        rid = rule.get("rule_id", "?")
        col.update_one(
            {"rule_id": rid},
            {"$set": {
                "approval_status":  "rejected",
                "rejection_reason": f"bucket_c_revalidation: {reason}",
                "rejected_at":      NOW,
            }}
        )
        n_rejected += 1
        print(f"  ❌ rejected        {rid:<20}  {reason[:60]}")

    print(f"\n  ❌ rejected               : {n_rejected}")

    # Error rules -- leave flagged, add note
    for rule, err in error_rules:
        rid = rule.get("rule_id", "?")
        col.update_one(
            {"rule_id": rid},
            {"$set": {"validation.revalidation_error": f"api_error {NOW}: {err[:200]}"}}
        )
        n_errors += 1

    if n_errors:
        print(f"  ⚠️  left at flagged (API errors): {n_errors}")

else:
    n_approved = len(approve_ids)
    n_fixed    = len(to_fix)
    n_rejected = len(reject_rules)
    n_errors   = len(error_rules)
    print(f"  DRY-RUN -- would write:")
    print(f"    auto_approved (direct) : {n_approved}")
    print(f"    auto_approved (fixed)  : {n_fixed}")
    print(f"    rejected               : {n_rejected}")
    print(f"    flagged (API errors)   : {n_errors}")

    # Show fix details in dry-run
    if to_fix:
        print()
        print("  Fix details:")
        for rule, fixes, reason in to_fix:
            rid = rule.get("rule_id", "?")
            for ff, fv in fixes:
                print(f"    {rid:<20}  {ff} → {str(fv)[:70]}")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print()
print("═" * 64)
print("  FINAL SUMMARY")
print("═" * 64)
print(f"  Input  : {len(rules)} flagged Bucket C rules")
print(f"  Output :")
print(f"    auto_approved : {n_approved + n_fixed}  "
      f"({n_approved} direct + {n_fixed} fixed)")
print(f"    rejected      : {n_rejected}")
print(f"    flagged (err) : {n_errors}")
print()

if not args.dry_run:
    print("  Post-run counts per batch:")
    for bid in REMEDY_BATCHES:
        label = bid.split("-")[1].capitalize()
        aa    = col.count_documents({"source.batch_id": bid, "approval_status": "auto_approved"})
        flag  = col.count_documents({"source.batch_id": bid, "approval_status": "flagged"})
        phr   = col.count_documents({"source.batch_id": bid, "approval_status": "pending_human_review"})
        rej   = col.count_documents({"source.batch_id": bid, "approval_status": "rejected"})
        print(f"    {label:<12}  auto_approved={aa}  flagged={flag}  phr={phr}  rejected={rej}")
    print()

mongo.close()

print("╔══════════════════════════════════════════════════════════════╗")
print("  ✅ Bucket C revalidation complete")
print(f"  Log saved → {log_path}")
print("╚══════════════════════════════════════════════════════════════╝")

sys.stdout = sys.__stdout__
tee.close()
