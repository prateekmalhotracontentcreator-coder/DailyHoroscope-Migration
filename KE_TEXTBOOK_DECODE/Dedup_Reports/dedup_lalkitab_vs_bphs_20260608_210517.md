============================================================
Lal Kitab Ch19-29 -- Retroactive Positional Conflict Dedup
Batch:  lalkitab_all_v2_20260605
Run:    20260608_210517
============================================================

--- STEP 0: Export LK rules from MongoDB → /tmp/lalkitab_rules_for_dedup ---
LOG FILE: KE_TEXTBOOK_DECODE/Dedup_Reports/export_lalkitab_for_dedup_20260608_153518.log
============================================================
Lal Kitab MongoDB Export for Dedup
Batch:   lalkitab_all_v2_20260605
Output:  /tmp/lalkitab_rules_for_dedup
Run:     20260608_153518
============================================================

Attempt 1/3 ...
Saved 467 rules → /tmp/lalkitab_rules_for_dedup/LalKitab_Ch19_29_Rules.json

✅  Export complete: 467 LK rules → /tmp/lalkitab_rules_for_dedup/LalKitab_Ch19_29_Rules.json

Next step -- run the dedup:
  bash backend/scripts/retroactive_dedup_lalkitab.sh
Log saved: KE_TEXTBOOK_DECODE/Dedup_Reports/export_lalkitab_for_dedup_20260608_153518.log

