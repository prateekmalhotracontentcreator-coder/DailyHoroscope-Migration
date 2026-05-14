# Temple vs Codex -- Findings Report
> Produced: 2026-05-14 | PM Role: Account 1 Audit Thread
> Repo audited: `/Users/apple/DailyHoroscope-Migration/` (live Temple repo -- NOT Codex test folder)
> Source: 18 × `06_RESPONSE_SUMMARY.md` + live repo grep verification

---

## ⚠️ Critical Pre-Note -- Audit Reference Discrepancy

The Codex cross-thread audit was conducted against `/Users/apple/DailyHoroscope-Codex-Test/` (the Codex reference build / test snapshot), **not** the live Temple repo at `/Users/apple/DailyHoroscope-Migration/`. Account 2 (Temple Team) has been integrating code into the live repo independently. Several CRITICAL issues flagged in the pre-findings **do not exist in the live Temple repo**. All status values below reflect the **live Temple repo** state as of 2026-05-14.

---

## Section A -- Summary Dashboard

| Module | Codex Status | Temple Status | Gap | Priority |
|---|---|---|---|---|
| Notification Engine | `complete` | `partial` | `minor` | `P3` |
| Love Bundle | `complete` | `live` | `none` | `confirmed_clean` |
| Lumina | `complete` | `live` | `minor` | `P3` |
| Palmistry | `complete` | `live` | `minor` | `P3` |
| Longevity | `complete` | `integrated_not_live` | `minor` | `P2` |
| Numerology | `complete` | `live` | `minor` | `P3` |
| Onboarding Questionnaire | `complete` | `live` | `minor` | `P3` |
| Tarot | `complete` | `live` | `minor` | `P3` |
| Punya Rewards | `complete` | `partial` | `major` | `P1` |
| Krishna Prashanavali | `complete` | `integrated_not_live` | `minor` | `P2` |
| Panchang | `complete` | `live` | `none` | `confirmed_clean` |
| Arc Angel | `complete` | `live` | `minor` | `P2` |
| Individual Reports | `complete` | `live` | `none` | `confirmed_clean` |
| Live TV | `complete` | `partial` | `major` | `P1` |
| Knowledge Engine | `complete` | `live` | `minor` | `P3` |
| Lagna Kundali | `complete` | `live` | `none` | `confirmed_clean` |
| Shadbala Engine | `complete` | `live` | `none` | `confirmed_clean` ⚠️ REVERSAL |
| Remedies Engine | `not_started` | `partial` | `major` | `P1` |

---

## Section B -- Detailed Gap Analysis

### B1. Punya Rewards -- MAJOR -- P1

**What Codex delivered:**
Complete activation package: `punya_rewards_service.py`, `punya_rewards_router.py`, `PunyaRewardsPage.jsx`, `PunyaRewardsAdminPanel.jsx`, `frontend/src/lib/punyaRewards.js`

**What Temple currently has (verified 2026-05-14):**
- ✅ `backend/punya_rewards_service.py` -- present
- ✅ `backend/punya_rewards_router.py` -- present
- ✅ `frontend/src/lib/punyaRewards.js` -- **PRESENT** (confirmed via `ls frontend/src/lib/`)
- ✅ `frontend/src/pages/PunyaRewardsPage.jsx` -- present (per Codex audit)
- ✅ `frontend/src/pages/admin/PunyaRewardsAdminPanel.jsx` -- present (per Codex audit)
- ❌ `punya_rewards_router` NOT in `backend/server.py` -- grep returns 0 hits
- ❌ `/punya-rewards` route NOT in `frontend/src/App.js` -- grep confirms absent
- ❌ `PunyaRewardsAdminPanel` NOT in `AdminDashboard.jsx` -- grep confirms absent

**What is specifically missing:**
1. `server.py`: `from punya_rewards_router import router as punya_rewards_router`
2. `server.py`: `app.include_router(punya_rewards_router)`
3. `App.js`: `<Route path="/punya-rewards" element={<PremiumRoute><PunyaRewardsPage /></PremiumRoute>} />`
4. `AdminDashboard.jsx`: Mount `PunyaRewardsAdminPanel` as admin tab/section

**Recommended action:**
All source files are present -- this is purely activation wiring. One Account 2 session can close this in ~2 hours. Do NOT modify any of the existing Punya Rewards files; only add the wiring lines.

