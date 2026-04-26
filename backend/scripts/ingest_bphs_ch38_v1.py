#!/usr/bin/env python3
"""
ingest_bphs_ch38_v1.py — BPHS Chapter 38: Solar Yogas

4 rules total:
  3  Vesi / Vosi / Ubhayachari yoga rules  (Slokas 1-3)
  1  Benefic/Malefic modifier              (Sloka 4 — general principle)

Hard-coded from RTF — zero AI extraction cost.
Checkable: 3 / 4 (75%).

New yoga_check type introduced:
  planet_in_house_from_sun  — non-Moon planet in specific house(s) from Sun
                               Sun-based parallel to planet_in_house_from_moon (Ch 37)

Cross-references:
  Vesi    ↔ Sunapha Yoga   (bphs-ch37-011) — same structure, Moon replaced by Sun
  Vosi    ↔ Anapha Yoga    (bphs-ch37-012) — same structure, Moon replaced by Sun
  Ubhayachari ↔ Duradhara  (bphs-ch37-013) + tba16-003 — same compound structure

Standard --save / --upload workflow:
  Step 1 — Dry run:
    python3 scripts/ingest_bphs_ch38_v1.py --dry-run --save scripts/bphs_ch38_rules.json

  Step 2 — Review bphs_ch38_rules.json; amend as needed.

  Step 3 — Upload (zero API calls):
    python3 scripts/ingest_bphs_ch38_v1.py \\
      --upload scripts/bphs_ch38_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 4 — Validate:
    python3 scripts/validate_rules.py \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id bphs-ch38-v1-20260426
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Constants ─────────────────────────────────────────────────────────────────

SCIENCE   = "jyotish"
BOOK      = "Brihat Parashara Hora Shastra"
BOOK_ID   = "bphs"
CHAPTER   = 38
CHAP_NAME = "Solar Yogas"
BATCH_ID  = "bphs-ch38-v1-20260426"

# ── yoga_check.type legend ────────────────────────────────────────────────────
# planet_in_house_from_sun  — non-Moon planet in specific house(s) from Sun
# complex                   — multi-condition / qualifier rule; checkable=False

# ── Yoga source data ──────────────────────────────────────────────────────────

YOGA_DATA: list[dict] = [

    # ── 1. VESI YOGA (Slokas 1-3) ─────────────────────────────────────────────
    {
        "yoga_name":    "Vesi Yoga",
        "sloka":        "ch38-sl01-03-vesi",
        "group":        "solar_yoga",
        "condition_type": "yoga_combination",
        "formation":    (
            "A planet other than the Moon occupies the 2nd house from the Sun's sign. "
            "Any non-Moon planet (Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu) "
            "in the 2nd from the Sun qualifies. Benefics in this position give the "
            "stated effects; malefics produce contrary results (see modifier rule "
            "bphs-ch38-004). Solar counterpart of Sunapha Yoga (bphs-ch37-011)."
        ),
        "effect":       (
            "One born in Vesi yoga will be even-sighted, truthful, long-bodied, "
            "indolent, happy, and endowed with negligible wealth. Effects are mixed "
            "— positive character traits alongside limited material prosperity and "
            "a tendency toward indolence."
        ),
        "is_benefic":   True,
        "life_domains": ["character", "happiness", "wealth"],
        "yoga_check": {
            "type":            "planet_in_house_from_sun",
            "checkable":       True,
            "house":           2,
            "exclude_planets": ["Moon"],
            "description":     (
                "Any planet except the Moon must occupy the 2nd house counted from "
                "the Sun's sign. Mars, Mercury, Jupiter, Venus, Saturn, Rahu, or Ketu "
                "in the 2nd from the Sun qualifies. Cross-ref: Sunapha Yoga "
                "(bphs-ch37-011) — identical structure with Moon as reference."
            ),
        },
    },

    # ── 2. VOSI YOGA (Slokas 1-3) ─────────────────────────────────────────────
    {
        "yoga_name":    "Vosi Yoga",
        "sloka":        "ch38-sl01-03-vosi",
        "group":        "solar_yoga",
        "condition_type": "yoga_combination",
        "formation":    (
            "A planet other than the Moon occupies the 12th house from the Sun's sign. "
            "Benefics in this position give the stated effects; malefics produce "
            "contrary results. Solar counterpart of Anapha Yoga (bphs-ch37-012)."
        ),
        "effect":       (
            "One born with Vosi yoga will be skilful, charitable, and endowed with "
            "fame, learning, and strength."
        ),
        "is_benefic":   True,
        "life_domains": ["career", "fame", "scholarship", "character"],
        "yoga_check": {
            "type":            "planet_in_house_from_sun",
            "checkable":       True,
            "house":           12,
            "exclude_planets": ["Moon"],
            "description":     (
                "Any planet except the Moon must occupy the 12th house counted from "
                "the Sun's sign. Cross-ref: Anapha Yoga (bphs-ch37-012) — identical "
                "structure with Moon as reference."
            ),
        },
    },

    # ── 3. UBHAYACHARI YOGA (Slokas 1-3) ──────────────────────────────────────
    {
        "yoga_name":    "Ubhayachari Yoga",
        "sloka":        "ch38-sl01-03-ubhayachari",
        "group":        "solar_yoga",
        "condition_type": "yoga_combination",
        "formation":    (
            "Planets other than the Moon occupy BOTH the 2nd and the 12th houses "
            "from the Sun simultaneously. This is the combined form of Vesi (planet "
            "in 2nd from Sun) and Vosi (planet in 12th from Sun). Solar counterpart "
            "of Duradhara Yoga (bphs-ch37-013). Cross-ref: tba16-003 (Ubhaychari "
            "Yoga in TBA Ch 16) — same formation, same name."
        ),
        "effect":       (
            "The Ubhayachari native will be a king or equal to a king and be happy."
        ),
        "is_benefic":   True,
        "life_domains": ["royalty", "happiness", "power"],
        "yoga_check": {
            "type":            "planet_in_house_from_sun",
            "checkable":       True,
            "houses":          [2, 12],
            "operator":        "and",
            "exclude_planets": ["Moon"],
            "description":     (
                "Non-Moon planets must occupy BOTH the 2nd AND the 12th house from "
                "the Sun simultaneously. Compound of Vesi + Vosi. Both positions must "
                "be filled by non-Moon planets. Cross-ref: Duradhara (bphs-ch37-013) "
                "and tba16-003 (Ubhaychari Yoga)."
            ),
        },
    },

    # ── 4. SOLAR YOGA BENEFIC/MALEFIC MODIFIER (Sloka 4) ─────────────────────
    {
        "yoga_name":    "Solar Yoga Benefic/Malefic Modifier",
        "sloka":        "ch38-sl04-modifier",
        "group":        "solar_yoga",
        "condition_type": "general_principle",
        "formation":    (
            "The nature of the planet forming Vesi, Vosi, or Ubhayachari yoga "
            "determines the quality of results. This rule modifies all three solar "
            "yogas based on the planet type."
        ),
        "effect":       (
            "Benefics (Jupiter, Venus, Mercury, waxing Moon) forming these solar yogas "
            "will give the effects described — even-sighted, truthful, charitable, "
            "fame, kingly status, etc. Malefics (Sun, Mars, Saturn, Rahu, Ketu, "
            "waning Moon) will produce contrary effects — the reverse of the stated "
            "beneficial qualities."
        ),
        "is_benefic":   True,
        "life_domains": ["character", "wealth", "fame", "royalty"],
        "yoga_check": {
            "type":        "complex",
            "checkable":   False,
            "description": (
                "Qualifying modifier for all three solar yogas (Vesi/Vosi/Ubhayachari). "
                "Determine the nature of the participating planet — natural benefic or "
                "malefic — to assess whether stated effects or contrary effects apply. "
                "Phase 2: implement as a planet-nature check layered on the base yoga."
            ),
        },
    },
]

# ── Group labels ──────────────────────────────────────────────────────────────

GROUP_LABEL: dict[str, str] = {
    "solar_yoga": "Solar Yogas (Vesi / Vosi / Ubhayachari)",
}

# ── build_rule ────────────────────────────────────────────────────────────────

def build_rule(yoga: dict, index: int) -> dict:
    rule_id      = f"bphs-ch38-{index:03d}"
    group        = yoga["group"]
    group_lbl    = GROUP_LABEL.get(group, group)
    yoga_name    = yoga["yoga_name"]
    is_ben       = yoga["is_benefic"]
    formation    = yoga["formation"]
    effect       = yoga["effect"]
    domains      = yoga["life_domains"]
    yc           = yoga["yoga_check"]
    sloka        = yoga.get("sloka", f"ch38-{yoga_name.lower().replace(' ', '-')}")
    cond_type    = yoga.get("condition_type", "yoga_combination")
    checkable    = yc.get("checkable", False)

    # ── Derive houses from yoga_check ─────────────────────────────────────────
    houses: list[int] = []
    if "house" in yc:
        houses = [yc["house"]]
    elif "houses" in yc:
        houses = list(yc["houses"])

    # ── Interpretation text ───────────────────────────────────────────────────
    detailed = (
        f"Yoga: {yoga_name} [{group_lbl}]\n\n"
        f"Formation: {formation}\n\n"
        f"Effect: {effect}"
    )
    summary_effect = effect[:200] + ("..." if len(effect) > 200 else "")
    summary = f"{yoga_name} — {summary_effect}"

    # ── Tags ──────────────────────────────────────────────────────────────────
    sentiment = "benefic" if is_ben else "malefic"
    tags = [
        "verbatim", "yoga", "chapter38",
        cond_type, "yoga_formation",
        f"group:bphs-ch38-{group}",
        sentiment,
    ]
    if checkable:
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
            "type":               cond_type,
            "sub_type":           "yoga_formation",
            "yoga_name":          yoga_name,
            "yoga_group":         group,
            "yoga_group_label":   group_lbl,
            "planets_involved":   [],
            "houses_involved":    houses,
            "sub_conditions":     [],
            "operator":           "and",
            "gender_context":     "neutral",
            "condition_group_id": f"bphs-ch38-{group}",
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
            "houses_involved":      houses,
            "signs_involved":       [],
            "condition_count":      1,
            "gender_context":       "neutral",
            "condition_group_id":   f"bphs-ch38-{group}",
            "is_group_summary":     False,
            "has_physical_markers": False,
            "physical_categories":  [],
            "yoga_checkable":       checkable,
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
        description="Ingest BPHS Ch 38 Solar Yogas into Knowledge Engine"
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
    for idx, yoga in enumerate(YOGA_DATA, start=1):
        all_rules.append(build_rule(yoga, idx))

    total     = len(all_rules)
    benefic   = sum(1 for r in all_rules if r["condition"]["is_benefic"])
    adverse   = total - benefic
    checkable = sum(1 for r in all_rules if r["metadata"]["yoga_checkable"])

    print(f"\n{'─' * 65}")
    print(f"BPHS Chapter {CHAPTER} — {CHAP_NAME}  [v1 hard-coded]")
    print(f"batch_id : {BATCH_ID}")
    print(f"{'─' * 65}")
    print(f"\nGroup breakdown:")
    print(f"  {GROUP_LABEL['solar_yoga']:<36} : {total}")
    print(f"  {'─' * 42}")
    print(f"  {'TOTAL':<36} : {total}")
    print(f"\nBenefic rules  : {benefic}")
    print(f"Adverse rules  : {adverse}")
    print(f"Yoga-checkable : {checkable} / {total}")

    print(f"\nSample rules (all {total}):")
    print("─" * 65)
    for r in all_rules:
        cond = r["condition"]
        yc   = cond.get("yoga_check", {})
        print(f"  rule_id   : {r['rule_id']}")
        print(f"  yoga      : {cond['yoga_name']}  [{cond['yoga_group_label']}]")
        print(f"  check_type: {yc.get('type','—'):<28}  checkable={yc.get('checkable',False)}")
        print(f"  is_benefic: {cond['is_benefic']}")
        print(f"  summary   : {r['interpretation']['summary'][:100]}...")
        print()

    print(f"Isolation: approval_status='pending_review' — zero rules reach live users")

    if not args.dry_run and not args.save:
        if not args.mongo_url:
            print(f"\n⚠  Live run requires --mongo-url  (or use --dry-run / --upload)")
            sys.exit(1)
        insert_rules_to_mongo(all_rules, args.mongo_url, args.db_name)
        print(f"\n   Validate with:")
        print(f"   python3 scripts/validate_rules.py --mongo-url $MONGO_URL \\")
        print(f"     --db-name horoscope_db --batch-id {BATCH_ID}")
        return

    if args.save:
        save_path = Path(args.save)
        with open(save_path, "w", encoding="utf-8") as fh:
            json.dump(all_rules, fh, indent=2, ensure_ascii=False, default=str)
        print(f"\n✅  Rules saved to {args.save}  ({total} rules)")
        print(f"   Review the file, then upload with:")
        print(f"   python3 scripts/ingest_bphs_ch38_v1.py \\")
        print(f"     --upload {args.save} --mongo-url $MONGO_URL --db-name {args.db_name}")


if __name__ == "__main__":
    main()