============================================================
PASS 1 -- Lal Kitab vs BPHS Vol 1
============================================================
--- Run dedup (LK vs BPHS Vol 1) ---
[warn] Skipping /Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/BPHS_Ch16_Effects_5th_House_Rules.json: unrecognised JSON structure (expected list or dict with 'rules' key)
[warn] Skipping /Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/BPHS_Ch17_Effects_6th_House_Rules.json: unrecognised JSON structure (expected list or dict with 'rules' key)
[warn] Skipping /Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/BPHS_Ch18_Effects_7th_House_Rules.json: unrecognised JSON structure (expected list or dict with 'rules' key)
[warn] Skipping /Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/BPHS_Ch20_Effects_9th_House_Rules.json: unrecognised JSON structure (expected list or dict with 'rules' key)
[warn] Skipping /Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/BPHS_Ch24_Effects_Bhava_Lords_Rules.json: unrecognised JSON structure (expected list or dict with 'rules' key)
[contradiction guard] Skipped 128 rules from A and 885 rules from B with no meaningful condition fields.
[positional] Keyed 44 planet×position groups from A, 240 from B -- 21 shared keys.
Loaded 467 valid rules from folder-a: /private/tmp/lalkitab_rules_for_dedup
Loaded 1456 valid rules from folder-b: /Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode
Rules in A: 467
Rules in B: 1456
Pairs evaluated: 679952
Similarity matches: 0
Contradiction pairs: 0
Positional conflicts: 80
POSITIONAL lalkitab-ch27-wave-w42 <-> bphs1-ch32-042 [positional_alternate_result] score=0.0766
POSITIONAL lalkitab-ch27-wave-w02 <-> bphs1-ch13-007 [positional_alternate_result] score=0.0422
POSITIONAL lalkitab-ch27-wave-w02 <-> bphs1-ch18-032 [positional_alternate_result] score=0.0860
POSITIONAL lalkitab-ch27-wave-w02 <-> bphs1-ch32-033 [positional_alternate_result] score=0.0538
POSITIONAL lalkitab-ch27-wave-w45 <-> bphs1-ch13-007 [positional_alternate_result] score=0.0444
POSITIONAL lalkitab-ch27-wave-w45 <-> bphs1-ch18-032 [positional_alternate_result] score=0.0679
POSITIONAL lalkitab-ch27-wave-w45 <-> bphs1-ch32-033 [positional_alternate_result] score=0.0428
POSITIONAL lalkitab-ch27-wave-w07 <-> bphs1-ch16-019 [positional_alternate_result] score=0.0536
POSITIONAL lalkitab-ch27-wave-w07 <-> bphs1-ch32-023 [positional_alternate_result] score=0.0530
POSITIONAL lalkitab-ch27-wave-w07 <-> bphs1-ch32-036 [positional_alternate_result] score=0.0512
POSITIONAL lalkitab-ch27-wave-w20 <-> bphs1-ch16-019 [positional_alternate_result] score=0.0545
POSITIONAL lalkitab-ch27-wave-w20 <-> bphs1-ch32-023 [positional_alternate_result] score=0.0452
POSITIONAL lalkitab-ch27-wave-w20 <-> bphs1-ch32-036 [positional_alternate_result] score=0.0321
POSITIONAL lalkitab-ch27-wave-w28 <-> bphs1-ch16-019 [positional_alternate_result] score=0.0544
POSITIONAL lalkitab-ch27-wave-w28 <-> bphs1-ch32-023 [positional_alternate_result] score=0.0436
POSITIONAL lalkitab-ch27-wave-w28 <-> bphs1-ch32-036 [positional_alternate_result] score=0.0415
POSITIONAL lalkitab-ch27-proh-09 <-> bphs1-ch18-012 [positional_alternate_result] score=0.0922
POSITIONAL lalkitab-ch27-proh-09 <-> bphs1-ch18-016 [positional_alternate_result] score=0.0599
POSITIONAL lalkitab-ch27-wave-w25 <-> bphs1-ch32-040 [positional_alternate_result] score=0.0493
POSITIONAL lalkitab-ch27-wave-w25 <-> bphs1-ch39-040 [positional_alternate_result] score=0.0717
POSITIONAL lalkitab-ch27-wave-w32 <-> bphs1-ch32-040 [positional_alternate_result] score=0.0432
POSITIONAL lalkitab-ch27-wave-w32 <-> bphs1-ch39-040 [positional_alternate_result] score=0.0746
POSITIONAL lalkitab-ch25-mars-h2 <-> bphs1-ch42-015 [positional_alternate_result] score=0.0574
POSITIONAL lalkitab-ch27-wave-w04 <-> bphs1-ch14-017 [positional_alternate_result] score=0.0385
POSITIONAL lalkitab-ch27-wave-w04 <-> bphs1-ch32-021 [positional_alternate_result] score=0.0282
POSITIONAL lalkitab-ch27-wave-w04 <-> bphs1-ch32-034 [positional_alternate_result] score=0.0347
POSITIONAL lalkitab-ch27-wave-w22 <-> bphs1-ch14-017 [positional_alternate_result] score=0.0453
POSITIONAL lalkitab-ch27-wave-w22 <-> bphs1-ch32-021 [positional_alternate_result] score=0.0302
POSITIONAL lalkitab-ch27-wave-w22 <-> bphs1-ch32-034 [positional_alternate_result] score=0.0286
POSITIONAL lalkitab-ch27-wave-w34 <-> bphs1-ch14-017 [positional_alternate_result] score=0.0648
POSITIONAL lalkitab-ch27-wave-w34 <-> bphs1-ch32-021 [positional_alternate_result] score=0.0355
POSITIONAL lalkitab-ch27-wave-w34 <-> bphs1-ch32-034 [positional_alternate_result] score=0.0504
POSITIONAL lalkitab-ch27-wave-w46 <-> bphs1-ch14-017 [positional_alternate_result] score=0.0453
POSITIONAL lalkitab-ch27-wave-w46 <-> bphs1-ch32-021 [positional_alternate_result] score=0.0410
POSITIONAL lalkitab-ch27-wave-w46 <-> bphs1-ch32-034 [positional_alternate_result] score=0.0396
POSITIONAL lalkitab-ch25-mercury-h1 <-> bphs1-ch15-005 [positional_alternate_result] score=0.0645
POSITIONAL lalkitab-ch25-mercury-h1 <-> bphs1-ch17-011 [positional_alternate_result] score=0.0691
POSITIONAL lalkitab-ch27-wave-w23 <-> bphs1-ch32-022 [positional_alternate_result] score=0.0455
POSITIONAL lalkitab-ch27-wave-w49 <-> bphs1-ch32-022 [positional_alternate_result] score=0.0469
POSITIONAL lalkitab-ch25-mercury-h7 <-> bphs1-ch18-011 [positional_alternate_result] score=0.0612
POSITIONAL lalkitab-ch27-wave-w11 <-> bphs1-ch18-011 [positional_alternate_result] score=0.0478
POSITIONAL lalkitab-ch27-wave-w30 <-> bphs1-ch18-011 [positional_alternate_result] score=0.0515
POSITIONAL lalkitab-ch25-moon-h1 <-> bphs1-ch17-006 [positional_alternate_result] score=0.0588
POSITIONAL lalkitab-ch25-moon-h1 <-> bphs1-ch17-007 [positional_alternate_result] score=0.0468
POSITIONAL lalkitab-ch25-moon-h1 <-> bphs1-ch17-008 [positional_alternate_result] score=0.0464
POSITIONAL lalkitab-ch25-moon-h1 <-> bphs1-ch17-017 [positional_alternate_result] score=0.0619
POSITIONAL lalkitab-ch25-moon-h10 <-> bphs1-ch45-022 [positional_alternate_result] score=0.2220
POSITIONAL lalkitab-ch25-moon-h3 <-> bphs1-ch14-013 [positional_alternate_result] score=0.0743
POSITIONAL lalkitab-ch25-moon-h3 <-> bphs1-ch14-014 [positional_alternate_result] score=0.0725
POSITIONAL lalkitab-ch27-wave-w05 <-> bphs1-ch32-020 [positional_alternate_result] score=0.0344
POSITIONAL lalkitab-ch27-wave-w05 <-> bphs1-ch32-035 [positional_alternate_result] score=0.0340
POSITIONAL lalkitab-ch27-wave-w27 <-> bphs1-ch32-020 [positional_alternate_result] score=0.0340
POSITIONAL lalkitab-ch27-wave-w27 <-> bphs1-ch32-035 [positional_alternate_result] score=0.0284
POSITIONAL lalkitab-ch27-wave-w35 <-> bphs1-ch32-020 [positional_alternate_result] score=0.0325
POSITIONAL lalkitab-ch27-wave-w35 <-> bphs1-ch32-035 [positional_alternate_result] score=0.0359
POSITIONAL lalkitab-ch27-wave-w47 <-> bphs1-ch32-020 [positional_alternate_result] score=0.0303
POSITIONAL lalkitab-ch27-wave-w47 <-> bphs1-ch32-035 [positional_alternate_result] score=0.0425
POSITIONAL lalkitab-ch27-proh-03 <-> bphs1-ch17-031 [positional_alternate_result] score=0.0752
POSITIONAL lalkitab-ch27-wave-w44 <-> bphs1-ch12-013 [positional_alternate_result] score=0.0282
POSITIONAL lalkitab-ch27-wave-w44 <-> bphs1-ch17-014 [positional_alternate_result] score=0.0352
POSITIONAL lalkitab-ch27-proh-04 <-> bphs1-ch17-028 [positional_alternate_result] score=0.1102
POSITIONAL lalkitab-ch27-proh-04 <-> bphs1-ch19-004 [positional_alternate_result] score=0.1545
POSITIONAL lalkitab-ch27-proh-04 <-> bphs1-ch32-025 [positional_alternate_result] score=0.1577
POSITIONAL lalkitab-ch27-proh-04 <-> bphs1-ch32-039 [positional_alternate_result] score=0.1110
POSITIONAL lalkitab-ch27-wave-w39 <-> bphs1-ch17-028 [positional_alternate_result] score=0.0506
POSITIONAL lalkitab-ch27-wave-w39 <-> bphs1-ch19-004 [positional_alternate_result] score=0.0493
POSITIONAL lalkitab-ch27-wave-w39 <-> bphs1-ch32-025 [positional_alternate_result] score=0.0430
POSITIONAL lalkitab-ch27-wave-w39 <-> bphs1-ch32-039 [positional_alternate_result] score=0.0363
POSITIONAL lalkitab-ch27-wave-w14 <-> bphs1-ch16-028 [positional_alternate_result] score=0.0386
POSITIONAL lalkitab-ch25-sun-h7 <-> bphs1-ch18-008 [positional_alternate_result] score=0.0810
POSITIONAL lalkitab-ch25-sun-h7 <-> bphs1-ch18-031 [positional_alternate_result] score=0.0762
POSITIONAL lalkitab-ch27-wave-w10 <-> bphs1-ch18-003 [positional_alternate_result] score=0.0911
POSITIONAL lalkitab-ch27-wave-w10 <-> bphs1-ch18-017 [positional_alternate_result] score=0.0436
POSITIONAL lalkitab-ch27-wave-w10 <-> bphs1-ch32-024 [positional_alternate_result] score=0.0517
POSITIONAL lalkitab-ch27-wave-w10 <-> bphs1-ch32-038 [positional_alternate_result] score=0.0436
POSITIONAL lalkitab-ch27-wave-w38 <-> bphs1-ch18-003 [positional_alternate_result] score=0.0701
POSITIONAL lalkitab-ch27-wave-w38 <-> bphs1-ch18-017 [positional_alternate_result] score=0.0472
POSITIONAL lalkitab-ch27-wave-w38 <-> bphs1-ch32-024 [positional_alternate_result] score=0.0490
POSITIONAL lalkitab-ch27-wave-w38 <-> bphs1-ch32-038 [positional_alternate_result] score=0.0521
POSITIONAL lalkitab-ch27-proh-07 <-> bphs1-ch18-046 [positional_alternate_result] score=0.1213
Dry run complete. No source JSON files were changed.
Report written to /Users/apple/DailyHoroscope-Migration/KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_lalkitab_vs_bphs_vol1_20260608_210517.json

