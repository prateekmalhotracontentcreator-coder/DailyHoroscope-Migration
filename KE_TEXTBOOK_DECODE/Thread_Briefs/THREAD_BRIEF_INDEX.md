# KE Ingest -- Thread Brief Index
## One-Liner Reference per Book

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-31
> Purpose: Paste the relevant one-liner into each book's dedicated thread to orient it to the correct brief.

---

## How to Use

Each line below is a one-liner you paste at the start of a dedicated book thread. The thread reads the linked brief, then proceeds with decode or ingest work for that book only.

---

## Phase 1 -- Foundation Books (BPHS First)

**BPHS Vol 1**
> Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_BPHS_VOL1_INGEST.md` for all BPHS Vol 1 KE Ingest. Status: 🟢 READY -- Phase 1 (~1,069 rules Ch12-44) already in MongoDB. Phase 2 (Ch03-Ch11, Ch25-26, Ch28-33) ready to ingest now.

**BPHS Vol 2**
> Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_BPHS_VOL2_INGEST.md` for all BPHS Vol 2 KE Ingest. Status: 🟢 READY -- Ch49-51, 249 rules, encode pass complete 2026-05-31.

---

## Phase 1 -- Additional Books

**300 Combinations** ✅ COMPLETE
> ~~Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_300COMBINATIONS_INGEST.md`~~ **Status: ✅ INGESTED + TRIAGE COMPLETE (2026-06-01) -- 329 rules, 141 auto_approved / 188 PHR / 0 flagged. Awaiting co-founder sign-off.** Post-ingest learnings in thread brief.

**300 Horoscopes Vol 1** ← START HERE (Priority 1, no blockers)
> Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_300HOROSCOPES_INGEST.md` for all 300 Horoscopes Vol 1 KE Ingest. Status: ✅ READY -- 57 rules, all 3 blocked rules cleared 2026-05-31. Also run dedup against 300 Combinations (already ingested).

**Longevity & Unnatural Death**
> Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_LONGEVITY_UNNATURAL_INGEST.md` for all Longevity Unnatural Death KE Ingest. Status: ✅ READY -- 44 rules, all 5 HIGH items resolved 2026-05-31.

**Destiny Numerology**
> Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_DESTINY_NUMEROLOGY_INGEST.md` for all Destiny Numerology KE Ingest. Status: 🟠 NEAR READY -- 189 rules, 10 HIGH OCR items need NLM/GAI pass before ingest.

**SBC (Sarvato Bhadra Chakra)**
> Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_SBC_INGEST.md` for all SBC KE Ingest. Status: 🔴 BLOCKED -- 181 rules, 7 TT conflict decisions + 4 CRITICAL OCR items + 17 source gaps required before ingest.

**Longevity 58 Chapters**
> Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_LONGEVITY_58CH_INGEST.md` for all Longevity (58 Chapters) KE Ingest. Status: 🔴 HARD BLOCKED -- ~600+ rules, aayu bucket methodology co-founder sign-off required. Do not ingest until approval given.

---

## Phase 2 -- After Phase 1 BPHS Complete

**KP Astrology**
> Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_KP_DECODE.md` for all KP Astrology KE Ingest. Status: 🟡 NEAR READY -- 256 rules, Cat B/C/G/H + F-01 to F-06 open items to resolve before ingest.

**Medical Astrology**
> Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_MEDICAL_ASTROLOGY_INGEST.md` for all Medical Astrology KE Ingest. Status: 🟢 READY -- all Grade A+B resolved 2026-05-31, gai_citation_unverified on 3 rules (cross-check before approval, not before ingest).

