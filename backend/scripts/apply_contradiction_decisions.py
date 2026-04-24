#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import time
from collections import Counter
from pathlib import Path

from pymongo import MongoClient
from pymongo.errors import AutoReconnect


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CSV = SCRIPT_DIR / "reports" / "horoscope_db_contradictions_reconciled.csv"
VALID_ACTIONS = {"keep_a", "keep_b", "keep_both", "deprecate_both"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply co-founder contradiction decisions.")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", required=True)
    parser.add_argument("--csv-path", default=str(DEFAULT_CSV))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    return parser.parse_args()


def with_retry(label: str, fn):
    for attempt in range(4):
        try:
            return fn()
        except AutoReconnect as exc:
            if attempt < 3:
                wait = 2 ** attempt
                print(f"[retry {attempt + 1}/3] MongoDB timeout during {label} — retrying in {wait}s ({exc})")
                time.sleep(wait)
            else:
                raise


def main() -> None:
    args = parse_args()
    live = args.apply
    rows = list(csv.DictReader(Path(args.csv_path).open(encoding="utf-8", newline="")))
    actionable = [row for row in rows if (row.get("final_action") or "").strip()]
    print(f"Loaded {len(rows)} rows from {args.csv_path}")
    print(f"Rows with final_action: {len(actionable)}")
    if not actionable:
        return

    client = MongoClient(args.mongo_url)
    try:
        col = client[args.db_name]["interpretation_rules"]
        counters: Counter[str] = Counter()

        for row in actionable:
            action = (row.get("final_action") or "").strip()
            if action not in VALID_ACTIONS:
                print(f"  Skipping {row.get('pair_id', '?')}: invalid final_action '{action}'")
                continue

            rule_id_a = row["rule_id_a"]
            rule_id_b = row["rule_id_b"]
            print(f"\n{row['pair_id']}: {action}")
            if action == "keep_a":
                print(f"  keep {rule_id_a}, deprecate {rule_id_b}")
                if live:
                    with_retry(
                        f"deprecate {rule_id_b}",
                        lambda rid=rule_id_b: col.update_many(
                            {"rule_id": rid},
                            {
                                "$set": {
                                    "approval_status": "deprecated",
                                    "validation.reconciliation_note": "cofounder_keep_a",
                                }
                            },
                        ),
                    )
            elif action == "keep_b":
                print(f"  keep {rule_id_b}, deprecate {rule_id_a}")
                if live:
                    with_retry(
                        f"deprecate {rule_id_a}",
                        lambda rid=rule_id_a: col.update_many(
                            {"rule_id": rid},
                            {
                                "$set": {
                                    "approval_status": "deprecated",
                                    "validation.reconciliation_note": "cofounder_keep_b",
                                }
                            },
                        ),
                    )
            elif action == "keep_both":
                print(f"  keep both {rule_id_a} and {rule_id_b} under pending_human_review")
                if live:
                    for rid in (rule_id_a, rule_id_b):
                        with_retry(
                            f"keep both {rid}",
                            lambda rule_id=rid: col.update_many(
                                {"rule_id": rule_id},
                                {
                                    "$set": {
                                        "approval_status": "pending_human_review",
                                        "validation.reconciliation_note": "contradiction_acknowledged_keep_both",
                                    }
                                },
                            ),
                        )
            elif action == "deprecate_both":
                print(f"  deprecate both {rule_id_a} and {rule_id_b}")
                if live:
                    for rid in (rule_id_a, rule_id_b):
                        with_retry(
                            f"deprecate both {rid}",
                            lambda rule_id=rid: col.update_many(
                                {"rule_id": rule_id},
                                {
                                    "$set": {
                                        "approval_status": "deprecated",
                                        "validation.reconciliation_note": "cofounder_deprecate_both",
                                    }
                                },
                            ),
                        )
            counters[action] += 1

        print("\nSummary:")
        for action in sorted(counters):
            print(f"  {action}: {counters[action]}")
        print("\nMode:", "APPLY" if live else "DRY RUN")
    finally:
        client.close()


if __name__ == "__main__":
    main()
