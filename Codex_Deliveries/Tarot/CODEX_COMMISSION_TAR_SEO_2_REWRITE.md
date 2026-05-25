# TAR-SEO-2 Commission Brief -- Tarot Data Rewrite (Copyright + Quality Fix)
> Thread: Tarot SEO Codex Thread (same thread as TAR-SEO-1)
> Commission ID: TAR-SEO-2
> Date: 2026-05-26
> Status: READY TO ISSUE
> Prerequisite: TAR-SEO-1 delivered ✅

---

## Context -- Why This Brief Exists

TAR-SEO-1 delivered `backend/tarot_seo_data.py` with 100 spread records, 78 card records,
and 20 intention records. A content audit found two problems that must be fixed before the
data is seeded to the live production database.

**No router, frontend, or wiring changes are needed. This brief touches ONE file only:**
`backend/tarot_seo_data.py`

---

## Problem 1 -- SPREADS: Verbatim Book Text (Copyright Risk) 🔴

The `purpose` and `when` fields in the `SPREADS` list contain text copied directly from the
source EPUB: `1001-tarot-spreads-the-complete-book-of-tarot-spreads-for-every-purpose.epub`

**Evidence:**
- 6 `purpose` fields are mid-sentence cuts -- the sentence is literally incomplete because it was
  truncated mid-copy from the book. Examples:
  - `"Any single uncomplicated question that requires a straightforward"` -- no ending
  - `"You can extend any unstructured three-card reading (see"` -- references a book page number
  - `"crescent-moon angels with the exception of Gabriel (see"` -- another book cross-reference
- 52 of 100 `purpose` fields are verbatim or near-verbatim book prose
- `when` fields follow the same pattern -- the author's voice, phrasing, and sentence structure

**The fix:** Rewrite ALL `purpose` and `when` fields across all 100 spreads as original prose.
Same meaning. Different words. No book sentences. No references to "see page X".
Each rewrite should be 1-3 sentences, written as a practitioner explaining the spread.

---

## Problem 2 -- CARDS: Mechanical Template Repetition (AI Detection Risk) 🟡

The `upright`, `reversed`, `love`, `career`, and `health` fields for all 78 cards follow
rigid sentence templates. The same structural sentence appears across dozens of cards:

**Detected repeated endings (verbatim across 20+ cards):**
- `upright` always ends: `"...It asks for conscious participation rather than passive hope."`
- `love` always uses: `"...asks whether the relationship can hold that energy honestly."`
- `career` always uses: `"...affecting leadership, timing, responsibility, or visibility."`
- `health` always uses: `"...how the nervous system, mindset, and daily rhythm respond to..."`

**The fix:** Rewrite `upright`, `reversed`, `love`, `career`, `health` for all 78 cards so
that each card has a UNIQUE sentence structure. No two cards should share the same closing
sentence. The content should feel like it was written specifically for that card -- not
assembled from a template with the card name filled in.

Tarot card meanings are well-established in the tradition. Write them from that tradition,
not from a fill-in-the-blank formula. Each card's `upright` should convey something only
that card communicates. Each `reversed` should feel like a distinct shadow, not a generic
"the lesson is delayed" wrapper.

---

## Deliverable -- Updated `tarot_seo_data.py`

**Only change these fields -- do not touch anything else:**

In `SPREADS` list:
- `purpose` -- all 100 entries: rewrite as original prose (1-3 sentences)
- `when` -- all 100 entries: rewrite as original prose (1-2 sentences)

In `CARDS` data (built by `_build_cards()`):
- `upright` -- all 78 cards: unique sentence structure per card
- `reversed` -- all 78 cards: unique sentence structure per card
- `love` -- all 78 cards: unique framing per card
- `career` -- all 78 cards: unique framing per card
- `health` -- all 78 cards: unique framing per card

**Do NOT change:**
- Spread `title`, `slug`, `chapter`, `positions` fields
- Card `slug`, `name`, `arcana`, `suit`, `rank`, `imagery` fields
- The `INTENTIONS` dict
- Any function definitions (`get_spread`, `get_card`, etc.)
- Any imports, constants, or the `SITE_URL`

---

## Quality Bar

**Spread `purpose` example -- BEFORE (verbatim book):**
> "You can use this Spread every day to alert you to what you need to know about the day ahead.
> If the answer is not clear, or if it is a particularly significant day, add a second card."

**After (original prose, same meaning):**
> "A daily practice spread for grounding your awareness before the day begins. Pull one card
> each morning to identify the energy, lesson, or opportunity most active for you today."

---

**Card `upright` example -- BEFORE (template):**
> "Upright, The Fool speaks of fresh possibility, trust, and a leap into the unknown. In a
> reading it usually shows the theme becoming visible, active, and impossible to ignore.
> It asks for conscious participation rather than passive hope."

**After (card-specific voice):**
> "The Fool upright is the moment before the first step -- full of potential precisely because
> nothing has been decided yet. In a reading, it signals that the situation is genuinely open,
> that overthinking is the main obstacle, and that moving with trust will reveal more than
> waiting for certainty ever could."

---

## Delivery Format

Deliver the complete updated `backend/tarot_seo_data.py` using multiple Write tool calls.
Batch the SPREADS rewrites (20 spreads per Write call) and the CARDS rewrites (15 cards per
Write call) so no single call exceeds the output limit.

**Verify before delivering:**
```bash
python3 -m py_compile backend/tarot_seo_data.py
python3 -c "from tarot_seo_data import list_spread_summaries, list_card_summaries, list_intention_summaries; print(len(list_spread_summaries()), len(list_card_summaries()), list_intention_summaries()[0]['slug'])"
# Should print: 100 78 love
```

---

## Acceptance Checklist

- [ ] All 100 `purpose` fields: original prose, no book sentences, no mid-sentence cuts
- [ ] All 100 `when` fields: original prose
- [ ] All 78 card `upright` fields: unique sentence structure (no shared closing sentence)
- [ ] All 78 card `reversed` fields: unique sentence structure
- [ ] All 78 card `love`/`career`/`health` fields: card-specific framing
- [ ] `python3 -m py_compile backend/tarot_seo_data.py` passes
- [ ] Record counts unchanged: 100 spreads, 78 cards, 20 intentions
- [ ] No changes to any other file