**Phaladeepika** ✅ COMPLETE
> ~~Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_PHALADEEPIKA_NLM.md`~~ **Status: ✅ INGESTED + TRIAGE COMPLETE (2026-06-01) -- 1,218 rules, 582 auto_approved / 271 PHR / 357 pending_review (PD-OP-01 truncation re-encode) / 8 flagged. Awaiting co-founder sign-off.** Ingest tracker: `.claude/ke/ingest/PHALADEEPIKA_INGEST.md`.

---

## Status Summary (as of 2026-06-01)

| Book | Status | Rules | Priority |
|---|---|---|---|
| BPHS Vol 1 | ✅ INGESTED + TRIAGE DONE | ~1,765 | P1 Foundation |
| BPHS Vol 2 (Ch49-51) | ✅ INGESTED + TRIAGE DONE | 249 | P1 Foundation |
| **300 Combinations** | ✅ **INGESTED + TRIAGE DONE** | **329** | **P1-3 -- COMPLETE** |
| **300 Horoscopes Vol 1** | **✅ READY -- START NOW** | **57** | **P1-4 (next)** |
| Longevity Unnatural Death | ✅ READY | 44 | P1-5 |
| Medical Astrology | 🟢 READY | 270 | P2-4 |
| **Phaladeepika** | **✅ INGESTED + TRIAGE DONE** | **1,218** | **P2-5 -- COMPLETE** |
| Destiny Numerology | 🟠 NEAR READY | 189 | P1-6 (OCR pass needed) |
| KP Astrology | 🟡 NEAR READY | 256 | P2-1 (Cat B/C/G/H pending) |
| SBC | 🔴 BLOCKED | 181 | P1-7 (TT + OCR decisions needed) |
| Longevity 58 Chapters | 🔴 HARD BLOCKED | ~600+ | P1-Last (aayu sign-off needed) |

---

## Absolute Rules for All Threads

1. **All rules enter as `approval_status: "pending_human_review"`.** No exceptions.
2. **`approved` status requires co-founder sign-off** -- not AI validation. These are two different things.
3. **All ingest targets `horoscope_db`.** Never use stale `EverydayHoroscope` DB.
4. **Always run `ke_dedup_script.py` before inserting a new book** -- against all already-ingested books' local JSON folders.
5. **Always write an `import_batches` record** after each successful ingest -- confirms idempotency.
6. **KE Freeze is LIFTED** (2026-05-22). Proceed with ingest.

---

---

## KE Milestone 2 -- Test Vectors + Case Study Decode (NEW 2026-06-05)

**THREAD 1 -- Longevity + Unnatural Deaths (93 Case Study Decode)**
> Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_TV_LONGEVITY_DECODE.md`. KE Milestone 2 Thread 1. Decode 93 case study chapters. Primary outputs: (1) 93 Test Vector JSONs, (2) `LU_CaseDerived_Rules.json`, (3) `LU_Gap_Report.md`. **STEP 1: Answer all Pre-Decode Questions (Section 1 of brief) before starting full decode.** Batch ID: `tv_lu_decode_v1`.

**THREAD 2 -- 765 Notable Horoscopes (Profession Library Decode)**
> Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_TV_765H_DECODE.md`. KE Milestone 2 Thread 2. Decode all 765 entries. Primary output: Profession Library (765 × profession + chart positions). **STEP 1: Answer all Pre-Decode Questions (Section 1 of brief) before starting full decode.** Batch ID: `tv_765h_decode_v1`.

**THREAD 3 -- 300 Important Horoscopes Vol 1 Part 1 (136 Case Study Decode)** ✅ STEP 2 COMPLETE
> Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_TV_300H1_DECODE.md`. KE Milestone 2 Thread 3. **✅ STEP 2 COMPLETE 2026-06-05 -- 136 JSONs delivered** (Ch001-Ch136, 0 decode errors). Coverage: Lagna 59% (81/136), date ~45%, time ~60%. All 136 JSONs + `300H1_CaseDerived_Rules.json` (4 gap candidates -- kp_star_lord ×150 obs, kp_signification_chain ×10) + `300H1_Gap_Report.md`. **Next: TT review → engine verification on 5 samples → Phase 4 chart computation.** Batch ID: `tv_300h1_decode_v1`.

**THREAD 4 -- 300 Important Horoscopes Vol 1 Part 2 (153 Case Study Decode)** ✅ STEP 2 COMPLETE
> Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_TV_300H2_DECODE.md`. KE Milestone 2 Thread 4. **✅ STEP 2 COMPLETE 2026-06-05 -- 151 JSONs delivered** (Ch004-Ch153 + Ch069a/b split). 8 parser fixes applied (HL/GL, compact body table, timezone OCR, death-type accuracy, Ch069 dedup). Coverage: Lagna 74%, date 42%, HL/GL 23-25%. All 151 JSONs + `300H2_CaseDerived_Rules.json` (30 candidates) + `300H2_Gap_Report.md` (41 flagged obs). **Next: TT review → Phase 4 chart computation.** Batch ID: `tv_300h2_decode_v1`.

*Thread 3 ✅ complete 2026-06-05. Thread 4 ✅ complete 2026-06-05. Threads 1 + 2 pending dispatch.*

---

*Index prepared by Temple Team -- EverydayHoroscope, 2026-05-31*
*Updated: 2026-06-01 -- 300 Combinations ✅ COMPLETE (329 rules, 141 AA / 188 PHR / 0 flagged). Phaladeepika ✅ COMPLETE (1,218 rules, 582 AA / 271 PHR / 357 pending_review PD-OP-01 / 8 flagged). 300 Horoscopes is Priority 1.*
*Updated: 2026-06-05 -- KE Milestone 2 Test Vectors added. Thread 1 (Longevity Unnatural) + Thread 2 (765H Profession Library) ready to dispatch.*
*Updated: 2026-06-05 -- Thread 4 (300H2) ✅ STEP 2 COMPLETE. 151 JSONs + rules + gap report delivered. 8 parser fixes applied. Awaiting TT review.*
