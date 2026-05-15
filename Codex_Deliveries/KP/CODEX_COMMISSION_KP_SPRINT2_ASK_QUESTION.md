# Commission KP-Sprint2 -- KP Oracle: /ask-question LLM Logic Router

> EverydayHoroscope · Stack: React 18, Tailwind CSS, FastAPI, MongoDB  
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`  
> Live app: https://www.everydayhoroscope.in  
> Date issued: 2026-05-14  
> Route: `/ask-question` (currently a `ComingSoonPage` stub)

---

## Context

The `/ask-question` route has existed as a ComingSoon stub since launch with the label "KP Astrology-powered personalised answers -- Sprint 2". This commission builds the full feature.

This is a **distinct product** from the 18×18 grid oracle. Instead of tapping a grid cell, the user types a natural-language question and receives a personalised answer drawn from the Bhagavad Gita, routed via a Guna classification engine, and enriched by their live dasha context.

**Architecture rule:** All dasha data must come from `vedic_calculator.py`. Do NOT add dasha calculation logic to the new router.

---

## What to Build

### Frontend
New page: `frontend/src/pages/kp/AskQuestionPage.jsx`  
Replace the `ComingSoonPage` at `/ask-question` in `App.js` with this new component.

### Backend
New endpoint: `POST /api/oracle/krishna-prashnavali/ask`  
Add to `backend/scriptural_oracle_router.py`.

---

## User Flow

```
1. Landing screen -- "Ask Lord Krishna"
2. Focus area selection (20 categories -- see below)
3. Question input (free text, 10-200 chars)
4. [Optional if logged in + birth profile saved] Dasha enrichment loaded automatically
5. Submit → loading state → Reveal
6. Reveal: 3-section answer (Verse + Cosmic Context + Practical Action)
7. Save to history | Share
```

---

## Frontend Spec -- `AskQuestionPage.jsx`

### Screen 1 -- Landing / Onboarding
- Full-page hero: dark background, gold Diya icon, headline "Ask Lord Krishna"
- Subline: "Type your question. Receive guidance rooted in the Bhagavad Gita."
- CTA: "Begin" → navigates to Screen 2

### Screen 2 -- Focus Area Selection
Grid of 20 category cards (4 columns on desktop, 2 on mobile). Each card:
- Icon (use Lucide icons -- suggested below)
- Category name
- One-line description

**20 Categories:**

| # | Name | Icon | Description |
|---|---|---|---|
| 1 | Job Change / Promotion | `Briefcase` | Should I accept this or wait? |
| 2 | Workplace Conflict | `Users` | How do I navigate a difficult colleague? |
| 3 | Startup / Business Risk | `TrendingUp` | Is now the right time to launch? |
| 4 | Leadership Decision | `Crown` | What does ethical leadership look like here? |
| 5 | Anxiety & Stress | `Wind` | I am overwhelmed -- what do I do? |
| 6 | Grief & Loss | `Heart` | How do I process this loss? |
| 7 | Anger & Resentment | `Flame` | I want to react -- should I? |
| 8 | Inner Peace | `Sunrise` | I need stillness -- where do I begin? |
| 9 | Marriage & Partnership | `Rings` → use `Link` | Is this the right person / path? |
| 10 | Parenting & Family | `Home` | How do I approach this family situation? |
| 11 | Forgiveness | `RefreshCw` | Can I -- should I -- let this go? |
| 12 | Exam / Study Focus | `BookOpen` | How do I concentrate and trust the process? |
| 13 | Life Purpose | `Compass` | What is my Swadharma (true calling)? |
| 14 | Procrastination | `Clock` | I keep delaying -- what is Krishna's counsel? |
| 15 | Financial Stability | `Coins` → use `DollarSign` | How do I relate to this financial situation? |
| 16 | Health & Healing | `Activity` | How do I approach this physical challenge? |
| 17 | Travel & Relocation | `MapPin` | Is this move / journey auspicious? |
| 18 | Toxic Relationship | `ShieldOff` | Do I stay, speak, or leave? |
| 19 | Overcoming a Habit | `RefreshCcw` | How do I break this cycle? |
| 20 | Daily Inspiration | `Star` | No specific question -- I seek wisdom for today. |

Selected category highlighted with gold border. User can select one at a time.  
"Next" button activates after selection.

### Screen 3 -- Question Input
- Selected category shown as a chip above
- Large textarea: `"Type your question to Lord Krishna..."`
- Character counter (10 min / 200 max)
- Below textarea: `"Your question is private. Krishna hears, not the algorithm."` (small grey text)
- If user is logged in + birth profile saved: show `"Your cosmic context (Mahadasha) will be included automatically ✦"` in gold
- "Submit" button

### Screen 4 -- Loading
- Dark screen, pulsing gold Diya animation
- Rotating text: `"Reading the Bhagavad Gita..."` → `"Listening to Krishna..."` → `"Your answer is forming..."`
- Duration: 2-4 seconds (actual API call)

### Screen 5 -- Reveal
Three-card layout (same as KP-2B Guidance Report UX):

**Card 1 -- The Verse**
- Gita reference (e.g., `Chapter 2, Verse 47`)
- Sanskrit shloka (Cinzel font, gold)
- English translation (Playfair Display italic)
- Verdict-style label: `"Krishna's guidance: [PROCEED / PAUSE / REFLECT / SURRENDER]"` in a colored badge

**Card 2 -- Cosmic Context** (only if birth data present)
- `"You are in [Planet] Mahadasha · [Antardasha] Antardasha"`
- One sentence connecting dasha to the Gita answer
- If no birth data: CTA to add birth details

**Card 3 -- Your Path Forward**
- `"What to do"` -- specific action from the Gita/Logic Router
- `"Inner shift"` -- behavioral/psychological guidance
- `"Timeframe"` -- general guidance on timing

**Bottom actions:** Share button | Save to History | Ask Again

---

## Backend Spec -- `POST /api/oracle/krishna-prashnavali/ask`

Add to `backend/scriptural_oracle_router.py`.

### Request model
```python
class AskQuestionRequest(BaseModel):
    question: str                    # 10-200 chars
    focus_area: str                  # one of 20 category slugs
    birth_date: Optional[str] = None
    birth_time: Optional[str] = None
    birth_place: Optional[str] = None
    user_id: Optional[str] = None
