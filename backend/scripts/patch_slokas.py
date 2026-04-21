#!/usr/bin/env python3
"""
patch_slokas.py — Targeted re-extraction for under-extracted slokas.

Re-runs extraction on specific sloka ranges using the current (improved) prompt,
then inserts only net-new rules into MongoDB alongside existing ones.
New rules are tagged source_note='gap_fill' for Rules Browser review.

Usage:
  python3 scripts/patch_slokas.py \
    --rtf "/path/to/chapter.rtf" \
    --chapter 58 \
    --dasha-lord Mercury \
    --batch-id bphs-ch58-dasha-20260419 \
    --slokas "59-61" \
    --mongo-url "$MONGO_URL" \
    --db-name horoscope_db \
    [--dry-run]
"""

import argparse
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pymongo

sys.path.insert(0, os.path.dirname(__file__))
from ingest_bphs_dasha_v1 import (
    CHAPTER_NAMES,
    SlokaExtractor,
    OpenAISlokaExtractor,
    strip_rtf,
    split_into_sloka_blocks,
    build_planet_position_map,
    clean_notes,
    should_skip,
    extracted_to_rule,
    make_source,
    SCIENCE,
    PLANETS,
    VALID_SUB_TYPES,
)


# ── Deduplication ──────────────────────────────────────────────────────────────

