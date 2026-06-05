#!/usr/bin/env python3
"""
ingest_destiny_numerology_phase_a.py
--------------------------------------------------------------------
Destiny Numerology Phase A -- KE Ingest (Ch03-Ch16)
310 rules across 20 non-empty files (⚠️ TT brief says 189 -- confirm post-NLM/GAI pass)

Source  : /Users/apple/Documents/Knowledge Engine_eBooks/
          DestinyNumerology_CC_Decode/
Book    : Destiny Numerology
Batch   : destiny_numerology_ch01-15_v1
Science : numerology

⚠️  STATUS: BLOCKED -- do NOT run --upload until Temple Team confirms:
    1. All 10 HIGH OCR items resolved via NLM/GAI pass (send Book_Wide_OCR_
       Inconsistencies_Report.docx to NLM/GAI decode thread)
    2. Rule count confirmed (189 per TT brief vs 310 in current decode folder)
    Brief: KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_DESTINY_NUMEROLOGY_INGEST.md

Excluded files (zero rules or non-rule schema):
  Numerology_Ch04v2_Characteristics_Rules_Part4.json  (0 rules)
  Numerology_Ch13_RepeatNumbers_Rules.json            (0 rules -- content in Part1/2)
  Numerology_Ch16_81Combinations_Rules_Part4.json     (0 rules)
  Numerology_Ch15_TestVectors.json                    (test vectors -- not KE rules)

Phase A OCR status (all HIGH items already handled in encoding):
  6-A  (Ch06 Lo Shu 8,7,6 discrepancy) -- num-ch06-017 flagged, lo_shu_source_unverifiable=True
  9-B  (Ch09 compound >=74 gap)        -- structural, existing 64 rules unaffected
  11-B (Ch11 IFSC rule)                -- num-ch11-003 flagged
  15-L (Lo Shu arrows foundational)    -- all Lo Shu arrow rules lo_shu_source_unverifiable=True
  16-B (Ch16 inferred rules)           -- all 75 Ch16 rules pending_human_review
  CRITICAL 17-A / 19-A outside Phase A (Ch17/Ch19 -- Phase B only)

Run sequence (mandatory):
  Step 1 -- Dry run + save JSON:
    python3 backend/scripts/ingest_destiny_numerology_phase_a.py --dry-run \
      --save backend/scripts/destiny_numerology_phase_a_rules.json

  Step 2 -- Pre-ingest dedup vs existing ingested books:
    python3 backend/ke_dedup_script.py \
      --folder-a /tmp/destiny_num_phase_a/ \
      --folder-b /Users/apple/Documents/Knowledge\\ Engine_eBooks/BPHS_Vol1_CC_Decode/ \
      --threshold 0.82 \
      --output-report KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_destiny_numerology_ph_a_vs_jyotish_$(date +%Y%m%d).md

  Step 3 -- Review saved JSON (spot-check per chapter)

  Step 4 -- Upload:
    python3 backend/scripts/ingest_destiny_numerology_phase_a.py \
      --upload backend/scripts/destiny_numerology_phase_a_rules.json \
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 5 -- Validate:
    python3 backend/scripts/validate_rules.py \
      --batch-id destiny-numerology-phase-a-20260604 \
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 6 -- Commit all files to git

Pre-ingest dedup  : PENDING (Step 2 above)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Constants ─────────────────────────────────────────────────────────────────

DECODE_FOLDER = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/DestinyNumerology_CC_Decode"
)

# 20 non-empty Phase A files (Ch03-Ch16), in chapter order.
# Excluded: *Part4.json files (0 rules), Ch13 base file (0 rules), Ch15 TestVectors
PHASE_A_FILES = [
    ("Numerology_Ch03_Calculations_Rules.json",             3,  "Calculation Methods"),
    ("Numerology_Ch04v2_Characteristics_Rules_Part1.json",  4,  "Number Characteristics Pt1"),
    ("Numerology_Ch04v2_Characteristics_Rules_Part2.json",  4,  "Number Characteristics Pt2"),
    ("Numerology_Ch04v2_Characteristics_Rules_Part3.json",  4,  "Number Characteristics Pt3"),
    ("Numerology_Ch05_FriendsNonFriends_Rules.json",        5,  "Friends & Non-Friends"),
    ("Numerology_Ch06_LoShuGrid_Rules.json",                6,  "Lo Shu Grid"),
    ("Numerology_Ch07_LuckyNumbers_Rules.json",             7,  "Lucky Numbers"),
    ("Numerology_Ch08_AlphabetNumbers_Rules.json",          8,  "Alphabet Number Values"),
    ("Numerology_Ch09_CompoundNumbers_Rules_Part1.json",    9,  "Compound Numbers Pt1"),
    ("Numerology_Ch09_CompoundNumbers_Rules_Part2.json",    9,  "Compound Numbers Pt2"),
    ("Numerology_Ch09_CompoundNumbers_Rules_Part3.json",    9,  "Compound Numbers Pt3"),
    ("Numerology_Ch09_CompoundNumbers_Rules_Part4.json",    9,  "Compound Numbers Pt4 (>=74 synthetic)"),
    ("Numerology_Ch10_NameCorrection_Rules.json",          10,  "Name Correction"),
    ("Numerology_Ch11_MobileNumber_Rules.json",            11,  "Mobile Number"),
    ("Numerology_Ch12_HouseNumber_Rules.json",             12,  "House Number"),
    ("Numerology_Ch13_RepeatNumbers_Rules_Part1.json",     13,  "Repeat Numbers Pt1"),
    ("Numerology_Ch13_RepeatNumbers_Rules_Part2.json",     13,  "Repeat Numbers Pt2"),
    ("Numerology_Ch14_MissingNumbers_Rules.json",          14,  "Missing Numbers"),
    ("Numerology_Ch16_81Combinations_Rules_Part1.json",    16,  "81 Combinations Pt1"),
    ("Numerology_Ch16_81Combinations_Rules_Part2.json",    16,  "81 Combinations Pt2"),
    ("Numerology_Ch16_81Combinations_Rules_Part3.json",    16,  "81 Combinations Pt3"),
]

BATCH_ID      = "destiny_numerology_ch01-15_v1"
SOURCE_BOOK   = "Destiny Numerology"
BOOK_ID       = "destiny_numerology_v1_20260518"
SCIENCE_ID    = "numerology"
EXPECTED_TOTAL = 311   # 310 Ch03-Ch16 + 1 synthetic (num-ch09-065) added per GAI Issue 9-B
                       # ⚠️ TT brief says 189 -- recount pending TT confirmation (decode may have grown post 2026-05-31)

# ── Tee-logging ───────────────────────────────────────────────────────────────

_buf: list[str] = []


def out(msg: str = "") -> None:
    print(msg)
    _buf.append(msg)


def _write_log(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(_buf), encoding="utf-8")


# ── Rule loading ──────────────────────────────────────────────────────────────

def load_rules_from_file(path: Path) -> list[dict]:
    """Load rules from a JSON file -- handles both list and dict-with-rules formats."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        out(f"  ⚠  JSON parse error in {path.name}: {e}")
        return []

    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        rules = data.get("rules", [])
        if not isinstance(rules, list):
            out(f"  ⚠  {path.name}: 'rules' key is not a list")
            return []
        return rules

    out(f"  ⚠  {path.name}: unexpected JSON root type {type(data)}")
    return []


