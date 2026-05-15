# Codex Commission Green Light Memo
> Review date: 2 May 2026
> Reviewer: Claude Code
> Status: All 3 commissions reviewed -- verdicts below

---

## Commission 1 -- Live TV (Sai Baba Arti): **GO** (4 spec corrections required)

### Verdict
GO -- architecture is sound. No blockers to commissioning. Four spec corrections must be applied before sending to Codex, plus one existing pre-commission blocker.

### Issues Found

#### 1. Home page route is WRONG in spec -- CORRECTION REQUIRED
The spec says the `LiveTVPanel` is for the "Home page (/)". That is incorrect.
- Root `/` maps to `<Landing />` (the public landing page)
- `/home` maps to `<Home />` (the authenticated home page, `frontend/src/pages/Home.jsx`)

**Decision required before commissioning:** Should the Live TV panel appear on:
- **(A)** The authenticated Home page at `/home` -- seen by logged-in users only
- **(B)** The public Landing page at `/` -- seen by all visitors (more SEO/acquisition value)

Recommend **(A)** unless the goal is public visibility. Update spec Section 3 Integration note accordingly.

#### 2. Home.jsx -- file name and export style -- CORRECTION REQUIRED
Spec comment says `frontend/src/pages/HomePage.jsx`. The actual file is:
```
frontend/src/pages/Home.jsx  →  export const Home = () => {   (named export)
```
Codex must import as: `import { Home } from '../pages/Home';`
The LiveTVPanel should be added inside the `Home` function's JSX return.

#### 3. `/live-sai-baba-arti` must be lazy-loaded -- CORRECTION REQUIRED
All new pages in this project are lazy-loaded (project convention -- see App.js line 1).
The spec shows a bare `<Route>` without lazy. Codex must follow this pattern:
```jsx
const LiveSaiBabaArtiPage = lazy(() => import('./pages/LiveSaiBabaArtiPage'));
```
Add this instruction to spec Section 7 (App.js entry).

#### 4. Router prefix -- follow existing convention -- CORRECTION REQUIRED
The spec says: `app.include_router(live_tv_router, prefix="/api/live-tv")`
Existing routers in this project define their prefix INTERNALLY:
```python
# live_tv_router.py
router = APIRouter(prefix="/api/live-tv", tags=["live-tv"])
```
Then `server.py` registers with no prefix arg:
```python
app.include_router(live_tv_router)
```
Codex must follow this pattern, not the spec's example.

#### 5. `backend/assets/live_tv/` directory does not exist
Directory must be created by the generation script on first run. Add to `generate_live_tv_video.py`: `os.makedirs(output_dir, exist_ok=True)`.

### Pre-Commission Blocker (Existing -- Prateek's action)
| Item | Owner | Status |
|---|---|---|
| `sai_baba_arti.mp3` + 5-8 images/clips placed in `backend/assets/live_tv/sai_baba/` | Prateek | ⏳ Pending |

Commission can be sent to Codex now. Pipeline cannot be RUN until assets arrive.

### Architecture Rule Check
Live TV has no dasha or astronomical computation. Architecture Rule (CLAUDE.md Section 16) not applicable. ✅

### Admin Console tab count
Current tabs: Overview · System · Users · Reports · Payments · Messages · Blog · Library · Notifications (9 tabs).
"Live TV" will be tab 10.

---

## Commission 2 -- Punya Rewards: **GO** (3 spec corrections + 1 architecture note)

### Verdict
GO -- self-contained commission, no architectural conflicts. Three function name mismatches in the spec must be corrected before Codex can wire hooks accurately.

### Issues Found

#### 1. TarotPage function names are WRONG in spec -- CORRECTION REQUIRED
Spec Section 8 says:
> `TarotPage.jsx` -- after `drawCard()` and `generateSpread()`

Actual functions in `TarotPage.jsx`:
| Spec name | Actual function | Location |
|---|---|---|
| `drawCard()` | `handleDraw` | line 209 |
| `generateSpread()` | `handleSpreadGenerate` | line 237 |

Codex must hook into `handleDraw` (daily draw) and `handleSpreadGenerate` (spread completion).

