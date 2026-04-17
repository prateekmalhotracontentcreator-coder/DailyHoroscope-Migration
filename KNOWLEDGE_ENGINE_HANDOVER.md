# Knowledge Engine — Session Handover
Date: 17 April 2026

## Non-Negotiable Rule
`approval_status = "approved"` is the ONLY status that reaches live users.
Flow: `pending_review` → validated → `auto_approved` / `pending_human_review` → co-founder promotes to `approved`.
**Decision standing:** Do NOT promote anything yet. Promote only after full multi-book ingest is complete.

---

## Current DB State

| Source | Chapter | Topic | Rules | auto_approved | pending_human_review | flagged | Batch ID |
|---|---|---|---|---|---|---|---|
| BPHS Vol 1 | Ch 12-18 | Houses 1-7 | 241 | 140 (58%) | 79 (33%) | 28 (12%) | bphs-ch12..18-v2-20260414 |
| BPHS Vol 1 | Ch 19-23 | Houses 8-12 | 119 | 70 (59%) | 39 (33%) | 10 (8%) | bphs-ch19..23-v2-20260415 |
| BPHS Vol 1 | Ch 24 | Bhava Lords | 376 | 267 (71%) | 77 (20%) | 32 (9%) | bphs-ch24-v2-20260416 |
| BPHS Vol 2 | Ch 47 | Mahadasha by Planet | 93 | 76 (82%) | 13 (14%) | 4 (4%) | bphs-ch47-dasha-20260416 |
| BPHS Vol 2 | Ch 48 | Dasha of House Lords | 46 | 34 (74%) | 11 (24%) | 1 (2%) | bphs-ch48-dasha-20260416 |
| BPHS Vol 2 | Ch 52 | Antardasha in Sun MD | 93 | 77 (83%) | 13 (14%) | 3 (3%) | bphs-ch52-dasha-20260416 |
| BPHS Vol 2 | Ch 53 | Antardasha in Moon MD | 68 | 52 (76%) | 12 (18%) | 4 (6%) | bphs-ch53-dasha-20260417 |
| **TOTAL** | | | **1,036** | **716 (69%)** | **244 (24%)** | **82 (8%)** | |

All contradictions: 25 pairs (13 in Ch 12-23; 5 in Ch 48; 3 in Ch 52; 4 in Ch 53).
Note: Ch 53 has 3 genuinely missing slokas (53, 54, 55) from the source edition — see below.

---

## ⚠️ Critical Workflow Rule — Always Run Scripts from Main

**Always run ingest/validate scripts from the main repo directory:**
```
cd ~/DailyHoroscope-Migration
python3 backend/scripts/ingest_bphs_dasha_v1.py ...
```
**Never run from a worktree path.** Worktrees are for code editing only — Claude Code edits land in the worktree branch and must be committed + merged to main before scripts are executed. Running from a worktree path risks using stale/old code or mismatched paths.

**Workflow:**
1. Claude Code edits script in worktree
2. Commit + merge (or copy file) to main
3. Run script from `~/DailyHoroscope-Migration/`

---

## Scripts Available (all in `backend/scripts/`)

| Script | Purpose | Key args |
|---|---|---|
| `ingest_bphs_houses_v2.py` | House + Bhava Lord chapters (BPHS Vol 1) | `--rtf --chapter 12-24 --house 1-12 or 0` |
| `ingest_bphs_dasha_v1.py` | Dasha chapters (BPHS Vol 2 Ch 47/48/52-60) | `--rtf --chapter --dasha-lord (optional)` |
| `validate_rules.py` | Run validation on a batch | `--mongo-url --db-name --batch-id` |
| `patch_punctuation.py` | Add terminal punctuation to rules missing it | `--batch-id` |
| `reset_to_pending.py` | Reset rejected rules back to pending_review | `--batch-id` |
| `peek_rules.py` | Quick spot-check of rules in DB | `--batch-id --limit` |

**All scripts require:** `ANTHROPIC_API_KEY`, `MONGO_URL`, `DB_NAME=EverydayHoroscope`

---

## RTF Files Location
`/Users/apple/Documents/Knowledge Engine_eBooks/`

