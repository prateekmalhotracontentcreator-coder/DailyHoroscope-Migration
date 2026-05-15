# Codex Commission Brief -- KE-IQ: Questionnaire UI + β/γ Knowledge Engine Wiring
> Commission ID: KE-IQ
> Thread: Knowledge Engine (Commission I-Q -- Phase 1, TD-19/TD-25)
> Issued: 2026-05-15 | Priority: 🔴 HIGH
> Pre-condition: KE Sprint 1 ✅. Ideally after KE Sprint 2 gate passes (β/γ scoring works best post-arbitration).

---

## Context

TD-19 (Session 3) locked: *"Questionnaire-driven β/γ inputs -- schema Phase 1; UI is Commission I-Q, a separate commission."* TD-25 confirmed: *"Separate Phase 1 commission outside Commission I hours."*

**What already exists in the codebase:**
- `frontend/src/pages/account/QuestionnairePage.jsx` -- 29-line thin wrapper page, routed at `/questionnaire`
- `frontend/src/components/QuestionnaireWidget.jsx` -- 1,101-line full UI widget (already renders the questionnaire form with all questions and categories)
- `knowledge_schema.py` -- `QuestionnaireResponse` schema with β/γ fields already defined (Phase 1 schema)
- `_score_rule()` in `knowledge_engine.py` -- already accepts β/γ multipliers (Sprint 1 wired the hook)

**What is missing (G-10):**
- Backend endpoint to save questionnaire answers and compute β/γ scores
- `QuestionnaireWidget.jsx` is not connected to any backend -- answers go nowhere
- β/γ scores are never retrieved and never passed into `scan_chart()` calls
- Confidence % in `ArcAngelPanel.jsx` stays at hardcoded baseline 42 regardless of questionnaire completion

---

## Architecture Rule

All dasha/astronomical computations must come from `vedic_calculator.py`. Do NOT add dasha functions to `knowledge_engine.py`. β/γ are user-contextual multipliers derived from questionnaire answers -- not astronomical data.

---

## What β and γ Are

From the KE Contract (TD-01/TD-19):

| Parameter | Meaning | Source |
|---|---|---|
| `alpha` | Macro-environmental signal (World Context Engine -- Phase 2) | Currently hardcoded 1.0 |
| **`beta`** | **User's current life-phase context** (age, career stage, family status, current concerns) | **Questionnaire** |
| **`gamma`** | **User's personal focus areas** (which of the 12 domains matter most to them right now) | **Questionnaire** |

β and γ are floating-point multipliers applied in `_score_rule()` to boost/dampen rules based on user context. Range: 0.78-1.22.

---

## Deliverables

### Deliverable 1 -- Backend: Questionnaire Storage + β/γ Computation

**New endpoint:** `POST /api/knowledge-engine/questionnaire/submit`

Request body:
```json
{
    "answers": {
        "age_band": "25-35",
        "career_stage": "growth",
        "family_status": "married_with_children",
        "current_concerns": ["career", "finances", "health"],
        "focus_domains": ["career", "relationships", "finances"],
        "life_phase": "building",
        "stress_level": "moderate"
    }
}
```

Response:
```json
{
    "beta": 1.08,
    "gamma": 1.12,
    "questionnaire_id": "...",
    "completed_at": "2026-05-15T10:00:00Z",
    "focus_domains": ["career", "relationships", "finances"]
}
```

**β/γ computation rules:**
- `beta` is computed from life-phase context answers (career_stage, age_band, family_status, stress_level)
- `gamma` is computed from domain focus area selections (focus_domains, current_concerns)
- Base value: 1.0. Adjust by ±0.04-0.08 per relevant answer. Max: 1.22, floor: 0.78.
- Store the result in a new MongoDB collection: `user_questionnaire_profiles`
- Document structure:
  ```json
  {
      "user_id": "...",
      "answers": { ... },
      "beta": 1.08,
      "gamma": 1.12,
      "focus_domains": [...],
      "completed_at": "...",
      "version": 1
  }
  ```

**New endpoint:** `GET /api/knowledge-engine/questionnaire/profile`

Returns the user's current β/γ profile (if they have completed the questionnaire), or `null` if not yet completed.

Response:
```json
{
    "completed": true,
    "beta": 1.08,
    "gamma": 1.12,
    "focus_domains": ["career", "relationships", "finances"],
    "completed_at": "2026-05-15T10:00:00Z"
}
```

Or if not completed:
```json
{ "completed": false, "beta": 1.0, "gamma": 1.0, "focus_domains": [] }
```

**Wire β/γ into scan_chart calls:**
Update `GET /api/knowledge-engine/arc-angel-windows` in `server.py` to:
1. Look up the user's questionnaire profile (if authenticated)
2. Pass the retrieved `beta` and `gamma` into `scan_chart()` call
3. If no profile exists, use defaults β=1.0, γ=1.0

---

### Deliverable 2 -- Confidence % Growth with Questionnaire Completion

The current `overall_confidence_pct` in the Arc Angel endpoint is hardcoded to 42 (birth data baseline).

Update the confidence computation in `GET /api/knowledge-engine/arc-angel-windows`:

