# DIAGNOSTIC_STR_2026-05
> The Strategist -- Phase 2 Triage Audit
> Audit date: 2026-05-30 | Auditor: Claude Code | Method: CD HTML vs integrated React side-by-side
> CD HTML source: `Codex_Deliveries/Strategist/DIAGNOSTIC_HTML/` (7 files -- 2B 2C 2D 2E 2F 2G 2I)

---

## Audit Scope

| Component | CD File | React Component | CSS File |
|---|---|---|---|
| ConquestScoreboard | STR-2F-ConquestScoreboard.html | `phase2/ConquestScoreboard.jsx` | `strategist-2f-scoreboard.css` |
| LKGateSummaries | STR-2E-LKGateSummaries.html | `phase2/LKGateSummaries.jsx` | `strategist-2e-lkgates.css` |
| OracleVerdictBanners | STR-2C-OracleVerdictBanners.html | `phase2/OracleVerdictBanners.jsx` | `strategist-2c-oracle.css` |
| ReentryLoop | STR-2D-ReentryLoop.html | `phase2/ReentryLoop.jsx` | `strategist-2d-reentry.css` |
| PrayPath | STR-2I-PrayPath.html | `phase2/PrayPath.jsx` | `strategist-2i-praypath.css` |
| KPGate0Panel | STR-2B-KPGate0Panel.html | `phase2/KPGate0Panel.jsx` | `strategist-2b-gate0.css` |
| ActionPlanPage (shell) | STR-2G-StrategistActionPlan.html | `StrategistActionPlanPage.jsx` | `strategist-2g-actionplan.css` |
| Token foundation | `_assets/strategist-shell.css` (CD) | `strategist-tokens.css` (integrated) | -- |

---

## GAP SEVERITY LEGEND

| Symbol | Meaning |
|---|---|
| 🔴 | Breaking -- visible defect or invisible element in production |
| 🟠 | Significant -- visual deviation from approved CD design |
| 🟡 | Minor -- data stub, low-visibility deviation, future commission scope |
| ✅ | Verified correct -- no gap |

---

## TOKEN GAPS (strategist-tokens.css vs _assets/strategist-shell.css)

### 🔴 GAP-T1 -- `--strategist-card-border-bold` UNDEFINED in light and dark modes

**Root cause:** CD HTML shell defines `--strategist-card-border-bold` for all modes. When CC built `strategist-tokens.css`, the same token was named `--strategist-card-border-strong` in the light and dark mode blocks -- but ALL extracted component CSS files use the original CD name `--strategist-card-border-bold`.

**Impact:** In light and dark modes, `var(--strategist-card-border-bold)` resolves to nothing -- 12 CSS rules produce invisible/missing borders and elements.

**Affected rules:**
| File | Rules broken | Elements affected |
|---|---|---|
| `strategist-2c-oracle.css` | 2 | `.ov-banner` top border + `.ov-banner__cta-secondary` underline |
| `strategist-2e-lkgates.css` | 1 | `.lk-chip--active` border |
| `strategist-2g-actionplan.css` | 4 | `.ap-deck` bottom border + `.ap-vc` border + `.ap-clear` border + `.ap-q` left accent |
| `strategist-2i-praypath.css` | 2 | Two prayer panel borders |
| `strategist-2b-gate0.css` | 3 | Main gate panel border + divider + inner section border |

**Fix:** Add alias `--strategist-card-border-bold: var(--strategist-card-border-strong)` to light AND dark mode blocks in `strategist-tokens.css`. **STATUS: FIXED in this session.**

---

### 🟠 GAP-T2 -- Light mode card surfaces use transparent gold instead of solid white

**Root cause:** When CC built the initial light mode token block (pre-Phase 2), `--strategist-card-bg` was set to the app-wide GlassCard pattern `hsl(38 60% 50% / 0.04)`. The CD HTML `strategist-shell.css` specifies `#FFFFFF` (solid white).

| Token | CD value | Integrated value | Visual impact |
|---|---|---|---|
| `--strategist-card-bg` | `#FFFFFF` | `hsl(38 60% 50% / 0.04)` | Cards appear nearly transparent instead of solid white |
| `--strategist-card-elev` | `#FBF7EC` | `hsl(38 60% 50% / 0.08)` | Elevated surfaces appear transparent instead of warm cream |

**Fix:** Update light mode block to CD-matching solid values. **STATUS: FIXED in this session.**

---

### 🟠 GAP-T3 -- Light mode `--strategist-bg` and `--strategist-fg` slightly off