| File | Status |
|---|---|
| `BPHS Ch 12-23 Vol 1.rtf` (individual files) | ✅ Ingested |
| `BPHS Ch 24 Vol1.rtf` | ✅ Ingested |
| `BPHS Ch 47 Vol 2.rtf` | ✅ Ingested |
| Ch 48 | ✅ Ingested (46 rules, bphs-ch48-dasha-20260416) |
| Ch 52 | ✅ Ingested (93 rules, bphs-ch52-dasha-20260416) |
| Ch 53-60 | ❌ Needs RTF conversion from PDF (only Ch 52 RTF existed) |
| A Text Book of Astrology Ch 15, 16 | ❌ Needs RTF conversion |

---

## What Was Built This Session

### 1. `ingest_bphs_houses_v2.py` — extended for Ch 24
- `--house 0` = lord-placement mode: `condition.type = lord_placement`, no house number set on rules
- `--chapter` now accepts 12–24 (was 12–23)
- Ch 24 added to `CHAPTER_NAMES`: `"Effects of Bhava Lords"`
- Extraction prompt, condition builder, fallback rule all handle house=0 correctly

### 2. `ingest_bphs_dasha_v1.py` — new script for Dasha chapters
Key design decisions worth knowing:
- **Position-map planet attribution**: pre-scans entire RTF text for all planet section headings, builds `(char_position, planet)` list, then each sloka looks up the last heading before its start position. This is more reliable than per-block detection because section headings in Ch 47 appear as free text between slokas (not as numbered sloka headings).
- **Transition planet override**: sloka 16-22 says "after describing Sun Dasa... I will now come to the effects of the Moon Dasa" — `detect_transition_planet()` catches the forward-looking phrase and overrides the position map's "Sun" attribution to "Moon".
- **Intro-only sloka skip**: slokas 44, 52, 61, 71, 78 are single-sentence planet introductions (no prediction content) — skipped via `_INTRO_ONLY_RE`.
- **Zero-space period fix**: `88-89.Similar` (no space after period) now caught by `[ \t]*` instead of `[ \t]+` in sloka_re.
- **Colon separator**: `34-39:` handled by `[.:]` in sloka_re.

---

## Next Session — Immediate Tasks

### ✅ Ch 48 — Dasas of Lords of Various Houses — COMPLETE
- **46 rules** | `condition.type = "dasha_of_house_lord"` | `condition.house` = 1-12 (or null for general)
- All 12 houses covered + 19 general/multi-house combination rules
- Batch ID: `bphs-ch48-dasha-20260416`
- **Script note:** `ingest_bphs_dasha_v1.py` auto-detects Ch 48 and uses house-lord mode (no flag needed)
- **RTF:** `BPHS Ch 48 Vol 2.rtf` ✅ already existed in eBooks folder

### ✅ Ch 53 — Antardasha in Moon Mahadasha — COMPLETE (68 rules + 4 patch)
- **68 rules** ingested from RTF | `condition.type = "dasha_planet"` | `dasha_lord = "Moon"`
- Batch ID: `bphs-ch53-dasha-20260417`
- **Missing slokas 53-55** (Venus Antardasha unfavourable + remedy) — genuinely absent from RS Santhanam Vol 2 edition
  - **Option C applied:** 4 patch rules inserted via `patch_ch53_venus_antardasha.py`
  - Batch ID: `bphs-ch53-venus-patch-20260417`
  - `approval_status = pending_human_review` | `confidence.base = 0.65` | `source.edition = "codex_supplement"`
  - Covers: 3 unfavourable (Venus debilitated/dusthana/malefic-afflicted) + 1 remedy
  - **Expert review required before promotion to approved** — these are supplemented, not verbatim

**To run the patch:** (from `~/DailyHoroscope-Migration/`)
```bash
python3 backend/scripts/patch_ch53_venus_antardasha.py \
  --mongo-url "$MONGO_URL" --db-name EverydayHoroscope
```

### Priority 1 (next): Remaining Antardasha chapters — Ch 54-60
- **What:** Sub-period effects for each Mahadasha × Antardasha combination
- **Script:** Same `ingest_bphs_dasha_v1.py --chapter 52 --dasha-lord Sun` (etc.)
- **ANTARDASHA_CHAPTER_LORD** dict already wired: `{52: "Sun", 53: "Moon", ..., 60: "Venus"}`
- **RTF status:** Need 9 RTF conversions from Vol 2 PDF
- **Est. rules:** ~80 per chapter × 9 = ~720 rules

