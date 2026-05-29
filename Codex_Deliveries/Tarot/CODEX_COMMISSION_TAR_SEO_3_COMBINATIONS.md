# TAR-SEO-3 Commission Brief -- Tarot Combination Pages (Phase 2)
> Commission ID: TAR-SEO-3
> Thread: Tarot Thread (same thread as TAR-SEO-1, TAR-SEO-2)
> Date: 2026-05-30
> Status: READY TO ISSUE
> Depends on: TAR-SEO-1 ✅ integrated | TAR-SEO-2 ✅ QA-cleared (ECHO/PACE strict + Layer G)

---

## 1. Context and Objective

Phase 1 delivered 199 Tarot SEO pages (100 spreads · 78 cards · 20 intentions · 1 hub),
all live at `everydayhoroscope.in` and fully QA-cleared under strict ECHO/PACE thresholds
(L1 BLOCKED ≥60%, L2 min_docs=2, Layer G BLOCKED >25%). All 15 Serper queries returned
0 hits. Content is confirmed original.

**Phase 2 (this commission) adds 4,621 pages:**

| Page type | Count | URL pattern |
|---|---|---|
| Card index hub | 1 | `/tarot/cards` |
| Card × Spread combination pages | 4,620 | `/tarot/card/:cardSlug/:spreadSlug` |
| **Phase 2 total** | **4,621** | |

**Formula:** 78 cards × ~59-60 selected spreads = ~4,620 combination pages.
The exact spread selection (60 from the 100 built in Phase 1) is specified in §4.

**The combination page answers a specific user query:**
*"What does [The Tower] mean when it appears in a [Celtic Cross] spread?"*
This is a high-intent, long-tail search pattern with no current competition in Indian
astrology/tarot markets.

---

## 2. Phase 1 Infrastructure -- What Already Exists (Do Not Duplicate)

These files are live. Read them before writing anything. Do NOT recreate or overwrite.

```
backend/tarot_seo_data.py          ← 100 spreads, 78 cards, 20 intentions, all QA-cleared
backend/tarot_seo_router.py        ← registered at /api/seo, prefix /tarot-seo
backend/server.py                  ← tarot_seo_router already wired
frontend/src/pages/tarot-seo/
    TarotSeoHubPage.jsx            ← /tarot/spreads (spread hub -- DO NOT TOUCH)
    TarotSpreadPage.jsx            ← /tarot/spread/:spreadSlug (DO NOT TOUCH)
    TarotCardPage.jsx              ← /tarot/card/:cardSlug (ADD spread navigator section only)
    TarotIntentionPage.jsx         ← /tarot/for/:intentionSlug (DO NOT TOUCH)
frontend/src/App.js                ← existing routes already wired
```

**Architecture rule:** Do NOT modify `backend/tarot_router.py` or
`frontend/src/pages/tarot/TarotPage.jsx`. Those are the interactive draw tool --
a completely separate module. These are content SEO pages.

---

## 3. New Files -- What This Commission Delivers

### Backend

```
backend/tarot_combinations_router.py   # New router -- combination pages + card hub
backend/scripts/seed_tarot_combinations.py  # Seeds tarot_combinations collection (4,620 docs)
```

**Add to `backend/server.py`:**
```python
from tarot_combinations_router import router as tarot_combinations_router
app.include_router(tarot_combinations_router, prefix="/api/seo")
```

### Frontend

```
frontend/src/pages/tarot-seo/TarotCardHubPage.jsx       # /tarot/cards (new)
frontend/src/pages/tarot-seo/TarotCombinationPage.jsx   # /tarot/card/:cardSlug/:spreadSlug (new)
```

**Modify (add one section only):**
```
frontend/src/pages/tarot-seo/TarotCardPage.jsx          # Add spread navigator section
frontend/src/pages/tarot-seo/TarotSpreadPage.jsx        # Add card quick-links section
```

### App.js -- New Routes

Add these after the existing tarot-seo routes:

