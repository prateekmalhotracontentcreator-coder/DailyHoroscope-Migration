#!/usr/bin/env python3
"""
BPHS Vol 2 Encoding Corrections
=================================
Data corrections for 10 rules where field values were mis-decoded at source.
These are NOT approval-status changes -- they correct wrong field values that
were identified during Phase 1 flagged triage and Ch.52 flagged triage.

All rule IDs, corrections, and PDF references are confirmed.

Corrections:
  Ch.47  R-BPHS47-PATCH-CC30B7  dasha_lord: "Sun"   → "Jupiter"
  Ch.52  R-BPHS52-040            condition_text: "own sign" → "debilitation sign"
  Ch.53  R-BPHS53-PATCH-094A74   dasha_lord: "Venus" → "Moon"
  Ch.53  R-BPHS53-PATCH-A460E9   dasha_lord: "Venus" → "Moon"
  Ch.53  R-BPHS53-PATCH-E77E96   dasha_lord: "Venus" → "Moon"
  Ch.53  R-BPHS53-PATCH-37CB8C   houses_involved: [7] → [2, 7]
  Ch.54  R-BPHS54-PATCH-3E2164   antardasha_planet: "Mars" → "Moon"
  Ch.54  R-BPHS54-PATCH-3E8999   antardasha_planet: "Mars" → "Rahu"
  Ch.54  R-BPHS54-PATCH-6592D5   antardasha_planet: "Mars" → "Jupiter"
  Ch.57  R-BPHS57-PATCH-0727F5   condition ref point "Ascendant" → "Dasa lord (Saturn)"

Usage (MONGO_URL must be exported in your terminal session):
  python3 backend/scripts/patch_bphs_vol2_encoding_corrections.py            # dry run
  python3 backend/scripts/patch_bphs_vol2_encoding_corrections.py --live     # write to DB
"""

import sys
import os
from datetime import datetime, timezone

DRY_RUN = "--live" not in sys.argv

CORRECTION_DATE    = "2026-06-03"
CORRECTION_SESSION = "bphs-vol2-encoding-corrections-20260603"

# ---------------------------------------------------------------------------
# Corrections
# Format: (rule_id, chapter, field_path, old_value, new_value, pdf_ref, note)
# field_path uses dot notation for nested fields
# ---------------------------------------------------------------------------
CORRECTIONS = [
    (
        "R-BPHS47-PATCH-CC30B7",
        "Ch.47",
        "dasha_lord",
        "Sun",
        "Jupiter",
        "Ch.47 slokas 49-51",
        "Ch.47 is Jupiter Mahadasha chapter. Batch script incorrectly set dasha_lord=Sun. "
        "PDF confirms Jupiter MD throughout Ch.47.",
    ),
    (
        "R-BPHS52-040",
        "Ch.52",
        "condition.description",
        None,  # string replacement -- see special handling below
        None,
        "Ch.52 slokas 21-22",
        "Condition text decoded as 'own sign' but PDF sloka 21-22 clearly says "
        "'sign of debilitation or be weak'. Corrected via string replacement in condition.description.",
    ),
    (
        "R-BPHS53-PATCH-094A74",
        "Ch.53",
        "dasha_lord",
        "Venus",
        "Moon",
        "Ch.53 slokas 1-2",
        "Ch.53 is Moon Mahadasha chapter. Batch script incorrectly set dasha_lord=Venus.",
    ),
    (
        "R-BPHS53-PATCH-A460E9",
        "Ch.53",
        "dasha_lord",
        "Venus",
        "Moon",
        "Ch.53 slokas 36-38",
        "Ch.53 is Moon Mahadasha chapter. Batch script incorrectly set dasha_lord=Venus.",
    ),
    (
        "R-BPHS53-PATCH-E77E96",
        "Ch.53",
        "dasha_lord",
        "Venus",
        "Moon",
        "Ch.53 sloka 35",
        "Ch.53 is Moon Mahadasha chapter. Batch script incorrectly set dasha_lord=Venus.",
    ),
    (
        "R-BPHS53-PATCH-37CB8C",
        "Ch.53",
        "houses_involved",
        [7],
        [2, 7],
        "Ch.53 sloka 51",
        "Sloka 51 refers to maraka houses (2nd AND 7th). houses_involved was set to [7] only. "
        "Corrected to [2, 7].",
    ),
    (
        "R-BPHS54-PATCH-3E2164",
        "Ch.54",
        "antardasha_planet",
        "Mars",
        "Moon",
        "Ch.54 slokas 70-73",
        "Ch.54 batch script set antardasha_planet=Mars for multiple rules. "
        "Slokas 70-73 cover Moon antardasha in Mars Mahadasha.",
    ),
    (
        "R-BPHS54-PATCH-3E8999",
        "Ch.54",
        "antardasha_planet",
        "Mars",
        "Rahu",
        "Ch.54 slokas 9-10",
        "Ch.54 batch script set antardasha_planet=Mars. "
        "Slokas 9-10 cover Rahu antardasha in Mars Mahadasha.",
    ),
    (
        "R-BPHS54-PATCH-6592D5",
        "Ch.54",
        "antardasha_planet",
        "Mars",
        "Jupiter",
        "Ch.54 slokas 20-22",
        "Ch.54 batch script set antardasha_planet=Mars. "
        "Slokas 20-22 cover Jupiter antardasha in Mars Mahadasha.",
    ),
    (
        "R-BPHS57-PATCH-0727F5",
        "Ch.57",
        "condition.description",
        None,  # string replacement -- see special handling below
        None,
        "Ch.57 slokas 32-34",
        "Condition reference point decoded as 'from Ascendant' but Ch.57 is Saturn MD; "
        "slokas 32-34 measure house positions from the Dasa lord (Saturn), not the Ascendant. "
        "Corrected via string replacement in condition.description.",
    ),
]

