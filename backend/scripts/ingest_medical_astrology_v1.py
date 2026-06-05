"""
ingest_medical_astrology_v1.py
KE Ingest -- Medical Astrology (Text Book) by Dr. S. Krishna Kumar
Batch ID  : medical_astrology_v1
Rules     : 270 (Ch01: 127, Ch02: 79, Ch03: 6, Ch04: 8, Ch05: 19,
                  Ch06: 17, Ch09: 10, Ch10: 2, Ch11: 2)
science_id: vedic_astrology
Source    : /Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode/

Two source schemas in the decode folder:

  Schema A (239 rules) -- Ch01, Ch02 parts 1-3, Ch03, Ch05, Ch09, Ch10
    Has: source block, top-level summary + full_text, result dict
    Map: full_text → interpretation.detailed
         summary   → interpretation.summary
         result    → result (pass-through)

  Schema B (31 rules) -- Ch02 Part4, Ch04, Ch06, Ch11
    Has: top-level batch_id/book_id/chapter, full_text, outcome dict
    Map: full_text          → interpretation.detailed
         outcome.primary    → interpretation.summary
         outcome            → result (normalised)
         source constructed from book_id, chapter, batch_id

Special flags (from OCR audit + Grade B resolutions):
  ma-ch03-005   gai_citation_unverified: true  (B-11 Rigveda 1.91.16 quote)

Grade C items (C-1 through C-6) are all benchmark data quality issues (Ch7
case logs). Ch7 has 0 ingested rules. No Grade C flags needed on the 270 rules.

Run:
  # Step 1 -- Dry run (parse + validate locally, save JSON)
  python3 backend/scripts/ingest_medical_astrology_v1.py --dry-run

  # Step 2 -- Dedup vs MongoDB full export
  python3 backend/ke_dedup_script.py \\
    --folder-a "/Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode/" \\
    --folder-b /tmp/mongo_existing_rules_dedup/ \\
    --output-report KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_medastro_vs_mongodb.md \\
    --threshold 0.82

  # Step 2B -- AI validate local JSON (pre-upload)
  python3 backend/scripts/validate_rules.py \\
    --json-file /tmp/medical_astrology_rules/medical_astrology_v1_DRY_RUN.json \\
    --batch-id medical_astrology_v1

  # Step 3 -- Upload validated JSON
  python3 backend/scripts/ingest_medical_astrology_v1.py \\
    --upload /tmp/medical_astrology_rules/medical_astrology_v1_DRY_RUN_VALIDATED.json
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
BATCH_ID    = "medical_astrology_v1"
SCIENCE_ID  = "vedic_astrology"
SOURCE_BOOK = "Medical Astrology"
LOG_DIR     = "KE_TEXTBOOK_DECODE/Dedup_Reports"

SOURCE_DIR = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode/"
)

# (filename, schema_type, chapter_label)
SOURCE_FILES: list[tuple[str, str, str]] = [
    # --- Schema A ---
    ("MedAstro_Ch01_DefinitionsYogas_Rules_Part1.json", "A", "Ch01"),
    ("MedAstro_Ch01_DefinitionsYogas_Rules_Part2.json", "A", "Ch01"),
    ("MedAstro_Ch01_DefinitionsYogas_Rules_Part3.json", "A", "Ch01"),
    ("MedAstro_Ch01_DefinitionsYogas_Rules_Part4.json", "A", "Ch01"),
    ("MedAstro_Ch01_DefinitionsYogas_Rules_Part5.json", "A", "Ch01"),
    ("MedAstro_Ch01_DefinitionsYogas_Rules_Part6.json", "A", "Ch01"),
    ("MedAstro_Ch02_ProgenyAndCurses_Rules_Part1.json", "A", "Ch02"),
    ("MedAstro_Ch02_ProgenyAndCurses_Rules_Part2.json", "A", "Ch02"),
    ("MedAstro_Ch02_ProgenyAndCurses_Rules_Part3.json", "A", "Ch02"),
    ("MedAstro_Ch03_MokshaAndSon_Rules.json",           "A", "Ch03"),
    ("MedAstro_Ch05_FemaleHoroscopy_Rules.json",        "A", "Ch05"),
    ("MedAstro_Ch09_DurationStars_Rules.json",          "A", "Ch09"),
    ("MedAstro_Ch10_PediatricRemedies_Rules.json",      "A", "Ch10"),
    # --- Schema B ---
    ("MedAstro_Ch02_ProgenyAndCurses_Rules_Part4.json", "B", "Ch02"),
    ("MedAstro_Ch04_SexualWeakness_Rules.json",         "B", "Ch04"),
    ("MedAstro_Ch06_VariousDiseases_Rules.json",        "B", "Ch06"),
    ("MedAstro_Ch11_Drekkana_Rules.json",               "B", "Ch11"),
]

# Rules requiring gai_citation_unverified flag (OCR Grade B resolutions)
# ma-ch03-005: B-11 Rigveda 1.91.16 / Moon-semen Vedic quote -- GAI reconstructed,
#              not independently verified from Sanskrit original
GAI_CITATION_UNVERIFIED: set[str] = {"ma-ch03-005"}

# ---------------------------------------------------------------------------
# Tee logger -- all output goes to stdout AND the log buffer simultaneously.
# log_path and buf are set at the start of main() before any output.
# ---------------------------------------------------------------------------
_buf: list[str] = []


def out(msg: str = "") -> None:
    """Print msg to stdout and append to log buffer."""
    print(msg)
    _buf.append(msg)


def _write_log(log_path: str) -> None:
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    Path(log_path).write_text("\n".join(_buf) + "\n", encoding="utf-8")
    # Print log-saved line AFTER writing (not buffered -- terminal only)
    print(f"\nLog saved: {log_path}")


# ---------------------------------------------------------------------------


def load_source_rules() -> list[tuple[dict, str, str]]:
    """
    Load all rules from source files.
    Returns list of (raw_rule, schema_type, chapter_label) tuples.
    """
    all_rules: list[tuple[dict, str, str]] = []
    for fname, schema, chapter in SOURCE_FILES:
        fpath = SOURCE_DIR / fname
        if not fpath.exists():
            raise FileNotFoundError(f"Source file not found: {fpath}")
        data = json.loads(fpath.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError(
                f"{fname}: expected JSON array at root, got {type(data).__name__}"
            )
        if not data:
            out(f"  {fname}: 0 rules (empty) -- skipped")
            continue
        out(f"  {chapter} {schema} ({fname}): {len(data)} rules")
        for rule in data:
            all_rules.append((rule, schema, chapter))
    return all_rules


def _map_schema_a(r: dict, now: str) -> dict:
    """
    Map Schema A source rule → canonical KE schema.
    Schema A: has source block, top-level summary + full_text, result dict.
    """
    rule_id = r["rule_id"]

    # interpretation
    full_text = (r.get("full_text") or "").strip()
    summary   = (r.get("summary")   or "").strip()
    interpretation = {"detailed": full_text, "summary": summary}

    # source block -- already present; stamp batch_id + book name
    source = dict(r.get("source") or {})
    source["book"]     = SOURCE_BOOK
    source["batch_id"] = BATCH_ID

    # result -- pass through
    result = r.get("result") or {}
    if not isinstance(result, dict):
        result = {}

    # condition -- pass through
    condition = r.get("condition") or {}
    if not isinstance(condition, dict):
        condition = {"type": "engine_specification"}

    rule: dict = {
        "rule_id":         rule_id,
        "science_id":      SCIENCE_ID,
        "active":          r.get("active", True),
        "approval_status": "pending_review",
        "checkable":       r.get("checkable", False),
        "source":          source,
        "source_book":     SOURCE_BOOK,
        "ingest_batch_id": BATCH_ID,
        "ingested_at":     now,
        "title":           r.get("title", ""),
        "interpretation":  interpretation,
        "condition":       condition,
        "result":          result,
        "claim_axis":      r.get("claim_axis", ""),
        "claim_scope":     r.get("claim_scope", ""),
        "claim_polarity":  r.get("claim_polarity", ""),
        "timing_bias":     r.get("timing_bias", ""),
        "strength_band":   r.get("strength_band", ""),
        "tags":            r.get("tags", []),
        "category":        r.get("category", ""),
    }

    for opt in ("yoga_name", "decode_notes", "vedic_layer",
                "remedy_available", "remedy_ref_id", "passage_ref_id"):
        if r.get(opt) is not None:
            rule[opt] = r[opt]

    return rule


def _map_schema_b(r: dict, now: str) -> dict:
    """
    Map Schema B source rule → canonical KE schema.
    Schema B: top-level batch_id/book_id/chapter, full_text, outcome dict.
    """
    rule_id = r["rule_id"]

    # interpretation
    full_text = (r.get("full_text") or "").strip()
    outcome   = r.get("outcome") or {}
    primary   = (outcome.get("primary") or "").strip()
    if not primary and full_text:
        primary = full_text.split(".")[0].strip()
    interpretation = {"detailed": full_text, "summary": primary}

    # Construct source block (Schema B has no source block)
    source = {
        "book":              SOURCE_BOOK,
        "book_id":           r.get("book_id", "medical_astrology_v1_20260518"),
        "chapter":           r.get("chapter"),
        "batch_id":          BATCH_ID,
        "passage_ref_id":    r.get("passage_ref_id"),
        "source_page_range": r.get("source_page_range"),
    }

    # Normalise outcome → result
    result = {
        "effect":           outcome.get("primary", ""),
        "mechanism":        outcome.get("mechanism", ""),
        "severity":         outcome.get("severity"),
        "disease_category": r.get("disease_category", ""),
        "body_system":      r.get("body_system", ""),
        "body_part":        r.get("body_part", ""),
        "aayu_bucket":      r.get("aayu_bucket"),
        "remedy_available": r.get("remedy_available", False),
        "remedy_ref_id":    r.get("remedy_ref_id"),
    }

    # condition -- pass through
    condition = r.get("condition") or {}
    if not isinstance(condition, dict):
        condition = {"type": "engine_specification"}

    rule: dict = {
        "rule_id":         rule_id,
        "science_id":      SCIENCE_ID,
        "active":          r.get("active", True),
        "approval_status": "pending_review",
        "checkable":       r.get("checkable", False),
        "source":          source,
        "source_book":     SOURCE_BOOK,
        "ingest_batch_id": BATCH_ID,
        "ingested_at":     now,
        "title":           r.get("title", ""),
        "interpretation":  interpretation,
        "condition":       condition,
        "result":          result,
        "claim_axis":      r.get("claim_axis", ""),
        "claim_scope":     r.get("claim_scope", ""),
        "claim_polarity":  r.get("claim_polarity", ""),
        "timing_bias":     r.get("timing_bias", ""),
        "strength_band":   r.get("strength_band", ""),
        "tags":            r.get("tags", []),
        "category":        r.get("category", ""),
    }

    for opt in ("yoga_name", "decode_notes", "vedic_layer",
                "passage_ref_id", "source_page_range"):
        if r.get(opt) is not None:
            rule[opt] = r[opt]

    return rule


def transform_rule(r: dict, schema: str, now: str) -> dict:
    """Dispatch to schema-specific mapper, then apply special flags."""
    rule = _map_schema_a(r, now) if schema == "A" else _map_schema_b(r, now)

    if rule["rule_id"] in GAI_CITATION_UNVERIFIED:
        rule["gai_citation_unverified"] = True
        rule["pending_review"] = True
        rule["pending_review_reason"] = (
            "GAI_CITATION_UNVERIFIED: classical text citation (Rigveda 1.91.16) "
            "reconstructed by GAI -- cross-check specific sloka ref before "
            "co-founder approval."
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
    elif len(text.split()) < 6:
        issues.append(f"interpretation very short ({len(text.split())} words)")
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
    """Load, transform, validate all rules. Returns (rules, issue_count)."""
    now = datetime.now(timezone.utc).isoformat()
    raw = load_source_rules()

    rules: list[dict] = []
    total_issues = 0

    for r, schema, chapter in raw:
        rule   = transform_rule(r, schema, now)
        issues = validate_rule_local(rule)
        if issues:
            out(f"  [ISSUE] {rule['rule_id']}: {'; '.join(issues)}")
            total_issues += len(issues)
        rules.append(rule)

    return rules, total_issues


def save_json(rules: list[dict], path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(
        json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    out(f"  Saved: {path}")


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
            out(f"  [ERROR] {rule['rule_id']}: {exc}")
            errors += 1

    db["import_batches"].update_one(
        {"batch_id": BATCH_ID},
        {"$set": {
            "batch_id":       BATCH_ID,
            "book":           SOURCE_BOOK,
            "science_id":     SCIENCE_ID,
            "rules_inserted": inserted,
            "rules_updated":  updated,
            "total_rules":    len(rules),
            "errors":         errors,
            "uploaded_at":    datetime.now(timezone.utc).isoformat(),
            "notes": (
                "Medical Astrology by Dr. S. Krishna Kumar. "
                "270 rules (vedic_astrology). "
                "Two source schemas: A (239 rules) + B (31 rules). "
                "ma-ch03-005 flagged gai_citation_unverified (B-11 Rigveda quote). "
                "Grade C items are benchmark data quality issues only -- no rule flags needed."
            ),
        }},
        upsert=True,
    )

    out(f"")
    out(f"  Inserted : {inserted}")
    out(f"  Updated  : {updated}")
    out(f"  Errors   : {errors}")
    out(f"  import_batches log written for batch {BATCH_ID}")
    client.close()


def print_summary(rules: list[dict], issues: int) -> None:
    ch_counts: dict[str, int] = {}
    for r in rules:
        ch = (r.get("source") or {}).get("chapter") or "?"
        ch_counts[str(ch)] = ch_counts.get(str(ch), 0) + 1

    out(f"")
    out(f"  {'Chapter':<10} {'Rules':>6}")
    out(f"  {'-'*10} {'-'*6}")
    for ch in sorted(ch_counts, key=lambda x: int(x) if str(x).isdigit() else 99):
        out(f"  {'Ch' + str(ch):<10} {ch_counts[ch]:>6}")
    out(f"  {'TOTAL':<10} {len(rules):>6}")
    out(f"")

    schema_b_ids      = {"ma-ch02-076", "ma-ch02-077", "ma-ch02-078", "ma-ch02-079"}
    schema_b_prefixes = ("ma-ch04-", "ma-ch06-", "ma-ch11-")
    schema_b_count    = sum(
        1 for r in rules
        if r["rule_id"].startswith(schema_b_prefixes)
        or r["rule_id"] in schema_b_ids
    )
    out(f"  Schema A (source block)  : {len(rules) - schema_b_count}")
    out(f"  Schema B (outcome-based) : {schema_b_count}")
    out(f"  gai_citation_unverified  : {sum(1 for r in rules if r.get('gai_citation_unverified'))}")
    out(f"  pending_review           : {sum(1 for r in rules if r.get('pending_review'))}")
    out(f"  Issues                   : {issues}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest Medical Astrology rules into horoscope_db"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--dry-run", action="store_true",
        help="Parse + validate locally, save JSON, do NOT upload"
    )
    mode.add_argument(
        "--upload", metavar="JSON_PATH",
        help="Upload a previously saved (and validated) JSON to MongoDB"
    )
    parser.add_argument(
        "--mongo-url", default=os.environ.get("MONGO_URL"),
        help="MongoDB connection string (or set MONGO_URL env var)"
    )
    parser.add_argument(
        "--save",
        default="/tmp/medical_astrology_rules/medical_astrology_v1_DRY_RUN.json",
        help="Output path for dry-run JSON"
    )
    args = parser.parse_args()

    # --- Log path computed FIRST so it appears in the opening header ---
    mode_tag = "dryrun" if args.dry_run else "upload"
    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = f"{LOG_DIR}/ingest_medical_astrology_v1_{ts}_{mode_tag}.log"

    out("=" * 75)
    out(f"  LOG FILE : {log_path}")
    out("=" * 75)

    if args.dry_run:
        out(f"")
        out(f"MEDICAL ASTROLOGY INGEST  |  DRY RUN")
        out(f"Batch ID  : {BATCH_ID}")
        out(f"Science   : {SCIENCE_ID}")
        out(f"Target    : horoscope_db.interpretation_rules")
        out(f"")
        out(f"Loading source files...")

        rules, issues = build_rules()
        print_summary(rules, issues)

        if issues:
            out(f"")
            out(f"⚠️  STOP -- fix issues before uploading.")
            _write_log(log_path)
            sys.exit(1)

        save_json(rules, args.save)

        validated_path = args.save.replace("_DRY_RUN.json", "_DRY_RUN_VALIDATED.json")
        out(f"""
