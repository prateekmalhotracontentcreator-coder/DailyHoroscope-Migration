# Commission IR-2A -- Lunar Cycle Wellness: Content Rework + Action Tracker

> EverydayHoroscope · Stack: FastAPI, pyswisseph 2.10.x, MongoDB, React 18
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Depends on: IR-2 ✅ (base router live at `/api/reports/lunar-cycle`)
> Date: 2026-05-16

---

## Context

IR-2 delivered the Lunar Cycle Wellness backend (`lunar_cycle_router.py`) and it is now live.
After live testing, **two issues are identified:**

1. **Thin content output** -- the Claude enrichment produces only a single short paragraph. The report lacks depth, structure, and actionable direction. Users see one block of text with no clear sections or guidance.
2. **No Action Tracker** -- there is no concrete, day-by-day or weekly action layer. The report describes the moon phase but does not tell the user what to *do* with that information.

This commission fixes both issues. It is an **amendment** to IR-2 -- no new endpoints, no schema-breaking changes.

---

## What to Read First

```
backend/lunar_cycle_router.py           ← live router (DO NOT change endpoint signatures)
backend/lunar_cycle_prompt_service.py   ← primary file to rework
backend/love_prompt_common.py           ← shared Claude helper (do not modify)
frontend/src/pages/reports/LoveReportsPage.jsx  ← frontend display (see Part B)
```

Read all four files before writing any code.

---

## Part A -- Backend: `lunar_cycle_prompt_service.py` (Full Rework)

### A1. Expand the Claude Prompt

Replace `_build_prompt()` with a substantially richer prompt that:

- Instructs Claude to write **each prose field as a full 2-3 paragraph narrative** (not a single sentence)
- Demands **specificity** -- reference the actual phase name, nakshatra name, natal moon sign, and transit house explicitly in the body of each field
- Demands **tone calibration** -- intimate, grounded, practically useful, never generic astrology boilerplate
- Sets strict field constraints (listed below)

**New prompt structure:**

```python
def _build_prompt(report: Any) -> str:
    output = report.output_payload
    phase = output.moon_phase.phase_name
    cycle_day = output.moon_phase.cycle_day
    illumination = output.moon_phase.illumination_pct
    days_to_full = output.moon_phase.days_to_full_moon
    days_to_new = output.moon_phase.days_to_new_moon
    nakshatra = output.moon_nakshatra.name
    pada = output.moon_nakshatra.pada
    lord = output.moon_nakshatra.lord
    natal_sign = output.natal_context.natal_moon_sign
    transit_house = output.natal_context.transit_house

    return f"""
You are writing a premium Vedic Lunar Cycle Wellness report for Everyday Horoscope.
The user's astronomical data is already computed -- your job is enrichment, not calculation.

Current lunar snapshot:
- Phase: {phase} (cycle day {cycle_day}/30, illumination {illumination}%)
- Days to Full Moon: {days_to_full} | Days to New Moon: {days_to_new}
- Moon Nakshatra: {nakshatra} Pada {pada} (lord: {lord})
- User's Natal Moon Sign: {natal_sign}
- Moon is currently transiting their {transit_house}th natal house

Existing summary line: {report.summary}

RULES:
1. Reference the specific phase name, nakshatra name, natal sign, and house number explicitly in the prose.
2. `phase_wellness_note` -- 3 paragraphs. Cover: (a) what this phase energetically means for the body and mood, (b) what activities/decisions it supports and which it does not, (c) how this interacts with the user's natal Moon in {natal_sign}.
3. `nakshatra_wellness_note` -- 2 paragraphs. Cover: (a) the quality and character of {nakshatra} and how it colours the emotional field, (b) specific wellness implications for this nakshatra-transit-house combination.
4. `weekly_rhythm` -- exactly 3 strings. Each string is one concrete scheduling or pacing principle for the week. Not vague. Actionable (e.g., "Front-load meetings before Wednesday -- lunar sensitivity peaks Thursday onward").
5. `recommended_practices` -- exactly 3 items, each with `practice_name` (3-5 words) and `description` (2-3 sentences -- what to do, when, and why it works for this phase/nakshatra combination).
6. `caution_note` -- 2 sentences. One thing to genuinely watch for this week and one reframe.
7. `action_tracker` -- 7 items, one per day (Monday through Sunday). Each item: `day` (e.g. "Monday"), `intention` (3-7 words -- the day's theme), `action` (1 sentence -- one concrete, specific thing to do or avoid).
8. `summary` -- one compelling sentence (under 25 words) summarising this week's lunar quality for the user.

TONE: Warm, intimate, precise. Never generic. Never use phrases like "the universe is guiding you" or "listen to your heart". Speak to actual rhythms, practices, and decisions.

Return valid JSON only with these keys:
summary, phase_wellness_note, nakshatra_wellness_note, weekly_rhythm,
recommended_practices, caution_note, action_tracker
""".strip()
```

