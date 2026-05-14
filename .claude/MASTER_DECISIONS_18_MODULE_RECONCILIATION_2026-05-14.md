# Master Decisions: 18-Module Reconciliation, Priorities & Web App UI/UX
> Created: 2026-05-14 | Owner: Prateek | For: Claude Code New Thread
> Status: CONFIRMED -- ready to commence build work
> This document supersedes all earlier gap analysis notes for the 18-module reconciliation.

---

## HOW TO USE THIS DOCUMENT

This is the single source of truth for the full EverydayHoroscope module reconciliation. A new Claude Code thread should:
1. Read this file in full before touching any code
2. Follow Section 1 (Process Rules) and Section 2 (Architecture Rules) absolutely -- no exceptions
3. Follow Section 3 (Web App UI/UX Principles) for every frontend commission
4. Execute modules in the Priority Order defined in Section 4
5. Use Section 5 for Adsense layout decisions on public pages
6. Use Section 6 to determine which modules need public SEO landing pages

---

## SECTION 1 -- PROCESS RULES (MANDATORY)

### 1.1 Codex-to-Temple File Workflow

**COPY, never MOVE.**

When integrating Codex-delivered files into the Temple repo:
- ✅ **DO:** Copy the file from `/Users/apple/DailyHoroscope-Codex-Test/` into `/Users/apple/DailyHoroscope-Migration/` at the correct path
- ❌ **DO NOT:** Move, rename, or delete files from the Codex-Test folder -- it is the reference archive
- ❌ **DO NOT:** Overwrite Temple files without first reading them and verifying what would be lost

