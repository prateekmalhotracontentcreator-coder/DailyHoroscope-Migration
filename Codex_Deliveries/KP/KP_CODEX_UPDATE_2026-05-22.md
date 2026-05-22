# KP Oracle -- Codex Update & KP-2B Commission
> Date: 2026-05-22  
> Applies to: KP-Sprint2 thread (context update) · KP-2B (new commission)  
> Stack: React 18 · FastAPI · MongoDB · Tailwind CSS

---

## Part A -- Critical Fixes Applied Since Last Codex Delivery (Read First)

Two bugs were found and fixed in the live codebase. Codex must not reintroduce either pattern.

### Fix 1 -- Bundle path (backend)

**File:** `backend/scriptural_oracle_router.py` · function `_source_bundle_path()` · commit `0db820b`

**What was wrong:**
```python
# BROKEN -- extra .parent caused path to resolve one level above backend/
Path(__file__).resolve().parent.parent / "assets" / "krishna_oracle" / "krishna_oracle_content.json"
```

**What is correct:**
```python
# CORRECT
Path(__file__).resolve().parent / "assets" / "krishna_oracle" / "krishna_oracle_content.json"
```

**Rule:** Any new file asset path inside `scriptural_oracle_router.py` or any new KP backend file must use `Path(__file__).resolve().parent / "assets" / ...` -- only one `.parent`.

---

### Fix 2 -- Remedy display (frontend)

**File:** `frontend/src/pages/kp/KrishnaOraclePage.jsx` · commit `0db820b`

The report now renders **both** remedy fields -- not OR, AND:

| Label | Source field | What it contains |
|---|---|---|
| **Behavioural Practice** | `answer.behavioral_remedy` | Contemplative shift to adopt internally |
| **Sacred Remedy** | `answer.remedy` | Specific ritual to perform (Hanuman Chalisa, copper vessel, etc.) |

**Current JSX (do not revert):**
```jsx
<div className="grid gap-4 md:grid-cols-2">
  <BilingualBlockView label="What to Do" block={reading.answer.what_to_do} />
  {(reading.summary_report?.behavioral_remedy || reading.answer.behavioral_remedy) && (
    <BilingualBlockView label="Behavioural Practice" block={reading.summary_report?.behavioral_remedy || reading.answer.behavioral_remedy} />
  )}
  <BilingualBlockView label="Precaution" block={reading.answer.precaution} />
  <BilingualBlockView label="Duration" block={reading.answer.duration} />
</div>
{reading.answer.remedy && (
  <BilingualBlockView label="Sacred Remedy" block={reading.answer.remedy} />
)}
```

---

## Part B -- KP-Sprint2 Status (No Change Required from Codex)

KP-Sprint2 (`/ask-question` -- Guna + Gita logic router) is commissioned and in progress. The spec is unchanged. The fixes in Part A do not alter the KP-Sprint2 deliverables.

For reference, the acceptance checklist remains:
- `/ask-question` no longer renders `ComingSoonPage`
- `AskQuestionPage.jsx` mounted at `frontend/src/pages/kp/AskQuestionPage.jsx`
- Route swap: `frontend/src/App.js` line 308 -- replace `ComingSoonPage` with `AskQuestionPage`
- All 20 focus area categories render
- Question validation: 10-200 chars
- Guna classification runs (SATTVA / RAJAS / TAMAS)
- Logic router JSON at `backend/assets/krishna_oracle/ask_question_logic_router.json` -- all 60 combinations
- Dasha enrichment via `vedic_calculator.py` only (not `knowledge_engine.py`)
- 3-card reveal: Verse · Cosmic Context · Practical Action
- Readings persist to `ask_question_readings`
- Free limit: 2 readings/month · Premium: unlimited
- Share and save actions work

**Asset path rule for KP-Sprint2:** The logic router JSON must be read using `Path(__file__).resolve().parent / "assets" / "krishna_oracle" / "ask_question_logic_router.json"` (one `.parent` only -- see Fix 1 above).

---

## Part C -- KP-2B Commission: Ritual Animation + 3-Pillar UX

**Status:** Ready to issue. All blockers cleared.  
**Depends on:** KP-2A ✅ integrated · KP-OP-9 ✅ verified · bundle loading ✅ fixed

### Existing files to modify (do NOT restructure)

| File | Current state |
|---|---|
| `frontend/src/pages/kp/KrishnaOraclePage.jsx` | 712 lines · main page |
| `frontend/src/components/KrishnaOracleGrid.jsx` | grid component |
| `backend/scriptural_oracle_router.py` | router, prefix `/api/oracle/krishna-prashnavali` |
| `backend/vedic_calculator.py` | sole source of all dasha/transit data -- do NOT modify |

### Task 1 -- White Light Meditation Ritual Screen

**Create:** `frontend/src/components/kp/KrishnaRitualScreen.jsx`  
**Props:** `{ onComplete: () => void }`  
**Rendered by:** `KrishnaOraclePage.jsx` above the grid when `!ritualComplete`

**Behaviour:**
- Fires once per browser session -- store completion in `sessionStorage` key `kp_ritual_done`
- Duration: 25-30 seconds, or user taps "I'm ready" to skip immediately
- After completion (timer or skip): ritual overlay fades out, grid fades in (no hard cut)

**Visual:**

Background -- full viewport, `bg-neutral-950`

White orb:
- Starts `w-8 h-8`, white (`bg-white/90`), centered, `border-radius: 50%`, `filter: blur(8px)`
- Expands to `w-64 h-64` over 8s via CSS `@keyframes` (scale transform)
- `opacity` oscillates 0.7-1.0 on 4s cycle (breathing)
- Outer glow: `box-shadow: 0 0 60px 20px rgba(255,255,255,0.08)`

