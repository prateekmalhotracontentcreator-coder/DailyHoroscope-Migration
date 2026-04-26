#!/usr/bin/env python3
"""
ingest_lalkitab_ch20_v1.py — Lal Kitab Chapter 20: Diseases

48 rules total across 8 groups:
   3  GP anatomy mapping  (sign/house/planet → body parts)
   3  GP engine logic     (diagnostic sequence, functional roles, interaction matrix)
  11  Planetary combination disease rules (YOG)
  10  Planet disease library — split from DOS-01 (one per planet)
   8  Nail diagnosis rules — split from DOS-02 (one per symptom-planet)
   9  Planet symptom + remedy rules (REM, dosha/disease)
   2  General trial rules (REM-10/11)
   2  Meta gate rules (debilitation gate, succession rule)

Source: Lal Kitab Ch 20 original + Notebook LM V2 decode (reviewed).
Extraction: hard_coded — zero API calls.

Decisions locked:
- DOS-01/DOS-02 split into individual rules for engine queryability
- GP engine sub-types preserved via condition.sub_type
- symptoms.physical/environmental → interpretation.physical_markers
- succour remedies folded into remedies array with category: "succour"
- YOG-11 (Varshaphalam) flagged checkable:false + requires:"varshaphalam"

Standard workflow:
  Step 1 — Dry run + save:
    python3 scripts/ingest_lalkitab_ch20_v1.py --dry-run --save scripts/lalkitab_ch20_rules.json

  Step 2 — Review JSON; amend as needed.

  Step 3 — Upload:
    python3 scripts/ingest_lalkitab_ch20_v1.py \\
      --upload scripts/lalkitab_ch20_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 4 — Validate:
    python3 scripts/validate_rules.py \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id lalkitab-ch20-v1-20260427
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Constants ──────────────────────────────────────────────────────────────────

SCIENCE   = "jyotish"
BOOK      = "Lal Kitab"
BOOK_ID   = "lal-kitab"
CHAPTER   = 20
CHAP_NAME = "Diseases"
BATCH_ID  = "lalkitab-ch20-v1-20260427"

# ── Shared skeleton ────────────────────────────────────────────────────────────

def _base_doc(rule_id: str, now: str) -> dict:
    return {
        "rule_id":    rule_id,
        "science_id": SCIENCE,
        "source": {
            "primary":  BOOK_ID,
            "book":     BOOK,
            "chapter":  CHAPTER,
            "chapter_name": CHAP_NAME,
            "batch_id": BATCH_ID,
        },
        "metadata": {
            "extraction_method": "hard_coded",
            "source_note":       "lalkitab-ch20-v2-decode",
            "created_at":        now,
        },
        "approval_status": "pending_review",
        "confidence": {
            "score":   0.80,
            "band":    "HIGH",
            "rationale": "Hard-coded from Notebook LM V2 decode — reviewed against source.",
        },
    }


# ── ❶ GP ANATOMY MAPPING RULES ────────────────────────────────────────────────

SIGN_BODY_PARTS = [
    ("Aries",       ["head", "stomach", "brain", "eyes"]),
    ("Taurus",      ["mouth", "eye", "bone", "flesh"]),
    ("Gemini",      ["throat", "respiratory tube", "shoulder", "arms"]),
    ("Cancer",      ["chest", "lungs", "blood"]),
    ("Leo",         ["back", "heart", "intestine", "kidney", "stomach"]),
    ("Virgo",       ["upper part of abdomen", "intestine", "bone", "flesh"]),
    ("Libra",       ["waist", "liver", "breathing", "genitals"]),
    ("Scorpio",     ["genital", "liver", "testicles"]),
    ("Sagittarius", ["thighs", "veins of thighs", "rectum", "buttocks"]),
    ("Capricorn",   ["bones at the joint", "flesh", "knees"]),
    ("Aquarius",    ["knee", "bone of knee", "flesh", "respiratory system"]),
    ("Pisces",      ["toes and its veins", "feet"]),
]

HOUSE_BODY_PARTS = [
    (1,  ["mouth", "teeth", "tongue", "forehead", "head"]),
    (2,  ["right eye", "face"]),
    (3,  ["ear", "neck", "hand", "shoulder", "respiratory tube"]),
    (4,  ["stomach", "shoulder", "chest"]),
    (5,  ["upper part of waist", "heart"]),
    (6,  ["right leg", "genital", "stomach", "kidney", "intestine"]),
    (7,  ["navel", "central part of abdomen", "genitals"]),
    (8,  ["left leg", "genital", "testicles"]),
    (9,  ["upper part of waist", "buttocks"]),
    (10, ["stomach", "shoulder", "knees"]),
    (11, ["left hand", "ear", "neck", "lower leg"]),
    (12, ["left eye", "sole of feet", "feet"]),
]

PLANET_BODY_PARTS = [
    ("Sun",         ["whole body", "right part of body"]),
    ("Moon",        ["heart", "left part of face"]),
    ("Mars Benefic",["liver", "upper lip"]),
    ("Mars Malefic",["liver", "lower lip"]),
    ("Mercury",     ["brain", "neurological system", "tongue", "teeth"]),
    ("Jupiter",     ["neck", "nose"]),
    ("Venus",       ["voice system", "cheeks"]),
    ("Saturn",      ["eyes", "eyebrows", "hair"]),
    ("Rahu",        ["shaking of head", "head", "chin"]),
    ("Ketu",        ["torso", "spinal cord", "knees", "toes", "paws", "ear"]),
]


def build_gp_anatomy_rules(now: str) -> list[dict]:
    rules = []

    # GP-01: Sign → body parts
    doc = _base_doc("lalkitab-ch20-gp-sign", now)
    doc.update({
        "condition": {
            "type":     "general_principle",
            "sub_type": "anatomy_mapping",
            "description": "Kaal Purush sign-to-body-part governance (Lal Kitab Ch 20).",
            "yoga_check": {"type": "none", "checkable": False},
        },
        "interpretation": {
            "summary": "Kaal Purush sign-to-body-part mapping: affliction of a sign indicates disease of its governed parts.",
            "detailed": (
                "Aries: head/stomach/brain/eyes. Taurus: mouth/eye/bone/flesh. "
                "Gemini: throat/respiratory/shoulder/arms. Cancer: chest/lungs/blood. "
                "Leo: back/heart/intestine/kidney. Virgo: upper abdomen/intestine. "
                "Libra: waist/liver/breathing/genitals. Scorpio: genital/liver/testicles. "
                "Sagittarius: thighs/veins/rectum/buttocks. Capricorn: joints/flesh/knees. "
                "Aquarius: knee/bone/flesh/respiratory. Pisces: toes/veins/feet."
            ),
            "lookup_table": [
                {"sign": s, "body_parts": bp} for s, bp in SIGN_BODY_PARTS
            ],
            "life_domains": ["health"],
            "is_benefic":   None,
        },
        "tags": ["anatomy", "kaal_purush", "sign_mapping", "disease"],
    })
    rules.append(doc)

    # GP-02: House → body parts
    doc = _base_doc("lalkitab-ch20-gp-house", now)
    doc.update({
        "condition": {
            "type":     "general_principle",
            "sub_type": "anatomy_mapping",
            "description": "Kaal Purush house-to-body-part governance (Lal Kitab Ch 20).",
            "yoga_check": {"type": "none", "checkable": False},
        },
        "interpretation": {
            "summary": "Kaal Purush house-to-body-part mapping: affliction of a house indicates disease of its governed parts.",
            "detailed": (
                "H1: mouth/teeth/tongue/forehead. H2: right eye/face. "
                "H3: ear/neck/hand/shoulder. H4: stomach/shoulder/chest. "
                "H5: upper waist/heart. H6: right leg/genital/kidney. "
                "H7: navel/central abdomen/genitals. H8: left leg/genital/testicles. "
                "H9: upper waist/buttocks. H10: stomach/shoulder/knees. "
                "H11: left hand/ear/neck/lower leg. H12: left eye/sole of feet/feet."
            ),
            "lookup_table": [
                {"house": h, "body_parts": bp} for h, bp in HOUSE_BODY_PARTS
            ],
            "life_domains": ["health"],
            "is_benefic":   None,
        },
        "tags": ["anatomy", "kaal_purush", "house_mapping", "disease"],
    })
    rules.append(doc)

    # GP-03: Planet → body parts
    doc = _base_doc("lalkitab-ch20-gp-planet", now)
    doc.update({
        "condition": {
            "type":     "general_principle",
            "sub_type": "anatomy_mapping",
            "description": "Planetary anatomical governance — conditioning planet logic (Lal Kitab Ch 20, p.170).",
            "yoga_check": {"type": "none", "checkable": False},
        },
        "interpretation": {
            "summary": "Each planet governs specific anatomical zones. Mars benefic/malefic state determined by conditioning planets (Sun/Mercury vs Sun/Saturn).",
            "detailed": (
                "Sun: whole body/right side. Moon: heart/left face. "
                "Mars Benefic (with Sun/Mercury): liver/upper lip. "
                "Mars Malefic (with Sun/Saturn): liver/lower lip. "
                "Mercury: brain/neurological/tongue/teeth. Jupiter: neck/nose. "
                "Venus: voice/cheeks. Saturn: eyes/eyebrows/hair. "
                "Rahu: head/chin/shaking of head. Ketu: torso/spinal cord/knees/toes/ear."
            ),
            "lookup_table": [
                {"planet": p, "body_parts": bp} for p, bp in PLANET_BODY_PARTS
            ],
            "life_domains": ["health"],
            "is_benefic":   None,
        },
        "tags": ["anatomy", "planetary_governance", "conditioning_planet", "disease"],
    })
    rules.append(doc)

    return rules


# ── ❷ GP ENGINE / LOGIC RULES ─────────────────────────────────────────────────

def build_gp_engine_rules(now: str) -> list[dict]:
    rules = []

    # GP-04: Diagnostic sequence
    doc = _base_doc("lalkitab-ch20-gp-seq", now)
    doc.update({
        "condition": {
            "type":     "general_principle",
            "sub_type": "diagnostic_sequence",
            "description": "Disease onset validation: malefic in H3 AND H9 triggers scan sequence 3→8→5→11→4.",
            "primary_trigger": {"houses": [3, 9], "requirement": "both_malefic"},
            "scan_sequence":   [3, 8, 5, 11, 4],
            "yoga_check": {"type": "none", "checkable": False},
        },
        "interpretation": {
            "summary": (
                "Disease is triggered when H3 AND H9 are malefic. The engine then scans "
                "H3→H8→H5→H11→H4 in order. The first non-vacant house identifies the "
                "primary affliction. If any house in the sequence is afflicted, the native "
                "becomes a patient."
            ),
            "detailed": (
                "Primary trigger (p.168): malefic in H3 AND H9 simultaneously activates "
                "disease state. Affliction search order (Varshaphalam basis): "
                "3 → 8 → 5 → 11 → 4. If a house is vacant, proceed to the next. "
                "H3 = ferocity/doom. H5 = immunity/soul injection. H9 = basis/foundation. "
                "H2+H4 = type of illness. H10 = form and velocity of disease."
            ),
            "life_domains": ["health"],
            "is_benefic":   None,
        },
        "tags": ["diagnostic_engine", "disease_trigger", "house_sequence"],
    })
    rules.append(doc)

    # GP-05: Functional roles of houses
    doc = _base_doc("lalkitab-ch20-gp-roles", now)
    doc.update({
        "condition": {
            "type":     "general_principle",
            "sub_type": "functional_roles",
            "description": "Functional role assignment to houses in the disease diagnostic engine.",
            "yoga_check": {"type": "none", "checkable": False},
        },
        "interpretation": {
            "summary": "Each key house has a specific functional role in disease diagnosis: H3=doom, H5=immunity, H9=basis, H2/H4=illness type, H10=velocity.",
            "detailed": (
                "H3: Expresses ferocity and possibility of illness — the 'Doom' house. "
                "H5: Capability to fight disease; infuses soul in the body — the immunity house. "
                "H9: The foundational basis/support for H5 and the soul/body. "
                "H2 and H4: Define the specific type or nature of the illness. "
                "H10: Defines the form and velocity (speed of progression) of the disease."
            ),
            "house_roles": [
                {"houses": [3],    "function": "ferocity_and_doom"},
                {"houses": [5],    "function": "immunity_and_resistance"},
                {"houses": [9],    "function": "soul_basis_and_body_stability"},
                {"houses": [2, 4], "function": "illness_type_definition"},
                {"houses": [10],   "function": "velocity_and_form_definition"},
            ],
            "life_domains": ["health"],
            "is_benefic":   None,
        },
        "tags": ["diagnostic_engine", "house_roles", "disease"],
    })
    rules.append(doc)

    # GP-06: House 3 and House 5 interaction matrix + debilitation chain
    doc = _base_doc("lalkitab-ch20-gp-interact", now)
    doc.update({
        "condition": {
            "type":     "general_principle",
            "sub_type": "interaction_logic",
            "description": "H3 and H5 support/injury interaction matrices + H3/H9 debilitation chain.",
            "yoga_check": {"type": "none", "checkable": False},
        },
        "interpretation": {
            "summary": (
                "H3 interaction: H1=unexpected injury, H2=help, H6=deception, H7=helpful, "
                "H8=unworthy deeds, H11=mutual help. H5 interaction: H1=mutual help, "
                "H4=help, H7=unexpected injury, H8=deception, H9=helpful, H10=confrontation. "
                "When H3 AND H9 both debilitated, H5 automatically debilitates (loss of immunity). "
                "Exception: Sun or Moon in H9 protects H5 from debilitation."
            ),
            "detailed": (
                "House 3 interaction matrix — H3 with: "
                "H1: unexpected injury; H2: will help; H6: will deceive; "
                "H7: will be helpful; H8: will make native do unworthy deeds; H11: mutual help. "
                "House 5 interaction matrix — H5 with: "
                "H1: mutual help; H4: will help; H7: unexpected injury; "
                "H8: will deceive; H9: will be helpful; H10: will confront. "
                "Debilitation chain: if H3 AND H9 are both debilitated, H5 automatically "
                "becomes debilitated — complete loss of immunity. "
                "Solar/Lunar exception: if Sun or Moon is in H9, H5 is protected "
                "even if H3 is weak."
            ),
            "h3_interactions": [
                {"with_house": 1,  "outcome": "unexpected_injury"},
                {"with_house": 2,  "outcome": "external_help"},
                {"with_house": 6,  "outcome": "deception_threat"},
                {"with_house": 7,  "outcome": "assistance_granted"},
                {"with_house": 8,  "outcome": "unworthy_deeds"},
                {"with_house": 11, "outcome": "mutual_help"},
            ],
            "h5_interactions": [
                {"with_house": 1,  "outcome": "mutual_help"},
                {"with_house": 4,  "outcome": "external_help"},
                {"with_house": 7,  "outcome": "unexpected_injury"},
                {"with_house": 8,  "outcome": "deception_threat"},
                {"with_house": 9,  "outcome": "assistance_granted"},
                {"with_house": 10, "outcome": "adversarial_confrontation"},
            ],
            "life_domains": ["health"],
            "is_benefic":   None,
        },
        "tags": ["diagnostic_engine", "house_interaction", "debilitation_chain"],
    })
    rules.append(doc)

    return rules


# ── ❸ PLANETARY COMBINATION (YOG) RULES ───────────────────────────────────────

YOG_RULES: list[dict] = [
    {
        "rule_id":  "lalkitab-ch20-yog-01",
        "summary":  "Malefic occupancy or aspect on Aries, with Mars lord afflicted: injury or disease of head or mind.",
        "detailed": (
            "Aries contains a malefic (Sun/Saturn/Mars/Rahu/Ketu) OR is aspected by a malefic, "
            "AND Mars (lord of Aries) is conjugated with a malefic. When this triple condition "
            "is met, the native is subject to injury or disease of the head or mind."
        ),
        "planets_involved": ["Mars"],
        "houses_involved":  [],
        "yoga_check": {
            "type": "planetary_combination", "checkable": True,
            "description": "Malefic in/aspecting Aries AND Mars lord afflicted by malefic conjunction.",
        },
        "is_benefic":   False,
        "life_domains": ["health"],
        "tags": ["disease", "aries", "malefic_affliction"],
    },
    {
        "rule_id":  "lalkitab-ch20-yog-02",
        "summary":  "Malefic affliction of Libra or Venus/its lord: genital disease or impotency.",
        "detailed": (
            "Libra contains a malefic OR is aspected by malefic; OR Venus is aspected by malefic; "
            "OR the ruler of Libra (Venus) is with malefic or aspected by malefic. "
            "Any of these conditions indicates disease related to genitals or impotency."
        ),
        "planets_involved": ["Venus"],
        "houses_involved":  [],
        "yoga_check": {
            "type": "planetary_combination", "checkable": True,
            "description": "Multi-OR: malefic in/aspecting Libra, or Venus afflicted, or Libra lord afflicted.",
        },
        "is_benefic":   False,
        "life_domains": ["health", "relationships"],
        "tags": ["disease", "libra", "impotency", "malefic_affliction"],
    },
    {
        "rule_id":  "lalkitab-ch20-yog-03",
        "summary":  "Jupiter conjunct Rahu or Mercury: asthma and respiratory/lung trouble.",
        "detailed": (
            "Jupiter in conjunction with Rahu, OR Jupiter in conjunction with Mercury, "
            "produces asthma and respiratory and lung trouble."
        ),
        "planets_involved": ["Jupiter", "Rahu", "Mercury"],
        "houses_involved":  [],
        "yoga_check": {
            "type": "planetary_combination", "checkable": True,
            "description": "Jupiter-Rahu conjunction OR Jupiter-Mercury conjunction.",
        },
        "is_benefic":   False,
        "life_domains": ["health"],
        "tags": ["disease", "asthma", "lung", "conjunction"],
    },
    {
        "rule_id":  "lalkitab-ch20-yog-04",
        "summary":  "Rahu and Ketu in interaction: madness or pneumonia.",
        "detailed": "Rahu and Ketu interacting (conjunction or opposition) produces madness or pneumonia.",
        "planets_involved": ["Rahu", "Ketu"],
        "houses_involved":  [],
        "yoga_check": {
            "type": "planetary_combination", "checkable": True,
            "description": "Rahu-Ketu conjunction or opposition.",
        },
        "is_benefic":   False,
        "life_domains": ["health", "mind"],
        "tags": ["disease", "madness", "pneumonia", "conjunction"],
    },
    {
        "rule_id":  "lalkitab-ch20-yog-05",
        "summary":  "Sun with Venus or Mercury, together with Jupiter: tuberculosis and asthma.",
        "detailed": (
            "Sun is with Venus OR Mercury, AND Jupiter is also involved in the combination. "
            "This triple conjunction indicates tuberculosis and asthma."
        ),
        "planets_involved": ["Sun", "Venus", "Mercury", "Jupiter"],
        "houses_involved":  [],
        "yoga_check": {
            "type": "planetary_combination", "checkable": True,
            "description": "Sun + (Venus OR Mercury) + Jupiter in combination.",
        },
        "is_benefic":   False,
        "life_domains": ["health"],
        "tags": ["disease", "tuberculosis", "asthma", "conjunction"],
    },
    {
        "rule_id":  "lalkitab-ch20-yog-06",
        "summary":  "Mars conjunct Saturn: leprosy and blood infection.",
        "detailed": "Conjunction of Mars and Saturn produces leprosy and blood infection.",
        "planets_involved": ["Mars", "Saturn"],
        "houses_involved":  [],
        "yoga_check": {
            "type": "planetary_combination", "checkable": True,
            "description": "Mars-Saturn conjunction.",
        },
        "is_benefic":   False,
        "life_domains": ["health"],
        "tags": ["disease", "leprosy", "blood_infection", "conjunction"],
    },
    {
        "rule_id":  "lalkitab-ch20-yog-07",
        "summary":  "Venus conjunct Rahu: impotence.",
        "detailed": "Conjunction of Venus and Rahu produces impotence.",
        "planets_involved": ["Venus", "Rahu"],
        "houses_involved":  [],
        "yoga_check": {
            "type": "planetary_combination", "checkable": True,
            "description": "Venus-Rahu conjunction.",
        },
        "is_benefic":   False,
        "life_domains": ["health", "relationships"],
        "tags": ["disease", "impotence", "conjunction"],
    },
    {
        "rule_id":  "lalkitab-ch20-yog-08",
        "summary":  "Venus conjunct Ketu: premature ejaculation.",
        "detailed": "Conjunction of Venus and Ketu produces premature ejaculation.",
        "planets_involved": ["Venus", "Ketu"],
        "houses_involved":  [],
        "yoga_check": {
            "type": "planetary_combination", "checkable": True,
            "description": "Venus-Ketu conjunction.",
        },
        "is_benefic":   False,
        "life_domains": ["health", "relationships"],
        "tags": ["disease", "premature_ejaculation", "conjunction"],
    },
    {
        "rule_id":  "lalkitab-ch20-yog-09",
        "summary":  "Jupiter with Mars Malefic (Sun-Saturn): jaundice.",
        "detailed": (
            "Jupiter in conjunction with Mars when Mars is in malefic state "
            "(conditioned by Sun-Saturn) produces jaundice."
        ),
        "planets_involved": ["Jupiter", "Mars", "Sun", "Saturn"],
        "houses_involved":  [],
        "yoga_check": {
            "type": "planetary_combination", "checkable": True,
            "description": "Jupiter + Mars Malefic (Sun-Saturn conditioning).",
        },
        "is_benefic":   False,
        "life_domains": ["health"],
        "tags": ["disease", "jaundice", "conjunction"],
    },
    {
        "rule_id":  "lalkitab-ch20-yog-10",
        "summary":  "Moon with Mercury (conjunction) or Moon clashing with Mars: glandular pathologies.",
        "detailed": (
            "Moon in conjunction with Mercury OR Moon in opposition/clash with Mars "
            "produces glandular pathologies."
        ),
        "planets_involved": ["Moon", "Mercury", "Mars"],
        "houses_involved":  [],
        "yoga_check": {
            "type": "planetary_combination", "checkable": True,
            "description": "Moon-Mercury conjunction OR Moon-Mars clash.",
        },
        "is_benefic":   False,
        "life_domains": ["health"],
        "tags": ["disease", "glands", "conjunction"],
    },
    {
        "rule_id":  "lalkitab-ch20-yog-11",
        "summary":  "Varshaphalam: malefic with Sun/Moon entering houses 1/6/7/8/10 triggers acute illness attack.",
        "detailed": (
            "Natal anchor: Mercury, Venus, or a malefic is conjugated with Sun or Moon. "
            "Varshaphalam trigger: in the annual chart, these planets enter houses 1, 6, 7, 8, or 10. "
            "When both conditions are met, an acute attack of illness is activated. "
            "Remedy: perform planetary remedies for the specific malefic involved."
        ),
        "planets_involved": ["Sun", "Moon", "Mercury", "Venus"],
        "houses_involved":  [1, 6, 7, 8, 10],
        "yoga_check": {
            "type": "varshaphalam_transit", "checkable": False,
            "requires": "varshaphalam",
            "description": "Requires annual Varshaphalam chart injection — outside current engine scope.",
        },
        "is_benefic":   False,
        "life_domains": ["health"],
        "tags": ["disease", "varshaphalam", "illness_attack"],
    },
]


def build_yog_rules(now: str) -> list[dict]:
    rules = []
    for r in YOG_RULES:
        doc = _base_doc(r["rule_id"], now)
        doc.update({
            "condition": {
                "type":             "planetary_combination",
                "planets_involved": r["planets_involved"],
                "houses_involved":  r.get("houses_involved", []),
                "yoga_check":       r["yoga_check"],
            },
            "interpretation": {
                "summary":      r["summary"],
                "detailed":     r["detailed"],
                "life_domains": r["life_domains"],
                "is_benefic":   r["is_benefic"],
            },
            "tags": r["tags"],
        })
        rules.append(doc)
    return rules


# ── ❹ PLANET DISEASE LIBRARY — split from DOS-01 ──────────────────────────────

DOS_PLANET_DISEASES: list[dict] = [
    {
        "planet": "Sun",
        "diseases": [
            "diphtheria", "eye disease", "indigestion", "rheumatoid arthritis",
            "blood pressure", "neurological weakness", "foaming of mouth", "paralysis",
        ],
    },
    {
        "planet": "Moon",
        "diseases": [
            "headache", "minor accidents", "heart disease", "constipation",
            "intestinal disease", "urinary disease", "wind formation", "eye disease",
        ],
    },
    {
        "planet": "Mars Benefic",
        "diseases": ["abdominal disease", "diarrhoea", "bile", "kidney disease"],
    },
    {
        "planet": "Mars Malefic",
        "diseases": [
            "accident", "paralysis", "heart disease", "blood pressure",
            "piles", "boil", "chronic pain",
        ],
    },
    {
        "planet": "Mercury",
        "diseases": [
            "skin disease", "neurological weakness", "anxiety", "mental weakness",
            "mental illness", "tongue disease", "dental disease",
        ],
    },
    {
        "planet": "Jupiter",
        "diseases": [
            "skin disease", "ringworm", "irritation", "diabetes", "septicemia",
            "bile disorder", "stomach pain", "anxiety", "impotence",
            "disinterest in pleasure", "blood disease", "wind",
            "respiratory and lung trouble",
        ],
    },
    {
        "planet": "Venus",
        "diseases": [
            "lung disease", "seminal weakness", "genital weakness", "weak heart",
            "urinary disease", "cough-related disease", "cold", "itching", "skin disease",
        ],
    },
    {
        "planet": "Saturn",
        "diseases": [
            "wind disease", "rheumatoid arthritis", "physical weakness", "constipation",
            "blood pressure", "leprosy", "urinary disease", "baldness",
            "pain in nose and ear", "eyesight issues", "asthma", "wheezing", "cough",
        ],
    },
    {
        "planet": "Rahu",
        "diseases": ["fever", "mental illness", "plague"],
    },
    {
        "planet": "Ketu",
        "diseases": [
            "urinary infection", "boils and warts", "filarial (galgand)",
            "testicles and venereal disease", "pain in hands and legs",
            "ear disease", "spinal cord disease",
        ],
    },
]


def build_dos_planet_rules(now: str) -> list[dict]:
    rules = []
    for entry in DOS_PLANET_DISEASES:
        planet_slug = entry["planet"].lower().replace(" ", "_")
        rule_id = f"lalkitab-ch20-dos-{planet_slug}"
        doc = _base_doc(rule_id, now)
        diseases_text = "; ".join(entry["diseases"])
        doc.update({
            "condition": {
                "type":             "dosha",
                "sub_type":         "disease",
                "dosha_type":       "disease_logic",
                "planets_involved": [entry["planet"]],
                "yoga_check": {
                    "type":      "planet_affliction",
                    "checkable": True,
                    "planet":    entry["planet"],
                    "description": f"Affliction of {entry['planet']} activates disease domain.",
                },
            },
            "interpretation": {
                "summary":      f"Afflicted {entry['planet']} is associated with: {diseases_text}.",
                "detailed": (
                    f"Traditional Lal Kitab disease catalog for {entry['planet']} (afflicted state). "
                    f"Diseases governed: {diseases_text}."
                ),
                "diseases":     entry["diseases"],
                "life_domains": ["health"],
                "is_benefic":   False,
            },
            "tags": ["disease", "planet_disease_catalog", planet_slug],
        })
        rules.append(doc)
    return rules


# ── ❺ NAIL DIAGNOSIS RULES — split from DOS-02 ────────────────────────────────

NAIL_RULES: list[dict] = [
    {
        "slug":    "mercury-color-change",
        "symptom": "General color change of hand nails",
        "planet":  "Mercury",
        "outcome": "Mental illness governed by Mercury.",
        "remedy":  "Treat Mercury.",
    },
    {
        "slug":    "rahu-blue",
        "symptom": "Nails turn blue",
        "planet":  "Rahu",
        "outcome": "Imminent blood dysfunction related to Rahu.",
        "remedy":  "Treat Rahu.",
    },
    {
        "slug":    "venus-short-white",
        "symptom": "Nails turn short and white",
        "planet":  "Venus",
        "outcome": "Anaemic disease governed by Venus.",
        "remedy":  "Treat Venus.",
    },
    {
        "slug":    "jupiter-small-pale",
        "symptom": "Nails turn small and pale",
        "planet":  "Jupiter",
        "outcome": "Heart disease related to Jupiter.",
        "remedy":  "Treat Jupiter.",
    },
    {
        "slug":    "saturn-black",
        "symptom": "Nails turn black",
        "planet":  "Saturn",
        "outcome": "Saturn-related diseases; high expenditure in treatment.",
        "remedy":  "Treat Saturn.",
    },
    {
        "slug":    "yellowish-pulmonary",
        "symptom": "Nails turn yellowish",
        "planet":  None,
        "outcome": "Lung and respiratory trouble.",
        "remedy":  "General trial of sweet breads (see lalkitab-ch20-trial-bread).",
    },
    {
        "slug":    "rahu-thin-silvery",
        "symptom": "Nails turn thin, irregular, or silvery",
        "planet":  "Rahu",
        "outcome": "Rahu-related affliction.",
        "remedy":  "Treat Rahu.",
    },
    {
        "slug":    "ketu-spotty",
        "symptom": "Nails turn spotty, deep colored, black, or white",
        "planet":  "Ketu",
        "outcome": "Ketu-related affliction.",
        "remedy":  "Treat Ketu.",
    },
]


def build_nail_rules(now: str) -> list[dict]:
    rules = []
    for entry in NAIL_RULES:
        rule_id = f"lalkitab-ch20-nail-{entry['slug']}"
        doc = _base_doc(rule_id, now)
        planet_tag = entry["planet"].lower() if entry["planet"] else "general"
        doc.update({
            "condition": {
                "type":             "dosha",
                "sub_type":         "disease",
                "dosha_type":       "disease_logic",
                "planets_involved": [entry["planet"]] if entry["planet"] else [],
                "yoga_check": {"type": "none", "checkable": False},
            },
            "interpretation": {
                "summary":  f"Nail symptom: {entry['symptom']} → {entry['outcome']}",
                "detailed": (
                    f"Lal Kitab nail diagnosis logic (Ch 20). Symptom: {entry['symptom']}. "
                    f"Planetary attribution: {entry['planet'] or 'General/non-specific'}. "
                    f"Outcome: {entry['outcome']} Remedy action: {entry['remedy']}"
                ),
                "physical_markers": [
                    {"category": "physical_symptom", "text": f"Nail symptom: {entry['symptom']}"},
                ],
                "remedies": [
                    {"text": entry["remedy"], "category": "ritual"},
                ],
                "life_domains": ["health"],
                "is_benefic":   False,
            },
            "tags": ["disease", "nail_diagnosis", planet_tag],
        })
        rules.append(doc)
    return rules


# ── ❻ PLANET SYMPTOM + REMEDY RULES (REM) ─────────────────────────────────────

REM_RULES: list[dict] = [
    {
        "planet": "Sun",
        "slug":   "sun",
        "physical_symptoms": [
            "Body parts turn inflexible and movement is difficult",
            "Native always drools",
        ],
        "environmental_omens": [
            "Red cow or brown buffalo dies or is lost",
        ],
        "remedies": [
            {"text": "Consume small amount of sweet (jaggery, sugar, or chocolate) and drink water before initiating work", "category": "lifestyle", "duration": "daily"},
        ],
    },
    {
        "planet": "Moon",
        "slug":   "moon",
        "physical_symptoms": [
            "Power to feel weakens",
        ],
        "environmental_omens": [
            "Well, pond, or hand pump stops working or dries up",
            "Milk-giving pets die",
        ],
        "remedies": [
            {"text": "Touch feet of elders and accept blessings", "category": "lifestyle", "duration": "daily"},
        ],
    },
    {
        "planet": "Mars",
        "slug":   "mars",
        "physical_symptoms": [
            "Joint pain",
            "Anemia",
            "Excessive anger and fighting",
        ],
        "environmental_omens": [
            "No progeny, or progeny dies soon after birth, or progeny becomes impaired",
        ],
        "remedies": [
            {"text": "Apply white kohl (surma) in the eyes", "category": "ritual", "duration": "occasional"},
        ],
    },
    {
        "planet": "Mercury",
        "slug":   "mercury",
        "physical_symptoms": [
            "Teeth are broken",
            "Smell ability weakens",
            "Power to copulate weakens",
        ],
        "environmental_omens": [],
        "remedies": [
            {"text": "Maintain dental hygiene", "category": "ritual", "duration": "daily"},
            {"text": "Pierce nose", "category": "ritual", "duration": "once"},
        ],
    },
    {
        "planet": "Jupiter",
        "slug":   "jupiter",
        "physical_symptoms": [
            "Baldness",
            "Habit of wearing garland around neck",
        ],
        "environmental_omens": [
            "Education interrupted in the middle",
            "False allegations and rumours propagate",
        ],
        "remedies": [
            {"text": "Apply saffron or yellow tilak on forehead", "category": "ritual", "duration": "daily"},
            {"text": "Keep nose dry and clear nose before starting work", "category": "ritual", "duration": "daily"},
        ],
    },
    {
        "planet": "Venus",
        "slug":   "venus",
        "physical_symptoms": [
            "Skin disease",
            "Premature ejaculation",
            "Thumb becomes weak or incapacitated",
        ],
        "environmental_omens": [],
        "remedies": [
            {"text": "Wear properly cleaned clothes and live hygienically", "category": "lifestyle", "duration": "daily"},
            {"text": "Execute remedies for Mercury (lalkitab-ch20-rem-mercury) and pierce nose", "category": "succour", "duration": "once"},
        ],
    },
    {
        "planet": "Saturn",
        "slug":   "saturn",
        "physical_symptoms": [
            "Hair falls from eyebrows or eyelids",
        ],
        "environmental_omens": [
            "Buffalo dies",
            "Fire occurs at home",
            "House collapses or is damaged",
        ],
        "remedies": [
            {"text": "Donate iron", "category": "ritual", "duration": "occasional"},
            {"text": "Clean mouth with babool datoon (toothstick)", "category": "ritual", "duration": "daily"},
            {"text": "Offer bread to crow", "category": "ritual", "duration": "43 days"},
            {"text": "Float coconut in the river", "category": "succour", "duration": "occasional"},
        ],
    },
    {
        "planet": "Rahu",
        "slug":   "rahu",
        "physical_symptoms": [
            "Nails of hand fall off",
            "Mind does not work (cognitive failure)",
        ],
        "environmental_omens": [
            "Black dog dies",
            "Rise in number of enemies",
        ],
        "remedies": [
            {"text": "Maintain a choti (braided tress) on head", "category": "lifestyle", "duration": "continuous"},
            {"text": "Reside in joint family", "category": "lifestyle", "duration": "continuous"},
            {"text": "Maintain good relations with in-laws", "category": "lifestyle", "duration": "continuous"},
        ],
    },
    {
        "planet": "Ketu",
        "slug":   "ketu",
        "physical_symptoms": [
            "Nails of feet fall off",
            "Urinary infection",
            "Joint pain",
        ],
        "environmental_omens": [
            "Progeny remains sick",
        ],
        "remedies": [
            {"text": "Keep a pet dog", "category": "ritual", "duration": "continuous"},
            {"text": "Pierce ear", "category": "ritual", "duration": "once"},
            {"text": "Execute remedies for Moon (lalkitab-ch20-rem-moon)", "category": "succour", "duration": "occasional"},
        ],
    },
]


def build_rem_rules(now: str) -> list[dict]:
    rules = []
    for r in REM_RULES:
        rule_id = f"lalkitab-ch20-rem-{r['slug']}"
        doc = _base_doc(rule_id, now)
        all_symptoms = (
            [{"category": "physical_symptom",    "text": s} for s in r["physical_symptoms"]] +
            [{"category": "environmental_omen",  "text": s} for s in r["environmental_omens"]]
        )
        remedies_text = "; ".join(rem["text"] for rem in r["remedies"])
        doc.update({
            "condition": {
                "type":             "dosha",
                "sub_type":         "disease",
                "dosha_type":       "disease_logic",
                "planets_involved": [r["planet"]],
                "yoga_check": {
                    "type":      "planet_affliction",
                    "checkable": True,
                    "planet":    r["planet"],
                    "description": f"{r['planet']} in inauspicious state triggers these symptoms.",
                },
            },
            "interpretation": {
                "summary": (
                    f"Inauspicious {r['planet']}: "
                    + "; ".join(r["physical_symptoms"][:2])
                    + ("." if r["physical_symptoms"] else "")
                ),
                "detailed": (
                    f"When {r['planet']} becomes inauspicious the following manifest. "
                    f"Physical symptoms: {'; '.join(r['physical_symptoms']) or 'None recorded'}. "
                    f"Environmental omens: {'; '.join(r['environmental_omens']) or 'None recorded'}. "
                    f"Remedies: {remedies_text}."
                ),
                "physical_markers": all_symptoms,
                "remedies":         r["remedies"],
                "life_domains":     ["health"],
                "is_benefic":       False,
            },
            "tags": ["disease", "inauspicious_planet", r["slug"], "symptoms", "remedies"],
        })
        rules.append(doc)
    return rules


# ── ❼ GENERAL TRIAL RULES ─────────────────────────────────────────────────────

def build_trial_rules(now: str) -> list[dict]:
    rules = []

    # REM-10: Sweet bread calculation
    doc = _base_doc("lalkitab-ch20-trial-bread", now)
    doc.update({
        "condition": {
            "type":     "general_principle",
            "sub_type": "general_trial",
            "description": "Sweet bread offering for chronic/resistant diseases with multi-planet house occupancy.",
            "yoga_check": {"type": "none", "checkable": False},
        },
        "interpretation": {
            "summary": (
                "General trial for chronic illness or resistant diseases: calculate quantity of "
                "sweet breads as (family count + average monthly guests + non-zero buffer). "
                "Offer monthly to animals, dogs, and crows."
            ),
            "detailed": (
                "Lal Kitab general trial for chronic or resistant disease where multiple planets "
                "occupy one house, creating conflict. Calculation formula: "
                "Quantity = (Family_Count + Avg_Monthly_Guests) + extra_buffer (non-zero). "
                "Prepare calculated number of sweet breads and offer once a month to animals, "
                "dogs, and crows. Applies when individual planetary remedies are insufficient."
            ),
            "remedies": [
                {
                    "text": "Calculate sweet breads: (family members + avg monthly guests + buffer). Offer monthly to animals/dogs/crows.",
                    "category": "offering",
                    "duration": "monthly",
                },
            ],
            "life_domains": ["health"],
            "is_benefic":   None,
        },
        "tags": ["disease", "general_trial", "sweet_bread", "chronic_illness"],
    })
    rules.append(doc)

    # REM-11: Temple/charity offerings
    doc = _base_doc("lalkitab-ch20-trial-charity", now)
    doc.update({
        "condition": {
            "type":     "general_principle",
            "sub_type": "general_trial",
            "description": "Temple and charity offerings for general disease obstruction.",
            "yoga_check": {"type": "none", "checkable": False},
        },
        "interpretation": {
            "summary": (
                "General trial for health blockage: distribute pumpkin porridge at temple monthly; "
                "place coins at patient's head-post and give to sweeper in the morning; "
                "throw coins on the path when approaching a crematory or graveyard."
            ),
            "detailed": (
                "Lal Kitab general trial for general disease obstruction. Three remedies: "
                "1. Distribute porridge of ripe pumpkin at a temple, once monthly. "
                "2. Place coins at the head-post of the patient at night; give them to a sweeper in the morning. "
                "3. Throw coins on the path when approaching a crematory or graveyard."
            ),
            "remedies": [
                {"text": "Distribute porridge of ripe pumpkin at temple", "category": "offering", "duration": "monthly"},
                {"text": "Place coins at head-post of patient at night; give to sweeper in morning", "category": "ritual", "duration": "daily"},
                {"text": "Throw coins on path when approaching crematory or graveyard", "category": "ritual", "duration": "as_encountered"},
            ],
            "life_domains": ["health"],
            "is_benefic":   None,
        },
        "tags": ["disease", "general_trial", "charity", "temple"],
    })
    rules.append(doc)

    return rules


# ── ❽ META GATE RULES ─────────────────────────────────────────────────────────

def build_meta_rules(now: str) -> list[dict]:
    rules = []

    # MET-01: Debilitation gate
    doc = _base_doc("lalkitab-ch20-met-gate", now)
    doc.update({
        "condition": {
            "type":     "general_principle",
            "sub_type": "debilitation_gate",
            "description": "Sun or Moon in H9 protects H5 from automatic debilitation.",
            "yoga_check": {
                "type":        "planet_in_house",
                "checkable":   True,
                "planets":     ["Sun", "Moon"],
                "houses":      [9],
                "operator":    "any",
                "description": "Sun OR Moon in H9 activates H5 protection override.",
            },
        },
        "interpretation": {
            "summary": (
                "Exception rule: when Sun or Moon is placed in the 9th house, the 5th house "
                "(immunity) is protected and does NOT become debilitated — even if H3 is weak."
            ),
            "detailed": (
                "Debilitation chain rule: if H3 AND H9 are both debilitated, H5 automatically "
                "debilitates (complete loss of immunity). Solar/Lunar exception overrides this: "
                "if Sun or Moon is in H9, H5 is protected regardless of H3 weakness. "
                "This exception preserves the native's disease-fighting capacity."
            ),
            "life_domains": ["health"],
            "is_benefic":   True,
        },
        "tags": ["disease", "debilitation_gate", "immunity_protection", "h5", "h9"],
    })
    rules.append(doc)

    # MET-02: Succession rule
    doc = _base_doc("lalkitab-ch20-met-succession", now)
    doc.update({
        "condition": {
            "type":     "general_principle",
            "sub_type": "succession_rule",
            "description": "In multi-planet houses, the planet that diminishes others takes priority.",
            "yoga_check": {"type": "none", "checkable": False},
        },
        "interpretation": {
            "summary": (
                "Succession/priority rule: in a house occupied by multiple planets, prioritize "
                "the planet that diminishes the influence of others. Example: Jupiter with Rahu "
                "destroys the effect of Rahu."
            ),
            "detailed": (
                "When multiple planets occupy a single house in the natal chart, the disease "
                "diagnostic engine must apply the succession rule: identify the planet whose "
                "presence reduces or negates the influence of the others, and treat it as the "
                "primary signifier. Classical example: Jupiter sitting with Rahu destroys "
                "the effect of Rahu — Jupiter's benefic nature overrides Rahu's malefic influence "
                "in the disease context."
            ),
            "life_domains": ["health"],
            "is_benefic":   None,
        },
        "tags": ["disease", "succession_rule", "multi_planet", "priority_logic"],
    })
    rules.append(doc)

    return rules


# ── ASSEMBLE ALL RULES ────────────────────────────────────────────────────────

def build_all_rules() -> list[dict]:
    now = datetime.now(timezone.utc).isoformat()
    rules: list[dict] = []
    rules += build_gp_anatomy_rules(now)   # 3
    rules += build_gp_engine_rules(now)    # 3
    rules += build_yog_rules(now)          # 11
    rules += build_dos_planet_rules(now)   # 10
    rules += build_nail_rules(now)         # 8
    rules += build_rem_rules(now)          # 9
    rules += build_trial_rules(now)        # 2
    rules += build_meta_rules(now)         # 2
    return rules                           # 48 total


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description="Ingest Lal Kitab Ch 20 — Diseases")
    p.add_argument("--dry-run",  action="store_true", help="Build rules and show summary without uploading")
    p.add_argument("--save",     metavar="FILE",       help="Save dry-run JSON to file")
    p.add_argument("--upload",   metavar="FILE",       help="Upload rules from saved JSON to MongoDB")
    p.add_argument("--mongo-url", default="",          help="MongoDB Atlas URL (required for --upload)")
    p.add_argument("--db-name",   default="horoscope_db")
    return p.parse_args()


def print_summary(rules: list[dict]) -> None:
    from collections import Counter
    print(f"\nLal Kitab Ch 20 — {CHAP_NAME}")
    print(f"  Total rules  : {len(rules)}")
    checkable = sum(
        1 for r in rules
        if (r.get("condition") or {}).get("yoga_check", {}).get("checkable", False)
    )
    print(f"  Checkable    : {checkable} / {len(rules)} ({checkable * 100 // len(rules)}%)")
    print(f"  Batch ID     : {BATCH_ID}")
    ctype_counts = Counter(r["condition"]["type"] for r in rules)
    sub_counts   = Counter(
        r["condition"].get("sub_type", "—")
        for r in rules if r["condition"].get("sub_type")
    )
    print(f"\n  By condition type:")
    for ctype, cnt in ctype_counts.most_common():
        print(f"    {ctype:<30} {cnt} rules")
    print(f"\n  By sub_type:")
    for sub, cnt in sub_counts.most_common():
        print(f"    {sub:<30} {cnt} rules")
    print(f"\n  Rule IDs:")
    for r in rules:
        yc = r["condition"].get("yoga_check", {})
        chk = "✓" if yc.get("checkable") else "✗"
        print(f"    {r['rule_id']:<40} [{chk}]")


def main():
    args = parse_args()

    if args.upload:
        # ── Upload mode: read saved JSON → insert into MongoDB ──────────────
        if not args.mongo_url:
            sys.exit("ERROR: --mongo-url required for --upload")
        path = Path(args.upload)
        if not path.exists():
            sys.exit(f"ERROR: file not found: {path}")
        rules = json.loads(path.read_text(encoding="utf-8"))
        print(f"Loaded {len(rules)} rules from {path}")

        try:
            from pymongo import MongoClient
        except ImportError:
            sys.exit("ERROR: pymongo not installed")

        client = MongoClient(args.mongo_url)
        coll = client[args.db_name]["interpretation_rules"]
        result = coll.insert_many(rules)
        print(f"✅ Inserted {len(result.inserted_ids)} rules into {args.db_name}.interpretation_rules")
        client.close()
        return

    # ── Dry-run / build mode ─────────────────────────────────────────────────
    rules = build_all_rules()
    print_summary(rules)

    if args.save:
        path = Path(args.save)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n  Saved {len(rules)} rules → {path}")
    elif not args.dry_run:
        print("\n  (use --dry-run to suppress this, or --save FILE to write JSON)")


if __name__ == "__main__":
    main()