NEXT STEPS:
  Step 2 -- Dedup vs MongoDB export:
    python3 backend/ke_dedup_script.py \\
      --folder-a "/Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode/" \\
      --folder-b /tmp/mongo_existing_rules_dedup/ \\
      --output-report KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_medastro_vs_mongodb.md \\
      --threshold 0.82

  Step 2B -- AI Validate (pre-upload):
    python3 backend/scripts/validate_rules.py \\
      --json-file {args.save} \\
      --batch-id {BATCH_ID}

  Step 3 -- Upload validated JSON:
    python3 backend/scripts/ingest_medical_astrology_v1.py \\
      --upload {validated_path}""")

    elif args.upload:
        if not args.mongo_url:
            out(f"ERROR: MONGO_URL not set. Run: export MONGO_URL='...' then re-run.")
            _write_log(log_path)
            raise SystemExit(1)

        upload_path = Path(args.upload)
        if not upload_path.exists():
            out(f"ERROR: upload file not found: {upload_path}")
            _write_log(log_path)
            raise SystemExit(1)

        rules = json.loads(upload_path.read_text(encoding="utf-8"))

        out(f"")
        out(f"MEDICAL ASTROLOGY INGEST  |  UPLOAD")
        out(f"Batch ID  : {BATCH_ID}")
        out(f"Loaded    : {len(rules)} rules from {args.upload}")
        out(f"Target    : horoscope_db.interpretation_rules")
        out(f"")

        client = pymongo.MongoClient(args.mongo_url)
        client.admin.command("ping")
        client.close()
        out(f"✅ MongoDB connection OK")
        out(f"")
        out(f"Upserting {len(rules)} rules...")

        upload_rules(rules, args.mongo_url)

        out(f"")
        out(f"=" * 75)
        out(f"UPLOAD COMPLETE")
        out(f"=" * 75)
        out(f"""
NEXT STEP -- Post-upload structural validation:
  python3 backend/scripts/validate_ingest_batch.py \\
    --batch-id {BATCH_ID} \\
    --mongo-url "$MONGO_URL" --db-name horoscope_db""")

    _write_log(log_path)


if __name__ == "__main__":
    main()
