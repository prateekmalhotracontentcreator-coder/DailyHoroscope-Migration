#!/usr/bin/env python3
"""
patch_bphs_vol2_phase1_c_metadata.py

Patches 61 Bucket C_metadata rules from BPHS Vol 2 Phase 1 triage.

C_metadata = condition metadata encoding error (NOT a doctrinal error).
The interpretation text is correct per BPHS source, but condition fields
(dasha_lord / antardasha_planet / planets_involved) were incorrectly
encoded at ingest time. The validator correctly spotted structural
inconsistency between condition metadata and interpretation text.

Treatment: flagged → pending_human_review + validator_error:true
           + cc_note identifying the specific encoding fix needed.

Grouped by batch-level root cause:
  Ch47 (20 rules): dasha_lord set to Sun for entire batch, overwriting
                   antardasha context (Moon AD, Ketu AD, Saturn AD, Venus AD)
  Ch53 (15 rules): dasha_lord set to Venus for Moon Mahadasha rules, or
                   antardasha_planet assigned wrong planet
  Ch54 ( 6 rules): antardasha_planet/dasha_lord mismatches (Mars batch)
  Ch55 ( 2 rules): antardasha_planet mismatches (Rahu batch)
  Ch56 ( 8 rules): antardasha_planet set to Jupiter for all non-Jupiter rules
  Ch57 ( 7 rules): antardasha_planet/dasha_lord mismatches (Saturn batch)
  Ch58 ( 3 rules): dasha_lord/planet mismatches (Mercury batch)

Dry run by default. Pass --live to apply.

Usage:
  MONGO_URL=<url> python3 backend/scripts/patch_bphs_vol2_phase1_c_metadata.py
  MONGO_URL=<url> python3 backend/scripts/patch_bphs_vol2_phase1_c_metadata.py --live
"""
import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR        = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")
TRIAGE_DATE    = "2026-06-03"
TRIAGE_SESSION = "bphs-vol2-ph1-triage-20260603"

# ── Shared note templates by batch ────────────────────────────────────────────
_CH47 = (
    "C_metadata -- Ch47 (Sun Mahadasha) batch encoding error: condition metadata "
    "`dasha_lord` set to Sun for entire batch, overwriting antardasha context. "
    "Interpretation text correctly describes Antardasha-period effects "
    "(Moon AD / Ketu AD / Saturn AD / Venus AD in Sun Mahadasha). "
    "`antardasha_planet` field requires re-encoding from source text. "
    "Rule content is correct per BPHS Ch.47 source. Pending TT condition-metadata correction."
)
_CH53 = (
    "C_metadata -- Ch53 (Moon Mahadasha) batch encoding error: condition metadata "
    "`dasha_lord` set to 'Venus' (wrong -- Ch53 is Moon Mahadasha) or "
    "`antardasha_planet` assigned incorrect planet. Interpretation text correctly "
    "describes Moon Mahadasha antardasha results. Condition structure requires "
    "re-encoding of `dasha_lord` (→ Moon) and `antardasha_planet` fields. "
    "Rule content is correct per BPHS Ch.53 source. Pending TT condition-metadata correction."
)
_CH54 = (
    "C_metadata -- Ch54 (Mars Mahadasha) batch encoding error: condition metadata "
    "`dasha_lord` or `antardasha_planet` field references Mars where the rule "
    "concerns a different planet's condition modifier. Standard BPHS multi-planet "
    "antardasha encoding -- interpretation text is correct per Ch.54. "
    "Condition structure requires planet-field re-encoding. Pending TT correction."
)
_CH55 = (
    "C_metadata -- Ch55 (Rahu Mahadasha) batch encoding error: condition metadata "
    "`antardasha_planet` field inconsistent with rule content. Interpretation text "
    "correctly describes Rahu Mahadasha antardasha results. Condition requires "
    "re-encoding. Rule content is correct per BPHS Ch.55 source. Pending TT correction."
)
_CH56 = (
    "C_metadata -- Ch56 (Jupiter Mahadasha) batch encoding error: condition metadata "
    "`antardasha_planet` set to Jupiter for rules that concern a different antardasha "
    "planet (Rahu / Saturn / Sun / Ketu). Systematic encoding error -- all rules in "
    "this group have correct interpretation text per BPHS Ch.56. `antardasha_planet` "
    "field requires re-encoding from source text. Pending TT condition-metadata correction."
)
_CH57 = (
    "C_metadata -- Ch57 (Saturn Mahadasha) batch encoding error: condition metadata "
    "`antardasha_planet` or `dasha_lord` field inconsistent with rule interpretation. "
    "Interpretation text correctly describes Saturn Mahadasha antardasha results. "
    "Condition structure requires re-encoding. Rule content is correct per BPHS Ch.57. "
    "Pending TT correction."
)
_CH58 = (
    "C_metadata -- Ch58 (Mercury Mahadasha) batch encoding error: condition metadata "
    "`dasha_lord` set to Mercury but rule concerns another planet's condition, or "
    "`antardasha_planet` field assigned wrong planet. Interpretation text is correct "
    "per BPHS Ch.58. Condition requires re-encoding. Pending TT correction."
)

