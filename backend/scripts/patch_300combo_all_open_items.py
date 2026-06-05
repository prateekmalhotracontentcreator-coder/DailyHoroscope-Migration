#!/usr/bin/env python3
"""
patch_300combo_all_open_items.py
--------------------------------------------------------------------
Closes all 6 open items from 300_COMBINATIONS_INGEST.md in one pass.

OP-01 / OP-02 (147 rules -- primary patch):
  Source JSON for Y117-Y300+ range has TWO encoding variants that the
  original ingest and old-schema patch did not handle:

  (a) results as list-of-dicts with 'effect'/'effect_type' keys (96 rules):
      patch_300combo_old_schema.py joined the dict repr instead of the effect
      text → interpretation.detailed contains "{' effect': '...', ...}"
      Fix: extract result['effect'] from each dict item

  (b) conditions as a rich DICT (not list) with type/conditions/variants (147 rules):
      build_condition() in old schema patch only handled list-of-conditions;
      dict conditions fell through to {'type': 'composite'} fallback
      Fix: store conditions dict directly as condition

  Flagged rules among these 147 → reset to pending_review after fix (re-validate)
  auto_approved / PHR → fix data, keep status (semantic content unchanged)

OP-04 (6 rules -- contradiction pair tags):
  Tag 3 Nabhasa cross-pairs as strength_dependent.

OP-05 (14 rules -- short interpretation):
  Add short_interpretation_justified: true, reset flagged/pending_review → PHR.

OP-06 (10 rules -- same-yoga variant pairs):
  Add variant_note -- conditions are distinct, both rules are valid.

OP-03 (70 rules -- new-schema AI re-validation):
  Reset new-schema PHR rules (Y001-040, intro, strength) to pending_review
  so validate_rules.py Stage 2 can pick them up.

Run (dry run first):
    python3 backend/scripts/patch_300combo_all_open_items.py --dry-run

Live:
    python3 backend/scripts/patch_300combo_all_open_items.py \
      --mongo-url "mongodb+srv://..." --db-name horoscope_db
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DECODE_FOLDER = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredCombinations_CC_Decode"
)
BATCH_ID = "300-combinations-v1-20260601"

# ──────────────────────────────────────────────
# OP-04: Nabhasa contradiction pair rule IDs
# ──────────────────────────────────────────────
NABHASA_PAIRS = [
    ("combo-y074-001", "combo-y078-001"),  # Danda vs Chapa
    ("combo-y080-001", "combo-y090-001"),  # Chandra vs Samudra
    ("combo-y082-001", "combo-y088-001"),  # Sakata vs Kamala
]
NABHASA_RULE_IDS = [rid for pair in NABHASA_PAIRS for rid in pair]

# ──────────────────────────────────────────────
# OP-05: Short-interpretation Nabhasa yogas
# ──────────────────────────────────────────────
SHORT_INTERP_RULE_IDS = [
    "combo-y075-001", "combo-y076-001", "combo-y077-001",
    "combo-y081-001", "combo-y084-001", "combo-y085-001",
    "combo-y086-001", "combo-y087-001", "combo-y100-001",
    "combo-y110-001", "combo-y114-001", "combo-y115-001",
    "combo-y116-001", "combo-y295-001",
]

# ──────────────────────────────────────────────
# OP-06: Same-yoga-name variant pairs
# Each entry: (rule_id_a, rule_id_b, yoga_name, distinction)
# ──────────────────────────────────────────────
VARIANT_PAIRS = [
    (
        "combo-y189-001", "combo-y190-001",
        "Ayatna Griha Prapta Yoga",
        "Y189 and Y190 encode distinct condition sets for the same yoga. "
        "Raman listed two separate planetary configurations; both are valid."
    ),
    (
        "combo-y191-001", "combo-y192-001",
        "Grihanasa Yoga",
        "Y191 uses multi-lord-position condition; Y192 uses navamsa-chain-lord condition. "
        "Different astrological mechanisms, same life outcome."
    ),
    (
        "combo-y193-001", "combo-y194-001",
        "Bandhu Pujya Yoga",
        "Y193 requires 4th lord to be a natural benefic; Y194 uses multi-trigger "
        "(4th house or 4th lord association). Distinct formation conditions."
    ),
    (
        "combo-y196-001", "combo-y197-001",
        "Matrudeerghayur Yoga",
        "Y196 requires benefics in 4th house; Y197 uses navamsa-chain-lord-disposition. "
        "Two different indicators for the same outcome."
    ),
    (
        "combo-y198-001", "combo-y199-001",
        "Matrunasa Yoga",
        "Y198 uses multi-trigger severity escalation; Y199 uses 3-step navamsa chain. "
        "Separate formation paths for the same malefic outcome."
    ),
]


def polarity_map(raw: Any) -> str:
    p = str(raw or "").strip().lower()
    return {
        "positive": "positive", "auspicious": "positive",
        "negative": "negative", "inauspicious": "negative",
        "mixed": "mixed", "neutral": "neutral",
        "conditional": "mixed",
    }.get(p, "neutral")


def extract_effects(results: Any) -> list[str]:
    """Extract plain-text effect strings from either string list or dict list."""
    if not isinstance(results, list):
        return []
    out = []
    for item in results:
        if isinstance(item, dict):
            # Primary: 'effect' key; fallback: 'description', then str(item)
            text = (
                item.get("effect")
                or item.get("description")
                or item.get("result")
                or str(item)
            )
            out.append(str(text).strip())
        elif isinstance(item, str):
            out.append(item.strip())
    return [t for t in out if t]


def build_interpretation_from_source(rule: dict[str, Any]) -> dict[str, str]:
    """Build interpretation.detailed + summary from source rule fields."""
    yoga_name   = str(rule.get("yoga_name") or "").strip()
    results     = rule.get("results") or []
    special     = str(rule.get("special_notes") or "").strip()

    effect_strs = extract_effects(results)
    results_str = "; ".join(effect_strs)

    parts = []
    if yoga_name:
        parts.append(f"{yoga_name}.")
    if results_str:
        parts.append(f"Results: {results_str}.")
    if special:
        parts.append(f"Notes: {special}")
    detailed = " ".join(parts).strip()

    summary_results = "; ".join(effect_strs[:2])
    if yoga_name and summary_results:
        summary = f"{yoga_name}: {summary_results}."
    elif yoga_name:
        summary = yoga_name
    else:
        summary = summary_results
    return {"detailed": detailed, "summary": summary[:500]}


def build_condition_from_source(rule: dict[str, Any]) -> dict[str, Any]:
    """
    Map source condition/conditions field to canonical condition dict.
    Three cases:
      1. 'conditions' is a rich dict → store directly as condition
      2. 'conditions' is a list → first element as primary + sub_conditions
      3. Neither → fallback to {type: rule_type}
    """
    conds = rule.get("conditions")

    if isinstance(conds, dict):
        # Already canonical -- store directly
        return conds

    if isinstance(conds, list) and conds:
        if len(conds) == 1:
            c = conds[0]
            return dict(c) if isinstance(c, dict) else {"type": str(c)}
        primary = dict(conds[0]) if isinstance(conds[0], dict) else {"type": str(conds[0])}
        primary["sub_conditions"] = [
            dict(c) if isinstance(c, dict) else {"type": str(c)}
            for c in conds[1:]
        ]
        primary["operator"] = "AND"
        if not primary.get("type"):
            primary["type"] = "composite"
        return primary

    rule_type = rule.get("type") or rule.get("rule_type") or "composite"
    return {"type": str(rule_type)}


def load_all_source_rules() -> dict[str, dict[str, Any]]:
    """Load all rules from all Combo_Y*.json files indexed by rule_id."""
    rules_by_id: dict[str, dict[str, Any]] = {}
    for f in sorted(DECODE_FOLDER.glob("Combo_Y*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            rules = data.get("rules", data) if isinstance(data, dict) else data
            for r in rules:
                if isinstance(r, dict) and r.get("rule_id"):
                    rules_by_id[str(r["rule_id"])] = r
        except Exception as e:
            print(f"  [warn] {f.name}: {e}")
    return rules_by_id


def identify_op01_op02_rule_ids(source_rules: dict[str, dict]) -> set[str]:
    """
    Return rule_ids that need OP-01 or OP-02 fix:
      - results is list of dicts  (OP-01)
      - conditions is a dict       (OP-02)
    """
    affected = set()
    for rid, rule in source_rules.items():
        results = rule.get("results", [])
        if isinstance(results, list) and results and isinstance(results[0], dict):
            affected.add(rid)
        conds = rule.get("conditions")
        if isinstance(conds, dict):
            affected.add(rid)
    return affected


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Patch all 300 Combinations open items.")
    p.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    p.add_argument("--db-name", default="horoscope_db")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skip-op03", action="store_true",
                   help="Skip OP-03 (reset 70 new-schema rules for re-validation)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    now_ts = datetime.now(timezone.utc).isoformat()
    dry = args.dry_run

    print("\n" + "=" * 65)
    print("patch_300combo_all_open_items.py")
    print(f"Mode:  {'DRY RUN' if dry else 'LIVE'}")
    print(f"Batch: {BATCH_ID}")
    print("=" * 65 + "\n")

    # ── Load source rules ──
    print("Loading source rules from decode folder...")
    source_rules = load_all_source_rules()
    print(f"  Loaded {len(source_rules)} rules\n")

    op01_02_ids = identify_op01_op02_rule_ids(source_rules)
    print(f"OP-01/02 affected rule_ids: {len(op01_02_ids)}")

    if not dry:
        if not args.mongo_url:
            print("ERROR: --mongo-url required", file=sys.stderr)
            sys.exit(1)
        from pymongo import MongoClient
        client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=15000)
        db = client[args.db_name]

        # Fetch current status for all batch rules once
        all_batch_rules = list(db["interpretation_rules"].find(
            {"ingest_batch_id": BATCH_ID},
            {"_id": 0, "rule_id": 1, "approval_status": 1}
        ))
        status_map = {r["rule_id"]: r["approval_status"] for r in all_batch_rules}
    else:
        status_map = {}

    # ══════════════════════════════════════════════════════
    # OP-01 + OP-02: Fix condition + interpretation for 147 rules
    # ══════════════════════════════════════════════════════
    print("\n── OP-01 + OP-02: Fix conditions and interpretation (147 rules) ──")
    op01_02_patched = 0
    op01_02_flagged_reset = 0
    op01_02_errors = 0

    for rule_id in sorted(op01_02_ids):
        source = source_rules.get(rule_id)
        if not source:
            print(f"  [warn] {rule_id} not in source")
            op01_02_errors += 1
            continue

        # Build fixed fields
        interpretation = build_interpretation_from_source(source)
        condition      = build_condition_from_source(source)
        raw_polarity   = source.get("polarity") or source.get("claim_polarity") or ""
        claim_polarity = polarity_map(raw_polarity)

        current_status = status_map.get(rule_id, "unknown")
        # Flagged rules → reset to pending_review for re-validation
        new_status = "pending_review" if current_status == "flagged" else None

        update: dict[str, Any] = {
            "interpretation": interpretation,
            "condition":      condition,
            "claim_polarity": claim_polarity,
            "patched_at":     now_ts,
            "patch_note":     "op01-op02-fix: dict-results effect extraction + dict-conditions direct store",
        }
        if new_status:
            update["approval_status"] = new_status

        if dry:
            if op01_02_patched < 3:
                print(f"\n  DRY {rule_id} [{current_status}{'→'+new_status if new_status else ''}]:")
                print(f"    interp.detailed: {interpretation['detailed'][:90]}")
                print(f"    condition.type:  {condition.get('type')}")
            op01_02_patched += 1
            if new_status:
                op01_02_flagged_reset += 1
        else:
            try:
                res = db["interpretation_rules"].update_one(
                    {"rule_id": rule_id, "ingest_batch_id": BATCH_ID},
                    {"$set": update},
                )
                if res.matched_count:
                    op01_02_patched += 1
                    if new_status:
                        op01_02_flagged_reset += 1
                else:
                    print(f"  [warn] {rule_id} not found in MongoDB")
                    op01_02_errors += 1
            except Exception as e:
                print(f"  [error] {rule_id}: {e}")
                op01_02_errors += 1

    print(f"  Patched:             {op01_02_patched}")
    print(f"  Flagged → pending_review: {op01_02_flagged_reset}")
    print(f"  Errors:              {op01_02_errors}")

    # ══════════════════════════════════════════════════════
    # OP-04: Tag Nabhasa contradiction pairs
    # ══════════════════════════════════════════════════════
    print("\n── OP-04: Nabhasa contradiction pair tags (6 rules) ──")
    op04_patched = 0
    for i, (rid_a, rid_b) in enumerate(NABHASA_PAIRS):
        pair_note = (
            f"Nabhasa yoga pair {i+1}/3: strength_dependent. "
            f"Both rules valid -- outcome scales with chart strength per L5."
        )
        for rid in (rid_a, rid_b):
            update = {
                "contradiction_resolution": "strength_dependent",
                "contradiction_note": pair_note,
                "patched_at": now_ts,
            }
            if dry:
                print(f"  DRY {rid}: contradiction_resolution=strength_dependent")
                op04_patched += 1
            else:
                try:
                    res = db["interpretation_rules"].update_one(
                        {"rule_id": rid, "ingest_batch_id": BATCH_ID},
                        {"$set": update},
                    )
                    if res.matched_count:
                        op04_patched += 1
                    else:
                        print(f"  [warn] {rid} not found")
                except Exception as e:
                    print(f"  [error] {rid}: {e}")
    print(f"  Patched: {op04_patched}/6")

    # ══════════════════════════════════════════════════════
    # OP-05: Short-interpretation Nabhasa yogas
    # ══════════════════════════════════════════════════════
    print("\n── OP-05: Short-interpretation justified (14 rules) ──")
    op05_patched = 0
    for rid in SHORT_INTERP_RULE_IDS:
        current_status = status_map.get(rid, "unknown")
        # Reset from pending_review → pending_human_review so they clear structural check
        new_status = "pending_human_review" if current_status == "pending_review" else None
        update: dict[str, Any] = {
            "short_interpretation_justified": True,
            "short_interpretation_note": (
                "Source text is genuinely brief -- Raman's original for this Nabhasa yoga "
                "lists 1-3 outcome phrases. The interpretation length reflects the source."
            ),
            "patched_at": now_ts,
        }
        if new_status:
            update["approval_status"] = new_status
        if dry:
            print(f"  DRY {rid} [{current_status}{'→'+new_status if new_status else ''}]: short_interpretation_justified=True")
            op05_patched += 1
        else:
            try:
                res = db["interpretation_rules"].update_one(
                    {"rule_id": rid, "ingest_batch_id": BATCH_ID},
                    {"$set": update},
                )
                if res.matched_count:
                    op05_patched += 1
            except Exception as e:
                print(f"  [error] {rid}: {e}")
    print(f"  Patched: {op05_patched}/14")

    # ══════════════════════════════════════════════════════
    # OP-06: Variant pair notes
    # ══════════════════════════════════════════════════════
    print("\n── OP-06: Variant pair notes (10 rules across 5 pairs) ──")
    op06_patched = 0
    for rid_a, rid_b, yoga_name, distinction in VARIANT_PAIRS:
        for rid, partner in ((rid_a, rid_b), (rid_b, rid_a)):
            update = {
                "variant_note": distinction,
                "variant_of": partner,
                "patched_at": now_ts,
                "patch_note": "op06: same-yoga-name variant -- distinct conditions, both valid",
            }
            if dry:
                print(f"  DRY {rid}: variant_of={partner}")
                op06_patched += 1
            else:
                try:
                    res = db["interpretation_rules"].update_one(
                        {"rule_id": rid, "ingest_batch_id": BATCH_ID},
                        {"$set": update},
                    )
                    if res.matched_count:
                        op06_patched += 1
                except Exception as e:
                    print(f"  [error] {rid}: {e}")
    print(f"  Patched: {op06_patched}/10")

    # ══════════════════════════════════════════════════════
    # OP-03: Reset 70 new-schema rules for AI re-validation
    # ══════════════════════════════════════════════════════
    if not args.skip_op03:
        print("\n── OP-03: Reset new-schema PHR rules for AI re-validation ──")
        new_schema_ids = [
            rid for rid, status in status_map.items()
            if status == "pending_human_review"
            and re.match(r"combo-(y0[0-3]\d|intro|strength)", rid)
        ]
        if not new_schema_ids and not dry:
            # Fallback: fetch from MongoDB
            phr_rules = list(db["interpretation_rules"].find(
                {"ingest_batch_id": BATCH_ID, "approval_status": "pending_human_review"},
                {"_id": 0, "rule_id": 1}
            ))
            new_schema_ids = [
                r["rule_id"] for r in phr_rules
                if re.match(r"combo-(y0[0-3]\d|intro|strength)", r["rule_id"])
            ]
        print(f"  New-schema PHR rules to reset: {len(new_schema_ids)}")
        if dry:
            print(f"  DRY: would reset {len(new_schema_ids)} rules to pending_review")
        else:
            if new_schema_ids:
                try:
                    res = db["interpretation_rules"].update_many(
                        {"rule_id": {"$in": new_schema_ids}, "ingest_batch_id": BATCH_ID},
                        {"$set": {"approval_status": "pending_review", "patched_at": now_ts,
                                  "patch_note": "op03: reset for AI quality re-validation"}},
                    )
                    print(f"  Reset: {res.modified_count} rules → pending_review")
                    print(f"  Next: run validate_rules.py --batch-id {BATCH_ID} with ANTHROPIC_API_KEY set")
                except Exception as e:
                    print(f"  [error] {e}")
            else:
                print("  No matching PHR rules found (already reset or not present)")
    else:
        print("\n── OP-03: SKIPPED (--skip-op03) ──")

    # ══════════════════════════════════════════════════════
    # Summary
    # ══════════════════════════════════════════════════════
    print(f"\n{'=' * 65}")
    print("PATCH SUMMARY")
    print(f"{'=' * 65}")
    print(f"  OP-01/02 -- interpretation + condition fix:  {op01_02_patched} rules")
    print(f"  OP-01/02 -- flagged → pending_review:        {op01_02_flagged_reset} rules")
    print(f"  OP-04    -- Nabhasa contradiction tags:       {op04_patched}/6 rules")
    print(f"  OP-05    -- short_interpretation_justified:   {op05_patched}/14 rules")
    print(f"  OP-06    -- variant pair notes:               {op06_patched}/10 rules")
    if not args.skip_op03:
        print(f"  OP-03    -- new-schema reset to pending_review: see output above")
    if dry:
        print("\n[DRY RUN] No writes made. Re-run without --dry-run to apply.")
    else:
        print(f"\nNEXT STEPS:")
        print(f"  1. Run validate_rules.py with ANTHROPIC_API_KEY set:")
        print(f"     ANTHROPIC_API_KEY='sk-ant-...' python3 backend/scripts/validate_rules.py \\")
        print(f"       --batch-id {BATCH_ID} --mongo-url \"$MONGO_URL\" --db-name {args.db_name}")
        print(f"  2. Review new validation report -- flagged rules should be significantly reduced")
        print(f"  3. Update 300_COMBINATIONS_INGEST.md open items")
    print("=" * 65)

    if not dry and "client" in dir():
        client.close()


if __name__ == "__main__":
    main()
