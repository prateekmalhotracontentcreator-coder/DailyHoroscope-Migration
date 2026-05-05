#!/usr/bin/env python3
"""
ingest_lalkitab_ch26_v1.py — Lal Kitab Chapter 26: Auspicious Timings & Planetary Debilitation

16 rules across 2 builder functions.
BATCH_ID: lalkitab-ch26-v1-20260505

Source files:
  Lal Kitab_Ch 26_JSON Ready.md (V9)
  Lal Kitab_Ch 26_Diagnostics.md

Rule groups:
  Day General Principles  (7): sunday, monday, tuesday, wednesday, thursday, friday, saturday
  Planet Debilitation     (9): sun, moon, mars, mercury, jupiter, ketu, venus, saturn, rahu

Design notes:
  - LU 26.10 covers Jupiter + Ketu (both Thursday) → split into 2 rules
  - LU 26.12 covers Venus + Saturn (both Friday) → split into 2 rules
  - Mars exaltation distinction (accept prasad) embedded in mars-debilitation
  - Venus+Saturn almonds succour (Diagnostic) embedded in venus-debilitation
  - Saturday has no travel direction → travel_direction = None

Workflow:
  # Dry run + save:
  python3 scripts/ingest_lalkitab_ch26_v1.py --dry-run --save scripts/lalkitab_ch26_rules.json

  # Upload:
  python3 scripts/ingest_lalkitab_ch26_v1.py \\
    --upload scripts/lalkitab_ch26_rules.json \\
    --mongo-url "$MONGO_URL" --db-name horoscope_db

  # Validate:
  python3 scripts/validate_rules.py \\
    --mongo-url "$MONGO_URL" --db-name horoscope_db \\
    --batch-id lalkitab-ch26-v1-20260505
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
CHAPTER   = 26
CHAP_NAME = "Auspicious Timings, Birth Traits, and Planetary Debilitation Remedies"
BATCH_ID  = "lalkitab-ch26-v1-20260505"

DOMAINS_TIMING  = ["timing", "auspicious_activities", "daily_life"]
DOMAINS_REMEDY  = ["remedies", "health", "wellbeing"]
DOMAINS_TRAVEL  = ["travel", "timing", "daily_life"]


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
         now, symptoms=None, physical_markers=None):
    doc = _base(rule_id, now)
    yc: dict = {"type": yoga_type, "checkable": checkable}
    if not checkable:
        yc["description"] = "Requires day-of-week / behavioral / ritual judgment — not automatable in Phase 1."
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
# GROUP 1: Day General Principles (7 rules)
# One rule per weekday covering: auspicious activities, travel direction, birth trait
# ─────────────────────────────────────────────────────────────────────────────

# Day data: (day_name, planet, logic_unit, auspicious, inauspicious, travel, birth_trait, travel_note)
DAY_DATA = [
    (
        "sunday", "Sunday", "Sun", "26.1",
        ["All auspicious deeds", "Seeking affection at dawn"],
        [],
        "East",
        "Journey towards East will be successful.",
        "Lucky",
    ),
    (
        "monday", "Monday", "Moon", "26.3",
        ["Weddings", "Nomenclature (naming ceremonies)", "House construction", "School admission"],
        [],
        "South to West",
        "Journey from South to West will be successful.",
        "Gentle and noble",
    ),
    (
        "tuesday", "Tuesday", "Mars", "26.5",
        ["Buying and selling houses"],
        ["Sewing or wearing new clothes"],
        "East and South",
        "No hurdles for journeys towards East and South.",
        "Aggressive by nature",
    ),
    (
        "wednesday", "Wednesday", "Mercury", "26.7",
        ["Wearing new clothes", "House entry (griha pravesh)", "Studying", "Cultivating land"],
        [],
        "East or West",
        "No hurdles for journeys towards East or West.",
        "Inclined towards religion",
    ),
    (
        "thursday", "Thursday", "Jupiter", "26.9",
        ["All kinds of work", "Success in jobs / career matters"],
        [],
        None,
        "No specific travel direction mentioned — Thursday is generally auspicious for all directions.",
        "Bright and virtuous",
    ),
    (
        "friday", "Friday", "Venus", "26.11",
        ["All work", "Evening journeys specifically favorable"],
        [],
        "Evening (timing, not direction)",
        "Evening journeys are favorable. No directional restriction.",
        "Romantic and choosy",
    ),
    (
        "saturday", "Saturday", "Saturn", "26.13",
        [],
        ["Starting new work", "Journeys of any kind", "Sewing or wearing new clothes"],
        None,
        "Absolutely inauspicious — avoid all new beginnings and travel.",
        "Generally sickly",
    ),
]


def build_day_generals(now):
    rules = []
    for (slug, day_name, planet, lu, auspicious, inauspicious, travel_dir, travel_note, birth_trait) in DAY_DATA:
        is_inauspicious_day = (slug == "saturday")
        auspicious_str = "; ".join(auspicious) if auspicious else "None (inauspicious day)"
        inauspicious_str = ("; ".join(inauspicious) + " (inauspicious)") if inauspicious else ""

        text_parts = [f"{day_name} is ruled by {planet}. "]
        if auspicious:
            text_parts.append(f"Auspicious activities: {auspicious_str}. ")
        if inauspicious:
            text_parts.append(f"Inauspicious activities to avoid: {inauspicious_str}. ")
        text_parts.append(f"Travel: {travel_note} ")
        text_parts.append(f"Birth trait: Native born on {day_name} will be {birth_trait}.")
        text = "".join(text_parts)

        tags = [slug, planet.lower(), "day_general", "auspicious_timing", "birth_trait", "travel"]
        if is_inauspicious_day:
            tags.append("inauspicious_day")

        rules.append(_doc(
            rule_id    = f"lalkitab-ch26-{slug}-general",
            name       = f"{day_name} — Auspicious Activities, Travel Direction, and Birth Trait",
            rtype      = "general_principle",
            sub_type   = "day_general_principle",
            checkable  = False,
            yoga_type  = "manual",
            text       = text,
            remedies   = [],
            domains    = DOMAINS_TIMING,
            tags       = tags,
            planets    = [planet] if planet not in ("Sunday", "Monday", "Tuesday",
                                                     "Wednesday", "Thursday", "Friday", "Saturday")
                         else [],
            houses     = [],
            extra_cond = {
                "weekday":              day_name,
                "ruling_planet":        planet,
                "logic_unit":           lu,
                "auspicious_activities": auspicious,
                "inauspicious_activities": inauspicious,
                "travel_direction":     travel_dir,
                "travel_note":          travel_note,
                "birth_trait":          birth_trait,
                "is_inauspicious_day":  is_inauspicious_day,
            },
            now        = now,
        ))
    return rules


# ─────────────────────────────────────────────────────────────────────────────
# GROUP 2: Planet Debilitation Remedies (9 rules)
# ─────────────────────────────────────────────────────────────────────────────

def build_debilitation_remedies(now):
    rules = []

    # ── LU 26.2 — Sun debilitation (Sunday) ──────────────────────────────────
    rules.append(_doc(
        rule_id    = "lalkitab-ch26-sun-debilitation",
        name       = "Sun Debilitation — Remedies to Strengthen/Exalt Sun",
        rtype      = "dosha",
        sub_type   = "debilitation",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "When Sun is debilitated or weak (requires strengthening): "
            "Remedy A: Immerse rice and jaggery in running water. "
            "Remedy B: Eat rice and milk cooked with jaggery (kheer with jaggery). "
            "Remedy C: Immerse copper coins in water. "
            "Remedy D: Donate wheat and jaggery wrapped in a red cloth."
        ),
        remedies   = [
            {"category": "offering", "action": "Immerse rice and jaggery in running water"},
            {"category": "ritual",   "action": "Eat rice and milk cooked with jaggery (jaggery kheer)"},
            {"category": "offering", "action": "Immerse copper coins in water"},
            {"category": "offering", "action": "Donate wheat and jaggery wrapped in a red cloth"},
        ],
        domains    = DOMAINS_REMEDY,
        tags       = ["Sun", "debilitation", "Sunday", "rice", "jaggery", "copper", "wheat"],
        planets    = ["Sun"],
        houses     = [],
        extra_cond = {
            "planet":       "Sun",
            "planet_state": "debilitated",
            "weekday":      "Sunday",
            "logic_unit":   "26.2",
        },
        now        = now,
        symptoms   = ["Sun weak / debilitated"],
    ))

    # ── LU 26.4 — Moon debilitation (Monday) ─────────────────────────────────
    rules.append(_doc(
        rule_id    = "lalkitab-ch26-moon-debilitation",
        name       = "Moon Debilitation — Remedies (Kheer, Pearl, White Tilak)",
        rtype      = "dosha",
        sub_type   = "debilitation",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "When Moon is debilitated or weak: "
            "Remedy A: Eat kheer (rice pudding / milk-rice). "
            "Remedy B: Wear white clothes and apply a white tilak. "
            "Remedy C: Wear a pearl set in a silver ring; donate pearls."
        ),
        remedies   = [
            {"category": "ritual",           "action": "Eat kheer (rice pudding / milk-rice)"},
            {"category": "ritual",           "action": "Wear white clothes and apply a white tilak on forehead"},
            {"category": "gemstone_jewelry", "action": "Wear a pearl set in a silver ring"},
            {"category": "offering",         "action": "Donate pearls"},
        ],
        domains    = DOMAINS_REMEDY,
        tags       = ["Moon", "debilitation", "Monday", "kheer", "pearl", "silver", "white"],
        planets    = ["Moon"],
        houses     = [],
        extra_cond = {
            "planet":       "Moon",
            "planet_state": "debilitated",
            "weekday":      "Monday",
            "logic_unit":   "26.4",
        },
        now        = now,
        symptoms   = ["Moon weak / debilitated"],
    ))

    # ── LU 26.6 — Mars debilitation / Mangali (Tuesday) ──────────────────────
    rules.append(_doc(
        rule_id    = "lalkitab-ch26-mars-debilitation",
        name       = "Mars Debilitation / Mangali — Remedies (Hanuman, Rewari, Sweet Bread)",
        rtype      = "dosha",
        sub_type   = "debilitation",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "When Mars is debilitated, malefic, or native is Mangali (Mars dosha): "
            "Prohibition: Do NOT use masoor dal (red lentils) for self. "
            "Remedy A: Immerse rewari (sesame-jaggery sweet) in water. "
            "Remedy B: Distribute sweet bread (paratha) among children and monkeys. "
            "Remedy C: Visit Hanumanji's temple. "
            "Exalted Mars distinction (Diagnostic): When Mars IS exalted/strong, the native "
            "must also accept/eat the prasad they distribute at the temple — this is not done "
            "for debilitated Mars where the offering is entirely external."
        ),
        remedies   = [
            {"category": "succour",  "action": "Do NOT use masoor dal (red lentils) for self — prohibition"},
            {"category": "offering", "action": "Immerse rewari (sesame-jaggery sweet) in water"},
            {"category": "offering", "action": "Distribute sweet bread (paratha) among children and monkeys"},
            {"category": "ritual",   "action": "Visit Hanumanji's temple and offer worship"},
        ],
        domains    = DOMAINS_REMEDY,
        tags       = ["Mars", "debilitation", "mangali", "Tuesday", "Hanuman", "rewari", "paratha", "masoor_prohibition"],
        planets    = ["Mars"],
        houses     = [],
        extra_cond = {
            "planet":            "Mars",
            "planet_state":      ["debilitated", "malefic", "mangali"],
            "weekday":           "Tuesday",
            "logic_unit":        "26.6",
            "prohibition":       "Do not use masoor dal (red lentils) for self",
            "exalted_distinction": (
                "When Mars is exalted: native must also accept and eat the prasad "
                "distributed at the temple — offering is both external and personal."
            ),
        },
        now        = now,
        symptoms   = ["Mars weak / debilitated", "Mangali dosha"],
    ))

    # ── LU 26.8 — Mercury debilitation (Wednesday) ───────────────────────────
    rules.append(_doc(
        rule_id    = "lalkitab-ch26-mercury-debilitation",
        name       = "Mercury Debilitation — 100-Day Nose Ritual, Moong Protocol, Structural Prohibitions",
        rtype      = "dosha",
        sub_type   = "debilitation",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "When Mercury is debilitated or weak: "
            "Dietary prohibition: Do not eat whole moong (green gram). "
            "Clothing prohibition: Do not wear green clothes. "
            "Structural prohibition: Do not keep wide-leaf plants, bamboo, or a grinding mill "
            "on the roof of the house. "
            "Remedy A (100-Day Ritual): Pierce nose and wear silver in it for exactly 100 days. "
            "Remedy B (Split-Day Moong Protocol): Soak moong on Tuesday evening; feed the soaked "
            "moong to animals on Wednesday morning. The split-day cycle is essential — "
            "soaking on Tuesday activates Mars energy; feeding on Wednesday morning channels "
            "it through Mercury's day."
        ),
        remedies   = [
            {"category": "succour",  "action": "Do NOT eat whole moong (green gram) — prohibition"},
            {"category": "succour",  "action": "Do NOT wear green clothes — prohibition"},
            {"category": "succour",  "action": "Do NOT keep wide-leaf plants, bamboo, or grinding mill on roof — structural prohibition"},
            {"category": "ritual",   "action": "Pierce nose and wear silver in it for exactly 100 days"},
            {"category": "offering", "action": "Soak moong on Tuesday evening; feed to animals on Wednesday morning (split-day cycle)"},
        ],
        domains    = DOMAINS_REMEDY,
        tags       = ["Mercury", "debilitation", "Wednesday", "nose_piercing", "silver", "moong", "100_days", "green_prohibition"],
        planets    = ["Mercury"],
        houses     = [],
        extra_cond = {
            "planet":       "Mercury",
            "planet_state": "debilitated",
            "weekday":      "Wednesday",
            "logic_unit":   "26.8",
            "prohibitions": [
                "Do not eat whole moong (green gram)",
                "Do not wear green clothes",
                "Do not keep wide-leaf plants, bamboo, or grinding mill on roof",
            ],
            "temporal_constraints": {
                "nose_piercing_duration_days": 100,
                "moong_soak_day":  "Tuesday",
                "moong_feed_day":  "Wednesday morning",
                "moong_cycle_logic": "Soak Tuesday (Mars energy activation) → feed Wednesday morning (Mercury channeling)",
            },
        },
        now        = now,
        symptoms   = ["Mercury weak / debilitated"],
    ))

    # ── LU 26.10 — Jupiter debilitation (Thursday) ───────────────────────────
    rules.append(_doc(
        rule_id    = "lalkitab-ch26-jupiter-debilitation",
        name       = "Jupiter Debilitation — Remedies (Yellow Clothes, Curry-Rice, Gram Pulse)",
        rtype      = "dosha",
        sub_type   = "debilitation",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "When Jupiter is debilitated or weak (Thursday remedy): "
            "Remedy A: Donate yellow clothes to Brahmins. "
            "Remedy B: Eat curry and rice (Jupiter's food — yellow dal + rice). "
            "Remedy C: Immerse gram pulse (chana dal) in water."
        ),
        remedies   = [
            {"category": "offering", "action": "Donate yellow clothes to Brahmins"},
            {"category": "ritual",   "action": "Eat curry and rice (yellow dal + rice — Jupiter's food)"},
            {"category": "offering", "action": "Immerse gram pulse (chana dal) in water"},
        ],
        domains    = DOMAINS_REMEDY,
        tags       = ["Jupiter", "debilitation", "Thursday", "yellow_clothes", "gram_pulse", "Brahmins"],
        planets    = ["Jupiter"],
        houses     = [],
        extra_cond = {
            "planet":       "Jupiter",
            "planet_state": "debilitated",
            "weekday":      "Thursday",
            "logic_unit":   "26.10",
            "shared_lu_note": "LU 26.10 also covers Ketu debilitation (same Thursday day) — see ch26-ketu-debilitation",
        },
        now        = now,
        symptoms   = ["Jupiter weak / debilitated"],
    ))

    # ── LU 26.10 — Ketu debilitation (Thursday — split from Jupiter) ──────────
    rules.append(_doc(
        rule_id    = "lalkitab-ch26-ketu-debilitation",
        name       = "Ketu Debilitation — Gold in Ears, Saffron, Yellow Cloth Offering (Thursday)",
        rtype      = "dosha",
        sub_type   = "debilitation",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "When Ketu is debilitated or weak (Thursday remedy): "
            "Remedy A: Put gold in ears (wear gold earrings). "
            "Remedy B: Eat saffron. "
            "Remedy C: Offer banana, wheat, gold, and jaggery wrapped in yellow cloth to a priest. "
            "Remedy D: Donate sesame (til) and a quilt to a saint."
        ),
        remedies   = [
            {"category": "gemstone_jewelry", "action": "Put gold in ears (wear gold earrings)"},
            {"category": "ritual",           "action": "Eat saffron"},
            {"category": "offering",         "action": "Offer banana, wheat, gold, and jaggery wrapped in yellow cloth to a priest"},
            {"category": "offering",         "action": "Donate sesame (til) and a quilt to a saint"},
        ],
        domains    = DOMAINS_REMEDY,
        tags       = ["Ketu", "debilitation", "Thursday", "gold", "saffron", "yellow_cloth", "sesame", "quilt"],
        planets    = ["Ketu"],
        houses     = [],
        extra_cond = {
            "planet":       "Ketu",
            "planet_state": "debilitated",
            "weekday":      "Thursday",
            "logic_unit":   "26.10",
            "shared_lu_note": "LU 26.10 covers both Jupiter and Ketu debilitation under Thursday — see ch26-jupiter-debilitation",
        },
        now        = now,
        symptoms   = ["Ketu weak / debilitated"],
    ))

    # ── LU 26.12 — Venus debilitation (Friday) ────────────────────────────────
    rules.append(_doc(
        rule_id    = "lalkitab-ch26-venus-debilitation",
        name       = "Venus Debilitation — Cow Service, Red Maize Offering, Almonds with Saturn Objects",
        rtype      = "dosha",
        sub_type   = "debilitation",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "When Venus is debilitated or weak (Friday remedy): "
            "Remedy A: Serve the cow (clean, feed, care for cows). "
            "Remedy B: Offer curd and red maize at a temple in quantity equal to the wife's "
            "weight OR one-tenth of the wife's weight. "
            "Remedy C: Feed yellow-colored boiled potatoes to a black cow. "
            "Succour remedy (Diagnostic): Consume almonds specifically alongside objects of "
            "Saturn — this combination exalts Venus by linking it to its friend Saturn's "
            "grounding energy."
        ),
        remedies   = [
            {"category": "succour",  "action": "Serve the cow — clean, feed, care for cows"},
            {"category": "offering", "action": "Offer curd and red maize at temple equal to wife's weight (or 1/10th of wife's weight)"},
            {"category": "ritual",   "action": "Feed yellow-colored boiled potatoes to a black cow"},
            {"category": "succour",  "action": "Consume almonds alongside Saturn objects — exalts Venus through Saturn's grounding energy (Diagnostic)"},
        ],
        domains    = DOMAINS_REMEDY,
        tags       = ["Venus", "debilitation", "Friday", "cow", "red_maize", "curd", "almonds", "Saturn_objects"],
        planets    = ["Venus"],
        houses     = [],
        extra_cond = {
            "planet":       "Venus",
            "planet_state": "debilitated",
            "weekday":      "Friday",
            "logic_unit":   "26.12",
            "weight_formula": "Offer red maize equal to wife's weight OR wife's weight / 10",
            "shared_lu_note": "LU 26.12 covers both Venus and Saturn debilitation under Friday — see ch26-saturn-debilitation",
            "succour_mechanism": "Consuming almonds alongside Saturn objects links Venus to its friend Saturn — boosts Venus energy through Saturn's stability",
        },
        now        = now,
        symptoms   = ["Venus weak / debilitated"],
    ))

    # ── LU 26.12 — Saturn debilitation (Friday — split from Venus) ───────────
    rules.append(_doc(
        rule_id    = "lalkitab-ch26-saturn-debilitation",
        name       = "Saturn Debilitation — Prohibitions (Wine/Meat/Eggs) and Crow/Cloth Remedies",
        rtype      = "dosha",
        sub_type   = "debilitation",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "When Saturn is debilitated or weak (Friday remedy): "
            "Prohibition: Do NOT use wine, urad (black gram), meat, or eggs for self — "
            "donate these items to others instead of consuming them. "
            "Remedy A: Donate black cloth on Saturday. "
            "Remedy B: Feed pakoras fried in mustard oil to crows (Saturn's bird)."
        ),
        remedies   = [
            {"category": "succour",  "action": "Do NOT consume wine, urad dal, meat, or eggs — donate them instead of self-consumption"},
            {"category": "offering", "action": "Donate black cloth on Saturday"},
            {"category": "offering", "action": "Feed pakoras fried in mustard oil to crows (Saturn's bird)"},
        ],
        domains    = DOMAINS_REMEDY,
        tags       = ["Saturn", "debilitation", "Friday", "Saturday", "black_cloth", "crows", "pakoras", "wine_prohibition"],
        planets    = ["Saturn"],
        houses     = [],
        extra_cond = {
            "planet":       "Saturn",
            "planet_state": "debilitated",
            "weekday":      "Friday",
            "logic_unit":   "26.12",
            "prohibitions": ["Wine / alcohol", "Urad dal (black gram)", "Meat", "Eggs"],
            "prohibition_note": "Substitutive logic: instead of self-consumption, donate these items — transforms Saturn's malefic consumption into charitable offering",
            "shared_lu_note": "LU 26.12 covers both Venus and Saturn debilitation under Friday — see ch26-venus-debilitation",
        },
        now        = now,
        symptoms   = ["Saturn weak / debilitated"],
    ))

    # ── LU 26.14 — Rahu debilitation (Saturday) ──────────────────────────────
    rules.append(_doc(
        rule_id    = "lalkitab-ch26-rahu-debilitation",
        name       = "Rahu Debilitation — Color Prohibition, Square Silver in Pocket, Coconut/Almond/Barley",
        rtype      = "dosha",
        sub_type   = "debilitation",
        checkable  = True,
        yoga_type  = "planet_in_house",
        text       = (
            "When Rahu is debilitated or weak (Saturday remedy): "
            "Color prohibition: Do NOT wear blue or black clothes on Wednesday or Saturday. "
            "Remedy A: Always keep a square piece of silver in the pocket (permanent carry). "
            "Remedy B: Immerse coconut, almond, and barley in water."
        ),
        remedies   = [
            {"category": "succour",  "action": "Do NOT wear blue or black clothes on Wednesday or Saturday — color prohibition"},
            {"category": "ritual",   "action": "Always keep a square piece of silver in pocket (permanent daily carry)"},
            {"category": "offering", "action": "Immerse coconut, almond, and barley in water"},
        ],
        domains    = DOMAINS_REMEDY,
        tags       = ["Rahu", "debilitation", "Saturday", "silver_square", "coconut", "almond", "barley", "color_prohibition"],
        planets    = ["Rahu"],
        houses     = [],
        extra_cond = {
            "planet":       "Rahu",
            "planet_state": "debilitated",
            "weekday":      "Saturday",
            "logic_unit":   "26.14",
            "prohibitions": ["Blue or black clothes on Wednesday", "Blue or black clothes on Saturday"],
            "silver_shape": "square",
            "silver_carry":  "permanent / always-on-person",
        },
        now        = now,
        symptoms   = ["Rahu weak / debilitated"],
    ))

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# Master builder
# ─────────────────────────────────────────────────────────────────────────────

def build_all(now: str) -> list[dict]:
    rules = []
    rules += build_day_generals(now)              # 7
    rules += build_debilitation_remedies(now)     # 9
    return rules                                  # 16 total


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Ingest Lal Kitab Ch 26 — Auspicious Timings & Planetary Debilitation"
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
    print(f"\nBreakdown by sub_type:")
    groups: dict[str, int] = {}
    for r in rules:
        g = r["condition"]["sub_type"]
        groups[g] = groups.get(g, 0) + 1
    for g, n in sorted(groups.items(), key=lambda x: -x[1]):
        print(f"  {g:30s}: {n}")

    print(f"\nRule IDs:")
    for r in rules:
        print(f"  {r['rule_id']}")

    if args.save:
        Path(args.save).write_text(json.dumps(rules, indent=2, ensure_ascii=False))
        print(f"\nSaved → {args.save}")

    if args.dry_run:
        print("\nDry run complete.")


if __name__ == "__main__":
    main()
