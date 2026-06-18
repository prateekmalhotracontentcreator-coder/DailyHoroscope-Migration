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
| 🔴 MUST READ | `Codex_Deliveries/Tarot/TAROT_FILE_MANIFEST.md` | **Complete file inventory** -- every frontend/backend/test file, its route, status, and architecture rules. Read before touching anything. |
| 🔴 MUST READ | `Codex_Deliveries/Tarot/TRACKER.md` | Live Tarot module status (v2.1) |
| 🟠 READ | `Codex_Deliveries/Tarot/TAR_ECHO_PACE_GAI_CONSULTATION.md` | ECHO/PACE content quality guidance for Tarot SEO pages |
| 🟠 READ | `Codex_Deliveries/Tarot/TAROT_V4_UI_RECONCILIATION_NOTE_2026-05-22.md` | Context on how TAR-v4 was reconciled against existing page |
| 🟡 REFERENCE | `Codex_Deliveries/Tarot/TAR_SEO_TITLE_HUMANIZATION_LIST.md` | ✅ RESOLVED -- titles humanized in TAR-SEO-2 |
| 🟡 REFERENCE | `#3_ACTION_TRACKER.md` (Tarot Thread) | Open commission actions |

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

### ✅ Phase 1 Complete -- Next Task: Issue TAR-SEO-3

ECHO/PACE is cleared. The module is QA-cleared. The next action is to issue TAR-SEO-3 to a Codex thread.

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

## 5. ECHO/PACE Quality Gate -- ✅ CLEARED 2026-05-30 (HISTORICAL)

> **This gate is fully closed.** TAR-SEO-1 + TAR-SEO-2 passed all ECHO/PACE layers under strict thresholds (L1 BLOCKED ≥60%, FLAGGED ≥40%, L2 min_docs=2, LG BLOCKED >25%, WATCH >10%). No further action needed here.

### Final Scan Results

| Page Type | L1 | L2 | L3 | LG |
|---|---|---|---|---|
| Spreads (100) | ✅ PASS -- peak 38.7% | ✅ PASS | ✅ PASS | ✅ PASS -- 0% dup |
| Cards (78) | ✅ PASS -- peak 35.0% | ✅ PASS -- 222→3 phrases | ✅ PASS | ✅ PASS -- 0% dup |
| Intentions (20) | ✅ PASS -- peak 39.5% | ✅ PASS | ✅ PASS | ✅ PASS -- 0% dup |

Layer G: **15/15 queries PASS, 0% duplication** (report: `tests/tarot_serper_detail_report.json`). Strict Serper detail script: `tests/echo_pace_tarot_serper_detail.py`.

Key fixes applied (commit `cc52900`): all 56 minor arcana given card-specific RWS imagery; health↔anxiety + spiritual-growth↔self-discovery intention pairs given unique `best_cards[:3]` and distinct prose; 4 spread pairs differentiated; `use` field varied across 18 spreads.

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

## 9. Current Active Task for Tarot Thread

> All Phase 1 work is complete. TAR-v4 ✅ · TAR-SEO-1 ✅ · TAR-SEO-2 ✅ · ECHO/PACE ✅ · Layer G ✅

**Issue TAR-SEO-3** -- 4,621 card×spread combination pages (78 cards × 60 spreads + card hub)

Brief: `Codex_Deliveries/Tarot/CODEX_COMMISSION_TAR_SEO_3_COMBINATIONS.md`

On receipt from Codex:
1. Run `python3 tests/echo_pace_tarot_scan.py` on the generated `tarot_combinations_router.py` content
2. Verify `seed_tarot_combinations.py` runs cleanly against `horoscope_db`
3. Check `TarotCombinationPage.jsx` and `TarotCardHubPage.jsx` build without errors
4. Confirm 4,621 URLs indexed in sitemap
5. Smoke test 3 representative combo URLs across card types (Major / Wands Court / Pentacles pip)

---
*Handover prepared: 2026-05-29 by Claude Code Main Thread*
