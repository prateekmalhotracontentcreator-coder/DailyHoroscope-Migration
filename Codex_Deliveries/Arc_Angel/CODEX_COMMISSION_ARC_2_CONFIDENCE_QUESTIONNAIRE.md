# Codex Commission Brief -- ARC-2: Arc Angel Dynamic Confidence Engine
> Commission ID: ARC-2
> Thread: Arc Angel
> Brief rewritten: 2026-05-17 (supersedes 2026-05-15 draft)
> Pre-condition: ARC-UI ✅ INTEGRATED · KE-Sprint3 ✅ must be INTEGRATED before issuing ARC-2
> Priority: 🟠 HIGH -- issue immediately after KE-Sprint3 gate passes

---

## ⭐ Read Before Writing a Single Line

**Architecture rule (TD-28):** All dasha/astronomical computations come from `vedic_calculator.py`. Do NOT add dasha logic to `knowledge_engine.py`.

**UI lock (Temple Team -- 2026-05-17):** The 3-column LeftNav Arc Angel panel with Confidence % donut scores is **locked**. No UI/UX changes to the existing panel without explicit Temple Team approval. Deliverables 2 and 3 in this brief are flagged accordingly.

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

## Deliverable 5 -- "Upgrade Confidence" Dashboard Prompt

> **UI note:** This is a new UI element, not a change to the existing panel. Requires Temple Team visual review before Codex builds. TT to confirm design or provide mockup before issuing this deliverable.

**Concept (subject to TT approval):**

When a user views the Arc Angel dashboard and their score is below 86%, show a contextual upgrade prompt:

```
┌─────────────────────────────────────────────┐
│  ✦  Upgrade your Confidence Score           │
│  Unlock 2 modules for +10% accuracy         │
│                                             │
│  [ Tarot Daily Draw +5% ]  [ Strategist +5% ]│
│                  [ Explore →]               │
└─────────────────────────────────────────────┘
```

Shown when:
- `pillar_3_score < 10` (user has not yet earned full ritual score)
- User is Premium (non-premium users see the premium gate first)

Links: Tarot button → `/tarot` · Strategist button → `/strategist`

**This deliverable is gated on TT design approval. Do not build until confirmed.**

---

## Deliverables 6 & 7 -- Premium Gate + Desktop Sidebar

> **UI lock (2026-05-17):** These were in the original ARC-2 brief. They are valid product features but are gated on explicit Temple Team visual approval before Codex can build. Do not include in the initial ARC-2 issue.
>
> **Deliverable 6 (Premium Gate on period columns):** Free users see blurred/locked auspicious/inauspicious windows with upgrade CTA. Premium users see full data.
>
> **Deliverable 7 (Desktop Sidebar):** Persistent `w-80` sticky sidebar on `lg+` in `ArcAngelPage.jsx`, collapsible, preference saved in `localStorage`.
>
> TT to explicitly confirm these two deliverables before they are added to the active commission.

---

## Files to Modify

```
backend/server.py                             ← Pillar 3 decay job (APScheduler)
backend/questionnaire_router.py              ← Pillar 1 area-complete hook
backend/[report routers]                     ← Pillar 2 IR-generated hook
backend/knowledge_engine.py                  ← log_ritual_event(), tiered_recovery_points()
```

**Do NOT touch:**
```
backend/vedic_calculator.py
frontend/src/components/ArcAngelPanel.jsx    ← UI locked -- no changes without TT approval
frontend/src/components/NavBar.jsx           ← UI locked
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

**Upgrade prompt:**
- [ ] ⏸ HOLD -- pending TT design approval (Deliverable 5)

**Premium gate + sidebar:**
- [ ] ⏸ HOLD -- pending TT explicit approval (Deliverables 6 + 7)
