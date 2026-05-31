# Thread Brief -- Phaladeepika KE Ingest
## Status · Key Facts · Pre-Ingest Checklist · Steps

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-06-01
> For: Phaladeepika Ingest Thread
> Status: **🟢 READY -- All 28 chapters decoded. All 6 HIGH OCR items resolved 2026-05-31. Phase 2 ingest: run after BPHS Vol 1 + Vol 2 are in MongoDB.**

---

## One-Liner

Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_PHALADEEPIKA_INGEST.md` for all Phaladeepika KE Ingest.

---

## Master Ingest Process

**Full 7-step workflow (read BEFORE writing script):**
```
/Users/apple/DailyHoroscope-Migration/.claude/ke/INGEST_PROCESS_BRIEF.md
```

**Decode brief (for decode-level queries only):**
```
KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_PHALADEEPIKA_NLM.md
```

The 7-step rule: **Dry Run → Save JSON → Review → Upload → Validate → Patch → Commit.** Never skip steps.

---

## Book Facts

| Field | Value |
|---|---|
| Decode folder | `/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode/` |
| Chapters | 28 decoded · Adhyaya XXVIII = 0 rules (colophon, skip) |
| Rules | 743+ total (exact count: run schema audit to confirm per-chapter counts) |
| Science ID | `jyotish` |
| Phase | **Phase 2** -- ingest AFTER BPHS Vol 1 + BPHS Vol 2 are in MongoDB |
| Batch ID | `phaladeepika-v1-20260601` (adjust date when running) |
| Ingest script | Create: `backend/scripts/ingest_phaladeepika_v1.py` |
| Reference script | `backend/scripts/ingest_bphs_vol1_phase2.py` (use as template -- has all schema helpers) |
| Post-ingest dedup | BPHS Vol 1 (highest expected overlap -- ~60-70% for house chapters) |

---

## ⚠️ Phase 2 Schema Learnings -- Apply Before Writing Script

**Learned from BPHS Vol 1 Phase 2 (2026-06-01). These failures cost a full re-upload cycle. Phaladeepika is 743+ rules across 27 chapter files -- schema problems at scale are expensive.**

**Run schema audit before writing the ingest script:**
```bash
python3 << 'EOF'
import json
from pathlib import Path

FOLDER = Path("/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode/")
for f in sorted(FOLDER.glob("*.json"))[:8]:
    data = json.loads(f.read_text())
    rules = data.get("rules", data) if isinstance(data, dict) else data
    if not isinstance(rules, list) or not rules:
        continue
    r = rules[0]
    interp = r.get("interpretation") or {}
    print(f"\n=== {f.name} ===")
    print(f"  Format: {'dict {rules:[...]}' if isinstance(data, dict) else 'list [...]'}")
    print(f"  keys: {list(r.keys())[:10]}")
    print(f"  interpretation.detailed: {repr((interp.get('detailed') or '')[:80])}")
    print(f"  condition dict: {isinstance(r.get('condition'), dict)} | conditions list: {bool(r.get('conditions'))}")
    print(f"  claim type: {type(r.get('claim')).__name__} | full_text: {bool(r.get('full_text'))}")
