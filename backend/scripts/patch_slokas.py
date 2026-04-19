#!/usr/bin/env python3
"""
patch_slokas.py — Targeted re-extraction for under-extracted slokas.

Re-runs extraction on specific sloka ranges from any Dasha chapter using the
current (improved) extraction prompt, then inserts only net-new rules into MongoDB.
Existing rules for the same sloka are preserved; new rules are added alongside them
with source_note='gap_fill' so reviewers can distinguish them in the Rules Browser.

Usage:
  python3 scripts/patch_slokas.py \
    --rtf "/path/to/chapter.rtf" \
    --chapter 58 \
    --dasha-lord Mercury \
    --batch-id bphs-ch58-dasha-20260419 \
    --slokas "39-40,52-53,59-61,62-63" \
    --mongo-url "$MONGO_URL" \
    --db-name EverydayHoroscope \
    [--dry-run]

Deduplication logic:
  For each re-extracted rule, check if any existing rule in MongoDB for the same
  (batch_id, sloka, sub_type) has a summary that shares >= 60% word overlap.
  If yes → skip (duplicate). If no → insert as new pending_review rule.
"""

import argparse
import os
import sys
import uuid
from datetime import datetime, timezone

import anthropic
import motor.motor_asyncio
import asyncio
from pydantic import BaseModel

# ── Import shared extraction logic from the main ingest script ─────────────────
sys.path.insert(0, os.path.dirname(__file__))
from ingest_bphs_dasha_v1 import (
    EXTRACTION_SYSTEM,
    EXTRACTION_PROMPT,
    CHAPTER_NAMES,
    SlokaExtractor,
    strip_rtf,
    parse_dasha_slokas,
)


# ── Deduplication ──────────────────────────────────────────────────────────────

