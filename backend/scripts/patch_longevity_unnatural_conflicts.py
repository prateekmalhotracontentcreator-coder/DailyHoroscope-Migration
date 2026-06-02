#!/usr/bin/env python3
"""patch_longevity_unnatural_conflicts.py

Reads the positional conflict dedup report for Longevity Unnatural and applies
targeted MongoDB patches.

Triage logic
-----------
  self_match               → SKIP (stale export dir artifact)
  positional_polarity_conflict → PATCH: pending_review=True + note
  positional_alternate_result  → REVIEW-ONLY: logged, no DB write
  TF-IDF matches           → PATCH: pending_review=True + similarity_note
  contradiction pairs      → PATCH: pending_review=True + contradiction_note

Usage:
  python3 backend/scripts/patch_longevity_unnatural_conflicts.py \\
    --mongo-url "$MONGO_URL" \\
    --dry-run

  python3 backend/scripts/patch_longevity_unnatural_conflicts.py \\
    --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BATCH_ID    = "longevity_unnatural_v1"
REPORT_PATH = Path(
    "KE_TEXTBOOK_DECODE/Dedup_Reports/"
    "dedup_longevity_unnatural_vs_mongodb_positional.json"
)


def load_report() -> dict:
    if not REPORT_PATH.exists():
        print(f"[error] Report not found: {REPORT_PATH}", file=sys.stderr)
        print("Run retroactive_dedup_longevity_unnatural.sh first.", file=sys.stderr)
        sys.exit(1)
    return json.loads(REPORT_PATH.read_text(encoding="utf-8"))


def triage(data: dict) -> tuple[list, list, list, list, list]:
    """Return (self_matches, polarity_conflicts, alt_results, sim_matches, contras)."""
    details    = data.get("positional_conflicts_detail", [])
    matches    = data.get("matches", [])
    contras    = data.get("contradictions", [])

    self_matches      = [d for d in details if d["rule_a_id"] == d["rule_b_id"]]
    polarity_conflicts = [
        d for d in details
        if d["rule_a_id"] != d["rule_b_id"]
        and d.get("relationship") == "positional_polarity_conflict"
    ]
    alt_results = [
        d for d in details
        if d["rule_a_id"] != d["rule_b_id"]
        and d.get("relationship") == "positional_alternate_result"
    ]
    return self_matches, polarity_conflicts, alt_results, matches, contras


def build_patches(
    polarity_conflicts: list,
    sim_matches: list,
    contras: list,
) -> dict[str, list[str]]:
    patches: dict[str, list[str]] = {}

    for c in polarity_conflicts:
        rule_id = c["rule_a_id"]
        note = (
            f"positional_polarity_conflict vs {c['rule_b_id']} "
            f"on {c['positional_key']} "
            f"(A={c.get('rule_a_polarity','?')}, B={c.get('rule_b_polarity','?')})"
        )
        patches.setdefault(rule_id, []).append(note)

    for m in sim_matches:
        rule_id = m.get("rule_a_id")
        if rule_id:
            note = (
                f"similarity_match vs {m.get('rule_b_id','?')} "
                f"score={m.get('similarity_score',0):.3f}"
            )
            patches.setdefault(rule_id, []).append(note)

    for c in contras:
        rule_id = c.get("rule_a_id")
        if rule_id:
            note = (
                f"contradiction vs {c.get('rule_b_id','?')} "
                f"score={c.get('similarity_score',0):.3f} "
                f"(A={c.get('rule_a_polarity','?')}, B={c.get('rule_b_polarity','?')})"
            )
            patches.setdefault(rule_id, []).append(note)

    return patches


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Patch Longevity Unnatural positional conflicts in MongoDB."
    )
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    data = load_report()
    self_matches, polarity_conflicts, alt_results, sim_matches, contras = triage(data)

    total = len(self_matches) + len(polarity_conflicts) + len(alt_results)
    print(f"Positional conflicts in report  : {total}")
    print(f"  self-match artifacts (SKIP)   : {len(self_matches)}")
    print(f"  polarity_conflict (PATCH)     : {len(polarity_conflicts)}")
    print(f"  alternate_result (REVIEW)     : {len(alt_results)}")
    print(f"TF-IDF similarity matches       : {len(sim_matches)}")
    print(f"Contradiction pairs             : {len(contras)}")
    print()

    patches = build_patches(polarity_conflicts, sim_matches, contras)

    if not patches:
        print("No genuine conflicts -- no MongoDB patches required.")
        print("Longevity Unnatural: CLEAN ✅")
        return

    if args.dry_run:
        print("[DRY RUN] The following patches WOULD be applied:")
        for rule_id, notes in sorted(patches.items()):
            print(f"  {rule_id}:")
            for note in notes:
                print(f"    → {note}")
        print()
        print(f"Total rules to patch: {len(patches)}")
        print("Re-run without --dry-run to apply.")
        return

    # ---- Live run -------------------------------------------------------
    try:
        from pymongo import MongoClient
    except ImportError:
        print("pymongo required. pip install pymongo", file=sys.stderr)
        raise SystemExit(1)

    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10_000)
    db     = client[args.db_name]
    col    = db["interpretation_rules"]

    patched = skipped = errors = 0

    for rule_id, notes in sorted(patches.items()):
        try:
            doc = col.find_one(
                {"rule_id": rule_id, "source.batch_id": BATCH_ID},
                {"rule_id": 1, "_id": 0},
            )
            if not doc:
                print(f"  [SKIP] {rule_id} not found in batch {BATCH_ID}")
                skipped += 1
                continue

            result = col.update_one(
                {"rule_id": rule_id, "source.batch_id": BATCH_ID},
                {"$set": {
                    "pending_review": True,
                    "positional_conflict_note": " | ".join(notes),
                    "positional_conflict_patched_at": datetime.now(timezone.utc).isoformat(),
                }},
            )
            if result.modified_count:
                print(f"  [OK]   {rule_id} → pending_review=True")
                patched += 1
            else:
                print(f"  [SKIP] {rule_id} -- already patched")
                skipped += 1
        except Exception as exc:
            print(f"  [ERR]  {rule_id}: {exc}")
            errors += 1

    print()
    print(f"Patch complete: {patched} patched / {skipped} skipped / {errors} errors")

    print(f"\nFinal DB state for batch {BATCH_ID}:")
    for status in ["auto_approved", "pending_human_review", "pending_review", "flagged"]:
        n = col.count_documents({"source.batch_id": BATCH_ID, "approval_status": status})
        print(f"  {status}: {n}")

    client.close()


if __name__ == "__main__":
    main()
