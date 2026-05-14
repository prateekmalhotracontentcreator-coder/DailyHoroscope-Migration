# Scripts Index
> One-line-per-script reference. Add new scripts here immediately after creation.
> Last updated: 2026-05-08

## Ingest Scripts
| Script | Book / Scope | Status |
|---|---|---|
| ingest_bphs_houses.py | BPHS Vol 1 Ch 12-24 (house lords) | ✅ Done |
| ingest_bphs_houses_v2.py | BPHS Vol 1 Ch 12-24 revised | ✅ Done |
| ingest_bphs_ch27_v1.py | BPHS Vol 1 Ch 27 | ✅ Done |
| ingest_bphs_ch34_v1.py | BPHS Vol 1 Ch 34 | ✅ Done |
| ingest_bphs_ch35_v1.py | BPHS Vol 1 Ch 35 | ✅ Done |
| ingest_bphs_ch36_v1.py | BPHS Vol 1 Ch 36 | ✅ Done |
| ingest_bphs_ch37_v1.py | BPHS Vol 1 Ch 37 | ✅ Done |
| ingest_bphs_ch38_v1.py | BPHS Vol 1 Ch 38 | ✅ Done |
| ingest_bphs_ch39_v1.py | BPHS Vol 1 Ch 39 | ✅ Done |
| ingest_bphs_ch40_v1.py | BPHS Vol 1 Ch 40 | ✅ Done |
| ingest_bphs_ch43_v1.py | BPHS Vol 1 Ch 43 | ✅ Done |
| ingest_bphs_ch44_v1.py | BPHS Vol 1 Ch 44 | ✅ Done |
| ingest_bphs_dasha_v1.py | BPHS Vol 2 Ch 47-48 (Dasha) | ✅ Done |
| ingest_chapter15.py | TBA Ch 15 (early version) | ✅ Done |
| ingest_tba_ch15_v1.py | TBA Ch 15 revised | ✅ Done |
| ingest_tba_ch16_v1.py | TBA Ch 16 | ✅ Done |
| ingest_lalkitab_ch19_v1.py | Lal Kitab Ch 19 | ✅ Done (deduped) |
| ingest_lalkitab_ch20_v1.py | Lal Kitab Ch 20 | ✅ Done |
| ingest_lalkitab_ch21_v1.py | Lal Kitab Ch 21 | ✅ Done |
| ingest_lalkitab_ch22_v1.py | Lal Kitab Ch 22 | ✅ Done |
| ingest_lalkitab_ch23_v1.py | Lal Kitab Ch 23 | ✅ Done |
| ingest_lalkitab_ch24_v1.py | Lal Kitab Ch 24 | ✅ Done |
| ingest_lalkitab_ch24_v2.py | Lal Kitab Ch 24 revised | ✅ Done |
| ingest_lalkitab_ch25_v1.py | Lal Kitab Ch 25 | ✅ Done |
| ingest_lalkitab_ch26_v1.py | Lal Kitab Ch 26 | ✅ Done |
| ingest_lalkitab_ch27_v1.py | Lal Kitab Ch 27 | ✅ Done |
| ingest_lalkitab_ch28_v1.py | Lal Kitab Ch 28 | ✅ Done |
| ingest_lalkitab_ch29_v1.py | Lal Kitab Ch 29 | ✅ Done |
| ingest_mundane_interpretation_v22.py | Mundane -- final interpretation rules | ✅ Done |
| ingest_mundane_engine_specs_v22.py | Mundane -- final engine specs | ✅ Done |
| ingest_mundane_geo_entities_v1.py | Mundane -- geo entity seed | ✅ Done |
| ingest_mundane_v2_novel_migrate.py | Mundane -- novel rule migration | ✅ Done |
| ingest_remedies_v1.py | Remedies & Mantras (100 rules) | ✅ Done |
| ingest_remedies_dhana_v1.py | Dhana Remedies IDs 1-100 | ✅ Written -- 100/100 dry-run pass |
| ingest_remedies_gemstones_v1.py | Gemstones IDs 101-200 | ✅ Written -- 98/100 (162,164 absent from source) |
| ingest_remedies_crystals_v1.py | Crystal Remedies IDs 201-300 | ✅ Written -- 100/100 (split-array fix applied) |
| ingest_remedies_chakra_v1.py | 7 Chakra Healing IDs 301-307 | ✅ Written -- 7/7 dry-run pass |
| ingest_lk_remedies_v1.py | LK Remedies IDs 308-668 (361 total) | ✅ Written -- Gate 0 clean, 361/361, ready to upload |
| ingest_strategist_v1.py | Strategist IDs 701-1025 | ⏳ Not yet written |

## Validation Scripts
| Script | Scope | Notes |
|---|---|---|
| validate_rules.py | BPHS, TBA, Lal Kitab, Remedies | Do NOT use for Mundane |
| validate_mundane_rules.py | Mundane ONLY | Use this for all mundane batches |