```jsx
<Route path="/tarot/cards" element={<TarotCardHubPage />} />
<Route path="/tarot/card/:cardSlug/:spreadSlug" element={<TarotCombinationPage />} />
```

**Route order matters.** The combination route `/tarot/card/:cardSlug/:spreadSlug`
must come AFTER `/tarot/card/:cardSlug` (Phase 1) so the more specific path matches first.

---

## 4. The 60 Spreads for the Combination Matrix

Select these 60 from the 100 Phase 1 spreads. Criteria: search volume potential,
intent diversity, combination uniqueness. These are the `slug` values from
`tarot_seo_data.py SPREADS`.

```python
COMBINATION_SPREADS = [
    # ── General / Foundational ────────────────────────────────
    "daily-tarot-reading-insight",
    "single-question-tarot-reading",
    "three-card-reading-any-topic",
    "past-present-future-timeline-reading",
    "horseshoe-seven-card-spread",
    "celtic-cross-ten-card-spread",          # add if present; if not, use closest spread
    "four-card-unstructured-reading",
    "six-card-unstructured-spread",
    "nine-card-unstructured-reading",
    "options-decision-spread",

    # ── Love & Relationships ─────────────────────────────────
    "soulmate-past-life-reading",
    "manifesting-true-love-and-soulmate-tarot",
    "resolving-relationship-conflicts-tarot",
    "dealing-with-emotional-immaturity-in-love",
    "deciphering-mixed-intimacy-signals-in-love",
    "will-i-find-my-soulmate-reading",
    "twin-soul-connection-reading",
    "love-quarrel-resolution-spread",
    "past-life-love-and-soul-connection",

    # ── Career & Money ────────────────────────────────────────
    "starting-a-business-venture-spread",
    "day-job-vs-side-business-priority-spread",
    "launching-freelance-and-solopreneur-gigs",
    "turning-temporary-gigs-into-full-time-jobs",
    "breaking-generational-financial-scarcity",
    "manifesting-urgent-financial-abundance",
    "manifesting-fast-secondary-income",
    "job-application-success-reading",
    "managing-difficult-bosses-and-coworkers",
    "five-year-ambition-plan-spread",

    # ── Decision & Life Path ─────────────────────────────────
    "major-life-path-choices-and-transitions",
    "overcoming-fear-barriers-spread",
    "settlement-vs-going-to-trial-analysis",
    "choosing-legal-battle-vs-settlement",
    "choosing-legal-battle-vs-settlement",
    "divine-signs-for-uncertain-crossroads",
    "life-change-when-feeling-stuck",
    "breaking-free-alternative-lifestyle",

    # ── Family & Social ───────────────────────────────────────
    "preparing-for-parenthood-relationship-check",
    "resolving-family-disputes-over-baby-names",
    "dealing-with-school-bullying-children",
    "resolving-friend-group-drama-advice",
    "overcoming-isolation-after-moving",
    "social-conflict-resolution-spread",

    # ── Health & Wellbeing ───────────────────────────────────
    "calming-anxiety-and-overthinking-tarot",
    "health-improvement-outlook-spread",
    "sports-fitness-motivation-spread",
    "dealing-with-grief-and-sudden-loss",

    # ── Spiritual & Ritual ───────────────────────────────────
    "new-moon-rituals-for-fresh-beginnings",
    "quarterly-solstice-and-equinox-reading",
    "12-month-wheel-of-year-forecast",
    "birthday-solar-return-planetary-map",
    "seven-day-planetary-energy-spread",
    "sun-sign-fast-answer-spread",
    "fool-inner-child-new-beginning-spread",
    "automatic-writing-tarot-spread",
    "four-seasons-life-review-spread",

    # ── Home, Travel, Pets ───────────────────────────────────
    "vastu-blessings-for-your-new-home",
    "finding-best-pet-companion-for-your-home",
    "managing-animal-sanctuaries-and-wildlife",
    "where-to-go-on-vacation-spread",
]
```

