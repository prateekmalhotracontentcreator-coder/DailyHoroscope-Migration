# Codex Commission -- STR-3C: Office Direction Selector (Digbala Unlock)
> Module: The Strategist
> Closes: STR-OP-30 (office direction UI for Digbala bonus)
> Depends on: STR-FIX-3 ✅ (`dc4b557` -- Digbala backend ready, reads `profile.office_direction`)
> Last updated: 2026-06-05

---

## What This Commission Delivers

The Digbala scoring factor in the Conquest Score engine is **fully wired** on the backend (as of `dc4b557`). It awards +15 to the Conquest Score when the user's office compass direction matches their command planet's power direction.

What is missing is the **UI input**: the user has no way to set their `office_direction`. This commission adds a single field to the Strategist profile flow and wires it to the backend.

---

## Background: How Digbala Works

Each command planet has a power direction (Digbala):

| Planet | Power Direction |
|---|---|
| Sun | South |
| Moon | North |
| Mercury | North |
| Mars | South |
| Jupiter | NE |
| Venus | SE |
| Saturn | West |
| Rahu | SW |
| Ketu | NW |

If the user's office (or primary workplace) faces / is located in the command planet's power direction → +15 to Conquest Score.

The `success_direction` for the user's command planet is already returned by `GET /api/strategist/dashboard` as `dashboard.success_direction`.

---

## What You Must NOT Touch

| File | Rule |
|---|---|
| `backend/strategist_router.py` | Do NOT modify. Backend already reads `profile.office_direction` and applies Digbala. |
| `backend/strategist_engine.py` | Do NOT modify. |
| `backend/lk_remedies_router.py` | Do NOT modify. |
| Any existing CSS class | Append-only. |

---

## Where the Input Goes

### Option A (preferred) -- Add to the existing `TheStrategistLandingPage.jsx` profile form

`TheStrategistLandingPage.jsx` already has a birth details form (DOB, birth time, city) that posts to `POST /api/strategist/profile`. Add one more field to this form: **"Which direction does your primary workplace face?"**

### Form field spec

```
Label: "Office / Workplace Direction"
Subtext: "Face of your building entrance, or city direction of your primary work location from home."
Input type: radio buttons or a styled select (7 options):
  ○ North    ○ South    ○ East    ○ West
  ○ NE       ○ SE       ○ SW      ○ NW
  ○ Not sure (skip)
```

"Not sure" = do not send the field (omit from POST body). When omitted, the backend treats Digbala as neutral (0 delta).

After the user selects a direction, show a hint:

```
Your command planet [Saturn] has power direction [West].
[If selected West]: ✓ Digbala aligned -- +15 to Conquest Score
[If selected other]: Digbala not aligned
[If "Not sure"]: Set this later to unlock Digbala bonus
```

This hint is purely frontend -- derive it from `dashboard.success_direction` (already in state if dashboard was previously fetched) or calculate it from `DIGBALA_DIRECTIONS` lookup hardcoded in the component.

### POST body extension

Add `office_direction` to the existing `POST /api/strategist/profile` request body:

```js
// existing body:
{ dob: "1990-01-15", tob: "06:30", city: "Mumbai" }

// new body:
{ dob: "1990-01-15", tob: "06:30", city: "Mumbai", office_direction: "West" }
```

**Backend already accepts extra fields silently** (FastAPI ignores unknown Pydantic fields). But we also need to store `office_direction` in the profile. Update `StrategistProfileRequest` in `strategist_router.py`:

**Wait -- CLAUDE.md rule says CC does this, not Codex. See CC Integration Note below.**

---

## Deliverables (CD scope only)

| File | Change |
|---|---|
| `frontend/src/pages/strategist/TheStrategistLandingPage.jsx` | Add office direction radio/select field to profile form; add Digbala hint text; include `office_direction` in POST body when set |

**No new files. No backend changes from CD scope.**

---

## CC Integration Note (for Claude Code to apply after CD delivers)

After CD delivers the frontend, CC must update `backend/strategist_router.py`:

1. Add `office_direction: Optional[str] = None` to `StrategistProfileRequest` Pydantic model
2. In `save_strategist_profile()`, add to the `update` dict:
   ```python
   if body.office_direction:
       update["office_direction"] = body.office_direction.strip()
   ```

This is a 2-line backend change. Do NOT issue a separate commission for it.

---

## DIGBALA_DIRECTIONS constant for frontend hint (hardcode in component)

```js
const DIGBALA_DIRECTIONS = {
  Sun: "South", Moon: "North", Mercury: "North", Mars: "South",
  Jupiter: "NE", Venus: "SE", Saturn: "West", Rahu: "SW", Ketu: "NW",
};
```

Use `dashboard.command_planet` (already in state) to look up the user's power direction and drive the hint.

---

## CSS guidance

Style the direction selector to match the existing form fields in `TheStrategistLandingPage.jsx`. Use the existing `.str-landing-*` CSS token classes that are already in the component. No new CSS file needed -- inline the small additions.

The Digbala hint line can be a small `<p>` below the selector, styled with `color: #4caf72` for aligned, `color: #c5a059` for not aligned, `opacity: 0.7` for "not sure".
