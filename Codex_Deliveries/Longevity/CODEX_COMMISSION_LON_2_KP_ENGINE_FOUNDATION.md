# Codex Commission: LON-2
## KP Engine Foundation Layer + Longevity Report Phase 2

> **Thread:** Longevity (new thread or continue LON thread)
> **Issued:** 2026-06-07
> **Status:** READY TO ISSUE
> **Depends on:** LON-1 ✅ INTEGRATED · kp_engine.py BSON fixes ✅ committed

---

## 1. Architectural Mandate (Read First)

The current `kp_engine.py` computes a full KP birth chart internally -- Placidus cusps, sub-lords, planet positions, KP chains, significators -- but exposes none of this as a clean, reusable output layer. The Longevity Report consumes it silently and outputs only derived health scores.

**The mandate for LON-2:**
> Build the engine right. Surface a clean KP Chart data layer from `kp_engine.py`. Plug it into the Longevity Report. Other modules (KP Oracle, future reports) will plug into the same foundation via their own threads.

Do NOT patch individual report sections. Fix the engine, then render from the engine output.

---

## 2. Scope

### Part A -- KP Engine Foundation Layer (Backend)

**File:** `backend/kp_engine.py`

The `build_birth_snapshot()` function already computes everything needed. The task is to:

1. **Formalize the KP Chart schema** as a named `TypedDict` or `dataclass` called `KPChart` (or extend `ReportInput`/`ReportOutput` appropriately):

```python
class KPChart(TypedDict):
    ayanamsha: str                        # "Krishnamurti"
    ascendant: dict                       # sign, degree, sub_lord, sub_sub_lord
    cusps: list[dict]                     # 12 entries: house, sign, degree, sub_lord, sub_sub_lord
    planets: dict[str, dict]             # planet → sign, house, degree, nakshatra, star_lord, sub_lord, sub_sub_lord, kp_chain
    significators: dict[str, list[int]]  # planet → [houses it signifies]
    longevity_classification: dict        # score, band, confidence
    current_dasha: dict                   # maha, antar, pratyantar + dates
```

2. **Expose a standalone endpoint** `POST /api/kp/birth-chart` that:
   - Accepts the same `ReportInput` payload (date, time, lat/lon, timezone)
   - Returns `KPChart` as clean JSON
   - Does NOT require premium -- this is the data layer that premium reports build on top of
   - Does NOT persist to MongoDB (stateless computation)

3. **Plug this into `compute_longevity_report()`** -- the existing function already builds this data; restructure it so the `KPChart` dict is explicitly assembled and then passed downstream to the health scoring functions. No logic change -- restructure for clarity and reuse.

4. **Return `kp_chart` as a top-level key** in `compute_longevity_report()` output alongside the existing sections. The Longevity Report frontend will render from this key.

---

### Part B -- Longevity Report Phase 2 (Frontend)

**File:** `frontend/src/pages/reports/LongevityReportPage.jsx`

Add a **KP Birth Chart Panel** as a collapsible section in the Longevity Report. This is not a new section number -- it is a data panel, presented before Section 01, titled **"Your KP Chart"** or **"KP Placements"**.

The panel must display three sub-tables:

#### Sub-table 1: Planet Placements
| Planet | Sign | House | Nakshatra | Star Lord | Sub-Lord |
|---|---|---|---|---|---|
| Sun | Gemini | 10 | Ardra | Rahu | Mars |
| ... | ... | ... | ... | ... | ... |

#### Sub-table 2: Placidus Cusp Table
| House | Cusp Sign | Degree | Sub-Lord |
|---|---|---|---|
| 1 | Virgo | 14°22' | Mercury |
| 2 | Libra | 08°11' | Venus |
| ... | ... | ... | ... |

#### Sub-table 3: Ascendant Summary
One-line: Ascendant sign · Ayanamsha used · Sub-lord of the ascendant cusp.

**UX rules:**
- Collapsed by default. User taps "Show KP Chart" to expand.
- Temple theme: `GlassCard`, `border-gold/20`, `text-muted-foreground` for labels, `text-foreground` for values.
- Mobile-first. Tables must scroll horizontally on small screens.
- No new API call required -- the `kp_chart` data comes from the existing `/api/longevity/generate` response payload.

---

