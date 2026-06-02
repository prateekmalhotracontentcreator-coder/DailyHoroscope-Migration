#!/bin/bash
# =============================================================================
# Retroactive Positional Conflict Dedup -- BPHS Vol 2
#                                          (bphs-vol2-ch49-51-v1)
# =============================================================================
# Run from repo root:
#   export MONGO_URL="mongodb+srv://..."
#   bash backend/scripts/retroactive_dedup_bphs_vol2.sh
#
# Source folder:
#   /Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/
#   Ch49 Kalachakra Dasa (154), Ch50 Chara Dasa (73), Ch51 Antardasas (22)
#   = 249 rules total (batch: bphs-vol2-ch49-51-v1)
#
# Why retroactive?
#   The positional conflict detector was added 2026-06-02, after this batch
#   was ingested 2026-06-01. BPHS Vol 2 covers Dasa chapters -- Kalachakra
#   and Chara Dasa planet state rules. Some planet×sign conditions present
#   (planet states in signs for Chara Dasa). Overlap likely with Vol 1.
#
# What this does:
#   1. Clears /tmp/mongo_existing_rules_dedup/ then exports ALL MongoDB rules
#      EXCEPT bphs-vol2-ch49-51-v1 (~10,415 rules)
#   2. Runs ke_dedup_script.py
#   3. Saves JSON report + .md log to KE_TEXTBOOK_DECODE/Dedup_Reports/
#   4. Prints triage summary
#
# If positional conflicts found, run patch script:
#   python3 backend/scripts/patch_bphs_vol2_conflicts.py \
#     --mongo-url "$MONGO_URL" --dry-run
# =============================================================================

set -euo pipefail

if [ -z "${MONGO_URL:-}" ]; then
  echo "ERROR: MONGO_URL environment variable not set."
  echo "Usage: export MONGO_URL=\"mongodb+srv://...\""
  echo "       bash backend/scripts/retroactive_dedup_bphs_vol2.sh"
  exit 1
fi

SCRIPT="backend/ke_dedup_script.py"
FOLDER_A="/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode"
MONGO_EXPORT_DIR="/tmp/mongo_existing_rules_dedup"
REPORTS="KE_TEXTBOOK_DECODE/Dedup_Reports"
REPORT_PATH="$REPORTS/dedup_bphs_vol2_vs_mongodb_positional.json"
BATCH_ID="bphs-vol2-ch49-51-v1"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_PATH="$REPORTS/bphs_vol2_dedup_${TIMESTAMP}.md"

mkdir -p "$REPORTS"

# ── Print log path FIRST ────────────────────────────────────────────────────
echo ""
echo "============================================================"
echo "  LOG FILE: $LOG_PATH"
echo "============================================================"
echo ""

# Check source folder exists
if [ ! -d "$FOLDER_A" ]; then
  echo "ERROR: Decode folder not found: $FOLDER_A"
  echo "Verify the path and update FOLDER_A in this script if it has moved."
  exit 1
fi

# ── Auto-save: tee all output to LOG_PATH ──────────────────────────────────
exec > >(tee -a "$LOG_PATH") 2>&1

echo "============================================================"
echo "BPHS Vol 2 -- Retroactive Positional Conflict Dedup"
echo "Method: Full MongoDB export (excludes batch $BATCH_ID)"
echo "Run: $TIMESTAMP"
echo "============================================================"
echo ""

# ------------------------------------------------------------------
# Step 1 -- Export MongoDB (all rules except BPHS Vol 2)
# ------------------------------------------------------------------
echo "--- STEP 1/3: Export MongoDB → $MONGO_EXPORT_DIR ---"
python3 backend/scripts/export_mongo_for_dedup.py \
  --exclude-batch "$BATCH_ID" \
  --output-dir "$MONGO_EXPORT_DIR" \
  --mongo-url "$MONGO_URL" \
  --db-name horoscope_db
echo ""

# ------------------------------------------------------------------
# Step 2 -- Run dedup: BPHS Vol 2 vs full MongoDB export
# ------------------------------------------------------------------
echo "--- STEP 2/3: Run dedup (BPHS Vol 2 vs full MongoDB) ---"
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

print(f"Rules in BPHS Vol 2 (A):            {rules_a}")
print(f"Rules in MongoDB export (B):         {rules_b}")
print(f"Pairs evaluated:                     {pairs:,}")
print()
print(f"TF-IDF similarity matches:           {matches}")
print(f"Contradiction pairs:                 {contras}")
print(f"Positional conflicts:                {positional}")
print()