## Patch / Fix Scripts
| Script | Purpose | Status |
|---|---|---|
| fix_flagged_ch27.py | BPHS Ch 27 false flag fix | ✅ Done |
| patch_ch27_summary_flags.py | BPHS Ch 27 summary flag patch | ✅ Done |
| patch_ch34_content_fixes.py | BPHS Ch 34 content patches | ✅ Done |
| patch_ch44_flags.py | BPHS Ch 44 flag fixes | ✅ Done |
| fix_ch47_sl4548.py | BPHS Ch 47 shloka 45-48 | ✅ Done |
| patch_ch53_venus_antardasha.py | BPHS Ch 53 Venus antardasha | ✅ Done |
| fix_ch56_sl7275.py | BPHS Ch 56 shloka 72-75 | ✅ Done |
| gap_fill_ch57_splits.py | BPHS Ch 57 split gaps | ✅ Done |
| fix_pending_ch20.py | LK Ch 20 pending flag fix | ✅ Done |
| patch_lalkitab_ch21_flags.py | LK Ch 21 flags | ✅ Done |
| patch_lalkitab_ch24_flags.py | LK Ch 24 flags | ✅ Done |
| patch_lalkitab_ch25_flags.py | LK Ch 25 flags | ✅ Done |
| patch_lalkitab_ch28_flags.py | LK Ch 28 flags | ✅ Done |
| patch_lalkitab_ch29_flags.py | LK Ch 29 flags | ✅ Done |
| patch_mars_h03.py | LK Mars House 3 correction | ✅ Done |
| patch_remedies_flags.py | Remedies & Mantras flag fixes | ✅ Done |
| patch_mundane_*.py (×14) | Mundane NLM-driven patches | ✅ All done |

## Approval Scripts
| Script | Purpose | Status |
|---|---|---|
| approve_mundane_*.py (×9) | Mundane category approval sweeps | ✅ All done |
| promote_mundane_auto_approved.py | Promote Mundane auto_approved → approved | ✅ Done |
| promote_mundane_phr_approved.py | Promote Mundane PHR → approved | ✅ Done |
| tag_cofounder_review_required.py | Tag 7 Mundane rules for co-founder | ✅ --apply done 2026-05-08 |
| apply_contradiction_decisions.py | Apply NLM contradiction resolutions | ✅ Done (partial) |
| apply_flagged_decisions.py | Apply NLM flagged decisions | ✅ Done (partial) |

## Migration / Maintenance Scripts
| Script | Purpose | Status |
|---|---|---|
| deprecate_pre_split_merged.py | Deprecate pre-split compound rules | ✅ Done |
| backfill_antardasha_planet.py | Backfill planet field on dasha rules | ✅ Done |
| migrate_ch41_varga_checkable.py | Ch 41 varga reclassify | ✅ Done -- production verified 2026-05-14: 24 rules updated, 0 skipped, 0 errors |
| patch_yoga_check_reclassify.py | Yoga_check tag reclassify | ✅ Done |
| dedup_lalkitab_ch19.py | Remove LK Ch 19 duplicates | ✅ Done |
| delete_lalkitab_ch19.py | Delete LK Ch 19 for re-ingest | ✅ Done |
| reset_lalkitab_ch19.py | Reset LK Ch 19 rules | ✅ Done |
| split_mundane_cat_c1_rules.py | Split compound Mundane Cat C1 | ✅ Done |
| migrate_mundane_v3_v7_conditions.py | Mundane v3→v7 condition migration | ✅ Done |
| migrate_dual_mapping_to_engine_specs.py | Dual-mapping → engine_specs | ✅ Done |
| seed_science_registry.py | Seed science registry collection | ✅ Done |
| patch_slokas.py | Sloka field standardization | ✅ Done |
| patch_punctuation.py | Punctuation cleanup | ✅ Done |

## Utility / Inspection Scripts
| Script | Purpose |
|---|---|
| peek_rules.py | Quick spot-check of rules in DB |
| review_book.py | Review all rules for a book |
| review_approved.py | Review approved rules |
| export_library_review.py | Export rules for review |
| generate_signoff_review.py | Generate co-founder signoff report |
| audit_mundane_phr_unknown.py | Audit Mundane PHR unknown category |
| inspect_mundane_cat_b.py | Inspect Mundane Cat B rules |
| inspect_cat_b_post_validation.py | Post-validation Cat B check |
| batch_ingest.py | Generic batch ingest runner |
| reconcile_contradictions.py | Contradiction reconciliation util |
| reconcile_flagged.py | Flagged rule reconciliation util |
| assess_undersplit_houses.py | Find undersplit house rules |
| verify_ch57_gaps.py | Verify Ch 57 gap fill |
| extract_book.py | Extract rules by book to file |