**Dependency/blocker:** None.

---

### B2. Live TV -- MAJOR -- P1

**What Codex delivered:**
`live_tv_router.py`, `live_tv_service.py`, `LiveTVPanel.jsx`, `LiveSaiBabaArtiPage.jsx`, `hooks/useLiveTv.js`

**What Temple currently has (verified 2026-05-14):**
- ✅ `backend/live_tv_router.py` -- present
- ✅ `backend/live_tv_service.py` -- present
- ✅ `frontend/src/components/LiveTVPanel.jsx` -- present
- ✅ `frontend/src/hooks/useLiveTv.js` -- present
- ✅ `frontend/src/pages/LiveSaiBabaArtiPage.jsx` -- present
- ✅ `App.js` route `/live-sai-baba-arti` -- line 123 confirmed
- ✅ `Landing.jsx` -- LiveTVPanel IS imported (line 5) and rendered (line 197)
- ❌ `live_tv_router` NOT in `backend/server.py` -- grep count = 0

**What is specifically missing:**
1. `server.py`: `from live_tv_router import router as live_tv_router`
2. `server.py`: `app.include_router(live_tv_router)`

**Recommended action:**
Two lines in `server.py`. Frontend is 100% complete. Account 2 can close in under 30 minutes.

**Dependency/blocker:** Final real video asset still pending (separate Prateek action). Register the router now -- the panel degrades gracefully without the asset.

---

### B3. Remedies Engine -- MAJOR -- P1 (Prateek Decision Required)

**What Codex delivered (formal commission):**
Nothing runtime -- formal Codex Remedies Engine commission has NOT been opened. Pre-commission documentation only: `REMEDIES_ENGINE_SPEC_V1.md`, `CODEX_GREEN_LIGHT_MEMO.md`.

**What Temple currently has (verified 2026-05-14):**
- ✅ `backend/remedies_router.py` -- **A functional remedies router IS live**
  - server.py line 62: `from remedies_router import router as remedies_router`
  - server.py line 2086: `app.include_router(remedies_router)`
  - Routes at `/api/remedies/*`
  - Queries MongoDB collections (interpretation docs, LK rules, KP rules) via `_query_interpretation_docs`, `_query_lk_docs`, `_query_kp_docs`
- ✅ `App.js` route `/remedies` → `<RemedyPage />`

**What is specifically missing vs formal Codex Remedies Engine spec:**
1. `krishna_prashnavali_remedies` MongoDB collection -- not created
2. `remedy_ref` pointer schema -- KP module cannot yet reference remedies by ID
3. `behavioral_remedy` field -- approved 2026-05-11, not yet in router
4. `remedy_type: "ritual" | "behavioral"` distinction -- not in router
5. Cross-module `remedy_ref` lookups for Tarot/Numerology/Strategist

**Recommended action:**
Commission Codex to build the formal Remedies Engine per `REMEDIES_ENGINE_SPEC_V1.md`. The Temple Team's existing router is a working interim but does not fulfill the KP v2 bundle contract (which requires `remedy_ref` pointers). See Section C3 for work assignment draft.

**Dependency/blocker:** KP v2 bundle contract swap is blocked on this. Strategist surrogate bridge also assumes `remedy_ref` schema. Recommend opening the Codex commission immediately after Prateek confirms E1.

---

### B4. Shadbala Engine -- ⚠️ PRE-AUDIT CRITICAL REVERSAL

**Pre-audit finding:** "Rolled back in Temple; repo copy errors on `_solar_event_jd()`; dignity/combustion functions missing" -- CRITICAL.

**Live Temple repo verification (2026-05-14):**
```
grep result on /Users/apple/DailyHoroscope-Migration/backend/vedic_calculator.py:
  Line 93:   # Planetary dignity tables
  Line 165:  def get_planet_dignity(...) ✅
  Line 193:  def is_planet_combust(...) ✅
  Line 786:  def calculate_shadbala(...) ✅
  Lines 1094-1102: Called inside calculate_vedic_chart() ✅
```

**Conclusion:** All Shadbala functions present and wired in the live Temple repo. The rollback described in the Codex audit affected `DailyHoroscope-Codex-Test` (the Codex reference snapshot), not the live Temple repo. Account 2 has correctly maintained the Shadbala integration. **Status: CONFIRMED CLEAN. No action required.**

