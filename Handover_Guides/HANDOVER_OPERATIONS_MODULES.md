# Handover Guide -- Operations Modules Thread
> Prepared by: Claude Code (Main Thread) → New Dedicated Thread
> Date: 2026-05-29
> Purpose: New thread owns all Codex commissions with considerable work remaining, excluding KE, SEO 20K, Book Decode, Tarot, and Strategist/LK.

---

## 1. Your Role in the New Thread

You are the **Operations Modules thread**. You own the completion, verification, and new commissions for all app modules listed in this guide.

**Modules assigned to you:**
KP Oracle · Kundali · Longevity · Punya Rewards · Self-Healing Center (SHC) · Lumina · Lo Shu Grid · Angel Numbers · Numerology · Individual Reports · Remedies Engine · Live TV · Palmistry · Panchang Language Pages · World Oracles (parking lot)

**You do NOT own:**
- Knowledge Engine (KE), Book Decode/Ingest -- main PM thread
- SEO 20K pages -- main PM thread
- Tarot -- dedicated Tarot thread
- Strategist + Lal Kitab -- dedicated Strategist/LK thread
- Play Store / Razorpay / admin panel buildout -- main PM thread (product management)

---

## 2. Essential Reference Files -- Read First

| File | What it Contains |
|---|---|
| `CLAUDE.md` (repo root) | Project identity, infrastructure, theme tokens, commit protocol |
| `#4_ROADMAP.md` | Active commission plan, issue order, TT integration actions |
| `#5_CODEX_COMMISSION_TABLE.md` | Master commission table -- all modules, status, brief paths, gap register |
| `#3_ACTION_TRACKER.md` | Open action items (M-15 onward most relevant) |
| `Codex_Deliveries/CODEX_QA_INTEGRATION_AUDIT_2026-05-27.md` | Full QA audit -- source of all gap register items |
| `Codex_Deliveries/INDEX.md` | Index of all commission brief folders |

---

## 3. Module Status -- At a Glance

| Module | Status | Next Action |
|---|---|---|
| KP Oracle | ⚠️ TRACKER UPDATE NEEDED (see Section 4) | TT acceptance verification |
| Kundali | 🟣 READY TO ISSUE (KUN-1) | Issue to Codex now |
| Longevity | 🟡 PARTIAL -- performance gap | Fix 46s latency |
| Punya Rewards | 🟡 PARTIAL -- missing action code | Fix PUN-OP-1 |
| Self-Healing Center | 🟡 PARTIAL -- env vars + admin UI | SHC-OPS-1 Render env vars |
| Lumina | 🟡 PARTIAL -- write-path + spec drift | TT scope confirmation |
| Lo Shu Grid | 🟠 LOCAL DELIVERY -- not integrated | TT integrate from `Codex_Deliveries/Lo_Shu_Grid/` |
| Angel Numbers | 🟡 PARTIAL -- Mongo stale | Run re-seed scripts |
| Numerology | 🟡 PARTIAL -- payload + CTA drift | Codex fix or CC fix |
| Individual Reports | 🟡 PARTIAL -- IR-5 smoke pending | TT smoke test |
| Remedies Engine | 🟡 PARTIAL -- 0 approved records | TT record approval |
| Live TV | 🟡 PARTIAL -- scope + HTTP fixes | Remove from Panchang, fix http:// |
| Palmistry | ✅ LIVE -- content drift only | Minor: fix birth data claim copy |
| Panchang Language Pages | 🟣 READY TO ISSUE (PAN-L1) | Issue to Codex (independent) |
| World Oracles | ⏸ PARKING LOT | Phase 3 -- do not touch |

---

## 4. MODULE: KP Oracle -- PRIORITY: HIGH

> **⚠️ TRACKER DISCREPANCY:** KP TRACKER.md (v2.1) shows KP-Sprint2 ✅ INTEGRATED (`20d4d29`) and KP-2B ✅ INTEGRATED (`20f7b83`). The master commission table is stale. Update the commission table when you start.

