# BPHS_VOL2_INGEST.md
> Last updated: 2026-06-01

## Coverage -- Phase 1 (Ch47, Ch48, Ch52-Ch60)
Original ingest (pre-2026-05-08). Chapters: 47, 48, 52-60
Total Rules: ~2,227 | Auto-Approved: 1,092 | PHR: ~582 | Flagged: ~190
Status: ✅ INGESTED | PHR triage: PENDING (TT review queue)

## Coverage -- Phase 2 (Ch49-51, Navamsa Dasa)
Ingested 2026-06-01 per A2 Ingest Session.
- Batch ID: `bphs-vol2-ch49-51-v1`
- Chapters: Ch49 (Navamsa Dasa Sign Outcomes), Ch50 (Planet States), Ch51 (Navamsa Bhoga)
- Total rules: 249 (248 active + 1 source gap: `bphs2-ch49-gemini-pada-8-gap`)
- Validation: 118 auto_approved / 131 PHR / 0 flagged (post-triage)
- Contradiction pairs: 5 detected, all 5 confirmed false positives (complementary polarity rules)
- GAI resolution log: `BPHS_Vol2_CC_Decode/BPHS_Vol2_GAI_Resolutions.md`
- Thread brief: `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_BPHS_VOL2_INGEST.md`
- Status: ✅ INGESTED + TRIAGE COMPLETE | Awaiting co-founder sign-off (118 auto_approved)

## Scripts Run -- Phase 1
| Script | Purpose | Status |
|---|---|---|
| ingest_bphs_dasha_v1.py | Ch 47-48 (Vimshottari Dasha) | ✅ Done |
| fix_ch47_sl4548.py | Fix shloka 45-48 edge cases Ch 47 | ✅ Done |
| patch_ch53_venus_antardasha.py | Venus antardasha patch Ch 53 | ✅ Done |
| fix_ch56_sl7275.py | Fix shlokas 72-75 Ch 56 | ✅ Done |
| gap_fill_ch57_splits.py | Fill split gaps Ch 57 | ✅ Done |
| verify_ch57_gaps.py | Verify Ch 57 gap fill complete | ✅ Done |
| validate_rules.py | Validation sweep | ✅ Done |

## Scripts Run -- Phase 2 (Ch49-51)
| Script | Purpose | Status |
|---|---|---|
| ingest_bphs_vol2_ch49_51.py | Ch49-51 ingest via generic folder script | ✅ Done |
| validate_rules.py | Stage 1 structural + Stage 2 AI quality + Stage 3 contradictions | ✅ Done |
| ke_dedup_script.py | Dedup vs BPHS Vol 1 (local) + vs MongoDB export | ✅ Done -- 0 dup, 0 contra |

## Open Items
| ID | Priority | Detail | Status |
|---|---|---|---|
| Ch49-Gemini-P8 | Source Gap | `bphs2-ch49-gemini-pada-8-gap` -- M-38. TT to source Santhanam full text. | Open |
| Ch51 rule 020 | Provisional | `bphs2-ch51-020` provisional:true -- algorithm verified but co-founder review pending. | Open |
| **Co-founder approval** | **BLOCKER** | **118 auto_approved (Ch49-51) await sign-off. Admin: `/admin/library → auto_approved → BPHS Vol 2`.** | **Blocked on sign-off** |
| PHR triage (Phase 1) | LOW | 582 PHR rules (Ch47-60) awaiting NLM/co-founder review | Open |
| Flagged triage (Phase 1) | LOW | 190 flagged rules (Ch47-60) -- review for false positives | Open |

## Status
Phase 1 (Ch47-48, Ch52-60): ✅ INGESTED | Phase 2 (Ch49-51): ✅ INGESTED + TRIAGE COMPLETE | Co-founder sign-off pending