# ── 61 C_metadata rules ───────────────────────────────────────────────────────
# Format: (rule_id, cc_note)  -- note overrides batch template where needed

C_METADATA = [

    # ── Ch47: Sun Mahadasha batch (20 rules) ──────────────────────────────────
    # Root cause: antardasha_planet / dasha_lord fields forced to Sun,
    # overwriting Moon / Ketu / Saturn / Venus antardasha context.

    ("R-BPHS47-PATCH-09C246",
     _CH47 + " Specific: dasha_lord=Sun, antardasha_planet=Moon but text says "
             "'Moon Dasa' -- should be 'Moon Antardasha in Sun Mahadasha.'"),
    ("R-BPHS47-PATCH-1069F7",
     _CH47 + " Specific: dasha_lord=Sun but text says 'Ketu Dasa' -- should be "
             "'Ketu Antardasha in Sun Mahadasha.'"),
    ("R-BPHS47-PATCH-2797E4",
     _CH47 + " Specific: dasha_lord=Sun, antardasha_planet=Ketu but text says "
             "'Ketu Dasa' -- interpretation text phrasing needs alignment to antardasha format."),
    ("R-BPHS47-PATCH-298CE9",
     _CH47 + " Specific: antardasha_planet=Sun but text references Moon Dasha context. "
             "antardasha_planet should be Moon."),
    ("R-BPHS47-PATCH-4A1525",
     _CH47 + " Specific: dasha_lord=Sun, antardasha_planet=Moon but text references "
             "'Moon Dasa' -- antardasha phrasing needs correction."),
    ("R-BPHS47-PATCH-67A820",
     _CH47 + " Specific: antardasha_planet=Sun but text describes Moon Dasha effects. "
             "antardasha_planet should be Moon."),
    ("R-BPHS47-PATCH-7184C5",
     _CH47 + " Specific: antardasha_planet=Sun but text references Moon Dasha. "
             "antardasha_planet should be Moon."),
    ("R-BPHS47-PATCH-7A5D78",
     _CH47 + " Specific: dasha_lord=Sun, antardasha_planet=Moon but text says "
             "'Moon Dasa'; also conflates waning Moon phase with house placement -- "
             "these are distinct condition parameters in the encoding."),
    ("R-BPHS47-PATCH-80282A",
     _CH47 + " Specific: dasha_lord=Sun with Ketu Antardasha but text says 'Ketu Dasa' -- "
             "antardasha phrasing needs alignment."),
    ("R-BPHS47-PATCH-88272C",
     _CH47 + " Specific: dasha_lord=Sun, antardasha_planet=Sun but condition_group_id "
             "references Moon-favourable context and text says 'Moon Dasha.' "
             "antardasha_planet should be Moon."),
    ("R-BPHS47-PATCH-8D595F",
     _CH47 + " Specific: dasha_lord=Sun, antardasha_planet=Sun but text references "
             "'Moon Dasha.' antardasha_planet should be Moon."),
    ("R-BPHS47-PATCH-D1922F",
     _CH47 + " Specific: dasha_lord=Sun but text says 'Saturn Dasa' -- should be "
             "'Saturn Antardasha in Sun Mahadasha.'"),
    ("R-BPHS47-PATCH-D30274",
     _CH47 + " Specific: dasha_lord and antardasha_planet both Sun but text describes "
             "Moon Dasha (Moon in kendra). antardasha_planet should be Moon."),
    ("R-BPHS47-PATCH-D5CC6E",
     _CH47 + " Specific: dasha_lord and antardasha_planet both Sun but text references "
             "'Moon in own sign during Moon Dasha.' antardasha_planet should be Moon."),
    ("R-BPHS47-PATCH-DE23B9",
     _CH47 + " Specific: dasha_lord=Sun but summary and text describe Venus Dasha/Antardasha. "
             "antardasha_planet should be Venus."),
    ("R-BPHS47-PATCH-E0CB28",
     _CH47 + " Specific: dasha_lord=Sun (Sun Mahadasha) but text says 'Ketu Dasa.' "
             "antardasha_planet should be Ketu; interpretation text phrasing needs update."),
    ("R-BPHS47-PATCH-E14959",
     _CH47 + " Specific: dasha_lord=Sun, antardasha_planet=Sun but text describes "
             "'Moon Dasha' effects. antardasha_planet should be Moon."),
    ("R-BPHS47-PATCH-E29B0D",
     _CH47 + " Specific: dasha_lord=Sun, antardasha_planet=Ketu but text says "
             "'Ketu Dasa.' May also duplicate R-BPHS47-PATCH-E0CB28 -- verify sloka ref."),
    ("R-BPHS47-PATCH-EE6596",
     _CH47 + " Specific: dasha_lord=Sun but actual period is Ketu Antardasha in Sun MD. "
             "antardasha_planet should be Ketu."),
    ("R-BPHS47-PATCH-FDF113",
     _CH47 + " Specific: condition_group encodes Saturn in Pisces (friendly_sign) but "
             "`houses_involved` and explicit sign field are missing. Summary correctly "
             "states 'Saturn in Pisces' -- condition structure needs sign encoding."),

    # ── Ch53: Moon Mahadasha batch (15 rules) ─────────────────────────────────
    # Root cause: dasha_lord set to 'Venus' (wrong) for Moon Mahadasha rules;
    # some have antardasha_planet set to 'Moon' where rule concerns another planet.

    ("R-BPHS53-PATCH-03DE50",
     _CH53 + " Specific: antardasha_planet=Moon but rule concerns Saturn in kendra "
             "(Saturn Antardasha in Moon MD). antardasha_planet should be Saturn."),
    ("R-BPHS53-PATCH-0EC9A8",
     _CH53 + " Specific: antardasha_planet=Moon but rule concerns Saturn in own sign. "
             "antardasha_planet should be Saturn."),
    ("R-BPHS53-PATCH-0F0AE5",
     _CH53 + " Specific: antardasha_planet=Moon but rule concerns Saturn in trikona. "
             "antardasha_planet should be Saturn."),
    ("R-BPHS53-PATCH-683029",
     _CH53 + " Specific: dasha_lord=Venus, antardasha_planet=Moon but rule concerns "
             "Rahu in trikona from Moon (Dasha lord). dasha_lord should be Moon."),
    ("R-BPHS53-PATCH-6CB14A",
     _CH53 + " Specific: dasha_lord=Venus but text says 'Moon Mahadasha, Sun Antardasha.' "
             "dasha_lord should be Moon; antardasha_planet should be Sun."),
    ("R-BPHS53-PATCH-76A429",
     _CH53 + " Specific: dasha_lord=Venus but text says 'Saturn Antardasha in Moon MD.' "
             "dasha_lord should be Moon; antardasha_planet should be Saturn."),
    ("R-BPHS53-PATCH-77CE04",
     _CH53 + " Specific: dasha_lord=Venus but text says 'Saturn Antardasha in Moon MD.' "
             "dasha_lord should be Moon; antardasha_planet should be Saturn. "
             "(Remedy rule -- also note this may be from a different BPHS chapter than 53.)"),
    ("R-BPHS53-PATCH-A318DE",
     _CH53 + " Specific: dasha_lord=Venus, antardasha_planet=Moon but rule concerns "
             "Jupiter weak in 8th from Moon. dasha_lord should be Moon."),
    ("R-BPHS53-PATCH-C604A1",
     _CH53 + " Specific: dasha_lord=Venus, antardasha_planet=Moon, planets_involved "
             "has Venus and Ketu -- but rule concerns Ketu in 12th from Moon Dasha lord. "
             "dasha_lord should be Moon."),
    ("R-BPHS53-PATCH-C89F02",
     _CH53 + " Specific: antardasha_planet=Moon, planets_involved lists Venus and Saturn. "
             "Rule concerns Saturn in own Navamsa during Moon MD. antardasha_planet should be Saturn."),
    ("R-BPHS53-PATCH-EB70F6",
     _CH53 + " Specific: dasha_lord=Venus, antardasha_planet=Moon but rule concerns "
             "Mars in trikona during Moon Mahadasha. dasha_lord should be Moon."),
    ("R-BPHS53-PATCH-F28C85",
     _CH53 + " Specific: dasha_lord=Venus, antardasha_planet=Mercury but text says "
             "'Mercury in 8th from Moon Dasha lord.' dasha_lord should be Moon."),
    ("R-BPHS53-PATCH-F44FC6",
     _CH53 + " Specific: dasha_lord=Venus but text says 'Mars in kendra during Moon MD.' "
             "dasha_lord should be Moon; antardasha_planet should be Mars."),
    ("R-BPHS53-PATCH-F4678B",
     _CH53 + " Specific: dasha_lord=Venus, antardasha_planet=Moon but text references "
             "Jupiter in 12th from Moon. dasha_lord should be Moon."),
    ("R-BPHS53-PATCH-F9E11F",
     _CH53 + " Specific: dasha_lord=Venus but text says 'Mercury Antardasha in Moon MD.' "
             "dasha_lord should be Moon; antardasha_planet should be Mercury."),

    # ── Ch54: Mars Mahadasha batch (6 rules) ──────────────────────────────────

    ("R-BPHS54-PATCH-267C0C",
     _CH54 + " Specific: condition assigns Rahu in 5th to Mars-Mars dasha context but "
             "the Rahu placement effects are independent of Mars period. dasha specification "
             "needs review -- antardasha_planet may be Rahu, not Mars."),
    ("R-BPHS54-PATCH-57F064",
     _CH54 + " Specific: Saturn in trikona condition during Mars MD -- antardasha_planet "
             "should be Saturn (Saturn Antardasha in Mars MD), not Mars."),
    ("R-BPHS54-PATCH-978D01",
     _CH54 + " Specific: antardasha_planet=Mars but rule concerns Sun as 2nd lord. "
             "antardasha_planet should be Sun."),
    ("R-BPHS54-PATCH-B98FFD",
     _CH54 + " Specific: dasha_lord=Mars, antardasha_planet=Mars but rule concerns "
             "Rahu in 5th from Ascendant. antardasha_planet should be Rahu."),
    ("R-BPHS54-PATCH-C3D51D",
     _CH54 + " Specific: Jupiter in 12th rule -- condition metadata has dasha_unfavourable "
             "flag with Mars/Mars dasha but rule content is about Jupiter's placement. "
             "Dasha context assignment needs review; interpretation text is correct."),
    ("R-BPHS54-PATCH-D39C3F",
     _CH54 + " Specific: condition encodes Mars MD/AD but rule concerns Mercury combust. "
             "antardasha_planet should be Mercury."),

    # ── Ch55: Rahu Mahadasha batch (2 rules) ──────────────────────────────────

    ("R-BPHS55-PATCH-03D34A",
     _CH55 + " Specific: Mercury in kendra from Rahu condition -- antardasha_planet is "
             "Rahu but should be Mercury (Mercury Antardasha in Rahu MD)."),
    ("R-BPHS55-PATCH-BCF6B4",
     _CH55 + " Specific: dasha_lord=Rahu, antardasha_planet=Rahu but rule concerns "
             "Jupiter associated with malefics. antardasha_planet should be Jupiter."),

    # ── Ch56: Jupiter Mahadasha batch (8 rules) ───────────────────────────────
    # Root cause: antardasha_planet systematically set to Jupiter for all rules
    # in Ch56, overwriting the actual antardasha planet (Rahu, Saturn, Sun, Ketu).

    ("R-BPHS56-PATCH-0003D2",
     _CH56 + " Specific: dasha_lord=Jupiter, antardasha_planet=Jupiter but rule concerns "
             "Saturn in kendra. antardasha_planet should be Saturn."),
    ("R-BPHS56-PATCH-064229",
     _CH56 + " Specific: antardasha_planet=Jupiter but rule concerns Rahu in trikona. "
             "antardasha_planet should be Rahu."),
    ("R-BPHS56-PATCH-4F443D",
     _CH56 + " Specific: antardasha_planet=Jupiter but rule concerns Sun as 2nd/7th lord. "
             "antardasha_planet should be Sun."),
    ("R-BPHS56-PATCH-6BCB5E",
     _CH56 + " Specific: condition type and planet fields contradict stated condition "
             "(Mercury in 6th from Ascendant). dasha/antardasha planet assignment needs "
             "full re-encoding from source sloka."),
    ("R-BPHS56-PATCH-931CD1",
     _CH56 + " Specific: antardasha_planet=Jupiter but rule concerns Ketu as 7th lord. "
             "antardasha_planet should be Ketu."),
    ("R-BPHS56-PATCH-A7E387",
     _CH56 + " Specific: antardasha_planet=Jupiter but rule describes Sun in kendra. "
             "antardasha_planet should be Sun."),
    ("R-BPHS56-PATCH-C18482",
     _CH56 + " Specific: dasha_lord=Jupiter, antardasha_planet=Jupiter but rule concerns "
             "Rahu associated with benefic. antardasha_planet should be Rahu."),
    ("R-BPHS56-PATCH-D52D1C",
     _CH56 + " Specific: antardasha_planet=Jupiter but rule describes Rahu in kendra. "
             "antardasha_planet should be Rahu."),

    # ── Ch57: Saturn Mahadasha batch (7 rules) ────────────────────────────────

    ("R-BPHS57-039",
     _CH57 + " Specific: rule concerns Jupiter favourable in transit during Venus AD "
             "in Saturn MD, but dasha/antardasha fields are inconsistent. Transit rules "
             "are encoded differently from placement rules -- condition structure needs "
             "transit-type encoding."),
    ("R-BPHS57-040",
     _CH57 + " Specific: rule concerns Saturn favourable in transit during Venus AD "
             "in Saturn MD with Rajayoga. Same transit-encoding issue as R-BPHS57-039. "
             "Condition structure needs transit-type encoding."),
    ("R-BPHS57-PATCH-0D45D7",
     _CH57 + " Specific: rule concerns Jupiter in 8th from Ascendant during Saturn MD "
             "but antardasha_planet=Saturn (same as dasha_lord). antardasha_planet "
             "should be Jupiter."),
    ("R-BPHS57-PATCH-1C6BF4",
     _CH57 + " Specific: condition 'Mercury associated with Sun, Mars, Rahu' -- "
             "antardasha_planet=Saturn same as dasha_lord. antardasha_planet should be "
             "Mercury (Mercury AD in Saturn MD)."),
    ("R-BPHS57-PATCH-2085B1",
     _CH57 + " Specific: antardasha_planet=Saturn same as dasha_lord but summary says "
             "'Ketu Antardasha in Saturn MD.' antardasha_planet should be Ketu."),
    ("R-BPHS57-PATCH-79CED3",
     _CH57 + " Specific: dasha_lord and antardasha_planet both Saturn but text says "
             "'Moon Antardasha in Saturn MD.' antardasha_planet should be Moon."),
    ("R-BPHS57-PATCH-9A7BCC",
     _CH57 + " Specific: condition specifies 'Rahu in Pisces' but summary and text "
             "omit sign specification. Condition sign encoding and interpretation text "
             "need alignment."),

    # ── Ch58: Mercury Mahadasha batch (3 rules) ───────────────────────────────

    ("R-BPHS58-PATCH-16D243",
     _CH58 + " Specific: dasha_lord=Mercury but rule concerns Jupiter conditions "
             "(unfavourable states). antardasha_planet should be Jupiter "
             "(Jupiter AD in Mercury MD)."),
    ("R-BPHS58-PATCH-B6420B",
     _CH58 + " Specific: condition encodes Mercury MD/AD but rule concerns Jupiter "
             "aspected by Saturn. antardasha_planet should be Jupiter."),
    ("R-BPHS58-PATCH-C446ED",
     _CH58 + " Specific: condition encodes Mercury MD but rule concerns Jupiter in 8th. "
             "antardasha_planet should be Jupiter. Possible duplicate of "
             "R-BPHS58-PATCH-B6420B -- verify sloka reference before correction."),
]


