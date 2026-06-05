#!/usr/bin/env python3
"""
BPHS Ch.52 Flagged Rules Triage Patch
======================================
Triages the 3 flagged rules from the Ch.52 (Sun MD) validate report.
All 3 confirmed authentic via Santhanam BPHS Vol 2 PDF -- validator errors.

Rules:
  R-BPHS52-040  → PDF CONFIRMED (encoding error noted: condition "own sign" → "debilitation sign")
  R-BPHS52-137  → PDF CONFIRMED (validator wrongly rejected maraka-lord-disease doctrine)
  R-BPHS52-138  → PDF CONFIRMED (validator wrongly rejected explicit "premature death" statement)

Action: flagged → pending_human_review + validator_error:true + C_pdf_confirmed

Usage (MONGO_URL must be exported in your terminal session):
  python3 backend/scripts/patch_bphs_ch52_flagged_triage.py            # dry run
  python3 backend/scripts/patch_bphs_ch52_flagged_triage.py --live     # write to DB
"""

import sys
import os
from datetime import datetime, timezone

DRY_RUN = "--live" not in sys.argv

TRIAGE_DATE    = "2026-06-03"
TRIAGE_SESSION = "bphs-ch52-flagged-triage-20260603"

# ---------------------------------------------------------------------------
# Rules to patch
# ---------------------------------------------------------------------------
# Format: (rule_id, pdf_sloka_ref, cc_review_note)
PDF_CONFIRMED = [
    (
        "R-BPHS52-040",
        "Ch.52 slokas 21-22",
        (
            "PDF CONFIRMED -- Santhanam slokas 21-22 explicitly state 'Mars in his sign of "
            "debilitation or be weak → destruction of wealth by displeasure of King'. "
            "Rule content is authentic. ENCODING ERROR: condition_text decoded as 'own sign' "
            "but PDF clearly says 'debilitation sign'. The apparent contradiction with R-BPHS52-041 "
            "is entirely due to this mis-decode and disappears once corrected. "
            "Separate data correction required: condition → 'Mars in his sign of debilitation or be weak'."
        ),
    ),
    (
        "R-BPHS52-137",
        "Ch.52 slokas 69-73",
        (
            "PDF CONFIRMED -- Santhanam slokas 69-73 explicitly state: 'If Venus be the lord of "
            "the 7th (and 2nd) there will be pains in the body and possibility of suffering from "
            "diseases.' Validator incorrectly claimed maraka lordship cannot cause disease. "
            "BPHS makes this link explicitly throughout antardasha chapters (same pattern confirmed "
            "in Ch.53-58 triage). Validator error."
        ),
    ),
    (
        "R-BPHS52-138",
        "Ch.52 slokas 69-73",
        (
            "PDF CONFIRMED -- Santhanam slokas 69-73 explicitly state: 'There will be premature "
            "death if Venus be associated with the lord of the 6th or 8th.' Validator called it "
            "'extreme' and 'lacking textual support' but the citation is verbatim in the PDF. "
            "Validator error."
        ),
    ),
]

# ---------------------------------------------------------------------------

def run():
    # Compute log path first so it appears in the header
    log_dir  = "KE_TEXTBOOK_DECODE/Dedup_Reports"
    mode_tag = "dryrun" if DRY_RUN else "live"
    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = f"{log_dir}/patch_bphs_ch52_flagged_triage_{ts}_{mode_tag}.log"
    os.makedirs(log_dir, exist_ok=True)

    # tee helper -- prints to stdout and buffers for log file
    buf = []
    def out(msg=""):
        print(msg)
        buf.append(msg)

    SEP = "=" * 75

    out(SEP)
    out(f"  LOG FILE: {log_path}")
    out(SEP)
    out()
    out("BPHS Ch.52 Flagged Triage Patch")
    out(f"Mode        : {'🟡 DRY RUN -- no changes' if DRY_RUN else '🔴 LIVE -- WRITING TO DB'}")
    out(f"Confirmed   : {len(PDF_CONFIRMED)} rules → PHR + validator_error:True + C_pdf_confirmed")
    out(f"Source      : Santhanam BPHS Vol 2 PDF, triage session {TRIAGE_DATE}")
    out()

    if not DRY_RUN:
        from db_connect import get_collection
        col = get_collection("interpretation_rules")

    now_str    = datetime.now(timezone.utc).isoformat()
    patched    = 0
    skipped    = 0
    not_found  = 0

    out("─" * 75)
    out(f"{'#':<5} {'Rule ID':<35} {'Pre-status':<20} Result")
    out("─" * 75)

    for i, (rule_id, sloka_ref, note) in enumerate(PDF_CONFIRMED, 1):
        if DRY_RUN:
            out(f"  {i:<3}  {rule_id:<35} {'flagged':<20} 🟡 DRY RUN  [{sloka_ref}]")
            patched += 1
            continue

        rule = col.find_one({"rule_id": rule_id})
        if not rule:
            out(f"  {i:<3}  {rule_id:<35} {'NOT FOUND':<20} ❌ SKIPPED")
            not_found += 1
            continue

        pre_status = rule.get("approval_status", "unknown")

        update = {
            "$set": {
                "approval_status":                  "pending_human_review",
                "validation.validator_error":       True,
                "validation.api_verdict":           None,
                "validation.pdf_verified":          True,
                "validation.pdf_sloka_ref":         sloka_ref,
                "validation.cc_review_note":        note,
                "validation.triage_date":           TRIAGE_DATE,
                "validation.triage_session":        TRIAGE_SESSION,
                "validation.triage_bucket":         "C_pdf_confirmed",
                "updated_at":                       now_str,
            }
        }

        result = col.update_one({"rule_id": rule_id}, update)
        if result.modified_count == 1:
            out(f"  {i:<3}  {rule_id:<35} {pre_status:<20} ✅ PATCHED  [{sloka_ref}]")
            patched += 1
        else:
            out(f"  {i:<3}  {rule_id:<35} {pre_status:<20} ⚠️  NO CHANGE (already patched?)")
            skipped += 1

    out()
    out(SEP)
    out("SUMMARY")
    out(f"  Mode      : {'DRY RUN' if DRY_RUN else 'LIVE'}")
    out(f"  Total     : {len(PDF_CONFIRMED)}")
    out(f"  Patched   : {patched} / {len(PDF_CONFIRMED)}")
    if skipped:
        out(f"  No-change : {skipped}")
    if not_found:
        out(f"  Not found : {not_found}")
    out()
    out("ENCODING ERROR NOTED (separate data correction task):")
    out("  R-BPHS52-040 : condition_text 'own sign' → should be 'debilitation sign'")
    out("                 (mis-decode of sloka 21 -- PDF says 'sign of debilitation or be weak')")
    out()
    if DRY_RUN:
        out("Re-run with --live to apply.")
    out()
    out(f"Log saved: {log_path}")

    # Write full buffered output to log file
    with open(log_path, "w") as f:
        f.write("\n".join(buf) + "\n")


if __name__ == "__main__":
    run()
