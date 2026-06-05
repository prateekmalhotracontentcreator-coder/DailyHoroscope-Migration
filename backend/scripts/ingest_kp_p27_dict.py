#!/usr/bin/env python3
"""KP P27 Profession Dictionary ingest.

Source : KP_P27_Profession_Dictionary.json  (229 entries)
Target : horoscope_db.interpretation_rules
Batch  : kp_p27_dict_v1_20260604

Schema notes
------------
These are lookup entries (profession → ruling planets), NOT IF-THEN prediction
rules.  The AI validator is bypassed -- all 229 go in as pending_human_review
directly.  Co-founder sign-off required before any entry reaches 'approved'.

condition.type  = "kp_profession_ruler"
condition.profession = <profession name>  (runtime lookup key)
result.planets_indicated = [<planet>, ...]
result.notes = <notes text if present>

Category tags
-------------
Entries 1-173  : industry/trade professions  → tag "industry_profession"
Entries 174-206: government/ministry roles   → tag "government_ministry"
Entries 207-229: professional/admin roles    → tag "professional_role"
Ministry entries (name starts "Ministry -") also tagged "ministry"

Run from repo root:
    python3 backend/scripts/ingest_kp_p27_dict.py --dry-run
    python3 backend/scripts/ingest_kp_p27_dict.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import motor.motor_asyncio
import asyncio

# ── config ────────────────────────────────────────────────────────────────────
BATCH_ID        = "kp_p27_dict_v1_20260604"
BOOK_ID         = "kp_vol3_20260526"
SOURCE_BOOK     = "KP Astrology Vol 3"
SOURCE_CHAPTER  = "P27"
SCIENCE_ID      = "kp_jyotish"
EXPECTED_TOTAL  = 229

SOURCE_FILE = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/"
    "KP_CC_Decode/KP_P27_Profession_Dictionary.json"
)

LOG_DIR  = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")
TS       = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
LOG_PATH = LOG_DIR / f"ingest_kp_p27_dict_{TS}.log"

# ── tee-logging ───────────────────────────────────────────────────────────────
_buf: list[str] = []

def out(msg: str = "") -> None:
    print(msg)
    _buf.append(msg)

def _write_log(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(_buf) + "\n", encoding="utf-8")
    print(f"Log saved: {path}")


# ── category helper ───────────────────────────────────────────────────────────
def _category_tags(index_1based: int, profession: str) -> list[str]:
    """Return category tags based on position and profession name."""
    base = ["kp_profession_dictionary", "career", "profession"]
    if index_1based <= 173:
        base.append("industry_profession")
    elif index_1based <= 206:
        base.append("government_ministry")
        if profession.startswith("Ministry"):
            base.append("ministry")
    else:
        base.append("professional_role")
    return base


def _entry_category(index_1based: int, profession: str) -> str:
    if index_1based <= 173:
        return "industry_profession"
    elif index_1based <= 206:
        return "government_ministry"
    else:
        return "professional_role"


# ── rule builder ──────────────────────────────────────────────────────────────
def build_rule(index_1based: int, entry: dict) -> dict:
    profession: str = entry["profession"].strip()
    planets: list[str] = [p.strip() for p in entry.get("planets", [])]
    notes: str = (entry.get("notes") or "").strip()

    rule_id = f"kp3-p27dict-{index_1based:03d}"

    planets_str = ", ".join(planets)
    full_text = f"{profession} is ruled by {planets_str}."
    if notes:
        full_text += f" {notes}"

    summary = f"KP profession ruler for {profession}: {planets_str}."

    result_block: dict = {
        "planets_indicated": planets,
        "interpretation": full_text,
    }
    if notes:
        result_block["notes"] = notes

    rule = {
        "rule_id":          rule_id,
        "science_id":       SCIENCE_ID,
        "active":           True,
        "approval_status":  "pending_human_review",
        "checkable":        False,

        "source": {
            "book":         SOURCE_BOOK,
            "book_id":      BOOK_ID,
            "chapter":      SOURCE_CHAPTER,
            "batch_id":     BATCH_ID,
        },
        "ingest_batch_id":  BATCH_ID,

        "title":   f"Profession Ruler: {profession}",
        "summary": summary,
        "full_text": full_text,

        "tags":     _category_tags(index_1based, profession),
        "category": "career",

        "condition": {
            "type":       "kp_profession_ruler",
            "profession": profession,
        },

        "claim_axis":    "career",
        "claim_polarity": "neutral",
        "claim_scope":   "individual",
        "timing_bias":   None,
        "strength_band": None,
        "subject_scope": "individual",

        "authority_override":    False,
        "contradiction_flag":    False,
        "duplicate_candidate":   False,
        "duplicate_source":      None,
        "mutually_exclusive_with": None,

        "result": result_block,
    }
    return rule


# ── structural validation ─────────────────────────────────────────────────────
REQUIRED_FIELDS = [
    "rule_id", "science_id", "active", "approval_status",
    "source", "ingest_batch_id", "title", "full_text",
    "condition", "result",
]

def validate_rule(rule: dict) -> list[str]:
    errors: list[str] = []
    for f in REQUIRED_FIELDS:
        if rule.get(f) is None:
            errors.append(f"missing {f}")
    src = rule.get("source") or {}
    if src.get("book") != SOURCE_BOOK:
        errors.append(f"source.book mismatch: {src.get('book')}")
    if src.get("batch_id") != BATCH_ID:
        errors.append(f"source.batch_id mismatch: {src.get('batch_id')}")
    if rule.get("ingest_batch_id") != BATCH_ID:
        errors.append(f"ingest_batch_id mismatch: {rule.get('ingest_batch_id')}")
    if rule.get("approval_status") != "pending_human_review":
        errors.append(f"approval_status not pending_human_review: {rule.get('approval_status')}")
    cond = rule.get("condition") or {}
    if cond.get("type") != "kp_profession_ruler":
        errors.append(f"condition.type not kp_profession_ruler: {cond.get('type')}")
    if not cond.get("profession"):
        errors.append("condition.profession missing")
    res = rule.get("result") or {}
    if not res.get("planets_indicated"):
        errors.append("result.planets_indicated missing or empty")
    return errors


# ── main ──────────────────────────────────────────────────────────────────────
async def main(dry_run: bool) -> None:
    out(f"LOG FILE: {LOG_PATH}")
    out(f"{'=' * 70}")
    out(f"KP P27 PROFESSION DICTIONARY INGEST")
    out(f"Batch: {BATCH_ID}  |  Expected: {EXPECTED_TOTAL}")
    out(f"Dry-run: {dry_run}")
    out(f"{'=' * 70}")
    out()

    # ── load source ──────────────────────────────────────────────────────────
    if not SOURCE_FILE.exists():
        out(f"ERROR: source file not found: {SOURCE_FILE}")
        _write_log(LOG_PATH)
        sys.exit(1)

    raw: list[dict] = json.loads(SOURCE_FILE.read_text(encoding="utf-8"))
    out(f"Source file  : {SOURCE_FILE.name}")
    out(f"Entries found: {len(raw)}")
    if len(raw) != EXPECTED_TOTAL:
        out(f"WARNING: expected {EXPECTED_TOTAL}, got {len(raw)}")
    out()

    # ── build rules ──────────────────────────────────────────────────────────
    rules: list[dict] = []
    build_errors: list[str] = []

    for i, entry in enumerate(raw, start=1):
        rule = build_rule(i, entry)
        errs = validate_rule(rule)
        if errs:
            build_errors.append(f"  Entry {i:3d} ({entry.get('profession','?')}): {errs}")
        rules.append(rule)

    out(f"Rules built  : {len(rules)}")
    if build_errors:
        out(f"Build errors : {len(build_errors)}")
        for e in build_errors:
            out(e)
    else:
        out("Build errors : 0 ✓")
    out()

    # ── sample output ─────────────────────────────────────────────────────────
    out("── Sample rules ──────────────────────────────────────────────────────")
    for idx in [0, 1, 99, 173, 174, 205, 206, 228]:
        if idx < len(rules):
            r = rules[idx]
            cond = r["condition"]
            res  = r["result"]
            out(f"  [{idx+1:3d}] {r['rule_id']:22s} | {cond['profession']:40s} | {res['planets_indicated']}")
    out()

    # ── category breakdown ────────────────────────────────────────────────────
    from collections import Counter
    cats = Counter()
    for r in rules:
        for t in r["tags"]:
            if t in ("industry_profession", "government_ministry", "professional_role", "ministry"):
                cats[t] += 1
    out("── Category breakdown ────────────────────────────────────────────────")
    for cat, n in cats.most_common():
        out(f"  {cat:30s}: {n}")
    out()

    if dry_run:
        out("DRY-RUN complete -- no DB writes.")
        _write_log(LOG_PATH)
        return

    # ── DB upsert ─────────────────────────────────────────────────────────────
    mongo_url = os.environ.get("MONGO_URL")
    if not mongo_url:
        out("ERROR: MONGO_URL not set")
        _write_log(LOG_PATH)
        sys.exit(1)

    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
    db     = client["horoscope_db"]
    col    = db["interpretation_rules"]

    inserted = updated = errors_db = 0

    for rule in rules:
        try:
            existing = await col.find_one({"rule_id": rule["rule_id"]})
            if existing:
                await col.replace_one({"rule_id": rule["rule_id"]}, rule)
                updated += 1
            else:
                await col.insert_one(rule)
                inserted += 1
        except Exception as exc:
            out(f"  DB ERROR {rule['rule_id']}: {exc}")
            errors_db += 1

    out("── DB result ─────────────────────────────────────────────────────────")
    out(f"  Inserted : {inserted}")
    out(f"  Updated  : {updated}")
    out(f"  Errors   : {errors_db}")
    out(f"  Total    : {inserted + updated}")
    out()

    if inserted + updated == EXPECTED_TOTAL and errors_db == 0:
        out("✓ All 229 entries ingested successfully.")
    else:
        out(f"WARNING: expected {EXPECTED_TOTAL}, got {inserted + updated} with {errors_db} errors.")

    out()
    out("── Post-ingest structural check ──────────────────────────────────────")
    db_count = await col.count_documents({"ingest_batch_id": BATCH_ID})
    phr_count = await col.count_documents({
        "ingest_batch_id": BATCH_ID,
        "approval_status": "pending_human_review"
    })
    type_count = await col.count_documents({
        "ingest_batch_id": BATCH_ID,
        "condition.type": "kp_profession_ruler"
    })
    out(f"  Total in DB (batch)          : {db_count}")
    out(f"  pending_human_review         : {phr_count}")
    out(f"  condition.type=kp_profession_ruler: {type_count}")

    client.close()

    _write_log(LOG_PATH)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    asyncio.run(main(args.dry_run))
