"""
ingest_longevity_unnatural_v1.py
KE Ingest -- Longevity & Unnatural Death
Batch ID : longevity_unnatural_v1
Rules    : 44 (S01: 10, S02: 7, S03: 6, S04: 21)
Source   : /Users/apple/Documents/Knowledge Engine_eBooks/LongevityUnnatural_CC_Decode/
science_id: kp_jyotish

Schema:
  Source field   → Canonical field
  full_text      → interpretation.detailed
  summary        → interpretation.summary
  condition      → condition (pass-through, already a dict)
  result         → result (pass-through)
  claim_axis     → overridden to "longevity" for ALL rules (thread brief mandate)

MEDIUM rules (pending_review: True -- open doctrinal questions, safe to ingest):
  lu-s04-007/008/009  -- aayu bucket mutual exclusivity tiebreaker not specified
  lu-s04-016/017/018  -- suicide conditions: sufficient vs necessary ambiguity
  lu-s02-006          -- "connected" definition for 10th-8th longevity link
  lu-s03-005          -- star lord absorption when star lord already Level 1
  (2 further MEDIUM items may be identified by TT during co-founder review)

Run:
  # Step 1 -- Dry run
  python3 backend/scripts/ingest_longevity_unnatural_v1.py --dry-run

  # Step 2 -- Dedup vs MongoDB (run from repo root)
  # (Source files already match *_Rules*.json pattern -- run directly)
  python3 backend/ke_dedup_script.py \\
    --folder-a "/Users/apple/Documents/Knowledge Engine_eBooks/LongevityUnnatural_CC_Decode/" \\
    --folder-b /tmp/mongo_existing_rules_dedup/ \\
    --output-report dedup_longunnat_vs_mongodb.md \\
    --threshold 0.82

  # Step 2B -- AI validate local JSON (pre-upload)
  python3 backend/scripts/validate_rules.py \\
    --json-file /tmp/longevity_unnatural_rules/longevity_unnatural_DRY_RUN.json \\
    --batch-id longevity_unnatural_v1

  # Step 3 -- Upload validated JSON
  python3 backend/scripts/ingest_longevity_unnatural_v1.py \\
    --upload /tmp/longevity_unnatural_rules/longevity_unnatural_DRY_RUN_VALIDATED.json \\
    --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import pymongo

# ---------------------------------------------------------------------------
BATCH_ID      = "longevity_unnatural_v1"
SCIENCE_ID    = "kp_jyotish"
SOURCE_BOOK   = "Longevity & Unnatural Death"
CLAIM_AXIS    = "longevity"   # Override for ALL rules -- thread brief mandate

SOURCE_DIR = Path("/Users/apple/Documents/Knowledge Engine_eBooks/LongevityUnnatural_CC_Decode/")

SOURCE_FILES = [
    ("S01", "LU_S01_FundamentalRules_Rules.json"),
    ("S02", "LU_S02_HousePlanetSignifications_Rules.json"),
    ("S03", "LU_S03_NodeSignifications_Rules.json"),
    ("S04", "LU_S04_BadhakaMaraka_Rules.json"),
]

# Rules with open doctrinal questions -- safe to ingest, flagged for TT review
MEDIUM_RULES: set[str] = {
    "lu-s04-007",   # Aayu bucket mutual exclusivity -- tiebreaker not specified in source
    "lu-s04-008",   # Aayu bucket mutual exclusivity -- tiebreaker not specified
    "lu-s04-009",   # Aayu bucket mutual exclusivity -- tiebreaker not specified
    "lu-s04-016",   # Suicide route 1 (12th): sufficient vs necessary ambiguity
    "lu-s04-017",   # Suicide route 2 (8th): sufficient vs necessary ambiguity
    "lu-s04-018",   # Suicide route 3 (lagna): sufficient vs necessary ambiguity
    "lu-s02-006",   # 10th-8th longevity link: "connected" not precisely defined
    "lu-s03-005",   # Star lord absorption: ambiguous when star lord is already Level 1
}
# ---------------------------------------------------------------------------


def load_source_rules() -> list[dict]:
    """Load all rules from the 4 section JSON files."""
    all_rules: list[dict] = []
    for section, fname in SOURCE_FILES:
        fpath = SOURCE_DIR / fname
        if not fpath.exists():
            raise FileNotFoundError(f"Source file not found: {fpath}")
        rules = json.loads(fpath.read_text(encoding="utf-8"))
        if not isinstance(rules, list):
            raise ValueError(f"{fname}: expected a JSON array at root, got {type(rules).__name__}")
        print(f"  {section} ({fname}): {len(rules)} rules")
        all_rules.extend(rules)
    return all_rules


def transform_rule(r: dict, now: str) -> dict:
    """
    Map source schema → canonical KE schema.

    Source fields used:
      rule_id, science_id, active, title, full_text, summary,
      tags, category, condition, claim_scope, claim_polarity,
      timing_bias, strength_band, result, decode_notes, checkable
    """
    rule_id = r["rule_id"]

    # --- interpretation block ---
    full_text = (r.get("full_text") or "").strip()
    summary   = (r.get("summary")   or "").strip()

    interpretation = {
        "detailed": full_text,
        "summary":  summary,
    }

    # --- source block ---
    source = dict(r.get("source") or {})
    source["book"]     = SOURCE_BOOK
    source["batch_id"] = BATCH_ID       # MANDATORY for validate_rules.py

    # --- condition (pass-through, already a dict) ---
    condition = r.get("condition") or {}
    if not isinstance(condition, dict):
        condition = {"type": "engine_specification"}

    # --- result (pass-through dict) ---
    result = r.get("result") or {}

    # --- build canonical rule ---
    rule: dict = {
        "rule_id":          rule_id,
        "science_id":       SCIENCE_ID,
        "active":           r.get("active", True),
        "approval_status":  "pending_review",   # validator queues on this
        "checkable":        r.get("checkable", False),
        "source":           source,
        "source_book":      SOURCE_BOOK,
        "ingest_batch_id":  BATCH_ID,
        "ingested_at":      now,
        "title":            r.get("title", ""),
        "interpretation":   interpretation,
        "condition":        condition,
        "result":           result,
        "claim_axis":       CLAIM_AXIS,          # Override -- all rules = longevity
        "claim_scope":      r.get("claim_scope", ""),
        "claim_polarity":   r.get("claim_polarity", ""),
        "timing_bias":      r.get("timing_bias", ""),
        "strength_band":    r.get("strength_band", ""),
        "tags":             r.get("tags", []),
        "category":         r.get("category", ""),
    }

    # Preserve decode_notes if present
    if r.get("decode_notes"):
        rule["decode_notes"] = r["decode_notes"]

    # Flag MEDIUM items
    if rule_id in MEDIUM_RULES:
        rule["pending_review"] = True
        rule["pending_review_reason"] = (
            "MEDIUM: open doctrinal question in source diagnostic -- "
            "safe to ingest, TT to resolve at co-founder review stage."
        )

    return rule


def validate_rule_local(rule: dict) -> list[str]:
    """Structural check mirroring validate_rules.py Stage 1."""
    issues = []
    interp   = rule.get("interpretation") or {}
    detailed = (interp.get("detailed") or "").strip()
    summary  = (interp.get("summary")  or "").strip()
    text     = detailed or summary

    if not text:
        issues.append("empty interpretation")
    elif len(text.split()) < 8:
        issues.append(f"interpretation too short ({len(text.split())} words)")
    elif text[-1] not in ".!?\"')":
        issues.append(f"possible truncation (ends '{text[-1]}')")

    if not isinstance(rule.get("condition"), dict) or not rule.get("condition"):
        issues.append("condition missing or empty")

    if not rule.get("rule_id"):
        issues.append("rule_id missing")

    if not (rule.get("source") or {}).get("batch_id"):
        issues.append("source.batch_id missing")

    return issues


def build_rules() -> tuple[list[dict], int]:
    """Load, transform, and validate all rules. Returns (rules, issue_count)."""
    now = datetime.now(timezone.utc).isoformat()
    raw_rules = load_source_rules()

    rules: list[dict] = []
    total_issues = 0

    for r in raw_rules:
        rule = transform_rule(r, now)
        issues = validate_rule_local(rule)
        if issues:
            print(f"  [ISSUE] {rule['rule_id']}: {'; '.join(issues)}")
            total_issues += len(issues)
        rules.append(rule)

    return rules, total_issues


def save_json(rules: list[dict], path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Saved: {path}")


def upload_rules(rules: list[dict], mongo_url: str) -> None:
    client = pymongo.MongoClient(mongo_url)
    db     = client["horoscope_db"]
    col    = db["interpretation_rules"]

    inserted = updated = errors = 0
    for rule in rules:
        try:
            res = col.update_one(
                {"rule_id": rule["rule_id"]},
                {"$set": rule},
                upsert=True,
            )
            if res.upserted_id:
                inserted += 1
            elif res.modified_count:
                updated += 1
        except Exception as exc:
            print(f"  [ERROR] {rule['rule_id']}: {exc}")
            errors += 1

    # Log import batch
    db["import_batches"].update_one(
        {"batch_id": BATCH_ID},
        {"$set": {
            "batch_id":        BATCH_ID,
            "book":            SOURCE_BOOK,
            "science_id":      SCIENCE_ID,
            "rules_inserted":  inserted,
            "rules_updated":   updated,
            "total_rules":     len(rules),
            "errors":          errors,
            "uploaded_at":     datetime.now(timezone.utc).isoformat(),
        }},
        upsert=True,
    )

    print(f"\n  Inserted : {inserted}")
    print(f"  Updated  : {updated}")
    print(f"  Errors   : {errors}")
    print(f"  import_batches log updated for batch {BATCH_ID}")
    client.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest Longevity & Unnatural Death rules")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run",  action="store_true",
                      help="Parse + validate locally, save JSON, do NOT upload")
    mode.add_argument("--upload",   metavar="JSON_PATH",
                      help="Upload a previously saved (and validated) JSON to MongoDB")
    parser.add_argument("--mongo-url", default=os.environ.get("MONGO_URL"),
                        help="MongoDB connection string (required for --upload)")
    parser.add_argument("--save",   default="/tmp/longevity_unnatural_rules/longevity_unnatural_DRY_RUN.json",
                        help="Output path for dry-run JSON")
    args = parser.parse_args()

    if args.dry_run:
        print("\nLONGEVITY UNNATURAL DEATH INGEST  |  DRY RUN")
        print("=" * 60)
        print("\nLoading source files...")
        rules, issues = build_rules()

        print(f"\n  S01 Fundamental Rules  : {sum(1 for r in rules if r['rule_id'].startswith('lu-s01'))}")
        print(f"  S02 House/Planet Sigs  : {sum(1 for r in rules if r['rule_id'].startswith('lu-s02'))}")
        print(f"  S03 Node Significations: {sum(1 for r in rules if r['rule_id'].startswith('lu-s03'))}")
        print(f"  S04 Badhaka/Maraka     : {sum(1 for r in rules if r['rule_id'].startswith('lu-s04'))}")
        print(f"  TOTAL                  : {len(rules)}")
        print(f"  MEDIUM (pending_review): {sum(1 for r in rules if r.get('pending_review'))}")
        print(f"  Issues                 : {issues}")

        if issues:
            print("\n  ⚠️  STOP -- fix issues before uploading.")
            sys.exit(1)

        save_json(rules, args.save)

        print(f"""
