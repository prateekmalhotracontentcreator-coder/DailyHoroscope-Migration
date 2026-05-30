# CD Commission: STR-UM-01 · The Strategist -- User Manual Guide
> Issued: 2026-05-31 | Status: 🔵 READY TO SEND TO CD
> Module: The Strategist | Surface: `/strategist/manual` (new dedicated page)
> Brief author: Temple Team | Design authority: CD

---

## 1. Purpose

The Strategist is a multi-screen, multi-layer module. New users arrive at the Landing Page, then flow through a Snapshot Dashboard and into a 5-Layer War Room -- with an Action Plan, Missions, Executive Brief, Surrogate Bridge, and Report accessible from there.

Without a guide, the learning curve is steep. The commission is to design and deliver a **visually rich, standalone User Manual** that lives inside the module. The manual explains:

- What The Strategist is and what problem it solves
- The complete navigation flow across all screens
- Each screen and what it shows
- Each layer, gate, and section -- what to read, what to do, when to act

The manual must look like a **war room intelligence brief** -- not a help page. Every screen should feel like it belongs to the Temple App aesthetic. Gold type, dark backgrounds, Cinzel headings.

---

## 2. Navigation Architecture (What the Manual Must Explain)

The complete user journey, in order:

```
① Landing Page         /strategist
        ↓  "Enter the War Room" CTA
② War Room Overview    /strategist/snapshot          ← Phase 1 Snapshot Dashboard
        ↓  "Enter Full War Room →" CTA
③ Full War Room        /strategist/war-room          ← 5-Layer Deep-Dive
        ↓  Layer pill navigation (L0 → L5)
④ Action Plan          /strategist/action-plan       ← Phase 2 Diagnostics + Verdict
⑤ Missions             /strategist/missions
⑥ Executive Brief      /strategist/executive
⑦ Surrogate Bridge     /strategist/surrogate
⑧ Report               /strategist/report
```

Each screen must have its own section in the manual with:
- **Screen name** + route
- **What this screen shows** (1-2 sentences)
- **How to navigate in/out**
- **Key actions available**

---

## 3. Screens Catalogue

### Screen ①  -- The Strategist Landing Page

- **Route:** `/strategist`
- **Who sees it:** All users (public page, no auth required)
- **What it shows:** Module introduction -- the problem it solves, the six intelligence layers, how KP Oracle and Lal Kitab work together, FAQs
- **Key CTA:** "Enter the War Room" -- takes logged-in users to the Snapshot, routes guests to login first

---

### Screen ②  -- War Room Overview (Snapshot Dashboard)

- **Route:** `/strategist/snapshot`
- **Auth required:** Yes (Premium)
- **What it shows:** A quick-glance operational read of the seeker's current strategic state. Five Phase 1 panels:

| Panel | What it shows |
|---|---|
| Conquest Score Gauge | The live score (0-99) with band label |
| Factor Table | The KP + LK factors driving the score |
| Mission Board | Active missions -- module/orbit/tactical variants |
| Dasha Timeline | Current Mahadasha + Antardasha with elapsed/remaining |
| Pitru-Rin Ledger | Ancestral debt rows or cleared state |
| Golden Hour Strip | Offensive / Golden / Defensive windows with live countdown |

- **Navigation:**
  - `← The Strategist` → back to Landing
  - `War Room · Overview` breadcrumb (current location indicator)
  - `Enter Full War Room →` → proceeds to Screen ③

---

### Screen ③  -- Full War Room (5-Layer Deep-Dive)

- **Route:** `/strategist/war-room`
- **Auth required:** Yes (Premium)
- **What it shows:** The complete six-layer strategic intelligence system. The hero section shows the War State (Offensive Gold / Golden Hour / Defensive Midnight) and live countdown. A sticky layer-pill navigation bar (L0-L5) lets the seeker jump between layers.

---

## 4. The Six Layers -- Detailed Breakdown

This is the core of the manual. Each layer must get a full section in the design.

---

### Layer 0 -- Gate 0: Krishna Prashnavali Oracle