**De-duplicate this list before seeding.** If any slug does not exist in `tarot_seo_data.py`,
skip it and use the next closest spread by category. Target: exactly 60 spreads.
Final count determines total pages: 78 cards × N spreads = N×78 combination pages.

---

## 5. Backend -- New Router

**File:** `backend/tarot_combinations_router.py`

```python
router = APIRouter(prefix="/tarot-seo", tags=["tarot-combinations"])

@router.get("/cards")                              # card hub
@router.get("/card/{card_slug}/{spread_slug}")     # combination page
```

### MongoDB Collection: `tarot_combinations`

One document per card × spread pair. 4,620 documents total.

```json
{
  "card_slug": "the-tower",
  "spread_slug": "celtic-cross-ten-card-spread",
  "card_name": "The Tower",
  "spread_title": "Celtic Cross Reading",
  "positions": [
    {
      "label": "The Present Moment",
      "card_role": "What The Tower reveals here",
      "guidance": "2-3 sentences specific to The Tower in THIS position of THIS spread"
    }
  ],
  "synthesis": "3-4 sentence paragraph. What The Tower's energy means when read through the lens of the Celtic Cross structure -- NOT a repeat of the card page upright meaning.",
  "action_step": "1 concrete action the reader should take, derived from this card-spread pairing.",
  "related_combos": ["the-tower/three-card-reading-any-topic", "the-star/celtic-cross-ten-card-spread"],
  "meta_title": "The Tower in a Celtic Cross -- What It Means in Each Position",
  "meta_description": "The Tower appearing in a Celtic Cross spread? Position-by-position guide to what this card reveals -- from the Present to the Outcome."
}
```

### Seed Script

**File:** `backend/scripts/seed_tarot_combinations.py`

- Reads `SPREADS` and `_build_cards()` from `tarot_seo_data.py`
- Filters to the 60 combination spreads
- For each card × spread pair, inserts one document
- Uses `upsert=True` on `{card_slug, spread_slug}` -- safe to re-run
- Target collection: `horoscope_db.tarot_combinations`
- Print progress: `Seeded 100/4620...` every 100 documents

---

## 6. Content Generation Rules -- ECHO/PACE Compliance

**This is the most critical section. Read it entirely before generating any content.**

Phase 2 operates under the same strict thresholds as Phase 1 (L1 BLOCKED ≥60%,
L2 min_docs=2, Layer G BLOCKED >25%). With 4,620 pages, the duplication risk is
exponentially higher than Phase 1's 199 pages. These rules are mandatory.

---

### Rule 1 -- The Synthesis Field Must Be Spread-Specific

The `synthesis` paragraph (3-4 sentences) must describe what THIS card means within
the STRUCTURE of THIS spread -- not a restatement of the card's upright meaning.

**Non-compliant (template -- will cause L1 BLOCKED):**
> "The Tower upright brings sudden disruption and unavoidable truth into the foreground.
> In a Celtic Cross, The Tower's energy is present. This is a powerful combination."

**Compliant:**
> "In a Celtic Cross, The Tower's position in the spread's architecture matters enormously.
> When it falls in the Crossing Card (Position 2), it names the force actively working
> against the situation -- disruption not as background energy but as the primary obstacle
> to read around. When it appears in the Outcome (Position 10), the collapse is not a
> warning but the destination already in motion."

The synthesis must reference the spread's structure by name (position names, the spread's
intent, the sequence of its narrative arc). It cannot be content that would work equally
well for any other spread.

---

### Rule 2 -- Position Guidance Must Be Card-Specific

Each `positions` entry must describe what THIS specific card means in that specific
position of that specific spread. It must not be a generic card definition
with the position name appended.

**Non-compliant:**
> "Position 3 (Distant Past): The Tower means sudden disruption and collapse."

