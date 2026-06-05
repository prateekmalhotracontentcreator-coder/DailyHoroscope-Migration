"""
patch_medical_astrology_bucket_a.py
Corrects the 3 Bucket A false-positive truncation flags in the TRIAGED JSON.

Background:
  The triage script classified ma-ch01-124, ma-ch09-007, ma-ch06-009 as
  Bucket A (truncation artifacts) based on partial AI validation output.
  Source file inspection (2026-06-04) confirmed all 3 texts are COMPLETE:
    ma-ch01-124  ends "...the severity is reduced."
    ma-ch09-007  ends "...and the dashas running at the given point of time."
    ma-ch06-009  ends "...with the bhukti of the afflicted 4th lord."

  The truncation_artifact flag was incorrectly applied. No other validator
  concerns exist for these rules. Corrective action:
    - Remove truncation_artifact: True
    - Remove validator_error: True  (set by Bucket A path, not applicable)
    - Remove triage_note (incorrect)
    - Change approval_status: pending_human_review → auto_approved
    - Add patch_note explaining the correction

Run:
  python3 backend/scripts/patch_medical_astrology_bucket_a.py --dry-run
  python3 backend/scripts/patch_medical_astrology_bucket_a.py --apply
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
INPUT_JSON  = "/tmp/medical_astrology_rules/medical_astrology_v1_TRIAGED.json"
OUTPUT_JSON = "/tmp/medical_astrology_rules/medical_astrology_v1_PATCHED.json"
LOG_DIR     = "KE_TEXTBOOK_DECODE/Dedup_Reports"

FALSE_POSITIVE_BUCKET_A: dict[str, str] = {
    "ma-ch01-124": 'ends "...the severity is reduced." -- complete sentence',
    "ma-ch09-007": 'ends "...and the dashas running at the given point of time." -- complete sentence',
    "ma-ch06-009": 'ends "...with the bhukti of the afflicted 4th lord." -- complete sentence',
}

# ---------------------------------------------------------------------------
_buf: list[str] = []


def out(msg: str = "") -> None:
    print(msg)
    _buf.append(msg)


def _write_log(log_path: str) -> None:
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    Path(log_path).write_text("\n".join(_buf) + "\n", encoding="utf-8")
    print(f"\nLog saved: {log_path}")

# ---------------------------------------------------------------------------


def patch(rules: list[dict], dry_run: bool) -> tuple[list[dict], dict]:
    now   = datetime.now(timezone.utc).isoformat()
    stats = {"patched": 0, "not_found": [], "already_clean": []}
    target_ids = set(FALSE_POSITIVE_BUCKET_A.keys())

    for rule in rules:
        rid = rule["rule_id"]
        if rid not in target_ids:
            continue

        if rule.get("approval_status") != "pending_human_review":
            out(f"  [SKIP] {rid} -- approval_status is '{rule.get('approval_status')}', expected PHR")
            stats["already_clean"].append(rid)
            continue

        source_evidence = FALSE_POSITIVE_BUCKET_A[rid]
        out(f"  [PATCH] {rid}")
        out(f"    Before : approval_status=pending_human_review  truncation_artifact=True  validator_error=True")
        out(f"    After  : approval_status=auto_approved  (flags removed)")
        out(f"    Evidence: source file confirms text {source_evidence}")

        if not dry_run:
            rule["approval_status"] = "auto_approved"
            # Remove incorrect flags
            rule.pop("truncation_artifact", None)
            rule.pop("validator_error", None)
            rule.pop("triage_note", None)
            # Add correction note
            rule["patch_note"] = (
                f"Bucket A false positive corrected {now}: "
                f"source file inspection confirmed text is complete "
                f"({source_evidence}). "
                "truncation_artifact and validator_error flags removed. "
                "Promoted to auto_approved."
            )
            rule.setdefault("validation", {})["patch_at"] = now

        stats["patched"] += 1

    for rid in target_ids:
        if rid not in {r["rule_id"] for r in rules}:
            stats["not_found"].append(rid)
            out(f"  [MISSING] {rid} -- not found in JSON")

    return rules, stats


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Patch Bucket A false-positive truncation flags in Medical Astrology TRIAGED JSON"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true",
                      help="Show what would change, do NOT write output JSON")
    mode.add_argument("--apply",   action="store_true",
                      help="Apply patch and write OUTPUT_JSON")
    args = parser.parse_args()

    mode_tag = "dryrun" if args.dry_run else "apply"
    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = f"{LOG_DIR}/patch_medastro_bucket_a_{ts}_{mode_tag}.log"

    out("=" * 75)
    out(f"  LOG FILE : {log_path}")
    out("=" * 75)
    out()
    out(f"MEDICAL ASTROLOGY -- BUCKET A PATCH  |  {'DRY RUN' if args.dry_run else 'APPLY'}")
    out(f"Input  : {INPUT_JSON}")
    out(f"Output : {OUTPUT_JSON}")
    out()
    out("Correction: 3 rules misclassified as truncation artifacts.")
    out("Source file inspection confirms all 3 texts are complete sentences.")
    out()

    if not Path(INPUT_JSON).exists():
        out(f"ERROR: input file not found: {INPUT_JSON}")
        _write_log(log_path)
        raise SystemExit(1)

    rules = json.loads(Path(INPUT_JSON).read_text(encoding="utf-8"))
    out(f"Loaded {len(rules)} rules")
    out()
    out("─" * 75)
    out("Patch decisions:")
    out("─" * 75)

    updated, stats = patch(rules, dry_run=args.dry_run)

    out()
    out("─" * 75)
    out("SUMMARY")
    out("─" * 75)
    out(f"  Mode    : {'DRY RUN -- no changes written' if args.dry_run else 'APPLIED'}")
    out(f"  Patched : {stats['patched']} rules (PHR → auto_approved, flags removed)")
    if stats["not_found"]:
        out(f"  Missing : {stats['not_found']}")
    if stats["already_clean"]:
        out(f"  Skipped : {stats['already_clean']} (already clean)")
    out()

    if args.apply:
        # Final status count
        final = {"auto_approved": 0, "pending_human_review": 0, "flagged": 0}
        for r in updated:
            s = r.get("approval_status", "other")
            if s in final:
                final[s] += 1
        out("POST-PATCH STATUS:")
        out(f"  auto_approved        : {final['auto_approved']}")
        out(f"  pending_human_review : {final['pending_human_review']}")
        out(f"  flagged              : {final['flagged']}")
        out(f"  TOTAL                : {len(updated)}")
        out()

        Path(OUTPUT_JSON).parent.mkdir(parents=True, exist_ok=True)
        Path(OUTPUT_JSON).write_text(
            json.dumps(updated, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        out(f"Patched JSON saved: {OUTPUT_JSON}")
        out()
        out("NEXT STEP -- upload patched JSON:")
        out("  python3 backend/scripts/ingest_medical_astrology_v1.py \\")
        out(f"    --upload {OUTPUT_JSON}")
    else:
        out("Re-run with --apply to write the patched JSON.")

    _write_log(log_path)


if __name__ == "__main__":
    main()
