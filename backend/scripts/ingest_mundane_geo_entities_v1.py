#!/usr/bin/env python3
"""
ingest_mundane_geo_entities_v1.py

Mundane Astrology — Geographic Entity Database
BATCH_ID: mundane-geo-v1-20260505
TARGET COLLECTION: horoscope_db.mundane_geo_entities

29 documents across 3 entity types:
  9  Koorma Chakra directional zones (Gaur Ch 4/5, Mehta Ch 7)
  12 Zodiac Geography sign documents  (Mehta Ch 3 primary, Gopal Ch 3 modern)
  8  National Foundation Horoscopes   (Mehta Ch 3 + Gopal Ch 3 + Raphael Ch 1)

Schema decisions (locked — see 5 Book Ingest Strategy_Account 1 Analysis.md Q15):
  - Collection: mundane_geo_entities  (NOT interpretation_rules, NOT geo_entities)
  - science: "mundane_jyotish"        (never "jyotish" — different domain)
  - Multi-book: synthesis_sources array lists all contributing books per entity
  - These are LOOKUP TABLES, not interpretable rules. The interpretation_rules
    collection will reference these by zone/sign for geo-targeted predictions.

Book attribution codes:
  gaur_aifas   — Gaur/AIFAS: Ancient Core (primary structural authority)
  mehta_rao    — Mehta/Rao: Operating System (modern Indian framework)
  gopal_modern — Gopalakrishnan: Modern ontology (post-independence updates)
  raphael_west — Raphael: Western granular calibrator
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pymongo import MongoClient

SCIENCE   = "mundane_jyotish"
BATCH_ID  = "mundane-geo-v1-20260505"
COLL_NAME = "mundane_geo_entities"

# ── KOORMA CHAKRA: 9 directional zones ───────────────────────────────────────
# Tortoise-body glyph maps 27 Nakshatras to 9 geographic directions.
# Sources: Gaur Ch 4/5 (primary grid), Mehta Ch 7 (reconciliation).
# 3 nakshatras per zone. Rules: Saturn/malefic transiting zone nakshatra
# → trouble in that direction. Benefic transit → prosperity in that direction.

KOORMA_ZONES = [
    {
        "entity_id":   "koorma-center-back",
        "zone_key":    "center_back",
        "body_part":   "Center-Back of Tortoise",
        "direction":   "Central India / Interior Regions",
        "nakshatras":  ["Krittika", "Rohini", "Mrigshira"],
        "special_note": (
            "Rohini is the CRITICAL GATE in this zone — Saturn or malefics transiting "
            "Rohini (Taurus 10°–23°20') create the 'Rohini Gate' war/famine threshold "
            "(validated: WWI 1914, WWII 1939, 1971 Indo-Pak War). See mundane-war-rohini-gate "
            "in interpretation_rules."
        ),
        "synthesis_sources": ["gaur_aifas", "mehta_rao"],
    },
    {
        "entity_id":   "koorma-mouth-east",
        "zone_key":    "mouth_east",
        "body_part":   "Mouth / Eastern Face of Tortoise",
        "direction":   "East",
        "nakshatras":  ["Ardra", "Punarvasu", "Pushya"],
        "special_note": (
            "Pushya nakshatra (Cancer 3°20'–16°40') in this zone: Saturn transiting Pushya "
            "triggers the 'Pushya Bull Run' — exceptional stock market growth. "
            "Validated: 2006 Sensex 6000 → 12000+ rise (Gopal Ch 14)."
        ),
        "synthesis_sources": ["gaur_aifas", "mehta_rao", "gopal_modern"],
    },
    {
        "entity_id":   "koorma-front-right-southeast",
        "zone_key":    "front_right_foot_southeast",
        "body_part":   "Front Right Foot of Tortoise",
        "direction":   "South-East",
        "nakshatras":  ["Ashlesha", "Magha", "Poorvaphalguni"],
        "synthesis_sources": ["gaur_aifas", "mehta_rao"],
    },
    {
        "entity_id":   "koorma-right-stomach-south",
        "zone_key":    "right_stomach_south",
        "body_part":   "Right Stomach of Tortoise",
        "direction":   "South",
        "nakshatras":  ["Uttaraphalguni", "Hasta", "Chitra"],
        "special_note": (
            "Mars in Taurus (South sign) identifies threats arriving FROM the South. "
            "Validated: Rajiv Gandhi assassination — LTTE/Tamil Tigers correctly identified "
            "as arriving from the South via Mars in Taurus (Mehta Ch 21)."
        ),
        "synthesis_sources": ["gaur_aifas", "mehta_rao"],
    },
    {
        "entity_id":   "koorma-back-right-southwest",
        "zone_key":    "back_right_foot_southwest",
        "body_part":   "Back Right Foot of Tortoise",
        "direction":   "South-West",
        "nakshatras":  ["Swati", "Anuradha", "Vishakha"],
        "synthesis_sources": ["gaur_aifas", "mehta_rao"],
    },
    {
        "entity_id":   "koorma-tail-west",
        "zone_key":    "tail_west",
        "body_part":   "Tail of Tortoise",
        "direction":   "West",
        "nakshatras":  ["Jyeshtha", "Mool", "Poorvashadh"],
        "synthesis_sources": ["gaur_aifas", "mehta_rao"],
    },
    {
        "entity_id":   "koorma-back-left-northwest",
        "zone_key":    "back_left_foot_northwest",
        "body_part":   "Back Left Foot of Tortoise",
        "direction":   "North-West",
        "nakshatras":  ["Uttarashadh", "Shravan", "Dhanishtha"],
        "synthesis_sources": ["gaur_aifas", "mehta_rao"],
    },
    {
        "entity_id":   "koorma-left-stomach-north",
        "zone_key":    "left_stomach_north",
        "body_part":   "Left Stomach of Tortoise",
        "direction":   "North",
        "nakshatras":  ["Shatbhisha", "Poorvabhadrapad", "Uttarabhadrapad"],
        "synthesis_sources": ["gaur_aifas", "mehta_rao"],
    },
    {
        "entity_id":   "koorma-front-left-northeast",
        "zone_key":    "front_left_foot_northeast",
        "body_part":   "Front Left Foot of Tortoise",
        "direction":   "North-East",
        "nakshatras":  ["Revati", "Ashwini", "Bharani"],
        "synthesis_sources": ["gaur_aifas", "mehta_rao"],
    },
]

# ── ZODIAC GEOGRAPHY: 12 signs → countries/cities ────────────────────────────
# Primary source: Mehta Ch 3 (traditional Indian framework).
# Modern updates: Gopal Ch 3 (post-independence geopolitical revisions).
# Raphael Ch 1 provides Western calibration for non-Indian entities.
# Usage: When a planet transits sign X, interpretation_rules for that sign's
# countries/regions are activated for geo-targeted mundane predictions.

ZODIAC_GEOGRAPHY = [
    {
        "entity_id": "geo-sign-aries",
        "sign":      "aries",
        "sign_no":   1,
        "countries": ["UK", "France", "Switzerland", "Germany", "Japan",
                      "Palestine", "Syria", "Denmark", "Poland"],
        "cities":    ["Birmingham", "Brunswick", "Florence", "Leicester",
                      "Cracow", "Naples", "Utrecht", "Marseilles"],
        "india_regions": ["Rajasthan", "Madhya Pradesh (Eastern)"],
        "element":   "fire",
        "modality":  "cardinal",
        "synthesis_sources": ["mehta_rao", "raphael_west"],
    },
    {
        "entity_id": "geo-sign-taurus",
        "sign":      "taurus",
        "sign_no":   2,
        "countries": ["Ireland", "Iran", "Cyprus", "Australia",
                      "Sri Lanka", "Pakistan"],
        "cities":    ["Dublin", "Tehran", "Palermo", "Parma", "Leipzig",
                      "St. Louis", "Mantua"],
        "india_regions": ["Gujarat", "Rajasthan (Western)", "Mumbai region"],
        "element":   "earth",
        "modality":  "fixed",
        "special_note": (
            "India's Lagna is TAURUS (Independence Chart: 15 Aug 1947). "
            "Pakistan's Lagna is ARIES — the 2/12 relationship between "
            "Taurus (India) and Aries (Pakistan) = permanent rivalry axis. "
            "See mundane-gopal-212-rivalry in interpretation_rules."
        ),
        "synthesis_sources": ["mehta_rao", "gopal_modern", "raphael_west"],
    },
    {
        "entity_id": "geo-sign-gemini",
        "sign":      "gemini",
        "sign_no":   3,
        "countries": ["USA", "Wales", "Belgium", "Armenia", "Eritrea",
                      "Tunisia", "Sardinia"],
        "cities":    ["London", "Versailles", "Nuremberg", "Plymouth",
                      "San Francisco", "Mecca"],
        "india_regions": ["Uttar Pradesh", "Bihar (Northern)", "Delhi NCR"],
        "element":   "air",
        "modality":  "dual",
        "synthesis_sources": ["mehta_rao", "raphael_west"],
    },
    {
        "entity_id": "geo-sign-cancer",
        "sign":      "cancer",
        "sign_no":   4,
        "countries": ["Holland", "Scotland", "New Zealand", "Paraguay",
                      "Mauritania", "Morocco"],
        "cities":    ["Amsterdam", "Berne", "Cadiz", "Constantinople",
                      "Genoa", "Milan", "Venice", "New York (Eastern)"],
        "india_regions": ["Bengal", "Assam", "Odisha", "Coastal East India"],
        "element":   "water",
        "modality":  "cardinal",
        "special_note": (
            "India's Cancer-Capricorn AXIS is the critical war axis (Mehta Ch 19). "
            "Afflictions to Cancer proven more serious than Taurus-Scorpio axis "
            "in 1962 and 1971 Indian wars."
        ),
        "synthesis_sources": ["mehta_rao", "raphael_west"],
    },
    {
        "entity_id": "geo-sign-leo",
        "sign":      "leo",
        "sign_no":   5,
        "countries": ["France", "Italy", "Macedonia", "Sicily",
                      "Romania", "Czech Republic"],
        "cities":    ["Rome", "Bath", "Bristol", "Bombay (financial)",
                      "Damascus", "Los Angeles", "Chicago"],
        "india_regions": ["Madhya Pradesh (Central)", "Chhattisgarh"],
        "element":   "fire",
        "modality":  "fixed",
        "special_note": (
            "Saturn entering Leo = 'Real Estate Bull Run': 100% growth in property "
            "prices (validated 2006-2008). Saturn-Ketu conjunction in Leo = oil at $70/barrel. "
            "USA Foundation Chart: Leo Lagna (4 Jul 1776, 10:21:30 AM, Philadelphia)."
        ),
        "synthesis_sources": ["mehta_rao", "gopal_modern", "raphael_west"],
    },
    {
        "entity_id": "geo-sign-virgo",
        "sign":      "virgo",
        "sign_no":   6,
        "countries": ["Greece", "Turkey", "Switzerland (southern)", "Brazil",
                      "Croatia", "Mesopotamia"],
        "cities":    ["Athens", "Corinth", "Boston", "Heidelberg",
                      "Jerusalem", "Paris (financial district)"],
        "india_regions": ["Andhra Pradesh", "Telangana", "Karnataka (Northern)"],
        "element":   "earth",
        "modality":  "dual",
        "synthesis_sources": ["mehta_rao", "raphael_west"],
    },
    {
        "entity_id": "geo-sign-libra",
        "sign":      "libra",
        "sign_no":   7,
        "countries": ["China", "Austria", "Japan (cultural)", "Argentina",
                      "Burma", "Tibet"],
        "cities":    ["Lisbon", "Vienna", "Frankfurt", "Antwerp",
                      "Johannesburg", "Nottingham", "Spires"],
        "india_regions": ["Uttar Pradesh (Western)", "Haryana", "Punjab"],
        "special_note": (
            "India's Trika Axis: Sagittarius/Aries/LIBRA = 8th house of "
            "Independent India. Sun transit through Libra activates danger "
            "phase for national security (Gopal Ch 8)."
        ),
        "element":   "air",
        "modality":  "cardinal",
        "synthesis_sources": ["mehta_rao", "raphael_west"],
    },
    {
        "entity_id": "geo-sign-scorpio",
        "sign":      "scorpio",
        "sign_no":   8,
        "countries": ["Norway", "Morocco", "Algeria", "Mexico",
                      "Bavaria", "North Africa (general)"],
        "cities":    ["Liverpool", "Baltimore", "Newcastle", "Washington DC",
                      "Frankfurt", "Ghent"],
        "india_regions": ["Himachal Pradesh", "Uttarakhand", "J&K"],
        "element":   "water",
        "modality":  "fixed",
        "special_note": (
            "Scorpio-Taurus axis = primary seismic trigger (Mehta Ch 11). "
            "Major malefics in Scorpio or Taurus + eclipse = highest earthquake risk."
        ),
        "synthesis_sources": ["mehta_rao", "raphael_west"],
    },
    {
        "entity_id": "geo-sign-sagittarius",
        "sign":      "sagittarius",
        "sign_no":   9,
        "countries": ["Hungary", "Spain", "Australia (inland)", "Arabia",
                      "Madagascar"],
        "cities":    ["Cologne", "Naples", "Stuttgart", "Avignon",
                      "Toledo", "Budapest"],
        "india_regions": ["Maharashtra", "Goa", "Konkan coast"],
        "special_note": (
            "India's Trika Axis: SAGITTARIUS/Aries/Libra = 8th house of India. "
            "Sun transit through Sagittarius = India danger phase. "
            "Saturn + Ketu conjunct in Capricorn aspecting Sagittarius = 1962 China war."
        ),
        "element":   "fire",
        "modality":  "dual",
        "synthesis_sources": ["mehta_rao", "raphael_west"],
    },
    {
        "entity_id": "geo-sign-capricorn",
        "sign":      "capricorn",
        "sign_no":   10,
        "countries": ["India (Central/Northern)", "Afghanistan", "Bulgaria",
                      "Lithuania", "Mexico (mountains)"],
        "cities":    ["Oxford", "Mecklenburg", "Brandenburg", "Delhi",
                      "Brussels", "Port Said"],
        "india_regions": ["Delhi", "Rajasthan (Northern)", "Punjab-Haryana border"],
        "special_note": (
            "India's Cancer-CAPRICORN axis is the critical war axis (Mehta Ch 19). "
            "Saturn/Ketu conjunction in Capricorn on Oct 20 1962 → China war outbreak. "
            "China Foundation Chart: Capricorn Lagna (1 Oct 1949, 15:15, Peking)."
        ),
        "element":   "earth",
        "modality":  "cardinal",
        "synthesis_sources": ["mehta_rao", "raphael_west"],
    },
    {
        "entity_id": "geo-sign-aquarius",
        "sign":      "aquarius",
        "sign_no":   11,
        "countries": ["Russia", "Sweden", "Abyssinia", "Iran (northern)",
                      "Prussia"],
        "cities":    ["Hamburg", "Bremen", "Moscow", "Salzburg",
                      "Trent", "St. Petersburg"],
        "india_regions": ["Bihar (Southern)", "Jharkhand", "West Bengal (Western)"],
        "element":   "air",
        "modality":  "fixed",
        "synthesis_sources": ["mehta_rao", "raphael_west"],
    },
    {
        "entity_id": "geo-sign-pisces",
        "sign":      "pisces",
        "sign_no":   12,
        "countries": ["Portugal", "Norway (northern)", "Calabria",
                      "Egypt", "Normandy"],
        "cities":    ["Alexandria", "Compostella", "Ratisbon",
                      "Seville", "Worms"],
        "india_regions": ["Kerala", "Tamil Nadu", "Coastal South India"],
        "element":   "water",
        "modality":  "dual",
        "synthesis_sources": ["mehta_rao", "raphael_west"],
    },
]

# ── NATIONAL FOUNDATION HOROSCOPES ───────────────────────────────────────────
# These are the "National DNA" charts — the most fundamental anchor for all
# mundane predictions targeting a specific nation (Mehta Ch 2: Step 1).
# Each nation's transits and dashas are evaluated against this foundation chart.

NATIONAL_HOROSCOPES = [
    {
        "entity_id":        "nat-india",
        "nation":           "India",
        "nation_slug":      "india",
        "sovereignty_date": "1947-08-15",
        "sovereignty_time": "00:00:00",
        "sovereignty_tz":   "IST (+5:30)",
        "location":         "New Delhi",
        "lagna":            "Taurus",
        "lagna_lord":       "Venus",
        "moon_sign":        "Capricorn",
        "sun_sign":         "Cancer",
        "key_house_lords": {
            "lagna_lord":  "Venus (1st/6th)",
            "8th_lord":    "Jupiter",
            "10th_lord":   "Saturn",
        },
        "trika_axis": {
            "description": "Sagittarius/Aries/Libra = 8th/12th/6th houses of India",
            "significance": "Sun transit through Trika signs = national danger phase",
        },
        "critical_transits": {
            "cancer_capricorn_axis": "Primary war axis — more dangerous than Taurus-Scorpio",
            "rohini_gate":           "Saturn/Mars in Rohini (Taurus 10°–23°20') = war/famine threshold",
        },
        "source_books": ["Mehta Ch 3", "Gopal Ch 3/8"],
        "synthesis_sources": ["mehta_rao", "gopal_modern"],
    },
    {
        "entity_id":        "nat-pakistan",
        "nation":           "Pakistan",
        "nation_slug":      "pakistan",
        "sovereignty_date": "1947-08-14",
        "sovereignty_time": "00:00:00",
        "sovereignty_tz":   "PKT (+5:00)",
        "location":         "Karachi",
        "lagna":            "Aries",
        "lagna_lord":       "Mars",
        "rivalry_note": (
            "India (Taurus) and Pakistan (Aries) are in 2/12 relationship — "
            "nations with Lagnas in 2/12 axis cannot maintain lasting peace "
            "(Gopal Ch 8: Neighbor Rivalry Veto). This is a foundational rule "
            "for India-Pakistan predictions."
        ),
        "source_books": ["Mehta Ch 3", "Gopal Ch 8"],
        "synthesis_sources": ["mehta_rao", "gopal_modern"],
    },
    {
        "entity_id":        "nat-china",
        "nation":           "China (PRC)",
        "nation_slug":      "china",
        "sovereignty_date": "1949-10-01",
        "sovereignty_time": "15:15:00",
        "sovereignty_tz":   "CST (+8:00)",
        "location":         "Peking (Beijing)",
        "lagna":            "Capricorn",
        "lagna_lord":       "Saturn",
        "key_note": (
            "India (Taurus) and China (Capricorn) are in 1/9 trine relationship — "
            "Capricorn falls on India's 9th house (luck/dharma axis). "
            "1962 war: Saturn and Ketu conjunct at 11° Capricorn, Mars in Cancer "
            "fully aspected → outbreak on October 20."
        ),
        "source_books": ["Mehta Ch 3", "Mehta Ch 19"],
        "synthesis_sources": ["mehta_rao"],
    },
    {
        "entity_id":        "nat-usa",
        "nation":           "USA",
        "nation_slug":      "usa",
        "sovereignty_date": "1776-07-04",
        "sovereignty_time": "10:21:30",
        "sovereignty_tz":   "LMT Philadelphia",
        "location":         "Philadelphia, Pennsylvania",
        "lagna":            "Leo",
        "lagna_lord":       "Sun",
        "moon_sign":        "Aquarius",
        "sun_sign":         "Cancer",
        "key_note": (
            "Leo Lagna — USA is a 'natural king' chart. JFK assassination validation: "
            "Lagna lord Mercury (wrong — Sun rules Leo; Mercury rules 2nd/11th) "
            "conjunct 8th lord Mars in 8th, aspected by 6th lord Saturn = "
            "terminal assassination signature (JFK Gold Standard, Mehta Ch 21)."
        ),
        "source_books": ["Mehta Ch 3", "Raphael Ch 1", "Mehta Ch 21"],
        "synthesis_sources": ["mehta_rao", "raphael_west"],
    },
    {
        "entity_id":        "nat-uk",
        "nation":           "United Kingdom",
        "nation_slug":      "uk",
        "sovereignty_date": "1801-01-01",
        "sovereignty_time": "00:00:00",
        "sovereignty_tz":   "GMT",
        "location":         "London",
        "lagna":            "Libra",
        "lagna_lord":       "Venus",
        "key_note": (
            "UK traditionally assigned Aries (Raphael) or Libra (Mehta). "
            "Libra Lagna: UK is a partnership-oriented governance chart. "
            "Raphael's Aries assignment also used in Western mundane tradition."
        ),
        "source_books": ["Mehta Ch 3", "Raphael Ch 1"],
        "synthesis_sources": ["mehta_rao", "raphael_west"],
    },
    {
        "entity_id":        "nat-bangladesh",
        "nation":           "Bangladesh",
        "nation_slug":      "bangladesh",
        "sovereignty_date": "1971-03-26",
        "sovereignty_time": "00:01:00",
        "sovereignty_tz":   "BDT (+6:00)",
        "location":         "Dhaka",
        "lagna":            "Scorpio",
        "key_note": (
            "1971 war validation: Saturn retrograde in Rohini (Taurus) + Mars in Aquarius "
            "aspecting Saturn in Rohini → birth of Bangladesh / dismemberment of Pakistan. "
            "Mars (Lagna lord of Pakistan: Aries) aspected by Saturn was the critical trigger."
        ),
        "source_books": ["Mehta Ch 3", "Mehta Ch 19"],
        "synthesis_sources": ["mehta_rao"],
    },
    {
        "entity_id":        "nat-russia",
        "nation":           "Russia (Soviet/Post-Soviet)",
        "nation_slug":      "russia",
        "sovereignty_date": "1991-12-25",
        "sovereignty_time": "19:38:00",
        "sovereignty_tz":   "MSK (+3:00)",
        "location":         "Moscow",
        "lagna":            "Gemini",
        "traditional_sign": "Aquarius",
        "key_note": (
            "Traditional zodiac geography assigns Russia to Aquarius. "
            "Modern Russia (1991 dissolution) has Gemini Lagna. "
            "For transit purposes, Aquarius remains the primary national sign."
        ),
        "source_books": ["Mehta Ch 3", "Gopal Ch 3"],
        "synthesis_sources": ["mehta_rao", "gopal_modern"],
    },
    {
        "entity_id":        "nat-independent-india-annual",
        "nation":           "India — Annual Hindu New Year Reference",
        "nation_slug":      "india_annual",
        "chart_type":       "Hindu_New_Year_Reference",
        "key_note": (
            "The Hindu New Year (Chaitra Shukla Pratipada) chart is cast annually "
            "for New Delhi as the primary mundane forecast vehicle for India. "
            "This entity records the chart TYPE, not a specific year's chart. "
            "Each annual chart is evaluated against India's Foundation Chart (nat-india). "
            "The Celestial Council (King, Minister, etc.) is re-appointed each year "
            "based on the weekday lord of the relevant ingress. See mundane_engine_specs."
        ),
        "evaluation_protocol": (
            "Step 1 of Mehta's 9-Step Scheme. Foundation Chart is the DNA; "
            "Hindu New Year is the annual manifestation layer."
        ),
        "source_books": ["Mehta Ch 2", "Gaur Ch 1/2"],
        "synthesis_sources": ["mehta_rao", "gaur_aifas"],
    },
]


# ── Document builder ─────────────────────────────────────────────────────────

def build_koorma_docs(now: str) -> list[dict]:
    docs = []
    for z in KOORMA_ZONES:
        doc = {
            "entity_id":   z["entity_id"],
            "entity_type": "koorma_zone",
            "source": {
                "science":           SCIENCE,
                "framework":         "Koorma Chakra",
                "primary_chapter":   "Gaur Ch 4/5 + Mehta Ch 7",
                "batch_id":          BATCH_ID,
                "synthesis_sources": z["synthesis_sources"],
            },
            "zone_key":   z["zone_key"],
            "body_part":  z["body_part"],
            "direction":  z["direction"],
            "nakshatras": z["nakshatras"],
            "created_at": now,
            "updated_at": now,
        }
        if "special_note" in z:
            doc["special_note"] = z["special_note"]
        docs.append(doc)
    return docs


def build_zodiac_docs(now: str) -> list[dict]:
    docs = []
    for s in ZODIAC_GEOGRAPHY:
        doc = {
            "entity_id":   s["entity_id"],
            "entity_type": "zodiac_geography",
            "source": {
                "science":           SCIENCE,
                "framework":         "Zodiac Geography",
                "primary_chapter":   "Mehta Ch 3 + Gopal Ch 3 + Raphael Ch 1",
                "batch_id":          BATCH_ID,
                "synthesis_sources": s["synthesis_sources"],
            },
            "sign":           s["sign"],
            "sign_no":        s["sign_no"],
            "element":        s["element"],
            "modality":       s["modality"],
            "countries":      s["countries"],
            "cities":         s["cities"],
            "india_regions":  s.get("india_regions", []),
            "created_at":     now,
            "updated_at":     now,
        }
        if "special_note" in s:
            doc["special_note"] = s["special_note"]
        docs.append(doc)
    return docs


def build_national_docs(now: str) -> list[dict]:
    docs = []
    for n in NATIONAL_HOROSCOPES:
        doc = {
            "entity_id":   n["entity_id"],
            "entity_type": "national_foundation_chart",
            "source": {
                "science":           SCIENCE,
                "framework":         "National Foundation Chart",
                "primary_chapter":   ", ".join(n.get("source_books", [])),
                "batch_id":          BATCH_ID,
                "synthesis_sources": n.get("synthesis_sources", []),
            },
            "nation":       n["nation"],
            "nation_slug":  n["nation_slug"],
            "created_at":   now,
            "updated_at":   now,
        }
        for field in ["sovereignty_date", "sovereignty_time", "sovereignty_tz",
                      "location", "lagna", "lagna_lord", "moon_sign", "sun_sign",
                      "chart_type", "traditional_sign", "key_house_lords",
                      "trika_axis", "critical_transits", "rivalry_note",
                      "key_note", "evaluation_protocol"]:
            if field in n:
                doc[field] = n[field]
        docs.append(doc)
    return docs


def build_all(now: str) -> list[dict]:
    docs = []
    docs.extend(build_koorma_docs(now))
    docs.extend(build_zodiac_docs(now))
    docs.extend(build_national_docs(now))
    return docs


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run",  action="store_true")
    parser.add_argument("--save",     help="Path to write JSON")
    parser.add_argument("--upload",   help="Path to JSON for upload")
    parser.add_argument("--mongo-url")
    parser.add_argument("--db-name",  default="horoscope_db")
    args = parser.parse_args()

    now  = datetime.now(timezone.utc).isoformat()
    docs = build_all(now)

    if args.dry_run or args.save:
        by_type: dict[str, int] = {}
        for d in docs:
            et = d["entity_type"]
            by_type[et] = by_type.get(et, 0) + 1

        print(f"Built {len(docs)} documents for batch {BATCH_ID}")
        print(f"Target collection: {COLL_NAME}\n")
        print("Breakdown by entity_type:")
        for et, count in sorted(by_type.items()):
            print(f"  {et:<35}: {count}")
        print("\nEntity IDs:")
        for d in docs:
            print(f"  {d['entity_id']}")

        if args.save:
            with open(args.save, "w") as f:
                json.dump(docs, f, indent=2, default=str)
            print(f"\nSaved → {args.save}")
        print("\nDry run complete.")
        return

    if args.upload:
        if not args.mongo_url:
            raise SystemExit("ERROR: --mongo-url is required with --upload")
        with open(args.upload) as f:
            docs = json.load(f)

        client   = MongoClient(args.mongo_url)
        col      = client[args.db_name][COLL_NAME]
        inserted = updated = 0
        for doc in docs:
            result = col.update_one(
                {"entity_id": doc["entity_id"]},
                {"$set":      doc},
                upsert=True,
            )
            if result.upserted_id:
                inserted += 1
            elif result.modified_count:
                updated += 1
        print(f"Loaded {len(docs)} documents from {args.upload}")
        print(f"Inserted {inserted} / Updated {updated} → {args.db_name}.{COLL_NAME}")
        client.close()


if __name__ == "__main__":
    main()
