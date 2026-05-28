# Handover Guide -- Tarot Module
> Prepared by: Claude Code (Main Thread) → New Dedicated Thread
> Date: 2026-05-29
> Purpose: New thread integrates TAR-SEO-1, activates TAR-SEO-2, and owns all future Tarot work.

---

## 1. Your Role in the New Thread

You are the **Tarot thread**. Your scope is:
- Integrate TAR-SEO-1 (199-page programmatic Tarot SEO module) into production
- Activate TAR-SEO-2 (content rewrite of `tarot_seo_data.py`) once TAR-SEO-1 is live
- Handle any ECHO/PACE content quality passes on Tarot SEO pages
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

## 4. Your First Task -- Integrate TAR-SEO-1

### What TAR-SEO-1 Built (already verified, not yet in main)

TAR-SEO-1 is a **build-verified local delivery**. It was prepared by Codex without touching the interactive `/tarot` tool. Files ready to integrate:

**Backend:**
- `backend/tarot_seo_router.py` -- SEO data endpoints (spread list, card detail, intention pages)
- Wiring: must be registered in `backend/server.py` (add `include_router` call)

**Frontend -- 4 new public SEO pages:**
- `frontend/src/pages/tarot/TarotSpreadsPage.jsx` → route `/tarot/spreads`
- `frontend/src/pages/tarot/TarotSpreadPage.jsx` → route `/tarot/spread/:spreadSlug`
- `frontend/src/pages/tarot/TarotCardPage.jsx` → route `/tarot/card/:cardSlug`
- `frontend/src/pages/tarot/TarotIntentionPage.jsx` → route `/tarot/for/:intentionSlug`

**Routes:** Must be added to `frontend/src/App.js`

**Sitemap:** `frontend/public/sitemap.xml` additions for Tarot SEO routes

**Vercel cache headers:** `vercel.json` additions for Tarot SEO routes

### SEO Data Source
All SEO content is served from `backend/tarot_seo_data.py`:
- 100 spread records
- 78 card records
- 20 intention records

**Total new URLs from TAR-SEO-1:** ~198 programmatic pages + 1 hub = 199 pages

### Integration Steps
1. Check out from `Codex_Deliveries/Tarot/` for the delivered files
2. Verify `tarot_seo_router.py` is present in `backend/`
3. Add router registration to `backend/server.py`
4. Add 4 page files to `frontend/src/pages/tarot/`
5. Wire 4 routes into `frontend/src/App.js`
6. Update `frontend/public/sitemap.xml`
7. Update `vercel.json` if cache headers are included
8. Run build: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
9. Fix any smart quote issues (Codex common issue): run node smart-quote fix if build errors on curly quotes
10. Commit and push to main

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

## 5. Second Task -- Activate TAR-SEO-2 (After TAR-SEO-1 Live)

### What TAR-SEO-2 Did

TAR-SEO-2 is a **one-file rewrite** of `backend/tarot_seo_data.py`. It replaces:
- Source-derived spread prose
- Rigid card description templates
- Repetitive closings and formulaic action steps

**Record counts unchanged:** 100 spreads / 78 cards / 20 intentions

**The rewritten file is ready** -- it was prepared locally and verified with `py_compile`. Once TAR-SEO-1 is integrated and the SEO routes are live, replace `backend/tarot_seo_data.py` with the TAR-SEO-2 version.

**TAR-SEO-2 has no production effect until TAR-SEO-1 routes are live** -- the rewritten data file only matters if the SEO endpoints are serving it.

---

## 6. Content Quality -- ECHO/PACE

The `TAR_ECHO_PACE_GAI_CONSULTATION.md` and `TAR_SEO_TITLE_HUMANIZATION_LIST.md` files document:
- How to humanize Tarot SEO page titles (pre-approved list)
- ECHO/PACE content duplication thresholds for Tarot content
- GAI (Generative AI) consultation notes on keeping content below 40% duplication ceiling

After TAR-SEO-1 + TAR-SEO-2 are live, run ECHO/PACE scans on the new Tarot SEO pages via Admin Console → ECHO/PACE tab. Target: internal ECHO score ≥60, Google duplication ≤40%.

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
3. Locate the delivered TAR-SEO-1 files in the repo (check `backend/tarot_seo_router.py` and `frontend/src/pages/tarot/`)
4. Verify all 4 frontend pages exist locally
5. Integrate TAR-SEO-1 (steps in Section 4 above)
6. Run build, fix any issues, commit and push
7. Verify 4 new SEO routes return 200 on production
8. Then integrate TAR-SEO-2 (one-file swap of `tarot_seo_data.py`)
9. Run ECHO/PACE scans on live Tarot SEO pages

---
*Handover prepared: 2026-05-29 by Claude Code Main Thread*
