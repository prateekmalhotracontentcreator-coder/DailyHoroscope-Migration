# LAL_KITAB_INGEST.md
> Last updated: 2026-05-11

## Application Layer Status (updated 2026-05-11)
LK Standalone module is **fully live**. All routes deployed on Render, all frontend pages live on Vercel.
- `POST /api/lk/onboard` -- 3-step wizard; now accepts birth details + auto-computes Jyotish + LK chart
- `POST /api/lk/compute-chart` -- standalone chart compute, no auth (dual house: Jyotish lagna-relative + LK natural zodiac)
- `POST /api/lk/diagnose` -- 5-gate diagnostic report (Gates 1-5)
- `POST /api/lk/conflict-check` -- safety gate IDs 616-625
- `POST /api/lk/debt-audit` -- karmic debt IDs 601-615, family census substitution
- `GET /api/lk/remedies` -- paginated browse with filters
- 43-day tracker: binary cycle enforced (miss = streak reset), sunrise-sunset window validation
- All 6 frontend pages live: LKRemediesPage, LKOnboardPage, LKReportPage, LKTrackerPage, LKDebtAuditPage, LKBrowsePage

Bug fixed 2026-05-11: `vedic_calculator.py` `_solar_event_jd` -- `swe.rise_trans` argument order (float `lon` was passing into `rsmi` int position). Now matches `panchang_router.py` pattern.

Rename 2026-05-11: "LK Remedies" → "Lal Kitab Remedies" across NavBar, LKOnboardPage, LKBrowsePage.

## Coverage
Chapters: 19-28  (Ch 29 ingested but flagged -- see open issues)
Total Rules: ~445 | Auto-Approved: ~275 | PHR: ~149 | Flagged: ~10

## Scripts Run
| Script | Purpose | Status |
|---|---|---|
| ingest_lalkitab_ch19_v1.py | Ch 19 | ✅ Done (deduped -- see below) |
| dedup_lalkitab_ch19.py | Remove duplicates from Ch 19 | ✅ Done |
| delete_lalkitab_ch19.py / reset_lalkitab_ch19.py | Reset + re-ingest Ch 19 | ✅ Done |
| ingest_lalkitab_ch20_v1.py | Ch 20 | ✅ Done |
| fix_pending_ch20.py | Fix pending flags Ch 20 | ✅ Done |
| ingest_lalkitab_ch21_v1.py | Ch 21 | ✅ Done |
| patch_lalkitab_ch21_flags.py | Flag fixes Ch 21 | ✅ Done |
| ingest_lalkitab_ch22_v1.py | Ch 22 | ✅ Done |
| ingest_lalkitab_ch23_v1.py | Ch 23 | ✅ Done |
| ingest_lalkitab_ch24_v1.py | Ch 24 | ✅ Done |
| ingest_lalkitab_ch24_v2.py | Ch 24 revised | ✅ Done |
| patch_lalkitab_ch24_flags.py / patch_lalkitab_ch24_v2_flags.py | Flag fixes Ch 24 | ✅ Done |
| ingest_lalkitab_ch25_v1.py | Ch 25 | ✅ Done |
| patch_lalkitab_ch25_flags.py | Flag fixes Ch 25 | ✅ Done |
| ingest_lalkitab_ch26_v1.py | Ch 26 | ✅ Done |
| ingest_lalkitab_ch27_v1.py | Ch 27 | ✅ Done |
| ingest_lalkitab_ch28_v1.py | Ch 28 | ✅ Done |
| patch_lalkitab_ch28_flags.py | Flag fixes Ch 28 | ✅ Done |
| ingest_lalkitab_ch29_v1.py | Ch 29 | ✅ Done (pending flag review) |
| patch_lalkitab_ch29_flags.py | Flag fixes Ch 29 | ✅ Done |
| patch_mars_h03.py | Mars House 3 correction | ✅ Done |
| validate_rules.py | Validation sweep | ✅ Done |

## Open Issues
1. **PHR triage pending** -- 149 PHR rules awaiting NLM/co-founder review
2. **Ch 29+** -- confirm with co-founder if further chapters exist in source book
3. **science_id** -- `jyotish` (shares namespace with BPHS; Lal Kitab rules tagged by chapter prefix)

## Status
INGESTED ✅ (Ch 19-28, Ch 29 done with flags) | PHR triage: PENDING
