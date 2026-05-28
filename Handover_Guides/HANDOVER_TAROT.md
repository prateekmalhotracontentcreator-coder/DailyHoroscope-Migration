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
1. Locate delivered files -- check `backend/tarot_seo_router.py` and `frontend/src/pages/tarot/`
2. Add router registration to `backend/server.py`
3. Wire 4 routes into `frontend/src/App.js`
4. Update `frontend/public/sitemap.xml`
5. Update `vercel.json` if cache headers are included
6. Run build: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
7. Fix any smart quote issues if needed (see Smart Quote Fix below)
8. Commit and push to main → wait for Vercel + Render deploy (~2-3 min)
9. **ECHO/PACE scan immediately** -- see Section 6 below before proceeding further
10. If ECHO/PACE passes → proceed to TAR-SEO-2
11. If ECHO/PACE fails → run GAI optimization loop (Section 6) until all page types pass, THEN TAR-SEO-2

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

### Thresholds
| Metric | Target | Fail = |
|---|---|---|
| Internal ECHO score | ≥ 60 | < 60 → humanise further |
| Google duplication rate | ≤ 40% | > 40% → GAI optimization loop |

### ECHO/PACE Scan Procedure
1. Go to `https://www.everydayhoroscope.in/admin/dashboard` → ECHO/PACE tab
2. Scan one URL from each page type:
   - Spread hub: `/tarot/spreads`
   - Spread detail: `/tarot/spread/celtic-cross` (or any slug)
   - Card detail: `/tarot/card/the-fool` (or any slug)
   - Intention page: `/tarot/for/love` (or any slug)
3. Record ECHO score + duplication % for each type
4. If all pass → proceed to TAR-SEO-2
5. If any fail → GAI optimization loop (below)

### GAI Optimization Loop (if any page type fails)
Reference: `Codex_Deliveries/Tarot/TAR_ECHO_PACE_GAI_CONSULTATION.md`

1. Identify which content fields are triggering duplication (ECHO output shows offending text)
2. Submit failing content blocks to NLM/GAI for rewrite
3. Update the relevant fields in `backend/tarot_seo_data.py`
4. Re-deploy and re-scan
5. Repeat until all 4 page types pass
6. Pre-approved humanized titles: `TAR_SEO_TITLE_HUMANIZATION_LIST.md`

### After ECHO/PACE Passes → Activate TAR-SEO-2

TAR-SEO-2 is a **one-file rewrite** of `backend/tarot_seo_data.py`:
- Removes source-derived spread prose and rigid card templates
- Record counts unchanged (100 spreads / 78 cards / 20 intentions)
- File is ready -- `py_compile` verified

**Steps:**
1. Replace `backend/tarot_seo_data.py` with the TAR-SEO-2 version
2. Commit and push to main
3. **Run ECHO/PACE again** on all 4 page types -- TAR-SEO-2 rewrites may affect scores
4. Apply GAI fixes if any page type regresses below threshold

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