**Compliant:**
> "In the Distant Past position, The Tower signals that the situation being read has
> a structural break in its history -- something that was dismantled, possibly with force,
> that shaped the current circumstance. The question to bring here is: what did that
> collapse free you from, and what did it take?"

---

### Rule 3 -- Prose Register by Card Energy

Apply the register that matches the card's energy. Do not use the same sentence
rhythm and length for The Star and The Tower.

**Register A -- Sharp / Abrupt** (short sentences, direct language):
Three of Swords, The Tower, Five of Pentacles, Ten of Swords, Five of Cups,
Nine of Swords, Five of Wands, Five of Swords, Eight of Swords, The Devil,
Seven of Swords, Three of Cups (reversed), The Moon (shadow context),
Death (when crisis-focused), The Hanged Man (resistance context)

**Register B -- Grounded / Measured** (balanced sentences, practical tone):
The Emperor, The Hierophant, Seven of Pentacles, Four of Cups, Justice,
The Chariot, Wheel of Fortune, Four of Wands, Three of Pentacles,
Eight of Pentacles, King of Swords, King of Pentacles, Queen of Swords,
Knight of Pentacles, Page of Pentacles, Six of Swords, Two of Wands,
Four of Pentacles, Two of Swords

**Register C -- Expansive / Flowing** (longer sentences, optimistic cadence):
The Star, The Sun, The World, Ace of Cups, The Lovers, The Empress,
The Fool, The Magician, Ten of Cups, Ten of Pentacles, Nine of Cups,
Nine of Pentacles, Six of Wands, Six of Cups, Three of Cups, Two of Cups,
Queen of Cups, Queen of Wands, Queen of Pentacles, King of Cups,
Ace of Wands, Ace of Pentacles, Ace of Swords, The High Priestess,
Judgement, Temperance, The Hermit (wisdom context)

---

### Rule 4 -- No Shared Synthesis Opening Sentence Pattern

Do not begin synthesis paragraphs with a template phrase that would appear across
multiple pages. The following openers will trigger L2 phrase flags:

❌ Banned: `"[Card] energy meets [Spread] intent..."`
❌ Banned: `"When [Card] appears in a [Spread], it signals..."`
❌ Banned: `"The [Card] in this spread reveals..."`
❌ Banned: Any opening that works for any card/spread with only names swapped

Each synthesis must open with something specific to the card-spread intersection.

---

### Rule 5 -- Position Labels Must Rotate (Synonym Set)

Never use the same position label word across more than 3 documents. Cycle through
synonyms drawn from this set:

| Concept | Synonyms |
|---|---|
| Past | What Came Before · The Root · What Was · Earlier Ground · The Foundation |
| Present | The Current Moment · Where You Stand · What Is Active · The Now · Present Ground |
| Future | What Is Approaching · The Direction · Where This Leads · What Is Forming · The Horizon |
| Challenge | The Obstacle · What Crosses · The Friction Point · What Resists · The Tension |
| Advice | The Guidance · What to Do · The Recommended Path · The Counsel · What the Cards Say |
| Outcome | The Resolution · Where This Settles · What Is Most Likely · The Result · How It Ends |
| Hidden Factor | What Is Not Yet Seen · The Undercurrent · The Unseen Force · What Lies Beneath |
| What to Release | What to Let Go · What No Longer Serves · The Release Point · What Must Be Left |
| What to Embrace | What to Welcome · The Growth Edge · What Is Calling You · What to Move Toward |
| External Influence | What Others Bring · The Outside Force · What the Environment Holds · External Pressure |

---

### Rule 6 -- Action Step Must Be Card × Spread Specific

The `action_step` (1 sentence) must be derived from the card-spread pairing, not
a generic card keyword. It must tell the reader what to do in response to THIS
card appearing in THIS spread.

**Non-compliant:** "Trust in new beginnings and take a leap of faith."
**Compliant:** "Before your next Celtic Cross reading, identify one structure in your
life you have been defending that may have already collapsed -- the Celtic Cross will
show you what is actually holding it up."