Text overlay (centered, above orb):
```
[small, gold, tracking-widest]          KRISHNA PRASHNAVALI
[large, white, Playfair Display italic] "Close your eyes."
[small, white/60, appears at 5s]        "Breathe in. Visualise a pure white light at your heart centre."
[small, white/60, appears at 12s]       "When you feel a connection, open your eyes and tap your letter."
```

Skip link: `"I'm ready"` -- bottom center, `text-white/40 hover:text-white/70`

Grid: starts `opacity-0`, fades to `opacity-100` as ritual dismisses (1.5s transition).

---

### Task 2 -- 3-Pillar Guidance Report UX

Replace the current flat layout in `KrishnaOraclePage.jsx` with a structured 3-pillar reveal.  
**Keep:** share bar, history link, "Ask again" CTA.  
**Remove:** current flat field dump for oracle answer.

**Pillar 1 -- The Sacred Verse**
```
[Verdict badge -- large, colour-coded per table below]
[chaupai_phrase -- Sanskrit, center, gold, Cinzel font]
[title.english_block -- center, white, subtitle]
[krishna_answer.english_block -- italic, Playfair Display, white/80, center, max 3 lines]
```

Verdict badge colours:
| Verdict | Classes |
|---|---|
| YES | `bg-green-900/40 border-green-500/40 text-green-300` |
| WAIT | `bg-blue-900/40 border-blue-500/40 text-blue-300` |
| NO | `bg-red-900/40 border-red-500/40 text-red-300` |
| PRAY | `bg-purple-900/40 border-purple-500/40 text-purple-300` |

**Pillar 2 -- Cosmic Context**

When birth data present:
```
[Header: "Your Cosmic Context"]
[Dasha line: "You are in [Planet] Mahadasha · [Antardasha] Antardasha"]
[astro_context string from backend]
[meaning.english_block -- "What this means for you"]
```

When birth data absent:
```
[Gold info banner] "Add your birth details to unlock your personal cosmic context."
[Link → /birth-chart]
```

**Pillar 3 -- The Practical Action**
```
[Header: "Your Path Forward"]
[what_to_do.english_block]
[behavioral_remedy.english_block -- label: "Inner shift required:"]
[remedy.english_block -- label: "Sacred Remedy:"]
[precaution.english_block -- label: "Watch for:"]
[duration.english_block -- label: "Timeframe:"]
```

Note: `behavioral_remedy` and `remedy` are distinct fields (see Fix 2 above). Both must appear.

**Layout:** Pillars stacked vertically on mobile. On `md+`: Pillars 2 + 3 side by side, Pillar 1 full width above.  
**Card:** GlassCard for each pillar: `rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`  
**Animation:** `animate-fadeInUp` per pillar, staggered 0.2s delay.

---

### Task 3 -- Astro-Filter Enrichment (Backend)

**File to modify:** `backend/scriptural_oracle_router.py`  
**Architecture rule (non-negotiable):** All dasha data from `vedic_calculator.py` -- import and call only, zero dasha logic inside the oracle router.

**Import to add:**
```python
from vedic_calculator import calculate_vimshottari_dasha, get_current_dasha
```

**When `POST /api/oracle/krishna-prashnavali/select` receives birth data (`date_of_birth`, `time_of_birth`, `latitude`, `longitude`):**

1. Call `calculate_vimshottari_dasha(birth_date, moon_longitude)` -- get dasha timeline
2. Call `get_current_dasha(dashas)` -- get active Mahadasha dict
3. Extract `current_mahadasha_planet`, `current_antardasha_planet`
4. Pass to existing `_claude_enrich_summary()` to generate `astro_context` string (one sentence, ≤20 words, connecting dasha period to oracle verdict)

**Add to response:**
```python
astro_context: str | None = None        # Claude-generated sentence
current_mahadasha: str | None = None    # e.g. "Saturn"
current_antardasha: str | None = None   # e.g. "Mercury"
birth_data_present: bool = False        # tells frontend which Pillar 2 variant to show
```

When birth data absent: all four fields default (None / False). Frontend shows "Add birth details" CTA.

---

### KP-2B Constraints

- Do NOT change `_extract_indices()` (chaupai algorithm)
- Do NOT change the 36-answer bundle or `cell_answer_map`
- Do NOT add dasha calculation logic to `scriptural_oracle_router.py` beyond the import
- Ritual screen skippable -- no user forced to wait
- All new components in `frontend/src/components/kp/`
- Use existing Tailwind tokens and GlassCard pattern
- Asset paths: use `Path(__file__).resolve().parent / "assets" / ...` (one `.parent`)

### KP-2B Acceptance Checklist

- [ ] Ritual screen fires on first oracle access per session; skippable via "I'm ready"
- [ ] White orb expands and pulses over 25s; text lines appear in sequence
- [ ] Grid fades in as ritual dismisses (no hard cut)
- [ ] Ritual skipped on return within same browser session (`sessionStorage`)
- [ ] Reveal shows 3 distinct pillars: Sacred Verse / Cosmic Context / Practical Action
- [ ] Verdict badge colour-coded for all 4 verdicts
- [ ] Pillar 3 shows both `behavioral_remedy` (Inner shift) AND `remedy` (Sacred Remedy)
- [ ] Pillar 2 shows Mahadasha + Antardasha + `astro_context` when birth data present
- [ ] Pillar 2 shows "Add birth details" CTA when birth data absent
- [ ] `/select` endpoint calls `vedic_calculator` and returns `astro_context`, `current_mahadasha`, `current_antardasha`, `birth_data_present`
- [ ] No dasha calculation code added to `scriptural_oracle_router.py`
- [ ] Build clean, all code committed
