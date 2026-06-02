#!/bin/bash
# =============================================================================
# Retroactive Positional Conflict Dedup -- Longevity 58Ch (longevity_58ch_v1)
# =============================================================================
# Run from repo root:
#   export MONGO_URL="mongodb+srv://..."
#   bash backend/scripts/retroactive_dedup_longevity58ch.sh
#
# What this does:
#   1. Exports all MongoDB rules EXCEPT the 58Ch batch itself
#      (10,515 rules = 10,664 total minus 149 in longevity_58ch_v1)
#   2. Runs ke_dedup_script.py (with positional conflict detector, added 2026-06-02)
#      against that full export -- ONE run covers the entire DB
#   3. Saves report to KE_TEXTBOOK_DECODE/Dedup_Reports/
#   4. Prints a summary with CLEAN / REVIEW flags
#
# Why --exclude-batch longevity_58ch_v1:
#   The batch is already in MongoDB. Comparing it against itself produces
#   100% similarity on every rule (trivial false positives). Excluding it
#   gives a clean cross-text view: 58Ch rules vs every OTHER rule in DB.
#
# Source: /tmp/longevity_58ch_rules/Longevity_58Ch_Rules.json (149 rules)
# Positional rules in this batch (6 of 149):
#   kp-ch12-001  Jupiter in H7  (negative)
#   kp-ch12-002  Jupiter in H1  (negative)
#   kp-ch12-005  Mercury in [H5,H8,H9]  (positive)
#   kp-ch13-001  Sun in H11  (negative)
#   kp-ch13-002  Venus in [H1,H8]  (conditional)
#   kp-ch13-003  Venus in [H1,H3..H10]  (positive)
# =============================================================================

set -euo pipefail

if [ -z "${MONGO_URL:-}" ]; then
  echo "ERROR: MONGO_URL environment variable not set."
  echo "Usage: export MONGO_URL=\"mongodb+srv://...\""
  echo "       bash backend/scripts/retroactive_dedup_longevity58ch.sh"
  exit 1
fi

SCRIPT="backend/ke_dedup_script.py"
FOLDER_A="/tmp/longevity_58ch_rules/"
MONGO_EXPORT_DIR="/tmp/mongo_existing_rules_dedup"
REPORTS="KE_TEXTBOOK_DECODE/Dedup_Reports"
REPORT_PATH="$REPORTS/dedup_58ch_vs_mongodb_v2_positional.json"
BATCH_ID="longevity_58ch_v1"

mkdir -p "$REPORTS"

echo "============================================================"
echo "Longevity 58Ch -- Retroactive Positional Conflict Dedup"
echo "Method: Full MongoDB export (excludes batch $BATCH_ID)"
echo "============================================================"
echo ""

# ------------------------------------------------------------------
# Step 1 -- Export MongoDB (all rules except the 58Ch batch)
# ------------------------------------------------------------------
echo "--- STEP 1/3: Export MongoDB → $MONGO_EXPORT_DIR ---"
python3 backend/scripts/export_mongo_for_dedup.py \
  --exclude-batch "$BATCH_ID" \
  --output-dir "$MONGO_EXPORT_DIR" \
  --mongo-url "$MONGO_URL" \
  --db-name horoscope_db
echo ""

# ------------------------------------------------------------------
# Step 2 -- Run dedup: 58Ch vs full MongoDB export
# ------------------------------------------------------------------
echo "--- STEP 2/3: Run dedup (58Ch vs full MongoDB) ---"
python3 "$SCRIPT" \
  --folder-a "$FOLDER_A" \
  --folder-b "$MONGO_EXPORT_DIR" \
  --threshold 0.82 \
  --output-report "$REPORT_PATH" \
  --dry-run
echo ""

# ------------------------------------------------------------------
# Step 3 -- Parse report and print summary
# ------------------------------------------------------------------
echo "--- STEP 3/3: Summary ---"
python3 - <<PYEOF
import json, sys

path = "$REPORT_PATH"
try:
    data = json.load(open(path))
except Exception as e:
    print(f"ERROR reading report: {e}")
    sys.exit(1)

rules_a       = data.get("rules_in_a", 0)
rules_b       = data.get("rules_in_b", 0)
pairs         = data.get("pairs_evaluated", 0)
matches       = data.get("duplicate_candidates", 0)
contras       = data.get("contradiction_pairs", 0)
positional    = data.get("positional_conflicts", 0)
details       = data.get("positional_conflicts_detail", [])

print(f"Rules in 58Ch batch (A):   {rules_a}")
print(f"Rules in MongoDB export (B): {rules_b}")
print(f"Pairs evaluated:             {pairs:,}")
print()
print(f"TF-IDF similarity matches:   {matches}")
print(f"Contradiction pairs:         {contras}")
print(f"Positional conflicts:        {positional}")
print()

if matches > 0:
    print("SIMILARITY MATCHES:")
    for m in data.get("matches", []):
        print(f"  [{m['relationship']}] {m['rule_a_id']} <-> {m['rule_b_id']}  score={m['similarity_score']:.4f}")
    print()

if contras > 0:
    print("CONTRADICTION PAIRS:")
    for c in data.get("contradictions", []):
        print(f"  [{c['relationship']}] {c['rule_a_id']} <-> {c['rule_b_id']}  score={c['similarity_score']:.4f}")
        print(f"    A polarity: {c.get('rule_a_polarity')}  B polarity: {c.get('rule_b_polarity')}")
    print()

if positional > 0:
    polarity_conflicts = [d for d in details if d.get("relationship") == "positional_polarity_conflict"]
    alt_results        = [d for d in details if d.get("relationship") == "positional_alternate_result"]
    print(f"POSITIONAL CONFLICTS ({positional} total):")
    print(f"  positional_polarity_conflict: {len(polarity_conflicts)}")
    print(f"  positional_alternate_result:  {len(alt_results)}")
    print()
    for d in details:
        print(f"  [{d['relationship']}]")
        print(f"    Key:    {d.get('positional_key', '?')}")
        print(f"    A:      {d['rule_a_id']}  polarity={d.get('rule_a_polarity','?')}")
        print(f"    B:      {d['rule_b_id']}  polarity={d.get('rule_b_polarity','?')}")
        print(f"    Score:  {d['similarity_score']:.4f}")
        print(f"    A text: {d.get('rule_a_full_text','')[:120]}")
        print(f"    B text: {d.get('rule_b_full_text','')[:120]}")
        print()

print("=" * 60)
if matches == 0 and contras == 0 and positional == 0:
    print("✅  CLEAN -- Zero matches, contradictions, or positional conflicts.")
    print("    Longevity 58Ch is clear against the full MongoDB.")
    print("    No patch required.")
else:
    print(f"⚠️   REVIEW REQUIRED")
    if positional > 0:
        print(f"    Run patch script to flag {positional} rule(s) in MongoDB:")
        print(f"    python3 backend/scripts/patch_58ch_positional_conflicts.py \\\\")
        print(f"      --mongo-url \"\$MONGO_URL\" --dry-run")
print("=" * 60)
PYEOF

echo ""
echo "Report saved: $REPORT_PATH"
