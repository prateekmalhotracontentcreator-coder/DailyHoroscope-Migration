# Codex Commission: KE-Sprint3 -- Arc Angel Computation Engine
> Module: Knowledge Engine · Sprint: 3 of 4 · Phase: 1.2
> Issued: 2026-05-17
> Dependencies: KE-Sprint2 ✅ COMPLETE · KE-2A ✅ COMPLETE (both confirmed 2026-05-17)
> Contract reference: `CODEX_KNOWLEDGE_ENGINE_CONTRACT.md` Section 19, TD-23, TD-28, TD-29, TD-30
> Gate: All 5 acceptance criteria in Sprint 2 confirmed passed. INGEST FREEZE lifted. Sprint 3 is fully unblocked.

---

## ⭐ MANDATORY -- Read Before Writing a Single Line

**Architecture Rule (TD-28 -- locked 19 April 2026):**
All live astronomical and dasha computations MUST originate from `backend/vedic_calculator.py` + pyswisseph.
`knowledge_engine.py` is the interpretation layer only. It must NOT contain independent dasha calculators.

**Explicitly stated for this sprint:**
- All dasha/antardasha data must come from `vedic_calculator.py`
- Do NOT add dasha calculation logic to `knowledge_engine.py`
- Do NOT duplicate `calculate_vimshottari_dasha()` or antardasha arithmetic inside `knowledge_engine.py`

**TD-29 Legacy Model baseline (locked):**
When zero KE rules carry `approval_status: "approved"` (current state -- all rules are `pending_human_review`),
Arc Angel period quality defaults to natural benefic/malefic classification:
- Jupiter / Venus / Mercury / Moon → `auspicious`
- Saturn / Mars / Rahu / Ketu / Sun → `inauspicious`
This is already implemented via `_natural_quality()` and `NATURAL_BENEFICS/MALEFICS` constants. Do NOT remove it.

---

## Reconcile First -- What Already Exists

Before writing any new code, run a repo audit. The following is already built and confirmed working:

| Symbol | File | Status |
|---|---|---|
| `compute_arc_angel_windows()` | `knowledge_engine.py` line 1134 | ✅ EXISTS |
| `compute_period_quality_now()` | `knowledge_engine.py` line 966 | ✅ EXISTS |
| `_flatten_antardasha_periods()` | `knowledge_engine.py` line 985 | ✅ EXISTS |
| `_quality_from_rules()` | `knowledge_engine.py` | ✅ EXISTS |
| `_collapse_short_windows()` | `knowledge_engine.py` | ✅ EXISTS |
| `_window_driver()` | `knowledge_engine.py` | ✅ EXISTS |
| `ARC_ANGEL_DOMAIN_SLUGS` (12 slugs) | `knowledge_engine.py` line 162 | ✅ EXISTS |
| `ARC_ANGEL_DOMAIN_LABELS` | `knowledge_engine.py` line 176 | ✅ EXISTS |
| `ARC_ANGEL_BASELINE_CONFIDENCE_PCT = 42` | `knowledge_engine.py` line 218 | ✅ EXISTS |
| `GET /api/knowledge-engine/arc-angel-windows` | `server.py` line 1997 | ✅ EXISTS |
| `compute_dasha_timeline()` | `knowledge_engine.py` line 829 | ⚠️ EXISTS -- TD-28 violation (see G-07 below) |
| `user_arc_angel_profile` collection | MongoDB | ❌ MISSING -- must build (G-09) |
| `GET /api/knowledge-engine/arc-angel-profile/{user_id}` | `server.py` | ❌ MISSING -- must build (G-09) |

**Do not rebuild what exists. Verify it passes its acceptance gate first, then extend.**

---

## Gap G-07 -- Post-Arbitration Period Quality Consumption

### What G-07 Requires

`compute_period_quality_now()` must consume **post-arbitration** output from `engine.scan_chart()` -- not raw matched rules.

Sprint 2 added arbitration: `scan_chart()` now returns rules annotated with `representation_mode`, `tension_blocks`, `c_score`, and converged/synthesized rule sets.

