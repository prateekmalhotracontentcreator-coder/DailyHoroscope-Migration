#!/usr/bin/env python3
"""patch_bphs_vol1_phase1_conflicts.py

Patches the BPHS Vol 1 Phase 1 side of the 29 polarity conflicts found
during the BPHS Vol 1 Phase 2 retroactive dedup run.

Background
----------
The Phase 2 dedup (retroactive_dedup_bphs_vol1_phase2.sh) loaded ALL chapters
from BPHS_CC_Decode/ (Phase 1 + Phase 2). All 29 polarity conflicts are
Phase 1 rules (Ch12, Ch14, Ch16-18, Ch42) -- not Phase 2 rules.

Phase 1 BPHS rules in MongoDB were ingested with old scripts (no batch_id
tracking). They live in the "unknown" source_book group with rule IDs like
R-BPHS17-*, R-BPHS18-*, etc. -- NOT the bphs1-ch17-* IDs in the local
decode files.

This script:
  1. Reads dedup_bphs_vol1_phase2_vs_mongodb_positional.json
  2. Extracts the 29 Phase 1 polarity conflicts (A-side in Ch12-18/42)
  3. For each, searches MongoDB by content fragment from rule_a_full_text
     (first 60 chars, cleaned to key phrase) in interpretation.detailed
     where the rule has no source.batch_id (Phase 1 rules)
  4. On match: sets pending_review=True + positional_conflict_note
  5. Skips bphs1-ch42-019 (empty A-text -- no content to search by)

Usage:
  python3 backend/scripts/patch_bphs_vol1_phase1_conflicts.py \\
    --mongo-url "$MONGO_URL" --dry-run

  python3 backend/scripts/patch_bphs_vol1_phase1_conflicts.py \\
    --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPORT_PATH = Path(
    "KE_TEXTBOOK_DECODE/Dedup_Reports/"
    "dedup_bphs_vol1_phase2_vs_mongodb_positional.json"
)
LOG_DIR = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")

# Phase 2 chapters -- exclude these from Phase 1 patch
PHASE2_CHS = set(range(3, 12)) | {25, 26} | set(range(28, 34))


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


def _chapter_num(rule_id: str) -> int | None:
    m = re.search(r"ch(\d+)", rule_id)
    return int(m.group(1)) if m else None


def _search_fragment(text: str) -> str:
    """Extract a 5-7 word search phrase from rule text, skipping preamble."""
    if not text or not text.strip():
        return ""
    # Strip HTML-ish, strip leading article/pronoun
    clean = re.sub(r"[^\w\s]", " ", text).strip()
    words = clean.split()
    # Skip leading common words to get to meaningful content
    skip = {"the", "a", "an", "if", "when", "one", "will", "native", "and", "or",
            "in", "of", "is", "are", "was", "be", "to", "for", "with", "from"}
    kept = [w for w in words if w.lower() not in skip]
    # Take 5 words from the meaningful start
    return " ".join(kept[:5]) if kept else " ".join(words[:6])


def load_phase1_conflicts() -> list[dict]:
    """Load the 29 Phase 1 polarity conflicts from the Phase 2 dedup report."""
    if not REPORT_PATH.exists():
        print(f"[error] Report not found: {REPORT_PATH}", file=sys.stderr)
        print("Run retroactive_dedup_bphs_vol1_phase2.sh first.", file=sys.stderr)
        sys.exit(1)
    data = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    details = data.get("positional_conflicts_detail", [])
    phase1 = [
        d for d in details
        if d["rule_a_id"] != d["rule_b_id"]
        and d.get("relationship") == "positional_polarity_conflict"
        and (_chapter_num(d["rule_a_id"]) or 0) not in PHASE2_CHS
    ]
    return phase1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Patch BPHS Vol 1 Phase 1 positional conflicts (content-based lookup)."
    )
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = "_dryrun" if args.dry_run else "_live"
    log_path = LOG_DIR / f"patch_bphs_vol1_phase1_{ts}{suffix}.log"
    tee = _Tee(log_path)
    sys.stdout = tee
    print("============================================================")
    print(f"  LOG FILE: {log_path}")
    print("============================================================")
    print()
    print("BPHS Vol 1 Phase 1 -- Positional Conflict Patch (content-based lookup)")
    print("Source: dedup_bphs_vol1_phase2_vs_mongodb_positional.json")
    print()

    phase1_conflicts = load_phase1_conflicts()
    print(f"Phase 1 polarity conflicts loaded: {len(phase1_conflicts)}")
    print("(These are Ch12/14/16-18/42 rules from FOLDER_A that are NOT Phase 2)")
    print()

    # Group by rule_a_id to consolidate multiple conflicts on same rule
    by_rule: dict[str, list[dict]] = {}
    for d in phase1_conflicts:
        rid = d["rule_a_id"]
        by_rule.setdefault(rid, []).append(d)

    print(f"Unique Phase 1 rule IDs to patch: {len(by_rule)}")
    print()

    # Build search targets
    search_targets: list[dict] = []
    skipped_no_text: list[str] = []

    for rule_id, conflicts in sorted(by_rule.items()):
        full_text = conflicts[0].get("rule_a_full_text", "").strip()
        ch = _chapter_num(rule_id)
        frag = _search_fragment(full_text)

        if not frag:
            print(f"  [SKIP-NOTEXT] {rule_id} -- empty text, cannot search by content")
            skipped_no_text.append(rule_id)
            continue

        notes = []
        for d in conflicts:
            notes.append(
                f"positional_polarity_conflict vs {d['rule_b_id']} "
                f"on {d['positional_key']} "
                f"(A={d.get('rule_a_polarity','?')}, B={d.get('rule_b_polarity','?')})"
            )

        search_targets.append({
            "rule_id": rule_id,
            "chapter": ch,
            "text_fragment": frag,
            "full_text_prefix": full_text[:120],
            "notes": notes,
        })

    print(f"Searchable targets: {len(search_targets)}")
    if skipped_no_text:
        print(f"Skipped (no text): {skipped_no_text}")
    print()

    if not search_targets:
        print("Nothing to search for. Exiting.")
        return

    try:
        from pymongo import MongoClient
    except ImportError:
        print("pymongo required.", file=sys.stderr); raise SystemExit(1)

    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10_000)
    col = client[args.db_name]["interpretation_rules"]

    found_total = not_found = already_patched = patched = errors = 0

    for target in search_targets:
        rule_id   = target["rule_id"]
        ch        = target["chapter"]
        frag      = target["text_fragment"]
        prefix    = target["full_text_prefix"]
        notes     = target["notes"]

        print(f"--- {rule_id} (Ch{ch}) ---")
        print(f"    search: '{frag}'")

        # Search MongoDB: Phase 1 rules have no source.batch_id
        # Try exact text fragment match first, then regex
        try:
            # Build regex from fragment (case-insensitive, allow for minor wording differences)
            # Use first 3 significant words as regex
            words = frag.split()[:3]
            pattern = r".*".join(re.escape(w) for w in words)
            candidates = list(col.find(
                {
                    "source.batch_id": {"$in": [None, ""]},
                    "interpretation.detailed": {"$regex": pattern, "$options": "i"},
                },
                {"rule_id": 1, "interpretation.detailed": 1, "pending_review": 1, "_id": 0},
            ).limit(5))

            if not candidates:
                # Fallback: drop batch_id filter, but restrict to R-BPHS* IDs only.
                # Phase 1 old-ingest rules always have the R-BPHS* pattern.
                # bphs1-ch* IDs belong to Phase 2 batch -- do NOT match those.
                candidates = list(col.find(
                    {
                        "rule_id": {"$regex": r"^R-BPHS", "$options": "i"},
                        "interpretation.detailed": {"$regex": pattern, "$options": "i"},
                    },
                    {"rule_id": 1, "interpretation.detailed": 1, "pending_review": 1, "_id": 0},
                ).limit(5))

        except Exception as exc:
            print(f"    [ERR] MongoDB query failed: {exc}")
            errors += 1
            continue

        if not candidates:
            print(f"    [NOT FOUND] No match in MongoDB for fragment")
            not_found += 1
            print(f"    A-text: {prefix[:100]}")
            print()
            continue

        # Use first candidate (best match by fragment)
        match = candidates[0]
        matched_id = match["rule_id"]
        already_pr = match.get("pending_review", False)

        print(f"    [MATCH] {matched_id}")
        print(f"    text  : {str(match.get('interpretation',{}).get('detailed',''))[:100]}")

        if already_pr:
            print(f"    [SKIP] Already has pending_review=True")
            already_patched += 1
            print()
            continue

        found_total += 1
        if args.dry_run:
            print(f"    [DRY RUN] Would set pending_review=True")
            for note in notes:
                print(f"      → {note}")
        else:
            try:
                result = col.update_one(
                    {"rule_id": matched_id},
                    {"$set": {
                        "pending_review": True,
                        "positional_conflict_note": " | ".join(notes),
                        "positional_conflict_patched_at": datetime.now(timezone.utc).isoformat(),
                        "conflict_source": "bphs_phase1_retroactive_dedup_via_phase2_run",
                    }},
                )
                if result.modified_count:
                    print(f"    [OK] {matched_id} → pending_review=True")
                    patched += 1
                else:
                    print(f"    [SKIP] {matched_id} -- update returned 0 modified")
                    already_patched += 1
            except Exception as exc:
                print(f"    [ERR] {exc}")
                errors += 1
        print()

    print("=" * 60)
    if args.dry_run:
        print(f"[DRY RUN] Would patch: {found_total}")
        print(f"Not found in MongoDB : {not_found}")
        print(f"Already patched      : {already_patched}")
        print(f"Skipped (no text)    : {len(skipped_no_text)}")
    else:
        print(f"Patched              : {patched}")
        print(f"Not found in MongoDB : {not_found}")
        print(f"Already patched      : {already_patched}")
        print(f"Skipped (no text)    : {len(skipped_no_text)}")
        print(f"Errors               : {errors}")

    if not_found > 0:
        print()
        print("NOTE: 'Not found' rules are Phase 1 BPHS rules whose content could not")
        print("be matched in MongoDB. They may have been ingested under significantly")
        print("different wording, or may not exist in MongoDB at all (if the old ingestion")
        print("script skipped or transformed those verses). Manual review recommended.")

    client.close()


if __name__ == "__main__":
    main()
