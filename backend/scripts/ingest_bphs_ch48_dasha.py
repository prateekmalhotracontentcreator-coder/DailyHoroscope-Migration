"""
ingest_bphs_ch48_dasha.py
KE Ingest -- BPHS Vol 2 Ch.48 Distinctive Effects of Vimshottari Dasa Lords
Batch ID  : bphs-ch48-dasha-20260603
Rules     : 46 (R-BPHS48-001 through R-BPHS48-046)
Science ID: vedic_astrology

Sections:
  A  General placement + per-house dasa effects (1st-12th) + translator notes (R001-R023)
  B  Harsha / Sarala / Vimala yoga exceptions (R021-R023, checkable:true)
  C  Kendra-trikona favourability + association/aspect rules (R024-R035)
  D  Unfavourable positional conditions + Rahu/Ketu exceptions (R036-R046)

Schema note:
  condition.type "dasha_of_house_lord" -- confirmed in ke_schema_constants.py VALID_CONDITION_TYPES.
  Thread brief had wrong type "house_lord_position" -- corrected in decode output.
  dasha_lord: null for all per-house rules (planet-agnostic).
  dasha_lord: "rahu" / "ketu" only for R-BPHS48-045 / R-BPHS48-046.

Run:
  # Step 1 -- Dry run (saves local JSON, no MongoDB write)
  python3 backend/scripts/ingest_bphs_ch48_dasha.py --dry-run

  # Step 2 -- Dedup vs MongoDB export
  python3 backend/ke_dedup_script.py \\
    --folder-a "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/" \\
    --folder-b /tmp/mongo_existing_rules_dedup/ \\
    --output-report KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_bphs_ch48_vs_mongodb.md \\
    --threshold 0.82

  # Step 3 -- AI validate (pre-upload)
  python3 backend/scripts/validate_rules.py \\
    --json-file /tmp/bphs_ch48_rules/bphs_ch48_DRY_RUN.json \\
    --batch-id bphs-ch48-dasha-20260603

  # Step 4 -- Triage (if needed) then upload
  python3 backend/scripts/ingest_bphs_ch48_dasha.py \\
    --upload /tmp/bphs_ch48_rules/bphs_ch48_DRY_RUN_VALIDATED.json
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
BATCH_ID    = "bphs-ch48-dasha-20260603"
SCIENCE_ID  = "vedic_astrology"
SOURCE_BOOK = "BPHS Vol 2"
DB_NAME     = "horoscope_db"
LOG_DIR     = "KE_TEXTBOOK_DECODE/Dedup_Reports"

SOURCE_JSON = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/"
    "BPHS_Vol2_CC_Decode/BPHS_Ch48_Vol2_Rules.json"
)
DRY_RUN_PATH = "/tmp/bphs_ch48_rules/bphs_ch48_DRY_RUN.json"

# ---------------------------------------------------------------------------
_buf: list[str] = []


def out(msg: str = "") -> None:
    print(msg)
    _buf.append(msg)


def _write_log(log_path: str) -> None:
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    Path(log_path).write_text("\n".join(_buf) + "\n", encoding="utf-8")
    print(f"\nLog saved: {log_path}")

# ---------------------------------------------------------------------------


def load_source_rules() -> list[dict]:
    if not SOURCE_JSON.exists():
        raise FileNotFoundError(f"Source file not found: {SOURCE_JSON}")
    data = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    rules = data.get("rules", [])
    if not rules:
        raise ValueError("No rules found in source JSON.")
    out(f"  Loaded {len(rules)} rules from {SOURCE_JSON.name}")
    return rules


def inject_fields(rule: dict, now: str) -> dict:
    """Inject required ingest fields onto every rule."""
    rule["approval_status"] = "pending_review"
    rule["science_id"]      = SCIENCE_ID        # top-level, overrides metadata.science_id
    rule["source_book"]     = SOURCE_BOOK
    rule["ingest_batch_id"] = BATCH_ID
    rule["ingested_at"]     = now

    # CRITICAL: validate_rules.py queries source.batch_id
    rule.setdefault("source", {})["batch_id"] = BATCH_ID

    # Safety guard: ensure interpretation.detailed + summary populated
    interp   = rule.get("interpretation") or {}
    detailed = (interp.get("detailed") or "").strip()
    summary  = (interp.get("summary") or "").strip()
    if not detailed and not summary:
        # Fallback to result.effect if both are absent
        effect = (rule.get("result") or {}).get("effect", "")
        if effect:
            rule.setdefault("interpretation", {})["detailed"] = effect
            rule["interpretation"]["summary"] = effect

    return rule


def validate_rule_local(rule: dict) -> list[str]:
    issues = []
    interp   = rule.get("interpretation") or {}
    detailed = (interp.get("detailed") or "").strip()
    summary  = (interp.get("summary") or "").strip()
    text     = detailed or summary

    if not text:
        issues.append("empty interpretation")
    elif len(text.split()) < 8:
        issues.append(f"interpretation too short ({len(text.split())} words)")

    if not rule.get("rule_id"):
        issues.append("rule_id missing")

    cond = rule.get("condition") or {}
    if not cond.get("type"):
        issues.append("condition.type missing")

    if not (rule.get("source") or {}).get("batch_id"):
        issues.append("source.batch_id missing")

    return issues


def build_rules() -> tuple[list[dict], int]:
    now      = datetime.now(timezone.utc).isoformat()
    raw      = load_source_rules()
    rules    = []
    n_issues = 0

    for r in raw:
        rule   = inject_fields(r, now)
        issues = validate_rule_local(rule)
        if issues:
            out(f"  [ISSUE] {rule.get('rule_id','?')}: {'; '.join(issues)}")
            n_issues += len(issues)
        rules.append(rule)

    return rules, n_issues


def save_json(rules: list[dict], path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8")
    out(f"  Saved: {path}")


def print_summary(rules: list[dict]) -> None:
    sections = {
        "A-General+PerHouse": [r for r in rules if r["rule_id"] in {f"R-BPHS48-{str(i).zfill(3)}" for i in range(1, 24)}],
        "C-KendraTrikona"   : [r for r in rules if r["rule_id"] in {f"R-BPHS48-{str(i).zfill(3)}" for i in range(24, 36)}],
        "D-Unfavourable"    : [r for r in rules if r["rule_id"] in {f"R-BPHS48-{str(i).zfill(3)}" for i in range(36, 47)}],
    }
    out()
    out("  Section breakdown:")
    for label, sec in sections.items():
        out(f"    {label}: {len(sec)} rules")
    out(f"  TOTAL                    : {len(rules)}")
    out()

    polarity_counts: dict[str, int] = {}
    checkable = 0
    for r in rules:
        p = r.get("effect_polarity", "unknown")
        polarity_counts[p] = polarity_counts.get(p, 0) + 1
        if (r.get("metadata") or {}).get("checkable") or r.get("checkable"):
            checkable += 1
    out("  Polarity breakdown:")
    for p, n in sorted(polarity_counts.items()):
        out(f"    {p}: {n}")
    out(f"  Checkable (yoga_check)   : {checkable}")


def upload_rules(rules: list[dict], mongo_url: str) -> None:
    client = pymongo.MongoClient(mongo_url)
    db     = client[DB_NAME]
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
            out(f"  [ERROR] {rule.get('rule_id','?')}: {exc}")
            errors += 1

    # import_batches log
    db["import_batches"].update_one(
        {"batch_id": BATCH_ID},
        {"$set": {
            "batch_id":       BATCH_ID,
            "book":           SOURCE_BOOK,
            "chapter":        48,
            "science_id":     SCIENCE_ID,
            "description":    (
                "BPHS Vol 2 Ch.48 -- Distinctive Effects of Vimshottari Dasa Lords. "
                "46 rules: general placement principles, per-house lord dasa effects (1-12), "
                "Harsha/Sarala/Vimala yogas, kendra-trikona Raj Yoga principles, "
                "unfavourable conditions, Rahu/Ketu trishadaya exceptions."
            ),
            "rules_inserted": inserted,
            "rules_updated":  updated,
            "total_rules":    len(rules),
            "errors":         errors,
            "uploaded_at":    datetime.now(timezone.utc).isoformat(),
            "dedup_note":     (
                "Dedup vs Vol 1 local: 0 genuine duplicates "
                "(181 empty-text false positives discarded -- Ch48 rules use "
                "interpretation.detailed not full_text; dedup script limitation). "
                "Content is quality-principles chapter, not planet-specific effects -- "
                "no overlap with existing BPHS Ch47/52-58 dasha batches."
            ),
        }},
        upsert=True,
    )

    out()
    out(f"  Inserted : {inserted}")
    out(f"  Updated  : {updated}")
    out(f"  Errors   : {errors}")
    out(f"  import_batches log written for batch {BATCH_ID}")
    client.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest BPHS Ch.48 rules into horoscope_db")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true",
                      help="Parse + validate locally, save JSON, do NOT upload")
    mode.add_argument("--upload",  metavar="JSON_PATH",
                      help="Upload a previously validated JSON to MongoDB")
    parser.add_argument("--mongo-url", default=os.environ.get("MONGO_URL"),
                        help="MongoDB connection string (required for --upload)")
    parser.add_argument("--save", default=DRY_RUN_PATH,
                        help=f"Output path for dry-run JSON (default: {DRY_RUN_PATH})")
    args = parser.parse_args()

    mode_tag = "dryrun" if args.dry_run else "upload"
    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = f"{LOG_DIR}/ingest_bphs_ch48_{ts}_{mode_tag}.log"

    out("=" * 75)
    out(f"  LOG FILE : {log_path}")
    out("=" * 75)
    out()
    out(f"BPHS VOL 2 CH.48 INGEST  |  {'DRY RUN' if args.dry_run else 'UPLOAD'}")
    out(f"Batch ID  : {BATCH_ID}")
    out(f"Science ID: {SCIENCE_ID}")
    out(f"Source    : {SOURCE_JSON.name}")
    out()

    if args.dry_run:
        out("Loading + transforming source rules...")
        rules, n_issues = build_rules()
        print_summary(rules)

        if n_issues:
            out(f"⚠️  {n_issues} structural issues found. Fix before uploading.")
            _write_log(log_path)
            sys.exit(1)

        out(f"Issues    : {n_issues} ✅")
        save_json(rules, args.save)
        out()
        out("NEXT STEPS:")
        out(f"  Step 2 -- Dedup vs MongoDB export:")
        out(f"    python3 backend/ke_dedup_script.py \\")
        out(f"      --folder-a \"/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/\" \\")
        out(f"      --folder-b /tmp/mongo_existing_rules_dedup/ \\")
        out(f"      --output-report KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_bphs_ch48_vs_mongodb.md \\")
        out(f"      --threshold 0.82")
        out(f"  Step 3 -- AI validate (pre-upload):")
        out(f"    python3 backend/scripts/validate_rules.py \\")
        out(f"      --json-file {args.save} \\")
        out(f"      --batch-id {BATCH_ID}")
        out(f"  Step 4 -- Upload validated JSON:")
        out(f"    python3 backend/scripts/ingest_bphs_ch48_dasha.py \\")
        out(f"      --upload {args.save.replace('_DRY_RUN.json','_DRY_RUN_VALIDATED.json')}")

    else:  # --upload
        if not args.mongo_url:
            out("ERROR: --mongo-url required for --upload (or set MONGO_URL env var)")
            _write_log(log_path)
            sys.exit(1)

        upload_path = Path(args.upload)
        if not upload_path.exists():
            out(f"ERROR: upload file not found: {upload_path}")
            _write_log(log_path)
            sys.exit(1)

        rules = json.loads(upload_path.read_text(encoding="utf-8"))
        out(f"Loaded    : {len(rules)} rules from {upload_path.name}")
        out(f"Target    : {DB_NAME}.interpretation_rules")
        out()

        # Connection check
        client = pymongo.MongoClient(args.mongo_url)
        client.admin.command("ping")
        client.close()
        out("✅ MongoDB connection OK")
        out(f"Upserting {len(rules)} rules...")
        out()

        upload_rules(rules, args.mongo_url)

        # Status breakdown
        status_counts: dict[str, int] = {}
        for r in rules:
            s = r.get("approval_status", "unknown")
            status_counts[s] = status_counts.get(s, 0) + 1
        out()
        out("STATUS BREAKDOWN (from uploaded JSON):")
        for s, n in sorted(status_counts.items()):
            out(f"  {s}: {n}")
        out(f"  TOTAL: {len(rules)}")
        out()
        out("=" * 75)
        out("UPLOAD COMPLETE")
        out("=" * 75)
        out()
        out("NEXT STEP -- Post-upload structural validation:")
        out(f"  python3 backend/scripts/validate_ingest_batch.py \\")
        out(f"    --batch-id {BATCH_ID} \\")
        out(f"    --mongo-url \"$MONGO_URL\" --db-name {DB_NAME}")

    _write_log(log_path)


if __name__ == "__main__":
    main()