### Priority 3: A Text Book of Astrology — Ch 15
- **What:** Planets in Different Houses (cross-validation baseline for BPHS house rules)
- **Script:** Extend `ingest_bphs_houses_v2.py` OR new `ingest_textbook_v1.py` (different `BOOK_ID = "textbook_astrology"`, different `source.book`)
- **RTF status:** Needs conversion
- **Est. rules:** ~100-150

---

## Approval Milestone Target
Promote to `approved` after reaching ~950 rules:
- ✅ BPHS Vol 1 Ch 12-24 complete (736 rules)
- ✅ BPHS Vol 2 Ch 47 complete (93 rules)
- ✅ BPHS Vol 2 Ch 48 complete (46 rules)
- ✅ BPHS Vol 2 Ch 52 complete (93 rules) — 968 total so far — milestone crossed
- ✅ BPHS Vol 2 Ch 53 complete (68 rules + 4 patch = 72) — **1,040 total**
- ⬜ Ch 54-60 (7 remaining Antardasha chapters) — need RTF conversion from PDF
- ⬜ A Text Book of Astrology Ch 15 (~100-150 rules)

---

## Pending Codex Review — Do Not Lock Until Confirmed

Two design decisions raised in Founder session (17 Apr 2026) — sent to Codex for validation:

**A — Country Kundali as α (Macro) Input** — `CODEX_REVIEWED ✅ 17 Apr 2026`
- Phase 1: `alpha` stays as `float | ContextSignal` — no change
- Phase 2: introduce typed `CountryKundaliSignal` as subtype under `alpha` umbrella
- `dasha_alignment` = compatibility between individual's active maha/antara lords and country chart's active mundane period lords, normalised 0–1
- Weighting model: <2yr abroad = 70/30 (birth/residence), 2–7yr = interpolate, >7yr = 30/70, same country = 100/0
- "Current Place of Residence" form field feeds residence country input
- Do not build before Commission J / World Context work
- **Next action:** Codex to draft TD spec entry (Phase 2) for `CountryKundaliSignal`

**B — Forecast Tier / Life Area Outlook** — `CODEX_REVIEWED ✅ 17 Apr 2026`
- Renamed from "Quality Tier" — it is outcome valence, not reliability
- Schema field: `forecast_tier` | User-facing label: `Life Area Outlook` [PENDING FOUNDER CONFIRM]
- Computed per section/domain (not per rule, not per full report)
- Weighted polarity by `effective_confidence` + backbone priority + final scored intensity — not majority vote
- Guardrail: if `representation_mode = honest_uncertainty` → suppress Excellent/Critical, collapse to middle bands
- Must not override `representation_mode`
- Phase 2: internal only first (tone selection, Arc Angel reconciliation, QA). User-facing only after wording tested.
- **Next action:** Codex to draft TD spec entry (Phase 2), aligned to existing TD structure

**Other design decisions locked this session (no Codex review needed):**
- Language tiers: Basic (simplified) / Premium (modern) / Pro (classical paraphrase — our authored text, not verbatim Santhanam)
- IP: Astrological if-then rules are facts, not copyrightable. Lightweight AI humanising layer in Phase 2.
- Paraphrasing via Codex: was scoped in early sessions, parked for Phase 2 — unpause then.
- Vector DB: deferred. MongoDB M0 sufficient for Phase 1 structured queries.

---

## Open Issues to Clear Before Co-Founder Review
1. **75 flagged rules** across all batches — pull from Admin > Rules Browser (filter: flagged), determine: dismiss / edit / escalate
2. **219 pending_human_review rules** — awaiting sign-off
3. **18 contradiction pairs** (13 in Ch 12-23; 5 in Ch 48) — verify if genuine classical contradictions or validator false positives
4. **Ch 15 low auto-approve (25%) and Ch 19 (33%)** — outlier batches; likely validator flags multi-condition rules. Inspect before promotion.

---

## Validation Command Template
```bash
# Ingest
python3 backend/scripts/ingest_bphs_dasha_v1.py \
  --rtf "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS Ch 48 Vol 2.rtf" \
  --chapter 48 \
  --mongo-url "$MONGO_URL" --db-name EverydayHoroscope

# Validate
python3 backend/scripts/validate_rules.py \
  --mongo-url "$MONGO_URL" --db-name EverydayHoroscope \
  --batch-id bphs-ch48-dasha-YYYYMMDD
```
