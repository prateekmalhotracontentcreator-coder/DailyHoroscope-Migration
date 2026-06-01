#!/usr/bin/env python3
"""
ingest_bphs_vol2_ch49_51.py
--------------------------------------------------------------------
BPHS Vol 2, Chapters 49-51 -- KE Ingest
249 rules (248 active, 1 source gap)

Source  : /Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/
Files   : BPHS_Vol2_Ch49_Rules.json (154 rules)
          BPHS_Vol2_Ch50_Rules.json  (73 rules)
          BPHS_Vol2_Ch51_Rules.json  (22 rules)
          *** Part files are LEGACY -- skipped ***

Batch ID: bphs-vol2-ch49-51-v1

Special handling:
  - bphs2-ch49-gemini-pada-8-gap  : active=false, source_gap=true -- ingested as-is
  - bphs2-ch51-020                : provisional=true -- ingested as-is, TT review before approval
  - Ch50 combustion rules         : decode_notes carry BPHS Ch07 cross-ref -- do NOT override

Run sequence (mandatory):
  Step 1 -- Dry run + save JSON:
    python3 backend/scripts/ingest_bphs_vol2_ch49_51.py --dry-run \
      --save backend/scripts/bphs_vol2_ch49_51_rules.json

  Step 2 -- Review saved JSON (spot-check first + last rule per chapter)

  Step 3 -- Upload:
    python3 backend/scripts/ingest_bphs_vol2_ch49_51.py \
      --upload backend/scripts/bphs_vol2_ch49_51_rules.json \
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 4 -- Validate:
    python3 backend/scripts/validate_rules.py \
      --batch-id bphs-vol2-ch49-51-v1 \
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 5 -- Inspect flagged rules, write patch script if needed
  Step 6 -- Commit all files to git

Pre-ingest dedup:  PASSED  (0 duplicates, 0 contradictions vs BPHS Vol 1)
Dedup report   :  dedup_bphs_vol2_vs_vol1.md
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

DECODE_FOLDER = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode"
)

# Only ingest master files -- Part files are legacy superseded versions
CANONICAL_FILES = [
    "BPHS_Vol2_Ch49_Rules.json",   # Ch49  154 rules
    "BPHS_Vol2_Ch50_Rules.json",   # Ch50   73 rules
    "BPHS_Vol2_Ch51_Rules.json",   # Ch51   22 rules
]

BATCH_ID   = "bphs-vol2-ch49-51-v1"
BOOK_NAME  = "BPHS Vol 2"
SCIENCE_ID = "jyotish"
BOOK_ID    = "bphs_vol2_20260526"

CHAPTER_TITLES = {
    49: "Effects of the Kalachakra Dasa",
    50: "Effects of the Chara etc. Dasas",
    51: "Working out of Antardasas",
}

# Rules that must NOT have active overridden
PRESERVE_ACTIVE_FALSE = {"bphs2-ch49-gemini-pada-8-gap"}


def load_rules_from_file(path: Path) -> list[dict]:
    """Load rules from a JSON file -- handles both list and dict-with-rules formats."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"  ⚠  JSON parse error in {path.name}: {e}", file=sys.stderr)
        return []

    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        rules = data.get("rules", [])
        if not isinstance(rules, list):
            print(f"  ⚠  {path.name}: 'rules' key is not a list", file=sys.stderr)
            return []
        return rules

    print(f"  ⚠  {path.name}: unexpected JSON root type {type(data)}", file=sys.stderr)
    return []


def _map_interpretation(rule: dict) -> dict:
    """
    Map Vol 2 source fields → canonical interpretation.detailed / interpretation.summary.

    Vol 2 schema (Schema B equivalent):
      full_text  → interpretation.detailed
      summary    → interpretation.summary  (fallback: first 200 chars of full_text)

    If interpretation.detailed or summary is already populated, skip (idempotent).
    """
    interp = rule.get("interpretation") or {}
    if (interp.get("detailed") or "").strip() or (interp.get("summary") or "").strip():
        return rule  # already populated

    full_text = (rule.get("full_text") or "").strip()
    summary   = (rule.get("summary")   or "").strip()

    rule["interpretation"] = {
        "detailed": full_text,
        "summary":  summary if summary else full_text[:200],
    }
    return rule


