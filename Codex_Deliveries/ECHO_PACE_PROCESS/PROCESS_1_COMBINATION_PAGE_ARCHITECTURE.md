# ECHO // PACE Process 1 -- Combination Page Architecture
> Reusable framework for all cross-product SEO page builds
> Source: GAI ECHO//PACE Compliance Consultation V1 + V2
> Applies to: TAR-M4 (card×spread), Angel Numbers (number×intent), Crystal (crystal×condition), Festival-Region (festival×region)
> Last updated: 2026-05-26

---

## The Core Problem This Solves

When an SEO engine generates pages by combining two data sets (Card × Spread, Number × Intent, Crystal × Chakra), the naive approach copies the same base definition into each page and changes only the combination name. Google's TF-IDF crawlers measure the cross-page cosine similarity and classify these pages as programmatic spam.

**Baseline risk without this framework: ~85% cross-page similarity → Helpful Content filter**
**Target with this framework: <30% cross-page similarity → Safe for indexing**

---

## The Three-Step Quick Fix (Zero Full Rewrite)

### Step 1 -- Anchor Flip (Context First)

**Problem:** Pages that lead with the generic base definition give crawlers identical opening vectors.

**Fix:** The unique content -- the *intersection synthesis* between the two data points -- must appear at the absolute top of the page as an H1/H2. The base definition moves below it and is truncated.

```
❌ OLD (85% similarity):
  "The Tower energy meets the Celtic Cross intent.
   The Tower upright brings grief, betrayal, and sudden shifts..."

✅ NEW (24% similarity):
  H1: Navigating Tower Transitions in a Celtic Cross Layout
  <synthesis>: When destabilizing Martian force meets a 10-card
  self-discovery matrix, the reading surfaces overdue structural shifts...
  <card context>: [1 sentence from intent-matched field only]
```

### Step 2 -- Intent-Matched Field Selection

**Problem:** Same 3-sentence definition pasted for love, career, and health contexts.

**Fix:** Map each combination's spread category to the specific card field that matches it. Only pull that one sentence.

```python
def get_card_context(card: dict, spread_category: str) -> str:
    """Select the single most relevant card field for this spread's intent."""
    if spread_category == "love":
        return card["love"]                           # 1 sentence
    elif spread_category == "career":
        return card["career"]                         # 1 sentence
    elif spread_category == "health":
        return card["health"]                         # 1 sentence
    else:
        return card["upright"].split(".")[0] + "."    # First sentence only
```

### Step 3 -- Position Label Rotation

**Problem:** `<h3>Position 1: Past</h3>` repeated identically across thousands of pages.

**Fix:** Use the `POSITION_SYNONYMS` lookup table (already in `tarot_seo_data.py`) to rotate labels deterministically per page (seed = slug hash so the label is stable per page but different across pages).

```python
import hashlib
def rotate_label(position_concept: str, slug: str) -> str:
    idx = int(hashlib.md5(slug.encode()).hexdigest(), 16) % 5
    return POSITION_SYNONYMS[position_concept][idx]
```

---

## Minimum Viable Page Structure (300 Words, <30% Similarity)

```
┌─────────────────────────────────────────────────────────────────┐
│ FIELD 1 -- Contextual Intersection Synthesis (~75 words)          │
│   - NO base definition boilerplate                               │
│   - Focuses on elemental/thematic interaction between the two    │
│     data points (card energy × spread intent)                    │
│   - This content is UNIQUE to this exact combination             │
├─────────────────────────────────────────────────────────────────┤
│ FIELD 2 -- Positional Guidance Blueprint (~150 words)             │
│   - Covers 3 key position groups from the spread                 │
│   - Position labels use POSITION_SYNONYMS rotation               │
│   - Each position block: what this card means IN THAT POSITION   │
│     (not generic card meaning -- position-specific interpretation) │
├─────────────────────────────────────────────────────────────────┤
│ FIELD 3 -- Tactical Remedial Action (~75 words)                   │
│   - Concrete actionable steps                                    │
│   - Language anchored to the spread's intent category            │
│   - Uses CARD_REGISTER prose style (A=sharp, B=measured, C=flow) │
└─────────────────────────────────────────────────────────────────┘
```

---

## Compliant Example: The Tower × Celtic Cross (Love Context)

**H1:** Reading The Tower Through a Celtic Cross Love Spread

**Field 1 -- Synthesis:**
When The Tower's force of sudden revelation meets the Celtic Cross's ten-position map of a relationship, the reading is not about disaster -- it is about the moment a hidden truth breaks through. In a love context, this combination identifies a specific point where what was unspoken can no longer hold. The cards reveal where the fracture lives and what it is actually clearing space for.

