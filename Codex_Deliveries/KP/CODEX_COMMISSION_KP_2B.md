# Commission KP-2B -- KP Oracle: Ritual Animation + Guidance Report UX + Astro-Filter

> EverydayHoroscope · Stack: React 18, Tailwind CSS, FastAPI, MongoDB  
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`  
> Live app: https://www.everydayhoroscope.in/krishna-prashnavali  
> Date issued: 2026-05-14  
> **Depends on:** KP-2A complete (bundle v2 editorial applied)

---

## Context

Phase 2B transforms the oracle from a functional tool into an immersive spiritual experience. Three UX and backend layers are added:
1. A meditation ritual screen before the grid appears
2. A structured 3-pillar reveal replacing the flat field dump
3. Live Mahadasha/transit enrichment injected into every reading

**Existing files (do NOT restructure):**
- `frontend/src/pages/kp/KrishnaOraclePage.jsx` -- main page (704 lines)
- `frontend/src/components/KrishnaOracleGrid.jsx` -- grid component
- `backend/scriptural_oracle_router.py` -- router, prefix `/api/oracle/krishna-prashnavali`
- `backend/vedic_calculator.py` -- **sole source of all dasha/transit data** (non-negotiable architecture rule)

---

## Task 1 -- White Light Meditation Ritual Screen

### What to build
A full-screen meditation interstitial that appears BEFORE the grid is shown. The grid renders beneath it and fades in when the ritual completes.

### Trigger
When the user clicks "Ask Krishna" / submits a focus area -- the ritual screen fires. After 25-30 seconds (or user taps "I'm ready"), it dismisses and the grid fades in.

### Visual spec

**Background:** Full viewport, `bg-neutral-950` (near-black)

**White orb animation:**
- A single circular `div`, starts `w-8 h-8`, white (`bg-white/90`), centered
- Expands to `w-64 h-64` over 8 seconds using CSS `@keyframes` (scale transform)
- `border-radius: 50%`, soft blur (`filter: blur(8px)` on the orb itself)
- Subtle pulsing brightness: `opacity` oscillates between `0.7` and `1.0` on a 4s cycle (simulate breathing)
- A faint outer glow ring: `box-shadow: 0 0 60px 20px rgba(255,255,255,0.08)`

**Text overlay (centered, above orb):**
```
[Line 1 -- small, gold, tracking-widest]  KRISHNA PRASHNAVALI
[Line 2 -- large, white, Playfair Display italic]  "Close your eyes."
[Line 3 -- small, white/60, appears at 5s]  "Breathe in. Visualise a pure white light at your heart centre."
[Line 4 -- small, white/60, appears at 12s]  "When you feel a connection, open your eyes and tap your letter."
```

**Grid fade-in:** The 18×18 grid (beneath this overlay) starts `opacity-0`. The ritual overlay fades out (`opacity: 0, transition 1.5s`) simultaneously as the grid fades to `opacity-100`.

**Skip option:** Small `"I'm ready"` text link (bottom center, `text-white/40 hover:text-white/70`) -- clicking it immediately dismisses the ritual and shows the grid.

**State:** Add `ritualComplete: boolean` to `KrishnaOracleApp` state. Ritual runs once per session (store completion in `sessionStorage`). On return visit within same session, skip directly to grid.

### Component
Create `frontend/src/components/kp/KrishnaRitualScreen.jsx`  
Props: `{ onComplete: () => void }`  
Rendered by `KrishnaOraclePage.jsx` above the grid when `!ritualComplete`.

---

## Task 2 -- 3-Pillar Guidance Report UX

### What to change
The current reveal screen in `KrishnaOraclePage.jsx` shows raw answer fields in a flat layout. Replace with the structured 3-pillar reveal.

### 3-Pillar structure

**Pillar 1 -- The Sacred Verse**
```
[Verdict badge: YES / WAIT / NO / PRAY -- large, colored]
[chaupai_phrase -- Sanskrit, center, gold, Cinzel font]
[title.english_block -- center, white, subtitle]
[krishna_answer.english_block -- italic, Playfair Display, white/80, center, max 3 lines]
```
Color coding for badge backgrounds:
- YES: `bg-green-900/40 border-green-500/40 text-green-300`
- WAIT: `bg-blue-900/40 border-blue-500/40 text-blue-300`
- NO: `bg-red-900/40 border-red-500/40 text-red-300`
- PRAY: `bg-purple-900/40 border-purple-500/40 text-purple-300`

**Pillar 2 -- The Astro-Scientific Context** *(new -- populated by Astro-Filter from Task 3)*
```
[Section header: "Your Cosmic Context"]
[Dasha line: "You are in [Planet] Mahadasha · [Antardasha Planet] Antardasha"]
[Context sentence: the astro_context string returned by backend]
[meaning.english_block -- "What this means for you"]
```
If user has no birth data on file, this pillar shows:
```
[Gold info banner] "Add your birth details to unlock your personal cosmic context."
[Link → /birth-chart]
```

**Pillar 3 -- The Practical Action**
```
[Section header: "Your Path Forward"]
[what_to_do.english_block -- full text]
[behavioral_remedy.english_block -- labeled "Inner shift required:"]
[precaution.english_block -- labeled "Watch for:"]
[duration.english_block -- labeled "Timeframe:"]
```

**Layout:** Three cards stacked vertically on mobile, or a 1-col → expanded 2-col on desktop (Pillars 2+3 side by side on md+).  
Use `GlassCard` for each pillar: `rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`

**Animation:** Each pillar appears with a `animate-fadeInUp` (staggered 0.2s delay between pillars) -- add this keyframe to the component or Tailwind config.

### Remove
Remove the current flat field dump layout for the oracle answer reveal. Keep the share button, history link, and "Ask again" CTA.

---

## Task 3 -- Astro-Filter Enrichment (Backend)

### Architecture rule (MANDATORY)
All dasha and planetary data MUST come from `vedic_calculator.py` via `calculate_vimshottari_dasha()` and `get_current_dasha()`. Do NOT add dasha calculation logic to `scriptural_oracle_router.py`.

### What to add to `POST /api/oracle/krishna-prashnavali/select`

**Input:** The `/select` endpoint already accepts `birth_date`, `birth_time`, `birth_place`. When these are provided:

1. Call `vedic_calculator.calculate_birth_chart(birth_date, birth_time, birth_place)` to get planetary positions
2. Call `vedic_calculator.calculate_vimshottari_dasha(birth_date, moon_longitude)` to get dasha timeline
3. Call `vedic_calculator.get_current_dasha(dashas)` to get active Mahadasha
4. Extract: `current_mahadasha_planet`, `current_antardasha_planet`

**Generate `astro_context` string:**  
Pass to Claude enrichment call (already in `_claude_enrich_summary()`):
```python
astro_context_prompt = f"""
User's current Mahadasha: {current_mahadasha_planet}
Current Antardasha: {current_antardasha_planet}
Oracle verdict: {answer.verdict_display}
Verdict theme: {answer.source_category}

Write one sentence (max 20 words) connecting the oracle verdict theme to the user's current dasha period. 
Be specific and grounded. Do not use generic phrases like 'the stars align'.
Example: 'Your Saturn Mahadasha makes this WAIT verdict especially apt -- patience is Saturn's core teaching.'
"""
```

**Add to response model:**
```python
class KrishnaReadingResponse(BaseModel):
    # ... existing fields ...
    astro_context: Optional[str] = None          # generated by Claude enrichment
    current_mahadasha: Optional[str] = None      # e.g., "Saturn"
    current_antardasha: Optional[str] = None     # e.g., "Mercury"
    birth_data_present: bool = False             # tells frontend whether to show Pillar 2 or the "add birth data" prompt