---

### Rule 7 -- Do Not Repeat Card Page Content

The combination page must not reproduce the card's upright/reversed/love/career/health
fields from `tarot_seo_data.py`. Those live on `/tarot/card/:cardSlug`. The combination
page should link back to the card page but must generate new content about the card
in this specific spread context.

---

### Rule 8 -- Minimum Unique Content Threshold

Each combination page must have at minimum:
- `synthesis`: 80+ words, spread-structure-specific
- `positions`: At minimum 3 positions, each 40+ words, card-position-specific
- `action_step`: 1 sentence, card×spread-specific
- **Cross-page cosine similarity target:** <50% between any two combination pages
  for the same card (e.g., The Tower × Celtic Cross vs The Tower × Three Card Reading)

---

## 7. Frontend -- Page Specifications

### 7a. Card Hub Page
**File:** `frontend/src/pages/tarot-seo/TarotCardHubPage.jsx`
**Route:** `/tarot/cards`

- H1: `Tarot Card Meanings -- All 78 Cards Explained`
- Filter tabs: All · Major Arcana · Wands · Cups · Swords · Pentacles
- 78-card grid: GlassCard per card -- name, arcana/suit badge, 1-line keyword, link → `/tarot/card/:slug`
- Below grid: "Explore a card in a specific spread" section -- search/browse into combination pages
- FAQ accordion: 5 questions
- JSON-LD: `FAQPage` + `BreadcrumbList`
- SEO title: `Tarot Card Meanings -- All 78 Cards Upright & Reversed | EverydayHoroscope`

### 7b. Card Page Enhancement (Existing File -- Add One Section)
**File:** `frontend/src/pages/tarot-seo/TarotCardPage.jsx`
**Route:** `/tarot/card/:cardSlug` (unchanged)

Add one new section below the existing card content:

**"See [Card Name] in a Specific Spread"**
- Pill/chip grid of all 60 combination spreads, each linking to `/tarot/card/:cardSlug/:spreadSlug`
- Label: the spread's humanized title
- Do not restructure the rest of the page

### 7c. Spread Page Enhancement (Existing File -- Add One Section)
**File:** `frontend/src/pages/tarot-seo/TarotSpreadPage.jsx`
**Route:** `/tarot/spread/:spreadSlug` (unchanged)

Add one new section at the bottom of the existing spread page:

**"What does a specific card mean in this spread?"**
- 78-card pill grid, each linking to `/tarot/card/:cardSlug/:spreadSlug`
- Only show this section if the spread is one of the 60 combination spreads
- Do not restructure the rest of the page

### 7d. Combination Page (New)
**File:** `frontend/src/pages/tarot-seo/TarotCombinationPage.jsx`
**Route:** `/tarot/card/:cardSlug/:spreadSlug`

Page structure:
1. **Breadcrumb:** Tarot → [Card Name] → [Spread Title]
2. **H1:** `[Card Name] in a [Spread Title] -- What It Means in Each Position`
3. **Synthesis block:** GlassCard -- the `synthesis` paragraph (3-4 sentences)
4. **Position accordion:** One expandable per spread position -- position label as heading,
   `guidance` text as body. Default: first 2 positions open.
5. **Action step strip:** Gold accent banner -- "Your next step:" + `action_step`
6. **Related combinations:** 3 GlassCards linking to `related_combos`
   - 2 same card / different spread
   - 1 different card / same spread
7. **CTAs:**
   - "Read the full [Card Name] meaning" → `/tarot/card/:cardSlug`
   - "Learn the [Spread Title] layout" → `/tarot/spread/:spreadSlug`
   - "Do a live reading now" → `/tarot`
8. JSON-LD: `FAQPage` (position Q&As) + `BreadcrumbList`

**Meta formula:**
- Title: `[Card Name] in [Spread Title] -- Position Guide | EverydayHoroscope`
- Description: `What does [Card Name] mean in a [Spread Title]? Position-by-position guide -- what this card reveals from [first position] to [last position].`

