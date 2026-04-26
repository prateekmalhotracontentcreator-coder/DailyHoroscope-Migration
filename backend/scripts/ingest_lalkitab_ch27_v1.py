#!/usr/bin/env python3
"""
ingest_lalkitab_ch27_v1.py — Lal Kitab Chapter 27: Lords of Planets, Parts of Body and Objects

99 rules total across 6 groups:
  10  Planetary Correspondence (C1-C10) — lord, colour, gem, animal, body, objects
   9  Affliction / Remedy Engine (R) — per planet symptoms + worship/donation/totaka remedies
  10  Conditional Prohibited Donation rules (P1-P10)
  12  Planet Transfer Placement protocol (H1-H12)
  49  Mental Wave Engine — 42 sections of mind (W1-W49)
   9  Invisible Planets / Totaka trials (IP1-IP9) — hard-coded from PDF extract

Source: Lal Kitab Ch 27 original PDF + Notebook LM V2 decode (reviewed).
Invisible Planets section (IP1-IP9) extracted directly from PDF JSON (not in V2).
Mars Benefic Objects (C3) left empty — confirmed column misalignment in source table;
  Moon Objects cross-confirmed as Rice/Milk/Silver from Section 3.

Standard workflow:
  Step 1 — Dry run + save:
    python3 scripts/ingest_lalkitab_ch27_v1.py --dry-run --save scripts/lalkitab_ch27_rules.json

  Step 2 — Review JSON; amend as needed.

  Step 3 — Upload:
    python3 scripts/ingest_lalkitab_ch27_v1.py \\
      --upload scripts/lalkitab_ch27_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 4 — Validate:
    python3 scripts/validate_rules.py \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id lalkitab-ch27-v1-20260427
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
CHAPTER   = 27
CHAP_NAME = "Lords of Planets, Parts of Body and Objects"
BATCH_ID  = "lalkitab-ch27-v1-20260427"

# ── Shared skeleton ────────────────────────────────────────────────────────────

def _base_doc(rule_id: str, now: str) -> dict:
    return {
        "rule_id":    rule_id,
        "science_id": SCIENCE,
        "source": {
            "primary":      BOOK_ID,
            "book":         BOOK,
            "chapter":      CHAPTER,
            "chapter_name": CHAP_NAME,
            "batch_id":     BATCH_ID,
        },
        "metadata": {
            "extraction_method": "hard_coded",
            "source_note":       "lalkitab-ch27-v2-decode + pdf-json-extract",
            "created_at":        now,
        },
        "approval_status": "pending_review",
        "confidence": {
            "score":     0.80,
            "band":      "HIGH",
            "rationale": "Hard-coded from Notebook LM V2 decode reviewed against source PDF.",
        },
    }


# ── ❶ PLANETARY CORRESPONDENCE RULES (C1-C10) ─────────────────────────────────

# Each entry: (rule_suffix, planet_label, lord, colour, gem_metal, animal, body_parts, objects, notes)
CORRESPONDENCE_DATA = [
    (
        "sun", "Sun",
        "Vishnu",
        "Wheatish",
        ["Red copper"],
        ["Cow", "Monkey"],
        ["Body", "Right face"],
        ["Red wheat", "Copper"],
        None,
    ),
    (
        "moon", "Moon",
        "Shiva",
        "Milky white",
        ["Pearl", "Silver"],
        ["Horse", "Mare"],
        ["Heart", "Left face"],
        ["Rice", "Milk", "Silver"],
        None,
    ),
    (
        "mars-benefic", "Mars Benefic",
        "Hanuman",
        "Red",
        ["Non-shining red gems"],
        ["Kite"],
        ["Liver", "Upper lip"],
        [],   # Source table column misalignment — data cross-confirms as Moon's; needs_review
        "Mars Benefic Objects field empty: source table column misalignment confirmed. "
        "Rice/Milk/Silver belong to Moon (cross-confirmed Section 3). Correct value unknown.",
    ),
    (
        "mars-malefic", "Mars Malefic",
        "Ghost and spirit",
        "Red",
        ["Bright red gem"],
        ["Camel", "Deer"],
        ["Liver", "Upper lip"],
        ["Red masoor pulse"],
        None,
    ),
    (
        "mercury", "Mercury",
        "Durga",
        "Green",
        ["Diamond", "Emerald"],
        ["Sheep", "Goat", "Bat"],
        ["Brain", "Teeth", "Neuron", "Tongue", "Nose"],
        ["Whole moong"],
        None,
    ),
    (
        "jupiter", "Jupiter",
        "Brahma",
        "Yellow",
        ["Gold", "Yellow sapphire"],
        ["Lion", "Lioness"],
        ["Neck", "Nose"],
        ["Gram pulse", "Gold"],
        None,
    ),
    (
        "venus", "Venus",
        "Lakshmi",
        "Curd-like",
        ["Pearl", "Fine soil"],
        ["Cow", "Bull"],
        ["Voice system", "Cheek"],
        ["Butter", "Camphor", "Pearl"],
        None,
    ),
    (
        "saturn", "Saturn",
        "Bhairav",
        "Black",
        ["Iron", "Steel"],
        ["Buffalo"],
        ["Eye", "Eyebrow", "Hair"],
        ["Whole black gram (Urad)"],
        None,
    ),
    (
        "rahu", "Rahu",
        "Saraswati",
        "Blue",
        ["Blue sapphire", "Gomed"],
        ["Wild rats"],
        ["Head", "Chin", "Head-shaking"],
        ["Mustard", "Blue sapphire"],
        None,
    ),
    (
        "ketu", "Ketu",
        "Ganesh",
        "Spotted",
        ["Vaidurya"],
        ["Dog", "Donkey", "Pig", "Lizard"],
        ["Torso", "Spinal cord", "Knees", "Toes", "Palm", "Ear"],
        ["Sesame"],
        None,
    ),
]


def build_correspondence_rules(now: str) -> list[dict]:
    rules = []
    for suffix, planet, lord, colour, gem_metal, animal, body, objects, notes in CORRESPONDENCE_DATA:
        doc = _base_doc(f"lalkitab-ch27-corr-{suffix}", now)
        summary = (
            f"{planet} correspondences: Lord {lord}, colour {colour}, "
            f"body parts {'/'.join(body)}, objects {'/'.join(objects) if objects else 'unverified'}."
        )
        detail_parts = [
            f"Lord: {lord}.",
            f"Colour: {colour}.",
            f"Gem/Metal: {', '.join(gem_metal)}.",
            f"Animal: {', '.join(animal)}.",
            f"Body parts: {', '.join(body)}.",
            f"Objects: {', '.join(objects) if objects else '[data quality issue — see notes]'}.",
        ]
        if notes:
            detail_parts.append(f"Note: {notes}")
        doc.update({
            "condition": {
                "type":     "general_principle",
                "sub_type": "correspondence_table",
                "planet":   planet,
                "description": f"Lal Kitab Ch 27 planetary correspondence entry for {planet}.",
                "yoga_check": {"type": "none", "checkable": False},
            },
            "interpretation": {
                "summary":  summary,
                "detailed": " ".join(detail_parts),
                "correspondence": {
                    "lord":      lord,
                    "colour":    colour,
                    "gem_metal": gem_metal,
                    "animal":    animal,
                    "body_parts": body,
                    "objects":   objects,
                },
                "life_domains": ["health", "remedies", "planetary_nature"],
                "is_benefic":   None,
            },
            "tags": ["correspondence", "planetary_significator", planet.lower().replace(" ", "_"),
                     "body_parts", "objects"],
        })
        if notes:
            doc["metadata"]["data_quality_note"] = notes
            doc["metadata"]["needs_review"] = True
        rules.append(doc)
    return rules


# ── ❷ AFFLICTION / REMEDY RULES (R: Sun + Moon + Mars + Mercury + Jupiter + Venus + Saturn + Rahu + Ketu) ──

AFFLICTION_DATA = [
    (
        "sun", "Sun",
        ["Heart disease", "Eye pain", "Abdominal problem", "Loss of money", "False allegations"],
        [
            {"text": "Worship Sun; chant Harivansh Purana.", "category": "mantra"},
            {"text": "Donate copper or wheat.", "category": "offering"},
            {"text": "Eat jaggery/sweets and drink water before starting any work.", "category": "ritual"},
            {"text": "Resolution with two equal copper pieces — immerse one in water, keep one always.", "category": "gemstone_jewelry"},
        ],
    ),
    (
        "moon", "Moon",
        ["Mental tension", "Worry", "Lung disease", "Chickenpox", "Financial trouble"],
        [
            {"text": "Worship family God/Goddess.", "category": "mantra"},
            {"text": "Donate rice, milk, and silver.", "category": "offering"},
            {"text": "Take blessings by touching elders' feet.", "category": "ritual"},
            {"text": "Adorn one pearl/silver piece after immersing another in water.", "category": "gemstone_jewelry"},
        ],
    ),
    (
        "mars", "Mars",
        ["Liver disease", "Fluttering of lips"],
        [
            {"text": "Chant Hanuman Chalisa; fast on Tuesday.", "category": "mantra"},
            {"text": "Donate masoor and moong pulse.", "category": "offering"},
            {"text": "Apply white kohl in eyes.", "category": "ritual"},
            {"text": "Adorn red stone or coral based on Sun/Moon remedies.", "category": "gemstone_jewelry"},
        ],
    ),
    (
        "mercury", "Mercury",
        ["Neurological disease", "Dental problem"],
        [
            {"text": "Worship Durgaji; chant Durga Saptshati.", "category": "mantra"},
            {"text": "Donate whole moong.", "category": "offering"},
            {"text": "Keep teeth clean; pierce nose.", "category": "ritual"},
            {"text": "Adorn diamond or shells.", "category": "gemstone_jewelry"},
        ],
    ),
    (
        "jupiter", "Jupiter",
        ["Loss of son", "Throat trouble"],
        [
            {"text": "Chant Harivansh Purana; worship Brahmaji.", "category": "mantra"},
            {"text": "Donate gram pulse.", "category": "offering"},
            {"text": "Apply saffron tilak on forehead; keep nose clean.", "category": "ritual"},
            {"text": "Keep gold or saffron.", "category": "gemstone_jewelry"},
        ],
    ),
    (
        "venus", "Venus",
        ["Unexpected hurdles", "Hurdles in auspicious deeds"],
        [
            {"text": "Worship Lakshmi.", "category": "mantra"},
            {"text": "Donate ghee, curd, camphor, and pearl.", "category": "offering"},
            {"text": "Wear clean clothes.", "category": "ritual"},
            {"text": "Adorn white pearl.", "category": "gemstone_jewelry"},
        ],
    ),
    (
        "saturn", "Saturn",
        ["Fire", "Accidents", "Incompetent progeny", "Eye disease"],
        [
            {"text": "Worship Bhairav.", "category": "mantra"},
            {"text": "Donate iron or black urad.", "category": "offering"},
            {"text": "Offer bread to crows for 43 consecutive days.", "category": "ritual"},
            {"text": "Wear iron ring; use black salt or kohl.", "category": "gemstone_jewelry"},
        ],
    ),
    (
        "rahu", "Rahu",
        ["Head injury", "Mental disease", "Leprosy", "State penalties"],
        [
            {"text": "Worship Saraswatiji.", "category": "mantra"},
            {"text": "Donate mustard or blue sapphire.", "category": "offering"},
            {"text": "Keep shikha (choti); maintain joint family and good in-law relations.", "category": "ritual"},
            {"text": "Wear blue sapphire.", "category": "gemstone_jewelry"},
        ],
    ),
    (
        "ketu", "Ketu",
        ["Knee pain", "Urinary infection", "Son trouble", "Ill treatment", "Attack on faith"],
        [
            {"text": "Worship Ganeshji.", "category": "mantra"},
            {"text": "Donate she-calf, cow, and sesame.", "category": "offering"},
            {"text": "Keep pet dog; pierce ear.", "category": "ritual"},
            {"text": "Wear two-coloured stone.", "category": "gemstone_jewelry"},
        ],
    ),
]


def build_affliction_rules(now: str) -> list[dict]:
    rules = []
    for suffix, planet, symptoms, remedies in AFFLICTION_DATA:
        doc = _base_doc(f"lalkitab-ch27-rem-{suffix}", now)
        symptom_str = "; ".join(symptoms)
        remedy_str  = " | ".join(r["text"] for r in remedies)
        doc.update({
            "condition": {
                "type":    "dosha",
                "sub_type": "affliction",
                "planet":   planet,
                "description": f"{planet} affliction causing disease/difficulty (Lal Kitab Ch 27).",
                "yoga_check": {"type": "planet_afflicted", "checkable": True, "planet": planet},
            },
            "interpretation": {
                "summary":  f"{planet} affliction: {symptom_str}. Remedy: {remedy_str[:120]}...",
                "detailed": (
                    f"Symptoms of {planet} affliction: {symptom_str}. "
                    f"Remedies: {remedy_str}"
                ),
                "remedies": remedies,
                "life_domains": ["health", "remedies"],
                "is_benefic":   False,
            },
            "tags": ["affliction", "remedy", planet.lower(), "disease", "donation", "worship"],
        })
        rules.append(doc)
    return rules


# ── ❸ CONDITIONAL PROHIBITED DONATION RULES (P1-P10) ──────────────────────────

PROHIBITION_DATA = [
    (
        "01", "Exalted/Debilitated general rule",
        "general_principle", None,
        "Never donate objects of an exalted planet; never accept objects of a debilitated planet.",
        "Exaltation/debilitation of a planet changes the energy of its associated objects. "
        "Donating exalted objects dissipates one's own strength; accepting debilitated objects "
        "invites the negative energy of that planet.",
        {"type": "manual", "checkable": False},
        None, None,
    ),
    (
        "02", "Temple visit prohibition (H2 vacant + evil in H8)",
        "planetary_combination", None,
        "If House 2 is vacant and evil planets occupy House 8, visiting a temple is strictly prohibited.",
        "House 2 (family/wealth) vacant combined with evil planets in House 8 (death/loss) creates "
        "a negative axis that makes temple visits inauspicious — potentially harmful to the native.",
        {"type": "planetary_combination", "checkable": True},
        {"h2_vacant": True, "h8_content": "evil_planets"}, "Death-like outcomes from temple visit.",
    ),
    (
        "03", "Moon in 6th — milk donation and water construction",
        "planetary_combination", None,
        "Moon in 6th house: do not donate milk; do not construct a well, pond, or water tap.",
        "Moon in 6th weakens the water/nourishment significations. Donating milk or creating "
        "water bodies amplifies this weakness — result: death in the family.",
        {"type": "planet_in_house", "checkable": True},
        {"planet": "Moon", "house": 6}, "Death in family.",
    ),
    (
        "04", "Saturn in 8th — dharmashala construction",
        "planetary_combination", None,
        "Saturn in 8th house: do not construct a welfare home (dharmashala).",
        "Saturn in the 8th house of obstruction/death makes charitable construction inauspicious "
        "for the native — it activates the obstructive qualities of Saturn against the donor.",
        {"type": "planet_in_house", "checkable": True},
        {"planet": "Saturn", "house": 8}, "Activates Saturn's obstructive 8th-house energy against the native.",
    ),
    (
        "05", "Saturn in Asc + Jupiter in 5th — copper donation to beggars",
        "planetary_combination", None,
        "Saturn in Ascendant and Jupiter in 5th: do not give copper to beggars.",
        "Jupiter in 5th governs children/progeny. Saturn in the Ascendant restricts personal "
        "vitality. Donating copper (Sun's metal) to beggars under this combination results in "
        "suffering of one's own children.",
        {"type": "planetary_combination", "checkable": True},
        {"saturn": "ascendant", "jupiter": "house_5"}, "Child suffering.",
    ),
    (
        "06", "Jupiter in 10th + Moon in 4th — temple construction",
        "planetary_combination", None,
        "Jupiter in 10th and Moon in 4th: do not construct a temple.",
        "This combination activates a tension between public karma (Jupiter 10th) and domestic "
        "peace (Moon 4th). Temple construction under this combination inverts auspiciousness "
        "— outcome is jail/confinement for the native.",
        {"type": "planetary_combination", "checkable": True},
        {"jupiter": "house_10", "moon": "house_4"}, "Jail risk.",
    ),
    (
        "07", "Venus in 9th — child adoption",
        "planetary_combination", None,
        "Venus in 9th house: do not adopt a child.",
        "Venus in 9th affects the dharma and fortune axis. Adopting a child under this "
        "placement creates an imbalance in progeny karma that works against the native's "
        "long-term fortune.",
        {"type": "planet_in_house", "checkable": True},
        {"planet": "Venus", "house": 9}, "Adverse effect on fortune and progeny karma.",
    ),
    (
        "08", "Moon in 12th — feast to saints / school construction",
        "planetary_combination", None,
        "Moon in 12th house: do not offer feast to saints; do not build schools.",
        "Moon in 12th (loss/isolation) means nourishment given out (feast to saints) or "
        "knowledge infrastructure built (schools) is absorbed by the 12th house negativity "
        "— returning as painful death for the native.",
        {"type": "planet_in_house", "checkable": True},
        {"planet": "Moon", "house": 12}, "Painful death.",
    ),
    (
        "09", "Jupiter in 7th — donating clothes",
        "planetary_combination", None,
        "Jupiter in 7th house: do not donate clothes.",
        "Jupiter governs wealth and abundance. In the 7th it concerns partnerships. Donating "
        "clothes (a Jupiter-governed article) from this position returns as deprivation — "
        "the native and family pine for clothes.",
        {"type": "planet_in_house", "checkable": True},
        {"planet": "Jupiter", "house": 7}, "Native and family pine for clothes.",
    ),
    (
        "10", "Sun in 7th or 8th — timing of donations",
        "planetary_combination", None,
        "Sun in 7th or 8th house: do not donate during morning or evening.",
        "Sun in 7th/8th creates sensitivity around transition periods (sunrise/sunset). "
        "Donations made at these times activate the negative potential of Sun's placement "
        "in these inauspicious positions.",
        {"type": "planet_in_house", "checkable": True},
        {"planet": "Sun", "houses": [7, 8]}, "Activates inauspicious Sun placement.",
    ),
]


def build_prohibition_rules(now: str) -> list[dict]:
    rules = []
    for suffix, title, ctype, sub_type, summary, detailed, yoga_check, condition_extra, outcome in PROHIBITION_DATA:
        doc = _base_doc(f"lalkitab-ch27-proh-{suffix}", now)
        cond: dict = {
            "type":        ctype,
            "description": title,
            "yoga_check":  yoga_check,
        }
        if sub_type:
            cond["sub_type"] = sub_type
        if condition_extra:
            cond.update(condition_extra)
        interp: dict = {
            "summary":     summary,
            "detailed":    detailed,
            "life_domains": ["remedies", "dharma", "health"],
            "is_benefic":   False,
        }
        if outcome:
            interp["outcome_if_violated"] = outcome
        doc.update({
            "condition":     cond,
            "interpretation": interp,
            "tags": ["prohibition", "donation_rule", "conditional", f"proh-{suffix}"],
        })
        rules.append(doc)
    return rules


# ── ❹ PLANET TRANSFER PLACEMENT PROTOCOL (H1-H12) ─────────────────────────────

TRANSFER_DATA = [
    (1,  "Ascendant", "Adorn the object around the neck.",
     "House 1 (Ascendant/self) — the planet's object must remain on the native's body "
     "(adorned around the neck) to channel its energy into the self directly."),
    (2,  "House 2",   "Place the object at a temple or religious place.",
     "House 2 (family/wealth/speech) — the object is offered to a place of worship, "
     "activating the religious/familial dimension of the planet."),
    (3,  "House 3",   "Wear the object as a gem on the hand.",
     "House 3 (siblings/effort/hands) — the object is worn as a gem on the hand, "
     "channelling the planet's energy through the native's effort and action."),
    (4,  "House 4",   "Immerse the object in running water.",
     "House 4 (home/mother/comfort) — immersion in running water activates the "
     "cleansing/domestic dimension; water carries the planet's energy into the household."),
    (5,  "House 5",   "Transfer the object to a school or college.",
     "House 5 (children/intelligence/education) — the object is given to an educational "
     "institution, activating progeny and learning outcomes."),
    (6,  "House 6",   "Drop the object in a well.",
     "House 6 (enemies/disease/debt) — dropping in a well removes the negative energy "
     "associated with the planet's difficult placement in the 6th."),
    (7,  "House 7",   "Bury the object under the ground.",
     "House 7 (spouse/partnership/open enemies) — burying grounds and neutralises "
     "the conflicting energy of the planet in the partnership house."),
    (8,  "House 8",   "Bury the object at the pyre ground.",
     "House 8 (death/transformation/hidden matters) — the pyre ground is the appropriate "
     "locus for objects associated with this house; it transforms and neutralises the energy."),
    (9,  "House 9",   "Donate the object at a temple or wear it.",
     "House 9 (luck/dharma/father/long journeys) — the object is either donated at a "
     "temple (offering to the divine) or worn (keeping dharma aligned with the self)."),
    (10, "House 10",  "Eatables: give to father. Wearables: wear them. Other objects: bury near public property shadow.",
     "House 10 (career/karma/authority/father) — three sub-rules based on object type: "
     "food items strengthen the father connection; wearables are kept on the self; "
     "other items are buried near a public property shadow to anchor career karma."),
    (11, "House 11",  "No action required.",
     "House 11 (gains/elder siblings/desires) — when a planet is in the 11th, no "
     "transfer action is needed; the planet's gains are self-actualising in this house."),
    (12, "House 12",  "Install the object on the roof of the house.",
     "House 12 (loss/liberation/foreign lands/sleep) — installing on the roof "
     "elevates the energy out of the house and into the expansive/liberating dimension "
     "associated with the 12th house."),
]


def build_transfer_rules(now: str) -> list[dict]:
    rules = []
    for house, house_label, summary, detailed in TRANSFER_DATA:
        doc = _base_doc(f"lalkitab-ch27-transfer-h{house:02d}", now)
        doc.update({
            "condition": {
                "type":        "general_principle",
                "sub_type":    "transfer_protocol",
                "house":       house,
                "house_label": house_label,
                "description": f"Planet Transfer Placement for {house_label} — Lal Kitab Ch 27.",
                "yoga_check":  {"type": "planet_in_house", "checkable": True},
            },
            "interpretation": {
                "summary":     summary,
                "detailed":    detailed,
                "life_domains": ["remedies"],
                "is_benefic":   None,
            },
            "tags": ["transfer_protocol", "planet_placement", f"house_{house}", "remedy"],
        })
        rules.append(doc)
    return rules


# ── ❺ MENTAL WAVE ENGINE — 42 SECTIONS (W1-W49) ───────────────────────────────

# Each entry:
# (unit_id, section_num, house, planet_label, wave_name, effect_text, age_note)
MENTAL_WAVE_DATA = [
    ("w01", 1,  1,  "Venus / Saturn",     "Love and Romance",
     "Physical/sexual love driven by Venus; verbal expression of love driven by Saturn.",
     "Active 16-36 years."),
    ("w02", 2,  2,  "Jupiter",            "Desire to Marry",
     "Intensifying desire to formalise union and build family.",
     "Intensifies 37-72 years."),
    ("w03", 3,  3,  "Venus",              "Offspring Affection",
     "Deep longing for a son; paternal/parental affection wave.",
     None),
    ("w04", 3,  3,  "Mars",               "Childhood Affection",
     "Childhood bonding and affection for siblings.",
     "Active 1-15 years."),
    ("w05", 4,  4,  "Moon",               "Friendship",
     "Pure platonic friendship; feelings devoid of lust or ulterior motive.",
     None),
    ("w06", 4,  4,  "Mars Malefic",       "Destructor",
     "Destructive tendency towards love relationships and friendships.",
     None),
    ("w07", 5,  5,  "Jupiter",            "Love for Country",
     "Love for nation and family members; patriotic and familial devotion.",
     None),
    ("w08", 6,  6,  "Ketu",               "Sacrifice and Passion",
     "Self-sacrifice for a beloved person; capacity for selfless devotion.",
     None),
    ("w09", 6,  6,  "Venus",              "Interest in Progeny",
     "Heightened attention and investment towards the male child.",
     None),
    ("w10", 7,  7,  "Venus",              "Ambition",
     "Burning desire to rise in social status and achieve higher standing.",
     None),
    ("w11", 7,  7,  "Mercury",            "Proof Desire",
     "Strong desire to prove oneself. Particularly strong in flat-headed natives.",
     None),
    ("w12", 8,  8,  "Mars Benefic",       "Resolution",
     "Completes tasks regardless of success or failure; unstoppable follow-through.",
     None),
    ("w13", 8,  8,  "Sun",                "Difficulty Courage",
     "Courage to face and overcome obstacles and adversity.",
     None),
    ("w14", 9,  9,  "Saturn",             "Revengefulness",
     "If unable to take revenge personally, the native teaches their child to take revenge before death.",
     None),
    ("w15", 10, 3,  "Mercury",            "Taste Strength",
     "Strong digestive capacity and hearty appetite; epicurean sensibility.",
     None),
    ("w16", 11, 11, "Saturn",             "Wealth Amassing",
     "Persistent engagement in accumulating wealth; may shade into compulsive hoarding or theft.",
     None),
    ("w17", 12, 12, "Rahu",               "Secrecy",
     "Tendency to swindle and maintain extreme secrecy about activities and intentions.",
     None),
    ("w18", 13, 10, "Saturn",             "Ingenuity",
     "Accomplishes tasks by accurately guessing future timing and circumstances.",
     None),
    ("w19", 14, 8,  "Mars Malefic",       "Egotist",
     "Considers everyone else trivial or inconsequential; inflated sense of own importance.",
     None),
    ("w20", 15, 5,  "Jupiter",            "Self-Pride",
     "Never dishonours others to preserve personal honour; dignified self-respect.",
     None),
    ("w21", 16, 6,  "Ketu",               "Patience",
     "Dedicated and persistent regardless of profit or loss; equanimous under pressure.",
     None),
    ("w22", 17, 3,  "Mars",               "Judicious",
     "Cannot tolerate cruelty; sincerely wishes well for all people.",
     None),
    ("w23", 18, 6,  "Mercury",            "Optimism",
     "Maintains hope of a good future even in adverse circumstances.",
     None),
    ("w24", 18, 6,  "Ketu",               "Future Faith",
     "Strong, unshakeable belief in a bright future ahead.",
     None),
    ("w25", 19, 9,  "Jupiter",            "Religious Power",
     "God-fearing with supreme self-confidence; strong spiritual conviction.",
     None),
    ("w26", 20, 5,  "Sun",                "Generosity",
     "Respects others and fulfils duty; quietly generous and honourable.",
     None),
    ("w27", 21, 4,  "Moon",               "Sympathy",
     "Deep empathy for others. Particularly high in wide/high-forehead natives.",
     None),
    ("w28", 22, 5,  "Jupiter",            "Intelligence",
     "Acts according to own mind rather than following others. Strong in wide/raised-forehead natives.",
     None),
    ("w29", 23, 6,  "Ketu",               "Beauty Appreciation",
     "Appreciates beauty intensely; strongly desires a beautiful spouse.",
     None),
    ("w30", 24, 7,  "Mercury",            "Hopefulness",
     "Wishes to remain ahead in prosperity and opulence; forward-looking optimism.",
     None),
    ("w31", 25, 8,  "Evil Planet",        "Imitator",
     "Wonderful capacity to imitate others; belligerent when crossed.",
     None),
    ("w32", 26, 9,  "Jupiter",            "Humour",
     "Affable and jovial; spreads warmth through humour.",
     None),
    ("w33", 26, 9,  "Mercury",            "Excess Humour",
     "Humour that tips into foolishness; wit without wisdom.",
     None),
    ("w34", 27, 3,  "Mars",               "Mental Strength",
     "Knows the underlying truth behind every situation and person.",
     None),
    ("w35", 28, 4,  "Moon",               "Memory",
     "Exceptional ability to remember very old and distant details.",
     None),
    ("w36", 29, 5,  "Sun",                "Survival Strength",
     "Capacity to take on and complete extremely difficult tasks.",
     None),
    ("w37", 30, 6,  "Ketu",               "Penetration",
     "Recognises the true nature and character of every person encountered.",
     None),
    ("w38", 31, 7,  "Venus",              "Object Recognition",
     "Discerning perception of colour, face, and character of people and objects.",
     None),
    ("w39", 32, 8,  "Saturn",             "Cleanliness",
     "Highly organised external life; may mask inner cunning.",
     None),
    ("w40", 33, 9,  "Mercury",            "Judgement Strength",
     "Balanced judgement between heart and mind; wise discernment.",
     None),
    ("w41", 34, 10, "Mars Malefic",       "Memory Power",
     "Exceptional memory; becomes a consummate cheat if Saturn is also malefic in House 10.",
     None),
    ("w42", 35, 11, "Jupiter",            "Old Memory",
     "Focus on historical and political events; long-term pattern recognition.",
     None),
    ("w43", 36, 12, "Rahu",               "Guessing Situation",
     "Ability to deduce the present situation accurately by analysing the past.",
     None),
    ("w44", 37, 1,  "Saturn",             "Musical Note",
     "Natural understanding of musical notes and rhythmic patterns.",
     None),
    ("w45", 38, 2,  "Jupiter",            "Language Knowledge",
     "Ability to learn and discover languages with relative ease.",
     None),
    ("w46", 39, 3,  "Mars",               "Search Tendency",
     "Driven to discover the underlying reason and cause behind everything.",
     None),
    ("w47", 40, 4,  "Moon",               "Comparison Centre",
     "Highly skilled at assessing genuineness and authenticity of people and objects.",
     None),
    ("w48", 41, 5,  "Sun",                "Virtue",
     "Gentle and beneficent by nature; innately ethical.",
     None),
    ("w49", 42, 6,  "Mercury",            "Beneficence",
     "Pleases everyone; behaves tit-for-tat with fairness and reciprocity.",
     None),
]


def build_mental_wave_rules(now: str) -> list[dict]:
    rules = []
    for unit_id, section, house, planet, wave_name, effect, age_note in MENTAL_WAVE_DATA:
        doc = _base_doc(f"lalkitab-ch27-wave-{unit_id}", now)
        summary = f"Section {section}, House {house}, {planet}: {wave_name}. {effect[:100]}"
        detailed = (
            f"Mental wave '{wave_name}' (Section {section}): influenced by {planet} in "
            f"House {house}. Effect: {effect}"
        )
        if age_note:
            detailed += f" Age window: {age_note}"
        doc.update({
            "condition": {
                "type":        "general_principle",
                "sub_type":    "mental_wave_engine",
                "section":     section,
                "house":       house,
                "planet":      planet,
                "wave_name":   wave_name,
                "description": f"42-section mental wave engine — Section {section}: {wave_name}.",
                "yoga_check":  {"type": "planet_in_house", "checkable": True},
            },
            "interpretation": {
                "summary":     summary,
                "detailed":    detailed,
                "life_domains": ["psychology", "character", "mind"],
                "is_benefic":   None,
            },
            "tags": [
                "mental_wave", "42_sections", f"section_{section}",
                f"house_{house}", planet.lower().replace(" ", "_").replace("/", "_"),
                wave_name.lower().replace(" ", "_"),
            ],
        })
        if age_note:
            doc["condition"]["age_window"] = age_note
        rules.append(doc)
    return rules


# ── ❻ INVISIBLE PLANETS / TOTAKA TRIALS (IP1-IP9) ─────────────────────────────
# Hard-coded directly from PDF JSON extract (page 4-5).
# This section was entirely absent from V2 decode.

INVISIBLE_PLANET_DATA = [
    (
        "sun", "Sun",
        [6, 7, 10],
        "Immerse jaggery in running water.",
        "When Sun occupies inauspicious houses (6th, 7th, or 10th), the planet becomes "
        "invisible/weakened. Remedial trial: immerse jaggery (Sun's sweet) in running water "
        "to dissolve the obstruction and restore Sun's positive energy flow.",
    ),
    (
        "moon", "Moon",
        [6, 8, 10, 11, 12],
        "Keep a pot of water at the headpost of the bed; irrigate a keekar tree every morning.",
        "Moon invisible in houses 6, 8, 10, 11, 12. Dual trial: water at headpost maintains "
        "lunar nourishment during sleep; irrigating the keekar tree (associated with Moon) "
        "establishes a daily ritual of lunar reconnection.",
    ),
    (
        "mars", "Mars",
        [4, 8],
        "Immerse rewari (sesame-jaggery sweet) in running water.",
        "Mars invisible in 4th (home/mother) or 8th (death/transformation). Rewari "
        "combines sesame (Ketu/Mars-associated) with jaggery (Sun) — immersion in "
        "running water clears the obstacle created by Mars's difficult placement.",
    ),
    (
        "mercury", "Mercury",
        [3, 8, 9, 10, 11, 12],
        "Take a copper coin with a hole; immerse in running water.",
        "Mercury invisible in houses 3, 8, 9, 10, 11, 12. Copper (Sun's metal, which "
        "Mercury orbits closely) with a hole (representing Mercury's quicksilver nature) — "
        "immersed in running water to dissolve the communication/intellect blockage.",
    ),
    (
        "jupiter", "Jupiter",
        [2, 4, 5, 7],
        "Apply saffron on the navel; or eat/drink saffron.",
        "Jupiter invisible in 2nd, 4th, 5th, 7th. Saffron is Jupiter's primary substance. "
        "Application on the navel (body's centre/solar plexus) or internal consumption "
        "reinstates Jupiter's wisdom and expansion energy directly into the body.",
    ),
    (
        "venus", "Venus",
        [1, 6, 9],
        "Donate a chari (cow-feed utensil) at a cowshed.",
        "Venus invisible in 1st, 6th, 9th. Venus governs cows and fertility. Donating "
        "a chari (the vessel that feeds cows) at a cowshed directly activates Venus's "
        "nourishment-giving quality and restores its positive influence.",
    ),
    (
        "saturn", "Saturn",
        [1, 4, 5, 6],
        "Donate oil after seeing your own image reflected in it.",
        "Saturn invisible in 1st, 4th, 5th, 6th. Oil (Saturn's primary substance) — the "
        "act of seeing one's own reflection in the oil before donating it is a Saturn-specific "
        "ritual acknowledgement of karma and self-awareness before releasing the offering.",
    ),
    (
        "rahu", "Rahu",
        [1, 2, 5, 7, 8, 10, 11, 12],
        "Donate radish; immerse coal in running water.",
        "Rahu invisible across 8 houses (1, 2, 5, 7, 8, 10, 11, 12). Dual trial: "
        "radish (Rahu's vegetable) is donated; coal (dark material associated with Rahu/Saturn) "
        "is immersed in running water to dissolve the shadow planet's obstructive energy.",
    ),
    (
        "ketu", "Ketu",
        [3, 4, 5, 6, 8],
        "Offer bread to dogs.",
        "Ketu invisible in 3rd, 4th, 5th, 6th, 8th. Dogs are Ketu's primary animal. "
        "Offering bread (nourishment) to dogs directly appeases Ketu's karmic energy "
        "and neutralises its inauspicious placement in these houses.",
    ),
]


def build_invisible_planet_rules(now: str) -> list[dict]:
    rules = []
    for suffix, planet, houses, trial, detailed in INVISIBLE_PLANET_DATA:
        doc = _base_doc(f"lalkitab-ch27-invis-{suffix}", now)
        houses_str = "/".join(str(h) for h in houses)
        doc.update({
            "condition": {
                "type":        "planetary_combination",
                "sub_type":    "invisible_planet",
                "planet":      planet,
                "inauspicious_houses": houses,
                "description": (
                    f"{planet} invisible/inauspicious in houses {houses_str} — "
                    f"remedial trial (totaka) required."
                ),
                "yoga_check":  {"type": "planet_in_house", "checkable": True, "planet": planet},
            },
            "interpretation": {
                "summary":  (
                    f"{planet} invisible in houses {houses_str}. "
                    f"Totaka remedy: {trial}"
                ),
                "detailed": detailed,
                "remedies": [{"text": trial, "category": "ritual"}],
                "life_domains": ["remedies", "planetary_pacification"],
                "is_benefic":   False,
            },
            "tags": [
                "invisible_planet", "totaka", "remedial_trial",
                planet.lower(), f"houses_{houses_str.replace('/', '_')}",
            ],
        })
        doc["metadata"]["source_note"] = (
            "lalkitab-ch27-pdf-json-extract — invisible planets section absent from V2 decode; "
            "hard-coded directly from PDF JSON page 4-5."
        )
        rules.append(doc)
    return rules


# ── BUILD ALL ──────────────────────────────────────────────────────────────────

def build_all_rules() -> list[dict]:
    now = datetime.now(timezone.utc).isoformat()
    rules: list[dict] = []
    rules.extend(build_correspondence_rules(now))
    rules.extend(build_affliction_rules(now))
    rules.extend(build_prohibition_rules(now))
    rules.extend(build_transfer_rules(now))
    rules.extend(build_mental_wave_rules(now))
    rules.extend(build_invisible_planet_rules(now))
    return rules


# ── CLI ────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest Lal Kitab Ch 27 rules.")
    parser.add_argument("--dry-run",  action="store_true",
                        help="Build rules and print summary — no DB write.")
    parser.add_argument("--save",     metavar="PATH",
                        help="Save rules JSON to this file (use with --dry-run).")
    parser.add_argument("--upload",   metavar="PATH",
                        help="Upload rules from this JSON file to MongoDB.")
    parser.add_argument("--mongo-url", default="",
                        help="MongoDB connection URL.")
    parser.add_argument("--db-name",  default="horoscope_db",
                        help="MongoDB database name.")
    args = parser.parse_args()

    # ── DRY RUN ──
    if args.dry_run:
        rules = build_all_rules()
        groups = {}
        for r in rules:
            prefix = "-".join(r["rule_id"].split("-")[:4])
            groups[prefix] = groups.get(prefix, 0) + 1
        print(f"\nDRY RUN — {len(rules)} rules built\n")
        for g, count in sorted(groups.items()):
            print(f"  {g:<40} {count} rules")
        print()

        # Show Mars C3 data quality note
        for r in rules:
            if r["rule_id"] == "lalkitab-ch27-corr-mars-benefic":
                print(f"[DATA QUALITY] {r['rule_id']}: objects = {r['interpretation']['correspondence']['objects']}")
                print(f"  Note: {r['metadata'].get('data_quality_note', '')}\n")
                break

        if args.save:
            path = Path(args.save)
            path.write_text(json.dumps(rules, indent=2, ensure_ascii=False))
            print(f"Saved → {path}  ({path.stat().st_size:,} bytes)\n")
        return

    # ── UPLOAD ──
    if args.upload:
        import os
        from pymongo import MongoClient

        mongo_url = args.mongo_url or os.environ.get("MONGO_URL", "").strip()
        if not mongo_url:
            mongo_url = input("Paste MongoDB Atlas URL: ").strip()

        path = Path(args.upload)
        if not path.exists():
            sys.exit(f"File not found: {path}")

        rules = json.loads(path.read_text())
        print(f"Loaded {len(rules)} rules from {path}")

        client = MongoClient(mongo_url)
        coll   = client[args.db_name]["interpretation_rules"]

        # Safety check — avoid double-ingest
        existing = coll.count_documents({"source.batch_id": BATCH_ID})
        if existing > 0:
            confirm = input(
                f"\n⚠️  {existing} rules already exist for batch {BATCH_ID}. "
                "Delete and re-insert? [y/N] "
            ).strip().lower()
            if confirm != "y":
                print("Aborted.")
                return
            coll.delete_many({"source.batch_id": BATCH_ID})
            print(f"Deleted {existing} existing rules.")

        result = coll.insert_many(rules)
        print(f"\n✅ Inserted {len(result.inserted_ids)} rules into {args.db_name}.interpretation_rules")
        print(f"   Batch ID: {BATCH_ID}\n")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
