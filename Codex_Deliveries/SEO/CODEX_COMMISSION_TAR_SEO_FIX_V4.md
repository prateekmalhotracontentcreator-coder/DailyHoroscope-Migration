# Codex Commission: TAR-SEO-FIX v4 -- Tarot SEO
> File: `backend/tarot_seo_data.py`
> Scan: `python3 tests/echo_pace_seoc_tarot_scan.py`
> Target: Spreads L2=0 · Cards L3<60% · Intentions L2=0 · L1 must NOT regress on any type

---

## Current Scan (v3 delivery, not committed)

```
Spreads:    L1 45.6% PASS  ·  L2 FAIL  ·  L3 FAIL
Cards:      L1 34.8% PASS  ·  L2 PASS  ·  L3 FAIL
Intentions: L1 11.6% PASS  ·  L2 FAIL  ·  L3 PASS
```

What improved: Intentions L3 now passing. All L1 scores holding. Cards L2 now clean.
Still failing: Spreads L2 + L3, Cards L3, Intentions L2.

---

## Fix 1 -- Spreads FAQ: two fixed answer sentences (line 1720)

**Location:** The FAQ list built inline in the spread page builder. Two answers are fully fixed templates that appear on all 100 spread pages.

**Violating sentences:**

```python
# Q2 -- "layout uses cards position" 100%, "its interpretive task use" 100%:
"answer": f"This layout uses {card_count} cards, with each position carrying its own interpretive task."

# Q3 -- "paced reading rather single" 100%:
"answer": f"Use it when {spread['chapter'].lower()} questions need a paced reading rather than a single-card shortcut."
```

**Replace with hash-selected pools.** Seed: `_hash_index(spread["slug"], "faq_q2", modulus=8)` and `_hash_index(spread["slug"], "faq_q3", modulus=8)`.

```python
q2_seed = _hash_index(spread["slug"], "faq_q2", modulus=8)
q2_answers = [
    f"It uses {card_count} cards. Each position in the layout addresses a distinct aspect of the question so the reading builds depth rather than repeating the same angle.",
    f"{card_count} cards, with every position assigned its own scope. The structure prevents the reading from collapsing into a single card doing all the interpretive work.",
    f"The spread draws {card_count} cards. Positions are separated by function -- each one holds a different slice of the situation -- which is what gives the reading its range.",
    f"{card_count} positions, each covering a different dimension of the question. The card count is not arbitrary; it matches the number of meaningful angles the spread is designed to illuminate.",
    f"This layout calls for {card_count} cards. Rather than one pull doing everything, the positions distribute the question across multiple frames so each card contributes something distinct.",
    f"{card_count} cards fill the layout. The design keeps each position focused on a specific role so the reading produces a coherent picture rather than overlapping impressions.",
    f"You draw {card_count} cards for this spread. Each position is scoped differently -- the count reflects how many separate questions the layout was built to answer simultaneously.",
    f"The spread has {card_count} positions. Keeping each card responsible for one part of the question is what separates a structured layout from a general freeform pull.",
]

q3_seed = _hash_index(spread["slug"], "faq_q3", modulus=8)
q3_answers = [
    f"When a {spread['chapter'].lower()} question has enough complexity that a single card would flatten the answer. This spread holds the nuance.",
    f"Reach for it when {spread['chapter'].lower()} situations need more than one angle -- when the answer depends on context, timing, or competing forces that a one-card pull cannot separate.",
    f"When the {spread['chapter'].lower()} question you are holding has layers that a quick pull would collapse. This layout is designed to keep those layers visible.",
    f"When clarity requires structure, not just a single impression. {spread['chapter'].title()} questions with multiple moving parts are exactly the kind this spread was built for.",
    f"Use it when you already sense that the {spread['chapter'].lower()} situation is not simple enough for a one-card read -- when you need the cards to map a territory, not just point at it.",
    f"When the {spread['chapter'].lower()} question you are working with has enough weight that you want each part of the answer to have its own card rather than sharing one.",
    f"Whenever a {spread['chapter'].lower()} situation calls for breadth. If a one-card pull feels too narrow for what you are holding, this spread gives each dimension its own position.",
    f"When the {spread['chapter'].lower()} reading needs depth over speed. This layout earns its card count by ensuring each position contributes something the others cannot.",
]
```

