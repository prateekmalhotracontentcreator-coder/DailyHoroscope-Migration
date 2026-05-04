#!/usr/bin/env python3
"""
ingest_lalkitab_ch21_v1.py — Lal Kitab Chapter 21: Freedom From Debt (Pitra Rina)

43 rules total across 7 groups:
    6  Global principles           (GP-01 to GP-06)
    2  Yoga combinations           (Kalsarpa, Khemdrum)
    8  Mercury Rival logic         (MERC-RIVAL-01 to 08)
    7  Jupiter Debt logic          (JUP-DEBT-01 to 06 + secondary markers)
    9  Core debt doshas            (debt-jupiter / sun / moon / venus / mars /
                                    mercury / saturn / rahu / ketu)
    7  Temporal remedy windows     (window per planet, Jupiter through Saturn)
    4  Family remedial logic       (equal-share, solo multiplier, sequencing, fast)

Source: Lal Kitab Ch 21 JSON Ready (V4) + Diagnostics file
Extraction: hard_coded — zero API calls.
Note: Diagnostic file cites "Sun+Venus+Mars in H12" for Rahu debt;
      JSON Ready file cites "Sun+Moon+Mars in H12". JSON Ready used as primary.

BATCH_ID = "lalkitab-ch21-v1-20260504"

Standard workflow:
  Step 1 — Dry run + save:
    python3 scripts/ingest_lalkitab_ch21_v1.py --dry-run \\
      --save scripts/lalkitab_ch21_rules.json

  Step 2 — Review JSON; amend as needed.

  Step 3 — Upload:
    python3 scripts/ingest_lalkitab_ch21_v1.py \\
      --upload scripts/lalkitab_ch21_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 4 — Validate:
    python3 scripts/validate_rules.py \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id lalkitab-ch21-v1-20260504
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
CHAPTER   = 21
CHAP_NAME = "Freedom From Debt — Pitra Rina"
BATCH_ID  = "lalkitab-ch21-v1-20260504"


# ── Shared base doc builder ───────────────────────────────────────────────────

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


# ── Section 2: Global Principles ─────────────────────────────────────────────

GLOBAL_PRINCIPLES = [
    {
        "id":    "gp-01",
        "name":  "Weakening Effect — Debt Identification via Sign Occupation",
        "text":  (
            "When a malefic planet occupies the sign of another planet, the sign's "
            "beneficial effect is destroyed and the malefic planet itself becomes "
            "weak. This simultaneous sign-destruction and self-weakening marks the "
            "presence of a Father's Debt (Pitra Rina) in the horoscope."
        ),
        "yoga_check_type": "horoscope_only",
        "note":  "manual_validation_required",
    },
    {
        "id":    "gp-02",
        "name":  "Significator Affliction — Curse of Family Member",
        "text":  (
            "If the significator house of Planet X contains an enemy planet of X, "
            "that house is afflicted. This affliction signals a curse from the "
            "corresponding family member represented by the significator."
        ),
        "yoga_check_type": "horoscope_only",
        "note":  "manual_validation_required",
    },
    {
        "id":    "gp-03",
        "name":  "Debilitated Recurrence — Generational Debt Confirmation",
        "text":  (
            "If a debilitated planet occupies the same house (or a house of similar "
            "significance) in both the native's horoscope and in the horoscope of the "
            "father, son, or brother, the pattern confirms an inherited karmic "
            "obligation — a generational debt is locked in."
        ),
        "yoga_check_type": "horoscope_only",
        "note":  "generational_mapping_required",
    },
    {
        "id":    "gp-04",
        "name":  "Jupiter Aspect — H9 Lord Displaced + Enemy Aspects Jupiter",
        "text":  (
            "If the lord of the 9th house (Jupiter's significator house) is placed in "
            "any other house AND an enemy planet aspects Jupiter, Jupiter is designated "
            "as the primary Debt Planet for that horoscope."
        ),
        "yoga_check_type": "horoscope_only",
    },
    {
        "id":    "gp-05",
        "name":  "Diminishing Influence — Enemy in Planet's Own Sign",
        "text":  (
            "If an enemy planet occupies the house of another planet and the enemy's "
            "own influence is in a state of diminishing, this marks a horoscope "
            "afflicted with Father's Debt."
        ),
        "yoga_check_type": "horoscope_only",
    },
    {
        "id":    "gp-06",
        "name":  "Mutual Destruction Gate — Enemies in Jupiter's Significator Houses",
        "text":  (
            "If the planets occupying the significator houses of Jupiter (the 9th house) "
            "are mutual enemies, or if those planets operate to destroy Jupiter's "
            "influence, Father's Debt is confirmed."
        ),
        "yoga_check_type": "horoscope_only",
    },
]


# ── Section 3: Yoga Combinations ─────────────────────────────────────────────

YOGA_COMBOS = [
    {
        "id":    "yoga-kalsarpa",
        "name":  "Kalsarpa Yoga — Generational Dosha",
        "text":  (
            "Presence of Kalsarpa Yoga in the horoscope indicates a generational dosha. "
            "The native's economic progress stalls and family joy is nullified. The "
            "affliction propagates across family genitures (son, grandson, nephew). "
            "Recurrence of Kalsarpa in multiple family charts confirms Pitra Rina."
        ),
        "planets": ["Rahu", "Ketu"],
        "checkable": True,
        "yoga_check_desc": "Kalsarpa Yoga — all seven planets hemmed between Rahu and Ketu. Standard yoga check.",
    },
    {
        "id":    "yoga-khemdrum",
        "name":  "Khemdrum Yoga — Moon Affliction Generational Debt",
        "text":  (
            "If the native has Khemdrum Yoga (Moon with no planets in the 2nd or 12th "
            "from Moon, i.e., Moon is alone), the same yoga is predicted to recur in "
            "the genitures of the son, grandson, brother, and nephew. This causes "
            "mental agitation and is a marker of generational Father's Debt."
        ),
        "planets": ["Moon"],
        "checkable": True,
        "yoga_check_desc": "Khemdrum Yoga — Moon in isolation (no planets in 2nd or 12th from Moon). Phase 2 check.",
    },
]


# ── Section 4a: Mercury Rival Logic ──────────────────────────────────────────
# Each entry: (mercury_houses, planet_in_h9, spoiled_planet)

MERCURY_RIVAL = [
    ([1, 8],     "Jupiter", "Jupiter"),
    ([2, 7],     "Venus",   "Venus"),
    ([3],        "Rahu",    "Rahu"),
    ([4],        "Moon",    "Moon"),
    ([5],        "Sun",     "Sun"),
    ([6],        "Ketu",    "Ketu"),
    ([10, 11],   "Saturn",  "Saturn"),
    ([12],       "Jupiter", "Jupiter"),
]


# ── Section 4b: Jupiter Center Placement Logic ────────────────────────────────
# Each entry: (secondary_conditions, description)
# Jupiter anchor: always in [1, 4, 7, 10]

JUPITER_DEBT = [
    # JUP-DEBT-01
    {
        "id":   "jup-debt-01",
        "name": "Jupiter Debt — Saturn in H2",
        "secondary_planets": ["Saturn"],
        "secondary_houses":  [2],
        "text": (
            "Jupiter in a kendra house (1/4/7/10) AND Saturn in the 2nd house "
            "confirms Father's Debt via Jupiter. Saturn's position in the house "
            "of speech and accumulated wealth afflicts the Jupiter channel."
        ),
    },
    # JUP-DEBT-02
    {
        "id":   "jup-debt-02",
        "name": "Jupiter Debt — Venus in H5",
        "secondary_planets": ["Venus"],
        "secondary_houses":  [5],
        "text": (
            "Jupiter in a kendra house (1/4/7/10) AND Venus in the 5th house "
            "confirms Father's Debt via Jupiter. Venus in H5 spoils Jupiter's "
            "progeny and intelligence channel."
        ),
    },
    # JUP-DEBT-03
    {
        "id":   "jup-debt-03",
        "name": "Jupiter Debt — Mercury in H9",
        "secondary_planets": ["Mercury"],
        "secondary_houses":  [9],
        "text": (
            "Jupiter in a kendra house (1/4/7/10) AND Mercury in the 9th house "
            "confirms Father's Debt via Jupiter. Mercury in Jupiter's significator "
            "house rivals and spoils Jupiter's dharma channel."
        ),
    },
    # JUP-DEBT-04
    {
        "id":   "jup-debt-04",
        "name": "Jupiter Debt — Rahu in H12",
        "secondary_planets": ["Rahu"],
        "secondary_houses":  [12],
        "text": (
            "Jupiter in a kendra house (1/4/7/10) AND Rahu in the 12th house "
            "confirms Father's Debt via Jupiter. Rahu's presence in the house "
            "of foreign lands and moksha disrupts Jupiter's expansive influence."
        ),
    },
    # JUP-DEBT-05
    {
        "id":   "jup-debt-05",
        "name": "Jupiter Debt — Mercury in H3 + Venus in H6",
        "secondary_planets": ["Mercury", "Venus"],
        "secondary_houses":  [3, 6],
        "text": (
            "Jupiter in a kendra house (1/4/7/10) AND Mercury in the 3rd house "
            "AND Venus in the 6th house simultaneously confirms Father's Debt via "
            "Jupiter. This dual-planet affliction pattern is a compound trigger."
        ),
    },
    # JUP-DEBT-06
    {
        "id":   "jup-debt-06",
        "name": "Jupiter Debt — Saturn in H3 or H6",
        "secondary_planets": ["Saturn"],
        "secondary_houses":  [3, 6],
        "text": (
            "Jupiter in a kendra house (1/4/7/10) AND Saturn in the 3rd or 6th "
            "house confirms Father's Debt via Jupiter. Saturn's presence in these "
            "houses of effort and enemies blocks Jupiter's protective blessings."
        ),
    },
]

JUPITER_SECONDARY = {
    "id":   "jup-secondary",
    "name": "Father's Debt — Secondary Conjunction Markers",
    "text": (
        "Presence of any of the following secondary markers confirms a potential "
        "Father's Debt via secondary conjunction: Rahu in H11 · Saturn in H4 or H6 · "
        "Mercury in H2, H3, H8, H11, or H12. These are confirmatory markers used "
        "alongside the primary Jupiter Center logic gates."
    ),
    "markers": [
        {"planet": "Rahu",    "houses": [11]},
        {"planet": "Saturn",  "houses": [4, 6]},
        {"planet": "Mercury", "houses": [2, 3, 8, 11, 12]},
    ],
}


# ── Section 5: Core Debt Doshas (9 Planets) ──────────────────────────────────

DEBT_DOSHAS = [
    {
        "id":            "debt-jupiter",
        "debt_planet":   "Jupiter",
        "debt_name":     "Father's Debt — Pitra Rina",
        "debt_type":     "pitra_rina",
        "trigger_planets": ["Venus", "Rahu", "Mercury"],
        "trigger_houses":  [2, 5, 9, 12],
        "anchor_planet":   "Jupiter",
        "anchor_houses":   [2, 5, 9, 12],
        "negative_planet": None,
        "negative_houses": [],
        "karmic_reason": (
            "Father changed the family priest; father caused or hired others to kill dogs."
        ),
        "symptoms": (
            "Nearby religious temple or Peepal tree destroyed; habit of wearing necklaces "
            "or garlands; premature whitening of hair; hair fall at the choti (braided "
            "tress); incomplete education or study hurdles; imprisonment despite innocence. "
            "Age window of impact: 16–24 years."
        ),
        "outcomes": (
            "Whitening hair by age 16–24; incomplete education; legal imprisonment despite "
            "innocence; ancestral spiritual markers (temple, Peepal tree) in ruins."
        ),
        "remedies": [
            {"text": "Collect equal money from all blood family members; donate the pooled sum to a temple.", "category": "offering"},
            {"text": "Clean a nearby neglected temple — restore it to a worshipful state.", "category": "ritual"},
            {"text": "Water and care for a Peepal tree regularly.", "category": "ritual"},
        ],
        "life_domains": ["ancestry", "education", "legal", "spirituality"],
        "tags": ["pitra_rina", "jupiter", "debt", "generational"],
    },
    {
        "id":            "debt-sun",
        "debt_planet":   "Sun",
        "debt_name":     "Self-Debt — Swayam Rina",
        "debt_type":     "swayam_rina",
        "trigger_planets": ["Venus"],
        "trigger_houses":  [5],
        "anchor_planet":   None,
        "anchor_houses":   [],
        "negative_planet": "Sun",
        "negative_houses": [1, 11],
        "karmic_reason": (
            "The native (or ancestor) dishonored religion/tradition; adopted atheism."
        ),
        "symptoms": (
            "A fire pot embedded under the floor of the home; an open section of the "
            "roof that allows light entry; heart disease present in the family."
        ),
        "outcomes": (
            "Doom or theft in the family when a son reaches 11 months or 11 years of "
            "age; body becomes inflexible with constant drooling; wealth status doomed."
        ),
        "remedies": [
            {"text": "Collect equal contributions from all family members; perform Sun's yajna with the combined capital.", "category": "ritual"},
        ],
        "life_domains": ["health", "wealth", "spirituality", "progeny"],
        "tags": ["swayam_rina", "sun", "debt", "heart", "yajna"],
    },
    {
        "id":            "debt-moon",
        "debt_planet":   "Moon",
        "debt_name":     "Mother's Debt — Matri Rina",
        "debt_type":     "matri_rina",
        "trigger_planets": ["Ketu"],
        "trigger_houses":  [4],
        "anchor_planet":   None,
        "anchor_houses":   [],
        "negative_planet": "Moon",
        "negative_houses": [4],
        "karmic_reason": (
            "Mother was disregarded after progeny birth; mother sent out of home; "
            "mother's grief was ignored."
        ),
        "symptoms": (
            "A neighboring well, river, or drainage system has been converted into a "
            "rubbish pile or effluent drain — water body desecrated."
        ),
        "outcomes": (
            "Savings depleted; chronic illness; weakened sensory perception; "
            "affliction spreads to those who help the native."
        ),
        "remedies": [
            {"text": "Collect equal shares of silver from all blood family members; drop all silver into a river at one single time.", "category": "offering"},
        ],
        "life_domains": ["health", "wealth", "family", "mother"],
        "tags": ["matri_rina", "moon", "debt", "silver", "water"],
    },
    {
        "id":            "debt-venus",
        "debt_planet":   "Venus",
        "debt_name":     "Wife's Debt — Stri Rina",
        "debt_type":     "stri_rina",
        "trigger_planets": ["Sun", "Rahu", "Ketu", "Moon"],
        "trigger_houses":  [2, 7],
        "anchor_planet":   None,
        "anchor_houses":   [],
        "negative_planet": "Venus",
        "negative_houses": [1, 8],
        "trigger_note": (
            "Primary: Sun/Rahu/Ketu in H2. Secondary reinforcement: Sun/Moon/Rahu in H2 or H7."
        ),
        "karmic_reason": (
            "An ancestor killed a pregnant woman for greed; family members fought "
            "amongst themselves."
        ),
        "symptoms": (
            "Collective family loathing of cows/service to animals; sorrow or death "
            "occurring in the family during occasions of joy."
        ),
        "outcomes": (
            "Death in family during joyful events; financial misfortune linked to Venus "
            "affliction."
        ),
        "remedies": [
            {"text": "Collect equal funds from all family members; feed fodder to 100 unimpaired (non-disabled) cows in a single day.", "category": "succour"},
            {"text": "Maintain proper traditional attire as respect for the feminine principle.", "category": "ritual"},
        ],
        "life_domains": ["marriage", "family", "wealth", "karma"],
        "tags": ["stri_rina", "venus", "debt", "cow", "karma"],
    },
    {
        "id":            "debt-mars",
        "debt_planet":   "Mars",
        "debt_name":     "Kin's Debt — Bandhu Rina",
        "debt_type":     "bandhu_rina",
        "trigger_planets": ["Mercury", "Ketu"],
        "trigger_houses":  [1, 8],
        "anchor_planet":   None,
        "anchor_houses":   [],
        "negative_planet": "Mars",
        "negative_houses": [7],
        "karmic_reason": (
            "An ancestor poisoned or deceived a friend; committed arson (burning crops "
            "or a house); killed someone else's buffalo."
        ),
        "symptoms": (
            "Hatred among kith and kin; no birthday celebrations in the household."
        ),
        "outcomes": (
            "Lack of progeny or disabled offspring; anaemia; non-functional joints; "
            "blindness in one eye; beaten without reason."
        ),
        "remedies": [
            {"text": "Collect equal money from each family member; donate the pooled funds to a doctor for the treatment of poor patients.", "category": "succour"},
        ],
        "life_domains": ["health", "progeny", "relationships", "karma"],
        "tags": ["bandhu_rina", "mars", "debt", "medical", "charity"],
    },
    {
        "id":            "debt-mercury",
        "debt_planet":   "Mercury",
        "debt_name":     "Sister/Daughter Debt — Bhagin Rina",
        "debt_type":     "bhagin_rina",
        "trigger_planets": ["Moon"],
        "trigger_houses":  [3, 6],
        "anchor_planet":   None,
        "anchor_houses":   [],
        "negative_planet": "Mercury",
        "negative_houses": [2, 12],
        "karmic_reason": (
            "An ancestor deceived or killed a sister or daughter; dishonored a female "
            "relative's chastity."
        ),
        "symptoms": (
            "Desire to sell or replace innocent children (child trafficking urge in "
            "the family lineage)."
        ),
        "outcomes": (
            "Misfortune during marriage of female relatives; loss of copulation power; "
            "teeth fall out; loss of sensory perception; wealth wasted during marriage."
        ),
        "remedies": [
            {"text": "Path A: Collect yellow shells from all family members; burn to ash and float in flowing water.", "category": "offering"},
            {"text": "Path B (Wednesday only): Prepare halwa/puri in pure ghee and feed 101 maids after washing their feet.", "category": "ritual"},
        ],
        "life_domains": ["marriage", "health", "family", "female_relatives"],
        "tags": ["bhagin_rina", "mercury", "debt", "sisters", "daughters"],
    },
    {
        "id":            "debt-saturn",
        "debt_planet":   "Saturn",
        "debt_name":     "Ruthless Debt — Kroor Rina",
        "debt_type":     "kroor_rina",
        "trigger_planets": ["Sun", "Moon"],
        "trigger_houses":  [10, 11],
        "trigger_operator": "and",
        "anchor_planet":   None,
        "anchor_houses":   [],
        "negative_planet": "Saturn",
        "negative_houses": [3, 4],
        "trigger_note": "Both Sun AND Moon must be in H10 or H11 simultaneously.",
        "karmic_reason": (
            "An ancestor committed murder; grabbed a house or property by deceit."
        ),
        "symptoms": (
            "South-facing main entrance to the home; house built on orphanage land, "
            "road, or atop a well."
        ),
        "outcomes": (
            "High frequency of accidents; family members become handicapped; hair "
            "falls from eyelids and eyebrows (alopecia of facial hair)."
        ),
        "remedies": [
            {"text": "Path A: Collect money from all family members and feed 100 laborers at the same time in one day.", "category": "succour"},
            {"text": "Path B: Offer bread to crows every day for 43 consecutive days.", "category": "offering"},
            {"text": "Path C: Collect fish from 100 separate sources and feed them in water.", "category": "offering"},
        ],
        "life_domains": ["health", "property", "karma", "accidents"],
        "tags": ["kroor_rina", "saturn", "debt", "murder", "property"],
    },
    {
        "id":            "debt-rahu",
        "debt_planet":   "Rahu",
        "debt_name":     "Debt of the Unborn — Praan Rina",
        "debt_type":     "praan_rina",
        "trigger_planets": ["Sun", "Moon", "Mars"],
        "trigger_houses":  [12],
        "trigger_note": (
            "Any of Sun/Moon/Mars in H12 triggers this debt. "
            "Note: Diagnostic cites Sun+Venus+Mars; JSON Ready cites Sun+Moon+Mars. "
            "JSON Ready used as primary source."
        ),
        "anchor_planet":   None,
        "anchor_houses":   [],
        "negative_planet": "Rahu",
        "negative_houses": [6],
        "karmic_reason": (
            "An ancestor deceived in-laws or cheated contacts continuously until "
            "the entire family was doomed."
        ),
        "symptoms": (
            "The south wall of the home adjoins forlorn land or a popcorn factory; "
            "an effluent drain is situated under the main threshold of the home."
        ),
        "outcomes": (
            "All efforts produce the opposite of the intended result; imprisonment "
            "without cause."
        ),
        "remedies": [
            {"text": "Gather one coconut from every family member; float all coconuts simultaneously in a river or flowing water.", "category": "offering"},
            {"text": "Maintain joint family residency and keep good relations with in-laws.", "category": "succour"},
        ],
        "life_domains": ["karma", "legal", "family", "in_laws"],
        "tags": ["praan_rina", "rahu", "debt", "coconut", "in_laws"],
    },
    {
        "id":            "debt-ketu",
        "debt_planet":   "Ketu",
        "debt_name":     "Nature's Debt — Prakriti Rina",
        "debt_type":     "prakriti_rina",
        "trigger_planets": ["Moon", "Mars"],
        "trigger_houses":  [6],
        "trigger_operator": "and",
        "trigger_note": "Both Moon AND Mars must be in H6 simultaneously.",
        "anchor_planet":   None,
        "anchor_houses":   [],
        "negative_planet": "Ketu",
        "negative_houses": [2],
        "karmic_reason": (
            "An ancestor killed a dog out of ill will; troubled holy men or mendicants; "
            "lived dishonestly with a lewd character."
        ),
        "symptoms": (
            "Secretly killing others' offspring; killing dogs by bullet; intent to "
            "end relatives' bloodlines."
        ),
        "outcomes": (
            "Male child is born handicapped, dies shortly after birth, or is never "
            "born; urinary diseases present."
        ),
        "remedies": [
            {"text": "Collect equal money from all family members; feed 100 dogs at once in a single day.", "category": "succour"},
            {"text": "Provide aid and assistance to neighborhood widows.", "category": "succour"},
        ],
        "life_domains": ["progeny", "health", "karma", "animals"],
        "tags": ["prakriti_rina", "ketu", "debt", "dogs", "progeny"],
    },
]


# ── Section 6: Temporal Remedy Windows ───────────────────────────────────────
# Execute debt remedy before the planet's life-cycle year threshold

TEMPORAL_WINDOWS = [
    {"planet": "Jupiter", "max_age": 16, "slug": "jupiter"},
    {"planet": "Sun",     "max_age": 22, "slug": "sun"},
    {"planet": "Moon",    "max_age": 24, "slug": "moon"},
    {"planet": "Venus",   "max_age": 25, "slug": "venus"},
    {"planet": "Mars",    "max_age": 28, "slug": "mars"},
    {"planet": "Mercury", "max_age": 34, "slug": "mercury"},
    {"planet": "Saturn",  "max_age": 36, "slug": "saturn"},
]


# ── Section 7: Family Remedial Logic ─────────────────────────────────────────

FAMILY_LOGIC = [
    {
        "id":   "fam-01",
        "name": "Equal Share Protocol — Blood Relation Contribution",
        "text": (
            "All debt remedies MUST include equal contributions (money, silver, or "
            "prescribed material) from ALL blood relations, specifically: Son, Daughter, "
            "Grandson (Dauhitra), Sister, Nephew, Niece. No family member may be "
            "excluded from the contribution pool."
        ),
    },
    {
        "id":   "fam-02",
        "name": "Solitary Native Multiplier — 10× Individual Share",
        "text": (
            "If the native is the only available family member (no blood relations "
            "living), the native must perform the remedy alone but multiply their "
            "individual contribution by 10. One share performed solo = 10 shares of "
            "the standard remedy."
        ),
    },
    {
        "id":   "fam-03",
        "name": "Remedial Sequencing — One at a Time, 7–14 Day Break",
        "text": (
            "Only ONE debt remedy should be performed at a time. A mandatory rest "
            "period of 7 to 14 days must be observed before initiating the next "
            "remedial measure. Performing multiple remedies simultaneously is "
            "prohibited."
        ),
    },
    {
        "id":   "fam-04",
        "name": "Family Growth Fast — 40 to 43 Day Consecutive Fasts",
        "text": (
            "To ensure family expansion and assist debt removal, the native should "
            "observe fasts for 40 to 43 days over a consecutive period of 40 to 43 "
            "weeks. This extended fasting protocol strengthens the family channel."
        ),
    },
]


# ── Rule builders ─────────────────────────────────────────────────────────────

def build_global_principles(now: str) -> list[dict]:
    rules = []
    for i, gp in enumerate(GLOBAL_PRINCIPLES, start=1):
        rule_id = f"lalkitab-ch21-{gp['id']}"
        doc = _base(rule_id, now)
        doc.update({
            "condition": {
                "type": "general_principle",
                "sub_type": "debt_identification",
                "yoga_check": {
                    "type":      gp["yoga_check_type"],
                    "checkable": False,
                    "description": (
                        "Requires comparison across multiple chart placements or "
                        "multi-generational horoscopes. Not automatable in Phase 1."
                    ),
                },
            },
            "interpretation": {
                "summary":  gp["name"],
                "detailed": gp["text"],
                "full_text_passages": [{"text": gp["text"], "confidence": "HIGH"}],
                "remedies":     [],
                "life_domain":  "ancestry",
                "life_domains": ["ancestry", "karma", "generational"],
                "tags":         ["general_principle", "pitra_rina", "debt_identification"],
                "physical_markers": [],
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
        if "note" in gp:
            doc["condition"]["validation_note"] = gp["note"]
        rules.append(doc)
    return rules


def build_yoga_combos(now: str) -> list[dict]:
    rules = []
    for yc in YOGA_COMBOS:
        rule_id = f"lalkitab-ch21-{yc['id']}"
        doc = _base(rule_id, now)
        doc.update({
            "condition": {
                "type": "planetary_combination",
                "sub_type": "generational_yoga",
                "planets_involved": yc["planets"],
                "yoga_check": {
                    "type":        "yoga",
                    "checkable":   yc["checkable"],
                    "description": yc["yoga_check_desc"],
                },
            },
            "interpretation": {
                "summary":  yc["name"],
                "detailed": yc["text"],
                "full_text_passages": [{"text": yc["text"], "confidence": "HIGH"}],
                "remedies":     [],
                "life_domain":  "ancestry",
                "life_domains": ["ancestry", "karma", "generational", "family"],
                "tags":         ["planetary_combination", "generational", "debt"],
                "physical_markers": [],
            },
            "metadata": {
                "planets_involved":     yc["planets"],
                "houses_involved":      [],
                "signs_involved":       [],
                "condition_count":      1,
                "gender_context":       "neutral",
                "is_group_summary":     False,
                "has_physical_markers": False,
                "physical_categories":  [],
                "yoga_checkable":       yc["checkable"],
            },
            "confidence": {
                "source_confidence": "HIGH",
                "extraction_method": "hard_coded",
                "validated":         False,
            },
        })
        rules.append(doc)
    return rules


def build_mercury_rival(now: str) -> list[dict]:
    rules = []
    for i, (merc_houses, planet_h9, spoiled) in enumerate(MERCURY_RIVAL, start=1):
        rule_id = f"lalkitab-ch21-merc-rival-{i:02d}"
        h_str   = "/".join(str(h) for h in merc_houses)
        name    = f"Mercury Rival — Mercury in H{h_str}: {planet_h9} in H9 Spoiled"
        text    = (
            f"Mercury placed in house {h_str} AND {planet_h9} placed in the 9th house "
            f"activates Mercury's 'rival planet' role — {spoiled} is designated as "
            f"'spoiled' (its influence is corrupted). This mercury-9th-house combination "
            f"marks a debt affliction pattern through the spoiled planet's domain."
        )
        doc = _base(rule_id, now)
        doc.update({
            "condition": {
                "type": "planetary_combination",
                "sub_type": "mercury_rival",
                "planet_a": "Mercury",
                "planet_a_houses": merc_houses,
                "planet_b": planet_h9,
                "planet_b_houses": [9],
                "spoiled_planet": spoiled,
                "yoga_check": {
                    "type":        "yoga",
                    "checkable":   True,
                    "description": (
                        f"Mercury in H{h_str} AND {planet_h9} in H9. "
                        "Two-planet positional check."
                    ),
                },
            },
            "interpretation": {
                "summary":  name,
                "detailed": text,
                "full_text_passages": [{"text": text, "confidence": "HIGH"}],
                "remedies":     [],
                "life_domain":  "ancestry",
                "life_domains": ["ancestry", "karma", "debt"],
                "tags":         ["mercury_rival", "planetary_combination", "debt"],
                "physical_markers": [],
            },
            "metadata": {
                "planets_involved":     ["Mercury", planet_h9],
                "houses_involved":      merc_houses + [9],
                "signs_involved":       [],
                "condition_count":      2,
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
        rules.append(doc)
    return rules


def build_jupiter_debt(now: str) -> list[dict]:
    rules = []
    anchor_houses = [1, 4, 7, 10]

    for jd in JUPITER_DEBT:
        rule_id  = f"lalkitab-ch21-{jd['id']}"
        all_planets = ["Jupiter"] + jd["secondary_planets"]
        all_houses  = anchor_houses + jd["secondary_houses"]
        doc = _base(rule_id, now)
        doc.update({
            "condition": {
                "type": "planetary_combination",
                "sub_type": "jupiter_center_debt",
                "anchor_planet":       "Jupiter",
                "anchor_houses":       anchor_houses,
                "secondary_planets":   jd["secondary_planets"],
                "secondary_houses":    jd["secondary_houses"],
                "yoga_check": {
                    "type":        "yoga",
                    "checkable":   True,
                    "description": (
                        f"Jupiter in kendra {anchor_houses} AND "
                        f"{jd['secondary_planets']} in {jd['secondary_houses']}. "
                        "Two-condition positional check."
                    ),
                },
            },
            "interpretation": {
                "summary":  jd["name"],
                "detailed": jd["text"],
                "full_text_passages": [{"text": jd["text"], "confidence": "HIGH"}],
                "remedies":     [],
                "life_domain":  "ancestry",
                "life_domains": ["ancestry", "karma", "father"],
                "tags":         ["jupiter_center", "pitra_rina", "debt"],
                "physical_markers": [],
            },
            "metadata": {
                "planets_involved":     all_planets,
                "houses_involved":      all_houses,
                "signs_involved":       [],
                "condition_count":      2,
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
        rules.append(doc)

    # Secondary markers rule
    jds = JUPITER_SECONDARY
    rule_id = f"lalkitab-ch21-{jds['id']}"
    doc = _base(rule_id, now)
    doc.update({
        "condition": {
            "type": "planetary_combination",
            "sub_type": "jupiter_secondary_markers",
            "markers": jds["markers"],
            "operator": "or",
            "yoga_check": {
                "type":        "yoga",
                "checkable":   True,
                "description": (
                    "Any of: Rahu in H11 · Saturn in H4 or H6 · "
                    "Mercury in H2/3/8/11/12. OR-condition positional check."
                ),
            },
        },
        "interpretation": {
            "summary":  jds["name"],
            "detailed": jds["text"],
            "full_text_passages": [{"text": jds["text"], "confidence": "HIGH"}],
            "remedies":     [],
            "life_domain":  "ancestry",
            "life_domains": ["ancestry", "karma", "father"],
            "tags":         ["secondary_markers", "pitra_rina", "debt"],
            "physical_markers": [],
        },
        "metadata": {
            "planets_involved":     ["Rahu", "Saturn", "Mercury"],
            "houses_involved":      [11, 4, 6, 2, 3, 8, 12],
            "signs_involved":       [],
            "condition_count":      3,
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
    rules.append(doc)
    return rules


def build_debt_doshas(now: str) -> list[dict]:
    rules = []
    for dd in DEBT_DOSHAS:
        rule_id = f"lalkitab-ch21-{dd['id']}"
        doc = _base(rule_id, now)

        # Build condition
        cond: dict = {
            "type":              "dosha",
            "sub_type":         "debt",
            "debt_type":         dd["debt_type"],
            "debt_planet":       dd["debt_planet"],
            "trigger_planets":   dd["trigger_planets"],
            "trigger_houses":    dd["trigger_houses"],
            "requires_equal_family_share": True,
            "multiplier_if_solo": 10,
            "yoga_check": {
                "type":        "yoga",
                "checkable":   True,
                "description": (
                    f"{'/'.join(dd['trigger_planets'])} in H"
                    f"{'/'.join(str(h) for h in dd['trigger_houses'])}"
                    + (
                        f" AND {dd['debt_planet']} in H"
                        f"{'/'.join(str(h) for h in dd['anchor_houses'])}"
                        if dd.get("anchor_houses") else ""
                    )
                    + (
                        f"; NOT {dd['negative_planet']} in H"
                        f"{'/'.join(str(h) for h in dd['negative_houses'])}"
                        if dd.get("negative_planet") else ""
                    )
                ),
            },
        }
        if dd.get("anchor_planet"):
            cond["anchor_planet"]  = dd["anchor_planet"]
            cond["anchor_houses"]  = dd["anchor_houses"]
        if dd.get("negative_planet"):
            cond["negative_condition"] = {
                "planet":     dd["negative_planet"],
                "houses":     dd["negative_houses"],
                "constraint": "absent",
            }
        if dd.get("trigger_operator"):
            cond["trigger_operator"] = dd["trigger_operator"]
        if dd.get("trigger_note"):
            cond["trigger_note"] = dd["trigger_note"]

        detailed = (
            f"{dd['debt_name']}\n\n"
            f"Karmic Reason: {dd['karmic_reason']}\n\n"
            f"Symptoms: {dd['symptoms']}\n\n"
            f"Outcomes: {dd['outcomes']}"
        )

        doc.update({
            "condition": cond,
            "interpretation": {
                "summary":  dd["debt_name"],
                "detailed": detailed,
                "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
                "remedies":     dd["remedies"],
                "life_domain":  dd["life_domains"][0],
                "life_domains": dd["life_domains"],
                "tags":         dd["tags"],
                "physical_markers": [],
            },
            "metadata": {
                "planets_involved":     [dd["debt_planet"]] + dd["trigger_planets"],
                "houses_involved":      dd["trigger_houses"] + dd.get("anchor_houses", []) + dd.get("negative_houses", []),
                "signs_involved":       [],
                "condition_count":      2 if dd.get("negative_planet") else 1,
                "gender_context":       "neutral",
                "is_group_summary":     False,
                "has_physical_markers": True,
                "physical_categories":  ["karmic_symptoms", "environmental_markers"],
                "yoga_checkable":       True,
            },
            "confidence": {
                "source_confidence": "HIGH",
                "extraction_method": "hard_coded",
                "validated":         False,
            },
        })
        rules.append(doc)
    return rules


def build_temporal_windows(now: str) -> list[dict]:
    rules = []
    for tw in TEMPORAL_WINDOWS:
        rule_id = f"lalkitab-ch21-window-{tw['slug']}"
        name    = f"Remedial Window — {tw['planet']}: Before Age {tw['max_age']}"
        text    = (
            f"The debt remedy associated with {tw['planet']} MUST be performed "
            f"before the native reaches the age of {tw['max_age']} years. Executing "
            f"the remedy after this life-cycle threshold significantly reduces its "
            f"efficacy. Vedic planetary cycles define these age-specific windows for "
            f"maximum karmic rectification."
        )
        doc = _base(rule_id, now)
        doc.update({
            "condition": {
                "type": "general_principle",
                "sub_type": "remedial_timing",
                "timing_constraint": True,
                "planet":   tw["planet"],
                "max_age":  tw["max_age"],
                "yoga_check": {
                    "type":        "timing",
                    "checkable":   False,
                    "description": "Age-based timing constraint. Not automatable in Phase 1.",
                },
            },
            "interpretation": {
                "summary":  name,
                "detailed": text,
                "full_text_passages": [{"text": text, "confidence": "HIGH"}],
                "remedies":     [],
                "life_domain":  "general",
                "life_domains": ["karma", "timing", "remedy"],
                "tags":         ["timing", "remedial_window", tw["slug"], "debt"],
                "physical_markers": [],
            },
            "metadata": {
                "planets_involved":     [tw["planet"]],
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
        rules.append(doc)
    return rules


def build_family_logic(now: str) -> list[dict]:
    rules = []
    for fl in FAMILY_LOGIC:
        rule_id = f"lalkitab-ch21-{fl['id']}"
        doc = _base(rule_id, now)
        doc.update({
            "condition": {
                "type": "general_principle",
                "sub_type": "family_remedy_protocol",
                "yoga_check": {
                    "type":        "procedural",
                    "checkable":   False,
                    "description": "Procedural remedy execution rule. Not automatable.",
                },
            },
            "interpretation": {
                "summary":  fl["name"],
                "detailed": fl["text"],
                "full_text_passages": [{"text": fl["text"], "confidence": "HIGH"}],
                "remedies":     [],
                "life_domain":  "general",
                "life_domains": ["karma", "remedy", "family"],
                "tags":         ["family_protocol", "remedy_sequencing", "debt"],
                "physical_markers": [],
            },
            "metadata": {
                "planets_involved":     [],
                "houses_involved":      [],
                "signs_involved":       [],
                "condition_count":      0,
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
        rules.append(doc)
    return rules


# ── Main ──────────────────────────────────────────────────────────────────────

def build_all_rules() -> list[dict]:
    now = datetime.now(timezone.utc).isoformat()
    rules: list[dict] = []
    rules.extend(build_global_principles(now))      #  6
    rules.extend(build_yoga_combos(now))            #  2
    rules.extend(build_mercury_rival(now))          #  8
    rules.extend(build_jupiter_debt(now))           #  7
    rules.extend(build_debt_doshas(now))            #  9
    rules.extend(build_temporal_windows(now))       #  7
    rules.extend(build_family_logic(now))           #  4
    return rules                                    # 43 total


def main() -> None:
    parser = argparse.ArgumentParser()
    group  = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run",  action="store_true")
    group.add_argument("--upload",   metavar="JSON_FILE")
    parser.add_argument("--save",    metavar="JSON_FILE")
    parser.add_argument("--mongo-url")
    parser.add_argument("--db-name", default="horoscope_db")
    args = parser.parse_args()

    if args.dry_run:
        rules = build_all_rules()
        print(f"Dry run: {len(rules)} rules generated")

        # Group summary
        groups = {}
        for r in rules:
            prefix = "-".join(r["rule_id"].split("-")[2:4])
            groups[prefix] = groups.get(prefix, 0) + 1
        for k, v in groups.items():
            print(f"  {k}: {v}")

        if args.save:
            Path(args.save).write_text(json.dumps(rules, indent=2, ensure_ascii=False))
            print(f"Saved → {args.save}")
        return

    # Upload mode
    if not args.mongo_url:
        print("ERROR: --mongo-url required for upload", file=sys.stderr)
        sys.exit(1)

    from pymongo import MongoClient

    rules = json.loads(Path(args.upload).read_text())
    print(f"Loaded {len(rules)} rules from {args.upload}")

    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]

    inserted = updated = 0
    for r in rules:
        res = col.update_one(
            {"rule_id": r["rule_id"]},
            {"$set": r},
            upsert=True,
        )
        if res.upserted_id:
            inserted += 1
        elif res.modified_count:
            updated += 1

    print(f"✅ Inserted {inserted} / Updated {updated} rules → {args.db_name}.interpretation_rules")
    client.close()


if __name__ == "__main__":
    main()
