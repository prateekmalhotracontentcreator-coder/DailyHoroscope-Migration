# Process: CD Integration Protocol
> Status: **ACTIVE** -- Issued 2026-05-29
> Issued by: Temple Team / CC Audit Session
> Applies to: All Claude Code sessions that touch Strategist (or any future CD-commissioned module)

---

## Why This Document Exists

On 2026-05-29, a full audit of the Strategist Phase 2 integration revealed three systemic failures:

1. **CC was building component approximations** (Phase2Components.jsx, strategist-phase2.css) instead of integrating CD's delivered HTML files
2. **`_assets/` folder was mistaken for the complete CD delivery** -- it is a partial assembly for the 2G canvas prototype, NOT the authoritative source
3. **CC's approximations were at ~50-60% visual fidelity** -- missing gradients, animations, entire components (Gate0Panel, ScoreboardExpanded, ContextStrip), and the full kp-panel CSS system

This document ensures these errors never repeat.

---

## 🔴 RULE 1 -- CC Never Designs or Rebuilds CD Components

**If a UI component exists in a CD-delivered HTML file, CC does NOT write, rewrite, or approximate it.**

CC's only permitted actions on CD components:
1. Extract CSS and JSX from the HTML file verbatim
2. Apply the 6-step conversion recipe (see Section 4)
3. Wire live API data in place of SEEKER demo stub
4. Run the smart-quote sanitiser

**Any visual gap, missing component, or design addition → raise with CD. Do not fill it yourself.**

---

## 🔴 RULE 2 -- HTML Files Are Always the Authoritative CSS Source

CD delivers components as standalone `.html` files. Each HTML file contains:
- A `<style>` block -- the **authoritative component CSS**
- A `<script type="text/babel">` block -- the **authoritative component JSX**

The `_assets/` folder (when it exists) is a **partial assembly** prepared for a specific canvas prototype. It is never a complete or authoritative source. Always diff before trusting.

**Hierarchy of CSS authority (highest → lowest):**
```
1. CD-delivered HTML <style> block (for that component)
2. _assets/strategist-shell.css (foundation + primitives -- updated by CD after individual files)
3. _assets/strategist-2g-surfaces.css (partial -- use only after verifying against HTML)
4. CC-written CSS -- NEVER permitted for CD components
```

---

## 🔴 RULE 3 -- Retain All CD Variants

CD builds components with A/B toggle views (Compact/Expanded, Command/Briefing, Focus/Triptych). These toggles are **permanent product features**, not canvas scaffolding.

**Never simplify, collapse, or remove a CD variant.** If a variant feels unnecessary for production, that is a Temple Team decision -- raise it, do not act on it.

---

## 🔴 RULE 4 -- Missing Components Go to CD, Not CC

If the audit reveals a component exists in an HTML file but not in `_assets/`:
- Log it as a CD action item in the Strategist TRACKER.md
- Do NOT approximate it in CC
- Flag it before integration begins so it can be bundled into a CD commission

---

## The CD Delivery Folder Structure

For the Strategist module, the canonical folder is:
```
/Users/apple/Documents/Knowledge Engine_eBooks/
  The Strategist_CD Delivery_Final_Stage 2/
  ├── Claude Design/            # Phase 1 canvas + integration notes
  │   └── strategist/           # Original canvas JSX (Babel format)
  ├── Strategist_Round2/        # R2A Visual Foundation delivery
  │   └── STR-R2-A_.../
  │       └── react/            # ✅ CD-converted ES module React files
  ├── step3/                    # Step 3 patches
  │   └── DailyHoroscope-Migration_patches/  # ✅ Drop-in repo patches
  ├── Phase 2 Commission/       # Phase 2 component deliveries
  │   ├── STR-2F · ConquestScoreboard.html    # ✅ Authoritative
  │   ├── STR-2E · LKGateSummaries.html       # ✅ Authoritative
  │   ├── STR-2C · OracleVerdictBanners.html  # ✅ Authoritative
  │   ├── STR-2D · ReentryLoop.html           # ✅ Authoritative
  │   ├── STR-2I · PrayPath.html              # ✅ Authoritative
  │   ├── STR-2G · StrategistActionPlan.html  # ✅ Authoritative (page shell)
  │   ├── STR-2B · KPGate0Panel.html          # ✅ Authoritative
  │   └── _assets/              # ⚠️ PARTIAL -- verify before using
  │       ├── strategist-shell.css        # ✅ Foundation -- use as CSS base
  │       ├── strategist-primitives.jsx   # ✅ Primitives -- use as JSX source
  │       ├── strategist-2g-modules.jsx   # ⚠️ Partial -- missing components
  │       ├── strategist-2g-surfaces.css  # ⚠️ Partial -- missing 719 CSS lines
  │       └── strategist-2g.css           # ⚠️ Partial
  └── strategist_r2b_output/    # R2B canvas output + tokens
```

