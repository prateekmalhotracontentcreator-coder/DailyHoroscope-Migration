#!/bin/bash
# =============================================================================
# Retroactive Positional Conflict Dedup -- Lal Kitab Ch19-29
#                                          (batch: lalkitab_all_v2_20260605)
# =============================================================================
# Run from repo root:
#   export MONGO_URL="mongodb+srv://..."
#   bash backend/scripts/retroactive_dedup_lalkitab.sh
#
# What this does:
#   Pass 1 -- LK vs BPHS Vol 1 (BPHS_CC_Decode):
#     1. Exports LK-only rules from MongoDB → /tmp/lalkitab_rules_for_dedup/
#     2. Runs ke_dedup_script.py (LK vs BPHS Vol 1 decode folder)
#     3. Saves JSON + .md log to KE_TEXTBOOK_DECODE/Dedup_Reports/
#     4. Prints triage summary
#
#   Pass 2 -- LK vs BPHS Vol 2 (BPHS_Vol2_CC_Decode):
#     1. Reuses LK export from Pass 1
#     2. Runs ke_dedup_script.py (LK vs BPHS Vol 2 decode folder)
#     3. Saves JSON + .md log to KE_TEXTBOOK_DECODE/Dedup_Reports/
#     4. Prints triage summary
#
# Why separate from standard retroactive dedup?
#   LK source files are docx/rtf (not *_Rules*.json), so folder-a is an
#   inline MongoDB export of just the LK batch -- same rules that were
#   validated and triaged in the session of 2026-06-05.
#
# If genuine conflicts found, create a patch script:
#   backend/scripts/patch_lalkitab_conflicts.py
# =============================================================================

set -euo pipefail

if [ -z "${MONGO_URL:-}" ]; then
  echo "ERROR: MONGO_URL environment variable not set."
  echo "Usage: export MONGO_URL=\"mongodb+srv://...\""
  echo "       bash backend/scripts/retroactive_dedup_lalkitab.sh"
  exit 1
fi

SCRIPT="backend/ke_dedup_script.py"
LK_EXPORT_DIR="/tmp/lalkitab_rules_for_dedup"
BPHS_VOL1_FOLDER="/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode"
BPHS_VOL2_FOLDER="/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode"
REPORTS="KE_TEXTBOOK_DECODE/Dedup_Reports"
LK_BATCH="lalkitab_all_v2_20260605"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_PATH="$REPORTS/dedup_lalkitab_vs_bphs_${TIMESTAMP}.md"

mkdir -p "$REPORTS"

# ── Print log path FIRST ────────────────────────────────────────────────────
echo ""
echo "============================================================"
echo "  LOG FILE: $LOG_PATH"
echo "============================================================"
echo ""

# Check BPHS source folders exist
if [ ! -d "$BPHS_VOL1_FOLDER" ]; then
  echo "ERROR: BPHS Vol 1 folder not found: $BPHS_VOL1_FOLDER"
  exit 1
fi
if [ ! -d "$BPHS_VOL2_FOLDER" ]; then
  echo "ERROR: BPHS Vol 2 folder not found: $BPHS_VOL2_FOLDER"
  exit 1
fi

# ── Auto-save: tee all output to LOG_PATH ──────────────────────────────────
exec > >(tee -a "$LOG_PATH") 2>&1

echo "============================================================"
echo "Lal Kitab Ch19-29 -- Retroactive Positional Conflict Dedup"
echo "Batch:  $LK_BATCH"
echo "Run:    $TIMESTAMP"
echo "============================================================"
echo ""

# ------------------------------------------------------------------
# Step 0 -- Export LK rules from MongoDB (skip if already done)
# ------------------------------------------------------------------
LK_EXPORT_FILE="$LK_EXPORT_DIR/LalKitab_Ch19_29_Rules.json"
if [ -f "$LK_EXPORT_FILE" ]; then
  RULE_COUNT=$(python3 -c "import json; d=json.load(open('$LK_EXPORT_FILE')); print(len(d))" 2>/dev/null || echo "?")
  echo "--- STEP 0: Skipping export -- $LK_EXPORT_FILE already exists ($RULE_COUNT rules) ---"
else
  echo "--- STEP 0: Export LK rules from MongoDB → $LK_EXPORT_DIR ---"
  python3 backend/scripts/export_lalkitab_for_dedup.py --mongo-url "$MONGO_URL" --db-name horoscope_db
  if [ ! -f "$LK_EXPORT_FILE" ]; then
    echo "ERROR: Export failed -- $LK_EXPORT_FILE not created. Run export standalone first:"
    echo "  python3 backend/scripts/export_lalkitab_for_dedup.py --mongo-url \"\$MONGO_URL\""
    exit 1
  fi
fi
echo ""

# ------------------------------------------------------------------
# PASS 1 -- LK vs BPHS Vol 1
# ------------------------------------------------------------------
REPORT_VOL1="$REPORTS/dedup_lalkitab_vs_bphs_vol1_${TIMESTAMP}.json"

echo "============================================================"
echo "PASS 1 -- Lal Kitab vs BPHS Vol 1"
echo "============================================================"