# ── Field injection ───────────────────────────────────────────────────────────

def _build_interpretation(rule: dict) -> dict:
    """
    Build interpretation.detailed / interpretation.summary from source fields.

    Priority:
      1. full_text  → interpretation.detailed
      2. summary    → interpretation.summary  (fallback: first 200 chars of detailed)
      3. If no full_text: use summary as detailed, title as last resort.

    Idempotent: if interpretation.detailed already populated, skip.
    """
    interp = rule.get("interpretation") or {}
    if (interp.get("detailed") or "").strip():
        return rule  # already built

    full_text = (rule.get("full_text") or "").strip()
    summary   = (rule.get("summary")   or "").strip()
    title     = (rule.get("title")     or "").strip()

    if full_text:
        detailed = full_text
    elif summary:
        detailed = summary
    else:
        detailed = title  # last resort fallback

    rule["interpretation"] = {
        "detailed": detailed,
        "summary":  summary if summary else detailed[:200],
    }
    return rule


def inject_fields(rule: dict, now: str) -> dict:
    """Inject standard ingest fields into a rule dict. Returns the mutated rule."""
    # Ingest metadata
    rule["ingest_batch_id"] = BATCH_ID
    rule["ingested_at"]     = now

    # KOP-03 CRITICAL: must force-set "pending_review" (NOT "pending_human_review").
    # validate_rules.py queries approval_status="pending_review". If uploaded as
    # "pending_human_review", the AI quality check is silently skipped entirely.
    # Source files carry "pending_human_review" -- override unconditionally here.
    rule["approval_status"] = "pending_review"

    # active: default True if not set; never override an explicit False
    rule.setdefault("active", True)

    # science_id guard
    if rule.get("science_id") != SCIENCE_ID:
        rule["science_id"] = SCIENCE_ID

    # source dict: patch missing fields + overwrite batch_id for validate_rules.py
    source = rule.get("source")
    if not isinstance(source, dict):
        source = {}
        rule["source"] = source

    if not source.get("book"):
        source["book"] = SOURCE_BOOK
    if not source.get("book_id"):
        source["book_id"] = BOOK_ID

    # MANDATORY: source.batch_id is queried by validate_rules.py
    source["batch_id"] = BATCH_ID

    # Build interpretation layer
    rule = _build_interpretation(rule)

    return rule