Then update the FAQ list to use:
```python
{"question": f"How many cards are in the {spread['title']} spread?", "answer": q2_answers[q2_seed]},
{"question": f"When should I use the {spread['title']} spread?", "answer": q3_answers[q3_seed]},
```

---

## Fix 2 -- Cards major arcana meta_title (line 2757)

**Location:** `get_card()` or the card page builder function around line 2757.

**Current (FAILING -- all 22 major arcana share 7 tokens → 71% Jaccard):**
```python
meta_title = f"{card['name']} Tarot Card - Meaning, Reversed and How to Read It"
```

The tokens "Tarot", "Card", "Meaning", "Reversed", "How", "Read", "It" are shared across all 22 major arcana pages. Any two major arcana cards with single-word names (The Sun, The Moon, The Star, The World...) get Jaccard = 7/9 = 78% → hard FAIL.

**Fix:** Add a card-unique keyword drawn from the first meaningful word in `card["upright"]`. Add this helper function:

```python
def _upright_keyword(card: dict) -> str:
    """Returns the first non-trivial word from the card's upright meaning."""
    SKIP = {
        "a", "an", "the", "this", "that", "it", "its", "is", "are", "was",
        "of", "in", "on", "for", "to", "and", "or", "but", "with", "by",
        "your", "you", "their", "they", "we", "when", "how", "what", "where",
        "often", "can", "will", "may", "might", "new", "one", "time",
    }
    import re
    text = re.sub(r"[^a-z\s]", "", (card.get("upright") or "").lower())
    for word in text.split():
        if word not in SKIP and len(word) > 3:
            return word.title()
    return "Guide"
```

Then replace the major arcana meta_title line:
```python
# BEFORE:
meta_title = f"{card['name']} Tarot Card - Meaning, Reversed and How to Read It"

# AFTER:
meta_title = f"{card['name']} Tarot -- {_upright_keyword(card)} & Reading Guide"
```

**Why this works:** "The Sun Tarot -- Vitality & Reading Guide" vs "The Moon Tarot -- Intuition & Reading Guide" → shared tokens after stop-word removal: {tarot, reading, guide} = 3. Union for two single-word-name cards = {sun, moon, tarot, vitality, intuition, reading, guide} = 7. Jaccard = 3/7 = 43% ✅

Leave the minor arcana title unchanged:
```python
if card["arcana"] == "minor":
    meta_title = f"{card['name']} Tarot Card -- {card['suit'].title()} Suit Guide"
```

---

## Fix 3 -- Intentions FAQ: two fixed answer sentences (line 2774)

**Location:** The FAQ list built inline in `get_intention()` around line 2774.

**Violating sentences:**

```python
# Q1 -- "quick clarity pull layered" 100%:
"answer": f"For {payload['label'].lower()}, choose between a quick clarity pull, a layered reflection spread, or a narrative layout depending on how much context the question needs."

# Q5 -- "tarot tool when want" 100%, "when want real draw" 100%:
"answer": f"Yes. Let these pages teach the symbolism around {payload['label'].lower()}, and use the live tarot tool when you want a real draw with guided interpretation."
```

**Replace with hash-selected pools. Seed: `_hash_index(slug, "int_faq_q1", modulus=8)` and `_hash_index(slug, "int_faq_q5", modulus=8)`.**