**Before any file copy:**
1. Read the Temple version (`wc -l`, review imports, check what's wired)
2. Read the Codex-Test version (`wc -l`, review what's new)
3. Diff them -- understand exactly what the Codex version adds
4. Only then integrate -- and integrate additively unless a full replacement is confirmed safe

**Rationale:** The Tarot backend situation proved this -- Temple `tarot_router.py` is 857 lines, Codex-Test is 1,616 lines. The 759-line delta contains the Manifestation Journal subsystem. This was not detected until a formal diff was run. Never assume Codex-Test = Temple.

### 1.2 Every Change Must Be a Real Upgrade

- No cosmetic-only changes to working modules
- No tab additions that are empty or placeholder
- No new routes without backend endpoints that respond correctly
- No frontend components that call non-existent API endpoints
- Every PR must have: what was missing → what was added → smoke-test result

### 1.3 Smart Quote Hygiene (Standard Pre-Integration Step)

All Codex-generated files must have Unicode curly quotes sanitised before integration:
```bash
node -e "
let f=require('fs'),p='path/to/file.jsx';
let c=f.readFileSync(p,'utf8');
c=c.replace(/"/g,'\"').replace(/"/g,'\"')
   .replace(/'/g,\"'\").replace(/'/g,\"'\");
f.writeFileSync(p,c);console.log('Done');"
```
Run this on every Codex file before build verification.

### 1.4 Build Verification (Before Every Commit)

```bash
CI=true DISABLE_ESLINT_PLUGIN=true npx craco build
```
A clean build is non-negotiable before any commit to main.

### 1.5 Module Home + Common Space Packet (Before Commission Opens)

Every new Codex commission must have:
- A `MODULE_<NAME>/` folder under `/Users/apple/Documents/New project/`
- A `README.md` in that folder with module identity, file paths, current status
- A `06_RESPONSE_SUMMARY.md` under `cross-thread-audit-pack/common-space/01_FOR_INDIVIDUAL_THREADS/`
- A row in `MASTER_TRACKER.md`

---

## SECTION 2 -- ARCHITECTURE RULES (LOCKED -- DO NOT BYPASS)

### 2.1 Legacy Model Rule (Decision date: 19 April 2026)

**All live astronomical and dasha computations MUST use `vedic_calculator.py` + `pyswisseph`.**

| File | Role | Rule |
|---|---|---|
| `backend/vedic_calculator.py` | Birth chart, Mahadasha timeline, planetary positions | Single source of truth -- never replace or bypass |
| `backend/panchang_router.py` | All Panchang computations | Single source of truth |
| `backend/knowledge_engine.py` | Interpretation/rules layer only | Zero approved rules until co-founder sign-off -- additive only |
| `backend/kp_engine.py` | KP (Krishnamurti Paddhati) system | Used by Longevity -- OK to continue using for KP modules only |

**For every commission brief, state explicitly:**
- "All dasha/astronomical data must come from `vedic_calculator.py`"
- "Do NOT add dasha calculation functions to `knowledge_engine.py`"

### 2.2 Individual Reports Architecture (Confirmed -- do not change)

| Layer | System | Model |
|---|---|---|
| Chart computation | `vedic_shared_utils.py` → pyswisseph (SIDM_LAHIRI) | Internal py calculator |
| Narrative generation | `individual_reports_prompt_common.py` → Anthropic AsyncAnthropic | `claude-sonnet-4-5` (configurable via `INDIVIDUAL_REPORTS_CLAUDE_MODEL` env var) |
| KE involvement | None | Not used -- do not add |

### 2.3 Longevity Architecture (Confirmed -- do not change)

| Layer | System | Model |
|---|---|---|
| Chart computation | `kp_engine.py` → pyswisseph (SIDM_LAHIRI) | KP-specific engine |
| Narrative generation | Inline in `longevity_router.py` → Anthropic AsyncAnthropic | `claude-sonnet-4-6` |
| KE involvement | Additive annotations only via importlib | Supplementary -- not core |

### 2.4 Theme Tokens (All frontend work must use these)

| Token | Usage |
|---|---|
| `bg-background` | Page background |
| `bg-card` | Card/panel surface |
| `text-foreground` | Primary text |
| `text-muted-foreground` | Secondary text |
| `text-gold` / `border-gold` / `bg-gold` | Gold accent (#c5a059) |
| `font-cinzel` | Headings |
| `font-playfair` | Body / narrative text |

**GlassCard:** `rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-6`
**Gold tile:** `bg-gradient-to-br from-gold/15 to-gold/5`

**Color themes for zodiac/horoscope modules must be retained as-is.** The element-based color system (Fire/Earth/Air/Water) is a confirmed design decision -- do not override.

---

## SECTION 3 -- WEB APP IMMERSIVE UI/UX PRINCIPLES

### 3.1 The Principle

Every premium module's public-facing landing page and authenticated first-screen must feel like a **web application**, not a content page. Reference: The Strategist commission (`CODEX_COMMISSION_STRATEGIST_LANDING.md`).

This applies to: **Individual Reports, Arc Angel, Tarot, Palmistry, Longevity, KP/Krishna Prashnavali, Lumina** -- and any future premium module.

This does NOT apply to: Panchang and Horoscope (see Section 5 for their approach).

### 3.2 What "Web App Treatment" Means -- The 7 Principles

**1. Full-Bleed Animated Hero**
- `min-h-screen` hero, no visible page edges on load
- Animated background: `StarField` component or equivalent particle/gradient animation
- `font-cinzel` headline at 4xl-6xl, gold accent on a key word
- Sub-headline in `font-playfair` italic
- Hero must make the user feel they have entered a different space

**2. Progressive Narrated Reveal**
- Content does not dump all at once -- it unfolds in scroll-triggered sections
- Each section introduces the next concept before presenting the UI for it
- Think: "Here is what this tells you" → (reveal) → "Here is how it is calculated" → (reveal) → "Here is your result"
- Use `framer-motion` `AnimatePresence` + `motion.div` with `initial={{ opacity: 0, y: 20 }}` + `whileInView={{ opacity: 1, y: 0 }}`

**3. State Machine Feel**
- The authenticated dashboard has distinct visual states (e.g., OFFENSIVE / DEFENSIVE / GOLDEN HOUR for Strategist)
- State changes the entire color palette, not just one element
- Premium modules should have a "mode" or "phase" that the user feels they are inside

**4. Rich Data Cards**
- Numbers and computations live in GlassCard components
- Key metrics get large typography treatment (text-4xl or larger)
- Supporting data is text-sm text-muted-foreground
- Cards have subtle gold border: `border-gold/20`
- Never show raw JSON or plain lists -- everything has a visual frame

**5. Mobile-First Construction**
- Build mobile layout first, then scale up to desktop
- No horizontal scroll on any viewport
- Touch targets minimum 44×44px
- Swipeable cards/tabs on mobile preferred over click-only navigation

**6. Gold Used Precisely**
- Gold is reserved for: active states, primary CTAs, section dividers, key metric labels, the brand mark
- Do NOT use gold for body text, secondary labels, or backgrounds (except `bg-gold/[0.04]` GlassCard tint)
- Over-use of gold makes everything feel cheap -- restraint is the rule

**7. Font Hierarchy**
- H1/H2 in `font-cinzel` (display, ceremonial feel)
- H3/H4 in `font-playfair` (editorial, warm authority)
- Body text in system sans-serif or `font-playfair` for narrative
- Data/numbers in monospace or `font-cinzel` for emphasis

### 3.3 Public Landing Page Structure (Template)

Every premium module's public landing page (`/the-<module>`) follows this structure:

```
Section 1: Full-bleed animated hero -- headline, sub-headline, primary CTA
Section 2: What this module reveals -- 3-4 feature tiles (GlassCard)
Section 3: How it works -- 3-step process with icons
Section 4: Sample output teaser -- blurred/masked real output to create curiosity
Section 5: Testimonial or credibility block (Vedic tradition reference)
Section 6: Pricing/access CTA -- PremiumRoute gate summary + Register/Upgrade button
```

The landing page is public (`noindex` if there is also a `/the-<module>` at the same level -- see Section 6). The tool page (`/<module>`) is behind `ProtectedRoute` or `PremiumRoute`.

### 3.4 Auth Redirect Pattern (Confirmed -- do not deviate)

When a CTA on a public landing page should send the user to login and then back:

```jsx
// CORRECT
navigate('/login', { state: { from: { pathname: '/strategist' } } })

// WRONG -- Login.jsx does not read URL params
navigate('/login?next=/strategist')
```

Login.jsx reads `location.state?.from?.pathname` (line 30). Register.jsx and AuthCallback.jsx always redirect to `/home` -- do NOT modify these files for context-aware redirect.

---

## SECTION 4 -- MODULE PRIORITY ORDER AND ALL DECISIONS

### PHASE 0 -- Immediate Activations (Account 2, no Codex needed)
> Target: This week. These are wiring-only -- no design, no new features.

---

#### MODULE: Live TV
**Status:** Backend not wired. Frontend 100% complete (LiveTVPanel, useLiveTv, Landing mount, App.js route all confirmed present).
**Action:** 2 lines in `backend/server.py`
```python
from live_tv_router import router as live_tv_router   # add to imports
app.include_router(live_tv_router)                     # add to include_router block
```
**Decision:** Activate now with the existing placeholder asset. Do not hold for real Sai Baba Arti video -- the frontend shows a placeholder gracefully.
**Smoke test:** `/api/live-tv/...` endpoints respond + Landing panel loads without console errors.
**Done when:** Live TV panel loads on the public Landing page with no 404s.

---

#### MODULE: Punya Rewards
**Status:** All 5 files exist (`punyaRewards.js` confirmed in `frontend/src/lib/`). Zero activation wiring -- not in `server.py`, no App.js route, no AdminDashboard mount.
**Route access decision:** ✅ **ProtectedRoute** -- all logged-in users can earn and view. This is a retention feature, not a premium differentiator.
**Earn hooks decision:** ✅ Fire for all registered users (free and premium). Rewards are a funnel tool -- restricting to premium defeats the purpose.

**Activation edits:**
1. `backend/server.py` -- import `punya_rewards_router` + `app.include_router(punya_rewards_router)`
2. `frontend/src/App.js` -- add `<ProtectedRoute path="/punya-rewards">` route with `PunyaRewardsPage` or equivalent component
3. `frontend/src/pages/admin/AdminDashboard.jsx` -- mount `PunyaRewardsAdminPanel` in the admin panel

**Earn hooks (after activation confirmed):**
Add `punyaRewards.js` hook calls to: `TarotPage.jsx`, `PanchangPage.jsx`, `NumerologyPage.jsx`, `BirthChartPage.jsx`, `DailyHoroscope.jsx`, `WeeklyHoroscope.jsx`, `MonthlyHoroscope.jsx`
Wire login streak trigger in auth flow.

**Done when:** `/punya-rewards` loads for any logged-in user + Admin panel shows rewards management + earn hooks fire on each action.

---

### PHASE 1 -- Formal Commissions (Codex threads, open this week)

---

#### MODULE: Remedies Engine
**Status:** `remedies_router.py` is live and registered in `server.py` (existing LK-layer). The Module 18 full commission (KP `remedy_ref` model + `krishna_prashnavali_remedies` MongoDB collection) has not been opened.
**Decision:** Commission now. The ingest extract is ready. Do not wait for Strategist to finish.
**KP v2 bundle decision:** Keep Remedies Engine Phase 1 and KP v2 bundle update as **separate commissions**. Do not combine -- reduces risk and keeps each thread scope clean.

**Commission scope:**
1. Write `backend/scripts/ingest_krishna_prashnavali_remedies_v1.py` -- loads `KRISHNA_PRASHNAVALI_REMEDIES_INGEST_V1.json` into MongoDB collection `krishna_prashnavali_remedies`
2. Extend `remedies_router.py` with `GET /api/remedies/ref/{remedy_ref_id}` endpoint
3. Update `scriptural_oracle_router.py` to return `remedy_ref` pointers instead of hardcoded inline mantras
4. End-to-end test: KP reading → `remedy_ref` → lookup → structured remedy object returned

**Spec file:** `REMEDIES_ENGINE_SPEC_V1.md` already exists in `.claude/`

---

#### MODULE: Tarot (CRITICAL -- USP Module, Full Web App Treatment)
**Status:** Frontend `TarotPage.jsx` is identical between Temple and Codex-Test (731 lines, 3 tabs). Backend gap is significant: Temple `tarot_router.py` = 857 lines, Codex-Test = 1,616 lines. The delta (+759 lines) contains:
- Manifestation Journal: 7 new endpoints, `tarot_manifestations` MongoDB collection, task tracking, bookmarking, stats
- Gamification: `TarotGamification` model, XP + daily streak
- Moon phase data: `moon_phase` field in reading models
- Ritual notes: `ritual_note` field per spread definition
- Spread categories: oracle / relationship / career / timing / spiritual / deep / healing

**Decision:** Full Web App Immersive UI/UX treatment. Tarot is a USP module and deserves the same quality as The Strategist commission.

**Commission scope:**
1. **Backend reconciliation first:** Copy Codex-Test `tarot_router.py` (1,616 lines) into Temple, run smart-quote hygiene, verify MongoDB collection alignment (`tarot_manifestations`), verify import paths, confirm build, commit
2. **Frontend v4 commission:** Build a new Tarot experience against the expanded endpoints -- Manifestation Journal tab, gamification surface (XP/streak display), moon phase badge, ritual notes per spread
3. **Public landing page:** `/the-tarot` -- full Web App treatment with sample card animation, spread teaser, feature tiles

**Pre-commission check:** Read both `tarot_router.py` files side-by-side before writing the Codex brief. The brief must list every new endpoint with exact path, method, and request/response contract.

---

#### MODULE: Individual Reports (5 Reports) -- Full Web App Treatment
**Status:** All 5 reports are live (pyswisseph → Claude API pipeline confirmed). No onboarding experience. No public landing pages.
**Architecture confirmed:** pyswisseph (`vedic_shared_utils.py`) → `claude-sonnet-4-5` via `individual_reports_prompt_common.py`. Knowledge Engine not involved. No changes needed to backend computation.

**Decision:** Full Web App Immersive UI/UX treatment for the onboarding + report experience. Individual public landing pages for each report (better SEO than one combined page).

**5 public landing routes:**
| Report | Public Landing | Tool Route |
|---|---|---|
| Karmic Debt | `/karmic-debt-report` | `/reports/karmic-debt` |
| Career Blueprint | `/career-blueprint-report` | `/reports/career-blueprint` |
| Shadow Self | `/shadow-self-report` | `/reports/shadow-self` |
| Retrograde Survival | `/retrograde-survival-report` | `/reports/retrograde-survival` |
| Life Cycles | `/life-cycles-report` | `/reports/life-cycles` |

**Commission scope:**
1. Onboarding flow: birth details form → report generation → animated reveal of report sections
2. Public landing page for each report (or a single `/premium-reports` landing with 5 tiles)
3. Apply Section 3.3 landing page template to each
4. Report output surface: full Web App treatment -- animated section reveals, GlassCard data presentation, copy-to-clipboard for key insights
5. SEO: full `<SEO>` component on each landing page with JSON-LD schema

**Note:** The Anthropic API call is already in production -- commission focuses on UX, not backend computation.

---

#### MODULE: The Strategist
**Status:** Commission open, brief finalised in `CODEX_COMMISSION_STRATEGIST_LANDING.md`. All 4 pre-build findings resolved.
**Action:** Submit brief to Codex. No changes needed before submission.

---

### PHASE 2 -- Decisions Made, Commissions to Follow

---

#### MODULE: Arc Angel
**Status:** Panel live. 3 technical fixes confirmed. Full spec needs writing before questionnaire gating commission opens.
**Current layout confirmed by Prateek:** Left nav, 12 areas of life, 3-column layout (Favourable / Unfavourable / Confidence%), donut chart, "View full 10-year outlook" CTA.

**Confirmed tasks (Phase 2a -- technical fixes, Account 2):**
1. Fix `ArcAngelPanel.jsx` line 162: wire `isPremium` to `useAuth()` instead of hardcoded `false`
2. Add `QuestionnaireWidget` compact embed to `ArcAngelPanel.jsx` (pattern from `ArcAngelPage.jsx`)
3. **Dasha source decision:** ✅ **Leave as-is for now.** Panel calls `compute_dasha_timeline()` from `knowledge_engine.py`. Since KE internally uses `vedic_calculator.py`, it is one layer away (not a bypass). Migrate in a dedicated thread once KE co-founder sign-off is in progress.

**Phase 2b -- Questionnaire gating spec:** Must be written before a Codex commission opens. Spec will cover: which areas gate behind questionnaire completion, what the questionnaire widget shows in the panel before completion, and how confidence% is affected by questionnaire data.

**Phase 2c -- Full Web App treatment:** Arc Angel dashboard and public landing page `/the-arc-angel`. Apply Section 3.2 principles. War Room-style state machine analogous to Strategist.

---

#### MODULE: Krishna Prashnavali
**Status:** Localhost/test-host verified. Production verification pending.
**Decision:** Production smoke test as a standalone task first. Once confirmed live in production, open the v2 bundle commission as a separate thread after Remedies Engine Phase 1 is complete (dependency: `remedy_ref` endpoint must exist before v2 bundle swap).

**Sequence:** Production verify → Remedies Engine Phase 1 done → KP v2 bundle (swap to `KRISHNA_ORACLE_CONTENT_CANONICAL_V2_FOR_TEMPLE.json`, add `behavioral_remedy` + `remedy_ref` fields)

---

#### MODULE: Longevity
**Status:** Live and working. Architecture confirmed (KP engine + Claude API). `knowledge_engine` used additively.
**Decision:** Check Render production logs for `longevity_router failed to load` warning. If warning present: fix import error and remove try/except guard. If clean: confirm live status, no further action.
**Web App treatment:** Phase 2c -- public landing page `/the-longevity-report` + onboarding upgrade to match Individual Reports standard.

---

#### MODULE: Palmistry
**Status:** `PalmistryPage.jsx` has marketing copy claiming live Vedic planetary positions and dasha lord. Backend is questionnaire + AI prompt only -- no live chart data.
**Decision:** **Direction A -- Fix the copy.** Remove or soften the unsupported astrological overlay marketing claims. Do not build chart integration yet. Keep the scope lean. Phase 2 chart integration may be revisited later.
**Note:** When the copy fix is done, it should not reduce the page's appeal -- rephrase as "personalised to your Vedic birth data" (which is true -- birth date is used) rather than removing all astrology references.

---

#### MODULE: Lumina
**Status:** Temple frontend expanded beyond original spec -- extra tabs (Marketplace, Devotion, Community), premium gating, gold styling.
**Decision:** **Do not change anything until the v2 scope is understood.** Before any reconciliation work opens, produce a tab-by-tab comparison: what exists in Temple vs what was in the original brief. If the Temple additions are genuinely better (real features, real UX upgrade) → accept as v2. If they are empty tabs or placeholder surfaces → revert to original brief. No changes go in either direction without a confirmed upgrade rationale.

---

### PHASE 3 -- Review and Lighter Touch

---

#### MODULE: Numerology
**Status:** Live with 11 report CTAs and on-page SEO content. More context needed before any changes.
**Decision:** Before opening any Numerology commission, document the current state in full:
- List all 11 report CTAs by name and current access level (free / premium)
- Map the existing SEO content (which sections, which keywords)
- Confirm which reports are fully functional vs placeholder
Only after this mapping is complete should a commission brief be written. No speculative changes.

---

#### MODULE: Onboarding Questionnaire
**Two drifts from original spec confirmed:**
1. `/questionnaire` is `PremiumRoute` (original spec: free teaser)
2. `QuestionnaireWidget` is in `ArcAngelPage.jsx` not `ArcAngelPanel.jsx`

**Decision:** **Accept both drifts as-is for now.** Do not revert. The premium-only gate may be intentional product positioning. The Arc Angel embed location will be addressed in the Arc Angel Phase 2a fix (widget will be added to the panel -- not moved, added). Update `MODULE_ONBOARDING_QUESTIONNAIRE` spec to document these as accepted amendments.

---

#### MODULE: Lagna Kundali
**Status:** Phase 1 only was commissioned and delivered.
**Decision:** Review all past Temple Team KE sessions to compile Phase 2+ spec before any new commission opens. No Codex work on Lagna Kundali until the spec review is done and Phase 2 scope is formally defined.

---

#### MODULE: Love Bundle
**Status:** Confirmed clean -- backend + frontend live.
**Decision:** No action required. Monitor for any UX upgrade opportunities in Phase 3.

---

### CONFIRMED CLEAN -- No Action Required

| Module | Status |
|---|---|
| Notification Engine | Backend live, partial channel live (WhatsApp pending Meta OTP) |
| Love Bundle | Backend + frontend live |
| Panchang | Live, verified, engine v8-swiss confirmed |
| Lagna Kundali | Live, reference-build aligned, Phase 1 complete |
| Individual Reports (backend) | All 5 report routers confirmed live and working |
| Knowledge Engine | Fully wired in server.py, yoga evaluator active, migrate script present |
| Shadbala Engine | All functions confirmed in vedic_calculator.py -- NOT rolled back |

---

## SECTION 5 -- ADSENSE LAYOUT STRATEGY (Panchang + Horoscope Pages)

### 5.1 Which Pages Carry Ads

**Carry ads:** Panchang, Daily Horoscope, Weekly Horoscope, Monthly Horoscope, Landing page (cautiously)
**Never carry ads:** Any `ProtectedRoute`/`PremiumRoute` page, Admin dashboard, active tool pages (Tarot draw, Birth chart generation, any report generation in progress)

### 5.2 Layout Architecture -- "Utility Column" Model

**Desktop (≥1280px):** Three-column layout
- Left column: `w-[160px]` -- 160×600 skyscraper (sticky)
- Content: `max-w-3xl mx-auto flex-1` -- existing tool content unchanged
- Right column: `w-[300px]` -- two 300×250 MPU units stacked (sticky)

**Tablet (768-1279px):** Two-column -- drop left column, content expands, right column 300×250 remains

**Mobile (<768px):** Single column, in-content interstitials only:
- One 320×50 banner below hero
- One 300×250 MPU between content sections (mid-page)
- One 300×250 MPU above footer

### 5.3 Implementation -- Reusable Wrapper

```jsx
// PublicPageLayout.jsx -- wrapper for ad-carrying pages only
const PublicPageLayout = ({ children, showAds = true }) => (
  <div className="min-h-screen bg-background">
    <div className="max-w-screen-xl mx-auto px-4">
      <div className="flex gap-6 justify-center">
        {showAds && (
          <aside className="hidden xl:block w-[160px] flex-shrink-0 pt-24 sticky top-24 self-start">
            <AdUnit slot="left-skyscraper" size="160x600" />
          </aside>
        )}
        <main className="flex-1 min-w-0 max-w-3xl">
          {children}
        </main>
        {showAds && (
          <aside className="hidden lg:block w-[300px] flex-shrink-0 pt-24 sticky top-24 self-start space-y-4">
            <AdUnit slot="right-mpu-1" size="300x250" />
            <AdUnit slot="right-mpu-2" size="300x250" />
          </aside>
        )}
      </div>
    </div>
  </div>
);
```

### 5.4 Critical Rules
- Use **manual placement units only** -- no Adsense Auto Ads (breaks React SPA DOM)
- Do not push content below the fold with above-fold ads on mobile
- Do not insert ads mid-card or mid-section -- only between cards
- Color themes for zodiac/element-based design must be fully retained -- ads sit in the gutter, not inside themed sections

---

## SECTION 6 -- PUBLIC SEO LANDING PAGES -- WHICH MODULES NEED THEM

### Must Have (Premium modules hidden behind auth)
| Module | Public Landing Route | Tool Route | Auth Level |
|---|---|---|---|
| The Strategist | `/the-strategist` | `/strategist` | PremiumRoute |
| Arc Angel | `/the-arc-angel` | `/arc-angel` | PremiumRoute |
| Karmic Debt | `/karmic-debt-report` | `/reports/karmic-debt` | PremiumRoute |
| Career Blueprint | `/career-blueprint-report` | `/reports/career-blueprint` | PremiumRoute |
| Shadow Self | `/shadow-self-report` | `/reports/shadow-self` | PremiumRoute |
| Retrograde Survival | `/retrograde-survival-report` | `/reports/retrograde-survival` | PremiumRoute |
| Life Cycles | `/life-cycles-report` | `/reports/life-cycles` | PremiumRoute |
| Longevity | `/the-longevity-report` | `/longevity` | PremiumRoute |
| Tarot | `/the-tarot` | `/tarot` | ProtectedRoute (partial free) |
| Krishna Prashnavali | `/the-krishna-prashnavali` | `/krishna-prashnavali` | PremiumRoute |

### Valuable but Not Urgent
| Module | Landing Route |
|---|---|
| Lumina | `/the-lumina` |
| Palmistry | `/the-palmistry` |
| Numerology | `/the-numerology` |
| Punya Rewards | `/rewards-program` (explains the program) |

### No Dedicated Landing Needed
| Module | Reason |
|---|---|
| Panchang | Tool IS the public page -- fully indexed |
| Daily / Weekly / Monthly Horoscope | Same -- tool page is the SEO page |
| Lagna Kundali | Birth chart tool is publicly accessible |
| Notification Engine | Backend feature -- no search intent |
| Love Bundle | Tool page is sufficient |

### SEO Deduplication Rule
When both `/the-<module>` and `/<module>` exist:
- `/the-<module>` (public landing): `<SEO>` with full indexing, canonical URL, JSON-LD schema
- `/<module>` (authenticated tool): `<SEO noindex={true}>` to prevent duplicate content
- Remove `/<module>` from `sitemap.xml` once `/the-<module>` is live
- Add `/the-<module>` to `sitemap.xml` at priority 0.90-0.95

---

## SECTION 7 -- COMMISSION QUEUE (ORDERED)

### This Week
| # | Task | Type | Who |
|---|---|---|---|
| 1 | Live TV: 2-line server.py activation | Account 2 | Account 2 |
| 2 | Punya Rewards: 3-file activation wiring | Account 2 | Account 2 |
| 3 | Remedies Engine Phase 1: formal commission | Codex | New Codex thread |
| 4 | Tarot backend: copy + integrate Codex-Test tarot_router.py | Account 2 | Account 2 |
| 5 | The Strategist: submit brief to Codex | Codex | Submit now |
| 6 | Longevity: Render log check + smoke test | Account 2 | Account 2 |
| 7 | KP: production smoke test | Account 2 | Account 2 |
| 8 | Palmistry: copy fix (Direction A) | Account 2 | Account 2 |

### Next Sprint
| # | Task | Type |
|---|---|---|
| 9 | Individual Reports: full Web App commission (5 landings + onboarding) | Codex |
| 10 | Tarot: frontend v4 Web App commission | Codex |
| 11 | Arc Angel: Phase 2a technical fixes | Account 2 |
| 12 | Arc Angel: questionnaire gating spec (write spec first, then commission) | Codex |
| 13 | Punya Rewards: earn hooks in 7 pages + login streak | Account 2 |
| 14 | Numerology: current state mapping before commission | Research |
| 15 | Lagna Kundali: past session review + Phase 2 spec | Research |

### Pending Decisions / Held
| # | Task | Held By |
|---|---|---|
| 16 | Lumina: v2 reconciliation | Tab-by-tab audit first |
| 17 | KP v2 bundle | Remedies Engine Phase 1 must complete first |
| 18 | Arc Angel: Web App landing + full dashboard | Questionnaire spec must be written first |
| 19 | Adsense implementation | `PublicPageLayout.jsx` wrapper commission |
| 20 | Longevity: public landing page | After Render log check confirms clean |

---

## SECTION 8 -- OPEN ITEMS REQUIRING FURTHER INPUT

These items cannot proceed without additional information or Prateek decision:

| # | Item | What is needed |
|---|---|---|
| 1 | Arc Angel questionnaire gating spec | Full spec must be written before Codex commission opens -- which areas gate, what the widget shows pre-completion, how confidence% changes |
| 2 | Numerology: full current state map | List all 11 report CTAs, their access levels, and SEO content sections before any changes |
| 3 | Lagna Kundali Phase 2+ scope | Review past Temple Team KE sessions -- no commission until scope is defined |
| 4 | Lumina v2 reconciliation | Tab-by-tab audit comparing Temple vs original brief -- accept or revert decision |
| 5 | Panchang calendar / social sharing / location picker cascade | Which other modules should receive these components? (User confirmed intent but target list not defined) |
| 6 | Adsense: activate now or after design refactor? | Adsense wrapper is ready to build -- decision on timing |

---

*Document prepared: 2026-05-14*
*Based on: Temple vs Codex Audit (TEMPLE_VS_CODEX_FINDINGS_2026-05-14.md), Codex 18-Module Gap Fix Plan, Strategist commission pre-build findings, KE logic investigation, Tarot reconciliation investigation, and Prateek's confirmed decisions from session 2026-05-14.*