**Field 2 -- Positional Blueprint:**
- *Origin Points:* The disruption has roots in a moment of emotional avoidance. Something that felt manageable became the weight the relationship could not carry forward.
- *Core Resistance:* The active tension is the urge to repair appearances rather than address what broke. The Tower here refuses that route.
- *Closing Synthesis:* Resolution arrives through one honest conversation that changes the terms permanently. The outcome is not comfortable -- but it is real.

**Field 3 -- Remedial Action:**
Identify the one thing neither party has said directly. Write it down before speaking it. The Tower in love does not reward delay -- but it does reward precision. One clear statement now prevents three months of ambiguity later.

---

## Module Application Map

| Module | Combination Type | Base Field A | Base Field B | Intent Match Field |
|---|---|---|---|---|
| **TAR-M4** | Card × Spread | `card.upright` (1 sentence) | `spread.purpose` | `card.love / career / health` |
| **Angel Numbers** | Number × Intent | `core.seeing_it_means` (1 sentence) | `intent.subtitle` | `intent.message` (full) |
| **Crystal** (future) | Crystal × Chakra | `crystal.upright` (1 sentence) | `chakra.theme` | Condition-matched crystal field |
| **Festival-Region** | Festival × Region | `festival.season` theme | `region.marker` | Zone-specific food + marker |

---

## Similarity Targets by Module

| Module | Pages | Target Cross-Page Cosine | Current Status |
|---|---|---|---|
| TAR-M4 (card×spread) | 4,680 | <30% | Not yet built -- apply this framework |
| Angel Numbers (number×intent) | 9,000 | <30% | Built -- scanner confirmed CLEAN ✅ |
| Festival-Region (festival×region) | 480 | <40% | M3-FIX-1 pending -- will address |
| Crystal (crystal×condition) | TBD | <30% | Not yet built |

---

## Prose Register by Card Energy (CARD_REGISTER)

Already stored in `tarot_seo_data.py`. Reference when writing synthesis copy:

| Register | Rule | Examples |
|---|---|---|
| **A -- Sharp/Abrupt** | Max 9 words/sentence. Blunt, active, no trailing adjectives. | Three of Swords, The Tower, Death, Nine of Swords |
| **B -- Grounded/Measured** | 12-18 words/sentence. Practical, balanced clauses. | The Emperor, Justice, Temperance, Seven of Pentacles |
| **C -- Expansive/Flowing** | 25+ word compound structures. Uplifting, sensory. | The Star, The Sun, Ace of Cups, The Fool |

---

## 12 P.A.C.E. Card Intent Differentiation Rules (D2 -- for TAR-SEO-3)

Insert these rules into the Codex system prompt for card field regeneration:

1. **Intention-First Framing:** Lead with the user's real-world problem, not an academic definition. Never start with "[Card] represents..."
2. **Context-Driven Analogy Substitution:** Career contexts use *restructuring, market disruption, contract dissolution*. Love contexts pivot to *emotional breakthroughs, boundary collapse, sudden disclosures*.
3. **Syntax Shift by Domain:** Career = active voice declarative verbs. Romance = passive voice, emotionally reflective phrasing.
4. **Varying Part-of-Speech Dominance:** Career text = action verbs dominant. Love text = descriptive adjectives dominant. Health = physical nouns dominant.
5. **Dynamic Length Mutation:** Career summaries: 3 sentences, under 45 words. Relationship cards: multi-clause, over 75 words.
6. **Prohibit Template Transitions:** Never begin with *"In a love context," "When it comes to career,"* or *"Regarding your health."*
7. **Intent-Specific Metaphors:** Career = structural/strategic imagery. Love = heat/depth/connection. Health = balance/energy/flow.
8. **Position-Level Structural Flipping:** Card as obstacle → lead with interrogative question. Card as advice → lead with imperative.
9. **Suit-to-Intent Alignment:** Swords in love = communication blocks and mental projections. Wands in finance = raw ambition and physical scaling.
10. **Thematic Vocabulary Partitioning:** *Liquidity, capital, execution* banned from love cards. *Intimacy, harmony, vulnerability* banned from career pages.
11. **Negative Structural Reframing:** Difficult cards in career = tactical risks. Same cards in love = interior mental patterns or defense mechanisms.
12. **Keyword Injection Distance:** Target intent keywords separated by minimum 25 neutral tokens to prevent keyword clustering penalties.

---

## When to Apply This Process

- Before issuing any Codex commission that generates N×M page combinations
- Before seeding any module where multiple pages share a common base data source
- After any scanner flags BLOCKED/FLAGGED -- use Step 1-3 to fix without full rewrite
- As a design constraint in every new TAR/ANGEL/CRYSTAL/FAITH Codex brief
