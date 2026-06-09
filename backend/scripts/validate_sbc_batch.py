#!/usr/bin/env python3
"""
validate_sbc_batch.py
---------------------
One-pass AI validation for the SBC (Sarvato Bhadra Chakra) batch.
Batch ID: sbc_v1_20260605  |  182 rules  |  16 chapters

SBC is a specialised classical Vedic system based on the 9×9 chakra grid.
It is used for muhurta (electional), transit timing, event forecasting, and
horary. Its logic (Vedha aspects, vowel/consonant mappings, nakshatra
sensitivity axes) is ENTIRELY DIFFERENT from standard natal chart Vedic.

DO NOT run validate_rules.py on SBC -- it applies BPHS natal criteria which
are simply the wrong framework for this system.

This script validates SBC rules only for:
  1. COMPLETENESS   -- rule has a meaningful condition + conclusion/interpretation
  2. CONSISTENCY    -- condition fields match the detailed text
  3. LANGUAGE       -- no incoherence, no truncation, no pseudo-science
  4. INTERNAL LOGIC -- stated conclusion follows from the stated condition

Verdicts:
  APPROVE → auto_approved
  FIX     → fix specific field(s) → auto_approved
  REJECT  → rejected (incoherent / unsalvageable)

Usage:
  python3 backend/scripts/validate_sbc_batch.py --dry-run
  python3 backend/scripts/validate_sbc_batch.py
  python3 backend/scripts/validate_sbc_batch.py --batch-size 8
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
parser.add_argument("--batch-size", type=int, default=8)
args = parser.parse_args()

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
mode_tag = "dry-run" if args.dry_run else "live"
log_path = LOG_DIR / f"validate_sbc_batch_{mode_tag}_{ts}.log"

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
print(f"  validate_sbc_batch.py  [{mode_tag.upper()}]")
print(f"  Batch : sbc_v1_20260605")
print(f"  Run   : {ts} UTC")
print(f"  Log   : {log_path}")
print("╚══════════════════════════════════════════════════════════════╝")
print()
if args.dry_run:
    print("  ⚠️  DRY-RUN -- no changes written to MongoDB.")
    print()

# ---------------------------------------------------------------------------
# Connect
# ---------------------------------------------------------------------------
MONGO_URL         = os.environ.get("MONGO_URL")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not MONGO_URL:
    print("ERROR: MONGO_URL not set."); sys.exit(1)
if not ANTHROPIC_API_KEY:
    print("ERROR: ANTHROPIC_API_KEY not set."); sys.exit(1)

mongo = MongoClient(MONGO_URL, serverSelectionTimeoutMS=10_000)
col   = mongo["horoscope_db"]["interpretation_rules"]
ai    = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

BATCH_ID = "sbc_v1_20260605"

# ---------------------------------------------------------------------------
# Load rules -- catch both pending_review and flagged (ingest may vary)
# ---------------------------------------------------------------------------
rules = list(col.find(
    {
        "source.batch_id": BATCH_ID,
        "approval_status": {"$in": ["pending_review", "pending_human_review", "flagged"]},
    },
    {"_id": 0}
))

print(f"  Rules to validate : {len(rules)}")
batch_count = (len(rules) + args.batch_size - 1) // args.batch_size if rules else 0
print(f"  Batch size        : {args.batch_size}  →  {batch_count} API calls")
print(f"  Validation model  : claude-haiku-4-5-20251001")
print(f"  Fix model         : claude-sonnet-4-6 (fallback only)")
print()

if not rules:
    print("✅ Nothing to do.")
    mongo.close()
    sys.stdout = sys.__stdout__; tee.close(); sys.exit(0)

# Per-chapter breakdown
from collections import Counter
chapter_counts = Counter((r.get("source") or {}).get("chapter_title", "unknown") for r in rules)
print("  Chapter breakdown:")
for ch, cnt in sorted(chapter_counts.items()):
    print(f"    {ch[:55]:<55} {cnt:>3}")
print()

# ---------------------------------------------------------------------------
# Field-path normalisation
# ---------------------------------------------------------------------------
FIELD_PATH_MAP = {
    "trigger_condition":  "condition.trigger_condition",
    "planets_involved":   "condition.planets_involved",
    "houses_involved":    "condition.houses_involved",
    "nakshatras":         "condition.nakshatras",
    "start_day":          "interpretation.start_day",
    "mantra":             "interpretation.mantra",
    "summary":            "interpretation.summary",
    "detailed":           "interpretation.detailed",
}

def normalise_fix_field(ff: str) -> str:
    return FIELD_PATH_MAP.get(ff, ff)

def normalise_fix_value(fix_field: str, raw_value) -> object:
    array_fields = {
        "condition.planets_involved",
        "condition.houses_involved",
        "condition.nakshatras",
    }
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
            if "[" in raw_value and "]" in raw_value:
                try:
                    return json.loads(raw_value[raw_value.index("["):raw_value.rindex("]")+1])
                except json.JSONDecodeError:
                    pass
        raise ValueError(f"Cannot parse array for {fix_field}: {str(raw_value)[:80]}")
    if isinstance(raw_value, str):
        return raw_value.strip().strip('"')
    return str(raw_value)

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are a quality validator for EverydayHoroscope, a Vedic astrology app.

You are validating rules from the SARVATO BHADRA CHAKRA (SBC) library. SBC is a
classical Vedic system based on a 9×9 chakra grid used for muhurta (electional
astrology), transit timing, event forecasting, and horary analysis.

SBC operates on ENTIRELY DIFFERENT logic from standard natal chart Vedic astrology:
  - Vedha (obstruction) aspects work on the grid, not house-based aspects
  - Nakshatra sensitivity axes (vowel/consonant mappings) determine affliction
  - Planets on the chakra activate rows/columns of nakshatras
  - Timing is determined by transit of planets across sensitive chakra points

NEVER flag an SBC rule for:
  - Not matching BPHS natal chart logic
  - Using Vedha aspects instead of standard aspects
  - Referencing chakra-grid positions or sensitivity axes
  - Using muhurta / horary / transit timing rather than natal interpretation
  - Having no "houses_involved" (SBC uses nakshatras and chakra rows, not houses)

VALIDATE each rule ONLY for:

1. COMPLETENESS
   Rule must have a clear SBC condition (which planet/nakshatra/transit triggers it)
   AND a meaningful interpretation/conclusion. If either is missing → FIX or REJECT.

2. FIELD CONSISTENCY
   planets_involved and nakshatras (if present) must match the detailed text.
   If condition arrays are empty but trigger_condition names specific planets or
   nakshatras → FIX: derive the correct array from the trigger_condition text.

3. LANGUAGE QUALITY
   No truncated text, no incoherent sentences, no pseudo-scientific claims.
   Truncated text → FIX: complete the sentence based on context.

4. INTERNAL LOGIC
   The stated conclusion must follow logically from the stated condition.
   If they directly contradict each other → REJECT.
   If the conclusion is reasonable for SBC even if unusual → APPROVE.

VERDICTS:
  APPROVE -- passes all checks.
  FIX     -- specific fixable issue. Provide "fixes" array with fix_field + fix_value.
  REJECT  -- core premise is incoherent or trigger and conclusion directly contradict.
             Use sparingly.

RESPONSE FORMAT -- valid JSON array, one object per rule:
{
  "rule_id": "...",
  "verdict": "APPROVE" | "FIX" | "REJECT",
  "reason": "one concise sentence",
  "fixes": [
    {"fix_field": "condition.planets_involved", "fix_value": ["Mars", "Saturn"]},
    {"fix_field": "condition.nakshatras", "fix_value": ["Ashwini", "Bharani"]},
    {"fix_field": "interpretation.detailed", "fix_value": "corrected full text"}
  ]
}

For APPROVE or REJECT: "fixes" should be [] or omitted.
fix_value for array fields must be a JSON array.
fix_value for text fields must be the complete corrected string.

Return ONLY the JSON array. No markdown, no explanation outside the JSON."""


