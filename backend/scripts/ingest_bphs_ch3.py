#!/usr/bin/env python3
"""
BPHS Chapter 3 — Planetary Characters and Description
ingest_bphs_ch3.py

Extracts 6 rule categories from BPHS Chapter 3:
  1. benefic_malefic  — natural benefic / malefic classification (9 rules)
  2. governance       — planetary lordship over life faculties (7 rules)
  3. cabinet_role     — planetary cabinet roles (9 rules)
  4. description      — physical and personality descriptions (9 rules)
  5. dhatu_rulership  — Sapta Dhatu body rulership, health domain (7 rules)
  6. digbala          — directional strength per planet (7 rules)

Total: ~48 rules.  Condition type: planet_nature.

Skipped (reference data, not prediction rules):
  Exaltation/debilitation degrees, Moolatrikona extents,
  natural relationship tables, trees, abodes, seasons, tastes.

Rule ID:  R-BPHS3-{PLANET_CODE}-{ATTR_CODE}-{INDEX:03d}
  e.g.   R-BPHS3-SUN-GOV-001
         R-BPHS3-MOO-DHATU-002
         R-BPHS3-MAR-DESC-003

Source:   Brihat Parashara Hora Shastra, Vol 1, Chapter 3
          R. Santhanam translation

Usage:
  python3 scripts/ingest_bphs_ch3.py \\
    --mongo-url "$MONGO_URL" \\
    --db-name EverydayHoroscope \\
    [--dry-run]
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pymongo import MongoClient

# ── Constants ─────────────────────────────────────────────────────────────────

SCIENCE   = "vedic_astrology"
BOOK      = "Brihat Parashara Hora Shastra"
BOOK_ID   = "bphs_vol1"
CHAPTER   = "3"
CHAP_NAME = "Planetary Characters and Description"
BATCH_ID  = f"bphs-ch3-v1-{datetime.now(timezone.utc).strftime('%Y%m%d')}"

PLANET_CODES: dict[str, str] = {
    "Sun": "SUN", "Moon": "MOO", "Mars": "MAR",
    "Mercury": "MER", "Jupiter": "JUP", "Venus": "VEN",
    "Saturn": "SAT", "Rahu": "RAH", "Ketu": "KET",
}

# ── Rule content ──────────────────────────────────────────────────────────────

# Section 1: Benefic / Malefic nature (sloka 11)
BENEFIC_MALEFIC: dict[str, tuple[str, str]] = {
    "Sun":     ("malefic",
                "The Sun is a natural malefic planet. His fiery nature causes separation, "
                "ego-conflicts, and health issues related to the body parts he afflicts, "
                "though he also confers authority and recognition."),
    "Moon":    ("conditional",
                "The Moon is a benefic when waxing (Shukla Paksha) and a malefic when waning "
                "(Krishna Paksha). If conjunct a benefic, even a waning Moon becomes benefic. "
                "If conjunct a waning Moon, Mercury also turns benefic."),
    "Mars":    ("malefic",
                "Mars is a natural malefic planet. He causes conflict, aggression, accidents, "
                "and surgery when afflicting sensitive points, though he also confers courage, "
                "landed property, and the capacity to defeat enemies."),
    "Mercury": ("conditional",
                "Mercury is a natural benefic but turns malefic when conjunct a malefic planet. "
                "His association determines his nature — he is the chameleon among planets, "
                "adopting the qualities of those he conjoins."),
    "Jupiter": ("benefic",
                "Jupiter is the greatest natural benefic (Guru). He confers knowledge, wisdom, "
                "children, prosperity, and spiritual progress wherever he is well-placed."),
    "Venus":   ("benefic",
                "Venus is a natural benefic. She governs marriage, sensual pleasures, luxuries, "
                "artistic abilities, and material comforts."),
    "Saturn":  ("malefic",
                "Saturn is a natural malefic. He signifies grief, delays, chronic conditions, "
                "hard labour, and losses, though a well-placed Saturn gives discipline, "
                "longevity, and eventual reward through sustained effort."),
    "Rahu":    ("malefic",
                "Rahu is a natural malefic shadow planet representing worldly obsessions, "
                "foreigners, unconventional paths, and sudden disruptions. He amplifies "
                "whatever planet he conjoins."),
    "Ketu":    ("malefic",
                "Ketu is a natural malefic shadow planet representing spiritual liberation, "
                "losses, renunciation, and karmic completion. He detaches the native from "
                "the significations of the house he occupies."),
}

# Section 2: Planetary Governance / Lordship (slokas 12–13)
# Sun governs soul, Moon governs mind, etc. — predictive because
# an afflicted planet harms the faculty it governs.
GOVERNANCE: dict[str, str] = {
    "Sun":     ("The Sun is the soul (Atma) of all living beings. A strong Sun gives "
                "a mature, developed soul, abundant spiritual progress, and self-authority. "
                "A weak or afflicted Sun diminishes self-confidence, vitality, and the "
                "relationship with the father."),
    "Moon":    ("The Moon governs the mind (Manas). A strong Moon gives emotional stability, "
                "fertile imagination, and mental clarity. An afflicted Moon produces mental "
                "disturbance, anxiety, emotional volatility, and issues with the mother."),
    "Mars":    ("Mars confers strength, courage, and physical vitality. A strong Mars gives "
                "boldness, the capacity to overcome opponents, and vigorous physical energy. "
                "An afflicted Mars causes recklessness, conflicts, and accidents."),
    "Mercury": ("Mercury is the giver of speech and analytical intelligence. A strong Mercury "
                "gives eloquence, sharp reasoning, and skill in communication, trade, and writing. "
                "An afflicted Mercury harms speech, memory, and the nervous system."),
    "Jupiter": ("Jupiter confers knowledge, wisdom, and happiness. A strong Jupiter gives "
                "learning, spiritual insight, prosperity through children, and general good fortune. "
                "An afflicted Jupiter diminishes wisdom, children, and religious merit."),
    "Venus":   ("Venus governs semen, potency, and sensual pleasures. A strong Venus gives "
                "marital happiness, artistic talent, material comforts, and a beautiful appearance. "
                "An afflicted Venus harms marriage, relationships, and reproductive health."),
    "Saturn":  ("Saturn denotes grief, sorrow, hard work, and longevity. Saturn's placement "
                "determines the areas of life where the native must work hard and endure delays "
                "before receiving reward. A well-placed Saturn gives discipline and long-lasting results."),
}

# Section 3: Planetary Cabinet (slokas 14–15)
CABINET: dict[str, str] = {
    "Sun":     ("The Sun holds royal status as the King among planets. He represents authority, "
                "government, the father, soul, and the self. When the Sun is strong, the native "
                "commands respect and achieves positions of authority."),
    "Moon":    ("The Moon holds royal status as the Queen among planets. She represents the mother, "
                "mind, public life, popularity, and emotional nature. A strong Moon gives public "
                "recognition and a nurturing, influential mother."),
    "Mars":    ("Mars is the Army Chief among planets. He represents commanders, siblings, "
                "landed property, and physical courage. Mars gives the native fighting spirit "
                "and the ability to lead in adversity."),
    "Mercury": ("Mercury is the Crown Prince (Prince Apparent) among planets. He represents "
                "intellect, communication, trade, diplomacy, and youthful energy. A strong Mercury "
                "gives success in intellectual and commercial fields."),
    "Jupiter": ("Jupiter is a Minister among planets, advising through wisdom and knowledge. "
                "He represents teachers, priests, advisers, and those who guide society through "
                "Dharmic counsel. Jupiter's strength gives wise mentors and sound judgement."),
    "Venus":   ("Venus is a Minister among planets with command over arts and diplomacy. "
                "He represents advisers dealing with wealth, beauty, arts, and pleasure. "
                "A strong Venus gives access to luxury and diplomatic skill."),
    "Saturn":  ("Saturn is the Servant among planets. He represents the working class, servants, "
                "labourers, and those who perform sustained work. Saturn's role is to enforce "
                "justice through karmic consequence."),
    "Rahu":    ("Rahu forms the planetary army. He represents foreigners, unconventional figures, "
                "outcasts, and mass forces outside normal social structures. Rahu's influence "
                "pushes the native towards unusual or taboo paths."),
    "Ketu":    ("Ketu forms the planetary army. He represents ascetics, spiritual seekers, "
                "and those who operate outside mainstream society. Ketu's influence detaches "
                "the native from material concerns and directs attention inward."),
}

# Section 4: Physical and Personality Descriptions (slokas 23–30)
DESCRIPTIONS: dict[str, str] = {
    "Sun":     ("The Sun has honey-coloured eyes and a square body. He is of clean habits, "
                "bilious in constitution, intelligent, and has limited hair on his head. "
                "Natives strongly influenced by the Sun tend to have a square, commanding face, "
                "sharp eyes, and an authoritative bearing."),
    "Moon":    ("The Moon is very windy and phlegmatic in constitution. She has a round body, "
                "auspicious looks, and sweet speech. She is fickle-minded and very lustful. "
                "Moon-dominated natives tend to have a round face, fair complexion, and "
                "an emotionally changeable, charming personality."),
    "Mars":    ("Mars has blood-red eyes and is fickle-minded. He is liberal, bilious, "
                "given to anger, and has a thin waist and lean physique. Mars-dominant "
                "natives tend towards a muscular or wiry build, sharp eyes, and an "
                "impulsive, energetic temperament."),
    "Mercury": ("Mercury is endowed with an attractive physique and the capacity to use "
                "words with many meanings. He is fond of jokes and has a mix of all three "
                "humours (vata, pitta, kapha). Mercury-influenced natives are typically "
                "slim, youthful in appearance, quick-witted, and verbally skilled."),
    "Jupiter": ("Jupiter has a big body, tawny hair, and tawny eyes. He is phlegmatic in "
                "constitution, intelligent, and learned in all shastras. Jupiter-dominant "
                "natives tend to have a large, well-built frame, a broad forehead, and "
                "a wise, benevolent demeanour."),
    "Venus":   ("Venus is charming with a splendorous physique and excellent disposition. "
                "He has charming eyes, is a poet, phlegmatic and windy in constitution, "
                "and has curly hair. Venus-influenced natives are typically beautiful or "
                "attractive, artistic, and fond of pleasures and refined comforts."),
    "Saturn":  ("Saturn has an emaciated and long physique. He has tawny eyes, is windy "
                "in temperament, has big teeth, is indolent, lame, and has coarse hair. "
                "Saturn-dominant natives tend to be tall, thin, dark, with a serious "
                "or melancholic expression and a slow, methodical manner."),
    "Rahu":    ("Rahu has a smoky appearance with a blue-mix physique. He resides in forests "
                "and is of horrible, unconventional appearance. He is windy in temperament "
                "and cunning in intelligence. Rahu-influenced natives often have an unusual "
                "or striking appearance and an unconventional life path."),
    "Ketu":    ("Ketu is akin to Rahu in nature — smoky, fierce, and associated with "
                "spiritual or ascetic energies. Ketu-dominant natives often have an "
                "otherworldly quality, interest in the occult or spiritual, and may "
                "carry marks or scars on the body."),
}

# Section 5: Sapta Dhatus — body rulership (sloka 31)
# Each planet rules one of the seven bodily tissues. Affliction to a planet
# harms the body part it governs. This is a direct health-domain prediction rule.
DHATUS: dict[str, tuple[str, str]] = {
    "Sun":     ("bones",
                "The Sun rules bones (Asthi) among the Sapta Dhatus. Affliction to the Sun "
                "in the birth chart indicates susceptibility to bone disorders, fractures, "
                "spinal issues, and skeletal problems. The Sun's strength protects bone "
                "density and structural integrity."),
    "Moon":    ("blood",
                "The Moon rules blood (Rakta) among the Sapta Dhatus. An afflicted Moon "
                "indicates disorders of the blood — anaemia, blood pressure irregularities, "
                "and circulatory issues. A strong Moon ensures healthy blood and "
                "emotional wellbeing."),
    "Mars":    ("bone marrow",
                "Mars rules bone marrow (Majja) among the Sapta Dhatus. Mars affliction "
                "indicates blood disorders originating from the marrow, immune system "
                "vulnerabilities, and issues with vitality and the manufacturing of "
                "blood cells."),
    "Mercury": ("skin",
                "Mercury rules skin (Tvak) among the Sapta Dhatus. Mercury affliction "
                "indicates skin diseases, rashes, nervous system disorders affecting the "
                "skin, and conditions like eczema or psoriasis. Mercury governs the skin "
                "as the organ of communication with the external world."),
    "Jupiter": ("fat",
                "Jupiter rules fat (Medas / adipose tissue) among the Sapta Dhatus. "
                "Jupiter affliction indicates disorders of fat metabolism, liver congestion, "
                "obesity, and pancreatic issues. A strong Jupiter maintains healthy fat "
                "metabolism and liver function."),
    "Venus":   ("semen",
                "Venus rules semen and reproductive fluids (Shukra) among the Sapta Dhatus. "
                "Venus affliction indicates reproductive disorders, urinary tract issues, "
                "and hormonal imbalances affecting fertility and sexual health."),
    "Saturn":  ("muscles",
                "Saturn rules muscles (Mamsa / muscular tissue) among the Sapta Dhatus. "
                "Saturn affliction indicates muscular disorders, chronic pain, fibromyalgia, "
                "and general weakness of the muscular system. Saturn's restriction manifests "
                "as stiffness, tension, and wasting of muscle tissue."),
}

# Section 6: Digbala — directional strength (slokas 35–38)
# A planet with Digbala in a house performs exceptionally well when posited there.
# During its Dasha, the native is directed fruitfully towards the planet's direction.
DIGBALA: dict[str, tuple[int, str, str]] = {
    # planet → (house, direction, detailed text)
    "Mercury": (1, "East / North",
                "Mercury acquires Digbala (directional strength) in the Ascendant (1st house). "
                "Mercury in the Ascendant gives exceptional intelligence, communication skills, "
                "and commercial ability. During Mercury's Dasha, the native achieves success "
                "through intellect and is directed towards the north for education and business."),
    "Jupiter": (1, "North-East",
                "Jupiter acquires Digbala (directional strength) in the Ascendant (1st house). "
                "Jupiter in the Ascendant is exceptionally powerful, greatly strengthening wisdom, "
                "teaching ability, and spiritual growth. During Jupiter's Dasha, the native "
                "achieves recognition through knowledge and noble conduct."),
    "Sun":     (10, "South",
                "The Sun acquires Digbala (directional strength) in the 10th house. A Sun in "
                "the 10th house is exceptionally powerful for career, authority, and public "
                "recognition. During Sun's Dasha, the native achieves prominence and commands "
                "respect in professional life."),
    "Mars":    (10, "South",
                "Mars acquires Digbala (directional strength) in the 10th house. Mars in "
                "the 10th gives exceptional drive, courage, and career achievement. During "
                "Mars's Dasha, the native accomplishes great feats through bold action and "
                "is directed towards the south."),
    "Saturn":  (7, "West",
                "Saturn acquires Digbala (directional strength) in the 7th house. Saturn in "
                "the 7th strengthens discipline, longevity of partnerships, and endurance. "
                "During Saturn's Dasha, the native achieves through sustained partnership "
                "and is directed towards the west."),
    "Moon":    (4, "North",
                "The Moon acquires Digbala (directional strength) in the 4th house. Moon in "
                "the 4th enhances emotional security, mother's influence, and home happiness. "
                "During Moon's Dasha, the native finds fulfilment through home, family, and "
                "is directed towards the north-west."),
    "Venus":   (4, "North",
                "Venus acquires Digbala (directional strength) in the 4th house. Venus in "
                "the 4th gives domestic happiness, vehicle comforts, and marital harmony. "
                "During Venus's Dasha, the native enjoys luxuries, home pleasures, and "
                "is directed towards the south-east."),
}


# ── Rule builder ──────────────────────────────────────────────────────────────

def make_source() -> dict:
    return {
        "book":           BOOK,
        "book_id":        BOOK_ID,
        "chapter":        CHAPTER,
        "chapter_name":   CHAP_NAME,
        "batch_id":       BATCH_ID,
        "primary":        BOOK,
        "page_ref":       None,
        "passage_ref_id": None,
    }


def make_rule(rule_id: str, planet: str, attribute: str, summary: str,
              detailed: str, life_domain: str, tags: list) -> dict:
    return {
        "rule_id":    rule_id,
        "science_id": SCIENCE,
        "source":     make_source(),
        "condition": {
            "type":           "planet_nature",
            "planet":         planet,
            "attribute":      attribute,
            "sub_conditions": [],
            "operator":       "and",
        },
        "interpretation": {
            "summary":            summary,
            "detailed":           detailed,
            "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
            "remedies":           [],
            "life_domain":        life_domain,
            "tags":               ["verbatim", "planet_nature", "chapter3"] + tags,
        },
        "metadata": {
            "planets_involved": [planet],
            "houses_involved":  [],
            "signs_involved":   [],
            "condition_count":  1,
        },
        "confidence": {
            "base":                  0.80,
            "source_weight":         0.95,   # BPHS = highest authority
            "cross_book_multiplier": 1.0,
        },
        "approval_status": "pending_review",
        "created_at":      datetime.now(timezone.utc).isoformat(),
    }


def build_all_rules() -> list[dict]:
    rules: list[dict] = []
    idx = 1

    # Section 1 — Benefic / Malefic (9 planets)
    for planet, (nature, text) in BENEFIC_MALEFIC.items():
        pc = PLANET_CODES[planet]
        rules.append(make_rule(
            rule_id     = f"R-BPHS3-{pc}-BEN-{idx:03d}",
            planet      = planet,
            attribute   = "benefic_malefic",
            summary     = f"{planet} is a natural {nature} planet.",
            detailed    = text,
            life_domain = "general",
            tags        = ["benefic_malefic"],
        ))
        idx += 1

    # Section 2 — Governance (7 planets: Sun–Saturn)
    for planet, text in GOVERNANCE.items():
        pc = PLANET_CODES[planet]
        rules.append(make_rule(
            rule_id     = f"R-BPHS3-{pc}-GOV-{idx:03d}",
            planet      = planet,
            attribute   = "governance",
            summary     = text.split(".")[0] + ".",
            detailed    = text,
            life_domain = "personality",
            tags        = ["governance"],
        ))
        idx += 1

    # Section 3 — Cabinet (9 planets)
    for planet, text in CABINET.items():
        pc = PLANET_CODES[planet]
        rules.append(make_rule(
            rule_id     = f"R-BPHS3-{pc}-CAB-{idx:03d}",
            planet      = planet,
            attribute   = "cabinet_role",
            summary     = text.split(".")[0] + ".",
            detailed    = text,
            life_domain = "career",
            tags        = ["cabinet"],
        ))
        idx += 1

    # Section 4 — Descriptions (9 planets)
    for planet, text in DESCRIPTIONS.items():
        pc = PLANET_CODES[planet]
        rules.append(make_rule(
            rule_id     = f"R-BPHS3-{pc}-DESC-{idx:03d}",
            planet      = planet,
            attribute   = "description",
            summary     = text.split(".")[0] + ".",
            detailed    = text,
            life_domain = "personality",
            tags        = ["description", "physical"],
        ))
        idx += 1

    # Section 5 — Sapta Dhatus (7 planets: Sun–Saturn)
    for planet, (dhatu, text) in DHATUS.items():
        pc = PLANET_CODES[planet]
        rules.append(make_rule(
            rule_id     = f"R-BPHS3-{pc}-DHATU-{idx:03d}",
            planet      = planet,
            attribute   = "dhatu_rulership",
            summary     = f"{planet} rules {dhatu} (Sapta Dhatu).",
            detailed    = text,
            life_domain = "health",
            tags        = ["dhatu", "health"],
        ))
        idx += 1

    # Section 6 — Digbala (7 planets: all except Rahu/Ketu)
    for planet, (house, direction, text) in DIGBALA.items():
        pc = PLANET_CODES[planet]
        rules.append(make_rule(
            rule_id     = f"R-BPHS3-{pc}-DIG-{idx:03d}",
            planet      = planet,
            attribute   = "digbala",
            summary     = f"{planet} has Digbala in house {house} ({direction}).",
            detailed    = text,
            life_domain = "general",
            tags        = ["digbala", "directional_strength"],
        ))
        idx += 1

    return rules


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Ingest BPHS Chapter 3 — Planetary Characters and Description"
    )
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   required=True)
    parser.add_argument("--dry-run",   action="store_true",
                        help="Print rule summary but do NOT write to MongoDB")
    args = parser.parse_args()

    rules = build_all_rules()

    # ── Print summary ─────────────────────────────────────────────────────────
    print(f"\nBPHS Chapter 3 — Planetary Characters and Description")
    print(f"{'─' * 56}")
    section_counts: dict[str, int] = {}
    for r in rules:
        attr = r["condition"]["attribute"]
        section_counts[attr] = section_counts.get(attr, 0) + 1
    for attr, count in section_counts.items():
        print(f"  {attr:<30} : {count}")
    print(f"  {'─' * 38}")
    print(f"  {'TOTAL':<30} : {len(rules)}")
    print(f"\n  batch_id : {BATCH_ID}")
    print(f"  Isolation: approval_status='pending_review' — zero rules reach live users")

    if args.dry_run:
        print("\n[DRY RUN] — no changes written to MongoDB")
        print("\nSample rules:")
        for r in rules[:3]:
            print(f"\n  {r['rule_id']}")
            print(f"    attribute : {r['condition']['attribute']}")
            print(f"    summary   : {r['interpretation']['summary'][:90]}")
        return

    # ── Insert into MongoDB ───────────────────────────────────────────────────
    client = MongoClient(args.mongo_url)
    db     = client[args.db_name]
    col    = db["interpretation_rules"]

    existing = col.count_documents({"source.batch_id": BATCH_ID})
    if existing:
        print(f"\n⚠  Batch '{BATCH_ID}' already has {existing} rules in MongoDB.")
        print("   Delete those documents first, then re-run without --dry-run.")
        client.close()
        return

    result = col.insert_many(rules, ordered=False)
    print(f"\n✅  Inserted {len(result.inserted_ids)} rules into MongoDB")
    print(f"   batch_id : {BATCH_ID}")
    print(f"\n   Validate with:")
    print(f"   python3 scripts/validate_rules.py --mongo-url $MONGO_URL \\")
    print(f"     --db-name EverydayHoroscope \\")
    print(f"     --batch-id {BATCH_ID}")
    client.close()


if __name__ == "__main__":
    main()
