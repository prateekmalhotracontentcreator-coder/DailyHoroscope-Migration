# Codex Commission Brief -- ARC-2: Arc Angel Dynamic Confidence Engine
> Commission ID: ARC-2
> Thread: Arc Angel
> Brief rewritten: 2026-05-17 (supersedes 2026-05-15 draft)
> UI design finalised: 2026-05-17 (all HOLDs lifted -- see Section UI-SPEC)
> Pre-condition: ARC-UI ✅ INTEGRATED · KE-Sprint3 ✅ LIVE · KE-OP-14 ✅ FIXED
> Priority: 🔴 HIGH -- all blockers cleared, issue immediately

---

## ⭐ Read Before Writing a Single Line

**Architecture rule (TD-28):** All dasha/astronomical computations come from `vedic_calculator.py`. Do NOT add dasha logic to `knowledge_engine.py`.

**UI redesign approved (2026-05-17):** The Left Nav Bar and Janamkundali Snapshot panel are being redesigned in this commission. Full spec in Section UI-SPEC below. The existing `ArcAngelPanel.jsx` is the starting point -- rebuild it to match the spec.

**Sprint 3 dependency:** KE-Sprint3 builds the `user_arc_angel_profile` schema skeleton with the 3-pillar structure and the `_compute_confidence()` function. ARC-2 wires the dynamic data into those pillars -- it does NOT rebuild the schema or the collection.

---

## Confidence Architecture (Temple Team locked 2026-05-17)

```
Foundation  40%  →  Vedic Astrology Engine (DOB + time + place)
                     Label always shown: "Vedic Astrology Engine Activated"

Pillar 1   +24%  →  12 Focus Areas Questionnaire
                     +2% per Focus Area fully completed (all 3 Q's answered)
                     Social Sphere = 6 of the 12 Focus Areas
                     (Social Sphere 12% is carved from the 24%, not additive)

Pillar 2   +12%  →  Individual Reports
                     +1% per IR generated and fed back to Arc Angel
                     Max 12 IRs × 1% = 12%

Pillar 3   +10%  →  Daily Rituals (dynamic -- decays with inactivity)
                     Tarot / Love Bundle: up to 5%
                     The Strategist: up to 5%

Cap         86%  →  100% is architecturally impossible (epistemic honesty)
```

**Case studies are internal KE accuracy benchmarks only** -- equivalent to DrikPanchang verification for Panchang. They do NOT contribute to user confidence score.

---

## Source of Truth Files (Read These First)

```
Codex_Deliveries/Arc_Angel/CODEX_COMMISSION_ARC_ANGEL_UI_PANEL.md    ← Phase 1 handoff
Codex_Deliveries/Knowledge_Engine/CODEX_COMMISSION_KE_SPRINT3_ARC_ANGEL.md  ← schema + _compute_confidence()
backend/knowledge_engine.py                                            ← Arc Angel computation
backend/server.py                                                      ← arc-angel-windows endpoint
frontend/src/components/ArcAngelPanel.jsx                              ← live panel (UI locked)
frontend/src/pages/ArcAngelPage.jsx                                    ← full detail view
```

---

---

## UI-SPEC -- Approved Design (Temple Team, 2026-05-17)

> All items in this section are **approved and active**. No HOLDs. Build exactly as specified.

### Left Nav Bar -- 2-Section Split

The Left Nav Bar is split into two independently scrollable / collapsible sections:

```
┌─────────────────────────────────┐
│  Section 1: Janamkundali        │  ← Snapshot panel (see below)
│  Snapshot                       │
├─────────────────────────────────┤
│  Section 2: Navigation          │  ← Replica of Top Menu Bar links
│  Home · Panchang · Tarot · ...  │    (same links as the top nav)
└─────────────────────────────────┘
```

Both sections are clickable. Section 2 mirrors the existing top nav structure -- no new routes needed.

---

### Section 1 -- Janamkundali Snapshot Panel

**Access:** All signed-up users (free and premium). No gate on the dashboard itself.