### What is Live
| Commission | Commit | What It Delivered |
|---|---|---|
| KP-2A | `7d42880` | Bundle editorial + share card + remedies admin frontend |
| KP-Sprint2 | `20d4d29` | `/ask-question` -- AskQuestionPage.jsx (514 lines), 60-route logic router JSON (20 SATTVA/RAJAS/TAMAS), ask endpoint in `scriptural_oracle_router.py` |
| KP-2B | `20f7b83` | Ritual animation + 3-pillar UX + astro-filter -- `KrishnaRitualScreen.jsx`, 3-pillar `KrishnaOraclePage.jsx` (799 lines), astro enrichment route |

### Key Files
- `frontend/src/pages/kp/KrishnaOraclePage.jsx` -- main page
- `frontend/src/pages/kp/AskQuestionPage.jsx` -- /ask-question page
- `backend/scriptural_oracle_router.py` -- all KP endpoints
- `backend/remedies_router.py` -- remedies endpoints
- `Codex_Deliveries/KP/TRACKER.md` -- full tracker with all open points

### Open Action Items (TT)
| ID | Action | Priority |
|---|---|---|
| KP-OP-12 | Acceptance verify KP-Sprint2 on production: `/ask-question` loads, 20 focus areas, Guna shows (SATTVA/RAJAS/TAMAS), 3-card reveal, free quota 2/month enforced, readings persist | 🟠 HIGH |
| KP-OP-13 | Acceptance verify KP-2B on production: ritual screen fires on first visit, skips on return, orb animates, 3 pillars visible, Verdict badge colour-coded, Cosmic Context shows Mahadasha+Antardasha | 🟠 HIGH |
| KP-OP-10 | Share card visual format needs redesign -- current `KrishnaShareCard.jsx` gold dark theme needs review | 🟠 HIGH |
| KP-OP-11 | Report structure UX review -- two-column grid layout needs TT sign-off | 🟠 HIGH |

---

## 5. MODULE: Kundali -- PRIORITY: ISSUE NOW

### Status: 🟣 READY TO ISSUE

The **backend is fully live** at `/api/lagna-kundali`. Frontend is the only missing piece.

**Brief:** `Codex_Deliveries/Kundali/CODEX_COMMISSION_KUNDALI_LAGNA_CONTRACT.md`

**What KUN-1 builds (frontend only):**
- `KundaliPage.jsx` -- birth details form + SVG chart + planet table + dasha timeline
- North Indian diamond-style SVG chart (rendered via flatlib + house-planet mapping)
- Dasha timeline component (uses `vedic_calculator.py` data already returned by backend)

**Architecture rule:** All dasha/astronomical data from `vedic_calculator.py` via the existing backend route. Do NOT add calculation logic to the frontend.

**No blockers** -- issue this commission immediately.

---

## 6. MODULE: Longevity -- PRIORITY: HIGH

**Brief:** `Codex_Deliveries/Longevity/CODEX_COMMISSION_LONGEVITY_REPORT_CONTRACT.md`

### Current State
- Page live at `/longevity-report`
- Preview generation works but takes **~46 seconds** (target: <10s)
- Save/history/detail path not fully verified

### Open Gaps
| ID | Gap | Action |
|---|---|---|
| LON-OP-2 | 46s response time for `/api/longevity/generate` | Profile the endpoint -- likely Claude API call is synchronous and blocking. Implement streaming response or async generation with polling pattern. |
| LON-OP-1 | Save/history/detail path not verified | TT to test: generate report → verify it appears in history → click detail view → confirm full report loads |

---

## 7. MODULE: Punya Rewards -- PRIORITY: MEDIUM

**Brief:** `Codex_Deliveries/Punya_Rewards/CODEX_COMMISSION_PUN_2_FRONTEND_INTEGRATION.md`

### Current State
- Home promo + SVG wheel + cross-module Punya hooks live
- Authenticated ledger/spin and admin tab smoke tests not done

