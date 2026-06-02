#!/bin/bash
# =============================================================================
# Retroactive Positional Conflict Dedup -- Longevity Unnatural (longevity_unnatural_v1)
# =============================================================================
# Run from repo root:
#   export MONGO_URL="mongodb+srv://..."
#   bash backend/scripts/retroactive_dedup_longevity_unnatural.sh
#
# Auto-save: all output is tee'd to a timestamped .md log in Dedup_Reports/.
# When the script finishes it prints: "Log saved: <path>" -- share that path.
#
# Pre-requisite:
#   The Longevity Unnatural source JSON must be at:
#   /tmp/longevity_unnatural_rules/Longevity_Unnatural_Rules.json
#   (44 rules, batch_id: longevity_unnatural_v1)
#
# What this does:
#   1. Clears /tmp/mongo_existing_rules_dedup/ (prevents stale-file false-positives)
#      then exports ALL MongoDB rules EXCEPT the Unnatural batch (~10,620 rules)
#   2. Runs ke_dedup_script.py -- ONE run covers the entire DB
#   3. Saves JSON report + human-readable .md log to KE_TEXTBOOK_DECODE/Dedup_Reports/
#   4. Prints triage summary: CLEAN / REVIEW
# =============================================================================

set -euo pipefail

if [ -z "${MONGO_URL:-}" ]; then
  echo "ERROR: MONGO_URL environment variable not set."
  echo "Usage: export MONGO_URL=\"mongodb+srv://...\""
  echo "       bash backend/scripts/retroactive_dedup_longevity_unnatural.sh"
  exit 1
fi

SCRIPT="backend/ke_dedup_script.py"
FOLDER_A="/tmp/longevity_unnatural_rules/"
MONGO_EXPORT_DIR="/tmp/mongo_existing_rules_dedup"
REPORTS="KE_TEXTBOOK_DECODE/Dedup_Reports"
REPORT_PATH="$REPORTS/dedup_longevity_unnatural_vs_mongodb_positional.json"
BATCH_ID="longevity_unnatural_v1"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_PATH="$REPORTS/longevity_unnatural_dedup_${TIMESTAMP}.md"

mkdir -p "$REPORTS"

# Check source folder exists
if [ ! -d "$FOLDER_A" ]; then
  echo "ERROR: Source folder not found: $FOLDER_A"
  echo "Place Longevity_Unnatural_Rules.json there before running."
  exit 1
fi

# ── Auto-save: tee all output to LOG_PATH ──────────────────────────────────
exec > >(tee -a "$LOG_PATH") 2>&1

echo "============================================================"
echo "Longevity Unnatural -- Retroactive Positional Conflict Dedup"
echo "Method: Full MongoDB export (excludes batch $BATCH_ID)"
echo "Run: $TIMESTAMP"
echo "============================================================"
echo ""

# ------------------------------------------------------------------
# Step 1 -- Export MongoDB (all rules except the Unnatural batch)
# ------------------------------------------------------------------
echo "--- STEP 1/3: Export MongoDB → $MONGO_EXPORT_DIR ---"
python3 backend/scripts/export_mongo_for_dedup.py \
  --exclude-batch "$BATCH_ID" \
  --output-dir "$MONGO_EXPORT_DIR" \
  --mongo-url "$MONGO_URL" \
  --db-name horoscope_db
echo ""

# ------------------------------------------------------------------
# Step 2 -- Run dedup: Unnatural vs full MongoDB export
# ------------------------------------------------------------------
echo "--- STEP 2/3: Run dedup (Longevity Unnatural vs full MongoDB) ---"
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
python3 - <<PYEOF
import json, sys

path = "$REPORT_PATH"
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

print(f"Rules in Unnatural batch (A): {rules_a}")
print(f"Rules in MongoDB export (B):  {rules_b}")
print(f"Pairs evaluated:              {pairs:,}")
print()
print(f"TF-IDF similarity matches:    {matches}")
print(f"Contradiction pairs:          {contras}")
print(f"Positional conflicts:         {positional}")
print()