**Top of panel -- Consolidated Donut:**
```
┌─────────────────────────────────────────────────────┐
│   [Consolidated Donut]   Arc Angel Confidence       │
│        40%               Vedic Astrology Engine     │
│                          Activated                  │
│  🔓 Unlock the Potential of Vedic Astrology         │
│     in all 12 Areas of Life                         │
└─────────────────────────────────────────────────────┘
```
- Consolidated donut = `overall_confidence_pct` from KE (the 3-pillar formula result)
- CTA text: **"🔓 Unlock the Potential of Vedic Astrology in all 12 Areas of Life"**
- CTA links to the full Questionnaire page (`/arc-angel/questionnaire` or `QuestionnairePage.jsx`)

**12 Domain Rows (2-column layout):**

Each row has two columns:
- **Column 1:** Focus area name (e.g. "Health & Fitness")
- **Column 2:** Individual domain donut showing `domain_confidence_pct` for that domain

```
┌──────────────────────────────┬────────────┐
│  Health & Fitness         ▼  │  [donut]   │
│                              │    42%     │
├──────────────────────────────┴────────────┤
│  ▸ Favourable Periods                     │
│    Moon AD in Rahu MD    2027-05→2028-11  │
│    Jupiter AD in Jup MD  2029-12→2032-01  │
│    Mercury AD in Jup MD  2034-08→2036-05  │
├───────────────────────────────────────────┤
│  ▸ Unfavourable Periods                   │
│    Venus AD in Rahu MD   2026-05→2027-05  │
│    Mars AD in Rahu MD    2028-11→2029-12  │
│    Saturn AD in Jup MD   2032-01→2034-08  │
└───────────────────────────────────────────┘
```

- Row is collapsed by default; clicking expands it
- Sub-dropdowns: **Favourable Periods** (3 rows) and **Unfavourable Periods** (3 rows)
- Period data comes from `/api/knowledge-engine/arc-angel-windows` (already live)
- **All 12 rows and all period data visible to all signed-up users** -- no blurring, no hiding
- If a domain has a Quality Badge (user ran a premium IR for this domain): show a small `⭐ Premium` chip alongside the donut in Column 2

**Per-domain confidence (`domain_confidence_pct`):**

Add a new field `domain_confidence_pct` to each domain object in the arc-angel-windows response:

```python
def _compute_domain_confidence(domain_id: str, profile: dict) -> int:
    """
    Per-domain confidence reflects data completeness for that specific area.
    Base 40% (birth data, same for all) + 2% if questionnaire answered for this domain.
    Quality badges (IR premium data) are separate visual indicators -- not % contributors.
    """
    score = 40
    areas_completed = (profile.get("pillar_1") or {}).get("areas_completed") or []
    if domain_id in areas_completed:
        score += 2
    return score
```

Consolidated donut = `overall_confidence_pct` (existing KE formula -- reflects all 3 pillars).

---

### Premium Gate -- What Is and Isn't Gated

| Element | Free Users | Premium Users |
|---|---|---|
| Arc Angel Dashboard | ✅ Full access | ✅ Full access |
| 12 domain rows | ✅ Visible | ✅ Visible |
| Period windows (Favourable / Unfavourable) | ✅ Visible | ✅ Visible |
| Questionnaire (all 12 areas) | ✅ Open | ✅ Open |
| Individual Reports (IRs) | 🔒 Premium only | ✅ Full access |
| Quality Badges (per domain) | Not shown | ⭐ Shown when IR run |
| Consolidated Donut | ✅ Visible | ✅ Visible + richer data |

**Free user lock CTA on Left Sidebar:**

For users without premium subscription, show at the bottom of Section 1:
```
🔒 Upgrade to Arc Angel Pro
   Get High-Fidelity Forecasts with Individual Reports
   [ Explore Reports → ]
```
- Links to the Individual Reports catalogue (`/individual-reports`)
- This is the ONLY lock shown to free users -- it's a soft upsell, not a content gate

---

### Quality Badges

A Quality Badge (`⭐ Premium`) appears in Column 2 of a domain row when the user has generated a premium IR that maps to that domain. Badge renders alongside the donut %, not replacing it.