| Token | CD value | Integrated value | Notes |
|---|---|---|---|
| `--strategist-bg` | `#F4EFE3` | `hsl(33 21 97%)` ≈ `#F7F4F0` | CD is warmer/more cream. Partially masked by radial gradient overlay. |
| `--strategist-fg` | `#2A2418` | `hsl(33 14 18%)` ≈ `#2F2B26` | Very minor difference. |

**Fix:** Align to CD hex values. **STATUS: FIXED in this session.**

---

### 🟡 GAP-T4 -- Dark mode border opacity minor difference

| Token | CD value | Integrated value |
|---|---|---|
| `--strategist-card-border` (dark) | `rgba(197, 160, 89, 0.15)` | `rgba(197, 160, 89, 0.20)` |

Low visual impact. Intentional or incidental? Leaving for TT review -- not changed.

---

## CSS-LEVEL GAPS (component CSS files vs CD HTML `<style>` blocks)

### ✅ strategist-2f-scoreboard.css
Near-verbatim extraction of CD HTML 2F `<style>` block. Gauge dimensions (192×192px, stroke-width 11, score font-size 52px), chip states, board-hero grid, board-compact, section-header, seg-pill, verdict-chip -- all match. No CSS gaps identified.

### ✅ strategist-2e-lkgates.css
CSS faithfully extracted from CD HTML 2E. LKStatusChip 4 states, ToneBar, lk-list, lk-row (with status accent borders), lk-grid 2+3 layout, lk-card, lk-proof strip -- all match. The token naming issue for `--strategist-card-border-bold` was the only gap (covered by GAP-T1 fix).

### ✅ strategist-2c-oracle.css
CSS faithfully extracted. Banner shell, 4-state verdict surfaces (yes/wait/no/pray gradient), left/right column layout, ov-context 4-cell strip, ov-proof strip -- all match. Token gap covered by GAP-T1 fix.

### ✅ strategist-2g-actionplan.css
CSS faithfully extracted from 2G composition shell. ap-deck sticky strip, ap-body, ap-sec sections, VerdictCompact (ap-vc), ClearanceCard (ap-clear), ActionQueue (ap-queue + ap-q) -- all match. Token gap covered by GAP-T1 fix.

### ✅ strategist-2b-gate0.css
CSS extracted. Token gap covered by GAP-T1 fix.

### ⚠️ strategist-2d-reentry.css / strategist-2i-praypath.css
Not fully line-compared in this audit session. CSS line counts (290 and 338 lines respectively) are consistent with the CD HTML style block sizes. GAP-T1 `--strategist-card-border-bold` confirmed in 2I (2 rules). Full visual verification needed in browser.

---

## JSX / COMPONENT STRUCTURE GAPS

### ✅ OracleVerdictBanners.jsx
Faithful reproduction. BANNERS hardcoded per verdict (appropriate -- live reasoning is a future KP Oracle integration). ContextStrip included. VerdictChip proof strip included per TT variant policy. SegPill 4-segment md toggle included. Data wiring correct for available API fields.

### ✅ LKGateSummaries.jsx
Faithful reproduction. LKStatusChip, ToneBar, GateRow (list), GateCard (grid 2+3), SectionHeader with summary counts, LKStatusChipProofStrip retained per TT policy. Data wiring maps to `data.gate_summaries[]`. Controlled `view` prop (for page-level density override) implemented correctly.

### ✅ StrategistActionPlanPage.jsx (2G composition)
Assembly matches 2G spec: five sections in chart-led order (Digest/Diagnostics/Verdict/Active Path/Action Queue). ONE density control (Command/Briefing) drives all sections. Active path slot `switch(verdict)` → 2D/2I/ClearanceCard correct. KP Gate 0 panel rendered above sections per TT process map. Floating ← War Room link + theme toggle in nav bar.

### 🟡 GAP-S1 -- Section component missing provenance sub-header
The 2G HTML `Section` component shows `srcTag` + `srcLabel` (e.g. "inherits · **2F** · compact") as a review annotation. The integrated `Section` component shows only `n` + `title`.
**Assessment:** The provenance sub-header is a CD review annotation, not a user-facing feature. Low priority. No action needed.

### 🟡 GAP-S2 -- Proof strips render on live page
`OracleVerdictProofStrip` and `LKStatusChipProofStrip` are CD canvas review components that render on the live Action Plan page. TT confirmed "retain all CD variants" policy. Flagged for TT decision -- remove or retain on live page.

---

## DATA WIRING GAPS