# ── Build ─────────────────────────────────────────────────────────────────────

def build_all_rules() -> tuple[list[dict], list[tuple]]:
    """Load all Phase A rules, inject fields, return (rules, per_file_stats)."""
    now       = datetime.now(timezone.utc).isoformat()
    all_rules = []
    stats     = []   # (filename, ch, title, count)
    seen_ids  = {}

    for filename, ch, ch_title in PHASE_A_FILES:
        path = DECODE_FOLDER / filename
        if not path.exists():
            out(f"  ✗  File not found: {path}")
            stats.append((filename, ch, ch_title, 0))
            continue

        raw_rules = load_rules_from_file(path)
        file_rules = []

        for rule in raw_rules:
            if not isinstance(rule, dict):
                continue
            rid = rule.get("rule_id")
            if not rid:
                out(f"  ⚠  Rule without rule_id in {filename} -- skipped")
                continue
            if rid in seen_ids:
                out(f"  ⚠  Duplicate rule_id {rid} in {filename} "
                    f"(first seen in {seen_ids[rid]}) -- skipped")
                continue
            seen_ids[rid] = filename
            file_rules.append(inject_fields(rule, now))

        stats.append((filename, ch, ch_title, len(file_rules)))
        all_rules.extend(file_rules)

    return all_rules, stats


# ── Structural check ──────────────────────────────────────────────────────────