class _Tee:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._log    = open(path, "w", encoding="utf-8")
        self._stdout = sys.__stdout__
    def write(self, data: str) -> None:
        self._stdout.write(data); self._stdout.flush()
        self._log.write(data);   self._log.flush()
    def flush(self) -> None:
        self._stdout.flush(); self._log.flush()
    def close(self) -> None:
        self._log.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", default=os.environ.get("MONGO_URL", ""))
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--live",      action="store_true")
    args = parser.parse_args()

    if not args.mongo_url:
        print("ERROR: MONGO_URL env var not set."); sys.exit(1)

    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    mode     = "live" if args.live else "dryrun"
    log_path = LOG_DIR / f"patch_bphs_vol2_phase1_c_metadata_{ts}_{mode}.log"
    tee      = _Tee(log_path)
    sys.stdout = tee

    print("=" * 70)
    print(f"  LOG FILE: {log_path}")
    print("=" * 70)
    print()
    print(f"BPHS Vol 2 Phase 1 -- C_metadata Patch")
    print(f"Mode    : {'🔴 LIVE -- WRITING TO DB' if args.live else '🟡 DRY RUN -- no changes'}")
    print(f"Rules   : {len(C_METADATA)}")
    print(f"Action  : flagged → pending_human_review + validator_error:true")
    print(f"          (condition metadata encoding errors -- content correct per BPHS)")
    print()

    from pymongo import MongoClient
    col = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10_000)[args.db_name]["interpretation_rules"]

    now     = datetime.now(timezone.utc)
    patched = 0
    skipped = 0
    errors  = []

    # Chapter grouping for display
    current_ch = None

    print(f"{'#':<4} {'Rule ID':<40} {'Pre-status':<22} Result")
    print("─" * 85)

    for i, (rule_id, note) in enumerate(C_METADATA, 1):
        # Print chapter header
        ch = rule_id.split("-")[1] if "-" in rule_id else "?"
        if ch != current_ch:
            current_ch = ch
            print(f"\n  ── {ch} ──")

        existing = col.find_one({"rule_id": rule_id},
                                {"approval_status": 1, "_id": 1})
        if not existing:
            print(f"  {i:<4} {rule_id:<40} {'NOT FOUND':<22} ⚠️  SKIP")
            errors.append(f"{rule_id}: not found in DB")
            skipped += 1
            continue

        pre_status = existing.get("approval_status", "?")
        if pre_status != "flagged":
            print(f"  {i:<4} {rule_id:<40} {pre_status:<22} ⏭  SKIP (not flagged)")
            skipped += 1
            continue

        update_doc = {
            "$set": {
                "approval_status":              "pending_human_review",
                "validation.validator_error":   True,
                "validation.cc_review_note":    note,
                "validation.triage_date":       TRIAGE_DATE,
                "validation.triage_session":    TRIAGE_SESSION,
                "validation.triage_bucket":     "C_metadata",
                "updated_at":                   now,
            }
        }

        if args.live:
            result = col.update_one({"rule_id": rule_id}, update_doc)
            ok = result.modified_count == 1
            status = "✅ PATCHED" if ok else "❌ FAILED"
            if ok:
                patched += 1
            else:
                errors.append(f"{rule_id}: update returned modified_count=0")
        else:
            status = "🟡 DRY RUN"
            patched += 1

        print(f"  {i:<4} {rule_id:<40} {pre_status:<22} {status}")

    print()
    print("=" * 70)
    print(f"Summary")
    print(f"  Mode    : {'LIVE' if args.live else 'DRY RUN'}")
    print(f"  Patched : {patched} / {len(C_METADATA)}")
    print(f"  Skipped : {skipped}")
    if errors:
        print(f"  Errors  : {len(errors)}")
        for e in errors:
            print(f"    {e}")
    if not args.live:
        print()
        print("  Re-run with --live to apply.")
    print()
    print(f"Log saved: {log_path}")
    tee.close()


if __name__ == "__main__":
    main()