The current route in `server.py` correctly calls:
```python
matched_rules = await engine.scan_chart(chart=chart_data, ...)
domain_rule_map = build_domain_rule_map(matched_rules)
domain_quality_now = compute_period_quality_now(dasha_timeline, domain_rule_map)
```

### G-07 Acceptance Gate

Verify the following -- do not rebuild if already correct:

1. `build_domain_rule_map(matched_rules)` accepts the full post-Sprint-2 `scan_chart()` output (which includes `representation_mode` and `tension_blocks` at the top level). It should only extract per-domain rules -- it must not crash on new Sprint 2 fields.

2. `compute_period_quality_now()` returns a dict keyed by all 12 `ARC_ANGEL_DOMAIN_SLUGS` with each value one of `"auspicious"`, `"inauspicious"`, or `"neutral"`.

3. When zero `approved` rules exist (current state), period quality falls through to `_natural_quality(antardasha_planet)` for each domain. Verify this with a unit test using a mock `scan_chart()` return that has no rules.

**If the existing code already satisfies all 3 points: mark G-07 VERIFIED in your response. No code change needed.**

---

## Gap G-08 -- 10-Year Arc Angel Window Generation

### What G-08 Requires

`compute_arc_angel_windows()` must generate per-domain auspicious/inauspicious windows over a 10-year horizon, using post-arbitration `domain_rule_map` as input.

The function already exists (line 1134). It already filters windows shorter than 90 days. It already formats dates as `YYYY-MM`.

### G-08 Acceptance Gate

Verify the following with a live unit test (use fixed birth data: `1990-05-15`, `10:30`, `New Delhi`):

1. `compute_arc_angel_windows(dasha_timeline, domain_rule_map, horizon_years=10)` returns a dict covering all 12 domain slugs.

2. Each domain entry has `auspicious_periods: list` and `inauspicious_periods: list`. Each period item has exactly three keys: `start` (YYYY-MM), `end` (YYYY-MM), `driver` (non-empty string).

3. At least 4 of the 12 domains have at least one window (either auspicious or inauspicious) over the 10-year horizon.

4. No window is shorter than 90 days.

5. All windows are chronologically sorted (start ascending within each domain).

**If the existing code already satisfies all 5 points: mark G-08 VERIFIED. No code change needed.**

---

## Gap G-07.TD28 -- Fix `compute_dasha_timeline()` Architecture Violation

### The Problem

`compute_dasha_timeline()` in `knowledge_engine.py` (line 829) independently computes antardasha sub-periods from date arithmetic using `_build_sub_dashas()`. This is a TD-28 architecture violation -- antardasha arithmetic belongs in `vedic_calculator.py`, not the interpretation layer.

Currently, `calculate_vimshottari_dasha()` in `vedic_calculator.py` returns only the 9 Mahadasha periods with no antardasha breakdown:
```python
[{planet, start, end, years}, ...]  # no antardashas key
```

The Arc Angel computation requires antardashas. `_flatten_antardasha_periods()` in `knowledge_engine.py` iterates `maha.get("antardashas")` for each maha period.

### The Fix -- Two File Changes

**Step 1: Add `build_dasha_timeline()` to `vedic_calculator.py`**

Add a new function to `vedic_calculator.py` that returns the full dasha timeline with antardasha periods baked in. This function is the single source of truth for dasha + antardasha data:

