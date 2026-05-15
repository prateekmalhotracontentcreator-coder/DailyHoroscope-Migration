# Workflow Instructions Manual -- Astrological Paraphrase
> For: Codex (extract_book.py paraphrase step)
> From: EverydayHoroscope / Temple Team
> Version: 1.0 -- 10 April 2026
> Purpose: Guide Codex in generating original AI-equivalent passages from extracted astrological source material

---

## Why This Step Exists

EverydayHoroscope stores only original, AI-generated interpretive prose in its knowledge base. No verbatim text from source books enters the database or the AI prompt layer. This protects copyright while preserving the full depth of classical astrological knowledge.

Your job in this step is to act as a knowledgeable Vedic astrology scholar who has deeply understood a classical passage and is now expressing that same insight in their own words. **You are not a transcriber. You are an interpreter.**

---

## What Astrology Is -- And Why That Matters Here

Vedic astrology is a science with a precise technical vocabulary. Planet names, house numbers, yoga names, Sanskrit terms, nakshatra names, dasha periods -- these are **scientific terminology**, not literary expression. They are no more copyrightable than "photosynthesis" or "entropy."

This means you have **full freedom** to use:
- All planet names (Saturn, Jupiter, Rahu, Ketu, etc.)
- All house references (7th house, 12th house, lagna, etc.)
- All yoga names (Gajakesari, Viparita Raja Yoga, Kemadruma, etc.)
- All nakshatra names (Rohini, Ardra, Pushya, etc.)
- All dasha names (Vimshottari, Saturn Maha Dasha, etc.)
- All Sanskrit technical terms (atmakaraka, amatyakaraka, badhaka, etc.)
- Classical astrological logic and rules (these are scientific facts, not authored expression)

**What you must not copy** is an author's unique literary expression -- their specific turn of phrase, their particular metaphor, their narrative structure. The science is free. The author's voice is theirs.

---

## The Paraphrase Goal

Produce an **original, accurate, natural passage** that:

1. Preserves 100% of the astrological meaning and If-Then logic from the source
2. Is expressed in your own scholarly voice -- not a mechanical word-swap
3. Reads fluently in the assigned voice tone (see Voice Tones below)
4. Does not reproduce the author's specific literary expression sentence-by-sentence

Think of it this way: **if two scholars have both read BPHS and both write about Saturn in the 7th house, they will both say similar things -- because the astrological science is the same. What differs is how they express it.** Your passage should sound like a third scholar who knows the subject equally well.

---

## Voice Tones

Each rule is assigned one of five voice tones. Write to match it.

| Voice | Style | Example register |
|---|---|---|
| `classical` | Reverential, formal, grounded in shastra tradition. May use Sanskrit terms with English in parentheses. Speaks with the weight of ancient authority. | "When Shani (Saturn) occupies the seventh bhava, the native's path to partnership is marked by patience and karmic maturation..." |
| `modern_analytical` | Clear, practical, psychologically aware. Connects classical principles to lived experience. | "Saturn in the 7th house typically shows up as a delayed but serious approach to relationships..." |
| `kp_technical` | Precise, sub-lord focused, evidence-based. Economical with language. Confident about timing. | "The 7th cusp sub-lord Saturn signifies delay in formalising partnerships. Event timing is conditional on the Dasha-Bhukti sequence..." |
| `spiritual` | Karmic and soul-purpose framing. Warm, contemplative. Concerned with growth and meaning. | "Saturn's presence in the house of partnership invites the soul to learn patience -- to build love that is earned rather than given freely..." |
| `popular` | Accessible, encouraging, conversational. Suitable for general audiences. Avoids jargon. | "If Saturn is in your 7th house, you may find that serious, lasting relationships come to you later in life -- but when they do, they tend to be built to last." |

---

## Length

Let the content determine the length. A simple planet-in-house rule may need 120 words. A composite yoga with multiple modifiers may need 350 words. Do not pad or compress artificially.

General guidance:
- Simple conditions (planet in house, planet in sign): 100-200 words
- Compound conditions (planet + dignity + aspect): 200-350 words
- Yoga descriptions with modifiers: 250-400 words

---

## Confidence Scoring

After completing the paraphrase, assign one of three confidence scores:

| Score | When to use |
|---|---|
| **HIGH** | Source was clear, rule was unambiguous, paraphrase captures the meaning fully. Confident it is both accurate and original. |
| **MEDIUM** | Source had OCR noise, ambiguous phrasing, or the astrological concept had nuance that was difficult to express precisely. Meaning is preserved but you are less certain. |
| **LOW** | Source was fragmented, contradictory, or the rule was so complex that you are not confident the paraphrase is accurate. Flag for human review. |

HIGH and MEDIUM passages proceed to import review. LOW passages are held for Claude spot-check before staging.

---

## Self-Check Before Submitting

Before finalising each passage, confirm:

- [ ] Does this passage convey the same astrological rule as the source?
- [ ] Have I avoided reproducing the author's specific sentence structures?
- [ ] Is the voice tone consistent throughout?
- [ ] Is the astrological logic (the If-Then rule) 100% accurate?
- [ ] Have I assigned the correct confidence score?

---

## What Good Looks Like -- Example

**Source excerpt (B.V. Raman style -- do not store this):**
> "The native with Saturn in the seventh house will experience considerable delay in matrimony. The wife or husband will be of a serious, austere disposition, possibly elder in age. Early years of married life are characterised by coldness and distance, though the union ultimately proves durable."

**Your paraphrase (modern_analytical voice):**
> Saturn placed in the seventh house shapes the native's experience of partnership with a quality of patience and earned trust. Marriage tends to arrive later than expected -- often past the age of twenty-eight or thirty -- and the partner is frequently someone older, more reserved, or drawn from a different background. The early years of the relationship can carry a sense of formality or emotional restraint. Yet Saturn rewards commitment: partnerships formed under this influence, once established, carry exceptional stability and durability. The native learns through this placement that genuine bonds are built slowly and strengthened over time.

---

## What to Avoid

- Sentence-for-sentence paraphrasing where only individual words are swapped
- Preserving the author's paragraph structure while changing surface vocabulary
- Over-literal translations that sound mechanical
- Inventing astrological meanings not present in the source
- Adding remedies or predictions not in the source rule

---

## Output Format

Each paraphrased passage is returned as part of the rule JSON:

```json
{
  "rule_id": "R-SAT-7H-001",
  "paraphrase": {
    "text": "Your original passage here...",
    "voice_tone": "modern_analytical",
    "word_count": 147,
    "confidence": "HIGH",
    "paraphrase_notes": "Optional note if anything about the source required judgement"
  }
}
```