```

### Processing pipeline

**Step 1 -- Guna Classification**  
Classify the question's intent as one of three Guna states using a Claude Haiku call:
```
System: "You are a Bhagavad Gita Guna classifier. Given a user question and focus area, classify the underlying state as exactly one of: SATTVA (clear, virtuous, seeking truth), RAJAS (action-driven, ego-involved, seeking results), TAMAS (confused, fearful, paralysed). Return only the word."
User: "Focus area: {focus_area}. Question: {question}"
```

**Step 2 -- Logic Router**  
Map `(focus_area, guna)` to a Gita verse and verdict using the Logic Router JSON (see below).

**Step 3 -- Dasha enrichment** (if birth data provided)  
```python
from vedic_calculator import calculate_vimshottari_dasha, get_current_dasha, calculate_birth_chart
chart = calculate_birth_chart(birth_date, birth_time, birth_place)
dashas = calculate_vimshottari_dasha(birth_date, chart["moon_longitude"])
current = get_current_dasha(dashas)
mahadasha = current["planet"]
antardasha = current["antardashas"][0]["planet"] if current.get("antardashas") else None
```

**Step 4 -- Claude synthesis**  
Single Claude Sonnet call combining verse + guna + dasha:
```
System: "You are Krishna speaking to a seeker through the Bhagavad Gita. Provide grounded, specific, and compassionate guidance. Never be vague. Never say 'the stars align'. Speak in second person to the seeker."
User: "
Gita verse: {verse_ref} -- {verse_sanskrit} -- {verse_english}
Seeker's state (Guna): {guna}
Focus area: {focus_area}
Question: {question}
Dasha context: {mahadasha} Mahadasha, {antardasha} Antardasha [omit if unavailable]

Return JSON:
{
  'verdict_label': 'PROCEED|PAUSE|REFLECT|SURRENDER',
  'krishna_voice': '2-3 sentence divine voice response',
  'what_to_do': 'specific action (1-2 sentences)',
  'inner_shift': 'behavioral guidance (1 sentence)',
  'timeframe': 'timing guidance (1 sentence)',
  'astro_context': 'dasha connection sentence [omit if no dasha data]'
}
"
```

**Step 5 -- Persist and respond**  
Save to MongoDB collection `ask_question_readings`:
```python
{
  "user_id": user_id,
  "question": question,
  "focus_area": focus_area,
  "guna": guna,
  "verse_ref": verse_ref,
  "response": synthesized_response,
  "mahadasha": mahadasha,
  "antardasha": antardasha,
  "created_at": datetime.utcnow()
}
```

### Response model
```python
class AskQuestionResponse(BaseModel):
    reading_id: str
    guna: str                        # SATTVA | RAJAS | TAMAS
    verse_ref: str                   # e.g., "Chapter 2, Verse 47"
    verse_sanskrit: str
    verse_english: str
    verdict_label: str               # PROCEED | PAUSE | REFLECT | SURRENDER
    krishna_voice: str
    what_to_do: str
    inner_shift: str
    timeframe: str
    astro_context: Optional[str]
    current_mahadasha: Optional[str]
    current_antardasha: Optional[str]
    birth_data_present: bool
