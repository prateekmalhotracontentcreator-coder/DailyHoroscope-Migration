#!/usr/bin/env python3
"""
ingest_bphs_ch35_v1.py — BPHS Chapter 35: Nabhasa Yogas

32 Nabhasa Yogas (Aashraya ×3, Dala ×2, Akriti ×20, Sankhya ×7)
+ 1 general meta-rule = 33 rules total.

All rules are hard-coded directly from the source RTF — zero AI extraction cost.

Standard --save/--upload workflow (no double-cost):
  Step 1 — Dry run:
    python3 scripts/ingest_bphs_ch35_v1.py --dry-run --save bphs_ch35_rules.json

  Step 2 — Review bphs_ch35_rules.json; amend, add, or remove entries as needed.

  Step 3 — Upload (zero API calls):
    python3 scripts/ingest_bphs_ch35_v1.py \\
      --upload bphs_ch35_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 4 — Validate:
    python3 scripts/validate_rules.py \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id bphs-ch35-v1-20260426
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
CHAPTER    = 35
CHAP_NAME  = "Nabhasa Yogas"
BATCH_ID   = "bphs-ch35-v1-20260426"

# ── Yoga source data ──────────────────────────────────────────────────────────
# Each entry describes one yoga.  `yoga_check` is the machine-checkable
# formation descriptor (runtime detection in vedic_calculator.py).
#
# yoga_check.type values used in this chapter:
#   sign_quality_all          — all 7 planets in signs of specific quality
#   angles_by_planet_type     — N angular houses occupied by benefics/malefics
#   all_planets_in_houses     — all 7 planets confined to a house set (single or OR of sets)
#   all_planets_in_alt_signs  — all 7 planets in alternating signs (odd or even)
#   planets_in_n_signs        — all 7 planets spread across exactly N signs
#   complex                   — compound / multi-condition; checkable=False

YOGA_DATA: list[dict] = [

    # ────────────────────────────────────────────────────────────────────────
    # AASHRAYA YOGAS (3)  — based on sign modality of all planets
    # ────────────────────────────────────────────────────────────────────────
    {
        "yoga_name":   "Rajju Yoga",
        "category":    "aashraya",
        "formation":   (
            "All planets are placed in movable (cardinal) signs: "
            "Aries (1), Cancer (4), Libra (7), Capricorn (10)."
        ),
        "effect":      (
            "One born in Rajju yoga will be fond of wandering, be charming, "
            "will earn in foreign countries, and be cruel and mischievous."
        ),
        "is_benefic":  False,
        "life_domains": ["travel", "career", "character"],
        "yoga_check": {
            "type":         "sign_quality_all",
            "checkable":    True,
            "description":  (
                "All 7 planets (Sun through Saturn) must be in movable/cardinal signs: "
                "Aries (1), Cancer (4), Libra (7), Capricorn (10)."
            ),
            "sign_quality": "movable",
            "sign_numbers": [1, 4, 7, 10],
        },
    },
    {
        "yoga_name":   "Musala Yoga",
        "category":    "aashraya",
        "formation":   (
            "All planets are placed in fixed signs: "
            "Taurus (2), Leo (5), Scorpio (8), Aquarius (11)."
        ),
        "effect":      (
            "One born in Musala yoga will be endowed with honour, wisdom, wealth etc., "
            "be dear to king, famous, will have many sons and be firm in disposition."
        ),
        "is_benefic":  True,
        "life_domains": ["wealth", "fame", "character"],
        "yoga_check": {
            "type":         "sign_quality_all",
            "checkable":    True,
            "description":  (
                "All 7 planets must be in fixed signs: "
                "Taurus (2), Leo (5), Scorpio (8), Aquarius (11)."
            ),
            "sign_quality": "fixed",
            "sign_numbers": [2, 5, 8, 11],
        },
    },
    {
        "yoga_name":   "Nala Yoga",
        "category":    "aashraya",
        "formation":   (
            "All planets are placed in dual (mutable/common) signs: "
            "Gemini (3), Virgo (6), Sagittarius (9), Pisces (12)."
        ),
        "effect":      (
            "One born in Nala yoga will have uneven physique, be interested in "
            "accumulating money, very skilful, helpful to relatives, and charming."
        ),
        "is_benefic":  True,
        "life_domains": ["wealth", "family", "character"],
        "yoga_check": {
            "type":         "sign_quality_all",
            "checkable":    True,
            "description":  (
                "All 7 planets must be in dual/mutable signs: "
                "Gemini (3), Virgo (6), Sagittarius (9), Pisces (12)."
            ),
            "sign_quality": "dual",
            "sign_numbers": [3, 6, 9, 12],
        },
    },

    # ────────────────────────────────────────────────────────────────────────
    # DALA YOGAS (2)  — based on benefic/malefic occupation of angles
    # ────────────────────────────────────────────────────────────────────────
    {
        "yoga_name":   "Maala Yoga",
        "category":    "dala",
        "formation":   (
            "Three angular houses (kendras: 1st, 4th, 7th, 10th) are occupied "
            "by natural benefics (Jupiter, Venus, Mercury, Moon)."
        ),
        "effect":      (
            "One born in Maala yoga will be ever happy, endowed with conveyances, "
            "robes, food and pleasures, be splendorous and endowed with many females."
        ),
        "is_benefic":  True,
        "life_domains": ["happiness", "wealth", "comforts"],
        "yoga_check": {
            "type":         "angles_by_planet_type",
            "checkable":    True,
            "description":  (
                "At least 3 of the 4 angular houses (1, 4, 7, 10) must be occupied "
                "by natural benefics (Jupiter, Venus, Mercury, waxing Moon)."
            ),
            "planet_type":  "benefic",
            "kendra_count": 3,
            "houses":        [1, 4, 7, 10],
        },
    },
    {
        "yoga_name":   "Sarpa Yoga",
        "category":    "dala",
        "formation":   (
            "Three angular houses (kendras: 1st, 4th, 7th, 10th) are occupied "
            "by natural malefics (Sun, Mars, Saturn, Rahu, Ketu). "
            "Also called Bhujanga Yoga."
        ),
        "effect":      (
            "One born in Sarpa (Bhujanga) yoga will be crooked, cruel, poor, "
            "miserable and will depend on others for food and drinks."
        ),
        "is_benefic":  False,
        "life_domains": ["poverty", "character", "hardship"],
        "yoga_check": {
            "type":         "angles_by_planet_type",
            "checkable":    True,
            "description":  (
                "At least 3 of the 4 angular houses (1, 4, 7, 10) must be occupied "
                "by natural malefics (Sun, Mars, Saturn, Rahu, Ketu)."
            ),
            "planet_type":  "malefic",
            "kendra_count": 3,
            "houses":        [1, 4, 7, 10],
        },
    },

    # ────────────────────────────────────────────────────────────────────────
    # AKRITI YOGAS (20)  — based on specific house-set occupation
    # ────────────────────────────────────────────────────────────────────────
    {
        "yoga_name":   "Gada Yoga",
        "category":    "akriti",
        "formation":   (
            "All planets occupy two successive angular houses — one of the pairs: "
            "1st & 4th, 4th & 7th, 7th & 10th, or 10th & 1st."
        ),
        "effect":      (
            "One born in Gada yoga will always make efforts to earn wealth, will "
            "perform sacrificial rites, be skilful in Sastras and songs and endowed "
            "with wealth, gold and precious stones."
        ),
        "is_benefic":  True,
        "life_domains": ["wealth", "spirituality", "career"],
        "yoga_check": {
            "type":        "all_planets_in_houses",
            "checkable":   True,
            "description": (
                "All 7 planets must be in one of these pairs of successive angular "
                "houses: [1,4], [4,7], [7,10], or [10,1]."
            ),
            "house_sets":  [[1, 4], [4, 7], [7, 10], [10, 1]],
            "operator":    "or",
        },
    },
    {
        "yoga_name":   "Sakata Yoga",
        "category":    "akriti",
        "formation":   (
            "All planets are disposed in the 1st and 7th houses only."
        ),
        "effect":      (
            "One born in Sakata yoga will be afflicted by diseases, will have "
            "diseased or ugly nails, be foolish, will live by pulling carts, "
            "be poor and devoid of friends and relatives."
        ),
        "is_benefic":  False,
        "life_domains": ["health", "poverty", "social"],
        "yoga_check": {
            "type":        "all_planets_in_houses",
            "checkable":   True,
            "description": "All 7 planets must be in the 1st and/or 7th houses only.",
            "houses":       [1, 7],
        },
    },
    {
        "yoga_name":   "Vihaga Yoga",
        "category":    "akriti",
        "formation":   (
            "All planets are confined to the 4th and 10th houses only."
        ),
        "effect":      (
            "One born in Vihaga yoga will be fond of roaming, be a messenger, "
            "will live by sexual dealings, be shameless and interested in quarrels."
        ),
        "is_benefic":  False,
        "life_domains": ["travel", "character", "career"],
        "yoga_check": {
            "type":        "all_planets_in_houses",
            "checkable":   True,
            "description": "All 7 planets must be in the 4th and/or 10th houses only.",
            "houses":       [4, 10],
        },
    },
    {
        "yoga_name":   "Sringataka Yoga",
        "category":    "akriti",
        "formation":   (
            "All planets are in the trine houses: 1st, 5th, and 9th."
        ),
        "effect":      (
            "One born in Sringataka yoga will be fond of quarrels and battles, "
            "be happy, dear to king, endowed with an auspicious wife, "
            "be rich and will hate women."
        ),
        "is_benefic":  True,
        "life_domains": ["wealth", "marriage", "fame"],
        "yoga_check": {
            "type":        "all_planets_in_houses",
            "checkable":   True,
            "description": "All 7 planets must be in the trikona (trine) houses: 1st, 5th, and 9th.",
            "houses":       [1, 5, 9],
        },
    },
    {
        "yoga_name":   "Hala Yoga",
        "category":    "akriti",
        "formation":   (
            "All planets are in the 2nd, 6th and 10th houses; "
            "OR in the 3rd, 7th and 11th houses; "
            "OR in the 4th, 8th and 12th houses."
        ),
        "effect":      (
            "One born in Hala yoga will eat a lot, be very poor, be a farmer, "
            "be miserable, agitated, given up by friends and relatives and be a servant."
        ),
        "is_benefic":  False,
        "life_domains": ["poverty", "hardship", "career"],
        "yoga_check": {
            "type":        "all_planets_in_houses",
            "checkable":   True,
            "description": (
                "All 7 planets must be in one of three trisecting house sets: "
                "[2,6,10], [3,7,11], or [4,8,12]."
            ),
            "house_sets":  [[2, 6, 10], [3, 7, 11], [4, 8, 12]],
            "operator":    "or",
        },
    },
    {
        "yoga_name":   "Vajra Yoga",
        "category":    "akriti",
        "formation":   (
            "All benefics in the 1st and 7th houses and all malefics in the "
            "4th and 10th; OR (contrary arrangement) all benefics in the "
            "4th and 10th and all malefics in the 1st and 7th."
        ),
        "effect":      (
            "One born in Vajra yoga will be happy in the beginning and at the "
            "end of life, be valorous, charming, devoid of desires and fortunes "
            "and be inimical."
        ),
        "is_benefic":  False,
        "life_domains": ["character", "happiness", "hardship"],
        "yoga_check": {
            "type":        "multi_house_requirements",
            "checkable":   True,
            "description": (
                "Natural benefics placed in houses 1 and 7 (horizon axis); "
                "natural malefics placed in houses 4 and 10 (meridian axis). "
                "All conditions evaluated from the ascendant."
            ),
            "operator": "and",
            "house_requirements": [
                {"houses": [1, 7],  "planet_type": "benefic", "constraint": "present"},
                {"houses": [4, 10], "planet_type": "malefic", "constraint": "present"},
            ],
        },
    },
    {
        "yoga_name":   "Yava Yoga",
        "category":    "akriti",
        "formation":   (
            "All benefics in the 4th and 10th houses and all malefics in the "
            "1st and 7th; OR all benefics in 1st and 7th and all malefics in "
            "4th and 10th. (Contrary disposition to Vajra Yoga.)"
        ),
        "effect":      (
            "One born in Yava yoga will observe fasts and other religious rules, "
            "will do auspicious acts, will obtain happiness, wealth and sons in "
            "his mid-life, be charitable and firm."
        ),
        "is_benefic":  True,
        "life_domains": ["spirituality", "wealth", "family"],
        "yoga_check": {
            "type":        "multi_house_requirements",
            "checkable":   True,
            "description": (
                "Natural benefics placed in houses 4 and 10 (meridian axis); "
                "natural malefics placed in houses 1 and 7 (horizon axis). "
                "Mirror formation of Vajra Yoga."
            ),
            "operator": "and",
            "house_requirements": [
                {"houses": [4, 10], "planet_type": "benefic", "constraint": "present"},
                {"houses": [1, 7],  "planet_type": "malefic", "constraint": "present"},
            ],
        },
    },
    {
        "yoga_name":   "Kamala Yoga",
        "category":    "akriti",
        "formation":   (
            "All planets are placed in the four angular (kendra) houses: "
            "1st, 4th, 7th, and 10th."
        ),
        "effect":      (
            "One born in Kamala yoga will be rich and virtuous, be long-lived, "
            "very famous, pure, will perform hundreds of auspicious acts and be a king."
        ),
        "is_benefic":  True,
        "life_domains": ["wealth", "fame", "royalty", "longevity"],
        "yoga_check": {
            "type":        "all_planets_in_houses",
            "checkable":   True,
            "description": (
                "All 7 planets must be distributed across the four kendra houses: "
                "1st, 4th, 7th, and 10th."
            ),
            "houses":       [1, 4, 7, 10],
        },
    },
    {
        "yoga_name":   "Vapi Yoga",
        "category":    "akriti",
        "formation":   (
            "All planets are in all four cadent (dusthana) houses (3rd, 6th, 9th, 12th); "
            "OR all planets are in all four succedent (panapara) houses (2nd, 5th, 8th, 11th)."
        ),
        "effect":      (
            "One born in Vapi yoga will be capable of accumulating wealth, be endowed "
            "with lasting wealth, and happiness and sons, be free from eye afflictions "
            "and be a king."
        ),
        "is_benefic":  True,
        "life_domains": ["wealth", "health", "royalty", "family"],
        "yoga_check": {
            "type":        "all_planets_in_houses",
            "checkable":   True,
            "description": (
                "All 7 planets must be in all cadent houses [3,6,9,12] OR "
                "all in succedent houses [2,5,8,11]."
            ),
            "house_sets":  [[3, 6, 9, 12], [2, 5, 8, 11]],
            "operator":    "or",
        },
    },
    {
        "yoga_name":   "Yupa Yoga",
        "category":    "akriti",
        "formation":   (
            "All 7 planets are in four consecutive houses commencing from the "
            "1st house: houses 1, 2, 3, and 4."
        ),
        "effect":      (
            "One born in Yupa yoga will have spiritual knowledge, be interested in "
            "sacrificial rites, endowed with a wife, be strong, interested in fasts "
            "and other religious observations and be distinguished."
        ),
        "is_benefic":  True,
        "life_domains": ["spirituality", "marriage", "character"],
        "yoga_check": {
            "type":        "all_planets_in_houses",
            "checkable":   True,
            "description": (
                "All 7 planets must be in houses 1, 2, 3, and 4 "
                "(four consecutive houses starting from the ascendant)."
            ),
            "houses":       [1, 2, 3, 4],
        },
    },
    {
        "yoga_name":   "Sara Yoga",
        "category":    "akriti",
        "formation":   (
            "All 7 planets are in four consecutive houses commencing from the "
            "4th house: houses 4, 5, 6, and 7."
        ),
        "effect":      (
            "One born in Sara yoga will make arrows, be head of prison, will earn "
            "through animals, will eat meat and indulge in torture and mean handiworks."
        ),
        "is_benefic":  False,
        "life_domains": ["career", "character", "hardship"],
        "yoga_check": {
            "type":        "all_planets_in_houses",
            "checkable":   True,
            "description": (
                "All 7 planets must be in houses 4, 5, 6, and 7 "
                "(four consecutive houses starting from the 4th)."
            ),
            "houses":       [4, 5, 6, 7],
        },
    },
    {
        "yoga_name":   "Sakthi Yoga",
        "category":    "akriti",
        "formation":   (
            "All 7 planets are in four consecutive houses commencing from the "
            "7th house: houses 7, 8, 9, and 10."
        ),
        "effect":      (
            "One born in Sakthi yoga will be bereft of wealth, be unsuccessful, "
            "miserable, mean, lazy, long-lived, interested and skilful in war, "
            "firm and auspicious."
        ),
        "is_benefic":  False,
        "life_domains": ["poverty", "longevity", "career"],
        "yoga_check": {
            "type":        "all_planets_in_houses",
            "checkable":   True,
            "description": (
                "All 7 planets must be in houses 7, 8, 9, and 10 "
                "(four consecutive houses starting from the 7th)."
            ),
            "houses":       [7, 8, 9, 10],
        },
    },
    {
        "yoga_name":   "Danda Yoga",
        "category":    "akriti",
        "formation":   (
            "All 7 planets are in four consecutive houses commencing from the "
            "10th house: houses 10, 11, 12, and 1."
        ),
        "effect":      (
            "One born in Danda yoga will lose his sons and wife, be indigent, "
            "unkind, away from his men, miserable and will serve mean people."
        ),
        "is_benefic":  False,
        "life_domains": ["family", "poverty", "hardship"],
        "yoga_check": {
            "type":        "all_planets_in_houses",
            "checkable":   True,
            "description": (
                "All 7 planets must be in houses 10, 11, 12, and 1 "
                "(four consecutive houses starting from the 10th)."
            ),
            "houses":       [10, 11, 12, 1],
        },
    },
    {
        "yoga_name":   "Nauka Yoga",
        "category":    "akriti",
        "formation":   (
            "All planets occupy seven consecutive houses commencing from the "
            "1st house: houses 1 through 7."
        ),
        "effect":      (
            "One born in Nauka yoga will derive his livelihood through water, "
            "be wealthy, famous, wicked, wretched, dirty and miserly."
        ),
        "is_benefic":  False,
        "life_domains": ["career", "wealth", "character"],
        "yoga_check": {
            "type":        "all_planets_in_houses",
            "checkable":   True,
            "description": (
                "All 7 planets must be in houses 1 through 7 "
                "(seven consecutive houses from the ascendant)."
            ),
            "houses":       [1, 2, 3, 4, 5, 6, 7],
        },
    },
    {
        "yoga_name":   "Koota Yoga",
        "category":    "akriti",
        "formation":   (
            "All planets occupy seven consecutive houses commencing from the "
            "4th house: houses 4 through 10."
        ),
        "effect":      (
            "One born in Koota yoga will be a liar, will head a jail, be poor, "
            "crafty, cruel and will live in hills and fortresses."
        ),
        "is_benefic":  False,
        "life_domains": ["career", "poverty", "character"],
        "yoga_check": {
            "type":        "all_planets_in_houses",
            "checkable":   True,
            "description": (
                "All 7 planets must be in houses 4 through 10 "
                "(seven consecutive houses starting from the 4th)."
            ),
            "houses":       [4, 5, 6, 7, 8, 9, 10],
        },
    },
    {
        "yoga_name":   "Chatra Yoga",
        "category":    "akriti",
        "formation":   (
            "All planets occupy seven consecutive houses commencing from the "
            "7th house: houses 7, 8, 9, 10, 11, 12, and 1."
        ),
        "effect":      (
            "One born in Chatra yoga will help his own men, be kind, dear to many "
            "kings, very intelligent, be happy at the beginning and end of his life "
            "and be long-lived."
        ),
        "is_benefic":  True,
        "life_domains": ["fame", "happiness", "longevity"],
        "yoga_check": {
            "type":        "all_planets_in_houses",
            "checkable":   True,
            "description": (
                "All 7 planets must be in houses 7, 8, 9, 10, 11, 12, and 1 "
                "(seven consecutive houses starting from the 7th)."
            ),
            "houses":       [7, 8, 9, 10, 11, 12, 1],
        },
    },
    {
        "yoga_name":   "Chapa Yoga",
        "category":    "akriti",
        "formation":   (
            "All planets occupy seven consecutive houses commencing from the "
            "10th house: houses 10, 11, 12, 1, 2, 3, and 4. "
            "Also called Dhanushi Yoga."
        ),
        "effect":      (
            "One born in Chapa yoga will be a liar, will protect secrets, be a thief, "
            "be fond of wandering in forests, be devoid of luck and be happy in the "
            "middle of his life."
        ),
        "is_benefic":  False,
        "life_domains": ["character", "travel", "hardship"],
        "yoga_check": {
            "type":        "all_planets_in_houses",
            "checkable":   True,
            "description": (
                "All 7 planets must be in houses 10, 11, 12, 1, 2, 3, and 4 "
                "(seven consecutive houses starting from the 10th)."
            ),
            "houses":       [10, 11, 12, 1, 2, 3, 4],
        },
    },
    {
        "yoga_name":   "Ardha Chandra Yoga",
        "category":    "akriti",
        "formation":   (
            "All planets are arranged in a half-moon (semicircular) pattern across "
            "seven consecutive houses. (Exact starting house not specified in this "
            "chapter; cross-reference other BPHS translations for the precise variant.)"
        ),
        "effect":      (
            "One born in Ardha Chandra Yoga will lead an army, will possess a "
            "splendorous body, be dear to king, be strong and endowed with gems, "
            "gold and ornaments."
        ),
        "is_benefic":  True,
        "life_domains": ["fame", "wealth", "royalty"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Half-moon (Ardha Chandra) formation: planets arranged in "
                "seven consecutive houses forming a semicircular arc. "
                "Exact starting house variant not explicitly defined in this chapter. "
                "Phase 2: resolve from cross-referencing other BPHS translations."
            ),
        },
    },
    {
        "yoga_name":   "Chakra Yoga",
        "category":    "akriti",
        "formation":   (
            "All planets occupy six alternating signs commencing from the ascendant "
            "(odd signs: 1, 3, 5, 7, 9, 11 — Aries, Gemini, Leo, Libra, "
            "Sagittarius, Aquarius)."
        ),
        "effect":      (
            "One born in Chakra yoga will be an emperor at whose feet will be "
            "the prostrating kings' heads adoring gem-studded diadems."
        ),
        "is_benefic":  True,
        "life_domains": ["royalty", "fame", "power"],
        "yoga_check": {
            "type":         "all_planets_in_alt_signs",
            "checkable":    True,
            "description":  (
                "All 7 planets must be in the 6 odd zodiac signs (1,3,5,7,9,11): "
                "Aries, Gemini, Leo, Libra, Sagittarius, Aquarius."
            ),
            "sign_numbers": [1, 3, 5, 7, 9, 11],
            "parity":        "odd",
        },
    },
    {
        "yoga_name":   "Samudra Yoga",
        "category":    "akriti",
        "formation":   (
            "All planets occupy six alternating signs commencing from the 2nd sign "
            "from the ascendant (even signs: 2, 4, 6, 8, 10, 12 — Taurus, Cancer, "
            "Virgo, Scorpio, Capricorn, Pisces)."
        ),
        "effect":      (
            "One born in Samudra yoga will have many precious stones and abundant "
            "wealth, be endowed with pleasures, dear to people, will have firm "
            "wealth and be well-disposed."
        ),
        "is_benefic":  True,
        "life_domains": ["wealth", "happiness", "comforts"],
        "yoga_check": {
            "type":         "all_planets_in_alt_signs",
            "checkable":    True,
            "description":  (
                "All 7 planets must be in the 6 even zodiac signs (2,4,6,8,10,12): "
                "Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces."
            ),
            "sign_numbers": [2, 4, 6, 8, 10, 12],
            "parity":        "even",
        },
    },

    # ────────────────────────────────────────────────────────────────────────
    # SANKHYA YOGAS (7)  — based on number of signs occupied by all planets
    # BPHS note: "None of these seven yogas will be operable if another
    # Nabhasa yoga (Aashraya/Dala/Akriti) is derivable."
    # ────────────────────────────────────────────────────────────────────────
    {
        "yoga_name":   "Gola Yoga",
        "category":    "sankhya",
        "formation":   (
            "All 7 planets are placed in only 1 zodiac sign. "
            "Note: Sankhya yogas are superseded by any applicable "
            "Aashraya, Dala, or Akriti Nabhasa yoga."
        ),
        "effect":      (
            "One born in Gola yoga will be strong, be devoid of wealth, learning "
            "and intelligence, be dirty, sorrowful and miserable."
        ),
        "is_benefic":  False,
        "life_domains": ["poverty", "health", "character"],
        "yoga_check": {
            "type":        "planets_in_n_signs",
            "checkable":   True,
            "description": (
                "All 7 planets (Sun through Saturn) must occupy exactly 1 zodiac sign. "
                "Superseded if any Aashraya/Dala/Akriti yoga is also present."
            ),
            "sign_count":  1,
            "precedence":  "superseded_by_higher_nabhasa",
        },
    },
    {
        "yoga_name":   "Yuga Yoga",
        "category":    "sankhya",
        "formation":   (
            "All 7 planets are distributed across exactly 2 zodiac signs. "
            "Note: Sankhya yogas are superseded by any applicable "
            "Aashraya, Dala, or Akriti Nabhasa yoga."
        ),
        "effect":      (
            "One born in Yuga yoga will be heretic, be devoid of wealth, "
            "be discarded by others, and be devoid of sons, mother and virtues."
        ),
        "is_benefic":  False,
        "life_domains": ["poverty", "family", "character"],
        "yoga_check": {
            "type":        "planets_in_n_signs",
            "checkable":   True,
            "description": (
                "All 7 planets must occupy exactly 2 zodiac signs. "
                "Superseded if any Aashraya/Dala/Akriti yoga is also present."
            ),
            "sign_count":  2,
            "precedence":  "superseded_by_higher_nabhasa",
        },
    },
    {
        "yoga_name":   "Soola Yoga",
        "category":    "sankhya",
        "formation":   (
            "All 7 planets are distributed across exactly 3 zodiac signs. "
            "Note: Sankhya yogas are superseded by any applicable "
            "Aashraya, Dala, or Akriti Nabhasa yoga."
        ),
        "effect":      (
            "One born in Soola yoga will be sharp, indolent, bereft of wealth, "
            "be torturous, prohibited, valiant, and famous through war."
        ),
        "is_benefic":  False,
        "life_domains": ["career", "poverty", "character"],
        "yoga_check": {
            "type":        "planets_in_n_signs",
            "checkable":   True,
            "description": (
                "All 7 planets must occupy exactly 3 zodiac signs. "
                "Superseded if any Aashraya/Dala/Akriti yoga is also present."
            ),
            "sign_count":  3,
            "precedence":  "superseded_by_higher_nabhasa",
        },
    },
    {
        "yoga_name":   "Kedara Yoga",
        "category":    "sankhya",
        "formation":   (
            "All 7 planets are distributed across exactly 4 zodiac signs. "
            "Note: Sankhya yogas are superseded by any applicable "
            "Aashraya, Dala, or Akriti Nabhasa yoga."
        ),
        "effect":      (
            "One born in Kedara yoga will be useful to many, be an agriculturist, "
            "be truthful, happy, fickle-minded and wealthy."
        ),
        "is_benefic":  True,
        "life_domains": ["career", "wealth", "character"],
        "yoga_check": {
            "type":        "planets_in_n_signs",
            "checkable":   True,
            "description": (
                "All 7 planets must occupy exactly 4 zodiac signs. "
                "Superseded if any Aashraya/Dala/Akriti yoga is also present."
            ),
            "sign_count":  4,
            "precedence":  "superseded_by_higher_nabhasa",
        },
    },
    {
        "yoga_name":   "Paasa Yoga",
        "category":    "sankhya",
        "formation":   (
            "All 7 planets are distributed across exactly 5 zodiac signs. "
            "Note: Sankhya yogas are superseded by any applicable "
            "Aashraya, Dala, or Akriti Nabhasa yoga."
        ),
        "effect":      (
            "One born in Paasa yoga will be liable to be imprisoned, be skilful "
            "in work, be deceiving in disposition, will talk much, be bereft of "
            "good qualities and will have many servants."
        ),
        "is_benefic":  False,
        "life_domains": ["career", "character", "legal"],
        "yoga_check": {
            "type":        "planets_in_n_signs",
            "checkable":   True,
            "description": (
                "All 7 planets must occupy exactly 5 zodiac signs. "
                "Superseded if any Aashraya/Dala/Akriti yoga is also present."
            ),
            "sign_count":  5,
            "precedence":  "superseded_by_higher_nabhasa",
        },
    },
    {
        "yoga_name":   "Dama Yoga",
        "category":    "sankhya",
        "formation":   (
            "All 7 planets are distributed across exactly 6 zodiac signs. "
            "Also called Daamini Yoga. "
            "Note: Sankhya yogas are superseded by any applicable "
            "Aashraya, Dala, or Akriti Nabhasa yoga."
        ),
        "effect":      (
            "One born in Dama yoga will be helpful to others, will have righteously "
            "earned wealth, be very affluent, famous, will have many sons and gems, "
            "be courageous and red-lettered."
        ),
        "is_benefic":  True,
        "life_domains": ["wealth", "fame", "family"],
        "yoga_check": {
            "type":        "planets_in_n_signs",
            "checkable":   True,
            "description": (
                "All 7 planets must occupy exactly 6 zodiac signs. "
                "Superseded if any Aashraya/Dala/Akriti yoga is also present."
            ),
            "sign_count":  6,
            "precedence":  "superseded_by_higher_nabhasa",
        },
    },
    {
        "yoga_name":   "Veena Yoga",
        "category":    "sankhya",
        "formation":   (
            "All 7 planets are each in a different zodiac sign (7 planets in 7 signs). "
            "Also called Vallaki Yoga. "
            "Note: Sankhya yogas are superseded by any applicable "
            "Aashraya, Dala, or Akriti Nabhasa yoga."
        ),
        "effect":      (
            "One born in Veena yoga will be fond of songs, dance and musical "
            "instruments, be skilful, happy, wealthy and be a leader of men."
        ),
        "is_benefic":  True,
        "life_domains": ["arts", "wealth", "fame"],
        "yoga_check": {
            "type":        "planets_in_n_signs",
            "checkable":   True,
            "description": (
                "All 7 planets must each occupy a different zodiac sign "
                "(7 planets in 7 distinct signs). "
                "Superseded if any Aashraya/Dala/Akriti yoga is also present."
            ),
            "sign_count":  7,
            "precedence":  "superseded_by_higher_nabhasa",
        },
    },
]

# ── Meta-rule (general principle for all Nabhasa yogas) ──────────────────────

META_RULE: dict = {
    "yoga_name":   "Nabhasa Yoga — General Principle",
    "category":    "general",
    "formation":   "General principle applicable to all 32 Nabhasa Yogas.",
    "effect":      (
        "Ancestors say that the results due to the said Nabhasa yogas will be "
        "felt throughout, in all the Dasa periods."
    ),
    "is_benefic":  True,
    "life_domains": ["general"],
    "yoga_check": {
        "type":        "complex",
        "checkable":   False,
        "description": (
            "Meta-rule: Results of any active Nabhasa yoga persist across all Dasa "
            "periods. Unlike most other yogas (which strengthen in relevant dasas), "
            "Nabhasa yoga effects are constant throughout the native's life."
        ),
    },
}

# ── Condition group IDs ───────────────────────────────────────────────────────

CATEGORY_GROUP: dict[str, str] = {
    "aashraya": "bphs-ch35-aashraya",
    "dala":     "bphs-ch35-dala",
    "akriti":   "bphs-ch35-akriti",
    "sankhya":  "bphs-ch35-sankhya",
    "general":  "bphs-ch35-general",
}

CATEGORY_LABEL: dict[str, str] = {
    "aashraya": "Aashraya Yoga",
    "dala":     "Dala Yoga",
    "akriti":   "Akriti Yoga",
    "sankhya":  "Sankhya Yoga",
    "general":  "General Principle",
}

# ── build_rule ────────────────────────────────────────────────────────────────

def build_rule(yoga: dict, index: int) -> dict:
    rule_id         = f"bphs-ch35-{index:03d}"
    cat             = yoga["category"]
    cond_group_id   = CATEGORY_GROUP[cat]
    cat_label       = CATEGORY_LABEL[cat]
    cond_type       = "general_principle" if cat == "general" else "yoga_combination"
    sub_type        = "yoga_formation"
    yoga_name       = yoga["yoga_name"]
    is_benefic      = yoga["is_benefic"]
    formation       = yoga["formation"]
    effect          = yoga["effect"]
    life_domains    = yoga["life_domains"]
    yc              = yoga["yoga_check"]

    detailed = (
        f"Yoga: {yoga_name} [{cat_label}]\n\n"
        f"Formation: {formation}\n\n"
        f"Effect: {effect}"
    )
    summary = f"{yoga_name} — {effect}"
    if len(summary) > 200:
        summary = summary[:197] + "..."

    tags = [
        "verbatim", "yoga", f"chapter{CHAPTER}", "nabhasa",
        f"nabhasa_{cat}", cond_type, sub_type,
        f"group:{cond_group_id}",
        "benefic" if is_benefic else "malefic",
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
            "sloka":          f"ch35-{yoga_name.lower().replace(' ', '-')}",
            "batch_id":       BATCH_ID,
            "primary":        BOOK,
            "page_ref":       None,
            "passage_ref_id": None,
        },
        "condition": {
            "type":               cond_type,
            "sub_type":           sub_type,
            "yoga_name":          yoga_name,
            "yoga_category":      cat,
            "yoga_category_label": cat_label,
            "planets_involved":   [],
            "houses_involved":    yc.get("houses") or [],
            "sub_conditions":     [],
            "operator":           "and",
            "gender_context":     "neutral",
            "condition_group_id": cond_group_id,
            "is_group_summary":   False,
            "is_benefic":         is_benefic,
            "yoga_check":         yc,
        },
        "interpretation": {
            "summary":            summary,
            "detailed":           detailed,
            "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
            "remedies":           [],
            "life_domain":        life_domains[0] if life_domains else "general",
            "life_domains":       life_domains,
            "tags":               tags,
            "physical_markers":   [],
        },
        "metadata": {
            "planets_involved":     [],
            "houses_involved":      yc.get("houses") or [],
            "signs_involved":       yc.get("sign_numbers") or [],
            "condition_count":      1,
            "gender_context":       "neutral",
            "condition_group_id":   cond_group_id,
            "is_group_summary":     False,
            "has_physical_markers": False,
            "physical_categories":  [],
            "yoga_checkable":       bool(yc.get("checkable")),
            "nabhasa_category":     cat,
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
        print("   Nothing inserted.  Drop the batch first if you want to re-ingest.")
        client.close()
        return
    result = col.insert_many(all_rules, ordered=False)
    print(f"\n✅  Inserted {len(result.inserted_ids)} rules into MongoDB")
    print(f"   batch_id : {BATCH_ID}")
    client.close()


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest BPHS Ch 35 Nabhasa Yogas into Knowledge Engine"
    )
    parser.add_argument("--mongo-url", default=None, help="MongoDB connection URL")
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--dry-run",   action="store_true",
                        help="Print sample output without writing to MongoDB")
    parser.add_argument("--save",      default=None, metavar="FILE",
                        help="(Dry-run) Save all rules to JSON file for review")
    parser.add_argument("--upload",    default=None, metavar="FILE",
                        help="Skip extraction — upload rules from this JSON file directly")
    args = parser.parse_args()

    # ── --upload path (zero extraction cost) ──────────────────────────────────
    if args.upload:
        if not args.mongo_url:
            print("⚠  --upload requires --mongo-url"); sys.exit(1)
        upload_path = Path(args.upload)
        if not upload_path.exists():
            print(f"⚠  File not found: {args.upload}"); sys.exit(1)
        with open(upload_path, encoding="utf-8") as fh:
            all_rules = json.load(fh)
        print(f"\n✅  Loaded {len(all_rules)} rules from {args.upload}")
        insert_rules_to_mongo(all_rules, args.mongo_url, args.db_name)
        print(f"\n   Validate with:")
        print(f"   python3 scripts/validate_rules.py --mongo-url $MONGO_URL \\")
        print(f"     --db-name {args.db_name} --batch-id {BATCH_ID}")
        return

    # ── Build all rules ───────────────────────────────────────────────────────
    all_rules: list[dict] = []
    index = 1
    for yoga in YOGA_DATA:
        all_rules.append(build_rule(yoga, index))
        index += 1
    all_rules.append(build_rule(META_RULE, index))   # meta-rule last

    total     = len(all_rules)
    benefic   = sum(1 for r in all_rules if r["condition"]["is_benefic"])
    adverse   = total - benefic
    checkable = sum(1 for r in all_rules if r["metadata"]["yoga_checkable"])

    # Category breakdown
    cat_counts: dict[str, int] = {}
    for r in all_rules:
        c = r["metadata"]["nabhasa_category"]
        cat_counts[c] = cat_counts.get(c, 0) + 1

    # ── Dry-run output ────────────────────────────────────────────────────────
    print(f"\n{'─' * 65}")
    print(f"BPHS Chapter {CHAPTER} — {CHAP_NAME}  [v1 hard-coded]")
    print(f"batch_id : {BATCH_ID}")
    print(f"{'─' * 65}")
    print(f"\nCategory breakdown:")
    for cat, count in cat_counts.items():
        print(f"  {CATEGORY_LABEL[cat]:<22} : {count}")
    print(f"  {'─' * 30}")
    print(f"  TOTAL                  : {total}")
    print(f"\nBenefic rules  : {benefic}")
    print(f"Adverse rules  : {adverse}")
    print(f"Yoga-checkable : {checkable} / {total}")

    print(f"\nSample rules (first 3):")
    print(f"{'─' * 65}")
    for rule in all_rules[:3]:
        cond  = rule["condition"]
        yc    = cond["yoga_check"]
        print(f"  rule_id   : {rule['rule_id']}")
        print(f"  yoga      : {cond['yoga_name']}  [{cond['yoga_category_label']}]")
        print(f"  check_type: {yc['type']}  checkable={yc['checkable']}")
        print(f"  is_benefic: {cond['is_benefic']}")
        print(f"  summary   : {rule['interpretation']['summary'][:90]}...")
        print()

    print(f"Isolation: approval_status='pending_review' — zero rules reach live users")

    if args.dry_run:
        if args.save:
            save_path = Path(args.save)
            with open(save_path, "w", encoding="utf-8") as fh:
                json.dump(all_rules, fh, indent=2, default=str)
            print(f"\n✅  Rules saved to {args.save}  ({total} rules)")
            print(f"   Review the file, then upload with:")
            print(f"   python3 scripts/ingest_bphs_ch35_v1.py \\")
            print(f"     --upload {args.save} --mongo-url $MONGO_URL --db-name {args.db_name}")
        return

    # ── Live run ──────────────────────────────────────────────────────────────
    if not args.mongo_url:
        print("\n⚠  Live run requires --mongo-url  (or use --dry-run / --upload)")
        sys.exit(1)

    if args.save:
        save_path = Path(args.save)
        with open(save_path, "w", encoding="utf-8") as fh:
            json.dump(all_rules, fh, indent=2, default=str)
        print(f"\n✅  Rules saved to {args.save} (backup before insert)")

    print(f"\nInserting {total} rules into MongoDB...")
    insert_rules_to_mongo(all_rules, args.mongo_url, args.db_name)

    print(f"\n   Validate with:")
    print(f"   python3 scripts/validate_rules.py --mongo-url $MONGO_URL \\")
    print(f"     --db-name {args.db_name} --batch-id {BATCH_ID}")


if __name__ == "__main__":
    main()
