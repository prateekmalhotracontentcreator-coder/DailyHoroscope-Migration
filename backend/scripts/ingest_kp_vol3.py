#!/usr/bin/env python3
"""
ingest_kp_vol3.py
--------------------------------------------------------------------
KP Astrology Vol 3 -- KE Ingest (all chapters)
256 rules across 77 files

Source  : /Users/apple/Documents/Knowledge Engine_eBooks/KP_CC_Decode/
Book    : KP Astrology Vol 3
Batch   : kp_vol3_v1_20260604
Science : kp_jyotish

Scope:
  T04, T06-T10         -- Theory chapters  (95 rules)
  P01-P88 (excl. P83/P84) -- Practical chapters (161 rules)
  P46, P50             -- Decoded but 0 extractable rules (by design)
  P79, P80             -- "KP rejects classical rules" (2 rules, contradiction_flag:true,
                           tba_needs_trigger → forced pending_review, treated as engine_spec PHR)

Not included (not decoded):
  T01 -- Pure background theory (TT decision pending)
  P83 -- Annual Horoscope (Western solar return method)
  P84 -- Ashtaka Varga (KP author says does not work universally)
  T02, T03, T05, P89 -- Summary.md only (lookup tables / glossary, no rules)

Special encodings (separate JSONs, NOT part of this ingest):
  KP_T05_Master_Sub_Significance.json  (249 entries -- distinct schema)
  KP_P27_Profession_Dictionary.json    (229 entries -- distinct schema)
  Both blocked on TT-1 / T05 OCR issues; ingest separately when cleared.

OCR open items (T05 only -- do NOT block this ingest):
  Cat B (8 P1): Duplicate/skipped entry numbers -- T05 only
  Cat C (2 P1): Rahu-star stubs Swathi 131-138 / Sathabisha 213-221 -- T05 only
  Cat D (1 P1): Entries 248-249 INFERRED -- TT-1 action required -- T05 only
  Cat G (1 P1): Conditional vs direct delineation inconsistency -- T05 only
  Cat H (3 P1): Formatting inconsistencies -- T05 only
  F-01 to F-06 (P2): Ambiguous medical/technical terms -- T05 only

Post-ingest dedup (informational, not blocking):
  Run against BPHS Vol 1 + Vol 2 after ingest.
  KP sub-lord vs traditional Jyotish = system-level differences, not genuine duplicates.

Run sequence:
  Step 1 -- Dry run + save JSON:
    python3 backend/scripts/ingest_kp_vol3.py --dry-run \\
      --save backend/scripts/kp_vol3_rules.json

  Step 2 -- Upload:
    python3 backend/scripts/ingest_kp_vol3.py \\
      --upload backend/scripts/kp_vol3_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 3 -- Validate:
    python3 backend/scripts/validate_rules.py \\
      --batch-id kp_vol3_v1_20260604 \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db
"""

import argparse
import glob
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

DECODE_FOLDER = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/KP_CC_Decode"
)

BATCH_ID    = "kp_vol3_v1_20260604"
SOURCE_BOOK = "KP Astrology Vol 3"
BOOK_ID     = "kp_vol3_20260526"
SCIENCE_ID  = "kp_jyotish"
EXPECTED_TOTAL = 256

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
    """Build interpretation block from full_text (100% present in KP rules)."""
    interp = rule.get("interpretation") or {}
    if (interp.get("detailed") or "").strip():
        return rule
    full_text = (rule.get("full_text") or "").strip()
    summary   = (rule.get("summary")   or "").strip()
    title     = (rule.get("title")     or "").strip()
    detailed  = full_text or summary or title
    rule["interpretation"] = {
        "detailed": detailed,
        "summary":  summary if summary else detailed[:250],
    }
    return rule

# ── Field injection ───────────────────────────────────────────────────────────

def inject_fields(rule: dict, now: str) -> dict:
    rule["ingest_batch_id"] = BATCH_ID
    rule["ingested_at"]     = now
    # KOP-03: force pending_review (covers pending_human_review AND tba_needs_trigger)
    rule["approval_status"] = "pending_review"
    rule.setdefault("active", True)
    # science_id already correct on all KP rules; verify only
    if rule.get("science_id") != SCIENCE_ID:
        rule["science_id"] = SCIENCE_ID

    source = rule.get("source")
    if not isinstance(source, dict):
        source = {}
        rule["source"] = source
    # book / book_id already correct; preserve them
    source.setdefault("book",    SOURCE_BOOK)
    source.setdefault("book_id", BOOK_ID)
    # Always overwrite batch_id to current ingest batch (was per-chapter previously)
    source["batch_id"] = BATCH_ID

    rule = _build_interpretation(rule)
    return rule

# ── Build ─────────────────────────────────────────────────────────────────────

