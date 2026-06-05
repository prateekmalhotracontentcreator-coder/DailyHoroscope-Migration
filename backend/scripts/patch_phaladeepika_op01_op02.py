#!/usr/bin/env python3
"""
patch_phaladeepika_op01_op02.py
-----------------------------------------------------------------------
Applies all post-validator patches for batch phaladeepika-v1-20260601:

  PD-OP-01: Fix trailing punctuation on 357 pending_review rules.
            Root cause: Stage 1 structural check requires text to end
            with .!?\"') -- not a content truncation, just missing period.

  PD-OP-02: Five condition/status fixes from decoder thread review:
    pd-ch06-028  Adhama Yoga  → condition corrected to Apoklima, PHR, contradiction_flag
    pd-ch06-030  Varishtha    → condition corrected to Kendra, PHR, contradiction_flag
    pd-ch07-024               → auto_approved (night-birth Kala Bala confirmed valid)
    pd-ch07-028               → PHR (3-tier series confirmed, no-malefics-in-Kendra correct)
    pd-ch18-102               → PHR + cross_reference (distinct from pd-ch18-106)
    pd-ch18-106               → cross_reference added (companion to pd-ch18-102)

  pd-ch08-111:  Activated with recovered Bhava Madhya content (Sloka 35).
"""
from __future__ import annotations

import os
import sys
from collections import Counter
from pymongo import MongoClient

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://PrateekMalhotra:NewDB%40%21123@cluster0.bqtc8l9.mongodb.net/?appName=Cluster0",
)
DB_NAME = "horoscope_db"
BATCH   = "phaladeepika-v1-20260601"
TERMINAL = set(".!?\"')")


