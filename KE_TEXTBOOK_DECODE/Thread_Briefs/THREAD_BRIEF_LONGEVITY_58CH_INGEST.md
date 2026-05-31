# Thread Brief -- Longevity 58 Chapters KE Ingest
## Status · Open Items · Immediate Next Action

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-31
> For: Longevity 58 Chapters Ingest Thread
> Status: **🔴 HARD BLOCKED -- Co-founder sign-off on aayu bucket methodology REQUIRED. Do not ingest a single rule until explicit approval is given.**

---

## One-Liner

Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_LONGEVITY_58CH_INGEST.md` for all Longevity (58 Chapters) KE Ingest.

---

## What This Thread Owns

"Longevity" full textbook -- 58 chapters, ~600+ decoded rules covering the complete Vedic longevity astrology system (Aayu calculation, Pindayu, Nisargayu, Amsayu, Maraka timing, Badhaka planets). This is the LAST book in the approved ingest sequence.

**Important distinction:** This is NOT the same as "Longevity & Unnatural Death" (44 rules -- already cleared). This is the complete longevity textbook with ~600+ rules across 58 chapters.

---

## Canonical Output Folder

```
/Users/apple/Documents/Knowledge Engine_eBooks/Longevity_CC_Decode/
```

Handover summary: `HANDOVER_SUMMARY_LongevityDecode.md` (in folder)

---

## Rule Count

| Metric | Value |
|---|---|
| Total rules | ~600+ (exact count pending final validation) |
| Chapters | 58 total |
| Ch4/Ch5 decode method | NLM thread |
| Ch6-Ch58 decode method | Claude Code |
| Aayu bucket rules | BLOCKED pending co-founder methodology approval |

---

## THE HARD BLOCK -- Aayu Bucket Methodology

The ~600 rules include a significant sub-set of **aayu bucket rules** -- longevity span calculation rules that classify a person's expected lifespan into Alpayu (short), Madhyayu (medium), or Purnayu (long) based on planetary configurations.

There are **two competing methodologies** for how the bucket boundaries are calculated (the exact year-span that defines "short" vs "medium" vs "long" life). Without co-founder sign-off on which methodology the KE will adopt, ingesting these rules would embed a contested calculation standard into the database.

**This is the ONLY gate. Once TT gives explicit co-founder approval with the chosen methodology, this thread is unblocked.**

---

## Blocker Resolution Process

1. **TT presents the two methodologies** to the co-founder with a brief summary of the difference and the implications
2. **Co-founder selects one methodology** and provides explicit written approval
3. **Approval text is recorded** in this brief (update the "Approval Record" section below) and in `HANDOVER_SUMMARY_LongevityDecode.md`
4. **This thread then unblocks** -- proceed to dedup and ingest

### Approval Record

```
Date:         [PENDING]
Methodology:  [PENDING -- co-founder to select]
Authority:    Prateek Malhotra (Co-Founder)
Statement:    [PENDING]
Recorded by:  [PENDING]
```

---

## Decode Status (for reference -- decode is complete)

| Phase | Status |
|---|---|
| Ch4-Ch5 (NLM) | ✅ Complete |
| Ch6-Ch58 (CC) | ✅ Complete -- all 58 chapters accounted for |
| Handover document | ✅ `HANDOVER_SUMMARY_LongevityDecode.md` present |
| Aayu bucket methodology | 🔴 Awaiting co-founder sign-off |
| Ch36-Ch58 case study extraction | 🔴 Separate Codex commission not yet issued |

The decode work is finished for rule extraction. It is ONLY the governance gate that blocks ingest.

**Note on Ch36-58 case study rules:** A separate Codex commission for extracting structured rules from the case study chapters (Ch36-Ch58) has NOT yet been issued. These chapters contain benchmark birth chart case studies requiring a different extraction approach from the rule chapters. When the aayu bucket gate is cleared, TT must also brief this Codex commission before the full ~600+ rule count can be finalised and ingested.

---

## ⚠️ Phase 2 Schema Learnings -- Apply When Unblocked

**Learned from BPHS Vol 1 Phase 2 (2026-06-01). When the aayu bucket gate is cleared and ingest begins, apply these before writing the script.**

**Ingest script checklist (for when gate clears):**
- [ ] `source["batch_id"] = BATCH_ID` inside `inject_fields()` -- NOT just top-level `ingest_batch_id`; validate_rules.py queries `source.batch_id`
- [ ] Run schema audit on `Longevity_CC_Decode/` folder first -- this book has 58 chapter files, high probability of schema variation
- [ ] `interpretation.detailed` and `interpretation.summary` non-empty on every rule -- add `_map_interpretation()` if needed
- [ ] `condition` is a non-empty dict -- add `_map_condition()` if source uses `conditions` list
- [ ] Pre-upload local structural check: `Issues: 0` before uploading ~600 rules

**Template helpers:** `_map_interpretation()` + `_map_condition()` from `backend/scripts/ingest_bphs_vol1_phase2.py`.

**Three-bucket triage for validation results:** A (artifact → `auto_approved`) · B (validator error → PHR) · C (genuine → flagged TT/GAI)

---

## Ingest Instructions (when unblocked -- do not read until gate cleared)

**Step 1 -- Record approval in HANDOVER_SUMMARY_LongevityDecode.md**

**Step 2 -- Run pre-ingest dedup (extensive -- this book will cross-match many others):**
```bash
# Against BPHS Vol 1 (longevity chapters Ch43/44)
python3 backend/ke_dedup_script.py \
  --folder-a ".../Longevity_CC_Decode/" \
  --folder-b ".../BPHS_CC_Decode/" \
  --output-report dedup_longevity_vs_bphs_vol1.md

# Against Longevity Unnatural Death
python3 backend/ke_dedup_script.py \
  --folder-a ".../Longevity_CC_Decode/" \
  --folder-b ".../LongevityUnnatural_CC_Decode/" \
  --output-report dedup_longevity_vs_longunnat.md

# Against KP Astrology (longevity rules)
python3 backend/ke_dedup_script.py \
  --folder-a ".../Longevity_CC_Decode/" \
  --folder-b ".../KP_CC_Decode/" \
  --output-report dedup_longevity_vs_kp.md
```

**Step 3 -- Inject on every rule:**
```python
rule["approval_status"]    = "pending_human_review"
rule["claim_axis"]         = "longevity"
rule["ingest_batch_id"]    = "longevity_58ch_v1"
rule["source_book"]        = "Longevity (58 Chapters)"
rule["source"]["batch_id"] = "longevity_58ch_v1"  # MANDATORY -- validate_rules.py queries this
```

---

## Post-Ingest Dedup Targets (high overlap expected)

| Target | Expected Overlap |
|---|---|
| BPHS Vol 1 Ch43/44 | HIGH -- BPHS is the primary source text |
| Longevity Unnatural Death | Moderate -- same domain, different emphasis |
| KP Astrology longevity rules | Moderate |
| Phaladeepika Adhyaya XIII/XIV | Moderate |

---

## Immediate Next Action (for TT)

1. **Present aayu bucket methodology choice to co-founder.** This is the sole remaining gate.
2. Record approval in this brief and in `HANDOVER_SUMMARY_LongevityDecode.md`.
3. Only then: begin dedup + ingest sequence.

**This thread has ZERO work to do until the approval is given. Do not run dedup, do not touch the JSON files.**

---

*Brief prepared by Temple Team -- EverydayHoroscope, 2026-05-31*
*KE Freeze LIFTED ✅ 2026-05-22. All ingest targets `horoscope_db`. Do NOT use stale `EverydayHoroscope` DB.*