#### 2. BirthChartPage has two chart generation triggers -- CLARIFICATION REQUIRED
`BirthChartPage.jsx` has two functions that generate a chart:
- `handleBirthDetailsSubmit` (line 51) -- first-time form submit
- `handleGenerateBirthChart` (line 75) -- re-generate button

Recommendation: Hook Punya point award into BOTH (check idempotency by `(user_id, "birth_chart", date)` -- the once-per-chart cap handles deduplication via the `POST /api/punya/award` idempotency constraint).

#### 3. `/punya-rewards` must be lazy-loaded -- CORRECTION REQUIRED
Same project convention as all other pages. Add to spec:
```jsx
const PunyaRewardsPage = lazy(() => import('./pages/PunyaRewardsPage'));
```

#### 4. Architecture note -- add to spec before commissioning
Add to Section 10 Constraints:
> "If dasha-based point multipliers are added in future (e.g., bonus points during benefic Mahadasha), all dasha/period data must be sourced from `vedic_calculator.calculate_vimshottari_dasha()`. Do NOT add dasha calculation to `punya_router.py` or any gamification module."

### Confirmations (all clear)
| Check | Status |
|---|---|
| `request.state.user` auth pattern exists in server.py | ✅ Confirmed (line 146) |
| NavBar item structure supports new entry | ✅ Structured `{ label, path, icon, children? }` array |
| SpinWheel CSS animation keyframe conflicts | ✅ None found |
| NumerologyPage trigger: `handleGenerate` | ✅ Confirmed (line 111) |
| MongoDB Motor upsert pattern for idempotency | ✅ Matches existing conventions |

### Admin Console tab count
"Punya Rewards" will be tab 10 (or 11 if Live TV is added first).

### Router prefix convention
Define prefix inside `punya_router.py`:
```python
router = APIRouter(prefix="/api/punya", tags=["punya"])
```
Register without prefix arg in `server.py`.

---

## Commission 3 -- Remedies Engine: **GO** (Phase 1 scope reduction + spec addenda)

### Verdict
GO -- engine architecture is clean and the Architecture Rule constraint is correctly stated. One significant Phase 1 scope item must be deferred (KP integration), and the Lal Kitab ingest strategy needs clarification. Add a bold architecture warning to the top of the spec before sending.

### Issues Found

#### 1. ⚠️ ARCHITECTURE RULE -- add bold warning to spec (HIGH PRIORITY)
The spec's Section 11 Constraint #2 correctly prohibits recomputing dasha in `remedies_engine.py`, but it is buried in a bullet list. Given historical risk of Codex adding `compute_dasha_timeline()` (as it did with knowledge_engine.py in Sprint 3), add this at the TOP of the commission brief:

```
⚠️ ARCHITECTURE RULE -- MANDATORY
Do NOT add any dasha, chart, or astronomical computation functions to remedies_engine.py.
All live chart data MUST be sourced by calling:
  from vedic_calculator import calculate_vimshottari_dasha, get_current_dasha
Any deviation from this rule will be rejected and require a re-commission.
```

Confirmed function signatures in `vedic_calculator.py`:
- `calculate_vimshottari_dasha(birth_date: str, moon_longitude: float) -> list` -- line 250 ✅
- `get_current_dasha(dashas: list) -> dict` -- line 291 ✅

#### 2. Krishna Prashanavali integration -- REMOVE FROM PHASE 1 SCOPE
The KP module does NOT exist yet. Current state in App.js:
```jsx
<Route path="/ask-question" element={
  <ComingSoonPage title="Ask 1 Question" subtitle="KP Astrology-powered personalised answers" eta="Sprint 2" />
} />
```
Phase 1 of Remedies Engine cannot integrate with a Coming Soon placeholder. Move all KP-related remedies integration to Phase 2 (after KP module is commissioned and live).

**Phase 1 scope after correction:**
- `remedies_engine.py` backend with `POST /api/remedies/suggest`
- MongoDB `remedies_rules` schema + indexes
- Lal Kitab remedies data (ingest run by Claude+Prateek post-delivery -- see item 3)
- Birth Chart "Remedies" tab (BirthChartPage.jsx) ← confirmed placement

**Phase 2 (unchanged):**
- Crystal Therapy, Feng Shui, Lo Shu Grid ingest
- Daily Horoscope "Today's Remedy" card
- KP integration (remedies section in oracle answer pack)
- Admin Console Remedies tab

