# Codex Commission: TAR-SEO-FIX v5 -- Tarot SEO
> Files: `backend/tarot_seo_data.py` · `tests/echo_pace_seoc_tarot_scan.py`
> Scan: `python3 tests/echo_pace_seoc_tarot_scan.py`
> Target: Spreads L2=0 · Spreads L3<60% · Cards L3<60% · Intentions L2=0

---

## Current Scan (v4 delivery, not committed)

```
Spreads:    L1 43.8% PASS  ·  L2 FAIL  ·  L3 FAIL
Cards:      L1 34.8% PASS  ·  L2 PASS  ·  L3 FAIL (71% major arcana)
Intentions: L1 16.3% PASS  ·  L2 FAIL  ·  L3 PASS
```

All L1 scores holding. Three new issues exposed after v4 fixed the previously
flagged phrases. Four surgical changes required.

---

## Fix 1 -- Scan Script: `_card_title()` must use `meta_title` (Cards L3)

**Root cause:** `_card_title()` in `tests/echo_pace_seoc_tarot_scan.py` (line ~232) is hardcoded to build `f"{name} Tarot Card - {arcana} Meaning & Guide"`. For all 22 major arcana cards, `arcana = "major"`. This makes every major arcana title share "Tarot Card - major Meaning & Guide" → 5 shared tokens out of 7 → Jaccard 71%.

The v4 fix correctly set `meta_title` to a unique per-card value (e.g., `"The Sun Tarot -- Vitality & Reading Guide"`), but the scan ignores `meta_title` for cards.

**Change `_card_title()` in `tests/echo_pace_seoc_tarot_scan.py`:**

```python
# BEFORE:
def _card_title(d: dict) -> str:
    name = d.get("name", d.get("slug", ""))
    arcana = d.get("arcana", "")
    return f"{name} Tarot Card - {arcana} Meaning & Guide"

# AFTER:
def _card_title(d: dict) -> str:
    if d.get("meta_title"):
        return d["meta_title"]
    name = d.get("name", d.get("slug", ""))
    arcana = d.get("arcana", "")
    return f"{name} Tarot Card - {arcana} Meaning & Guide"
```

**Why this is the right fix:** `meta_title` is the actual SEO title served to search engines. The L3 test should check what is actually served. The `meta_title` was already set uniquely per major arcana card in v4 (e.g., "The Sun Tarot -- Vitality & Reading Guide" vs "The Moon Tarot -- Intuition & Reading Guide"). With `meta_title` as the input, Jaccard drops to 3/7 = 43% ✅.

**This is the only change to the scan script.**

---

## Fix 2 -- Spreads FAQ `use` answer: Replace `spread["use"]` with hash-selected variants (Spreads L2)

**Root cause:** Line 1764 in `get_spread()` passes the raw `spread["use"]` field directly into `faq[3].answer`:
```python
faq = [..., {"question": f"Do I need a full deck for the {spread['title']} spread?",
             "answer": spread["use"] or "A full 78-card deck works best..."}]
```
~30 spreads have `"use": "The twenty-two Major cards."` or similar. This identical string appears in 30% of spread page bodies → L2 FAIL ("twenty two major cards" 30%).

**Replace the FAQ answer construction with a helper that varies the phrasing:**

```python
def _use_answer(spread: dict, seed: int) -> str:
    use = spread.get("use", "") or ""
    ulow = use.lower()
    if "twenty-two" in ulow or "major cards" in ulow or ("major" in ulow and "card" in ulow):
        variants = [
            f"Yes. Pull the 22 major arcana cards from the deck and set the minor arcana aside before you shuffle. This spread works within that focused range.",
            f"Use the major arcana only -- all 22 cards. Separate them from the full deck before you begin so the reading stays within the archetypal layer.",
            f"Draw from the 22 major arcana. Their symbolic range fits the scope of this spread better than the full 78-card deck.",
            f"Major arcana only (22 cards). Setting the minor arcana aside keeps the reading focused on the broader life-theme language those cards carry.",
        ]
        return variants[seed % 4]
    if "minor" in ulow and "court" in ulow:
        variants = [
            f"Use the 56 minor arcana cards -- the 40 pip cards and 16 court cards. Leave the major arcana out of the shuffle.",
            f"Draw from the minor arcana only (pip and court cards across all four suits). The major arcana are not needed for this layout.",
            f"The spread works with the 56-card minor arcana set. Separating them from the major arcana keeps the reading in the everyday-action register.",
            f"Pull the minor arcana -- the numbered pip cards and all 16 court cards -- and set the 22 major arcana aside before shuffling.",
        ]
        return variants[seed % 4]
    # Default: full deck
    full_variants = [
        "A full 78-card deck. No separation needed -- shuffle the complete deck and draw from anywhere.",
        "The full 78-card deck works best here. Keep all suits and arcana together when you shuffle.",
        "Use the complete deck of 78 cards. This spread draws on the full symbolic range.",
        "All 78 cards. Do not separate the deck before shuffling.",
    ]
    return full_variants[seed % 4]
```

