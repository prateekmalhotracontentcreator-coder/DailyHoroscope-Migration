#!/usr/bin/env python3
"""
ingest_phaladeepika_v1.py
-------------------------------------------------------------------
Ingest Phaladeepika (28 chapters, 1,218 rules) into horoscope_db.

Source: /Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode/
Batch:  phaladeepika-v1-20260601

THREE source schemas detected during schema audit (2026-06-01):

  Schema A -- Ch01-Ch13, Ch15-Ch16, Ch18, Ch27 (758 active rules)
    Fields: full_text, summary, condition (dict), claim_polarity,
            category, science_id, source (full dict w/ original_text)

  Schema C -- Ch14, Ch17, Ch19-Ch25 (355 active rules)
    Fields: description, conditions (list), rule_type, claim_polarity,
            source (partial, no original_text), engine_dependency

  Schema B -- Ch22, Ch26, Ch28 (93 active rules)
    Fields: content, conditions (empty list), type, polarity,
            chapter + sloka as top-level fields (no source dict),
            engine_note

Mapping: full_text|description|content → interpretation.detailed
         summary|title           → interpretation.summary
         condition|conditions    → condition (canonical dict)
         category|rule_type|type → category
         claim_polarity|polarity → claim_polarity

12 TBA/inactive rules (Ch08 PDF gap) are ingested with active=False.
All source approval_status values IGNORED -- all rules enter as
approval_status="pending_review" for validate_rules.py to process.

Usage:
    python3 backend/scripts/ingest_phaladeepika_v1.py --dry-run
    python3 backend/scripts/ingest_phaladeepika_v1.py \\
        --mongo-url "mongodb+srv://..." --db-name horoscope_db
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DECODE_FOLDER = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode/"
)
BATCH_ID    = "phaladeepika-v1-20260601"
SOURCE_BOOK = "Phaladeepika"
SCIENCE_ID  = "jyotish"

# Chapter files in order (Ch28 has 0 meaningful rules but 8 meta_notes -- ingest them)
CHAPTER_FILES = [
    "PD_Ch01_Definitions_Rules.json",
    "PD_Ch02_Planets_Rules.json",
    "PD_Ch03_Zodiac_Rules.json",
    "PD_Ch04_Shadbalas_Rules.json",
    "PD_Ch05_Profession_Rules.json",
    "PD_Ch06_Yogas_Rules.json",
    "PD_Ch07_Maharajayogas_Rules.json",
    "PD_Ch08_PlanetsInBhavas_Rules.json",
    "PD_Ch09_SignsAsLagna_Rules.json",
    "PD_Ch10_7thHouse_Rules.json",
    "PD_Ch11_FemaleHoroscopes_Rules.json",
    "PD_Ch12_Children_Rules.json",
    "PD_Ch13_LengthOfLife_Rules.json",
    "PD_Ch14_DiseasesDeath_Rules.json",
    "PD_Ch15_BhavaStudy_Rules.json",
    "PD_Ch16_GeneralBhavas_Rules.json",
    "PD_Ch17_ExitWorld_Rules.json",
    "PD_Ch18_Conjunctions_Rules.json",
    "PD_Ch19_Dasas_Rules.json",
    "PD_Ch20_BhavaLordDasas_Rules.json",
    "PD_Ch21_SubDivisionsOfDasas_Rules.json",
    "PD_Ch22_KalachakraDasa_Rules.json",
    "PD_Ch23_Ashtakavarga_Rules.json",
    "PD_Ch24_AshtakavargaEffects_Rules.json",
    "PD_Ch25_Upagrahas_Rules.json",
    "PD_Ch26_Transits_Rules.json",
    "PD_Ch27_AsceticYogas_Rules.json",
    "PD_Ch28_Upasamhara_Rules.json",
]


# ──────────────────────────────────────────────────────────────────────
# Schema mapping helpers
# ──────────────────────────────────────────────────────────────────────

def _map_interpretation(rule: dict) -> dict[str, str]:
    """Build interpretation.detailed + summary from whichever fields are present."""
    # Priority: full_text (Schema A) → description (Schema C) → content (Schema B) → title
    detailed = (
        rule.get("full_text") or
        rule.get("description") or
        rule.get("content") or
        ""
    ).strip()

    summary = (rule.get("summary") or "").strip()
    title   = (rule.get("title") or "").strip()

    # Enrich detailed with result text if it adds substantive info
    result = rule.get("result")
    if result:
        if isinstance(result, str) and result.strip():
            suffix = result.strip()
            if suffix not in detailed:
                detailed = detailed.rstrip(".") + "\n\nResult: " + suffix
        elif isinstance(result, dict):
            primary = (
                result.get("primary") or
                result.get("primary_outcome") or
                ""
            )
            if primary and str(primary).strip() not in detailed:
                detailed = (detailed + " " + str(primary).strip()).strip()

    if not summary:
        summary = title or (
            detailed[:120].rsplit(" ", 1)[0]
            if len(detailed) > 120
            else detailed
        )

    return {
        "detailed": detailed.strip(),
        "summary":  summary.strip(),
    }


def _map_condition(rule: dict) -> dict[str, Any]:
    """Map condition / conditions to a canonical condition dict."""
    # Schema A: condition is already a proper dict with type key
    cond = rule.get("condition")
    if isinstance(cond, dict) and cond and cond.get("type"):
        return cond

    # Schema B/C: conditions is a list
    conds = rule.get("conditions")
    if isinstance(conds, list) and conds:
        dict_conds = [c for c in conds if isinstance(c, dict)]
        str_conds  = [c for c in conds if isinstance(c, str)]

        if len(dict_conds) == 1:
            return dict_conds[0]
        elif len(dict_conds) > 1:
            return {
                "type":         "multi_condition",
                "all_required": True,
                "conditions":   dict_conds,
            }
        elif str_conds:
            # Ch26: string conditions like "Vedha must NOT be present"
            return {
                "type":        "engine_specification",
                "description": "; ".join(str_conds),
            }

    # Empty or missing -- derive from rule_type / type / category
    rule_type = (
        rule.get("rule_type") or
        rule.get("type") or
        rule.get("category") or
        "general_principle"
    )
    return {
        "type":        rule_type,
        "description": (rule.get("title") or ""),
    }


def _map_source(rule: dict) -> dict[str, Any]:
    """Build canonical source dict, always including batch_id."""
    src = rule.get("source")
    if isinstance(src, dict):
        out = dict(src)
        out["batch_id"] = BATCH_ID
        out.setdefault("book", SOURCE_BOOK)
        return out
    # Schema B: chapter + sloka / slokas as separate top-level fields
    return {
        "book":     SOURCE_BOOK,
        "chapter":  rule.get("chapter"),
        "sloka":    rule.get("sloka") or rule.get("slokas"),
        "batch_id": BATCH_ID,
    }


def transform_rule(rule: dict, now: str) -> dict[str, Any]:
    """Transform a source rule (any schema) into the canonical KE format."""
    out: dict[str, Any] = {}

    # ── Identity ──
    out["rule_id"]       = rule["rule_id"]
    out["science_id"]    = rule.get("science_id") or SCIENCE_ID
    out["source_book"]   = SOURCE_BOOK
    out["ingest_batch_id"] = BATCH_ID
    out["source"]        = _map_source(rule)

    # ── Status -- always pending_review at ingest ──
    out["approval_status"] = "pending_review"
    out["ingested_at"]     = now

    # ── Core content ──
    out["interpretation"] = _map_interpretation(rule)
    out["condition"]      = _map_condition(rule)

    # ── Classification ──
    out["category"] = (
        rule.get("category") or
        rule.get("rule_type") or
        rule.get("type") or
        "general_principle"
    )
    out["claim_polarity"] = (
        rule.get("claim_polarity") or
        rule.get("polarity") or
        "neutral"
    )
    out["claim_axis"]   = rule.get("claim_axis",   "general")
    out["claim_scope"]  = rule.get("claim_scope",  "natal")
    out["timing_bias"]  = rule.get("timing_bias",  "none")
    out["strength_band"] = rule.get("strength_band", "any")
    out["subject_scope"] = rule.get("subject_scope", "any")

    # ── Flags preserved from source ──
    out["active"]             = rule.get("active", True)
    out["checkable"]          = rule.get("checkable", False)
    out["tags"]               = rule.get("tags") or []
    out["duplicate_candidate"] = rule.get("duplicate_candidate", False)
    out["duplicate_source"]   = rule.get("duplicate_source")
    out["contradiction_flag"] = rule.get("contradiction_flag", False)
    out["cross_text_matches"] = rule.get("cross_text_matches")

    # ── Special flags -- only set if truthy in source ──
    for flag in ("tba", "pending_review", "gai_citation_unverified",
                 "engine_dependency", "engine_note", "engine_notes",
                 "vedha_nullifier", "decode_notes"):
        v = rule.get(flag)
        if v:
            out[flag] = v

    return out


# ──────────────────────────────────────────────────────────────────────
# Load all chapters
# ──────────────────────────────────────────────────────────────────────

def load_all_rules() -> list[dict]:
    all_rules: list[dict] = []
    for fname in CHAPTER_FILES:
        fp = DECODE_FOLDER / fname
        if not fp.exists():
            print(f"  [warn] missing file: {fname}")
            continue
        data = json.loads(fp.read_text(encoding="utf-8"))
        rules = data.get("rules", data) if isinstance(data, dict) else data
        if not isinstance(rules, list):
            print(f"  [warn] {fname}: not a list, skipping")
            continue
        all_rules.extend(rules)
        print(f"  Loaded {len(rules):4} rules from {fname}")
    return all_rules


# ──────────────────────────────────────────────────────────────────────
# Pre-upload structural validation
# ──────────────────────────────────────────────────────────────────────

VALID_CONDITION_TYPES = frozenset({
    "yoga_combination", "general_principle", "dosha", "neechabhanga_rule",
    "neechabhanga", "lagna_sign", "ashtakavarga_threshold", "engine_specification",
    "engine_spec", "methodology", "planet_in_house", "house_lord_placement",
    "planet_conjunction", "planet_in_sign", "varga_dignity_tier", "dasha_period",
    "planet_affliction", "planet_combust", "multi_condition", "predictive",
    "transit", "ashtakavarga_calculation", "planet_strength",
    "general_principle", "meta_note", "ascetic_yoga", "arishta_yoga",
    "planet_in_house_from_sun", "house_position", "yoga",
})


def validate_rules(rules: list[dict]) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    seen_ids: set[str] = set()
    for r in rules:
        rid = r.get("rule_id", "?")
        is_tba = r.get("tba", False)
        is_active = r.get("active", True)

        # Duplicate rule_id check
        if rid in seen_ids:
            issues.append((rid, "duplicate_rule_id"))
        seen_ids.add(rid)

        # Skip structural checks for TBA/inactive
        if is_tba or not is_active:
            continue

        interp = r.get("interpretation") or {}
        detailed = (interp.get("detailed") or "").strip()
        summary  = (interp.get("summary") or "").strip()
        if not detailed and not summary:
            issues.append((rid, "empty_interpretation"))

        cond = r.get("condition") or {}
        if not isinstance(cond, dict) or not cond:
            issues.append((rid, "missing_condition"))

        src = r.get("source") or {}
        if not src.get("batch_id"):
            issues.append((rid, "missing_source.batch_id"))

        if r.get("approval_status") != "pending_review":
            issues.append((rid, f"wrong_approval_status:{r.get('approval_status')}"))

    return issues


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Ingest Phaladeepika into horoscope_db.")
    p.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    p.add_argument("--db-name",   default="horoscope_db")
    p.add_argument("--dry-run",   action="store_true",
                   help="Transform + validate; do not write to MongoDB")
    p.add_argument("--save",      default="backend/scripts/phaladeepika_rules.json",
                   help="Path to save transformed rules JSON (always written)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    now  = datetime.now(timezone.utc).isoformat()

    print("\n" + "=" * 65)
    print("ingest_phaladeepika_v1.py")
    print(f"Mode:  {'DRY RUN' if args.dry_run else 'LIVE UPLOAD'}")
    print(f"Batch: {BATCH_ID}")
    print("=" * 65)

    # ── Step 1: Load ──
    print("\n── Loading source files ──")
    raw_rules = load_all_rules()
    print(f"\nTotal source rules loaded: {len(raw_rules)}")

    # ── Step 2: Transform ──
    print("\n── Transforming (schema mapping) ──")
    transformed: list[dict] = []
    for r in raw_rules:
        transformed.append(transform_rule(r, now))

    active   = sum(1 for r in transformed if r.get("active", True) and not r.get("tba"))
    inactive = sum(1 for r in transformed if not r.get("active", True) or r.get("tba"))
    print(f"  Transformed: {len(transformed)} total  |  {active} active  |  {inactive} TBA/inactive")

    # ── Step 3: Validate ──
    print("\n── Pre-upload structural validation ──")
    issues = validate_rules(transformed)
    for rid, reason in issues[:20]:
        print(f"  [issue] {rid}: {reason}")
    if issues:
        print(f"\n  TOTAL ISSUES: {len(issues)}")
        if not args.dry_run:
            print("  ABORTING -- fix issues before live upload")
            sys.exit(1)
    else:
        print(f"  Issues: 0  ✅")

    # ── Step 4: Save JSON ──
    save_path = Path(args.save)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text(json.dumps(transformed, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n── Saved transformed rules → {save_path} ──")

    if args.dry_run:
        # Print sample rules from each schema
        print("\n── Sample rules (first active from Ch01, Ch14, Ch22, Ch26) ──")
        by_ch = {}
        for r in transformed:
            ch = (r.get("source") or {}).get("chapter")
            if ch not in by_ch:
                by_ch[ch] = r
        for ch in [1, 14, 22, 26]:
            if ch in by_ch:
                r = by_ch[ch]
                print(f"\n  Ch{ch} [{r['rule_id']}]")
                print(f"    interpretation.detailed: {r['interpretation']['detailed'][:100]}...")
                print(f"    condition.type:  {r['condition'].get('type','?')}")
                print(f"    claim_polarity:  {r['claim_polarity']}")
                print(f"    category:        {r['category']}")
                print(f"    source.batch_id: {r['source'].get('batch_id','?')}")
        print(f"\n[DRY RUN] No writes made.")
        print("=" * 65)
        return

    # ── Step 5: Idempotency check ──
    from pymongo import MongoClient
    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=20000)
    db = client[args.db_name]

    existing = db["import_batches"].find_one({"batch_id": BATCH_ID})
    if existing:
        print(f"\n[ABORT] batch_id '{BATCH_ID}' already in import_batches. Idempotency guard.")
        print("  To re-run: delete the import_batches record manually and retry.")
        client.close()
        sys.exit(1)

    # ── Step 6: Upload ──
    print(f"\n── Uploading {len(transformed)} rules to {args.db_name}.interpretation_rules ──")
    inserted = 0
    skipped  = 0
    errors   = 0
    for r in transformed:
        try:
            rid = r["rule_id"]
            existing_rule = db["interpretation_rules"].find_one(
                {"rule_id": rid, "ingest_batch_id": BATCH_ID}, {"_id": 1}
            )
            if existing_rule:
                skipped += 1
                continue
            db["interpretation_rules"].insert_one(r)
            inserted += 1
        except Exception as e:
            errors += 1
            print(f"  [error] {r.get('rule_id','?')}: {e}")

    print(f"  Inserted: {inserted}  |  Skipped: {skipped}  |  Errors: {errors}")

    # ── Step 7: Write import_batches record ──
    db["import_batches"].insert_one({
        "batch_id":    BATCH_ID,
        "source_book": SOURCE_BOOK,
        "science_id":  SCIENCE_ID,
        "ingested_at": now,
        "rules_inserted": inserted,
        "rules_skipped":  skipped,
        "errors":         errors,
        "notes": (
            "28 chapters (Adhyaya I-XXVIII). 3 source schemas: "
            "A (Ch01-13,15-16,18,27: full_text+condition dict), "
            "C (Ch14,17,19-25: description+conditions list), "
            "B (Ch22,26,28: content+empty conditions). "
            "12 TBA/inactive rules (Ch08 PDF gap). "
            "gai_citation_unverified: pd-ch21-041. "
            "~25 MED OCR items set pending_review:true post-validate."
        ),
        "triage_status": "pending",
    })
    print(f"  import_batches record written: {BATCH_ID}")

    # ── Step 8: Verification query ──
    count = db["interpretation_rules"].count_documents({"ingest_batch_id": BATCH_ID})
    print(f"\n── Verification: {count} rules in DB with batch_id={BATCH_ID} ──")

    client.close()
    print(f"\n{'=' * 65}")
    print("NEXT STEPS:")
    print(f"  1. Run validate_rules.py:")
    print(f"     ANTHROPIC_API_KEY='sk-ant-...' python3 backend/scripts/validate_rules.py \\")
    print(f"       --batch-id {BATCH_ID} --mongo-url \"$MONGO_URL\" --db-name {args.db_name}")
    print(f"  2. Triage flagged rules (Bucket A/B/C).")
    print(f"  3. Update .claude/ke/ingest/PHALADEEPIKA_INGEST.md.")
    print("=" * 65)


if __name__ == "__main__":
    main()
