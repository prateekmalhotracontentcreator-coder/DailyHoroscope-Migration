#!/usr/bin/env python3
"""patch_58ch_positional_conflicts.py

Reads the positional conflict dedup report for Longevity 58Ch and applies
targeted MongoDB patches.

Triage logic
-----------
  self_match           rule_a_id == rule_b_id
                       → ARTIFACT (stale export dir bug, now fixed)
                       → SKIP: no patch

  positional_polarity_conflict  explicit +/− polarity clash
                       → GENUINE cross-system conflict
                       → PATCH: pending_review=True + positional_conflict_note

  positional_alternate_result   same key, dissimilar text, compatible polarity
                       → CONTEXTUAL (KP longevity lens vs classical natal lens)
                       → REVIEW-ONLY: printed to console, no MongoDB patch

Usage:
  python3 backend/scripts/patch_58ch_positional_conflicts.py \\
    --mongo-url "$MONGO_URL" \\
    --dry-run

  python3 backend/scripts/patch_58ch_positional_conflicts.py \\
    --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BATCH_ID    = "longevity_58ch_v1"
REPORT_PATH = Path("KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_58ch_vs_mongodb_v2_positional.json")
LOG_DIR     = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")


class _Tee:
    """Write to both stdout and a log file simultaneously."""
    def __init__(self, log_path: Path):
        log_path.parent.mkdir(parents=True, exist_ok=True)
        self._log = open(log_path, "w", encoding="utf-8")
        self._stdout = sys.__stdout__
    def write(self, data: str) -> None:
        self._stdout.write(data)
        self._stdout.flush()
        self._log.write(data)
        self._log.flush()
    def flush(self) -> None:
        self._stdout.flush()
        self._log.flush()
    def close(self) -> None:
        self._log.close()


def load_report() -> list[dict]:
    if not REPORT_PATH.exists():
        print(f"[error] Report not found: {REPORT_PATH}", file=sys.stderr)
        sys.exit(1)
    data = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    return data.get("positional_conflicts_detail", [])


def triage(details: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    """Return (self_matches, polarity_conflicts, alt_results)."""
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
    return self_matches, polarity_conflicts, alt_results


def print_triage_summary(self_matches, polarity_conflicts, alt_results) -> None:
    total = len(self_matches) + len(polarity_conflicts) + len(alt_results)
    print(f"Positional conflicts in report : {total}")
    print(f"  self-match artifacts (SKIP)  : {len(self_matches)}")
    print(f"  polarity_conflict (PATCH)    : {len(polarity_conflicts)}")
    print(f"  alternate_result (REVIEW)    : {len(alt_results)}")
    print()

    if self_matches:
        print("ARTIFACTS (self-matches -- stale export dir, now fixed, no action needed):")
        for d in self_matches:
            print(f"  {d['rule_a_id']} <-> {d['rule_b_id']}  key={d['positional_key']}  score={d['similarity_score']:.4f}")
        print()

    if polarity_conflicts:
        print("GENUINE POLARITY CONFLICTS (will be patched with pending_review=True):")
        for d in polarity_conflicts:
            print(f"  {d['rule_a_id']} vs {d['rule_b_id']}")
            print(f"    key    : {d['positional_key']}")
            print(f"    A pol  : {d.get('rule_a_polarity','?')}  B pol: {d.get('rule_b_polarity','?')}")
            print(f"    B text : {d.get('rule_b_full_text','')[:160]}")
            print()

    if alt_results:
        print("CONTEXTUAL ALTERNATE RESULTS (review-only, no patch):")
        print("  These are KP-longevity rules vs classical natal rules -- different frameworks,")
        print("  not genuine contradictions. TT will evaluate at co-founder approval stage.")
        print()
        # Group by positional key for readability
        by_key: dict[str, list[dict]] = {}
        for d in alt_results:
            by_key.setdefault(d["positional_key"], []).append(d)
        for key, entries in sorted(by_key.items()):
            print(f"  [{key}]  ({len(entries)} pair(s))")
            for d in entries:
                print(f"    {d['rule_a_id']} vs {d['rule_b_id']}  score={d['similarity_score']:.4f}")
        print()


def build_patches(polarity_conflicts: list[dict]) -> dict[str, list[str]]:
    """Build patch notes keyed by rule_a_id (the 58Ch rule to be patched)."""
    patches: dict[str, list[str]] = {}
    for c in polarity_conflicts:
        rule_id = c["rule_a_id"]
        note = (
            f"positional_polarity_conflict vs {c['rule_b_id']} "
            f"on {c['positional_key']} "
            f"(A={c.get('rule_a_polarity','?')}, B={c.get('rule_b_polarity','?')}, "
            f"score={c.get('similarity_score',0):.3f})"
        )
        patches.setdefault(rule_id, []).append(note)
    return patches


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Patch Longevity 58Ch positional polarity conflicts in MongoDB."
    )
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print what would be patched without writing to MongoDB."
    )
    args = parser.parse_args()

    # ── Auto-save: tee all output to a timestamped log file ───────────────
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = "_dryrun" if args.dry_run else "_live"
    log_path = LOG_DIR / f"patch_58ch_{ts}{suffix}.log"
    tee = _Tee(log_path)
    sys.stdout = tee
    print(f"============================================================")
    print(f"  LOG FILE: {log_path}")
    print(f"============================================================")
    print()

    details = load_report()
    if not details:
        print("No positional conflicts in report. Nothing to patch.")
        print("Longevity 58Ch: CLEAN ✅")
        return

    self_matches, polarity_conflicts, alt_results = triage(details)
    print_triage_summary(self_matches, polarity_conflicts, alt_results)

    if not polarity_conflicts:
        print("No genuine polarity conflicts -- no MongoDB patches required.")
        print("Longevity 58Ch: CLEAN ✅  (all conflicts are contextual or artifacts)")
        return

    patches = build_patches(polarity_conflicts)

    if args.dry_run:
        print("[DRY RUN] The following patches WOULD be applied:")
        for rule_id, notes in sorted(patches.items()):
            print(f"  {rule_id}:")
            for note in notes:
                print(f"    pending_review=True | {note}")
        print()
        print("Re-run without --dry-run to apply.")
        return

    # ---- Live run -------------------------------------------------------
    try:
        from pymongo import MongoClient
    except ImportError:
        print("pymongo required. Install: pip install pymongo", file=sys.stderr)
        raise SystemExit(1)

    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10_000)
    db     = client[args.db_name]
    col    = db["interpretation_rules"]

    patched = skipped = errors = 0

    for rule_id, notes in sorted(patches.items()):
        try:
            doc = col.find_one(
                {"rule_id": rule_id, "source.batch_id": BATCH_ID},
                {"rule_id": 1, "approval_status": 1, "pending_review": 1, "_id": 0},
            )
            if not doc:
                print(f"  [SKIP] {rule_id} not found in batch {BATCH_ID}")
                skipped += 1
                continue

            combined_note = " | ".join(notes)
            result = col.update_one(
                {"rule_id": rule_id, "source.batch_id": BATCH_ID},
                {"$set": {
                    "pending_review": True,
                    "positional_conflict_note": combined_note,
                    "positional_conflict_patched_at": datetime.now(timezone.utc).isoformat(),
                }},
            )
            if result.modified_count:
                print(f"  [OK]   {rule_id} → pending_review=True  ({len(notes)} conflict note(s))")
                patched += 1
            else:
                print(f"  [SKIP] {rule_id} -- already patched or no change")
                skipped += 1
        except Exception as exc:
            print(f"  [ERR]  {rule_id}: {exc}")
            errors += 1

    print()
    print(f"Patch complete: {patched} patched / {skipped} skipped / {errors} errors")

    # Post-patch DB state
    print(f"\nFinal DB state for batch {BATCH_ID}:")
    for status in ["auto_approved", "pending_human_review", "pending_review", "flagged"]:
        n = col.count_documents({"source.batch_id": BATCH_ID, "approval_status": status})
        print(f"  {status}: {n}")

    client.close()


if __name__ == "__main__":
    main()
