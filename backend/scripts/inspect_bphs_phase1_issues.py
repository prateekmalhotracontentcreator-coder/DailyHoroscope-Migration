#!/usr/bin/env python3
"""
inspect_bphs_phase1_issues.py
Read-only inspection of all 5 BPHS Vol 1 Phase 1 open issues.
Run this FIRST before any patch scripts.
"""
import argparse
import os
from pymongo import MongoClient

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    parser.add_argument("--db-name", default="horoscope_db")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col = client[args.db_name]["interpretation_rules"]

    print("\n" + "="*60)
    print("BPHS VOL 1 -- PHASE 1 ISSUE INSPECTION")
    print("="*60)

    # ── ISSUE 1: Contradiction holds ──────────────────────────────
    print("\n── ISSUE 1: Contradiction Pairs (should be 13) ──")
    # Try top-level approval_status first
    c1 = list(col.find(
        {"approval_status": "contradiction_hold"},
        {"_id": 0, "rule_id": 1, "approval_status": 1,
         "source_chapter": 1, "source": 1, "batch_id": 1}
    ))
    # Also try nested
    c1b = list(col.find(
        {"validation.approval_status": "contradiction_hold"},
        {"_id": 0, "rule_id": 1, "validation.approval_status": 1,
         "source_chapter": 1, "source": 1, "batch_id": 1}
    ))
    all_contra = {r.get("rule_id"): r for r in c1 + c1b}
    print(f"  Found: {len(all_contra)} rules in contradiction_hold")
    for rid, r in sorted(all_contra.items()):
        ch = r.get("source_chapter") or r.get("source", {}).get("chapter", "?")
        print(f"  • {rid}  chapter={ch}")

    # ── ISSUE 2: Ch15 pending_human_review ────────────────────────
    print("\n── ISSUE 2: Ch15 pending_human_review ──")
    ch15_phr = col.count_documents({
        "$or": [
            {"source_chapter": {"$regex": "ch.?15", "$options": "i"},
             "approval_status": "pending_human_review"},
            {"source.chapter": 15, "approval_status": "pending_human_review"},
        ]
    })
    ch15_total = col.count_documents({
        "$or": [
            {"source_chapter": {"$regex": "ch.?15", "$options": "i"}},
            {"source.chapter": 15},
        ]
    })
    print(f"  Ch15 PHR: {ch15_phr} / {ch15_total} total rules")
    auto = ch15_total - ch15_phr
    rate = round(auto/ch15_total*100) if ch15_total else 0
    print(f"  Auto-approve rate: {rate}%  (expected ~25%)")

    # ── ISSUE 3: Ch19 pending_human_review ────────────────────────
    print("\n── ISSUE 3: Ch19 pending_human_review ──")
    ch19_phr = col.count_documents({
        "$or": [
            {"source_chapter": {"$regex": "ch.?19", "$options": "i"},
             "approval_status": "pending_human_review"},
            {"source.chapter": 19, "approval_status": "pending_human_review"},
        ]
    })
    ch19_total = col.count_documents({
        "$or": [
            {"source_chapter": {"$regex": "ch.?19", "$options": "i"}},
            {"source.chapter": 19},
        ]
    })
    print(f"  Ch19 PHR: {ch19_phr} / {ch19_total} total rules")
    auto19 = ch19_total - ch19_phr
    rate19 = round(auto19/ch19_total*100) if ch19_total else 0
    print(f"  Auto-approve rate: {rate19}%  (expected ~33%)")

    # ── ISSUE 4: Ch34 flagged rules ───────────────────────────────
    print("\n── ISSUE 4: Ch34 Flagged Rules (should be 15) ──")
    ch34_flagged = list(col.find(
        {"$or": [
            {"source_chapter": {"$regex": "ch.?34", "$options": "i"},
             "approval_status": "flagged"},
            {"source.chapter": 34, "approval_status": "flagged"},
        ]},
        {"_id": 0, "rule_id": 1, "approval_status": 1,
         "validation": 1, "source_chapter": 1}
    ))
    print(f"  Found: {len(ch34_flagged)} flagged rules in Ch34")
    for r in ch34_flagged:
        flag_reason = ""
        if isinstance(r.get("validation"), dict):
            flag_reason = r["validation"].get("flag_reason", "")[:80]
        print(f"  • {r.get('rule_id')}  flag='{flag_reason}'")

    # ── ISSUE 5: yoga_check audit Ch35-42 ─────────────────────────
    # yoga_check lives at condition.yoga_check (NOT validation.yoga_check)
    # metadata.yoga_checkable and interpretation.tags also carry checkability signals
    print("\n── ISSUE 5: yoga_check Status Ch35-42 ──")
    for ch in range(35, 43):
        total = col.count_documents({
            "$or": [
                {"source_chapter": {"$regex": f"ch.?{ch}\\b", "$options": "i"}},
                {"source.chapter": ch},
            ]
        })
        # Primary field: condition.yoga_check (rich structured object set by yoga checker)
        has_yoga_check = col.count_documents({
            "$or": [
                {"source_chapter": {"$regex": f"ch.?{ch}\\b", "$options": "i"},
                 "condition.yoga_check": {"$exists": True, "$ne": None}},
                {"source.chapter": ch,
                 "condition.yoga_check": {"$exists": True, "$ne": None}},
            ]
        })
        # Cross-check: metadata.yoga_checkable flag
        meta_checkable = col.count_documents({
            "$or": [
                {"source_chapter": {"$regex": f"ch.?{ch}\\b", "$options": "i"},
                 "metadata.yoga_checkable": True},
                {"source.chapter": ch,
                 "metadata.yoga_checkable": True},
            ]
        })
        print(f"  Ch{ch}: {total} total | condition.yoga_check set: {has_yoga_check} | metadata.yoga_checkable=True: {meta_checkable}")

    # ── Summary ───────────────────────────────────────────────────
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"  Contradiction holds : {len(all_contra)}")
    print(f"  Ch15 PHR            : {ch15_phr}")
    print(f"  Ch19 PHR            : {ch19_phr}")
    print(f"  Ch34 flagged        : {len(ch34_flagged)}")
    print(f"  yoga_check gap      : see per-chapter above")
    print("\nPaste full output back to Claude before running patch scripts.\n")

    client.close()

if __name__ == "__main__":
    main()
