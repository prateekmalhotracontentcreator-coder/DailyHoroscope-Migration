#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import time
from collections import Counter, defaultdict
from pathlib import Path

from pymongo import MongoClient
from pymongo.errors import AutoReconnect


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CSV = SCRIPT_DIR / "reports" / "horoscope_db_flagged_reconciled.csv"
VALID_ACTIONS = {"approve", "needs_edit", "deprecate"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply co-founder decisions for flagged rules.")
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
    with Path(args.csv_path).open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    actionable = [row for row in rows if (row.get("final_action") or "").strip()]
    print(f"Loaded {len(rows)} rows from {args.csv_path}")
    print(f"Rows with final_action: {len(actionable)}")
    if not actionable:
        return

    client = MongoClient(args.mongo_url)
    try:
        col = client[args.db_name]["interpretation_rules"]
        action_counts: Counter[str] = Counter()
        per_book: dict[str, Counter[str]] = defaultdict(Counter)

        for row in actionable:
            action = (row.get("final_action") or "").strip()
            if action not in VALID_ACTIONS:
                print(f"  Skipping {row.get('rule_id', '?')}: invalid final_action '{action}'")
                continue
            rule_id = row["rule_id"]
            book = row.get("book", "Unknown")
            print(f"\n{rule_id} | {book} | {action}")

            if action == "approve":
                if live:
                    with_retry(
                        f"approve {rule_id}",
                        lambda rid=rule_id: col.update_many(
                            {"rule_id": rid},
                            {
                                "$set": {
                                    "approval_status": "auto_approved",
                                    "validation.reconciliation_note": "cofounder_approve_flagged",
                                }
                            },
                        ),
                    )
            elif action == "needs_edit":
                suggested_edit = row.get("suggested_edit", "")
                if live:
                    with_retry(
                        f"needs_edit {rule_id}",
                        lambda rid=rule_id, note=suggested_edit: col.update_many(
                            {"rule_id": rid},
                            {
                                "$set": {
                                    "approval_status": "pending_human_review",
                                    "validation.edit_note": note,
                                    "validation.reconciliation_note": "cofounder_needs_edit",
                                }
                            },
                        ),
                    )
            elif action == "deprecate":
                if live:
                    with_retry(
                        f"deprecate {rule_id}",
                        lambda rid=rule_id: col.update_many(
                            {"rule_id": rid},
                            {
                                "$set": {
                                    "approval_status": "deprecated",
                                    "validation.reconciliation_note": "cofounder_deprecate_flagged",
                                }
                            },
                        ),
                    )

            action_counts[action] += 1
            per_book[book][action] += 1

        print("\nGrouped summary by source book:")
        for book in sorted(per_book):
            print(f"  {book}")
            for action in sorted(per_book[book]):
                print(f"    {action}: {per_book[book][action]}")

        print("\nOverall summary:")
        for action in sorted(action_counts):
            print(f"  {action}: {action_counts[action]}")
        print("\nMode:", "APPLY" if live else "DRY RUN")
    finally:
        client.close()


if __name__ == "__main__":
    main()