---

### B5. Knowledge Engine -- ⚠️ PRE-AUDIT CRITICAL REVERSAL

**Pre-audit finding:** "`knowledge_engine.py` runtime wiring missing; `migrate_ch41_varga_checkable.py` absent" -- CRITICAL.

**Live Temple repo verification (2026-05-14):**
- server.py line 88: `from knowledge_engine import (...)` ✅
- server.py line 2167: `configure_default_knowledge_engine(db)` at startup ✅
- `knowledge_engine.py` Phase 2 wiring: `ChartFacts`, `_populate_varga_dignity_facts()`, `ke_yoga_evaluator` import (line 635) ✅
- `backend/scripts/migrate_ch41_varga_checkable.py` -- PRESENT ✅
- `knowledge_router` registered in server.py line 2082 ✅

**Conclusion:** Both critical gaps from pre-audit are resolved in the live Temple repo. **Status: CONFIRMED LIVE -- downgraded to P3 operational note.**

**Remaining P3 operational note:** KE rules are gated by `approval_status = "approved"`. Zero approved rules currently = KE provides no live output. This is by design (co-founder approval gate), not a code defect. Timeline for first rule batch approval is decision E8.

---

## Section C -- Work Assignment Drafts

### C1. Punya Rewards Activation -- Account 2 -- ~2 hours

Open a new Account 2 session with this brief:

> Activate the Punya Rewards module in the live Temple repo at `/Users/apple/DailyHoroscope-Migration/`. All delivery files are already present and complete. This is wiring-only -- do not modify any existing Punya Rewards files.
>
> **File 1 -- `backend/server.py`**: Add `from punya_rewards_router import router as punya_rewards_router` near line 100 (alongside other router imports). Add `app.include_router(punya_rewards_router)` near line 2085 (alongside other `include_router` calls).
>
> **File 2 -- `frontend/src/App.js`**: Add `const PunyaRewardsPage = lazy(() => import('./pages/PunyaRewardsPage'));` in the lazy import section. Add route `<Route path="/punya-rewards" element={<PremiumRoute feature="Punya Rewards"><PunyaRewardsPage /></PremiumRoute>} />` alongside other premium routes.
>
> **File 3 -- `frontend/src/pages/admin/AdminDashboard.jsx`**: Import `PunyaRewardsAdminPanel` from `./PunyaRewardsAdminPanel` and add it as a tab (suggested tab name: "Rewards"). Follow the existing tab pattern in AdminDashboard.
>
> Verify CI build passes. Confirm `/punya-rewards` route loads for premium user. Confirm `/api/punya-rewards/` responds. Commit.

---

### C2. Live TV Backend Registration -- Account 2 -- ~30 minutes (same session as C1)

> In `backend/server.py` add:
> Line ~100: `from live_tv_router import router as live_tv_router`
> Line ~2085: `app.include_router(live_tv_router)`
>
> Nothing else. The frontend is 100% complete. Verify build. Commit.

---

### C3. Remedies Engine Codex Commission -- Codex -- 1-2 threads (after Prateek approves E1)

> Commission Codex to extend the existing remedies system into the formal Remedies Engine.
>
> **Spec files:** `REMEDIES_ENGINE_SPEC_V1.md`, `CODEX_GREEN_LIGHT_MEMO.md`, `MODULE_REMEDIES_ENGINE/KRISHNA_ORACLE_REMEDY_ENGINE_SCHEMA.md`, `MODULE_REMEDIES_ENGINE/KRISHNA_PRASHNAVALI_REMEDIES_INGEST_V1.json`
>
> **What to build:**
> 1. Extend `backend/remedies_router.py` to add `GET /api/remedies/by-ref/{remedy_ref_id}` -- lookup a single remedy by its `remedy_ref` ID from the `krishna_prashnavali_remedies` collection
> 2. Create MongoDB ingest script for `KRISHNA_PRASHNAVALI_REMEDIES_INGEST_V1.json` → `krishna_prashnavali_remedies` collection
> 3. Add `behavioral_remedy` field support to the router response model
> 4. Add `remedy_type: "ritual" | "behavioral"` field to returned documents
>
> **Architecture guardrail (MANDATORY):** Remedies Engine must never recompute astrology. All live chart data comes from `vedic_calculator.py`. KP answer/verdict fields must never be overridden.
>
> **Definition of done:** `GET /api/remedies/by-ref/<id>` resolves from `krishna_prashnavali_remedies` collection; ingest script runs cleanly; `behavioral_remedy` field present in responses.

