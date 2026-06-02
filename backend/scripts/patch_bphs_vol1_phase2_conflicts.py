#!/usr/bin/env python3
"""patch_bphs_vol1_phase2_conflicts.py

Reads the positional conflict dedup report for BPHS Vol 1 Phase 2 and applies
targeted MongoDB patches.

Triage:
  self_match                   → SKIP
  positional_polarity_conflict → PATCH: pending_review=True + note
  positional_alternate_result  → REVIEW-ONLY: logged, no DB write
  TF-IDF matches               → PATCH: pending_review=True + similarity_note
  contradiction pairs          → PATCH: pending_review=True + contradiction_note

Usage:
  python3 backend/scripts/patch_bphs_vol1_phase2_conflicts.py \\
    --mongo-url "$MONGO_URL" --dry-run

  python3 backend/scripts/patch_bphs_vol1_phase2_conflicts.py \\
    --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BATCH_ID    = "bphs-vol1-phase2-v1-20260601"
REPORT_PATH = Path(
    "KE_TEXTBOOK_DECODE/Dedup_Reports/"
    "dedup_bphs_vol1_phase2_vs_mongodb_positional.json"
)
LOG_DIR     = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")


class _Tee:
    def __init__(self, log_path: Path):
        log_path.parent.mkdir(parents=True, exist_ok=True)
        self._log = open(log_path, "w", encoding="utf-8")
        self._stdout = sys.__stdout__
    def write(self, data: str) -> None:
        self._stdout.write(data); self._stdout.flush()
        self._log.write(data); self._log.flush()
    def flush(self) -> None:
        self._stdout.flush(); self._log.flush()
    def close(self) -> None:
        self._log.close()


def load_report() -> dict:
    if not REPORT_PATH.exists():
        print(f"[error] Report not found: {REPORT_PATH}", file=sys.stderr)
        print("Run retroactive_dedup_bphs_vol1_phase2.sh first.", file=sys.stderr)
        sys.exit(1)
    return json.loads(REPORT_PATH.read_text(encoding="utf-8"))


def triage(data: dict):
    details = data.get("positional_conflicts_detail", [])
    matches = data.get("matches", [])
    contras = data.get("contradictions", [])
    self_matches       = [d for d in details if d["rule_a_id"] == d["rule_b_id"]]
    polarity_conflicts = [d for d in details if d["rule_a_id"] != d["rule_b_id"] and d.get("relationship") == "positional_polarity_conflict"]
    alt_results        = [d for d in details if d["rule_a_id"] != d["rule_b_id"] and d.get("relationship") == "positional_alternate_result"]
    return self_matches, polarity_conflicts, alt_results, matches, contras


def build_patches(polarity_conflicts, sim_matches, contras) -> dict[str, list[str]]:
    patches: dict[str, list[str]] = {}
    for c in polarity_conflicts:
        note = (f"positional_polarity_conflict vs {c['rule_b_id']} on {c['positional_key']} "
                f"(A={c.get('rule_a_polarity','?')}, B={c.get('rule_b_polarity','?')})")
        patches.setdefault(c["rule_a_id"], []).append(note)
    for m in sim_matches:
        if m.get("rule_a_id"):
            patches.setdefault(m["rule_a_id"], []).append(
                f"similarity_match vs {m.get('rule_b_id','?')} score={m.get('similarity_score',0):.3f}")
    for c in contras:
        if c.get("rule_a_id"):
            patches.setdefault(c["rule_a_id"], []).append(
                f"contradiction vs {c.get('rule_b_id','?')} score={c.get('similarity_score',0):.3f} "
                f"(A={c.get('rule_a_polarity','?')}, B={c.get('rule_b_polarity','?')})")
    return patches


def main() -> None:
    parser = argparse.ArgumentParser(description="Patch BPHS Vol 1 Phase 2 positional conflicts.")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = "_dryrun" if args.dry_run else "_live"
    log_path = LOG_DIR / f"patch_bphs_vol1_phase2_{ts}{suffix}.log"
    tee = _Tee(log_path)
    sys.stdout = tee
    print("============================================================")
    print(f"  LOG FILE: {log_path}")
    print("============================================================")
    print()

    data = load_report()
    self_matches, polarity_conflicts, alt_results, sim_matches, contras = triage(data)

    print(f"Positional conflicts in report    : {len(self_matches)+len(polarity_conflicts)+len(alt_results)}")
    print(f"  self-match artifacts (SKIP)     : {len(self_matches)}")
    print(f"  polarity_conflict (PATCH)       : {len(polarity_conflicts)}")
    print(f"  alternate_result (REVIEW-ONLY)  : {len(alt_results)}")
    print(f"TF-IDF similarity matches (PATCH) : {len(sim_matches)}")
    print(f"Contradiction pairs (PATCH)       : {len(contras)}")
    print()

    if self_matches:
        print(f"WARNING: {len(self_matches)} self-match artifact(s) -- export dir not cleared.")
        for d in self_matches:
            print(f"  ARTIFACT SKIP: {d['rule_a_id']} == {d['rule_b_id']}")
        print()

    if alt_results:
        by_key: dict = {}
        for d in alt_results:
            by_key.setdefault(d["positional_key"], []).append(d)
        print(f"CONTEXTUAL ALTERNATE RESULTS (review-only, {len(alt_results)} pairs across {len(by_key)} keys):")
        for key, entries in sorted(by_key.items(), key=lambda x: -len(x[1])):
            print(f"  [{key}]  ({len(entries)} pair(s))")
        print("  → No DB patch needed.")
        print()

    patches = build_patches(polarity_conflicts, sim_matches, contras)

    if not patches:
        print("No genuine conflicts -- no MongoDB patches required.")
        print("BPHS Vol 1 Phase 2: CLEAN ✅")
        return

    if args.dry_run:
        print(f"[DRY RUN] {len(patches)} rule(s) WOULD be patched:")
        for rule_id, notes in sorted(patches.items()):
            print(f"  {rule_id}:")
            for note in notes:
                print(f"    → {note}")
        print()
        print(f"Total rules to patch: {len(patches)}")
        print("Re-run without --dry-run to apply.")
        return

    try:
        from pymongo import MongoClient
    except ImportError:
        print("pymongo required.", file=sys.stderr); raise SystemExit(1)

    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10_000)
    col    = client[args.db_name]["interpretation_rules"]
    patched = skipped = errors = 0

    for rule_id, notes in sorted(patches.items()):
        try:
            doc = col.find_one({"rule_id": rule_id, "source.batch_id": BATCH_ID}, {"rule_id": 1, "_id": 0})
            if not doc:
                print(f"  [SKIP] {rule_id} not found in batch {BATCH_ID}"); skipped += 1; continue
            result = col.update_one(
                {"rule_id": rule_id, "source.batch_id": BATCH_ID},
                {"$set": {"pending_review": True, "positional_conflict_note": " | ".join(notes),
                          "positional_conflict_patched_at": datetime.now(timezone.utc).isoformat()}})
            if result.modified_count:
                print(f"  [OK]   {rule_id} → pending_review=True"); patched += 1
            else:
                print(f"  [SKIP] {rule_id} -- already patched"); skipped += 1
        except Exception as exc:
            print(f"  [ERR]  {rule_id}: {exc}"); errors += 1

    print()
    print(f"Patch complete: {patched} patched / {skipped} skipped / {errors} errors")
    print(f"\nFinal DB state for batch {BATCH_ID}:")
    for status in ["auto_approved", "pending_human_review", "pending_review", "flagged"]:
        n = col.count_documents({"source.batch_id": BATCH_ID, "approval_status": status})
        print(f"  {status}: {n}")
    print(f"  pending_review=True (flag): {col.count_documents({'source.batch_id': BATCH_ID, 'pending_review': True})}")
    client.close()


if __name__ == "__main__":
    main()