def _map_condition(rule: dict) -> dict:
    """
    Ensure rule["condition"] is a non-empty dict.

    Vol 2 rules already have condition as a dict -- this is a defensive
    fallback consistent with Phase 2 template.
    """
    if isinstance(rule.get("condition"), dict) and rule["condition"]:
        return rule  # already correct

    conditions = rule.get("conditions", [])
    if isinstance(conditions, list) and conditions:
        rule["condition"] = conditions[0]
    else:
        rule_type = rule.get("type") or rule.get("rule_type") or "general_principle"
        rule["condition"] = {"type": rule_type}

    return rule


def inject_fields(rule: dict, now: str) -> dict:
    """Inject standard ingest fields. Preserves active=false for source-gap rules."""
    rule["approval_status"] = "pending_review"
    rule["ingest_batch_id"] = BATCH_ID
    rule["source_book"]     = BOOK_NAME
    rule["ingested_at"]     = now

    # Preserve active=false and stamp source_gap for known source-gap rules
    rid = rule.get("rule_id", "")
    if rid in PRESERVE_ACTIVE_FALSE:
        rule["active"]      = False
        rule["source_gap"]  = True
    else:
        rule.setdefault("active", True)

    # science_id
    if rule.get("science_id") not in ("jyotish",):
        rule["science_id"] = SCIENCE_ID

    # source dict -- patch missing fields
    source = rule.get("source")
    if not isinstance(source, dict):
        source = {}
        rule["source"] = source

    if not source.get("book_id"):
        source["book_id"] = BOOK_ID

    if not source.get("book"):
        source["book"] = BOOK_NAME

    # MANDATORY: source.batch_id (validate_rules.py queries this, not ingest_batch_id)
    source["batch_id"] = BATCH_ID

    # Schema normalisation
    rule = _map_interpretation(rule)
    rule = _map_condition(rule)

    return rule


def build_all_rules() -> tuple[list[dict], dict]:
    """Load, inject, and return all 249 rules with per-chapter counts."""
    now       = datetime.now(timezone.utc).isoformat()
    all_rules = []
    ch_counts = {}
    seen_ids  = {}

    for filename in CANONICAL_FILES:
        path = DECODE_FOLDER / filename
        if not path.exists():
            print(f"  ✗  File not found: {path}", file=sys.stderr)
            continue

        rules = load_rules_from_file(path)
        ch_rules = []

        for rule in rules:
            if not isinstance(rule, dict):
                continue
            rid = rule.get("rule_id")
            if not rid:
                print(f"  ⚠  Rule without rule_id in {filename} -- skipped")
                continue
            if rid in seen_ids:
                print(f"  ⚠  Duplicate rule_id {rid} in {filename} "
                      f"(first seen in {seen_ids[rid]}) -- skipped")
                continue
            seen_ids[rid] = filename
            ch_rules.append(inject_fields(rule, now))

        # Derive chapter number from source field of first rule
        ch_num = None
        if ch_rules:
            src = ch_rules[0].get("source", {})
            ch_num = src.get("chapter")
        ch_counts[filename] = (ch_num, len(ch_rules))
        all_rules.extend(ch_rules)

    return all_rules, ch_counts