```

---

## Logic Router JSON -- Seed Data

Create file: `backend/assets/krishna_oracle/ask_question_logic_router.json`

Structure per focus_area × guna combination:
```json
{
  "routes": [
    {
      "focus_area": "job_change_promotion",
      "guna": "SATTVA",
      "verse_ref": "Chapter 2, Verse 47",
      "verse_sanskrit": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन",
      "verse_english": "You have a right to perform your prescribed duties, but you are not entitled to the fruits of your actions.",
      "base_verdict": "PROCEED",
      "logic_tag": "Nishkama Karma"
    },
    {
      "focus_area": "job_change_promotion",
      "guna": "RAJAS",
      "verse_ref": "Chapter 3, Verse 21",
      "verse_sanskrit": "यद्यदाचरति श्रेष्ठस्तत्तदेवेतरो जनः",
      "verse_english": "Whatever actions a great person performs, common people follow. Whatever standards they set, all the world pursues.",
      "base_verdict": "PAUSE",
      "logic_tag": "Dharmic Leadership"
    },
    {
      "focus_area": "job_change_promotion",
      "guna": "TAMAS",
      "verse_ref": "Chapter 6, Verse 35",
      "verse_sanskrit": "असंशयं महाबाहो मनो दुर्निग्रहं चलम्",
      "verse_english": "O mighty-armed Arjuna, the mind is undoubtedly restless and difficult to control -- but it can be conquered by practice and detachment.",
      "base_verdict": "PAUSE",
      "logic_tag": "Mind Mastery"
    }
  ]
}
```

Seed with all 60 combinations (20 focus areas × 3 Gunas). Use the verse-theme mapping below as guidance:

| Theme | Sattva verse | Rajas verse | Tamas verse |
|---|---|---|---|
| Action/Work | 2.47 | 3.21 | 6.35 |
| Patience/Wait | 17.16 | 4.38 | 2.14 |
| Emotional | 6.5 | 2.62-63 | 2.14 |
| Relationships | 13.8 | 16.1-3 | 18.66 |
| Purpose/Identity | 18.47 | 3.35 | 9.34 |
| Fear/Anxiety | 4.10 | 2.14 | 18.58 |
| Grief | 2.20 | 2.23 | 9.33 |
| Forgiveness | 12.13 | 16.3 | 18.66 |
| Financial | 9.22 | 3.12 | 4.31 |
| Health | 17.8 | 6.17 | 17.9 |

Fill remaining combinations using Gita wisdom appropriate to the theme. The Claude synthesis step will personalise -- the Logic Router just provides the base verse and logic_tag.

---

## Premium Gating

| User state | Experience |
|---|---|
| Logged out | See landing + category selector. On submit → auth prompt |
| Free logged-in | 2 free readings/month. On limit → premium upgrade CTA |
| Premium | Unlimited. Full dasha enrichment shown. |

Gate check at `/ask` endpoint start: query `users` collection for `is_premium` and monthly reading count.

---

## Auth Wiring

The endpoint uses `optional_auth` (same pattern as other KP endpoints) -- returns reading without user_id if unauthenticated, persists to DB if authenticated.

---

## Acceptance Criteria

- [ ] `/ask-question` route renders `AskQuestionPage.jsx` (no longer ComingSoonPage)
- [ ] All 20 category cards render with correct icons, names, descriptions
- [ ] Question textarea enforces 10-200 char limits
- [ ] Loading state shows animated Diya + rotating text
- [ ] Reveal shows 3-card layout: Verse / Cosmic Context / Practical Action
- [ ] Guna classification runs via Claude Haiku (fast, cheap)
- [ ] Logic Router JSON seeds all 60 routes
- [ ] Dasha enrichment calls `vedic_calculator` when birth data provided
- [ ] `astro_context` sentence appears in Cosmic Context card
- [ ] No birth data → "Add birth details" CTA in Cosmic Context card
- [ ] Readings persisted to `ask_question_readings` collection
- [ ] Premium gating: 2 free/month, unlimited premium
- [ ] Share button and Save to History functional
- [ ] All code committed to `main`
