============================================================
Longevity Unnatural -- Retroactive Positional Conflict Dedup
Method: Full MongoDB export (excludes batch longevity_unnatural_v1)
Run: 20260603_041549
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
[contradiction guard] Skipped 44 rules from A and 3046 rules from B with no meaningful condition fields.
[positional] Keyed 0 planet×position groups from A, 308 from B -- 0 shared keys.
Loaded 44 valid rules from folder-a: /Users/apple/Documents/Knowledge Engine_eBooks/LongevityUnnatural_CC_Decode
Loaded 10620 valid rules from folder-b: /private/tmp/mongo_existing_rules_dedup
Rules in A: 44
Rules in B: 10620
Pairs evaluated: 467280
Similarity matches: 0
Contradiction pairs: 0
Positional conflicts: 0
Dry run complete. No source JSON files were changed.
Report written to /Users/apple/DailyHoroscope-Migration/KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_longevity_unnatural_vs_mongodb_positional.json

--- STEP 3/3: Triage Summary ---
Rules in Unnatural batch (A): 44
Rules in MongoDB export (B):  10620
Pairs evaluated:              467,280

TF-IDF similarity matches:    0
Contradiction pairs:          0
Positional conflicts:         0

TRIAGE BREAKDOWN:
  self-match artifacts         : 0  (should be 0 with fixed export script)
  positional_polarity_conflict : 0  (PATCH -- genuine cross-system conflict)
  positional_alternate_result  : 0  (REVIEW -- contextual, no patch)

============================================================
✅  CLEAN -- Zero genuine matches, contradictions, or polarity conflicts.
    Longevity Unnatural is clear against the full MongoDB.
============================================================

JSON report : KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_longevity_unnatural_vs_mongodb_positional.json
Log saved   : KE_TEXTBOOK_DECODE/Dedup_Reports/longevity_unnatural_dedup_20260603_041549.md