---

## 8. Sitemap

Add combination page URLs to the existing tarot sitemap endpoint in `seo_router.py`.
The existing `/api/seo/sitemap/tarot` currently returns 199 URLs. Extend it to also
return combination page URLs:

```
/tarot/cards
/tarot/card/{cardSlug}/{spreadSlug}   × 4,620
```

Priority: 0.6 (lower than card/spread pages at 0.8, higher than intentions at 0.5).
Change frequency: monthly.

---

## 9. Vercel Cache Headers

In `vercel.json`, add the combination page pattern:

```json
{
  "source": "/tarot/card/:cardSlug/:spreadSlug",
  "headers": [{ "key": "Cache-Control", "value": "s-maxage=86400, stale-while-revalidate" }]
}
```

Also add `/tarot/cards` to the cache header list.

---

## 10. ECHO/PACE Compliance Gate

After local delivery, CC will run:

```bash
python3 tests/echo_pace_tarot_scan.py
```

The scanner will need updating to include combination pages. The acceptable thresholds
for TAR-SEO-3 are the same strict thresholds as Phase 1:
- L1 BLOCKED ≥60% (any two combination pages)
- L1 FLAGGED ≥40% (requires manual review justification)
- L2 min_docs=2 (phrase in 2+ documents)
- Layer G BLOCKED >25%

**CC will not integrate until L1 BLOCKED is 0.**

---

## 11. Acceptance Checklist

- [ ] `/tarot/cards` renders the 78-card hub with filter tabs
- [ ] `/tarot/card/:cardSlug` shows new "See in a specific spread" pill section
- [ ] `/tarot/spread/:spreadSlug` shows new "What does a card mean here?" section (60 spreads only)
- [ ] `/tarot/card/:cardSlug/:spreadSlug` renders synthesis + position accordion + action step + related combos
- [ ] 4,620 (or 78 × N) combination documents seeded in `horoscope_db.tarot_combinations`
- [ ] Seed script runs cleanly with `upsert=True` -- no duplicates, safe to re-run
- [ ] Existing Phase 1 routes (`/tarot/spreads`, `/tarot/spread/:slug`, `/tarot/card/:slug`, `/tarot/for/:slug`) are UNCHANGED
- [ ] No modifications to `tarot_router.py` or `TarotPage.jsx`
- [ ] Sitemap returns Phase 1 + Phase 2 URLs (199 + 4,621)
- [ ] Build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
- [ ] ECHO/PACE L1-L2 scan: 0 pairs BLOCKED across all combination pages

---

## 12. What CC Will Do After Delivery

1. Run ECHO/PACE scan on combination pages (update scanner for new page type)
2. Fix any L1 BLOCKED pairs before integrating
3. Register new router in `server.py`
4. Wire new App.js routes
5. Run seed script against production MongoDB (`MONGO_URL` from Render env)
6. Run Layer G (Serper) on 5 combination page samples
7. Update `Codex_Deliveries/Tarot/TRACKER.md`

---

## 13. Reference Files

Read these before writing any content or code:

| File | Purpose |
|---|---|
| `backend/tarot_seo_data.py` | All Phase 1 content -- 100 spreads, 78 cards, 20 intentions |
| `backend/tarot_seo_router.py` | Phase 1 router pattern to match |
| `frontend/src/pages/tarot-seo/TarotCardPage.jsx` | File to extend (spread navigator section) |
| `frontend/src/pages/tarot-seo/TarotSpreadPage.jsx` | File to extend (card quick-links section) |
| `Codex_Deliveries/Tarot/CODEX_COMMISSION_TAROT_SEO.md` | Original architecture reference |
| `Codex_Deliveries/Tarot/TAR_ECHO_PACE_GAI_CONSULTATION.md` | ECHO/PACE compliance consultation |
| `CLAUDE.md` | Architecture rules, theme tokens, commit protocol |