### Part C -- Significators Display (Optional, include if clean)

If the `significators` dict in the engine output is clean after the BSON fix, add a fourth sub-table to the KP Chart Panel:

#### Sub-table 4: House Significators
| Planet | Houses Signified |
|---|---|
| Mars | 1, 6, 8 |
| Saturn | 1, 6, 8, 12 |
| ... | ... |

This is the raw KP significator mapping. It contextualises the health scores already visible in Sections 01-06.

---

## 3. Files to Touch

| File | Change |
|---|---|
| `backend/kp_engine.py` | Add `KPChart` TypedDict, restructure `build_birth_snapshot` output, add `kp_chart` key to `compute_longevity_report()` return |
| `backend/server.py` or new `backend/kp_chart_router.py` | Register `POST /api/kp/birth-chart` endpoint |
| `backend/longevity_router.py` | Pass through `kp_chart` from engine output to API response (it's already in `output_payload`) |
| `frontend/src/pages/reports/LongevityReportPage.jsx` | Add KP Chart Panel (collapsible, 3-4 sub-tables) |
| `backend/panchang_router.py` | Bump `ENGINE_VERSION` |

Do NOT touch:
- `backend/vedic_calculator.py` -- Vedic/Lahiri engine, separate concern
- `backend/knowledge_engine.py` -- interpretation layer only
- Any other report router

---

## 4. Acceptance Gates

| # | Gate | Pass Condition |
|---|---|---|
| G-01 | `POST /api/kp/birth-chart` returns clean JSON | Response has `cusps` (12 entries), `planets` (9+ entries), `ascendant`, `significators` |
| G-02 | All keys in response are strings (no integer keys) | `json.dumps(response)` has zero `"key": <int>` pairs as keys |
| G-03 | Longevity Report renders KP Chart Panel | Panel visible in DOM on report page, collapsed by default |
| G-04 | Planet table has correct columns | sign, house, nakshatra, star_lord, sub_lord present for all 9 planets |
| G-05 | Cusp table has 12 rows | Houses 1-12, each with sign, degree, sub_lord |
| G-06 | Ayanamsha is Krishnamurti in output | `ayanamsha: "Krishnamurti"` confirmed in response |
| G-07 | Frontend production build passes | `CI=true npx craco build` exit 0 |
| G-08 | Backend compiles clean | `python3 -m py_compile kp_engine.py longevity_router.py server.py` exit 0 |

---

## 5. Out of Scope for LON-2

| Item | Where it belongs |
|---|---|
| KP Oracle displaying KP chart | KP-3 (separate KP Oracle thread) -- uses same engine foundation |
| PDF export of KP chart | LON-3 or future pass |
| KP Prashna chart | KP Oracle thread |
| Birth chart editing / re-input within Longevity Report | Arc Angel pre-fill commission (task_4a5b229a) |
| KE rule integration into Longevity | Deferred until TT approves health-category KE rules (KE gate) |

---

## 6. Context for Codex

- `kp_engine.py` uses `swe.SIDM_KRISHNAMURTI` (Krishnamurti ayanamsha) -- this is correct and intentional. Do not change.
- `build_birth_snapshot()` already computes all KP data. The LON-2 task is to surface it, not re-compute.
- All dict keys must be strings (BSON requirement) -- this is already enforced post-LON-1 fixes. Maintain this in any new code.
- The `_slim_payload_for_prompt()` function in `longevity_router.py` trims the payload for the Claude narrative call. Do not pipe the full KP chart into the Claude prompt -- it is for display only.
- `knowledge_engine.py` interpretation rules are NOT active in the Longevity Report (KE gate not cleared). Do not re-enable `_try_scan_chart`.

---

## 7. Suggested Commit Sequence

```
feat(kp-engine): add KPChart TypedDict and expose kp_chart in compute_longevity_report output
feat(kp-chart): add POST /api/kp/birth-chart stateless endpoint
feat(longevity): add KP Chart Panel (cusps + planets + significators) to LongevityReportPage
chore(panchang): bump ENGINE_VERSION to v27-lon2-kp-chart-panel
```

---

*Brief written by Claude Code 2026-06-07 · Architectural direction: TT 2026-06-07*
*Foundation reference: `kp_engine.py` · `AYANAMSHA_DECISION_REGISTER.md`*