NEXT STEPS:
  Step 2 -- Dedup vs MongoDB:
    python3 backend/ke_dedup_script.py \\
      --folder-a "/Users/apple/Documents/Knowledge Engine_eBooks/LongevityUnnatural_CC_Decode/" \\
      --folder-b /tmp/mongo_existing_rules_dedup/ \\
      --output-report dedup_longunnat_vs_mongodb.md \\
      --threshold 0.82

  Step 2B -- AI Validate (pre-upload):
    python3 backend/scripts/validate_rules.py \\
      --json-file {args.save} \\
      --batch-id {BATCH_ID}

  Step 3 -- Upload validated JSON:
    python3 backend/scripts/ingest_longevity_unnatural_v1.py \\
      --upload {args.save.replace('_DRY_RUN.json', '_DRY_RUN_VALIDATED.json')} \\
      --mongo-url "$MONGO_URL"
""")

    elif args.upload:
        if not args.mongo_url:
            raise SystemExit("ERROR: --mongo-url required for --upload (or set MONGO_URL env var)")

        upload_path = Path(args.upload)
        if not upload_path.exists():
            raise SystemExit(f"ERROR: upload file not found: {upload_path}")

        rules = json.loads(upload_path.read_text(encoding="utf-8"))
        print(f"\nLONGEVITY UNNATURAL DEATH INGEST  |  batch: {BATCH_ID}")
        print("=" * 60)
        print(f"\nLoaded {len(rules)} rules from {args.upload}")
        print(f"Target: horoscope_db.interpretation_rules")
        print(f"Batch : {BATCH_ID}")

        # Quick connection check
        client = pymongo.MongoClient(args.mongo_url)
        client.admin.command("ping")
        client.close()
        print("✅ MongoDB connection OK")

        print(f"Upserting {len(rules)} rules...\n")
        upload_rules(rules, args.mongo_url)

        print(f"\n{'=' * 60}")
        print("UPLOAD COMPLETE")
        print("=" * 60)
        print(f"""
NEXT STEP -- Post-upload structural validation:
  python3 backend/scripts/validate_ingest_batch.py \\
    --batch-id {BATCH_ID} \\
    --mongo-url "$MONGO_URL" --db-name horoscope_db
""")


if __name__ == "__main__":
    main()