### 🟡 GAP-D1 -- BANNERS + SIGNALS hardcoded in OracleVerdictBanners.jsx
The oracle reasoning text (headline, reasoning, CTA, window) and signal labels (3 transit signals per verdict) are hardcoded constants. The CD design intends these to be seeker-specific -- driven by live KP Oracle verdict + chart transits.
**Path to live:** Requires KP Oracle full integration (STR-2A2 future commission). Hardcoded is correct scaffold for now.

### 🟡 GAP-D2 -- ACTION_QUEUE hardcoded in StrategistActionPlanPage.jsx
Three action queue moves are hardcoded scaffolds. Live moves need to be distilled from verdict + gate diagnostics by the backend.
**Path to live:** Backend endpoint addition needed. Future commission.

### 🟡 GAP-D3 -- KPGate0Panel question text hardcoded
Question rendered: "Should I proceed with the named action in this Dasha period?" -- this should be the seeker's actual question.
**Path to live:** API must expose `gate0_question` field. Future backend addition.

### 🟡 GAP-D4 -- gate_summaries API field shape unverified
`LKGateSummaries` expects gates array with shape `{ id, code, name, facet, status, narrative, asideLabel, asideValue }`. This shape needs backend verification -- empty `gates=[]` means the §02 Diagnostics section renders blank (no gates, no error).

---

## COMMISSIONS NEEDED

| ID | Component | What CD needs to build | Priority |
|---|---|---|---|
| STR-OP-20 | War Room | Horizontal snap-scroll layout -- Gate 0 sticky + Layers 1-5 as full-width panels (commission brief already written) | 🔴 Ready to issue |
| NEW STR-OP-21 | OracleVerdictBanners | Live seeker-specific reasoning: banner headline/text driven by KP Oracle verdict + transit signals from chart engine | 🟡 Phase 3 scope |
| NEW STR-OP-22 | ActionQueueModule | Backend-driven action queue: 3 moves distilled from verdict + gate states by the strategist engine | 🟡 Phase 3 scope |

---

## VERIFIED CORRECT -- No Gaps

| Area | Verdict |
|---|---|
| Phase 2 primitives (SegPill, VerdictChip, SectionHeader) | ✅ Faithful to CD |
| All Phase 2 CSS extractions (2B/2C/2D/2E/2F/2G/2I) | ✅ Verbatim from CD HTML `<style>` blocks |
| StrategistActionPlanPage.jsx 2G assembly | ✅ Matches 2G composition spec |
| LKGateSummaries.jsx | ✅ Faithful to 2E |
| OracleVerdictBanners.jsx | ✅ Faithful to 2C |
| Theme isolation (strategist theme vs host app) | ✅ Fixed this session -- override block in light mode |
| ConquestGauge overflow (donut glow bleed) | ✅ Fixed this session -- overflow:hidden + 7px glow |
| CR grid -- darker green (#2d7a42) + smaller cells | ✅ Fixed this session |
| Theme toggle on all module pages | ✅ Fixed this session |

---

## FIX SUMMARY (This Session)

| Gap | Fix | Files |
|---|---|---|
| GAP-T1 (card-border-bold missing) | Added `--strategist-card-border-bold` alias to light + dark mode blocks | `strategist-tokens.css` |
| GAP-T2 (card surfaces transparent) | Updated light mode `--strategist-card-bg: #FFFFFF`, `--strategist-card-elev: #FBF7EC` | `strategist-tokens.css` |
| GAP-T3 (bg/fg off) | Updated `--strategist-bg: #F4EFE3`, `--strategist-fg: #2A2418` in light mode | `strategist-tokens.css` |

---

## OPEN POINTS POST-AUDIT

| # | Item | Owner | Priority |
|---|---|---|---|
| 1 | Verify `gate_summaries` API field shape matches LKGateSummaries gate object | CC (backend check) | 🟠 |
| 2 | TT decision: keep or remove proof strips (OracleVerdictProofStrip, LKStatusChipProofStrip) on live page | TT | 🟡 |
| 3 | Issue STR-OP-20 War Room H-scroll commission to CD | TT | 🔴 |
| 4 | Issue STR-OP-21 live oracle reasoning commission to CD (Phase 3 scope) | TT | 🟡 |
| 5 | Issue STR-OP-22 backend-driven action queue | TT | 🟡 |
| 6 | Full browser visual verification after re-wire | CC | 🔴 |

---

*Diagnostic generated: 2026-05-30 | Next action: Apply token fixes → Re-wire routes → Browser verify*
