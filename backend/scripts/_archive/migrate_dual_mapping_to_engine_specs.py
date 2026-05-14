#!/usr/bin/env python3
"""
migrate_dual_mapping_to_engine_specs.py

Moves mundane-gaur-ch8-dual-mapping-volatility from interpretation_rules
to mundane_engine_specs, then retires it from the interpretation layer.

Why:
  The rule's result says "Engine outputs 'Dual-Signal Conflict' flag; position
  sizing should be reduced." This is engine behavior (conflict resolution logic),
  not an interpretation rule. It tells the scoring engine HOW to handle a
  sign/nakshatra conflict, not WHAT the planetary configuration means.

Action:
  1. Insert a structured engine_spec document into mundane_engine_specs collection
  2. Update the original interpretation_rules entry:
       approval_status → "retired"
       validation note → "Migrated to mundane_engine_specs as conflict_resolution spec"

Usage:
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/migrate_dual_mapping_to_engine_specs.py --mongo-url "$MONGO_URL"
  python3 /Users/apple/DailyHoroscope-Migration/backend/scripts/migrate_dual_mapping_to_engine_specs.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

SOURCE_RULE_ID = "mundane-gaur-ch8-dual-mapping-volatility"

ENGINE_SPEC = {
    "spec_id":          "mundane-conflict-dual-mapping-sign-vs-nakshatra",
    "spec_type":        "conflict_resolution",
    "science_id":       "mundane_jyotish",
    "source_rule_id":   SOURCE_RULE_ID,
    "source_batch_id":  "mundane-interp-v16-20260506",
    "source_chapter":   "Gaur Ch8",
    "title":            "Dual-Mapping Conflict Handler -- Sign-Signal vs Nakshatra-Signal",
    "description": (
        "When a commodity's governing zodiac sign produces a Bullish signal AND "
        "its governing nakshatra simultaneously produces a Bearish signal (or "
        "vice versa), the engine cannot resolve a clean directional forecast."
    ),
    "trigger": {
        "condition":    "sign_signal != nakshatra_signal",
        "example":      "Gold: Aries (sign) = Bullish, Pushya (nakshatra) = Bearish",
        "commodity_domain": "any commodity with both sign and nakshatra mappings",
    },
    "engine_behavior": {
        "output_flag":          "DUAL_SIGNAL_CONFLICT",
        "directional_forecast": "None -- price oscillates, no clean trend",
        "market_characterisation": "Choppy trading",
        "position_sizing":      "Reduce -- conflict flag means elevated uncertainty",
        "resolution_logic":     (
            "Do not force a directional output. Surface the conflict to the user "
            "with both signals displayed. Let human analyst decide weighting."
        ),
    },
    "notes": (
        "This is a meta-rule about signal conflict, not about planetary "
        "interpretation. Lives in engine_specs, not interpretation_rules. "
        "Source: Gaur Ch8 dual-mapping framework."
    ),
    "status":       "active",
    "created_at":   None,   # set at runtime
    "created_by":   "migrate_dual_mapping_to_engine_specs.py",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--apply",     action="store_true")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    db     = client[args.db_name]
    rules  = db["interpretation_rules"]
    specs  = db["mundane_engine_specs"]
    now    = datetime.now(timezone.utc).isoformat()

    print(f"\n{'═'*65}")
    print(f"C2 Migration: dual-mapping-volatility → mundane_engine_specs")
    print(f"Mode: {'APPLY ✏️' if args.apply else 'DRY RUN 🔍'}")
    print(f"{'═'*65}\n")

    # Verify source rule exists
    r = rules.find_one(
        {"rule_id": SOURCE_RULE_ID, "science_id": "mundane_jyotish"},
        {"_id": 0, "rule_id": 1, "title": 1, "approval_status": 1},
    )
    if not r:
        print(f"  ⚠️  Source rule NOT FOUND in interpretation_rules: {SOURCE_RULE_ID}")
        client.close()
        return

    print(f"  Source rule     : {SOURCE_RULE_ID}")
    print(f"  Current status  : {r.get('approval_status','?')}")
    print(f"  Target spec_id  : {ENGINE_SPEC['spec_id']}")
    print(f"  Target collection: mundane_engine_specs")

    # Check if spec already exists
    existing = specs.find_one({"spec_id": ENGINE_SPEC["spec_id"]}, {"_id": 0, "spec_id": 1})
    if existing:
        print(f"\n  ⚠️  Engine spec already exists: {ENGINE_SPEC['spec_id']}")
        print(f"       Re-run will update the retire note on interpretation_rules only.")

    print()

    if args.apply:
        # 1. Insert engine spec
        if not existing:
            doc = {**ENGINE_SPEC, "created_at": now}
            specs.insert_one(doc)
            print(f"  ✅ Inserted engine spec into mundane_engine_specs")
        else:
            print(f"  ℹ️  Engine spec already present -- skipping insert")

        # 2. Retire source rule from interpretation_rules
        res = rules.update_one(
            {"rule_id": SOURCE_RULE_ID},
            {"$set": {
                "approval_status":               "retired",
                "validation.verdict":            "retired",
                "validation.retired_reason":     (
                    "Migrated to mundane_engine_specs as conflict_resolution spec "
                    "(spec_id: mundane-conflict-dual-mapping-sign-vs-nakshatra). "
                    "This is engine behavior logic, not an interpretation rule."
                ),
                "validation.retired_at":         now,
                "validation.retired_by":         "migrate_dual_mapping_to_engine_specs.py",
                "validation.engine_spec_ref":    ENGINE_SPEC["spec_id"],
            }},
        )
        if res.modified_count:
            print(f"  ✅ Retired source rule in interpretation_rules → 'retired'")
        else:
            print(f"  ⚠️  No change written to interpretation_rules")

        # Library summary
        print(f"\n{'─'*65}")
        approved = rules.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "approved"}
        )
        phr = rules.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "pending_human_review"}
        )
        flagged = rules.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "flagged"}
        )
        retired = rules.count_documents(
            {"science_id": "mundane_jyotish", "approval_status": "retired"}
        )
        spec_count = specs.count_documents({"science_id": "mundane_jyotish"})
        print(f"interpretation_rules (mundane_jyotish):")
        print(f"  approved             : {approved}")
        print(f"  pending_human_review : {phr}")
        print(f"  flagged              : {flagged}")
        print(f"  retired              : {retired}")
        print(f"\nmundane_engine_specs:")
        print(f"  total specs          : {spec_count}")
    else:
        print(f"  🔍 WOULD INSERT engine spec into mundane_engine_specs")
        print(f"  🔍 WOULD RETIRE source rule in interpretation_rules → 'retired'")
        print(f"\nRe-run with --apply to write.")

    client.close()


if __name__ == "__main__":
    main()