echo "--- Run dedup (LK vs BPHS Vol 1) ---"
python3 "$SCRIPT" \
  --folder-a "$LK_EXPORT_DIR" \
  --folder-b "$BPHS_VOL1_FOLDER" \
  --threshold 0.82 \
  --output-report "$REPORT_VOL1" \
  --dry-run
echo ""

echo "--- Pass 1 Triage Summary ---"
DEDUP_REPORT_PATH="$REPORT_VOL1" python3 - <<'PYEOF'
import json, os, sys
path = os.environ["DEDUP_REPORT_PATH"]
try:
    data = json.load(open(path))
except Exception as e:
    print(f"ERROR reading report: {e}"); sys.exit(1)

rules_a    = data.get("rules_in_a", 0)
rules_b    = data.get("rules_in_b", 0)
pairs      = data.get("pairs_evaluated", 0)
matches    = data.get("duplicate_candidates", 0)
contras    = data.get("contradiction_pairs", 0)
positional = data.get("positional_conflicts", 0)
details    = data.get("positional_conflicts_detail", [])

print(f"Rules in LK (A):                     {rules_a}")
print(f"Rules in BPHS Vol 1 (B):             {rules_b}")
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
print(f"  positional_polarity_conflict : {len(polarity_conf)}  (PATCH -- genuine cross-system conflict)")
print(f"  positional_alternate_result  : {len(alt_results)}  (REVIEW -- contextual, no patch)")
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
            print(f"    {d['rule_a_id']} vs {d['rule_b_id']}  score={d.get('similarity_score',0):.4f}")
        if len(entries) > 3:
            print(f"    ... and {len(entries)-3} more")
    print()

print("=" * 60)
genuine = len(polarity_conf) + matches + contras
if genuine == 0 and not self_matches:
    print("PASS 1 ✅  CLEAN -- LK is clear against BPHS Vol 1.")
else:
    if polarity_conf: print(f"PASS 1 ⚠️   {len(polarity_conf)} GENUINE POLARITY CONFLICT(S) -- patch required.")
    if matches > 0:   print(f"PASS 1 ⚠️   {matches} SIMILARITY MATCH(ES) -- review.")
    if contras > 0:   print(f"PASS 1 ⚠️   {contras} CONTRADICTION PAIR(S) -- review.")
print("=" * 60)
PYEOF

echo ""

# ------------------------------------------------------------------
# PASS 2 -- LK vs BPHS Vol 2
# ------------------------------------------------------------------
REPORT_VOL2="$REPORTS/dedup_lalkitab_vs_bphs_vol2_${TIMESTAMP}.json"

echo "============================================================"
echo "PASS 2 -- Lal Kitab vs BPHS Vol 2"
echo "============================================================"

echo "--- Run dedup (LK vs BPHS Vol 2) ---"
python3 "$SCRIPT" \
  --folder-a "$LK_EXPORT_DIR" \
  --folder-b "$BPHS_VOL2_FOLDER" \
  --threshold 0.82 \
  --output-report "$REPORT_VOL2" \
  --dry-run
echo ""

echo "--- Pass 2 Triage Summary ---"
DEDUP_REPORT_PATH="$REPORT_VOL2" python3 - <<'PYEOF'
import json, os, sys
path = os.environ["DEDUP_REPORT_PATH"]
try:
    data = json.load(open(path))
except Exception as e:
    print(f"ERROR reading report: {e}"); sys.exit(1)

rules_a    = data.get("rules_in_a", 0)
rules_b    = data.get("rules_in_b", 0)
pairs      = data.get("pairs_evaluated", 0)
matches    = data.get("duplicate_candidates", 0)
contras    = data.get("contradiction_pairs", 0)
positional = data.get("positional_conflicts", 0)
details    = data.get("positional_conflicts_detail", [])

print(f"Rules in LK (A):                     {rules_a}")
print(f"Rules in BPHS Vol 2 (B):             {rules_b}")
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
print(f"  positional_polarity_conflict : {len(polarity_conf)}  (PATCH -- genuine cross-system conflict)")
print(f"  positional_alternate_result  : {len(alt_results)}  (REVIEW -- contextual, no patch)")
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
            print(f"    {d['rule_a_id']} vs {d['rule_b_id']}  score={d.get('similarity_score',0):.4f}")
        if len(entries) > 3:
            print(f"    ... and {len(entries)-3} more")
    print()

print("=" * 60)
genuine = len(polarity_conf) + matches + contras
if genuine == 0 and not self_matches:
    print("PASS 2 ✅  CLEAN -- LK is clear against BPHS Vol 2.")
else:
    if polarity_conf: print(f"PASS 2 ⚠️   {len(polarity_conf)} GENUINE POLARITY CONFLICT(S) -- patch required.")
    if matches > 0:   print(f"PASS 2 ⚠️   {matches} SIMILARITY MATCH(ES) -- review.")
    if contras > 0:   print(f"PASS 2 ⚠️   {contras} CONTRADICTION PAIR(S) -- review.")
print("=" * 60)
PYEOF

echo ""
echo "JSON report (Vol 1) : $REPORT_VOL1"
echo "JSON report (Vol 2) : $REPORT_VOL2"
echo "Log saved           : $LOG_PATH"
