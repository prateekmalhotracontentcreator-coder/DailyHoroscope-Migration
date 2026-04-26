#!/usr/bin/env python3
"""
ingest_lalkitab_ch19_v1.py — Lal Kitab Chapter 19: Mangalik Evil and Trials

78 rules total across 5 groups:
   5  Base house rules         (Mars in H1 / H4 / H7 / H8 / H12)
  60  Ascendant-specific rules (12 ascendants x 5 Mars houses, with remedies)
   9  Special conjunction rules (Widowhood, Pap Kartari, Impotency x2,
                                 Financial Ruin x2, Family Abandonment,
                                 Jupiter-5th, Venus-7th)
   2  Social identification rules (Molia Mangal, Chunari Mangal)
   2  General principle rules  (Behavioral archetype, Conspiracy/Persistence)

Source: Lal Kitab Ch 19 original PDF + Notebook LM v2 decode (reviewed).
Extraction: hard_coded — zero API calls.
All 60 ascendant-specific remedies cross-referenced against source trial table.

Aspect house corrections applied (Option 2 — standard 4th/7th/8th from position):
  H1 : [4, 7, 8]     H4 : [7, 10, 11]   H7 : [1, 2, 10]
  H8 : [2, 3, 11]    H12: [3, 6, 7]
Note: textbook's universal statement ("Mars burns H4/H8 from any position")
explains why decode had H4+H8 in H12 aspects. Corrected to standard calculation.
Phase 2: verify against a confirmed Lal Kitab aspect reference.

Standard workflow:
  Step 1 — Dry run + save:
    python3 scripts/ingest_lalkitab_ch19_v1.py --dry-run --save scripts/lalkitab_ch19_rules.json

  Step 2 — Review lalkitab_ch19_rules.json; amend as needed.

  Step 3 — Upload (zero API calls):
    python3 scripts/ingest_lalkitab_ch19_v1.py \\
      --upload scripts/lalkitab_ch19_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 4 — Validate:
    python3 scripts/validate_rules.py \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id lalkitab-ch19-v1-20260426
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Constants ─────────────────────────────────────────────────────────────────

SCIENCE   = "jyotish"
BOOK      = "Lal Kitab"
BOOK_ID   = "lal-kitab"
CHAPTER   = 19
CHAP_NAME = "Mangalik Evil and Trials"
BATCH_ID  = "lalkitab-ch19-v1-20260426"

# ── Trial catalog: trial_no -> (text, category) ───────────────────────────────

TRIALS: dict[int, tuple[str, str]] = {
    1:  ("Chant Hanuman Chalisa",                                           "mantra"),
    2:  ("Offer prasad to Hanumanji and distribute it",                     "offering"),
    3:  ("Offer vermilion to Hanumanji",                                    "offering"),
    4:  ("Chant Gayatri mantra",                                            "mantra"),
    5:  ("Read Durga paadh",                                                "mantra"),
    6:  ("Read Sundar Kand of the Ramayan",                                 "mantra"),
    7:  ("Keep along red handkerchief",                                     "ritual"),
    8:  ("Wear silver ring which has no joint",                             "gemstone_jewelry"),
    9:  ("Wear ring of copper or gold studded with coral",                  "gemstone_jewelry"),
    10: ("Wear a wristlet made of silver and studded with a nail of copper","gemstone_jewelry"),
    11: ("Colour a silver bangle red and let your wife wear it",            "gemstone_jewelry"),
    12: ("Offer food to monkeys",                                           "offering"),
    13: ("Offer sweet bread of oven to dogs",                               "offering"),
    14: ("Distribute sweet food at the temple",                             "offering"),
    15: ("Drop sugar in flowing water",                                     "offering"),
    16: ("Float honey or vermilion in running water",                       "offering"),
    17: ("Dismantle kachchi wall after building it",                        "ritual"),
    18: ("Keep servant at home",                                            "ritual"),
}


def make_remedies(trial_nos: list[int]) -> list[dict]:
    return [
        {"text": TRIALS[n][0], "category": TRIALS[n][1], "trial_no": n}
        for n in trial_nos
    ]


# ── Corrected aspect houses (standard 4th / 7th / 8th from Mars position) ─────

ASPECT_HOUSES: dict[int, list[int]] = {
    1:  [4, 7, 8],
    4:  [7, 10, 11],
    7:  [1, 2, 10],
    8:  [2, 3, 11],
    12: [3, 6, 7],
}

# ── Base outcome texts (Section 3 of v2 decode) — used as `detailed` field ────

OUTCOME_DETAILED: dict[int, str] = {
    1: (
        "Mars in the 1st house aspects the 7th house (happiness/pleasure), causing "
        "excitement and rashness in domestic life. The native is excessively inclined "
        "toward material pleasure, incorporating sadism into their enjoyment. The "
        "native lacks decisive intellect due to rashness and repents wrong decisions. "
        "This placement effectively burns happiness, household peace, and intelligence."
    ),
    4: (
        "Mars in the 4th house reduces domestic joy, materialistic joy, and business "
        "prosperity due to extreme incitement, rashness, and anger. The native is "
        "rendered idle and frequently changes jobs or business ventures. Significant "
        "antagonism with the father is noted, with widely differing ideologies. "
        "Financial income deteriorates, leading to social disrespect and persistent "
        "unhappiness."
    ),
    7: (
        "Mars in the 7th house acts as a primary barrier to domestic joy. The native "
        "is characterized as extremely obstinate, rash, and furious. There is an "
        "inclination toward unnatural intercourse and sexual dissatisfaction. Because "
        "the 8th house is the family house for the 7th, opposition with the family is "
        "natural. Life remains devoid of family, business, and health."
    ),
    8: (
        "Mars in the 8th house leaves the family and kin devoid of money and "
        "prosperity. The native becomes idle and lazy, destroying paternal property "
        "instead of building assets. This results in the loss of social respect and "
        "abandonment by friends and brothers. Charm between husband and wife is "
        "rendered impossible."
    ),
    12: (
        "Mars in the 12th house causes the dissipation of non-monetary profits. The "
        "native faces perennial illness, grief, enemies, and repeated humiliation. "
        "Frustration and annoyance are projected onto the spouse, creating a hellish "
        "domestic life defined by constant mistrust and opposition."
    ),
}

# ── 60 ascendant-specific rules ───────────────────────────────────────────────
# Format: (ascendant, mars_house, [trial_nos], outcome_summary)
# outcome_summary from Section 4 of v2 decode (condensed per-rule text)

ASC_RULES: list[tuple[str, int, list[int], str]] = [
    # Aries
    ("Aries",       1,  [7, 9, 12, 13], "Excitement and rashness in domestic life; sadism in pleasure; burns happiness and intelligence."),
    ("Aries",       4,  [10, 12, 18],   "Reduced domestic/material joy; idle nature; job changes; antagonism with father."),
    ("Aries",       7,  [9, 18],        "Barrier to domestic joy; obstinate and furious; sexual dissatisfaction; family opposition."),
    ("Aries",       8,  [8, 10, 15],    "Family devoid of money; destruction of paternal property; loss of social respect."),
    ("Aries",      12,  [6],            "Perennial illness and enemies; revenge taken on spouse; hellish domestic life."),
    # Taurus
    ("Taurus",      1,  [9, 7, 11],     "Lack of decisive intellect; sadness in material life; loss of household peace."),
    ("Taurus",      4,  [2, 10, 16],    "Deterioration in income; business suffers from incitement; ideological differences with father."),
    ("Taurus",      7,  [6, 9],         "Native is furious and unsatisfied sexually; instability in health and family."),
    ("Taurus",      8,  [13, 18],       "Brothers and friends leave the idler; charm between husband and wife is impossible."),
    ("Taurus",     12,  [4, 5, 8],      "Spendthrift regarding non-monetary profits; constant mistrust between spouses."),
    # Gemini
    ("Gemini",      1,  [2, 9, 11],     "Sadism in pleasure; destruction of wisdom; lack of social respect."),
    ("Gemini",      4,  [10, 16],       "Frequent job changes; rash native becomes a point of disrespect; unhappiness."),
    ("Gemini",      7,  [2, 8, 17],     "Obstinate nature causes barrier in domestic joy; family opposition."),
    ("Gemini",      8,  [10],           "Destruction of paternal property; inability to sustain spirit; idle and lazy."),
    ("Gemini",     12,  [11],           "Repeated humiliation; revenge taken on spouse; influence of anger and rashness."),
    # Cancer
    ("Cancer",      1,  [1, 9, 11, 18], "Division and separation in domestic life; repentance after wrong decisions."),
    ("Cancer",      4,  [10, 12],       "Ideological gap with father; financial deterioration; disrespect in society."),
    ("Cancer",      7,  [11, 17],       "Barrier to joy; native is against the father; no business or family health."),
    ("Cancer",      8,  [9, 10],        "Family devoid of money; brother leaves considering him an idler; loss of charm."),
    ("Cancer",     12,  [9],            "Spends non-monetary profits; perennially seized by illness, grief, and enemies."),
    # Leo
    ("Leo",         1,  [7, 9],         "Excessive material inclination; rashness; burning of household intelligence."),
    ("Leo",         4,  [9, 11],        "Reduced domestic/business joy; idle native; deterioration in financial income."),
    ("Leo",         7,  [9, 11],        "Obstinate and furious; unsatisfied sex; opposition with the family."),
    ("Leo",         8,  [9, 10],        "Destruction of paternal property; social respect reduces; loss of marital charm."),
    ("Leo",        12,  [2, 4, 5, 11],  "Humiliation and disrespect; constant mistrust and opposition with spouse."),
    # Virgo
    ("Virgo",       1,  [1, 11],        "Bereft of happiness; lack of land and house; repetitive repentance for wrong decisions."),
    ("Virgo",       4,  [10, 16],       "Deterioration in income; ideologically at odds with father; idle nature."),
    ("Virgo",       7,  [11, 17],       "Great barrier in domestic joy; furious temperament; no stability in business or health."),
    ("Virgo",       8,  [10, 11],       "Kin devoid of money; friends and brothers leave; inability to build property."),
    ("Virgo",      12,  [2, 11, 18],    "Spendthrift nature; humiliated again and again; hellish domestic life under anger."),
    # Libra
    ("Libra",       1,  [9, 11],        "Cruel toward spouse; short of decisive intellect; sadism in pleasure."),
    ("Libra",       4,  [10, 16],       "Reduction in business joy; job changes; antagonism with father."),
    ("Libra",       7,  [1],            "Obstinate and furious; barrier in domestic joy; no family stability."),
    ("Libra",       8,  [10, 13],       "Family devoid of prosperity; social respect reduces; charm in marriage impossible."),
    ("Libra",      12,  [2, 4, 5],      "Humiliation and disrespect; seized by illness and grief; revenge taken on spouse."),
    # Scorpio
    ("Scorpio",     1,  [7, 8, 9, 11],  "Separation and division; rash decisions; burns household and intelligence."),
    ("Scorpio",     4,  [10, 16],       "Ideological conflict with father; deterrent to income; social disrespect."),
    ("Scorpio",     7,  [9, 11],        "Unsatisfied sexually; great barrier in domestic joy; opposition with family."),
    ("Scorpio",     8,  [10, 13],       "Destroys paternal property; brother leaves considering him an idler; no social respect."),
    ("Scorpio",    12,  [1, 9, 11],     "Spendthrift; perennial illness and grief; constant mistrust in marriage."),
    # Sagittarius
    ("Sagittarius", 1,  [1, 7],         "Lack of decisive intellect; cruelty; excitement and rashness in domestic life."),
    ("Sagittarius", 4,  [12],           "Reduces business/material joy; idle native; antagonism with father."),
    ("Sagittarius", 7,  [2, 17],        "Furious and obstinate; family opposition; no health or business stability."),
    ("Sagittarius", 8,  [4, 5, 8],      "Family devoid of money; inability to sustain spirit; destruction of paternal assets."),
    ("Sagittarius",12,  [1, 8],         "Constant mistrust; revenge taken on spouse; humiliation and disrespect."),
    # Capricorn
    ("Capricorn",   1,  [9],            "Sadism in pleasure; bereft of happiness; lack of house and land."),
    ("Capricorn",   4,  [10, 12],       "Deterioration in income; non-earning status leads to social disrespect; ideological conflicts."),
    ("Capricorn",   7,  [17],           "Barrier in domestic joy; unsatisfied in sex; against the father and family."),
    ("Capricorn",   8,  [9],            "Devoid of prosperity; paternal property destroyed; charm in marriage impossible."),
    ("Capricorn",  12,  [1, 9],         "Spends non-monetary profits; perennially ill; life made hell under anger."),
    # Aquarius
    ("Aquarius",    1,  [2, 7],         "Burns household peace; lack of decisive intellect; repentance."),
    ("Aquarius",    4,  [2, 10, 16],    "Rashness and anger; idle native; frequent job or business changes."),
    ("Aquarius",    7,  [1],            "Great barrier in domestic joy; furious and obstinate; unstable family life."),
    ("Aquarius",    8,  [10],           "Family devoid of money; brother leaves idler; loss of social respect."),
    ("Aquarius",   12,  [2, 11],        "Humiliation and disrespect; seized by grief and enemies; mistrust in marriage."),
    # Pisces
    ("Pisces",      1,  [7, 18],        "Bereft of happiness; lack of decisiveness; sadism in material pleasure."),
    ("Pisces",      4,  [12],           "Reduction in domestic joy/business; idle nature; financial deterioration."),
    ("Pisces",      7,  [9, 11, 17],    "Obstinate and unsatisfied sexually; opposition with family; no business stability."),
    ("Pisces",      8,  [9, 13],        "Destruction of paternal property; social respect reduces; charm impossible."),
    ("Pisces",     12,  [3, 9],         "Perennial illness; revenge on spouse; constant opposition in domestic life."),
]

# ── Special conjunction / Yog rules (Section 5 of v2 decode) ─────────────────

CONJUNCTION_RULES: list[dict] = [
    {
        "rule_name":      "Triple Mangali Widowhood",
        "condition_text": (
            "Native is Mangali simultaneously from all three reference points: "
            "Mars in a Mangali house (1/4/7/8/12) counted from the Ascendant, "
            "from the Moon sign, AND from the Sun sign."
        ),
        "outcome": (
            "The native will certainly be a widow or widower. Verified beyond doubt "
            "by the Lal Kitab text."
        ),
        "is_benefic":   False,
        "life_domains": ["marriage", "longevity"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "description": (
                "Requires evaluating Mangali condition from three reference points "
                "(Ascendant, Moon sign, Sun sign) simultaneously. Phase 2: "
                "implement as triple_mangali_check."
            ),
        },
        "tags": ["widowhood", "triple_mangali", "conjunction"],
    },
    {
        "rule_name":      "Pap Kartari Yog — Permanent Domestic Hell",
        "condition_text": (
            "The 7th house is hemmed between malefic planets: the 6th house OR the "
            "8th house contains any of Sun, Mars, Saturn, Rahu, or Ketu."
        ),
        "outcome": (
            "The native will never obtain domestic pleasure regardless of effort, "
            "resulting in a hellish existence throughout life."
        ),
        "is_benefic":   False,
        "life_domains": ["marriage", "domestic"],
        "yoga_check": {
            "type":        "multi_house_requirements",
            "checkable":   True,
            "description": (
                "Malefic planets (Sun, Mars, Saturn, Rahu, Ketu) in H6 or H8 "
                "flanking H7. Pure positional check — malefic classification "
                "uses natural malefic list."
            ),
            "operator": "or",
            "house_requirements": [
                {"houses": [6], "planet_type": "malefic", "constraint": "present"},
                {"houses": [8], "planet_type": "malefic", "constraint": "present"},
            ],
        },
        "tags": ["pap_kartari", "marriage", "conjunction"],
    },
    {
        "rule_name":      "Impotency — Venus and Ketu in Ascendant",
        "condition_text": "Venus and Ketu are both placed in the 1st house (Ascendant).",
        "outcome":        "Impotency is a verified systemic possibility.",
        "is_benefic":     False,
        "life_domains":   ["health", "marriage"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "description": (
                "Requires both Venus AND Ketu in H1. Phase 2: implement as "
                "specific_planets_in_house with planets=['Venus','Ketu'], houses=[1]."
            ),
        },
        "tags": ["impotency", "conjunction", "health"],
    },
    {
        "rule_name":      "Impotency — Sun-Venus-Saturn Combination",
        "condition_text": (
            "Sun is placed in the 4th house, Venus in the 5th house, AND "
            "Saturn in the 7th house — all three simultaneously."
        ),
        "outcome":        "Impotency is a verified systemic possibility.",
        "is_benefic":     False,
        "life_domains":   ["health", "marriage"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "description": (
                "Three specific planets in three specific houses. Phase 2: "
                "implement as specific_planets_in_house compound rule — "
                "Sun in [4] AND Venus in [5] AND Saturn in [7]."
            ),
        },
        "tags": ["impotency", "conjunction", "health"],
    },
    {
        "rule_name":      "Financial Ruin via Blind Lust — Configuration A",
        "condition_text": (
            "Sun is in the 6th house AND either Mars or Moon is in the 10th house, "
            "OR Jupiter is in the 11th house."
        ),
        "outcome": (
            "The native will blow off all savings and property in the pursuit "
            "of blind lust."
        ),
        "is_benefic":   False,
        "life_domains": ["wealth", "health"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "description": (
                "Multi-planet OR condition across H6, H10, H11 with specific "
                "planet assignments. Phase 2: composite condition engine required."
            ),
        },
        "tags": ["financial_ruin", "lust", "conjunction"],
    },
    {
        "rule_name":      "Financial Ruin via Blind Lust — Configuration B",
        "condition_text": (
            "Moon is in the Ascendant AND either (Jupiter AND Venus together in "
            "the 10th house) OR Jupiter alone in the 11th house."
        ),
        "outcome": (
            "The native will blow off all savings and property in the pursuit "
            "of blind lust."
        ),
        "is_benefic":   False,
        "life_domains": ["wealth", "health"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "description": (
                "Compound OR condition with multi-planet conjunction requirement "
                "in H10. Phase 2: composite condition engine required."
            ),
        },
        "tags": ["financial_ruin", "lust", "conjunction"],
    },
    {
        "rule_name":      "Family Abandonment — Saturn in 11th",
        "condition_text": "Saturn is placed in the 11th house.",
        "outcome": (
            "High probability that the native abandons wife and children "
            "at a young age."
        ),
        "is_benefic":   False,
        "life_domains": ["marriage", "family", "children"],
        "yoga_check": {
            "type":      "planet_in_house",
            "checkable": True,
            "planet":    "Saturn",
            "houses":    [11],
            "description": "Saturn in H11. Pure positional check.",
        },
        "tags": ["family_abandonment", "conjunction"],
    },
    {
        "rule_name":      "Jupiter in 5th Alone — Son Impossible",
        "condition_text": (
            "Jupiter is placed alone in the 5th house with no other planet "
            "aspecting it."
        ),
        "outcome":        "The joy of a son is not possible in this configuration.",
        "is_benefic":     False,
        "life_domains":   ["children", "progeny"],
        "yoga_check": {
            "type":      "complex",
            "checkable": False,
            "description": (
                "Requires confirming Jupiter is unaspected in H5 — aspect "
                "detection is outside current engine scope."
            ),
        },
        "tags": ["progeny", "conjunction"],
    },
    {
        "rule_name":      "Venus in 7th — Excess Pleasure and Illicit Relations",
        "condition_text": "Venus is placed in the 7th house.",
        "outcome": (
            "The native becomes excessively pleasure-seeking, leading to "
            "chronic dissatisfaction and illicit relations."
        ),
        "is_benefic":   False,
        "life_domains": ["marriage", "relationships"],
        "yoga_check": {
            "type":      "planet_in_house",
            "checkable": True,
            "planet":    "Venus",
            "houses":    [7],
            "description": "Venus in H7. Pure positional check.",
        },
        "tags": ["marriage", "conjunction", "relationships"],
    },
]

# ── General principle + Social identification rules ────────────────────────────

GENERAL_RULES: list[dict] = [
    {
        "rule_name":    "Molia Mangal — Male Social Identifier",
        "rule_type":    "social_identification",
        "condition_text": (
            "The native is male AND Mars is placed in one of the Mangali "
            "houses (1, 4, 7, 8, or 12)."
        ),
        "outcome": (
            "The male native is socially identified as 'Molia Mangal' — "
            "from 'Molia', referring to the turban worn by men. This is a "
            "social classification tag used in traditional Vedic matchmaking."
        ),
        "is_benefic":   None,
        "life_domains": ["marriage", "social"],
        "tags":         ["mangalik", "social_id", "molia"],
    },
    {
        "rule_name":    "Chunari Mangal — Female Social Identifier",
        "rule_type":    "social_identification",
        "condition_text": (
            "The native is female AND Mars is placed in one of the Mangali "
            "houses (1, 4, 7, 8, or 12)."
        ),
        "outcome": (
            "The female native is socially identified as 'Chunari Mangal' — "
            "from 'Chunari', referring to the attire or veil worn by women. "
            "This is a social classification tag used in traditional Vedic matchmaking."
        ),
        "is_benefic":   None,
        "life_domains": ["marriage", "social"],
        "tags":         ["mangalik", "social_id", "chunari"],
    },
    {
        "rule_name":    "Mars Behavioral Archetype",
        "rule_type":    "behavioral_archetype",
        "condition_text": (
            "Mars (Mangal) is present in any house of the horoscope as a "
            "general planetary influence."
        ),
        "outcome": (
            "Mars is characterized by strict discipline, extreme arrogance, and "
            "firmness. Excessive firmness leads to sorrow; extreme self-pride "
            "becomes unbearable. Mars rules anger — as anger peaks, happiness "
            "recedes. The influence of Mars destroys decisive intellect and "
            "common sense through rashness and excitement, causing a cycle of "
            "wrong decisions and subsequent repentance."
        ),
        "is_benefic":   None,
        "life_domains": ["general", "mind", "health"],
        "tags":         ["mangalik", "behavioral", "general_principle"],
    },
    {
        "rule_name":    "Mangal Dosha Persistence — Age Conspiracy Rule",
        "rule_type":    "persistence_logic",
        "condition_text": (
            "Traditional claim: Mangal Dosha expires or diminishes when the "
            "native reaches age 24, 28, or 30."
        ),
        "outcome": (
            "Lal Kitab categorically rejects age-based expiration of Mangal "
            "Dosha. Mars does not physically vanish from the sky, nor does its "
            "cosmic range or brilliance diminish with age. The claim is labelled "
            "a 'conspiracy' — a social survival mechanism by parents of daughters "
            "aged 27-28 who fear the limited pool of available grooms. The Dosha "
            "is persistent regardless of age. Strict adherence to the trial "
            "remedies is required throughout life."
        ),
        "is_benefic":   None,
        "life_domains": ["marriage", "general"],
        "tags":         ["mangalik", "persistence", "general_principle"],
    },
]


# ── Rule builders ─────────────────────────────────────────────────────────────

def _base_doc(rule_id: str, now: str) -> dict:
    """Shared skeleton fields."""
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


def build_base_house_rule(house: int, index: int, now: str) -> dict:
    """5 base Mangalik house rules — no ascendant filter."""
    rule_id = f"lalkitab-ch19-{index:03d}"
    detailed = OUTCOME_DETAILED[house]
    doc = _base_doc(rule_id, now)
    doc.update({
        "condition": {
            "type":            "dosha",
            "sub_type":        "mangalik",
            "dosha_type":      "mangalik",
            "planets_involved": ["Mars"],
            "houses_involved": [house],
            "ascendant":       None,
            "aspect_houses":   ASPECT_HOUSES[house],
            "sub_conditions":  [],
            "operator":        "and",
            "gender_context":  "neutral",
            "is_benefic":      False,
            "yoga_check": {
                "type":        "planet_in_house",
                "checkable":   True,
                "planet":      "Mars",
                "houses":      [house],
                "description": (
                    f"Mars in house {house} — core Mangali placement. "
                    f"Pure positional check from natal Lagna."
                ),
            },
        },
        "interpretation": {
            "summary":            detailed[:120],
            "detailed":           detailed,
            "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
            "remedies":           [],
            "life_domain":        "marriage",
            "life_domains":       ["marriage", "domestic", "relationships"],
            "tags":               ["mangalik", f"mars_h{house}", "base_rule"],
            "physical_markers":   [],
        },
        "metadata": {
            "planets_involved":     ["Mars"],
            "houses_involved":      [house],
            "signs_involved":       [],
            "condition_count":      1,
            "gender_context":       "neutral",
            "is_group_summary":     False,
            "has_physical_markers": False,
            "physical_categories":  [],
            "yoga_checkable":       True,
        },
        "confidence": {
            "source_confidence": "HIGH",
            "extraction_method": "hard_coded",
            "validated":         False,
        },
    })
    return doc


def build_ascendant_rule(
    ascendant: str, mars_house: int,
    trial_nos: list[int], outcome_summary: str,
    index: int, now: str,
) -> dict:
    """60 ascendant-specific rules with remedies."""
    rule_id  = f"lalkitab-ch19-{index:03d}"
    detailed = OUTCOME_DETAILED[mars_house]
    remedies = make_remedies(trial_nos)
    doc = _base_doc(rule_id, now)
    doc.update({
        "condition": {
            "type":            "dosha",
            "sub_type":        "mangalik",
            "dosha_type":      "mangalik",
            "planets_involved": ["Mars"],
            "houses_involved": [mars_house],
            "ascendant":       ascendant,
            "aspect_houses":   ASPECT_HOUSES[mars_house],
            "sub_conditions":  [],
            "operator":        "and",
            "gender_context":  "neutral",
            "is_benefic":      False,
            "yoga_check": {
                "type":             "planet_in_house",
                "checkable":        True,
                "planet":           "Mars",
                "houses":           [mars_house],
                "ascendant_filter": ascendant,
                "description": (
                    f"Mars in house {mars_house} with {ascendant} ascendant. "
                    f"Ascendant-specific remedy lookup."
                ),
            },
        },
        "interpretation": {
            "summary":            outcome_summary,
            "detailed":           detailed,
            "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
            "remedies":           remedies,
            "life_domain":        "marriage",
            "life_domains":       ["marriage", "domestic", "relationships"],
            "tags": [
                "mangalik",
                f"mars_h{mars_house}",
                f"ascendant_{ascendant.lower()}",
                "remedy_rule",
            ],
            "physical_markers": [],
        },
        "metadata": {
            "planets_involved":     ["Mars"],
            "houses_involved":      [mars_house],
            "signs_involved":       [],
            "condition_count":      1,
            "gender_context":       "neutral",
            "is_group_summary":     False,
            "has_physical_markers": False,
            "physical_categories":  [],
            "yoga_checkable":       True,
        },
        "confidence": {
            "source_confidence": "HIGH",
            "extraction_method": "hard_coded",
            "validated":         False,
        },
    })
    return doc


def build_conjunction_rule(conj: dict, index: int, now: str) -> dict:
    """9 special conjunction / Yog rules."""
    rule_id    = f"lalkitab-ch19-{index:03d}"
    yoga_check = conj["yoga_check"]
    checkable  = yoga_check.get("checkable", False)

    houses: list[int] = []
    if yoga_check.get("type") == "planet_in_house":
        houses = yoga_check.get("houses", [])
    elif yoga_check.get("type") == "multi_house_requirements":
        for hr in yoga_check.get("house_requirements", []):
            houses.extend(hr.get("houses", []))
        houses = sorted(set(houses))

    detailed = (
        f"Condition: {conj['condition_text']}\n\n"
        f"Outcome: {conj['outcome']}"
    )
    doc = _base_doc(rule_id, now)
    doc.update({
        "condition": {
            "type":            "planetary_combination",
            "sub_type":        "special_yog",
            "planets_involved": [],
            "houses_involved": houses,
            "sub_conditions":  [],
            "operator":        "and",
            "gender_context":  "neutral",
            "is_benefic":      conj["is_benefic"],
            "yoga_check":      yoga_check,
        },
        "interpretation": {
            "summary":            conj["outcome"][:120],
            "detailed":           detailed,
            "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
            "remedies":           [],
            "life_domain":        conj["life_domains"][0] if conj["life_domains"] else "general",
            "life_domains":       conj["life_domains"],
            "tags":               conj["tags"],
            "physical_markers":   [],
        },
        "metadata": {
            "planets_involved":     [],
            "houses_involved":      houses,
            "signs_involved":       [],
            "condition_count":      len(houses) or 1,
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


def build_general_rule(gen: dict, index: int, now: str) -> dict:
    """2 social ID + 2 general principle rules."""
    rule_id  = f"lalkitab-ch19-{index:03d}"
    detailed = (
        f"Condition: {gen['condition_text']}\n\n"
        f"Outcome: {gen['outcome']}"
    )
    doc = _base_doc(rule_id, now)
    doc.update({
        "condition": {
            "type":            "general_principle",
            "sub_type":        gen["rule_type"],
            "planets_involved": [],
            "houses_involved": [],
            "sub_conditions":  [],
            "operator":        "and",
            "gender_context":  "neutral",
            "is_benefic":      gen["is_benefic"],
            "yoga_check": {
                "type":      "complex",
                "checkable": False,
                "description": "General principle — not a formation condition.",
            },
        },
        "interpretation": {
            "summary":            gen["outcome"][:120],
            "detailed":           detailed,
            "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
            "remedies":           [],
            "life_domain":        gen["life_domains"][0] if gen["life_domains"] else "general",
            "life_domains":       gen["life_domains"],
            "tags":               gen["tags"],
            "physical_markers":   [],
        },
        "metadata": {
            "planets_involved":     [],
            "houses_involved":      [],
            "signs_involved":       [],
            "condition_count":      1,
            "gender_context":       "neutral",
            "is_group_summary":     False,
            "has_physical_markers": False,
            "physical_categories":  [],
            "yoga_checkable":       False,
        },
        "confidence": {
            "source_confidence": "HIGH",
            "extraction_method": "hard_coded",
            "validated":         False,
        },
    })
    return doc


# ── Assemble all rules ────────────────────────────────────────────────────────

def build_all_rules() -> list[dict]:
    now   = datetime.now(timezone.utc).isoformat()
    rules = []
    idx   = 1

    # Group 1 — 5 base house rules
    for house in [1, 4, 7, 8, 12]:
        rules.append(build_base_house_rule(house, idx, now))
        idx += 1

    # Group 2 — 60 ascendant-specific rules
    for (asc, mh, trials, summary) in ASC_RULES:
        rules.append(build_ascendant_rule(asc, mh, trials, summary, idx, now))
        idx += 1

    # Group 3 — 9 special conjunction rules
    for conj in CONJUNCTION_RULES:
        rules.append(build_conjunction_rule(conj, idx, now))
        idx += 1

    # Group 4 — 4 general / social rules
    for gen in GENERAL_RULES:
        rules.append(build_general_rule(gen, idx, now))
        idx += 1

    return rules


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest Lal Kitab Ch 19 — Mangalik Evil and Trials"
    )
    parser.add_argument("--dry-run",   action="store_true",
                        help="Build rules and print summary without writing")
    parser.add_argument("--save",      metavar="PATH",
                        help="Save dry-run JSON to file")
    parser.add_argument("--upload",    metavar="PATH",
                        help="Upload rules from saved JSON (zero API calls)")
    parser.add_argument("--mongo-url", default="mongodb://localhost:27017")
    parser.add_argument("--db-name",   default="horoscope_db")
    args = parser.parse_args()

    # ── Upload path ───────────────────────────────────────────────────────────
    if args.upload:
        from pymongo import MongoClient
        path = Path(args.upload)
        if not path.exists():
            print(f"ERROR: file not found: {path}", file=sys.stderr)
            sys.exit(1)
        with open(path) as f:
            rules = json.load(f)
        client = MongoClient(args.mongo_url)
        coll   = client[args.db_name]["interpretation_rules"]
        result = coll.insert_many(rules)
        print(f"✅ Uploaded {len(result.inserted_ids)} rules to "
              f"{args.db_name}.interpretation_rules")
        print(f"   Batch ID: {BATCH_ID}")
        print(f"\nNext step — validate:")
        print(f"   python3 scripts/validate_rules.py "
              f"--mongo-url $MONGO_URL --db-name {args.db_name} "
              f"--batch-id {BATCH_ID}")
        client.close()
        return

    # ── Build rules ───────────────────────────────────────────────────────────
    rules = build_all_rules()

    # ── Summary ───────────────────────────────────────────────────────────────
    total      = len(rules)
    checkable  = [r for r in rules if r["metadata"]["yoga_checkable"]]
    by_type: dict[str, int] = {}
    for r in rules:
        t = r["condition"]["type"]
        by_type[t] = by_type.get(t, 0) + 1

    print(f"\nLal Kitab Ch {CHAPTER} — {CHAP_NAME}")
    print(f"  Total rules  : {total}")
    print(f"  Checkable    : {len(checkable)} / {total} "
          f"({100 * len(checkable) // total}%)")
    print(f"  Batch ID     : {BATCH_ID}")
    print(f"\n  By condition type:")
    for t, n in by_type.items():
        print(f"    {t:<25} {n} rules")

    print(f"\n  Checkable rules:")
    for r in checkable:
        yc = r["condition"]["yoga_check"]
        asc = r["condition"].get("ascendant") or "—"
        print(f"    {r['rule_id']}  {yc.get('type','?'):<25}  asc={asc}")

    if args.dry_run and not args.save:
        print("\n  [dry-run only — use --save to write JSON]")
        return

    # ── Save ──────────────────────────────────────────────────────────────────
    out_path = Path(args.save) if args.save else None
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(rules, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"\n✅ Saved {total} rules → {out_path}")
        print(f"\nNext step — review {out_path}, then upload:")
        print(f"   python3 scripts/ingest_lalkitab_ch19_v1.py \\")
        print(f"     --upload {out_path} --mongo-url $MONGO_URL "
              f"--db-name {args.db_name}")


if __name__ == "__main__":
    main()
