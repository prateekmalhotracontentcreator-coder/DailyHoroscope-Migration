# Knowledge Engine — Session Handover
> Last updated: 21 Apr 2026
> Written at end of Session 3 (context compressed twice before this point)
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

### Rules in DB: ~1,726 RTF-sourced rules (all `approval_status = pending_review` or `auto_approved`)

### antardasha_planet coverage: **802 / 802 = 100%** across Ch 47–58 ✅
- 2 universal meta-rules: `R-BPHS47-008`, `R-BPHS47-009` → `applies_to_all_dasha_lords: true`

### Chapters ingested (RTF pipeline):

| Source | Batch IDs | Rules | Status |
|---|---|---|---|
| BPHS Vol 1 Ch 12-18 | bphs-ch12..18-v2-20260414 | 241 | ✅ validated |
| BPHS Vol 1 Ch 19-23 | bphs-ch19..23-v2-20260415 | 119 | ✅ validated |
| BPHS Vol 1 Ch 24 | bphs-ch24-v2-20260416 | 376 | ✅ validated |
| BPHS Vol 2 Ch 47 | bphs-ch47-dasha-20260416 | 93 | ✅ validated |
| BPHS Vol 2 Ch 48 | bphs-ch48-dasha-20260416 | 46 | ✅ (antardasha backfill clean) |
| BPHS Vol 2 Ch 52 | bphs-ch52-dasha-20260416 | 93 | ingested, not validated |
| BPHS Vol 2 Ch 53 | bphs-ch53-dasha-20260417 | 72 | ingested, not validated |
| BPHS Vol 2 Ch 54 | bphs-ch54-dasha-20260417 | 86 | ingested, not validated |
| BPHS Vol 2 Ch 55 | bphs-ch55-dasha-20260417 | 96 | ingested, not validated |
| BPHS Vol 2 Ch 56 | bphs-ch56-dasha-20260418 | 126 | ✅ validated |
| BPHS Vol 2 Ch 57 | bphs-ch57-dasha-20260419 | 132 | ✅ validated |
| BPHS Vol 2 Ch 58 | bphs-ch58-dasha-20260419 | 104 | ✅ validated |
| BPHS Vol 2 Ch 59 | bphs-ch59-dasha-20260420 | 88 | ✅ validated |

---

## 4. Immediate Next Steps (in priority order)

### Step 1 — Test the new SPLITTING GUIDANCE (NEXT ACTION)

```bash
cd /Users/apple/DailyHoroscope-Migration/backend
export ANTHROPIC_API_KEY="sk-ant-..."
python3 /tmp/test_splitting.py
```

Verify:
- Sloka 45-47: ~9 rules extracted (3 dignity + 2 category + 3 house + 1 timing)
- Sloka 1-2: ~6 rules (2 category + 1 Asc lord + 3 separate lord rules)
- Sloka 3-4: 1-2 rules only (compound condition — do NOT over-split)

If output is correct → proceed. If wrong → adjust prompt before anything else.

### Step 2 — Gap-fill sweep: Ch 59 sloka 1-2

```bash
python3 scripts/patch_slokas.py \
  --rtf "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_ch59_Vol2.rtf" \
  --chapter 59 \
  --dasha-lord Ketu \
  --batch-id bphs-ch59-dasha-20260420 \
  --slokas "1-2" \
  --mongo-url "$MONGO_URL" \
  --db-name horoscope_db \
  --dry-run
```

Expected: +3 new rules (9th lord / 10th lord / 4th lord split that was merged in original ingest).

### Step 3 — Gap-fill sweep: ALL Ch 47-59 for splitting under-extractions

The new SPLITTING GUIDANCE will produce more rules per sloka than the old prompt. For previously ingested chapters (Ch 47-58), slokas with house-list or dignity-list conditions were under-extracted.

**Strategy:** 
- Do NOT re-ingest entire chapters (risk of duplicates)
- Use `patch_slokas.py` targeted at specific slokas identified by a DB query
- Query to find candidates: rules whose `interpretation.summary` contains patterns like `"kendra, trikona"` or `"6th, 8th"` or `"own sign"` — these are likely merged rules

Run this query first to assess scale:

```python
import pymongo, re
client = pymongo.MongoClient("YOUR_MONGO_URL")
col = client["horoscope_db"]["interpretation_rules"]
patterns = [
    r"kendra.*trikona",
    r"6th.*8th",
    r"8th.*12th",
    r"own sign.*exaltation",
    r"exaltation.*own sign",
    r"friend.s sign",
]
candidates = []
for doc in col.find({"source.batch_id": {"$regex": "bphs-ch(47|52|53|54|55|56|57|58|59)"}}, 
                     {"rule_id":1, "source.sloka":1, "interpretation.summary":1, "source.batch_id":1}):
    summary = doc.get("interpretation",{}).get("summary","")
    for p in patterns:
        if re.search(p, summary, re.IGNORECASE):
            candidates.append(doc)
            break
print(f"Candidate under-split rules: {len(candidates)}")
for d in candidates[:20]:
    print(f"  {d['rule_id']} | {d['source'].get('batch_id','')} sloka {d['source'].get('sloka','')} | {d['interpretation']['summary'][:80]}")
```