Then in `get_spread()`, replace the FAQ use answer:
```python
use_seed = _hash_index(spread["slug"], "use_ans", modulus=4)

faq = [
    {"question": f"What is the {spread['title']} tarot spread for?", "answer": spread["purpose"]},
    {"question": f"How many cards are in the {spread['title']} spread?", "answer": q2_answers[q2_seed]},
    {"question": f"When should I use the {spread['title']} spread?", "answer": q3_answers[q3_seed]},
    {"question": f"Do I need a full deck for the {spread['title']} spread?",
     "answer": _use_answer(spread, use_seed)},        # ← replaces spread["use"]
]
```

**Why 4 variants with modulus=4 is sufficient:** Major-arcana-only spreads number ~30 pages. With 4 variants and even distribution: 30/4 = 7.5 pages per slot = 7.5% < 15% ✅.

---

## Fix 3 -- Spreads FAQ q3 variant 2: Rephrase "holding layers quick pull collapse" (Spreads L2)

**Root cause:** Line 1753 in `q3_answers`:
```python
f"When the {spread['chapter'].lower()} question you are holding has layers that a quick pull would collapse. This layout is designed to keep those layers visible.",
```
After stop-word filtering, this produces 4-grams "holding layers quick pull", "layers quick pull collapse" at 17%.

**Replace line 1753 (the third item in q3_answers, index 2) with:**
```python
f"When the {spread['chapter'].lower()} question has more than one moving part and a single card would compress them into one answer. This layout keeps each part in its own position.",
```

**Verify:** After stop filtering: chapter-word, "question", "moving", "part", "single", "card", "compress", "answer", "layout", "keeps", "part", "position" → no 4-gram appears on > 15% of pages. ✅

---

## Fix 4 -- Intentions FAQ int_q1 variant 7: Rephrase "position labelled choosing spread" (Intentions L2)

**Root cause:** Line 2827, the 8th item (index 7) in `int_q1_answers`:
```python
f"The best spread for {payload['label'].lower()} is the one whose positions match what you actually need to know. Check how each position is labelled before choosing - a spread that names the right questions will read more clearly than a general one.",
```
After stop filtering, produces 4-grams "position labelled choosing spread", "how position labelled choosing", "read clearly general one" at 35%.

**Replace line 2827 (index 7, the last item in int_q1_answers) with:**
```python
f"For {payload['label'].lower()}, the right spread is one where the card positions map directly to the parts of your question. When each card holds a distinct scope, the reading builds a coherent picture rather than overlapping itself.",
```

**Verify:** After stop filtering: label-words, "right", "spread", "one", "card", "positions", "map", "directly", "parts", "question", "card", "holds", "distinct", "scope", "reading", "builds", "coherent", "picture", "rather", "overlapping", "itself" → no run of 4 consecutive stop-filtered tokens matches any high-frequency pattern. ✅

---

## Execution Order

1. Apply Fix 1 (scan script) -- this does NOT change any app code
2. Apply Fixes 2, 3, 4 (all in `backend/tarot_seo_data.py`)
3. Run scan once after all four fixes

---

## L1 Guard -- Must Not Regress

Current L1: Spreads 43.8%, Cards 34.8%, Intentions 16.3%.

All four changes:
- Fix 1: scan script only → no change to L1 inputs
- Fix 2: replaces raw `spread["use"]` with hash-selected variants → slight structural variety, no L1 risk
- Fix 3: rephrases one q3 variant → no new shared vocabulary introduced
- Fix 4: rephrases one int_q1 variant → no new shared vocabulary introduced

None of these changes introduce structural repetition. L1 must not regress on any type.

---

## Acceptance Criteria

Single run of `python3 tests/echo_pace_seoc_tarot_scan.py`:

| Type | L1 | L2 | L3 |
|---|---|---|---|
| Spreads | < 50% (must not regress from 43.8%) | 0 violations | < 60% |
| Cards | < 50% (must not regress from 34.8%) | 0 violations | < 60% |
| Intentions | < 50% (must not regress from 16.3%) | 0 violations | < 60% |

All three must pass simultaneously. Do not commit until the scan is clean.
