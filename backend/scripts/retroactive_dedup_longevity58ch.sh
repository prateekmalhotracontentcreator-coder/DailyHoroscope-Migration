#!/bin/bash
# =============================================================================
# Retroactive Positional Conflict Dedup -- Longevity 58Ch (longevity_58ch_v1)
# =============================================================================
# Run from repo root: bash backend/scripts/retroactive_dedup_longevity58ch.sh
#
# What this does:
#   Runs ke_dedup_script.py (with positional conflict detector, added 2026-06-02)
#   against all 6 previously-ingested books. The earlier pre-ingest dedup used
#   the old script and has no positional_conflicts_detail section.
#
# Source: /tmp/longevity_58ch_rules/ (149 rules, 6 positional: Jupiter×H7,
#         Jupiter×H1, Mercury×[5,8,9], Sun×H11, Venus×[1,8], Venus×[1,3..10])
#
# Reports saved to: KE_TEXTBOOK_DECODE/Dedup_Reports/
# =============================================================================

set -euo pipefail

SCRIPT="backend/ke_dedup_script.py"
FOLDER_A="/tmp/longevity_58ch_rules/"
REPORTS="KE_TEXTBOOK_DECODE/Dedup_Reports"

BPHS1="/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/"
BPHS2="/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/"
PD="/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode/"
COMBO="/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredCombinations_CC_Decode/"
H300="/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredHoroscopes_CC_Decode/"
LU="/Users/apple/Documents/Knowledge Engine_eBooks/LongevityUnnatural_CC_Decode/"

mkdir -p "$REPORTS"

echo "============================================================"
echo "Longevity 58Ch -- Retroactive Positional Conflict Dedup"
echo "Source: $FOLDER_A"
echo "Reports: $REPORTS"
echo "============================================================"
echo ""

# ------------------------------------------------------------------
# Run 1: 58Ch vs Longevity Unnatural (KP x KP longevity -- HIGHEST VALUE)
# ------------------------------------------------------------------
echo "--- RUN 1/6: 58Ch vs LongevityUnnatural ---"
python3 "$SCRIPT" \
  --folder-a "$FOLDER_A" \
  --folder-b "$LU" \
  --threshold 0.82 \
  --output-report "$REPORTS/dedup_58ch_vs_lu_positional.json" \
  --dry-run
echo ""

# ------------------------------------------------------------------
# Run 2: 58Ch vs 300 Horoscopes (KP x KP -- HIGH VALUE)
# ------------------------------------------------------------------
echo "--- RUN 2/6: 58Ch vs 300_Horoscopes ---"
python3 "$SCRIPT" \
  --folder-a "$FOLDER_A" \
  --folder-b "$H300" \
  --threshold 0.82 \
  --output-report "$REPORTS/dedup_58ch_vs_h300_positional.json" \
  --dry-run
echo ""

# ------------------------------------------------------------------
# Run 3: 58Ch vs BPHS Vol 1 (KP x Classical -- Ch43/44 longevity overlap)
# ------------------------------------------------------------------
echo "--- RUN 3/6: 58Ch vs BPHS_Vol1 ---"
python3 "$SCRIPT" \
  --folder-a "$FOLDER_A" \
  --folder-b "$BPHS1" \
  --threshold 0.82 \
  --output-report "$REPORTS/dedup_58ch_vs_bphs1_positional.json" \
  --dry-run
echo ""

# ------------------------------------------------------------------
# Run 4: 58Ch vs Phaladeepika (KP x Classical commentary)
# ------------------------------------------------------------------
echo "--- RUN 4/6: 58Ch vs Phaladeepika ---"
python3 "$SCRIPT" \
  --folder-a "$FOLDER_A" \
  --folder-b "$PD" \
  --threshold 0.82 \
  --output-report "$REPORTS/dedup_58ch_vs_phaladeepika_positional.json" \
  --dry-run
echo ""

