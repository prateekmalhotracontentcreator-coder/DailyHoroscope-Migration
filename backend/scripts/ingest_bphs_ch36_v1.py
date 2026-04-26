#!/usr/bin/env python3
"""
ingest_bphs_ch36_v1.py — BPHS Chapter 36: Many Other Yogas

25 named yogas (Subha through Chandradhi, incl. 3 Trimurthi sub-yogas)
+ 7 divisional-dignity rules = 32 rules total.

Added after dry-run review:
  - Hamsa Yoga (Sloka 3-4 Notes): Jupiter in exaltation (Cancer) in kendra
    from Moon; Pancha Mahapurusha form, distinct from ordinary Gajakesari.
  - Chandradhi Yoga (Sloka 37 Notes): Benefics in 6th/7th/8th from the Moon;
    Moon-based counterpart to Lagnadhi which counts from ascendant.

All rules are hard-coded from the source RTF — zero AI extraction cost.

Standard --save/--upload workflow:
  Step 1 — Dry run:
    python3 scripts/ingest_bphs_ch36_v1.py --dry-run --save bphs_ch36_rules.json

  Step 2 — Review bphs_ch36_rules.json; amend as needed.

  Step 3 — Upload (zero API calls):
    python3 scripts/ingest_bphs_ch36_v1.py \\
      --upload bphs_ch36_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 4 — Validate:
    python3 scripts/validate_rules.py \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id bphs-ch36-v1-20260426
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Constants ─────────────────────────────────────────────────────────────────

SCIENCE    = "jyotish"
BOOK       = "Brihat Parashara Hora Shastra"
BOOK_ID    = "bphs"
CHAPTER    = 36
CHAP_NAME  = "Many Other Yogas"
BATCH_ID   = "bphs-ch36-v1-20260426"

# ── yoga_check.type legend ────────────────────────────────────────────────────
# benefics_in_houses        — natural benefics occupy specified houses
# malefics_in_houses        — natural malefics occupy specified houses
# planet_in_kendra_from     — planet in angular house relative to reference point
# benefic_only_in_house     — benefic in house with no malefic co-occupation
# planet_in_house           — specific planet in specific house(s)
# complex                   — compound / multi-lord condition; checkable=False
# divisional_dignity        — lagna lord in specific varga dignity; checkable=False

# ── Yoga source data ──────────────────────────────────────────────────────────

YOGA_DATA: list[dict] = [

    # ── 1. SUBHA YOGA (verses 1-2) ────────────────────────────────────────────
    {
        "yoga_name":    "Subha Yoga",
        "sloka":        "ch36-subha-yoga",
        "group":        "benefic_malefic",
        "formation":    (
            "A natural benefic (Jupiter, Venus, Mercury, waxing Moon) occupies "
            "the ascendant (1st house); OR benefics occupy both the 2nd and the "
            "12th houses simultaneously. The stronger form is when benefics occupy "
            "all three houses (12th, 1st, and 2nd)."
        ),
        "effect":       (
            "One born in Subha yoga will be eloquent, charming, and virtuous. "
            "This yoga confers physical beauty, excellent virtues, eloquent "
            "disposition, a happy life, health, wealth, longevity, and fame."
        ),
        "is_benefic":   True,
        "life_domains": ["character", "happiness", "wealth", "fame"],
        "yoga_check": {
            "type":        "benefics_in_houses",
            "checkable":   True,
            "description": (
                "Natural benefics (Jupiter, Venus, Mercury, waxing Moon) in the 1st house; "
                "OR in both the 2nd and 12th houses. Superior form: benefics in all three "
                "(12th, 1st, and 2nd). Benefic must be free from debilitation and combustion "
                "for full effects. Planetary dignity and strength modify the results."
            ),
            "houses":       [1, 2, 12],
            "planet_type":  "benefic",
            "operator":     "or",
        },
    },

    # ── 2. ASUBHA YOGA (verses 1-2) ───────────────────────────────────────────
    {
        "yoga_name":    "Asubha Yoga",
        "sloka":        "ch36-asubha-yoga",
        "group":        "benefic_malefic",
        "formation":    (
            "A natural malefic (Sun, Mars, Saturn, Rahu, Ketu, waning Moon) "
            "occupies the ascendant; OR malefics occupy both the 12th and 2nd "
            "houses simultaneously. Increasingly malefic with more malefics in "
            "these positions."
        ),
        "effect":       (
            "One born in Asubha yoga will be sensuous, will do sinful acts, and "
            "will enjoy or appropriate others' wealth. Two or three malefics in "
            "such positions produce most unfavourable results, adversely affecting "
            "health and longevity."
        ),
        "is_benefic":   False,
        "life_domains": ["character", "health", "hardship"],
        "yoga_check": {
            "type":        "malefics_in_houses",
            "checkable":   True,
            "description": (
                "Natural malefics (Sun, Mars, Saturn, Rahu, Ketu) in the 1st house; "
                "OR in both the 12th and 2nd houses. More malefics in these positions "
                "intensify adverse results. Can be nullified by compensating benefic factors."
            ),
            "houses":       [1, 2, 12],
            "planet_type":  "malefic",
            "operator":     "or",
        },
    },

    # ── 3. GAJAKESARI YOGA (verses 3-4) ──────────────────────────────────────
    {
        "yoga_name":    "Gajakesari Yoga",
        "sloka":        "ch36-gajakesari-yoga",
        "group":        "raja_yoga",
        "formation":    (
            "Jupiter is in an angular house (1st, 4th, 7th, or 10th) from the "
            "ascendant or from the Moon, AND is conjunct or aspected by another "
            "natural benefic. Jupiter must be free from debilitation, combustion, "
            "and placement in an inimical sign."
        ),
        "effect":       (
            "One born in Gaja Kesari yoga will be splendorous, wealthy, and "
            "intelligent, endowed with many laudable virtues, and will please the "
            "king. The yoga gives wealth, fame, intelligence, and longevity, with "
            "full effects manifesting in the Dasa periods of Jupiter, Moon, and "
            "planets related to them."
        ),
        "is_benefic":   True,
        "life_domains": ["wealth", "fame", "intelligence", "royalty"],
        "yoga_check": {
            "type":        "planet_in_kendra_from",
            "checkable":   True,
            "description": (
                "Jupiter must be in an angular house (1, 4, 7, 10) counted from the "
                "ascendant OR from the Moon's position. Additionally, Jupiter must be "
                "conjunct or receive an aspect from another natural benefic (Venus, "
                "Mercury, or waxing Moon). Jupiter must be free from debilitation "
                "(Capricorn), combustion (within 11° of Sun), and inimical signs."
            ),
            "planet":       "Jupiter",
            "reference":    ["ascendant", "Moon"],
            "houses":        [1, 4, 7, 10],
            "conditions":   ["aspected_by_benefic", "free_from_debilitation", "free_from_combustion"],
        },
    },

    # ── 4. HAMSA YOGA (verses 3-4 notes) ────────────────────────────────────
    {
        "yoga_name":    "Hamsa Yoga",
        "sloka":        "ch36-hamsa-yoga",
        "group":        "raja_yoga",
        "formation":    (
            "Jupiter occupies its exaltation sign (Cancer) AND is placed in an "
            "angular house (1st, 4th, 7th, or 10th) counted from the Moon. This "
            "is a specific form of the Pancha Mahapurusha yoga, distinguished from "
            "the broader Gajakesari formation by the requirement of Jupiter's "
            "exaltation. Jupiter must be free from combustion."
        ),
        "effect":       (
            "One born in Hamsa yoga will be splendorous, wealthy, and intelligent, "
            "endowed with many laudable virtues. As a Pancha Mahapurusha yoga it "
            "confers the highest order of Jupiter's blessings — learning, "
            "spirituality, prosperity, physical grace, and honour from kings and "
            "society."
        ),
        "is_benefic":   True,
        "life_domains": ["wealth", "scholarship", "fame", "royalty", "spirituality"],
        "yoga_check": {
            "type":        "planet_in_kendra_from",
            "checkable":   True,
            "description": (
                "Jupiter must be in Cancer (its exaltation sign) AND in an angular "
                "house (1, 4, 7, or 10) counted from the Moon's sign position. "
                "Jupiter must be free from combustion. Distinguished from ordinary "
                "Gajakesari by requiring exaltation rather than merely kendra "
                "placement from Moon."
            ),
            "planet":       "Jupiter",
            "sign":         "Cancer",
            "reference":    "Moon",
            "houses":       [1, 4, 7, 10],
            "conditions":   ["exalted_sign", "free_from_combustion"],
        },
    },

    # ── 5. AMALA YOGA (verses 5-6) ───────────────────────────────────────────
    {
        "yoga_name":    "Amala Yoga",
        "sloka":        "ch36-amala-yoga",
        "group":        "benefic_yoga",
        "formation":    (
            "Exclusively a natural benefic (Jupiter, Venus, or Mercury) occupies "
            "the 10th house from the ascendant OR the 10th from the Moon. No malefic "
            "must be present in the same 10th house — any malefic co-occupation "
            "voids the yoga."
        ),
        "effect":       (
            "Amala yoga confers fame lasting till the moon and stars exist. The "
            "native will be honoured by the king, enjoy abundant pleasures, be "
            "charitable, fond of relatives, helpful to others, pious and virtuous. "
            "It is primarily a yoga of lasting name and fame rather than wealth."
        ),
        "is_benefic":   True,
        "life_domains": ["fame", "career", "character", "spirituality"],
        "yoga_check": {
            "type":        "benefic_only_in_house",
            "checkable":   True,
            "description": (
                "A natural benefic (Jupiter, Venus, Mercury) must occupy the 10th "
                "house from the ascendant OR from the Moon. The 10th must have no "
                "malefic planet. A single malefic in the 10th nullifies the yoga entirely."
            ),
            "house":        10,
            "reference":    ["ascendant", "Moon"],
            "planet_type":  "benefic",
            "no_malefic":   True,
        },
    },

    # ── 6. PARVATA YOGA (verses 7-8) ─────────────────────────────────────────
    {
        "yoga_name":    "Parvata Yoga",
        "sloka":        "ch36-parvata-yoga",
        "group":        "raja_yoga",
        "formation":    (
            "Benefics occupy the angular houses (1st, 4th, 7th, 10th) while the "
            "7th and 8th houses are either vacant or occupied only by benefics. "
            "Alternative version: lords of the ascendant and 12th are in mutual "
            "angular positions aspected by friendly planets."
        ),
        "effect":       (
            "One born in Parvatha yoga will be wealthy, eloquent, charitable, "
            "learned in Sastras, fond of mirth, famous, splendorous, and be the "
            "leader of a city. The yoga matures during the Dasa periods of the "
            "benefics placed in the angles."
        ),
        "is_benefic":   True,
        "life_domains": ["wealth", "fame", "scholarship", "leadership"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Primary condition: natural benefics in angular houses (1, 4, 7, 10) "
                "AND houses 7 and 8 must be unoccupied or occupied by benefics only. "
                "Multiple classical variants exist across Parasara, Jataka Parijata, "
                "and Phala Deepika. Phase 2: implement primary form as compound check."
            ),
        },
    },

    # ── 7. KAHALA YOGA (verses 9-10) ─────────────────────────────────────────
    {
        "yoga_name":    "Kahala Yoga",
        "sloka":        "ch36-kahala-yoga",
        "group":        "raja_yoga",
        "formation":    (
            "The 4th lord and Jupiter are in mutual angular positions while the "
            "ascendant lord is strong. Alternatively, the 4th lord is in his own "
            "or exaltation sign and is conjunct the 10th lord."
        ),
        "effect":       (
            "The native will be energetic, adventurous, cunning, endowed with a "
            "complete army consisting of chariots, elephants, horses, and infantry, "
            "and will lord over a few villages."
        ),
        "is_benefic":   True,
        "life_domains": ["power", "fame", "career", "leadership"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Condition 1: 4th lord and Jupiter in mutual kendra positions + "
                "strong ascendant lord. Condition 2 (OR): 4th lord in own/exaltation "
                "sign conjunct 10th lord. Requires lord-position computation and "
                "strength assessment. Phase 2 implementation needed."
            ),
        },
    },

    # ── 8. CHAMARA YOGA (verses 11-12) ───────────────────────────────────────
    {
        "yoga_name":    "Chamara Yoga",
        "sloka":        "ch36-chamara-yoga",
        "group":        "raja_yoga",
        "formation":    (
            "The ascendant lord is exalted in an angular house (1st, 4th, 7th, "
            "or 10th) and is aspected by Jupiter. Alternatively, two or more "
            "natural benefics are placed in the ascendant, 9th, 10th, or 7th house."
        ),
        "effect":       (
            "The native will be a king or be honoured by the king, long-lived, "
            "scholarly, eloquent, and versed in all arts. This yoga gives long "
            "life, prospering like the increasing Moon, fame, virtue, and leadership."
        ),
        "is_benefic":   True,
        "life_domains": ["royalty", "scholarship", "fame", "longevity"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Condition 1: ascendant lord exalted in angular house + aspected by "
                "Jupiter. Condition 2 (OR): 2+ natural benefics in houses 1, 7, 9, "
                "or 10. Requires ascendant lord identification and exaltation check. "
                "Phase 2 implementation."
            ),
        },
    },

    # ── 9. SANKHA YOGA (verses 13-14) ────────────────────────────────────────
    {
        "yoga_name":    "Sankha Yoga",
        "sloka":        "ch36-sankha-yoga",
        "group":        "raja_yoga",
        "formation":    (
            "The ascendant lord is strong while the lords of the 5th and 6th "
            "are in mutual angular positions. Alternatively, the ascendant lord "
            "together with the 10th lord is in a movable sign while the 9th lord "
            "is strong."
        ),
        "effect":       (
            "One born with Sankha yoga will be endowed with wealth, spouse and "
            "sons, be kindly disposed, propitious, intelligent, meritorious and "
            "long-lived."
        ),
        "is_benefic":   True,
        "life_domains": ["wealth", "family", "longevity", "character"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Condition 1: strong ascendant lord + lords of 5th and 6th in "
                "mutual kendra positions. Condition 2 (OR): ascendant lord + 10th "
                "lord in movable sign + strong 9th lord. Requires multiple lord "
                "positions and strength assessment."
            ),
        },
    },

    # ── 10. BHERI YOGA (verses 15-16) ─────────────────────────────────────────
    {
        "yoga_name":    "Bheri Yoga",
        "sloka":        "ch36-bheri-yoga",
        "group":        "raja_yoga",
        "formation":    (
            "The 12th, ascendant, 2nd, and 7th houses are all occupied by planets "
            "while the 9th lord is strong. Alternatively, Venus, Jupiter, and the "
            "ascendant lord are all in an angular house while the 9th lord is strong."
        ),
        "effect":       (
            "The native will be endowed with wealth, wife and sons, be a king, "
            "be famous, virtuous, and endowed with good behaviour, happiness and "
            "pleasures."
        ),
        "is_benefic":   True,
        "life_domains": ["wealth", "royalty", "fame", "family"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Condition 1: planets in all four of houses 12, 1, 2, and 7 + "
                "strong 9th lord. Condition 2 (OR): Venus + Jupiter + ascendant "
                "lord all in angular houses + strong 9th lord. Requires lord "
                "position and strength assessment."
            ),
        },
    },

    # ── 11. MRIDANGA YOGA (verse 17) ─────────────────────────────────────────
    {
        "yoga_name":    "Mridanga Yoga",
        "sloka":        "ch36-mridanga-yoga",
        "group":        "raja_yoga",
        "formation":    (
            "The ascendant lord is strong while the remaining planets occupy "
            "angular houses (1, 4, 7, 10), trine houses (1, 5, 9), their own "
            "signs, or signs of exaltation."
        ),
        "effect":       (
            "The native concerned will be a king or equal to a king, and be happy."
        ),
        "is_benefic":   True,
        "life_domains": ["royalty", "happiness", "power"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Strong ascendant lord required. Remaining planets (excluding ascendant "
                "lord) must be in angular houses, trine houses, own signs, or exaltation "
                "signs. Requires strength assessment and dignity checks across all planets."
            ),
        },
    },

    # ── 12. SRINATHA YOGA (verse 18) ─────────────────────────────────────────
    {
        "yoga_name":    "Srinatha Yoga",
        "sloka":        "ch36-srinatha-yoga",
        "group":        "raja_yoga",
        "formation":    (
            "The 7th lord is placed in the 10th house while the 10th lord is "
            "exalted and is in the company of (conjunct) the 9th lord. "
            "For Sagittarius ascendant, this forms simply when Sun and Mercury "
            "are in the 10th house in Virgo (with Mercury in the first half of Virgo)."
        ),
        "effect":       (
            "The native with this yoga will be equal to lord Devendra (the supreme "
            "god), indicating the highest order of royal status, power, fame, "
            "and divine favour."
        ),
        "is_benefic":   True,
        "life_domains": ["royalty", "fame", "power", "spirituality"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "7th lord must be in the 10th house + 10th lord exalted + 10th lord "
                "conjunct 9th lord. Requires identifying house lords for the specific "
                "ascendant and verifying exaltation and conjunction. "
                "Sagittarius-specific shortcut: Sun + Mercury in 10th in Virgo."
            ),
        },
    },

    # ── 13. SARADA YOGA (verses 19-20) ───────────────────────────────────────
    {
        "yoga_name":    "Sarada Yoga",
        "sloka":        "ch36-sarada-yoga",
        "group":        "raja_yoga",
        "formation":    (
            "The 10th lord is in the 5th house while Mercury is in an angular "
            "house and the Sun with strength is in Leo. Alternatively, Jupiter "
            "or Mercury is in a trine (1st, 5th, or 9th) to the Moon while "
            "Mars is in the 11th house."
        ),
        "effect":       (
            "One born in either kind of Sarada yoga will obtain wealth, spouse "
            "and sons, be happy, scholarly, dear to king, pious and virtuous."
        ),
        "is_benefic":   True,
        "life_domains": ["scholarship", "wealth", "royalty", "family"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Condition 1: 10th lord in 5th + Mercury in angular house + Sun "
                "strong in Leo (Leo must be the Sun's actual sign position). "
                "Condition 2 (OR): Jupiter or Mercury in trine to Moon + Mars in "
                "11th house. Requires lord positions, sign identification, and "
                "trine computation from Moon."
            ),
        },
    },

    # ── 14. MATSYA YOGA (verses 21-22) ───────────────────────────────────────
    {
        "yoga_name":    "Matsya Yoga",
        "sloka":        "ch36-matsya-yoga",
        "group":        "raja_yoga",
        "formation":    (
            "Natural benefics occupy the 9th and 1st houses, mixed planets (both "
            "benefics and malefics) are in the 5th house, and malefics occupy "
            "the 4th and 8th houses."
        ),
        "effect":       (
            "The native will be an astrologer, be a synonym of kindness, be "
            "virtuous, strong, beautiful, famous, learned and pious."
        ),
        "is_benefic":   True,
        "life_domains": ["scholarship", "astrology", "fame", "character"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   True,
            "description": (
                "Three simultaneous house requirements: (1) natural benefics in "
                "houses 9 and 1; (2) mixed planets (at least one benefic AND one "
                "malefic) in house 5; (3) malefics in houses 4 and 8. All three "
                "conditions must hold simultaneously."
            ),
            "house_requirements": [
                {"houses": [1, 9], "planet_type": "benefic"},
                {"houses": [5],    "planet_type": "mixed"},
                {"houses": [4, 8], "planet_type": "malefic"},
            ],
        },
    },

    # ── 15. KOORMA YOGA (verses 23-24) ───────────────────────────────────────
    {
        "yoga_name":    "Koorma Yoga",
        "sloka":        "ch36-koorma-yoga",
        "group":        "raja_yoga",
        "formation":    (
            "The 5th, 6th, and 7th houses are occupied by benefic planets in "
            "their own, exaltation, or friendly signs; while malefics occupy the "
            "3rd, 11th, and 1st houses in their own signs or exaltation."
        ),
        "effect":       (
            "The native will be a king, be courageous, virtuous, famous, helpful, "
            "happy and be leader of men."
        ),
        "is_benefic":   True,
        "life_domains": ["royalty", "fame", "character", "leadership"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Benefics in houses 5, 6, and 7 in own/exaltation/friendly signs + "
                "malefics in houses 3, 11, and 1 in own/exaltation signs. "
                "Dignity requirement (friendly/own/exaltation) makes this complex. "
                "Phase 2 implementation."
            ),
        },
    },

    # ── 16. KHADGA YOGA (verses 25-26) ───────────────────────────────────────
    {
        "yoga_name":    "Khadga Yoga",
        "sloka":        "ch36-khadga-yoga",
        "group":        "raja_yoga",
        "formation":    (
            "The lords of the 2nd and 9th houses exchange signs (parivartana — "
            "each is placed in the other's sign) while the ascendant lord is in "
            "an angular house (1, 4, 7, 10) or a trine house (1, 5, 9)."
        ),
        "effect":       (
            "One with Khadga yoga will be endowed with wealth, fortunes and "
            "happiness, be learned in Sastras, be intelligent, mighty, grateful "
            "and skilful."
        ),
        "is_benefic":   True,
        "life_domains": ["wealth", "scholarship", "happiness", "character"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Parivartana (sign exchange) between lords of houses 2 and 9 + "
                "ascendant lord in angular or trine house. Requires identifying "
                "house lords and checking mutual sign placement. Phase 2 implementation."
            ),
        },
    },

    # ── 17. LAKSHMI YOGA (verses 27-28) ──────────────────────────────────────
    {
        "yoga_name":    "Lakshmi Yoga",
        "sloka":        "ch36-lakshmi-yoga",
        "group":        "raja_yoga",
        "formation":    (
            "The 9th lord is in an angular house (1, 4, 7, or 10) in his "
            "Moolatrikona sign, own sign, or sign of exaltation; while the "
            "ascendant lord is endowed with strength."
        ),
        "effect":       (
            "The native with this yoga will be charming, virtuous, kingly in "
            "status, endowed with many sons and abundant wealth, be famous and "
            "be of high moral merits."
        ),
        "is_benefic":   True,
        "life_domains": ["wealth", "royalty", "fame", "family"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "9th lord in angular house (1, 4, 7, 10) in own/moolatrikona/"
                "exaltation sign + strong ascendant lord. Requires computing 9th "
                "lord's sign placement and dignity check. Phase 2 implementation."
            ),
        },
    },

    # ── 18. KUSUMA YOGA (verses 29-30) ───────────────────────────────────────
    {
        "yoga_name":    "Kusuma Yoga",
        "sloka":        "ch36-kusuma-yoga",
        "group":        "raja_yoga",
        "formation":    (
            "For a native born with a fixed sign (Taurus, Leo, Scorpio, or "
            "Aquarius) ascending: Venus is in an angular house, the Moon is in "
            "a trine house (1, 5, or 9) conjunct or aspected by a benefic, "
            "and Saturn is in the 10th house."
        ),
        "effect":       (
            "Such a native will be a king or equal to him, be charitable, will "
            "enjoy pleasures, be happy, prime among his race men, virtuous "
            "and red-lettered."
        ),
        "is_benefic":   True,
        "life_domains": ["royalty", "wealth", "happiness", "character"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Ascendant must be a fixed sign (Taurus=2, Leo=5, Scorpio=8, "
                "Aquarius=11) + Venus in angular house + Moon in trine with benefic "
                "aspect/conjunction + Saturn in 10th house. Compound multi-planet "
                "check with ascendant sign precondition."
            ),
        },
    },

    # ── 19. KALANIDHI YOGA (verses 31-32) ────────────────────────────────────
    {
        "yoga_name":    "Kalanidhi Yoga",
        "sloka":        "ch36-kalanidhi-yoga",
        "group":        "raja_yoga",
        "formation":    (
            "Jupiter is placed in the 2nd or the 5th house and receives the "
            "aspects of both Mercury and Venus."
        ),
        "effect":       (
            "The native will be virtuous, honoured by kings, bereft of diseases, "
            "be happy, wealthy and learned."
        ),
        "is_benefic":   True,
        "life_domains": ["scholarship", "wealth", "health", "royalty"],
        "yoga_check": {
            "type":        "planet_in_house",
            "checkable":   True,
            "description": (
                "Jupiter in house 2 or house 5 AND aspected by Mercury (by Vedic "
                "full aspect: 7th-house aspect, or other applicable aspects) AND "
                "aspected by Venus. All three conditions must hold simultaneously."
            ),
            "planet":       "Jupiter",
            "houses":        [2, 5],
            "aspected_by":   ["Mercury", "Venus"],
        },
    },

    # ── 20. KALPADRUMA YOGA / PARIJATA YOGA (verses 33-34) ───────────────────
    {
        "yoga_name":    "Kalpadruma Yoga",
        "sloka":        "ch36-kalpadruma-yoga",
        "group":        "raja_yoga",
        "formation":    (
            "Four planets form a chain of dispositors: (a) the ascendant lord, "
            "(b) the dispositor of (a), (c) the dispositor of (b), (d) the "
            "Navamsa dispositor of (c). ALL four of these planets must be placed "
            "in angular or trine houses from the ascendant, OR be exalted. "
            "Also known as Parijata Yoga."
        ),
        "effect":       (
            "One with this yoga will be endowed with all kinds of wealth, be a "
            "king, pious, strong, fond of war and merciful. This yoga grants any "
            "boon to the possessor, equivalent to divine status (Devendra)."
        ),
        "is_benefic":   True,
        "life_domains": ["wealth", "royalty", "spirituality", "power"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Four-step dispositor chain from ascendant lord (Rasi + Navamsa). "
                "All four chain planets must be in angular/trine houses or exalted. "
                "Requires full divisional chart computation. Phase 2 implementation."
            ),
        },
    },

    # ── 21. HARI YOGA (verses 35-36 — Trimurthi group) ───────────────────────
    {
        "yoga_name":    "Hari Yoga",
        "sloka":        "ch36-hari-yoga",
        "group":        "trimurthi",
        "formation":    (
            "Counted from the position of the 2nd lord: natural benefics "
            "(Jupiter, Venus, Mercury, or waxing Moon) individually occupy the "
            "2nd, 12th, and 8th positions from the 2nd lord's placement. "
            "One of the three Trimurthi yogas (representing Lord Vishnu)."
        ),
        "effect":       (
            "One born in Hari yoga will be happy, learned and endowed with wealth "
            "and sons."
        ),
        "is_benefic":   True,
        "life_domains": ["happiness", "scholarship", "wealth", "family"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Identify the 2nd lord and its placement. From that position, houses "
                "2, 12, and 8 must each be individually occupied by a natural benefic "
                "(Jupiter, Venus, Mercury; waxing Moon included, Sun excluded). "
                "Waning Moon is also excluded. Phase 2 implementation."
            ),
        },
    },

    # ── 22. HARA YOGA (verses 35-36 — Trimurthi group) ───────────────────────
    {
        "yoga_name":    "Hara Yoga",
        "sloka":        "ch36-hara-yoga",
        "group":        "trimurthi",
        "formation":    (
            "Counted from the sign occupied by the 7th lord: natural benefics "
            "individually occupy the 4th, 9th, and 8th positions from the 7th "
            "lord's placement. One of the three Trimurthi yogas (representing "
            "Lord Shiva)."
        ),
        "effect":       (
            "One born in Hara yoga will be happy, learned and endowed with wealth "
            "and sons."
        ),
        "is_benefic":   True,
        "life_domains": ["happiness", "scholarship", "wealth", "family"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Identify the 7th lord and its sign placement. From that sign, "
                "positions 4, 9, and 8 must each be occupied by a natural benefic. "
                "Sun and waning Moon excluded. Phase 2 implementation."
            ),
        },
    },

    # ── 23. BRAHMA YOGA (verses 35-36 — Trimurthi group) ─────────────────────
    {
        "yoga_name":    "Brahma Yoga",
        "sloka":        "ch36-brahma-yoga",
        "group":        "trimurthi",
        "formation":    (
            "Counted from the sign occupied by the ascendant lord: natural "
            "benefics individually occupy the 4th, 10th, and 11th positions from "
            "the ascendant lord's placement. One of the three Trimurthi yogas "
            "(representing Lord Brahma)."
        ),
        "effect":       (
            "One born in Brahma yoga will be happy, learned and endowed with "
            "wealth and sons."
        ),
        "is_benefic":   True,
        "life_domains": ["happiness", "scholarship", "wealth", "family"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Identify the ascendant lord and its sign placement. From that "
                "sign, positions 4, 10, and 11 must each be occupied by a natural "
                "benefic. Sun and waning Moon excluded. Phase 2 implementation."
            ),
        },
    },

    # ── 24. LAGNADHI YOGA (verse 37) ──────────────────────────────────────────
    {
        "yoga_name":    "Lagnadhi Yoga",
        "sloka":        "ch36-lagnadhi-yoga",
        "group":        "benefic_yoga",
        "formation":    (
            "Natural benefics (Jupiter, Venus, Mercury) occupy the 7th and 8th "
            "houses from the ascendant, devoid of conjunction or aspect of any "
            "malefic planet. Note: This is the Lagna-based version (Chandradhi "
            "yoga applies the same rule from the Moon, adding the 6th house)."
        ),
        "effect":       (
            "The native will be a great person, learned in Sastras and happy. "
            "When the three benefics (Mercury in 6th, Jupiter in 7th, Venus in "
            "8th) are optimally placed, the native will be highly learned, wealthy, "
            "and among the most supreme men on earth."
        ),
        "is_benefic":   True,
        "life_domains": ["scholarship", "happiness", "wealth"],
        "yoga_check": {
            "type":        "benefics_in_houses",
            "checkable":   True,
            "description": (
                "Natural benefics (Jupiter, Venus, Mercury) must occupy the 7th "
                "and/or 8th houses from the ascendant. No malefic may conjoin or "
                "aspect these benefics. Optimal form: Mercury in 6th, Jupiter in "
                "7th, Venus in 8th. The 4th house should be unoccupied per some "
                "versions. Best effects: all three benefics placed, free from "
                "combustion and debilitation."
            ),
            "houses":       [7, 8],
            "planet_type":  "benefic",
            "no_malefic_aspect": True,
        },
    },

    # ── 25. CHANDRADHI YOGA (verse 37 notes) ─────────────────────────────────
    {
        "yoga_name":    "Chandradhi Yoga",
        "sloka":        "ch36-chandradhi-yoga",
        "group":        "benefic_yoga",
        "formation":    (
            "Natural benefics (Jupiter, Venus, Mercury) occupy the 6th, 7th, and/or "
            "8th houses counted from the Moon, devoid of malefic conjunction or "
            "aspect. This is the Moon-based counterpart to Lagnadhi Yoga (which "
            "counts from the ascendant). The key distinction is the inclusion of "
            "the 6th house from the Moon. Optimal form: Mercury in 6th, Jupiter "
            "in 7th, Venus in 8th from the Moon. The 4th from the Moon should be "
            "unoccupied. Benefics must be free from combustion and debilitation."
        ),
        "effect":       (
            "The native will be highly learned, wealthy, and among the most supreme "
            "men on earth. The yoga confers greatness, scholarship, prosperity, and "
            "exalted social standing. Effects are strongest when all three benefics "
            "(Mercury, Jupiter, Venus) are optimally placed in the 6th, 7th, and "
            "8th from the Moon."
        ),
        "is_benefic":   True,
        "life_domains": ["scholarship", "wealth", "fame", "happiness"],
        "yoga_check": {
            "type":        "benefics_in_houses",
            "checkable":   True,
            "description": (
                "Natural benefics (Jupiter, Venus, Mercury) must occupy the 6th, "
                "7th, and/or 8th houses counted from the Moon's sign. No malefic "
                "may conjoin or aspect the benefics in these positions. Optimal: "
                "Mercury in 6th, Jupiter in 7th, Venus in 8th from Moon. 4th from "
                "Moon should be vacant. Benefics must be free from combustion and "
                "debilitation. Reference point: Moon (not ascendant)."
            ),
            "houses":            [6, 7, 8],
            "reference":         "Moon",
            "planet_type":       "benefic",
            "no_malefic_aspect": True,
        },
    },
]

# ── Divisional dignity rules (verses 38-39) ───────────────────────────────────
# Each Varga dignity of the ascendant lord gives specific effects.

DIVISIONAL_DIGNITY_DATA: list[dict] = [
    {
        "dignity_name": "Parijathamsa",
        "rank":         1,
        "effect":       "The ascendant lord in Parijathamsa (a specific Varga dignity level) will make the native happy.",
        "life_domains": ["happiness"],
    },
    {
        "dignity_name": "Vargothama",
        "rank":         2,
        "effect":       (
            "The ascendant lord in Vargothama (occupying the same sign in both "
            "the Rasi and Navamsa charts) makes the native immune to diseases and "
            "grants excellent health and constitution."
        ),
        "life_domains": ["health", "longevity"],
    },
    {
        "dignity_name": "Gopuramsa",
        "rank":         3,
        "effect":       "The ascendant lord in Gopuramsa makes the native rich with wealth and grains.",
        "life_domains": ["wealth"],
    },
    {
        "dignity_name": "Sinhasanamsa",
        "rank":         4,
        "effect":       "The ascendant lord in Sinhasanamsa (throne dignity) makes the native a king.",
        "life_domains": ["royalty", "power"],
    },
    {
        "dignity_name": "Paravathamsa",
        "rank":         5,
        "effect":       "The ascendant lord in Paravathamsa makes the native a scholar.",
        "life_domains": ["scholarship"],
    },
    {
        "dignity_name": "Devalokamsa",
        "rank":         6,
        "effect":       "The ascendant lord in Devalokamsa makes the native opulent and endowed with conveyances.",
        "life_domains": ["wealth", "comforts"],
    },
    {
        "dignity_name": "Iravathramsa",
        "rank":         7,
        "effect":       "The ascendant lord in Iravathramsa makes the native famous and honoured by kings.",
        "life_domains": ["fame", "royalty"],
    },
]

# ── Group labels ──────────────────────────────────────────────────────────────

GROUP_LABEL: dict[str, str] = {
    "benefic_malefic": "Benefic/Malefic Yogas",
    "raja_yoga":       "Raja Yoga",
    "benefic_yoga":    "Benefic Yoga",
    "trimurthi":       "Trimurthi Yoga",
    "divisional":      "Divisional Dignity",
}

# ── build_rule ────────────────────────────────────────────────────────────────

def build_yoga_rule(yoga: dict, index: int) -> dict:
    rule_id   = f"bphs-ch36-{index:03d}"
    group     = yoga["group"]
    group_lbl = GROUP_LABEL.get(group, group)
    yoga_name = yoga["yoga_name"]
    is_ben    = yoga["is_benefic"]
    formation = yoga["formation"]
    effect    = yoga["effect"]
    domains   = yoga["life_domains"]
    yc        = yoga["yoga_check"]
    sloka     = yoga.get("sloka", f"ch36-{yoga_name.lower().replace(' ', '-')}")

    detailed = (
        f"Yoga: {yoga_name} [{group_lbl}]\n\n"
        f"Formation: {formation}\n\n"
        f"Effect: {effect}"
    )
    summary = f"{yoga_name} — {effect}"
    if len(summary) > 200:
        summary = summary[:197] + "..."

    tags = [
        "verbatim", "yoga", f"chapter{CHAPTER}",
        "yoga_combination", "yoga_formation",
        f"group:bphs-ch36-{group}",
        "benefic" if is_ben else "malefic",
    ]
    if yc.get("checkable"):
        tags.append("yoga_checkable")

    return {
        "rule_id":    rule_id,
        "science_id": SCIENCE,
        "source": {
            "book":           BOOK,
            "book_id":        BOOK_ID,
            "chapter":        CHAPTER,
            "chapter_name":   CHAP_NAME,
            "sloka":          sloka,
            "batch_id":       BATCH_ID,
            "primary":        BOOK,
            "page_ref":       None,
            "passage_ref_id": None,
        },
        "condition": {
            "type":               "yoga_combination",
            "sub_type":           "yoga_formation",
            "yoga_name":          yoga_name,
            "yoga_group":         group,
            "yoga_group_label":   group_lbl,
            "planets_involved":   [],
            "houses_involved":    yc.get("houses", []),
            "sub_conditions":     [],
            "operator":           "and",
            "gender_context":     "neutral",
            "condition_group_id": f"bphs-ch36-{group}",
            "is_group_summary":   False,
            "is_benefic":         is_ben,
            "yoga_check":         yc,
        },
        "interpretation": {
            "summary":            summary,
            "detailed":           detailed,
            "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
            "remedies":           [],
            "life_domain":        domains[0] if domains else "general",
            "life_domains":       domains,
            "tags":               tags,
            "physical_markers":   [],
        },
        "metadata": {
            "planets_involved":     [],
            "houses_involved":      yc.get("houses", []),
            "signs_involved":       [],
            "condition_count":      1,
            "gender_context":       "neutral",
            "condition_group_id":   f"bphs-ch36-{group}",
            "is_group_summary":     False,
            "has_physical_markers": False,
            "physical_categories":  [],
            "yoga_checkable":       bool(yc.get("checkable")),
        },
        "confidence": {
            "source_confidence":  "HIGH",
            "extraction_method":  "hard_coded",
            "validated":          False,
        },
        "approval_status": "pending_review",
        "created_at":      datetime.now(timezone.utc).isoformat(),
    }


def build_divisional_rule(div: dict, index: int) -> dict:
    rule_id    = f"bphs-ch36-{index:03d}"
    dig_name   = div["dignity_name"]
    effect     = div["effect"]
    domains    = div["life_domains"]
    rank       = div["rank"]

    detailed = (
        f"Yoga: Ascendant Lord in {dig_name} [Divisional Dignity — rank {rank}]\n\n"
        f"Formation: The ascendant lord occupies the Varga dignity level "
        f"known as {dig_name}.\n\n"
        f"Effect: {effect}"
    )
    summary = f"Lagna lord in {dig_name} — {effect}"
    if len(summary) > 200:
        summary = summary[:197] + "..."

    tags = [
        "verbatim", "yoga", f"chapter{CHAPTER}",
        "general_principle", "divisional_dignity",
        f"varga:{dig_name.lower()}",
        "group:bphs-ch36-divisional",
        "benefic",
    ]

    yc = {
        "type":        "divisional_dignity",
        "checkable":   False,
        "description": (
            f"Ascendant lord occupies {dig_name} Varga dignity. "
            "Requires full divisional (Varga) chart computation across "
            "multiple divisional charts. Phase 2 implementation."
        ),
        "dignity_name": dig_name,
        "dignity_rank": rank,
    }

    return {
        "rule_id":    rule_id,
        "science_id": SCIENCE,
        "source": {
            "book":           BOOK,
            "book_id":        BOOK_ID,
            "chapter":        CHAPTER,
            "chapter_name":   CHAP_NAME,
            "sloka":          f"ch36-divisional-{dig_name.lower()}",
            "batch_id":       BATCH_ID,
            "primary":        BOOK,
            "page_ref":       None,
            "passage_ref_id": None,
        },
        "condition": {
            "type":               "general_principle",
            "sub_type":           "divisional_dignity",
            "yoga_name":          f"Lagna Lord in {dig_name}",
            "yoga_group":         "divisional",
            "yoga_group_label":   GROUP_LABEL["divisional"],
            "dignity_name":       dig_name,
            "dignity_rank":       rank,
            "planets_involved":   [],
            "houses_involved":    [],
            "sub_conditions":     [],
            "operator":           "and",
            "gender_context":     "neutral",
            "condition_group_id": "bphs-ch36-divisional",
            "is_group_summary":   False,
            "is_benefic":         True,
            "yoga_check":         yc,
        },
        "interpretation": {
            "summary":            summary,
            "detailed":           detailed,
            "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
            "remedies":           [],
            "life_domain":        domains[0] if domains else "general",
            "life_domains":       domains,
            "tags":               tags,
            "physical_markers":   [],
        },
        "metadata": {
            "planets_involved":     [],
            "houses_involved":      [],
            "signs_involved":       [],
            "condition_count":      1,
            "gender_context":       "neutral",
            "condition_group_id":   "bphs-ch36-divisional",
            "is_group_summary":     False,
            "has_physical_markers": False,
            "physical_categories":  [],
            "yoga_checkable":       False,
        },
        "confidence": {
            "source_confidence":  "HIGH",
            "extraction_method":  "hard_coded",
            "validated":          False,
        },
        "approval_status": "pending_review",
        "created_at":      datetime.now(timezone.utc).isoformat(),
    }


# ── MongoDB insert ────────────────────────────────────────────────────────────

def insert_rules_to_mongo(all_rules: list[dict], mongo_url: str, db_name: str) -> None:
    from pymongo import MongoClient
    client = MongoClient(mongo_url)
    col    = client[db_name]["interpretation_rules"]
    existing = col.count_documents({"source.batch_id": BATCH_ID})
    if existing:
        print(f"\n⚠  Batch '{BATCH_ID}' already has {existing} rules in MongoDB.")
        print("   Nothing inserted. Drop the batch first if you want to re-ingest.")
        client.close()
        return
    result = col.insert_many(all_rules, ordered=False)
    print(f"\n✅  Inserted {len(result.inserted_ids)} rules into MongoDB")
    print(f"   batch_id : {BATCH_ID}")
    client.close()


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest BPHS Ch 36 Many Other Yogas into Knowledge Engine"
    )
    parser.add_argument("--mongo-url", default=None)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--dry-run",   action="store_true")
    parser.add_argument("--save",      default=None, metavar="FILE")
    parser.add_argument("--upload",    default=None, metavar="FILE")
    args = parser.parse_args()

    # ── --upload path ──────────────────────────────────────────────────────────
    if args.upload:
        if not args.mongo_url:
            print("⚠  --upload requires --mongo-url"); sys.exit(1)
        p = Path(args.upload)
        if not p.exists():
            print(f"⚠  File not found: {args.upload}"); sys.exit(1)
        with open(p, encoding="utf-8") as fh:
            all_rules = json.load(fh)
        print(f"\n✅  Loaded {len(all_rules)} rules from {args.upload}")
        insert_rules_to_mongo(all_rules, args.mongo_url, args.db_name)
        print(f"\n   Validate with:")
        print(f"   python3 scripts/validate_rules.py --mongo-url $MONGO_URL \\")
        print(f"     --db-name {args.db_name} --batch-id {BATCH_ID}")
        return

    # ── Build rules ────────────────────────────────────────────────────────────
    all_rules: list[dict] = []
    idx = 1
    for yoga in YOGA_DATA:
        all_rules.append(build_yoga_rule(yoga, idx)); idx += 1
    for div in DIVISIONAL_DIGNITY_DATA:
        all_rules.append(build_divisional_rule(div, idx)); idx += 1

    total     = len(all_rules)
    benefic   = sum(1 for r in all_rules if r["condition"]["is_benefic"])
    adverse   = total - benefic
    checkable = sum(1 for r in all_rules if r["metadata"]["yoga_checkable"])

    # Group breakdown
    groups: dict[str, int] = {}
    for r in all_rules:
        g = r["condition"].get("yoga_group", "other")
        groups[g] = groups.get(g, 0) + 1

    print(f"\n{'─' * 65}")
    print(f"BPHS Chapter {CHAPTER} — {CHAP_NAME}  [v1 hard-coded]")
    print(f"batch_id : {BATCH_ID}")
    print(f"{'─' * 65}")
    print(f"\nGroup breakdown:")
    for g, cnt in groups.items():
        print(f"  {GROUP_LABEL.get(g, g):<28} : {cnt}")
    print(f"  {'─' * 35}")
    print(f"  {'TOTAL':<28} : {total}")
    print(f"\nBenefic rules  : {benefic}")
    print(f"Adverse rules  : {adverse}")
    print(f"Yoga-checkable : {checkable} / {total}")

    print(f"\nSample rules (first 3):")
    print(f"{'─' * 65}")
    for rule in all_rules[:3]:
        c  = rule["condition"]
        yc = c.get("yoga_check", {})
        print(f"  rule_id   : {rule['rule_id']}")
        print(f"  yoga      : {c.get('yoga_name','?')}  [{c.get('yoga_group_label','?')}]")
        print(f"  check_type: {yc.get('type','?')}  checkable={yc.get('checkable','?')}")
        print(f"  is_benefic: {c['is_benefic']}")
        print(f"  summary   : {rule['interpretation']['summary'][:90]}...")
        print()

    print(f"Isolation: approval_status='pending_review' — zero rules reach live users")

    if args.dry_run:
        if args.save:
            sp = Path(args.save)
            with open(sp, "w", encoding="utf-8") as fh:
                json.dump(all_rules, fh, indent=2, default=str)
            print(f"\n✅  Rules saved to {args.save}  ({total} rules)")
            print(f"   Review the file, then upload with:")
            print(f"   python3 scripts/ingest_bphs_ch36_v1.py \\")
            print(f"     --upload {args.save} --mongo-url $MONGO_URL --db-name {args.db_name}")
        return

    if not args.mongo_url:
        print("\n⚠  Live run requires --mongo-url  (or use --dry-run / --upload)")
        sys.exit(1)

    if args.save:
        sp = Path(args.save)
        with open(sp, "w", encoding="utf-8") as fh:
            json.dump(all_rules, fh, indent=2, default=str)
        print(f"\n✅  Rules saved to {args.save} (backup before insert)")

    print(f"\nInserting {total} rules into MongoDB...")
    insert_rules_to_mongo(all_rules, args.mongo_url, args.db_name)
    print(f"\n   Validate with:")
    print(f"   python3 scripts/validate_rules.py --mongo-url $MONGO_URL \\")
    print(f"     --db-name {args.db_name} --batch-id {BATCH_ID}")


if __name__ == "__main__":
    main()
