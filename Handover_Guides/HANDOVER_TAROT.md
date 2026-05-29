# Handover Guide -- Tarot Module
> Prepared by: Claude Code (Main Thread) → New Dedicated Thread
> Date: 2026-05-29
> Purpose: New thread integrates TAR-SEO-1, activates TAR-SEO-2, and owns all future Tarot work.

---

## 1. Your Role in the New Thread

You are the **Tarot thread**. Your scope is:
- ~~Integrate TAR-SEO-1~~ ✅ DONE (`8f36fc8`) -- 199 pages live
- ~~Activate TAR-SEO-2~~ ✅ DONE (`b0dfdd4`) -- content rewritten
- ~~ECHO/PACE quality gate~~ ✅ CLEARED 2026-05-30 -- strict L1-L3 + Layer G 15/15 PASS
- **Issue TAR-SEO-3** (4,621 card×spread combination pages) -- brief at `Codex_Deliveries/Tarot/CODEX_COMMISSION_TAR_SEO_3_COMBINATIONS.md`
- Own all future Tarot feature or SEO commissions

**You do NOT own:** KE, SEO 20K, Book Decode, Strategist/LK, or any other module.

---

## 2. Reference Files -- Read These on Startup

| Priority | File | What it Contains |
|---|---|---|
| 🔴 MUST READ | `Codex_Deliveries/Tarot/TRACKER.md` | Live Tarot module status (v1.4) |
| 🔴 MUST READ | `Codex_Deliveries/Tarot/CODEX_COMMISSION_TAR_SEO_1.md` | TAR-SEO-1 full brief -- what was built, how to integrate |
| 🔴 MUST READ | `Codex_Deliveries/Tarot/CODEX_COMMISSION_TAR_SEO_2_REWRITE.md` | TAR-SEO-2 brief -- content rewrite scope |
| 🟠 READ | `Codex_Deliveries/Tarot/TAROT_V4_UI_RECONCILIATION_NOTE_2026-05-22.md` | Context on how TAR-v4 was reconciled against existing page |
| 🟠 READ | `Codex_Deliveries/Tarot/TAR_ECHO_PACE_GAI_CONSULTATION.md` | ECHO/PACE content quality guidance for Tarot SEO pages |
| 🟠 READ | `Codex_Deliveries/Tarot/TAR_SEO_TITLE_HUMANIZATION_LIST.md` | Pre-approved humanized titles for Tarot SEO pages |
| 🟡 REFERENCE | `#5_CODEX_COMMISSION_TABLE.md` (MODULE 8) | Master commission status for Tarot |
| 🟡 REFERENCE | `#3_ACTION_TRACKER.md` (M-15) | TAR-SEO-1 integration action item |

---

## 3. Current State -- What is Live

### TAR-v4 -- ✅ INTEGRATED (QA 2026-05-27)

The interactive Tarot tool is fully live at `/tarot`. 5 tabs confirmed:
- Daily Draw · Spreads · Favorable Periods · Journal · History

| File | Role |
|---|---|
| `frontend/src/pages/tarot/TarotPage.jsx` | Main Tarot page -- all 5 tabs |
| `backend/tarot_router.py` | All Tarot API endpoints |
| `frontend/public/tarot_cards.json` | 78-card SVG deck |

**Punya Rewards hooks wired:** `tarot_daily_draw`, `tarot_spread_complete`, `tarot_bookmark` -- all fire-and-forget via `safeClaimPunyaAction()`.

**Architecture rule: TAR-v4 is visual only.** Do NOT modify `tarot_router.py` or `tarot_cards.json` in any future Tarot work unless explicitly scoped.

---

## 4. Current Live State -- TAR-SEO-1 + TAR-SEO-2 Already Integrated

> ✅ **TAR-SEO-1 and TAR-SEO-2 are both already live in production** (confirmed 2026-05-29 via Codex delivery doc cross-check). Your task is NOT integration -- it is ECHO/PACE quality sign-off.

