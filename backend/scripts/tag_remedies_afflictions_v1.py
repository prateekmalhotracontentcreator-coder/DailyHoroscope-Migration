#!/usr/bin/env python3
"""
tag_remedies_afflictions_v1.py -- Multi-Parameter Remedy Tagging Script
=======================================================================
Adds SEO and affliction tags to all remedy documents across all collections.

Collections touched:
  horoscope_db.interpretation_rules  (science_ids: mantras, gemstones, crystals, dhana, chakra)
  horoscope_db.knowledge_rules       (science_id: jyotish_lk_remedies)

Tags added per document:
  affliction_tags:  [list]  -- which of the 12 doshas this remedy addresses
  seo_focus_area:   [list]  -- 12 Areas of Life (Career, Love, etc.)
  seo_problem_area: [list]  -- specific problems (Marriage, Job Loss, etc.)
  seo_planet_remedy:[list]  -- canonical planet(s) this remedy targets
  seo_zodiac_sign:  [list]  -- applicable zodiac signs
  remedy_type:      str     -- mantra | gemstone | crystal | donation | ritual | lk_ritual

Usage:
  # Dry-run: prints stats only
  python3 scripts/tag_remedies_afflictions_v1.py --dry-run

  # Apply tags to MongoDB
  python3 scripts/tag_remedies_afflictions_v1.py \
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  # Save tagged JSON for review before uploading
  python3 scripts/tag_remedies_afflictions_v1.py --dry-run \
      --save scripts/tagged_remedies_preview.json

Issued: 2026-05-22
Commission: SEO-20K Batch 9 -- Remedy Hub Pages
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# ─────────────────────────────────────────────────────────────────────────────
# 12 AFFLICTIONS (Batch 9 hub page slugs)
# ─────────────────────────────────────────────────────────────────────────────
AFFLICTIONS = [
    "shani-sade-sati",
    "manglik-dosha",
    "pitru-dosha",
    "kaal-sarp-dosha",
    "shani-mahadasha",
    "rahu-mahadasha",
    "ketu-mahadasha",
    "guru-chandal-yoga",
    "grahan-yoga",
    "nadi-dosha",
    "gana-dosha",
    "bhakoot-dosha",
]

# ─────────────────────────────────────────────────────────────────────────────
# 12 AREAS OF LIFE → SEO Focus Area Labels
# ─────────────────────────────────────────────────────────────────────────────
FOCUS_AREAS = [
    "Health & Fitness",
    "Career & Work",
    "Finances",
    "Intellectual Life",
    "Emotional Life",
    "Spirituality",
    "Love Relationships",
    "Family Life",
    "Social Life",
    "Adventure & Travel",
    "Environment",
    "Creativity & Hobbies",
]

# ─────────────────────────────────────────────────────────────────────────────
# PLANET → ZODIAC SIGNS (owned/exalted -- for sign tagging)
# ─────────────────────────────────────────────────────────────────────────────
PLANET_SIGNS: dict[str, list[str]] = {
    "Sun":     ["Leo", "Aries"],
    "Moon":    ["Cancer", "Taurus"],
    "Mars":    ["Aries", "Scorpio", "Capricorn"],
    "Mercury": ["Gemini", "Virgo"],
    "Jupiter": ["Sagittarius", "Pisces", "Cancer"],
    "Venus":   ["Taurus", "Libra", "Pisces"],
    "Saturn":  ["Capricorn", "Aquarius", "Libra"],
    "Rahu":    ["Gemini", "Virgo", "Taurus"],
    "Ketu":    ["Sagittarius", "Pisces", "Scorpio"],
}

# ─────────────────────────────────────────────────────────────────────────────
# AFFLICTION DETECTION RULES
# Each affliction has keyword patterns checked against:
#   - interpretation.summary / focus_area
#   - condition.trigger_tags
#   - primary_planet
#   - condition.astrological_mapping.planet
# ─────────────────────────────────────────────────────────────────────────────
AFFLICTION_RULES: dict[str, dict] = {
    "shani-sade-sati": {
        "planets":   {"Saturn"},
        "keywords":  {"sade sati", "shani sade", "saturn transit", "delay", "karma", "saturn 12th",
                      "saturn 1st", "saturn 2nd", "obstruction", "obstacles", "shani"},
        "trigger_tags": {"shani_sade_sati", "saturn_transit_12_1_2", "saturn_affliction",
                         "delay_karma", "saturn_debilitated", "low_shadbala_saturn"},
        "focus_kws": {"delay", "karma", "obstacle", "saturn", "shani", "sorrow"},
    },
    "manglik-dosha": {
        "planets":   {"Mars"},
        "keywords":  {"manglik", "mangal dosha", "mars afflict", "mars debil", "mars 1st", "mars 4th",
                      "mars 7th", "mars 8th", "mars 12th", "kuja dosha"},
        "trigger_tags": {"mangal_dosha", "mars_debilitated", "low_shadbala_mars", "mars_combust",
                         "mars_1_4_7_8_12", "kuja_dosha"},
        "focus_kws": {"marriage delay", "relationship conflict", "anger", "accident", "mars"},
    },
    "pitru-dosha": {
        "planets":   {"Sun", "Saturn", "Rahu"},
        "keywords":  {"pitru", "ancestor", "ancestral", "pitra", "father", "forefathers",
                      "ancestral debt", "pitru rin", "ancestral curse", "ancestral blessing",
                      "priest curse"},
        "trigger_tags": {"ancestor_blessing", "ancestral_wealth", "pitru_dosha", "sun_6_8_12",
                         "ancestral_debt"},
        "focus_kws": {"ancestor", "pitru", "father", "ancestral", "pitra"},
    },
    "kaal-sarp-dosha": {
        "planets":   {"Rahu", "Ketu"},
        "keywords":  {"kaal sarp", "kal sarp", "kalsarp", "eclipse birth", "rahu ketu axis",
                      "serpent", "naga", "snake"},
        "trigger_tags": {"kaal_sarp", "eclipse_birth", "rahu_ketu_opposition", "rahu_debilitated",
                         "ketu_affliction"},
        "focus_kws": {"kaal sarp", "eclipse", "rahu", "ketu"},
    },
    "shani-mahadasha": {
        "planets":   {"Saturn"},
        "keywords":  {"saturn mahadasha", "shani mahadasha", "saturn dasha", "saturn period",
                      "19 year", "delay", "discipline", "hard work"},
        "trigger_tags": {"saturn_mahadasha", "shani_dasha", "saturn_affliction", "delay_karma",
                         "low_shadbala_saturn", "saturn_debilitated"},
        "focus_kws": {"saturn", "shani", "delay", "discipline", "karma"},
    },
    "rahu-mahadasha": {
        "planets":   {"Rahu"},
        "keywords":  {"rahu mahadasha", "rahu dasha", "18 year rahu", "north node", "confusion",
                      "illusion", "foreign", "obsession", "shadow planet"},
        "trigger_tags": {"rahu_mahadasha", "rahu_dasha", "rahu_affliction", "rahu_debilitated",
                         "confusion_obsession"},
        "focus_kws": {"rahu", "confusion", "illusion", "foreign", "obsession"},
    },
    "ketu-mahadasha": {
        "planets":   {"Ketu"},
        "keywords":  {"ketu mahadasha", "ketu dasha", "7 year ketu", "south node", "detachment",
                      "moksha", "spirituality", "liberation"},
        "trigger_tags": {"ketu_mahadasha", "ketu_dasha", "ketu_affliction", "detachment_moksha"},
        "focus_kws": {"ketu", "detachment", "moksha", "spirituality", "liberation"},
    },
    "guru-chandal-yoga": {
        "planets":   {"Jupiter", "Rahu"},
        "keywords":  {"guru chandal", "jupiter rahu", "chandal yoga", "jupiter conjunct rahu",
                      "corrupted guru", "false teacher"},
        "trigger_tags": {"guru_chandal", "jupiter_rahu_conjunction", "jupiter_combust"},
        "focus_kws": {"guru chandal", "jupiter rahu", "teacher", "mentor", "wisdom"},
        "planet_combos": {frozenset({"Jupiter", "Rahu"})},
    },
    "grahan-yoga": {
        "planets":   {"Sun", "Moon", "Rahu", "Ketu"},
        "keywords":  {"grahan", "eclipse", "solar eclipse", "lunar eclipse", "sun rahu", "moon rahu",
                      "sun ketu", "moon ketu"},
        "trigger_tags": {"eclipse_birth", "grahan_yoga", "kaal_sarp", "sun_rahu_conjunction"},
        "focus_kws": {"eclipse", "grahan", "sun rahu", "moon rahu"},
        "planet_combos": {frozenset({"Sun", "Rahu"}), frozenset({"Moon", "Rahu"}),
                          frozenset({"Sun", "Ketu"}), frozenset({"Moon", "Ketu"})},
    },
    "nadi-dosha": {
        "planets":   {"Mercury", "Moon"},
        "keywords":  {"nadi", "compatibility", "marriage matching", "gun milan", "ashta koota",
                      "health compatibility"},
        "trigger_tags": {"nadi_dosha", "compatibility", "marriage_matching"},
        "focus_kws": {"nadi", "marriage", "compatibility"},
    },
    "gana-dosha": {
        "planets":   {"Moon", "Jupiter"},
        "keywords":  {"gana", "deva gana", "manushya gana", "rakshasa gana", "temperament",
                      "nature compatibility"},
        "trigger_tags": {"gana_dosha", "temperament_mismatch"},
        "focus_kws": {"gana", "temperament", "compatibility"},
    },
    "bhakoot-dosha": {
        "planets":   {"Moon"},
        "keywords":  {"bhakoot", "moon sign compatibility", "rashikoot", "moon compatibility"},
        "trigger_tags": {"bhakoot_dosha", "moon_sign_mismatch"},
        "focus_kws": {"bhakoot", "moon sign", "compatibility"},
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# FOCUS AREA MAPPING RULES
# ─────────────────────────────────────────────────────────────────────────────
FOCUS_AREA_KEYWORDS: dict[str, list[str]] = {
    "Career & Work":       ["career", "job", "promotion", "business", "professional", "work",
                            "success", "leadership", "contract", "competitive exam"],
    "Finances":            ["wealth", "money", "finance", "debt", "abundance", "prosperity",
                            "income", "property", "asset", "dhana", "lakshmi", "kubera"],
    "Love Relationships":  ["love", "relationship", "partner", "attraction", "romance",
                            "marriage", "spouse", "soulmate", "union", "affection"],
    "Family Life":         ["family", "child", "fertility", "home", "domestic", "ancestor",
                            "parent", "mother", "father", "pitru", "ancestral"],
    "Health & Fitness":    ["health", "healing", "disease", "illness", "chronic", "bone",
                            "digestive", "skin", "eye", "vitality", "energy", "strength"],
    "Spirituality":        ["spiritual", "moksha", "detachment", "liberation", "meditation",
                            "mantra", "yantra", "prayer", "divine", "god", "deity", "ketu",
                            "protection", "aura", "chakra"],
    "Emotional Life":      ["emotional", "anxiety", "fear", "depression", "peace", "mental",
                            "calm", "stress", "clarity", "mind", "confidence"],
    "Intellectual Life":   ["academic", "education", "study", "learning", "intelligence",
                            "concentration", "exam", "knowledge", "wisdom", "mercury"],
    "Social Life":         ["friendship", "social", "ally", "network", "community", "trust",
                            "conflict", "enemy"],
    "Creativity & Hobbies":["creativity", "art", "artistic", "music", "talent", "expression"],
    "Adventure & Travel":  ["travel", "foreign", "journey", "adventure", "abroad", "overseas"],
    "Environment":         ["home", "space", "environment", "vastu", "land", "property"],
}

# ─────────────────────────────────────────────────────────────────────────────
# PROBLEM AREA MAPPING
# ─────────────────────────────────────────────────────────────────────────────
PROBLEM_AREA_KEYWORDS: dict[str, list[str]] = {
    "Marriage Delay":       ["marriage delay", "delayed marriage", "early marriage", "late marriage",
                             "marriage obstacle"],
    "Job Loss":             ["job loss", "career setback", "career block", "professional downfall"],
    "Financial Loss":       ["financial loss", "debt", "poverty", "bankruptcy"],
    "Health Crisis":        ["chronic disease", "fatal illness", "accident", "injury", "bone"],
    "Relationship Conflict":["relationship conflict", "divorce", "separation", "partner conflict"],
    "Ancestral Karma":      ["ancestral debt", "pitru dosha", "ancestor curse", "karmic debt"],
    "Mental Distress":      ["anxiety", "depression", "fear", "mental illness", "confusion",
                             "obsession", "stress"],
    "Enemy & Opposition":   ["enemy", "black magic", "evil eye", "nazar", "opposition"],
    "Child & Fertility":    ["fertility", "child", "pregnancy", "conception"],
    "Business Failure":     ["business loss", "business failure", "financial obstacle"],
    "Foreign Settlement":   ["foreign land", "abroad", "immigration", "overseas"],
    "Spiritual Blockage":   ["spiritual block", "eclipse birth", "kaal sarp", "rahu ketu"],
}

# ─────────────────────────────────────────────────────────────────────────────
# REMEDY TYPE MAPPING (by science_id)
# ─────────────────────────────────────────────────────────────────────────────
REMEDY_TYPE_MAP = {
    "jyotish_remedies_mantras":  "mantra",
    "jyotish_remedies_gemstones":"gemstone",
    "jyotish_remedies_crystals": "crystal",
    "jyotish_remedies_dhana":    "donation",
    "jyotish_remedies_chakra":   "chakra_ritual",
    "jyotish_lk_remedies":       "lk_ritual",
}


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _text_blob(doc: dict) -> str:
    """Extract all searchable text from a remedy document."""
    parts = []
    # Mantras / gemstones / crystals / dhana / chakra (interpretation_rules schema)
    interp = doc.get("interpretation", {})
    if interp:
        parts.append(str(interp.get("summary", "")))
        parts.append(str(interp.get("detailed", "")))
    cond = doc.get("condition", {})
    if cond:
        parts.append(str(cond.get("yoga_name", "")))
        parts.append(str(cond.get("trigger_condition", "")))
        parts.extend(cond.get("trigger_tags", []))
        astr = cond.get("astrological_mapping", {})
        if isinstance(astr, dict):
            parts.extend(astr.get("planet", []))
    # LK remedies (knowledge_rules schema)
    parts.append(str(doc.get("focus_area", "")))
    parts.append(str(doc.get("primary_planet", "")))
    parts.append(str(doc.get("ke_inference", "")))
    parts.append(str(doc.get("trigger_ke_inference", "")))
    return " ".join(parts).lower()


def _get_planets(doc: dict) -> set[str]:
    """Extract canonical planet names from document."""
    planets = set()
    cond = doc.get("condition", {})
    astr = cond.get("astrological_mapping", {}) if cond else {}
    for p in astr.get("planet", []):
        planets.add(p)
    for p in doc.get("condition", {}).get("planets_involved", []):
        planets.add(p)
    # LK schema
    raw = str(doc.get("primary_planet", ""))
    CANONICAL = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
                 "Saturn", "Rahu", "Ketu"}
    for cp in CANONICAL:
        if cp.lower() in raw.lower():
            planets.add(cp)
    return planets


def _get_trigger_tags(doc: dict) -> set[str]:
    return set(doc.get("condition", {}).get("trigger_tags", []))


def _detect_afflictions(doc: dict) -> list[str]:
    """Return list of affliction slugs this remedy addresses."""
    blob = _text_blob(doc)
    planets = _get_planets(doc)
    tags = _get_trigger_tags(doc)
    matched = []

    for affliction, rules in AFFLICTION_RULES.items():
        score = 0

        # Planet match
        if planets & rules.get("planets", set()):
            score += 2

        # Planet combo match (e.g. Jupiter+Rahu for Guru Chandal)
        combos = rules.get("planet_combos", set())
        for combo in combos:
            if combo.issubset(planets):
                score += 3

        # Trigger tag match
        if tags & rules.get("trigger_tags", set()):
            score += 3

        # Keyword match in blob
        kws = rules.get("keywords", set()) | rules.get("focus_kws", set())
        matched_kws = sum(1 for kw in kws if kw in blob)
        score += matched_kws

        if score >= 2:
            matched.append(affliction)

    return matched


def _detect_focus_areas(doc: dict) -> list[str]:
    blob = _text_blob(doc)
    matched = []
    for area, kws in FOCUS_AREA_KEYWORDS.items():
        if any(kw in blob for kw in kws):
            matched.append(area)
    return matched or ["Spirituality"]  # default


def _detect_problem_areas(doc: dict) -> list[str]:
    blob = _text_blob(doc)
    matched = []
    for area, kws in PROBLEM_AREA_KEYWORDS.items():
        if any(kw in blob for kw in kws):
            matched.append(area)
    return matched


def _detect_zodiac_signs(doc: dict) -> list[str]:
    planets = _get_planets(doc)
    signs = set()
    for p in planets:
        signs.update(PLANET_SIGNS.get(p, []))
    return sorted(signs)


def _get_remedy_type(doc: dict) -> str:
    science_id = doc.get("science_id", "")
    return REMEDY_TYPE_MAP.get(science_id, "ritual")


def tag_document(doc: dict) -> dict:
    """Add all SEO + affliction tags to a remedy document (returns copy)."""
    tagged = dict(doc)
    tagged["affliction_tags"]   = _detect_afflictions(doc)
    tagged["seo_focus_area"]    = _detect_focus_areas(doc)
    tagged["seo_problem_area"]  = _detect_problem_areas(doc)
    tagged["seo_planet_remedy"] = sorted(_get_planets(doc))
    tagged["seo_zodiac_sign"]   = _detect_zodiac_signs(doc)
    tagged["remedy_type"]       = _get_remedy_type(doc)
    return tagged


# ─────────────────────────────────────────────────────────────────────────────
# LOAD LOCAL JSON FILES (for offline dry-run without MongoDB)
# ─────────────────────────────────────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).parent

LOCAL_JSON_FILES = {
    "interpretation_rules": [
        SCRIPTS_DIR / "remedies_rules.json",       # mantras (100)
        # gemstone_rules.json, crystal_rules.json, dhana_rules.json, chakra_rules.json
        # generated by their respective ingest scripts with --dry-run --save
    ],
    "knowledge_rules": [
        SCRIPTS_DIR / "lk_remedies.json",           # LK (361)
    ],
}


def load_local_docs() -> list[dict]:
    docs = []
    for collection, paths in LOCAL_JSON_FILES.items():
        for path in paths:
            if path.exists():
                batch = json.loads(path.read_text())
                if isinstance(batch, list):
                    for d in batch:
                        d["_source_collection"] = collection
                    docs.extend(batch)
                    print(f"  Loaded {len(batch)} docs from {path.name}")
                else:
                    print(f"  ⚠️  {path.name} is not a JSON array -- skipped")
            else:
                print(f"  ⚠️  {path} not found -- skipped")
    return docs


# ─────────────────────────────────────────────────────────────────────────────
# MONGODB UPLOAD
# ─────────────────────────────────────────────────────────────────────────────
def apply_tags_to_mongo(mongo_url: str, db_name: str) -> None:
    try:
        from pymongo import MongoClient, UpdateOne
    except ImportError:
        print("ERROR: pymongo not installed. Run: pip install pymongo")
        sys.exit(1)

    client = MongoClient(mongo_url)
    db = client[db_name]

    REMEDY_SCIENCE_IDS = [
        "jyotish_remedies_mantras",
        "jyotish_remedies_gemstones",
        "jyotish_remedies_crystals",
        "jyotish_remedies_dhana",
        "jyotish_remedies_chakra",
    ]

    total_updated = 0

    # --- interpretation_rules ---
    col = db["interpretation_rules"]
    docs = list(col.find({"science_id": {"$in": REMEDY_SCIENCE_IDS}}))
    print(f"\ninterpretation_rules: {len(docs)} remedy docs found")
    ops = []
    for doc in docs:
        tagged = tag_document(doc)
        ops.append(UpdateOne(
            {"_id": doc["_id"]},
            {"$set": {
                "affliction_tags":   tagged["affliction_tags"],
                "seo_focus_area":    tagged["seo_focus_area"],
                "seo_problem_area":  tagged["seo_problem_area"],
                "seo_planet_remedy": tagged["seo_planet_remedy"],
                "seo_zodiac_sign":   tagged["seo_zodiac_sign"],
                "remedy_type":       tagged["remedy_type"],
            }}
        ))
    if ops:
        result = col.bulk_write(ops)
        print(f"  Updated {result.modified_count} / {len(ops)} docs")
        total_updated += result.modified_count

    # --- knowledge_rules (LK) ---
    col2 = db["knowledge_rules"]
    lk_docs = list(col2.find({"science_id": "jyotish_lk_remedies"}))
    print(f"\nknowledge_rules (LK): {len(lk_docs)} remedy docs found")
    ops2 = []
    for doc in lk_docs:
        tagged = tag_document(doc)
        ops2.append(UpdateOne(
            {"_id": doc["_id"]},
            {"$set": {
                "affliction_tags":   tagged["affliction_tags"],
                "seo_focus_area":    tagged["seo_focus_area"],
                "seo_problem_area":  tagged["seo_problem_area"],
                "seo_planet_remedy": tagged["seo_planet_remedy"],
                "seo_zodiac_sign":   tagged["seo_zodiac_sign"],
                "remedy_type":       tagged["remedy_type"],
            }}
        ))
    if ops2:
        result2 = col2.bulk_write(ops2)
        print(f"  Updated {result2.modified_count} / {len(ops2)} docs")
        total_updated += result2.modified_count

    print(f"\n✅ Total updated: {total_updated} remedy documents")
    client.close()


# ─────────────────────────────────────────────────────────────────────────────
# REPORT
# ─────────────────────────────────────────────────────────────────────────────
def print_stats(tagged_docs: list[dict]) -> None:
    print("\n" + "=" * 60)
    print("REMEDY TAGGING STATS")
    print("=" * 60)

    affliction_counts: dict[str, int] = {a: 0 for a in AFFLICTIONS}
    focus_counts: dict[str, int] = {}
    untagged_affliction = 0

    for doc in tagged_docs:
        aff = doc.get("affliction_tags", [])
        if not aff:
            untagged_affliction += 1
        for a in aff:
            affliction_counts[a] = affliction_counts.get(a, 0) + 1
        for fa in doc.get("seo_focus_area", []):
            focus_counts[fa] = focus_counts.get(fa, 0) + 1

    print(f"\nTotal docs tagged: {len(tagged_docs)}")
    print(f"Docs with no affliction match: {untagged_affliction}")

    print("\n── Affliction Coverage ──────────────────────────────────")
    for a in AFFLICTIONS:
        bar = "█" * min(affliction_counts.get(a, 0), 50)
        print(f"  {a:<30} {affliction_counts.get(a, 0):>4}  {bar}")

    print("\n── SEO Focus Area Coverage ──────────────────────────────")
    for fa in FOCUS_AREAS:
        bar = "█" * min(focus_counts.get(fa, 0), 50)
        print(f"  {fa:<30} {focus_counts.get(fa, 0):>4}  {bar}")

    print("=" * 60)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-parameter remedy tagging script")
    parser.add_argument("--dry-run", action="store_true",
                        help="Load local JSON files, tag, print stats -- no DB writes")
    parser.add_argument("--mongo-url", default="",
                        help="MongoDB connection string (required unless --dry-run)")
    parser.add_argument("--db-name", default="horoscope_db",
                        help="MongoDB database name (default: horoscope_db)")
    parser.add_argument("--save", metavar="PATH",
                        help="Save tagged docs to JSON file (use with --dry-run)")
    args = parser.parse_args()

    if args.dry_run or not args.mongo_url:
        print("=== DRY RUN -- loading local JSON files ===\n")
        docs = load_local_docs()
        print(f"\nTagging {len(docs)} documents...")
        tagged = [tag_document(d) for d in docs]
        print_stats(tagged)
        if args.save:
            Path(args.save).write_text(json.dumps(tagged, indent=2, ensure_ascii=False))
            print(f"\nSaved tagged output → {args.save}")
    else:
        print(f"=== APPLYING TAGS TO MONGODB: {args.db_name} ===")
        apply_tags_to_mongo(args.mongo_url, args.db_name)
        print("\nDone. Run with --dry-run to verify coverage stats first.")


if __name__ == "__main__":
    main()