```python
int_q1_seed = _hash_index(slug, "int_faq_q1", modulus=8)
int_q1_answers = [
    f"For {payload['label'].lower()}, the spread choice depends on what the question is actually asking. A focused two- or three-card pull works when the situation is clear; a larger layout helps when you need to map relationships between factors.",
    f"Match the spread to the depth of the question. Simpler {payload['label'].lower()} questions fit a direct three-card format; anything involving multiple people, timelines, or obstacles usually benefits from a position-based layout.",
    f"The spreads listed on this page were selected specifically for {payload['label'].lower()} work. The right one depends on whether you need a snapshot, a trajectory, or a full situational map.",
    f"For {payload['label'].lower()}, start with the spread that best matches the complexity of what you are holding. A single focus question suits fewer cards; a multi-layered situation generally rewards more positions.",
    f"The spread selection comes down to the scope of the {payload['label'].lower()} question. One-angle questions work with direct layouts; questions with multiple unknowns need structured position spreads that can hold each variable separately.",
    f"Choose based on how many distinct aspects the {payload['label'].lower()} question contains. One central concern needs three to four positions; a situation with several competing forces needs a layout that keeps each one in its own card.",
    f"For {payload['label'].lower()} readings, the recommended spreads on this page are ordered by use case. Scan the 'when to use' note for each one -- that is the fastest way to choose the right structure for your question.",
    f"The best spread for {payload['label'].lower()} is the one whose positions match what you actually need to know. Check how each position is labelled before choosing -- a spread that names the right questions will read more clearly than a general one.",
]

int_q5_seed = _hash_index(slug, "int_faq_q5", modulus=8)
int_q5_answers = [
    f"Yes. These pages build the vocabulary for {payload['label'].lower()} readings -- card meanings, spread logic, and interpretive patterns. The interactive draw complements that by applying the vocabulary to your specific question in real time.",
    f"Absolutely. The pages here give you the symbolic framework; the live draw gives you a positioned reading. They are designed to work together, not replace each other.",
    f"Yes -- the two serve different purposes. This section teaches the symbolic and structural layer of {payload['label'].lower()} tarot; the interactive draw applies it to whatever you are holding right now.",
    f"Yes. Reading these pages before a live draw is worth doing -- you will bring more interpretive precision to the session because you already understand the card and spread logic for {payload['label'].lower()} questions.",
    f"Both are useful. These pages build context for {payload['label'].lower()} symbolism; the draw takes that context and grounds it in a specific position-by-position reading of your current question.",
    f"Yes. Think of these pages as the preparation layer and the interactive draw as the application layer. The combination gives you more than either one alone.",
    f"Definitely. Understanding the cards and spreads for {payload['label'].lower()} before you draw tends to produce cleaner, more precise readings than going in cold.",
    f"Yes -- the pages here give you interpretive depth; the live tool gives you a specific positional reading. For {payload['label'].lower()} questions that matter, doing both in sequence produces the sharpest results.",
]
```

Update the FAQ list to use:
```python
{"question": f"Which tarot spread is best for {payload['label'].lower()}?", "answer": int_q1_answers[int_q1_seed]},
...
{"question": f"Should I still use the interactive tarot tool for {payload['label'].lower()}?", "answer": int_q5_answers[int_q5_seed]},
```

---

## L1 Guard -- Must Not Regress

All three page types currently pass L1. The only content changed is:
- 2 FAQ answers in Spreads (hash-selected variants -- no structural repetition introduced)
- meta_title for 22 major arcana cards (adds unique per-card keyword -- reduces repetition)
- 2 FAQ answers in Intentions (hash-selected variants -- no structural repetition introduced)

None of these changes introduce shared structural vocabulary. L1 should hold or improve.

**If L1 regresses on any type after these changes, stop and report before committing.**

---

## Acceptance Criteria

Single run of `python3 tests/echo_pace_seoc_tarot_scan.py` shows:

| Type | L1 | L2 | L3 |
|---|---|---|---|
| Spreads | < 50% (must not regress from 45.6%) | 0 violations | < 60% |
| Cards | < 50% (must not regress from 34.8%) | 0 violations | < 60% |
| Intentions | < 50% (must not regress from 11.6%) | 0 violations | < 60% |

All three must pass simultaneously. Do not commit until the scan is clean.
