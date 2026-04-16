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
| **TOTAL** | | | **829** | **553 (67%)** | **208 (25%)** | **74 (9%)** | |

All contradictions: 13 pairs (all in Ch 12-18 and Ch 19-23; Ch 24 and Ch 47 = 0).

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
| Ch 48, Ch 52-60 | ❌ Needs RTF conversion from PDF first |
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

### Priority 1: Ch 48 — Dasas of Lords of Various Houses
- **What:** Effects when you run the Dasha of the lord of each house (1st lord Dasha → 12th lord Dasha)
- **Condition type:** `dasha_of_house_lord` — note this is NOT yet in the script's condition types. `ingest_bphs_dasha_v1.py` currently uses `dasha_planet`. For Ch 48 you may want to either:
  - Use the existing script as-is (condition.type stays `dasha_planet`, `dasha_lord` = the house lord planet), OR
  - Add a `--mode house_lord` flag that sets `condition.type = dasha_of_house_lord` and adds a `house` field
  - **Recommended:** check the Ch 48 RTF structure first before deciding
- **Script:** `ingest_bphs_dasha_v1.py --chapter 48`
- **RTF status:** Needs conversion from `BPHS - 2 RSanthanam.pdf` (Vol 2 PDF is in the eBooks folder)
- **Est. rules:** ~100-120

### Priority 2: Ch 52-60 — Antardasha chapters (9 chapters)
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
- ⬜ BPHS Vol 2 Ch 48 (~100-120 rules) ← next
- ⬜ A Text Book of Astrology Ch 15 (~100-150 rules)

---

## Open Issues to Clear Before Co-Founder Review
1. **74 flagged rules** across all batches — pull from Admin > Rules Browser (filter: flagged), determine: dismiss / edit / escalate
2. **208 pending_human_review rules** — awaiting sign-off
3. **13 contradiction pairs** (all in Ch 12-23) — verify if genuine classical contradictions or validator false positives
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