```python
def build_dasha_timeline(birth_date: str, moon_longitude: float) -> list[dict]:
    """
    Returns the full Vimshottari dasha timeline with antardasha sub-periods.
    This is the authoritative dasha+antardasha source for all modules.
    Do NOT duplicate this logic in knowledge_engine.py.
    
    Each item: {planet, start, end, years, antardashas: [{planet, start, end}]}
    """
    top_level = calculate_vimshottari_dasha(birth_date, moon_longitude)
    timeline = []
    for maha in top_level:
        maha_planet = maha["planet"]
        maha_start = datetime.strptime(maha["start"], "%Y-%m-%d")
        maha_end = datetime.strptime(maha["end"], "%Y-%m-%d")
        maha_total_days = (maha_end - maha_start).days
        maha_years = DASHA_YEARS[maha_planet]
        
        # Build antardasha sequence starting from the same Mahadasha lord
        lord_idx = DASHA_ORDER.index(maha_planet)
        antardashas = []
        cursor = maha_start
        for i in range(9):
            antar_lord = DASHA_ORDER[(lord_idx + i) % 9]
            antar_years = DASHA_YEARS[antar_lord]
            antar_fraction = antar_years / maha_years
            antar_days = int(maha_total_days * antar_fraction)
            antar_end = cursor + timedelta(days=antar_days)
            if antar_end > maha_end:
                antar_end = maha_end
            antardashas.append({
                "planet": antar_lord,
                "start": cursor.strftime("%Y-%m-%d"),
                "end": antar_end.strftime("%Y-%m-%d"),
            })
            cursor = antar_end
        # Ensure last antardasha end aligns exactly with maha end
        if antardashas:
            antardashas[-1]["end"] = maha["end"]
        
        timeline.append({
            "planet": maha_planet,
            "start": maha["start"],
            "end": maha["end"],
            "years": maha["years"],
            "antardashas": antardashas,
        })
    return timeline
```

**Step 2: Update the Arc Angel route in `server.py`**

Replace the call to `compute_dasha_timeline(chart_data)` with `build_dasha_timeline(birth_date, moon_longitude)`:

```python
from vedic_calculator import calculate_vedic_chart, build_dasha_timeline

# In the route handler -- replace:
#   dasha_timeline = compute_dasha_timeline(chart_data)
# With:
moon_longitude = chart_data.get("moon_longitude_raw")   # see note below
dasha_timeline = build_dasha_timeline(birth_date, moon_longitude)
```

**Note:** `calculate_vedic_chart()` currently does NOT expose `moon_longitude` in its return dict. You must also add `"moon_longitude": moon_lon` to the return dict in `calculate_vedic_chart()` (line ~1130 in `vedic_calculator.py`, inside the return block). This is a one-line addition to the existing return dict -- do not modify any calculation logic.

**Step 3: Deprecate in `knowledge_engine.py`**

- Remove `_build_sub_dashas()` -- it is replaced by `build_dasha_timeline()` in `vedic_calculator.py`.
- Refactor `compute_dasha_timeline()` to a thin shim or remove it. If other callers exist in the codebase, have them import `build_dasha_timeline` from `vedic_calculator` instead.
- Add a comment at the deletion site: `# Removed: TD-28 -- moved to vedic_calculator.build_dasha_timeline()`

### G-07.TD28 Acceptance Gate

1. `vedic_calculator.build_dasha_timeline("1990-05-15", 123.45)` returns a list of 9 dicts, each with `{planet, start, end, years, antardashas}`, where `antardashas` has exactly 9 entries, and the last antardasha `end` equals the maha `end`.

2. `_build_sub_dashas()` is removed from `knowledge_engine.py`.

3. `compute_dasha_timeline()` is either removed from `knowledge_engine.py` or reduced to a one-line import shim calling `build_dasha_timeline`.

4. The arc-angel-windows route in `server.py` no longer calls `compute_dasha_timeline()`.

5. `calculate_vedic_chart()` return dict includes `"moon_longitude"` key.

---

## Gap G-09 -- `user_arc_angel_profile` MongoDB Persistence

### What G-09 Requires

The Arc Angel profile must be **persisted to MongoDB** on every compute, not just returned in-flight.
Currently the route computes and returns but never writes to DB. This is the main missing piece.

### MongoDB Collection: `user_arc_angel_profile`

Collection name: `user_arc_angel_profile` (already listed in contract Section 19)
Database: `horoscope_db`