### Open Gap
| ID | Gap | Action |
|---|---|---|
| PUN-OP-1 | `individual_report` action code missing from backend | When a user generates an Individual Report, no Punya points are awarded. Add `individual_report` action code to the Punya backend action handler. CC fix -- check `backend/punya_router.py` and add the action mapping. |

---

## 8. MODULE: Self-Healing Center (SHC) -- PRIORITY: HIGH

**Tracker:** `Codex_Deliveries/Self_Healing_Center/` (check for TRACKER.md)

### Current State
- SHC-1 backend + telemetry hooks live
- SHC-2 Razorpay lifecycle ledger + webhook live
- SHC-3 backend routes deployed
- `DiagnosticsTab.jsx` IS wired into `AdminDashboard.jsx` (confirmed 2026-05-29, import line 25, render line 742) -- TT verify "Self-Heal" tab visible at `/admin/dashboard`

### Open Gaps
| ID | Gap | Action |
|---|---|---|
| SHC-UI-1 | Verify "Self-Heal" tab visible at `/admin/dashboard` | TT to check current Vercel deploy. If missing, investigate `AdminDashboard.jsx` lazy-load or build issue. |
| SHC-OPS-1 | 5 Render env vars for Gmail/GST + OAuth | TT to set in Render dashboard: `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`, `SUPPORT_EMAIL`, `BUSINESS_STATE` -- then run Gmail OAuth flow |

---

## 9. MODULE: Lumina -- PRIORITY: MEDIUM

### Current State
- Backend AI/read routes live
- Frontend live at `/lumina` -- 9-tab gold variant (vs original 6-tab dark-indigo Phase 1 spec)
- Write-path (prayers, manifestation completion) not fully smoke-tested

### Open Gaps
| ID | Gap | Action |
|---|---|---|
| LUM-OP-1 | 9-tab gold frontend vs original 6-tab Phase 1 contract -- spec drift | TT to confirm: is the 9-tab gold UI the accepted v2 scope, or does it need to revert? Once confirmed, close this gap. |
| Write-path smoke | Prayers + manifestation completion endpoints | TT to test: submit a prayer → verify persistence; complete a manifestation → verify status update. If routes fail, flag for CC fix. |

---

## 10. MODULE: Lo Shu Grid -- PRIORITY: HIGH

### Status: 🟠 LOCAL DELIVERY -- Not yet integrated

Delivered locally. Build-verified. Not merged to `main`.

**Delivered files (check `Codex_Deliveries/Lo_Shu_Grid/`):**
- Backend router (Lo Shu Grid calculation)
- 4 public frontend pages
- Seed script for Mongo
- `sitemap.xml` additions
- `vercel.json` additions

### Integration Steps (TT)
1. Copy backend router file to `backend/` and register in `server.py`
2. Copy 4 frontend page files to `frontend/src/pages/`
3. Add routes to `frontend/src/App.js`
4. Update `sitemap.xml` and `vercel.json`
5. Run build: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
6. Commit and push → wait for deploy
7. Run seed script on Render if Mongo collections need seeding
8. **ECHO/PACE scan immediately after deploy** (blocking gate -- see Section 20 for procedure)
   - Scan 1 URL from each of the 4 public page types
   - Target: internal ECHO ≥60, Google duplication ≤40%
   - If fails: GAI optimization loop on the content fields → re-seed → re-scan
   - Only declare LSG-1 complete once all page types pass

---

## 11. MODULE: Angel Numbers -- PRIORITY: HIGH

### Current State
- Routes live at `/angel-numbers/111` and `/angel-numbers/111/love`
- API returns 200 but serves **pre-ANGEL-2 Mongo content** -- old generic closing sentences and action steps
- ANGEL-2 code is in repo but Mongo collections are stale (not re-seeded)

### Action Required (TT)
Run the re-seed scripts on Render. Seeds are at:
- `backend/seed_angel_numbers_core.py`
- `backend/seed_angel_numbers_intents.py`