EOF
```

**Ingest script checklist (check off before running --upload):**
- [ ] `source["batch_id"] = BATCH_ID` inside `inject_fields()` -- NOT just top-level `ingest_batch_id`; validate_rules.py line 51 queries `source.batch_id`
- [ ] `interpretation.detailed` and `interpretation.summary` non-empty on every rule -- add `_map_interpretation()` if source uses `claim`, `full_text`, `result` instead
- [ ] `condition` is a non-empty dict -- add `_map_condition()` if source uses `conditions` list
- [ ] JSON loader handles both `{"rules":[...]}` dict-format and `[...]` list-format
- [ ] Pre-upload local structural check: `Issues: 0` before uploading 743 rules

**Copy `_map_interpretation()` + `_map_condition()` from `backend/scripts/ingest_bphs_vol1_phase2.py`** as the starting template.

**Three-bucket triage for validation results:**
- Bucket A: Data artifact (truncation only, detailed OK) → patch to `auto_approved`
- Bucket B: Validator doctrinal error (validator makes wrong Vedic claim -- cross-check PDF) → PHR + `validator_error:true`
- Bucket C: Genuine flag (fabrication, contradiction, source gap) → stay flagged, TT/GAI queue

---

## 6 HIGH OCR Items -- All Resolved (2026-05-31)

| ID | Chapter | Resolution |
|---|---|---|
| pd-ch22-c001 | Adhyaya XXII (Kalachakra) | ✅ Resolved |
| pd-ch25-c002 | Adhyaya XXV (Upagrahas) | ✅ Resolved |
| pd-ch26-c004 | Adhyaya XXVI (Transits / Vedha) | ✅ Resolved -- vedha_pairs corrected: 2nd transit Vedha = 5th (not 8th) |
| pd-ch12-c001 | Adhyaya XII (Children) | ✅ TEXT-NATIVE CONFIRMED: Benefic in own sign/exalt in 5th → child loss (Ch12 Sloka 3, p.117) |
| pd-ch27-c001 | Adhyaya XXVII (Ascetic Yogas) | ✅ Emancipation vs ascetic = NOT a contradiction -- complementary facets (Ch27 Slokas 1+8, pp.319-322) |
| pd-ch21-c003 | Adhyaya XXI (Sub-periods) | ✅ Jupiter/Mercury Bhukti -- cross-text majority POSITIVE (BPHS + Saravali + JP). `claim_polarity: positive`. `gai_citation_unverified:true` on pd-ch21-041. |

**~25 remaining MED items:** Ingest all with `pending_review:true`. Do NOT block ingest.
**69 LOW items:** Cosmetic only. No action needed.

---

## Special Fields -- Chapter-Specific

Phaladeepika uses several schema types not present in BPHS Phase 2. The ingest script must handle all of these:

| Chapter | Special schema requirement | Field / value |
|---|---|---|
| Adhyaya VII (Neechabhanga) | `condition.type: "neechabhanga_rule"` | Fields: `cancellation_trigger`, `reference_point` |
| Adhyaya IX (Lagna Signs) | `condition.type: "lagna_sign"` | + `scope: "natal_lagna"` -- do NOT use `planet: "lagna"` |
| Adhyaya XXIII/XXIV (Ashtakavarga) | `condition.type: "ashtakavarga_threshold"` | + `engine_dependency: ["ashtakavarga_calculator"]` |
| Adhyaya XXVI (Transits) | `vedha_nullifier` block at rule root | `vedha_house`, `exception_planets`, `nullification_type: "positive_result_cancelled"` |
| Adhyaya XXII (Kalachakra Dasa) | `dasha_system: "kalachakra"` | + `engine_dependency: ["kalachakra_dasa_calculator"]` on every rule |
| Adhyaya XXV (Upagrahas) | Extended planet enum | Valid: `mandi`, `dhuma`, `vyatipata`, `paridhi`, `indra_dhanus`, `upaketu` + `planet_category: "upagraha"` |
| Adhyaya XIII/XIV/XVII | `claim_axis: "longevity"` | Configurational rules → `scope: "natal"`. Algorithmic → `scope: "engine_specification"` + `engine_dependency: ["longevity_calculator"]` |
| Adhyaya XIV (Past/Future Births) | `claim_axis: "past_lives"` | Confirmed in `VALID_CLAIM_AXES` |
| Adhyaya VIII (Ch08 TBA) | `tba: true` + `active: false` | 6 Sun-in-house rules where PDF starts at Sloka 4 (Ch08 PDF gap) |

**Schema constants:** `backend/ke_schema_constants.py`
**Schema validation:** `backend/knowledge_schema.py`

---

## Ch08 TBA Rules -- Handle Carefully

6 Sun-in-houses-1-6 rules are PDF gaps. Ch08 PDF starts at Sloka 4 (houses 1-6 for Sun not in source text). Additionally, 1 Sloka 34 is truncated mid-sentence.

```python
# For the 6 TBA rules:
rule["tba"] = True
rule["active"] = False
rule["decode_notes"] = "PDF gap: Ch08 starts at Sloka 4. Sun houses 1-6 absent from source text. TT to source clean scan."
```

Total active rules from Ch08: 104 of 111.

---

## gai_citation_unverified Rules

Three rules carry `gai_citation_unverified: true`. These are **safe to ingest** but must be cross-checked before co-founder approval (NOT before ingest):

| Rule | Chapter | What to cross-check |
|---|---|---|
| pd-ch21-041 | Adhyaya XXI | Jupiter/Mercury Bhukti -- verify specific BPHS/Saravali/JP chapter/sloka refs cited by GAI |
| (see MedAstro brief for B-7/B-8/B-11 pattern) | -- | Same gai_citation_unverified pattern -- cross-check before approval gate |

Log these in the `import_batches` record so TT can track the pre-approval cross-check.

---

## Ingest Steps

**Step 1 -- Pre-ingest dedup (mandatory -- BPHS Vol 1 must be ingested first):**
```bash
# Phaladeepika vs BPHS Vol 1 (highest expected overlap)
python3 backend/ke_dedup_script.py \
  --folder-a "/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode/" \
  --folder-b "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/" \
  --threshold 0.82 \
  --output-report backend/scripts/dedup_reports/dedup_phaladeepika_vs_bphs_vol1.json

# Phaladeepika vs BPHS Vol 2
python3 backend/ke_dedup_script.py \
  --folder-a "/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode/" \
  --folder-b "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/" \
  --threshold 0.82 \
  --output-report backend/scripts/dedup_reports/dedup_phaladeepika_vs_bphs_vol2.json
```

Expected: 60-70% duplicate_candidate rate on Adhyaya VIII (Planets in 12 Bhavas) vs BPHS house chapters. This is expected cross-text agreement, not a problem. Review report and tag confirmed duplicates with `duplicate_candidate:true` before upload.

**Step 2 -- Run schema audit** (script above -- check all 27 chapter files).

**Step 3 -- Dry run:**
```bash
python3 backend/scripts/ingest_phaladeepika_v1.py \
  --dry-run \
  --save backend/scripts/phaladeepika_rules.json
