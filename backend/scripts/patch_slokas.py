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
    --slokas "59-61" \
    --mongo-url "$MONGO_URL" \
    --db-name EverydayHoroscope \
    [--dry-run]

Deduplication: for each re-extracted rule, checks if any existing rule in MongoDB
for the same (batch_id, sloka, sub_type) has a summary with >= 60% Jaccard word
overlap. Skips duplicates; inserts only net-new rules.
"""

import argparse
import os
import sys
import uuid
from datetime import datetime, timezone

import pymongo

sys.path.insert(0, os.path.dirname(__file__))
from ingest_bphs_dasha_v1 import (
    CHAPTER_NAMES,
    SlokaExtractor,
    strip_rtf,
    parse_dasha_slokas,
)


# ── Deduplication ──────────────────────────────────────────────────────────────

def word_overlap(a: str, b: str) -> float:
    wa = set(a.lower().split())
    wb = set(b.lower().split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def is_duplicate(new_summary: str, existing_summaries: list, threshold: float = 0.60) -> bool:
    return any(word_overlap(new_summary, s) >= threshold for s in existing_summaries)


# ── Sloka range helpers ────────────────────────────────────────────────────────

def parse_sloka_ranges(slokas_arg: str) -> list:
    return [s.strip() for s in slokas_arg.split(",") if s.strip()]


def sloka_label_matches(label: str, targets: list) -> bool:
    label_norm = label.strip()
    for t in targets:
        if label_norm == t:
            return True
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

def main():
    parser = argparse.ArgumentParser(
        description="Re-extract specific under-extracted slokas and insert net-new rules."
    )
    parser.add_argument("--rtf",        required=True)
    parser.add_argument("--chapter",    required=True, type=int)
    parser.add_argument("--dasha-lord", required=True,
                        choices=["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"])
    parser.add_argument("--batch-id",   required=True)
    parser.add_argument("--slokas",     required=True,
                        help="Comma-separated sloka ranges, e.g. '39-40,59-61'")
    parser.add_argument("--mongo-url",  required=True)
    parser.add_argument("--db-name",    required=True)
    parser.add_argument("--model",      default="claude-haiku-4-5")
    parser.add_argument("--dry-run",    action="store_true")
    args = parser.parse_args()

    chapter      = args.chapter
    dasha_lord   = args.dasha_lord
    batch_id     = args.batch_id
    target_slokas = parse_sloka_ranges(args.slokas)
    chapter_name  = CHAPTER_NAMES.get(chapter, f"Chapter {chapter}")

    print(f"\nPatch Slokas — Ch {chapter} {chapter_name}")
    print(f"Dasha lord : {dasha_lord}")
    print(f"Batch ID   : {batch_id}")
    print(f"Target     : {', '.join(target_slokas)}")
    print(f"Mode       : {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("─" * 60)

    # MongoDB (sync)
    mongo_client = pymongo.MongoClient(args.mongo_url)
    db           = mongo_client[args.db_name]
    collection   = db["knowledge_rules"]

    # Parse RTF
    rtf_text  = strip_rtf(args.rtf)
    all_slokas = parse_dasha_slokas(rtf_text, chapter)

    targets = [s for s in all_slokas if sloka_label_matches(s["sloka"], target_slokas)]
    if not targets:
        print(f"ERROR: No slokas matched {target_slokas} in the parsed RTF.")
        print(f"Available: {[s['sloka'] for s in all_slokas]}")
        return

    extractor   = SlokaExtractor(model=args.model)
    total_new   = 0
    total_skipped = 0

    for entry in targets:
        sloka_label       = entry["sloka"]
        sloka_text        = entry.get("text", "")
        antardasha_planet = entry.get("antardasha_planet", dasha_lord)

        existing_docs     = list(collection.find({"batch_id": batch_id, "sloka": sloka_label}))
        existing_summaries = [d.get("summary", "") for d in existing_docs]
        existing_count    = len(existing_docs)

        print(f"\n  Sloka {sloka_label:10s} | existing: {existing_count} | re-extracting...")

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
            print(f"    ERROR: {e}")
            continue

        sloka_new = sloka_skipped = 0

        for rule in new_rules:
            summary  = getattr(rule, "summary", str(rule))
            sub_type = getattr(rule, "sub_type", "dasha_unfavourable")

            if is_duplicate(summary, existing_summaries):
                sloka_skipped += 1
                continue

            rule_id = f"R-BPHS{chapter:02d}-PATCH-{uuid.uuid4().hex[:6].upper()}"
            doc = {
                "rule_id":           rule_id,
                "batch_id":          batch_id,
                "source":            "BPHS",
                "chapter":           chapter,
                "sloka":             sloka_label,
                "dasha_lord":        dasha_lord,
                "antardasha_planet": antardasha_planet,
                "sub_type":          sub_type,
                "summary":           summary,
                "condition":         getattr(rule, "condition", ""),
                "result":            getattr(rule, "result", ""),
                "planets":           getattr(rule, "planets", []),
                "houses":            getattr(rule, "houses", []),
                "approval_status":   "pending_review",
                "source_note":       "gap_fill",
                "created_at":        datetime.now(timezone.utc).isoformat(),
            }

            if args.dry_run:
                print(f"    [DRY RUN] {rule_id} | {sub_type:22s} | {summary[:72]}...")
            else:
                collection.insert_one(doc)
                print(f"    Inserted  {rule_id} | {sub_type:22s} | {summary[:72]}...")

            existing_summaries.append(summary)
            sloka_new += 1

        print(f"    Result: +{sloka_new} new  |  {sloka_skipped} skipped (duplicates)")
        total_new     += sloka_new
        total_skipped += sloka_skipped

    print(f"\n{'─' * 60}")
    if args.dry_run:
        print(f"[DRY RUN] Would insert {total_new} net-new rules  |  {total_skipped} duplicates skipped")
    else:
        print(f"✅  Inserted {total_new} net-new rules  |  {total_skipped} duplicates skipped")
        if total_new:
            print(f"    approval_status='pending_review', source_note='gap_fill'")
            print(f"    Review: Admin > Library > Rules Browser → batch {batch_id} → source_note: gap_fill")

    mongo_client.close()


if __name__ == "__main__":
    main()