Run via Render shell or schedule as one-off task. This will replace stale Mongo docs with the ANGEL-2 quality content.

---

## 12. MODULE: Numerology -- PRIORITY: MEDIUM

**Brief:** `Codex_Deliveries/` -- check for Numerology folder

### Current State
- `/numerology` live, 11 tiles + Premium Ankjyotish present
- `/numerology/report/test` live

### Open Gaps
| ID | Gap | Action |
|---|---|---|
| NUM-OP-1 | Backend missing `remedy_card`, `supportive_gems`, `supportive_metals`, `remediation_plan` payload fields vs Codex delivery contract | CC or Codex fix: add missing fields to `backend/numerology_router.py` response payload |
| NUM-OP-2 | `NumerologyPage.jsx` uses generic Brihat-Kundali CTA instead of tile-aware CTA map | CC fix: implement tile-aware CTA routing in `NumerologyPage.jsx` |

---

## 13. MODULE: Individual Reports -- PRIORITY: MEDIUM

### Current State -- Mostly ✅ LIVE

| Commission | Status |
|---|---|
| IR-1 (5 SEO landing pages) | ✅ INTEGRATED `825a294` |
| IR-2 (Lunar Cycle Wellness backend) | ✅ INTEGRATED `f9f6690` |
| IR-3 (8 Love Report SEO landing pages) | ✅ INTEGRATED |
| IR-4 (6 Phase 3 Natal Reports) | ✅ INTEGRATED |
| IR-5 (12 Areas of Life Enhancement) | ✅ INTEGRATED but full panel smoke with real data pending |

### Open Gap
| ID | Gap | Action |
|---|---|---|
| IR-5 smoke | `/api/reports/enhanced-analysis` returns 400 on empty payload (correct) but full smoke with real birth data not done | TT to test: submit real birth details to `/api/reports/enhanced-analysis` with a valid `analysis_type` parameter -- verify 200 response with structured output |

---

## 14. MODULE: Remedies Engine -- PRIORITY: HIGH

**Brief:** `Codex_Deliveries/Remedies/CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md`

### Current State
- `/api/remedies/ref/` endpoint live
- `krishna_prashnavali_remedies` collection seeded (36 records)
- BUT: 0 KP records have `approval_status = approved`

### Open Gaps
| ID | Gap | Action |
|---|---|---|
| REM-OP-1 | `/api/remedies/ref/` fails -- 0 approved KP records | TT to review and approve KP remedy records in Admin Console → Remedies tab, or run approval script on Render |
| REM-OP-2 | `/api/remedies/suggest` returns empty for public input | Investigate: does the suggest endpoint require an approved record? If so, fix REM-OP-1 first. If a separate bug, debug `remedies_router.py` suggest logic. |
| REM-REC-1 | Verdict split is 10/8/8/10 (YES/WAIT/NO/PRAY) vs spec'd 9/9/9/9 | TT to confirm if intentional or if re-ingest is needed. |

---

## 15. MODULE: Live TV -- PRIORITY: HIGH

### Open Gaps
| ID | Gap | Action |
|---|---|---|
| LTV-SCOPE-1 | `LiveTVPanel` component mounted on Panchang + Home pages -- original spec was home page only | Remove `LiveTVPanel` mount from `frontend/src/pages/PanchangPage.jsx`. Re-test `/panchang` routes. Keep on Home (`/`). |
| LTV-HTTP-1 | Backend emits `http://` media stream URLs -- mixed-content risk on HTTPS production site | Find `http://` URL construction in `backend/live_tv_router.py` or equivalent, change to `https://`. May need CDN/proxy for actual stream delivery if source is HTTP-only. |

---

## 16. MODULE: Palmistry -- PRIORITY: LOW

### Current State: ✅ LIVE

Backend + frontend at `/palmistry`. Full analysis + history working.