**Tagline:** *Ask Krishna before any campaign. One verdict determines the day's route into the War Room.*

**What it is:**
Gate 0 is the entry clearance check. Before any mission can run, the seeker asks Krishna one question -- a free-form career intent. The response comes as one of four verdicts: YES, WAIT, NO, or PRAY.

**How to use it:**
1. The 9×9 oracle grid appears (81 cells)
2. The seeker focuses on their career question
3. They tap one cell -- one pick only
4. The verdict is returned instantly

**The four verdicts:**

| Verdict | Meaning | What happens next |
|---|---|---|
| ✅ YES | Path is clear. Move. | War Room fully unlocked. All layers active. |
| ⏳ WAIT | Hold. The window does not favor. | Pre-Flight Mode. LK Tracker work priority. |
| 🛑 NO | Conditions deny. Do not proceed. | Conquest Score must reach 60% before re-test. |
| 🙏 PRAY | The answer is not in action. Offer. | Full Surrender Path. Mantra + debt work first. |

**Gate status persists for 24 hours.** The seeker does not need to re-consult within the same day.

---

### Layer 1 -- Astrology Engine

**Tagline:** *Birth-chart timing, command planet, and dasha weather form your strategic operating system.*

**What it shows:**
- **Mahadasha:** The ruling 7-20 year planetary period. Sets the macro strategy.
- **Antardasha:** The ruling sub-period within the Mahadasha. Sets the micro tone.
- **Command Planet:** The planet that governs the current Dasha. Determines which remedies activate and which surrogates are needed.
- **Current Dasha Weather:** A plain-language summary of what the planetary period means for career action.

**How to read it:**
The Dasha Timeline bar shows elapsed vs. remaining time in each period. The Command Planet tag shows which planet is in command -- all remedy prescriptions flow from this.

---

### Layer 2 -- Lal Kitab 5-Gate Diagnosis

**Tagline:** *Debt, dormant houses, Mercury collisions, and geographic alignment stay visible in one strip.*

**What it shows:**
Five diagnostic gates from Lal Kitab (the planetary remedy system):

| Gate | Facet | What it scans |
|---|---|---|
| G01 | Karmic Debt (Pitru Rin) | Ancestral debt active / cleared |
| G02 | Sleeping Houses | Dormant planetary houses blocking energy |
| G03 | Year Cycle | Current annual lord and its implications |
| G04 | Mercury Scan | Communication + intellect blockers |
| G05 | Geographical | Power direction -- which direction amplifies effort |

Each gate shows a **status chip**: `Clear` (emerald) · `Active` (gold) · `Warning` (amber) · `Dormant` (red).

**ToneBar:** A compact 5-tick summary at the top of the section shows all five gate states at a glance.

---

### Layer 3 -- Strategist Engine + Missions

**Tagline:** *Mission triggers, hurdle alerts, and surrogate pivots surface only when the path is ready.*

**What it shows:**
Active missions generated by the Strategist Engine based on the seeker's birth chart, current Dasha, and KP sub-lord readings. Each mission represents a specific strategic action window.

**Mission anatomy:**

| Field | Description |
|---|---|
| Mission ID | e.g. `M-01` |
| Title | The strategic action |
| Command Planet | Which planet this mission operates under |
| KP Sub-Lord | The KP House Sub-Lord that unlocked this mission |
| Hurdle | Any active blockers (shown as HurdleAlert) |
| 9-Parameter Score | Rating across 9 strategic parameters |
| Status | Active / Pending / Complete / Blocked |

**Three display variants:**
- **Module** -- grouped by module (career, finance, relationships, etc.)
- **Orbit** -- grouped by Command Planet
- **Tactical** -- priority order by urgency

**Hurdle Alerts:**
Red/amber warning banners that surface when a mission has an active blocker. Each hurdle names the blocker, explains it, and gives a pivot recommendation.

---

### Layer 4 -- 43-Day Remedy Roadmap (Action Plan)

**Tagline:** *Your streak, debt clearance, and next threshold become an execution board instead of static data.*