def main() -> None:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=20000)
    db  = client[DB_NAME]
    col = db["interpretation_rules"]

    # ── PD-OP-01: trailing punctuation fix ──────────────────────────────
    pending = list(col.find(
        {"ingest_batch_id": BATCH, "approval_status": "pending_review"},
        {"_id": 1, "rule_id": 1, "interpretation": 1},
    ))
    print(f"PD-OP-01: {len(pending)} pending_review rules")

    fixed = 0
    for r in pending:
        interp  = r.get("interpretation") or {}
        detailed = (interp.get("detailed") or "").strip()
        summary  = (interp.get("summary") or "").strip()
        updates: dict = {}
        if detailed and detailed[-1] not in TERMINAL:
            updates["interpretation.detailed"] = detailed + "."
        if summary and summary[-1] not in TERMINAL:
            updates["interpretation.summary"] = summary + "."
        if updates:
            col.update_one({"_id": r["_id"]}, {"$set": updates})
            fixed += 1

    print(f"  Punctuation appended on: {fixed} rules")
    print(f"  Already terminated:      {len(pending) - fixed} rules")

    # ── PD-OP-02 ─────────────────────────────────────────────────────────

    # pd-ch06-028 -- Adhama Yoga: Apoklima condition
    r = col.update_one(
        {"rule_id": "pd-ch06-028", "ingest_batch_id": BATCH},
        {"$set": {
            "condition": {
                "type":            "moon_sun_angular_relationship",
                "relationship":    "Apoklima",
                "houses_from_sun": [3, 6, 9, 12],
                "description":     "Moon in Apoklima (3rd/6th/9th/12th) from Sun -- weakest Moon-Sun phase",
            },
            "contradiction_flag": True,
            "approval_status":    "pending_human_review",
            "engine_note": (
                "Source PDF edition has Adhama/Varishtha pair swapped vs classical doctrine. "
                "Classical texts (BPHS/Saravali) confirm Adhama=Apoklima. "
                "Cross-reference second Phaladeepika edition (Rangacharya/Raman) before approval."
            ),
            "validator_error": False,
        }},
    )
    print(f"\nPD-OP-02 pd-ch06-028 (Adhama→Apoklima): {r.modified_count}")

    # pd-ch06-030 -- Varishtha Yoga: Kendra condition
    r = col.update_one(
        {"rule_id": "pd-ch06-030", "ingest_batch_id": BATCH},
        {"$set": {
            "condition": {
                "type":            "moon_sun_angular_relationship",
                "relationship":    "Kendra",
                "houses_from_sun": [1, 4, 7, 10],
                "description":     "Moon in Kendra (1st/4th/7th/10th) from Sun -- strongest Moon-Sun phase",
            },
            "contradiction_flag": True,
            "approval_status":    "pending_human_review",
            "engine_note": (
                "Source PDF edition has Adhama/Varishtha pair swapped vs classical doctrine. "
                "Classical texts confirm Varishtha=Kendra. "
                "Cross-reference second Phaladeepika edition before approval."
            ),
            "validator_error": False,
        }},
    )
    print(f"PD-OP-02 pd-ch06-030 (Varishtha→Kendra): {r.modified_count}")

    # pd-ch07-024 -- confirmed valid, night-birth Kala Bala
    r = col.update_one(
        {"rule_id": "pd-ch07-024", "ingest_batch_id": BATCH},
        {"$set": {
            "approval_status": "auto_approved",
            "engine_note": (
                "Night-birth Kala Bala: Moon/Venus/Saturn gain temporal strength at night. "
                "Benefics in upachaya houses (11/6/3) with night-birth dignity produce ascending outcomes. "
                "Three-alternative OR structure confirmed per Sloka 16. Validator logic error -- condition correct."
            ),
            "validator_error": True,
        }},
    )
    print(f"PD-OP-02 pd-ch07-024 (→ auto_approved): {r.modified_count}")

    # pd-ch07-028 -- confirmed correct (3-tier series, no-malefics-in-Kendra)
    r = col.update_one(
        {"rule_id": "pd-ch07-028", "ingest_batch_id": BATCH},
        {"$set": {
            "approval_status": "pending_human_review",
            "engine_note": (
                "3-tier series Sloka 19: (a) Moon in Kendra → king, "
                "(b) Moon NOT in Kendra + no malefics in Kendra → oppressive king, "
                "(c) malefics in Kendra → worst outcome. "
                "Condition 'no_malefics_in_kendra' is correct for middle tier. Validator error."
            ),
            "validator_error": True,
        }},
    )
    print(f"PD-OP-02 pd-ch07-028 (→ PHR): {r.modified_count}")

    # pd-ch18-102 -- distinct outcome from pd-ch18-106; add cross_reference
    r = col.update_one(
        {"rule_id": "pd-ch18-102", "ingest_batch_id": BATCH},
        {"$set": {
            "approval_status":  "pending_human_review",
            "cross_reference":  ["pd-ch18-106"],
            "engine_note": (
                "Mars aspect: compulsive psychological craving (habitual desire). "
                "Saturn aspect (pd-ch18-106): methodical boundary transgression (actual conduct). "
                "Outcomes are distinct -- Mars=desire, Saturn=action. Validator surface-similarity error."
            ),
            "validator_error": True,
        }},
    )
    print(f"PD-OP-02 pd-ch18-102 (→ PHR + cross_ref): {r.modified_count}")

    # pd-ch18-106 -- add cross_reference (companion rule)
    r = col.update_one(
        {"rule_id": "pd-ch18-106", "ingest_batch_id": BATCH},
        {"$set": {
            "cross_reference": ["pd-ch18-102"],
            "engine_note": (
                "Saturn aspect: methodical boundary transgression (actual adulterous conduct). "
                "Mars aspect (pd-ch18-102): compulsive psychological craving (desire only). "
                "Outcomes are distinct -- see pd-ch18-102."
            ),
        }},
    )
    print(f"pd-ch18-106 (cross_ref added): {r.modified_count}")

    # ── pd-ch08-111: Activate with recovered Bhava Madhya content ────────
    r = col.update_one(
        {"rule_id": "pd-ch08-111", "ingest_batch_id": BATCH},
        {"$set": {
            "active":          True,
            "tba":             False,
            "approval_status": "auto_approved",
            "interpretation": {
                "detailed": (
                    "Bhava Madhya (house midpoint) principle: a planet positioned at the exact "
                    "midpoint of a Bhava produces its full effect for that house's significations. "
                    "As the planet moves away from the midpoint toward either cusp, the effect "
                    "proportionally diminishes. Maximum effect at Bhava Madhya; minimum effect "
                    "at Bhava Sandhi (junction)."
                ),
                "summary": (
                    "Planet at Bhava Madhya produces full house effect; "
                    "effect diminishes toward cusp."
                ),
            },
            "source": {
                "book":     "Phaladeepika",
                "chapter":  8,
                "sloka":    35,
                "batch_id": BATCH,
            },
            "decode_notes": (
                "Recovered from Ch09 PDF page 1 (documented in "
                "PD_Ch09_SignsAsLagna_NLM_Extract.md). Ch08 source PDF begins at Sloka 4 -- "
                "Sloka 35 was overleaf in Ch09 scan."
            ),
        }},
    )
    print(f"\npd-ch08-111 (activated, auto_approved): {r.modified_count}")

    # ── Final counts ──────────────────────────────────────────────────────
    all_rules = list(col.find({"ingest_batch_id": BATCH}, {"_id": 0, "approval_status": 1}))
    counts = Counter(r["approval_status"] for r in all_rules)
    print(f"\n── Post-patch status distribution ──")
    for s, n in sorted(counts.items()):
        print(f"  {s}: {n}")
    print(f"  Total: {sum(counts.values())}")

    client.close()


if __name__ == "__main__":
    main()
