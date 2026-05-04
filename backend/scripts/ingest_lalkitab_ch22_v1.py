#!/usr/bin/env python3
"""
ingest_lalkitab_ch22_v1.py — Lal Kitab Chapter 22: Happiness of Having Children

17 rules total across 6 groups:
    4  Context / foundational       (ctx-01 to ctx-04)
    2  Progeny doshas               (dosha-gender-imbalance, dosha-childlessness)
    2  Planetary diagnostics        (planet-saturn, planet-ketu-h5)
    4  Survival / longevity rituals (ritual-red-thread, ritual-ganesha,
                                     ritual-animal-feeding, ritual-dog-feeding,
                                     ritual-she-dog) — 5 rules
    2  Delivery + birthday          (delivery-protocol, ritual-salt-birthday)
    2  Prohibitions                 (prohibition-01, prohibition-02)

Source: Lal Kitab Ch 22 JSON Ready (V5) + Diagnostic + Technical files.
Technical file is primary for context units and sub_type schema.
Note: Technical file contains typo "children die soon after death" —
      corrected to "children die soon after birth" in ingestion.

BATCH_ID = "lalkitab-ch22-v1-20260504"

Standard workflow:
  Step 1 — Dry run + save:
    python3 scripts/ingest_lalkitab_ch22_v1.py --dry-run \\
      --save scripts/lalkitab_ch22_rules.json

  Step 2 — Review JSON; amend as needed.

  Step 3 — Upload:
    python3 scripts/ingest_lalkitab_ch22_v1.py \\
      --upload scripts/lalkitab_ch22_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 4 — Validate:
    python3 scripts/validate_rules.py \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id lalkitab-ch22-v1-20260504
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
CHAPTER   = 22
CHAP_NAME = "Happiness of Having Children"
BATCH_ID  = "lalkitab-ch22-v1-20260504"


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


# ── Rule data ─────────────────────────────────────────────────────────────────

RULES = [

    # ── Section 1: Context / Foundational (4) ────────────────────────────────

    {
        "rule_id":    "lalkitab-ch22-ctx-01",
        "name":       "Motherhood Foundation — Om, Ma, and the Sacred Bond",
        "type":       "general_principle",
        "sub_type":   "context",
        "checkable":  False,
        "yoga_type":  "contextual_inquiry",
        "text": (
            "The phonetic sound of 'Om' and the sacred word 'Ma' (mother) form the "
            "spiritual foundation of this chapter. A mother's affection is compared to "
            "the holy river Ganga — pure and life-giving. Every mother becomes Yashoda "
            "and every child symbolizes Krishna Kanhaya. This contextual recognition is "
            "the baseline for all progeny diagnostics in Lal Kitab Chapter 22."
        ),
        "remedies":    [],
        "domains":     ["spirituality", "family", "progeny"],
        "tags":        ["context", "motherhood", "foundation"],
        "checkable_note": None,
        "constraint_flag": None,
    },
    {
        "rule_id":    "lalkitab-ch22-ctx-02",
        "name":       "Four Ashrams Framework — Grihasthashram as the Highest",
        "type":       "general_principle",
        "sub_type":   "context",
        "checkable":  False,
        "yoga_type":  "contextual_inquiry",
        "text": (
            "The rishis and maharishis established four ashrams (phases) for human life: "
            "brahmcharya (celibacy), grihastha (householder), vaanprastha (forest "
            "dwelling), and sanyas (renunciation). Among these, grihasthashram is "
            "considered the highest — even the gods take birth on earth to enjoy this "
            "phase. The desire for children is therefore a sacred and sanctioned aspiration."
        ),
        "remedies":    [],
        "domains":     ["spirituality", "family", "dharma"],
        "tags":        ["context", "ashram", "grihastha", "foundation"],
        "constraint_flag": None,
    },
    {
        "rule_id":    "lalkitab-ch22-ctx-03",
        "name":       "Erratic Mind Logic — Mind as Root of All Disturbance",
        "type":       "general_principle",
        "sub_type":   "context",
        "checkable":  False,
        "yoga_type":  "contextual_inquiry",
        "text": (
            "Joy, sorrow, victory, defeat, honor, and dishonor all reside in the mind. "
            "The mind is erratic and constantly moving. This baseline recognition "
            "establishes that all progeny-related suffering — anxiety about childlessness, "
            "fear of infant mortality, gender preference anguish — originates as a "
            "disturbance of the mind. Stabilizing the mind is the first step in all "
            "progeny remedial work."
        ),
        "remedies":    [],
        "domains":     ["mind", "general", "progeny"],
        "tags":        ["context", "mind", "baseline"],
        "constraint_flag": None,
    },
    {
        "rule_id":    "lalkitab-ch22-ctx-04",
        "name":       "Universal Human Suffering — The Wanderer's Diagnostic",
        "type":       "general_principle",
        "sub_type":   "context",
        "checkable":  False,
        "yoga_type":  "contextual_inquiry",
        "text": (
            "During life as a wanderer, multi-modal life afflictions are observed: sadness "
            "due to health, lack of wealth, joblessness, trade loss, expansion worries, "
            "childlessness, unworthy children, or marital status issues. The core "
            "diagnostic baseline is that 'everybody is bothered for one or the other "
            "reason.' Childlessness is one affliction among many; no seeker should feel "
            "uniquely cursed. This perspective shapes the compassionate framing of all "
            "Chapter 22 remedies."
        ),
        "remedies":    [],
        "domains":     ["general", "progeny", "karma"],
        "tags":        ["context", "universal_suffering", "diagnostic_baseline"],
        "constraint_flag": None,
    },

    # ── Section 2: Progeny Doshas (2) ────────────────────────────────────────

    {
        "rule_id":    "lalkitab-ch22-dosha-gender-imbalance",
        "name":       "Gender Imbalance Dosha — Four Daughters, No Son",
        "type":       "dosha",
        "sub_type":   "progeny_imbalance",
        "checkable":  False,
        "yoga_type":  "contextual_inquiry",
        "text": (
            "A natal situation where the native has four daughters but no son creates a "
            "specific progeny imbalance dosha. The native faces family coaxing from "
            "husband and in-laws, along with emotional distress, sobbing while showing "
            "the horoscope. The prescribed experimental remedy is Santan Gopal Sadhana."
        ),
        "remedies": [
            {"text": "Observe Santan Gopal Sadhana — the primary experimental remedy for progeny imbalance.", "category": "mantra"},
        ],
        "domains":     ["progeny", "family", "gender"],
        "tags":        ["progeny_imbalance", "dosha", "sons", "daughters"],
        "constraint_flag": None,
    },
    {
        "rule_id":    "lalkitab-ch22-dosha-childlessness",
        "name":       "Childlessness Dosha — Santan Gopal Sadhana",
        "type":       "dosha",
        "sub_type":   "childlessness",
        "checkable":  False,
        "yoga_type":  "contextual_inquiry",
        "text": (
            "The native is bereft of the joy of progeny or branded as 'infertile' by "
            "society. The house craves the sound of a child's babbling; the native "
            "suffers verbal assault from family and society. This condition — regardless "
            "of astrological cause — is addressed by Santan Gopal Sadhana, observed "
            "with complete reverence, confidence, and devotion in God."
        ),
        "remedies": [
            {"text": "Observe Santan Gopal Sadhana with complete faith, reverence, and devotion in God.", "category": "mantra"},
        ],
        "domains":     ["progeny", "health", "family"],
        "tags":        ["childlessness", "dosha", "santan_gopal", "mantra"],
        "constraint_flag": None,
    },

    # ── Section 3: Planetary Diagnostics (2) ─────────────────────────────────

    {
        "rule_id":    "lalkitab-ch22-planet-saturn",
        "name":       "Saturn-Induced Childlessness — Donate via Nephew and Niece",
        "type":       "planetary_combination",
        "sub_type":   "childlessness",
        "checkable":  True,
        "yoga_type":  "planetary_position",
        "yoga_desc":  "Saturn affliction (inauspicious placement) identified in the natal chart as the cause of childlessness. Phase 2: implement as Saturn-specific affliction check.",
        "text": (
            "When childlessness is specifically caused by the inauspicious effect of "
            "Saturn in the horoscope, the prescribed remedy is the donation of Saturn-"
            "associated objects (iron, oil, black sesame, black cloth) — but these "
            "donations MUST be made through the hands of a nephew and niece, not "
            "directly by the native. This relay-donation structure is the key "
            "operative element of the remedy."
        ),
        "remedies": [
            {"text": "Donate Saturn-associated objects (iron, oil, black sesame, black cloth) through the hands of a nephew and niece — not directly by the native.", "category": "offering"},
        ],
        "domains":     ["progeny", "saturn", "karma"],
        "tags":        ["saturn", "childlessness", "planetary_combination", "donation"],
        "planets":     ["Saturn"],
        "houses":      [],
        "constraint_flag": None,
    },
    {
        "rule_id":    "lalkitab-ch22-planet-ketu-h5",
        "name":       "Ketu / Evil Planet in 5th House — Child Ill Effects",
        "type":       "planetary_combination",
        "sub_type":   "longevity",
        "checkable":  True,
        "yoga_type":  "house_placement",
        "yoga_desc":  "Ketu or any natural malefic planet in H5 (house of progeny). Pure positional check.",
        "text": (
            "Presence of Ketu or any evil (malefic) planet in the 5th house — the house "
            "of progeny and intelligence — causes the child to face ill effects. This is "
            "a diagnostic marker for child health challenges, infant vulnerability, or "
            "progeny obstacles arising from 5th house affliction. No direct remedy is "
            "prescribed in the text; the other Chapter 22 longevity rituals serve as "
            "the remedial layer."
        ),
        "remedies":    [],
        "domains":     ["progeny", "health", "child_longevity"],
        "tags":        ["ketu", "h5", "planetary_combination", "child_health"],
        "planets":     ["Ketu"],
        "houses":      [5],
        "constraint_flag": None,
    },

    # ── Section 4: Delivery Protocol + Birthday Remedy (2) ───────────────────

    {
        "rule_id":    "lalkitab-ch22-delivery-protocol",
        "name":       "Painless Delivery Ritual — Milk Pot + Sugar Pot",
        "type":       "general_principle",
        "sub_type":   "delivery",
        "checkable":  False,
        "yoga_type":  "contextual_inquiry",
        "text": (
            "To ensure a painless delivery: fill one pot with milk and one pot with "
            "sugar. The pregnant woman must touch both pots before the birth occurs. "
            "After the delivery is complete, gift both pots to a temple. This ritual "
            "is a protective and auspicious preparation for childbirth."
        ),
        "remedies": [
            {"text": "Fill one pot with milk and one with sugar; pregnant woman touches both before birth. Gift both pots to a temple after delivery.", "category": "offering"},
        ],
        "domains":     ["progeny", "health", "delivery"],
        "tags":        ["delivery", "ritual", "pregnancy", "temple"],
        "constraint_flag": None,
    },
    {
        "rule_id":    "lalkitab-ch22-ritual-salt-birthday",
        "name":       "Birthday Salt Donation — Annual Progeny Welfare Remedy",
        "type":       "general_principle",
        "sub_type":   "longevity",
        "checkable":  False,
        "yoga_type":  "behavioral",
        "text": (
            "For general progeny welfare and support: donate salt or salty items on "
            "the native's own birthday each year. This annual offering maintains the "
            "protective channel for child longevity and family prosperity."
        ),
        "remedies": [
            {"text": "Donate salt or salty items on your own birthday annually.", "category": "offering"},
        ],
        "domains":     ["progeny", "family", "annual_ritual"],
        "tags":        ["birthday", "salt", "offering", "longevity"],
        "constraint_flag": None,
    },

    # ── Section 5: Survival / Longevity Rituals (5) ──────────────────────────

    {
        "rule_id":    "lalkitab-ch22-ritual-red-thread",
        "name":       "Red Thread Transfer Protocol — Infant Mortality Prevention",
        "type":       "general_principle",
        "sub_type":   "survival",
        "checkable":  False,
        "yoga_type":  "behavioral",
        "text": (
            "When children die soon after birth (infant mortality pattern): "
            "Step 1 — tie a red thread around the pregnant woman's wrist soon after "
            "conception. Step 2 — at birth, untie the thread from the mother and "
            "secure it around the child's wrist; simultaneously tie a new, second "
            "red thread around the mother's wrist. Step 3 — both threads must remain "
            "tied for exactly 18 months without being removed."
        ),
        "remedies": [
            {"text": "Tie red thread on pregnant woman's wrist at conception. At birth: transfer thread to child, tie new thread on mother. Both threads worn for exactly 18 months.", "category": "ritual"},
        ],
        "domains":     ["progeny", "health", "infant_mortality"],
        "tags":        ["red_thread", "infant_mortality", "survival", "ritual"],
        "constraint_flag": None,
    },
    {
        "rule_id":    "lalkitab-ch22-ritual-ganesha",
        "name":       "Ganesha Worship — Riddhi-Siddhi for Progeny Obstacles",
        "type":       "general_principle",
        "sub_type":   "survival",
        "checkable":  False,
        "yoga_type":  "behavioral",
        "text": (
            "For removal of progeny obstacles and attainment of success: observe daily "
            "worship and devotion to Ganeshji, the provider of Riddhi (prosperity) and "
            "Siddhi (spiritual accomplishment). Regular Ganesha worship clears the path "
            "for healthy progeny."
        ),
        "remedies": [
            {"text": "Observe daily worship and devotion to Ganeshji — provider of Riddhi-Siddhi.", "category": "ritual"},
        ],
        "domains":     ["progeny", "spirituality", "obstacles"],
        "tags":        ["ganesha", "worship", "riddhi_siddhi", "survival"],
        "constraint_flag": None,
    },
    {
        "rule_id":    "lalkitab-ch22-ritual-animal-feeding",
        "name":       "Daily Animal Feeding — Meal Portion to Cow and Animals",
        "type":       "general_principle",
        "sub_type":   "longevity",
        "checkable":  False,
        "yoga_type":  "behavioral",
        "text": (
            "For general longevity and progeny protection: offer some part of every "
            "daily meal to a cow and such animals. This daily offering of food "
            "maintains the protective shield around children and supports long life "
            "for existing progeny."
        ),
        "remedies": [
            {"text": "Offer a portion of every daily meal to a cow and other animals — daily, without interruption.", "category": "offering"},
        ],
        "domains":     ["progeny", "health", "daily_ritual"],
        "tags":        ["cow", "animal_feeding", "daily", "longevity"],
        "constraint_flag": None,
    },
    {
        "rule_id":    "lalkitab-ch22-ritual-dog-feeding",
        "name":       "Stray Dog Sweet Bread Offering — Child Longevity Protocol",
        "type":       "general_principle",
        "sub_type":   "longevity",
        "checkable":  False,
        "yoga_type":  "behavioral",
        "text": (
            "For general child longevity: feed stray dogs with sweet breads prepared "
            "in an earthen oven. The combination of the sweet bread and the earthen "
            "oven preparation is the specific ritual requirement — ordinary bread or "
            "modern cooking methods do not carry the same remedial potency."
        ),
        "remedies": [
            {"text": "Feed stray dogs with sweet breads prepared specifically in an earthen oven.", "category": "offering"},
        ],
        "domains":     ["progeny", "health", "child_longevity"],
        "tags":        ["dogs", "sweet_bread", "earthen_oven", "longevity"],
        "constraint_flag": None,
    },
    {
        "rule_id":    "lalkitab-ch22-ritual-she-dog",
        "name":       "One-Puppy She-Dog — Child Survival Longevity Marker",
        "type":       "general_principle",
        "sub_type":   "survival",
        "checkable":  False,
        "yoga_type":  "behavioral",
        "text": (
            "To ensure the child 'starts living' (i.e., survives the vulnerable early "
            "period): keep a pet she-dog that has delivered only one puppy in her "
            "litter. The singularity of the litter — exactly one puppy — is the "
            "operative spiritual condition. This she-dog serves as a protective "
            "surrogate life-force anchor for the child."
        ),
        "remedies": [
            {"text": "Keep a pet she-dog that has delivered exactly one puppy — not more, not less.", "category": "ritual"},
        ],
        "domains":     ["progeny", "health", "infant_survival"],
        "tags":        ["she_dog", "one_puppy", "survival", "child_protection"],
        "constraint_flag": None,
    },

    # ── Section 6: Prohibitions (2) ──────────────────────────────────────────

    {
        "rule_id":    "lalkitab-ch22-prohibition-01",
        "name":       "Prohibition — Childless Native Must Not Adopt Elder Brother's Son",
        "type":       "general_principle",
        "sub_type":   "prohibition",
        "checkable":  False,
        "yoga_type":  "behavioral",
        "text": (
            "A childless native is strictly prohibited from adopting the son of their "
            "elder brother. This prohibition is absolute — the adoption of a fraternal "
            "nephew as a son carries karmic and progeny consequences that deepen, "
            "rather than resolve, the childlessness affliction."
        ),
        "remedies":    [],
        "domains":     ["progeny", "family", "prohibition"],
        "tags":        ["prohibition", "adoption", "elder_brother", "childless"],
        "constraint_flag": "strictly_prohibited",
    },
    {
        "rule_id":    "lalkitab-ch22-prohibition-02",
        "name":       "Prohibition — Childless Native Must Not Fund Elder Brother's Daughter's Wedding",
        "type":       "general_principle",
        "sub_type":   "prohibition",
        "checkable":  False,
        "yoga_type":  "behavioral",
        "text": (
            "A childless native is strictly prohibited from arranging or funding the "
            "wedding of their elder brother's daughter at their own expense. Bearing "
            "the financial burden of this wedding — when the native has no children "
            "of their own — creates a karmic imbalance that further blocks the "
            "progeny channel."
        ),
        "remedies":    [],
        "domains":     ["progeny", "family", "prohibition"],
        "tags":        ["prohibition", "wedding", "elder_brother", "childless"],
        "constraint_flag": "strictly_prohibited",
    },
]


# ── Rule builder ──────────────────────────────────────────────────────────────

def build_all_rules() -> list[dict]:
    now = datetime.now(timezone.utc).isoformat()
    docs = []

    for r in RULES:
        doc = _base(r["rule_id"], now)

        # Build yoga_check
        yoga_check: dict = {
            "type":      r["yoga_type"],
            "checkable": r["checkable"],
        }
        if r.get("yoga_desc"):
            yoga_check["description"] = r["yoga_desc"]
        if not r["checkable"]:
            yoga_check["description"] = yoga_check.get(
                "description",
                "Behavioral/contextual rule — not automatable in Phase 1.",
            )

        # Build condition
        cond: dict = {
            "type":     r["type"],
            "sub_type": r["sub_type"],
            "yoga_check": yoga_check,
        }
        if r.get("planets"):
            cond["planets_involved"] = r["planets"]
        if r.get("houses"):
            cond["houses_involved"] = r["houses"]
        if r.get("constraint_flag"):
            cond["constraint_flag"] = r["constraint_flag"]

        doc.update({
            "condition": cond,
            "interpretation": {
                "summary":  r["name"],
                "detailed": r["text"],
                "full_text_passages": [{"text": r["text"], "confidence": "HIGH"}],
                "remedies":     r["remedies"],
                "life_domain":  r["domains"][0],
                "life_domains": r["domains"],
                "tags":         r["tags"],
                "physical_markers": [],
            },
            "metadata": {
                "planets_involved":     r.get("planets", []),
                "houses_involved":      r.get("houses", []),
                "signs_involved":       [],
                "condition_count":      1,
                "gender_context":       "neutral",
                "is_group_summary":     False,
                "has_physical_markers": False,
                "physical_categories":  [],
                "yoga_checkable":       r["checkable"],
            },
            "confidence": {
                "source_confidence": "HIGH",
                "extraction_method": "hard_coded",
                "validated":         False,
            },
        })
        docs.append(doc)

    return docs


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    group  = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--upload",  metavar="JSON_FILE")
    parser.add_argument("--save",   metavar="JSON_FILE")
    parser.add_argument("--mongo-url")
    parser.add_argument("--db-name", default="horoscope_db")
    args = parser.parse_args()

    if args.dry_run:
        rules = build_all_rules()
        print(f"Dry run: {len(rules)} rules generated")
        for r in rules:
            ct = r["condition"]["type"]
            st = r["condition"]["sub_type"]
            ck = "✓" if r["condition"]["yoga_check"]["checkable"] else "·"
            print(f"  {ck} {r['rule_id']:50s} [{ct}/{st}]")
        if args.save:
            Path(args.save).write_text(json.dumps(rules, indent=2, ensure_ascii=False))
            print(f"\nSaved → {args.save}")
        return

    if not args.mongo_url:
        print("ERROR: --mongo-url required for upload", file=sys.stderr)
        sys.exit(1)

    from pymongo import MongoClient
    rules = json.loads(Path(args.upload).read_text())
    print(f"Loaded {len(rules)} rules from {args.upload}")

    client   = MongoClient(args.mongo_url)
    col      = client[args.db_name]["interpretation_rules"]
    inserted = updated = 0
    for r in rules:
        res = col.update_one({"rule_id": r["rule_id"]}, {"$set": r}, upsert=True)
        if res.upserted_id:
            inserted += 1
        elif res.modified_count:
            updated += 1

    print(f"✅ Inserted {inserted} / Updated {updated} rules → {args.db_name}.interpretation_rules")
    client.close()


if __name__ == "__main__":
    main()
