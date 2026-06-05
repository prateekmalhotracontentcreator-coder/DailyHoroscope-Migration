#!/usr/bin/env python3
"""Bucket B triage patch for Lal Kitab -- bulk_write version (single round-trip).

Run from repo root:
    python3 backend/scripts/patch_lalkitab_bucket_b.py --dry-run
    python3 backend/scripts/patch_lalkitab_bucket_b.py
"""
from __future__ import annotations
import argparse, os, sys
from datetime import datetime, timezone
from pathlib import Path
from pymongo import MongoClient, UpdateOne

BATCH_ID = "lalkitab_all_v2_20260605"
LOG_DIR  = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")
TS       = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
LOG_PATH = LOG_DIR / f"patch_lalkitab_bucket_b_{TS}.log"

_buf: list[str] = []
def out(msg: str = "") -> None:
    print(msg); _buf.append(msg)
def _write_log(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(_buf) + "\n", encoding="utf-8")
    print(f"Log saved: {p}")

BUCKET_B = [
    # Truncated interpretation.summary
    ("lalkitab-ch19-001", "Bucket B: interpretation.summary truncated (old schema artefact)"),
    ("lalkitab-ch19-002", "Bucket B: interpretation.summary truncated (old schema artefact)"),
    ("lalkitab-ch19-003", "Bucket B: interpretation.summary truncated (old schema artefact)"),
    ("lalkitab-ch19-004", "Bucket B: interpretation.summary truncated (old schema artefact)"),
    ("lalkitab-ch19-005", "Bucket B: interpretation.summary truncated (old schema artefact)"),
    # LK Rina/Debt system
    ("lalkitab-ch21-debt-sun",     "Bucket B: Swayam Rina is authentic LK Ch21 concept -- validator lacks LK Rina knowledge"),
    ("lalkitab-ch21-debt-moon",    "Bucket B: Matri Rina is authentic LK Ch21 concept -- validator lacks LK Rina knowledge"),
    ("lalkitab-ch21-debt-mercury", "Bucket B: Bhagin Rina is authentic LK Ch21 concept -- validator lacks LK Rina knowledge"),
    # LK 42-section Wave Engine
    ("lalkitab-ch27-wave-w01",     "Bucket B: 42-section wave engine is LK-native concept -- validator knowledge gap"),
    ("lalkitab-ch27-wave-w02",     "Bucket B: 42-section wave engine is LK-native concept -- validator knowledge gap"),
    ("lalkitab-ch27-wave-w03",     "Bucket B: 42-section wave engine is LK-native concept -- validator knowledge gap"),
    ("lalkitab-ch27-wave-w09",     "Bucket B: LK wave sub-rule -- text-native LK, validator lacks wave framework knowledge"),
    ("lalkitab-ch27-wave-w31",     "Bucket B: 'Evil Planet' is LK source vagueness, not an encoding error"),
    ("lalkitab-ch27-wave-w44",     "Bucket B: 'Musical Note' classification is LK Ch27 native concept -- validator knowledge gap"),
    # LK-native extreme outcomes
    ("lalkitab-ch19-066",          "Bucket B: Triple Mangali is authentic LK concept -- validator knowledge gap for LK Mangali variants"),
    ("lalkitab-ch19-072",          "Bucket B: Saturn H11 abandonment is text-native LK extreme prediction -- LK makes strong house-specific claims"),
    ("lalkitab-ch20-yog-06",       "Bucket B: Mars-Saturn leprosy is text-native LK content -- extreme by classical standards, authentic to source"),
    ("lalkitab-ch20-yog-08",       "Bucket B: Venus-Ketu outcome is text-native LK content -- LK explicitly encodes physiological effects"),
    # LK schema/methodology limits
    ("lalkitab-ch20-yog-11",       "Bucket B: Varshaphalam (annual chart) schema not yet implemented -- rule valid, engine limitation"),
    ("lalkitab-ch27-transfer-h08", "Bucket B: House 8 burial protocol is authentic LK remedy -- validator ethical concern, not encoding error"),
    ("lalkitab-ch28-influence-priority", "Bucket B: Three-step propagation is LK Ch28 methodology -- complex but text-native"),
    # LOW confidence / source uncertainty
    ("lalkitab-ch27-proh-06",      "Bucket B: LOW source confidence is valid PHR, not a rejection"),
    ("lalkitab-ch27-proh-10",      "Bucket B: LOW source confidence is valid PHR, not a rejection"),
    ("lalkitab-ch27-corr-mars-benefic", "Bucket B: Source marks objects field as unverified -- PHR is correct status"),
    # LK cross-person / birth rules
    ("lalkitab-ch25-moon-h11",     "Bucket B: 52-day birth protocol is authentic LK birth-timing rule"),
    ("lalkitab-ch25-mars-mercury-sister", "Bucket B: Cross-person influence is standard LK cross-chart technique"),
    # LK formula
    ("lalkitab-ch23-formula-remainder", "Bucket B: (L+B)×3÷8 formula is LK Ch23 native -- validator lacks LK formula knowledge"),
]

STRUCTURAL_FAILURE = (
    "lalkitab-ch20-yog-07",
    "Bucket B: Structural failure -- validator Stage 4 did not write verdict to DB. Venus-Rahu content is text-native LK; moved to PHR for TT review",
)

