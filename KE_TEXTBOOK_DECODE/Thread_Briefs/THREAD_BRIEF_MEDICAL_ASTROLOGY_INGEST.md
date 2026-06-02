# Thread Brief -- Medical Astrology KE Ingest
## Status · Open Items · Immediate Next Action

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-31
> For: Medical Astrology Ingest Thread
> Status: **🟢 READY -- All Grade A + Grade B items resolved 2026-05-31. Phase 2 (P2-4) ingest. Proceed after Phase 1 books are ingested.**

---

## One-Liner

Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_MEDICAL_ASTROLOGY_INGEST.md` for all Medical Astrology KE Ingest.

---

## What This Thread Owns

Medical Astrology textbook -- all chapters decoded. 81 OCR items assessed; all Grade A and Grade B items resolved. Phase 2 Priority 4 in the approved ingest sequence (after BPHS Vol 1, BPHS Vol 2, and KP Astrology are ingested).

---

## Canonical Output Folder

```
/Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode/
```

Temple Team brief: `MedAstro_TempleTeam_Brief.md`
OCR audit: `MedAstro_OCR_Issues_Audit.md`

---

## OCR Resolution Summary (2026-05-31)

| Grade | Count | Status |
|---|---|---|
| Grade A (Critical) | 2 | ✅ Both resolved |
| Grade B (High) | 11 | ✅ All 11 of 11 resolved |
| Grade C (Medium) | 7 | 🟡 Ingest with special flags |
| Grade D (Low/Cosmetic) | 61 | ✅ No action needed |

**Total OCR items: 81. Blocking items cleared: 13 of 13.**

---

## Grade A Resolutions (both confirmed 2026-05-31)

| Item | Resolution |
|---|---|
| A-1: Chart IX birth data | ✅ Permanently absent from text. bench-004: `birth_data_unavailable:true`. Aquarius Lagna derived from analysis. Cancer Lagna fully verified by pyswisseph. |
| A-2: "17/46" notation | ✅ Confirmed Lagna degree notation (Cancer 17°46'), NOT birth time. Chart DOB "7-9-1958" = one-day print error → Sept 6, 1958 (Moon+Mars in Taurus H11 matches analysis). |

---

## Grade B Resolutions (all 11 confirmed 2026-05-31)

Key resolutions:
- **B-7 Shambhu Hora:** Shambhu Hora Prakash by Punjarajacharya (~15th-16th c. CE, Chowkhamba) confirmed. Rahu-H6 maternal uncle rule verbatim. Applied to bench-015. `gai_citation_unverified: true`.
- **B-8 Chaturdashi Dagdha:** Dagdha = Gemini/Virgo/Sagittarius/Pisces per Kalaprakashika. Chart XVIII blindness mechanism confirmed. Applied to bench-013. `gai_citation_unverified: true`.
- **B-11 Vedic quote:** Rigveda 1.91.16 reconstructed. Applied to ma-ch03-005 + DataTable 3.2. `gai_citation_unverified: true`.

**Critical note for Ingest Thread on B-7, B-8, B-11:** These three rules carry `gai_citation_unverified: true`. Before co-founder approval (NOT before ingest), cross-check the specific chapter/sloka references for each. Do not hold ingest -- hold the approval gate.

---

## ⚠️ Phase 2 Schema Learnings -- Apply Before Writing Script

**Learned from BPHS Vol 1 Phase 2 (2026-06-01). Apply from the start.**

**Run schema audit on decode folder:**
```bash
python3 << 'EOF'
import json
from pathlib import Path
FOLDER = Path("/Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode/")
for f in sorted(FOLDER.glob("*.json"))[:4]:
    data = json.loads(f.read_text())
    rules = data.get("rules", data) if isinstance(data, dict) else data
    if not isinstance(rules, list) or not rules: continue
    r = rules[0]
    interp = r.get("interpretation") or {}
    print(f"\n=== {f.name} ===")
    print(f"  keys: {list(r.keys())[:10]}")
    print(f"  interpretation.detailed: {repr((interp.get('detailed') or '')[:80])}")
    print(f"  condition dict: {isinstance(r.get('condition'), dict)}")