**Confidence architecture (locked 2026-05-17):**
```
Foundation  40%  →  Vedic Astrology Engine (DOB + time + place)
Pillar 1   +24%  →  Questionnaire: 12 Focus Areas × 2% per area (all 3 Q's answered)
                     Social Sphere is 6 of the 12 areas (its 12% is carved from the 24%)
Pillar 2   +12%  →  Individual Reports: 1% per IR run + fed back (max 12 IRs)
Pillar 3   +10%  →  Daily Rituals: Tarot/Love 5% + The Strategist 5%
                     Dynamic -- maintained by daily ritual, decays after 3-day miss
Cap         86%  →  100% is architecturally impossible (epistemic honesty)
```

Schema (upsert on every compute when user_id is provided):

```json
{
  "user_id": "string (from auth)",
  "birth_date": "YYYY-MM-DD",
  "birth_time": "HH:MM",
  "birth_place": "string",
  "computed_at": "ISO 8601 UTC",
  "engine_label": "Vedic Astrology Engine Activated",
  "overall_confidence_pct": 40,
  "pillar_1": {
    "areas_completed": [],
    "social_sphere_areas_completed": [],
    "score": 0,
    "max_score": 24
  },
  "pillar_2": {
    "reports_run": [],
    "score": 0,
    "max_score": 12
  },
  "pillar_3": {
    "tarot_love_score": 0,
    "strategist_score": 0,
    "pillar_3_score": 0,
    "last_ritual_date": null,
    "decay_started_at": null,
    "max_score": 10,
    "note": "Decay engine wired in ARC-2. Sprint 3 reads stored pillar_3_score only."
  },
  "domains": [
    {
      "domain_id": "career",
      "domain_label": "Career & Work",
      "period_quality": "auspicious",
      "confidence_pct": 40,
      "period_indicator": "Jupiter AD in Saturn MD -- career auspicious period",
      "auspicious_periods": [
        { "start": "2026-06", "end": "2028-11", "driver": "Jupiter AD -- career expansion" }
      ],
      "inauspicious_periods": [],
      "last_updated": "ISO 8601 UTC"
    }
    // ... 11 more domains
  ]
}
```

### Upsert Logic

```python
async def upsert_arc_angel_profile(db, user_id: str, profile_data: dict):
    await db.user_arc_angel_profile.update_one(
        {"user_id": user_id},
        {"$set": profile_data},
        upsert=True
    )
```

### Cache Rule

If a profile already exists for this user and `computed_at` is less than 6 hours ago **and** `data_completeness` is unchanged: return the stored profile without recomputing.

### Route Changes to `server.py`

**Existing route -- extend (do NOT replace):**

```
GET /api/knowledge-engine/arc-angel-windows
```

Add an optional `user_id` query parameter (string, optional). Behaviour:
- If `user_id` provided AND cached profile is fresh (< 6h, same data_completeness): return stored profile.
- Otherwise: compute as now, then upsert to `user_arc_angel_profile`, then return.

**New route -- add:**

```
GET /api/knowledge-engine/arc-angel-profile/{user_id}
```

Returns the stored `user_arc_angel_profile` document for this user without recomputing. Raises `404` if no profile exists yet (client should call `arc-angel-windows` first). Returns the full schema as defined above.

### Confidence Scoring for Phase 1

`overall_confidence_pct` is computed by `_compute_confidence(profile: dict) -> int`.

**Architecture (Temple Team locked 2026-05-17):**
- Foundation = Vedic Astrology Engine. Label shown to user: `"Vedic Astrology Engine Activated"`.
- Case studies are internal KE accuracy benchmarks (equivalent of DrikPanchang verification for Panchang). They do NOT contribute to user confidence score.
- Pillar 3 decay is managed by ARC-2. Sprint 3 reads `pillar_3_score` from stored profile only.

