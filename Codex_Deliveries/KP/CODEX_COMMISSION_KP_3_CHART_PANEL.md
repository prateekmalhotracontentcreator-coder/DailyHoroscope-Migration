# Codex Commission: KP-3
## KP Oracle -- KP Chart Panel (Reusable Component + Oracle Integration)

> **Thread:** KP Oracle (continue existing KP thread)
> **Issued:** 2026-06-07
> **Status:** READY TO ISSUE
> **Depends on:** LON-2 ✅ CC-VERIFIED 2026-06-07 -- `POST /api/kp/birth-chart` live, `KPChart` TypedDict in `kp_engine.py`

---

## 1. Context (Read First)

**What LON-2 built:** A reusable KP engine foundation layer in `kp_engine.py` -- `KPChart` TypedDict, `build_kp_chart()`, `compute_kp_chart()`, and a stateless `POST /api/kp/birth-chart` endpoint. The Longevity Report now renders this as a collapsible "Your KP Chart" panel (4 sub-tables: planet placements, Placidus cusps, ascendant summary, house significators).

**What KP Oracle currently shows in "Your Cosmic Context":**
- Current Mahadasha · Antardasha (text label only)
- `astro_context` (a Claude-generated free-text string)
- "Add birth details" CTA when birth data is absent

**What KP Oracle does NOT show:**
- KP planet placements (sign, house, nakshatra, sub-lord)
- Placidus cusp table (12 cusps with sub-lords)
- KP significators (which houses each planet signifies)
- Ascendant sub-lord

**The mandate for KP-3:**
> Extract the KP Chart Panel from the Longevity Report into a reusable shared component. Plug it into the KP Oracle page and the Ask Question page. Both call the same engine foundation -- no new backend logic required.

---

## 2. Scope

### Part A -- Extract Shared Component

**New file:** `frontend/src/components/KPChartPanel.jsx`

Extract the KP Chart panel currently inlined in `LongevityReportPage.jsx` (lines ~601-727) into a standalone reusable component:

```jsx
// Props:
// kpChart: KPChart object (from /api/kp/birth-chart or from report output)
// defaultOpen: bool (default false -- collapsed)
// title: string (default "Your KP Chart")
// eyebrow: string (default "Foundation Layer")

export default function KPChartPanel({ kpChart, defaultOpen = false, title, eyebrow }) { ... }
```

The component renders the same 4 sub-tables:
1. Planet Placements (planet, sign, house, nakshatra, star lord, sub-lord)
2. Placidus Cusp Table (house, sign, degree, sub-lord)
3. Ascendant Summary (one-line: sign, degree, ayanamsha, sub-lord)
4. House Significators (planet → houses signified)

**Update `LongevityReportPage.jsx`** to import and use `<KPChartPanel kpChart={kpChart} />` instead of the inlined version. No behavioural change.

---

### Part B -- KP Oracle Page Integration

**File:** `frontend/src/pages/kp/KrishnaOraclePage.jsx`

**Where:** Add a standalone "Your KP Chart" section on the page. This is NOT inside an individual reading -- it is a persistent natal chart panel that appears at the top of the page (below the hero / reading controls, before the reading grid), visible when birth data is present.

**Data source:** Call `POST /api/kp/birth-chart` from the frontend when:
- User is logged in (`user` is present)
- User profile has complete birth data: `birth_date`, `birth_time`, `birth_lat`, `birth_lon`, `birth_timezone` (or equivalent fields from `/api/auth/me`)

Use a `useEffect` + `useState(null)` pattern. On first load, if birth data is complete, call the endpoint and set `kpChart`. Show a loading skeleton while fetching. If birth data is incomplete, show the same "Add birth details" CTA that already exists in the Cosmic Context pillar.

**No new backend endpoint required** -- `POST /api/kp/birth-chart` is already live from LON-2.

**Check what profile fields hold birth location:** The user profile in `scriptural_oracle_router.py` resolves `date_of_birth`, `time_of_birth`, `timezone` from the profile. KP-3 also needs `latitude` and `longitude`. Check `/api/auth/me` response to confirm which fields hold these -- if not present, add them to the profile response (backend change scoped below).

---

### Part C -- Ask Question Page Integration

**File:** `frontend/src/pages/kp/AskQuestionPage.jsx`

The Ask Question endpoint (`POST /api/oracle/krishna-prashnavali/ask`) already accepts `latitude`, `longitude`, `date_of_birth`, `time_of_birth` as optional fields (KP-Sprint2 delivery). 

Add the same `<KPChartPanel>` to `AskQuestionPage.jsx` using the same frontend-driven fetch pattern from Part B. Show it in the "Cosmic Context" section of the answer reveal (after the Mahadasha/Antardasha row, before the meaning block). Collapsed by default.

---

### Part D -- Backend: Ensure lat/lon in Profile Resolve (Conditional)

**Check first:** Does `GET /api/auth/me` return `birth_lat` / `birth_lon` (or equivalent) from the user profile?