### Open Gap (Minor)
| ID | Gap | Action |
|---|---|---|
| PALM-OP-1 | Frontend copy says birth data is used; backend does not collect or use birth data | Update frontend copy in `PalmistryPage.jsx` to remove the birth data claim, OR add birth data collection to backend. TT to decide which path. |

---

## 17. MODULE: Panchang Language Pages -- PRIORITY: LOW

### Status: 🟣 READY TO ISSUE -- Independent, no blockers

**Brief:** `Codex_Deliveries/Panchang/CODEX_COMMISSION_PANCHANG_LANGUAGE_PAGES.md`

**What PAN-L1 builds:** Tamil, Telugu, and Malayalam language/regional Panchang pages -- programmatic pages using existing Panchang backend with translated UI labels.

Issue this commission any time. It is fully independent of all other modules.

**⚠️ ECHO/PACE gate applies after integration:** Language/regional pages are content-heavy and localized -- run ECHO/PACE scan on at least one page per language (Tamil, Telugu, Malayalam) immediately after deploy. Target: internal ECHO ≥60, Google duplication ≤40%. If any language variant fails, apply GAI optimization before declaring the module complete.

---

## 18. MODULE: World Oracles -- PARKING LOT

**Status:** ⏸ Phase 3 -- do NOT build yet.

**Brief:** `Codex_Deliveries/World_Oracles/CODEX_COMMISSION_ORACLE_P3_WORLD_ORACLES.md`

**Scope:** 5 World Oracle Modules (Bible, Islamic, Taoist, Greek, Sikh)

**Gate:** Issue only after KP Oracle has been live for 30+ days and Phase 2 is stable.

---

## 19. QA Gap Register -- Your Full Responsibility

From `Codex_Deliveries/CODEX_QA_INTEGRATION_AUDIT_2026-05-27.md`:

| # | Gap ID | Module | Description | Priority | Owner |
|---|---|---|---|---|---|
| 1 | LON-OP-2 | Longevity | Preview ~46s (target <10s) | 🟠 High | TT + CC |
| 2 | LON-OP-1 | Longevity | Save/history/detail path not verified | 🔶 Med | TT |
| 5 | REM-OP-1 | Remedies | `/api/remedies/ref/` fails -- 0 approved KP records | 🟠 High | TT |
| 6 | REM-OP-2 | Remedies | `/api/remedies/suggest` returns empty | 🟠 High | TT + CC |
| 7 | ANGEL-OP-1 | Angel Numbers | ANGEL-2 in repo; Mongo not re-seeded | 🟠 High | TT |
| 9 | LTV-SCOPE-1 | Live TV | `LiveTVPanel` on Panchang + Home -- scope drift | 🟠 High | TT |
| 10 | LTV-HTTP-1 | Live TV | Backend emits `http://` -- mixed content | 🟠 High | TT + CC |
| 12 | SHC-UI-1 | SHC | `DiagnosticsTab.jsx` wired -- TT verify tab visible | 🟡 Med | TT |
| 13 | SHC-OPS-1 | SHC | Gmail/GST -- 5 Render env vars + OAuth | 🟠 High | TT |
| 15 | PUN-OP-1 | Punya | `individual_report` action code missing | 🔶 Med | TT + CC |
| 16 | REM-REC-1 | Remedies | Verdict split 10/8/8/10 vs spec 9/9/9/9 | 🔶 Med | TT |
| 18 | PALM-OP-1 | Palmistry | Frontend says birth data used; backend doesn't collect | 🔶 Med | TT + Codex |
| 19 | LUM-OP-1 | Lumina | 9-tab gold vs 6-tab Phase 1 spec -- drift | 🔶 Med | TT |
| 20 | NUM-OP-1 | Numerology | Missing `remedy_card`, `supportive_gems`, `remediation_plan` vs contract | 🔶 Med | TT + Codex |

---

## 20. ECHO/PACE Gate -- General Procedure