```python
# Confidence formula constants (Temple Architecture -- locked 2026-05-17)
CONFIDENCE_BASE = 40         # Vedic Astrology Engine activated. Label: "Vedic Astrology Engine Activated"
PILLAR_1_PER_AREA = 2        # +2% per Focus Area fully answered (all 3 Q's). Max 12 × 2 = 24%
                              # Social Sphere = 6 of the 12 areas (their 12% is carved from the 24%)
PILLAR_2_PER_IR = 1          # +1% per Individual Report generated + fed back to Arc Angel. Max 12 × 1 = 12%
PILLAR_3_MAX = 10            # Tarot/Love 5% + The Strategist 5%. Dynamic -- managed by ARC-2 decay engine
CONFIDENCE_CAP = 86          # Hard ceiling. 100% is architecturally impossible (epistemic honesty)


def _compute_confidence(profile: dict) -> int:
    score = CONFIDENCE_BASE

    # Pillar 1: Questionnaire -- 2% per Focus Area fully completed (all 3 Q's answered)
    # Social Sphere areas are 6 of the 12 areas -- their score is already inside this total
    areas_completed = (profile.get("pillar_1") or {}).get("areas_completed") or []
    score += min(len(areas_completed), 12) * PILLAR_1_PER_AREA

    # Pillar 2: Individual Reports -- 1% per IR run and fed back to Arc Angel
    reports_run = (profile.get("pillar_2") or {}).get("reports_run") or []
    score += min(len(reports_run), 12) * PILLAR_2_PER_IR

    # Pillar 3: Daily Rituals -- read stored score; decay engine wired in ARC-2
    pillar_3_score = (profile.get("pillar_3") or {}).get("pillar_3_score", 0)
    score += min(int(pillar_3_score), PILLAR_3_MAX)

    return min(score, CONFIDENCE_CAP)
```

Per-domain `confidence_pct` equals `overall_confidence_pct` for Phase 1 (uniform). Phase 2 will differentiate per domain based on which areas and reports relate to that domain.

**Pillar 3 decay rules (stored in schema, activated by ARC-2):**
- Daily ritual completed → score maintained
- Day 1-2 miss → grace period, no decay (notification: motivational)
- Day 3+ miss → decay begins toward 0 (notification: score-dip-risk alert)
- Score floor: 0 (never negative)
- Ritual resumes → tiered recovery (gradual re-earn, not instant restore)
- Sprint 3 task: store `last_ritual_date` + `decay_started_at` fields. ARC-2 activates the decay job.

### G-09 Acceptance Gates

1. Calling `GET /api/knowledge-engine/arc-angel-windows?birth_date=1990-05-15&birth_time=10:30&birth_place=New+Delhi&user_id=test_sprint3_user` creates (or updates) a document in `user_arc_angel_profile` with the correct 3-pillar schema.

2. `GET /api/knowledge-engine/arc-angel-profile/test_sprint3_user` returns the stored document including all 12 domains, `engine_label`, `overall_confidence_pct`, `pillar_1`, `pillar_2`, `pillar_3` fields.

3. A second call to `arc-angel-windows` within 6 hours for the same `user_id` (same pillar data) returns the cached profile without recomputing (confirm via response field `"cached": true`).

4. Calling `arc-angel-windows` without `user_id` still works as before -- no persistence, no crash.

5. Formula verification:
   - Birth data only, no questionnaire, no reports, no rituals → `_compute_confidence(...)` = `40`
   - All 12 areas answered, no reports, no rituals → `40 + 24 = 64`
   - All 12 areas + all 12 IRs + full ritual score → `min(40 + 24 + 12 + 10, 86) = 86`
   - `engine_label` field = `"Vedic Astrology Engine Activated"` always present.

---

## Full Acceptance Test Suite (All 3 Gaps)

Write these as pytest tests in `tests/test_ke_sprint3_arc_angel.py`. All tests must pass before marking Sprint 3 complete.

### G-07 Tests