# Triage breakdown
self_matches  = [d for d in details if d["rule_a_id"] == d["rule_b_id"]]
polarity_conf = [d for d in details if d["rule_a_id"] != d["rule_b_id"] and d.get("relationship") == "positional_polarity_conflict"]
alt_results   = [d for d in details if d["rule_a_id"] != d["rule_b_id"] and d.get("relationship") == "positional_alternate_result"]

print(f"TRIAGE BREAKDOWN:")
print(f"  self-match artifacts         : {len(self_matches)}  (should be 0 with fixed export script)")
print(f"  positional_polarity_conflict : {len(polarity_conf)}  (PATCH -- genuine cross-system conflict)")
print(f"  positional_alternate_result  : {len(alt_results)}  (REVIEW -- contextual, no patch)")
print()

if self_matches:
    print("WARNING: Self-matches detected -- export dir may still contain stale files.")
    for d in self_matches:
        print(f"  ARTIFACT: {d['rule_a_id']} <-> {d['rule_b_id']}")
    print()

if matches > 0:
    print("SIMILARITY MATCHES (possible duplicates):")
    for m in data.get("matches", []):
        print(f"  [{m['relationship']}] {m['rule_a_id']} <-> {m['rule_b_id']}  score={m['similarity_score']:.4f}")
        print(f"    A: {m.get('rule_a_full_text','')[:120]}")
        print(f"    B: {m.get('rule_b_full_text','')[:120]}")
    print()

if contras > 0:
    print("CONTRADICTION PAIRS:")
    for c in data.get("contradictions", []):
        print(f"  [{c['relationship']}] {c['rule_a_id']} <-> {c['rule_b_id']}  score={c['similarity_score']:.4f}")
        print(f"    A polarity: {c.get('rule_a_polarity','?')}  B polarity: {c.get('rule_b_polarity','?')}")
        print(f"    A: {c.get('rule_a_full_text','')[:120]}")
        print(f"    B: {c.get('rule_b_full_text','')[:120]}")
    print()

if polarity_conf:
    print("GENUINE POLARITY CONFLICTS (action required):")
    for d in polarity_conf:
        print(f"  {d['rule_a_id']} vs {d['rule_b_id']}")
        print(f"    key    : {d['positional_key']}")
        print(f"    A pol  : {d.get('rule_a_polarity','?')}  B pol: {d.get('rule_b_polarity','?')}")
        print(f"    A text : {d.get('rule_a_full_text','')[:140]}")
        print(f"    B text : {d.get('rule_b_full_text','')[:140]}")
    print()

if alt_results:
    print("CONTEXTUAL ALTERNATE RESULTS (review-only, no patch needed):")
    by_key = {}
    for d in alt_results:
        by_key.setdefault(d["positional_key"], []).append(d)
    for key, entries in sorted(by_key.items()):
        print(f"  [{key}]  ({len(entries)} pair(s))")
        for d in entries[:5]:  # cap display to 5 per key
            print(f"    {d['rule_a_id']} vs {d['rule_b_id']}  score={d['similarity_score']:.4f}")
        if len(entries) > 5:
            print(f"    ... and {len(entries)-5} more")
    print()

print("=" * 60)
genuine = len(polarity_conf) + matches + contras
if genuine == 0 and not self_matches:
    print("✅  CLEAN -- Zero genuine matches, contradictions, or polarity conflicts.")
    print("    Longevity Unnatural is clear against the full MongoDB.")
else:
    if genuine > 0:
        print(f"⚠️   REVIEW REQUIRED")
        if polarity_conf:
            print(f"    Run patch script:")
            print(f"    python3 backend/scripts/patch_longevity_unnatural_conflicts.py \\")
            print(f"      --mongo-url \"\$MONGO_URL\" --dry-run")
    if self_matches:
        print(f"⚠️   {len(self_matches)} self-match artifact(s) detected.")
        print("    Re-run after verifying export_mongo_for_dedup.py clears the output dir.")
print("=" * 60)
PYEOF

echo ""
echo "JSON report : $REPORT_PATH"
echo "Log saved   : $LOG_PATH"