--- Pass 1 Triage Summary ---
Rules in LK (A):                     467
Rules in BPHS Vol 1 (B):             1456
Pairs evaluated:                     679,952

TF-IDF similarity matches:           0
Contradiction pairs:                 0
Positional conflicts:                80

TRIAGE BREAKDOWN:
  positional_polarity_conflict : 0  (PATCH -- genuine cross-system conflict)
  positional_alternate_result  : 80  (REVIEW -- contextual, no patch)

CONTEXTUAL ALTERNATE RESULTS (review-only):
  [jupiter in house 11]  (1 pair(s))
    lalkitab-ch27-wave-w42 vs bphs1-ch32-042  score=0.0766
  [jupiter in house 2]  (6 pair(s))
    lalkitab-ch27-wave-w02 vs bphs1-ch13-007  score=0.0422
    lalkitab-ch27-wave-w02 vs bphs1-ch18-032  score=0.0860
    lalkitab-ch27-wave-w02 vs bphs1-ch32-033  score=0.0538
    ... and 3 more
  [jupiter in house 5]  (9 pair(s))
    lalkitab-ch27-wave-w07 vs bphs1-ch16-019  score=0.0536
    lalkitab-ch27-wave-w07 vs bphs1-ch32-023  score=0.0530
    lalkitab-ch27-wave-w07 vs bphs1-ch32-036  score=0.0512
    ... and 6 more
  [jupiter in house 7]  (2 pair(s))
    lalkitab-ch27-proh-09 vs bphs1-ch18-012  score=0.0922
    lalkitab-ch27-proh-09 vs bphs1-ch18-016  score=0.0599
  [jupiter in house 9]  (4 pair(s))
    lalkitab-ch27-wave-w25 vs bphs1-ch32-040  score=0.0493
    lalkitab-ch27-wave-w25 vs bphs1-ch39-040  score=0.0717
    lalkitab-ch27-wave-w32 vs bphs1-ch32-040  score=0.0432
    ... and 1 more
  [mars in house 2]  (1 pair(s))
    lalkitab-ch25-mars-h2 vs bphs1-ch42-015  score=0.0574
  [mars in house 3]  (12 pair(s))
    lalkitab-ch27-wave-w04 vs bphs1-ch14-017  score=0.0385
    lalkitab-ch27-wave-w04 vs bphs1-ch32-021  score=0.0282
    lalkitab-ch27-wave-w04 vs bphs1-ch32-034  score=0.0347
    ... and 9 more
  [mercury in house 1]  (2 pair(s))
    lalkitab-ch25-mercury-h1 vs bphs1-ch15-005  score=0.0645
    lalkitab-ch25-mercury-h1 vs bphs1-ch17-011  score=0.0691
  [mercury in house 6]  (2 pair(s))
    lalkitab-ch27-wave-w23 vs bphs1-ch32-022  score=0.0455
    lalkitab-ch27-wave-w49 vs bphs1-ch32-022  score=0.0469
  [mercury in house 7]  (3 pair(s))
    lalkitab-ch25-mercury-h7 vs bphs1-ch18-011  score=0.0612
    lalkitab-ch27-wave-w11 vs bphs1-ch18-011  score=0.0478
    lalkitab-ch27-wave-w30 vs bphs1-ch18-011  score=0.0515
  [moon in house 1]  (4 pair(s))
    lalkitab-ch25-moon-h1 vs bphs1-ch17-006  score=0.0588
    lalkitab-ch25-moon-h1 vs bphs1-ch17-007  score=0.0468
    lalkitab-ch25-moon-h1 vs bphs1-ch17-008  score=0.0464
    ... and 1 more
  [moon in house 10]  (1 pair(s))
    lalkitab-ch25-moon-h10 vs bphs1-ch45-022  score=0.2220
  [moon in house 3]  (2 pair(s))
    lalkitab-ch25-moon-h3 vs bphs1-ch14-013  score=0.0743
    lalkitab-ch25-moon-h3 vs bphs1-ch14-014  score=0.0725
  [moon in house 4]  (8 pair(s))
    lalkitab-ch27-wave-w05 vs bphs1-ch32-020  score=0.0344
    lalkitab-ch27-wave-w05 vs bphs1-ch32-035  score=0.0340
    lalkitab-ch27-wave-w27 vs bphs1-ch32-020  score=0.0340
    ... and 5 more
  [moon in house 6]  (1 pair(s))
    lalkitab-ch27-proh-03 vs bphs1-ch17-031  score=0.0752
  [saturn in house 1]  (2 pair(s))
    lalkitab-ch27-wave-w44 vs bphs1-ch12-013  score=0.0282
    lalkitab-ch27-wave-w44 vs bphs1-ch17-014  score=0.0352
  [saturn in house 8]  (8 pair(s))
    lalkitab-ch27-proh-04 vs bphs1-ch17-028  score=0.1102
    lalkitab-ch27-proh-04 vs bphs1-ch19-004  score=0.1545
    lalkitab-ch27-proh-04 vs bphs1-ch32-025  score=0.1577
    ... and 5 more
  [saturn in house 9]  (1 pair(s))
    lalkitab-ch27-wave-w14 vs bphs1-ch16-028  score=0.0386
  [sun in house 7]  (2 pair(s))
    lalkitab-ch25-sun-h7 vs bphs1-ch18-008  score=0.0810
    lalkitab-ch25-sun-h7 vs bphs1-ch18-031  score=0.0762
  [venus in house 7]  (8 pair(s))
    lalkitab-ch27-wave-w10 vs bphs1-ch18-003  score=0.0911
    lalkitab-ch27-wave-w10 vs bphs1-ch18-017  score=0.0436
    lalkitab-ch27-wave-w10 vs bphs1-ch32-024  score=0.0517
    ... and 5 more
  [venus in house 9]  (1 pair(s))
    lalkitab-ch27-proh-07 vs bphs1-ch18-046  score=0.1213