```python
def test_period_quality_now_returns_all_12_domains():
    # compute_period_quality_now with empty domain_rule_map
    # expect: all 12 ARC_ANGEL_DOMAIN_SLUGS present, each value in {auspicious,neutral,inauspicious}

def test_period_quality_falls_back_to_natural_quality_when_no_approved_rules():
    # mock scan_chart returning 0 approved rules
    # active antardasha planet = Jupiter → expect 'auspicious' for all domains

def test_period_quality_inauspicious_for_saturn_antardasha():
    # active antardasha = Saturn, no approved rules
    # expect 'inauspicious' for all domains

def test_build_domain_rule_map_tolerates_sprint2_arbitration_fields():
    # scan_chart output includes representation_mode, tension_blocks, c_score
    # build_domain_rule_map must not raise; must return valid dict
```

### G-08 Tests

```python
def test_arc_angel_windows_covers_all_12_domains():
    # compute_arc_angel_windows with known dasha_timeline, empty domain_rule_map
    # expect: all 12 slugs present in result

def test_arc_angel_windows_no_window_shorter_than_90_days():
    # all windows in output must span >= 90 calendar days

def test_arc_angel_windows_periods_have_required_keys():
    # each period item must have: start (YYYY-MM), end (YYYY-MM), driver (non-empty str)

def test_arc_angel_windows_sorted_chronologically():
    # within each domain, auspicious_periods and inauspicious_periods sorted by start ascending
```

### G-07.TD28 Tests

```python
def test_build_dasha_timeline_returns_9_maha_periods():
    result = build_dasha_timeline("1990-05-15", 123.45)
    assert len(result) == 9

def test_build_dasha_timeline_each_maha_has_9_antardashas():
    result = build_dasha_timeline("1990-05-15", 123.45)
    for maha in result:
        assert len(maha["antardashas"]) == 9

def test_build_dasha_timeline_antardasha_end_aligns_with_maha_end():
    result = build_dasha_timeline("1990-05-15", 123.45)
    for maha in result:
        assert maha["antardashas"][-1]["end"] == maha["end"]

def test_compute_dasha_timeline_removed_or_shim():
    # If compute_dasha_timeline still exists in knowledge_engine, it must not contain
    # _build_sub_dashas logic -- it must delegate to vedic_calculator.build_dasha_timeline
    pass
```

### G-09 Tests (unit -- mock MongoDB)

```python
def test_compute_confidence_base_only():
    # Birth data entered, no questionnaire, no IRs, no rituals
    profile = {"pillar_1": {"areas_completed": []},
               "pillar_2": {"reports_run": []},
               "pillar_3": {"pillar_3_score": 0}}
    assert _compute_confidence(profile) == 40

def test_compute_confidence_all_questionnaire_areas():
    # All 12 Focus Areas completed, no IRs, no rituals
    all_areas = ["health", "career", "finances", "learning", "emotional",
                 "spirituality", "relationships", "family", "social",
                 "adventure", "environment", "creativity"]
    profile = {"pillar_1": {"areas_completed": all_areas},
               "pillar_2": {"reports_run": []},
               "pillar_3": {"pillar_3_score": 0}}
    assert _compute_confidence(profile) == 64  # 40 + 24

def test_compute_confidence_partial_questionnaire():
    # 6 areas answered = +12%
    profile = {"pillar_1": {"areas_completed": ["health", "career", "finances",
                                                 "learning", "emotional", "spirituality"]},
               "pillar_2": {"reports_run": []},
               "pillar_3": {"pillar_3_score": 0}}
    assert _compute_confidence(profile) == 52  # 40 + 12

def test_compute_confidence_with_irs():
    # 6 areas + 6 IRs
    profile = {"pillar_1": {"areas_completed": ["health", "career", "finances",
                                                 "learning", "emotional", "spirituality"]},
               "pillar_2": {"reports_run": ["brihat_kundali", "numerology", "longevity",
                                             "kp_oracle", "tarot", "palmistry"]},
               "pillar_3": {"pillar_3_score": 0}}
    assert _compute_confidence(profile) == 58  # 40 + 12 + 6

def test_compute_confidence_cap_at_86():
    # Fully engaged user -- must never exceed 86
    all_areas = ["health", "career", "finances", "learning", "emotional",
                 "spirituality", "relationships", "family", "social",
                 "adventure", "environment", "creativity"]
    all_irs = ["brihat_kundali", "numerology", "longevity", "kp_oracle",
               "tarot", "palmistry", "lk", "love", "ir1", "ir2", "ir3", "ir4"]
    profile = {"pillar_1": {"areas_completed": all_areas},
               "pillar_2": {"reports_run": all_irs},
               "pillar_3": {"pillar_3_score": 10}}
    assert _compute_confidence(profile) == 86  # min(40+24+12+10, 86)

def test_engine_label_always_present():
    # Profile doc must always have engine_label field
    # build_arc_angel_profile_doc() → doc["engine_label"] == "Vedic Astrology Engine Activated"
    pass

def test_arc_angel_profile_schema_has_12_domains():
    # build_arc_angel_profile_doc() returns a doc with len(domains) == 12
    pass

def test_arc_angel_profile_each_domain_has_required_fields():
    # domain_id, domain_label, period_quality, confidence_pct,
    # period_indicator, auspicious_periods, inauspicious_periods, last_updated
    pass

def test_pillar_3_decay_fields_present_in_schema():
    # profile["pillar_3"] must contain: pillar_3_score, last_ritual_date,
    # decay_started_at, tarot_love_score, strategist_score
    pass
```

