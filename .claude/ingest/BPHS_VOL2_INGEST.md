# BPHS_VOL2_INGEST.md
> Last updated: 2026-05-08

## Coverage
Chapters: 47, 48, 52-60
Total Rules: ~2,227 | Auto-Approved: 1,092 | PHR: ~582 | Flagged: ~190

## Scripts Run
| Script | Purpose | Status |
|---|---|---|
| ingest_bphs_dasha_v1.py | Ch 47-48 (Vimshottari Dasha) | ✅ Done |
| fix_ch47_sl4548.py | Fix shloka 45-48 edge cases Ch 47 | ✅ Done |
| patch_ch53_venus_antardasha.py | Venus antardasha patch Ch 53 | ✅ Done |
| fix_ch56_sl7275.py | Fix shlokas 72-75 Ch 56 | ✅ Done |
| gap_fill_ch57_splits.py | Fill split gaps Ch 57 | ✅ Done |
| verify_ch57_gaps.py | Verify Ch 57 gap fill complete | ✅ Done |
| validate_rules.py | Validation sweep | ✅ Done |

## Open Issues
1. **PHR triage pending** -- 582 PHR rules awaiting NLM/co-founder review
2. **190 flagged rules** -- review for false positives pending
3. **Ch 49-51 EXCLUDED** -- co-founder decision (do not ingest)

## Status
INGESTED ✅ | Split-upgrade complete ✅ | PHR triage: PENDING
