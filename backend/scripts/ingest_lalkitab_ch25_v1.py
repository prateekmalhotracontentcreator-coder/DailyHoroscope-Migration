#!/usr/bin/env python3
"""
ingest_lalkitab_ch25_v1.py — Lal Kitab Chapter 25: Remedial Measures for Planetary Dosh

35 rules across 12 builder functions.
BATCH_ID: lalkitab-ch25-v1-20260505

Source files:
  Lal Kitab_Ch 25_JSON Ready.md (V8 + Final Expansion)
  Lal Kitab_Ch 25_Diagnostic.md

Rule groups:
  Foundations        (1): significators-aries-base
  Sun                (3): affliction, h7, h10
  Moon               (6): affliction, h1, h3, mother, h10, h11
  Mars               (3): affliction, h2, h9
  Mercury            (3): affliction, h7, h1
  Jupiter            (2): affliction, h12
  Venus              (1): affliction
  Saturn             (3): affliction, h5-sun-leo, h10-h4-benefit
  Rahu               (2): affliction, h8
  Ketu               (1): affliction
  Conjunctions       (7): jup-sun-financial, sun-sat-wife-health, sun-sat-property,
                          sun-sat-gold-loss, sun-rahu-eclipse, moon-rahu-eclipse,
                          mars-mercury-sister
  General Principles (3): daytime-conjunction-rule, sun-friend-cooperation,
                          donation-modesty

New schema fields introduced in this batch:
  condition.symptoms          — list of physical/social symptoms indicating affliction
  condition.diagnostic_markers — embedded in sun-affliction (salt intake ↔ Sun strength)
  condition.affliction_of     — 'mother' / 'wife' / 'sister' / 'son' for relational rules
  condition.trigger           — 'solar_eclipse' / 'lunar_eclipse' / 'financial_difficulty'
                                / 'construction'
  condition.yoga_check        — {"type": ..., "checkable": bool}
  interpretation.remedies     — list of {category, action} dicts
  interpretation.deity        — presiding deity name
  interpretation.mantra       — mantra text
  interpretation.mechanism    — explanatory note on WHY the remedy works

Workflow:
  # Dry run + save:
  python3 scripts/ingest_lalkitab_ch25_v1.py --dry-run --save scripts/lalkitab_ch25_rules.json

  # Upload:
  python3 scripts/ingest_lalkitab_ch25_v1.py \\
    --upload scripts/lalkitab_ch25_rules.json \\
    --mongo-url "$MONGO_URL" --db-name horoscope_db

  # Validate:
  python3 scripts/validate_rules.py \\
    --mongo-url "$MONGO_URL" --db-name horoscope_db \\
    --batch-id lalkitab-ch25-v1-20260505
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
CHAPTER   = 25
CHAP_NAME = "Remedial Measures for Planetary Dosh (Evil Effects)"
BATCH_ID  = "lalkitab-ch25-v1-20260505"

DOMAINS_REMEDY  = ["remedies", "health", "wellbeing"]
DOMAINS_HEALTH  = ["health", "remedies"]
DOMAINS_FAMILY  = ["family", "remedies", "relationships"]
DOMAINS_FINANCE = ["finance", "remedies", "wealth"]
DOMAINS_GENERAL = ["remedies", "general_principles"]


# ─────────────────────────────────────────────────────────────────────────────
# Base document builder
# ─────────────────────────────────────────────────────────────────────────────

def _base(rule_id: str, now: str) -> dict:
    return {
        "rule_id":        rule_id,
        "science_id":     SCIENCE,
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
         text, remedies, domains, tags, planets, houses, extra_cond,
         now, deity=None, mantra=None, mechanism=None,
         symptoms=None, physical_markers=None):
    doc = _base(rule_id, now)
    yc: dict = {"type": yoga_type, "checkable": checkable}
    if not checkable:
        yc["description"] = "Requires contextual / ritual / diagnostic judgment — not automatable in Phase 1."
    cond: dict = {"type": rtype, "sub_type": sub_type, "yoga_check": yc}
    if planets:
        cond["planets_involved"] = planets
    if houses:
        cond["houses_involved"] = houses
    if symptoms:
        cond["symptoms"] = symptoms
    cond.update(extra_cond)

    interp: dict = {
        "summary":            name,
        "detailed":           text,
        "full_text_passages": [{"text": text, "confidence": "HIGH"}],
        "remedies":           remedies,
        "life_domain":        domains[0],
        "life_domains":       domains,
        "tags":               tags,
        "physical_markers":   physical_markers or [],
    }
    if deity:
        interp["deity"]    = deity
    if mantra:
        interp["mantra"]   = mantra
    if mechanism:
        interp["mechanism"] = mechanism

    has_phys = bool(physical_markers)
    doc.update({
        "condition": cond,
        "interpretation": interp,
        "metadata": {
            "planets_involved":     planets or [],
            "houses_involved":      houses or [],
            "signs_involved":       [],
            "condition_count":      1,
            "gender_context":       "neutral",
            "is_group_summary":     False,
            "has_physical_markers": has_phys,
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
# GROUP 1: Foundations (1 rule)
# ─────────────────────────────────────────────────────────────────────────────

def build_foundations(now):
    rules = []

    # LU 25.1 — House significators + Aries-base rule
    significator_map = {
        "H1": "Sun", "H2": "Jupiter", "H3": "Mars", "H4": "Moon",
        "H5": "Jupiter", "H6": "Ketu", "H7": "Venus",
        "H8": ["Saturn", "Mars"], "H9": "Jupiter",
        "H10": "Saturn", "H11": "Jupiter", "H12": "Rahu",
    }
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-significators-aries-base",
        name       = "Lal Kitab Permanent House Significators (Aries Ascendant Rule)",
        rtype      = "general_principle",
        sub_type   = "foundational",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "In Lal Kitab, predictions are made by permanently fixing the ascendant as Aries, "
            "regardless of the native's natural ascendant. Permanent house significators: "
            "H1=Sun, H2=Jupiter, H3=Mars, H4=Moon, H5=Jupiter, H6=Ketu, H7=Venus, "
            "H8=Saturn/Mars, H9=Jupiter, H10=Saturn, H11=Jupiter, H12=Rahu. "
            "When a planet afflicts a specific house, remedies may involve the objects of "
            "EITHER the afflicting planet OR the house's permanent significator (the "
            "'Significator Swap' methodology)."
        ),
        remedies   = [],
        domains    = DOMAINS_GENERAL,
        tags       = ["significators", "aries_base", "foundational", "remedy_framework"],
        planets    = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"],
        houses     = list(range(1, 13)),
        extra_cond = {
            "significator_map":    significator_map,
            "aries_base_rule":     True,
            "significator_swap":   (
                "If planet afflicts H1 (significator=Sun, lord=Mars/Aries), "
                "remedy may use Mars objects rather than Sun objects."
            ),
        },
        now        = now,
        mechanism  = (
            "Lal Kitab uses permanent (non-moving) house ownership based on Aries ascendant. "
            "This fixed map underlies all house-modifier remedy selection in this chapter."
        ),
    ))
    return rules


# ─────────────────────────────────────────────────────────────────────────────
# GROUP 2: Sun Rules (3 rules)
# LU 25.2: General Sun affliction (diagnostic markers embedded)
# LU 25.3: Sun H7, Sun H10
# ─────────────────────────────────────────────────────────────────────────────

def build_sun(now):
    rules = []

    # LU 25.2 — General Sun affliction
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-sun-affliction",
        name       = "Sun Affliction — Symptoms, Diagnostic Marker, and Remedies",
        rtype      = "dosha",
        sub_type   = "affliction",
        checkable  = False,
        yoga_type  = "planet_weak",
        text       = (
            "When Sun is afflicted (weak, debilitated, combust, or malefic-aspected): "
            "Symptoms: right eye pain, heart attack / cardiac issue, abdominal dysfunction, "
            "financial loss. "
            "Dietary diagnostic marker: native eats MORE salt when Sun is weak; eats LESS salt "
            "when Sun is exalted/strong. "
            "Remedies: donate jaggery (prepared as gulguley), wheat, or copper utensils; "
            "perform yajna; offer water to Sun at dawn; chant 'Vishnusahashra namawali' "
            "from 'Harivansh Puran'. Deity: Lord Vishnu."
        ),
        remedies   = [
            {"category": "offering", "action": "Donate jaggery (prepared as gulguley), wheat, or copper utensils"},
            {"category": "ritual",   "action": "Perform yajna"},
            {"category": "ritual",   "action": "Offer water to Sun at dawn each morning"},
            {"category": "mantra",   "action": "Chant 'Vishnusahashra namawali' from 'Harivansh Puran'"},
        ],
        domains    = DOMAINS_HEALTH,
        tags       = ["Sun", "affliction", "dosha", "right_eye", "heart", "yajna", "Vishnu"],
        planets    = ["Sun"],
        houses     = [],
        extra_cond = {
            "diagnostic_markers": {
                "high_salt_intake": "Sun is weak/afflicted",
                "low_salt_intake":  "Sun is exalted/strong",
            },
        },
        now        = now,
        deity      = "Lord Vishnu",
        mantra     = "Vishnusahashra namawali from Harivansh Puran",
        symptoms   = ["Right eye pain", "Heart attack / cardiac issue", "Abdominal dysfunction", "Financial loss"],
    ))

    # LU 25.3 — Sun in H7
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-sun-h7",
        name       = "Sun in H7 — Particularly Inauspicious State and Fire-Milk Remedy",
        rtype      = "planetary_combination",
        sub_type   = "house_modifier",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "Sun placed in the 7th house is in a particularly inauspicious and debilitated "
            "state (H7 = Venus's house; Venus and Sun are enemies). "
            "Remedy A: Put out fire with milk at night (Water/Moon calms Fire/Sun). "
            "Remedy B: Habitually put sweets in the mouth followed by drinking water "
            "(cooperation of Mars and Moon — friends of Sun — to calm the affliction)."
        ),
        remedies   = [
            {"category": "ritual",  "action": "Extinguish fire with milk at night"},
            {"category": "ritual",  "action": "Habitually eat sweets then drink water (Mars+Moon cooperation to calm Sun)"},
        ],
        domains    = DOMAINS_HEALTH,
        tags       = ["Sun", "H7", "house_modifier", "fire_milk", "inauspicious"],
        planets    = ["Sun"],
        houses     = [7],
        extra_cond = {
            "planet":        "Sun",
            "house":         7,
            "house_lord":    "Venus",
            "enmity_note":   "Venus and Sun are natural enemies — H7 placement intensifies Sun's malefic effect",
        },
        now        = now,
        mechanism  = "Sun (Fire) is calmed by Moon (Water/Milk) and Mars (Sweets/Honey) — its natural friends.",
    ))

    # LU 25.3 — Sun in H10
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-sun-h10",
        name       = "Sun in H10 — Copper Coins in Flowing Water Remedy",
        rtype      = "planetary_combination",
        sub_type   = "house_modifier",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "Sun placed in the 10th house (career/action house). "
            "Remedy: Drop copper coins in flowing water. "
            "Symbolic logic: Copper = Sun's metal; Moveable Sign / Flowing Water = kinetic "
            "energy that disperses the Sun's pent-up malefic force."
        ),
        remedies   = [
            {"category": "offering", "action": "Drop copper coins in flowing water (river or stream)"},
        ],
        domains    = DOMAINS_HEALTH,
        tags       = ["Sun", "H10", "house_modifier", "copper", "flowing_water"],
        planets    = ["Sun"],
        houses     = [10],
        extra_cond = {
            "planet":     "Sun",
            "house":      10,
            "house_lord": "Saturn",
        },
        now        = now,
        mechanism  = "Copper = Sun's metal. Flowing water (moveable sign) disperses accumulated malefic force.",
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# GROUP 3: Moon Rules (6 rules)
# LU 25.4: General Moon affliction
# LU 25.5: Moon H1, H3, Mother, H10, H11
# ─────────────────────────────────────────────────────────────────────────────

def build_moon(now):
    rules = []

    # LU 25.4 — General Moon affliction
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-moon-affliction",
        name       = "Moon Affliction — Symptoms and Remedies (Shiva)",
        rtype      = "dosha",
        sub_type   = "affliction",
        checkable  = False,
        yoga_type  = "planet_weak",
        text       = (
            "When Moon is afflicted: Symptoms: mother ill, mental worry / weakness, "
            "lung-related disease, depreciating wealth. "
            "Remedies: Float silver in the river; keep a pot of water or milk at the "
            "headpost during sleep and pour it on a Peepal tree in the morning. "
            "Lord: Lord Shiva. Ritual: Perform 'Rudrabhisheka' or chant 'Shiv Mahinm "
            "Strotra'; sprinkle holy water on Shiva idol."
        ),
        remedies   = [
            {"category": "offering", "action": "Float silver in the river"},
            {"category": "ritual",   "action": "Keep pot of water or milk at headpost during sleep; pour on Peepal tree in morning"},
            {"category": "ritual",   "action": "Perform Rudrabhisheka"},
            {"category": "mantra",   "action": "Chant 'Shiv Mahinm Strotra'; sprinkle holy water on Shiva"},
        ],
        domains    = DOMAINS_HEALTH,
        tags       = ["Moon", "affliction", "dosha", "mother", "lungs", "Shiva", "silver"],
        planets    = ["Moon"],
        houses     = [],
        extra_cond = {},
        now        = now,
        deity      = "Lord Shiva",
        mantra     = "Shiv Mahinm Strotra",
        symptoms   = ["Mother ill", "Mental worry / weakness", "Lung-related disease", "Depreciating wealth"],
    ))

    # LU 25.5 — Moon H1
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-moon-h1",
        name       = "Moon Afflicting in H1 — Do Not Sell Milk",
        rtype      = "planetary_combination",
        sub_type   = "house_modifier",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "Moon afflicting in the 1st house (Ascendant). "
            "Prohibition: Do NOT sell milk (selling milk = becoming bereft of Moon's mercy). "
            "Remedy: Cleanse self with natural water; keep rice and silver close."
        ),
        remedies   = [
            {"category": "succour",  "action": "Do NOT sell milk — this depletes Moon's mercy"},
            {"category": "ritual",   "action": "Spruce/cleanse self with natural water, rice, and silver"},
        ],
        domains    = DOMAINS_HEALTH,
        tags       = ["Moon", "H1", "house_modifier", "milk_prohibition", "silver", "rice"],
        planets    = ["Moon"],
        houses     = [1],
        extra_cond = {
            "planet":      "Moon",
            "house":       1,
            "prohibition": "Do not sell milk",
        },
        now        = now,
        mechanism  = "Selling milk = surrendering Moon's nurturing energy; prohibition preserves Moon's grace.",
    ))

    # LU 25.5 — Moon H3
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-moon-h3",
        name       = "Moon Afflicting in H3 — Donate Green Clothes to Maidens",
        rtype      = "planetary_combination",
        sub_type   = "house_modifier",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "Moon afflicting in the 3rd house. "
            "Remedy: Donate green clothes to maidens (succour Mercury — H3 significator is Mars, "
            "but green = Mercury's color; this provides Mercury succour to stabilise the house)."
        ),
        remedies   = [
            {"category": "succour", "action": "Donate green clothes to maidens (Mercury succour for H3 stabilisation)"},
        ],
        domains    = DOMAINS_FAMILY,
        tags       = ["Moon", "H3", "house_modifier", "green_clothes", "Mercury_succour"],
        planets    = ["Moon"],
        houses     = [3],
        extra_cond = {
            "planet":       "Moon",
            "house":        3,
            "house_lord":   "Mars",
            "succour_planet": "Mercury",
        },
        now        = now,
    ))

    # LU 25.5 — Moon afflicting Mother (relational, not house-specific)
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-moon-mother",
        name       = "Moon Afflicting Mother — Milk Prohibition and Free Milk Offering",
        rtype      = "general_principle",
        sub_type   = "relational_modifier",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "When Moon is afflicting the native's mother (causing mother's illness). "
            "Prohibition: Do NOT use or drink milk at night. "
            "Remedy: Offering milk free of cost to others is excellent — it reverses the "
            "Moon-milk depletion dynamic and restores Moon's benefic energy."
        ),
        remedies   = [
            {"category": "succour",  "action": "Do NOT use or drink milk at night"},
            {"category": "offering", "action": "Offer milk free of cost to others — reverses Moon-milk depletion"},
        ],
        domains    = DOMAINS_FAMILY,
        tags       = ["Moon", "mother", "relational_modifier", "milk_prohibition", "free_milk"],
        planets    = ["Moon"],
        houses     = [],
        extra_cond = {
            "affliction_of": "mother",
            "prohibition":   "Do not use or drink milk at night",
        },
        now        = now,
        mechanism  = "Moon governs milk/mother. Charging for milk when Moon afflicts mother worsens the depletion. Gifting milk reverses it.",
    ))

    # LU 25.5 — Moon H10
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-moon-h10",
        name       = "Moon Afflicting in H10 — Do Not Drink Milk at Night",
        rtype      = "planetary_combination",
        sub_type   = "house_modifier",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "Moon afflicting in the 10th house (career/Saturn's house). "
            "Prohibition: Do NOT drink milk at night."
        ),
        remedies   = [
            {"category": "succour", "action": "Do NOT drink milk at night"},
        ],
        domains    = DOMAINS_HEALTH,
        tags       = ["Moon", "H10", "house_modifier", "milk_prohibition", "night"],
        planets    = ["Moon"],
        houses     = [10],
        extra_cond = {
            "planet":      "Moon",
            "house":       10,
            "house_lord":  "Saturn",
            "prohibition": "Do not drink milk at night",
        },
        now        = now,
    ))

    # LU 25.5 — Moon H11 + Birth Protocol
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-moon-h11",
        name       = "Moon Afflicting in H11 — Bhairav Temple and 52-Day Birth Protocol",
        rtype      = "planetary_combination",
        sub_type   = "house_modifier",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "Moon afflicting in the 11th house. "
            "Remedy: Visit Bhairav temple and offer milk. "
            "Birth Protocol (52-Day Rule): Moon in H11 aspects the 5th house (children). "
            "Because Moon signifies the mother, her presence during birth creates a malefic "
            "aspect on the child. Correction: The wife/mother must change locations during "
            "labor and must avoid looking at the newborn child's face for 52 days to break "
            "the aspectual cycle."
        ),
        remedies   = [
            {"category": "ritual",   "action": "Visit Bhairav temple and offer milk"},
            {"category": "succour",  "action": "Wife must change location during labor (breaks Moon H11 → H5 malefic aspect on child)"},
            {"category": "succour",  "action": "Wife must avoid looking at newborn's face for 52 days after birth"},
        ],
        domains    = DOMAINS_FAMILY,
        tags       = ["Moon", "H11", "house_modifier", "Bhairav", "birth_protocol", "52_days", "children"],
        planets    = ["Moon"],
        houses     = [11],
        extra_cond = {
            "planet":            "Moon",
            "house":             11,
            "house_lord":        "Saturn",
            "aspect_house":      5,
            "birth_protocol":    {
                "location_change": "Wife must change location during labor",
                "avoidance_days":  52,
                "avoidance_rule":  "Wife must not look at newborn's face for 52 days",
                "reason":          "Moon H11 aspects H5 (children); mother's gaze during/after birth extends the malefic aspect",
            },
        },
        now        = now,
        mechanism  = "Moon H11 casts an aspect on H5 (children). The mother IS Moon's representative — her physical presence during birth prolongs the malefic aspectual link. 52-day avoidance breaks the cycle.",
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# GROUP 4: Mars Rules (3 rules)
# LU 25.6: General Mars affliction, Mars H2, Mars H9
# ─────────────────────────────────────────────────────────────────────────────

def build_mars(now):
    rules = []

    # LU 25.6 — General Mars affliction
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-mars-affliction",
        name       = "Mars Affliction — Symptoms and Remedies (Hanumanji)",
        rtype      = "dosha",
        sub_type   = "affliction",
        checkable  = False,
        yoga_type  = "planet_weak",
        text       = (
            "When Mars is afflicted: "
            "Remedies: Donate sweet bread prepared in an earthen oven; drop rewari or "
            "batashey (sugar candy) in running water. "
            "Lord: Hanumanji. Ritual: Worship with gur-churma (jaggery+wheat); offer "
            "vermilion and silver foil; take prasad."
        ),
        remedies   = [
            {"category": "offering", "action": "Donate sweet bread prepared in an earthen oven"},
            {"category": "offering", "action": "Drop rewari or batashey (sugar candy) in running water"},
            {"category": "ritual",   "action": "Worship Hanumanji with gur-churma (jaggery + wheat)"},
            {"category": "ritual",   "action": "Offer vermilion and silver foil to Hanumanji; take prasad"},
        ],
        domains    = DOMAINS_HEALTH,
        tags       = ["Mars", "affliction", "dosha", "Hanuman", "rewari", "gur_churma"],
        planets    = ["Mars"],
        houses     = [],
        extra_cond = {},
        now        = now,
        deity      = "Hanumanji",
        symptoms   = [],
    ))

    # LU 25.6 — Mars H2 (Taurus — childlessness)
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-mars-h2",
        name       = "Mars Malefic in H2 — Childlessness Conjunction and Foster Remedy",
        rtype      = "planetary_combination",
        sub_type   = "house_modifier",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "Mars malefic in the 2nd house (Taurus house in Lal Kitab's Aries base): "
            "A 'conjunction of childlessness' occurs — the Mars malefic energy in the "
            "wealth/family house suppresses progeny potential. "
            "Remedy: Foster family members (provide shelter, care, or support to children "
            "of relatives) to mitigate the childlessness effect."
        ),
        remedies   = [
            {"category": "succour", "action": "Foster family members — provide shelter or care to children of relatives"},
        ],
        domains    = DOMAINS_FAMILY,
        tags       = ["Mars", "H2", "house_modifier", "childlessness", "foster", "progeny"],
        planets    = ["Mars"],
        houses     = [2],
        extra_cond = {
            "planet":      "Mars",
            "house":       2,
            "house_lord":  "Jupiter",
            "affliction":  "childlessness_conjunction",
        },
        now        = now,
        mechanism  = "Mars (aggression/fire) in H2 (family/Jupiter's house) blocks Jupiter's progeny-giving function. Fostering acts as a surrogate Jupiter remedy.",
    ))

    # LU 25.6 — Mars H9 (House of Luck)
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-mars-h9",
        name       = "Mars Malefic in H9 — Brother's Wife Must Perform Nursing/Service",
        rtype      = "planetary_combination",
        sub_type   = "house_modifier",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "Mars malefic in the 9th house (House of Luck/Fortune; Jupiter's house). "
            "Remedy: The wife of the native's brother must perform nursing or service "
            "duties for the native. This relational act neutralises Mars's malefic "
            "influence on fortune."
        ),
        remedies   = [
            {"category": "succour", "action": "Brother's wife must perform nursing or service for the native"},
        ],
        domains    = DOMAINS_FAMILY,
        tags       = ["Mars", "H9", "house_modifier", "brothers_wife", "nursing", "luck"],
        planets    = ["Mars"],
        houses     = [9],
        extra_cond = {
            "planet":      "Mars",
            "house":       9,
            "house_lord":  "Jupiter",
            "affliction_of": "fortune",
        },
        now        = now,
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# GROUP 5: Mercury Rules (3 rules)
# LU 25.7: General Mercury affliction, Mercury H7, Mercury H1
# ─────────────────────────────────────────────────────────────────────────────

def build_mercury(now):
    rules = []

    # LU 25.7 — General Mercury affliction
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-mercury-affliction",
        name       = "Mercury Affliction — Social Symptoms and Remedies (Goddess Durga)",
        rtype      = "dosha",
        sub_type   = "affliction",
        checkable  = False,
        yoga_type  = "planet_weak",
        text       = (
            "When Mercury is afflicted: "
            "Remedies: Burn shells and immerse ash in river; immerse pierced copper coins "
            "or holed coins; pierce nose; clean teeth with alum. "
            "If disease is caused by Mercury → Donate bland pumpkin at a religious place. "
            "Lord: Goddess Durga. Mantra: Chant 'Durga Saptshati'; fast during Navratri; "
            "serve maidens."
        ),
        remedies   = [
            {"category": "ritual",   "action": "Burn shells and immerse ash in river"},
            {"category": "offering", "action": "Immerse pierced copper or holed coins in river"},
            {"category": "ritual",   "action": "Pierce nose"},
            {"category": "ritual",   "action": "Clean teeth with alum"},
            {"category": "offering", "action": "If Mercury-caused disease: donate bland pumpkin at a religious place"},
            {"category": "mantra",   "action": "Chant 'Durga Saptshati'; fast during Navratri; serve maidens"},
        ],
        domains    = DOMAINS_HEALTH,
        tags       = ["Mercury", "affliction", "dosha", "Durga", "shells", "alum", "pumpkin"],
        planets    = ["Mercury"],
        houses     = [],
        extra_cond = {},
        now        = now,
        deity      = "Goddess Durga",
        mantra     = "Durga Saptshati",
        symptoms   = ["Sister and aunt (Bua) suffering", "Teeth issues"],
    ))

    # LU 25.7 — Mercury H7 (social symptom)
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-mercury-h7",
        name       = "Mercury in H7 — Sister and Aunt (Bua) Suffer Massively",
        rtype      = "planetary_combination",
        sub_type   = "house_modifier",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "Mercury placed in the 7th house: sister and aunt (Bua — father's sister) "
            "suffer massively. H7 is Venus's house; Mercury's presence here creates "
            "cross-planet tension affecting female relatives signified by both Venus (sisters) "
            "and Mercury (aunts/Bua)."
        ),
        remedies   = [],
        domains    = DOMAINS_FAMILY,
        tags       = ["Mercury", "H7", "house_modifier", "sister", "aunt", "Bua", "suffering"],
        planets    = ["Mercury"],
        houses     = [7],
        extra_cond = {
            "planet":      "Mercury",
            "house":       7,
            "house_lord":  "Venus",
            "affliction_of": ["sister", "aunt_bua"],
        },
        now        = now,
        symptoms   = ["Sister suffers massively", "Aunt (Bua / father's sister) suffers massively"],
    ))

    # LU 25.7 — Mercury H1 (Ascendant — Significator Swap)
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-mercury-h1",
        name       = "Mercury Afflicting in H1 — Donate Objects of Mars (Significator Swap)",
        rtype      = "planetary_combination",
        sub_type   = "house_modifier",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "Mercury afflicting in the 1st house (Ascendant). "
            "Remedy: Donate objects of Mars (H1 lord under Aries-base rule). "
            "Significator swap logic: H1 significator = Sun; H1 lord = Mars (Aries). "
            "Donating Mars objects (red items, coral, honey, sugar) pacifies Mercury's "
            "affliction of the Ascendant."
        ),
        remedies   = [
            {"category": "offering", "action": "Donate objects of Mars (red items, coral, honey, sugar, masoor dal)"},
        ],
        domains    = DOMAINS_HEALTH,
        tags       = ["Mercury", "H1", "house_modifier", "significator_swap", "Mars_objects"],
        planets    = ["Mercury"],
        houses     = [1],
        extra_cond = {
            "planet":              "Mercury",
            "house":               1,
            "house_significator":  "Sun",
            "house_lord_aries":    "Mars",
            "remedy_planet":       "Mars",
            "significator_swap":   True,
        },
        now        = now,
        mechanism  = "H1 under Aries-base is ruled by Mars (Aries). Donating Mars objects supplies the energy the afflicted house needs to push back against Mercury.",
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# GROUP 6: Jupiter Rules (2 rules)
# LU 25.8: General Jupiter affliction, Jupiter H12
# ─────────────────────────────────────────────────────────────────────────────

def build_jupiter(now):
    rules = []

    # LU 25.8 — General Jupiter affliction
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-jupiter-affliction",
        name       = "Jupiter Affliction — Progeny/Financial Symptoms and Remedies (Lord Brahma)",
        rtype      = "dosha",
        sub_type   = "affliction",
        checkable  = False,
        yoga_type  = "planet_weak",
        text       = (
            "When Jupiter is afflicted: Symptoms include childlessness, financial difficulty, "
            "spiritual decline. "
            "Remedies: Collect one paisa from every blood relation and donate at a temple; "
            "plant Peepal trees; donate saffron, turmeric, gold, gram pulse (chana dal), "
            "yellow cloth, or books. "
            "Lord: Lord Brahma. If childless due to Jupiter affliction → Worship 'Shri Hari'."
        ),
        remedies   = [
            {"category": "offering", "action": "Collect one paisa from every blood relation and donate at a temple"},
            {"category": "ritual",   "action": "Plant Peepal trees"},
            {"category": "offering", "action": "Donate saffron, turmeric, gold, gram pulse (chana dal), yellow cloth, or books"},
            {"category": "ritual",   "action": "If childless due to Jupiter: Worship 'Shri Hari'"},
        ],
        domains    = ["family", "finance", "remedies", "spirituality"],
        tags       = ["Jupiter", "affliction", "dosha", "Brahma", "Peepal", "saffron", "childlessness"],
        planets    = ["Jupiter"],
        houses     = [],
        extra_cond = {},
        now        = now,
        deity      = "Lord Brahma",
        symptoms   = ["Childlessness", "Financial difficulty", "Spiritual decline"],
    ))

    # LU 25.8 — Jupiter H12
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-jupiter-h12",
        name       = "Jupiter Afflicting in H12 — Gram/Saffron/Gold at Night (Post-Father's Death)",
        rtype      = "planetary_combination",
        sub_type   = "house_modifier",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "Jupiter afflicting in the 12th house. "
            "Remedy: Keep gram (chana), saffron, and gold close to self during the night "
            "to ensure sound sleep and restore Jupiter's protective energy. "
            "IMPORTANT CONDITION: This remedy is applicable ONLY after the death of the "
            "father or grandfather — not before."
        ),
        remedies   = [
            {"category": "succour", "action": "Keep gram (chana), saffron, and gold close during night for sound sleep — ONLY after death of father or grandfather"},
        ],
        domains    = DOMAINS_HEALTH,
        tags       = ["Jupiter", "H12", "house_modifier", "gram", "saffron", "gold", "night_remedy"],
        planets    = ["Jupiter"],
        houses     = [12],
        extra_cond = {
            "planet":              "Jupiter",
            "house":               12,
            "house_lord":          "Rahu",
            "conditional_trigger": "Only applicable after death of father or grandfather",
        },
        now        = now,
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# GROUP 7: Venus Rules (1 rule)
# LU 25.9: General Venus affliction
# ─────────────────────────────────────────────────────────────────────────────

def build_venus(now):
    rules = []

    rules.append(_doc(
        rule_id    = "lalkitab-ch25-venus-affliction",
        name       = "Venus Affliction — Remedies (Goddess Lakshmi)",
        rtype      = "dosha",
        sub_type   = "affliction",
        checkable  = False,
        yoga_type  = "planet_weak",
        text       = (
            "When Venus is afflicted: "
            "Remedies: Spare food from meals to feed cows; donate ghee, curd, camphor, "
            "items of makeup, and pearls. "
            "Succour: Offer support to a female native in need. "
            "Lord: Goddess Lakshmi. Mantra: Worship Lakshmi and chant 'Shri Sookt'."
        ),
        remedies   = [
            {"category": "offering", "action": "Spare food from meals to feed cows"},
            {"category": "offering", "action": "Donate ghee, curd, camphor, makeup items, and pearls"},
            {"category": "succour",  "action": "Offer support or assistance to a female native in need"},
            {"category": "mantra",   "action": "Worship Goddess Lakshmi and chant 'Shri Sookt'"},
        ],
        domains    = ["relationships", "remedies", "wealth"],
        tags       = ["Venus", "affliction", "dosha", "Lakshmi", "cows", "pearls", "ghee"],
        planets    = ["Venus"],
        houses     = [],
        extra_cond = {},
        now        = now,
        deity      = "Goddess Lakshmi",
        mantra     = "Shri Sookt",
        symptoms   = [],
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# GROUP 8: Saturn Rules (3 rules)
# LU 25.10: General Saturn affliction, Saturn H5+Sun Leo, Saturn H10→H4 benefit
# ─────────────────────────────────────────────────────────────────────────────

def build_saturn(now):
    rules = []

    # LU 25.10 — General Saturn affliction
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-saturn-affliction",
        name       = "Saturn Affliction — Construction/Property Symptoms and Remedies (Lord Shiva)",
        rtype      = "dosha",
        sub_type   = "affliction",
        checkable  = False,
        yoga_type  = "planet_weak",
        text       = (
            "When Saturn is afflicted: Symptoms relate to property, construction, servants, "
            "and longevity issues. "
            "Remedies: Feed wheat dough balls to fish; share meals with crows; view one's "
            "image in an oil-filled pot (Chhaya Patra / shadow vessel). "
            "Saturn's objects: black gram (urad dal), iron, leather, stone, almond, "
            "oven, pincers (chimta), pan (tawa), wine, spirit. "
            "Lord: Lord Shiva."
        ),
        remedies   = [
            {"category": "offering", "action": "Feed wheat dough balls to fish"},
            {"category": "ritual",   "action": "Share meals with crows (Saturn's bird)"},
            {"category": "ritual",   "action": "View own image in an oil-filled pot (Chhaya Patra)"},
        ],
        domains    = DOMAINS_HEALTH,
        tags       = ["Saturn", "affliction", "dosha", "Shiva", "crows", "fish", "Chhaya_Patra"],
        planets    = ["Saturn"],
        houses     = [],
        extra_cond = {
            "saturn_objects": ["black gram (urad dal)", "iron", "leather", "stone", "almond",
                               "oven", "pincers (chimta)", "pan (tawa)", "wine", "spirit"],
        },
        now        = now,
        deity      = "Lord Shiva",
        symptoms   = ["Property / construction problems", "Servant troubles", "Longevity concerns"],
    ))

    # LU 25.10 — Saturn H5 + Sun in Leo → Son risk during construction
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-saturn-h5-sun-leo",
        name       = "Saturn H5 AND Sun in Leo — Son Faces Risk During House Construction",
        rtype      = "planetary_combination",
        sub_type   = "house_modifier",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "Condition: Saturn in 5th house AND Sun in Leo (sign). "
            "Trigger: Native begins house construction. "
            "Outcome: Son faces significant risk / trouble during the construction period. "
            "Remedy (Enemy Sacrifice Protocol): Use objects of Saturn's enemy (the Sun) — "
            "wheat, jaggery, copper — to neutralise Saturn's threatening force. "
            "Alternative: Wait for son to build the house rather than the native doing so."
        ),
        remedies   = [
            {"category": "offering", "action": "Use Sun objects — wheat, jaggery, copper — during construction to neutralise Saturn's threat to son"},
            {"category": "succour",  "action": "Alternative: Have the son himself build the house to remove Saturn's malefic aspect on him"},
        ],
        domains    = DOMAINS_FAMILY,
        tags       = ["Saturn", "H5", "Sun_Leo", "son", "construction", "house_building", "enemy_sacrifice"],
        planets    = ["Saturn", "Sun"],
        houses     = [5],
        extra_cond = {
            "planet":           "Saturn",
            "house":            5,
            "secondary_planet": "Sun",
            "secondary_sign":   "Leo",
            "trigger":          "construction",
            "affliction_of":    "son",
            "remedy_planet":    "Sun",
        },
        now        = now,
        mechanism  = "Enemy Sacrifice Protocol: when Saturn is the threat (destroyer), donate objects of its enemy (Sun) to satisfy and neutralise the malefic force.",
    ))

    # LU 25.10 — Saturn H10 → H4 benefit window (Reference House Logic)
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-saturn-h10-h4-benefit",
        name       = "Saturn H10 Benefits H4 ONLY During Active Construction (Reference House Logic)",
        rtype      = "planetary_combination",
        sub_type   = "house_modifier",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "Saturn in the 10th house (7th from the 4th house) benefits the 4th house "
            "(home/property/construction) ONLY while construction is actively in progress. "
            "Reference House Rule: A planet in the 7th house from a reference house "
            "provides benefits to the original house until the goal (construction) is complete. "
            "Once the construction is finished, Saturn in H10 stops being useful and may "
            "turn malefic — the benefit window closes permanently."
        ),
        remedies   = [
            {"category": "succour", "action": "Complete construction while Saturn is in H10 — the benefit window is time-limited"},
        ],
        domains    = ["property", "remedies", "timing"],
        tags       = ["Saturn", "H10", "H4", "construction", "benefit_window", "reference_house_logic", "timing"],
        planets    = ["Saturn"],
        houses     = [10, 4],
        extra_cond = {
            "planet":              "Saturn",
            "house":               10,
            "reference_house":     4,
            "benefit_condition":   "construction_in_progress",
            "benefit_expires":     "construction_complete",
            "logic_type":          "reference_house_7th_benefit",
            "logic_note":          "Saturn H10 is 7th from H4. Planet 7th from reference house benefits that house until its object (construction) is complete.",
        },
        now        = now,
        mechanism  = "Reference House Benefit Rule: planet 7th from a reference house supports it until its associated goal is achieved. Once done, the supportive aspect closes.",
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# GROUP 9: Rahu Rules (2 rules)
# LU 25.11: General Rahu affliction, Rahu H8
# ─────────────────────────────────────────────────────────────────────────────

def build_rahu(now):
    rules = []

    # LU 25.11 — General Rahu affliction
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-rahu-affliction",
        name       = "Rahu Affliction — Leprosy Trial and Eclipse Remedies (Goddess Saraswati)",
        rtype      = "dosha",
        sub_type   = "affliction",
        checkable  = False,
        yoga_type  = "planet_weak",
        text       = (
            "When Rahu is afflicted: "
            "Standard remedies: Immerse coconut in water; float barley washed with milk "
            "in the river; immerse coal; donate radish, mustard, or sapphire. "
            "Leprosy Trial remedy: Wash barley with cow's urine, tie in red cloth, keep "
            "with self at all times; clean teeth with cow's urine. "
            "Lord: Goddess Saraswati."
        ),
        remedies   = [
            {"category": "offering", "action": "Immerse coconut in water"},
            {"category": "offering", "action": "Float barley washed with milk in the river"},
            {"category": "offering", "action": "Immerse coal in water"},
            {"category": "offering", "action": "Donate radish, mustard, or sapphire"},
            {"category": "ritual",   "action": "Leprosy Trial: wash barley with cow's urine, tie in red cloth, keep on person at all times"},
            {"category": "ritual",   "action": "Leprosy Trial: clean teeth with cow's urine"},
        ],
        domains    = DOMAINS_HEALTH,
        tags       = ["Rahu", "affliction", "dosha", "Saraswati", "coconut", "barley", "sapphire", "leprosy"],
        planets    = ["Rahu"],
        houses     = [],
        extra_cond = {},
        now        = now,
        deity      = "Goddess Saraswati",
        symptoms   = ["Leprosy / skin disease (Rahu trial)", "Eclipse-related disturbances"],
    ))

    # LU 25.11 — Rahu H8
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-rahu-h8",
        name       = "Rahu in H8 — Throw Gilded Coins in River",
        rtype      = "planetary_combination",
        sub_type   = "house_modifier",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "Rahu placed in the 8th house (longevity/Saturn's house). "
            "Remedy: Throw gilded (gold-plated) coins in the river."
        ),
        remedies   = [
            {"category": "offering", "action": "Throw gilded (gold-plated) coins in the river"},
        ],
        domains    = DOMAINS_HEALTH,
        tags       = ["Rahu", "H8", "house_modifier", "gilded_coins", "river"],
        planets    = ["Rahu"],
        houses     = [8],
        extra_cond = {
            "planet":     "Rahu",
            "house":      8,
            "house_lord": "Saturn",
        },
        now        = now,
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# GROUP 10: Ketu Rules (1 rule)
# LU 25.12: General Ketu affliction
# ─────────────────────────────────────────────────────────────────────────────

def build_ketu(now):
    rules = []

    rules.append(_doc(
        rule_id    = "lalkitab-ch25-ketu-affliction",
        name       = "Ketu Affliction — Son's Behavior, Foot/Urinary Issues and Remedies (Lord Ganapati)",
        rtype      = "dosha",
        sub_type   = "affliction",
        checkable  = False,
        yoga_type  = "planet_weak",
        text       = (
            "When Ketu is afflicted: "
            "Standard remedies: Feed dogs (Ketu = dog's planet); donate sesame (til). "
            "Son's behavior improper → Donate a quilt at a temple. "
            "Disease (foot trouble or urinary infection) → Adorn pure silk thread and "
            "a pearl set in a silver ring. "
            "Lord: Lord Ganapati."
        ),
        remedies   = [
            {"category": "offering", "action": "Feed dogs (Ketu's representative animal)"},
            {"category": "offering", "action": "Donate sesame (til)"},
            {"category": "offering", "action": "If son's behavior is improper: donate a quilt at a temple"},
            {"category": "gemstone_jewelry", "action": "For foot trouble or urinary infection: wear pure silk thread and pearl in a silver ring"},
        ],
        domains    = DOMAINS_HEALTH,
        tags       = ["Ketu", "affliction", "dosha", "Ganapati", "dogs", "sesame", "pearl", "son"],
        planets    = ["Ketu"],
        houses     = [],
        extra_cond = {},
        now        = now,
        deity      = "Lord Ganapati",
        symptoms   = ["Son's behavior improper", "Foot trouble", "Urinary infection"],
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# GROUP 11: Conjunction Rules (7 rules)
# LU 25.13–25.19
# ─────────────────────────────────────────────────────────────────────────────

def build_conjunctions(now):
    rules = []

    # LU 25.13 — Jupiter + Sun + financial difficulty
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-jup-sun-financial",
        name       = "Jupiter+Sun Conjunction AND Financial Difficulty — Saffron/Gold/Books",
        rtype      = "planetary_combination",
        sub_type   = "conjunction_remedy",
        checkable  = True,
        yoga_type  = "planet_conjunction",
        text       = (
            "Condition: Jupiter and Sun are in conjunction AND the native is facing "
            "financial difficulty. "
            "Remedy A: Eat saffron (ingest directly). "
            "Remedy B: Adorn / wear gold. "
            "Remedy C: Donate books."
        ),
        remedies   = [
            {"category": "ritual",             "action": "Eat saffron (consume directly)"},
            {"category": "gemstone_jewelry",   "action": "Adorn or wear gold jewelry"},
            {"category": "offering",           "action": "Donate books"},
        ],
        domains    = DOMAINS_FINANCE,
        tags       = ["Jupiter", "Sun", "conjunction", "financial_difficulty", "saffron", "gold", "books"],
        planets    = ["Jupiter", "Sun"],
        houses     = [],
        extra_cond = {
            "conjunction":        ["Jupiter", "Sun"],
            "trigger":            "financial_difficulty",
            "secondary_condition": "Native is facing financial struggle",
        },
        now        = now,
    ))

    # LU 25.14 — Sun + Saturn + wife's health suffering
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-sun-sat-wife-health",
        name       = "Sun+Saturn Conjunction AND Wife's Health Suffering — Donate Maize Equal to Wife's Weight",
        rtype      = "planetary_combination",
        sub_type   = "conjunction_remedy",
        checkable  = True,
        yoga_type  = "planet_conjunction",
        text       = (
            "Condition: Sun and Saturn are in conjunction AND the native's wife is "
            "suffering in health. "
            "Remedy: Donate maize equivalent to the weight of the wife."
        ),
        remedies   = [
            {"category": "offering", "action": "Donate maize (corn) equivalent to the weight of the wife"},
        ],
        domains    = DOMAINS_FAMILY,
        tags       = ["Sun", "Saturn", "conjunction", "wife_health", "maize", "weight_donation"],
        planets    = ["Sun", "Saturn"],
        houses     = [],
        extra_cond = {
            "conjunction":         ["Sun", "Saturn"],
            "trigger":             "wife_health_suffering",
            "affliction_of":       "wife",
            "secondary_condition": "Wife's health is suffering",
        },
        now        = now,
    ))

    # LU 25.15 — Sun + Saturn + Saturn's property / objects being destroyed
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-sun-sat-property",
        name       = "Sun+Saturn Conjunction AND Saturn Objects Being Destroyed — Donate Sun Objects",
        rtype      = "planetary_combination",
        sub_type   = "conjunction_remedy",
        checkable  = True,
        yoga_type  = "planet_conjunction",
        text       = (
            "Condition: Sun and Saturn are in conjunction AND Saturn's objects/property "
            "are being destroyed (by the Sun's power/aggression). "
            "Mechanism: Saturn is afflicted specifically due to the Sun's dominance in the "
            "conjunction. The Sun is the attacker. "
            "Remedy (Enemy Sacrifice Protocol): Donate objects related to the attacker (Sun) — "
            "copper, jaggery, wheat."
        ),
        remedies   = [
            {"category": "offering", "action": "Donate objects of the Sun (copper, jaggery, wheat) to pacify Sun's destruction of Saturn's domain"},
        ],
        domains    = ["property", "remedies"],
        tags       = ["Sun", "Saturn", "conjunction", "property_destruction", "copper", "jaggery", "enemy_sacrifice"],
        planets    = ["Sun", "Saturn"],
        houses     = [],
        extra_cond = {
            "conjunction":         ["Sun", "Saturn"],
            "trigger":             "saturn_objects_being_destroyed",
            "attacker_planet":     "Sun",
            "remedy_planet":       "Sun",
        },
        now        = now,
        mechanism  = "Enemy Sacrifice: Saturn's objects are being destroyed by Sun's force. Donating Sun's objects to the divine satisfies Sun and stops the destruction.",
    ))

    # LU 25.16 — Sun + Saturn + gold/jaggery loss
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-sun-sat-gold-loss",
        name       = "Sun+Saturn Conjunction AND Gold/Jaggery Loss — Donate Saturn Objects",
        rtype      = "planetary_combination",
        sub_type   = "conjunction_remedy",
        checkable  = True,
        yoga_type  = "planet_conjunction",
        text       = (
            "Condition: Sun and Saturn are in conjunction AND the native is experiencing "
            "loss of gold or jaggery (Sun's objects). "
            "Mechanism: The loss is triggered by Saturn's affliction of Sun's objects — "
            "Saturn is the attacker here. "
            "Remedy (Enemy Sacrifice Protocol): Donate objects of Saturn (the attacker) — "
            "iron, oil, or almonds."
        ),
        remedies   = [
            {"category": "offering", "action": "Donate Saturn objects — iron, oil, or almonds — to pacify Saturn's destruction of Sun's domain"},
        ],
        domains    = DOMAINS_FINANCE,
        tags       = ["Sun", "Saturn", "conjunction", "gold_loss", "jaggery_loss", "iron", "oil", "almonds"],
        planets    = ["Sun", "Saturn"],
        houses     = [],
        extra_cond = {
            "conjunction":         ["Sun", "Saturn"],
            "trigger":             "gold_or_jaggery_loss",
            "attacker_planet":     "Saturn",
            "remedy_planet":       "Saturn",
        },
        now        = now,
        mechanism  = "Enemy Sacrifice: Sun's objects (gold/jaggery) are being lost due to Saturn's force. Donating Saturn's own objects satisfies and neutralises the attacker.",
    ))

    # LU 25.17 — Sun + Rahu → Solar Eclipse Protocol
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-sun-rahu-eclipse",
        name       = "Sun+Rahu Conjunction — Float Rahu Objects DURING Solar Eclipse Only",
        rtype      = "planetary_combination",
        sub_type   = "conjunction_remedy",
        checkable  = True,
        yoga_type  = "planet_conjunction",
        text       = (
            "Condition: Sun and Rahu are in conjunction. "
            "Remedy: Float objects of the harmful planet (Rahu) — coal or mustard — "
            "in the river. "
            "CRITICAL TIMING CONSTRAINT: This remedy is valid and useful ONLY if performed "
            "specifically within the window of a solar eclipse. Performing outside of an "
            "eclipse has no effect."
        ),
        remedies   = [
            {"category": "offering", "action": "Float coal or mustard in the river — MUST be done during a solar eclipse window"},
        ],
        domains    = DOMAINS_HEALTH,
        tags       = ["Sun", "Rahu", "conjunction", "solar_eclipse", "coal", "mustard", "eclipse_timing"],
        planets    = ["Sun", "Rahu"],
        houses     = [],
        extra_cond = {
            "conjunction":         ["Sun", "Rahu"],
            "trigger":             "solar_eclipse",
            "timing_constraint":   "MUST be performed during solar eclipse — ineffective otherwise",
            "remedy_objects":      ["coal", "mustard"],
        },
        now        = now,
        mechanism  = "Eclipse Ingestion Logic: Sun+Rahu conjunction remedies are valid ONLY within the eclipse window, when the malefic conjunction is cosmically 'active' and receptive to intervention.",
    ))

    # LU 25.18 — Moon + Rahu → Lunar Eclipse Protocol
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-moon-rahu-eclipse",
        name       = "Moon+Rahu Conjunction — Immerse Rahu/Saturn Objects DURING Lunar Eclipse Only",
        rtype      = "planetary_combination",
        sub_type   = "conjunction_remedy",
        checkable  = True,
        yoga_type  = "planet_conjunction",
        text       = (
            "Condition: Moon and Rahu are in conjunction. "
            "Remedy: Immerse objects of Rahu or Saturn (Saturn being an enemy of Moon) "
            "in the river. "
            "Outcome: This ritual exalts the Moon's effect — restores Moon's full benefic power. "
            "CRITICAL TIMING CONSTRAINT: This remedy is valid and useful ONLY if performed "
            "specifically within the window of a lunar eclipse."
        ),
        remedies   = [
            {"category": "offering", "action": "Immerse Rahu or Saturn objects in the river — MUST be done during a lunar eclipse window"},
        ],
        domains    = DOMAINS_HEALTH,
        tags       = ["Moon", "Rahu", "conjunction", "lunar_eclipse", "eclipse_timing", "Saturn_objects"],
        planets    = ["Moon", "Rahu"],
        houses     = [],
        extra_cond = {
            "conjunction":         ["Moon", "Rahu"],
            "trigger":             "lunar_eclipse",
            "timing_constraint":   "MUST be performed during lunar eclipse — ineffective otherwise",
            "remedy_planets":      ["Rahu", "Saturn"],
        },
        now        = now,
        mechanism  = "Eclipse Ingestion Logic: Moon+Rahu conjunction remedies are valid ONLY within the lunar eclipse window. Saturn is included as enemy of Moon — its objects serve as additional sacrifice.",
    ))

    # LU 25.19 — Mars + Mercury → Sister's health suffering
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-mars-mercury-sister",
        name       = "Mars+Mercury Conjunction AND Sister's Health Suffering — Bury Mars Objects in Earthen Pot",
        rtype      = "planetary_combination",
        sub_type   = "conjunction_remedy",
        checkable  = True,
        yoga_type  = "planet_conjunction",
        text       = (
            "Condition: Mars and Mercury are in conjunction AND the native's sister is "
            "suffering health issues. "
            "Diagnostic logic: Sister's illness is a marker for an overheated Mars in the "
            "Mars-Mercury conjunction. "
            "Remedy (Isolated Burial Protocol): Fill an earthen pot (surahi) with objects "
            "of Mars — brown sugar, honey, aniseed — and bury it at an isolated place. "
            "Outcome: This ritual removes Mars's malefic energy from the home environment "
            "and calms the overheated Mars."
        ),
        remedies   = [
            {"category": "ritual", "action": "Fill earthen pot (surahi) with Mars objects (brown sugar, honey, aniseed) and bury at an isolated location"},
        ],
        domains    = DOMAINS_FAMILY,
        tags       = ["Mars", "Mercury", "conjunction", "sister_health", "earthen_pot", "burial", "isolated"],
        planets    = ["Mars", "Mercury"],
        houses     = [],
        extra_cond = {
            "conjunction":         ["Mars", "Mercury"],
            "trigger":             "sister_health_suffering",
            "affliction_of":       "sister",
            "remedy_objects":      ["brown sugar", "honey", "aniseed"],
            "ritual_vessel":       "earthen pot (surahi)",
        },
        now        = now,
        mechanism  = "Sister's illness is a social symptom of Mars being overheated by Mercury's conjunction. The 'Isolated Burial' removes the malefic force away from the domestic environment.",
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# GROUP 12: General Principles (3 rules)
# LU 25.20: Daytime rule for conjunction remedies
# LU 25.21: Sun friend-cooperation mechanism
# LU 25.22: Donation-modesty principle
# ─────────────────────────────────────────────────────────────────────────────

def build_general_principles(now):
    rules = []

    # LU 25.20 — Daytime constraint for all conjunction remedies
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-daytime-conjunction-rule",
        name       = "Conjunction Remedies Must Be Performed During Daytime (Universal Constraint)",
        rtype      = "general_principle",
        sub_type   = "temporal_constraint",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "Universal rule for Chapter 25: ALL remedies mentioned for multi-planet "
            "conjunctions — including Sun+Saturn, Sun+Rahu, Moon+Rahu, Mars+Mercury, "
            "Jupiter+Sun — MUST be undertaken during the daytime. Performing conjunction "
            "remedies at night invalidates the remedy."
        ),
        remedies   = [],
        domains    = DOMAINS_GENERAL,
        tags       = ["conjunction_remedies", "daytime_rule", "temporal_constraint", "universal"],
        planets    = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Saturn", "Rahu"],
        houses     = [],
        extra_cond = {
            "timing_rule":     "daytime_only",
            "applies_to":      "all_conjunction_remedies_in_ch25",
            "applies_to_rules": [
                "lalkitab-ch25-jup-sun-financial",
                "lalkitab-ch25-sun-sat-wife-health",
                "lalkitab-ch25-sun-sat-property",
                "lalkitab-ch25-sun-sat-gold-loss",
                "lalkitab-ch25-sun-rahu-eclipse",
                "lalkitab-ch25-moon-rahu-eclipse",
                "lalkitab-ch25-mars-mercury-sister",
            ],
        },
        now        = now,
    ))

    # LU 25.21 — Sun friend-cooperation mechanism
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-sun-friend-cooperation",
        name       = "Sun Friend-Cooperation Principle — Moon (Water) and Mars (Sweets) Calm Sun (Fire)",
        rtype      = "general_principle",
        sub_type   = "remedy_mechanism",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "Foundational remedy mechanism for Sun afflictions: "
            "Sun represents Fire. Sun is calmed by its natural friends — Moon (Water/Milk) "
            "and Mars (Sweets/Honey). "
            "Ritual application: Habitually put sweets in the mouth (Mars element) and "
            "then drink water (Moon element). This sequence activates the friend-cooperation "
            "formula to subdue Sun's malefic fire."
        ),
        remedies   = [
            {"category": "ritual", "action": "Habitually eat sweets (Mars element) then drink water (Moon element) — activates Sun friend-cooperation formula"},
        ],
        domains    = DOMAINS_GENERAL,
        tags       = ["Sun", "Moon", "Mars", "friend_cooperation", "fire_water_sweets", "mechanism"],
        planets    = ["Sun", "Moon", "Mars"],
        houses     = [],
        extra_cond = {
            "mechanism_type":    "friend_cooperation",
            "afflicted_planet":  "Sun",
            "calming_elements":  {"Moon": "Water/Milk", "Mars": "Sweets/Honey"},
        },
        now        = now,
        mechanism  = "Sun (Fire) + Moon (Water) + Mars (Sweets/Honey) = elemental balance. Friends neutralise the afflicted planet's excess energy through their complementary elemental properties.",
    ))

    # LU 25.22 — Donation modesty principle
    rules.append(_doc(
        rule_id    = "lalkitab-ch25-donation-modesty",
        name       = "Donation Modesty Principle — Even Small Sun Offering Triggers 'Modesty' and Dissolves Troubles",
        rtype      = "general_principle",
        sub_type   = "remedy_mechanism",
        checkable  = False,
        yoga_type  = "manual",
        text       = (
            "Universal remedy principle: Making a donation of even a few grains in the "
            "name of the Sun triggers 'modesty' (humility before the divine), which "
            "subdues the planet's anger. "
            "Outcome: The native's troubles 'flow off' like running water — they are "
            "dissolved rather than accumulated."
        ),
        remedies   = [
            {"category": "offering", "action": "Donate even a few grains in the name of the Sun — humility itself is the remedy"},
        ],
        domains    = DOMAINS_GENERAL,
        tags       = ["Sun", "donation", "modesty", "humility", "general_principle", "remedy_mechanism"],
        planets    = ["Sun"],
        houses     = [],
        extra_cond = {
            "mechanism_type": "donation_modesty",
            "minimum_offering": "even a few grains",
            "outcome": "Troubles flow away like running water",
        },
        now        = now,
        mechanism  = "Lal Kitab's donation philosophy: the ACT of giving — not its scale — activates cosmic 'modesty' (surrender of ego). This reverses the planet's anger regardless of donation size.",
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# Master builder
# ─────────────────────────────────────────────────────────────────────────────

def build_all(now: str) -> list[dict]:
    rules = []
    rules += build_foundations(now)        # 1
    rules += build_sun(now)                # 3
    rules += build_moon(now)               # 6
    rules += build_mars(now)               # 3
    rules += build_mercury(now)            # 3
    rules += build_jupiter(now)            # 2
    rules += build_venus(now)              # 1
    rules += build_saturn(now)             # 3
    rules += build_rahu(now)               # 2
    rules += build_ketu(now)               # 1
    rules += build_conjunctions(now)       # 7
    rules += build_general_principles(now) # 3
    return rules                           # 35 total


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Ingest Lal Kitab Ch 25 — Remedial Measures for Planetary Dosh"
    )
    parser.add_argument("--dry-run",   action="store_true", help="Build rules without uploading")
    parser.add_argument("--save",      metavar="FILE",      help="Save rules to JSON file")
    parser.add_argument("--upload",    metavar="FILE",      help="Upload rules from JSON file to MongoDB")
    parser.add_argument("--mongo-url", metavar="URL",       help="MongoDB connection string")
    parser.add_argument("--db-name",   default="horoscope_db")
    args = parser.parse_args()

    now = datetime.now(timezone.utc).isoformat()

    # ── Upload path ───────────────────────────────────────────────────────────
    if args.upload:
        if not args.mongo_url:
            print("ERROR: --mongo-url is required with --upload", file=sys.stderr)
            sys.exit(1)
        from pymongo import MongoClient
        rules = json.loads(Path(args.upload).read_text())
        client = MongoClient(args.mongo_url)
        col = client[args.db_name]["interpretation_rules"]
        inserted = updated = 0
        for rule in rules:
            res = col.update_one(
                {"rule_id": rule["rule_id"]},
                {"$set": rule},
                upsert=True,
            )
            if res.upserted_id:
                inserted += 1
            elif res.modified_count:
                updated += 1
        print(f"Loaded {len(rules)} rules from {args.upload}")
        print(f"Inserted {inserted} / Updated {updated} rules → {args.db_name}.interpretation_rules")
        client.close()
        return

    # ── Dry-run / build path ──────────────────────────────────────────────────
    rules = build_all(now)
    print(f"\nBuilt {len(rules)} rules for batch {BATCH_ID}")
    print(f"\nBreakdown by group:")
    groups: dict[str, int] = {}
    for r in rules:
        g = r["condition"]["sub_type"]
        groups[g] = groups.get(g, 0) + 1
    for g, n in sorted(groups.items(), key=lambda x: -x[1]):
        print(f"  {g:30s}: {n}")
    print()

    if args.save:
        Path(args.save).write_text(json.dumps(rules, indent=2, ensure_ascii=False))
        print(f"Saved → {args.save}")

    if args.dry_run:
        print("\nDry run — first rule sample:")
        print(json.dumps(rules[0], indent=2, ensure_ascii=False)[:800], "...\n")


if __name__ == "__main__":
    main()