**Domain → IR mapping (for badge logic):**

```python
DOMAIN_IR_MAP = {
    "health":        ["longevity", "individual_natal"],
    "career":        ["brihat_kundali", "numerology", "individual_natal"],
    "finances":      ["brihat_kundali", "lal_kitab", "numerology"],
    "learning":      ["brihat_kundali", "kp_oracle"],
    "emotional":     ["love_compatibility", "lunar_cycle"],
    "spirituality":  ["kp_oracle", "individual_natal"],
    "relationships": ["love_compatibility", "soul_connection"],
    "family":        ["brihat_kundali", "individual_natal"],
    "social":        ["numerology", "individual_natal"],
    "adventure":     ["individual_natal", "solar_return"],
    "environment":   ["lal_kitab", "individual_natal"],
    "creativity":    ["numerology", "tarot_spread"],
}

def domain_has_quality_badge(domain_id: str, reports_run: list) -> bool:
    mapped_irs = DOMAIN_IR_MAP.get(domain_id, [])
    return any(ir in reports_run for ir in mapped_irs)
```

Return `has_quality_badge: bool` per domain in the arc-angel-windows response.

---

### Upgrade Prompt Placements (Approved)

**Placement 1 -- User Account Section:**
1-line prompt with link to dedicated page:
```
Unlock Arc Angel Pro -- Higher confidence forecasts across all 12 life areas. Learn more →
```
Links to `/arc-angel/upgrade` or the Individual Reports catalogue.

**Placement 2 -- Questionnaire Page:**
Full CTA block at the top/bottom of the Questionnaire page:
```
┌─────────────────────────────────────────────────────┐
│  ✦ Complete Your Arc Angel Profile                  │
│  Every question answered raises your confidence %.  │
│  Upgrade to Arc Angel Pro for Individual Reports    │
│  that elevate each domain's accuracy by up to 43%. │
│                  [ Explore Reports → ]              │
└─────────────────────────────────────────────────────┘
```

---

## 12 Domain Slugs (Locked -- Do Not Change)

```
health · career · finances · learning · emotional · spirituality
relationships · family · social · adventure · environment · creativity
```

Social Sphere Focus Areas (6 of 12): `family · social · environment · relationships · adventure · spirituality`
*(Exact 6 to confirm against questionnaire design -- use this list until TT specifies otherwise)*

---

## Deliverable 1 -- Pillar 1: Questionnaire Dynamic Wiring

### What to build

The questionnaire has 12 Focus Areas, 3 questions per area. When a user completes all 3 questions in a Focus Area, that area is marked complete and `pillar_1.areas_completed` in `user_arc_angel_profile` is updated.

**Backend: `backend/questionnaire_router.py` (or wherever questionnaire answers are saved)**

On questionnaire answer submission:
1. Check if all 3 questions for a Focus Area are now answered
2. If yes: add that area's slug to `user_arc_angel_profile.pillar_1.areas_completed` for this user (upsert)
3. Also update `pillar_1.social_sphere_areas_completed` if the area is one of the 6 Social Sphere areas
4. Call `_compute_confidence()` and update `overall_confidence_pct` in the profile document
5. Return the updated confidence score in the questionnaire submission response so the frontend can animate the donut immediately

**Social Sphere graduation (within Pillar 1):**

