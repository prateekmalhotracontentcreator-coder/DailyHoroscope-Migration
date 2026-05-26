# Codex Commission -- STR-R03: Pitru Rin Ledger

> Module: The Strategist
> Closes: War Room `pitruRin: []` hardcoded placeholder
> Depends on: STR-R01 ✅
> Stack: FastAPI + React 18 + Tailwind + MongoDB
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Issued: 2026-05-26

---

## The Gap Being Closed

`StrategistWarRoomPage.jsx` → `mapWarRoomProps()` returns `pitruRin: []` -- hardcoded.
`PitruRinLedger.jsx` (inside StrategistWarRoom) receives this empty array and renders "No active ancestral debt detected" regardless of the user's actual Gate 1 diagnosis.

Gate 1 data already exists in `strategist_router.py` (`gate1.records[]`). This commission:
1. Maps `gate1.records` to the `PitruRinRow` debt shape (backend)
2. Adds `pitru_rin_ledger` to the dashboard response (backend)
3. Wires `pitruRin` in `mapWarRoomProps` (frontend)

---

## What You Must NOT Touch

| File | Rule |
|---|---|
| `frontend/src/components/strategist/war-room/StrategistWarRoom.jsx` | DO NOT modify |
| `frontend/src/components/strategist/war-room/PitruRinLedger.jsx` | DO NOT modify |
| `backend/vedic_calculator.py` | DO NOT touch |
| `backend/strategist_engine.py` | DO NOT touch |
| `backend/lk_diagnostics.py` | DO NOT modify |

---

## PitruRinRow Debt Shape (what the frontend component expects)

```javascript
{
  id: string,           // unique per debt row
  name: string,         // debt name / planet label
  type: string,         // e.g. "Ancestral" | "Karmic" | "Paternal"
  severity: "high" | "medium" | "low",
  ritual: string,       // prescribed remedy text
  streakDays: number,   // days of continuous remedy (0 if not started)
  daysSinceRitual: number, // days since last ritual log (null if never)
  cleared: boolean,     // true when resolved
}
```

---

## Deliverables (2 files)

### File 1 -- `backend/strategist_router.py`

**Add `_map_gate1_to_ledger()` helper** (add before `_build_war_room_state`):

```python
def _map_gate1_to_ledger(gate1: dict) -> list[dict]:
    """
    Maps Gate 1 knowledge_rules records to PitruRinRow debt shape.
    Returns [] if no active debt.
    """
    if not gate1.get("active_pitru_rin"):
        return []

    records = gate1.get("records", [])
    ledger = []
    for i, rec in enumerate(records[:5]):   # cap at 5 displayed debts
        severity_score = rec.get("severity", 2)
        if severity_score >= 4:
            sev = "high"
        elif severity_score >= 2:
            sev = "medium"
        else:
            sev = "low"

        ledger.append({
            "id": rec.get("id", f"debt-{i}"),
            "name": rec.get("title") or rec.get("planet", "Ancestral Debt"),
            "type": rec.get("debt_type") or "Ancestral",
            "severity": sev,
            "ritual": rec.get("remedy") or rec.get("full_text") or "Perform ancestral remedy as prescribed.",
            "streakDays": 0,          # streak tracking is in lk_tracker collection -- stub for now
            "daysSinceRitual": None,  # same
            "cleared": False,
        })
    return ledger
```

**Inside `_build_war_room_state()`**, after the `gate1` extraction line, add:
```python
pitru_rin_ledger = _map_gate1_to_ledger(gate1)
```

Add to return dict:
```python
"pitru_rin_ledger": pitru_rin_ledger,
```

---

### File 2 -- `frontend/src/pages/strategist/StrategistWarRoomPage.jsx`

**Update `mapWarRoomProps`** -- replace the hardcoded line:
```javascript
// BEFORE:
pitruRin: [],

// AFTER:
pitruRin: Array.isArray(dashboard?.pitru_rin_ledger) ? dashboard.pitru_rin_ledger : [],
```

Also update `pitruEmptyMeta` to only show the "no debt" message when the ledger is actually empty AND `pitruDelta` is 0:
```javascript
// BEFORE:
pitruEmptyMeta: pitruActive ? undefined : { message: 'No active ancestral debt detected.' },

// AFTER:
pitruEmptyMeta:
  pitruActive
    ? undefined
    : { message: 'No active ancestral debt detected. Karma is balanced.' },
```

---

## Acceptance Checklist

- [ ] `_map_gate1_to_ledger()` returns `[]` when `active_pitru_rin` is `false`
- [ ] `_map_gate1_to_ledger()` returns up to 5 debt items when active, each with all required shape fields
- [ ] `GET /api/strategist/dashboard` response includes `"pitru_rin_ledger"` array
- [ ] `pitruRin` prop in `mapWarRoomProps` is no longer hardcoded `[]`
- [ ] `PitruRinLedger` renders debt rows when backend returns active Gate 1 records
- [ ] Empty state ("Karma is balanced") renders correctly when no debt
- [ ] No crash when `records` is empty or missing from gate1 response
- [ ] Build: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` → 0 errors