# ------------------------------------------------------------------
# Run 5: 58Ch vs 300 Combinations (KP x Classical combinations)
# ------------------------------------------------------------------
echo "--- RUN 5/6: 58Ch vs 300_Combinations ---"
python3 "$SCRIPT" \
  --folder-a "$FOLDER_A" \
  --folder-b "$COMBO" \
  --threshold 0.82 \
  --output-report "$REPORTS/dedup_58ch_vs_300combo_positional.json" \
  --dry-run
echo ""

# ------------------------------------------------------------------
# Run 6: 58Ch vs BPHS Vol 2 (KP x Classical Dasa chapters)
# ------------------------------------------------------------------
echo "--- RUN 6/6: 58Ch vs BPHS_Vol2 ---"
python3 "$SCRIPT" \
  --folder-a "$FOLDER_A" \
  --folder-b "$BPHS2" \
  --threshold 0.82 \
  --output-report "$REPORTS/dedup_58ch_vs_bphs2_positional.json" \
  --dry-run
echo ""

# ------------------------------------------------------------------
# Summary: parse all 6 reports and print consolidated counts
# ------------------------------------------------------------------
echo "============================================================"
echo "SUMMARY -- Positional Conflict Counts Across All 6 Runs"
echo "============================================================"
python3 - <<'PYEOF'
import json, os, glob

reports = {
    "58Ch vs LongevityUnnatural": "KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_58ch_vs_lu_positional.json",
    "58Ch vs 300_Horoscopes":     "KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_58ch_vs_h300_positional.json",
    "58Ch vs BPHS_Vol1":          "KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_58ch_vs_bphs1_positional.json",
    "58Ch vs Phaladeepika":       "KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_58ch_vs_phaladeepika_positional.json",
    "58Ch vs 300_Combinations":   "KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_58ch_vs_300combo_positional.json",
    "58Ch vs BPHS_Vol2":          "KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_58ch_vs_bphs2_positional.json",
}

total_matches = 0
total_contradictions = 0
total_positional = 0
total_polarity_conflicts = 0
total_alt_results = 0

for name, path in reports.items():
    try:
        data = json.load(open(path))
        m  = data.get("duplicate_candidates", 0)
        c  = data.get("contradiction_pairs", 0)
        p  = data.get("positional_conflicts", 0)
        details = data.get("positional_conflicts_detail", [])
        polarity = sum(1 for d in details if d.get("relationship") == "positional_polarity_conflict")
        alt      = sum(1 for d in details if d.get("relationship") == "positional_alternate_result")
        total_matches        += m
        total_contradictions += c
        total_positional     += p
        total_polarity_conflicts += polarity
        total_alt_results        += alt
        flag = " ⚠️  REVIEW" if p > 0 else ""
        print(f"  {name:<35s}  matches={m:>3}  contra={c:>3}  positional={p:>3}{flag}")
        if details:
            for d in details:
                print(f"    {d['relationship']:35s}  {d['rule_a_id']} <-> {d['rule_b_id']}  key={d.get('positional_key','?')}  score={d['similarity_score']:.3f}")
    except Exception as e:
        print(f"  {name:<35s}  ERROR: {e}")

print("")
print(f"  TOTALS: matches={total_matches}  contradictions={total_contradictions}  positional_conflicts={total_positional}")
print(f"    positional_polarity_conflicts: {total_polarity_conflicts}")
print(f"    positional_alternate_results:  {total_alt_results}")
if total_positional == 0:
    print("")
    print("  ✅ CLEAN -- No positional conflicts found across all 6 runs.")
    print("  Longevity 58Ch positional dedup is COMPLETE.")
else:
    print("")
    print(f"  ⚠️  {total_positional} positional conflict(s) found -- review required.")
    print("  Run: python3 backend/scripts/patch_58ch_positional_conflicts.py --mongo-url \"$MONGO_URL\" --dry-run")
    print("  Then re-run without --dry-run to apply patches.")
PYEOF

echo ""
echo "Reports saved to: KE_TEXTBOOK_DECODE/Dedup_Reports/"
echo "Next step: review summary above."
echo "  If positional_conflicts > 0: run patch_58ch_positional_conflicts.py"
echo "  If all clean: update KE TRACKER and mark dedup COMPLETE."