---

### C4. Krishna Prashanavali Bundle Swap -- Account 2 -- ~3 hours (after C3)

> Prerequisites: Remedies Engine (C3) must be live. Then:
>
> 1. Update `backend/scriptural_oracle_router.py` to support `remedy_ref` field -- when a KP slot has `remedy_ref`, call `GET /api/remedies/by-ref/{id}` instead of returning inline `remedy`/`mantra`
> 2. Replace `assets/krishna_oracle/krishna_oracle_content.json` with the approved v2 bundle at `MODULE_KRISHNA_PRASHANAVALI/KRISHNA_ORACLE_CONTENT_CANONICAL_V2_FOR_TEMPLE.json`
> 3. Verify 7 approved editorial sample slots (slots 1, 11, 19, 27, 31, 33, 36) display correctly
> 4. Confirm `krishna_answer` is unique per slot (not repeat of `title`)
>
> Definition of done: KrishnaOraclePage loads v2 bundle; PRAY/YES/WAIT/NO verdicts display correctly; remedy lookups resolve via Remedies Engine; no inline hardcoded mantra strings.

---

### C5. Arc Angel Panel Amendment + Dasha Fix -- Account 2 -- ~2 hours

> Three targeted fixes in the live Temple repo:
>
> **Fix 1 -- `frontend/src/components/ArcAngelPanel.jsx`**: Add `QuestionnaireWidget` compact embed (currently only in `ArcAngelPage.jsx`). Follow the existing QuestionnaireWidget pattern from `QuestionnairePage.jsx`. Place after the guidance strip.
>
> **Fix 2 -- `frontend/src/components/ArcAngelPanel.jsx`**: Replace `const isPremium = false` with actual premium status from `useAuth()` hook. Pattern: `const { user } = useAuth(); const isPremium = user?.subscription_status === 'premium';`
>
> **Fix 3 -- `backend/knowledge_engine.py`**: The Arc Angel windows endpoint (`/api/knowledge-engine/arc-angel-windows` in `server.py`) currently calls `compute_dasha_timeline()` from `knowledge_engine.py`. Per the CLAUDE.md Legacy Model architectural rule, this MUST come from `vedic_calculator.calculate_vimshottari_dasha()`. Replace the internal compute call with an import from `vedic_calculator`.
>
> Definition of done: Panel shows questionnaire for premium users; panel columns are premium-locked correctly; Arc Angel dasha data sourced from `vedic_calculator`.

---

## Section D -- Modules Confirmed Clean

| Module | Verification |
|---|---|
| **Love Bundle** | 8 Love routers + Ritual Engine all in server.py; `/love`, `/love-reports`, `/ritual-engine` in App.js; Temple-confirmed live |
| **Panchang** | `panchang_router` registered; v17 engine confirmed; all 6 tabs live |
| **Individual Reports** | All 5 report routers + kundali_router registered; `/reports`, `/individual-reports`, `/lagna-kundali` routes present; premium-gated correctly |
| **Lagna Kundali** | `kundali_router` registered; KE Phase 2B1 Dasa Varga amendment (ENABLED_CHARTS dict) confirmed in router; PremiumRoute-gated |
| **Shadbala Engine** | `get_planet_dignity` (line 165), `is_planet_combust` (line 193), `calculate_shadbala` (line 786) all present in `vedic_calculator.py`; called in `calculate_vedic_chart()` lines 1094-1102. **REVERSAL from CRITICAL -- confirmed live.** |

---

## Section E -- Decisions Required from Prateek

### E1. Remedies Engine -- Commission Codex Now or Defer?
**Context:** Temple Team has a working `remedies_router.py` (live). Formal Codex Remedies Engine spec adds `krishna_prashnavali_remedies` collection + `remedy_ref` schema + `behavioral_remedy` field. KP v2 bundle requires `remedy_ref`. Strategist surrogate bridge assumes this schema.
**Options:** (a) Commission Codex now, (b) Defer to Phase 2 with current Temple implementation as interim.
**PM Recommendation:** Commission now -- KP editorial approvals from 2026-05-11 depend on it.