### A2. Add `LunarCycleActionDay` and `LunarCycleActionTracker` Models

In `lunar_cycle_router.py`, add these two model classes (insert after `LunarCycleWellness`):

```python
class LunarCycleActionDay(StrictModel):
    day: str
    intention: str
    action: str


class LunarCycleActionTracker(StrictModel):
    days: list[LunarCycleActionDay] = Field(default_factory=list)
```

Add `action_tracker` field to `LunarCycleOutput`:

```python
class LunarCycleOutput(StrictModel):
    reference_date: str
    moon_phase: LunarCycleMoonPhase
    moon_nakshatra: LunarCycleMoonNakshatra
    natal_context: LunarCycleNatalContext
    wellness: LunarCycleWellness
    action_tracker: LunarCycleActionTracker   # ← ADD THIS
    generated_at: datetime
```

### A3. Update `_default_wellness()` + Add `_default_action_tracker()`

Add a `_default_action_tracker()` function that returns 7 placeholder days.
Update `_build_report()` in `lunar_cycle_router.py` to call it and populate `action_tracker`.

**`_default_action_tracker()` example:**
```python
def _default_action_tracker(phase_name: str) -> LunarCycleActionTracker:
    is_waxing = phase_name in ("New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous")
    days = [
        LunarCycleActionDay(day="Monday",    intention="Set the week's anchor",       action="Write one clear intention for the week before checking messages." if is_waxing else "Review last week's open threads before opening anything new."),
        LunarCycleActionDay(day="Tuesday",   intention="Forward motion",              action="Schedule your most demanding task in the morning window." if is_waxing else "Delegate or defer anything non-essential."),
        LunarCycleActionDay(day="Wednesday", intention="Connection and communication",action="Initiate a meaningful conversation or collaboration." if is_waxing else "Listen more than you speak in group settings today."),
        LunarCycleActionDay(day="Thursday",  intention="Energy check",                action="Notice your energy at noon -- use it as a guide for the rest of the week." if is_waxing else "Protect your afternoon for restorative, solo work."),
        LunarCycleActionDay(day="Friday",    intention="Consolidate gains",           action="Finish what you started -- resist opening new projects." if is_waxing else "Close loops rather than beginning anything new."),
        LunarCycleActionDay(day="Saturday",  intention="Nourish the body",            action="Spend 20 minutes outdoors, ideally near water or greenery." if is_waxing else "Extra rest today is not laziness -- it is phase-appropriate recovery."),
        LunarCycleActionDay(day="Sunday",    intention="Inner review",                action="Journal briefly: what expanded this week and what drained you?" if is_waxing else "Set tomorrow's one priority before the evening ends."),
    ]
    return LunarCycleActionTracker(days=days)
```

### A4. Update `_apply_content()` in `lunar_cycle_prompt_service.py`

Add action_tracker parsing after the existing `recommended_practices` block:

```python
action_tracker_raw = content.get("action_tracker")
if isinstance(action_tracker_raw, list) and action_tracker_raw:
    parsed_days = []
    for item in action_tracker_raw:
        if not isinstance(item, dict):
            continue
        day = str(item.get("day") or "").strip()
        intention = str(item.get("intention") or "").strip()
        action = str(item.get("action") or "").strip()
        if day and intention and action:
            parsed_days.append({"day": day, "intention": intention, "action": action})
    if parsed_days:
        report.output_payload.action_tracker = {"days": parsed_days[:7]}
```

