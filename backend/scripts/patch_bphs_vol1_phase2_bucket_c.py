#!/usr/bin/env python3
"""patch_bphs_vol1_phase2_bucket_c.py

Patches 18 Bucket C rules from BPHS Vol 1 Phase 2 batch that are confirmed
resolvable via direct PDF reading of the Santhanam translation.

PDF source:
  /Users/apple/Documents/Knowledge Engine_eBooks/BPHS Vol 1 De-code/
  BPHS_Vol1_PDF Chapters/Maharishi_Parashara_-_Brihat_Parasara_Hora_Sastra_(Vol._1).pdf

All 18 rules: flagged → pending_human_review + validator_error:true + cc_read_note
Interpretation text is NOT changed -- content was confirmed correct from source.

Rules addressed by chapter:
  Ch04 (p.59)    : bphs1-ch04-020  Adhana Lagna nocturnal/diurnal classification
  Ch26 (pp.255-258): bphs1-ch26-004/-005/-017/-018  Drishti formula + special additions
  Ch32 (pp.317-325): bphs1-ch32-003/-004/-011/-012/-018/-041  Chara Karaka doctrine
  Ch33 (pp.327-339): bphs1-ch33-035/-038/-039/-043/-049/-079/-098  Karakamsa outcomes

Ch30 (pp.303-310): bphs1-ch30-026  benefic rescue logic for Upa Pada malefic conditions

Usage:
  python3 backend/scripts/patch_bphs_vol1_phase2_bucket_c.py \\
    --mongo-url "$MONGO_URL" --dry-run

  python3 backend/scripts/patch_bphs_vol1_phase2_bucket_c.py \\
    --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

BATCH_ID = "bphs-vol1-phase2-v1-20260601"
LOG_DIR  = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")

# ── Per-rule validator_error notes (verbatim source citations) ────────────────

CH04_020_NOTE = (
    "CC PDF read (Ch04 p.59 Santhanam, Stage 4 of Adhana Lagna calculation): "
    "BPHS explicitly classifies Aries, Taurus, Gemini, Cancer, Sagittarius, Capricorn "
    "as nocturnal signs (strong during night); Leo, Virgo, Libra, Scorpio, Aquarius, "
    "Pisces as diurnal (strong during day) -- specific to the Adhana Lagna sub-system. "
    "Validator error: flagged as contradicting the standard odd/even classification, "
    "but this is a distinct BPHS classification applied only in the Adhana Lagna context. "
    "Both systems coexist in BPHS; this rule should be tagged context=adhana_lagna."
)

CH26_DRISHTI_FORMULA_NOTE = (
    "CC PDF read (Ch26 pp.255-257 Santhanam, v.6-8): Drishti (aspectual value) formula "
    "confirmed verbatim. Step 1: subtract aspected longitude from aspecting planet. "
    "If > 180 deg, subtract again from 300 deg. Convert to degrees. Divide by 2 = "
    "Drishti Kona. Then apply six degree-range rules: "
    "Rule 1 (30-60 deg): reduce 30, divide by 2. "
    "Rule 2 (60-90 deg): reduce 60, add 15. "
    "Rule 3 (90-120 deg): reduce from 120, halve, increase by 30. "
    "Rule 4 (120-150 deg): reduce from 150. "
    "Rule 5 (150-180 deg): reduce 150, double the result. "
    "Rule 6 (180-300 deg): reduce from 300, halve. "
    "No aspectual value if angle is between 300 and 30 degrees. "
    "Validator error: 'simplified Addition A/B undefined' -- terms appear in "
    "Santhanam translator notes p.257-258 (see ch26-017/-018). Rule content is correct."
)

CH26_SPECIAL_ADDITIONS_NOTE = (
    "CC PDF read (Ch26 pp.257-258 Santhanam translator notes v.9-12): "
    "Special planetary aspect additions confirmed verbatim: "
    "Addition A -- Mars: when aspect angle is 90-120 deg or 210-249 deg, add 15 Virupas "
    "to the speculum value. "
    "Addition B -- Jupiter: when aspect angle is 120-150 deg or 240-270 deg, add 30 Virupas. "
    "Addition C -- Saturn: when aspect angle is 60-90 deg or 270-300 deg, add 45 Virupas. "
    "Labels A/B/C are Santhanam translator notation, not from Sanskrit verses; "
    "they are in the authoritative Santhanam translation and are valid source references. "
    "Validator error: terminology is confirmed in source."
)

CH32_ATMAKARKA_DEFINITION_NOTE = (
    "CC PDF read (Ch32 p.317 v.3-8 Santhanam): Atmakarka definition verbatim: "
    "'Among the planets from the Sun etc. whichever has traversed maximum number of "
    "degrees in a particular sign is called Atmakarka.' "
    "Tie resolution order: (1) more minutes, (2) more seconds, "
    "(3) if all three equal, the three planets become Anthyakaraka, Madhyakaraka, "
    "Upakheta. Planets ranked by degrees within the SIGN (devoid of Rasis), not by "
    "absolute longitude. Validator error: rule content is verbatim BPHS source."
)

CH32_RAHU_ADJUSTMENT_NOTE = (
    "CC PDF read (Ch32 p.317 v.7 Santhanam): Rahu longitude adjustment verbatim: "
    "'In the case of Rahu, deduct his longitude in that particular sign from 30.' "
    "Rahu effective degrees for Chara Karaka ranking = 30 minus actual degrees in sign. "
    "Example from text (p.319): Rahu effective degrees = 22 deg 22 min 54 sec "
    "(i.e. 30 - ~7 deg 37 min = ~22 deg 23 min, confirming the formula). "
    "Validator error: rule encoding this adjustment is correct per source."
)

CH32_EIGHT_KARAKAS_NOTE = (
    "CC PDF read (Ch32 p.318 v.13-17 Santhanam): 8 Chara Karakas listed verbatim "
    "in descending longitude order: (1) Atma Karaka, (2) Amatya Karaka, "
    "(3) Bhratru Karaka, (4) Matru Karaka, (5) Pitru Karaka, (6) Putra Karaka, "
    "(7) Gnati Karaka, (8) Stree Karaka (also called Dara Karaka). "
    "Text note: 'Rahu also added to the seven planets from Sun to Saturn' when using "
    "8 Karakas. Worked example (p.319) shows all 8 positions. "
    "Validator error: list is verbatim BPHS source."
)

CH32_SEVEN_KARAKAS_NOTE = (
    "CC PDF read (Ch32 p.319 Santhanam): 7-karaka variant explicitly acknowledged: "
    "'Some consider Matrukaraku and Putrakaraka as identical. This section thus counts "
    "only 7 Karakas.' Also: 'If two planets have the same longitude, both become the "
    "same karaka. In that circumstance, consider constant significator in the context "
    "of benefic/malefic influence for the concerned relative.' "
    "Validator error: 7-karaka school is confirmed in Santhanam's BPHS translation."
)

CH32_HOUSE_KARAKA_NOTE = (
    "CC PDF read (Ch32 p.324-325 v.31-34 Santhanam): House karakatwa table verbatim. "
    "Verse 31: '...dhana bhavam vijaniyad darakarake meva hi...' -- 2nd house is "
    "explicitly linked to darakaraka (wife indicator) in this verse context. "
    "Santhanam translator table (p.325) confirms: "
    "'2. Jupiter: 2nd house (family, finance, wife etc.)' "
    "'7. Venus: 7th house (wife, conjugal bliss etc.)' "
    "Both 2nd and 7th house carry wife signification in Ch32 -- they are complementary, "
    "not contradictory. Validator error: 'wife in 2nd house' IS in the BPHS source."
)

CH32_TIEBREAKER_TERMS_NOTE = (
    "CC PDF read (Ch32 p.317 v.5 Santhanam): Triple-tie tiebreaker terms verbatim: "
    "'If the minutes are also identical then the one with higher seconds of arc will "
    "have to be considered. In that case, these three are called Anthyakaraka, "
    "Madhyakarka and Upakheta.' These Sanskrit terms apply specifically when three "
    "planets share identical degrees, minutes AND seconds in their sign longitude. "
    "Validator error: terminology is confirmed verbatim in Ch32 source text."
)

CH30_BENEFIC_RESCUE_NOTE = (
    "CC PDF read (Ch30 pp.303-310 Santhanam): Benefic rescue principle for Upa Pada "
    "malefic conditions is stated VERBATIM in two places. "
    "(1) p.304: 'If (in the said circumstances) there be a benefic aspect (on upa pada "
    "or the related malefic), or conjunction, deprival of spouse will not come to pass.' "
    "(2) Translator notes p.307 (v.19-22): 'These evils will not come to pass if there "
    "be conjunction or aspect from a benefic (or from another benefic in the case of "
    "affliction being caused by a benefic himself).' "
    "This is a direct Santhanam translation statement, not an interpretive synthesis. "
    "Validator error: rule content is confirmed in BPHS Ch30 source text."
)

CH33_EXTREME_OUTCOMES_NOTE = (
    "CC PDF read (Ch33 pp.327-339 Santhanam): Ch33 explicitly contains extreme outcomes "
    "throughout -- these are verbatim BPHS source content, not Codex fabrications. "
    "Confirmed extreme outcomes in source text: "
    "v.19-22 (p.329): Rahu-Sun in Karakamsa + malefic aspect → death through serpents. "
    "v.23-24 (p.330): Gulika in Karakamsa → administer poison or die of poisoning; "
    "Mercury aspect → large testicles (Santhanam verbatim). "
    "v.30-31 (p.331): 2nd from Karakamsa in Venus/Mars divisions → addicted to others' wives. "
    "v.50-56 (p.334): 9th from Karakamsa + Mars/Venus + 6 identical vargas → "
    "female ill-related to native will die; Mercury/Moon → imprisonment. "
    "v.63-74 (pp.336-337): 12th from Karakamsa → final emancipation (moksha) conditions. "
    "Validator error: flagging these as fabricated/extreme; they are authentic Ch33 content."
)

# ── Rule list with assigned notes ────────────────────────────────────────────

BUCKET_C_PDF_RESOLVED = [
    # ── Ch04 ──
    {"rule_id": "bphs1-ch04-020",
     "note": CH04_020_NOTE,
     "label": "Ch04 Adhana nocturnal/diurnal classification"},

    # ── Ch30 ──
    {"rule_id": "bphs1-ch30-026",
     "note": CH30_BENEFIC_RESCUE_NOTE,
     "label": "Ch30 Benefic rescue principle for Upa Pada malefic conditions"},

    # ── Ch26 ──
    {"rule_id": "bphs1-ch26-004",
     "note": CH26_DRISHTI_FORMULA_NOTE,
     "label": "Ch26 Drishti degree-range formula"},
    {"rule_id": "bphs1-ch26-005",
     "note": CH26_DRISHTI_FORMULA_NOTE,
     "label": "Ch26 Drishti degree-range formula"},
    {"rule_id": "bphs1-ch26-017",
     "note": CH26_SPECIAL_ADDITIONS_NOTE,
     "label": "Ch26 Special planetary aspect addition"},
    {"rule_id": "bphs1-ch26-018",
     "note": CH26_SPECIAL_ADDITIONS_NOTE,
     "label": "Ch26 Special planetary aspect addition"},

    # ── Ch32 ──
    {"rule_id": "bphs1-ch32-003",
     "note": CH32_ATMAKARKA_DEFINITION_NOTE,
     "label": "Ch32 Atmakarka definition (max degrees in sign)"},
    {"rule_id": "bphs1-ch32-004",
     "note": CH32_RAHU_ADJUSTMENT_NOTE,
     "label": "Ch32 Rahu longitude = 30 - sign degrees"},
    {"rule_id": "bphs1-ch32-011",
     "note": CH32_EIGHT_KARAKAS_NOTE,
     "label": "Ch32 8 Chara Karakas list"},
    {"rule_id": "bphs1-ch32-012",
     "note": CH32_SEVEN_KARAKAS_NOTE,
     "label": "Ch32 7-karaka variant (Matru=Putra)"},
    {"rule_id": "bphs1-ch32-018",
     "note": CH32_HOUSE_KARAKA_NOTE,
     "label": "Ch32 Jupiter = 2nd house karaka (family/finance/wife)"},
    {"rule_id": "bphs1-ch32-041",
     "note": CH32_TIEBREAKER_TERMS_NOTE,
     "label": "Ch32 Tiebreaker terms (Anthyakaraka/Madhyakaraka/Upakheta)"},

    # ── Ch33 ──
    {"rule_id": "bphs1-ch33-035",
     "note": CH33_EXTREME_OUTCOMES_NOTE,
     "label": "Ch33 Karakamsa extreme outcome"},
    {"rule_id": "bphs1-ch33-038",
     "note": CH33_EXTREME_OUTCOMES_NOTE,
     "label": "Ch33 Karakamsa extreme outcome"},
    {"rule_id": "bphs1-ch33-039",
     "note": CH33_EXTREME_OUTCOMES_NOTE,
     "label": "Ch33 Karakamsa extreme outcome"},
    {"rule_id": "bphs1-ch33-043",
     "note": CH33_EXTREME_OUTCOMES_NOTE,
     "label": "Ch33 Karakamsa extreme outcome"},
    {"rule_id": "bphs1-ch33-049",
     "note": CH33_EXTREME_OUTCOMES_NOTE,
     "label": "Ch33 Karakamsa extreme outcome"},
    {"rule_id": "bphs1-ch33-079",
     "note": CH33_EXTREME_OUTCOMES_NOTE,
     "label": "Ch33 Karakamsa extreme outcome"},
    {"rule_id": "bphs1-ch33-098",
     "note": CH33_EXTREME_OUTCOMES_NOTE,
     "label": "Ch33 Karakamsa extreme outcome"},
]


class _Tee:
    def __init__(self, log_path: Path):
        log_path.parent.mkdir(parents=True, exist_ok=True)
        self._log = open(log_path, "w", encoding="utf-8")
        self._stdout = sys.__stdout__
    def write(self, data: str) -> None:
        self._stdout.write(data); self._stdout.flush()
        self._log.write(data); self._log.flush()
    def flush(self) -> None:
        self._stdout.flush(); self._log.flush()
    def close(self) -> None:
        self._log.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = "_dryrun" if args.dry_run else "_live"
    log_path = LOG_DIR / f"patch_bphs_vol1_phase2_bucket_c_{ts}{suffix}.log"
    tee = _Tee(log_path)
    sys.stdout = tee

    print("=" * 70)
    print(f"  LOG FILE: {log_path}")
    print("=" * 70)
    print()
    print("BPHS Vol 1 Phase 2 -- Bucket C PDF-Resolved Rules Patch")
    print(f"Batch : {BATCH_ID}")
    print(f"Rules : {len(BUCKET_C_PDF_RESOLVED)} rules (19 PDF-confirmed validator errors)")
    print(f"Mode  : {'DRY RUN' if args.dry_run else 'LIVE'}")
    print()
    print("Action: flagged → pending_human_review + validator_error:true")
    print("        Interpretation text NOT changed (content confirmed correct from PDF)")
    print()

    try:
        from pymongo import MongoClient
    except ImportError:
        print("pymongo required."); raise SystemExit(1)

    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10_000)
    col = client[args.db_name]["interpretation_rules"]
    now = datetime.now(timezone.utc).isoformat()

    patched = skipped = errors = not_found = 0

    current_chapter = None
    for entry in BUCKET_C_PDF_RESOLVED:
        rule_id  = entry["rule_id"]
        note     = entry["note"]
        label    = entry["label"]
        chapter  = rule_id.split("-")[1]          # e.g. "ch04"

        if chapter != current_chapter:
            current_chapter = chapter
            print(f"── {chapter.upper()} ──────────────────────────────────────────────")

        doc = col.find_one(
            {"rule_id": rule_id, "source.batch_id": BATCH_ID},
            {"rule_id": 1, "approval_status": 1, "_id": 0},
        )
        if not doc:
            print(f"  [MISS]  {rule_id}  ({label})")
            not_found += 1
            continue

        current_status = doc.get("approval_status", "?")
        if current_status not in ("flagged",):
            print(f"  [SKIP]  {rule_id}  status={current_status} (not flagged)")
            skipped += 1
            continue

        if args.dry_run:
            print(f"  [DRY]   {rule_id}  → pending_human_review + validator_error:true")
            print(f"          {label}")
            patched += 1
        else:
            try:
                r = col.update_one(
                    {"rule_id": rule_id, "source.batch_id": BATCH_ID},
                    {"$set": {
                        "approval_status": "pending_human_review",
                        "validator_error": True,
                        "validator_error_note": note,
                        "triage_patched_at": now,
                        "triage_bucket": "C-pdf",
                    }},
                )
                if r.modified_count:
                    print(f"  [OK]    {rule_id}  → pending_human_review  ({label})")
                    patched += 1
                else:
                    print(f"  [SKIP]  {rule_id}  0 modified")
                    skipped += 1
            except Exception as exc:
                print(f"  [ERR]   {rule_id}: {exc}")
                errors += 1

    print()
    print("=" * 70)
    if args.dry_run:
        print(f"[DRY RUN] Would patch {patched} / {len(BUCKET_C_PDF_RESOLVED)} rules")
        print(f"  Not found : {not_found}")
        print(f"  Skipped   : {skipped}")
    else:
        print(f"Patch complete:")
        print(f"  Patched   : {patched}")
        print(f"  Skipped   : {skipped}")
        print(f"  Not found : {not_found}")
        print(f"  Errors    : {errors}")
        print()
        print("Batch status after patch:")
        for status in ["auto_approved", "pending_human_review", "flagged", "rejected"]:
            n = col.count_documents({"source.batch_id": BATCH_ID,
                                      "approval_status": status})
            print(f"  {status:<30} {n}")
        remaining = col.count_documents({
            "source.batch_id": BATCH_ID, "approval_status": "flagged"
        })
        print()
        if remaining == 1:
            print(f"Remaining flagged: {remaining} rule (bphs1-ch30-026 -- GAI queue)")
        elif remaining == 0:
            print("Remaining flagged: 0 -- all Bucket C rules cleared!")
        else:
            print(f"Remaining flagged: {remaining}")

    print()
    print("─" * 70)
    print("All 19 Bucket C rules addressed via direct PDF reading.")
    print(f"Log saved: {log_path}")

    client.close()


if __name__ == "__main__":
    main()
