#!/usr/bin/env python3
"""
ingest_bphs_ch44_v1.py — BPHS Chapter 44: Marakas (Killer Planets)

40 rules across 7 groups:
   8  maraka_identification  — Primary killer houses, hierarchy, Saturn override,
                               H2 mathematical precedence, Moon-centric sweep
   6  maraka_timing          — Sub-period prohibition, lifespan classes, star triggers,
                               Longevity-Maraka correlation gate, sub-period triad
   3  rahu_ketu              — Node killer status, exclusion zones, Node-Signifier override
   7  cause_of_death         — 3rd house planet-cause library, multi-planet, gender-specific,
                               mixed occupation, Moon-sign Maraka lords
   5  eighth_house_library   — 8th house planet-cause, Sacred Passing yoga, corpse fate,
                               Serpent decanate, post-death world (vacant houses)
   4  death_environment      — Place/locality diagnosis, pre-natal abode (decanate),
                               post-death worlds (H12/7/6/8 planets), status ranking
   7  consciousness_fate     — Consciousness protocol, childhood vulnerability (<20),
                               childhood remedy, pre-natal sin diagnosis, afterlife ranking,
                               22nd decanate asterism trigger, asterism dasa master logic

Source:
  PDF:    BPHS_Vol 1_Ch 44_Marakas.pdf  /  BPHS_Vol 1_Ch 44_Part1.pdf
  Decode: BPHS_Vol 1_Ch44_JSON Ready_LM.md (V14 — de-duplicated)
  Ref:    Summary Logic of Ch43 and Ch44.md

Checkable: 14 / 40
  planet_in_house:       malefic in H2/H7, benefic+12L, Rahu/Ketu nodes, node-exclusion,
                         8th house cause library, sacred passing yoga,
                         3rd house cause library, Venus+female trigger,
                         multi-planet H3, consciousness protocol
  planetary_combination: Saturn override, sub-period triad, node-signifier override

Standard workflow:
  python3 scripts/ingest_bphs_ch44_v1.py --dry-run --save scripts/bphs_ch44_rules.json
  python3 scripts/ingest_bphs_ch44_v1.py --upload scripts/bphs_ch44_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db
  python3 scripts/validate_rules.py --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id bphs-ch44-v1-20260504
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCIENCE   = "jyotish"
BOOK      = "Brihat Parashara Hora Shastra"
BOOK_ID   = "bphs"
CHAPTER   = 44
CHAP_NAME = "Marakas (Killer Planets)"
BATCH_ID  = "bphs-ch44-v1-20260504"

YOGA_DATA: list[dict] = [

    # ═══════════════════════════════════════════════════════════════════════════
    # GROUP 1: MARAKA IDENTIFICATION
    # ═══════════════════════════════════════════════════════════════════════════

    {
        "yoga_name":      "Primary Maraka Houses — H2 and H7",
        "sloka":          "ch44-sloka-01-03",
        "group":          "maraka_identification",
        "condition_type": "general_principle",
        "formation": (
            "The 2nd and 7th houses are designated Maraka (killer) houses. "
            "Lords and occupants of these houses gain power to cause death during "
            "their Dasa and Antar-dasa periods when the native's calculated lifespan "
            "window coincides."
        ),
        "effect": (
            "2nd and 7th lords or occupants become primary killers. "
            "House 2 is more lethal than House 7 because it is simultaneously "
            "the 12th from the 3rd house (Longevity house) and the 7th from the "
            "8th house (House of Death). This double-terminal positioning grants H2 "
            "the primary qualification as the chief killer."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [2, 7],
        "phase": 2,
    },
    {
        "yoga_name":      "Malefic in H2/H7 — Prime Killer Designation",
        "sloka":          "ch44-sloka-02",
        "group":          "maraka_identification",
        "condition_type": "planet_in_house",
        "formation": (
            "A natural malefic planet (Saturn, Mars, Rahu, Ketu, Sun) occupies "
            "or lords over the 2nd or 7th house."
        ),
        "effect": (
            "The malefic planet becomes a prime killer and will inflict death "
            "during its Dasa period provided the lifespan window permits."
        ),
        "checkable": True,
        "yoga_check_type": "planet_in_house",
        "planets_involved": ["Saturn", "Mars", "Rahu", "Ketu", "Sun"],
        "houses_involved": [2, 7],
        "phase": 2,
    },
    {
        "yoga_name":      "Benefic Killer Trigger — 12th Lord Association",
        "sloka":          "ch44-sloka-03",
        "group":          "maraka_identification",
        "condition_type": "planet_in_house",
        "formation": (
            "A natural benefic planet (Jupiter, Venus, Mercury waxing, Moon waxing) "
            "is related to (conjunct, aspects, or is aspected by) the lord of the "
            "12th house."
        ),
        "effect": (
            "The benefic acquires Maraka power and can inflict death during its "
            "Dasa period. Without the 12th lord link, a benefic cannot cause death "
            "from the Maraka houses alone."
        ),
        "checkable": True,
        "yoga_check_type": "planet_in_house",
        "planets_involved": ["Jupiter", "Venus", "Mercury", "Moon"],
        "houses_involved": [12],
        "phase": 2,
    },
    {
        "yoga_name":      "Maraka Power Hierarchy — Three-Grade Descending Order",
        "sloka":          "ch44-sloka-04-07",
        "group":          "maraka_identification",
        "condition_type": "general_principle",
        "formation": (
            "All planets are ranked for Maraka power based on the houses they "
            "lord or occupy: Grade 1 (maximum) through Grade 3 (minimum)."
        ),
        "effect": (
            "Grade 1 (Maximum Power): Lords or occupants of Houses 12, 3, 8, 7, and 2. "
            "Grade 2 (Secondary Killers): Lords or occupants of Houses 6 and 11. "
            "Grade 3 (Least Power): Lords or occupants of Houses 5, 9, 10, 4, and 1 — "
            "these only become killers if specific secondary criteria (conjunction, "
            "asterism, or Moon-centric Maraka rules) are met."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "phase": 2,
    },
    {
        "yoga_name":      "Saturn Killer Priority Override",
        "sloka":          "ch44-sloka-05",
        "group":          "maraka_identification",
        "condition_type": "planetary_combination",
        "formation": (
            "Saturn is ill-disposed (debilitated, in enemy sign, combust, or "
            "afflicted) AND is related to (conjoins, aspects, or is aspected by) "
            "any Grade 1 or Grade 2 Maraka planet."
        ),
        "effect": (
            "Saturn will be the FIRST to kill in preference to all other Maraka "
            "planets regardless of their individual Maraka grade. This override "
            "supersedes the standard hierarchy and activates Saturn as the primary "
            "Maraka for the period in question."
        ),
        "checkable": True,
        "yoga_check_type": "planetary_combination",
        "planets_involved": ["Saturn"],
        "houses_involved": [],
        "phase": 2,
    },
    {
        "yoga_name":      "Moon-Centric Dual Maraka Sweep",
        "sloka":          "ch44-sloka-15-21",
        "group":          "maraka_identification",
        "condition_type": "general_principle",
        "formation": (
            "The Maraka identification engine executes two sweeps: (1) from the "
            "Ascendant (Lagna), and (2) from the Moon sign. In the second sweep, "
            "the 2nd and 12th houses are counted from the Moon sign."
        ),
        "effect": (
            "If the lord of the 2nd or 12th from Moon is a malefic, it qualifies "
            "to cause physical death. If the lord is a benefic, it causes only "
            "disease and distress, not death. When a planet is a Maraka from the "
            "Moon but benefic from the Ascendant, the Moon rule prevails — the "
            "planet causes disease rather than death."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [2, 12],
        "phase": 2,
    },
    {
        "yoga_name":      "First-Rate Exclusive Malefic Designation",
        "sloka":          "ch44-sloka-06",
        "group":          "maraka_identification",
        "condition_type": "general_principle",
        "formation": (
            "A planet classified as an exclusive malefic (natural malefic without "
            "any benefic dignity relief) is related to any Maraka house lord or "
            "occupant, regardless of the exclusive malefic's own house ownership."
        ),
        "effect": (
            "The exclusive malefic is capable of inflicting death regardless of "
            "which house it lords, overriding the normal Grade 1/2/3 hierarchy. "
            "Its Maraka power is activated by the relationship to the Maraka house."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [],
        "phase": 2,
    },
    {
        "yoga_name":      "Node-Signifier Override — Rahu/Ketu Steal Maraka Power",
        "sloka":          "ch44-sloka-22",
        "group":          "maraka_identification",
        "condition_type": "planetary_combination",
        "formation": (
            "Rahu or Ketu joins (conjuncts) a Maraka planet OR occupies the house "
            "of a Maraka planet (2nd or 7th lord's sign)."
        ),
        "effect": (
            "The Node steals the Maraka power from the original Maraka planet and "
            "acts as the primary killer itself during its Dasa or Antar-dasa. "
            "The original Maraka planet's killing power is diminished once the Node "
            "takes over the Maraka signification."
        ),
        "checkable": True,
        "yoga_check_type": "planetary_combination",
        "planets_involved": ["Rahu", "Ketu"],
        "houses_involved": [2, 7],
        "phase": 2,
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # GROUP 2: MARAKA TIMING
    # ═══════════════════════════════════════════════════════════════════════════

    {
        "yoga_name":      "Sub-Period Death Prohibition — Benefic Antar-dasa Buffer",
        "sloka":          "ch44-sloka-08",
        "group":          "maraka_timing",
        "condition_type": "general_principle",
        "formation": (
            "The major Dasa (Maha-dasa) is of a malefic Maraka planet AND the "
            "running sub-period (Antar-dasa) belongs to a benefic planet, even if "
            "the benefic is related to the malefic Maraka."
        ),
        "effect": (
            "Death will NOT occur during this combination. The benefic Antar-dasa "
            "acts as a safety buffer even within a malefic Maraka major period. "
            "Death instead occurs during the sub-period of an unrelated malefic "
            "planet within the same Maha-dasa."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [],
        "phase": 2,
    },
    {
        "yoga_name":      "Lifespan Boundary Classes — Four-Tier Classification",
        "sloka":          "ch44-sloka-09",
        "group":          "maraka_timing",
        "condition_type": "general_principle",
        "formation": (
            "The calculated Ayurdaya (longevity span from Ch 43) is compared to "
            "four boundary thresholds to classify the native into a lifespan tier."
        ),
        "effect": (
            "Short Life: Death before 32 years. "
            "Medium Life: Death between 32 and 64 years. "
            "Long Life: Death between 64 and 100 years. "
            "Supreme Longevity: Life beyond 100 years. "
            "The Maraka Dasa must coincide with the calculated boundary of the "
            "native's tier for physical death to occur."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [],
        "phase": 2,
    },
    {
        "yoga_name":      "Longevity-Maraka Correlation Gate",
        "sloka":          "ch44-sloka-15",
        "group":          "maraka_timing",
        "condition_type": "general_principle",
        "formation": (
            "A Maraka Dasa is running AND the calculated Ayurdaya lifespan window "
            "is compared to the native's current age to determine activation state."
        ),
        "effect": (
            "IF Maraka Dasa coincides with the calculated Ayurdaya end: Physical "
            "death occurs. "
            "IF Maraka Dasa occurs outside the calculated longevity window: "
            "The native experiences 'difficulties equal to death' — severe misery, "
            "disease, or poverty — but not physical death. "
            "This gate is the primary guard against false mortality predictions."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [],
        "phase": 2,
    },
    {
        "yoga_name":      "Star-Based Mortality Timing — Vipat, Pratyak, Vadha",
        "sloka":          "ch44-sloka-09",
        "group":          "maraka_timing",
        "condition_type": "general_principle",
        "formation": (
            "The native's birth Nakshatra is identified. The 3rd (Vipat), 5th "
            "(Pratyak), and 7th (Vadha) Nakshatras counted from birth are the "
            "Killer Asterisms. Their Dasa lords are the Asterism Marakas."
        ),
        "effect": (
            "Short Life natives: The Dasa of the Vipat star (3rd from birth) is "
            "the mortality trigger. "
            "Medium Life natives: The Dasa of the Pratyak star (5th from birth) "
            "is the mortality trigger. "
            "Long Life natives: The Dasa of the Vadha star (7th from birth) is "
            "the mortality trigger. "
            "These asterism-based periods override general house-lord Dasa analysis "
            "and are prioritized in timing calculations."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [],
        "phase": 2,
    },
    {
        "yoga_name":      "Specific Killer Asterisms — 22nd Decanate and Nakshatra Lords",
        "sloka":          "ch44-sloka-19",
        "group":          "maraka_timing",
        "condition_type": "general_principle",
        "formation": (
            "The lord of the 22nd decanate (counted from the Ascendant decanate) "
            "OR the lords of the 23rd, 3rd, 5th, or 7th asterisms from the birth "
            "Nakshatra are identified as Specific Killer Lords."
        ),
        "effect": (
            "These lords acquire the power to terminate life during their respective "
            "Dasa and Antar-dasa periods. They are ranked above standard house-lord "
            "Marakas in timing precision for mortality prediction."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [],
        "phase": 2,
    },
    {
        "yoga_name":      "Sub-Period Triad — 6th Lord Dasa Mortality Window",
        "sloka":          "ch44-sloka-20",
        "group":          "maraka_timing",
        "condition_type": "planetary_combination",
        "formation": (
            "The major Dasa (Maha-dasa) belongs to the lord of the 6th house AND "
            "the sub-period (Antar-dasa) belongs to the lord of the 6th, 8th, "
            "or 12th house."
        ),
        "effect": (
            "A high-mortality window is activated. These specific overlaps of "
            "dushtana lords (6th/8th/12th) in Dasa-Antar-dasa create a potent "
            "mortality trigger. Death is likely if the Longevity-Maraka Correlation "
            "Gate (Logic Unit 44.25) also confirms the native's lifespan boundary "
            "is reached."
        ),
        "checkable": True,
        "yoga_check_type": "planetary_combination",
        "planets_involved": [],
        "houses_involved": [6, 8, 12],
        "phase": 2,
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # GROUP 3: RAHU / KETU
    # ═══════════════════════════════════════════════════════════════════════════

    {
        "yoga_name":      "Rahu/Ketu Killer Status — H2/H7 or Maraka Lord Association",
        "sloka":          "ch44-sloka-22-24",
        "group":          "rahu_ketu",
        "condition_type": "planet_in_house",
        "formation": (
            "Rahu or Ketu occupies the 2nd or 7th house (Condition A), OR Rahu/Ketu "
            "is conjunct with or aspected by the lord of the 2nd or 7th house "
            "(Condition B)."
        ),
        "effect": (
            "The Nodes acquire full Maraka power and can kill during their major "
            "or sub-periods. Restriction: If the Nodes are aspected by or conjunct "
            "with a benefic planet, they cause severe difficulties and disease "
            "rather than physical death."
        ),
        "checkable": True,
        "yoga_check_type": "planet_in_house",
        "planets_involved": ["Rahu", "Ketu"],
        "houses_involved": [2, 7],
        "phase": 2,
    },
    {
        "yoga_name":      "Rahu/Ketu Non-Maraka Exclusion Zones",
        "sloka":          "ch44-sloka-23",
        "group":          "rahu_ketu",
        "condition_type": "planet_in_house",
        "formation": (
            "Rahu or Ketu occupies specific houses other than the 2nd and 7th — "
            "namely houses that do not confer Maraka lordship or Maraka-planet "
            "association upon them."
        ),
        "effect": (
            "In these non-Maraka placements, Rahu and Ketu will NOT act as killers "
            "regardless of other conjunctions, aspects, or dasas running. The Nodes "
            "require either direct H2/H7 placement or Maraka-lord association to "
            "acquire killing power."
        ),
        "checkable": True,
        "yoga_check_type": "planet_in_house",
        "planets_involved": ["Rahu", "Ketu"],
        "houses_involved": [],
        "phase": 2,
    },
    {
        "yoga_name":      "Benefic Aspect on Nodes — Difficulty Not Death",
        "sloka":          "ch44-sloka-24",
        "group":          "rahu_ketu",
        "condition_type": "planetary_combination",
        "formation": (
            "Rahu or Ketu has acquired Maraka status (H2/H7 placement or Maraka-lord "
            "association) AND the Node is aspected by or conjunct with a natural "
            "benefic planet (Jupiter, Venus, Mercury waxing, Moon waxing)."
        ),
        "effect": (
            "The Node's Maraka power is neutralized. Instead of physical death, "
            "the Dasa of the Node causes severe disease, prolonged suffering, "
            "or crisis-level difficulties equivalent to death — but the native survives."
        ),
        "checkable": True,
        "yoga_check_type": "planetary_combination",
        "planets_involved": ["Rahu", "Ketu", "Jupiter", "Venus", "Mercury", "Moon"],
        "houses_involved": [],
        "phase": 2,
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # GROUP 4: CAUSE OF DEATH
    # ═══════════════════════════════════════════════════════════════════════════

    {
        "yoga_name":      "3rd House Planet-Cause Library — Per Planet Diagnosis",
        "sloka":          "ch44-sloka-25-31",
        "group":          "cause_of_death",
        "condition_type": "planet_in_house",
        "formation": (
            "A specific planet occupies the 3rd house of the natal chart."
        ),
        "effect": (
            "Sun in H3: Death by king's/legal punishment or cardiac problems. "
            "Moon in H3: Death by tuberculosis or lung disorders. "
            "Mars in H3: Death by wounds, weapons, fire, electricity, or thirst. "
            "Saturn or Rahu in H3: Death by poison, water, fire, falls from heights, "
            "or confinement. "
            "Mercury in H3: Death by severe fever (typhoid or similar). "
            "Jupiter in H3: Death by swelling, tumors, jaundice, or dropsy. "
            "Venus in H3: Death by urinary disorders or venereal diseases."
        ),
        "checkable": True,
        "yoga_check_type": "planet_in_house",
        "planets_involved": ["Sun", "Moon", "Mars", "Saturn", "Rahu", "Mercury",
                             "Jupiter", "Venus"],
        "houses_involved": [3],
        "phase": 2,
    },
    {
        "yoga_name":      "Multi-Planet H3 — Death by Many Diseases",
        "sloka":          "ch44-sloka-31",
        "group":          "cause_of_death",
        "condition_type": "planet_in_house",
        "formation": (
            "Multiple planets (more than one) occupy the 3rd house simultaneously."
        ),
        "effect": (
            "Death will be caused by a combination of many diseases rather than a "
            "single ailment. The exact diseases are diagnosed by reading each "
            "occupant's cause individually per the 3rd house library."
        ),
        "checkable": True,
        "yoga_check_type": "planet_in_house",
        "planets_involved": [],
        "houses_involved": [3],
        "phase": 2,
    },
    {
        "yoga_name":      "Venus in H3 — Gender-Specific Diagnosis (Female Native)",
        "sloka":          "ch44-sloka-30",
        "group":          "cause_of_death",
        "condition_type": "planet_in_house",
        "formation": (
            "Venus occupies the 3rd house AND the native is female."
        ),
        "effect": (
            "For a female native specifically: death involving leucorrhea, "
            "urinary disorders, or venereal diseases. The gender-specific "
            "sub-diagnosis overrides the general Venus-in-H3 reading for "
            "male natives when the native is female."
        ),
        "checkable": True,
        "yoga_check_type": "planet_in_house",
        "planets_involved": ["Venus"],
        "houses_involved": [3],
        "phase": 2,
    },
    {
        "yoga_name":      "Mixed H3 Occupation — Multiple Reasons Diagnosis",
        "sloka":          "ch44-sloka-31",
        "group":          "cause_of_death",
        "condition_type": "planet_in_house",
        "formation": (
            "The 3rd house contains a mix of planets with conflicting natures "
            "(benefic and malefic together, or planets representing "
            "different cause categories)."
        ),
        "effect": (
            "Death occurs for various reasons or under mixed environmental "
            "circumstances. No single cause dominates; the diagnosis reflects "
            "the combined influence of all occupants."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [3],
        "phase": 2,
    },
    {
        "yoga_name":      "Moon-Sign Lordship Marakas — Malefic vs Benefic Lords",
        "sloka":          "ch44-sloka-15-17",
        "group":          "cause_of_death",
        "condition_type": "general_principle",
        "formation": (
            "The 2nd and 12th houses are counted from the Moon sign (not Lagna). "
            "The lords of these houses are identified as Moon-centric Marakas."
        ),
        "effect": (
            "If the lord of the 2nd or 12th from Moon is a malefic: it is qualified "
            "to bring physical death during its Dasa. "
            "If the lord is a benefic: it triggers only disease and distress, not "
            "physical death. The Moon-centric sweep must be run in parallel with "
            "the Ascendant-based sweep and conflicts resolved per the dual-sweep protocol."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [2, 12],
        "phase": 2,
    },
    {
        "yoga_name":      "Death Environment — Place and Locality Diagnosis",
        "sloka":          "ch44-sloka-32",
        "group":          "cause_of_death",
        "condition_type": "general_principle",
        "formation": (
            "The nature and placement of planets in the 3rd house, combined with "
            "the sign type of the 3rd house, determine the place and locality "
            "of death."
        ),
        "effect": (
            "Place of death (planet type): Benefic in H3 → Death in a shrine or "
            "sacred place. Malefic in H3 → Death in a sinful, inauspicious place. "
            "Locality (sign type): Movable sign in H3 (Aries/Cancer/Libra/Capricorn) "
            "→ Death in a foreign place. Fixed sign in H3 (Taurus/Leo/Scorpio/ "
            "Aquarius) → Death in own house. Dual sign in H3 (Gemini/Virgo/ "
            "Sagittarius/Pisces) → Death while traveling or on the way."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [3],
        "phase": 2,
    },
    {
        "yoga_name":      "3rd House Occupant Priority — Misnomer Prevention",
        "sloka":          "ch44-sloka-25",
        "group":          "cause_of_death",
        "condition_type": "general_principle",
        "formation": (
            "The cause-of-death engine must not rely solely on the 2nd lord "
            "for death cause. The 3rd house occupants are equally capable "
            "death-givers and must be checked."
        ),
        "effect": (
            "Prioritize 3rd house occupants as death-cause indicators alongside "
            "2nd lord analysis to avoid 'misnomer' errors in prediction. "
            "The 3rd house planet-cause library (per-planet mapping) governs the "
            "nature of death, independent of the Maraka house hierarchy."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [3],
        "phase": 2,
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # GROUP 5: EIGHTH HOUSE LIBRARY
    # ═══════════════════════════════════════════════════════════════════════════

    {
        "yoga_name":      "8th House Occupancy Cause-of-Death Library",
        "sloka":          "ch44-sloka-35-36",
        "group":          "eighth_house_library",
        "condition_type": "planet_in_house",
        "formation": (
            "A specific planet occupies the 8th house of the natal chart."
        ),
        "effect": (
            "Sun in H8: Death by fire. "
            "Moon in H8: Death by water. "
            "Mars in H8: Death by weapons. "
            "Mercury in H8: Death by fever. "
            "Jupiter in H8: Death by diseases (internal, chronic). "
            "Venus in H8: Death by hunger or starvation. "
            "Saturn in H8: Death by thirst."
        ),
        "checkable": True,
        "yoga_check_type": "planet_in_house",
        "planets_involved": ["Sun", "Moon", "Mars", "Mercury", "Jupiter",
                             "Venus", "Saturn"],
        "houses_involved": [8],
        "phase": 2,
    },
    {
        "yoga_name":      "Sacred Passing Yoga — Death in Shrine",
        "sloka":          "ch44-sloka-37",
        "group":          "eighth_house_library",
        "condition_type": "planetary_combination",
        "formation": (
            "The 8th house is occupied by a benefic OR aspected by a benefic, "
            "AND the 9th lord is conjunct with a benefic planet."
        ),
        "effect": (
            "The native is guaranteed to die in a shrine, temple, or sacred place. "
            "Both conditions must be simultaneously satisfied: the benefic influence "
            "on H8 plus the 9th lord's benefic conjunction confirm the sacred "
            "environment of death."
        ),
        "checkable": True,
        "yoga_check_type": "planetary_combination",
        "planets_involved": [],
        "houses_involved": [8, 9],
        "phase": 2,
    },
    {
        "yoga_name":      "Fate of the Corpse — 22nd Decanate Diagnosis",
        "sloka":          "ch44-sloka-38-40",
        "group":          "eighth_house_library",
        "condition_type": "general_principle",
        "formation": (
            "The 22nd decanate (counted from the Ascendant decanate) is identified "
            "and classified as Benefic, Malefic, Mixed, or Serpent decanate."
        ),
        "effect": (
            "Benefic 8th decanate: Corpse is burnt in fire as per the Shastras "
            "(traditional cremation). "
            "Malefic 8th decanate: Body is thrown away in water (immersed). "
            "Mixed 8th decanate: Dead body dries up (abandoned or delayed funeral). "
            "Serpent 8th decanate (Cancer 2nd/3rd, Scorpio 1st, Pisces 3rd): "
            "Body is eaten by animals or crows."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [8],
        "phase": 2,
    },
    {
        "yoga_name":      "Serpent Decanate Identification",
        "sloka":          "ch44-sloka-39",
        "group":          "eighth_house_library",
        "condition_type": "general_principle",
        "formation": (
            "The 8th house decanate (or 22nd decanate from Ascendant) falls in "
            "one of the following positions: Cancer 2nd decanate, Cancer 3rd "
            "decanate, Scorpio 1st decanate, or Pisces 3rd decanate."
        ),
        "effect": (
            "The decanate is classified as a Serpent decanate. Applied to funeral "
            "fate: the dead body will be eaten by animals and crows rather than "
            "receiving a traditional funeral. This is the most inauspicious corpse "
            "treatment outcome."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [8],
        "phase": 2,
    },
    {
        "yoga_name":      "Post-Death World — Vacant H12/H7/H6/H8 Fallback",
        "sloka":          "ch44-sloka-43-45",
        "group":          "eighth_house_library",
        "condition_type": "general_principle",
        "formation": (
            "The 12th, 7th, 6th, and 8th houses are all vacant (no planet occupies "
            "them). The fallback rule activates: identify the stronger of the "
            "decanate lords of the 6th and 8th houses."
        ),
        "effect": (
            "The stronger decanate lord determines the native's post-death world. "
            "If Jupiter decanate lord: World of Gods. "
            "If Venus or Moon decanate lord: World of Manes. "
            "If Mars or Sun decanate lord: Earth (rebirth). "
            "If Mercury or Saturn decanate lord: Hell. "
            "This fallback only applies when the primary diagnostic houses are vacant."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [6, 7, 8, 12],
        "phase": 2,
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # GROUP 6: DEATH ENVIRONMENT
    # ═══════════════════════════════════════════════════════════════════════════

    {
        "yoga_name":      "Pre-Natal Abode — Luminary Decanate Diagnosis",
        "sloka":          "ch44-sloka-33-34",
        "group":          "death_environment",
        "condition_type": "general_principle",
        "formation": (
            "The strongest luminary (Sun or Moon, whichever has greater Shadbala "
            "or dignity) is identified. The decanate it occupies in the natal chart "
            "is classified by its planetary ruler."
        ),
        "effect": (
            "Jupiter decanate: The native originates from and returns to the World "
            "of Gods. "
            "Venus or Moon decanate: The native originates from and returns to the "
            "World of Manes (ancestors). "
            "Sun or Mars decanate: The native originates from and returns to the "
            "World of the Dead (Yama, implying rebirth). "
            "Mercury or Saturn decanate: The native originates from and returns "
            "to Hell."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": ["Sun", "Moon"],
        "houses_involved": [],
        "phase": 2,
    },
    {
        "yoga_name":      "Post-Death World — Terminal House Planet Mapping",
        "sloka":          "ch44-sloka-43-45",
        "group":          "death_environment",
        "condition_type": "general_principle",
        "formation": (
            "Planets occupying the terminal houses (12th, 7th, 6th, 8th) of the "
            "natal chart are identified. Each planet in these houses indicates a "
            "specific post-death destination."
        ),
        "effect": (
            "Jupiter in terminal houses: Heaven (World of Gods). "
            "Moon or Venus in terminal houses: World of Manes. "
            "Mars or Sun in terminal houses: Earth (rebirth cycle). "
            "Mercury or Saturn in terminal houses: Hell. "
            "If multiple terminal houses are occupied, the strongest planet governs. "
            "If all terminal houses are vacant, the decanate fallback rule applies."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": ["Jupiter", "Moon", "Venus", "Mars", "Sun",
                             "Mercury", "Saturn"],
        "houses_involved": [6, 7, 8, 12],
        "phase": 2,
    },
    {
        "yoga_name":      "Afterlife Status Ranking — Dignity of World Planet",
        "sloka":          "ch44-sloka-45",
        "group":          "death_environment",
        "condition_type": "general_principle",
        "formation": (
            "The planet indicating the native's post-death world (from terminal "
            "house or decanate analysis) is assessed for its dignity at the time "
            "of birth: exalted, own sign, friendly, neutral, enemy, debilitated."
        ),
        "effect": (
            "The dignity level of the world-indicating planet determines the "
            "native's status within that afterlife world. Higher dignity → Higher "
            "rank and enjoyment in the world. Exalted → Supreme status. "
            "Debilitated → Low or suffering status in that world."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [],
        "phase": 2,
    },
    {
        "yoga_name":      "Second-Grade Killer Hierarchy — H6 and H11 Lords",
        "sloka":          "ch44-sloka-07",
        "group":          "death_environment",
        "condition_type": "general_principle",
        "formation": (
            "After the Grade 1 Marakas (H12/H3/H8/H7/H2 lords and occupants) are "
            "identified, the engine sweeps for Grade 2 killers: lords or occupants "
            "of the 6th and 11th houses."
        ),
        "effect": (
            "The 6th and 11th lords are secondary killers with significant Maraka "
            "power. Grade 3 (H5/H9/H10/H4/H1) kill only when conjunction overrides "
            "or asterism triggers activate them per the secondary criteria in "
            "slokas 15-21. The hierarchy must be applied in descending grade order "
            "to identify the primary Maraka dasa."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [6, 11],
        "phase": 2,
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # GROUP 7: CONSCIOUSNESS AND FATE
    # ═══════════════════════════════════════════════════════════════════════════

    {
        "yoga_name":      "Consciousness at Death — Jupiter/Venus in H3",
        "sloka":          "ch44-sloka-33",
        "group":          "consciousness_fate",
        "condition_type": "planet_in_house",
        "formation": (
            "Jupiter or Venus occupies the 3rd house of the natal chart."
        ),
        "effect": (
            "The native will maintain full consciousness at the time of death. "
            "Death arrives with awareness intact — the native can participate in "
            "final rituals, prayers, or farewells. "
            "Any other planet in H3 indicates unconsciousness or loss of awareness "
            "before death."
        ),
        "checkable": True,
        "yoga_check_type": "planet_in_house",
        "planets_involved": ["Jupiter", "Venus"],
        "houses_involved": [3],
        "phase": 2,
    },
    {
        "yoga_name":      "Childhood Vulnerability Protocol — Age Under 20",
        "sloka":          "ch44-sloka-10-14",
        "group":          "consciousness_fate",
        "condition_type": "general_principle",
        "formation": (
            "The native's current age is under 20 years and a Maraka Dasa or "
            "adverse transit is running."
        ),
        "effect": (
            "Longevity cannot be decided with certainty for a child under 20. "
            "Standard Maraka and Ayurdaya calculations are probabilistic, not "
            "definitive, in this window. "
            "Protective remedy: Sacred recitations (mantras) and religious "
            "offerings (ghee poured into consecrated fire) must be performed "
            "to protect the child's life."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [],
        "phase": 2,
    },
    {
        "yoga_name":      "Pre-20 Premature Death — Father, Mother, Past Karma",
        "sloka":          "ch44-sloka-10-14",
        "group":          "consciousness_fate",
        "condition_type": "general_principle",
        "formation": (
            "A native under 20 years shows strong mortality indicators (Maraka Dasa "
            "active, severe 8th house afflictions, no protective yogas)."
        ),
        "effect": (
            "Premature death in the under-20 window is diagnosed as the result of "
            "the sins of the father, the mother, or the native's own previous birth "
            "(karmic debt). This is a metaphysical root-cause diagnosis, not a "
            "planetary one. The standard Maraka rules are considered secondary to "
            "the karmic liability in this age bracket."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [],
        "phase": 2,
    },
    {
        "yoga_name":      "Childhood Remedy — Sacred Recitations and Ghee Offering",
        "sloka":          "ch44-sloka-13",
        "group":          "consciousness_fate",
        "condition_type": "general_principle",
        "formation": (
            "A child under 20 is diagnosed as being in a mortality-risk window "
            "based on Maraka Dasa + adverse planetary patterns."
        ),
        "effect": (
            "Protective remedy prescribed: perform sacred recitations (Vedic "
            "mantras, particularly Maha Mrityunjaya) and pour oblations of ghee "
            "into a consecrated ritual fire (Havan/Homam). "
            "This is the canonical BPHS remedy for childhood mortality risk and "
            "must be flagged as a ritual recommendation for human review."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [],
        "phase": 2,
        "remedy_category": ["ritual"],
    },
    {
        "yoga_name":      "Unconsciousness at Death — Non-Jupiter/Venus in H3",
        "sloka":          "ch44-sloka-33",
        "group":          "consciousness_fate",
        "condition_type": "planet_in_house",
        "formation": (
            "Any planet other than Jupiter or Venus occupies the 3rd house, OR "
            "the 3rd house is occupied by malefic planets (Saturn, Mars, Rahu, "
            "Ketu, Sun)."
        ),
        "effect": (
            "The native will lose consciousness or awareness before death arrives. "
            "The death is not peaceful or aware; the native may be in a coma, "
            "delirious, or otherwise unaware at the moment of passing."
        ),
        "checkable": True,
        "yoga_check_type": "planet_in_house",
        "planets_involved": ["Sun", "Moon", "Mars", "Mercury", "Saturn",
                             "Rahu", "Ketu"],
        "houses_involved": [3],
        "phase": 2,
    },
    {
        "yoga_name":      "Asterism Dasa Master Logic — Priority Ordering",
        "sloka":          "ch44-sloka-19",
        "group":          "consciousness_fate",
        "condition_type": "general_principle",
        "formation": (
            "Multiple Maraka indicators are active simultaneously: house-lord "
            "Marakas, Moon-centric Marakas, Asterism Marakas (Vipat/Pratyak/Vadha), "
            "and 22nd decanate/specific asterism lords."
        ),
        "effect": (
            "Priority order for timing death: "
            "(1) Asterism Marakas (Vipat, Pratyak, or Vadha per lifespan class) "
            "— highest timing precision. "
            "(2) 22nd decanate lord and 23rd/3rd/5th/7th asterism lords. "
            "(3) Sub-period Triad (6th lord Dasa + 6th/8th/12th Antar-dasa). "
            "(4) Grade 1 house-lord Marakas. "
            "(5) Saturn override if applicable. "
            "All must pass the Longevity-Maraka Correlation Gate before death is "
            "confirmed."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [],
        "phase": 2,
    },
    {
        "yoga_name":      "Corpse Consciousness Diagnostic — Full Decision Tree",
        "sloka":          "ch44-sloka-33-40",
        "group":          "consciousness_fate",
        "condition_type": "general_principle",
        "formation": (
            "The engine evaluates: (1) H3 occupants for consciousness quality, "
            "(2) 22nd decanate type for corpse treatment, and (3) terminal house "
            "planets for post-death world. All three are independent diagnostic "
            "axes that run in parallel."
        ),
        "effect": (
            "Axis 1 — Consciousness: Jupiter/Venus in H3 → Aware death. "
            "Others in H3 → Unconscious death. "
            "Axis 2 — Corpse: Benefic 22nd decanate → Cremation. Malefic → Water. "
            "Mixed → Dries up. Serpent → Eaten by animals. "
            "Axis 3 — World: Terminal house planets per planet-world mapping, "
            "with dignity modifier for status within that world. "
            "If terminal houses vacant, decanate lord fallback applies."
        ),
        "checkable": False,
        "yoga_check_type": "manual",
        "planets_involved": [],
        "houses_involved": [3, 6, 7, 8, 12],
        "phase": 2,
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# BUILDER
# ─────────────────────────────────────────────────────────────────────────────

def _build_rules() -> list[dict]:
    rules: list[dict] = []
    now = datetime.now(timezone.utc).isoformat()

    group_counters: dict[str, int] = {}
    group_prefixes = {
        "maraka_identification": "MI",
        "maraka_timing":         "MT",
        "rahu_ketu":             "RK",
        "cause_of_death":        "CD",
        "eighth_house_library":  "EH",
        "death_environment":     "DE",
        "consciousness_fate":    "CF",
    }

    for entry in YOGA_DATA:
        group = entry["group"]
        group_counters[group] = group_counters.get(group, 0) + 1
        seq = group_counters[group]
        prefix = group_prefixes[group]
        rid = f"bphs-ch44-{prefix}{seq:02d}"

        yoga_name      = entry["yoga_name"]
        ctype          = entry["condition_type"]
        formation      = entry["formation"]
        effect         = entry["effect"]
        sloka          = entry.get("sloka", "")
        checkable      = entry.get("checkable", False)
        ycheck_type    = entry.get("yoga_check_type", "manual")
        planets        = entry.get("planets_involved", [])
        houses         = entry.get("houses_involved", [])
        phase          = entry.get("phase", 2)
        remedy_cat     = entry.get("remedy_category", [])

        detailed = f"{formation}\n\nEffect: {effect}"

        ycheck: dict = {"type": ycheck_type, "checkable": checkable}
        if checkable and ctype == "planet_in_house" and houses:
            ycheck["houses"] = houses
            ycheck["planets"] = planets
        if checkable and ctype == "planetary_combination":
            ycheck["planets"] = planets
            if houses:
                ycheck["houses"] = houses

        rule: dict = {
            "rule_id":    rid,
            "science_id": SCIENCE,
            "source": {
                "book":         BOOK,
                "book_id":      BOOK_ID,
                "chapter":      CHAPTER,
                "chapter_name": CHAP_NAME,
                "sloka":        sloka,
                "batch_id":     BATCH_ID,
                "primary":      BOOK,
                "page_ref":     None,
                "passage_ref_id": None,
            },
            "condition": {
                "type":              ctype,
                "sub_type":          "maraka_diagnostic",
                "yoga_name":         yoga_name,
                "yoga_group":        group,
                "yoga_group_label":  group.replace("_", " ").title(),
                "planets_involved":  planets,
                "houses_involved":   houses,
                "yoga_check":        ycheck,
                "trigger_condition": formation,
            },
            "interpretation": {
                "summary": yoga_name,          # always yoga_name — avoids truncation flags
                "detailed": detailed,
                "full_text_passages": [
                    {"text": detailed, "confidence": "HIGH"}
                ],
                "remedy":           [],
                "timing_indicator": False,
                "strength_modifier": None,
            },
            "metadata": {
                "phase":            phase,
                "checkable":        checkable,
                "yoga_group":       group,
                "yoga_group_label": group.replace("_", " ").title(),
                "remedy_category":  remedy_cat,
                "source_quality":   "PRIMARY",
                "tags":             [group, "maraka", "longevity", "ch44",
                                     "bphs", "vol1"],
            },
            "confidence": "HIGH",
            "approval_status": "pending_review",
            "validation": {
                "verdict":       "pending",
                "flag_reason":   None,
                "validated_by":  None,
                "validated_at":  None,
            },
            "created_at":  now,
            "updated_at":  now,
        }
        rules.append(rule)

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest BPHS Ch 44 Maraka rules into MongoDB"
    )
    parser.add_argument("--dry-run",  action="store_true",
                        help="Build rules and print summary without uploading")
    parser.add_argument("--save",     metavar="FILE",
                        help="Save JSON to FILE (use with --dry-run)")
    parser.add_argument("--upload",   metavar="FILE",
                        help="Upload JSON FILE to MongoDB")
    parser.add_argument("--mongo-url", default="",
                        help="MongoDB connection URL (required for --upload)")
    parser.add_argument("--db-name",  default="horoscope_db")
    args = parser.parse_args()

    if not args.dry_run and not args.upload:
        parser.print_help()
        sys.exit(1)

    # ── DRY RUN ──────────────────────────────────────────────────────────────
    if args.dry_run:
        rules = _build_rules()
        print(f"\n{'='*60}")
        print(f"  BPHS Ch 44 — Dry Run")
        print(f"  Total rules built: {len(rules)}")
        print(f"  Batch ID:          {BATCH_ID}")
        print(f"{'='*60}")

        from collections import Counter
        groups: Counter = Counter()
        checkable_count = 0
        for r in rules:
            groups[r["metadata"]["yoga_group"]] += 1
            if r["metadata"]["checkable"]:
                checkable_count += 1

        for g, cnt in groups.items():
            print(f"  {cnt:3d}  {g}")
        print(f"{'─'*60}")
        print(f"  Checkable: {checkable_count} / {len(rules)}")

        if args.save:
            out = Path(args.save)
            out.write_text(json.dumps(rules, indent=2, ensure_ascii=False))
            print(f"\n  ✅ Saved {len(rules)} rules → {out}")

        print()
        return

    # ── UPLOAD ───────────────────────────────────────────────────────────────
    if args.upload:
        src = Path(args.upload)
        if not src.exists():
            print(f"ERROR: {src} not found — run --dry-run --save first")
            sys.exit(1)

        rules = json.loads(src.read_text())

        try:
            from pymongo import MongoClient, UpdateOne
        except ImportError:
            print("ERROR: pymongo not installed — pip install pymongo")
            sys.exit(1)

        if not args.mongo_url:
            print("ERROR: --mongo-url is required for upload")
            sys.exit(1)

        client = MongoClient(args.mongo_url)
        col = client[args.db_name]["interpretation_rules"]

        ops = [
            UpdateOne(
                {"rule_id": r["rule_id"]},
                {"$set": r},
                upsert=True,
            )
            for r in rules
        ]
        result = col.bulk_write(ops, ordered=False)
        print(f"\n  ✅ Inserted {result.upserted_count} / "
              f"Updated {result.modified_count} rules "
              f"→ {args.db_name}.interpretation_rules")
        client.close()


if __name__ == "__main__":
    main()
