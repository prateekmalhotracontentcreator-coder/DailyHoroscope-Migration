#!/usr/bin/env python3
"""
Ingest: Sarvato Bhadra Chakra (SBC) v1
Batch:  sbc_v1_20260605
Source: /Users/apple/Documents/Knowledge Engine_eBooks/
        New Ingest_5 Books/1. Sarvato Bhadra Chakra_V2/

16 chapters ingested (Ch02-Ch18, excl Ch15/19/20 -- scoped out per SBC_Session_Answers_2026-05-20.md):
  Ch02 Ch03 Ch04 Ch05 Ch06 Ch07 Ch08 Ch09 Ch10
  Ch11 Ch12 Ch13 Ch14 Ch16 Ch17 Ch18

3 source schemas:
  C -- Ch02/03/04 : full_text + summary + result.effect (no top-level effect or interpretation)
  A -- Ch05-Ch10  : title + description + effect.claim
  B -- Ch11-Ch18  : title + interpretation.result (no source dict, source_ref string)

Usage (from repo root):
    # Dry-run -- structural validation only, no DB write:
    python3 backend/scripts/ingest_sbc_v1.py --dry-run

    # Live ingest:
    python3 backend/scripts/ingest_sbc_v1.py --mongo-url "$MONGO_URL"

    # Live ingest with custom DB:
    python3 backend/scripts/ingest_sbc_v1.py --mongo-url "$MONGO_URL" --db-name horoscope_db
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

# ── Tee-logging ────────────────────────────────────────────────────────────────
LOG_DIR  = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")
TS       = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
LOG_PATH = LOG_DIR / f"sbc_ingest_{TS}.log"
_buf: list[str] = []

def out(msg: str = "") -> None:
    print(msg); _buf.append(msg)

def _write_log(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(_buf) + "\n", encoding="utf-8")
    print(f"Log saved: {p}")

# ── Constants ───────────────────────────────────────────────────────────────────
BATCH_ID  = "sbc_v1_20260605"
BOOK      = "Sarvato Bhadra Chakra"
BOOK_ID   = "sbc_v2_20260518"
SRC_DIR   = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/"
    "New Ingest_5 Books/1. Sarvato Bhadra Chakra_V2"
)

# Chapters included (Ch15/19/20 scoped out per architecture decisions 2026-05-20)
CHAPTER_FILES = [
    ("SBC_Ch02_Rules_v1.json",  2),
    ("SBC_Ch03_Rules_v1.json",  3),
    ("SBC_Ch04_Rules_v1.json",  4),
    ("SBC_Ch05_Rules_v1.json",  5),
    ("SBC_Ch06_Rules_v1.json",  6),
    ("SBC_Ch07_Rules_v1.json",  7),
    ("SBC_Ch08_Rules_v1.json",  8),
    ("SBC_Ch09_Rules_v1.json",  9),
    ("SBC_Ch10_Rules_v1.json", 10),
    ("SBC_Ch11_Rules_v1.json", 11),
    ("SBC_Ch12_Rules_v1.json", 12),
    ("SBC_Ch13_Rules_v1.json", 13),
    ("SBC_Ch14_Rules_v1.json", 14),
    ("SBC_Ch16_Rules_v1.json", 16),
    ("SBC_Ch17_Rules_v1.json", 17),
    ("SBC_Ch18_Rules_v1.json", 18),
]

# Chapter name map -- used when reconstructing source dict for Schema B
CHAPTER_NAMES = {
    2:  "Elementary Norms and Time Conversion",
    3:  "Sarvato Bhadra Chakra and Its Constituents",
    4:  "All About Stars",
    5:  "All About Planets",
    6:  "All About Signs",
    7:  "Numerical Strength of Planets",
    8:  "General Strength of Planets (Shadbala)",
    9:  "Vedha Aspect of Planets",
    10: "Forecasting Methodology -- Future of Individuals",
    11: "Muhurata Optimization",
    12: "Sickness and Accident Diagnostic",
    13: "Geopolitical and War Analysis",
    14: "Horary Diagnostic",
    16: "Social and Group Events",
    17: "Master Coordinate Library",
    18: "Sarvato Bhadra Chakra and Other Important Chakras",
}

# ── Schema detection ────────────────────────────────────────────────────────────
def _detect_schema(rule: dict) -> str:
    """Return 'A', 'B', or 'C' based on top-level key presence."""
    if "effect" in rule:
        return "A"
    if "interpretation" in rule and isinstance(rule["interpretation"], dict):
        return "B"
    # Schema C: full_text + summary + result.effect (Ch02/03/04)
    return "C"

# ── Interpretation mapping ──────────────────────────────────────────────────────
def _map_interpretation(rule: dict, schema: str) -> dict:
    """Return {'detailed': str, 'summary': str} for the rule."""
    if schema == "C":
        detailed = (
            rule.get("full_text")
            or rule.get("result", {}).get("effect")
            or rule.get("summary")
            or ""
        )
        summary  = rule.get("summary") or detailed[:400]

    elif schema == "A":
        effect_claim = (rule.get("effect") or {}).get("claim", "")
        description  = rule.get("description", "")
        detailed     = description
        if effect_claim and effect_claim not in description:
            detailed = description + "\n\nEffect: " + effect_claim
        summary = description[:400] if description else effect_claim[:400]

    else:  # Schema B
        interp   = rule.get("interpretation") or {}
        detailed = interp.get("result", "")
        summary  = detailed[:400]

    return {"detailed": detailed.strip(), "summary": summary.strip()}


# ── Source dict mapping ─────────────────────────────────────────────────────────
def _map_source(rule: dict, ch_num: int, schema: str) -> dict:
    """Return a standardised source dict."""
    if schema in ("A", "C"):
        src = dict(rule.get("source") or {})
        src["batch_id"] = BATCH_ID          # overwrite old chapter batch_id
        return src
    else:  # Schema B -- reconstruct from source_ref string
        return {
            "book":         BOOK,
            "book_id":      BOOK_ID,
            "chapter":      ch_num,
            "chapter_name": CHAPTER_NAMES.get(ch_num, f"Chapter {ch_num}"),
            "sloka":        None,
            "batch_id":     BATCH_ID,
            "passage_ref_id": None,
            "source_ref":   rule.get("source_ref", ""),
        }


# ── inject_fields ───────────────────────────────────────────────────────────────
def inject_fields(rule: dict, ch_num: int, now_iso: str) -> dict:
    """
    Normalise a source-JSON rule into the standard KE interpretation_rules schema.
    Mutates and returns a NEW dict.
    """
    schema = _detect_schema(rule)
    r      = deepcopy(rule)

    # Mandatory injected fields
    r["ingest_batch_id"]   = BATCH_ID
    r["ingested_at"]       = now_iso
    r["approval_status"]   = "pending_human_review"
    r["source_book"]       = BOOK
    r["active"]            = r.get("active", True)
    r["checkable"]         = r.get("checkable", False)

    # Standardise source dict (and ensure source.batch_id is set)
    r["source"] = _map_source(r, ch_num, schema)

    # Standardise interpretation block
    r["interpretation"] = _map_interpretation(r, schema)

    # Ensure condition is a non-empty dict
    cond = r.get("condition")
    if not isinstance(cond, dict) or not cond:
        r["condition"] = {"type": "engine_specification"}

    # Normalise claim_scope default (missing in Schema B)
    if not r.get("claim_scope"):
        pol = r.get("claim_polarity", "neutral")
        r["claim_scope"] = "engine_specification" if pol == "neutral" else "event_timing"

    # Remove Schema-B top-level fields that have been absorbed into source/interpretation
    for k in ("source_ref", "batch_id", "result", "full_text", "summary",
              "description", "effect", "category", "passage_ref_id"):
        r.pop(k, None)

    return r


# ── Structural validation ───────────────────────────────────────────────────────
REQUIRED_FIELDS = [
    "rule_id", "science_id", "approval_status", "checkable", "active",
    "source", "ingest_batch_id", "interpretation", "condition",
    "claim_axis", "claim_polarity",
]

def _validate_rule(r: dict, issues: list[str]) -> None:
    rid = r.get("rule_id", "<unknown>")

    for f in REQUIRED_FIELDS:
        if f not in r:
            issues.append(f"{rid}: missing field '{f}'")

    if r.get("ingest_batch_id") != BATCH_ID:
        issues.append(f"{rid}: ingest_batch_id mismatch")
    if (r.get("source") or {}).get("batch_id") != BATCH_ID:
        issues.append(f"{rid}: source.batch_id mismatch")
    if r.get("science_id") != "sbc":
        issues.append(f"{rid}: science_id != 'sbc'")

    interp = r.get("interpretation") or {}
    if not interp.get("detailed"):
        issues.append(f"{rid}: interpretation.detailed is empty")
    if not interp.get("summary"):
        issues.append(f"{rid}: interpretation.summary is empty")

    cond = r.get("condition")
    if not isinstance(cond, dict) or not cond:
        issues.append(f"{rid}: condition is empty or not a dict")


# ── Load all chapters ───────────────────────────────────────────────────────────
def load_all_rules() -> list[dict]:
    rules = []
    for filename, ch_num in CHAPTER_FILES:
        path = SRC_DIR / filename
        if not path.exists():
            out(f"  WARNING: {filename} not found -- skipping")
            continue
        raw = json.loads(path.read_text(encoding="utf-8"))
        out(f"  {filename:35s}  {len(raw):3d} rules")
        rules.extend((r, ch_num) for r in raw)
    return rules


# ── Main ────────────────────────────────────────────────────────────────────────
def main() -> None:
    out(f"LOG FILE: {LOG_PATH}")
    out("=" * 60)
    out(f"SBC KE Ingest v1")
    out(f"Batch:   {BATCH_ID}")
    out(f"Source:  {SRC_DIR}")
    out(f"Run:     {TS}")
    out("=" * 60)
    out()

    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument("--dry-run", action="store_true",
                        help="Structural validation only -- no DB write")
    args = parser.parse_args()

    if not args.dry_run and not args.mongo_url:
        out("ERROR: --mongo-url not provided and MONGO_URL not set.")
        sys.exit(1)

    # ── Step 1: Load ────────────────────────────────────────────────────────────
    out("STEP 1 -- Loading source JSON files")
    raw_pairs = load_all_rules()
    out(f"  Total raw rules loaded: {len(raw_pairs)}")
    out()

    # ── Step 2: Transform ───────────────────────────────────────────────────────
    out("STEP 2 -- Transforming to standard schema")
    now_iso = datetime.now(timezone.utc).isoformat()
    transformed: list[dict] = []
    for raw_rule, ch_num in raw_pairs:
        transformed.append(inject_fields(raw_rule, ch_num, now_iso))
    out(f"  Transformed: {len(transformed)} rules")
    out()

    # ── Step 3: Structural validation ───────────────────────────────────────────
    out("STEP 3 -- Structural validation")
    issues: list[str] = []

    # Duplicate rule_id check
    seen_ids: dict[str, int] = {}
    for i, r in enumerate(transformed):
        rid = r.get("rule_id", "")
        if rid in seen_ids:
            issues.append(f"Duplicate rule_id '{rid}' at index {i} (first at {seen_ids[rid]})")
        else:
            seen_ids[rid] = i

    for r in transformed:
        _validate_rule(r, issues)

    if issues:
        out(f"  Issues: {len(issues)}")
        for iss in issues:
            out(f"    ❌  {iss}")
        out()
        if not args.dry_run:
            out("ABORT: structural issues found -- fix before live ingest.")
            sys.exit(1)
    else:
        out(f"  Issues: 0  ✅")
    out()

    # ── Step 4: Per-chapter summary ─────────────────────────────────────────────
    out("STEP 4 -- Per-chapter breakdown")
    ch_counts: dict[int, int] = {}
    for r in transformed:
        ch = r.get("source", {}).get("chapter", 0)
        ch_counts[ch] = ch_counts.get(ch, 0) + 1
    for ch in sorted(ch_counts):
        out(f"  Ch{ch:02d}  {CHAPTER_NAMES.get(ch, '?'):45s}  {ch_counts[ch]:3d} rules")
    out(f"  {'TOTAL':50s}  {len(transformed):3d} rules")
    out()

    if args.dry_run:
        out("DRY-RUN complete.  No DB writes performed.")
        out()
        out("To run live ingest:")
        out("  python3 backend/scripts/ingest_sbc_v1.py --mongo-url \"$MONGO_URL\"")
        return

    # ── Step 5: Upload to MongoDB ────────────────────────────────────────────────
    out("STEP 5 -- Uploading to MongoDB")
    from pymongo import MongoClient, UpdateOne
    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=30000)
    col    = client[args.db_name]["interpretation_rules"]

    ops = [
        UpdateOne({"rule_id": r["rule_id"]}, {"$set": r}, upsert=True)
        for r in transformed
    ]
    result = col.bulk_write(ops, ordered=False)
    client.close()

    inserted = result.upserted_count
    updated  = result.modified_count
    out(f"  Inserted: {inserted}  Updated: {updated}  Total: {inserted + updated}")
    out()

    # ── Step 6: Write import_batches record ─────────────────────────────────────
    out("STEP 6 -- Writing import_batches log")
    log_path = Path(f"KE_TEXTBOOK_DECODE/Dedup_Reports/import_batch_{BATCH_ID}.json")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    batch_record = {
        "batch_id":    BATCH_ID,
        "book":        BOOK,
        "ingested_at": now_iso,
        "total_rules": len(transformed),
        "inserted":    inserted,
        "updated":     updated,
        "chapters":    sorted(ch_counts.keys()),
        "status":      "ingested",
    }
    log_path.write_text(json.dumps(batch_record, indent=2), encoding="utf-8")
    out(f"  Batch log: {log_path}")
    out()

    out("=" * 60)
    out("SBC INGEST COMPLETE")
    out(f"  {len(transformed)} rules → horoscope_db.interpretation_rules")
    out(f"  Batch: {BATCH_ID}")
    out()
    out("Next steps:")
    out("  1. Run doctrinal validator:")
    out(f"     python3 backend/validate_rules.py --batch-id {BATCH_ID} --mongo-url \"$MONGO_URL\"")
    out("  2. Triage results (3-bucket: A=artifact→AA, B=validator_error→PHR, C=genuine→flag)")
    out("  3. TT: co-founder sign-off on auto_approved rules")
    out("  4. TT: review 17 source gap OQs → patch_sbc_source_gaps.py when ready")
    out("=" * 60)


if __name__ == "__main__":
    try:
        main()
    finally:
        _write_log(LOG_PATH)