#### 3. Lal Kitab ingest -- clarification for Codex brief
The existing KE ingest (ch19: 78 rules, ch20: 48 rules, ch27: 99 rules = 225 total) targets the `knowledge_rules` collection. These are predictive rules, not the same as the remedy-specific content needed for `remedies_rules`.

The Remedies Engine commission covers:
- Codex builds: `remedies_engine.py`, schema, API, Birth Chart tab
- Codex does NOT run the ingest (no MongoDB access)
- Ingest is Claude+Prateek's job post-delivery, using the pipeline in spec Section 7

Add this clarification to the spec's Phase 1 delivery scope:
> "Codex delivers the engine code and ingest script. Lal Kitab data ingest (~200 rules) is run by the project team after delivery."

The `lal_kitab.json` source file exists at `backend/scripts/lal_kitab.json` and can be used as input to the ingest pipeline.

#### 4. `RemedyPage.jsx` at `/remedies` -- no collision in Phase 1
Existing file confirmed: static "Coming Soon" placeholder, zero data/API dependencies.
Phase 1 Remedies Engine is backend-only + embedded in BirthChartPage -- no new frontend route.
**No collision.** ✅

Note for Phase 2: when Admin Console Remedies tab is built, the `/remedies` placeholder should be upgraded to a full remedies discovery page (or deprecated). Do not let it sit alongside a live engine indefinitely.

#### 5. Router prefix -- follow existing convention
```python
# remedies_engine.py
router = APIRouter(prefix="/api/remedies", tags=["remedies"])
```
Register without prefix arg in `server.py`.

#### 6. Open questions in spec Section 10
Phase 1 questions are resolved:
- "Remedies tab part of BirthChartPage or BrihatKundliPage?" → **BirthChartPage** (confirmed by Phase 1 scope in spec Section 9)
- KP questions → deferred (KP not built)
- Dasha/Arc Angel questions → defer until Arc Angel commission

No blocking open questions remain for Phase 1.

### Architecture Rule Check
Section 11 Constraint #2 explicitly states: "The engine calls `vedic_calculator.py` for any live chart data -- do NOT recompute in remedies_engine.py." ✅
Function signatures confirmed in vedic_calculator.py. ✅
Bold warning to be added at top of spec before sending. ⚠️

---

## Recommended Send Order

| Order | Commission | Reason |
|---|---|---|
| **1st** | **Remedies Engine** | Pure backend + schema. No frontend route in Phase 1. Unblocks Birth Chart tab. |
| **2nd** | **Punya Rewards** | Self-contained. Module hooks are additive. High user-facing value. Can send immediately after Remedies brief. |
| **3rd** | **Live TV** | Send brief now (Codex can build while assets are being prepared). Pipeline runs only when Prateek supplies `sai_baba_arti.mp3` + images. |

---

## Shared Constraints to Add to All 3 Briefs

Add this block to the Constraints section of each brief before sending:

```
1. All new pages must be lazy-loaded in App.js:
   const MyPage = lazy(() => import('./pages/MyPage'));

2. Router prefix must be defined INSIDE the router file:
   router = APIRouter(prefix="/api/my-prefix", tags=["my-tag"])
   Registration in server.py: app.include_router(my_router)  ← no prefix arg

3. Follow Temple App theme: bg-background, bg-card, text-foreground, text-gold,
   border-gold/20, GlassCard pattern (rounded-xl border border-gold/20 bg-gold/[0.04])

4. All strings in JSX must use straight quotes -- Codex output often contains curly/smart
   quotes (", ", ', ') that break Babel. Claude will fix on delivery.

5. Auth: use request.state.user (existing session middleware). Do NOT implement
   new auth flows.
```

---

## Summary Table

| Commission | Verdict | Blocker count | Spec corrections needed | Can send today? |
|---|---|---|---|---|
| Live TV | ✅ GO | 0 blockers (1 pre-existing asset blocker) | 4 | Yes -- Codex can build; pipeline runs when assets arrive |
| Punya Rewards | ✅ GO | 0 | 3 corrections + 1 architecture note | Yes |
| Remedies Engine | ✅ GO | 0 | Phase 1 scope reduction (remove KP) + bold warning + ingest clarification | Yes |