def word_overlap(a: str, b: str) -> float:
    wa = set(a.lower().split())
    wb = set(b.lower().split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def condition_part(summary: str) -> str:
    """Extract only the condition side of a summary (before ' → ').

    Summaries are formatted as 'Condition text → Result text'.
    Comparing the full string causes false duplicate hits when rules share
    a long result sentence but have distinct conditions (e.g. different
    house lords all producing the same broad life outcome).
    Comparing only the condition side avoids this while still catching
    true duplicates where the condition itself repeats.
    """
    return summary.split(" → ")[0].strip() if " → " in summary else summary


def is_duplicate(new_summary: str, existing_summaries: list, threshold: float = 0.60) -> bool:
    new_cond = condition_part(new_summary)
    return any(word_overlap(new_cond, condition_part(s)) >= threshold for s in existing_summaries)


# ── Sloka range helpers ────────────────────────────────────────────────────────

def parse_sloka_ranges(arg: str) -> list:
    return [s.strip() for s in arg.split(",") if s.strip()]


def sloka_label_matches(label: str, targets: list) -> bool:
    label_norm = label.strip()
    for t in targets:
        if label_norm == t:
            return True
        try:
            t_start, t_end = (int(x) for x in t.split("-")) if "-" in t else (int(t), int(t))
            l_start, l_end = (int(x) for x in label_norm.split("-")) if "-" in label_norm else (int(label_norm), int(label_norm))
            if l_start == t_start and l_end == t_end:
                return True
        except ValueError:
            pass
    return False


# ── Summary extraction helper ──────────────────────────────────────────────────

def rule_summary(rule_doc: dict) -> str:
    """Extract a comparable summary string from a stored rule document."""
    interp = rule_doc.get("interpretation", {})
    return interp.get("summary", "") or rule_doc.get("summary", "")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Re-extract specific under-extracted slokas.")
    parser.add_argument("--rtf",        required=True)
    parser.add_argument("--chapter",    required=True, type=int)
    parser.add_argument("--dasha-lord", required=True,
                        choices=["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"])
    parser.add_argument("--batch-id",   required=True)
    parser.add_argument("--slokas",     required=True,
                        help="Comma-separated sloka ranges, e.g. '39-40,59-61'")
    parser.add_argument("--mongo-url",  required=True)
    parser.add_argument("--db-name",    required=True)
    parser.add_argument("--model",         default="claude-haiku-4-5")
    parser.add_argument("--provider",      choices=["anthropic", "openai"], default="anthropic",
                        help="AI provider: 'anthropic' (default) or 'openai'")
    parser.add_argument("--openai-model",  default="gpt-4o-mini",
                        help="OpenAI model when --provider=openai (default: gpt-4o-mini)")
    parser.add_argument("--dry-run",       action="store_true")
    parser.add_argument("--split-upgrade", action="store_true",
                        help="Tag new rules as split_upgrade instead of gap_fill. "
                             "Use when replacing pre_split_merged merged-condition rules.")
    args = parser.parse_args()

    chapter       = args.chapter
    dasha_lord    = args.dasha_lord
    batch_id      = args.batch_id
    target_slokas = parse_sloka_ranges(args.slokas)
    chapter_name  = CHAPTER_NAMES.get(chapter, f"Chapter {chapter}")
    new_source_note = "split_upgrade" if args.split_upgrade else "gap_fill"

    print(f"\nPatch Slokas — Ch {chapter} {chapter_name}")
    print(f"Dasha lord : {dasha_lord}")
    print(f"Batch ID   : {batch_id}")
    print(f"Target     : {', '.join(target_slokas)}")
    print(f"Provider   : {args.provider}  |  model: {args.openai_model if args.provider == 'openai' else args.model}")
    print(f"Mode       : {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("─" * 60)

    # In dry-run mode we skip MongoDB entirely — no connection needed
    if args.dry_run:
        mongo_client = None
        collection   = None
    else:
        mongo_client = pymongo.MongoClient(args.mongo_url)
        db           = mongo_client[args.db_name]
        collection   = db["interpretation_rules"]

    # Parse RTF into sloka blocks
    raw   = Path(args.rtf).expanduser().read_text(encoding="utf-8", errors="replace")
    plain = strip_rtf(raw)
    blocks = split_into_sloka_blocks(plain)

    # Build planet-position map (needed for multi-section chapters)
    planet_map = build_planet_position_map(plain)

    def planet_at(pos: int) -> str:
        result = dasha_lord
        for p, planet in planet_map:
            if p <= pos:
                result = planet
            else:
                break
        return result

    # Filter to target sloka blocks
    targets = [
        (label, text, pos)
        for label, text, pos in blocks
        if sloka_label_matches(label, target_slokas) and not should_skip(label, text, chapter)
    ]

    if not targets:
        print(f"ERROR: No slokas matched {target_slokas}.")
        print(f"Available: {[b[0] for b in blocks]}")
        if mongo_client:
            mongo_client.close()
        return

    if args.provider == "openai":
        extractor = OpenAISlokaExtractor(model=args.openai_model)
    else:
        extractor = SlokaExtractor(model=args.model)
    total_new   = 0
    total_skipped = 0

    # Count existing rules to generate non-colliding IDs (live mode only)
    existing_total = collection.count_documents({"source.batch_id": batch_id}) if collection is not None else 0
    id_counter = existing_total + 1

    for sloka_label, sloka_text, sloka_pos in targets:
        rule_text, notes_text = clean_notes(sloka_text)
        antardasha_planet     = planet_at(sloka_pos)

        # In dry-run: no DB lookup — treat every rule as new (dedup within run only)
        if collection is not None:
            existing_docs = list(collection.find(
                {"source.batch_id": batch_id, "source.sloka": sloka_label}
            ))
            if not existing_docs:
                existing_docs = list(collection.find(
                    {"batch_id": batch_id, "condition.sloka": sloka_label}
                ))
        else:
            existing_docs = []

        # Two separate dedup lists with different thresholds:
        #   db_summaries   — clean DB rules (60% overlap = duplicate)
        #                    EXCLUDES pre_split_merged rules — those are being superseded
        #   patch_summaries — rules added in THIS run (90% overlap = near-exact repeat only)
        # Keeping them separate prevents house-lord variants like "9th lord" vs "10th lord"
        # (75% overlap) from blocking each other mid-run, while still catching true DB dups.
        db_summaries = [
            rule_summary(d) for d in existing_docs
            if d.get("metadata", {}).get("source_note") != "pre_split_merged"
        ]
        patch_summaries: list[str] = []
        existing_count  = len(existing_docs)

        print(f"\n  Sloka {sloka_label:10s} | existing: {existing_count} | re-extracting...")

        try:
            new_rules = extractor.extract(
                sloka_label=sloka_label,
                rule_text=rule_text,
                notes_text=notes_text,
                chapter=chapter,
                dasha_lord=dasha_lord,
            )
        except Exception as e:
            print(f"    ERROR: {e}")
            continue

        sloka_new = sloka_skipped = 0

        for rule in new_rules:
            # Build rule doc using shared helper
            doc = extracted_to_rule(
                rule,
                sloka_label,
                dasha_lord,
                antardasha_planet,
                chapter,
                batch_id,
                id_counter,
            )

            new_summary = doc["interpretation"]["summary"]

            # Block if already in DB (condition-only comparison, 60% threshold)
            if is_duplicate(new_summary, db_summaries, threshold=0.60):
                sloka_skipped += 1
                continue

            # Block near-exact repeats within this run only (90% threshold)
            if is_duplicate(new_summary, patch_summaries, threshold=0.90):
                sloka_skipped += 1
                continue

            # Tag as gap-fill / split-upgrade and give unique ID
            doc["rule_id"]                 = f"R-BPHS{chapter}-PATCH-{uuid.uuid4().hex[:6].upper()}"
            doc["metadata"]["source_note"] = new_source_note
            doc["approval_status"]         = "pending_review"

            if args.dry_run:
                sub = doc["condition"]["sub_type"]
                print(f"    [DRY RUN] {doc['rule_id']} | {sub:22s} | {new_summary[:70]}...")
            else:
                collection.insert_one(doc)
                sub = doc["condition"]["sub_type"]
                print(f"    Inserted  {doc['rule_id']} | {sub:22s} | {new_summary[:70]}...")

            patch_summaries.append(new_summary)
            id_counter += 1
            sloka_new  += 1

        print(f"    Result: +{sloka_new} new  |  {sloka_skipped} skipped (duplicates)")
        total_new     += sloka_new
        total_skipped += sloka_skipped

    print(f"\n{'─' * 60}")
    if args.dry_run:
        print(f"[DRY RUN] Would insert {total_new} net-new rules  |  {total_skipped} duplicates skipped")
    else:
        print(f"✅  Inserted {total_new} net-new rules  |  {total_skipped} duplicates skipped")
        if total_new:
            print(f"    approval_status='pending_review', source_note='{new_source_note}'")
            print(f"    Review: Admin > Library > Rules Browser → batch {batch_id}")

    if mongo_client:
        mongo_client.close()


if __name__ == "__main__":
    main()
