# Codex Thread Summary — Arc Angel UI Panel

To: New Codex Thread
From: Knowledge Engine Thread
Date: 18 April 2026 (updated: 19 April 2026 — response shape corrected, amendments logged)
Status: READY FOR NEW THREAD — UI panel (ArcAngelPanel.jsx) already delivered and live

## Purpose

This summary is the handoff note for the next thread focused on the Arc Angel UI panel.
The backend prerequisites from Knowledge Engine Phase 1.2 Sprints 1–3 are now in place.

Recommended next thread scope:
- Arc Angel left-nav / profile UI
- frontend wiring to the new Arc Angel backend output
- any lightweight backend shape adjustments needed strictly for UI consumption

Recommended not to mix into this thread:
- Numerology issues
- unrelated module UI work
- new scoring-model changes beyond the locked contract

## Recommendation

Open a new thread for Arc Angel UI.

Reason:
- the backend scoring and arbitration work is now substantial and complete enough to treat as dependency context
- the next work is cross-cutting but primarily UI/integration focused
- a fresh thread will keep acceptance, review, and handoff cleaner

## Source Of Truth Files

New thread should review these first:

1. `/Users/apple/DailyHoroscope-Migration/.claude/CODEX_KNOWLEDGE_ENGINE_CONTRACT.md`
2. `/Users/apple/DailyHoroscope-Migration/CODEX_MASTER_ROADMAP.md`
3. `/Users/apple/DailyHoroscope-Migration/backend/knowledge_engine.py`
4. `/Users/apple/DailyHoroscope-Migration/backend/knowledge_schema.py`
5. `/Users/apple/DailyHoroscope-Migration/backend/server.py`

If the UI brief references prior Sprint decisions, also review:

6. `/Users/apple/DailyHoroscope-Migration/backend/tranche_filter.py`
7. `/Users/apple/DailyHoroscope-Migration/frontend/src/pages/BrihatKundliPage.jsx`
8. `/Users/apple/DailyHoroscope-Migration/frontend/src/pages/admin/LibraryConsolePage.jsx`

## Current State

### Commission I backend status

CPath-1 is complete.

Phase 1.2 backend status:
- Sprint 1 complete: contextual `alpha/beta/gamma` multipliers wired into `_score_rule()`
- Sprint 2 complete: contradiction scoring, representation mode selection, tension block generation, and supersession lookup runtime
- Sprint 3 complete: Arc Angel period-quality computation and 10-year window generation

### Latest relevant commit

Sprint 3 commit:
- `9d35140` — `feat(knowledge-engine): implement sprint 3 arc angel runtime`

Recent supporting commits:
- `57e347a` — Sprint 1 contextual multipliers + TD-26 / TD-27 contract update
- `9915b60` — Sprint 2 arbitration runtime

## What Sprint 3 Added

### In `/Users/apple/DailyHoroscope-Migration/backend/knowledge_engine.py`

Added:
- `compute_dasha_timeline(chart)`
- `assign_period_quality(rule, dasha_timeline, as_of=None)`
- `compute_period_quality_now(dasha_timeline, domain_matched_rules, as_of=None)`
- `compute_arc_angel_windows(dasha_timeline, domain_matched_rules, horizon_years=10, as_of=None)`
- `build_domain_rule_map(matched_rules)`

Updated:
- `KnowledgeEngine.scan_chart(...)`
  - new optional param: `dasha_timeline`
  - each matched rule now gets `period_quality`

Supporting additions:
- Arc Angel domain slug constants
- category-to-domain-slug mapping
- window merge/collapse logic so no output periods under 3 months remain

### In `/Users/apple/DailyHoroscope-Migration/backend/server.py`

Added endpoint:
- `GET /api/knowledge-engine/arc-angel-windows`

Query params:
- `birth_date` required
- `birth_time` required
- `birth_place` required
- `horizon_years` optional, default `10`, max `20`

Response shape (**updated 19 April 2026** — commit `cae440e`):

```json
{
  "overall_confidence_pct": 42,
  "domain_quality_now": {
    "health": "auspicious",
    "career": "neutral",
    "finances": "inauspicious"
  },
  "arc_angel_windows": [
    {
      "domain_id": "health",
      "domain_label": "Health & Fitness",
      "auspicious_periods": [
        {
          "start": "2026-06",
          "end": "2028-11",
          "driver": "Jupiter AD in Mars MD — health expansion"
        }
      ],
      "inauspicious_periods": [],
      "period_quality_now": "auspicious",
      "confidence_pct": 42
    }
  ]
}
```

Note: `arc_angel_windows` is a **list** (not a dict). Each item includes `domain_id`, `domain_label`, `period_quality_now`, and `confidence_pct`. `overall_confidence_pct` is always 42 in Phase 1 (birth data only baseline).

## Arc Angel Domain Contract

Use these exact 12 slugs in UI/backend integration:

- `health`
- `career`
- `finances`
- `learning`
- `emotional`
- `spirituality`
- `relationships`
- `family`
- `social`
- `adventure`
- `environment`
- `creativity`

Human labels already mapped in backend:
- Health & Fitness
- Career & Work
- Finances
- Intellectual Life & Learning
- Emotional Life
- Spirituality
- Love Relationships
- Family Life
- Social Life & Friendship
- Adventure & Travel
- Environment
- Creativity & Hobbies

## Important Backend Notes

### 1. The brief and live code diverged slightly

The Sprint 3 brief referenced:
- existing `compute_dasha_timeline()`
- `vedic_calculator.get_birth_chart()`

In the real codebase:
- `compute_dasha_timeline()` did not exist and was added in Sprint 3
- the endpoint uses existing `calculate_vedic_chart()` instead

