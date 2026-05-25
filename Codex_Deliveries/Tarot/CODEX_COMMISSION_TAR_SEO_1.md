# TAR-SEO-1 Commission Brief -- Tarot SEO Pages (SEO-20K M4)
> Thread: SEO Legacy Thread (same thread as SEO-20K M1/M2/M3)
> Commission ID: TAR-SEO-1 / SEO-20K M4
> Date: 2026-05-26
> Status: READY TO ISSUE

---

## Objective

Build the Tarot SEO module -- programmatic pages derived from the decoded spread textbook. Pages organised by card meaning, spread type, and problem/intention area. This replaces the original "78 cards × 28 spreads" plan which required a combination engine. The new approach is content-driven from the source book.

**Source book:**
```
/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/Tarot/1001-tarot-spreads-the-complete-book-of-tarot-spreads-for-every-purpose.epub
```

---

## Page Architecture -- 3 Categories

### Category 1 -- Tarot Spread Pages (~100 pages)

URL: `/tarot/spread/{spread-slug}`

The source book contains 1,001 spreads organised by purpose. Codex should extract the top 100 most searchable spread types (3-card spreads, Celtic Cross variants, love spreads, career spreads, etc.) and build one SEO page per spread.

**Page content:**
- H1: `[Spread Name] Tarot Spread -- How to Do It & What It Reveals`
- What this spread is for (2-3 sentences)
- **Spread diagram**: ASCII or description of card positions (e.g., Position 1 = Past, Position 2 = Present...)
- **How to perform**: Step-by-step instructions
- **Sample reading**: Example card in each position with brief interpretation
- **When to use this spread**: Best situations/questions
- **FAQ accordion**: 4 Q&As
- CTA → `/tarot` (Tarot tool)
- JSON-LD: FAQPage + HowTo

### Category 2 -- Tarot Card Meaning Pages (78 pages)

URL: `/tarot/card/{card-slug}`

One page per card (Major Arcana 22 + Minor Arcana 56).

**Page content:**
- H1: `[Card Name] Tarot Card -- Meaning, Reversed & How to Read It`
- Upright meaning (3-4 sentences)
- Reversed meaning (3-4 sentences)
- **In love readings**: What this card means for relationships
- **In career readings**: What this card means for work/finances
- **In health readings**: What this card means for wellbeing
- **Symbols and imagery**: Key visual elements and their meaning
- **Best spreads for this card**: 2-3 spread types where this card is most powerful
- **FAQ accordion**: 4 Q&As
- CTA → `/tarot`
- JSON-LD: FAQPage + Article

### Category 3 -- Problem/Intention Spread Pages (20 pages)

URL: `/tarot/for/{intention-slug}`

Pages targeting high-volume searches like "tarot spread for love", "tarot spread for career", etc.

**Intentions:**
love, career, money, health, relationships, breakup, new-beginnings, anxiety, decision-making, spiritual-growth, family, travel, manifestation, self-discovery, forgiveness, loss-grief, friendship, pregnancy, legal-matters, past-lives

**Page content:**
- H1: `Best Tarot Spreads for [Intention] -- Top [N] Layouts Explained`
- Intro: How tarot addresses this area (2-3 sentences)
- **Top 3 spreads**: Name, card positions, how to interpret for this intention
- **Best cards to see in this spread**: 5-6 favourable cards with brief meanings
- **Cards that signal caution**: 3-4 challenging cards and what they mean here
- **Sample reading walkthrough**: One example reading for this intention
- **FAQ accordion**: 5 Q&As
- CTA → `/tarot`
- JSON-LD: FAQPage + Article

---

## Total Pages

| Category | Count |
|---|---|
| Spread pages | ~100 |
| Card meaning pages | 78 |
| Intention/problem pages | 20 |
| Hub | 1 |
| **Total** | **~199** |

---

## Technical Requirements

### New files

**Backend:**
```
backend/tarot_seo_data.py      # All content data (spreads, cards, intentions)
backend/tarot_seo_router.py    # FastAPI router, prefix /api/tarot-seo
backend/scripts/seed_tarot_seo.py
```

**Frontend:**
```
frontend/src/pages/tarot-seo/TarotSeoHubPage.jsx      # /tarot/spreads (hub)
frontend/src/pages/tarot-seo/TarotSpreadPage.jsx      # /tarot/spread/:spreadSlug
frontend/src/pages/tarot-seo/TarotCardPage.jsx        # /tarot/card/:cardSlug
frontend/src/pages/tarot-seo/TarotIntentionPage.jsx   # /tarot/for/:intentionSlug
```

### Backend routes

```
GET /api/tarot-seo/spread/{slug}    → spread page data
GET /api/tarot-seo/card/{slug}      → card meaning page data
GET /api/tarot-seo/for/{slug}       → intention page data
GET /api/tarot-seo/hub              → hub page data (list of all spreads + cards)
```

### Sitemap

New endpoint in `seo_router.py`:
```
GET /api/seo/sitemap/tarot    # ~199 URLs
```

Add to `sitemap-index.xml`.

### App.js routes

```jsx
<Route path="/tarot/spreads" element={<TarotSeoHubPage />} />
<Route path="/tarot/spread/:spreadSlug" element={<TarotSpreadPage />} />
<Route path="/tarot/card/:cardSlug" element={<TarotCardPage />} />
<Route path="/tarot/for/:intentionSlug" element={<TarotIntentionPage />} />
```

**Important:** Do NOT conflict with existing `/tarot` route (TarotPage.jsx -- the interactive draw tool). These are SEO content pages, not the interactive tool.

### Vercel cache headers

Add `/tarot/spread/*`, `/tarot/card/*`, `/tarot/for/*`, `/tarot/spreads` patterns with `s-maxage=86400`.

### Wire in `server.py`

```python
from tarot_seo_router import router as tarot_seo_router
app.include_router(tarot_seo_router, prefix="/api/seo")
```

---

## Architecture Rules

1. **Do NOT modify** `backend/tarot_router.py` (the existing interactive tarot draw tool) -- these are separate
2. **Do NOT modify** `frontend/src/pages/TarotPage.jsx` -- that is the interactive tool
3. All content is original Codex writing inspired by the source EPUB -- no direct reproduction
4. GlassCard pattern, Gold accent, Tailwind only
5. `SEO` component + JSON-LD on every page

---

## Acceptance Checklist

- [ ] Hub page renders at `/tarot/spreads`
- [ ] ~100 spread pages render at `/tarot/spread/{slug}` with card positions + how-to + FAQ
- [ ] 78 card pages render at `/tarot/card/{slug}` with upright + reversed + love/career/health meanings
- [ ] 20 intention pages render at `/tarot/for/{slug}` with top spreads + best/caution cards
- [ ] No conflict with existing `/tarot` interactive tool route
- [ ] Sitemap returns ~199 URLs
- [ ] Seed script runs cleanly
- [ ] Build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