Social Sphere areas have sub-fields that unlock progressively. Example: the `family` area may have Q1 = parents birth data, Q2 = siblings, Q3 = household composition. Each question answered is tracked. The area unlocks its full 2% only when all 3 Q's are answered -- no partial credit per question, except for the following critical fields which unlock a partial score on their own:
- Parents birth data (DOB + birthplace): +0.5% per parent provided (max +1% within the area's 2%)
- Current city/location (last 12 months): +0.5% if provided within the relevant area

All other questions in a Focus Area: all-or-nothing (2% only when all 3 answered).

### Acceptance gates

1. User answers all 3 Q's for `career` area → `pillar_1.areas_completed` gains `"career"` → `_compute_confidence()` returns `40 + 2 = 42`
2. User completes all 12 areas → `pillar_1.score = 24` → `overall_confidence_pct = 64`
3. User provides parents birth data in a Social Sphere area → partial +1% applied correctly
4. Answering 1 or 2 Q's in an area (non-critical): no score change for that area

---

## Deliverable 2 -- Pillar 2: Individual Reports Wiring

### What to build

When any Individual Report is generated and its output is fed back to Arc Angel, `pillar_2.reports_run` gains that report's ID and `_compute_confidence()` is recomputed.

**Backend: report generation endpoints** (wherever IRs are saved/returned)

After each IR generation:
1. Add report type slug to `user_arc_angel_profile.pillar_2.reports_run` (skip duplicates -- 1% per unique IR only)
2. Recompute confidence and update `overall_confidence_pct`
3. Return updated confidence in report response

**Report type slugs to track (12 IRs):**
```
brihat_kundali · numerology · longevity · kp_oracle · tarot_spread
palmistry · lal_kitab · love_compatibility · lunar_cycle · solar_return
karmic_debt · individual_natal
```

*(Align with IR commission brief slugs -- these 12 map to the 12 IRs in the commission pipeline)*

### Acceptance gates

1. User generates `numerology` report → `pillar_2.reports_run` gains `"numerology"` → confidence updates
2. Generating the same report twice → `reports_run` not duplicated → score unchanged
3. 12 unique IRs generated → `pillar_2.score = 12` → confidence increases by 12 points

---

## Deliverable 3 -- Pillar 3: Daily Ritual Decay Engine

### What to build

Pillar 3 is the only dynamic, reversible pillar. It rewards daily engagement and decays with inactivity.

**Backend: add a daily scheduled job (APScheduler -- already in `server.py`)**

Job name: `arc_angel_pillar3_decay_job`
Schedule: runs daily at 02:00 IST

```python
async def arc_angel_pillar3_decay_job():
    """
    For every user_arc_angel_profile:
    1. Calculate days since last_ritual_date (or infinity if null)
    2. If days_since <= 2: grace period -- no change
    3. If days_since == 3: set decay_started_at = now, begin decay
    4. If decay_started_at set: reduce pillar_3_score by 1 per day (floor = 0)
    5. Recompute overall_confidence_pct and update document
    6. If score dropped: flag profile for notification (see Deliverable 4)
    """
```

**Ritual event logging:**

When a user completes a Tarot draw or Strategist session, call:
```python
async def log_ritual_event(db, user_id: str, ritual_type: str):
    """
    ritual_type: "tarot_love" | "strategist"
    1. Update user_arc_angel_profile.pillar_3.last_ritual_date = today
    2. Clear decay_started_at if currently set (ritual resumed)
    3. Tiered recovery: if pillar_3_score < max, apply tiered_recovery_points(days_since_decay_start)
    4. Recompute and save overall_confidence_pct
    """
```

**Tiered recovery (Phase 1):**

| Day of resumed ritual | Points added that day |
|---|---|
| Day 1 | +1 |
| Day 2 | +2 |
| Day 3 | +2 |
| Day 4+ | +2 (until max reached) |

Score never exceeds Pillar 3 max (10). Recovery is gradual -- not instant restore.

**Score split between sub-pillars:**
- Tarot/Love Bundle max: 5 points (`tarot_love_score`)
- The Strategist max: 5 points (`strategist_score`)
- `pillar_3_score = tarot_love_score + strategist_score`
- Each sub-pillar decays and recovers independently based on its own ritual events

### Pillar 3 Phase 1 rules (to refine in Phase 2)
- Grace period: 2 days (days 1-2 missed = no decay)
- Decay start: day 3 missed
- Decay rate: −1 point per day
- Floor: 0 (never negative)
- Recovery: tiered as above

### Acceptance gates

1. User with `pillar_3_score = 5` misses 2 days → no change (grace period)
2. Same user misses day 3 → `decay_started_at` set, score drops to 4
3. User resumes ritual on decay day 1 → `decay_started_at` cleared, +1 recovery → score = 5
4. Score never goes below 0 or above sub-pillar max
5. Each sub-pillar (tarot_love, strategist) decays independently

---

## Deliverable 4 -- Notification Engine Hooks

### What to build

Two notification triggers -- both hook into the existing Notifications module.

**Trigger 1: Motivational (day 2 miss -- grace period still active)**
- Fire when `days_since_last_ritual == 2` (detected by decay job)
- Message type: motivational
- Push + in-app: *"Your Arc Angel score is at {score}%. Complete today's Tarot draw to maintain your streak."*

**Trigger 2: Score-dip-risk alert (day 3+ miss -- decay started)**
- Fire when `decay_started_at` is newly set (first day of decay)
- Message type: score-dip-risk
- Push + in-app: *"Your Arc Angel Confidence score dropped to {score}%. Resume your daily ritual to recover."*
- Re-fire every 2 days while decay continues (avoid daily spam)

**Integration point:**
Hook into the existing Notifications router. The decay job flags profiles for notification; the Notifications module handles delivery (push + in-app). Do NOT build a separate notification pipeline -- use what exists.

### Acceptance gates

1. `decay_job` flags user profile with `notification_pending: "motivational"` on day 2 miss
2. `decay_job` flags profile with `notification_pending: "score_dip_risk"` on day 3+ miss
3. Re-fire: `score_dip_risk` fires again after 2 additional days of continued decay
4. Notification flag cleared after the notification is sent by the Notifications module

---

## Deliverable 5 -- Left Nav Bar Redesign + Snapshot Panel

> **Approved by Temple Team 2026-05-17. Build as specified in Section UI-SPEC.**

### 5a -- Left Nav Bar 2-Section Split

Modify the left sidebar component to show two independently collapsible sections:

1. **Janamkundali Snapshot** -- Arc Angel confidence panel (built in 5b)
2. **Navigation** -- replica of existing Top Menu Bar links (Home, Panchang, Tarot, KP Oracle, Strategist, etc.) -- same routes, no new pages

Primary UX requirement: all 12 domain rows must be visible without scroll. This split is what enables that.

### 5b -- Janamkundali Snapshot Panel Rebuild

Rebuild `ArcAngelPanel.jsx` to the approved design in Section UI-SPEC:

- **Top:** 1 consolidated donut (`overall_confidence_pct`) + engine label + CTA button
- **12 rows:** 2-column layout (Focus Area name | per-domain donut `domain_confidence_pct`)
- **Expand each row:** 2 sub-dropdowns -- Favourable Periods (3 rows) + Unfavourable Periods (3 rows)
- **Quality badge:** `⭐ Premium` chip on Column 2 when `has_quality_badge = true`
- **Free user lock CTA:** at bottom of panel for non-premium users -- "🔒 Upgrade to Arc Angel Pro" → `/individual-reports`

### 5c -- Per-domain API extension

Add `domain_confidence_pct` and `has_quality_badge` to each domain object in the `GET /api/knowledge-engine/arc-angel-windows` response. Compute using the functions defined in Section UI-SPEC. No changes to the `user_arc_angel_profile` MongoDB schema.

### 5d -- Upgrade Prompt placements (both approved)

- **User Account section:** 1-liner -- *"Unlock Arc Angel Pro -- Higher confidence forecasts across all 12 life areas. Learn more →"* -- links to `/individual-reports`
- **Questionnaire page:** Full CTA block (copy defined in Section UI-SPEC)

### Acceptance gates

1. Left Nav shows 2 distinct sections: Snapshot above, Navigation below
2. All 12 domain rows visible without scroll
3. Each row: Focus Area name (col 1) + per-domain donut % (col 2)
4. Expanding a row shows Favourable (3 rows) and Unfavourable (3 rows) sub-dropdowns with real period data from the API
5. Domain with IR run → `⭐ Premium` badge visible alongside donut
6. Free user sees "🔒 Upgrade to Arc Angel Pro" CTA at bottom of Snapshot → `/individual-reports`
7. Premium user: no lock CTA shown
8. `domain_confidence_pct` = 40% + 2% if questionnaire complete for that domain (range 40-42%)
9. Consolidated donut = `overall_confidence_pct` (existing KE formula -- reflects all 3 pillars)
10. Upgrade prompt 1-liner present in User Account section
11. Upgrade prompt full CTA block present on Questionnaire page

---

## Files to Modify

```
backend/server.py                             ← Pillar 3 decay job (APScheduler) + domain_confidence_pct + has_quality_badge in arc-angel-windows response
backend/questionnaire_router.py              ← Pillar 1 area-complete hook
backend/[report routers]                     ← Pillar 2 IR-generated hook
backend/knowledge_engine.py                  ← log_ritual_event(), tiered_recovery_points(), _compute_domain_confidence(), domain_has_quality_badge()
frontend/src/components/ArcAngelPanel.jsx    ← Full redesign per UI-SPEC (2-section split, 2-col rows, expandable sub-dropdowns)
frontend/src/components/NavBar.jsx           ← Add 2-section Left Nav split
frontend/src/pages/ArcAngelPage.jsx          ← Upgrade prompt placements
frontend/src/pages/QuestionnairePage.jsx     ← Upgrade prompt full CTA block
```

**Do NOT touch:**
```
backend/vedic_calculator.py
backend/knowledge_schema.py                  ← schema owned by Sprint 3
```

---

## Theme Tokens

```css
bg-background · bg-card · text-foreground · text-muted-foreground
text-gold / border-gold / bg-gold  (#c5a059)
GlassCard: rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm
```

---

## Build Verification

```bash
cd frontend && CI=true DISABLE_ESLINT_PLUGIN=true npx craco build
```

---

## Commit Format

```
feat(arc-angel): ARC-2 -- dynamic confidence engine, pillar 1/2/3 wiring, decay job, notification hooks
```

---

## Definition of Done

**Pillar 1:**
- [ ] Questionnaire answer submission updates `pillar_1.areas_completed` on full area completion
- [ ] Social Sphere partial credit for parents birth data (+0.5% per parent) and current location (+0.5%)
- [ ] `overall_confidence_pct` recomputed and saved after every questionnaire answer

**Pillar 2:**
- [ ] IR generation hooks update `pillar_2.reports_run` (unique slugs only)
- [ ] Confidence recomputed after each new IR

**Pillar 3:**
- [ ] `arc_angel_pillar3_decay_job` scheduled at 02:00 IST
- [ ] Grace period: 2 days no-decay
- [ ] Decay starts day 3: −1/day per sub-pillar
- [ ] Score floor: 0
- [ ] Tiered recovery on ritual resume (+1, +2, +2, +2...)
- [ ] `tarot_love_score` and `strategist_score` decay/recover independently
- [ ] `log_ritual_event()` updates `last_ritual_date` and clears `decay_started_at` on resume

**Notifications:**
- [ ] Day 2 miss → `notification_pending: "motivational"` flagged
- [ ] Day 3+ miss → `notification_pending: "score_dip_risk"` flagged
- [ ] Re-fire every 2 days during continued decay

**Left Nav + Snapshot Panel (Deliverable 5 -- approved):**
- [ ] Left Nav split: Janamkundali Snapshot section + Navigation section
- [ ] All 12 domain rows visible without scroll
- [ ] 2-column row layout: Focus Area name + per-domain donut %
- [ ] Expand each row: Favourable (3 rows) + Unfavourable (3 rows) sub-dropdowns with live API data
- [ ] Quality badge (`⭐ Premium`) shown when domain has matching IR in `pillar_2.reports_run`
- [ ] Free user: "🔒 Upgrade to Arc Angel Pro" CTA at bottom → `/individual-reports`
- [ ] Premium user: no lock CTA
- [ ] `domain_confidence_pct` and `has_quality_badge` added to arc-angel-windows API response
- [ ] Consolidated donut = `overall_confidence_pct` (3-pillar formula)
- [ ] Upgrade prompt 1-liner in User Account section
- [ ] Upgrade prompt full CTA block on Questionnaire page