### What Is Live

| Item | Commit | Status |
|---|---|---|
| TAR-SEO-1 -- 4 routes + backend router | `8f36fc8` | ✅ Live in `main` |
| TAR-SEO-2 -- content rewrite (100 spreads + 78 cards) | `b0dfdd4` | ✅ Live in `main` |

**Live files:**
- `backend/tarot_seo_router.py` -- SEO endpoints, registered in `server.py` at prefix `/api/seo`
- `frontend/src/pages/tarot-seo/TarotSeoHubPage.jsx` → `/tarot/spreads`
- `frontend/src/pages/tarot-seo/TarotSpreadPage.jsx` → `/tarot/spread/:spreadSlug`
- `frontend/src/pages/tarot-seo/TarotCardPage.jsx` → `/tarot/card/:cardSlug`
- `frontend/src/pages/tarot-seo/TarotIntentionPage.jsx` → `/tarot/for/:intentionSlug`
- `backend/tarot_seo_data.py` -- 100 spreads, 78 cards, 20 intentions (post-TAR-SEO-2 rewrite)

**Total live URLs: 199 pages** (1 hub + 100 spreads + 78 cards + 20 intentions)

### Your First Task -- ECHO/PACE Quality Sign-off

The pages are live. The content has been rewritten. The only remaining gates before this module is fully QA-cleared are the ECHO/PACE scan and Layer G.

### Smart Quote Fix (if needed)
```bash
node -e "
let f=require('fs'),p='frontend/src/pages/tarot/TargetFile.jsx';
let c=f.readFileSync(p,'utf8');
c=c.replace(/"/g,'\"').replace(/"/g,'\"')
   .replace(/'/g,\"'\").replace(/'/g,\"'\");
f.writeFileSync(p,c);console.log('Done');"
```

---

## 5. ECHO/PACE Quality Gate (Mandatory -- Before TAR-SEO-2)

> **This is a blocking gate.** TAR-SEO-1 pages must pass ECHO/PACE before TAR-SEO-2 is activated.

### Why ECHO/PACE First

Tarot SEO pages (199 programmatic pages) are content-dense and risk duplication penalties from Google. The M3 festival-region pages required 9 rounds of GAI optimization to stay below the 40% ceiling. Tarot spread/card/intention pages have similar risk. Catch failures now -- before Google indexes the content.

### Run the Scanner (replaces manual admin panel check)

A 4-layer scanner script is in the repo. **Run this instead of the admin panel:**

```bash
# From repo root -- Layers 1-3 (no API key needed):
python3 tests/echo_pace_tarot_scan.py

# All 4 layers including Google duplication (get SERPER_API_KEY from Render env):
SERPER_API_KEY=your_key python3 tests/echo_pace_tarot_scan.py
```

Output is saved to `tests/echo_pace_tarot_report.json`. Share full console output with TT for sign-off.

### Thresholds (enforced by script)

| Layer | Method | BLOCKED | FLAGGED / WATCH | PASS |
|---|---|---|---|---|
| L1 | TF-IDF cosine inter-page | any pair ≥ 70% | 50-69% | < 50% |
| L2 | N-gram 4+ word match | -- | phrase in ≥ 3 docs | 0 phrases |
| L3 | Jaccard heading match | -- | score ≥ 60% vs corpus | all < 60% |
| LG | Google duplication (Serper) | peak > 40% | avg > 20% | avg ≤ 20% |

### First Run Results (TAR-SEO-1, confirmed 2026-05-29)

| Page Type | L1 | L2 | L3 | LG |
|---|---|---|---|---|
| Spreads (100) | ⚠️ FLAGGED -- 2 near-duplicate topic pairs (60%) | ⚠️ FLAGGED -- deck composition boilerplate in 15 spreads | ℹ️ INFO -- generic names expected | Not yet run |
| Cards (78) | ✅ PASS -- peak 36% | ⚠️ FLAGGED -- 219 Wands suit shared imagery phrases | ℹ️ INFO | Not yet run |
| Intentions (20) | ⚠️ FLAGGED -- 2 pairs | ⚠️ FLAGGED | ℹ️ INFO -- slugs are generic (love, career, etc.) | Not yet run |

