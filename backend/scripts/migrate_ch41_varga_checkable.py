#!/usr/bin/env python3
from __future__ import annotations

import argparse
from typing import Any

from pymongo import MongoClient


BATCH_ID = "bphs-ch41-v1-20260502"
TARGET_GROUPS = ("angular_lord_varga", "fifth_lord_varga", "ninth_lord_varga")
PLANET_ROLE_MAP = {
    "angular_lord_varga": "angular_lord",
    "fifth_lord_varga": "fifth_lord",
    "ninth_lord_varga": "ninth_lord",
}
VIMSHOPAKA_TIERS = {
    2: "Parijatamsa",
    3: "Uttamamsa",
    4: "Gopuramsa",
    5: "Simhasanamsa",
    6: "Paravatamsa",
    7: "Devalokamsa",
    8: "Suralokamsa",
    9: "Iravatamsa",
    10: "Iravatamsa",
}
TIER_ALIASES = {"Brahmalokamsa": "Suralokamsa"}
VALID_TIER_LABELS = sorted(set(VIMSHOPAKA_TIERS.values()) | set(TIER_ALIASES), key=len, reverse=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Migrate BPHS Ch 41 Varga rules to varga_dignity_tier")
    parser.add_argument("--mongo-url", required=True, help="MongoDB connection string")
    parser.add_argument("--db-name", required=True, help="MongoDB database name")
    parser.add_argument("--dry-run", action="store_true", help="Print updates without writing them")
    return parser.parse_args()


def canonical_tier(value: str | None) -> str | None:
    if not value:
        return None
    return TIER_ALIASES.get(value.strip(), value.strip())


def extract_required_tier(yoga_name: str | None) -> str | None:
    text = str(yoga_name or "").strip()
    for candidate in VALID_TIER_LABELS:
        if candidate in text:
            tier = canonical_tier(candidate)
            return tier if tier in set(VIMSHOPAKA_TIERS.values()) else None
    return None


def load_rules(collection: Any) -> list[dict[str, Any]]:
    query = {
        "source.batch_id": BATCH_ID,
        "condition.yoga_group": {"$in": list(TARGET_GROUPS)},
    }
    return list(collection.find(query, {"_id": 0}))


def update_rule(collection: Any, rule_id: str, planet_role: str, required_tier: str, dry_run: bool) -> None:
    update = {
        "$set": {
            "condition.yoga_check.type": "varga_dignity_tier",
            "condition.yoga_check.checkable": True,
            "condition.yoga_check.planet_role": planet_role,
            "condition.yoga_check.required_tier": required_tier,
            "condition.yoga_check.blockers": [],
            "metadata.yoga_checkable": True,
            "approval_status": "pending_human_review",
        }
    }
    if dry_run:
        print(f"DRY-RUN {rule_id}: role={planet_role} tier={required_tier}")
        return
    collection.update_one({"rule_id": rule_id}, update)


def main() -> int:
    args = parse_args()
    client = MongoClient(args.mongo_url)
    collection = client[args.db_name].interpretation_rules
    rules = load_rules(collection)
    updated = 0
    skipped = 0
    errors = 0

    try:
        for rule in rules:
            try:
                condition = rule.get("condition") or {}
                yoga_group = str(condition.get("yoga_group") or "")
                planet_role = PLANET_ROLE_MAP.get(yoga_group)
                required_tier = extract_required_tier(condition.get("yoga_name"))
                if not planet_role or not required_tier:
                    skipped += 1
                    print(f"SKIP {rule.get('rule_id')}: group={yoga_group or 'missing'} tier={required_tier or 'invalid'}")
                    continue
                update_rule(collection, str(rule.get("rule_id") or ""), planet_role, required_tier, args.dry_run)
                updated += 1
            except Exception as exc:  # pragma: no cover - operational path
                errors += 1
                print(f"ERROR {rule.get('rule_id')}: {exc}")
    finally:
        client.close()

    print(f"Summary: rules updated={updated}, rules skipped={skipped}, errors={errors}")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