**What it shows:**
The full Phase 2 Action Plan page (`/strategist/action-plan`) is accessible from Layer 4. This is the seeker's daily execution board -- five sections:

| Section | What it contains |
|---|---|
| § Daily Digest | Dasha weather summary + today's strategic posture |
| § LK Gate Diagnostics | Live gate status -- list or grid view |
| § Oracle Verdict | The active YES/WAIT/NO/PRAY banner with validity window |
| § Active Path | The path prescribed by the current verdict (Re-entry Loop or Pray Path) |
| § Action Queue | Upcoming ritual + remedy actions by date |

**Conquest Scoreboard:**
At the heart of Layer 4 is the Scoreboard -- the live conquest score, streak, tier, karmic debt status, and progress bar toward the next threshold. This is the number that determines whether Gate 0 verdicts can advance.

**Score bands:**

| Band | Range | Strategic stance |
|---|---|---|
| Sovereign Dominance | 85-99% | Expansion / All-In |
| Operational Friction | 60-84% | Patch & Pivot |
| Strategic Siege | 40-59% | Hold Ground / Remedy |
| Karmic Lockdown | 0-39% | Withdraw / Full Reset |

---

### Layer 5 -- Executive Intelligence Brief

**Tagline:** *A premium output layer for the user who wants the whole battle plan in one polished brief.*

**What it shows:**
The Executive Brief (`/strategist/executive`) is the module's output layer -- a polished, printable summary of the seeker's complete strategic state:
- War Room state summary
- Current Dasha interpretation
- Gate 0 verdict + validity
- Active missions
- Conquest score trend
- Immediate action recommendations

This is designed for seekers who want to save or share their strategic brief.

---

## 5. Supporting Screens

### Surrogate Bridge  `/strategist/surrogate`

Many Lal Kitab remedies require action involving a **Command Planet relative** (e.g., father, elder brother, maternal uncle). When that relative is absent, the Surrogate Bridge maps the remedy to an available substitute -- preserving the karmic vector.

The Surrogate Bridge shows:
- The required Command Planet + its natural relative
- Why the original relative is unavailable (absent, deceased, estranged)
- The mapped surrogate option
- The exact remedy re-stated for the surrogate

---

### Missions Board  `/strategist/missions`

The full Mission Board view -- all active, pending, and completed missions in one place. Sortable by module, orbit, or tactical priority. Each mission expandable to show the full 9-parameter breakdown.

---

### Report  `/strategist/report`

The downloadable/shareable version of the Executive Brief. Formatted for screen or PDF-export.

---

## 6. Key Concepts Glossary

The manual must include a Glossary section. Every term defined in plain language.

| Term | Definition |
|---|---|
| Gate 0 | The KP Oracle entry clearance. Must be passed before missions unlock. |
| Conquest Score | 0-99 index of strategic readiness. Computed from KP, LK, Dasha, and ritual streak. |
| Mahadasha | 7-20 year ruling planetary period from Vimshottari Dasha system. The macro timeline. |
| Antardasha | Sub-period within the Mahadasha. The micro tone. |
| Command Planet | The planet ruling the current Dasha. All remedies and missions flow from this. |
| Pitru Rin | Ancestral karmic debt. Surfaced by Lal Kitab Gate 1. Blocks career progress until cleared. |
| KP Sub-Lord | KP Astrology's house signification layer. Determines mission unlocks. |
| Lal Kitab | Ancient Urdu planetary remedy system. The 5-Gate diagnostic layer of The Strategist. |
| Hurdle | An active blocker on a mission. Named, explained, with a pivot recommendation. |
| Surrogate | A substitute for the Command Planet relative when the original is unavailable. |
| Golden Hour | The 30-minute window before sunset. The highest-energy offensive action window. |
| Offensive Window | The daytime action window before Golden Hour. Full campaign mode. |
| Defensive Window | Post-sunset. Night protocol -- hold, no offensive actions. |
| War State | The current temporal state: `OFFENSIVE_GOLD`, `GOLDEN_HOUR`, or `DEFENSIVE_MIDNIGHT`. |
| Streak | Consecutive days of ritual completion. Compounds Conquest Score. |
| Score Tier | Named band for the Conquest Score level: Sovereign / Friction / Siege / Lockdown. |
| Gate Status | Lal Kitab gate health: Clear / Active / Warning / Dormant. |
| Verdict | Gate 0 Oracle output: YES / WAIT / NO / PRAY. |

