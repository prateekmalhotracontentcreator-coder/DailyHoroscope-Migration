#!/usr/bin/env python3
"""Schema patch for BPHS Ch27 / Ch43 / Ch44 rules.

These 103 rules were ingested 2026-05-04 using an old schema that stored
rich text inside an `interpretation.detailed` nested block.  The current
pipeline reads `full_text` at the top level.  As a result:
  - full_text is empty in MongoDB (confirmed 2026-06-04)
  - The early validator scored them on empty content
  - approval_status results (AA/PHR) are unreliable

This script reads from the authoritative source JSON files, populates:
  - full_text          ← interpretation.detailed  (full rich text)
  - summary            ← first 400 chars of interpretation.detailed
  - result             ← {"interpretation": full_text}
  - ingest_batch_id    ← new tracking batch ID
  - approval_status    ← reset to "pending_review" for re-validation

Run from repo root:
    python3 backend/scripts/patch_ch27_43_44_schema.py --dry-run
    python3 backend/scripts/patch_ch27_43_44_schema.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import motor.motor_asyncio
import asyncio

# ── config ────────────────────────────────────────────────────────────────────
PATCH_BATCH_ID = "bphs_ch27_43_44_v2_20260604"

SOURCES = [
    {
        "label": "Ch27 -- Shadbala",
        "file": Path("backend/scripts/bphs_ch27_rules.json"),
        "orig_batch": "bphs-ch27-v1-20260504",
        "expected": 28,
    },
    {
        "label": "Ch43 -- Longevity (Ayurdaya)",
        "file": Path("backend/scripts/bphs_ch43_rules.json"),
        "orig_batch": "bphs-ch43-v1-20260504",
        "expected": 35,
    },
    {
        "label": "Ch44 -- Marakas",
        "file": Path("backend/scripts/bphs_ch44_rules.json"),
        "orig_batch": "bphs-ch44-v1-20260504",
        "expected": 40,
    },
]

LOG_DIR  = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")
TS       = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
LOG_PATH = LOG_DIR / f"patch_ch27_43_44_schema_{TS}.log"

# ── tee-logging ───────────────────────────────────────────────────────────────
_buf: list[str] = []

def out(msg: str = "") -> None:
    print(msg)
    _buf.append(msg)

def _write_log(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(_buf) + "\n", encoding="utf-8")
    print(f"Log saved: {path}")


# ── helpers ───────────────────────────────────────────────────────────────────
def _extract_full_text(rule: dict) -> str:
    """Pull richest available text from old-schema interpretation block."""
    interp = rule.get("interpretation") or {}
    # Priority: detailed → full_text_passages[0] → summary
    detailed = (interp.get("detailed") or "").strip()
    if detailed:
        return detailed
    passages = interp.get("full_text_passages") or []
    if passages and isinstance(passages[0], dict):
        p = (passages[0].get("text") or "").strip()
        if p:
            return p
    return (interp.get("summary") or "").strip()


def _build_summary(full_text: str) -> str:
    """First complete sentence(s) up to ~400 chars."""
    if not full_text:
        return ""
    if len(full_text) <= 400:
        return full_text
    # Try to end on a sentence boundary
    chunk = full_text[:400]
    last_dot = chunk.rfind(". ")
    if last_dot > 100:
        return chunk[:last_dot + 1]
    return chunk.rstrip() + "..."


def _build_patch(rule: dict) -> dict:
    """Return the $set payload for MongoDB update."""
    full_text = _extract_full_text(rule)
    summary   = _build_summary(full_text)
    return {
        "full_text":        full_text,
        "summary":          summary,
        "result":           {"interpretation": full_text},
        "ingest_batch_id":  PATCH_BATCH_ID,
        "approval_status":  "pending_review",
    }


# ── validation ────────────────────────────────────────────────────────────────
def _validate_patch(rule_id: str, patch: dict) -> list[str]:
    errors: list[str] = []
    if not patch.get("full_text"):
        errors.append(f"{rule_id}: full_text is empty after extraction")
    if not patch.get("summary"):
        errors.append(f"{rule_id}: summary is empty")
    if patch.get("approval_status") != "pending_review":
        errors.append(f"{rule_id}: approval_status not pending_review")
    return errors


# ── main ──────────────────────────────────────────────────────────────────────
async def main(dry_run: bool) -> None:
    out(f"LOG FILE: {LOG_PATH}")
    out(f"{'=' * 70}")
    out(f"BPHS Ch27 / Ch43 / Ch44 -- SCHEMA PATCH")
    out(f"Patch batch ID : {PATCH_BATCH_ID}")
    out(f"Dry-run        : {dry_run}")
    out(f"{'=' * 70}")
    out()

    # ── load source files ─────────────────────────────────────────────────────
    all_patches: dict[str, dict] = {}   # rule_id → patch payload
    load_errors: list[str] = []

    for src in SOURCES:
        out(f"── {src['label']} ──────────────────────────────────────────────")
        if not src["file"].exists():
            out(f"  ERROR: source file not found: {src['file']}")
            load_errors.append(str(src["file"]))
            continue

        rules: list[dict] = json.loads(src["file"].read_text(encoding="utf-8"))
        out(f"  Source rules : {len(rules)} (expected {src['expected']})")
        if len(rules) != src["expected"]:
            out(f"  WARNING: count mismatch")

        ch_errors = 0
        for rule in rules:
            rid = rule.get("rule_id")
            if not rid:
                out(f"  WARNING: rule missing rule_id -- skipped")
                continue
            patch = _build_patch(rule)
            errs  = _validate_patch(rid, patch)
            if errs:
                for e in errs:
                    out(f"  ERROR: {e}")
                ch_errors += 1
            else:
                all_patches[rid] = patch

        out(f"  Patches built: {len([r for r in rules if r.get('rule_id') in all_patches])} / {len(rules)}")
        out(f"  Build errors : {ch_errors}")

        # Sample
        if rules:
            r0 = rules[0]
            ft = _extract_full_text(r0)
            out(f"  Sample [{r0.get('rule_id')}] full_text[:100]: {ft[:100]}")
        out()

    if load_errors:
        out(f"ABORT: {len(load_errors)} source file(s) missing")
        _write_log(LOG_PATH)
        sys.exit(1)

    out(f"Total patches ready: {len(all_patches)}")
    out()

    if dry_run:
        out("DRY-RUN complete -- no DB writes.")
        _write_log(LOG_PATH)
        return

    # ── DB patch ──────────────────────────────────────────────────────────────
    mongo_url = os.environ.get("MONGO_URL")
    if not mongo_url:
        out("ERROR: MONGO_URL not set")
        _write_log(LOG_PATH)
        sys.exit(1)

    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
    db     = client["horoscope_db"]
    col    = db["interpretation_rules"]

    patched = not_found = errors_db = 0

    for rid, patch in all_patches.items():
        try:
            result = await col.update_one(
                {"rule_id": rid},
                {"$set": patch},
            )
            if result.matched_count == 0:
                out(f"  NOT FOUND in DB: {rid}")
                not_found += 1
            else:
                patched += 1
        except Exception as exc:
            out(f"  DB ERROR {rid}: {exc}")
            errors_db += 1

    out("── DB result ─────────────────────────────────────────────────────────")
    out(f"  Patched      : {patched}")
    out(f"  Not found    : {not_found}")
    out(f"  DB errors    : {errors_db}")
    out()

    # ── post-patch verification ───────────────────────────────────────────────
    out("── Post-patch verification ───────────────────────────────────────────")
    for src in SOURCES:
        batch = src["orig_batch"]
        total       = await col.count_documents({"source.batch_id": batch})
        with_ft     = await col.count_documents({"source.batch_id": batch, "full_text": {"$exists": True, "$ne": ""}})
        pending_rev = await col.count_documents({"source.batch_id": batch, "approval_status": "pending_review"})
        out(f"  {src['label']:35s}: total={total} | full_text={with_ft}/{total} | pending_review={pending_rev}")

    total_all   = await col.count_documents({"ingest_batch_id": PATCH_BATCH_ID})
    pending_all = await col.count_documents({"ingest_batch_id": PATCH_BATCH_ID, "approval_status": "pending_review"})
    out()
    out(f"  ingest_batch_id={PATCH_BATCH_ID}: {total_all} rules, {pending_all} pending_review")

    if patched == 103 and not_found == 0 and errors_db == 0:
        out()
        out("✓ All 103 rules patched. Re-run AI validator on these rules next.")
        out(f"  Validation command:")
        out(f"    python3 backend/knowledge_engine.py --validate-batch {PATCH_BATCH_ID}")
    else:
        out()
        out(f"WARNING: expected 103 patches, got {patched}. Check errors above.")

    client.close()
    _write_log(LOG_PATH)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    asyncio.run(main(args.dry_run))