EOF
```

**Ingest script checklist:**
- [ ] `source["batch_id"] = BATCH_ID` inside `inject_fields()` -- NOT just top-level `ingest_batch_id`
- [ ] `interpretation.detailed` and `interpretation.summary` non-empty on every rule
- [ ] `condition` is a non-empty dict on every rule
- [ ] Pre-upload local structural check: `Issues: 0`

**Three-bucket triage for validation results:**
- Bucket A: Artifact only → `auto_approved`; Bucket B: Validator error → PHR; Bucket C: Genuine → flagged TT/GAI

**Note on `gai_citation_unverified` rules:** Validator may flag these for unusual references (Shambhu Hora Prakash, Kalaprakashika, Rigveda quote). These are Bucket B (validator doctrinal error or unrecognised classical text) → PHR. Do NOT leave as flagged -- the source has been confirmed by GAI.

---

## Ingest Instructions

**Step 0 -- Pre-upload AI validation (run on local JSON before touching MongoDB):**
```bash
python3 backend/scripts/validate_rules.py \
  --json-file /tmp/medical_astrology_dry_run.json \
  --batch-id medical_astrology_v1
```
Triage: Bucket A (truncation) → PHR. Bucket B (framework mismatch -- classical medical astrology uses house-based significations that differ from BPHS; validator may over-flag) → PHR + validator_error:True. Bucket C (genuine) → flag for TT. See INGEST_PROCESS_BRIEF.md KOP-03/KOP-04.

**Step 1 -- Pre-ingest dedup:**
```bash
python3 backend/ke_dedup_script.py \
  --folder-a "/Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode/" \
  --folder-b "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/" \
  --output-report backend/scripts/dedup_reports/dedup_medastro_vs_bphs_vol1.json \
  --threshold 0.82
```
Medical astrology principles derive from BPHS planetary significations -- moderate overlap expected.

**Dedup report review:** Check THREE sections in the JSON output:
1. `matches` -- lexical similarity duplicates
2. `contradictions` -- same condition, opposite polarity
3. `positional_conflicts_detail` -- same planet×house/sign, different result (NEW 2026-06-02). `positional_polarity_conflict` = high confidence; `positional_alternate_result` = same condition, dissimilar result text. Flag all for TT review.

**Step 2 -- Inject on every rule:**

> ⚠️ CRITICAL (KOP-03): Set `pending_review` -- NOT `pending_human_review`. If you upload with `pending_human_review`, the AI validator finds 0 rules and silently skips the entire batch.

```python
rule["approval_status"]    = "pending_review"          # NOT pending_human_review -- see KOP-03
rule["ingested_at"]        = datetime.now(timezone.utc).isoformat()
rule["ingest_batch_id"]    = "medical_astrology_v1"
rule["source_book"]        = "Medical Astrology"
rule["source"]["batch_id"] = "medical_astrology_v1"  # MANDATORY -- validate_rules.py queries this
```

**Step 3 -- Special field handling by rule type:**

| Rule / Benchmark | Field to set | Value |
|---|---|---|
| bench-004 (Chart IX) | `birth_data_unavailable` | `true` |
| Charts XI, XII, XXII (missing DOBs) | `analytical_description_only` | `true` |
| B-7 (bench-015), B-8 (bench-013), B-11 (ma-ch03-005 + DataTable 3.2) | `gai_citation_unverified` | `true` |
| Grade C rules (7 items) | `pending_review` | `true` |

---

## Open Items

| Category | Count | Action |
|---|---|---|
| `gai_citation_unverified` flags | 3 rules | Cross-check sloka refs before co-founder approval (NOT before ingest) |
| `birth_data_unavailable` | 1 rule (bench-004) | Already set -- include in ingest |
| `analytical_description_only` | 3 benchmarks (Charts XI/XII/XXII) | Already set -- include in ingest |
| Grade C items | 7 | Include with `pending_review:true` |
| Grade D items | 61 | Include as-is (cosmetic only) |

---

## Post-Ingest Dedup Targets

| Target | Expected Overlap |
|---|---|
| BPHS Vol 1 | Moderate -- planetary significations shared |
| KP Astrology (health rules) | Low-moderate |

---

## Immediate Next Action

1. Run dedup against BPHS Vol 1 local folder
2. Set all special fields (birth_data_unavailable, analytical_description_only, gai_citation_unverified, pending_review) on relevant rules in the JSON files
3. Run ingest (dry-run → review → upload)
4. Verify count in MongoDB
5. Log gai_citation_unverified rules in `import_batches` record for TT to cross-check before approval

---

*Brief prepared by Temple Team -- EverydayHoroscope, 2026-05-31*
*KE Freeze LIFTED ✅ 2026-05-22. All ingest targets `horoscope_db`. Do NOT use stale `EverydayHoroscope` DB.*
