#!/usr/bin/env python3
"""
migrate_mundane_v3_v7_conditions.py

Converts all 74 dict-condition rules in batches v3–v7 to prose IF-THEN
strings, then resets their approval_status to 'pending_review' so the
validator can re-evaluate them through all three stages.

Batches targeted:
  mundane-interp-v3-20260506   (27 rules)
  mundane-interp-v4-20260506   (15 rules)
  mundane-interp-v5-20260506   (12 rules)
  mundane-interp-v6-20260506   (11 rules)
  mundane-interp-v7-20260506   ( 9 rules)
  Total:                        74 rules

Conversion strategy (7 dict patterns):
  1. Dict has "primary" key → use it directly (already prose)
  2. Dict has "planet_outcomes" → generate 7-planet IF-chain (Celestial Council)
  3. Dict has "trigger" key → extract trigger + sign-specific effects
  4. Dict has motion-state keys (direct_motion/retrograde/rising/combusted)
  5. Dict has "formula" key → Cloud/Snake auxiliary
  6. Dict has house-outcome keys (4th_house/6th_house/8th_house/12th_house)
  7. Anything else → first 4 key-value pairs joined as prose

After conversion:
  - condition field updated to prose string
  - approval_status reset to 'pending_review'
  - validation subdoc cleared (so validator treats rule as fresh)

Usage:
  # Inspect (dry run — no DB writes):
  python3 backend/scripts/migrate_mundane_v3_v7_conditions.py --mongo-url "$MONGO_URL"

  # Apply:
  python3 backend/scripts/migrate_mundane_v3_v7_conditions.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from pymongo import MongoClient

BATCHES = [
    "mundane-interp-v3-20260506",
    "mundane-interp-v4-20260506",
    "mundane-interp-v5-20260506",
    "mundane-interp-v6-20260506",
    "mundane-interp-v7-20260506",
]

MAX_OUTCOME_CHARS = 100   # max chars per planet outcome in the generated string


# ── Prose Converter ───────────────────────────────────────────────────────────

def _trunc(s: str, n: int = MAX_OUTCOME_CHARS) -> str:
    s = str(s).strip()
    return s[:n] + "…" if len(s) > n else s


def dict_to_prose(cond: dict, rule_id: str) -> str:
    """Convert a condition dict to a prose IF-THEN string."""

    # Pattern 1 — has "primary" key (already prose-embedded)
    if "primary" in cond:
        base = str(cond["primary"]).strip()
        extras = []
        for k, v in cond.items():
            if k in ("primary", "calculation", "notes"):
                continue
            if isinstance(v, str) and len(v) > 10:
                extras.append(f"{k.replace('_', ' ')}: {_trunc(v, 80)}")
            elif isinstance(v, dict):
                # nested dict — take its first value
                first = next(iter(v.values()), "")
                extras.append(f"{k.replace('_', ' ')}: {_trunc(str(first), 60)}")
        if extras:
            return base + " Also: " + "; ".join(extras[:3]) + "."
        return base

    # Pattern 2 — Celestial Council planet_outcomes matrix
    if "planet_outcomes" in cond:
        official  = cond.get("official", "Official")
        formula   = cond.get("appointment_formula", "weekday lord formula")
        domain    = cond.get("domain", "annual forecast domain")
        outcomes  = cond["planet_outcomes"]
        parts = [
            f"IF {planet} → {_trunc(outcome)}"
            for planet, outcome in outcomes.items()
        ]
        return (
            f"Identify the {official} planet as lord of weekday on {formula} "
            f"for the {domain}. "
            f"Apply 7-planet outcome matrix: {'; '.join(parts)}."
        )

    # Pattern 3 — has "trigger" key (eclipse / event rules)
    if "trigger" in cond:
        trigger = str(cond["trigger"]).strip()
        sign_effects = []
        for k, v in cond.items():
            if k == "trigger":
                continue
            if isinstance(v, str):
                sign_effects.append(f"{k}: {_trunc(v, 80)}")
        extra = (" Sign/context effects: " + "; ".join(sign_effects) + ".") if sign_effects else ""
        return f"IF {trigger}.{extra}"

    # Pattern 4 — planet motion-state keys
    motion_keys = [k for k in cond if k in (
        "direct_motion", "retrograde", "rising", "combusted", "conjunction_rule"
    )]
    if motion_keys:
        parts = []
        for k in motion_keys:
            parts.append(f"IF {k.replace('_', ' ')} → {_trunc(str(cond[k]))}")
        extra_keys = [k for k in cond if k not in motion_keys]
        for k in extra_keys[:1]:
            parts.append(f"{k.replace('_', ' ')}: {_trunc(str(cond[k]))}")
        return " ".join(parts) + "."

    # Pattern 5 — has "formula" key (Cloud/Snake auxiliary)
    if "formula" in cond:
        formula   = str(cond["formula"]).strip()
        good_key  = next((k for k in cond if "good" in k.lower()), None)
        poor_key  = next((k for k in cond if "poor" in k.lower()), None)
        notable_key = next((k for k in cond if "notable" in k.lower()), None)
        good_str  = f" Good-rain signal: {_trunc(str(cond[good_key]), 80)}." if good_key else ""
        poor_str  = f" Poor-rain signal: {_trunc(str(cond[poor_key]), 80)}." if poor_key else ""
        note_str  = f" Notable signals: {_trunc(str(cond[notable_key]), 120)}." if notable_key else ""
        return f"Apply formula: {formula}{good_str}{poor_str}{note_str}"

    # Pattern 6 — house-outcome keys (4th_house, 6th_house etc.)
    house_keys = [k for k in cond if "house" in k.lower() and isinstance(cond[k], str)]
    if len(house_keys) >= 2:
        parts = [f"IF Saturn in {k.replace('_', ' ')} → {_trunc(str(cond[k]))}" for k in house_keys]
        return " ".join(parts) + "."

    # Pattern 7 — complex nested / miscellaneous (terrorism, political party, empirical)
    # Extract the most informative top-level string values
    parts = []
    for k, v in cond.items():
        if isinstance(v, str) and len(v) > 15:
            parts.append(f"{k.replace('_', ' ')}: {_trunc(v, 100)}")
        elif isinstance(v, list) and v:
            first = str(v[0])[:80]
            parts.append(f"{k.replace('_', ' ')}: {first}")
        elif isinstance(v, dict):
            sub = next(iter(v.values()), "")
            if isinstance(sub, str) and len(sub) > 10:
                parts.append(f"{k.replace('_', ' ')} — {_trunc(sub, 80)}")
        if len(parts) >= 4:
            break
    if parts:
        return "IF " + "; ".join(parts) + "."
    # Final fallback
    return f"Complex diagnostic condition — see rule notes and result for details. (rule_id: {rule_id})"


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--apply",     action="store_true",
                        help="Write changes to DB. Omit for dry-run inspection.")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]

    total_found = total_converted = total_skipped = 0

    for batch in BATCHES:
        rules = list(col.find(
            {"batch_id": batch},
            {"_id": 0, "rule_id": 1, "condition": 1, "approval_status": 1},
        ))
        dict_rules = [r for r in rules if isinstance(r.get("condition"), dict)]
        prose_rules = [r for r in rules if isinstance(r.get("condition"), str)]

        print(f"\n{'─'*60}")
        print(f"Batch: {batch}")
        print(f"  Total rules: {len(rules)} | Dict: {len(dict_rules)} | Already prose: {len(prose_rules)}")

        total_found += len(dict_rules)

        for r in dict_rules:
            rid  = r["rule_id"]
            cond = r["condition"]
            prose = dict_to_prose(cond, rid)

            print(f"\n  [{rid}]")
            print(f"  OLD (dict): {str(cond)[:80]}...")
            print(f"  NEW (prose): {prose[:120]}{'…' if len(prose) > 120 else ''}")

            if args.apply:
                result = col.update_one(
                    {"rule_id": rid},
                    {"$set": {
                        "condition":       prose,
                        "approval_status": "pending_review",
                    },
                    "$unset": {
                        "validation": "",
                    }},
                )
                if result.modified_count:
                    print(f"  ✅ Updated")
                    total_converted += 1
                else:
                    print(f"  ⚠️  No change written")
                    total_skipped += 1
            else:
                total_converted += 1  # count as would-convert in dry run

    print(f"\n{'═'*60}")
    if args.apply:
        print(f"APPLIED: {total_converted} converted, {total_skipped} skipped")
        print(f"All converted rules reset to approval_status='pending_review'")
        print(f"Validation subdoc cleared — ready for re-validation.")
        print(f"\nNext step: run validate_mundane_rules.py for each batch:")
        for b in BATCHES:
            short = b.replace("mundane-interp-", "").replace("-20260506", "")
            print(f"  --batch-id {b}")
    else:
        print(f"DRY RUN: {total_converted} rules would be converted")
        print(f"Re-run with --apply to write changes to DB.")

    client.close()


if __name__ == "__main__":
    main()