---

## Files to Modify

```
backend/vedic_calculator.py        ← ADD: build_dasha_timeline(), ADD moon_longitude to return dict
backend/knowledge_engine.py        ← REMOVE: _build_sub_dashas(), refactor compute_dasha_timeline()
                                      ADD: _compute_confidence(), build_arc_angel_profile_doc()
backend/server.py                  ← EXTEND: arc-angel-windows route (user_id param + upsert)
                                      ADD: GET /api/knowledge-engine/arc-angel-profile/{user_id}
tests/test_ke_sprint3_arc_angel.py ← NEW: all tests above
```

**Do NOT touch:**
```
backend/panchang_router.py
frontend/                          (zero frontend changes in this commission)
```

---

## What Comes Next (Sprint 4 -- do not build in this commission)

Sprint 4 = KE-IQ (G-10): Questionnaire UI + β/γ multiplier wiring.
Brief already written: `CODEX_COMMISSION_KE_IQ_QUESTIONNAIRE_UI.md`.
Sprint 4 can run in parallel with ARC-2 (confidence % dynamic scoring from questionnaire).
Issue when Sprint 3 gate passes.

---

## Delivery Format

**Single diff touching only the files listed above.**
Commit message: `feat(knowledge-engine): Sprint 3 -- Arc Angel persistence + TD-28 dasha fix`

**Delivery checklist:**
- [ ] G-07 acceptance gate: VERIFIED (code change or no-op confirmed)
- [ ] G-08 acceptance gate: VERIFIED (code change or no-op confirmed)
- [ ] G-07.TD28: `build_dasha_timeline()` added to `vedic_calculator.py`
- [ ] G-07.TD28: `moon_longitude` added to `calculate_vedic_chart()` return dict
- [ ] G-07.TD28: `_build_sub_dashas()` removed from `knowledge_engine.py`
- [ ] G-09: `user_arc_angel_profile` upsert on compute (when user_id provided)
- [ ] G-09: GET `/api/knowledge-engine/arc-angel-profile/{user_id}` route live
- [ ] G-09: Cache rule implemented (< 6h + same data_completeness → return stored)
- [ ] G-09: `_compute_confidence()` implemented with locked 3-pillar formula (base 40, Pillar 1 +2/area, Pillar 2 +1/IR, Pillar 3 read-from-stored, cap 86)
- [ ] G-09: `engine_label: "Vedic Astrology Engine Activated"` field present in all profile docs
- [ ] G-09: `pillar_3` schema fields present (`tarot_love_score`, `strategist_score`, `pillar_3_score`, `last_ritual_date`, `decay_started_at`) -- values default 0/null for Phase 1
- [ ] All pytest tests in `tests/test_ke_sprint3_arc_angel.py` pass
- [ ] No existing tests broken (run full test suite before delivery)