BUCKET_C = [
    "lalkitab-ch20-yog-01", "lalkitab-ch20-yog-05", "lalkitab-ch20-yog-09",
    "lalkitab-ch20-gp-interact", "lalkitab-ch21-gp-05", "lalkitab-ch23-geoveto-triangle",
    "lalkitab-ch24-mortality-north-star", "lalkitab-ch24-mortality-reflection-organic",
    "lalkitab-ch24-mortality-reflection-mirror", "lalkitab-ch24-mortality-stasis",
    "lalkitab-ch24-age-infancy-12d", "lalkitab-ch24-age-childhood-12m",
    "lalkitab-ch24-age-sudden-death", "lalkitab-ch24-age-long-illness",
    "lalkitab-ch24-age-survival-son", "lalkitab-ch24-age-father-dependency",
    "lalkitab-ch24-age-shortlife-2y",
]


def main(dry_run: bool) -> None:
    out(f"LOG FILE: {LOG_PATH}")
    out(f"{'=' * 70}")
    out(f"LAL KITAB -- Bucket B Triage Patch (bulk_write, sync pymongo)")
    out(f"Batch: {BATCH_ID}  |  Dry-run: {dry_run}")
    out(f"{'=' * 70}")
    out()

    url = os.environ.get("MONGO_URL")
    if not url:
        out("ERROR: MONGO_URL not set")
        _write_log(LOG_PATH); sys.exit(1)

    client = MongoClient(url)
    col    = client["horoscope_db"]["interpretation_rules"]

    # ── Group 1: Bucket B flagged → PHR (single bulk_write) ───────────────────
    out(f"Group 1 -- Bucket B flagged → PHR ({len(BUCKET_B)} rules, bulk_write)")
    ops_b = [
        UpdateOne(
            {"rule_id": rid, "approval_status": "flagged"},
            {"$set": {
                "approval_status": "pending_human_review",
                "validator_error":  True,
                "triage_note":      note,
                "triage_bucket":    "B",
            }}
        )
        for rid, note in BUCKET_B
    ]
    if not dry_run:
        result = col.bulk_write(ops_b, ordered=False)
        out(f"  Matched / Modified: {result.matched_count} / {result.modified_count}")
    else:
        for rid, _ in BUCKET_B:
            out(f"  [DRY] {rid}")
        out(f"  Would update: {len(BUCKET_B)} rules")
    out()

    # ── Group 2: Structural failure → PHR ─────────────────────────────────────
    out(f"Group 2 -- Structural failure → PHR (1 rule)")
    rid_sf, note_sf = STRUCTURAL_FAILURE
    if not dry_run:
        r = col.update_one(
            {"rule_id": rid_sf},
            {"$set": {
                "approval_status": "pending_human_review",
                "validator_error":  True,
                "triage_note":      note_sf,
                "triage_bucket":    "B",
            }}
        )
        out(f"  OK   {rid_sf} -- modified: {r.modified_count}")
    else:
        out(f"  [DRY] {rid_sf}")
    out()

    # ── Group 3: Restore interpretation.summary for 5 Ch19 truncated rules ────
    out(f"Group 3 -- Truncated interpretation.summary fix (5 Ch19 rules, bulk_write)")
    ch19_rids = [rid for rid, _ in BUCKET_B[:5]]
    docs = list(col.find(
        {"rule_id": {"$in": ch19_rids}},
        {"_id": 0, "rule_id": 1, "summary": 1}
    ))
    sum_map = {d["rule_id"]: d.get("summary", "") for d in docs}

    ops_g3 = [
        UpdateOne(
            {"rule_id": rid},
            {"$set": {"interpretation.summary": sum_map.get(rid, "")}}
        )
        for rid in ch19_rids if sum_map.get(rid)
    ]
    if not dry_run and ops_g3:
        result3 = col.bulk_write(ops_g3, ordered=False)
        out(f"  Matched / Modified: {result3.matched_count} / {result3.modified_count}")
        for rid in ch19_rids:
            s = sum_map.get(rid, "")
            out(f"  OK   {rid}: interpretation.summary restored ({len(s)} chars)")
    else:
        for rid in ch19_rids:
            s = sum_map.get(rid, "")
            out(f"  [DRY] {rid}: interpretation.summary ({len(s)} chars)")
    out()

    # ── Bucket C summary ───────────────────────────────────────────────────────
    out(f"Bucket C -- stay flagged ({len(BUCKET_C)} rules, no action)")
    for rid in BUCKET_C:
        out(f"  {rid}")
    out()

    # ── Final counts ───────────────────────────────────────────────────────────
    out("── Post-patch counts ─────────────────────────────────────────────────")
    if not dry_run:
        aa  = col.count_documents({"source.batch_id": BATCH_ID, "approval_status": "auto_approved"})
        phr = col.count_documents({"source.batch_id": BATCH_ID, "approval_status": "pending_human_review"})
        fl  = col.count_documents({"source.batch_id": BATCH_ID, "approval_status": "flagged"})
        pr  = col.count_documents({"source.batch_id": BATCH_ID, "approval_status": "pending_review"})
        out(f"  auto_approved        : {aa}")
        out(f"  pending_human_review : {phr}")
        out(f"  flagged              : {fl}")
        out(f"  pending_review       : {pr}")
        out(f"  TOTAL                : {aa + phr + fl + pr}")
    else:
        out("  (dry-run -- no DB counts)")

    client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        main(args.dry_run)
    except Exception as exc:
        out(f"\nFATAL ERROR: {exc}")
        import traceback
        out(traceback.format_exc())
    finally:
        _write_log(LOG_PATH)
