#!/usr/bin/env python3
"""
prep_bphs_phase2_dedup_folders.py
--------------------------------------------------------------------
Creates two temp folders for BPHS Vol 1 Phase 2 pre-ingest dedup:

  /tmp/bphs_phase1_rules/   ← Phase 1 source Rule JSONs (already ingested)
  /tmp/bphs_phase2_rules/   ← Phase 2 source Rule JSONs (about to be ingested)

ke_dedup_script.py requires two separate folder arguments.
Phase 1 and Phase 2 files sit in the same BPHS_CC_Decode folder,
so this script separates them before the dedup run.

After running this script, run:
  python3 backend/ke_dedup_script.py \
    --folder-a /tmp/bphs_phase2_rules/ \
    --folder-b /tmp/bphs_phase1_rules/ \
    --output-report backend/scripts/dedup_reports/dedup_bphs_phase2_vs_phase1.json \
    --threshold 0.82

Then review the report before ingesting.
"""

import shutil
from pathlib import Path

DECODE_FOLDER = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode"
)

PHASE1_DEST = Path("/tmp/bphs_phase1_rules")
PHASE2_DEST = Path("/tmp/bphs_phase2_rules")

# Phase 1 chapters -- already in MongoDB, use as comparison baseline
PHASE1_CHAPTERS = [12,13,14,15,16,17,18,19,20,21,22,23,24,27,34,35,36,37,38,39,40,41,42,43,44]

# Phase 2 chapters -- about to be ingested, these are being checked
PHASE2_CHAPTERS = [3,4,5,6,7,8,9,10,11,25,26,28,29,30,31,32,33]


def copy_chapter_files(chapters: list, dest: Path, label: str) -> int:
    dest.mkdir(parents=True, exist_ok=True)
    # Clear any stale files from a previous run
    for f in dest.glob("*.json"):
        f.unlink()

    copied = 0
    missing = []

    for ch in chapters:
        # Match files like BPHS_Ch03_*_Rules*.json or BPHS_Ch3_*_Rules*.json
        patterns = [
            f"BPHS_Ch{ch:02d}_*_Rules*.json",
            f"BPHS_Ch{ch}_*_Rules*.json",
        ]
        matched = []
        for pattern in patterns:
            matched.extend(DECODE_FOLDER.glob(pattern))
        # Remove duplicates
        matched = list({f.name: f for f in matched}.values())

        if not matched:
            missing.append(ch)
            continue

        for f in sorted(matched):
            shutil.copy2(f, dest / f.name)
            copied += 1

    print(f"\n{label}")
    print(f"  Dest folder : {dest}")
    print(f"  Files copied: {copied}")
    if missing:
        print(f"  ⚠  No Rule JSON found for chapters: {missing}")
    return copied


def main():
    print("=" * 60)
    print("BPHS Phase 2 Dedup Folder Prep")
    print("=" * 60)

    if not DECODE_FOLDER.exists():
        print(f"\n❌ Decode folder not found: {DECODE_FOLDER}")
        return

    p1 = copy_chapter_files(PHASE1_CHAPTERS, PHASE1_DEST, "Phase 1 (already ingested)")
    p2 = copy_chapter_files(PHASE2_CHAPTERS, PHASE2_DEST, "Phase 2 (to be ingested)")

    print(f"\n{'=' * 60}")
    print("READY. Run dedup with:")
    print(f"{'=' * 60}")
    print(f"""
cd /Users/apple/DailyHoroscope-Migration

python3 backend/ke_dedup_script.py \\
  --folder-a {PHASE2_DEST} \\
  --folder-b {PHASE1_DEST} \\
  --threshold 0.82 \\
  --output-report backend/scripts/dedup_reports/dedup_bphs_phase2_vs_phase1.json

# Review the report, then paste summary to Claude.
""")

    if p1 == 0 or p2 == 0:
        print("⚠  One or both folders are empty. Check decode folder path and chapter file names.")


if __name__ == "__main__":
    main()
