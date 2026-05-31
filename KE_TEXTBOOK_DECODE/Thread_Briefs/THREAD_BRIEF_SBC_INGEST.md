# Thread Brief -- Sarvato Bhadra Chakra (SBC) KE Ingest
## Status · Open Items · Immediate Next Action

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-31
> For: SBC Ingest Thread
> Status: **🔴 BLOCKED -- TT decisions required + 4 CRITICAL OCR items + 17 source gaps open. Do not ingest until gates cleared.**

---

## One-Liner

Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_SBC_INGEST.md` for all Sarvato Bhadra Chakra KE Ingest.

---

## What This Thread Owns

"Sarvato Bhadra Chakra" -- 181 decoded rules for the SBC transit and electional astrology system. Priority 3 in the approved ingest sequence. **Currently blocked** -- requires TT resolution of 7 priority conflicts and NLM/GAI resolution of 4 CRITICAL OCR items before ingest can begin.

---

## Canonical Output Folder

```
/Users/apple/Documents/Knowledge Engine_eBooks/New Ingest_5 Books/1. Sarvato Bhadra Chakra_V2/
```

Note: Two SBC folders exist (`1. Sarvato Bhadra Chakra/` and `1. Sarvato Bhadra Chakra_V2/`). Use **V2** only -- it is the canonical corrected output. Do not read from the non-V2 folder.

Master decode summary: `SBC_Master_Decode_Summary.md` (in the V2 folder)
OCR report: `SBC_OCR_Issues_Report.docx`

---

## Rule Count

| Metric | Value |
|---|---|
| Total rules | 181 |
| TT conflict rules | 7 (blocking) |
| Source gap rules | 24 open questions (7 resolved, 17 remaining) |
| CRITICAL OCR items | 4 |

---

## Blockers -- All Must Be Cleared Before Ingest

### Blocker 0: 6 Architecture / Collection Decisions (NEW -- from A1 session review)

The SBC system requires 6 dedicated lookup dataset collections in MongoDB that do not yet exist. These must be designed and seeded BEFORE any SBC rule ingest, because the rules reference these collections.

| Collection name | Contents |
|---|---|
| `vedha_coordinates` | Vedha obstruction coordinate pairs for SBC grid |
| `latta_coordinates` | Latta (kick) coordinate pairs |
| `upgraha_coordinates` | Upagraha position coordinates for SBC |
| `planet_significations` | Planet-to-nakshatra signification lookup |
| `sbc_geopolitical_coordinates` | City/region coordinates for geopolitical SBC analysis |
| `sapt_salaka_coordinates` | Sapt Salaka (7-spoke) table coordinates (also a CRITICAL OCR item C-02) |

**Action: TT must decide the schema for each collection before this blocker can be cleared.** These are architecture decisions -- they cannot be resolved by NLM/GAI alone.

---

### Blocker 1: 7 TT Priority Conflicts

These are genuine doctrinal ambiguities where the decode produced two valid readings that require TT co-founder decision.

**Action: Temple Team must review and resolve all 7 from `SBC_Master_Decode_Summary.md` before ingest.**

The 7 conflicts are listed with full context in that file. Each conflict needs:
- A TT decision on which reading to adopt
- The non-adopted reading marked as rejected (or kept as alternative with lower priority)

### Blocker 2: 4 CRITICAL OCR Items

| ID | Description |
|---|---|
| C-01 | Chandra Kalanal index -- column headers unclear |
| C-02 | Sapt Salaka table -- 7-spoke table values partially illegible |
| C-03 | Star rank results -- ranking table partially corrupt |
| C-04 | Devanagari consonant groups -- Sanskrit character grouping unclear |

**Action: Send to NLM/GAI session with the SBC PDF. Request direct PDF resolution of C-01 through C-04. These cannot be guessed -- PDF source required.**

### Blocker 3: 17 Remaining Open Questions (Source Gaps)

7 of 24 original open questions (OQ-08-01 through OQ-18-01) have been resolved and documented. 17 remain open.

**Action: TT to review the 17 remaining OQs in `SBC_Master_Decode_Summary.md` -- resolve as either "close with source_gap:true" or "requires NLM/GAI re-read".**

---

## ⚠️ Phase 2 Schema Learnings -- Apply When Unblocked

**Learned from BPHS Vol 1 Phase 2 (2026-06-01). SBC uses custom lookup collections not seen in other books -- schema audit is critical.**

**Ingest script checklist (for when all blockers are cleared):**
- [ ] `source["batch_id"] = BATCH_ID` inside `inject_fields()` -- NOT just top-level `ingest_batch_id`
- [ ] Run schema audit on `Sarvato Bhadra Chakra_V2/` folder first -- custom lookup collections mean the JSON schema may differ from standard rule books
- [ ] `interpretation.detailed` and `interpretation.summary` non-empty -- SBC coordinate/lookup rules may not have standard interpretation fields; add `_map_interpretation()` if needed
- [ ] `condition` is a non-empty dict -- add `_map_condition()` if source uses `conditions` list
- [ ] Pre-upload local structural check: `Issues: 0`
- [ ] The 6 custom lookup collections (`vedha_coordinates`, `latta_coordinates`, etc.) must be seeded BEFORE any rule ingest

**Three-bucket triage for validation results:** A (artifact → `auto_approved`) · B (validator error → PHR) · C (genuine → flagged TT/GAI)

---

## Ingest Instructions (when unblocked)

**Step 1 -- Pre-ingest dedup:**
```bash
python3 backend/ke_dedup_script.py \
  --folder-a "/Users/apple/Documents/Knowledge Engine_eBooks/New Ingest_5 Books/1. Sarvato Bhadra Chakra_V2/" \
  --folder-b "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/" \
  --output-report dedup_sbc_vs_bphs_vol1.md \
  --threshold 0.82
