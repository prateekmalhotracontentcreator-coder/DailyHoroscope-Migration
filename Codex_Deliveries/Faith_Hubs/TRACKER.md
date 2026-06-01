# Faith & Scripture -- Module Tracker
> Path: `Codex_Deliveries/Faith_Hubs/TRACKER.md`
> Last updated: 2026-05-31 IST · v1.1

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🔴 CRITICAL BLOCK (L1 failures on 3 of 4 page types) |
| **Backend** | ✅ Delivered + registered in `server.py` |
| **Frontend routes** | Partially wired (hub/transit/daily routes exist; verify) |
| **Mongo seed** | ❌ NOT seeded (blocked -- critical L1 failures) |
| **ECHO/PACE scan** | ✅ Run 2026-05-31 -- Gita/Bible/Transit BLOCKED ❌ |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| **FAITH-1** | Core hub structure | ✅ DELIVERED | `CODEX_COMMISSION_FAITH_1.md` |
| **FAITH-1A** | Hub enhancement | ✅ DELIVERED | `CODEX_COMMISSION_FAITH_1A.md` |
| **FAITH-20K** | 10,500 Gita + 6,000 Bible + 156 Transit + 144 Daily pages | ✅ DELIVERED (generator in repo) | `CODEX_COMMISSION_FAITH_20K.md` |
| **FAITH-HUBS** | Faith hub pages | ✅ DELIVERED | `CODEX_COMMISSION_FAITH_HUBS.md` |
| **FAITH-REWRITE** | L1 fix: verse-specific anchoring for Gita/Bible/Transit/Daily | 🔴 READY TO ISSUE -- CRITICAL | (brief to be drafted) |

---

## Open Points

| ID | Description | Owner | Status |
|---|---|---|---|
| FAITH-OP-1 | Issue FAITH-REWRITE commission (CRITICAL -- Gita L1=100%, Bible L1=82%, Transit L1=100%) | TT/CC | READY |
| FAITH-OP-2 | Draft FAITH-REWRITE brief: verse-specific anchoring (see root cause below) | CC | IN PROGRESS |
| FAITH-OP-3 | Do NOT seed any Faith collections until FAITH-REWRITE passes L1 < 50% | CC | BLOCKER |
| FAITH-OP-4 | Re-run ECHO/PACE scan after FAITH-REWRITE delivery | CC | PENDING REWRITE |
| FAITH-OP-5 | DAILY pages: L1 at exactly 50.0% (on-gate) -- minor seasonal framing variation may be sufficient inline fix | CC | ASSESS |
| FAITH-OP-6 | Run Layer G before seeding | CC | PENDING |

---

## ECHO/PACE Results (2026-05-31)

Full report: `Codex_Deliveries/ECHO_PACE/ECHO_PACE_SCAN_RUD_CRY_FAITH_2026-05-31.md`

| Page Type | Total | Sample | L1 | L2 | L3 | Verdict |
|---|---|---|---|---|---|---|
| GITA | 10,500 | 3,480 | 100.0% | FAIL ❌ | FLAGGED ⚠️ | BLOCKED ❌ |
| BIBLE | 6,000 | 100 | 81.7% | FAIL ❌ | FLAGGED ⚠️ | BLOCKED ❌ |
| TRANSIT | 156 | all | 99.5% | FAIL ❌ | FLAGGED ⚠️ | BLOCKED ❌ |
| DAILY | 144 | all | 50.0% | FAIL ❌ | FLAGGED ⚠️ | ON-GATE ⚠️ |

### L1 Root Cause -- Gita (100%)
`get_gita_page()` fills `summary`, `hook`, and `application` from `situation['hook']`, `situation['hidden_fear']`, `situation['practice_shift']` -- constants per situation. These strings are **identical for every verse in the same situation** (e.g., all 700+ Gita pages for "Relationship Breakdown" share word-for-word body text). Only the chapter:verse number token changes, which has negligible TF-IDF weight → cosine = 1.0 within cluster.

Key evidence -- the following phrase appears verbatim on every one of the 10,500 Gita pages:
```
"It does not ask for denial. It asks for a truer next step"
```

### L1 Root Cause -- Bible (81.7%)
`summary` field: `"This page approaches {transition} through the Bible theme of {topic}, keeping the promise practical, emotionally honest, and connected to a parallel Vedic bridge."` -- this fixed sentence appears on every Bible page. Verse text contributes some variation, but shared boilerplate vocabulary dominates.

### L1 Root Cause -- Transit (99.5%)
Transit pages exist in Gita and Bible tradition variants. "Mars Retrograde - Gita" vs "Mars Retrograde - Bible" share identical transit-level body content (panchang description, transit_layer, practice text) with only the verse citation differing → near-identical TF-IDF vectors.

### Fix Specification for FAITH-REWRITE Commission
Must address all four areas:

1. **Gita per-verse anchoring**: `hook` and `summary` must incorporate the specific verse's translation keywords (min 2 verse-unique words, not situation boilerplate). Use `_hash_index(chapter, verse_num, situation_slug, modulus=8)` to select from 8 situation sub-templates, each seeded by different verse content.

2. **Bible per-verse body**: `summary` and `emotional_frame` must vary by verse content. At minimum: 5 topic-variant opening sentences, selected by hash. Remove the fixed template sentence.

3. **Transit tradition separation**: Gita-tradition and Bible-tradition transit pages must have meaningfully distinct body text. Currently near-identical. Each tradition must have a minimum of 3 distinct framing approaches per transit family (retrograde, ingress, etc.).

4. **Daily seasonal variation**: `summary` and `message` must have at least 5 monthly framing variants per sign, hash-selected. Currently 12 months × 12 signs share too much seasonal vocabulary.

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.1 | 2026-05-31 | ECHO/PACE scan run. CRITICAL: Gita L1=100%, Bible L1=82%, Transit L1=100%. All 4 types L2 FAIL. Module BLOCKED. FAITH-REWRITE commission brief required. Tracker created. | CC | `ECHO_PACE_SCAN_RUD_CRY_FAITH_2026-05-31.md` |
| v1.0 | 2026-05 | FAITH-20K generator delivered by Codex (faith_gita_data.py, faith_bible_data.py, faith_seo_data.py). Backend registered. | Codex | `CODEX_COMMISSION_FAITH_20K.md` |
