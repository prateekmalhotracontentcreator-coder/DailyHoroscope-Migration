#!/bin/bash
# =============================================================================
# Retroactive Positional Conflict Dedup -- Longevity 58Ch (longevity_58ch_v1)
# =============================================================================
# Run from repo root:
#   export MONGO_URL="mongodb+srv://..."
#   bash backend/scripts/retroactive_dedup_longevity58ch.sh
#
# Auto-save: all output is tee'd to a timestamped .md log in Dedup_Reports/.
# When the script finishes it prints: "Log saved: <path>" -- share that path.
#
# What this does:
#   1. Clears /tmp/mongo_existing_rules_dedup/ (prevents stale-file false-positives)
#      then exports all MongoDB rules EXCEPT the 58Ch batch (10,515 rules)
#   2. Runs ke_dedup_script.py against that export -- ONE run covers the entire DB
#   3. Saves JSON report + human-readable .md log to KE_TEXTBOOK_DECODE/Dedup_Reports/
#   4. Prints a triage summary: CLEAN / REVIEW
#
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
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_PATH="$REPORTS/longevity_58ch_dedup_${TIMESTAMP}.md"

mkdir -p "$REPORTS"

# ── Print log path BEFORE redirect so it always appears on screen ──────────
echo ""
echo "============================================================"
echo "  LOG FILE: $LOG_PATH"
echo "============================================================"
echo ""

# ── Auto-save: tee all output to LOG_PATH ──────────────────────────────────
exec > >(tee -a "$LOG_PATH") 2>&1

echo "============================================================"
echo "Longevity 58Ch -- Retroactive Positional Conflict Dedup"
echo "Method: Full MongoDB export (excludes batch $BATCH_ID)"
echo "Run: $TIMESTAMP"
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
# Step 3 -- Parse report and print triage summary
# ------------------------------------------------------------------
echo "--- STEP 3/3: Triage Summary ---"
# Use quoted <<'PYEOF' to prevent bash from mangling backslashes and quotes
# inside the Python code. Pass the report path via env var instead.
DEDUP_REPORT_PATH="$REPORT_PATH" python3 - <<'PYEOF'
import json, os, sys

path = os.environ["DEDUP_REPORT_PATH"]
try:
    data = json.load(open(path))
except Exception as e:
    print(f"ERROR reading report: {e}")
    sys.exit(1)

rules_a    = data.get("rules_in_a", 0)
rules_b    = data.get("rules_in_b", 0)
pairs      = data.get("pairs_evaluated", 0)
matches    = data.get("duplicate_candidates", 0)
contras    = data.get("contradiction_pairs", 0)
positional = data.get("positional_conflicts", 0)
details    = data.get("positional_conflicts_detail", [])

print(f"Rules in 58Ch batch (A):     {rules_a}")
print(f"Rules in MongoDB export (B): {rules_b}")
print(f"Pairs evaluated:             {pairs:,}")
print()
print(f"TF-IDF similarity matches:   {matches}")
print(f"Contradiction pairs:         {contras}")
print(f"Positional conflicts:        {positional}")
print()

self_matches  = [d for d in details if d["rule_a_id"] == d["rule_b_id"]]
polarity_conf = [d for d in details if d["rule_a_id"] != d["rule_b_id"] and d.get("relationship") == "positional_polarity_conflict"]
alt_results   = [d for d in details if d["rule_a_id"] != d["rule_b_id"] and d.get("relationship") == "positional_alternate_result"]

print("TRIAGE BREAKDOWN:")
print(f"  self-match artifacts         : {len(self_matches)}  (SKIP -- stale export dir, fixed)")
print(f"  positional_polarity_conflict : {len(polarity_conf)}  (PATCH -- genuine cross-system conflict)")
print(f"  positional_alternate_result  : {len(alt_results)}  (REVIEW -- contextual, no patch)")
print()

if polarity_conf:
    print("GENUINE POLARITY CONFLICTS:")
    for d in polarity_conf:
        print(f"  {d['rule_a_id']} vs {d['rule_b_id']}")
        print(f"    key={d['positional_key']}  A={d.get('rule_a_polarity','?')}  B={d.get('rule_b_polarity','?')}")
        print(f"    B: {d.get('rule_b_full_text','')[:140]}")
    print()

print("=" * 60)
genuine = len(polarity_conf)
if matches == 0 and contras == 0 and genuine == 0:
    print("✅  CLEAN -- Zero genuine matches, contradictions, or polarity conflicts.")
    print("    Longevity 58Ch is clear against the full MongoDB.")
else:
    print(f"⚠️   REVIEW REQUIRED -- {genuine} genuine polarity conflict(s)")
    if genuine > 0:
        print("    Run patch script (dry-run first):")
        print("    python3 backend/scripts/patch_58ch_positional_conflicts.py \\")
        print('      --mongo-url "$MONGO_URL" --dry-run')
print("=" * 60)
PYEOF

echo ""
echo "JSON report : $REPORT_PATH"
echo "Log saved   : $LOG_PATH"