```
Expected: 743+ rules. Check first and last rule. Confirm special schema types are present.

**Step 4 -- Pre-upload local structural validation:**
```bash
python3 << 'EOF'
import json
from pathlib import Path

YOGA_SCHEMA_TYPES = frozenset({"yoga_combination", "general_principle", "dosha", "neechabhanga_rule",
                                "lagna_sign", "ashtakavarga_threshold", "engine_specification"})
rules = json.loads(Path("backend/scripts/phaladeepika_rules.json").read_text())
issues = []
for r in rules:
    interp = r.get("interpretation") or {}
    detailed = (interp.get("detailed") or "").strip()
    summary  = (interp.get("summary") or "").strip()
    text = detailed or summary
    cond_type = (r.get("condition") or {}).get("type", "")
    if r.get("tba") or not r.get("active", True):
        continue  # skip TBA rules -- they intentionally have placeholder content
    if not text:
        issues.append((r.get("rule_id"), "empty_interpretation"))
    elif cond_type not in YOGA_SCHEMA_TYPES and text[-1] not in ".!?\"')":
        issues.append((r.get("rule_id"), f"truncated_text (ends '{text[-1]}')"))
    if not isinstance(r.get("condition"), dict) or not r.get("condition"):
        issues.append((r.get("rule_id"), "missing_condition"))
print(f"Total rules: {len(rules)} | Issues: {len(issues)}")
for rid, reason in issues[:20]:
    print(f"  {rid}: {reason}")
EOF
```
Expected: `Issues: 0` (excluding the 6 TBA rules).

**Step 5 -- Upload:**
```bash
python3 backend/scripts/ingest_phaladeepika_v1.py \
  --upload backend/scripts/phaladeepika_rules.json \
  --mongo-url "$MONGO_URL" \
  --db-name horoscope_db
```

**Step 6 -- Validate:**
```bash
python3 backend/scripts/validate_rules.py \
  --batch-id phaladeepika-v1-20260601 \
  --mongo-url "$MONGO_URL" \
  --db-name horoscope_db
```

**Step 7 -- Patch flagged rules** (three-bucket triage: A → auto_approved · B → PHR · C → flagged TT/GAI).

**Step 8 -- Commit:**
```bash
git add backend/scripts/ingest_phaladeepika_v1.py \
        backend/scripts/phaladeepika_rules.json
git commit -m "chore(ingest): Phaladeepika -- 28 chapters, 743+ rules (Phase 2)"
```

---

## Fields to Inject on Every Rule

```python
rule["approval_status"]    = "pending_review"
rule["ingested_at"]        = datetime.now(timezone.utc).isoformat()
rule["ingest_batch_id"]    = "phaladeepika-v1-20260601"
rule["source_book"]        = "Phaladeepika"
rule["science_id"]         = "jyotish"
rule["source"]["batch_id"] = "phaladeepika-v1-20260601"  # MANDATORY -- validate_rules.py queries this
```

Special per-rule fields (set in the source JSON or via inject_fields logic):
- `pending_review: True` on ~25 MED items
- `tba: True` + `active: False` on 6 Ch08 Sun-in-house TBA rules
- `gai_citation_unverified: True` on pd-ch21-041
- `duplicate_candidate: True` on confirmed dedup matches from Step 1

---

## Post-Ingest Dedup Targets

| Target | Expected overlap | Notes |
|---|---|---|
| BPHS Vol 1 | **HIGH (60-70%)** for house chapters | Phaladeepika is a commentary tradition on BPHS -- cross-text agreement is expected |
| BPHS Vol 2 | MED -- Dasa chapters | Adhyaya XIX/XX/XXI vs BPHS Dasa chapters |
| 300 Combinations | MED -- Yoga chapters | Adhyaya VI/VII (yogas) may echo |
| KP Astrology | LOW -- system differences | KP sub-lord vs traditional lordship |

> Cross-text matches with BPHS are expected to be the richest in the entire KE. Tag Phaladeepika rules that agree with BPHS as `relationship: "corroborates"` -- these will be the strongest-confidence rules in the engine.

---

## Ingest Sequence Gate

**Do not start ingest until:**
- [ ] BPHS Vol 1 confirmed in MongoDB (Phase 1 + Phase 2 both in)
- [ ] BPHS Vol 2 (Ch49-51) confirmed in MongoDB
- [ ] Dedup reports against both Vol 1 and Vol 2 reviewed and `duplicate_candidate:true` applied

---

*Brief prepared 2026-06-01 · KE Freeze LIFTED ✅ 2026-05-22 · All ingest targets `horoscope_db`. Do NOT use stale `EverydayHoroscope` DB.*
*Decode brief: `THREAD_BRIEF_PHALADEEPIKA_NLM.md` · Ingest process: `INGEST_PROCESS_BRIEF.md`*
