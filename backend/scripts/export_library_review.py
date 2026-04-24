#!/usr/bin/env python3
"""
Export scripts for co-founder review session.

Generates three CSV files:
  1. everydayhoroscope_source_breakdown.csv  — chapter/source map for EverydayHoroscope
  2. everydayhoroscope_all_rules.csv         — all EverydayHoroscope rules for bucketization
  3. horoscope_db_contradictions.csv         — all contradiction pairs from horoscope_db

Usage:
  python3 backend/scripts/export_library_review.py \
    --mongo-url "mongodb+srv://user:pass@host/" \
    --output-dir backend/scripts/reports/
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from pymongo import MongoClient


def parse_args():
    parser = argparse.ArgumentParser(description="Export Knowledge Engine rules for co-founder review")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--output-dir", default="backend/scripts/reports/")
    return parser.parse_args()


def export_everydayhoroscope_breakdown(db, output_dir: Path):
    """Source/chapter breakdown with rule counts and status split."""
    print("\n[1/3] EverydayHoroscope — source breakdown...")

    groups: dict[str, dict] = defaultdict(lambda: {
        "book": "", "chapter": "", "batch_ids": set(),
        "auto_approved": 0, "flagged": 0, "pending_human_review": 0,
        "rejected": 0, "total": 0
    })

    for rule in db["interpretation_rules"].find({}, {
        "source": 1, "approval_status": 1, "_id": 0
    }):
        src = rule.get("source") or {}
        book = src.get("primary", "Unknown")
        chapter = src.get("chapter", "Unknown")
        batch = src.get("batch_id", "Unknown")
        status = rule.get("approval_status", "unknown")
        key = f"{book}||{chapter}"
        groups[key]["book"] = book
        groups[key]["chapter"] = chapter
        groups[key]["batch_ids"].add(batch)
        groups[key]["total"] += 1
        if status in groups[key]:
            groups[key][status] += 1

    path = output_dir / "everydayhoroscope_source_breakdown.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "book", "chapter", "batch_ids",
            "total", "auto_approved", "flagged",
            "pending_human_review", "rejected", "flag_rate_%"
        ])
        for g in sorted(groups.values(), key=lambda x: (-x["total"], x["book"])):
            flag_rate = round(g["flagged"] / g["total"] * 100) if g["total"] else 0
            writer.writerow([
                g["book"], g["chapter"],
                " | ".join(sorted(g["batch_ids"])),
                g["total"], g["auto_approved"], g["flagged"],
                g["pending_human_review"], g["rejected"], f"{flag_rate}%"
            ])

    print(f"  Written: {path}  ({len(groups)} chapter groups)")
    return groups


def export_everydayhoroscope_rules(db, output_dir: Path):
    """Full rule export for EverydayHoroscope — all statuses."""
    print("\n[2/3] EverydayHoroscope — full rule export...")

    path = output_dir / "everydayhoroscope_all_rules.csv"
    count = 0

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "rule_id", "approval_status", "book", "chapter", "batch_id",
            "condition_type", "planet", "house", "sign",
            "interpretation_summary", "flag_reason", "verdict"
        ])

        for rule in db["interpretation_rules"].find({}, {
            "rule_id": 1, "approval_status": 1, "source": 1,
            "condition": 1, "interpretation": 1, "validation": 1, "_id": 0
        }).sort("source.primary", 1):
            src = rule.get("source") or {}
            cond = rule.get("condition") or {}
            interp = rule.get("interpretation") or {}
            val = rule.get("validation") or {}

            passages = interp.get("full_text_passages") or []
            summary = passages[0].get("text", "")[:200] if passages else ""

            writer.writerow([
                rule.get("rule_id", ""),
                rule.get("approval_status", ""),
                src.get("primary", ""),
                src.get("chapter", ""),
                src.get("batch_id", ""),
                cond.get("type", ""),
                cond.get("planet", ""),
                cond.get("house", ""),
                cond.get("sign", ""),
                summary,
                val.get("flag_reason", ""),
                val.get("verdict", "")
            ])
            count += 1

    print(f"  Written: {path}  ({count} rules)")


def export_contradictions(db, output_dir: Path):
    """Export all contradiction pairs from horoscope_db."""
    print("\n[3/3] horoscope_db — contradiction pairs export...")

    # Find rules with contradiction_ids populated
    path = output_dir / "horoscope_db_contradictions.csv"
    count = 0
    pairs_seen: set[frozenset] = set()

    # Build a lookup of rule_id → rule
    print("  Loading rule index...")
    rule_index: dict[str, dict] = {}
    for rule in db["interpretation_rules"].find(
        {"validation.contradiction_ids": {"$exists": True, "$ne": []}},
        {"rule_id": 1, "approval_status": 1, "source": 1, "condition": 1,
         "interpretation": 1, "validation": 1, "_id": 0}
    ):
        rule_index[rule["rule_id"]] = rule

    print(f"  Found {len(rule_index)} rules involved in contradictions")

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "pair_id",
            "rule_id_a", "status_a", "book_a", "chapter_a", "condition_a", "planet_a", "house_a",
            "interpretation_a",
            "rule_id_b", "status_b", "book_b", "chapter_b", "condition_b", "planet_b", "house_b",
            "interpretation_b",
            "contradiction_summary",
            "recommended_action"
        ])

        for rule_id_a, rule_a in rule_index.items():
            val_a = rule_a.get("validation") or {}
            for rule_id_b in (val_a.get("contradiction_ids") or []):
                pair_key = frozenset([rule_id_a, rule_id_b])
                if pair_key in pairs_seen:
                    continue
                pairs_seen.add(pair_key)

                rule_b = rule_index.get(rule_id_b, {})
                src_a = rule_a.get("source") or {}
                src_b = rule_b.get("source") or {}
                cond_a = rule_a.get("condition") or {}
                cond_b = rule_b.get("condition") or {}
                interp_a = rule_a.get("interpretation") or {}
                interp_b = rule_b.get("interpretation") or {}
                passages_a = interp_a.get("full_text_passages") or []
                passages_b = interp_b.get("full_text_passages") or []
                text_a = passages_a[0].get("text", "")[:300] if passages_a else ""
                text_b = passages_b[0].get("text", "")[:300] if passages_b else ""
                val_b = rule_b.get("validation") or {}
                summary = val_a.get("contradiction_summary") or val_b.get("contradiction_summary") or ""

                count += 1
                writer.writerow([
                    f"pair-{count:03d}",
                    rule_id_a,
                    rule_a.get("approval_status", ""),
                    src_a.get("primary", ""),
                    src_a.get("chapter", ""),
                    cond_a.get("type", ""),
                    cond_a.get("planet", ""),
                    cond_a.get("house", ""),
                    text_a,
                    rule_id_b,
                    rule_b.get("approval_status", ""),
                    src_b.get("primary", ""),
                    src_b.get("chapter", ""),
                    cond_b.get("type", ""),
                    cond_b.get("planet", ""),
                    cond_b.get("house", ""),
                    text_b,
                    summary,
                    ""  # recommended_action — blank for co-founder to fill
                ])

    print(f"  Written: {path}  ({count} unique pairs)")


def main():
    args = parse_args()
    client = MongoClient(args.mongo_url)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        print(f"\nConnected. Output dir: {output_dir.resolve()}")

        # EverydayHoroscope exports
        db_eh = client["EverydayHoroscope"]
        export_everydayhoroscope_breakdown(db_eh, output_dir)
        export_everydayhoroscope_rules(db_eh, output_dir)

        # horoscope_db contradiction export
        db_hdb = client["horoscope_db"]
        export_contradictions(db_hdb, output_dir)

        print(f"\n{'='*55}")
        print("EXPORT COMPLETE")
        print(f"  {output_dir}/everydayhoroscope_source_breakdown.csv")
        print(f"  {output_dir}/everydayhoroscope_all_rules.csv")
        print(f"  {output_dir}/horoscope_db_contradictions.csv")
        print(f"\nOpen in Excel / Numbers / Google Sheets for review.")

    finally:
        client.close()


if __name__ == "__main__":
    main()
