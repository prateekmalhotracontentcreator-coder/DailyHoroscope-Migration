#!/usr/bin/env python3
"""
ingest_bphs_vol1_phase2.py
--------------------------------------------------------------------
BPHS Vol 1 Phase 2 ingest -- 17 new chapters, 696 rules

Chapters: Ch03-Ch11, Ch25, Ch26, Ch28-Ch33
Batch ID: bphs-vol1-phase2-v1-20260601
Source  : /Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/

Schema handling:
  - Dict-format files (Ch03-Ch31 Thread A/C/D decode): {"rules": [...]}
  - List-format files (Ch11 bare, Ch32, Ch33 Thread D/E decode): [...]
  - Superseded bare _Rules.json for Ch32/Ch33 are SKIPPED (Part files are canonical)
  - Ch11 bare _Rules.json is INCLUDED (only file for that chapter)

Run sequence (mandatory):
  Step 1 -- Dry run + save JSON:
    python3 backend/scripts/ingest_bphs_vol1_phase2.py --dry-run \
      --save backend/scripts/bphs_vol1_phase2_rules.json

  Step 2 -- Review saved JSON (spot-check first + last rule per chapter)

  Step 3 -- Upload:
    python3 backend/scripts/ingest_bphs_vol1_phase2.py \
      --upload backend/scripts/bphs_vol1_phase2_rules.json \
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 4 -- Validate:
    python3 backend/scripts/validate_rules.py \
      --batch-id bphs-vol1-phase2-v1-20260601 \
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 5 -- Inspect flagged rules, write patch script if needed
  Step 6 -- Commit all files to git
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

DECODE_FOLDER = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode"
)

BATCH_ID   = "bphs-vol1-phase2-v1-20260601"
BOOK_NAME  = "BPHS Vol 1"
SCIENCE_ID = "jyotish"
BOOK_ID    = "bphs_vol1_20260526"

# Phase 2 chapters in ingest order
PHASE2_CHAPTERS = [3, 4, 5, 6, 7, 8, 9, 10, 11,
                   25, 26, 28, 29, 30, 31, 32, 33]

# Chapters that have both bare _Rules.json AND Part files.
# The bare file is superseded -- skip it and use Part files only.
SKIP_BARE_FOR = {32, 33}


def load_rules_from_file(path: Path) -> list[dict]:
    """Load rules from a JSON file handling both list and dict formats."""
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


def get_chapter_files(chapter: int) -> list[Path]:
    """
    Return the canonical Rule JSON files for a chapter.
    Prefers Part files over bare _Rules.json.
    Falls back to bare _Rules.json only if no Part files exist.
    """
    patterns = [
        f"BPHS_Ch{chapter:02d}_*_Rules_Part*.json",
        f"BPHS_Ch{chapter}_*_Rules_Part*.json",
    ]
    part_files = []
    for pattern in patterns:
        part_files.extend(DECODE_FOLDER.glob(pattern))
    part_files = sorted({f.resolve(): f for f in part_files}.values())

    if part_files:
        return part_files

    # No Part files -- try bare _Rules.json (Ch11 case)
    if chapter in SKIP_BARE_FOR:
        return []

    bare_patterns = [
        f"BPHS_Ch{chapter:02d}_*_Rules.json",
        f"BPHS_Ch{chapter}_*_Rules.json",
    ]
    bare_files = []
    for pattern in bare_patterns:
        bare_files.extend(DECODE_FOLDER.glob(pattern))
    return sorted({f.resolve(): f for f in bare_files}.values())


def _map_interpretation(rule: dict) -> dict:
    """
    Map source-schema fields → canonical interpretation.detailed / summary.

    Phase 2 source files use three schemas -- none pre-populate
    interpretation.detailed / interpretation.summary, which validate_rules.py
    requires. Mapping by detected schema:

    Schema A1 (Ch03-Ch10): claim is a dict {axis, polarity, text}; full_text = sloka
        → detailed = claim["text"], summary = full_text

    Schema A2 (Ch29-Ch31): claim is a plain string; title may exist
        → detailed = claim, summary = title or claim[:200]

    Schema C  (Ch25-Ch26-Ch28): no claim; result is a plain string; source_text = sloka
        → detailed = result, summary = source_text[:200] or result[:200]

    Schema B  (Ch11-Ch32-Ch33): full_text + top-level summary; result is a Python-dict
        repr string -- do NOT use it
        → detailed = full_text, summary = summary field
    """
    interp = rule.get("interpretation") or {}
    # Already correctly populated -- skip
    if (interp.get("detailed") or "").strip() or (interp.get("summary") or "").strip():
        return rule

    claim      = rule.get("claim", "")
    full_text  = rule.get("full_text", "")
    summary    = rule.get("summary", "")
    result     = rule.get("result", "")
    source_text = rule.get("source_text", "")
    title      = rule.get("title", "")

    if isinstance(claim, dict):
        # Schema A1
        detailed = (claim.get("text") or "").strip() or full_text.strip()
        smry     = full_text.strip() or detailed[:200]
    elif isinstance(claim, str) and claim.strip():
        # Schema A2
        detailed = claim.strip()
        smry     = (title or detailed[:200]).strip()
    elif isinstance(result, str) and result.strip() and not result.strip().startswith("{"):
        # Schema C  (result is plain prose, not a Python-dict repr)
        detailed = result.strip()
        smry     = source_text[:200].strip() if source_text else detailed[:200]
    elif full_text.strip():
        # Schema B
        detailed = full_text.strip()
        smry     = summary.strip() if summary else detailed[:200]
    else:
        # Nothing useful -- validator will flag; do not crash ingest
        detailed = ""
        smry     = ""

    rule["interpretation"] = {
        "detailed": detailed,
        "summary":  smry,
    }
    return rule


def _map_condition(rule: dict) -> dict:
    """
    Ensure rule has a 'condition' dict (singular).

    Ch25-Ch26-Ch28-Ch29-Ch30-Ch31 source files use 'conditions' (list) instead.
    validate_rules.py structural check requires condition to be a non-empty dict.

    Mapping:
      - conditions is a non-empty list → use conditions[0]
      - conditions is empty or missing → synthetic minimal dict from rule's 'type'
    """
    # Already has condition dict -- skip
    if isinstance(rule.get("condition"), dict) and rule["condition"]:
        return rule

    conditions = rule.get("conditions", [])
    if isinstance(conditions, list) and conditions:
        rule["condition"] = conditions[0]
    else:
        # Synthetic fallback for engine-spec / general-principle rules
        rule_type = rule.get("type") or rule.get("rule_type") or "general_principle"
        rule["condition"] = {"type": rule_type}

    return rule


def inject_fields(rule: dict, now: str, chapter_num: int) -> dict:
    """Inject standard ingest fields onto a rule dict."""
    rule["approval_status"] = "pending_review"
    rule["ingest_batch_id"] = BATCH_ID
    rule["source_book"]     = BOOK_NAME
    rule["ingested_at"]     = now
    rule["active"]          = rule.get("active", True)

    # science_id -- set if missing or wrong
    if rule.get("science_id") not in ("jyotish",):
        rule["science_id"] = SCIENCE_ID

    # Ensure source is a dict and patch missing fields
    source = rule.get("source")
    if not isinstance(source, dict):
        source = {}
        rule["source"] = source

    if not source.get("book_id"):
        source["book_id"] = BOOK_ID

    # source.batch_id -- validate_rules.py queries this field (source.batch_id)
    # NOT the top-level ingest_batch_id. Must be kept in sync.
    source["batch_id"] = BATCH_ID

    # source.chapter -- dict-format files (Ch03-Ch31 Thread A/C/D) do not store
    # the chapter as an integer in source.chapter. Inject from loop context.
    if not source.get("chapter"):
        source["chapter"] = chapter_num

    # source.book -- normalise to canonical name
    if not source.get("book"):
        source["book"] = BOOK_NAME

    # Schema normalisation -- map source-specific fields to canonical KE schema
    rule = _map_interpretation(rule)
    rule = _map_condition(rule)

    return rule


def build_all_rules() -> tuple[list[dict], dict]:
    """Load and inject all Phase 2 rules. Returns (rules_list, chapter_counts)."""
    now = datetime.now(timezone.utc).isoformat()
    all_rules = []
    chapter_counts = {}
    seen_ids = {}

    for chapter in PHASE2_CHAPTERS:
        files = get_chapter_files(chapter)
        if not files:
            print(f"  ⚠  Ch{chapter:02d}: no Rule JSON files found")
            chapter_counts[chapter] = 0
            continue

        ch_rules = []
        for f in files:
            rules = load_rules_from_file(f)
            for rule in rules:
                if not isinstance(rule, dict):
                    continue
                rid = rule.get("rule_id")
                if not rid:
                    print(f"  ⚠  Rule without rule_id in {f.name} -- skipped")
                    continue
                if rid in seen_ids:
                    print(f"  ⚠  Duplicate rule_id {rid} in {f.name} "
                          f"(first seen in {seen_ids[rid]}) -- skipped")
                    continue
                seen_ids[rid] = f.name
                ch_rules.append(inject_fields(rule, now, chapter))

        chapter_counts[chapter] = len(ch_rules)
        all_rules.extend(ch_rules)

    return all_rules, chapter_counts


def main():
    parser = argparse.ArgumentParser(
        description="BPHS Vol 1 Phase 2 ingest -- 17 chapters, 696 rules"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Build rules in memory, print summary, no DB write")
    parser.add_argument("--save", metavar="PATH",
                        help="Save built rules to JSON file (use with --dry-run)")
    parser.add_argument("--upload", metavar="PATH",
                        help="Upload rules from saved JSON to MongoDB")
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    parser.add_argument("--db-name", default="horoscope_db")
    args = parser.parse_args()

    if not args.dry_run and not args.upload:
        parser.error("Specify --dry-run or --upload PATH")

    print("\n" + "=" * 70)
    print(f"BPHS VOL 1 PHASE 2 INGEST  |  batch: {BATCH_ID}")
    print("=" * 70)

    # ── DRY RUN ───────────────────────────────────────────────────────────────
    if args.dry_run:
        print(f"\nSource folder: {DECODE_FOLDER}")
        print(f"\nBuilding rules...")
        all_rules, chapter_counts = build_all_rules()

        print(f"\n{'─' * 70}")
        print(f"{'Ch':<6} {'Title':<45} {'Rules':>6}")
        print(f"{'─' * 70}")

        chapter_titles = {
            3:  "Planetary Characters",
            4:  "Zodiacal Signs",
            5:  "Special Ascendants",
            6:  "Sixteen Divisions",
            7:  "Divisional Consideration",
            8:  "Aspects of Signs",
            9:  "Evils at Birth (Balarishta)",
            10: "Antidotes for Evils",
            11: "Judgement of Houses",
            25: "Non-Luminous Planets (Rahu/Ketu)",
            26: "Evaluation of Planetary Aspects",
            28: "Ishta Kashta Balas",
            29: "Bhavapadas (Arudha Padas)",
            30: "Upa Pada",
            31: "Argala",
            32: "Planetary Karakatwa",
            33: "Effects of Karakamsa",
        }

        for ch in PHASE2_CHAPTERS:
            count = chapter_counts.get(ch, 0)
            title = chapter_titles.get(ch, "")
            flag = "" if count > 0 else "  ⚠  NO FILES"
            print(f"  Ch{ch:<4} {title:<45} {count:>4}{flag}")

        print(f"{'─' * 70}")
        print(f"  {'TOTAL':<49} {len(all_rules):>4}")
        print()

        if all_rules:
            print("First rule:")
            r0 = all_rules[0]
            print(f"  rule_id      : {r0.get('rule_id')}")
            print(f"  science_id   : {r0.get('science_id')}")
            print(f"  approval_status: {r0.get('approval_status')}")
            print(f"  ingest_batch_id: {r0.get('ingest_batch_id')}")
            print(f"  source.chapter : {(r0.get('source') or {}).get('chapter')}")

            print("\nLast rule:")
            rN = all_rules[-1]
            print(f"  rule_id      : {rN.get('rule_id')}")
            print(f"  science_id   : {rN.get('science_id')}")
            print(f"  source.chapter : {(rN.get('source') or {}).get('chapter')}")

        if args.save and all_rules:
            save_path = Path(args.save)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_text(
                json.dumps(all_rules, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8"
            )
            print(f"\n✅ Saved {len(all_rules)} rules → {save_path}")
        elif args.save and not all_rules:
            print("\n⚠  No rules built -- nothing saved.")

        print(f"\n[DRY RUN] No writes made.")
        print(f"Re-run with: --upload {args.save or 'PATH'} --mongo-url \"...\"")
        return

    # ── UPLOAD ────────────────────────────────────────────────────────────────
    if args.upload:
        if not args.mongo_url:
            parser.error("--mongo-url is required for upload")

        upload_path = Path(args.upload)
        if not upload_path.exists():
            print(f"\n❌ File not found: {upload_path}")
            sys.exit(1)

        all_rules = json.loads(upload_path.read_text(encoding="utf-8"))
        print(f"\nLoaded {len(all_rules)} rules from {upload_path}")

        try:
            from pymongo import MongoClient
            client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10000)
            col = client[args.db_name]["interpretation_rules"]
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            sys.exit(1)

        inserted = 0
        updated  = 0
        errors   = []

        print(f"Upserting to {args.db_name}.interpretation_rules...")

        for rule in all_rules:
            rid = rule.get("rule_id")
            if not rid:
                continue
            try:
                result = col.replace_one(
                    {"rule_id": rid},
                    rule,
                    upsert=True
                )
                if result.upserted_id:
                    inserted += 1
                elif result.modified_count:
                    updated += 1
            except Exception as e:
                errors.append(f"{rid}: {e}")

        print(f"\nInserted {inserted} / Updated {updated} rules → {args.db_name}.interpretation_rules")

        if errors:
            print(f"\n⚠  {len(errors)} errors:")
            for e in errors[:10]:
                print(f"  {e}")

        # Log to import_batches
        try:
            client[args.db_name]["import_batches"].replace_one(
                {"batch_id": BATCH_ID},
                {
                    "batch_id":   BATCH_ID,
                    "book":       BOOK_NAME,
                    "science_id": SCIENCE_ID,
                    "chapters":   PHASE2_CHAPTERS,
                    "rules_inserted": inserted,
                    "rules_updated":  updated,
                    "total_rules":    inserted + updated,
                    "errors":         len(errors),
                    "uploaded_at":    datetime.now(timezone.utc).isoformat(),
                },
                upsert=True
            )
            print(f"✅ import_batches log updated for batch {BATCH_ID}")
        except Exception as e:
            print(f"⚠  Could not write import_batches log: {e}")

        print(f"\nNEXT: Run validate_rules.py --batch-id {BATCH_ID}")
        client.close()


if __name__ == "__main__":
    main()
