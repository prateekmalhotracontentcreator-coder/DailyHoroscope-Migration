#!/usr/bin/env python3
"""
ingest_lalkitab_ch28_v1.py

Lal Kitab Ch 28 — Varshaphalam and Journey
BATCH_ID: lalkitab-ch28-v1-20260505
18 rules:
  4 varshaphalam_timing  (general_principle)
  1 illness              (dosha)
  1 journey_principle    (general_principle)
  12 journey_outcome     (one per Ketu annual house)

Sources reconciled:
  Lal Kitab_Ch28_JSON Ready_LM.md   — primary rule logic + 120-year table
  Lal Kitab_ch28_Diagnostic_LM.md   — awakening/sleep + conditional modifier logic
  Lal Kitab_Ch28_AI query Answers.md — typed modifier schema (state_gate / priority_override
                                        / dependency_proxy) + enriched per-house detail

Key design decisions:
  1. FORMULA NOT TABLE — LU 28.3 encodes the cyclic formula:
       annual_house = ((natal_house - 1 + (age - 1) % 12) % 12) + 1
     Verified against source: age 34, natal H1 → annual H10 ✓; natal H2 → annual H11 ✓.
     Saves context window; handles any age without hallucination risk.

  2. TYPED MODIFIER SCHEMA (from AI guidance):
     Each Ketu journey rule carries exactly two optional modifier slots:
       condition.state_gate    — PRE-CONDITION: must be satisfied for primary outcome.
                                 Types: dependency, planet_state, house_state,
                                        counter_block, planet_activation, activation_trigger
       condition.priority_override — POST-CONDITION: veto / blocker that overwrites primary
                                     outcome regardless of state_gate result.
     Both slots are None (null) when not applicable.
     Each carries an explicit "logic" string in IF-THEN-ELSE form for LLM state-machine use.

  3. KETU JOURNEY — 12 ATOMIC RULES:
     One rule per Ketu annual house (H1–H12). Per-house detail from AI guidance:
       H1:  Abortive Travel          — activation_trigger: birth of a son
       H2:  Elevation Journey        — Jupiter dependency for promotion
       H3:  Long-distance Migration  — H3-asleep gate → separation from siblings
       H4:  Domestic Stasis          — Moon-in-H4 blocker (long-distance forbidden)
       H5:  Intra-City Relocation    — Jupiter dependency for profitable relocation
       H6:  Climate-Based Journey    — Ketu-awake gate (not awake → useless/troublesome)
       H7:  Forced Short Travel      — Venus/Mercury awaken Ketu to trigger travel
       H8:  Involuntary Hardship     — Moon/Mars-in-H11 veto cancels negative diagnosis
       H9:  Joyful Ancestral Journey — enemy-in-H3 counter-block neutralises joy
       H10: Proxy-Driven Outcome     — Saturn dependency_proxy (Saturn in H4 → harmful)
       H11: Altered Course           — no gate; deferred decision + waste of resources
       H12: Profitable Recreation    — activation_trigger: time with progeny
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pymongo import MongoClient

SCIENCE  = "jyotish"
BOOK     = "Lal Kitab"
BATCH_ID = "lalkitab-ch28-v1-20260505"

# ── Ketu Journey data (12 houses) ────────────────────────────────────────────

KETU_JOURNEY_DATA = [
    {
        "house": 1,
        "slug":  "h1",
        "lu":    "28.5",
        "primary_outcome":  "Abortive Travel",
        "diagnostic_logic": (
            "Preparations manifest but journey fails or results in immediate return. "
            "Activated by the birth of a son."
        ),
        "outcome_quality": "inauspicious",
        "state_gate": {
            "type":               "activation_trigger",
            "activation_trigger": "Progeny (birth of a son)",
            "logic":              "IF birth of son occurs THEN travel intent activates BUT journey aborts or returns immediately",
        },
        "priority_override": None,
    },
    {
        "house": 2,
        "slug":  "h2",
        "lu":    "28.5",
        "primary_outcome":  "Elevation Journey",
        "diagnostic_logic": (
            "Successful travel resulting in job promotion or increased social status. "
            "Jupiter must be auspicious to secure the promotion."
        ),
        "outcome_quality": "auspicious",
        "state_gate": {
            "type":      "dependency",
            "planet":    "Jupiter",
            "condition": "Jupiter must be auspicious",
            "logic":     "IF Jupiter IS auspicious THEN Outcome = 'Promotion secured via travel' ELSE promotion benefit diminished",
        },
        "priority_override": None,
    },
    {
        "house": 3,
        "slug":  "h3",
        "lu":    "28.5",
        "primary_outcome":  "Long-distance Employment Migration",
        "diagnostic_logic": (
            "Professional life defined by frequent long-distance travel. "
            "If H3 is asleep, native lives separately from siblings with no journey."
        ),
        "outcome_quality": "conditional",
        "state_gate": {
            "type":      "house_state",
            "house":     3,
            "condition": "House Asleep",
            "logic":     "IF H3 is asleep THEN Outcome = 'Native lives separately from siblings; No Journey' ELSE long-distance migration proceeds",
        },
        "priority_override": None,
    },
    {
        "house": 4,
        "slug":  "h4",
        "lu":    "28.5",
        "primary_outcome":  "Domestic Stasis",
        "diagnostic_logic": (
            "Minimal to zero travel; any travel restricted to mother's hometown. "
            "Moon in H4 strictly forbids long-distance travel."
        ),
        "outcome_quality": "neutral",
        "state_gate": None,
        "priority_override": {
            "type":      "blocker",
            "condition": "Moon in H4",
            "effect":    "Strictly forbids long-distance travel",
            "logic":     "IF Moon IS in annual H4 THEN long-distance travel is forbidden regardless of primary outcome",
        },
    },
    {
        "house": 5,
        "slug":  "h5",
        "lu":    "28.5",
        "primary_outcome":  "Intra-City Relocation",
        "diagnostic_logic": (
            "Change of residence within local city limits. "
            "Auspicious Jupiter makes the relocation profitable."
        ),
        "outcome_quality": "conditional",
        "state_gate": {
            "type":   "dependency",
            "planet": "Jupiter",
            "logic":  "IF Jupiter IS auspicious THEN Outcome = 'Profitable relocation' ELSE relocation proceeds with neutral result",
        },
        "priority_override": None,
    },
    {
        "house": 6,
        "slug":  "h6",
        "lu":    "28.5",
        "primary_outcome":  "Climate-Based Single Journey",
        "diagnostic_logic": (
            "A one-time journey for health or environmental change. "
            "Journey only occurs if Ketu is awake; otherwise travel is useless or troublesome."
        ),
        "outcome_quality": "conditional",
        "state_gate": {
            "type":    "planet_state",
            "planet":  "Ketu",
            "state":   "awake",
            "logic":   "IF Ketu is NOT awake THEN Outcome = 'Useless/Troublesome travel' ELSE climate journey proceeds",
        },
        "priority_override": None,
    },
    {
        "house": 7,
        "slug":  "h7",
        "lu":    "28.5",
        "primary_outcome":  "Forced Short Travel",
        "diagnostic_logic": (
            "Mandatory short-duration trips. Ketu must be awakened by Venus or Mercury "
            "to trigger the travel. Resistance creates a dead-body travel indicator."
        ),
        "outcome_quality": "inauspicious",
        "state_gate": {
            "type":               "planet_activation",
            "activation_planets": ["Venus", "Mercury"],
            "logic":              "Ketu must be awakened by Venus or Mercury to trigger forced travel; without activation no journey manifests",
        },
        "priority_override": None,
    },
    {
        "house": 8,
        "slug":  "h8",
        "lu":    "28.5",
        "primary_outcome":  "Involuntary Hardship Travel",
        "diagnostic_logic": (
            "Journey against will involving financial loss. "
            "Vetoed (negative diagnosis cancelled) if Moon or Mars are in annual H11."
        ),
        "outcome_quality": "inauspicious",
        "state_gate": None,
        "priority_override": {
            "type":           "veto",
            "veto_condition": ["Moon in annual H11", "Mars in annual H11"],
            "veto_operator":  "OR",
            "logic":          "IF Moon OR Mars IS in annual H11 THEN 'Negative diagnosis is cancelled'",
        },
    },
    {
        "house": 9,
        "slug":  "h9",
        "lu":    "28.5",
        "primary_outcome":  "Joyful Ancestral Journey",
        "diagnostic_logic": (
            "Pleasant travel toward hometown/roots with favorable results. "
            "Joy is neutralized if H3 is occupied by enemy planets."
        ),
        "outcome_quality": "auspicious",
        "state_gate": {
            "type":          "counter_block",
            "counter_block": "Enemy in H3",
            "logic":         "IF annual H3 is occupied by enemy planets THEN Outcome = 'Joy is neutralized'",
        },
        "priority_override": None,
    },
    {
        "house": 10,
        "slug":  "h10",
        "lu":    "28.5",
        "primary_outcome":  "Proxy-Driven Outcome",
        "diagnostic_logic": (
            "Travel nature is a direct reflection of Saturn's status. "
            "Ketu is the vehicle; Saturn is the gatekeeper that determines safety and utility. "
            "Auspicious Saturn = extremely favorable; Saturn in H4 = harmful or useless."
        ),
        "outcome_quality": "conditional",
        "state_gate": {
            "type":              "dependency_proxy",
            "dependency_proxy":  "Saturn",
            "logic":             "IF Saturn IS auspicious THEN Outcome = 'Extremely Favorable' ELSE IF Saturn IS in H4 THEN Outcome = 'Harmful/Useless'",
        },
        "priority_override": None,
    },
    {
        "house": 11,
        "slug":  "h11",
        "lu":    "28.5",
        "primary_outcome":  "Altered Course / Delayed Travel",
        "diagnostic_logic": (
            "Decision to travel is deferred; path changes midway; "
            "results in waste of resources. Native loses control over decision-making."
        ),
        "outcome_quality": "inauspicious",
        "state_gate":       None,
        "priority_override": None,
    },
    {
        "house": 12,
        "slug":  "h12",
        "lu":    "28.5",
        "primary_outcome":  "Profitable Recreation",
        "diagnostic_logic": (
            "Gains and happiness achieved at home; physical travel is pleasant but unnecessary. "
            "Good time with children (progeny) activates the recreation benefit."
        ),
        "outcome_quality": "auspicious",
        "state_gate": {
            "type":               "activation_trigger",
            "activation_trigger": "Spending time with progeny",
            "logic":              "IF time with progeny occurs THEN recreation and home-based gains manifest",
        },
        "priority_override": None,
    },
]


# ── Base document builder ─────────────────────────────────────────────────────

def _base(rule_id: str, logic_unit: str, rule_type: str, sub_type: str,
          summary: str, detailed: str, now: str) -> dict:
    return {
        "rule_id":         rule_id,
        "approval_status": "pending_review",
        "source": {
            "science":    SCIENCE,
            "book":       BOOK,
            "chapter":    28,
            "logic_unit": logic_unit,
            "batch_id":   BATCH_ID,
        },
        "metadata": {
            "rule_type":  rule_type,
            "sub_type":   sub_type,
            "chart_type": "varshaphalam",
        },
        "interpretation": {
            "summary": summary,
            "detailed": detailed,
            "remedies": [],
        },
        "validation": {
            "checkable":     False,
            "yoga_check":    None,
            "validated_by":  None,
            "validated_at":  None,
        },
        "created_at": now,
        "updated_at": now,
    }


# ── Builder: Varshaphalam Timing Engine (4 rules) ────────────────────────────

def build_timing_engine(now: str) -> list[dict]:
    rules = []

    # LU 28.1 — Birth Month Rule
    r = _base(
        rule_id    = "lalkitab-ch28-birth-month-rule",
        logic_unit = "28.1",
        rule_type  = "general_principle",
        sub_type   = "varshaphalam_timing",
        summary    = "ch28-birth-month-rule",
        detailed   = (
            "If the planet occupying Natal House 1 also appears in Varshaphalam House 1, "
            "that planet's effect manifests specifically during the native's birth month. "
            "House 1 in the annual horoscope represents the month of birth."
        ),
        now        = now,
    )
    r["condition"] = {
        "chart_type":   "varshaphalam",
        "planet_of":    "natal_house_1",
        "annual_house": 1,
        "match_type":   "natal_to_annual_h1",
    }
    r["validation"]["yoga_check"] = {"type": "manual", "checkable": False}
    rules.append(r)

    # LU 28.2 — Sun Timing Marker
    r = _base(
        rule_id    = "lalkitab-ch28-sun-timing-marker",
        logic_unit = "28.2",
        rule_type  = "general_principle",
        sub_type   = "varshaphalam_timing",
        summary    = "ch28-sun-timing-marker",
        detailed   = (
            "The primary effect of the Varshaphalam (annual horoscope) becomes available "
            "in the calendar month where the Sun is positioned in the annual chart. "
            "Sun's annual house is the master timing calendar for all Varshaphalam effects."
        ),
        now        = now,
    )
    r["condition"] = {
        "chart_type":    "varshaphalam",
        "planet":        "Sun",
        "role":          "timing_marker",
        "timing_method": "sun_annual_house_position",
    }
    r["validation"]["yoga_check"] = {"type": "manual", "checkable": False}
    rules.append(r)

    # LU 28.3 — Annual Conversion Formula (algorithmic; replaces 120-row table)
    r = _base(
        rule_id    = "lalkitab-ch28-annual-conversion-formula",
        logic_unit = "28.3",
        rule_type  = "general_principle",
        sub_type   = "varshaphalam_timing",
        summary    = "ch28-annual-conversion-formula",
        detailed   = (
            "Every planet's natal house maps to a Varshaphalam (annual) house based on "
            "the native's current age. The mapping follows a 12-year cycle. "
            "Formula: annual_house = ((natal_house - 1 + (age - 1) % 12) % 12) + 1. "
            "LLM should compute the annual house dynamically rather than retrieving from "
            "a static lookup table to preserve context precision. "
            "Verified: age 34 → shift 9; natal H1 → annual H10, natal H2 → annual H11. "
            "Identity years (shift = 0): ages 1, 13, 25, 37, 49, 61, 73, 85, 97, 109."
        ),
        now        = now,
    )
    r["condition"] = {
        "chart_type":        "varshaphalam",
        "conversion_method": "age_based_house_rotation",
    }
    r["condition"]["extra_cond"] = {
        "engine_type":  "algorithmic",
        "component":    "Varshaphalam_Rotation_Engine",
        "formula":      "annual_house = ((natal_house - 1 + (age - 1) % 12) % 12) + 1",
        "cycle_period": 12,
        "max_age":      120,
        "validation_check": {
            "age":                   34,
            "natal_house":           1,
            "expected_annual_house": 10,
        },
        "usage_instructions": (
            "LLM should compute annual_house dynamically rather than retrieving from a "
            "static list to preserve context window and precision."
        ),
        "identity_ages": [1, 13, 25, 37, 49, 61, 73, 85, 97, 109],
    }
    r["validation"]["yoga_check"] = {"type": "manual", "checkable": False}
    rules.append(r)

    # LU 28.3 sub — Influence Priority (propagation order for H1 planet)
    r = _base(
        rule_id    = "lalkitab-ch28-influence-priority",
        logic_unit = "28.3",
        rule_type  = "general_principle",
        sub_type   = "varshaphalam_timing",
        summary    = "ch28-influence-priority",
        detailed   = (
            "When a planet enters Annual House 1, its influence propagates in strict order: "
            "(1) First influences the Natal House where it originally resides. "
            "(2) Then influences its enemy planets in their current annual houses. "
            "(3) Finally influences its friendly planets in their annual houses. "
            "This sequence must be followed before determining the full Varshaphalam effect."
        ),
        now        = now,
    )
    r["condition"] = {
        "chart_type":  "varshaphalam",
        "planet_in":   "annual_house_1",
        "propagation": "natal_house → enemy_planets → friendly_planets",
    }
    r["validation"]["yoga_check"] = {"type": "manual", "checkable": False}
    rules.append(r)

    return rules


# ── Builder: Illness Engine (1 rule) ─────────────────────────────────────────

def build_illness_engine(now: str) -> list[dict]:
    rules = []

    # LU 28.4 — Illness Trigger
    r = _base(
        rule_id    = "lalkitab-ch28-illness-trigger",
        logic_unit = "28.4",
        rule_type  = "dosha",
        sub_type   = "illness",
        summary    = "ch28-illness-trigger",
        detailed   = (
            "In the Varshaphalam (annual chart), if any planet from Group A "
            "(Venus, Mercury, Rahu, or Ketu) forms a conjunction with any planet "
            "from Group B (Sun or Moon), the native is afflicted with illness during "
            "that annual period. The conjunction must occur in the annual chart houses."
        ),
        now        = now,
    )
    r["condition"] = {
        "chart_type":        "varshaphalam",
        "logic_gate":        "AND",
        "conjunction_set_a": ["Venus", "Mercury", "Rahu", "Ketu"],
        "conjunction_set_b": ["Sun", "Moon"],
        "set_operator":      "any_a_with_any_b",
        "houses":            "any_annual_house",
    }
    r["interpretation"]["outcome"] = "native_state: afflicted_with_illness"
    r["validation"]["checkable"]   = True
    r["validation"]["yoga_check"]  = {"type": "planetary_combination", "checkable": True}
    rules.append(r)

    return rules


# ── Builder: Ketu Journey Engine (13 rules) ──────────────────────────────────

def build_ketu_journey(now: str) -> list[dict]:
    rules = []

    # General favorable journey condition
    r = _base(
        rule_id    = "lalkitab-ch28-ketu-journey-general",
        logic_unit = "28.5",
        rule_type  = "general_principle",
        sub_type   = "journey_principle",
        summary    = "ch28-ketu-journey-general",
        detailed   = (
            "For the Varshaphalam Journey Engine: A journey is favorable when Ketu occupies "
            "an earlier annual house than the Moon AND the Moon is not inauspicious. "
            "Ketu's annual house position is the primary significator of journey nature and "
            "outcome. Each house carries specific state_gate (pre-conditions) and "
            "priority_override (veto) logic that the LLM must evaluate in sequence."
        ),
        now        = now,
    )
    r["condition"] = {
        "chart_type": "varshaphalam",
        "planet":     "Ketu",
        "role":       "journey_significator",
        "favorable_condition": {
            "ketu_house_earlier_than_moon":       True,
            "moon_must_not_be_inauspicious":      True,
        },
        "evaluation_sequence": [
            "1. Check primary_outcome",
            "2. Evaluate state_gate (is pre-condition met?)",
            "3. Evaluate priority_override (does veto/blocker apply?)",
        ],
    }
    r["validation"]["yoga_check"] = {"type": "manual", "checkable": False}
    rules.append(r)

    # Per-house Ketu journey rules
    for data in KETU_JOURNEY_DATA:
        rid = f"lalkitab-ch28-ketu-journey-{data['slug']}"
        r = _base(
            rule_id    = rid,
            logic_unit = data["lu"],
            rule_type  = "journey_outcome",
            sub_type   = "journey_outcome",
            summary    = f"ch28-ketu-journey-{data['slug']}",
            detailed   = data["diagnostic_logic"],
            now        = now,
        )
        r["condition"] = {
            "chart_type":        "varshaphalam",
            "planet":            "Ketu",
            "ketu_annual_house": data["house"],
        }
        if data["state_gate"] is not None:
            r["condition"]["state_gate"] = data["state_gate"]
        if data["priority_override"] is not None:
            r["condition"]["priority_override"] = data["priority_override"]

        r["interpretation"]["primary_outcome"] = data["primary_outcome"]
        r["interpretation"]["outcome_quality"] = data["outcome_quality"]
        r["validation"]["checkable"]           = True
        r["validation"]["yoga_check"]          = {"type": "house_position", "checkable": True}
        rules.append(r)

    return rules


# ── Aggregate ─────────────────────────────────────────────────────────────────

def build_all(now: str) -> list[dict]:
    rules = []
    rules.extend(build_timing_engine(now))
    rules.extend(build_illness_engine(now))
    rules.extend(build_ketu_journey(now))
    return rules


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run",  action="store_true")
    parser.add_argument("--save",     help="Path to write JSON")
    parser.add_argument("--upload",   help="Path to JSON for upload")
    parser.add_argument("--mongo-url")
    parser.add_argument("--db-name",  default="horoscope_db")
    args = parser.parse_args()

    now   = datetime.now(timezone.utc).isoformat()
    rules = build_all(now)

    if args.dry_run or args.save:
        by_sub: dict[str, int] = {}
        for r in rules:
            st = r["metadata"]["sub_type"]
            by_sub[st] = by_sub.get(st, 0) + 1

        print(f"Built {len(rules)} rules for batch {BATCH_ID}\n")
        print("Breakdown by sub_type:")
        for st, count in sorted(by_sub.items()):
            print(f"  {st:<30}: {count}")
        print("\nRule IDs:")
        for r in rules:
            print(f"  {r['rule_id']}")

        if args.save:
            with open(args.save, "w") as f:
                json.dump(rules, f, indent=2, default=str)
            print(f"\nSaved → {args.save}")
        print("\nDry run complete.")
        return

    if args.upload:
        if not args.mongo_url:
            raise SystemExit("ERROR: --mongo-url is required with --upload")
        with open(args.upload) as f:
            rules = json.load(f)

        client   = MongoClient(args.mongo_url)
        col      = client[args.db_name]["interpretation_rules"]
        inserted = updated = 0
        for rule in rules:
            result = col.update_one(
                {"rule_id": rule["rule_id"]},
                {"$set":    rule},
                upsert=True,
            )
            if result.upserted_id:
                inserted += 1
            elif result.modified_count:
                updated += 1
        print(f"Loaded {len(rules)} rules from {args.upload}")
        print(f"Inserted {inserted} / Updated {updated} rules → {args.db_name}.interpretation_rules")
        client.close()


if __name__ == "__main__":
    main()