self_matches  = [d for d in details if d["rule_a_id"] == d["rule_b_id"]]
polarity_conf = [d for d in details if d["rule_a_id"] != d["rule_b_id"] and d.get("relationship") == "positional_polarity_conflict"]
alt_results   = [d for d in details if d["rule_a_id"] != d["rule_b_id"] and d.get("relationship") == "positional_alternate_result"]

print("TRIAGE BREAKDOWN:")
print(f"  self-match artifacts         : {len(self_matches)}  (should be 0 with fixed export script)")
print(f"  positional_polarity_conflict : {len(polarity_conf)}  (PATCH -- genuine cross-system conflict)")
print(f"  positional_alternate_result  : {len(alt_results)}  (REVIEW -- contextual, no patch)")
print()

if self_matches:
    print("WARNING: Self-matches detected -- stale export dir bug.")
    for d in self_matches:
        print(f"  ARTIFACT: {d['rule_a_id']} <-> {d['rule_b_id']}")
    print()

if matches > 0:
    print("SIMILARITY MATCHES:")
    for m in data.get("matches", []):
        print(f"  [{m['relationship']}] {m['rule_a_id']} <-> {m['rule_b_id']}  score={m['similarity_score']:.4f}")
        print(f"    A: {m.get('rule_a_full_text','')[:120]}")
        print(f"    B: {m.get('rule_b_full_text','')[:120]}")
    print()

if contras > 0:
    print("CONTRADICTION PAIRS:")
    for c in data.get("contradictions", []):
        print(f"  [{c['relationship']}] {c['rule_a_id']} <-> {c['rule_b_id']}  score={c['similarity_score']:.4f}")
        print(f"    A pol: {c.get('rule_a_polarity','?')}  B pol: {c.get('rule_b_polarity','?')}")
        print(f"    A: {c.get('rule_a_full_text','')[:120]}")
        print(f"    B: {c.get('rule_b_full_text','')[:120]}")
    print()

if polarity_conf:
    print("GENUINE POLARITY CONFLICTS (action required):")
    by_key = {}
    for d in polarity_conf:
        by_key.setdefault(d["positional_key"], []).append(d)
    for key, entries in sorted(by_key.items()):
        print(f"  [{key}]  ({len(entries)} pair(s))")
        for d in entries[:10]:
            print(f"    {d['rule_a_id']} vs {d['rule_b_id']}")
            print(f"      A pol: {d.get('rule_a_polarity','?')}  B pol: {d.get('rule_b_polarity','?')}")
            print(f"      A: {d.get('rule_a_full_text','')[:120]}")
            print(f"      B: {d.get('rule_b_full_text','')[:120]}")
        if len(entries) > 10:
            print(f"    ... and {len(entries)-10} more (see JSON report)")
    print()

if alt_results:
    print("CONTEXTUAL ALTERNATE RESULTS (review-only):")
    by_key = {}
    for d in alt_results:
        by_key.setdefault(d["positional_key"], []).append(d)
    for key, entries in sorted(by_key.items()):
        print(f"  [{key}]  ({len(entries)} pair(s))")
        for d in entries[:3]:
            print(f"    {d['rule_a_id']} vs {d['rule_b_id']}  score={d['similarity_score']:.4f}")
        if len(entries) > 3:
            print(f"    ... and {len(entries)-3} more")
    print()

print("=" * 60)
genuine = len(polarity_conf) + matches + contras
if genuine == 0 and not self_matches:
    print("✅  CLEAN -- Zero genuine matches, contradictions, or polarity conflicts.")
    print("    BPHS Vol 2 is clear against the full MongoDB.")
else:
    if polarity_conf:
        print(f"⚠️   {len(polarity_conf)} GENUINE POLARITY CONFLICT(S) -- patch required.")
        print("    python3 backend/scripts/patch_bphs_vol2_conflicts.py \\")
        print('      --mongo-url "$MONGO_URL" --dry-run')
    if matches > 0:
        print(f"⚠️   {matches} SIMILARITY MATCH(ES) -- review.")
    if contras > 0:
        print(f"⚠️   {contras} CONTRADICTION PAIR(S) -- review.")
    if self_matches:
        print(f"⚠️   {len(self_matches)} self-match artifact(s) detected.")
print("=" * 60)
PYEOF

echo ""
echo "JSON report : $REPORT_PATH"
echo "Log saved   : $LOG_PATH"
