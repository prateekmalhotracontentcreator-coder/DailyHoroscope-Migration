# Knowledge Engine — Session Handover
> Last updated: 27 Apr 2026 — Session 9 (Lal Kitab Ch 19 ingested + validated)
> Lal Kitab Ch 19 (78 rules, 63% auto_approved) complete. Next: BPHS Ch 40 (PDF on disk). See Section 4 for exact next actions.
> Next session: read this FIRST before touching any script or DB

---

## ⚠️ How to Keep This Document Current

**This file does NOT auto-update when context exhausts.** Three rules to prevent staleness:

1. **INGEST_NOTES.md is the living operational log** — always accurate because it's committed after every batch. When this doc is stale, INGEST_NOTES.md is the ground truth for what has been done.

2. **Update this doc at milestones, not just session end.** After every chapter ingest + validation, after every architectural decision, after every new script — update Section 4 (Next Steps) and the relevant section. Do not wait until context is nearly full.

3. **Start every new session with:**
   > *"Read `.claude/HANDOVER.md` and `backend/scripts/INGEST_NOTES.md`, then tell me what's pending before we proceed."*
   This forces reconstruction of current state before any action is taken.

---

## 1. Who You Are / What This Project Is

You are the Claude Code agent for **EverydayHoroscope** (https://www.everydayhoroscope.in) — India's premium Vedic astrology platform. The Knowledge Engine is a rules library that will power AI-driven chart interpretations. The user is **Prateek** (founder). His philosophy: *"This is our only shot to success. This work vs. rest of our lives."* Build it right the first time.

**Stack:** FastAPI backend (Render) · React frontend (Vercel) · MongoDB (`horoscope_db`) · Claude API for rule extraction

---

## 2. The Most Important Decision Made This Session

### Splitting Guidance Overhaul — 21 Apr 2026

The extraction prompt (`EXTRACTION_SYSTEM` in `ingest_bphs_dasha_v1.py`) previously said:

```
DO NOT split: "kendra, trikona, or the 11th" → one rule
DO NOT split: "6th, 8th, or 12th" → one rule
DO NOT split: "own sign or exaltation" → one rule
```

**This was wrong.** These are the exact cases that MUST be split. Here is why:

| Case | Why split |
|---|---|
| 6th vs 8th vs 12th | Completely different intensity — 8th = crisis, 6th = manageable adversity, 12th = losses/isolation |
| Exaltation vs own sign vs friend's sign | Different strength levels → different `strength_band` values. Can't modulate effect intensity without this split |
| kendra vs trikona vs 11th vs 3rd vs 2nd | Each house is independently queryable. User with planet in 11th should not get rules for kendra/trikona bundled in |

**New rule (now in the prompt):**

- **ALWAYS SPLIT**: Specific house numbers (each house = one rule) · Dignity states (exaltation/own/friend's/enemy/debilitation = one rule each)
- **KEEP AS ONE**: Named abstract categories (kendra as a group, trikona as a group) · Compound conditions requiring ALL parts simultaneously

**strength_band mapping now in prompt:**

| Condition | strength_band |
|---|---|
| Exaltation | `"high"` |
| Own sign | `"high"` |
| Friend's sign | `"medium"` |
| Enemy sign | `"low"` |
| Debilitation | `"low"` |
| Kendra | `"high"` |
| Trikona | `"high"` |
| 11th / 3rd / 2nd | `"medium"` |
| 8th house | `"high"` (intensity of harm) |
| 6th / 12th | `"medium"` |

This was committed but **NOT YET TESTED with live API**. The test script is at `/tmp/test_splitting.py`. The user needs to run:

```bash
cd /Users/apple/DailyHoroscope-Migration/backend
export ANTHROPIC_API_KEY="sk-ant-..."
python3 /tmp/test_splitting.py
```

Expected output for sloka 45-47: ~9 rules (was 2). For sloka 1-2: ~6 rules (was 3). For sloka 3-4: 1-2 rules (compound — should NOT over-split).

---

## 3. Current Knowledge Engine State

### MongoDB: `horoscope_db` (MANDATORY — never use `EverydayHoroscope`)

### Rules in DB: ~6,000+ rules across `horoscope_db` (fully validated 25 Apr 2026)

**Validation state (post full-library clean pass, 25 Apr 2026):**
| Status | Count |
|---|---|
| `auto_approved` | 2,705 |
| `pending_human_review` | 1,850 |
| `flagged` | 1,329 |
| `rejected` | 32 |
| **132 contradiction pairs** | downgraded to pending_human_review |

Note: TBA Ch 15 (1,530 rules, 24 Apr) sits at `pending_review` — not yet validated.
TBA Ch 16 (129 rules, 25 Apr) is **fully validated** — see Section 9 for final breakdown.

**Split-upgrade rules (+1,150 total, 21–24 Apr 2026):** Ch 47–59 fully swept — see Step 3 table above.
**TBA Ch 15 rules (+1,530, 24 Apr 2026):** `batch_id = tba-ch15-v1-20260424` — Planets × Houses × Signs
**TBA Ch 16 rules (+129, 25 Apr 2026):** `batch_id = tba-ch16-v1-20260425` — Yoga rules (named + category groups)

### antardasha_planet coverage: **802 / 802 = 100%** across Ch 47–59 ✅
- 2 universal meta-rules: `R-BPHS47-008`, `R-BPHS47-009` → `applies_to_all_dasha_lords: true`

### Chapters ingested (RTF pipeline):

| Source | Batch ID | Original Rules | Split-Upgrade +Rules | Status |
|---|---|---|---|---|
| BPHS Vol 1 Ch 12-18 | bphs-ch12..18-v2-20260414 | 241 | — | ✅ validated |
| BPHS Vol 1 Ch 19-23 | bphs-ch19..23-v2-20260415 | 119 | — | ✅ validated |
| BPHS Vol 1 Ch 24 | bphs-ch24-v2-20260416 | 376 | — | ✅ validated |
| BPHS Vol 2 Ch 47 (Sun MD) | bphs-ch47-dasha-20260416 | 93 | +126 ✅ + 1 GRP fix ✅ | split-upgrade complete (24 Apr) — **220 rules total** — not validated |
| BPHS Vol 2 Ch 48 (Moon MD) | bphs-ch48-dasha-20260416 | 46 | +34 ✅ | split-upgrade done, not validated |
| BPHS Vol 2 Ch 52 (Sun MD) | bphs-ch52-dasha-20260416 | 93 | +139 ✅ | split-upgrade done, not validated |
| BPHS Vol 2 Ch 53 (Venus MD) | bphs-ch53-dasha-20260417 | 72 | +123 ✅ | split-upgrade done, not validated |
| BPHS Vol 2 Ch 54 (Mars MD) | bphs-ch54-dasha-20260417 | 86 | +121 ✅ | split-upgrade done, not validated |
| BPHS Vol 2 Ch 55 (Rahu MD) | bphs-ch55-dasha-20260417 | 96 | +153 ✅ | split-upgrade done, not validated |
| BPHS Vol 2 Ch 56 (Jupiter MD) | bphs-ch56-dasha-20260418 | 126 | +118 ✅ + 2 grouped fix ✅ | split-upgrade + Flag 1 fix complete — **246 rules total** |
| BPHS Vol 2 Ch 57 (Saturn MD) | bphs-ch57-dasha-20260419 | 132 | +126 ✅ + 7 gap-fill ✅ | split-upgrade done, not validated — **265 rules total** |
| BPHS Vol 2 Ch 58 (Mercury MD) | bphs-ch58-dasha-20260419 | 104 | +132 ✅ | split-upgrade complete (24 Apr) — **236 rules total** — not validated post-split |
| BPHS Vol 2 Ch 59 (Ketu MD) | bphs-ch59-dasha-20260421 | 91 | +195 ✅ | split-upgrade complete (24 Apr) — **286 rules total** — not validated post-split |
| BPHS Vol 2 Ch 60 (Venus MD) | bphs-ch60-dasha-20260424 | 182 | +12 ✅ | split-upgrade complete (24 Apr) — **194 rules total** — not validated |
| TBA Ch 15 (Planets in Houses/Signs) | tba-ch15-v1-20260424 | 1,530 | — | ✅ ingested (24 Apr) — not validated — ⚠️ Mars-H03 flag (see INGEST_NOTES) |
| TBA Ch 16 (Yogas) | tba-ch16-v1-20260425 | 129 | — | ✅ **fully validated** (26 Apr) — 86 auto_approved / 35 PHR / 8 flagged — ⚠️ tba16-003 yoga_check flag (see §9) |
| BPHS Ch 35 (Nabhasa Yogas) | bphs-ch35-v1-20260426 | 33 | — | ✅ **fully validated** (26 Apr) — 25 auto / 6 PHR / 2 flagged — 0 contradictions · Vajra + Yava promoted to `multi_house_requirements` (26 Apr) |
| BPHS Ch 36 (Many Other Yogas) | bphs-ch36-v1-20260426 | 32 | — | ✅ **fully validated** (26 Apr) — 13 auto / 17 PHR / 2 flagged — 0 contradictions · Matsya + Parvata promoted to `multi_house_requirements` (26 Apr) |
| BPHS Ch 37 (Lunar Yogas) | bphs-ch37-v1-20260426 | 14 | — | ✅ **fully validated** (26 Apr) — 9 auto / 3 PHR / 2 flagged — 0 contradictions |
| BPHS Ch 38 (Solar Yogas) | bphs-ch38-v1-20260426 | 4 | — | ✅ **fully validated** (26 Apr) — 1 auto / 2 PHR / 1 flagged — 0 contradictions |
| BPHS Ch 39 (Raja Yogas) | bphs-ch39-v1-20260426 | 50 | — | ✅ **fully validated** (26 Apr) — 41 auto / 6 PHR / 3 flagged — 0 contradictions · 82% auto-approved (best ratio any yoga chapter) |
| **Lal Kitab Ch 19 (Mangalik Evil)** | lalkitab-ch19-v1-20260426 | **78** | — | ✅ **fully validated** (27 Apr) — 49 auto / 23 PHR / 6 flagged — 0 contradictions · 63% auto_approved · first Lal Kitab chapter |

---

## 4. Immediate Next Steps — as of 26 Apr 2026 (Session 8 end)

> All dasha sweep steps (0–3) are COMPLETE. All yoga chapters Ch 35–39 are ingested and validated.
> The active track is now: **Yoga Chapter Ingestion (Ch 40 → Ch 41 → Ch 43/44 → 300 Combinations)**.

### 🔜 Priority 1 — Ingest BPHS Ch 40 (Yogas for Royal Association)

**File on disk:** `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Ch40_Yogas for Royal Association.pdf`

**Workflow:**
```bash
# Step 1: Extract text from PDF
# Step 2: Build hard-coded ingest script backend/scripts/ingest_bphs_ch40_v1.py
#         (template: use ingest_bphs_ch39_v1.py as the base — it has the correct schema)
# Step 3: Dry-run → save JSON → review → upload
python3 backend/scripts/ingest_bphs_ch40_v1.py --dry-run --save backend/scripts/bphs_ch40_rules.json
python3 backend/scripts/ingest_bphs_ch40_v1.py --upload backend/scripts/bphs_ch40_rules.json --mongo-url "$MONGO_URL" --db-name horoscope_db
# Step 4: Validate
python3 backend/scripts/validate_rules.py --batch-id bphs-ch40-v1-20260426 --db-name horoscope_db
```

**Schema template:** Copy `build_rule()` from `ingest_bphs_ch39_v1.py` exactly — it has the correct `source{}`, `metadata{}`, `confidence{}` block structure. Ch 39 is the canonical reference for yoga chapter scripts.

**Batch ID format:** `bphs-ch40-v1-YYYYMMDD`

---

### 🔜 Priority 2 — Ingest BPHS Ch 41 (Yogas for Wealth)

**File on disk:** `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Ch41_Yogas for wealth.pdf`
Same workflow as Ch 40.

---

### 🔜 Priority 3 — Validate TBA Ch 15 (1,530 rules — PENDING)

**Batch ID:** `tba-ch15-v1-20260424`
**Status:** ingested, NOT validated.

```bash
cd /Users/apple/DailyHoroscope-Migration/backend
python3 scripts/validate_rules.py --batch-id tba-ch15-v1-20260424 --db-name horoscope_db
```

⚠️ Known issue: Mars-H03 flag (see INGEST_NOTES.md). May see high `flagged` count due to appearance-text density.

---

### 🔜 Priority 4 — Validate Dasha Chapters (Ch 47–60, post-split)

All dasha split-upgrades are complete. None of the split-upgrade batches have been re-validated.
Run `validate_rules.py` for each — start with the smallest:

```bash
python3 scripts/validate_rules.py --batch-id bphs-ch48-dasha-20260416 --db-name horoscope_db
python3 scripts/validate_rules.py --batch-id bphs-ch52-dasha-20260416 --db-name horoscope_db
# ... etc for ch53/54/55/56/57/58/59/60
```

---

---

## 9a. Lal Kitab Ingestion Track (NEW — 27 Apr 2026)

### What is the Lal Kitab track?

Parallel to BPHS and TBA, we are ingesting **Lal Kitab** chapters. Lal Kitab rules differ fundamentally from BPHS — they use a **table-based cross-reference structure** (Ascendant × Planet House → Trial Numbers → Remedies) rather than narrative slokas. Extraction method: **Notebook LM decode** (structured JSON extraction) → reviewed → hard-coded ingest script (zero API calls).

### New schema fields introduced by Lal Kitab:

| Field | Path | Purpose |
|---|---|---|
| `condition.ascendant` | condition | Ascendant sign specificity (Aries / Taurus / etc.) |
| `condition.aspect_houses` | condition | Standard 4th/7th/8th from Mars house |
| `condition.dosha_type` | condition | `"mangalik"` — identifies dosha type |
| `condition.yoga_check.ascendant_filter` | condition.yoga_check | Ascendant-specific planet_in_house check |
| `interpretation.remedies[].category` | interpretation | Remedy category (ritual / gem / donation / behavioral / marital) |
| `interpretation.remedies[].trial_no` | interpretation | Trial number cross-ref to source table |

### Aspect house standard (locked — Option 2):
All aspect houses use standard 4th/7th/8th from Mars position:
- H1 → [4, 7, 8] · H4 → [7, 10, 11] · H7 → [1, 2, 10] · H8 → [2, 3, 11] · H12 → [3, 6, 7]

### Workflow for Lal Kitab chapters:
```
Step 1 — PDF → Notebook LM → structured decode (docx)
Step 2 — Claude reviews decode against source PDF for accuracy
Step 3 — Hard-coded ingest script (zero API) from decode
Step 4 — Dry-run --save JSON → review → --upload → validate
```

### Lal Kitab chapters ingested:

| Chapter | Topic | Batch ID | Rules | Condition types | Status |
|---|---|---|---|---|---|
| Ch 19 — Mangalik Evil and Trials | Mars dosha + remedies | lalkitab-ch19-v1-20260426 | **78** | 65 dosha · 9 planetary_combination · 4 general_principle | ✅ **Fully validated** (27 Apr 2026) |

**Validation summary — Ch 19 (27 Apr 2026):**
| Status | Count | % |
|---|---|---|
| `auto_approved` | 49 | 63% |
| `pending_human_review` | 23 | 29% |
| `flagged` | 6 | 8% |
| Contradictions | 0 | — |

63% auto_approved on first clean run for a brand-new book + schema type is a healthy result. The 29% PHR reflects Claude being appropriately cautious on novel remedy specifics from Lal Kitab. 6 flagged = inspect manually via Rules Browser.

### validator fix applied (27 Apr 2026):
`knowledge_validator.py` `VALIDATION_PROMPT` now includes explicit guidance for `dosha` condition type — Claude evaluates mangalik rules on interpretation text only, not on unfamiliar condition schema fields (commit `39cd966`).

---

## 9. TBA Chapter Ingestion Track (NEW — 26 Apr 2026)

### What is the TBA track?

Parallel to BPHS, we are ingesting **"A Text-Book of Astrology"** chapters into the same `interpretation_rules` collection. TBA rules use a separate ingest script (`ingest_tba_ch16_v1.py`) tuned for the Yoga chapter structure (Type A named yogas + Type B category bullet groups).

Key schema additions vs. BPHS rules:
- `condition.yoga_check` — machine-checkable formation condition (checkable: True/False)
- `interpretation.physical_markers` — appearance/disability/behavioral observations per rule

### TBA Chapters ingested:

| Chapter | Batch ID | Rules | Status |
|---|---|---|---|
| Ch 16 — Planetary Combinations / Yogas | tba-ch16-v1-20260425 | **129** | ✅ **Fully validated** (26 Apr 2026) |

Apply run + validation confirmed:
- 44 named yoga rules (Type A) — 42 yogas incl. 3 Vipreet Rajyoga variants + Kendradhipati Dosha
- 85 category bullet rules (Type B) — Arishta/Wealth/Marriage/Progeny/Disability/Eye/Co-Borns etc.
- 49/129 yoga_check checkable=True (programmatic runtime detection ready)
- Physical markers in 44 rules (disability: 18, behavioral: 17, facial_features: 6, body_build: 5, voice: 5)
- Minor variance vs dry run: 1 rule shifted neutral→benefic (expected AI float — eliminated going forward by --save/--upload workflow)

**Validation summary (two-pass, 26 Apr 2026):**
| Status | Run 1 (34) | Re-run (95) | **Total** |
|---|---|---|---|
| `auto_approved` | 26 | 60 | **86 (67%)** |
| `pending_human_review` | 5 | 30 | **35 (27%)** |
| `flagged` | 3 | 5 | **8 (6%)** |
| Contradictions | 0 | 0 | **0** |

**Why two-pass?** First validation run hit 95/129 structural failures because `knowledge_validator.py`'s `truncated_text` check expected terminal punctuation on every rule. TBA Ch 16 `detailed` field ends with AI-extracted effect text (no period). Fix: `structural_check()` now skips `truncated_text` for `yoga_combination`, `general_principle`, `dosha` types (commit `ccb475c`). Re-validation cleared all 95 rules.

**This fix applies to all future yoga-schema chapters** (TBA Ch 35, etc.) — no action needed on those.

**⚠️ Manual Review Flag — tba16-003 (Ubhaychari Yoga)**

| Field | Value |
|---|---|
| rule_id | tba16-003 |
| yoga_name | Ubhaychari Yoga |
| yoga_check.type | complex |
| yoga_check.checkable | False |
| Issue | Condition is "Planets other than Moon on BOTH sides of Sun simultaneously" (2nd AND 12th from Sun). Each side is individually checkable as `any_planet_relative`, but the compound AND requirement was flagged as `complex`. |
| Fix path | Promote to `planet_in_house_from_sun` with `houses: [2, 12]` and `operator: "both"` — equivalent to BPHS Ch 38 Ubhayachari (bphs-ch38-003). Or use `multi_house_requirements` with two `planet_in_house_from_sun` clauses. Cross-ref: bphs-ch38-003. |
| Priority | Low — rule is still usable for report generation; only runtime detection (yoga_check) is affected. |

### yoga_check audit — BPHS Ch 35–38 complete (26 Apr 2026)

Full audit of all `complex/False` rules across Ch 35–38. Each rule inspected and classified. Summary:

| Chapter | complex/False | Promoted | Confirmed non-promotable | Reason category |
|---|---|---|---|---|
| Ch 35 | 4 | 2 (Vajra, Yava → `multi_house_requirements`) | 2 | Source incomplete (Ardha Chandra) · General principle (Meta-rule) |
| Ch 36 | 17 | 2 (Matsya type-fix, Parvata → `multi_house_requirements`) | 15 | House lord lookup (12) · Dignity/strength (2) · Multi-chart dispositor chain (1) |
| Ch 37 | 3 | 0 | 3 | D-9 Navamsa chart + birth-time required |
| Ch 38 | 1 | 0 | 1 | General principle / result modifier |
| **Total** | **25** | **4** | **21** | |

**Blocker key:**
- **L** = House lord identification required
- **D** = Dignity/strength calculation required (own sign, exalt, moolatrikona, "strong")
- **N** = D-9 Navamsa chart required
- **C** = Dispositor chain across multiple charts

**Phase 2 promotion roadmap for the 21 confirmed non-promotable:**

| When available | Rules unlocked | New type needed |
|---|---|---|
| Lord identification in engine | Kahala, Chamara, Sankha, Bheri, Mridanga, Srinatha, Sarada, Khadga, Lakshmi, Kusuma, Hari, Hara, Brahma (13) | `planet_in_house_from_lord` |
| Dignity check in engine | Koorma (1) | Extend `multi_house_requirements` with `min_dignity` field |
| D-9 Navamsa exposure | Moon Navamsa ×3 (Ch 37) | `moon_navamsa_check` |
| Multi-chart chains | Kalpadruma (1) | `dispositor_chain` (lowest priority) |
| Never | Ardha Chandra (source gap), Meta-rule, Solar modifier | — |

Full per-rule details in INGEST_NOTES.md — Ch 35/36/37/38 `complex/False` audit tables.

### Source files status (26 Apr 2026):
- BPHS Ch 39 ✅ ingested and validated
- BPHS Ch 40 — **PDF on disk**, ready to ingest: `BPHS_Ch40_Yogas for Royal Association.pdf`
- BPHS Ch 41 — **PDF on disk**, ready to ingest: `BPHS_Ch41_Yogas for wealth.pdf`
- BPHS Ch 43–44 — not yet confirmed on disk; ask Prateek
- 300 Important Combinations — **PDF on disk**: `300_Important_Combinations_BV_Raman.pdf`

### ⚠️ Phase 2 Schema Enrichment — physical_markers + yoga_check backfill (DEFERRED)

TBA Ch 15 (1,530 rules) and BPHS Ch 12-59 lack `physical_markers` and `yoga_check` fields.
Script `enrich_rules.py` — not yet built. Priority: TBA Ch 15 first (richest appearance data).
Defer until at least two more TBA chapters are live and the pattern is stable.

MongoDB query to find candidates when ready:
```python
db.interpretation_rules.count_documents({
    "interpretation.physical_markers": {"$exists": False},
    "approval_status": {"$ne": "deprecated"}
})
```

---

## 10. Two Workflow Decisions Locked — 26 Apr 2026

### Decision 1: --dry-run --save / --upload pattern (all future ingest scripts)

**Problem:** The old workflow ran AI extraction twice (dry run + apply = double cost). Any classification variance between runs (e.g., neutral→benefic) would silently diverge from the reviewed output.

**Decision:** Standard ingest workflow for ALL future chapters:
```
Step 1: python3 scripts/ingest_xxx.py --dry-run --save rules.json
         → AI runs ONCE. Output saved to JSON.
Step 2: Review rules.json. Make any amendments / additions directly in the file.
Step 3: python3 scripts/ingest_xxx.py --upload rules.json --mongo-url $MONGO_URL --db-name horoscope_db
         → ZERO AI calls. JSON uploaded directly to MongoDB.
Step 4: python3 scripts/validate_rules.py --batch-id <batch-id>
```

The --upload path guarantees the MongoDB content is byte-for-byte identical to the reviewed JSON. No variance possible.

**Patch script** handles any section-specific fixes after upload — no need to re-run full extraction.

### Decision 2: JSON review layer (audit + amendability)

All JSON files downloaded from dry runs are kept as a human-readable audit trail.
Rules can be:
- Amended (edit a field in the JSON before upload)
- Added (insert a new rule dict into the JSON before upload)
- Flagged for removal (delete from JSON before upload)

This means the Knowledge Engine ruleset has a human-review checkpoint at every chapter boundary, before anything reaches MongoDB.

---

## 5. Key Architecture Decisions (locked — do not revisit without strong reason)

### Premium Report Architecture — Confirmed 26 April 2026

**Decision: Structure-first, AI for Articulation only.**

The personalization in a premium report does NOT come from AI generating content from scratch. It comes from the structured intake data — the native's date/time/place of birth, answers to the 12 life-domain questions (family, career, relationships, health, etc.), active dasha period, active yogas detected by the engine. This contextual richness IS the personalization layer.

**The three-layer report model:**

| Layer | Source | Technology | API calls |
|---|---|---|---|
| **Detection** | vedic_calculator.py evaluates chart against yoga_check conditions | Pure Python | 0 |
| **Content** | Knowledge Engine fetches full_result + physical_markers for active yogas/rules | MongoDB query | 0 |
| **Articulation** | Claude converts structured KE output into flowing Vedic-style prose | ONE Claude API call per report | 1 |

**What AI does and does NOT do:**
- ✅ AI converts structured data into professional, humanized Vedic prose (articulation)
- ✅ AI trained via system prompt on sample Vedic astrology reports to establish house style and language register
- ✅ Temperature=0 ensures consistency across reports for the same chart
- ❌ AI does NOT generate or invent astrological judgments
- ❌ AI does NOT decide favorable/unfavorable outcomes — the KE rule provides that
- ❌ AI does NOT personalize from the chart — the structured intake data does that

**Why this is the professional standard:**
A human Jyotishi also follows a confirmed, structured methodology. They do not free-form a chart. They follow a known sequence of evaluations (lagna, dashas, yogas, house lords) and then articulate findings in their professional voice. The KE is that methodology encoded. Claude is that professional voice — trained on our Vedic textbooks.

**Free tier vs. Premium:**
- Free report → Template output only (zero AI cost)
- Premium report → Template + Articulation layer (one Haiku API call, ~₹0.20–0.30)

**Future training path:**
- System prompt includes: core Vedic language from ingested textbooks + sample premium reports
- As more chapters are ingested, the system prompt's Vedic vocabulary depth increases automatically
- A fine-tuned model (Phase 3) can eventually replace the API call entirely for this specific task

### Universal Rule Pattern
Rules at chapter openings before any antardasha sub-section begins:
- **MD-opening general rules** → `antardasha_planet = dasha_lord` (self-period)
- **True universal rules** (all 9 planets in `planets_involved`) → `antardasha_planet = null` + `applies_to_all_dasha_lords = true`
- See INGEST_NOTES.md for full detection signals

### Legacy Model is single source of truth for live data
`vedic_calculator.py` computes all dasha timelines. `knowledge_engine.py` is interpretation layer only. Never add dasha calculation to `knowledge_engine.py`.

### Two-key filtering
Knowledge engine matches rules on BOTH `dasha_lord` AND `antardasha_planet`. Legacy fallback uses `antardasha_lord` field for old rules.

### DB name
Always `horoscope_db`. Never `EverydayHoroscope` (that was a local mistake — 3200 rules were migrated from it on 20 Apr 2026).

---

## 6. Scripts Reference

| Script | Purpose | Key flags |
|---|---|---|
| `ingest_bphs_dasha_v1.py` | Ingest BPHS dasha chapters from RTF | `--chapter --dasha-lord --dry-run` |
| `ingest_bphs_houses_v2.py` | Ingest BPHS house chapters from RTF | `--chapter --house --dry-run` |
| `ingest_tba_ch16_v1.py` | Ingest TBA Ch 16 Yogas from RTF | `--rtf --dry-run --save FILE --upload FILE` |
| `patch_slokas.py` | Gap-fill under-extracted slokas | `--slokas --dasha-lord --batch-id --dry-run` |
| `validate_rules.py` | Run validator on a batch | `--batch-id` |
| `backfill_antardasha_planet.py` | Backfill `condition.antardasha_planet` | `--dry-run` (Pass 5 complete) |
| `extract_book.py` + `batch_ingest.py` | OCR/PDF pipeline (separate, keep archived) | not for RTF use |

**Standard ingest workflow (all future chapters):**
```
--dry-run --save rules.json  →  review JSON  →  --upload rules.json
```

All scripts: `cd /Users/apple/DailyHoroscope-Migration/backend`

---

## 7. Parser Fixes (cumulative — applied to `ingest_bphs_dasha_v1.py`)

| Fix | What | Trigger |
|---|---|---|
| `temperature=0` | Deterministic extraction | Ch 57 non-determinism |
| `condition.antardasha_planet` field | Queryable sub-period planet | KE filtering |
| `SPLITTING GUIDANCE` added | Explicit split/no-split examples | Ch 58 under-extraction |
| `SPLITTING GUIDANCE` OVERHAULED | House-by-house + dignity-by-dignity splits + strength_band mapping | Ch 59 sloka 20-21 analysis — **21 Apr 2026** |
| Period-as-range-separator `5.6.` → `5-6` | `split_into_sloka_blocks()` regex | Ch 59 sloka 5-6 missing |
| Ch 59 added to `INTRO_SLOKAS_BY_CHAPTER` with empty set | No skip-list inheritance | Ch 59 sloka 1-2 |
| `infer_strength_band_from_condition()` + `strength_band` field | `extracted_to_rule()` + `_fallback_rule()` — commit `19cec9e` | `strength_band` was completely absent from dasha pipeline — **21 Apr 2026** |
| **ANTI-COLLISION RULE** added to `EXTRACTION_SYSTEM` | Prevents partial splits: if splitting, must generate ALL individuals AND must NOT also keep a merged rule. Either split completely OR keep merged — never both. | Ch 52 sloka 69-73: Venus 6th missing individually while Venus 6th/8th/12th merged remained — **21 Apr 2026** |
| **LORDSHIP QUALIFIER COMPOUND RULES** added (KEEP AS ONE — point 4) | When source text combines placement list WITH lordship qualifier ("associated with lord of X"), extract individual placement rules per ALWAYS SPLIT PLUS one standalone compound rule capturing placement+lordship | Ch 54 sloka 64-66: compound condition silently absorbed — **21 Apr 2026** |
| `--sloka-filter` flag in dry-run | Shows all rules for a specific sloka label with full field details (dignity_state, strength_band, summary) — enables targeted verification before live ingest | Verification of anti-collision fix in Ch 52 sloka 69-73 — **21 Apr 2026** |
| `strength_band` moderate override in `infer_strength_band_from_condition()` | Checks for "moderate effect/result/at" keywords BEFORE house-based intensity inference — prevents `high` being assigned to rules with explicitly moderated outcomes | Ch 52 fix — **21 Apr 2026** |
| `dignity_state` default changed to `"general"` | Both `extracted_to_rule()` (line 668) and `extracted_to_rule_house_lord()` (line 780): `item.dignity_state or "general"` (was `or ""`) | Remedy rules and uncategorised rules had empty `dignity_state` — **21 Apr 2026** |
| `max_tokens` raised from 2048 → 4096 (commit f1fd623) | Prevents JSON truncation on large slokas with many rules | Ch 52 large sloka extraction — **21 Apr 2026** |

---

## 8. Open Points Across All Chapters

### Ch 12-24 (House chapters)
- 38 flagged rules — not yet reviewed in Rules Browser
- 13 contradiction pairs — not yet resolved
- 197 pending_human_review — awaiting co-founder sign-off
- **Under-split review pending** — same house/dignity bundling issue exists here; assess after dasha split-upgrade sweep is complete

### Ch 56 — Jupiter MD (22 Apr 2026) — ⚠️ FLAG POINTS FOR REVIEW

#### ⚠️ Sloka 72-75 — sub_type anomaly (same pattern as Ch 55 sloka 21-24)

Dry run shows `R-BPHS56-PATCH-D1BCEE` will be tagged `dasha_grouped_outcome` + `is_group_summary=True` but it is an **individual Rahu-exaltation condition rule**, not a grouped summary.

**✅ COMPLETE (22 Apr 2026)**

Two slokas fixed — same anomaly pattern (single-condition rule mis-tagged as grouped summary):

| Sloka | Mis-tagged rule | Fix | Grouped rule inserted | condition_group_id |
|---|---|---|---|---|
| 72-75 | `R-BPHS56-PATCH-6CC98D` (Rahu exaltation) | → `dasha_favourable`, `grp=False` | `R-BPHS56-PATCH-66C586-GRP` | `ch56-sl7275-rahu-favourable` |
| 51-53 | `R-BPHS56-PATCH-CAEF2D` (Sun exaltation) | → `dasha_favourable`, `grp=False` | `R-BPHS56-PATCH-34CC52-GRP` | `ch56-sl5153-sun-favourable` |

16 individual rules back-filled with `condition_group_id` (8 per sloka). Script: `fix_ch56_sl7275.py`.

#### Phase 3 candidates — slokas missing grouped outcome rules (6 slokas)

| Sloka | Condition count | Type | Notes |
|---|---|---|---|
| 33-34 | 4 | unfavourable | 4 Jupiter AD malefic placement conditions |
| 44 | 7 | unfavourable | 7 Saturn conditions with combined outcomes |
| 51-53 | 7 | favourable | 7 distinct favourable conditions |
| 54-55 | 6 | unfavourable | 6 unfavourable combinations |
| 61-63 | 8 | unfavourable | 8 unfavourable conditions — largest group |
| 65-66 | 4 | favourable | 4 favourable planet-in-sign conditions |

These 6 slokas will have individual split rules inserted by split-upgrade, but their grouped summary (`dasha_grouped_outcome`, `is_group_summary=True`) will be absent. Add to Phase 3 re-run list alongside pre-Ch-55 chapters.

#### Ch 56 totals
- Original: 126 rules (bphs-ch56-dasha-20260418)
- Split-upgrade live: +118 net-new rules (dry run predicted +159; −41 = temperature=0 variance)
- Sloka 72-75 grouped fix: +1 (pending — run fix_ch56_sl7275.py)
- **Total after fix: 245 rules**

---

### Ch 47-59 (Dasha chapters)
- **Split-upgrade sweep IN PROGRESS** — Ch 48/52/53/54/55 done (+570 rules). Ch 56 (dry run done)/57/58/59/47 still pending live ingest.
- **Validation pending** — Ch 52/53/54/55/56 not yet validated. Run `validate_rules.py` after split-upgrade for each.
- Ch 57 split-upgrade ✅ complete (+126); slokas 20-21, 30-31 over-split check still pending (original ingest flags, not new)
- Ch 59 sloka 45-47 — OCR-corrupted sloka, verify extracted rules cover all placement conditions
- Ch 59 batch ID in DB is `bphs-ch59-dasha-20260421` (not 20260420 as in some notes)

### ⚠️ Pre-Split_Merged Deprecation — MANDATORY Step 0 Before Co-Founder Review

All `pre_split_merged` original rules across ALL chapters must be deprecated **before Prateek opens Rules Browser for any review**. Without this, he will see:
- 4-5 near-identical merged-condition rows per sloka sitting alongside the correct split rules
- Mixed sub_type errors (e.g. R-BPHS55-020/021 tagged `dasha_unfavourable` on a favourable condition — original ingest error)

**Script (run ONCE after full split-upgrade sweep is complete):**
```python
col.update_many(
    {"metadata.source_note": "pre_split_merged"},
    {"$set": {"approval_status": "deprecated"}}
)
```
Verify with: `col.count_documents({"metadata.source_note": "pre_split_merged", "approval_status": {"$ne": "deprecated"}})` → should return 0.

**Do NOT run mid-sweep** — chapters with pending split-upgrades (56/57/58/59/47) still need their pre_split_merged originals as the only existing coverage until split-upgrade runs.

### Phase 2 — Lordship Qualifier Compound Rules
Chapters ingested before 21 Apr 2026 (Ch 47/48/52/53/54/56/57/58/59) may be missing compound placement+lordship rules. Prompt fix is now in `ingest_bphs_dasha_v1.py`. Audit deferred to after co-founder approval. See INGEST_NOTES.md Phase 2 section for query pattern.

### Ch 48 Schema Gap
34 split-upgrade rules inserted pre-schema-upgrade may lack `dignity_state` or `planet_context_note`. One-shot DB update script needed.

### Co-founder Review Workflow
Not yet commissioned. Prateek must approve before any rule gets `approval_status = 'approved'` (the only status the live backend queries). Zero approved rules currently — Knowledge Engine is interpretation-layer-ready but not live.

### CPath-1 Items
- Item 18: `longevity_router.py` import fail — not addressed
- Item 19: science_registry editor — not addressed
- Commission I-K: Kota Chakra — not addressed

---

### ⚠️ Phase 2 Schema Enrichment — physical_markers + yoga_check backfill

**Decision date:** 26 April 2026

#### What happened
TBA Ch 16 (Yogas) introduced two new fields to the rule schema:

| Field | Path in document | Purpose |
|---|---|---|
| `physical_markers[]` | `interpretation.physical_markers` | Physical appearance, voice, disability, behavioural markers extracted verbatim from source text |
| `yoga_check{}` | `condition.yoga_check` | Machine-checkable yoga formation condition for runtime detection by `vedic_calculator.py` |

These fields are **NOT present** in any previously ingested batches:
- TBA Ch 15 (1,530 rules — tba-ch15-v1-*)
- BPHS Ch 12–24 (house chapters — bphs-ch12..24-v2-*)
- BPHS Ch 47–59 (dasha chapters — bphs-ch47..59-dasha-*)
- Any OCR-sourced batches

#### Why this matters
1. **Premium Report — Yoga Detection**: Runtime yoga detection (vedic_calculator → yoga_check → active yogas → report) requires `yoga_check.checkable = True` on relevant rules. Without backfill, only Ch 16+ rules can be used for yoga detection.
2. **Physical Appearance Verification Report**: Querying `db.find({"interpretation.physical_markers.category": "body_build"})` will return zero results from all pre-Ch-16 batches. The appearance data exists in the `full_text_passages` text but is not structured.
3. **Ch 15 Planet-in-House rules**: These have rich physical appearance content (height, facial features, skin tone) for all 9 planets × 12 houses — the most important source for appearance-based birth chart verification.

#### Phase 2 script to build: `enrich_rules.py`

**Approach:**
- Reads existing rules from MongoDB by `source.batch_id` or `source.book_id`
- For each rule, sends `interpretation.full_text_passages[0].text` to Claude with a targeted prompt:
  *"Extract physical_markers and yoga_check from this rule text. Return empty lists if none present."*
- Patches existing documents using `update_many` with `$set` on only the new fields
- Does NOT touch any existing fields — additive-only patch
- Runs with `--dry-run` first

**Priority order for backfill:**
1. TBA Ch 15 (planet-in-house) — highest value for physical appearance data
2. BPHS Ch 12–24 (house chapters) — secondary appearance data
3. BPHS Ch 47–59 (dasha chapters) — yoga_check rarely applicable; physical markers sparse

**Status:** NOT YET BUILT — deferred until Ch 16 is validated and live.

**Query to identify backfill candidates when ready:**
```python
# Rules missing physical_markers field entirely
db.interpretation_rules.count_documents({
    "interpretation.physical_markers": {"$exists": False},
    "approval_status": {"$ne": "deprecated"}
})

# Rules missing yoga_check field
db.interpretation_rules.count_documents({
    "condition.yoga_check": {"$exists": False},
    "approval_status": {"$ne": "deprecated"}
})
```

---

## 9. Key Learning — Dry Run vs Live Divergence

> **Higher live count ≠ over-split.** Always verify by reading the source sloka.

Ch 59 slokas 20-21 and 41-42 both showed dry runs (1 and 2 rules) vs live (4 rules each). Both dry runs were WRONG — the live run correctly applied SPLITTING GUIDANCE. The rule: if live count is higher, check the source text. If it lists N distinct house positions or dignity states → N rules is correct.

---

## 10. Source Files on Disk

Location: `/Users/apple/Documents/Knowledge Engine_eBooks/`

### Yoga chapters — available for immediate ingestion:

| File | Format | Status |
|---|---|---|
| `BPHS_Ch35_Nabhasa Yogas.rtf` | RTF | ✅ ingested (Ch 35 done) |
| `BPHS_Ch36_Many Other Yogas.rtf` | RTF | ✅ ingested (Ch 36 done) |
| `BPHS_Ch37_Lunaryogas.pdf` | PDF | ✅ ingested (Ch 37 done) |
| `BPHS-Ch38_SolarYogas.pdf` | PDF | ✅ ingested (Ch 38 done) |
| `BPHS_Ch39_Raja Yogas.rtf` | RTF | ✅ ingested (Ch 39 done) |
| `BPHS_Ch40_Yogas for Royal Association.pdf` | **PDF** | 🔜 **NEXT — ready to ingest** |
| `BPHS_Ch41_Yogas for wealth.pdf` | **PDF** | 🔜 ready to ingest after Ch 40 |
| `300_Important_Combinations_BV_Raman.pdf` | **PDF** | 🔜 ready (large — assess size first) |

### Dasha chapters — all ingested:

BPHS Ch 47/48/52/53/54/55/56/57/58/59/60 — all in `horoscope_db`. RTFs in eBooks folder.
Ch 61 RTF: `BPHS_ch 61_Vol2.rtf` — available but not yet ingested.

### TBA (Text-Book of Astrology):
- Ch 15 (Planets in Houses/Signs): ingested, NOT validated → `tba-ch15-v1-20260424`
- Ch 16 (Yogas): ✅ fully validated → `tba-ch16-v1-20260425`
- Full TBA source: `ATextBookOfAstrology/` folder in eBooks

---

## 11. Git Status — as of Session 9 end (27 Apr 2026)

Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
Branch: `main` (deploy-on-push to Vercel + Render)

**Last commits (most recent first):**
```
39cd966 fix(knowledge-engine): dedup Lal Kitab Ch19 double-ingest + validator dosha guidance
82da579 feat(knowledge-engine): ingest Lal Kitab Ch 19 Mangalik Evil — 78 rules
21d82fc docs(knowledge-engine): refresh HANDOVER for Session 9 start
0233bae fix(knowledge-engine): raise max_tokens to 8192 + join standalone RTF headings
c2ecefb docs(knowledge-engine): refresh HANDOVER for Session 9 start
```

**No uncommitted changes.** Repo is clean as of Session 9 end.