### Step 4 — Ch 59 Open Points (Rules Browser)

- Check 4 flagged rules: Rules Browser → filter flagged, batch `bphs-ch59-dasha-20260420`
- Sloka 45-47: verify 2 extracted rules cover all placement conditions

### Step 5 — Next Chapter Ingestion

**BPHS Ch 60** — Prateek has not yet provided RTF. Ask him.

Other dasha chapters available:
- Ch 48 (Moon MD) — already in DB but no RTF confirmed
- Ch 52-55 (Ketu/Venus/Mars/Moon MD) — in DB, no validation stats recorded

---

## 5. Key Architecture Decisions (locked — do not revisit without strong reason)

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
| `patch_slokas.py` | Gap-fill under-extracted slokas | `--slokas --dasha-lord --batch-id --dry-run` |
| `validate_rules.py` | Run validator on a batch | `--batch-id` |
| `backfill_antardasha_planet.py` | Backfill `condition.antardasha_planet` | `--dry-run` (Pass 5 complete) |
| `extract_book.py` + `batch_ingest.py` | OCR/PDF pipeline (separate, keep archived) | not for RTF use |

All scripts: `cd /Users/apple/DailyHoroscope-Migration/backend`

---

## 7. Parser Fixes (cumulative — applied to `ingest_bphs_dasha_v1.py`)

| Fix | What | Trigger |
|---|---|---|
| `temperature=0` | Deterministic extraction | Ch 57 non-determinism |
| `condition.antardasha_planet` field | Queryable sub-period planet | KE filtering |
| `SPLITTING GUIDANCE` added | Explicit split/no-split examples | Ch 58 under-extraction |
| `SPLITTING GUIDANCE` OVERHAULED | House-by-house + dignity-by-dignity splits + strength_band | Ch 59 sloka 20-21 analysis — **21 Apr 2026** |
| Period-as-range-separator `5.6.` → `5-6` | `split_into_sloka_blocks()` regex | Ch 59 sloka 5-6 missing |
| Ch 59 added to `INTRO_SLOKAS_BY_CHAPTER` with empty set | No skip-list inheritance | Ch 59 sloka 1-2 |

---

## 8. Open Points Across All Chapters

### Ch 12-24 (House chapters)
- 38 flagged rules — not yet reviewed in Rules Browser
- 13 contradiction pairs — not yet resolved
- 197 pending_human_review — awaiting co-founder sign-off
- **Under-split review pending** — same house/dignity bundling issue exists here; assess after Step 3 gap-fill sweep methodology is proven on dasha chapters

### Ch 47-59 (Dasha chapters)
- Ch 52/53/54/55 — in DB but no validation stats recorded. Run `validate_rules.py` on each when Prateek is ready
- Ch 57 slokas 20-21, 30-31 — over-split suspected, review in Rules Browser
- Ch 59 sloka 45-47 — verify 2 rules cover all conditions
- Ch 59 sloka 1-2 — gap-fill with new splitting prompt (Step 2 above)

### Co-founder Review Workflow
Not yet commissioned. Brief needed for dedicated sign-off queue. Prateek must approve before any rule gets `approval_status = 'approved'` (the only status the live backend queries).

### CPath-1 Items
- Item 18: `longevity_router.py` import fail — not addressed
- Item 19: science_registry editor — not addressed
- Commission I-K: Kota Chakra — not addressed

---

## 9. Key Learning — Dry Run vs Live Divergence

> **Higher live count ≠ over-split.** Always verify by reading the source sloka.

Ch 59 slokas 20-21 and 41-42 both showed dry runs (1 and 2 rules) vs live (4 rules each). Both dry runs were WRONG — the live run correctly applied SPLITTING GUIDANCE. The rule: if live count is higher, check the source text. If it lists N distinct house positions or dignity states → N rules is correct.

---

## 10. RTF Files Available

Location: `/Users/apple/Documents/Knowledge Engine_eBooks/`

Confirmed available:
- BPHS Ch 57, 58, 59 Vol 2 ✅
- BPHS Ch 56 Vol 2 ✅

Pending from Prateek:
- BPHS Ch 60 (next in sequence)
- BPHS Ch 52, 53, 54, 55 (in DB but RTF status unclear)
- Lal Kitab, Longevity, Text-Book of Astrology — OCR batches in DB, RTF files not prepared

---

## 11. Git Status

Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
Branch: `main` (deploy-on-push to Vercel + Render)
Last commit: `ea9bd7c` — Ch 59 sloka 20-21 / 41-42 assessment corrected

**Splitting Guidance overhaul** is committed locally but Prateek runs from the repo. Confirm push status at session start:
```bash
cd /Users/apple/DailyHoroscope-Migration && git log --oneline -5
```