============================================================
PASS 1 ✅  CLEAN -- LK is clear against BPHS Vol 1.
============================================================

============================================================
PASS 2 -- Lal Kitab vs BPHS Vol 2
============================================================
--- Run dedup (LK vs BPHS Vol 2) ---
[contradiction guard] Skipped 128 rules from A and 142 rules from B with no meaningful condition fields.
[positional] Keyed 44 planet×position groups from A, 9 from B -- 0 shared keys.
Loaded 467 valid rules from folder-a: /private/tmp/lalkitab_rules_for_dedup
Loaded 400 valid rules from folder-b: /Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode
Rules in A: 467
Rules in B: 400
Pairs evaluated: 186800
Similarity matches: 0
Contradiction pairs: 0
Positional conflicts: 0
Dry run complete. No source JSON files were changed.
Report written to /Users/apple/DailyHoroscope-Migration/KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_lalkitab_vs_bphs_vol2_20260608_210517.json

--- Pass 2 Triage Summary ---
Rules in LK (A):                     467
Rules in BPHS Vol 2 (B):             400
Pairs evaluated:                     186,800

TF-IDF similarity matches:           0
Contradiction pairs:                 0
Positional conflicts:                0

TRIAGE BREAKDOWN:
  positional_polarity_conflict : 0  (PATCH -- genuine cross-system conflict)
  positional_alternate_result  : 0  (REVIEW -- contextual, no patch)

============================================================
PASS 2 ✅  CLEAN -- LK is clear against BPHS Vol 2.
============================================================

JSON report (Vol 1) : KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_lalkitab_vs_bphs_vol1_20260608_210517.json
JSON report (Vol 2) : KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_lalkitab_vs_bphs_vol2_20260608_210517.json
Log saved           : KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_lalkitab_vs_bphs_20260608_210517.md
