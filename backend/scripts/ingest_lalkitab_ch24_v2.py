#!/usr/bin/env python3
"""
ingest_lalkitab_ch24_v2.py — Lal Kitab Chapter 24: Determination of Age (Ayurdaya)
VERSION 2 — Full rewrite incorporating AI De-coded master source (5 May 2026)

Changes from v1 (49 → 60 rules):
  CORRECTED  mortality-stasis: removed "glassy eyes" (stomach stirs only)
  KEPT AS-IS mod-saturn-jup-h11: H11 primary; H11 vacant → standard table
  SPLIT      age-midlife (1 bundle) → 5 atomic rules with corrected conditions
               age-40: Jupiter+Rahu in H9/H11 (was: any house)
               age-56: Moon+Rahu+Mercury in H2/H5 (was: any house)
  SPLIT      age-latelife (1 bundle) → 4 atomic rules
               age-80 gains OR branch: Moon in H3 or H6
  SPLIT      age-shortlife-indicators (1 bundle) → 4 atomic rules
               ind-04: Moon+Rahu in H7/H8 (not any house)
  CORRECTED  age-shortlife-2y: branch A → Jupiter H8-11 + Mars/Mercury/Venus H7
  EXPANDED   age-infancy-12d: branches A/B with OR operator
  EXPANDED   age-childhood-12m: branches + jupiter_houses [2,5,9,11] resolved
  EXPANDED   physical-forehead-whole: added 7 lines (male=50yr)
  EXPANDED   physical-forehead-broken: added 3 lines (M=40,F=50) & 4 lines (M=40)
  NEW        age-longlife-sun-rahu: 3-condition AND gate → long life

Rules to DELETE from DB before upload (bundles replaced by atomic rules):
  lalkitab-ch24-age-midlife
  lalkitab-ch24-age-latelife
  lalkitab-ch24-age-shortlife-indicators

BATCH_ID: lalkitab-ch24-v1-20260504 (unchanged — upsert handles updates)

Standard workflow:
  Step 1 — Delete old bundle rules:
    python3 scripts/ingest_lalkitab_ch24_v2.py \\
      --delete-bundles --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 2 — Dry run + save:
    python3 scripts/ingest_lalkitab_ch24_v2.py \\
      --dry-run --save scripts/lalkitab_ch24_rules.json

  Step 3 — Upload:
    python3 scripts/ingest_lalkitab_ch24_v2.py \\
      --upload scripts/lalkitab_ch24_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 4 — Validate:
    python3 scripts/validate_rules.py \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id lalkitab-ch24-v1-20260504
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCIENCE   = "jyotish"
BOOK      = "Lal Kitab"
BOOK_ID   = "lal-kitab"
CHAPTER   = 24
CHAP_NAME = "Determination of Age — Ayurdaya"
BATCH_ID  = "lalkitab-ch24-v1-20260504"

DOMAINS_LONGEVITY = ["longevity", "health", "timing"]

BUNDLE_RULES_TO_DELETE = [
    "lalkitab-ch24-age-midlife",
    "lalkitab-ch24-age-latelife",
    "lalkitab-ch24-age-shortlife-indicators",
]


def _base(rule_id: str, now: str) -> dict:
    return {
        "rule_id":    rule_id,
        "science_id": SCIENCE,
        "source": {
            "book":           BOOK,
            "book_id":        BOOK_ID,
            "chapter":        CHAPTER,
            "chapter_name":   CHAP_NAME,
            "sloka":          None,
            "batch_id":       BATCH_ID,
            "primary":        BOOK,
            "page_ref":       None,
            "passage_ref_id": None,
        },
        "approval_status": "pending_review",
        "created_at":      now,
    }


def _doc(rule_id, name, rtype, sub_type, checkable, yoga_type,
         text, remedies, domains, tags, planets, houses, extra_cond, now):
    doc = _base(rule_id, now)
    yc: dict = {"type": yoga_type, "checkable": checkable}
    if not checkable:
        yc["description"] = "Physical/behavioral/observational — not automatable in Phase 1."
    cond: dict = {"type": rtype, "sub_type": sub_type, "yoga_check": yc}
    if planets:
        cond["planets_involved"] = planets
    if houses:
        cond["houses_involved"] = houses
    cond.update(extra_cond)
    doc.update({
        "condition": cond,
        "interpretation": {
            "summary":           name,
            "detailed":          text,
            "full_text_passages": [{"text": text, "confidence": "HIGH"}],
            "remedies":          remedies,
            "life_domain":       domains[0],
            "life_domains":      domains,
            "tags":              tags,
            "physical_markers":  [],
        },
        "metadata": {
            "planets_involved":     planets,
            "houses_involved":      houses,
            "signs_involved":       [],
            "condition_count":      1,
            "gender_context":       "neutral",
            "is_group_summary":     False,
            "has_physical_markers": False,
            "physical_categories":  [],
            "yoga_checkable":       checkable,
        },
        "confidence": {
            "source_confidence": "HIGH",
            "extraction_method": "hard_coded",
            "validated":         False,
        },
    })
    return doc


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: Moon-House Age Engine (12 rules) — unchanged from v1
# ─────────────────────────────────────────────────────────────────────────────

MOON_HOUSE_DATA = [
    (1,  90,  "Wednesday", ["Mars"]),
    (2,  96,  "Friday",    ["Venus"]),
    (3,  80,  "Wednesday", ["Mercury"]),
    (4,  85,  "Friday",    ["Moon"]),
    (5,  100, "Tuesday",   ["Ketu", "Mercury"]),
    (6,  80,  "Sunday",    ["Venus"]),
    (7,  85,  "Monday",    ["Mars"]),
    (8,  90,  "Wednesday", ["Jupiter"]),
    (9,  75,  "Thursday",  ["Jupiter"]),
    (10, 90,  "Tuesday",   ["Saturn"]),
    (11, 90,  "Saturday",  ["Saturn"]),
    (12, 90,  "Thursday",  ["Rahu", "Jupiter"]),
]


def build_moon_house(now):
    rules = []
    for h, age, day, lords in MOON_HOUSE_DATA:
        sfx  = "st" if h == 1 else "nd" if h == 2 else "rd" if h == 3 else "th"
        name = f"Moon in H{h} — Lifespan {age} Years, Death on {day}"
        text = (
            f"Moon placed in the {h}{sfx} house: base lifespan = {age} years. "
            f"Day of death = {day}. House lord(s) = {', '.join(lords)}. "
            f"The house lord determines the specific day of death and confirms the "
            f"lifespan reading from the Moon-House primary engine."
        )
        rules.append(_doc(
            rule_id    = f"lalkitab-ch24-moon-h{h}",
            name       = name,
            rtype      = "planetary_combination",
            sub_type   = "moon_age_engine",
            checkable  = True,
            yoga_type  = "planet_in_house",
            text       = text,
            remedies   = [],
            domains    = DOMAINS_LONGEVITY,
            tags       = ["moon", f"h{h}", "age_engine", "lifespan", day.lower()],
            planets    = ["Moon"],
            houses     = [h],
            extra_cond = {"predicted_age": age, "day_of_death": day, "house_lords": lords},
            now        = now,
        ))
    return rules


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: Moon Modifiers (4 rules)
# mod-saturn-jup-h11: kept as-is — H11 primary; H11 vacant → standard table
# ─────────────────────────────────────────────────────────────────────────────

def build_moon_modifiers(now):
    rules = []

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-mod-venus",
        name       = "Moon-Venus Conjunction Modifier — Age 85",
        rtype      = "planetary_combination",
        sub_type   = "moon_modifier",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = (
            "When Moon is conjunct Venus (in the same house), the lifespan modifier "
            "overrides the base Moon-House reading and sets the predicted age to 85 years."
        ),
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["moon", "venus", "conjunction", "modifier", "age_85"],
        planets    = ["Moon", "Venus"],
        houses     = [],
        extra_cond = {"predicted_age": 85, "modifier_type": "conjunction"},
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-mod-male-planet",
        name       = "Moon-Male Planet Conjunction Modifier — Age 96",
        rtype      = "planetary_combination",
        sub_type   = "moon_modifier",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = (
            "When Moon is conjunct any male planet (Jupiter, Sun, or Mars), the lifespan "
            "modifier overrides the base Moon-House reading and sets the predicted age to 96 years."
        ),
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["moon", "jupiter", "sun", "mars", "conjunction", "modifier", "age_96"],
        planets    = ["Moon", "Jupiter", "Sun", "Mars"],
        houses     = [],
        extra_cond = {"predicted_age": 96, "modifier_type": "conjunction", "planet_set": "male"},
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-mod-evil-planet",
        name       = "Moon-Evil Planet Conjunction Modifier — Minus 3 Years",
        rtype      = "planetary_combination",
        sub_type   = "moon_modifier",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = (
            "When Moon is conjunct Rahu or Ketu (evil/shadow planets), the lifespan "
            "is reduced by 3 years from the base Moon-House reading. Subtractive modifier "
            "applied on top of the primary age calculation."
        ),
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["moon", "rahu", "ketu", "conjunction", "modifier", "minus_3"],
        planets    = ["Moon", "Rahu", "Ketu"],
        houses     = [],
        extra_cond = {"age_adjustment": -3, "modifier_type": "subtraction"},
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-mod-saturn-jup-h11",
        name       = "Saturn+Jupiter Present — Age Calculated from H11 (H11 Vacant → Standard Table)",
        rtype      = "general_principle",
        sub_type   = "moon_modifier",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "When Saturn and Jupiter are both present in the chart, the age is determined "
            "from house number 11. If the 11th house is vacant, the estimate of age is "
            "made from the standard Moon-House table. "
            "Decision gate: IF Saturn+Jupiter present → use H11 calculation; "
            "IF H11 vacant → revert to Moon-House standard table."
        ),
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["saturn", "jupiter", "h11", "override", "decision_tree"],
        planets    = ["Saturn", "Jupiter"],
        houses     = [11],
        extra_cond = {
            "modifier_type":      "override",
            "primary_house":      11,
            "fallback_condition": "h11_vacant",
            "fallback_action":    "use_standard_moon_house_table",
        },
        now        = now,
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: Luck / Maturity Logic (3 rules) — unchanged from v1
# ─────────────────────────────────────────────────────────────────────────────

def build_luck_maturity(now):
    rules = []

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-luck-childhood",
        name       = "Childhood Luck Uncertainty — Null State Until Age 12",
        rtype      = "general_principle",
        sub_type   = "luck_window",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "A child's luck remains in an uncertain/null state until the age of 12. "
            "Astrological predictions for life events, career, or wealth cannot be "
            "reliably made for natives under 12 years. Engine flags as luck_state: uncertain."
        ),
        remedies   = [],
        domains    = ["general", "timing", "children"],
        tags       = ["luck", "childhood", "uncertainty", "age_12"],
        planets    = [],
        houses     = [],
        extra_cond = {"age_threshold": 12, "luck_state": "uncertain"},
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-luck-senior",
        name       = "Senior Luck Uncertainty — Null State After Age 70-72",
        rtype      = "general_principle",
        sub_type   = "luck_window",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "A native's luck returns to an uncertain state after the age of 70-72 years. "
            "Engine flags queries for natives over 70-72 as luck_state: uncertain."
        ),
        remedies   = [],
        domains    = ["general", "timing", "longevity"],
        tags       = ["luck", "senior", "uncertainty", "age_70"],
        planets    = [],
        houses     = [],
        extra_cond = {"age_threshold": 72, "luck_state": "uncertain"},
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-maturity-catalog",
        name       = "Planet Maturity Age Catalog — Special Effect Trigger Years",
        rtype      = "general_principle",
        sub_type   = "maturity_ages",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "Each planet manifests its special effect at its maturity age: "
            "Sun=2, Jupiter=16, Moon=24, Venus=25, Mars=28, Mercury=34, "
            "Saturn=36, Rahu=42, Ketu=48."
        ),
        remedies   = [],
        domains    = ["general", "timing", "dasha"],
        tags       = ["maturity", "planet_ages", "special_effect", "trigger_years"],
        planets    = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"],
        houses     = [],
        extra_cond = {
            "maturity_ages": {
                "Sun": 2, "Jupiter": 16, "Moon": 24, "Venus": 25,
                "Mars": 28, "Mercury": 34, "Saturn": 36, "Rahu": 42, "Ketu": 48,
            }
        },
        now        = now,
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: Mortality Symptom Engine (5 rules)
# CORRECTED: mortality-stasis — removed "glassy eyes"; stomach only
# RETAINED:  mortality-reflection-organic (confirmed in source)
# ─────────────────────────────────────────────────────────────────────────────

def build_mortality_symptoms(now):
    SYMPTOMS = [
        (
            "mortality-harsh-nature",
            "Mortality Symptom — Harsh Nature Change (1 Year Remaining)",
            "If the native's habits change and their nature becomes harsh (sudden behavioral "
            "shift toward cruelty or bitterness), the remaining lifespan is approximately 1 year.",
            "1 year",
            ["behavior", "mortality_symptom", "harsh_nature"],
        ),
        (
            "mortality-north-star",
            "Mortality Symptom — Cannot Locate North Star (40 Days Remaining)",
            "If the native becomes unable to locate the North Star (Dhruv Tara) at night — "
            "a capability they previously possessed — the remaining lifespan is approximately 40 days.",
            "40 days",
            ["north_star", "mortality_symptom", "celestial_orientation"],
        ),
        (
            "mortality-reflection-organic",
            "Mortality Symptom — No Reflection in Ghee/Oil/Water (7 Days Remaining)",
            "If the native's reflection is not visible in ghee, oil, or water (organic media), "
            "the critical mortality state is triggered. Remaining lifespan is approximately 7 days.",
            "7 days",
            ["reflection", "ghee", "oil", "water", "mortality_symptom"],
        ),
        (
            "mortality-reflection-mirror",
            "Mortality Symptom — No Reflection in Mirror (1 Day Remaining)",
            "If the native's reflection is not visible in a mirror, the remaining lifespan "
            "is approximately 1 day. More severe indicator than the organic media reflection test.",
            "1 day",
            ["reflection", "mirror", "mortality_symptom", "critical"],
        ),
        (
            "mortality-stasis",
            "Mortality Symptom — Physical Stasis (Few Hours Remaining)",
            "Final phase indicator: if the stomach does not stir during breathing, "
            "the native has only a few hours remaining. Terminal physical stasis marker.",
            "a few hours",
            ["physical_stasis", "stomach", "mortality_symptom", "terminal"],
        ),
    ]

    rules = []
    for slug, name, text, remaining, tags in SYMPTOMS:
        rules.append(_doc(
            rule_id    = f"lalkitab-ch24-{slug}",
            name       = name,
            rtype      = "general_principle",
            sub_type   = "mortality_symptom",
            checkable  = False,
            yoga_type  = "behavioral",
            text       = text,
            remedies   = [],
            domains    = ["longevity", "health", "death"],
            tags       = tags,
            planets    = [],
            houses     = [],
            extra_cond = {"remaining_lifespan": remaining},
            now        = now,
        ))
    return rules


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5A: Core Planetary Age Logic (9 rules)
# Includes the NEW age-longlife-sun-rahu rule
# ─────────────────────────────────────────────────────────────────────────────

def build_core_age(now):
    rules = []

    # Critical Infancy — branches A/B with OR
    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-infancy-12d",
        name       = "Critical Infancy — 12 Days (Moon H6+Sun H10 OR Moon+Ketu H6)",
        rtype      = "planetary_combination",
        sub_type   = "short_life",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = (
            "Critical infancy mortality trigger. "
            "Branch A: Moon in H6 AND Sun in H10 (two-house AND condition). "
            "Branch B: Moon conjunct Ketu in H6. "
            "Branch operator: OR — either branch alone triggers the 12-day prediction. "
            "Predicted age: 12 days."
        ),
        remedies   = [],
        domains    = ["longevity", "progeny", "infant_mortality"],
        tags       = ["infancy", "moon", "ketu", "h6", "short_life", "12_days"],
        planets    = ["Moon", "Sun", "Ketu"],
        houses     = [6, 10],
        extra_cond = {
            "predicted_age_days": 12,
            "branch_operator": "OR",
            "branches": [
                {"branch": "A", "condition": "Moon in H6 AND Sun in H10",
                 "planets": ["Moon", "Sun"], "houses": [6, 10], "operator": "AND"},
                {"branch": "B", "condition": "Moon conjunct Ketu in H6",
                 "planets": ["Moon", "Ketu"], "houses": [6], "operator": "conjunction"},
            ],
        },
        now        = now,
    ))

    # Childhood Mortality — branches + jupiter_houses resolved
    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-childhood-12m",
        name       = "Childhood Mortality — 12 Months (Sun+Saturn in Jupiter's House OR with Unfriendly Male Planet)",
        rtype      = "planetary_combination",
        sub_type   = "short_life",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = (
            "Childhood mortality trigger. Predicted age: 12 months. "
            "Branch A: Sun and Saturn conjunct in the house of Jupiter "
            "(Jupiter's natural houses in Kaal Purush: H2, H5, H9, H11). "
            "Branch B: Sun and Saturn conjunct with a male planet that is not friendly. "
            "Branch operator: OR."
        ),
        remedies   = [],
        domains    = ["longevity", "progeny", "infant_mortality"],
        tags       = ["childhood", "sun", "saturn", "jupiter", "short_life", "12_months"],
        planets    = ["Sun", "Saturn"],
        houses     = [2, 5, 9, 11],
        extra_cond = {
            "predicted_age_months": 12,
            "branch_operator": "OR",
            "branches": [
                {"branch": "A", "condition": "Sun+Saturn in House of Jupiter",
                 "jupiter_houses": [2, 5, 9, 11], "operator": "conjunction_in_house"},
                {"branch": "B", "condition": "Sun+Saturn with unfriendly male planet",
                 "operator": "conjunction_with_planet_type", "planet_type": "unfriendly_male"},
            ],
        },
        now        = now,
    ))

    # Early childhood 9 years
    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-early-9y",
        name       = "Early Childhood — Sun+Moon in H11 → Age 9 Years",
        rtype      = "planetary_combination",
        sub_type   = "short_life",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = "Sun and Moon conjunct in H11 → predicted age: 9 years.",
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["sun", "moon", "h11", "short_life", "age_9"],
        planets    = ["Sun", "Moon"],
        houses     = [11],
        extra_cond = {"predicted_age": 9},
        now        = now,
    ))

    # Early childhood 10 years
    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-early-10y",
        name       = "Early Childhood — Moon+Ketu in H1 → Age 10 Years",
        rtype      = "planetary_combination",
        sub_type   = "short_life",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = "Moon and Ketu conjunct in H1 → predicted age: 10 years.",
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["moon", "ketu", "h1", "short_life", "age_10"],
        planets    = ["Moon", "Ketu"],
        houses     = [1],
        extra_cond = {"predicted_age": 10},
        now        = now,
    ))

    # Sudden death: Moon+Rahu H1
    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-sudden-death",
        name       = "Sudden Death — Moon+Rahu in H1 → Bullet Shot, Afternoon",
        rtype      = "planetary_combination",
        sub_type   = "death_cause",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = (
            "Moon conjunct Rahu in H1: cause of death is bullet shot; "
            "time of death is afternoon. Sudden violent death marker."
        ),
        remedies   = [],
        domains    = ["longevity", "death", "violence"],
        tags       = ["moon", "rahu", "h1", "sudden_death", "bullet", "afternoon"],
        planets    = ["Moon", "Rahu"],
        houses     = [1],
        extra_cond = {"death_cause": "bullet_shot", "death_time": "afternoon"},
        now        = now,
    ))

    # Long illness: 20 years
    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-long-illness",
        name       = "Long Illness — Jupiter+Rahu H2 or Mercury+Jupiter H6 → 20 Years",
        rtype      = "planetary_combination",
        sub_type   = "health_affliction",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = (
            "Long illness trigger. "
            "Branch A: Jupiter conjunct Rahu in H2. "
            "Branch B: Mercury conjunct Jupiter in H6. "
            "Branch operator: OR. Native suffers prolonged illness of approximately 20 years."
        ),
        remedies   = [],
        domains    = ["longevity", "health"],
        tags       = ["jupiter", "rahu", "mercury", "h2", "h6", "long_illness", "20_years"],
        planets    = ["Jupiter", "Rahu", "Mercury"],
        houses     = [2, 6],
        extra_cond = {
            "illness_duration_years": 20,
            "branch_operator": "OR",
            "branches": [
                {"branch": "A", "planets": ["Jupiter", "Rahu"], "house": 2},
                {"branch": "B", "planets": ["Mercury", "Jupiter"], "house": 6},
            ],
        },
        now        = now,
    ))

    # Survival by son
    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-survival-son",
        name       = "Survival by Son — Moon/Rahu H6 + Venus/Ketu Weakened + Physical Signs",
        rtype      = "planetary_combination",
        sub_type   = "longevity_marker",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "Complex AND gate survival marker. "
            "Condition 1: Moon+Rahu in H6 OR Mars malefic in H6. "
            "Condition 2: Venus weakened AND Ketu weakened. "
            "Condition 3 (physical): gums visible when speaking, ear taut upwards. "
            "IF all three conditions met THEN native will be survived by his son. "
            "Non-checkable — physical markers require observational assessment."
        ),
        remedies   = [],
        domains    = ["longevity", "progeny", "family"],
        tags       = ["survival", "son", "moon", "rahu", "h6", "physical_marker"],
        planets    = ["Moon", "Rahu", "Mars", "Venus", "Ketu"],
        houses     = [6],
        extra_cond = {
            "outcome": "survived_by_son",
            "logic_gate": "AND",
            "requires_physical_check": True,
            "physical_markers": ["gums_visible_when_speaking", "ear_taut_upwards"],
        },
        now        = now,
    ))

    # Father dependency
    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-father-dependency",
        name       = "Father's Death Dependency — Mercury+Jupiter H2 or Jupiter+Rahu H3 → Age 30",
        rtype      = "planetary_combination",
        sub_type   = "short_life",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = (
            "Branch A: Mercury conjunct Jupiter in H2. "
            "Branch B: Jupiter conjunct Rahu in H3. "
            "Branch operator: OR. "
            "Native's predicted age: 30 years. Father's death certain at native's age 16, 19, or 22."
        ),
        remedies   = [],
        domains    = ["longevity", "family", "father"],
        tags       = ["mercury", "jupiter", "rahu", "h2", "h3", "age_30", "father_death"],
        planets    = ["Mercury", "Jupiter", "Rahu"],
        houses     = [2, 3],
        extra_cond = {
            "predicted_age": 30,
            "father_death_at_native_age": [16, 19, 22],
            "branch_operator": "OR",
            "branches": [
                {"branch": "A", "planets": ["Mercury", "Jupiter"], "house": 2},
                {"branch": "B", "planets": ["Jupiter", "Rahu"], "house": 3},
            ],
        },
        now        = now,
    ))

    # NEW: Long Life — 3-condition AND gate
    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-longlife-sun-rahu",
        name       = "Long Life — Sun+Rahu H10/H11 AND Life-Slashers H8 AND Saturn H3/5/6",
        rtype      = "planetary_combination",
        sub_type   = "longevity_marker",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = (
            "Counter-intuitive 3-condition AND gate for long life. All three must be met. "
            "Condition 1: Sun and Rahu conjunct in H10 or H11. "
            "Condition 2: Life-slashing planets (Mars, Saturn, Rahu, Ketu) present in H8. "
            "Condition 3: Saturn placed in H3, H5, or H6. "
            "The normally malefic H8 life-slashers are neutralised and transformed into "
            "a longevity indicator by the Sun-Rahu conjunction in H10/H11 combined with "
            "Saturn's specific placement. Classic Lal Kitab counter-intuitive gate. "
            "Outcome: long life."
        ),
        remedies   = [],
        domains    = ["longevity", "health", "timing"],
        tags       = ["long_life", "sun", "rahu", "h10", "h11", "h8", "saturn", "counter_intuitive"],
        planets    = ["Sun", "Rahu", "Saturn"],
        houses     = [3, 5, 6, 8, 10, 11],
        extra_cond = {
            "outcome": "long_life",
            "logic_gate": "AND",
            "conjunction": ["Sun", "Rahu"],
            "conjunction_houses": [10, 11],
            "auxiliary_placement": {
                "planet_type": "life_slashing",
                "eligible_planets": ["Mars", "Saturn", "Rahu", "Ketu"],
                "house": 8,
            },
            "saturn_placement": {
                "planet": "Saturn",
                "eligible_houses": [3, 5, 6],
            },
        },
        now        = now,
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5B: Mid-Life Age Thresholds (5 atomic rules)
# SPLIT from age-midlife bundle
# CORRECTED: age-40 → H9/H11; age-56 → H2/H5
# ─────────────────────────────────────────────────────────────────────────────

def build_midlife_thresholds(now):
    rules = []

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-threshold-35",
        name       = "Mid-Life Age 35 — Moon+Rahu+Mercury in Any House",
        rtype      = "planetary_combination",
        sub_type   = "age_threshold",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = "Moon, Rahu, and Mercury conjunct in any house → predicted age: 35 years.",
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["age_35", "moon", "rahu", "mercury", "midlife", "threshold"],
        planets    = ["Moon", "Rahu", "Mercury"],
        houses     = [],
        extra_cond = {"predicted_age": 35, "house_constraint": "any",
                      "rule_group": "mid-life-age-thresholds"},
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-threshold-40",
        name       = "Mid-Life Age 40 — Jupiter+Rahu in H9 or H11",
        rtype      = "planetary_combination",
        sub_type   = "age_threshold",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = "Jupiter and Rahu conjunct in H9 or H11 → predicted age: 40 years.",
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["age_40", "jupiter", "rahu", "h9", "h11", "midlife", "threshold"],
        planets    = ["Jupiter", "Rahu"],
        houses     = [9, 11],
        extra_cond = {"predicted_age": 40, "house_constraint": "H9_or_H11",
                      "rule_group": "mid-life-age-thresholds"},
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-threshold-45",
        name       = "Mid-Life Age 45 — Rahu+Jupiter H6 OR Mercury+Ketu H12",
        rtype      = "planetary_combination",
        sub_type   = "age_threshold",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = (
            "Branch A: Rahu and Jupiter conjunct in H6. "
            "Branch B: Mercury and Ketu conjunct in H12. "
            "Branch operator: OR. Predicted age: 45 years."
        ),
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["age_45", "rahu", "jupiter", "mercury", "ketu", "h6", "h12",
                      "midlife", "threshold"],
        planets    = ["Rahu", "Jupiter", "Mercury", "Ketu"],
        houses     = [6, 12],
        extra_cond = {
            "predicted_age": 45,
            "rule_group": "mid-life-age-thresholds",
            "branch_operator": "OR",
            "branches": [
                {"branch": "A", "planets": ["Rahu", "Jupiter"], "house": 6},
                {"branch": "B", "planets": ["Mercury", "Ketu"], "house": 12},
            ],
        },
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-threshold-50",
        name       = "Mid-Life Age 50 — Moon+Rahu H5 OR Debilitated Planets in H2 and H7",
        rtype      = "planetary_combination",
        sub_type   = "age_threshold",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = (
            "Branch A: Moon and Rahu conjunct in H5. "
            "Branch B: Planets in H2 and H7 are debilitated/powerless. "
            "Branch operator: OR. Predicted age: 50 years."
        ),
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["age_50", "moon", "rahu", "h5", "debilitated", "midlife", "threshold"],
        planets    = ["Moon", "Rahu"],
        houses     = [2, 5, 7],
        extra_cond = {
            "predicted_age": 50,
            "rule_group": "mid-life-age-thresholds",
            "branch_operator": "OR",
            "branches": [
                {"branch": "A", "planets": ["Moon", "Rahu"], "house": 5,
                 "operator": "conjunction"},
                {"branch": "B", "condition": "planets_debilitated", "houses": [2, 7]},
            ],
        },
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-threshold-56",
        name       = "Mid-Life Age 56 — Moon+Rahu+Mercury in H2 or H5",
        rtype      = "planetary_combination",
        sub_type   = "age_threshold",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = "Moon, Rahu, and Mercury conjunct in H2 or H5 → predicted age: 56 years.",
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["age_56", "moon", "rahu", "mercury", "h2", "h5", "midlife", "threshold"],
        planets    = ["Moon", "Rahu", "Mercury"],
        houses     = [2, 5],
        extra_cond = {"predicted_age": 56, "house_constraint": "H2_or_H5",
                      "rule_group": "mid-life-age-thresholds"},
        now        = now,
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5C: Late-Life Age Thresholds (4 atomic rules)
# SPLIT from age-latelife bundle
# CORRECTED: age-80 gains OR branch — Moon in H3 or H6
# ─────────────────────────────────────────────────────────────────────────────

def build_latelife_thresholds(now):
    rules = []

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-threshold-60",
        name       = "Late-Life Age 60 — Moon+Mercury in H2",
        rtype      = "planetary_combination",
        sub_type   = "age_threshold",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = "Moon and Mercury conjunct in H2 → predicted age: 60 years.",
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["age_60", "moon", "mercury", "h2", "latelife", "threshold"],
        planets    = ["Moon", "Mercury"],
        houses     = [2],
        extra_cond = {"predicted_age": 60, "rule_group": "late-life-age-thresholds"},
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-threshold-75",
        name       = "Late-Life Age 75 — Moon+Rahu in H9",
        rtype      = "planetary_combination",
        sub_type   = "age_threshold",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = "Moon and Rahu conjunct in H9 → predicted age: 75 years.",
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["age_75", "moon", "rahu", "h9", "latelife", "threshold"],
        planets    = ["Moon", "Rahu"],
        houses     = [9],
        extra_cond = {"predicted_age": 75, "rule_group": "late-life-age-thresholds"},
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-threshold-80",
        name       = "Late-Life Age 80 — Moon+Jupiter H4 OR Moon in H3/H6",
        rtype      = "planetary_combination",
        sub_type   = "age_threshold",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = (
            "Branch A: Moon and Jupiter conjunct in H4 → predicted age: 80 years. "
            "Branch B: Moon placed in H3 or H6 (no conjunction required) → predicted age: 80 years. "
            "Branch operator: OR — either branch triggers the 80-year prediction."
        ),
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["age_80", "moon", "jupiter", "h3", "h4", "h6", "latelife", "threshold"],
        planets    = ["Moon", "Jupiter"],
        houses     = [3, 4, 6],
        extra_cond = {
            "predicted_age": 80,
            "rule_group": "late-life-age-thresholds",
            "branch_operator": "OR",
            "branches": [
                {"branch": "A", "planets": ["Moon", "Jupiter"], "house": 4,
                 "operator": "conjunction"},
                {"branch": "B", "planet": "Moon", "houses": [3, 6],
                 "operator": "placement"},
            ],
        },
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-threshold-85",
        name       = "Late-Life Age 85 — Moon+Mars in H7",
        rtype      = "planetary_combination",
        sub_type   = "age_threshold",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = "Moon and Mars conjunct in H7 → predicted age: 85 years.",
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["age_85", "moon", "mars", "h7", "latelife", "threshold"],
        planets    = ["Moon", "Mars"],
        houses     = [7],
        extra_cond = {"predicted_age": 85, "rule_group": "late-life-age-thresholds"},
        now        = now,
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5D: Short Life Rules
# CORRECTED: age-shortlife-2y branch A: Jupiter H8-11 + Mars/Mercury/Venus H7
# SPLIT: age-shortlife-indicators → 4 atomic rules
#        ind-04: Moon+Rahu in H7/H8 (not any house)
# ─────────────────────────────────────────────────────────────────────────────

def build_shortlife(now):
    rules = []

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-age-shortlife-2y",
        name       = "Short Life — 2 Years (Jupiter H8-11+Mars/Mercury/Venus H7 OR Moon+Mercury+Venus H5)",
        rtype      = "dosha",
        sub_type   = "short_life",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = (
            "Two-year lifespan doshas. "
            "Branch A (AND gate): Jupiter in H8, H9, H10, or H11 AND "
            "Mars+Mercury+Venus conjunct in H7. Both sub-conditions must be met. "
            "Branch B: Mercury+Venus+Moon conjunct in H5. "
            "Branch operator: OR — either branch triggers predicted age 2 years."
        ),
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["short_life", "dosha", "age_2", "h5", "h7", "jupiter"],
        planets    = ["Jupiter", "Mars", "Mercury", "Venus", "Moon"],
        houses     = [5, 7, 8, 9, 10, 11],
        extra_cond = {
            "predicted_age": 2,
            "branch_operator": "OR",
            "branches": [
                {
                    "branch": "A",
                    "logic_gate": "AND",
                    "jupiter_in_houses": [8, 9, 10, 11],
                    "conjunction": ["Mars", "Mercury", "Venus"],
                    "conjunction_house": 7,
                },
                {
                    "branch": "B",
                    "conjunction": ["Mercury", "Venus", "Moon"],
                    "house": 5,
                },
            ],
        },
        now        = now,
    ))

    # ind-01: Jupiter hemmed — non-checkable
    rules.append(_doc(
        rule_id    = "lalkitab-ch24-shortlife-ind-01",
        name       = "Short Life Indicator 1 — Jupiter Hemmed by Many Planets",
        rtype      = "dosha",
        sub_type   = "short_life",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "Very many planets surrounding Jupiter (hemmed in on multiple sides) → short life. "
            "Non-checkable: 'very many' is qualitative, requires manual chart assessment. "
            "OR relationship with shortlife-ind-02, -03, -04. Any single match is sufficient."
        ),
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["short_life", "jupiter", "hemmed", "indicator"],
        planets    = ["Jupiter"],
        houses     = [],
        extra_cond = {
            "outcome": "short_life",
            "rule_group": "shortlife-indicators",
            "indicator_number": 1,
            "logic_note": "OR with shortlife-ind-02, -03, -04. Any single match sufficient.",
        },
        now        = now,
    ))

    # ind-02: Mercury+Jupiter+Venus in H9
    rules.append(_doc(
        rule_id    = "lalkitab-ch24-shortlife-ind-02",
        name       = "Short Life Indicator 2 — Mercury+Jupiter+Venus in H9",
        rtype      = "dosha",
        sub_type   = "short_life",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = (
            "Mercury, Jupiter, and Venus conjunct in H9 → short life. "
            "OR relationship with shortlife-ind-01, -03, -04. Any single match is sufficient."
        ),
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["short_life", "mercury", "jupiter", "venus", "h9", "indicator"],
        planets    = ["Mercury", "Jupiter", "Venus"],
        houses     = [9],
        extra_cond = {
            "outcome": "short_life",
            "rule_group": "shortlife-indicators",
            "indicator_number": 2,
            "logic_note": "OR with shortlife-ind-01, -03, -04. Any single match sufficient.",
        },
        now        = now,
    ))

    # ind-03: Jupiter's enemies (Mercury, Venus, Rahu) in H9
    rules.append(_doc(
        rule_id    = "lalkitab-ch24-shortlife-ind-03",
        name       = "Short Life Indicator 3 — Jupiter's Enemies (Mercury+Venus+Rahu) in H9",
        rtype      = "dosha",
        sub_type   = "short_life",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = (
            "Enemy planets of Jupiter — Mercury, Venus, and Rahu — conjunct in H9 → short life. "
            "Jupiter's natural enemies placed in its karaka house (H9). "
            "OR relationship with shortlife-ind-01, -02, -04. Any single match is sufficient."
        ),
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["short_life", "mercury", "venus", "rahu", "h9", "jupiter_enemies", "indicator"],
        planets    = ["Mercury", "Venus", "Rahu"],
        houses     = [9],
        extra_cond = {
            "outcome": "short_life",
            "rule_group": "shortlife-indicators",
            "indicator_number": 3,
            "jupiter_enemies": ["Mercury", "Venus", "Rahu"],
            "logic_note": "OR with shortlife-ind-01, -02, -04. Any single match sufficient.",
        },
        now        = now,
    ))

    # ind-04: Moon+Rahu in H7/H8 AND Mercury in H9
    rules.append(_doc(
        rule_id    = "lalkitab-ch24-shortlife-ind-04",
        name       = "Short Life Indicator 4 — Moon+Rahu in H7/H8 AND Mercury in H9",
        rtype      = "dosha",
        sub_type   = "short_life",
        checkable  = True,
        yoga_type  = "planetary_combination",
        text       = (
            "Compound AND condition: Moon and Rahu conjunct in H7 or H8, "
            "AND Mercury placed in H9. Both conditions must be met simultaneously. "
            "Outcome: short life. "
            "OR relationship with shortlife-ind-01, -02, -03. Any single match is sufficient."
        ),
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["short_life", "moon", "rahu", "h7", "h8", "mercury", "h9", "indicator"],
        planets    = ["Moon", "Rahu", "Mercury"],
        houses     = [7, 8, 9],
        extra_cond = {
            "outcome": "short_life",
            "logic_gate": "AND",
            "rule_group": "shortlife-indicators",
            "indicator_number": 4,
            "conditions": [
                {"planets": ["Moon", "Rahu"], "houses": [7, 8],
                 "operator": "conjunction_in_either"},
                {"planet": "Mercury", "house": 9, "operator": "placement"},
            ],
            "logic_note": "OR with shortlife-ind-01, -02, -03. Any single match sufficient.",
        },
        now        = now,
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6: Physical Metric Engine (5 rules)
# EXPANDED: forehead-whole adds 7 lines (male=50)
# EXPANDED: forehead-broken adds 3 lines (M=40,F=50) and 4 lines (M=40)
# ─────────────────────────────────────────────────────────────────────────────

def build_physical_metrics(now):
    rules = []

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-physical-height",
        name       = "Height-to-Age Engine — Angul Scale (90-108 Anguls → 30-120 Years)",
        rtype      = "general_principle",
        sub_type   = "physical_metric",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "Standard: 48 angul = 36 inches (1 angul ≈ 0.75 inch). "
            "Base: 90 angul → 30 years. Each additional angul adds 5 years. "
            "90→30yr, 91→35yr, 92→40yr, 93→45yr, 94→50yr, 95→55yr, 96→60yr, "
            "97→65yr, 98→70yr, 99→75yr, 100→80yr, 101→85yr, 102→90yr, 103→95yr, "
            "104→100yr, 105→105yr, 106→110yr, 107→115yr, 108→120yr."
        ),
        remedies   = [],
        domains    = ["longevity", "physical_diagnosis"],
        tags       = ["height", "angul", "physical_metric", "age_engine"],
        planets    = [],
        houses     = [],
        extra_cond = {
            "measurement_unit": "angul",
            "conversion": {"angul": 48, "inches": 36, "ratio_inch_per_angul": 0.75},
            "baseline": {"anguls": 90, "years": 30},
            "increment": {"per_angul": 1, "years_added": 5},
            "maximum": {"anguls": 108, "years": 120},
            "full_table": {str(a): (a - 90) * 5 + 30 for a in range(90, 109)},
        },
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-physical-maniband",
        name       = "Maniband (Wrist) Lines — 1=30yr, 2=60yr, 3=90yr, 4=120yr",
        rtype      = "general_principle",
        sub_type   = "physical_metric",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "Count clear, prominent lines at the wrist (maniband). "
            "1 line → 30yr (Short Life). 2 lines → 60yr (Middle Life). "
            "3 lines → 90yr (Long Life). 4 lines → 120yr (Extraordinary Long Life)."
        ),
        remedies   = [],
        domains    = ["longevity", "physical_diagnosis"],
        tags       = ["maniband", "wrist_lines", "palm", "physical_metric"],
        planets    = [],
        houses     = [],
        extra_cond = {
            "measurement": "maniband_lines",
            "scale": {
                1: {"years": 30,  "category": "short_life"},
                2: {"years": 60,  "category": "middle_life"},
                3: {"years": 90,  "category": "long_life"},
                4: {"years": 120, "category": "extraordinary_long_life"},
            },
        },
        now        = now,
    ))

    # EXPANDED: 0-7 lines (added 7 lines: male=50)
    rules.append(_doc(
        rule_id    = "lalkitab-ch24-physical-forehead-whole",
        name       = "Forehead Whole Lines — Gender-Specific Age Table (0-7 Lines)",
        rtype      = "general_principle",
        sub_type   = "physical_metric",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "Whole (unbroken) forehead lines, gender-specific. "
            "0 lines: male=100yr. "
            "1 line: male=20yr, female=40yr. "
            "2 lines: male=30yr, female=60yr. "
            "3 lines: male=60yr, female=70yr. "
            "4 lines: male=80yr, female=80yr. "
            "5 lines: male=100yr, female=100yr. "
            "6 lines: male=120yr, female=80yr. "
            "7 lines: male=50yr (non-linear — high count = overextension); "
            "female value not specified in source."
        ),
        remedies   = [],
        domains    = ["longevity", "physical_diagnosis"],
        tags       = ["forehead", "whole_lines", "gender_specific", "physical_metric"],
        planets    = [],
        houses     = [],
        extra_cond = {
            "line_type": "whole",
            "scale": {
                0: {"male": 100, "female": None},
                1: {"male": 20,  "female": 40},
                2: {"male": 30,  "female": 60},
                3: {"male": 60,  "female": 70},
                4: {"male": 80,  "female": 80},
                5: {"male": 100, "female": 100},
                6: {"male": 120, "female": 80},
                7: {"male": 50,  "female": None},
            },
            "note": "7 lines non-linear: overextension. Female for 0 and 7 lines not in source.",
        },
        now        = now,
    ))

    # EXPANDED: 1-4 broken lines (added 3 and 4)
    rules.append(_doc(
        rule_id    = "lalkitab-ch24-physical-forehead-broken",
        name       = "Forehead Broken Lines — Gender-Specific Age Table (1-4 Broken Lines)",
        rtype      = "general_principle",
        sub_type   = "physical_metric",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "Broken (incomplete) forehead lines, gender-specific. "
            "1 broken line: male=10yr, female=20yr. "
            "2 broken lines: male=30yr, female=40yr. "
            "3 broken lines: male=40yr, female=50yr. "
            "4 broken lines: male=40yr, female=not specified."
        ),
        remedies   = [],
        domains    = ["longevity", "physical_diagnosis"],
        tags       = ["forehead", "broken_lines", "gender_specific", "physical_metric"],
        planets    = [],
        houses     = [],
        extra_cond = {
            "line_type": "broken",
            "scale": {
                1: {"male": 10, "female": 20},
                2: {"male": 30, "female": 40},
                3: {"male": 40, "female": 50},
                4: {"male": 40, "female": None},
            },
        },
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-physical-forehead-ear-to-ear",
        name       = "Forehead Ear-to-Ear Lines — 1 Line=100yr, 2 Lines=70yr",
        rtype      = "general_principle",
        sub_type   = "physical_metric",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "Whole forehead lines extending from ear to ear. "
            "1 ear-to-ear line → 100 years. "
            "2 ear-to-ear lines → 70 years."
        ),
        remedies   = [],
        domains    = ["longevity", "physical_diagnosis"],
        tags       = ["forehead", "ear_to_ear", "whole_lines", "physical_metric"],
        planets    = [],
        houses     = [],
        extra_cond = {"line_type": "ear_to_ear_whole", "scale": {1: 100, 2: 70}},
        now        = now,
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7: Special Effect Cycles (5 rules) — unchanged from v1
# ─────────────────────────────────────────────────────────────────────────────

def build_special_effects(now):
    rules = []

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-effect-sun-h4-exalted",
        name       = "Sun Exalted / Lord of H4 — Starts Work + Home/Vehicle Joy at Age 22",
        rtype      = "planetary_combination",
        sub_type   = "age_effect",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "Sun exalted or sitting in / lord of H4. At age 22: native starts working "
            "or becomes self-employed; gains joy of house and vehicle."
        ),
        remedies   = [],
        domains    = ["career", "property", "timing"],
        tags       = ["sun", "h4", "exalted", "age_22", "career", "property"],
        planets    = ["Sun"],
        houses     = [4],
        extra_cond = {"activation_age": 22,
                      "effects": ["start_work_or_self_employed", "joy_of_house_vehicle"]},
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-effect-sun-h4-debil",
        name       = "Sun Debilitated in H4 — Inauspicious Job/Business + Loss of House/Vehicle",
        rtype      = "planetary_combination",
        sub_type   = "age_effect",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "Sun debilitated in H4: inauspicious effect on job and business; "
            "loss of joy of house and vehicle; affliction to mother."
        ),
        remedies   = [],
        domains    = ["career", "property", "family"],
        tags       = ["sun", "h4", "debilitated", "career", "property", "mother"],
        planets    = ["Sun"],
        houses     = [4],
        extra_cond = {"effects": ["inauspicious_job_business",
                                  "loss_house_vehicle", "mother_affliction"]},
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-effect-moon-h7",
        name       = "Moon Exalted / Lord of H7 — Native Marries at Age 24",
        rtype      = "planetary_combination",
        sub_type   = "age_effect",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = "Moon exalted or sitting in / lord of H7. At age 24: native marries.",
        remedies   = [],
        domains    = ["marriage", "timing"],
        tags       = ["moon", "h7", "exalted", "age_24", "marriage"],
        planets    = ["Moon"],
        houses     = [7],
        extra_cond = {"activation_age": 24, "effects": ["native_marries"]},
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-effect-saturn-h4",
        name       = "Saturn Exalted / Lord of H4 — Native Acquires Land/Property",
        rtype      = "planetary_combination",
        sub_type   = "age_effect",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "Saturn exalted or sitting in / lord of H4: "
            "facilitates proprietary ownership of a piece of land."
        ),
        remedies   = [],
        domains    = ["property", "wealth"],
        tags       = ["saturn", "h4", "exalted", "property", "land"],
        planets    = ["Saturn"],
        houses     = [4],
        extra_cond = {"effects": ["land_ownership"]},
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-effect-rahu-h9",
        name       = "Rahu in H9 — Rise of Luck at Age 42",
        rtype      = "planetary_combination",
        sub_type   = "age_effect",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "Rahu in H9: at age 42 (Rahu's maturity year), "
            "the native experiences a rise of luck."
        ),
        remedies   = [],
        domains    = ["luck", "timing"],
        tags       = ["rahu", "h9", "age_42", "luck"],
        planets    = ["Rahu"],
        houses     = [9],
        extra_cond = {"activation_age": 42, "effects": ["rise_of_luck"]},
        now        = now,
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 8: Foundational Placement Logic (3 rules) — unchanged from v1
# ─────────────────────────────────────────────────────────────────────────────

def build_foundation(now):
    rules = []

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-foundation-beneficence",
        name       = "Foundational — Exalted/Own/Friend's House = Auspicious; Enemy's = Evil",
        rtype      = "general_principle",
        sub_type   = "foundational",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "Planetary dignity table for Ch 24 age effects: "
            "Exalted sign → Auspicious. Own house → Excellent. "
            "Friend's house → Auspicious. Enemy's house → Evil."
        ),
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["dignity", "exalted", "own_house", "foundation"],
        planets    = [],
        houses     = [],
        extra_cond = {
            "dignity_effects": {
                "exalted_sign":  "auspicious",
                "own_house":     "excellent",
                "friends_house": "auspicious",
                "enemies_house": "evil",
            }
        },
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-foundation-exaltation-principle",
        name       = "Foundational — H4 and H9 Give Good Effect",
        rtype      = "general_principle",
        sub_type   = "foundational",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "Houses 4 and 9 give generally good effect. "
            "Moon's relative houses (H3, H6, H11): if exalted → auspicious; "
            "if debilitated → can afflict."
        ),
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["h4", "h9", "foundation", "house_quality"],
        planets    = [],
        houses     = [4, 9],
        extra_cond = {
            "favorable_houses": [4, 9],
            "moon_relative_houses": {
                "houses": [3, 6, 11],
                "if_exalted":     "auspicious",
                "if_debilitated": "can_afflict",
            },
        },
        now        = now,
    ))

    rules.append(_doc(
        rule_id    = "lalkitab-ch24-foundation-debilitation-clock",
        name       = "Debilitation Clock — Malefic Effect Starts 1 Month After Birth",
        rtype      = "general_principle",
        sub_type   = "foundational",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "For debilitated planets, the malefic effect countdown starts specifically "
            "1 month after the date of birth — NOT at birth itself. "
            "Applies to all debilitation-based age and effect calculations in Ch 24."
        ),
        remedies   = [],
        domains    = DOMAINS_LONGEVITY,
        tags       = ["debilitation", "timing", "birth_offset", "foundation"],
        planets    = [],
        houses     = [],
        extra_cond = {
            "effect_start_offset": "1_month_after_birth",
            "applies_to":          "debilitated_planets",
        },
        now        = now,
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# MASTER BUILDER
# ─────────────────────────────────────────────────────────────────────────────

def build_all(now: str) -> list:
    rules = []
    rules.extend(build_moon_house(now))           # 12
    rules.extend(build_moon_modifiers(now))        #  4
    rules.extend(build_luck_maturity(now))         #  3
    rules.extend(build_mortality_symptoms(now))    #  5
    rules.extend(build_core_age(now))              #  9  (includes longlife-sun-rahu)
    rules.extend(build_midlife_thresholds(now))    #  5
    rules.extend(build_latelife_thresholds(now))   #  4
    rules.extend(build_shortlife(now))             #  5  (shortlife-2y + 4 indicators)
    rules.extend(build_physical_metrics(now))      #  5
    rules.extend(build_special_effects(now))       #  5
    rules.extend(build_foundation(now))            #  3
    return rules  # Total: 60


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    group  = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run",        action="store_true")
    group.add_argument("--upload",         metavar="JSON_FILE")
    group.add_argument("--delete-bundles", action="store_true",
                       help="Delete old bundle rules replaced by atomic splits.")
    parser.add_argument("--save",      metavar="JSON_FILE")
    parser.add_argument("--mongo-url", default="")
    parser.add_argument("--db-name",   default="horoscope_db")
    args = parser.parse_args()

    now = datetime.now(timezone.utc).isoformat()

    # ── Delete bundles ────────────────────────────────────────────────────────
    if args.delete_bundles:
        if not args.mongo_url:
            print("ERROR: --mongo-url required for --delete-bundles", file=sys.stderr)
            sys.exit(1)
        from pymongo import MongoClient
        client = MongoClient(args.mongo_url)
        col    = client[args.db_name]["interpretation_rules"]
        print(f"Deleting {len(BUNDLE_RULES_TO_DELETE)} bundle rules from {args.db_name}...\n")
        for rid in BUNDLE_RULES_TO_DELETE:
            res = col.delete_one({"rule_id": rid})
            status = "✅ deleted" if res.deleted_count else "⚠️  not found"
            print(f"  {status}: {rid}")
        client.close()
        print("\nBundle deletion complete. Proceed with --dry-run then --upload.")
        return

    # ── Dry run ────────────────────────────────────────────────────────────────
    if args.dry_run:
        rules     = build_all(now)
        checkable = sum(1 for r in rules if r["condition"]["yoga_check"]["checkable"])
        print(f"Dry run: {len(rules)} rules generated\n")
        print(f"  Checkable: {checkable} / {len(rules)}\n")
        for r in rules:
            chk = "✓" if r["condition"]["yoga_check"]["checkable"] else "·"
            st  = r["condition"].get("sub_type", "")
            print(f"  {chk} {r['rule_id']:<62} [{st}]")
        if args.save:
            Path(args.save).write_text(json.dumps(rules, indent=2, ensure_ascii=False))
            print(f"\nSaved → {args.save}")
        return

    # ── Upload ─────────────────────────────────────────────────────────────────
    if not args.mongo_url:
        print("ERROR: --mongo-url required for upload", file=sys.stderr)
        sys.exit(1)
    from pymongo import MongoClient
    rules    = json.loads(Path(args.upload).read_text())
    print(f"Loaded {len(rules)} rules from {args.upload}")
    client   = MongoClient(args.mongo_url)
    col      = client[args.db_name]["interpretation_rules"]
    inserted = updated = 0
    for r in rules:
        res = col.update_one({"rule_id": r["rule_id"]}, {"$set": r}, upsert=True)
        if res.upserted_id:
            inserted += 1
        elif res.modified_count:
            updated += 1
    print(f"✅ Inserted {inserted} / Updated {updated} rules → {args.db_name}.interpretation_rules")
    client.close()


if __name__ == "__main__":
    main()