def local_structural_check(rules: list[dict]) -> int:
    """
    Pre-upload sanity check. Returns issue count.
    Mirrors key checks from validate_rules.py.
    """
    issues = 0
    for r in rules:
        rid = r.get("rule_id", "(no id)")
        interp = r.get("interpretation") or {}

        if not interp.get("detailed"):
            out(f"  [ISSUE] {rid}: interpretation.detailed is empty")
            issues += 1
        if not interp.get("summary"):
            out(f"  [ISSUE] {rid}: interpretation.summary is empty")
            issues += 1
        if r.get("approval_status") != "pending_review":
            out(f"  [ISSUE] {rid}: approval_status wrong "
                f"({r.get('approval_status')!r}) -- expected 'pending_review' (KOP-03)")
            issues += 1
        src = r.get("source", {})
        if src.get("batch_id") != BATCH_ID:
            out(f"  [ISSUE] {rid}: source.batch_id mismatch ({src.get('batch_id')!r})")
            issues += 1
        if r.get("ingest_batch_id") != BATCH_ID:
            out(f"  [ISSUE] {rid}: ingest_batch_id mismatch ({r.get('ingest_batch_id')!r})")
            issues += 1

    return issues


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    today   = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")
    log_path = log_dir / f"ingest_destiny_num_phase_a_{today}.log"

    parser = argparse.ArgumentParser(
        description="Destiny Numerology Phase A ingest -- 310 rules (Ch03-Ch16)"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Build and validate rules in memory, no DB write")
    parser.add_argument("--save", metavar="PATH",
                        help="Save built rules to JSON (use with --dry-run)")
    parser.add_argument("--upload", metavar="PATH",
                        help="Upload rules from saved JSON to MongoDB")
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    parser.add_argument("--db-name",   default="horoscope_db")
    args = parser.parse_args()

    if not args.dry_run and not args.upload:
        parser.error("Specify --dry-run [--save PATH] or --upload PATH")

    out("=" * 70)
    out(f"LOG FILE: {log_path}")
    out(f"DESTINY NUMEROLOGY PHASE A INGEST  |  batch: {BATCH_ID}")
    out(f"Scope: Ch03-Ch16 ({EXPECTED_TOTAL} rules, 20 files)")
    out("=" * 70)

    # ── DRY RUN ───────────────────────────────────────────────────────────────
    if args.dry_run:
        out(f"\nSource folder : {DECODE_FOLDER}")
        out(f"Files         : {len(PHASE_A_FILES)}")
        out(f"\nBuilding rules...")

        all_rules, stats = build_all_rules()

        out(f"\n{'─' * 70}")
        out(f"  {'File':<48} {'Ch':>3}  {'Rules':>6}")
        out(f"{'─' * 70}")
        ch_totals: dict[int, int] = {}
        for fname, ch, ch_title, count in stats:
            out(f"  {fname:<48} {ch:>3}  {count:>6}")
            ch_totals[ch] = ch_totals.get(ch, 0) + count
        out(f"{'─' * 70}")
        out(f"  {'TOTAL':<48}       {len(all_rules):>6}")
        out(f"{'─' * 70}\n")

        out("Rules by chapter:")
        for ch, count in sorted(ch_totals.items()):
            out(f"  Ch{ch:02d}: {count}")
        out()

        # Local structural check
        out(f"Running local structural check...")
        issues = local_structural_check(all_rules)
        out(f"Issues found: {issues}")
        if issues:
            out("  ✗  Fix issues before uploading.")
            _write_log(log_path)
            print(f"\nLog saved: {log_path}")
            sys.exit(1)
        else:
            out("  ✓  All rules pass structural check.")

        # Spot-check first and last rule
        if all_rules:
            r0 = all_rules[0]
            out(f"\nSpot-check first rule ({r0['rule_id']}):")
            out(f"  approval_status  : {r0.get('approval_status')}")
            out(f"  ingest_batch_id  : {r0.get('ingest_batch_id')}")
            out(f"  source.batch_id  : {r0.get('source', {}).get('batch_id')}")
            out(f"  source.chapter   : {r0.get('source', {}).get('chapter')}")
            out(f"  interp.detailed  : {repr((r0['interpretation']['detailed'])[:80])}")
            out(f"  interp.summary   : {repr((r0['interpretation']['summary'])[:80])}")

            rN = all_rules[-1]
            out(f"\nSpot-check last rule ({rN['rule_id']}):")
            out(f"  approval_status  : {rN.get('approval_status')}")
            out(f"  ingest_batch_id  : {rN.get('ingest_batch_id')}")
            out(f"  source.batch_id  : {rN.get('source', {}).get('batch_id')}")
            out(f"  source.chapter   : {rN.get('source', {}).get('chapter')}")
            out(f"  interp.detailed  : {repr((rN['interpretation']['detailed'])[:80])}")
            out(f"  interp.summary   : {repr((rN['interpretation']['summary'])[:80])}")

        # Count rules with each flag
        phr_count  = sum(1 for r in all_rules if r.get("approval_status") == "pending_human_review")
        lo_shu_flag = sum(1 for r in all_rules if r.get("lo_shu_source_unverifiable"))
        out(f"\nFlag summary:")
        out(f"  pending_human_review      : {phr_count}")
        out(f"  lo_shu_source_unverifiable: {lo_shu_flag}")
        out(f"  active=False              : {sum(1 for r in all_rules if r.get('active') == False)}")

        # Count gap vs full_text
        with_full_text = sum(1 for r in all_rules if (r.get("full_text") or "").strip())
        out(f"  rules with full_text      : {with_full_text}")
        out(f"  rules without full_text   : {len(all_rules) - with_full_text}")

        if args.save:
            save_path = Path(args.save)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_text(
                json.dumps(all_rules, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            out(f"\nSaved {len(all_rules)} rules → {save_path}")

        if len(all_rules) != EXPECTED_TOTAL:
            out(f"\n  ⚠  Expected {EXPECTED_TOTAL} rules -- got {len(all_rules)}. "
                f"Verify source files.")
        else:
            out(f"\n  ✓  Rule count matches expected {EXPECTED_TOTAL}.")

        out(f"\n✓ Dry run complete.")
        out(f"  Next steps:")
        out(f"    1. Review {args.save or 'output JSON'}")
        out(f"    2. Run pre-ingest dedup vs existing ingested books (see script header)")
        out(f"    3. Re-run with --upload PATH after dedup passes")

        _write_log(log_path)
        print(f"\nLog saved: {log_path}")
        return

    # ── UPLOAD ────────────────────────────────────────────────────────────────
    if args.upload:
        upload_path = Path(args.upload)
        if not upload_path.exists():
            out(f"✗  Upload file not found: {upload_path}")
            _write_log(log_path)
            print(f"\nLog saved: {log_path}")
            sys.exit(1)

        if not args.mongo_url:
            out("✗  MONGO_URL not set. Export it or pass --mongo-url.")
            _write_log(log_path)
            print(f"\nLog saved: {log_path}")
            sys.exit(1)

        try:
            from pymongo import MongoClient
        except ImportError as e:
            out(f"✗  Missing dependency: {e}")
            _write_log(log_path)
            print(f"\nLog saved: {log_path}")
            sys.exit(1)

        rules = json.loads(upload_path.read_text(encoding="utf-8"))
        out(f"\nLoaded {len(rules)} rules from {upload_path}")

        # Final structural check before touching DB
        out("Running final structural check before upload...")
        issues = local_structural_check(rules)
        out(f"Issues found: {issues}")
        if issues:
            out("✗  Fix issues before uploading. Aborting.")
            _write_log(log_path)
            print(f"\nLog saved: {log_path}")
            sys.exit(1)

        client = MongoClient(args.mongo_url)
        db     = client[args.db_name]
        col    = db["interpretation_rules"]
        batches_col = db["import_batches"]

        # Pre-check for already-ingested rule_ids
        rule_ids = [r["rule_id"] for r in rules]
        existing_ids = set(
            d["rule_id"] for d in col.find(
                {"rule_id": {"$in": rule_ids}},
                {"rule_id": 1}
            )
        )
        new_rules = [r for r in rules if r["rule_id"] not in existing_ids]
        skipped   = len(rules) - len(new_rules)

        if skipped:
            out(f"  ⚠  {skipped} rules already in DB -- skipped (upsert not used; "
                f"re-run with fresh batch_id if you need to overwrite)")

        if not new_rules:
            out("  Nothing to insert. All rules already present in DB.")
            client.close()
            _write_log(log_path)
            print(f"\nLog saved: {log_path}")
            return

        result = col.insert_many(new_rules)
        inserted = len(result.inserted_ids)
        out(f"\n  ✓  Inserted {inserted} rules into {args.db_name}.interpretation_rules")

        # Record batch in import_batches
        now_ts = datetime.now(timezone.utc).isoformat()
        chapters = sorted({r.get("source", {}).get("chapter") for r in new_rules
                           if r.get("source", {}).get("chapter")})
        batches_col.update_one(
            {"batch_id": BATCH_ID},
            {"$set": {
                "batch_id":       BATCH_ID,
                "source_book":    SOURCE_BOOK,
                "science_id":     SCIENCE_ID,
                "chapters":       chapters,
                "rules_inserted": inserted,
                "rules_skipped":  skipped,
                "uploaded_at":    now_ts,
                "status":         "ingested",
                "phase":          "A",
                "notes":          "Ch03-Ch16. Ch15 TestVectors excluded (not KE rules).",
            }},
            upsert=True,
        )
        out(f"  ✓  import_batches record upserted  (batch_id: {BATCH_ID})")
        out(f"     chapters ingested: {chapters}")

        # Verification query
        count = col.count_documents({"ingest_batch_id": BATCH_ID})
        out(f"\n  Verification: db.interpretation_rules.count_documents"
            f"({{\"ingest_batch_id\": \"{BATCH_ID}\"}}) = {count}")

        if count != EXPECTED_TOTAL:
            out(f"  ⚠  Expected {EXPECTED_TOTAL} -- got {count}. "
                f"Check for pre-existing rules that were skipped (skipped={skipped}).")
        else:
            out(f"  ✓  Count matches expected {EXPECTED_TOTAL}.")

        client.close()
        out(f"\n✓ Upload complete.")
        out(f"  Next: python3 backend/scripts/validate_rules.py "
            f"--batch-id {BATCH_ID} --mongo-url \"$MONGO_URL\" --db-name horoscope_db")

        _write_log(log_path)
        print(f"\nLog saved: {log_path}")


if __name__ == "__main__":
    main()