---

## 7. Design Direction

### Visual Identity
- **Background:** Dark -- same `var(--strategist-bg)` as the War Room
- **Type:** Cinzel for headings, Playfair Italic for narrative, mono for codes/labels
- **Accent:** Gold (`--strategist-gold`) throughout
- **Cards:** GlassCard style -- `rgba(197,160,89,0.04)` background, gold/20 border
- **Section dividers:** Thin gold line (`rgba(197,160,89,0.12)`)

### Layout
- **Desktop:** Two-column sidebar navigation + main content area
  - Left sidebar: numbered section list (clickable, sticky while scrolling)
  - Right main: section content
- **Mobile:** Single column, section list collapses to a dropdown nav
- **Section numbering:** `01`, `02`, `03`... in small gold mono caps above each heading

### Section Structure (CD to follow)
Each section should have:
1. **Section chip** -- small gold/mono `SECTION 01` label
2. **Heading** -- Cinzel, large
3. **Sub-heading / tagline** -- Playfair italic
4. **Body copy** -- readable at 16-17px, generous line-height (1.7-1.8)
5. **Diagrams / anatomy cards** (where relevant) -- gold-bordered cards showing field labels
6. **Status chip / verdict colour samples** (where relevant) -- inline visual examples

### Tone
Military intelligence manual. Concise. No fluff. Every sentence either defines something or tells the user what to do. The seeker has limited time -- the manual must respect that.

---

## 8. Deliverable Spec

| # | Deliverable | Format |
|---|---|---|
| 1 | Standalone HTML file: `str-user-manual.html` | Self-contained · all CSS inline / `<style>` |
| 2 | All sections as listed in §3-§6 | Complete -- no sections marked TODO |
| 3 | Desktop layout (sidebar + content) | Visible at ≥ 1024px |
| 4 | Mobile layout (stacked, dropdown nav) | Visible at < 768px |
| 5 | 4 theme variants supported | `data-mode` toggle or separate sections |
| 6 | Glossary section | All 18 terms in §6 |
| 7 | Navigation flow diagram | Visual diagram showing screens ①-⑧ from §2 |

**Integration note for CC:**
- This becomes a new page at `/strategist/manual`
- Accessible from the module nav (small "Manual" link alongside the back/forward CTAs)
- No backend data needed -- this is a fully static page
- Route: `ProtectedRoute` (Premium only) or open to all logged-in users -- TT to confirm

---

## 9. Reference Files

| File | Purpose |
|---|---|
| `frontend/src/pages/strategist/StrategistPage.jsx` | Full 5-layer War Room -- layer definitions and taglines |
| `frontend/src/pages/strategist/TheStrategistLandingPage.jsx` | Landing page copy -- FAQ, problem sections, credibility |
| `frontend/src/pages/strategist/StrategistWarRoomPage.jsx` | Snapshot dashboard -- panels and data |
| `frontend/src/components/strategist/war-room/utils.js` | Band definitions, verdict copy, score thresholds |
| `frontend/src/styles/strategist-tokens.css` | All CSS tokens -- full token registry |
| `Codex_Deliveries/Strategist/THE_STRATEGIST_FULL_SPEC.md` | Full module specification -- master reference |

---

## 10. Commission Priority

| Field | Value |
|---|---|
| Priority | 🟠 HIGH -- blocks new user onboarding comprehension |
| Blocking | Soft launch to paid users |
| Bundle with | Any other post-diagnostic Strategist CD commissions |
| Estimated CD effort | Large -- full page design, all sections |
| New route needed | `/strategist/manual` -- CC to wire after delivery |
