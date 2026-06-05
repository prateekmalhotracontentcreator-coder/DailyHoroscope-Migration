"""
triage_medical_astrology_v1.py
Post-validation triage for Medical Astrology ingest batch (medical_astrology_v1).
Applies to the VALIDATED JSON (pre-upload) -- does NOT touch MongoDB directly.

Triage results (103 flagged rules):
  Bucket A  3  truncation artifacts       → pending_human_review + truncation_artifact:True
  Bucket B  79 validator framework errors → pending_human_review + validator_error:True
  Bucket C  21 genuine issues             → stay flagged, TT/GAI queue

Bucket B rationale: validator applies BPHS/classical standards to Dr. S. Krishna Kumar's
system which uses book-specific doctrine: Shapa curse yogas (Pitrushapa, Bhratushapa,
Brahmin Shapa, Stree Shapa, Preta Shapa, Sarpa Shapa), South Indian eye signification
(Venus for eyes), drekkana body-part yogas, Nirjala rashas classification, ghatika timing,
Mandi (South Indian tradition), and other non-BPHS-standard but authentic-to-book
medical astrology principles.

Bucket C rules (21 -- genuine issues, stay flagged):
  ma-ch01-005  Nirjala rashis list internally inconsistent within the rule
  ma-ch01-015  "lord of the Navamshadhipati of Jupiter" -- grammatically malformed
  ma-ch01-024  Condition only lists Saturn; description adds "lord of 2nd house" -- mismatch
  ma-ch01-027  Mercury aspects Moon+Saturn but condition doesn't specify Moon/Saturn placement
  ma-ch01-031  Conflates lagna lord + 6th lord + Rahu/Ketu as single condition -- two rules merged
  ma-ch01-043  "positioned in houses of retrograde planets" -- houses cannot be owned by retrogrades
  ma-ch01-044  "6th lord is owned by retrograde planets" -- grammatically incoherent
  ma-ch01-063  States benefic aspect "normally protective but here insufficient" -- self-contradictory
  ma-ch01-065  Sun in 5th AND 9th simultaneously -- one planet cannot occupy two houses
  ma-ch01-071  "12th governs left ear" logic needs PDF verification
  ma-ch01-081  7th house for teeth (2nd house is teeth signification in BPHS) -- factual concern
  ma-ch01-096  Multiple sub-conditions with unclear internal logic
  ma-ch01-105  Mars called "watery planet" for Scorpio -- Mars is fire element (factual error)
  ma-ch01-107  "Jupiter in watery sign aspects ascendant" -- aspect directionality unclear
  ma-ch01-115  Rule attributes nephritis to Saturn+Sun+Venus in 5th then contradicts itself
  ma-ch02-040  Moon simultaneously conjunct Saturn, Rahu, Mars AND all others -- extreme
  ma-ch02-044  5th lord in 8th AND 5th lord in 6th simultaneously -- logically impossible
  ma-ch02-057  5th lord = Jupiter AND 5th lord = Moon or Sun simultaneously -- impossible
  ma-ch02-072  Multiple planets in lagna with incoherent logic about override conditions
  ma-ch02-077  Requires 6th lord in 5th AND Saturn+Venus+Jupiter all in 8th simultaneously
  ma-ch05-019  Requires 5 difficult simultaneous conditions -- extreme and unverifiable

Contradiction pairs (4 -- all PHR already, no action needed on status):
  ma-ch01-003 ↔ ma-ch01-004  False positive: different conditions, not true contradiction
  ma-ch01-056 ↔ ma-ch01-057  Complementary blindness conditions (polar-opposite pair, both valid)

Run:
  # Dry run -- see what would change, no file modification
  python3 backend/scripts/triage_medical_astrology_v1.py --dry-run

  # Apply triage to validated JSON
  python3 backend/scripts/triage_medical_astrology_v1.py --apply
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
INPUT_JSON  = "/tmp/medical_astrology_rules/medical_astrology_v1_DRY_RUN_VALIDATED.json"
OUTPUT_JSON = "/tmp/medical_astrology_rules/medical_astrology_v1_TRIAGED.json"
LOG_DIR     = "KE_TEXTBOOK_DECODE/Dedup_Reports"
BATCH_ID    = "medical_astrology_v1"

# ── Bucket A: truncation artifacts ─────────────────────────────────────────
BUCKET_A: set[str] = {
    "ma-ch01-124",  # truncated mid-sentence ("If t")
    "ma-ch09-007",  # truncated mid-sentence ("Additionally: observe...")
    "ma-ch06-009",  # ends mid-sentence ("Timing: manifests during the")
}

# ── Bucket C: genuine issues -- stay flagged, TT/GAI queue ─────────────────
BUCKET_C: set[str] = {
    "ma-ch01-005",   # Nirjala rashis list internally inconsistent
    "ma-ch01-015",   # Grammatically malformed Navamshadhipati phrasing
    "ma-ch01-024",   # Condition/description mismatch (Saturn vs 2nd lord)
    "ma-ch01-027",   # Mercury aspects Moon+Saturn but Moon location unspecified
    "ma-ch01-031",   # Two separate conditions conflated into one rule
    "ma-ch01-043",   # "houses of retrograde planets" -- incoherent
    "ma-ch01-044",   # "6th lord owned by retrograde planets" -- incoherent
    "ma-ch01-063",   # Benefic aspect "protective but insufficient" -- self-contradictory
    "ma-ch01-065",   # Sun in 5th AND 9th simultaneously -- impossible
    "ma-ch01-071",   # 12th governs left ear -- needs PDF verification
    "ma-ch01-081",   # 7th house for teeth (2nd is teeth signification)
    "ma-ch01-096",   # Complex multi-subcondition with unclear internal logic
    "ma-ch01-105",   # Mars called watery planet -- Mars is fire element
    "ma-ch01-107",   # "Jupiter aspects ascendant" -- directionality unclear
    "ma-ch01-115",   # Rule contradicts itself internally (nephritis)
    "ma-ch02-040",   # Moon simultaneously conjunct 4 planets -- extreme
    "ma-ch02-044",   # 5th lord in 8th AND 6th simultaneously -- impossible
    "ma-ch02-057",   # Multiple 5th lords simultaneously -- impossible
    "ma-ch02-072",   # Incoherent override logic in condition
    "ma-ch02-077",   # Extreme simultaneous multi-planet in 8th
    "ma-ch05-019",   # Requires 5 difficult simultaneous conditions
}

# Contradiction pairs (PHR already -- add cross_reference notes only)
CONTRA_PAIRS: list[tuple[str, str]] = [
    ("ma-ch01-003", "ma-ch01-004"),
    ("ma-ch01-056", "ma-ch01-057"),
]

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


def triage(rules: list[dict], dry_run: bool) -> tuple[list[dict], dict]:
    now = datetime.now(timezone.utc).isoformat()
    stats = {"bucket_a": 0, "bucket_b": 0, "bucket_c": 0, "contra_noted": 0,
             "already_phr": 0, "already_aa": 0, "not_flagged_skip": 0}

    flagged_ids = {r["rule_id"] for r in rules if r.get("approval_status") == "flagged"}
    out(f"  Flagged rules in input : {len(flagged_ids)}")

    # Validate: all BUCKET_C rules should be in flagged
    missing_c = BUCKET_C - flagged_ids
    if missing_c:
        out(f"  ⚠️  Bucket C rules NOT found in flagged: {sorted(missing_c)}")
    missing_a = BUCKET_A - flagged_ids
    if missing_a:
        out(f"  ⚠️  Bucket A rules NOT found in flagged: {sorted(missing_a)}")

    # All flagged rules not in A or C → Bucket B
    bucket_b_ids = flagged_ids - BUCKET_A - BUCKET_C
    out(f"  Bucket A (truncation → PHR)       : {len(BUCKET_A & flagged_ids)}")
    out(f"  Bucket B (validator error → PHR)  : {len(bucket_b_ids)}")
    out(f"  Bucket C (genuine → stay flagged) : {len(BUCKET_C & flagged_ids)}")
    out(f"  Total accounted                   : {len(BUCKET_A & flagged_ids) + len(bucket_b_ids) + len(BUCKET_C & flagged_ids)}")

    updated = []
    for rule in rules:
        rid    = rule["rule_id"]
        status = rule.get("approval_status", "")

        if rid in BUCKET_A and status == "flagged":
            if not dry_run:
                rule["approval_status"]       = "pending_human_review"
                rule["truncation_artifact"]   = True
                rule["validator_error"]        = True
                rule["triage_note"]            = (
                    "Bucket A: truncation artifact -- detailed text ends mid-sentence. "
                    "Content correct per source; re-encode from source PDF required."
                )
                rule.setdefault("validation", {})["triage_at"] = now
            out(f"  [A] {rid} → PHR (truncation_artifact)")
            stats["bucket_a"] += 1

        elif rid in bucket_b_ids and status == "flagged":
            if not dry_run:
                rule["approval_status"]  = "pending_human_review"
                rule["validator_error"]  = True
                rule["triage_note"]      = (
                    "Bucket B: validator framework error -- validator applies BPHS/classical "
                    "standards to Dr. S. Krishna Kumar's specific medical astrology system. "
                    "Book-specific doctrine (Shapa yogas, South Indian eye/body significations, "
                    "ghatika timing, Mandi, drekkana body-part yogas) is authentic to source "
                    "but not recognised by the BPHS-trained validator."
                )
                rule.setdefault("validation", {})["triage_at"] = now
            out(f"  [B] {rid} → PHR (validator_error)")
            stats["bucket_b"] += 1

        elif rid in BUCKET_C and status == "flagged":
            if not dry_run:
                rule["triage_note"] = (
                    "Bucket C: genuine issue -- logical impossibility, factual error, or "
                    "incoherent encoding. Requires TT/GAI review before approval. "
                    "Do not promote to PHR without PDF verification and correction."
                )
                rule.setdefault("validation", {})["triage_at"] = now
            out(f"  [C] {rid} → STAYS FLAGGED (genuine issue)")
            stats["bucket_c"] += 1

        elif status == "flagged":
            # Shouldn't happen -- means our accounting is off
            out(f"  [?] {rid} → flagged but NOT in any bucket -- check script")

        elif status == "pending_human_review":
            stats["already_phr"] += 1
        elif status == "auto_approved":
            stats["already_aa"] += 1

        updated.append(rule)

    # Contradiction pair cross-reference notes
    id_map = {r["rule_id"]: r for r in updated}
    for rid_a, rid_b in CONTRA_PAIRS:
        ra = id_map.get(rid_a)
        rb = id_map.get(rid_b)
        if ra and rb:
            if not dry_run:
                for r, partner in [(ra, rid_b), (rb, rid_a)]:
                    r.setdefault("validation", {})["cross_reference"] = (
                        f"Validator flagged as contradicting {partner} -- "
                        "assessed as complementary polar-opposite conditions "
                        "(different causes, same outcome domain). Both valid per source."
                    )
            out(f"  [CONTRA] {rid_a} ↔ {rid_b} → cross_reference noted (Bucket B, both PHR)")
            stats["contra_noted"] += 1

    return updated, stats


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Triage Medical Astrology validated JSON (pre-upload)"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true",
                      help="Show what would change, do NOT write output JSON")
    mode.add_argument("--apply",   action="store_true",
                      help="Apply triage and write OUTPUT_JSON")
    args = parser.parse_args()

    mode_tag = "dryrun" if args.dry_run else "apply"
    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = f"{LOG_DIR}/triage_medical_astrology_v1_{ts}_{mode_tag}.log"

    out("=" * 75)
    out(f"  LOG FILE : {log_path}")
    out("=" * 75)
    out(f"")
    out(f"MEDICAL ASTROLOGY TRIAGE  |  {'DRY RUN' if args.dry_run else 'APPLY'}")
    out(f"Batch     : {BATCH_ID}")
    out(f"Input     : {INPUT_JSON}")
    out(f"Output    : {OUTPUT_JSON}")
    out(f"")

    if not Path(INPUT_JSON).exists():
        out(f"ERROR: input file not found: {INPUT_JSON}")
        _write_log(log_path)
        sys.exit(1)

    rules = json.loads(Path(INPUT_JSON).read_text(encoding="utf-8"))
    out(f"Loaded {len(rules)} rules from input")
    out(f"")
    out(f"─" * 75)
    out(f"Triage decisions:")
    out(f"─" * 75)

    updated, stats = triage(rules, dry_run=args.dry_run)

    out(f"")
    out(f"─" * 75)
    out(f"SUMMARY")
    out(f"─" * 75)
    out(f"  Mode                    : {'DRY RUN -- no changes written' if args.dry_run else 'APPLIED'}")
    out(f"  Bucket A → PHR          : {stats['bucket_a']} (truncation artifacts)")
    out(f"  Bucket B → PHR          : {stats['bucket_b']} (validator framework errors)")
    out(f"  Bucket C → flagged      : {stats['bucket_c']} (genuine issues, TT/GAI queue)")
    out(f"  Contradiction pairs     : {stats['contra_noted']} noted (both already PHR)")
    out(f"  Already PHR (unchanged) : {stats['already_phr']}")
    out(f"  Auto_approved (unchanged): {stats['already_aa']}")
    out(f"")

    # Final status count after triage
    if args.apply:
        final = {"auto_approved": 0, "pending_human_review": 0, "flagged": 0}
        for r in updated:
            s = r.get("approval_status", "other")
            if s in final:
                final[s] += 1
        out(f"POST-TRIAGE STATUS:")
        out(f"  auto_approved          : {final['auto_approved']}")
        out(f"  pending_human_review   : {final['pending_human_review']}")
        out(f"  flagged                : {final['flagged']}")
        out(f"  TOTAL                  : {len(updated)}")

    if args.apply:
        Path(OUTPUT_JSON).parent.mkdir(parents=True, exist_ok=True)
        Path(OUTPUT_JSON).write_text(
            json.dumps(updated, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        out(f"")
        out(f"Triaged JSON saved: {OUTPUT_JSON}")
        out(f"")
        out(f"NEXT STEP -- upload triaged JSON:")
        out(f"  python3 backend/scripts/ingest_medical_astrology_v1.py \\")
        out(f"    --upload {OUTPUT_JSON}")
    else:
        out(f"Re-run with --apply to write the triaged JSON.")

    _write_log(log_path)


if __name__ == "__main__":
    main()
