============================================================
Longevity Unnatural -- Retroactive Positional Conflict Dedup
Method: Full MongoDB export (excludes batch longevity_unnatural_v1)
Run: 20260603_040642
============================================================

--- STEP 1/3: Export MongoDB → /tmp/mongo_existing_rules_dedup ---
Cleared stale export directory: /tmp/mongo_existing_rules_dedup
Excluding batch: longevity_unnatural_v1
Fetched 10620 rules from MongoDB
  300_Combinations: 329 rules → 300_Combinations_Rules.json
  300_Horoscopes_Vol_1: 57 rules → 300_Horoscopes_Vol_1_Rules.json
  BPHS_Vol_1: 696 rules → BPHS_Vol_1_Rules.json
  BPHS_Vol_2: 249 rules → BPHS_Vol_2_Rules.json
  Longevity_(58_Chapters): 149 rules → Longevity_(58_Chapters)_Rules.json
  Phaladeepika: 1218 rules → Phaladeepika_Rules.json
  unknown: 7922 rules → unknown_Rules.json

Total exported: 10620 rules across 7 source_book groups
Output directory: /tmp/mongo_existing_rules_dedup

--- STEP 2/3: Run dedup (Longevity Unnatural vs full MongoDB) ---
[warn] No *_Rules*.json files found in /private/tmp/longevity_unnatural_rules
[contradiction guard] Skipped 0 rules from A and 3046 rules from B with no meaningful condition fields.
[positional] Keyed 0 planet×position groups from A, 308 from B -- 0 shared keys.
Loaded 10620 valid rules from folder-b: /private/tmp/mongo_existing_rules_dedup
Rules in A: 0
Rules in B: 10620
Pairs evaluated: 0
Similarity matches: 0
Contradiction pairs: 0
Positional conflicts: 0
Dry run complete. No source JSON files were changed.
Report written to /Users/apple/DailyHoroscope-Migration/KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_longevity_unnatural_vs_mongodb_positional.json

--- STEP 3/3: Triage Summary ---
  File "<stdin>", line 94
    print(f"    python3 backend/scripts/patch_longevity_unnatural_conflicts.py \")
                                                                                  ^
SyntaxError: EOL while scanning string literal