> Applies to any module with **public programmatic/SEO content pages**: LSG-1, PAN-L1, and any future content modules.
> ECHO/PACE runs AFTER deploy but BEFORE the module is declared complete.

### Thresholds
| Metric | Target | Action if Fail |
|---|---|---|
| Internal ECHO score | ≥ 60 | Humanise content fields, redeploy, rescan |
| Google duplication rate | ≤ 40% | GAI optimization loop (can take multiple rounds) |

### Scan Procedure
1. Deploy module to production
2. Go to `/admin/dashboard` → ECHO/PACE tab
3. Scan 1 representative URL per page type
4. If all pass → module complete
5. If any fail → identify offending content fields from ECHO output → send to NLM/GAI for rewrite → update data files → redeploy → rescan
6. Precedent: M3 festival-region pages required 9 rounds to clear the 40% ceiling

---

## 21. Recommended Work Order

### Week 1 -- Quick Wins and Blockers

1. **Commission table already updated** -- KP-Sprint2 and KP-2B corrected to ✅ INTEGRATED (`20d4d29` + `20f7b83`) by main thread 2026-05-29
2. **Lo Shu Grid (LSG-1)** -- Integrate → deploy → ECHO/PACE scan → fix if needed (TT, 60-90 min total)
3. **Angel Numbers re-seed** -- Run `seed_angel_numbers_core.py` + `seed_angel_numbers_intents.py` on Render (TT, 10 min)
4. **KP acceptance** -- Verify KP-Sprint2 (KP-OP-12) + KP-2B (KP-OP-13) on production
5. **Live TV scope** -- Remove `LiveTVPanel` from Panchang page (LTV-SCOPE-1, CC fix, 15 min)
6. **Kundali (KUN-1)** -- Issue to Codex immediately (no blockers)

### Week 2 -- Completions

7. **SHC-OPS-1** -- Configure 5 Render env vars for Gmail/GST (TT action)
8. **Remedies approval** -- TT approves KP records to fix REM-OP-1/2
9. **Longevity latency** -- Profile LON-OP-2 (46s → <10s), implement fix
10. **Numerology fixes** -- Fix NUM-OP-1 (missing payload fields) + NUM-OP-2 (CTA drift)

### When Kundali and other threads are running

11. **Panchang Language Pages (PAN-L1)** -- Issue to Codex → integrate → ECHO/PACE scan (1 page per language)
12. **Lumina scope confirm** -- TT signs off on 9-tab vs 6-tab scope

---

## 21. Architecture Rules (Mandatory for All Modules)

1. **All dasha/astronomical data** from `backend/vedic_calculator.py` + `pyswisseph` ONLY
2. **Never add dasha calculation functions** to any router or `knowledge_engine.py`
3. **Knowledge Engine** is interpretation layer only -- never for live computation
4. **Existing MongoDB collections** -- do NOT create new collections without explicit need; route to existing ones first
5. **Temple Theme tokens:** `bg-background`, `bg-card`, `text-foreground`, `text-gold` (`#c5a059`), `border-gold`, `bg-gold`
6. **GlassCard pattern:** `rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`
7. **Build verification always:** `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` before committing
8. **Commit format:** `feat(scope):`, `fix(scope):`, `chore(scope):`

---

## 22. Infrastructure Quick Reference

| Layer | Platform | Deploy |
|---|---|---|
| Frontend | Vercel | `git push main` (~2 min) |
| Backend | Render (Docker) | `git push main` (~3 min) |
| Database | MongoDB (Motor) | Env: `MONGO_URL`, `DB_NAME` |
| Payments | Razorpay | Env: `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET` |

**Backend entry point:** `backend/server.py` -- all routers registered here  
**Frontend entry point:** `frontend/src/App.js` -- all routes here  
**Live URL:** https://www.everydayhoroscope.in  
**Backend API:** https://everydayhoroscope-api.onrender.com

---
*Handover prepared: 2026-05-29 by Claude Code Main Thread*
