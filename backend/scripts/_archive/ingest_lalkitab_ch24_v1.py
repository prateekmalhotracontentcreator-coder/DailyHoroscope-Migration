#!/usr/bin/env python3
"""
ingest_lalkitab_ch24_v1.py — Lal Kitab Chapter 24: Determination of Age (Ayurdaya)

49 rules total across 8 groups:
   12  Moon-House Age Engine          (moon-h1 through moon-h12)
    4  Moon modifiers                 (mod-venus, mod-male, mod-evil, mod-saturn-jup)
    3  Luck / maturity logic          (luck-childhood, luck-senior, maturity-catalog)
    5  Mortality symptom engine       (mortality-harsh, mortality-north-star,
                                        mortality-reflection-organic,
                                        mortality-reflection-mirror, mortality-stasis)
   12  Complex planetary age logic    (age-infancy-12d, age-childhood-12m,
                                        age-early-9y, age-early-10y,
                                        age-sudden-death, age-long-illness,
                                        age-survival-son, age-father-dependency,
                                        age-midlife, age-latelife,
                                        age-shortlife-2y, age-shortlife-indicators)
    5  Physical metric engine         (physical-height, physical-maniband,
                                        physical-forehead-whole,
                                        physical-forehead-broken,
                                        physical-forehead-ear-to-ear)
    5  Special effect cycles          (effect-sun-h4-exalted, effect-sun-h4-debil,
                                        effect-moon-h7, effect-saturn-h4,
                                        effect-rahu-h9)
    3  Foundational placement logic   (foundation-beneficence,
                                        foundation-exaltation-principle,
                                        foundation-debilitation-clock)

Source: Lal Kitab Ch 24 JSON Ready (V7 + V11 Final Expansion) + Diagnostic file.
Extraction: hard_coded — zero API calls.

BATCH_ID = "lalkitab-ch24-v1-20260504"

Standard workflow:
  Step 1 — Dry run + save:
    python3 scripts/ingest_lalkitab_ch24_v1.py --dry-run \\
      --save scripts/lalkitab_ch24_rules.json

  Step 2 — Upload:
    python3 scripts/ingest_lalkitab_ch24_v1.py \\
      --upload scripts/lalkitab_ch24_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 3 — Validate:
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
            "summary":  name,
            "detailed": text,
            "full_text_passages": [{"text": text, "confidence": "HIGH"}],
            "remedies":     remedies,
            "life_domain":  domains[0],
            "life_domains": domains,
            "tags":         tags,
            "physical_markers": [],
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
# SECTION 1: Moon-House Age Engine (12 rules)
# ─────────────────────────────────────────────────────────────────────────────
# (house, age, day_of_death, lord_of_house)
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
        rid  = f"lalkitab-ch24-moon-h{h}"
        name = f"Moon in H{h} — Lifespan {age} Years, Death on {day}"
        text = (
            f"Moon placed in the {h}{'st' if h==1 else 'nd' if h==2 else 'rd' if h==3 else 'th'} house: "
            f"base lifespan = {age} years. Day of death = {day}. "
            f"House lord(s) = {', '.join(lords)}. "
            f"The house lord determines the specific day of death and confirms the "
            f"lifespan reading from the Moon-House primary engine."
        )
        rules.append(_doc(
            rule_id   = rid,
            name      = name,
            rtype     = "planetary_combination",
            sub_type  = "moon_age_engine",
            checkable = True,
            yoga_type = "planet_in_house",
            text      = text,
            remedies  = [],
            domains   = DOMAINS_LONGEVITY,
            tags      = ["moon", f"h{h}", "age_engine", "lifespan", day.lower()],
            planets   = ["Moon"],
            houses    = [h],
            extra_cond = {
                "predicted_age":   age,
                "day_of_death":    day,
                "house_lords":     lords,
            },
            now = now,
        ))
    return rules


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: Moon Modifiers (4 rules)
# ─────────────────────────────────────────────────────────────────────────────

def build_moon_modifiers(now):
    rules = []

    rules.append(_doc(
        rule_id   = "lalkitab-ch24-mod-venus",
        name      = "Moon-Venus Conjunction Modifier — Age 85",
        rtype     = "planetary_combination",
        sub_type  = "moon_modifier",
        checkable = True,
        yoga_type = "planetary_combination",
        text      = (
            "When Moon is conjunct Venus (in the same house), the lifespan modifier "
            "overrides the base Moon-House reading and sets the predicted age to 85 years."
        ),
        remedies  = [],
        domains   = DOMAINS_LONGEVITY,
        tags      = ["moon", "venus", "conjunction", "modifier", "age_85"],
        planets   = ["Moon", "Venus"],
        houses    = [],
        extra_cond = {"predicted_age": 85, "modifier_type": "conjunction"},
        now       = now,
    ))

    rules.append(_doc(
        rule_id   = "lalkitab-ch24-mod-male-planet",
        name      = "Moon-Male Planet Conjunction Modifier — Age 96",
        rtype     = "planetary_combination",
        sub_type  = "moon_modifier",
        checkable = True,
        yoga_type = "planetary_combination",
        text      = (
            "When Moon is conjunct any male planet (Jupiter, Sun, or Mars), the "
            "lifespan modifier overrides the base Moon-House reading and sets the "
            "predicted age to 96 years."
        ),
        remedies  = [],
        domains   = DOMAINS_LONGEVITY,
        tags      = ["moon", "jupiter", "sun", "mars", "conjunction", "modifier", "age_96"],
        planets   = ["Moon", "Jupiter", "Sun", "Mars"],
        houses    = [],
        extra_cond = {"predicted_age": 96, "modifier_type": "conjunction", "planet_set": "male"},
        now       = now,
    ))

    rules.append(_doc(
        rule_id   = "lalkitab-ch24-mod-evil-planet",
        name      = "Moon-Evil Planet Conjunction Modifier — Minus 3 Years",
        rtype     = "planetary_combination",
        sub_type  = "moon_modifier",
        checkable = True,
        yoga_type = "planetary_combination",
        text      = (
            "When Moon is conjunct Rahu or Ketu (evil/shadow planets), the lifespan "
            "is reduced by 3 years from the base Moon-House reading. This is a "
            "subtractive modifier applied on top of the primary age calculation."
        ),
        remedies  = [],
        domains   = DOMAINS_LONGEVITY,
        tags      = ["moon", "rahu", "ketu", "conjunction", "modifier", "minus_3"],
        planets   = ["Moon", "Rahu", "Ketu"],
        houses    = [],
        extra_cond = {"age_adjustment": -3, "modifier_type": "subtraction"},
        now       = now,
    ))

    rules.append(_doc(
        rule_id   = "lalkitab-ch24-mod-saturn-jup-h11",
        name      = "Saturn-Jupiter in H11 — Override Moon Table with H11 Calculation",
        rtype     = "general_principle",
        sub_type  = "moon_modifier",
        checkable = False,
        yoga_type = "manual",
        text      = (
            "Decision tree: If Saturn and Jupiter are both in H11 AND H11 is NOT vacant "
            "(other planets present), calculate lifespan from H11 data — do not use the "
            "Moon table. If H11 IS vacant, revert to the standard Moon table calculation. "
            "This is the priority override rule for the Moon-House Age Engine."
        ),
        remedies  = [],
        domains   = DOMAINS_LONGEVITY,
        tags      = ["saturn", "jupiter", "h11", "override", "decision_tree"],
        planets   = ["Saturn", "Jupiter"],
        houses    = [11],
        extra_cond = {"modifier_type": "override", "override_condition": "h11_not_vacant"},
        now       = now,
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: Luck / Maturity Logic (3 rules)
# ─────────────────────────────────────────────────────────────────────────────

def build_luck_maturity(now):
    rules = []

    rules.append(_doc(
        rule_id   = "lalkitab-ch24-luck-childhood",
        name      = "Childhood Luck Uncertainty — Null State Until Age 12",
        rtype     = "general_principle",
        sub_type  = "luck_window",
        checkable = False,
        yoga_type = "manual",
        text      = (
            "A child's luck remains in an uncertain/null state until the age of 12. "
            "Astrological predictions for life events, career, or wealth cannot be "
            "reliably made for natives under 12 years. The engine flags any query for "
            "a native under 12 as 'luck_state: uncertain.'"
        ),
        remedies  = [],
        domains   = ["general", "timing", "children"],
        tags      = ["luck", "childhood", "uncertainty", "age_12"],
        planets   = [],
        houses    = [],
        extra_cond = {"age_threshold": 12, "luck_state": "uncertain"},
        now       = now,
    ))

    rules.append(_doc(
        rule_id   = "lalkitab-ch24-luck-senior",
        name      = "Senior Luck Uncertainty — Null State After Age 70-72",
        rtype     = "general_principle",
        sub_type  = "luck_window",
        checkable = False,
        yoga_type = "manual",
        text      = (
            "A native's luck returns to an uncertain state after the age of 70-72 years. "
            "Just as childhood luck is unpredictable before age 12, senior luck becomes "
            "unpredictable after 70-72. The engine flags queries for natives over 70-72 "
            "as 'luck_state: uncertain.'"
        ),
        remedies  = [],
        domains   = ["general", "timing", "longevity"],
        tags      = ["luck", "senior", "uncertainty", "age_70"],
        planets   = [],
        houses    = [],
        extra_cond = {"age_threshold": 72, "luck_state": "uncertain"},
        now       = now,
    ))

    rules.append(_doc(
        rule_id   = "lalkitab-ch24-maturity-catalog",
        name      = "Planet Maturity Age Catalog — Special Effect Trigger Years",
        rtype     = "general_principle",
        sub_type  = "maturity_ages",
        checkable = False,
        yoga_type = "manual",
        text      = (
            "Each planet manifests its 'special effect' in the native's life at its "
            "maturity age: Sun=2, Jupiter=16, Moon=24, Venus=25, Mars=28, Mercury=34, "
            "Saturn=36, Rahu=42, Ketu=48. These years are logic triggers — the engine "
            "checks for the relevant planet's placement and status when the native "
            "reaches that maturity year."
        ),
        remedies  = [],
        domains   = ["general", "timing", "dasha"],
        tags      = ["maturity", "planet_ages", "special_effect", "trigger_years"],
        planets   = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"],
        houses    = [],
        extra_cond = {
            "maturity_ages": {
                "Sun": 2, "Jupiter": 16, "Moon": 24, "Venus": 25,
                "Mars": 28, "Mercury": 34, "Saturn": 36, "Rahu": 42, "Ketu": 48,
            }
        },
        now       = now,
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: Mortality Symptom Engine (5 rules)
# ─────────────────────────────────────────────────────────────────────────────

def build_mortality_symptoms(now):
    SYMPTOMS = [
        (
            "mortality-harsh-nature",
            "Mortality Symptom — Harsh Nature Change (1 Year Remaining)",
            "behavioral",
            "If the native's habits change and their nature becomes harsh (sudden "
            "behavioral shift toward cruelty or bitterness), the remaining lifespan "
            "is approximately 1 year.",
            "1 year",
            ["behavior", "mortality_symptom", "harsh_nature"],
        ),
        (
            "mortality-north-star",
            "Mortality Symptom — Cannot Locate North Star (40 Days Remaining)",
            "behavioral",
            "If the native becomes unable to locate the North Star (Dhruv Tara) at "
            "night — a capability they previously possessed — the remaining lifespan "
            "is approximately 40 days.",
            "40 days",
            ["north_star", "mortality_symptom", "celestial_orientation"],
        ),
        (
            "mortality-reflection-organic",
            "Mortality Symptom — No Reflection in Ghee/Oil/Water (7 Days Remaining)",
            "behavioral",
            "If the native's reflection is not visible in ghee, oil, or water (organic "
            "media), the critical mortality state is triggered. Remaining lifespan is "
            "approximately 7 days.",
            "7 days",
            ["reflection", "ghee", "oil", "water", "mortality_symptom"],
        ),
        (
            "mortality-reflection-mirror",
            "Mortality Symptom — No Reflection in Mirror (1 Day Remaining)",
            "behavioral",
            "If the native's reflection is not visible in a mirror — a more severe "
            "indicator than organic media failure — the remaining lifespan is "
            "approximately 1 day.",
            "1 day",
            ["reflection", "mirror", "mortality_symptom", "critical"],
        ),
        (
            "mortality-stasis",
            "Mortality Symptom — Physical Stasis (Few Hours Remaining)",
            "behavioral",
            "Final phase indicator: if the stomach does not stir during breathing "
            "AND the eyes become 'stoned' (fixed/glassy), the native has only a few "
            "hours remaining. This is the terminal physical stasis marker.",
            "a few hours",
            ["physical_stasis", "stomach", "eyes", "mortality_symptom", "terminal"],
        ),
    ]

    rules = []
    for slug, name, yoga_type, text, remaining, tags in SYMPTOMS:
        rules.append(_doc(
            rule_id   = f"lalkitab-ch24-{slug}",
            name      = name,
            rtype     = "general_principle",
            sub_type  = "mortality_symptom",
            checkable = False,
            yoga_type = yoga_type,
            text      = text,
            remedies  = [],
            domains   = ["longevity", "health", "death"],
            tags      = tags,
            planets   = [],
            houses    = [],
            extra_cond = {"remaining_lifespan": remaining},
            now       = now,
        ))
    return rules


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: Complex Planetary Age Logic (12 rules)
# ─────────────────────────────────────────────────────────────────────────────

def build_complex_age(now):
    rules = []

    # 24.20 — Critical Infancy
    rules.append(_doc(
        rule_id   = "lalkitab-ch24-age-infancy-12d",
        name      = "Critical Infancy — Moon H6+Sun H10 or Moon+Ketu H6 → 12 Days",
        rtype     = "planetary_combination",
        sub_type  = "short_life",
        checkable = True,
        yoga_type = "planetary_combination",
        text      = (
            "Critical infancy mortality trigger: "
            "(A) Moon in H6 AND Sun in H10, OR "
            "(B) Moon conjunct Ketu in H6. "
            "Predicted age: 12 days. Applies to infant mortality within the first fortnight."
        ),
        remedies  = [],
        domains   = ["longevity", "progeny", "infant_mortality"],
        tags      = ["infancy", "moon", "ketu", "h6", "short_life", "12_days"],
        planets   = ["Moon", "Sun", "Ketu"],
        houses    = [6, 10],
        extra_cond = {"predicted_age_days": 12},
        now       = now,
    ))

    # 24.21 — Childhood Mortality
    rules.append(_doc(
        rule_id   = "lalkitab-ch24-age-childhood-12m",
        name      = "Childhood Mortality — Sun+Saturn in Jupiter's House → 12 Months",
        rtype     = "planetary_combination",
        sub_type  = "short_life",
        checkable = True,
        yoga_type = "planetary_combination",
        text      = (
            "Childhood mortality trigger: Sun and Saturn conjunct in Jupiter's house "
            "OR Sun and Saturn conjunct with an unfriendly male planet. "
            "Predicted age: 12 months. Applies to mortality within the first year of life."
        ),
        remedies  = [],
        domains   = ["longevity", "progeny", "infant_mortality"],
        tags      = ["childhood", "sun", "saturn", "jupiter", "short_life", "12_months"],
        planets   = ["Sun", "Saturn", "Jupiter"],
        houses    = [],
        extra_cond = {"predicted_age_months": 12},
        now       = now,
    ))

    # 24.22a — Early Childhood 9 years
    rules.append(_doc(
        rule_id   = "lalkitab-ch24-age-early-9y",
        name      = "Early Childhood — Sun+Moon in H11 → Age 9 Years",
        rtype     = "planetary_combination",
        sub_type  = "short_life",
        checkable = True,
        yoga_type = "planetary_combination",
        text      = "Sun and Moon conjunct in the 11th house → predicted age: 9 years.",
        remedies  = [],
        domains   = DOMAINS_LONGEVITY,
        tags      = ["sun", "moon", "h11", "short_life", "age_9"],
        planets   = ["Sun", "Moon"],
        houses    = [11],
        extra_cond = {"predicted_age": 9},
        now       = now,
    ))

    # 24.22b — Early Childhood 10 years
    rules.append(_doc(
        rule_id   = "lalkitab-ch24-age-early-10y",
        name      = "Early Childhood — Moon+Ketu in H1 → Age 10 Years",
        rtype     = "planetary_combination",
        sub_type  = "short_life",
        checkable = True,
        yoga_type = "planetary_combination",
        text      = "Moon and Ketu conjunct in the 1st house → predicted age: 10 years.",
        remedies  = [],
        domains   = DOMAINS_LONGEVITY,
        tags      = ["moon", "ketu", "h1", "short_life", "age_10"],
        planets   = ["Moon", "Ketu"],
        houses    = [1],
        extra_cond = {"predicted_age": 10},
        now       = now,
    ))

    # 24.23 — Sudden Death
    rules.append(_doc(
        rule_id   = "lalkitab-ch24-age-sudden-death",
        name      = "Sudden Death — Moon+Rahu in H1 → Bullet Shot, Afternoon",
        rtype     = "planetary_combination",
        sub_type  = "short_life",
        checkable = True,
        yoga_type = "planetary_combination",
        text      = (
            "Moon conjunct Rahu in the 1st house: cause of death is bullet shot; "
            "time of death is afternoon. This is a sudden violent death marker."
        ),
        remedies  = [],
        domains   = ["longevity", "death", "violence"],
        tags      = ["moon", "rahu", "h1", "sudden_death", "bullet", "afternoon"],
        planets   = ["Moon", "Rahu"],
        houses    = [1],
        extra_cond = {"death_cause": "bullet_shot", "death_time": "afternoon"},
        now       = now,
    ))

    # 24.24 — Long Illness
    rules.append(_doc(
        rule_id   = "lalkitab-ch24-age-long-illness",
        name      = "Long Illness — Jupiter+Rahu H2 or Mercury+Jupiter H6 → 20 Years",
        rtype     = "planetary_combination",
        sub_type  = "health_affliction",
        checkable = True,
        yoga_type = "planetary_combination",
        text      = (
            "Long illness trigger: "
            "(A) Jupiter conjunct Rahu in H2, OR "
            "(B) Mercury conjunct Jupiter in H6. "
            "The native suffers a prolonged illness lasting approximately 20 years."
        ),
        remedies  = [],
        domains   = ["longevity", "health"],
        tags      = ["jupiter", "rahu", "mercury", "h2", "h6", "long_illness", "20_years"],
        planets   = ["Jupiter", "Rahu", "Mercury"],
        houses    = [2, 6],
        extra_cond = {"illness_duration_years": 20},
        now       = now,
    ))

    # 24.25 — Survival by Son
    rules.append(_doc(
        rule_id   = "lalkitab-ch24-age-survival-son",
        name      = "Survival by Son Marker — Moon/Rahu H6 + Weakened Venus/Ketu + Physical Signs",
        rtype     = "planetary_combination",
        sub_type  = "longevity_marker",
        checkable = False,
        yoga_type = "manual",
        text      = (
            "Complex survival marker: IF (Moon+Rahu in H6 OR Mars malefic in H6) "
            "AND (Venus weakened AND Ketu weakened) "
            "AND physical signs (gums visible when speaking, ear taut upwards) "
            "THEN the native will definitely be survived by his son."
        ),
        remedies  = [],
        domains   = ["longevity", "progeny", "family"],
        tags      = ["survival", "son", "moon", "rahu", "h6", "physical_marker"],
        planets   = ["Moon", "Rahu", "Mars", "Venus", "Ketu"],
        houses    = [6],
        extra_cond = {"outcome": "survived_by_son", "requires_physical_check": True},
        now       = now,
    ))

    # 24.26 — Father Dependency
    rules.append(_doc(
        rule_id   = "lalkitab-ch24-age-father-dependency",
        name      = "Father's Death Dependency — Mercury+Jupiter H2 or Jupiter+Rahu H3",
        rtype     = "planetary_combination",
        sub_type  = "short_life",
        checkable = True,
        yoga_type = "planetary_combination",
        text      = (
            "Father dependency trigger: "
            "(A) Mercury conjunct Jupiter in H2, OR "
            "(B) Jupiter conjunct Rahu in H3. "
            "Native's predicted age: 30 years. "
            "Father's death: certain at native's age 16, 19, or 22."
        ),
        remedies  = [],
        domains   = ["longevity", "family", "father"],
        tags      = ["mercury", "jupiter", "rahu", "h2", "h3", "age_30", "father_death"],
        planets   = ["Mercury", "Jupiter", "Rahu"],
        houses    = [2, 3],
        extra_cond = {
            "predicted_age": 30,
            "father_death_at_native_age": [16, 19, 22],
        },
        now       = now,
    ))

    # 24.27 — Mid-Life Thresholds
    rules.append(_doc(
        rule_id   = "lalkitab-ch24-age-midlife",
        name      = "Mid-Life Age Thresholds — 35 / 40 / 45 / 50 / 56 Years",
        rtype     = "planetary_combination",
        sub_type  = "age_threshold",
        checkable = True,
        yoga_type = "planetary_combination",
        text      = (
            "Mid-life planetary age thresholds:\n"
            "Age 35: Moon+Rahu+Mercury in any house.\n"
            "Age 40: Jupiter+Rahu in any house.\n"
            "Age 45: Rahu+Jupiter in H6 OR Mercury+Ketu in H12.\n"
            "Age 50: Moon+Rahu in H5 OR any debilitated planets.\n"
            "Age 56: Moon+Rahu+Mercury in any house."
        ),
        remedies  = [],
        domains   = DOMAINS_LONGEVITY,
        tags      = ["midlife", "age_35", "age_40", "age_45", "age_50", "age_56", "threshold"],
        planets   = ["Moon", "Rahu", "Mercury", "Jupiter", "Ketu"],
        houses    = [5, 6, 12],
        extra_cond = {
            "thresholds": [
                {"age": 35, "condition": "Moon+Rahu+Mercury any house"},
                {"age": 40, "condition": "Jupiter+Rahu any house"},
                {"age": 45, "condition": "Rahu+Jupiter H6 OR Mercury+Ketu H12"},
                {"age": 50, "condition": "Moon+Rahu H5 OR debilitated planets"},
                {"age": 56, "condition": "Moon+Rahu+Mercury any house"},
            ]
        },
        now       = now,
    ))

    # 24.28 — Late-Life Thresholds
    rules.append(_doc(
        rule_id   = "lalkitab-ch24-age-latelife",
        name      = "Late-Life Age Thresholds — 60 / 75 / 80 / 85 Years",
        rtype     = "planetary_combination",
        sub_type  = "age_threshold",
        checkable = True,
        yoga_type = "planetary_combination",
        text      = (
            "Late-life planetary age thresholds:\n"
            "Age 60: Moon+Mercury in H2.\n"
            "Age 75: Moon+Rahu in H9.\n"
            "Age 80: Moon+Jupiter in H4.\n"
            "Age 85: Moon+Mars in H7."
        ),
        remedies  = [],
        domains   = DOMAINS_LONGEVITY,
        tags      = ["latelife", "age_60", "age_75", "age_80", "age_85", "threshold"],
        planets   = ["Moon", "Mercury", "Rahu", "Jupiter", "Mars"],
        houses    = [2, 7, 9, 4],
        extra_cond = {
            "thresholds": [
                {"age": 60, "condition": "Moon+Mercury H2"},
                {"age": 75, "condition": "Moon+Rahu H9"},
                {"age": 80, "condition": "Moon+Jupiter H4"},
                {"age": 85, "condition": "Moon+Mars H7"},
            ]
        },
        now       = now,
    ))

    # 24.29 — Short Life 2 Years
    rules.append(_doc(
        rule_id   = "lalkitab-ch24-age-shortlife-2y",
        name      = "Short Life Conjunction — 2 Years (Mars+Mercury+Venus H7 or Moon+Mercury+Venus H5)",
        rtype     = "dosha",
        sub_type  = "short_life",
        checkable = True,
        yoga_type = "planetary_combination",
        text      = (
            "Two-year lifespan doshas:\n"
            "(A) Mars+Mercury+Venus conjunct in H7 (with Jupiter present), OR\n"
            "(B) Mercury+Venus+Moon conjunct in H5.\n"
            "Both are critical short-life indicators with predicted age of 2 years."
        ),
        remedies  = [],
        domains   = DOMAINS_LONGEVITY,
        tags      = ["short_life", "dosha", "age_2", "h5", "h7"],
        planets   = ["Mars", "Mercury", "Venus", "Moon", "Jupiter"],
        houses    = [5, 7],
        extra_cond = {"predicted_age": 2},
        now       = now,
    ))

    # 24.30 — General Short Life Indicators
    rules.append(_doc(
        rule_id   = "lalkitab-ch24-age-shortlife-indicators",
        name      = "General Short Life Indicators — Jupiter Surrounded or H9 Enemies",
        rtype     = "dosha",
        sub_type  = "short_life",
        checkable = True,
        yoga_type = "planetary_combination",
        text      = (
            "General short life indicators:\n"
            "1. Many planets surrounding Jupiter (hemmed in).\n"
            "2. Mercury+Jupiter+Venus conjunct in H9.\n"
            "3. Mercury+Venus+Rahu (enemies of Jupiter) conjunct in H9.\n"
            "4. Moon+Rahu conjunct in any house AND Mercury in H9."
        ),
        remedies  = [],
        domains   = DOMAINS_LONGEVITY,
        tags      = ["short_life", "dosha", "jupiter", "h9", "indicators"],
        planets   = ["Mercury", "Jupiter", "Venus", "Rahu", "Moon"],
        houses    = [9],
        extra_cond = {},
        now       = now,
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6: Physical Metric Engine (5 rules)
# ─────────────────────────────────────────────────────────────────────────────

def build_physical_metrics(now):
    rules = []

    # Height table (concise mapping format to stay within read window)
    rules.append(_doc(
        rule_id   = "lalkitab-ch24-physical-height",
        name      = "Height-to-Age Ratio Engine — Angul Scale (90-108 Anguls)",
        rtype     = "general_principle",
        sub_type  = "physical_metric",
        checkable = False,
        yoga_type = "manual",
        text      = (
            "Standard: 48 angul = 36 inches. Formula: each angul above 90 adds 5 years. "
            "Scale: 90→30yr, 91→35yr, 92→40yr, 93→45yr, 94→50yr, 95→55yr, 96→60yr, "
            "97→65yr, 98→70yr, 99→75yr, 100→80yr, 101→85yr, 102→90yr, 103→95yr, "
            "104→100yr, 105→105yr, 106→110yr, 107→115yr, 108→120yr."
        ),
        remedies  = [],
        domains   = ["longevity", "physical_diagnosis"],
        tags      = ["height", "angul", "physical_metric", "age_engine"],
        planets   = [],
        houses    = [],
        extra_cond = {
            "measurement_unit": "angul",
            "baseline": {"anguls": 90, "years": 30},
            "increment": {"per_angul": 1, "years_added": 5},
            "maximum": {"anguls": 108, "years": 120},
        },
        now       = now,
    ))

    # Maniband lines
    rules.append(_doc(
        rule_id   = "lalkitab-ch24-physical-maniband",
        name      = "Maniband (Wrist) Lines — 1 Line=30yr, 2=60yr, 3=90yr, 4=120yr",
        rtype     = "general_principle",
        sub_type  = "physical_metric",
        checkable = False,
        yoga_type = "manual",
        text      = (
            "Count the lines at the start of the palm (wrist area). "
            "Each complete wrist line represents a 30-year lifecycle block: "
            "1 line → 30 years, 2 lines → 60 years, 3 lines → 90 years, 4 lines → 120 years."
        ),
        remedies  = [],
        domains   = ["longevity", "physical_diagnosis"],
        tags      = ["maniband", "wrist_lines", "palm", "physical_metric", "age_engine"],
        planets   = [],
        houses    = [],
        extra_cond = {
            "measurement": "maniband_lines",
            "scale": {1: 30, 2: 60, 3: 90, 4: 120},
        },
        now       = now,
    ))

    # Forehead whole lines
    rules.append(_doc(
        rule_id   = "lalkitab-ch24-physical-forehead-whole",
        name      = "Forehead Lines — Whole Lines Gender-Specific Age Table",
        rtype     = "general_principle",
        sub_type  = "physical_metric",
        checkable = False,
        yoga_type = "manual",
        text      = (
            "Whole forehead lines (gender-specific): "
            "0 lines: male=100yr. "
            "1 line: male=20yr, female=40yr. "
            "2 lines: male=30yr, female=60yr. "
            "3 lines: male=60yr, female=70yr. "
            "4 lines: male=80yr, female=80yr. "
            "5 lines: male=100yr, female=100yr. "
            "6 lines: male=120yr, female=80yr."
        ),
        remedies  = [],
        domains   = ["longevity", "physical_diagnosis"],
        tags      = ["forehead", "whole_lines", "gender_specific", "physical_metric"],
        planets   = [],
        houses    = [],
        extra_cond = {
            "line_type": "whole",
            "scale": {
                0: {"male": 100},
                1: {"male": 20, "female": 40},
                2: {"male": 30, "female": 60},
                3: {"male": 60, "female": 70},
                4: {"male": 80, "female": 80},
                5: {"male": 100, "female": 100},
                6: {"male": 120, "female": 80},
            },
        },
        now       = now,
    ))

    # Forehead broken lines
    rules.append(_doc(
        rule_id   = "lalkitab-ch24-physical-forehead-broken",
        name      = "Forehead Lines — Broken Lines (Reduced Lifespan) Gender Table",
        rtype     = "general_principle",
        sub_type  = "physical_metric",
        checkable = False,
        yoga_type = "manual",
        text      = (
            "Broken (incomplete) forehead lines carry significantly lower age markers: "
            "1 broken line: male=10yr, female=20yr. "
            "2 broken lines: male=30yr, female=40yr."
        ),
        remedies  = [],
        domains   = ["longevity", "physical_diagnosis"],
        tags      = ["forehead", "broken_lines", "gender_specific", "physical_metric"],
        planets   = [],
        houses    = [],
        extra_cond = {
            "line_type": "broken",
            "scale": {
                1: {"male": 10, "female": 20},
                2: {"male": 30, "female": 40},
            },
        },
        now       = now,
    ))

    # Forehead ear-to-ear lines
    rules.append(_doc(
        rule_id   = "lalkitab-ch24-physical-forehead-ear-to-ear",
        name      = "Forehead Lines — Ear-to-Ear Whole Lines (1=100yr, 2=70yr)",
        rtype     = "general_principle",
        sub_type  = "physical_metric",
        checkable = False,
        yoga_type = "manual",
        text      = (
            "Whole forehead lines that reach ear-to-ear carry special longevity markers: "
            "1 ear-to-ear line → 100 years. "
            "2 ear-to-ear lines → 70 years."
        ),
        remedies  = [],
        domains   = ["longevity", "physical_diagnosis"],
        tags      = ["forehead", "ear_to_ear", "whole_lines", "physical_metric"],
        planets   = [],
        houses    = [],
        extra_cond = {
            "line_type": "whole_ear_to_ear",
            "scale": {1: 100, 2: 70},
        },
        now       = now,
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7: Special Effect Cycles (5 rules)
# ─────────────────────────────────────────────────────────────────────────────

def build_special_effects(now):
    rules = []

    rules.append(_doc(
        rule_id   = "lalkitab-ch24-effect-sun-h4-exalted",
        name      = "Sun in H4 Exalted/Lord — Self-Employment + House/Vehicle at Age 22",
        rtype     = "planetary_combination",
        sub_type  = "age_effect",
        checkable = True,
        yoga_type = "planet_in_house",
        text      = (
            "Sun in the 4th house (exalted state or as H4 lord): at age 22 the native "
            "starts self-employment and gains a house and vehicle. This is a milestone "
            "prosperity trigger at the Sun's maturity-aligned age."
        ),
        remedies  = [],
        domains   = ["career", "property", "timing"],
        tags      = ["sun", "h4", "exalted", "age_22", "self_employment", "property"],
        planets   = ["Sun"],
        houses    = [4],
        extra_cond = {"effect_age": 22, "state": "exalted", "outcome": "self_employment_and_assets"},
        now       = now,
    ))

    rules.append(_doc(
        rule_id   = "lalkitab-ch24-effect-sun-h4-debil",
        name      = "Sun in H4 Debilitated — Inauspicious Career + Mother Affliction",
        rtype     = "planetary_combination",
        sub_type  = "age_effect",
        checkable = True,
        yoga_type = "planet_in_house",
        text      = (
            "Sun in the 4th house (debilitated state): inauspicious effect on career "
            "and assets; simultaneous affliction to the mother. Opposite outcome to "
            "the exalted Sun H4 rule."
        ),
        remedies  = [],
        domains   = ["career", "property", "mother"],
        tags      = ["sun", "h4", "debilitated", "career", "mother_affliction"],
        planets   = ["Sun"],
        houses    = [4],
        extra_cond = {"state": "debilitated", "outcome": "career_loss_and_mother_affliction"},
        now       = now,
    ))

    rules.append(_doc(
        rule_id   = "lalkitab-ch24-effect-moon-h7",
        name      = "Moon in H7 Exalted/Lord — Marriage at Age 24",
        rtype     = "planetary_combination",
        sub_type  = "age_effect",
        checkable = True,
        yoga_type = "planet_in_house",
        text      = (
            "Moon in the 7th house (exalted or as H7 lord): the native marries in "
            "the 24th year. Aligned with Moon's maturity age of 24."
        ),
        remedies  = [],
        domains   = ["marriage", "timing"],
        tags      = ["moon", "h7", "exalted", "age_24", "marriage"],
        planets   = ["Moon"],
        houses    = [7],
        extra_cond = {"effect_age": 24, "state": "exalted", "outcome": "marriage"},
        now       = now,
    ))

    rules.append(_doc(
        rule_id   = "lalkitab-ch24-effect-saturn-h4",
        name      = "Saturn in H4 Exalted/Lord — Land Proprietary",
        rtype     = "planetary_combination",
        sub_type  = "age_effect",
        checkable = True,
        yoga_type = "planet_in_house",
        text      = (
            "Saturn in the 4th house (exalted or as H4 lord): facilitates proprietary "
            "of land — the native gains or inherits land/property. Saturn's slow "
            "nature ensures this manifests steadily over time."
        ),
        remedies  = [],
        domains   = ["property", "land", "timing"],
        tags      = ["saturn", "h4", "exalted", "land", "property"],
        planets   = ["Saturn"],
        houses    = [4],
        extra_cond = {"state": "exalted", "outcome": "land_proprietary"},
        now       = now,
    ))

    rules.append(_doc(
        rule_id   = "lalkitab-ch24-effect-rahu-h9",
        name      = "Rahu in H9 — Luck Rises After Age 42",
        rtype     = "planetary_combination",
        sub_type  = "age_effect",
        checkable = True,
        yoga_type = "planet_in_house",
        text      = (
            "Rahu in the 9th house: luck rises significantly after the native reaches "
            "the age of 42 — aligned with Rahu's maturity age of 42. The 9th house "
            "is the house of fortune; Rahu's late activation here signals a delayed "
            "but strong lucky period in the second half of life."
        ),
        remedies  = [],
        domains   = ["luck", "timing", "fortune"],
        tags      = ["rahu", "h9", "age_42", "luck", "fortune"],
        planets   = ["Rahu"],
        houses    = [9],
        extra_cond = {"effect_age": 42, "outcome": "luck_rises"},
        now       = now,
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 8: Foundational Placement Logic (3 rules)
# ─────────────────────────────────────────────────────────────────────────────

def build_foundational(now):
    rules = []

    rules.append(_doc(
        rule_id   = "lalkitab-ch24-foundation-beneficence",
        name      = "General House Beneficence — H4/H9 Benefic Pass for Malefics",
        rtype     = "general_principle",
        sub_type  = "foundational",
        checkable = False,
        yoga_type = "manual",
        text      = (
            "Any planet placed in H4 or H9 receives a 'Benefic Pass' regardless of "
            "its natural malefic status, provided it is not severely debilitated. "
            "This environmental logic override means Mars, Saturn, Rahu, Ketu, and "
            "Sun in H4 or H9 are treated as conferring good effects in this engine."
        ),
        remedies  = [],
        domains   = ["general", "longevity"],
        tags      = ["benefic_pass", "h4", "h9", "malefic_override", "foundational"],
        planets   = [],
        houses    = [4, 9],
        extra_cond = {},
        now       = now,
    ))

    rules.append(_doc(
        rule_id   = "lalkitab-ch24-foundation-exaltation-principle",
        name      = "Exaltation/Debilitation Principle — State Determines Outcome",
        rtype     = "general_principle",
        sub_type  = "foundational",
        checkable = False,
        yoga_type = "manual",
        text      = (
            "Universal modifier: if any planet is exalted, its outcome is auspicious; "
            "if debilitated, its outcome is an affliction. The Moon-House Exaltation "
            "Principle applies to all planetary placements in the age determination "
            "engine — state overrides house placement in the final prediction."
        ),
        remedies  = [],
        domains   = ["general", "longevity"],
        tags      = ["exaltation", "debilitation", "state_modifier", "foundational"],
        planets   = [],
        houses    = [],
        extra_cond = {},
        now       = now,
    ))

    rules.append(_doc(
        rule_id   = "lalkitab-ch24-foundation-debilitation-clock",
        name      = "Debilitation Clock — Malefic Count Starts 1 Month After Birth",
        rtype     = "general_principle",
        sub_type  = "foundational",
        checkable = False,
        yoga_type = "manual",
        text      = (
            "Precision counting rule: for debilitated planets, the malefic effect "
            "countdown does NOT start at birth — it starts specifically 1 month after "
            "the date of birth. The 'Debilitation Clock' is offset by one month for "
            "precise timing of afflictions."
        ),
        remedies  = [],
        domains   = ["general", "timing", "longevity"],
        tags      = ["debilitation_clock", "timing", "one_month_offset", "foundational"],
        planets   = [],
        houses    = [],
        extra_cond = {"clock_offset_months": 1},
        now       = now,
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def build_all_rules() -> list[dict]:
    now   = datetime.now(timezone.utc).isoformat()
    rules: list[dict] = []
    rules.extend(build_moon_house(now))         # 12
    rules.extend(build_moon_modifiers(now))     #  4
    rules.extend(build_luck_maturity(now))      #  3
    rules.extend(build_mortality_symptoms(now)) #  5
    rules.extend(build_complex_age(now))        # 12
    rules.extend(build_physical_metrics(now))   #  5
    rules.extend(build_special_effects(now))    #  5
    rules.extend(build_foundational(now))       #  3
    return rules                                # 49 total


def main() -> None:
    parser = argparse.ArgumentParser()
    group  = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--upload",  metavar="JSON_FILE")
    parser.add_argument("--save",   metavar="JSON_FILE")
    parser.add_argument("--mongo-url")
    parser.add_argument("--db-name", default="horoscope_db")
    args = parser.parse_args()

    if args.dry_run:
        rules = build_all_rules()
        print(f"Dry run: {len(rules)} rules generated\n")
        checkable = sum(1 for r in rules if r["condition"]["yoga_check"]["checkable"])
        print(f"  Checkable: {checkable} / {len(rules)}\n")
        for r in rules:
            ck = "✓" if r["condition"]["yoga_check"]["checkable"] else "·"
            st = r["condition"]["sub_type"]
            print(f"  {ck} {r['rule_id']:55s} [{st}]")
        if args.save:
            Path(args.save).write_text(json.dumps(rules, indent=2, ensure_ascii=False))
            print(f"\nSaved → {args.save}")
        return

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
