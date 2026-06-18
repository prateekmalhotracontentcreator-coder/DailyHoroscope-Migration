#!/usr/bin/env python3
"""
deactivate_l0_legacy_pre_layer_c.py
--------------------------------------
KE-OP-40 PRE-RUN: Deactivate L0 rules that are in the Layer C corpus (AA or PHR)
and have no evaluable condition anchor.

These are structurally broken rules -- they fire on every chart (L0_no_condition)
or fire broadly with no natal anchor (L0_general, L0_composite_no_anchor with AA/PHR).
They contaminate Layer C Run 4 scoring.

Target: active=True + tier in {L0_no_condition, L0_general, L0_composite_no_anchor}
        + approval_status in {auto_approved, pending_human_review}

DOES NOT touch:
  - pending_review_l0  (formally bucketized, KE-OP-40 hold)
  - flagged / rejected / deprecated L0 rules (already excluded from Layer C corpus)

Run:
  python3.12 backend/scripts/deactivate_l0_legacy_pre_layer_c.py [--live]
"""

from __future__ import annotations
import os, sys, argparse
from datetime import datetime, timezone
from pathlib import Path
from pymongo import MongoClient, UpdateMany

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

_buf: list[str] = []
def out(msg: str = "") -> None:
    print(msg, flush=True)
    _buf.append(msg)

TARGET_TIERS = ["L0_no_condition", "L0_general", "L0_composite_no_anchor"]
TARGET_STATUSES = ["auto_approved", "pending_human_review"]

QUERY = {
    "active": True,
    "metadata.precision_tier": {"$in": TARGET_TIERS},
    "approval_status": {"$in": TARGET_STATUSES},
}


def main(live: bool) -> None:
    LOG_PATH = LOG_DIR / f"deactivate_l0_legacy_pre_layer_c_{TS}.log"
    out(f"deactivate_l0_legacy_pre_layer_c.py  LIVE={live}")
    out(f"Log → {LOG_PATH}")
    out(f"Started: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    out()

    client = MongoClient(MONGO_URL)
    coll   = client["horoscope_db"]["interpretation_rules"]
    _      = coll.count_documents({})
    out("Connected ✓")
    out()

    # ── Dry-run breakdown ──────────────────────────────────────────────────
    out("TARGET QUERY:")
    out(f"  precision_tier  ∈ {TARGET_TIERS}")
    out(f"  approval_status ∈ {TARGET_STATUSES}")
    out(f"  active           = True")
    out()

    from pymongo import ASCENDING
    breakdown = list(coll.aggregate([
        {"$match": QUERY},
        {"$group": {
            "_id": {
                "book":    "$source.book",
                "tier":    "$metadata.precision_tier",
                "status":  "$approval_status",
            },
            "count": {"$sum": 1},
            "sample_ids": {"$push": "$rule_id"},
        }},
        {"$sort": {"_id.tier": 1, "_id.book": 1}},
    ]))

    total = sum(r["count"] for r in breakdown)
    out(f"Targeted rules: {total}")
    out()

    cur_tier = None
    tier_totals: dict[str, int] = {}
    for row in breakdown:
        tier   = row["_id"].get("tier") or "?"
        book   = row["_id"].get("book") or "(unknown)"
        status = row["_id"].get("status") or ""
        n      = row["count"]
        sids   = row.get("sample_ids", [])[:3]
        tier_totals[tier] = tier_totals.get(tier, 0) + n
        if tier != cur_tier:
            out(f"  ── {tier} ──")
            cur_tier = tier
        sample = ", ".join(str(s) for s in sids if s)[:70]
        out(f"    {book[:30]:<30}  [{status:<22}]  count={n:>4}  e.g. {sample}")

    out()
    out("Tier subtotals:")
    for t, n in tier_totals.items():
        out(f"  {t:<35}  {n:>4}")
    out(f"  {'TOTAL':<35}  {total:>4}")
    out()

    if total == 0:
        out("Nothing to deactivate. Exiting.")
        client.close()
        LOG_PATH.write_text("\n".join(_buf) + "\n", encoding="utf-8")
        return

    if not live:
        out("DRY RUN -- pass --live to apply.")
        client.close()
        LOG_PATH.write_text("\n".join(_buf) + "\n", encoding="utf-8")
        print(f"\nLog → {LOG_PATH}", flush=True)
        return

    # ── Live update ────────────────────────────────────────────────────────
    now_str = datetime.now(timezone.utc).isoformat()
    result = coll.update_many(
        QUERY,
        {"$set": {
            "active":                  False,
            "metadata.deactivated_at": now_str,
            "metadata.deactivation_reason": "l0_legacy_pre_layer_c_ke_op_40",
        }},
    )

    out(f"bulk update matched:  {result.matched_count}")
    out(f"bulk update modified: {result.modified_count}")
    out()
    out("Done. Run audit_precision_tier_distribution.py to verify updated corpus.")
    out()
    out("Impact:")
    out("  Layer C corpus (AA + PHR evaluable): was 12,831 → should drop by these deactivated rules")
    out("  Quality: L0_no_condition rules NO LONGER fire on every test vector")

    client.close()
    LOG_PATH.write_text("\n".join(_buf) + "\n", encoding="utf-8")
    print(f"\nLog → {LOG_PATH}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    main(live=args.live)
