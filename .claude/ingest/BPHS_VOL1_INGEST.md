# BPHS_VOL1_INGEST.md
> Last updated: 2026-05-08

## Coverage
Chapters: 12-24, 27, 34, 35-40, 43, 44
Total Rules: ~1,069 | Auto-Approved: ~628 | PHR: ~352 | Flagged: ~95

## Scripts Run
| Script | Purpose | Status |
|---|---|---|
| ingest_bphs_houses.py | Ch 12-24 (house lords) | ✅ Done |
| ingest_bphs_houses_v2.py | Revised Ch 12-24 pass | ✅ Done |
| ingest_bphs_ch27_v1.py | Ch 27 | ✅ Done |
| ingest_bphs_ch34_v1.py | Ch 34 | ✅ Done |
| ingest_bphs_ch35_v1.py → ingest_bphs_ch44_v1.py | Ch 35-44 (yoga chapters) | ✅ Done |
| validate_rules.py | Validation sweep | ✅ Done |
| fix_flagged_ch27.py | Fix false flags Ch 27 | ✅ Done |
| patch_ch27_summary_flags.py | Patch Ch 27 summary flags | ✅ Done |
| patch_ch34_content_fixes.py | Content patch Ch 34 | ✅ Done |
| patch_ch44_flags.py | Flag fixes Ch 44 | ✅ Done |
| deprecate_pre_split_merged.py | Deprecate pre-split compound rules | ✅ Done |
| apply_contradiction_decisions.py | Apply NLM contradiction resolutions | ✅ Done (partial) |
| apply_flagged_decisions.py | Apply NLM flagged decisions | ✅ Done (partial) |
| backfill_antardasha_planet.py | Backfill planet field on dasha rules | ✅ Done |
| migrate_ch41_varga_checkable.py | Ch 41 varga reclassify | ✅ Done |
| patch_yoga_check_reclassify.py | Yoga_check tag reclassify Ch 35-40 | ✅ Done |
| assess_undersplit_houses.py | Audit undersplit house rules | ✅ Done |

## Open Issues
1. **13 contradiction pairs** in Ch 12-23 → NLM queue (see BPHS_VOL1_NLM.md)
2. **Ch 15 auto-approve rate: 25%** -- worst PHR batch, priority NLM target
3. **Ch 19 auto-approve rate: 33%** -- second worst, NLM target
4. **Ch 34 flagged=15** -- confirmed false truncation pattern → bulk-approval script pending (no NLM needed)
5. **Phase 2 yoga_check audit** -- Ch 35-40 yoga rules promotability review pending

## Status
INGESTED ✅ | Split-upgrade complete ✅ | PHR triage: IN PROGRESS via NLM