---

## The 6-Step Conversion Recipe (from CD's Integration Note)

When extracting JSX from a CD HTML file and converting to ES module React:

```
Step 1 -- Add React import
  import React, { useState, useEffect } from 'react';

Step 2 -- Replace window.SEEKER / global reads with props
  // BEFORE: const s = window.SEEKER;
  // AFTER:  function Component({ score, tier, ... }) { ... }

Step 3 -- Replace Object.assign(window, ...) with ES exports
  // BEFORE: Object.assign(window, { VerdictChip, SegPill });
  // AFTER:  export { VerdictChip, SegPill };

Step 4 -- Convert static inline styles to Tailwind (where repo already uses Tailwind)
  // Pragmatic rule: static reusable styles → Tailwind
  // Dynamic per-instance values (planet tints, severity borders) → keep inline style={{}}

Step 5 -- Resolve import paths to repo conventions
  // Use @/components/strategist/... pattern

Step 6 -- Wire live API data
  // Map /api/strategist/dashboard fields → component props
  // See Section 5 for the live API → SEEKER field map
```

**Do NOT apply Step 4 to any class that appears in the CD CSS files.** Only apply Tailwind conversion to structural wrapper elements that the repo already patterns this way.

---

## Live API → SEEKER Field Map (Phase 2)

| SEEKER field | Live API source | Field path |
|---|---|---|
| `score` | `/api/strategist/dashboard` | `conquest_probability.score` |
| `max` | hardcoded | `99` |
| `tier` | `/api/strategist/dashboard` | `scoreboard.score_tier` |
| `tierBand` | derived | band from score: 75-99=emerald, 50-74=amber, 25-49=orange, 0-24=red |
| `nextThreshold` | `/api/strategist/dashboard` | `scoreboard.next_threshold` |
| `pointsToNext` | `/api/strategist/dashboard` | `scoreboard.points_to_next` |
| `nextTier` | `/api/strategist/dashboard` | `scoreboard.next_threshold_label` |
| `verdict` | `/api/strategist/dashboard` | `scoreboard.gate0_last_verdict` (lowercase) |
| `karmic` | `/api/strategist/dashboard` | `diagnosis_summary.karmic_debt_cleared` |
| `streak.days` | `/api/strategist/dashboard` | `scoreboard.streak_days` |
| `streak.tier` | `/api/strategist/dashboard` | `scoreboard.streak_tier` |
| `directive` | `/api/strategist/dashboard` | `scoreboard.score_directive` |
| `asOf` | derived | format `new Date()` as `'D MMM · HH:mm IST'` |
| `gates[]` | `/api/strategist/dashboard` | `gate_summaries` (map to gate shape) |
| `banners{}` | hardcoded per verdict | see SEEKER.banners in _assets/strategist-primitives.jsx |
| `reentry` | derived | from score + threshold + gate_summaries |
| `pray` | hardcoded | from _assets/strategist-primitives.jsx SEEKER.pray |

---

## Pre-Integration Checklist

Before writing a single line of integration code, verify all of the following:

```
[ ] 1. HTML file read -- extracted CSS and JSX to /tmp for comparison
[ ] 2. _assets/ files read -- compared against HTML for gaps
[ ] 3. Gap analysis complete -- all missing components logged in TRACKER.md
[ ] 4. Missing components flagged to CD (or confirmed as canvas-only)
[ ] 5. All CD variants identified and marked for retention
[ ] 6. Live API field map confirmed (Section 5 above)
[ ] 7. CC-written approximations deleted (Phase2Components.jsx etc.)
[ ] 8. No new CC-authored design code introduced
```

---

## What CC IS Permitted to Contribute

These are the areas where CC adds genuine value that CD does not cover:

| CC Contribution | Why CD doesn't cover it |
|---|---|
| ES module conversion (Steps 1-3 above) | CD delivers Babel/script-tag format by design |
| Live API data wiring (Step 6) | CD uses SEEKER demo stub -- no API access |
| Import path resolution | Repo-specific, CD works in standalone HTML |
| Smart quote sanitisation | Pre-commit hook, automated |
| Tracker / process doc updates | Temple Team operations |
| Raising missing components to CD | Temple Team operations |
| Backend endpoint additions/fixes | CD doesn't touch backend |

Everything else -- component structure, CSS values, visual logic, variant architecture -- belongs to CD.