**L2 FLAGGED items for Tarot are mostly legitimate shared vocabulary** (deck composition descriptions, tarot suit imagery terms). Review the top offenders in the report -- only escalate to GAI if phrases appear to be verbatim from a source book.

**L1 FLAGGED spread pairs** -- "Manifesting Urgent Financial Abundance" ↔ "Manifesting Fast Secondary Income" (51.6%) and "Settlement vs Going to Trial Analysis" ↔ "Choosing Legal Battle vs Settlement" (60%) -- these are thematically near-duplicate spreads. Assess whether their body prose is sufficiently differentiated.

**Layer G (Google duplication) still required** -- get SERPER_API_KEY from Render dashboard env vars and run with the key before declaring the module QA-passed.

### GAI Optimization Loop (if any page type is BLOCKED)

Reference: `Codex_Deliveries/Tarot/TAR_ECHO_PACE_GAI_CONSULTATION.md`

1. Identify which content fields triggered BLOCKED (script output shows offending phrases)
2. Submit failing content blocks to NLM/GAI for rewrite
3. Update the relevant fields in `backend/tarot_seo_data.py`
4. Re-run script: `python3 tests/echo_pace_tarot_scan.py`
5. Repeat until all BLOCKED items clear
6. Pre-approved humanized titles: `TAR_SEO_TITLE_HUMANIZATION_LIST.md`

### After ECHO/PACE Passes → Activate TAR-SEO-2

TAR-SEO-2 is a **one-file rewrite** of `backend/tarot_seo_data.py`:
- Removes source-derived spread prose and rigid card templates
- Record counts unchanged (100 spreads / 78 cards / 20 intentions)
- File is ready -- `py_compile` verified

**Steps:**
1. Replace `backend/tarot_seo_data.py` with the TAR-SEO-2 version
2. Commit and push to main
3. **Re-run the scanner** immediately: `python3 tests/echo_pace_tarot_scan.py`
4. Apply GAI fixes if any page type regresses to BLOCKED

---

## 7. Architecture Rules

1. **TAR-v4 is visual only** -- never modify `tarot_router.py` or `tarot_cards.json` in Tarot SEO work
2. **Punya hooks are fire-and-forget** -- never block page render on `safeClaimPunyaAction()`
3. **New SEO pages are static/programmatic** -- no AI calls, pure data-driven from `tarot_seo_data.py`
4. **`tarot_seo_data.py` is the only backend file modified by TAR-SEO-2** -- all other backend files untouched

---

## 8. QA Gap Register Items Assigned to This Thread


| Gap ID | Description | Priority |
|---|---|---|
| TAR-SEO-INT | TAR-SEO-1 local delivery not merged/deployed | 🟠 High |

---

## 9. Immediate First Actions for New Thread

1. Read `Codex_Deliveries/Tarot/TRACKER.md`
2. Read `Codex_Deliveries/Tarot/CODEX_COMMISSION_TAR_SEO_1.md`
3. Read `Codex_Deliveries/Tarot/TAR_ECHO_PACE_GAI_CONSULTATION.md` (understand the quality gate)
4. Locate the delivered TAR-SEO-1 files in the repo
5. Integrate TAR-SEO-1 (steps in Section 4) → commit and push
6. Verify 4 new SEO routes return 200 on production
7. **Run ECHO/PACE on all 4 page types** (Section 5 procedure) -- this is a blocking gate
8. GAI optimization loop if any page type fails -- repeat until all pass
9. Once all pass → activate TAR-SEO-2 (one-file swap)
10. **Run ECHO/PACE again** after TAR-SEO-2 to confirm no regression

---
*Handover prepared: 2026-05-29 by Claude Code Main Thread*