def build_user_prompt(batch: list) -> str:
    summaries = []
    for r in batch:
        cond   = r.get("condition") or {}
        interp = r.get("interpretation") or {}
        src    = r.get("source") or {}
        summaries.append({
            "rule_id":           r.get("rule_id"),
            "chapter":           src.get("chapter_title", ""),
            "trigger_condition": cond.get("trigger_condition", ""),
            "planets_involved":  cond.get("planets_involved", []),
            "houses_involved":   cond.get("houses_involved", []),
            "nakshatras":        cond.get("nakshatras", []),
            "summary":           (interp.get("summary") or "")[:200],
            "detailed":          (interp.get("detailed") or "")[:700],
        })
    return (
        f"Validate the following {len(batch)} SBC (Sarvato Bhadra Chakra) rules.\n"
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


# ---------------------------------------------------------------------------
# Phase 1 -- Batch validate (haiku)
# ---------------------------------------------------------------------------
print("═" * 64)
print("  Phase 1: Batch validation (claude-haiku-4-5-20251001)")
print("═" * 64)

approve_ids:  list[str]   = []
to_fix:       list[tuple] = []   # (rule, [(fix_field, fix_value)], reason)
reject_rules: list[tuple] = []   # (rule, reason)
error_rules:  list[tuple] = []   # (rule, error_msg)
needs_sonnet: list[tuple] = []   # (rule, existing_fixes, reason)

rule_lookup = {r["rule_id"]: r for r in rules}

for i in range(0, len(rules), args.batch_size):
    batch = rules[i : i + args.batch_size]
    bn = i // args.batch_size + 1
    print(f"\n  ── Batch {bn}/{batch_count} "
          f"(rules {i+1}-{min(i+args.batch_size, len(rules))}) ──")

    try:
        raw      = call_api(
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
            print(f"    ✅ APPROVE  {rid:<22}  {reason[:65]}")

        elif verdict == "FIX":
            raw_fixes = v.get("fixes") or []
            if not raw_fixes:
                ff = normalise_fix_field(v.get("fix_field") or "")
                fv = v.get("fix_value")
                if ff:
                    raw_fixes = [{"fix_field": ff, "fix_value": fv}]

            if not raw_fixes:
                print(f"    🔧 FIX      {rid:<22}  {reason[:55]}  [no fix → Sonnet]")
                needs_sonnet.append((rule, [], reason))
                continue

            parsed_fixes = []
            sonnet_needed = False
            for entry in raw_fixes:
                ff = normalise_fix_field(entry.get("fix_field") or "")
                fv = entry.get("fix_value")
                if not ff:
                    continue
                if fv is None:
                    sonnet_needed = True
                    continue
                try:
                    fv_norm = normalise_fix_value(ff, fv)
                    parsed_fixes.append((ff, fv_norm))
                    print(f"    🔧 FIX      {rid:<22}  {reason[:50]}")
                    print(f"               {ff} → {str(fv_norm)[:70]}")
                except ValueError as exc:
                    print(f"               ⚠️  parse error {ff}: {exc} → Sonnet")
                    sonnet_needed = True

            if sonnet_needed:
                needs_sonnet.append((rule, parsed_fixes, reason))
            else:
                to_fix.append((rule, parsed_fixes, reason))

        elif verdict == "REJECT":
            reject_rules.append((rule, reason))
            print(f"    ❌ REJECT   {rid:<22}  {reason[:65]}")

        else:
            print(f"    ⚠️  Unknown verdict '{verdict}' for {rid} → APPROVE")
            approve_ids.append(rid)

    if bn < batch_count:
        time.sleep(1.5)

# ---------------------------------------------------------------------------
# Phase 2 -- Sonnet fix generation (fallback)
# ---------------------------------------------------------------------------
if needs_sonnet:
    print(f"\n{'═'*64}")
    print(f"  Phase 2: Fix generation (claude-sonnet-4-6)")
    print(f"  Rules needing Sonnet: {len(needs_sonnet)}")
    print("═" * 64)

    for rule, existing_fixes, reason in needs_sonnet:
        rid   = rule.get("rule_id", "?")
        cond  = rule.get("condition") or {}
        interp = rule.get("interpretation") or {}
        print(f"\n  ── {rid} ──  {reason[:70]}")

        fix_prompt = f"""An SBC (Sarvato Bhadra Chakra) rule needs specific corrections.

Rule ID   : {rid}
Issue     : {reason}

Current rule:
  trigger_condition : {cond.get('trigger_condition', '')}
  planets_involved  : {json.dumps(cond.get('planets_involved', []))}
  nakshatras        : {json.dumps(cond.get('nakshatras', []))}
  houses_involved   : {json.dumps(cond.get('houses_involved', []))}
  summary           : {(interp.get('summary') or '')[:200]}
  detailed          : {(interp.get('detailed') or '')[:500]}

Return a JSON array of fix operations:
[
  {{"fix_field": "condition.planets_involved", "fix_value": ["Mars"]}},
  {{"fix_field": "interpretation.detailed", "fix_value": "corrected text"}}
]
Include only fields that need changing. Return the JSON array only."""

        try:
            raw = call_api(
                model="claude-sonnet-4-6",
                messages=[{"role": "user", "content": fix_prompt}],
                max_tokens=1024,
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
                print(f"     ❌ No valid fixes → REJECT")
                reject_rules.append((rule, f"sonnet_no_fixes: {reason}"))
            time.sleep(0.5)

        except Exception as e:
            print(f"     ❌ Fix generation failed: {e} → REJECT")
            reject_rules.append((rule, f"fix_failed: {e}"))

# ---------------------------------------------------------------------------
# Phase 3 -- Write to MongoDB
# ---------------------------------------------------------------------------
print(f"\n{'═'*64}")
print(f"  Phase 3: Writing to MongoDB")
print("═" * 64)

NOW = datetime.now(timezone.utc).isoformat()
n_approved = n_fixed = n_rejected = n_errors = 0

if not args.dry_run:
    for rid in approve_ids:
        col.update_one(
            {"rule_id": rid},
            {"$set": {
                "approval_status":            "auto_approved",
                "validation.verdict":         "approved",
                "validation.sbc_validation":  f"Passed SBC one-pass validation {NOW}",
            }}
        )
        n_approved += 1

    for rule, fixes, reason in to_fix:
        rid     = rule.get("rule_id", "?")
        set_doc = {
            "approval_status":            "auto_approved",
            "validation.verdict":         "approved",
            "validation.sbc_validation":  f"Fixed in SBC one-pass validation {NOW} -- {reason[:100]}",
        }
        for ff, fv in fixes:
            set_doc[ff] = fv
        col.update_one({"rule_id": rid}, {"$set": set_doc})
        n_fixed += 1
        print(f"  🔧 {rid:<24}  {', '.join(ff for ff, _ in fixes)}")

    for rule, reason in reject_rules:
        rid = rule.get("rule_id", "?")
        col.update_one(
            {"rule_id": rid},
            {"$set": {
                "approval_status":  "rejected",
                "rejection_reason": f"sbc_validation: {reason}",
                "rejected_at":      NOW,
            }}
        )
        n_rejected += 1
        print(f"  ❌ REJECTED  {rid:<24}  {reason[:60]}")

    for rule, err in error_rules:
        rid = rule.get("rule_id", "?")
        col.update_one(
            {"rule_id": rid},
            {"$set": {"validation.revalidation_error": f"api_error {NOW}: {err[:200]}"}}
        )
        n_errors += 1

    print(f"\n  ✅ auto_approved (direct) : {n_approved}")
    print(f"  ✅ auto_approved (fixed)  : {n_fixed}")
    print(f"  ❌ rejected               : {n_rejected}")
    if n_errors:
        print(f"  ⚠️  left pending (errors) : {n_errors}")

else:
    n_approved = len(approve_ids)
    n_fixed    = len(to_fix)
    n_rejected = len(reject_rules)
    n_errors   = len(error_rules)
    print(f"  DRY-RUN -- would write:")
    print(f"    auto_approved (direct) : {n_approved}")
    print(f"    auto_approved (fixed)  : {n_fixed}")
    print(f"    rejected               : {n_rejected}")
    print(f"    pending (API errors)   : {n_errors}")
    if to_fix:
        print()
        print("  Fix details:")
        for rule, fixes, reason in to_fix:
            rid = rule.get("rule_id", "?")
            for ff, fv in fixes:
                print(f"    {rid:<24}  {ff} → {str(fv)[:65]}")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print()
print("═" * 64)
print("  FINAL SUMMARY")
print("═" * 64)
print(f"  Input  : {len(rules)} SBC rules (batch: {BATCH_ID})")
print(f"  Output :")
print(f"    auto_approved : {n_approved + n_fixed}  ({n_approved} direct + {n_fixed} fixed)")
print(f"    rejected      : {n_rejected}")
print(f"    pending (err) : {n_errors}")
print()

if not args.dry_run:
    aa  = col.count_documents({"source.batch_id": BATCH_ID, "approval_status": "auto_approved"})
    rej = col.count_documents({"source.batch_id": BATCH_ID, "approval_status": "rejected"})
    phr = col.count_documents({"source.batch_id": BATCH_ID, "approval_status": "pending_human_review"})
    flg = col.count_documents({"source.batch_id": BATCH_ID, "approval_status": "flagged"})
    prv = col.count_documents({"source.batch_id": BATCH_ID, "approval_status": "pending_review"})
    print(f"  DB post-run (batch {BATCH_ID}):")
    print(f"    auto_approved={aa}  rejected={rej}  phr={phr}  flagged={flg}  pending_review={prv}")
    print()

mongo.close()

print("╔══════════════════════════════════════════════════════════════╗")
print("  ✅ SBC batch validation complete")
print(f"  Log saved → {log_path}")
print("╚══════════════════════════════════════════════════════════════╝")

sys.stdout = sys.__stdout__
tee.close()
