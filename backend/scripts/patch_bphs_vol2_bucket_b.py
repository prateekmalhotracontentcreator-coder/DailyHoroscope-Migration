#!/usr/bin/env python3
"""
Apply GAI-confirmed Bucket B patches for BPHS Vol 2 Ch49-51 flagged rules.

GAI response date: 2026-06-01
Source: /Users/apple/Documents/Knowledge Engine_eBooks/# GAI Response -- BPHS Vol 2 Ch49-51 Flagged Rules.md

Actions:
1. 7 flagged rules → pending_human_review with validator_error:true
2. 7 false-contradiction-downgraded rules → restored to auto_approved
3. ch51-014: amend interpretation to remove bad sloka citation
4. aquarius-pada-7/8: patch nakshatra field to sign name + add pada_step
"""

from datetime import datetime, timezone
from pymongo import MongoClient

import os
MONGO_URL = os.environ.get("MONGO_URL", "")
if not MONGO_URL:
    raise RuntimeError("MONGO_URL environment variable is required")
DB_NAME = "horoscope_db"
NOW = datetime.now(timezone.utc).isoformat()
GAI_SOURCE = "GAI_BPHS_Vol2_Ch49_51_Triage_2026-06-01"


def main():
    client = MongoClient(MONGO_URL)
    db = client[DB_NAME]
    col = db["interpretation_rules"]

    print("=== Bucket B Patches -- BPHS Vol 2 Ch49-51 ===\n")

    # ─────────────────────────────────────────────────────────────────────────
    # BLOCK 1: Flagged rules → pending_human_review (validator errors)
    # ─────────────────────────────────────────────────────────────────────────

    # 1a. ch50-001 & ch50-002: Upachaya polarity reversal -- validator error
    #     GAI: "Malefics in 3rd/6th from Dasa Rasi bring victory -- BPHS Slokas 4-10 Page 604"
    for rule_id in ["bphs2-ch50-001", "bphs2-ch50-002"]:
        r = col.update_one(
            {"rule_id": rule_id},
            {"$set": {
                "approval_status": "pending_human_review",
                "validation.verdict": "spot_check",
                "validation.flag_reason": "validator_error:true -- upachaya_dasa_rasi_inversion. "
                    "GAI confirmed: BPHS Slokas 4-10 (Page 604) explicitly state malefics in 3rd/6th "
                    "from Dasa Rasi → victory; benefics → defeat. Validator incorrectly applied Radix "
                    "natal logic to Dasa Rasi displacements.",
                "validation.validator_error": True,
                "validation.gai_verified": True,
                "validation.gai_source": GAI_SOURCE,
                "validation.gai_sloka_ref": "BPHS_Vol2_Ch50_Slokas_4-10_Page_604",
                "validation.validated_at": NOW,
            }}
        )
        print(f"  {rule_id}: flagged → PHR | modified={r.modified_count}")

    # 1b. ch50-003: False contradiction flag -- complementary polarity rule
    #     GAI: "003/015/046 are complementary polarity rules -- all must be retained"
    r = col.update_one(
        {"rule_id": "bphs2-ch50-003"},
        {"$set": {
            "approval_status": "pending_human_review",
            "validation.verdict": "spot_check",
            "validation.flag_reason": "validator_error:true -- false_contradiction_flag. "
                "GAI confirmed: rules 003/015/046 describe opposite planet categories (malefics vs benefics) "
                "for same house positions -- these are complementary polarity rules, not contradictions. "
                "All three must be retained as distinct execution blocks.",
            "validation.validator_error": True,
            "validation.is_complementary": True,
            "validation.gai_verified": True,
            "validation.gai_source": GAI_SOURCE,
            "validation.validated_at": NOW,
            "validation.contradiction_ids": [],
            "validation.contradiction_summary": "",
        }}
    )
    print(f"  bphs2-ch50-003: flagged → PHR | modified={r.modified_count}")

    # 1c. ch50-032: Venus/Moon terminal aspect -- validator doctrinal ignorance
    #     GAI: "Slokas 43-45 Page 609 explicitly state this rule. Jala Tattva closing-gate mechanism."
    r = col.update_one(
        {"rule_id": "bphs2-ch50-032"},
        {"$set": {
            "approval_status": "pending_human_review",
            "validation.verdict": "spot_check",
            "validation.flag_reason": "validator_error:true -- text_verified. "
                "GAI confirmed: BPHS Slokas 43-45 (Page 609) explicitly state Venus or Moon aspecting "
                "concluding Dasa Rasi → displeasure of government and loss of wealth. "
                "Jala Tattva closing-gate mechanism in Jaimini/Chara Dasa context.",
            "validation.validator_error": True,
            "validation.gai_verified": True,
            "validation.gai_source": GAI_SOURCE,
            "validation.gai_sloka_ref": "BPHS_Vol2_Ch50_Slokas_43-45_Page_609",
            "validation.engine_tags": ["TERMINAL_DASA_OVERRIDE", "POLITICAL_RISK", "FINANCIAL_INERTIA"],
            "validation.validated_at": NOW,
        }}
    )
    print(f"  bphs2-ch50-032: flagged → PHR | modified={r.modified_count}")

    # 1d. ch51-014: Source misattribution -- logic sound but not in Ch51 slokas literally
    #     GAI: "Remove explicit Sloka 12 citation. Relocate to jaimini_foundational."
    #     Also amend interpretation to remove incorrect sloka attribution
    NEW_DETAILED = (
        "In the Rasi Antardasa 8th-house terminal logic: when the Paka (Dwara/Soul) Rasi of the active "
        "Antardasa coincides with the natal 8th house (the house governing longevity, obstacles, and death), "
        "the sub-period activates the exit-gate of the chart. This produces terminal instability -- a "
        "critical life juncture involving danger to longevity, a potential mortality window, or severe "
        "structural collapse of the entity's foundations. The 8th house connection brings the Antardasa "
        "into direct contact with the chart's most sensitive longevity point; when the sub-period's Soul "
        "Rasi operates from here, the effects are not merely adverse but potentially existential. "
        "Note (GAI 2026-06-01): This rule reflects standard cross-referencing of an active Dasa sign "
        "position against natal radix houses, which is standard Jaimini methodology. Paka Rasi and "
        "Dwara Rasi are synonymous in this context per BPHS Ch51. The original Ch51 Sloka 12 citation "
        "has been removed as this principle is foundational Jaimini logic rather than a specific Ch51 sloka."
    )
    r = col.update_one(
        {"rule_id": "bphs2-ch51-014"},
        {"$set": {
            "approval_status": "pending_human_review",
            "interpretation.detailed": NEW_DETAILED,
            "source.chapter": 51,
            "source.sloka": "jaimini_foundational",
            "validation.verdict": "spot_check",
            "validation.flag_reason": "source_tag_mutated:true -- "
                "GAI confirmed logic is conceptually sound (standard Jaimini Dasa sign vs natal house "
                "cross-reference). However Ch51 Sloka 12 citation was incorrect -- no literal sloka "
                "establishes this rule. Sloka citation removed; rule relocated to jaimini_foundational "
                "category. Paka Rasi = Dwara Rasi confirmed synonymous per GAI.",
            "validation.source_tag_mutated": True,
            "validation.gai_verified": True,
            "validation.gai_source": GAI_SOURCE,
            "validation.validated_at": NOW,
        }}
    )
    print(f"  bphs2-ch51-014: flagged → PHR + interpretation amended | modified={r.modified_count}")

    # 1e. aquarius-pada-7: Kalachakra non-linear wheel -- schema patch
    #     GAI: "Aries at Pada 7 text-authentic (Slokas 30-32). Nakshatra field → sign name."
    r = col.update_one(
        {"rule_id": "bphs2-ch49-aquarius-pada-7"},
        {"$set": {
            "approval_status": "pending_human_review",
            "condition.nakshatra": "Aries",
            "condition.pada_step": 7,
            "validation.verdict": "spot_check",
            "validation.flag_reason": "validator_error:true -- schema_patched. "
                "GAI confirmed: Kalachakra Dasa Aquarius sequence (Slokas 30-32 Page 601) "
                "uses a non-linear Savya/Apasavya wheel where Aries is the 7th step -- "
                "sign repetition is intentional, not an error. Nakshatra field renamed to sign name 'Aries'; "
                "pada_step=7 added.",
            "validation.validator_error": True,
            "validation.schema_patched": True,
            "validation.gai_verified": True,
            "validation.gai_source": GAI_SOURCE,
            "validation.gai_sloka_ref": "BPHS_Vol2_Ch49_Slokas_30-32_Page_601",
            "validation.validated_at": NOW,
        }}
    )
    print(f"  bphs2-ch49-aquarius-pada-7: flagged → PHR + schema patched | modified={r.modified_count}")

    # 1f. aquarius-pada-8: Kalachakra non-linear wheel -- schema patch
    #     GAI: "Taurus at Pada 8 → death. Sanskrit confirmed: vrishabe maranam bhavet (Sloka 31)."
    r = col.update_one(
        {"rule_id": "bphs2-ch49-aquarius-pada-8"},
        {"$set": {
            "approval_status": "pending_human_review",
            "condition.nakshatra": "Taurus",
            "condition.pada_step": 8,
            "validation.verdict": "spot_check",
            "validation.flag_reason": "validator_error:true -- schema_patched. "
                "GAI confirmed: Kalachakra Aquarius Pada 8 = Taurus → death. "
                "Sanskrit: वृषभे मरणं भवेत् (vrishabe maranam bhavet) -- Sloka 31 Page 601. "
                "Taurus repetition in wheel is intentional Savya/Apasavya behaviour. "
                "Outcome 'death' is text-authentic -- not an extreme encoding artifact. "
                "Nakshatra field renamed to sign name 'Taurus'; pada_step=8 added.",
            "validation.validator_error": True,
            "validation.schema_patched": True,
            "validation.severity_tier": "CRITICAL_TERMINAL",
            "validation.gai_verified": True,
            "validation.gai_source": GAI_SOURCE,
            "validation.gai_sloka_ref": "BPHS_Vol2_Ch49_Sloka_31_Page_601",
            "validation.gai_sanskrit_ref": "vrishabe maranam bhavet",
            "validation.validated_at": NOW,
        }}
    )
    print(f"  bphs2-ch49-aquarius-pada-8: flagged → PHR + schema patched | modified={r.modified_count}")

    print()

    # ─────────────────────────────────────────────────────────────────────────
    # BLOCK 2: False-contradiction-downgraded rules → restored to auto_approved
    # ─────────────────────────────────────────────────────────────────────────

    # 015, 039, 046, 021: were auto_approved, downgraded due to false contradictions
    # GAI confirmed: all complementary polarity rules
    restore_to_approved = [
        ("bphs2-ch50-015", "Complementary to 003/039 -- benefics in 5th/9th from Dasa Rasi → favourable. "
            "Confirmed not a contradiction with 003 (malefics → distress) by GAI."),
        ("bphs2-ch50-039", "Complementary to 003/015 -- malefics in 5th+9th → destruction. "
            "Confirmed not a contradiction with 015 (benefics → favourable) by GAI."),
        ("bphs2-ch50-046", "Complementary to 003 -- benefics/exalted in 5th/7th/9th → government recognition. "
            "Confirmed not a contradiction with 003 (malefics → distress) by GAI."),
        ("bphs2-ch50-020", "Malefics/debilitated in 5th+9th from Antardasa Rasi → death-level adversity. "
            "Complementary to 021 (exalted → elevation). GAI confirmed 020↔021 are dual-polarity rules."),
        ("bphs2-ch50-021", "Exalted in 5th or 9th from Antardasa Rasi → elevation. "
            "Complementary to 020 (malefics → adversity). GAI confirmed pair is not a contradiction."),
        ("bphs2-ch50-071", "8th lord in active Dasa Rasi → evil environmental effects (Slokas 56-59). "
            "GAI confirmed dual-layer with 072: validator truncation flag was incorrect. "
            "Both 071 and 072 are complementary processing layers per BPHS."),
        ("bphs2-ch50-072", "House lords (incl. 8th) in active Dasa Rasi → growth of house significations (Sloka 66.5). "
            "GAI confirmed dual-layer with 071: engine must process challenge loop (071) AND "
            "localized asset boost (072) simultaneously."),
    ]

    for rule_id, gai_note in restore_to_approved:
        r = col.update_one(
            {"rule_id": rule_id},
            {"$set": {
                "approval_status": "auto_approved",
                "validation.verdict": "approve",
                "validation.flag_reason": f"false_contradiction_cleared -- {gai_note}",
                "validation.contradiction_ids": [],
                "validation.contradiction_summary": "",
                "validation.gai_verified": True,
                "validation.gai_source": GAI_SOURCE,
                "validation.dual_layer_processing": True,
                "validation.validated_at": NOW,
            }}
        )
        print(f"  {rule_id}: PHR → auto_approved | modified={r.modified_count}")

    print()

    # ─────────────────────────────────────────────────────────────────────────
    # FINAL STATUS CHECK
    # ─────────────────────────────────────────────────────────────────────────
    from collections import Counter
    statuses = Counter(r["approval_status"] for r in col.find(
        {"source.batch_id": "bphs-vol2-ch49-51-v1"},
        {"approval_status": 1, "_id": 0}
    ))
    print("=== Final status breakdown for bphs-vol2-ch49-51-v1 ===")
    for k, v in sorted(statuses.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")
    print(f"  Total: {sum(statuses.values())}")

    client.close()


if __name__ == "__main__":
    main()
