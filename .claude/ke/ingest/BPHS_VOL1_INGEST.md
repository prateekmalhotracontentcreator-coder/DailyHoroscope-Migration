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

## Open Issues (Phase 1 -- existing batches)
> Last inspected: 2026-06-01 via inspect_bphs_phase1_issues.py

1. ✅ **13 contradiction pairs Ch 12-23** -- CLOSED. Live DB = 0 contradiction_hold. Resolved in prior session; tracker was stale.
2. ✅ **Ch 15 PHR (rate was 25%)** -- CLOSED. Live DB = 0 PHR, 100% auto-approve.
3. ✅ **Ch 19 PHR (rate was 33%)** -- CLOSED. Live DB = 0 PHR, 100% auto-approve.
4. ✅ **Ch 34 flagged=15** -- CLOSED 2026-06-01. 12 truncation rules → PHR (`patch_ch34_flagged.py`). 3 content-flag rules → auto_approved via GAI review (`patch_ch34_content_flags_v2.py`). Live DB: Ch34 flagged = 0.
5. ✅ **yoga_check audit Ch35-41** -- FALSE ALARM. yoga_check IS populated at `condition.yoga_check` (rich structured object) and `metadata.yoga_checkable`. Inspect script was querying wrong field (`validation.yoga_check`). Script corrected. No migration needed.

## Phase 2 -- New Chapters (not yet ingested)
Chapters decoded by Phase 2 NLM thread, ready for ingest after A2 archives superseded bare files:
Ch03, Ch04, Ch05, Ch06, Ch07, Ch08, Ch09, Ch10, Ch11, Ch25, Ch26, Ch28, Ch29, Ch30, Ch31, Ch32, Ch33

**5 MED items now CLOSED (2026-06-01):** TT-CH06-02, TT-CH09-02, TT-CH30-02, TT-CH30-03, TT-CH31-02
Applied via `apply_med_items_resolve.py` → decode_notes + resolution_status added to 6 rule objects.
See: `BPHS_CC_Decode/BPHS_Vol1_GAI_Resolutions.md` and `apply_med_items_resolve.py`.

**Folder housekeeping (A2 action):** Archive superseded bare `_Rules.json` files for Ch16/17/18/20/24/32/33
to `BPHS_CC_Decode/_ARCHIVED/` before running Phase 2 ingest script.

**Phase 2 ingest script:** `ingest_bphs_vol1_phase2.py` (to be written by A2)
**Batch ID:** `bphs-vol1-phase2-v1-20260601`

## Status
Phase 1: INGESTED ✅ | Split-upgrade complete ✅ | All 5 NLM issues CLOSED ✅ (2026-06-01)
Phase 2: READY ✅ | MED items CLOSED ✅ | Awaiting A2 folder housekeeping → ingest