def word_overlap(a: str, b: str) -> float:
    """Jaccard word overlap between two summary strings."""
    wa = set(a.lower().split())
    wb = set(b.lower().split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def is_duplicate(new_summary: str, existing_summaries: list[str], threshold: float = 0.60) -> bool:
    return any(word_overlap(new_summary, s) >= threshold for s in existing_summaries)


# ── Sloka range parsing ────────────────────────────────────────────────────────

def parse_sloka_ranges(slokas_arg: str) -> list[str]:
    """Parse '39-40,52-53,59-61' → ['39-40', '52-53', '59-61']"""
    return [s.strip() for s in slokas_arg.split(",") if s.strip()]


def sloka_label_matches(label: str, targets: list[str]) -> bool:
    """Check if a sloka's label matches any target range."""
    label_norm = label.strip()
    for t in targets:
        if label_norm == t:
            return True
        # Also match single-number target against range labels
        try:
            t_start, t_end = (int(x) for x in t.split("-")) if "-" in t else (int(t), int(t))
            if "-" in label_norm:
                l_start, l_end = (int(x) for x in label_norm.split("-"))
            else:
                l_start = l_end = int(label_norm)
            if l_start == t_start and l_end == t_end:
                return True
        except ValueError:
            pass
    return False


# ── Main ───────────────────────────────────────────────────────────────────────

async def run(args):
    # Connect to MongoDB
    client = motor.motor_asyncio.AsyncIOMotorClient(args.mongo_url)
    db = client[args.db_name]
    collection = db["knowledge_rules"]

    chapter = args.chapter
    dasha_lord = args.dasha_lord
    batch_id = args.batch_id
    target_slokas = parse_sloka_ranges(args.slokas)
    chapter_name = CHAPTER_NAMES.get(chapter, f"Chapter {chapter}")

    print(f"\nPatch Slokas — Ch {chapter} {chapter_name}")
    print(f"Dasha lord : {dasha_lord}")
    print(f"Batch ID   : {batch_id}")
    print(f"Target     : {', '.join(target_slokas)}")
    print(f"Mode       : {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("─" * 60)

    # Parse RTF
    rtf_text = strip_rtf(args.rtf)
    all_slokas = parse_dasha_slokas(rtf_text, chapter)

    # Filter to target slokas only
    targets = [s for s in all_slokas if sloka_label_matches(s["sloka"], target_slokas)]
    if not targets:
        print(f"ERROR: No slokas matched {target_slokas} in the parsed RTF.")
        print(f"Available slokas: {[s['sloka'] for s in all_slokas]}")
        return

    extractor = SlokaExtractor(model=args.model)
    total_new = 0
    total_skipped = 0

    for entry in targets:
        sloka_label = entry["sloka"]
        sloka_text = entry.get("text", "")
        antardasha_planet = entry.get("antardasha_planet", dasha_lord)

        # Fetch existing rules for this sloka from MongoDB
        existing_docs = await collection.find(
            {"batch_id": batch_id, "sloka": sloka_label}
        ).to_list(length=None)
        existing_summaries = [d.get("summary", "") for d in existing_docs]
        existing_count = len(existing_docs)

        print(f"\n  Sloka {sloka_label:10s} | existing: {existing_count} | re-extracting...")

        # Re-extract with improved prompt
        try:
            new_rules = extractor.extract(
                sloka_label=sloka_label,
                rule_text=sloka_text,
                notes_text="",
                chapter=chapter,
                dasha_lord=dasha_lord,
                antardasha_planet=antardasha_planet,
            )
        except Exception as e:
            print(f"    ERROR extracting sloka {sloka_label}: {e}")
            continue

        sloka_new = 0
        sloka_skipped = 0

        for rule in new_rules:
            summary = rule.summary if hasattr(rule, "summary") else str(rule)
            if is_duplicate(summary, existing_summaries):
                sloka_skipped += 1
                continue

            # Net-new rule — build document
            rule_id = f"R-BPHS{chapter:02d}-PATCH-{uuid.uuid4().hex[:6].upper()}"
            doc = {
                "rule_id": rule_id,
                "batch_id": batch_id,
                "source": "BPHS",
                "chapter": chapter,
                "sloka": sloka_label,
                "dasha_lord": dasha_lord,
                "antardasha_planet": antardasha_planet,
                "sub_type": rule.sub_type if hasattr(rule, "sub_type") else "dasha_unfavourable",
                "summary": summary,
                "condition": rule.condition if hasattr(rule, "condition") else "",
                "result": rule.result if hasattr(rule, "result") else "",
                "planets": rule.planets if hasattr(rule, "planets") else [],
                "houses": rule.houses if hasattr(rule, "houses") else [],
                "approval_status": "pending_review",
                "source_note": "gap_fill",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }

            if args.dry_run:
                print(f"    [DRY RUN] Would insert: {rule_id} | {doc['sub_type']:22s} | {summary[:70]}...")
            else:
                await collection.insert_one(doc)
                print(f"    Inserted : {rule_id} | {doc['sub_type']:22s} | {summary[:70]}...")

            existing_summaries.append(summary)  # prevent same-run duplicates
            sloka_new += 1

        print(f"    Result   : +{sloka_new} new  |  {sloka_skipped} skipped (duplicates)")
        total_new += sloka_new
        total_skipped += sloka_skipped

    print(f"\n{'─' * 60}")
    if args.dry_run:
        print(f"[DRY RUN] Would insert {total_new} net-new rules  |  {total_skipped} duplicates skipped")
    else:
        print(f"✅ Inserted {total_new} net-new rules  |  {total_skipped} duplicates skipped")
        print(f"   All new rules: approval_status='pending_review', source_note='gap_fill'")
        print(f"   Review in Admin > Library > Rules Browser → filter: batch {batch_id}, source_note: gap_fill")


def main():
    parser = argparse.ArgumentParser(
        description="Re-extract specific under-extracted slokas and insert net-new rules."
    )
    parser.add_argument("--rtf",        required=True,  help="Path to chapter RTF file")
    parser.add_argument("--chapter",    required=True,  type=int)
    parser.add_argument("--dasha-lord", required=True,
                        choices=["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"])
    parser.add_argument("--batch-id",   required=True,  help="Existing batch ID to patch")
    parser.add_argument("--slokas",     required=True,
                        help="Comma-separated sloka ranges to re-extract, e.g. '39-40,52-53,59-61'")
    parser.add_argument("--mongo-url",  required=True)
    parser.add_argument("--db-name",    required=True)
    parser.add_argument("--model",      default="claude-haiku-4-5")
    parser.add_argument("--dry-run",    action="store_true")
    args = parser.parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