```python
BASE_CONFIDENCE = 42          # birth data only
QUESTIONNAIRE_BONUS = 18      # completing questionnaire
MODULE_BONUS_PER_MODULE = 4   # each additional module used (cap at 3 modules = +12)

confidence_pct = BASE_CONFIDENCE
if questionnaire_completed:
    confidence_pct += QUESTIONNAIRE_BONUS   # → 60%
# Module usage tracked via Punya Rewards earn hooks already wired
# Check user's action_log for: birth_chart_generate, numerology_report_generate,
# tarot_daily_draw, panchang_daily_view (each = +4, max 3 = +12)
# Total max: 42 + 18 + 12 = 72%
```

Store module usage count on `user_questionnaire_profiles` document as `modules_used: int`.

Update the response:
```json
{
    "overall_confidence_pct": 60,
    "questionnaire_completed": true,
    "confidence_breakdown": {
        "birth_data": 42,
        "questionnaire": 18,
        "module_usage": 0
    }
}
```

Also propagate updated `confidence_pct` to each domain in `arc_angel_windows`.

---

### Deliverable 3 -- Frontend: Wire QuestionnaireWidget to Backend

**File:** `frontend/src/pages/account/QuestionnairePage.jsx`

Currently 29 lines -- just renders `<QuestionnaireWidget />`. Expand to:

1. On mount: call `GET /api/knowledge-engine/questionnaire/profile` to check if already completed
2. If completed: show completion state with β/γ values + CTA to retake or view Arc Angel
3. If not completed: render `<QuestionnaireWidget onComplete={handleSubmit} />` 
4. `handleSubmit(answers)`:
   - Call `POST /api/knowledge-engine/questionnaire/submit` with answers
   - On success: show "Your Cosmic Profile is set ✦" confirmation
   - Display returned β/γ scores with brief explanation ("Your focus context is now calibrating your Vedic readings")
   - CTA: "View Your Arc Angel Reading →" → navigate to `/arc-angel`
5. Authentication guard: if not logged in, show login prompt (do NOT redirect automatically -- show inline CTA)

**QuestionnaireWidget.jsx integration:**
- `QuestionnaireWidget` already renders the full question flow (1,101 lines)
- Add `onComplete` prop: `onComplete(answers: object) => void`
- On the final "Submit" action inside the widget, call `onComplete(answers)` instead of doing nothing
- Do NOT rewrite the widget -- only add the `onComplete` callback hook at the submit action

---

### Deliverable 4 -- ArcAngelPanel.jsx: Show Questionnaire CTA when Not Completed

In `frontend/src/components/ArcAngelPanel.jsx`:

After fetching the Arc Angel windows, also fetch `GET /api/knowledge-engine/questionnaire/profile`.

If `completed: false`:
- Add a subtle prompt below the domain table:
  ```
  ✦ Complete your Cosmic Profile to improve accuracy to 60%+
  [Complete Questionnaire →]  (links to /questionnaire)
  ```
- Show current confidence % prominently: "Accuracy: 42% (birth data only)"

If `completed: true`:
- Show: "Accuracy: 60% ✦" (or actual computed value)
- No questionnaire CTA

---

## Files to Create / Modify

### Create:
```
(none -- QuestionnairePage.jsx already exists)
```

### Modify:
```
backend/server.py                              ← add 2 new endpoints + wire β/γ into arc-angel-windows
backend/knowledge_engine.py                   ← update confidence_pct computation
frontend/src/pages/account/QuestionnairePage.jsx  ← expand from 29 lines to full wired page
frontend/src/components/QuestionnaireWidget.jsx   ← add onComplete prop at submit action
frontend/src/components/ArcAngelPanel.jsx         ← add questionnaire completion check + CTA
```

### Do NOT touch:
```
backend/vedic_calculator.py
backend/panchang_router.py
backend/knowledge_schema.py    (schema already has QuestionnaireResponse -- do not restructure)
frontend/src/pages/ArcAngelPage.jsx   (full detail page -- separate from the panel)
```

---

## Theme Tokens

```css
bg-background · bg-card · text-foreground · text-muted-foreground
text-gold / border-gold / bg-gold   (#c5a059)
```

GlassCard: `rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`

---

## Route (Already Registered)

`/questionnaire` is already in App.js. Do not modify App.js unless there is a broken import.

---

## Build Verification

```bash
cd frontend && CI=true DISABLE_ESLINT_PLUGIN=true npx craco build
```

Zero errors required.

---

## Commit Format

```
feat(ke-iq): wire questionnaire β/γ to knowledge engine + confidence % growth
```

---

## Definition of Done

- [ ] `POST /api/knowledge-engine/questionnaire/submit` saves to `user_questionnaire_profiles` and returns β/γ
- [ ] `GET /api/knowledge-engine/questionnaire/profile` returns completion state + β/γ or `completed: false`
- [ ] `GET /api/knowledge-engine/arc-angel-windows` passes user β/γ into `scan_chart()` when profile exists
- [ ] Confidence % grows from 42 → 60 when questionnaire is completed
- [ ] `QuestionnairePage.jsx` shows completion state and submits answers to backend
- [ ] `QuestionnaireWidget.jsx` calls `onComplete(answers)` on final submit
- [ ] `ArcAngelPanel.jsx` shows questionnaire CTA and live confidence %
- [ ] Build passes zero errors