```

**When birth data is absent:** `astro_context = None`, `birth_data_present = False`. Frontend shows the "Add birth details" prompt in Pillar 2.

**Import in scriptural_oracle_router.py:**
```python
from vedic_calculator import calculate_vimshottari_dasha, get_current_dasha, calculate_birth_chart
```

---

## Constraints

- **Architecture rule:** All dasha data from `vedic_calculator.py` -- never recalculate in the oracle router
- Do NOT change the chaupai extraction algorithm (`_extract_indices`)
- Do NOT change the 36-answer bundle structure
- The ritual screen must be skippable -- no user should be forced to wait 30 seconds
- The ritual runs once per browser session (sessionStorage key: `kp_ritual_done`)
- All new components go in `frontend/src/components/kp/`
- Use existing Tailwind tokens and GlassCard pattern throughout

## Acceptance Criteria

- [ ] Ritual screen appears on first oracle access per session; skippable via "I'm ready"
- [ ] White orb expands and pulses over 25 seconds; text lines appear in sequence
- [ ] Grid fades in as ritual dismisses (no hard cut)
- [ ] Ritual skipped on return within same browser session
- [ ] Reveal shows 3 distinct pillars: Sacred Verse / Cosmic Context / Practical Action
- [ ] Verdict badge colour-coded correctly for all 4 verdict types
- [ ] Pillar 2 shows Mahadasha + Antardasha + `astro_context` string when birth data present
- [ ] Pillar 2 shows "Add birth details" CTA when birth data absent
- [ ] `/select` endpoint calls `vedic_calculator` and returns `astro_context`, `current_mahadasha`, `current_antardasha`
- [ ] No dasha calculation code added to `scriptural_oracle_router.py` beyond the import
- [ ] All code committed to `main`