def build_all_rules() -> tuple[list[dict], list[tuple]]:
    """Discover and build all rules from *_Rules.json files."""
    now        = datetime.now(timezone.utc).isoformat()
    all_rules  = []
    stats      = []
    seen_ids: dict[str, str] = {}

    rule_files = sorted(DECODE_FOLDER.glob("*_Rules.json"))
    for path in rule_files:
        raw_rules  = load_rules_from_file(path)
        file_rules = []
        for rule in raw_rules:
            if not isinstance(rule, dict):
                continue
            rid = rule.get("rule_id")
            if not rid:
                out(f"  ⚠  Rule without rule_id in {path.name} -- skipped")
                continue
            if rid in seen_ids:
                out(f"  ⚠  Duplicate rule_id {rid} (also in {seen_ids[rid]}) -- skipped")
                continue
            seen_ids[rid] = path.name
            file_rules.append(inject_fields(rule, now))
        stats.append((path.name, len(raw_rules), len(file_rules)))
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
            out(f"  [ISSUE] {rid}: source.book={src.get('book')!r}")
            issues += 1
    return issues

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    today    = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = Path("KE_TEXTBOOK_DECODE/Dedup_Reports") / f"ingest_kp_vol3_{today}.log"

    parser = argparse.ArgumentParser(
        description="KP Astrology Vol 3 ingest -- 256 rules"
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
    out(f"KP ASTROLOGY VOL 3 INGEST  |  batch: {BATCH_ID}")
    out(f"Scope: 256 rules · 77 files · science_id: {SCIENCE_ID}")
    out("=" * 70)

    # ── DRY RUN ───────────────────────────────────────────────────────────────
    if args.dry_run:
        out(f"\nDiscovering and building rules...")
        all_rules, stats = build_all_rules()

        # Summary table -- only show non-zero files + note zero-rule ones
        zero_files = [(f, raw, inj) for f, raw, inj in stats if raw == 0]
        nonzero    = [(f, raw, inj) for f, raw, inj in stats if raw > 0]

        out(f"\n{'─'*70}")
        out(f"  {'File':<58} {'Rules':>6}")
        out(f"{'─'*70}")
        for fname, raw, inj in nonzero:
            out(f"  {fname:<58} {inj:>6}")
        out(f"{'─'*70}")
        out(f"  {'TOTAL':<58} {len(all_rules):>6}")
        if zero_files:
            out(f"\nZero-rule files (by design):")
            for fname, _, _ in zero_files:
                out(f"  {fname}")
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
        r_first = all_rules[0]
        out(f"\nSpot-check first rule ({r_first['rule_id']}):")
        out(f"  approval_status  : {r_first.get('approval_status')}")
        out(f"  ingest_batch_id  : {r_first.get('ingest_batch_id')}")
        out(f"  source.book      : {r_first.get('source',{}).get('book')}")
        out(f"  source.batch_id  : {r_first.get('source',{}).get('batch_id')}")
        out(f"  science_id       : {r_first.get('science_id')}")
        out(f"  claim_axis       : {r_first.get('claim_axis')}")
        out(f"  claim_polarity   : {r_first.get('claim_polarity')}")
        out(f"  cond.type        : {r_first.get('condition',{}).get('type') if isinstance(r_first.get('condition'),dict) else r_first.get('condition')}")
        out(f"  interp.detailed  : {repr(r_first['interpretation']['detailed'][:80])}")

        # P79/P80 tba_needs_trigger verification
        tba_rules = [r for r in all_rules if r['rule_id'] in ('kp3-chP79-001', 'kp3-chP80-001')]
        out(f"\ntba_needs_trigger rules (P79/P80) -- status after injection:")
        for r in tba_rules:
            out(f"  {r['rule_id']}: approval_status={r['approval_status']} "
                f"contradiction_flag={r.get('contradiction_flag')}")

        # Field preservation check -- KP-specific fields
        kp_fields = ['claim_axis', 'claim_polarity', 'claim_scope', 'timing_bias',
                     'strength_band', 'subject_scope', 'authority_override',
                     'contradiction_flag', 'duplicate_candidate']
        out(f"\nKP-specific field preservation (first rule):")
        for fld in kp_fields:
            val = r_first.get(fld)
            if val is not None:
                out(f"  {fld:<25} : {val}")

        # claim_axis distribution
        claim_axes: dict[str, int] = {}
        for r in all_rules:
            ax = r.get('claim_axis') or 'none'
            claim_axes[ax] = claim_axes.get(ax, 0) + 1
        out(f"\nclaim_axis distribution:")
        for ax, n in sorted(claim_axes.items(), key=lambda x: -x[1])[:10]:
            out(f"  {ax:<30} {n}")

        # contradiction_flag count
        contra = sum(1 for r in all_rules if r.get('contradiction_flag'))
        out(f"\ncontradiction_flag=True : {contra} rules")

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
        out(f"  Next: python3 backend/scripts/ingest_kp_vol3.py \\")
        out(f"    --upload backend/scripts/kp_vol3_rules.json \\")
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
            if r.get("source", {}).get("chapter")
        }, key=lambda x: str(x))
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
                "notes":          (
                    "256 rules, 77 chapters (P01-P88 excl. P83/P84 + T04/T06-T10). "
                    "T05/T02/T03/P89 not included (lookup/glossary). "
                    "P46/P50 = 0-rule files (by design). "
                    "P79/P80 tba_needs_trigger → forced pending_review (engine_spec, "
                    "contradiction_flag:true). "
                    "Post-ingest dedup vs BPHS Vol1+Vol2 pending."
                ),
            }},
            upsert=True,
        )
        out(f"  ✓  import_batches record upserted  (batch_id: {BATCH_ID})")
        out(f"     chapters: {len(chapters)} distinct chapter IDs")

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