def local_structural_check(rules: list[dict]) -> int:
    """
    Pre-upload sanity check. Returns issue count.
    Mirrors the key checks from validate_rules.py so we catch schema failures
    before touching MongoDB.
    """
    issues = 0
    for r in rules:
        rid = r.get("rule_id", "(no id)")
        interp = r.get("interpretation") or {}

        if not interp.get("detailed"):
            print(f"  [ISSUE] {rid}: interpretation.detailed is empty")
            issues += 1
        if not interp.get("summary"):
            print(f"  [ISSUE] {rid}: interpretation.summary is empty")
            issues += 1
        if not isinstance(r.get("condition"), dict) or not r.get("condition"):
            print(f"  [ISSUE] {rid}: condition is missing or empty dict")
            issues += 1
        src = r.get("source", {})
        if src.get("batch_id") != BATCH_ID:
            print(f"  [ISSUE] {rid}: source.batch_id mismatch ({src.get('batch_id')!r})")
            issues += 1
        if r.get("approval_status") != "pending_human_review":
            print(f"  [ISSUE] {rid}: approval_status wrong ({r.get('approval_status')!r})")
            issues += 1

    return issues


def main():
    parser = argparse.ArgumentParser(
        description="BPHS Vol 2 Ch49-51 ingest -- 249 rules"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Build and validate rules in memory, no DB write")
    parser.add_argument("--save", metavar="PATH",
                        help="Save built rules to JSON (use with --dry-run)")
    parser.add_argument("--upload", metavar="PATH",
                        help="Upload rules from saved JSON to MongoDB")
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    parser.add_argument("--db-name", default="horoscope_db")
    args = parser.parse_args()

    if not args.dry_run and not args.upload:
        parser.error("Specify --dry-run [--save PATH] or --upload PATH")

    print("\n" + "=" * 70)
    print(f"BPHS VOL 2 CH49-51 INGEST  |  batch: {BATCH_ID}")
    print("=" * 70)

    # ── DRY RUN ───────────────────────────────────────────────────────────────
    if args.dry_run:
        print(f"\nSource folder : {DECODE_FOLDER}")
        print(f"Canonical files: {CANONICAL_FILES}")
        print(f"\nBuilding rules...")

        all_rules, ch_counts = build_all_rules()

        print(f"\n{'─' * 70}")
        print(f"{'File':<42} {'Ch':>4}  {'Rules':>6}")
        print(f"{'─' * 70}")
        for fname, (ch_num, count) in ch_counts.items():
            title = CHAPTER_TITLES.get(ch_num, "")
            print(f"  {fname:<40} {str(ch_num):>4}  {count:>6}   {title}")
        print(f"{'─' * 70}")
        print(f"  {'TOTAL':<40}       {len(all_rules):>6}")
        print(f"{'─' * 70}\n")

        # Special rule status
        for rid in PRESERVE_ACTIVE_FALSE:
            match = next((r for r in all_rules if r.get("rule_id") == rid), None)
            if match:
                print(f"  source_gap rule  : {rid}  active={match.get('active')}  "
                      f"source_gap={match.get('source_gap')}")
            else:
                print(f"  ⚠  source_gap rule not found: {rid}")

        prov = [r for r in all_rules if r.get("provisional")]
        if prov:
            for r in prov:
                print(f"  provisional rule : {r['rule_id']}  provisional={r.get('provisional')}")

        # Local structural check
        print(f"\nRunning local structural check...")
        issues = local_structural_check(all_rules)
        print(f"Issues: {issues}")
        if issues:
            print("  ✗  Fix issues before uploading.")
            sys.exit(1)
        else:
            print("  ✓  All rules pass structural check.")

        # Sample spot-check: first and last rule
        if all_rules:
            print(f"\nSpot-check first rule ({all_rules[0]['rule_id']}):")
            r0 = all_rules[0]
            print(f"  approval_status : {r0.get('approval_status')}")
            print(f"  source.batch_id : {r0.get('source', {}).get('batch_id')}")
            print(f"  interp.detailed : {repr(r0['interpretation']['detailed'][:80])}")
            print(f"  interp.summary  : {repr(r0['interpretation']['summary'][:80])}")
            print(f"  condition       : {r0.get('condition')}")

            print(f"\nSpot-check last rule ({all_rules[-1]['rule_id']}):")
            rN = all_rules[-1]
            print(f"  approval_status : {rN.get('approval_status')}")
            print(f"  source.batch_id : {rN.get('source', {}).get('batch_id')}")
            print(f"  interp.detailed : {repr(rN['interpretation']['detailed'][:80])}")
            print(f"  interp.summary  : {repr(rN['interpretation']['summary'][:80])}")

        if args.save:
            save_path = Path(args.save)
            save_path.write_text(
                json.dumps(all_rules, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            print(f"\nSaved {len(all_rules)} rules → {save_path}")

        print(f"\n✓ Dry run complete. {len(all_rules)} rules ready.")
        print(f"  Next: review {args.save or 'output'}, then re-run with --upload PATH")
        return

    # ── UPLOAD ────────────────────────────────────────────────────────────────
    if args.upload:
        upload_path = Path(args.upload)
        if not upload_path.exists():
            print(f"✗  Upload file not found: {upload_path}", file=sys.stderr)
            sys.exit(1)

        if not args.mongo_url:
            print("✗  MONGO_URL not set. Export it or pass --mongo-url.", file=sys.stderr)
            sys.exit(1)

        try:
            import motor.motor_asyncio  # noqa: F401 -- confirm motor is available
            from pymongo import MongoClient
        except ImportError as e:
            print(f"✗  Missing dependency: {e}", file=sys.stderr)
            sys.exit(1)

        rules = json.loads(upload_path.read_text(encoding="utf-8"))
        print(f"\nLoaded {len(rules)} rules from {upload_path}")

        # Final structural check before touching DB
        print("Running final structural check before upload...")
        issues = local_structural_check(rules)
        print(f"Issues: {issues}")
        if issues:
            print("✗  Fix issues before uploading. Aborting.")
            sys.exit(1)

        client = MongoClient(args.mongo_url)
        db     = client[args.db_name]
        col    = db["interpretation_rules"]
        batches_col = db["import_batches"]

        # Deduplicate against existing DB rules
        existing_ids = set(
            d["rule_id"] for d in col.find(
                {"rule_id": {"$in": [r["rule_id"] for r in rules]}},
                {"rule_id": 1}
            )
        )
        new_rules = [r for r in rules if r["rule_id"] not in existing_ids]
        skipped   = len(rules) - len(new_rules)

        if skipped:
            print(f"  ⚠  {skipped} rules already in DB -- skipped (no overwrite)")

        if not new_rules:
            print("  Nothing to insert. All rules already present.")
            client.close()
            return

        result = col.insert_many(new_rules)
        inserted = len(result.inserted_ids)
        print(f"\n  ✓  Inserted {inserted} rules into {args.db_name}.interpretation_rules")

        # Record batch in import_batches
        now = datetime.now(timezone.utc).isoformat()
        batches_col.update_one(
            {"batch_id": BATCH_ID},
            {"$set": {
                "batch_id":     BATCH_ID,
                "source_book":  BOOK_NAME,
                "chapters":     [49, 50, 51],
                "rules_inserted": inserted,
                "rules_skipped":  skipped,
                "uploaded_at":  now,
                "status":       "ingested",
            }},
            upsert=True,
        )
        print(f"  ✓  import_batches record upserted  (batch_id: {BATCH_ID})")

        # Verification query
        count = col.count_documents({"ingest_batch_id": BATCH_ID})
        print(f"\n  Verification: db.interpretation_rules.count_documents"
              f"({{\"ingest_batch_id\": \"{BATCH_ID}\"}}) = {count}")

        if count != 249:
            print(f"  ⚠  Expected 249 -- got {count}. "
                  f"Check for pre-existing rules that were skipped.")
        else:
            print(f"  ✓  Count matches expected 249.")

        client.close()
        print(f"\n✓ Upload complete.")
        print(f"  Next: run validate_rules.py --batch-id {BATCH_ID}")


if __name__ == "__main__":
    main()
