#!/usr/bin/env python3
"""Ingest 300 Horoscopes Vol 1 rules into horoscope_db.interpretation_rules.

Batch ID   : 300_horoscopes_vol1_v1
Source     : /Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredHoroscopes_CC_Decode/
Rules      : 57 total (5 JSON files)
Book       : 300 Horoscopes Vol. 1 -- MK Viswanath Nair | KP Jyotish

Schema mapping (single schema -- all 5 files identical):
  full_text (top-level)   → interpretation.detailed
  summary (top-level)     → interpretation.summary
  condition (dict)        → passed through as-is
  result (dict)           → passed through as-is
  source["batch_id"]      → OVERRIDDEN to BATCH_ID (MANDATORY)

Special handling:
  - 6 intra-book superseded rules → active: False
    (h300-s02-010/011/012, h300-s04-003/006/007)
  - 2 TT-decision duplicate candidates → pending_review: True + decode_notes
    (h300-s01a-009, h300-s03-004)
  - 15 case studies in H300_TestVectors.json → NOT rules, SKIPPED entirely
  - approval_status: "pending_human_review" for all 57 rules (per thread brief)
    Bypasses AI validator -- TT reviews at approval stage.

Pre-ingest dedup: 0 matches across 593,598 pairs vs full MongoDB (10,414 rules).
Report: H300_Dedup_vs_FullMongoDB.md
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BATCH_ID = "300_horoscopes_vol1_v1"
SOURCE_FOLDER = Path("/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredHoroscopes_CC_Decode/")
RULE_FILES = [
    "H300_S01_FundamentalRules_Rules.json",
    "H300_S01a_Aspects_Rules.json",
    "H300_S02_StarLordSystem_Rules.json",
    "H300_S03_VMD_Rules.json",
    "H300_S04_Nodes_Rules.json",
]

# 6 intra-book superseded rules → active: False
SUPERSEDED_RULES = {
    "h300-s02-010",  # overlaps h300-s01a-001..005 + h300-s01a-010 (aspects reiteration)
    "h300-s02-011",  # overlaps h300-s01a-011 (Rahu/Ketu 4-level hierarchy -- 2nd time)
    "h300-s02-012",  # overlaps h300-s01a-012 (planets in node stars -- 2nd time)
    "h300-s04-003",  # overlaps h300-s01a-011, h300-s02-011 (4-level hierarchy -- 3rd time)
    "h300-s04-006",  # overlaps h300-s01a-012, h300-s02-012 (planets in node stars -- 3rd time)
    "h300-s04-007",  # overlaps h300-s01a-001..005, h300-s02-010 (aspects -- 3rd reiteration)
}

# 2 TT-decision duplicate candidates → pending_review: True + decode_notes
TT_DECISION_RULES: dict[str, str] = {
    "h300-s01a-009": (
        "TT review required: Rule states 'Lagna or Moon Sign may be used as 1st house'. "
        "KP Jyotish strictly uses Placidus lagna -- Moon sign substitution may conflict with "
        "KP orthodoxy. Requires co-founder decision whether to keep or deactivate."
    ),
    "h300-s03-004": (
        "TT review required: Rule groups Sun, Mars, Ketu, Moon as the four short-period dasha "
        "planets. Verify against Longevity book categorisation -- Longevity may treat these "
        "individually rather than as an explicit group. Co-founder to confirm canonical phrasing."
    ),
}


def _map_interpretation(rule: dict) -> dict[str, str]:
    """Build interpretation.detailed + summary from top-level full_text and summary fields."""
    detailed = (rule.get("full_text") or "").strip()
    summary = (rule.get("summary") or "").strip()

    # Fallback: if full_text empty, try result.effect
    if not detailed:
        result = rule.get("result") or {}
        detailed = (result.get("effect") or "").strip()

    # Fallback: summary from detailed
    if not summary and detailed:
        summary = detailed[:120].rsplit(" ", 1)[0]

    return {
        "detailed": detailed,
        "summary": summary,
    }


def _map_source(rule: dict) -> dict[str, Any]:
    """Build canonical source dict, always with batch_id overridden to BATCH_ID."""
    src = rule.get("source") or {}
    out: dict[str, Any] = {}
    # Preserve all existing source fields
    for k, v in src.items():
        out[k] = v
    # Override batch_id -- MANDATORY: validate_rules.py queries this field
    out["batch_id"] = BATCH_ID
    return out


def inject_fields(rule: dict, now_iso: str) -> dict[str, Any]:
    """Transform one source rule to canonical MongoDB document."""
    out = dict(rule)  # shallow copy

    # --- Core overrides (per thread brief Step 2) ---
    out["approval_status"] = "pending_human_review"
    out["ingested_at"] = now_iso
    out["ingest_batch_id"] = BATCH_ID
    out["source_book"] = "300 Horoscopes Vol 1"
    out["source"] = _map_source(rule)

    # --- Interpretation --- (source has null interpretation; build from full_text + summary)
    out["interpretation"] = _map_interpretation(rule)

    # --- Superseded rules --- (intra-book overlap, not useful as standalone)
    rule_id = rule.get("rule_id", "")
    if rule_id in SUPERSEDED_RULES:
        out["active"] = False

    # --- TT-decision duplicate candidates ---
    if rule_id in TT_DECISION_RULES:
        out["pending_review"] = True
        out["decode_notes"] = TT_DECISION_RULES[rule_id]

    return out


def load_source_rules() -> list[dict]:
    """Load all rules from the 5 H300 rule JSON files."""
    all_rules: list[dict] = []
    for fname in RULE_FILES:
        fpath = SOURCE_FOLDER / fname
        if not fpath.exists():
            print(f"[ERROR] Source file not found: {fpath}", file=sys.stderr)
            sys.exit(1)
        rules = json.loads(fpath.read_text())
        if not isinstance(rules, list):
            print(f"[ERROR] {fname} did not parse to a list", file=sys.stderr)
            sys.exit(1)
        all_rules.extend(rules)
        print(f"  Loaded {len(rules):3d} rules from {fname}")
    return all_rules


def structural_check(rules: list[dict]) -> list[tuple[str, str]]:
    """Verify all transformed rules pass structural requirements before upload."""
    issues: list[tuple[str, str]] = []
    for r in rules:
        rid = r.get("rule_id", "?")
        interp = r.get("interpretation") or {}
        detailed = (interp.get("detailed") or "").strip()
        summary = (interp.get("summary") or "").strip()

        if not detailed and not summary:
            issues.append((rid, "empty_interpretation"))
        elif not detailed:
            issues.append((rid, "empty_interpretation.detailed"))
        elif not summary:
            issues.append((rid, "empty_interpretation.summary"))

        src = r.get("source") or {}
        if not src.get("batch_id"):
            issues.append((rid, "missing_source.batch_id"))
        elif src["batch_id"] != BATCH_ID:
            issues.append((rid, f"wrong_source.batch_id:{src['batch_id']}"))

        if r.get("ingest_batch_id") != BATCH_ID:
            issues.append((rid, f"wrong_ingest_batch_id:{r.get('ingest_batch_id')}"))

        if r.get("approval_status") != "pending_human_review":
            issues.append((rid, f"wrong_approval_status:{r.get('approval_status')}"))

        cond = r.get("condition")
        if not cond or not isinstance(cond, dict):
            issues.append((rid, "missing_or_invalid_condition"))

    # Verify superseded rules are inactive
    for rid in SUPERSEDED_RULES:
        matching = [r for r in rules if r.get("rule_id") == rid]
        if matching and matching[0].get("active") is not False:
            issues.append((rid, "superseded_rule_not_marked_inactive"))

    # Verify TT-decision rules have pending_review flag
    for rid in TT_DECISION_RULES:
        matching = [r for r in rules if r.get("rule_id") == rid]
        if matching and not matching[0].get("pending_review"):
            issues.append((rid, "tt_decision_rule_missing_pending_review_flag"))

    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest 300 Horoscopes Vol 1 rules.")
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument("--dry-run", action="store_true",
                        help="Transform and validate rules but do not write to MongoDB.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print(f"\n{'='*60}")
    print(f" 300 Horoscopes Vol 1 -- KE Ingest")
    print(f" Batch ID: {BATCH_ID}")
    print(f" Mode:  {'DRY RUN' if args.dry_run else 'LIVE UPLOAD'}")
    print(f"{'='*60}\n")

    # --- Load source rules ---
    print("Loading source rules:")
    source_rules = load_source_rules()
    print(f"\nTotal source rules loaded: {len(source_rules)}")

    # --- Transform ---
    now_iso = datetime.now(timezone.utc).isoformat()
    transformed: list[dict] = []
    for rule in source_rules:
        transformed.append(inject_fields(rule, now_iso))

    # --- Structural check ---
    issues = structural_check(transformed)
    if issues:
        print(f"\n[ERROR] Structural check FAILED -- {len(issues)} issue(s):")
        for rid, msg in issues:
            print(f"  {rid}: {msg}")
        sys.exit(1)
    print(f"\nStructural check: PASSED (Issues: 0)")

    # --- Preview sample rules ---
    print("\n── Sample rules (first 3 active, first superseded, first TT-decision) ──")
    shown = 0
    for r in transformed:
        if shown >= 3 and r.get("rule_id") not in SUPERSEDED_RULES and r.get("rule_id") not in TT_DECISION_RULES:
            continue
        if shown < 3 or r.get("rule_id") in SUPERSEDED_RULES or r.get("rule_id") in TT_DECISION_RULES:
            tag = ""
            if r.get("rule_id") in SUPERSEDED_RULES:
                tag = " [SUPERSEDED → active:False]"
            elif r.get("rule_id") in TT_DECISION_RULES:
                tag = " [TT-DECISION → pending_review:True]"
            print(f"\n  {r['rule_id']}{tag}")
            print(f"    approval_status: {r.get('approval_status')}")
            print(f"    active:          {r.get('active', True)}")
            print(f"    source.batch_id: {r['source'].get('batch_id','?')}")
            print(f"    interp.summary:  {r['interpretation']['summary'][:80]}...")
            print(f"    interp.detailed: {r['interpretation']['detailed'][:100]}...")
            shown += 1
        if shown >= 5:
            break

    # --- Summary counts ---
    superseded_count = sum(1 for r in transformed if r.get("rule_id") in SUPERSEDED_RULES)
    tt_count = sum(1 for r in transformed if r.get("rule_id") in TT_DECISION_RULES)
    active_count = sum(1 for r in transformed if r.get("active", True) is not False)
    print(f"\n── Transform Summary ──")
    print(f"  Total rules:              {len(transformed)}")
    print(f"  Active rules:             {active_count}")
    print(f"  Superseded (active=False): {superseded_count}")
    print(f"  TT-decision (flagged):    {tt_count}")
    print(f"  approval_status:          pending_human_review (all)")

    if args.dry_run:
        print("\n[DRY RUN] No data written to MongoDB.")
        print("Run without --dry-run to upload.\n")
        return

    # --- MongoDB upload ---
    if not args.mongo_url:
        print("[ERROR] --mongo-url not provided and MONGO_URL env var not set.", file=sys.stderr)
        sys.exit(1)

    try:
        from pymongo import MongoClient
    except ImportError:
        print("[ERROR] pymongo not installed.", file=sys.stderr)
        sys.exit(1)

    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=15000)
    db = client[args.db_name]

    # Idempotency guard
    existing = db["import_batches"].find_one({"batch_id": BATCH_ID})
    if existing:
        print(f"\n[ABORT] batch_id '{BATCH_ID}' already in import_batches. Idempotency guard.")
        print("Delete the import_batches record and re-run to force re-ingest.\n")
        sys.exit(1)

    print(f"\n── Uploading {len(transformed)} rules to {args.db_name}.interpretation_rules ──")
    inserted = 0
    skipped = 0
    for r in transformed:
        rid = r.get("rule_id")
        existing_rule = db["interpretation_rules"].find_one(
            {"rule_id": rid, "ingest_batch_id": BATCH_ID}, {"_id": 1}
        )
        if existing_rule:
            print(f"  [SKIP] {rid} -- already exists in this batch")
            skipped += 1
        else:
            db["interpretation_rules"].insert_one(r)
            inserted += 1

    # Import batch record
    db["import_batches"].insert_one({
        "batch_id":        BATCH_ID,
        "source_book":     "300 Horoscopes Vol 1",
        "rules_inserted":  inserted,
        "rules_skipped":   skipped,
        "created_at":      now_iso,
        "notes": (
            f"57 KP Jyotish rules. "
            f"{superseded_count} superseded (active:False): h300-s02-010/011/012, h300-s04-003/006/007. "
            f"{tt_count} TT-decision flags: h300-s01a-009 (lagna/moon-sign), h300-s03-004 (short-dasha grouping). "
            f"Pre-ingest dedup: 0 matches vs 10,414 MongoDB rules. "
            f"approval_status=pending_human_review for all (AI validator bypassed -- TT reviews at approval)."
        ),
    })

    print(f"\n── Upload Complete ──")
    print(f"  Inserted:  {inserted}")
    print(f"  Skipped:   {skipped}")
    print(f"  DB record: {args.db_name}.import_batches → {BATCH_ID}\n")

    # Verification query
    total_in_db = db["interpretation_rules"].count_documents(
        {"ingest_batch_id": BATCH_ID}
    )
    active_in_db = db["interpretation_rules"].count_documents(
        {"ingest_batch_id": BATCH_ID, "active": {"$ne": False}}
    )
    phr_in_db = db["interpretation_rules"].count_documents(
        {"ingest_batch_id": BATCH_ID, "approval_status": "pending_human_review"}
    )
    print(f"── Verification ──")
    print(f"  Total in DB (this batch):         {total_in_db}   (expected 57)")
    print(f"  Active rules:                     {active_in_db}  (expected 51)")
    print(f"  pending_human_review:             {phr_in_db}  (expected 57)\n")


if __name__ == "__main__":
    main()
