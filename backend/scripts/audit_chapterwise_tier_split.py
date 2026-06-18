#!/usr/bin/env python3
"""
audit_chapterwise_tier_split.py
---------------------------------
Full textbook / chapter-wise breakdown of precision_tier distribution.
Shows exactly which legacy rules are active but un-retired at each tier.

Run:
  python3.12 backend/scripts/audit_chapterwise_tier_split.py
"""

from __future__ import annotations
import os, sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from pymongo import MongoClient

_root = Path(__file__).resolve().parents[2]
for _env in [_root / "backend" / ".env", _root / ".env", Path(".env")]:
    if _env.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(_env)
        except ImportError:
            pass
        break

MONGO_URL = os.environ.get("MONGO_URL")
if not MONGO_URL:
    print("ERROR: MONGO_URL not set.", flush=True)
    sys.exit(1)

LOG_DIR  = Path("KE_TEXTBOOK_DECODE/Test_Vectors/phase4_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
TS       = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
LOG_PATH = LOG_DIR / f"audit_chapterwise_tier_split_{TS}.log"

_buf: list[str] = []
def out(msg: str = "") -> None:
    print(msg, flush=True)
    _buf.append(msg)
def save_log() -> None:
    LOG_PATH.write_text("\n".join(_buf) + "\n", encoding="utf-8")
    print(f"\nLog → {LOG_PATH}", flush=True)

# Tier groups
EVALUABLE = {"L1","L2","L1_bhava","yoga_L1","dasha_L1","kp_system","L3+"}
SUPPORT   = {"L4","L5","mundane_macro"}
L0_TIERS  = {"L0_general","L0_no_condition","L0_string_malformed",
             "L0_composite_no_anchor","pending_review_l0"}
EXCLUDED  = {"engine_specification","methodology","numerology",
             "remedy_engine","transit_excluded"}
RETIRED   = {"retired_pre_l1l2"}

def group(tier: str) -> str:
    if tier in EVALUABLE: return "EVAL"
    if tier in SUPPORT:   return "SUPP"
    if tier in L0_TIERS:  return "L0"
    if tier in EXCLUDED:  return "EXCL"
    if tier in RETIRED:   return "RET"
    return "NULL"

# Book display order + labels
BOOK_ORDER = [
    ("bphs_vol1",          "BPHS Vol 1"),
    ("bphs_vol2",          "BPHS Vol 2"),
    ("300_combinations",   "300 Combinations"),
    ("lal_kitab",          "Lal Kitab"),
    ("kp",                 "KP System"),
    ("phaladeepika",       "Phaladeepika"),
    ("medical_astrology",  "Medical Astrology"),
    ("mundane_astrology",  "Mundane Astrology"),
    ("sbc",                "SBC"),
    ("numerology",         "Numerology"),
    ("remedies",           "Remedies"),
]


def main() -> None:
    out(f"audit_chapterwise_tier_split.py")
    out(f"Log → {LOG_PATH}")
    out(f"Started: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    out()

    client = MongoClient(MONGO_URL)
    coll   = client["horoscope_db"]["interpretation_rules"]
    _      = coll.count_documents({})
    out("Connected ✓")
    out()

    # ── Aggregate by book × chapter × tier × active ────────────────────────
    pipeline = [
        {"$group": {
            "_id": {
                "book":    "$source.book",
                "chapter": "$source.chapter",
                "tier":    "$metadata.precision_tier",
                "active":  "$active",
                "status":  "$approval_status",
            },
            "count": {"$sum": 1},
        }},
        {"$sort": {"_id.book": 1, "_id.chapter": 1, "_id.tier": 1}},
    ]
    rows = list(coll.aggregate(pipeline))

    # ── Organise into nested dict: book → chapter → tier → {active, inactive}
    # Structure: data[book][chapter][tier][active_bool] = count
    data: dict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {"active": 0, "inactive": 0, "aa": 0, "phr": 0, "flagged": 0})))

    all_books   = set()
    all_chapters: dict[str, set] = defaultdict(set)

    for row in rows:
        b   = row["_id"].get("book") or "(unknown)"
        ch  = row["_id"].get("chapter") or 0
        t   = row["_id"].get("tier") or "(null)"
        act = row["_id"].get("active", False)
        st  = row["_id"].get("status") or ""
        n   = row["count"]

        all_books.add(b)
        all_chapters[b].add(ch)

        slot = data[b][ch][t]
        if act:
            slot["active"] += n
            if st == "auto_approved":          slot["aa"]      += n
            elif st == "pending_human_review": slot["phr"]     += n
            elif st == "flagged":              slot["flagged"] += n
        else:
            slot["inactive"] += n

    # ── SECTION 1: Book × chapter summary table ────────────────────────────
    out("=" * 100)
    out("SECTION 1: BOOK × CHAPTER TIER SUMMARY (active rules only)")
    out("=" * 100)
    out(f"{'Book':<22} {'Ch':>4}  {'EVAL':>6}  {'SUPP':>6}  {'L0':>6}  {'EXCL':>6}  {'NULL':>6}  {'RET':>4}  {'TOTAL':>6}  Notes")
    out("-" * 100)

    grand = defaultdict(int)

    def print_book(book_key: str, book_label: str) -> None:
        def _ch_key(x):
            if x is None:
                return (1, 0, "")
            try:
                return (0, int(x), "")
            except (ValueError, TypeError):
                return (0, 0, str(x))
        chapters = sorted(all_chapters.get(book_key, []), key=_ch_key)
        if not chapters:
            return
        book_totals = defaultdict(int)
        for ch in chapters:
            ch_tiers = data[book_key][ch]
            buckets  = defaultdict(int)
            for tier, slot in ch_tiers.items():
                g = group(tier)
                buckets[g] += slot["active"]
                book_totals[g] += slot["active"]
                grand[g] += slot["active"]
            total = sum(buckets.values())
            if total == 0:
                continue
            # Build notes for L0 active rules
            notes_parts = []
            for tier, slot in ch_tiers.items():
                if tier in L0_TIERS and slot["active"] > 0:
                    notes_parts.append(f"{tier}×{slot['active']}")
            notes = ", ".join(notes_parts) if notes_parts else ""
            ch_display = str(ch) if ch else "--"
            out(f"  {book_label:<20} {ch_display:>4}  {buckets['EVAL']:>6}  {buckets['SUPP']:>6}  {buckets['L0']:>6}  {buckets['EXCL']:>6}  {buckets['NULL']:>6}  {buckets['RET']:>4}  {total:>6}  {notes}")
        # Book subtotal
        bt = sum(book_totals.values())
        out(f"  {'  └─ '+book_label+' TOTAL':<20} {'':>4}  {book_totals['EVAL']:>6}  {book_totals['SUPP']:>6}  {book_totals['L0']:>6}  {book_totals['EXCL']:>6}  {book_totals['NULL']:>6}  {book_totals['RET']:>4}  {bt:>6}")
        out()

    for bk, bl in BOOK_ORDER:
        print_book(bk, bl)

    # Unknown books
    known = {b for b, _ in BOOK_ORDER}
    for b in sorted(all_books - known):
        print_book(b, b[:22])

    out("-" * 100)
    gt = sum(grand.values())
    out(f"  {'GRAND TOTAL':<26}  {grand['EVAL']:>6}  {grand['SUPP']:>6}  {grand['L0']:>6}  {grand['EXCL']:>6}  {grand['NULL']:>6}  {grand['RET']:>4}  {gt:>6}")
    out()

    # ── SECTION 2: Legacy L0 rules still active -- retirement candidates ────
    out("=" * 100)
    out("SECTION 2: ACTIVE L0 / LEGACY RULES -- RETIREMENT CANDIDATES")
    out("=" * 100)
    out("These are active rules with no evaluable condition anchor. They fire broadly and")
    out("dilute Layer C scores. Each is a retirement or restructuring candidate.")
    out()

    l0_pipeline = [
        {"$match": {
            "active": True,
            "metadata.precision_tier": {"$in": list(L0_TIERS)},
        }},
        {"$group": {
            "_id": {
                "book":    "$source.book",
                "chapter": "$source.chapter",
                "tier":    "$metadata.precision_tier",
                "status":  "$approval_status",
            },
            "count": {"$sum": 1},
            "sample_ids": {"$push": "$rule_id"},
        }},
        {"$sort": {"_id.tier": 1, "_id.book": 1, "_id.chapter": 1}},
    ]
    l0_rows = list(coll.aggregate(l0_pipeline))

    cur_tier = None
    l0_grand = 0
    for row in l0_rows:
        tier  = row["_id"].get("tier") or "(null)"
        book  = row["_id"].get("book") or "(unknown)"
        ch    = row["_id"].get("chapter") or "?"
        st    = row["_id"].get("status") or ""
        n     = row["count"]
        sids  = row.get("sample_ids", [])[:3]
        l0_grand += n
        if tier != cur_tier:
            out(f"  ── {tier} ──")
            cur_tier = tier
        sample = ", ".join(str(s) for s in sids if s)
        out(f"    {book:<25} ch={str(ch):<4}  [{st:<22}]  count={n:>4}  e.g. {sample[:60]}")

    out()
    out(f"  TOTAL active L0 rules: {l0_grand}")
    out()

    # ── SECTION 3: Active NULL-tier rules (blank rule_id) ─────────────────
    out("=" * 100)
    out("SECTION 3: ACTIVE NULL-TIER RULES (precision_tier missing)")
    out("=" * 100)
    null_pipeline = [
        {"$match": {
            "active": True,
            "$or": [
                {"metadata.precision_tier": {"$exists": False}},
                {"metadata.precision_tier": None},
                {"metadata.precision_tier": ""},
            ],
        }},
        {"$group": {
            "_id": {
                "book":    "$source.book",
                "chapter": "$source.chapter",
                "status":  "$approval_status",
            },
            "count": {"$sum": 1},
        }},
        {"$sort": {"_id.book": 1, "_id.chapter": 1}},
    ]
    null_rows = list(coll.aggregate(null_pipeline))
    null_grand = 0
    for row in null_rows:
        book = row["_id"].get("book") or "(unknown)"
        ch   = row["_id"].get("chapter") or "?"
        st   = row["_id"].get("status") or ""
        n    = row["count"]
        null_grand += n
        out(f"    {book:<25} ch={str(ch):<4}  [{st:<22}]  count={n:>4}")
    out()
    out(f"  TOTAL active null-tier rules: {null_grand}  (these have blank rule_id -- cannot be ID'd)")
    out()

    # ── SECTION 4: Book-level retirement summary ───────────────────────────
    out("=" * 100)
    out("SECTION 4: RETIREMENT ASSESSMENT BY BOOK")
    out("=" * 100)
    out(f"{'Book':<25}  {'Evaluable':>10}  {'Legacy L0 Active':>17}  {'Null-tier':>10}  {'Action'}")
    out("-" * 90)

    retire_pipeline = [
        {"$match": {"active": True}},
        {"$group": {
            "_id": {
                "book":  "$source.book",
                "group": {
                    "$switch": {
                        "branches": [
                            {"case": {"$in": ["$metadata.precision_tier", list(EVALUABLE)]}, "then": "EVAL"},
                            {"case": {"$in": ["$metadata.precision_tier", list(L0_TIERS)]},  "then": "L0"},
                        ],
                        "default": "OTHER"
                    }
                }
            },
            "count": {"$sum": 1},
        }},
        {"$sort": {"_id.book": 1}},
    ]
    retire_rows = list(coll.aggregate(retire_pipeline))
    book_data: dict[str, dict[str, int]] = defaultdict(lambda: {"EVAL": 0, "L0": 0, "OTHER": 0})
    for row in retire_rows:
        b = row["_id"].get("book") or "(unknown)"
        g = row["_id"].get("group", "OTHER")
        book_data[b][g] += row["count"]

    for b in sorted(book_data.keys()):
        ev = book_data[b]["EVAL"]
        l0 = book_data[b]["L0"]
        ot = book_data[b]["OTHER"]
        action = ""
        if l0 > 0 and ev > 0:
            action = f"⚠ Retire {l0} L0 rules -- superseded by {ev} evaluable"
        elif l0 > 0 and ev == 0:
            action = f"⚠ Review {l0} L0 rules -- no evaluable counterpart yet"
        elif l0 == 0:
            action = "✓ Clean"
        out(f"  {b:<25}  {ev:>10,}  {l0:>17,}  {ot:>10,}  {action}")
    out()

    client.close()
    save_log()


if __name__ == "__main__":
    main()