# Special string replacements for condition.description fields
CONDITION_TEXT_REPLACEMENTS = {
    "R-BPHS52-040": {
        "find":    "own sign",
        "replace": "sign of debilitation",
        "also_find": "his own sign",
        "also_replace": "his sign of debilitation",
    },
    "R-BPHS57-PATCH-0727F5": {
        "find":    "from Ascendant",
        "replace": "from Dasa lord (Saturn)",
        "also_find": "from the Ascendant",
        "also_replace": "from the Dasa lord (Saturn)",
    },
}

# ---------------------------------------------------------------------------

def apply_nested_update(doc, field_path, new_value):
    """Set a nested field using dot notation. Returns the $set key and value."""
    return {field_path: new_value}


def run():
    # Compute log path first so it appears in the header
    log_dir  = "KE_TEXTBOOK_DECODE/Dedup_Reports"
    mode_tag = "dryrun" if DRY_RUN else "live"
    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = f"{log_dir}/patch_bphs_vol2_encoding_corrections_{ts}_{mode_tag}.log"
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
    out("BPHS Vol 2 -- Encoding Corrections")
    out(f"Mode        : {'🟡 DRY RUN -- no changes' if DRY_RUN else '🔴 LIVE -- WRITING TO DB'}")
    out(f"Corrections : {len(CORRECTIONS)} field-level encoding errors → corrected in-place")
    out(f"Source      : Santhanam BPHS Vol 2 PDF, confirmed session {CORRECTION_DATE}")
    out()

    if not DRY_RUN:
        from db_connect import get_collection
        col = get_collection("interpretation_rules")

    now_str   = datetime.now(timezone.utc).isoformat()
    patched   = 0
    skipped   = 0
    not_found = 0

    out("─" * 75)
    out(f"{'#':<4} {'Rule ID':<35} {'Ch':<6} {'Field':<28} Result")
    out("─" * 75)

    for i, (rule_id, chapter, field_path, old_val, new_val, pdf_ref, note) in enumerate(CORRECTIONS, 1):

        field_display = f"{field_path} (text sub)" if old_val is None else field_path

        if DRY_RUN:
            out(f"  {i:<3} {rule_id:<35} {chapter:<6} {field_display:<28} 🟡 DRY RUN  [{pdf_ref}]")
            patched += 1
            continue

        # --- LIVE MODE ---
        rule = col.find_one({"rule_id": rule_id})
        if not rule:
            out(f"  {i:<3} {rule_id:<35} {chapter:<6} {field_display:<28} ❌ NOT FOUND")
            not_found += 1
            continue

        update_dict = {
            "updated_at":                               now_str,
            "validation.encoding_corrected":            True,
            "validation.encoding_correction_date":      CORRECTION_DATE,
            "validation.encoding_correction_session":   CORRECTION_SESSION,
            "validation.encoding_correction_note":      note,
            "validation.encoding_correction_ref":       pdf_ref,
        }

        if old_val is None:
            # String replacement in condition.description (and interpretation.detailed)
            repl = CONDITION_TEXT_REPLACEMENTS[rule_id]
            current_desc = rule.get("condition", {}).get("description", "")
            new_desc = current_desc
            if repl.get("find") in new_desc:
                new_desc = new_desc.replace(repl["find"], repl["replace"])
            if repl.get("also_find") and repl["also_find"] in new_desc:
                new_desc = new_desc.replace(repl["also_find"], repl["also_replace"])

            interp_detailed = rule.get("interpretation", {}).get("detailed", "")
            new_interp = interp_detailed
            if repl.get("find") in interp_detailed:
                new_interp = interp_detailed.replace(repl["find"], repl["replace"])
            if repl.get("also_find") and repl["also_find"] in new_interp:
                new_interp = new_interp.replace(repl["also_find"], repl["also_replace"])

            if new_desc != current_desc:
                update_dict["condition.description"] = new_desc
            if new_interp != interp_detailed:
                update_dict["interpretation.detailed"] = new_interp

            if new_desc == current_desc and new_interp == interp_detailed:
                out(f"  {i:<3} {rule_id:<35} {chapter:<6} {field_display:<28} ⚠️  NO MATCH (text not found)")
                skipped += 1
                continue
        else:
            update_dict[field_path] = new_val

        result = col.update_one({"rule_id": rule_id}, {"$set": update_dict})
        if result.modified_count == 1:
            change = "text replacement applied" if old_val is None else f"{repr(old_val)} → {repr(new_val)}"
            out(f"  {i:<3} {rule_id:<35} {chapter:<6} {field_display:<28} ✅ PATCHED  [{change}]")
            patched += 1
        else:
            out(f"  {i:<3} {rule_id:<35} {chapter:<6} {field_display:<28} ⚠️  NO CHANGE (already patched?)")
            skipped += 1

    out()
    out(SEP)
    out("SUMMARY")
    out(f"  Mode        : {'DRY RUN' if DRY_RUN else 'LIVE'}")
    out(f"  Total       : {len(CORRECTIONS)}")
    out(f"  Patched     : {patched} / {len(CORRECTIONS)}")
    if skipped:
        out(f"  No-change   : {skipped}")
    if not_found:
        out(f"  Not found   : {not_found}")
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
