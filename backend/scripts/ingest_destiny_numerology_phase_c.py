#!/usr/bin/env python3
"""
ingest_destiny_numerology_phase_c.py
--------------------------------------------------------------------
Destiny Numerology Phase C -- KE Ingest (Ch20-Ch28 + Derived Rules)
103 rules across 12 files

Source  : /Users/apple/Documents/Knowledge Engine_eBooks/
          DestinyNumerology_CC_Decode/
Book    : Destiny Numerology
Batch   : destiny_numerology_phase_c_20260604
Science : numerology

Chapters (core, 39 rules):
  Ch20 -- Cyclones, Tsunamis & Hurricanes  ( 3 rules)
  Ch21 -- Pandemic Framework               ( 1 rule ) [Issue 21-A: chapter_name
                                                        is internal; display as
                                                        "Pandemic Numerology Framework"]
  Ch22 -- Major Earthquakes                ( 3 rules)
  Ch23 -- Nation Name Numbers              ( 5 rules)
  Ch24 -- City/State Numbers               ( 3 rules)
  Ch25 -- Fire Countries                   ( 2 rules)
  Ch26 -- Company Numbers                  ( 6 rules) [Issue 26-A: 4-way routing
                                                        confirmed by GAI]
  Ch27 -- Company Logos                    ( 6 rules)
  Ch28 -- Remarriage / Marumangalya        (10 rules) [Issue 28-A: weekday table
                                                        withheld -- expert referral.
                                                        Issue 28-B: Number 6
                                                        loophole locked to marriage
                                                        destiny dates only]

Derived rules (64 rules):
  CareerAlignment        (31 rules) -- no source block; synthetic injected
  PersonalYearCycle      (12 rules) -- non-standard source block; batch_id injected
  CaseDerivedInference   (21 rules) -- no source block; result.interpretation → detailed

GAI issues:
  26-A: 4-way routing matrix for Rahu/Number 4 CONFIRMED -- engine-level, no patch
  28-A: Withheld weekday table -- freeze automation, redirect to expert referral
  28-B: Number 6 marriage loophole LOCKED to marriage destiny dates only
  21-A: Ch21 chapter_name masked at display layer; source.chapter_name stays internal

Notes:
  - source.book in Ch20-Ch28 source files = "Your Destiny Is In Your Name & DOB"
    (OCR artefact). Force-overridden to "Destiny Numerology" for all rules.
  - CDI rules use result.interpretation as interpretation.detailed (richer than summary)
  - PYC rules retain their non-standard source fields; batch_id is added

Run sequence:
  Step 1 -- Dry run + save JSON:
    python3 backend/scripts/ingest_destiny_numerology_phase_c.py --dry-run \\
      --save backend/scripts/destiny_numerology_phase_c_rules.json

  Step 2 -- Upload:
    python3 backend/scripts/ingest_destiny_numerology_phase_c.py \\
      --upload backend/scripts/destiny_numerology_phase_c_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 3 -- Validate:
    python3 backend/scripts/validate_rules.py \\
      --batch-id destiny_numerology_phase_c_20260604 \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

DECODE_FOLDER = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/DestinyNumerology_CC_Decode"
)

# (filename, chapter_number_or_None, label)
PHASE_C_FILES = [
    # Core -- Ch20-Ch28
    ("Numerology_Ch20_CyclonesTsunamis_Rules.json",  20,   "Cyclones, Tsunamis & Hurricanes"),
    ("Numerology_Ch21_ChineseVirus_Rules.json",       21,   "Pandemic Framework"),
    ("Numerology_Ch22_MajorEarthquakes_Rules.json",   22,   "Major Earthquakes"),
    ("Numerology_Ch23_NationNameNumbers_Rules.json",  23,   "Nation Name Numbers"),
    ("Numerology_Ch24_CityStateNumbers_Rules.json",   24,   "City / State Numbers"),
    ("Numerology_Ch25_FireCountries_Rules.json",       25,   "Fire Countries"),
    ("Numerology_Ch26_CompanyNumbers_Rules.json",      26,   "Company Numbers"),
    ("Numerology_Ch27_CompanyLogos_Rules.json",        27,   "Company Logos"),
    ("Numerology_Ch28_Remarriage_Rules.json",          28,   "Remarriage / Marumangalya"),
    # Derived
    ("Numerology_CareerAlignment_Rules.json",          None, "Career Alignment (derived)"),
    ("Numerology_PersonalYearCycle_Rules.json",        None, "Personal Year Cycle (derived)"),
    ("Numerology_CaseDerivedInference_Rules.json",     None, "Case Derived Inference (derived)"),
]

BATCH_ID       = "destiny_numerology_phase_c_20260604"
SOURCE_BOOK    = "Destiny Numerology"
BOOK_ID        = "destiny_numerology_v1_20260518"
SCIENCE_ID     = "numerology"
EXPECTED_TOTAL = 103  # 39 core + 64 derived

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
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        out(f"  ⚠  JSON parse error in {path.name}: {e}")
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        rules = data.get("rules", [])
        if isinstance(rules, list):
            return rules
    out(f"  ⚠  {path.name}: unexpected JSON root type {type(data)}")
    return []

# ── Interpretation builder ────────────────────────────────────────────────────

def _build_interpretation(rule: dict) -> dict:
    """Build interpretation block. Priority:
      1. Already populated  → leave as-is
      2. result.interpretation (CDI rules)  → use as detailed
      3. full_text  → use as detailed
      4. summary → use as detailed
      5. title → last resort
    """
    interp = rule.get("interpretation") or {}
    if (interp.get("detailed") or "").strip():
        return rule

    # CDI rules: result dict may have a rich interpretation string
    result = rule.get("result") or {}
    if isinstance(result, dict):
        ri = (result.get("interpretation") or "").strip()
        if ri:
            summary = (rule.get("summary") or "").strip()
            rule["interpretation"] = {
                "detailed": ri,
                "summary":  summary if summary else ri[:200],
            }
            return rule

    # Standard fallback
    full_text = (rule.get("full_text") or "").strip()
    summary   = (rule.get("summary")   or "").strip()
    title     = (rule.get("title")     or "").strip()
    detailed  = full_text or summary or title
    rule["interpretation"] = {
        "detailed": detailed,
        "summary":  summary if summary else detailed[:200],
    }
    return rule

# ── Field injection ───────────────────────────────────────────────────────────

def inject_fields(rule: dict, now: str) -> dict:
    rule["ingest_batch_id"] = BATCH_ID
    rule["ingested_at"]     = now
    # KOP-03: must be pending_review for AI validator to find rules
    rule["approval_status"] = "pending_review"
    rule.setdefault("active", True)
    if rule.get("science_id") != SCIENCE_ID:
        rule["science_id"] = SCIENCE_ID

    source = rule.get("source")
    if not isinstance(source, dict):
        source = {}
        rule["source"] = source

    # Force-override book name (fixes OCR artefact "Your Destiny Is In Your Name & DOB")
    source["book"]    = SOURCE_BOOK
    source["book_id"] = BOOK_ID
    # Always overwrite batch_id to current ingest batch
    source["batch_id"] = BATCH_ID

    rule = _build_interpretation(rule)
    return rule

# ── Build ─────────────────────────────────────────────────────────────────────

def build_all_rules() -> tuple[list[dict], list[tuple]]:
    now       = datetime.now(timezone.utc).isoformat()
    all_rules = []
    stats     = []
    seen_ids: dict[str, str] = {}

    for filename, ch, label in PHASE_C_FILES:
        path = DECODE_FOLDER / filename
        if not path.exists():
            out(f"  ✗  File not found: {path}")
            stats.append((filename, ch, label, 0))
            continue
        raw_rules  = load_rules_from_file(path)
        file_rules = []
        for rule in raw_rules:
            if not isinstance(rule, dict):
                continue
            rid = rule.get("rule_id")
            if not rid:
                out(f"  ⚠  Rule without rule_id in {filename} -- skipped")
                continue
            if rid in seen_ids:
                out(f"  ⚠  Duplicate rule_id {rid} (also in {seen_ids[rid]}) -- skipped")
                continue
            seen_ids[rid] = filename
            file_rules.append(inject_fields(rule, now))
        stats.append((filename, ch, label, len(file_rules)))
        all_rules.extend(file_rules)

    return all_rules, stats

# ── Structural check ──────────────────────────────────────────────────────────

def local_structural_check(rules: list[dict]) -> int:
    issues = 0
    for r in rules:
        rid    = r.get("rule_id", "(no id)")
        interp = r.get("interpretation") or {}
        if not interp.get("detailed"):
            out(f"  [ISSUE] {rid}: interpretation.detailed empty")
            issues += 1
        if not interp.get("summary"):
            out(f"  [ISSUE] {rid}: interpretation.summary empty")
            issues += 1
        if r.get("approval_status") != "pending_review":
            out(f"  [ISSUE] {rid}: approval_status={r.get('approval_status')!r} (expected pending_review)")
            issues += 1
        src = r.get("source", {})
        if src.get("batch_id") != BATCH_ID:
            out(f"  [ISSUE] {rid}: source.batch_id mismatch ({src.get('batch_id')!r})")
            issues += 1
        if r.get("ingest_batch_id") != BATCH_ID:
            out(f"  [ISSUE] {rid}: ingest_batch_id mismatch")
            issues += 1
        if src.get("book") != SOURCE_BOOK:
            out(f"  [ISSUE] {rid}: source.book={src.get('book')!r} (expected {SOURCE_BOOK!r})")
            issues += 1
    return issues

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    today    = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = Path("KE_TEXTBOOK_DECODE/Dedup_Reports") / f"ingest_destiny_num_phase_c_{today}.log"

    parser = argparse.ArgumentParser(
        description="Destiny Numerology Phase C ingest -- 103 rules (Ch20-Ch28 + Derived)"
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--save",    metavar="PATH")
    parser.add_argument("--upload",  metavar="PATH")
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    parser.add_argument("--db-name",   default="horoscope_db")
    args = parser.parse_args()

    if not args.dry_run and not args.upload:
        parser.error("Specify --dry-run [--save PATH] or --upload PATH")

    out("=" * 70)
    out(f"LOG FILE: {log_path}")
    out(f"DESTINY NUMEROLOGY PHASE C INGEST  |  batch: {BATCH_ID}")
    out(f"Scope: Ch20-Ch28 (39 rules) + Derived (64 rules) = {EXPECTED_TOTAL} total")
    out("=" * 70)

    # ── DRY RUN ───────────────────────────────────────────────────────────────
    if args.dry_run:
        out(f"\nBuilding rules...")
        all_rules, stats = build_all_rules()

        out(f"\n{'─'*70}")
        out(f"  {'File':<52} {'Ch':>4}  {'Rules':>6}")
        out(f"{'─'*70}")
        core_total    = 0
        derived_total = 0
        for fname, ch, label, count in stats:
            ch_str = str(ch) if ch is not None else "--"
            out(f"  {fname:<52} {ch_str:>4}  {count:>6}   {label}")
            if ch is not None:
                core_total += count
            else:
                derived_total += count
        out(f"{'─'*70}")
        out(f"  {'Core subtotal (Ch20-Ch28)':<52}       {core_total:>6}")
        out(f"  {'Derived subtotal':<52}       {derived_total:>6}")
        out(f"  {'TOTAL':<52}       {len(all_rules):>6}")
        out(f"{'─'*70}\n")

        out("Running local structural check...")
        issues = local_structural_check(all_rules)
        out(f"Issues found: {issues}")
        if issues:
            out("  ✗  Fix issues before uploading.")
            _write_log(log_path)
            print(f"\nLog saved: {log_path}")
            sys.exit(1)
        out("  ✓  All rules pass structural check.")

        # Spot-checks
        if all_rules:
            r0 = all_rules[0]
            out(f"\nSpot-check first rule ({r0['rule_id']}):")
            out(f"  approval_status : {r0.get('approval_status')}")
            out(f"  ingest_batch_id : {r0.get('ingest_batch_id')}")
            out(f"  source.book     : {r0.get('source',{}).get('book')}")
            out(f"  source.batch_id : {r0.get('source',{}).get('batch_id')}")
            out(f"  interp.detailed : {repr(r0['interpretation']['detailed'][:80])}")

            # CDI spot-check (rule_id starts with num-cdi)
            cdi_rules = [r for r in all_rules if r.get('rule_id','').startswith('num-cdi')]
            if cdi_rules:
                rc = cdi_rules[0]
                out(f"\nSpot-check CDI rule ({rc['rule_id']}):")
                out(f"  source.book     : {rc.get('source',{}).get('book')}")
                out(f"  interp.detailed : {repr(rc['interpretation']['detailed'][:80])}")
                out(f"  interp.summary  : {repr(rc['interpretation']['summary'][:80])}")

            # PYC spot-check
            pyc_rules = [r for r in all_rules if r.get('rule_id','').startswith('num-pyc')]
            if pyc_rules:
                rp = pyc_rules[0]
                out(f"\nSpot-check PYC rule ({rp['rule_id']}):")
                out(f"  source keys     : {list(rp.get('source',{}).keys())}")
                out(f"  source.book     : {rp.get('source',{}).get('book')}")
                out(f"  interp.detailed : {repr(rp['interpretation']['detailed'][:80])}")

            rN = all_rules[-1]
            out(f"\nSpot-check last rule ({rN['rule_id']}):")
            out(f"  approval_status : {rN.get('approval_status')}")
            out(f"  source.book     : {rN.get('source',{}).get('book')}")
            out(f"  interp.detailed : {repr(rN['interpretation']['detailed'][:80])}")

        # Interpretation method breakdown
        out(f"\nInterpretation source breakdown:")
        from_result   = sum(1 for r in all_rules
                            if isinstance(r.get('result'), dict) and
                               r['result'].get('interpretation') and
                               r['interpretation']['detailed'] == r['result']['interpretation'])
        from_fulltext = sum(1 for r in all_rules
                            if r.get('full_text') and
                               r['interpretation']['detailed'] == r.get('full_text','').strip())
        from_summary  = len(all_rules) - from_result - from_fulltext
        out(f"  result.interpretation → detailed : {from_result}")
        out(f"  full_text → detailed             : {from_fulltext}")
        out(f"  summary → detailed               : {from_summary}")

        if len(all_rules) != EXPECTED_TOTAL:
            out(f"\n  ⚠  Expected {EXPECTED_TOTAL} -- got {len(all_rules)}.")
        else:
            out(f"\n  ✓  Rule count matches expected {EXPECTED_TOTAL}.")

        if args.save:
            save_path = Path(args.save)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_text(
                json.dumps(all_rules, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            out(f"\nSaved {len(all_rules)} rules → {save_path}")

        out(f"\n✓ Dry run complete.")
        out(f"  Next: python3 backend/scripts/ingest_destiny_numerology_phase_c.py \\")
        out(f"    --upload backend/scripts/destiny_numerology_phase_c_rules.json \\")
        out(f"    --mongo-url \"$MONGO_URL\" --db-name horoscope_db")
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
            out("✗  MONGO_URL not set.")
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
        out("Running final structural check before upload...")
        issues = local_structural_check(rules)
        out(f"Issues found: {issues}")
        if issues:
            out("✗  Fix issues. Aborting.")
            _write_log(log_path)
            print(f"\nLog saved: {log_path}")
            sys.exit(1)

        client = MongoClient(args.mongo_url)
        db     = client[args.db_name]
        col    = db["interpretation_rules"]
        batches_col = db["import_batches"]

        existing_ids = set(
            d["rule_id"] for d in col.find(
                {"rule_id": {"$in": [r["rule_id"] for r in rules]}},
                {"rule_id": 1}
            )
        )
        new_rules = [r for r in rules if r["rule_id"] not in existing_ids]
        skipped   = len(rules) - len(new_rules)
        if skipped:
            out(f"  ⚠  {skipped} rules already in DB -- skipped")
        if not new_rules:
            out("  Nothing to insert.")
            client.close()
            _write_log(log_path)
            print(f"\nLog saved: {log_path}")
            return

        result = col.insert_many(new_rules)
        inserted = len(result.inserted_ids)
        out(f"\n  ✓  Inserted {inserted} rules into {args.db_name}.interpretation_rules")

        now_ts   = datetime.now(timezone.utc).isoformat()
        chapters = sorted({
            r.get("source", {}).get("chapter")
            for r in new_rules
            if isinstance(r.get("source", {}).get("chapter"), int)
        })
        modules = sorted({
            r.get("module")
            for r in new_rules
            if r.get("module")
        })
        batches_col.update_one(
            {"batch_id": BATCH_ID},
            {"$set": {
                "batch_id":       BATCH_ID,
                "source_book":    SOURCE_BOOK,
                "science_id":     SCIENCE_ID,
                "chapters":       chapters,
                "modules":        modules,
                "rules_inserted": inserted,
                "rules_skipped":  skipped,
                "uploaded_at":    now_ts,
                "status":         "ingested",
                "phase":          "C",
                "notes":          (
                    "Ch20-Ch28 (39 rules) + CareerAlignment (31) + PersonalYearCycle (12) "
                    "+ CaseDerivedInference (21). GAI: 26-A/28-A/28-B resolved (engine-level). "
                    "21-A: Ch21 chapter_name internal only. source.book force-overridden to "
                    "'Destiny Numerology' for all rules."
                ),
            }},
            upsert=True,
        )
        out(f"  ✓  import_batches record upserted  (batch_id: {BATCH_ID})")
        out(f"     chapters: {chapters}")
        out(f"     modules : {modules}")

        count = col.count_documents({"ingest_batch_id": BATCH_ID})
        out(f"\n  Verification: count = {count}")
        if count != EXPECTED_TOTAL:
            out(f"  ⚠  Expected {EXPECTED_TOTAL} -- got {count} (skipped={skipped}).")
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