### E2. Lumina -- Accept Temple UX Amendments or Revert?
**Context:** Original spec was 6-tab dark-indigo. Temple build has 9-tab gold/card with Marketplace, Devotion, Community tabs + reward tracking.
**Options:** (a) Accept as v2 scope, (b) Revert to original spec, (c) Hybrid -- keep structure, remove unsupported tabs.

### E3. Palmistry -- Unsupported Astrology-Overlay Copy
**Context:** `PalmistryPage.jsx` claims "reading incorporates live Vedic planetary positions, current dasha lord, transit influences." The palmistry router does not actually do this.
**Options:** (a) Remove/rewrite the copy, (b) Wire palmistry to `vedic_calculator` to make the claim true (Phase 2 scope), (c) Leave as aspirational.

### E4. Onboarding Questionnaire -- Free Teaser vs Premium-Only
**Context:** Original spec: free-teaser capable (free users see questions, locked on results). Temple: fully `PremiumRoute` -- free users see nothing.
**Options:** (a) Accept Premium-only as product decision, (b) Restore free-teaser intent.

### E5. Tarot -- v4 Full Frontend or Current Slim Version?
**Context:** Current Temple `TarotPage.jsx` = remediation-era slim 4-tab version. Fuller v4 frontend exists in Codex builds but not integrated.
**Options:** (a) Steady state with current version, (b) Commission v4 frontend promotion as new scope.

### E6. Longevity -- Contract Reconciliation
**Context:** `longevity_router.py` endpoint surface differs from `CONTRACT_COMMISSION_H.md` API spec. Guarded import in `server.py` (works but non-standard). Runtime not verified.
**Options:** (a) Accept current implementation as the new canonical baseline, (b) Reconcile to contract.

### E7. Arc Angel -- Persistence Decision
**Context:** Should `UserArcAngelProfileDocument` results be saved per user in MongoDB? Separate from the dasha fix (which should be done regardless -- it's a CLAUDE.md architectural violation).
**Options:** (a) Persist Arc Angel window results, (b) Stateless only (re-compute on each call).

### E8. Knowledge Engine -- Rule Promotion Schedule
**Context:** KE is live and wired in production. Zero approved rules currently = no live output. Co-founder approval gate is the only remaining step.
**Decision needed:** Schedule the first co-founder rule review session.

---

## Appendix -- Exact Repo Commands That Drove This Report

```bash
# punyaRewards.js confirmed present
ls /Users/apple/DailyHoroscope-Migration/frontend/src/lib/
# → punyaRewards.js, utils.js

# LiveTVPanel + useLiveTv confirmed present
ls /Users/apple/DailyHoroscope-Migration/frontend/src/components/ | grep LiveTV
# → LiveTVPanel.jsx
ls /Users/apple/DailyHoroscope-Migration/frontend/src/hooks/
# → useLiveTv.js present

# live_tv_router NOT in server.py
grep -c "live_tv" /Users/apple/DailyHoroscope-Migration/backend/server.py
# → 0

# punya_rewards NOT in server.py
grep -n "punya" /Users/apple/DailyHoroscope-Migration/backend/server.py
# → 0 results

# Landing.jsx mounts LiveTVPanel
grep -n "LiveTV" /Users/apple/DailyHoroscope-Migration/frontend/src/pages/Landing.jsx
# → line 5 import, line 197 render

# Shadbala functions confirmed in vedic_calculator.py
grep -n "get_planet_dignity\|is_planet_combust\|calculate_shadbala" /Users/apple/DailyHoroscope-Migration/backend/vedic_calculator.py
# → lines 165, 193, 786 ✅

# knowledge_engine startup wiring confirmed
grep -n "configure_default_knowledge_engine" /Users/apple/DailyHoroscope-Migration/backend/server.py
# → lines 96, 1963, 2007, 2167 ✅

# migrate_ch41_varga_checkable.py confirmed present
ls /Users/apple/DailyHoroscope-Migration/backend/scripts/ | grep "ch41"
# → migrate_ch41_varga_checkable.py, ingest_bphs_ch41_v1.py ✅

# remedies_router confirmed live
grep -n "remedies_router" /Users/apple/DailyHoroscope-Migration/backend/server.py
# → line 62 import, line 2086 include_router ✅
```
