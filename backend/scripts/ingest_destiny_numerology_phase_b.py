#!/usr/bin/env python3
"""
ingest_destiny_numerology_phase_b.py
--------------------------------------------------------------------
Destiny Numerology Phase B -- KE Ingest (Ch17-Ch19)
34 rules across 3 files

Source  : /Users/apple/Documents/Knowledge Engine_eBooks/
          DestinyNumerology_CC_Decode/
Book    : Destiny Numerology
Batch   : destiny_numerology_phase_b_20260604
Science : numerology

Chapters:
  Ch17 -- Gemstone Numerology  (13 rules)
  Ch18 -- Donations             (16 rules)
  Ch19 -- Deadly Wars / Element Classification (5 rules)

Gate status (all cleared 2026-06-04):
  CRITICAL-1 (17-A): Number 3 Amethyst proxy remedy -- intentional, confirmed by GAI
  CRITICAL-2 (19-A): Dual element routing -- Wu Xing (Lo Shu) / Pancha Mahabootas
                     (Deadly Wars) -- confirmed by GAI
  Issue 17-B: Paksha data patched: Number 6 → Shukla, Number 8 → Krishna (2026-06-04)

Run sequence:
  Step 1 -- Dry run + save JSON:
    python3 backend/scripts/ingest_destiny_numerology_phase_b.py --dry-run \\
      --save backend/scripts/destiny_numerology_phase_b_rules.json

  Step 2 -- Upload:
    python3 backend/scripts/ingest_destiny_numerology_phase_b.py \\
      --upload backend/scripts/destiny_numerology_phase_b_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 3 -- Validate:
    python3 backend/scripts/validate_rules.py \\
      --batch-id destiny_numerology_phase_b_20260604 \\
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

PHASE_B_FILES = [
    ("Numerology_Ch17_GemstoneNumerology_Rules.json", 17, "Gemstone Numerology"),
    ("Numerology_Ch18_Donations_Rules.json",          18, "Donations"),
    ("Numerology_Ch19_DeadlyWars_Rules.json",         19, "Deadly Wars / Element Classification"),
]

BATCH_ID       = "destiny_numerology_phase_b_20260604"
SOURCE_BOOK    = "Destiny Numerology"
BOOK_ID        = "destiny_numerology_v1_20260518"
SCIENCE_ID     = "numerology"
EXPECTED_TOTAL = 34

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

# ── Field injection ───────────────────────────────────────────────────────────

def _build_interpretation(rule: dict) -> dict:
    interp = rule.get("interpretation") or {}
    if (interp.get("detailed") or "").strip():
        return rule
    full_text = (rule.get("full_text") or "").strip()
    summary   = (rule.get("summary")   or "").strip()
    title     = (rule.get("title")     or "").strip()
    detailed  = full_text or summary or title
    rule["interpretation"] = {
        "detailed": detailed,
        "summary":  summary if summary else detailed[:200],
    }
    return rule

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
    if not source.get("book"):
        source["book"] = SOURCE_BOOK
    if not source.get("book_id"):
        source["book_id"] = BOOK_ID
    source["batch_id"] = BATCH_ID
    rule = _build_interpretation(rule)
    return rule

# ── Build ─────────────────────────────────────────────────────────────────────

def build_all_rules() -> tuple[list[dict], list[tuple]]:
    now       = datetime.now(timezone.utc).isoformat()
    all_rules = []
    stats     = []
    seen_ids  = {}
    for filename, ch, ch_title in PHASE_B_FILES:
        path = DECODE_FOLDER / filename
        if not path.exists():
            out(f"  ✗  File not found: {path}")
            stats.append((filename, ch, ch_title, 0))
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
                out(f"  ⚠  Duplicate rule_id {rid} -- skipped")
                continue
            seen_ids[rid] = filename
            file_rules.append(inject_fields(rule, now))
        stats.append((filename, ch, ch_title, len(file_rules)))
        all_rules.extend(file_rules)
    return all_rules, stats

# ── Structural check ──────────────────────────────────────────────────────────

def local_structural_check(rules: list[dict]) -> int:
    issues = 0
    for r in rules:
        rid   = r.get("rule_id", "(no id)")
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
    return issues

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    today    = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = Path("KE_TEXTBOOK_DECODE/Dedup_Reports") / f"ingest_destiny_num_phase_b_{today}.log"

    parser = argparse.ArgumentParser(
        description="Destiny Numerology Phase B ingest -- 34 rules (Ch17-Ch19)"
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--save",   metavar="PATH")
    parser.add_argument("--upload", metavar="PATH")
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    parser.add_argument("--db-name",   default="horoscope_db")
    args = parser.parse_args()

    if not args.dry_run and not args.upload:
        parser.error("Specify --dry-run [--save PATH] or --upload PATH")

    out("=" * 70)
    out(f"LOG FILE: {log_path}")
    out(f"DESTINY NUMEROLOGY PHASE B INGEST  |  batch: {BATCH_ID}")
    out(f"Scope: Ch17-Ch19 ({EXPECTED_TOTAL} rules, 3 files)")
    out("=" * 70)

    # ── DRY RUN ───────────────────────────────────────────────────────────────
    if args.dry_run:
        out(f"\nBuilding rules...")
        all_rules, stats = build_all_rules()

        out(f"\n{'─'*70}")
        out(f"  {'File':<48} {'Ch':>3}  {'Rules':>6}")
        out(f"{'─'*70}")
        for fname, ch, ch_title, count in stats:
            out(f"  {fname:<48} {ch:>3}  {count:>6}   {ch_title}")
        out(f"{'─'*70}")
        out(f"  {'TOTAL':<48}       {len(all_rules):>6}")
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

        if all_rules:
            r0 = all_rules[0]
            out(f"\nSpot-check first rule ({r0['rule_id']}):")
            out(f"  approval_status : {r0.get('approval_status')}")
            out(f"  ingest_batch_id : {r0.get('ingest_batch_id')}")
            out(f"  source.batch_id : {r0.get('source',{}).get('batch_id')}")
            out(f"  interp.detailed : {repr(r0['interpretation']['detailed'][:80])}")
            rN = all_rules[-1]
            out(f"\nSpot-check last rule ({rN['rule_id']}):")
            out(f"  approval_status : {rN.get('approval_status')}")
            out(f"  source.chapter  : {rN.get('source',{}).get('chapter')}")
            out(f"  interp.detailed : {repr(rN['interpretation']['detailed'][:80])}")

        # Paksha verification
        out(f"\nPaksha patch verification:")
        for r in all_rules:
            result = r.get('result') or {}
            if isinstance(result, dict) and result.get('paksha'):
                out(f"  {r['rule_id']}: paksha={result['paksha']}")

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
                "phase":          "B",
                "notes":          "Ch17-Ch19. CRITICAL-1/2 cleared by GAI. Issue 17-B Paksha patched.",
            }},
            upsert=True,
        )
        out(f"  ✓  import_batches record upserted  (batch_id: {BATCH_ID})")
        out(f"     chapters: {chapters}")

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
