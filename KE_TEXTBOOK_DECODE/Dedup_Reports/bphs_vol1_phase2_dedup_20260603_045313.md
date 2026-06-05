============================================================
BPHS Vol 1 Phase 2 -- Retroactive Positional Conflict Dedup
Method: Full MongoDB export (excludes batch bphs-vol1-phase2-v1-20260601)
Run: 20260603_045313
============================================================

--- STEP 1/3: Export MongoDB → /tmp/mongo_existing_rules_dedup ---
Cleared stale export directory: /tmp/mongo_existing_rules_dedup
Excluding batch: bphs-vol1-phase2-v1-20260601
Fetched 9968 rules from MongoDB
  300_Combinations: 329 rules → 300_Combinations_Rules.json
  300_Horoscopes_Vol_1: 57 rules → 300_Horoscopes_Vol_1_Rules.json
  BPHS_Vol_2: 249 rules → BPHS_Vol_2_Rules.json
  Longevity_&_Unnatural_Death: 44 rules → Longevity_&_Unnatural_Death_Rules.json
  Longevity_(58_Chapters): 149 rules → Longevity_(58_Chapters)_Rules.json
  Phaladeepika: 1218 rules → Phaladeepika_Rules.json
  unknown: 7922 rules → unknown_Rules.json

Total exported: 9968 rules across 7 source_book groups
Output directory: /tmp/mongo_existing_rules_dedup

--- STEP 2/3: Run dedup (BPHS Vol 1 Ph2 vs full MongoDB) ---
[warn] Skipping /Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/BPHS_Ch16_Effects_5th_House_Rules.json: unrecognised JSON structure (expected list or dict with 'rules' key)
[warn] Skipping /Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/BPHS_Ch17_Effects_6th_House_Rules.json: unrecognised JSON structure (expected list or dict with 'rules' key)
[warn] Skipping /Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/BPHS_Ch18_Effects_7th_House_Rules.json: unrecognised JSON structure (expected list or dict with 'rules' key)
[warn] Skipping /Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/BPHS_Ch20_Effects_9th_House_Rules.json: unrecognised JSON structure (expected list or dict with 'rules' key)
[warn] Skipping /Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/BPHS_Ch24_Effects_Bhava_Lords_Rules.json: unrecognised JSON structure (expected list or dict with 'rules' key)
[contradiction guard] Skipped 885 rules from A and 2577 rules from B with no meaningful condition fields.
[positional] Keyed 240 planet×position groups from A, 258 from B -- 54 shared keys.
Loaded 1456 valid rules from folder-a: /Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode
Loaded 9968 valid rules from folder-b: /private/tmp/mongo_existing_rules_dedup
Rules in A: 1456
Rules in B: 9968
Pairs evaluated: 14513408
Similarity matches: 19
Contradiction pairs: 0
Positional conflicts: 2387
MATCH bphs1-ch16-007 <-> R-BPHS16-008 [near_identical] score=0.9259
MATCH bphs1-ch14-009 <-> R-BPHS14-022 [near_identical] score=0.9114
MATCH bphs1-ch14-010 <-> R-BPHS14-023 [near_identical] score=0.9019
MATCH bphs1-ch15-014 <-> R-BPHS15-019 [partial_overlap] score=0.8858
MATCH bphs1-ch16-025 <-> R-BPHS16-034 [partial_overlap] score=0.8801
MATCH bphs1-ch16-005 <-> R-BPHS16-006 [partial_overlap] score=0.8765
MATCH bphs1-ch16-012 <-> R-BPHS16-015 [partial_overlap] score=0.8729
MATCH bphs1-ch13-014 <-> R-BPHS13-014 [partial_overlap] score=0.8664
MATCH bphs1-ch15-011 <-> R-BPHS15-014 [partial_overlap] score=0.8617
MATCH bphs1-ch16-006 <-> R-BPHS16-007 [partial_overlap] score=0.8611
MATCH bphs1-ch16-009 <-> R-BPHS16-012 [partial_overlap] score=0.8602
MATCH bphs1-ch16-021 <-> R-BPHS16-029 [partial_overlap] score=0.8589
MATCH bphs1-ch16-003 <-> R-BPHS16-003 [partial_overlap] score=0.8475
MATCH bphs1-ch15-007 <-> R-BPHS15-010 [partial_overlap] score=0.8457
MATCH bphs1-ch14-013 <-> R-BPHS14-026 [partial_overlap] score=0.8414
MATCH bphs1-ch15-012 <-> R-BPHS15-015 [partial_overlap] score=0.8332
MATCH bphs1-ch16-001 <-> R-BPHS16-001 [partial_overlap] score=0.8314
MATCH bphs1-ch15-009 <-> R-BPHS15-012 [partial_overlap] score=0.8257
MATCH bphs1-ch15-005 <-> R-BPHS15-008 [partial_overlap] score=0.8247
POSITIONAL bphs1-ch36-005 <-> pd-ch06-021 [positional_alternate_result] score=0.1588
POSITIONAL bphs1-ch36-005 <-> pd-ch16-049 [positional_alternate_result] score=0.2371
POSITIONAL bphs1-ch12-012 <-> R-ATEXTB-JUP-1H-ARI-V-048-01 [positional_alternate_result] score=0.0271
POSITIONAL bphs1-ch12-012 <-> R-ATEXTB-JUP-1H-CAP-V-048-02 [positional_alternate_result] score=0.0287
POSITIONAL bphs1-ch12-012 <-> R-ATEXTB-JUP-1H-DEB-V-048-09 [positional_alternate_result] score=0.0262
POSITIONAL bphs1-ch12-012 <-> R-ATEXTB-JUP-1H-EXA-V-048-10 [positional_alternate_result] score=0.0196
POSITIONAL bphs1-ch12-012 <-> R-ATEXTB-JUP-1H-LEO-V-048-03 [positional_alternate_result] score=0.0268
POSITIONAL bphs1-ch12-012 <-> R-ATEXTB-JUP-1H-PIS-V-048-04 [positional_alternate_result] score=0.0234
POSITIONAL bphs1-ch12-012 <-> R-ATEXTB-JUP-1H-SAG-V-048-05 [positional_alternate_result] score=0.0300
POSITIONAL bphs1-ch12-012 <-> R-ATEXTB-JUP-1H-SCO-V-048-06 [positional_alternate_result] score=0.0246
POSITIONAL bphs1-ch12-012 <-> R-ATEXTB-JUP-1H-TAU-V-048-07 [positional_alternate_result] score=0.0289
POSITIONAL bphs1-ch12-012 <-> R-ATEXTB-JUP-1H-V-048 [positional_alternate_result] score=0.0493
POSITIONAL bphs1-ch12-012 <-> R-ATEXTB-JUP-1H-VIR-V-048-08 [positional_alternate_result] score=0.0287
POSITIONAL bphs1-ch12-012 <-> R-TBA15-742 [positional_alternate_result] score=0.0184
POSITIONAL bphs1-ch12-012 <-> R-TBA15-743 [positional_alternate_result] score=0.0371
POSITIONAL bphs1-ch12-012 <-> R-TBA15-744 [positional_alternate_result] score=0.0248
POSITIONAL bphs1-ch12-012 <-> R-TBA15-745 [positional_alternate_result] score=0.0292
POSITIONAL bphs1-ch12-012 <-> R-TBA15-746 [positional_alternate_result] score=0.0239
POSITIONAL bphs1-ch12-012 <-> R-TBA15-747 [positional_alternate_result] score=0.0334
POSITIONAL bphs1-ch12-012 <-> R-TBA15-748 [positional_alternate_result] score=0.0285
POSITIONAL bphs1-ch12-012 <-> R-TBA15-749 [positional_alternate_result] score=0.0281
POSITIONAL bphs1-ch12-012 <-> R-TBA15-750 [positional_alternate_result] score=0.0353
POSITIONAL bphs1-ch12-012 <-> R-TBA15-751 [positional_alternate_result] score=0.0312
POSITIONAL bphs1-ch12-012 <-> R-TBA15-752 [positional_alternate_result] score=0.0310
POSITIONAL bphs1-ch12-012 <-> R-TBA15-753 [positional_alternate_result] score=0.0311
POSITIONAL bphs1-ch12-012 <-> R-TBA15-754 [positional_alternate_result] score=0.0298
POSITIONAL bphs1-ch12-012 <-> R-TBA15-755 [positional_alternate_result] score=0.0241
POSITIONAL bphs1-ch12-012 <-> R-TBA15-756 [positional_alternate_result] score=0.0248
POSITIONAL bphs1-ch12-012 <-> R-TBA15-757 [positional_alternate_result] score=0.0248
POSITIONAL bphs1-ch12-012 <-> R-TBA15-758 [positional_alternate_result] score=0.0284
POSITIONAL bphs1-ch12-012 <-> R-TBA15-759 [positional_alternate_result] score=0.0272
POSITIONAL bphs1-ch12-012 <-> R-TBA15-760 [positional_alternate_result] score=0.0208
POSITIONAL bphs1-ch12-012 <-> R-TBA15-761 [positional_alternate_result] score=0.0231
POSITIONAL bphs1-ch12-012 <-> R-TBA15-762 [positional_alternate_result] score=0.0354
POSITIONAL bphs1-ch12-012 <-> R-TBA15-763 [positional_alternate_result] score=0.0307
POSITIONAL bphs1-ch12-012 <-> R-TBA15-764 [positional_alternate_result] score=0.0135
POSITIONAL bphs1-ch12-012 <-> kp-ch12-002 [positional_polarity_conflict] score=0.0337
POSITIONAL bphs1-ch12-012 <-> pd-ch08-050 [positional_alternate_result] score=0.0670
POSITIONAL bphs1-ch12-012 <-> pd-ch13-022 [positional_alternate_result] score=0.0379
POSITIONAL bphs1-ch17-012 <-> R-ATEXTB-JUP-1H-ARI-V-048-01 [positional_alternate_result] score=0.0247
POSITIONAL bphs1-ch17-012 <-> R-ATEXTB-JUP-1H-CAP-V-048-02 [positional_alternate_result] score=0.0261
POSITIONAL bphs1-ch17-012 <-> R-ATEXTB-JUP-1H-DEB-V-048-09 [positional_alternate_result] score=0.0181
POSITIONAL bphs1-ch17-012 <-> R-ATEXTB-JUP-1H-EXA-V-048-10 [positional_alternate_result] score=0.0228
POSITIONAL bphs1-ch17-012 <-> R-ATEXTB-JUP-1H-LEO-V-048-03 [positional_alternate_result] score=0.0244
POSITIONAL bphs1-ch17-012 <-> R-ATEXTB-JUP-1H-PIS-V-048-04 [positional_alternate_result] score=0.0186
POSITIONAL bphs1-ch17-012 <-> R-ATEXTB-JUP-1H-SAG-V-048-05 [positional_alternate_result] score=0.0277
POSITIONAL bphs1-ch17-012 <-> R-ATEXTB-JUP-1H-SCO-V-048-06 [positional_alternate_result] score=0.0224
POSITIONAL bphs1-ch17-012 <-> R-ATEXTB-JUP-1H-TAU-V-048-07 [positional_alternate_result] score=0.0262
POSITIONAL bphs1-ch17-012 <-> R-ATEXTB-JUP-1H-V-048 [positional_alternate_result] score=0.0353
POSITIONAL bphs1-ch17-012 <-> R-ATEXTB-JUP-1H-VIR-V-048-08 [positional_alternate_result] score=0.0261
POSITIONAL bphs1-ch17-012 <-> R-TBA15-742 [positional_alternate_result] score=0.0423
POSITIONAL bphs1-ch17-012 <-> R-TBA15-743 [positional_alternate_result] score=0.0800
POSITIONAL bphs1-ch17-012 <-> R-TBA15-744 [positional_alternate_result] score=0.0601
POSITIONAL bphs1-ch17-012 <-> R-TBA15-745 [positional_alternate_result] score=0.0629
POSITIONAL bphs1-ch17-012 <-> R-TBA15-746 [positional_alternate_result] score=0.0579
POSITIONAL bphs1-ch17-012 <-> R-TBA15-747 [positional_alternate_result] score=0.0625
POSITIONAL bphs1-ch17-012 <-> R-TBA15-748 [positional_alternate_result] score=0.0690
POSITIONAL bphs1-ch17-012 <-> R-TBA15-749 [positional_alternate_result] score=0.0681
POSITIONAL bphs1-ch17-012 <-> R-TBA15-750 [positional_alternate_result] score=0.0661
POSITIONAL bphs1-ch17-012 <-> R-TBA15-751 [positional_alternate_result] score=0.0755
POSITIONAL bphs1-ch17-012 <-> R-TBA15-752 [positional_alternate_result] score=0.0751
POSITIONAL bphs1-ch17-012 <-> R-TBA15-753 [positional_alternate_result] score=0.0755
POSITIONAL bphs1-ch17-012 <-> R-TBA15-754 [positional_alternate_result] score=0.0559
POSITIONAL bphs1-ch17-012 <-> R-TBA15-755 [positional_alternate_result] score=0.0584
POSITIONAL bphs1-ch17-012 <-> R-TBA15-756 [positional_alternate_result] score=0.0501
POSITIONAL bphs1-ch17-012 <-> R-TBA15-757 [positional_alternate_result] score=0.0465
POSITIONAL bphs1-ch17-012 <-> R-TBA15-758 [positional_alternate_result] score=0.0560
POSITIONAL bphs1-ch17-012 <-> R-TBA15-759 [positional_alternate_result] score=0.0585
POSITIONAL bphs1-ch17-012 <-> R-TBA15-760 [positional_alternate_result] score=0.0512
POSITIONAL bphs1-ch17-012 <-> R-TBA15-761 [positional_alternate_result] score=0.0570
POSITIONAL bphs1-ch17-012 <-> R-TBA15-762 [positional_alternate_result] score=0.0798
POSITIONAL bphs1-ch17-012 <-> R-TBA15-763 [positional_alternate_result] score=0.0662
POSITIONAL bphs1-ch17-012 <-> R-TBA15-764 [positional_alternate_result] score=0.0318
POSITIONAL bphs1-ch17-012 <-> kp-ch12-002 [positional_polarity_conflict] score=0.0509
POSITIONAL bphs1-ch17-012 <-> pd-ch08-050 [positional_alternate_result] score=0.0927
POSITIONAL bphs1-ch17-012 <-> pd-ch13-022 [positional_alternate_result] score=0.0347
POSITIONAL bphs1-ch32-042 <-> R-ATEXTB-JUP-11H-007 [positional_alternate_result] score=0.0569
POSITIONAL bphs1-ch32-042 <-> R-ATEXTB-JUP-11H-CAN-V-057-01 [positional_alternate_result] score=0.0579
POSITIONAL bphs1-ch32-042 <-> R-ATEXTB-JUP-11H-DEB-V-057-02 [positional_alternate_result] score=0.0716
POSITIONAL bphs1-ch32-042 <-> R-ATEXTB-JUP-11H-V-057 [positional_alternate_result] score=0.0496
POSITIONAL bphs1-ch32-042 <-> R-TBA15-884 [positional_alternate_result] score=0.0516
POSITIONAL bphs1-ch32-042 <-> R-TBA15-885 [positional_alternate_result] score=0.0746
POSITIONAL bphs1-ch32-042 <-> R-TBA15-886 [positional_alternate_result] score=0.0866
POSITIONAL bphs1-ch32-042 <-> R-TBA15-887 [positional_alternate_result] score=0.0771
POSITIONAL bphs1-ch32-042 <-> R-TBA15-888 [positional_alternate_result] score=0.0479
POSITIONAL bphs1-ch32-042 <-> lalkitab-ch27-wave-w42 [positional_alternate_result] score=0.0528
POSITIONAL bphs1-ch32-042 <-> pd-ch08-060 [positional_alternate_result] score=0.0647
POSITIONAL bphs1-ch13-007 <-> R-ATEXTB-JUP-2H-DEB-V-049-03 [positional_alternate_result] score=0.0201
POSITIONAL bphs1-ch13-007 <-> R-ATEXTB-JUP-2H-EXA-V-049-04 [positional_alternate_result] score=0.0280
POSITIONAL bphs1-ch13-007 <-> R-ATEXTB-JUP-2H-OWN-V-049-05 [positional_alternate_result] score=0.0280
POSITIONAL bphs1-ch13-007 <-> R-ATEXTB-JUP-2H-SAG-V-049-01 [positional_alternate_result] score=0.0277
POSITIONAL bphs1-ch13-007 <-> R-ATEXTB-JUP-2H-V-049 [positional_alternate_result] score=0.0723
POSITIONAL bphs1-ch13-007 <-> R-ATEXTB-JUP-2H-VIR-V-049-02 [positional_alternate_result] score=0.0748
POSITIONAL bphs1-ch13-007 <-> R-BRIHAT-JUP-2H-169 [positional_alternate_result] score=0.0681
POSITIONAL bphs1-ch13-007 <-> R-TBA15-765 [positional_alternate_result] score=0.0274
POSITIONAL bphs1-ch13-007 <-> R-TBA15-766 [positional_alternate_result] score=0.1527
POSITIONAL bphs1-ch13-007 <-> R-TBA15-767 [positional_alternate_result] score=0.0713
POSITIONAL bphs1-ch13-007 <-> R-TBA15-768 [positional_alternate_result] score=0.0954
POSITIONAL bphs1-ch13-007 <-> R-TBA15-769 [positional_alternate_result] score=0.1222
POSITIONAL bphs1-ch13-007 <-> R-TBA15-770 [positional_alternate_result] score=0.1124
POSITIONAL bphs1-ch13-007 <-> R-TBA15-771 [positional_alternate_result] score=0.1296
POSITIONAL bphs1-ch13-007 <-> R-TBA15-772 [positional_alternate_result] score=0.1658
POSITIONAL bphs1-ch13-007 <-> R-TBA15-773 [positional_alternate_result] score=0.1580
POSITIONAL bphs1-ch13-007 <-> R-TBA15-774 [positional_alternate_result] score=0.1056
POSITIONAL bphs1-ch13-007 <-> R-TBA15-775 [positional_alternate_result] score=0.1058
POSITIONAL bphs1-ch13-007 <-> R-TBA15-776 [positional_alternate_result] score=0.1102
POSITIONAL bphs1-ch13-007 <-> R-TBA15-777 [positional_alternate_result] score=0.0375
POSITIONAL bphs1-ch13-007 <-> lalkitab-ch27-wave-w02 [positional_alternate_result] score=0.0257
POSITIONAL bphs1-ch13-007 <-> lalkitab-ch27-wave-w45 [positional_alternate_result] score=0.0280
POSITIONAL bphs1-ch13-007 <-> pd-ch08-051 [positional_alternate_result] score=0.1466
POSITIONAL bphs1-ch18-032 <-> R-ATEXTB-JUP-2H-DEB-V-049-03 [positional_alternate_result] score=0.0281
POSITIONAL bphs1-ch18-032 <-> R-ATEXTB-JUP-2H-EXA-V-049-04 [positional_alternate_result] score=0.0235
POSITIONAL bphs1-ch18-032 <-> R-ATEXTB-JUP-2H-OWN-V-049-05 [positional_alternate_result] score=0.0235
POSITIONAL bphs1-ch18-032 <-> R-ATEXTB-JUP-2H-SAG-V-049-01 [positional_alternate_result] score=0.0554
POSITIONAL bphs1-ch18-032 <-> R-ATEXTB-JUP-2H-V-049 [positional_alternate_result] score=0.0506
POSITIONAL bphs1-ch18-032 <-> R-ATEXTB-JUP-2H-VIR-V-049-02 [positional_alternate_result] score=0.0245
POSITIONAL bphs1-ch18-032 <-> R-BRIHAT-JUP-2H-169 [positional_alternate_result] score=0.0718
POSITIONAL bphs1-ch18-032 <-> R-TBA15-765 [positional_alternate_result] score=0.0329
POSITIONAL bphs1-ch18-032 <-> R-TBA15-766 [positional_alternate_result] score=0.0929
POSITIONAL bphs1-ch18-032 <-> R-TBA15-767 [positional_alternate_result] score=0.0539
POSITIONAL bphs1-ch18-032 <-> R-TBA15-768 [positional_alternate_result] score=0.1101
POSITIONAL bphs1-ch18-032 <-> R-TBA15-769 [positional_alternate_result] score=0.0862
POSITIONAL bphs1-ch18-032 <-> R-TBA15-770 [positional_alternate_result] score=0.0757
POSITIONAL bphs1-ch18-032 <-> R-TBA15-771 [positional_alternate_result] score=0.0878
POSITIONAL bphs1-ch18-032 <-> R-TBA15-772 [positional_alternate_result] score=0.1005
POSITIONAL bphs1-ch18-032 <-> R-TBA15-773 [positional_alternate_result] score=0.1046
POSITIONAL bphs1-ch18-032 <-> R-TBA15-774 [positional_alternate_result] score=0.0790
POSITIONAL bphs1-ch18-032 <-> R-TBA15-775 [positional_alternate_result] score=0.0792
POSITIONAL bphs1-ch18-032 <-> R-TBA15-776 [positional_alternate_result] score=0.0756
POSITIONAL bphs1-ch18-032 <-> R-TBA15-777 [positional_alternate_result] score=0.0643
POSITIONAL bphs1-ch18-032 <-> lalkitab-ch27-wave-w02 [positional_alternate_result] score=0.0596
POSITIONAL bphs1-ch18-032 <-> lalkitab-ch27-wave-w45 [positional_alternate_result] score=0.0398
POSITIONAL bphs1-ch18-032 <-> pd-ch08-051 [positional_alternate_result] score=0.1532
POSITIONAL bphs1-ch32-033 <-> R-ATEXTB-JUP-2H-DEB-V-049-03 [positional_alternate_result] score=0.0126
POSITIONAL bphs1-ch32-033 <-> R-ATEXTB-JUP-2H-EXA-V-049-04 [positional_alternate_result] score=0.0178
POSITIONAL bphs1-ch32-033 <-> R-ATEXTB-JUP-2H-OWN-V-049-05 [positional_alternate_result] score=0.0178
POSITIONAL bphs1-ch32-033 <-> R-ATEXTB-JUP-2H-SAG-V-049-01 [positional_alternate_result] score=0.0197
POSITIONAL bphs1-ch32-033 <-> R-ATEXTB-JUP-2H-V-049 [positional_alternate_result] score=0.0271
POSITIONAL bphs1-ch32-033 <-> R-ATEXTB-JUP-2H-VIR-V-049-02 [positional_alternate_result] score=0.0183
POSITIONAL bphs1-ch32-033 <-> R-BRIHAT-JUP-2H-169 [positional_alternate_result] score=0.1163
POSITIONAL bphs1-ch32-033 <-> R-TBA15-765 [positional_alternate_result] score=0.0330
POSITIONAL bphs1-ch32-033 <-> R-TBA15-766 [positional_alternate_result] score=0.0772
POSITIONAL bphs1-ch32-033 <-> R-TBA15-767 [positional_alternate_result] score=0.0428
POSITIONAL bphs1-ch32-033 <-> R-TBA15-768 [positional_alternate_result] score=0.0581
POSITIONAL bphs1-ch32-033 <-> R-TBA15-769 [positional_alternate_result] score=0.0734
POSITIONAL bphs1-ch32-033 <-> R-TBA15-770 [positional_alternate_result] score=0.0562
POSITIONAL bphs1-ch32-033 <-> R-TBA15-771 [positional_alternate_result] score=0.0772
POSITIONAL bphs1-ch32-033 <-> R-TBA15-772 [positional_alternate_result] score=0.0848
POSITIONAL bphs1-ch32-033 <-> R-TBA15-773 [positional_alternate_result] score=0.0889
POSITIONAL bphs1-ch32-033 <-> R-TBA15-774 [positional_alternate_result] score=0.0666
POSITIONAL bphs1-ch32-033 <-> R-TBA15-775 [positional_alternate_result] score=0.0667
POSITIONAL bphs1-ch32-033 <-> R-TBA15-776 [positional_alternate_result] score=0.0620
POSITIONAL bphs1-ch32-033 <-> R-TBA15-777 [positional_alternate_result] score=0.0557
POSITIONAL bphs1-ch32-033 <-> lalkitab-ch27-wave-w02 [positional_alternate_result] score=0.0342
POSITIONAL bphs1-ch32-033 <-> lalkitab-ch27-wave-w45 [positional_alternate_result] score=0.0252
POSITIONAL bphs1-ch32-033 <-> pd-ch08-051 [positional_alternate_result] score=0.0880
POSITIONAL bphs1-ch16-019 <-> R-ATEXTB-JUP-5H-ARI-V-052-01 [positional_alternate_result] score=0.0196
POSITIONAL bphs1-ch16-019 <-> R-ATEXTB-JUP-5H-DEB-V-052-02 [positional_alternate_result] score=0.0319
POSITIONAL bphs1-ch16-019 <-> R-ATEXTB-JUP-5H-EXA-V-052-03 [positional_alternate_result] score=0.0232
POSITIONAL bphs1-ch16-019 <-> R-ATEXTB-JUP-5H-OWN-V-052-04 [positional_alternate_result] score=0.0232
POSITIONAL bphs1-ch16-019 <-> R-ATEXTB-JUP-5H-V-052 [positional_alternate_result] score=0.0258
POSITIONAL bphs1-ch16-019 <-> R-TBA15-820 [positional_alternate_result] score=0.0263
POSITIONAL bphs1-ch16-019 <-> R-TBA15-821 [positional_alternate_result] score=0.0553
POSITIONAL bphs1-ch16-019 <-> R-TBA15-822 [positional_alternate_result] score=0.0462
POSITIONAL bphs1-ch16-019 <-> R-TBA15-823 [positional_alternate_result] score=0.0578
POSITIONAL bphs1-ch16-019 <-> R-TBA15-824 [positional_alternate_result] score=0.0407
POSITIONAL bphs1-ch16-019 <-> R-TBA15-825 [positional_alternate_result] score=0.0523
POSITIONAL bphs1-ch16-019 <-> R-TBA15-826 [positional_alternate_result] score=0.0555
POSITIONAL bphs1-ch16-019 <-> R-TBA15-827 [positional_alternate_result] score=0.0425
POSITIONAL bphs1-ch16-019 <-> R-TBA15-828 [positional_alternate_result] score=0.0466
POSITIONAL bphs1-ch16-019 <-> R-TBA15-829 [positional_alternate_result] score=0.0693
POSITIONAL bphs1-ch16-019 <-> R-TBA15-830 [positional_alternate_result] score=0.0375
POSITIONAL bphs1-ch16-019 <-> R-TBA15-831 [positional_alternate_result] score=0.0290
POSITIONAL bphs1-ch16-019 <-> R-TBA15-832 [positional_alternate_result] score=0.0614
POSITIONAL bphs1-ch16-019 <-> lalkitab-ch27-wave-w07 [positional_alternate_result] score=0.0372
POSITIONAL bphs1-ch16-019 <-> lalkitab-ch27-wave-w20 [positional_alternate_result] score=0.0366
POSITIONAL bphs1-ch16-019 <-> lalkitab-ch27-wave-w28 [positional_alternate_result] score=0.0359
POSITIONAL bphs1-ch16-019 <-> pd-ch08-054 [positional_alternate_result] score=0.0518
POSITIONAL bphs1-ch32-023 <-> R-ATEXTB-JUP-5H-ARI-V-052-01 [positional_alternate_result] score=0.0204
POSITIONAL bphs1-ch32-023 <-> R-ATEXTB-JUP-5H-DEB-V-052-02 [positional_alternate_result] score=0.0186
POSITIONAL bphs1-ch32-023 <-> R-ATEXTB-JUP-5H-EXA-V-052-03 [positional_alternate_result] score=0.0350
POSITIONAL bphs1-ch32-023 <-> R-ATEXTB-JUP-5H-OWN-V-052-04 [positional_alternate_result] score=0.0350
POSITIONAL bphs1-ch32-023 <-> R-ATEXTB-JUP-5H-V-052 [positional_alternate_result] score=0.0315
POSITIONAL bphs1-ch32-023 <-> R-TBA15-820 [positional_alternate_result] score=0.0610
POSITIONAL bphs1-ch32-023 <-> R-TBA15-821 [positional_alternate_result] score=0.1411
POSITIONAL bphs1-ch32-023 <-> R-TBA15-822 [positional_alternate_result] score=0.0800
POSITIONAL bphs1-ch32-023 <-> R-TBA15-823 [positional_alternate_result] score=0.1314
POSITIONAL bphs1-ch32-023 <-> R-TBA15-824 [positional_alternate_result] score=0.1017
POSITIONAL bphs1-ch32-023 <-> R-TBA15-825 [positional_alternate_result] score=0.1305
POSITIONAL bphs1-ch32-023 <-> R-TBA15-826 [positional_alternate_result] score=0.1262
POSITIONAL bphs1-ch32-023 <-> R-TBA15-827 [positional_alternate_result] score=0.1078
POSITIONAL bphs1-ch32-023 <-> R-TBA15-828 [positional_alternate_result] score=0.1025
POSITIONAL bphs1-ch32-023 <-> R-TBA15-829 [positional_alternate_result] score=0.1284
POSITIONAL bphs1-ch32-023 <-> R-TBA15-830 [positional_alternate_result] score=0.0983
POSITIONAL bphs1-ch32-023 <-> R-TBA15-831 [positional_alternate_result] score=0.0659
POSITIONAL bphs1-ch32-023 <-> R-TBA15-832 [positional_alternate_result] score=0.1215
POSITIONAL bphs1-ch32-023 <-> lalkitab-ch27-wave-w07 [positional_alternate_result] score=0.0340
POSITIONAL bphs1-ch32-023 <-> lalkitab-ch27-wave-w20 [positional_alternate_result] score=0.0275
POSITIONAL bphs1-ch32-023 <-> lalkitab-ch27-wave-w28 [positional_alternate_result] score=0.0263
POSITIONAL bphs1-ch32-023 <-> pd-ch08-054 [positional_alternate_result] score=0.1444
POSITIONAL bphs1-ch32-036 <-> R-ATEXTB-JUP-5H-ARI-V-052-01 [positional_alternate_result] score=0.0152
POSITIONAL bphs1-ch32-036 <-> R-ATEXTB-JUP-5H-DEB-V-052-02 [positional_alternate_result] score=0.0144
POSITIONAL bphs1-ch32-036 <-> R-ATEXTB-JUP-5H-EXA-V-052-03 [positional_alternate_result] score=0.0286
POSITIONAL bphs1-ch32-036 <-> R-ATEXTB-JUP-5H-OWN-V-052-04 [positional_alternate_result] score=0.0286
POSITIONAL bphs1-ch32-036 <-> R-ATEXTB-JUP-5H-V-052 [positional_alternate_result] score=0.0243
POSITIONAL bphs1-ch32-036 <-> R-TBA15-820 [positional_alternate_result] score=0.0407
POSITIONAL bphs1-ch32-036 <-> R-TBA15-821 [positional_alternate_result] score=0.0698
POSITIONAL bphs1-ch32-036 <-> R-TBA15-822 [positional_alternate_result] score=0.0448
POSITIONAL bphs1-ch32-036 <-> R-TBA15-823 [positional_alternate_result] score=0.0713
POSITIONAL bphs1-ch32-036 <-> R-TBA15-824 [positional_alternate_result] score=0.0638
POSITIONAL bphs1-ch32-036 <-> R-TBA15-825 [positional_alternate_result] score=0.0747
POSITIONAL bphs1-ch32-036 <-> R-TBA15-826 [positional_alternate_result] score=0.0685
POSITIONAL bphs1-ch32-036 <-> R-TBA15-827 [positional_alternate_result] score=0.0637
POSITIONAL bphs1-ch32-036 <-> R-TBA15-828 [positional_alternate_result] score=0.0594
POSITIONAL bphs1-ch32-036 <-> R-TBA15-829 [positional_alternate_result] score=0.0728
POSITIONAL bphs1-ch32-036 <-> R-TBA15-830 [positional_alternate_result] score=0.0682
POSITIONAL bphs1-ch32-036 <-> R-TBA15-831 [positional_alternate_result] score=0.0410
POSITIONAL bphs1-ch32-036 <-> R-TBA15-832 [positional_alternate_result] score=0.0689
POSITIONAL bphs1-ch32-036 <-> lalkitab-ch27-wave-w07 [positional_alternate_result] score=0.0321
POSITIONAL bphs1-ch32-036 <-> lalkitab-ch27-wave-w20 [positional_alternate_result] score=0.0194
POSITIONAL bphs1-ch32-036 <-> lalkitab-ch27-wave-w28 [positional_alternate_result] score=0.0291
POSITIONAL bphs1-ch32-036 <-> pd-ch08-054 [positional_alternate_result] score=0.1344
POSITIONAL bphs1-ch18-012 <-> R-ATEXTB-JUP-7H-AQU-V-054-01 [positional_alternate_result] score=0.0479
POSITIONAL bphs1-ch18-012 <-> R-ATEXTB-JUP-7H-CAP-V-054-02 [positional_alternate_result] score=0.0531
POSITIONAL bphs1-ch18-012 <-> R-ATEXTB-JUP-7H-DEB-V-054-04 [positional_alternate_result] score=0.0350
POSITIONAL bphs1-ch18-012 <-> R-ATEXTB-JUP-7H-ENE-V-054-05 [positional_alternate_result] score=0.0350
POSITIONAL bphs1-ch18-012 <-> R-ATEXTB-JUP-7H-EXA-V-054-06 [positional_alternate_result] score=0.0267
POSITIONAL bphs1-ch18-012 <-> R-ATEXTB-JUP-7H-OWN-V-054-07 [positional_alternate_result] score=0.0291
POSITIONAL bphs1-ch18-012 <-> R-ATEXTB-JUP-7H-PIS-V-054-03 [positional_alternate_result] score=0.0302
POSITIONAL bphs1-ch18-012 <-> R-ATEXTB-JUP-7H-V-054 [positional_alternate_result] score=0.0615
POSITIONAL bphs1-ch18-012 <-> R-TBA15-842 [positional_alternate_result] score=0.0541
POSITIONAL bphs1-ch18-012 <-> R-TBA15-843 [positional_alternate_result] score=0.1119
POSITIONAL bphs1-ch18-012 <-> R-TBA15-844 [positional_alternate_result] score=0.0878
POSITIONAL bphs1-ch18-012 <-> R-TBA15-845 [positional_alternate_result] score=0.1071
POSITIONAL bphs1-ch18-012 <-> R-TBA15-846 [positional_alternate_result] score=0.1004
POSITIONAL bphs1-ch18-012 <-> R-TBA15-847 [positional_alternate_result] score=0.1106
POSITIONAL bphs1-ch18-012 <-> R-TBA15-848 [positional_alternate_result] score=0.1027
POSITIONAL bphs1-ch18-012 <-> R-TBA15-849 [positional_alternate_result] score=0.1045
POSITIONAL bphs1-ch18-012 <-> R-TBA15-850 [positional_alternate_result] score=0.0447
POSITIONAL bphs1-ch18-012 <-> kp-ch12-001 [positional_alternate_result] score=0.0612
POSITIONAL bphs1-ch18-012 <-> lalkitab-ch27-proh-09 [positional_alternate_result] score=0.0632
POSITIONAL bphs1-ch18-012 <-> pd-ch08-056 [positional_polarity_conflict] score=0.1029
POSITIONAL bphs1-ch18-012 <-> pd-ch10-009 [positional_alternate_result] score=0.1350
POSITIONAL bphs1-ch18-016 <-> R-ATEXTB-JUP-7H-AQU-V-054-01 [positional_alternate_result] score=0.0125
POSITIONAL bphs1-ch18-016 <-> R-ATEXTB-JUP-7H-CAP-V-054-02 [positional_alternate_result] score=0.0128
POSITIONAL bphs1-ch18-016 <-> R-ATEXTB-JUP-7H-DEB-V-054-04 [positional_alternate_result] score=0.0229
POSITIONAL bphs1-ch18-016 <-> R-ATEXTB-JUP-7H-ENE-V-054-05 [positional_alternate_result] score=0.0229
POSITIONAL bphs1-ch18-016 <-> R-ATEXTB-JUP-7H-EXA-V-054-06 [positional_alternate_result] score=0.0128
POSITIONAL bphs1-ch18-016 <-> R-ATEXTB-JUP-7H-OWN-V-054-07 [positional_alternate_result] score=0.0220
POSITIONAL bphs1-ch18-016 <-> R-ATEXTB-JUP-7H-PIS-V-054-03 [positional_alternate_result] score=0.0223
POSITIONAL bphs1-ch18-016 <-> R-ATEXTB-JUP-7H-V-054 [positional_alternate_result] score=0.0201
POSITIONAL bphs1-ch18-016 <-> R-TBA15-842 [positional_alternate_result] score=0.0175
POSITIONAL bphs1-ch18-016 <-> R-TBA15-843 [positional_alternate_result] score=0.0431
POSITIONAL bphs1-ch18-016 <-> R-TBA15-844 [positional_alternate_result] score=0.0385
POSITIONAL bphs1-ch18-016 <-> R-TBA15-845 [positional_alternate_result] score=0.0272
POSITIONAL bphs1-ch18-016 <-> R-TBA15-846 [positional_alternate_result] score=0.0266
POSITIONAL bphs1-ch18-016 <-> R-TBA15-847 [positional_alternate_result] score=0.0290
POSITIONAL bphs1-ch18-016 <-> R-TBA15-848 [positional_alternate_result] score=0.0393
POSITIONAL bphs1-ch18-016 <-> R-TBA15-849 [positional_alternate_result] score=0.0399
POSITIONAL bphs1-ch18-016 <-> R-TBA15-850 [positional_alternate_result] score=0.0180
POSITIONAL bphs1-ch18-016 <-> kp-ch12-001 [positional_polarity_conflict] score=0.0477
POSITIONAL bphs1-ch18-016 <-> lalkitab-ch27-proh-09 [positional_alternate_result] score=0.0366
POSITIONAL bphs1-ch18-016 <-> pd-ch08-056 [positional_alternate_result] score=0.0491
POSITIONAL bphs1-ch18-016 <-> pd-ch10-009 [positional_polarity_conflict] score=0.0653
POSITIONAL bphs1-ch32-040 <-> R-ATEXTB-JUP-9H-ARI-V-055-01 [positional_alternate_result] score=0.0097
POSITIONAL bphs1-ch32-040 <-> R-ATEXTB-JUP-9H-CAN-V-055-02 [positional_alternate_result] score=0.0142
POSITIONAL bphs1-ch32-040 <-> R-ATEXTB-JUP-9H-CAP-V-055-03 [positional_alternate_result] score=0.0142
POSITIONAL bphs1-ch32-040 <-> R-ATEXTB-JUP-9H-EXA-V-055-12 [positional_alternate_result] score=0.0206
POSITIONAL bphs1-ch32-040 <-> R-ATEXTB-JUP-9H-GEM-V-055-04 [positional_alternate_result] score=0.0136
POSITIONAL bphs1-ch32-040 <-> R-ATEXTB-JUP-9H-LEO-V-055-05 [positional_alternate_result] score=0.0136
POSITIONAL bphs1-ch32-040 <-> R-ATEXTB-JUP-9H-LIB-V-055-06 [positional_alternate_result] score=0.0135
POSITIONAL bphs1-ch32-040 <-> R-ATEXTB-JUP-9H-PIS-V-055-07 [positional_alternate_result] score=0.0143
POSITIONAL bphs1-ch32-040 <-> R-ATEXTB-JUP-9H-SAG-V-055-08 [positional_alternate_result] score=0.0137
POSITIONAL bphs1-ch32-040 <-> R-ATEXTB-JUP-9H-SCO-V-055-09 [positional_alternate_result] score=0.0137
POSITIONAL bphs1-ch32-040 <-> R-ATEXTB-JUP-9H-TAU-V-055-10 [positional_alternate_result] score=0.0137
POSITIONAL bphs1-ch32-040 <-> R-ATEXTB-JUP-9H-V-055 [positional_alternate_result] score=0.0203
POSITIONAL bphs1-ch32-040 <-> R-ATEXTB-JUP-9H-VIR-V-055-11 [positional_alternate_result] score=0.0137
POSITIONAL bphs1-ch32-040 <-> R-TBA15-861 [positional_alternate_result] score=0.0343
POSITIONAL bphs1-ch32-040 <-> R-TBA15-862 [positional_alternate_result] score=0.0518
POSITIONAL bphs1-ch32-040 <-> R-TBA15-863 [positional_alternate_result] score=0.0401
POSITIONAL bphs1-ch32-040 <-> R-TBA15-864 [positional_alternate_result] score=0.0387
POSITIONAL bphs1-ch32-040 <-> R-TBA15-865 [positional_alternate_result] score=0.0419
POSITIONAL bphs1-ch32-040 <-> R-TBA15-866 [positional_alternate_result] score=0.0419
POSITIONAL bphs1-ch32-040 <-> R-TBA15-867 [positional_alternate_result] score=0.0420
POSITIONAL bphs1-ch32-040 <-> R-TBA15-868 [positional_alternate_result] score=0.0315
POSITIONAL bphs1-ch32-040 <-> R-TBA15-869 [positional_alternate_result] score=0.0408
POSITIONAL bphs1-ch32-040 <-> R-TBA15-870 [positional_alternate_result] score=0.0406
POSITIONAL bphs1-ch32-040 <-> R-TBA15-871 [positional_alternate_result] score=0.0405
POSITIONAL bphs1-ch32-040 <-> R-TBA15-872 [positional_alternate_result] score=0.0403
POSITIONAL bphs1-ch32-040 <-> R-TBA15-873 [positional_alternate_result] score=0.0405
POSITIONAL bphs1-ch32-040 <-> R-TBA15-874 [positional_alternate_result] score=0.0402
POSITIONAL bphs1-ch32-040 <-> R-TBA15-875 [positional_alternate_result] score=0.0408
POSITIONAL bphs1-ch32-040 <-> R-TBA15-876 [positional_alternate_result] score=0.0406
POSITIONAL bphs1-ch32-040 <-> R-TBA15-877 [positional_alternate_result] score=0.0395
POSITIONAL bphs1-ch32-040 <-> R-TBA15-878 [positional_alternate_result] score=0.0408
POSITIONAL bphs1-ch32-040 <-> R-TBA15-879 [positional_alternate_result] score=0.0226
POSITIONAL bphs1-ch32-040 <-> lalkitab-ch27-wave-w25 [positional_alternate_result] score=0.0322
POSITIONAL bphs1-ch32-040 <-> lalkitab-ch27-wave-w32 [positional_alternate_result] score=0.0249
POSITIONAL bphs1-ch32-040 <-> pd-ch08-058 [positional_alternate_result] score=0.0755
POSITIONAL bphs1-ch39-040 <-> R-ATEXTB-JUP-9H-ARI-V-055-01 [positional_alternate_result] score=0.0209
POSITIONAL bphs1-ch39-040 <-> R-ATEXTB-JUP-9H-CAN-V-055-02 [positional_alternate_result] score=0.0306
POSITIONAL bphs1-ch39-040 <-> R-ATEXTB-JUP-9H-CAP-V-055-03 [positional_alternate_result] score=0.0305
POSITIONAL bphs1-ch39-040 <-> R-ATEXTB-JUP-9H-EXA-V-055-12 [positional_alternate_result] score=0.0442
POSITIONAL bphs1-ch39-040 <-> R-ATEXTB-JUP-9H-GEM-V-055-04 [positional_alternate_result] score=0.0292
POSITIONAL bphs1-ch39-040 <-> R-ATEXTB-JUP-9H-LEO-V-055-05 [positional_alternate_result] score=0.0292
POSITIONAL bphs1-ch39-040 <-> R-ATEXTB-JUP-9H-LIB-V-055-06 [positional_alternate_result] score=0.0291
POSITIONAL bphs1-ch39-040 <-> R-ATEXTB-JUP-9H-PIS-V-055-07 [positional_alternate_result] score=0.0306
POSITIONAL bphs1-ch39-040 <-> R-ATEXTB-JUP-9H-SAG-V-055-08 [positional_alternate_result] score=0.0294
POSITIONAL bphs1-ch39-040 <-> R-ATEXTB-JUP-9H-SCO-V-055-09 [positional_alternate_result] score=0.0295
POSITIONAL bphs1-ch39-040 <-> R-ATEXTB-JUP-9H-TAU-V-055-10 [positional_alternate_result] score=0.0295
POSITIONAL bphs1-ch39-040 <-> R-ATEXTB-JUP-9H-V-055 [positional_alternate_result] score=0.0068
POSITIONAL bphs1-ch39-040 <-> R-ATEXTB-JUP-9H-VIR-V-055-11 [positional_alternate_result] score=0.0294
POSITIONAL bphs1-ch39-040 <-> R-TBA15-861 [positional_alternate_result] score=0.0160
POSITIONAL bphs1-ch39-040 <-> R-TBA15-862 [positional_alternate_result] score=0.0642
POSITIONAL bphs1-ch39-040 <-> R-TBA15-863 [positional_alternate_result] score=0.0650
POSITIONAL bphs1-ch39-040 <-> R-TBA15-864 [positional_alternate_result] score=0.0561
POSITIONAL bphs1-ch39-040 <-> R-TBA15-865 [positional_alternate_result] score=0.0608
POSITIONAL bphs1-ch39-040 <-> R-TBA15-866 [positional_alternate_result] score=0.0607
POSITIONAL bphs1-ch39-040 <-> R-TBA15-867 [positional_alternate_result] score=0.0609
POSITIONAL bphs1-ch39-040 <-> R-TBA15-868 [positional_alternate_result] score=0.0551
POSITIONAL bphs1-ch39-040 <-> R-TBA15-869 [positional_alternate_result] score=0.0712
POSITIONAL bphs1-ch39-040 <-> R-TBA15-870 [positional_alternate_result] score=0.0710
POSITIONAL bphs1-ch39-040 <-> R-TBA15-871 [positional_alternate_result] score=0.0707
POSITIONAL bphs1-ch39-040 <-> R-TBA15-872 [positional_alternate_result] score=0.0705
POSITIONAL bphs1-ch39-040 <-> R-TBA15-873 [positional_alternate_result] score=0.0707
POSITIONAL bphs1-ch39-040 <-> R-TBA15-874 [positional_alternate_result] score=0.0703
POSITIONAL bphs1-ch39-040 <-> R-TBA15-875 [positional_alternate_result] score=0.0712
POSITIONAL bphs1-ch39-040 <-> R-TBA15-876 [positional_alternate_result] score=0.0709
POSITIONAL bphs1-ch39-040 <-> R-TBA15-877 [positional_alternate_result] score=0.0545
POSITIONAL bphs1-ch39-040 <-> R-TBA15-878 [positional_alternate_result] score=0.0590
POSITIONAL bphs1-ch39-040 <-> R-TBA15-879 [positional_alternate_result] score=0.0315
POSITIONAL bphs1-ch39-040 <-> lalkitab-ch27-wave-w25 [positional_alternate_result] score=0.0391
POSITIONAL bphs1-ch39-040 <-> lalkitab-ch27-wave-w32 [positional_alternate_result] score=0.0402
POSITIONAL bphs1-ch39-040 <-> pd-ch08-058 [positional_alternate_result] score=0.0387
POSITIONAL bphs1-ch17-016 <-> R-ATEXTB-KET-1H-AQU-V-094-01 [positional_alternate_result] score=0.0319
POSITIONAL bphs1-ch17-016 <-> R-ATEXTB-KET-1H-ARI-V-094-02 [positional_alternate_result] score=0.0226
POSITIONAL bphs1-ch17-016 <-> R-ATEXTB-KET-1H-CAN-V-094-03 [positional_alternate_result] score=0.0287
POSITIONAL bphs1-ch17-016 <-> R-ATEXTB-KET-1H-CAP-V-094-04 [positional_alternate_result] score=0.0228
POSITIONAL bphs1-ch17-016 <-> R-ATEXTB-KET-1H-GEM-V-094-05 [positional_alternate_result] score=0.0141
POSITIONAL bphs1-ch17-016 <-> R-ATEXTB-KET-1H-LEO-V-094-06 [positional_alternate_result] score=0.0243
POSITIONAL bphs1-ch17-016 <-> R-ATEXTB-KET-1H-OWN-V-094-12 [positional_alternate_result] score=0.0325
POSITIONAL bphs1-ch17-016 <-> R-ATEXTB-KET-1H-PIS-V-094-07 [positional_alternate_result] score=0.0200
POSITIONAL bphs1-ch17-016 <-> R-ATEXTB-KET-1H-SAG-V-094-08 [positional_alternate_result] score=0.0210
POSITIONAL bphs1-ch17-016 <-> R-ATEXTB-KET-1H-SCO-V-094-09 [positional_alternate_result] score=0.0179
POSITIONAL bphs1-ch17-016 <-> R-ATEXTB-KET-1H-TAU-V-094-10 [positional_alternate_result] score=0.0224
POSITIONAL bphs1-ch17-016 <-> R-ATEXTB-KET-1H-V-094 [positional_alternate_result] score=0.0220
POSITIONAL bphs1-ch17-016 <-> R-ATEXTB-KET-1H-VIR-V-094-11 [positional_alternate_result] score=0.0162
POSITIONAL bphs1-ch17-016 <-> R-TBA15-1298 [positional_alternate_result] score=0.0220
POSITIONAL bphs1-ch17-016 <-> R-TBA15-1299 [positional_alternate_result] score=0.0471
POSITIONAL bphs1-ch17-016 <-> R-TBA15-1300 [positional_alternate_result] score=0.0520
POSITIONAL bphs1-ch17-016 <-> R-TBA15-1301 [positional_alternate_result] score=0.0496
POSITIONAL bphs1-ch17-016 <-> R-TBA15-1302 [positional_alternate_result] score=0.0520
POSITIONAL bphs1-ch17-016 <-> R-TBA15-1303 [positional_alternate_result] score=0.0456
POSITIONAL bphs1-ch17-016 <-> R-TBA15-1304 [positional_alternate_result] score=0.0585
POSITIONAL bphs1-ch17-016 <-> R-TBA15-1305 [positional_alternate_result] score=0.0463
POSITIONAL bphs1-ch17-016 <-> R-TBA15-1306 [positional_alternate_result] score=0.0296
POSITIONAL bphs1-ch17-016 <-> R-TBA15-1307 [positional_alternate_result] score=0.0439
POSITIONAL bphs1-ch17-016 <-> pd-ch02-014 [positional_alternate_result] score=0.0624
POSITIONAL bphs1-ch17-016 <-> pd-ch02-015 [positional_alternate_result] score=0.0567
POSITIONAL bphs1-ch17-016 <-> pd-ch02-016 [positional_alternate_result] score=0.0539
POSITIONAL bphs1-ch17-016 <-> pd-ch02-017 [positional_alternate_result] score=0.0711
POSITIONAL bphs1-ch17-016 <-> pd-ch08-099 [positional_alternate_result] score=0.0338
POSITIONAL bphs1-ch42-003 <-> R-ATEXTB-KET-1H-AQU-V-094-01 [positional_alternate_result] score=0.0627
POSITIONAL bphs1-ch42-003 <-> R-ATEXTB-KET-1H-ARI-V-094-02 [positional_alternate_result] score=0.0445
POSITIONAL bphs1-ch42-003 <-> R-ATEXTB-KET-1H-CAN-V-094-03 [positional_alternate_result] score=0.0564
POSITIONAL bphs1-ch42-003 <-> R-ATEXTB-KET-1H-CAP-V-094-04 [positional_alternate_result] score=0.0447
POSITIONAL bphs1-ch42-003 <-> R-ATEXTB-KET-1H-GEM-V-094-05 [positional_alternate_result] score=0.0220
POSITIONAL bphs1-ch42-003 <-> R-ATEXTB-KET-1H-LEO-V-094-06 [positional_alternate_result] score=0.0371
POSITIONAL bphs1-ch42-003 <-> R-ATEXTB-KET-1H-OWN-V-094-12 [positional_alternate_result] score=0.0484
POSITIONAL bphs1-ch42-003 <-> R-ATEXTB-KET-1H-PIS-V-094-07 [positional_alternate_result] score=0.0362
POSITIONAL bphs1-ch42-003 <-> R-ATEXTB-KET-1H-SAG-V-094-08 [positional_alternate_result] score=0.0255
POSITIONAL bphs1-ch42-003 <-> R-ATEXTB-KET-1H-SCO-V-094-09 [positional_alternate_result] score=0.0241
POSITIONAL bphs1-ch42-003 <-> R-ATEXTB-KET-1H-TAU-V-094-10 [positional_alternate_result] score=0.0441
POSITIONAL bphs1-ch42-003 <-> R-ATEXTB-KET-1H-V-094 [positional_alternate_result] score=0.0149
POSITIONAL bphs1-ch42-003 <-> R-ATEXTB-KET-1H-VIR-V-094-11 [positional_alternate_result] score=0.0207
POSITIONAL bphs1-ch42-003 <-> R-TBA15-1298 [positional_alternate_result] score=0.0433
POSITIONAL bphs1-ch42-003 <-> R-TBA15-1299 [positional_alternate_result] score=0.0926
POSITIONAL bphs1-ch42-003 <-> R-TBA15-1300 [positional_alternate_result] score=0.1021
POSITIONAL bphs1-ch42-003 <-> R-TBA15-1301 [positional_alternate_result] score=0.0975
POSITIONAL bphs1-ch42-003 <-> R-TBA15-1302 [positional_alternate_result] score=0.1022
POSITIONAL bphs1-ch42-003 <-> R-TBA15-1303 [positional_alternate_result] score=0.0895
POSITIONAL bphs1-ch42-003 <-> R-TBA15-1304 [positional_alternate_result] score=0.1063
POSITIONAL bphs1-ch42-003 <-> R-TBA15-1305 [positional_alternate_result] score=0.0842
POSITIONAL bphs1-ch42-003 <-> R-TBA15-1306 [positional_alternate_result] score=0.0557
POSITIONAL bphs1-ch42-003 <-> R-TBA15-1307 [positional_alternate_result] score=0.0798
POSITIONAL bphs1-ch42-003 <-> pd-ch02-014 [positional_alternate_result] score=0.0701
POSITIONAL bphs1-ch42-003 <-> pd-ch02-015 [positional_alternate_result] score=0.0758
POSITIONAL bphs1-ch42-003 <-> pd-ch02-016 [positional_alternate_result] score=0.0520
POSITIONAL bphs1-ch42-003 <-> pd-ch02-017 [positional_alternate_result] score=0.0696
POSITIONAL bphs1-ch42-003 <-> pd-ch08-099 [positional_alternate_result] score=0.0287
POSITIONAL bphs1-ch32-044 <-> R-TBA15-1416 [positional_alternate_result] score=0.0469
POSITIONAL bphs1-ch32-044 <-> R-TBA15-1417 [positional_alternate_result] score=0.1563
POSITIONAL bphs1-ch32-044 <-> R-TBA15-1418 [positional_alternate_result] score=0.1567
POSITIONAL bphs1-ch32-044 <-> R-TBA15-1419 [positional_alternate_result] score=0.1395
POSITIONAL bphs1-ch32-044 <-> R-TBA15-1420 [positional_alternate_result] score=0.1406
POSITIONAL bphs1-ch32-044 <-> R-TBA15-1421 [positional_alternate_result] score=0.1147
POSITIONAL bphs1-ch32-044 <-> R-TBA15-1422 [positional_alternate_result] score=0.0882
POSITIONAL bphs1-ch32-044 <-> pd-ch08-110 [positional_alternate_result] score=0.0997
POSITIONAL bphs1-ch17-010 <-> R-ATEXTB-MAR-1H-ARI-V-024-01 [positional_alternate_result] score=0.0267
POSITIONAL bphs1-ch17-010 <-> R-ATEXTB-MAR-1H-CAN-V-024-02 [positional_alternate_result] score=0.0138
POSITIONAL bphs1-ch17-010 <-> R-ATEXTB-MAR-1H-CAP-V-024-03 [positional_alternate_result] score=0.0260
POSITIONAL bphs1-ch17-010 <-> R-ATEXTB-MAR-1H-DEB-V-024-08 [positional_alternate_result] score=0.0196
POSITIONAL bphs1-ch17-010 <-> R-ATEXTB-MAR-1H-LIB-V-024-04 [positional_alternate_result] score=0.0168
POSITIONAL bphs1-ch17-010 <-> R-ATEXTB-MAR-1H-OWN-V-024-09 [positional_alternate_result] score=0.0196
POSITIONAL bphs1-ch17-010 <-> R-ATEXTB-MAR-1H-PIS-V-024-05 [positional_alternate_result] score=0.0138
POSITIONAL bphs1-ch17-010 <-> R-ATEXTB-MAR-1H-SCO-V-024-06 [positional_alternate_result] score=0.0208
POSITIONAL bphs1-ch17-010 <-> R-ATEXTB-MAR-1H-TAU-V-024-07 [positional_alternate_result] score=0.0182
POSITIONAL bphs1-ch17-010 <-> R-ATEXTB-MAR-1H-V-024 [positional_alternate_result] score=0.0528
POSITIONAL bphs1-ch17-010 <-> R-TBA15-379 [positional_alternate_result] score=0.0406
POSITIONAL bphs1-ch17-010 <-> R-TBA15-380 [positional_alternate_result] score=0.0332
POSITIONAL bphs1-ch17-010 <-> R-TBA15-381 [positional_alternate_result] score=0.0204
POSITIONAL bphs1-ch17-010 <-> R-TBA15-382 [positional_alternate_result] score=0.0481
POSITIONAL bphs1-ch17-010 <-> R-TBA15-383 [positional_alternate_result] score=0.0479
POSITIONAL bphs1-ch17-010 <-> R-TBA15-384 [positional_alternate_result] score=0.0481
POSITIONAL bphs1-ch17-010 <-> R-TBA15-385 [positional_alternate_result] score=0.0472
POSITIONAL bphs1-ch17-010 <-> R-TBA15-386 [positional_alternate_result] score=0.0481
POSITIONAL bphs1-ch17-010 <-> R-TBA15-387 [positional_alternate_result] score=0.0482
POSITIONAL bphs1-ch17-010 <-> R-TBA15-388 [positional_alternate_result] score=0.0371
POSITIONAL bphs1-ch17-010 <-> R-TBA15-389 [positional_alternate_result] score=0.0407
POSITIONAL bphs1-ch17-010 <-> R-TBA15-390 [positional_alternate_result] score=0.0387
POSITIONAL bphs1-ch17-010 <-> R-TBA15-391 [positional_alternate_result] score=0.0586
POSITIONAL bphs1-ch17-010 <-> R-TBA15-392 [positional_alternate_result] score=0.0484
POSITIONAL bphs1-ch17-010 <-> R-TBA15-393 [positional_alternate_result] score=0.0336
POSITIONAL bphs1-ch17-010 <-> R-TBA15-394 [positional_alternate_result] score=0.0401
POSITIONAL bphs1-ch17-010 <-> R-TBA15-395 [positional_alternate_result] score=0.0399
POSITIONAL bphs1-ch17-010 <-> R-TBA15-396 [positional_alternate_result] score=0.0377
POSITIONAL bphs1-ch17-010 <-> R-TBA15-397 [positional_alternate_result] score=0.0455
POSITIONAL bphs1-ch17-010 <-> R-TBA15-398 [positional_alternate_result] score=0.0456
POSITIONAL bphs1-ch17-010 <-> R-TBA15-399 [positional_alternate_result] score=0.0423
POSITIONAL bphs1-ch17-010 <-> R-TBA15-400 [positional_alternate_result] score=0.0253
POSITIONAL bphs1-ch17-010 <-> R-TBA15-401 [positional_alternate_result] score=0.0473
POSITIONAL bphs1-ch17-010 <-> R-TBA15-402 [positional_alternate_result] score=0.0510
POSITIONAL bphs1-ch17-010 <-> R-TBA15-403 [positional_alternate_result] score=0.0548
POSITIONAL bphs1-ch17-010 <-> R-TBA15-404 [positional_alternate_result] score=0.0563
POSITIONAL bphs1-ch17-010 <-> R-TBA15-405 [positional_alternate_result] score=0.0410
POSITIONAL bphs1-ch17-010 <-> R-TBA15-406 [positional_alternate_result] score=0.0319
POSITIONAL bphs1-ch17-010 <-> R-TBA15-407 [positional_alternate_result] score=0.0515
POSITIONAL bphs1-ch17-010 <-> R-TBA15-408 [positional_alternate_result] score=0.0515
POSITIONAL bphs1-ch17-010 <-> R-TBA15-409 [positional_alternate_result] score=0.0512
POSITIONAL bphs1-ch17-010 <-> R-TBA15-410 [positional_alternate_result] score=0.0444
POSITIONAL bphs1-ch17-010 <-> pd-ch08-026 [positional_alternate_result] score=0.0649
POSITIONAL bphs1-ch42-015 <-> R-ATEXTB-MAR-2H-DEB-V-025-03 [positional_alternate_result] score=0.0511
POSITIONAL bphs1-ch42-015 <-> R-ATEXTB-MAR-2H-ENE-V-025-04 [positional_alternate_result] score=0.0370
POSITIONAL bphs1-ch42-015 <-> R-ATEXTB-MAR-2H-EXA-V-025-05 [positional_alternate_result] score=0.0322
POSITIONAL bphs1-ch42-015 <-> R-ATEXTB-MAR-2H-OWN-V-025-06 [positional_alternate_result] score=0.0322
POSITIONAL bphs1-ch42-015 <-> R-ATEXTB-MAR-2H-SCO-V-025-01 [positional_alternate_result] score=0.0366
POSITIONAL bphs1-ch42-015 <-> R-ATEXTB-MAR-2H-V-025 [positional_alternate_result] score=0.0110
POSITIONAL bphs1-ch42-015 <-> R-ATEXTB-MAR-2H-VIR-V-025-02 [positional_alternate_result] score=0.0481
POSITIONAL bphs1-ch42-015 <-> R-TBA15-411 [positional_alternate_result] score=0.0163
POSITIONAL bphs1-ch42-015 <-> R-TBA15-412 [positional_alternate_result] score=0.0825
POSITIONAL bphs1-ch42-015 <-> R-TBA15-413 [positional_alternate_result] score=0.0623
POSITIONAL bphs1-ch42-015 <-> R-TBA15-414 [positional_alternate_result] score=0.0620
POSITIONAL bphs1-ch42-015 <-> R-TBA15-415 [positional_alternate_result] score=0.0714
POSITIONAL bphs1-ch42-015 <-> R-TBA15-416 [positional_alternate_result] score=0.0767
POSITIONAL bphs1-ch42-015 <-> R-TBA15-417 [positional_alternate_result] score=0.0754
POSITIONAL bphs1-ch42-015 <-> R-TBA15-418 [positional_alternate_result] score=0.0715
POSITIONAL bphs1-ch42-015 <-> R-TBA15-419 [positional_alternate_result] score=0.0841
POSITIONAL bphs1-ch42-015 <-> R-TBA15-420 [positional_alternate_result] score=0.0705
POSITIONAL bphs1-ch42-015 <-> R-TBA15-421 [positional_alternate_result] score=0.0275
POSITIONAL bphs1-ch42-015 <-> lalkitab-ch25-mars-h2 [positional_alternate_result] score=0.0383
POSITIONAL bphs1-ch42-015 <-> pd-ch08-027 [positional_alternate_result] score=0.0384
POSITIONAL bphs1-ch14-017 <-> R-ATEXTB-MAR-3H-ARI-V-026-01 [positional_alternate_result] score=0.0140
POSITIONAL bphs1-ch14-017 <-> R-ATEXTB-MAR-3H-EXA-V-026-03 [positional_alternate_result] score=0.0362
POSITIONAL bphs1-ch14-017 <-> R-ATEXTB-MAR-3H-GEM-V-026-02 [positional_alternate_result] score=0.0275
POSITIONAL bphs1-ch14-017 <-> R-ATEXTB-MAR-3H-OWN-V-026-04 [positional_alternate_result] score=0.0237
POSITIONAL bphs1-ch14-017 <-> R-ATEXTB-MAR-3H-V-026 [positional_alternate_result] score=0.0276
POSITIONAL bphs1-ch14-017 <-> R-BRIHAT-MAR-3H-066 [positional_alternate_result] score=0.0476
POSITIONAL bphs1-ch14-017 <-> R-TBA15-422 [positional_alternate_result] score=0.0253
POSITIONAL bphs1-ch14-017 <-> R-TBA15-423 [positional_alternate_result] score=0.0711
POSITIONAL bphs1-ch14-017 <-> R-TBA15-424 [positional_alternate_result] score=0.0594
POSITIONAL bphs1-ch14-017 <-> R-TBA15-425 [positional_alternate_result] score=0.0579
POSITIONAL bphs1-ch14-017 <-> R-TBA15-426 [positional_alternate_result] score=0.0689
POSITIONAL bphs1-ch14-017 <-> R-TBA15-427 [positional_alternate_result] score=0.0493
POSITIONAL bphs1-ch14-017 <-> R-TBA15-428 [positional_alternate_result] score=0.0509
POSITIONAL bphs1-ch14-017 <-> R-TBA15-429 [positional_alternate_result] score=0.0503
POSITIONAL bphs1-ch14-017 <-> R-TBA15-430 [positional_alternate_result] score=0.0603
POSITIONAL bphs1-ch14-017 <-> R-TBA15-431 [positional_alternate_result] score=0.0436
POSITIONAL bphs1-ch14-017 <-> R-TBA15-432 [positional_alternate_result] score=0.0726
POSITIONAL bphs1-ch14-017 <-> R-TBA15-433 [positional_alternate_result] score=0.0186
POSITIONAL bphs1-ch14-017 <-> lalkitab-ch27-wave-w04 [positional_alternate_result] score=0.0285
POSITIONAL bphs1-ch14-017 <-> lalkitab-ch27-wave-w22 [positional_alternate_result] score=0.0329
POSITIONAL bphs1-ch14-017 <-> lalkitab-ch27-wave-w34 [positional_alternate_result] score=0.0491
POSITIONAL bphs1-ch14-017 <-> lalkitab-ch27-wave-w46 [positional_alternate_result] score=0.0312
POSITIONAL bphs1-ch14-017 <-> pd-ch08-028 [positional_alternate_result] score=0.0967
POSITIONAL bphs1-ch14-017 <-> tba15-mars-h03-female-201 [positional_alternate_result] score=0.0361
POSITIONAL bphs1-ch14-017 <-> tba15-mars-h03-female-202 [positional_alternate_result] score=0.0361
POSITIONAL bphs1-ch14-017 <-> tba15-mars-h03-female-203 [positional_alternate_result] score=0.0361
POSITIONAL bphs1-ch14-017 <-> tba15-mars-h03-neutral-101 [positional_alternate_result] score=0.0361
POSITIONAL bphs1-ch14-017 <-> tba15-mars-h03-neutral-102 [positional_alternate_result] score=0.0265
POSITIONAL bphs1-ch14-017 <-> tba15-mars-h03-neutral-103 [positional_alternate_result] score=0.0361
POSITIONAL bphs1-ch32-021 <-> R-ATEXTB-MAR-3H-ARI-V-026-01 [positional_alternate_result] score=0.0142
POSITIONAL bphs1-ch32-021 <-> R-ATEXTB-MAR-3H-EXA-V-026-03 [positional_alternate_result] score=0.0422
POSITIONAL bphs1-ch32-021 <-> R-ATEXTB-MAR-3H-GEM-V-026-02 [positional_alternate_result] score=0.0548
POSITIONAL bphs1-ch32-021 <-> R-ATEXTB-MAR-3H-OWN-V-026-04 [positional_alternate_result] score=0.0260
POSITIONAL bphs1-ch32-021 <-> R-ATEXTB-MAR-3H-V-026 [positional_alternate_result] score=0.0204
POSITIONAL bphs1-ch32-021 <-> R-BRIHAT-MAR-3H-066 [positional_alternate_result] score=0.0345
POSITIONAL bphs1-ch32-021 <-> R-TBA15-422 [positional_alternate_result] score=0.0274
POSITIONAL bphs1-ch32-021 <-> R-TBA15-423 [positional_alternate_result] score=0.0943
POSITIONAL bphs1-ch32-021 <-> R-TBA15-424 [positional_alternate_result] score=0.0771
POSITIONAL bphs1-ch32-021 <-> R-TBA15-425 [positional_alternate_result] score=0.0745
POSITIONAL bphs1-ch32-021 <-> R-TBA15-426 [positional_alternate_result] score=0.1111
POSITIONAL bphs1-ch32-021 <-> R-TBA15-427 [positional_alternate_result] score=0.0654
POSITIONAL bphs1-ch32-021 <-> R-TBA15-428 [positional_alternate_result] score=0.0640
POSITIONAL bphs1-ch32-021 <-> R-TBA15-429 [positional_alternate_result] score=0.0598
POSITIONAL bphs1-ch32-021 <-> R-TBA15-430 [positional_alternate_result] score=0.0800
POSITIONAL bphs1-ch32-021 <-> R-TBA15-431 [positional_alternate_result] score=0.0475
POSITIONAL bphs1-ch32-021 <-> R-TBA15-432 [positional_alternate_result] score=0.0933
POSITIONAL bphs1-ch32-021 <-> R-TBA15-433 [positional_alternate_result] score=0.0226
POSITIONAL bphs1-ch32-021 <-> lalkitab-ch27-wave-w04 [positional_alternate_result] score=0.0201
POSITIONAL bphs1-ch32-021 <-> lalkitab-ch27-wave-w22 [positional_alternate_result] score=0.0213
POSITIONAL bphs1-ch32-021 <-> lalkitab-ch27-wave-w34 [positional_alternate_result] score=0.0239
POSITIONAL bphs1-ch32-021 <-> lalkitab-ch27-wave-w46 [positional_alternate_result] score=0.0263
POSITIONAL bphs1-ch32-021 <-> pd-ch08-028 [positional_alternate_result] score=0.1091
POSITIONAL bphs1-ch32-021 <-> tba15-mars-h03-female-201 [positional_alternate_result] score=0.0449
POSITIONAL bphs1-ch32-021 <-> tba15-mars-h03-female-202 [positional_alternate_result] score=0.0449
POSITIONAL bphs1-ch32-021 <-> tba15-mars-h03-female-203 [positional_alternate_result] score=0.0449
POSITIONAL bphs1-ch32-021 <-> tba15-mars-h03-neutral-101 [positional_alternate_result] score=0.0449
POSITIONAL bphs1-ch32-021 <-> tba15-mars-h03-neutral-102 [positional_alternate_result] score=0.0330
POSITIONAL bphs1-ch32-021 <-> tba15-mars-h03-neutral-103 [positional_alternate_result] score=0.0449
POSITIONAL bphs1-ch32-034 <-> R-ATEXTB-MAR-3H-ARI-V-026-01 [positional_alternate_result] score=0.0144
POSITIONAL bphs1-ch32-034 <-> R-ATEXTB-MAR-3H-EXA-V-026-03 [positional_alternate_result] score=0.0423
POSITIONAL bphs1-ch32-034 <-> R-ATEXTB-MAR-3H-GEM-V-026-02 [positional_alternate_result] score=0.0299
POSITIONAL bphs1-ch32-034 <-> R-ATEXTB-MAR-3H-OWN-V-026-04 [positional_alternate_result] score=0.0284
POSITIONAL bphs1-ch32-034 <-> R-ATEXTB-MAR-3H-V-026 [positional_alternate_result] score=0.0991
POSITIONAL bphs1-ch32-034 <-> R-BRIHAT-MAR-3H-066 [positional_alternate_result] score=0.1284
POSITIONAL bphs1-ch32-034 <-> R-TBA15-422 [positional_alternate_result] score=0.1235
POSITIONAL bphs1-ch32-034 <-> R-TBA15-423 [positional_alternate_result] score=0.0454
POSITIONAL bphs1-ch32-034 <-> R-TBA15-424 [positional_alternate_result] score=0.0355
POSITIONAL bphs1-ch32-034 <-> R-TBA15-425 [positional_alternate_result] score=0.0359
POSITIONAL bphs1-ch32-034 <-> R-TBA15-426 [positional_alternate_result] score=0.0473
POSITIONAL bphs1-ch32-034 <-> R-TBA15-427 [positional_alternate_result] score=0.0848
POSITIONAL bphs1-ch32-034 <-> R-TBA15-428 [positional_alternate_result] score=0.0295
POSITIONAL bphs1-ch32-034 <-> R-TBA15-429 [positional_alternate_result] score=0.0446
POSITIONAL bphs1-ch32-034 <-> R-TBA15-430 [positional_alternate_result] score=0.0385
POSITIONAL bphs1-ch32-034 <-> R-TBA15-431 [positional_alternate_result] score=0.0204
POSITIONAL bphs1-ch32-034 <-> R-TBA15-432 [positional_alternate_result] score=0.0413
POSITIONAL bphs1-ch32-034 <-> R-TBA15-433 [positional_alternate_result] score=0.0268
POSITIONAL bphs1-ch32-034 <-> lalkitab-ch27-wave-w04 [positional_alternate_result] score=0.0230
POSITIONAL bphs1-ch32-034 <-> lalkitab-ch27-wave-w22 [positional_alternate_result] score=0.0198
POSITIONAL bphs1-ch32-034 <-> lalkitab-ch27-wave-w34 [positional_alternate_result] score=0.0322
POSITIONAL bphs1-ch32-034 <-> lalkitab-ch27-wave-w46 [positional_alternate_result] score=0.0248
POSITIONAL bphs1-ch32-034 <-> pd-ch08-028 [positional_alternate_result] score=0.1236
POSITIONAL bphs1-ch32-034 <-> tba15-mars-h03-female-201 [positional_alternate_result] score=0.0417
POSITIONAL bphs1-ch32-034 <-> tba15-mars-h03-female-202 [positional_alternate_result] score=0.0417
POSITIONAL bphs1-ch32-034 <-> tba15-mars-h03-female-203 [positional_alternate_result] score=0.0417
POSITIONAL bphs1-ch32-034 <-> tba15-mars-h03-neutral-101 [positional_alternate_result] score=0.0417
POSITIONAL bphs1-ch32-034 <-> tba15-mars-h03-neutral-102 [positional_alternate_result] score=0.0306
POSITIONAL bphs1-ch32-034 <-> tba15-mars-h03-neutral-103 [positional_alternate_result] score=0.0417
POSITIONAL bphs1-ch17-019 <-> R-ATEXTB-MAR-6H-AQU-V-029-01 [positional_alternate_result] score=0.0242
POSITIONAL bphs1-ch17-019 <-> R-ATEXTB-MAR-6H-ARI-V-029-02 [positional_alternate_result] score=0.0233
POSITIONAL bphs1-ch17-019 <-> R-ATEXTB-MAR-6H-CAN-V-029-03 [positional_alternate_result] score=0.0212
POSITIONAL bphs1-ch17-019 <-> R-ATEXTB-MAR-6H-CAP-V-029-04 [positional_alternate_result] score=0.0214
POSITIONAL bphs1-ch17-019 <-> R-ATEXTB-MAR-6H-DEB-V-029-11 [positional_alternate_result] score=0.0201
POSITIONAL bphs1-ch17-019 <-> R-ATEXTB-MAR-6H-EXA-V-029-12 [positional_alternate_result] score=0.1709
POSITIONAL bphs1-ch17-019 <-> R-ATEXTB-MAR-6H-GEM-V-029-05 [positional_alternate_result] score=0.0233
POSITIONAL bphs1-ch17-019 <-> R-ATEXTB-MAR-6H-LEO-V-029-06 [positional_alternate_result] score=0.0243
POSITIONAL bphs1-ch17-019 <-> R-ATEXTB-MAR-6H-PIS-V-029-07 [positional_alternate_result] score=0.0219
POSITIONAL bphs1-ch17-019 <-> R-ATEXTB-MAR-6H-SCO-V-029-08 [positional_alternate_result] score=0.0245
POSITIONAL bphs1-ch17-019 <-> R-ATEXTB-MAR-6H-TAU-V-029-09 [positional_alternate_result] score=0.0242
POSITIONAL bphs1-ch17-019 <-> R-ATEXTB-MAR-6H-V-029 [positional_alternate_result] score=0.1392
POSITIONAL bphs1-ch17-019 <-> R-ATEXTB-MAR-6H-VIR-V-029-10 [positional_alternate_result] score=0.0234
POSITIONAL bphs1-ch17-019 <-> R-TBA15-471 [positional_alternate_result] score=0.1677
POSITIONAL bphs1-ch17-019 <-> R-TBA15-472 [positional_alternate_result] score=0.0245
POSITIONAL bphs1-ch17-019 <-> R-TBA15-473 [positional_alternate_result] score=0.1763
POSITIONAL bphs1-ch17-019 <-> R-TBA15-474 [positional_alternate_result] score=0.0203
POSITIONAL bphs1-ch17-019 <-> R-TBA15-475 [positional_alternate_result] score=0.0276
POSITIONAL bphs1-ch17-019 <-> R-TBA15-476 [positional_alternate_result] score=0.0277
POSITIONAL bphs1-ch17-019 <-> R-TBA15-477 [positional_alternate_result] score=0.0253
POSITIONAL bphs1-ch17-019 <-> R-TBA15-478 [positional_alternate_result] score=0.0297
POSITIONAL bphs1-ch17-019 <-> R-TBA15-479 [positional_alternate_result] score=0.0294
POSITIONAL bphs1-ch17-019 <-> R-TBA15-480 [positional_alternate_result] score=0.0298
POSITIONAL bphs1-ch17-019 <-> R-TBA15-481 [positional_alternate_result] score=0.0294
POSITIONAL bphs1-ch17-019 <-> R-TBA15-482 [positional_alternate_result] score=0.0261
POSITIONAL bphs1-ch17-019 <-> R-TBA15-483 [positional_alternate_result] score=0.0262
POSITIONAL bphs1-ch17-019 <-> R-TBA15-484 [positional_alternate_result] score=0.0262
POSITIONAL bphs1-ch17-019 <-> R-TBA15-485 [positional_alternate_result] score=0.0259
POSITIONAL bphs1-ch17-019 <-> R-TBA15-486 [positional_alternate_result] score=0.0235
POSITIONAL bphs1-ch17-019 <-> R-TBA15-487 [positional_alternate_result] score=0.0251
POSITIONAL bphs1-ch17-019 <-> R-TBA15-488 [positional_alternate_result] score=0.0249
POSITIONAL bphs1-ch17-019 <-> R-TBA15-489 [positional_alternate_result] score=0.0236
POSITIONAL bphs1-ch17-019 <-> R-TBA15-490 [positional_alternate_result] score=0.0341
POSITIONAL bphs1-ch17-019 <-> R-TBA15-491 [positional_alternate_result] score=0.0681
POSITIONAL bphs1-ch17-019 <-> R-TBA15-492 [positional_alternate_result] score=0.0819
POSITIONAL bphs1-ch17-019 <-> pd-ch08-031 [positional_polarity_conflict] score=0.0924
POSITIONAL bphs1-ch18-049 <-> R-ATEXTB-MAR-6H-AQU-V-029-01 [positional_alternate_result] score=0.0180
POSITIONAL bphs1-ch18-049 <-> R-ATEXTB-MAR-6H-ARI-V-029-02 [positional_alternate_result] score=0.0114
POSITIONAL bphs1-ch18-049 <-> R-ATEXTB-MAR-6H-CAN-V-029-03 [positional_alternate_result] score=0.0118
POSITIONAL bphs1-ch18-049 <-> R-ATEXTB-MAR-6H-CAP-V-029-04 [positional_alternate_result] score=0.0104
POSITIONAL bphs1-ch18-049 <-> R-ATEXTB-MAR-6H-DEB-V-029-11 [positional_alternate_result] score=0.0220
POSITIONAL bphs1-ch18-049 <-> R-ATEXTB-MAR-6H-EXA-V-029-12 [positional_alternate_result] score=0.0250
POSITIONAL bphs1-ch18-049 <-> R-ATEXTB-MAR-6H-GEM-V-029-05 [positional_alternate_result] score=0.0238
POSITIONAL bphs1-ch18-049 <-> R-ATEXTB-MAR-6H-LEO-V-029-06 [positional_alternate_result] score=0.0180
POSITIONAL bphs1-ch18-049 <-> R-ATEXTB-MAR-6H-PIS-V-029-07 [positional_alternate_result] score=0.0138
POSITIONAL bphs1-ch18-049 <-> R-ATEXTB-MAR-6H-SCO-V-029-08 [positional_alternate_result] score=0.0182
POSITIONAL bphs1-ch18-049 <-> R-ATEXTB-MAR-6H-TAU-V-029-09 [positional_alternate_result] score=0.0180
POSITIONAL bphs1-ch18-049 <-> R-ATEXTB-MAR-6H-V-029 [positional_alternate_result] score=0.0405
POSITIONAL bphs1-ch18-049 <-> R-ATEXTB-MAR-6H-VIR-V-029-10 [positional_alternate_result] score=0.0239
POSITIONAL bphs1-ch18-049 <-> R-TBA15-471 [positional_alternate_result] score=0.0452
POSITIONAL bphs1-ch18-049 <-> R-TBA15-472 [positional_alternate_result] score=0.0346
POSITIONAL bphs1-ch18-049 <-> R-TBA15-473 [positional_alternate_result] score=0.0278
POSITIONAL bphs1-ch18-049 <-> R-TBA15-474 [positional_alternate_result] score=0.0236
POSITIONAL bphs1-ch18-049 <-> R-TBA15-475 [positional_alternate_result] score=0.0303
POSITIONAL bphs1-ch18-049 <-> R-TBA15-476 [positional_alternate_result] score=0.0304
POSITIONAL bphs1-ch18-049 <-> R-TBA15-477 [positional_alternate_result] score=0.0277
POSITIONAL bphs1-ch18-049 <-> R-TBA15-478 [positional_alternate_result] score=0.0239
POSITIONAL bphs1-ch18-049 <-> R-TBA15-479 [positional_alternate_result] score=0.0236
POSITIONAL bphs1-ch18-049 <-> R-TBA15-480 [positional_alternate_result] score=0.0239
POSITIONAL bphs1-ch18-049 <-> R-TBA15-481 [positional_alternate_result] score=0.0237
POSITIONAL bphs1-ch18-049 <-> R-TBA15-482 [positional_alternate_result] score=0.0210
POSITIONAL bphs1-ch18-049 <-> R-TBA15-483 [positional_alternate_result] score=0.0146
POSITIONAL bphs1-ch18-049 <-> R-TBA15-484 [positional_alternate_result] score=0.0146
POSITIONAL bphs1-ch18-049 <-> R-TBA15-485 [positional_alternate_result] score=0.0145
POSITIONAL bphs1-ch18-049 <-> R-TBA15-486 [positional_alternate_result] score=0.0131
POSITIONAL bphs1-ch18-049 <-> R-TBA15-487 [positional_alternate_result] score=0.0177
POSITIONAL bphs1-ch18-049 <-> R-TBA15-488 [positional_alternate_result] score=0.0175
POSITIONAL bphs1-ch18-049 <-> R-TBA15-489 [positional_alternate_result] score=0.0166
POSITIONAL bphs1-ch18-049 <-> R-TBA15-490 [positional_alternate_result] score=0.0214
POSITIONAL bphs1-ch18-049 <-> R-TBA15-491 [positional_alternate_result] score=0.0363
POSITIONAL bphs1-ch18-049 <-> R-TBA15-492 [positional_alternate_result] score=0.0253
POSITIONAL bphs1-ch18-049 <-> pd-ch08-031 [positional_polarity_conflict] score=0.0716
POSITIONAL bphs1-ch32-037 <-> R-ATEXTB-MAR-6H-AQU-V-029-01 [positional_alternate_result] score=0.0229
POSITIONAL bphs1-ch32-037 <-> R-ATEXTB-MAR-6H-ARI-V-029-02 [positional_alternate_result] score=0.0170
POSITIONAL bphs1-ch32-037 <-> R-ATEXTB-MAR-6H-CAN-V-029-03 [positional_alternate_result] score=0.0185
POSITIONAL bphs1-ch32-037 <-> R-ATEXTB-MAR-6H-CAP-V-029-04 [positional_alternate_result] score=0.0192
POSITIONAL bphs1-ch32-037 <-> R-ATEXTB-MAR-6H-DEB-V-029-11 [positional_alternate_result] score=0.0155
POSITIONAL bphs1-ch32-037 <-> R-ATEXTB-MAR-6H-EXA-V-029-12 [positional_alternate_result] score=0.0283
POSITIONAL bphs1-ch32-037 <-> R-ATEXTB-MAR-6H-GEM-V-029-05 [positional_alternate_result] score=0.0241
POSITIONAL bphs1-ch32-037 <-> R-ATEXTB-MAR-6H-LEO-V-029-06 [positional_alternate_result] score=0.0230
POSITIONAL bphs1-ch32-037 <-> R-ATEXTB-MAR-6H-PIS-V-029-07 [positional_alternate_result] score=0.0227
POSITIONAL bphs1-ch32-037 <-> R-ATEXTB-MAR-6H-SCO-V-029-08 [positional_alternate_result] score=0.0232
POSITIONAL bphs1-ch32-037 <-> R-ATEXTB-MAR-6H-TAU-V-029-09 [positional_alternate_result] score=0.0230
POSITIONAL bphs1-ch32-037 <-> R-ATEXTB-MAR-6H-V-029 [positional_alternate_result] score=0.0376
POSITIONAL bphs1-ch32-037 <-> R-ATEXTB-MAR-6H-VIR-V-029-10 [positional_alternate_result] score=0.0243
POSITIONAL bphs1-ch32-037 <-> R-TBA15-471 [positional_alternate_result] score=0.0368
POSITIONAL bphs1-ch32-037 <-> R-TBA15-472 [positional_alternate_result] score=0.0537
POSITIONAL bphs1-ch32-037 <-> R-TBA15-473 [positional_alternate_result] score=0.0550
POSITIONAL bphs1-ch32-037 <-> R-TBA15-474 [positional_alternate_result] score=0.0329
POSITIONAL bphs1-ch32-037 <-> R-TBA15-475 [positional_alternate_result] score=0.0531
POSITIONAL bphs1-ch32-037 <-> R-TBA15-476 [positional_alternate_result] score=0.0533
POSITIONAL bphs1-ch32-037 <-> R-TBA15-477 [positional_alternate_result] score=0.0486
POSITIONAL bphs1-ch32-037 <-> R-TBA15-478 [positional_alternate_result] score=0.0507
POSITIONAL bphs1-ch32-037 <-> R-TBA15-479 [positional_alternate_result] score=0.0501
POSITIONAL bphs1-ch32-037 <-> R-TBA15-480 [positional_alternate_result] score=0.0508
POSITIONAL bphs1-ch32-037 <-> R-TBA15-481 [positional_alternate_result] score=0.0502
POSITIONAL bphs1-ch32-037 <-> R-TBA15-482 [positional_alternate_result] score=0.0445
POSITIONAL bphs1-ch32-037 <-> R-TBA15-483 [positional_alternate_result] score=0.0469
POSITIONAL bphs1-ch32-037 <-> R-TBA15-484 [positional_alternate_result] score=0.0469
POSITIONAL bphs1-ch32-037 <-> R-TBA15-485 [positional_alternate_result] score=0.0463
POSITIONAL bphs1-ch32-037 <-> R-TBA15-486 [positional_alternate_result] score=0.0420
POSITIONAL bphs1-ch32-037 <-> R-TBA15-487 [positional_alternate_result] score=0.0483
POSITIONAL bphs1-ch32-037 <-> R-TBA15-488 [positional_alternate_result] score=0.0478
POSITIONAL bphs1-ch32-037 <-> R-TBA15-489 [positional_alternate_result] score=0.0453
POSITIONAL bphs1-ch32-037 <-> R-TBA15-490 [positional_alternate_result] score=0.0633
POSITIONAL bphs1-ch32-037 <-> R-TBA15-491 [positional_alternate_result] score=0.0662
POSITIONAL bphs1-ch32-037 <-> R-TBA15-492 [positional_alternate_result] score=0.0713
POSITIONAL bphs1-ch32-037 <-> pd-ch08-031 [positional_alternate_result] score=0.0844
POSITIONAL bphs1-ch18-010 <-> R-ATEXTB-MAR-7H-004 [positional_polarity_conflict] score=0.0594
POSITIONAL bphs1-ch18-010 <-> R-ATEXTB-MAR-7H-084 [positional_alternate_result] score=0.0480
POSITIONAL bphs1-ch18-010 <-> R-ATEXTB-MAR-7H-ARI-V-030-01 [positional_alternate_result] score=0.0436
POSITIONAL bphs1-ch18-010 <-> R-ATEXTB-MAR-7H-CAN-V-030-02 [positional_alternate_result] score=0.0221
POSITIONAL bphs1-ch18-010 <-> R-ATEXTB-MAR-7H-CAP-V-030-03 [positional_alternate_result] score=0.0221
POSITIONAL bphs1-ch18-010 <-> R-ATEXTB-MAR-7H-DEB-V-030-06 [positional_alternate_result] score=0.0207
POSITIONAL bphs1-ch18-010 <-> R-ATEXTB-MAR-7H-ENE-V-030-07 [positional_alternate_result] score=0.0225
POSITIONAL bphs1-ch18-010 <-> R-ATEXTB-MAR-7H-EXA-V-030-08 [positional_alternate_result] score=0.0145
POSITIONAL bphs1-ch18-010 <-> R-ATEXTB-MAR-7H-OWN-V-030-09 [positional_alternate_result] score=0.0173
POSITIONAL bphs1-ch18-010 <-> R-ATEXTB-MAR-7H-PIS-V-030-04 [positional_alternate_result] score=0.0178
POSITIONAL bphs1-ch18-010 <-> R-ATEXTB-MAR-7H-SCO-V-030-05 [positional_alternate_result] score=0.0435
POSITIONAL bphs1-ch18-010 <-> R-ATEXTB-MAR-7H-V-030 [positional_alternate_result] score=0.0768
POSITIONAL bphs1-ch18-010 <-> R-TBA15-493 [positional_alternate_result] score=0.0546
POSITIONAL bphs1-ch18-010 <-> R-TBA15-494 [positional_alternate_result] score=0.0466
POSITIONAL bphs1-ch18-010 <-> R-TBA15-495 [positional_alternate_result] score=0.1149
POSITIONAL bphs1-ch18-010 <-> R-TBA15-496 [positional_alternate_result] score=0.0410
POSITIONAL bphs1-ch18-010 <-> R-TBA15-497 [positional_alternate_result] score=0.0384
POSITIONAL bphs1-ch18-010 <-> R-TBA15-498 [positional_alternate_result] score=0.0512
POSITIONAL bphs1-ch18-010 <-> R-TBA15-499 [positional_alternate_result] score=0.0394
POSITIONAL bphs1-ch18-010 <-> R-TBA15-500 [positional_alternate_result] score=0.0325
POSITIONAL bphs1-ch18-010 <-> R-TBA15-501 [positional_alternate_result] score=0.0391
POSITIONAL bphs1-ch18-010 <-> R-TBA15-502 [positional_alternate_result] score=0.0424
POSITIONAL bphs1-ch18-010 <-> R-TBA15-503 [positional_alternate_result] score=0.0435
POSITIONAL bphs1-ch18-010 <-> R-TBA15-504 [positional_alternate_result] score=0.0435
POSITIONAL bphs1-ch18-010 <-> R-TBA15-505 [positional_alternate_result] score=0.0433
POSITIONAL bphs1-ch18-010 <-> R-TBA15-506 [positional_alternate_result] score=0.0449
POSITIONAL bphs1-ch18-010 <-> R-TBA15-507 [positional_alternate_result] score=0.0494
POSITIONAL bphs1-ch18-010 <-> R-TBA15-508 [positional_alternate_result] score=0.0414
POSITIONAL bphs1-ch18-010 <-> R-TBA15-509 [positional_alternate_result] score=0.0412
POSITIONAL bphs1-ch18-010 <-> R-TBA15-510 [positional_alternate_result] score=0.0442
POSITIONAL bphs1-ch18-010 <-> R-TBA15-511 [positional_alternate_result] score=0.0375
POSITIONAL bphs1-ch18-010 <-> R-TBA15-512 [positional_alternate_result] score=0.0483
POSITIONAL bphs1-ch18-010 <-> R-TBA15-513 [positional_alternate_result] score=0.0497
POSITIONAL bphs1-ch18-010 <-> R-TBA15-514 [positional_alternate_result] score=0.0404
POSITIONAL bphs1-ch18-010 <-> R-TBA15-515 [positional_alternate_result] score=0.0341
POSITIONAL bphs1-ch18-010 <-> R-TBA15-516 [positional_alternate_result] score=0.0513
POSITIONAL bphs1-ch18-010 <-> R-TBA15-517 [positional_alternate_result] score=0.0513
POSITIONAL bphs1-ch18-010 <-> R-TBA15-518 [positional_alternate_result] score=0.0539
POSITIONAL bphs1-ch18-010 <-> R-TBA15-519 [positional_alternate_result] score=0.0382
POSITIONAL bphs1-ch18-010 <-> pd-ch08-032 [positional_alternate_result] score=0.0611
POSITIONAL bphs1-ch18-014 <-> R-ATEXTB-MAR-7H-004 [positional_alternate_result] score=0.0651
POSITIONAL bphs1-ch18-014 <-> R-ATEXTB-MAR-7H-084 [positional_alternate_result] score=0.0421
POSITIONAL bphs1-ch18-014 <-> R-ATEXTB-MAR-7H-ARI-V-030-01 [positional_alternate_result] score=0.0565
POSITIONAL bphs1-ch18-014 <-> R-ATEXTB-MAR-7H-CAN-V-030-02 [positional_alternate_result] score=0.0394
POSITIONAL bphs1-ch18-014 <-> R-ATEXTB-MAR-7H-CAP-V-030-03 [positional_alternate_result] score=0.0232
POSITIONAL bphs1-ch18-014 <-> R-ATEXTB-MAR-7H-DEB-V-030-06 [positional_alternate_result] score=0.0189
POSITIONAL bphs1-ch18-014 <-> R-ATEXTB-MAR-7H-ENE-V-030-07 [positional_alternate_result] score=0.0236
POSITIONAL bphs1-ch18-014 <-> R-ATEXTB-MAR-7H-EXA-V-030-08 [positional_alternate_result] score=0.0144
POSITIONAL bphs1-ch18-014 <-> R-ATEXTB-MAR-7H-OWN-V-030-09 [positional_alternate_result] score=0.0172
POSITIONAL bphs1-ch18-014 <-> R-ATEXTB-MAR-7H-PIS-V-030-04 [positional_alternate_result] score=0.0232
POSITIONAL bphs1-ch18-014 <-> R-ATEXTB-MAR-7H-SCO-V-030-05 [positional_alternate_result] score=0.0563
POSITIONAL bphs1-ch18-014 <-> R-ATEXTB-MAR-7H-V-030 [positional_alternate_result] score=0.0591
POSITIONAL bphs1-ch18-014 <-> R-TBA15-493 [positional_alternate_result] score=0.0312
POSITIONAL bphs1-ch18-014 <-> R-TBA15-494 [positional_alternate_result] score=0.0711
POSITIONAL bphs1-ch18-014 <-> R-TBA15-495 [positional_alternate_result] score=0.0836
POSITIONAL bphs1-ch18-014 <-> R-TBA15-496 [positional_alternate_result] score=0.0609
POSITIONAL bphs1-ch18-014 <-> R-TBA15-497 [positional_alternate_result] score=0.0642
POSITIONAL bphs1-ch18-014 <-> R-TBA15-498 [positional_alternate_result] score=0.0780
POSITIONAL bphs1-ch18-014 <-> R-TBA15-499 [positional_alternate_result] score=0.0724
POSITIONAL bphs1-ch18-014 <-> R-TBA15-500 [positional_alternate_result] score=0.0467
POSITIONAL bphs1-ch18-014 <-> R-TBA15-501 [positional_alternate_result] score=0.0597
POSITIONAL bphs1-ch18-014 <-> R-TBA15-502 [positional_alternate_result] score=0.0626
POSITIONAL bphs1-ch18-014 <-> R-TBA15-503 [positional_alternate_result] score=0.0719
POSITIONAL bphs1-ch18-014 <-> R-TBA15-504 [positional_alternate_result] score=0.0720
POSITIONAL bphs1-ch18-014 <-> R-TBA15-505 [positional_alternate_result] score=0.0716
POSITIONAL bphs1-ch18-014 <-> R-TBA15-506 [positional_alternate_result] score=0.0663
POSITIONAL bphs1-ch18-014 <-> R-TBA15-507 [positional_alternate_result] score=0.0750
POSITIONAL bphs1-ch18-014 <-> R-TBA15-508 [positional_alternate_result] score=0.0627
POSITIONAL bphs1-ch18-014 <-> R-TBA15-509 [positional_alternate_result] score=0.0757
POSITIONAL bphs1-ch18-014 <-> R-TBA15-510 [positional_alternate_result] score=0.0731
POSITIONAL bphs1-ch18-014 <-> R-TBA15-511 [positional_alternate_result] score=0.0691
POSITIONAL bphs1-ch18-014 <-> R-TBA15-512 [positional_alternate_result] score=0.0733
POSITIONAL bphs1-ch18-014 <-> R-TBA15-513 [positional_alternate_result] score=0.0941
POSITIONAL bphs1-ch18-014 <-> R-TBA15-514 [positional_alternate_result] score=0.0463
POSITIONAL bphs1-ch18-014 <-> R-TBA15-515 [positional_alternate_result] score=0.0551
POSITIONAL bphs1-ch18-014 <-> R-TBA15-516 [positional_alternate_result] score=0.0719
POSITIONAL bphs1-ch18-014 <-> R-TBA15-517 [positional_alternate_result] score=0.0719
POSITIONAL bphs1-ch18-014 <-> R-TBA15-518 [positional_alternate_result] score=0.0705
POSITIONAL bphs1-ch18-014 <-> R-TBA15-519 [positional_alternate_result] score=0.0404
POSITIONAL bphs1-ch18-014 <-> pd-ch08-032 [positional_polarity_conflict] score=0.0806
POSITIONAL bphs1-ch18-027 <-> R-ATEXTB-MAR-7H-004 [positional_polarity_conflict] score=0.1255
POSITIONAL bphs1-ch18-027 <-> R-ATEXTB-MAR-7H-084 [positional_alternate_result] score=0.0526
POSITIONAL bphs1-ch18-027 <-> R-ATEXTB-MAR-7H-ARI-V-030-01 [positional_alternate_result] score=0.0831
POSITIONAL bphs1-ch18-027 <-> R-ATEXTB-MAR-7H-CAN-V-030-02 [positional_alternate_result] score=0.0248
POSITIONAL bphs1-ch18-027 <-> R-ATEXTB-MAR-7H-CAP-V-030-03 [positional_alternate_result] score=0.0425
POSITIONAL bphs1-ch18-027 <-> R-ATEXTB-MAR-7H-DEB-V-030-06 [positional_alternate_result] score=0.0194
POSITIONAL bphs1-ch18-027 <-> R-ATEXTB-MAR-7H-ENE-V-030-07 [positional_alternate_result] score=0.0233
POSITIONAL bphs1-ch18-027 <-> R-ATEXTB-MAR-7H-EXA-V-030-08 [positional_alternate_result] score=0.0291
POSITIONAL bphs1-ch18-027 <-> R-ATEXTB-MAR-7H-OWN-V-030-09 [positional_alternate_result] score=0.0319
POSITIONAL bphs1-ch18-027 <-> R-ATEXTB-MAR-7H-PIS-V-030-04 [positional_alternate_result] score=0.0262
POSITIONAL bphs1-ch18-027 <-> R-ATEXTB-MAR-7H-SCO-V-030-05 [positional_alternate_result] score=0.0830
POSITIONAL bphs1-ch18-027 <-> R-ATEXTB-MAR-7H-V-030 [positional_alternate_result] score=0.0600
POSITIONAL bphs1-ch18-027 <-> R-TBA15-493 [positional_alternate_result] score=0.0424
POSITIONAL bphs1-ch18-027 <-> R-TBA15-494 [positional_alternate_result] score=0.0790
POSITIONAL bphs1-ch18-027 <-> R-TBA15-495 [positional_alternate_result] score=0.0550
POSITIONAL bphs1-ch18-027 <-> R-TBA15-496 [positional_alternate_result] score=0.0721
POSITIONAL bphs1-ch18-027 <-> R-TBA15-497 [positional_alternate_result] score=0.0795
POSITIONAL bphs1-ch18-027 <-> R-TBA15-498 [positional_alternate_result] score=0.0867
POSITIONAL bphs1-ch18-027 <-> R-TBA15-499 [positional_alternate_result] score=0.0703
POSITIONAL bphs1-ch18-027 <-> R-TBA15-500 [positional_alternate_result] score=0.0692
POSITIONAL bphs1-ch18-027 <-> R-TBA15-501 [positional_alternate_result] score=0.0787
POSITIONAL bphs1-ch18-027 <-> R-TBA15-502 [positional_alternate_result] score=0.0735
POSITIONAL bphs1-ch18-027 <-> R-TBA15-503 [positional_alternate_result] score=0.1109
POSITIONAL bphs1-ch18-027 <-> R-TBA15-504 [positional_alternate_result] score=0.1109
POSITIONAL bphs1-ch18-027 <-> R-TBA15-505 [positional_alternate_result] score=0.1104
POSITIONAL bphs1-ch18-027 <-> R-TBA15-506 [positional_alternate_result] score=0.0978
POSITIONAL bphs1-ch18-027 <-> R-TBA15-507 [positional_alternate_result] score=0.1200
POSITIONAL bphs1-ch18-027 <-> R-TBA15-508 [positional_alternate_result] score=0.0693
POSITIONAL bphs1-ch18-027 <-> R-TBA15-509 [positional_alternate_result] score=0.0709
POSITIONAL bphs1-ch18-027 <-> R-TBA15-510 [positional_alternate_result] score=0.0898
POSITIONAL bphs1-ch18-027 <-> R-TBA15-511 [positional_alternate_result] score=0.0670
POSITIONAL bphs1-ch18-027 <-> R-TBA15-512 [positional_alternate_result] score=0.0939
POSITIONAL bphs1-ch18-027 <-> R-TBA15-513 [positional_alternate_result] score=0.0842
POSITIONAL bphs1-ch18-027 <-> R-TBA15-514 [positional_alternate_result] score=0.0590
POSITIONAL bphs1-ch18-027 <-> R-TBA15-515 [positional_alternate_result] score=0.0740
POSITIONAL bphs1-ch18-027 <-> R-TBA15-516 [positional_alternate_result] score=0.0857
POSITIONAL bphs1-ch18-027 <-> R-TBA15-517 [positional_alternate_result] score=0.0857
POSITIONAL bphs1-ch18-027 <-> R-TBA15-518 [positional_alternate_result] score=0.0814
POSITIONAL bphs1-ch18-027 <-> R-TBA15-519 [positional_alternate_result] score=0.0496
POSITIONAL bphs1-ch18-027 <-> pd-ch08-032 [positional_alternate_result] score=0.1276
POSITIONAL bphs1-ch15-005 <-> R-ATEXTB-MER-1H-AQU-V-036-01 [positional_alternate_result] score=0.0175
POSITIONAL bphs1-ch15-005 <-> R-ATEXTB-MER-1H-CAP-V-036-02 [positional_alternate_result] score=0.0145
POSITIONAL bphs1-ch15-005 <-> R-ATEXTB-MER-1H-EXA-V-036-07 [positional_alternate_result] score=0.0213
POSITIONAL bphs1-ch15-005 <-> R-ATEXTB-MER-1H-GEM-V-036-03 [positional_alternate_result] score=0.0178
POSITIONAL bphs1-ch15-005 <-> R-ATEXTB-MER-1H-LIB-V-036-04 [positional_alternate_result] score=0.0176
POSITIONAL bphs1-ch15-005 <-> R-ATEXTB-MER-1H-OWN-V-036-08 [positional_alternate_result] score=0.0213
POSITIONAL bphs1-ch15-005 <-> R-ATEXTB-MER-1H-SCO-V-036-05 [positional_alternate_result] score=0.0188
POSITIONAL bphs1-ch15-005 <-> R-ATEXTB-MER-1H-V-036 [positional_alternate_result] score=0.0204
POSITIONAL bphs1-ch15-005 <-> R-ATEXTB-MER-1H-VIR-V-036-06 [positional_alternate_result] score=0.0178
POSITIONAL bphs1-ch15-005 <-> R-TBA15-600 [positional_alternate_result] score=0.0131
POSITIONAL bphs1-ch15-005 <-> R-TBA15-601 [positional_alternate_result] score=0.0293
POSITIONAL bphs1-ch15-005 <-> R-TBA15-602 [positional_alternate_result] score=0.0428
POSITIONAL bphs1-ch15-005 <-> R-TBA15-603 [positional_alternate_result] score=0.0422
POSITIONAL bphs1-ch15-005 <-> R-TBA15-604 [positional_alternate_result] score=0.0422
POSITIONAL bphs1-ch15-005 <-> R-TBA15-605 [positional_alternate_result] score=0.0419
POSITIONAL bphs1-ch15-005 <-> R-TBA15-606 [positional_alternate_result] score=0.0422
POSITIONAL bphs1-ch15-005 <-> R-TBA15-607 [positional_alternate_result] score=0.0363
POSITIONAL bphs1-ch15-005 <-> R-TBA15-608 [positional_alternate_result] score=0.0380
POSITIONAL bphs1-ch15-005 <-> R-TBA15-609 [positional_alternate_result] score=0.0368
POSITIONAL bphs1-ch15-005 <-> R-TBA15-610 [positional_alternate_result] score=0.0357
POSITIONAL bphs1-ch15-005 <-> R-TBA15-611 [positional_alternate_result] score=0.0379
POSITIONAL bphs1-ch15-005 <-> R-TBA15-612 [positional_alternate_result] score=0.0397
POSITIONAL bphs1-ch15-005 <-> R-TBA15-613 [positional_alternate_result] score=0.0378
POSITIONAL bphs1-ch15-005 <-> R-TBA15-614 [positional_alternate_result] score=0.0387
POSITIONAL bphs1-ch15-005 <-> R-TBA15-615 [positional_alternate_result] score=0.0384
POSITIONAL bphs1-ch15-005 <-> R-TBA15-616 [positional_alternate_result] score=0.0436
POSITIONAL bphs1-ch15-005 <-> R-TBA15-617 [positional_alternate_result] score=0.0457
POSITIONAL bphs1-ch15-005 <-> R-TBA15-618 [positional_alternate_result] score=0.0184
POSITIONAL bphs1-ch15-005 <-> R-TBA15-619 [positional_alternate_result] score=0.0343
POSITIONAL bphs1-ch15-005 <-> lalkitab-ch25-mercury-h1 [positional_alternate_result] score=0.0411
POSITIONAL bphs1-ch15-005 <-> pd-ch08-038 [positional_alternate_result] score=0.0556
POSITIONAL bphs1-ch17-011 <-> R-ATEXTB-MER-1H-AQU-V-036-01 [positional_alternate_result] score=0.0252
POSITIONAL bphs1-ch17-011 <-> R-ATEXTB-MER-1H-CAP-V-036-02 [positional_alternate_result] score=0.0216
POSITIONAL bphs1-ch17-011 <-> R-ATEXTB-MER-1H-EXA-V-036-07 [positional_alternate_result] score=0.0270
POSITIONAL bphs1-ch17-011 <-> R-ATEXTB-MER-1H-GEM-V-036-03 [positional_alternate_result] score=0.0256
POSITIONAL bphs1-ch17-011 <-> R-ATEXTB-MER-1H-LIB-V-036-04 [positional_alternate_result] score=0.0253
POSITIONAL bphs1-ch17-011 <-> R-ATEXTB-MER-1H-OWN-V-036-08 [positional_alternate_result] score=0.0270
POSITIONAL bphs1-ch17-011 <-> R-ATEXTB-MER-1H-SCO-V-036-05 [positional_alternate_result] score=0.0271
POSITIONAL bphs1-ch17-011 <-> R-ATEXTB-MER-1H-V-036 [positional_alternate_result] score=0.0505
POSITIONAL bphs1-ch17-011 <-> R-ATEXTB-MER-1H-VIR-V-036-06 [positional_alternate_result] score=0.0257
POSITIONAL bphs1-ch17-011 <-> R-TBA15-600 [positional_alternate_result] score=0.0311
POSITIONAL bphs1-ch17-011 <-> R-TBA15-601 [positional_alternate_result] score=0.0439
POSITIONAL bphs1-ch17-011 <-> R-TBA15-602 [positional_alternate_result] score=0.0616
POSITIONAL bphs1-ch17-011 <-> R-TBA15-603 [positional_alternate_result] score=0.0607
POSITIONAL bphs1-ch17-011 <-> R-TBA15-604 [positional_alternate_result] score=0.0608
POSITIONAL bphs1-ch17-011 <-> R-TBA15-605 [positional_alternate_result] score=0.0604
POSITIONAL bphs1-ch17-011 <-> R-TBA15-606 [positional_alternate_result] score=0.0608
POSITIONAL bphs1-ch17-011 <-> R-TBA15-607 [positional_alternate_result] score=0.0522
POSITIONAL bphs1-ch17-011 <-> R-TBA15-608 [positional_alternate_result] score=0.0547
POSITIONAL bphs1-ch17-011 <-> R-TBA15-609 [positional_alternate_result] score=0.1244
POSITIONAL bphs1-ch17-011 <-> R-TBA15-610 [positional_alternate_result] score=0.0471
POSITIONAL bphs1-ch17-011 <-> R-TBA15-611 [positional_alternate_result] score=0.0510
POSITIONAL bphs1-ch17-011 <-> R-TBA15-612 [positional_alternate_result] score=0.0634
POSITIONAL bphs1-ch17-011 <-> R-TBA15-613 [positional_alternate_result] score=0.0544
POSITIONAL bphs1-ch17-011 <-> R-TBA15-614 [positional_alternate_result] score=0.0675
POSITIONAL bphs1-ch17-011 <-> R-TBA15-615 [positional_alternate_result] score=0.0553
POSITIONAL bphs1-ch17-011 <-> R-TBA15-616 [positional_alternate_result] score=0.0605
POSITIONAL bphs1-ch17-011 <-> R-TBA15-617 [positional_alternate_result] score=0.0721
POSITIONAL bphs1-ch17-011 <-> R-TBA15-618 [positional_alternate_result] score=0.0354
POSITIONAL bphs1-ch17-011 <-> R-TBA15-619 [positional_alternate_result] score=0.0536
POSITIONAL bphs1-ch17-011 <-> lalkitab-ch25-mercury-h1 [positional_alternate_result] score=0.0435
POSITIONAL bphs1-ch17-011 <-> pd-ch08-038 [positional_polarity_conflict] score=0.0527
POSITIONAL bphs1-ch32-041 <-> R-ATEXTB-MER-10H-011 [positional_alternate_result] score=0.0591
POSITIONAL bphs1-ch32-041 <-> R-ATEXTB-MER-10H-DEB-V-045-02 [positional_alternate_result] score=0.0703
POSITIONAL bphs1-ch32-041 <-> R-ATEXTB-MER-10H-EXA-V-045-03 [positional_alternate_result] score=0.0772
POSITIONAL bphs1-ch32-041 <-> R-ATEXTB-MER-10H-OWN-V-045-04 [positional_alternate_result] score=0.0772
POSITIONAL bphs1-ch32-041 <-> R-ATEXTB-MER-10H-V-045 [positional_alternate_result] score=0.0382
POSITIONAL bphs1-ch32-041 <-> R-ATEXTB-MER-10H-VIR-V-045-01 [positional_alternate_result] score=0.0737
POSITIONAL bphs1-ch32-041 <-> R-TBA15-716 [positional_alternate_result] score=0.0530
POSITIONAL bphs1-ch32-041 <-> R-TBA15-717 [positional_alternate_result] score=0.0988
POSITIONAL bphs1-ch32-041 <-> R-TBA15-718 [positional_alternate_result] score=0.1060
POSITIONAL bphs1-ch32-041 <-> R-TBA15-719 [positional_alternate_result] score=0.0908
POSITIONAL bphs1-ch32-041 <-> R-TBA15-720 [positional_alternate_result] score=0.0878
POSITIONAL bphs1-ch32-041 <-> R-TBA15-721 [positional_alternate_result] score=0.1039
POSITIONAL bphs1-ch32-041 <-> R-TBA15-722 [positional_alternate_result] score=0.0756
POSITIONAL bphs1-ch32-041 <-> R-TBA15-723 [positional_alternate_result] score=0.0452
POSITIONAL bphs1-ch32-041 <-> pd-ch08-047 [positional_alternate_result] score=0.0764
POSITIONAL bphs1-ch42-016 <-> R-ATEXTB-MER-2H-052 [positional_alternate_result] score=0.0187
POSITIONAL bphs1-ch42-016 <-> R-ATEXTB-MER-2H-LEO-V-037-01 [positional_alternate_result] score=0.0481
POSITIONAL bphs1-ch42-016 <-> R-ATEXTB-MER-2H-V-037 [positional_alternate_result] score=0.0199
POSITIONAL bphs1-ch42-016 <-> R-BRIHAT-MER-2H-220 [positional_alternate_result] score=0.0195
POSITIONAL bphs1-ch42-016 <-> R-BRIHAT-MER-2H-244 [positional_alternate_result] score=0.0317
POSITIONAL bphs1-ch42-016 <-> R-TBA15-620 [positional_alternate_result] score=0.0288
POSITIONAL bphs1-ch42-016 <-> R-TBA15-621 [positional_alternate_result] score=0.0800
POSITIONAL bphs1-ch42-016 <-> R-TBA15-622 [positional_alternate_result] score=0.0682
POSITIONAL bphs1-ch42-016 <-> R-TBA15-623 [positional_alternate_result] score=0.0765
POSITIONAL bphs1-ch42-016 <-> R-TBA15-624 [positional_alternate_result] score=0.0741
POSITIONAL bphs1-ch42-016 <-> R-TBA15-625 [positional_alternate_result] score=0.0785
POSITIONAL bphs1-ch42-016 <-> R-TBA15-626 [positional_alternate_result] score=0.0754
POSITIONAL bphs1-ch42-016 <-> R-TBA15-627 [positional_alternate_result] score=0.0625
POSITIONAL bphs1-ch42-016 <-> R-TBA15-628 [positional_alternate_result] score=0.0528
POSITIONAL bphs1-ch42-016 <-> R-TBA15-629 [positional_alternate_result] score=0.0700
POSITIONAL bphs1-ch42-016 <-> R-TBA15-630 [positional_alternate_result] score=0.0731
POSITIONAL bphs1-ch42-016 <-> R-TBA15-631 [positional_alternate_result] score=0.0658
POSITIONAL bphs1-ch42-016 <-> R-TBA15-632 [positional_alternate_result] score=0.0848
POSITIONAL bphs1-ch42-016 <-> R-TBA15-633 [positional_alternate_result] score=0.0544
POSITIONAL bphs1-ch42-016 <-> R-TBA15-634 [positional_alternate_result] score=0.0721
POSITIONAL bphs1-ch42-016 <-> R-TBA15-635 [positional_alternate_result] score=0.0384
POSITIONAL bphs1-ch42-016 <-> pd-ch08-039 [positional_alternate_result] score=0.0414
POSITIONAL bphs1-ch32-022 <-> R-300IMP-MER-6H-142 [positional_alternate_result] score=0.0416
POSITIONAL bphs1-ch32-022 <-> R-ATEXTB-MER-6H-CAN-V-041-01 [positional_alternate_result] score=0.0257
POSITIONAL bphs1-ch32-022 <-> R-ATEXTB-MER-6H-DEB-V-041-02 [positional_alternate_result] score=0.0223
POSITIONAL bphs1-ch32-022 <-> R-ATEXTB-MER-6H-ENE-V-041-03 [positional_alternate_result] score=0.0223
POSITIONAL bphs1-ch32-022 <-> R-ATEXTB-MER-6H-V-041 [positional_alternate_result] score=0.0333
POSITIONAL bphs1-ch32-022 <-> R-TBA15-668 [positional_alternate_result] score=0.0521
POSITIONAL bphs1-ch32-022 <-> R-TBA15-669 [positional_alternate_result] score=0.0239
POSITIONAL bphs1-ch32-022 <-> R-TBA15-670 [positional_alternate_result] score=0.0334
POSITIONAL bphs1-ch32-022 <-> R-TBA15-671 [positional_alternate_result] score=0.0269
POSITIONAL bphs1-ch32-022 <-> R-TBA15-672 [positional_alternate_result] score=0.0249
POSITIONAL bphs1-ch32-022 <-> R-TBA15-673 [positional_alternate_result] score=0.0243
POSITIONAL bphs1-ch32-022 <-> R-TBA15-674 [positional_alternate_result] score=0.0307
POSITIONAL bphs1-ch32-022 <-> R-TBA15-675 [positional_alternate_result] score=0.0308
POSITIONAL bphs1-ch32-022 <-> R-TBA15-676 [positional_alternate_result] score=0.0323
POSITIONAL bphs1-ch32-022 <-> R-TBA15-677 [positional_alternate_result] score=0.0342
POSITIONAL bphs1-ch32-022 <-> R-TBA15-678 [positional_alternate_result] score=0.0453
POSITIONAL bphs1-ch32-022 <-> R-TBA15-679 [positional_alternate_result] score=0.0556
POSITIONAL bphs1-ch32-022 <-> lalkitab-ch27-wave-w23 [positional_alternate_result] score=0.0307
POSITIONAL bphs1-ch32-022 <-> lalkitab-ch27-wave-w49 [positional_alternate_result] score=0.0301
POSITIONAL bphs1-ch32-022 <-> pd-ch08-043 [positional_alternate_result] score=0.0640
POSITIONAL bphs1-ch18-011 <-> R-ATEXTB-MER-7H-DEB-V-042-05 [positional_alternate_result] score=0.0220
POSITIONAL bphs1-ch18-011 <-> R-ATEXTB-MER-7H-ENE-V-042-06 [positional_alternate_result] score=0.0220
POSITIONAL bphs1-ch18-011 <-> R-ATEXTB-MER-7H-GEM-V-042-01 [positional_alternate_result] score=0.0191
POSITIONAL bphs1-ch18-011 <-> R-ATEXTB-MER-7H-PIS-V-042-02 [positional_alternate_result] score=0.0201
POSITIONAL bphs1-ch18-011 <-> R-ATEXTB-MER-7H-TAU-V-042-03 [positional_alternate_result] score=0.0227
POSITIONAL bphs1-ch18-011 <-> R-ATEXTB-MER-7H-V-042 [positional_alternate_result] score=0.0444
POSITIONAL bphs1-ch18-011 <-> R-ATEXTB-MER-7H-VIR-V-042-04 [positional_alternate_result] score=0.0212
POSITIONAL bphs1-ch18-011 <-> R-TBA15-680 [positional_alternate_result] score=0.0448
POSITIONAL bphs1-ch18-011 <-> R-TBA15-681 [positional_alternate_result] score=0.0481
POSITIONAL bphs1-ch18-011 <-> R-TBA15-682 [positional_alternate_result] score=0.0606
POSITIONAL bphs1-ch18-011 <-> R-TBA15-683 [positional_alternate_result] score=0.1127
POSITIONAL bphs1-ch18-011 <-> R-TBA15-684 [positional_alternate_result] score=0.0415
POSITIONAL bphs1-ch18-011 <-> R-TBA15-685 [positional_alternate_result] score=0.0664
POSITIONAL bphs1-ch18-011 <-> R-TBA15-686 [positional_alternate_result] score=0.0527
POSITIONAL bphs1-ch18-011 <-> R-TBA15-687 [positional_alternate_result] score=0.0563
POSITIONAL bphs1-ch18-011 <-> R-TBA15-688 [positional_alternate_result] score=0.0633
POSITIONAL bphs1-ch18-011 <-> R-TBA15-689 [positional_alternate_result] score=0.0504
POSITIONAL bphs1-ch18-011 <-> R-TBA15-690 [positional_alternate_result] score=0.0635
POSITIONAL bphs1-ch18-011 <-> R-TBA15-691 [positional_alternate_result] score=0.0267
POSITIONAL bphs1-ch18-011 <-> R-TBA15-692 [positional_alternate_result] score=0.0609
POSITIONAL bphs1-ch18-011 <-> R-TBA15-693 [positional_alternate_result] score=0.0355
POSITIONAL bphs1-ch18-011 <-> R-TBA15-694 [positional_alternate_result] score=0.0464
POSITIONAL bphs1-ch18-011 <-> lalkitab-ch25-mercury-h7 [positional_alternate_result] score=0.0391
POSITIONAL bphs1-ch18-011 <-> lalkitab-ch27-wave-w11 [positional_alternate_result] score=0.0278
POSITIONAL bphs1-ch18-011 <-> lalkitab-ch27-wave-w30 [positional_alternate_result] score=0.0298
POSITIONAL bphs1-ch18-011 <-> pd-ch08-044 [positional_polarity_conflict] score=0.0711
POSITIONAL bphs1-ch18-011 <-> pd-ch10-008 [positional_alternate_result] score=0.0513
POSITIONAL bphs1-ch17-006 <-> R-ATEXTB-MOO-1H-AQU-V-013-01 [positional_alternate_result] score=0.0482
POSITIONAL bphs1-ch17-006 <-> R-ATEXTB-MOO-1H-ARI-V-013-02 [positional_alternate_result] score=0.0593
POSITIONAL bphs1-ch17-006 <-> R-ATEXTB-MOO-1H-CAN-V-013-03 [positional_alternate_result] score=0.0750
POSITIONAL bphs1-ch17-006 <-> R-ATEXTB-MOO-1H-CAP-V-013-04 [positional_alternate_result] score=0.0248
POSITIONAL bphs1-ch17-006 <-> R-ATEXTB-MOO-1H-DEB-V-013-10 [positional_alternate_result] score=0.0211
POSITIONAL bphs1-ch17-006 <-> R-ATEXTB-MOO-1H-EXA-V-013-11 [positional_alternate_result] score=0.0244
POSITIONAL bphs1-ch17-006 <-> R-ATEXTB-MOO-1H-LEO-V-013-05 [positional_alternate_result] score=0.0259
POSITIONAL bphs1-ch17-006 <-> R-ATEXTB-MOO-1H-LIB-V-013-06 [positional_alternate_result] score=0.0299
POSITIONAL bphs1-ch17-006 <-> R-ATEXTB-MOO-1H-SAG-V-013-07 [positional_alternate_result] score=0.0283
POSITIONAL bphs1-ch17-006 <-> R-ATEXTB-MOO-1H-SCO-V-013-08 [positional_alternate_result] score=0.0482
POSITIONAL bphs1-ch17-006 <-> R-ATEXTB-MOO-1H-TAU-V-013-09 [positional_alternate_result] score=0.0633
POSITIONAL bphs1-ch17-006 <-> R-ATEXTB-MOO-1H-V-013 [positional_alternate_result] score=0.0915
POSITIONAL bphs1-ch17-006 <-> R-TBA15-162 [positional_alternate_result] score=0.0153
POSITIONAL bphs1-ch17-006 <-> R-TBA15-163 [positional_alternate_result] score=0.0779
POSITIONAL bphs1-ch17-006 <-> R-TBA15-164 [positional_alternate_result] score=0.0476
POSITIONAL bphs1-ch17-006 <-> R-TBA15-165 [positional_alternate_result] score=0.0470
POSITIONAL bphs1-ch17-006 <-> R-TBA15-166 [positional_alternate_result] score=0.0885
POSITIONAL bphs1-ch17-006 <-> R-TBA15-167 [positional_alternate_result] score=0.0327
POSITIONAL bphs1-ch17-006 <-> R-TBA15-168 [positional_alternate_result] score=0.0227
POSITIONAL bphs1-ch17-006 <-> R-TBA15-169 [positional_alternate_result] score=0.0392
POSITIONAL bphs1-ch17-006 <-> R-TBA15-170 [positional_alternate_result] score=0.0368
POSITIONAL bphs1-ch17-006 <-> R-TBA15-171 [positional_alternate_result] score=0.0377
POSITIONAL bphs1-ch17-006 <-> R-TBA15-172 [positional_alternate_result] score=0.0382
POSITIONAL bphs1-ch17-006 <-> R-TBA15-173 [positional_alternate_result] score=0.0443
POSITIONAL bphs1-ch17-006 <-> R-TBA15-174 [positional_alternate_result] score=0.0394
POSITIONAL bphs1-ch17-006 <-> R-TBA15-175 [positional_alternate_result] score=0.0465
POSITIONAL bphs1-ch17-006 <-> R-TBA15-176 [positional_alternate_result] score=0.0449
POSITIONAL bphs1-ch17-006 <-> R-TBA15-177 [positional_alternate_result] score=0.0448
POSITIONAL bphs1-ch17-006 <-> R-TBA15-178 [positional_alternate_result] score=0.0490
POSITIONAL bphs1-ch17-006 <-> R-TBA15-179 [positional_alternate_result] score=0.0365
POSITIONAL bphs1-ch17-006 <-> R-TBA15-180 [positional_alternate_result] score=0.0540
POSITIONAL bphs1-ch17-006 <-> R-TBA15-181 [positional_alternate_result] score=0.0341
POSITIONAL bphs1-ch17-006 <-> R-TBA15-182 [positional_alternate_result] score=0.0337
POSITIONAL bphs1-ch17-006 <-> R-TBA15-183 [positional_alternate_result] score=0.0897
POSITIONAL bphs1-ch17-006 <-> R-TBA15-184 [positional_alternate_result] score=0.0336
POSITIONAL bphs1-ch17-006 <-> R-TBA15-185 [positional_alternate_result] score=0.0538
POSITIONAL bphs1-ch17-006 <-> R-TBA15-186 [positional_alternate_result] score=0.0602
POSITIONAL bphs1-ch17-006 <-> R-TBA15-187 [positional_alternate_result] score=0.0395
POSITIONAL bphs1-ch17-006 <-> R-TBA15-188 [positional_alternate_result] score=0.0329
POSITIONAL bphs1-ch17-006 <-> R-TBA15-189 [positional_alternate_result] score=0.0302
POSITIONAL bphs1-ch17-006 <-> R-TBA15-190 [positional_alternate_result] score=0.0614
POSITIONAL bphs1-ch17-006 <-> R-TBA15-191 [positional_alternate_result] score=0.0686
POSITIONAL bphs1-ch17-006 <-> R-TBA15-192 [positional_alternate_result] score=0.0571
POSITIONAL bphs1-ch17-006 <-> R-TBA15-193 [positional_alternate_result] score=0.0704
POSITIONAL bphs1-ch17-006 <-> R-TBA15-194 [positional_alternate_result] score=0.0552
POSITIONAL bphs1-ch17-006 <-> R-TBA15-195 [positional_alternate_result] score=0.0339
POSITIONAL bphs1-ch17-006 <-> R-TBA15-196 [positional_alternate_result] score=0.0339
POSITIONAL bphs1-ch17-006 <-> R-TBA15-197 [positional_alternate_result] score=0.0739
POSITIONAL bphs1-ch17-006 <-> R-TBA15-198 [positional_alternate_result] score=0.0338
POSITIONAL bphs1-ch17-006 <-> R-TBA15-199 [positional_alternate_result] score=0.0250
POSITIONAL bphs1-ch17-006 <-> lalkitab-ch25-moon-h1 [positional_alternate_result] score=0.0375
POSITIONAL bphs1-ch17-006 <-> pd-ch08-013 [positional_polarity_conflict] score=0.0787
POSITIONAL bphs1-ch17-006 <-> pd-ch08-014 [positional_alternate_result] score=0.0789
POSITIONAL bphs1-ch17-007 <-> R-ATEXTB-MOO-1H-AQU-V-013-01 [positional_alternate_result] score=0.0169
POSITIONAL bphs1-ch17-007 <-> R-ATEXTB-MOO-1H-ARI-V-013-02 [positional_alternate_result] score=0.0156
POSITIONAL bphs1-ch17-007 <-> R-ATEXTB-MOO-1H-CAN-V-013-03 [positional_alternate_result] score=0.0161
POSITIONAL bphs1-ch17-007 <-> R-ATEXTB-MOO-1H-CAP-V-013-04 [positional_alternate_result] score=0.0266
POSITIONAL bphs1-ch17-007 <-> R-ATEXTB-MOO-1H-DEB-V-013-10 [positional_alternate_result] score=0.0119
POSITIONAL bphs1-ch17-007 <-> R-ATEXTB-MOO-1H-EXA-V-013-11 [positional_alternate_result] score=0.0178
POSITIONAL bphs1-ch17-007 <-> R-ATEXTB-MOO-1H-LEO-V-013-05 [positional_alternate_result] score=0.0162
POSITIONAL bphs1-ch17-007 <-> R-ATEXTB-MOO-1H-LIB-V-013-06 [positional_alternate_result] score=0.0190
POSITIONAL bphs1-ch17-007 <-> R-ATEXTB-MOO-1H-SAG-V-013-07 [positional_alternate_result] score=0.0148
POSITIONAL bphs1-ch17-007 <-> R-ATEXTB-MOO-1H-SCO-V-013-08 [positional_alternate_result] score=0.0165
POSITIONAL bphs1-ch17-007 <-> R-ATEXTB-MOO-1H-TAU-V-013-09 [positional_alternate_result] score=0.0171
POSITIONAL bphs1-ch17-007 <-> R-ATEXTB-MOO-1H-V-013 [positional_alternate_result] score=0.0435
POSITIONAL bphs1-ch17-007 <-> R-TBA15-162 [positional_alternate_result] score=0.0310
POSITIONAL bphs1-ch17-007 <-> R-TBA15-163 [positional_alternate_result] score=0.0557
POSITIONAL bphs1-ch17-007 <-> R-TBA15-164 [positional_alternate_result] score=0.0637
POSITIONAL bphs1-ch17-007 <-> R-TBA15-165 [positional_alternate_result] score=0.0629
POSITIONAL bphs1-ch17-007 <-> R-TBA15-166 [positional_alternate_result] score=0.0633
POSITIONAL bphs1-ch17-007 <-> R-TBA15-167 [positional_alternate_result] score=0.0534
POSITIONAL bphs1-ch17-007 <-> R-TBA15-168 [positional_alternate_result] score=0.0508
POSITIONAL bphs1-ch17-007 <-> R-TBA15-169 [positional_alternate_result] score=0.0607
POSITIONAL bphs1-ch17-007 <-> R-TBA15-170 [positional_alternate_result] score=0.0505
POSITIONAL bphs1-ch17-007 <-> R-TBA15-171 [positional_alternate_result] score=0.0594
POSITIONAL bphs1-ch17-007 <-> R-TBA15-172 [positional_alternate_result] score=0.0511
POSITIONAL bphs1-ch17-007 <-> R-TBA15-173 [positional_alternate_result] score=0.0623
POSITIONAL bphs1-ch17-007 <-> R-TBA15-174 [positional_alternate_result] score=0.0528
POSITIONAL bphs1-ch17-007 <-> R-TBA15-175 [positional_alternate_result] score=0.0622
POSITIONAL bphs1-ch17-007 <-> R-TBA15-176 [positional_alternate_result] score=0.0601
POSITIONAL bphs1-ch17-007 <-> R-TBA15-177 [positional_alternate_result] score=0.0599
POSITIONAL bphs1-ch17-007 <-> R-TBA15-178 [positional_alternate_result] score=0.0656
POSITIONAL bphs1-ch17-007 <-> R-TBA15-179 [positional_alternate_result] score=0.0538
POSITIONAL bphs1-ch17-007 <-> R-TBA15-180 [positional_alternate_result] score=0.0445
POSITIONAL bphs1-ch17-007 <-> R-TBA15-181 [positional_alternate_result] score=0.0507
POSITIONAL bphs1-ch17-007 <-> R-TBA15-182 [positional_alternate_result] score=0.0501
POSITIONAL bphs1-ch17-007 <-> R-TBA15-183 [positional_alternate_result] score=0.0505
POSITIONAL bphs1-ch17-007 <-> R-TBA15-184 [positional_alternate_result] score=0.0499
POSITIONAL bphs1-ch17-007 <-> R-TBA15-185 [positional_alternate_result] score=0.0228
POSITIONAL bphs1-ch17-007 <-> R-TBA15-186 [positional_alternate_result] score=0.0571
POSITIONAL bphs1-ch17-007 <-> R-TBA15-187 [positional_alternate_result] score=0.0486
POSITIONAL bphs1-ch17-007 <-> R-TBA15-188 [positional_alternate_result] score=0.0491
POSITIONAL bphs1-ch17-007 <-> R-TBA15-189 [positional_alternate_result] score=0.0450
POSITIONAL bphs1-ch17-007 <-> R-TBA15-190 [positional_alternate_result] score=0.0278
POSITIONAL bphs1-ch17-007 <-> R-TBA15-191 [positional_alternate_result] score=0.0335
POSITIONAL bphs1-ch17-007 <-> R-TBA15-192 [positional_alternate_result] score=0.0279
POSITIONAL bphs1-ch17-007 <-> R-TBA15-193 [positional_alternate_result] score=0.0332
POSITIONAL bphs1-ch17-007 <-> R-TBA15-194 [positional_alternate_result] score=0.0447
POSITIONAL bphs1-ch17-007 <-> R-TBA15-195 [positional_alternate_result] score=0.0488
POSITIONAL bphs1-ch17-007 <-> R-TBA15-196 [positional_alternate_result] score=0.0488
POSITIONAL bphs1-ch17-007 <-> R-TBA15-197 [positional_alternate_result] score=0.0488
POSITIONAL bphs1-ch17-007 <-> R-TBA15-198 [positional_alternate_result] score=0.0486
POSITIONAL bphs1-ch17-007 <-> R-TBA15-199 [positional_alternate_result] score=0.0214
POSITIONAL bphs1-ch17-007 <-> lalkitab-ch25-moon-h1 [positional_alternate_result] score=0.0279
POSITIONAL bphs1-ch17-007 <-> pd-ch08-013 [positional_polarity_conflict] score=0.0512
POSITIONAL bphs1-ch17-007 <-> pd-ch08-014 [positional_alternate_result] score=0.0704
POSITIONAL bphs1-ch17-008 <-> R-ATEXTB-MOO-1H-AQU-V-013-01 [positional_alternate_result] score=0.0176
POSITIONAL bphs1-ch17-008 <-> R-ATEXTB-MOO-1H-ARI-V-013-02 [positional_alternate_result] score=0.0179
POSITIONAL bphs1-ch17-008 <-> R-ATEXTB-MOO-1H-CAN-V-013-03 [positional_alternate_result] score=0.0179
POSITIONAL bphs1-ch17-008 <-> R-ATEXTB-MOO-1H-CAP-V-013-04 [positional_alternate_result] score=0.0133
POSITIONAL bphs1-ch17-008 <-> R-ATEXTB-MOO-1H-DEB-V-013-10 [positional_alternate_result] score=0.0121
POSITIONAL bphs1-ch17-008 <-> R-ATEXTB-MOO-1H-EXA-V-013-11 [positional_alternate_result] score=0.0181
POSITIONAL bphs1-ch17-008 <-> R-ATEXTB-MOO-1H-LEO-V-013-05 [positional_alternate_result] score=0.0174
POSITIONAL bphs1-ch17-008 <-> R-ATEXTB-MOO-1H-LIB-V-013-06 [positional_alternate_result] score=0.0153
POSITIONAL bphs1-ch17-008 <-> R-ATEXTB-MOO-1H-SAG-V-013-07 [positional_alternate_result] score=0.0143
POSITIONAL bphs1-ch17-008 <-> R-ATEXTB-MOO-1H-SCO-V-013-08 [positional_alternate_result] score=0.0175
POSITIONAL bphs1-ch17-008 <-> R-ATEXTB-MOO-1H-TAU-V-013-09 [positional_alternate_result] score=0.0167
POSITIONAL bphs1-ch17-008 <-> R-ATEXTB-MOO-1H-V-013 [positional_alternate_result] score=0.0345
POSITIONAL bphs1-ch17-008 <-> R-TBA15-162 [positional_alternate_result] score=0.0200
POSITIONAL bphs1-ch17-008 <-> R-TBA15-163 [positional_alternate_result] score=0.0434
POSITIONAL bphs1-ch17-008 <-> R-TBA15-164 [positional_alternate_result] score=0.0462
POSITIONAL bphs1-ch17-008 <-> R-TBA15-165 [positional_alternate_result] score=0.0457
POSITIONAL bphs1-ch17-008 <-> R-TBA15-166 [positional_alternate_result] score=0.0459
POSITIONAL bphs1-ch17-008 <-> R-TBA15-167 [positional_alternate_result] score=0.0398
POSITIONAL bphs1-ch17-008 <-> R-TBA15-168 [positional_alternate_result] score=0.0296
POSITIONAL bphs1-ch17-008 <-> R-TBA15-169 [positional_alternate_result] score=0.0472
POSITIONAL bphs1-ch17-008 <-> R-TBA15-170 [positional_alternate_result] score=0.0403
POSITIONAL bphs1-ch17-008 <-> R-TBA15-171 [positional_alternate_result] score=0.0359
POSITIONAL bphs1-ch17-008 <-> R-TBA15-172 [positional_alternate_result] score=0.0371
POSITIONAL bphs1-ch17-008 <-> R-TBA15-173 [positional_alternate_result] score=0.0467
POSITIONAL bphs1-ch17-008 <-> R-TBA15-174 [positional_alternate_result] score=0.0411
POSITIONAL bphs1-ch17-008 <-> R-TBA15-175 [positional_alternate_result] score=0.0451
POSITIONAL bphs1-ch17-008 <-> R-TBA15-176 [positional_alternate_result] score=0.0436
POSITIONAL bphs1-ch17-008 <-> R-TBA15-177 [positional_alternate_result] score=0.0435
POSITIONAL bphs1-ch17-008 <-> R-TBA15-178 [positional_alternate_result] score=0.0476
POSITIONAL bphs1-ch17-008 <-> R-TBA15-179 [positional_alternate_result] score=0.0388
POSITIONAL bphs1-ch17-008 <-> R-TBA15-180 [positional_alternate_result] score=0.0359
POSITIONAL bphs1-ch17-008 <-> R-TBA15-181 [positional_alternate_result] score=0.0387
POSITIONAL bphs1-ch17-008 <-> R-TBA15-182 [positional_alternate_result] score=0.0383
POSITIONAL bphs1-ch17-008 <-> R-TBA15-183 [positional_alternate_result] score=0.0386
POSITIONAL bphs1-ch17-008 <-> R-TBA15-184 [positional_alternate_result] score=0.0381
POSITIONAL bphs1-ch17-008 <-> R-TBA15-185 [positional_alternate_result] score=0.0170
POSITIONAL bphs1-ch17-008 <-> R-TBA15-186 [positional_alternate_result] score=0.0320
POSITIONAL bphs1-ch17-008 <-> R-TBA15-187 [positional_alternate_result] score=0.0499
POSITIONAL bphs1-ch17-008 <-> R-TBA15-188 [positional_alternate_result] score=0.0357
POSITIONAL bphs1-ch17-008 <-> R-TBA15-189 [positional_alternate_result] score=0.0327
POSITIONAL bphs1-ch17-008 <-> R-TBA15-190 [positional_alternate_result] score=0.0209
POSITIONAL bphs1-ch17-008 <-> R-TBA15-191 [positional_alternate_result] score=0.0263
POSITIONAL bphs1-ch17-008 <-> R-TBA15-192 [positional_alternate_result] score=0.0219
POSITIONAL bphs1-ch17-008 <-> R-TBA15-193 [positional_alternate_result] score=0.0386
POSITIONAL bphs1-ch17-008 <-> R-TBA15-194 [positional_alternate_result] score=0.0329
POSITIONAL bphs1-ch17-008 <-> R-TBA15-195 [positional_alternate_result] score=0.0338
POSITIONAL bphs1-ch17-008 <-> R-TBA15-196 [positional_alternate_result] score=0.0338
POSITIONAL bphs1-ch17-008 <-> R-TBA15-197 [positional_alternate_result] score=0.0338
POSITIONAL bphs1-ch17-008 <-> R-TBA15-198 [positional_alternate_result] score=0.0337
POSITIONAL bphs1-ch17-008 <-> R-TBA15-199 [positional_alternate_result] score=0.0172
POSITIONAL bphs1-ch17-008 <-> lalkitab-ch25-moon-h1 [positional_alternate_result] score=0.0266
POSITIONAL bphs1-ch17-008 <-> pd-ch08-013 [positional_polarity_conflict] score=0.0528
POSITIONAL bphs1-ch17-008 <-> pd-ch08-014 [positional_alternate_result] score=0.0520
POSITIONAL bphs1-ch17-017 <-> R-ATEXTB-MOO-1H-AQU-V-013-01 [positional_alternate_result] score=0.0126
POSITIONAL bphs1-ch17-017 <-> R-ATEXTB-MOO-1H-ARI-V-013-02 [positional_alternate_result] score=0.0123
POSITIONAL bphs1-ch17-017 <-> R-ATEXTB-MOO-1H-CAN-V-013-03 [positional_alternate_result] score=0.0133
POSITIONAL bphs1-ch17-017 <-> R-ATEXTB-MOO-1H-CAP-V-013-04 [positional_alternate_result] score=0.0116
POSITIONAL bphs1-ch17-017 <-> R-ATEXTB-MOO-1H-DEB-V-013-10 [positional_alternate_result] score=0.0141
POSITIONAL bphs1-ch17-017 <-> R-ATEXTB-MOO-1H-EXA-V-013-11 [positional_alternate_result] score=0.0158
POSITIONAL bphs1-ch17-017 <-> R-ATEXTB-MOO-1H-LEO-V-013-05 [positional_alternate_result] score=0.0094
POSITIONAL bphs1-ch17-017 <-> R-ATEXTB-MOO-1H-LIB-V-013-06 [positional_alternate_result] score=0.0148
POSITIONAL bphs1-ch17-017 <-> R-ATEXTB-MOO-1H-SAG-V-013-07 [positional_alternate_result] score=0.0086
POSITIONAL bphs1-ch17-017 <-> R-ATEXTB-MOO-1H-SCO-V-013-08 [positional_alternate_result] score=0.0144
POSITIONAL bphs1-ch17-017 <-> R-ATEXTB-MOO-1H-TAU-V-013-09 [positional_alternate_result] score=0.0133
POSITIONAL bphs1-ch17-017 <-> R-ATEXTB-MOO-1H-V-013 [positional_alternate_result] score=0.0274
POSITIONAL bphs1-ch17-017 <-> R-TBA15-162 [positional_alternate_result] score=0.0261
POSITIONAL bphs1-ch17-017 <-> R-TBA15-163 [positional_alternate_result] score=0.0265
POSITIONAL bphs1-ch17-017 <-> R-TBA15-164 [positional_alternate_result] score=0.0303
POSITIONAL bphs1-ch17-017 <-> R-TBA15-165 [positional_alternate_result] score=0.0300
POSITIONAL bphs1-ch17-017 <-> R-TBA15-166 [positional_alternate_result] score=0.0301
POSITIONAL bphs1-ch17-017 <-> R-TBA15-167 [positional_alternate_result] score=0.0246
POSITIONAL bphs1-ch17-017 <-> R-TBA15-168 [positional_alternate_result] score=0.0188
POSITIONAL bphs1-ch17-017 <-> R-TBA15-169 [positional_alternate_result] score=0.0295
POSITIONAL bphs1-ch17-017 <-> R-TBA15-170 [positional_alternate_result] score=0.0225
POSITIONAL bphs1-ch17-017 <-> R-TBA15-171 [positional_alternate_result] score=0.0229
POSITIONAL bphs1-ch17-017 <-> R-TBA15-172 [positional_alternate_result] score=0.0244
POSITIONAL bphs1-ch17-017 <-> R-TBA15-173 [positional_alternate_result] score=0.0282
POSITIONAL bphs1-ch17-017 <-> R-TBA15-174 [positional_alternate_result] score=0.0251
POSITIONAL bphs1-ch17-017 <-> R-TBA15-175 [positional_alternate_result] score=0.0296
POSITIONAL bphs1-ch17-017 <-> R-TBA15-176 [positional_alternate_result] score=0.0286
POSITIONAL bphs1-ch17-017 <-> R-TBA15-177 [positional_alternate_result] score=0.0285
POSITIONAL bphs1-ch17-017 <-> R-TBA15-178 [positional_alternate_result] score=0.0312
POSITIONAL bphs1-ch17-017 <-> R-TBA15-179 [positional_alternate_result] score=0.0304
POSITIONAL bphs1-ch17-017 <-> R-TBA15-180 [positional_alternate_result] score=0.0267
POSITIONAL bphs1-ch17-017 <-> R-TBA15-181 [positional_alternate_result] score=0.0304
POSITIONAL bphs1-ch17-017 <-> R-TBA15-182 [positional_alternate_result] score=0.0300
POSITIONAL bphs1-ch17-017 <-> R-TBA15-183 [positional_alternate_result] score=0.0303
POSITIONAL bphs1-ch17-017 <-> R-TBA15-184 [positional_alternate_result] score=0.0299
POSITIONAL bphs1-ch17-017 <-> R-TBA15-185 [positional_alternate_result] score=0.0203
POSITIONAL bphs1-ch17-017 <-> R-TBA15-186 [positional_alternate_result] score=0.0266
POSITIONAL bphs1-ch17-017 <-> R-TBA15-187 [positional_alternate_result] score=0.0261
POSITIONAL bphs1-ch17-017 <-> R-TBA15-188 [positional_alternate_result] score=0.0234
POSITIONAL bphs1-ch17-017 <-> R-TBA15-189 [positional_alternate_result] score=0.0214
POSITIONAL bphs1-ch17-017 <-> R-TBA15-190 [positional_alternate_result] score=0.0222
POSITIONAL bphs1-ch17-017 <-> R-TBA15-191 [positional_alternate_result] score=0.0226
POSITIONAL bphs1-ch17-017 <-> R-TBA15-192 [positional_alternate_result] score=0.0188
POSITIONAL bphs1-ch17-017 <-> R-TBA15-193 [positional_alternate_result] score=0.0253
POSITIONAL bphs1-ch17-017 <-> R-TBA15-194 [positional_alternate_result] score=0.0228
POSITIONAL bphs1-ch17-017 <-> R-TBA15-195 [positional_alternate_result] score=0.0249
POSITIONAL bphs1-ch17-017 <-> R-TBA15-196 [positional_alternate_result] score=0.0249
POSITIONAL bphs1-ch17-017 <-> R-TBA15-197 [positional_alternate_result] score=0.0249
POSITIONAL bphs1-ch17-017 <-> R-TBA15-198 [positional_alternate_result] score=0.0248
POSITIONAL bphs1-ch17-017 <-> R-TBA15-199 [positional_alternate_result] score=0.0177
POSITIONAL bphs1-ch17-017 <-> lalkitab-ch25-moon-h1 [positional_alternate_result] score=0.0396
POSITIONAL bphs1-ch17-017 <-> pd-ch08-013 [positional_polarity_conflict] score=0.0513
POSITIONAL bphs1-ch17-017 <-> pd-ch08-014 [positional_alternate_result] score=0.0478
POSITIONAL bphs1-ch45-022 <-> R-ATEXTB-MOO-10H-ARI-V-021-01 [positional_alternate_result] score=0.1974
POSITIONAL bphs1-ch45-022 <-> R-ATEXTB-MOO-10H-CAN-V-021-02 [positional_alternate_result] score=0.1963
POSITIONAL bphs1-ch45-022 <-> R-ATEXTB-MOO-10H-CAP-V-021-03 [positional_alternate_result] score=0.1952
POSITIONAL bphs1-ch45-022 <-> R-ATEXTB-MOO-10H-ENE-V-021-05 [positional_alternate_result] score=0.1971
POSITIONAL bphs1-ch45-022 <-> R-ATEXTB-MOO-10H-EXA-V-021-06 [positional_alternate_result] score=0.2586
POSITIONAL bphs1-ch45-022 <-> R-ATEXTB-MOO-10H-LIB-V-021-04 [positional_alternate_result] score=0.1938
POSITIONAL bphs1-ch45-022 <-> R-ATEXTB-MOO-10H-V-021 [positional_alternate_result] score=0.0777
POSITIONAL bphs1-ch45-022 <-> R-TBA15-333 [positional_alternate_result] score=0.0692
POSITIONAL bphs1-ch45-022 <-> R-TBA15-334 [positional_alternate_result] score=0.2320
POSITIONAL bphs1-ch45-022 <-> R-TBA15-335 [positional_alternate_result] score=0.2917
POSITIONAL bphs1-ch45-022 <-> R-TBA15-336 [positional_alternate_result] score=0.2652
POSITIONAL bphs1-ch45-022 <-> R-TBA15-337 [positional_alternate_result] score=0.2187
POSITIONAL bphs1-ch45-022 <-> R-TBA15-338 [positional_alternate_result] score=0.1864
POSITIONAL bphs1-ch45-022 <-> R-TBA15-339 [positional_alternate_result] score=0.2412
POSITIONAL bphs1-ch45-022 <-> R-TBA15-340 [positional_alternate_result] score=0.2628
POSITIONAL bphs1-ch45-022 <-> R-TBA15-341 [positional_alternate_result] score=0.2958
POSITIONAL bphs1-ch45-022 <-> R-TBA15-342 [positional_alternate_result] score=0.2449
POSITIONAL bphs1-ch45-022 <-> R-TBA15-343 [positional_alternate_result] score=0.2448
POSITIONAL bphs1-ch45-022 <-> R-TBA15-344 [positional_alternate_result] score=0.2421
POSITIONAL bphs1-ch45-022 <-> R-TBA15-345 [positional_alternate_result] score=0.2442
POSITIONAL bphs1-ch45-022 <-> R-TBA15-346 [positional_alternate_result] score=0.2166
POSITIONAL bphs1-ch45-022 <-> R-TBA15-347 [positional_alternate_result] score=0.2523
POSITIONAL bphs1-ch45-022 <-> R-TBA15-348 [positional_alternate_result] score=0.2249
POSITIONAL bphs1-ch45-022 <-> R-TBA15-349 [positional_alternate_result] score=0.2652
POSITIONAL bphs1-ch45-022 <-> R-TBA15-350 [positional_alternate_result] score=0.1393
POSITIONAL bphs1-ch45-022 <-> lalkitab-ch25-moon-h10 [positional_alternate_result] score=0.1702
POSITIONAL bphs1-ch45-022 <-> pd-ch08-023 [positional_alternate_result] score=0.1161
POSITIONAL bphs1-ch14-013 <-> R-ATEXTB-MOO-3H-DEB-V-015-01 [positional_alternate_result] score=0.0243
POSITIONAL bphs1-ch14-013 <-> R-ATEXTB-MOO-3H-EXA-V-015-02 [positional_alternate_result] score=0.0291
POSITIONAL bphs1-ch14-013 <-> R-ATEXTB-MOO-3H-V-015 [positional_alternate_result] score=0.0354
POSITIONAL bphs1-ch14-013 <-> R-BRIHAT-MOO-3H-087 [positional_alternate_result] score=0.0677
POSITIONAL bphs1-ch14-013 <-> R-TBA15-216 [positional_alternate_result] score=0.0311
POSITIONAL bphs1-ch14-013 <-> R-TBA15-217 [positional_alternate_result] score=0.0485
POSITIONAL bphs1-ch14-013 <-> R-TBA15-218 [positional_alternate_result] score=0.0629
POSITIONAL bphs1-ch14-013 <-> R-TBA15-219 [positional_alternate_result] score=0.0536
POSITIONAL bphs1-ch14-013 <-> R-TBA15-220 [positional_alternate_result] score=0.0429
POSITIONAL bphs1-ch14-013 <-> R-TBA15-221 [positional_alternate_result] score=0.0380
POSITIONAL bphs1-ch14-013 <-> R-TBA15-222 [positional_alternate_result] score=0.0433
POSITIONAL bphs1-ch14-013 <-> R-TBA15-223 [positional_alternate_result] score=0.0517
POSITIONAL bphs1-ch14-013 <-> R-TBA15-224 [positional_alternate_result] score=0.0249
POSITIONAL bphs1-ch14-013 <-> lalkitab-ch25-moon-h3 [positional_alternate_result] score=0.0449
POSITIONAL bphs1-ch14-013 <-> pd-ch08-016 [positional_alternate_result] score=0.1115
POSITIONAL bphs1-ch14-014 <-> R-ATEXTB-MOO-3H-DEB-V-015-01 [positional_alternate_result] score=0.0258
POSITIONAL bphs1-ch14-014 <-> R-ATEXTB-MOO-3H-EXA-V-015-02 [positional_alternate_result] score=0.0309
POSITIONAL bphs1-ch14-014 <-> R-ATEXTB-MOO-3H-V-015 [positional_alternate_result] score=0.0441
POSITIONAL bphs1-ch14-014 <-> R-BRIHAT-MOO-3H-087 [positional_alternate_result] score=0.0799
POSITIONAL bphs1-ch14-014 <-> R-TBA15-216 [positional_alternate_result] score=0.0239
POSITIONAL bphs1-ch14-014 <-> R-TBA15-217 [positional_alternate_result] score=0.0496
POSITIONAL bphs1-ch14-014 <-> R-TBA15-218 [positional_alternate_result] score=0.0644
POSITIONAL bphs1-ch14-014 <-> R-TBA15-219 [positional_alternate_result] score=0.0549
POSITIONAL bphs1-ch14-014 <-> R-TBA15-220 [positional_alternate_result] score=0.0912
POSITIONAL bphs1-ch14-014 <-> R-TBA15-221 [positional_alternate_result] score=0.0426
POSITIONAL bphs1-ch14-014 <-> R-TBA15-222 [positional_alternate_result] score=0.0465
POSITIONAL bphs1-ch14-014 <-> R-TBA15-223 [positional_alternate_result] score=0.0529
POSITIONAL bphs1-ch14-014 <-> R-TBA15-224 [positional_alternate_result] score=0.0247
POSITIONAL bphs1-ch14-014 <-> lalkitab-ch25-moon-h3 [positional_alternate_result] score=0.0440
POSITIONAL bphs1-ch14-014 <-> pd-ch08-016 [positional_alternate_result] score=0.1099
POSITIONAL bphs1-ch32-020 <-> R-ATEXTB-MOO-4H-CAN-V-016-01 [positional_alternate_result] score=0.0167
POSITIONAL bphs1-ch32-020 <-> R-ATEXTB-MOO-4H-DEB-V-016-07 [positional_alternate_result] score=0.0155
POSITIONAL bphs1-ch32-020 <-> R-ATEXTB-MOO-4H-ENE-V-016-08 [positional_alternate_result] score=0.0354
POSITIONAL bphs1-ch32-020 <-> R-ATEXTB-MOO-4H-EXA-V-016-09 [positional_alternate_result] score=0.0151
POSITIONAL bphs1-ch32-020 <-> R-ATEXTB-MOO-4H-LEO-V-016-02 [positional_alternate_result] score=0.0148
POSITIONAL bphs1-ch32-020 <-> R-ATEXTB-MOO-4H-SAG-V-016-03 [positional_alternate_result] score=0.0271
POSITIONAL bphs1-ch32-020 <-> R-ATEXTB-MOO-4H-SCO-V-016-04 [positional_alternate_result] score=0.0150
POSITIONAL bphs1-ch32-020 <-> R-ATEXTB-MOO-4H-TAU-V-016-05 [positional_alternate_result] score=0.0104
POSITIONAL bphs1-ch32-020 <-> R-ATEXTB-MOO-4H-V-016 [positional_alternate_result] score=0.0470
POSITIONAL bphs1-ch32-020 <-> R-ATEXTB-MOO-4H-VIR-V-016-06 [positional_alternate_result] score=0.0149
POSITIONAL bphs1-ch32-020 <-> R-TBA15-225 [positional_alternate_result] score=0.0323
POSITIONAL bphs1-ch32-020 <-> R-TBA15-226 [positional_alternate_result] score=0.0751
POSITIONAL bphs1-ch32-020 <-> R-TBA15-227 [positional_alternate_result] score=0.0868
POSITIONAL bphs1-ch32-020 <-> R-TBA15-228 [positional_alternate_result] score=0.0486
POSITIONAL bphs1-ch32-020 <-> R-TBA15-229 [positional_alternate_result] score=0.0719
POSITIONAL bphs1-ch32-020 <-> R-TBA15-230 [positional_alternate_result] score=0.0947
POSITIONAL bphs1-ch32-020 <-> R-TBA15-231 [positional_alternate_result] score=0.0658
POSITIONAL bphs1-ch32-020 <-> R-TBA15-232 [positional_alternate_result] score=0.0742
POSITIONAL bphs1-ch32-020 <-> R-TBA15-233 [positional_alternate_result] score=0.0620
POSITIONAL bphs1-ch32-020 <-> R-TBA15-234 [positional_alternate_result] score=0.1191
POSITIONAL bphs1-ch32-020 <-> R-TBA15-235 [positional_alternate_result] score=0.0980
POSITIONAL bphs1-ch32-020 <-> R-TBA15-236 [positional_alternate_result] score=0.0359
POSITIONAL bphs1-ch32-020 <-> R-TBA15-237 [positional_alternate_result] score=0.0840
POSITIONAL bphs1-ch32-020 <-> R-TBA15-238 [positional_alternate_result] score=0.0681
POSITIONAL bphs1-ch32-020 <-> lalkitab-ch27-wave-w05 [positional_alternate_result] score=0.0202
POSITIONAL bphs1-ch32-020 <-> lalkitab-ch27-wave-w27 [positional_alternate_result] score=0.0210
POSITIONAL bphs1-ch32-020 <-> lalkitab-ch27-wave-w35 [positional_alternate_result] score=0.0195
POSITIONAL bphs1-ch32-020 <-> lalkitab-ch27-wave-w47 [positional_alternate_result] score=0.0178
POSITIONAL bphs1-ch32-020 <-> pd-ch08-017 [positional_alternate_result] score=0.1440
POSITIONAL bphs1-ch32-035 <-> R-ATEXTB-MOO-4H-CAN-V-016-01 [positional_alternate_result] score=0.0199
POSITIONAL bphs1-ch32-035 <-> R-ATEXTB-MOO-4H-DEB-V-016-07 [positional_alternate_result] score=0.0157
POSITIONAL bphs1-ch32-035 <-> R-ATEXTB-MOO-4H-ENE-V-016-08 [positional_alternate_result] score=0.0388
POSITIONAL bphs1-ch32-035 <-> R-ATEXTB-MOO-4H-EXA-V-016-09 [positional_alternate_result] score=0.0212
POSITIONAL bphs1-ch32-035 <-> R-ATEXTB-MOO-4H-LEO-V-016-02 [positional_alternate_result] score=0.0130
POSITIONAL bphs1-ch32-035 <-> R-ATEXTB-MOO-4H-SAG-V-016-03 [positional_alternate_result] score=0.0127
POSITIONAL bphs1-ch32-035 <-> R-ATEXTB-MOO-4H-SCO-V-016-04 [positional_alternate_result] score=0.0132
POSITIONAL bphs1-ch32-035 <-> R-ATEXTB-MOO-4H-TAU-V-016-05 [positional_alternate_result] score=0.0124
POSITIONAL bphs1-ch32-035 <-> R-ATEXTB-MOO-4H-V-016 [positional_alternate_result] score=0.0485
POSITIONAL bphs1-ch32-035 <-> R-ATEXTB-MOO-4H-VIR-V-016-06 [positional_alternate_result] score=0.0131
POSITIONAL bphs1-ch32-035 <-> R-TBA15-225 [positional_alternate_result] score=0.0260
POSITIONAL bphs1-ch32-035 <-> R-TBA15-226 [positional_alternate_result] score=0.0569
POSITIONAL bphs1-ch32-035 <-> R-TBA15-227 [positional_alternate_result] score=0.0510
POSITIONAL bphs1-ch32-035 <-> R-TBA15-228 [positional_alternate_result] score=0.0368
POSITIONAL bphs1-ch32-035 <-> R-TBA15-229 [positional_alternate_result] score=0.0627
POSITIONAL bphs1-ch32-035 <-> R-TBA15-230 [positional_alternate_result] score=0.0761
POSITIONAL bphs1-ch32-035 <-> R-TBA15-231 [positional_alternate_result] score=0.0528
POSITIONAL bphs1-ch32-035 <-> R-TBA15-232 [positional_alternate_result] score=0.0615
POSITIONAL bphs1-ch32-035 <-> R-TBA15-233 [positional_alternate_result] score=0.0570
POSITIONAL bphs1-ch32-035 <-> R-TBA15-234 [positional_alternate_result] score=0.1057
POSITIONAL bphs1-ch32-035 <-> R-TBA15-235 [positional_alternate_result] score=0.0599
POSITIONAL bphs1-ch32-035 <-> R-TBA15-236 [positional_alternate_result] score=0.0331
POSITIONAL bphs1-ch32-035 <-> R-TBA15-237 [positional_alternate_result] score=0.0637
POSITIONAL bphs1-ch32-035 <-> R-TBA15-238 [positional_alternate_result] score=0.0595
POSITIONAL bphs1-ch32-035 <-> lalkitab-ch27-wave-w05 [positional_alternate_result] score=0.0210
POSITIONAL bphs1-ch32-035 <-> lalkitab-ch27-wave-w27 [positional_alternate_result] score=0.0187
POSITIONAL bphs1-ch32-035 <-> lalkitab-ch27-wave-w35 [positional_alternate_result] score=0.0229
POSITIONAL bphs1-ch32-035 <-> lalkitab-ch27-wave-w47 [positional_alternate_result] score=0.0255
POSITIONAL bphs1-ch32-035 <-> pd-ch08-017 [positional_alternate_result] score=0.1811
POSITIONAL bphs1-ch18-018 <-> R-TBA15-239 [positional_alternate_result] score=0.0512
POSITIONAL bphs1-ch18-018 <-> R-TBA15-240 [positional_alternate_result] score=0.0376
POSITIONAL bphs1-ch18-018 <-> R-TBA15-241 [positional_alternate_result] score=0.0449
POSITIONAL bphs1-ch18-018 <-> R-TBA15-242 [positional_alternate_result] score=0.0216
POSITIONAL bphs1-ch18-018 <-> R-TBA15-243 [positional_alternate_result] score=0.0547
POSITIONAL bphs1-ch18-018 <-> R-TBA15-244 [positional_alternate_result] score=0.0491
POSITIONAL bphs1-ch18-018 <-> R-TBA15-245 [positional_alternate_result] score=0.0493
POSITIONAL bphs1-ch18-018 <-> R-TBA15-246 [positional_alternate_result] score=0.0445
POSITIONAL bphs1-ch18-018 <-> R-TBA15-247 [positional_alternate_result] score=0.0429
POSITIONAL bphs1-ch18-018 <-> R-TBA15-248 [positional_alternate_result] score=0.0484
POSITIONAL bphs1-ch18-018 <-> R-TBA15-249 [positional_alternate_result] score=0.0245
POSITIONAL bphs1-ch18-018 <-> R-TBA15-250 [positional_alternate_result] score=0.0344
POSITIONAL bphs1-ch18-018 <-> R-TBA15-251 [positional_alternate_result] score=0.0350
POSITIONAL bphs1-ch18-018 <-> R-TBA15-252 [positional_alternate_result] score=0.0273
POSITIONAL bphs1-ch18-018 <-> R-TBA15-253 [positional_alternate_result] score=0.0368
POSITIONAL bphs1-ch18-018 <-> R-TBA15-254 [positional_alternate_result] score=0.0365
POSITIONAL bphs1-ch18-018 <-> R-TBA15-255 [positional_alternate_result] score=0.0367
POSITIONAL bphs1-ch18-018 <-> R-TBA15-256 [positional_alternate_result] score=0.0369
POSITIONAL bphs1-ch18-018 <-> R-TBA15-257 [positional_alternate_result] score=0.0311
POSITIONAL bphs1-ch18-018 <-> R-TBA15-258 [positional_alternate_result] score=0.0495
POSITIONAL bphs1-ch18-018 <-> R-TBA15-259 [positional_alternate_result] score=0.0323
POSITIONAL bphs1-ch18-018 <-> R-TBA15-260 [positional_alternate_result] score=0.0413
POSITIONAL bphs1-ch18-018 <-> pd-ch08-018 [positional_polarity_conflict] score=0.1159
POSITIONAL bphs1-ch18-018 <-> pd-ch11-010 [positional_alternate_result] score=0.1438
POSITIONAL bphs1-ch17-031 <-> R-ATEXTB-MOO-6H-CAN-V-017-01 [positional_alternate_result] score=0.0513
POSITIONAL bphs1-ch17-031 <-> R-ATEXTB-MOO-6H-CAP-V-017-02 [positional_alternate_result] score=0.0617
POSITIONAL bphs1-ch17-031 <-> R-ATEXTB-MOO-6H-DEB-V-017-08 [positional_alternate_result] score=0.0244
POSITIONAL bphs1-ch17-031 <-> R-ATEXTB-MOO-6H-EXA-V-017-09 [positional_alternate_result] score=0.0222
POSITIONAL bphs1-ch17-031 <-> R-ATEXTB-MOO-6H-GEM-V-017-03 [positional_alternate_result] score=0.0193
POSITIONAL bphs1-ch17-031 <-> R-ATEXTB-MOO-6H-PIS-V-017-04 [positional_alternate_result] score=0.0195
POSITIONAL bphs1-ch17-031 <-> R-ATEXTB-MOO-6H-SAG-V-017-05 [positional_alternate_result] score=0.0195
POSITIONAL bphs1-ch17-031 <-> R-ATEXTB-MOO-6H-TAU-V-017-06 [positional_alternate_result] score=0.0514
POSITIONAL bphs1-ch17-031 <-> R-ATEXTB-MOO-6H-V-017 [positional_alternate_result] score=0.0848
POSITIONAL bphs1-ch17-031 <-> R-ATEXTB-MOO-6H-VIR-V-017-07 [positional_alternate_result] score=0.0195
POSITIONAL bphs1-ch17-031 <-> R-TBA15-261 [positional_alternate_result] score=0.0532
POSITIONAL bphs1-ch17-031 <-> R-TBA15-262 [positional_alternate_result] score=0.0855
POSITIONAL bphs1-ch17-031 <-> R-TBA15-263 [positional_alternate_result] score=0.0718
POSITIONAL bphs1-ch17-031 <-> R-TBA15-264 [positional_alternate_result] score=0.0960
POSITIONAL bphs1-ch17-031 <-> R-TBA15-265 [positional_alternate_result] score=0.0835
POSITIONAL bphs1-ch17-031 <-> R-TBA15-266 [positional_alternate_result] score=0.0957
POSITIONAL bphs1-ch17-031 <-> R-TBA15-267 [positional_alternate_result] score=0.0995
POSITIONAL bphs1-ch17-031 <-> R-TBA15-268 [positional_alternate_result] score=0.1054
POSITIONAL bphs1-ch17-031 <-> R-TBA15-269 [positional_alternate_result] score=0.1114
POSITIONAL bphs1-ch17-031 <-> R-TBA15-270 [positional_alternate_result] score=0.1116
POSITIONAL bphs1-ch17-031 <-> R-TBA15-271 [positional_alternate_result] score=0.1120
POSITIONAL bphs1-ch17-031 <-> R-TBA15-272 [positional_alternate_result] score=0.1130
POSITIONAL bphs1-ch17-031 <-> R-TBA15-273 [positional_alternate_result] score=0.0881
POSITIONAL bphs1-ch17-031 <-> R-TBA15-274 [positional_alternate_result] score=0.1002
POSITIONAL bphs1-ch17-031 <-> R-TBA15-275 [positional_alternate_result] score=0.1104
POSITIONAL bphs1-ch17-031 <-> R-TBA15-276 [positional_alternate_result] score=0.1374
POSITIONAL bphs1-ch17-031 <-> R-TBA15-277 [positional_alternate_result] score=0.1283
POSITIONAL bphs1-ch17-031 <-> R-TBA15-278 [positional_alternate_result] score=0.0887
POSITIONAL bphs1-ch17-031 <-> R-TBA15-279 [positional_alternate_result] score=0.0751
POSITIONAL bphs1-ch17-031 <-> R-TBA15-280 [positional_alternate_result] score=0.0851
POSITIONAL bphs1-ch17-031 <-> R-TBA15-281 [positional_alternate_result] score=0.0853
POSITIONAL bphs1-ch17-031 <-> lalkitab-ch27-proh-03 [positional_alternate_result] score=0.0486
POSITIONAL bphs1-ch17-031 <-> pd-ch08-019 [positional_alternate_result] score=0.1477
POSITIONAL bphs1-ch18-009 <-> R-ATEXTB-MOO-7H-003 [positional_alternate_result] score=0.2117
POSITIONAL bphs1-ch18-009 <-> R-ATEXTB-MOO-7H-AQU-V-018-01 [positional_alternate_result] score=0.0267
POSITIONAL bphs1-ch18-009 <-> R-ATEXTB-MOO-7H-CAN-V-018-02 [positional_alternate_result] score=0.0101
POSITIONAL bphs1-ch18-009 <-> R-ATEXTB-MOO-7H-DEB-V-018-06 [positional_alternate_result] score=0.0261
POSITIONAL bphs1-ch18-009 <-> R-ATEXTB-MOO-7H-ENE-V-018-07 [positional_alternate_result] score=0.0237
POSITIONAL bphs1-ch18-009 <-> R-ATEXTB-MOO-7H-EXA-V-018-08 [positional_alternate_result] score=0.0225
POSITIONAL bphs1-ch18-009 <-> R-ATEXTB-MOO-7H-PIS-V-018-03 [positional_alternate_result] score=0.0268
POSITIONAL bphs1-ch18-009 <-> R-ATEXTB-MOO-7H-SAG-V-018-04 [positional_alternate_result] score=0.0268
POSITIONAL bphs1-ch18-009 <-> R-ATEXTB-MOO-7H-TAU-V-018-05 [positional_alternate_result] score=0.0268
POSITIONAL bphs1-ch18-009 <-> R-ATEXTB-MOO-7H-V-018 [positional_alternate_result] score=0.0487
POSITIONAL bphs1-ch18-009 <-> R-TBA15-282 [positional_alternate_result] score=0.0259
POSITIONAL bphs1-ch18-009 <-> R-TBA15-283 [positional_alternate_result] score=0.0261
POSITIONAL bphs1-ch18-009 <-> R-TBA15-284 [positional_alternate_result] score=0.0161
POSITIONAL bphs1-ch18-009 <-> R-TBA15-285 [positional_alternate_result] score=0.0188
POSITIONAL bphs1-ch18-009 <-> R-TBA15-286 [positional_alternate_result] score=0.0253
POSITIONAL bphs1-ch18-009 <-> R-TBA15-287 [positional_alternate_result] score=0.0167
POSITIONAL bphs1-ch18-009 <-> R-TBA15-288 [positional_alternate_result] score=0.0242
POSITIONAL bphs1-ch18-009 <-> R-TBA15-289 [positional_alternate_result] score=0.0253
POSITIONAL bphs1-ch18-009 <-> R-TBA15-290 [positional_alternate_result] score=0.0293
POSITIONAL bphs1-ch18-009 <-> R-TBA15-291 [positional_alternate_result] score=0.0211
POSITIONAL bphs1-ch18-009 <-> R-TBA15-292 [positional_alternate_result] score=0.0369
POSITIONAL bphs1-ch18-009 <-> R-TBA15-293 [positional_alternate_result] score=0.0133
POSITIONAL bphs1-ch18-009 <-> R-TBA15-294 [positional_alternate_result] score=0.0226
POSITIONAL bphs1-ch18-009 <-> R-TBA15-295 [positional_alternate_result] score=0.0257
POSITIONAL bphs1-ch18-009 <-> R-TBA15-296 [positional_alternate_result] score=0.0252
POSITIONAL bphs1-ch18-009 <-> R-TBA15-297 [positional_alternate_result] score=0.0253
POSITIONAL bphs1-ch18-009 <-> R-TBA15-298 [positional_alternate_result] score=0.0255
POSITIONAL bphs1-ch18-009 <-> R-TBA15-299 [positional_alternate_result] score=0.0298
POSITIONAL bphs1-ch18-009 <-> R-TBA15-300 [positional_alternate_result] score=0.0261
POSITIONAL bphs1-ch18-009 <-> R-TBA15-301 [positional_alternate_result] score=0.0485
POSITIONAL bphs1-ch18-009 <-> R-TBA15-302 [positional_alternate_result] score=0.0399
POSITIONAL bphs1-ch18-009 <-> R-TBA15-303 [positional_alternate_result] score=0.0488
POSITIONAL bphs1-ch18-009 <-> pd-ch08-020 [positional_alternate_result] score=0.1190
POSITIONAL bphs1-ch18-025 <-> R-ATEXTB-MOO-7H-003 [positional_alternate_result] score=0.1528
POSITIONAL bphs1-ch18-025 <-> R-ATEXTB-MOO-7H-AQU-V-018-01 [positional_alternate_result] score=0.0228
POSITIONAL bphs1-ch18-025 <-> R-ATEXTB-MOO-7H-CAN-V-018-02 [positional_alternate_result] score=0.0162
POSITIONAL bphs1-ch18-025 <-> R-ATEXTB-MOO-7H-DEB-V-018-06 [positional_alternate_result] score=0.0329
POSITIONAL bphs1-ch18-025 <-> R-ATEXTB-MOO-7H-ENE-V-018-07 [positional_alternate_result] score=0.0335
POSITIONAL bphs1-ch18-025 <-> R-ATEXTB-MOO-7H-EXA-V-018-08 [positional_alternate_result] score=0.0268
POSITIONAL bphs1-ch18-025 <-> R-ATEXTB-MOO-7H-PIS-V-018-03 [positional_alternate_result] score=0.0229
POSITIONAL bphs1-ch18-025 <-> R-ATEXTB-MOO-7H-SAG-V-018-04 [positional_alternate_result] score=0.0229
POSITIONAL bphs1-ch18-025 <-> R-ATEXTB-MOO-7H-TAU-V-018-05 [positional_alternate_result] score=0.0221
POSITIONAL bphs1-ch18-025 <-> R-ATEXTB-MOO-7H-V-018 [positional_alternate_result] score=0.0675
POSITIONAL bphs1-ch18-025 <-> R-TBA15-282 [positional_alternate_result] score=0.0252
POSITIONAL bphs1-ch18-025 <-> R-TBA15-283 [positional_alternate_result] score=0.0426
POSITIONAL bphs1-ch18-025 <-> R-TBA15-284 [positional_alternate_result] score=0.0353
POSITIONAL bphs1-ch18-025 <-> R-TBA15-285 [positional_alternate_result] score=0.0254
POSITIONAL bphs1-ch18-025 <-> R-TBA15-286 [positional_alternate_result] score=0.0303
POSITIONAL bphs1-ch18-025 <-> R-TBA15-287 [positional_alternate_result] score=0.0291
POSITIONAL bphs1-ch18-025 <-> R-TBA15-288 [positional_alternate_result] score=0.0342
POSITIONAL bphs1-ch18-025 <-> R-TBA15-289 [positional_alternate_result] score=0.0317
POSITIONAL bphs1-ch18-025 <-> R-TBA15-290 [positional_alternate_result] score=0.0269
POSITIONAL bphs1-ch18-025 <-> R-TBA15-291 [positional_alternate_result] score=0.0253
POSITIONAL bphs1-ch18-025 <-> R-TBA15-292 [positional_alternate_result] score=0.0316
POSITIONAL bphs1-ch18-025 <-> R-TBA15-293 [positional_alternate_result] score=0.0545
POSITIONAL bphs1-ch18-025 <-> R-TBA15-294 [positional_alternate_result] score=0.0309
POSITIONAL bphs1-ch18-025 <-> R-TBA15-295 [positional_alternate_result] score=0.0321
POSITIONAL bphs1-ch18-025 <-> R-TBA15-296 [positional_alternate_result] score=0.0315
POSITIONAL bphs1-ch18-025 <-> R-TBA15-297 [positional_alternate_result] score=0.0316
POSITIONAL bphs1-ch18-025 <-> R-TBA15-298 [positional_alternate_result] score=0.0319
POSITIONAL bphs1-ch18-025 <-> R-TBA15-299 [positional_alternate_result] score=0.0255
POSITIONAL bphs1-ch18-025 <-> R-TBA15-300 [positional_alternate_result] score=0.0314
POSITIONAL bphs1-ch18-025 <-> R-TBA15-301 [positional_alternate_result] score=0.0307
POSITIONAL bphs1-ch18-025 <-> R-TBA15-302 [positional_alternate_result] score=0.0721
POSITIONAL bphs1-ch18-025 <-> R-TBA15-303 [positional_alternate_result] score=0.0765
POSITIONAL bphs1-ch18-025 <-> pd-ch08-020 [positional_polarity_conflict] score=0.0908
POSITIONAL bphs1-ch16-016 <-> R-ATEXTB-MOO-8H-CAN-V-019-01 [positional_alternate_result] score=0.0230
POSITIONAL bphs1-ch16-016 <-> R-ATEXTB-MOO-8H-EXA-V-019-03 [positional_alternate_result] score=0.1043
POSITIONAL bphs1-ch16-016 <-> R-ATEXTB-MOO-8H-OWN-V-019-04 [positional_alternate_result] score=0.1043
POSITIONAL bphs1-ch16-016 <-> R-ATEXTB-MOO-8H-TAU-V-019-02 [positional_alternate_result] score=0.0230
POSITIONAL bphs1-ch16-016 <-> R-ATEXTB-MOO-8H-V-019 [positional_alternate_result] score=0.0797
POSITIONAL bphs1-ch16-016 <-> R-TBA15-304 [positional_alternate_result] score=0.0372
POSITIONAL bphs1-ch16-016 <-> R-TBA15-305 [positional_alternate_result] score=0.0588
POSITIONAL bphs1-ch16-016 <-> R-TBA15-306 [positional_alternate_result] score=0.0627
POSITIONAL bphs1-ch16-016 <-> R-TBA15-307 [positional_alternate_result] score=0.0730
POSITIONAL bphs1-ch16-016 <-> R-TBA15-308 [positional_alternate_result] score=0.0371
POSITIONAL bphs1-ch16-016 <-> R-TBA15-309 [positional_alternate_result] score=0.0531
POSITIONAL bphs1-ch16-016 <-> R-TBA15-310 [positional_alternate_result] score=0.0532
POSITIONAL bphs1-ch16-016 <-> R-TBA15-311 [positional_alternate_result] score=0.0496
POSITIONAL bphs1-ch16-016 <-> R-TBA15-312 [positional_alternate_result] score=0.0623
POSITIONAL bphs1-ch16-016 <-> R-TBA15-313 [positional_alternate_result] score=0.0751
POSITIONAL bphs1-ch16-016 <-> R-TBA15-314 [positional_alternate_result] score=0.0645
POSITIONAL bphs1-ch16-016 <-> R-TBA15-315 [positional_alternate_result] score=0.0582
POSITIONAL bphs1-ch16-016 <-> R-TBA15-316 [positional_alternate_result] score=0.0558
POSITIONAL bphs1-ch16-016 <-> R-TBA15-317 [positional_alternate_result] score=0.0364
POSITIONAL bphs1-ch16-016 <-> R-TBA15-318 [positional_alternate_result] score=0.0661
POSITIONAL bphs1-ch16-016 <-> R-TBA15-319 [positional_alternate_result] score=0.0713
POSITIONAL bphs1-ch16-016 <-> R-TBA15-320 [positional_alternate_result] score=0.0852
POSITIONAL bphs1-ch16-016 <-> pd-ch08-021 [positional_alternate_result] score=0.1261
POSITIONAL bphs1-ch17-015 <-> R-ATEXTB-RAH-1H-AQU-V-082-01 [positional_alternate_result] score=0.0189
POSITIONAL bphs1-ch17-015 <-> R-ATEXTB-RAH-1H-ARI-V-082-02 [positional_alternate_result] score=0.0187
POSITIONAL bphs1-ch17-015 <-> R-ATEXTB-RAH-1H-CAN-V-082-03 [positional_alternate_result] score=0.0182
POSITIONAL bphs1-ch17-015 <-> R-ATEXTB-RAH-1H-CAP-V-082-04 [positional_alternate_result] score=0.0190
POSITIONAL bphs1-ch17-015 <-> R-ATEXTB-RAH-1H-GEM-V-082-05 [positional_alternate_result] score=0.0164
POSITIONAL bphs1-ch17-015 <-> R-ATEXTB-RAH-1H-LEO-V-082-06 [positional_alternate_result] score=0.0189
POSITIONAL bphs1-ch17-015 <-> R-ATEXTB-RAH-1H-PIS-V-082-07 [positional_alternate_result] score=0.0189
POSITIONAL bphs1-ch17-015 <-> R-ATEXTB-RAH-1H-SCO-V-082-08 [positional_alternate_result] score=0.0191
POSITIONAL bphs1-ch17-015 <-> R-ATEXTB-RAH-1H-TAU-V-082-09 [positional_alternate_result] score=0.0164
POSITIONAL bphs1-ch17-015 <-> R-ATEXTB-RAH-1H-V-082 [positional_alternate_result] score=0.0235
POSITIONAL bphs1-ch17-015 <-> R-ATEXTB-RAH-1H-VIR-V-082-10 [positional_alternate_result] score=0.0164
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1189 [positional_alternate_result] score=0.0286
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1190 [positional_alternate_result] score=0.0420
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1191 [positional_alternate_result] score=0.0419
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1192 [positional_alternate_result] score=0.0420
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1193 [positional_alternate_result] score=0.0403
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1194 [positional_alternate_result] score=0.0454
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1195 [positional_alternate_result] score=0.0452
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1196 [positional_alternate_result] score=0.0456
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1197 [positional_alternate_result] score=0.0450
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1198 [positional_alternate_result] score=0.0452
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1199 [positional_alternate_result] score=0.0456
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1200 [positional_alternate_result] score=0.0454
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1201 [positional_alternate_result] score=0.0457
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1202 [positional_alternate_result] score=0.0360
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1203 [positional_alternate_result] score=0.0480
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1204 [positional_alternate_result] score=0.0478
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1205 [positional_alternate_result] score=0.0475
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1206 [positional_alternate_result] score=0.0476
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1207 [positional_alternate_result] score=0.0476
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1208 [positional_alternate_result] score=0.0415
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1209 [positional_alternate_result] score=0.0395
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1210 [positional_alternate_result] score=0.0823
POSITIONAL bphs1-ch17-015 <-> R-TBA15-1211 [positional_alternate_result] score=0.0200
POSITIONAL bphs1-ch17-015 <-> pd-ch02-010 [positional_alternate_result] score=0.0627
POSITIONAL bphs1-ch17-015 <-> pd-ch02-011 [positional_alternate_result] score=0.0718
POSITIONAL bphs1-ch17-015 <-> pd-ch02-012 [positional_alternate_result] score=0.0510
POSITIONAL bphs1-ch17-015 <-> pd-ch02-013 [positional_alternate_result] score=0.1096
POSITIONAL bphs1-ch17-015 <-> pd-ch08-087 [positional_alternate_result] score=0.0684
POSITIONAL bphs1-ch18-045 <-> R-ATEXTB-RAH-2H-DEB-V-083-02 [positional_alternate_result] score=0.0206
POSITIONAL bphs1-ch18-045 <-> R-ATEXTB-RAH-2H-LIB-V-083-01 [positional_alternate_result] score=0.0280
POSITIONAL bphs1-ch18-045 <-> R-ATEXTB-RAH-2H-V-083 [positional_alternate_result] score=0.0383
POSITIONAL bphs1-ch18-045 <-> R-TBA15-1212 [positional_alternate_result] score=0.0447
POSITIONAL bphs1-ch18-045 <-> R-TBA15-1213 [positional_alternate_result] score=0.0457
POSITIONAL bphs1-ch18-045 <-> R-TBA15-1214 [positional_alternate_result] score=0.0655
POSITIONAL bphs1-ch18-045 <-> R-TBA15-1215 [positional_alternate_result] score=0.0568
POSITIONAL bphs1-ch18-045 <-> R-TBA15-1216 [positional_alternate_result] score=0.0387
POSITIONAL bphs1-ch18-045 <-> pd-ch08-088 [positional_alternate_result] score=0.0831
POSITIONAL bphs1-ch16-022 <-> R-300IMP-RAH-5H-088 [positional_alternate_result] score=0.0637
POSITIONAL bphs1-ch16-022 <-> R-ATEXTB-RAH-5H-ARI-V-086-01 [positional_alternate_result] score=0.0288
POSITIONAL bphs1-ch16-022 <-> R-ATEXTB-RAH-5H-CAN-V-086-02 [positional_alternate_result] score=0.0287
POSITIONAL bphs1-ch16-022 <-> R-ATEXTB-RAH-5H-TAU-V-086-03 [positional_alternate_result] score=0.0287
POSITIONAL bphs1-ch16-022 <-> R-ATEXTB-RAH-5H-V-086 [positional_alternate_result] score=0.0215
POSITIONAL bphs1-ch16-022 <-> R-TBA15-1242 [positional_alternate_result] score=0.0327
POSITIONAL bphs1-ch16-022 <-> R-TBA15-1243 [positional_alternate_result] score=0.0829
POSITIONAL bphs1-ch16-022 <-> R-TBA15-1244 [positional_alternate_result] score=0.0830
POSITIONAL bphs1-ch16-022 <-> R-TBA15-1245 [positional_alternate_result] score=0.0826
POSITIONAL bphs1-ch16-022 <-> R-TBA15-1246 [positional_alternate_result] score=0.0825
POSITIONAL bphs1-ch16-022 <-> R-TBA15-1247 [positional_alternate_result] score=0.0726
POSITIONAL bphs1-ch16-022 <-> R-TBA15-1248 [positional_alternate_result] score=0.0424
POSITIONAL bphs1-ch16-022 <-> R-TBA15-1249 [positional_alternate_result] score=0.0670
POSITIONAL bphs1-ch16-022 <-> pd-ch08-091 [positional_alternate_result] score=0.0912
POSITIONAL bphs1-ch17-021 <-> R-ATEXTB-RAH-6H-EXA-V-087-01 [positional_alternate_result] score=0.0160
POSITIONAL bphs1-ch17-021 <-> R-ATEXTB-RAH-6H-V-087 [positional_alternate_result] score=0.0115
POSITIONAL bphs1-ch17-021 <-> R-BRIHAT-RAH-6H-090 [positional_alternate_result] score=0.1348
POSITIONAL bphs1-ch17-021 <-> R-TBA15-1250 [positional_alternate_result] score=0.0232
POSITIONAL bphs1-ch17-021 <-> R-TBA15-1251 [positional_alternate_result] score=0.0705
POSITIONAL bphs1-ch17-021 <-> R-TBA15-1252 [positional_alternate_result] score=0.0790
POSITIONAL bphs1-ch17-021 <-> R-TBA15-1253 [positional_alternate_result] score=0.0469
POSITIONAL bphs1-ch17-021 <-> pd-ch08-092 [positional_alternate_result] score=0.1554
POSITIONAL bphs1-ch17-026 <-> R-ATEXTB-RAH-6H-EXA-V-087-01 [positional_alternate_result] score=0.0228
POSITIONAL bphs1-ch17-026 <-> R-ATEXTB-RAH-6H-V-087 [positional_alternate_result] score=0.0206
POSITIONAL bphs1-ch17-026 <-> R-BRIHAT-RAH-6H-090 [positional_alternate_result] score=0.1636
POSITIONAL bphs1-ch17-026 <-> R-TBA15-1250 [positional_alternate_result] score=0.0364
POSITIONAL bphs1-ch17-026 <-> R-TBA15-1251 [positional_alternate_result] score=0.0694
POSITIONAL bphs1-ch17-026 <-> R-TBA15-1252 [positional_alternate_result] score=0.0822
POSITIONAL bphs1-ch17-026 <-> R-TBA15-1253 [positional_alternate_result] score=0.0513
POSITIONAL bphs1-ch17-026 <-> pd-ch08-092 [positional_alternate_result] score=0.0949
POSITIONAL bphs1-ch12-013 <-> R-ATEXTB-SAT-1H-AQU-V-071-01 [positional_alternate_result] score=0.0229
POSITIONAL bphs1-ch12-013 <-> R-ATEXTB-SAT-1H-ARI-V-071-02 [positional_alternate_result] score=0.0725
POSITIONAL bphs1-ch12-013 <-> R-ATEXTB-SAT-1H-CAN-V-071-03 [positional_alternate_result] score=0.0609
POSITIONAL bphs1-ch12-013 <-> R-ATEXTB-SAT-1H-CAP-V-071-04 [positional_alternate_result] score=0.0216
POSITIONAL bphs1-ch12-013 <-> R-ATEXTB-SAT-1H-ENE-V-071-12 [positional_alternate_result] score=0.0189
POSITIONAL bphs1-ch12-013 <-> R-ATEXTB-SAT-1H-EXA-V-071-13 [positional_alternate_result] score=0.0282
POSITIONAL bphs1-ch12-013 <-> R-ATEXTB-SAT-1H-GEM-V-071-05 [positional_alternate_result] score=0.0661
POSITIONAL bphs1-ch12-013 <-> R-ATEXTB-SAT-1H-LEO-V-071-06 [positional_alternate_result] score=0.0757
POSITIONAL bphs1-ch12-013 <-> R-ATEXTB-SAT-1H-OWN-V-071-14 [positional_alternate_result] score=0.0296
POSITIONAL bphs1-ch12-013 <-> R-ATEXTB-SAT-1H-PIS-V-071-07 [positional_alternate_result] score=0.0306
POSITIONAL bphs1-ch12-013 <-> R-ATEXTB-SAT-1H-SAG-V-071-08 [positional_alternate_result] score=0.0306
POSITIONAL bphs1-ch12-013 <-> R-ATEXTB-SAT-1H-SCO-V-071-09 [positional_alternate_result] score=0.0571
POSITIONAL bphs1-ch12-013 <-> R-ATEXTB-SAT-1H-TAU-V-071-10 [positional_alternate_result] score=0.0749
POSITIONAL bphs1-ch12-013 <-> R-ATEXTB-SAT-1H-V-071 [positional_alternate_result] score=0.0696
POSITIONAL bphs1-ch12-013 <-> R-ATEXTB-SAT-1H-VIR-V-071-11 [positional_alternate_result] score=0.0504
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1015 [positional_alternate_result] score=0.0238
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1016 [positional_alternate_result] score=0.0294
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1017 [positional_alternate_result] score=0.0261
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1018 [positional_alternate_result] score=0.0262
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1019 [positional_alternate_result] score=0.0262
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1020 [positional_alternate_result] score=0.0261
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1021 [positional_alternate_result] score=0.0263
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1022 [positional_alternate_result] score=0.0767
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1023 [positional_alternate_result] score=0.0449
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1024 [positional_alternate_result] score=0.0450
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1025 [positional_alternate_result] score=0.0332
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1026 [positional_alternate_result] score=0.0336
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1027 [positional_alternate_result] score=0.0464
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1028 [positional_alternate_result] score=0.0336
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1029 [positional_alternate_result] score=0.0297
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1030 [positional_alternate_result] score=0.0370
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1031 [positional_alternate_result] score=0.0302
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1032 [positional_alternate_result] score=0.0303
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1033 [positional_alternate_result] score=0.0324
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1034 [positional_alternate_result] score=0.0229
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1035 [positional_alternate_result] score=0.0289
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1036 [positional_alternate_result] score=0.0343
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1037 [positional_alternate_result] score=0.0492
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1038 [positional_alternate_result] score=0.0316
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1039 [positional_alternate_result] score=0.0291
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1040 [positional_alternate_result] score=0.0348
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1041 [positional_alternate_result] score=0.0273
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1042 [positional_alternate_result] score=0.0428
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1043 [positional_alternate_result] score=0.0334
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1044 [positional_alternate_result] score=0.0180
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1045 [positional_alternate_result] score=0.0322
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1046 [positional_alternate_result] score=0.0352
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1047 [positional_alternate_result] score=0.0305
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1048 [positional_alternate_result] score=0.0304
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1049 [positional_alternate_result] score=0.0305
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1050 [positional_alternate_result] score=0.0369
POSITIONAL bphs1-ch12-013 <-> R-TBA15-1051 [positional_alternate_result] score=0.0402
POSITIONAL bphs1-ch12-013 <-> lalkitab-ch27-wave-w44 [positional_alternate_result] score=0.0159
POSITIONAL bphs1-ch12-013 <-> pd-ch08-074 [positional_alternate_result] score=0.0692
POSITIONAL bphs1-ch12-013 <-> pd-ch08-075 [positional_alternate_result] score=0.0548
POSITIONAL bphs1-ch17-014 <-> R-ATEXTB-SAT-1H-AQU-V-071-01 [positional_alternate_result] score=0.0112
POSITIONAL bphs1-ch17-014 <-> R-ATEXTB-SAT-1H-ARI-V-071-02 [positional_alternate_result] score=0.0148
POSITIONAL bphs1-ch17-014 <-> R-ATEXTB-SAT-1H-CAN-V-071-03 [positional_alternate_result] score=0.0120
POSITIONAL bphs1-ch17-014 <-> R-ATEXTB-SAT-1H-CAP-V-071-04 [positional_alternate_result] score=0.0121
POSITIONAL bphs1-ch17-014 <-> R-ATEXTB-SAT-1H-ENE-V-071-12 [positional_alternate_result] score=0.0181
POSITIONAL bphs1-ch17-014 <-> R-ATEXTB-SAT-1H-EXA-V-071-13 [positional_alternate_result] score=0.0080
POSITIONAL bphs1-ch17-014 <-> R-ATEXTB-SAT-1H-GEM-V-071-05 [positional_alternate_result] score=0.0149
POSITIONAL bphs1-ch17-014 <-> R-ATEXTB-SAT-1H-LEO-V-071-06 [positional_alternate_result] score=0.0148
POSITIONAL bphs1-ch17-014 <-> R-ATEXTB-SAT-1H-OWN-V-071-14 [positional_alternate_result] score=0.0083
POSITIONAL bphs1-ch17-014 <-> R-ATEXTB-SAT-1H-PIS-V-071-07 [positional_alternate_result] score=0.0105
POSITIONAL bphs1-ch17-014 <-> R-ATEXTB-SAT-1H-SAG-V-071-08 [positional_alternate_result] score=0.0105
POSITIONAL bphs1-ch17-014 <-> R-ATEXTB-SAT-1H-SCO-V-071-09 [positional_alternate_result] score=0.0145
POSITIONAL bphs1-ch17-014 <-> R-ATEXTB-SAT-1H-TAU-V-071-10 [positional_alternate_result] score=0.0149
POSITIONAL bphs1-ch17-014 <-> R-ATEXTB-SAT-1H-V-071 [positional_alternate_result] score=0.0131
POSITIONAL bphs1-ch17-014 <-> R-ATEXTB-SAT-1H-VIR-V-071-11 [positional_alternate_result] score=0.0101
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1015 [positional_alternate_result] score=0.0160
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1016 [positional_alternate_result] score=0.0242
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1017 [positional_alternate_result] score=0.0273
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1018 [positional_alternate_result] score=0.0274
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1019 [positional_alternate_result] score=0.0274
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1020 [positional_alternate_result] score=0.0273
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1021 [positional_alternate_result] score=0.0275
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1022 [positional_alternate_result] score=0.0301
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1023 [positional_alternate_result] score=0.0400
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1024 [positional_alternate_result] score=0.0398
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1025 [positional_alternate_result] score=0.0396
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1026 [positional_alternate_result] score=0.0399
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1027 [positional_alternate_result] score=0.0394
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1028 [positional_alternate_result] score=0.0400
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1029 [positional_alternate_result] score=0.0353
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1030 [positional_alternate_result] score=0.0353
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1031 [positional_alternate_result] score=0.0373
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1032 [positional_alternate_result] score=0.0376
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1033 [positional_alternate_result] score=0.0383
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1034 [positional_alternate_result] score=0.0232
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1035 [positional_alternate_result] score=0.0303
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1036 [positional_alternate_result] score=0.0312
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1037 [positional_alternate_result] score=0.0356
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1038 [positional_alternate_result] score=0.0408
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1039 [positional_alternate_result] score=0.0346
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1040 [positional_alternate_result] score=0.0371
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1041 [positional_alternate_result] score=0.0400
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1042 [positional_alternate_result] score=0.0367
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1043 [positional_alternate_result] score=0.0302
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1044 [positional_alternate_result] score=0.0164
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1045 [positional_alternate_result] score=0.0381
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1046 [positional_alternate_result] score=0.0294
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1047 [positional_alternate_result] score=0.0320
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1048 [positional_alternate_result] score=0.0319
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1049 [positional_alternate_result] score=0.0320
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1050 [positional_alternate_result] score=0.0348
POSITIONAL bphs1-ch17-014 <-> R-TBA15-1051 [positional_alternate_result] score=0.0280
POSITIONAL bphs1-ch17-014 <-> lalkitab-ch27-wave-w44 [positional_alternate_result] score=0.0193
POSITIONAL bphs1-ch17-014 <-> pd-ch08-074 [positional_polarity_conflict] score=0.0267
POSITIONAL bphs1-ch17-014 <-> pd-ch08-075 [positional_alternate_result] score=0.0292
POSITIONAL bphs1-ch32-043 <-> R-ATEXTB-SAT-12H-EXA-V-081-01 [positional_alternate_result] score=0.0768
POSITIONAL bphs1-ch32-043 <-> R-ATEXTB-SAT-12H-V-081 [positional_alternate_result] score=0.0442
POSITIONAL bphs1-ch32-043 <-> R-TBA15-1180 [positional_alternate_result] score=0.0641
POSITIONAL bphs1-ch32-043 <-> R-TBA15-1181 [positional_alternate_result] score=0.1575
POSITIONAL bphs1-ch32-043 <-> R-TBA15-1182 [positional_alternate_result] score=0.1317
POSITIONAL bphs1-ch32-043 <-> R-TBA15-1183 [positional_alternate_result] score=0.1333
POSITIONAL bphs1-ch32-043 <-> R-TBA15-1184 [positional_alternate_result] score=0.1518
POSITIONAL bphs1-ch32-043 <-> R-TBA15-1185 [positional_alternate_result] score=0.1412
POSITIONAL bphs1-ch32-043 <-> R-TBA15-1186 [positional_alternate_result] score=0.1070
POSITIONAL bphs1-ch32-043 <-> R-TBA15-1187 [positional_alternate_result] score=0.1151
POSITIONAL bphs1-ch32-043 <-> R-TBA15-1188 [positional_alternate_result] score=0.0685
POSITIONAL bphs1-ch32-043 <-> pd-ch08-086 [positional_alternate_result] score=0.0919
POSITIONAL bphs1-ch42-019 <-> R-ATEXTB-SAT-2H-V-072 [positional_alternate_result] score=0.0050
POSITIONAL bphs1-ch42-019 <-> R-BRIHAT-SAT-2H-257 [positional_polarity_conflict] score=0.0475
POSITIONAL bphs1-ch42-019 <-> R-TBA15-1052 [positional_alternate_result] score=0.0134
POSITIONAL bphs1-ch42-019 <-> R-TBA15-1053 [positional_alternate_result] score=0.0567
POSITIONAL bphs1-ch42-019 <-> R-TBA15-1054 [positional_alternate_result] score=0.0611
POSITIONAL bphs1-ch42-019 <-> R-TBA15-1055 [positional_alternate_result] score=0.0777
POSITIONAL bphs1-ch42-019 <-> R-TBA15-1056 [positional_alternate_result] score=0.0519
POSITIONAL bphs1-ch42-019 <-> R-TBA15-1057 [positional_alternate_result] score=0.0370
POSITIONAL bphs1-ch42-019 <-> R-TBA15-1058 [positional_alternate_result] score=0.0650
POSITIONAL bphs1-ch42-019 <-> R-TBA15-1059 [positional_alternate_result] score=0.0511
POSITIONAL bphs1-ch42-019 <-> R-TBA15-1060 [positional_alternate_result] score=0.0449
POSITIONAL bphs1-ch42-019 <-> R-TBA15-1061 [positional_alternate_result] score=0.0361
POSITIONAL bphs1-ch42-019 <-> pd-ch08-076 [positional_alternate_result] score=0.0338
POSITIONAL bphs1-ch14-016 <-> R-ATEXTB-SAT-3H-AQU-V-073-01 [positional_alternate_result] score=0.0254
POSITIONAL bphs1-ch14-016 <-> R-ATEXTB-SAT-3H-ARI-V-073-02 [positional_alternate_result] score=0.0301
POSITIONAL bphs1-ch14-016 <-> R-ATEXTB-SAT-3H-CAP-V-073-03 [positional_alternate_result] score=0.0255
POSITIONAL bphs1-ch14-016 <-> R-ATEXTB-SAT-3H-DEB-V-073-05 [positional_alternate_result] score=0.0214
POSITIONAL bphs1-ch14-016 <-> R-ATEXTB-SAT-3H-EXA-V-073-06 [positional_alternate_result] score=0.0344
POSITIONAL bphs1-ch14-016 <-> R-ATEXTB-SAT-3H-LIB-V-073-04 [positional_alternate_result] score=0.0252
POSITIONAL bphs1-ch14-016 <-> R-ATEXTB-SAT-3H-OWN-V-073-07 [positional_alternate_result] score=0.0344
POSITIONAL bphs1-ch14-016 <-> R-ATEXTB-SAT-3H-V-073 [positional_alternate_result] score=0.0320
POSITIONAL bphs1-ch14-016 <-> R-TBA15-1062 [positional_alternate_result] score=0.0189
POSITIONAL bphs1-ch14-016 <-> R-TBA15-1063 [positional_alternate_result] score=0.1208
POSITIONAL bphs1-ch14-016 <-> R-TBA15-1064 [positional_alternate_result] score=0.1167
POSITIONAL bphs1-ch14-016 <-> R-TBA15-1065 [positional_alternate_result] score=0.1208
POSITIONAL bphs1-ch14-016 <-> R-TBA15-1066 [positional_alternate_result] score=0.0814
POSITIONAL bphs1-ch14-016 <-> R-TBA15-1067 [positional_alternate_result] score=0.0796
POSITIONAL bphs1-ch14-016 <-> R-TBA15-1068 [positional_alternate_result] score=0.0919
POSITIONAL bphs1-ch14-016 <-> R-TBA15-1069 [positional_alternate_result] score=0.1013
POSITIONAL bphs1-ch14-016 <-> R-TBA15-1070 [positional_alternate_result] score=0.1023
POSITIONAL bphs1-ch14-016 <-> R-TBA15-1071 [positional_alternate_result] score=0.1019
POSITIONAL bphs1-ch14-016 <-> R-TBA15-1072 [positional_alternate_result] score=0.1005
POSITIONAL bphs1-ch14-016 <-> R-TBA15-1073 [positional_alternate_result] score=0.0878
POSITIONAL bphs1-ch14-016 <-> R-TBA15-1074 [positional_alternate_result] score=0.1189
POSITIONAL bphs1-ch14-016 <-> R-TBA15-1075 [positional_alternate_result] score=0.1089
POSITIONAL bphs1-ch14-016 <-> R-TBA15-1076 [positional_alternate_result] score=0.0830
POSITIONAL bphs1-ch14-016 <-> R-TBA15-1077 [positional_alternate_result] score=0.0281
POSITIONAL bphs1-ch14-016 <-> pd-ch08-077 [positional_alternate_result] score=0.0570
POSITIONAL bphs1-ch17-023 <-> R-300IMP-SAT-6H-121 [positional_alternate_result] score=0.0693
POSITIONAL bphs1-ch17-023 <-> R-ATEXTB-SAT-6H-DEB-V-076-08 [positional_alternate_result] score=0.0126
POSITIONAL bphs1-ch17-023 <-> R-ATEXTB-SAT-6H-ENE-V-076-09 [positional_alternate_result] score=0.0228
POSITIONAL bphs1-ch17-023 <-> R-ATEXTB-SAT-6H-EXA-V-076-10 [positional_alternate_result] score=0.0197
POSITIONAL bphs1-ch17-023 <-> R-ATEXTB-SAT-6H-GEM-V-076-01 [positional_alternate_result] score=0.0183
POSITIONAL bphs1-ch17-023 <-> R-ATEXTB-SAT-6H-LEO-V-076-02 [positional_alternate_result] score=0.0149
POSITIONAL bphs1-ch17-023 <-> R-ATEXTB-SAT-6H-PIS-V-076-03 [positional_alternate_result] score=0.0183
POSITIONAL bphs1-ch17-023 <-> R-ATEXTB-SAT-6H-SAG-V-076-04 [positional_alternate_result] score=0.0183
POSITIONAL bphs1-ch17-023 <-> R-ATEXTB-SAT-6H-SCO-V-076-05 [positional_alternate_result] score=0.0150
POSITIONAL bphs1-ch17-023 <-> R-ATEXTB-SAT-6H-TAU-V-076-06 [positional_alternate_result] score=0.0149
POSITIONAL bphs1-ch17-023 <-> R-ATEXTB-SAT-6H-V-076 [positional_alternate_result] score=0.0229
POSITIONAL bphs1-ch17-023 <-> R-ATEXTB-SAT-6H-VIR-V-076-07 [positional_alternate_result] score=0.0183
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1101 [positional_alternate_result] score=0.0339
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1102 [positional_alternate_result] score=0.0651
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1103 [positional_alternate_result] score=0.0568
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1104 [positional_alternate_result] score=0.0682
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1105 [positional_alternate_result] score=0.0745
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1106 [positional_alternate_result] score=0.0408
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1107 [positional_alternate_result] score=0.0810
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1108 [positional_alternate_result] score=0.0625
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1109 [positional_alternate_result] score=0.0621
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1110 [positional_alternate_result] score=0.0627
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1111 [positional_alternate_result] score=0.0574
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1112 [positional_alternate_result] score=0.0793
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1113 [positional_alternate_result] score=0.0794
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1114 [positional_alternate_result] score=0.0796
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1115 [positional_alternate_result] score=0.0802
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1116 [positional_alternate_result] score=0.0680
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1117 [positional_alternate_result] score=0.0652
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1118 [positional_alternate_result] score=0.0647
POSITIONAL bphs1-ch17-023 <-> R-TBA15-1119 [positional_alternate_result] score=0.0397
POSITIONAL bphs1-ch17-023 <-> pd-ch08-080 [positional_alternate_result] score=0.0602
POSITIONAL bphs1-ch18-013 <-> R-ATEXTB-SAT-7H-AQU-V-077-01 [positional_alternate_result] score=0.0204
POSITIONAL bphs1-ch18-013 <-> R-ATEXTB-SAT-7H-CAP-V-077-02 [positional_alternate_result] score=0.0205
POSITIONAL bphs1-ch18-013 <-> R-ATEXTB-SAT-7H-EXA-V-077-09 [positional_alternate_result] score=0.0175
POSITIONAL bphs1-ch18-013 <-> R-ATEXTB-SAT-7H-GEM-V-077-03 [positional_alternate_result] score=0.0193
POSITIONAL bphs1-ch18-013 <-> R-ATEXTB-SAT-7H-LIB-V-077-04 [positional_alternate_result] score=0.0204
POSITIONAL bphs1-ch18-013 <-> R-ATEXTB-SAT-7H-OWN-V-077-10 [positional_alternate_result] score=0.0175
POSITIONAL bphs1-ch18-013 <-> R-ATEXTB-SAT-7H-PIS-V-077-05 [positional_alternate_result] score=0.0159
POSITIONAL bphs1-ch18-013 <-> R-ATEXTB-SAT-7H-SAG-V-077-06 [positional_alternate_result] score=0.0149
POSITIONAL bphs1-ch18-013 <-> R-ATEXTB-SAT-7H-SCO-V-077-07 [positional_alternate_result] score=0.0200
POSITIONAL bphs1-ch18-013 <-> R-ATEXTB-SAT-7H-V-077 [positional_alternate_result] score=0.0277
POSITIONAL bphs1-ch18-013 <-> R-ATEXTB-SAT-7H-VIR-V-077-08 [positional_alternate_result] score=0.0193
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1120 [positional_alternate_result] score=0.0298
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1121 [positional_alternate_result] score=0.0625
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1122 [positional_alternate_result] score=0.0544
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1123 [positional_alternate_result] score=0.0592
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1124 [positional_alternate_result] score=0.0592
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1125 [positional_alternate_result] score=0.0594
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1126 [positional_alternate_result] score=0.0599
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1127 [positional_alternate_result] score=0.0556
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1128 [positional_alternate_result] score=0.0439
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1129 [positional_alternate_result] score=0.0442
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1130 [positional_alternate_result] score=0.0441
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1131 [positional_alternate_result] score=0.0415
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1132 [positional_alternate_result] score=0.0483
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1133 [positional_alternate_result] score=0.0687
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1134 [positional_alternate_result] score=0.0661
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1135 [positional_alternate_result] score=0.0658
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1136 [positional_alternate_result] score=0.0617
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1137 [positional_alternate_result] score=0.0253
POSITIONAL bphs1-ch18-013 <-> R-TBA15-1138 [positional_alternate_result] score=0.0595
POSITIONAL bphs1-ch18-013 <-> pd-ch08-081 [positional_alternate_result] score=0.0648
POSITIONAL bphs1-ch18-015 <-> R-ATEXTB-SAT-7H-AQU-V-077-01 [positional_alternate_result] score=0.0303
POSITIONAL bphs1-ch18-015 <-> R-ATEXTB-SAT-7H-CAP-V-077-02 [positional_alternate_result] score=0.0305
POSITIONAL bphs1-ch18-015 <-> R-ATEXTB-SAT-7H-EXA-V-077-09 [positional_alternate_result] score=0.0210
POSITIONAL bphs1-ch18-015 <-> R-ATEXTB-SAT-7H-GEM-V-077-03 [positional_alternate_result] score=0.0203
POSITIONAL bphs1-ch18-015 <-> R-ATEXTB-SAT-7H-LIB-V-077-04 [positional_alternate_result] score=0.0302
POSITIONAL bphs1-ch18-015 <-> R-ATEXTB-SAT-7H-OWN-V-077-10 [positional_alternate_result] score=0.0210
POSITIONAL bphs1-ch18-015 <-> R-ATEXTB-SAT-7H-PIS-V-077-05 [positional_alternate_result] score=0.0305
POSITIONAL bphs1-ch18-015 <-> R-ATEXTB-SAT-7H-SAG-V-077-06 [positional_alternate_result] score=0.0166
POSITIONAL bphs1-ch18-015 <-> R-ATEXTB-SAT-7H-SCO-V-077-07 [positional_alternate_result] score=0.0481
POSITIONAL bphs1-ch18-015 <-> R-ATEXTB-SAT-7H-V-077 [positional_alternate_result] score=0.0559
POSITIONAL bphs1-ch18-015 <-> R-ATEXTB-SAT-7H-VIR-V-077-08 [positional_alternate_result] score=0.0203
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1120 [positional_alternate_result] score=0.0594
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1121 [positional_alternate_result] score=0.0645
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1122 [positional_alternate_result] score=0.0708
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1123 [positional_alternate_result] score=0.0693
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1124 [positional_alternate_result] score=0.0694
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1125 [positional_alternate_result] score=0.0696
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1126 [positional_alternate_result] score=0.0701
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1127 [positional_alternate_result] score=0.0622
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1128 [positional_alternate_result] score=0.0650
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1129 [positional_alternate_result] score=0.0655
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1130 [positional_alternate_result] score=0.0653
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1131 [positional_alternate_result] score=0.0623
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1132 [positional_alternate_result] score=0.0637
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1133 [positional_alternate_result] score=0.0805
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1134 [positional_alternate_result] score=0.0760
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1135 [positional_alternate_result] score=0.0770
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1136 [positional_alternate_result] score=0.0924
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1137 [positional_alternate_result] score=0.0374
POSITIONAL bphs1-ch18-015 <-> R-TBA15-1138 [positional_alternate_result] score=0.0635
POSITIONAL bphs1-ch18-015 <-> pd-ch08-081 [positional_alternate_result] score=0.1495
POSITIONAL bphs1-ch18-019 <-> R-ATEXTB-SAT-7H-AQU-V-077-01 [positional_alternate_result] score=0.0231
POSITIONAL bphs1-ch18-019 <-> R-ATEXTB-SAT-7H-CAP-V-077-02 [positional_alternate_result] score=0.0233
POSITIONAL bphs1-ch18-019 <-> R-ATEXTB-SAT-7H-EXA-V-077-09 [positional_alternate_result] score=0.0125
POSITIONAL bphs1-ch18-019 <-> R-ATEXTB-SAT-7H-GEM-V-077-03 [positional_alternate_result] score=0.0448
POSITIONAL bphs1-ch18-019 <-> R-ATEXTB-SAT-7H-LIB-V-077-04 [positional_alternate_result] score=0.0231
POSITIONAL bphs1-ch18-019 <-> R-ATEXTB-SAT-7H-OWN-V-077-10 [positional_alternate_result] score=0.0125
POSITIONAL bphs1-ch18-019 <-> R-ATEXTB-SAT-7H-PIS-V-077-05 [positional_alternate_result] score=0.0385
POSITIONAL bphs1-ch18-019 <-> R-ATEXTB-SAT-7H-SAG-V-077-06 [positional_alternate_result] score=0.0279
POSITIONAL bphs1-ch18-019 <-> R-ATEXTB-SAT-7H-SCO-V-077-07 [positional_alternate_result] score=0.0364
POSITIONAL bphs1-ch18-019 <-> R-ATEXTB-SAT-7H-V-077 [positional_alternate_result] score=0.0488
POSITIONAL bphs1-ch18-019 <-> R-ATEXTB-SAT-7H-VIR-V-077-08 [positional_alternate_result] score=0.0441
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1120 [positional_alternate_result] score=0.0438
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1121 [positional_alternate_result] score=0.0469
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1122 [positional_alternate_result] score=0.0478
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1123 [positional_alternate_result] score=0.0525
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1124 [positional_alternate_result] score=0.0517
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1125 [positional_alternate_result] score=0.0411
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1126 [positional_alternate_result] score=0.0413
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1127 [positional_alternate_result] score=0.0604
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1128 [positional_alternate_result] score=0.0393
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1129 [positional_alternate_result] score=0.0396
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1130 [positional_alternate_result] score=0.0395
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1131 [positional_alternate_result] score=0.0371
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1132 [positional_alternate_result] score=0.0417
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1133 [positional_alternate_result] score=0.0475
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1134 [positional_alternate_result] score=0.0466
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1135 [positional_alternate_result] score=0.0454
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1136 [positional_alternate_result] score=0.0563
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1137 [positional_alternate_result] score=0.0195
POSITIONAL bphs1-ch18-019 <-> R-TBA15-1138 [positional_alternate_result] score=0.0425
POSITIONAL bphs1-ch18-019 <-> pd-ch08-081 [positional_alternate_result] score=0.0793
POSITIONAL bphs1-ch18-028 <-> R-ATEXTB-SAT-7H-AQU-V-077-01 [positional_alternate_result] score=0.0226
POSITIONAL bphs1-ch18-028 <-> R-ATEXTB-SAT-7H-CAP-V-077-02 [positional_alternate_result] score=0.0228
POSITIONAL bphs1-ch18-028 <-> R-ATEXTB-SAT-7H-EXA-V-077-09 [positional_alternate_result] score=0.0286
POSITIONAL bphs1-ch18-028 <-> R-ATEXTB-SAT-7H-GEM-V-077-03 [positional_alternate_result] score=0.0562
POSITIONAL bphs1-ch18-028 <-> R-ATEXTB-SAT-7H-LIB-V-077-04 [positional_alternate_result] score=0.0226
POSITIONAL bphs1-ch18-028 <-> R-ATEXTB-SAT-7H-OWN-V-077-10 [positional_alternate_result] score=0.0286
POSITIONAL bphs1-ch18-028 <-> R-ATEXTB-SAT-7H-PIS-V-077-05 [positional_alternate_result] score=0.0613
POSITIONAL bphs1-ch18-028 <-> R-ATEXTB-SAT-7H-SAG-V-077-06 [positional_alternate_result] score=0.0475
POSITIONAL bphs1-ch18-028 <-> R-ATEXTB-SAT-7H-SCO-V-077-07 [positional_alternate_result] score=0.0304
POSITIONAL bphs1-ch18-028 <-> R-ATEXTB-SAT-7H-V-077 [positional_alternate_result] score=0.0511
POSITIONAL bphs1-ch18-028 <-> R-ATEXTB-SAT-7H-VIR-V-077-08 [positional_alternate_result] score=0.0562
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1120 [positional_alternate_result] score=0.0449
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1121 [positional_alternate_result] score=0.0776
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1122 [positional_alternate_result] score=0.0675
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1123 [positional_alternate_result] score=0.1238
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1124 [positional_alternate_result] score=0.1240
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1125 [positional_alternate_result] score=0.1244
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1126 [positional_alternate_result] score=0.1253
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1127 [positional_alternate_result] score=0.1066
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1128 [positional_alternate_result] score=0.0661
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1129 [positional_alternate_result] score=0.0665
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1130 [positional_alternate_result] score=0.0663
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1131 [positional_alternate_result] score=0.0620
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1132 [positional_alternate_result] score=0.0628
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1133 [positional_alternate_result] score=0.0994
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1134 [positional_alternate_result] score=0.0915
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1135 [positional_alternate_result] score=0.0951
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1136 [positional_alternate_result] score=0.1059
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1137 [positional_alternate_result] score=0.0614
POSITIONAL bphs1-ch18-028 <-> R-TBA15-1138 [positional_alternate_result] score=0.0764
POSITIONAL bphs1-ch18-028 <-> pd-ch08-081 [positional_alternate_result] score=0.1347
POSITIONAL bphs1-ch17-028 <-> R-ATEXTB-SAT-8H-DEB-V-078-01 [positional_alternate_result] score=0.0201
POSITIONAL bphs1-ch17-028 <-> R-ATEXTB-SAT-8H-ENE-V-078-02 [positional_alternate_result] score=0.0459
POSITIONAL bphs1-ch17-028 <-> R-ATEXTB-SAT-8H-EXA-V-078-03 [positional_alternate_result] score=0.0260
POSITIONAL bphs1-ch17-028 <-> R-ATEXTB-SAT-8H-OWN-V-078-04 [positional_alternate_result] score=0.0425
POSITIONAL bphs1-ch17-028 <-> R-ATEXTB-SAT-8H-V-078 [positional_alternate_result] score=0.0395
POSITIONAL bphs1-ch17-028 <-> R-TBA15-1139 [positional_alternate_result] score=0.0335
POSITIONAL bphs1-ch17-028 <-> R-TBA15-1140 [positional_alternate_result] score=0.0593
POSITIONAL bphs1-ch17-028 <-> R-TBA15-1141 [positional_alternate_result] score=0.0827
POSITIONAL bphs1-ch17-028 <-> R-TBA15-1142 [positional_alternate_result] score=0.0478
POSITIONAL bphs1-ch17-028 <-> R-TBA15-1143 [positional_alternate_result] score=0.0474
POSITIONAL bphs1-ch17-028 <-> R-TBA15-1144 [positional_alternate_result] score=0.0679
POSITIONAL bphs1-ch17-028 <-> R-TBA15-1145 [positional_alternate_result] score=0.0855
POSITIONAL bphs1-ch17-028 <-> R-TBA15-1146 [positional_alternate_result] score=0.0911
POSITIONAL bphs1-ch17-028 <-> R-TBA15-1147 [positional_alternate_result] score=0.0800
POSITIONAL bphs1-ch17-028 <-> R-TBA15-1148 [positional_alternate_result] score=0.0904
POSITIONAL bphs1-ch17-028 <-> R-TBA15-1149 [positional_alternate_result] score=0.0761
POSITIONAL bphs1-ch17-028 <-> R-TBA15-1150 [positional_alternate_result] score=0.0818
POSITIONAL bphs1-ch17-028 <-> R-TBA15-1151 [positional_alternate_result] score=0.0543
POSITIONAL bphs1-ch17-028 <-> R-TBA15-1152 [positional_alternate_result] score=0.0333
POSITIONAL bphs1-ch17-028 <-> lalkitab-ch27-proh-04 [positional_alternate_result] score=0.0657
POSITIONAL bphs1-ch17-028 <-> lalkitab-ch27-wave-w39 [positional_alternate_result] score=0.0303
POSITIONAL bphs1-ch17-028 <-> pd-ch08-082 [positional_alternate_result] score=0.0592
POSITIONAL bphs1-ch19-004 <-> R-ATEXTB-SAT-8H-DEB-V-078-01 [positional_alternate_result] score=0.0841
POSITIONAL bphs1-ch19-004 <-> R-ATEXTB-SAT-8H-ENE-V-078-02 [positional_alternate_result] score=0.1589
POSITIONAL bphs1-ch19-004 <-> R-ATEXTB-SAT-8H-EXA-V-078-03 [positional_alternate_result] score=0.0393
POSITIONAL bphs1-ch19-004 <-> R-ATEXTB-SAT-8H-OWN-V-078-04 [positional_alternate_result] score=0.0629
POSITIONAL bphs1-ch19-004 <-> R-ATEXTB-SAT-8H-V-078 [positional_alternate_result] score=0.0669
POSITIONAL bphs1-ch19-004 <-> R-TBA15-1139 [positional_alternate_result] score=0.0304
POSITIONAL bphs1-ch19-004 <-> R-TBA15-1140 [positional_alternate_result] score=0.0766
POSITIONAL bphs1-ch19-004 <-> R-TBA15-1141 [positional_alternate_result] score=0.0757
POSITIONAL bphs1-ch19-004 <-> R-TBA15-1142 [positional_alternate_result] score=0.0624
POSITIONAL bphs1-ch19-004 <-> R-TBA15-1143 [positional_alternate_result] score=0.0603
POSITIONAL bphs1-ch19-004 <-> R-TBA15-1144 [positional_alternate_result] score=0.0914
POSITIONAL bphs1-ch19-004 <-> R-TBA15-1145 [positional_alternate_result] score=0.1134
POSITIONAL bphs1-ch19-004 <-> R-TBA15-1146 [positional_alternate_result] score=0.1190
POSITIONAL bphs1-ch19-004 <-> R-TBA15-1147 [positional_alternate_result] score=0.1046
POSITIONAL bphs1-ch19-004 <-> R-TBA15-1148 [positional_alternate_result] score=0.1737
POSITIONAL bphs1-ch19-004 <-> R-TBA15-1149 [positional_alternate_result] score=0.1806
POSITIONAL bphs1-ch19-004 <-> R-TBA15-1150 [positional_alternate_result] score=0.1973
POSITIONAL bphs1-ch19-004 <-> R-TBA15-1151 [positional_alternate_result] score=0.0667
POSITIONAL bphs1-ch19-004 <-> R-TBA15-1152 [positional_alternate_result] score=0.0448
POSITIONAL bphs1-ch19-004 <-> lalkitab-ch27-proh-04 [positional_alternate_result] score=0.1019
POSITIONAL bphs1-ch19-004 <-> lalkitab-ch27-wave-w39 [positional_alternate_result] score=0.0314
POSITIONAL bphs1-ch19-004 <-> pd-ch08-082 [positional_alternate_result] score=0.0571
POSITIONAL bphs1-ch32-025 <-> R-ATEXTB-SAT-8H-DEB-V-078-01 [positional_alternate_result] score=0.0221
POSITIONAL bphs1-ch32-025 <-> R-ATEXTB-SAT-8H-ENE-V-078-02 [positional_alternate_result] score=0.0185
POSITIONAL bphs1-ch32-025 <-> R-ATEXTB-SAT-8H-EXA-V-078-03 [positional_alternate_result] score=0.0211
POSITIONAL bphs1-ch32-025 <-> R-ATEXTB-SAT-8H-OWN-V-078-04 [positional_alternate_result] score=0.0499
POSITIONAL bphs1-ch32-025 <-> R-ATEXTB-SAT-8H-V-078 [positional_alternate_result] score=0.0206
POSITIONAL bphs1-ch32-025 <-> R-TBA15-1139 [positional_alternate_result] score=0.0336
POSITIONAL bphs1-ch32-025 <-> R-TBA15-1140 [positional_alternate_result] score=0.0873
POSITIONAL bphs1-ch32-025 <-> R-TBA15-1141 [positional_alternate_result] score=0.0862
POSITIONAL bphs1-ch32-025 <-> R-TBA15-1142 [positional_alternate_result] score=0.0769
POSITIONAL bphs1-ch32-025 <-> R-TBA15-1143 [positional_alternate_result] score=0.0759
POSITIONAL bphs1-ch32-025 <-> R-TBA15-1144 [positional_alternate_result] score=0.0806
POSITIONAL bphs1-ch32-025 <-> R-TBA15-1145 [positional_alternate_result] score=0.1108
POSITIONAL bphs1-ch32-025 <-> R-TBA15-1146 [positional_alternate_result] score=0.1129
POSITIONAL bphs1-ch32-025 <-> R-TBA15-1147 [positional_alternate_result] score=0.0992
POSITIONAL bphs1-ch32-025 <-> R-TBA15-1148 [positional_alternate_result] score=0.0845
POSITIONAL bphs1-ch32-025 <-> R-TBA15-1149 [positional_alternate_result] score=0.0943
POSITIONAL bphs1-ch32-025 <-> R-TBA15-1150 [positional_alternate_result] score=0.1061
POSITIONAL bphs1-ch32-025 <-> R-TBA15-1151 [positional_alternate_result] score=0.0870
POSITIONAL bphs1-ch32-025 <-> R-TBA15-1152 [positional_alternate_result] score=0.0388
POSITIONAL bphs1-ch32-025 <-> lalkitab-ch27-proh-04 [positional_alternate_result] score=0.1027
POSITIONAL bphs1-ch32-025 <-> lalkitab-ch27-wave-w39 [positional_alternate_result] score=0.0250
POSITIONAL bphs1-ch32-025 <-> pd-ch08-082 [positional_alternate_result] score=0.0604
POSITIONAL bphs1-ch32-039 <-> R-ATEXTB-SAT-8H-DEB-V-078-01 [positional_alternate_result] score=0.0176
POSITIONAL bphs1-ch32-039 <-> R-ATEXTB-SAT-8H-ENE-V-078-02 [positional_alternate_result] score=0.0166
POSITIONAL bphs1-ch32-039 <-> R-ATEXTB-SAT-8H-EXA-V-078-03 [positional_alternate_result] score=0.0181
POSITIONAL bphs1-ch32-039 <-> R-ATEXTB-SAT-8H-OWN-V-078-04 [positional_alternate_result] score=0.0300
POSITIONAL bphs1-ch32-039 <-> R-ATEXTB-SAT-8H-V-078 [positional_alternate_result] score=0.0159
POSITIONAL bphs1-ch32-039 <-> R-TBA15-1139 [positional_alternate_result] score=0.0130
POSITIONAL bphs1-ch32-039 <-> R-TBA15-1140 [positional_alternate_result] score=0.0384
POSITIONAL bphs1-ch32-039 <-> R-TBA15-1141 [positional_alternate_result] score=0.0379
POSITIONAL bphs1-ch32-039 <-> R-TBA15-1142 [positional_alternate_result] score=0.0304
POSITIONAL bphs1-ch32-039 <-> R-TBA15-1143 [positional_alternate_result] score=0.0342
POSITIONAL bphs1-ch32-039 <-> R-TBA15-1144 [positional_alternate_result] score=0.0340
POSITIONAL bphs1-ch32-039 <-> R-TBA15-1145 [positional_alternate_result] score=0.0467
POSITIONAL bphs1-ch32-039 <-> R-TBA15-1146 [positional_alternate_result] score=0.0476
POSITIONAL bphs1-ch32-039 <-> R-TBA15-1147 [positional_alternate_result] score=0.0418
POSITIONAL bphs1-ch32-039 <-> R-TBA15-1148 [positional_alternate_result] score=0.0395
POSITIONAL bphs1-ch32-039 <-> R-TBA15-1149 [positional_alternate_result] score=0.0397
POSITIONAL bphs1-ch32-039 <-> R-TBA15-1150 [positional_alternate_result] score=0.0447
POSITIONAL bphs1-ch32-039 <-> R-TBA15-1151 [positional_alternate_result] score=0.0391
POSITIONAL bphs1-ch32-039 <-> R-TBA15-1152 [positional_alternate_result] score=0.0257
POSITIONAL bphs1-ch32-039 <-> lalkitab-ch27-proh-04 [positional_alternate_result] score=0.0791
POSITIONAL bphs1-ch32-039 <-> lalkitab-ch27-wave-w39 [positional_alternate_result] score=0.0206
POSITIONAL bphs1-ch32-039 <-> pd-ch08-082 [positional_alternate_result] score=0.0490
POSITIONAL bphs1-ch16-028 <-> R-ATEXTB-SAT-9H-061 [positional_alternate_result] score=0.0620
POSITIONAL bphs1-ch16-028 <-> R-ATEXTB-SAT-9H-DEB-V-079-01 [positional_alternate_result] score=0.0163
POSITIONAL bphs1-ch16-028 <-> R-ATEXTB-SAT-9H-EXA-V-079-02 [positional_alternate_result] score=0.0188
POSITIONAL bphs1-ch16-028 <-> R-ATEXTB-SAT-9H-OWN-V-079-03 [positional_alternate_result] score=0.0176
POSITIONAL bphs1-ch16-028 <-> R-ATEXTB-SAT-9H-V-079 [positional_alternate_result] score=0.0202
POSITIONAL bphs1-ch16-028 <-> R-BRIHAT-SAT-9H-133 [positional_alternate_result] score=0.0634
POSITIONAL bphs1-ch16-028 <-> R-TBA15-1153 [positional_alternate_result] score=0.0315
POSITIONAL bphs1-ch16-028 <-> R-TBA15-1154 [positional_alternate_result] score=0.1053
POSITIONAL bphs1-ch16-028 <-> R-TBA15-1155 [positional_alternate_result] score=0.0917
POSITIONAL bphs1-ch16-028 <-> R-TBA15-1156 [positional_alternate_result] score=0.0815
POSITIONAL bphs1-ch16-028 <-> R-TBA15-1157 [positional_alternate_result] score=0.0911
POSITIONAL bphs1-ch16-028 <-> R-TBA15-1158 [positional_alternate_result] score=0.0945
POSITIONAL bphs1-ch16-028 <-> R-TBA15-1159 [positional_alternate_result] score=0.0883
POSITIONAL bphs1-ch16-028 <-> R-TBA15-1160 [positional_alternate_result] score=0.0774
POSITIONAL bphs1-ch16-028 <-> R-TBA15-1161 [positional_alternate_result] score=0.0817
POSITIONAL bphs1-ch16-028 <-> R-TBA15-1162 [positional_alternate_result] score=0.1092
POSITIONAL bphs1-ch16-028 <-> R-TBA15-1163 [positional_alternate_result] score=0.0396
POSITIONAL bphs1-ch16-028 <-> lalkitab-ch27-wave-w14 [positional_alternate_result] score=0.0211
POSITIONAL bphs1-ch16-028 <-> pd-ch08-083 [positional_polarity_conflict] score=0.0779
POSITIONAL bphs1-ch17-009 <-> R-ATEXTB-SUN-1H-002 [positional_alternate_result] score=0.0413
POSITIONAL bphs1-ch17-009 <-> R-ATEXTB-SUN-1H-ARI-V-001-01 [positional_alternate_result] score=0.0359
POSITIONAL bphs1-ch17-009 <-> R-ATEXTB-SUN-1H-CAN-V-001-02 [positional_alternate_result] score=0.0360
POSITIONAL bphs1-ch17-009 <-> R-ATEXTB-SUN-1H-DEB-V-001-06 [positional_alternate_result] score=0.0263
POSITIONAL bphs1-ch17-009 <-> R-ATEXTB-SUN-1H-EXA-V-001-07 [positional_alternate_result] score=0.0166
POSITIONAL bphs1-ch17-009 <-> R-ATEXTB-SUN-1H-LEO-V-001-03 [positional_alternate_result] score=0.0359
POSITIONAL bphs1-ch17-009 <-> R-ATEXTB-SUN-1H-OWN-V-001-08 [positional_alternate_result] score=0.0342
POSITIONAL bphs1-ch17-009 <-> R-ATEXTB-SUN-1H-PIS-V-001-04 [positional_alternate_result] score=0.0232
POSITIONAL bphs1-ch17-009 <-> R-ATEXTB-SUN-1H-SCO-V-001-05 [positional_alternate_result] score=0.0234
POSITIONAL bphs1-ch17-009 <-> R-ATEXTB-SUN-1H-V-001 [positional_alternate_result] score=0.0383
POSITIONAL bphs1-ch17-009 <-> R-TBA15-001 [positional_alternate_result] score=0.0297
POSITIONAL bphs1-ch17-009 <-> R-TBA15-002 [positional_alternate_result] score=0.0479
POSITIONAL bphs1-ch17-009 <-> R-TBA15-003 [positional_alternate_result] score=0.0290
POSITIONAL bphs1-ch17-009 <-> R-TBA15-004 [positional_alternate_result] score=0.0430
POSITIONAL bphs1-ch17-009 <-> R-TBA15-005 [positional_alternate_result] score=0.0690
POSITIONAL bphs1-ch17-009 <-> R-TBA15-006 [positional_alternate_result] score=0.0440
POSITIONAL bphs1-ch17-009 <-> R-TBA15-007 [positional_alternate_result] score=0.0457
POSITIONAL bphs1-ch17-009 <-> R-TBA15-008 [positional_alternate_result] score=0.0504
POSITIONAL bphs1-ch17-009 <-> R-TBA15-009 [positional_alternate_result] score=0.0497
POSITIONAL bphs1-ch17-009 <-> R-TBA15-010 [positional_alternate_result] score=0.0444
POSITIONAL bphs1-ch17-009 <-> R-TBA15-011 [positional_alternate_result] score=0.0468
POSITIONAL bphs1-ch17-009 <-> R-TBA15-012 [positional_alternate_result] score=0.0468
POSITIONAL bphs1-ch17-009 <-> R-TBA15-013 [positional_alternate_result] score=0.0540
POSITIONAL bphs1-ch17-009 <-> R-TBA15-014 [positional_alternate_result] score=0.0486
POSITIONAL bphs1-ch17-009 <-> R-TBA15-015 [positional_alternate_result] score=0.0254
POSITIONAL bphs1-ch17-009 <-> R-TBA15-016 [positional_alternate_result] score=0.0302
POSITIONAL bphs1-ch17-009 <-> R-TBA15-017 [positional_alternate_result] score=0.0446
POSITIONAL bphs1-ch17-009 <-> R-TBA15-018 [positional_alternate_result] score=0.0480
POSITIONAL bphs1-ch17-009 <-> R-TBA15-019 [positional_alternate_result] score=0.0479
POSITIONAL bphs1-ch17-009 <-> pd-ch08-001 [positional_alternate_result] score=0.0223
POSITIONAL bphs1-ch32-032 <-> R-ATEXTB-SUN-1H-002 [positional_alternate_result] score=0.0652
POSITIONAL bphs1-ch32-032 <-> R-ATEXTB-SUN-1H-ARI-V-001-01 [positional_alternate_result] score=0.0280
POSITIONAL bphs1-ch32-032 <-> R-ATEXTB-SUN-1H-CAN-V-001-02 [positional_alternate_result] score=0.0280
POSITIONAL bphs1-ch32-032 <-> R-ATEXTB-SUN-1H-DEB-V-001-06 [positional_alternate_result] score=0.0212
POSITIONAL bphs1-ch32-032 <-> R-ATEXTB-SUN-1H-EXA-V-001-07 [positional_alternate_result] score=0.0111
POSITIONAL bphs1-ch32-032 <-> R-ATEXTB-SUN-1H-LEO-V-001-03 [positional_alternate_result] score=0.0279
POSITIONAL bphs1-ch32-032 <-> R-ATEXTB-SUN-1H-OWN-V-001-08 [positional_alternate_result] score=0.0266
POSITIONAL bphs1-ch32-032 <-> R-ATEXTB-SUN-1H-PIS-V-001-04 [positional_alternate_result] score=0.0180
POSITIONAL bphs1-ch32-032 <-> R-ATEXTB-SUN-1H-SCO-V-001-05 [positional_alternate_result] score=0.0182
POSITIONAL bphs1-ch32-032 <-> R-ATEXTB-SUN-1H-V-001 [positional_alternate_result] score=0.0315
POSITIONAL bphs1-ch32-032 <-> R-TBA15-001 [positional_alternate_result] score=0.0502
POSITIONAL bphs1-ch32-032 <-> R-TBA15-002 [positional_alternate_result] score=0.0769
POSITIONAL bphs1-ch32-032 <-> R-TBA15-003 [positional_alternate_result] score=0.0594
POSITIONAL bphs1-ch32-032 <-> R-TBA15-004 [positional_alternate_result] score=0.0943
POSITIONAL bphs1-ch32-032 <-> R-TBA15-005 [positional_alternate_result] score=0.0935
POSITIONAL bphs1-ch32-032 <-> R-TBA15-006 [positional_alternate_result] score=0.0890
POSITIONAL bphs1-ch32-032 <-> R-TBA15-007 [positional_alternate_result] score=0.0924
POSITIONAL bphs1-ch32-032 <-> R-TBA15-008 [positional_alternate_result] score=0.1018
POSITIONAL bphs1-ch32-032 <-> R-TBA15-009 [positional_alternate_result] score=0.1006
POSITIONAL bphs1-ch32-032 <-> R-TBA15-010 [positional_alternate_result] score=0.0898
POSITIONAL bphs1-ch32-032 <-> R-TBA15-011 [positional_alternate_result] score=0.0946
POSITIONAL bphs1-ch32-032 <-> R-TBA15-012 [positional_alternate_result] score=0.0947
POSITIONAL bphs1-ch32-032 <-> R-TBA15-013 [positional_alternate_result] score=0.0925
POSITIONAL bphs1-ch32-032 <-> R-TBA15-014 [positional_alternate_result] score=0.0833
POSITIONAL bphs1-ch32-032 <-> R-TBA15-015 [positional_alternate_result] score=0.0745
POSITIONAL bphs1-ch32-032 <-> R-TBA15-016 [positional_alternate_result] score=0.0454
POSITIONAL bphs1-ch32-032 <-> R-TBA15-017 [positional_alternate_result] score=0.0977
POSITIONAL bphs1-ch32-032 <-> R-TBA15-018 [positional_alternate_result] score=0.0984
POSITIONAL bphs1-ch32-032 <-> R-TBA15-019 [positional_alternate_result] score=0.1050
POSITIONAL bphs1-ch32-032 <-> pd-ch08-001 [positional_alternate_result] score=0.0175
POSITIONAL bphs1-ch42-017 <-> R-ATEXTB-SUN-2H-AQU-V-002-01 [positional_alternate_result] score=0.0492
POSITIONAL bphs1-ch42-017 <-> R-ATEXTB-SUN-2H-ARI-V-002-02 [positional_alternate_result] score=0.0498
POSITIONAL bphs1-ch42-017 <-> R-ATEXTB-SUN-2H-CAN-V-002-03 [positional_alternate_result] score=0.0497
POSITIONAL bphs1-ch42-017 <-> R-ATEXTB-SUN-2H-CAP-V-002-04 [positional_alternate_result] score=0.0493
POSITIONAL bphs1-ch42-017 <-> R-ATEXTB-SUN-2H-ENE-V-002-10 [positional_alternate_result] score=0.0417
POSITIONAL bphs1-ch42-017 <-> R-ATEXTB-SUN-2H-EXA-V-002-11 [positional_alternate_result] score=0.0842
POSITIONAL bphs1-ch42-017 <-> R-ATEXTB-SUN-2H-LEO-V-002-05 [positional_alternate_result] score=0.0495
POSITIONAL bphs1-ch42-017 <-> R-ATEXTB-SUN-2H-LIB-V-002-06 [positional_alternate_result] score=0.0491
POSITIONAL bphs1-ch42-017 <-> R-ATEXTB-SUN-2H-OWN-V-002-12 [positional_alternate_result] score=0.0817
POSITIONAL bphs1-ch42-017 <-> R-ATEXTB-SUN-2H-PIS-V-002-07 [positional_alternate_result] score=0.0494
POSITIONAL bphs1-ch42-017 <-> R-ATEXTB-SUN-2H-SAG-V-002-08 [positional_alternate_result] score=0.0494
POSITIONAL bphs1-ch42-017 <-> R-ATEXTB-SUN-2H-SCO-V-002-09 [positional_alternate_result] score=0.0497
POSITIONAL bphs1-ch42-017 <-> R-ATEXTB-SUN-2H-V-002 [positional_alternate_result] score=0.0380
POSITIONAL bphs1-ch42-017 <-> R-TBA15-020 [positional_alternate_result] score=0.0187
POSITIONAL bphs1-ch42-017 <-> R-TBA15-021 [positional_alternate_result] score=0.0760
POSITIONAL bphs1-ch42-017 <-> R-TBA15-022 [positional_alternate_result] score=0.0916
POSITIONAL bphs1-ch42-017 <-> R-TBA15-023 [positional_alternate_result] score=0.0916
POSITIONAL bphs1-ch42-017 <-> R-TBA15-024 [positional_alternate_result] score=0.0916
POSITIONAL bphs1-ch42-017 <-> R-TBA15-025 [positional_alternate_result] score=0.0916
POSITIONAL bphs1-ch42-017 <-> R-TBA15-026 [positional_alternate_result] score=0.0916
POSITIONAL bphs1-ch42-017 <-> R-TBA15-027 [positional_alternate_result] score=0.0783
POSITIONAL bphs1-ch42-017 <-> R-TBA15-028 [positional_alternate_result] score=0.0572
POSITIONAL bphs1-ch42-017 <-> R-TBA15-029 [positional_alternate_result] score=0.0786
POSITIONAL bphs1-ch42-017 <-> R-TBA15-030 [positional_alternate_result] score=0.0700
POSITIONAL bphs1-ch42-017 <-> R-TBA15-031 [positional_alternate_result] score=0.0693
POSITIONAL bphs1-ch42-017 <-> R-TBA15-032 [positional_alternate_result] score=0.0729
POSITIONAL bphs1-ch42-017 <-> R-TBA15-033 [positional_alternate_result] score=0.0274
POSITIONAL bphs1-ch42-017 <-> R-TBA15-034 [positional_alternate_result] score=0.0346
POSITIONAL bphs1-ch42-017 <-> R-TBA15-035 [positional_alternate_result] score=0.0343
POSITIONAL bphs1-ch42-017 <-> R-TBA15-036 [positional_alternate_result] score=0.0424
POSITIONAL bphs1-ch42-017 <-> R-TBA15-037 [positional_alternate_result] score=0.0702
POSITIONAL bphs1-ch42-017 <-> R-TBA15-038 [positional_alternate_result] score=0.0435
POSITIONAL bphs1-ch42-017 <-> R-TBA15-039 [positional_alternate_result] score=0.0870
POSITIONAL bphs1-ch42-017 <-> R-TBA15-040 [positional_alternate_result] score=0.0737
POSITIONAL bphs1-ch42-017 <-> pd-ch08-002 [positional_alternate_result] score=0.0197
POSITIONAL bphs1-ch42-018 <-> R-ATEXTB-SUN-2H-AQU-V-002-01 [positional_alternate_result] score=0.0552
POSITIONAL bphs1-ch42-018 <-> R-ATEXTB-SUN-2H-ARI-V-002-02 [positional_alternate_result] score=0.0558
POSITIONAL bphs1-ch42-018 <-> R-ATEXTB-SUN-2H-CAN-V-002-03 [positional_alternate_result] score=0.0557
POSITIONAL bphs1-ch42-018 <-> R-ATEXTB-SUN-2H-CAP-V-002-04 [positional_alternate_result] score=0.0553
POSITIONAL bphs1-ch42-018 <-> R-ATEXTB-SUN-2H-ENE-V-002-10 [positional_alternate_result] score=0.0468
POSITIONAL bphs1-ch42-018 <-> R-ATEXTB-SUN-2H-EXA-V-002-11 [positional_alternate_result] score=0.0944
POSITIONAL bphs1-ch42-018 <-> R-ATEXTB-SUN-2H-LEO-V-002-05 [positional_alternate_result] score=0.0555
POSITIONAL bphs1-ch42-018 <-> R-ATEXTB-SUN-2H-LIB-V-002-06 [positional_alternate_result] score=0.0550
POSITIONAL bphs1-ch42-018 <-> R-ATEXTB-SUN-2H-OWN-V-002-12 [positional_alternate_result] score=0.0916
POSITIONAL bphs1-ch42-018 <-> R-ATEXTB-SUN-2H-PIS-V-002-07 [positional_alternate_result] score=0.0553
POSITIONAL bphs1-ch42-018 <-> R-ATEXTB-SUN-2H-SAG-V-002-08 [positional_alternate_result] score=0.0554
POSITIONAL bphs1-ch42-018 <-> R-ATEXTB-SUN-2H-SCO-V-002-09 [positional_alternate_result] score=0.0557
POSITIONAL bphs1-ch42-018 <-> R-ATEXTB-SUN-2H-V-002 [positional_alternate_result] score=0.0908
POSITIONAL bphs1-ch42-018 <-> R-TBA15-020 [positional_alternate_result] score=0.0210
POSITIONAL bphs1-ch42-018 <-> R-TBA15-021 [positional_alternate_result] score=0.0852
POSITIONAL bphs1-ch42-018 <-> R-TBA15-022 [positional_alternate_result] score=0.1027
POSITIONAL bphs1-ch42-018 <-> R-TBA15-023 [positional_alternate_result] score=0.1027
POSITIONAL bphs1-ch42-018 <-> R-TBA15-024 [positional_alternate_result] score=0.1027
POSITIONAL bphs1-ch42-018 <-> R-TBA15-025 [positional_alternate_result] score=0.1027
POSITIONAL bphs1-ch42-018 <-> R-TBA15-026 [positional_alternate_result] score=0.1027
POSITIONAL bphs1-ch42-018 <-> R-TBA15-027 [positional_alternate_result] score=0.0878
POSITIONAL bphs1-ch42-018 <-> R-TBA15-028 [positional_alternate_result] score=0.0641
POSITIONAL bphs1-ch42-018 <-> R-TBA15-029 [positional_alternate_result] score=0.0881
POSITIONAL bphs1-ch42-018 <-> R-TBA15-030 [positional_alternate_result] score=0.0785
POSITIONAL bphs1-ch42-018 <-> R-TBA15-031 [positional_alternate_result] score=0.0777
POSITIONAL bphs1-ch42-018 <-> R-TBA15-032 [positional_alternate_result] score=0.0817
POSITIONAL bphs1-ch42-018 <-> R-TBA15-033 [positional_alternate_result] score=0.0307
POSITIONAL bphs1-ch42-018 <-> R-TBA15-034 [positional_alternate_result] score=0.0388
POSITIONAL bphs1-ch42-018 <-> R-TBA15-035 [positional_alternate_result] score=0.0385
POSITIONAL bphs1-ch42-018 <-> R-TBA15-036 [positional_alternate_result] score=0.0475
POSITIONAL bphs1-ch42-018 <-> R-TBA15-037 [positional_alternate_result] score=0.0787
POSITIONAL bphs1-ch42-018 <-> R-TBA15-038 [positional_alternate_result] score=0.0488
POSITIONAL bphs1-ch42-018 <-> R-TBA15-039 [positional_alternate_result] score=0.0975
POSITIONAL bphs1-ch42-018 <-> R-TBA15-040 [positional_alternate_result] score=0.0827
POSITIONAL bphs1-ch42-018 <-> pd-ch08-002 [positional_alternate_result] score=0.1717
POSITIONAL bphs1-ch14-015 <-> R-ATEXTB-SUN-3H-DEB-V-003-01 [positional_alternate_result] score=0.0180
POSITIONAL bphs1-ch14-015 <-> R-ATEXTB-SUN-3H-V-003 [positional_alternate_result] score=0.0762
POSITIONAL bphs1-ch14-015 <-> R-BRIHAT-SUN-3H-177 [positional_polarity_conflict] score=0.0952
POSITIONAL bphs1-ch14-015 <-> R-TBA15-041 [positional_alternate_result] score=0.0803
POSITIONAL bphs1-ch14-015 <-> R-TBA15-042 [positional_alternate_result] score=0.0947
POSITIONAL bphs1-ch14-015 <-> R-TBA15-043 [positional_alternate_result] score=0.1022
POSITIONAL bphs1-ch14-015 <-> R-TBA15-044 [positional_alternate_result] score=0.0653
POSITIONAL bphs1-ch14-015 <-> R-TBA15-045 [positional_alternate_result] score=0.0860
POSITIONAL bphs1-ch14-015 <-> R-TBA15-046 [positional_alternate_result] score=0.0806
POSITIONAL bphs1-ch14-015 <-> R-TBA15-047 [positional_alternate_result] score=0.0362
POSITIONAL bphs1-ch14-015 <-> pd-ch08-003 [positional_alternate_result] score=0.0379
POSITIONAL bphs1-ch15-011 <-> R-ATEXTB-SUN-4H-EXA-V-004-02 [positional_alternate_result] score=0.0340
POSITIONAL bphs1-ch15-011 <-> R-ATEXTB-SUN-4H-OWN-V-004-03 [positional_alternate_result] score=0.0340
POSITIONAL bphs1-ch15-011 <-> R-ATEXTB-SUN-4H-SCO-V-004-01 [positional_alternate_result] score=0.0247
POSITIONAL bphs1-ch15-011 <-> R-ATEXTB-SUN-4H-V-004 [positional_alternate_result] score=0.0321
POSITIONAL bphs1-ch15-011 <-> R-BRIHAT-SUN-4H-072 [positional_alternate_result] score=0.3247
POSITIONAL bphs1-ch15-011 <-> R-TBA15-048 [positional_alternate_result] score=0.0359
POSITIONAL bphs1-ch15-011 <-> R-TBA15-049 [positional_alternate_result] score=0.0196
POSITIONAL bphs1-ch15-011 <-> R-TBA15-050 [positional_alternate_result] score=0.0424
POSITIONAL bphs1-ch15-011 <-> R-TBA15-051 [positional_alternate_result] score=0.0284
POSITIONAL bphs1-ch15-011 <-> R-TBA15-052 [positional_alternate_result] score=0.0239
POSITIONAL bphs1-ch15-011 <-> R-TBA15-053 [positional_alternate_result] score=0.0825
POSITIONAL bphs1-ch15-011 <-> R-TBA15-054 [positional_alternate_result] score=0.0238
POSITIONAL bphs1-ch15-011 <-> R-TBA15-055 [positional_alternate_result] score=0.0299
POSITIONAL bphs1-ch15-011 <-> R-TBA15-056 [positional_alternate_result] score=0.0506
POSITIONAL bphs1-ch15-011 <-> pd-ch08-004 [positional_alternate_result] score=0.0109
POSITIONAL bphs1-ch18-008 <-> R-ATEXTB-SUN-7H-CAP-V-007-01 [positional_alternate_result] score=0.0252
POSITIONAL bphs1-ch18-008 <-> R-ATEXTB-SUN-7H-DEB-V-007-02 [positional_alternate_result] score=0.0425
POSITIONAL bphs1-ch18-008 <-> R-ATEXTB-SUN-7H-ENE-V-007-03 [positional_alternate_result] score=0.0201
POSITIONAL bphs1-ch18-008 <-> R-ATEXTB-SUN-7H-EXA-V-007-04 [positional_alternate_result] score=0.0207
POSITIONAL bphs1-ch18-008 <-> R-ATEXTB-SUN-7H-OWN-V-007-05 [positional_alternate_result] score=0.0202
POSITIONAL bphs1-ch18-008 <-> R-ATEXTB-SUN-7H-V-007 [positional_alternate_result] score=0.0389
POSITIONAL bphs1-ch18-008 <-> R-TBA15-089 [positional_alternate_result] score=0.0253
POSITIONAL bphs1-ch18-008 <-> R-TBA15-090 [positional_alternate_result] score=0.0715
POSITIONAL bphs1-ch18-008 <-> R-TBA15-091 [positional_alternate_result] score=0.0227
POSITIONAL bphs1-ch18-008 <-> R-TBA15-092 [positional_alternate_result] score=0.0228
POSITIONAL bphs1-ch18-008 <-> R-TBA15-093 [positional_alternate_result] score=0.0225
POSITIONAL bphs1-ch18-008 <-> R-TBA15-094 [positional_alternate_result] score=0.0310
POSITIONAL bphs1-ch18-008 <-> R-TBA15-095 [positional_alternate_result] score=0.0268
POSITIONAL bphs1-ch18-008 <-> R-TBA15-096 [positional_alternate_result] score=0.0759
POSITIONAL bphs1-ch18-008 <-> R-TBA15-097 [positional_alternate_result] score=0.0266
POSITIONAL bphs1-ch18-008 <-> R-TBA15-098 [positional_alternate_result] score=0.0176
POSITIONAL bphs1-ch18-008 <-> R-TBA15-099 [positional_alternate_result] score=0.0551
POSITIONAL bphs1-ch18-008 <-> R-TBA15-100 [positional_alternate_result] score=0.0350
POSITIONAL bphs1-ch18-008 <-> lalkitab-ch25-sun-h7 [positional_alternate_result] score=0.0516
POSITIONAL bphs1-ch18-008 <-> pd-ch08-007 [positional_alternate_result] score=0.0783
POSITIONAL bphs1-ch18-031 <-> R-ATEXTB-SUN-7H-CAP-V-007-01 [positional_alternate_result] score=0.0159
POSITIONAL bphs1-ch18-031 <-> R-ATEXTB-SUN-7H-DEB-V-007-02 [positional_alternate_result] score=0.0781
POSITIONAL bphs1-ch18-031 <-> R-ATEXTB-SUN-7H-ENE-V-007-03 [positional_alternate_result] score=0.0209
POSITIONAL bphs1-ch18-031 <-> R-ATEXTB-SUN-7H-EXA-V-007-04 [positional_alternate_result] score=0.0143
POSITIONAL bphs1-ch18-031 <-> R-ATEXTB-SUN-7H-OWN-V-007-05 [positional_alternate_result] score=0.0815
POSITIONAL bphs1-ch18-031 <-> R-ATEXTB-SUN-7H-V-007 [positional_alternate_result] score=0.0681
POSITIONAL bphs1-ch18-031 <-> R-TBA15-089 [positional_alternate_result] score=0.0581
POSITIONAL bphs1-ch18-031 <-> R-TBA15-090 [positional_alternate_result] score=0.1005
POSITIONAL bphs1-ch18-031 <-> R-TBA15-091 [positional_alternate_result] score=0.0144
POSITIONAL bphs1-ch18-031 <-> R-TBA15-092 [positional_alternate_result] score=0.0216
POSITIONAL bphs1-ch18-031 <-> R-TBA15-093 [positional_alternate_result] score=0.0829
POSITIONAL bphs1-ch18-031 <-> R-TBA15-094 [positional_alternate_result] score=0.0182
POSITIONAL bphs1-ch18-031 <-> R-TBA15-095 [positional_alternate_result] score=0.0171
POSITIONAL bphs1-ch18-031 <-> R-TBA15-096 [positional_alternate_result] score=0.0305
POSITIONAL bphs1-ch18-031 <-> R-TBA15-097 [positional_alternate_result] score=0.0135
POSITIONAL bphs1-ch18-031 <-> R-TBA15-098 [positional_alternate_result] score=0.0112
POSITIONAL bphs1-ch18-031 <-> R-TBA15-099 [positional_alternate_result] score=0.0301
POSITIONAL bphs1-ch18-031 <-> R-TBA15-100 [positional_alternate_result] score=0.0572
POSITIONAL bphs1-ch18-031 <-> lalkitab-ch25-sun-h7 [positional_alternate_result] score=0.0506
POSITIONAL bphs1-ch18-031 <-> pd-ch08-007 [positional_polarity_conflict] score=0.0715
POSITIONAL bphs1-ch32-019 <-> R-ATEXTB-SUN-9H-DEB-V-009-02 [positional_alternate_result] score=0.0156
POSITIONAL bphs1-ch32-019 <-> R-ATEXTB-SUN-9H-ENE-V-009-03 [positional_alternate_result] score=0.0467
POSITIONAL bphs1-ch32-019 <-> R-ATEXTB-SUN-9H-EXA-V-009-04 [positional_alternate_result] score=0.0275
POSITIONAL bphs1-ch32-019 <-> R-ATEXTB-SUN-9H-OWN-V-009-05 [positional_alternate_result] score=0.0508
POSITIONAL bphs1-ch32-019 <-> R-ATEXTB-SUN-9H-SAG-V-009-01 [positional_alternate_result] score=0.0201
POSITIONAL bphs1-ch32-019 <-> R-ATEXTB-SUN-9H-V-009 [positional_alternate_result] score=0.0361
POSITIONAL bphs1-ch32-019 <-> R-TBA15-116 [positional_alternate_result] score=0.0555
POSITIONAL bphs1-ch32-019 <-> R-TBA15-117 [positional_alternate_result] score=0.1036
POSITIONAL bphs1-ch32-019 <-> R-TBA15-118 [positional_alternate_result] score=0.0755
POSITIONAL bphs1-ch32-019 <-> R-TBA15-119 [positional_alternate_result] score=0.0983
POSITIONAL bphs1-ch32-019 <-> R-TBA15-120 [positional_alternate_result] score=0.0519
POSITIONAL bphs1-ch32-019 <-> R-TBA15-121 [positional_alternate_result] score=0.0769
POSITIONAL bphs1-ch32-019 <-> R-TBA15-122 [positional_alternate_result] score=0.0890
POSITIONAL bphs1-ch32-019 <-> R-TBA15-123 [positional_alternate_result] score=0.0440
POSITIONAL bphs1-ch32-019 <-> R-TBA15-124 [positional_alternate_result] score=0.0776
POSITIONAL bphs1-ch32-019 <-> pd-ch08-009 [positional_alternate_result] score=0.1620
POSITIONAL bphs1-ch17-013 <-> R-ATEXTB-VEN-1H-AQU-V-059-01 [positional_alternate_result] score=0.0169
POSITIONAL bphs1-ch17-013 <-> R-ATEXTB-VEN-1H-ARI-V-059-02 [positional_alternate_result] score=0.0183
POSITIONAL bphs1-ch17-013 <-> R-ATEXTB-VEN-1H-CAN-V-059-03 [positional_alternate_result] score=0.0288
POSITIONAL bphs1-ch17-013 <-> R-ATEXTB-VEN-1H-CAP-V-059-04 [positional_alternate_result] score=0.0183
POSITIONAL bphs1-ch17-013 <-> R-ATEXTB-VEN-1H-EXA-V-059-10 [positional_alternate_result] score=0.0361
POSITIONAL bphs1-ch17-013 <-> R-ATEXTB-VEN-1H-GEM-V-059-05 [positional_alternate_result] score=0.0169
POSITIONAL bphs1-ch17-013 <-> R-ATEXTB-VEN-1H-LIB-V-059-06 [positional_alternate_result] score=0.0170
POSITIONAL bphs1-ch17-013 <-> R-ATEXTB-VEN-1H-OWN-V-059-11 [positional_alternate_result] score=0.0242
POSITIONAL bphs1-ch17-013 <-> R-ATEXTB-VEN-1H-PIS-V-059-07 [positional_alternate_result] score=0.0391
POSITIONAL bphs1-ch17-013 <-> R-ATEXTB-VEN-1H-SCO-V-059-08 [positional_alternate_result] score=0.0388
POSITIONAL bphs1-ch17-013 <-> R-ATEXTB-VEN-1H-TAU-V-059-09 [positional_alternate_result] score=0.0173
POSITIONAL bphs1-ch17-013 <-> R-ATEXTB-VEN-1H-V-059 [positional_alternate_result] score=0.0593
POSITIONAL bphs1-ch17-013 <-> R-TBA15-898 [positional_alternate_result] score=0.0528
POSITIONAL bphs1-ch17-013 <-> R-TBA15-899 [positional_alternate_result] score=0.0484
POSITIONAL bphs1-ch17-013 <-> R-TBA15-900 [positional_alternate_result] score=0.0451
POSITIONAL bphs1-ch17-013 <-> R-TBA15-901 [positional_alternate_result] score=0.0447
POSITIONAL bphs1-ch17-013 <-> R-TBA15-902 [positional_alternate_result] score=0.0434
POSITIONAL bphs1-ch17-013 <-> R-TBA15-903 [positional_alternate_result] score=0.0445
POSITIONAL bphs1-ch17-013 <-> R-TBA15-904 [positional_alternate_result] score=0.0449
POSITIONAL bphs1-ch17-013 <-> R-TBA15-905 [positional_alternate_result] score=0.0349
POSITIONAL bphs1-ch17-013 <-> R-TBA15-906 [positional_alternate_result] score=0.0431
POSITIONAL bphs1-ch17-013 <-> R-TBA15-907 [positional_alternate_result] score=0.0430
POSITIONAL bphs1-ch17-013 <-> R-TBA15-908 [positional_alternate_result] score=0.0428
POSITIONAL bphs1-ch17-013 <-> R-TBA15-909 [positional_alternate_result] score=0.0424
POSITIONAL bphs1-ch17-013 <-> R-TBA15-910 [positional_alternate_result] score=0.0361
POSITIONAL bphs1-ch17-013 <-> R-TBA15-911 [positional_alternate_result] score=0.0557
POSITIONAL bphs1-ch17-013 <-> R-TBA15-912 [positional_alternate_result] score=0.0370
POSITIONAL bphs1-ch17-013 <-> R-TBA15-913 [positional_alternate_result] score=0.0445
POSITIONAL bphs1-ch17-013 <-> R-TBA15-914 [positional_alternate_result] score=0.0346
POSITIONAL bphs1-ch17-013 <-> R-TBA15-915 [positional_alternate_result] score=0.0611
POSITIONAL bphs1-ch17-013 <-> R-TBA15-916 [positional_alternate_result] score=0.0394
POSITIONAL bphs1-ch17-013 <-> R-TBA15-917 [positional_alternate_result] score=0.0253
POSITIONAL bphs1-ch17-013 <-> R-TBA15-918 [positional_alternate_result] score=0.0643
POSITIONAL bphs1-ch17-013 <-> R-TBA15-919 [positional_alternate_result] score=0.0370
POSITIONAL bphs1-ch17-013 <-> pd-ch04-027 [positional_polarity_conflict] score=0.0486
POSITIONAL bphs1-ch17-013 <-> pd-ch08-062 [positional_polarity_conflict] score=0.0693
POSITIONAL bphs1-ch18-042 <-> R-ATEXTB-VEN-1H-AQU-V-059-01 [positional_alternate_result] score=0.0251
POSITIONAL bphs1-ch18-042 <-> R-ATEXTB-VEN-1H-ARI-V-059-02 [positional_alternate_result] score=0.0249
POSITIONAL bphs1-ch18-042 <-> R-ATEXTB-VEN-1H-CAN-V-059-03 [positional_alternate_result] score=0.0241
POSITIONAL bphs1-ch18-042 <-> R-ATEXTB-VEN-1H-CAP-V-059-04 [positional_alternate_result] score=0.0250
POSITIONAL bphs1-ch18-042 <-> R-ATEXTB-VEN-1H-EXA-V-059-10 [positional_alternate_result] score=0.1042
POSITIONAL bphs1-ch18-042 <-> R-ATEXTB-VEN-1H-GEM-V-059-05 [positional_alternate_result] score=0.0251
POSITIONAL bphs1-ch18-042 <-> R-ATEXTB-VEN-1H-LIB-V-059-06 [positional_alternate_result] score=0.0252
POSITIONAL bphs1-ch18-042 <-> R-ATEXTB-VEN-1H-OWN-V-059-11 [positional_alternate_result] score=0.0491
POSITIONAL bphs1-ch18-042 <-> R-ATEXTB-VEN-1H-PIS-V-059-07 [positional_alternate_result] score=0.0757
POSITIONAL bphs1-ch18-042 <-> R-ATEXTB-VEN-1H-SCO-V-059-08 [positional_alternate_result] score=0.0239
POSITIONAL bphs1-ch18-042 <-> R-ATEXTB-VEN-1H-TAU-V-059-09 [positional_alternate_result] score=0.0257
POSITIONAL bphs1-ch18-042 <-> R-ATEXTB-VEN-1H-V-059 [positional_alternate_result] score=0.0596
POSITIONAL bphs1-ch18-042 <-> R-TBA15-898 [positional_alternate_result] score=0.0357
POSITIONAL bphs1-ch18-042 <-> R-TBA15-899 [positional_alternate_result] score=0.0467
POSITIONAL bphs1-ch18-042 <-> R-TBA15-900 [positional_alternate_result] score=0.0708
POSITIONAL bphs1-ch18-042 <-> R-TBA15-901 [positional_alternate_result] score=0.0701
POSITIONAL bphs1-ch18-042 <-> R-TBA15-902 [positional_alternate_result] score=0.0680
POSITIONAL bphs1-ch18-042 <-> R-TBA15-903 [positional_alternate_result] score=0.0697
POSITIONAL bphs1-ch18-042 <-> R-TBA15-904 [positional_alternate_result] score=0.0704
POSITIONAL bphs1-ch18-042 <-> R-TBA15-905 [positional_alternate_result] score=0.0568
POSITIONAL bphs1-ch18-042 <-> R-TBA15-906 [positional_alternate_result] score=0.0677
POSITIONAL bphs1-ch18-042 <-> R-TBA15-907 [positional_alternate_result] score=0.0675
POSITIONAL bphs1-ch18-042 <-> R-TBA15-908 [positional_alternate_result] score=0.0672
POSITIONAL bphs1-ch18-042 <-> R-TBA15-909 [positional_alternate_result] score=0.0666
POSITIONAL bphs1-ch18-042 <-> R-TBA15-910 [positional_alternate_result] score=0.0589
POSITIONAL bphs1-ch18-042 <-> R-TBA15-911 [positional_alternate_result] score=0.0582
POSITIONAL bphs1-ch18-042 <-> R-TBA15-912 [positional_alternate_result] score=0.0533
POSITIONAL bphs1-ch18-042 <-> R-TBA15-913 [positional_alternate_result] score=0.0778
POSITIONAL bphs1-ch18-042 <-> R-TBA15-914 [positional_alternate_result] score=0.0494
POSITIONAL bphs1-ch18-042 <-> R-TBA15-915 [positional_alternate_result] score=0.0578
POSITIONAL bphs1-ch18-042 <-> R-TBA15-916 [positional_alternate_result] score=0.0658
POSITIONAL bphs1-ch18-042 <-> R-TBA15-917 [positional_alternate_result] score=0.0249
POSITIONAL bphs1-ch18-042 <-> R-TBA15-918 [positional_alternate_result] score=0.0683
POSITIONAL bphs1-ch18-042 <-> R-TBA15-919 [positional_alternate_result] score=0.0669
POSITIONAL bphs1-ch18-042 <-> pd-ch04-027 [positional_alternate_result] score=0.0795
POSITIONAL bphs1-ch18-042 <-> pd-ch08-062 [positional_alternate_result] score=0.0711
POSITIONAL bphs1-ch15-010 <-> R-ATEXTB-VEN-12H-DEB-V-070-02 [positional_alternate_result] score=0.0561
POSITIONAL bphs1-ch15-010 <-> R-ATEXTB-VEN-12H-EXA-V-070-03 [positional_alternate_result] score=0.0491
POSITIONAL bphs1-ch15-010 <-> R-ATEXTB-VEN-12H-LIB-V-070-01 [positional_alternate_result] score=0.0703
POSITIONAL bphs1-ch15-010 <-> R-ATEXTB-VEN-12H-V-070 [positional_alternate_result] score=0.0358
POSITIONAL bphs1-ch15-010 <-> R-TBA15-1006 [positional_alternate_result] score=0.0454
POSITIONAL bphs1-ch15-010 <-> R-TBA15-1007 [positional_alternate_result] score=0.0820
POSITIONAL bphs1-ch15-010 <-> R-TBA15-1008 [positional_alternate_result] score=0.1105
POSITIONAL bphs1-ch15-010 <-> R-TBA15-1009 [positional_alternate_result] score=0.0818
POSITIONAL bphs1-ch15-010 <-> R-TBA15-1010 [positional_alternate_result] score=0.1156
POSITIONAL bphs1-ch15-010 <-> R-TBA15-1011 [positional_alternate_result] score=0.1140
POSITIONAL bphs1-ch15-010 <-> R-TBA15-1012 [positional_alternate_result] score=0.1009
POSITIONAL bphs1-ch15-010 <-> R-TBA15-1013 [positional_alternate_result] score=0.0730
POSITIONAL bphs1-ch15-010 <-> R-TBA15-1014 [positional_alternate_result] score=0.0606
POSITIONAL bphs1-ch15-010 <-> pd-ch08-073 [positional_alternate_result] score=0.1062
POSITIONAL bphs1-ch18-038 <-> R-ATEXTB-VEN-2H-002 [positional_alternate_result] score=0.0904
POSITIONAL bphs1-ch18-038 <-> R-ATEXTB-VEN-2H-DEB-V-060-01 [positional_alternate_result] score=0.0156
POSITIONAL bphs1-ch18-038 <-> R-ATEXTB-VEN-2H-ENE-V-060-02 [positional_alternate_result] score=0.0197
POSITIONAL bphs1-ch18-038 <-> R-ATEXTB-VEN-2H-EXA-V-060-03 [positional_alternate_result] score=0.0181
POSITIONAL bphs1-ch18-038 <-> R-ATEXTB-VEN-2H-V-060 [positional_alternate_result] score=0.0351
POSITIONAL bphs1-ch18-038 <-> R-TBA15-920 [positional_alternate_result] score=0.0409
POSITIONAL bphs1-ch18-038 <-> R-TBA15-921 [positional_alternate_result] score=0.0563
POSITIONAL bphs1-ch18-038 <-> R-TBA15-922 [positional_alternate_result] score=0.0602
POSITIONAL bphs1-ch18-038 <-> R-TBA15-923 [positional_alternate_result] score=0.0686
POSITIONAL bphs1-ch18-038 <-> R-TBA15-924 [positional_alternate_result] score=0.0479
POSITIONAL bphs1-ch18-038 <-> R-TBA15-925 [positional_alternate_result] score=0.0452
POSITIONAL bphs1-ch18-038 <-> R-TBA15-926 [positional_alternate_result] score=0.0689
POSITIONAL bphs1-ch18-038 <-> R-TBA15-927 [positional_alternate_result] score=0.0495
POSITIONAL bphs1-ch18-038 <-> R-TBA15-928 [positional_alternate_result] score=0.0515
POSITIONAL bphs1-ch18-038 <-> R-TBA15-929 [positional_alternate_result] score=0.0268
POSITIONAL bphs1-ch18-038 <-> pd-ch08-063 [positional_alternate_result] score=0.0770
POSITIONAL bphs1-ch18-041 <-> R-ATEXTB-VEN-5H-CAN-V-063-01 [positional_alternate_result] score=0.0414
POSITIONAL bphs1-ch18-041 <-> R-ATEXTB-VEN-5H-DEB-V-063-03 [positional_alternate_result] score=0.0318
POSITIONAL bphs1-ch18-041 <-> R-ATEXTB-VEN-5H-V-063 [positional_alternate_result] score=0.0332
POSITIONAL bphs1-ch18-041 <-> R-ATEXTB-VEN-5H-VIR-V-063-02 [positional_alternate_result] score=0.0216
POSITIONAL bphs1-ch18-041 <-> R-TBA15-942 [positional_alternate_result] score=0.0465
POSITIONAL bphs1-ch18-041 <-> R-TBA15-943 [positional_alternate_result] score=0.0711
POSITIONAL bphs1-ch18-041 <-> R-TBA15-944 [positional_alternate_result] score=0.0993
POSITIONAL bphs1-ch18-041 <-> R-TBA15-945 [positional_alternate_result] score=0.1124
POSITIONAL bphs1-ch18-041 <-> R-TBA15-946 [positional_alternate_result] score=0.0948
POSITIONAL bphs1-ch18-041 <-> R-TBA15-947 [positional_alternate_result] score=0.0633
POSITIONAL bphs1-ch18-041 <-> pd-ch08-066 [positional_alternate_result] score=0.0899
POSITIONAL bphs1-ch18-003 <-> R-300IMP-VEN-7H-132 [positional_alternate_result] score=0.1441
POSITIONAL bphs1-ch18-003 <-> R-ATEXTB-VEN-7H-AQU-V-065-01 [positional_alternate_result] score=0.0225
POSITIONAL bphs1-ch18-003 <-> R-ATEXTB-VEN-7H-ARI-V-065-02 [positional_alternate_result] score=0.0227
POSITIONAL bphs1-ch18-003 <-> R-ATEXTB-VEN-7H-CAP-V-065-03 [positional_alternate_result] score=0.0206
POSITIONAL bphs1-ch18-003 <-> R-ATEXTB-VEN-7H-DEB-V-065-06 [positional_alternate_result] score=0.0217
POSITIONAL bphs1-ch18-003 <-> R-ATEXTB-VEN-7H-ENE-V-065-07 [positional_alternate_result] score=0.0217
POSITIONAL bphs1-ch18-003 <-> R-ATEXTB-VEN-7H-EXA-V-065-08 [positional_alternate_result] score=0.0243
POSITIONAL bphs1-ch18-003 <-> R-ATEXTB-VEN-7H-LEO-V-065-04 [positional_alternate_result] score=0.0256
POSITIONAL bphs1-ch18-003 <-> R-ATEXTB-VEN-7H-OWN-V-065-09 [positional_alternate_result] score=0.0319
POSITIONAL bphs1-ch18-003 <-> R-ATEXTB-VEN-7H-SCO-V-065-05 [positional_alternate_result] score=0.0218
POSITIONAL bphs1-ch18-003 <-> R-ATEXTB-VEN-7H-V-065 [positional_alternate_result] score=0.0360
POSITIONAL bphs1-ch18-003 <-> R-TBA15-953 [positional_alternate_result] score=0.0433
POSITIONAL bphs1-ch18-003 <-> R-TBA15-954 [positional_alternate_result] score=0.1247
POSITIONAL bphs1-ch18-003 <-> R-TBA15-955 [positional_alternate_result] score=0.1437
POSITIONAL bphs1-ch18-003 <-> R-TBA15-956 [positional_alternate_result] score=0.1431
POSITIONAL bphs1-ch18-003 <-> R-TBA15-957 [positional_alternate_result] score=0.1462
POSITIONAL bphs1-ch18-003 <-> R-TBA15-958 [positional_alternate_result] score=0.1033
POSITIONAL bphs1-ch18-003 <-> R-TBA15-959 [positional_alternate_result] score=0.1168
POSITIONAL bphs1-ch18-003 <-> R-TBA15-960 [positional_alternate_result] score=0.1169
POSITIONAL bphs1-ch18-003 <-> R-TBA15-961 [positional_alternate_result] score=0.1165
POSITIONAL bphs1-ch18-003 <-> R-TBA15-962 [positional_alternate_result] score=0.1162
POSITIONAL bphs1-ch18-003 <-> R-TBA15-963 [positional_alternate_result] score=0.1044
POSITIONAL bphs1-ch18-003 <-> R-TBA15-964 [positional_alternate_result] score=0.1049
POSITIONAL bphs1-ch18-003 <-> R-TBA15-965 [positional_alternate_result] score=0.1483
POSITIONAL bphs1-ch18-003 <-> R-TBA15-966 [positional_alternate_result] score=0.1053
POSITIONAL bphs1-ch18-003 <-> R-TBA15-967 [positional_alternate_result] score=0.0899
POSITIONAL bphs1-ch18-003 <-> R-TBA15-968 [positional_alternate_result] score=0.0499
POSITIONAL bphs1-ch18-003 <-> R-TBA15-969 [positional_alternate_result] score=0.1035
POSITIONAL bphs1-ch18-003 <-> R-TBA15-970 [positional_alternate_result] score=0.1020
POSITIONAL bphs1-ch18-003 <-> lalkitab-ch27-wave-w10 [positional_alternate_result] score=0.0709
POSITIONAL bphs1-ch18-003 <-> lalkitab-ch27-wave-w38 [positional_alternate_result] score=0.0447
POSITIONAL bphs1-ch18-003 <-> pd-ch08-068 [positional_alternate_result] score=0.1413
POSITIONAL bphs1-ch18-003 <-> pd-ch10-007 [positional_alternate_result] score=0.1774
POSITIONAL bphs1-ch18-017 <-> R-300IMP-VEN-7H-132 [positional_alternate_result] score=0.0824
POSITIONAL bphs1-ch18-017 <-> R-ATEXTB-VEN-7H-AQU-V-065-01 [positional_alternate_result] score=0.0193
POSITIONAL bphs1-ch18-017 <-> R-ATEXTB-VEN-7H-ARI-V-065-02 [positional_alternate_result] score=0.0195
POSITIONAL bphs1-ch18-017 <-> R-ATEXTB-VEN-7H-CAP-V-065-03 [positional_alternate_result] score=0.0155
POSITIONAL bphs1-ch18-017 <-> R-ATEXTB-VEN-7H-DEB-V-065-06 [positional_alternate_result] score=0.0214
POSITIONAL bphs1-ch18-017 <-> R-ATEXTB-VEN-7H-ENE-V-065-07 [positional_alternate_result] score=0.0214
POSITIONAL bphs1-ch18-017 <-> R-ATEXTB-VEN-7H-EXA-V-065-08 [positional_alternate_result] score=0.0127
POSITIONAL bphs1-ch18-017 <-> R-ATEXTB-VEN-7H-LEO-V-065-04 [positional_alternate_result] score=0.0228
POSITIONAL bphs1-ch18-017 <-> R-ATEXTB-VEN-7H-OWN-V-065-09 [positional_alternate_result] score=0.0196
POSITIONAL bphs1-ch18-017 <-> R-ATEXTB-VEN-7H-SCO-V-065-05 [positional_alternate_result] score=0.0146
POSITIONAL bphs1-ch18-017 <-> R-ATEXTB-VEN-7H-V-065 [positional_alternate_result] score=0.0207
POSITIONAL bphs1-ch18-017 <-> R-TBA15-953 [positional_alternate_result] score=0.0258
POSITIONAL bphs1-ch18-017 <-> R-TBA15-954 [positional_alternate_result] score=0.0579
POSITIONAL bphs1-ch18-017 <-> R-TBA15-955 [positional_alternate_result] score=0.0733
POSITIONAL bphs1-ch18-017 <-> R-TBA15-956 [positional_alternate_result] score=0.0730
POSITIONAL bphs1-ch18-017 <-> R-TBA15-957 [positional_alternate_result] score=0.0746
POSITIONAL bphs1-ch18-017 <-> R-TBA15-958 [positional_alternate_result] score=0.0546
POSITIONAL bphs1-ch18-017 <-> R-TBA15-959 [positional_alternate_result] score=0.0609
POSITIONAL bphs1-ch18-017 <-> R-TBA15-960 [positional_alternate_result] score=0.0610
POSITIONAL bphs1-ch18-017 <-> R-TBA15-961 [positional_alternate_result] score=0.0608
POSITIONAL bphs1-ch18-017 <-> R-TBA15-962 [positional_alternate_result] score=0.0606
POSITIONAL bphs1-ch18-017 <-> R-TBA15-963 [positional_alternate_result] score=0.0545
POSITIONAL bphs1-ch18-017 <-> R-TBA15-964 [positional_alternate_result] score=0.0553
POSITIONAL bphs1-ch18-017 <-> R-TBA15-965 [positional_alternate_result] score=0.0758
POSITIONAL bphs1-ch18-017 <-> R-TBA15-966 [positional_alternate_result] score=0.0631
POSITIONAL bphs1-ch18-017 <-> R-TBA15-967 [positional_alternate_result] score=0.0443
POSITIONAL bphs1-ch18-017 <-> R-TBA15-968 [positional_alternate_result] score=0.0313
POSITIONAL bphs1-ch18-017 <-> R-TBA15-969 [positional_alternate_result] score=0.0462
POSITIONAL bphs1-ch18-017 <-> R-TBA15-970 [positional_alternate_result] score=0.0537
POSITIONAL bphs1-ch18-017 <-> lalkitab-ch27-wave-w10 [positional_alternate_result] score=0.0267
POSITIONAL bphs1-ch18-017 <-> lalkitab-ch27-wave-w38 [positional_alternate_result] score=0.0282
POSITIONAL bphs1-ch18-017 <-> pd-ch08-068 [positional_alternate_result] score=0.0925
POSITIONAL bphs1-ch18-017 <-> pd-ch10-007 [positional_polarity_conflict] score=0.0996
POSITIONAL bphs1-ch32-024 <-> R-300IMP-VEN-7H-132 [positional_alternate_result] score=0.1117
POSITIONAL bphs1-ch32-024 <-> R-ATEXTB-VEN-7H-AQU-V-065-01 [positional_alternate_result] score=0.0200
POSITIONAL bphs1-ch32-024 <-> R-ATEXTB-VEN-7H-ARI-V-065-02 [positional_alternate_result] score=0.0201
POSITIONAL bphs1-ch32-024 <-> R-ATEXTB-VEN-7H-CAP-V-065-03 [positional_alternate_result] score=0.0153
POSITIONAL bphs1-ch32-024 <-> R-ATEXTB-VEN-7H-DEB-V-065-06 [positional_alternate_result] score=0.0379
POSITIONAL bphs1-ch32-024 <-> R-ATEXTB-VEN-7H-ENE-V-065-07 [positional_alternate_result] score=0.0379
POSITIONAL bphs1-ch32-024 <-> R-ATEXTB-VEN-7H-EXA-V-065-08 [positional_alternate_result] score=0.0226
POSITIONAL bphs1-ch32-024 <-> R-ATEXTB-VEN-7H-LEO-V-065-04 [positional_alternate_result] score=0.0289
POSITIONAL bphs1-ch32-024 <-> R-ATEXTB-VEN-7H-OWN-V-065-09 [positional_alternate_result] score=0.0343
POSITIONAL bphs1-ch32-024 <-> R-ATEXTB-VEN-7H-SCO-V-065-05 [positional_alternate_result] score=0.0179
POSITIONAL bphs1-ch32-024 <-> R-ATEXTB-VEN-7H-V-065 [positional_alternate_result] score=0.0235
POSITIONAL bphs1-ch32-024 <-> R-TBA15-953 [positional_alternate_result] score=0.0452
POSITIONAL bphs1-ch32-024 <-> R-TBA15-954 [positional_alternate_result] score=0.1109
POSITIONAL bphs1-ch32-024 <-> R-TBA15-955 [positional_alternate_result] score=0.1234
POSITIONAL bphs1-ch32-024 <-> R-TBA15-956 [positional_alternate_result] score=0.1229
POSITIONAL bphs1-ch32-024 <-> R-TBA15-957 [positional_alternate_result] score=0.1255
POSITIONAL bphs1-ch32-024 <-> R-TBA15-958 [positional_alternate_result] score=0.1044
POSITIONAL bphs1-ch32-024 <-> R-TBA15-959 [positional_alternate_result] score=0.0957
POSITIONAL bphs1-ch32-024 <-> R-TBA15-960 [positional_alternate_result] score=0.0957
POSITIONAL bphs1-ch32-024 <-> R-TBA15-961 [positional_alternate_result] score=0.0954
POSITIONAL bphs1-ch32-024 <-> R-TBA15-962 [positional_alternate_result] score=0.0951
POSITIONAL bphs1-ch32-024 <-> R-TBA15-963 [positional_alternate_result] score=0.0855
POSITIONAL bphs1-ch32-024 <-> R-TBA15-964 [positional_alternate_result] score=0.1053
POSITIONAL bphs1-ch32-024 <-> R-TBA15-965 [positional_alternate_result] score=0.1355
POSITIONAL bphs1-ch32-024 <-> R-TBA15-966 [positional_alternate_result] score=0.1027
POSITIONAL bphs1-ch32-024 <-> R-TBA15-967 [positional_alternate_result] score=0.0800
POSITIONAL bphs1-ch32-024 <-> R-TBA15-968 [positional_alternate_result] score=0.0499
POSITIONAL bphs1-ch32-024 <-> R-TBA15-969 [positional_alternate_result] score=0.0759
POSITIONAL bphs1-ch32-024 <-> R-TBA15-970 [positional_alternate_result] score=0.0902
POSITIONAL bphs1-ch32-024 <-> lalkitab-ch27-wave-w10 [positional_alternate_result] score=0.0326
POSITIONAL bphs1-ch32-024 <-> lalkitab-ch27-wave-w38 [positional_alternate_result] score=0.0307
POSITIONAL bphs1-ch32-024 <-> pd-ch08-068 [positional_alternate_result] score=0.1122
POSITIONAL bphs1-ch32-024 <-> pd-ch10-007 [positional_alternate_result] score=0.1753
POSITIONAL bphs1-ch32-038 <-> R-300IMP-VEN-7H-132 [positional_alternate_result] score=0.0593
POSITIONAL bphs1-ch32-038 <-> R-ATEXTB-VEN-7H-AQU-V-065-01 [positional_alternate_result] score=0.0203
POSITIONAL bphs1-ch32-038 <-> R-ATEXTB-VEN-7H-ARI-V-065-02 [positional_alternate_result] score=0.0205
POSITIONAL bphs1-ch32-038 <-> R-ATEXTB-VEN-7H-CAP-V-065-03 [positional_alternate_result] score=0.0156
POSITIONAL bphs1-ch32-038 <-> R-ATEXTB-VEN-7H-DEB-V-065-06 [positional_alternate_result] score=0.0396
POSITIONAL bphs1-ch32-038 <-> R-ATEXTB-VEN-7H-ENE-V-065-07 [positional_alternate_result] score=0.0396
POSITIONAL bphs1-ch32-038 <-> R-ATEXTB-VEN-7H-EXA-V-065-08 [positional_alternate_result] score=0.0183
POSITIONAL bphs1-ch32-038 <-> R-ATEXTB-VEN-7H-LEO-V-065-04 [positional_alternate_result] score=0.0215
POSITIONAL bphs1-ch32-038 <-> R-ATEXTB-VEN-7H-OWN-V-065-09 [positional_alternate_result] score=0.0278
POSITIONAL bphs1-ch32-038 <-> R-ATEXTB-VEN-7H-SCO-V-065-05 [positional_alternate_result] score=0.0189
POSITIONAL bphs1-ch32-038 <-> R-ATEXTB-VEN-7H-V-065 [positional_alternate_result] score=0.0506
POSITIONAL bphs1-ch32-038 <-> R-TBA15-953 [positional_alternate_result] score=0.0535
POSITIONAL bphs1-ch32-038 <-> R-TBA15-954 [positional_alternate_result] score=0.0476
POSITIONAL bphs1-ch32-038 <-> R-TBA15-955 [positional_alternate_result] score=0.0465
POSITIONAL bphs1-ch32-038 <-> R-TBA15-956 [positional_alternate_result] score=0.0462
POSITIONAL bphs1-ch32-038 <-> R-TBA15-957 [positional_alternate_result] score=0.0472
POSITIONAL bphs1-ch32-038 <-> R-TBA15-958 [positional_alternate_result] score=0.0559
POSITIONAL bphs1-ch32-038 <-> R-TBA15-959 [positional_alternate_result] score=0.0422
POSITIONAL bphs1-ch32-038 <-> R-TBA15-960 [positional_alternate_result] score=0.0422
POSITIONAL bphs1-ch32-038 <-> R-TBA15-961 [positional_alternate_result] score=0.0421
POSITIONAL bphs1-ch32-038 <-> R-TBA15-962 [positional_alternate_result] score=0.0420
POSITIONAL bphs1-ch32-038 <-> R-TBA15-963 [positional_alternate_result] score=0.0377
POSITIONAL bphs1-ch32-038 <-> R-TBA15-964 [positional_alternate_result] score=0.0594
POSITIONAL bphs1-ch32-038 <-> R-TBA15-965 [positional_alternate_result] score=0.0596
POSITIONAL bphs1-ch32-038 <-> R-TBA15-966 [positional_alternate_result] score=0.0560
POSITIONAL bphs1-ch32-038 <-> R-TBA15-967 [positional_alternate_result] score=0.0321
POSITIONAL bphs1-ch32-038 <-> R-TBA15-968 [positional_alternate_result] score=0.0303
POSITIONAL bphs1-ch32-038 <-> R-TBA15-969 [positional_alternate_result] score=0.0297
POSITIONAL bphs1-ch32-038 <-> R-TBA15-970 [positional_alternate_result] score=0.0458
POSITIONAL bphs1-ch32-038 <-> lalkitab-ch27-wave-w10 [positional_alternate_result] score=0.0275
POSITIONAL bphs1-ch32-038 <-> lalkitab-ch27-wave-w38 [positional_alternate_result] score=0.0315
POSITIONAL bphs1-ch32-038 <-> pd-ch08-068 [positional_alternate_result] score=0.0930
POSITIONAL bphs1-ch32-038 <-> pd-ch10-007 [positional_alternate_result] score=0.0806
POSITIONAL bphs1-ch18-043 <-> R-ATEXTB-VEN-8H-DEB-V-066-04 [positional_alternate_result] score=0.0314
POSITIONAL bphs1-ch18-043 <-> R-ATEXTB-VEN-8H-EXA-V-066-05 [positional_alternate_result] score=0.0224
POSITIONAL bphs1-ch18-043 <-> R-ATEXTB-VEN-8H-LIB-V-066-01 [positional_alternate_result] score=0.0253
POSITIONAL bphs1-ch18-043 <-> R-ATEXTB-VEN-8H-PIS-V-066-02 [positional_alternate_result] score=0.0268
POSITIONAL bphs1-ch18-043 <-> R-ATEXTB-VEN-8H-TAU-V-066-03 [positional_alternate_result] score=0.0270
POSITIONAL bphs1-ch18-043 <-> R-ATEXTB-VEN-8H-V-066 [positional_alternate_result] score=0.0560
POSITIONAL bphs1-ch18-043 <-> R-TBA15-971 [positional_alternate_result] score=0.0523
POSITIONAL bphs1-ch18-043 <-> R-TBA15-972 [positional_alternate_result] score=0.0762
POSITIONAL bphs1-ch18-043 <-> R-TBA15-973 [positional_alternate_result] score=0.0639
POSITIONAL bphs1-ch18-043 <-> R-TBA15-974 [positional_alternate_result] score=0.0925
POSITIONAL bphs1-ch18-043 <-> R-TBA15-975 [positional_alternate_result] score=0.0672
POSITIONAL bphs1-ch18-043 <-> R-TBA15-976 [positional_alternate_result] score=0.0666
POSITIONAL bphs1-ch18-043 <-> R-TBA15-977 [positional_alternate_result] score=0.0674
POSITIONAL bphs1-ch18-043 <-> R-TBA15-978 [positional_alternate_result] score=0.0633
POSITIONAL bphs1-ch18-043 <-> R-TBA15-979 [positional_alternate_result] score=0.0663
POSITIONAL bphs1-ch18-043 <-> R-TBA15-980 [positional_alternate_result] score=0.0812
POSITIONAL bphs1-ch18-043 <-> R-TBA15-981 [positional_alternate_result] score=0.0403
POSITIONAL bphs1-ch18-043 <-> pd-ch08-069 [positional_polarity_conflict] score=0.1065
POSITIONAL bphs1-ch18-046 <-> R-ATEXTB-VEN-9H-CAP-V-067-01 [positional_alternate_result] score=0.0561
POSITIONAL bphs1-ch18-046 <-> R-ATEXTB-VEN-9H-TAU-V-067-02 [positional_alternate_result] score=0.0287
POSITIONAL bphs1-ch18-046 <-> R-ATEXTB-VEN-9H-V-067 [positional_alternate_result] score=0.0461
POSITIONAL bphs1-ch18-046 <-> R-TBA15-982 [positional_alternate_result] score=0.0521
POSITIONAL bphs1-ch18-046 <-> R-TBA15-983 [positional_alternate_result] score=0.1195
POSITIONAL bphs1-ch18-046 <-> R-TBA15-984 [positional_alternate_result] score=0.0995
POSITIONAL bphs1-ch18-046 <-> R-TBA15-985 [positional_alternate_result] score=0.1149
POSITIONAL bphs1-ch18-046 <-> R-TBA15-986 [positional_alternate_result] score=0.0959
POSITIONAL bphs1-ch18-046 <-> R-TBA15-987 [positional_alternate_result] score=0.0794
POSITIONAL bphs1-ch18-046 <-> R-TBA15-988 [positional_alternate_result] score=0.0906
POSITIONAL bphs1-ch18-046 <-> R-TBA15-989 [positional_alternate_result] score=0.0315
POSITIONAL bphs1-ch18-046 <-> lalkitab-ch27-proh-07 [positional_alternate_result] score=0.0926
POSITIONAL bphs1-ch18-046 <-> pd-ch08-070 [positional_polarity_conflict] score=0.0688
POSITIONAL bphs1-ch17-020 <-> R-TBA15-1443 [positional_alternate_result] score=0.0841
POSITIONAL bphs1-ch18-004 <-> R-ATEXTB-VEN-VIR-064 [positional_polarity_conflict] score=0.1169
POSITIONAL bphs1-ch18-004 <-> R-TBA15-1488 [positional_alternate_result] score=0.1097
Dry run complete. No source JSON files were changed.
Report written to /Users/apple/DailyHoroscope-Migration/KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_bphs_vol1_phase2_vs_mongodb_positional.json

--- STEP 3/3: Triage Summary ---
Rules in BPHS Vol 1 Phase 2 (A):   1456
Rules in MongoDB export (B):         9968
Pairs evaluated:                     14,513,408

TF-IDF similarity matches:           19
Contradiction pairs:                 0
Positional conflicts:                2387

TRIAGE BREAKDOWN:
  self-match artifacts         : 0  (should be 0 with fixed export script)
  positional_polarity_conflict : 29  (PATCH -- genuine cross-system conflict)
  positional_alternate_result  : 2358  (REVIEW -- contextual, no patch)

SIMILARITY MATCHES:
  [near_identical] bphs1-ch16-007 <-> R-BPHS16-008  score=0.9259
    A: If the 5th lord is in fall and be not in aspect to the 5th while Saturn and Mercury are in the 5th, the native's wife wi
    B: Condition: If the 5th lord is in fall and be not in aspect to the 5th while Saturn and Mercury are in the 5th

Effect: t
  [near_identical] bphs1-ch14-009 <-> R-BPHS14-022  score=0.9114
    A: If Mercury is in the 3rd while the 3rd lord and Moon are together as the indicator (Mars) joins Saturn, the effects are:
    B: Condition: If Mercury is in the 3rd while the 3rd lord and Moon are together as the indicator (Mars) joins Saturn

Effec
  [near_identical] bphs1-ch14-010 <-> R-BPHS14-023  score=0.9019
    A: Should Mars and Rahu be conjunct while the 3rd lord is in his sign of debilitation, there will be loss of younger brothe
    B: Condition: Should Mars and Rahu be conjunct while the 3rd lord is in his sign of debilitation

Effect: there will be los
  [partial_overlap] bphs1-ch15-014 <-> R-BPHS15-019  score=0.8858
    A: Should a benefic be in the 4th, aspect the 4th, or is conjunct with or aspect the lord of the 4th house, then the native
    B: Condition: Should a benefic be in the 4th, aspect the 4th, or is conjunct with or aspect the lord of the 4th house

Effe
  [partial_overlap] bphs1-ch16-025 <-> R-BPHS16-034  score=0.8801
    A: There will be 10 sons if the 4th and the 6th are occupied by malefics while the 5th lord is in deep exaltation joining t
    B: Condition: The 4th and the 6th are occupied by malefics while the 5th lord is in deep exaltation joining the ascendant l
  [partial_overlap] bphs1-ch16-005 <-> R-BPHS16-006  score=0.8765
    A: If the 5th lord is in the 6th as the ascendant lord is conjunct Mars, the native will lose his very first child whereaft
    B: Condition: If the 5th lord is in the 6th as the ascendant lord is conjunct Mars

Effect: the native will lose his very f
  [partial_overlap] bphs1-ch16-012 <-> R-BPHS16-015  score=0.8729
    A: Adopted issue is indicated if the 5th is tenanted by six planets while its lord is in the 12th, and the Moon and ascenda
    B: Condition: The 5th is tenanted by six planets while its lord is in the 12th, and the Moon and ascendant are endowed with
  [partial_overlap] bphs1-ch13-014 <-> R-BPHS13-014  score=0.8664
    A: There will be penury right from birth and the native will have to beg even for his food if the lords of the 2nd and the 
    B: Condition: The lords of the 2nd and the 11th are both combust or be with malefics

Effect: There will be penury right fr
  [partial_overlap] bphs1-ch15-011 <-> R-BPHS15-014  score=0.8617
    A: Should the Sun be in the 4th house as the 4th lord is exalted and be with Venus, one will acquire conveyances in his 32n
    B: Condition: Should the Sun be in the 4th house, as the 4th lord is exalted and be with Venus

Effect: one will acquire co
  [partial_overlap] bphs1-ch16-006 <-> R-BPHS16-007  score=0.8611
    A: Should the 5th lord be in fall in the 6th, 8th or the 12th while Mercury and Ketu are in the 5th, the native's wife will
    B: Condition: Should the 5th lord be in fall in the 6th, 8th or the 12th while Mercury and Ketu are in the 5th

Effect: the
  [partial_overlap] bphs1-ch16-009 <-> R-BPHS16-012  score=0.8602
    A: If the 5th lord is in the 6th, 8th or the 12th or be in an inimical sign or be in fall or in the 5th itself, the native 
    B: Condition: If the 5th lord is in the 6th, 8th or the 12th or be in an inimical sign or in fall or in the 5th itself

Eff
  [partial_overlap] bphs1-ch16-021 <-> R-BPHS16-029  score=0.8589
    A: If Jupiter is in the 9th from the ascendant while Venus is in the 9th from Jupiter along with the ascendant lord, one wi
    B: Condition: Jupiter is in the 9th from the ascendant while Venus is in the 9th from Jupiter along with the ascendant lord
  [partial_overlap] bphs1-ch16-003 <-> R-BPHS16-003  score=0.8475
    A: Should the lord of the 5th be combust or be with malefics and be weak, there will be no children; even if per chance iss
    B: Condition: Should the 5th lord be combust or be with malefics and be weak

Effect: there will be no children; even if pe
  [partial_overlap] bphs1-ch15-007 <-> R-BPHS15-010  score=0.8457
    A: The native's mother will be happy if the 4th lord is in an angle while Venus is also in an angle as Mercury is exalted.
    B: Condition: The 4th lord is in an angle while Venus is also in an angle as Mercury is exalted

Effect: The native's mothe
  [partial_overlap] bphs1-ch14-013 <-> R-BPHS14-026  score=0.8414
    A: If the Moon is lonely placed in the 3rd in aspect to male planets, there will be younger brothers.
    B: Condition: The Moon is lonely placed in the 3rd in aspect to male planets

Effect: There will be younger brothers.
  [partial_overlap] bphs1-ch15-012 <-> R-BPHS15-015  score=0.8332
    A: It will be in the 42nd year that one will be endowed with conveyances if the 4th lord joins the 10th lord in his (4th lo
    B: Condition: It will be in the 42nd year that one will be endowed with conveyances if the 4th lord joins the 10th lord in 
  [partial_overlap] bphs1-ch16-001 <-> R-BPHS16-001  score=0.8314
    A: If the lords of the ascendant and the 5th are in their own signs or in an angle or in a trine, one will enjoy thorough h
    B: Condition: If the lords of the ascendant and the 5th are in their own signs or in an angle or in a trine

Effect: one wi
  [partial_overlap] bphs1-ch15-009 <-> R-BPHS15-012  score=0.8257
    A: Should the 4th house be a movable one while its lord and Mars are together in the 6th or the 8th house, the native will 
    B: Condition: Should the 4th house be a movable one while its lord and Mars are together in the 6th or the 8th house

Effec
  [partial_overlap] bphs1-ch15-005 <-> R-BPHS15-008  score=0.8247
    A: Should Mercury be in the ascendant while the 4th lord being a benefic is aspected by another benefic, the native will be
    B: Condition: Mercury in the ascendant while the 4th lord being a benefic is aspected by another benefic

Effect: The nativ

GENUINE POLARITY CONFLICTS (action required):
  [jupiter in house 1]  (2 pair(s))
    bphs1-ch12-012 vs kp-ch12-002
      A pol: positive  B pol: negative
      A: The native will be endowed with royal marks (Rajалакшанам -- the 32 auspicious bodily marks of greatness) if Mercury, Jup
      B: Position of Jupiter in Virgo shall be detrimental for longevity as maraca and badhaka lord is in lagna.
    bphs1-ch17-012 vs kp-ch12-002
      A pol: positive  B pol: negative
      A: Jupiter in similar case (6th and 8th lords in the ascendant with Jupiter) will destroy any disease. Jupiter's natural be
      B: Position of Jupiter in Virgo shall be detrimental for longevity as maraca and badhaka lord is in lagna.
  [jupiter in house 7]  (3 pair(s))
    bphs1-ch18-012 vs pd-ch08-056
      A pol: negative  B pol: positive
      A: Wife of a Brahmin or a pregnant female will be in the native's association if Jupiter is in the 7th house. Jupiter's dha
      B: Jupiter placed in the 7th house (Kalatra Bhava -- house of spouse) produces very favorable outcomes. The wife and sons ar
    bphs1-ch18-016 vs kp-ch12-001
      A pol: positive  B pol: negative
      A: Jupiter will bring a spouse with hard and prominent breasts. Jupiter's association with fullness, expansion, and physica
      B: For Virgo (Kanya) lagna, Jupiter is lord of 07th house and it is the badhaka. This is because Virgo is a dual (dwi-swabh
    bphs1-ch18-016 vs pd-ch10-009
      A pol: positive  B pol: negative
      A: Jupiter will bring a spouse with hard and prominent breasts. Jupiter's association with fullness, expansion, and physica
      B: When Jupiter occupies the 7th house and is in depression (Neecha -- Capricorn/Makara), the native's wife will die. Jupite
  [mars in house 6]  (2 pair(s))
    bphs1-ch17-019 vs pd-ch08-031
      A pol: negative  B pol: positive
      A: One will suffer from severe fever at the age of 6 and at the age of 12 if Mars is in the 6th house while the 6th lord is
      B: Mars placed in the 6th house (Ripu Bhava -- house of enemies, diseases, and competition) produces remarkably positive out
    bphs1-ch18-049 vs pd-ch08-031
      A pol: negative  B pol: positive
      A: If the 6th, 7th, and 8th houses are in their order occupied by Mars, Rahu, and Saturn respectively, the native's wife wi
      B: Mars placed in the 6th house (Ripu Bhava -- house of enemies, diseases, and competition) produces remarkably positive out
  [mars in house 7]  (3 pair(s))
    bphs1-ch18-010 vs R-ATEXTB-MAR-7H-004
      A pol: negative  B pol: positive
      A: Mars placed in the 7th will denote association with marriageable girls (those who have come of age or are in their month
      B: When the Moon and Venus are in opposition to Mars and Saturn, and either Mars or Saturn is located in the 7th house rela
    bphs1-ch18-014 vs pd-ch08-032
      A pol: positive  B pol: negative
      A: Mars in the 7th denotes a spouse (or female associate) with attractive breasts. Mars's association with physical energy,
      B: Mars placed in the 7th house (Kalatra Bhava -- house of spouse, partnerships, and marriage) produces adverse outcomes. Th
    bphs1-ch18-027 vs R-ATEXTB-MAR-7H-004
      A pol: negative  B pol: positive
      A: If Mars and Venus are in the 7th house, the native will have three wives. The dual presence of the planet of desire (Ven
      B: When the Moon and Venus are in opposition to Mars and Saturn, and either Mars or Saturn is located in the 7th house rela
  [mercury in house 1]  (1 pair(s))
    bphs1-ch17-011 vs pd-ch08-038
      A pol: negative  B pol: positive
      A: Mercury so featuring (i.e. 6th and 8th lords in the ascendant with Mercury) will bring in bilious diseases like jaundice
      B: Mercury placed in the 1st house (Lagna) produces excellent outcomes, as Mercury is a natural benefic and the karaka of i
  [mercury in house 7]  (1 pair(s))
    bphs1-ch18-011 vs pd-ch08-044
      A pol: negative  B pol: positive
      A: Mercury in the 7th indicates association with harlots, mean females, and females belonging to the traders' community. Me
      B: Mercury placed in the 7th house (Kalatra Bhava -- house of spouse and partnerships) produces highly positive outcomes. Th
  [moon in house 1]  (4 pair(s))
    bphs1-ch17-006 vs pd-ch08-013
      A pol: negative  B pol: positive
      A: If the Moon is in the ascendant -- provided that ascendant is not Cancer -- and is conjunct Rahu, white leprosy will affli
      B: The Moon placed in the 1st house (Lagna) when waxing (Shukla paksha -- bright half, Tithi 1-15 from Amavasya to Purnima) 
    bphs1-ch17-007 vs pd-ch08-013
      A pol: negative  B pol: positive
      A: Saturn in place of Rahu -- i.e. Saturn conjunct the Moon in the ascendant (instead of Rahu) -- will cause black leprosy. T
      B: The Moon placed in the 1st house (Lagna) when waxing (Shukla paksha -- bright half, Tithi 1-15 from Amavasya to Purnima) 
    bphs1-ch17-008 vs pd-ch08-013
      A pol: negative  B pol: positive
      A: Mars similarly (in place of Rahu or Saturn) conjunct the Moon in the ascendant will afflict the native with blood-lepros
      B: The Moon placed in the 1st house (Lagna) when waxing (Shukla paksha -- bright half, Tithi 1-15 from Amavasya to Purnima) 
    bphs1-ch17-017 vs pd-ch08-013
      A pol: negative  B pol: positive
      A: The Moon (with the 6th and 8th lords in the ascendant) will inflict dangers through water and phlegmatic disorders -- cou
      B: The Moon placed in the 1st house (Lagna) when waxing (Shukla paksha -- bright half, Tithi 1-15 from Amavasya to Purnima) 
  [moon in house 5]  (1 pair(s))
    bphs1-ch18-018 vs pd-ch08-018
      A pol: negative  B pol: positive
      A: Malefics in the 12th and 7th while the Moon (decreasing/waning) is in the 5th house -- the native will be controlled by h
      B: The Moon placed in the 5th house (Putra Bhava -- house of children, intelligence, and creativity) produces excellent resu
  [moon in house 7]  (1 pair(s))
    bphs1-ch18-025 vs pd-ch08-020
      A pol: negative  B pol: positive
      A: If the Moon is in the 7th as the 7th lord is in the 12th and the Karaka (Venus -- indicator of wife) is bereft of strengt
      B: The Moon placed in the 7th house (Kalatra Bhava -- house of spouse and partnerships) produces highly favorable results fo
  [saturn in house 1]  (1 pair(s))
    bphs1-ch17-014 vs pd-ch08-074
      A pol: negative  B pol: positive
      A: Saturn (with the 6th and 8th lords in the ascendant) will cause windy diseases -- conditions such as rheumatism, arthriti
      B: Saturn placed in the 1st house (Lagna) in exaltation (Tula/Libra) or its own signs (Makara/Capricorn or Kumbha/Aquarius)
  [saturn in house 2]  (1 pair(s))
    bphs1-ch42-019 vs R-BRIHAT-SAT-2H-257
      A pol: negative  B pol: positive
      A: 
      B: When Mars and Saturn reside jointly in the second house, the individual's financial prosperity shall face ruin.
  [saturn in house 9]  (1 pair(s))
    bphs1-ch16-028 vs pd-ch08-083
      A pol: positive  B pol: negative
      A: Seven sons will be born, with twins occurring twice among them, if Saturn is in the 9th house from the ascendant while t
      B: Saturn placed in the 9th house (Dharma Bhava -- house of fortune, father, religion, and merit) produces a comprehensive d
  [sun in house 3]  (1 pair(s))
    bphs1-ch14-015 vs R-BRIHAT-SUN-3H-177
      A pol: negative  B pol: positive
      A: The Sun in the 3rd will destroy the preborn. Sage Bhrigu also opines that the Sun in the 3rd house will not allow the na
      B: When the Sun traverses the 3rd house from the Moon, it is deemed auspicious. However, this benefic influence may be dimi
  [sun in house 7]  (1 pair(s))
    bphs1-ch18-031 vs pd-ch08-007
      A pol: positive  B pol: negative
      A: If the Sun is in the 7th while his dispositor is conjunct Venus, there will be marriage at the 7th or 11th year of age. 
      B: The Sun placed in the 7th house (Kalatra Bhava) produces a restless, wandering life. The native is deprived of a wife or
  [venus in house 1]  (2 pair(s))
    bphs1-ch17-013 vs pd-ch04-027
      A pol: negative  B pol: positive
      A: Similarly, Venus (with the 6th and 8th lords in the ascendant) will cause diseases through females/sexual union. Venus g
      B: When Venus alone occupies the Lagna -- with no other planet in conjunction with Venus in the Lagna, and no other planet a
    bphs1-ch17-013 vs pd-ch08-062
      A pol: negative  B pol: positive
      A: Similarly, Venus (with the 6th and 8th lords in the ascendant) will cause diseases through females/sexual union. Venus g
      B: Venus placed in the 1st house (Lagna) produces excellent outcomes for physical wellbeing and happiness. The body is heal
  [venus in house 7]  (1 pair(s))
    bphs1-ch18-017 vs pd-ch10-007
      A pol: positive  B pol: negative
      A: Venus will bring one (spouse) with full and excellent breasts. Venus's signification of beauty, charm, and sensual appea
      B: When Venus occupies Vrischika (Scorpio) and that sign is the 7th house (which occurs for Taurus Lagna natives), the wife
  [venus in house 8]  (1 pair(s))
    bphs1-ch18-043 vs pd-ch08-069
      A pol: negative  B pol: positive
      A: Loss of wife will occur in the 18th year or 33rd year of age of the native if the 7th lord is in fall (debilitation) whi
      B: Venus placed in the 8th house (Ayu Bhava) produces surprisingly elevated outcomes -- another example of a benefic produci
  [venus in house 9]  (1 pair(s))
    bphs1-ch18-046 vs pd-ch08-070
      A pol: negative  B pol: positive
      A: If Venus is in the 9th while his dispositor is in a sign of Saturn (Capricorn or Aquarius), death of wife will take plac
      B: Venus placed in the 9th house (Dharma Bhava) produces well-rounded positive outcomes. The native is blessed with wife, f
  [venus in sign virgo]  (1 pair(s))
    bphs1-ch18-004 vs R-ATEXTB-VEN-VIR-064
      A pol: negative  B pol: positive
      A: Venus debilitated -- in any house of the horoscope -- will cause loss of wife (death or separation). Venus is the primary 
      B: When Venus is positioned in Virgo, it can indicate wealth, especially if it is in the 12th house. However, if it is retr

CONTEXTUAL ALTERNATE RESULTS (review-only):
  [benefic in house 10]  (2 pair(s))
    bphs1-ch36-005 vs pd-ch06-021  score=0.1588
    bphs1-ch36-005 vs pd-ch16-049  score=0.2371
  [jupiter in house 1]  (72 pair(s))
    bphs1-ch12-012 vs R-ATEXTB-JUP-1H-ARI-V-048-01  score=0.0271
    bphs1-ch12-012 vs R-ATEXTB-JUP-1H-CAP-V-048-02  score=0.0287
    bphs1-ch12-012 vs R-ATEXTB-JUP-1H-DEB-V-048-09  score=0.0262
    ... and 69 more
  [jupiter in house 11]  (11 pair(s))
    bphs1-ch32-042 vs R-ATEXTB-JUP-11H-007  score=0.0569
    bphs1-ch32-042 vs R-ATEXTB-JUP-11H-CAN-V-057-01  score=0.0579
    bphs1-ch32-042 vs R-ATEXTB-JUP-11H-DEB-V-057-02  score=0.0716
    ... and 8 more
  [jupiter in house 2]  (69 pair(s))
    bphs1-ch13-007 vs R-ATEXTB-JUP-2H-DEB-V-049-03  score=0.0201
    bphs1-ch13-007 vs R-ATEXTB-JUP-2H-EXA-V-049-04  score=0.0280
    bphs1-ch13-007 vs R-ATEXTB-JUP-2H-OWN-V-049-05  score=0.0280
    ... and 66 more
  [jupiter in house 5]  (66 pair(s))
    bphs1-ch16-019 vs R-ATEXTB-JUP-5H-ARI-V-052-01  score=0.0196
    bphs1-ch16-019 vs R-ATEXTB-JUP-5H-DEB-V-052-02  score=0.0319
    bphs1-ch16-019 vs R-ATEXTB-JUP-5H-EXA-V-052-03  score=0.0232
    ... and 63 more
  [jupiter in house 7]  (39 pair(s))
    bphs1-ch18-012 vs R-ATEXTB-JUP-7H-AQU-V-054-01  score=0.0479
    bphs1-ch18-012 vs R-ATEXTB-JUP-7H-CAP-V-054-02  score=0.0531
    bphs1-ch18-012 vs R-ATEXTB-JUP-7H-DEB-V-054-04  score=0.0350
    ... and 36 more
  [jupiter in house 9]  (70 pair(s))
    bphs1-ch32-040 vs R-ATEXTB-JUP-9H-ARI-V-055-01  score=0.0097
    bphs1-ch32-040 vs R-ATEXTB-JUP-9H-CAN-V-055-02  score=0.0142
    bphs1-ch32-040 vs R-ATEXTB-JUP-9H-CAP-V-055-03  score=0.0142
    ... and 67 more
  [ketu in house 1]  (56 pair(s))
    bphs1-ch17-016 vs R-ATEXTB-KET-1H-AQU-V-094-01  score=0.0319
    bphs1-ch17-016 vs R-ATEXTB-KET-1H-ARI-V-094-02  score=0.0226
    bphs1-ch17-016 vs R-ATEXTB-KET-1H-CAN-V-094-03  score=0.0287
    ... and 53 more
  [ketu in house 12]  (8 pair(s))
    bphs1-ch32-044 vs R-TBA15-1416  score=0.0469
    bphs1-ch32-044 vs R-TBA15-1417  score=0.1563
    bphs1-ch32-044 vs R-TBA15-1418  score=0.1567
    ... and 5 more
  [mars in house 1]  (43 pair(s))
    bphs1-ch17-010 vs R-ATEXTB-MAR-1H-ARI-V-024-01  score=0.0267
    bphs1-ch17-010 vs R-ATEXTB-MAR-1H-CAN-V-024-02  score=0.0138
    bphs1-ch17-010 vs R-ATEXTB-MAR-1H-CAP-V-024-03  score=0.0260
    ... and 40 more
  [mars in house 2]  (20 pair(s))
    bphs1-ch42-015 vs R-ATEXTB-MAR-2H-DEB-V-025-03  score=0.0511
    bphs1-ch42-015 vs R-ATEXTB-MAR-2H-ENE-V-025-04  score=0.0370
    bphs1-ch42-015 vs R-ATEXTB-MAR-2H-EXA-V-025-05  score=0.0322
    ... and 17 more
  [mars in house 3]  (87 pair(s))
    bphs1-ch14-017 vs R-ATEXTB-MAR-3H-ARI-V-026-01  score=0.0140
    bphs1-ch14-017 vs R-ATEXTB-MAR-3H-EXA-V-026-03  score=0.0362
    bphs1-ch14-017 vs R-ATEXTB-MAR-3H-GEM-V-026-02  score=0.0275
    ... and 84 more
  [mars in house 6]  (106 pair(s))
    bphs1-ch17-019 vs R-ATEXTB-MAR-6H-AQU-V-029-01  score=0.0242
    bphs1-ch17-019 vs R-ATEXTB-MAR-6H-ARI-V-029-02  score=0.0233
    bphs1-ch17-019 vs R-ATEXTB-MAR-6H-CAN-V-029-03  score=0.0212
    ... and 103 more
  [mars in house 7]  (117 pair(s))
    bphs1-ch18-010 vs R-ATEXTB-MAR-7H-084  score=0.0480
    bphs1-ch18-010 vs R-ATEXTB-MAR-7H-ARI-V-030-01  score=0.0436
    bphs1-ch18-010 vs R-ATEXTB-MAR-7H-CAN-V-030-02  score=0.0221
    ... and 114 more
  [mercury in house 1]  (61 pair(s))
    bphs1-ch15-005 vs R-ATEXTB-MER-1H-AQU-V-036-01  score=0.0175
    bphs1-ch15-005 vs R-ATEXTB-MER-1H-CAP-V-036-02  score=0.0145
    bphs1-ch15-005 vs R-ATEXTB-MER-1H-EXA-V-036-07  score=0.0213
    ... and 58 more
  [mercury in house 10]  (15 pair(s))
    bphs1-ch32-041 vs R-ATEXTB-MER-10H-011  score=0.0591
    bphs1-ch32-041 vs R-ATEXTB-MER-10H-DEB-V-045-02  score=0.0703
    bphs1-ch32-041 vs R-ATEXTB-MER-10H-EXA-V-045-03  score=0.0772
    ... and 12 more
  [mercury in house 2]  (22 pair(s))
    bphs1-ch42-016 vs R-ATEXTB-MER-2H-052  score=0.0187
    bphs1-ch42-016 vs R-ATEXTB-MER-2H-LEO-V-037-01  score=0.0481
    bphs1-ch42-016 vs R-ATEXTB-MER-2H-V-037  score=0.0199
    ... and 19 more
  [mercury in house 6]  (20 pair(s))
    bphs1-ch32-022 vs R-300IMP-MER-6H-142  score=0.0416
    bphs1-ch32-022 vs R-ATEXTB-MER-6H-CAN-V-041-01  score=0.0257
    bphs1-ch32-022 vs R-ATEXTB-MER-6H-DEB-V-041-02  score=0.0223
    ... and 17 more
  [mercury in house 7]  (26 pair(s))
    bphs1-ch18-011 vs R-ATEXTB-MER-7H-DEB-V-042-05  score=0.0220
    bphs1-ch18-011 vs R-ATEXTB-MER-7H-ENE-V-042-06  score=0.0220
    bphs1-ch18-011 vs R-ATEXTB-MER-7H-GEM-V-042-01  score=0.0191
    ... and 23 more
  [moon in house 1]  (208 pair(s))
    bphs1-ch17-006 vs R-ATEXTB-MOO-1H-AQU-V-013-01  score=0.0482
    bphs1-ch17-006 vs R-ATEXTB-MOO-1H-ARI-V-013-02  score=0.0593
    bphs1-ch17-006 vs R-ATEXTB-MOO-1H-CAN-V-013-03  score=0.0750
    ... and 205 more
  [moon in house 10]  (27 pair(s))
    bphs1-ch45-022 vs R-ATEXTB-MOO-10H-ARI-V-021-01  score=0.1974
    bphs1-ch45-022 vs R-ATEXTB-MOO-10H-CAN-V-021-02  score=0.1963
    bphs1-ch45-022 vs R-ATEXTB-MOO-10H-CAP-V-021-03  score=0.1952
    ... and 24 more
  [moon in house 3]  (30 pair(s))
    bphs1-ch14-013 vs R-ATEXTB-MOO-3H-DEB-V-015-01  score=0.0243
    bphs1-ch14-013 vs R-ATEXTB-MOO-3H-EXA-V-015-02  score=0.0291
    bphs1-ch14-013 vs R-ATEXTB-MOO-3H-V-015  score=0.0354
    ... and 27 more
  [moon in house 4]  (58 pair(s))
    bphs1-ch32-020 vs R-ATEXTB-MOO-4H-CAN-V-016-01  score=0.0167
    bphs1-ch32-020 vs R-ATEXTB-MOO-4H-DEB-V-016-07  score=0.0155
    bphs1-ch32-020 vs R-ATEXTB-MOO-4H-ENE-V-016-08  score=0.0354
    ... and 55 more
  [moon in house 5]  (23 pair(s))
    bphs1-ch18-018 vs R-TBA15-239  score=0.0512
    bphs1-ch18-018 vs R-TBA15-240  score=0.0376
    bphs1-ch18-018 vs R-TBA15-241  score=0.0449
    ... and 20 more
  [moon in house 6]  (33 pair(s))
    bphs1-ch17-031 vs R-ATEXTB-MOO-6H-CAN-V-017-01  score=0.0513
    bphs1-ch17-031 vs R-ATEXTB-MOO-6H-CAP-V-017-02  score=0.0617
    bphs1-ch17-031 vs R-ATEXTB-MOO-6H-DEB-V-017-08  score=0.0244
    ... and 30 more
  [moon in house 7]  (65 pair(s))
    bphs1-ch18-009 vs R-ATEXTB-MOO-7H-003  score=0.2117
    bphs1-ch18-009 vs R-ATEXTB-MOO-7H-AQU-V-018-01  score=0.0267
    bphs1-ch18-009 vs R-ATEXTB-MOO-7H-CAN-V-018-02  score=0.0101
    ... and 62 more
  [moon in house 8]  (23 pair(s))
    bphs1-ch16-016 vs R-ATEXTB-MOO-8H-CAN-V-019-01  score=0.0230
    bphs1-ch16-016 vs R-ATEXTB-MOO-8H-EXA-V-019-03  score=0.1043
    bphs1-ch16-016 vs R-ATEXTB-MOO-8H-OWN-V-019-04  score=0.1043
    ... and 20 more
  [moon in sign sagittarius]  (1 pair(s))
    bphs1-ch17-020 vs R-TBA15-1443  score=0.0841
  [rahu in house 1]  (39 pair(s))
    bphs1-ch17-015 vs R-ATEXTB-RAH-1H-AQU-V-082-01  score=0.0189
    bphs1-ch17-015 vs R-ATEXTB-RAH-1H-ARI-V-082-02  score=0.0187
    bphs1-ch17-015 vs R-ATEXTB-RAH-1H-CAN-V-082-03  score=0.0182
    ... and 36 more
  [rahu in house 2]  (9 pair(s))
    bphs1-ch18-045 vs R-ATEXTB-RAH-2H-DEB-V-083-02  score=0.0206
    bphs1-ch18-045 vs R-ATEXTB-RAH-2H-LIB-V-083-01  score=0.0280
    bphs1-ch18-045 vs R-ATEXTB-RAH-2H-V-083  score=0.0383
    ... and 6 more
  [rahu in house 5]  (14 pair(s))
    bphs1-ch16-022 vs R-300IMP-RAH-5H-088  score=0.0637
    bphs1-ch16-022 vs R-ATEXTB-RAH-5H-ARI-V-086-01  score=0.0288
    bphs1-ch16-022 vs R-ATEXTB-RAH-5H-CAN-V-086-02  score=0.0287
    ... and 11 more
  [rahu in house 6]  (16 pair(s))
    bphs1-ch17-021 vs R-ATEXTB-RAH-6H-EXA-V-087-01  score=0.0160
    bphs1-ch17-021 vs R-ATEXTB-RAH-6H-V-087  score=0.0115
    bphs1-ch17-021 vs R-BRIHAT-RAH-6H-090  score=0.1348
    ... and 13 more
  [saturn in house 1]  (109 pair(s))
    bphs1-ch12-013 vs R-ATEXTB-SAT-1H-AQU-V-071-01  score=0.0229
    bphs1-ch12-013 vs R-ATEXTB-SAT-1H-ARI-V-071-02  score=0.0725
    bphs1-ch12-013 vs R-ATEXTB-SAT-1H-CAN-V-071-03  score=0.0609
    ... and 106 more
  [saturn in house 12]  (12 pair(s))
    bphs1-ch32-043 vs R-ATEXTB-SAT-12H-EXA-V-081-01  score=0.0768
    bphs1-ch32-043 vs R-ATEXTB-SAT-12H-V-081  score=0.0442
    bphs1-ch32-043 vs R-TBA15-1180  score=0.0641
    ... and 9 more
  [saturn in house 2]  (12 pair(s))
    bphs1-ch42-019 vs R-ATEXTB-SAT-2H-V-072  score=0.0050
    bphs1-ch42-019 vs R-TBA15-1052  score=0.0134
    bphs1-ch42-019 vs R-TBA15-1053  score=0.0567
    ... and 9 more
  [saturn in house 3]  (25 pair(s))
    bphs1-ch14-016 vs R-ATEXTB-SAT-3H-AQU-V-073-01  score=0.0254
    bphs1-ch14-016 vs R-ATEXTB-SAT-3H-ARI-V-073-02  score=0.0301
    bphs1-ch14-016 vs R-ATEXTB-SAT-3H-CAP-V-073-03  score=0.0255
    ... and 22 more
  [saturn in house 6]  (32 pair(s))
    bphs1-ch17-023 vs R-300IMP-SAT-6H-121  score=0.0693
    bphs1-ch17-023 vs R-ATEXTB-SAT-6H-DEB-V-076-08  score=0.0126
    bphs1-ch17-023 vs R-ATEXTB-SAT-6H-ENE-V-076-09  score=0.0228
    ... and 29 more
  [saturn in house 7]  (124 pair(s))
    bphs1-ch18-013 vs R-ATEXTB-SAT-7H-AQU-V-077-01  score=0.0204
    bphs1-ch18-013 vs R-ATEXTB-SAT-7H-CAP-V-077-02  score=0.0205
    bphs1-ch18-013 vs R-ATEXTB-SAT-7H-EXA-V-077-09  score=0.0175
    ... and 121 more
  [saturn in house 8]  (88 pair(s))
    bphs1-ch17-028 vs R-ATEXTB-SAT-8H-DEB-V-078-01  score=0.0201
    bphs1-ch17-028 vs R-ATEXTB-SAT-8H-ENE-V-078-02  score=0.0459
    bphs1-ch17-028 vs R-ATEXTB-SAT-8H-EXA-V-078-03  score=0.0260
    ... and 85 more
  [saturn in house 9]  (18 pair(s))
    bphs1-ch16-028 vs R-ATEXTB-SAT-9H-061  score=0.0620
    bphs1-ch16-028 vs R-ATEXTB-SAT-9H-DEB-V-079-01  score=0.0163
    bphs1-ch16-028 vs R-ATEXTB-SAT-9H-EXA-V-079-02  score=0.0188
    ... and 15 more
  [sun in house 1]  (60 pair(s))
    bphs1-ch17-009 vs R-ATEXTB-SUN-1H-002  score=0.0413
    bphs1-ch17-009 vs R-ATEXTB-SUN-1H-ARI-V-001-01  score=0.0359
    bphs1-ch17-009 vs R-ATEXTB-SUN-1H-CAN-V-001-02  score=0.0360
    ... and 57 more
  [sun in house 2]  (70 pair(s))
    bphs1-ch42-017 vs R-ATEXTB-SUN-2H-AQU-V-002-01  score=0.0492
    bphs1-ch42-017 vs R-ATEXTB-SUN-2H-ARI-V-002-02  score=0.0498
    bphs1-ch42-017 vs R-ATEXTB-SUN-2H-CAN-V-002-03  score=0.0497
    ... and 67 more
  [sun in house 3]  (10 pair(s))
    bphs1-ch14-015 vs R-ATEXTB-SUN-3H-DEB-V-003-01  score=0.0180
    bphs1-ch14-015 vs R-ATEXTB-SUN-3H-V-003  score=0.0762
    bphs1-ch14-015 vs R-TBA15-041  score=0.0803
    ... and 7 more
  [sun in house 4]  (15 pair(s))
    bphs1-ch15-011 vs R-ATEXTB-SUN-4H-EXA-V-004-02  score=0.0340
    bphs1-ch15-011 vs R-ATEXTB-SUN-4H-OWN-V-004-03  score=0.0340
    bphs1-ch15-011 vs R-ATEXTB-SUN-4H-SCO-V-004-01  score=0.0247
    ... and 12 more
  [sun in house 7]  (39 pair(s))
    bphs1-ch18-008 vs R-ATEXTB-SUN-7H-CAP-V-007-01  score=0.0252
    bphs1-ch18-008 vs R-ATEXTB-SUN-7H-DEB-V-007-02  score=0.0425
    bphs1-ch18-008 vs R-ATEXTB-SUN-7H-ENE-V-007-03  score=0.0201
    ... and 36 more
  [sun in house 9]  (16 pair(s))
    bphs1-ch32-019 vs R-ATEXTB-SUN-9H-DEB-V-009-02  score=0.0156
    bphs1-ch32-019 vs R-ATEXTB-SUN-9H-ENE-V-009-03  score=0.0467
    bphs1-ch32-019 vs R-ATEXTB-SUN-9H-EXA-V-009-04  score=0.0275
    ... and 13 more
  [venus in house 1]  (70 pair(s))
    bphs1-ch17-013 vs R-ATEXTB-VEN-1H-AQU-V-059-01  score=0.0169
    bphs1-ch17-013 vs R-ATEXTB-VEN-1H-ARI-V-059-02  score=0.0183
    bphs1-ch17-013 vs R-ATEXTB-VEN-1H-CAN-V-059-03  score=0.0288
    ... and 67 more
  [venus in house 12]  (14 pair(s))
    bphs1-ch15-010 vs R-ATEXTB-VEN-12H-DEB-V-070-02  score=0.0561
    bphs1-ch15-010 vs R-ATEXTB-VEN-12H-EXA-V-070-03  score=0.0491
    bphs1-ch15-010 vs R-ATEXTB-VEN-12H-LIB-V-070-01  score=0.0703
    ... and 11 more
  [venus in house 2]  (16 pair(s))
    bphs1-ch18-038 vs R-ATEXTB-VEN-2H-002  score=0.0904
    bphs1-ch18-038 vs R-ATEXTB-VEN-2H-DEB-V-060-01  score=0.0156
    bphs1-ch18-038 vs R-ATEXTB-VEN-2H-ENE-V-060-02  score=0.0197
    ... and 13 more
  [venus in house 5]  (11 pair(s))
    bphs1-ch18-041 vs R-ATEXTB-VEN-5H-CAN-V-063-01  score=0.0414
    bphs1-ch18-041 vs R-ATEXTB-VEN-5H-DEB-V-063-03  score=0.0318
    bphs1-ch18-041 vs R-ATEXTB-VEN-5H-V-063  score=0.0332
    ... and 8 more
  [venus in house 7]  (131 pair(s))
    bphs1-ch18-003 vs R-300IMP-VEN-7H-132  score=0.1441
    bphs1-ch18-003 vs R-ATEXTB-VEN-7H-AQU-V-065-01  score=0.0225
    bphs1-ch18-003 vs R-ATEXTB-VEN-7H-ARI-V-065-02  score=0.0227
    ... and 128 more
  [venus in house 8]  (17 pair(s))
    bphs1-ch18-043 vs R-ATEXTB-VEN-8H-DEB-V-066-04  score=0.0314
    bphs1-ch18-043 vs R-ATEXTB-VEN-8H-EXA-V-066-05  score=0.0224
    bphs1-ch18-043 vs R-ATEXTB-VEN-8H-LIB-V-066-01  score=0.0253
    ... and 14 more
  [venus in house 9]  (12 pair(s))
    bphs1-ch18-046 vs R-ATEXTB-VEN-9H-CAP-V-067-01  score=0.0561
    bphs1-ch18-046 vs R-ATEXTB-VEN-9H-TAU-V-067-02  score=0.0287
    bphs1-ch18-046 vs R-ATEXTB-VEN-9H-V-067  score=0.0461
    ... and 9 more
  [venus in sign virgo]  (1 pair(s))
    bphs1-ch18-004 vs R-TBA15-1488  score=0.1097

============================================================
⚠️   29 GENUINE POLARITY CONFLICT(S) -- patch required.
    python3 backend/scripts/patch_bphs_vol1_phase2_conflicts.py \
      --mongo-url "$MONGO_URL" --dry-run
⚠️   19 SIMILARITY MATCH(ES) -- review.
============================================================

JSON report : KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_bphs_vol1_phase2_vs_mongodb_positional.json
Log saved   : KE_TEXTBOOK_DECODE/Dedup_Reports/bphs_vol1_phase2_dedup_20260603_045313.md