### A5. Update `_fallback_content()` in `lunar_cycle_prompt_service.py`

Replace the thin single-sentence fallback strings with 2-3 paragraph versions for `phase_wellness_note` and `nakshatra_wellness_note`.

Add a fallback `action_tracker` with 7 default days (waxing/waning aware, same as `_default_action_tracker()`).

Expand `caution_note` to 2 full sentences.

---

## Part B -- Frontend: `LoveReportsPage.jsx` (Display Rework)

### Current State
The existing renderer displays the `wellness` object fields as blocks of text. The `action_tracker` is new and has no renderer yet.

### What to Add

Find the section in `LoveReportsPage.jsx` where the `lunar_cycle_wellness` report output is rendered (look for the `output_payload` display block for `report_type === "lunar_cycle_wellness"` or the generic wellness display).

**Add the following sections to the Lunar Cycle report display:**

#### 1. Phase Wellness Note (expanded -- already exists, just ensure full multi-paragraph display)
Render `output_payload.wellness.phase_wellness_note` in a styled prose block. Use `white-space: pre-line` so paragraph breaks render correctly.

#### 2. Nakshatra Wellness Note (expanded -- already exists)
Same treatment as above for `nakshatra_wellness_note`.

#### 3. Weekly Rhythm (already exists -- confirm it renders all 3 bullets as a list)
Render `weekly_rhythm` as a bulleted list with a section header "This Week's Rhythm".

#### 4. Recommended Practices (already exists -- confirm card display)
Render as 3 cards: `practice_name` as card title, `description` as body.

#### 5. Action Tracker -- NEW SECTION
Title: **"Your 7-Day Lunar Action Tracker"**

Render `output_payload.action_tracker.days` as a 7-row tracker table or card stack:

```
┌──────────────┬──────────────────────────┬────────────────────────────────────────┐
│ Day          │ Intention                │ Today's Action                         │
├──────────────┼──────────────────────────┼────────────────────────────────────────┤
│ Monday       │ Set the week's anchor    │ Write one clear intention before...    │
│ Tuesday      │ Forward motion           │ Schedule your most demanding task...   │
│ ...          │ ...                      │ ...                                    │
└──────────────┴──────────────────────────┴────────────────────────────────────────┘
```

Style: gold header row, alternating subtle row tints, consistent with GlassCard design system.
Mobile: collapse to card stack (one card per day, day name as card header).

**Highlight today's row** -- compare `day` string to the current JavaScript weekday name and apply a gold border or background to the matching row.

#### 6. Caution Note (already exists -- add icon prefix ⚠️ and style as a soft warning card)

---

## Part C -- Update `max_tokens` in prompt service

In `lunar_cycle_prompt_service.py`, the current call is:
```python
content = await try_claude_generation(_build_prompt(report), max_tokens=750)
```

The expanded output (7 action days + rich prose) needs more tokens. Change to:
```python
content = await try_claude_generation(_build_prompt(report), max_tokens=1800)
```

---

## Constraints

- **Do NOT change the endpoint URLs** -- `/api/reports/lunar-cycle/generate` and `/history` stay the same
- **Do NOT break existing stored reports** -- `action_tracker` must default gracefully when absent (old reports have no `action_tracker` key)
- **Do NOT modify `vedic_shared_utils.py`**, `love_prompt_common.py`, or `server.py`
- All Python follows existing style: `StrictModel`, type annotations, `Field(default_factory=list)`
- React display must pass `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` with zero errors

---

## Acceptance Criteria

- [ ] `POST /api/reports/lunar-cycle/generate` returns `action_tracker.days` with 7 items
- [ ] `phase_wellness_note` is at least 3 paragraphs in generated output
- [ ] `nakshatra_wellness_note` is at least 2 paragraphs
- [ ] Frontend Lunar Cycle report displays the 7-Day Action Tracker section
- [ ] Today's row is highlighted in the tracker
- [ ] All 6 display sections render (Phase Note, Nakshatra Note, Weekly Rhythm, Practices, Action Tracker, Caution)
- [ ] Old stored reports without `action_tracker` do not crash the frontend (graceful empty state)
- [ ] Build exits 0 with no ESLint errors
