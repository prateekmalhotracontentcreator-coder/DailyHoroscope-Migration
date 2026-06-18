#!/usr/bin/env python3
"""
inspect_bphs1_ch45_avastha.py
-------------------------------
KE-OP-40 prep: inspect all BPHS Vol 1 Ch45 L0_no_condition rules so we can
manually review their content and design proper avastha conditions to encode.

Run:
  python3.12 backend/scripts/inspect_bphs1_ch45_avastha.py
"""

from __future__ import annotations
import os, sys
from pathlib import Path
from datetime import datetime, timezone
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

LOG_DIR = Path("KE_TEXTBOOK_DECODE/Test_Vectors/phase4_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
TS = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
LOG_PATH = LOG_DIR / f"inspect_bphs1_ch45_avastha_{TS}.log"

_buf: list[str] = []
def out(msg: str = "") -> None:
    print(msg, flush=True)
    _buf.append(msg)


def main() -> None:
    out("inspect_bphs1_ch45_avastha.py")
    out(f"Log → {LOG_PATH}")
    out(f"Started: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    out()

    client = MongoClient(MONGO_URL)
    coll   = client["horoscope_db"]["interpretation_rules"]
    out("Connected ✓")
    out()

    # ── All bphs1-ch45 rules (both L0_no_condition and evaluable) ─────────
    all_ch45 = list(coll.find(
        {"rule_id": {"$regex": "^bphs1-ch45-"}},
        {"rule_id": 1, "active": 1, "approval_status": 1,
         "metadata.precision_tier": 1, "metadata.claim_axis": 1,
         "condition": 1, "interpretation": 1, "description": 1,
         "source": 1, "_id": 0}
    ).sort("rule_id", 1))

    out(f"Total bphs1-ch45-* rules in DB: {len(all_ch45)}")
    out()

    l0_rules  = [r for r in all_ch45 if r.get("metadata", {}).get("precision_tier") == "L0_no_condition"]
    eval_rules = [r for r in all_ch45 if r.get("metadata", {}).get("precision_tier") not in
                  ("L0_no_condition", "L0_general", "L0_composite_no_anchor",
                   "pending_review_l0", "L0_string_malformed")]

    out(f"L0_no_condition: {len(l0_rules)}")
    out(f"Evaluable (L1/L2/etc): {len(eval_rules)}")
    out()

    # ── Section 1: Full detail on L0_no_condition rules ───────────────────
    out("=" * 100)
    out("SECTION 1: L0_NO_CONDITION RULES -- FULL CONTENT")
    out("=" * 100)
    out()

    for i, r in enumerate(l0_rules, 1):
        rid   = r.get("rule_id", "?")
        tier  = r.get("metadata", {}).get("precision_tier", "?")
        axis  = r.get("metadata", {}).get("claim_axis", "?")
        stat  = r.get("approval_status", "?")
        active = r.get("active", "?")
        cond  = r.get("condition", {}) or {}
        interp = r.get("interpretation", "") or r.get("description", "") or ""
        src    = r.get("source", {}) or {}

        out(f"── [{i:02d}] {rid} ──────────────────────────────────────────────────────────")
        out(f"  tier:           {tier}")
        out(f"  claim_axis:     {axis}")
        out(f"  approval_status:{stat}")
        out(f"  active:         {active}")
        out(f"  source.chapter: {src.get('chapter','?')} | source.book: {src.get('book','?')}")
        out()
        # Condition detail
        out(f"  CONDITION:")
        if not cond:
            out("    (empty -- fires unconditionally)")
        else:
            for k, v in cond.items():
                out(f"    {k}: {v}")
        out()
        # Interpretation text
        out(f"  INTERPRETATION:")
        if interp:
            for line in str(interp)[:600].split("\n"):
                out(f"    {line}")
        else:
            out("    (no interpretation text)")
        out()

    # ── Section 2: Tier breakdown of ALL ch45 rules ───────────────────────
    out("=" * 100)
    out("SECTION 2: TIER DISTRIBUTION -- ALL BPHS1-CH45 RULES")
    out("=" * 100)
    out()

    from collections import Counter
    tier_counts = Counter(r.get("metadata", {}).get("precision_tier") for r in all_ch45)
    for tier, n in sorted(tier_counts.items(), key=lambda x: x[0] or ""):
        out(f"  {(tier or '(null)'):<40}  {n:>4}")
    out()

    # ── Section 3: Evaluable rules -- what conditions exist ────────────────
    out("=" * 100)
    out("SECTION 3: EVALUABLE RULES -- CONDITION TYPES PRESENT")
    out("=" * 100)
    out()

    cond_keys = Counter()
    for r in eval_rules:
        cond = r.get("condition", {}) or {}
        for k in cond.keys():
            cond_keys[k] += 1

    out(f"Distinct condition keys across {len(eval_rules)} evaluable rules:")
    for k, n in cond_keys.most_common(30):
        out(f"  {k:<45}  {n:>4}")
    out()

    # Sample a few evaluable rules for comparison
    out("Sample evaluable rules (first 5):")
    out()
    for r in eval_rules[:5]:
        rid   = r.get("rule_id", "?")
        tier  = r.get("metadata", {}).get("precision_tier", "?")
        axis  = r.get("metadata", {}).get("claim_axis", "?")
        cond  = r.get("condition", {}) or {}
        interp = r.get("interpretation", "") or r.get("description", "") or ""
        out(f"  [{rid}]  tier={tier}  axis={axis}")
        out(f"    condition keys: {list(cond.keys())}")
        out(f"    text: {str(interp)[:200]}")
        out()

    client.close()
    LOG_PATH.write_text("\n".join(_buf) + "\n", encoding="utf-8")
    out(f"\nLog → {LOG_PATH}")


if __name__ == "__main__":
    main()
