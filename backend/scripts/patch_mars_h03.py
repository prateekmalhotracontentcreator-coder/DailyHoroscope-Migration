#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import time
from datetime import datetime, timezone
from typing import Any

from pymongo import MongoClient
from pymongo.errors import AutoReconnect


PATCH_FLAG_REASON = "merged_or_condition_split_by_patch_mars_h03"
GROUP_NEUTRAL = "tba15-mars-h03-neutral"
GROUP_FEMALE = "tba15-mars-h03-female"

# Reviewable patch payload. The final inserted documents inherit stable source
# metadata from the merged originals and apply these exact condition/text values.
PATCH_RULES: list[dict[str, Any]] = [
    {
        "rule_id": "R-TBA15-MARS-H03-NEUTRAL-101",
        "condition_group_id": GROUP_NEUTRAL,
        "gender": "neutral",
        "condition_type": "combination",
        "additional_condition": "Mars is conjunct malefics",
        "summary": "If Mars is conjunct malefics - unfavourable for elder co-borns.",
        "interpretation_text": "If Mars is conjunct malefics - unfavourable for elder co-borns.",
        "tags": ["planet_occupation", "house_placement", "mars_h03_patch"],
    },
    {
        "rule_id": "R-TBA15-MARS-H03-NEUTRAL-102",
        "condition_group_id": GROUP_NEUTRAL,
        "gender": "neutral",
        "condition_type": "aspect_rule",
        "additional_condition": "Mars is aspected by malefics",
        "summary": "If Mars is aspected by malefics - unfavourable for elder co-borns.",
        "interpretation_text": "If Mars is aspected by malefics - unfavourable for elder co-borns.",
        "tags": ["planet_occupation", "house_placement", "mars_h03_patch"],
    },
    {
        "rule_id": "R-TBA15-MARS-H03-NEUTRAL-103",
        "condition_group_id": GROUP_NEUTRAL,
        "gender": "neutral",
        "condition_type": "general_principle",
        "additional_condition": "Mars is conjunct malefics or aspected by malefics",
        "summary": "If Mars is conjunct malefics or aspected by malefics - unfavourable for elder co-borns.",
        "interpretation_text": "If Mars is conjunct malefics or aspected by malefics - unfavourable for elder co-borns.",
        "tags": ["planet_occupation", "house_placement", "mars_h03_patch", "grouped_condition_summary"],
    },
    {
        "rule_id": "R-TBA15-MARS-H03-FEMALE-201",
        "condition_group_id": GROUP_FEMALE,
        "gender": "female",
        "condition_type": "planet_in_house_special",
        "additional_condition": "Mars is in own sign",
        "summary": "If Mars is in own sign - prosperous.",
        "interpretation_text": "If Mars is in own sign - prosperous.",
        "tags": ["planet_occupation", "house_placement", "mars_h03_patch", "female_horoscope"],
    },
    {
        "rule_id": "R-TBA15-MARS-H03-FEMALE-202",
        "condition_group_id": GROUP_FEMALE,
        "gender": "female",
        "condition_type": "planet_in_house_special",
        "additional_condition": "Mars is exalted",
        "summary": "If Mars is exalted - prosperous.",
        "interpretation_text": "If Mars is exalted - prosperous.",
        "tags": ["planet_occupation", "house_placement", "mars_h03_patch", "female_horoscope"],
    },
    {
        "rule_id": "R-TBA15-MARS-H03-FEMALE-203",
        "condition_group_id": GROUP_FEMALE,
        "gender": "female",
        "condition_type": "general_principle",
        "additional_condition": "Mars is in own sign or exalted",
        "summary": "If Mars is in own sign or exalted - prosperous.",
        "interpretation_text": "If Mars is in own sign or exalted - prosperous.",
        "tags": [
            "planet_occupation",
            "house_placement",
            "mars_h03_patch",
            "female_horoscope",
            "grouped_condition_summary",
        ],
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Patch Mars in 3rd House merged OR-conditions.")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", required=True)
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


def merged_match(rule: dict[str, Any], group_id: str) -> bool:
    text = " ".join(
        str(part)
        for part in [
            ((rule.get("interpretation") or {}).get("summary") or ""),
            ((rule.get("interpretation") or {}).get("detailed") or ""),
            ((rule.get("condition") or {}).get("additional_condition") or ""),
        ]
    ).lower()
    if group_id == GROUP_NEUTRAL:
        return "with malefics" in text and "aspected by malefics" in text
    if group_id == GROUP_FEMALE:
        return "own sign" in text and "exalted" in text and "prosperous" in text
    return False


def find_merged_rules(col) -> list[dict[str, Any]]:
    candidates = list(
        with_retry(
            "find merged rules",
            lambda: col.find(
                {
                    "$or": [
                        {"condition_group_id": {"$in": [GROUP_NEUTRAL, GROUP_FEMALE]}},
                        {"condition.condition_group_id": {"$in": [GROUP_NEUTRAL, GROUP_FEMALE]}},
                        {"metadata.condition_group_id": {"$in": [GROUP_NEUTRAL, GROUP_FEMALE]}},
                    ]
                },
                {"_id": 0},
            ).sort("rule_id", 1),
        )
    )
    merged: list[dict[str, Any]] = []
    for group_id in (GROUP_NEUTRAL, GROUP_FEMALE):
        group_rules = [
            rule
            for rule in candidates
            if group_id
            in {
                rule.get("condition_group_id"),
                (rule.get("condition") or {}).get("condition_group_id"),
                (rule.get("metadata") or {}).get("condition_group_id"),
            }
        ]
        chosen = next((rule for rule in group_rules if merged_match(rule, group_id)), None)
        if chosen:
            merged.append(chosen)
    return merged


def build_patch_doc(template: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    source = copy.deepcopy(template.get("source") or {})
    source.setdefault("primary", "A Text Book of Astrology")
    source.setdefault("chapter", "Chapter 15 — Mars")
    source.setdefault("author_voice", "modern_analytical")

    interpretation_text = spec["interpretation_text"]
    return {
        "rule_id": spec["rule_id"],
        "science_id": template.get("science_id", "vedic_astrology"),
        "approval_status": "pending_review",
        "condition": {
            "type": spec["condition_type"],
            "planet": "Mars",
            "house": 3,
            "gender": spec["gender"],
            "additional_condition": spec["additional_condition"],
            "condition_group_id": spec["condition_group_id"],
            "is_group_summary": False,
        },
        "interpretation": {
            "summary": spec["summary"],
            "full_text_passages": [
                {
                    "text": interpretation_text,
                    "confidence": "HIGH",
                    "context": "natal",
                }
            ],
        },
        "condition_group_id": spec["condition_group_id"],
        "is_group_summary": False,
        "source": source,
        "metadata": {
            "condition_group_id": spec["condition_group_id"],
            "is_group_summary": False,
            "patch_name": "patch_mars_h03",
        },
        "tags": list(spec["tags"]),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def print_rule(rule: dict[str, Any]) -> None:
    summary = ((rule.get("interpretation") or {}).get("summary") or "").strip()
    print(f"  {rule.get('rule_id', '<missing>')} | {rule.get('condition_group_id')} | {summary}")


def main() -> None:
    args = parse_args()
    live = args.apply
    client = MongoClient(args.mongo_url)
    try:
        col = client[args.db_name]["interpretation_rules"]
        print("\nPATCH_RULES review payload:")
        print(json.dumps(PATCH_RULES, indent=2, ensure_ascii=False))

        merged_rules = find_merged_rules(col)
        print("\nMerged rules identified:")
        if not merged_rules:
            print("  None found.")
            return
        for rule in merged_rules:
            print_rule(rule)

        if len(merged_rules) != 2:
            print(f"\nExpected 2 merged originals, found {len(merged_rules)}. Stopping before apply.")
            return

        if not live:
            print("\n[DRY RUN] Would insert 6 patch rules and deprecate 2 merged originals.")
            return

        existing_patch_ids = set(
            with_retry(
                "check existing patch rules",
                lambda: col.distinct("rule_id", {"rule_id": {"$in": [item["rule_id"] for item in PATCH_RULES]}}),
            )
        )
        if existing_patch_ids:
            print(f"\nPatch rule_ids already exist: {sorted(existing_patch_ids)}")
            print("Aborting to avoid duplicate inserts.")
            return

        template_by_group = {rule["condition_group_id"]: rule for rule in merged_rules}
        docs = [build_patch_doc(template_by_group[item["condition_group_id"]], item) for item in PATCH_RULES]

        insert_result = with_retry("insert patch docs", lambda: col.insert_many(docs, ordered=True))
        deprecated_ids: list[str] = []
        for rule in merged_rules:
            rule_id = rule["rule_id"]
            with_retry(
                f"deprecate {rule_id}",
                lambda rid=rule_id: col.update_many(
                    {"rule_id": rid},
                    {
                        "$set": {
                            "approval_status": "deprecated",
                            "validation.flag_reason": PATCH_FLAG_REASON,
                            "validation.validated_at": datetime.now(timezone.utc).isoformat(),
                        }
                    },
                ),
            )
            deprecated_ids.append(rule_id)

        print("\nPatch applied successfully.")
        print(f"  Inserted   : {len(insert_result.inserted_ids)}")
        print(f"  Deprecated : {len(deprecated_ids)} unique merged rules")
        print("  New rules  :")
        for doc in docs:
            print(f"    - {doc['rule_id']}")
        print("  Deprecated originals:")
        for rule_id in deprecated_ids:
            print(f"    - {rule_id}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