- If **yes** → no backend change needed.
- If **no** → add `birth_lat`, `birth_lon`, `birth_timezone_name` to the profile fields returned by `GET /api/auth/me` (small backend change in the auth/profile router). These are needed for the frontend to call `POST /api/kp/birth-chart`.

Scope this check before writing Part B frontend code.

---

## 3. Files to Touch

| File | Change |
|---|---|
| `frontend/src/components/KPChartPanel.jsx` | **NEW** -- extracted reusable component from LongevityReportPage |
| `frontend/src/pages/reports/LongevityReportPage.jsx` | Replace inlined chart panel with `<KPChartPanel>` import |
| `frontend/src/pages/kp/KrishnaOraclePage.jsx` | Add KP Chart Panel section (frontend-driven fetch) |
| `frontend/src/pages/kp/AskQuestionPage.jsx` | Add KP Chart Panel to answer Cosmic Context section |
| `backend/auth_router.py` (or wherever `/api/auth/me` is served) | Add `birth_lat`, `birth_lon`, `birth_timezone_name` to profile response -- **only if not already present** |
| `backend/panchang_router.py` | Bump `ENGINE_VERSION` |

Do NOT touch:
- `backend/kp_engine.py` -- engine is complete from LON-2
- `backend/kp_chart_router.py` -- endpoint is live from LON-2
- `backend/scriptural_oracle_router.py` -- reading logic unchanged
- `backend/knowledge_engine.py` -- interpretation layer, not involved

---

## 4. Acceptance Gates

| # | Gate | Pass Condition |
|---|---|---|
| G-01 | `KPChartPanel.jsx` extracted as standalone component | Component renders correctly when imported in Longevity, KP Oracle, and Ask Question |
| G-02 | LongevityReportPage uses imported component | Inlined panel replaced, behaviour identical |
| G-03 | KP Oracle page shows KP Chart Panel | Panel appears when birth data with lat/lon is present, collapsed by default |
| G-04 | KP Oracle page shows CTA when birth data incomplete | "Add birth details" CTA shown when lat/lon missing |
| G-05 | Ask Question reveal shows KP Chart Panel | Panel appears in Cosmic Context section of answer, collapsed by default |
| G-06 | Frontend call uses `POST /api/kp/birth-chart` (not a new endpoint) | Network tab shows call to `/api/kp/birth-chart` with correct payload |
| G-07 | Frontend production build passes | `CI=true npx craco build` exit 0 |
| G-08 | Backend compiles clean | `python3 -m py_compile` on all modified backend files exit 0 |

---

## 5. Out of Scope for KP-3

| Item | Where it belongs |
|---|---|
| KP Prashna (horary) chart | KP-4 or separate Oracle commission |
| Sub-lord-based question interpretation using KP chart | KP-4 |
| Editing birth details inline in KP Oracle page | Arc Angel pre-fill commission (task_4a5b229a) |
| KP chart in Strategist module | STR future pass |
| PDF/share card of KP chart | LON-3 or future pass |
| KE rule integration | KE gate not cleared -- do not touch `_try_scan_chart` |

---

## 6. Architecture Notes for Codex

- `POST /api/kp/birth-chart` is stateless, no auth, no premium gate. Any logged-in or logged-out user can call it. It is pure computation.
- `KPChart` TypedDict is in `backend/kp_engine.py`. The response shape is documented there and in `AYANAMSHA_DECISION_REGISTER.md`.
- Ayanamsha is always `Krishnamurti` for KP module. Do not change.
- The Longevity Report panel currently uses Temple theme classes (`border-[#d5a14a]/25`, `bg-[#1b1510]`, etc.). The KP Oracle uses its own amber/stone theme (`OracleGlassCard`, `border-amber-200/80`). `KPChartPanel.jsx` should accept a `theme` prop or use neutral classes that work in both contexts -- or use CSS variables already defined in the project.
- `scriptural_oracle_router.py` already has `birth_data_present` flag. KP-3 frontend logic should mirror this gate: show chart only when `birth_data_present` is true AND lat/lon is available.
- The user profile fields for birth location -- check `backend/auth_utils.py` and the `users` collection schema before writing frontend code. The Longevity Report collects lat/lon at generation time (user inputs it in the form). KP Oracle needs these from the stored profile.

---

## 7. Suggested Commit Sequence

```
refactor(longevity): extract KPChartPanel as shared component
feat(kp-oracle): add KP Chart Panel to KrishnaOraclePage
feat(kp-ask): add KP Chart Panel to AskQuestionPage Cosmic Context section
[fix(auth): add birth_lat/birth_lon to /api/auth/me profile response -- if needed]
chore(panchang): bump ENGINE_VERSION to v28-kp3-chart-panel
```

---

*Brief written by Claude Code 2026-06-07*
*Engine foundation: `kp_engine.py` · `kp_chart_router.py` (LON-2)*
*KP Oracle codebase: `KrishnaOraclePage.jsx` · `AskQuestionPage.jsx` · `scriptural_oracle_router.py`*