This is intentional and already implemented.

### 2. Arc Angel logic consumes post-arbitration output

This is important.

The Arc Angel helpers are intended to consume rule payloads after:
- scoring
- arbitration
- tranche adjustment

For UI work, do not rebuild domain logic from raw library rules unless there is a very specific reason.

### 3. Current endpoint is stateless

The new endpoint computes from birth input on demand.
It does not yet persist a `user_arc_angel_profile` document in this sprint.

That means the next thread may need to decide whether Arc Angel UI should:
- call the endpoint live and render transient data, or
- add a persistence layer and hydrate the UI from stored profile documents

That depends on the UI brief and Phase 1.2 scope boundary.

## Schema Context

Relevant models already exist in:
- `/Users/apple/DailyHoroscope-Migration/backend/knowledge_schema.py`

Look at:
- `ArcAngelPeriod`
- `ArcAngelDomainSnapshot`
- `UserArcAngelProfileDocument`
- `PeriodQuality`

Current important fields:
- `ArcAngelDomainSnapshot.period_quality_now`
- `ArcAngelDomainSnapshot.auspicious_periods`
- `ArcAngelDomainSnapshot.inauspicious_periods`
- `ArcAngelDomainSnapshot.confidence_pct`

Note:
- Sprint 3 computes the period-quality and windows runtime payload
- it does not yet populate `UserArcAngelProfileDocument` automatically

## Validation Already Done

Validated in the Knowledge Engine thread:
- AST parse passed for `knowledge_engine.py` and `server.py`
- import passed for `knowledge_engine.py`
- smoke tests passed for:
  - `assign_period_quality()`
  - `compute_period_quality_now()`
  - `compute_arc_angel_windows()`

Known environment caveat:
- validator script still hits the known sandbox `__pycache__` write issue in this desktop environment
- no-bytecode validation path was used successfully

## Likely UI Questions For Next Thread

The new thread should answer these early:

1. Should Arc Angel UI call the new endpoint directly, or should backend first persist `user_arc_angel_profile`?
2. Where does the Arc Angel panel live first:
   - left nav inside an existing report page
   - standalone panel
   - reusable shell component for multiple report modules
3. What is the gating behavior when subscription or birth data is missing?
4. ~~How should `confidence_pct` be computed or surfaced if the current endpoint does not yet emit it?~~ **RESOLVED** — endpoint now emits `confidence_pct: 42` per domain and `overall_confidence_pct: 42` (commit `cae440e`)
5. Should the UI render all 12 domains always, even with empty periods? The backend currently returns all 12.

## Arc Angel UI — Live State (19 April 2026)

The Arc Angel UI panel is already delivered and live. Any future thread iteration should treat this as the baseline, not start from scratch.

### Files delivered and live on `main`

| File | Status | Commit |
|---|---|---|
| `frontend/src/components/ArcAngelPanel.jsx` | ✅ Live | `c01ec8d` |
| `frontend/src/components/NavBar.jsx` | ✅ Updated | `c01ec8d` |
| `frontend/src/pages/ArcAngelPage.jsx` | ✅ Live (full detail view) | `1d05230` |

### What ArcAngelPanel.jsx does

- Collapsible "Janma Kundali Snapshot" in the NavBar mobile drawer (top item, logged-in users only)
- Fetches birth profile from `GET /api/profile/birth` → uses `date_of_birth`, `time_of_birth`, `location`
- Calls `GET /api/knowledge-engine/arc-angel-windows?birth_date=&birth_time=&birth_place=`
- Renders 4-column table: Domain | Auspicious Periods | Inauspicious Periods | Confidence % (SVG donut)
- Left border colour: green (auspicious) / red (inauspicious) / grey (neutral)
- Loading skeletons, API error state, no-birth-data prompt → links to `/account`
- Footer: "View full 10-year outlook →" links to `/arc-angel`

### Amendments made to Codex deliverable after delivery (RULE 9 — for next iteration awareness)

The following corrections were applied to `ArcAngelPanel.jsx` before going live:
1. `subscription` removed from `useAuth()` — AuthContext does not expose it
2. Birth data source changed: `user.birth_date` / `user.birth_lat` etc. → `GET /api/profile/birth` response fields
3. API params corrected: `birth_lat`/`birth_lon`/`timezone` → `birth_place` (city string matching backend)

### What remains for future iterations

- Premium gate on Auspicious/Inauspicious period columns (currently shows data to all logged-in users — Phase 1 decision)
- Persist `user_arc_angel_profile` in MongoDB (currently stateless — computed on demand)
- Confidence % growth as user runs more modules / fills questionnaire
- Desktop sidebar integration (current panel is mobile drawer only)

---

## Suggested Starting Point For The New Thread

Suggested kickoff ask:

"Implement Arc Angel UI panel using the existing Knowledge Engine Sprint 3 backend. Start by reviewing `CODEX_ARC_ANGEL_UI_THREAD_SUMMARY.md`, `CODEX_KNOWLEDGE_ENGINE_CONTRACT.md`, `knowledge_engine.py`, `knowledge_schema.py`, and `server.py`. Confirm whether the panel should use transient endpoint data or persist `user_arc_angel_profile`, then build the UI against the locked 12-domain contract."

## What Not To Reinvestigate

These are already settled unless a new brief explicitly reopens them:
- Sprint 1 contextual multiplier math
- Sprint 2 contradiction/runtime arbitration architecture
- TD-26 Country Kundali as alpha signal
- TD-27 Forecast Tier / Life Area Outlook
- Numerology render issue handling in this thread

## Thread Boundary Reminder

Numerology-related updates should remain in the original Numerology thread.
This new thread should stay centered on Arc Angel / Knowledge Engine UI integration.