```

**Step 2 -- Inject on every rule:**
```python
rule["approval_status"]    = "pending_human_review"
rule["ingested_at"]        = datetime.now(timezone.utc).isoformat()
rule["ingest_batch_id"]    = "sbc_v1"
rule["source_book"]        = "Sarvato Bhadra Chakra"
rule["source"]["batch_id"] = "sbc_v1"  # MANDATORY -- validate_rules.py queries this
```

**Step 3 -- Special handling:**
- Rules with unresolved source gaps: set `source_gap: true` + `pending_review: true`
- Rules where TT adopted one reading: mark rejected reading as `active: false`

---

## Open Items Summary

| Category | Count | Status |
|---|---|---|
| TT priority conflicts | 7 | 🔴 BLOCKING -- TT must decide |
| CRITICAL OCR items | 4 | 🔴 BLOCKING -- NLM/GAI PDF resolution needed |
| Remaining source gap OQs | 17 | 🔴 BLOCKING -- TT must close each as `source_gap:true` or escalate |
| Resolved OQs | 7 | ✅ Done -- documented in SBC_Master_Decode_Summary.md |

---

## Post-Ingest Dedup Targets (when ready)

| Target | Expected Overlap |
|---|---|
| BPHS Vol 1 | Low-moderate -- SBC is a transit/electional system, different from natal BPHS |
| 300 Horoscopes Vol 1 | Low |
| 300 Combinations | Low |

---

## Immediate Next Action (for TT)

1. Open `SBC_Master_Decode_Summary.md`
2. Review and decide on 7 priority conflict rules
3. Review and close 17 remaining OQs (source_gap or escalate to NLM/GAI)
4. Send SBC PDF + C-01 through C-04 to NLM/GAI for CRITICAL OCR resolution

**This thread cannot proceed until TT completes the above. Do not attempt ingest.**

---

*Brief prepared by Temple Team -- EverydayHoroscope, 2026-05-31*
*KE Freeze LIFTED ✅ 2026-05-22. All ingest targets `horoscope_db`. Do NOT use stale `EverydayHoroscope` DB.*
